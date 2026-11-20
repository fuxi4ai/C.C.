---
title: 会话日志 2026-11-20 — brain-dream 每日班建班
tags: [log, brain, scheduled, dream]
created: 2026-11-20
updated: 2026-11-20
status: active
type: log
project: brain（跨项目 · 基础设施）
---

# 会话日志 — 2026-11-20

**项目**：brain（跨项目 · 基础设施）
**主题**：按 Doctor 交来的建班单，在官方云端建 `brain-dream-daily` 定时班

---

## 完成的工作

- 建班前三查（实跑实读）：
  - `list_triggers` 翻完 4 页全量，没有同名或同类的 dream 班。
  - 本机时区：03:40 的真相层抽取是 Mac 本地 launchd（`.tools/launchd/com.brain.transcript-ingest.plist`，Hour 3 / Minute 40）。`permanent/定时任务清单.md` 写明 cron 走本机美西时区，现有云端班也全部用 `CRON_TZ=America/Los_Angeles`，所以定为美西。
  - 盘上都有：`.skills/brain-dream/SKILL.md`（16,670 B）、`.tools/dream_collect.py`；正文写的「04:30，排在 03:40 之后」与排班一致。
- 建班：`brain-dream-daily` · `trig_01PZU9bKngpB7yDrCuNUdHQ3` · `CRON_TZ=America/Los_Angeles 30 4 * * *` · `requires_local_device=true` · `permission_mode=auto`。04:30 没按抖动规则往前挪（这个班要排在事件之后，按规则保持原时刻）；平台给的下次运行是 UTC 12:37（美西 04:37，平台随机延后几分钟）。
- 提示词：Doctor 交来的原文**一字未改**，前面加了一段与其他云端班同款的「运行环境前置」（全部命令走 device_bash、开工先建 `~/Documents` 软链、挂载缺失就停、不申请删除权限）。理由：云端会话用 Read 读 `~/Documents` 会读空，然后误报「技能正文不可达」。已向 Doctor 列明这一点可以否决。
- 回读发现 `folders_state=NONE`（建班不带 folders 参数时的已知行为，见经验库 4469 行追记 ①）→ 请 Doctor 在 Cowork 里把 Documents 挂上 → Doctor 回「done」→ 按 id 回读：`FOLDERS_STATE_PRESENT` · `["/Users/lunarabbit/Documents"]`，prompt、cron、自动执行都没变。
- 朗读：ElevenLabs Hiddleston-CN。第一次落 `/tmp`，`play_audio` 拒绝（白名单只认 `Documents/Claude/临时文件`），改落临时文件后播放成功；`rm` 报 EPERM（挂载区默认禁删），音频留在临时文件，等 conch 清空。

## 做出的决策

| 决策 | 原因 | 影响 |
|------|------|------|
| 时区用 America/Los_Angeles | 前置的抽取任务是 Mac 本地 launchd，本机时区经清单与现有班双证为美西 | 04:30 本地，与抽取同一时区，次序有保证 |
| 04:30 不做抖动前挪 | 规则写明「排在某事件之后的班保持原时刻」 | 平台仍会随机延后几分钟（实测下次运行 04:37） |
| 提示词前加运行环境前置（推荐即默认，可否决） | 云端班读 Mac 文件必须走 device_bash，其余云端班都有这一段 | 否决的话改回原文，但改提示词要 Doctor 在关联这台 Mac 的会话里批一次 |
| 不给 dream 班建 `scheduled-live-mirror/live/` 镜像目录 | 镜像现在只给推看板的班当正文真源用；dream 班的正文真源就是技能本身 | 镜像里没有这个班；需要的话另行裁定 |

## 遗留问题 / 待办

- [ ] 首跑核验（已挂进 TODO）：`logs/dream/2026-11-20-dream.md` 有没有生成、`permanent/_dream_state.json` 有没有生成、`first_run` 基线是否记了。
- 隐患（记录在这里，不挂 TODO）：Mac 凌晨要是睡着，当天那一次会报挂载缺失直接跳过，云端班不会补跑；连着几天睡眠会漏核一部分 7 天待办期内的日志。

## 记忆分拣

本场两条平台事实都已经在库里，按 v3.7 查重后不新建：
- `create_trigger` 不带 folders → `folders_state=NONE` → 经验库 4469 行追记 ①（命中）。
- `play_audio` 白名单只认 `Documents/Claude/临时文件`、`rm` 报 EPERM → 经验库 4012 行追记（2026-11-18，命中）。

## 相关笔记

- [[2026-11-19_Dream技能_PRD]]（`logs/checkpoints/`）
- [[2026-11-19_真相层_PRD]]（`logs/checkpoints/`）
- [[经验库]]（官方云端迁移条 · 2026-11-04 追记）
