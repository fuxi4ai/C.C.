---
title: 会话日志 2026-11-08 — RiskDaily 事件层 v4 与 AI 评分口径
tags: [log, 风险日报]
created: 2026-11-08
updated: 2026-11-10
status: active
type: log
project: 风险日报
---

# 会话日志 — 2026-11-08（承 [[2026-11-07-RiskDaily重推与叙事消化度]]，同一会话跨 UTC 日）

**项目**：风险日报
**主题**：叙事消化度 v2 → 事件拆分设计（事实状态×证据等级）→ 事件层 v4 上线 → AI 评分口径三连修（市场数据类 · 代理阻断 · 多次采样）→ 融资维传导通道分档 → 班正文 v4 合同写入
**时长**：约 2026-11-07 17:40Z – 2026-11-08 13:40Z（中间有离场）

---

## 完成的工作

### A. 叙事消化度 v2（11-07 晚）
- Doctor 三轮纠正：「砸得动」是未来式→描述性 → 「利空日跌不跌≠消化充分（突发利空当天下跌是正常消化）」→ 「看**跌的程度**」。授权检索主流机构评论补分母语料。
- 区块改三段：① 已知利空的下跌消化度（SOX 峰→谷 −38.4%、相对 SPY −36.9pp；三把尺完成度：估值回归 133%/75% · MS 目标媒体折算 9,500 → 110%、按 10-28 收盘自算区间 120–137% · 历史回撤 103%/256%，不合成状态词）② 未来利空提示（不计入消化度）③ 尚未计入项（盈利端未下修、融资端随跌加重）。手工参照源 `data/digestion_reference.json` + 语料札记 `docs/2026-11-07-机构参照-半导体回撤消化度语料.md`。
- 综合温度改双轨（均值 + 最高分子/最高原子），Doctor 裁 C。
- 独立审查两轮（D 区 PASS_WITH_LIMITS；改正 V8 札记缺 MS 15GW 出处、MS 9,500 折算与 10-28 收盘不自洽 → 并列区间行）。

### B. 事件拆分设计（Doctor 命题 developing 三分法 → CC 反思「新增维度」→ Doctor 同意单一切分标准）
- 设计稿 `风险日报/architecture/事件拆分设计提案-事实状态×证据等级.md`（approved）：两轴＝`fact_status`（occurred/forecast/contingent）× `lifecycle`（证据是否达标）；可引用＝occurred|forecast ∧ confirmed；拆分检查单（单事实·四句探针·部分发生拆两条·传闻·family·contingent 四字段）。
- Phase 1（不改 schema）：events 35→40（中期选举拆四、Meta/光模块拆二、预期类改标）；复核包加 review_note。
- **三条术语/口径裁定**：「预期」专指市场预期，机构数字称「测算」（forecast），未发生不称预期；政策阶梯（提案阶段 occurred 计入维度分、不撑 critical，≥ adopted 可撑）；信息事件（白名单媒体报道＝occurred·report，可进维度分不撑 critical）+ 市场隐含概率观测行。

### C. 事件层 v4（Phase 2 · PRD `logs/checkpoints/2026-11-08_事件层v4事实状态_PRD.md`）
- schema 3→4、`_v4_event_error` 字段校验、`citable/critical_eligible/contingent_expiry`；迁移脚本 `ops/migrate_events_v4.py`（occurred 32/forecast 6/contingent 2，幂等，v4 文件只校验不覆写）；复核包剔 contingent 单列 future_watchlist；维度卡「机构测算」；未来利空提示显触发条件/落入维度/到期处置；合同 `docs/事件登记合同-v4.md`。
- 独立审查 PASS_WITH_LIMITS：白名单子串匹配实错（microsoft.com 命中 ft.com）→ 改 hostname 后缀；F9 待归档、review_note 矛盾等修正。

### D. AI 评分口径（Doctor 质疑 65.2 偏低 → 三处修）
- v4 首跑 AI 76（红·融资 critical）→ 65.2：CDS/债券收益率被归为报道型不能撑 critical。**归类错误**：市场数据转述≠传闻报道 → 新增 `market_data` 证据类（可撑 critical），Doctor 批。
- 交付 36→63 系「已发生事件（选举结果）替未发生政策（法案）作代理」软性泄漏 → **代理阻断**规则（同 family 有未解除 contingent 且 lands_in 含本维度 → 该族已发生事件不得作本维度压力依据）；模型无视提示照引 → 被阻断事件移出可引用 events。
- 同版本内包含旧评估 + ±15 限幅 → 模型照抄旧分 → 升 v21；5 次独立评分 funding 68–78、1/5 判 critical，总分双峰（≈60 或 78）→ **多次采样取共识**（Doctor 批）：N=3，多数票定 critical，取最接近中位的整份样本；配套三处：去旧评估锚（日间稳定改由 bounded_check 校验）、input_template + 嵌套平铺修复、篇幅上限（防 8000 token 截断）。
- 机构观点检索（CNN/Morningstar/Fitch 主流：局部承压未系统性；CNBC/Moody's/Goldman 偏紧：压力在外溢）→ Doctor 裁**分档**：违约/重组、头部实验室融资失败＝充分条件（规则强制融资 critical·下限 75·面板注「规则触发」）；投资级恶化＝必要条件。v22。Meta 展望调负标 ig_deterioration。
- 当前读数：AI **59.0**（funding 74 非 critical；3 样本 1 被剔、余 2 个 80-critical/74 → 不过半）。测试 test_narrative_score 113/0、test_narrative_digestion 15 OK。

