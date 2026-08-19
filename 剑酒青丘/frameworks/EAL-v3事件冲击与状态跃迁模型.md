---
title: "EAL v3 方法合同 · 事件冲击与状态跃迁"
created: 2026-08-19
updated: 2026-08-19
contract_version: "3.0.0-shadow.7"
status: draft
document_role: codex_staging_handoff
project: 剑酒青丘 / Event Attribution Ledger
canonical_status: staging_only
canonical_system: "/Users/lunarabbit/Documents/Claude/brain"
proposed_canonical_target: "/Users/lunarabbit/Documents/Claude/brain/剑酒青丘/frameworks/EAL-v3事件冲击与状态跃迁模型.md"
implementation_authorization: "not_granted_by_this_document"
staging_implementation_authorization: "Doctor 2026-08-19 明确批准方案 2；仅限本 Codex Review Runs 升级包"
---

# EAL v3 方法合同：事件冲击与状态跃迁

Package / method-contract version: `3.0.0-shadow.7`（shadow.6 终审 BLOCK 后修复候选）。
SQL persistence contract: `eal-v3-additive-schema-v3.0.0-shadow.7`；exact manifest：`schemas/eal_v3-sql-schema-v3.2.json`；SQL SHA-256：`898fda27b3fbc6b25f3fde4211bc19bd22423fe489badaf63b5bbad650644013`；schema fingerprint：`205af71a3e266f93460d3b6da8796c2e790497a23f1a4016e2c11c37d2e801e5`；inventory：16 tables / 12 explicit indexes（37 indexes including 25 autoindexes）/ 54 triggers / 107 namespace objects / 15 mapped data tables。
当前实施证据：SQL 独立只读数据合同复核 PASS；runtime 普通/`-O` 各 35/35，migration 各 19/19，legacy migration 各 7/7；具名源的只读 backup→fresh candidate apply/verify-only replay 亦通过；32-payload manifest/verifier 与 archive/sidecar→唯一空目录解包机械终验均通过。经终验的 prestatus 归档已封存、不交付；最后文档字节冻结后由主线按同一机械链重生，最终归档只以外置同名 sidecar 标识。真实 frozen registry 仍未形成；这些证据不是独立功能验收签字。

> **真源声明**：本文件是 Codex Review Runs 中交给 CC 的 staging 规格，不是 Brain canonical。CC 只能在另获实施授权后，把经现状核对和冲突处理后的合同单向落入 Brain；在那之前，Brain 现行事件归因台账、GOTCHAS、PRD 合同和复现材料优先。本文件不得被生产脚本、Gateway 或正式 artifact 直接读取。

> **方法边界**：当前 staging 实现的主结果是无控制 `DAILY_SHADOW`：事件或状态跃迁簇的观察复利收益减同长度 compound daily baseline。它是描述性 shadow，不是原先 `ΣAR` 定义的 CAR，也不是 local projection；正式 CAR/local projection 是后续独立估计量。v3 不承诺为每个交易日找齐原因，不把同日共变系数当因果权重，也不要求不同原因加总为 100%。

## 1. 合同目标

本合同把以下判断变成机器可执行约束：

1. 何谓事件、状态、transition 和重叠簇；
2. 事件首次公开时刻如何映射到交易窗口；
3. 分类怎样与事件后价格彻底隔离；
4. 当前 daily shadow 为什么只允许空控制集，以及未来前置控制须怎样另行开放；
5. “冲击”“杀伤烈度”“缓和反弹”“权重”分别输出什么；
6. 多小的样本只能做个案或探索，多大的样本才允许提升措辞；
7. 因果识别、来源可信度和统计精度怎样分轴表达；
8. v2.3、机械层、数据库、Brain 和 artifact 怎样兼容而不形成双真源。

## 2. 估计对象与结果身份

### 2.1 当前 shadow 与后续估计量必须分开

| estimand_id | 名称 | 回答的问题 | 允许的主要输入 | 禁止的宣称 |
|---|---|---|---|---|
| `DAILY_SHADOW` | 当前日频 shadow gap | 整个事件簇观察复利收益比同长度日基线高/低多少 | 目标日收益、冻结 daily baseline、事件/簇时钟；controls 必须为空 | 不得称 CAR、local projection 或因果总效应 |
| `TE_EVENT` | 后续事件/簇总效应 | 正式识别设计下事件相对无事件反事实带来多少边际变化 | 后续已验收估计器、事件前信息、价格盲标签 | 当前 shadow 不得复用此身份 |
| `TE_TRANSITION` | 后续状态跃迁总效应 | 正式识别设计下进入、升级、缓和或退出状态后行情怎样变化 | 预注册状态规则、跃迁时钟、后续已验收估计器 | 不得把持续状态水平本身当每日冲击 |
| `XASSET_RESPONSE` | 跨资产响应 | 同一事件窗内不同市场怎样共同响应 | 事件时钟、各资产窗内收益 | 不得与 `TE_EVENT` 机械相加或扣减 |
| `DIRECT_ASSOC` | 直接条件关联 | 控制同日通道变量后剩余关系是什么 | 明示的同日变量与独立规格 | 不得称因果总效应、预测模型或归因账 |

每个结果必须有唯一 `estimand_id`。同一数值不能在不同结果身份之间复制而不留派生关系。当前 `DAILY_SHADOW` 输出不得填充 `TE_EVENT/TE_TRANSITION` 字段；v2.3 的 M4 固定为 `DIRECT_ASSOC` 家族。

### 2.2 主结果不是“逐日百分比解释”

- 有合格事件/transition：当前先报告 `DAILY_SHADOW` 复利 gap、路径、样本门和识别限制；后续正式估计器另报 CAR/local projection。
- 无合格事件：只报告实际收益、冻结 daily baseline 对照、基线偏离、当前状态和“无可识别事件”标志；不得把该 baseline 改称已识别无事件反事实。
- 漏标诊断可以把极端残差送入待研究队列，但不得根据残差自动生成已确认事件。
- 不输出强制 100% 的逐日原因饼图。

## 3. 数据分层与真源

### 3.1 真源分工

| 层 | 真源职责 | 不得承担的职责 |
|---|---|---|
| Brain | 方法、口径、治理、人工裁定和状态说明 | 不作为大规模逐行市场数据存储 |
| 结构化数据库/冻结面板 | 事件事实键、时钟、状态、市场观测、运行输入 | 不独立改写 Brain 方法合同 |
| 代码与配置 | 确定性变换、估计、校验和审计 | 不把硬编码输出冒充事实真源 |
| artifact | 当前已发布结果的派生展示 | 不成为第三套可手改方法或数据真源 |
| Codex staging | 升级建议、评审和交接 | 不参与生产读取，不覆盖 Brain |

### 3.2 数据域必须物理或逻辑隔离

至少建立以下只增量的 v3 域；实际表名可因仓库约定调整，但职责不可合并：

- `event_facts`
- `event_classifications`
- `event_clocks`
- `state_intervals`
- `state_transitions`
- `window_specs`
- `event_clusters`
- `market_observations`
- `estimation_runs`
- `impact_results`
- `run_exclusions`
- `run_audit`

分类器运行时的数据视图不得包含事件后市场观测列。当前 daily shadow 只接受空 controls；后续总效应基线构造器若开放前置控制，只能接收通过 `available_at < treatment_time` 审计的字段。

### 3.3 本升级包的并行实现兼容规则

本目录可能由多个并行工作者同时补充迁移 SQL、review-queue schema、运行时代码和测试。它们不是因为位于同一目录就自动成为同一份合同。集成时必须遵守：

1. 本节列出的表名是**逻辑域**；物理表可以采用 `eal_v3_*` 前缀或把相邻字段合表，但须提供逐字段 mapping，并证明职责隔离、约束和追溯链没有丢失。
2. legacy migration 的 `needs_coding` JSONL 只是待人工核证的 intake；它不能被运行时估计器当作 `frozen` event registry。intake schema 与 runtime registry schema 必须使用不同 `schema_version/record_kind`，并由显式、受测的审核转换连接。
3. 事件层只能使用五个原子族 `macro / monetary_policy / geopolitical / earnings / other`；`mixed` 只能由 cluster 层派生。若并行 SQL 或旧 schema 把 `mixed` 放在事件枚举中，装载前必须修正或通过单向迁移映射，不能沿用成第二口径。
4. transition 的同义枚举（例如 `enter/entry`、`escalate/escalation`、`deescalate/easing`）必须在 canonical 化时选定一套，其他写法只作为入口 alias；持久化结果不得并存同义值。
5. 严重度量表必须由 `severity_rubric_version` 定义有限范围与事实锚点。若候选实现的范围不同，须迁移或版本隔离，禁止仅按比例换算后声称同口径。
6. runtime 合同与 SQL 合同之间必须有版本化 adapter：输入固定为 `eal-event-registry-v3.2`，配置固定为 `eal-model-contract-v3.2`，结果 JSON 固定为 `eal-event-effects-v3.2`。runtime registry/result JSON 均使用 `transition`，SQL event/result row 使用 `transition_type`；adapter 只做这类已登记字段映射，不静默改值、补默认值或丢字段。
7. Draft 2020-12 JSON Schema 是分发的 shape 合同；当前 stdlib runtime 不内置或伪造一个不完整的通用 JSON Schema 引擎。持久测试必须逐字证明 schema `required/properties`、版本化 fact allowlist 与 runtime parser 字段集一致；每行再由 `parse_event` 执行 exact-shape、类型/枚举和跨字段、时间、身份、状态、可报告性 semantic 门。schema/runtime parity 与 semantic/runtime validation 联合构成必经门。落库前记录源/目标 schema fingerprint，落库后回读并证明 runtime→SQL→runtime canonical round-trip 等价。
8. 任何并行实现完成、测试通过或生成文件，都只是 PRD 的执行证据；在字段、枚举和结果身份对齐且经独立验收前，不得标记为 canonical 或 production-ready。

