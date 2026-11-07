---
title: DVA · GOTCHAS（已知坑 · 索引）
tags: [DVA, gotchas, index]
created: 2026-05-14
updated: 2026-11-05
status: active
type: resource
project: DVA
---

# DVA · GOTCHAS（已知坑 · 索引）

> **本文件是索引/沉淀，不是日志。** 实时踩坑日志在
> **`Codex/Project Mirror/DVA/GOTCHAS.md`（权威真源 · Codex 日常在写）**。
> 本文件只做：① 统一术语约定；② 指向权威日志；③ 沉淀少数跨项目通用教训。

> ⚠ **权威改判（2026-09-17 Doctor /todo 裁「权威改 Codex 镜像仓」）**——**本条已于 2026-09-26 /todo 现核时补落**：
> 原文写「权威源 = `~/Documents/Claude/Projects/DVA/GOTCHAS.md`」，与 09-17 裁定**相反**，且 `Projects/DVA/GOTCHAS.md`
> 头部同期已加权威反转注记（自即日起为**历史副本**、只读参照）。两处声明不一致曾挂为 TODO 条目（2026-09-17 挂 · 5 天）；
> 本场现核实读：`Projects/DVA/GOTCHAS.md` 头部**有**注记、`brain/DVA/GOTCHAS.md`（本文件）**无**——即 09-17 的
> 「brain/DVA/GOTCHAS.md 纪律反转注记」当年**未实际落盘**。现按裁定补正：权威真源 = **`Codex/Project Mirror/DVA/GOTCHAS.md`**；
> Mac 侧新条目报 Doctor 后落镜像仓；回流方向反转（Codex→Mac 汇报制）。
> 三源现状（2026-09-26 实读）：`Codex/Project Mirror/DVA/GOTCHAS.md` **239,139B · 09-25 20:47**（活）／
> `Claude/Projects/DVA/GOTCHAS.md` 156,464B · 09-26 01:07（历史副本，当日仍有写入）／
> 本文件 14,929B · 09-18（索引）。

## 统一术语约定（与 Codex/Project Mirror/DVA/GOTCHAS.md 完全一致）

**编号：** `[BUG-YYYYMMDD-NNN]`（代码逻辑）/ `[INFRA-YYYYMMDD-NNN]`（环境·链路·依赖）/ `[RISK-YYYYMMDD-NNN]`（已知风险）
**状态：** ✅ 已修复（**仅由 Doctor 或指定独立验收方落，实施者不得自标**）/ 🔄 待修复·已修待验 / ⚠️ 已知风险（暂不修复）
**优先级：** 🔴 高（阻断核心功能）/ 🟡 中（影响常用功能）/ 🟢 低（边缘情况）

> 旧 `ERR-` 前缀、`⏳ 待解决` 状态词已于 2026-06-13 审核统一并入上表，不再使用。

## 权威日志入口

- 实时全量坑库：**`Codex/Project Mirror/DVA/GOTCHAS.md`** —— 一切 BUG/INFRA/RISK 条目以此为准。
  **（2026-09-30 /todo 现核改）** 原写 `Projects/DVA/GOTCHAS.md`，**与本文件头部 L17「权威改判（2026-09-17 Doctor /todo 裁『权威改 Codex 镜像仓』）」相抵**；`Claude/Projects/DVA/GOTCHAS.md` 自 09-17 起为**历史副本、只读参照**（其头部已标）。本条为事务性对齐，不新增裁定。
- 回写时机：CC 排查超过一轮并解决后，立即在权威日志追加条目，无需 Doctor 提示。
- 本索引只在出现「值得跨项目复用的通用教训」时，才把要点沉淀到下方。

## 当前未闭环（来自权威日志，便于快速扫描）

