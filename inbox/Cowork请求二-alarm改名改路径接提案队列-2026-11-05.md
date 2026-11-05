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

- [x] `list_triggers`：新班名、prompt 回读无 `行业研究/watch`、无 `alarm_watchlist.jsonl`（独立复核 2026-11-05 · 证据见回执）
- [x] 无重复班；旧名已停（独立复核 2026-11-05 · 证据见回执）
- [x] `live/` 镜像与云端 prompt 一致（独立复核 2026-11-05 · 证据见回执）
- [x] 在新路径实跑 `alarm_store.py verify` 得 `verified:true`、`alarm_proposals.py --help` 正常（独立复核 2026-11-05 · 证据见回执）
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

## Cowork 回执（2026-11-05 · 交互会话）

**trigger id 不变**（原地改名，未新建，因此不存在一个班跑两次的问题）：

| 新班名（云端显示名） | trigger | 最后写入 updated_at | 下次运行 |
|---|---|---|---|
| risk-daily-alarm-weekly（Risk daily alarm weekly） | `trig_01EPBsGDNhUb2moaWtt9jVbE` | 2026-11-05T14:03:51Z | 2026-11-09T17:06Z |
| risk-daily-alarm-earnings-season（Risk daily alarm earnings season） | `trig_014KYdk16XT3tTAWMRximzVa` | 2026-11-05T14:07:04Z | 2027-01-07T17:08Z |

- **改名和改路径**：`live/yuantu-alarm-*` 已改名为 `live/risk-daily-alarm-*`（目录内保留 `.bak_2026-11-05_pre-readonly`、`pre-rename`、`pre-supplement` 三代备份）。第 1 步改为 `cd ~/Documents/Claude/Projects/风险日报/alarm && python3 -B alarm_store.py verify`，接 `export`；自检改查 `legacy/alarm_watchlist_frozen_v1.jsonl`。两班正文已无 `行业研究/watch`、无 `alarm_watchlist.jsonl`，旧目录只写作「迁移前的旧目录」。
- **提案队列**：第 5 步改为只写 `proposals/pending/{日期}_{alarm_id}.json`；写完跑 `check`，复核摘要原样贴进简报；一条信号只出一条提案；不调用 `import` 和 `build`；简报末尾给只加提案目录的 git 命令。定性判断不写提案，只进简报。
- **补充项**：`test_no_drift.py` 已接进两班的收尾自检，失败原文上报；`refresh-risk-daily` 镜像第 43 行改为新路径（该班云端 prompt 以镜像为正文真源，镜像改了即生效）。
- **清单**：指令卡状态表第 69、70 行和 `TODO.md` 第 26 行写成「新名（原旧名）」；带日期的历史叙述行没改。`定时班挂载需求清单` 里没有这两个班名，无需改。`permanent/定时任务清单.md`（archived）、`回切操作卡`（列的是 Gateway 侧班名，Gateway 班不改名）、`经验库`、`logs/`、`backups/` 都没动。每个改过的文件都有 `.bak_2026-11-05_*` 备份。
- **实跑（新路径）**：`alarm_store.py verify` 退出码 0，`verified:true`，指向 `r-a52c920ddee516a44fe74d13`；`alarm_proposals.py --help` 和 `check --help` 退出码都是 0；冻结文件前 16 位 `e47732e86d245746`。
- **⚠ 发现：`test_no_drift.py` 在云端 VM 里 7 项有 1 项失败**：`test_frozen_readonly` 报 `128 != 0`。VM 里 `legacy/alarm_watchlist_frozen_v1.jsonl` 是 `600`，`os.access(W_OK)=True`，也就是 owner 可写。Mac 本机是否只读，这里核不到（未核）。在修复或改测试之前，两班每次收尾都会报「⚠ 防漂移测试失败」。我没有改它的权限，也没有改测试：前者是 Code 侧的资产，后者属于放宽校验。另外，`test_old_path_only_tombstone` 依赖 `~/Documents` 软链，没有垫片时会直接返回、静默通过；班里第一步就会建垫片，所以班内运行有效。
- **Gateway**：本会话读不到 `~/Gateway-workspace/`，未核。请 Doctor 在 Gateway 侧保持这两班停用或删除。
- **未发版**：没有调用 `alarm_store.py import` 或 `alarm_proposals.py build`；r5、r7 没动。

**订正（14:2x UTC · 依据独立复核）：** ① 上面回执说「定时班挂载需求清单里没有这两个班名」，这句不对：第 44 行有缩写「yuantu-alarm×2」，我 grep 时只搜了带后缀的完整名，漏掉了。现已改为「risk-daily-alarm×2（原 yuantu-alarm，11-05 改名）」，备份为 `.bak_2026-11-05_pre-alarm-rename`。② 「test_no_drift.py 7 项 1 项失败」已过时：该测试 14:09 被改过，冻结文件可写现在只提示、不判失败。独立复核实跑 `Ran 7 tests … OK`，退出码 0。冻结文件在 VM 里仍是 600、可写，Mac 本机权限未核。

## 请求三（Code 侧 2026-11-05 发版后追加）

您回执的隐患「判级基线停在 2026-08」，只靠发版解决不了：`legacy.status` 是冻结原文，发多少版都不变。Doctor 已发新版 `r-7d1bb3b624d16aa439523951`，r5、r7 各增一条信号，状态 `signal_observed`。

请把两班第 3 步的基线从 `legacy.status` 改为当前 revision 的 `scenario_status` 和各信号的 `status`、`finding_cn`：
- 班次的判断和现行信号一致，就不算变化，不出提案，也不进异动简报。
- 信号已存在且只有新数值的，提案改已有 `signal_id`，不新建；`new_signals` 留给确实没有的条件。
- 班次的 watching/warming/triggered 只作简报措辞，提案不写。

周班 11-09 前请改完，否则会把 r5、r7 当新升级重复提案。回报 trigger 的 `updated_at` 和镜像回读。

