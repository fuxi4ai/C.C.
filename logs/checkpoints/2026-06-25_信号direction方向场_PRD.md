---
title: PRD · 信号 direction 方向场
tags: [prd, acceptance, 烛照九阴]
created: 2026-06-25
updated: 2026-06-25
status: 进行中  # 进行中 / 待验收 / 已交付 / 已取消
doctor_decision: 待  # 待 / 已审 / 已取消
type: prd
project: 烛照九阴
template_version: v1.0
---

# PRD · 信号 direction 方向场（多/空）+ 日报兑现卡方向感知 + 星空正面星(D>S)显示

## §一 · 任务目标

**动机**：当前 closure 引擎是「只做多」单向口径——`yuantu_buy_signals` 把每条信号都当买点，「代表 ETF 对 510300 超额连续为正 ≥ Y=3 日」才算进入趋势/兑现。对「供给过剩」这类**利空/空头逻辑**方向是反的：典型如 `concept_SolarGlassOversupply`（光伏玻璃供给过剩），KG trend=↓↓、category=问题、受益标的为空，却因一段 +2.4% 反抽噪声被误判 closing/进入趋势，而真实 excess_cum=−11.3%（板块大幅跑输）。需给信号补**方向场**，让日报「兑现卡」按多/空分治，根治利空被当买点误追踪。

**范围**：给 `yuantu_buy_signals` 加 `direction`（多=买入/空=卖出）字段，来源为渊图 KG `trend`+`category` 映射；closure 引擎与 `gen_daily_report.py` 按方向分治呈现与追踪。**本轮只动 yuantu_buy_signals**（industry_signals 无 KG 节点链接，留待后续）。

**范围（续 · 2026-06-25 追加 · 星空）**：复用同一方向口径，给**渊图星空可视化**做「正面星(D>S)」显示改造——派生分类 `persistent_imbalance (D>S)` = persistent_imbalance ∩ direction=多；星空按信号类筛选/检索 persistent_imbalance 时**只高亮正面星（D>S/direction=多）**，负面星（S>D/direction=空，如光伏玻璃过剩）不高亮。**纯星空 render 层改造**：persistent_imbalance canon tag、共享数据 signal_type、日报对「持续失衡」的渲染一律不动——已核实改本体会波及日报（持续失衡标签 41 处 + `yuantu_client.SIGNAL_CATS` 校验），故走 Doctor 指定 fallback：单独划出 D>S、只改星空显示。

**Doctor 原始指令**（逐字引用）：
> "这样修：1、给信号补一个 `direction`（多/空）字段，对应的是"产业信号：买入"和"产业信号：卖出"，日报中的"产业信号观察逻辑"对前者开始追踪（超额价格信号没满足时也显示），对后者提示风险。如果是先有产业逻辑买入信号，转产业逻辑卖出信号，就在转卖出信号时提示风险，并在"-5%绝对回撤"后，停止跟踪。如果一开始就是卖出信号，直接提示风险，可以不追踪。"

**Doctor 追加指令（2026-06-25 · 星空）**（逐字引用）：
> "还有个需求：改一下渊图星空可视化的persistent_imbalance逻辑，把它变成persistent_imbalance (D>S)，即只统计多方的不平衡，包括检索也是只高亮"正面星"。如果影响日报产出，则不修改persistent_imbalance，而单独划出一个persistent_imbalance (D>S)，并修改渊图星空显示就行"

