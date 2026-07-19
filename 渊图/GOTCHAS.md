---
title: 渊图 · GOTCHAS（已知坑）
tags: [渊图, gotchas]
created: 2026-05-14
updated: 2026-07-19
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

## [ERR-20260719-001] 二次生成摘要的相对年份系统性偏移 → 入库 LLM 不做统一裁决、逐节点各自猜 → 同篇内**混合污染**
**状态**: ✅ 已归正（2026-07-19，7 节点 / 3 边，canonical 3384/3903 守恒）**优先级**: 🔴 高

**触发**: Doctor 阅读 `2026.07.18-国泰海通：超节点产业化突破与技术演进.md`（P2）时发现「大量混入 25 年时间节点，同时使用未来/预期，弄不清是过时信息还是笔误」。

**真因（两层，缺一不可）**:
1. **raw 层**——该篇 §1-9 摘要为二次生成，把专家原话的「今年 / 明年 / 去年」系统性映射为 **2025 / 2026 / 2024**，**整体倒退一年**。16 段 A 答案正文**零个绝对年份**（全为相对表述），所有绝对年份都是摘要层自己加的。
2. **入库层**——`kg_ingest` 面对「摘要说 2025 / 文件名 2026.07.18」这一矛盾，**没有做统一裁决**，而是逐节点各自猜：产出了错的 `concept_SupernodeMarketScaleChina2025`，同时又产出了对的 `metric_B300ServerPrice.price_2026h1`。

**★ 危险点：混合污染比全错更难查**。全错会显得突兀，混合污染里对的那部分反而给错的那部分背书，肉眼扫一遍容易判「大体没问题」。与 ERR-20260718-001「分裂型幽灵」同族——**同一篇里部分对、部分错，是渊图目前最难自动发现的一类**。

**核实方法（可复用）**: 用**外部硬锚**反推相对年份基准，四项一致才采信——① 昇腾 950PR 2026-Q1 推出、2026-04 量产（文中「已小批量供货」）；② 950DT 原定 2026-Q4、现确定 8 月上线（文中「8 月拿商用片、9 月末–10 月中下旬批量交付」）；③ 智谱 GLM-5.2 于 2026-06 发布（文中「下半年若出现 GLM 5.2 级别爆点」）；④ x86 CPU 2026 年两轮涨价累计 40%-50%（文中「今年已涨价两轮」）。→ 确认 **今年=2026 / 明年=2027 / 去年=2025**。
另有**内部自证**：摘要 §6 写「2026 年行业最大问题在供给侧」，其对应 Q10 原话是「**明年**行业最大的问题…」，在「今年=2025」假设下二者不可能同真。
另有**同批语料旁证**：`2026.07.12-超节点交换机`篇同样用今年/明年，入库时被正确解读为 2026。

**处置**: raw 摘要层 13 处 +1 年归正 + 顶部加校勘头（Q&A 段未动）；图谱走 `mapping/fix_guotai_year_20260719.py`——4 节点改 id（旧 id 入 aliases）+ 3 边端点同步（边 id 留旧）+ 7 节点 1 边 name/desc/props 归正 + `_meta.年份归正_20260719` 审计留痕。守恒 3384/3903、旧 id 零残留、非目标对象逐字节守恒。

**预防**:
- ① **凡 raw 是「二次生成摘要」而非逐字纪要，入库前必先做相对年份基准校验**——判据：正文出现绝对年份但同篇 Q&A/正文用相对词，即为高危；
- ② **凡节点 id 带年份，入库后比对该年份与来源文件名年份**，差值 ≠ 0 即人工复核（本例四个节点差值分别为 −1/−1/−1/−1，机器一扫即出）；
- ③ 入库 LLM 遇到「文档内年份」与「文件名年份」冲突时**不应逐节点自由裁量**——考虑在 prompt 里显式给出文件日期并要求统一基准，或后处理告警（沿 ERR-20260718-001「prompt 是请求、后处理是保证」的结论）；
- ④ 高时效判断先看**外部硬锚**（产品路线图 / 发布时间 / 涨价周期），别只靠文内自洽。

