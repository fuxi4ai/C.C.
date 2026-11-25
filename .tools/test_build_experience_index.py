#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build_experience_index.py 的 Projects/ 来源回归测试（ERR-20261104-004）。
只在临时目录里造夹具并运行生成器，不碰真实 brain。
用法:
  python3 test_build_experience_index.py
  GEN=<旧版生成器路径> python3 test_build_experience_index.py   # 负向验证：旧版应失败
"""
import os, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
GEN = os.environ.get("GEN") or os.path.join(HERE, "build_experience_index.py")


OPEN_WORDS = ["已知风险", "已修待验", "待修复", "未修复", "待执行", "待核", "待裁", "待老师核订", "待验证"]
CLOSED_WORDS = ["已解决", "已修复", "已修", "已裁", "已定性", "已登记", "已验证", "已复核", "已复现并修复"]
# 2026-11-05 Doctor 裁 1A：白泽大宗 / 风险日报 / 星空 退出白名单（并入 brain 侧 canonical），夹具改挂白泽观星
SOURCES = ["白泽观星", "海螺姑娘", "EAL"]


def write(root, rel, text):
    p = os.path.join(root, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        f.write(text)


def build(docs):
    r = subprocess.run([sys.executable, "-I", GEN], env={**os.environ, "DOCS_DIR": docs},
                       capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit(f"生成器退出码 {r.returncode}: {r.stderr[-400:]}")
    with open(os.path.join(docs, "Claude/brain/permanent/经验索引.md"), encoding="utf-8") as f:
        return f.read()


def main():
    fails = []

    def check(name, ok):
        print(("PASS " if ok else "FAIL ") + name)
        if not ok:
            fails.append(name)

    with tempfile.TemporaryDirectory() as docs:
        os.makedirs(os.path.join(docs, "Claude/brain/permanent"))
        write(docs, "Claude/brain/白泽观星/GOTCHAS.md",
              "# x\n\n## [ERR-20260101-001] brain 侧条目\n**状态**: ✅ 已解决\n")
        write(docs, "Claude/Projects/Financial/白泽观星/GOTCHAS.md",
              "# x\n\n<!-- Template:\n## [ERR-20260505-001] 注释里的不算\n**状态**: 🔄\n-->\n"
              "## [ERR-20260101-001] 同号条目\n**状态**：🔄 待修复\n\n"
              "## [ERR-20260202-001] 项目侧开放条目\n**状态**：🔄 已修待验（✅ 落签走分轨）\n\n"
              "## [NOTE-20260202-002] 项目侧已闭条目\n**状态**: ✅ 已解决\n\n"
              "## 🔴 普通分类标题\n\n"
              "### GOTCHA-012: 表格状态含闭合与开放\n| **状态** | ✅ 已立；⚠️ 待执行 |\n\n"
              "### GOTCHA-016: 文字开放\n| **状态** | 🟡 待老师核订 |\n\n"
              "### [ ] 待办勾选不是条目\n\n"
              "## [ERR-20260404-001] 无状态条目\n正文\n\n"
              "## [ERR-20260404-002] 紧邻的开放条目\n**状态**: 🔄\n\n"
              "## 无编号的坑\n**状态**: ✅ 已修复\n\n"
              "## [ERR-20260707-001] 无状态甲\n正文\n\n### GOTCHA-030: 紧邻下一条\n| **状态** | 🔄 x |\n\n"
              "## [ERR-20260707-002] 无状态乙\n正文\n\n## 分类二\n**状态**: 🔄 分类下文字\n\n"
              "## 统计\n| 状态 | 数量 |\n")
        write(docs, "Claude/brain/司南/GOTCHAS.md",
              "# x\n\n## [ERR-20260606-001] brain 纯文字\n**状态**: 待修复\n\n"
              "## [ERR-20260606-002] brain 混合\n**状态**: ⏳ 治本未做 · ✅ 本轮已修\n")
        write(docs, "Claude/Projects/Financial/Event-Attribution-Ledger/GOTCHAS.md",
              "# x\n\n- **EAL-M001 · 列表闭合（已验证）**：正文\n"
              "- **EAL-UI008 · 列表开放（⚠ 已知风险）**：正文\n\n"
              "## [ERR-20260303-001] 纯文字状态\n\n状态: 已知风险\n\n"
              "## G-020 — 破折号条目\n- 状态：🔄 已读日志\n\n"
              + "".join(f"## [OPEN-{i}-1] 词\n**状态**: {w}\n\n" for i, w in enumerate(OPEN_WORDS))
              + "".join(f"## [DONE-{i}-1] 词\n**状态**: {w}\n\n" for i, w in enumerate(CLOSED_WORDS)))
        # brain 侧并入格式（2026-11-05 · 1A）：列表粗体 + 无方括号 H3（白泽大宗 `GOTCHA-NNN:` 表格状态 / 星空 `G-NN ·` 无状态）+ 方括号 H2 并存
        write(docs, "Claude/brain/白泽大宗/GOTCHAS.md",
              "# x\n\n- **G-01 列表条目**：正文\n\n## 自 Projects 侧并入\n\n### GOTCHA-001: 表格状态\n\n| 项目 | 内容 |\n|:---|:---|\n| **状态** | ✅ 已修复 |\n\n"
              "### G-07 · 无状态条目\n正文\n\n### GOTCHA-016: 文字开放词\n| **状态** | 🟡 待老师核订 |\n\n## [ERR-GOTCHA-028] 方括号条目\n**状态**: 🔄 待修复\n\n## G-15+ 候选区索引（不是条目）\n")
        # 海螺姑娘故意不建：来源缺失必须显形
        idx = build(docs)
        lines = idx.splitlines()

        def row(eid):
            return next((l for l in lines if l.startswith(f"- `{eid}`")), "")

        check("Projects 条目进索引且指针相对 brain",
              "../Projects/Financial/白泽观星/GOTCHAS.md" in row("ERR-20260202-001"))
        check("开放与未标分开计数", "- 白泽观星: 10 条（开放 5 · 未标 3）" in idx)
        check("brain 侧无方括号 H3 条目进索引（GOTCHA-NNN: / G-NN ·）",
              " ✅ " in row("GOTCHA-001") and "白泽大宗/GOTCHAS.md" in row("GOTCHA-001")
              and " — " in row("G-07") and "白泽大宗/GOTCHAS.md" in row("G-07")
              and " 🔄 " in row("GOTCHA-016") and "白泽大宗/GOTCHAS.md" in row("GOTCHA-016"))
        check("brain 侧四格式并存条数守恒且 G-15+ 不当条目", "- 白泽大宗: 5 条（开放 2 · 未标 2）" in idx and "G-15+" not in idx)
        check("同行有闭合词时仍判开放", " ⚠ " in row("GOTCHA-012"))
        check("待老师核订判开放", " 🔄 " in row("GOTCHA-016"))
        check("含 ✅ 落签字样的 🔄 行判开放", " 🔄 " in row("ERR-20260202-001"))
        check("条目不吃下一条的状态", " — " in row("ERR-20260404-001") and " 🔄 " in row("ERR-20260404-002"))
        check("条目在下一条目处截断（中间无 ## 分类）", " — " in row("ERR-20260707-001") and " 🔄 " in row("GOTCHA-030"))
        check("条目在 ## 分类处截断", " — " in row("ERR-20260707-002"))
        check("brain 来源不走 project_status", " — " in row("ERR-20260606-001") and " ✅ " in row("ERR-20260606-002"))
        check("开放词逐词判开放", all(" 🔄 " in row(f"OPEN-{i}-1") or " ⚠ " in row(f"OPEN-{i}-1") for i in range(len(OPEN_WORDS))))
        check("闭合词逐词判闭合", all(" ✅ " in row(f"DONE-{i}-1") for i in range(len(CLOSED_WORDS))))
        cover = next((l for l in lines if l.startswith("> 覆盖：")), "")
        check("白名单来源都在", all(n in cover for n in SOURCES) and "风险日报" not in cover and "星空" not in cover)
        check("表头行不触发未解析告警", "统计" not in next((l for l in lines if "未解析标题" in l), ""))
        check("同号条目只保留 brain 侧", "✅" in row("ERR-20260101-001")
              and sum(l.startswith("- `ERR-20260101-001`") for l in lines) == 1)
        check("同号冲突在索引头显形", "⚠ 编号重复" in idx and "ERR-20260101-001 @" in idx)
        check("方括号待办不当条目", "待办勾选" not in idx)
        check("HTML 注释里的条目不进索引", "ERR-20260505-001" not in idx)
        check("模板条目不进索引", "NNN" not in "".join(l for l in lines if l.startswith("- `")))
        check("EAL 四种格式齐全", " ✅ " in row("EAL-M001") and " ⚠ " in row("EAL-UI008")
              and " ⚠ " in row("ERR-20260303-001") and " 🔄 " in row("G-020"))
        check("来源缺失在索引头显形", "⚠ 来源缺失：Projects/海螺姑娘/GOTCHAS.md" in idx)
        check("带状态行的未解析标题显形", "⚠ 未解析标题 2 个" in idx and "无编号的坑" in idx)
        check("未纳入来源写明", "> 未纳入：Projects/DVA" in idx and "Projects/{风险日报,星空,Financial/白泽大宗}（2026-11-05 已并入 brain 侧 canonical）" in idx)
        check("重跑条目不变",
              [l for l in lines if l.startswith("- `")] ==
              [l for l in build(docs).splitlines() if l.startswith("- `")])

    with tempfile.TemporaryDirectory() as docs2:
        os.makedirs(os.path.join(docs2, "Claude/brain/permanent"))
        write(docs2, "Claude/Projects/海螺姑娘/GOTCHAS.md",
              "# 只有模板\n\n## [ERR-YYYYMMDD-NNN] 模板\n\n## P1\n")
        idx2 = build(docs2)
        check("来源解析为 0 在索引头显形", "⚠ 来源解析为 0 条：Projects/海螺姑娘/GOTCHAS.md" in idx2)

    # 2026-11-13：经验库「同条订正」追记识别（TODO「经验索引生成器不识别同条订正」）
    with tempfile.TemporaryDirectory() as docs3:
        os.makedirs(os.path.join(docs3, "Claude/brain/permanent"))
        write(docs3, "Claude/brain/permanent/经验库.md",
              "# 经验库\n\n## cases\n\n"
              "### [EXP-20261020-005-T] 旧标题：确定性复用可靠\n**做法**：旧做法写得足够长的一行\n"
              "**⚠ 2026-11-01 同条订正（NOTE-20261101-001 · 追记不新建）**：本条的「复用」实为**巧合**——顺序一变全图重排。\n"
              "**来源**：x\n\n"
              "### [EXP-20261020-006-T] 未订正条\n**做法**：普通做法写得足够长的一行\n"
              "**⚠ 警示**：这只是普通警示，不是订正\n\n"
              "### [EXP-20261020-007-T] 订正带状态\n"
              "**⚠ 2026-11-02 同条订正（NOTE-20261102-009）**：结论已撤回。状态 ✅ 已沉淀\n")
        idx3 = build(docs3)
        row3 = lambda eid: next((l for l in idx3.splitlines() if l.startswith(f"- `{eid}`")), "")
        r5 = row3("EXP-20261020-005-T")
        check("同条订正：索引行标「已订正→指向 NOTE-20261101-001」", "已订正→指向 NOTE-20261101-001" in r5)
        check("同条订正：标题显示订正首句、原标题括注", "本条的「复用」实为巧合" in r5 and "（原：旧标题" in r5)
        check("同条订正：订正段无状态 → 沿用原判 —", " · — · " in r5)
        check("非订正的 ⚠ 追记不误标", "已订正" not in row3("EXP-20261020-006-T") and "未订正条" in row3("EXP-20261020-006-T"))
        r7 = row3("EXP-20261020-007-T")
        check("同条订正：订正段有状态 → 显示订正后状态 ✅", "已订正→指向 NOTE-20261102-009" in r7 and " ✅ " in r7)

    # 2026-11-24 G-X296：条目内多条状态行取最后一条（行首状态行 + 复核行内「 · 状态：」）；行中引用不算；无行首状态行沿用首处
    with tempfile.TemporaryDirectory() as docs4:
        os.makedirs(os.path.join(docs4, "Claude/brain/permanent"))
        write(docs4, "Claude/Projects/海螺姑娘/GOTCHAS.md",
              "# x\n\n## [ERR-20261124-101] 先闭后开\n**状态**: ✅ 已修复\n追记\n- **状态**: 🔄 复发待修\n\n"
              "## [ERR-20261124-102] 先开后复核闭\n**状态**: 🔄 已修待验\n"
              "- **独立复核（2026-11-24）**: PASS · 实读 x · 状态：✅（PASS） · 未参与实施的审核者代签\n\n"
              "## [ERR-20261124-103] 单行\n**状态**: ✅ 已解决\n\n"
              "## [ERR-20261124-104] 行中引用不算\n**状态**: ✅ 已修复\n**建议修法**: 以行首 `**状态**：🔄` 判，见「状态：🔄」\n")
        write(docs4, "Claude/brain/司南/GOTCHAS.md",
              "# x\n\n## [ERR-20261124-201] brain 先闭后开\n**状态**：✅ 该次已修\n追记\n**状态**：🔄 本形态待修\n\n"
              "## [ERR-20261124-202] brain 无行首状态行\n**根因**：x。**状态**：⚠️ 已知风险\n**追记**：y。**状态**：✅ 已修\n\n"
              "## [ERR-20261124-203] brain 行中引用不算\n**状态**：✅ 已修复\n**根因**：`status_of()` 取第一条 `**状态**` 🔄\n")
        idx4 = build(docs4)
        row4 = lambda eid: next((l for l in idx4.splitlines() if l.startswith(f"- `{eid}`")), "")
        check("多条状态行：Projects 先闭后开 → 🔄", " 🔄 " in row4("ERR-20261124-101"))
        check("多条状态行：Projects 复核行「 · 状态：✅」→ ✅", " ✅ " in row4("ERR-20261124-102"))
        check("多条状态行：单行不变", " ✅ " in row4("ERR-20261124-103"))
        check("多条状态行：Projects 行中引用不算", " ✅ " in row4("ERR-20261124-104"))
        check("多条状态行：brain 先闭后开 → 🔄", " 🔄 " in row4("ERR-20261124-201"))
        check("多条状态行：brain 无行首状态行沿用首处 ⚠", " ⚠ " in row4("ERR-20261124-202"))
        check("多条状态行：brain 行中引用不算", " ✅ " in row4("ERR-20261124-203"))

    # 参数解析（2026-11-24 · G-X236 同根第三次复发）：--help 与未知参数不得写盘；--out 只写预跑目录
    with tempfile.TemporaryDirectory() as docs5, tempfile.TemporaryDirectory() as pre:
        perm5 = os.path.join(docs5, "Claude/brain/permanent")
        os.makedirs(perm5)
        write(docs5, "Claude/brain/司南/GOTCHAS.md", "# x\n\n## [ERR-20261124-301] 参数夹具\n**状态**: 🔄 待修复\n")
        formal = [os.path.join(perm5, n) for n in ("经验索引.md", "_exchange_index.md")]

        def run(args, extra_env=None, cwd=None):
            env = {k: v for k, v in os.environ.items() if k not in ("EXP_INDEX_OUT", "EXP_EXCH_OUT")}
            env.update({"DOCS_DIR": docs5, **(extra_env or {})})
            return subprocess.run([sys.executable, "-I", GEN, *args], env=env, capture_output=True, text=True, cwd=cwd)

        untouched = lambda: not any(os.path.exists(p) for p in formal)
        r = run(["--help"])
        check("参数：--help 退出码 0 且打印用法", r.returncode == 0 and "usage" in r.stdout.lower())
        check("参数：--help 不写正式索引", untouched())
        r = run(["--bogus"])
        check("参数：未知参数退出码 2", r.returncode == 2)
        r = run(["--ou", pre])
        check("参数：缩写 --ou 不被当成 --out（退出码 2）", r.returncode == 2)
        r = run(["--out", os.path.join(pre, "不存在")])
        check("参数：--out 目录不存在退出码 2", r.returncode == 2)
        r = run(["--out", perm5])
        check("参数：--out 指向正式 permanent/ 退出码 2", r.returncode == 2)
        # 独立验收限①③（2026-11-24）：同一目录的其他写法也要拒
        side = os.path.join(docs5, "side")
        os.makedirs(side)
        os.symlink(perm5, os.path.join(side, "link"))
        variants = [("尾斜杠", perm5 + "/", None), ("相对路径", "permanent", os.path.join(docs5, "Claude/brain")),
                    ("符号链接", os.path.join(side, "link"), None)]
        upper = os.path.join(docs5, "Claude/brain/PERMANENT")
        if os.path.isdir(upper):  # 只在大小写不分的文件系统上（如 macOS APFS）测
            variants.append(("大小写变体", upper, None))
        for name, arg, cwd in variants:
            r = run(["--out", arg], cwd=cwd)
            check(f"参数：--out 指向 permanent 的{name}写法退出码 2", r.returncode == 2 and untouched())
        # 独立验收限②：DOCS_DIR 指向别处时，--out 也不能写进真实 brain 的 permanent（用假 HOME 模拟真实树，不碰真索引）
        home = os.path.join(docs5, "home")
        real_perm = os.path.join(home, "Documents/Claude/brain/permanent")
        os.makedirs(real_perm)
        r = run(["--out", real_perm], {"HOME": home})
        check("参数：--out 指向真实 brain 的 permanent（DOCS_DIR 在别处）退出码 2",
              r.returncode == 2 and not os.listdir(real_perm))
        check("参数：以上失败调用都不写正式索引", untouched() and not os.listdir(pre))
        sink = os.path.join(pre, "env")
        os.makedirs(sink)
        r = run(["--out", pre], {"EXP_INDEX_OUT": os.path.join(sink, "a.md"), "EXP_EXCH_OUT": os.path.join(sink, "b.md")})
        got = [os.path.join(pre, n) for n in ("经验索引.md", "_exchange_index.md")]
        check("参数：--out 写进预跑目录、优先于环境变量",
              r.returncode == 0 and all(os.path.exists(p) for p in got) and not os.listdir(sink))
        check("参数：--out 不写正式索引", untouched())
        r = run([])
        strip = lambda p: [l for l in open(p, encoding="utf-8").read().splitlines() if "生成：" not in l]
        check("参数：不带参数照旧写正式索引，内容与预跑一致（除生成时间行）",
              r.returncode == 0 and all(os.path.exists(p) for p in formal + got)
              and all(strip(a) == strip(b) for a, b in zip(got, formal)))

    print(f"\n{'全部通过' if not fails else f'{len(fails)} 项失败'}")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
