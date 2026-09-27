#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""研究件引文核验器 · 「换案先归零」的机械门禁（只读）

为什么有这个脚本
----------------
2026-09-26 同一会话连做三案（PEC D4 · CS-05 → CS-02 → CS-09）。
做第三案（CS-09）时，**把前两案的行号与内容携带了过来**，同一件内两处：

  ① 引「`学者谱系.md:5`『本谱系**强制引入非盎格鲁视角**』」
     —— 那是 **CS-02** 谱系的原话；CS-09 谱系 `:5` 真身是 frontmatter 行
        `updated: 2026-05-15`；「非盎格鲁」在 CS-09 全树**零命中**。
  ② 写「对照面见 **清单 `:311-318`**」
     —— 该范围在 CS-09 任何文件都不存在（其清单仅 146 行），
        真身是 **CS-05** 时间线 `:311`／`:313-318`。

**共同点**：行号在同一会话内是「可携带的」，而**引用形式看起来完全正常**；
且这两处**一在 ④ 散文、一在括号夹注**——当日的机器核只覆盖「载体表的引录列」，
**结构上够不到它们**。同日独立复验据此判该线首个 FAIL。

所以这个脚本只做一件事：**把引文核验从「某几列」扩到「全件的每一个 `文件:行号`」**，
并加一道**行号越界**闸。它不是「让人记得归零」，是**让忘记归零自己报出来**（G-X103）。

同源登记
--------
`permanent/通用教训.md` **`[G-X161]` 追记**（射程自 2026-09-26 含「案级研究件」：
「A 的东西挂到 B 名下」不限于实体，也适用于文件、行号、条款编号）
· `permanent/经验库.md` **`[EXP-20260926-011-T]`**（逐字引录核验配方 · 七坑）

用法
----
    python3 verify_citations.py --target <件.md> --corpus <dir> [--corpus <dir> ...]

    --target   要核的研究件
    --corpus   **该案**的真源目录（可多次）；解析裸简写与判定「非本案语料」都靠它
    --quiet    只打结论行

退出码：0 = 无 FAIL；1 = 有 FAIL（越界 / 引文不在所指行）

三项检查
--------
  **FAIL · 行号越界**        引了 `X:NNN`，但 X 只有 N 行
  **FAIL · 引文不在所指行**  同行紧邻的 `「…」` 不是该行归一化后的连续子串
  **FAIL · 裸简写无法归属**  引了 `:NNN` 而同行与全文均无前置文件名（读者也无从定位）
  **WARN · 非本案语料文件**  引的文件不在 --corpus 内（可能是正当的跨案引用，也可能是携带）

已知边界（别当它有它没有的能力）
--------------------------------
**⚠ 首轮实测（2026-09-26 · 对上三案件）——本工具「金丝雀全过，但当闸还不够」**

| | CS-05 | CS-02 | CS-09 |
|---|---|---|---|
| 已核引用 | 234 | 162 | 133 |
| FAIL | 22 | 15 | 26 |
| 其中假红（已分类） | ≥6 | 待分 | ≥20 |

**⇒ 现阶段的正确用法＝「提示器」，不是「闸」。判红必须先人核。**

**三类假红（已定位根因，尚未修）**：
  - **A · 跨行 carry**：表格行里引录列的裸简写（如 `:1923`）会被**同行后出现的文件名**吸走
    （实测 CS-05 的 `学者谱系.md:1923` 全是假——那是**时间线**的行号）。⇒ 正解是**按「格」作用域**解析，不是按整行。
  - **B · 年份被当行号**：文案里的 `：2026`（年份）会被识别成「行号 2026」。⇒ 需加四位数前置过滤。
  - **C · 别案行号未写全路径**：件里写「CS-05 的 `时间线:311`」而 corpus 只给本案 ⇒ 判「越界」，实为「非本案语料」。
    ⇒ **归属判据应先于越界判据。**

**一类真错但被归成假红**：**引号在件里两用**（逐字引录 ＋ 作者转述/标签），本工具无法区分，
于是把「被搬形制／被引文本」「≥2 个不同处境下的重新选中」「Nelson 殉道符号」这类**转述**判成「引文失据」。
**⇒ 这是体例问题，不是工具问题**：要让这道闸真正可用，**必须先让「引录」在版面上机器可识别**
（例如另用一种标记，或规定「引录必须紧跟 `文件:行号`、转述一律不加引号」）。**该体例裁量归 Doctor。**

其余边界：
  1. **只核「同行紧邻」的引文**——引文与引用被换行/表格分隔时看不到（宁漏不误报）。
  2. **归一化容忍粗体/反引号/反斜杠转义/空白差异**，故「对上」≠「逐字节相同」。
  3. **不判「该处是否支持该断言」**（语义层，机器判不了）。
  4. 裸简写归属**按「本行最近前置、无则全文最近前置」**；无法归属者**报 FAIL**——
     2026-09-26 金丝雀逮出：初版把此处降为 WARN，于是「读者也无从定位」的引用被判绿。