**Q10 标题特例（Doctor 2026-07-19 裁定改）**: Q&A 段唯一的绝对年份出现在 **Q10 标题**「是否会卡住 2026 年的交付」，而 A10 答的是「**明年**…」。值得留意的是，这处**表面上是支持「今年=2025」的反向证据**（若今年=2025，问 2026 而答「明年」恰好自洽）。判为偏移残留的理由：① 四项外部锚是硬事实，Q10 标题是软推断，不能用软的推翻硬的；② Q 标题带脚注编号、系二次归纳而非专家原话；③ 16 段 A 正文一个绝对年份都没有，唯独 Q 标题冒出一个，形态上更像转换产物。**已改为 2027 年**。
**方法论留痕**: 遇到与主结论相冲的单点证据，**先分清它是硬锚还是软推断**再决定权重，不要因为「有反例」就动摇整条证据链，也不要因为结论已定就把反例藏起来不报。

## [ERR-20260709-001] kg_ingest 自动 base 查找不扫 mapping/ → 新终端未设 KG_BASE_JSON 即失败
**状态**: ✅ 已解决（绕过）**优先级**: 🟡 中
**要点**: 新登录 shell `python3 kg_ingest.py --batch` 报「未找到知识图谱 JSON」。根因 `find_latest_kg` 只扫 `~/Downloads`+行业研究根、**不扫 `mapping/`**，而 canonical 在 mapping/ 下；历史靠 profile 里 export `KG_BASE_JSON` 才隐性跑通。修：命令默认带 `--base mapping/行业知识图谱_完整数据库.json`（不依赖环境变量）。**详**: `Database/行业研究/渊图_GOTCHAS.md` [ERR-20260709-001]

## [NOTE-20260709-001] CC 拼既有工具命令别从源码 grep 臆造参数——先查历史日志实敲命令
**类型**: 📝 流程教训（CC 协作）**优先级**: 🟡 中
**要点**: CC 拼渊图入库命令两次臆测两次错（文件列表式命令 vs 真实 `--batch` 扫目录；`DEEPSEEK_API_KEY` vs 真实 `KG_API_KEY`），根因都是从散落/过时源码 grep 拼参数、没核 main() 也没照历史实敲命令。取信序＝历史 logs 实敲命令 > `--help`/main() 现行 argparse > 源码推断。附元教训：落盘类动作宣称完成前必 grep/stat 复核（本坑上轮曾假完成）。**详**: `Database/行业研究/渊图_GOTCHAS.md` [NOTE-20260709-001]

## [NOTE-20260702-002] 渊图BT基板产业链A股缺口——供应商节点全为台股
**类型**: 📝 数据缺口（如实记录）**优先级**: 🟡 中
**现象**: 查"BT基板对应公司"时，图谱里 BT基板的直接 supplies 节点（欣兴电子 Unimicron、南亚电路板、景硕科技）全是台湾上市公司，**没有任何一家纯正 A 股 BT基板标的**。
**处理**: A股这条线只能靠兴森科技（长鑫是其BT载板第一大客户，锁定S3工厂一半产能）和深南电路（存储相关BT基板需求助力广州基板厂盈亏平衡）的BT关联业务间接覆盖，不是独立一批公司。按数据真实性铁律**如实告知缺口，不强行拉一家不精确的A股标的凑数**。
**预防**: 未来做"BT基板对应A股公司"一类检索时，直接引用本条，不必重新 search 一遍才发现缺口；若后续帕米尔/研报语料补上国产BT基板玩家（如兴森/深南以外的独立标的），及时回填本条并升级为有解状态。

## [NOTE-20260702-001] ABF载板三套梯队口径易混淆，须分开引用
**类型**: 📝 认知澄清（非错误）**优先级**: 🟡 中
**现象**: "ABF载板第一梯队"这个问法背后其实挂着图谱里三套不同维度的梯队节点，容易被误当成同一件事引用：
1. **全球ABF载板第一梯队**（技术/产能双料龙头）：揖斐电 Ibiden（"全球领先ABF基板供应商"）、新光电气 Shinko Electric（节点原话"属于全球第一梯队"）、欣兴电子 Unimicron（属性直接标 `market_position: 第一梯队`）。
2. **国产ABF载板厂商竞争格局**（华为海思供应链内部口径，节点 `国产ABF载板厂商竞争格局`）：`hisilicon_tier1_supplier`=兴森科技（24层/系统良率85%）、`tier2`=深南电路（20层/良率82%）、`tier3`=迪景半导体（珠海越亚）。节点原文明确"与国际一线大厂在良率和层数上仍有约一至两年的差距"——国产Tier1不等于全球第一梯队。
3. **mSAP光模块PCB竞争格局**（节点 `光模块PCB竞争格局（mSAP）`，服务1.6T光模块而非CPU/GPU封装载板）：Tier1=鹏鼎、深南电路、欣兴/景硕；Tier2=方正科技、胜宏科技、生益科技、景旺电子。深南电路和欣兴电子在这条线上也是Tier1，但产品和客户群与ABF封装载板不同。
**预防**: 引用"ABF载板梯队"前先确认问的是哪一套口径（全球 vs 华为供应链内部 vs mSAP光模块PCB），三者节点独立、不能互相替代引用，尤其"国产Tier1"不能直接等同"全球第一梯队"。

