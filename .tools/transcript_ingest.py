#!/usr/bin/env python3
"""
transcript_ingest.py — 真相层（原始会话）抽取器（C 档 · v7）

把原始记录抽成 brain 自有的长期库：对话文字（含中途插话、后台任务回报）+ 工具调用参数
（每条上限 8KB）+ 工具结果（每条截前 2KB），逐条脱敏。

来源（--source 标签=路径，可重复；不给则用默认三处本机来源）：
  code      ~/.claude/projects                                   （Claude Code）
  cowork    ~/Library/Application Support/Claude/local-agent-mode-sessions     （官方 Cowork）
  cowork3p  ~/Library/Application Support/Claude-3p/local-agent-mode-sessions  （Gateway 模式 Cowork）
  除 code 外，只收路径中含 /.claude/projects/ 的会话文件；audit.jsonl（带签名的审计日志，
  对话部分与会话文件重合）与 outputs/ 下的产物不收。

输出：brain/chats/transcripts/YYYY-MM/<首条本地日期>_<来源>_<会话文件名>_<路径哈希10位>.jsonl.gz
  第 1 行 header；其后每行一条记录：
  {"uid","ts","role": user|assistant|notification,"kind": text|tool_use|tool_result,
   "tool"?,"tool_use_id"?,"is_error"?,"truncated"?,"queued"?,"text"}
  uid＝消息 uuid#块序号，跨文件重复（续接会话复制历史）由检索端按 uid 去重。
  日期一律按本机时区。

保全：源被清理后抽取件不删；源变小，或重抽后的记录不再覆盖旧抽取件的全部 uid（源被改写）时，
  旧件改名为 *.superseded-<时间>.jsonl.gz 保留，再写新件。
增量：_state.json 记每个来源文件的 (size, mtime)；未变跳过。状态文件损坏时备份后从空重建。
并发：抽取目录加文件锁，第二个进程直接退出（退出码 3）。对源只读。

PRD：brain/logs/checkpoints/2026-11-19_真相层_PRD.md
"""
import argparse
import fcntl
import gzip
import hashlib
import json
import os
import re
import sys
import time
from collections import Counter
from datetime import datetime
from pathlib import Path

EXTRACTOR = "transcript_ingest/7"
TOOL_RESULT_CAP = 2000
TOOL_INPUT_CAP = 8000
HOME = Path(os.path.expanduser("~"))
APP = HOME / "Library" / "Application Support"
DEFAULT_SOURCES = [
    ("code", HOME / ".claude" / "projects"),
    ("cowork", APP / "Claude" / "local-agent-mode-sessions"),
    ("cowork3p", APP / "Claude-3p" / "local-agent-mode-sessions"),
]
DEFAULT_DST = HOME / "Documents" / "Claude" / "brain" / "chats" / "transcripts"
SAVE_EVERY = 50

# ---------- 脱敏（v4：形态规则 + 键值规则 + 高熵兜底；规则收窄以减误伤） ----------
import math as _math

_S = r"[A-Za-z0-9_\-./+=]"
_Q = r"(?:\\?[\"'`“”‘’「」])?"  # 可带转义的引号（JSON 里 \" 也认）、反引号、弯引号、直角引号
_SEP = r"[ \t]*[:=：＝][ \t]*"   # 半角/全角冒号、等号（不跨行）
_MASK = r"(?:[*•·.…]+|\(redacted\)|\[redacted\]|<[^>\n]{0,20}>|[ \t])*"  # 部分遮掩：***、(redacted)、<前10位隐藏> 等
_VAL = r"[A-Za-z0-9_\-./+=%]"

# 令牌/密钥类键名（大小写不敏感，允许 secret key / access key id 这种中间带空格的写法）
_SECRET_KEY = (r"(?:[A-Za-z0-9_\-]*(?:token|secret|api[ _\-]?key|access[ _\-]?key(?:[ _\-]?id)?|accesskeyid|"
               r"secret[ _\-]?key|auth[ _\-]?key|app[ _\-]?key|private[ _\-]?key|signature)[A-Za-z0-9_\-]*)")
# 键名里出现这些词的不算密钥（计数、上限、路径、标识等）
_KEY_SKIP = re.compile(r"(?i)(tokens\b|tokens_|_tokens|tokenizer|token_?(count|limit|budget|usage|len|num|type|file|path|dir)|"
                       r"(file|path|dir|url|name|count|limit|len|length|type|hash|_id_?path)$|keyword|signature_?(version|method|type))")
_PASS_KEY = r"(?:[A-Za-z0-9_\-]*(?:passw(?:or)?d|pwd)[A-Za-z0-9_\-]*)"
_PASS_SKIP_KEYS = {"PWD", "OLDPWD", "nPWD", "nOLDPWD"}  # shell 工作目录变量（JSON 里 \nPWD 会被读成 nPWD）
_PASS_SKIP_SUFFIX = ("_file", "-file", "_url", "-url", "_hash", "_reset", "_path", "_policy", "_length", "_len", "_url_")


