#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
make_commit_block.py —— 把「探针输出 → 提交命令块」这一步**脚本化**。

为什么存在
==========
`G-X83`（给 git 提交命令前先探工作树·禁默认 `git add -A`）自 2026-07-23 首例起已复发 **5 次**，
原因跨 5 种：未探工作树（07-23）／状态闸顺序写反 + 范围不明（09-22）／探针用 mtime 不可靠（09-23）／
自行实现 `.gitignore` 语义（09-23）／**探针正确但命令块退回默认 `-A`**（09-27）。

共同点不是「不知道规矩」——规矩 5 次都在盘上——而是**知识没落成机械动作**。
⇒ 本工具强制「探针结论 → scoped add 清单」这一转换经它落地，而不是靠实施者记得手改。

设计边界（照录 canonical，**不得放宽**）
====================================
① **只读**：本工具**不跑任何 git 子命令**（沙箱禁 git 是硬约束 G-X2），只解析 `.git/` 纯文本；
   生成命令块交 Doctor 终端执行。
② **只认内容级比对**：`.git/index` 每条目 blob SHA vs 现算 `sha1("blob <len>\\0" + 内容)`。
   mtime 只可当「最近动过」的粗提示，**不得作干净判据**（G-X83 2026-09-23）。
③ **符号链接一律 `readlink()` 比字符串、禁跟进目标内容**（同坑 3 次：09-12 / 09-23 / 09-27）。
④ **绝不自行实现 `.gitignore` 语义**：未跟踪件一律标「候选（未过 ignore 判）」，
   并**在块内**给出 `git check-ignore -v` 让 git 自己判（G-X83 2026-09-23）。
⑤ 生成的块**永不包含 `git add -A` / `--all`**；`--selftest` 会断死这一点（负向守卫）。
⑥ 块内 `git status --short` 必须排在 `git add` **之前**（给人留闸 · 加固①）。
⑦ 块**幂等**：重跑结果相同（提交前置 `git diff --cached --quiet` 闸；不用 append 类写入 · G-X120）。
⑧ **块内不用 `cd`，一律 `git -C <仓>`**（2026-09-27 新增）。原因见下。

⑧ 为什么禁 `cd`（2026-09-27 实测事故形态 · G-X134 同族）
-------------------------------------------------------
首版块内写 `cd '~/Documents/Claude/brain'`——**单引号会吞掉波浪号展开**，
`cd` 当场失败，而块内没有 `set -e` ⇒ **后续命令全部在「当前所在的那个仓」里继续跑**。
本次幸而落空（那两个路径在错仓里不存在，`git add` 报 `fatal: pathspec`，
最后幂等闸打印的又是「无暂存变化，跳过提交」——**看起来像成功**）。
但若错仓里恰好有同名路径，就会**把文件加进错误的仓并提交**。

⇒ 三重加固：**(a)** 不用 `cd`，每条命令自带 `git -C <仓>`（无 shell 状态，错路径就地报错）；
**(b)** 路径渲染成 `"$HOME/..."`（**双**引号，`$HOME` 可展开，空格也安全）；
**(c)** 整段包在 `[ -d "$_repo/.git" ]` 守卫里 —— 仓不存在就只打印 ❌ 并**跳过全部命令**。
注意**不能**用 `set -e` / `exit`：Doctor 是**交互式 shell**，那会把他的终端关掉。

用法
====
    python3 make_commit_block.py <repo> [<repo2> ...] [--msg "提交信息"] [--max-untracked 30]
    python3 make_commit_block.py <repo> --include 新文件.py --include 另一个.py   # 人工核过的未跟踪件
    python3 make_commit_block.py --selftest          # 输出不变量自检（含负向），任何一项不过 exit 1

