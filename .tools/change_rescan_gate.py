#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""change_rescan_gate.py —— 改动-回扫闸（P1–P5 的对策 · 2026-10-03 立 · 未经独立复验）

## 它治什么

「**改一处就交**」—— 同一事实／同一措辞在别处还活着，而只改了被点名的那一处。
2026-10-02 PEC 语料补料三案场：**32 项自伤里 26 项**出自这个动作（路径清单 P1–P5）。
纪律层已被证无效（族 1 六次复发、六次靠外审逮出）⇒ 本件把「扫」做成**准入步**：
**改前先产清单，不过清单不许动手**；改后再跑一次做交付对账。

## 两个子命令

| 子命令 | 治 | 输入 |
|---|---|---|
| `anchors` | P1 姊妹件／P2 同件另一处／P3 同一措辞 | `--plan plan.json`（点名清单＋锚串＋已申报件） |
| `citer`   | P4 被改出处的引用未回扫／P5 插删行致行号漂移 | `--file <被引件>`（全仓谁在引它） |

## 边界（必读 · 不粉饰）

- **它是线索机，不是判据机**：锚串是**代理指标**（`G-X211`）—— 命中 ≠ 同一结论，
  不命中 ≠ 不存在。**「同义型」（换措辞的同一结论）它搜不到** ⇒ 人读那一步不能省。
- **默认排除备份件**（`.bak*` · `_bak/` · `_DEPRECATED_*` · `archived/` · `__pycache__` · `.skill`）。
  排除规则**与被排除的量都打印**（族 4：静默收窄面 ＝ 制造盲面）；`--no-exclude` 看原面。
- **`citer` 的「弱归属」是猜测**：同件内裸 `:NNN` 是否指向该被引件，本件只能按「同行是否出现该件名」
  或「该件是全文前置件名」弱判 —— 判定归人。
- **它拦不住 Edit**（Edit 不过 shell）⇒ 纪律与它必须并存，不可只靠其一。
- **登记射程 `fixed`（2026-10-03 加）**：**不读取快照或 diff**，`declared`／`fixed` 均只是名单登记，**不证明实际修改**（历史字段 `unfixed` 表示命中未被登记覆盖）。每条 claim 可给
  `fixed`（元素为 `path`＝件级，或 `path:line`＝位点级）。**命中落在 `declared` 但未被 `fixed` 覆盖 ⇒ 判红
  「已申报未修」**。**无 `fixed` 字段 ⇒ 旧行为，但会打印「位点级校验未启用」——不得静默降级。**
  - **优先级写死**：`allow`（件级／位点级）> `fixed` > `declared` > 未申报。**`allow` 有两档**：
    件级 `{"file":…}` ／ **位点级 `{"file":…,"line":N}` 或锚串级 `{"file":…,"anchor":"串"}`（后者豁免该文件中该锚串的**全部**命中，不是唯一位点）** —— 后者是为
    `declared` 件内**必然存在**的「历史留痕落点」（修订记录 · dated 追记）留的：它们**该留**，
    但件级豁免会把整件连同未修的活文一并放过 ⇒ **必须能只豁免一处并写明理由**（打印区分「已豁免·件级／已豁免·位点」）。
  - **件级放行必须报量**：`fixed` 只给裸 `path` 时，该件全部命中按「件」放行，**放行数与「降级」字样都会打印**
    （族 4：加档位规则必须把规则与**被放行的量**一起报出来）。
  - **幻影位点**：`fixed` 列了而**无任何锚串命中**的位点会单列（**这正是行号漂移的探针** —— 本仓实测漂过）。
  - **使用边界**：准入步登记**拟改**射程；交付步须**先对账实际 diff 再登记结果**。字段本身不完成该核验。
  - **⚠ `path:line` 形式每次跑前须重取行号**（行号会漂 —— 本仓实测：同一 plan 在几十分钟内其位点即失配）。
    粗粒度可写裸 `path`，但那会触发「**件级放行报量 ＋ 降级**」提示。**本闸自身的 plan 也吃这条。**
