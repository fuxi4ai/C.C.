#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""经验索引生成器 v2——从 GOTCHAS/通用教训/经验库 扫描生成薄索引（非事实源 · 可重建 · 幂等）。
v2（2026-09-03 独立审查修复）：①覆盖 4 种条目格式（H2/H3/列表粗体/表格）；②纳入经验库 EXP 条目；③字段扩至 9 项。
用法:
  python3 build_experience_index.py          # Mac 终端（DOCS_DIR 默认 ~/Documents）
  DOCS_DIR=/sessions/xxx/mnt/Documents python3 build_experience_index.py   # 沙箱
产物: brain/permanent/经验索引.md + brain/permanent/_exchange_index.md
原则: 索引只含指针与状态摘要，正文真源=各项目 GOTCHAS.md / 通用教训.md / 经验库.md；索引可随时重建。
"""
import os, re, hashlib, datetime, json

DOCS = os.environ.get("DOCS_DIR") or os.path.expanduser("~/Documents")
BRAIN = os.path.join(DOCS, "Claude/brain")
PERM = os.path.join(BRAIN, "permanent")
OUT = os.path.join(PERM, "经验索引.md")
EXCH = os.path.join(PERM, "_exchange_index.md")

MACHINE_GATES = [
    "Database/行业研究/rules/kg_promote.py",
    "Database/行业研究/rules/check_desc_shrink.py",
    "Database/行业研究/rules/bare_alias_check.py",
    "Database/行业研究/rules/check_id_consistency.py",
    "Database/行业研究/rules/name_code_consistency_check.py",
    "Database/行业研究/consumers/龙鱼五力/check_ds_evidence.py",
    "Database/行业研究/consumers/龙鱼五力/test_check_ds_evidence.py",
]

TYPE_MAP = [("ERR", "故障"), ("BUG", "缺陷"), ("RISK", "风险"), ("INFRA", "设施"),
            ("FIX", "修复"), ("NOTE", "观察"), ("NAMING", "命名"), ("GOTCHA", "坑"),
            ("EXP", "经验"), ("G-", "教训"), ("G-X", "教训")]

def sha256(p):
    try:
        return hashlib.sha256(open(p, "rb").read()).hexdigest()[:16]
    except Exception:
        return "MISSING"

def status_of(body, title=""):
    """状态行 → 标题内嵌（白泽等格式·🔄 在 ✅ 前按出现序） → 正文头部窗口。"""
    m = re.search(r"\*\*状态[:：]?\*\*\s*[:：]?\s*([^\n*]+)", body)  # 2026-11-05：兼容 `**状态：**`（DVA 6 条曾落 —）
    if m:
        s = m.group(1)
    elif title:
        s = title
    else:
        s = body[:600]
    for mark in ("🔄", "⚠", "✅", "⏳"):
        if mark in s:
            return mark
    return "—"

# Projects/ 来源专用（brain 来源仍走 status_of，旧条目判定不变）。
# 同一行既有开放词又有闭合词时判开放：宁可多报，不低报（海螺 GOTCHA-20260819-001 同类教训）。
OPEN_TOKENS = (("🔄", "🔄"), ("⚠", "⚠"), ("⏳", "⏳"), ("已知风险", "⚠"), ("已修待验", "🔄"), ("待修复", "🔄"),
               ("未修复", "🔄"), ("待执行", "🔄"), ("待核", "🔄"), ("待裁", "🔄"), ("待老师", "🔄"), ("待验", "🔄"))
CLOSED_TOKENS = ("✅", "已解决", "已修复", "已修", "已裁", "已定性", "已登记", "已验证", "已复核", "并修复")

def project_status(body, title=""):
    """覆盖 `**状态**:`、`**状态：**`、`| **状态** | x |`、`状态: x`、`- 状态：x`；无状态行则看标题。"""
    m = re.search(r"^\s*(?:[-*|]\s*)*(?:\*\*)?状态(?:\*\*)?\s*[:：|]?\s*(?:\*\*)?\s*[:：|]?\s*(.+)$", body, re.M)
    s = m.group(1) if m else title
    for token, mark in OPEN_TOKENS:
        if token in s:
            return mark
    return "✅" if any(token in s for token in CLOSED_TOKENS) else "—"

def type_of(eid):
    for pre, t in TYPE_MAP:
        if eid.startswith(pre):
            return t
    return "其他"

def date_of(eid):
    m = re.search(r"(20\d{2})[.-]?(\d{2})[.-]?(\d{2})", eid)
    return m.group(1) + "-" + m.group(2) + "-" + m.group(3) if m else "—"

def machine_hint(body):
    return bool(re.search(r"(check_desc_shrink|bare_alias_check|kg_promote|kg_merge_safe|check_ds_evidence|第1[0-9]项|负向测试|断言|校验脚本|门禁|守卫|guard)", body))

entries = []

SEEN_IDS = {}
SOURCE_WARNINGS = []
def add(proj, eid, title, body, fname, status=None):
    if "YYYYMMDD" in eid or "NNN" in eid:
        return
    # 2026-11-05 审计：同来源同 ID 不再双计（PEC 表格+列表双写 14 条、通用教训「G-X2 补」追记、烛照撞号曾被静默双计）；标题不同才告警
    key = (proj, eid)
    if key in SEEN_IDS:
        if SEEN_IDS[key] != title:
            SOURCE_WARNINGS.append(f"编号重复（保留先出现者）：{proj}/{eid} @ {fname}")
        return
    SEEN_IDS[key] = title
    entries.append({
        "proj": proj, "id": eid, "title": title.replace("|", "｜")[:64],
        "type": type_of(eid), "date": date_of(eid), "status": status or status_of(body, title),
        "mach": "✓" if machine_hint(body) else "-",
        "ptr": fname, "xside": "-", "body": body,
        "trig": trigger_of(body),
    })

TRIG_PRI = ["警报信号", "判据", "做法", "强制询问", "强制问询", "避坑", "预防门禁", "触发条件", "修法", "处置"]

def trigger_of(body):
    """**触发条件**（2026-09-29 加 · 承 Doctor 批）：从条目**自带的、被加粗的字段名行**里抽**一行**——
    **不改任何正文，只改「索引抽什么」**。
    为什么需要：原索引只抽标题，而「万能概念陷阱」这类标题**判不出「此刻该不该把它调出来」**。
    收严口径（首版放到「任意含关键词的行」，实测抽到的是标题装饰 `（★★★ 关键 · …）` ⇒ 已收紧）：
      ① 只认**被 `**…**` 包住的字段名行**（或紧邻其下的正文行）；
      ② 值须 ≥6 字且**不以括号开头**（滤掉 `（★★★ 关键 · 2026-05-20 立）` 这类装饰）；
      ③ 按 `TRIG_PRI` **优先级**取第一个命中（判据／做法 先于 修法／处置）；
      ④ 抽不到 ⇒ `—`（如实标，不编）。
    ⚠ 已知缺：**老格式条目**（标题写作 `**G-Xn 标题**（★★★…）`、下设无加粗字段名）抽不到 ⇒ `—`。"""
    lines = (body or "").splitlines()
    for name in TRIG_PRI:
        pat = re.compile(rf"^\s*(?:>\s*)?(?:[-*]\s*)?\*\*\s*{re.escape(name)}[^*]*\*\*\s*[:：]?\s*(.*)$")
        for i, l in enumerate(lines):
            m = pat.match(l)
            if not m:
                continue
            seg = m.group(1).strip()
            if not seg:
                for nxt in lines[i + 1:i + 4]:
                    if nxt.strip():
                        seg = nxt.strip()
                        break
            seg = re.sub(r"^[-*>\s]+", "", seg)
            seg = re.sub(r"\*\*|`", "", seg).strip()
            if len(seg) >= 6 and not seg.startswith(("（", "(")):
                return f"[{name}] {seg[:54]}"
    return "—"


def seg_until(txt, start, marker):
    body = txt[start:]
    nxt = re.search(marker, body, re.M)
    return body[:nxt.start()] if nxt else body

# 1) 各项目 GOTCHAS：H2 格式（渊图/烛照九阴/龙鱼五力/风险日报等）
for d in sorted(os.listdir(BRAIN)):
    p = os.path.join(BRAIN, d, "GOTCHAS.md")
    if not os.path.isfile(p):
        continue
    txt = open(p, encoding="utf-8").read()
    for m in re.finditer(r"^## \[([^\]]+)\]\s*(.*)$", txt, re.M):
        add(d, m.group(1), m.group(2).strip(), seg_until(txt, m.end(), r"^## \["), f"{d}/GOTCHAS.md")
    # H3 格式（剑酒青丘）
    for m in re.finditer(r"^### \[([^\]]+)\]\s*(.*)$", txt, re.M):
        add(d, m.group(1), m.group(2).strip(), seg_until(txt, m.end(), r"^### \[|^## \[|^## "), f"{d}/GOTCHAS.md")
    # 列表粗体格式（白泽大宗 G-01 等）
    for m in re.finditer(r"^- \*\*(G-\d+)\s+(.*?)\*\*", txt, re.M):
        add(d, m.group(1), m.group(2).strip(), seg_until(txt, m.end(), r"^- \*\*G-\d+|^## |^# "), f"{d}/GOTCHAS.md")
    # 表格索引格式（PEC G-01~G-14 全表索引行）
    for m in re.finditer(r"^\|\s*(G-\d+)\s*\|\s*([^|]+)\|\s*([^|]+)\|", txt, re.M):
        add(d, m.group(1), m.group(2).strip(), "", f"{d}/GOTCHAS.md 全表索引（正文在 Projects/PEC/GOTCHAS.md）")

# 1b) canonical 落在 Projects/ 的 GOTCHAS（2026-11-04 Doctor 批「修生成器」· ERR-20261104-004）
#     显式白名单，不递归扫：DVA 为历史副本（权威在 Codex 镜像仓）、烛照九阴为退役指针，都不进来。
#     条目格式：`[ID]` 标题、`GOTCHA-NNN:`／`G-NNN —` 标题、`- **EAL-M001 · …**` 列表。
#     `### [ ] 待办勾选` 不算条目；带状态行却解析不了的标题会写进索引头，不静默跳过。
PROJECT_SOURCES = [
    ("白泽大宗", "Projects/Financial/白泽大宗/GOTCHAS.md"),
    ("白泽观星", "Projects/Financial/白泽观星/GOTCHAS.md"),
    ("风险日报", "Projects/风险日报/GOTCHAS.md"),
    ("星空", "Projects/星空/GOTCHAS.md"),
    ("海螺姑娘", "Projects/海螺姑娘/GOTCHAS.md"),
    ("EAL", "Projects/Financial/宏观研究体系/EAL/GOTCHAS.md"),
]
NOT_COVERED = ("Projects/DVA（含 yt-dlp；历史副本，真源在 Codex 镜像仓）、Projects/Financial/烛照九阴（退役指针，含 news）、"
               "Projects/PEC（brain 已有全表索引）、Projects/O MY HTML 与 Projects/Financial/剑酒青丘/*（无编号格式）、"
               "EAL/backtest/eal_v3（只读保留件）")
PROJECT_ENTRY_RES = [
    re.compile(r"^#{2,3} \[([A-Z][A-Z0-9]*(?:-[A-Za-z0-9]+)+)\]\s*(.*)$", re.M),
    re.compile(r"^#{2,3} ((?:GOTCHA|G)-\d+)\s*[:：·—-]+\s*(.*)$", re.M),
    re.compile(r"^- \*\*([A-Z]+-[A-Z]*\d+)\s*·\s*(.*?)\*\*", re.M),
]
SOURCE_WARNINGS = []
for proj, rel in PROJECT_SOURCES:
    p = os.path.join(DOCS, "Claude", rel)
    if not os.path.isfile(p):
        SOURCE_WARNINGS.append(f"来源缺失：{rel}")
        continue
    txt = re.sub(r"<!--.*?-->", "", open(p, encoding="utf-8").read(), flags=re.S)
    ptr = "../" + rel  # 证据指针统一相对 brain/
    matches = sorted((m for r in PROJECT_ENTRY_RES for m in r.finditer(txt)), key=lambda m: m.start())
    matches = [m for m in matches if "YYYYMMDD" not in m.group(1) and "NNN" not in m.group(1)]
    starts = {m.start() for m in matches}
    seen = {e["id"] for e in entries if e["proj"] == proj}
    for i, m in enumerate(matches):
        if m.group(1) in seen:
            SOURCE_WARNINGS.append(f"编号重复（保留先出现者）：{proj}/{m.group(1)} @ {rel}")
            continue
        seen.add(m.group(1))
        end = matches[i + 1].start() if i + 1 < len(matches) else len(txt)
        body = txt[m.end():end]
        sect = re.search(r"^## ", body, re.M)
        body = body[:sect.start()] if sect else body
        title = m.group(2).strip()
        add(proj, m.group(1), title, body, ptr, status=project_status(body, title))
    if not matches:
        SOURCE_WARNINGS.append(f"来源解析为 0 条：{rel}")
    # 带状态行却没被解析成条目的标题
    heads = list(re.finditer(r"^#{2,3} (.*)$", txt, re.M))
    missed = [h.group(1)[:30] for j, h in enumerate(heads) if h.start() not in starts
              and re.search(r"^\s*(?:[-*]\s*|\|\s*\*\*)*(?:\*\*)?状态", txt[h.end():heads[j + 1].start() if j + 1 < len(heads) else len(txt)], re.M)]
    if missed:
        SOURCE_WARNINGS.append(f"未解析标题 {len(missed)} 个（带状态行，未进索引）：{rel}：" + "；".join(missed))

# 2) 通用教训（粗体 G-X 行）
gl = os.path.join(PERM, "通用教训.md")
if os.path.isfile(gl):
    gl_txt = open(gl, encoding="utf-8").read()
    for m in re.finditer(r"^\*\*(G-X\d+)\s+(.*?)\*\*", gl_txt, re.M):
        add("通用教训", m.group(1), m.group(2).strip(), gl_txt[m.end():m.end()+1500], "permanent/通用教训.md")
    for m in re.finditer(r"^## \[(G-X\d+)\]\s*(.*)$", gl_txt, re.M):
        add("通用教训", m.group(1), m.group(2).strip(), seg_until(gl_txt, m.end(), r"^## \[|^## "), "permanent/通用教训.md")

# 3) 经验库 EXP（H3 · cases/patterns 分节）
exp = os.path.join(PERM, "经验库.md")
if os.path.isfile(exp):
    exp_txt = open(exp, encoding="utf-8").read()
    cur_sect = "经验库"
    for m in re.finditer(r"^## (cases|patterns)[^\n]*|^### \[(EXP-[^\]]+)\]\s*(.*)$", exp_txt, re.M):
        if m.group(1):
            cur_sect = m.group(1)
        else:
            add(f"经验库·{cur_sect}", m.group(2), m.group(3).strip(),
                seg_until(exp_txt, m.end(), r"^### \[|^## "), "permanent/经验库.md")

by_proj = {}
for e in entries:
    by_proj.setdefault(e["proj"], []).append(e)

# 对侧状态 sidecar（手写回填不被重建冲掉 · 2026-09-03 立）：permanent/_exchange_status.jsonl
# 行 schema: {"proj": "...", "id": "...", "xside": "⚑已预警|✓已复验", "ts": "...", "evidence": "..."}
XSIDE = {}
xpath = os.path.join(PERM, "_exchange_status.jsonl")
if os.path.isfile(xpath):
    for line in open(xpath, encoding="utf-8"):
        line = line.strip()
        if not line:
            continue
        try:
            d = json.loads(line)
            XSIDE[(d["proj"], d["id"])] = d
        except Exception:
            pass
for e in entries:
    d = XSIDE.get((e["proj"], e["id"]))
    if d:
        e["xside"] = f"{d['xside']}@{d['ts'][:10]}"

now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
lines = [
    "# 经验索引（薄索引 · 非事实源 · 可重建 · v2）",
    "",
    f"> 生成：{now} · 生成器 brain/.tools/build_experience_index.py（v2）· 重跑幂等",
    "> 字段 10 项（**2026-09-29 加第 10 项「触发条件」** · 承 Doctor 批）：条目ID · 类型 · 日期 · 状态 · 机器化 · 标题 · 证据指针 · 来源主体（节头） · 对侧状态（- 未见 / 👁已扫描未命中 / ⚑已预警 / ✓已复验）。",
    "> 状态闭集：✅已修复/已沉淀 · 🔄待修复/已修待验 · ⚠已知风险 · ⏳旧状态词 · —未标。**触发条件＝从条目自带的「警报信号／判据／做法／强制问询／预防门禁」抽一行**（2026-09-29 起；原为「＝标题摘要」，已取代）；正文按指针取。",
    "> 覆盖：brain 各项目 GOTCHAS（H2/H3/列表粗体/表格四格式）+ Projects/ 下白名单 GOTCHAS（" + "、".join(n for n, _ in PROJECT_SOURCES) + "）+ 通用教训 + 经验库 EXP。Projects 来源的证据指针相对 brain/。",
    "> 未纳入：" + NOT_COVERED + "。**「开放 0」只表示已入索引的条目中无开放项；「未标」＝条目无可判定状态，不等于已闭。**",
    *[f"> ⚠ {w}" for w in SOURCE_WARNINGS],
    "",
    f"## 总览（{len(entries)} 条 · {len(by_proj)} 个来源）",
    "",
]
for proj in sorted(by_proj):
    es = by_proj[proj]
    n_open = sum(1 for e in es if e["status"] in ("🔄", "⚠", "⏳"))
    n_unmarked = sum(1 for e in es if e["status"] == "—")
    lines.append(f"- {proj}: {len(es)} 条（开放 {n_open} · 未标 {n_unmarked}）")
for proj in sorted(by_proj):
    lines.append(f"\n## {proj}")
    for e in by_proj[proj]:
        lines.append(f"- `{e['id']}` · {e['type']} · {e['date']} · {e['status']} · 闸{e['mach']} · {e['title'][:56]} · **触发**：{e['trig']} · → {e['ptr']} · 对侧{e['xside']}")
open(OUT, "w", encoding="utf-8").write("\n".join(lines) + "\n")

GATES_META = {
    "Database/行业研究/rules/kg_promote.py": {
        "replay": "python3 rules/kg_promote.py <candidate> <base>（参数以 --help 为准）",
        "expect": "一键门全过：丢失 0/第 12 项 0%/双空 0/边 schema PASS/三元组 0",
        "last_run": "2026-09-01 渊图入库场（日志实据·全绿）", "note": "用法未在本场实跑·复验方首跑时核 --help"},
    "Database/行业研究/rules/check_desc_shrink.py": {
        "replay": "python3 rules/check_desc_shrink.py <base> <candidate>（参数以 --help 为准）",
        "expect": "exit 0 = 无 desc 缩减；对未修 _v2 报出 15 处、对 canonical 报 0",
        "last_run": "2026-09-01 渊图 QA 场（日志实据）", "note": "用法未在本场实跑"},
    "Database/行业研究/rules/bare_alias_check.py": {
        "replay": "python3 rules/bare_alias_check.py（参数以 --help 为准）",
        "expect": "大小写重复/裸简称/近名兄弟簇清单；无新增违例",
        "last_run": "2026-08 渊图入库 QA（日志实据）", "note": "用法未在本场实跑"},
    "Database/行业研究/rules/check_id_consistency.py": {
        "replay": "python3 rules/check_id_consistency.py（参数以 --help 为准）",
        "expect": "id 一致性 exit 0（187 条年份警告系存量噪音）",
        "last_run": "2026-08-25 渊图批（日志实据）", "note": "用法未在本场实跑"},
    "Database/行业研究/rules/name_code_consistency_check.py": {
        "replay": "python3 rules/name_code_consistency_check.py（参数以 --help 为准）",
        "expect": "name↔code 无告警",
        "last_run": "2026-09-01 渊图批（日志实据）", "note": "用法未在本场实跑"},
    "Database/行业研究/consumers/龙鱼五力/check_ds_evidence.py": {
        "replay": "python3 check_ds_evidence.py --date 2026-08-29",
        "expect": "有 ⚠ 即 exit 1（设计）；输出三档计数+锚出处",
        "last_run": "2026-09-03 本场实跑（109 只 · ⚠69）"},
    "Database/行业研究/consumers/龙鱼五力/test_check_ds_evidence.py": {
        "replay": "python3 test_check_ds_evidence.py",
        "expect": "5/5 PASS · exit 0",
        "last_run": "2026-09-03 本场 subagent 独立验收实跑（5/5 PASS）"},
}

ex = [
    "# CC 侧经验对侧索引（薄 · 供 VV 只读 · 可重建 · 非事实源）",
    "",
    f"> 生成：{now} · 生成器 brain/.tools/build_experience_index.py（v2）",
    "> 正文真源在 CC 侧 canonical（brain/ 各项目 GOTCHAS.md + Projects/ 下白名单 GOTCHAS + permanent/通用教训.md + permanent/经验库.md），本文件只含定位指针，供跨系统预警与复验。",
    "",
    f"## 摘要（{len(entries)} 条）",
    "结构与 permanent/经验索引.md 相同（对侧对 brain 只读可直取）。",
    "",
    "## 机器闸清单（六字段：路径/SHA/可见性/重放命令/预期通过/最近运行）",
    "",
    "> 可见性统一为「Doctor 侧路径 · VV 可见范围外」——复验需经 Doctor 转达或受控镜像（正文不复制，保持 canonical 唯一）。",
    "",
]
for g in GATES_META:
    m = GATES_META[g]
    ex.append(f"- {g}")
    ex.append(f"  - sha256[:16]={sha256(os.path.join(DOCS, g))}")
    ex.append(f"  - 可见性: Doctor 侧路径 · VV 可见范围外")
    ex.append(f"  - 重放: {m['replay']}")
    ex.append(f"  - 预期通过: {m['expect']}")
    ex.append(f"  - 最近运行: {m['last_run']}" + (f" · ⚠{m['note']}" if m.get("note") else ""))
ex += [
    "",
    "## 对侧状态约定",
    "- 未见（默认 -） / 👁已扫描未命中 / ⚑已预警 / ✓已复验（复验=实读或实跑该条目内容本身，扫描索引不算复验）",
    "- 复验须带：命令 + 关键输出摘录 + 复验日期，回填至本地索引对应条目行（对侧列）。",
    "",
    "## 对侧消费记录（sidecar permanent/_exchange_status.jsonl · 手写不被重建冲掉）",
    "",
]
for line in open(xpath, encoding="utf-8") if os.path.isfile(xpath) else []:
    line = line.strip()
    if not line:
        continue
    try:
        d = json.loads(line)
        ex.append(f"- {d['ts']} · {d['proj']}/{d['id']} · {d['xside']} · {d['evidence']}")
    except Exception:
        pass
open(EXCH, "w", encoding="utf-8").write("\n".join(ex) + "\n")

print(f"本地索引：{OUT}（{len(entries)} 条）")
print(f"对侧索引：{EXCH}")
