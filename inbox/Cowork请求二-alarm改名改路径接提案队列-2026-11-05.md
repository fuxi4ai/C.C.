---
title: Cowork 请求二：alarm 两班改名、改路径、接提案队列
tags: [风险日报, 定时任务, alarm, 跨壳交接]
created: 2026-11-05
updated: 2026-11-05
status: active
type: fleeting
---

# Cowork 请求二：alarm 两班改名、改路径、接提案队列

> 发件：Code 标签会话。经 Doctor 2026-11-05 令。承接第一份请求（只读班，您已完成，感谢）。
> 关联：[[风险日报]] · `Projects/风险日报/alarm/ALARM_LAYER.md`

## 背景

Doctor 裁定：AI Tech Alarm 属于**风险日报**，不属于渊图。文件已迁，旧文件已归档。

| 项 | 旧 | 新 |
|---|---|---|
| 目录 | `~/Documents/Database/行业研究/watch/` | `~/Documents/Claude/Projects/风险日报/alarm/` |
| 冻结输入 | `watch/alarm_watchlist.jsonl` | `alarm/legacy/alarm_watchlist_frozen_v1.jsonl`（只读，SHA 不变 `e47732e8…`） |
| 旧目录现状 | | 只剩 `MOVED.md`；归档在 `行业研究/archived/2026-11-05/watch_迁至风险日报/` |

**不改的后果：** 周班第 1 步的 `cd .../watch && python3 -B alarm_store.py verify` 现在必然失败，它会报错停止，无法判级。下次运行 2026-11-09T17:06Z（您回报的时间），须在此前改完。

## 请您做

**1. 改名（两班）**

| 旧 | 新 |
|---|---|
| `yuantu-alarm-weekly` | `risk-daily-alarm-weekly` |
| `yuantu-alarm-earnings-season` | `risk-daily-alarm-earnings-season` |

- 说明里的「渊图警报监控」改为「Risk Daily · AI Tech Alarm 监控」。
- trigger 能改名就原地改；不能改名就新建后停用旧的，并回报新 trigger id，避免一个班跑两次。
- `live/` 镜像目录、`官方端适配指令卡`、`定时班挂载需求清单`、`brain/TODO.md` 等现行清单里的班名同步。`logs/` 和归档不用改。

**2. 改路径（两班）**

- 第 1 步改为 `cd ~/Documents/Claude/Projects/风险日报/alarm && python3 -B alarm_store.py verify`，接 `export`。
- 「只读班」段和第 5 步里的 `watch/` 路径、`alarm_watchlist.jsonl` 全部换成新路径和新文件名。
- 收尾自检改查 `legacy/alarm_watchlist_frozen_v1.jsonl` 的 SHA 前 16 位。
- `refresh-risk-daily` 第 43 行禁令里的路径同步；它的构建走 `render_alarm_tab.py`，已改好，不用动代码。

**3. 接提案队列（Doctor 已裁「进提案队列」）**

现在的第 5 步「不写任何文件」改为：

- 判出变化且有**来源、时间、数值和可比较的阈值**：在 `alarm/proposals/pending/{日期}_{alarm_id}.json` 写一条提案，字段见 `alarm/alarm_proposals.py` 文件头。
- 写完必须跑 `python3 -B alarm_proposals.py check <提案>`，退出码非 0 就不算交付，错误原文报给 Doctor。
- 定性判断，或拿不到数值的：不写提案，只进简报。
- 仍然绝不写 `legacy/`、`current.json`、`revisions/`，**不调用 `alarm_store.py import`、不调用 `build`**。
- 简报末尾列出本次新提案的文件名，写「待 Doctor 复核」。

第 6 步：提案会产生未提交文件，请提示 Doctor 终端 `git -C ~/Documents/Claude/Projects/风险日报 add alarm/proposals/pending && git -C ~/Documents/Claude/Projects/风险日报 commit`，不要 `git add` 其他路径（该仓常有并行改动）。

## Gateway 风险（您上次报的未核项）

Gateway 同名班的 SKILL 正文仍是写文件的旧版，打开 Gateway app 补跑漏班时可能重建旧路径文件。新路径下它不会碰到冻结输入；`alarm/test_no_drift.py` 会发现旧路径出现副本。请提醒 Doctor：这两班在 Gateway 侧保持停用或删除。

## 验收（请回报实读证据）

- [ ] `list_triggers`：新班名、prompt 回读无 `行业研究/watch`、无 `alarm_watchlist.jsonl`
- [ ] 无重复班；旧名已停
- [ ] `live/` 镜像与云端 prompt 一致
- [ ] 在新路径实跑 `alarm_store.py verify` 得 `verified:true`、`alarm_proposals.py --help` 正常
- [ ] 11-09 周班跑完：`python3 -B alarm/test_no_drift.py` 通过

## 补充（Code 侧 2026-11-05 05:50 PT 追加）

已从 `live/` 镜像看到两班改了名、改了路径、接了提案队列（未核云端 prompt）。还差：

- `refresh-risk-daily` 第 43 行禁令仍写旧路径 `watch/alarm_watchlist.jsonl`，改成 `alarm/legacy/`、`alarm/current.json`、`alarm/revisions/`。
- 两班收尾自检加一步：`python3 -B ~/Documents/Claude/Projects/风险日报/alarm/test_no_drift.py`，失败把原文报给 Doctor。它比只查 SHA 多查只读权限、revision 链和旧路径有无副本。
- `alarm_proposals.py check` 现在会打印复核摘要，请把摘要原样放进简报。同一信号不能同时被两条提案修改，一条信号只出一条提案。
- 请回报上面验收清单的实读证据和新 trigger id。

## 不在这次请求里

- **r5、r7 判断是否发版：** 待 Doctor 定，请不要发版。内容在 `alarm/legacy/drift_ce6ce1bb_20261103.jsonl`，未外核。
- **`风险日报/test_narrative_score.py` 第 4d 条失败：** Code 侧跟进。
