#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""post_edit_selfcheck.py —— 改后自核（P6 的对策 · 2026-10-03 立 · 2026-10-03 迭代-2 增第 4 支 · 未经独立复验）

## 它治什么

**改完没回读**。2026-10-02 场的四个实证（方案件 P6）：

| # | 形态 | 实例 |
|---|---|---|
| 1 | **自证句写完即假** | 留痕说「Guadalupe／Hidalgo 在 CS-03 **全案** 0 命中」——**该句写完的那一刻就假了**（词串正存在于该留痕自身） |
| 2 | **版本号与标题没同批跟** | `G-NN命名空间对照表` 升了 frontmatter `version: v1.1`，**H1 标题仍写 `（v1.0）`** |
| 3 | 新写行触发体例闸 | 盘点件新写句带引号，新造 1 处写入侧闸 A 类未过 |
| 4 | **坐标类同型二次复发** | `TODO.md:54`→实 `:61`（当日又漂到 `:80`）· `经验库.md:3249`→实 `:3271` ⇒ **行号类坐标连「写对」都保不住** |

分别对应四个子命令：`claims` · `sync` · `quotes` · `asserts`。

## `asserts` 的射程与来源（不粉饰）

- **A · 坐标（闸）**：四条红 —— 件不存在 / 行号越界 / 目标行空行 / 锚串不在该行上；
  **前三条与 `check_quote_binding.py` 的 B 项（可达）同义** ⇒ 本支**复用其 `check()` 与 `Resolver`**（不重写规则），
  只按行区间取它的 `fb`；**第 4 条（锚串复算）是本支新增**（实测：`check_quote_binding` 对「纯坐标 + 非空行 + 内容
  不符」**不转红**，故不属重复造轮子）。**不整体照跑它的 A/C 项** —— 域外件上实测 A 未过数百、C 未过数条，是假报机。
- **B · 量词 / C · 自造术语：提示器，非闸。** B 的词表是**开放集、不是穷举**；B 的豁免窗口＝同行／紧邻 ±2 行。
  **B/C 在 `--strict` 下也只提示，不计入返回码。**（2026-10-03 订正：此前 `--strict` 会把 B/C 计入 rc —— 那等于把**开放集启发式**升成闸，既制造假红，又会**逼出族 10「修红反噬」**：为过闸去改被测对象。该升闸开关退役。）
- **默认只报（rc=0）**；`--strict` ⇒ **仅 A 的红**计入 rc=1。
- **`--file` 自身读不了 ⇒ rc=2（环境）；坐标所指的件不存在 ⇒ 红（不是 rc=2）。**
- **解析根**：件所在目录 → 其父 → docs 根 → `--root` 补。**根给少了会假红**（同族实测：漏根时报 53 条、补根后 0 条）。
- **不做 `quotes` 那道域闸**：坐标问题在 `brain/**` 一样犯，`asserts` 刻意**域中立** —— 此为有意，不是漏做。
- **建议只对「本批新写的行区间」跑**（`--lines A B`）：件内**历史引证**的坐标（族例里的 `checkups/…:NNN`、案例目录
  相对引用等）根在别处，整件跑会出**已知噪声** —— 那是「不可解析」，不是本批缺陷。**噪声与真红的区分判据 ＝
  该坐标在不在本批 `fixed` 面内。**

## 边界（必读 · 不粉饰）

- **`claims` 只复算「范围可机械解析」的两类自证句**：`<串> … 命中 N 处` 与 `<串> … 0 命中`。
  范围解析规则写在 `_resolve_scope()` 里，**解析不出的会逐条列出**（叫「未能复算」，不是「通过」）。
  **「未能复算」是有意显形的** —— 让写自证句的人知道：范围写不清楚，这句话就没人能替你核。
- **`sync` 的「枚举」一栏是提示清单，不是判据**：它只把件内的计数式声明列出来给人核，
  **不自动判定**（自动判定需要知道每个数的应该有值，那超出机械可判的范围）。
- **`quotes` 不重写体例规则**：它调用 `check_quote_binding.check()`（生产谓词），
  只把红线**按行区间过滤**。体例本身的真伪仍归该工具。
- **它拦不住 Edit**（Edit 不过 shell）⇒ 它是**交付前自核的机械部分**，人读那半不能省。

## 用法

    python3 post_edit_selfcheck.py claims  --file <md> [--docs DIR] [--strict]
    python3 post_edit_selfcheck.py sync    --file <md>
    python3 post_edit_selfcheck.py quotes  --file <md> --lines A B [--docs DIR] [--root R] [--force]
    python3 post_edit_selfcheck.py asserts --file <md> [--lines A B] [--docs DIR] [--root R] [--strict]
    python3 post_edit_selfcheck.py --self-test

## 退出码

    0 = 无红项        1 = 有红项（claims 的「未能复算」须加 --strict 才计入）
    2 = 环境不可用（目标件读不了 / docs 根不可达 / check_quote_binding 导入失败）—— fail-closed
