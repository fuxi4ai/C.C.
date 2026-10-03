#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""strip_visibility_guard.py —— 剥离可见性对拍（P0「修红反噬」的对策 · 2026-10-03 立 · 未经独立复验）

## 它治什么

**为了让闸变绿而去改被测对象**，改掉了闸赖以识别的特征 ⇒ 闸从此看不见那一片。
本库实证（2026-10-02 PEC 语料补料三案场·第七轮外审逮出）：为过 `check_quote_binding.py` 的 A 项，
批量剥离 **221 处**非引录引号，**连带把 8 处本该带角括号的真引录也剥了** ⇒ 该工具（A 项只认 `「」`）
**从此看不见它们**。后果不是「N 个错」，是**后续每一轮都漏检这一片**。

## 它怎么工作（一句话）

    snap → 记下「可见引录数」；操作；chk → 再数一次。**数变少 ⇒ 判红。**

判据来源：**直接 import `check_quote_binding.QUOTE`**（生产谓词），不从本件重抄一份 ——
「自检把生产护栏的逻辑重抄一遍」正是族 4 的假齿形态（该库已有实例）。

## 边界（必读 · 不粉饰）

- **它只数「可见引录数」这一个量**：数不变 ≠ 没剥错（等量替换抓不到）；它治的是**批量剥离**这个形态。
- **它拦不住 Edit**（Edit 不过 shell）；它是**配对使用**的流程闸，不是自动拦截器。
- **豁免句（P0b「用文字给自己开豁免」）本件不覆盖** —— 那一支**无机械闸**，只有 skill 里的门禁（人读）。
  写在这里是为了不让人误以为跑完本件就万事大吉。
- `chk` 的**红**是机械的（数变少）；但「变少的那些是不是真引录」**归人判**：本件给出前后差与文件级明细，
  不代替 `check_quote_binding.py` 的 A 项判定。

## 用法

    python3 strip_visibility_guard.py snap --file <md> [--file ...] [--files-from list.txt] [--tag T]
    python3 strip_visibility_guard.py chk  --file <md> [--file ...] [--files-from list.txt] [--tag T]
    python3 strip_visibility_guard.py --self-test

    路径可用「相对当前工作目录 / 相对 --docs / 绝对路径」；`--docs` 语义与 change_rescan_gate.py 同
    （**显式给出即具权威性，无效则 rc=2，不回落默认根**）。

## 退出码

    0 = 无文件可见引录数下降     1 = 有下降（判红）
    2 = 环境不可用（缺 PyYAML / 导入不了 check_quote_binding / 快照缺失或半截 / 根不可达）—— fail-closed