> 详情见 `Projects/DVA/GOTCHAS.md` 对应条目；此处仅留指针，避免双写漂移。
> **2026-06-23 梳理**：权威库当时 5 条非 ✅，已逐一处理——2 条治本、1 条待 Mac 收尾、2 条正式接受。
> **2026-06-26 对齐**：BUG-20260505-003 权威库已闭环（✅）；当前权威库实况＝0 条 🔄 actionable + 2 条 ⚠️ 已接受/won't-fix。看板 manifest gotchas 口径定为「actionable-only」→ DVA 计数 2→0（⚠️ 已接受项不计积压）。
> **2026-08-06 对齐**（DVA-Database 例行自查，修正上文旧口径）：权威库实况＝**1 条 🔄 actionable**（`BUG-20260711-002` update-all `--limit 0` 吞零，仍活在 fuxi 部署代码中）+ **2 条 ⏹**（`INFRA-20260702-001` Codex 看门狗——fuxi 化架空 superseded；`INFRA-20260727-002` 恢复控制器——Doctor 裁「按设计退役」：自动恢复已由 heartbeat 告警+人工授权补跑取代）+ ⚠️ 已接受/won't-fix 若干（其中 `RISK-20260724-001` Mac 侧 cookie 四文件收敛仍待 Doctor 授权）。
> **双库漂移修复（2026-08-06 已落笔）**：Codex 镜像 `Codex/Project Mirror/DVA/GOTCHAS.md` 11 条经内容级复核——**10 条真正缺失**、1 条（`ERR-20260723-002`）与既有 `GIT-20260723-001` 同题双收（初判 7 条系弱关键词误中、中文标题曾漏过查重），且镜像沿用 06-13 已废止的 ERR- 编号。已按 Doctor 裁定以**精华版**（重编号 INFRA-、逐条溯源原号）并入权威库第七节，同题双收合并为 `INFRA-20260723-005`（留双溯源）；权威库非规范编号随之归零（`ERR-20260711-001`→`INFRA-20260711-001` 留曾用编号），终态 81 条（08-07 追加 `INFRA-20260807-001` index 平台分层重建 · `-002` 长任务认证与告警四分面）。镜像只读不动（VV 有 DVA 定时检查在跑）。此后纪律＝权威库单写，镜像只读回流，VV 新条目报 Doctor 后落权威库。
> **2026-09-17 权威改判（Doctor /todo 裁「权威改 Codex 镜像仓」）**：上句纪律自即日起反转——权威真源 = `Codex/Project Mirror/DVA/GOTCHAS.md`（Codex 日常在写·65 条含当日 ERR-20260917-004/005/006）；Mac 库 `Projects/DVA/GOTCHAS.md` 为历史副本（已加指针注记）；Mac 侧新条目报 Doctor 后落镜像仓，回流方向反转（Codex→Mac 汇报制）。

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
**状态：** ✅ 已修复（✅ 2026-10-23 错题本消化 · 未参与实施的审核 subagent 落签 · 证据：现行 `dyd/dva_asr.py` 输出路径由 `_compute_out_paths(output_dir…)` 推导（L439-446）、默认规范 Transcripts 目录（L99-100），全树 grep `dva_asr_out`/`/tmp/dva_asr` 0 命中〔源码+现存字幕目录〕）
**现象：** 一条 ASR `--poll-once` 卡住，state 的 `_note` 写着"OSS 北京区白名单 blocker"。
**真相：** 白名单 blocker 已不存在（transcript 正常下载）；实际卡点是 state 的 `out_txt` 硬编码到 stale `/tmp/dva_asr_out_5`（属主 nobody 不可写）。改向规范 `Transcripts/` 目录即一次 finalize 跑通。
**教训：** transcript 写失败先查**输出路径**权限/存在性（尤其硬编码 `/tmp` 旧目录），再怀疑网络/白名单。另：挂载盘默认禁删，清理需 `allow_cowork_file_delete`。

