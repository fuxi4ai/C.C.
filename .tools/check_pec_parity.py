#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""PEC 判据/方法论 · 「规范落点 ↔ 现行执行件」同版校验 · **v2**（只读 · 提示器级）

为什么存在
----------
2026-09-29 批内**三次**出现「改了规范落点、没改执行件」：
  ① 差额口径三处不同版 ② 钟摆型订正未追到下游转述件 ③ 「每处引录另附一句「为何支撑」」进了 `系统 §四 4.5`、没进 `起手包 §三`
⇒ 该纪律此前只有一句要求、没有机械动作（同族 `G-X200`）。台账见 `Projects/PEC/GOTCHAS.md` **`G-35`**。

它保证什么 / 不保证什么（**2026-09-29 v2 重写 · 采纳对抗复验的结论**）
--------------------------------------------------------------------
**能保证**（前提：配置未被改动）
· 三组同版对的**关键串在整件层面同时存在**；某串从任一件**整体消失** ⇒ 红并点名。
· **声明指纹与实算指纹一致**（v2 新增回读）：件改了而文档里的指纹没改 ⇒ 红。
· 脚本**不改**被审件（`--self-test` 内含 sha256 前后断言）。

**⚠ 不能保证（v1 曾过度声称，v2 如实降级）**
· **不保证位置**：关键串可藏在**订正留痕／代码围栏／废止声明／无关小节**里而在册 ⇒ 判据是**全文子串**、无块作用域。
  ⇒ **纪律：加订正留痕时，不要把关键串逐字抄进留痕**（抄了就等于给它留后门）。本机制自身即因此被击穿过一次。
· **不保证逐字同版**：两侧体例本就不同（`系统` 用表格、`起手包` 用引述）；**同义改写会假红**，漏改措辞也会漏判。
· **指纹是「声明值 vs 实算值」的一致性检查，不是件的全量摘要**：它只覆盖**被校块**，别拿它当「文件没被改」的凭证。
· **⚠ 三处声明只有第一处被回读**（2026-09-29 由未参与实施的独立审核者实核报出）：`FP_RE.search` 只取**首个**匹配，而三处声明里的**后两处**（`系统` §四 头 · `起手包` §三 头）**都在被哈希块内**、已被 `_norm_fp` 归一化 ⇒ **单独改这两处不会被发现**。⇒ 改指纹时**三处必须一起改**，别指望脚本替你抓。
· **只做正向检查**：它抓「**该有的没有**」（关键串缺席／指纹失配），**抓不住「不该有的还在」**——某事实的状态改了、旧状态的反向陈述（同义写法）还散在别处，本脚本**一律不报**（2026-09-29 `G-35` 追记的形态二即此）。
· **它不是闸**：绿 ＝「这些关键串找得到 ＋ 声明指纹对得上」，仅此而已。

用法
----
    python3 ~/Documents/Claude/brain/.tools/check_pec_parity.py               # 校验
    python3 ~/Documents/Claude/brain/.tools/check_pec_parity.py --print       # 只打印实算指纹（不改退出码语义）
    python3 ~/Documents/Claude/brain/.tools/check_pec_parity.py --self-test   # 负向自检

退出码：0 ＝ 全过 · 1 ＝ 有缺口/指纹失配 · 2 ＝ 配置或路径错误
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import sys
import tempfile

D = "Documents/Claude/"
HOST = "/Users/lunarabbit/" + D

SYS = "Projects/PEC/文明基因/判据/文明基因系统.md"
# ⚠ 2026-10-01 订正：路径原为 `brain/logs/checkpoints/…`——**日志月折后（meditation 折进 `logs/YYYY-MM/`）该路径失效**，
#   本脚本自 2026-09-30 前后起**静默 exit 1**，「改一边必改另一边」的机械动作**实际已断**。
#   由第七轮独立复验者实跑逮出（判据侧系统↔起手包漂移即因此长期无人发现）。
KIT = "brain/logs/2026-09/checkpoints/2026-09-26_D4重跑起手包.md"

