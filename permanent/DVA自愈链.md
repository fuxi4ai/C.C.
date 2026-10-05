---
title: DVA 链（现行机制图与判读判据 · 含已退役旧链）
tags: [DVA, fuxi, 参考, 判读地图]
created: 2026-09-22
updated: 2026-10-04
status: active
type: reference
---

# DVA 链 — 现行机制图与判读判据

> ⚠ **2026-09-29 架构级取代**：旧「自愈闭环」链（heartbeat → `run_dva_self_heal.py` → coordinator）**已退役**；现行＝**增量协调器**（`dva_incremental_pipeline.py`）。旧链保留在本文件末尾**历史层**（只读不改，作考古）。
> **用途**：判「有没有跑 / 有没有推进 / 卡在哪」时照这张图找面，**别再从零摸**。
> **最后核验**：效果层（fuxi/Mac 落盘产物）2026-09-30 实测；配置层（Codex automation 清单）2026-10-04 本机实读已核（审计方核验：`fuxi-dva` 每日 00:00 PT · `dva-mac` 每日 06:30 PT）。沙箱对配置层仍不可达，本文件涉配置层以 2026-10-04 实读为准。

## 一、现行链（2026-09-29 起）

```
[Codex] `Fuxi-DVA-数据库驱动更新`（id `fuxi-dva` · ACTIVE · 每日 00:00 PT ＝ 北京 15:00）★已核 2026-10-04 本机实读
   └─ 采集 / 下载 / 转写 / 按 mode 分析 → 写 fuxi canonical ＋ `incremental_pipeline_runs`
[Codex] `DVA Mac 增量成果回流`（id `dva-mac` · ACTIVE · 每日 06:30 PT）★已核 2026-10-04 本机实读
   └─ 把**已登记成果**打成代次 → fuxi `ops\mirror\ready\dva-mirror-{ts}-{hash}\`
        └─ [Mac] 原子替换 `Documents/Database/Douyin/`（权威库 `DVA-Inventory/videos.sqlite3`）
```

**旧 Windows 侧已退役**（实测）：`DVA-Refill` / `DVA-Healthcheck` 于 **2026-09-27 17:58/17:59 禁用**（`State=Disabled`；旧批次恢复协议**仅保留历史**）。

## 二、现行判读表（按这张表找面）

| 想看什么 | 去哪看 | 说明 |
|---|---|---|
| **上游跑没跑 / 有无新增量** | fuxi `E:\AI\DVA\data\DVA-Inventory\videos.sqlite3` → 表 **`incremental_pipeline_runs`** | 每行一次运行：`status`（`success`/`failed`）· `phase` · `started_at` · **`source_ids` / `completed_ids`** · `errors` |
| 新内容有没有进来 | fuxi `E:\AI\DVA\data\Transcripts\{作者}\` | 看 **`CreationTime`**，别只看 mtime（mtime 会被搬运/重写刷新） |
| 新链的内容观察凭证 | fuxi `ops\state\content-observations-v1\` | 每件 = `creation-intent.json` + `creation-receipt.json` |
| **镜像代次出没出** | fuxi `E:\AI\DVA\ops\mirror\ready\` | 目录名即代次；内含 `payload/` · `manifest.json` · `payload.zip` · `windows-certutil-proof.json` |
| **代次到没到 Mac** | `Documents/Database/Douyin/.dva-fuxi-mirror.json` | `run_id`（与上格代次对拍）· `published_at` · `source_health.mode`（增量为 `INCREMENTAL_DATABASE`，schema 3） |
| Mac 权威库 | `Documents/Database/Douyin/DVA-Inventory/videos.sqlite3` | 新权威库。⚠ 旧的 `DVA-Database/dy_downloader.db`（~190 MB）是 **09-18 原件、未被替换**，读的人易误判 |
| fuxi 侧健康基线 | `E:\AI\DVA\ops\state\dva-static-certification-v1.json` · `dva-runtime-guarded-baseline.json` | 认证/基线类，非业务产物 |

⚠ **镜像代次「连出两代」未必是两次推进**：实测两代 `payload` 件数／总字节／扩展名直方图**完全相同**、仅 `payload.zip` 差 5 字节。要判真推进，比 `content_sha256` / `database_sha256`，别数代次。

## 三、判读判据（跨链通用 · 仍有效）

1. **判别力优先**：落结论前问「若反面为真，这个面会不同吗？」——不会 ⇒ 该面**零判别力**，换面，别拿它当证据。（→ [[通用教训]] G-X190）
2. **「零写入」≠「没跑」**：写不写取决于机制设计。从「没痕迹」推「没发生」，**先证「发生必然留痕」**，并**找反例**——样本同向不等于必然。（→ G-X190）
3. **`memory.md` 缺失 ≠ automation 从未运行**（实证反例，见 [[Codex自动化层]] §4）。
4. **`source_ids=[]` 有两种成因**：上游确无新片 / 采集路**静默盲采**（基线错、`sec_uid` 错、路由不全）。**单次空窗不足以证明健康**，需跨多轮观察或反向探针。
5. **`status=failed` 的行要与成功的行一起看**——只读成功行会漏掉失败那一次。
6. **「有新文件」不等于「真新采集」**：存量重转写（如 `authorized-asr12/asr21-*`）同样产生新 mtime。要看 `incremental_pipeline_runs` 的 `source_ids` 是否非空。
7. **「上游有新采集」须按作者分述**，不可整体断言——同窗口内有的作者 `source_ids` 非空、有的为空。

## 四、边界

- 本条是**判读地图**，不是操作授权；任何执行/部署/受理都归既有授权链。
- 权威状态文档在 Codex 侧 `Codex/Project Mirror/DVA/{README,AUDIT,GOTCHAS}.md`——**实机优先于任何文档**。⚠ 注意这些文档里可能残留**旧协议描述**（如「`DVA-Refill` 每日 17:00 北京」「Codex 自愈观察 18:15」），那些已随退役过期。
- fuxi 侧 canonical：`E:\AI\DVA`；Mac 消费镜像 `Documents/Database/Douyin` **只读**，不得反写 fuxi。
- **沙箱可达性**：fuxi 走 `ssh -i …/.sandbox-ssh/id_ed25519 Codex@192.168.1.32`（**禁主机名**）；Mac 侧仅 `Documents` 挂载面内可达；`~/.codex`、`~/Gateway-workspace` **不可达**。

## 相关

- [[Codex自动化层]] · [[通用教训]] G-X190 / G-X191 / G-X192
- `brain/TODO.md` 长期观察段「DVA · 增量新链的观察面」（八条待验）

---

# 历史层（2026-09-22 摸清的旧链 · 2026-09-29 退役 · 只读不改）

> 以下为**已退役**的旧「自愈闭环」链。留此仅供考古与判据溯源；**勿据以执行**。旧链的两个根因修法随架构取代一并作废。

## H1 · 旧三段式链路

```
[Mac 侧] Codex automation `dva-fuxi-mac`（kind=heartbeat · 每日北京 18:15）
   └─ 跑 `run_dva_self_heal.py`
        ├─ --inspect  全时段只读诊断（本地）
        ├─ --poll     只读远端观察 + 写本地进度记忆   ← 每轮都跑
        └─ --execute  SSH → [fuxi] ops/bootstrap/dva_self_heal_bootstrap.py
                              └─ stdio ↔ dva_self_heal_coordinator.py（唯一 retry owner）
