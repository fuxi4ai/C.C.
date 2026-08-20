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
**状态：** ✅ 已修复（**仅由 Doctor 或指定独立验收方落，实施者不得自标**）/ 🔄 待修复·已修待验 / ⚠️ 已知风险（暂不修复）
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
> **双库漂移修复（2026-08-06 已落笔）**：Codex 镜像 `Codex/Project Mirror/DVA/GOTCHAS.md` 11 条经内容级复核——**10 条真正缺失**、1 条（`ERR-20260723-002`）与既有 `GIT-20260723-001` 同题双收（初判 7 条系弱关键词误中、中文标题曾漏过查重），且镜像沿用 06-13 已废止的 ERR- 编号。已按 Doctor 裁定以**精华版**（重编号 INFRA-、逐条溯源原号）并入权威库第七节，同题双收合并为 `INFRA-20260723-005`（留双溯源）；权威库非规范编号随之归零（`ERR-20260711-001`→`INFRA-20260711-001` 留曾用编号），终态 81 条（08-07 追加 `INFRA-20260807-001` index 平台分层重建 · `-002` 长任务认证与告警四分面）。镜像只读不动（VV 有 DVA 定时检查在跑）。此后纪律＝权威库单写，镜像只读回流，VV 新条目报 Doctor 后落权威库。

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

### [BUG-20260819-001] Qwen3-ASR 长音频整段转写 CUDA OOM（生产班受波及）
**状态：** 🔄 已修待验（2026-08-20 adapter 分段修复落地 Mac 源 · 单测 9/9 绿 · **bundle→fuxi 已部署**〔`dva-runtime-20260820T150155Z` · sha256 `ae008d4e…` · 旧 runtime→`runtime.bak.20260820-230624` 可回滚〕· **Doctor 快验通过**〔single-20260820-152826Z · 32.5min 视频端到端 exit=0 无 OOM · 10314 字 · 产物 asr_status=success / source=qwen3-asr-1.7b-local-fuxi〕· 待 VV 独立补验后关条〔移交件 `docs/移交VV_ASR长音频分段修复_20260820.md`〕· **VV 补验顺延（2026-08-20 额度用尽）**· 周六 08-22 05:00 定时班为自然第二验证点）
**优先级：** 🟡 中
**触发：** 2026-08-19 调研情报局单视频任务：32.5min 视频 `single_one.ps1` 转写稳定复现 OOM——torch 报进程内已分配 34.58 GiB（4090 仅 24 GiB）、请求 3.62 GiB 失败。同日 `refill-20260818-210000Z.log`（周三 05:00 班）含多行同款 OOM，班次转写成批失败。
**根因：** `transcribe.py` 把整段长音频一次传入 `model.transcribe()`，无分段/流式；模型加载（~3.4GB bf16）与 20s 短音频均正常（probe 实证 exit 0），长音频处理阶段内存膨胀至 OOM。
**影响面：** 长视频（估 >15-20min）转写必失败；短视频不受影响。SpaceBlockout server（pythonw 8568）无关联（probe 8GiB 分配正常）。
**绕过（已验证）：** 450s×5 分段转写（`E:\AI\DVA\ops\tmp\gtj_chunk_asr2.ps1` 范式——ffmpeg segment + 逐段 CLI + 拼接，5/5 成功，产物落 Transcripts/ 规范路径）。
**建议修法：** ~~transcribe.py 内建分段（whisper 式滑窗或 N 分钟分段+拼接）；或 DVA 管线层对超长音频预分段。修复与部署由 Doctor/VV 裁。~~ → **已按「DVA adapter 分段」修**（Doctor 2026-08-20 裁）：`dyd/asr_local_qwen3.py` 内建 ffprobe 探测 >900s → ffmpeg 切 450s 段 → 逐段 CLI → 拼接（backend=`local-cuda-chunked-450s`）；单测 `dyd/tests/test_asr_local_qwen3.py` 9/9。**待**：bundle→fuxi 部署 + VV 端到端验长视频。CLI 内建分段（模型单次加载更省）作优化建议知会 VV，改不改由 VV 定。
**预防门禁：** 新音频长度 >15min 先测整段再上；班日志出现 OutOfMemory 即查本条族。
**来源：** 2026-08-19 调研情报局单视频任务（硬证据：两次整段复现 + 20s 对照 + 班日志 OOM 行）