## 4. 输入 schema

以下为逻辑 schema。所有时间戳使用 ISO-8601 并保存 UTC；需要展示时另存 IANA 时区，不以无偏移本地字符串作为真源。分发 JSON Schema 描述结构、类型、枚举和局部条件；当前 stdlib runtime 由持久 parity test 锁定其 shape 字段，再由 parser 执行 identity 重算、时间先后、状态跃迁、日历边界、finality 与跨行唯一性。不得把 schema 文件存在或 parity 通过单独当成逐行 semantic validation。

### 4.1 `event_facts`

| 字段 | 类型 | 必填 | 合同 |
|---|---|---:|---|
| `event_id` | string | 是 | 全局稳定主键；禁止按行号生成 |
| `event_version` | integer | 是 | 从 1 单调递增；事实修订不覆盖旧版 |
| `episode_id` | string | 是 | 同一底层冲击/持续事态的稳定标识；样本独立性去重键之一 |
| `independence_group_id` | string | 是 | 预注册独立组；默认等于 `episode_id`，已知相依 episode 必须共享同一值 |
| `identity_sha256` | lowercase hex64 | 是 | 对版本化 canonical identity material 求 SHA-256；数据库必须 `UNIQUE` |
| `headline` | string | 是 | 中性事实摘要，不含价格结果推断 |
| `fact_text` | string | 是 | 可审计事实描述；不得含由行情反推的标签 |
| `fact_schema_version` | enum | 是 | 与事件族一一对应的版本化 structural-fact schema |
| `fact_payload` | closed object | 是 | 字段集必须与该 `fact_schema_version` exact allowlist 相等，不接受自由文本或额外键 |
| `source_ref` | string | 是 | 可回读来源标识或 URL |
| `source_type` | enum | 是 | `primary_official / primary_party / contemporaneous_wire / secondary / unknown` |
| `source_published_at_raw` | string | 是 | 来源显示的原始时间文本 |
| `source_timezone` | IANA string | 条件 | 原始时间非 UTC 时必填 |
| `first_public_ts_utc` | timestamp | 条件 | 可解析首次公开时刻；不确定时为空并给原因 |
| `timestamp_precision` | enum | 是 | frozen v3.2 只允许 `minute / hour`；日期级/未解记录留 intake |
| `known_at_utc` | timestamp | 是 | 该事实版本最晚何时已可获得 |
| `revision_of_event_id` | string | 否 | 修订或二次发布的父事件 |
| `fact_status` | enum | 是 | `active / corrected / withdrawn / superseded` |
| `ingested_at_utc` | timestamp | 是 | 审计字段，不可作识别时钟 |
| `ingestion_version` | string | 是 | 导入代码/映射版本 |

唯一键为 `(event_id, event_version)`，`identity_sha256` 另设唯一约束。identity material 至少包括稳定来源、首次公开时钟、规范化事实指纹和版本语义，不含数据库 rowid、导入时间或输出顺序。相同 `source_ref + first_public_ts_utc + normalized_fact_fingerprint` 的重复输入必须拒绝或显式归并，不能悄悄生成两个事件。

frozen v3.2 对两类易受市场代码污染的事实包固定 exact 闭集：

- `family=macro` 必须用 `fact_schema_version=eal-facts-macro-v2`，`fact_payload` exact keys 为 `release_code/actual_value/consensus_value/measurement_unit`。`release_code` 只允许 `CORE_CPI_US / CORE_PCE_US / CPI_US / GDP_ADVANCE_US / ISM_MANUFACTURING_US / NONFARM_PAYROLLS_US / PCE_PRICE_INDEX_US / RETAIL_SALES_US / UNEMPLOYMENT_RATE_US`；`measurement_unit` 只允许 `index / percent / count / annualized_percent`。
- `family=earnings` 必须用 `fact_schema_version=eal-facts-earnings-v2`，`fact_payload` exact keys 为 `issuer_code/release_code/actual_value/consensus_value/measurement_unit`。`issuer_code` 当前仅允许 `^CIK-[0-9]{10}$`（不声称支持 LEI）；`release_code` 只允许 `quarterly / annual / guidance`，`measurement_unit` 只允许 `currency / percent / count`。

`SPY`、`SP500` 或任何 target/index ticker 都不是 macro release identity 或 earnings issuer identity，必须以 `EAL_FACT_SCHEMA_INVALID` 同族稳定错误拒绝。

### 4.2 `event_classifications`

| 字段 | 类型 | 必填 | 合同 |
|---|---|---:|---|
| `classification_id` | string | 是 | 稳定主键 |
| `event_id` / `event_version` | key | 是 | 关联已存在的事实版本 |
| `taxonomy_version` | string | 是 | 分类字典版本 |
| `atomic_family` | enum | 是 | `macro / monetary_policy / geopolitical / earnings / other` |
| `subtype` | string | 是 | 版本化词典中的细类 |
| `state_type` | string | 是 | frozen registry 必填；状态不适用时写 canonical sentinel `not_applicable`，不得为空 |
| `expected_direction` | enum | 是 | `negative / neutral / positive / ambiguous`；基于事实和预期，不基于价格 |
| `severity_ordinal` | integer/null | 否 | 仅允许预注册的事实型 0–3 等级；证据不足为空 |
| `expectation_ref` | string/null | 否 | 事件前已发布预期或共识的来源 |
| `expectation_known_at_utc` | timestamp/null | 条件 | 使用预期时必填，且早于事件时点 |
| `classifier_type` | enum | 是 | `rule / model / human_review` |
| `classifier_version` | string | 是 | 代码、规则或提示版本 |
| `classified_at_utc` | timestamp | 是 | 审计字段 |
| `price_blind_attestation` | boolean | 是 | 必须为 true 才可进入 v3 |
| `classification_rationale_ref` | string | 是 | 可回读的非价格证据 |

`mixed` 不是原子事件族，禁止写入 `atomic_family`。只有 cluster 包含两个及以上原子族时，cluster 层才能派生 `mixed`。

frozen runtime registry 必须逐行携带非空 `episode_id`、`independence_group_id`、`state_type`、`state_rule_version` 与唯一 `identity_sha256`。`needs_coding` intake 可以暂空，但在这些字段核证前不得转为 `frozen/reportable`。所有聚合、entry/exit 配对和状态不对称计算必须使用**相同 `state_type + state_rule_version`**，或有 canonical 且可重放的显式兼容映射；`not_applicable` 不能与真实状态类型配对。

### 4.3 `event_clocks`

| 字段 | 类型 | 必填 | 合同 |
|---|---|---:|---|
| `clock_id` | string | 是 | 稳定主键 |
| `event_id` / `event_version` | key | 是 | 引用事实版本 |
| `venue_id` | string | 是 | 目标市场/交易场所 |
| `market_calendar_version` | string | 是 | 日历版本，不得用工作日近似 |
| `source_published_at_raw` | string | 是 | 来源原样时间文本，不以解析后 UTC 覆盖 |
| `source_timezone` | IANA string | 是 | 原文可自带 offset，但本字段必须是可解析 IANA zone |
| `first_public_ts_utc` | timestamp | 是 | frozen v3.2 固定等于 lower bound |
| `first_public_lower_utc` / `first_public_upper_utc` | timestamp | 是 | `minute/hour` 证据的半开包络边界 |
| `session_timezone` | IANA string | 是 | 交易所正式时区 |
| `session_bucket` | enum | 是 | `pre_open / regular / post_close / non_session / unknown` |
| `effective_trade_date` | date/null | 条件 | 由规则派生；不可识别时为空 |
| `clock_quality` | enum | 是 | frozen v3.2 为 `reported_minute / reported_hour`，与 precision 一一对应 |
| `clock_rule_version` | string | 是 | 派生规则版本 |
| `override_flag` | boolean | 是 | 默认 false |
| `override_reason` / `override_ref` | string/null | 条件 | 人工覆盖时必填 |
| `clock_exclusion_code` | string/null | 否 | 无法进入某类窗口的原因 |