# 被校块（用于指纹）：anchor → (start_pat, end_pat)
BLOCKS = {
    SYS: [("### 2.0 条文", "### 2.1 名册"), ("## §四 方法论层", "## §五 沿革层"),
          # ⚠ 2026-10-01 新增（承第九轮独立复验者 E5(a) ＋ Doctor 同日裁「纳入」）：
          #   此前 **§七 7.1 不在任何被校块内** ⇒ 本批第 1 号改动（撤「外生条件」档 —— 一条 Doctor 令）
          #   在**系统侧零机械覆盖**。直证（第九轮变异实测）：把 7.1 表体增一字，**指纹纹丝不动**；
          #   把 2.0（五）／2.0（六）／起手包 §三 表体各增一字，指纹**都变**。
          #   纳入后它与其余两块同受指纹盯：改它而不更新声明 ⇒ 红。
          ("### 7.1 入场表单", "## §八")],
    KIT: [("## 三、可执行判据集", "## 四、输入件与产出")],
}

PAIRS = [
    {
        "name": "判据条文（§二 2.0 ↔ 起手包 §三）",
        "files": [SYS, KIT],
        "canaries": ["再次被用于回答", "政权数 ≥2", "≥2 个不同处境下的重新选中实例",
                     "o` 后回归 `i`", "钟摆型", "可证伪条件", "政权层产物", "同一对象两层"],
    },
    {
        "name": "执行定义（§四 4.1 ↔ 起手包 §三）",
        "files": [SYS, KIT],
        "canaries": ["两者并列", "不要求教学主体", "被引文本", "被搬形制", "被教正典",
                     "制度连续", "G-08", "`S6` 规则二"],
    },
    {
        "name": "引录体例（§四 4.5 ↔ 起手包 §三）",
        "files": [SYS, KIT],
        "canaries": ["逐字引录必须紧跟一个", "文件:行号", "为何支撑",
                     "转述／标签／强调一律不加引号"],
    },
]

# 只在被点名的件里要求出现（本体不在规范落点，不能进上面的「每件都要有」清单）
CONDITIONAL = [
    {"file": KIT, "canaries": ["被用作正当性表述", "作为被争夺的对象出现"],
     "why": "`B1` 入场表单**四列**〔**订正 2026-10-01**：原「五列」——第 4 档「作为原因／条件出现（地缘 · 气候 · 禀赋）」已随 Doctor 裁删；本描述未跟改，由第七轮独立复验者逮出〕（**本体已迁**：`文明基因/判据/文明基因系统.md` §七 `7.1 入场表单（S8 · 四列）`〔**订正 2026-10-01b**：本指针串原写「**五列**」——**与同批已改的姊妹落点（`raw/2026-09-25_analysis_文明基因晋升系统与形成史.md:623` 的指针目标）是同一缺陷的两处**，那边改了、这边漏改；**且漏的这处在当时刚被列为头号修复目标的文件里**。承第八轮独立复验者逮出。〕；**2026-09-29 前**本体住在 `raw/2026-09-25_analysis_文明基因晋升系统与形成史.md` §14.5，该处**现只留指针** · 承审计 `C-03`／P2 裁定⑭）"},
    # ⚠ 2026-10-01 新增（承 Doctor 裁「补表 ＋ 加守卫」）：守 `起手包 §三` 必须复述 `2.0（五）` 二值判定表本体。
    #   为什么要有这条：同日规则三行已改为「其余情形 ⇒ 见 `2.0（五）` 二值判定表」，而**本件当时无此表**
    #   ⇒ 执行者「照书跑到一半发现无处可查」。**canary 集原不覆盖该表**（第八轮复验者指出），故补此守卫。
    #   两条 canary 取本表**独有**的行文（不在 §三 别处出现），以保证「缺表即红」归因唯一。
    {"file": KIT, "canaries": ["未达 ≥2 处境", "久无重选、未被否定", "其余情形 ⇒ 见"],
     "why": "`2.0（五）` 二值判定表本体（**2026-10-01 补入本件** · 承 Doctor 裁）——本表**本体在系统件**，执行件须**同版复述**〔**订正 2026-10-01m**：原写「`系统 §二 2.0（七）` 口径」，而**该节不存在**（`2.0` 止于（六））——系本批在**头号修复目标那个文件里**新造的悬空引用，且只在报红时打印、盘上无读者；由**第九轮独立复验者**逮出〕；若本件缺表，则规则三行的「见 `2.0（五）`」**无处可指**（该缺口由第七轮复验者逮出、第八轮复核）"},
    # ⚠ 2026-10-01 新增（承第九轮独立复验者 E5(b)/(c)）：**两侧成对**钉住「规则三的现行措辞」。
    #   为什么要有这条：原 canary 只挂 KIT、且只钉行首串 ⇒ 第九轮变异实测证明
    #   「**单侧**改回旧措辞 ＋ 同步指纹」与「**两侧**都改回」**均全绿**——而那正是 `G-35` 要治的形状。
    #   两侧各钉同款 canary 后，任一侧缺失即报红（对应第九轮变异 T4／T5）。
    {"file": SYS, "canaries": ["其余情形 ⇒ 见"],
     "why": "`2.0（二）` 规则三的**现行措辞**（系统侧 · 与 KIT 侧同款 canary 成对）"},
]