注意：`--msg` 只填一次、复用到所有仓；跨仓批量时**逐仓分开写块**（加固③），本工具已按此输出。
未跟踪件**默认一律不入册**，只列「候选」；要入册必须用 `--include` 逐条显式列出。
"""
from __future__ import annotations

import argparse
import hashlib
import os
import pathlib
import re
import shlex
import struct
import sys

# 生成块内被禁止出现的 add 形态（G-X83⑤）。--selftest 负向守住。
BANNED_ADD = ("git add -A", "git add --all", "git add -u", "git add .")


# ─────────────────────────── 探针层（只读 · 无 git） ───────────────────────────

def read_index(repo: pathlib.Path):
    """解析 `.git/index` → [(path, blob_sha)]。

    步长配方是踩过坑的：**相对步长** `((base+namelen+1+7)//8)*8`
    （补零含 NUL 终止字节；写成「绝对偏移向 8 取整」或「带外层 %8」都会整段错位），
    且 **base 随扩展标志位 0x4000 由 62 切 64**。
    """
    p = repo / ".git" / "index"
    d = p.read_bytes()
    if d[:4] != b"DIRC":
        raise ValueError(f"不是 git index：{p}")
    _ver, n = struct.unpack(">II", d[4:12])
    off, out = 12, []
    for _ in range(n):
        ext = struct.unpack(">H", d[off + 60:off + 62])[0] & 0x4000
        base = 64 if ext else 62
        namelen = struct.unpack(">H", d[off + base - 2:off + base])[0]
        sha = d[off + 40:off + 60].hex()
        name = d[off + base:off + base + namelen].decode("utf-8", "surrogateescape")
        out.append((name, sha))
        off += ((base + namelen + 1 + 7) // 8) * 8
    return out


def head_sha(repo: pathlib.Path):
    """只读解析 HEAD → sha（不跑 git）。解析不出（packed 异常等）返回 None。"""
    try:
        h = (repo / ".git" / "HEAD").read_text().strip()
        if h.startswith("ref:"):
            ref = h[5:].strip()
            f = repo / ".git" / ref
            if f.is_file():
                return f.read_text().strip()
            pf = repo / ".git" / "packed-refs"
            if pf.is_file():
                for line in pf.read_text().splitlines():
                    if line.startswith("#") or not line.strip():
                        continue
                    parts = line.split()
                    if len(parts) == 2 and parts[1] == ref:
                        return parts[0]
            return None
        return h or None
    except Exception:  # noqa: BLE001
        return None


def _blob_sha(b: bytes) -> str:
    return hashlib.sha1(b"blob %d\0" % len(b) + b).hexdigest()


def worktree_state(repo: pathlib.Path):
    """→ (index, M, D, untracked_candidates)。全部内容级；符号链接不跟进。"""
    idx = read_index(repo)
    M, D = [], []
    for name, sha in idx:
        f = repo / name
        if f.is_symlink():
            cur = _blob_sha(os.readlink(f).encode("utf-8", "surrogateescape"))
        elif f.is_file():
            cur = _blob_sha(f.read_bytes())
        else:
            D.append(name)
            continue
        if cur != sha:
            M.append(name)
    tracked = {n for n, _ in idx}
    disk = set()
    for p in repo.rglob("*"):
        rel = p.relative_to(repo)
        if ".git" in rel.parts:
            continue
        if p.is_symlink() or p.is_file():
            disk.add(rel.as_posix())
    return idx, sorted(M), sorted(D), sorted(disk - tracked)


# ─────────────────────────── 渲染层（纯函数 · 可单测） ───────────────────────────

_SANDBOX_MNT = re.compile(r"^/sessions/[^/]+/mnt/(.*)$")


def _disp(p: pathlib.Path) -> str:
    """把路径显示成 Doctor 终端**原样可跑**的形态（G-X134：贴块前自问「粘进去能不能跑」）。

    ⚠ 挂载盘在沙箱里是 `/sessions/<vm>/mnt/Documents/...`，而 Doctor 终端看到的是 `~/Documents/...`。
    直接对 `$HOME` 做字符串替换会产出 `~/mnt/Documents/...` —— **跑不了**。
    2026-09-27 首版实跑就踩了这处（属 G-X134 同族）。
    """
    s = str(p)
    m = _SANDBOX_MNT.match(s)
    if m:
        return "~/" + m.group(1)
    h = str(pathlib.Path.home())
    if s == h:
        return "~"
    if s.startswith(h + "/"):
        return "~/" + s[len(h) + 1:]
    return s


def _sh_repo(path_disp: str) -> str:
    """仓路径 → shell 里**可展开**的形态。

    `shlex.quote("~/x")` 会给出 `'~/x'`——**单引号吞掉波浪号展开**，`cd`/`-C` 当场失败。
    故 `~/` 前缀一律渲染成 `"$HOME/…"`（双引号：`$HOME` 可展开、空格也安全）。
    """
    if path_disp.startswith("~/"):
        rest = path_disp[2:]
        if not any(ch in rest for ch in '"\\$`'):
            return '"$HOME/' + rest + '"'
    return shlex.quote(path_disp)


def render_block(repo: pathlib.Path, M, D, U, msg: str,
                 max_untracked: int = 30, include=None, head: str | None = None) -> str:
    """把探针结论渲染成一个提交命令块。纯字符串拼接，无副作用。

    `include` = 人工**显式核过**的未跟踪件（相对仓路径），才会进 scoped add；
    其余未跟踪件一律只作「候选」列出、不自动入册（G-X83 2026-09-23）。
    """
    q = shlex.quote
    inc = list(include or [])
    path_disp = _disp(repo)
    repo_sh = _sh_repo(path_disp)
    G = f"git -C {repo_sh}"
    targets = list(M) + list(D)

    L = []
    L.append(f"# ══ {path_disp} ══  M={len(M)} · D={len(D)} · 未跟踪候选={len(U)} · include={len(inc)}")
    L.append(f"_repo={repo_sh}")
    L.append('# 守卫（2026-09-27 加）：仓不存在 → 只打印并**跳过全部命令**，绝不在别的目录里跑 git。')
    L.append('# 刻意不用 set -e / exit —— Doctor 是交互式 shell，那会把终端关掉。')
    L.append('if [ ! -d "$_repo/.git" ]; then')
    L.append('  echo "❌ 仓不存在或不是 git 仓：$_repo"')
    L.append('  echo "   —— 本块其余命令已跳过（不会在任何其它目录执行 git）"')
    L.append('else')

    body = []

    def add(s=""):
        body.append(s)

    add("# ── 闸：先看工作树，别先 add（G-X83 加固①）──")
    add(f'{G} status --short')
    if head:
        add(f'# 探针时的 HEAD = {head[:8]}；下列比对只报警不中止（HEAD 变了不代表 add 清单失效）')
        add(f'[ "$({G} rev-parse HEAD)" = "{head}" ] || echo "⚠ HEAD 已变（探针时 {head[:8]}）——清单可能过期，建议重生成"')
    add("")

    if U:
        add("# ── 未跟踪候选（**未过 ignore 判**）· 按 G-X83 2026-09-23：绝不自行实现 ignore 语义 ──")
        add("# 先让 git 自己判；被 ignore 者会自动排除在下面的 add 之外。")
        shown = U[:max_untracked]
        for cs in range(0, len(shown), 8):
            chunk = shown[cs:cs + 8]
            add(f'{G} check-ignore -v -- ' + " ".join(q(x) for x in chunk) + " || true")
        if len(U) > len(shown):
            add(f"# …另有 {len(U) - len(shown)} 件未列出（--max-untracked 上调可看全）")
        add("# ⚠ 只把**你确认属于本次范围**的候选补进下面的 add；其余保持未跟踪。")
        add("")

    if targets or inc:
        add("# ── scoped add：只加本次范围 —— M/D 来自内容级探针 · include 来自人工显式核过的未跟踪件 ──")
        for i in range(0, len(targets), 6):
            add(f'{G} add -- ' + " ".join(q(x) for x in targets[i:i + 6]))
        for x in inc:
            add(f'{G} add -- ' + q(x))
    else:
        add("# ── 无 M/D 且无 --include：本次没有已跟踪文件的内容变化 ──")
        add("#    若要走未跟踪件，用 `--include <路径>` 显式列出（**不要**改成整批 add）")
    add("")

    add("# ── 复核：暂存范围 / 空白与冲突标记 ──")
    add(f'{G} status --short')
    add(f'{G} diff --cached --stat')
    add(f'{G} diff --cached --check')
    add("")

    add(f"# ── 提交信息须覆盖暂存清单的**全部文件族**（加固②）：本条探到 M={len(M)} / D={len(D)} / 候选={len(U)} / include={len(inc)} ──")
    add("# 幂等：无暂存变化则不提交、不推送——重跑本块结果相同（G-X120）")
    add(f'if ! {G} diff --cached --quiet; then')
    add(f'  {G} commit -m {q(msg)} && {G} push')
    add("else")
    add('  echo "无暂存变化，跳过提交"')
    add("fi")

    L += ["  " + ln if ln else "" for ln in body]
    L.append("fi")
    return "\n".join(L)


def emit_repo(repo: pathlib.Path, msg: str, max_untracked: int = 30, include=None) -> str:
    _idx, M, D, U = worktree_state(repo)
    return render_block(repo, M, D, U, msg, max_untracked, include, head_sha(repo))


# ─────────────────────────── 自检（含负向守卫） ───────────────────────────

def selftest() -> int:
    q = shlex.quote
    fake = pathlib.Path("/tmp/假 仓/有 空格")
    adversarial = ["-weird.txt", "中文 名.md", "a'b.md", "子目录/文件.txt", "--x"]

    block = render_block(fake, adversarial, ["删 掉.md"], ["未跟踪 候选.txt"], "msg: 测试", 30)
    gitlines = [ln.strip() for ln in block.splitlines()
                if ln.strip() and not ln.strip().startswith("#")]
    cmdlines = [ln.strip() for ln in block.splitlines() if ln.strip().startswith("git ")]

    cases = []
    cases.append(("① 永不出现 add -A/--all/-u/.", not any(x in block for x in BANNED_ADD)))
    cases.append(("② status --short 排在 add 之前",
                  block.find("status --short") < block.find("add --")))
    cases.append(("③ 每个路径都经引号（含空格/CJK/引号/前导横线）",
                  all(q(p) in block or _sh_repo(p) in block
                      for p in adversarial + ["删 掉.md", "未跟踪 候选.txt"])))

    def _after_ddash(path: str) -> bool:
        """该路径是否存在某一行，使其落在该行 `-- ` 分隔符**之后**。

        注意断言不能写成 `("-- " + q(p)) in block` —— 那只有在「该路径是一行里第一个被
        列出的路径」时才成立（2026-09-27 selftest 首跑就是这么写错的，FAIL 后订正）。
        """
        qp = q(path)
        return any(qp in ln and "-- " in ln and ln.index(qp) > ln.index("-- ")
                   for ln in block.splitlines())

    cases.append(("④ 危险路径落在 `--` 之后（防当选项解析）",
                  all(_after_ddash(p) for p in adversarial)))
    cases.append(("⑤ 幂等闸存在", "diff --cached --quiet" in block))
    cases.append(("⑥ 有未跟踪候选时必须给 git 自己判的机会", "check-ignore -v --" in block))
    cases.append(("⑦ 禁止 append 类写入（无 `>>`）", ">>" not in block))

    empty = render_block(fake, [], [], [], "msg", 30)
    cases.append(("⑧ 零变化时块内不出现悬空 add", "add --" not in empty))
    cases.append(("⑨ 零变化时仍有闸与幂等提交",
                  "status --short" in empty and "diff --cached --quiet" in empty))
    cases.append(("⑩ 删件进 add 清单（D 也要显式加）",
                  any(("add --" in ln and q("删 掉.md") in ln) for ln in block.splitlines())))

    # ⑪ 路径必须显示成 Doctor 终端原样可跑的形态（G-X134 同族：`~/mnt/...` 跑不了）
    sb = render_block(pathlib.Path("/sessions/cool-lucid-ritchie/mnt/Documents/Claude/brain"),
                      ["a.md"], [], [], "m", 30)
    cases.append(("⑪ 沙箱挂载路径映射为 ~/…（且块内不残留 /sessions/）",
                  "~/Documents/Claude/brain" in sb and "/sessions/" not in sb))

    # ⑫ --include 的未跟踪件必须**显式进 add**，而未列出的候选不得入册
    inc = render_block(fake, [], [], ["候选甲.txt", "候选乙.txt"], "m", 30, include=["核过件.txt"])
    cases.append(("⑫ include 进 add · 未列出的候选不入册",
                  any(("add --" in ln and q("核过件.txt") in ln) for ln in inc.splitlines())
                  and not any(("add --" in ln and q("候选甲.txt") in ln) for ln in inc.splitlines())))

    # ⑬⑭⑮ 2026-09-27 事故族：禁 cd / 双引号 $HOME / 仓守卫
    cases.append(("⑬ 块内不出现 `cd `（改用 git -C；防 cd 失败后跑错仓）",
                  not any(ln.startswith("cd ") for ln in gitlines)))
    cases.append(("⑭ 路径用 \"$HOME/…\" 双引号渲染（单引号会吞掉波浪号展开）",
                  '"$HOME/' in sb and "'~/" not in sb))
    cases.append(("⑮ 每条 git 命令都自带 -C",
                  bool(cmdlines) and all(ln.startswith("git -C ") for ln in cmdlines)))
    cases.append(("⑯ 仓存在性守卫在场（仓不在就跳过全部命令）",
                  '[ ! -d "$_repo/.git" ]' in block and "本块其余命令已跳过" in block))
    # ⚠ 这两个断言首版写宽了：`set -e` 命中了**注释**里那句「刻意不用 set -e」，
    #   而「每条 git 都带 -C」被守卫里的 `echo "…不是 git 仓…"` 文案绊倒。
    #   故一律只看**真命令行**（`gitlines` 已剔除注释；`cmdlines` 再收窄到首 token 是 git 的行）。
    cases.append(("⑰ 不出现 set -e / exit（会把 Doctor 的交互式终端关掉）",
                  not any("set -e" in ln for ln in gitlines)
                  and not any(ln == "exit" or ln.startswith("exit ") for ln in gitlines)))

    # ⑱ 活体：解析本工具所在仓的 index（只读，不跑 git）。
    #    自 __file__ 逐级向上找含 .git/index 的目录 —— 本工具被复制到别处跑时（如负向探针）
    #    不应因「/tmp 下没有仓」而误红（2026-09-27 首版就这么误红过一次）。
    here = pathlib.Path(__file__).resolve().parent
    repo_live = None
    for cand in [here, *here.parents]:
        if (cand / ".git" / "index").exists():
            repo_live = cand
            break
    if repo_live is None:
        cases.append(("⑱ 真仓 index 可解析（向上未找到 .git/index）", False))
    else:
        try:
            idx = read_index(repo_live)
            cases.append((f"⑱ 真仓 index 可解析（{repo_live} · {len(idx)} 条）", len(idx) > 0))
        except Exception as e:  # noqa: BLE001
            cases.append((f"⑱ 真仓 index 可解析（异常：{e}）", False))

    bad = 0
    for name, ok in cases:
        print(("  PASS  " if ok else "  FAIL  ") + name)
        bad += 0 if ok else 1
    print(f"\nselftest：{len(cases) - bad}/{len(cases)} 通过")
    return 1 if bad else 0


# ─────────────────────────── CLI ───────────────────────────

def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="探针输出 → 提交命令块（只读·不跑 git）")
    ap.add_argument("repos", nargs="*", help="仓路径（可多个；逐仓分开出块）")
    ap.add_argument("--msg", default="", help="提交信息（跨仓复用）")
    ap.add_argument("--max-untracked", type=int, default=30)
    ap.add_argument("--include", action="append", default=[],
                    help="人工**显式核过**的未跟踪件（相对仓路径），才会进 scoped add；可重复")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)

    if a.selftest:
        return selftest()

    if not a.repos:
        ap.print_help()
        return 2

    if not a.msg:
        print("⚠ 未给 --msg：块内会留空 message。加固②要求提交信息覆盖全部文件族。", file=sys.stderr)

    for r in a.repos:
        repo = pathlib.Path(os.path.expanduser(r)).resolve()
        if not (repo / ".git" / "index").exists():
            print(f"⚠ 跳过（无 .git/index）：{repo}", file=sys.stderr)
            continue
        idx, M, D, U = worktree_state(repo)
        # --include 自检：盘上不存在的直接剔除（否则块会照写、`git add` 报错、
        # 而块内没有 `set -e` ⇒ **静默跳过提交**——正是我们要消灭的那种失败形态）。
        Uset, inc = set(U), []
        for x in a.include:
            f = repo / x
            if not (f.exists() or f.is_symlink()):
                print(f"⚠ --include 丢弃 {x!r}：盘上不存在（拼写错？）", file=sys.stderr)
                continue
            if x not in Uset:
                print(f"⚠ --include {x!r} 不在未跟踪候选集内（已被跟踪？）——仍按你的指定入册",
                      file=sys.stderr)
            inc.append(x)
        print("```bash")
        print(render_block(repo, M, D, U, a.msg, a.max_untracked, inc, head_sha(repo)))
        print("```")
        print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