[fuxi 侧] DVA-Refill（每日北京 17:00）→ 失败则留 handoff 票据
```

发起方在 Mac，fuxi 只被动接受 SSH——这正是「fuxi 侧对 `dva_self_heal_startup/stdio/server` 零引用」的原因，**是设计不是断链**。

## H2 · 旧落点表

| 想看什么 | 旧落点 |
|---|---|
| 跑没跑（旧） | Mac `Codex/Project Mirror/DVA/ops/state/dva-codex-supervision/state.json` → `observedAt` |
| 有无推进（旧） | 同上 → `lastBusinessProgressAt`；同目录 `plan-*.json` |
| 诊断计划（旧） | `plan-{incidentId}-{evidenceFp}-{planFp}.json`（五字段：hypothesis / minimalChange / verification / rollback / resumeScope） |
| 票据（旧） | fuxi `ops/state/dva-self-heal-handoffs/*.pending` → 兑现为 `{cycle}.json` |
| 票据被认领（旧） | fuxi `ops/state/dva-refill-handoff-latest.json`（locator） |
| 班次终态（旧） | fuxi `ops/state/refill-cycle-{cycleId}.json` |

## H3 · 旧链两个已诊断未执行的真根因（随架构取代作废）

**㈠ policy 时间戳比较 bug** —— inspect 在**自身 terminal journal 更新之前**捕获快照，policy 却拿 `observed_at` 比 inspect 的 `recordedAt`，**不可能满足的次序** ⇒ **递归的无副作用检查链**：一个合法 writer，却永不产生业务动作。（修法：inspect 只比 `issuedAt`，业务动作保留 `recordedAt` 边界。）

**㈡ enrollment 错配** —— bootstrap 仍批准**更旧的 release transaction**，与已装 policy 不匹配 ⇒ 新 cycle 拿不到 coordinator enrollment。（修法：certification-only core transaction + bootstrap 升级。）

⚠ 两者 plan 皆 `executionAuthorized: false` · `businessRuns: 0`；**Doctor 2026-09-29 裁「标取代·不执行」**（原 TODO 条已迁 `references/TODO-已完成归档.md` 的「已取消」段）。

> **H3 的迁移价值**：㈠ 是「**有合法 writer 却零副作用 ⇒ 先疑自我循环，不是门禁拒绝**」的活例（→ G-X192）；㈡ 是「**版本化事务的批准链与已装字节错配**」的活例。

## H4 · 旧入口的硬闸（解释「为什么沙箱跑不了」）

`run_dva_self_heal.py` 对 `--poll`/`--record-plan`/`--execute` 有双闸：

```python
if sys.platform != "darwin" or Path(__file__).resolve() != LOCAL_ENTRY:
    → {"outcome":"ALERT","reason":"LAUNCHER_ENTRY_REFUSED"} / "SUPERVISOR_ENTRY_REFUSED"
```

`LOCAL_ENTRY` 是**硬编码**的 Mac 绝对路径 ⇒ 沙箱（Linux）必拒、换路径也必拒。**设计意图，不是可绕的障碍。**