**自我订正（建造期实测，留痕）**：本工具首版**自己犯了配方里的第 3 坑（叉积）**——一行 N 个引用 ×
M 段引文两两配对，造出 20+ 条假红，**被回扫当场逮出**。另有两个自身 bug（6 元组按 5 名解包 ·
把行号当 owner 索引）由**崩溃**而非静默暴露。⇒ **「门禁自己也要过金丝雀」这条，本工具是亲身注脚。**
"""

from __future__ import annotations

import argparse
import re
import sys
import unicodedata
from pathlib import Path

# ── 归一化（与 [EXP-20260926-011-T] 同口径）───────────────────────────────
def norm(s: str) -> str:
    s = s.replace("**", "").replace("\\", "").replace("`", "")
    return re.sub(r"\s+", "", unicodedata.normalize("NFKC", s))


# ── 引用解析：只用反引号 span 内的 `文件:行号` ──────────────────────────────
CITE = re.compile(r"[:：]\s*(\d{1,5})(?:\s*[–—-]\s*(\d{1,5}))?")
NAME = re.compile(r"([^\s`/\\|]+\.md)")


def parse_citations(lines: list[str]):
    """产出一串 (行号, 文件, 起行号, 止行号, 归属来源)。

    归属规则（与配方一致）：**同 span 内文件名 → 本行最近前置文件名 → 全文最近前置**。
    """
    out = []
    carry: str | None = None      # 全文最近前置文件名
    for i, line in enumerate(lines, 1):
        line_name: str | None = None
        for span in re.findall(r"`([^`]+)`", line):
            names = NAME.findall(span)
            if names:
                line_name = names[-1]
                carry = line_name
            for m in CITE.finditer(span):
                a = int(m.group(1))
                b = int(m.group(2)) if m.group(2) else None
                if b is not None and a > b:
                    a, b = b, a
                owner = line_name or carry
                src = "span内" if names else ("本行前置" if line_name else ("全文前置" if carry else "无"))
                out.append((i, owner, a, b, src, line))
    return out


def resolve(name: str | None, corpus: list[Path]) -> Path | None:
    if not name:
        return None
    for root in corpus:
        cand = root / name if root.is_dir() else None
        if cand and cand.exists():
            return cand
        if root.is_file() and root.name == name:
            return root
        if root.is_dir():
            hits = list(root.rglob(name))
            if hits:
                return hits[0]
    return None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", required=True)
    ap.add_argument("--corpus", action="append", required=True,
                    help="**本案语料**（可多次）。越界判据的 `_maxlen` **只在 --corpus 内取**。")
    ap.add_argument("--extra", action="append", default=[],
                    help="非本案但**正当引用**的件（如别案 raw、GOTCHAS、起手包）。**只参与解析、不抬高 _maxlen**，"
                         "并把这些件上的命中单列为「非本案语料」提示。"
                         "2026-09-26 实测：若把 extra 混进 --corpus，_maxlen 会被大的件抬高 ⇒ **闸变钝、真越界不报**。")
    ap.add_argument("--quiet", action="store_true")
    ap.add_argument("--gate", choices=["all", "range"], default="all",
                    help="range＝只把「行号越界」当 FAIL，其余（引文失据/无法归属）降为 WARN。"
                         "2026-09-26 Doctor 裁：体例（引录须紧跟 `文件:行号`、转述不加引号）定妥前，"
                         "先只开越界闸——越界判据**不依赖引号**，已可用。")
    args = ap.parse_args()

    target = Path(args.target)
    corpus = [Path(c) for c in args.corpus]
    lines = target.read_text(encoding="utf-8").splitlines()

    # 语料缓存：路径 → (行列表, 归一化行列表)
    cache: dict[Path, tuple[list[str], list[str]]] = {}

    def load(p: Path):
        if p not in cache:
            ls = p.read_text(encoding="utf-8").splitlines()
            cache[p] = (ls, [norm(x) for x in ls])
        return cache[p]

    def load_pre(p: Path) -> list[str]:
        return load(p)[0]

    # ★ 越界判据＝「--corpus 内最长文件」的 **OR 语义**（2026-09-26 金丝雀二轮逮出）：
    #   初版把越界检查挂在「owner 已解析」之后 ⇒ 裸简写走「无法归属」分支、**越界根本没跑**
    #   （真错漏网、跨行 carry 造的假红全留下 —— 最坏组合）。改为 corpus 级 OR：
    #   **没有任何语料文件够长**才判红。代价＝「该简写属 A 而 A 不够长、但 B 够长」会漏 —— 宁漏不误报。
    corpus_files: list[Path] = []
    for root in corpus:
        corpus_files += sorted(root.rglob("*.md")) if root.is_dir() else [root]
    _maxlen = max((len(load_pre(p)) for p in corpus_files), default=0)
    # extra 只并入解析面，**不进 _maxlen**
    resolve_roots = list(corpus) + [Path(e) for e in args.extra]

    fails: list[str] = []
    warns: list[str] = []
    checked = 0
    pairs_by_line: dict[int, list] = {}   # 行 → [(owner, path, a, b)]（引文对拍按行聚合）

    for lineno, owner, a, b, src, line in parse_citations(lines):
        # ── 越界闸（不依赖引号、不依赖 owner 解析）──
        for n in filter(None, (a, b)):
            if _maxlen and n > _maxlen:
                msg = (f"L{lineno} **行号越界**：引 `:{n}`（owner={owner or '未归属'}），"
                       f"但 --corpus 内最长文件只有 {_maxlen} 行")
                # ★ 年份过滤（2026-09-26 实测假红类 B）：行文里的 `：1588`／`：1805`／`：2026`
                #   是**年份**，不是行号。判据＝**四位数（≥1000）且超出语料最长文件** ⇒ 降 WARN。
                #   为什么不写成区间：本线语料的年份跨「前 586 → 2026」，任何区间都会漏。
                #   ⚠ **代价（如实记）**：**四位数行号的「跨案携带」会漏**（如把 CS-05 的 `:1923`
                #     搬进一个 300 行的语料）。该型**只能靠体例治**——引录须紧跟全路径 `文件:行号`，
                #     拿不准的一律人核。**宁漏不误报**是本闸的既定取向。
                if n >= 1000:
                    warns.append(msg + " ——⚠ **疑似年份／编号**（四位数且超出语料长度），降为提示")
                else:
                    fails.append(msg)
        if owner is None:
            # ★ 2026-09-26 金丝雀逮出的门禁缺口：初版把此处降为 WARN，于是
            #   「引 `:311-318` 而全件从未出现任何文件名」这类**读者也无法定位**的引用
            #   被判绿。规约：**无法归属 = 件自身的缺陷**，报 FAIL。
            msg = (f"L{lineno} **裸简写无法归属**：引 `:{a}`"
                   + (f"-{b}" if b else "")
                   + "，但同行与全文均无前置文件名 ⇒ **读者也无从知道它指哪个文件**")
            (warns if args.gate == "range" else fails).append(msg)
            continue
        path = resolve(owner, resolve_roots)
        if path is None:
            warns.append(f"L{lineno} 引 `{owner}` —— **不在 --corpus/--extra 内**（跨案引用？还是携带？）")
            continue
        elif not any(str(path).startswith(str(r)) for r in corpus):
            warns.append(f"L{lineno} 引 `{owner}` —— 落在 **--extra（非本案语料）**，本行不参与越界判据")
            continue
        src_lines, src_norm = load(path)
        checked += 1
        # ★ 越界检查用「按行引用集的 OR」：表格行的简写（如引录列的 `:1931`）
        #   常指向**同行的另一个文件**，硬按「最后一个文件名」归属会造大量假红。
        #   规约：裸简写只要在**本行被引的任一文件**里不越界即通过；
        #   全行文件都不够长才判红（此时的报错信息列出该行的文件集）。
        #   代价：会漏掉「该简写其实属 A 而 A 不够长、但 B 够长」的个案——**宁漏不误报**。
        # 引文对拍：**按行聚合**——一行可有多个引用与多段引文，
        # ★ 每段引文只需对上**本行任一处引用**（配方 [EXP-20260926-011-T] 第 3 坑：禁叉积）。
        #   本脚本首版正是犯了这个叉积，被 2026-09-26 的回扫逮出（见文末「自我订正」）。
        pairs_by_line.setdefault(lineno, []).append((owner, path, a, b))

    # ── 按行聚合的引文对拍（每段引文只需对上本行任一处引用）──────────────
    for lineno, pairs in sorted(pairs_by_line.items()):
        line = lines[lineno - 1]
        quotes = re.findall(r"「([^」]{6,})」", line)
        if not quotes:
            continue
        cands = []
        for owner, path, a, b in pairs:
            src_lines, src_norm = load(path)
            for n in (a, b):
                if n and n <= len(src_lines):
                    cands.append((owner, n, src_norm[n - 1]))
        if not cands:
            continue
        for q in quotes:
            qn, core = norm(q), norm(q)[:30]
            if not any(core in sn or sn[:30] in qn for _, _, sn in cands):
                where = " · ".join(f"`{o}:{n}`" for o, n, _ in cands)
                msg = f"L{lineno} **引文不在所指行**：本行引用 {where}，但均找不到 → 「{q[:44]}…」"
                (warns if args.gate == "range" else fails).append(msg)

    print(f"引文核验：{target.name}")
    print(f"  corpus: " + " · ".join(str(c) for c in corpus))
    print(f"  已核引用 {checked} 处 · FAIL {len(fails)} · WARN {len(warns)} · gate={args.gate}")
    if fails:
        print("\n  ❌ FAIL：")
        for f in fails:
            print("     " + f)
    if warns and not args.quiet:
        print("\n  ⚠ WARN（不是错，但请人核一眼）：")
        for w in warns:
            print("     " + w)
    if not fails:
        print("\n  ✅ 未发现越界与引文失据。")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
