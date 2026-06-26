---
title: 渊图 · GOTCHAS（已知坑）
tags: [渊图, gotchas]
created: 2026-05-14
updated: 2026-06-26
status: active
type: resource
project: 渊图
---

# 渊图 · GOTCHAS（已知坑）

<!-- 2026-06-24 错题本积压复盘：3 条 ⏳ 已消化 →
     ERR-20260614-002 relation 死字段 ✅ 已净化（P2）；
     ERR-20260608-003 provenance 🟧 第①步已修+单测，第②步另立 PRD（P1）；
     ERR-20260614-001 TPU ✅ 已结案（谱系理顺单脉 + 伞节点 Doctor 定为保留世代锚）。
     当前开放 ⏳ = 0；待 Doctor 决策 = 1（ERR-003 第②步 kg_ingest 覆盖率根治 PRD 是否启动）。
     2026-06-24（二轮）：manifest `brain.gotchas` 3→1 回写（上轮只改本注释、漏回写 manifest 致看板仍显 3）；
     口径＝🟧/⏳/⬜ 未闭环计数，apply 后 =1（仅 ERR-003 第②步待PRD）。BACKLOG-20260624-001 方案就绪待 apply；派工健康埋点 ✅ 已做。
     2026-06-25：ERR-003 第②步 forward 已实装（Route A·非 PRD）→ ✅；BACKLOG-20260624-001 已 apply commit 9e9a259 → ✅。当前开放 🟧/⏳ = 0；唯一 followup = ERR-003 历史 207 孤儿回填（数据卫生·非坑）。看板 brain.gotchas 应随之 1→0（待重建 asset-dashboard.html）。 -->


> 排查超过一轮的问题都该记录在这里。CC 遇到报错并解决后**立即**回写，无需 Doctor 提示。
> 实时操作日志写在项目目录的 `Projects/渊图/GOTCHAS.md`；这里是沉淀+索引。

## 格式

```
## [ERR-YYYYMMDD-NNN] 简要描述
**状态**: ✅ 已解决 / ⏳ 待解决
**优先级**: 🔴 高 / 🟡 中 / 🟢 低
**触发场景**:
**错误信息**:
**解决方案**:
**预防措施**:
```

---

<!-- 在下方追加新条目 -->

## [FIX-20260625-001] 中兴微张冠李戴：误记「中科曙光旗下」实为中兴通讯子公司（ERR-20260602-001 族系）
**状态**: ✅ 已 apply 落盘（2026-06-25，canonical 2700/3248，读盘核验全绿：错边 target=company_ZTECorp、desc 已改中兴通讯、0 重复 0 悬挂）**优先级**: 🟡 中
**触发**: F9000 入库 kb 查重时撞见——`company_ZTEMicro`（中兴微）description 写「中科曙光旗下交换芯片公司」+ 错边 `rel_ZTEMicro_Dawning`（中兴微 --part_of--> 曙光；_meta relabel_2026_05_16 还以 0.95 置信"误确认"该隶属）。
**核查/解决**: 2026-06-25 联网坐实 中兴微（Sanechips，深圳市中兴微电子）= 中兴通讯（ZTE，000063）控股子公司，前身 1996 年中兴 IC 设计部，与曙光无隶属。图谱已有 `company_ZTECorp`（中兴通讯）作正确锚。错源 = 2026-05-03 国产交换芯片研报把集采名单「中兴/华为/盛科」的"中兴"误并曙光。id/name/aliases 本就对，错的仅 description 与边 target。patch `mapping/_v3_20260625_ZTEMicro_fix.json`：update_nodes 修 description + 补 parent/stock_code；update_edges 把 `rel_ZTEMicro_Dawning` 的 target 改指 `company_ZTECorp`、desc/evidence 同步、_meta 记 supersedes；边 id 留旧（Doctor 定·仅内部标签）。Δ +0/+0，dry-run took_patch✅。
**预防**: 入库后跑 `name_code_consistency_check`；研报里集采/名单类多公司并列（中兴/华为/盛科）易被 ingest 误并到相邻实体——建公司隶属（part_of）边前核 evidence 原文 + 联网坐实母子关系。

