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

**跑之前先跑它的金丝雀**：`python3 test_verify_citations.py`（**21 例 · 改判据前必跑**）

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
（**⚠ 上句是 2026-09-26 的状态。见下节——2026-09-27 修掉两处判据缺陷后，越界闸已可当真闸用。**）

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

**⚠⚠ 2026-09-27 二轮独立复验判 `FAIL` —— 上一句「越界闸已可用」过强，本工具定级回到「提示器」**
二轮复验（另一位未参与实施的审核者）逮出 **10 项**，其中 **3 项是本轮修复自己新引入的**。
**⇒ 实施者已停止自行修补**（同 09-26 那条经验：同一方案连改三轮会累积新错）。**以下四条为未闭项：**

  1. **fail-closed 第四闸误诊并吞红（本轮新引入）**：「解析到引用却一处没落进本案语料」⇒ exit 2。
     但**一个「只引别案材料」的件，语料是对的**，会被判成「`--corpus` 指错」；且它在**打印前返回**，
     把 `all` 下本该出的「裸简写无法归属」／越界红**一并吞掉** ⇒ 人会去改路径而不是改件。
  2. **兜底门限对「已解析到 `--extra`」的引用误红（本轮新引入）**：修法①（归属落 extra）时仍拿
     **本案**最长件当门限 ⇒ `311 > 本案最长件` 即误红。**这与下面「使用约定」写的
     「跨案全路径 = WARN，不判越界」直接矛盾**；同型四位数反而被年份过滤放行 ⇒ **两个方向都测错对象**。
     **金丝雀 `P1` 现为红，即为本条。**
  3. **★ 目标错误在 carry 够长时零信号（判据效力）**：本工具的**存在理由**是抓 `清单 :311-318` 这类。
     实测：当「全文最近前置文件名」恰好**够长**时，owner 被误指到那个长件、门限随之抬高 ⇒
     **该错完全不报（连一行提示都没有）**。⇒ 上面那句「越界闸已可用」在这条上**不成立**。
  4. **`src=全文前置` 的归属该不该继承该文件长度**——这是 3 的根因，属**归属规则设计**，未自决。

**⚠ 归 Doctor 裁的是「方向」、不是「再改一版」**：1／2 要动判据设计，3／4 要动归属规则。
**在裁之前：只用本工具的提示，不得据其绿放行**；`起手包 §七 2.5` 已按此改口径。

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

**配套守卫测试**：`brain/.tools/test_verify_citations.py`（**21 例 · N/F/P/R 四组**）。
**纪律：改本文件判据前先跑它；新增判据必须同时补一对 N（该报）+ P（不该报）**——
只补 N，闸会慢慢退化成「总在报红」的噪声源。**R 组（真树回归）跳过时，汇总行会显式标「R 组未跑」**，
不让守卫静默消失。

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
DATEISH = re.compile(r"(1[0-9]{3}|20[0-9]{2})\s*[-–—/.]\s*(\d{1,2})(?:\s*[-–—/.]\s*(\d{1,2}))?")


def strip_dates(span: str) -> str:
    """把 span 里的日期串（YYYY-MM[-DD]，且月/日在合法域内）抹成空格，再交给 CITE。"""
    def repl(m: re.Match) -> str:
        mo, dd = int(m.group(2)), m.group(3)
        if 1 <= mo <= 12 and (dd is None or 1 <= int(dd) <= 31):
            return " "
        return m.group(0)
    return DATEISH.sub(repl, span)


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
            for m in CITE.finditer(strip_dates(span)):
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
    if not target.exists():
        print(f"❌ --target 不存在：{target}\n   fail-closed：读不到件，拒绝出绿。", file=sys.stderr)
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
        return any(str(p).startswith(str(r)) for r in corpus)

    # 本案语料 basename → 行数（行级 OR 用；避免逐行 rglob）
    # ★ 2026-09-27 修复（缺陷⑤「同名件两套取法不一致」· 承独立复验 P6）：
    #   原先 `resolve()` 取 `rglob()[0]`（**目录序**）、这里取 `sorted(rglob)` 的 `setdefault`（**字典序**），
    #   同一 basename 有两个件时**两处指向不同文件** ⇒ 门限按**无关件**算，可放行真越界。
    #   真实语料里并不罕见：CS-05 有 **9 个 `README.md`**，CS-01/02/03 各 2 个。
    #   修法＝**歧义 basename 不进行级 OR**，退回 owner 自身长度（取更紧的那把尺）。
    _seen: dict[str, Path | None] = {}
    for p in corpus_files:
        _seen[p.name] = None if p.name in _seen else p
    corpus_len: dict[str, int] = {k: len(load_pre(v)) for k, v in _seen.items() if v is not None}
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
    pairs_by_line: dict[int, list] = {}   # 行 → [(owner, path, a, b)]（引文对拍按行聚合）

    for lineno, owner, a, b, src, line in parse_citations(lines):
        total_cites += 1
        path = resolve(owner, resolve_roots) if owner else None
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
            warns.append(f"L{lineno} 引 `{owner}` —— 落在 **--extra（非本案语料）**，本行按兜底判据")
        else:
            checked += 1
            pairs_by_line.setdefault(lineno, []).append((owner, path, a, b))

        # ── 越界闸（任何引用都过闸，两档门限）──
        # ★ 2026-09-27 修复（缺陷⑥「归属失败的引用整行不查越界」· 承独立复验 P3 —— **本轮自己引入的回归**）：
        #   修前把越界检查挪到三个 `continue` 之后 ⇒ **文件名写错 / 粘标点 / 裸简写**全部只落 WARN、
        #   退出码 0 —— **恰恰是要拦的形态被放过了**。现改为：
        #     ① 归属落在本案语料内 → **行级 OR**（紧：本行被引文件的最长者）
        #     ② 归属失败 / 落在 --extra / 无法归属 → **兜底门限＝本案语料最长件**（松，宁可漏不可误报）
        if in_corpus_hit:
            lens = line_files_lens(line)
            allowed = max(lens) if lens else len(load_pre(path))
            where = f"owner={owner} · 归属来源={src}"
        else:
            allowed = _maxlen
            where = f"owner={owner or '未归属'} · 归属来源={src} · **兜底判据**"
        if allowed:
            for n in filter(None, (a, b)):
                if n > allowed:
                    msg = (f"L{lineno} **行号越界**：引 `:{n}`（{where}），"
                           f"但本行可解析的本案语料文件最长只有 {allowed} 行")
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

    # ★ fail-closed（缺陷⑦「指错但存在的目录」· 承独立复验 P1）：`--corpus` 指到一个**存在却指错**
    #   的目录（如把 `PEC/raw` 当成案语料）时，上面的 exists()／空目录两闸都拦不住——
    #   结果是**已核引用 0 处 · FAIL 0 · exit 0 · 「✅ 未发现越界与引文失据」**，
    #   即**缺陷④「路径写错反而全绿」的另一种、而且更可能发生的形态**。
    #   判据：**解析到了引用，却一处都没落进本案语料** ⇒ 拒绝出绿。
    if total_cites and not checked:
        print(f"❌ 解析到 {total_cites} 处引用，但**没有一处落进本案语料** ——"
              f"\n   几乎肯定是 `--corpus` 指错了目录（当前：{' · '.join(str(c) for c in corpus)}）"
              "\n   fail-closed：一条都没核到，此处的绿灯无意义。", file=sys.stderr)
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
