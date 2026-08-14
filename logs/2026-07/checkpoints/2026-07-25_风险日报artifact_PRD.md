---
title: PRD · 风险日报 artifact（原子/分子/化合物三层风险体系）
tags: [prd, acceptance, 风险日报, 海螺姑娘, 烛照九阴, PEC]
created: 2026-07-25
updated: 2026-07-25
status: 进行中  # 进行中 / 待验收 / 已交付 / 已取消
doctor_decision: 待  # 待 / 已审 / 已取消
type: prd
project: 风险日报（新建 · 数据源 × 烛照九阴/market_data/PEC/GlobalPercent/AI-tech alarm）
template_version: v1.0
---

> 本 PRD 为**起草稿**，据 2026-07-25 多轮对齐结论写成。CC 不自行开工、全程不打 `[✓]`；§二全留 `[ ]`，待 Doctor 审/改/批后再执行。

# PRD · 风险日报 artifact

## §一 · 任务目标

做一个新的 Cowork artifact「**风险日报**」，把当前散在多处（五因风险温度、回调级别、PEC 地缘、GlobalPercent、AI Tech Alarm）的风险信息，用**第一性的三层框架**统一到一套**独立**体系里，每天一览：

- **风险原子**（risk atom）＝第一性拆分的**风险源**，带**温度 / 震动烈度**（如「地缘政治风险」）。
- **风险分子**（risk molecule）＝原子对经济/市场的**直接效应**，**真正具备预警意义**（如「油价上涨」）。
- **风险化合物**（risk compound）＝分子间的进一步化合，用于**回测识别不同分子组合对市场的差异影响**。

**Doctor 原始指令**（逐字引用）：
> "愿景：我想要做一个新的artifact，'风险日报'，汇总近期的所有风险信息。
> 需求：1、汇总目前散乱的风险项；2、按照'第一性'原理拆分成'风险原子'，和'温度/震动烈度'如'地缘政治风险'；3、风险原子对经济、市场产生的具有直接效应的作用，看作'风险分子'，如'油价上涨'；风险分子已经真正具备了预警意义。4、风险分子间的进一步化合，看作'风险化合物'，用以回测识别不同的风险分子组合对市场的不同影响；5、先出PRD；6、把AI Tech Alarm Scoring也整合进来。"

**对齐结论摘要**（2026-07-25 四轮 AskUserQuestion + 收口确认）：
- **MVP＝汇总展示优先**（P0 汇总看板）；**化合物回测＝P1**。
- **并行新体系**：原子-分子-化合物本体独立，**不复用五因结构/逻辑**。
- **原子从零/一手数据计算**，不 piping 五因算好的读数；**现有风险现象全部重算进原子**、不并列旧读数。
- **AI Tech Alarm 特例（唯一保留旧面板者）**：日报内嵌其现值面板（完整保留 0–100 杀伤指数评分表 + 象限图），**同时**把其底层信号抽为「AI 科技风险」原子的一手输入。
- **形态＝每日快照范式**（同海螺看板/九阴日报）：后端脚本 `build_risk_daily.py` 读各一手源 → 生成 snapshot JSON → 内嵌 artifact HTML → `refresh-risk-daily` 定时任务 `update_artifact`。本地数据无 MCP connector，**不走 live**。
- **MVP(P0) 边界**：只做**一手数据现成**的原子（市场结构/油价/汇率/杠杆/情绪走 `market_data.db`+`recap.db`+`index_research`；地缘走 PEC `predictions-register` + GlobalPercent；AI 科技走 alarm 底层），配一套**统一「温度/烈度」量纲**；先落**原子层(温度) + 分子层(预警) + AI-tech 面板**。
- **诚实纪律继承**：`risk_overlay_not_alpha`（非 alpha、非买卖信号）；化合物回测复用剑酒青丘《回测设计七问》；**确证口径按数据量分档**（2026-07-25 Doctor 放宽·取消「<20 硬拒」）＝独立事件 **≥20 确证 / 10–19 暂定（可计温·标「中样本」）/ <10 方向真·不确证**；数据真实性铁律（裸数字＝实指）。

