---
title: 渊图 · GOTCHAS（已知坑）
tags: [渊图, gotchas]
created: 2026-05-14
updated: 2026-05-14
status: active
type: resource
project: 渊图
---

# 渊图 · GOTCHAS（已知坑）

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

## [ERR-20260614-002] relation 旧字段 2777 条历史遗留（schema v3 称已删实未净）
**状态**: ⏳ 观察（不阻塞）**优先级**: 🟢 低
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
**状态**: ✅ 2修+1提案+建校验 **优先级**: 🔴 高
**触发**: ingest混淆 生益(Shengyi)/胜宏(Shenghong)拼音 + 生益科技600183(母CCL)/生益电子688183(子PCB)母子公司
**3错节点**: ShengyiElectronics(已并)·Shengyi_PCB(提案待apply)→均name写胜宏实为生益电子;真胜宏Shenghong(300476)独立
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
**状态**: ⏳ 待解决（已诊断+定位，根治在 kg_merge，待 Doctor 定）
**优先级**: 🟡 中
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
**状态**: ⏳ 待解决（已定位，不阻塞技术先进度落值）**优先级**: 🟡 中
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
**状态**: ✅ 方案就绪（脚本 + dry-run 通过，待 Doctor 终端落盘）**优先级**: 🟡 中
**触发**: 入交换芯片结构增量时发现盛科通信有两个节点——`company_Centec`（挂集采/SwitchTray 边）与 `company_CenturyCore`（挂 supplies Switch256T/512T、competes 博通/中兴微、enables from DualVendorPolicy 边），同实体重复。
**核查**: 两节点 aliases 都含「盛科」；CenturyCore 的 competes_with 博通边与 Centec 既有 `rel_Centec_BroadcomCompete` 重叠。零代码碰撞（非近名拼音错，是纯重复实体）。
**方案(Doctor 批 · 保 Centec)**: `mapping/dedup_centec_20260616.py`——重指 5 边(CenturyCore→Centec)、与既有同向同型边去重合并 data_sources、合并 props/aliases/data_sources(补真别名盛科通信/Centec Communications/688702)、删 CenturyCore 节点。备份 backups/…dedupCentec + 守恒断言(节点 -1 / 无残留 CenturyCore / 无悬挂 / 无重复边 / 无关节点逐字节守恒)。
**预防**: 公司入库前先 kb 查重（同实体异 id）；入库后跑 name_code_consistency_check。
