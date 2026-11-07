---
name: handshake-consumer
description: 消费 Shake Hands 机器握手通道（方案 B）。触发：每日 09:00 定时任务自动调用，或用户说「消费握手」「跑 consumer」「处理 to CC/scheduled」。扫 `to CC/scheduled/*.latest.json` → schema+checksum+run_id 幂等校验 → 按 task_id 路由 → 走 brain 铁律落盘 → 写 ack 回执 → 报告 Doctor。Codex(V.V.) 主跑重活只吐数据，规矩全在 Claude 侧执行。
---

# handshake-consumer — 消费机器握手通道（方案 B · Claude 侧）

## 定位

方案 B 的 **Claude 消费端**：Codex(V.V.) 定时跑抓取/提炼/核实，把结构化数据写进 `to CC/scheduled/{task_id}.latest.json`；本 skill 校验后按 task_id 路由，**走 brain 铁律**落盘，并写 ack 回执。

- 握手层契约：`~/Documents/4AI/Shake hands/scheduled/README.md`
- 信封 schema：`~/Documents/4AI/Shake hands/spec/handshake-schema.json`
- 辅助脚本：本 skill 的 `scripts/consume.py`（纯 stdlib，机械活；判断与落盘由本指令让 agent 走铁律）

## 前置 · 路径 env + 挂载（G-X45）

握手层在 `~/Documents/4AI/Shake hands`。**gateway 平铺挂载下无统一 Documents 根**，须先设 env 指向挂载点：

```bash
# Mac 原生：默认路径即可，无需设 env
# gateway/沙箱：先确认 4AI 挂载点，再导出
export SHAKE_HANDS_ROOT="$(dirname $(find /sessions/*/mnt/4AI -maxdepth 1 -name 'Shake hands' 2>/dev/null | head -1))/Shake hands"
# 若上句为空 → 4AI 未挂载，向 Doctor 报告「握手层未挂载」并停，不臆测路径
```

`consume.py` 认 `SHAKE_HANDS_ROOT`；无则回退 `~/Documents/4AI/Shake hands`。

## 流程

### Step 1 · 扫描 + 校验 + 幂等

```bash
python3 <skill>/scripts/consume.py scan
```

输出三类：
- `ready`：schema+checksum 过、run_id 未消费 → **本轮要处理**
- `skipped_idempotent`：run_id 已在 ack 里记过 → 跳过（幂等，不重复落盘）
- `rejected`：校验失败（schema/checksum/版本漂移）→ **不消费**，为每个 rejected 写 ack `status: failed`（附 reason），并在报告里列出交 Doctor

若 `ready` 为空 → 报告「本轮无待消费握手」并退出。

### Step 2 · 逐个路由（按 task_id）

对每个 ready 项，按 `task_id` 进对应路由（见下「路由表」）。路由前先看 `sample` 字段：

- **`sample: true`** → **dry-run**：只验证校验+路由+落盘映射是否成立，**绝不写 canonical/wiki/库**；报告"样本干跑通过/不通过"，ack 里 `dry_run: true`。（数据真实性铁律）
- **`sample: false`** → 正常消费，按路由落盘。

### Step 3 · 落盘走 brain 铁律（关键）

无论哪个路由，落盘一律遵守：
- **数据真实性铁律**：payload 里查不到/留空的字段，落盘也留空标「待核验」，绝不补编。
- **promote 需 Doctor 显式**：只追加视角层 / 提候选，**绝不 promote 进 canonical**。
- **不在沙箱跑 git 写**：需要提交时**只生成 git 命令交 Doctor 终端跑**。
- **suggested_actions 仅供参考**：Codex 的建议动作是线索，最终由你按铁律裁决是否执行、怎么执行。

### Step 4 · 写 ack 回执（含滚动）

每个任务消费完（成功/失败/跳过）都写 ack：

```bash
python3 <skill>/scripts/consume.py write-ack \
  --task-id <tid> --status <ok|failed|skipped> --run-id <消费的run_id> \
  --outputs '["落盘产物路径1","路径2"]' \
  --leftovers '["待人工项1"]' \
  --notes "一句话说明" [--dry-run]
```

脚本自动滚动 `ack.latest → ack.prev`（copy-then-overwrite，只写不删），再写新 `ack.latest`。`--run-id` 写进 `last_consumed_run_id`，作下次幂等锚。**样本消费加 `--dry-run`。**

### Step 5 · 报告 Doctor

汇总：本轮 ready N 个、消费成功 X、失败 Y（附原因）、跳过 Z；各任务落盘产物路径；需 Doctor 跑的 git 命令；遗留/待人工项。用 `present_files` 给 Doctor 看新增/改动的落盘文件。

## 路由表

### `touzhijunjun-perspective-refresh`（投知君君视角刷新）

Codex 侧已完成 Stage 1-3（增量检测 + 三分桶提炼 + 图谱候选核实），payload 结构见 `to VV/scheduled/CC致VV-投知君君握手改造需求.md`。**Claude 侧只做原 SKILL 的 Stage 4-5**：

payload 预期字段（由对接需求约束）：
- `payload.perspective_items[]`：产业逻辑条目（论断/原文引述/来源视频/类型/时效性）
- `payload.contrarian_items[]`：反共识纠偏三元组（共识→真相→产业依据+引述+性质+图谱价值）
- `payload.graph_candidates[]`：核实通过的图谱候选（web 核实结论/Tier/建议节点边/渊图现状）
- `payload.new_processed[]`：本期并入 `_last_processed.json` 的视频文件名

落盘动作（走 `~/Documents/Database/行业研究/`）：
1. `contrarian_items` → 追加 `wiki/视角/投知君君/_反共识纠偏录.md` 对应分区，更新文末计数 + `反共识纠偏录.card.md`
2. `perspective_items` → 追加 `wiki/视角/投知君君/_产业逻辑raw.md` 对应主题分区，必要时更新主题 `.card.md`
3. 更新 `wiki/视角/INDEX.md` 计数
4. `graph_candidates` → 追加 `docs/PROPOSAL-投知君君图谱候选.md`（**只提候选，不建 patch、不 promote**）
5. `new_processed` → 并入 `wiki/视角/投知君君/_last_processed.json` 的 processed 列表，更新 processed_count + updated
6. 所有新增标来源视频与日期
7. **git 命令交 Doctor**（不在沙箱跑）：
   ```
   cd ~/Documents/Database/行业研究 && git add "wiki/视角/投知君君/" "wiki/视角/INDEX.md" "docs/PROPOSAL-投知君君图谱候选.md" && git commit -m "投知君君周更(握手消费):本期+N纠偏+M候选" && git push
   ```
8. 若有图谱候选，提示 Doctor：「本期 M 条图谱候选，需 promote 请说一声，我走 核实→patch→dry-run→读盘核验。」

### 新任务接入

新 task_id 接入时：① 先在 `to VV/scheduled/` 写该任务的《对接需求》约定 payload 结构；② 在本路由表加一节落盘映射；③ 更新 `scheduled/README.md` 的「当前接入任务」表。

## 铁律

① 校验不过（schema/checksum/版本）→ 拒绝消费、ack failed，绝不带病落盘。
② `sample: true` → 一律 dry-run，绝不写 canonical。
③ promote 进 canonical 须 Doctor 显式；本 skill 只追加视角层/提候选。
④ 不在沙箱跑 git 写/下载/ASR；git 只给命令。
⑤ 引述/数据逐字真实，payload 没有的绝不补编；缺口留空标待核验。
⑥ ack 与 payload 均不得含明文 token/凭据。
