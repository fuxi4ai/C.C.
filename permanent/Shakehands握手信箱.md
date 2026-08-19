---
title: Shake hands 握手信箱
tags: [reference, 协作, VV]
created: 2026-08-19
updated: 2026-08-19
status: active
type: permanent
---

# Shake hands 握手信箱

> CC ↔ VV 的通信基础设施（`~/Documents/4AI/Shake hands/`）。**非 git 仓**（2026-08-19 实核）。

## 结构

- `to CC/` —— VV 来信（验收回执、审查报告）
- `to VV/` —— CC 去信（执行件、对账回执）
- `archived/` —— 历史归档（`to-CC/`、`to-VV/` 两个子目录）
- `scheduled/` —— 定期任务机器通道（touzhijunjun 试点中）
- 存续性契约文档（`collaboration-needs`、`CC致VV-协作需求.md`、`PRD-定期更新-DVA.md`、`fuxi-station操作指南`、`README`×2、`spec/`）——**不是沟通记录，删了会破坏协议，永不清除**

## 判定口径

- 「已完成」**没有机器可判的状态字段**，只能按内容判定（收件→执行→回执闭环）
- 清理类操作走普通工作流（PRD 需 Doctor 显式触发「写交付标准」才立；否则不立 PRD 按既有授权工作流执行）
- 删除是不可逆操作：范围（删哪些信）+ 判定口径 + 删除方式三维度先与 Doctor 对齐，快照留档后再删
- 首轮 rm 会被 Documents 挂载拦（Operation not permitted）——走 `allow_cowork_file_delete` 流程申请删除权限

## 最近一次清理（2026-08-19）

- 范围：`to CC/` 12 封 DVA fuxi 批次回执 + `to VV/` 19 封执行件 + 2 个 `.__wtest` 残留 → 71→38
- PRD：`brain/logs/checkpoints/2026-08-19_Shakehands清理_PRD.md`（awaiting_acceptance 待 Doctor 总 ✓）
- 注意：真删不可逆，旧回执已物理删除