## [FIX-20260623-001] 张冠李戴修正须 name/aliases/边/desc 全字段同改（非只改 description）
**状态**: ✅ 已立规 **优先级**: 🟡 中
**触发**: `metric_ShengyiElectronicsRevenueForecast` 06-18 修张冠李戴时只改了 description（胜宏→生益电子）+ _meta，但 name「胜宏科技收入预测」、aliases[胜宏/VG/300476]、`measured_by` 边 source=`company_VictoryGiant`(胜宏) 全未改 → name_code_consistency_check 每次 recheck 持续报 2 条告警，入库 batch 也带出告警。
**核查/解决**: 2026-06-23 联网坐实 Shengyi Electronics=生益电子 688183（纯 PCB 厂·Nomura BUY/TP RMB90·上调 2026E）、胜宏=Victory Giant 300476；归位：id 本就 `ShengyiElectronics` 语义正确**不动**，只归正 name/aliases + `measured_by` 边 source→`company_Shengyidianzi` + 两边 desc 胜宏→生益电子 + _meta 审计。告警清零。
**预防**: 修近名/张冠李戴节点时，**name + aliases + 引用边(source/target/desc) + description + properties.stock_code 全字段一并核改**，不能只改 description；改完必跑 `name_code_consistency_check` 确认清零。属 ERR-20260602-001 / FIX-20260619-001 族系。

## [FIX-20260619-001] 公司实体辨识坑：近名/英文名张冠李戴 + 母子混挂（ERR-20260602-001 族系总条）
**状态**: ✅ 已批量清（dedup 54 簇审阅 commit `1e55bee`）**优先级**: 🔴 高
**触发**: V4 Pro 入库时按英文名/拼音建公司节点，常把**另一家公司的英文名**当 id 或 name，或把母子/同集团公司事实混挂到一个节点。本轮深度审阅查实多例：
- **id 英文名指向另一家公司**（张冠李戴）：`company_Eoptolink` name 标"中际旭创"实为**新易盛(300502)**（Eoptolink=新易盛）；`company_IluvatarCoreX` name 标"燧原科技"实为**天数智芯**（Iluvatar CoreX=天数智芯，8 条边错记到燧原账上）；`company_NewPhotonics` name 标"光迅科技"实为**以色列硅光初创**（与光迅 Accelink 002281 无关）；`company_Taiyo` 的 alias"Taiyo"实为**太阳诱电**（节点本体是台光电材 EMC 2383）；`company_TongfangPhotonics` id"同方"误导（本体是光库科技 300620）。
- **母子/同集团混挂**：`company_Shengyi`（生益电子 688183）历史混挂 8 条**胜宏科技(300476)**边 + 3 条**生益科技(600183)**边——胜宏当时无独立节点。
- **错 alias**：`company_Xinxing` 挂"景硕"（景硕=Kinsus 3189 是另一家）；`company_BoqianNewMaterials` 描述串"铂科新材"（铂科 300811≠博迁 605376）。
**核查/解决**: 张冠李戴**禁按边数自动选 survivor**（会把对的边并进错实体）；必**逐边读边描述定归属 + 联网坐实英文名↔实体**，再决定改名/拆/并。本轮：Eoptolink→新易盛＋拆易飞扬建 Gigalight＋1017 布归旭创；IluvatarCoreX 8 边并入既有 `company_Tianshu`、伟测 FT 归燧原；生益电子拆出胜宏 `company_VictoryGiant`。
**预防**: ① 建公司节点前 kb 查重（同实体异 id）；② 入库后跑 `name_code_consistency_check`；③ 易混中文公司 id 用「4 字简称全拼」（见通用教训 G-X22）；④ 登记易混英文名对照表（Eoptolink=新易盛 / IluvatarCoreX=天数智芯 / Enflame=燧原 / NewPhotonics=以色列 / Taiyo=太阳诱电 / 光库=Advanced Fiber Resources / 光迅=Accelink）。