"""
from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
SNAPDIR = pathlib.Path("/tmp/.strip_vis")


def _import_predicate():
    """生产谓词取自 check_quote_binding（A 项只认这个）。**不重抄**（族 4 假齿）。"""
    if str(HERE) not in sys.path:
        sys.path.insert(0, str(HERE))
    try:
        import check_quote_binding as cqb            # noqa: N813
    except Exception as e:                            # noqa: BLE001
        return None, f"导入 check_quote_binding 失败：{e}"
    q = getattr(cqb, "QUOTE", None)
    if q is None:
        return None, "check_quote_binding 无 QUOTE 常量（生产谓词被改名/移除）"
    return q, ""


def find_docs_root(explicit: str | None):
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


def resolve_files(paths, docs):
    out = []
    for raw in paths:
        p = pathlib.Path(raw)
        cands = [p] if p.is_absolute() else [pathlib.Path.cwd() / p]
        if docs is not None:
            cands.append(docs / p)
        hit = next((c for c in cands if c.exists() and c.is_file()), None)
        out.append(hit if hit is not None else p)
    return out


def read(p: pathlib.Path):
    try:
        return p.read_text(encoding="utf-8", errors="replace").split("\n")
    except OSError:
        return None


def measure(f, QUOTE):
    """可见引录数 = 「…」 成对出现次数（**生产谓词**）。"""
    if not f.exists():
        return None
    text = f.read_text(encoding="utf-8", errors="replace")
    return {
        "count": len(QUOTE.findall(text)),
        "unclosed": text.count("「") - text.count("」"),
        "bytes": len(text.encode("utf-8")),
        "sha": hashlib.sha256(text.encode("utf-8")).hexdigest()[:16],
    }


def cmd_snap(args) -> int:
    QUOTE, err = _import_predicate()
    if QUOTE is None:
        print(f"✗ {err}", file=sys.stderr)
        return 2
    docs = find_docs_root(args.docs)
    if args.docs and docs is None:
        print(f"✗ --docs 不可达（须含 brain/）：{args.docs}", file=sys.stderr)
        return 2
    files = resolve_files(args.files, docs)
    state, missing = {}, 0
    for f in files:
        m = measure(f, QUOTE)
        if m is None:
            print(f"   ✗ 取不到：{f}", file=sys.stderr)
            missing += 1
            continue
        state[f.as_posix()] = m
        print(f"   · {f}  可见引录 {m['count']} 处 · {m['bytes']} B · sha {m['sha']}")
    if missing:
        print(f"✗ {missing} 件取不到 ⇒ 不落快照（fail-closed，别拿半截快照当基线）", file=sys.stderr)
        return 2
    SNAPDIR.mkdir(parents=True, exist_ok=True)
    tag = args.tag or "default"
    (SNAPDIR / f"{tag}.json").write_text(
        json.dumps({"tag": tag, "files": state}, ensure_ascii=False, indent=2), encoding="utf-8")
    tot = sum(v["count"] for v in state.values())
    print(f"\n✓ 快照已落：{SNAPDIR / f'{tag}.json'} · {len(state)} 件 · 可见引录合计 {tot} 处")
    return 0


def cmd_chk(args) -> int:
    QUOTE, err = _import_predicate()
    if QUOTE is None:
        print(f"✗ {err}", file=sys.stderr)
        return 2
    tag = args.tag or "default"
    snap_p = SNAPDIR / f"{tag}.json"
    if not snap_p.exists():
        print(f"✗ 无快照 {snap_p} ⇒ 先 snap（absent ≠ 通过）", file=sys.stderr)
        return 2
    snap = json.loads(snap_p.read_text(encoding="utf-8"))["files"]
    docs = find_docs_root(args.docs)
    files = resolve_files(args.files, docs) if args.files else [pathlib.Path(k) for k in snap]
    red, rows, gone = [], [], []
    for f in files:
        key = f.as_posix()
        if key not in snap:
            gone.append(key)
            continue
        m = measure(f, QUOTE)
        if m is None:
            print(f"✗ 取不到：{f}", file=sys.stderr)
            return 2
        before = snap[key]["count"]
        delta = m["count"] - before
        rows.append((key, before, m["count"], delta))
        if delta < 0:
            red.append((key, before, m["count"], delta))
    print(f"# 剥离可见性对拍 · tag = {tag}")
    for key, b, a, d in rows:
        flag = "✗ 下降" if d < 0 else ("· 上升" if d > 0 else "✓ 不变")
        print(f"   {flag}  {key}   {b} → {a}  ({d:+d})")
    if gone:
        print(f"\n# ⚠ 快照里有而本次未列的件 {len(gone)} 件（未参与本次对拍，非通过）：")
        for g in gone:
            print(f"   · {g}")
    tb, ta = sum(r[1] for r in rows), sum(r[2] for r in rows)
    print(f"\n# 合计：{tb} → {ta}  ({ta - tb:+d})")
    if red:
        print(f"\n✗ 判红：{len(red)} 件的可见引录数下降 —— 很可能是把真引录一并剥了（P0 形态）。")
        print("  处置：逐件回读被剥掉的引录、补回「」并绑出处；**不许**以改对象为过闸手段。")
        print("  （数不变 ≠ 没剥错：等量替换本件抓不到。）")
        return 1
    print("\n✓ 无下降。⚠ 但「数不变」只排除批量剥离这一形态；A 项真伪仍归 check_quote_binding.py。")
    return 0


def cmd_residue(args) -> int:
    """裸引录残留嗅探 —— 抓「已经在盘上」的剥离残留（对拍抓不到的那一半）。

    ⚠ **本子命令是超出原设计（snap/chk 对拍）的扩改**（2026-10-03），理由：方案 §七 的回归判据要求
    本支报出已登记的 8 处盲区，而**对拍只能报「本次改少了」，报不出「上次改剩的」**。此处显式申报。

    **两个信号，都是提示（须人判）**：
      S1 · 裸文本与被引行大段重叠：该行有 `` `文件:行号` ``，但被引行上的长串（≥`--min` 字）
          在该行中**出现在「」之外** ⇒ 疑似**本该带角括号而没带**。
      S2 · 长 ASCII 双引号引文：A 项只认 `「」`，`"…"` 形式的长引文**工具看不见**（本库实证形态）。
    """
    QUOTE, err = _import_predicate()
    if QUOTE is None:
        print(f"✗ {err}", file=sys.stderr)
        return 2
    if str(HERE) not in sys.path:
        sys.path.insert(0, str(HERE))
    import check_quote_binding as cqb                        # noqa: N813
    import difflib

    target = pathlib.Path(args.file).expanduser()
    lines = read(target)
    if lines is None:
        print(f"✗ 读不了：{target}", file=sys.stderr)
        return 2
    docs = find_docs_root(args.docs)
    if args.docs and docs is None:
        print(f"✗ --docs 不可达（须含 brain/）：{args.docs}", file=sys.stderr)
        return 2
    roots = [str(target.parent), str(target.parent.parent)] + ([str(docs)] if docs else [])
    res = cqb.Resolver(roots)
    norm = lambda s: re.sub(r"[\s*|`>#]+", "", s)            # noqa: E731
    # frontmatter 区间：其内的 YAML 双引号标量**不是引文**，进 S2 就是纯假报（实测 11 处全为此）
    fm_end = 0
    if lines and lines[0].strip() == "---":
        for j, l in enumerate(lines[1:], 1):
            if l.strip() == "---":
                fm_end = j
                break
    s1, s1_filtered, s2 = [], [], []
    IDENT = re.compile(r"[A-Za-z0-9 .\-_/–—:()',&%°…]+$")     # 纯标识串：题名/书架号/URL/域名
    for i, line in enumerate(lines, 1):
        for m in cqb.CITE.finditer(line):
            rel, n = m.group(1), m.group(2)
            real, src = res.resolve(rel)
            if not (real and src and 1 <= int(n) <= len(src)):
                continue
            outside = norm(re.sub(r"`[^`]*`", "", QUOTE.sub("", line)))
            inside = norm(src[int(n) - 1])
            if not outside or not inside:
                continue
            blk = difflib.SequenceMatcher(None, outside, inside, autojunk=False).find_longest_match(
                0, len(outside), 0, len(inside))
            if blk.size < args.min:
                continue
            span = outside[blk.a:blk.a + blk.size]
            # 两档滤波（**被滤掉的量照报**，不静默）：
            #   ① 以冒号收尾的是「标签行」（如 `第4条（不经议会拨款征税违法）：`），不是引录
            #   ② 纯标识串（题名/书架号/URL）——实测 2026-10-03 该库此类占假阳性多数
            if span.rstrip().endswith(("：", ":")) or IDENT.fullmatch(span.replace(" ", "")):
                s1_filtered.append((i, rel, n, blk.size, span))
                continue
            s1.append((i, rel, n, blk.size, span))
        # S2 只在该行**确有出处**时才看 —— 引文脱离出处的长双引号串才是病；否则是散文／YAML
        if i <= fm_end or not (cqb.CITE.search(line) or cqb.BARE.search(line)):
            continue
        for mm in re.finditer(r'"([^"\n]{%d,})"' % args.min, line):
            s2.append((i, mm.group(1)[:70]))
    print(f"# 裸引录残留嗅探 · {target.name} · 阈值 ≥{args.min} 字")
    print(f"# 引用解析根：{roots}"
          + (f" · 已跳过 frontmatter（1–{fm_end} 行，其内 YAML 双引号不计）" if fm_end else ""))
    print(f"\n■ S1 · 与被引行大段重叠而出在「」之外 · {len(s1)} 处")
    for i, rel, n, size, span in s1:
        print(f"   ? L{i}  ← `{rel}:{n}`  重叠 {size} 字：{span[:60]}")
    print(f"\n■ S2 · 长 ASCII 双引号引文（工具盲区形态）· {len(s2)} 处")
    for i, txt in s2:
        print(f"   ? L{i}  \"{txt}…\"")
    if s1_filtered:
        print(f"\n□ 已滤除（标签行／纯标识串）· {len(s1_filtered)} 处 —— **量照报，不静默**")
        for i, rel, n, size, span in s1_filtered[:8]:
            print(f"   · L{i} 重叠 {size} 字：{span[:50]}")
        if len(s1_filtered) > 8:
            print(f"   · …另 {len(s1_filtered) - 8} 处")
    tot = len(s1) + len(s2)
    print(f"\n■ 未滤除命中 {tot} 处（S1 {len(s1)} + S2 {len(s2)}）")
    print("判据：本支是**提示器**（默认 rc=0）。--strict ⇒ 有命中即 rc=1。")
    print("⚠ **精度已知不足**：实测 2026-10-03 在 PEC 九件上，已登记的 8 处盲区全部报出，"
          "但同批亦报出若干『同一事实两处独立写法』。⇒ 逐处人判，**不得照单全改**（那正是族 9 假警报驱动）。")
    if args.strict and tot:
        return 1
    return 0


# ────────────────────────────── self-test ──────────────────────────────

def self_test() -> int:
    import shutil
    import tempfile

    cases = []

    def run(fn):
        """跑一例：**吞掉该例的 stdout**（成功即静默），失败时把捕获内容一并打出。"""
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

    QUOTE, err = _import_predicate()
    if QUOTE is None:
        print(f"✗ {err}—— self-test 无法进行（生产谓词不可得）", file=sys.stderr)
        return 2

    tmp = pathlib.Path(tempfile.mkdtemp(prefix="svg_selftest_"))
    try:
        # T1 生产谓词取自 check_quote_binding（非本件重抄）
        # ⚠ 判据用 **哨兵替换**，不用 `is` 比对象：`re.compile` 有内部缓存，同一 pattern 串
        #   会返回**同一实例** ⇒ 「自抄一份」也能骗过 `is` 判定。2026-10-03 变异实测（B2）当场逮出
        #   本用例原版是**假齿**（把谓词换成自抄的，rc 仍 0）⇒ 改为：把生产件的 QUOTE 换成哨兵，
        #   若函数返回哨兵，才证明确实**读的是生产件那一处**。
        def t1():
            import check_quote_binding as cqb
            sentinel = object()
            old = cqb.QUOTE
            try:
                cqb.QUOTE = sentinel
                q, e = _import_predicate()
                assert q is sentinel, f"谓词不是取自生产件当前值（＝重抄，假齿）: {e}"
            finally:
                cqb.QUOTE = old
        cases.append(("T1 谓词取自生产件（哨兵判据，抗 re 缓存）", run(t1)))

        # T2 谓词行为：只认「」成对
        def t2():
            assert len(QUOTE.findall("「甲」和「乙丙」")) == 2
            assert len(QUOTE.findall('"引" 与 「未闭合')) == 0
        cases.append(("T2 谓词只认「」成对", run(t2)))

        f = tmp / "a.md"
        tag = "selftest"

        # T3 snap 后不改 ⇒ 绿
        f.write_text("「甲甲」`x.md:1` 与「乙乙」。\n", encoding="utf-8")

        def t3():
            rc = cmd_snap(argparse.Namespace(files=[str(f)], files_from=None, docs=None, tag=tag))
            assert rc == 0, f"snap 应 rc=0，实为 {rc}"
            rc = cmd_chk(argparse.Namespace(files=[str(f)], files_from=None, docs=None, tag=tag))
            assert rc == 0, f"未改应 rc=0，实为 {rc}"
        cases.append(("T3 snap→未改 ⇒ 绿", run(t3)))

        # T4 剥掉一处「」（P0 形态）⇒ 红
        def t4():
            f.write_text("甲甲 `x.md:1` 与「乙乙」。\n", encoding="utf-8")
            rc = cmd_chk(argparse.Namespace(files=[str(f)], files_from=None, docs=None, tag=tag))
            assert rc == 1, f"剥掉一处应 rc=1，实为 {rc}"
        cases.append(("T4 剥掉引号 ⇒ 红", run(t4)))

        # T5 增引录 ⇒ 不红（上升不算 P0；真伪归 check_quote_binding）
        def t5():
            f.write_text("「甲甲」`x.md:1` 与「乙乙」和「丙丙」。\n", encoding="utf-8")
            rc = cmd_chk(argparse.Namespace(files=[str(f)], files_from=None, docs=None, tag=tag))
            assert rc == 0, f"上升不应判红，实为 {rc}"
        cases.append(("T5 上升不判红", run(t5)))

        # T6 等量替换的**已知盲区** —— 明写进用例，不粉饰
        def t6():
            g = tmp / "eq.md"
            g.write_text("「甲甲」`x.md:1`\n", encoding="utf-8")
            rc = cmd_snap(argparse.Namespace(files=[str(g)], files_from=None, docs=None, tag="eq"))
            assert rc == 0, f"snap 应 rc=0，实为 {rc}"
            g.write_text("「乙乙」`x.md:1`\n", encoding="utf-8")     # 数不变、内容被换
            rc = cmd_chk(argparse.Namespace(files=[str(g)], files_from=None, docs=None, tag="eq"))
            assert rc == 0, f"等量替换本件抓不到（预期为盲区），实为 rc={rc}"
        cases.append(("T6 等量替换＝已知盲区（预期不红）", run(t6)))

        # T7 无快照 ⇒ rc=2（absent ≠ 通过）
        def t7():
            rc = cmd_chk(argparse.Namespace(files=[str(f)], files_from=None, docs=None,
                                            tag="never_snapped"))
            assert rc == 2, f"无快照应 rc=2，实为 {rc}"
        cases.append(("T7 无快照 ⇒ rc=2", run(t7)))

        # T8 snap 遇取不到的件 ⇒ rc=2，且**不落快照**
        def t8():
            rc = cmd_snap(argparse.Namespace(files=[str(f), str(tmp / "nope.md")], files_from=None,
                                             docs=None, tag="half"))
            assert rc == 2, f"半截快照应 rc=2，实为 {rc}"
            assert not (SNAPDIR / "half.json").exists(), "半截快照被落盘了（absent 会被当通过）"
        cases.append(("T8 半截快照 ⇒ rc=2 且不落盘", run(t8)))

        # T9 显式 --docs 无效 ⇒ rc=2（不回落）
        def t9():
            rc = cmd_snap(argparse.Namespace(files=[str(f)], files_from=None,
                                             docs=str(tmp / "nowhere"), tag="d9"))
            assert rc == 2, f"无效 --docs 应 rc=2，实为 {rc}"
        cases.append(("T9 无效 --docs ⇒ rc=2（不回落）", run(t9)))

    finally:
        shutil.rmtree(tmp, ignore_errors=True)
        for t in ("selftest", "half", "d9", "eq"):
            p = SNAPDIR / f"{t}.json"
            if p.exists():
                p.unlink()

    bad = [n for n, (okk, _) in cases if not okk]
    for n, (okk, msg) in cases:
        print(f"  {'✓' if okk else '✗'} {n}" + (f" —— {msg}" if msg else ""))
    print(f"\nself-test: {len(cases) - len(bad)}/{len(cases)}")
    return 0 if not bad else 1


def main() -> int:
    ap = argparse.ArgumentParser(description="剥离可见性对拍（P0）")
    ap.add_argument("--self-test", action="store_true", dest="self_test")
    sub = ap.add_subparsers(dest="cmd")

    def common(p):
        p.add_argument("--file", action="append", default=[], dest="files")
        p.add_argument("--files-from", dest="files_from", help="每行一个路径的清单件")
        p.add_argument("--docs", help="docs 根（含 brain/）")
        p.add_argument("--tag", default="default")

    ps = sub.add_parser("snap", help="记下可见引录数")
    common(ps)
    pc = sub.add_parser("chk", help="再数一次并对拍")
    common(pc)
    pr = sub.add_parser("residue", help="裸引录残留嗅探（抓已在盘上的剥离残留 · 提示器）")
    pr.add_argument("--file", required=True)
    pr.add_argument("--docs")
    pr.add_argument("--min", type=int, default=20, help="重叠/引文最小字数，默认 20（实测 8 会淹没在标签行里）")
    pr.add_argument("--strict", action="store_true")

    args = ap.parse_args()
    if args.self_test:
        return self_test()
    if getattr(args, "files_from", None):
        args.files += [ln.strip() for ln in pathlib.Path(args.files_from).read_text(
            encoding="utf-8").splitlines() if ln.strip() and not ln.startswith("#")]
    if args.cmd == "snap":
        if not args.files:
            print("✗ snap 须给 --file 或 --files-from", file=sys.stderr)
            return 2
        return cmd_snap(args)
    if args.cmd == "chk":
        return cmd_chk(args)
    if args.cmd == "residue":
        return cmd_residue(args)
    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
