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
        write(docs, "Claude/Projects/Financial/宏观研究体系/EAL/GOTCHAS.md",
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

    print(f"\n{'全部通过' if not fails else f'{len(fails)} 项失败'}")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