## [NOTE-20260617-001] kg_merge_safe --apply 日志"Δ+0/skipped"是幂等噪音，须读盘核验
**类型**: 📝 认知澄清（非错误）**优先级**: 🟡 中
**现象**: 跑 `kg_merge_safe.py <patch>`（非 dry-run）落盘第二批时，日志同时报"Nodes Skipped (3): ID 已存在→改为 update""Edges Updated/Skipped""Δ +0 节点/+0 边"，又报"合并后 canonical: 2383/2882"——自相矛盾。
**真相**: 实际落盘**正确**（2380/2876 → 2383/2882，+3/+6）。日志的 skipped/Δ+0 是 merge 报告逻辑的幂等性噪音（疑似对已合并的中间态又比了一次），**不代表没写入**。
**规则**: 落盘后**别信合并日志的增量数**，一律**读盘核验**——`json.load` canonical 数实际节点/边数 + 断言新节点/新边在库 + 0 悬挂/0 重复/边 id 唯一。三批均按此核验通过。
**预防**: promote 工作流固定加"读盘核验"步（见 [[经验库]] EXP-20260617-004-P）。

## [FIX-20260617-001] raw/ 被 .gitignore 忽略 → 视角层提炼成品须放 wiki/(tracked)
**状态**: ✅ 已处理 **优先级**: 🟡 中
**触发**: 投知君君视角层先把"产业逻辑 raw 摘录 + 反共识纠偏录"放 `raw/视角/投知君君/`；Doctor 第一批 commit 时 git 提示 `raw` 被 .gitignore（第16行 `raw/`）忽略——提炼成品没进版本控制、只在本地。
**核查**: raw/ 全局 ignore 是设计（原始字幕/暂存料不入 git，老石谈芯 raw 同样不跟踪）；但**提炼成品价值高于原始料**，不该随 raw/ 被忽略。手工 patch json（mapping/_v3_*manual.json）同样被 ignore，属预期（canonical 为已提交真相）。
**解决**: 提炼成品（`_产业逻辑raw.md` / `_反共识纠偏录.md`）`mv` 进 `wiki/视角/投知君君/`（wiki/ tracked），卡片 source/INDEX 引用同步改向；raw/视角/投知君君/ 仅留 README 指针。
**预防**: 视角层"提炼成品进 wiki/（tracked）、原始料留 raw/（ignored）"作为归位铁律。

## [ERR-20260614-002] relation 旧字段历史遗留（schema v3 称已删实未净）
**状态**: ✅ 已净化（2026-06-24，一次性脚本删 2755 条，type 逐边断言不变）**优先级**: 🟢 低
**结案（2026-06-24 复盘 P2）**: 删 relation 死字段 2755→0；节点/边数不变 3263 条、type 字段 100% 覆盖且逐边比对未动、边 id 顺序不变。备份 `backups/…bak_pre_relclean.20260624_142719`。下方为原始诊断，留档。
**触发**: 2026-06-14 帕米尔7篇入库做全图 8 项校验时，发现 2862 条边里 2777 条仍带 `relation` 旧字段（值如 relates_to/evolves_from/used_in）
**核查**: canonical=2777 / _v2=2777 → **本批 0 新增**；属 canonical 既有遗留。schema v3 决策记录称"relation 字段删除 1155 条"，但实际仅删了"同时有 type+relation 的那批"，大量边的 relation 字段从未清。权威字段 `type` 全图干净（0 非法 type、11 种 schema 内），下游 wiki/kb 均读 type，故不影响分析正确性
**绕过**: 入库 QA 只校验 type 字段；relation 视为死字段忽略
**根治待办**: 若要彻底净化，写一次性脚本 `del e['relation']`（全图扫，注意先备份+断言 type 不动），与 schema v3 决策对齐。非紧急
**详**: 本批未动，留待专门 pass

## [NOTE-20260614-001] kg_ingest --batch 的 _v2 输出是全量图，非增量 patch
**类型**: 📝 认知澄清（非错误）**优先级**: 🟢 低
**要点**: `kg_ingest.py --batch --base <canonical>` 的输出 `mapping/_v2_<ts>_N篇.json` 已是 base+增量**滚动合并后的全量图**（含全部 canonical 节点/边 + 新增），不是 add_nodes 式增量 patch。因此：① 所谓"merge 入 canonical"实为**带备份的 promote**（断言全量图 ⊇ canonical 后覆盖）；`kg_merge_safe` 的 patch 格式闸（要 add_nodes 四键）**不适用**于全量图；② QA 时 delta = `_v2 − canonical`（集合差算新增），8 项校验直接跑全量图。
**实例**: 2026-06-14 帕米尔7篇，_v2=2365/2862 = canonical 2286/2786 + 79/76；CC 修补后 promote 到 2367/2860。下次 batch 别再把 _v2 当增量 patch 喂 kg_merge_safe。

