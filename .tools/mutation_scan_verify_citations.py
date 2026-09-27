#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""变异扫描台 —— `verify_citations.py`「守卫有没有齿」的机器扫描（**只读原文件**）

    python3 mutation_scan_verify_citations.py              # 全跑
    python3 mutation_scan_verify_citations.py -v           # 附失败例名
    python3 mutation_scan_verify_citations.py --point norm-flatten

为什么有这个脚本
----------------
2026-09-27 的七轮独立复验把该工具从「闸」降回「提示器」时，用的是**人工逐点阉割**；
第 7 位复验方另做了一次 49 点独立扫描——两组数字（23 点 vs 49 点）本身就说明
**「扫了多少点」是人的选择，不是机器的输出**。⇒ 把它落成盘上脚本，让扫描**可复跑、可扩点**。

做法（两个轴交叉）
------------------
对每个**实现点**注入**定向变异**（精确字符串替换），在**临时目录**里：
  ① 跑金丝雀（连同被测工具一起拷进临时目录）→ 判「**有无守卫**」
  ② 跑四案真树（`--gate range`）→ 判「**是否改变真案读数**」

  有守卫 · 改读数 → ✅ 已守
  有守卫 · 不改   → ✅ 已守（惰性，但变异确实有齿）
  无守卫 · 改读数 → ⚠️ **目标格**（最危险：改坏了没人知道，且真案读数会变）
  无守卫 · 不改   → ⚪ 惰性（登记，不急）

⚠ **「改读数」这个轴的定义（承未参与实施的二轮复验方 · 2026-09-27 收窄）**
--------------------------------------------------------------
本轴的判据**只比四案汇总行 `已核引用 … · FAIL … · WARN …` 那一行**，**不含**紧随其后的
「弱归属（归属来源＝全文前置）N / M 处引用」行。⇒ **`改读数=否` 不等于「什么都没变」**：
`weak-total-*` 那两条**会改弱归属计数**，只因它不在比对行内才报「否」。
**引用本矩阵时请连读这一句**，勿把「否」当「无影响」。

⚠ **另一个更重要的界限**：矩阵的**分母是人的选择**。本表只覆盖**写入 `MUTATIONS` 的那几行**；
**「目标格 0/N」只对表内这几行成立**，**不等于该点类闭合**。二轮复验方自造 41 条非重复变异，
15 条逃逸、其中 6 条改四案读数 ⇒ **示例式守卫只能守住「想到的那一种改法」**。
**故：报扫描结论时，必须同时报「扫了哪些行、用了哪几种改法」。**
铁律（三条，都是踩出来的）
--------------------------
1. **只在临时目录里改副本** —— 本脚本对盘上 `verify_citations.py` **只读**，
   全程不写原文件；**运行头与审计尾各印一次该件的 SHA-256**，两次一致即可比对
   （⚠ 承三轮复验：这里原先写「见 `--verify-untouched`」——**那个 flag 根本不存在**，
   已订正为如实的口径）。
2. **变异必须真的生效** —— 目标字符串找不到 ⇒ 报 `MUTATION-NOT-APPLIED` 并计入失败，
   **不得静默跳过**（G-X197 同型：一条判据的下一个动作是什么，答不出就等于没写）。
3. **「金丝雀全绿」不等于「变异被抓」** —— 判据是**变异后**金丝雀是否转红，不是基线是否绿。
   基线的绿由 `EXPECTED_CASES` 例数守卫另管。

⚠ **自证范围（2026-09-27 三轮复验后如实补）**：本脚本只做**块内自证**（运行头与审计尾各印一次
`verify_citations.py` 的 SHA-256，可比对）。**它没有独立的第三方锚**——`judgment_points()` 的 AST
过滤集、以及 `BASELINE_*` / `ANCHOR_MAX_HITS` 三组常量**都在被审文件里自报**，**改它们即免疫**。