### E. 班正文
- Doctor「批准」→ 镜像 `references/scheduled-live-mirror/live/refresh-risk-daily/SKILL.md` 步骤 2 插入 v4 登记合同两条（sha `0b52da9d`→`f761c906`，备份在旁）。

### F. 操作差错
- 第十二版推送时 update_artifact 与 SendUserFile 并行发出，误用上一版 file_uuid + 占位说明推了一次旧版，随即重推覆盖。

## 做出的决策

| 决策 | 原因 | 影响 |
|------|------|------|
| 消化度看「跌的程度÷机构参照」，三把尺不合成状态词 | Doctor：跌不跌/跌几天不等于消化；未来式状态词等于方向判断 | 区块三段；手工参照源 |
| 事件两轴 fact_status × lifecycle；「预期」专指市场预期 | developing 扛两件事致校验误拒；词义混淆市场定价与机构测算 | schema v4；合同文档 |
| 提案阶段计入维度分不撑 critical；报道型同 | 市场最敏感窗口不应滞后；critical 杠杆最大须硬证据 | policy_stage / evidence_basis |
| market_data 可撑 critical | CDS/债券价格是可观测数据，非传闻 | 融资维证据重分类 |
| 代理阻断 | 防已发生事件替未发生政策计分 | 交付 63→45 |
| 多次采样取共识（N=3） | 单样本在门槛附近双峰摆动 | 调用 ×3；去旧评估锚 |
| 传导通道分档：硬通道充分、投资级恶化必要 | 机构主流认为边际借款人困境属局部；真正断裂须确定翻红 | v22；规则触发 critical |

## 遗留问题 / 待办（已同步 TODO.md）
- [ ] 17:05Z 自然班首跑核：事件自检、REVIEW_ACCEPTED、3 样本分布、push 待补推
- [ ] Phase 2 PRD 终审（F3/F5/F12/F13 为 [~]；F14–F17 新增；修正部分未二次独立审查）
- [ ] 平局规则：2 有效样本 1:1 时现按「非 critical」，是否改为补一次采样（Doctor 未裁）
- [ ] 投资级恶化的「利差显著走阔」阈值未定（Oracle 发债利差是否标通道待定）
- [ ] CoreWeave 11-10 财报（再融资/现金回收）· Oracle 利差/CDS 为近期观察点
- [ ] `digestion_reference.json` ③ 文案仍写「对应 funding 维 critical」，与现状不符，待更新
- [ ] 两仓 git 提交（命令见本次 /save 回报）

## 追记（2026-11-08 晚 · 首次 /save 之后）
- **投资级恶化阈值（Doctor 裁）**：检索机构观点——无单一「显著走阔」数字，常用三类参照：对比评级同档（S&P 市场情报：Oracle 5 年 CDS 约 300bp 相当于 BB/B）、自身历史（2008 峰值 198bp · 大摩目标 150/200bp）、评级基本面触发（S&P 杠杆 > 4.5 倍等）。现状 11-02 新发债利差 240–335bp，较 2 月宽 145–175bp。Doctor 选**相对指数口径**：10 年期利差 ≥ BBB 指数 2 倍，或 3 个月内相对指数多走阔 ≥ 100bp，持续 5 个交易日。已记决策记录与 TODO，**未实施**（需接 BBB 指数数据、改合同 v4 与 narrative_score，待 Doctor 说「实施」）。
- **口径澄清**：融资维 critical 的必要条件是「依据中至少一条带传导通道」，投资级恶化只是三种通道之一；硬通道（违约/重组、头部实验室融资失败）满足即规则强制 critical（下限 75），不需投资级恶化。已对照代码现读确认。
- 未核：BBB 指数 +95bp 系 TwentyFour 写 2 月发债时的数，现值未取；10-20 之后 Oracle CDS 未取；阈值未回测。

## 相关笔记
- [[2026-11-07-RiskDaily重推与叙事消化度]] · [[2026-11-07_叙事消化度_PRD]] · [[2026-11-08_事件层v4事实状态_PRD]]
- [[风险日报/architecture/事件拆分设计提案-事实状态×证据等级]] · [[风险日报/architecture/决策记录]] · [[风险日报/GOTCHAS]]
