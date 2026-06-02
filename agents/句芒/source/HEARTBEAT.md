# HEARTBEAT.md

## 频率：每 6 小时一次

## 职责边界
- **心跳**：轻量级高频巡检（<10 tool calls，不产生文件变更）
- **海螺**：深度项目整理（每周自动 + 手动触发）
- **冥想**：核心文件审计（Gateway 重启后 + 每月一次）

---

## 巡检项目（全部必做）

### 1. Git 健康
```bash
git status --short | wc -l          # 未提交变更数量
git status --short                  # 列出前 10 条
```
**告警阈值**：>5 个未提交 → 提醒哥哥

### 2. Memory 连续性
- 检查 `memory/` 下今天和昨天的日记文件是否存在
- 检查最近 7 天是否有 >2 天空白
**告警阈值**：今天日记缺失 OR 最近 7 天空白 >2 天 → 提醒

### 3. 回收站
```bash
find .trash/ -maxdepth 1 -mtime +7 | wc -l    # 超 7 天文件数
du -sh .trash/ 2>/dev/null                     # 回收站总大小
```
**告警阈值**：有超 7 天文件（次日自动删）OR 回收站 >200MB → 提醒

### 4. 磁盘占用（快速）
```bash
du -sh skills/ tools/ scripts/ quant_research/ database/ archive/ .trash/ data_history/ 2>/dev/null
```
**告警阈值**：单目录 >500MB → 记录趋势

### 5. Cron Job 状态
```
cron list（检查每个 job 的 consecutiveErrors 和 lastRunStatus）
```
**告警阈值**：任一 job consecutiveErrors >0 → 提醒

### 6. TODO 进度
- 读 TODO.md，检查 Active 项是否有进展
- 有超过 7 天未更新的 Active 任务 → 提醒

---

## 执行规则

1. **安静时间**：23:00-08:00 跳过巡检，只回复 HEARTBEAT_OK（紧急除外）
2. **无异常**：回复 HEARTBEAT_OK
3. **有异常**：回复异常摘要（简短，不超过 5 条），不包含 HEARTBEAT_OK
4. **不产生变更**：心跳只读不写，不 commit、不移动文件、不创建新文件
5. **发现严重问题**：记录到 `temp/heartbeat-issues.md`（追加模式），让哥哥醒来后查看

---

## 自检（每周日重置）

每周日凌晨 3:00 Dream 周优化时，顺便检查本文件是否需要调整巡检项/阈值。
值。