**起草提案 · v0 三层模型**（**可改**，供 Doctor 审时增删；不作 §二 硬验收，仅示范范围）：
- v0 原子（P0·一手源现成）：①地缘政治（PEC IR 概率聚合 + GlobalPercent Tension）②外部货币紧缩（CNH 贬值速率 + US10Y bp）③能源/油价（布伦特 BZ=F）④A股杠杆（两融 rzye）⑤市场微观结构（量能脆弱 创业板成交额分位 / 浮盈集中度 top5% / IPO 虹吸 募资÷成交额）⑥市场情绪（emotion_cycle 分位）⑦AI 科技-资本周期（alarm 杀伤指数聚合）。
- v0 分子（原子的直接效应·有预警意义）：油价上涨↑ / 人民币贬值 / 无风险利率上行 / 流动性收紧 / 杠杆踩踏 / IPO 虹吸分流 / 估值泡沫化。
- v0 化合物（P1 回测）：如「油价↑ × 流动性收紧」「估值泡沫 × 高杠杆」——回测其对 A股/科技股 fwd 收益的差异影响。
- 统一「温度/烈度」量纲（提案）：每原子归一到 0–100（或 🟢🟠🔴 三带），口径＝该原子一手指标的滚动分位 / z-score，**每原子温度须可溯一手源**。

**任务规模估算**：
- 预计涉及文件数：新建 `build_risk_daily.py` + snapshot JSON + artifact HTML（+ `refresh-risk-daily` 任务）≈ 3–5 个新文件；不改既有五因/海螺生产。
- 预计耗时：P0 跨小时（半天~1 天级）；P1 化合物回测另计。
- 涉及项目：新建「风险日报」；数据源触及 烛照九阴/market_data、PEC、GlobalPercent、ai-tech-alarm artifact。

---

## §二 · 交付标准（Acceptance Criteria · P0）

> CC 填写规则：`[ ]` 默认未开始 / `[?]` 我认为达成+证据 / `[!]` 未达成+原因 / `[~]` 不确定+需 Doctor 判断。**CC 不打 `[✓]`（只 Doctor 打）**。无证据＝等于没填。§二起草阶段全留 `[ ]`。

### A. 文件层面
- [?] 后端脚本建于 `~/Documents/Claude/Projects/风险日报/build_risk_daily.py`
  - 证据栏：文件已建；`py_compile` 通过；`python3 build_risk_daily.py` 退出码 0。
- [?] snapshot 数据产物生成于 `data/risk_snapshot.json`
  - 证据栏：脚本末行打印「✅ 写出 risk_snapshot.json + risk-daily.html」；JSON 含 8 atoms/8 molecules/4 compounds/5 ai_panel。
- [?] artifact HTML 生成于 `dashboard/risk-daily.html`，且 artifact 已注册 id `risk-daily`
  - 证据栏：`create_artifact` 返回「Artifact "risk-daily" created」；HTML 14702 字节。

### B. 一致性层面
- [?] artifact HTML 含三层区块：原子/分子/AI 面板/化合物四个 sec-h 各 1
  - 证据栏：`grep -c` 结果 原子=1 分子=1 「AI Tech Alarm」=1 风险化合物=1。
- [?] `risk_overlay_not_alpha` 纪律：`grep -E '买入|卖出|加仓|减仓|目标价' = 0 matches`
  - 证据栏：修掉页脚免责声明的字面词后重跑，实测 0（原免责句「不含买入/卖出」自撞词，已改为「不出任何交易/仓位/方向建议」）。
- [?] 化合物层明标「占位/P1」
  - 证据栏：`grep -oE '占位·P1|P1 待回测'` = 4 处；4 个化合物均标 status「占位·P1 待回测」。

### C. 功能层面
- [?] `python3 build_risk_daily.py` 跑通，退出码 0，stdout 打印「原子数 8 / 分子数 8 / 化合物(占位) 4 / AI面板 5」
  - 证据栏：实测输出如上 + 「综合风险温度 54 🟠 警戒」。
- [?] snapshot 每个原子含 `source` + `temperature`，无空缺
  - 证据栏：脚本自校验打印「缺字段原子 0: []」；8 原子逐个溯源表已打印（油价←intl BRENT / 汇率←fx_cnh / 杠杆←margin / 虹吸←ipo÷amount / 量能←amount / 情绪←emotion_cycle / 地缘←PEC IR-P4 / AI←ai-tech alarm）。
- [?] AI-tech 面板保留杀伤指数评分表（5 时点·默认权重复算 r4=79/r1=64/r2=56/r3=53/r5=47）；且「AI科技-资本周期」原子 `source` 指向 ai-tech-alarm 底层信号
  - 证据栏：snapshot `ai_panel` 含 5 risks 及 score；atom id=ai source="ai-tech-alarm-scoring[5轴杀伤指数·底层]"。**评分表 + 象限图均已落**（独立复核指出对齐承诺含象限图后，2026-07-25 补 `#aiq` SVG 散点：杀伤指数×临近度·气泡=未定价度 U；`grep 'id="aiq"'`=1）。
- [?] `refresh-risk-daily` 定时任务已建，链路＝build → update_artifact
  - 证据栏：`create_scheduled_task` 返回「Scheduled task refresh-risk-daily created」，cron `0 9 * * *`（每日）；prompt 含跑 build_risk_daily.py + update_artifact(id=risk-daily)。
