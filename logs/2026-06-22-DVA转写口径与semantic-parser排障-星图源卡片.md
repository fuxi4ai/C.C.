---
title: 会话日志 2026-06-22 — DVA 转写口径修正 + semantic-parser LLM 排障 + 星图源卡片自动化任务
tags: [log, 星空, DVA]
created: 2026-06-22
updated: 2026-06-22
status: active
type: log
project: 星空 · DVA（跨线）
---

# 会话日志 — 2026-06-22（续）

**项目**：星空（Brain Vault Dashboard）+ DVA（跨线）
**主题**：常更作者表现状核查→transcribe-only 完成口径纠错；semantic-parser 知识图谱构建 LLM 排障（断网→截断→缓存）；星图「源」节点卡片显自动化任务+最近运行时间

---

## 完成的工作

### 线一 · 常更作者表现状核查 → transcribe-only 完成口径纠错
- 核 watchlist + snapshot：8 人全启用，今天 ~16:00(CST) 跑过一轮，黑盒/独夫/浪浪/SansanYe 下载微涨。
- 初判它们「待入库一大堆」**测错了地方**——读 dva.js 发现 **transcribe-only 模式故意跳过 seed入库 + import-transcripts**（产物给 PEC 消费、不入 DVA-DB）；转写产物落 `~/Documents/Database/Douyin/Transcripts/<昵称>/`（`__<aweme_id>.transcript.txt`，按 aweme_id 去重）。
- 核 Transcripts/：四个作者今天都转写了（68/114/116/43 文件、当天新鲜）→ 它们「下载+转写」其实都做了、符合 transcribe-only 目标。
- **修 snapshot + 二级页**：transcribe-only 完成判据改为 `transcripts ≥ 下载−排除 − 容差`，读 Transcripts/ 而非 DVA-DB；文案「下载 N · 转写 M」、去掉误导的入库/待入库。5 个 transcribe-only 由「进行中」转正为完成 → **总览 8/0**。

### 线二 · semantic-parser 知识图谱构建 LLM 排障（三段）
- **断网**：`semantic-parser.js`（discoverConcepts→mergeConcepts→extractRelations，用 `llm-client.js` 调 deepseek-v4-pro）整批 `Connection error`、0 产出。定性＝端点连不上（沙箱网络到不了 DeepSeek/APIYI；必须 Mac 终端跑+source 凭证）。补跑命令：先 `node 基础模块/llm-client.js` 自检端点通，再跑 build；缓存（`~/Database/Douyin/.llm-cache`·7天）支持断点续。
- **JSON 截断**：连上后整批 `JSON 解析失败`。根因＝推理模型 max_tokens 偏低致 JSON 被截断。**修 A** chatJSON 失败兜底打印原始返回（截断判断）；**修 B** 抬 max_tokens（concept 2000→4000 / merge 3000→8000 / relation 1500→4000）→ merge 由全挂→1061→920（−141 同义词）、关系流起来。
- **残留抖动 + 缓存补丁**：诊断 A 照出残留真因＝**空响应（len 0）+ 流中断（559 字符截句中，远低于 4k token，非 max_tokens）**＝DeepSeek 端点偶发，非配置。**改 chatJSON**：缓存收归本函数（只缓存解析成功的好文本·重试成功也缓存·坏值/空响应不缓存·旧坏缓存解析失败自愈）+ 空响应短退避 + 诊断分类（空响应/未闭合截断·流中断/格式非法）。抽取正则一字未动（保已成功批次行为）。
- 末轮整跑完成：920 概念 / 635 关系 / 三文件落盘（Reports/）。

### 线三 · 星图「源」节点卡片显示自动化任务
- 约束：任务 lastRunAt 是 **app 内部态**（`Scheduled/<task>/` 只有 SKILL.md、无运行记录），snapshot 读不到 → 走「随刷新烘焙」：snapshot 出 `source_tasks` 映射（含 task_id + last_run 占位），看板刷新时由 agent 调 `list_scheduled_tasks` 按 task_id 填 lastRunAt。refresh 任务 SKILL.md 加了这步。
- index.html openStarCard：源节点「上游」显「🤖 任务名」，下一行「最近运行 YYYY-MM-DD（今天/昨天/N天前）」（换行·到日·相对提示·按日历日）。
- **源→任务映射两轮校正**（Doctor 把关）：① 渊图 显示名改「金融领域常更作者语料提炼」；② **收窄**——只列有产出/拉取该源的定时任务：渊图/Tushare/四维度课件/管线JSON(baize产出)/抖音(本机cron·无时间)；**去掉** Gangtise edb / SMM/web补价 / 龙鱼五力（被 baize 消费的外部数据商/他项目输入、非任务产出 → 上游显「—」）。

---

## 做出的决策

| 决策 | 原因 | 影响 |
|------|------|------|
| transcribe-only 完成按 Transcripts/ 判（下载≈转写） | 该模式故意不入 DVA-DB、转写产物在 Transcripts/；拿 DVA-DB 入库/subtitle 判是测错地方 | snapshot transcripts 字段 + 二级页文案改 |
| semantic-parser 抬 max_tokens（4k/8k/4k） | deepseek 推理模型思考吃预算→JSON 截断 | merge 由全挂转通 |
| chatJSON 缓存收归本函数 | 根除「非空但解析失败的坏内容被缓存、重跑老命中坏值」；重试成功也缓存→补满收敛 | 重跑只命中真没成过的批次·坏缓存自愈 |
| 源「上游」只列有产出/拉取任务的源 | 外部数据商(Gangtise)/外部行情(SMM/web补价)/他项目输出(龙鱼五力)是被消费的输入、非任务产出 | 这三个源上游显「—」 |
| 任务运行时间走「随刷新烘焙」 | lastRunAt 是 app 内部态、磁盘读不到 | refresh 任务加 list_scheduled_tasks 填 last_run 步 |

---

## 遗留问题 / 待办

- [ ] Doctor 真机提交：DVA 仓（llm-client.js + semantic-parser.js）+ brain 仓（dashboard-snapshot.py）
- [ ] semantic-parser 若想关系更全：重跑（缓存让已成批次秒过、只补空响应/中断的）；DeepSeek 端点偶发抖动治不绝，多跑一两次收敛
- [ ] 可选：chatJSON retries 2→3 / 关系 max_tokens 再抬（现已能跑通·按 G-12 暂不动）
- [ ] concepts.json/relations.json 下一步 → dva-to-graphify / 入渊图

## 相关笔记

- [[星空]] · [[DVA]] · [[渊图]]
- Projects/DVA/基础模块/llm-client.js（chatJSON 缓存收归+空响应退避+诊断分类）
- Projects/DVA/3-文本分析/semantic-understanding/semantic-parser.js（max_tokens 4k/8k/4k）
- brain/.tools/dashboard-snapshot.py（dva transcripts 字段 + source_tasks 收窄）
- Artifacts/brain-vault-dashboard/index.html（源卡片自动化任务·换行到日相对提示）
- Scheduled/refresh-brain-vault-dashboard/SKILL.md（烘焙 lastRunAt 步）
- [[2026-06-22-看板DVA日报数据驱动与星图反哺修复]]（前序）
