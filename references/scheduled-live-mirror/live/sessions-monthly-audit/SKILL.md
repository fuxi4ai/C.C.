---
name: sessions-monthly-audit
description: 每月 1 日 20:00 PT 只读盘点本地会话树（大小/会话数/超 45 天未归档），超阈提醒 Doctor 归档；执行与删除闸门归 Doctor 终端，本班无删除权。
---

你是 CC 的月频盘点班（2026-10-16 Doctor 裁定：只盘点+提醒归档，执行与删除闸门归 Doctor 终端，本班无删除权）。

步骤：
1. 只读统计会话树 `/Users/lunarabbit/Library/Application Support/Claude-3p/local-agent-mode-sessions/`（Glob/Read 文件工具，或 bash `du`/计数）。若可达：统计会话总数、总大小（GB）、mtime 超 45 天的会话目录数、单目录 Top3 大小。
2. 若不可达（挂载/权限拒绝）：重试不超过 2 次；仍不可达则读上次盘点报告 `brain/permanent/_sessions_monthly_audit.md` 最后一条记录——若距今 >35 天输出 ⚠ 提醒；<35 天输出正常说明。（brain 路径在沙箱内探测：`~/Documents/Claude/brain` 或 `/sessions/*/mnt/Documents/Claude/brain`，取存在者。）
3. 每次运行把一行结果**追加**到 `brain/permanent/_sessions_monthly_audit.md`（不可写则只在输出中报告），格式：`- {YYYY-MM-DD} 盘点：会话 {N} 场 · {S} GB · 超45天 {M} 个 · 树{可达/不可达} · 动作：{正常/⚠提醒归档}`。不修改既有历史行。
4. 红线（违反即失败）：不删除/移动任何文件；不动 `memory/`、`uploads/` 目录；不跑任何 git 命令；不代执行清理。
5. 提醒判据（任一满足即在输出首行标 ⚠）：总大小 >1 GB；会话数 >400；超 45 天未归档数较上次记录增长 >100；树不可达且上次记录 >35 天。
6. 输出格式：首行结论（正常 / ⚠ 提醒归档）；次行盘点数或不可达说明；若 ⚠，贴 Doctor 终端手动盘点命令：
```bash
du -sh ~/Library/Application\ Support/Claude-3p/local-agent-mode-sessions
ls -d ~/Library/Application\ Support/Claude-3p/local-agent-mode-sessions/* | wc -l
find ~/Library/Application\ Support/Claude-3p/local-agent-mode-sessions -maxdepth 1 -type d -mtime +45 | wc -l
```
7. 归档执行范本（供 Doctor 参考，本班不执行）：brain 日志 `logs/2026-10-13-本地会话清理归档.md`——删除闸门＝冷归档 fuxi `F:\Mac_Backup\cc_sessions\` 双端 SHA 逐位一致。