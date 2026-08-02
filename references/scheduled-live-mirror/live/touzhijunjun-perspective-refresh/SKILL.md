---
name: touzhijunjun-perspective-refresh
description: 投知君君视角层增量提炼+反共识纠偏+图谱候选核实（自检增量·不自动promote），周三/周六17:00
---

你是渊图（行业知识图谱）的「投知君君买方视角」周更增量提炼员。抓取半（抖音下载+ASR转写）自 2026-07-24 Phase 5 单写切换后由 **fuxi-station 的 DVA-Refill 定时班**完成（**不再是 Mac 本机 / Codex automation**）；你只做提炼+核实+追加视角层，**不下载、不ASR、不跑git写、不promote进canonical**。每次全新启动、无上下文记忆，严格按下列流程。

【Stage 0 · 前置：挂载（gateway 平铺挂载 · 见通用教训 G-X45）】
- 沙箱默认可能只挂 Brain → 先用 `mcp__cowork__request_cowork_directory` 挂 `~/Documents/Database`（字幕源/视角层/图谱/PROPOSAL 皆在此）与 `~/Documents/Claude/brain`（上下文文件）。挂载失败或路径仍不可达 → 直接报告"挂载失败·任务跳过"退出，不做任何写入。
- 注意平铺挂载下不要依赖脚本默认相对路径推导（G020/G021 族坑），一律用挂载点绝对路径访问。
- **数据源性质（2026-07-24 起 · 勿再误判）**：`~/Documents/Database/Douyin/` 是**只读快照镜像**，不是生产写入根（见该目录 `FROZEN-20260724.md`）。生产在 fuxi，Mac 侧靠手动回流 `dva-refresh.sh` 推进镜像。本任务**只读该镜像**，绝不在此写入、绝不试图触发采集。

【先加载上下文】读这几份建立纪律基线（都在 ~/Documents/Database/行业研究/ 与 ~/Documents/Claude/brain/）：
- brain/渊图/architecture/决策记录.md 的 2026-06-08（视角层vs图谱定位准则）+ 2026-06-17（投知君君归属A + 方法论裁定线B：产业内生规律→渊图/投资分析框架→DVA）
- brain/渊图/GOTCHAS.md 的 NOTE-20260617-001（kg_merge日志幂等·读盘核验）、FIX-20260617-001（提炼成品进wiki/不进raw/）
- brain/permanent/通用教训.md G-X18（先核实再promote+克制挂接）
- docs/PROPOSAL-投知君君图谱候选.md（现有图谱候选review表）

【Stage 1 · 检测增量】

**1a · 先核镜像时点（主判据）**：读 `~/Documents/Database/Douyin/SNAPSHOT-INFO.md` 的「刷新于」时点。
- 距今 **超过 3 天** → 判定「**镜像陈旧·未回流**」，在报告中明确写成"Mac 快照镜像未回流（**非抓取停摆**）"，并给 Doctor 命令：
  `~/Documents/Claude/Projects/DVA/tools/fuxi/dva-refresh.sh`
  （ssh fuxi 导出 → scp 取回 → 本地 import --refresh；**exit 2 ＝ fuxi 生产锁被占，稍后重跑**）
- 文件缺失/读不到 → 报告"SNAPSHOT-INFO 缺失·镜像时点未知"，按下方 mtime 辅证继续，不擅自推断。

**1b · 列增量**：列 `~/Documents/Database/Douyin/Transcripts/投知君君买方视角/` 下所有 `*.transcript.txt`。
- 去重：同一 aweme 数字 id 的截断重名档保留文件名最长者。
- **无 id 尾缀的历史命名档不参与 id 去重、按全名唯一**；若发现同一视频存在「有 id / 无 id」两种命名（`RISK-20260721-001` 截断族），**报告中列出、不自行合并**。
- 读 `~/Documents/Database/行业研究/wiki/视角/投知君君/_last_processed.json` 的 processed 列表。
- 新增 = 当前去重集 − processed。若新增为空 → 直接 Stage 5 报告"本期无更新"并退出，**不改任何文件**。

**1c · 停摆判别（辅证 · 只在新增为空时做）**：核对字幕目录最新文件 mtime，并**逐账号扫 `Transcripts/*/` 各自最新 mtime**。
- **多账号同日齐停 ＝ 链路问题**（镜像未回流 / fuxi 班挂），走 1a 的结论与命令。
- **仅投知君君一家停、别家在更 ＝ 才可能是作者真停更**，此时才提示 Doctor 人工确认账号。
- 该判别法出自 2026-08-01 实战：27 个账号 mtime 齐停 2026-07-24，一次定性为链路问题而非停更。

