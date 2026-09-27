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
    python3 verify_citations.py --target <件.md> --corpus <dir> [--corpus <dir> ...] [--extra <件|dir> ...]

    --target   要核的研究件
    --corpus   **该案**的真源目录（可多次）；解析裸简写与判定「非本案语料」都靠它
    --extra    非本案但**正当引用**的件（别案 raw／GOTCHAS／起手包）。只参与解析、**不抬高越界门限**
    --gate     默认 all；**已交三案（旧体例）用 range**
    --quiet    只打结论行

**跑之前先跑它的金丝雀**：`python3 test_verify_citations.py`（**64 例 · 改判据前必跑**）

退出码：0 = 无 FAIL；1 = 有 FAIL（越界 / 引文不在所指行）；
**2 = 配置错误**（fail-closed · 四条：`--target` 不存在 · `--corpus` 不存在 · `--corpus` 无 .md ·
**解析到引用却一处都没落进本案语料**——最后一条防的是「`--corpus` 指到存在但指错的目录 ⇒ 全绿」）

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
| 已核引用 | 234 | 162 | 133→**138**（二轮复验实测订正） |
| FAIL | 22 | 15 | 26 |
| 其中假红（已分类） | ≥6 | 待分 | ≥20 |

**⇒ 现阶段的正确用法＝「提示器」，不是「闸」。判红必须先人核。**
（**⚠ 上句是 2026-09-26 的状态。下节记有两处判据缺陷的修法 —— 但「可当真闸用」这句已被推翻：
本工具当天即由二轮与四轮独立复验两次判 `FAIL`，**定级＝提示器**。请以紧接的下一段为准，勿单引本行。**）

**★ 2026-09-27 判据修复（两处缺陷 · 由负向测试逮出，非自审）**

负向测试（把两处真实跨案携带错按原样注回样本件）暴露：**本工具在 `range` 模式下，
两处真错一处都抓不到**。原表所谓「金丝雀全过」不假——但**金丝雀只测了不该报的不报，
没测该报的报不报**（守卫缺正向覆盖，G-X202 同型）。

  - **缺陷①「路径被吞」（已修 `NAME`）**：正则原为 `[^\s`/\\|]+\.md`，**排除 `/`**，
    于是本工具**自己规定的**「跨案引用写全路径」写法被**截成裸文件名**，再落到**本案同名件**上。
    实证：CS-09 件 L193 写 `CS-05_中华文明/共享基础/历史时间线.md:311`（写法完全合规）
    ⇒ 只取到 `历史时间线.md` ⇒ 落到本案 176 行的同名件 ⇒ **假越界**。
    **规则说「写全路径」，解析器却把路径丢掉**（G-X197 同型：口径词未在实现里落成定义）。
  - **缺陷②「corpus 级 OR 把闸抬到形同不存在」（已改为行级 OR）**：原判据＝
    「`--corpus` 内**最长**文件」——任何件够长就全体放行。实证 CS-09 corpus max=**559**
    （框架应用/A03），而真错 `清单:311-318` 的归属件只有 **146** 行 ⇒ **真越界不报**。
    该口径当初是为压 A 类假红引入的，代价却是**工具丧失存在理由**（它正是为抓这条而造）。
    ⇒ 改为「**本行出现的、且本案语料内可解析的文件**的最长者」。**不改成 owner 级**，
    是因为 owner 级会把 A 类假红放回来。

**修后实测（2026-09-27 · 四案 · `--gate range`）**：CS-05 / CS-02 / CS-01 **FAIL 0**；
CS-09 仍报 **2** 条，均在 **L193**——那是**把错误原文的行号放进反引号复述**的 `:311` 与 `:318`
（**订正**：首版写作「用引号转述」，归因不准 —— 触发的是**反引号**，不是 `「」`，见下节）。
**⇒ 越界闸已可用；「带留痕复述的件」仍会产红，是当前唯一的已知红源。**
（**⚠ 此句当日即被判「过强」并已订正 —— 见紧接的下一段；保留原文以留痕，勿单引。**）

**⚠⚠ 2026-09-27 二轮独立复验判 `FAIL` —— 上一句「越界闸已可用」过强，本工具定级回到「提示器」**
二轮复验（另一位未参与实施的审核者）逮出 **10 项**，其中 **3 项是本轮修复自己新引入的**。

**⚠ 同日修 6 项；余 1 项（③ 的**检测面**）未闭 —— 它已拆半：零信号那半已修，判不判得出那半需动归属规则（归 Doctor）**
**全表见** `brain/logs/checkpoints/2026-09-26_D4重跑起手包.md` §三「二轮未闭项」。**摘要**：
  1. **已闭合** — **fail-closed 第四闸误诊并吞红**：判据由「按 **basename** 找本案同名件」改为
     「**在所有给的根（corpus ∪ extra）里一处都解析不到**」——**与 `resolve()` 同用一把尺**
     （旧版两把尺不一致，正是四轮复验 E6/E7 两个反例的共同根因）。把判据改回旧口径，`N6` 与 `F6`
     **两条一起红**；「返回前先打 FAIL、不吞红」另配 `F4` 断言。守卫 `N5`·`N6`·`F4`·`F6`。
  2. **已闭合** — **兜底门限误红 `--extra` 引用** → **已解析到 extra 的引用按那一件自身长度判**。守卫 `P1`（**已由红转绿**）。
  3. ⚠ **部分闭合（检测面 · WARN 级）** — **目标错误在 carry 够长时零信号**：承 Doctor 令「加」，
     新增**散文名绑定**（`prose_candidates`）——取件名（去 `.md`）的**最长后缀**，看它是否出现在引用**前面的散文窗口**（12 字）里（**后缀须占件名 ≥1/3**）；命中即为候选，行号**超出可辨认候选中最长的**则报 WARN 并列出候选与行数。
     **刻意只出 WARN、不改红/绿**（绑定是启发式，升 FAIL 会把「猜错」变成「假红」——本工具一路栽过的坑）。
     **实证**：四轮复验的 E1 形状（`清单 \`:311-318\``）**被抓到**；四案实测**零假阳**
     （CS-05/02/01 = 0，CS-09 = 2、**两条正落在已知出错的 L193**）。
     ⚠ **真案回归另逮一型（比「夹带」更硬）**：`sn[:30] in qn` 在**被引行是空行**时 `sn[:30]==""`、**`"" in 任意串` 恒真** ⇒ **指向空行的引用此前一律被静默放行**；真案 CS-02 实测 **9 处**。现**分开报「被引行是空行」**（WARN、不改判决）。
     ⚠ **首版假阳现场修**：词元原为 `[0-9A-Za-z_一-鿿]{2,}`，散文里的 `CS-02` 让 `02` 匹配上
     `A02_a8_v3_多极并立阶段.md` ⇒ 真案 CS-09 L323 造出假阳；规约改 **CJK≥2 字 / 纯 ASCII≥4 字符**。
     另附「零信号」半：汇总行报**弱归属计数**＋说明该型靠绑定提示、不判 FAIL。守卫 `N7`·`P13`·`P12`。
  4. **同名件随目录序** → 歧义名**取最短件**（与 `resolve` 解耦）＋ `resolve` 的 hits 排序。守卫 `P7`。
  5. **`strip_dates` 吞合法四位数区间** → 日期判据改**三段式** `YYYY-MM-DD`。守卫 `P9`。
  6. **`--target` 指目录 rc=1** → 纳入 fail-closed，**rc=2**。守卫 `F5`。
  7. **`in_corpus` 前缀塌缩** → 改**路径相对性**判（`is_relative_to`）。守卫 `P11`。