frozen v3.2 的 `minute` 必须以整分钟 lower 开始，upper=lower+1 分钟；`hour` 必须以整小时 lower 开始，upper=lower+1 小时。两者均要求 `first_public_ts_utc=lower`，且 raw timestamp 在 IANA zone 下解析后与 lower 一致；DST gap/fold 不可静默选边。日期级/未解时钟不伪造时分秒，留在 intake 或以稳定 exclusion code 排除。UTC lower 早于冻结日历首个 session，或需要“下一交易日”却超过日历末端时，必须 fail-closed，不外推工作日。

### 4.4 `state_intervals` 与 `state_transitions`

`state_intervals`：

| 字段 | 类型 | 必填 | 合同 |
|---|---|---:|---|
| `state_interval_id` | string | 是 | 稳定主键 |
| `state_type` | string | 是 | 如政策限制、冲突强度、风险制度；须有规则版本 |
| `state_level` | string/number | 是 | 有序或数值等级；尺度在规则中定义 |
| `valid_from_utc` | timestamp | 是 | 状态开始生效时点 |
| `valid_to_utc` | timestamp/null | 否 | 开放状态为空 |
| `state_rule_version` | string | 是 | 生成规则版本 |
| `source_ref` | string | 是 | 外部事实或正式裁定来源 |
| `known_at_utc` | timestamp | 是 | 当时可获得时点 |
| `price_blind_attestation` | boolean | 是 | 必须为 true |

`state_transitions`：

| 字段 | 类型 | 必填 | 合同 |
|---|---|---:|---|
| `transition_id` | string | 是 | 稳定主键 |
| `state_type` | string | 是 | 引用状态定义 |
| `from_level` / `to_level` | string/number | 是 | 跃迁前后等级 |
| `transition_type` | enum | 是 | 实体跃迁只允许 `entry / escalation / easing / exit` |
| `effective_ts_utc` | timestamp | 是 | 首次生效或首次公开时点，规则需声明 |
| `event_id` | string/null | 否 | 若由明确事件触发则关联 |
| `transition_rule_version` | string | 是 | 确定性规则版本 |
| `source_ref` | string | 是 | 可回读证据 |

持续状态水平只可作为事件前条件或交互项；`transition` 才能充当离散处理。frozen event 与 runtime result JSON 用 `transition=none` 表示无跃迁，adapter 逐字映射为 SQL event/result row 的 `transition_type=none`；`state_transitions` 实体表不为 `none` 造行。cluster 成员的 transition 不同时可派生 `mixed`，但 `mixed` 同样不是实体跃迁行。不得每天重复创建“仍处于某状态”的伪事件。

### 4.5 `market_observations`

| 字段 | 类型 | 必填 | 合同 |
|---|---|---:|---|
| `series_id` | string | 是 | 目标或参照序列稳定标识 |
| `observation_ts_utc` | timestamp | 是 | 观测时点/区间终点 |
| `frequency` | enum | 是 | `tick / minute / hour / daily` |
| `price_type` | enum | 是 | `trade / mid / close / adjusted_close / total_return_index` |
| `value` | finite number | 是 | 非有限值拒绝 |
| `currency` | string | 条件 | 价格类序列必填 |
| `source_ref` | string | 是 | 数据源与版本 |
| `available_at_utc` | timestamp | 是 | 防前视审计核心字段 |
| `quality_flag` | enum | 是 | `ok / stale / corrected / missing` |

目标收益计算必须声明复权、时区、收盘价、缺失、停牌和货币换算规则。不同 `price_type` 不得在同一运行中静默拼接。每次运行还必须绑定 exact `market_data_snapshot(snapshot_id,database_sha256,source_version,quality_status,observed_at_utc)`；当前 v3.2 强制 `quality_status=sealed_final`、`observed_at_utc=market_data_as_of_utc`，且 `database_sha256` 与实际读取文件逐位一致。当紧凑的日频物理表没有逐行 `available_at_utc` 时，只能用这个封存 snapshot 的 `observed_at_utc` 作为全批次保守可得边界；不得仅因行存在就认定当时已可得。

### 4.6 `window_specs`

| 字段 | 类型 | 必填 | 合同 |
|---|---|---:|---|
| `window_spec_id` | string | 是 | 稳定主键 |
| `frequency` | enum | 是 | `intraday / daily` |
| `anchor` | enum | 是 | `first_public_ts / effective_trade_date / transition_ts` |
| `pre_start` / `pre_end` | duration/index | 是 | 基线或预窗 |
| `post_start` / `post_end` | duration/index | 是 | 估计窗；日频主窗含事件当日 |
| `reporting_horizons` | integer array | 是 | 严格升序且含 0；当前建议 `[0,1,3,5]` |
| `overlap_horizon` | integer | 是 | 必须严格等于 `max(reporting_horizons)` |
| `boundary_rule` | enum | 是 | `closed / left_closed / right_closed` |
| `data_finality_lag` | duration | 是 | 逐 target/逐 horizon 的最晚 session 收盘后还需等待的冻结延迟 |
| `window_rule_version` | string | 是 | 版本化 |

当前 daily shadow 建议报告 horizon `[0,1,3,5]`，统一以**最后一个 cluster member 的有效交易日**为 `h=0`；重叠识别始终使用最大报告 horizon 5。cluster 的覆盖从最早成员开始，右端延伸到 `last_member + max_horizon`；对任一较短 `h`，观察窗仍从最早成员前一日收盘起，到 `last_member+h` 止。每个 target/horizon 独立通过两道 finality 门：所需观测的 `available_at_utc`（或更保守的 snapshot `observed_at_utc`）不得晚于 `as_of_utc`，且该 horizon 最后 session 的 `close_utc + data_finality_lag ≤ as_of_utc`。较短 horizon 已 final 不会让较长 horizon 自动 final。若分钟数据质量通过验收，可增加独立窄窗规格，但不能改变已冻结日频 cluster membership 而不升版本。

### 4.7 `estimation_runs`

每次运行至少记录：

- `run_id`、`created_at_utc`、`as_of_utc`；
- `eal-model-contract-v3.2 / eal-event-registry-v3.2 / eal-event-effects-v3.2` 及其 schema fingerprint；
- 输入快照 hash、`market_data_snapshot` 五字段、代码 commit、依赖锁 hash；
- taxonomy、clock、state、cluster、window、baseline、estimator、gate 版本；
- `target_series_ids`、`reference_series_ids`，以及逐 target 的预注册 `headline_orientation`（`higher_is_favorable / lower_is_favorable / neutral`）；
- 当前 `controls=[]` 的显式审计结果；若非空必须失败，前置控制待后续实现另开版本；
- 随机种子、优化器协议、重试协议、数值容差；
- 输入事件数、cluster 数、开放簇数、关闭清洁簇数、不同 episode 数、预注册独立组数、排除数和异常数；
- `run_status`：`started / completed / failed / completed_with_exclusions`。

`as_of_utc` 是冻结截止，不得使用该时点后才发布、修订或才为当时系统可得的数据。`market_data_as_of_utc` 必须与 snapshot attestation 的 `observed_at_utc` 逐字一致、不得晚于系统 UTC，DB SHA 必须与本次实际读取的封存文件一致；未来 attestation 以 `EAL_FUTURE_ATTESTATION` 拒绝。每行 frozen event 的 `first_public_ts_utc`、`first_public_lower_utc`、`first_public_upper_utc`、`classified_at_utc`、`state_known_at_utc` 和非空 `expectation_known_at_utc` 均必须 `≤ as_of_utc`，超过者以 `EAL_EVENT_METADATA_AFTER_AS_OF` 拒绝。正式 CLI 使用系统 UTC 作未来证明边界，不接受 caller 传入“当前时间”绕过。

## 5. 事件时钟合同

### 5.1 来源优先级

1. 权威主体的原始发布时戳或正式机器接口；
2. 可核对的同期通讯社/交易所时戳；
3. 有明确抓取时间与证据链的存档；
4. 事后新闻摘要只能补事实，不能把摘要发布时间当首次公开时点。

若多个可靠来源冲突，不得静默择一：保存候选、给 `bounded` 或 `unresolved`，并记录裁定依据。

### 5.2 交易日映射

对每个 `venue_id` 使用版本化正式交易日历：

- 交易日开盘前公开：映射到当日；
- 正常交易时段 `[open, close)` 公开：映射到当日；
- 收盘时点及之后公开：映射到下一交易日；
- 周末、法定休市、临时休市：映射到下一交易日；
- 同一事实的修订：建立新事实版本/修订事件，不能改写原时钟；
- 只有日期、无可界定时刻：保留在 needs-coding/历史证据层；当前 `eal-event-registry-v3.2` frozen runtime 不接受它，不得为进入日频 shadow 而伪造时分秒；
- 无法确定日期或来源：留 intake 并给稳定 unresolved 原因，任何估计排除。