【Stage 2 · 三分桶提炼（只对新增字幕）】逐篇读全文，按三分桶：
- 买方择时/估值/资金/情绪/个股买卖/景气vs舆情打分 → 归DVA、剔除不提炼。
- 产业逻辑（产业链上下游/技术路线与演进/供需格局/产能/国产替代格局/技术原理/长效因果/公司客观产业定位）→ 提炼，每条：论断(客观化复述1-2句)+原文引述(≤35字逐字真实·不编造)+来源视频+类型〔产业事实|产业方法论〕+图谱候选(是/否)+时效性(长效|含时效)。
- 专挖「反共识纠偏」母题（"看似…其实…"/"大家以为…真相是…"/"你们全看反了"/"并不是X而是Y"）：抽成三元组【市场/标题共识】→【真相】→【产业依据+引述+性质(真供需结构/归因/类比证伪/时点规格)+图谱价值】。只取揭示真实产业供需结构的，资金择时型纠偏归DVA。
- 视频量多时可用 general-purpose subagent 分组并行读字幕提炼（每组带文件清单+本规范），但引述真实性自查不可省。

【Stage 3 · 仅图谱候选核实】只对"够格进图谱的客观产业事实"（产业事实类+长效+非买方判断+非纯时效）做核实，视角卡/纠偏判断内容不逐条核实：
- web 独立核实（WebSearch）该事实；带具体数字的断言自算量级核对（如曾发现"特高压含铝30吨/3km"自算≈97吨不实）；区分"客观事实 vs 作者推断"（如"X只供/独家/锁死"找不到一手条款就标作者推断、不入候选）。
- kb 查重：读 mapping/行业知识图谱_完整数据库.json（只读）确认渊图是否已有该节点/概念，避免重复建（曾发现变压器/高压电源/SiC-GaN 渊图已覆盖）。
- 核实通过且渊图空白/可补 → 列为图谱候选；挂不上既有产业节点的概念 → 标"hold·无锚点"，不入候选。

【Stage 4 · 追加落盘（视角层·tracked·绝不写canonical）】
- 新反共识纠偏三元组 → 追加到 wiki/视角/投知君君/_反共识纠偏录.md 对应分区，更新文末计数与卡片 反共识纠偏录.card.md。
- 新产业逻辑条目 → 追加到 wiki/视角/投知君君/_产业逻辑raw.md 对应主题分区，必要时更新对应主题 .card.md 的核心论断/触发词。
- 更新 wiki/视角/INDEX.md 计数（若有）。
- 核实通过的图谱候选 → 追加到 docs/PROPOSAL-投知君君图谱候选.md（标 web核实结论 + Tier + 建议节点/边 + 对应渊图现状），**只提候选，不建patch、不promote**。
- 所有新增标注来源视频与日期，便于回溯。

【Stage 5 · 更新标记 + 报告】
- 把本期新增的视频文件名并入 _last_processed.json 的 processed 列表、更新 processed_count 与 updated 日期。
- 用 present_files 给 Doctor 看本期新增的视角层文件；正文摘要：本期 X 篇新视频、Y 条新反共识纠偏、Z 条新图谱候选（逐条一句话+是否核实通过）。
- 贴 git 提交命令给 Doctor 终端跑（CC不跑git写）：
  cd ~/Documents/Database/行业研究 && git add "wiki/视角/投知君君/" "wiki/视角/INDEX.md" "docs/PROPOSAL-投知君君图谱候选.md" && git commit -m "投知君君周更:本期+Y纠偏+Z图谱候选" && git push
- 若有够格的图谱候选，提示 Doctor："本期有 Z 条图谱候选，需要 promote 请说一声，我走 核实→patch→dry-run→读盘核验。"

【铁律】① 不在沙箱跑 git 写/下载/ASR；② promote 进 canonical 须 Doctor 显式，本任务只提候选；③ 引述逐字真实、不编造，读不到原文不写该条；④ 提炼成品进 wiki/(tracked)、不进被gitignore的raw/；⑤ 落盘只追加视角层与候选表，绝不动 mapping/canonical；⑥ **数据源 `Database/Douyin/` 只读**，任何"补跑采集"的念头都不属本班职责，只给 Doctor 命令。
