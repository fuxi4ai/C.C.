#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""verify_citations.py 的金丝雀 —— 「换案先归零」**提示器**的持久化守卫测试（只读）

> **⚠ 定级：本工具是「提示器」，不是「闸」**（2026-09-27 二轮独立复验判 `FAIL` 后由 Doctor 裁「留级提示器」）。
> **它的红要人核，它的绿不能当通过**——未闭项见 `brain/logs/checkpoints/2026-09-26_D4重跑起手包.md` §三。
> 本文件历史上称「门禁的守卫测试」；**改称提示器**是承三轮复验逮出「本文件自身无定级字样」而补的。

为什么有这个文件
----------------
`G-X161` 追记把「换案先归零」列为**必要动作**，`verify_citations.py` 是实现它的机械闸。
但 2026-09-27 的负向测试发现：**该闸在 `range` 模式下，两处真实跨案携带错一处都抓不到**，
根因两处（路径被吞 / corpus 级 OR 把闸抬高到形同不存在）。原文档所谓「金丝雀 4/4 全过」不假，
但**金丝雀只测了「不该报的不报」，没测「该报的报不报」**——守卫缺**正向覆盖**。

⇒ 本文件就是补这一课的：**每条断言都必须成对**——
  · **N 类（负向）**：把真实错按原样注进去，**闸必须报**（fail-closed）
  · **P 类（正向）**：把正常件放进去，**闸必须不报**（防误报把闸变成噪声源）

⚠ 纪律：**改 `verify_citations.py` 的判据，必须先跑本文件**；
   新增判据必须同时补一对 N/P 例，只补 N 会让闸慢慢变成「总在报红」。

**⚠ 本文件全绿 ≠ 工具闭合 —— 这是**守卫**的状态，不是**工具能力**的状态（2026-09-27）**
---
四轮复验判 `FAIL` 的那两处 HIGH，**同日已闭合**，但请连带读它们的**残留代价**：

  - **① 第四闸「指错目录」**：判据已改「在**所有给的根**（corpus ∪ extra）里**一处都解析不到**」
    ＝ **与 `resolve()` 同用一把尺**（旧版按 basename、与 resolve 的按路径**两把尺不一致**，
    正是四轮复验 E6/E7 两个反例的共同根因）。
  - **③ 目标错误零信号**：新增**散文名绑定**（引用前散文窗口抽词元 → 语料件名含之者为候选 →
    行号超出**可辨认候选中最长者**即报）。**⚠ 它刻意只出 WARN、不判 FAIL** —— 绑定是启发式（两件可能含同一词元），
    升 FAIL 会把「猜错」变成「假红」。**`N7` 守它必须报、`P13` 守它不许乱报。**
  - ⇒ **本文件全绿只说明「已覆盖的判据没被改坏」**；**工具的检出面仍是提示级：红须人核、绿不能当通过。**
  - 另记：**「把每处判据改回坏的、守卫全红」只在「整条修法删掉」这一种变异取法下成立** ——
    子改动子集里另有几处无守卫（四轮复验逮出），**故该结论不能当通说**。未闭项见
    `brain/logs/checkpoints/2026-09-26_D4重跑起手包.md` §三「二轮未闭项」。

用法
----
    python3 test_verify_citations.py            # 全跑
    python3 test_verify_citations.py -v         # 打印每例的输出

退出码 0 = 全过；1 = 有例不过。