## [ERR-20260531-002] kg_merge 默认不回写 canonical，多 patch 必须链式
**状态**: ✅ 已解决 **优先级**: 🔴 高
**触发场景**: 同日多 patch 各自以原始 canonical 为 base 分别 merge → 后者不含前者节点，merge 报"新建/更新 0"，节点丢失
**解决方案**: 链式 merge（前者 `--output` 临时文件当后者 base，末条 `--output` 回写 canonical），merge 后核对节点/边数等于预算值
**预防措施**: 报告"Doctor 操作"节给链式命令+预期数字；"新建/更新 0"视为告警
**详**: Database/行业研究/渊图_GOTCHAS.md

## [ERR-20260531-003] kg_ingest max_retries=0 致端点抖动时整批全跳过
**状态**: ✅ 已解决 **优先级**: 🔴 高
**触发**: batch 21篇 PDF 每篇~10s Connection error, 0 patch
**真因**: 端点瞬时抖动 + max_retries=0 不重试(非key/PDF/参数问题, 已 curl+诊断脚本 C1-C4 排除)
**解决**: client 加 max_retries=4(KG_MAX_RETRIES可覆盖)+timeout=120; 幂等安全(失败篇未标kg_processed,可重跑)
**预防**: LLM客户端永不 max_retries=0; 整批0 patch=基础设施故障先测端点
**详**: Database/行业研究/渊图_GOTCHAS.md

## [ERR-20260602-001] 生益/胜宏近名张冠李戴(3处)+名↔代码校验脚本
**状态**: ✅ 全闭环（2修+拆分落地+建校验；原「Shengyi_PCB 提案待apply」子项 2026-06-25 核 canonical 确认已并/拆净）**优先级**: 🔴 高
**触发**: ingest混淆 生益(Shengyi)/胜宏(Shenghong)拼音 + 生益科技600183(母CCL)/生益电子688183(子PCB)母子公司
**3错节点**: ShengyiElectronics·Shengyi_PCB→均已并/拆净（2026-06-25 核 canonical：两旧 id 皆不在；现 company_Shengyidianzi 生益电子 + company_VictoryGiant 胜宏 独立并存，FIX-20260619-001 拆分落地）;真胜宏Shenghong(300476)独立
**解决**: 建 rules/name_code_consistency_check.py(代码↔name+拼音↔name自洽校验);入库后跑作delta gate
**预防**: 易混公司登记校验表;修正走dry-run+防误伤断言(禁动生益科技/真胜宏)
**详**: Database/行业研究/渊图_GOTCHAS.md

## [ERR-20260608-001] 价格层并发写竞态：price_extract 与 kg_ingest 钩子不可同时跑
**状态**: ✅ 已知约束 **优先级**: 🔴 高
**触发**: 两者都向 `prices/commodity_prices.jsonl` append；并发时各自读 pre-state 再写 → 撞键/丢点（本次 kg_ingest 价格钩子与源码编辑赶在一起，致 53 条混入 + 部分预测点被吞）
**解决**: 顺序跑、不并发；价格层唯一写入口 `price_query.append_prices()`（去重+重建快照）
**预防**: 回填期间不跑新文档 kg_ingest；分工 kg_ingest 管新文档、price_extract 只做一次性回填

## [ERR-20260608-002] 价格去重键漏 horizon → 现价/预测同日撞键误并
**状态**: ✅ 已解决 **优先级**: 🔴 高
**触发**: 去重键 (commodity,grade,price_type,as_of,source_file) 不含 horizon → 同篇同商品同类型同日的"现价/历史对比"与"预测"被判重复，后者被丢（典型：MLCC基粉 涨跌幅 历史+10% vs 预测+10%）
**解决**: 去重键 / 快照键(rebuild_latest) / _price_id 全部加入 horizon；price_query + price_extract 同步修；已污染数据清层重建（重置种子 21 条→Doctor 重跑回填）
**预防**: 价格 schema 凡区分时态（现价/预测/历史对比）的维度都须进去重键