def _looks_path(v):
    return v.startswith(("/", "~", "./", "../", "$", "http://", "https://"))


def _assign_repl(m):
    key, sep, val = m.group(1), m.group(2), m.group(3)
    if _KEY_SKIP.search(key) or _looks_path(re.sub(r"^(?:[*•·.]+|\(redacted\)|\[redacted\]|<[^>]{0,20}>|\s)*", "", val)):
        return m.group(0)
    return f"{key}{sep}[REDACTED:assign]"


def _passwd_repl(m):
    key, sep, val = m.group(1), m.group(2), m.group(3)
    k = key.lower()
    if key in _PASS_SKIP_KEYS or k.endswith(_PASS_SKIP_SUFFIX) or "reset" in k or _looks_path(val):
        return m.group(0)
    return f"{key}{sep}[REDACTED:assign]"


_HASH_CTX = re.compile(r"(?i)(sha\d*|md5|hash|digest|commit|checksum|etag|blob|tree|ref)\W{0,30}$")


def _hexnear_repl(m):
    if _HASH_CTX.search(m.group(1)[-40:]):
        return m.group(0)
    return m.group(1) + "[REDACTED:hex]"


def _entropy(s):
    n = len(s)
    return -sum(c / n * _math.log2(c / n) for c in (s.count(ch) for ch in set(s)))


# 高熵兜底（收窄版）：只认 ≥32 位、只含字母数字与 + /、大小写字母和数字俱全、香农熵≥4.5、不像单词或路径的串。
# 收窄是为了少误伤（URL 参数、标识符、路径段）；本机已知凭证由黑名单精确兜住。
_WORDISH = re.compile(r"[A-Z]?[a-z]{4,}")


def _is_secretish(v, min_len=32):
    if len(v) < min_len:
        return False
    if not (re.search(r"[A-Z]", v) and re.search(r"[a-z]", v) and re.search(r"[0-9]", v)):
        return False
    if _entropy(v) < 4.5:
        return False
    return sum(len(w) for w in _WORDISH.findall(v)) <= 0.4 * len(v)


# 前文是这些的高熵串是公开标识或内容哈希，不遮：SRI 完整性哈希、YouTube 列表/视频 ID、data URI
_PUBLIC_CTX = re.compile(r"(?i)(sha(?:256|384|512)-|[?&]list=|[?&]v=|youtu\.be/|;base64,|data:[\w/+.\-]+,)$")


def _highent_repl(m):
    v = m.group(0)
    if _PUBLIC_CTX.search(m.string[max(0, m.start() - 40):m.start()]):
        return v
    if "/" not in v:
        return "[REDACTED:highent]" if _is_secretish(v) else v
    if "+" in v and _is_secretish(v.replace("/", "")):
        return "[REDACTED:highent]"
    return "/".join("[REDACTED:highent]" if _is_secretish(seg) else seg for seg in v.split("/"))


# ---------- 已知凭证黑名单（运行时从本机凭证文件读入内存，不落盘） ----------
KNOWN_FULL = []        # 完整凭证值，按长度降序
KNOWN_WIN = set()      # 凭证的 8 字符窗口（用于遮掉碎片）
_WIN = 8
_SECRET_NAME = re.compile(r"(?i)(token|key|secret|pass|pwd|auth|cookie|sid|credential|(?:^|_)(?:ak|sk)$)")
_RUN = re.compile(r"[A-Za-z0-9+/=_\-.]{%d,}" % _WIN)


def _window_ok(w):
    classes = sum(bool(re.search(p, w)) for p in (r"[A-Z]", r"[a-z]", r"[0-9]"))
    return classes >= 2 and len(set(w)) >= 5


def set_known_secrets(values):
    global KNOWN_FULL, KNOWN_WIN
    vals = sorted({v for v in values if len(v) >= 12}, key=len, reverse=True)
    KNOWN_FULL = vals
    win = set()
    for v in vals:
        # 值里有 _RUN 字符类以外的字符（: @ ! 等）时按它们分段，各段单独取窗口，否则跨段窗口在文本里永远匹配不上
        for seg in re.split(r"[^A-Za-z0-9+/=_\-.]", v):
            win.update(seg[i:i + _WIN] for i in range(len(seg) - _WIN + 1) if _window_ok(seg[i:i + _WIN]))
    KNOWN_WIN = win


LOAD_STATS = {"list_missing": False, "failed": 0}
_PLACEHOLDER = re.compile(r"(?i)(your[_\-]|xxx|change[_\-]?me|placeholder|example|dummy|sample|replace[_\-]?me|\*{3,})")
_HOSTNAME = re.compile(r"[a-z0-9\-]+(\.[a-z0-9\-]+)*\.[a-z]{2,10}(:\d+)?")  # 全小写主机名


