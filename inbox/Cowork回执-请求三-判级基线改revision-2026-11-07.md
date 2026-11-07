---
title: Cowork 回执·请求三：alarm 两班判级基线由 legacy.status 改为当前 revision v2 信号状态
tags: [风险日报, 定时任务, alarm, 跨壳交接]
created: 2026-11-07
updated: 2026-11-07
status: active
type: fleeting
---

# Cowork 回执·请求三：alarm 两班判级基线改 revision（2026-11-07 · Doctor 裁 18A）

> 执行者：Cowork 主会话委派的实施 subagent。关联：[[风险日报]] · `Projects/风险日报/alarm/ALARM_LAYER.md` · GOTCHAS `ERR-20261105-101`。
> 原 inbox 位置：alarm/ 下无 inbox 目录，按「Cowork请求二」回执所在 `brain/inbox/` 照放。

## 改动面（两件镜像 · 改法一致）

- `brain/references/scheduled-live-mirror/live/risk-daily-alarm-weekly/SKILL.md`（备份 `_bak/SKILL.md.bak_2026-11-07_18A`）
- `brain/references/scheduled-live-mirror/live/risk-daily-alarm-earnings-season/SKILL.md`（备份 `_bak/SKILL.md.bak_2026-11-07_18A`）
- 仅动步骤 1 的字段清单一句与步骤 3 判级一行；步骤 2/4/5/6、硬约束、背景段字节未动。**云端 trigger prompt 未改**（本 subagent 无 trigger 工具；镜像为正文真源，需 Doctor/主会话同步到云端）。

## 改前 → 改后

**步骤 1（字段清单）**
- 改前：`…legacy.status（判级基线：watching/warming/triggered），以及 v2 机器判据 scenario_status 与 signals[]（status/condition_cn/finding_cn，仅供参考，不改写）。`
- 改后：`…legacy.verify_signals（仅作核验清单与历史参考），以及判级基线＝当前 revision 的 v2 信号状态：scenario_status（unknown / monitoring / signal_observed / threshold_met）与 signals[] 逐条的 signal_id / status（met / not_met / unknown）/ test / condition_cn / finding_cn / observed_at_utc，并记下 trigger_all / warming_any 两个 signal_id 组合。legacy.status 是冻结迁移原文，不再作判级基线（2026-11-07 Doctor 裁 18A）。`

**步骤 3（判级规则）**
- 改前（周班）：`判级：无变化＝watching；信号开始异动＝warming；阈值击穿＝triggered。逐条与第 1 步的 legacy.status 基线比较。`
- 改前（财报季）：`判级 watching→warming→triggered，同常态任务口径；逐条与第 1 步的 legacy.status 基线比较。`
- 改后（两班同文，财报季前缀「同常态任务口径；」）：基线＝第 1 步 export 出的当前 revision v2 信号状态；逐条对 `signals[]` 判本班观察状态（met / not_met / unknown，只有来源、回读时间、数值与比较式齐备才判 met/not_met），与 revision 该 `signal_id` 的 `status` 比较——不同即为变化；警报级别按组合推：`warming_any` 任一 met → `signal_observed`（≈旧 warming），`trigger_all` 全部 met → `threshold_met`（≈旧 triggered），已核未满足 → `monitoring`（≈旧 watching），缺证据 → `unknown`；与 revision `scenario_status` 比较得「无变化/升级/回落」。简报写「<signal_id>：revision <旧 status> → 本班观察 <新 status>」，不再用 watching/warming/triggered 作结论。

## 真实键名依据（只读实跑 `alarm_store.py export` · 2026-11-07）

- envelope：`revision_id` = `r-7d1bb3b624d16aa439523951`，`pack.as_of_utc` = `2026-11-05T14:19:33Z`，`sha256`。
- `pack.alarms[]` 键：`id name legacy scenario_status signals trigger_all warming_any window evidence_status pricing_status …`
- `signals[]` 键：`signal_id name status test condition_cn finding_cn observed_at_utc source_ids`；`status` 实值集合 {met, not_met, unknown}。
- `scenario_status` 实值集合 {unknown, signal_observed}（ALARM_LAYER.md 另定义 monitoring / threshold_met）。
- 当前 7 条：r2-collectiveFCF / r5-grid / r7-yencarry = signal_observed（各有 1 条 met），其余 4 条 unknown；`legacy.status` 则是 triggered×3 / warming×3 / watching×1——两套口径不一致，正是改基线的理由。

## 验证

- 两镜像 `grep legacy.status`：仅剩「不再作判级基线」与「不是 legacy.status」两处说明性出现，无作为基线的用法。
- `diff` 两镜像步骤 1-3：仅财报季前缀「同常态任务口径；」一处差异，其余判级文字逐字一致。
- `alarm_store.py export` rc=0；未调用 import / 未写 alarm/ 任何文件。

## 待办（非本回执范围）

- 云端 trigger prompt 同步（Doctor/主会话）。
- 11-09 周班自然验：简报应出现「<signal_id>：revision … → 本班观察 …」句式。