## [NOTE-20260628-001] update_nodes/update_edges 改 properties 必带 updated_at，否则深合并不生效
**类型**: 📝 数据卫生（合并语义坑）**优先级**: 🟡 中
**触发**: 2026-06-28 央视华工入库 patch，A·`concept_COUPEGen2Production` update_node 只写 id+properties+data_sources（未写 `updated_at`）。kg_merge_safe dry-run 报 7 改、看似成功，但 in-memory 读盘核验发现 COUPE 新 props **没合进去**（仍 4 个），仅 data_sources 并了（1→2）。
**真因**: `kg_merge._merge_node` 按 `updated_at` 判新旧——patch 无 updated_at → `_parse_ts("")` 视为极早 < base_ts → 走 **kept_base** 分支（只 append data_sources、**不调 `_deep_merge_dict_fields`**）。NOTE-20260626-001 的深合并只接在 **took_patch** 分支。同批 `company_HGTech` 因 base 本身无 updated_at（两边都空、不满足 patch_ts<base_ts）才侥幸走 took_patch、props 正常合并——纯属巧合。
**解决**: 给两个 update_node 补 `updated_at=2026-06-28`（≥base）→ 强制走 took_patch → COUPE props 4→8 正确深合并、描述/其余字段不动、HGTech 旧 props 全保留。
**预防**: ① **凡 update_nodes/update_edges 改 properties/_meta，patch 必带 `updated_at` 且 ≥ base 的 updated_at**，否则深合并静默失效；② 落盘前别只信 kg_merge_safe 的 diff 动作标签（kept_base/took_patch），必 **in-memory 跑 merge(dry_run=False) 读盘核验目标子键真在**（注意 `merge(dry_run=True)` 只算 diff、不返回已应用图，核验要用 dry_run=False 的内存结果，不写盘）。属 NOTE-20260626-001 族系。

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
**类型**: 📝 数据卫生（回归）→ ✅ 已根治（2026-06-26 深合并实装）**优先级**: 🟡 中
**根治（2026-06-26）**: `kg_merge._deep_merge_dict_fields` 对 `properties`/`_meta` 改子键并集深合并（patch 子键胜出、base 独有保留），took_patch 分支节点+边均接入。薄/空 props patch 不再冲掉富 props。单测 `tests/test_kg_merge_deepmerge.py` 4/4（含空 props、子键覆盖、_meta 并集、富 props 不丢）；provenance 既有单测 4/4 回归通过。代价：无法再经 patch 删子键（本库 props 累加事实，可接受；删走专门脚本）。下方为原始诊断，留档。
**现象**: `company_Shenghejingwei` 在 2026-06-22「950 产能」批次后 updated_at=2026-06-24，desc 仅剩 3 句、`properties={}`；而 wiki 卡（2026-06-23 快照）仍存 46 条 props——**卡比节点全**。
**真因**: kg_merge `_merge_node` 在 patch 胜出时 `merged=deepcopy(patch_node)` 后只保留 base 中 patch **未提供**的顶层 key；若本批 LLM 产出薄 patch **带了** `properties`（哪怕是 {} 或少量），整块替换掉旧富 props（top-level 替换、非深合并）。
**绕过/解决**: 从 wiki 06-23 快照回填 desc + 46 props（本次已做，保留 06-24 新增的「2025 管理问题」事实）。
**预防**: ① 入库后抽查热门节点 props 是否被薄 patch 冲淡；② 富节点 props 以 wiki 卡为快照备份源；③ 治本选项：kg_merge `properties`/`_meta` 改深合并（patch 缺的子 key 保留 base）——触及入库主链，另议立项。