## [ERR-20260608-003] kg_merge 去重并入已有节点时不 union provenance → 已处理研报"零来源"
**状态**: ✅ 根治闭环（2026-06-25）——第①步 _merge_data_sources 复合键 (file,reference)；第②步 forward cite 指纹走 Route A（kg_ingest 加 cite_nodes 槽 + _cite_nodes_to_updates 纯函数 + 零足迹告警，单测 3/3、第①步回归 4/4），原拟「另立高风险 PRD」由更轻的 Route A 取代。残留仅历史 207 孤儿回填，降级为数据卫生 followup（forward-only 观察期）**优先级**: 🟡 中
**进展（2026-06-24 复盘 P1）**: 第①步落地——`kg_merge._merge_data_sources` 去重键 `reference` → `(file, reference)` 复合键，根治「同 reference 不同 file 被吞」；加 `tests/test_kg_merge_provenance.py` 4 测全过（含旧逻辑复现 ERR-003 对照）。**残留第②步**：某报告仅「提到」已存在实体、未改属性时 kg_ingest 不把它写进 patch → merge 层无源可 union，需改 kg_ingest patch 生成 + provenance 覆盖率门槛告警，触及入库主链、风险高，**另立 PRD**。下方为原始诊断。
**触发**: 建生料关系图时发现 37 篇已 `kg_processed=true` 的研报在 canonical 里无任何节点/边 `data_sources.file` 记到 → 抽样核对其实体（碳化硅/华工/800G/电子布等）都已在图谱、但来源记的是别篇
**真因**: kg_merge 合并时实体若已存在→并进已有节点，却**不把本篇 file union 进 data_sources**；报告"处理过"却查不到当过来源
**影响**: 按 file 反查溯源的下游全漏记（生料图谱/信源覆盖/研报审计）；低估热门实体来源广度；误判已入库为未入库
**绕过**: 生料图侧加"内容回链"（扫正文匹配枢纽名补连，弱连接），覆盖 114→154/169，非根治
**根治**: kg_merge 去重并入时 union data_sources（按 file+reference 去重，注意置信度/vintage 合并、防膨胀）；加单测+provenance 覆盖率门槛
**详**: Database/行业研究/渊图_GOTCHAS.md [ERR-20260608-003]

## [ERR-20260609-001] 龙鱼六维:技术供需维把赛道β/嘴炮指引当公司兑现致虚高
**状态**: ✅校准 **优先级**: 🔴高
**触发**: 德科立72虚高(Doctor质疑嘴炮型)→校准62/谨慎
**根因**: 技术供需维用"赛道需求大"代替"公司自身订单/份额已兑现",把未落地期权当现实
**解决**: 三维(技术供需/竞争/新赛道)打"兑现折扣",分β(行业)vs α(公司),只为已兑现给高分;先过降级核查法(EXP-20260609-003-P)
**预防**: regime零容忍业绩下,ROE极低+靠guidance的设上限;同分段横向校验
**详**: Database/行业研究/渊图_GOTCHAS.md

## [ERR-20260611-merge] kg_merge 漏 --output 致 canonical 未更新 → kg_merge_safe.py 固化
**状态**: ✅修正（2026-06-11 卡点修复批次）**优先级**: 🔴高
**触发**: Doctor 跑 kg_merge 漏 `--output`，4 次默认输出时间戳文件、canonical 未动；commit 信息(2279/2777)与实际提交图谱(2227/2718)错位
**解决**: 新建 `Database/行业研究/kg_merge_safe.py`——输出强制指向 canonical（无漏写可能）+ merge 前自动备份 backups/ + patch 格式闸（缺 add_nodes 等四键拒绝合并，防错文件静默合 0 条）+ merge 后重读盘校验节点/边只增不减 + 打印与实际图谱强一致的 commit 命令。**今后合并一律用 safe 包装，不再裸跑 kg_merge.py**
**详**: kg_merge_safe.py 头注释；自测三关（合并/拒错/真库 dry-run）通过