**守卫有效性不是自述**：把每处判据**改回坏的**跑全量金丝雀，**7/7 都由对应那一条守卫报红**（无一恒真）。

**⚠ 但定级仍为「提示器」、不是「闸」**：本轮修的是**已发现的**缺陷；`all` 的引文闸**在新体例件上仍无实测样本**，
且两条**已知代价未消**——① 同行 span 内「引」与「提」机器分不出（行级 OR 仍可能被无关件名抬高）；
② **四位数行号的越界降 WARN 会漏**。⇒ **红仍须人核、绿不能当通过**；`起手包 §七 2.5` 已按此改口径。
**本场七项修复待独立复验（实施者不自签）。**

**★ 同日二轮：独立复验又逮出三处（含一处**本轮自己引入的回归**）**

  - **缺陷③「日期被当行号」**：`updated: 2026-05-15` 被 CITE 匹配成 `: 2026-05`，
    再经 a>b 交换变成**行号区间 `:5-2026`**——一条日期造两条噪声，其中 `:5` 还**可能真判越界**。
    原「四位数前置过滤」只把 2026 降 WARN，**没治住 `:5` 那半截**。
    ⇒ 修法＝**找引用之前先把日期串抠掉**（`strip_dates`），而不是事后过滤数字；
    判据必须「像日期」（月 1–12、日 1–31），否则 `1588-16` 这类**合法四位数行号区间会被误吞**。
  - **缺陷④「空语料 fail-open」（最危险的一处）**：`--corpus` 指向**空目录或没有 .md 的目录**时，
    全部引用走「无法归属」WARN ⇒ **FAIL 0 · exit 0**——**路径写错反而全绿**；
    这比报错更坏：它让人以为核过了。⇒ 加 fail-closed（退出码 **2**）硬停。
    （**订正**：指向**完全不存在**的路径时旧版是**未捕获 traceback**（rc=1），不是 exit 0——
    fail-open 的实锤是「存在但为空」那半。**独立复验实测补正。**）
    **本条是"正常路径 exit 0 不证明 fail-fast"的现场注脚。**
  - **缺陷⑤「同名件两套取法不一致」**：`resolve()` 取 `rglob()[0]`（目录序）、`corpus_len` 取
    `sorted(rglob)` 首位（字典序）⇒ 同 basename 有两个件时**两处指向不同文件**，门限按**无关件**算。
    真实语料并不罕见（CS-05 有 **9 个 `README.md`**）。⇒ 歧义 basename **不进行级 OR**，退回 owner 长度。
  - **缺陷⑥「归属失败的引用整行不查越界」（★ 本轮自己引入的回归）**：把越界检查挪到三个
    `continue` 之后 ⇒ **文件名写错 / 粘标点 / 裸简写**全部只落 WARN、退出码 0——
    **恰恰是要拦的形态被放过了**。⇒ 改为**两档门限、任何引用都过闸**（见下）。
  - **缺陷⑦「指错但存在的目录」**：`--corpus` 指到一个**存在却指错**的目录（如把 `PEC/raw`
    当成案语料）⇒ **已核 0 处 · FAIL 0 · exit 0 · ✅ 全绿**——缺陷④的**另一种、更可能发生的形态**。
    ⇒ 判据：**解析到了引用、却一处都没落进本案语料** ⇒ exit 2。

**越界闸的两档门限（2026-09-27 定 · 缺陷⑥的修法）**：
  ① 归属**落在本案语料内** → **行级 OR**（紧：本行被引文件的最长者）；
  ② 归属失败／落在 --extra／无法归属 → **兜底门限＝本案语料最长件**（松，宁漏不误报）。
  **为什么不能只用 ①**：只用 ① 会把「写错文件名」这类**最该拦**的形态整行放过；只用 ② 就是被
  缺陷② 证伪的旧口径。两档并存＝**紧的管能定位的、松的管定不了位的**。

**配套守卫测试**：`brain/.tools/test_verify_citations.py`（**64 例 · N/F/P/R 四组**
——⚠ 承复验方：**N 类与 P 类成对相邻放置，故 P 段内亦含 `N*` 例**，分组名与段落名不完全重合）。
**配套变异扫描台**：`brain/.tools/mutation_scan_verify_citations.py`（定向变异 × 金丝雀转红？× 四案读数变？
＋ **点类登记表**：每类写明落点锚串与形态下限，并用 AST 数出本件的判据点、报**未归属数**
——⚠ **未归属不等于缺陷，它是「没想到要扫」的可见化**；改动本件判据点结构须复测该基线）。
**纪律：改本文件判据前先跑它；新增判据必须同时补一对 N（该报）+ P（不该报）**——
只补 N，闸会慢慢退化成「总在报红」的噪声源。**R 组（真树回归）跳过或部分跳过时，汇总行会显式标
「R 组 n/4」**（承六轮复验订正：先前写「R 组未跑」，实际字面是 `R 组 0/4`），不让守卫静默消失。