## [NAMING-20260628-001] 命名规范铁律：禁裸拼音简称 id + 三路审计对账法（ERR-20260602-001 族系总治理）
**状态**: ✅ 已立律 + 配检测脚本 + 12 组真重复合并落地（2026-06-28，canonical 2767/3337）**优先级**: 🔴 高
**触发**: Doctor「不允许再出现 company_xiandao/company_tongmei 这种简写节点名」。裸拼音简称 id 光看无法唯一定位实体（先导有微电子/集团/基电/智能多家；通美有 AXT/北京通美/金瑞佳业），是张冠李戴温床。
**核查法（Doctor 定）**: 开 **3 个独立 subagent 同任务核查、互不喂结论**，CC 对照三方结论差异 → 对分歧点做二次重点核查（联网+desc）。本次成效：三路共识 9 组真重复 + 二次核查坐实 3 组（天弘=Celestica/长光华芯幽灵节点/铟杰=英杰），并**驳回 1 个误并**（利森诺克 Lisenoke ≠ 力森诺科 Lisennock=Resonac——靠 Showa「为利森诺克供铜箔」的矛盾识破，单路会误并）。
**落地**: ① 合并 12 组（海光/海思/Meta/台光三合一/中兴微/鼎泰高科/通美/新凯来/鑫耀=新耀/天弘=Celestica/长光华芯/铟杰=英杰）；② 改名纠错（升腾删 Enflame 别名归华为昇腾·910C 实为昇腾；GUC 正名创意电子·清「世界先进/世芯」错挂）；③ 立**命名规范铁律**写进 `Database/行业研究/CLAUDE.md`（禁裸简称 id/上市带 code/大小写唯一/外企用全称）；④ 配检测脚本 `rules/bare_alias_check.py`（[1] 大小写重复必修·[2] 裸简称清单·[3] 近名兄弟簇），接 batch 后跑。治理后 [1]=0、33 组近名兄弟人工扫均为合理母子/不同实体。
**遗留**: 利森诺克真身（独立 CCL 厂·联网未坐实）；宝德 PowerLeader 液冷描述疑张冠李戴（待回研报）；222 单义裸简称登记黑名单渐进改；先锐科技英文待核。
**预防**: 新建 company 节点遵铁律；batch 后强制跑 bare_alias_check.py；易混/族系实体（先导/通美/住友/三菱/鼎泰/海光/海思/台光/中兴微/生益…）建节点前 kb 查重 + 联网坐实英文名↔实体。属 ERR-20260602-001 / FIX-20260619-001 族系总治理条。