DST 必须由 IANA 时区和市场日历处理，禁止手写固定 UTC 偏移。原始时间文本和其宣称时区/偏移必须保留；解析结果与原文冲突、`first_public_ts_utc` 不在已声明 bounds 内、事件早于日历首个 session，或需要后继 session 而日历已穷尽，均必须阻断并给稳定时钟错误族。

`clock_quality` 不是人工信心分。frozen v3.2 的 `reported_minute/reported_hour` 必须与 precision 和 bounds 机械一致；证据精度不足时只能留 intake/排除，不能以默认收盘时间伪造精确性。

### 5.3 覆盖与例外

人工覆盖必须同时具备 `override_flag=true`、原因、证据引用、操作者和时间；覆盖不能抹掉原派生值。覆盖记录属于审计事实，不自动提高识别等级。

## 6. Price-blind 分类合同

### 6.1 允许输入

分类进程只能看到版本化 structural-fact allowlist：

- 事件权威文本、原始数值、单位、正式规模、适用范围与法定等级；
- 事件前已经发布的共识/预期及其 `known_at_utc`；
- 事件前已确定的状态水平、`state_rule_version` 与 snapshot hash；
- 预注册 taxonomy、规则、词典或固定模型版本；
- 来源/发布时钟和与价格无关的事实证据引用。

allowlist 以字段名+来源 lineage+规则版本冻结；“业务上看起来像事实”不构成动态放行。

### 6.2 禁止输入

- 事件发生后或同一估计窗内的目标收益、SPY、VIX、油价、利率、信用利差、行业 ETF、成交量或隐含波动；
- 由上述行情生成的“冲击强弱”“市场认可”“风险开关”等派生标签；
- 事后复盘文本中引用市场反应的句子；
- 用结果方向覆盖原有 `expected_direction`。

### 6.3 执行约束

1. 分类在 join 市场观测前完成并冻结 `classification_id`。
2. 分类进程的数据视图不暴露禁止字段；只靠提示语“不要看价格”或 `price_blind_attestation=true` 不合格。attestation 只是审计声明，不是技术隔离证明。
3. 任意改变事件后市场数据而保留事实输入，分类逐字段和 hash 必须不变。
4. 人工复核只能引用非价格证据；若复核者因事后行情改变标签，必须另建研究注释，不能回写 price-blind 分类。
5. 无法 price-blind 分类时用 `ambiguous`/null，不用价格补齐。
6. 运行记录必须保存 allowlist 版本、分类输入 hash、lineage 和 denylist 扫描结果；市场价格置换后输出 hash 不变是必要证据，仍不单独证明不存在未见隐蔽通道。

## 7. Cluster 合同

### 7.1 确定性构造

对每个 `window_spec_id`：

1. 令 `Hmax = max(reporting_horizons)`，并强制 `overlap_horizon = Hmax`；
2. 为每个可进入的 event/transition 生成重叠区间 `[member_anchor, member_anchor+Hmax]`；
3. 两区间只要按 `boundary_rule` 相交就连边；
4. 区间图的连通分量构成 cluster，链式重叠不得拆开；
5. cluster 的 `first_member_anchor` 取最早成员，`last_member_anchor` 取最后成员，完整右边界为 `last_member_anchor+Hmax`；
6. `cluster_identity_material` 的 exact keys 为 `cluster_rule_version/window_spec_id/maximum_horizon/boundary_rule/member_identity_sha256`，其中 `maximum_horizon=Hmax`、成员 identity 排序；`cluster_identity_sha256=sha256(canonical_json(cluster_identity_material))`。`cluster_id` 可加固定 namespace 前缀，但必须包含完整 lowercase hex64 digest，不得截断，也不使用行号、输入顺序或显示名称；
7. 输入行顺序、数据库自然顺序和显示排序不得改变 cluster；
8. 单成员也是 cluster，便于统一审计；
9. 多个原子族成员时 `cluster_family=mixed`，同时保留成员原子族。

cluster 对象与每条以它为 analysis unit 的结果必须保留 `cluster_id`、`cluster_identity_sha256`、完整 `cluster_identity_material`（含排序后的 `member_identity_sha256`、`maximum_horizon`、`boundary_rule` 与 `window_spec_id`）。结果不得只存 `cluster_id` 或显示名称；adapter/SQL 回读必须重算 identity 并证明成员与窗口未漂移。

### 7.2 开放、关闭和清洁状态

- `open`：只用于所需 session 已可由冻结 calendar 定义、但至少一日仍满足 `close_utc + data_finality_lag > as_of_utc`。finality cutoff 前即使该日价格行暂不存在，也只记入 `window_unfinalized_dates`，不得提前记作 missing；稳定代码为 `EAL_EVENT_WINDOW_NOT_FINAL`。已经 final 的前缀 horizons 继续保留，但只可标 `descriptive_only`，所属 cluster 的 `n_closed_clean=0` 且不得进入 pool。
- 多成员 H0 前 canonical empty-horizon：若 `as_of_utc` 早于最后成员 H0 finality，则更早成员已 final 的负 `tau` 只属于内部路径，不能冒充非负 horizon。target 必须保持 `status=open/reason=data_finality_lag_not_elapsed/reason_code=EAL_EVENT_WINDOW_NOT_FINAL`、`horizons=[]`、`window_missing_dates=[]`，并把最后成员 H0 交易日列入 `window_unfinalized_dates`；除此只保留登记的最小审计 shape，不得带 estimate、baseline path、min/max 或 recovery。adapter 不生成 impact row，只留每 target 1 条 exclusion。
- `closed`：对该 target/horizon，从最早成员前一交易日收盘到 `last_member_anchor+h` 的完整市场观测均已到齐，观测 availability/snapshot 门与 session close+lag 门均通过。不得用 H=0 的 closed 替 H=5 签字。
- `not_estimable`：只有 finality cutoff 已到而事件窗应有 session 仍缺价时，才固定输出 `reason=missing_event_window_prices`、`reason_code=EAL_EVENT_WINDOW_PRICE_MISSING`、精确排序 `window_missing_dates` 和空 `horizons`；窗口超出 frozen calendar 时用 `EAL_EVENT_WINDOW_CALENDAR_INCOMPLETE`。
- `clean`：时钟、分类、基线、数据质量、重叠处理和排除审计均通过。
- 样本门的 `n` 不计 `cluster_id`；只计通过窗口与质量门后不同的 `independence_group_id`。同一 `episode_id` 的多个 cluster 只能贡献一个 episode 点，已知相依 episode 共享一个预注册独立组。

### 7.3 簇内识别

当前合同的 `separation_status` 只允许 `not_separable / not_applicable`：多成员 cluster 固定为 `not_separable`，单成员 cluster 为 `not_applicable`。当前实现不提供成员级分离；未来只有另升合同版本、引入第三种明确状态并独立验收后，才可输出成员级因果贡献。后续分离候选至少须满足：

- 成员具有不重叠的更窄有效窗口；或
- 存在预注册、外生且线性独立的 surprise measures，并通过秩与弱识别检查；或
- 有另一明确识别设计在 canonical 合同中登记并独立验收。

文本不同、事件族不同或模型能拟合出多个系数，不构成可分离证据。多成员簇只报告整体 shadow；成员行可列事实与机械窗口，但统一标记 `◌ not_separable`。不得使用其他同义拼写或空值作为持久化状态。

## 8. 状态与跃迁合同

### 8.1 状态不是每日方向信号

状态用于回答“同样的事件在不同背景下传导是否不同”。它可进入预事件交互项、分层报告或风险条件，但不能因为状态仍在就每天制造同方向冲击。

### 8.2 跃迁定义

- `entry`：从无状态/基准状态首次进入目标状态；
- `escalation`：状态等级严格上升；
- `easing`：等级下降但尚未退出；
- `exit`：回到明确定义的非状态/基准状态。

`none` 是 frozen event 与 runtime result JSON 中“本行无状态跃迁”的 canonical sentinel，不是第五种跃迁实体。runtime registry/result JSON 字段名为 `transition`，SQL event/result row 字段名为 `transition_type`，adapter 映射后值仍为 `none`。cluster 包含不同成员 transition 时可派生 `mixed`；`mixed` 也不允许写入 `state_transitions` 实体表。

跃迁规则必须只依赖外部事实或正式裁定，且在看事件后价格前确定。进入和退出使用独立 treatment 标签、独立系数和独立样本门；不得假定 `exit_effect = -entry_effect`。

frozen registry 中 `state_type` 必须非空。entry/exit 配对至少同时满足 `episode_id` 相同、`state_type` 相同、状态规则版本兼容且时间顺序有效；聚合键也必须包含 `state_type`。不同 `state_type`、真实状态与 `not_applicable`、或仅因文本相似的事件禁止配对或合池。

