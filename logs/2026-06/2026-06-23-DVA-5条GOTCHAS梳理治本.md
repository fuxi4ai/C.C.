---
title: 会话日志 2026-06-23 — DVA 5 条 GOTCHAS 梳理治本
tags: [log, DVA]
created: 2026-06-23
updated: 2026-06-23
status: active
type: log
project: DVA
---

# 会话日志 — 2026-06-23

**项目**：DVA
**主题**：5 条未闭环 GOTCHAS 逐一梳理 + 分级处理

---

## 完成的工作

- 核实「5 个 GOTCHAS」实指：权威库 `Projects/DVA/GOTCHAS.md`（46 条）非 ✅ 状态正好 5 条，与提示吻合。
- 发现并修复索引漂移：brain 索引「当前未闭环」只列 3 条且 2 条已过期，比权威库旧（「5 vs 3」）。
- #4 `[BUG-20260618-002]` 治本：`dva.js:1359` `parseInt(...) || 5` 改 `Number.isFinite(parsedLimit) ? parsedLimit : 5`，`--limit 0` 正确表示全部。`node --check` 通过。
- #3 `[BUG-20260618-001]` 治本：`dyd/storage/database.py` `_get_conn()` connect 后加 `PRAGMA journal_mode=WAL` + `busy_timeout=5000`（带 `[DVA 本地补丁]` 注释锚）。`py_compile` 通过；Mac 本地实跑打印 `journal_mode = wal`。
- #2 `[BUG-20260505-003]` `dyd/~` 残留目录：Doctor Mac 端 `rm -rf` 已清除（沙箱核实不存在）。
- #1 `[RISK-20260617-001]` 沙箱 DB guard、#5 `[INFRA-20260618-003]` 图文 .webp 403：正式归档为「已接受约束」/「won't-fix·外部失效」，权威库 + 索引均标注。
- 两仓提交：brain 仓 commit+push 成功（`fuxi4ai/C.C.` main `c60a4f5..bb280df`）；DVA 主仓本地 commit（`25adfed`）。

## 做出的决策

| 决策 | 原因 | 影响 |
|------|------|------|
| #3 治本采用 fork 第三方 DYD（改 database.py），而非只用分库规避法 | Doctor 选「再加治本 #3」；WAL+busy_timeout 根治跨进程锁 | 建了 fork 点，DYD 升级须手动 rebase 此补丁（注释锚便于定位） |
| #1/#5 不修，正式接受 | #1 是防孤儿空表的有意兜底；#5 是抖音侧渲染失效，非脚本可控 | 降噪：不再当「待修」反复占注意力 |
| DVA 主仓保持本地仓，不配 remote | Doctor 确认 DVA 一直当本地 git 仓 | commit 留本地，不推远端 |
| 验收脚本 `Event loop is closed` 判为无害 | 我临时脚本未关 aiosqlite 连接的退出噪音，PRAGMA 已执行成功（打印 wal） | 补丁本身无问题 |

## 遗留问题 / 待办

- [ ] 权威库 `Projects/DVA/GOTCHAS.md`「六、统计」表停在旧数 21 条（实际 46 条），与本轮无关，留作可选清理。
- [ ] #3 WAL 在 FUSE/挂载盘有 I/O 风险（INFRA-20260614-003 已落 /tmp 规避）；DYD 未来升级时记得 rebase `[DVA 本地补丁 2026-06-23]`。
- [ ] 长期容忍项未除根：DYD 文件名截断丢 aweme_id、单链接 harvest 不 seed DB。

## 相关笔记

- [[GOTCHAS]] — Projects/DVA/GOTCHAS.md（权威坑库）
- [[系统概览]]
