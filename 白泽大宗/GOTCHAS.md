---
title: 白泽大宗 · GOTCHAS
tags: [白泽大宗, gotchas]
created: 2026-06-10
updated: 2026-11-05
status: active
type: resource
---

# 白泽大宗 GOTCHAS

- **G-01 周报 MD 位置**：`build_weekly_report.py` 的 MD 是**单份滚动**落 `PROJ/周报/白泽周报_最新.md`（每周覆盖、零历史）；AI4ME outputs 目录**只收看板 HTML**（dated + 定名版）。别再去 outputs 找 MD。（2026-06-10 修正 Scheduled SKILL.md 漂移）
- **G-02 local_prep_health.json 可能为空 `{}`**：Mac 侧 weekly_local_prep.sh 未跑成或被覆盖时如此。按"健康未知"处理——以 live store 实际新鲜度为准，不臆断 cron 成败。
- **G-03 build_weekly_report.py 验证法**：改模板后在沙箱镜像目录实跑验证（拷 PROJ 到 /tmp/verify/Documents/ 下保持 Documents 祖先名，脚本 `_documents_root()` 即自动指向镜像，不污染真实交付物）。2026-06-10 已用此法验证 06-09 改造：MD 与周日版同长、七节齐全、看板含待核验斜纹+置信徽。
- **G-04 配置权威源**：`configs/config_index.json` 为准（main_config=白泽大宗_v4.1.yaml）；CONFIG_INDEX.md 是人读摘要，曾滞后标 v3.0（2026-06-10 已同步，今后改配置两处一起动）。
- **G-05 tushare-cache 仅 27 只标的**：是白泽取数缓存，不是全市场名单，不可用于 ST 识别/全市场统计。
- **G-06 模板/artifact 字体壳分叉（技术债）**：看板 artifact `baize-weekly-dashboard` 的「系统中文衬线回退栈（Songti/STSong/SimSun）+ 去 Google Fonts 外链」只做在**产物侧手工壳**，**未并入** `_HTML_TMPL`。故每次从脚本重渲都得重套这层壳；下周日 Stage4 自动重渲若未先并模板，产出的 artifact 会缺系统回退栈（外链字体加载慢/失败时中文降级难看）。根治＝把这两项并进 `_HTML_TMPL`，让重渲直接产出 artifact 格式。（2026-07-09 涨价卡改多列时手工补壳发现）状态 ✅ 已修复（2026-11-01 Doctor Q10 批根治 · 壳已并入 _HTML_TMPL · 未参与实施的审核者代签）（注记：核据——`build_weekly_report.py` 实读 fonts.googleapis 零命中 · `--serif` 定义行＝字面栈 "Songti SC","STSong","SimSun","Source Han Serif SC",serif（无 var(--serif) 自引用）· 其余 var(--serif) 引用点均合法 · 产物 白泽周报看板_最新_20261101_Q10验证.html 无 fonts.googleapis、body font-family 字面栈在场）
- **G-07 沙箱直写挂载盘 db 留热 journal（2026-08-06 实撞）**：对本库 business_breakdown.db 直接 UPDATE，commit 半途 disk I/O error 留 41KB 热 journal，此后连只读 open 都报 disk I/O error（要回滚 journal 而写入被拦）。处置：`: > business_breakdown.db-journal` 清零 → 备份 cat 恢复 → 改库全程在 /tmp 副本做、`cat /tmp/x.db > 挂载路径` 覆写回；只读查询用 `file:...?mode=ro` URI。注意 /tmp+cat 已裁定**仅应急**（通用教训 G-X131），常规写库走停写窗口+backup API+原子替换+查并发。
- **G-08 真源 JSON 品种级 source 挂治理文本（2026-08-31 例行自查发现·当日处置）**：`data/stocks_fundamentals.json` 13/14 品种的 source 字段自 08-09 起挂着「年报/投资者问答(P0) · 待逐项标注采集日期」——「待逐项」是治理挂账文本，混进真源数据字段，随 warehouse 投影进 db 的 `benefit_relations.commodity_source`（47/48 行带挂账标记）。处置（Doctor 裁「按范本改口径」）：13 品种 source 改写为「年报/投资者问答(P0) · 披露期 2026-03~04」，核查事实留行级 `verified` 字段（30/48 行有 07-09 核查、18 行无，品种级不写核查句防以偏概全）；范本=覆铜板「2025年报(P0) · 渊图候选补采 2026-06-25」。**预防门禁**：挂账/待办文本不得进真源数据字段——治理欠账记 TODO/札记，数据字段只放事实口径；同类检查=改库前 grep 真源 JSON 的「待/暂/TODO」字样。
- **G-09 钨价 SMM 登录锁 + SVG 坐标幻觉（2026-08-31 实撞 · ✅ 已修已验）**：`commodity_prices_live.json` 钨条目出现 price=**1333 元/标吨**（yoy 算出 -99.4%）。**根因（2026-08-31 重抓证伪后定案）**：SMM h5 钨页（hq.smm.cn/h5/tungsten-ore-price）已将黑钨精矿价格列全部上登录锁（价格单元格=登录锁图、login 链接），公开页无价格数字；回退解析路径在锁定页巨型行内捞数字时，把 SVG 图标的 `transform="translate(-1333,-1165)"` **坐标值当成了均价**——row_match 没抓错行，是无数据+解析器幻觉。**放大器**：weekly_health 只查 asof 新鲜度不查量级 → 幻觉价带「age 0 新鲜」进周报/弹性（-99.4% yoy 污染钨弹性排序），健康层不暴露。**处置（已做）**：Doctor 裁「重抓」→ SMM 免费页已死重抓证伪 → 钨条目降级待核验（price/yoy 置 null·confidence 0·source 注记登录锁+SVG 幻觉·备份 .bak_20260901_pre_w_quarantine）→ warehouse 重建+看板刷新。**修法（✅ 2026-09-01 Doctor 裁「双层守卫」· CC 实施）**：① 锁定页标记检测 `_LOCK_MARKERS=("translate(","登录")`——行内命中即判无数据（探针实证：锁页 pandas 路径价格单元格=nan 已天然 fail-closed，幻觉出自回退路径 `_parse_row` 整行捞数）；② 品种量级校验 `sane_min/sane_max`（钨=50000~800000 元/标吨·历史区间），出界或缺失即拒写（fail-closed）。**证据**：持久化负向测试 `scripts/data_collection/test_smm_h5_guard.py` 9/9 PASS + py_compile 过 + probe 实跑锁页判「均价=None 日期=None」（1333 不再产出）。状态 ✅ 已修已验（✅ 2026-10-23 错题本消化 · 未参与实施的审核 subagent 落签 · 证据：test_smm_h5_guard.py 沙箱实跑 9/9 PASS·rc=0；守卫在位 fetch_smm_h5.py L100/L132；运行配置 smm_h5_map.json 钨 sane 50000~800000；备份件在 data/archived/；现网钨=315000 元/标吨（中钨在线）无 1333 幻觉价）。**候选源**（未做·待另裁）：中钨在线（免费可爬·信源图谱备选）/SMM 登录态重抓。**注**：SMM 若解锁但页面仍含 translate( 会误拒——可接受的 fail-closed 代价（跳过写留待核验，不造假价）。
- **G-10 persistence_type 全域空转 + 渊图价格层未接线（2026-09-11 发现 · ✅ 已修已验）**：看板 08-23/08-30/09-06 三期**全品种**挂「待判(渊图)」+「渊图待补」旗标。**硬证据**：`commodity_prices_live.json` 8 个鲜价品种 persistence_type 全 None；`fetch_futures_prices.py` L116 写死 None（注释「结构判断交渊图/分析」）后无任何回填者（周班 Stage 1 只对 web 补价品种写 CSV，期货品种天然漏）；`yuantu_priors_2026-09-06.json` 全 14 品种 structure 空串（08-30 版有值——agent 执行回归）。**影响面**：数据驱动结论（compute_persistence·碳酸锂 41 周结构性确认）在场却全挂「渊图待补」，误导读者以为持续性未判定；同期 AI 硬件 6 品种无信源全「待核验+旧价参考(2026-06)」，渊图价格层（prices/latest.json·09-09 更新·134 个相关 P1 点位·消费契约 price-coupling-v1 早已立）从未接线。**修法（✅ 2026-09-11 Doctor 裁「方案 A 全接」· CC 实施）**：① build_weekly_report 数据驱动兜底——persist_weeks>0 时按 persist_label 映射 type（结构性/趋势性），旗标仅剩「无 persist 数据且无 type」者；② 新 `scripts/data_collection/fetch_yuantu_prices.py` 按契约取价（scope=commodity·horizon≠预测·ttl 时效自判·映射表 BAIZE_TO_YUANTU 6 品种）+ 负向测试 `test_fetch_yuantu_prices.py` 7 例 PASS；③ MD 三·附2 + 看板「渊图价格层取数」折叠条（P1 参考不入弹性）；④ 周班 SKILL Stage 1 加 2c 步。**证据**：镜像构建 exit 0 · node --check 0 · payload 实读（碳酸锂/铜/钨=结构性·原油=趋势性·黄金维持待判·旗标仅黄金·yprices 40 条）。状态 ✅ 已修已验（✅ 2026-10-23 错题本消化 · 未参与实施的审核 subagent 落签 · Doctor 2026-10-23 问答板授权 · 证据：test_fetch_yuantu_prices.py /tmp 镜像实跑 PASS rc=0 · build_weekly_report.py L159-165 数据驱动兜底在盘〔persist_weeks>0 按 persist_label 映射 结构性/趋势性·无数据驱动结论维持待判 fail-closed〕· yuantu_price_layer.json 落盘 data/weekly/）。**预防门禁**：①「脚本写死 None 交上游填」必须有下游回填者或消费端兜底断言（本案例两层都缺）；② 已立契约（price-coupling-v1）的取数接口，新周班接入后要有负向测试防预测/陈价混入。
- **G-11 文档口径漂移族（2026-09-11 全金融审计发现 · ✅ 已修已验）**：四处事实性文档错误与真源/调度器不一致——① `README.md` L132 仍写「公司汇总弹性 = Σ(各商品净利润增幅 × revenue_ratio)」，与 2026-07-09 弹性 v2「禁净利润增幅」裁定直接冲突（弹性分=相对排序分·非利润预测）；② `configs/config_index.json` database.main 仍指 `data/business_breakdown.db`（本地库 06-15 已归档·真源=宏观库 lib_paths.BUSINESS_DB）；③ 调度时间三处漂移：概览+接手指南写周报周日 14:30/哨兵工作日 08:40/双scorer 周日 08:01，调度器实为周报周日 01:09（cron `0 1 * * 0`）/哨兵 02:40（`40 2 * * 1-5`）/双scorer 周六 22:01（`0 22 * * 6`）；④ 商品数概览正文自相矛盾（「当前数字」表 13 种 vs 09-11 更新条自写 AI 硬件 6 品种含覆铜板=14 种）。**修法（事务性·唯一最佳解）**：逐处按真源/调度注册表实况同步，待 Doctor 授权执行。**预防门禁**：改调度时间必须同步概览/接手指南/README 三处（调度注册表=真源）。**来源**：2026-09-11 全金融审计（README L132 实读 · list_scheduled_tasks 实读 · 概览内部互斥实读）· **追记 2026-09-12（Doctor 批「同意」· CC 实施）**：四处已按真源同步——① README 公式改 v2 口径（当周同比×持续性系数×信源权重×传导系数·禁净利润增幅）；② config_index database.main 指 lib_paths.BUSINESS_DB（宏观库）；③ 概览触发任务表+接手指南三处时间对齐注册表（周报 01:09/哨兵 02:40/双scorer 周六 22:01·概览加注 cron）；④ 商品数 13→14（周期 8+AI 硬件 6 含覆铜板·fundamentals.json 真源实读 14 键）+ 鲜价分母 8/13→8/14。残留 grep 零命中（实跑）。✅ 已修已验（✅ 2026-10-23 错题本消化 · 未参与实施的审核 subagent 落签 · 证据：README L132 v2 公式在位且旧公式串 grep 0 命中；config_index database.main=宏观库 lib_paths.BUSINESS_DB；概览+接手指南三处时间=注册表实读 cron 0 1 * * 0 / 40 2 * * 1-5 / 0 22 * * 6；概览 14 种·8/14；fundamentals.json 实读 14 键）。

---

## 自 Projects 侧并入（2026-11-05 · Doctor 裁 1A：brain 为 canonical）

> 以下条目逐字来自 `Projects/Financial/白泽大宗/GOTCHAS.md`（并入前 mtime 2026-11-05 06:01:27 UTC · 585 行 · sha256 前 16 位 `997da1d0a1cb31ed`），编号体系保留原样；原文件已退为指针。

<!-- 2026-09-14 错题本积压复盘（Doctor「审查并修复」批全案 · 大宗·商品数据库例行自查）：
     消化 7 条未闭环——✅ 代标 3 条（ERR-GOTCHA-028 补状态行·node --check 防御在盘 / ERR-20260819-001 window_day L251+sentinel_state=23 实落 /
     ERR-20260912-001 merge_prices L44 纯函数）；⏳→⚠️ 归一 3 条（ERR-20260719-001 / ERR-20260802-002 / NOTE-20260809-001）；
     维持 1 条（NOTE-20260819-001 ⚠️ 审计须知）。
     库结构核：business_breakdown.db integrity ok · ingest_meta 6 deprecated 已登记（commodity_prices 等停 04-05=设计状态）+ 6 ok（09-13 班全新鲜）·
     macro_prediction.db 治理良好 · 0 字节 journal 残骸已清。消化后计数：未闭环 = 0。 -->

---

## 🔴 高频 / 严重

### GOTCHA-001: 核心模块与测试位置分离

| 项目 | 内容 |
|:---|:---|
| **现象** | pytest 报 `ModuleNotFoundError: No module named 'core'` |
| **根因** | 核心模块在 `dragon-palace/src/core/`，测试在 `baize-commodity/tests/`，不在同一目录 |
| **正确操作** | 在 `tests/conftest.py` 中将 `dragon-palace/src/` 加入 `sys.path` |
| **状态** | ✅ 已修复 |
| **发现时间** | 2026-05-06 |

---

### GOTCHA-002: 测试文件 project_root 计算错误

| 项目 | 内容 |
|:---|:---|
| **现象** | `project_root = Path(__file__).parent.parent.parent` 指向错误目录 |
| **根因** | 从 `tests/core/` 出发，parent.parent 已是项目根，多算了一层 |
| **正确操作** | `project_root = Path(__file__).parent.parent`，或在 `conftest.py` 统一处理 |
| **状态** | ✅ 已修复 |
| **发现时间** | 2026-05-06 |

---

### GOTCHA-003: 配置文件路径不一致

| 项目 | 内容 |
|:---|:---|
| **现象** | 引擎找不到 `configs/commodity/白泽大宗_v4.1.yaml` |
| **根因** | 引擎从 `dragon-palace/src/core/` 解析路径，但配置文件在 `baize-commodity/configs/` |
| **正确操作** | 在 `dragon-palace/src/configs/` 创建软链接指向实际配置文件 |
| **状态** | ✅ 已修复 |
| **发现时间** | 2026-05-06 |

---

## 🟡 中频 / 影响大

### GOTCHA-004: extreme 测试配置字段不完整

| 项目 | 内容 |
|:---|:---|
| **现象** | predictor 初始化报 `ValueError: 配置缺少必需字段` |
| **根因** | extreme YAML 缺少 `cut_signals`、`hike_calc`、`macro_weight` 等嵌套字段 |
| **正确操作** | 对照 `predictor.py` 的 `required_keys` 检查配置完整性 |
| **状态** | ✅ 已修复 |
| **发现时间** | 2026-05-06 |

---

### GOTCHA-005: PredictionResult 不可 unpack

| 项目 | 内容 |
|:---|:---|
| **现象** | `recommendation, p_cut, p_hold, p_hike, condition = predictor.predict(data)` 报 TypeError |
| **根因** | `predict()` 返回 `PredictionResult` 对象（dataclass），不是 tuple |
| **正确操作** | `result = predictor.predict(data)`，然后用 `result.policy`、`result.p_cut` 等属性访问 |
| **状态** | ✅ 已修复 |
| **发现时间** | 2026-05-06 |

---

### GOTCHA-006: calculate_growth 返回字段变更

| 项目 | 内容 |
|:---|:---|
| **现象** | 测试访问 `result['growth_mid']` 报 KeyError |
| **根因** | v4.1 版本返回值改为 `{'base_growth', 'adjusted_growth', 'revenue_ratio'}` |
| **正确操作** | 使用 `result['adjusted_growth']` 和 `result['base_growth']` |
| **状态** | ✅ 已修复 |
| **发现时间** | 2026-05-06 |

---

### GOTCHA-007: 数据库文件 0 字节问题

| 项目 | 内容 |
|:---|:---|
| **现象** | `business_breakdown.db` 变为 0 字节 |
| **根因** | 进程异常终止时数据库连接未正确关闭 |
| **正确操作** | 定期检查数据库文件大小，使用 `with` 上下文管理器确保连接关闭 |
| **状态** | ✅ 已解决（2026-05-23 复检：文件大小 108KB，integrity_check=ok） |
| **发现时间** | 2026-05-05 |

---

## 📊 统计（2026-06-07 订正：按实际条目重算）

| 分类 | 数量 |
|:---|:---:|
| 🔴 高频/严重（001-003）| 3 |
| 🟡 中频/影响大（004-007）| 4 |
| 🔒 预防性（008、011）| 2 |
| 🟠 习惯/流程（009、010）| 2 |
| **总计** | **11** |

| 状态 | 数量 |
|:---|:---:|
| ✅ 已解决 | 8（001-007、010）|
| 🔁 复发已收口 | 1（008）|
| 🔒 预防性在管 | 2（008 同时在管、011）|
| ⚠️ 待人工 | Token 轮换（010）|

**收口率**: 9/11 已闭环（另 2 条为长期预防性/待人工轮换）

---

## 🔒 数据真实性铁律（2026-06-07 立 · 本项目重灾区）

### GOTCHA-012: 占位/样本数据冒充行情

| 项目 | 内容 |
|:---|:---|
| **现象** | `run_full_analysis_v4_1.py` 内嵌 `COMMODITY_DATA`/`AI_HARDWARE_DATA` 硬编码样本价（碳酸锂 +112%、稀土 400000 等），报告直接呈现，险些当真实行情用 |
| **根因（三层）** | ① demo-first 脚手架占位跑通后没拆；② `data_collection/` 抓取层从未接入主分析流（主脚本读内嵌常量）；③ 沙箱连不上 Tushare（403/无 MCP）〔注 2026-06-25：该 403 限当时；约 06-11 白名单开放后沙箱经 localhost:3128 代理 + token 已可连，见本档 GOTCHA「tushare 白名单已通」〕，"先写死让它跑"成惯性 |
| **铁律** | **宁可缺数，不可假数**：无新鲜可核验真值→留空(`—`/`待核验`)，绝不占位填充；占位数据**不入库**（含 business_breakdown.db）、**不进最终报告**；取数受阻→报"数据缺失"交 Doctor 跑真实管线，不得退化为硬编码 |
| **正确操作** | ① 主脚本价格改为从 data_collection 实时结果读取，缺失则置空+标注；② 样本仅限 dev/sample 专区且显式标"样本·非真实"；③ 每个数值带 source+asof；④ 交付前自检：报告内是否还有答不出来源的数 |
| **状态** | ✅ 铁律常驻 · 代码层 06-07 已改造 · 库层 08-09 收口（2026-11-07 未参与实施的审核者 subagent 独立复验 PASS 代签 · 证据：`run_full_analysis_v4_1.py` L36-41 注明 COMMODITY_DATA/AI_HARDWARE_DATA 已外化、全仓 `COMMODITY_DATA =` 仅 archive/_archived 旧件命中） |
| **沿革** | 🔒 铁律已立（全局 CLAUDE.md + permanent/通用教训.md）；⚠️ 白泽代码层的占位→留空/实时改造待执行（见下方"待执行"）；✅ **库数据层占位已收口（2026-08-09 P0）**——`commodity_prices`/`price_increases` 全表 26 行 `is_current` 1→0、DROP `latest_prices`/`price_trend` 两视图、行保留考古未删（脚本 `quarantine_legacy_price_data_20260809.py` · commit `08fafdc` · 快照 `bak_p0quarantine_20260809_213249`） |
| **发现时间** | 2026-06-02 首轮标记 → 2026-06-07 升格为铁律 |

> 完整铁律见 `~/Documents/Claude/brain/CLAUDE.md`「🔒 数据真实性铁律」与 `permanent/通用教训.md`「数据治理」。

---

## 🔒 预防性（AI 辅助开发模式固有）

### GOTCHA-008: 接缝债（Iterative Seam Debt）

| 项目 | 内容 |
|:---|:---|
| **现象** | 单模块工程质量高（类型注解、配置驱动、测试齐全），但跨模块接缝处全是坑：字段名对不上、量纲不统一、导了不用、实例化了不调、配置维护成两份 |
| **根因** | AI 辅助开发天然倾向"增量迭代"——每次会话都在加东西，很少有人专门花一轮做跨版本一致性回扫。龙鱼五力 v3.2→v3.3 渊图加载器降级也是同一个味道 |
| **典型案例** | `aggregate_by_company` 读错字段、`resilience` 导了不用、`elasticity_calc` 实例化了不调、`commodity_growth` 一个当百分比一个当小数 |
| **正确操作** | 每次合并/重构后跑一致性检查脚本：字段名对齐、量纲统一、死导入清理、未引用实例检查、配置单源验证 |
| **状态** | 🔁 复发→已收口（2026-06-07：第二轮审计发现仍在——引擎 analyze_stock 字段错配、生产脚本死导入引擎、配置双份。已逐项修复，check_consistency 严重项清零）|
| **发现时间** | 2026-05-23（2026-06-07 复检并修复）|

### GOTCHA-009: 密钥硬编码（习惯问题）

| 项目 | 内容 |
|:---|:---|
| **现象** | Notion Token、飞书 appSecret 明文写死在 shell 脚本和 JSON 配置中 |
| **根因** | 写脚本时顺手写死，后续没意识到风险。跟模型能力无关，纯粹是习惯 |
| **正确操作** | 凭证一律走 `.secrets/*.env` 或环境变量，`.gitignore` 第一时间配好 |
| **状态** | ✅ 已修复（2026-11-07 未参与实施的审核者 subagent 独立复验 PASS 代签 · 证据：项目内 secret/token 字面量与 40-64 位 hex grep 0 命中，`.secrets/`、`scripts/notion/`、`configs/feishu-config.json` 盘上不存在，.gitignore 四类在列；所引 GOTCHA-010 已闭环且 token 已轮换） |
| **沿革** | ✅ 代码层已修复；⚠️ 但导出 zip 仍把 .secrets 打了进去（见 GOTCHA-010），密钥轮换需手动 |
| **发现时间** | 2026-05-23 |

### GOTCHA-010: 导出/打包不遵守 .gitignore，把密钥打进 zip

| 项目 | 内容 |
|:---|:---|
| **现象** | `.gitignore` 已正确忽略 `.secrets/ *.env scripts/notion/*.sh`，但人工打包导出时按目录全量压缩，真实 Tushare Token 被打进 `4AI/_待审导出/白泽/白泽大宗-baize-commodity.zip` |
| **根因** | 打包用 `zip -r` 直压目录，绕过了 .gitignore；".gitignore 配好"≠"导出安全" |
| **正确操作** | 导出一律用 `git archive HEAD`（自动遵守忽略规则），或显式 `zip ... -x '*.secrets/*' '*.env' 'scripts/notion/*.sh'`；泄露过的 token 一律轮换 |
| **状态** | ✅ 已闭环（2026-06-07）：重打 zip 剔除密钥 + **Token 已轮换**（泄漏的为老 token，已作废）|
| **发现时间** | 2026-06-02（2026-06-07 处置）|

### GOTCHA-011: predictor 跨项目硬路径依赖兄弟目录

| 项目 | 内容 |
|:---|:---|
| **现象** | `src/core/predictor.py` 用 `parents[3]/'白泽观星'/'engine'` 把公共预测引擎接进来 |
| **根因** | 抽公共层（修 predictor 双份）时用了相对硬路径；白泽观星一旦改名/移动，大宗 predictor 立刻 ImportError |
| **正确操作** | 长期应做成可安装包或显式配置路径；至少在此登记这条隐式假设，迁移目录时同步检查 |
| **状态** | 🔒 预防性（当前路径有效，import 验证通过）|
| **发现时间** | 2026-06-07 |

---

## 🔧 周报自动化工作流（2026-06-07 排障实录）

### GOTCHA-013: Tushare token 两套约定不统一，轮换后只更一处 → 全失败

| 项目 | 内容 |
|:---|:---|
| **现象** | 龙鱼引擎全 `ENGINE_FAILED`；token 配好后又变 `找不到标的 002756.SZ`（其实是 stock_basic 鉴权失败被吞成"找不到"）|
| **根因** | 白泽 `fetch_futures` 读 env `TUSHARE_TOKEN`/`.secrets`，龙鱼引擎读 **Keychain 服务名 `tushare_pro`·账户 `doctor`** 或 `~/.tushare/token`——两套约定。轮换后只更新了一处，另一处还是失效老 token |
| **正确操作** | 统一：token 存龙鱼约定（Keychain `tushare_pro/doctor` 或 `~/.tushare/token`）一处；`fetch_futures_prices.get_token()` 与 `weekly_local_prep.sh` 都改为按"env→.secrets→Keychain tushare_pro/doctor→~/.tushare/token"顺序读，一个 token 喂两边。写文件用 `printf` 不用 `echo`（避免尾换行）|
| **状态** | ✅ 已统一（2026-06-07）|

### GOTCHA-014: Cowork 沙箱 `Path.home()` ≠ 挂载的 Documents（跨项目通用坑）

| 项目 | 内容 |
|:---|:---|
| **现象** | 渲染器在沙箱里把报告写到 `/sessions/<id>/Documents/...`（临时、用户看不到），且读不到龙鱼 latest.json → 全"待引擎" |
| **根因** | Cowork 定时任务以沙箱身份跑，`Path.home()`=`/sessions/<id>`，而用户 Documents 挂载在 `/sessions/<id>/mnt/Documents`。Mac 上 `Path.home()/Documents` 才对——所以本机测没事、定时任务翻车 |
| **正确操作** | **绝不用 `Path.home()` 定位 Documents**；改为从脚本自身位置向上找名为 `Documents` 的祖先目录（`_documents_root()`）。Mac 与沙箱都适用 |
| **状态** | ✅ 已修（build_weekly_report 的 OUT 与 _find_longyu_batch）|

### GOTCHA-015: 龙鱼 latest.json 结构 + 只有财务自动分

| 项目 | 内容 |
|:---|:---|
| **现象** | 按 `latest.json[name].total_score` 读，全 None |
| **根因** | 实际结构 `{batch_meta, packages:[{stock.name, financial_score.total(/5), valuation_context.pe_pct_3y, ...}]}`；且引擎只产**财务维度自动分**，完整六维需 LLM 评分步 `score_with_llm_apiyi.py`（未在本地 cron 内）|
| **正确操作** | 消费方按 `packages[].stock.name` 建映射，读 `financial_score.total`（标"龙鱼财务/5"）+ `valuation_context.pe_pct_3y`；完整六维待接 LLM 评分步。期货价的 `persistence_type` 留空由渊图先验填，报告显示"待判(渊图)" |
| **状态** | 🔒 已适配；六维 LLM 评分为后续增强 |

> 通用坑（GOTCHA-014）已同步登记 `brain/permanent/通用教训.md`。

### GOTCHA-016: stocks_fundamentals「赣锋锂业」ts_code 误标 002497.SZ（实为雅化集团）

| 项目 | 内容 |
|:---|:---|
| **现象** | 接龙鱼个股库后，按 ts_code 查分会把 **雅化集团(002497.SZ)** 的财务/估值贴到 **赣锋锂业** 头上 |
| **根因** | `data/stocks_fundamentals.json` 碳酸锂池中赣锋锂业 ts_code 记为 `002497.SZ`（雅化集团代码）；赣锋锂业 A 股应为 **002460.SZ** |
| **正确操作** | ①渲染层已加「名称一致性闸」(`score_of`)：ts_code 命中但分值条目记名 ≠ 本公司则退『待引擎』，绝不张冠李戴；②**待老师核**：用 `sync_longyu_universe.py --expand-universe` 以正确 ts_code(002460.SZ)修正赣锋，或确认是否本就想跟踪雅化集团 |
| **状态** | ✅ 已修复（2026-11-07 未参与实施的审核者 subagent 独立复验 PASS 代签 · 证据：`data/stocks_fundamentals.json` 赣锋锂业 ts_code=002460.SZ，L58 note「由 002497.SZ 订正为 002460.SZ · 2026-06-07」） |
| **沿革** | 🟡 渲染层已防误贴；源数据 ts_code 待老师核订 |

### GOTCHA-017: latest.json 可能指向失败重跑；逐股 reports/ 才是可用真值

| 项目 | 内容 |
|:---|:---|
| **现象** | `batch_out/latest.json`(13:32 重跑)25 只分值全空，但同日 12:13 的 `reports/five_forces_data_*.json` 有真实财务分+PE/PB分位 |
| **根因** | latest 软链指向最近一次（可能失败）批次；成功批次的逐股报告留在 `reports/` |
| **正确操作** | `sync_longyu_universe.py` 先扫 `reports/` 按时间戳取每股最新**有可用分值**者，再以 latest.json 补缺；六维总分(/100)仍须 LLM 评分步，缺则留『待引擎』 |
| **状态** | ✅ 已适配（connector ingest 逻辑）|

### GOTCHA-018: 钨价『元/标吨』vs『元/吨』量纲冲突（27.7万 vs 44万 vs 104万 之谜）

| 项目 | 内容 |
|:---|:---|
| **现象** | web 检索钨精矿价跨度离谱：27.7万 / 44万 / 104万，无法判真 |
| **根因** | SMM 报『元/**标吨**』(标准吨=折 100% WO₃ 当量)，中钨在线/部分媒体报『元/**吨**』(实物吨)，两者差一个品位折算系数；混用即冲突 |
| **正确操作** | 统一以 **SMM `hq.smm.cn/h5/tungsten-ore-price` 黑钨精矿≥65% 元/标吨** 为准(`fetch_smm_h5.py` 已抓)；同比用同源同单位序列(本地历史 smm_history.jsonl，缺则 config 锚 2025 年均 21.79万/标吨)。本周值: 50.05万/标吨(06-05, P1, 置信60%) |
| **状态** | ✅ 已接 SMM h5 爬取器；钨入库覆盖 8/13 |

### GOTCHA-019: AKShare 大宗现货只覆盖『有期货品种』，不解无期货缺口

| 项目 | 内容 |
|:---|:---|
| **现象** | 期望 AKShare 补稀土/钨/特气，实测补不了 |
| **根因** | akshare `futures_spot_price*` 取生意社「有期货品种」现货(算基差用)，无稀土/钨/氦/六氟化钨/小金属专用接口；沙箱亦被生意社 403 墙 |
| **正确操作** | 无期货品种走 **SMM h5**(`fetch_smm_h5.py`)；AKShare 连接器已归档 `archive/deprecated_sources/`，仅留作未来工业硅/多晶硅现货+基差 |
| **状态** | ✅ 已归档并替换 |

### GOTCHA-020: 沙箱裸 http.client 不认代理 env → 被引擎吞成「找不到标的」

| 项目 | 内容 |
|:---|:---|
| **现象** | tushare 白名单已通(curl/SDK 都行)，龙鱼 batch 在沙箱仍成批 `ENGINE_FAILED`/「找不到标的 002378.SZ」 |
| **根因** | 沙箱出网必经 `https_proxy=localhost:3128`；curl/requests/tushare SDK/urllib 自动走代理，但引擎 `five_forces_engine_v3.py` 用裸 `http.client.HTTPSConnection` 直连 → DNS 失败 → `call()` 返回 ok=False 被标的校验吞成「找不到标的」（GOTCHA-013 同款掩蔽，根因不同）|
| **正确操作** | 引擎 `_connect` 已加补丁(2026-06-11)：有 `https_proxy` env 则 CONNECT 隧道，无则原直连(Mac 零影响)。今后沙箱排查顺序：先 curl 验白名单+token → 再怀疑代理穿透 → 最后才是 ts_code |
| **状态** | ✅ 已修复 |

### GOTCHA-021: 沙箱 bash 每条命令独立 bwrap，nohup 后台进程不跨调用存活

| 项目 | 内容 |
|:---|:---|
| **现象** | `nohup batch_score.py ... &` 后下一条命令查日志——文件不存在，进程无影 |
| **根因** | 每条 bash 调用独立 bwrap 沙箱 + `--die-with-parent`，调用结束即杀全部子进程；只有文件系统跨调用持久 |
| **正确操作** | 长任务**分片**：每条调用同步跑完一小块（龙鱼 batch 每次一只股 `timeout 43`，约 40s/只）；绝不用「后台跑+下条轮询」 |
| **状态** | ✅ 已写入 baize-weekly-report SKILL Stage 0.5 |

### GOTCHA-022: 沙箱白名单是会话启动快照，会话中途加域名当场不生效

| 项目 | 内容 |
|:---|:---|
| **现象** | Doctor 加完 hq.smm.cn/api.deepseek.com 白名单，当前会话 curl 仍被代理 403；而 tushare（会话开始前加的）一直通 |
| **根因** | 沙箱代理的放行规则在会话（VM）启动时固化；中途变更不热加载 |
| **正确操作** | 加白名单后到**新会话**验证（定时任务每次跑都是新会话，天然生效）；无人值守脚本步骤前置 curl 自检，403 即走回退路径 |
| **状态** | ✅ 已写入 SKILL 自检守卫 |

### GOTCHA-023: deepseek-v4-pro 思维链默认开，六维单票 >45s 必撞沙箱上限

| 项目 | 内容 |
|:---|:---|
| **现象** | 沙箱跑 [4] 六维（score_with_llm_apiyi.py → Deepseek anthropic 端点），降 max_tokens 8000→3000 仍超时；16-token 探针 2.3s 返回且 content 是 `thinking` 块 |
| **根因** | `deepseek-v4-pro` 是推理模型，Anthropic 协议下思维链**默认开启**；慢在思维链生成（数千 token），与网络/max_tokens 无关 |
| **正确操作** | 请求体加 `"thinking":{"type":"disabled"}` → 单票 ~22s。`call_apiyi()` 已打补丁（2026-06-11）：base_url 含 deepseek 才加此参数，APIYI/Claude 路径零影响 |
| **状态** | ✅ 已修复（4 家订正股实测 22-24s/只；6/14 [4] 首验应顺畅） |

**⚠ 追记（2026-07-31 · 实测 · 关键是「勿收窄判据」）**

考虑切 `deepseek-v4-flash` 时跑了三组对照探针（`scripts/automation/probe_deepseek_model.py`，走生产同款 `/anthropic/v1/messages` 请求体）：

| 组 | 模型 | `thinking` | 结果 | `content` 类型 | in/out tokens |
|---|---|---|---|---|---|
| A | `deepseek-v4-flash` | `disabled` | ✅ 200 · 1.27s | `['text']` | **12 / 1** |
| B | `deepseek-v4-flash` | 不传 | ✅ 200 · 1.39s | **`['thinking','text']`** | **91 / 16** |
| C | `deepseek-v4-pro` | `disabled` | ✅ 200 · 1.26s | `['text']` | 12 / 1 |

**① `flash` 同样是推理模型、思维链默认开**（B 组吐 `thinking` 块）。⇒ 上面「正确操作」里 `call_apiyi()` 的判据「**base_url 含 deepseek 就加此参数**」对 flash **依然正确**，**切勿收窄成「且 model 含 pro」**——那样等于给 flash 关掉补丁，单票耗时打回 45s 撞沙箱上限，本条坑原样复发。（立此条时的直觉预设恰恰相反：以为 flash 不是推理模型、补丁该收窄。实测推翻。）

**② 思维链的 token 代价首次量化**：同一个 trivial 问题，开/关思维链 **输入侧 91 vs 12（7.6×）、输出侧 16 vs 1**。本条原文只记了耗时，没记成本；六维那种长 prompt 上这是实打实的钱。

**③ 顺带澄清一个前提**：DeepSeek 文档「Responses API 仅支持 `deepseek-v4-flash`，`pro` 待 2026-08 初」说的是 **`/responses` 端点**（为 Codex 而设），与本项目走的 **`/anthropic/v1/messages`** 是两条独立的路——C 组实测 pro 在本端点仍可用。**故不存在「被迫迁移」**；2026-07-31 评估后维持 `KG_MODEL=deepseek-v4-pro`（配在 `~/Documents/Database/.env`）。

**④ 配置侧同日修**：`scripts/automation/weekly_local_prep.sh` 此前只从 `.env` 读 `KG_API_KEY`、**不读 `KG_MODEL`**，而 `docs/WORKFLOW_周报自动化.md` 却写着「如需改在 .env 里设」——那句一直是空头支票。现已补上三档取值（环境变量 → `.env` → 内置兜底 `deepseek-v4-pro`），换模型只动 `.env` 一行。

**来源** → `brain/logs/2026-07-31-US10Y口径终查与TODO五条失效前提-0937.md` 同场后续 · 探针脚本 `scripts/automation/probe_deepseek_model.py`

### GOTCHA-025: Gangtise EDB 滚动一年窗，越界查询报误导性「410006 时间格式错误」

| 项目 | 内容 |
|:---|:---|
| **现象** | `edb-data` 取 2024-05→2025-05 报 `410006 时间格式错误`（格式与成功调用完全一致）；另一窗口从 2025-05-01 请求，首行却是 2025-06-30 |
| **根因** | EDB 数据保留约滚动一年；start-date 越过窗口边界即拒，错误码与「时间格式」无关，纯误导 |
| **正确操作** | ①同比基线**赶早自存本地**（如 `data/weekly/optical_customs.csv` 已存 2025-06 光模块海关基线），别指望 EDB 回溯；②月度海关数据约 T+45 天发布；③遇 410006 先怀疑越界而非格式 |
| **状态** | ✅ 已规避（基线落本地，2026-07 起严格同比自给） |

### GOTCHA-024: SMM h5 对 curl 返回压缩流，不加 --compressed 会误判「页面无内容」

| 项目 | 内容 |
|:---|:---|
| **现象** | 沙箱 curl 抓 hq.smm.cn/h5/* 返回 200 + 百 KB 响应，但 grep 中文/价格全空，疑似 JS 空壳。**2026-06-14 复发升级**：`fetch_smm_h5.py --fetch` 钨/稀土全『未解析到，跳过』，一度误判「SMM 改版/登录墙」。**2026-09 再复发（gzip 修复后新态）**：`--fetch --merge` 对钨页报「未解析到 黑钨精矿≥65% 均价，跳过」，稀土摘除后仅钨仍挂失败——连续三周（09-13/09-20/09-27 周报 health 实据）走 web 补价兜底（中钨在线/生意社），说明页面结构或 row_match 模式又变，与 gzip 无关 |
| **根因** | curl 默认带 `Accept-Encoding` 时服务器返回 gzip 流，落盘是二进制；并非页面无数据——价格其实以内嵌 JSON（`product_name/average/renew_date`）直出。**2026-06-14 升级**：SMM h5 如今对**裸 urllib（不声明 Accept-Encoding）也无条件返回 gzip**——GOTCHA-024 原假设「urllib 路径通常不受影响」已不成立；`fetch_smm_h5._get` 只 `r.read().decode('utf-8')` 不解 gzip → 二进制硬解成乱码 → row_match 找不到「黑钨精矿」→ 误判页面无内容 |
| **正确操作** | curl 探页一律加 `--compressed`；**所有 urllib 取 SMM 的函数都必须按 `Content-Encoding`/gzip 魔数(`\x1f\x8b`)解压**——`fetch_smm_h5._get` 已补（2026-06-14，gzip+deflate 容错）。诊断口诀：SMM 返 200 却解析空时，**先怀疑 gzip 未解，别先怀疑改版/登录墙**（白泽 6/14 首验差点栽这） |
| **状态** | ✅ 已修复（2026-11-07 未参与实施的审核者 subagent 独立复验 PASS 代签 · 证据：diff `configs/_bak/smm_h5_map.json.bak_2026-11-07_12A` 仅 mappings→[] / 钨整条入 `_retired_mappings` / 新增 `_变更_20261107` 注；审核者独立实跑 `python3 -B scripts/data_collection/fetch_smm_h5.py --fetch` → 「未取到可写现货价」rc 0，`data/weekly/smm_fill.csv`、`smm_history.jsonl` mtime/size 前后不变） |
| **沿革** | 🔄 已修待验（2026-11-07 Doctor 裁 12A：钨 SMM h5 退役、以 web 源为记录源——`configs/smm_h5_map.json` mappings 置空、钨条目移入 `_retired_mappings` 留档（仅改配置、不改代码）；沙箱实跑 `fetch_smm_h5.py --fetch` 零映射→「未取到可写现货价」rc 0、不再对钨报 SMM ✗；钨价按 SKILL Stage 1 web 补价（中钨在线/生意社 P1）。gzip 容错已修·2026-06-14 验证通过；09-13 起钨页 row_match 失配史见上） |

### GOTCHA-026: SMM 稀土 row_match『氧化镨钕』先命中 SEO 文章标题 → 抓到错数

| 项目 | 内容 |
|:---|:---|
| **现象** | gzip 修好后 `fetch_smm_h5` 稀土解出 **1240 元/吨 · 同比 -99.8%**（实价应 ~70万/吨），被 merge 写进 live store，险违铁律 |
| **根因** | `rare-earth-metal-oxides-price` 页顶部有 SEO 月度分析文章标题含「氧化镨钕」（如『淡季拖累5月稀土价格 氧化镨钕、氧化镝跌幅显著』），子串 row_match 先命中标题、抓到邻近无关数字；真正的价格表行未被取到。钨页（黑钨精矿≥65%）无此问题、结构稳 |
| **正确操作** | 稀土**移出 `configs/smm_h5_map.json`**（2026-06-14 新建实配覆盖 sample，只留钨）；稀土非持仓重点、走 web/旧价即可（老师 2026-06-14 定）。如日后要恢复稀土：row_match 须收紧到价格表行（排除 `<a href=.../content/...>` 文章块），或改按内嵌 JSON `product_name=="氧化镨钕"` 精确取 `average` |
| **状态** | ✅ 已规避（稀土摘除 + live store 还原为 web 值 69.75万/05-21）；稀土精确解析为可选后续增强 |

### GOTCHA-027: 沙箱挂载盘禁删文件 → sqlite 直写报 `disk I/O error`

| 项目 | 内容 |
|:---|:---|
| **现象** | Cowork 沙箱内对挂载盘（~/Documents 映射）的 `.db` 用 sqlite3 直写，建表即 `sqlite3.OperationalError: disk I/O error`；只读（`?immutable=1`）正常。中止后还在真机盘留下 hot `-journal` |
| **根因** | 该挂载盘 bash **允许建文件、禁止删文件**（`rm` 报 `Operation not permitted`）。sqlite 事务要建并删 rollback `-journal`，删不掉 → I/O error。注意这是**沙箱挂载层**限制，真机 APFS 上 sqlite 一切正常（现有库即真机写出） |
| **正确操作** | 别在沙箱对挂载盘 .db 直写。两条路：①本地 `/tmp` 拷副本→跑通→`cp` 回（纯 cp 不涉删除，挂载盘可写）；②交真机终端跑。warehouse ingest 即走真机（接手指南 Stage 5）。**遗留清理**：中止留下的 `-journal`、沙箱建的临时 .db 沙箱删不掉，须真机 `rm`（建文件/cp 可在沙箱，仅删除受限） |
| **状态** | ✅ 已根治（2026-06-22：`build_warehouse.py` 自动 /tmp 暂存回写，沙箱单轨自落库；下游连锁与根治详 GOTCHA-028） |

### GOTCHA-028: 中止留下的 hot `-journal` 让"只读"打开也报 `readonly database` → 看板误判断链；build_warehouse 自动 /tmp 回写根治

| 项目 | 内容 |
|:---|:---|
| **现象** | Brain Vault 看板「数据库新鲜度」白泽大宗-商品长期断链；snapshot 以 `?mode=ro` 读 `business_breakdown.db` 报 `attempt to write a readonly database`。库 integrity ok，却连只读都打不开——库旁残留一个与库同时间戳的 `-journal`（6/21 周更写库被 GOTCHA-027 挂载盘 I/O 打断、事务未提交）|
| **根因** | sqlite 打开带 hot `-journal` 的库**必须先回放日志回滚**，而回滚要**写**库；`mode=ro` 写不了 → 报 `readonly database`（非权限问题，是回滚被只读挡住）。任何只读消费者（看板/巡检）全被挡，表象=「断链」。是 GOTCHA-027（挂载盘直写 I/O）的**下游连锁**：直写中止→留 hot journal→只读侧全废 |
| **正确操作** | ①**应急复原**（真机）：备份库+journal → `sqlite3 库 "PRAGMA integrity_check;"`（rw 打开触发回滚+删 journal，打印 ok 即净）。②**根治**（已落）：`build_warehouse.py` 加挂载盘直写兜底——撞 `disk I/O error`/`readonly` 时自动「拷 /tmp→副本上 ingest（顺带回滚 journal）→残留 journal **截断为 0 字节**（挂载盘禁删但可截断·0 字节=无需回滚·无害）→ /tmp 整库 cp 覆盖回写」。沙箱单轨从此自落库，不再每周手动补跑。③真机跑则 journal 正常删除、更干净。④顺带：同款「禁删」也让沙箱 git 留 `.git/index.lock`（陈旧空锁卡 commit），真机 `rm -f .git/index.lock` 即解 |
| **状态** | ✅ 已根治（2026-06-22：自动 /tmp 回写·真实挂载库实测兜底触发+回写成功·integrity ok·幂等不误伤既有表；应急复原流程已验）|

### GOTCHA-029: `business_breakdown` 双关——库文件名 == 库内 SQL 表名，改名禁全局替换

| 项目 | 内容 |
|:---|:---|
| **现象** | 要把库**文件** `business_breakdown.db` 改名时，全仓 grep `business_breakdown` 命中一大片，若无脑 `sed s/business_breakdown/新名/g` 会把库**内表名** `business_breakdown` / `business_breakdown_history` 一起改掉，污染 schema、所有 `FROM business_breakdown` SQL 当场失效 |
| **根因** | `business_breakdown` 是**双关**：既是库文件名（`...宏观-大宗商品/business_breakdown.db`），又是库内核心 SQL 表名（`business_breakdown` 受益关系表、`business_breakdown_history` 历史表）。两者无任何关联，但同名 |
| **正确操作** | 改库文件名只动**路径字面量**，绝不碰裸 `business_breakdown` 表 token。路径收口在 `scripts/lib_paths.py`（SSOT，改一处覆盖 8 个消费脚本）；但 `lib_public_read.py`、`configs/config_index.json`(`"main"`)、`tests/*`、烛照 `tools/fundamentals_lookup.py`、brain `.tools/dashboard-snapshot.py` 各带独立路径字面量须逐一改。**改名前先 `sqlite3 库 ".tables"` 确认有无与文件同名的表** |
| **状态** | 📌 已记录（2026-06-29 海螺看板改名时勘出；当次最终只改看板显示名、未做物理改名，故白泽侧未触发，留作日后真改名的护栏）|

---

## 📝 更新日志

| 日期 | 更新 |
|:---|:---|
| 2026-05-07 | 创建，录入 7 条历史教训 |
| 2026-05-23 | +GOTCHA-008（接缝债）、+GOTCHA-009（密钥硬编码），统计更新 |
| 2026-06-07 | 第二轮审计：GOTCHA-008 标复发并收口；+GOTCHA-010（导出泄密）、+GOTCHA-011（predictor 硬路径）；统计订正 |
| 2026-06-11 | 四域名白名单开通、cron 四步全迁沙箱：+GOTCHA-020（裸 http.client 不认代理）、+GOTCHA-021（nohup 不跨 bash 调用存活）、+GOTCHA-022（白名单=会话快照） |
| 2026-06-11 | 白名单新会话自检通过；4 家订正股六维补跑完成；+GOTCHA-023（deepseek-v4-pro 思维链超时→call_apiyi 补 thinking disabled） |
| 2026-06-12 | HVLP-Gen4 接 SMM 铜箔加工费代理价（探价注记层·老师裁决）：+GOTCHA-024（SMM h5 curl 须 --compressed）；新连接器 fetch_smm_copper_foil_probe.py |
| 2026-06-12 | 铁律修订（老师定）：①旧价/代理价必标具体时点+已过天数（>30 天标『过期』）；②旧价参考**可入弹性测算**〔旧价口径〕，前提是有真实同比基线（probe.yoy），无基线弹性留待核验。渲染器双端+探针+接手指南+信源图谱已同步 |
| 2026-06-15 | 汇总只读层：新增 `scripts/database/build_warehouse.py`（warehouse·6表·additive·周快照累积）+ SKILL Stage 5；+GOTCHA-027（沙箱挂载盘禁删→sqlite 直写报 disk I/O error；/tmp 跑通拷回 或真机跑） |
| 2026-06-14 | 周日双轨首验：GOTCHA-024 升级（SMM h5 对裸 urllib 也无条件 gzip，`fetch_smm_h5._get` 补 gzip 容错→钨解出 52.75万/06-12）；+GOTCHA-026（稀土 row_match 命中文章标题抓错数→稀土摘除走 web）；Mac cron 因『Operation not permitted』全废→老师定**直接退役 cron**，主轨 Cowork 单轨独立兜住 |
| 2026-06-22 | GOTCHA-027 根治：`build_warehouse.py` 加挂载盘直写自动 /tmp 回写（撞 I/O 时拷 /tmp→ingest→残留 journal 截断为 0→cp 覆盖回写）；+GOTCHA-028（hot journal→只读报 readonly→看板断链；应急复原 + 自动回写 + 0 字节 journal + index.lock 顺带）|
| 2026-06-29 | +GOTCHA-029（`business_breakdown` 双关：库文件名==SQL表名，改名禁全局替换·只动路径字面量）——海螺看板「大宗基本面库→大宗·商品数据库」改名时勘出；当次最终只改看板显示名+连线，物理库/脚本未动 |
| 2026-06-24 | **SMM 三坑结案核实**：海螺资产看板 `SMM/web补价` 那条「沙箱代理墙·gzip容错坑·SEO标题误命中」经核=陈旧汇总——gzip=GOTCHA-024（已修·魔数兜底解压）、SEO标题=GOTCHA-026（稀土摘走 web 已处置·现行只抓钨）、代理墙=设计约束（沙箱抓不到→Mac 跑·非 bug）；钨补价正常（asof 2026-06-18/fetched 06-21）。已把 `海螺姑娘/data/asset_manifest.json` 该节点校正 `status=healthy`·`issues=[]`·freshness 重写（看板 Reload 即转绿）|

## [ERR-GOTCHA-028] 看板模板 JS 重复声明 → 全板白屏

**状态**: ✅ 已修（2026-09-14 复盘补标 · node --check 防御实读在盘 build_weekly_report L849-856 · Doctor 批全案 · CC 代记）

- 2026-07-09 版式改造(三级分级)时新段落重复 `const attribBy`，SyntaxError 杀死整段脚本，看板空白。
- 防御: build_weekly_report 渲染后自动 `node --check` 内嵌 JS(语法坏则🟥告警)；改模板新增顶层 const 前先 grep 既有声明。

## [ERR-20260719-001] 沙箱 web_fetch provenance 限制封死东方财富公告 API 兜底路
**状态**: ✅ 已修复（2026-11-07 未参与实施的审核者 subagent 独立复验 PASS 代签 · 证据：diff `live/baize-weekly-report/_bak/SKILL.md.bak_2026-11-07_11A`→`_12A` 仅 L80-86→L80-82 降级链段；`_12A`→现行仅 L33 一句 12A 注；全文已无「web_fetch 东财 API 自拼」路径为主路、旧路仅作 parse 复用注）
**沿革**: 🔄 已修待验（2026-11-07 Doctor 裁 11A：环境已变、SKILL 降级链已改——baize-weekly-report/SKILL.md Stage 2 第 2 级改为「WebSearch 取到公告页 URL → WebFetch 直取；取不到按原 fail-visible 报缺」；10-11 已有 21 份公告实取）
**优先级**: 🟡 中
**触发场景**: Stage 2 双面交叉验证，WebSearch 可用但欲用 P1 公告面兜底，按 SKILL 走 `fetch_announcement_evidence.py urls` → 对打印的 url 调 `mcp__workspace__web_fetch`。
**错误信息**: `URL not in provenance set. web_fetch can only retrieve URLs that appeared in a user message, a prior web_fetch result, or a WebSearch result.`
**解决方案**: 本轮回退到 SKILL 三级降级的第 1 级（WebSearch），按商品分组做主题检索（每组 1 次覆盖 2-3 家），19 家全部取到双面证据，crossval gate 一次通过。
**预防措施**: 脚本自行拼装的 URL 不在 provenance 集内 → 公告 API 兜底**只在 URL 曾出现于 WebSearch 结果时可用**。SKILL 中「WebSearch 拒返 → web_fetch 公告兜底」的降级链在本环境不成立，应改为：WebSearch 拒返时先用 WebSearch 搜到公告页 URL 再 fetch，否则直接走第 3 级（沿用旧 crossval 并如实声明）。

## [ERR-20260719-002] 原油同比继承了不可靠的美元基线，跨口径误算 +26.1%（实为 +1.2%）
**状态**: ✅ 已解决
**优先级**: 🔴 高（数据真实性铁律相关）
**触发场景**: Stage 1 补价。历史 CSV 注记写「同比基线沿用 EIA 2025-06 月均 $69.85（方法同上期）」，本周照抄该基线、以 Brent 点价 88.09 算得 YoY +26.1% 写入 store，并据此让中国海油/中国石油/石化油服进入受益传导。
**错误信息**: 无报错。build_weekly_report 把原油划进「静默区」并标注「实测同比 -12.8%」（取自 persistence_metrics 的 Tushare SC.INE 同口径序列），与 store 的 +26.1% 正负相反 —— 是渲染层的口径打架暴露了问题，而非任何校验器拦住。
**解决方案**: 直接查 Tushare `fut_daily(SC.INE)`：2026-07-17 收 510.5 元/桶，2025-07-22 收 504.3 元/桶 → 同口径 YoY = **+1.2%**（环比 +0.1%）。以 P0 同口径序列覆盖 store，并在 source 里保留更正说明；同步把三家油企 crossval 的 refute 首条改为口径更正、中国海油由「成立」降为「存疑」。
**预防措施**:
1. **跨口径同比一律不可信**：`点价 vs 月均`、`Brent(美元) vs SC(人民币)` 都不是同比。凡 store 里同比的分子分母不同源/不同频，credibility 上限 P2 且 confidence ≤40，不得驱动弹性。
2. **「方法同上期」是污染放大器**：继承的基线若从未被独立核过，会逐周复制。凡 source 里出现「沿用/方法同上期」，本周必须重新验一次基线，验不动就降级为『待核验』。
3. **有 Tushare 就别用 web 估**：SC.INE/LC.GFE/CU.SHF/AU.SHF 均可 P0 直取同口径同比，优先级高于任何 web 点价拼算。

**追记（2026-09-11 · VV 独立审计确认复发 · CC 实读 live JSON 复核）**: 本条的预防措施 1（跨口径同比不得驱动弹性）在 09-06 期产物仍未生效——`commodity_prices_live.json` 实读：稀土 change_yoy=27.6%（生意社 09-04 点价 727500 vs 中钨在线 2025-08 月均 570095 · **点价vs月均** · confidence 60）、钨 change_yoy=79.2%（卓创**周均价** vs 中钨在线 2025-08-26 **单日点价** · **跨源跨频** · confidence 65）。两者仍标 P1 入弹性候选集；09-06 Artifact culled 区含章源钨业弹性 53.5/厦门钨业 36.4/中国稀土 22.6（当期被市场确认/离场条件剔除未成入选建议，但不合格分数已进入动态中位门槛样本，仍可能影响其他候选筛选）。另发现 `fetch_futures_prices.py` 把 asof 写为**执行当天**而非最后交易日（09-06 周日生成的铜/金/锂 asof=09-06）。**修法候选（VV 建议+CC 同意·待 Doctor 裁）**: 分子/基线分别保留 series ID+日期+频率+单位+品级，只有匹配才生成同比；不匹配则降级「跨口径参考变化」退出弹性分与动态门槛样本；asof 分列最后成交日期与采集时间。

**实施留痕（2026-09-11 晚间 · Doctor 批「三项全开工」· CC 实施 · 状态 🔄 已修待验·实施者不自签 ✅）**:
1. `commodity_prices_live.json`：钨/稀土/六氟化钨标 `yoy_comparable:false`（六氟化钨基线源未注明·保守 false 待补同源基线）、原油 true；期货三品由脚本生成 true。
2. `fetch_futures_prices.py`：asof 改最后交易日（df.trade_date 末行）+ 写 yoy_comparable=True。
3. `refresh_commodity_prices.py --from-csv`：新增 CSV 列 `yoy_comparable`（缺省 False fail-closed）。
4. `src/core/data_source.py` `build_commodity_dataset`：透传 `yoy_comparable`（缺省 True·兼容旧条目）。
5. `build_weekly_report.py`：三处 gate——`_invest_tier`（跨口径降观察区+why 标注）、`enrich_priced`（退出弹性分与 _els_all 门槛样本）、`commodity_attrib`（ref_only 条目·MD/HTML 双端显「跨口径参考变化·未入弹性」）。
6. `run_full_analysis_v4_1.py`：priced/review 两路同 gate。
7. 周班 SKILL Stage 1 加 yoy_comparable 必填说明（staging `~/Documents/_staging_baize_skillaudit_yoyflag_2026-09-11_SKILL.md` · store 部署走 Doctor 终端。**2026-09-12 注记**：该 staging 已随根目录清场归档至 `brain/archived/staging_2026-09-12/`，store 部署早前已执行，本注记仅路径迁移留痕）。
8. **验证（G-03 镜像法实跑）**：/tmp/verify_yoyflag_20260911 镜像 build exit 0——MD/HTML 双端 3 处「跨口径参考变化·未入弹性」；**动态门槛 22.6→21.4**（跨口径样本退出后中位变化）；受益榜 Top20 无钨/稀土系；剔除名单无弹性分理由残留；py_compile 全绿。
**待验**：09-13 周日班自然验证（SKILL 新列+代码 gate 全链）；✅ 归 Doctor/VV 独立验收。

**追记（2026-09-11 深夜 · VV 独立验收后修复 · 状态 🔄 已修待验·第二轮）**: VV 验收四负例（缺旗标/null/字符串"false"/旧价 probe 回退）全部重新计分、门槛升至 24.2——根因=① `data_source` 缺省 True 放行 + ② gate 只排布尔 False + ③ probe 回退不核可比性 + ④ 首屏价格锚/价表/快照未传播身份。已修：① data_source 缺省改 **None（unknown）**、gate 全链改 **`is not True`**（只有规范布尔 True 入弹性；缺旗标/null/字符串全挡）；② probe 回退加 `p.get("yoy_comparable") is True` 判定（fail-closed）；③ live JSON 期货三品补显式 true；④ 可比性身份传播——price_list/comms 加 `cmp` 字段（HTML payload 14 处）、首屏价格锚优先可比项（无可比项才用参考项并标「（参考）·不确认连续同比趋势」）、MD 价格表同比列标「（参考）」；⑤ run_full_analysis 持续性表/核心结论同 gate（L243/L271）。**五用例镜像复现（/tmp/verify_yoyflag2_20260911）**：①-⑤ 全部门槛维持 21.4、钨段「跨口径参考变化·未入弹性」、无弹性分数字残留、剔除名单无钨系——与 VV 验收基线一致。py_compile 5 文件 ✓、live JSON 合法 ✓。**SKILL 部署勘误（VV 验收指出）**：目标 SKILL 与 staging 已同字节（SHA `ceb38eb5…`）——此前「未部署」表述不成立；`preYoyFlag` 备份命令先覆盖后备份、备份件即新版，**不能提供旧版回退**（若需旧版应从可证明版本的历史来源恢复）。staging 件与目标一致，无需重复部署。
**追记（2026-09-11 深夜 · VV 第二轮复验后修复 · 状态 🔄 已修待验·第三轮）**: VV 二轮缺口——① fetch 路径（`refresh --from-fetch`）未透传上游旗标 → 已加 `yoy_comparable` 透传（上游无声明→False fail-closed）；② 合格旧价 probe 被误拦 → probe 判定改「显式 False 才拦、缺失按旧价口径合同放行」+ **enrich_priced 顺序重排**（probe fallback 先于可比性闸——此前 `is not True → continue` 抢在 needs_review 分支前，把无价商品永久拦在 probe 路径外）；③ 价卡「已入弹性(旧价口径)」表述 → 改「有同比基线（是否入弹性以受益榜为准）」。**镜像复验（/tmp/verify_yoyflag3_20260911）**：probe 无声明 → 放行（门槛 24.2·章源离场线剔除）；probe 显式 false → 拦（门槛 21.4·不进 culled）——两方向一致。
**追记（2026-09-12 · VV 第三轮复验后修复 · 状态 🔄 已修待验·第四轮）**: VV 三轮缺口——① 普通价卡未消费可比性（pcard 仍显「同比+连续N周>20%·结构性确认」）→ pcard 加 `isRef=r.cmp!==true`：同比值标「(参)」、persistLine 替换为「参考变化·未入弹性（跨口径）」不显示连续同比确认（首屏/价卡/详情同一资格）；② from_fetch 真实类接口不匹配（`fetch_all` 不存在·真实类为 `fetch_all_commodities` 分组字典）→ 明确 ⛔ unavailable 提示 + 返回空（不接模拟数据·main 已有空 rows 不写 store 守卫）；③ probe 非法值与缺失混同 → 判定改「`"yoy_comparable" in p` 且非 True → 拦（含 null/字符串 false/数字 1）；键缺失 → 旧价口径合同放行」；④ CSV 模板（--template）补 yoy_comparable 列+口径说明。**镜像复验（/tmp/verify_yoyflag4_20260912）**：缺失→放行 24.2 · null/字符串false/数字1→全拦 21.4 四用例一致 + py_compile ✓ + pcard isRef 模板在盘。

**2026-09-12 VV 本次存量价回读**：live JSON 本次快照中铜/黄金/碳酸锂 asof 仍为 2026-09-06（周日），yoy_comparable 均为规范 True；代码已经改为最后 trade_date，不代表旧存量身份已修。本轮不调用行情接口、不猜应改成哪一交易日；建议获批后按真实原序列重新生成，保留采集时间与观察日区别。钨/稀土/六氟化钨 flag 当前均为 false，本轮不复述它们仍入弹性为当前事实。快照与 request_id 见 `/Users/lunarabbit/Documents/AI4ME/Financial-Audit-outputs/harness-rollout/五项目注册与自检_20260912/trial-results.json` baize_live；不据采集日推断交易数据断更。

## [GOTCHA-20260728-001] 弃用表在 ingest_meta 残留 ok 状态 → 被审计当成「断供 30 天」误报
**状态**: ✅ 已定性（2026-07-28 全金融审查勘误）｜ **优先级**: 🟡 中
**现象**: `business_breakdown.stock_scores` 于 2026-06-29 领域分库时刻意弃用（镜像表不再构建/刷新·冻结保留可逆·build_warehouse.py L58/L280），但 `ingest_meta` 仍留有该表 `status='ok', last_success=2026-06-28` 的行、无 deprecated 标记——审查 agent 据元数据判「摄取停摆 30 天」，误报为 P0 断供。真链路：白泽/烛照九阴均直读龙鱼库真源 `龙鱼-标的分析库/records/`（07-26 活·104 只），评分全程健康。
**教训**: 弃用一张表 = 三件事一起做：①停构建 ②源码注释 ③**清理/标注元数据与监控注册**（ingest_meta、_health、MANIFEST）。只做前两件，死表就会伪装成事故，浪费未来审查者（包括 AI）的判断。
**待办（提案·待 Doctor 批）**: ingest_meta 的 stock_scores/fundamentals 行标 `deprecated` 或删除（一条 UPDATE/DELETE·跑前备份）。

## [ERR-20260802-001] 沙箱共享 /tmp 残留他属文件 → 硬编码 /tmp 路径的脚本 PermissionError
**状态**: ✅ 已绕过（脚本未改，运行时替换）
**优先级**: 🟡 中
**触发场景**: 2026-08-02 周任务 Stage 1.6 与 Stage 5。沙箱 `/tmp` 为多会话共享目录（drwxrwxrwt，属 nobody:nogroup + sticky bit），上一轮会话（2026-07-26）留下的中间文件仍在，且属主为 `nobody` —— 本会话用户既不能覆盖也不能删除。
**错误信息**:
- `compute_persistence.py`：`⚠️ warehouse 快照读取失败：[Errno 13] Permission denied: '/tmp/_bb_ro.db'` —— 不报错退出，但**静默丢掉快照类商品**（稀土/钨/六氟化钨/氦气的 persist_weeks 全部缺失，只剩 4 个期货品种）。
- `build_warehouse.py`：`PermissionError: [Errno 13] Permission denied: '/tmp/baize_warehouse/business_breakdown.db'` —— 挂载盘直写先报 `disk I/O error`（GOTCHA-027 老问题）走 /tmp 暂存回写兜底，兜底自己又被 /tmp 权限打死，整步 traceback 退出。
**解决方案**: 不改仓内脚本（避免未批的资产改动），改在运行时替换路径字面量后 exec，`__file__` 仍指向原路径以保 ROOT 解析正确：
```python
p = os.path.abspath("scripts/analysis/compute_persistence.py")
src = open(p).read().replace('"/tmp/_bb_ro.db"', 'os.path.expanduser("~/tmpwork/_bb_ro.db")')
exec(compile(src, p, "exec"), {"__file__": p, "__name__": "__main__"})
```
build_warehouse.py 同法替换 `Path("/tmp/baize_warehouse")`。两步替换后均一次跑通。
**预防措施**:
1. **临时文件落 `$HOME`，不落 `/tmp`**：沙箱 `/tmp` 跨会话共享且他属文件不可删。建议把 `compute_persistence.py:132` 的 `tmp = "/tmp/_bb_ro.db"` 与 `build_warehouse.py:421` 的 `_STAGE_DIR = Path("/tmp/baize_warehouse")` 改为读 `tempfile.gettempdir()`（认 `TMPDIR` env）或直接 `Path.home()/".cache"/...`，并在周任务前置 env 里 `export TMPDIR="$HOME/tmpwork"`。**（改动提案·待 Doctor 批）**
2. **静默降级要出声**：compute_persistence 的 warehouse 分支 `except` 只打印一行 warning 就继续，结果是 8 个商品悄悄变 4 个、弹性系数集体塌到 0.5 而榜照出。凡「取不到就少算一批」的分支，应在产物 JSON 里落一个 `partial: true` 标记，让下游看板/自检能发现，而不是靠人肉比对行数。
3. `build_weekly_report.py:_recent_returns` 已用 `tempfile.gettempdir()`（认 TMPDIR），是正确写法，可作改造样板。

## [ERR-20260802-002] web_fetch provenance 闸复发 —— 公告面兜底路仍不通（ERR-20260719-001 的第二次实测）
**状态**: ✅ 已并入 ERR-20260719-001（重复登记 · 2026-11-07 审核者订正）
**沿革**: ⚠️ 已知风险（2026-09-14 状态词归一 · 公告面兜底路仍不通 · 按既定第 1 级降级绕过中）
**优先级**: 🟡 中
**触发场景**: 2026-08-02 周任务 Stage 2，复现 ERR-20260719-001：`fetch_announcement_evidence.py urls` 生成 29 条东财公告 API URL，逐条调 `mcp__workspace__web_fetch` 全部被拒。
**错误信息**: `URL not in provenance set. web_fetch can only retrieve URLs that appeared in a user message, a prior web_fetch result, or a WebSearch result. Retries will fail.`
**解决方案**: 与上次相同——回退第 1 级 WebSearch，按商品分组做主题检索（7 组覆盖 19 家），成立面/证伪面均取到，crossval gate 一次通过。
**预防措施**: 已确认这是**稳定的环境约束而非偶发**（两次实测同样结果），建议正式修订 SKILL 的三级降级链：删掉「WebSearch 拒返 → 直接 web_fetch 公告 API」这一级（在本环境永不成立），改为「WebSearch 拒返 → WebSearch 搜公告页拿到 URL 后再 fetch → 仍不行则沿用旧 crossval 并如实声明」。**（SKILL 改动提案·待 Doctor 批）**

## [NOTE-20260808-001] 旧价表 commodity_prices/price_increases 停更 4 个月无 deprecated 登记——GOTCHA-20260728-001 同坑复发（第二次实例）
**状态**: ✅ 已登记（2026-08-08 三处补齐：ingest_meta 补 3 行 deprecated·_health.json legacy_sources 补 2 项·lib_public_read.lookup_commodity docstring 标弃用；写库走 Doctor 终端脚本 deprecate_legacy_price_tables_20260808.py）；✅ **库数据层收口（2026-08-09 P0）**：登记落到数据——两旧价表 `is_current` 1→0 + DROP `latest_prices`/`price_trend`，占位价不再经库查询可得（`quarantine_legacy_price_data_20260809.py` · commit `08fafdc`）
**优先级**: 🟡 中
**现象**: 例行自查发现 `commodity_prices`（26 行·停 2026-04-05）、`price_increases`（26 行·停 2026-04-05）已被 `commodity_prices_live.json`+`price_snapshots` 链路整体取代（周日班读价走 live.json·build_weekly_report 全文无 `FROM commodity_prices`·lookup_commodity 零调用方），但三处登记皆缺：ingest_meta 无 deprecated 行、_health.json legacy_sources 未收录、lookup_commodity 无弃用标注——下一个接手人会误判两表仍是现行价源。`update_log`（8 行·停 04-11·含 2 行「测试数据」残留）同批补登。
**根因**: 06-28/07-28 领域分库退役批只登记了 stock_scores/fundamentals，这两张旧价表漏登——正是 GOTCHA-20260728-001「弃用一张表＝三件事一起做（停构建＋源码注释＋元数据登记）」的第二次踩坑（上次是残留 ok 误报断供，这次是干脆无登记）。
**三本账分辨（勿混）**: ① GAI 看板 stale 印章＝**live.json 文件**四品种过期（在轨：TODO 龙鱼 3 件②·周日班处理）；② 本库两旧价表停更＝库内账（本场登记闭环）；③ 快照流水线 6 表（board_snapshots/crossval/web_probes/price_snapshots/proxy_prices/benefit_relations）在更健康——主表 business_breakdown 27 行全 2025 年报期系披露节律非病。
**旧采集管线死链清单（仅登记·不动盘 · 2026-08-08 Doctor 批）**: fetch_real_commodity_data.py / fetch_tushare_data.py / incremental_updater.py / batch_fetcher.py / weekly_database_update.py / run_full_pipeline.py / data_quality_monitor.py——引用自成闭环、无现行入口（唯一外部引用＝docs/审查_20260607 审计文档）。⚠ **手动跑 data_quality_monitor 仍会读旧表出误导报告**；新链路勿引这批脚本。
**⇒ 2026-08-13 P2 剩尾加固（Doctor 批）**：`incremental_updater.insert_with_change_detection` 顶部加守卫生 fail-closed（写 frozen/deprecated 的 business_breakdown_history 直接 RuntimeError 拒绝）——防手滑回混旧刻度。**data_hash 保持旧值、刻意不重算**：旧 hash 与旧口径源数据（百分比刻度）自洽，重算成 0-1 刻度反而会让每次手滑跑旧链都「检测到变更」→ 回混常态化（反效果）。同场：`build_warehouse.py` 澄清 rows_written 语义＝「本次构建收集写入的总行数」（全量重写表=表总行数·board_snapshots 累积表=累积总行数），非「新增行数」。
**教训**: 退役链路登记要「表×文件×函数」三视角全查——表（ingest_meta/_health）登记了不算完，读旧表的公共函数（lookup_commodity）与采集脚本本体同为误导面。

## [NOTE-20260809-001] 中际旭创 1.6T 营收占比库内双值冲突——benefit_relations 0.4 vs history 0.15，标「待核验」不改值
**状态**: ⚠️ 已知风险（2026-09-14 状态词归一 · Doctor 08-09 裁「标待核验·暂不改值」语义保留）
**优先级**: 🟡 中
**现象**: 同标的同产品（中际旭创 300308.SZ · 光模块-1.6T）两表取值不一：`benefit_relations` id 1949〔2026-11-07 实读订正，原记 941〕 = `revenue_ratio 0.4`（40%·源=投资者问答·披露 2026-03-15·P0）；`business_breakdown_history` 当前 v2 = 0.15（`update_log` id6：2026-04-11 由 0.10→0.15·源=投资者问答·note「Q3 批量出货」）。P1 改动①立 benefit_relations 为真源后，若不标注会把存疑的 0.4 一并供为真理。
**研判（非结论·待核原始问答/渊图）**: 1.6T 2025Q3 才放量，FY2025 占总营收 40% 偏高、15% 更贴合时间线；但 0.4 或为「占光模块收入」的不同分母——两值或非同口径，未必谁错。
**处置**: benefit_relations 无 note/status/credibility 列（列仅 commodity…data_source…priority…raw_json），无法行内打 flag，故「待核验」落本错题本、库值 0.4 不动；核清分母口径（总营收 vs 光模块收入）后回写统一。若要行内 flag 需 ALTER TABLE 加列，另案。
**预防**: 真源裁定（表级）与单值存疑（行级）解耦——表立为真源 ≠ 每行已核；行级存疑单列待核验。

## [ERR-20260809-001] build_weekly_report 动态门槛 CULL_MIN_EL 作用域 NameError（仅在『本周有剔除标的』时炸）
**状态**: ✅ 已解决
**优先级**: 🟡 中
**触发场景**: 2026-08-09 周日班 Stage 3 出报告，build_weekly_report.py 在 _render_md 渲染剔除说明时崩：`NameError: name 'CULL_MIN_EL' is not defined`。
**根因**: 07-28 审计修复把剔除门槛从绝对 30 改「候选中位·地板10·上限30」，`CULL_MIN_EL` 在 `build()` 内局部定义，但 `_render_md` 的剔除说明 f-string 也引用它——该 f-string 在 `if culled:` 分支内，故**只有本周真有被剔除标的时才触发**；07-28/08-02 两周 culled 为空 → 潜伏两周未暴露。08-09 市场回撤潮触发 18 家剔除 → 即刻引爆。
**解决方案**: 模块级加默认副本 `CULL_MIN_EL = 10.0`（地板值），`build()` 算出动态值后 `globals()["CULL_MIN_EL"] = CULL_MIN_EL` 同步。两行改动，不改公式语义。
**预防措施**: 凡『分支内才求值的 f-string 引用外层局部变量』的模式，改条件渲染逻辑后须用『分支必触发』的用例回归（本周恰恰是无剔除→有剔除的翻转暴露了它）。同类潜伏面自查：_render_html 未引用该变量，无第二处。

## [NOTE-20260813-001] macro_prediction 择源——v3 为源，v1 弃用
**状态**: ✅ 已裁（2026-08-13 问答板 · Doctor 裁「v3 为源 + v1 标 deprecated」）
**优先级**: 🟡 中
**现象**: macro_prediction.db 里 macro_predictions(v1) 与 macro_predictions_v3 并存，行数相同（3/12）。
**裁定**: v3 为源——v3 是白泽观星引擎 engine_cn.py L662 建表写入的新版口径；v1 是旧表，标 deprecated。
**处置**: ①停构建——v1 已无构建者（观星引擎写 v3）；②源码注释——engine_cn.py 已写 v3；③元数据标注——ingest_meta/_health 若含 v1 登记需同步标 deprecated（db 写沙箱不可达，贴 Doctor 终端）。
**依据**: 问答板 2026-08-13 第 8 题。

## [ERR-20260819-001] 观察窗日计数「第?/40天」——信号B转换日 window_day 未落
**状态**: ✅ 已修（2026-09-14 复盘证据核：breakout_sentinel L251 转换分支已写 window_day + sentinel_state 黄金 active window_day=23 实落 · Doctor 批全案 · CC 代记）｜ **优先级**: 🟢 低（仅显示层）
**触发场景**: 2026-08-19 哨兵日报输出「活跃观察窗：黄金 第?/40天」；同日黄金恰为信号B确认日（pending_confirm→active 转换）。
**硬证据**: ①盘上 sentinel_state.json 黄金事件无 window_day 键（实测）；②源码 breakout_sentinel.py L244-272：状态转换走 `if e["status"]=="pending_confirm"` 分支，转换后 `elif e["status"]=="active"` 不再执行，而 window_day 只在 active 分支 else（L272）赋值；③L324 `.get('window_day','?')` 兜底打印"?"。
**根因**: if/elif 结构 + 展示字段只在非转换分支落值——转换当日 window_day 缺失。
**影响面**: 仅显示层一日之疵：状态/记账/C2 皆不受影响；次日运行起（t0+6）elapsed 重算后自然恢复。误导面：日报"?"易被误判为脚本故障（哨兵任务已据此误报一次）。
**建议修法**: 转换处（L251 置 active 时）同步 `e["window_day"] = elapsed`；或 L324 显示层改由 t0/tds 现算兜底。
**预防门禁**: 状态机「当日转换+当日展示」场景，转换分支须同步落展示字段；回归用例＝转换日实况（本案即 2026-08-19）。
**来源**: 2026-08-19 Doctor「查证」· 只读审计。
**修复（2026-08-21 · Doctor 批 · CC 实施 · 建议修法①）**: L251 转换处同步落 `e["window_day"] = elapsed`——转换日显示 elapsed（=CONFIRM_D），与 active 分支 L272 口径一致。验证：`python3 -m py_compile` exit 0；结构实读 L251 新行在盘、L272/L324 未动；转换日逻辑走查（pending_confirm→active 当日 window_day 已落 → L324 不再打印"?"）。运行时回归＝下个信号确认日实跑（转换日场景自然复现），待独立验收。

## [NOTE-20260819-001] signal_ledger.jsonl 缺席≠路径错——append-only 台账在首个窗口关闭前不存在（审计须知）
**状态**: ✅ 已修复（2026-11-07 未参与实施的审核者 subagent 独立复验 PASS 代签 · 证据：`data/weekly/signal_ledger.jsonl` 已存在 3 行、首行黄金 C2 exit_date=20260918——「首个闭窗前不存在」前提已于 09-18 自然失效；审计须知保留：ledger 首条随首个闭窗事件产生）｜ **优先级**: 🟢
**沿革**: ⚠️ 已知风险（审计须知 · 非代码错误）
**现象**: 只读审计发现 `data/weekly/signal_ledger.jsonl` 盘上不存在，一度误判「任务书路径与脚本现状有出入」。
**根因**: 台账系 append-only，仅三处写入（B 记账窗到期 L269 / rejected A 回填 L279 / C2 离场 L308），且 gated 事件不入生命周期（L218 pend 只含 pending_confirm/active）。截至 2026-08-19 尚无事件闭窗（黄金 8/11 建档仍 active、原油 8/18 gated），故文件尚未诞生——与 sentinel_state.json（活状态）是两本账，互不替代。
**影响面**: 未来哨兵/审计若见该文件缺席，勿再误报为路径错或断链。
**建议**: 无代码改动；接手指南可补一句「ledger 首条记录随首个闭窗事件产生」。
**来源**: 2026-08-19 Doctor「查证」· 只读审计（上轮哨兵报告误报之自纠）。

## [ERR-20260912-001] 期货部分取数成功时 merge 删除失败品种旧价

**状态**：✅ 已修（2026-09-14 复盘证据核：merge_prices 纯函数 L44 在盘 + 三态负测已过 · Doctor 批全案 · CC 代记 · 原 2026-09-12 Doctor 批「同意」· CC 实施：`merge_prices()` 抽为纯函数——仅按本轮成功品种集合替换，失败品种保留原价与原 asof + `update_status=failed_this_run`/`stale_note` 显式标注陈旧；全失败 `if not rows: return` 保持原 store 不动；写入仍单次 write_text（FUSE 无 rename·原子性按环境能力）。持久化负向测试 `scripts/data_collection/test_fetch_futures_prices_merge.py` 三态+回归 4/4 PASS · py_compile 过（实跑）。✅ 落签归 Doctor。
**优先级**：高（行情条目完整性）。
**触发/根因**：`fetch_futures_prices.py:135-136` 用整个 FUT_MAP 剔除旧项，再追加本轮成功 rows。合成旧价包含氦气/锂/铜/金；仅铜成功时，原两行 merge 输出只剩氦气/铜，锂/金被删除。三品全成功正控保留四品。
**影响边界**：证明部分成功分支会移除失败品种，未证明当前 store 已发生该丢失；本轮不执行完整采集、凭据读取或 LIVE.write_text。
**建议修法**：仅按本轮成功品种集合替换；失败品种保留原价与原 asof，并显式标注本轮更新失败/陈旧，不能当新行情。全失败保持原 store；替换写入保持原子性。
**验法**：全成功、单品成功、全失败三态；核未成功品种原字节身份与日期不被刷新，消费端能看到更新失败。
**证据**：`/Users/lunarabbit/Documents/AI4ME/Financial-Audit-outputs/harness-rollout/五项目注册与自检_20260912/business-replays.json` baize_partial_merge，绑定当前 main L65至函数尾的快照，执行其中精确两行合并代码；独立 Seatbelt 重放一致。

**2026-09-12 CC 独立试用追记（同根·不重复造条）**：/audit 生产管线（inbox→自动派发→同 ID 回读）重放 baize-merge-replay 冻结适配器，request_id `61bdde4b24e54b52837e9f77beb5943c`，10/10 对拍成立（copper_only 案 failed_names_removed=[碳酸锂,黄金]，全成功案四品保留、returned_same_object=true 就地改写）；scope=frozen main merge block with synthetic inputs——outer main/真实拉取/生产写库未执行，10/10 系冻结行为对拍非实跑（V.V. 复核勘误补）；固件 origin sha256=5325fa68… 与现行 fetch_futures_prices.py 全文快照一致（958c75ee 路），确认生产代码含同根缺陷。状态维持 🔄 待 Doctor 审批。

**追记（2026-09-12 深夜 · VV 第四轮复验后修复 · 状态 🔄 已修待验·第五轮）**: 唯一剩余出口补齐——`--fetch` 自动入口：① 能力检查移到构造器之前（类级 `hasattr(CommodityDataFetcher,"fetch_all")`，不实例化真实类）；② main 里 `--fetch` 得空/不可用 → **sys.exit(1) 非零退出**（fail-loud）；CSV 正常路线 exit 0 不受影响。py_compile ✓。

**追记（2026-09-12 深夜 · VV 第五轮复验 · 无新增代码待修）**: 第五轮确认——非零退出、CSV 路线、失败品种旧价保护（ERR-20260912-001 并行补丁）均通过；白泽包无新增待修项。

## [NOTE-20260914-001] 受益公司卡窄屏重叠——640 断点改列未重置子项网格定位

**状态**：✅ 2026-09-14 Doctor 目验落签（「OK了」· 手机宽度目验通过 · CC 代记；修复执行与重建重推全链已收口，git 已提交 5f50e51）
**优先级**：低（展示层）。
**触发/根因**：Doctor 报「窄屏收益公司卡排版问题」→ 实核：`.benrow` 基础四列网格 `46px 1fr 1.5fr auto`，640 断点切两列 `34px 1fr` 但**未重置子项显式网格定位**——`.metrics{grid-column:3}`、`.bverdict{grid-column:4}` 在 2 列下越界且继承 `grid-row:1/span2` → 与 rank/bmain 矩形重叠；`.bmain` 被 1fr 压至 26px 宽、内部固定宽子项（bhead 112 + belb 156）溢出 284px；`.belb{grid-column:1/-1}` 对 flex 子项无效（想换行实际没生效）。`.benwrap{overflow:hidden}` 掩盖溢出——**卡内元素互叠、页面无横滚，问题不显于滚动条**。
**影响面**：≤640px 视口受益公司榜全部卡片；桌面/平板（>640px）零影响。
**修复**：640 断点内显式重置——rank/bmain 固定两列单行、`.bmain` 加 flex-wrap 允许换行、belb 换行独占、metrics/bverdict/bdvg 全宽自然流（grid-row:auto）。headless Chromium 五视口（1280/820/640/390/320）几何断言：零重叠、bmain 零溢出、页无横滚（640px bmain 26→498）；Gateway 回读命中。已重建+重推 baize-weekly-dashboard。
**验法**：手机宽度打开受益公司榜目验。
**教训**：媒体查询里改 grid-template-columns 时，必须同步重置子项继承的显式 grid-column/grid-row；flex 子项不吃 grid 属性。
**来源**：2026-09-14 Doctor 报 · CC 实核（渲染复现 + 几何断言 + 修复后复验）

## [ERR-20260925-001] tushare 拒绝明文 HTTP → 哨兵期货腿与生命周期推进全失败（api.tushare.pro 硬编码 http://）

**状态**：✅ 已修复（2026-11-07 未参与实施的审核者 subagent 独立复验 PASS 代签 · 证据：grep `api.tushare.pro` 排 bak 仅 3 处且全为 https（breakout_sentinel L50 / compute_persistence L57 / compute_realized_beta L38）；`sentinel_state.json` mtime 11-06、4 期货腿 asof=20261106 均 checked——09-28 起自然班持续取数成功）
**沿革**：🔄 已修待验（2026-09-25 Doctor 授权修复 · CC 实施：`breakout_sentinel.py` / `compute_persistence.py` / `compute_realized_beta.py` 三处 `http://api.tushare.pro` → `https://api.tushare.pro`，各一处最小改动；自验：哨兵重跑 4 期货腿 + 事件生命周期推进全部恢复、无 ⚠️ 行、exit 0、三文件 py_compile 过。✅ 落签归 Doctor）
**优先级**：🔴 高（哨兵全期货腿断供）
**触发/硬证据**：2026-09-25 哨兵班（baize-breakout-sentinel）输出 4 条「⚠️ 取数失败：HTTP Error 400」+「事件生命周期推进失败」。对照探针（同 token、同 payload、同秒）：`http://api.tushare.pro` → HTTP 400；`https://api.tushare.pro` → code 0 正常返回 trade_cal 数据。token 有效（56 字节，与 Database/.env 一致，写入无尾换行）。
**根因**：tushare 服务端已停止接受明文 HTTP，仅 HTTPS 可用；三个脚本 `_api()` 均硬编码 `http://api.tushare.pro`（urllib 直连，非 SDK）。
**影响面**：哨兵 4 期货品种日检、事件生命周期推进、C2 持仓跟踪全部断腿；compute_persistence / compute_realized_beta 主分析链同根受影响（修复后未实跑验证，仅 py_compile）。当日恰逢中秋非交易日（trade_cal is_open=0），20260924 即最新数据、当日零数据损失；但下一交易日（2026-09-28）起将随新数据出现持续失败，直至修复。
**建议修法**：`http://` → `https://`（已实施）。
**预防门禁**：①外部 API 调用一律用 https，禁止明文 http 硬编码；②token 有效但全线 400/403 时，排查顺序：协议对照探针（http/https 同参同秒）→ 再怀疑 token 与代理；③「不用旧值冒充当日」纪律下，取数失败必须如实报腿、不静默用 state 旧值。
**来源**：2026-09-25 哨兵调度班实跑 · Doctor 授权修复（CC 实施）。

## [ERR-20261026-001] 盛和资源 universe 行 ts_code=null → 龙鱼提取漏收、榜位六维「待引擎」

**状态**：✅ 已修已验（2026-10-26 周班自发现 · CC 实施：`stocks_fundamentals.json` 稀土 direct 行盛和资源补填 `ts_code=600392.SH`（原 null）· verify_note 追加补填痕迹；未动其余 provenance 字段（仍 needs_provenance=true 待 Doctor 批核）。复验：提取集 29→30 只；`batch_score 600392.SH` 引擎通过、`score_with_llm 600392.SH` 落龙鱼库；重建周报后榜上盛和六维/财务显示。✅ 落签走分轨） · 2026-10-26 未参与实施的审核者 subagent 独立核验代签（实读实跑证据：实读 data/stocks_fundamentals.json——fundamentals(L4).稀土(L71).direct(L73) 内 name=盛和资源 行 ts_code="600392.SH"（L119；L127 verify_note 有 2026-10-26 补填痕迹）；实读 Database/龙鱼-标的分析库/records/600392.SH_盛和资源.json——analyses 最新 analysis_date=2026-10-26（L258），total=53.0（L268），rating=谨慎（L269））
**优先级**：中（榜位数据完整性）
**触发/硬证据**：2026-10-26 周报受益榜盛和资源显示「待引擎」→ 排查发现 universe 提取（weekly_local_prep.sh L49 取 direct.ts_code 非空）漏掉盛和；`stock_basic('600392.SZ')` 空集（初按 .SZ 试错）→ 龙鱼库 records 文件名 `600392.SH_盛和资源.json` 交叉印证正确代码为沪市 600392.SH；json 原文该行 `"ts_code": null`。
**根因**：盛和资源为沪市股，当初入 universe 时 ts_code 未填（null），direct 提取按 ts_code 非空过滤 → 该行从龙鱼 batch/六维清单消失，但 run_full_analysis 按 name 读入 → 榜上有名、六维无源。
**影响面**：龙鱼 batch/六维提取清单漏 1 只（其余 29 只正常）；受益榜盛和六维/财务分「待引擎」；不涉价格数据与弹性计算。
**建议修法**：补填 ts_code（已实施）；provenance 字段（data_source/priority/rev_confidence）仍待 Doctor 批核后按 sync_longyu_universe 门禁补齐。
**预防门禁**：①universe 提取后对「name 在榜但 ts_code 缺失」的 direct 行做告警（周班对账一步）；②新增受益行必须过 sync_longyu_universe 门禁（ts_code/data_source/priority 缺一拒收）。
**来源**：2026-10-26 baize-weekly-report 周班实跑 · CC 自发现并修复。

## [ERR-20261026-002] 负同比渲染双符号「+-7.0%」——MD 归因节硬编码「+」前缀 + HTML 运行时 '+'+yoy 拼接

**状态**：✅ 已修已验（2026-10-26 周班自发现 · CC 实施：`build_weekly_report.py` 三处改符号感知——①MD 归因节 `同比 +{a['yoy']}%` → `同比 {yoy_s}`（`f"{yoy:+g}%"` 正负自适配）；②HTML 价格卡 `${_tp.yoy!=null?'+'+_tp.yoy+'%':'—'}` → `(_tp.yoy>0?'+':'')+_tp.yoy+'%'`；③HTML benCard `${_ben0.el!=null?'+'+_ben0.el:''}` → `(_ben0.el>0?'+':'')+_ben0.el`。py_compile 过·重建后黄金行显示「同比 -7.0%」。✅ 落签走分轨） · 2026-10-26 未参与实施的审核者 subagent 独立核验代签（实读实跑证据：实读 scripts/reports/build_weekly_report.py——L634 `f"{a['yoy']:+g}%" if a['yoy'] is not None else "—"`、L1177 `(_ben0.el>0?'+':'')+_ben0.el`、L1189 `(_tp.yoy>0?'+':'')+_tp.yoy+'%'` 三处修复在场，裸 `同比 +{a['yoy']}%` grep 0 命中；实跑 python3 -m py_compile 该文件 exit 0；实读 周报/白泽周报_最新.md——黄金行「同比 -7%」（L74），grep "+-" 0 命中；实跑 scripts/reports/validate_crossval.py exit 0·crossval 合格）
**优先级**：低（展示层·负值品种首次触发）
**触发/硬证据**：2026-10-26 周报 MD 黄金行渲染为「同比 +-7.0%」（黄金 yoy 首次转负触发）；HTML 侧同缺陷在运行时拼接产生（静态文件 grep「+-」为 0 但 JS `'+'+yoy` 运行时渲染「+-7%」）。
**根因**：模板写死「+」前缀拼接，未考虑负 yoy；黄金 yoy 自 2025-10 高基数起转负（-7.0%），首次暴露。
**影响面**：所有负 yoy 品种的 MD 归因节标题与看板价格卡/benCard 弹性分显示；正数路径零影响（输出不变）。
**建议修法**：符号感知格式化（已实施）。
**预防门禁**：①模板拼接数值符号一律用 `:+g` 或 `(v>0?'+':'')` 模式，禁裸「+」前缀；②负值路径渲染需负向测试（本缺陷因历史上所有 yoy 为正而未被发现）。
**来源**：2026-10-26 baize-weekly-report 周班实跑 · CC 自发现并修复。

## [ERR-20261104-001] 干跑试跑探 `--help` 误触哨兵脚本本体 → sentinel_state.json 被当日扫描覆盖（无备份）

**状态**：✅ 已修已验（2026-11-04 登记；同日 Doctor 批「按合理推荐执行修复」→ CC 实施参数守卫；独立复核 PASS_WITH_LIMITS；**2026-11-04 Doctor 验收通过**（功能性修复·Doctor 亲裁，CC 代记））
**优先级**：🟡 中（本次结果无事件、ledger 未动，实害低；但 state 旧版不可复原）
**触发/硬证据**：2026-11-04 19:00 UTC，官方云端「Baize breakout sentinel」任务按 Doctor 授权做**干跑试跑**（指令明写「不跑哨兵脚本本体、只可试 --help/--dry-run」）。试跑会话执行 `python3 scripts/analysis/breakout_sentinel.py --help`，脚本**无 argparse、忽略未知参数**，直接走完主体：`data/weekly/sentinel_state.json` mtime → 2026-11-04 19:00:26 UTC（被当日结果覆盖，旧版未备份）；`signal_ledger.jsonl` mtime 仍 10-15（未追加）；输出「无突破事件」；未写 token、未 --set-event-type。试跑自报原文见 `brain/.tmp/trial-2026-11-04/baize-breakout-sentinel.md`。
**根因**：① 脚本不解析参数，`--help` 不是安全探针；② 干跑指令只禁「跑本体」却允许「试 --help」，没要求先读源码确认有无参数解析。
**影响面**：sentinel_state.json 的「上次状态」基线被今日值刷新——Gateway 同名班当日 02:40 PT 已跑过一次，两次读同一日数据，状态翻转报警基线大概率不变；但旧 state 内容已无法核对。ledger/台账未受影响。
**建议修法**：~~（待 Doctor 定）~~ 2026-11-04 Doctor 批「按合理推荐执行修复」→ 已按下条落地（取最小参数守卫，不引 argparse、不新增 --dry-run）。
**修复（2026-11-04 · 已修待验）**：`main()` 开头加参数守卫（未引 argparse，最小改动）：`-h/--help` → 打印用法 exit 0、不扫描不写盘；未知参数（含 `--dry-run`，脚本本无干跑模式）与 `--set-event-type` 参数不足 → exit 64、不执行主体；无参扫描与 `--set-event-type <id> <类型> [<依据>]` 语义不变（旧版 argv≥4 门槛 ≡ 新版 args≥3）。备份 `_bak/breakout_sentinel.py.bak_2026-11-04_argguard`（md5 a857fa9c…）。持久化负向测试 `tests/test_breakout_sentinel_argguard.py`（副本树跑，3/3 OK；故障注入：对旧版跑同测 2 FAIL）。真盘 sentinel_state/ledger 测前测后 mtime+md5 不变。
**独立复核（2026-11-04 · 未参与实施的 subagent）**：PASS_WITH_LIMITS——diff 仅守卫块、阈值等价、真盘五种探针 rc 与 state/ledger 指纹前后一致、单测 3/3、故障注入 2 FAIL 均复现。限：复核时多试了合法形态 `--set-event-type x y`（未命中事件）→ 真盘 state **内容 md5 不变（c94e4bb0…）但 mtime 由 19:00:26 变为约 20:22 UTC**，故本条「19:00:26 被覆盖」此后只能凭文字核，不能再 stat。另发现既有行为：`set_event_type` 未命中也重写 STATE（可改为 hit=False 不写盘，待批）。
**预防门禁**：① 对任何脚本做干跑前，先 `grep -n "argparse\|sys.argv" 脚本` 确认有参数解析，**没有就不许带任何参数试跑**；② 给试跑会话的指令里写「不许试 --help」而非「可试 --help」，除非已确认脚本支持；③ 可能写状态的脚本，试跑前先 `cp` 状态文件留快照。
**来源**：2026-11-04 官方端迁移场（云端定时任务干跑试跑）· 试跑会话自报 + 主会话 stat 复核。