## [ERR-20260718-001] LLM 把正文首行「XX-学习材料（MMDD）」当文件名写进 data_sources.file → provenance 静默失配
**状态**: ✅ **已根治闭环（2026-07-18 当日）** **优先级**: 🔴 高
**根治落地**: `kg_ingest._enforce_source_filename(patch, filename)` —— patch 解析后、cite/价格钩子/merge **之前**，强制把所有 `data_sources.file` 覆写为真实文件名，**不采信 LLM 输出**。LLM 编造的原值留痕在 `ds['_file_llm_said']`，改写数 >0 即打 WARNING，作为长期监控指标（本次 15 篇里 3 篇跑偏，非偶发）。
**为何选后处理而非改 prompt**：prompt 是请求、后处理是保证；且同文件的 cite 路径（`_cite_ds`）一直是代码直写 filename，从未产生幽灵，可作对照佐证。
**安全性论证**：一个 patch 只对应一篇文档，filename 唯一，不存在「合法引用其他文档」情形（LLM 只看得到这一篇）；跨文档 data_sources union 发生在 kg_merge 阶段，不受影响。
**测试**: `tests/test_enforce_source_filename.py` 18/18（含分裂型真假混杂、标题型/日期型两种篡改、6 类边界）；既有 provenance 4/4 + deepmerge 4/4 回归通过。
**历史数据清理**: 本批归正 86 处 + 绿的谐波 49 处 + 历史幽灵 A/B/D1 共 2116 处；幽灵总量 371 种/4487 处 → **287 种/2371 处**。剩余多为已归档 PDF、`web:` 网页源、以及归一化后有多候选的歧义项（机器分不出，**宁可不修**）。
<!-- 以下为原始诊断，留档 -->
**原状态**: 🟧 本批已归正（86处），根治待立项
**触发**: 2026-07-18 帕米尔15篇 batch，六氟丁二烯篇报「provenance 零足迹」。查证发现节点确已抽出（6节点/6边），但 `data_sources.file` 写的是 LLM 自造的名字，按 file 反查匹配不上。
**真因**: `kg_ingest` 让 LLM 自行产出 `data_sources.file` 字段，而 LLM **不知道真实文件名**，于是拿文档正文首行的「XX-学习材料（MMDD）」或**处理当天日期**去编。本批 3 篇中招 86 处：
- 六氟丁二烯 14 处**全错**（用了处理当天 `2026.07.18`，真实文件 `07.12`）
- 磷化铟 41 处幽灵 / 16 处真名 —— **分裂**
- 超节点交换机 31 处幽灵 / 26 处真名 —— **分裂**
**★ 告警盲区**: `provenance 零足迹` 告警只在**该篇一处都没记对**时触发。磷化铟/交换机因为有部分节点记对了，**告警不响、静默漏过** —— 这是比坑本身更危险的部分。
**波及历史**: 上一批（2026-07-13）绿的谐波篇同样中招，幽灵 `2026.07.12-帕米尔研究：减速器学习材料：绿的谐波人形订单超30万台.md` 49 处**已进 canonical**。全图另有 373 个对不上磁盘的 file 名，但多数应属文件移动/归档/Notion hash 清理，**不可一概算篡改**，需专项审计逐个配对。
**影响**: 不伤图谱结构正确性（节点/边/type 全对），只污染按 file 反查的溯源链——正是 ERR-20260608-003 当初要根治的伤害，从另一个口子漏回来。
**本批处置**: `mapping/fix_batch15_20260718.py` [7] 按显式映射归正 86 处，加 `_file_corrected_by` 审计字段。
**根治方向（待立项）**: `data_sources.file` **改由代码强制写入传入的真实文件名，不让 LLM 产出该字段**——LLM 本来就无从知道文件名，没有任何理由让它自由发挥。触及入库主链，单独立项。
**关键澄清（Doctor 2026-07-18）**: 正文（MMDD）**不是 LLM 编造**，是文档标注的**会议日期**；文件名日期是**纪要发布/获取日期**（Doctor 无法参加所有会议，会议与纪要之间有 1-7 天延迟）。语义上会议日期更准 → 另立「会议日期改名批」对齐 32 篇。**但改名修不了本坑**：LLM 连标题一起重写成「XX-学习材料」，日期对上标题仍对不上，两件事必须解耦。
**预防**: ① batch 后除看零足迹告警外，**必须主动扫「幽灵 file」**（`data_sources.file` ∉ 磁盘真实文件 ∪ index）——告警抓不到分裂型；② 逐篇核对「本篇真实文件名被记为来源的次数」，为 0 或异常偏低即中招。

## [NOTE-20260718-003] raw/ 混着「老石谈芯」视频转录，与帕米尔纪要**日期常撞车**——按日期配对文件必错配
**类型**: 📝 数据事实（配对陷阱）**优先级**: 🔴 高
**触发**: 2026-07-18 修历史幽灵 file 时，想用「幽灵名的日期段 + 该日磁盘文件唯一」来自动配对。实测直接错配：
- `2025.05.31-帕米尔研究：先进封装：学习材料.md` → 配到 `2025.05.31-老石谈芯-宝马竟然想靠这个技术弯道超车…`
- `2026.06.15-帕米尔研究：玻璃基板学习材料.md` → 配到 `2026.06.15-老石谈芯-中国市场，对于遥遥领先的英伟达…`
- `2026.06.08-帕米尔研究：碳化硅衬底-学习材料.md` → 同日只有老石谈芯转录
**真因**: `raw/视角/老石谈芯/` 下有大量视频转录，文件名同样是 `YYYY.MM.DD-` 前缀，**与帕米尔纪要共用日期命名空间**且数量可观，「该日唯一文件」这个条件经常由老石谈芯的篇目满足。
**正确做法**: 配对**必须日期 + 主题双重校验**——从两侧文件名剥掉停用词（帕米尔研究/学习材料/调研/纪要…）后算字符重合率，要求 ≥60% **且显著领先次优**（≥+0.25）才采信。实测该规则把 8-9 种错配全部拦下，只放行 10 种主题 100% 重合的。
**附带坑**: 主题词切分若用 `len>=2` 过滤，会把**单字主题**（「钨」「膜」）滤成空集、误判为零重合——`2026.06.15-帕米尔研究：钨-学习材料.md` 一度被判无匹配，实际对应 `钨价企稳反弹`。改用字符级重合后正确。
**预防**: 凡在 `raw/` 下做「按文件名/日期自动配对」的操作，先确认候选集里有没有老石谈芯（及其他视角类转录）。属 FIX-20260619-001「张冠李戴禁自动配对，必逐边核」在**文件层**的同构表现。

