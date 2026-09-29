---
name: dva-selfheal-1815-completion-check
description: 一次性：DVA 自愈 18:15 首考的第二点核查（完成态），只读，结果报 Doctor
---

【DVA 自愈链 18:15 首考 · 第二点核查（完成态）· 一次性 · 严格只读】

## 背景（自足）

DVA 的每日失败自愈由 **Mac 侧「本地唯一 heartbeat」**驱动，每日**北京 18:15** 触发（宿主 Codex，模式 `failed_runs_only`），业务恢复只由唯一 coordinator 执行。2026-09-19 北京 17:00 的 DVA-Refill 班失败，exit **75**（＝ `FINANCE_PENDING_HANDOFF`，**设计内退出码**），17:08:13 留下一个 `.pending` 票据。

**今天 18:15 是该 heartbeat 恢复 ACTIVE 后的首次自然点火。** 本任务是**第二点**核查（北京约 19:40，即 +85 分钟后），用来给出「完成态」结论；第一点核查（北京 18:20 / +5 分钟）另有一个一次性任务，看的是「有没有开始」。

**为什么需要第二点**：heartbeat 先做只读诊断（`run_dva_self_heal.py --inspect`），诊断阶段**可能完全不碰 fuxi**，因此 +5 分钟那一点出现「零变化」**不足以判定未点火**。+85 分钟这一点才够区分「真的没动」与「动了但当时还没落盘」。

## 连接方式

```bash
K=$(ls /sessions/*/mnt/Documents/Claude/.sandbox-ssh/id_ed25519 2>/dev/null | head -1)
cp "$K" /tmp/fk && chmod 600 /tmp/fk
ssh -i /tmp/fk -o StrictHostKeyChecking=no -o ConnectTimeout=15 Codex@192.168.1.32 "<PowerShell 命令>"
```

**禁主机名**走 IP；远端默认 PowerShell，分隔用 `;`，**禁 `&`**。先 `(Get-Date).ToString('yyyy-MM-dd HH:mm:ss')` 对表。

## 基线（2026-09-19 北京 17:30:27 实测）

- locator `E:\AI\DVA\ops\state\dva-refill-handoff-latest.json` → **不存在（False）**
- `ops\state\dva-self-heal-handoffs\` 仅一件：`.refill-cycle-20260919T090001620Z.ce4f60e1cceaa1fad6dd723772733714e30a9b83e63fc303abe803fdb35ee686.pending`（1,180 B，17:08:13）
- `ops\state` 最新写入停在 **17:08:13**；班次 `refill-cycle-20260919T090001620Z` · FAILED · exit 75

## 要读的

1. `Test-Path 'E:\AI\DVA\ops\state\dva-refill-handoff-latest.json'`
2. `Get-ChildItem 'E:\AI\DVA\ops\state\dva-self-heal-handoffs' -Force | Select LastWriteTime,Length,Name`
3. `Get-ChildItem 'E:\AI\DVA\ops\state' | Sort LastWriteTime -Desc | Select -First 15 LastWriteTime,Length,Name | Format-Table -AutoSize`
4. `Get-ChildItem 'E:\AI\DVA\ops\logs' | Sort LastWriteTime -Desc | Select -First 6 LastWriteTime,Length,Name | Format-Table -AutoSize`
5. `Get-ChildItem 'E:\AI\DVA\ops\mirror' -Recurse | Sort LastWriteTime -Desc | Select -First 10 LastWriteTime,Length,FullName | Format-Table -AutoSize`
6. `Get-ChildItem 'E:\AI\DVA\ops\failures' | Sort LastWriteTime -Desc | Select -First 4 LastWriteTime,Length,Name | Format-Table -AutoSize`

若有 18:15 之后的新动作，只读打开对应 journal / receipt / state JSON，**取关键字段与时间戳，别整份 dump**。

## 判据

- **点火且推进**：locator 出现，且 `ops/state` 或 `ops/mirror` 有 18:15 之后的新写入（新 journal / receipt / campaign 前进 / mirror 新代次）
- **点火但停住**：locator 出现但无后续写入 —— 值得警惕，说明认领了却没走完
- **未点火**：三条全与基线一致、无任何 18:15 后写入
- 如实描述，**不要硬套**。也注意区分：写入了但内容是失败诊断，与「没写入」是两回事。

## 报告格式

1. **结论一行**：点火且推进 / 点火但停住 / 未点火
2. 远端对表时刻
3. **时间线**：基线 → 现在，逐条列出关键 LastWriteTime 变化；零变化就直说「零变化」
4. **与第一点（+5 分钟）对照**：若第一点结论已知，说明两点是否一致
5. **若未点火**：列出**已知可能原因之首**＝`failed_runs_only` 未必把 exit 75（设计内 FINANCE_PENDING_HANDOFF）计为 failed run，故 heartbeat 可能按设计就不动作。标明这是**假设，未核实**，需与 Codex 侧配置对账
6. **未核项**：heartbeat 的具体配置在 Codex 侧沙箱不可达处，说明哪些核不了

## 边界（硬）

- **严格只读**。不得执行 `--execute`、不得重跑任何班、不得修改/创建/删除任何文件、**不得跑任何 git 子命令**。
- 发现需要修的问题 —— **只报告，不动手**，更不要替它点火（入口有 darwin + 路径双闸，本就跑不了）。