- **⚠ plan 与复核类文档不得落在扫根内（2026-10-03 Doctor 裁「移出扫根」）**：本闸**不排除自身 plan** ⇒
  plan 落在扫根内时，闸无法把 plan 自身与目标面区分，未申报命中**（除把 plan 自身写进 `declared`／`allow`
  外）恒 > 0**；修法是**显式给 `--root`** 把它划出去，**不是给闸打排除补丁**（排除规则会制造盲面，族 4）。
  **被移出扫根的面须在清单里写明**（本仓为 `brain/logs/**`）。

## 用法

    python3 change_rescan_gate.py anchors --plan plan.json [--docs DIR] [--root DIR ...] \\
                                          [--json OUT] [--no-exclude] [--context 0]
    python3 change_rescan_gate.py citer  --file <相对 docs 的路径> [--docs DIR] [--root DIR ...]
    python3 change_rescan_gate.py --self-test

## 退出码

    0 = 全部命中已申报（或列入 allow）   1 = 存在未申报命中
    2 = 环境不可用（docs 根不可达／计划件读不了／plan 缺必填字段）—— fail-closed，不静默通过
"""
from __future__ import annotations

import argparse
import json
import os
import pathlib
import re
import shutil
import sys
import tempfile

try:
    import yaml  # 可选：plan 也吃 JSON
except ImportError:  # pragma: no cover
    yaml = None

HERE = pathlib.Path(__file__).resolve().parent
EXCLUDE_RE = re.compile(r"(^|/)(_bak|archived|__pycache__)($|/)|\.bak|_DEPRECATED_|\.skill$")
DEFAULT_ROOTS = ["brain", "Projects/PEC"]
CITE_LINE = re.compile(r"(?P<path>[\w一-鿿./\-]+?\.(?:md|json|py|txt|yaml|yml)):(?P<n>\d+)")
BARE_LINE = re.compile(r"(?<![\w./-]):(?P<n>\d+)\b")
TEXT_EXT = {".md", ".txt", ".json", ".py", ".yaml", ".yml"}


# ────────────────────────────── 基础设施 ──────────────────────────────

def find_docs_root(explicit: str | None) -> pathlib.Path | None:
    """docs 根 = 含 brain/ 的那一层。沙箱内 `~/Documents` 会解析错（少 mnt/ 段）⇒ 显式传 --docs。

    ⚠ **显式值具权威性**（2026-10-03 由本件 self-test T8 逮出的缺陷改正）：`--docs` 一旦给出即**只认它**，
    无效则返回 None（调用方 rc=2）。**原实现会静默回落到脚本自身推的根** —— 实测把 self-test 跑到了
    真仓 1660 件上（一条指向不存在目录的用例，结果扫了整个 brain 树）。**静默回落＝假根不报错。**
    """
    if explicit:
        c = pathlib.Path(explicit).expanduser()
        try:
            return c.resolve() if (c / "brain").is_dir() else None
        except OSError:
            return None
    if os.environ.get("DOCS_DIR"):
        c = pathlib.Path(os.environ["DOCS_DIR"]).expanduser()
        try:
            if (c / "brain").is_dir():
                return c.resolve()
        except OSError:
            pass
    for c in (HERE.parent.parent, HERE.parent.parent.parent):      # brain/.tools → Claude → Documents
        try:
            if (c / "brain").is_dir():
                return c.resolve()
        except OSError:
            continue
    return None


def iter_files(roots: list[pathlib.Path], exts: set[str], exclude: bool):
    """返回 (文件表, 按扩展名排除数, 按备份规则排除数)。

    ⚠ **两类排除必须分别计数**（2026-10-03 由本件 self-test T2/T3 逮出的缺陷改正）：原实现先按后缀过滤、
    再判备份规则，于是形如 `x.md.bak_2026` 的件**被后缀过滤吃掉且不计入任何排除数** ——
    「扫描面 N 件」因此虚高、被吞掉的量看不见。**这正是族 4 的「静默收窄面＝制造盲面」。**
    逐件判定，不剪枝整目录 —— 剪枝会静默吞掉整片。
    """
    kept, skip_ext, skip_pat = [], 0, 0
    for r in roots:
        if not r.exists():
            continue
        for p in sorted(r.rglob("*")):
            if not p.is_file():
                continue
            if p.suffix.lower() not in exts:
                skip_ext += 1
                continue
            if exclude and EXCLUDE_RE.search(p.as_posix()):
                skip_pat += 1
                continue
            kept.append(p)
    return kept, skip_ext, skip_pat


def read_lines(p: pathlib.Path):
    try:
        return p.read_text(encoding="utf-8", errors="replace").split("\n")
    except OSError:
        return None


def rel_to(p: pathlib.Path, docs: pathlib.Path) -> str:
    try:
        return p.resolve().relative_to(docs.resolve()).as_posix()
    except ValueError:
        return p.as_posix()


def load_plan(path: pathlib.Path):
    raw = path.read_text(encoding="utf-8")
    if path.suffix.lower() in (".yaml", ".yml"):
        if yaml is None:
            raise RuntimeError("plan 是 YAML 但环境无 PyYAML ⇒ 换 JSON 或 pip install pyyaml")
        return yaml.safe_load(raw)
    return json.loads(raw)


# ────────────────────────────── anchors ──────────────────────────────

def cmd_anchors(args) -> int:
    docs = find_docs_root(args.docs)
    if docs is None:
        print("✗ docs 根不可达（须含 brain/）⇒ 显式传 --docs", file=sys.stderr)
        return 2
    plan_p = pathlib.Path(args.plan).expanduser()
    if not plan_p.exists():
        print(f"✗ 计划件不存在：{plan_p}", file=sys.stderr)
        return 2
    try:
        plan = load_plan(plan_p)
    except Exception as e:                                    # noqa: BLE001
        print(f"✗ 计划件解析失败：{e}", file=sys.stderr)
        return 2
    claims = (plan or {}).get("claims")
    if not isinstance(claims, list) or not claims:
        print("✗ 计划件缺 claims（须为非空列表）", file=sys.stderr)
        return 2

    roots = [docs / r for r in (args.root or plan.get("roots") or DEFAULT_ROOTS)]
    files, skip_ext, skip_pat = iter_files(roots, set(args.ext or TEXT_EXT), not args.no_exclude)
    print(f"# 改动-回扫闸 · batch = {plan.get('batch', '(未命名)')}")
    print(f"# 扫描根：{[rel_to(r, docs) for r in roots]}")
    print(f"# 扫描面：{len(files)} 件 · 排除 {skip_pat} 件（规则：.bak* / _bak/ / _DEPRECATED_* / "
          f"archived/ / __pycache__ / *.skill）"
          + ("" if args.no_exclude else " · 备份规则生效")
          + f" · 另 {skip_ext} 件非目标扩展名")
    if args.no_exclude:
        print("# ⚠ --no-exclude：备份规则未生效，命中面含 .bak/_bak 等备份件（只作对照，不作判据）")
    print()

    corpus = []
    for f in files:
        lines = read_lines(f)
        if lines is not None:
            corpus.append((f, lines, rel_to(f, docs)))

    summary, red_un_total, red_unfixed_total = [], 0, 0
    for ci, claim in enumerate(claims, 1):
        cid = claim.get("id") or f"C{ci}"
        anchors = claim.get("anchors") or []
        if not anchors:
            print(f"✗ {cid} 缺 anchors", file=sys.stderr)
            return 2
        declared = {str(x) for x in (claim.get("declared") or [])}
        # ── allow 两档（2026-10-03 加位点级）：件级 `{"file":…}` ／ 位点级 `{"file":…,"line":N}` 或 `{"file":…,"anchor":"串"}`
        #    为什么要有位点级：`declared` 件内**必然**存在「历史留痕落点」（修订记录 · dated 追记）—— 那是**该留**的，
        #    但件级 allow 会把整件一并豁免、把位点级校验掏空。故必须能「只豁免这一处、并写明理由」。
        allow_all, allow_occ = {}, []
        for a in (claim.get("allow") or []):
            f = str(a.get("file"))
            if a.get("line") is not None or a.get("anchor"):
                allow_occ.append((f, a.get("line"), str(a.get("anchor") or ""), a.get("reason", "")))
            else:
                allow_all[f] = a.get("reason", "")
        # ── 登记射程 fixed（2026-10-03 加）：`path`（件级）或 `path:line`（位点级）
        #    ⚠ 仅名单登记，不读取快照/diff：准入步登记拟改射程，交付步须先对账实际 diff 再登记结果。
        raw_fixed = claim.get("fixed")
        fixed_on = isinstance(raw_fixed, list) and len(raw_fixed) > 0
        fixed_files, fixed_pts = set(), set()
        for x in (raw_fixed or []):
            head, _, tail = str(x).rpartition(":")
            (fixed_pts if (head and tail.isdigit()) else fixed_files).add(str(x))
        print(f"── {cid} · {claim.get('text', '')} " + "─" * max(0, 40 - len(str(claim.get('text', '')))))
        print("   # 登记射程 fixed = " + (f"位点 {sorted(fixed_pts)} · 件级 {sorted(fixed_files)}"
                                            if fixed_on else "（未给）"))
        undeclared, allowed, declared_hits, fixed_hits, unfixed, total = [], [], [], [], [], 0
        blanket_hits, all_pts = 0, set()
        for anchor in anchors:
            hits = []
            for f, lines, rel in corpus:
                for i, line in enumerate(lines, 1):
                    if anchor in line:
                        hits.append((rel, i, line.strip()))
            total += len(hits)
            print(f"   锚串「{anchor}」：命中 {len(hits)} 处" if hits else f"   锚串「{anchor}」：命中 0 处")
            for rel, i, text in hits:
                all_pts.add(f"{rel}:{i}")
                # 优先级**写死**：allow > fixed > declared > 未申报（2026-10-03 · 修前审 R5）
                #   allow 优先，否则「已豁免命中被判红」会与 allow 的语义直接对撞。
                if rel in allow_all:
                    allowed.append((rel, i, anchor))
                    print(f"     ~ 已豁免·件级  {rel}:{i}  （理由：{allow_all[rel]}）")
                elif any(rel == f and ((ln is not None and ln == i) or (anc and anc == anchor))
                         for (f, ln, anc, _r) in allow_occ):
                    _r = next(r for (f, ln, anc, r) in allow_occ
                              if rel == f and ((ln is not None and ln == i) or (anc and anc == anchor)))
                    allowed.append((rel, i, anchor))
                    print(f"     ~ 已豁免·位点  {rel}:{i}  （理由：{_r}）")
                elif fixed_on and (f"{rel}:{i}" in fixed_pts or rel in fixed_files):
                    fixed_hits.append((rel, i, anchor))
                    if rel in fixed_files and f"{rel}:{i}" not in fixed_pts:
                        blanket_hits += 1
                    print(f"     ~ 登记为 fixed（未核差异） {rel}:{i}")
                elif fixed_on and rel in declared:
                    unfixed.append((rel, i, anchor))
                    print(f"     ✗ 已申报未修  {rel}:{i}   ← 件在 declared 内，但这一处未列入 fixed")
                elif rel in declared:
                    declared_hits.append((rel, i, anchor))
                    print(f"     ✓ 已申报  {rel}:{i}")
                else:
                    undeclared.append((rel, i, anchor))
                    print(f"     ✗ 未申报  {rel}:{i}")
                if args.context:
                    print(f"       > {text[:200]}")
        ghost = sorted(x for x in fixed_pts if x not in all_pts)
        red_un_total += len(undeclared)
        red_unfixed_total += len(unfixed)
        print(f"   ⇒ 未申报命中 {len(undeclared)} 处 · 已申报未修命中 {len(unfixed)} 处"
              f"（declared 内、未被 fixed 覆盖）")
        if fixed_on:
            print(f"      · 件级放行 {blanket_hits} 处（fixed 只给 path、未给 path:line）")
            print(f"      · fixed 幻影位点 {len(ghost)} 处（fixed 列了、但无任何锚串命中）")
            for g in ghost:
                print(f"        · {g}")
            if blanket_hits:
                print(f"   ⚠ 位点级校验降级（本 claim 的 fixed 含裸 path：{'、'.join(sorted(fixed_files))}）"
                      f"—— 该件 {blanket_hits} 处命中按「件」放行。")
        else:
            print("   ⚠ 位点级校验未启用（本 claim 无 fixed）—— declared 只是名单登记：只到「件」粒度，"
                  "**不证明该件动过，也不证明任一处改到**。")
        print()
        summary.append({"id": cid, "anchors": anchors, "total_hits": total,
                        "declared": declared_hits, "allowed": allowed, "undeclared": undeclared,
                        "fixed": fixed_hits, "unfixed": unfixed,
                        "blanket_total": blanket_hits, "ghost_fixed": ghost, "fixed_on": fixed_on})

    print("=" * 62)
    red_total = red_un_total + red_unfixed_total
    print(f"合计：未申报命中 {red_un_total} 处 · 已申报未修命中 {red_unfixed_total} 处 ⇒ 红合计 {red_total}")
    print("判据：红合计 == 0 ⇒ 过；> 0 ⇒ 逐处处置后再动手（改前准入步），或改后同批补改。")
    print("⚠ 提示：锚串是代理指标（G-X211）—— 同义型搜不到，人读不可省。")
    print("⚠ `fixed` 仅登记射程，未读取快照/diff；交付时实际修改须另行对账。")
    if args.json:
        pathlib.Path(args.json).write_text(
            json.dumps({"batch": plan.get("batch"), "claims": summary,
                        "undeclared_total": red_un_total,
                        "unfixed_total": red_unfixed_total,
                        "red_total": red_total}, ensure_ascii=False, indent=2),
            encoding="utf-8")
        print(f"（机读结果已写 {args.json}）")
    return 1 if red_total else 0


# ────────────────────────────── citer ──────────────────────────────

def cmd_citer(args) -> int:
    docs = find_docs_root(args.docs)
    if docs is None:
        print("✗ docs 根不可达（须含 brain/）⇒ 显式传 --docs", file=sys.stderr)
        return 2
    target = pathlib.Path(args.file)
    if not target.is_absolute():
        target = docs / args.file
    if not target.exists():
        print(f"✗ 被引件不存在：{target}", file=sys.stderr)
        return 2
    name = target.name
    roots = [docs / r for r in (args.root or DEFAULT_ROOTS)]
    files, skip_ext, skip_pat = iter_files(roots, set(args.ext or TEXT_EXT), not args.no_exclude)
    print(f"# 引用方扫描 · 被引件 = {rel_to(target, docs)}")
    print(f"# 扫描面：{len(files)} 件 · 排除 {skip_pat} 件（同 anchors 规则） · 另 {skip_ext} 件非目标扩展名")
    strong, weak = [], []
    for f in files:
        if f.resolve() == target.resolve():
            continue
        lines = read_lines(f)
        if lines is None:
            continue
        rel = rel_to(f, docs)
        for i, line in enumerate(lines, 1):
            if name in line:
                for m in CITE_LINE.finditer(line):
                    if m.group("path").endswith(name):
                        strong.append((rel, i, f"{m.group('path')}:{m.group('n')}"))
                for m in BARE_LINE.finditer(line):
                    weak.append((rel, i, m.group("n")))
    print(f"\n■ 强引用（带文件名）· {len(strong)} 处 —— 该件插行／删行后**全部**须重扫")
    for rel, i, ref in strong:
        print(f"   {rel}:{i}  引 → {ref}")
    print(f"\n■ 弱归属（同件内裸 `:NNN`，且该行出现件名）· {len(weak)} 处 —— 归属需人判")
    for rel, i, n in weak:
        print(f"   {rel}:{i}  `:{n}`")
    print("\n判据：被引件若发生**插行／删行**，强引用必须逐处重扫（P5）；头部插行属高危形态，禁。")
    return 0


# ────────────────────────────── self-test ──────────────────────────────

def self_test() -> int:
    cases = []

    def run(fn):
        """跑一例：**吞掉该例 stdout**（成功即静默），失败时把捕获内容一并打出。

        ⚠ 必须捕获：T14/T15 要断言的是**打印出来的提示**（「位点级校验未启用／降级／件级放行／幻影位点」），
        不捕获就只能断言 rc，那会把这两例退化成**假齿**（2026-10-03 修前审指出的实现坑）。
        """
        import contextlib
        import io
        buf = io.StringIO()
        try:
            with contextlib.redirect_stdout(buf):
                fn()
            return True, ""
        except AssertionError as e:
            return False, f"{e}\n     ↓ 该例捕获输出 ↓\n" + "\n".join(
                "     " + ln for ln in buf.getvalue().rstrip().split("\n"))

    tmp = pathlib.Path(tempfile.mkdtemp(prefix="crg_selftest_"))
    try:
        docs = tmp / "docs"
        (docs / "brain" / "sub").mkdir(parents=True)
        (docs / "Projects" / "PEC").mkdir(parents=True)
        (docs / "brain" / "a.md").write_text("正文提到「四套」口径。\n另一行。\n", encoding="utf-8")
        (docs / "brain" / "sub" / "b.md").write_text("这里也写「四套」。\n", encoding="utf-8")
        (docs / "Projects" / "PEC" / "c.md").write_text("无关。\n", encoding="utf-8")
        (docs / "brain" / "backup.md.bak_2026").write_text("「四套」\n", encoding="utf-8")
        (docs / "brain" / "_bak").mkdir()
        (docs / "brain" / "_bak" / "old.md").write_text("「四套」\n", encoding="utf-8")

        # T1 docs 根定位
        def t1():
            r = find_docs_root(str(docs))
            assert r is not None and (r / "brain").is_dir(), "docs 根定位失败"
        cases.append(("T1 docs 根定位", run(t1)))

        # T2 排除规则生效且**两类分别计数**
        def t2():
            kept, skip_ext, skip_pat = iter_files([docs / "brain"], {".md"}, True)
            assert skip_pat == 1, f"备份规则应排除 1（_bak/old.md），实为 {skip_pat}"
            assert skip_ext == 1, f"形如 x.md.bak_2026 的件须计入排除数（原缺陷＝被静默吃掉），实为 {skip_ext}"
            assert len(kept) == 2, f"应留 2，实为 {len(kept)}"
        cases.append(("T2 两类排除分别计数", run(t2)))

        # T3 --no-exclude 放宽备份规则
        def t3():
            kept, skip_ext, skip_pat = iter_files([docs / "brain"], {".md"}, False)
            assert skip_pat == 0, f"不排除时备份规则计数应 0，实为 {skip_pat}"
            assert len(kept) == 3, f"原面应 3，实为 {len(kept)}"
        cases.append(("T3 --no-exclude 放宽备份规则", run(t3)))

        # T3b 已知残留（明写，不粉饰）：扩展名过滤不吃 --no-exclude
        def t3b():
            kept, skip_ext, _ = iter_files([docs / "brain"], {".md", ".bak_2026"}, False)
            assert len(kept) == 4, f"补 --ext .bak_2026 后应能看到该件（应 4，实为 {len(kept)})"
        cases.append(("T3b 备份件须 --ext 才能入面（已知残留）", run(t3b)))

        # T4 anchors：未申报命中 ⇒ rc=1
        planf = docs / "plan.json"
        planf.write_text(json.dumps({
            "batch": "selftest", "roots": ["brain"],
            "claims": [{"id": "C1", "text": "四套口径", "anchors": ["四套"],
                        "declared": ["brain/a.md"]}]
        }, ensure_ascii=False), encoding="utf-8")

        def t4():
            rc = cmd_anchors(argparse.Namespace(plan=str(planf), docs=str(docs), root=None,
                                                ext=None, no_exclude=False, context=0, json=None))
            assert rc == 1, f"未申报命中应 rc=1，实为 {rc}"
        cases.append(("T4 anchors 未申报 ⇒ 红", run(t4)))

        # T5 全申报 ⇒ rc=0
        planf2 = docs / "plan2.json"
        planf2.write_text(json.dumps({
            "batch": "selftest2", "roots": ["brain"],
            "claims": [{"id": "C1", "text": "四套口径", "anchors": ["四套"],
                        "declared": ["brain/a.md", "brain/sub/b.md"]}]
        }, ensure_ascii=False), encoding="utf-8")

        def t5():
            rc = cmd_anchors(argparse.Namespace(plan=str(planf2), docs=str(docs), root=None,
                                                ext=None, no_exclude=False, context=0, json=None))
            assert rc == 0, f"全申报应 rc=0，实为 {rc}"
        cases.append(("T5 anchors 全申报 ⇒ 绿", run(t5)))

        # T6 allow 豁免生效
        planf3 = docs / "plan3.json"
        planf3.write_text(json.dumps({
            "batch": "selftest3", "roots": ["brain", "Projects/PEC"],
            "claims": [{"id": "C1", "text": "四套口径", "anchors": ["四套"],
                        "declared": ["brain/a.md"],
                        "allow": [{"file": "brain/sub/b.md", "reason": "资料层原文·已挂指针"}]}]
        }, ensure_ascii=False), encoding="utf-8")

        def t6():
            rc = cmd_anchors(argparse.Namespace(plan=str(planf3), docs=str(docs), root=None,
                                                ext=None, no_exclude=False, context=0, json=None))
            assert rc == 0, f"allow 后应 rc=0，实为 {rc}"
        cases.append(("T6 allow 豁免 ⇒ 绿", run(t6)))

        # T7 plan 缺 claims ⇒ rc=2（fail-closed）
        planf4 = docs / "plan4.json"
        planf4.write_text(json.dumps({"batch": "bad"}), encoding="utf-8")

        def t7():
            rc = cmd_anchors(argparse.Namespace(plan=str(planf4), docs=str(docs), root=None,
                                                ext=None, no_exclude=False, context=0, json=None))
            assert rc == 2, f"缺 claims 应 rc=2，实为 {rc}"
        cases.append(("T7 缺 claims ⇒ rc=2", run(t7)))

        # T8 显式 --docs 根不可达 ⇒ rc=2（**不得静默回落到脚本自身推的根**）
        def t8():
            rc = cmd_anchors(argparse.Namespace(plan=str(planf), docs=str(tmp / "nowhere"),
                                                root=None, ext=None, no_exclude=False,
                                                context=0, json=None))
            assert rc == 2, f"根不可达应 rc=2，实为 {rc}"
        cases.append(("T8 显式根不可达 ⇒ rc=2（不回落默认根）", run(t8)))

        # T9 citer：强引用与弱归属分列
        cited = docs / "brain" / "a.md"

        def t9():
            (docs / "brain" / "ref.md").write_text(
                "见 `a.md:2` 与裸 :2 的写法。\n", encoding="utf-8")
            import io
            import contextlib
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                rc = cmd_citer(argparse.Namespace(file=str(cited), docs=str(docs), root=["brain"],
                                                 ext=None, no_exclude=False))
            out = buf.getvalue()
            assert rc == 0, f"citer 应 rc=0，实为 {rc}"
            assert "a.md:2" in out, "未报出强引用"
            assert "弱归属" in out, "未分列弱归属"
        cases.append(("T9 citer 强/弱分列", run(t9)))

        # T10 自引件不进引用方（避免把被引件自己算成引用方）
        def t10():
            import io
            import contextlib
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                cmd_citer(argparse.Namespace(file=str(cited), docs=str(docs), root=["brain"],
                                             ext=None, no_exclude=False))
            out = buf.getvalue()
            body = out.split("■ 强引用")[1] if "■ 强引用" in out else ""
            assert "brain/a.md:2   引 →" not in body, "被引件自己被当成引用方"
        cases.append(("T10 自引件不入引用方", run(t10)))

        # ── 位点级 fixed 四例（2026-10-03 加 · 治族 1「件在 declared 里 ≠ 这处改到」）
        def _run_plan(planobj, tag):
            import contextlib
            import io
            planf = docs / f"plan_{tag}.json"
            planf.write_text(json.dumps(planobj, ensure_ascii=False), encoding="utf-8")
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                rc = cmd_anchors(argparse.Namespace(plan=str(planf), docs=str(docs), root=None,
                                                    ext=None, no_exclude=False, context=0, json=None))
            return rc, buf.getvalue()

        def t12():
            rc, out = _run_plan({"batch": "t12", "roots": ["brain"],
                                 "claims": [{"id": "C1", "anchors": ["四套"],
                                             "declared": ["brain/a.md", "brain/sub/b.md"],
                                             "fixed": ["brain/a.md:1"]}]}, "t12")
            assert rc == 1, f"declared 内有一处未修应判红，实为 rc={rc}"
            assert "已申报未修" in out, "未报出「已申报未修」"
        cases.append(("T12 位点级：declared 内未修 ⇒ 红", run(t12)))

        def t13():
            rc, _ = _run_plan({"batch": "t13", "roots": ["brain"],
                               "claims": [{"id": "C1", "anchors": ["四套"],
                                           "declared": ["brain/a.md", "brain/sub/b.md"],
                                           "fixed": ["brain/a.md:1", "brain/sub/b.md:1"]}]}, "t13")
            assert rc == 0, f"位点全覆盖应 rc=0，实为 {rc}"
        cases.append(("T13 位点级：全覆盖 ⇒ 绿", run(t13)))

        def t14():
            rc, out = _run_plan({"batch": "t14", "roots": ["brain"],
                                 "claims": [{"id": "C1", "anchors": ["四套"],
                                             "declared": ["brain/a.md", "brain/sub/b.md"]}]}, "t14")
            assert rc == 0, f"无 fixed 的旧行为应 rc=0，实为 {rc}"
            assert "位点级校验未启用" in out, "无 fixed 时未打印提示（＝静默降级）"
        cases.append(("T14 无 fixed ⇒ 旧行为＋打印未启用", run(t14)))

        def t15():
            rc, out = _run_plan({"batch": "t15", "roots": ["brain"],
                                 "claims": [{"id": "C1", "anchors": ["四套"],
                                             "declared": ["brain/a.md", "brain/sub/b.md"],
                                             "fixed": ["brain/a.md", "brain/sub/b.md:99"]}]}, "t15")
            assert "件级放行" in out and "降级" in out, "件级放行未报量或未标降级"
            assert "幻影位点" in out and "brain/sub/b.md:99" in out, "幻影位点未报出"
            assert rc == 1, f"b.md:1 未修应判红，实为 rc={rc}"
        cases.append(("T15 件级放行报量 ＋ 幻影位点", run(t15)))

        # T16 位点级 allow：历史留痕落点须能「只豁免这一处」
        def t16():
            rc, out = _run_plan({"batch": "t16", "roots": ["brain"],
                                 "claims": [{"id": "C1", "anchors": ["四套"],
                                             "declared": ["brain/a.md", "brain/sub/b.md"],
                                             "fixed": ["brain/a.md:1"],
                                             "allow": [{"file": "brain/sub/b.md", "anchor": "四套",
                                                        "reason": "历史留痕落点（该留不改）"}]}]}, "t16")
            assert rc == 0, f"位点级 allow 后应 rc=0，实为 {rc}"
            assert "已豁免·位点" in out, "未打印位点级豁免（会让人以为被件级兜底）"
            # ⚠ 判据必须带 `✗ ` 前缀：「已申报未修」五字也出现在**恒印的汇总行**里（首跑踩过 ⇒ 假红断言）
            assert "✗ 已申报未修" not in out, "位点级 allow 未生效，仍判了已申报未修"
        cases.append(("T16 位点级 allow：只豁免一处", run(t16)))

    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    bad = [n for n, (okk, _) in cases if not okk]
    for n, (okk, msg) in cases:
        print(f"  {'✓' if okk else '✗'} {n}" + (f" —— {msg}" if msg else ""))
    print(f"\nself-test: {len(cases) - len(bad)}/{len(cases)}")
    return 0 if not bad else 1


# ────────────────────────────── main ──────────────────────────────

def main() -> int:
    ap = argparse.ArgumentParser(description="改动-回扫闸（P1–P5）")
    ap.add_argument("--self-test", action="store_true", dest="self_test")
    sub = ap.add_subparsers(dest="cmd")

    def common(p):
        p.add_argument("--docs", help="docs 根（含 brain/）；沙箱内必传")
        p.add_argument("--root", action="append", help="扫描根（相对 docs），可重复")
        p.add_argument("--ext", action="append", help="参与扫描的扩展名，可重复")
        p.add_argument("--no-exclude", action="store_true", dest="no_exclude")

    pa = sub.add_parser("anchors", help="锚串全仓在场扫描（P1–P3）")
    common(pa)
    pa.add_argument("--plan", required=True, help="点名清单（JSON/YAML）")
    pa.add_argument("--json", help="机读结果落点")
    pa.add_argument("--context", type=int, default=0, help="≥1 时打印命中行全文")

    pc = sub.add_parser("citer", help="全仓谁在引这个被引件（P4–P5）")
    common(pc)
    pc.add_argument("--file", required=True, help="被引件（相对 docs 或绝对路径）")

    args = ap.parse_args()
    if args.self_test:
        return self_test()
    if args.cmd == "anchors":
        return cmd_anchors(args)
    if args.cmd == "citer":
        return cmd_citer(args)
    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
