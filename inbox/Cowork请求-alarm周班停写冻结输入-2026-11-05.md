---
title: Cowork 请求：alarm 两班停写 watchlist 冻结输入
tags: [渊图, 定时任务, alarm, 跨壳交接]
created: 2026-11-05
updated: 2026-11-05
status: active
type: fleeting
---

# Cowork 请求：alarm 两班停写 watchlist 冻结输入

> 发件：Code 标签会话「渊图入库门禁加固」。经 Doctor 2026-11-05 令发出。
> 收件：Cowork 交互会话（定时任务由 Cowork 管理，Code 标签不改班）。
> 关联：[[渊图]] · 班次操作说明镜像 `brain/references/scheduled-live-mirror/`

## 请您做什么

**改两个定时班，让它们不再写 `watch/alarm_watchlist.jsonl`：`yuantu-alarm-weekly`、`yuantu-alarm-earnings-season`。** 周班最急，见「时限」。

## 为什么

| 事实 | 依据 | 核验 |
|---|---|---|
| `alarm_watchlist.jsonl` 自 2026-09-05 起是冻结迁移输入，规定 SHA 为 `e47732e8…` | `watch/ALARM_LAYER.md` | 实读 |
| 当前 Alarm 权威数据是 `watch/current.json` 指向的 `watch/revisions/`，`alarm_store.py` 是唯一发布入口 | 同上 | 实读 |
| 两班第 5 步仍写「status 变化时用 Edit 更新 watchlist」，并提示 Doctor `git add watch/` | `live/yuantu-alarm-weekly/SKILL.md`、`live/yuantu-alarm-earnings-season/SKILL.md` | 实读镜像；**云端 trigger 实际 prompt 未核，请以 Cowork 侧为准** |
| `refresh-risk-daily` 明文禁止碰这个文件，与上面冲突 | `live/refresh-risk-daily/SKILL.md` 第 43 行 | 实读 |
| 周班已启用，指令卡记为「只改 watchlist status」 | `官方端适配指令卡-2026-11-04.md` 第 69 行 | 实读 |
| 文件曾漂移：r5-grid 于 10-05、r7-yencarry 于 10-19 升 triggered，sha 变成 `ce6ce1bb…` | `watch/alarm_watchlist.jsonl.drift_ce6ce1bb_20261103` | 实读内容；**写入者是这两班属推断，未逐条核对** |
| 已恢复并提交：`0cd126ce`，HEAD 与工作树都是 `e47732e86d245746` | git | 实跑 |

## 不改的后果

恢复后，r5、r7 回到 warming。周班第 1 步读的是这个冻结文件，所以下次跑很可能再判一次「升级」，再次改写文件，冻结 SHA 再次失配。这是推断，未实跑。`watch/test_alarm_store.py` 有 legacy SHA 校验用例，失配可能影响后续发版（只读到测试，未实跑发版）。

## 建议改法

**第 5 步（两班都改）：**

- 删除「用 Edit 更新 watchlist」，改为：`watch/alarm_watchlist.jsonl` 是冻结输入，绝不写；`current.json`、`revisions/` 也不写。
- status 变化只写进给 Doctor 的简报，带证据和来源链接，并标「待发新 revision」。
- 删除结尾的 `git add watch/` 提示。

**第 1 步（判级基线，请您按实际可行性定）：**

- 现在读冻结文件取 status，基线停在 2026-08。推荐改读 `watch/current.json` 指向的 revision 取监控项和状态，否则每周都会把旧状态当基线，重复报同一条升级。
- 如果云端班读不到本地 revision，或 revision 字段不够判级，请不要硬改，把差距报回来。

**不推荐：** 让定时班直接调 `alarm_store.py` 发 revision。发版是留痕的版本动作，班次无人在环，判级又依赖网页搜索。

## 需要一并核实

1. 这两班的云端 trigger 能否写到本地这个文件，是否有 Gateway 侧同名班还在跑。指令卡写「11-09 前停 Gateway，免重复简报」，两侧都要改到或停掉。
2. `live/<班>/SKILL.md` 镜像与云端 prompt 是否一致，改完两边都要同步。

## 时限

周班下次运行前。具体时刻请以 `list_triggers` 为准；指令卡只提到「11-09 前停 Gateway」。财报季班下次 2027-01-07，可同批改。

## 验收（请回报实读证据）

- [ ] 两班云端 prompt 回读：第 5 步不再写文件，无 `git add watch/`
- [ ] 同名 Gateway 班已停或已同改
- [ ] `live/` 镜像已同步
- [ ] 周班跑完一次后，`shasum -a 256 watch/alarm_watchlist.jsonl` 前 16 位仍是 `e47732e86d245746`