## [NOTE-20260718-002] 重指边去重必须只作用于被重指的边，否则误伤显式声明的重复边组
**类型**: 📝 流程教训（CC 自查）**优先级**: 🟡 中
**触发**: 写 `fix_batch15_20260718.py` 时，TPU 合并段的去重循环遍历了**全部**边（用一个 `seen_keys` 累积），结果把 [3] 段本该显式处理、且要**把 description 并入 properties** 的两组重复边提前**裸删**，信息丢失。dry-run 计数 `tpu_edge_deduped: 4`（预期 2）暴露了它。
**解决**: 拆成两步——重指阶段**只重指不去重**；去重统一推迟到 [3b]，且 survivor 优先取「未被本脚本重指」的既有边，被撞边的 `description` 存进 `keep.properties`、`data_sources` 并集合并。
**预防**: ① 凡「合并节点后重指边」的脚本，去重范围**必须限定在 touched 集合内**；② dry-run 的计数与预期不符**即视为 bug**，别放过（本次正是靠 4≠2 逮到）；③ 去重一律「保留最丰富 + 信息并入 + data_sources 并集」，不裸删（沿 2026-05-23 完整性清理立的规矩）。

## [NOTE-20260712-001] kg_merge_safe.py 不吃 `--base`（与 kg_ingest.py 参数面正相反）——贴错旗标 argparse 直接报错、merge 空转
**状态**: ✅ 已澄清 **优先级**: 🟢 低
**触发场景**: 2026-07-12 特斯拉 patch promote，CC 给 Doctor 构造终端命令时写成 `python3 kg_merge_safe.py <patch> --base mapping/行业知识图谱_完整数据库.json`。两条 merge 命令（dry-run + 正式）argparse 均报 `error: unrecognized arguments: --base …`、**未执行**（无害：canonical 早已在本会话 promote 到 3125/3683，读盘核验 + git tree clean 佐证）。
**根因**: 两脚本参数面**相反**、极易交叉记混——`kg_merge_safe.py` 签名仅 `[-h] [--dry-run] patch`，base=canonical **已内建强制指向**（见 ERR-20260611-merge：safe 包装就是为「输出强制指向 canonical 无漏写」而生），**不接 --base**；而 `kg_ingest.py --batch` 反而**必须**带 `--base mapping/行业知识图谱_完整数据库.json`（见 ERR-20260709-001：find_latest_kg 不扫 mapping/）。
**预防**: 构造命令前认准脚本——**promote/merge** 走 `kg_merge_safe.py <patch> [--dry-run]`（无 --base）；**ingest 批处理**才带 --base。贴 Doctor 终端前对一眼 usage，避免整轮终端往返空转。

## [NOTE-20260718-002] 研报数字必回原报告看信源标注——转述链最先丢的是时间限定词
**类型**: 📝 数据卫生（信源定级）**优先级**: 🟡 中
**触发**: 2026-07-18 核实比亚迪电子光模块，「800G 月产能 5 万只」这一广泛流传的数字，追到底是开源证券 2025-09 研报原文「2025 **年内**产能 5 万**片**/月」经东财财富号「股问观值」转述后的变形。所有二次传播均可回溯至同一句话。
**三处损耗**（按危害排序）：
① **时间限定词丢失**——「年内」消失后，**年度目标伪装成既成现状**。最隐蔽、危害最大。
② 量词漂移——「片」→「只」。
③ 单源伪装共识——一句话经自媒体扩散后被引为「市场普遍认为」。
**规则**:
- 引用研报数字前，**必须回到原报告看它自己的信源标注**（据公司交流 / 据公司公告 / 券商测算），据此定级：管理层口径→P1；券商自行测算→P3。拿不到原文的，一律标「**P2·单源转述·信源类型未知**」，不得升级。
- 转述文本里凡出现「年内」「有望」「预计」「目标」等限定词，**入库时必须原样保留**，不得压缩成陈述句。CC 本轮初稿即因删「年内」二字把目标写成现状。
- 同一数字若所有二次传播都能回溯到同一篇，即为**单源**，**不因传播广度升级**。
**配套**: 与「高时效数据不入 canonical」铁律配套——高时效数字即便只入 props 注记，**限定词与信源类型也须一并写入**。
**同批次副产**: 同一核实还撞出**分部口径矛盾**——2025H1 分部「新型智能产品」72.09 亿（其中数据中心相关 10 亿）vs FY2025 年报分部「AI 算力基础设施」9.43 亿，H1 已 10 亿而全年 9.43 亿，必非同口径。教训：**跨期引用分部数据前先确认分部划分未变**，公司常在年报重划分部。属 FIX-20260626-001（粒度/时效错配）族系。
**详**: `Database/行业研究/raw/核实/2026-07-18-比亚迪杀入光模块传闻核实札记.md`

