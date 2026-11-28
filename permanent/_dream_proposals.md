---
title: Dream 提案队列
tags: [dream, proposals]
created: 2026-11-21
updated: 2026-11-23
status: active
type: reference
---

# Dream 提案队列（只追加 · 状态由 Doctor 批/拒时改）

### [DRM-20261121-1231-01] 官方云端 Cowork 会话不进真相层，Dream 核其日志只能落「查无出处」
- 类型：新记忆
- 内容：在真相层「已知局限」补一条：2026-11-04 迁官方云端后，云端 Cowork 会话不在本机 `~/.claude/projects/` 下，`transcript_ingest.py` 抽不到（`chats/transcripts/2026-11/` 里 `cowork_` 抽取件只到 2026-11-04 共 16 个）。凡写于云端 Cowork 会话的日志（例：`2026-11-20-云端定时班四处改班.md`、`2026-11-20-brain-dream每日班建班.md`），只能靠别的 Code 会话转贴、Code 会话的工具输出或当轮 `list_triggers` 等旁证核对；其余陈述必然「查无出处」，不代表记错。另建议 brain-dream Step 2 增设第四类「真相层未覆盖」，与「查无出处」分开计数，免得把覆盖缺口误读成转述过度。
- 理由：持久（云端会话的存放位置不会自己变）；难复得（要对照 PRD R5 的抽取口径与 11-04 迁移才看得出，本轮是核两篇日志时才发现）；会再用（每次 Dream 遇到 Cowork 会话日志都会撞上，/resume 读核对结果时也要知道这一口径）。
- 证据：本轮 2026-11-21 dream 实读 `chats/transcripts/2026-11/` 列表（cowork_ 16 个，全为 2026-11-04）；`logs/checkpoints/2026-11-19_真相层_PRD.md:79`（R5 只收 `/.claude/projects/` 下的会话）；日志 `2026-11-20-云端定时班四处改班.md` 第 15 行（会话标为 Cowork、跨三天）在真相层无对应主会话。
- 建议落点：`chats/README.md`「已知局限」一节；`.skills/brain-dream/SKILL.md` Step 2 判定分类（技能改动须 Doctor 批）。
- 状态：已批（Doctor 2026-11-23 · 两处都批）——已落 `chats/README.md`「已知局限」、`.skills/brain-dream/SKILL.md` v1.4

### [DRM-20261122-1231-02] 去重键须含全部区分维度（多写方共用记录）——升格通用教训
- 类型：新记忆
- 内容：在 `permanent/通用教训.md` 末尾 G-X 区新增一条：多个写方（或多维口径，如 scorer、horizon）共用同一记录时，「同键覆盖」的键必须包含全部区分维度；只按日期等单一维度去重，会让后写方静默删掉另一方的当日条目。门禁：写后断言「同日其他写方条目数不减」，并配持久化负向测试。成员：龙鱼 ERR-20261122-001（record_writer 只按 analysis_date 去重，09:08 deepseek 批跑抹掉 5 只 claude 11-22 条目）、渊图 ERR-20260608-002（价格去重键漏 horizon，现价/预测同日撞键误并）。
- 理由：持久——去重键设计会在新写方接入时反复出现；难复得——这类丢失不报错，要对比 mtime、report_path 和覆盖前快照才看得出（本轮靠对比文件反证）；会再用——龙鱼、渊图两个项目已各出一次，GOTCHAS 合同规定跨项目出现即应升格。
- 证据：本轮 dream 盘上实读 `Database/龙鱼-标的分析库/records/` 5 只 mtime 09:08 UTC、`record_writer.py` L83–86、`对比校正/全库_对比_20261122.md`；独立 subagent 复核成立；`permanent/经验索引.md:287`（渊图 ERR-20260608-002）。
- 建议落点：`permanent/通用教训.md` G-X 区末（编号落盘时 grep 取 max+1）；龙鱼 ERR-20261122-001 与渊图条目各加反链。
- 状态：已批（Doctor 2026-11-23）——已立 `permanent/通用教训.md` [G-X291]，龙鱼 ERR-20261122-001、渊图 ERR-20260608-002 加反链

### [DRM-20261122-1231-03] brain 侧 PEC/GOTCHAS.md 索引缺 G-31～G-47
- 类型：事实订正
- 内容：`brain/PEC/GOTCHAS.md` 索引补 G-31～G-47 各一行（标题与状态从 `Projects/PEC/GOTCHAS.md` canonical 取）。
- 理由：索引现只有 G-01～G-30 与 G-48（本轮 grep 实数），按索引找 PEC 坑会漏 17 条；属新增内容，超出 dream 订正射程，故提案。
- 证据：本轮 `grep -oE "G-[0-9]+" brain/PEC/GOTCHAS.md | sort -u`；日志 `logs/2026-11-22-PEC深圳APEC追踪与Codex自动化收录核对.md:51` 已记此隐患。
- 建议落点：`brain/PEC/GOTCHAS.md` 索引表。
- 状态：已批（Doctor 2026-11-23）——`brain/PEC/GOTCHAS.md` 候选区索引补 G-31～G-47 共 17 行