## [ERR-20260614-001] TPU 在 evolves_from 裂成两分量 + 重复节点，待 dedup
**状态**: ✅ 已结案（2026-06-24）**优先级**: 🟢 低
**复盘核验+收口（2026-06-24）**: ① **重复节点已清**——codename_map 列的 6 个旧重复/张冠李戴节点（GoogleTPUv10Humufish / TPUV8AX / TPUV8X / GoogleTPUv8Zebrafish / GoogleTPUv7Ironwood / GoogleTPUv7eSunfish）逐一核对均已不在 canonical，06-19 dedup 已落地。② **「大小写两套」非重复而是两层粒度**：`TPUV6/V8/V9`=世代锚、`GoogleTPUv7/v8i/v8t/v10`=型号变体，图中 `v8t/v8i --part_of--> TPUV8` 结构本就对，不机械合并（ERR-001 自身铁律：张冠李戴禁自动选 survivor）。③ **谱系已理顺单脉**：删 3 条冗余/隔代 `evolves_from`（TPUV9→{GoogleTPUv7, v8t, v8i}）+ v10 改承 v9，世代脊成单线 `V6←v7←V8←V9←v10`，v8t/v8i 降生自 v7 + part_of V8；边 3263→3260，备份 `bak_pre_tpulineage.20260624_143139`。④ **伞节点框架决策（Doctor 2026-06-24 定）**：`TPUV8` **保留为 v8 世代锚**（维持 v8t/v8i part_of），不并入 v8i。下方为原始诊断。
**触发**: 建技术先进度 family 时发现 谷歌TPU 在 evolves_from 子图里裂成两个连通分量——小写 `product_GoogleTPUv7/v8i/v8t/v9_Pumafish…` 与大写 `product_TPUV6/V7/V8/V9`；且 `product_TPUv8t` 与 `product_GoogleTPUv8t` 名称同为「谷歌TPU v8t（训练版）」疑似重复节点
**影响**: 同一代际被拆成两套 id；按 family 聚合/溯源会低估关联；先进度对齐时需手工合并为一条 family（已在 tech_eras.json `family_google_tpu` 合并处理，不受影响）
**根治待办**: 跑 dedup 把大小写两套 TPU 节点按代际对齐合并、删重复 v8t（注意 union data_sources，见 ERR-20260608-003）
**详**: Database/行业研究/mapping/tech_eras.json review_notes

## [ERR-20260609-001b] α折扣串维重复扣分→维度正交修正
**状态**: ✅修正 **优先级**: 🔴高
**触发**: ERR-001把"利润未兑现"同时扣技术+竞争+财务三维(扣三次);Doctor纠:财务问题只扣财务,技术好不扣技术,订单好不扣竞争,扩产对齐供需是好事
**解决**: 维度正交归因——负面信息先归一个维只在该维扣;扩产/重资产爬坡默认中性偏正;但竞争维真问题(源杰单客户/联讯链内循环)仍保留
**详**: Database/行业研究/渊图_GOTCHAS.md

## [FIX-20260615-001] 三环集团 id 拼音误植 Sanhua→Sanhuan（系统性近名坑）
**状态**: ✅ 已修复 **优先级**: 🟡 中
**触发**: 跑龙鱼五力时发现三环集团节点 id 为 `company_SanhuaGroup`——"Sanhua" 是三花（智控,002050,制冷/汽车热管理/机器人执行器）的拼音，三环应为 Sanhuan。属 ERR-20260602-001 同类近名坑。
**核查**: name「三环集团」正确、内容(MLCC/离型膜/洁美/南充德阳)确系三环、图谱内**无三花智控节点**故零碰撞——错的仅 id 串与 alias「Sanhua Group」。误植系统性：连带 4 个 concept/metric 节点 id 同误。
**方案B(彻底·Doctor 批)**: 5 个 id 全 Sanhua→Sanhuan + 9 边/12 端点同步 + alias 修正并补真别名(潮州三环/CCTC/300408) + 加 properties.stock_code 与 disambiguation 防混 + wiki 卡 sanhuagroup.md→sanhuangroup.md。
**安全纪律**: 备份 backups/…preSanhuanRename + 断言节点2367/边2860守恒+无残留+无悬挂+body仅公司节点改。沙箱删不了旧 wiki，交 Doctor `git rm`。
**预防**: 入库后跑 rules/name_code_consistency_check.py；易混公司(三环Sanhuan/三花Sanhua)登记防误。