## [ERR-20260718-002] 并发会话覆盖：CC 改 brain 文件后被另一会话的 git 提交无痕回退
**状态**: ✅ 已复现并定位 **优先级**: 🔴 高
**触发**: 2026-07-18 本会话用 Edit 工具改 `渊图/GOTCHAS.md`（加 NOTE）+ `渊图/architecture/决策记录.md`（加决策条）+ 两处 frontmatter `updated`，工具均报成功。Doctor 终端 `git add/commit` 却报 **`nothing to commit, working tree clean`**。
**核查**: 沙箱 grep 确认两处改动**盘上根本不存在**（NOTE 计数 0、决策条计数 0、frontmatter 仍为旧值 2026-07-09 / 2026-05-14）。git 报 clean 是**正确的**，错的是 CC。
**真因**: 同日另有会话在动渊图（提交 `d5aa9d6 session: 渊图帕米尔15篇入库与provenance根治 2026-07-18`），该提交**包含 `渊图/GOTCHAS.md`**，把本会话的编辑覆盖/回退。会话中途 CC 曾收到「文件被外部修改」提示（frontmatter 从 2026-07-18 变回 2026-07-09），**当时未察觉那就是回退信号**。
**连带**: 同一并发会话把 canonical 从 **3207/3746 promote 到 3384/3903**，导致本会话三份文档记录的 `canonical_at_time: 3207/3746` 与 patch 的 `_base` 断言集体过期。
**规则**:
- **落盘类动作宣称完成前必 grep/stat 复核**（NOTE-20260709-001 元教训的再次实证，本轮 CC 连犯两次：说「已落」两次均未核）。
- 收到「文件被外部修改」提示时，**必须立即 diff 确认自己的改动是否还在**，不可默认「外部改动与我无关」。
- 动 brain tracked 文件前先 `git log --oneline -3 -- <file>` 看当日是否有并发会话触碰；写完到 Doctor commit 之间若跨越较长时间，commit 前重新核验。
- 引用 canonical 计数前**当场读盘**，不沿用会话早期读到的值——并发 promote 会让它在会话中途改变。
**预防**: 长会话中 brain 文件的「改 → 报告 → Doctor 提交」链条越长，被并发覆盖的窗口越大；高价值改动应**改完立刻请 Doctor 提交**，不要攒到会话末尾。

**追加（同日 · CC 二次踩坑 · 铁律边界订正）**: 铁律「不在沙箱跑 git 写命令」的边界被 CC 划错——以为只禁写命令，于是跑了 `git status --short` 做落盘核验。**`git status` 会刷新索引并创建 `.git/index.lock`，而沙箱无权删除**（输出末尾已有 `warning: unable to unlink '.git/index.lock': Operation not permitted`，CC 当时未理会），残留 0 字节孤儿锁，导致 Doctor 终端 commit 报 `Another git process seems to be running`。
- **订正后的铁律：沙箱内不跑任何 git 子命令，包括 `status`/`diff`/`log` 等看似只读的**。
- 需核验落盘一律用 `grep` / `stat` / `ls`；需看仓库状态则构造命令交 Doctor 终端。
- 残留锁处理：确认无真 git 进程后 `rm -f .git/index.lock`（本次锁为 0 字节、ps 无 git 进程，安全删除）。

**追加二（同日 · 交付格式教训）**: CC 把「拟写入文件的 Markdown 正文」放进代码块给 Doctor 过目，Doctor 误当命令粘进终端，触发一串 `command not found`（无副作用）。**规则：代码块只放可执行命令；给 Doctor 审阅的文档正文用引用块或普通段落呈现，并显式标注「这是文件内容，不是命令」。** 更根本的是——**文件内容应由 CC 自己写入，不该让 Doctor 手工搬运**。
