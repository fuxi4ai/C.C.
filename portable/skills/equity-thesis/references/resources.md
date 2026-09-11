# 本地资源与只读合同

这些绝对路径是 2026-09-10 本轮实读确认的发现入口；每次使用重新确认当前文件和身份。缺失时定向搜索现行 README/canonical，不静默改读历史副本。无需全量读取所有资源；先按公司与机制检索。所有 CC 路径在本 skill 内只读。

## 渊图与案例方法

根：`/Users/lunarabbit/Documents/Database/行业研究/`

- 当前结构：`CLAUDE.md`、`渊图_GOTCHAS.md`、`rules/confidence_levels.md`。历史 `docs/渊图_索引.md` 只用于发现，不能视为当前状态。
- 唯一图谱：`mapping/行业知识图谱_完整数据库.json`。直接只读解析 JSON，按 id/name/aliases/stock_code 找节点及相关边，回读 description/properties/evidence/data_sources/_meta/updated_at。不要导入 `kb.py`，它导入时建目录且可能回退历史图谱。
- `wiki/` 是派生导航；核有效节点和 `mapping/_tombstones/` 的合并/删除记录，再回证据。图谱结构合法不证明事实正确，字段更新时间不证明数据期间新鲜。
- 方法案例：`raw/核实/2026-08-22-曦智光跃验证与订单核实札记.md`、`2026-08-22-华为OCS链核实札记.md`、`2026-08-22-德科立OCS谷歌300台专项核查札记.md`、`2026-08-26-OCS框架层图谱补丁札记.md`、`2026-09-01-盛科51.2T与超节点交换芯片独立核实札记.md`。后四个文件与首个同目录。
- 案例主节点：`company_Lightelligence`、`product_LightSphereX`、`company_Centec`、`product_Shengke51p2TSwitchChip`；只作为搜索键，先确认仍有效。曦智 wiki 曾滞后于主图，旧盛科产品 ID 已合并；盛科部分数值字段 bn 与正文亿元存在待核冲突，不能自动换算。
- CC 历史：`/Users/lunarabbit/Documents/AI4ME/龙鱼五力-outputs/曦智科技-产业地位深挖-2026-08-22.md`，以及 `/Users/lunarabbit/Documents/Claude/brain/logs/2026-08/2026-08-22-曦智科技深挖与龙鱼三标的跑分.md`。用来理解旧判断与纠偏，不传承旧价格/市占/目标价。
- Codex 已完成案例：`/Users/lunarabbit/Documents/Codex/2026-09-10/曦智科技近一周研究/曦智科技近一周投资研究.md`。结论只对当时证据负责，不是新研究的标准答案。

## 风险日报与风险卡

- 概览：`/Users/lunarabbit/Documents/Claude/Projects/风险日报/data/risk_snapshot.json`；方法/GOTCHAS 在同项目。generated 是构建时间，atoms/molecules/compounds/edge_evidence 各字段仍须核原始观察时点。
- 卡片真源：上述渊图根 `watch/current.json` → 读取 revision_id → `watch/revisions/<revision_id>.json`。revision 是含 pack/revision_id/sha256 的 wrapper。按 `watch/alarm_store.py` 的现行合同校验：`sha256((json.dumps(pack, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False) + '\n').encode('utf-8'))` 等于 wrapper 和指针的 sha256；revision_id 等于 `r-` 加 digest 前 24 位。**不是 wrapper 原文件的字节 hash。** 路径须在 revisions 内；schema/状态派生另行按当前合同校验，hash 不证明金融事实。不要硬编码当前 revision ID，不回退冻结的 `watchlist.jsonl`。快照 ai_panel 是简化派生，缺失证据不能据此补齐。
- 保留 pack schema_version/as_of_utc 与卡片 id/assets/event_group_id、scenario_cn/assessment_cn/invalidation_cn、evidence_status/pricing_status/scenario_status、last_verified_at_utc、signals[].test/source_ids/observed_at_utc、trigger_all/warming_any。回到引用 source 的 locator/日期和指标 period/unit/basis/calculation。
- `legacy` 强断言不晋升当前事实；verified/signal_observed 也不意味着已定价或未计价。价格状态 unknown 必须保留。风险叠加是风险观察层，不直接生成 alpha、仓位或概率。

## EAL 宏观事件与估值