“状态规则版本兼容”不得只比较 `state_type` 名称。聚合键必须包含 `state_rule_version`；只有 canonical 合同中存在显式、可重放的版本兼容映射，并证明等级顺序、边界和 transition 语义不变，才能跨版本合池；否则分开报告或以稳定排除码降级。

### 8.3 防止时间偏差

- 状态的 `valid_from` 使用首次生效/公开时点，不用事后确认日回填而不留版本；
- 开放状态不得提前知道未来 `valid_to`；
- 只使用事件前状态判断交互项，禁止把事件后升级作为事件前条件；
- 回溯重分类只能在新运行版本生效，旧运行保留原快照。

## 9. Baseline、后续反事实与控制合同

### 9.1 当前 daily shadow：控制集只能为空

当前 staging runtime 只实现未调整的日频 shadow。配置必须逐字满足 `controls=[]`，`control_set_id` 必须指向 canonical empty set。任何控制项——即使声称是事件前变量——都以 `EAL_CONTROLS_NOT_IMPLEMENTED` 或同族稳定错误非零退出，不能静默忽略。

这不是说前置控制在方法上永远禁止，而是当前实现尚未具备逐行 `available_at`、训练窗隔离、估计器身份和相应负测。先保持空集，避免“schema 接受了、实际没正确实现”的伪支持。

### 9.2 当前 daily baseline

当前 shadow 冻结并版本化的是 baseline **构造规格和本次运行结果**，不是假定外部预供一条第二真源序列，更不是已识别的“没发生事件”反事实。当前参考规格从每个 cluster 之前的 target daily change 取固定 lookback，在满足最小观测数后计算 trailing mean，并用该均值生成窗口内同长度 compound daily baseline；lookback、最小观测数、收益单位、排除策略、所得 `baseline_mean` 和逐 horizon baseline path 都须随运行冻结。若训练窗排除事件，只允许排除 `as_of_utc` 前已进入本次 frozen registry 且已登记的完整事件窗；不得根据本次收益残差、事后新闻或事后扩张的模糊事件集合追加排除。未知或尚未登记事件只能作为污染风险披露，不能事后删样本。运行时不再用控制变量调整该 baseline。

同一 cluster/horizon 的 observed 与 baseline 必须：

- 使用完全相同的起止交易日和交易日历；
- 使用相同收益单位和复利规则；
- 覆盖从 `first_member_anchor-1` 收盘到 `last_member_anchor+h`；
- finality cutoff 前的 baseline 日无论价格行是否已到，都只进入 `baseline_unfinalized_dates`；target 返回 `status=open/reason_code=EAL_BASELINE_NOT_FINAL` 且不输出 horizon。只有 cutoff 已到而应有行仍不存在，才进入 `baseline_missing_dates` 并给稳定 `EAL_BASELINE_PRICE_MISSING`；可用观测数低于预注册 minimum 时用 `EAL_BASELINE_INSUFFICIENT_OBSERVATIONS`。不能把缺失补 0、缩短窗口或 drop 日后继续可报告。无缺失且全部 final 时也须显式保存 `baseline_complete=true` 和空缺失/未 final 清单。

### 9.3 同日/处理后变量仍属禁止输入

目标资产和基准资产当期收益、SPY/QQQ/SMH、VIX、油价、黄金、美元、利率、信用利差、`ai_gap`、成交量、资金流、事后新闻情绪及由其生成的标签，均不得作为当前 shadow 的 control 或分类输入。预注册为 target outcome 的序列可以作为结果，但不能同时作为 control。

把这些变量纳入后得到的至多是 `DIRECT_ASSOC`，不是 `DAILY_SHADOW` 或 `TE_EVENT`。即使拟合提高，也不得越权改名。

### 9.4 后续前置控制的开放条件

未来若实现正式 CAR、market model 或 local projection，必须另升 `estimator_spec_id/contract_version`，并同时完成：

- 只接受 treatment 前已可得的信息 `I(t0−)`；
- 逐行验证 `available_at_utc < treatment_time`；
- 训练窗、holdout gap 和参数冻结无前视；
- allowlist/denylist 与别名负测；
- 合成真值、普通/`-O`、共同窗和异常账验收。

这些条件完成并独立验收前，不能通过配置“提前开启”controls。

## 10. 估计与指标合同

### 10.1 当前 return daily shadow 的唯一公式

对 cluster `k`，记：

- `d_first(k)`：最早成员的有效交易日；
- `d_last(k)`：最后成员的有效交易日；
- `d_pre(k)`：`d_first(k)` 的前一交易日；
- `d_end(k,h)`：`d_last(k)` 后第 `h` 个交易日，`h=0` 即最后成员当日；
- `r(k,d)`：目标的 close-to-close daily return；
- `b(k,d)`：同一交易日、同一收益单位的 frozen daily baseline return。

从 `d_pre` 收盘到 `d_end(k,h)` 的 return shadow 定义为：

```text
R_observed(k,h) = Π[d=d_first(k)..d_end(k,h)] (1 + r(k,d)) - 1
R_baseline(k,h) = Π[d=d_first(k)..d_end(k,h)] (1 + b(k,d)) - 1
daily_shadow_compound_gap(k,h) = R_observed(k,h) - R_baseline(k,h)
```

observed 与 baseline 必须覆盖完全相同的交易日。cluster 内即使有多名成员，起点也固定为最早成员前一日收盘，horizon 固定从最后成员锚定；不得为较短 horizon 截掉较早成员。内部须计算 `h=0..Hmax` 的完整路径，展示可只选预注册 horizon。

所有多事件 response 的时间坐标统一为 `tau(d) = trading_day_index(d) - trading_day_index(d_last(k))`：最后成员有效交易日恒为 `tau=0`，更早成员可位于负 `tau`，报告 horizon `h` 就是正向 `tau=h`。不得另以 `d_first` 重置第二套 `h=0`；`d_first/d_pre` 只定义复利观察起点。

这个量**不是**原先 `AR(k,h)` 再做 `ΣAR` 的 CAR，也不得命名为 `AR/CAR/CAAR`。正式 abnormal return、CAR、CAAR 与 local projection 留给后续独立估计器和结果身份。非 return 的 level target 必须使用另一个显式 additive metric（例如 `daily_shadow_level_gap`），不得与复利 return 混用。

### 10.2 当前 shadow 的烈度与恢复指标

每个完整关闭簇基于 `daily_shadow_compound_gap(k,h)` 的 `tau` 路径，先计算不带价值方向的中性响应：

- `shadow_gap_tau0` 及所有预注册正向 horizon 的 gap；
- `min_shadow_gap` 与 `tau_at_min`：完整路径最小值及首次达到它的相对 `d_last` 坐标；
- `max_shadow_gap` 与 `tau_at_max`：完整路径最大值及首次达到它的相对 `d_last` 坐标；
- 中性 `entry_exit_gap_difference` 与 `entry_exit_gap_ratio` 是明确的未来项，当前 runtime/SQL 不生成也不承诺这两个字段。

`expected_direction` 描述事件相对预期的事实方向，不等于资产损益 orientation。当前实现只支持在看结果前冻结的 SPY `headline_orientation=higher_is_favorable`，并由中性 min/max 派生 adverse/rebound/recovery；orientation 缺失、`neutral`、其他 target 或事后填写时，只报告中性 min/max，不生成方向化字段。所有派生字段须记录 orientation 值与版本，不能根据实际涨跌选择符号。其他 target/orientation 以及中性 entry/exit 组间 gap 比较均须另升合同后实现。

指标单位、收益定义、`d_first/d_last/d_pre`、`tau` 与 horizon 必须随结果保存。窗口内未恢复时，orientation 派生的 `time_to_recovery` 为 null 并标 `right_censored`。

### 10.3 当前 shadow 聚合

当前聚合仍是描述性 `DAILY_SHADOW`，不是 local projection：

1. 聚合键至少包含 `estimand_id`、`metric_id`、`target_series_id`、`window_spec_id`、`atomic_family`、`state_type`、`state_rule_version`、canonical `transition_type`、horizon、shock unit 和 rubric version；这些字段任一不同均不得合池；
2. 同一 `episode_id` 在同一聚合键下的多个 cluster 先用预注册 reducer（当前建议等权 episode mean）压成一个 episode 点；
3. 已知相依的多个 episode 再按 `independence_group_id` 压成一个独立组点；
4. 样本 `n` 只计独立组点；不得以 cluster 数、事件数、target 数或 horizon 数抬高；
5. entry/exit 配对和聚合不得跨 `state_type`；
6. 数值型 `shock_value=0` 是有效观察：必须进入相应描述聚合，也不得从预注册 shock–gap 斜率中静默删除。只有 shock 缺失、单位/量表不兼容或组内无变异时才令 slope 不可用，并输出稳定原因；描述聚合仍保留该组；
7. 小样本只按 §12 的措辞门显示，不输出伪精确因果 p 值。

可报告均值、范围、描述性区间和预注册 shock–gap 斜率，但字段须含 `estimand_id=DAILY_SHADOW`、独立组数和“描述性”状态。