**三类假红现状**：
  - **A · 跨行 carry**：修后**已被行级 OR 吸收**（CS-05「**已核引用 234 处**」实测 0 假红。
    **订正**：首版写「256 处」有误——256 是**解析到的引用总数**、234 才是「已核」数，两个量不是一回事）。
    ⚠ 「按**格**作用域」仍是未做的正解——行级 OR 是**更粗的压制**。
    **代价（2026-09-27 二轮订正，比首版记的更宽）**：并非只限「同行跨件」，而是
    **本行反引号 span 内只要出现任何够长的件名，整行即放行**——**包括明文撇清的提及**
    （实测 `…另与 \`长件.md\` 无关` 照样抬高门限）。已收窄为**只认 span 内的件名**
    （散文里的提及不再算），但 **span 内「引」与「提」机器分不出** ⇒ 这条漏面**结构性存在**，
    只能靠体例。**故行级 OR 是「比 corpus 级紧、比 owner 级松」的折中，不是正解。**
  - **B · 年份被当行号**：**已修**——见下**缺陷③**（改为「先抠日期串再找引用」，不再靠事后过滤数字）。
  - **C · 别案行号未写全路径**：**已随缺陷①整条修正**——写全路径者不再被误判；
    仍写裸文件名并落到本案同名件者，**报红保留**（该红是对的，见「使用约定」）。

**一类真错但被归成假红**：**引号在件里两用**（逐字引录 ＋ 作者转述/标签），本工具无法区分，
于是把「被搬形制／被引文本」「≥2 个不同处境下的重新选中」「Nelson 殉道符号」这类**转述**判成「引文失据」。
**⇒ 这是体例问题，不是工具问题**：要让「引文不在所指行」这道闸真正可用，**必须先让「引录」在版面上机器可识别**。
**✅ 该体例已裁（2026-09-26 Doctor）**：**逐字引录必须紧跟一个 `` `文件:行号` ``、「…」紧接其后；
转述／标签／强调一律不加引号（裸写即可）**；**自下一案起适用，已交三案（CS-01/02/05/09）不动**。
出处＝`brain/logs/checkpoints/2026-09-26_D4重跑起手包.md` §三 引录体例。
**⚠ 本段原写「该体例裁量归 Doctor」——2026-09-27 实核已裁、系 stale 断言，已订正。**
**⚠ 同一根因也咬越界闸**：**复述错误原文**的行（如 CS-09 L193 的留痕）会把被复述的 `:311-318`
当成本件引用 ⇒ 报越界。
**⚠ 本段原写「该形状在新体例下被治住」——2026-09-27 二轮独立复验实测证伪，已订正**：
把 CS-09 L191–193 的 `「清单 \`:311-318\`」` **只**去掉 `「」`、其余逐字不动 ⇒ **仍报 FAIL 2、两条都在 L193**。
**红的触发器是「反引号包着的 `:NNN`」，而体例管的是 `「」`** ⇒ 一件**完全遵守新体例**的留痕行
**照样会红**。**故「新案就不会撞上」是错的**；新案会撞上，须人核确认是「复述」还是「真引用」。
（**要不要让解析器跳过「引述/初稿/留痕」语义词后的 span？** 属**方法裁定** ⇒ 归 Doctor，本轮未自决。）

**一条使用约定（2026-09-26 立 · 2026-09-27 订正措辞）**：**正当的跨案引用应写「全路径」**（如
`CS-05_中华文明/共享基础/历史时间线.md:311`），并把该案语料传入 `--extra`。
2026-09-27 之前，写全路径**同样被误判**（解析器吞路径，见缺陷①）；修后该写法**被正确识别为
「非本案语料」**（WARN，不判越界）。仍写裸文件名者会被解析到**本案**的同名文件，
`:311` 超出本案长度 ⇒ 报「行号越界」——**这个报红是对的**（它确实指向本案之外）。
**件的写法决定闸的读数。**

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
# ★ 2026-09-27 修复（Bug-1「路径被吞」）：原式 `[^\s`/\\|]+` **排除 `/`**，于是本工具自己
#   规定的「跨案引用写全路径」写法（见文末「使用约定」）被**截成裸文件名**，再被解析到
#   **本案的同名件**上，造出假越界。实证：CS-09 件 L193 写 `CS-05_中华文明/共享基础/历史时间线.md:311`
#   （写法完全合规），原式只取到 `历史时间线.md` ⇒ 落到本案 176 行的同名件 ⇒ 报越界。
#   **规则说「写全路径」，解析器却把路径丢掉**——规则与实现口径不一致（G-X197 同型）。
NAME = re.compile(r"([^\s`\\|]+\.md)")

# ★ 2026-09-27 修复（Bug-3「日期被当行号」）：`updated: 2026-05-15` 这类 frontmatter 行会被
#   CITE 匹配成 `: 2026-05` ⇒ 再经 a>b 交换变成**行号区间 `:5-2026`**——一条日期造出两条噪声，
#   其中 `:5` 还可能真的判越界。原「四位数前置过滤」只是把 2026 降为 WARN，**没治住 `:5` 那半截**。
#   修法＝**在找引用之前先把日期串抠掉**，而不是事后过滤数字。
#   ⚠ 判据必须是「像日期」而非「四位数-两位数」：`1588-16`（月=16 不合法）不算日期、不得抠，
#     否则合法的四位数行号区间会被误吞。
#   ★ 2026-09-27 二次修复（承三轮复验 B8）：**要求三段式 `YYYY-MM-DD`**。上一版允许两段式，
#     于是 `:1905-12` 这类**合法的四位数行号区间**被当成日期整段抹掉（实测连 WARN 都没有）。
#     两段式日期（`2026-05`）仍会被读成区间，但经四位数过滤只降 WARN —— **如实留此残留**。
DATEISH = re.compile(r"(1[0-9]{3}|20[0-9]{2})\s*[-–—/.]\s*(\d{1,2})\s*[-–—/.]\s*(\d{1,2})")


