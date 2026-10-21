---
title: Artifact manifest 快照 2026-10-21（模式切换备份件）
tags: [模式切换, artifact, manifest, 备份]
created: 2026-10-21
updated: 2026-10-21
status: active
type: 备份
---

# Artifact Manifest 快照 — 2026-10-21

> 用途：Gateway → 官方登录模式适配的 artifact 层备份台账。来源：Gateway 壳 `mcp__cowork__list_artifacts` 实读（2026-10-21 04:4x PT）＋ Doctor 终端 `ls ~/Claude's\ workspace/Artifacts/`（2026-10-21 04:36 PT）。

## Gateway 侧（真源 · 10 板）

| id | name | updatedAt |
|---|---|---|
| pec-starry-skies | Pec Starry Skies | 2026-10-12 |
| eal-v3-event-transition | Eal V3 Event Transition | 2026-10-21 |
| x-board | X Board | 2026-10-21 |
| yuantu-starry-skies | Yuantu Starry Skies | 2026-10-21 |
| zhuzhao-jiuyin-daily | Zhuzhao Jiuyin Daily | 2026-10-20 |
| longyu-stock-library | Longyu Stock Library | 2026-10-18 |
| event-attribution-ledger | Event Attribution Ledger | 2026-08-19（此后未更新） |
| baize-weekly-dashboard | Baize Weekly Dashboard | 2026-10-18 |
| risk-daily | Risk Daily | 2026-10-20 |
| global-asset-inventory | Global Asset Inventory | 2026-10-21 |

落点：`~/Gateway-workspace/Artifacts/{id}/index.html`

## 官方侧（落后方 · 9 板 · 来自终端 ls）

`baize-weekly-dashboard` · `event-attribution-ledger` · `global-asset-inventory` · `longyu-holdings-board` · `longyu-stock-library` · `risk-daily` · `touzhijunjun-workflow` · `yuantu-starry-skies` · `zhuzhao-jiuyin-daily`

## 差异

- **官方缺 3**：`pec-starry-skies` · `eal-v3-event-transition` · `x-board`（切换后需官方壳重推，生成器在仓）
- **官方独有 2**：`touzhijunjun-workflow`（8-03 已定性幽灵板同族）· `longyu-holdings-board`（处置归 Doctor 裁）
- **交集 7**：由各班首跑 update_artifact 自然刷回（回切卡 §三原话）

## 注

- `event-attribution-ledger` 08-19 后未更新——上轮已建议不迁移（退役板），处置待 Doctor 裁。
- 本件是台账快照，非 HTML 本体备份；10 板均属可再生产物（生成器+数据在仓）。