- 方法入口：`/Users/lunarabbit/Documents/Claude/Projects/Financial/宏观研究体系/EAL/PRODUCT.md` 和 `backtest/VALUATION_WORKFLOW.md`。框架 draft/staging/预注册先验不冒充已验定律。
- 主库：`/Users/lunarabbit/Documents/Database/宏观研究体系/EAL/attribution.db`，SQLite 必须 `file:...?...mode=ro` 连接并设 `PRAGMA query_only=ON`；不得复制生产库后声称当前消费，不运行构建器。
- 先读取 `v_event_workbench_latest` 的 run_id/as_of_utc/valuation_run_id/pack_json，再按**该 valuation_run_id**读取 valuation_runs。不要拼两个独立 latest。先查询 schema，仅取本次有关事件/机制；不存在 observation 就明说未观察，日常价格刷新不代表研究包刷新。
- 按需读取 `v_macro_event_facts`、`v_macro_transmission_evidence`、`v_ai_financing_latest`。事件 clock/hypotheses/checkpoints，价格 quote_at/data_date/horizon/inputs/assumptions，预期 kind/period/unit/currency/basis/condition/source_ids 均保留原意。
- 历史风险回测 `/Users/lunarabbit/Documents/Claude/Projects/Financial/剑酒青丘/回测报告/2026-07-27_风险日报_风险项综合回测_R1.md` 仅作已发表历史报告；本轮没有重跑就不能说重新验证其结论。

## 龙鱼六维：互补接口

根：`/Users/lunarabbit/Documents/Database/龙鱼-标的分析库/`，先查 README.md/SCHEMA.md，records 是权威记录，HTML 是派生。用 `rg --files records` 定位并核 ts_code，不根据简称模糊匹配直接选股；HK 前导零应按库身份保留。

`scripts/read_longyu.py` 输出每个 scorer 的最新可用记录与元数据。analyses 包含 analysis_date/source/scorer/six_dim/total/engine_facts/_meta；latest 只是日期指针，不能代表唯一 scorer。评分是模型研究和部分财务锚点的结构化结果。engine_facts 为空时不能宣称当轮跑过财务引擎。不同 scorer 各自展示，不平均、不覆写。

| 六维（现行字段/上限） | 定性研究补充 |
|---|---|
| 政策与监管(5) | 政策实际覆盖、实施条件、现金流传导 |
| 技术变革与供需(35) | 行业需求与公司兑现、路线与供给约束证据 |
| 竞争格局与产业链(25) | 进入路径、客户选型、议价和价值分配 |
| 新赛道与未来预期(15) | 期权里程碑、概率边界、融资与兑现时间 |
| 估值与安全边际(15) | 现价隐含假设、同口径场景与催化条件 |
| 财务健康与风险(5) | 现金、债务、回款、会计口径与融资链 |

两期变动仅在相同且已知 scorer、相同且已知方法口径、完整评分、不同可比日期下解读；口径改变不等于基本面改变。经营、估值、锚点分开解释，单条事实不要各维重复惩罚。现行方法在渊图 `consumers/龙鱼五力/双scorer交叉打分制度.md` 与实际评分代码/记录 _meta；旧 v4 方案不保证对应当前 v4 口径。该 skill 不重打分，发现确定错误只报告位置与证据。

合法 engine-only 记录可以只有财务维度；null 保留为未知，partial 不生成总分或趋势。无分析占位明确 unavailable；不能为了可读而给缺项补零。分析日期与打分日期按 schema 必须一致，冲突拒绝。仅有用户给出的汇总分时标为“摘录、原始记录未核”，仍可解释方法/时点差异，不宣称脚本通过或六维已复核。`--as-of` 仅过滤记录日期，缺当时冻结快照/入库时钟就不具备历史回测的时点已知资格。

## 经验召回

入口：`/Users/lunarabbit/Documents/Codex/Codex Brain/permanent/经验索引.md`，按项目/对象/操作/失败检索再读命中正文。初次提炼采用：`VV-LESSON-EE3912E119`（原始出处）、`VV-LESSON-702EFEC9B0`（机制与未知）、`VV-LESSON-6AB6304A11`（字段时效）、`VV-LESSON-4D09996675`（确定性校验）、`VV-LESSON-2A94F74F99`（单向消费回读）。使用时先确认正文仍适用，不把本清单当自动采用证明。
