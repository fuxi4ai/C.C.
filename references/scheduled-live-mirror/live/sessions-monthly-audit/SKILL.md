---
name: sessions-monthly-audit
description: 每月 1 日 20:00 PT 只读盘点官方 app 本地会话树（会话数/大小/较上次增量/超 45 天），增量超阈提醒 Doctor 归档；执行与删除闸门归 Doctor 终端，本班无删除权。
---

你是 CC 的月频盘点班（2026-10-16 Doctor 裁定：只盘点+提醒归档，执行与删除闸门归 Doctor 终端，本班无删除权；2026-11-04 Doctor 裁：盘点对象改为官方 app 会话树、阈值改增量制）。

**盘点对象**：官方 app 本地会话树 `/Users/lunarabbit/Library/Application Support/Claude/local-agent-mode-sessions/`。会话目录在**深度 3**（第 1 层是账户目录与 `skills-plugin`，只数第 1 层会严重少数）。
Gateway 旧树 `Claude-3p/local-agent-mode-sessions/` 自 2026-11-04 停用冻结（基线 1233 场 · 21 GB），走一次性冷归档、**不在本班盘点范围**。

步骤：
1. 只读统计会话树（bash `du`/`find`）。若可达：会话数（深度 3 目录数）、总大小（GB）、超 45 天未改动的会话目录数、近 30 天改动体积。
2. 若不可达（云端虚拟机读不到 `~/Library` 属预期）：读上次盘点记录 `~/Documents/Claude/brain/permanent/_sessions_monthly_audit.md` 最后一条——距今 >35 天输出 ⚠ 提醒；否则输出正常说明，并贴第 6 步命令请 Doctor 终端跑。
3. 每次运行把一行结果**追加**到 `~/Documents/Claude/brain/permanent/_sessions_monthly_audit.md`（不可写则只在输出中报告），格式：`- {YYYY-MM-DD} 盘点（官方树）：会话 {N} 场 · {S} GB · 超45天 {M} 个 · 较上次 +{ΔN} 场/+{ΔS} GB · 树{可达/不可达} · 动作：{正常/⚠提醒归档}`。
4. 红线（违反即失败）：不删除/移动任何文件；不动 `memory/`、`uploads/` 目录；不跑任何 git 命令；不代执行清理。
5. 提醒判据（增量制 · 任一满足即在输出首行标 ⚠）：较上次记录 **+1 GB 以上** 或 **+200 场以上**；超 45 天未改动数较上次 **+100 以上**；树不可达且上次记录 >35 天。
6. 输出格式：首行结论（正常 / ⚠ 提醒归档）；次行盘点数或不可达说明；不可达或 ⚠ 时贴 Doctor 终端只读盘点命令：
```bash
d="$HOME/Library/Application Support/Claude/local-agent-mode-sessions"
du -sh "$d"
echo "会话数: $(find "$d" -mindepth 3 -maxdepth 3 -type d | wc -l)"
echo "超45天: $(find "$d" -mindepth 3 -maxdepth 3 -type d -mtime +45 | wc -l)"
echo "近30天改动体积: $(find "$d" -type f -mtime -30 -exec stat -f%z {} + 2>/dev/null | awk '{s+=$1} END{printf "%.0f MB\n", s/1048576}')"
```
7. 归档执行范本（供 Doctor 参考，本班不执行）：brain 日志 `logs/2026-10-13-本地会话清理归档.md`——删除闸门＝冷归档 fuxi `F:\Mac_Backup\cc_sessions\` 双端 SHA 逐位一致。
