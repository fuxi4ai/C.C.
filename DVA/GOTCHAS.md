---
title: DVA · GOTCHAS（已知坑 · 索引）
tags: [DVA, gotchas, index]
created: 2026-05-14
updated: 2026-06-14
status: active
type: resource
project: DVA
---

# DVA · GOTCHAS（已知坑 · 索引）

> **本文件是索引/沉淀，不是日志。** 实时踩坑日志在
> `~/Documents/Claude/Projects/DVA/GOTCHAS.md`（权威源，30+ 条，CC 解决问题后**立即**回写那里）。
> 本文件只做：① 统一术语约定；② 指向权威日志；③ 沉淀少数跨项目通用教训。

## 统一术语约定（与 Projects/DVA/GOTCHAS.md 完全一致）

**编号：** `[BUG-YYYYMMDD-NNN]`（代码逻辑）/ `[INFRA-YYYYMMDD-NNN]`（环境·链路·依赖）/ `[RISK-YYYYMMDD-NNN]`（已知风险）
**状态：** ✅ 已修复 / 🔄 待修复 / ⚠️ 已知风险（暂不修复）
**优先级：** 🔴 高（阻断核心功能）/ 🟡 中（影响常用功能）/ 🟢 低（边缘情况）

> 旧 `ERR-` 前缀、`⏳ 待解决` 状态词已于 2026-06-13 审核统一并入上表，不再使用。

## 权威日志入口

- 实时全量坑库：`Projects/DVA/GOTCHAS.md` —— 一切 BUG/INFRA/RISK 条目以此为准。
- 回写时机：CC 排查超过一轮并解决后，立即在权威日志追加条目，无需 Doctor 提示。
- 本索引只在出现「值得跨项目复用的通用教训」时，才把要点沉淀到下方。

## 当前未闭环（来自权威日志，便于快速扫描）

> 详情见 `Projects/DVA/GOTCHAS.md` 对应条目；此处仅留指针，避免双写漂移。

- 🔄 `[BUG-20260505-003]` `dyd/~` 字面量残留目录待手动清理（Node 侧根因已修，残留目录需 Mac 端 `rm -rf`）。
- 详尽列表请直接看权威日志的 🔄 / ⚠️ 标记。

## 沉淀的通用教训

### [INFRA-20260605-001] 兼容 Anthropic 协议的推理模型：content[0] 多为 thinking 块，勿当文本
> （原编号 ERR-20260605-001，2026-06-13 统一为 INFRA- 前缀）

**状态：** ✅ 已修复
**优先级：** 🔴 高
**触发场景：** 切换分析 LLM 为 DeepSeek V4 Pro 后，`基础模块/llm-client.js` 自检报「连接失败，详情 undefined」。
**根因：** `chat()` 写死取 `response.content[0]?.text`。推理模型在 Anthropic 兼容格式下 content[0] 是 `thinking` 块（无 `.text`），真正答案在后续 `text` 块 → 取到空串。影响所有分析调用，非仅自检。
**修复：** `chat()` 改为 `content.filter(b=>b.type==='text')` 拼接所有 text 块，兜底回退 `content[0].text`；healthCheck「已连通但回复未含 OK」路径把实际文本带出，不再丢 undefined。（`llm-client.js:118-122`，已核实在库。）
**通用预防：** 接入任何兼容 Anthropic 协议的模型时，不要假设 `content[0]` 即文本；按 `type` 取块。此教训对所有调用 LLM 的项目通用。

## DVA 运维 / Codex 对接（2026-06-14）

### [P0-20260614] `update-all` 失败路径写死源 GOTCHAS.md → 破"源只读"边界
**状态：** ✅ 已修复（CC，2026-06-14）
**根因：** `dva.js:80` `gotchasPath = path.join(__dirname,'GOTCHAS.md')` 写死；顶层 `mainWithErrorHandling` 出错即追加写**源** GOTCHAS.md。成功路径干净（只写 `/tmp` 与 `Database/`），仅失败路径破边界；每个子进程（harvest/analyze-level1）各带这套兜底。
**修复：** 改 `process.env.DVA_ERROR_LOG_PATH || path.join(__dirname,'GOTCHAS.md')`。默认行为不变；自动任务设 env 改向 `Database/Douyin/DVA-ops/failures/dva-errors.md`（目标文件须含 `## 🐛 当前易错点` 标记，否则不写入）。已验证设 env 后源 GOTCHAS.md 字节前后一致。

### [OPS-20260614] ASR finalize 卡点：先查落地路径，别先怪网络
**现象：** 一条 ASR `--poll-once` 卡住，state 的 `_note` 写着"OSS 北京区白名单 blocker"。
**真相：** 白名单 blocker 已不存在（transcript 正常下载）；实际卡点是 state 的 `out_txt` 硬编码到 stale `/tmp/dva_asr_out_5`（属主 nobody 不可写）。改向规范 `Transcripts/` 目录即一次 finalize 跑通。
**教训：** transcript 写失败先查**输出路径**权限/存在性（尤其硬编码 `/tmp` 旧目录），再怀疑网络/白名单。另：挂载盘默认禁删，清理需 `allow_cowork_file_delete`。