### [INFRA-20260603-003 追加·2026-07-24] import 孤儿告警在 secUidFilter 过滤之前触发＝假红根因
**关联：** INFRA-20260603-003（扫整根·本条为其治本①的机理补充）
**机理：** `handleImportTranscriptsCommand` 的 `walk(rootDir)` 扫**整个** `TRANS_DIR`；解析不到 sec_uid 的字幕在 `dva.js:1608` 打 `[无法定位作者]` 告警，而**这一步早于 `secUidFilter` 过滤（1612 行）**。故定时班即便只补一个作者、传了 secUid，全树 ~630 条跨作者孤儿仍逐条假红——三桶分级只是把它单列止血，非治本。
**治本①（1a·作者域扫描）：** harvest 第 3 步 import 扫描根改 `path.join(TRANS_DIR, authorName)`（不存在兜底退整根）→ 跨作者孤儿永不被访问。standalone `dva import-transcripts <dir> [sec_uid]` CLI 不改，整根手动导入仍照常告警（回归基线）。
**排查提示：** 复查「假红/告警洪泛」先看**告警点与过滤点的行序**——过滤在告警之后＝全量误报。改 import 相关逻辑时以此为第一手线索。
**状态：** ✅ 已闭（2026-11-05 · 未参与实施的审核者独立核验 PASS_WITH_LIMITS）← 原：① 已改 Mac 源（未部署·待 bundle/VV 验）；② 孤儿集中裁决留①稳定后另起。
**✅ 落签（2026-11-05 · 未参与实施的审核者 · 独立核验后自主落签）**: PASS_WITH_LIMITS——① Mac 源 `dva.js` L1517-1525：harvest 第 3 步 `importRoot = path.join(TRANS_DIR, authorName)`，目录不存在兜底整根，standalone `import-transcripts` CLI 未改；`node --check dva.js` rc=0；② 20260820T150155Z 与 20260909T123945Z 两 bundle 内 `dva.js`（sha `7406d4b22648`）与 Mac 源逐字一致——原状态「未部署」已过时，08-20 / 09-09 两次 install 均已带上。限：该路径无自动化测；fuxi 生产班日志（`[无法定位作者]` 假红是否归零）盘上不可达未核。② 孤儿集中裁决不在本签范围，由 `logs/2026-08/checkpoints/2026-08-13_DVA孤儿②集中裁决移交.md`（已裁定 + 已移交 VV · 待 VV 执行回报）追踪。

