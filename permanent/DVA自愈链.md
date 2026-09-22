---
title: DVA 自愈链（机制图与判读判据）
tags: [DVA, 自愈, fuxi, 参考]
created: 2026-09-22
updated: 2026-09-22
status: active
type: reference
---

# DVA 自愈链 — 机制图与判读判据

> 2026-09-22 全链只读摸清（跨三日 · 读 Mac 侧 Codex 仓 + fuxi 侧 + automation 配置）。
> **用途**：判「自愈有没有跑 / 有没有推进 / 卡在哪」时，直接照这张图找面，别再从零摸。
> ⚠ 2026-09-19→26 fuxi 出游离线，链处于「诊断完备、执行受阻」；26 号回线后本图应复核一次。

## 一、三段式链路

```
[Mac 侧] Codex automation `dva-fuxi-mac`（kind=heartbeat · 每日北京 18:15）
   └─ 跑 `run_dva_self_heal.py`
        ├─ --inspect  全时段只读诊断（本地）
        ├─ --poll     只读远端观察 + 写本地进度记忆   ← 每轮都跑
        └─ --execute  SSH → [fuxi 侧] ops/bootstrap/dva_self_heal_bootstrap.py
                              └─ stdio 协议 ↔ dva_self_heal_coordinator.py
                                   └─ 唯一 retry owner，执行业务恢复
[fuxi 侧] DVA-Refill（每日北京 17:00）→ 失败则留 handoff 票据
```

**发起方在 Mac**。fuxi 只被动接受 SSH——这正是「fuxi 侧对 `dva_self_heal_startup/stdio/server` 零引用」的原因，**是设计不是断链**。

## 二、关键落点（判读时按这张表找面）

| 想看什么 | 去哪看 | 说明 |
|---|---|---|
| 配置 / 调度 / 是否 ACTIVE | `~/.codex/automations/dva-fuxi-mac/automation.toml` | 见 [[Codex自动化层]] |
| **跑没跑** | `Documents/Codex/Project Mirror/DVA/ops/state/dva-codex-supervision/state.json` → **`observedAt`** | Mac 本地进度记忆，每次 poll 更新 |
| **有没有推进** | 同上 → **`lastBusinessProgressAt`** | 最后一次业务进展；也在该目录的 `plan-*.json` 落盘时间留痕 |
| 出的诊断计划 | 同目录 `plan-{incidentId}-{evidenceFp}-{planFp}.json` | 五字段：hypothesis / minimalChange / verification / rollback / resumeScope |
| 票据（待认领） | fuxi `E:\AI\DVA\ops\state\dva-self-heal-handoffs\*.pending` | 班次失败后生成 |
| 票据被认领 | fuxi `E:\AI\DVA\ops\state\dva-refill-handoff-latest.json` | locator，出现＝被认领 |
| 班次终态 | fuxi `ops/state/refill-cycle-{cycleId}.json` | `status` / `exit_code` |
| 镜像到没到 Mac | `Documents/Database/Douyin/.dva-fuxi-mirror.json` | `run_id` / `published_at` |

## 三、三条判读判据（本场付学费换来的）

1. **fuxi 侧零写入 ≠ 自愈没跑。** `--poll` 从设计上只读远端、只写 **Mac 本地**。拿 fuxi 的写入面去判「跑没跑」，那个面**恒为零**、零判别力。（→ G-X190）
2. **`memory.md` 缺失 ≠ 从未运行。** 反例就在本链上。（→ G-X190）
3. **判「Mac 侧有没有跑」只认 `state.json` 的 `observedAt` / `lastBusinessProgressAt`。** 这是该链唯一诚实的证据面。

## 四、入口的硬闸（解释「为什么沙箱跑不了」）

`run_dva_self_heal.py` 对 `--poll`/`--record-plan`/`--execute` 有双闸：

```python
if sys.platform != "darwin" or Path(__file__).resolve() != LOCAL_ENTRY:
    → {"outcome":"ALERT","reason":"LAUNCHER_ENTRY_REFUSED"} / "SUPERVISOR_ENTRY_REFUSED"
```

`LOCAL_ENTRY` 是**硬编码**的 Mac 绝对路径。⇒ 沙箱（Linux）必拒、换个路径也必拒。**这是设计意图，不是可绕的障碍**——CC 侧只能只读判读，不能代跑。

## 五、两个已诊断的真根因（2026-09-19/20 由 VV 定位 · 均未执行）

**㈠ policy 时间戳比较 bug** —— inspect 在**自身 terminal journal 更新之前**捕获快照，policy 却拿 `observed_at` 比 inspect 的 `recordedAt`，**不可能满足的次序** ⇒ **递归的无副作用检查链**：一个合法 writer，却永不产生业务动作。
▸ 修法：inspect 只比 `issuedAt`，业务动作保留 `recordedAt` 边界。

**㈡ enrollment 错配** —— bootstrap 仍批准**更旧的 release transaction**，与已装 policy 不匹配 ⇒ 新 cycle 拿不到 coordinator enrollment。
▸ 修法：certification-only core transaction（before/after 哈希相同）+ bootstrap 升级；明文**不动**业务代码/数据/调度/原 FAILED/journal。

⚠ 两者的两个 plan 都是 `executionAuthorized: false` · `businessRuns: 0` —— **诊断完成、未执行**；且都需 fuxi 在线才能部署/认证。

## 六、边界

- 本条是**判读地图**，不是操作授权；任何 `--execute`／部署／受理票据都归既有授权链（coordinator 是唯一 retry owner，不得叠加第二套重试）。
- 权威状态文档在 Codex 侧：`Codex/Project Mirror/DVA/{README,AUDIT,GOTCHAS,PRD-self-healing}.md`——**实机优先于任何文档**。
- fuxi 侧 canonical：`E:\AI\DVA`；Mac 消费镜像 `Documents/Database/Douyin` 只读，不得反写 fuxi。

## 相关

- [[Codex自动化层]] · [[通用教训]] G-X190/191/192 · `brain/TODO.md` DVA 条（26 号回线四项补核清单）
- 日志：`logs/2026-09-22-DVA自愈链诊断与三条教训.md`
