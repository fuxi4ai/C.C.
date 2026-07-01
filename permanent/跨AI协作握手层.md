---
title: 跨AI协作握手层
tags: [permanent, 架构模式, 跨AI协作, 基建]
created: 2026-07-01
updated: 2026-07-01
status: active
type: permanent
---

# 跨 AI 协作握手层（Handshake Layer）

> 让不同 AI 承担不同职能而彼此不共享 runtime、不共享上下文时，靠**结构化文件契约**接力。适用 CC × Codex、CC × 数灵、CC × 未来第三家模型等一切"两个及以上 AI 分工"场景。

## 核心原则：能力分层 + 规矩不外泄

跨 AI 分工时不要"让一家扛全套"，而是**把每家最强的那一段挑出来接一段**：

- **重活给完成度最高的模型**（读多源材料、做 web 核实、结构化产出）——本条视具体任务定，谁在该任务上 tool-use 稳态最好、alignment 最合规、上下文长度最够，就派谁。
- **细活留在磨合过的模型**（落盘规矩、propose-then-confirm、数据真实性铁律、语域规范、级联检查、promote 铁律 G-X4/G-X18）——这些"约束执行力"和"约定俗成"极依赖模型跟主场生态的磨合深度，不要迁移到新模型上重训。

**推论**：**重活产出结构化数据，规矩执行方消费数据**。产出方不写 canonical、不改本项目状态、不做 promote 判断；执行方拿到数据后按主场规矩落盘。这样约束/铁律永远只在**主场一份**，不用同步到外援。

## 握手协议规格

### 目录约定

```
~/Documents/4AI/Shake hands/
├── to CC/                  ← 外援→主场方向（Codex→Claude 等）
│   ├── {task_id}.latest.json    ← 最新版，主场消费源
│   └── {task_id}.prev.json      ← 最近一份副本，只留一个（备查用，Doctor 2026-07-01 追加约定）
├── from CC/                ← 主场→外援回执方向
│   └── {task_id}.ack.json       ← 最近消费的 run_id + 状态，外援下次跑前可读
└── spec/                   ← 协议本身
    ├── handshake-schema.json    ← 唯一 schema（版本化）
    └── README.md                 ← 目录约定 + 生命周期
```

**滚动规则**：外援每次覆盖 `latest.json` **之前**，先把当前 `latest.json` 挪到 `prev.json`（原子 rename）。永远只留 latest + 一份 prev，不无限堆积。

### JSON 负载（最小契约）

```json
{
  "schema_version": 1,
  "task_id": "…",                    // 任务命名空间，路由用
  "run_id": "ISO8601-…-shortHash",   // 幂等 key，主场按 run_id 判是否已消费
  "asof": "ISO8601+TZ",              // 数据快照时刻
  "producer": "codex|数灵|…",
  "producer_version": "…",
  "status": "ok|partial|error|noop", // noop 也要写，避免"没跑"与"没料"混淆
  "payload_kind": "…",               // 语义标签（如 delta_extraction、weekly_report）
  "payload": { … },                  // 结构化数据 + 建议动作，绝不含"已落盘"假设
  "notes": "自述/警告/待人工核对项",
  "checksum": "sha256(payload)"
}
```

### 幂等与生命周期

- `run_id` 是主场判"消费与否"的唯一依据；主场消费成功后写 `from CC/{task_id}.ack.json` 记录 `last_run_id`。
- 外援下次跑前可选读 ack 决定是否 skip；但因 payload 是 delta 语义 + `processed_added` 去重，即便重复覆盖也不产生副作用。
- 主场消费失败时写 `error.json` 报错，不改 canonical。
- schema 有版本号，兼容升级走 `schema_version + 1` + 主场消费者兼容旧版一段时间。

## 触发方式（谁醒来读握手）

三档，从轻到重：