"""
from __future__ import annotations

import argparse
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent

HIT_STMT = re.compile(r"(?P<subj>[^\s，。；]{1,40}?)"
                      r"(?:[^。\n]{0,24}?)"
                      r"(?:命中|出现|找到)\s*(?P<n>\d+)\s*(?:处|次|条|个)?")
ZERO_STMT = re.compile(r"(?:0\s*命中|零\s*命中|无一处|没有一处|零处)")
COUNT_DECL = re.compile(r"(?:共|合计|总计)\s*(\d+)\s*(?:条|项|例|处|个|件|族)")
VERSION_IN_H1 = re.compile(r"[（(]\s*(v\d+(?:\.\d+)*)\s*[）)]")


def read(p: pathlib.Path):
    try:
        return p.read_text(encoding="utf-8", errors="replace").split("\n")
    except OSError:
        return None


def find_docs_root(explicit):
    """显式 --docs 具权威性；无效即 None（调用方 rc=2），**不回落默认根**。"""
    if explicit:
        c = pathlib.Path(explicit).expanduser()
        try:
            return c.resolve() if (c / "brain").is_dir() else None
        except OSError:
            return None
    for c in (HERE.parent.parent, HERE.parent.parent.parent):
        try:
            if (c / "brain").is_dir():
                return c.resolve()
        except OSError:
            continue
    return None


def _corpus(scope: pathlib.Path, exts=(".md",)):
    if scope.is_file():
        return [scope]
    return sorted(p for p in scope.rglob("*") if p.is_file() and p.suffix.lower() in exts)


def _count(subject: str, scope: pathlib.Path, docs: pathlib.Path | None):
    """复算 subject 在 scope 内的**出现总次数**（非行数）。"""
    if not scope.exists():
        return None
    total = 0
    for f in _corpus(scope):
        lines = read(f)
        if lines is None:
            continue
        total += sum(ln.count(subject) for ln in lines)
    return total


def _resolve_scope(line: str, target: pathlib.Path, docs: pathlib.Path | None):
    """把自证句里的「范围」解析成一个路径。解析不出返回 (None, 原因)。

    规则（**全部写在代码里，不靠记忆**）：
      ① 同行反引号里的路径/文件名 → 按 `target 所在目录` 与 `docs 根` 依次解析
      ② 同行反引号外的 `X.md` 形态 → 同上
      ③ 含「全仓/全库」→ docs 根
      ④ 含「本件/全文」→ target 自身
      ⑤ 含「全案/全案文」→ **不机械解析**（案例目录边界须人给）⇒ 报不可解析
    """
    m = re.search(r"`([^`]+\.(?:md|json|py|txt|yaml|yml))`", line) or \
        re.search(r"([\w一-鿿./\-]+\.(?:md|json|py|txt|yaml|yml))", line)
    if m:
        rel = m.group(1)
        for base in (target.parent, docs):
            if base is None:
                continue
            cand = base / rel
            if cand.exists():
                return cand, ""
        return None, f"路径 `{rel}` 未解析到（试了 {target.parent} 与 docs 根）"
    if "全仓" in line or "全库" in line:
        return (docs, "") if docs else (None, "含「全仓/全库」但 docs 根不可得")
    if "全案" in line:
        return None, "含「全案」——案例目录边界不机械解析，须人给具体件"
    if "本件" in line or "全文" in line:
        return target, ""
    return None, "无法判定范围（既无文件名，也无全仓/本件一类限定）"


def cmd_claims(args) -> int:
    target = pathlib.Path(args.file).expanduser()
    lines = read(target)
    if lines is None:
        print(f"✗ 读不了：{target}", file=sys.stderr)
        return 2
    docs = find_docs_root(args.docs)
    if args.docs and docs is None:
        print(f"✗ --docs 不可达（须含 brain/）：{args.docs}", file=sys.stderr)
        return 2
    red, unresolved, checked = [], [], 0
    for i, line in enumerate(lines, 1):
        is_hit = bool(HIT_STMT.search(line))
        is_zero = bool(ZERO_STMT.search(line))
        if not (is_hit or is_zero):
            continue
        # 主体 = 该行第一个「…」里的串；没有就取第一个反引号串
        ms = re.search(r"「([^」]{2,})」", line) or re.search(r"`([^`]{2,})`", line)
        if not ms:
            unresolved.append((i, "有命中声明但抽不出主体串", line.strip()[:100]))
            continue
        subj = ms.group(1)
        scope, why = _resolve_scope(line, target, docs)
        if scope is None:
            unresolved.append((i, why, line.strip()[:100]))
            continue
        actual = _count(subj, scope, docs)
        if actual is None:
            unresolved.append((i, "范围内无件可数", line.strip()[:100]))
            continue
        checked += 1
        if is_zero and actual > 0:
            red.append((i, f"写「0 命中」，实为 {actual} 处（主体「{subj}」· 范围 {scope.name}）",
                        line.strip()[:100]))
        elif is_hit:
            stated = int(HIT_STMT.search(line).group("n"))
            if stated != actual:
                red.append((i, f"写「{stated} 处」，实为 {actual} 处（主体「{subj}」· 范围 {scope.name}）",
                            line.strip()[:100]))
    print(f"# 自证句复核 · {target.name}")
    print(f"# 复算 {checked} 句 · 红 {len(red)} · 未能复算 {len(unresolved)}")
    for i, why, text in red:
        print(f"   ✗ L{i}：{why}\n       > {text}")
    if unresolved:
        print(f"\n# ⚠ 未能复算（**不是通过**）· {len(unresolved)} 句：")
        for i, why, text in unresolved:
            print(f"   ? L{i}：{why}\n       > {text}")
        print("   处置：把范围写成可机械解析的形式（点名到件），否则这句话没人能替你核。")
    print(f"\n判据：红 == 0{'且未能复算 == 0' if args.strict else ''} ⇒ 过"
          f"{'（--strict）' if args.strict else '（未开 --strict：未能复算不计红）'}")
    if red or (args.strict and unresolved):
        return 1
    return 0


def cmd_sync(args) -> int:
    target = pathlib.Path(args.file).expanduser()
    lines = read(target)
    if lines is None:
        print(f"✗ 读不了：{target}", file=sys.stderr)
        return 2
    # frontmatter
    fm = {}
    if lines and lines[0].strip() == "---":
        try:
            end = next(i for i, l in enumerate(lines[1:], 1) if l.strip() == "---")
        except StopIteration:
            end = None
        if end:
            try:
                import yaml
                fm = yaml.safe_load("\n".join(lines[1:end])) or {}
            except Exception as e:                          # noqa: BLE001
                print(f"✗ frontmatter 解析失败：{e}", file=sys.stderr)
                return 2
    fm_ver = str(fm.get("version", "")).strip()
    h1 = next((l for l in lines if l.startswith("# ")), "")
    h1_ver = (VERSION_IN_H1.search(h1) or [None, ""])[1] if h1 else ""
    red = []
    if fm_ver and h1_ver:
        norm = lambda s: s.lstrip("vV").strip()                       # noqa: E731
        if norm(fm_ver) != norm(h1_ver):
            red.append(f"frontmatter version = {fm_ver}，H1 标题写 {h1_ver} —— 头尾不同步")
    print(f"# 版本号 ↔ 标题同步核 · {target.name}")
    print(f"   frontmatter version = {fm_ver or '(无)'} · H1 版本 = {h1_ver or '(无)'}")
    if not fm_ver or not h1_ver:
        print("   · 不适用（缺一侧）——**不是通过**，是这一栏核不了")
    for r in red:
        print(f"   ✗ {r}")

    # 枚举栏：只列给人核，不代判
    decls = [(i, l.strip()) for i, l in enumerate(lines, 1) if COUNT_DECL.search(l)]
    print(f"\n# 枚举栏（**提示清单，非判据**）· 件内计数式声明 {len(decls)} 处，逐条人核：")
    for i, text in decls[:40]:
        print(f"   L{i}: {text[:120]}")
    if len(decls) > 40:
        print(f"   …另有 {len(decls) - 40} 处（未列全，按需自取）")
    if not decls:
        print("   （无）")
    print("\n判据：版本号一栏红 == 0 ⇒ 过；枚举栏**不计红**（须人核）。")
    return 1 if red else 0


def cmd_quotes(args) -> int:
    target = pathlib.Path(args.file).expanduser()
    if not target.exists():
        print(f"✗ 目标件不存在：{target}", file=sys.stderr)
        return 2
    # ★ 域闸（2026-10-03 由实测假报逮出后加）：`check_quote_binding.py` 的体例判据**只适用于 PEC 树**。
    #   实测：对 `brain/.skills/damper/SKILL.md`（域外）跑一次 ⇒ **324 条 A 未过，全部是「术语加引号」的误判**。
    #   域外照跑＝造一台假报机（族 4：假报训练人忽略告警）⇒ 默认拒绝，须显式 --force。
    if "Projects/PEC" not in target.as_posix() and not args.force:
        print(f"# 新写行引号体例核 · {target.name}")
        print("   · **不适用** —— 本栏判据（`check_quote_binding.py`）**只适用于 PEC 树**"
              "（该域已写在 damper §六）。")
        print("   ⇒ **不适用 ≠ 通过**：域外件这一栏核不了，须人工读，或加 `--force` 强行跑（自担假报）。")
        return 0
    if str(HERE) not in sys.path:
        sys.path.insert(0, str(HERE))
    try:
        import check_quote_binding as cqb
    except Exception as e:                                   # noqa: BLE001
        print(f"✗ 导入 check_quote_binding 失败：{e}", file=sys.stderr)
        return 2
    docs = find_docs_root(args.docs)
    # ⚠ 引用解析根必须给全（2026-10-03 实测）：件内相对引用的根**不止一个** ——
    #   如 PEC 件里既有 `共享基础/历史时间线.md`（根＝案例目录）又有 `文明基因/判据/…`（根＝PEC 根）。
    #   根给少了 ⇒ A 项**假报「上逐字找不到」**（实测：漏根时该件报 53 条，补根后 0 条）。故默认给
    #   件目录、其父目录，并支持 --root 显式补根。
    roots = [str(target.parent), str(target.parent.parent)]
    for r in getattr(args, "root", []) or []:
        for base in (pathlib.Path.cwd(), docs):
            if base is None:
                continue
            cand = (base / r)
            if cand.exists():
                roots.append(str(cand.resolve()))
                break
        else:
            roots.append(r)
    if docs:
        roots.append(str(docs))
    res, errs = cqb.check(str(target), roots)
    if res is None:
        print(f"✗ 检查器返回空：{errs}", file=sys.stderr)
        return 2
    lo, hi = (args.lines[0], args.lines[1]) if args.lines else (0, 10 ** 9)
    rows = []
    for tag, key in (("A", "fa"), ("A2", "fa2"), ("C", "fc")):
        for item in res.get(key, []):
            ln = item[1]
            if lo <= ln <= hi:
                rows.append((tag, ln, item[2] if len(item) > 2 else "", item[-1]))
    print(f"# 新写行引号体例核 · {target.name} · 行区间 [{lo}, {hi}]")
    print(f"# 体例判据取自 check_quote_binding.check()（生产谓词，未重写）")
    print(f"# 该件全文：A 过 {res.get('ok_a', 0)} · B 过 {res.get('ok_b', 0)} · "
          f"A 未过 {len(res.get('fa', []))} · A2 {len(res.get('fa2', []))} · C {len(res.get('fc', []))} · "
          f"D {len(res.get('fd', []))}")
    for tag, ln, q, why in rows:
        print(f"   ✗ [{tag}] L{ln}: {why}" + (f"  「{q}」" if q else ""))
    if not rows:
        print("   ✓ 区间内无 A／A2／C 未过项")
    print("\n判据：区间内未过项 == 0 ⇒ 过。⚠ 全文级未过项须另跑 check_quote_binding.py（本件不代替它）。")
    return 1 if rows else 0


def cmd_asserts(args) -> int:
    """断言可核化三查（2026-10-03 加 · 治「新写断言未核」的坐标／量词／自造术语三形态）。

    **A · 坐标（闸）**：A1 可达类 —— **复用 `check_quote_binding.check()` 的 B 项**（生产谓词，不重写：
    件不存在／行号越界／目标行空行）；A2 锚串类 —— **本支新增**：每个 `` `文件:行号` `` 须在**同行或 ±1 行**
    给出一个「最近锚串」（`「…」` 或 `` `…` `` 短串，≥2 字且不含空格），并复算该锚串在**目标行上逐字存在**。
    ⚠ **只认同行锚串**（2026-10-03 首次真盘跑后由「同行或 ±1 行」收紧）：按 ±1 行取最近会把**邻行的无关串**
    当锚、造出**假红**（实测 `TODO.md:54` 被配上邻行「**以新方式犯错为主**」）⇒ 跨行**一律降为「裸坐标·黄」**。
    红时附**该行现文**与**该锚串在全文的现命中行** —— 让读者一眼分辨「我写错了」还是「文件漂了」。

    **B · 量词 · C · 自造术语：提示器，非闸**（docstring 段「射程与来源」已写明）。
    """
    target = pathlib.Path(args.file).expanduser()
    lines = read(target)
    if lines is None:
        print(f"✗ 读不了：{target}", file=sys.stderr)          # ← 环境问题 ⇒ rc=2（**不是红**）
        return 2
    if str(HERE) not in sys.path:
        sys.path.insert(0, str(HERE))
    try:
        import check_quote_binding as cqb                     # noqa: N813
    except Exception as e:                                    # noqa: BLE001
        print(f"✗ 导入 check_quote_binding 失败：{e}", file=sys.stderr)
        return 2
    docs = find_docs_root(args.docs)
    if args.docs and docs is None:
        print(f"✗ --docs 不可达（须含 brain/）：{args.docs}", file=sys.stderr)
        return 2
    # ⚠ 解析根策略**写死在此**（R7）：件目录 → 其父 → **docs/brain** → docs 根 → `--root` 补。
    #   根给少了会**假红**（本仓实测两次：同族检查漏根时报 53 条、补根后 0 条；本支首次真盘跑时
    #   又因缺 `brain/` 把 `TODO.md` `经验库.md` 这类**仓内相对引用**报成「文件不存在」）。
    roots = [str(target.parent), str(target.parent.parent)]
    if docs and (docs / "brain").is_dir():
        roots.append(str(docs / "brain"))
    for r in (getattr(args, "root", []) or []):
        for base in (pathlib.Path.cwd(), docs):
            if base is None:
                continue
            cand = base / r
            if cand.exists():
                roots.append(str(cand.resolve()))
                break
        else:
            roots.append(r)
    if docs:
        roots.append(str(docs))
    lo, hi = (args.lines[0], args.lines[1]) if args.lines else (1, len(lines))

    print(f"# 断言可核化三查 · {target.name} · 行区间 [{lo}, {hi}] · 解析根 {len(roots)} 个")

    # ── A1 · 可达类：复用 cqb 的 B 项（不重写规则）
    res, _errs = cqb.check(str(target), roots)
    reach = [(i, rel, n, why) for (_t, i, rel, n, why) in res.get("fb", []) if lo <= i <= hi]

    # ── A2 · 锚串类（本支新增）
    nomemo, anchor_red = [], []
    resolver = cqb.Resolver(roots)
    coin_re = re.compile(r"`([^`]{2,})`")
    for i in range(lo, min(hi, len(lines)) + 1):
        line = lines[i - 1]
        cites = [(m.group(1), m.group(2), m.start(), m.end()) for m in cqb.CITE.finditer(line)]
        if not cites:
            continue
        # 候选锚串：**只认同行**（2026-10-03 首次真盘跑后收紧）。
        #   ⚠ 原本按「同行或 ±1 行、取最近」实现 ⇒ 真盘上把**邻行的无关串**当了锚、造出假红
        #   （实测：`TODO.md:54` 被配上邻行「**以新方式犯错为主**」）。跨行的**一律降为「裸坐标·黄」** ——
        #   宁可黄，不可假红（假红训练人忽略告警）。
        cands = []
        raw = line
        for m in cqb.QUOTE.finditer(raw):
            if 2 <= len(m.group(1)) <= 60 and " " not in m.group(1):
                cands.append((m.group(1), m.start(), m.end()))
        for m in coin_re.finditer(raw):
            s = m.group(1)
            if cqb.CITE.fullmatch(m.group(0)) or (":" in s and s.rsplit(":", 1)[-1].isdigit()):
                continue                                       # 这个反引号本身就是坐标，不是锚串
            if 2 <= len(s) <= 60 and " " not in s:
                cands.append((s, m.start(), m.end()))
        for rel, n, cs, ce in cites:
            real, src = resolver.resolve(rel)
            if not (real and src and 1 <= int(n) <= len(src)):
                continue                                       # 可达类已由 A1 报，避免重报
            # ★ 只认**紧贴该坐标之前**（间距 ≤2 字）的锚串 —— 这是本仓的书写约定「锚串`件:行`」。
            #   ⚠ 原按「同行取最近」实现 ⇒ 真盘上挑错了锚：一行里多个引号串并存时，「最近」≠「所属」
            #   （实测 `TODO.md:54` 被配上同行的「**以新方式犯错为主**」）⇒ 造出**假红**。
            #   其余情形**一律降为「裸坐标·黄」** —— 宁可黄，不可假红（假红训练人忽略告警）。
            near = [c for c in cands if 0 <= (cs - c[2]) <= 2]
            if not near:
                nomemo.append((i, rel, n))
                continue
            anchor = near[-1][0]
            if anchor not in src[int(n) - 1]:
                hitlines = [j for j, l in enumerate(src, 1) if anchor in l]
                anchor_red.append((i, rel, n, anchor, src[int(n) - 1].strip()[:110], hitlines[:5]))

    # ── B · 量词（提示器）
    QUANT = re.compile(r"全部|所有|任何|无一|唯一|永远|从不|绝不|恰好|零个|零处|恒(?![定等])|必(?!须|需)")
    EXEMPT = re.compile(r"反证：|穷尽：|<!-- quant-ok")
    quant_hits = []
    for i in range(lo, min(hi, len(lines)) + 1):
        line = lines[i - 1]
        if not QUANT.search(line):
            continue
        window = "\n".join(lines[max(0, i - 3):i + 2])
        if cqb.CITE.search(window) or EXEMPT.search(window):
            continue
        quant_hits.append((i, QUANT.search(line).group(0), line.strip()[:110]))

    # ── C · 自造术语（提示器）：形如 v数字 / 字母数字编号，且**全件只出现 1 次**
    whole = "\n".join(lines)
    coins = []
    for m in re.finditer(r"`(v\d+|[A-Za-z]{1,6}\d+(?:-\d+)*)`|\*\*(v\d+|[A-Za-z]{1,6}\d+(?:-\d+)*)\*\*",
                         whole):
        tok = m.group(1) or m.group(2)
        if tok and whole.count(tok) == 1:
            ln = whole[:m.start()].count("\n") + 1
            if lo <= ln <= hi:
                coins.append((ln, tok))

    print(f"\n■ A1 · 可达类红（复用 cqb B 项）· {len(reach)} 处")
    for i, rel, n, why in reach:
        print(f"   ✗ L{i} `{rel}:{n}` —— {why}")
        print(f"        · 写法提示：仓内坐标请写**相对 `brain/` 的完整路径**（如 `permanent/经验库.md:3271`）—— "
              f"裸文件名在多目录同名时机器不可解析")
    print(f"\n■ A2 · 锚串类红（本支新增）· {len(anchor_red)} 处")
    for i, rel, n, anchor, cur, hl in anchor_red:
        print(f"   ✗ L{i} `{rel}:{n}` 的锚串「{anchor}」在该行上找不到")
        print(f"        · 该行现文：{cur}")
        print(f"        · 「{anchor}」在全文的现命中行：{hl if hl else '（全文 0 命中）'}")
    if nomemo:
        print(f"\n□ 裸坐标（同行无锚串，黄 · 机器不可核）· {len(nomemo)} 处")
        for i, rel, n in nomemo[:12]:
            print(f"   ? L{i} `{rel}:{n}`")
        if len(nomemo) > 12:
            print(f"   ? …另 {len(nomemo) - 12} 处")
        print("   处置：在该坐标**同行**补一个可在目标行上逐字找到的锚串（「…」或 `…`）。")
    print(f"\n■ B · 量词（**提示器**）· {len(quant_hits)} 处 —— 词表是**开放集、不是穷举**")
    for i, w, text in quant_hits[:12]:
        print(f"   ? L{i} 「{w}」 {text}")
    print(f"\n■ C · 自造术语（**提示器**，本件仅出现 1 次）· {len(coins)} 处")
    for ln, tok in coins[:12]:
        print(f"   ? L{ln} `{tok}` —— 疑未定义／无出处")
    rn = len(reach) + len(anchor_red)
    print(f"\n判据：A 红 {rn} 处{'（--strict ⇒ 计入 rc）' if args.strict else '（默认只报，rc 不因此变）'}；"
          f"B/C 共 {len(quant_hits) + len(coins)} 处命中**恒为提示器**，不计入 rc。")
    print("⚠ `--file` 自身读不了 ⇒ rc=2（环境）；**坐标所指的件不存在 ⇒ 红**（不是 rc=2）。")
    if args.strict and rn:
        return 1
    return 0


# ────────────────────────────── self-test ──────────────────────────────

def self_test() -> int:
    import contextlib
    import io
    import shutil
    import tempfile

    cases = []

    def run(fn):
        buf = io.StringIO()
        try:
            with contextlib.redirect_stdout(buf):
                fn()
            return True, ""
        except AssertionError as e:
            return False, f"{e}\n     ↓ 该例捕获输出 ↓\n" + "\n".join(
                "     " + ln for ln in buf.getvalue().rstrip().split("\n"))

    tmp = pathlib.Path(tempfile.mkdtemp(prefix="pesc_selftest_"))
    try:
        docs = tmp
        (docs / "brain").mkdir()

        # T1 自证句：写「0 命中」而实际有 ⇒ 红
        def t1():
            src = tmp / "src.md"
            src.write_text("甲甲乙\n乙乙丙\n", encoding="utf-8")
            tgt = tmp / "claim1.md"
            tgt.write_text("核查：「甲甲乙」在 `src.md` 全文中 0 命中。\n", encoding="utf-8")
            rc = cmd_claims(argparse.Namespace(file=str(tgt), docs=None, strict=False))
            assert rc == 1, f"应判红，实为 rc={rc}"
        cases.append(("T1 「0 命中」而实际有 ⇒ 红", run(t1)))

        # T2 自证句写对 ⇒ 绿
        def t2():
            tgt = tmp / "claim2.md"
            tgt.write_text("核查：「丙丁」在 `src.md` 中 0 命中。\n", encoding="utf-8")
            rc = cmd_claims(argparse.Namespace(file=str(tgt), docs=None, strict=False))
            assert rc == 0, f"应绿，实为 rc={rc}"
        cases.append(("T2 自证句为真 ⇒ 绿", run(t2)))

        # T3 「N 命中」数字不符 ⇒ 红
        def t3():
            tgt = tmp / "claim3.md"
            tgt.write_text("全仓「乙乙」命中 5 处。\n", encoding="utf-8")
            rc = cmd_claims(argparse.Namespace(file=str(tgt), docs=str(tmp), strict=False))
            assert rc == 1, f"数字不符应红，实为 rc={rc}"
        cases.append(("T3 命中数不符 ⇒ 红", run(t3)))

        # T4 范围解析不出 ⇒ 计入「未能复算」；非 strict 不判红，strict 判红
        def t4():
            tgt = tmp / "claim4.md"
            tgt.write_text("核查：「甲甲乙」在 CS-03 全案 0 命中。\n", encoding="utf-8")
            rc = cmd_claims(argparse.Namespace(file=str(tgt), docs=str(tmp), strict=False))
            assert rc == 0, f"非 strict 不应判红，实为 rc={rc}"
            rc = cmd_claims(argparse.Namespace(file=str(tgt), docs=str(tmp), strict=True))
            assert rc == 1, f"strict 应判红，实为 rc={rc}"
        cases.append(("T4 未能复算：非 strict 不红 / strict 红", run(t4)))

        # T5 version ↔ H1 不同步 ⇒ 红
        def t5():
            tgt = tmp / "ver1.md"
            tgt.write_text("---\nversion: v1.1\n---\n\n# 对照表（v1.0）\n\n共 3 条。\n", encoding="utf-8")
            rc = cmd_sync(argparse.Namespace(file=str(tgt)))
            assert rc == 1, f"不同步应红，实为 rc={rc}"
        cases.append(("T5 version≠H1 ⇒ 红", run(t5)))

        # T6 version ↔ H1 同步 ⇒ 绿
        def t6():
            tgt = tmp / "ver2.md"
            tgt.write_text("---\nversion: v1.1\n---\n\n# 对照表（v1.1）\n", encoding="utf-8")
            rc = cmd_sync(argparse.Namespace(file=str(tgt)))
            assert rc == 0, f"同步应绿，实为 rc={rc}"
        cases.append(("T6 version=H1 ⇒ 绿", run(t6)))

        # T7 缺一侧 ⇒ 不适用、不判红（**不是通过**）
        def t7():
            tgt = tmp / "ver3.md"
            tgt.write_text("# 无版本标题\n", encoding="utf-8")
            rc = cmd_sync(argparse.Namespace(file=str(tgt)))
            assert rc == 0, f"不适用不应判红，实为 rc={rc}"
        cases.append(("T7 缺 version/H1 ⇒ 不适用不判红", run(t7)))

        # T8 quotes：区间内有 A 未过 ⇒ 红；区间外 ⇒ 绿（并披露全文级未过）。**须 --force（域外件）**
        def t8():
            src = tmp / "a.md"
            src.write_text("甲甲甲\n", encoding="utf-8")
            tgt = tmp / "q.md"
            tgt.write_text("第一行正常。\n这是「甲甲甲」但没有出处的行。\n", encoding="utf-8")
            rc = cmd_quotes(argparse.Namespace(file=str(tgt), lines=[2, 2], docs=str(tmp), force=True))
            assert rc == 1, f"区间内 A 未过应红，实为 rc={rc}"
            rc = cmd_quotes(argparse.Namespace(file=str(tgt), lines=[1, 1], docs=str(tmp), force=True))
            assert rc == 0, f"区间外应绿，实为 rc={rc}"
        cases.append(("T8 quotes 按行区间过滤（--force）", run(t8)))

        # T11 域闸：非 PEC 树默认拒绝（**不适用 ≠ 通过**），不得产出成百条假报
        def t11():
            tgt = tmp / "domain.md"
            tgt.write_text("这里「全是」加引号的「术语」，「一条」出处也没有。\n", encoding="utf-8")
            rc = cmd_quotes(argparse.Namespace(file=str(tgt), lines=[1, 1], docs=str(tmp), force=False))
            assert rc == 0, f"域外默认应 rc=0（不适用），实为 {rc}"
            pec = tmp / "Projects" / "PEC"
            pec.mkdir(parents=True, exist_ok=True)
            tgt2 = pec / "in.md"
            tgt2.write_text("这里「全是」加引号的「术语」。\n", encoding="utf-8")
            rc = cmd_quotes(argparse.Namespace(file=str(tgt2), lines=[1, 1], docs=str(tmp), force=False))
            assert rc == 1, f"域内应真跑并判红，实为 {rc}"
        cases.append(("T11 域闸：域外不适用 / 域内真跑", run(t11)))

        # ── asserts 六例（2026-10-03 加）
        def t12():
            (tmp / "a.md").write_text("甲甲甲\n", encoding="utf-8")
            tgt = tmp / "as1.md"
            tgt.write_text("见「乙乙乙」`a.md:1` 处。\n", encoding="utf-8")
            rc = cmd_asserts(argparse.Namespace(file=str(tgt), docs=str(tmp), lines=None,
                                                root=[], strict=True))
            assert rc == 1, f"锚串不在目标行应判红，实为 {rc}"
        cases.append(("T12 asserts·A2 锚串不符 ⇒ 红", run(t12)))

        def t13():
            tgt = tmp / "as2.md"
            tgt.write_text("见「甲甲甲」`a.md:1` 处。\n", encoding="utf-8")
            rc = cmd_asserts(argparse.Namespace(file=str(tgt), docs=str(tmp), lines=None,
                                                root=[], strict=True))
            assert rc == 0, f"锚串相符应绿，实为 {rc}"
        cases.append(("T13 asserts·A2 锚串相符 ⇒ 绿", run(t13)))

        def t18():
            # 回归锁：锚串**不紧贴**坐标（写在坐标之后 / 隔了别的字）⇒ 只降为「裸坐标·黄」，**不得假红**。
            #   依据＝2026-10-03 首次真盘跑：按「同行取最近」会把无关串当锚、造出假红。
            tgt = tmp / "as6.md"
            tgt.write_text("见 `a.md:1` 里的「乙乙乙」。\n", encoding="utf-8")
            import contextlib
            import io
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                rc = cmd_asserts(argparse.Namespace(file=str(tgt), docs=str(tmp), lines=None,
                                                    root=[], strict=True))
            out = buf.getvalue()
            assert rc == 0, f"非紧贴锚串不得判红（宁可黄），实为 rc={rc}"
            assert "裸坐标" in out, "未降级为「裸坐标」"
        cases.append(("T18 asserts·A2 非紧贴锚串 ⇒ 黄不红（假红回归锁）", run(t18)))

        # T19 · 解析根回归锁（治「缺 docs/brain ⇒ 把仓内相对引用报成文件不存在」）
        #   ⚠ T18 锁不住这两处修复 —— 2026-10-03 修后审变异实测证明：删掉 `docs/brain` 根、或把「紧贴」
        #   放宽回「坐标之前的最近候选」，**自测仍 18/18 全绿**。故本版补 T19／T19b 两条**真锁**。
        def t19():
            (tmp / "a.md").write_text("甲甲甲\n", encoding="utf-8")   # 已在上文建过，此处确保在场
            (tmp / "brain" / "TODO.md").write_text("甲甲甲\n", encoding="utf-8")
            tgt = tmp / "as7.md"
            tgt.write_text("见「甲甲甲」`TODO.md:1`。\n", encoding="utf-8")   # 坐标根＝docs/brain
            rc = cmd_asserts(argparse.Namespace(file=str(tgt), docs=str(tmp), lines=None,
                                                root=[], strict=True))
            assert rc == 0, f"经 docs/brain 可解析的仓内相对引用不应判红，实为 {rc}"
        cases.append(("T19 asserts·解析根含 docs/brain（回归锁）", run(t19)))

        def t19b():
            # 紧贴判据的回归锁：候选锚串在坐标**之前但不相邻** ⇒ 严格版只降黄；放宽版会拿它当锚 ⇒ 红
            tgt = tmp / "as8.md"
            tgt.write_text("见「丙丙丙」这个词，另见 `a.md:1`。\n", encoding="utf-8")
            rc = cmd_asserts(argparse.Namespace(file=str(tgt), docs=str(tmp), lines=None,
                                                root=[], strict=True))
            assert rc == 0, f"非相邻锚串应只降为黄、不得判红，实为 {rc}"
        cases.append(("T19b asserts·只认紧贴锚串（回归锁）", run(t19b)))

        def t14():
            tgt = tmp / "as3.md"
            tgt.write_text("见 `nope.md:1` 处。\n", encoding="utf-8")
            rc = cmd_asserts(argparse.Namespace(file=str(tgt), docs=str(tmp), lines=None,
                                                root=[], strict=True))
            assert rc == 1, f"件不存在应判红（不是 rc=2），实为 {rc}"
        cases.append(("T14 asserts·A1 件不存在 ⇒ 红", run(t14)))

        def t15():
            tgt = tmp / "as4.md"
            # ⚠ 夹具要点：两条量词句须**拉开 ≥4 行** —— B 的豁免窗口是「同行／紧邻 ±2 行」，
            #   贴太近会让「有出处」那条把「无出处」那条一并豁免（2026-10-03 首跑踩过，是夹具错不是实现错）
            tgt.write_text("这一条全部都适用。\n\n\n\n这一条全部都适用。见 `a.md:1`。\n",
                           encoding="utf-8")
            import contextlib
            import io
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                rc = cmd_asserts(argparse.Namespace(file=str(tgt), docs=str(tmp), lines=[1, 1],
                                                    root=[], strict=True))
            out = buf.getvalue()
            assert rc == 0 and "量词" in out, "量词提示应保留，但不得令 strict 失败"
            with contextlib.redirect_stdout(io.StringIO()):
                rc2 = cmd_asserts(argparse.Namespace(file=str(tgt), docs=str(tmp), lines=[5, 5],
                                                     root=[], strict=True))
            assert rc2 == 0, f"有出处的量词行应豁免，实为 {rc2}"
        cases.append(("T15 asserts·B 量词：无出处报/有出处免", run(t15)))

        def t16():
            tgt = tmp / "as5.md"
            tgt.write_text("本批叫 `v9` 这个批次。\n`G-X206` 与 `G-X206`。\n", encoding="utf-8")
            import contextlib
            import io
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                rc = cmd_asserts(argparse.Namespace(file=str(tgt), docs=str(tmp), lines=[1, 1],
                                                    root=[], strict=True))
            out = buf.getvalue()
            assert rc == 0 and "v9" in out, "术语提示应保留，但不得令 strict 失败"
            tail = out.split("■ C ·")[1] if "■ C ·" in out else ""
            assert "G-X206" not in tail, "出现两次的 `G-X206` 不应被报为疑未定义"
        cases.append(("T16 asserts·C 自造术语：一次报/两次免", run(t16)))

        def t17():
            rc = cmd_asserts(argparse.Namespace(file=str(tmp / "nope.md"), docs=None, lines=None,
                                                root=[], strict=False))
            assert rc == 2, f"`--file` 自身读不了应 rc=2，实为 {rc}"
        cases.append(("T17 asserts：--file 读不了 ⇒ rc=2（环境≠红）", run(t17)))

        # T9 目标件不存在 ⇒ rc=2
        def t9():
            rc = cmd_claims(argparse.Namespace(file=str(tmp / "nope.md"), docs=None, strict=False))
            assert rc == 2, f"件不存在应 rc=2，实为 {rc}"
        cases.append(("T9 目标件不存在 ⇒ rc=2", run(t9)))

        # T10 显式 --docs 无效 ⇒ rc=2（不回落）
        def t10():
            tgt = tmp / "claim5.md"
            tgt.write_text("正文。\n", encoding="utf-8")
            rc = cmd_claims(argparse.Namespace(file=str(tgt), docs=str(tmp / "nowhere"), strict=False))
            assert rc == 2, f"无效 --docs 应 rc=2，实为 {rc}"
        cases.append(("T10 无效 --docs ⇒ rc=2（不回落）", run(t10)))

    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    bad = [n for n, (okk, _) in cases if not okk]
    for n, (okk, msg) in cases:
        print(f"  {'✓' if okk else '✗'} {n}" + (f" —— {msg}" if msg else ""))
    print(f"\nself-test: {len(cases) - len(bad)}/{len(cases)}")
    return 0 if not bad else 1


def main() -> int:
    ap = argparse.ArgumentParser(description="改后自核（P6）：claims/sync/quotes/asserts 四支")
    ap.add_argument("--self-test", action="store_true", dest="self_test")
    sub = ap.add_subparsers(dest="cmd")
    for name, helptext in (("claims", "自证句复核"), ("sync", "版本号↔标题同步核"),
                           ("quotes", "新写行引号体例核"), ("asserts", "断言可核化三查（坐标/量词/自造术语）")):
        p = sub.add_parser(name, help=helptext)
        p.add_argument("--file", required=True)
        p.add_argument("--docs")
        if name in ("claims", "asserts"):
            p.add_argument("--strict", action="store_true")
        if name == "asserts":
            p.add_argument("--lines", nargs=2, type=int, metavar=("A", "B"))
            p.add_argument("--root", action="append", default=[],
                           help="引用解析根（可重复）；根给少了会**假红**")
        if name == "quotes":
            p.add_argument("--lines", nargs=2, type=int, metavar=("A", "B"))
            p.add_argument("--root", action="append", default=[],
                           help="引用解析根（可重复）；件内相对引用的根往往不止一个，缺根会假报")
            p.add_argument("--force", action="store_true",
                           help="域外件强行跑（默认拒绝：非 PEC 树会出成百条假报）")

    args = ap.parse_args()
    if args.self_test:
        return self_test()
    if args.cmd == "claims":
        return cmd_claims(args)
    if args.cmd == "sync":
        return cmd_sync(args)
    if args.cmd == "quotes":
        return cmd_quotes(args)
    if args.cmd == "asserts":
        return cmd_asserts(args)
    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