# 声明指纹的读取位置（v2 新增回读）：在系统件里声明，须与实算一致
DECLARED_IN = SYS
FP_RE = re.compile(r"(?:同版|声明)指纹\s*`([0-9a-f]{12})`")


def resolve(rel: str) -> str | None:
    c = os.path.join(HOST, rel)
    if os.path.exists(c):
        return c
    import glob
    for p in sorted(glob.glob("/sessions/*/mnt/" + D + rel)):
        if os.path.exists(p):
            return p
    return None


def _norm_fp(text: str) -> str:
    """把「同版指纹 `<12hex>`」的值替换为占位符 —— 否则**声明行自身在被哈希的块里**，
    改声明就改指纹、改指纹又要改声明，成循环。只占位**值**，行内其余文字仍参与哈希。"""
    return re.sub(r"((?:同版|声明)指纹\s*`)[0-9a-f]{12}(`)", r"\1FP\2", text)


def _blocks_of(text: str, anchors) -> str:
    out = []
    for a, b in anchors:
        i = text.find(a)
        if i < 0:
            out.append(f"<MISSING-BLOCK:{a}>")
            continue
        j = text.find(b, i + len(a))
        out.append(_norm_fp(text[i: j if j > 0 else len(text)]))
    return "\n".join(out)


def fingerprint(texts: dict) -> str:
    """**v2**：由**被校块的实际内容**求出——件改了它就变（v1 只由配置求出，与件无关）。"""
    canon = json.dumps([_blocks_of(texts[r], BLOCKS[r]) for r in sorted(BLOCKS)],
                       ensure_ascii=False, sort_keys=True)
    return hashlib.sha256(canon.encode("utf-8")).hexdigest()[:12]


def _read(rel: str, base: str | None) -> str:
    if base is None:
        p = resolve(rel)
        if p is None:
            raise FileNotFoundError(rel)
    else:
        p = os.path.join(base, os.path.basename(rel))
    with open(p, encoding="utf-8") as fh:
        return fh.read()