1. **主场保留一个"薄定时任务"每天低峰醒一次跑 handshake-consumer**——最省心、成本最低（消费任务本身极轻，不 web、不子 agent）、Doctor 无需记流程。**默认档**。
2. **Doctor 手动触发**——外援跑完发通知，Doctor 打开 Claude 说一句"消费握手"走 skill。备档。
3. **launchd/fswatch 监听目录**——文件写入即触发主场。工程化最重，仅在高频/低延迟场景采用。

## 为什么优于"一家扛全套"

反面对照——若让单一模型全跑（哪怕能全局切通道）：

- **Tool-use / subagent 编排稳态**是模型 × 平台高度耦合的能力，换模型走"兼容协议"能跑但复杂嵌套（e.g. 派并行 subagent、AskUserQuestion 结构化参数）容易掉链子。
- **"宁缺勿滥"的 alignment 强度**差异很大——数据真实性铁律的执行深度极依赖模型训练里"抗诱惑不编数据"的对齐深度，弱模型容易"顺手补一个像模像样的数字"。
- **规矩迁移代价**——把主场几年沉淀的 skill 生态（brain-anchors / GOTCHAS / 语域规范 / propose-then-confirm）迁到新模型等于让新员工背 200 页 SOP，走一段才能顺手。这套磨合成本 Doctor 会长期承担。

而握手层让新模型**只吐 JSON**，不用懂任何主场规矩——规矩执行仍在主场，约束不外泄。

## 平台能力边界的前置核查（配套教训 G-X47）

设计跨 AI 分工前**必须先核**：

1. 目标平台是否支持 **per-task 粒度的模型选择/通道路由**？（决定"仅切定时任务通道"是否可行）
2. 是否支持 **per-task 权限/工具集隔离**？（决定敏感任务能否走弱模型）
3. 是否有 **文件系统触发/调度**？（决定握手能不能自动化）

搞不清就动手 = 会走到一半发现某档不通、方案报废。判据参 [[通用教训]] G-X41（负向能力声明是待验证假设）+ G-X47（能力边界前置核查）。

## 实例映射

| 场景 | 主场 | 外援 | 握手内容 |
|------|------|------|---------|
| 定时任务成本&完成度双优化（2026-07-01 立此模式） | Claude Desktop（brain 主场） | Codex（GPT-5.5，包月） | 提炼产出（视角刷新 / 周报 / 复盘）的 delta JSON + 建议动作 |
| 数灵转移（云端 agent→本地 subagent） | CLI CC | 云端 agent | 同构：agent 产结构化归档、CC 落归位（参 [[数灵转移]]） |
| 未来第三家模型接入 | 视场景 | 视场景 | 同一 schema 版本化扩展即可 |

## 边界与代价

- **多一层同步复杂度**：跨系统握手多一个失败点——但走本地目录 `~/Documents/4AI/` 不走云同步就基本可控。
- **外援版本漂移**：外援 CLI/模型升级可能改输出格式——`schema_version` + 主场 schema 校验兜住。
- **首次搭建工程量**：一次性成本，之后每加一个新任务只是加一份外援 prompt + 一份主场路由分支。

## 相关

- [[数灵转移]]（云端 agent → 本地 subagent，同类跨 AI 分工问题）
- [[通用教训]] G-X47（跨 AI 分工决策前核平台能力边界）
- [[通用教训]] G-X4（PRD 交付标准纪律 / CC 永不打✓）——握手层里"外援不 promote、不改 canonical"是它的跨模型延伸
- [[通用教训]] G-X18（先核实再 promote + 克制挂接）——握手层把"promote"这道闸永远留在主场
- [[Doctor协作偏好]] propose-then-confirm

## 源

- logs/2026-07-01-定时任务架构-方案B定案
- 触发讨论：APIYI 按需计费的定时任务成本问题（Deepseek 白菜价可全局切；Codex 包月边际免费）→ 抛开价格纯以完成度/可信度评估→ 定方案 B（Codex 主跑 + Claude 消费握手）
- Doctor 追加的"latest + 一份 prev 副本"滚动规则，本笔记落款