**对齐结论摘要**（2026-06-25 两轮 AskUserQuestion + 收口确认）：
- **核心需求**：信号加方向，日报兑现卡按方向分治，根治利空被当买点、噪声反抽误触发超额追踪。
- **direction 来源（2026-06-25 执行中 Doctor 复核纠偏 · 定稿）**：原拟「KG trend+category 映射」**实测两头误判**——把「供给约束/短缺=利好(多)」（如 DRAM 产能扩张约束，实际跑出 +36.6% 超额）误判成空，把成本通胀两面信号也误判成空。**改「规则出候选 + 逐条核 KG 描述定案」**：入库 direction 以 **CURATED_SHORT 核定空头清单**（按 signal_node）为准，仅明确「供给过剩 / 下游需求被压制」为空；成本通胀类看**受益标的**（上游/可提价转嫁＝提价胜＝多）。Doctor 2026-06-25 定案空头 = `concept_SolarGlassOversupply`(光伏玻璃过剩) + `concept_ConsumerElectronicsMemoryHeadwind2026`(存储压制消费电子) **共 2 条**；auto 关键词规则降级为只对清单外新信号生成候选打日志、不入库。
- **回填范围**：**仅 yuantu_buy_signals 全量回填**；industry_signals 本轮不动（无 signal_node→KG，无真实方向源，不猜）。
- **转卖出识别**：KG 同节点 trend 由 ↑系翻为 ↓系（且 category 转问题）→ 该链 direction 由多改空，引擎记 `direction_flip_date`。
- **−5% 停跟口径**：买入转卖出后，自买入以来 `excess_peak − excess_cum ≥ 5pp`（复用现有 closed 绝对回撤口径）触发**停跟**。
- **状态机三态**：①纯买入→正向追踪，超额未触发也显示「跟踪中·未进入趋势」；②纯卖出→直接风险提示、不进正向追踪台账、可不追踪；③买入转卖出→转换点风险提示 + peak−cum≥5pp 停跟。
- **验收锚**：`concept_SolarGlassOversupply` 经改后 direction=空，从兑现卡正向追踪/「进入趋势 N 天」移出，改风险提示，不再显示噪声触发超额。
- **星空决策（2026-06-25 追加）**：① 已核实「改 persistent_imbalance 本体会影响日报」（日报渲染持续失衡 41 处 + `yuantu_client.SIGNAL_CATS` 校验）→ 取 Doctor fallback：不动本体、单独派生 `persistent_imbalance (D>S)`、只改星空；② 正面星(D>S) 口径**复用 direction**（KG trend+category），全局一处定、不另立口径；③ 本星空改造**并入本 PRD**。

**任务规模估算**：
- 预计涉及文件数：4–5（recap.db schema + 回填脚本；`tools/closure_engine.py`；`tools/gen_daily_report.py`；星空 render `Projects/星空/render-archive/yuantu-starry-skies-v3-full.html` 及/或其数据/构建层）
- 预计耗时：约 3–5 小时（含回填校验、三类呈现样本核对、星空正面星筛选验证）
- 涉及项目：烛照九阴 + 星空

---

## §二 · 交付标准（Acceptance Criteria）

> `[ ]` 默认未开始；CC 执行时改 `[?]`+证据 / `[!]`+原因 / `[~]`+待判断点；`[✓]` 仅 Doctor 打。

### A. 文件层面

- [ ] `yuantu_buy_signals` 新增三列：`direction` TEXT、`direction_src` TEXT、`direction_flip_date` TEXT
  - 验证：`PRAGMA table_info(yuantu_buy_signals)` 含上述三列名
  - 证据栏（CC 填）：
- [ ] direction 全量回填，无空值
  - 验证：`SELECT COUNT(*) FROM yuantu_buy_signals WHERE direction IS NULL OR direction=''` = 0
  - 证据栏（CC 填）：
- [ ] 回填脚本已落于 `~/Documents/Claude/Projects/Financial/烛照九阴/tools/`（新建或集成进既有，文件可 `ls` 见）
  - 证据栏（CC 填）：

### B. 一致性层面

- [ ] direction 取值域 ⊆ {多, 空}（仅这两值，无第三态/脏值）
  - 验证：`SELECT DISTINCT direction FROM yuantu_buy_signals` 仅返回 多 / 空
  - 证据栏（CC 填）：
