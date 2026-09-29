---
name: dva-heartbeat-1815-b
description: 一次性：DVA heartbeat 自然验证窗口（北京 19:40 / +85 分）完成态核查，只读，结果报 Doctor
---

【DVA heartbeat 自然验证 · 第二点（+85 分钟 · 定案）· 一次性 · 严格只读】

## 背景（自足）

DVA 自愈链自 2026-09-19 起**停摆七天**：09-20～09-25 连续六班全部 FAILED/75，七张自愈票据全停在 `FAILED_REQUIRES_DIAGNOSIS`（`diagnosis_owner: "codex"`、`codex_diagnosis_required: true`、`business_runs: 0`、`automatic_redispatch: false`），**Mac 消费镜像七天无新代次**（最后 `dva-mirror-20260918T191145Z-047034d0`）。

原因是 **fuxi-station 出游离线（09-19 晚～09-26）**，现已回归、通道恢复。消费方＝Mac 侧 Codex automation **`dva-fuxi-mac`**（`kind=heartbeat`，PT 03:15 ＝ **北京 18:15**）。

**本点是定案点**：第一点（北京 18:20 / +5 分）若显示「零变化」，**不足以判死**（诊断阶段可能根本不落盘）；+85 分钟这一点才够区分「真没动」与「动了但当时还没落盘」。

## 判据（★ 用这条，别用 memory.md）

**主判据 = Mac 侧进度记忆的 `observedAt` 是否前进。**

`/sessions/*/mnt/Documents/Codex/Project Mirror/DVA/ops/state/dva-codex-supervision/state.json`

**基线（2026-09-25 20:06 PT 实测）**：
- `observedAt` = `2026-09-21T17:01:23.595734+00:00`（**停在 09-21**）
- `lastBusinessProgressAt` = `2026-09-20T10:54:18.150561+00:00`
- `active` = false · `available` = false · `requiresDiagnosis` = true · `reason` = `OBSERVATION_UNAVAILABLE_OR_INVALID`

⚠ **两条已作废的错判据**：① 不用 `memory.md` 判断跑没跑；② 不拿「fuxi 侧零写入」推「Mac 侧没跑」（`--poll` 从设计上不写 fuxi）。

## 要做的事

**A. Mac 侧（主 · 定案依据）**
上述 `state.json` 六字段 + mtime，与基线对拍。另看 `dva-codex-supervision/` 目录下有无**新的 plan 文件**（`plan-*.json`，看 mtime 与文件名）。

**B. fuxi 侧（只读）**
```bash
K=$(ls /sessions/*/mnt/Documents/Claude/.sandbox-ssh/id_ed25519 2>/dev/null | head -1)
cp "$K" /tmp/fk && chmod 600 /tmp/fk
ssh -i /tmp/fk -o StrictHostKeyChecking=no -o ConnectTimeout=15 Codex@192.168.1.32 "<PowerShell 命令>"
```
（**禁主机名**走 IP；PowerShell 分隔用 `;`，**禁 `&`**）
- 今天北京 17:00 班是否已跑：`Get-ChildItem 'E:\AI\DVA\ops\state' -Filter 'refill-cycle-*.json' | Sort LastWriteTime -Desc | Select -First 3 LastWriteTime,Length,Name`
- 票据：`Get-ChildItem 'E:\AI\DVA\ops\state\dva-self-heal-handoffs' -Force | Sort LastWriteTime -Desc | Select -First 5 LastWriteTime,Length,Name`
- 最新失败：`Get-Content 'E:\AI\DVA\ops\state\dva-failure-latest.json' -Encoding UTF8`（只取关键字段：`outcome` / `diagnosis_owner` / `codex_diagnosis_required` / `cycle_run_id` / `exit_code`，**别整份 dump**）
- 镜像：`Get-ChildItem 'E:\AI\DVA\ops\mirror\ready' | Sort LastWriteTime -Desc | Select -First 3 LastWriteTime,Name`

**C. 修法落地痕迹**：Mac 侧 `Codex/Project Mirror/DVA/runtime/tools/fuxi/` 的 `dva_self_heal_policy.py` / `dva_self_heal_journal.py` + `ops/bootstrap/dva_self_heal_bootstrap.py` 的 mtime。

## 报告

1. **结论一行**：`observedAt` **前进** / **未前进**（附两个时间戳对比）
2. 六字段实值 + state.json mtime + `dva-codex-supervision/` 有无新 plan
3. fuxi 侧：今日班次状态 / 票据 / `dva-failure-latest.json` 关键字段 / 镜像代次是否前进
4. 修法落地痕迹（有/无）
5. **若 `observedAt` 未前进**：写「未前进」，并列**两种未排除的解释**——㈠ heartbeat 未触发或已停；㈡ 触发了但 `poll()` 抛异常走 `except → ALERT` 且不写 state。**不得把任一说成结论。** 另说明：`~/.codex`（automation 真源）不可达，**无法从沙箱判定它是否 armed**。
6. **若 `observedAt` 前进**：给出前进到的时刻，并核 `available` 是否转为 true、`reason` 是否不再 `OBSERVATION_UNAVAILABLE`。

## 边界

**严格只读**。不得执行 `run_dva_self_heal.py` 任何模式、不得重跑班次、不得改任何文件、**不得跑任何 git 子命令**。发现问题只报告，不动手、不替它点火。