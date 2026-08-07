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
> **2026-06-23 梳理**：权威库当时 5 条非 ✅，已逐一处理——2 条治本、1 条待 Mac 收尾、2 条正式接受。
> **2026-06-26 对齐**：BUG-20260505-003 权威库已闭环（✅）；当前权威库实况＝0 条 🔄 actionable + 2 条 ⚠️ 已接受/won't-fix。看板 manifest gotchas 口径定为「actionable-only」→ DVA 计数 2→0（⚠️ 已接受项不计积压）。
> **2026-08-06 对齐**（DVA-Database 例行自查，修正上文旧口径）：权威库实况＝**1 条 🔄 actionable**（`BUG-20260711-002` update-all `--limit 0` 吞零，仍活在 fuxi 部署代码中）+ **2 条 ⏹**（`INFRA-20260702-001` Codex 看门狗——fuxi 化架空 superseded；`INFRA-20260727-002` 恢复控制器——Doctor 裁「按设计退役」：自动恢复已由 heartbeat 告警+人工授权补跑取代）+ ⚠️ 已接受/won't-fix 若干（其中 `RISK-20260724-001` Mac 侧 cookie 四文件收敛仍待 Doctor 授权）。
> **双库漂移修复（2026-08-06 已落笔）**：Codex 镜像 `Codex/Project Mirror/DVA/GOTCHAS.md` 11 条经内容级复核——**10 条真正缺失**、1 条（`ERR-20260723-002`）与既有 `GIT-20260723-001` 同题双收（初判 7 条系弱关键词误中、中文标题曾漏过查重），且镜像沿用 06-13 已废止的 ERR- 编号。已按 Doctor 裁定以**精华版**（重编号 INFRA-、逐条溯源原号）并入权威库第七节，同题双收合并为 `INFRA-20260723-005`（留双溯源）；权威库非规范编号随之归零（`ERR-20260711-001`→`INFRA-20260711-001` 留曾用编号），终态 79 条。镜像只读不动（VV 有 DVA 定时检查在跑）。此后纪律＝权威库单写，镜像只读回流，VV 新条目报 Doctor 后落权威库。

本轮（2026-06-23）处理结果：
- ✅ `[BUG-20260618-002]` `--limit 0` 被 `|| 5` 吞 → 治本（`dva.js` 改 `Number.isFinite`）。
- ✅ `[BUG-20260618-001]` 并发撞 `dy_downloader.db` 锁 → 治本（DYD `database.py` 加 WAL+busy_timeout，**fork 第三方·升级须 rebase**）。
- ✅ `[BUG-20260505-003]` `dyd/~` 残留目录 → 权威库 2026-06-23 已标 ✅（根因已修、清理命令已交付）；本索引 06-26 对齐回填。
- ⚠️ `[RISK-20260617-001]` 沙箱 DB root guard 写死绝对路径 → **已接受约束**（防孤儿空表的有意兜底，采集只在 Mac 跑）。
- ⚠️ `[INFRA-20260618-003]` 图文 `.webp` 永久 403 → **won't-fix**（外部 CDN 渲染失效，只要视频 mp4，接受丢弃）。

长期容忍（根因未除·非本轮 5 条，但仍在）：
- 🔁 `DYD 文件名截断丢 aweme_id` —— 根因在第三方下载器（80 字截断）未除，反复在 INFRA-20260521-001/003、20260603-001、20260610-002 下游打补丁兜底（前缀匹配 / 扫父目录名）。现容忍，治本成本高。
- 🔁 `单链接 harvest-links.js 不 seed DB` —— 设计缺口，产物成 import 孤儿（INFRA-20260603-003）。建议优先在 harvest 末尾补 seed 收口。
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

### [INFRA-20260603-003 追加·2026-07-24] import 孤儿告警在 secUidFilter 过滤之前触发＝假红根因
**关联：** INFRA-20260603-003（扫整根·本条为其治本①的机理补充）
**机理：** `handleImportTranscriptsCommand` 的 `walk(rootDir)` 扫**整个** `TRANS_DIR`；解析不到 sec_uid 的字幕在 `dva.js:1608` 打 `[无法定位作者]` 告警，而**这一步早于 `secUidFilter` 过滤（1612 行）**。故定时班即便只补一个作者、传了 secUid，全树 ~630 条跨作者孤儿仍逐条假红——三桶分级只是把它单列止血，非治本。
**治本①（1a·作者域扫描）：** harvest 第 3 步 import 扫描根改 `path.join(TRANS_DIR, authorName)`（不存在兜底退整根）→ 跨作者孤儿永不被访问。standalone `dva import-transcripts <dir> [sec_uid]` CLI 不改，整根手动导入仍照常告警（回归基线）。
**排查提示：** 复查「假红/告警洪泛」先看**告警点与过滤点的行序**——过滤在告警之后＝全量误报。改 import 相关逻辑时以此为第一手线索。
**状态：** ① 已改 Mac 源（未部署·待 bundle/VV 验）；② 孤儿集中裁决留①稳定后另起。