# ── 散文名绑定（缺陷③b 的检测面 · 2026-09-27 Doctor 令「加」）────────────────────
# **为什么需要**：`清单 \`:311-318\`` 这类引用的**真身写在散文里、不在反引号内**，解析器绑不到 ⇒
#   原样**零信号**。这是本工具的存在理由那一型，也是四轮复验里唯一判「未闭」的检测面。
# **做法**：取引用**前面的散文窗口**，抽出词元，凡**语料件名（去 `.md`）包含该词元**者即为候选。
# **⚠ 刻意只出 WARN、不改红/绿**：绑定是启发式（两个不同件都可能含同一词元），
#   把它升成 FAIL 会把「猜错」变成「假红」，正是本工具一路栽过的坑。
#   **级别＝提示**：它把「零信号」变成「有人看得见的一行」，判不判得准仍归人。
PROSE_WINDOW = 12


def _ok_token(s: str) -> bool:
    """词元合格判据：CJK ≥2 字；**含 ASCII 则须 ≥4 字符**。

    ⚠ 两处都是现场踩出来的：**≥4** 挡掉 `02` 匹配 `A02_…`（CS-09 L323 假阳）；
    **≥2 CJK** 挡掉单字词元（如 `中` 匹配 `数据中台`）——单字在中文里命中率过高、必成噪声源。
    """
    if not s:
        return False
    if any(c.isascii() for c in s):
        return len(s) >= 4
    return len(s) >= 2


def prose_candidates(line: str, span_start: int, corpus_len: dict[str, int],
                     window: int = PROSE_WINDOW) -> list[tuple[str, int]]:
    """引用**前置散文窗口**里可能指代的语料件 → [(件名, 行数)]（**按行数降序**，最长者在前）。

    **做法（2026-09-27 二次修 · 承五轮复验 A2b）**：不用「切词元再找件」，改为
    **对每个件名（去 `.md`）取其最长后缀，看该后缀是否出现在散文窗口里**。

    **为什么换**：首版「切词元 → `tok in stem`」是**单向包含**，而中文散文常把件名与上下文**粘连**
    （`对照面见清单`、`CS-05 的时间线`）。首版在这两种写法下**静默不报**；真件 CS-09 L193 能被抓到，
    **只因原文恰好写成了 `「清单 `:311…`——引号＋空格给了分隔符**。⇒ **那是形态运气，不是能力**。
    后缀匹配天然处理粘连：`对照面见清单` 含 `清单`、`CS-05 的时间线` 含 `时间线`（⊂ `历史时间线`）。
    **排序改为按行数降序**：`_hi`（决定「超出可辨认候选」的那个）必须排在最前，否则 `[:4]` 截断会把它藏掉。
    """
    prose = line[max(0, span_start - window):span_start]
    hits: dict[str, int] = {}
    for name, L in corpus_len.items():
        stem = name[:-3] if name.endswith(".md") else name
        for k in range(len(stem), 1, -1):          # 从最长后缀往下试
            sub = stem[-k:]
            if not _ok_token(sub) or sub not in prose:
                continue
            # ★ 2026-09-27 三次修（承**自测复现的五轮复验同类假阳**）：还须「**词元占件名相当比例**」。
            #   放宽粘连支持后，CS-05 立刻多出 2 条假阳——`核心`(2 字) 撞上 12 字的
            #   `03_大学中庸_四书核心.md`、`中华`(2 字) 撞上 18 字的 `A04_…_中华.md`；
            #   而 CS-05 是中华文明案，`中华` 满篇都是。⇒ 规约 `len(sub) * 3 >= len(stem)`：
            #   **短通用后缀撞长名 = 弱证据，弃**；`清单`⊂`文明基因清单`(2×3≥6) 这类同量级的保留。
            if len(sub) * 3 < len(stem):
                continue
            hits[name] = L
            break
    return sorted(hits.items(), key=lambda kv: (-kv[1], kv[0]))


def strip_dates(span: str) -> str:
    """把 span 里的**三段式日期**（YYYY-MM-DD，且月/日在合法域内）抹成空格，再交给 CITE。"""
    def repl(m: re.Match) -> str:
        mo, dd = int(m.group(2)), int(m.group(3))
        if 1 <= mo <= 12 and 1 <= dd <= 31:
            return " "
        return m.group(0)
    return DATEISH.sub(repl, span)