def check(base: str | None = None) -> tuple[int, list, str]:
    rels = sorted({r for pr in PAIRS for r in pr["files"]} | {c["file"] for c in CONDITIONAL})
    texts, bad = {}, []
    for rel in rels:
        try:
            texts[rel] = _read(rel, base)
        except FileNotFoundError:
            bad.append(f"路径不存在（两个候选根都探过）：{rel}")
    if not texts:
        return 2, bad, "-"

    for pr in PAIRS:
        for rel in pr["files"]:
            if rel not in texts:
                continue
            for can in pr["canaries"]:
                if can not in texts[rel]:
                    bad.append(f"[{pr['name']}] {rel} —— 缺关键串：「{can}」")
    for cd in CONDITIONAL:
        if cd["file"] in texts:
            for can in cd["canaries"]:
                if can not in texts[cd["file"]]:
                    bad.append(f"[{cd['why']}] {cd['file']} —— 缺关键串：「{can}」")

    fp = fingerprint(texts) if len(texts) == len(rels) else "-"
    # v2 回读：声明值 vs 实算值
    if fp != "-" and DECLARED_IN in texts:
        m = FP_RE.search(texts[DECLARED_IN])
        if m is None:
            bad.append(f"未在 {DECLARED_IN} 找到声明的同版指纹（格式：`同版指纹 `<12位小写十六进制>``）")
        elif m.group(1) != fp:
            bad.append(f"**同版指纹失配**：声明 `{m.group(1)}` ≠ 实算 `{fp}` "
                       f"⇒ 件被改过而声明未更新。修法：把三处声明改成 `{fp}` 并留痕。")
    return (1 if bad else 0), bad, fp


def main(argv: list) -> int:
    if "--self-test" in argv:
        rc0, bad0, fp0 = check()
        print(f"[自检 0] 正路径：退出码 {rc0}（应 0）· 实算指纹 {fp0}")
        if rc0 != 0:
            for b in bad0:
                print("   ", b)
            return 2
        rels = sorted({r for pr in PAIRS for r in pr["files"]} | {c["file"] for c in CONDITIONAL})
        with tempfile.TemporaryDirectory() as td:
            before, targets = {}, {}
            for rel in rels:
                p = resolve(rel)
                before[rel] = hashlib.sha256(open(p, "rb").read()).hexdigest()
                t = os.path.join(td, os.path.basename(rel))
                shutil.copy2(p, t)
                targets[rel] = t
            # 攻击 1：抹掉「为何支撑」（本批真实漏过的那一条）
            t = open(targets[KIT], encoding="utf-8").read()
            open(targets[KIT], "w", encoding="utf-8").write(t.replace("为何支撑", "已抹"))
            rc1, bad1, _ = check(base=td)
            print(f"[自检 1] 抹掉「为何支撑」：退出码 {rc1}（应 1）")
            for b in bad1:
                print("   ", b)
            # 攻击 2：改件不改声明指纹 ⇒ 应指纹失配
            t2 = open(targets[SYS], encoding="utf-8").read()
            open(targets[SYS], "w", encoding="utf-8").write(t2.replace("政权数 ≥2", "政权数≥2"))
            rc2, bad2, fp2 = check(base=td)
            hit = any("同版指纹失配" in b for b in bad2)
            print(f"[自检 2] 同义改动（去掉空格）：退出码 {rc2}（应 1）· 指纹失配被抓={hit}（应 True）· 实算 {fp2}")
            for rel in rels:  # 原件未被改动
                if hashlib.sha256(open(resolve(rel), "rb").read()).hexdigest() != before[rel]:
                    print(f"[自检 3] ✗ 原文件被改动：{rel}")
                    return 2
            print("[自检 3] 原文件未被改动 ✓")
            ok = rc1 == 1 and any("为何支撑" in b for b in bad1) and hit
            print(f"[自检 4] 负向断言={'通过 ✓' if ok else '失败 ✗'}")
            return 0 if ok else 2

    rc, bad, fp = check()
    if "--print" in argv:
        print(fp)
        return rc
    print(f"同版指纹（实算）{fp} · 对 {len(PAIRS)} 组 ＋ 条件项 {len(CONDITIONAL)} 组")
    if rc == 0:
        print("✓ 关键串齐备 ＋ 声明指纹一致（⚠ 提示器级：位置与逐字同版均不保证，见 docstring）")
    else:
        print(f"✗ 发现 {len(bad)} 处：")
        for b in bad:
            print("   ", b)
        print("\n修法：改 `系统 §二／§四` 任一关键串后必须同批改 `起手包 §三`（或反向）；"
              "改完把三处声明指纹更新为上面的实算值，重跑本脚本，并在 `GOTCHAS.md` `G-35` 留痕。")
    return rc


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