def _value_ok(v):
    """值的形态门槛：排除纯字母单词、主机名、占位词、环境变量名，只留像凭证的值。"""
    if len(v) < 12 or " " in v or v.startswith(("/", "~", "$", "http://", "https://")):
        return False
    if _PLACEHOLDER.search(v) or _HOSTNAME.fullmatch(v):
        return False
    if re.fullmatch(r"[A-Z_]+", v) and "_" in v:  # 另一个环境变量名
        return False
    if not re.search(r"[0-9]", v) and len(v) < 24:  # 不含数字的短串多是单词（Authorization 等）
        return False
    classes = sum(bool(re.search(p, v)) for p in (r"[A-Z]", r"[a-z]", r"[0-9]"))
    return classes >= 2


def load_known_secrets(sources_file):
    """读凭证文件里的值（只进内存）。返回 (值列表, 读到的文件数)。"""
    import glob as _glob
    vals, nfiles = [], 0
    LOAD_STATS.update(list_missing=False, failed=0)
    if not sources_file or not Path(sources_file).exists():
        LOAD_STATS["list_missing"] = True
        return vals, 0
    try:
        listing = Path(sources_file).read_text(encoding="utf-8").splitlines()
    except Exception:
        LOAD_STATS["list_missing"] = True  # 清单读不了按「不存在」处理（fail-closed，退出码 4）
        return vals, 0
    for raw in listing:
        pat = raw.strip()
        if not pat or pat.startswith("#"):
            continue
        for fp in _glob.glob(os.path.expanduser(pat), recursive=True):
            if not os.path.isfile(fp) or fp.endswith((".example", ".sample", ".template")):
                continue
            try:
                text = Path(fp).read_text(encoding="utf-8", errors="ignore")
            except Exception:
                LOAD_STATS["failed"] += 1
                continue
            nfiles += 1
            lines = [l for l in text.splitlines() if l.strip() and not l.lstrip().startswith("#")]
            one = lines[0].strip().strip("\"'") if len(lines) == 1 else ""
            if one and ("=" not in one or re.fullmatch(r"[A-Za-z0-9+/_\-]+=*", one)):
                vals.append(one)  # 纯令牌文件（含以 = 补齐的 base64）
                continue
            for l in lines:
                l = re.sub(r"^\s*export\s+", "", l)
                if "=" not in l:
                    continue
                k, v = l.split("=", 1)
                v = v.strip()
                if v and v[0] in "\"'":  # 注意空串：'' in "..." 恒为真
                    v = v[1:].split(v[0], 1)[0]
                else:
                    v = v.split(" #", 1)[0].strip()
                k = k.strip()
                if len(v) > 2 and v[0] == "<" and v[-1] == ">":  # 有人把真值包在尖括号里，取里面的值再判
                    v = v[1:-1].strip()
                if "://" in v and "@" in v:  # 带口令的连接串（postgres://user:pass@host）
                    if not re.search(r"@(localhost|127\.0\.0\.1|0\.0\.0\.0)\b", v) and not _PLACEHOLDER.search(v):
                        vals.append(v)
                    continue
                if not _value_ok(v):
                    continue
                if _SECRET_NAME.search(k):
                    vals.append(v)
    return vals, nfiles


def _redact_known(text, counter):
    if not KNOWN_FULL:
        return text
    for v in KNOWN_FULL:
        if v in text:
            counter["known"] += text.count(v)
            text = text.replace(v, "[REDACTED:known]")

    def repl(m):
        run = m.group(0)
        n = len(run)
        cov = bytearray(n)
        for i in range(n - _WIN + 1):
            if run[i:i + _WIN] in KNOWN_WIN:
                cov[i:i + _WIN] = b"\x01" * _WIN
        if not any(cov):
            return run
        out, i = [], 0
        while i < n:
            if cov[i]:
                j = i
                while j < n and cov[j]:
                    j += 1
                out.append("[REDACTED:known]")
                counter["known"] += 1
                i = j
            else:
                out.append(run[i])
                i += 1
        return "".join(out)
    return _RUN.sub(repl, text)


def _akso_repl(m):
    """整词 AK/SK：值是路径（shell 变量 SK=/sessions/...）时不遮。"""
    if _looks_path(m.group(3)) or "/sessions" in m.group(3):
        return m.group(0)
    return f"{m.group(1)}{m.group(2)}[REDACTED:assign]"


def _cli_repl(m):
    if _looks_path(m.group(2)):
        return m.group(0)
    return m.group(1) + "[REDACTED:assign]"


def _sk_repl(m):
    """sk- 开头的 URL 词串（sk-hynix-hbm4-shipments…）不是密钥：三段以上连字符、且有两段以上是 3 个字母以上的纯小写单词。"""
    tail = m.group(0)[3:]
    segs = tail.split("-")
    if len(segs) >= 3 and sum(1 for x in segs if re.fullmatch(r"[a-z]{3,}", x)) >= 2:
        return m.group(0)
    return "[REDACTED:sk]"