### [BUG-20260819-001] Qwen3-ASR 长音频整段转写 CUDA OOM（生产班受波及）
**状态：** ✅ 已闭（2026-11-05 · 未参与实施的审核者独立核验 PASS_WITH_LIMITS）← 原：🔄 已修待验（2026-08-20 adapter 分段修复落地 Mac 源 · 单测 9/9 绿 · **bundle→fuxi 已部署**〔`dva-runtime-20260820T150155Z` · sha256 `ae008d4e…` · 旧 runtime→`runtime.bak.20260820-230624` 可回滚〕· **Doctor 快验通过**〔single-20260820-152826Z · 32.5min 视频端到端 exit=0 无 OOM · 10314 字 · 产物 asr_status=success / source=qwen3-asr-1.7b-local-fuxi〕· 待 VV 独立补验后关条〔移交件 `docs/移交VV_ASR长音频分段修复_20260820.md`〕· **VV 补验顺延（2026-08-20 额度用尽）**· 周六 08-22 05:00 定时班为自然第二验证点）
**优先级：** 🟡 中
**触发：** 2026-08-19 调研情报局单视频任务：32.5min 视频 `single_one.ps1` 转写稳定复现 OOM——torch 报进程内已分配 34.58 GiB（4090 仅 24 GiB）、请求 3.62 GiB 失败。同日 `refill-20260818-210000Z.log`（周三 05:00 班）含多行同款 OOM，班次转写成批失败。
**根因：** `transcribe.py` 把整段长音频一次传入 `model.transcribe()`，无分段/流式；模型加载（~3.4GB bf16）与 20s 短音频均正常（probe 实证 exit 0），长音频处理阶段内存膨胀至 OOM。
**影响面：** 长视频（估 >15-20min）转写必失败；短视频不受影响。SpaceBlockout server（pythonw 8568）无关联（probe 8GiB 分配正常）。
**绕过（已验证）：** 450s×5 分段转写（`E:\AI\DVA\ops\tmp\gtj_chunk_asr2.ps1` 范式——ffmpeg segment + 逐段 CLI + 拼接，5/5 成功，产物落 Transcripts/ 规范路径）。
**建议修法：** ~~transcribe.py 内建分段（whisper 式滑窗或 N 分钟分段+拼接）；或 DVA 管线层对超长音频预分段。修复与部署由 Doctor/VV 裁。~~ → **已按「DVA adapter 分段」修**（Doctor 2026-08-20 裁）：`dyd/asr_local_qwen3.py` 内建 ffprobe 探测 >900s → ffmpeg 切 450s 段 → 逐段 CLI → 拼接（backend=`local-cuda-chunked-450s`）；单测 `dyd/tests/test_asr_local_qwen3.py` 9/9。**待**：bundle→fuxi 部署 + VV 端到端验长视频。CLI 内建分段（模型单次加载更省）作优化建议知会 VV，改不改由 VV 定。
**预防门禁：** 新音频长度 >15min 先测整段再上；班日志出现 OutOfMemory 即查本条族。
**来源：** 2026-08-19 调研情报局单视频任务（硬证据：两次整段复现 + 20s 对照 + 班日志 OOM 行）
**✅ 落签（2026-11-05 · 未参与实施的审核者 · 独立核验后自主落签）**: PASS_WITH_LIMITS——① Mac 源 `dyd/asr_local_qwen3.py` 含 ffprobe>900s → 450s 分段 → 逐段 CLI → 拼接（L50-58 / L95-208）；② `dist/dva-runtime-20260820T150155Z.tar.gz`（sha256 `ae008d4e4377…`＝本条所记部署包）与 `dva-runtime-20260909T123945Z.tar.gz`（`7c3f105392c1…`＝09-09 会话日志所记 install 包）内 `dyd/asr_local_qwen3.py`（sha `6bbaa6613198`）及其单测与 Mac 源逐字一致；③ `python3 -m pytest -q -p no:cacheprovider tests/test_asr_local_qwen3.py` 9 passed rc=0；④ Doctor 快验证据在 `docs/移交VV_ASR长音频分段修复_20260820.md`（single-20260820-152826Z · 32.5min · wav≈1949s>900s 走分段 · 10314 字 · exit=0 无 OOM · asr_status=success）。限：fuxi 生产日志（08-22 起 refill 班是否再现 OOM）盘上不可达未核；VV 独立端到端补验无回执；`Projects/DVA/GOTCHAS.md` 同条副本仍为 🔄（本签只落 brain 件）。

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

## DVA 现行链身份与自检（2026-11-06）