- [ ] 每条 direction 可追溯 KG 来源（`direction_src` 非空，记 trend+category）
  - 验证：`SELECT COUNT(*) FROM yuantu_buy_signals WHERE direction_src IS NULL OR direction_src=''` = 0
  - 证据栏（CC 填）：
- [ ] 映射口径与对齐结论一致：trend∈{↓↓,↓}且category=问题 的节点 direction=空，其余=多
  - 验证：抽样比对 ≥5 个 KG 节点的 (trend,category) 与入库 direction 一致；含 concept_SolarGlassOversupply=空
  - 证据栏（CC 填）：

### C. 功能层面

- [ ] `tools/closure_engine.py --apply` 跑通（走 /tmp 副本往返），且对 direction=空 的纯卖出信号**不写** date_realized/不判进入趋势
  - 验证：脚本退出码 0；`SELECT COUNT(*) FROM yuantu_buy_signals WHERE direction='空' AND direction_flip_date IS NULL AND date_realized!=''` = 0
  - 证据栏（CC 填）：
- [ ] `tools/gen_daily_report.py` 跑通生成日报，三类呈现各有样本
  - 验证：报告 HTML 中——买入未触发者含「跟踪中·未进入趋势」；卖出信号含风险提示文案；买入转卖出含「风险提示」+停跟标注
  - 证据栏（CC 填）：

### D. 自审层面

- [ ] G-X1 self-audit 段已写（本任务由 Doctor 监督下推进，非自主，但记一段反偏置自审）
  - 证据栏：
- [ ] 派独立审查子 agent 对照本 PRD 逐条复核（Step 7.5 闭环）
  - 证据栏：

### E. 沟通层面

- [ ] /save 已触发 + 落 `~/Documents/Claude/brain/agents/烛阴/logs/`
  - 证据栏：
- [ ] recap.db schema 改动 + 代码改动的 git commit 命令已贴给 Doctor（CC 不在 sandbox 跑 git，G-X2）
  - 证据栏：
- [ ] Artifact `zhuzhao-jiuyin-daily` 同步新报（若 Doctor 批准重渲）
  - 证据栏：

### F. 任务专属

- [ ] closure_engine.py 代码层有 direction 分支：空头不按多头超额为正判进入趋势
  - 验证：`Grep "direction" tools/closure_engine.py` > 0 matches 且含空头分支逻辑
  - 证据栏（CC 填）：
- [ ] 买入转卖出状态机：检 KG 同节点 trend 翻向→direction 由多改空→记 `direction_flip_date`，且 peak−cum≥5pp 触发停跟（进 dormant/停跟态）
  - 验证：构造或命中 ≥1 条 flip 信号，`direction_flip_date` 非空且停跟逻辑生效
  - 证据栏（CC 填）：
- [ ] **验收锚**：concept_SolarGlassOversupply（光伏玻璃供给过剩）direction=空，日报中**不在**兑现卡正向追踪/「进入趋势 N 天」，**出现在**风险提示区
  - 验证：`Grep "光伏玻璃供给过剩.*进入趋势：[0-9]" 报告` = 0 matches；且该链出现在风险提示区块
  - 证据栏（CC 填）：

#### F-星空（2026-06-25 追加）

- [ ] 星空 render 层有派生分类 `persistent_imbalance (D>S)` = persistent_imbalance ∩ direction=多（trend+category 口径同 direction）
  - 验证：星空 render HTML 含 D>S 派生标识（`Grep` 新标识 > 0）；节点带派生 direction 属性
  - 证据栏（CC 填）：
- [ ] 星空筛选/检索 persistent_imbalance 时只高亮正面星（direction=多）；负面星不入高亮集
  - 验证：以 persistent_imbalance 筛选，高亮集 ∩ {direction=空 节点} = ∅；含 concept_SolarGlassOversupply 不被高亮
  - 证据栏（CC 填）：
- [ ] **回归锚**：persistent_imbalance canon tag 与日报「持续失衡」不变
  - 验证：改后重渲日报 `Grep "持续失衡" 报告` 计数 = 改前（41）；共享数据 signal_type 语义未改
  - 证据栏（CC 填）：