REDACTIONS = [
    # —— 形态规则（各家密钥前缀）——
    ("pem", re.compile(r"-----BEGIN [A-Z0-9 ]*PRIVATE KEY-----(?:[A-Za-z0-9+/=\s]|\\[nr])*(?:-----END [A-Z0-9 ]*PRIVATE KEY-----)?"), "[REDACTED:pem]"),
    ("anthropic", re.compile(r"sk-ant-[A-Za-z0-9_\-]{20,}"), "[REDACTED:anthropic]"),
    ("sk", re.compile(r"(?<![\w\-])sk-(?:proj-)?(?=[A-Za-z0-9_\-]*\d)[A-Za-z0-9_\-]{20,}"), _sk_repl),  # 前面不能是字母数字或连字符（避开 samsung-sk-hynix 一类 URL 词）
    ("sk_hex", re.compile(r"\bsk_[0-9a-f]{32,}\b"), "[REDACTED:sk]"),
    ("github", re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,})"), "[REDACTED:github]"),
    ("aws", re.compile(r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b"), "[REDACTED:aws]"),
    ("volc", re.compile(r"\bAKLT[A-Za-z0-9+/=_\-]{20,}"), "[REDACTED:volc]"),
    ("aliyun", re.compile(r"\bLTAI[A-Za-z0-9]{12,}"), "[REDACTED:aliyun]"),
    ("gitlab", re.compile(r"\bglpat-[A-Za-z0-9_\-]{20,}"), "[REDACTED:gitlab]"),
    ("hf", re.compile(r"\bhf_[A-Za-z0-9]{30,}"), "[REDACTED:hf]"),
    ("notion", re.compile(r"\b(?:ntn_[A-Za-z0-9]{20,}|secret_[A-Za-z0-9]{30,})"), "[REDACTED:notion]"),
    ("zhipu", re.compile(r"\b[0-9a-f]{32}\.[A-Za-z0-9]{16}\b"), "[REDACTED:zhipu]"),
    ("google", re.compile(r"\bAIza[0-9A-Za-z_\-]{35}"), "[REDACTED:google]"),
    ("slack", re.compile(r"\bxox[abprs]-[A-Za-z0-9\-]{10,}"), "[REDACTED:slack]"),
    ("jwt", re.compile(r"\beyJ[A-Za-z0-9_\-]{10,}\.eyJ[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}"), "[REDACTED:jwt]"),
    ("url_pass", re.compile(r"(\b[a-zA-Z][a-zA-Z0-9+.\-]*://[^\s:/@\"']+:)([^\s@/\"']{3,})@"), r"\1[REDACTED:url]@"),
    ("bearer", re.compile(r"(?i)\b(bearer\s+)" + _S + r"{16,}"), r"\1[REDACTED:bearer]"),
    ("api_call", re.compile(r"(?i)((?:set_token|pro_api)\(\s*(?:token\s*=\s*)?" + _Q + r")" + _S + r"{16,}"), r"\1[REDACTED:token]"),
    # .env 里没写键名的裸值被 shell 当命令执行后打印出来
    ("env_bare", re.compile(r"(\.env: line \d+: )([^\s:]{12,})(: command not found)"), r"\1[REDACTED:assign]\3"),
    # —— 键值规则 ——
    ("env_default", re.compile(
        r"(?i)((?:get|getenv)\(\s*" + _Q + r"[A-Za-z0-9_]*(?:token|secret|api_?key|access_?key|secret_?key|passw\w*)[A-Za-z0-9_]*" + _Q
        + r"\s*,\s*" + _Q + r")((?=[^\"'\\\s)]*[0-9])[^\"'\\\s)]{12,})"), r"\1[REDACTED:assign]"),
    ("passwd", re.compile(
        r"(?i)\b(" + _PASS_KEY + r")(\**" + _Q + _SEP + _Q + r")(?!\[REDACTED)([^\s\"'\\,;}{&，。`”’」]{6,})"), _passwd_repl),
    ("assign", re.compile(
        r"(?i)\b(" + _SECRET_KEY + r")(\**" + _Q + _SEP + _Q + r")(?!\[REDACTED)(" + _MASK + r"(?=" + _VAL + r"*[0-9])" + _VAL + r"{16,})"),
        _assign_repl),
    # 中文键名：密码/口令/令牌/密钥 + 可选「是/为」+ 可选分隔符 + ASCII 值（含数字或≥16 位）
    ("cn_assign", re.compile(r"((?:密码|口令|令牌|密钥|秘钥|私钥|凭证|授权码)(?:[（(][^）)\n]{1,20}[）)])?(?:[ \t]*(?:是|为))?[ \t]*[:：=＝]?[ \t]*" + _Q + r")(?!\[REDACTED)((?=[A-Za-z0-9_\-./+=@!#$%^&*]*\d)[A-Za-z0-9_\-./+=@!#$%^&*]{8,}|[A-Za-z0-9_\-./+=@!#$%^&*]{16,})"), r"\1[REDACTED:assign]"),
    # 整词 AK / SK（大小写敏感，火山等平台的习惯写法）
    ("ak_sk", re.compile(r"\b(AK|SK)(" + _Q + _SEP + _Q + r")(?!\[REDACTED)(" + _VAL + r"{16,})"), _akso_repl),
    # 命令行参数：--token 值 / --api-key=值 / --password 值
    ("cli_flag", re.compile(r"(?i)(--(?:api[-_]?key|token|secret|password|passwd|access[-_]?key|secret[-_]?key)(?:=|[ \t]+)" + _Q + r")(?![\[$<])(" + _VAL + r"{12,})"),
     _cli_repl),
    # —— 浏览器会话 cookie（大小写敏感，避免吞掉驼峰的 sessionId）——
    ("cookie_hdr", re.compile(r"(?im)((?:^|[\"'\s])(?:set-)?cookie:\s*)([^\n\"'\\]*=[^\n\"'\\]*;[^\n\"'\\]*)"), r"\1[REDACTED:cookie]"),
    ("cookie_kv", re.compile(
        r"\b(\w*SESSIONID\w*|\w*sessionid(?:_ss)?|sid_tt|sid_guard|uid_tt(?:_ss)?|odin_tt|d_ticket|ttwid|passport_csrf_token(?:_default)?|"
        r"msToken|s_v_web_id|__ac_signature|sso_uid_tt(?:_ss)?|toutiao_sso_user(?:_ss)?|sid_ucp_v1|ssid_ucp_v1|UIFID\w*|_?bd_ticket\w*)"
        r"(" + _Q + r"\s*[:=]\s*" + _Q + r")([A-Za-z0-9_\-.%|=+/]{12,})"), r"\1\2[REDACTED:cookie]"),
    # —— 十六进制 ——
    ("hex_near", re.compile(
        r"(?i)((?<![A-Za-z])(?:tushare|token|secret|api[_\-]?key|access[_\-]?key|auth|authorization|令牌|密钥|口令)(?![a-z])[^\n]{0,80}?)(?<![0-9a-f])[0-9a-f]{32,64}(?![0-9a-f])"),
        _hexnear_repl),
    ("hex56", re.compile(r"(?i)(?<![0-9a-z])[0-9a-f]{56}(?![0-9a-z])"), "[REDACTED:hex]"),
    # —— 高熵兜底：≥32 位、只含字母数字与 + /、大小写字母和数字俱全、香农熵≥4.5 的串（无键名的随机串）——
    ("highent", re.compile(r"(?<![A-Za-z0-9+/])[A-Za-z0-9+/]{32,}(?![A-Za-z0-9+/])"), _highent_repl),
]


def redact(text, counter):
    text = _redact_known(text, counter)
    for name, rx, repl in REDACTIONS:
        new = rx.sub(repl, text)
        if new != text:
            counter[name] += new.count("[REDACTED:") - text.count("[REDACTED:")
            text = new
    return text


def redact_obj(obj, counter):
    """递归脱敏 JSON 值里的每个字符串（含键名不动），再由调用方序列化。"""
    if isinstance(obj, str):
        return redact(obj, counter)
    if isinstance(obj, list):
        return [redact_obj(x, counter) for x in obj]
    if isinstance(obj, dict):
        return {k: redact_obj(v, counter) for k, v in obj.items()}
    return obj


def cap_bytes(s, cap):
    b = s.encode("utf-8")
    if len(b) <= cap:
        return s, False
    return b[:cap].decode("utf-8", errors="ignore"), True


def local_day(ts):
    """ISO 时间（多为 UTC 'Z'）→ 本机时区日期 YYYY-MM-DD；解析失败退回前 10 位。"""
    if not ts:
        return ""
    try:
        return datetime.fromisoformat(ts.replace("Z", "+00:00")).astimezone().strftime("%Y-%m-%d")
    except Exception:
        return ts[:10]


# ---------- 抽取 ----------
def _blocks_text(content):
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for i in content:
            if not isinstance(i, dict):
                continue
            t = i.get("type")
            if t == "text":
                parts.append(i.get("text", ""))
            elif t == "image":
                parts.append("[image]")
            elif t == "tool_reference":
                parts.append(f"[tool_reference: {i.get('tool_name') or i.get('name') or ''}]")
            elif t == "document":
                parts.append("[document]")
        return "\n".join(parts)
    return "" if content is None else str(content)


def _epoch(ts):
    try:
        return datetime.fromisoformat(ts.replace("Z", "+00:00")).timestamp()
    except Exception:
        return None


def extract_session(path, red):
    """返回 (header, records, bad_lines)。只读源文件。"""
    records, queued, bad = [], [], 0
    ph = hashlib.sha1(str(path).encode("utf-8")).hexdigest()[:10]  # 无 uuid 时的回退前缀，防跨文件撞 uid
    lineno = 0
    title = None
    first_ts = last_ts = None
    sidechain = False
    with open(path, "rb") as f:
        for raw in f:
            lineno += 1
            try:
                d = json.loads(raw)
            except Exception:
                bad += 1
                continue
            if not isinstance(d, dict):
                bad += 1
                continue
            t = d.get("type")
            if t == "ai-title" and d.get("aiTitle"):
                title = d.get("aiTitle")
            elif t == "custom-title" and d.get("customTitle"):
                title = d.get("customTitle")
            ts = d.get("timestamp")
            if t == "attachment":
                a = d.get("attachment") or {}
                if a.get("type") == "queued_command":
                    txt = _blocks_text(a.get("prompt")).strip()
                    if txt:
                        role = "user" if a.get("commandMode") == "prompt" else "notification"
                        queued.append({"uid": f"{d.get('uuid') or a.get('delivery_id') or ph + ':L' + str(lineno)}#q", "ts": ts or a.get("timestamp"),
                                       "role": role, "kind": "text", "queued": True, "text": txt})
                continue
            if t not in ("user", "assistant"):
                continue
            if ts:
                first_ts = ts if first_ts is None or ts < first_ts else first_ts
                last_ts = ts if last_ts is None or ts > last_ts else last_ts
            if d.get("isSidechain"):
                sidechain = True
            uuid = d.get("uuid") or (d.get("message") or {}).get("id") or f"{ph}:L{lineno}"
            content = (d.get("message") or {}).get("content")
            role = t
            if isinstance(content, str):
                if content.strip():
                    r = "notification" if content.lstrip().startswith("<task-notification>") else role
                    records.append({"uid": f"{uuid}#0", "ts": ts, "role": r, "kind": "text", "text": redact(content, red)})
                continue
            if not isinstance(content, list):
                continue
            for i, blk in enumerate(content):
                if not isinstance(blk, dict):
                    continue
                bt = blk.get("type")
                uid = f"{uuid}#{i}"
                if bt == "text":
                    txt = blk.get("text") or ""
                    if txt.strip():
                        records.append({"uid": uid, "ts": ts, "role": role, "kind": "text", "text": redact(txt, red)})
                elif bt == "tool_use":
                    s = json.dumps(redact_obj(blk.get("input"), red), ensure_ascii=False)
                    s, cut = cap_bytes(redact(s, red), TOOL_INPUT_CAP)
                    rec = {"uid": uid, "ts": ts, "role": role, "kind": "tool_use", "tool": blk.get("name"),
                           "tool_use_id": blk.get("id"), "text": s}
                    if cut:
                        rec["truncated"] = True
                    records.append(rec)
                elif bt == "tool_result":
                    # 先脱敏再截断：先截会切断密钥使正则漏网
                    s, cut = cap_bytes(redact(_blocks_text(blk.get("content")), red), TOOL_RESULT_CAP)
                    rec = {"uid": uid, "ts": ts, "role": role, "kind": "tool_result",
                           "tool_use_id": blk.get("tool_use_id"), "text": s}
                    if blk.get("is_error"):
                        rec["is_error"] = True
                    if cut:
                        rec["truncated"] = True
                    records.append(rec)
                # thinking / image 块按 C 档口径不抽取
    # 中途插话：插话后 1 小时内以相同正文正式送达、且该条尚未被别的插话认领的，视为同一条，不重复收
    delivered = {}
    for r in records:
        if r["kind"] == "text" and r["role"] in ("user", "notification"):
            delivered.setdefault(r["text"].strip(), []).append([_epoch(r.get("ts") or ""), False])
    for q in sorted(queued, key=lambda x: x.get("ts") or ""):
        q["text"] = redact(q["text"], red)
        qt = _epoch(q.get("ts") or "")
        matched = False
        for slot in delivered.get(q["text"].strip(), []):
            if not slot[1] and qt is not None and slot[0] is not None and 0 <= slot[0] - qt <= 3600:
                slot[1] = matched = True
                break
        if not matched:
            records.append(q)
            if q["ts"]:
                first_ts = q["ts"] if first_ts is None or q["ts"] < first_ts else first_ts
                last_ts = q["ts"] if last_ts is None or q["ts"] > last_ts else last_ts
    records.sort(key=lambda r: r.get("ts") or "")
    header = {
        "type": "header", "extractor": EXTRACTOR, "title": redact(title, red) if title else title,
        "first_ts": first_ts, "last_ts": last_ts, "sidechain": sidechain,
        "counts": dict(Counter(r["kind"] for r in records)), "bad_lines": bad,
    }
    meta = path.with_name(path.stem + ".meta.json")
    if meta.exists():
        try:
            m = json.loads(meta.read_text(encoding="utf-8"))
            header["agent_type"] = m.get("agentType")
            header["agent_description"] = redact(str(m.get("description") or ""), red)
            header["title"] = header["title"] or header["agent_description"] or None
        except Exception:
            pass
    return header, records, bad


def out_relpath(label, src_rel, first_ts, mtime):
    day = local_day(first_ts) or time.strftime("%Y-%m-%d", time.localtime(mtime))
    h = hashlib.sha1(f"{label}:{src_rel}".encode("utf-8")).hexdigest()[:10]
    return f"{day[:7]}/{day}_{label}_{Path(src_rel).stem}_{h}.jsonl.gz"


def write_atomic_gz(path, lines):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(f"{path.name}.{os.getpid()}.tmp")
    with gzip.open(tmp, "wt", encoding="utf-8", compresslevel=6) as g:
        for obj in lines:
            g.write(json.dumps(obj, ensure_ascii=False) + "\n")
        g.flush()
    with open(tmp, "rb") as fh:
        os.fsync(fh.fileno())
    os.replace(tmp, path)


def _is_superset(target, records):
    """新记录的 uid 集合是否覆盖旧抽取件——不覆盖就说明源被改写，旧件须保全。"""
    try:
        with gzip.open(target, "rt", encoding="utf-8") as g:
            next(g, None)
            old = {json.loads(x).get("uid") for x in g}
    except Exception:
        return False
    old = {u for u in old if not str(u).endswith("#q")}  # 插话之后正式送达会换 uid，不算改写
    return old <= {r.get("uid") for r in records}


def load_state(dst, log):
    p = dst / "_state.json"
    if p.exists():
        try:
            with open(p, encoding="utf-8") as f:
                st = json.load(f)
            if isinstance(st, dict) and isinstance(st.get("sources"), dict):
                return st
            raise ValueError("结构不符")
        except Exception as e:
            bak = p.with_name(f"_state.json.corrupt-{time.strftime('%Y%m%d%H%M%S')}")
            os.replace(p, bak)
            log(f"⚠ 状态文件损坏（{e.__class__.__name__}），已另存为 {bak.name}，从空状态重建")
    return {"version": 2, "sources": {}}


def save_state(dst, state):
    p = dst / "_state.json"
    tmp = p.with_name(f"_state.json.{os.getpid()}.tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=1, sort_keys=True)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, p)


def iter_source_files(label, root):
    for p in sorted(root.rglob("*.jsonl")):
        if p.name == "audit.jsonl":
            continue
        rel = p.relative_to(root).as_posix()
        if label != "code" and "/.claude/projects/" not in "/" + rel:
            continue
        yield p, rel


def run(sources, dst, dry_run=False, log=print, secret_sources=None, accept_secret_change=False):
    dst = Path(dst)
    sources = [(lbl, Path(root)) for lbl, root in sources]
    live = [(l, r) for l, r in sources if r.is_dir()]
    for l, r in sources:
        if not r.is_dir():
            log(f"⚠ 来源 {l} 不存在，跳过：{r}")
    if not live:
        log("❌ 没有可用来源")
        return 2
    if dry_run:
        state, lockf = {"version": 2, "sources": {}}, None
        if (dst / "_state.json").exists():
            try:
                with open(dst / "_state.json", encoding="utf-8") as f:
                    loaded = json.load(f)
                if not isinstance(loaded, dict) or not isinstance(loaded.get("sources"), dict):
                    raise ValueError("结构不符")
                state = loaded
            except Exception:
                log("⚠ 状态文件损坏；dry-run 按空状态估算（实跑时会另存并重建）")
    else:
        dst.mkdir(parents=True, exist_ok=True)
        lockf = open(dst / ".lock", "w")
        try:
            fcntl.flock(lockf, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            log("⏸ 另一个抽取进程正在运行，本次退出")
            return 3
        state = load_state(dst, log)
    if secret_sources is not None:
        vals, nf = load_known_secrets(secret_sources)
        set_known_secrets(vals)
        log(f"已知凭证黑名单：{len(KNOWN_FULL)} 个值（来自 {nf} 个凭证文件，只在内存中使用）")
        # fail-closed：黑名单配置了却没加载起来、有凭证文件读不了、或比上次少，都不写抽取件（无人值守时尤其要紧）
        side = dst / "_secret_baseline.json"
        base = state.get("secret_baseline") or {}
        side_bad = False
        if not base and side.exists():  # 状态文件损坏重建后，基线从旁路文件取回
            try:
                base = json.loads(side.read_text(encoding="utf-8"))
                if not isinstance(base, dict) or not all(isinstance(base.get(k), int) for k in ("files", "values")):
                    raise ValueError
            except Exception:
                base, side_bad = {}, True
        why = None
        if side_bad and not accept_secret_change:
            why = "旁路基线文件 _secret_baseline.json 损坏、无法比对；确认无误后加 --accept-secret-change 重建基线"
        elif LOAD_STATS["list_missing"]:
            why = f"来源清单不存在：{secret_sources}"
        elif nf == 0 or not KNOWN_FULL:
            why = "一个凭证值都没加载到"
        elif LOAD_STATS["failed"]:
            why = f"{LOAD_STATS['failed']} 个凭证文件读取失败"
        elif base and (nf < base.get("files", 0) or len(KNOWN_FULL) < base.get("values", 0)) and not accept_secret_change:
            why = (f"凭证文件/值比上次少（文件 {base.get('files')}→{nf}，值 {base.get('values')}→{len(KNOWN_FULL)}）；"
                   "确认是有意变动后加 --accept-secret-change 重跑")
        if why:
            log(f"❌ 黑名单加载异常，本次不写抽取件：{why}")
            if lockf:
                lockf.close()
            return 4
        state["secret_baseline"] = {"files": nf, "values": len(KNOWN_FULL)}
        if not dry_run:
            tmp = side.with_name(f"_secret_baseline.json.{os.getpid()}.tmp")
            tmp.write_text(json.dumps(state["secret_baseline"]), encoding="utf-8")
            os.replace(tmp, side)
    srcs = state.setdefault("sources", {})
    used_out = {v.get("out"): k for k, v in srcs.items()}
    st_ = Counter()
    red = Counter()
    t0 = time.time()
    seen = set()
    for label, root in live:
        for p, rel in iter_source_files(label, root):
            key = f"{label}:{rel}"
            seen.add(key)
            st_["files"] += 1
            try:
                stt = p.stat()
                prev = srcs.get(key)
                if prev and prev.get("size") == stt.st_size and prev.get("mtime") == stt.st_mtime \
                        and (dst / prev.get("out", "")).exists():
                    st_["skipped"] += 1
                    continue
                header, records, bad = extract_session(p, red)
            except Exception as e:
                st_["failed"] += 1
                log(f"⚠ 读取失败，跳过（下次重试）：{key} · {e.__class__.__name__}: {e}")
                continue
            st_["bad_lines"] += bad
            out = prev["out"] if prev and prev.get("out") else out_relpath(label, rel, header["first_ts"], stt.st_mtime)
            if not prev and out in used_out and used_out[out] != key:
                out = out.replace(".jsonl.gz", f"_{hashlib.sha1(key.encode()).hexdigest()[:16]}.jsonl.gz")
            header.update({"source": label, "session_id": p.stem, "source_rel": rel,
                           "project_dir": rel.split("/")[0], "source_size": stt.st_size,
                           "extracted_at": time.strftime("%Y-%m-%dT%H:%M:%S%z")})
            st_["updated" if prev else "new"] += 1
            st_["records"] += len(records)
            if dry_run:
                continue
            target = dst / out
            if target.exists() and (prev and stt.st_size < prev.get("size", 0) or not _is_superset(target, records)):
                keep = target.with_name(target.name.replace(".jsonl.gz", f".superseded-{time.strftime('%Y%m%d%H%M%S')}.jsonl.gz"))
                os.replace(target, keep)
                st_["superseded"] += 1
                log(f"⚠ 源被改写（新内容不再覆盖旧抽取件），旧件保留为 {keep.name}")
            write_atomic_gz(target, [header] + records)
            srcs[key] = {"size": stt.st_size, "mtime": stt.st_mtime, "out": out}
            used_out[out] = key
            if (st_["new"] + st_["updated"]) % SAVE_EVERY == 0:
                save_state(dst, state)
    gone = [k for k in srcs if k not in seen and any(k.startswith(l + ":") for l, _ in live)]
    if not dry_run:
        state["version"] = 2
        state["last_run"] = time.strftime("%Y-%m-%dT%H:%M:%S%z")
        save_state(dst, state)
        lockf.close()
    log(f"源文件 {st_['files']} · 新抽 {st_['new']} · 更新 {st_['updated']} · 跳过 {st_['skipped']} · "
        f"失败 {st_['failed']} · 记录 {st_['records']} · 坏行 {st_['bad_lines']} · 改写保全 {st_['superseded']} · "
        f"源已被清理但抽取件保留 {len(gone)} · 脱敏命中（截断前） {sum(red.values())} {dict(red)} · "
        f"用时 {time.time() - t0:.1f}s" + (" · dry-run 未写" if dry_run else ""))
    return 1 if st_["failed"] else 0


def parse_sources(items):
    out = []
    for s in items:
        if "=" not in s:
            raise SystemExit(f"--source 需写成 标签=路径：{s}")
        lbl, path = s.split("=", 1)
        if not re.fullmatch(r"[A-Za-z0-9_\-]+", lbl):
            raise SystemExit(f"来源标签只允许字母数字、下划线、连字符：{lbl}")
        out.append((lbl, Path(os.path.expanduser(path))))
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description="真相层（原始会话）抽取器（C 档 · v7）")
    ap.add_argument("--source", action="append", default=[], help="标签=路径，可重复；不给用默认三处")
    ap.add_argument("--dst", default=os.environ.get("TRANSCRIPT_DST", str(DEFAULT_DST)))
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--accept-secret-change", action="store_true", help="凭证文件或值比上次少是有意变动时用，更新基线")
    ap.add_argument("--secret-sources", default=str(Path(__file__).resolve().parent / "transcript_secret_sources.txt"),
                    help="已知凭证来源清单（glob），设为空字符串则不用黑名单")
    a = ap.parse_args(argv)
    sources = parse_sources(a.source) if a.source else DEFAULT_SOURCES
    return run(sources, a.dst, a.dry_run, secret_sources=a.secret_sources or None,
               accept_secret_change=a.accept_secret_change)


if __name__ == "__main__":
    sys.exit(main())