## [FIX-20260616-001] 盛科重复节点 company_Centec / company_CenturyCore（ERR-20260602-001 同类）
**状态**: ✅ 已落盘核验（2026-06-25 核 canonical：company_CenturyCore 已不在、company_Centec 保留并挂全 10 节点边系，去重生效）**优先级**: 🟡 中
**触发**: 入交换芯片结构增量时发现盛科通信有两个节点——`company_Centec`（挂集采/SwitchTray 边）与 `company_CenturyCore`（挂 supplies Switch256T/512T、competes 博通/中兴微、enables from DualVendorPolicy 边），同实体重复。
**核查**: 两节点 aliases 都含「盛科」；CenturyCore 的 competes_with 博通边与 Centec 既有 `rel_Centec_BroadcomCompete` 重叠。零代码碰撞（非近名拼音错，是纯重复实体）。
**方案(Doctor 批 · 保 Centec)**: `mapping/dedup_centec_20260616.py`——重指 5 边(CenturyCore→Centec)、与既有同向同型边去重合并 data_sources、合并 props/aliases/data_sources(补真别名盛科通信/Centec Communications/688702)、删 CenturyCore 节点。备份 backups/…dedupCentec + 守恒断言(节点 -1 / 无残留 CenturyCore / 无悬挂 / 无重复边 / 无关节点逐字节守恒)。
**预防**: 公司入库前先 kb 查重（同实体异 id）；入库后跑 name_code_consistency_check。

## [派工·非坑] ⚡ 更新健康埋点（派工v1 · 2026-06-24）
**状态**: ✅ 已做（2026-06-24）**优先级**: 🟡 中
**落地**: 写 `scripts/write_health.py`（可复用 stamp，跑结构校验→写 `mapping/_health.json`：updated_at=canonical mtime、update_ok=全绿则 true）+ 已生成首版 `_health.json`（全绿 2713/3260）；`asset_manifest.json` 渊图KG 节点补 `health_file`。看板「渊图KG」卡即点亮「更新时刻 +（无错误/报错）」。固化建议：把 write_health() 接进 kg_merge_safe 落盘成功分支，未来每跑自动刷新（未做，留待动既有码时一并）。
**详**: `Claude/Projects/海螺姑娘/dashboard/UPDATE_HEALTH_派工_v1.md`（任务卡 ⑤）；原待办见 git 历史。

## [BACKLOG-20260624-001] 非规范前缀节点 + 剂泰科技/METiS 生物子图串入（2026-06-24 复盘：实况比记录严重，脚本就绪待 apply）
**状态**: ✅ 已 apply 落盘（2026-06-25，commit 9e9a259）——节点 2713→2699、边 3260→3246，MITMediaLab 保留+剥离、equipment_ 纳入允许集、milestone_×3→event_/market_×1→concept_ **优先级**: 🟡 中（原记 🟢，复盘上调）
**复盘订正实况（2026-06-24）**: 记录原写「6 前缀 + 2 疑串入」，实测**非规范前缀 18 个**、**生物串入为整篇`剂泰科技：全球独家AI纳米递送平台`报告的 15 节点子图**（远超记录）。
- **前缀 18 拆分**：`equipment_`×12（制造设备类·type=equipment·成体系）→ Doctor 裁定**纳入允许集**（已改 `kg_ingest.py` known_prefixes/KNOWN_PREFIXES 加 equipment，不动图）；`milestone_`×3（OCS认证/量产订单/盈利兑现）→ `event_`；`market_`×1（OpticalChipTestEquipment）→ `concept_`；`technology_`×2（LipidBert/高通量LNP）属下方 bio 子图，随删。
- **bio 串入子图 15 节点**（剂泰/睿正/科拓/菁童/MITMediaLab + 陈红敏/赖才达 + MTS004/108 + LipidBert/高通量LNP + 非肝靶向/心肌靶向/双轮模式/LNP专利）：全溯源同一篇剂泰科技研报，属生物医药/mRNA递送，非渊图 AI 硬件域。
**裁定（Doctor 2026-06-24）**: ① equipment_ 纳入允许集；② 边界点 `company_MITMediaLab` **保留+剥离**剂泰 data_source/bio 边（保住手工补的「电液纤维肌肉」合法关联），其余 14 节点删；③ `TFLNPhotonicChip`(薄膜铌酸锂光子芯片) 是正当光子内容**勿误删**（仅 substring 撞 LNP）。
**落地**: `mapping/cleanup_yuantu_bio_prefix_20260624.py`（归档子图→archived/ + 备份 + 守恒断言 + 删14+改4前缀）dry-run 全过：节点 2713→2699、边 3260→3246、MITMediaLab 仍连电液纤维肌肉、前缀改名同步 16 边端点。**待 Doctor 终端 `--apply` + git**。
**预防**: kg_ingest 已校 type↔id 前缀∈允许集（本次把 equipment 纳入唯一真相集）；建公司/技术节点前先 kb 查重 + 核 data_source 主题域，防跨项目（生物/AI硬件）串入。属 ERR-20260602-001 族系的「跨域串入」变体。