⚠ 本脚本**不改任何判据、不代签**：它只产出一张矩阵。**红/绿怎么处置归人。**
"""

from __future__ import annotations

import argparse
import ast
import hashlib
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOOL = HERE / "verify_citations.py"
CANARY = HERE / "test_verify_citations.py"

# ── 真案（与金丝雀 R 组同源；改这里须同步改 R 组）───────────────────────────
REAL_CASES = [
    ("CS-05", "raw/2026-09-26_analysis_CS05证据层补全_折中法.md", "case-studies/CS-05_中华文明"),
    ("CS-02", "raw/2026-09-26_analysis_CS02证据层补全_折中法.md", "case-studies/CS-02_盎格鲁撒克逊-英国文明"),
    ("CS-01", "raw/2026-09-26_analysis_CS01证据层补全_折中法样板.md", "case-studies/CS-01_犹太-以色列文明"),
    ("CS-09", "raw/2026-09-26_analysis_CS09证据层补全_折中法.md", "case-studies/CS-09_伊斯兰文明"),
]

# ── 变异点表 ────────────────────────────────────────────────────────────────
# `old` 必须在源文件里**恰好出现一次**；否则报 MUTATION-NOT-APPLIED（铁律 2）。
# 2026-09-27 首批＝七轮复验「未闭项」里点名的 5 点 ＋ P19 边界 1 点 ＋ 惰性 3 点。
MUTATIONS = [
    dict(
        id="norm-flatten",
        point="norm() 空白折叠（`re.sub(r'\\s+','',…)`）",
        note="删掉空白折叠。散文里全角/半角空格一多，引文对拍与归属就整体移位。",
        old='    return re.sub(r"\\s+", "", unicodedata.normalize("NFKC", s))',
        new='    return unicodedata.normalize("NFKC", s)',
    ),
    dict(
        id="cite-fullwidth-colon",
        point="CITE 全角冒号（`[:：]`）",
        note="只留半角冒号。中文件里 `：311` 这类写法会整条不被解析。",
        old='CITE = re.compile(r"[:：]\\s*(\\d{1,5})(?:\\s*[–—-]\\s*(\\d{1,5}))?")',
        new='CITE = re.compile(r"[:]\\s*(\\d{1,5})(?:\\s*[–—-]\\s*(\\d{1,5}))?")',
    ),
    dict(
        id="quote-minlen-raise",
        point="引文最短长度 6 字（`「([^」]{6,})」`）· 抬高侧",
        note="6→8：短引文整条不检 ⇒ 漏报方向。",
        old='        quotes = re.findall(r"「([^」]{6,})」", line)',
        new='        quotes = re.findall(r"「([^」]{8,})」", line)',
    ),
    dict(
        id="quote-minlen-lower",
        point="引文最短长度 6 字 · 压低侧",
        note="6→4：更多短引文进检 ⇒ 噪声方向（闸退化成噪声源的经典路径）。",
        old='        quotes = re.findall(r"「([^」]{6,})」", line)',
        new='        quotes = re.findall(r"「([^」]{4,})」", line)',
    ),
    dict(
        id="weak-total-src",
        point="weak_total 判据（`if src == \"全文前置\"`）",
        note="改成认「本行前置」⇒ 汇总行报的弱归属计数变。",
        old='        if src == "全文前置":\n            weak_total += 1',
        new='        if src == "本行前置":\n            weak_total += 1',
    ),
    dict(
        id="weak-total-drop",
        point="weak_total 计数（整个增量拿掉）",
        note="七轮复验点名的形态之一：计数恒 0 ⇒ 汇总行那句自陈消失。",
        old='        if src == "全文前置":\n            weak_total += 1',
        new='        if src == "全文前置":\n            weak_total += 0',
    ),
    dict(
        id="weak-over-owner-cond",
        point="weak_over_owner 判据（缺陷⑨ 收敛版触发器）",
        note="整条关掉 ⇒「弱归属放行」WARN 不再出。",
        old='                elif src == "全文前置" and owner_len is not None and n > owner_len:',
        new='                elif False:',
    ),
    dict(
        id="quote-pair-ab",
        point="引文对拍 `for n in (a, b)`",
        note="只试起行 `a`、丢掉止行 `b` ⇒ 区间引用只要起行对不上就整条漏。",
        old='            for n in (a, b):\n                if n and n <= len(src_lines):',
        new='            for n in (a,):\n                if n and n <= len(src_lines):',
    ),
    dict(
        id="p19-ratio-le",
        point="P19 边界：散文后缀占比 `len(sub)*3 < len(stem)` 的 `<=` 侧",
        note="`<`→`<=`：占比**恰 1/3** 的件被排除。P19 用的是 0.4，故它守不住这一侧。",
        old='            if len(sub) * 3 < len(stem):',
        new='            if len(sub) * 3 <= len(stem):',
    ),
    dict(
        id="ok-token-cjk-min",
        point="_ok_token 单字 CJK 门槛（`return len(s) >= 2`）",
        note="≥2→≥1：单字词元进来 ⇒ 中文里命中率过高、必成噪声源。",
        old='    return len(s) >= 2\n\n\ndef prose_candidates',
        new='    return len(s) >= 1\n\n\ndef prose_candidates',
    ),
    dict(
        id="year-filter-1000",
        point="年份过滤 1000 阈值（`if n >= 1000:`）",
        note="≥1000→>1000：恰 1000 的行号不再降 WARN。",
        old='                    if n >= 1000:',
        new='                    if n > 1000:',
    ),
    dict(
        id="prose-sort",
        point="prose_candidates 排序（`key=lambda kv: (-kv[1], kv[0])`）",
        note="去掉行数降序 ⇒ 展示的前 4 件可能不含 `_hi`（`_hi` 用 max，故触发不变）。",
        old='    return sorted(hits.items(), key=lambda kv: (-kv[1], kv[0]))',
        new='    return sorted(hits.items(), key=lambda kv: (kv[1], kv[0]))',
    ),
    # ── 以下两条承**未参与实施的独立复验方**（2026-09-27 首轮 · 对抗测试）补 ──────────────
    # 复验方自造 23 条非重复变异，**9 条逃过 55/55**；这两条是其中**触碰真案输出**者。
    # ⇒ 教训：**「目标格 0/6」只对表内 12 行为真**——补一对守卫只守住了「实施者想到的那一种改法」。
    dict(
        id="quote-charclass-dot",
        point="引文收集的**字符类**（`「([^」]{6,})」` 的 `[^」]` → `.`）",
        note="同行两条引文会被**并成一条**。实测逃过 55/55 且**改动四案 WARN 读数**"
             "（CS-05 27→43 · CS-02 54→46 · CS-09 53→49）——按本台自己的判据它就是目标格。",
        old='        quotes = re.findall(r"「([^」]{6,})」", line)',
        new='        quotes = re.findall(r"「(.{6,})」", line)',
    ),
    dict(
        id="quote-pair-bonly",
        point="引文对拍**只试止行**（`for n in ((b,) if b else (a,))`）",
        note="与 `for n in (a,)` 反向的同一缺口。实测逃过 55/55；能把「起行匹配」的区间引用由绿翻红。",
        old='            for n in (a, b):\n                if n and n <= len(src_lines):',
        new='            for n in ((b,) if b else (a,)):\n                if n and n <= len(src_lines):',
    ),
    # ── 以下四条承**二轮独立复验方**（2026-09-27 · 判 `PASS_WITH_LIMITS`）+ Doctor 裁「补完这两处后收」──
    # 二轮复验方另造 41 条变异、15 条逃逸、**6 条改读数**；这四条是其中改读数的 4 条（余 2 条见下「未闭」）。
    # **⚠ 它们的存在本身就在说：点类的形态不可穷尽**——每补一轮，下一轮仍能再造出新的。
    dict(
        id="quote-findall-first-only",
        point="引文收集**只取首条**（`re.findall(...)[:1]`）",
        note="逃过 58/58，且改读数：CS-05 27→14 · CS-02 54→40 · CS-09 53→41。",
        old='        quotes = re.findall(r"「([^」]{6,})」", line)',
        new='        quotes = re.findall(r"「([^」]{6,})」", line)[:1]',
    ),
    dict(
        id="quote-findall-last-only",
        point="引文收集**只取末条**（`re.findall(...)[-1:]`）",
        note="逃过 58/58，且改读数：CS-05 27→16 · CS-02 54→47 · CS-09 53→45。",
        old='        quotes = re.findall(r"「([^」]{6,})」", line)',
        new='        quotes = re.findall(r"「([^」]{6,})」", line)[-1:]',
    ),
    dict(
        id="quote-lazy-dot",
        point="引文收集**懒匹配**（`[^」]{6,}` → `.{6,}?`）",
        note="`.` 能匹配 `」` ⇒ 短引文被并进后一条。逃过 58/58，改读数：CS-05 27→60 · CS-02 54→64 · CS-09 53→58。",
        old='        quotes = re.findall(r"「([^」]{6,})」", line)',
        new='        quotes = re.findall(r"「(.{6,}?)」", line)',
    ),
    dict(
        id="quote-any-to-all",
        point="引文对拍 **`any` → `all`**（要求每条候选行都含引文）",
        note="逃过 58/58（靠**反向包含兜底**吞掉），改读数：CS-05 27→67 · CS-02 54→75 · CS-09 53→64。",
        old='            if any(core in sn for _, _, sn in cands):',
        new='            if all(core in sn for _, _, sn in cands):',
    ),
    # ── 以下四条承**三轮独立复验方**（2026-09-27）──
    # 其中三条是「引文收集」**取 N 条 / 去重排序**族，一条是「引文夹带**门槛下侧**」。
    dict(
        id="quote-sorted-set-first",
        point="引文收集**去重排序后取首**（`sorted(set(...))[:1]`）",
        note="实测逃过 62/62 且改读数：CS-05 27→13 · CS-02 54→41 · CS-09 53→39。"
             "⚠ 它能逃过当时的 N14/N15，是因为那两例的坏引文码位**低于**好引文（已修为 `龘`）。",
        old='        quotes = re.findall(r"「([^」]{6,})」", line)',
        new='        quotes = sorted(set(re.findall(r"「([^」]{6,})」", line)))[:1]',
    ),
    dict(
        id="quote-take-two",
        point="引文收集**取前两条**（`[:2]`）",
        note="实测逃过 62/62 且改读数：CS-05 27→18 · CS-02 54→47 · CS-09 53→47。",
        old='        quotes = re.findall(r"「([^」]{6,})」", line)',
        new='        quotes = re.findall(r"「([^」]{6,})」", line)[:2]',
    ),
    dict(
        id="quote-take-last-two",
        point="引文收集**取末两条**（`[-2:]`）",
        note="实测逃过 62/62 且改读数：CS-05 27→22 · CS-02 54→52 · CS-09 53→50。",
        old='        quotes = re.findall(r"「([^」]{6,})」", line)',
        new='        quotes = re.findall(r"「([^」]{6,})」", line)[-2:]',
    ),
    # ⚠ 以下三条承**四轮复验**：第三次修 `某`→`龘`（坏条码位**最高**）时，**自己造出**了
    #   「排序后取末」这一族逃逸（与三轮 `[:1]` 是同一机理的**镜像**）。N15 改用最低码位的 `一` 后堵上。
    dict(
        id="quote-sorted-set-two",
        point="引文收集**去重排序后取前二**（`sorted(set(...))[:2]`）",
        note="与 `quote-sorted-set-first` 同族；由 N14（坏条码位最高）逮住。",
        old='        quotes = re.findall(r"「([^」]{6,})」", line)',
        new='        quotes = sorted(set(re.findall(r"「([^」]{6,})」", line)))[:2]',
    ),
    dict(
        id="quote-sorted-set-last",
        point="引文收集**去重排序后取末**（`sorted(set(...))[-1:]`）",
        note="★ 四轮复验逮出的**回归**：逃过 63/63 且改读数（CS-05 27→17 · CS-02 54→47 · CS-09 53→48）。"
             "由 N15（坏条改用码位**最低**的 `一`）逮住。",
        old='        quotes = re.findall(r"「([^」]{6,})」", line)',
        new='        quotes = sorted(set(re.findall(r"「([^」]{6,})」", line)))[-1:]',
    ),
    dict(
        id="quote-sorted-set-lasttwo",
        point="引文收集**去重排序后取末二**（`sorted(set(...))[-2:]`）",
        note="同族另一格：逃过 63/63 且改读数（CS-05 27→23 · CS-02 54→51 · CS-09 53→52）。",
        old='        quotes = re.findall(r"「([^」]{6,})」", line)',
        new='        quotes = sorted(set(re.findall(r"「([^」]{6,})」", line)))[-2:]',
    ),
    dict(
        id="quote-carry-threshold-0",
        point="引文夹带**门槛下侧**（`len(sn_[:30]) + 20` → `+ 0`）",
        note="实测逃过 62/62，改读数：CS-09 W53→56。二轮只补了「够长必须报」的上侧。",
        old='                elif len(qn) >= len(sn_[:30]) + 20:',
        new='                elif len(qn) >= len(sn_[:30]) + 0:',
    ),
]


# ══════════════════════════════════════════════════════════════════════════════
# 点类登记表（结构层 · 2026-09-27 Doctor 裁「都做」）
# ══════════════════════════════════════════════════════════════════════════════
# **为什么要有这一层**：上面的 `MUTATIONS` 是一张**平铺清单**——分母（扫多少点）是**人的选择**。
#   两轮独立复验反复咬到的正是这一点：每轮都能再造成新的逃逸，而报告里只有分子没有分母。
#   本层把「人的选择」换成**三样可核的东西**：
#     ① **声明点类**：每类写明**落点锚串**（证明该类还在它说的位置）＋ **形态下限 `min_forms`**
#        —— 形态数掉到下限以下即判红，**不能靠删表悄悄降覆盖**；
#     ② **判据点归属**：用 AST 数出 `verify_citations.py` 里所有判据点（`If` 节点 ＋ 正则编译/调用），
#        要求每个判据点命中某个已声明点类的锚串；**未归属的逐个列出**——
#        这就是「我没想到要扫」的**可见化**（原来它是隐形的）；
#     ③ **报法**：不再只报「目标格 0/N」，改报「点类 X/Y · 形态 Z 种 · 判据点归属 P/Q · 逃逸 W（改读数 V）」。
# **它治什么、不治什么**：治**分母不可见**；**不治**形态本身的不可穷尽（真穷尽要形式化语义，做不到）。
#   ⇒ **把一个隐藏的洞，换成一行可见的指标。**

POINT_CLASSES: list[dict] = [
    dict(id="normalize", name="归一化（空白折叠 / NFKC）",
         anchors=["def norm(", "unicodedata.normalize"],
         min_forms=1, forms=["norm-flatten"]),
    dict(id="cite-parse", name="引用解析正则（CITE）",
         anchors=["CITE = re.compile"],
         min_forms=1, forms=["cite-fullwidth-colon"]),
    dict(id="quote-collect", name="引文收集（正则）",
         anchors=['quotes = re.findall'],
         min_forms=12,
         forms=["quote-minlen-raise", "quote-minlen-lower", "quote-charclass-dot",
                "quote-findall-first-only", "quote-findall-last-only", "quote-lazy-dot",
                "quote-sorted-set-first", "quote-sorted-set-two",
                "quote-sorted-set-last", "quote-sorted-set-lasttwo",
                "quote-take-two", "quote-take-last-two"]),
    dict(id="quote-match", name="引文对拍（候选行匹配）",
         anchors=["for n in (a, b):", "if any(core in sn"],
         min_forms=4,
         forms=["quote-pair-ab", "quote-pair-bonly", "quote-any-to-all",
                "quote-carry-threshold-0"]),
    dict(id="prose-ratio", name="散文绑定 · 后缀占比阈值",
         anchors=["if len(sub) * 3 < len(stem)"],
         min_forms=1, forms=["p19-ratio-le"]),
    dict(id="prose-token", name="散文绑定 · 词元门槛（_ok_token）",
         anchors=["def _ok_token("],
         min_forms=1, forms=["ok-token-cjk-min"]),
    dict(id="prose-sort", name="散文绑定 · 候选排序",
         anchors=["return sorted(hits.items()"],
         min_forms=1, forms=["prose-sort"]),
    dict(id="weak-count", name="弱归属计数（weak_total）",
         anchors=["weak_total += 1"],
         min_forms=2, forms=["weak-total-src", "weak-total-drop"]),
    dict(id="weak-trigger", name="弱归属放行触发器（weak_over_owner）",
         anchors=['elif src == "全文前置" and owner_len'],
         min_forms=1, forms=["weak-over-owner-cond"]),
    dict(id="year-filter", name="年份过滤阈值",
         anchors=["if n >= 1000:"],
         min_forms=1, forms=["year-filter-1000"]),
]

# 判据点归属的**基线**（未归属数的上限）。
# ★ 语义：**未归属数不得比基线增长**——新加一个判据点却不给它归属点类，就会红。
#   ⚠ 这不是「未归属=0」的要求：**未归属本身就是本层的产出**（它把「没想到要扫」显形），
#     要求归零等于要求把没扫的点类都编一个名字，正是本层要防的形式主义。
#   基线值由 **`--coverage-only` 实测**后钉死：2026-09-27 实测 **55 个判据点 · 已归属 6 · 未归属 49**。
#   ⚠ **49/55 未归属**这个数本身就是本层最值钱的产出——它诚实地说明**登记表只覆盖了很小一片**，
#     其余判据点**没有任何已登记的变异形态在扫**。改 `verify_citations.py` 的判据点结构须同步复测。
BASELINE_UNASSIGNED = 49

# ★ 同批（承三轮独立复验的 C3/C4/C5b 三种攻击）：登记表的牙**不能只有「在不在」**——
#   复验方实测四种「不碰任何判据就把绿造出来」的路子，故各补一道：
#   ① **判据点总数下限**：弱化 `judgment_points()` 的 AST 过滤 ⇒ 分母缩水、未归属绝对数假降而转绿。
#      现钉总数：低于基线即红（比**绝对数**多一道，缩小分母不再免疫）。
#   ② **锚串特异性**：把锚串放宽成 `"if "` 之类 ⇒ 41 个无关判据点被「假归属」上去、未归属 49→7。
#      现钉：**单个锚串命中的判据点不得超过 `ANCHOR_MAX_HITS`**。
#   ③ **跨类重复登记**：同一变异 id 挂在两个点类 ⇒ 按点类的「逃逸 0 ✅」可以被打假（C5c 实证）。
#      现钉：同一个 id 不得出现在 >1 个点类里。
#   ⚠ **仍然无法在文件内解决的一条（如实披露）**：`BASELINE_UNASSIGNED`／`BASELINE_JUDGMENT_POINTS`／
#     `ANCHOR_MAX_HITS` 与 `judgment_points()` 的过滤集**都在被审文件里自报**——**改它们即免疫**
#     （复验方攻击 C2 实证：基线 49→500 ＋ 真造 3 个未归属点 ⇒ rc=0）。
#     **登记表自己的尺也是人的选择**；它挡的是**无意识的漂移**，不挡**有意识的自我豁免**。
BASELINE_JUDGMENT_POINTS = 55
ANCHOR_MAX_HITS = 8


def judgment_points(src: str) -> list[tuple[int, str]]:
    """枚举 `verify_citations.py` 的「判据点」→ [(行号, 该行原文 stripped)]。

    判据点＝**机械可复算**的两类 AST 节点，按行号去重（一行多个算一个）：
      ① 每个 `ast.If`；② 每个正则编译/调用（`re.compile` 赋值 · `re.findall`/`finditer`/`search`）。
    ⚠ 刻意**不**把裸比较运算符也算进来：那会把 `i < n` 这类循环边界也算判据点，噪声淹没信号。
      代价如实记：**纯比较式子（如 `n > allowed` 单独成句而不在 `if` 里）会漏**。
    """
    tree = ast.parse(src)
    lines = src.splitlines()
    hits: set[int] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.If):
            hits.add(node.lineno)
        elif isinstance(node, ast.Call):
            n = getattr(node.func, "attr", None)
            if n in ("findall", "finditer", "search", "compile"):
                hits.add(node.lineno)
    return sorted((n, lines[n - 1].strip()) for n in hits if n <= len(lines))


def coverage_report(src: str, rows: list) -> tuple[bool, list[str]]:
    """点类登记表的审计 + 报法。返回 (是否判红, 报告行列表)。"""
    out: list[str] = []
    bad: list[str] = []
    lines = src.splitlines()

    # ① 点类声明完整性：锚串必须在盘上找得到；形态数必须 ≥ min_forms
    out.append(f"{'点类':<28}{'锚串':<7}{'形态':<12}判定")
    covered = 0
    # ★ 负向探针逮出的缺口（2026-09-27）：原判据取 `len(pc["forms"])`，于是**把一个形态 id
    #   改成不存在的串**时长度不变 ⇒ 形态数虚报、判据不响（实测 rc=0）。现改为
    #   **只数在 `MUTATIONS` 表里真存在的 id**，并单独报「幽灵形态」。
    known_forms = {m["id"] for m in MUTATIONS}
    # ★ 承三轮复验 C5b：同一 id 挂多个点类 ⇒ 按点类的 ✅ 可被打假。跨类重复登记即红。
    seen_in: dict[str, list[str]] = {}
    for pc in POINT_CLASSES:
        for f in set(pc["forms"]):
            seen_in.setdefault(f, []).append(pc["id"])
    cross_dup = {f: v for f, v in seen_in.items() if len(v) > 1}
    if cross_dup:
        for f, v in cross_dup.items():
            bad.append(f"变异 id `{f}` 跨 {len(v)} 个点类重复登记（{' · '.join(v)}）"
                       " ⇒ 按点类的逃逸统计会被打假")
    # ★ 承三轮复验 C4：锚串须有特异性——命中过多判据点＝假归属（锚串放宽成 `if ` 可把 48/55 归上去）。
    pts_pre = judgment_points(src)
    over_wide: list[str] = []
    for pc in POINT_CLASSES:
        for a in pc["anchors"]:
            n_hit = sum(1 for n, _t in pts_pre if a in lines[n - 1])
            if n_hit > ANCHOR_MAX_HITS:
                over_wide.append(f"{pc['id']} 的锚串 `{a}` 命中 {n_hit} 个判据点")
    if over_wide:
        bad.append("锚串过宽（假归属风险，上限 " + str(ANCHOR_MAX_HITS) + "）：" + " · ".join(over_wide))
    for pc in POINT_CLASSES:
        miss = [a for a in pc["anchors"] if a not in src]
        ghost = [f for f in pc["forms"] if f not in known_forms]
        # ★ 去重后再数（自审逮出）：原式按**列表长度**数，于是把同一个 id 写两遍就能
        #   凭空凑够下限——与「幽灵 id 虚报」同族。现按 **distinct** 数，并另报重复项。
        dup = sorted({f for f in pc["forms"] if pc["forms"].count(f) > 1})
        n_forms = len({f for f in pc["forms"] if f in known_forms})
        ok = not miss and not ghost and not dup and n_forms >= pc["min_forms"]
        covered += 1 if ok else 0
        why = ("锚串已不在源码里 ⇒ 该类落点漂移" if miss
               else f"形态 id 在变异表里不存在：{' · '.join(ghost)} ⇒ **虚报形态数**" if ghost
               else f"形态 id 重复登记：{' · '.join(dup)} ⇒ **用重复凑下限**" if dup
               else f"形态 {n_forms} < 下限 {pc['min_forms']} ⇒ 覆盖被悄悄降低")
        out.append(f"{pc['id']:<28}{'✓' if not miss else '✗':<7}"
                   f"{n_forms}/{pc['min_forms']:<10}{'✅' if ok else '❌ ' + why}")
        if not ok:
            bad.append(f"{pc['id']}：{why}")
    # ★ 承三轮复验 M2：**声明里写了「点类 X/Y」这个聚合数，盘上却从不打印**（`covered` 是死变量）。
    #   该类措辞要么打印、要么删掉——现按声明打印。
    out.append(f"  ⇒ **点类 {covered}/{len(POINT_CLASSES)}** 通过（锚串在场 · 形态数达标 · 无幽灵/重复/跨类重复）")

    # ② 判据点归属：AST 数出来的每个判据点，须命中某个已声明点类的锚串
    pts = judgment_points(src)
    anchors = [(pc["id"], a) for pc in POINT_CLASSES for a in pc["anchors"]]
    unassigned = [(n, t) for n, t in pts
                  if not any(a in lines[n - 1] for _, a in anchors)]
    out.append("")
    out.append(f"判据点归属：**{len(pts) - len(unassigned)}/{len(pts)}** 已归属"
               f"（未归属 {len(unassigned)} · 上限 {BASELINE_UNASSIGNED}）"
               f" · 判据点总数 {len(pts)}（下限 {BASELINE_JUDGMENT_POINTS}）")
    if len(unassigned) > BASELINE_UNASSIGNED:
        bad.append(f"未归属判据点 {len(unassigned)} > 上限 {BASELINE_UNASSIGNED}"
                   "（新加的判据点没给归属点类）")
    # ★ 承三轮复验 C3：只钉「未归属绝对数」时，**弱化 `judgment_points()` 的过滤集**会把分母缩小、
    #   绝对数随之下降 ⇒ 判绿而覆盖实为变差（实测 49→42 转绿）。⇒ 另钉**判据点总数下限**。
    if len(pts) < BASELINE_JUDGMENT_POINTS:
        bad.append(f"判据点总数 {len(pts)} < 下限 {BASELINE_JUDGMENT_POINTS}"
                   "（`judgment_points()` 的 AST 过滤集被收窄 ⇒ 分母缩水、未归属假降）")
    if unassigned:
        out.append("  ⚠ **未归属的判据点（＝「没想到要扫」的可见化）**：")
        for n, t in unassigned[:12]:
            out.append(f"     · L{n}: {t[:92]}")
        if len(unassigned) > 12:
            out.append(f"     …另有 {len(unassigned) - 12} 个")

    # ③ 逃逸统计（按点类聚合，来自上面的矩阵）
    # ★ 承三轮复验 M4（C5c 实证）：原式用 `next(...)` **只取首个命中的点类** ⇒ 把一个**已知无守卫**的
    #   变异挪进另一个类，原类仍印「形态 1 · 逃逸 0 ✅」——**按点类的 ✅ 可以被打假**。
    #   现改为**多类同挂**（一个 id 属几个类就计入几个），且形态数按 **distinct** 印。
    esc_by_class: dict[str, list[str]] = {}
    for m, st, verdict, payload in rows:
        if st != "OK":
            continue
        cls_list = [pc["id"] for pc in POINT_CLASSES if m["id"] in pc["forms"]]
        if not cls_list:
            cls_list = ["（未登记点类）"]
        if not payload[0]:
            for c in cls_list:
                esc_by_class.setdefault(c, []).append(m["id"])
    out.append("")
    out.append("按点类的逃逸：")
    for pc in POINT_CLASSES:
        e = esc_by_class.get(pc["id"], [])
        # 「逃逸」＝无守卫逮住该变异；再分「改读数」与「惰性」两档（前者才是目标格）
        n_ch = sum(1 for m, st, _v, p in rows
                   if st == "OK" and m["id"] in pc["forms"] and not p[0] and p[1])
        out.append(f"  · {pc['id']:<18} 形态 {len(set(pc['forms']))} · 逃逸 {len(e)}"
                   f"（其中**改读数** {n_ch}）"
                   + (f"：{' · '.join(e)}" if e else " ✅"))
    stray = esc_by_class.get("（未登记点类）")
    if stray:
        out.append(f"  · ⚠ **未登记点类的变异**：{' · '.join(stray)}")
        bad.append("存在未登记点类的变异（表与登记表不同步）")

    # ③b **静态**孤儿检查（承负向探针：上面那条只在跑完变异矩阵后才可能响，
    #     `--coverage-only` 下永远不响）。⇒ 不依赖运行结果，直接查表：
    orphan = [m["id"] for m in MUTATIONS
              if not any(m["id"] in pc["forms"] for pc in POINT_CLASSES)]
    if orphan:
        out.append(f"  · ⚠ **变异表里有 id 不属于任何点类**：{' · '.join(orphan)}")
        bad.append(f"{len(orphan)} 个变异 id 未登记到任何点类（表与登记表不同步）")
    return (len(bad) > 0), out + (["  判红原因："] + [f"   ❌ {b}" for b in bad] if bad else [])


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def find_pec_root() -> Path | None:
    for base in (Path("/sessions"), Path("/Users")):
        if not base.exists():
            continue
        cands = sorted(base.glob("*/mnt/Documents/Claude/Projects/PEC"))
        cands += sorted(base.glob("*/Documents/Claude/Projects/PEC"))
        if cands:
            return cands[0]
    return None


def run_canary(tmp: Path) -> tuple[int, list[str]]:
    """在临时目录里跑金丝雀，返回 (rc, 失败例名)。"""
    p = subprocess.run([sys.executable, str(tmp / CANARY.name)],
                       capture_output=True, text=True, cwd=str(tmp))
    out = p.stdout + p.stderr
    fails = []
    for ln in out.splitlines():
        s = ln.strip()
        if s.startswith("❌ "):
            fails.append(s[2:].strip())
    return p.returncode, fails


def run_real(tool: Path, root: Path) -> dict[str, tuple[int, str]]:
    """跑四案真树，返回 {案: (rc, '已核 X · FAIL Y · WARN Z')}。"""
    res: dict[str, tuple[int, str]] = {}
    for tag, tgt, corp in REAL_CASES:
        t, c = root / tgt, root / corp
        if not (t.exists() and c.exists()):
            res[tag] = (-1, "⏭ 缺件")
            continue
        p = subprocess.run([sys.executable, str(tool), "--target", str(t), "--corpus", str(c),
                            "--gate", "range"], capture_output=True, text=True)
        summary = next((x.strip() for x in p.stdout.splitlines() if "已核引用" in x), "（无汇总行）")
        res[tag] = (p.returncode, summary)
    return res


def _coverage_section(rows: list, coverage_only: bool) -> int:
    """打印「点类登记表」审计，返回其退出码（1 ＝ 登记表判红）。"""
    print("═" * 78)
    print("点类登记表 · 覆盖审计"
          + ("（--coverage-only：本轮只跑登记表，不跑变异矩阵）" if coverage_only else ""))
    print("═" * 78)
    cov_bad, cov_lines = coverage_report(TOOL.read_text(encoding="utf-8"), rows)
    for ln in cov_lines:
        print("  " + ln)
    if coverage_only:
        print("  ⚠ 本轮未跑变异矩阵 ⇒ 上面「按点类的逃逸」一栏不可用。")
    print()
    print(f"  原文件未改动自证：verify_citations.py SHA-256 {sha256(TOOL)[:16]}…")
    return 1 if cov_bad else 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--point", action="append", default=[], help="只跑指定变异 id（可重复）")
    ap.add_argument("-v", "--verbose", action="store_true", help="附失败例名与逐案读数")
    ap.add_argument("--coverage-only", action="store_true",
                    help="只跑「点类登记表」审计（秒级），不跑变异矩阵")
    args = ap.parse_args()

    print("═" * 78)
    print("变异扫描台 · verify_citations.py")
    print(f"  工具 SHA-256 {sha256(TOOL)[:16]}…   金丝雀 SHA-256 {sha256(CANARY)[:16]}…")
    print("═" * 78)

    root = find_pec_root()
    if root is None:
        print("❌ 找不到 PEC 真树 —— 四案读数轴测不了。fail-closed：不出一张只有半边的矩阵。")
        return 2
    print(f"  PEC 根：{root}\n")

    todo = [m for m in MUTATIONS if not args.point or m["id"] in args.point]
    rows: list = []

    # ── 基线 ────────────────────────────────────────────────────────────────
    if args.coverage_only:
        print("── 基线：跳过（--coverage-only）────────────────────────────────")
        print()
        return _coverage_section(rows, True)

    print("── 基线（未变异）────────────────────────────────────────────────")
    base_rc, base_fails = run_canary(HERE)
    base_real = run_real(TOOL, root)
    print(f"  金丝雀 rc={base_rc} · 失败 {len(base_fails)} 例")
    for tag, (rc, s) in base_real.items():
        print(f"    {tag}: rc={rc} | {s}")
    if base_rc != 0:
        print("\n❌ 基线金丝雀就不是绿的 —— 先修基线，再看变异（否则整张矩阵无法解释）。")
        return 2
    print()

    # ── 逐点变异 ────────────────────────────────────────────────────────────
    rows = []
    for m in todo:
        src = TOOL.read_text(encoding="utf-8")
        n = src.count(m["old"])
        if n != 1:
            rows.append((m, "NOT-APPLIED", f"目标串出现 {n} 次（须恰 1 次）", None))
            print(f"❌ {m['id']:<22} MUTATION-NOT-APPLIED（目标串出现 {n} 次）")
            continue

        tmp = Path(tempfile.mkdtemp(prefix="vcx-mut-"))
        try:
            mutated = tmp / TOOL.name
            mutated.write_text(src.replace(m["old"], m["new"]), encoding="utf-8")
            shutil.copy2(CANARY, tmp / CANARY.name)

            rc, fails = run_canary(tmp)
            real = run_real(mutated, root)

            changed = {tag: (rc_, s) for tag, (rc_, s) in real.items()
                       if base_real.get(tag) != (rc_, s)}
            guarded = (rc != 0)
            row_verdict = ("✅ 已守" if guarded
                           else ("⚠️ 目标格（无守卫 ∧ 改读数）" if changed else "⚪ 惰性（无守卫 ∧ 未改读数）"))
            rows.append((m, "OK", row_verdict, (guarded, changed, fails)))

            print(f"{'✅' if guarded else ('⚠️' if changed else '⚪')} {m['id']:<22} "
                  f"守卫={'有' if guarded else '**无**'} · 真案读数{'变了' if changed else '未变'} · {row_verdict}")
            if args.verbose:
                if fails:
                    print(f"     被逮于：{'; '.join(fails[:3])}{' …' if len(fails) > 3 else ''}")
                for tag, (rc_, s) in changed.items():
                    print(f"     {tag}: rc={rc_} | {s}")
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    # ── 矩阵汇总 ────────────────────────────────────────────────────────────
    print("\n" + "═" * 78)
    print("汇总矩阵")
    print("═" * 78)
    print(f"{'id':<24}{'守卫':<8}{'改读数':<10}判定")
    for m, status, verdict, payload in rows:
        if status != "OK":
            print(f"{m['id']:<24}{'—':<8}{'—':<10}{verdict}")
            continue
        guarded, changed, _ = payload
        print(f"{m['id']:<24}{'有' if guarded else '无':<8}{'是' if changed else '否':<10}{verdict}")

    targets = [m["id"] for m, st, v, _ in rows if st == "OK" and not v.startswith("✅")]
    hard = [m["id"] for m, st, v, _ in rows if st == "OK" and "目标格" in v]
    print()
    print(f"  已扫 {len(rows)} 点 · 有守卫 {sum(1 for m, st, v, _ in rows if st == 'OK' and v.startswith('✅'))} 点"
          f" · 无守卫 {len(targets)} 点（其中**改真案读数** {len(hard)} 点）")
    if hard:
        print(f"  ⚠️ 目标格：{' · '.join(hard)}")
    not_applied = [m["id"] for m, st, _, _ in rows if st != "OK"]
    if not_applied:
        print("  ❌ 有变异未生效（MUTATION-NOT-APPLIED）—— 该点本次**未被真正扫描**，不得计入结论。")
        # ★ 承**未参与实施的独立复验方**（2026-09-27 首轮）：本条原先**只打印不反映到退出码**
        #   ⇒ 脚本化调用（`scan && echo ok`）会把「一个点都没真扫」当成成功。现计入 rc。
        print(f"     （退出码将因这 {len(not_applied)} 条非 0）")

    # ── 点类登记表（结构层）─────────────────────────────────────────────────
    print()
    cov_rc = _coverage_section(rows, False)

    # rc 语义：1 ＝ ① 存在目标格（无守卫 ∧ 改读数）· ② 存在未生效的变异（本次扫描不成立）
    #              ③ **点类登记表判红**（锚串漂移 / 形态数低于下限 / 未归属判据点超上限 /
    #                 存在未登记点类的变异）。
    return 1 if (hard or not_applied or cov_rc) else 0


if __name__ == "__main__":
    sys.exit(main())