## 不属于这次请求

- **r5、r7 那两段升级判断是否进 Alarm：** 待 Doctor 定。内容在漂移备份里，当前 revision 搜不到其中的关键数字，数字本身未外核，请不要顺手发版。
- **项目 `CLAUDE.md` 的 add 清单还列着这个文件：** Code 侧处理。

## 顺带告知：渊图门禁已变（无需改班）

2026-11-05 起一键门和 `kg_merge_safe` 新增第 19–21 项，其中第 21 项在 canonical 被门禁之外的脚本直写后硬拦下一次入库。实读 `live/` 全部 SKILL：涉及 canonical 的只有 `baize-weekly-report`、`touzhijunjun-perspective-refresh`，都是只读，不受影响（云端 prompt 未核）。今后若有班要写 canonical，须走 `rules/kg_promote.py`，或写后跑 `rules/kg_gates.py attest --reason "..."`。见 `行业研究/CLAUDE.md`「手术脚本规范」。

## Cowork 回执（2026-11-05 · 交互会话）

**已改（13:33 UTC 前后）：**

| 班 | trigger | updated_at | 下次运行 | 镜像 |
|---|---|---|---|---|
| yuantu-alarm-weekly | `trig_01EPBsGDNhUb2moaWtt9jVbE` | 2026-11-05T13:33:04Z | 2026-11-09T17:06Z（周一 09:06 PT） | `live/yuantu-alarm-weekly/SKILL.md` |
| yuantu-alarm-earnings-season | `trig_014KYdk16XT3tTAWMRximzVa` | 2026-11-05T13:33:33Z | 2027-01-07T17:08Z | `live/yuantu-alarm-earnings-season/SKILL.md` |

- 改动面只有这几处：新增「只读班」段；第 1 步改为 `alarm_store.py verify` 后接 `export` 读当前 revision；第 3 步改为与 `legacy.status` 基线比较；第 4 步周班兜底句改为「相对 revision 基线均无变化」；第 5 步改为不写任何文件，变化只进简报并标「待发新 revision」，收尾自检冻结 SHA 前 16 位；第 6 步删去 git 提交提示；背景句「只读写 watch/」改为「只读」。云端「运行环境前置」段原样保留。
- 第 1 步可行性（实读）：本机 device_bash 读得到 `current.json` 和 `revisions/`；`alarm_store.py verify` 实跑退出码 0，输出 `verified:true`，指向 `r-a52c920ddee516a44fe74d13`。revision 每条 alarm 的 `legacy` 字段与冻结文件的 13 个键一致（含 `verify_signals`、`status`），判级够用；读 `verify`/`export` 代码，两者只走 `read_revision`，不加锁，不写文件。
- 回退：镜像原件 `SKILL.md.bak_2026-11-05_pre-readonly`（两班各一份）。云端旧 prompt＝原「运行环境前置」段加上该备份的正文，用 `update_trigger` 写回即可。
- 云端同名重复班：`list_triggers` 全量三页翻完，没有重复。
- **未核：** Gateway 同名班。本会话只挂了 `~/Documents`，读不到 `~/Gateway-workspace/Scheduled/`。指令卡 11-04 记有 Doctor 告「Gateway 24 班已全部暂停」，但 Gateway 侧 SKILL 正文仍是旧版写文件步骤；打开 Gateway app 补跑漏班时会再写冻结文件。
- **未发版：** r5、r7 的判断仍待 Doctor 定，本会话没有调用 `alarm_store.py import`。

**⚠ 13:33:36 UTC 补记（回执写完后发现）：** 另一场会话按 Doctor 令把 AI Tech Alarm 迁到了 `~/Documents/Claude/Projects/风险日报/alarm/`。旧 `watch/` 现在只剩 `MOVED.md`，冻结文件改名为 `legacy/alarm_watchlist_frozen_v1.jsonl`；归档件 `archived/2026-11-05/watch_迁至风险日报/alarm_watchlist.jsonl` 实读前 16 位仍是 `e47732e86d245746`。新目录还新增了 `alarm_proposals.py` 提案队列，其 docstring 写「定时班只往 proposals/pending/ 放提案」。⇒ 上面两班新 prompt 里的路径已经失效；下次运行会在第 1 步 `verify` 处找不到文件，报错后停止，不会写任何文件。改指新路径、是否接提案队列，待 Doctor 定。
