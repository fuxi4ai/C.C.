# GOTCHAS · 工作区

## 🐛 已知易错点

### 🔴 高优先级
- [ ] **Cron SessionKey 幽灵事件** — `/new` 或 `/reset` 后旧 sessionKey 继续生效，cron 投递到已废弃的 session，新 session 收不到任何定时任务结果。**修复**：每次新 session 启动后第 7 步自动刷新 sessionKey（2026-05-13 曾导致梦境 cron 跑空数小时，经验来自九儿）
- [ ] **Heartbeat 告警遗漏** — 巡检发现异常但回复时未报告，导致问题静默流过。**修复**：严格按 HEARTBEAT.md 执行规则，有异常必须输出异常摘要

### 🟡 中优先级
- [ ] s3fs 挂载有缓存问题，文件可能不同步到 TOS 控制台 → 用 Python SDK 上传
- [ ] Gateway 重启后 defaultModel 字段可能被删 → 需要恢复脚本
- [ ] 不同 Agent 之间文件系统不互通 → 用 TOS 共享盘中转
- [ ] **Cron 新旧版本双重执行** — 更新 cron 时旧版可能仍然 enabled，导致任务跑两遍。**修复**：更新时检查并禁用旧版（2026-05-20 发现）
- [x] **dream-state.json 缺失** — AGENTS.md `/new` 规则引用了 `~/.openclaw/dream-data/dream-state.json` 但文件不存在。**修复**：已初始化文件（2026-05-24 周度优化）
- [ ] **长耗时 subprocess 卡死 session** — 项目审核脚本无 timeout 导致 session 挂起。**修复**：所有 subprocess 调用必须设 timeout（2026-05-23 session crash）
- [ ] **Conch 周扫连续失败** — consecutiveErrors=2，报错 `Error: [1500] Unknown error`。可能原因：扫描范围过大导致 timeout（timeoutSeconds=300），或 Phase 1.6 数据健康检查卡住。**待排查**：手动跑一次观察（2026-05-31 发现）
- [ ] **旧脚本路径残留** — `build_market_db.py` 仍引用 `dragon-palace/` 旧路径，`update_800_stocks_*.py` 已被 `update_market_data.py` 替代但未清理（2026-06-03 发现）
- [ ] **ALTER RENAME 幂等碰撞误判** — 改主库退役表时 `ALTER TABLE x RENAME TO y` 报 `no such table: x`，但 `.tables`/`PRAGMA quick_check` 显示末态已正确（x 无、y 在、ok）＝重命名已生效、二次点名才报错。**处置**：看末态别看报错，末态对就别回滚（2026-07-17 fx_daily 退役发现）

### 🟢 低优先级
- [ ] memory/ 日记连续性有断档 (4月16日→5月5日)

## ✅ 已解决
- [x] SKILL.md 缺失（6 个已补齐）(2026-05-06)
- [x] 龙灵/龙宫路径命名冲突 → 架构重构为热区/冷区 (2026-05-07)
