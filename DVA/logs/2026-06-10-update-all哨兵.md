---
title: 2026-06-10 update-all 哨兵检查
tags: [DVA, log, cron, 哨兵]
created: 2026-06-10
updated: 2026-06-10
status: active
type: log
project: DVA
---

# 2026-06-10 update-all 哨兵检查（周三 05:08）

**结论：🚩 今天没跑，且疑似 cron 从未部署成功。**

## 发现

- 预期日志 `Projects/DVA/logs/cron/update-all-2026-06.log` 不存在。
- 更严重：`Projects/DVA/logs/` 整个目录都不存在。run-update-all.sh 每次运行都会 `mkdir -p logs/cron` 并追加日志（脚本 L40-50），所以目录缺失 = **该脚本从未通过 cron（或手动）完整运行过**，不只是今天没跑。
- 脚本本身在位且可执行（`run-update-all.sh`，3.8K，rwx，6/4 更新），内容正常：PATH 补齐、加载 `dyd/.env.dva` 与 `~/.dva_secrets`、按月写日志。

## 可能原因

1. crontab 条目 `0 5 * * 3,6 .../run-update-all.sh` 未实际安装（`crontab -l` 验证）。
2. Mac 在 05:00 处于睡眠（cron 不补跑错过的任务）。
3. macOS 未给 cron「完全磁盘访问」权限，无法进 Documents。

## 给 Doctor 的手动补跑 / 排查命令（macOS 终端执行）

```bash
# 1. 确认 cron 是否部署
crontab -l

# 2. 手动补跑本周更新
bash /Users/lunarabbit/Documents/Claude/Projects/DVA/run-update-all.sh

# 3. 跑完查看日志
cat /Users/lunarabbit/Documents/Claude/Projects/DVA/logs/cron/update-all-$(date +%Y-%m).log
```

若 `crontab -l` 为空，按 run-update-all.sh 末尾 SETUP 注释部署；若 cron 已在但没产生日志，检查 系统设置 → 隐私与安全性 → 完全磁盘访问 中 `/usr/sbin/cron` 是否勾选。

——哨兵（只读检查，未重跑、未动 DVA 数据）