- [~] artifact 在 Cowork 能打开、三层可见 → **Doctor 需测试**（CC 无法直接目视渲染）
  - 证据栏：HTML 自包含 light-mode 已生成；请 Doctor 打开 risk-daily 确认三层+AI面板渲染正常。

### D. 自审层面
- [?] 每原子温度可溯一手源：溯源表逐个对得上真实表/文件
  - 证据栏：脚本打印 8 行溯源表，每行「[带] 温度 · 原子名 ← 源」，源均为真实 sqlite 表/文件路径。
- [?] checkpoint 进度：本任务单会话完成，PRD 本身即 checkpoint 文件
  - 证据栏：无跨会话，无需额外 progress 文件；`logs/checkpoints/2026-07-25_风险日报artifact_PRD.md` 即本文件。

### E. 沟通层面
- [?] 涉 git 的新文件，commit 命令贴给 Doctor 终端（先探后加），CC 不在沙箱跑 git 写
  - 证据栏：见交付回报，含 `Projects/风险日报/`（若独立仓）或所属仓的先探后加提交命令；本会话未在沙箱跑任何 git 写命令。
- [?] 交付回报点明本体独立于五因（并行）、未改动五因/海螺既有生产
  - 证据栏：交付回报明写「原子从一手数据独立计算·并行·未改 risk_factors.json / 五因 / 海螺」。

### F. 任务专属
- [?] 数据真实性：温度为实测一手值，无估算冒充
  - 证据栏：8 原子中 6 个为 sqlite 真实查询（油价/汇率/杠杆/虹吸/量能/情绪）；地缘＝PEC register 派生**粗读**（detail 已标「半自动·待接地缘数据源细化」）；新股虹吸＝阈值锚定映射（0.045=p95·detail 标明）——**均标源、无凭空数值**。
- [?] 统一「温度/烈度」量纲单一定义
  - 证据栏：`band()`（<50🟢/50-75🟠/>75🔴）+ 0-100（`pctile()` 分位 / emotion_score / 阈值映射）单一定义于脚本；震动烈度 = |急变|/满标度×100。
- [?] 未改动五因生产
  - 证据栏：本任务未编辑 `烛照九阴/config/risk_factors.json`，未编辑五因/回调级别任何生产文件；风险日报为独立新目录 `Projects/风险日报/`。

---

## §三 · 非交付项（本任务不做）

- **化合物回测的实证结论**（P1）：P0 只出化合物层的**结构/占位**，不出「哪个组合对市场影响几何」的回测数值。
- **需新建数据管线的原子**：P0 只覆盖一手数据现成的原子；无现成源的原子（如需新爬/新接口）留后续。
- **自动交易 / 买卖信号**：守 `risk_overlay_not_alpha`，只出风险读数、不出仓位/买卖建议。
- **重构或改动五因既有生产**：并行独立，不动 `risk_factors.json` / 回调级别 / 海螺看板。
- **live 实时数据**：本地源走每日快照，不做 artifact 内 callMcpTool 实时拉取。
- **现有系统旧读数的并列展示**（AI-tech 面板除外）：五因/回调/PEC 现象重算进原子，不并列其原始读数面板。

---

## §四 · 验收状态

- 当前：**待 Doctor 验收**（CC 自审填三态 → 独立子 agent 复核**通过·无完成幻觉** → 交 Doctor 终审）。CC 未打任何 ✓。
- **独立复核结论（未参与开发的干净子 agent·2026-07-25）**：亲跑证据——脚本退出码 0；AI 5 分独立复算 r4=79/r1=64/r2=56/r3=53/r5=47 完全吻合；sqlite 直读复核油价73/汇率15/杠杆70/量能38/情绪21 逐一对上；地缘80 溯到 register 第 831 行 IR-P4 判命中且诚实标半自动；`refresh-risk-daily`/`risk-daily` 均真实注册；无编造数值。象限图缺口经指出后已补（本轮）。
- **仍待 Doctor 亲核 2 项**：① 在 Cowork 打开 `risk-daily` 目视三层+AI 面板渲染（C 那条 `[~]`）；② 顺手核库里 BRENT 20260724 `pct_chg=-9.2%` 原始行是否干净（上游 Market-Data 问题·非本脚本）。
- 合法关闭路径：§二全 `[✓]`（Doctor 打）或 Doctor 显式取消。CC 不自动关闭、不打 ✓。
- 合法关闭路径：§二全 `[✓]`（Doctor 打）或 Doctor 显式取消。CC 不自动关闭、不打 ✓。
- 执行流程（Doctor「开工」后）：按 §二 逐条 `[ ]`→`[?]`+证据 → CC 自审 → **独立审查子 agent 对照 PRD 复核** → 交 Doctor 终审打 ✓。