## [FIX-20260626-001] 盛合 CoWoS-L 口径矛盾：节点 prop 与 supplies 边冲突（粒度+时效错配，非真矛盾）
**状态**: ✅ 已校对落 patch（待 Doctor 终端 apply）**优先级**: 🟡 中
**触发**: Doctor 追问「盛合也部分上混合键合了么」→ CC 核图谱发现 `concept_DomesticCoWoSLPackagingLandscape` prop「盛合承接 CoWoS-S，不涉及 950/960 CoWoS-L」与 `rel_Shenghejingwei_supplies_HiSilicon`（含 950PR）/ `rel_Shenghejingwei_Supplies_Ascend950PR`（封测）冲突。
**核查**: 非真矛盾。旧口径 P1 = 帕米尔 2025-05-31（一年前·prop 标 undated）；新口径 P1 = 帕米尔 2026-04-27 / 2026-06-22。**950PR = 入门级小尺寸 CoWoS ≠ 950/960 旗舰大尺寸 CoWoS-L**——盛合承接 950PR 入门级，旗舰大尺寸归华为自有产线（Tier1 领先约 3 个月）。混合键合方面：盛合唯一连接是麒麟2026 一单（P2 华泰，2026 秋季未上市），确凿量产仍是 2.5D micro-bump 20μm。
**解决**: 精修 prop 为分粒度口径 + 加 `_meta.校对_盛合CoWoSL粒度时效_2026_06_26`，保留全部边。patch `mapping/_v3_20260626_盛合校对_manual.json`，纯 update 计数 2702/3254 不变。
**预防**: prop 带时态/粒度（入门级 vs 旗舰）须显式 as_of；近名/口径冲突先比 data_vintage 再判、新覆旧；同实体多批次入库做交叉口径核对。属 ERR-20260602-001 族系。

## [NOTE-20260626-001] kg_ingest 后续薄 patch 把既有公司节点「瘦身」：desc 精简 + props 清空成 {}
**类型**: 📝 数据卫生（回归）**优先级**: 🟡 中
**现象**: `company_Shenghejingwei` 在 2026-06-22「950 产能」批次后 updated_at=2026-06-24，desc 仅剩 3 句、`properties={}`；而 wiki 卡（2026-06-23 快照）仍存 46 条 props——**卡比节点全**。
**真因**: kg_merge `_merge_node` 在 patch 胜出时 `merged=deepcopy(patch_node)` 后只保留 base 中 patch **未提供**的顶层 key；若本批 LLM 产出薄 patch **带了** `properties`（哪怕是 {} 或少量），整块替换掉旧富 props（top-level 替换、非深合并）。
**绕过/解决**: 从 wiki 06-23 快照回填 desc + 46 props（本次已做，保留 06-24 新增的「2025 管理问题」事实）。
**预防**: ① 入库后抽查热门节点 props 是否被薄 patch 冲淡；② 富节点 props 以 wiki 卡为快照备份源；③ 治本选项：kg_merge `properties`/`_meta` 改深合并（patch 缺的子 key 保留 base）——触及入库主链，另议立项。