夹具
----
本案语料与别案语料在临时目录里**合成**（不依赖 PEC 真树），故本文件可离线、可重复、快。
真树回归单列在最后一组（PEC 不在盘上则跳过该组）。
"""

from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

TOOL = Path(__file__).resolve().with_name("verify_citations.py")
VERBOSE = "-v" in sys.argv

_results: list[tuple[bool, str, str]] = []
# ★ 例数守卫（承五轮复验 J1a/J1b）：汇总行只报 `N/N`，**删掉几例不会被任何断言拦住**
#   （实测删 2 例仍 `29/29 通过 rc=0`），而四件文档到处写死具体例数（加此守卫时是 31，现已 34）。
#   ⇒ 钉住期望例数；**改例数必须同步改本常量与那四处文档**。
EXPECTED_CASES = 35


def run(target: Path, corpus: list[Path], extra: list[Path] | None = None,
        gate: str | None = None, quiet: bool = False):
    # ★ 承**七轮复验**：原先**没有 `quiet` 形参** ⇒ `F7`（守「覆盖率信号在 `--quiet` 下也必须在场」）
    #   实际测的是**非 `--quiet`** 输出，**对它点名的那个变异不响**（把覆盖率提示移回 `warns`
    #   ⇒ 金丝雀仍 35/35 全绿，而 `--quiet` 下该信号一个字都不打）。**一个不守的守卫比没有守卫更坏**：
    #   它把「我验过了」借给了一个没被验证的行为。
    cmd = [sys.executable, str(TOOL), "--target", str(target)]
    for c in corpus:
        cmd += ["--corpus", str(c)]
    for e in (extra or []):
        cmd += ["--extra", str(e)]
    if gate:
        cmd += ["--gate", gate]
    if quiet:
        cmd += ["--quiet"]
    p = subprocess.run(cmd, capture_output=True, text=True)
    return p.returncode, (p.stdout + p.stderr)


def check(name: str, ok: bool, detail: str = ""):
    _results.append((ok, name, detail))
    print(f"  {'✅' if ok else '❌'} {name}")
    if detail and (VERBOSE or not ok):
        for ln in detail.strip().splitlines():
            print(f"       {ln}")


def body(n: int, tag: str) -> str:
    return "\n".join(f"{tag} 第 {i} 行 —— 合成语料占位内容" for i in range(1, n + 1))


def main() -> int:
    tmp = Path(tempfile.mkdtemp(prefix="vcx-canary-"))
    try:
        case_a = tmp / "本案语料"          # 本案：长件 500 / 短件 10 / 谱系 20
        case_b = tmp / "别案语料"          # 别案：短件 900（与本案同名）
        case_a.mkdir(); case_b.mkdir()
        (case_a / "长件.md").write_text(body(500, "长"), encoding="utf-8")
        (case_a / "短件.md").write_text(body(10, "短"), encoding="utf-8")
        (case_a / "谱系.md").write_text(body(20, "谱"), encoding="utf-8")
        (case_b / "短件.md").write_text(body(900, "别案短"), encoding="utf-8")
        # 同名件歧义夹具（P7 用）：同案语料内两个同名件、长度差 40 倍。
        # ⚠ 刻意都短于 长件.md(500)，**不抬高本案 _maxlen**（否则会污染 N4 的兜底门限断言）。
        (case_a / "a").mkdir(); (case_a / "z").mkdir()
        (case_a / "a" / "同名.md").write_text(body(400, "同名A"), encoding="utf-8")
        (case_a / "z" / "同名.md").write_text(body(10, "同名Z"), encoding="utf-8")
        # 散文名绑定夹具（N7/P13）：`清单.md` 供「散文词 → 件名」命中；`A02_样件.md` 供假阳守卫
        # （散文里的 `CS-02` 曾让词元 `02` 匹配上它 ⇒ 首版假阳现场）。
        (case_a / "清单.md").write_text(body(20, "清单"), encoding="utf-8")
        (case_a / "A02_样件.md").write_text(body(30, "A02"), encoding="utf-8")
        samples = tmp / "samples"; samples.mkdir()

        def sample(fn: str, text: str) -> Path:
            p = samples / fn
            p.write_text(text, encoding="utf-8")
            return p

        print("\n══ N 类 · 负向（闸必须报）══")

        # N1 真错②形状：**文件名在正文／行号是裸简写**（09-26 真错原形：
        #    「对照面见 **清单 `:311-318`**」——名字在散文里、简写在反引号里）。
        #    ⚠ 引用只在**反引号 span 内**才被解析（设计如此），故夹具必须还原这个形态。
        s = sample("N1.md", "本案的清单是 `短件.md`（共 10 行）。\n对照面见 清单 `:200` 的那一段。\n")
        rc, out = run(s, [case_a], gate="range")
        check("N1 裸简写越界 → 判 FAIL（真错②必须抓到）", rc == 1 and "行号越界" in out,
              f"rc={rc}\n{out}")

        # N2 真错①形状：跨案携带的引文（行号在本案存在、内容不是那行）
        #    写法取旧体例（引录带引号但不紧跟 `文件:行号`），正是 09-26 出事那一处
        s = sample("N2.md", "本例引 `谱系.md:5`「本谱系强制引入非盎格鲁视角」的表述。\n")
        rc, out = run(s, [case_a], gate="all")
        check("N2 引文不在所指行 → all 下判 FAIL（真错①必须抓到）", rc == 1 and "引文不在所指行" in out,
              f"rc={rc}\n{out}")

        # N3 无法归属：裸简写 + 此前全件无任何文件名 ⇒ 读者无从定位。
        #    ⚠ 夹具刻意把**可解析的引用放在后面**：真实的件总有自己的语料引用，
        #      而 fail-closed 的语义是「**一条都没核到**」——若全件都核不到，会先被 exit 2 拦下，
        #      本例要测的是「核到了别处、但这一处归属失败」的报法。
        s = sample("N3.md", "另见 `:123` 处的说法。\n本案见 `短件.md:3` 处。\n")
        rc_all, out_all = run(s, [case_a], gate="all")
        rc_rng, out_rng = run(s, [case_a], gate="range")
        check("N3 裸简写无法归属 → all 判 FAIL / range 降 WARN", rc_all == 1 and rc_rng == 0,
              f"all rc={rc_all} · range rc={rc_rng}\n{out_all}")

        # N4 ★ 归属失败的引用**仍须过越界闸**（缺陷⑥ · 本轮自己引入的回归）
        #    修前：越界检查被挪到 `continue` 之后 ⇒ 文件名写错/粘标点/裸简写**整行不查**、只落 WARN、rc=0
        #    ——**恰恰是要拦的形态被放过了**。修后走兜底门限（本案语料最长件 = 500）。
        s = sample("N4.md", "另见 `清单v2.md:900` 的行。\n本案见 `短件.md:3` 处。\n")
        rc, out = run(s, [case_a], gate="range")
        check("N4 归属失败 + 行号**超过语料最长件** → FAIL（⚠ 只覆盖这一子情形：`：200` 这类不超的仍会静默放过）", rc == 1 and "行号越界" in out and "兜底判据" in out,
              f"rc={rc}\n{out}")

        # N5 ★ 缺陷⑩ 守卫（承三轮复验 B2）：**只引别案材料的件是正当形态**，
        #    不得被 fail-closed 第四闸判成「--corpus 指错」。收窄判据＝还要「owner 名字在本案一个同名件都找不到」。
        #    ⚠ 四轮复验指出：本条**只覆盖「别案件与本案撞名」这个子情形**——把 extra 件改名成
        #      `GOTCHAS.md`（`--extra` 的典型载荷、本案语料里通常无同名件）就会 rc=2。名称勿读宽。
        s = sample("N5.md", "本案的真身见 `别案语料/短件.md:9` 那一行。\n")
        rc, out = run(s, [case_a], extra=[tmp], gate="range")
        check("N5 只引别案材料且**与本案撞名** → 不得 exit 2（⚠ 只覆盖撞名子情形）", rc == 0, f"rc={rc}\n{out}")

        # N6 ★ 承四轮复验 E6：N5 过得了**只是因为它恰好撞名**。把 extra 件改成 `--extra` 的
        #    **典型载荷名**（本案语料里没有同名件）——旧判据（按 basename 找同名）立刻失效，
        #    而「按解析」的新判据仍然正确。
        (case_b / "GOTCHAS.md").write_text(body(30, "别案坑"), encoding="utf-8")
        s = sample("N6.md", "本案的真身见 `别案语料/GOTCHAS.md:9` 那一行。\n")
        rc, out = run(s, [case_a], extra=[tmp], gate="range")
        check("N6 只引别案材料、且该名**本案无同名**（GOTCHAS 型）→ 仍不得 exit 2",
              rc == 0, f"rc={rc}\n{out}")

        print("\n══ F 类 · 故障注入（配置错误必须硬停 —— 不得静默放绿）══")

        # ⚠ 本组断言一律用 **rc == 2**（不是 `rc != 0`）。承独立复验 P7(c)：旧断言 `rc != 0`
        #   连「未捕获 traceback 崩了（rc=1）」都算过——**分不出 fail-closed 与崩溃**，
        #   而「崩溃然后被 CI 当成通过」正是这类脚本的经典死法。
        s = sample("F1.md", "本案清单 `:999` 的那段。\n")
        rc, out = run(s, [tmp / "根本不存在的语料目录"], gate="range")
        check("F1 --corpus 不存在 → exit 2（fail-closed，非崩溃）", rc == 2, f"rc={rc}\n{out}")

        empty = tmp / "空语料"; empty.mkdir()
        rc, out = run(s, [empty], gate="range")
        check("F2 --corpus 为空目录 → exit 2（fail-closed）", rc == 2, f"rc={rc}\n{out}")

        # F2b ★ 隔离检查（承三轮复验 B-3）：上一条**分不出是哪道闸给的 2**——
        #   夹具带引用 ⇒ 第四闸（「一条都没核到」）会**代偿**，于是**单独撤掉「空语料闸」抓不到**。
        #   本条用**无引用件**：此时第四闸不触发，`2` 只能来自「空语料闸」本身。
        rc, out = run(sample("F2b.md", "本件不含任何引用。\n"), [empty], gate="range")
        check("F2b 无引用件 + 空语料 → exit 2（空语料闸必须自己响，不被第四闸代偿）",
              rc == 2 and "空语料" in out, f"rc={rc}\n{out}")

        # F5 ★ 承三轮复验：`--target` 指向**目录**时原先是未捕获 `IsADirectoryError`、rc=1
        #    （与「有 FAIL」同码，调用方分不出「崩溃」与「判决」）⇒ 纳入 fail-closed，rc=2。
        rc, out = run(tmp, [case_a], gate="range")
        check("F5 --target 是目录 → exit 2（fail-closed，非崩溃）", rc == 2, f"rc={rc}\n{out}")

        rc, out = run(tmp / "不存在.md", [case_a], gate="range")
        check("F3 --target 不存在 → exit 2（fail-closed，非崩溃）", rc == 2, f"rc={rc}\n{out}")

        # F4 ★ 「存在但指错」的目录 —— 缺陷④的另一形态，**比空目录更可能发生**
        #    （把 PEC/raw 当成案语料），修前是 **已核 0 处 · FAIL 0 · exit 0 · ✅ 全绿**。
        wrong = tmp / "像语料但不是语料"; wrong.mkdir()
        (wrong / "别的东西.md").write_text(body(50, "别"), encoding="utf-8")
        rc, out = run(sample("F4.md", "本案清单 `短件.md`，另见 `:200` 那段。\n"), [wrong], gate="range")
        # ⚠ 承四轮复验：原断言只有 `rc == 2`，**「返回前先打 FAIL、不吞红」那半无守卫**（删掉它也全绿）。
        #   现加一条：必须真的把已判出的 FAIL 打出来。
        check("F4 --corpus 指到存在但无关的目录 → exit 2 且**不吞红**（先打已判出的 FAIL）",
              rc == 2 and "返回前先报" in out, f"rc={rc}\n{out}")

        # F6 ★ 承四轮复验 E7：**错语料里恰有一个与引用名同名的件** —— 这是上一版收窄判据
        #    会漏掉的 fail-open 形状（按 basename 找同名 ⇒ 被同名件骗过 ⇒ rc=0 · ✅）。
        #    新判据按「解析到没有」判：该件里的两个引用在给的任何根里都解析不到 ⇒ 仍须 exit 2。
        wrong2 = tmp / "像语料但指错"; wrong2.mkdir()
        (wrong2 / "README.md").write_text(body(20, "错语料README"), encoding="utf-8")
        (wrong2 / "CHANGELOG.md").write_text(body(20, "错语料CHANGELOG"), encoding="utf-8")
        s = sample("F6.md", "见 `共享基础/README.md:5` 与 `共享基础/CHANGELOG.md:3`。\n")
        rc, out = run(s, [wrong2], gate="range")
        check("F6 错语料里**有同名件**但引用解析不到 → 仍须 exit 2（缺陷⑦ fail-open 复发守卫）",
              rc == 2, f"rc={rc}\n{out}")

        # F7 ★ 承五轮复验 HIGH#1 / 六轮复验 A4：**错语料里恰有同名的「长」件碰巧解析** ⇒ 合取被解除、
        #   回到 `已核 1 处 · FAIL 0 · ✅`。该形态**无法硬拦**（会误杀「只引 extra 的正当件」），
        #   故改为**覆盖率显著提示**；而首版把它 append 进 `warns` ⇒ **`--quiet` 下被整片吞掉**、
        #   又是零信号。⇒ 移到**汇总行常显**。本条守的就是「`--quiet` 下也必须在场」。
        wrong3 = tmp / "有同名长件"; wrong3.mkdir()
        (wrong3 / "短件.md").write_text(body(3000, "错语料长同名件"), encoding="utf-8")
        s = sample("F7.md", "见 `短件.md:3` 处。\n另见 `清单.md:999` 处。\n再见 `别件.md:5` 处。\n"
                            "又见 `他件.md:7` 处。\n末见 `这件.md:9` 处。\n")
        rc, out = run(s, [wrong3], gate="range", quiet=True)
        check("F7 错语料含同名的长件 → `--quiet` 下汇总行**仍须**报「覆盖率过低」（fail-open 显形守卫）",
              rc == 0 and "本案语料覆盖率过低" in out, f"rc={rc}\n{out}")

        print("\n══ P 类 · 正向（闸必须不报 —— 防误报把闸变成噪声源）══")

        # P1 Bug-1 守卫：**写全路径的跨案引用不得被判本案越界**
        #    （修前：正则吞掉 `/` ⇒ 截成 `短件.md` ⇒ 落到本案 10 行件 ⇒ 假越界）
        # ⚠ 二轮复验逮出：本条原夹具**没有反引号** ⇒ 解析到 **0 处引用** ⇒ **断言恒真、守的是空气**
        #    （对已知有 bug 的旧版也 ✅）。现补反引号，并配一条可解析的本案引用
        #    （否则会被 fail-closed 第四闸拦成 exit 2，根本走不到越界判据）。
        s = sample("P1.md", "本案见 `短件.md:3` 处。\n真身是 `别案语料/短件.md:800` 那一行。\n")
        rc, out = run(s, [case_a], extra=[tmp], gate="range")
        check("P1 跨案全路径引用 → 不得判越界（Bug-1 复发守卫）",
              rc == 0 and "行号越界" not in out, f"rc={rc}\n{out}")

        # P2 假红 A 守卫：本行另有足够长的文件 ⇒ 不判越界（引录列简写常指同行另一件）
        #    ⚠ 同上，原夹具无反引号 ⇒ 恒真。现补反引号。
        #    ⚠⚠ 承三轮复验 B-2：**顺序必须让 `：300` 归属到短件（谱系 20 行）**。
        #       首版写成「谱系 · 长件」，owner 落 **长件（500 行）** ⇒ 300 本来就不越界，
        #       于是 **owner 级错实现下它也照样绿**（复验方 17 变体矩阵实测）——**自称的守卫无效**。
        #       对调后：行级 OR 取 500 ⇒ 绿；退回 owner 级取 20 ⇒ 300>20 ⇒ 红 ⇒ 真能守。
        s = sample("P2.md", "| 载体 | `长件.md` · `谱系.md` | `:300` |\n")
        rc, out = run(s, [case_a], gate="range")
        check("P2 同行另有足够长件 → 不得判越界（假红 A 守卫）",
              rc == 0 and "行号越界" not in out, f"rc={rc}\n{out}")

        # P3 假红 B 守卫：日期串不得被当行号（修前 `updated: 2026-05-15` ⇒ 区间 `:5-2026`）
        s = sample("P3.md", "`谱系.md` 的 frontmatter 写 `updated: 2026-05-15`，正文见 `长件.md:3`。\n")
        rc, out = run(s, [case_a], gate="range")
        check("P3 日期串不得被当行号/行号区间（假红 B 守卫）",
              rc == 0 and "疑似年份" not in out, f"rc={rc}\n{out}")
        # ⚠ 承五轮复验（LOW 11）：原先还带一个 `":5-" not in out` 子句——实测该字面**从不出现**
        #   于任何输出，属**恒真死重**，且给读者「连行号区间都查了」的错觉。已删。

        # P4/P5 日期规则的方向性（直接单测 strip_dates，不依赖语料）
        sys.path.insert(0, str(TOOL.parent))
        import verify_citations as V  # noqa: E402
        check("P4 真日期（月/日在合法域）必须被抠掉",
              V.strip_dates("updated: 2026-05-15").strip() == "updated:", V.strip_dates("updated: 2026-05-15"))
        check("P5 非日期数字（月>12）不得被抠掉——否则合法行号区间会被误吞",
              V.strip_dates("x 1588-16 y") == "x 1588-16 y", V.strip_dates("x 1588-16 y"))

        # P6 新体例正例：逐字引录紧跟 `文件:行号`、「…」紧接其后 ⇒ 双闸全绿
        head = body(500, "长").splitlines()
        s = sample("P6.md", f"本条的重选链见 `长件.md:3`「{head[2]}」与 `长件.md:7`「{head[6]}」。\n")
        rc, out = run(s, [case_a], gate="all")
        check("P6 合规新体例件 → 双闸 FAIL 0、exit 0", rc == 0,
              f"rc={rc}\n{out}")

        # P7 ★ 同名件歧义时门限必须取**被引那一个**，不得按无关件算（缺陷⑤ · 承独立复验 P6）
        #   夹具刻意让 `a/同名.md`(400) 与 `z/同名.md`(10) 同名；引用走 `z/同名.md` 全路径
        #   ⇒ resolve 用 `root/"z/同名.md"` 是**确定性**的（目录序影响不到），
        #     而旧口径 corpus_len 取 sorted 字典序首位 = `a/同名.md`(400) ⇒ 门限被无关件抬高、放行。
        s = sample("P7.md", "见 `z/同名.md:300` 的行。\n")
        rc, out = run(s, [case_a], gate="range")
        check("P7 同名件互异长度 → 门限取被引件（FAIL，不得放行）",
              rc == 1 and "行号越界" in out and "400" not in out, f"rc={rc}\n{out}")

        # P8 ★ 明文提及（**不在反引号内**）的件不得抬高门限（承独立复验 P4 的可修部分）
        s = sample("P8.md", "本案清单是 `短件.md`。\n对照面见 清单 `:200`，另见 长件.md（与本行无关）。\n")
        rc, out = run(s, [case_a], gate="range")
        check("P8 散文里提及的件不抬高门限（仍有 200>10 的越界 → FAIL）",
              rc == 1 and "行号越界" in out, f"rc={rc}\n{out}")

        # P9 ★ 缺陷⑫ 守卫（承三轮复验 B8）：日期判据改为**三段式**后，
        #    `:1905-12` 这类**合法四位数行号区间**不得再被当日期整段抹掉。
        check("P9 两段式 `:1905-12` 不得被当日期抠掉（否则合法行区间被吞）",
              V.strip_dates("x :1905-12 y") == "x :1905-12 y", V.strip_dates("x :1905-12 y"))
        # （原 `P9b 三段式真日期仍须被抠掉` 与 `P4` 表达式**逐字相同**、不增覆盖，承四轮复验已删。）

        # P10 ★ 缺陷⑨ 守卫（承三轮复验 B4）：弱归属（`src=全文前置`）**不得零信号**。
        #     ⚠ 触发器已**收敛**（首版无条件 WARN ⇒ 实测占 CS-02 全部 WARN 的 73%、把提示通道淹了）：
        #     现只在「**弱归属确实改变了判决**」时报——该行号**超出全文前置认定的那一件**，
        #     却被同行另一件放过。故夹具必须造成这个形状：
        #     全文前置认定的是 `短件.md`（10 行），`:300` 本应越界，被同行的 `长件.md`（500 行）放过。
        s = sample("P10.md", "本案见 `短件.md:3` 处。\n另有一段无关正文。\n对照面见 清单 `:300`，与 `长件.md` 同段。\n")
        rc, out = run(s, [case_a], gate="range")
        check("P10 弱归属放行（门限被同行件抬高）必须发 WARN，不得零信号（缺陷⑨ 守卫）",
              "弱归属放行" in out, f"rc={rc}\n{out}")

        # P11 ★ 缺陷⑧ 守卫（承三轮复验 B8）：corpus 名是 extra 名的**字符串前缀**时，
        #     extra 件不得被 `startswith` 误认成本案（旧法 `A` 会把 `AB` 当亲戚）。
        ext2 = tmp / "本案语料-EXTRA"; ext2.mkdir()
        (ext2 / "别.md").write_text(body(50, "别"), encoding="utf-8")
        s = sample("P11.md", "本案见 `短件.md:3` 处。\n另见 `本案语料-EXTRA/别.md:9` 处。\n")
        rc, out = run(s, [case_a], extra=[tmp], gate="range")
        check("P11 corpus 名是 extra 名的前缀时，不得误认成本案（缺陷⑧ 守卫）",
              "落在 **--extra" in out, f"rc={rc}\n{out}")

        # P12 ★ 缺陷③「零信号」那半的守卫：工具**判不出**该型（另一半未闭、归 Doctor），
        #     但**必须把「有多少引用是弱归属」和「不保证判出该型」讲出来** —— 零信号本身是缺陷的一半。
        rc, out = run(sample("P12.md", "本案见 `短件.md:3` 处。\n另见 `:4` 处。\n"), [case_a], gate="range")
        check("P12 汇总必须报**正确的**弱归属计数 ＋ 说明该型靠散文绑定提示、不判 FAIL（缺陷③）",
              "弱归属（归属来源＝全文前置）1 / 2 处引用" in out and "不判 FAIL" in out, f"rc={rc}\n{out}")
        # ⚠ 承五轮复验 A3：原断言只查「标签串存在」，而那两个串只要 `total_cites>0` 就必然打印
        #   ⇒ 断言退化为「件里有至少一处引用」（把 `weak_total += 1` 挖空，金丝雀仍全绿）。
        #   现钉**具体数字**：本夹具恰 2 处引用、其中 1 处弱归属。

        # N7 ★ 缺陷③b 的**检测面**（Doctor 令「加」的散文名绑定）：`清单 \`:99\`` 这类——
        #     真身写在**散文**里、不在反引号内 ⇒ 旧版零信号。绑定后必须报出候选与超出。
        #     ⚠ 断言必须用 **WARN 前缀**（`散文名绑定·超出`）：汇总自陈行里也有「散文名绑定」四字，
        #       用裸词断会**恒真**（本套自身当场踩过）。
        s = sample("N7.md", "本案见 `长件.md`（500 行）。\n对照面见 清单 `:99` 的那一段。\n")
        rc, out = run(s, [case_a], gate="range")
        check("N7 散文名绑定：`清单` 型零信号须被报出（③b 检测面）",
              "散文名绑定·超出" in out and "清单.md" in out, f"rc={rc}\n{out}")

        # P13 ★ 散文绑定的**假阳守卫**（首版现场）：散文里的 `CS-02` 曾让词元 `02` 匹配上
        #     `A02_样件.md` ⇒ 真案 CS-09 L323 造出假阳。规约＝CJK 词元 ≥2、纯 ASCII 词元 ≥4。
        s = sample("P13.md", "本案见 `长件.md`（500 行）。\n参考 CS-02 的内容 `:99`。\n")
        rc, out = run(s, [case_a], gate="range")
        check("P13 纯数字/短 ASCII 词元不得绑件（`CS-02`→`A02_…` 假阳守卫）",
              "散文名绑定·超出" not in out, f"rc={rc}\n{out}")

        # P14 ★ 边界（承五轮复验 E1 的 `>=` off-by-one）：**行号恰等于候选长度 ⇒ 不得报**；
        #     多 1 才报。`清单.md` 在夹具里是 20 行。
        s = sample("P14.md", "本案见 `长件.md`（500 行）。\n对照面见 清单 `:20` 的那段。\n")
        rc, out = run(s, [case_a], gate="range")
        check("P14 行号**恰等于**候选长度 → 不得报（`>=` 边界守卫）",
              "散文名绑定·超出" not in out, f"rc={rc}\n{out}")
        s = sample("P14b.md", "本案见 `长件.md`（500 行）。\n对照面见 清单 `:21` 的那段。\n")
        rc, out = run(s, [case_a], gate="range")
        check("P14b 行号**超出 1 行** → 必须报（边界另一侧）",
              "散文名绑定·超出" in out, f"rc={rc}\n{out}")

        # P15 ★ 单字 CJK 词元不得绑件（承五轮复验 E7）：`件` 是 `长件`/`短件`/`A02_样件` 的公共后缀，
        #     单字在中文里命中率过高 ⇒ 必成噪声源。规约＝CJK 词元 ≥2 字。
        s = sample("P15.md", "本案见 `长件.md`（500 行）。\n对照面见 件 `:99` 的那段。\n")
        rc, out = run(s, [case_a], gate="range")
        check("P15 单字 CJK 词元不得绑件（`件` 是多个件的公共后缀）",
              "散文名绑定·超出" not in out, f"rc={rc}\n{out}")

        print("\n══ R 类 · 真树回归 ══")
        # ⚠ 承独立复验 P7(a)：原先只用 `Path("/sessions")` 探——**Mac 侧原生跑必然探不到**，
        #   且跳过时只在打印里提一句、**仍报「全过」**：守卫可以静默消失而汇总行照样绿。
        #   现改为：多候选根 ＋ 跳过时**显式体现在汇总行**（`R 组 n/4`；`⏭` 行另有「R 组未跑」字样），
        #   不让缺失伪装成通过。
        roots: list[Path] = []
        # ★ 二轮复验逮出两处：① 此变量原先只在 else 分支赋值、跳过分支却无条件读 ⇒
        #   **UnboundLocalError 崩溃**；② 即使初始化，「探针根存在、但四个真件缺失」这条路径
        #   也会把标志置真 ⇒ **汇总行静默报全过**。
        #   改用「**实际跑成的 R 例数**」当判据，两条跳过路径都能现形。
        r_checks = 0
        for base in (Path("/sessions"), Path("/Users")):
            if base.exists():
                roots += sorted(base.glob("*/mnt/Documents/Claude/Projects/PEC"))
                roots += sorted(base.glob("*/Documents/Claude/Projects/PEC"))
        if not roots:
            print("  ⏭ PEC 不在盘上 —— **R 组未跑**（真树层本次无覆盖，汇总行会标注）")
        else:
            root = roots[0]
            real = [
                ("CS-05", "raw/2026-09-26_analysis_CS05证据层补全_折中法.md", "case-studies/CS-05_中华文明", 0),
                ("CS-02", "raw/2026-09-26_analysis_CS02证据层补全_折中法.md", "case-studies/CS-02_盎格鲁撒克逊-英国文明", 0),
                ("CS-01", "raw/2026-09-26_analysis_CS01证据层补全_折中法样板.md", "case-studies/CS-01_犹太-以色列文明", 0),
                # CS-09 是出事那一案：留痕行**引述错误原文**，越界闸按现状会报 2 条。
                # 这是**已知且已定性**的读数（旧体例 + 引述），不是回归失败 ⇒ 断言**恰好 2 条、逐条在 L193**。
                # ⚠ 承独立复验 P7(b)：原断言写的是 `<= 2` 而名字却称「均落在 L193」——
                #   0/1/2 条、落在任何一行都算过，**缺陷② 若复发这一例不会响**。现收紧。
                ("CS-09", "raw/2026-09-26_analysis_CS09证据层补全_折中法.md", "case-studies/CS-09_伊斯兰文明", -1),
            ]
            for tag, tgt, corp, expect in real:
                t, c = root / tgt, root / corp
                if not (t.exists() and c.exists()):
                    print(f"  ⏭ {tag} 缺件，跳过")
                    continue
                rc, out = run(t, [c], gate="range")
                r_checks += 1
                nfail = next((int(x.split("FAIL ")[1].split(" ")[0])
                              for x in out.splitlines() if "FAIL " in x and "已核引用" in x), None)
                if expect == 0:
                    check(f"R {tag} · 越界闸 FAIL 0（已交案回归）", rc == 0 and nfail == 0,
                          f"rc={rc} fail={nfail}")
                else:
                    # 收紧断言（承独立复验 P7b）：恰好 2 条，且**每条**报错都落在 L193。
                    # 原写 `<= 2` ⇒ 0/1/2 条、落任何一行都算过，**缺陷② 若复发这一例不会响**。
                    fail_lines = [x for x in out.splitlines() if "**行号越界**" in x]
                    ok = (nfail == 2) and len(fail_lines) == 2 and all("L193" in x for x in fail_lines)
                    check("R CS-09 · 越界闸 FAIL == 2 且**逐条**落在 L193（留痕引述 · 已知读数）",
                          ok, f"rc={rc} fail={nfail} fail_lines={len(fail_lines)}\n{out}")

        print()
        n_actual = len(_results)
        expected_ok = (n_actual == EXPECTED_CASES)
        bad = [r for r in _results if not r[0]]
        # ⚠ 承独立复验 P7(a)：R 组跳过时**必须在汇总行现形**，否则「守卫静默消失」看起来仍是全过。
        # ⚠⚠ 承三轮复验 B-1：判据原为二值（0 / >0）⇒ **「部分缺件」（跑成 1/4 或 3/4）照样不现形**。
        #   现报**实际跑成的例数 n/4**，三种形状（0 · 部分 · 4）在汇总行都可辨。
        note = "" if r_checks == 4 else f"  ⚠ **R 组 {r_checks}/4**（真树层覆盖不全）"
        print(f"══ 金丝雀：{n_actual - len(bad)}/{n_actual} 通过{note} ══")
        if not expected_ok:
            print(f"  ❌ **例数守卫**：期望 {EXPECTED_CASES} 例、实际 {n_actual} 例"
                  f"（删例须同步改 EXPECTED_CASES 与四件文档里的「{EXPECTED_CASES} 例」）")
        if bad:
            print("未过：")
            for _, n, _ in bad:
                print(f"  · {n}")
        return 1 if (bad or not expected_ok) else 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
