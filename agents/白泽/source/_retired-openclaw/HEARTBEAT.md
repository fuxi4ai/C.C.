# HEARTBEAT.md - 系统健康自动巡检

> **频率：** 每 6 小时一次
> **最后更新：** 2026-06-03

---

## 每次心跳必做

1. **Cron 健康度**：`cron list` → 失败任务立即 `cron run` 重试 → 仍失败则记录并通知
2. **Git 状态**：`git status --short` → 未提交变更超过 24h 则提醒
3. **磁盘空间**：`df -h /home` → >85% 报警，>95% 立即通知
4. **自愈脚本**：`python3 scripts/self_heal.py` → 自动修复 + 写入 `status/self_heal_alerts.json`
5. **Bridge 监控**：`python3 scripts/monitor_bridge.py` → 飞书 Bridge + 网络连通性

---

## 自愈规则

| 触发条件 | 自动处理 |
|:---------|:---------|
| Git 未提交变更 >24h | 自动 checkpoint（含变更摘要） |
| 磁盘 >85% | 清理 `__pycache__/` + `archive/` 最旧 3 文件 |
| 磁盘 >95% | 写入告警文件 + 通知老师 |
| 飞书 Bridge 异常 | 写入告警文件 |
| 网络异常 | 写入告警文件 |
| Cron 任务失败 | 自动重试（心跳流程内置） |

### 告警机制
- 所有告警 → `status/self_heal_alerts.json`
- 有告警 → `message` 工具推送
- 全部正常 → 清除告警文件

---

## 正常时

回复 `HEARTBEAT_OK`，不产生噪音

---

## 静默规则

- **静默时段**：23:00-08:00（仅严重异常通知）
- **免打扰条件**：用户明显忙碌 / 上次检查 <30min

---

*白泽 · HEARTBEAT.md v2.0 · 2026-06-03*