def parse_citations(lines: list[str]):
    """产出一串 (行号, 文件, 起行号, 止行号, 归属来源, 行文本, span 起点)。

    归属规则（与配方一致）：**同 span 内文件名 → 本行最近前置文件名 → 全文最近前置**。
    `span 起点` 供**散文名绑定**取「引用前面的散文窗口」用（见 `prose_candidates`）。
    """
    out = []
    carry: str | None = None      # 全文最近前置文件名
    for i, line in enumerate(lines, 1):
        line_name: str | None = None
        for sm in re.finditer(r"`([^`]+)`", line):
            span = sm.group(1)
            names = NAME.findall(span)
            if names:
                line_name = names[-1]
                carry = line_name
            for m in CITE.finditer(strip_dates(span)):
                a = int(m.group(1))
                b = int(m.group(2)) if m.group(2) else None
                if b is not None and a > b:
                    a, b = b, a
                owner = line_name or carry
                src = "span内" if names else ("本行前置" if line_name else ("全文前置" if carry else "无"))
                out.append((i, owner, a, b, src, line, sm.start()))
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
            # ★ 2026-09-27：`rglob` 顺序未定义（目录序）⇒ **同名件取哪个不可复现**。
            #   排序后再取，至少让同一输入的读数稳定（承三轮复验 A6）。
            hits = sorted(root.rglob(name))
            if hits:
                return hits[0]
    return None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", required=True)
    ap.add_argument("--corpus", action="append", required=True,
                    help="**本案语料**（可多次；**通常给整案目录** —— 只给 `共享基础/` 会让一批引用解析不到而整行跳过）。"
                         "越界门限**只在 --corpus 内取**。")
    ap.add_argument("--extra", action="append", default=[],
                    help="非本案但**正当引用**的件（如别案 raw、GOTCHAS、起手包）。**只参与解析、不抬高本案门限**，"
                         "并把这些件上的命中单列为「非本案语料」提示。"
                         "2026-09-26 实测：若把 extra 混进 --corpus，门限会被大的件抬高 ⇒ **闸变钝、真越界不报**。")
    ap.add_argument("--quiet", action="store_true")
    ap.add_argument("--gate", choices=["all", "range"], default="all",
                    help="all（**默认**）＝越界 ＋ 引文失据双闸——**体例已裁**（2026-09-26 Doctor："
                         "逐字引录须紧跟 `文件:行号`、「…」紧接其后；转述/标签/强调一律不加引号；"
                         "见 brain/logs/checkpoints/2026-09-26_D4重跑起手包.md §三 引录体例），"
                         "**自下一案起适用**，故新案按 all 跑。"
                         "range＝只把「行号越界」当 FAIL，其余降 WARN——**给已交三案（旧体例）用**，"
                         "它们按裁「不动」、不随新体例重写。"
                         "⚠ 2026-09-27 实测红数：all 在已交案上 CS-05 16／CS-02 15／CS-09 24／CS-01 0"
                         "（旧体例所致、非错），**在新体例件上尚无实测样本**——首个新案跑 all 时若红数异常，"
                         "先取一条原文对拍，再判是件错还是闸误。")
    args = ap.parse_args()

    target = Path(args.target)
    if not target.exists() or target.is_dir():
        why = "不存在" if not target.exists() else "是目录、不是件"
        print(f"❌ --target {why}：{target}\n   fail-closed：读不到件，拒绝出绿。", file=sys.stderr)
        return 2
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

    # ★ 越界判据（2026-09-27 **换口径：corpus 级 OR → 行级 OR** · Bug-2）
    #   原口径＝「--corpus 内**最长**文件」：任何件够长就全体放行 ⇒ **闸被最大的件抬高到形同不存在**。
    #   实证：CS-09 corpus max=559（框架应用/A03），而真错 `清单:311-318` 的归属件只有 **146** 行
    #   ⇒ **真越界不报**——而本工具当初正是为抓这条错而造（判据失效＝工具丧失存在理由）。
    #   新口径＝「**本行出现的、且在本案语料内可解析的文件**的最长者」（行级 OR）。
    #   **为什么不改成 owner 级**：owner 级会把「引录列的裸简写被同行后置文件名吸走」那类**假红**
    #   放回来（CS-05 实测 `学者谱系.md:1923` 实为时间线行号）。行级 OR 两端都挡。
    #   代价（如实记）：**同一行内「属 A 而 A 不够长、但同行 B 够长」的个案会漏** —— 宁漏不误报。
    corpus_files: list[Path] = []
    for root in corpus:
        corpus_files += sorted(root.rglob("*.md")) if root.is_dir() else [root]
    resolve_roots = list(corpus) + [Path(e) for e in args.extra]

    # ★ fail-closed（2026-09-27 · **故障注入**逮出，非自审）：空的／不存在的 `--corpus` 不得静默放行。
    #   实测：`--corpus <空目录>` 时全部引用走「无法归属」WARN、FAIL 0、**exit 0**
    #   ——**路径写错反而全绿**。闸的全部意义就是「不许说不出声地过」，故此处必须硬停。
    #   退出码 **2 ＝ 配置错误**（区别于 1 ＝ 有 FAIL），便于调用方分辨「件错」与「没跑起来」。
    missing = [c for c in corpus if not c.exists()]
    if missing:
        print("❌ --corpus 不存在：" + " · ".join(str(m) for m in missing)
              + "\n   fail-closed：语料缺失时判不了越界，拒绝出绿。", file=sys.stderr)
        return 2
    if not corpus_files:
        print(f"❌ --corpus 内没有可解析的 .md（给了 {len(corpus)} 个根）"
              "\n   fail-closed：空语料下每条引用都走「无法归属」，此处的绿灯无意义。", file=sys.stderr)
        return 2

    def in_corpus(p: Path) -> bool:
        # ★ 2026-09-27 修复（缺陷⑧「前缀塌缩」· 承三轮复验 B8）：原用 `str(p).startswith(str(r))`，
        #   于是 `--corpus .../A` 会把 `.../AB/...` 当成**本案**（`A` 是 `AB` 的**字符串**前缀）⇒
        #   既漏「落在 --extra」的提示、又**绕过第四闸**（fail-open 方向）。
        #   改用**路径相对性**判，不靠字符串前缀。
        try:
            rp = p.resolve()
        except Exception:
            rp = p
        for r in corpus:
            try:
                rr = r.resolve()
                if rp == rr or rp.is_relative_to(rr):
                    return True
            except Exception:
                continue
        return False

    # 本案语料 basename → 行数（行级 OR 用；避免逐行 rglob）
    # ★ 2026-09-27 修复（缺陷⑤「同名件两套取法不一致」· 承独立复验 P6）：
    #   原先 `resolve()` 取 `rglob()[0]`（**目录序**）、这里取 `sorted(rglob)` 的 `setdefault`（**字典序**），
    #   同一 basename 有两个件时**两处指向不同文件** ⇒ 门限按**无关件**算，可放行真越界。
    #   真实语料里并不罕见：CS-05 有 **9 个 `README.md`**，CS-01/02/03 各 2 个。
    #   修法＝**歧义 basename 不进行级 OR**，退回 owner 自身长度（取更紧的那把尺）。
    # ★ 2026-09-27 二次修复（缺陷⑤续 · 承三轮复验 A6/B-5）：上一版把歧义名**排除**出行级 OR，
    #   门限于是退回 `resolve()` 取到的那一个——而 `resolve()` 用**未排序**的 `rglob()[0]`，
    #   实测量到的是 400 行件而非更紧的 10 行件 ⇒ **同一行文本的红/绿由文件系统顺序决定**。
    #   修法两件：① 歧义 basename 取**最短件**（宁紧不松，且**与 resolve 的取法解耦**）；
    #   ② `resolve()` 的 hits 先排序，去掉不确定性。
    corpus_len: dict[str, int] = {}
    for p in corpus_files:
        _L = len(load_pre(p))
        corpus_len[p.name] = _L if p.name not in corpus_len else min(corpus_len[p.name], _L)
    _maxlen = max((len(load_pre(p)) for p in corpus_files), default=0)   # 兜底判据用

    def line_files_lens(line: str) -> list[int]:
        """本行**反引号 span 内**出现的、本案语料内**无歧义**的文件的**行数**，降序。

        ⚠ 只取 span 内的名字（2026-09-27 收窄 · 承独立复验 P4）：原先对**整行原文**做
        `NAME.findall`，于是「同行只要出现任何够长的件名即整行放行」——**连明文撇清的提及也算**
        （实测 `…与 长件.md 无关` 会抬高门限）。收窄后与文档所述「本行被引文件」一致。
        """
        keys: set[str] = set()
        for span in re.findall(r"`([^`]+)`", line):
            keys |= {Path(n).name for n in NAME.findall(span)}
        return sorted((corpus_len[k] for k in keys if k in corpus_len), reverse=True)

    fails: list[str] = []
    warns: list[str] = []
    checked = 0
    total_cites = 0
    weak_total = 0              # 归属来源＝全文前置 的引用数（弱归属）
    weak_over_owner = 0         # 其中「该行号已超出全文前置认定的那一件」——最需人核的子集
    resolved_anywhere = 0       # 引用**在任何给的根里**（corpus ∪ extra）解析成功的次数（第四闸用）
    pairs_by_line: dict[int, list] = {}   # 行 → [(owner, path, a, b)]（引文对拍按行聚合）

    for lineno, owner, a, b, src, line, span_start in parse_citations(lines):
        total_cites += 1
        path = resolve(owner, resolve_roots) if owner else None
        if path is not None:
            resolved_anywhere += 1
        in_corpus_hit = path is not None and in_corpus(path)

        if owner is None:
            # ★ 2026-09-26 金丝雀逮出的门禁缺口：初版把此处降为 WARN，于是
            #   「引 `:311-318` 而全件从未出现任何文件名」这类**读者也无法定位**的引用
            #   被判绿。规约：**无法归属 = 件自身的缺陷**，报 FAIL。
            msg = (f"L{lineno} **裸简写无法归属**：引 `:{a}`"
                   + (f"-{b}" if b else "")
                   + "，但同行与全文均无前置文件名 ⇒ **读者也无从知道它指哪个文件**")
            (warns if args.gate == "range" else fails).append(msg)
        elif path is None:
            warns.append(f"L{lineno} 引 `{owner}` —— **不在 --corpus/--extra 内**（跨案引用？还是携带？）")
        elif not in_corpus_hit:
            warns.append(f"L{lineno} 引 `{owner}` —— 落在 **--extra（非本案语料）**，按其自身长度判")
        else:
            checked += 1
            pairs_by_line.setdefault(lineno, []).append((owner, path, a, b))

        # ── 越界闸（任何引用都过闸 · 三档门限）──
        # ★ 2026-09-27 二次修复（缺陷⑥续 · 承三轮复验 B1/B3）：
        #   ① 归属落在**本案语料内** → 行级 OR（紧：本行被引文件的最长者）
        #   ② 归属**已解析、但落在 --extra** → **用那一件自己的长度**
        #      （★★ 改正：上一版拿**本案**最长件当门限 ⇒ 写法完全合规的跨案引用会误红，
        #        `311 > 本案最长件` 就报——而 `:311` 在别案件里是合法行；**两个方向都测错对象**。）
        #   ③ **真·归属失败**（解析不到 owner／无 owner）→ 兜底＝本案语料最长件（松，宁漏不误报）
        if in_corpus_hit:
            lens = line_files_lens(line)
            allowed = max(lens) if lens else len(load_pre(path))
            owner_len = len(load_pre(path))
            where = f"owner={owner} · 归属来源={src}"
            budget = f"本行可解析的**本案语料**文件最长只有 {allowed} 行"
        elif path is not None:
            allowed = len(load_pre(path))
            owner_len = allowed
            where = f"owner={owner} · 归属来源={src} · 非本案语料"
            # ★ 承四轮复验 E5：原模板一律说「本行可解析的**本案语料**文件最长只有 N 行」，
            #   但这一档的 N 是**别案那一件自身**的长度 —— 文案自相矛盾（把别案长度说成本案语料长度）。
            budget = f"被引的那一件（非本案语料）自身只有 {allowed} 行"
        else:
            allowed = _maxlen
            owner_len = None
            where = f"owner={owner or '未归属'} · 归属来源={src} · **兜底判据**"
            budget = f"本案语料最长件只有 {allowed} 行"
        # ⚠ 弱归属计数（缺陷③ 的**可诚实交付的那半**）：本工具**无法**保证判出该型（见 summary 末行的自陈），
        #   但至少要让「这件里有多少引用是弱归属的」**可见** —— 零信号本身就是缺陷的一半。
        if src == "全文前置":
            weak_total += 1
        # ★ 散文名绑定（缺陷③b 的**检测面** · WARN 级、不改红/绿）：
        #   **触发条件＝该引用自身 span 里没有文件名**（`src != "span内"`）。
        #   ⚠ 承五轮复验 A2b：首版只认 `src == "全文前置"`，于是**行内任何更早的 span 出现件名**
        #     就会把 `src` 变成「本行前置」⇒ **整条绑定不跑**（同一条引用，只多一个无关 span 即静默）。
        if src != "span内":
            _cands = prose_candidates(line, span_start, corpus_len)
            if _cands:
                _hi = max(L for _, L in _cands)
                _shown = " · ".join(f"`{nm}`（{L} 行）" for nm, L in _cands[:4])
                _more = f" …等 {len(_cands)} 件" if len(_cands) > 4 else ""
                for n in filter(None, (a, b)):
                    if n > _hi:
                        warns.append(
                            f"L{lineno} **散文名绑定·超出可辨认候选**：引 `:{n}`，引用前的散文词可对应 "
                            f"{_shown}{_more}，该行号**超出这些候选中最长的**（{_hi} 行）⇒ "
                            "请人核这一处指哪个文件（可能正是要找的跨案携带错）")
                        # ⚠ 文案改「可辨认候选」（承六轮复验 D-1）：候选集**经过筛选**（见
                        #   `prose_candidates` 的 ≥1/3 规则 ＋ 12 字窗口），旧文案写「全部候选」是**过强**——
                        #   一个被筛掉的**更长**同缀件会让这条提示把人引向错的件。逐条附「局限见汇总」。
                    # ★ 五轮复验**删支**：原本还有一档「超出**部分**候选」（`n > _lo`），
                    #   实测**一个 3 行的同名桩件就能让 `n=4…200` 全部报** ⇒ 把提示通道淹没
                    #   （正是缺陷⑨当初栽过的形态）。**只留「超出全部候选」这一高档**，宁漏不误报。
        if allowed:
            for n in filter(None, (a, b)):
                if n > allowed:
                    msg = (f"L{lineno} **行号越界**：引 `:{n}`（{where}），但 {budget}")
                    # ★ 年份过滤（2026-09-26 实测假红类 B）：行文里的 `：1588`／`：1805`／`：2026`
                    #   是**年份**，不是行号。判据＝**四位数（≥1000）且超出可解析长度** ⇒ 降 WARN。
                    #   真日期串已由 `strip_dates` 先行抠掉，这里管的是「像年份但不构成日期」的残例。
                    #   ⚠ **代价（如实记）**：**四位数行号的「跨案携带」会漏**（如把 CS-05 的 `:1923`
                    #     搬进一个 300 行的语料）。该型**只能靠体例治**——引录须紧跟全路径 `文件:行号`，
                    #     拿不准的一律人核。**宁漏不误报**是本闸的既定取向。
                    if n >= 1000:
                        warns.append(msg + " ——⚠ **疑似年份／编号**（四位数），降为提示")
                    else:
                        fails.append(msg)
                elif src == "全文前置" and owner_len is not None and n > owner_len:
                    # ★ 缺陷⑨ 的**收敛版**（自测收窄）：首版是**无条件**对每条 `src=全文前置` 的引用
                    #   发 WARN —— 实测占 CS-02 全部 WARN 的 **67–76%** ⇒ **把提示通道淹了**。
                    #   收敛为**只在「弱归属确实改变了判决」时报**：按「全文前置」认定的那一件
                    #   **本应判越界**，却被同行另一件／本案门限放过了。
                    #   ⚠ 四轮复验正告：**这条触发器与缺陷③的原型（carry 够长）互斥、按构造不可能触发** ——
                    #   它现在补的是「另一种形状」，**不是** ③ 本身；③ 的检测面仍未闭（见 summary 末行）。
                    weak_over_owner += 1
                    warns.append(
                        f"L{lineno} **弱归属放行**：引 `:{n}`（owner={owner} · 归属来源＝全文前置），"
                        f"该行号**已超出「全文前置」认定的那一件**（{owner_len} 行），"
                        f"是**同行的另一件（最长 {allowed} 行）把它放过的** ⇒ "
                        "**请人核这一处到底指哪个文件**（可能正是要找的跨案携带错）")

    # ★ 承五轮复验 HIGH#1「第四闸残余 fail-open」＋ 六轮复验 A4：
    #   错语料里只要有**一个同名的长件**碰巧解析，上面的合取就被解除 ⇒ 回到 `已核 1 处 · FAIL 0 · rc=0 · ✅`
    #   （＝缺陷⑦ 的同一张脸）。**不改硬判**（会与「只引 extra 的正当件」打架），改为**显著提示**。
    #   ⚠⚠ 修法二改（六轮复验逮出）：首版把提示 append 进 `warns` ⇒ **`--quiet` 下被整片吞掉**、
    #   该形态在 `--quiet` 下仍是 `rc=0 · ✅ · 零信号`（本工具推荐用法之一就是 `--quiet`）。
    #   ⇒ 移到**汇总行常显**（见下方 `已核引用 …（本案覆盖率 …）`），**不再依赖 WARN 列表**。
    low_coverage = bool(total_cites >= 5 and checked * 2 < total_cites)

    # ★ fail-closed（缺陷⑦「指错但存在的目录」· 承独立复验 P1）：`--corpus` 指到一个**存在却指错**
    #   的目录（如把 `PEC/raw` 当成案语料）时，上面的 exists()／空目录两闸都拦不住——
    #   结果是**已核引用 0 处 · FAIL 0 · exit 0 · 「✅ 未发现越界与引文失据」**。
    # ★ 2026-09-27 二次修复（缺陷⑩ · 承三轮复验 B2/B7）：上一版判据过宽且**吞红**——对
    #   「**一个只引别案材料的件**」也判「--corpus 指错」（**那是正当形态**），且它在打印前返回，
    #   把 `all` 下本该出的红**一并吞掉**。修法两件：
    #     ① **判据＝「一条都没核到，且在所有给的根里（corpus ∪ extra）一处都解析不到」**。
    #        ⚠ 承四轮复验 E6/E7 —— 上一版按 **owner 的 basename** 判「本案有没有同名件」，
    #        而 `resolve()` 是按**路径**找的 ⇒ **两把尺不一致**：错语料里恰有一个同名件
    #        （如 `README.md`）就能骗过它、回到 `rc=0 · ✅`（缺陷⑦ 被重新打开）；反过来，
    #        只引 extra 的件若引用名本案无同名（`GOTCHAS.md` 正是 extra 典型载荷）又会被误判 exit 2。
    #        **改用「解析到没有」这把与 `resolve()` 同一把的尺，两个反例同时被覆盖。**
    #     ② **先把已判出的 FAIL/WARN 打出来再返回** —— 不吞红。
    if total_cites and not checked and resolved_anywhere == 0:
        print(f"❌ 解析到 {total_cites} 处引用，但没有一处落进本案语料，"
              f"**且这些引用在给的所有根（corpus ∪ extra）里一处都解析不到** ——"
              f"\n   几乎肯定是 `--corpus` 指错了目录（当前：{' · '.join(str(c) for c in corpus)}）"
              "\n   fail-closed：一条都没核到，此处的绿灯无意义。", file=sys.stderr)
        if fails:
            print("\n  ❌ 返回前先报已判出的 FAIL（不吞红）：", file=sys.stderr)
            for f_ in fails:
                print("     " + f_, file=sys.stderr)
        if warns and not args.quiet:
            print(f"  ⚠ 另有 {len(warns)} 条 WARN（`--quiet` 下不展开）", file=sys.stderr)
        return 2

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
            if any(core in sn for _, _, sn in cands):
                continue
            # ★ 反向包含（承八轮复验 MEDIUM-2，2026-09-27 Doctor 裁「加 WARN、不改判决」）：
            #   判据里还有一条 `sn[:30] in qn`——**源行前 30 字 ⊂ 引文** ⇒ 放行。
            #   它本是给「引文带截断/省略号」用的，但**同时放行了「源行前 30 字 ＋ 任意编造续写」**：
            #   实测「源行前 30 字 + 90 字编造」判绿，而这条闸正是为抓跨案携带而造。
            #   **不收紧判据**（会误伤合法的截断引文）：改为**发 WARN**，只在引文**显著长于**
            #   被匹配片段（≥20 字）时才报——把「夹带编造续写」从隐形变可见。
            _rev = [(o_, n_, sn_) for o_, n_, sn_ in cands if sn_[:30] in qn]
            if _rev:
                o_, n_, sn_ = _rev[0]
                if len(sn_.strip()) == 0:
                    # ★★ 承**自测真案回归**逮出的另一型（比「夹带」更硬）：**被引行是空行**时
                    #   `sn[:30]` == ""，而 `"" in 任何串` **恒真** ⇒ 旧判据把「指向空行的引用」
                    #   **一律静默放行**。实测 CS-02 件 4 处（`学者谱系.md:107/169/218` 等）
                    #   即此型：引文写着具体内容、被引行却什么都没有。**分开报**，别混进「夹带」。
                    warns.append(
                        f"L{lineno} **被引行是空行**：引 `{o_}:{n_}`，但该行**归一化后为空**，"
                        "而本闸原按「源行前缀 ⊂ 引文」放行（空串恒真）⇒ **这类引用此前一直被静默放过**；"
                        "请人核该引文究竟出自哪一行")
                elif len(qn) >= len(sn_[:30]) + 20:
                    warns.append(
                        f"L{lineno} **引文夹带（反向包含放行）**：引 `{o_}:{n_}` 的引文比该行前 30 字"
                        f"**长出 {len(qn) - len(sn_[:30])} 字** —— 本闸按「源行前缀 ⊂ 引文」放行，"
                        "**故引文尾部可能含编造的续写**；请人核该引文是否逐字取自该行")
                continue
            where = " · ".join(f"`{o}:{n}`" for o, n, _ in cands)
            msg = f"L{lineno} **引文不在所指行**：本行引用 {where}，但均找不到 → 「{q[:44]}…」"
            (warns if args.gate == "range" else fails).append(msg)

    print(f"引文核验：{target.name}")
    print(f"  corpus: " + " · ".join(str(c) for c in corpus))
    _cov = f"{checked}/{total_cites}" if total_cites else "—"
    _low = ("  ⚠ **本案语料覆盖率过低（" + _cov + "）—— 先确认 `--corpus` 是否指对目录**"
            if low_coverage else "")
    print(f"  已核引用 {checked} 处（本案覆盖率 {_cov}）· FAIL {len(fails)} · WARN {len(warns)} · gate={args.gate}{_low}")
    # ★ 缺陷③ 的**可诚实交付的那半**：检测面仍未闭（见下），但「有多少引用是弱归属」必须可见 ——
    #   零信号本身是缺陷的一半，且是唯一现在还修得动的那一半（另一半要动归属规则，归 Doctor 裁）。
    if total_cites:
        extra = (f" · 其中 **{weak_over_owner} 处该行号已超出全文前置认定的那一件**（最需人核）"
                 if weak_over_owner else "")
        print(f"  弱归属（归属来源＝全文前置）{weak_total} / {total_cites} 处引用{extra}")
        print("  ⚠ **「carry 够长型」越界靠『散文名绑定』提示、不判 FAIL**：该型下 owner 被指到长件、"
              "门限随之抬高 ⇒ 越界闸**可能一行都不报**；绑定是从引用前的散文词去找语料件，"
              "**是启发式、会猜错**。**四条已披露的局限**（承五/六轮复验，逐条实测）："
              "① 候选集**经筛选**（后缀须占件名 ≥1/3、只看引用前 12 字窗口）⇒ 报出的「可辨认候选」"
              "**可能不是全部相关件**，`超出可辨认候选` **≠ 一定越界**；"
              "② 因此**覆盖与否部分取决于件名有多长**——同内容同写法，件名多几个字就可能**零候选、零提示**；"
              "③ **英文缩写前缀写法绑不到**（如 `A02_a8` 指 `A02_a8_v3_…`，首版词元法能、后缀法不能）；"
              "④ 名字被推出 12 字窗口即失效；"
              "⑤ **覆盖率提示的边界**：它对「只引 `--extra` 的正当件」会**误问一句**（那类件覆盖率天然低），"
              "且**有地板**——引用少于 5 处时**不报**；"
              "⑥ **候选集里混进无关的、够长的同缀件**时 `_hi` 被顶高 ⇒ 本提示**可能被整条压掉**（漏报方向）。"
              "**⇒ 弱归属占比高、或见到「散文名绑定」时，请回件对那几处 `文件:行号` 逐条实 grep。**")
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
