---
name: bak-diaoyan-20260827
description: 渊图 bak_20260820_diaoyan 保护期到期提醒（08-27 摘 protect 并归档）
---

你是 CC，执行渊图 bak_20260820_diaoyan 保护期到期提醒班（一次性）。背景：`~/Documents/Database/行业研究/` 下 `.conchconfig.yml` 的 protect 列表含 `mapping/行业知识图谱_完整数据库.json.bak_20260820_diaoyan`（2026-08-20 调研情报局入库场回滚点 · Doctor 批 P1 延后 7 天至 08-27）。今天 2026-08-27 到期。

执行：
1. 现核现状（只读）：`ls -la ~/Documents/Database/行业研究/mapping/*.bak_20260820_diaoyan*` 与 `.conchconfig.yml` 中 protect 段是否仍含该条。
2. 向 Doctor 报告并贴出归档命令（不在沙箱跑任何 git 子命令或 conch 命令——归档批是 Doctor 终端动作）：

```bash
cd ~/Documents/Database/行业研究
# 摘 protect：从 .conchconfig.yml 的 protect 列表删除 bak_20260820_diaoyan 行
# 归档（按 08-20 既定裁定「P1 延后 7 天」→ 移 archived/）：
mkdir -p archived
mv "mapping/行业知识图谱_完整数据库.json.bak_20260820_diaoyan" archived/
```

3. 报告格式：现状一行 + 命令块 + 一句话建议（若 Doctor 已自行处置则确认并报告闭环，不重复要求执行）。
4. 边界：不改任何其他文件；不动 canonical 图谱；不跑 git 子命令。完成后更新 brain/TODO.md 中「渊图 · bak_20260820_diaoyan 归档」条目的执行状态注记（Edit 追加，不改 checkbox——勾销权归 Doctor）。