### [NOTE-20261106-001] GAI 看板 DVA-Database 节点测的是冻结的 watchlist → 对活链报 D 37（资产身份过期 · 假警报）
**状态**: ✅ 已修复（2026-11-06 未参与实施的审核者 subagent 独立复验 PASS 代签 · 证据：只读实跑 dva_health.py v2 两产物 overall=ok/update_ok=true、空 DVA_DOUYIN_ROOT 时 overall=fail rc=1，运行前后 Database/Douyin 全部 111312 文件 mtime 无变化；manifest 两节点 A 与看板内嵌 JSON 一致、SHA-256 9590169d…）
**优先级**: 🟠 高（看板最差榜首连续数日，掩盖真实状态）
**触发**: 2026-11-06 例行自查：`DVA-Database/_health.json` 由 `dva_health.py v1` 按 `indexes/watchlist.json.updatedAt`（2026-09-26）判 stale → 新鲜度 27 / 自检 50 → D 37。实读权威库 `DVA-Inventory/videos.sqlite3`：`incremental_pipeline_runs` 近 7 天 56 次 run 零失败、镜像回执 `dva-mirror-20261106T143300Z` 当日落 Mac——链是活的。
**硬证据**: `dy_downloader.db` 末次 download_time 2026-09-14 09:15Z；`watchlist.json.updatedAt` 2026-09-26；`global-index.json` 老毛最新 create_time 2026-09-13（`updatedAt=2026-10-31` 系空壳刷新）；而 `authors/<sec_uid>/videos.json` 老毛最新 2026-11-04 16:05Z，与 `videos.published_at` 逐秒一致。
**根因**: 09-18 回流改走 `dva-mac` 增量通道后，`DVA-Database/` 成为**混合层**（覆盖层日更 · db/indexes 冻结），但自检脚本与 GAI manifest 节点仍钉在冻结件上；`permanent/DVA自愈链.md` §二虽早已注明「旧 dy_downloader.db 未被替换、读的人易误判」，没有任何机器把这句话变成判据。
**影响面**: GAI 看板（假 D）· `UPDATE_HEALTH_派工_v2.md` ④「gap_days 40（真实信号）」判断失实 · 任何按 watchlist 判 DVA 新鲜度的读者。
**修法（已实施）**: ① `Projects/DVA/tools/fuxi/dva_health.py` v2：测现行链（镜像回执 + `incremental_pipeline_runs`）→ `Projects/DVA/_health/dva-inventory_health.json`；第二产物 `dva-database-overlay_health.json` 测覆盖层（watchlist 作者 `videos.json` 最大 create_time 对拍权威库，download-only 作者不计）。产物落 `Projects/DVA/_health/`，**不落 `Database/Douyin/`**（FROZEN-20260724 守卫 + 镜像面）。② GAI manifest：新增 `DVA-Inventory` 数据库节点（expect_days 3）；`DVA-Database` 改题「分析覆盖层」、health_file 指第二产物；边改指。③ 看板重推。首轮按原批 P0-A 曾把 DVA-Database 标 archived，实读覆盖层后订正（Doctor 裁丙）。备份 `tools/fuxi/_bak/dva_health.py.bak_2026-11-06_pre_inventory` · `海螺姑娘/data/_bak/asset_manifest.bak_2026-11-06_dva-inventory.json`。
**预防门禁**: ① 数据库节点的 health_file 指向什么，必须能回答「这个文件由现行链的哪一步写」——写不出来的就是退役件；② 自检产物无定时触发者时，conch F3 会按 expect_days 自然降 stale，这是正确行为，不要为消灯把 expect_days 调大。
**遗留**: 两份自检产物目前无定时触发（`dva-refresh.sh` 09-18 退役）——嵌入点归 DVA 链（派工卡见 `海螺姑娘/dashboard/UPDATE_HEALTH_派工_v2.md` ④ 2026-11-06 追记）；`Database/Douyin/DVA-Database/scripts/dva_health.py` 是 fuxi bundle 乘客（INFRA-20260807-003），仍为 v1，勿改勿用。
**来源**: 2026-11-06 Cowork 会话（Doctor 令「审查并修复抖音作者分析库」）· 实读 sqlite ro/immutable · 实跑 v2 正向+负向（根缺失 → fail rc=1）

### [NOTE-20261106-002] DVA-Database 冻结件清单（只记不修 · 归发布链专场）
**状态**: ⚠️ 已知风险
**优先级**: 🟢 低
**现象**: ① watchlist 8 人 → `global-index.json` 40 位作者仅 26 位有目录、7 个目录仅 `info.json`；② `global-index.json` `updatedAt=2026-10-31` 而内容止于 09-13——写者未核；③ `_DEPRECATED_dva.db` 0 B、`dy_downloader.db-shm/-wal` 10-16 遗留、`_health.json.bak_2026-11-04_pre_rerun` 带 ACL；④ `transcript_job` 89 行全 failed（已登记 INFRA-20260831-001）。
**边界**: `Database/Douyin/` 为 fuxi 镜像消费面、FROZEN-20260724 常驻禁写，Mac 侧改了也会被每日回流冲掉——修复点只在 fuxi 侧，随 TODO「DVA · 发布链三洞根治专场」处理。
**来源**: 2026-11-06 Cowork 会话实读
