---
name: dva-heartbeat-1815-a
description: 一次性：DVA heartbeat 自然验证窗口（北京 18:20 / +5 分），只读，结果报 Doctor
---

【DVA heartbeat 自然验证 · 第一点（+5 分钟）· 一次性 · 严格只读】

## 背景（自足）

DVA 自愈链自 2026-09-19 起**停摆七天**：09-20～09-25 连续六班全部 FAILED/75，七张自愈票据全停在 `FAILED_REQUIRES_DIAGNOSIS`（`diagnosis_owner: "codex"`、`codex_diagnosis_required: true`、`business_runs: 0`），**Mac 消费镜像七天无新代次**（最后仍是 `dva-mirror-20260918T191145Z-047034d0`）。

原因是 **fuxi-station 出游离线（09-19 晚～09-26）**，现已回归，**通道已恢复**（沙箱实测：Mac → fuxi 主机名与 IP 两条路径均通）。

消费方是 Mac 侧 Codex automation **`dva-fuxi-mac`**（`kind=heartbeat`，rrule `FREQ=DAILY;BYHOUR=3;BYMINUTE=15` ＝ PT 03:15 ＝ **北京 18:15**），入口 `run_dva_self_heal.py`。

**今天北京 18:15 是通道恢复后的第一次自然触发窗口** —— 它能否回答「这个 heartbeat 还活着吗」。

## 判据（★ 用这条，别用 memory.md）

**主判据 = Mac 侧进度记忆的 `observedAt` 是否前进。**

文件（沙箱可达，在 Documents 挂载面内）：
`/sessions/*/mnt/Documents/Codex/Project Mirror/DVA/ops/state/dva-codex-supervision/state.json`

**基线（2026-09-25 20:06 PT 实测）**：
- `observedAt` = `2026-09-21T17:01:23.595734+00:00`（**停在 09-21，四天未前进**）
- `lastBusinessProgressAt` = `2026-09-20T10:54:18.150561+00:00`
- `active` = false · `available` = false · `requiresDiagnosis` = true · `reason` = `OBSERVATION_UNAVAILABLE_OR_INVALID`

⚠ **两条已作废的错判据，勿再使用**：
① 不能用 `memory.md` 存在与否判断跑没跑（跑过也可能不写）；
② 不能拿「fuxi 侧零写入」推「Mac 侧没跑」——`--poll` 从设计上只读远端、只写 Mac 本地。

## 要做的事

**A. Mac 侧（主）**
读上述 `state.json`，报出 `observedAt` / `lastBusinessProgressAt` / `active` / `available` / `requiresDiagnosis` / `reason` 六个字段，并与基线对拍。同时报文件 mtime。

**B. fuxi 侧（辅·只读）**
```bash
K=$(ls /sessions/*/mnt/Documents/Claude/.sandbox-ssh/id_ed25519 2>/dev/null | head -1)
cp "$K" /tmp/fk && chmod 600 /tmp/fk
ssh -i /tmp/fk -o StrictHostKeyChecking=no -o ConnectTimeout=15 Codex@192.168.1.32 "<PowerShell 命令>"
```
（**禁主机名**走 IP；远端默认 PowerShell，分隔用 `;`，**禁 `&`**）
- `Get-ChildItem 'E:\AI\DVA\ops\state' | Sort LastWriteTime -Desc | Select -First 8 LastWriteTime,Length,Name`
- `Get-ChildItem 'E:\AI\DVA\ops\state\dva-self-heal-handoffs' -Force | Select LastWriteTime,Length,Name`
- `Test-Path 'E:\AI\DVA\ops\state\dva-refill-handoff-latest.json'`

**C. 顺带**：`Documents/Codex/Project Mirror/DVA/runtime/tools/fuxi/` 下 `dva_self_heal_policy.py` / `dva_self_heal_journal.py` / `ops/bootstrap/dva_self_heal_bootstrap.py` 的 mtime —— 看修法有没有开始落地。

## 报告

1. **结论一行**：`observedAt` 前进 / 未前进（附两个时间戳）
2. 六字段实值 + 文件 mtime
3. fuxi 侧 8 条 state 写入时间戳
4. 修法落地痕迹（有/无）
5. **若 `observedAt` 未前进**：明确写「未前进」，并列出**并列未排除**的两种解释——㈠ heartbeat 未触发/已停；㈡ 触发了但 `poll()` 抛异常走 `except → ALERT` 且不写 state（代码里就是这样）。**不要把两者中的任一个说成结论。**
6. **未核项**：`~/.codex`（automation 真源、memory.md）在沙箱挂载面外、不可达 —— 涉及它的判断一律标「未核」。

## 边界

**严格只读**。不得执行 `run_dva_self_heal.py` 的任何模式、不得重跑班次、不得改任何文件、**不得跑任何 git 子命令**。发现要修的问题——只报告。

本点是 **+5 分钟**观测，若显示「零变化」，**不足以判死**（诊断阶段可能不落盘）——留给第二点（+85 分钟）定案。