### [NOTE-20260820-001] single_one.ps1 BOM 丢失复发——修复被覆盖＝发布链有洞
**状态**: ⚠️ 已知风险
**优先级**: 🟡 中
**触发**: 2026-08-20 调研情报局单视频任务：single_one.ps1 解析错误（PS5.1 按 GBK 读无 BOM 的 UTF-8 → 字符串缺终止符等 parser 错）。字节证据：首三字节 `23 20 73`（"# s"）无 BOM；对照 harvest_one.ps1 首三字节 `EF BB BF` 正常。08-14 VV 已修过 BOM 并首跑验证成功——本次发现修复被后续 scp 覆盖。
**根因**: fuxi 脚本发布链无 BOM 校验门禁——修复靠人记，覆盖后无哨兵。
**处置**: 现场补 BOM（ReadAllText UTF-8 → WriteAllText UTF8Encoding($true)），验证 EF BB BF 后脚本正常。
**预防门禁**: fuxi 侧 ps1 脚本 scp 落地后校验首三字节；或脚本写入管线统一 BOM 化。与 BUG-20260819-001 同场发现（同视频任务）。
**来源**: 2026-08-20 调研情报局单视频任务（字节证据 23 20 73 → EF BB BF）

### [NOTE-20260820-002] runtime 整体换入丢 `dyd\config.yml`——harvest-links 硬编码路径（发布链洞②）
**状态**: ⚠️ 已知风险
**优先级**: 🟡 中
**触发**: 2026-08-20 分段修复部署（bundle `dva-runtime-20260820T150155Z`）：install 整体换 runtime 后 single_one 报「❌ 找不到 DYD 配置：E:\AI\DVA\runtime\dyd\config.yml」（exit=1）。
**根因**: `harvest-links.js` L221 硬编码 `path.join(__dirname,'dyd','config.yml')`，不读 `DVA_DYD_CONFIG` env（dva.js 读、harvest-links 不读）；bundle 因含秘密刻意排除 config.yml；install 脚本换入后无补件步骤。
**处置**: 现场从 `config\config.fuxi.yml` 拷贝恢复（旧 runtime.bak 内并无该文件——此前同法放置）。**根治待裁**：a) harvest-links 认 env；b) install 换入后自动补拷；c) 两者都做。
**预防门禁**: 每次换 runtime 后先跑 single_one/harvest_one 冒烟再离手。
**来源**: 2026-08-20 部署现场（single-20260820-151105Z exit=1 → 拷贝后复跑通过）

### [NOTE-20260820-003] fuxi runtime 补丁不在 Mac 源——换 runtime 即丢（发布链洞③ · 同族升格）
**状态**: ⚠️ 已知风险
**优先级**: 🟡 中
**触发**: 同场部署连续两坑：① 旧 runtime 的 harvest-links.js 用 `PYTHON_BIN` 变量、新 bundle（Mac 源）硬编码 `python3` → fuxi 无 python3 命令（spawnSync 失败 stderr 空、报「(无输出)」），现场建 venv python3.exe shim + PATH 前置绕过；② 旧 runtime 的 DASHSCOPE_KEY/TOS_AK/TOS_SK 前置检查被 fuxi 侧绕过、Mac 源无条件检查 → local 后端本不需云凭证却被拦，现场塞 dummy 值绕过。
**根因**: fuxi 生产 runtime 长期积累的运维态补丁从未回流 Mac 源——「修复靠人记、覆盖后无哨兵」的 NOTE-20260820-001 同族**第三次复发**（BOM / config.yml / runtime 补丁）。**应升格通用教训**：异地部署点补丁必须回流源仓，或发布链加换入后 diff 哨兵。
**处置**: shim + dummy env 属临时措施，**下次换 runtime 会再丢**；根治三选项待 Doctor/VV 裁（回流 Mac 源 / install 脚本内置 / 发布后 diff 哨兵），已写入移交 VV 件。
**预防门禁**: bundle 构建前 diff fuxi runtime 与 Mac 源关键文件；或部署后跑 single_one 冒烟清单。
**来源**: 2026-08-20 部署现场（152429Z python3 ENOENT → shim；152204Z DASHSCOPE 拦截 → dummy）