### 10.4 后续正式 CAR/local projection

正式异常收益/CAR 或 local projection 不在当前 shadow 实现范围。后续至少须：

- 使用新的 `estimator_spec_id/contract_version`；
- 定义事件前训练信息集、controls、标准误与共同窗；
- 以独立 episode/预注册独立组做推断；
- 通过合成真值、弱识别、收敛、异常账及普通/`-O` 负测；
- 不覆盖或重命名既有 shadow 字段。

### 10.5 权重/份额合同

当前可选份额只能叫 `shadow_share`：

```text
shadow_share = daily_shadow_compound_gap / R_observed
```

它必须标注“描述性、非 CAR、非因果”，且只在分母绝对值超过预注册阈值时显示。允许负值和大于 100%，分别表示抵消或放大；不可分离 mixed cluster 只给 cluster 份额。后续 `TE_EVENT/TE_TRANSITION` 若定义正式 `impact_share`，必须使用另一结果身份，且任何份额不得跨 `estimand_id` 相加。

## 11. 输出 schema

### 11.1 `event_clusters`

至少包含：

```text
cluster_id, cluster_identity_sha256, cluster_identity_material,
cluster_rule_version, window_spec_id, maximum_horizon, boundary_rule,
member_event_ids, member_identity_sha256, member_transition_ids, member_count,
member_episode_ids, independence_group_ids,
cluster_family, transition, first_member_anchor, last_member_anchor,
window_start_utc, window_end_utc,
cluster_status, data_final_at_utc, clean_flag,
separation_status, separation_reason_code
```

`cluster_identity_material` 的 exact keys 是 `cluster_rule_version/window_spec_id/maximum_horizon/boundary_rule/member_identity_sha256`；成员 identity 必须排序。`cluster_id` 必须包含该 material 的完整 64 位 SHA-256 digest（允许固定 namespace 前缀）；`cluster_identity_sha256` 必须可由同行 material 重算。当前 `separation_status` 只能为 `not_separable` 或 `not_applicable`。cluster `transition` 可为五个 canonical event 值或派生 `mixed`。

### 11.2 `impact_results`

每行一个结果—指标—horizon：

```text
result_id, identity_sha256, run_id, model_version, estimand_id, estimator_spec_id,
analysis_unit_type, analysis_unit_id, cluster_id, cluster_identity_sha256,
cluster_identity_material, target_series_id,
atomic_family, cluster_family, state_type, state_rule_version, transition_type,
episode_id, independence_group_id,
window_spec_id, metric_id, horizon_id, response_tau, unit,
first_member_anchor, last_member_anchor, window_complete,
headline_orientation, orientation_version,
baseline_complete, baseline_missing_dates, baseline_exclusion_code,
market_data_snapshot_id, market_data_snapshot_database_sha256, market_data_source_version,
data_final_at_utc, data_finality_status,
estimate, standard_error, ci_level, ci_lower, ci_upper, p_value,
n_events_raw, n_clusters_total, n_independent_episodes,
n_independence_groups,
sample_gate, identification_grade, source_confidence,
statistical_precision, result_status, exclusion_code,
baseline_spec_id, control_set_id, created_at_utc
```

约束：

- `identity_sha256` 对完整结果身份 material 做 SHA-256，并在 SQL 中设 `UNIQUE`；`result_id` 可由它稳定派生。同 identity 不同值必须报冲突，不能 last-write-wins。
- frozen event 与可报告结果的 `state_type` 必须非空；不适用时使用 canonical sentinel，不得用 SQL null 绕过聚合键。
- runtime `transition` 落库为 `transition_type`，值不改；无跃迁固定为 `none`，cluster 层可为 `mixed`，不得以 null/空字符串创建第二口径。
- cluster analysis unit 的 runtime 结果必须同时含 `cluster_id/cluster_identity_sha256/cluster_identity_material`；SQL normalized impact row 分别保存 `cluster_id/cluster_identity_sha256/cluster_identity_material_json`，并与 parent cluster exact 相等。pool result 的这三个 cluster identity 字段必须全为 null，不能借用任一成员簇身份。
- 聚合或 entry/exit 配对不得跨不兼容 `state_rule_version`；无明示兼容映射时必须分池。
- `result_status in (reportable, descriptive_only)` 时，`estimate` 必须有限、`window_complete=true`、identity/窗口/state_type 完整且 `exclusion_code` 为空。
- `result_status in (not_identified, excluded, failed)` 时，必须有 `exclusion_code`；`excluded/failed` 的 `estimate` 必须为空，不能用 0 代替。
- 当前 `DAILY_SHADOW` 的 `control_set_id` 必须指向空集，`metric_id` 不得包含 `AR/CAR/CAAR/local_projection`。
- `baseline_complete=false` 时该 horizon 不可报告。finality lag 尚未届满时使用 `baseline_unfinalized_dates/EAL_BASELINE_NOT_FINAL`；cutoff 已到但行仍缺失时才使用 `baseline_missing_dates/EAL_BASELINE_PRICE_MISSING`。两者都不能以 0 estimate 表示。
- 每个进入 `horizons` 的 row 必须携 `data_final_at_utc` 与 `data_finality_status=final`。事件窗开放时保留已经 final 的前缀 rows；adapter/SQL 将这些前缀 estimate 持久化为 `descriptive_only`，但 cluster 仍保持 `n_closed_clean=0`，任何前缀 row 都不得进入 pool。未 final 日期进入 target 的 `window_unfinalized_dates`，只有 cutoff 已到仍无行才进入 `window_missing_dates`。target 总体完结性只由“全部预注册 horizon 的 `status=final`”派生判断，不另存 `finality_complete` runtime/SQL 字段；不得从另一 horizon 继承。
- `p_value` 在合同不允许推断时必须为 null。
- 每个结果可追到 cluster/event、输入快照、配置和代码版本。

上述约束必须同时存在于入口校验和 SQL `UNIQUE/CHECK` 层。报告汇总的 reportable/non-reportable 计数必须与 SQL 行逐项对账；不能只在渲染器里过滤出“看起来一致”的页面。

### 11.3 `run_exclusions`

```text
run_id, analysis_unit_id, stage, exclusion_code,
message, source_row_ref, first_seen_at_utc
```

排除和异常分列汇总。任何异常不得被共同窗不匹配、收敛失败或最终汇总遮住。

### 11.4 Missingness audit

当前 runtime 可把审计内联在 target 对象，SQL/analytics 层可拆成 `missingness_audit` 逻辑表。每个 `run_id + analysis_unit_id + target_series_id + horizon_id + stage` 至少可还原：

```text
expected_session_dates, observed_session_dates, missing_session_dates,
market_data_snapshot_id, availability_cutoff_utc, data_final_at_utc,
is_headline_target, disposition, exclusion_code
```

`stage` 区分 `event_window / baseline_lookback / response_asset / finality`。headline target 或 baseline 缺失使对应 horizon 不可报告；预注册可选 response asset 缺失可只降级该 response，不污染 headline，但两者都必须留账。空清单也必须显式保存，不能以“无记录”表示无缺失。

当前 target 对象的精确审计字段是 `baseline_complete`、`baseline_candidate_n`、`baseline_used_n`、`baseline_missing_dates`、`baseline_unfinalized_dates`、`baseline_excluded_registered_event_dates`、`window_missing_dates`、`window_unfinalized_dates`、`data_final_at_utc`。cutoff 前无行只能进入相应 unfinalized 清单；`window_missing_dates` 只记录 cutoff 已到仍缺失的累计路径 anchor(t−1) 或窗口端点。

### 11.5 Runtime→SQL adapter 和 round-trip

adapter 是生产候选的必经路径，不是可选导出器。它必须独立接收 candidate DB、frozen market DB、result JSON、frozen registry、frozen calendar 与 `loaded_at_utc` 六项输入。market DB 必须是绝对路径、非 symlink 的单硬链接普通文件，不得与 candidate 指向同一 inode，也不得带 `-wal/-shm/-journal`；稳定读取必须用 `O_NOFOLLOW` 打开，并在快照前后核对同一 `(st_dev,st_ino,st_size,st_mtime_ns)`，事务结束后再重验源 SHA。该 SHA 必须同时等于 result 的 `input_identity.database` 与嵌入配置的 `market_data_snapshot.database_sha256`。

adapter 不能信任 result JSON 中任何同名派生值。它使用同一冻结 market snapshot、registry、calendar 与 result 内嵌 config 重新执行 `run_event_study`，并要求重放所得整个 canonical result document 逐字义 exact 相等；不相等统一拒绝为 `EAL_RESULT_RUNTIME_REPLAY_MISMATCH`。这个全文门覆盖 input identity、cluster/member、finality、missingness、baseline path、min/max、recovery 与所有排除记录，不能缩成 SQL 投影或少数字段抽查。随后 adapter 再验证 schema/runtime shape parity 的固定版本、逐行 semantic parser 与 SQL schema-contract fingerprint，使用登记 mapping 落库，并从同一 transaction 及提交后只读 reopen 回读 canonical runtime 形状。`loaded_at_utc` 必须是带时区的 UTC 审计时间，但不进入 result identity。