---

## §三 · 非交付项（范围排除）

- 不包含：industry_signals 加 direction（无 KG 节点链接、无真实方向源，留待后续另定来源）
- 不包含：改 closure 多头超额主口径（Y_STREAK=3 / X_PEAK=5% / DD_ABS=5pp / RELIGHT 一律不动）
- 不包含：卖出信号的「负超额兑现度」量化打分（本轮卖出只提示风险，不算兑现分）
- 不包含：动 stock_daily 等句芒维护的表，或四张烛阴行情表 schema
- 不包含：在 sandbox 跑 git 写命令（构造命令贴 Doctor 终端）
- 不包含：KG 节点本身的方向标注回写（KG 只读外部源，不改）
- 不包含：改 persistent_imbalance canon tag / 共享数据 signal_type 语义（走 fallback，仅星空 render 层派生 D>S）
- 不包含：改日报对 persistent_imbalance/「持续失衡」的渲染（日报回归不变，标签计数守恒）
- 不包含：破坏星空现有视觉配方（守星空 GOTCHAS G-02 bloom/halo 平衡、G-04 position:fixed 定位）

---

## §四 · 状态

- [x] 进行中（立 PRD · 时间：2026-06-25）
- [x] 待 Doctor 验收（P1-P4 执行完毕 + 独立审查 7 条全 PASS · 时间：2026-06-25）
- [x] 已交付（Doctor 2026-06-25「都确定」口头确认全部交付标准 · 验收依据＝独立审查 7 条全 PASS + §五证据）
- [ ] 已取消（Doctor 显式取消 · 时间：____ · 原因：____）

**关闭路径**：全 ✓ 关闭 / Doctor 显式取消关闭；禁 CC 自动关闭。

---

## §五 · 变更记录

- 2026-06-25 CC（九儿）：立 PRD · 含 16 条交付标准（任务专属/功能/一致性/文件 11 条 + 自审/沟通闭环 5 条）· 起草稿待 Doctor 审/改/批 · 未开工、未打 ✓
- 2026-06-25 CC（九儿）：按 Doctor 星空追加需求扩 PRD · +3 条星空交付项（D>S 派生 + 只高亮正面星 + 日报回归锚）· +3 条星空非交付项 · 口径与 direction 同源一处定 · 共 19 条交付标准 · 仍待审/改/批、未开工
- 2026-06-25 CC（九儿）：Doctor「开工」→ 执行 P1-P4。**执行中 Doctor 纠偏口径**：原 trend+category 机械规则两头误判，改「核定清单制」，定案空头仅 id80/id96 两条（id69 DRAM 供给约束改判多·实测+36.6%）。已重跑 backfill→closure→日报，并撤星空对 DRAM 的 _neg 排除（星空当前 PI(D>S)=55、0 真负面）。
- 2026-06-25 CC（九儿）：**独立审查子 agent（干净上下文）对照 §二 逐条复核 → 7 条核心全 PASS、无 FAIL**（A schema / B 一致性+口径 / C closure / C 日报回归锚 持续失衡=41·卖出=2·验收锚 光伏玻璃移出正向追踪入风险块停跟 / F 星空 PI=55·_neg=0·DRAM 解禁·标签 D>S / 非交付项 KG 只读未污染语义）。§四 转「待 Doctor 验收」。**CC 全程未打 ✓**，✓ 留 Doctor 终审。旁注：KG 主库今日 mtime 变动属独立图谱维护流程、非本任务（本任务对 KG 只读），请 Doctor 顺手确认。

---

## v 历史

- v1.0（2026-06-25）：初版 · 九儿起草 · 经两轮 AskUserQuestion 对齐（direction 来源=KG trend+category／回填仅 yuantu／转卖出=KG trend 翻向驱动／−5%=peak−cum≥5pp／industry_signals 本轮不动）