### [DRM-20261123-1231-01] G-X287 状态行由实施会话自标「✅ 已修已验」，未经未参与实施的审核者代签
- 类型：事实订正
- 内容：`permanent/通用教训.md` [G-X287] 状态行现为「✅ 已修已验」，系实施会话自己改的；建议派未参与实施的 subagent 从 `skill_release.py status`、`check_skill_parity.py`、两套测试实跑复核后再决定是否保留 ✅，未复核前回到「🔄 已修待验」。
- 理由：GOTCHAS 自动登记合同——新条目实施者不得自行标 ✅（事务性项可由未参与实施的 subagent 独立审核后代落）。该条独立复核 PASS_WITH_LIMITS 发生在 D1–D3 修补之前，修补后未再派审；Doctor 终端只实跑了一个测试，未签字。状态行属 dream 订正射程之外，故提案。
- 证据：会话 69a8198f 2026-11-23 02:13Z 助手原文「G-X287 我已改成「✅ 已修已验」」；同会话 15:30Z「复核结论是有限通过……D1、D2、D3……现在一并修掉」；盘上 `permanent/通用教训.md` G-X287 状态行（本轮实读）。另：该会话未 /save，logs 下无对应日志。
- 建议落点：`permanent/通用教训.md` [G-X287] 状态行。
- 状态：已批（Doctor 2026-11-23 · 派审核者复核定状态）——G-X287 状态行先回 🔄，未参与实施的审核者 2026-11-23 复核 PASS_WITH_LIMITS 后代落 ✅

### [DRM-20261124-1231-01] Settings 注入原文「硬约束」条缺「提交命令整合」后半句，与镜像第 26 行不一致
- 类型：注入层
- 内容：本轮（云端 Cowork 定时班）注入的 Settings 偏好块里，「硬约束」条止于「……一次会话动 ≥2 个 git 仓时合并成一个 code block 分段连发。」；`permanent/全局偏好-Settings镜像.md` 第 26 行在此之后还有一整句「提交命令在安全前提下整合成一条贴出：add→commit→push 用 `&&` 串联……须先看输出再定下一步时才拆开分步。」。前半句（含「或音视频/大文件下载、ASR」「接口取数不在此限，可在沙箱跑」）逐字一致。请 Doctor 定：① 重贴 Settings 补回该句（镜像不动）；或 ② 该句确属有意不放进 Settings（例如长度限制），则镜像第 26 行与维护注记 L101「提交整合句不动」改写说明。
- 理由：维护注记 L101 写明本次改版「git 部分与提交整合句不动」、L103 挂「⏳ 待下场 Cowork 新会话起手逐行比对验证」；本轮即该次比对，结果第 26 行不一致。注入层属 dream 禁改范围，只提不改。
- 证据：本次运行 2026-11-24 12:31Z 注入的偏好块（本轮实读）对 `permanent/全局偏好-Settings镜像.md:26`（本轮实读）；`permanent/全局偏好-Settings镜像-维护注记.md:101,103`；日志 `logs/2026-11-23-Settings镜像硬约束收窄与命令块单行.md:21,37`。
- 建议落点：Claude Settings 偏好块「硬约束」条，或 `permanent/全局偏好-Settings镜像.md:26` + 维护注记。
- 状态：待批

### [DRM-20261128-0248-01] 「提交命令不带联合作者行」只在 permanent，注入层没有，立规后仍有提交命令带上署名
- 类型：注入层
- 内容：把 `permanent/Doctor协作偏好.md:102`「提交不带联合作者行（2026-11-26 立 · 原话「以后提交命令不带联合作者那行」）」同步进注入层——建议落 Claude Settings 偏好块「硬约束」条（git 相关句之后）并同步 `permanent/全局偏好-Settings镜像.md` 与维护注记；或至少进 `brain/CLAUDE.md`。
- 理由：运行环境每场都会注入「提交说明末尾加 Co-Authored-By」的署名提示，与 Doctor 规矩直接冲突；规矩现只在需主动读取的 permanent 笔记里，注入层四件与 Settings 镜像 grep「联合作者 / Co-Authored」均无命中（本轮实读）。立规 22 分钟后另一会话给出的提交命令仍带该行，说明只靠 permanent 拦不住。
- 证据：会话 693b747e 2026-11-26 12:55:06 Doctor「这是"联合作者声明"？」、12:55:56 Doctor「以后提交命令不带联合作者那行」；会话 48040bb7 2026-11-26 13:17:41 Doctor 终端执行的提交命令仍含 `-m "Co-Authored-By: Claude Opus 5.5 …"`（bash-input 原文）；本轮 grep `CLAUDE.md`、`portable/claude-code/CLAUDE.md`、`permanent/全局偏好-Settings镜像*.md` 无命中。
- 建议落点：Claude Settings 偏好块「硬约束」条 + `permanent/全局偏好-Settings镜像.md`（同步维护注记）；备选 `brain/CLAUDE.md`。
- 状态：待批