registry member purity 是严格门，cluster impact 的 digest/material 必须绑定 parent exact，pool 的 cluster identity 三字段必须全空。事件窗开放时，已经 final 的前缀 horizon estimate round-trip 为 `descriptive_only`；target 级 `open/EAL_EVENT_WINDOW_NOT_FINAL` 原因由 source result JSON 与 exclusion ledger 保留，cluster 的 `n_closed_clean=0` 且不得写入 pool。若多成员簇在最后成员 H0 finality 前没有可发布的非负 horizon，adapter 必须产生 0 条 impact row 和每 target 1 条 exclusion，不能从较早成员的负 `tau` 造 estimate。pool `sample_gate` 必须按冻结 exact object 并从真实 junction membership 重算；持久枚举精确为 `preliminary_pooling/provisional_band`，重复 membership、层级权重漂移或加权均值不一致都在 seal 前阻断。版本化 fact v2 既保存 normalized 列，也保留 raw registry row。round-trip 比较必须覆盖类型、null/`none`、枚举、identity、cluster 成员、逐 horizon finality、缺失/未 final 清单和 reportability；任一不等价都撤回本次候选写入。shadow.7 SQL 独立只读数据合同复核 PASS：最终 SQL SHA-256 为 `898fda27b3fbc6b25f3fde4211bc19bd22423fe489badaf63b5bbad650644013`，schema fingerprint 为 `205af71a3e266f93460d3b6da8796c2e790497a23f1a4016e2c11c37d2e801e5`；inventory 为 16 tables / 12 explicit indexes（37 indexes including 25 autoindexes）/ 54 triggers / 107 namespace objects，15 张 mapped data tables，migration 普通/`-O` 均 19/19，legacy migration 均 7/7。若生产集成环境另有 standards-compliant Draft 2020-12 validator，可作为附加门，但不能替代 `parse_event` semantic 门。

## 12. 样本门

样本计数单位统一为通过窗口/质量门后的 `independence_group_id`。默认一个 `episode_id` 对应一个独立组；同一 episode 的多个 cluster 先压成一个 episode 点，已知相依的多个 episode 按预注册映射合并为一个独立组。并按同一 event family、canonical transition、`state_type`、`state_rule_version`、目标资产、window 和 estimator 规格计算。

| n | 允许输出 | 禁止措辞 |
|---:|---|---|
| 0 | `◌ no eligible independent group` 与原因 | 任何方向、均值或权重 |
| 1 | 个案机械路径 | 稳定规律、平均效应、显著性 |
| 2 | 并列个案与范围 | 池化结论、趋势确认 |
| 3–5 | 方向性探索，完整逐例清单 | “证明”“稳定”“确认” |
| 6–9 | `preliminary_pooling`，宽区间与敏感性 | 稳健、可外推 |
| 10–19 | `provisional_band`，可比较规格 | 最终确认、普遍规律 |
| ≥20 | `confirmation_candidate`，仍须通过识别/来源/精度门 | 因样本数自动称因果 |

`sample_gates` 在 model v3.2 内不是可调超参数，而是 same-schema exact frozen object：必须恰为 `case_only_max=2`、`directional_max=5`、`preliminary_max=9`、`provisional_min=10`、`candidate_min=20`、`minimum_independence_groups=3`。只满足单调关系仍不合格；runtime 必须以 `EAL_CONFIG_INVALID` 拒绝，adapter 另以 `EAL_SAMPLE_GATE_MISMATCH` 拒绝与冻结合同不一致的 result。

事件行或 cluster 行不直接计 `n`。同一 episode 即使落入多个不相交 cluster 也只计一次；多个 window、target 或 horizon 不是额外独立样本。开放簇、重复事实、同一冲击的修订和未处理依赖不计入样本。独立组映射必须在看结果前冻结并版本化。

## 13. 识别、来源与精度三轴

### 13.1 识别等级

| 等级 | 最低条件 | 允许表述 |
|---|---|---|
| `ID-A` | 预定事件；精确时钟；事件前共识与实时 surprise；干净窄窗；无重叠或已识别分离；设计预注册 | “高频识别的边际冲击” |
| `ID-B` | 权威突发事件；精确首次公开时钟；price-blind 强度；干净窄窗；无近邻混杂；稳健性通过 | “准实验式事件冲击候选”，并列限制 |
| `ID-C` | 日频事件/簇研究、状态跃迁描述或存在不可排除混杂 | “异常变动”“描述性边际关联” |
| `ID-U` | 时钟/来源未解、结果泄漏、不良控制、窗口不完整、簇不可用或关键合同失败 | 只报告不可识别与原因 |

`ID-A/B` 不是由回归显著性授予；`ID-C` 也不因样本大自动升级。

当前 `DAILY_SHADOW` 因使用日频无控制描述性基线，识别等级最高为 `ID-C`；达到 20 个独立组也只能成为统计上的 confirmation candidate，不能升级为 `ID-A/B`。`ID-A/B` 只留给后续正式高频/识别设计。

### 13.2 来源可信度

建议独立枚举：

- `SRC-1`：权威原始发布/正式记录；
- `SRC-2`：可核对的同期高质量二手来源；
- `SRC-3`：来源间接、时间或内容有实质不确定；
- `SRC-U`：不可回读或冲突未解。

### 13.3 统计精度

建议独立枚举：

- `PREC-0`：不提供推断；
- `PREC-1`：极宽区间/小样本探索；
- `PREC-2`：暂定，主要规格和敏感性方向一致；
- `PREC-3`：预注册精度阈值通过且稳健性一致。

三轴并列展示，例如 `ID-C / SRC-1 / PREC-2`。任何 UI 或摘要不得压缩为单一“可信分”。

## 14. Fail-closed 与排除合同

### 14.1 必须阻断当前运行的错误

- JSON Schema/runtime parity 漂移、semantic parser 未通过，或 schema/version 不支持；
- 主键重复、`identity_sha256` 重复、时间无序、非法枚举；
- frozen registry 缺 `episode_id/independence_group_id/state_type/state_rule_version`；
- 非有限收益、预测或方差；
- 原始时区/偏移与解析 UTC 冲突、时钟 bounds/质量矛盾或越出冻结日历；
- `market_data_as_of_utc/snapshot.observed_at_utc` 不等或晚于系统 UTC，或事件首次公开/bounds/分类/状态/预期时间晚于 run as-of；
- `available_at`/snapshot 可得边界违规，或任一 target/horizon 被误标 final；
- 分类器读取禁止市场字段；
- 当前 daily shadow 的 controls 非空；
- `overlap_horizon != max(reporting_horizons)`；
- cluster 成员/窗口不一致，或未覆盖 `first_member-1` 至 `last_member+Hmax`；
- cluster identity 未使用完整 SHA-256，或 `cluster_identity_material` 缺 exact `maximum_horizon/boundary_rule/member_identity_sha256`；
- 聚合或 entry/exit 配对跨 `state_type`、跨不兼容 `state_rule_version`，或无跃迁值未 canonical 为 `none`；
- 聚合键缺 target/metric/estimand/window spec，或合法 zero shock 被静默删除；
- 同 episode 多 cluster 被重复计入样本门；
- 结果同键异值；
- runtime→SQL adapter 遇到未登记映射、schema fingerprint 不符或 round-trip 不等价；
- reportable 状态与 estimate、完整窗口、state_type、identity 不一致；
- 非可报告状态缺 exclusion code；
- 共同窗与预期不一致且未显式授权排除；
- 所有窗口失败、存在未入账异常，或缺失/finality 对账不完整。

关键守卫使用显式异常，不使用 `assert`。普通模式和 `python -O` 必须产生相同错误族与非零退出。

### 14.2 可降级但必须显式记录的情况

- 单个事件低精度时钟；
- 开放簇；
- finality cutoff 已到后的个别市场或 baseline 观测缺失：对应 target/horizon 必须为 `not_estimable`，列出精确 missing 日期与稳定 exclusion code，不得标为 `open`；cutoff 前同一无行只能进入 unfinalized 清单并使用相应 `open` finality code；
- 单一敏感性规格不收敛但 primary 完整；
- 样本门不足；
- 识别等级只能为 C/U。

降级必须生成 `run_exclusions` 或结果级状态，汇总输入数、排除数、异常数和最终共同样本。不得静默 dropna 后只报告剩余 `n`。

## 15. 验证合同

### 15.1 必备测试族

