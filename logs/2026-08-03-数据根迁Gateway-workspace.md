---
title: 会话日志 2026-08-03 — 数据根迁Gateway-workspace
tags: [log, 数灵转移, gateway, 挂载保护, 定时任务]
created: 2026-08-03
updated: 2026-08-03
status: active
type: log
project: 数灵转移
---

# 会话日志 — 2026-08-03（跨午夜场 · 始 08-02 22:49 PDT · Kimi K3 壳内）

**项目**：数灵转移（19 班迁移收尾 · 数据根迁出 Documents 连坐区）
**主题**：数据根迁Gateway-workspace

> 承上：`logs/2026-08-02-E验收与19班迁Kimi壳.md`。本场从 /resume 开场，主线 = 终封 diff 核验 → 挂载保护机制深聊 → 数据根迁出全程执行与定案。

---

## 完成的工作

- **终封 diff 核验（Doctor 终端跑）**：19 班 = 18 OK + 2 DIFF。longyu-weekly-dualscorer 为**预期 DIFF**（F2 注记唯一刻意偏离）；touzhijunjun-perspective-refresh 为**意外 DIFF**——定位两行漂移：subagent 分组并行段整行缺失 + 文件末尾换行符丢失（镜像 mtime 08-01 22:28 vs store 08-02 13:49）。已通过 MCP `update_scheduled_task` 以镜像为准修正。
- **挂载保护机制定案（三条新事实）**：① **保护跟随 store 位置、不随路径名**——新根 `~/Gateway-workspace/Scheduled` 挂载同报 "overlaps a protected host location"；迁出换来的是父目录解放、**不是** store 可读性。② **改 setting 只重写注册表指针、不搬文件**（Doctor 确认）；19 班 + 6 artifact 的 path 自动指向新根，零手工。③ `~/Documents` 与 `~/Documents/Claude` 整挂恢复，三年连坐解除（G-X53 a 案二次落地）。
- **归并 Cowork 目录之议（Doctor 问）→ 否决**：归并目录只得文件层共享，注册表照旧分裂 → 双向鬼影 + 双写者 + 回切冗余归零；且 workspace 树沙箱同样不可达，连可读性收益都没有。维持两 store 分治 + 镜像供读 + rsync 回切。
- **命名定案 `~/Gateway-workspace/`**：Doctor 否掉 `Developer-workspace`（撞 macOS `~/Developer` 与 D11「dev 模式=Claude Code CLI」语义）→ 改 vendor 中立名，对齐既有三环境词汇（桌面应用 / gateway / Claude Code）。
- **迁移执行**：CC 出完整目标树（Scheduled 21 目录/31 文件 + Artifacts 6）与搬前 `find > /tmp/pre-move.txt` 核对法；Doctor 终端手动 mv + Settings 改根。实测账目：Scheduled 恰好 19 班（`_archived/` 与 handshake 空目录未随搬——内容在镜像 git 有全备份，**存档此后归镜像/git 管，store 保持「只有活班」**）；Artifacts 7 个——逮到幽灵 `龙鱼五力个股库看板/`（index.html mtime 2026-07-05 20:28，07-05 拷贝事件族第四例，`touzhijunjun-workflow` 同族），定照 handshake 先例归档。
- **落盘五处（会话中已完成）**：D14（[[数灵转移/architecture/决策记录]]）· 回切卡 · `scheduler_snapshot.py`（GATEWAY_TREE 常量/DEAD_TREE 语义改注释）· G-X53 结局段 · TODO 观察条改写 + `permanent/全局偏好-Settings镜像.md`。
- **C1 确认**：scheduler-weekly-audit 已于 08-02 20:00:59 PDT 在本壳首点火（lastRunAt 实据）——19 班迁移后首个 cron 触发成立。

## 做出的决策

| 决策 | 原因 | 影响 |
|------|------|------|
| 数据根迁 `~/Gateway-workspace/`（vendor 中立） | 不只 Kimi——gateway 模式诸壳共用；对齐三环境词汇 | Documents 连坐解除；保护随迁新根 |
| 不归并 Cowork 目录、不指 Cowork workspace | 注册表分裂是结构性的（文件层≠注册表层）；双写绝不可行 | 两 store 分治 + 镜像 + rsync 回切架构不变 |
| touzhijunjun 漂移以镜像为准补齐 | 镜像（08-01 22:28）内容更新且完整，store 是迁移拷贝时丢行 | 班 prompt 恢复完整；终封 diff 应转 OK |
| `_archived` 不随迁、归镜像/git 管 | store 保持「只有活班」；归档内容镜像有全备份 | 归档单一真源 = brain 镜像（git tracked） |

## 遗留问题 / 待办

- [ ] **Doctor 终端复跑终封 diff**——touzhijunjun 修正后应 19 OK（longyu 若已 sed 修正则为 19/19 全 OK 收官）
- [ ] **longyu 步骤 2/3 修正状态核实**（TODO 观察条提及「本次 longyu sed 修正」，待确认是否已落 store）
- [ ] **龙鱼看板幽灵归档**（Doctor 终端：`mv ~/Gateway-workspace/Artifacts/龙鱼五力个股库看板{,_DEPRECATED_20260803}` 或入 `_archived/`）
- [ ] **C4**：明早日更班首 fire 观察（简报产出 / 放回校验 / 并发判据三条）
- [ ] Doctor 动作余项：V.V. ferry · Fable 5 API 密钥/预算 · 本次 git 提交（命令见 /save 回报）

## 相关笔记

- [[数灵转移/architecture/决策记录]] D14 · `permanent/通用教训.md` G-X53 结局段 · `references/scheduled-live-mirror/回切操作卡.md`
- `permanent/全局偏好-Settings镜像.md` · `.tools/scheduler_snapshot.py`（GATEWAY_TREE）
- 上游：logs/2026-08-02-E验收与19班迁Kimi壳.md · logs/2026-08-02-扫尾批与巡检镜像步.md
