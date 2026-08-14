---
name: brain-monthly-checkup
description: 每月初跑 meditation 心灵与记忆健康自检：折叠上月 logs + 记忆指标 + 数灵人格层 + 警告
---

执行 Doctor 的 brain 月度自检（meditation：心灵 + 记忆健康）。

步骤 1：运行自检脚本（apply 模式）
```bash
python3 ~/Documents/Claude/Projects/海螺姑娘/meditation/meditation.py --json
```
（脚本前身 brain_checkup.py，2.0 起更名 meditation 并加心灵维度。）

这个脚本会自动：
- 把上个月 logs/ 根目录下的日志折叠到 logs/YYYY-MM/ 子目录
- 采集记忆健康指标（logs/inbox/permanent/graphify 体积、项目子目录文件数）
- 采集心灵健康指标（数灵 白泽/烛阴/句芒 的性格档案/长期记忆时效/归位漂移）
- 在 logs/checkups/YYYY-MM-DD-checkup.md 生成报告
- 自动 git commit

脚本会输出一个 JSON 摘要到 stdout，包含 folded_count / warnings / stats / soul / report_path。

步骤 2：解析 JSON，给 Doctor 一份简短回报，结构是：

🧘 Meditation 月度自检 — YYYY-MM-DD
═══════════════════════════════
✓ 折叠 N 条 logs → logs/YYYY-MM/
✓ 记忆：N 条本月 logs / N 篇 permanent / X MB graphify
✓ 心灵：N/3 数灵健康[，归位漂移 N]

[如果有 warnings，列出来；否则写 "✓ 全部健康"]

报告：[file:// 链接到 report_path]

[只在 warnings 中提到 inbox 积压或 permanent 长期未更新时，加一条建议：是否现在运行 /consolidate-memory ?]
[没有 warnings 就不加任何建议]

注意事项：
- 不要主动运行 /consolidate-memory，只提示；那是 LLM 重活，需要 Doctor 主动触发
- 报告路径用 file:// 协议，方便 Doctor 直接点击查看
- 整个回报保持 < 12 行，clean 风格，没有警告就不要硬塞建议