1. Draft 2020-12 JSON Schema 的 `required/properties`、fact allowlist 与 runtime parser 持久 shape parity，加 semantic parser 正反例；重复键/identity、跨字段矛盾、乱序、非法枚举及 frozen `state_type/state_rule_version` 缺失不能只靠 schema 文件/parity 拦截；
2. 事件时钟矩阵：盘前/盘中/盘后/周末/休市/DST/日期级/修订，外加 raw timezone/offset 冲突、bounds 矛盾、日历前边界/后边界；
3. price-blind structural-fact allowlist、lineage/denylist 哨兵、价格置换不变测试，并证明只改 `price_blind_attestation` 不能绕过技术隔离；macro v2 的 9 个闭集 release code、earnings v2 的 CIK exact identity 与 `SPY/SP500` 假代码负测须同时通过；
4. cluster 链式重叠、输入乱序、`overlap_horizon=max(horizons)`、最后成员锚、开放/关闭、mixed 派生，以及 exact `cluster_identity_material` 与完整 SHA-256 identity；
5. state/transition 合成序列、`none`/`mixed` canonical 边界、未来信息隔离、相同 `state_type + state_rule_version` 聚合与 entry/exit 配对，以及无兼容映射的跨版本拒绝；
6. daily baseline 冻结、非反事实标记、只排 registered frozen events、未知事件不事后排除、cutoff 前 unfinalized 与 cutoff 后 missing 的互斥日期/exclusion、`EAL_BASELINE_NOT_FINAL`、事件后数据置换、最早成员前一日到最后成员加 h 的同长度覆盖；
7. 当前 controls 空集正例与任意非空字段负测；
8. 手算复利 observed、compound baseline、shadow gap、相对 `d_last` 的 `tau`、中性 min/max；另验证当前只有预注册 SPY `higher_is_favorable` orientation 才派生 adverse/rebound/recovery，中性 entry/exit gap difference/ratio 不存在，并证明不是 `ΣAR` CAR；
9. shadow 合成路径、空 gap、异质 gap 和重叠不可分离；
10. episode/预注册独立组去重、完整聚合键、合法 zero shock 保留、样本门全部边界，以及 same-schema `sample_gates` 任一数值漂移仍以 `EAL_CONFIG_INVALID` 拒绝；
11. ID/SRC/PREC 全组合及降级原因；
12. SQL identity 唯一、结果同键异值、reportability CHECK、null 与 0 语义及总数对账；
13. runtime→SQL adapter 字段映射、schema fingerprint 漂移拒绝、冻结 `sample_gates` exact mismatch、market DB 的绝对路径/symlink/hardlink/candidate-alias/sidecar/stable-file/SHA 安全门，以及对伪造 finality、missingness、baseline、min/max、recovery 的 whole-document runtime replay 拒绝；随后验证含 `none/mixed`、cluster identity、缺失和 finality 的 canonical SQL round-trip；
14. 逐 target/逐 horizon availability+close/lag finality，future config/event metadata 拒绝，cutoff 前无行仍为 unfinalized、开放事件窗保留 final 前缀且 SQL round-trip 为 `descriptive_only`/cluster `n_closed_clean=0`/pool 0、最后成员 H0 finality 前多成员簇 canonical `horizons=[]` 且 0 impact row/每 target 1 exclusion、baseline 未 final 无 horizons、cutoff 后事件窗缺价 `not_estimable`、calendar 不完整、baseline 缺价/观测不足、headline/可选 response 分流与全量 missingness audit；
15. 全失败窗、共同窗异常和异常汇总；后续估计器另加优化器/收敛测试；
16. 普通与 `-O` 双模式；
17. v2.3/v3 冻结样本双跑、兼容读取和回滚；
18. artifact 事件导航、空状态、不可识别、移动端与可访问性人工走查。

### 15.2 可重放运行包

至少包含：

- 冻结输入及数据字典；
- 单一入口命令与真实退出码；
- 精确依赖锁和 Python/SQLite 版本；当前参考实现只使用 Python 标准库，声明支持 CPython 3.11+，但本轮本机证据只覆盖 CPython 3.14.6 + Python `sqlite3` runtime SQLite 3.53.2（operator CLI SQLite 3.51.0），其他小版本须在独立 CI 重跑后才能称已验；
- 配置、随机种子和所有 rule/model versions；
- 原始 stdout/stderr 或结构化运行日志；
- 输入、输出、测试和代码 payload 的 SHA256；manifest 不得自哈希；
- README 中的普通、`-O`、负向注入、影子双跑和回滚命令；
- 每次运行的排除/异常/收敛全量审计。

这些均是功能验收证据，不自动赋予 PRD `[✓]`。

## 16. 兼容与退役策略

### 16.1 v2.3 保留

- 冻结 v2.3 输入、代码、输出和方法说明，不重写历史；
- M4 标为 `DIRECT_ASSOC`，保留“同日条件共变、解释性、非因果、非预测”身份；
- 旧 `trade_date` 继续可读，新时钟另存 `effective_trade_date` 和差异原因；
- v3 不复用 v2.3 结果键，不在同一字段里覆盖旧数值。

### 16.2 机械层退役

旧固定幅度/关键词映射层在 v3 独立验收前继续作为 `legacy_mechanical` 比较基线。满足以下条件后才可从主产品退役：

1. v3 对既有事件覆盖率达到 canonical 预设阈值；
2. PRD 功能与非功能需求获得合法验收；
3. 至少完成预设次数的冻结样本影子双跑；
4. artifact 和下游消费者已迁移且回读通过；
5. 回滚到最后已验收 v2.3 版本的演练通过；
6. Doctor 明确批准切换。

退役是从主入口移至 archive，不删除历史输入、结果或说明。

### 16.3 单向发布

建议链路：

```text
Codex staging（本目录，仅建议）
  → CC 实读 Brain 与仓库现状
  → Brain canonical 方法合同 + PRD
  → 结构化 schema / 代码 / 冻结复现包
  → preview / candidate
  → 独立功能验收
  → 正式发布机制
  → Gateway active 回读
  → Brain mirror / manifest 刷新
```

任何层失败都停在当前层，不用手工复制绕过生产发布器，不从 Gateway 或 artifact 反向改 Brain 方法。

## 17. CC 实施建议文件面

这是职责清单，不是本 staging 轮的写权限：

```text
/Users/lunarabbit/Documents/Claude/brain/
  logs/checkpoints/2026-08-19_EALv3事件冲击与状态跃迁_PRD.md
  剑酒青丘/frameworks/EAL-v3事件冲击与状态跃迁模型.md
  剑酒青丘/frameworks/事件归因台账.md              # 只加指针/状态/经确认结果
  剑酒青丘/GOTCHAS.md                              # 实际错题登记

/Users/lunarabbit/Documents/Database/剑酒青丘/
  backtest/eal_v3/schema.sql
  backtest/eal_v3/migrate_v23_to_v3.py
  backtest/eal_v3/build_event_clock.py
  backtest/eal_v3/classify_event_price_blind.py
  backtest/eal_v3/build_clusters.py
  backtest/eal_v3/build_state_transitions.py
  backtest/eal_v3/build_descriptive_baseline.py
  backtest/eal_v3/estimate_event_impacts.py
  backtest/eal_v3/validate_contract.py
  backtest/eal_v3/config/
  backtest/eal_v3/tests/
  backtest/eal_v3/repro/
```

CC 必须先用 `rg --files` 和 Brain 现行规则校准实际落点。若已有同职责模块，优先兼容和迁移，不平行复制；若路径变化，在 canonical 变更记录中写明替代关系。

## 18. 明确不作的声明

- 不把当前 `daily_shadow_compound_gap` 称为 AR、CAR、CAAR、local projection 或已识别因果效应；
- 不声称控制更多同日市场变量就更接近总效应；
- 不声称事件族系数能逐日精确拆账；
- 不声称 mixed cluster 的成员权重可分离；
- 不声称 p 值显著即可升级识别等级；
- 不声称事件行数、cluster 行数或 episode 行数自动等于预注册独立组数；
- 不声称文件、hash、grep 或测试通过即完成独立功能验收；
- 不声称本 staging 合同已经写入 Brain、被 CC 实施或被 Doctor 验收。

## 19. 起草依据与实施前回读

CC 在 canonical 化前至少回读：

- `/Users/lunarabbit/Documents/Claude/brain/剑酒青丘/frameworks/事件归因台账.md`
- `/Users/lunarabbit/Documents/Claude/brain/剑酒青丘/frameworks/状态-触发-传导系数.md`
- `/Users/lunarabbit/Documents/Claude/brain/logs/checkpoints/2026-08-17_EAL-B阶段G2G3执行方案.md`
- `/Users/lunarabbit/Documents/Claude/brain/剑酒青丘/frameworks/机械回测口径-v0.md`
- `/Users/lunarabbit/Documents/Database/剑酒青丘/backtest/build_factor_daily_backtest.py`
- `/Users/lunarabbit/Documents/Database/剑酒青丘/backtest/repro_v23/`

若这些现行材料已发生变化，以 Brain 最新 canonical 和可重放数据为准，并在迁移报告中列出本合同需要调整的条款，而不是静默沿用过时 staging。
