---
name: dva-selfheal-1815-firstrun-check
description: 一次性：核 DVA 自愈链 18:15（北京）首考是否点火，只读，结果直接报 Doctor
---

【DVA 自愈链 18:15 首考观察 · 一次性 · 严格只读】

## 背景（自足，无需查历史会话）

DVA（抖音视频分析生产系统）的每日失败自愈由 **Mac 侧「本地唯一 heartbeat」**驱动，每日**北京 18:15** 跑一次，宿主是 Codex，模式 `failed_runs_only`；它消费 fuxi 侧 `E:\AI\DVA\ops\state\dva-self-heal-handoffs\` 下的票据，业务恢复由唯一 coordinator 执行（入口 `run_dva_self_heal.py --inspect` / `--execute`，见 `~/Documents/Codex/Project Mirror/DVA/README.md` 的「关键入口」与 L60）。

2026-09-19 北京 17:00 的 DVA-Refill 班失败，exit **75**（＝ `FINANCE_PENDING_HANDOFF`，**设计内退出码**，不是硬故障），在北京 17:08:13 留下一个 `.pending` 票据。**今天 18:15 是该 heartbeat 恢复 ACTIVE 后的第一次自然点火**，本轮任务就是核它有没有点着。

## 连接方式

沙箱 → fuxi-station 直连（注意：**禁主机名**，走 IP；远端默认 PowerShell，命令分隔用 `;`，**禁用 `&`**）：

```bash
K=$(ls /sessions/*/mnt/Documents/Claude/.sandbox-ssh/id_ed25519 2>/dev/null | head -1)
cp "$K" /tmp/fk && chmod 600 /tmp/fk
ssh -i /tmp/fk -o StrictHostKeyChecking=no -o ConnectTimeout=15 Codex@192.168.1.32 "<PowerShell 命令>"
```

先跑 `(Get-Date).ToString('yyyy-MM-dd HH:mm:ss')` 对表，确认远端当前北京时刻。

## 基线（2026-09-19 北京 17:30:27 实测，作为对照）

- locator `E:\AI\DVA\ops\state\dva-refill-handoff-latest.json` → **不存在（False）**
- `ops\state\dva-self-heal-handoffs\` 只有一件：`.refill-cycle-20260919T090001620Z.ce4f60e1cceaa1fad6dd723772733714e30a9b83e63fc303abe803fdb35ee686.pending`（1,180 B，2026-09-19 17:08:13）
- `ops\state` 最新写入停在 **17:08:13**（dva-refill-latest.json / refill-cycle-20260919T090001620Z.json / 同名 .parent.json / dva-self-heal-handoffs）
- 班次 JSON：`refill-cycle-20260919T090001620Z` · status=FAILED · exit_code=75 · attempt_limit=1 · retry_count=0 · minimum_retry_minutes=75

## 要读的五件（全部只读）

1. `Test-Path 'E:\AI\DVA\ops\state\dva-refill-handoff-latest.json'`
2. `Get-ChildItem 'E:\AI\DVA\ops\state\dva-self-heal-handoffs' -Force | Select LastWriteTime,Length,Name`
3. `Get-ChildItem 'E:\AI\DVA\ops\state' | Sort LastWriteTime -Desc | Select -First 12 LastWriteTime,Length,Name | Format-Table -AutoSize`
4. `Get-ChildItem 'E:\AI\DVA\ops\logs' | Sort LastWriteTime -Desc | Select -First 5 LastWriteTime,Length,Name | Format-Table -AutoSize`
5. `Get-ChildItem 'E:\AI\DVA\ops\mirror' -Recurse | Sort LastWriteTime -Desc | Select -First 8 LastWriteTime,Length,FullName | Format-Table -AutoSize`

若发现 18:15 之后确实有新动作，再只读打开对应的 journal / receipt / state JSON 摘要（**别整份 dump**，取关键字段与时间戳即可）。

## 判据

- **点火**：locator 出现 · `.pending` 变为/伴随 `{cycle}.json` 形态的正式票据 · `ops/state` 出现 18:15 之后的新写入（新 journal / receipt / mirror 动作 / campaign 状态前进）
- **未点火**：以上三条全部与基线一致，无任何 18:15 后写入
- **半点火**：locator 出现但无后续动作，或有新写入但票据未变 —— **如实描述，不要硬套前两档**

## 报告格式

1. **结论一行**：点火 / 未点火 / 半点火（附一句最关键的时间戳证据）
2. **对表**：远端实测北京时刻
3. **时间线**：基线 → 现在的关键 LastWriteTime 变化（没有变化就直说「零变化」）
4. **若是未点火**：明确写「未点火，未见任何 18:15 后写入」，并列出**已知可能原因之首**＝`failed_runs_only` 未必把 exit 75（设计内 FINANCE_PENDING_HANDOFF）计为 failed run，故 heartbeat 可能按设计就不动作——这是**假设，未核实**，需与 Codex 侧配置对账才能定论
5. **未核项**：说明哪些你没法核（heartbeat 的具体配置在 Codex 侧 `~/.codex` 一类沙箱不可达处）

## 边界（硬）

- **严格只读**。不得执行 `run_dva_self_heal.py` 的 `--execute`，不得重跑任何班，不得修改/创建/删除 fuxi 或 Mac 侧任何文件，**不得跑任何 git 子命令**。
- 发现需要修的问题 —— **只报告，不动手**。
- 本任务是「核验」不是「修复」；若判据显示未点火，也不要尝试替它点火（那超出授权，且入口有 darwin+路径双闸本就跑不了）。