---
title: TODO 已完成归档
tags: [todo, archive]
created: 2026-07-30
updated: 2026-08-22
status: active
type: log
---

# TODO · 已完成归档

> 从 [[TODO]] 拆出（2026-07-30 `/consolidate`）。**条目正文一字未改**，仅迁移位置。
> 拆分动机：`TODO.md` 39KB 里 70% 是已完成条目，`brain-resume` 每场整篇读入，token 花在已经做完的事上。

## 已完成

- [x] **DVA · 孤儿字幕②（2026-07-24 挂 · 收窄 2026-08-14 · 2026-08-22 勾销迁档 · 剩尾全闭环）**：single_one 首跑 ✓（BOM 修复生效·取景框视频转写成功·退出码 0·无残留锁）；AIGC秋雅 Downloaded 落位 ✓；滞留进程安全终止 ✓（0.3s CPU/零网络/零写入僵死·留痕 closure.log）。**机构调研日记件 ✅ 2026-08-21 已销**（Doctor 裁「seed 搜作者+存量篇落 raw」：sec_uid 已取·fuxi harvest_one 后台·08-13 篇落 raw·07-04 篇核实入库 1a0fff4）。**seed 搜作者班后核查待做**（cc-harvest-0821-jgdy 后台产物拉回/分流待核）。**剩 1 件**：TechScopeLab-科境坊 FCC 反转 1 篇（待 Doctor 裁：归档+正文研判 / 归档 / seed 搜作者）。
  **✅ 2026-08-22 剩尾两件闭环（实跑证据）**：① seed 搜作者班后核查——cc-harvest-0821-jgdy 任务 State=Ready 已完成，summary SUCCESS（exit 0 · known_orphan_warnings 48 属 INFRA-20260603-003 基线 ~630 噪声 · other_warnings 0），log 尾部实读「导入完成 成功:297 空:0 跳过:0 找不到:0 出错:0 · 全局索引 1946 条 Level1 97%」，Downloaded 690 文件、Transcripts 字幕落位；Mac 快照同步走 Doctor dva-refresh.sh 常规动作、喂渊图属另场 feed 裁定。② TechScopeLab-科境坊 FCC 反转 1 篇——Doctor 裁「归档+札记补充」：fuxi move 至 `archived\orphan_20260813\`（moved=True·与 VV 12 项同批）；正文研判（1700 字·Maverick/B.Riley/花旗/高盛四机构 FCC 草案解读综述 P2/P3 无一手增量）→ 口径补入 `行业研究/raw/核实/2026-08-19-FCC机器人禁令与特斯拉链供应商影响核实札记.md` §六（花旗三情景/65% 原产内容门槛/铟反制/高盛三辩论，全部标转述等级）。

- [x] **渊图 · 档案计数漂移对账（2026-08-20 挂 · 2026-08-22 勾销迁档 · Doctor 裁「深查」）**：canonical 实测 4960/5539 vs 档案 08-19 手术记 4964/5542 差 −4/−3——NOTE-20260719-001 族「档案计数未随修复回写」镜像（同族 −1/−12 已于 08-19 对账为 08-17 VV 盲审修复）。本处待 Doctor 裁：深查（git log 对 08-19→08-20 变更）或直接按实测回写档案。
  **✅ 2026-08-22 深查闭环（实跑证据）**：08-19 手术分两阶段——stage1 移出 119/147 → 4964/5542（`bak_pre_patch_embodied2_20260819_070307` 实测），embodied2 patch 续按门禁移启元族 4 节点/3 边 → 终态 4960/5539。三重证据：① commit `a58e35c`（08-19 00:13 PT）message 自证「canonical 4960/5539 · 墓碑123节点150边」；② 墓碑文件实测 removed_nodes=123/removed_edges=150/merged_nodes=2（123=119+4·150=147+3 吻合）；③ 双快照差集恰为启元族（QiyuanBrandPositioning/QiyuanLargeModelArchitecture/QiyuanQ1/QiyuanT1 + 3 条 part_of 边）。档案已回写：决策记录 L81 订正（两阶段 -123 含合并 -2/-150）、系统概览 08-19 段订正、决策记录 L2088 附带发现②标已对账、GOTCHAS NOTE-20260719-001 追记第四实例（教训增量：多阶段批次档案回写以最终 commit 计数为准）。审计脚本 `Database/行业研究/outputs/audit_count_drift_20260822.py` 在盘可重放。

- [x] **fuxi 冷归档 · 三隔离区期满清算（2026-08-03 挂 · 2026-08-22 勾销迁档 · CC 常驻授权执行）**：`_to_delete_20260721`（3.3GB·窗口至 **08-20**）· `_to_delete_20260723_tts`（9.5MB·窗口至 **08-22**）· `_隔离_20260724`（12K·随 08-22 一并裁）。**① 迁址已完成（2026-08-04）**：三件 tarball 经 scp 至 `fuxi-station:F:\Mac_Quarantine\`、SHA-256 三串逐位回验一致、cmd 侧解包 move 落位、本地源已删（释放 3.45GB · Doctor 批准）。**② ✅ 第一件已删（2026-08-20 · Doctor 亲执行）**：删前只读核查三件全部在盘、尺寸/文件数/时间戳与台账三重吻合（`_to_delete_20260721` 3176.64MB/101,906 文件·`_tts` 9.39MB/32·`_隔离_` 0.01MB/9）；`rmdir /s /q` 后复读确认该目录已消失、另两件完好、F 盘余 715.27GB。**③ 剩余（dated 08-22）**：`_to_delete_20260723_tts` + `_隔离_20260724`。⚠ **中文目录名不可按名删**——远端回显乱码（`_????_20260724`），到期须改用 ASCII 日期串匹配绕开编码：`Get-ChildItem F:\Mac_Quarantine -Directory | Where-Object { $_.Name -match '20260723_tts|20260724' } | Remove-Item -Recurse -Force`。**④ tarball 已验内容、时序已定（2026-08-20 验 · Doctor 同日授「自主执行后续」随 08-22 批最后删）**：`mac_quarantine_20260803.tar.gz`（1011.75MB）——2026-08-20 `tar -tzf` 全量列出 **108,852 条目**，顶层恰好三目录、无杂项：`_to_delete_20260721` 108,805（盘上 101,906 文件 + ≈6,899 目录吻合）· `_tts` 33（32 文件）· `_隔离_` 14（9 文件）。**判定：tarball = 三件的精确压缩副本，可随 08-22 批同批处置**。⚠ 删除顺序建议：两目录先删、复读确认后再删 tarball——它是 08-04 SHA-256 回验的基准，最后删。**⑤ 范围外未动**：`cc_sessions_archive_20260811.tar.gz`(266MB) · `bak_20260808_batch20.tar.gz`(17MB) · 08-13 中文名归档(0.08MB) · 空 `.incoming` —— 属别的批次，本条不含。全清后按 v3.1 迁归档。**⑥ Doctor 常驻授权（2026-08-20 授「自主执行后续」）**：08-22 窗口期满后**无需再询问**，CC 按 ③→④ 预置顺序直接执行——两目录 ASCII 日期串匹配删除 → 复读确认消失 → 最后删 tar 包 → 勾销本条目按 v3.1 迁归档，完成后回报留痕。**执行边界**：仅限本条预置的三个对象（`_to_delete_20260723_tts` + `_隔离_20260724` + `mac_quarantine_20260803.tar.gz`）；⑤ 列的范围外物件不在授权内、仍不动。
  **✅ 2026-08-22 执行完毕（CC 常驻授权 · 实跑证据）**：沙箱直连 fuxi（192.168.1.32 · codex）——① 删前只读核查：三件目标在盘、尺寸与台账吻合（tar 1,060,897,539B=1011.75MB）；② 两目录按预置 ASCII 日期串匹配删除，远端复读确认消失（DIRCOUNT 3→1）；③ 复读确认 tar 完好后最后删 tar，`Test-Path=False` 确认 gone；④ 终验复读：范围外五件完好未动（`bak_20260808_batch20.tar.gz` 18,105,202B · `cc_sessions_archive_20260811.tar.gz` 279,369,492B · `cc_archive_sha256.txt` 107B · `光通信札记归档_20260813.tar.gz` 81,485B · 空 `.incoming`），F 盘余 716.26GB（较 08-20 记录 +0.99GB，与所删 tar 体积吻合）。

- [x] **EAL v3 · 发布链收尾（2026-08-21 挂 · 2026-08-21 勾销迁档 · Doctor 总签+「～！」发布授权）**：① ✅ PRD 20 R/N 验收——Doctor 2026-08-21 会话总签（「EAL总签」），PRD status=delivered、checkbox 保持 [?] 保留未自签审计链、§五总签记录+§六变更历史落盘；② ✅ R14 视觉目验——总签覆盖验收，结构级复核已过（4 簇/7 筛选器/窄屏 CSS/FOMC 标题在盘），视觉目验可由 Doctor 在 Cowork artifact 直接看；③ ✅ Gateway 发布回读——新 artifact `eal-v3-event-transition`（2026-08-21 17:28Z · 盘上 SHA `94602559…` 与发布副本逐位一致 · v2.3 event-attribution-ledger 原样保留）· manifest 回读 ✓ · T16 关闭。依据：本会话 Doctor 总签指令与「～！」授权 · `logs/2026-08-21-EALv3-pass3核验与验收推进.md`
- [x] **渊图 · 机构调研日记 08-13 篇核实入库（2026-08-21 挂 · 2026-08-21 勾销迁档 · 证据：commit `cb46d6948d`「首席梳理篇核实入库(Nebius+Lumentum/腾讯capex/Coherent补强) + 第14项边schema断言门禁」· canonical 4979/5559→4980/5560 · patch `mapping/_v3_20260821_机构调研日记首席梳理篇_manual.json` · 札记 `raw/核实/2026-08-21-机构调研日记机构首席最新梳理视频核实札记.md` 在盘）**：开源证券通信首席转述已落 raw（`2026.08.13-机构调研日记-机构首席最新梳理.md`·P2·勘误表·7673346665977253139）。增量候选：CPO 2027H2 高功率激光器放量 / Lumentum 1.6T+ELS 订单 / APO 四大配套（FAU/CW激光器/保偏光纤/棱镜透镜隔离器）/ 光纤供需修复 / 国产超节点链。核实后按 P2 入库；与 08-20 光纤场同域注意去重。

- [x] **EAL v3 吸收与升级实施（2026-08-19 收口迁档）**：shadow.7 验包→吸收（backtest/eal_v3/ 平铺+relocation test+canonical 两件）→§3 数据迁移（sealed `ac00862e…`→candidate→schema 双跑→intake 27/27）→编码 pass2（8 frozen/19 exclusion·共识点值 WebSearch 补全）→DAILY_SHADOW 首跑 4 簇→candidate2 落库 48 结果。生产候选 Mac 3.13.3 全套全绿；PRD 20 R/N 待 VV 验收；additive schema 生产采用待裁。

- [x] **Shakehands 清理 PRD Doctor 总 ✓（2026-08-19 迁档）**：删除 33 项（71→38）· 保留 20 项零缺失 · 独立审查员背书 · Doctor 会话签署总 ✓（status=delivered）· 真删不知会 VV（Doctor 裁）。

- [x] **存量 PRD 处置表（2026-08-19 迁档）**：11 份五类分流 Doctor 四题全按推荐执行——BT-19/provenance→delivered、EAL v2.0/v2.1/战争/残差→cancelled+superseded、19 班→cancelled、畸形节点待 Doctor 目验收口、gate 证据同步待 VV 八轮（该验收后随 v2.3 退役取消）。

- [x] **渊图 · 08-08 三轮清洗与结构修复专场（2026-08-14 重建挂 · 原条漂移丢失·并入 14 组重复边挂账）**：（✅ 2026-08-15 畸形收口场勾销迁档 · 全子项闭环证据：① QA 第 9 项 08-06 实装／第 10 项 08-15 三轮专场实装 ② 双 id 28 组 08-13 并 + 4 对 08-15 清 ③ 幂等闸/防重跑 08-13 标已解决 ④ 14 组重复边 round1 08-15 清 + round2 24 条清 · 畸形还原 08-13 已做 + 08-15 收口闭环。决策记录 2026-08-15「畸形节点还原收口」条）① QA 第 9/10 项机制修复（aliases/data_sources 元素类型断言·file 存在性断言——08-13 归档遗留指向本条）；② 图谱双 id 手术（~7 对 08-08 带入 + 存量 26 组同名双 id）；③ 幂等闸/防重跑保险丝；④ **新增挂账**：14 组重复边（同 source,target,type 三键·28 条边·**2026-08-15 核因已做**：三类构成——同篇重复入库 2（美迪西 07-15 篇·08-08 三轮清洗重跑带入·边 id 一短一长逃过 id 去重）／单篇产重 8（量子 07.09 篇 4·兴森 BT 07.05 篇 1·Lumentum 08.08 核实场双路来源 3）／跨篇同事实 4（鼎泰→胜宏·伟测→昆仑芯·洁美 MLCC·中船特气 WF6）·**无一为 08-13 专场带入**（并点重指边不产生同三元组）；根因=8 项校验「重复」口径是边 id 非三元组＋同篇重入库无闸＋单篇内 LLM 不查三元组；「四查」术语无文档定义·口径待专场比 kg_merge_safe 校验清单定。修法：QA 加同三元组检测＋ingest 单篇产出去重＋14 组去重手术（desc 并入 properties 不裸删））。依据：`渊图/architecture/系统概览.md` 当前数字表 · `logs/2026-08-14-渊图NVCPO量产入库.md`。

- [x] **金融 · BT-19 观星转正评估（2026-08-14 Q5B 裁「优先开」）**：✅ 已交付——36 会 PIT 重建+四闸（闸3 p=0.502 不过）→ 维持信息层三重锁；Δp_hike 入预注册观察。PRD=`logs/checkpoints/2026-08-14_BT-19观星转正评估_PRD.md`（原则轨 4 条 ✓ + 客观轨 20 条总 ✓ · Doctor 2026-08-14「都可以勾」）。2010+ 扩窗独立排队；转正执行待 Doctor 另裁。

- [x] **DVA · fuxi 单视频入口（2026-07-25 挂 · 收窄 2026-08-14）**：VV 08-13 已验证通过（Qwen3 转写 4190 字·未 seed 业务库），CC 已出 single_one.ps1 并 scp 至 fuxi。**⇒ ✅ 首跑验收完成（Doctor 2026-08-09 目标模式授权代勾 · CC 代记留痕 · 证据：VV 08-14 回报——BOM 修复后 single_one.ps1 重试成功〔SHA 801976FA…·取景框视频 7380945333871775013 下载/ASR 1/1·退出码 0·无 refill.lock〕）**


- [x] **git 三仓提交 + brain 镜像 rsync（2026-08-03 由 /todo 漏挂对账补挂 · ⇒ 2026-08-09 目标模式 Doctor 裁：收窄改写）**：**⇒ ✅ 收口（2026-08-14 Doctor 终端执行 · CC 代记留痕 · 证据：Doctor「补那 5 条 done」——08-14 凌晨批剑酒青丘/brain/行业研究/backtest 四仓已提交〔输出在盘〕+ 白泽/DVA/海螺三仓与剑酒青丘两脚本补交完成；brain 镜像 rsync 已于 08-11 裁并进 08-16 周巡检班，无需手动）**


- [x] **DVA · B 系列收口（2026-08-08 挂 · 收窄 2026-08-14）**：B1-B6 已闭环，B0/B7/PH 已裁（决策记录 2026-08-13 在盘）；B4 16 组改名冲突比对——VV 08-14 完成（1 组短 ID 重复候选 + 15 组两存，零删除）；VV 执行面并入孤儿②条。**⇒ ✅ 收口（Doctor 2026-08-14 问答板 Q1A 收窄裁定 + VV 08-14 回执 · CC 代记留痕 · 证据：VV 回执落 docs/移交VV_孤儿裁决包_20260813.md 尾部）**


- [x] **跨项目 · `.bak_audit20260728` 另 10 个散在 5 处（2026-07-30 挂 · ⇒ ✅ 已清（Doctor 终端）· 2026-07-31 补挂 TODO · 2026-08-03 /todo 重取计数）**：风险日报 ×1 / 白泽大宗 ×3 / brain ×3 / Market-Data ×1 / 烛照九阴 archived ×2。**⇒ ✅ 最终收口（2026-08-14 问答板 Q4A 裁删 · Doctor 终端 rm 清掉实余 5 个〔沙箱 find 证据正确〕；贴回的 transcript 系第二遍 rm 的 No such file 输出 · 证据：Doctor 确认「贴上来之前 rm 跑了两遍」+ 沙箱复查五路径已消失）**


- [x] **EAL · 08-12 台账 2-L p≈50% 订正（2026-08-14 目标模式补挂）**：会前保险概率 p≈50%（检索快照）vs CME FedWatch 官方 ~34.4%。**⇒ ✅ 已执行（Doctor 2026-08-14 问答板 Q8A 裁「加双口径注记」· CC 代记留痕 · 证据：事件归因台账.md 2-L 段已落「双口径注记 2026-08-14 Doctor 裁」——注册时点以检索快照为准、官方值作参照并存）**


- [x] **金融 · macro_prediction.db 择一为源（2026-08-08 挂）**：v3（macro_predictions_v3）是白泽观星引擎 engine_cn.py 写的新版口径（L662 建表），v1 是旧表；消费方=白泽观星。**⇒ ✅ 已执行（Doctor 终端 v1 改名 deprecated）· 收口（Doctor 2026-08-09 目标模式授权代勾 · CC 代记留痕 · 证据：macro_prediction.db 现表清单= _deprecated_macro_predictions/_deprecated_macro_indicators + macro_predictions_v3/macro_indicators_v3，08-14 现核）**

- [x] **白泽大宗 · P2 缓项包（2026-08-10 挂）**：NULL-source 20 行回填「人工配置」+ data_source 归一 + config_index 补 benefit_relations（08-13 已做）；剩 ingest_meta rows_written 语义 + macro v1/v3 注记 + data_hash 隐患。**⇒ ✅ 全收口（Doctor 2026-08-09 目标模式授权代勾 · CC 代记留痕 · 证据：incremental_updater.py 守卫生在盘〔grep「已退役（2026-08-13）」命中〕+ GOTCHAS 死链清单条目已补加固段 + checkpoint 2026-08-13_白泽P2剩尾收口.md 在盘；data_hash 刻意不重算〔重算=回混放大器〕）**

- [x] **渊图 · 兴森「广州兴森 2025 收入 2689.99 万/净亏 5.33 亿」两数待核（2026-08-12 由 /todo 漏挂对账补挂）**：**⇒ ✅ tushare 核证（Doctor 2026-08-09 目标模式授权代勾 · CC 代记留痕 · 证据：行业知识图谱_完整数据库.json 含注记「广州兴森收入 2689.99 万」确证有误〔IC 基板分部 16.70 亿〕·「净亏 5.33 亿」量级合理，08-14 现核）**

- [x] **金融 · 9 月加息概率实时数值源未核（2026-08-12 挂）**：**⇒ ✅ 已核（Doctor 2026-08-09 目标模式授权代勾 · CC 代记留痕 · 证据：Projects/风险日报/fomc_market_exp.json 在盘〔hold 65.6% / 加 25bp 34.4%〕，08-14 现核；Kalshi 26SEP 订单簿全空=无定价已查明）**

- [x] **渊图 · 云锗「InP 业务贡献多少业绩」未核财报（2026-08-13 挂）**：**⇒ ✅ tushare 核证（Doctor 2026-08-09 目标模式授权代勾 · CC 代记留痕 · 证据：08-13 大活日志载核证结果〔化合物半导体材料分部 2025 收入 1.38 亿/占 12.9%/分部利润 3217 万·「5.7-8.55 亿」系远期长单〕，08-14 现核）**


- [x] **`us-close-backfill` 与 `zhuzhao` 双写者职责未理清（2026-08-01 挂）**：**⇒ 2026-08-13 已解决（Doctor 裁「标已解决+补注记」）**——重盘：三写者（zhuzhao 班/launchd marketdata/launchd usclose）全部 INSERT OR IGNORE 幂等 + 直接写、无 /tmp 整库 cp 覆盖，『整片抹掉』机制已不存在；us-close-backfill 班只读看门狗。权属清单注记落 `烛照九阴/GOTCHAS.md` NOTE-20260813-001。两处诊断过时：五表→四表+intl_index、kr_stocks 表已废。

- [x] **金融 · A股首样本记账（2026-07-30 挂）**：「暂停转鹰×事前负×hold」＋事后首日弱格 obs ＋ 混杂标注。**⇒ 已做（07-30 当晚 BT-18 报告「追记 A股首样本记账·记录但 n 不增·Doctor 批」L108-118 + 07-30 日志①，含空袭带弹混杂标注）；08-03 定「补记」系记忆漂移，实际当晚已记 · CC 2026-08-13 重盘认定**

- [x] **渊图 · kg_ingest 机制修复（2026-08-09 挂）**：③ 机制修复——价格钩子幂等查重已在 `price_query.append_prices`（按 commodity/grade/price_type/as_of/source_file/horizon 去重，L145-149）；防重跑保险丝已在 kg_ingest L1094（没有新的未处理文件即退出）。**⇒ 2026-08-13 标已解决（两机制均已实装，诊断过时 · CC 代记留痕）**

- [x] **白泽大宗 · benefit_relations 银泰黄金→山金国际名称规范化（2026-08-06 挂）**：id=918 name「银泰黄金」→「山金国际」+ ts_code 补 000975.SZ；龙鱼侧 grep 零残留，白泽 archive 历史脚本静态配置留档不动。**⇒ 2026-08-13 白泽专场已做（Doctor 批 5 项全做 · CC 代记留痕）**

- [x] **两仓清账的三条尾巴（2026-08-01 挂）**：①护栏抽公共模块——护栏早已在 config.py connect_write（标已解决）②兑现变更命名——closure_engine --apply 自动留痕统一命名（py_compile 过）③sync_hot_sectors——废弃改名 _DEPRECATED_。**⇒ 2026-08-13 三尾全收口（Doctor 批 · CC 代记留痕）**

- [x] **白泽大宗 · 中际旭创 1.6T 双值核验（2026-08-10 挂）**：benefit_relations 0.4 保留 + raw_json 加口径注记（0.4 vs history latest 0.15，疑分母口径不同，原文不可得待核）。**⇒ 2026-08-13 标口径双留（Doctor 批 · CC 代记留痕）**

- [x] **★ 渊图 · `concept_XinsenBTSubstrateCustomerShare` 畸形节点还原 —— 11 个节点静默丢失 26 天（2026-08-01 挖出 · Doctor 定甲案「本批不动、另开一场」）**
  **病灶**：该节点的 `aliases` 是个 15 元素数组，其中 **12 个是 dict** —— `[3]` 是它自己的 description/properties/data_sources（故顶层 `description=None`），`[4]~[14]` 是 **11 个完整节点**被整个吞了进去。
  **⇒ 2026-08-13 目标模式代勾**（Doctor 2026-08-09 目标模式授权代勾 · CC 代记留痕 · 证据：canonical 11 节点入图 + 16 边 + 6 update + 帝尔归正并入 company_DRLaser，QA 四查全 0，nodes 3930→3912；剩 QA 第9/10项机制修复挂 TODO「08-08 三轮清洗」③）

- [x] **渊图 · 幽灵 file 专项审计（2026-08-12 补挂 · 2026-08-13 已执行）**：实测 58 真幽灵（571 引用去重 = 165 web + 25 跨命名空间 + 381 文件引用）。
  **⇒ 2026-08-13 目标模式代勾**（Doctor 2026-08-09 目标模式授权代勾 · CC 代记留痕 · 证据：校正 7 file 值 99 处 + 标 unresolvable 49 值 521 处 + 图手术（畸形还原 + 双 id 28 合并墓碑 29），canonical QA 全绿）

- [x] **brain 仓 · 中间 commit `9a531cf` 作者/message 未核（2026-08-11 由 /todo 漏挂对账补挂 · 源：`logs/2026-08-09-目标模式首验与量能回补收口.md` · ⇒ Doctor 2026-08-11 裁「贴命令终端核」）**：沙箱跑不了 git log（硬约束）；若非 Doctor 手笔需查来源。命令见 08-11 /todo 回报；待 Doctor 终端跑完贴回，CC 比对判归属后勾销。
  **⇒ 2026-08-11 目标模式收口（条内授权「CC 比对判归属后勾销」· CC 代记留痕并迁档）**：Doctor 终端 `git log/show 9a531cf` 实跑贴回——作者 **Doctor**（garciajessicadltis7409）、时间 08-09 20:15、主题「ERR-20260719-003 收口(A2双综指) + 甲案修订待裁补挂」；改动 TODO.md(+1)/烛照九阴GOTCHAS.md(8)。A2 双综指重填系 L151 所载真实 08-09 事件、message 连贯对应真实工作，判定为 Doctor 本人正常 commit，无疑问。

- [x] **财新 8/3 联手干预全文（低优先 · 2026-08-03 由 /todo 漏挂对账补挂 · 源：`logs/2026-08-03-日元能否救回与禁抛美债核验.md`）**：付费墙，FIMA 句现仅经 meta 描述 + 金十交叉确认、未读全文；Doctor 若有订阅可取全文入档补强。
  **⇒ 2026-08-11 目标模式 Doctor 裁「关闭·不做了」（FIMA 句已 meta+金十两源交叉、全文仅边际补强、付费墙），CC 代记留痕并迁档**

- [x] **dev · 定时任务模型切换落点未核验（2026-08-10 由 /todo 漏挂对账补挂 · 源：同上）**：定时任务无 model 配置项、壳层派发现为 Kimi K3，Doctor 已自行配置切换，落点未核。
  **⇒ 2026-08-11 目标模式 Doctor 裁「关闭·不做了」（模型切换落点 Doctor 已自行配置、无需追踪），CC 代记留痕并迁档**

- [x] **渊图 · CLAUDE.md 状态行顺手刷（2026-08-09 InP 入库聚簇补挂 · 琐碎 · 源：`logs/2026-08-09-InP衬底专项与入库.md`）**：下次入库顺手把「当前状态」段数字刷新——本会话已核盘上确为旧值：边 4426→4429、价格层 776→779、latest 760→763（InP 入库 commit `0961ad7` 所致）。不单独 commit，搭下次入库车。**⇒ 2026-08-11 目标模式执行（小快灵）**：`Database/行业研究/CLAUDE.md` L24/L34 已刷——关系 4426→**4429**、价格层 776→**779**、latest 760→**763**，节点 3928 不变；改前逐数现核（mapping/latest.json edges=4429 · commodity_prices.jsonl=779 行 · prices/latest.json=763 条），双 subagent 对照审查两路一致通过（agent-A 证据四数独立重算命中＋数据文件 mtime 停 08-09 未动 · agent-B 快照含旧值可 cp 回退、未触红线）。未 commit，随下次入库车。（**Doctor 2026-08-09 目标模式授权代勾 · CC 代记留痕 · 证据：CLAUDE.md L24/L34 新值在盘 ＋ 快照 `backups/todo-auto/2026-08-11-2159_行业研究CLAUDE.md` 含旧值**）

- [x] **PEC 日本线 · 抖音口播稿《日本的诚》待您审稿（2026-07-21 产出 · 2026-07-30 从 inbox 归位并补挂）**：全文约 1600 字 / 正常语速约 5 分钟，三个标题候选，含发布小贴士。**⇒ 2026-08-11 全链收口**：Doctor 裁「时长=三分钟删减版 · 口味维持现状」（竖屏分镜/多音字清单未点=不要）→ 删减版落 `Projects/PEC/case-studies/CS-08_大和-日本文明/衍生传播/抖音口播稿_日本的诚_三分钟删减版.md`（删京都茶泡饭＋齐太史两处含收束句，约 1270 字；原稿一字未动）→ **Doctor 审过**（口头勾定「球在我这的现在都做了」）。（**Doctor 2026-08-11 口头勾定，CC 代记留痕并迁档** · 证据：删减版文件在盘 · 原稿未动）
  关联：`logs/2026-07-21-日本的诚抖音口播稿.md` · `logs/2026-07-21-日本的诚配音体检.md`

- [x] **PEC 日本线 · 日元落盘包扩充（2026-08-09 目标模式末批补挂 · 源：`logs/2026-08-03-日元carry监控注册AI警报.md` L44）**：raw 落盘包四件套基础上追加 carry 三层账本 + 美股定价四渠道 + 观察框架三层。**⇒ Doctor 2026-08-11 批「照三向扩充」→ CC 起草落盘 → Doctor 把关通过**：三件全文落 `raw/2026-08-03_analysis_日元能否救回与禁抛美债核验_专项.md` §七（含 08-11 COT 口径勘误补注：非商业 6 月极值 -155,092／首破 -150k=06-16 期／08-04 期 -45,473）。（**Doctor 2026-08-11 口头勾定，CC 代记留痕并迁档** · 证据：专项文件 §七在盘 · L87 指针已改指 §七）

- [x] **基建 · 镜像常态化刷新机制裁定（2026-08-09 目标模式补挂 · 源：`logs/2026-08-02-dev模式打通四件套.md`）**：巡检镜像的常态化刷新走哪条路——并进周巡检班 vs 手动随 /save。**⇒ 2026-08-11 Doctor 裁：并进周巡检班**——scheduler-weekly-audit 班 prompt 已加「沙箱无法执行时贴 Doctor 终端双命令（巡检＋`rsync -a --delete ~/Gateway-workspace/Scheduled/ → scheduled-live-mirror/live/`）」步、description 同步（update_scheduled_task 落）；Kimi 侧班 prompt 变更监控由镜像 git diff 承载，脚本不接 GATEWAY_TREE、零改动（与 L32 定案联动闭合）。08-16 周巡检班首验并班。（**Doctor 2026-08-11 /todo 统一授权勾定，CC 代记留痕并迁档** · 证据：update_scheduled_task 返回「updated: prompt, description」＋镜像目录 20 班在盘）

- [x] **风险日报 · 成交额定源裁定（甲案）修订裁定（2026-08-09 级联复查补挂 · 源：ERR-20260719-003 收口）**：甲案前提「volume_trillion 仅 2026-06 起」已破，待 Doctor 裁 2020+ 窗口是否切源。**⇒ 2026-08-11 /todo 现核：本条已被 08-09 乙案落地消化（前提失效）**——`Market-Data/MANIFEST.md` L71-77「双源定源裁定（2026-08-09 Doctor 批·乙案，成交额条取代 07-28 甲案）」全文在盘：2020+ 统一锁 `volume_trillion`、`market_amount_daily` 降 2010 前长史专用、F4/ipo 阈值重锚 0.045→0.030 等已随案生效；另两处落点已不存在（风险日报仓无 `architecture/决策记录.md`、烛照九阴无 `architecture/` 目录、「长序列仍用 index_research」全文无命中）。Doctor 08-11 再裁「照修订切源」与盘上乙案一致，无需动笔。（**Doctor 2026-08-11 /todo 统一授权勾定，CC 代记留痕并迁档** · 证据：MANIFEST.md L71-77 乙案全文在盘）

- [x] **白泽大宗 · update_log「5 行→2 行」订正（2026-08-10 由 /todo 漏挂对账补挂 · 源：同上）**：实测 2 行，GOTCHA 435 行 + 08-08 弃用脚本注释仍写 5。**⇒ 已改（Doctor 2026-08-11 点头）**：改前复核 update_log 实测 8 行中 `data_source='测试数据'` 恰 2 行（id 7/8 嘉元 Gen4/山东黄金），GOTCHAS L435 与 `deprecate_legacy_price_tables_20260808.py` L7 两处「5 行」→「2 行」已订正。（**Doctor 2026-08-11 /todo 统一授权勾定，CC 代记留痕并迁档** · 证据：`business_breakdown.db` update_log 8 行全量 dump 实测 ＋ 两处文件 Edit 落盘）

- [x] **brain · 08-09 /save 记忆分拣三候选待 Doctor 点选（2026-08-10 由 /todo 漏挂对账补挂 · 源：`logs/2026-08-09-三轮尾账清算与todo清尾.md`）**：G-X135 Edit 误报 / EXP 清洗脚本六件套 / 失真 commit stance 三条。**⇒ 2026-08-11 /todo 现核：三条已全落 permanent（前提失效）**——G-X135（Edit 误报）· G-X137（口径双纪律 · 失真 commit 族）在 `permanent/通用教训.md`，EXP-20260809-001-P（六件套）在 `经验库.md` L1598；「不改写历史」stance 由 G-X134＋L154③＋L729③ 覆盖。Doctor 08-11 点选「三条全要」与盘上现状一致，无需补写。（**Doctor 2026-08-11 /todo 统一授权勾定，CC 代记留痕并迁档** · 证据：通用教训 L1457/L1473 ＋ 经验库 L1598 条目在盘）

- [x] **风险日报 · r7「6 月极值读数」按非商业口径回填（2026-08-08 由 /todo 漏挂对账补挂 · 源：`logs/2026-08-03-brain-todo建成与两轮实战.md`）**：AI 警报 r7 的 6 月极值读数待按 FuturesB 非商业口径回填。**⇒ 2026-08-11 执行（Doctor /todo 批「照数值回填」）**：CFTC 官方 Socrata 实测——6 月极值=06-30 期 **-155,092 张**（多 111,872/空 266,964）、首破 -150k 线=**06-16 期 -150,132**（07-28 期 -163,412 非首破），已落 watchlist r7 卡 trigger+notes 两处（改前快照 `backups/todo-auto/2026-08-11-0805_alarm_watchlist.jsonl`，改后 JSONL 7 行 parse 复验通过）；同场顺带实证 08-04 期非商业 -45,473、单周净转向 +117,939=2003 年有数以来最大。（**Doctor 2026-08-11 /todo 统一授权勾定，CC 代记留痕并迁档** · 证据：`alarm_watchlist.jsonl` r7 卡 trigger 尾部含「06-30 期 -155,092…首破=06-16 期」＋ notes 尾部含「2026-08-11 非商业口径回填」段）

- [x] **基建 · commit `9a531cf` 作者/message 未核（2026-08-10 由 /todo 漏挂对账补挂 · 源：`logs/2026-08-09-目标模式首验与量能回补收口.md`）**：沙箱跑不了 git log；若非 Doctor 手笔需查。需 Doctor 终端 `git log -1 9a531cf`（脑仓）。**⇒ 2026-08-11 Doctor 终端实跑**：Author=**Doctor 本人**、2026-08-09 20:15 PDT、message「ERR-20260719-003 收口(A2双综指) + 甲案修订待裁补挂」——与 08-09 收口场记录吻合，非外来改动。（**Doctor 2026-08-11 /todo 统一授权勾定，CC 代记留痕并迁档** · 证据：终端 `git log -1 9a531cf` 输出Author 行）

- [x] **渊图仓 · 工作区 3 个非我改未提交文件待 Doctor 认账（2026-08-09 目标模式补挂 · 源：`logs/2026-08-09-InP入库收口与TODO分流.md`）**：行业研究仓 git status 见 3 个非本会话改动的未提交文件（99 增 2 删），疑并行会话半成品或积压；待 Doctor 认账处置。**⇒ 2026-08-11 现核前提已消**：reflog 实证 08-10 晚两个 commit（`58b1fbb` r7 Obon 注记 21:55 PDT · `dbb84136` 同上+classify_holdings 落地 22:53 PDT）已把外来改动认账入史；当前 status 仅剩 CC 的 r7 回填（M watch/alarm_watchlist.jsonl·搭下次入库车）+ 3 件有档 .bak（08-15 清理批）。（**Doctor 2026-08-11 /todo 统一授权勾定，CC 代记留痕并迁档** · 证据：Doctor 终端 `git status --short` 输出 ＋ `.git/logs/HEAD` 尾两行）

- [x] **白泽大宗 · 仓 commit 确认（2026-08-10 由 /todo 漏挂对账补挂 · 源：`logs/2026-08-09-大宗库P0P1审查修复.md`）**：weekly_health.py（legacy 登记）+ `scripts/database/p1_truth_source_and_scale_20260809.py` + GOTCHAS.md 三件 commit——08-09 场命令已贴 Doctor 终端、未确认已跑。属 Doctor 终端动作。**⇒ 2026-08-11 /todo 纯文本核查闭环（沙箱零 git 子命令）**：P0 `08fafdc`（08-09 21:33 PDT）+ P1 `6589297`（22:06）已 commit，且 origin/main=6589297 于 08-10 00:27 PDT **已 push 上 GitHub**（该仓有远端 Baize-Commodity.git，非本地单点）；08-08 三场前置 commit 亦同批在远端。（**Doctor 2026-08-11 /todo 统一授权勾定，CC 代记留痕并迁档** · 证据：`.git/logs/HEAD` reflog 五行 ＋ `refs/remotes/origin/main`=6589297 ＋ origin reflog「update by push」@1786346816）
  依据：`logs/2026-08-09-大宗库P0P1审查修复.md`

- [x] **龙鱼 · classify_holdings.py 一键分态分类器（2026-08-10 由 /todo 漏挂对账补挂 · 源：`logs/2026-08-10-龙鱼持仓板并入个股库与持仓迭代.md` · ⇒ Doctor 2026-08-10 /todo 裁「立」）**：分态双轴规则（市值 30 万 × 利润率 30%、负成本=纯利不参与判定）已定量可复算，小脚本消手工重判；落 `consumers/龙鱼五力/`，不碰引擎。**⇒ 裁「立」当日 22:29 已落成**：只读复算器（数据源=board_data.build_payload 单一真源，价源回退 行情库→px_hkd/px_manual 手录，贴边 ±2万/±3pp 警示，不一致 exit 1）。2026-08-11 /todo 实跑验证：16 只持仓复算与现分态 **0 不一致**、exit 0、行情锚 20260811、分布 利润奔跑3/最小观察7/成本较高6 与 08-10 核定一致。（**Doctor 2026-08-11 /todo 统一授权勾定，CC 代记留痕并迁档** · 证据：文件在盘 mtime 08-10 22:29 ＋ 本场实跑输出 16 只全一致 exit 0）
  依据：`logs/2026-08-10-龙鱼持仓板并入个股库与持仓迭代.md`

- [x] **风险日报 · yuantu-alarm-weekly 首跑带 r7（2026-08-09 由 /todo 漏挂对账补挂 · 源：`logs/2026-08-03-日元carry监控注册AI警报.md` · dated 08-10 09:07 PDT）**：r7 于 08-03 白天注册、08-03 09:07 那班跑在注册前——**判级口径首验＝08-10 09:07 班**（班表实证 lastRunAt 08-03/nextRunAt 08-10）；scores 标度可按首跑回修。班后核 r7 是否进榜、判级是否合理。**⇒ 2026-08-10 首验通过**：r7 进榜且为本周头条（COT 日元投机净空 -101,990→-60,825 张 · 2011 年来最大单周转向），班判「有序疏解非失序螺旋」维持 warming；Obon 窗沿裁定（Doctor：窗沿+有序释放+无阈值击穿=不升级）已注记 watchlist r7 卡 notes。（**Doctor 2026-08-10 /todo 统一授权勾定，CC 代记留痕并迁档** · 证据：班表 lastRunAt 2026-08-10T16:07Z ＋ 班 transcript 简报在 ＋ `alarm_watchlist.jsonl` r7 notes 含「2026-08-10 裁定」jsonl parse 复验）
  依据：`logs/2026-08-03-日元carry监控注册AI警报.md` · `logs/2026-08-10-渊图星空常驻与观察点核验.md`

- [x] **EAL · event-attribution-watch 重生成（2026-08-09 由 /todo 漏挂对账补挂 · 源：`logs/2026-08-08-EAL口径v0.1收官.md` · dated 08-10）**：周一 2026-08-10 17:44 PT 班（班表 nextRunAt 实证吻合）读更新后正源＋重跑 export_mech 重生成 artifact；班后核产物。**⇒ 2026-08-10 班后核产物通过**：班 17:43 PT 起跑、21:44 收尾（200+ turns），台账 md 落账（2-J 全文＋记账 8 行＋验证簿＋运行记录），artifact 重生成九日曲线、同代自检全绿。班自报隐患：mech 长段数据 asof 08-05 未刷新（Database 未挂载）。（**Doctor 2026-08-10 /todo 统一授权勾定，CC 代记留痕并迁档** · 证据：event-attribution-ledger artifact updatedAt 2026-08-11T04:44:18Z ＋ 班简报自述「两件交付均落盘并核验通过」）
  依据：`logs/2026-08-08-EAL口径v0.1收官.md` · `logs/2026-08-10-渊图星空常驻与观察点核验.md`

- [x] **风险日报 · AI 面板双硬编码根治（2026-08-03 挂 · Doctor 定是否做）**：`build_risk_daily.py` 的 `AI_RISKS`（7 条）与 `ai_tech_alarm_snapshot.html` 的 `RISKS`（7 条）是**两份手工维护的硬编码**——2026-08-03 注册 r7 时已手工对齐，但日后一方改分另一方不会跟（两处真源同族病）。根治 = 构建脚本改读 `Database/行业研究/watch/alarm_watchlist.jsonl`（watchlist 已是周班维护的活真源，含 scores/kill_score），快照亦可选同源生成。**注意差异**：快照 r6=卖铲人**不在** watchlist（该条只存在于快照/脚本），合并前先裁定卖铲人归何处。**⇒ 2026-08-08 Doctor 裁定根治**：`build_risk_daily.py` 改读 watchlist + r6 卖铲人补入 `alarm_watchlist.jsonl`（单一真源）；风险日报仓未挂载，挂载后出逐文件 patch。**⇒ 2026-08-08 四件全落**：① `alarm_watchlist.jsonl` 补登 r6 卖铲人（08-03 撞号漏登清算）+ r4 U8→7/kill79→77 + r2 prox8→9 口径回填 + 全 7 行补 `display_note`；② `build_risk_daily.py` 删 `AI_RISKS` 硬编码、改 loader 读 watchlist 单一真源（fail-visible·无硬编码兜底，py_compile ✓，loader 预演与 08-07 live JSON 同序同分）；③ yuantu-alarm-weekly 班 prompt 已同步（「本周 7 个」+ 五轴/kill/display_note 归 Risk Daily 单一真源权属注记 + 顺带归一既有双 frontmatter）；④ 快照与脚本双硬编码并源完成。**待今晚 risk-daily 班首验**（构建输出无 ⚠ alarm_watchlist 行即过），过后再提请 Doctor 勾。（2026-08-09 目标模式 Doctor 裁：续挂待 09:08 班首验）**⇒ 2026-08-09 首验通过**（Doctor 2026-08-09 目标模式授权代勾 · CC 代记留痕 · 证据：refresh-risk-daily 班 2026-08-09 09:08 lastRunAt 实证跑通 ＋ risk-daily artifact 同日 09:10 刷新、AI 面板渲染含 r6 卖铲人、无 ⚠ alarm_watchlist/本轮缺失告警 ＋ `build_risk_daily.py` L43 `AI_RISKS=[]` 经 loader 读 watchlist 单一真源、硬编码已删）
  依据：`logs/2026-08-03-日元carry监控注册AI警报.md`

- [x] **烛照九阴 · daily_market.volume_trillion 历史 0-fill 回补（2026-08-08 错题本复盘补挂 · 源：ERR-20260719-003）**：该列 20260603 前 1552 行填 0 而非 NULL（名义覆盖 1584 日、实际非零仅 32 日），滚动分位恒≈1.0 失真；同族 `max_consecutive` 一并回补。回补路径＝tushare 大盘接口（**Doctor 终端跑**，沙箱不下载）；回补前长历史量能研究按条目口径用 `index_research.db` 000001.SH / 399006.SZ。回补后回写 ERR-20260719-003 状态行。**⇒ 2026-08-08 脚本已交付、待 Doctor 审后终端跑**：`backfill_daily_market_volume_20260808.py`（dry-run 默认 · 指数/本地双口径校验贴库率 <80% 即中止 · `.market-data-writer.lock` 单写者锁 · backup API 快照 · UPDATE 只命中 0/NULL · 写后行数守恒+integrity_check；落位 `Projects/Financial/剑酒青丘/infrastructure/取数工具/` 待定）。**⇒ 2026-08-09 CC 通读核对（Doctor 令「你核对一下」）**：防护五件套逐条在码属实；**三点报 Doctor**——① 口径断点（旧段 ~840 只池只能走 tushare 指数口径 000001.SH+399001.SZ 合成 vs 既有值 ≥5000 只池本地加总，系统性小差预计 <2%）接不接受须 Doctor 裁，dry-run 先实测印报告；② `max_consecutive` 脚本只诊断不写（定义未核，08-08 刻意收窄），该列回补须定义核准后另做；③ 脚本在 session outputs 区未落项目正式位（建议先 cp 落位再跑，命令见 08-09 /todo 场回报）。跑法：先默认 dry-run 看现状+校验+拟回补行数 → 断点可接受后 `--apply`（~1552 行 × 限流护栏，约一刻钟；需 TUSHARE_TOKEN 于 env 或 `~/Documents/Database/.env`）。**⇒ 2026-08-09 Doctor 终端真写完成**：回补 **1550/1552**（20200928、20220802 tushare 超时缺数 · 脚本幂等、重跑即补）· 行数守恒 ✓ · integrity_check ok · 快照 `market_data.db.bak_20260808_volume` 落 Market-Data 目录。**⚠ 口径断点实测 ~22%（远大于脚本预估 <2%）**：dry-run 校验=既有非零值 10/10 贴 B 本地口径（差 0.0%）、0/10 贴 A 指数口径（差 20~23%）——而旧段只能落 A 口径（000001.SH+399001.SZ 合成，399001.SZ 为深成指非深市全量，疑缺创业板等大头），故新库 = 旧段 A 口径（系统性低 ~22%）+ 20260603 起 B 口径（≥5000 只池本地加总）拼接，**跨断点分位比较会偏**（窗跨 20260603 时旧段偏低 ⇒ 现值分位偏高）。⇒ 2026-08-09 Doctor 裁「先零写库验证再定」：A2 双综指（000001.SH+399106.SZ）对近期 B 口径 10/10 样本差 -0.6~-0.8%（根因坐实=399001.SZ 深成指缺深市非成分；补创业板 399006 仍差 6~10%）→ Doctor 批 A2 重填，`refill_daily_market_volume_a2_20260809.py` 真写 **1552/1552**（v1 两超时行本次补齐）· 行数守恒 + integrity_check ok · 快照 `market_data.db.bak_20260809_volume_a2`。**终态：全列统一「全市场成交额」口径——旧段 A2 ≈ 新段 B，缝差 <1%，跨缝分位恢复可比；恒≈1.0 失真与 22% 台阶两失真俱消**。ERR-20260719-003 状态行待回写（口径=A2 · 烛照九阴未挂载）；两 .bak 快照搭 08-15 批次清理车。**⇒ 2026-08-09 收口**（Doctor 2026-08-09 目标模式授权代勾 · CC 代记留痕 · 证据：`market_data.db` `daily_market` 20260603 前 1552/1552 非零、最老 20200102、覆盖 2020–2026 ＋ `brain/烛照九阴/GOTCHAS.md` ERR-20260719-003 状态行已 ✅已解决(2026-08-09 A2 双综指口径)——本条自述「待回写」系滞后，实际已落）

- [x] **★ dev 模式打通 · E 验收（2026-08-02 挂 · A–D 已落地 commit `782b404`，E 未跑）**：开发者模式切 Kimi/DeepSeek 实跑 `/resume`，合格线三条——①自己找到 `~/Documents/Claude/brain` 给出结构化交接；②对 Doctor 用「您」；③给结论带「核过没有/有什么隐患」两问。唤「白泽」验 symlink agent 兼容性（**无先例，未核**）+ 引擎路径（`Projects/Financial/白泽观星/engine/`）。可加测 `agents/灵魂校验题.md`。**验收结果（尤其跑不过的条目）落盘 = L4 保真度第一份实测基线。在 E 通过之前，「CC 在第三方模式还在」只是结构就位，不是行为验证。** 已装内容：bootstrap `~/.claude/CLAUDE.md`（cp 自 `portable/claude-code/`）· 6 skill symlink（真源 `portable/skills/`）· 3 agent symlink（真身 `agents/{灵}/{灵}.agent.md`）· live Scheduled 镜像 `references/scheduled-live-mirror/live/`（刷新纪律见其 README）。旧件在 `~/.claude/_archived_20260802/`。**⇒ 2026-08-09 E 验收通过**：Doctor 实跑 dev 模式 `/resume`，三合格线全过（「验收做完了，没问题」）。（**Doctor 2026-08-09 口头勾定，CC 代记留痕并迁档**）

- [x] **风险日报快照 r6/r7 渲染目验（2026-08-03 由 /todo 漏挂对账补挂 · 源：`logs/2026-08-03-日元carry监控注册AI警报.md`）**：r6/r7 象限标签间距是估算；risk-daily artifact 已于 2026-08-03 09:27 更新（list_artifacts 实证），r7 卡应已上线——现在即可目验，标签重叠则调 OFF。**⇒ 2026-08-09 Doctor 目验：r6/r7 标签不重叠，通过，无需调 OFF。**（**Doctor 2026-08-09 口头勾定，CC 代记留痕并迁档**）

- [x] **渊图 · batch 日期漂移汇总行（原「渊图 1 件」之① · 2026-08-08 由 /todo 漏挂对账补挂 · 源：`logs/2026-08-05-渊图3篇入库_CCL年份偏移修补.md` ＋ `logs/2026-08-06-渊图4篇入库.md`）**：batch 收尾加「解析日期≠文件年份」显式汇总行（07-28 已建议未实装，已四次复发——药明康德 07-13→07-09、美迪西 07-17→07-15 且两轮错得一模一样＝可复现系统性错位；价格层 as_of 同事实三轮各安 07-10/07-16/07-11）。**⇒ 2026-08-09 收口**：`kg_ingest.py` 价格钩子后插漂移记录点（`report_meta.date` / `data_vintage` / `as_of` 三方对文件名日期，不一致当场 ⚠ 并累计）、batch 收尾加漂移汇总段（0 篇漂移也显式报 ✓）；纯报告性、不改任何数据、零入库行为变化，py_compile ✓。首验＝下次 batch 入库。（**Doctor 2026-08-09 勾定 · CC 依 2026-08-03 长期授权执行并留痕**）

- [x] **渊图 hold 6 篇清算入库（原「渊图 2 件」之② · 2026-08-08 由 /todo 漏挂对账补挂 · 源：`logs/2026-08-05-渊图3篇入库_CCL年份偏移修补.md` ＋ `logs/2026-08-06-渊图4篇入库.md`）**：`raw/_hold_跨域待定/` 积 6 篇（量子科技 07-09／药明康德 07-13／油运 07-16／CXO 07-17／AI 治理 07-17／太空算力 07-30）→ Doctor 裁定全入库、移回 MD 通道。**⇒ 2026-08-08 收口**：首次 batch 空跑——index.json 残留 6 条 `kg_processed=true`（上次 batch 打标、promote 前被 hold），去重跳过；置 False 重跑后 6 篇全入（新节点 66／更新 40／新关系 57 · 价格层 +9），**kg_promote 首战全绿**（3894 节点／4389 边 · 悬挂=0 自环=0 非法type=0 丢失旧内容=0），wiki 641 卡刷新，commit bdfff54 推 Yuantu/master。衍生留账：`index.json.bak_20260808_hold6` 搭 .bak_20260808 批次（08-15 后）清理；药明康德篇日期解析错＝「解析日期≠文件日期」第四次复发（① 仍在挂）。（**Doctor 2026-08-08 勾定 · CC 依 2026-08-03 长期授权执行并留痕**）

- [x] **EAL 回测库 · events 表补 `trade_date` 列（2026-08-08 由 /todo 漏挂对账补挂 · 源：`logs/2026-08-06-回测库建成移交VV与台账v1.3.1闭合.md`）**：周末事件映射规则写死（方向①终审复算差一天的根因；谁执行都行）。2026-08-08 现核：`Database/剑酒青丘/backtest/attribution.db` events 表 25 行、仍无该列。涉 DB 写，执行前需 Doctor 批。**⇒ 2026-08-08 Doctor 批 CC 执行**（先 dry-run 报 diff、点头后才真写）；库未挂载，挂载后开做。
  **⇒ 2026-08-08 收口**：列已落库（events 第 7 列 `trade_date TEXT`），25 行回填守恒——17 当日 + 4 顺延（02-28 开战→03-02、06-14 MOU→06-15、08-02 两件→08-03）+ 4 NULL（NFP 08-07 / Jackson Hole 08-27 / FOMC 09-16 日历未及 + '2026-05' 月级 MOU 粒度不足）；integrity_check 前后及真库三重 ok。口径三方写死：当日或之后首个 SPY 交易日（= `trade_day_on_or_after`，越窗/月级留 NULL）。`update_attribution_db.py` 已插防腐钩子（commit 前只补 NULL、幂等、异常不阻塞发布），`知会VV-events表trade_date列_20260808.md` 落 backtest/。首验观察点＝VV 下次发布应打印「补映射 1 行」（NFP 行 NULL 自解）。（**Doctor 2026-08-08 勾定 · CC 依 2026-08-03 长期授权执行并留痕**）

- [x] **看门狗班沙箱挂载缺失治理（2026-08-03 第二轮 /todo 逮到 · Doctor 定「CC 查配置方法再报」）**：`us-close-backfill`（14:30 看门狗）启动时沙箱**未挂载**烛照九阴项目与 Market-Data 目录（仅 brain + 白泽观星/engine），本轮靠临时申请获批才跑通核对；不补则每轮 14:30 都要人工批一次、无人值守时即失明。**下一步**：CC 查 scheduled task 的目录授权/挂载固化机制，出可批方案。同类班（zhuzhao / market-data-daily 等）是否同样缺挂载，一并扫（G-X111 同族扫）。
  **进展（2026-08-08 /todo 现核）**：机制查明——`references/scheduled-live-mirror/README.md` 明记沙箱挂载根被管理员限在 `~/Documents`，**无全局固化入口**，惯例是各班 SKILL.md 自写「前置挂载确认」段（sentinel/recap-ingest 班均有）。同族扫：20 班 08-07 全部正常点火（lastRunAt 逐班过），仅本班 08-03 报过缺挂载。**剩余**：给本班 SKILL.md 补挂载前置段——文件在 Gateway 保护区，需 Doctor 贴该班现 prompt（由 CC 走 update_scheduled_task 改）或 app 侧加挂载授权。
  **⇒ 2026-08-08 收口**：前置段已补入——SKILL.md 新增「前置〇：挂载」段（缺挂载即用 `request_cowork_directory` 申请 Database + 烛照九阴两目录 / `ls /sessions/*/mnt/` 确认 / 挂不上则简报明写「失明可见」再停）＋「前置：路径」cd 行改 `/sessions/*/mnt/烛照九阴` glob 优先；Doctor 批准草案后 CC 走 update_scheduled_task 落盘、回读验证（段在 L35-39、cd 在 L44），其余内容未动。首次实战检验＝08-10 14:30 班。（**Doctor 2026-08-08 勾定，CC 代记留痕并迁档**）

- [x] **Artifacts · `touzhijunjun-workflow` 幽灵查证（2026-08-02 挂 · Artifact 层盘点时逮到）**：盘上有目录（12K，含 index.html），`list_artifacts` manifest 返回的 **6** 个里没有它——「盘上有/清单无」第三例。候选定性：旧 workflow 卡片被 artifact 化后又从 manifest 摘除，目录残留（index.html mtime＝2026-07-05 10:46，与 workspace 整根拷贝事件同一分钟，大概率 7-05 迁移残留）。**⇒ 2026-08-08 实核收口**：`ls ~/Gateway-workspace/Artifacts/` 示该目录已整个从盘上消失（live 6 个正好＝manifest 6 个、无它；`_archived` 里亦无）——查证对象不存在、前提消失、清理目的已达（被删而非归档；artifact 可由其班再生，风险低）。（**Doctor 2026-08-08 勾定 · CC 依 2026-08-03 长期授权执行并留痕**）

- [x] **Artifacts · `龙鱼五力个股库看板` 幽灵归档（2026-08-03 挂 · 数据根搬迁清点时逮到）**：`~/Gateway-workspace/Artifacts/龙鱼五力个股库看板/`（index.html mtime 2026-07-05 20:28）不在 manifest 的 6 个之内——「盘上有/清单无」第四例，07-05 拷贝事件族，上代看板残留躯壳。处置已定（D14）：照 handshake 先例归档。依据：[[数灵转移/architecture/决策记录]] D14 搬迁账目 · `logs/2026-08-03-数据根迁Gateway-workspace.md`。**⇒ 2026-08-08 实核收口**：已归档——`_archived/龙鱼五力个股库看板_DEPRECATED_20260803` 在、live 旧壳已无（`_archived` 目录 mtime Aug 3 00:58，即挂条当日移入）；live 的 `longyu-stock-library`（08-06）即其新身。（**Doctor 2026-08-08 勾定 · CC 依 2026-08-03 长期授权执行并留痕**）

- [x] **brain · CLAUDE.md 项目列表「渊图 最后工作」漂移归正（2026-08-08 由 /todo 漏挂对账补挂 · 源：`logs/2026-08-08-渊图光模块双讯核实与对冲定性.md`）**：列表写 2026-07-03，实际 08-06 promote、08-08 两场 → 归正为 2026-08-08（CLAUDE.md L107 单格改动）。（**Doctor 2026-08-08 勾定 · CC 依 2026-08-03 长期授权执行并留痕**）

- [x] **经验库 · 7 个悬空引用查证（2026-08-02 挂 · 重编号场同轮揪出 · 自「重复编号」条拆出独立成条）**
  **7 个悬空引用**：全库 86 个被引用的 EXP id 里，**7 个在经验库中零条命中** —— `EXP-20260607-001`(1处) · `EXP-20260607-008`(1) · `EXP-20260613-005`(1) · **`EXP-20260617-004-P`(3处·最多)** · `EXP-20260625-001`(2) · `EXP-20260723-003`(1) · `EXP-20260727-005`(1)。
  **归属已判明：不是本次改号造成的**——本次只动 14 个 id，每个旧号都还留 1 条，新号全经「全文零出现」预检；这 7 个无一在改动清单内。`EXP-20260617-004-P` 尤其能证明：取新号时正因它**在正文被提及**而占了序号 4、才跳到 005，但它**从来没有对应的 `###` 条目**。
  **性质**：与撞号相反且**更隐蔽**——撞号是「一号指两条」（至少还能跳到某条）、悬空是「一号指零条」（彻底断链，且 `[[经验库#EXP-…]]` 点了没反应，容易被当成渲染问题而非数据问题）。
  **下一步**：逐个查这 7 个的引用上下文，判是①编号笔误（改引用）②条目被改名（补别名或改引用）③条目从未写成（补写或删引用）。**需 Doctor 参与判 ③**。
  **⇒ 2026-08-08 /todo 逐条现核收口**：**3 假悬空**——`0607-001`/`0607-008`/`0727-005` 系日志区间简写被边界 grep 误捕，实指 `-P` 后缀条目均在；**2 后缀省略已消歧**——通用教训 L288 改 `EXP-20260613-005-P／006-P`；龙鱼 GOTCHAS 自编号撞经验库名空间，改 `NOTE-20260625-001`（L32）＋系统概览 L15 引用同步；**2 真悬空已补**——`0617-004-P` 条目头补 -P（L965，3 处既有引用全接通）；`0723-003` 删源收官三闸条目补写落经验库 L158。复扫：全库裸 005 / 裸 0625-001 残留＝0。（**Doctor 2026-08-08 口头勾定，CC 代记留痕并迁档**）

- [x] **哨兵班明早 02:40 自然确认（2026-08-03 由 /todo 漏挂对账补挂 · 源：`logs/2026-08-03-哨兵班400风控二分定位.md`）**：手动终验已过（今日 03:47 手动 Run now，注册表 lastRunAt 实证）；若 08-04 02:40 自动点火再 400 则存在组合效应，需重启探针。（**2026-08-08 /todo 现核勾销**：`baize-breakout-sentinel` lastRunAt=2026-08-07 02:40 PDT 正常点火，08-04~08-07 四场日志无一再提 400，窗口已过、无组合效应——Doctor 2026-08-08 勾定 · CC 依 2026-08-03 长期授权执行并留痕）

- [x] ★ **`us-close-backfill` 修复版首跑核验（2026-07-30 挂 · **2026-08-01 全条重写：首跑已发生且已零写入，四失败面已根治并装机，本条时效改为周一 08-03**）**
  **原条已失效**：写的是「`lastRunAt` 不存在＝从未跑过，首跑就是 08-01」。实际 **07-31 13:34 PDT 已首跑**（`lastRunAt`=2026-07-31T20:34:45Z），但**库里零写入**——`us_anchor_daily` 07-31 零行、`intl_index_daily` 美股腿零行，且**简报从未取到**。
  **08-01 已查明四个独立失败面并全部根治**（详见 `logs/2026-08-01-us-close-backfill四失败面根治.md`）：**F1** `cd` 两候选全摔（沙箱 `~/Documents` 不存在、`/mnt/` 空）· **F2** 挂载盘直写 `disk I/O error`（**比 F1 致命，cd 修好也写不进**；原 SKILL 全文无 `/tmp` 副本段）· **F3** ~~`--source yfinance` 已死~~ **系误判、当场证伪**（那是历史 choice 名，实走 urllib 直取 Yahoo chart）· **F4** 缺 G-X51「无人值守绝不 request」（**这条解释了为何连简报都没有**：request → 悬挂 → 超时杀）。
  **已装**（2026-08-01 · 备份 `SKILL.md.bak_20260801` · `diff` 逐字一致）：挂载探测段 + `/tmp` 副本两件套 + 放回校验 + mtime 并发判据 + 核对段去 env + yfinance 措辞订正，90→约 160 行。
  **⏸ 待核（窗已改 · 2026-08-03 /todo 现核改写）**：**班已于 08-01 09:00 重构为只读看门狗**（cron 14:30 PT · description「绝不写库(G019)」· 注册表实证），写库迁 launchd `com.zhuzhao.usclose`（14:00 PT）——出处 `logs/2026-08-02-定时任务巡检机制.md` §一。新核验窗 = **今日 14:00 launchd 首跑 + 14:30 看门狗简报**：① `us_anchor_daily` 当日 19 票是否补上 · ② `intl_index_daily` 美股腿（NASDAQ/SPCX/NVDA/AVGO/LITE）是否补上 · ③ **简报这次有没有产出**（F4 修没修好看这个）· ④⑤（放回只增不减校验 / 并发判据）**随 /tmp 副本写法退役而失效**（zhuzhao 班自身的放回校验是另一条线，不在本条）。⚠ 美股腿当前停 07-31 属正常（08-01/02 为周末）。
  **⚠ 别当已结案**：四个面都是实测坐实的，但「零写入**就是**它们造成的」仍是**推断**——首跑简报始终没拿到，那才是决定性证据。**若周一仍零写入 ⇒ 存在第五个失败面。**
  **✅ 2026-08-03 晚核验全绿**：launchd `com.zhuzhao.usclose` 14:00:27 首跑落 8/8 外盘 + 19/19 anchor；看门狗 14:30 简报产出且达标；CC 独立查库复核一致（`us_anchor_daily` 08-03 共 19 票落后 0 天 · intl 美股腿 NASDAQ/SPCX/NVDA/AVGO/LITE 全到 08-03）。①②③ 全过、④⑤ 随旧写法退役。第五失败面未出现。**遗留新事**：看门狗班启动时沙箱缺烛照九阴+Market-Data 挂载（本轮临时申请获批才跑通）——另挂 TODO 治理。（**Doctor 2026-08-03 勾定，CC 代记留痕并迁档**）

- [x] **PEC 日元落盘包（2026-08-03 挂 · 待 Doctor 批方向）**：① raw 一篇（日元能否救回全链推演 + 禁抛美债核验纠错留痕）；② `predictions-register` JP-P2 对账快照 + JP-P2a 观测追加（上半年净卖美债 $80B+ 记「机制混杂、信号部分反向」不判证伪 + 联手干预/FIMA dated 增量）；③ macro-facts §19 刷新（干预累计 ¥11.73 万亿 / 日本美债持仓 5 月 ~$1.143T / FY2026 国债费申请 ¥32.39T≈26.5%）；④ CS-08 A03 §5.3 摊牌触发条件第 3 条 dated 增量（2026-01 日债六西格玛 + 2026-07/08 许可制干预落地）。观察点：10 月日银会议（市场定价 80% 加 1.25%）· 2027 CPI 回 2% 时终端是否停 ≤1.5%（JP-P2 ① 腿真考验）。另：Doctor 若持贝森特「禁止抛售」逐字出处 → 入档补强（现分级：功能等价坐实、逐字待证）。
  依据：`logs/2026-08-03-日元能否救回与禁抛美债核验.md`
  **✅ 2026-08-03 当日完成**：四件套全落并自验——`raw/2026-08-03_analysis_日元能否救回与禁抛美债核验_专项.md` 新建 + register 两处 dated 追加（概率 70% 未动）+ macro-facts §19「2026-08 流量刷新」子节 + A03 §5.3 第 3 条补注（管理权易手）。（**Doctor 2026-08-03 勾定，CC 代记留痕并迁档**）

- [x] **第三方壳 · Artifacts/定时任务 分裂脑治理（2026-08-02 E 验收补测挖出 · 定时班侧已清、artifacts 侧残留 · 待您勾）**：第三方模式本体（Kimi 壳）里 `scheduled-tasks` 与 `artifacts` 两个 MCP 后端是 **07-01 被遗弃的原 store**（本壳注册表 + 旧数据根 `~/Documents/Claude/{Scheduled,Artifacts}`；官方活树在 `~/Claude's workspace/`）。**治理已执行（C 案 · Doctor 批）**：11 个僵尸班全部删除、复 list 验证本壳定时班 = 0，明晨 09:06 观察窗作废；artifacts 侧 5 个旧 manifest 条目 Doctor 手动删除、复 list 验证 = 0。**分裂脑清零，本壳两子系统均为「干净为空、保持为空」**；凡建/改一律回 Cowork 侧。
  **剩余**：无（① 观察窗已作废 · ② 载体已定位 · ③ 写侧归属已推定 · ④ C 案已执行）。勾掉后按 v3.1 迁归档。
  依据：`logs/checkpoints/2026-08-02_E验收_L4保真度基线.md` §六（含载体定位与治理执行）
  **2026-08-03 /todo 首轮佐证**：本壳 `list_scheduled_tasks` = 19 班、`list_artifacts` = 6 条，全为 Gateway live store 内容，与迁移后架构一致。（**Doctor 2026-08-03 /todo 首轮勾定，CC 代记留痕并迁档**）

- [x] **dyd 侧 dy_downloader.db 旧副本核实**（2026-07-21 挂 · 低优先 · Doctor 定「留原地挂 TODO」· **2026-07-23 核实：不移**）
  `Claude/Projects/DVA/dyd/dy_downloader.db`（110MB，07-13）比 ops 活跃本体（`DVA-ops/runtime/`，07-18）旧 5 天；核 dyd 本地开发流是否还读它——不需要则移隔离区，避免开发误用旧库。
  **2026-07-23 核实结论**：① dyd fork 自己的开发代码（`config/default_config.py`/`cli/main.py`/`asr_clean.py`/`storage/database.py`/`refresh-cookie.py`）**确引用本地 dy_downloader.db**——非孤儿，dyd 本地开发流在读它 → **按可逆优先，不移**。
  **2026-07-24 悬案解决**：「ops 活跃本体」定位到 **`Database/Douyin/DVA-ops/runtime/dy_downloader.db`**（07-23 08:43·活跃·含 offsite 列，非 Projects 下故前次没找到）。dyd 副本（07-13·无 offsite 列）确是**旧开发库**。**待 Doctor 拍板**：dyd 本地开发流是否改指向 `DVA-ops/runtime` 活跃库（架构选型）；不改则 dyd 旧库留原地（已定不移）。
  **✅ 结案（2026-07-31 实核 · 上面 07-24 那段的三条事实现已全部失效，本条可销账，待您勾）**——
  ① **对照目标已不存在**：`Database/Douyin/DVA-ops/` 现只剩 `failures/state/summaries/tmp`，**无 `runtime/` 子目录**；那个库 07-25 被整体快照进 `DVA-ops.pre-refresh-20260725T054523Z/runtime/`（07-23 08:43·1559 行/39 作者/offsite=1 共 1556）。
  ② **dyd 库不是旧开发库，是活的**：mtime **2026-07-31 03:27**·113MB·**offsite 三列齐全**（07-24 记的「07-13 / 110MB / 无 offsite 列」三条全不成立）。1396 行 / 37 作者。
  ③ **03:27 那次写入查实＝人为单链下载**：`download_history` id=179 · `https://v.douyin.com/kec3SLI0RRQ/`（短链单条）· `download_time=1785493672`＝07-31 03:27:52 PDT · total=1/success=1 · config 里 `path=…/Database/Douyin-2nd/Downloaded/` `thread=3` `headless=false` `link=[单条]`。**18 个 live 调度里没有任何 DVA/dyd 下载班**，03:27 也无任何班 ⇒ 非残留调度。即 TODO「DVA·fuxi 单视频入口」条里写的那条 **Mac 保底线**（`dva-single.sh --force-local`·产物落 Douyin-2nd 第二线根）。按日聚合佐证：07-31 +1 / 07-29 +4 / 07-13 +1 / 07-05 +5（全个位数＝单链手动），而 6 月是 18–29 条/日（批量线）——**此库自 07-02 起只吃单链**。
  ④ **`offsite=1` 计数为 0 不是 bug**：单链产物留在 Mac 本地 `Douyin-2nd`，从未外移 fuxi，offsite 本就该恒 0（另两个库 1434/1556 是批量线外移后的结果）。
  **⇒ 架构结论：不改。** dyd 库是「Mac 单链保底线」的当前真相源，**不该指向任何 Mac 归档库**；原问题的两个候选里没有一个是「该切过去的活跃批量库」——批量线真相源在 fuxi 上（07-24 完全 fuxi 化之后）。三个 Mac 库行数/作者数互不包含（1396/37 · 1459/34 · 1559/39），是**三条各自演化的线**，不是同一谱系的新旧副本。
  **2026-08-03 /todo 首轮复核**：结案四条事实全部成立（`aweme` 1396 行 · offsite 三列齐 · mtime 07-31 03:27 · `DVA-ops/` 无 runtime/）。（**Doctor 2026-08-03 /todo 首轮勾定，CC 代记留痕并迁档**）

- [x] **烛照九阴 · 复核「US10Y 0.09pp 归因」→ ✅ 当日完成，质疑不成立、原归因成立（2026-07-30 挂于日志 · 2026-07-31 补挂 TODO 并当日结案，可销账待您勾）**
  **⚠ 本条补挂时自身就带着两个错**（CC 照抄 07-30 日志的遗留段，没重取核对，与当日已连撞四次的是同一个病）：
  ① **编号错**——该归因**不在 G030**（G030 是 `ticker_resolver` 种子源失联静默降级，与 US10Y 毫无关系），在 **G031「预防措施 ③」**：「`US10Y` 6 月起若干 0.09pp 级差异属 2dp 收盘价四舍五入，非本坑」。提出质疑的是 **G033 的「衍生待办」段**（`Projects/Financial/烛照九阴/GOTCHAS.md` L690），错号从那里起、经 07-30 日志传到本条。
  ② **结论也反了**——原以为「2dp 误差上限 0.005 解释不了 0.09」，实测**恰恰解释得了**。
  **实测（`market_data.db::intl_index_daily` code=US10Y · 20260601 起 42 个交易日 · 只读）**：逐日以表内 `close` 重算 `pct_chg` 与存值对照 ⇒ **差 >0.02pp 的 31 天，超出 2dp 舍入传播上限的 0 天**；最大差 **0.2239pp @ 20260702**，当日上限 0.2242pp，压线在内。
  **质疑错在量纲**：拿 **close 的绝对舍入误差 ±0.005** 比 **`pct_chg` 的差 0.09pp`**。`pct=(c/prev−1)×100`，舍入误差经两条腿各放大 `100/prev`，yield≈4.6 时约 **43 倍**，上限 `100×(0.005/prev + c×0.005/prev²) ≈ ±0.217pp` ⇒ 0.09pp 在噪声内。**⇒ 四问（日期/时点/语义/源）之外还得加一问：量纲与传导。**
  **已落盘**：`Projects/Financial/烛照九阴/GOTCHAS.md` L690 的衍生待办段已改为「已复核结案」（原文划线保留、不删），并写明 **G031 正文一字不改**、US10Y 的 0.09pp 与 G033 读数语义**无关**、勿再混为一谈。
  **2026-08-03 /todo 首轮复核**：源头 GOTCHAS L690 状态行 =「✅ 已复核结案（2026-07-31）」，与条内一致。（**Doctor 2026-08-03 /todo 首轮勾定，CC 代记留痕并迁档**）

- [x] **brain · 扫 TODO 里其余的二手名单（2026-07-31 挂）**：07-31 只订正了「系统概览缺口」这一条名单，**同类风险未扫**。**当日又连撞三条同病**——`P-11「15:30 ET 待坐实」`（其实当日已坐实）· `dyd 库「07-13 旧副本·无 offsite 列」`（实为 07-31 仍在写的活跃单链库，offsite 三列齐全，且对照目标 `DVA-ops/runtime` 已不存在）· `import-transcripts 治本①`（2026-07-24 就做完了，见 `dva.js` L1517-1524 与当日专场日志）。⇒ **TODO 里凡是「引用某个数字/名单/路径」的条目，引用前都要重取一次**；本条要做的是**逐条过一遍待办、把已失效的前提标出来**。
  **✅ 2026-08-03 由 /todo 首轮执行完毕**：30 条逐条现核，逮到 3 处名单/计数漂移（系统概览注册数 15→16 · `.bak_audit20260728` 计数 8→10 · 烛阴课件日志「记 190 实测 192」指控不实）+ 2 条大前提失效（`us-close-backfill` 已重构为只读看门狗 · 双写者已加单写者锁），均已按 Doctor 批改写进对应条目。（**Doctor 2026-08-03 /todo 首轮勾定，CC 代记留痕并迁档**）

- [x] **定时任务 · `handshake-consumer-daily` 幽灵查证（2026-08-02 挂 · 镜像 rsync 时逮到）**：live 磁盘树 `Claude's workspace/Scheduled/` 有其目录，但当日 `list_scheduled_tasks` 返回的 19 班里**没有它**——删班留目录，还是调度器有一层未返回？与 08-02 日志「第三个 launchd job 不在任何清单」同族、方向相反（盘上有/清单无）。查法：侧栏找该班；或下次周巡检看 snapshot 是否报差。~~**未核，勿据本条下结论。**~~
  **✅ 2026-08-02 /consolidate 结案**：`permanent/定时任务清单.md` L10（2026-07-01 条）明载「方案 B 的 handshake-consumer-daily **已搁置、不重建**」——07-01 切回官方工作区重建 10 班时刻意搁置，目录是搁置前的残留。残目录已于当日归档进 live `_archived/`。**本条可销账，待您勾。**
  （**Doctor 2026-08-02 口头勾定，CC 代记留痕并迁档**）

- [x] **workspace 7-05 旧副本处置待裁（2026-08-02 挂 · 当日 F 方向未批，先定性不动）**：`Claude's workspace/` 下 Brain / BRAIN_VAULT.md / Env / Infrastructure / Projects **mtime 全部定格 2026-07-05 10:46 同一分钟**＝一次性拷贝事件；live 方向按资产劈开、恰好相反（Brain/Projects live 在 `~/Documents/Claude`，Scheduled live 在 workspace）——07-31「Scheduled 双树」是这个几何的一半。风险：旧副本不再被写，但可能被未来会话**静默误读**。候选处置：照 Scheduled 死树先例标死（README 或 _DEPRECATED_ 改名）；**动手前先跑 `find "/Users/lunarabbit/Claude's workspace/Brain" -newermt 2026-07-06 | head` 验零写入**。详 `logs/2026-08-02-dev模式打通四件套.md`。
  **✅ 2026-08-02 处置完成**：`find -newermt 2026-07-06` 零输出验毕零写入，`_DEAD_COPIES_README_20260802.txt` 已落 workspace 根（Scheduled/Artifacts 两例外注明）。（**Doctor 2026-08-02 口头勾定，CC 代记留痕并迁档**）

- [x] **`permanent/经验库.md` 10:03 并发改动查证（2026-08-02 挂 · 扫尾批时逮到）**：该文件 mtime 2026-08-02 10:03:11——在 Doctor 09:52 提交 `698f643` **之后**又被动了一次，而今日编号条目仍只有昨夜 `EXP-20260802-001-T` ⇒ 有未知会话/定时班在改**既有内容**（非新增条）。周日 10:03 无任何已知班在跑。查法：`cd ~/Documents/Claude/brain && git diff permanent/经验库.md`；无异常随下次 /save 批提交，有异常回溯写者。~~**未核，勿据本条下结论。**~~
  **✅ 2026-08-02 当日结案**：写者查明＝Doctor 并行开的「EXP 重编号」场，合法写入，已自行提交 **`50fd6d2` 经验库: EXP id 撞号 14 组全清(284 条守恒)**。⇒ 本条与「经验库 · 14 组重复编号致 11 处引用歧义」那条**双双可销账，待您勾**（后者的 11 处引用是否已同步改，以该场自己的记录为准，本条不代核）。
  （**Doctor 2026-08-02 口头勾定，CC 代记留痕并迁档**）

- [x] **经验库 · 重复编号 → ✅ 14 组全清（2026-08-02 完成，待您勾）；⚠ 但同轮揪出 7 个「悬空引用」，本条待办改指后者**

  **✅ 已完成（2026-08-02）**：撞号 **14 组 → 0**，条目数全程守恒 **284 → 284**（纯改号、零增删、正文一字未动）。
  **分两批做**：① **8 组无外部引用**——机械改号，规则「先出现的留原号」；② **6 组被外部引用**——**逐条读引用上下文判「哪条留原号」**。
  **② 值得记的一点**：`20260707-001-P` / `20260724-001-P` / `20260730-001-P` **三组要留的是「后出现」那条**，与①的规则**完全相反**。若机械套用规则，这三组会把现有 8 处引用**全指错**，而且指错后**看起来完全正常**（id 存在、格式合法、能跳转，只是跳到另一条上）。⇒ **凡改动会影响引用锚点的，判据只能是「引用上下文在说哪一条」，不能是任何位置/顺序规则。**
  **唯一真歧义组** `20260624-009-P`（渊图决策记录指【过关门槛】、通用教训指【artifact 漂移修法】）Doctor 定：**A 留原号**，同步改通用教训那一处引用 → `EXP-20260624-010-P`。渊图决策记录未动。
  （**Doctor 2026-08-02 口头勾定，CC 代记留痕并迁档**）（7 个悬空引用的后续已拆出独立成条，见 TODO）

- [x] **brain · 悬空链接清理 → ✅ 25 条全清（2026-07-30 挂 · **2026-07-31 最后 1 条定位并修复，本条可销账，待您勾**）**：`build-backlinks.py` 实测悬空 **25 条**，现 **0 条**。
  **✅ 最后 1 条已解（2026-07-31）**：`渊图/logs/2026-07-10-渊图-帕米尔10篇入库.md` → `[[航天·太空光伏隔离区]]`。**既不是没落盘、也不是改名**——实体一直在 `Database/行业研究/raw/航天·太空光伏·太空算力/`（目录 + README.md，立区 2026-06-25）。**是引用时把目录名和「隔离区」三字揉成了一个从未存在过的文件名**（真名结尾是「太空算力」）。铁证：`Database/行业研究/raw/核聚变/README.md` L10「故沿用 2026-06-25『**航天·太空光伏·太空算力**』隔离区范式：只攒、不入」。**修法采乙（Doctor 2026-07-31 批）**：别名语法 `[[Database/行业研究/raw/航天·太空光伏·太空算力/README|航天·太空光伏隔离区]]`——目标补对、显示名一字不动，同 07-30 处理「兑现回测」两处的手法。该目标在 vault 外，属跨库，下次跑 `build-backlinks.py` 应落进 `crossref.txt` 而非 `dangling.txt`（**待下次实跑验证**）。
  **已做（内容侧·均为真 bug）**：经验库 4 处裸 `[[EXP-…]]` → `[[经验库#EXP-…]]`（同文件内已有 3 处正确写法，是两种写法混用，裸写点了跳不过去）· `[[渊图系统概览]]` → `[[渊图/architecture/系统概览]]`（裸 stem「系统概览」全库多项目重名，必须路径式）· `[[兑现跟踪暗态点亮Phase1_PRD]]` 补日期前缀 · `[[兑现回测_去门槛_20260629]]` ×2 改用别名语法 `[[2026-06-29_兑现_去门槛|原措辞]]`（目标补对、显示名不动）· **补建 `GlobalPercent/GlobalPercent.md` 项目 stub**（3 处 `[[GlobalPercent]]` 悬空的根因是漏建 stub，渊图/PEC/DVA 都有）· 顺带补 `风险日报/风险日报.md`。
  **已做（工具侧）**：`build-backlinks.py` 加**三分法**——`markers.txt`（编号标记，`MARKER_RE` 匹配 `GE-\d`/`CS-\d`/`G-X\d`/`A\d\d`/`GOTCHAS ` 等，本就无文件）· `crossref.txt`（vault 外但真实存在，非错误）· `dangling.txt` 只留真悬空。**刻意不把 `EXP-`/`ERR-` 列进标记白名单**——它们有正确写法，裸写是 bug，进白名单等于把真 bug 藏起来。现输出：真悬空 1 · 跨库 14 · 标记 2。
  **⚠ 勘误（2026-07-30 · 本条原文已重写）**：原条目写「全库解析失败 **464 处**、两套 `[[ ]]` 语义各占 94%、`build-backlinks --orphans` 的悬空数字因此哑掉」——**这三句都不准**。464 是 CC 用**自己临时写的脚本**算出来的，而那脚本**没有既有工具 L117-119 的 `logs/`+`chats/` 过滤**（历史定格内容不算活跃悬空），那两个目录正是 464 的绝大部分。CC **从没跑过 `build-backlinks.py` 就断言它哑了**——实跑只报 26 条，信噪比一直是好的。**错在用自制口径的数去推断既有工具的行为**（G-X79：负向结论要跨源核实再断言）。方向也随之修正：原定「只改工具不改内容」，实际内容侧那 6 处是真 bug、修了才有收益，当初担心的「批量改 464 处历史正文」的风险根本不存在。
  **⚠ 顺带发现（未处理）**：`风险日报/architecture/系统概览.md` **不存在**，而 `brain-save` Step 4 规定「同步项目状态 → 更新该文件的最后活跃字段」——这一步对风险日报一直是空转。补写需梳理项目全貌，留您定何时补。
  **✅ 追记（2026-08-02 /consolidate 实跑验证）**：「应落 crossref 待验证」一项已验——该链在沙箱跑会被误判真悬空，系 `build-backlinks.py` 两处分类缺陷（logs 豁免只认顶层段 + 路径式跨库配不上 stem 索引），当日已修（logs 任意段豁免 + `Database/`/`AI4ME/` 前缀归跨库），复跑真悬空 0。（**Doctor 2026-08-02 口头勾定，CC 代记留痕并迁档**）

- [x] **DVA ASR 云→本地迁移 → 已扩展为完全 fuxi 化并于当日完成单写切换**（2026-07-24 挂 · **2026-07-31 由 Doctor 会话中口头确认「勾了」，CC 代记留痕并迁档**）：Qwen3-ASR 本地后端+runtime+数据+调度全迁 fuxi，Phase 0→5 收官（终版包 135000Z·offsite 回填 1388·DVA-Refill Ready）。剩余尾巴已拆入新待办：07-25 首班核验 / Phase 6 观察期 / Phase 7 清理另批。详见 logs/2026-07-24-DVA-fuxi化Phase2至5单写切换完成。原条目内文（次序①-⑤）全部兑现。
  fuxi 有本地算力 → 甩掉云管线（DashScope key + 火山 TOS + OSS 白名单坑 + 计费 + 网络脆弱）。**选型＝`Qwen/Qwen3-ASR-1.7B-hf`**（阿里 Qwen 开源·Apache-2.0·2026-01-29 开源/06-26 原生 Transformers·中文新一代 SOTA·22 方言·原生带 BGM 音频·可选词级时间戳·Open ASR 榜 WER 5.59）——**2026-07-24 Doctor 指正选型**：初稿推 SenseVoiceSmall，Qwen3-ASR 更强且同为阿里开源本地，改选它（SenseVoiceSmall 退备选）。方案 `Projects/DVA/docs/ASR本地化迁移方案_20260724.md`。
  **次序（先部署后写码后验收·同 F4 纪律）**：① fuxi 装 `git+transformers`+torch、下载 `Qwen/Qwen3-ASR-1.7B-hf`、最小验证（Doctor/VV 终端·沙箱做不了下载）；② 真实抖音音频（有语音的）本地 Qwen3 vs 云抽样对比；③ CC 改 dva_asr 加 `--backend local`（`AutoModelForMultimodalLM`+`apply_transcription_request`·云默认不动·本地 opt-in·出 diff 待批·装好模型才可测）；④ 首批本地跑验收 → 全面切本地（云留兜底）；⑤ 更新 VV 请求为 Qwen3 本地口径（已改前瞻 1b）。

> 下面 6 条为 2026-07-21 文件系统健康自检产出（Doctor 批「全部挂 TODO」）。清理执行明细见 `~/Documents/_to_delete_20260721/_MANIFEST.md`（观察期至 2026-08-20）。

- [x] **警示页 styleguide §06 免责条款回灌 → 核实已闭环、条目过期销账（2026-07-30 结案）**（2026-07-27 挂·提案制）
  **2026-07-30 核实**：文件现状与本条诉求已完全一致——§06 正文写「**形态（v1.2 回灌·2026-07-28）：一句并入页首综合读数标签行即可，独立横幅可选**（活范例 risk-daily 自 2026-07-27 起为缩并形态·Doctor 批『缩并不删』；定性不可省，形式可缩）」，长版横幅降级为标注「（可选）」的示例块（原文保留·可逆）；§07 反对条只写「页首挂 nowcast 免责」，不指定形态、与缩并不冲突。**应是 07-30 做 v1.3 时顺手带过去而未销账**——零新增改动，Doctor 批「勾掉销账」。
  原文：活范例 risk-daily 的 nowcast 免责已「缩一句并入综合读数标签行」（Doctor 批），styleguide §06 仍写「页首必挂**横幅**」+长版示例、§07 禁区条同——范式与 canonical 活范例不一致。文件：`Projects/O MY HTML/design-system/warm-warningpage-styleguide.html`。

- [x] **警示页 styleguide v1.4 §12「因子归因图表选型」落地（2026-07-30 Doctor 确认后当场完成）**
  **判据**：雷达适合同质轮廓，**带正负的归因用零轴**（07-29 FOMC×伊朗五因子分解五轮迭代产出）。**主图＝函数式归因曲线**（横轴事件时间·水平零轴·因子累计贡献 f(t) 分段线性＋残差 ≡ 实际走势，**恒等式在图上闭合**·实抽残差 ≤0.18pp，读者不查代码即可验账）；**配图分工**＝零轴柱(静态权重对账)／象限(结清度视角)／雷达(**弃用存档·留作选型反例·不删**)／分时图(素材层)；**视觉语法三分**＝色域填充(结构性持续因子)／实线(事件性)／虚线(不确定性·残差)——线型只说「哪一类」，强弱交给数值与位置；**章节序铁律**＝归因页首节即主图，写进定时班 prompt 不得改序。
  **落盘**：`warm-warningpage-styleguide.html` v1.3→**v1.4**（备份 `.bak_20260730_v13`）——新增 §12、头注版本、两处「十一件事」→「十二件事」并补 ⑫、§07 反对条 +2（雷达画带正负归因／象限雷达当主图令恒等式无处闭合）、footer 设计依据补 case study 路径；`README.md` 注册表行同步 v1.4。**零改旧章**（追加语法，同 v1.3 纪律）。自检过：13 section 全闭合、「十一件事」残留 0、v1.3 仅存历史沿革与旧章标注。
  **注记**：上场那份逐文件清单只活在对话里、未落盘（`logs/2026-07-30-事件归因值守系统上线.md:38` 仅记「清单已出」）→ 本次按 case study + 会话日志重建后经 Doctor 二次确认才动手。（2026-07-30 Doctor 裁：不升 G-X。）

- [x] **PEC · 关系化图谱可行性 → 落地（复用渊图图基建 + PEC 专属图 schema）（2026-07-25 挂 · ⏳ 等下周一 2026-07-27 Fable 5 额度恢复后再做）**：承 2026-07-25 会话「渊图关系化图谱能否在 PEC 整体实现」判定——**整体照搬渊图那套静态实体-关系图＝不行**（PEC 内核层：dated 裁定链 / 概率·双读 / α-α′ 二阶反身 / 机理论证，正是渊图刻意 strip 的高时效＋它没有的二阶关系，硬图化会失真）；**可行且值得＝复用渊图图基建（schema 化 kg_ingest / 结构 QA / wiki_autogen / provenance / 命名铁律）＋ 给 PEC 另配 schema**（node type：框架 / 预测 / 案例 / GOTCHA / 实体；edge type：挂框架 / 同族 / 精化 / 证伪-命中 / 校正 / α 审计；每断言带 `as_of` + `confidence`）——**共享工具链、不共享图模型/本体论**。**下一步（走 propose-then-confirm）**：① 出「PEC 可图化层 vs 不可图化层」映射表；② 草拟 PEC 专属图 schema 草案。**为何等 Fable 5**：任务重、跨渊图 × PEC 两库，留下周一额度恢复后做。关联：raw `Projects/PEC/raw/2026-07-25_analysis_江学勤预测性历史框架…`（同日会话上游）· 渊图系统概览（图模型/11 边 schema/基建）。
  **✅ 2026-07-31 Doctor 裁定销账 —— 两项「下一步」均已交付（2026-07-28 完成，做完未销账）**：
  ① **可图化层 vs 不可图化层映射表**（15 层逐层判定）· ② **PEC 专属图 schema v0.1**（12 节点类型，含新立的 `case`/`prediction`/`verdict`/`clause`；11 边类型）——`verdict` 设为一等公民节点以承载「严读/宽读」双裁定，正是照搬渊图会失真的那部分。
  **另加做了原方案没写的第三步**：拿 **IR 预测组**做样本试跑（`build_ir_sample.py` → **57 节点 / 92 边**，结构 QA **12 项全绿**），并在过程中新发现第 5 项 QA「双读一致性」。
  **结论（与 07-25 原判定有出入，已在文档 §三 记明）**：可行**已证**、值得**未证** → 推荐 **lint-first**（先用图基建做一致性检查，暂不建全量图）。
  **产出**：`Projects/PEC/图谱化方案_v0.1_20260727.md`（21252 B · 文件名沿用 07-27，实际成文 07-28）· `Projects/PEC/build_ir_sample.py`。
  **⚠ 本条曾挂「⏳ 等 2026-07-27 Fable 5 额度恢复后再做」**——那天早已过、事也办了，属**做完未销账**；同期另有一处「引用自家编号」勘误（原写 G-11，实为 G-27 子条款）已在文档 §四 核验留痕中更正。

- [x] **brain-save skill Step 5 改「先探后加」（2026-07-24 完成·Doctor 已安装 v2.9）**（2026-07-23 挂）
  Step 5 旧默认 `git add -A` 会在工作树积压时混入范围不明改动（G-X83 / DVA GIT-20260723-001）。**已改**：brain-save v2.9 四处 commit 模板（Step5 step2/3/4 + Step6 回报）全改「先探后加」（`git status --short` → `git add <明确文件>` → `git diff --cached --check` → commit → push），禁 `git add -A`。CC 出 `.skill` 包（源 `Claude/brain-save/`）→ Doctor 经 Settings/Save skill 安装生效。
  **留档小事**：`Claude/Brain/.skills/brain-save/` v2.7 旧漂移副本（07-22 记过 .skills 漂移·G-X90）——**2026-07-24 已冷区归档** → `_DEPRECATED_brain-save_v2.7_20260724`（dir + .skill 包·可逆）。真源 `Claude/brain-save/` v2.9。

- [x] **E1 · DVA 空转写重跑 ASR（2026-07-24 VV 执行完成·13 条确证真静音）**（2026-07-21 挂 · 自检产出 · 中优先）
  **2026-07-24 结案**：VV 经握手层执行——13/13 从 fuxi 取回（SHA-256 逐条一致）→ 重提交 sensevoice-v1 → **全部 `EmptyOutput`（无可识别语音）**，现各带 `asr_status:"empty"` 的 `.transcript.json`，从「无定性 0 字节假完成」变「已确证真静音」。真相：这批是 SansanYe AI 画面/音乐视频 + 老石 122s「沉浸式开箱」ASMR，本就无解说，非丢失转写。dva_asr 幂等已凭 .json 定性不再重跑。回传 `4AI/Shake hands/to CC/VV回传-E1空转写取回重ASR-20260724.md`。VV 未碰 DB/canonical/正本（守握手层）。
  **孤儿（第14条）已闭环**：`764710303268505`（15 位）＝**文件名截断**丢 id 的真视频 `7647103032685055247`（SansanYe《CHRONOS HUNTER》4.34s 新片预告·DYD 80 字截断坑活实例·[[DVA/GOTCHAS]] RISK-20260721-001）。2026-07-24 VV 经 addendum 取回（SHA 一致 838443B）+ 重 ASR（全 id）→ **也 `EmptyOutput`·已定性**，新转写用全 id 命名。回传 `to CC/VV回传-E1第14条-20260724.md`。**14/14 全确证真静音，E1 彻底结案。**
  **主场清理（Doctor·沙箱禁删）**：旧截断一对待删——`rm ~/Documents/Database/Douyin/Transcripts/SansanYe/*__764710303268505.transcript.*`（0B txt + 79B json·已被全 id 版取代）。
  反向对账「有转写无视频」（投知/卷宇宙）另账未动。
  SansanYe×9/老石×2/AI个体指南×1 等 0 字节转写＝假完成标记。
  **2026-07-24 核实**：实为 **14 个 0 字节转写**（SansanYe×11 / 老石谈芯×2 / AI个体指南×1）。其中 **13 个 offsite=1**（删源已删本地 mp4·元数据 json 留·**已避开路径假阳性坑**核实：file_path 存的是视频文件夹非 mp4，误判「在」）→ **须先 fuxi 取回再 ASR**；另 1 个 `764710303268505`（短 id）＝DB 孤儿、不在 aweme 表，单独查。**取回清单**：`outputs/E1_取回清单_20260724.tsv`（aweme_id/作者/offsite_uri/本地目标）。
  **好消息**：`dva_asr.py` 的 E1 核心坑**已修**（284-294/410 行·内容感知幂等：0 字节判未完成自动重转，无需手删）。**无批量取回脚本**（recovery_drill 只 verify）。
  **Doctor 终端序列**：① 按清单 scp 从 fuxi 取回 13 mp4 → 各自 file_path 文件夹；② `dva_asr.py --author-dir Downloaded/{作者}/post/ --sec-uid …`（SansanYe/老石/AI个体三个作者，幂等自动重转 0 字节）；③ 孤儿 764710303268505 单独处理（删空转写或重映射）。反向对账「有转写无视频」（投知/卷宇宙）另账。

- [x] **E2 · $CODEX_HOME 字面目录根因修复 + 归位（2026-07-24 闭环·仅剩正本合并 Mac 一行）**（2026-07-21 挂 · 低优先）
  **2026-07-24 VV+CC 协作闭环**：VV(Codex侧) 确认——① automation `dva-16469639bf3b` 已 ACTIVE→**PAUSED**；② 真实 CODEX_HOME=`/Users/lunarabbit/.codex`，正本 memory=`.codex/automations/dva-16469639bf3b/memory.md`；③ **根因加固**：automation 上下文注入未展开 `$CODEX_HOME/...`，2026-07-11 执行代理当字面相对路径写到 `Documents/$CODEX_HOME/` → prompt 已加**绝对路径锁**（只读写 .codex 正本·禁字面 $CODEX_HOME·禁相对 cwd 解析）。两份不重复：字面=7/11 记录、正本已有 7/18/7/22 → **合并非覆盖**。
  **CC 主场**：字面目录移 `Documents/_隔离_20260724/CODEX_HOME字面bug/`（可逆·根已无）。**2026-07-24 Doctor 已跑正本合并**（7/11 条目 append 进 .codex 正本）→ **E2 彻底结案**（automation PAUSED + 根因加固 + 字面目录隔离 + 正本合并齐）。
  Documents 根 `$CODEX_HOME/`＝变量未展开 bug，内含 automation「DVA 定期补库」memory.md（有价值）。顺序：Codex App 侧确认 automation dva-16469639bf3b 已停用 → memory.md 并回真实 CODEX_HOME → bug 目录进隔离区 → 修 automations 里未展开的变量引用。确认前不动（否则目录再生）。
  **2026-07-24 CC 核实**：`$CODEX_HOME/` 内容＝`.DS_Store` + `automations/dva-16469639bf3b/memory.md`（仅此一文件有值）。真实 CODEX_HOME 沙箱内 `~/.codex` 未命中（在 Doctor Mac 侧·CC 定不了）。**memory.md 6 行内容存档防丢**：
  > `# DVA 定期补库 memory` · 2026-07-11 按要求仅执行一次 `Database/Douyin/DVA-ops/run_refill_watchlist.sh`；latest.json：status=success/exit_code=0/authors_ok=8/8/warning_count=0；摘要 `DVA-ops/summaries/refill-watchlist-20260711-112202-3308.md`；耗时~30s；期间一次 `/bin/ps: Operation not permitted` 告警但状态未受影响。
  **待 Doctor（Codex App 侧·CC 做不了）**：① 确认 automation `dva-16469639bf3b` 已停用（否则目录再生）；② 告知真实 CODEX_HOME 路径。之后 CC 可给 mv 命令：memory.md 并回真实 CODEX_HOME → `$CODEX_HOME/` 整目录移 `_to_delete/隔离区` → 修 automations 里未展开的 `$CODEX_HOME` 变量引用（根治再生）。**沙箱不动**（删/移挂载盘受限 + 停用未确认前动了会再生）。

- [x] **E4 · 备份策略统一 gz + 轮换（分级 B 代码 + 分级 C backlog gz 均完成·2026-07-24）**（2026-07-21 挂）
  Market-Data gz 快照已示范（~75MB/份，较裸 .bak 省 3.2 倍）；拟裸 .bak 复制流全面转 gz；recap predaily/preingest 双钩子同日去重；`bak_fxdeprecate_20260717`（253MB）等观察期锚随新策略自然轮换出局。
  **2026-07-23 进展（分级 B）**：recap predaily 已按日键 cp（同日自动覆盖），跨日清理**沙箱禁删** → 给 Doctor Mac 清理命令（保最近 N 份），不塞沙箱 SKILL。
  **2026-07-24 分级 C 复核（Doctor 批做 C）· CC 反建议缩范围**：清点后大户＝**两个 ~240MB market_data .bak**（`bak_fxdeprecate_20260717` 旧观察锚 + `bak_preF4backfill_20260723` F4 回补锚·已验证）＝空间 99% 在这俩；recap .bak 仅 ~4MB×7、已被 B 的轮换管着。故「裸 .bak **全面转 gz** 的代码改造」**边际极低**（无高频裸 .bak 钩子·snapshot_market_db.py 早已 gz），reader/回滚复杂度不值当。**CC 建议只做 backlog 压缩、不改代码**：`gzip` 那两个 240MB 锚（Mac·gzip 删原文件沙箱做不了）→ 省 ~320MB。preF4backfill 锚 F4 已验证可考虑直接删（可逆起见先 gz 留着）。
  **2026-07-24 完成**：两个裸 .bak 已压 gz——`bak_fxdeprecate_20260717.gz` 73MB(原241) + `bak_preF4backfill_20260723.gz` 74MB(原245)，**486MB→147MB·省 ~339MB**。分级 C 的「全面转 gz 代码改造」按 CC 反建议不做（边际低）。E4 整条结案。

- [x] **brain 注册项目缺 `GOTCHAS.md` 补齐（2026-07-24 完成·REQ-F2 达成）**（2026-07-19 挂 · 低优先）
  烛照九阴是撞见才发现没有的，REQ-F2 当年标了 `[x]`「所有 brain 注册项目补齐 GOTCHAS」，说明当时可能只漏了它、也可能不止。
  `for d in ~/Documents/Claude/brain/*/; do [ -f "$d/GOTCHAS.md" ] || echo "缺: $d"; done`
  **2026-07-23 扫描结果**：真项目里缺 brain 侧 `GOTCHAS.md` 的有 **4 个：MiroFish / 剑酒青丘 / 星空 / 称象**。
  **2026-07-24 补建（Doctor 批）**：4 个 GOTCHAS.md 全建好。剑酒青丘 填真实 [BUG-20260723-001]（`_mnt` 平铺挂载坑·code 侧归位·交叉引 [[通用教训]] G-X88 + 烛照九阴 GOTCHA-20260723-001）；MiroFish/星空/称象 为骨架（frontmatter+术语+待追加）。REQ-F2「所有 brain 注册项目补齐 GOTCHAS」达成。

- [x] **定时 run 级别读数占位 → 根因已定位并修（2026-07-23 结案·待下班验证）**（2026-07-21 挂 · 时间敏感）
  **定论：定时链路确复发**——07-23 10:11 定时班日报仍占位「级别读数不可用」（非一次性瞬态）。根因＝跨项目 `剑酒青丘/adjustment_grade.py` 的 `_mnt()` 硬走 `../×6`，沙箱平铺挂载下溢出到 `/` → `grade_section` 两分支皆败降级；app.log 无痕系 stderr 落定时会话而非 app.log。**已修**（Doctor 批准·自愈式+env 兵底）：`_find_root()` 改探测「含 Database 子目录的祖先」作根，Mac 正路零改动、平铺沙箱落 `/mnt`；三布局隔离测试 + 真脚本 `--json`(L3·confirm True) 均过。详见 [[烛照九阴/GOTCHAS]] GOTCHA-20260723-001。
  **留验证**：下一工作日（07-24）10:00 定时班后，确认日报「回调级别读数」栏出真读数（非占位）即彻底结案；仍占位则回看 `剑酒青丘` 那班是否实际挂载/env。

- [x] **E3 · artifact 保存钩子节流**（2026-07-21 挂 · **2026-07-23 完成·分级 B**）
  `gen_daily_report.py` 每次保存落 2.1MB 全量 index.bak 无轮换（曾单日 42 份）+ 日报 `.pre-*` 同源双倍。**已改**（deletion-free·挂载盘禁删适配）：新增 `_rotate_backups()`（跨日保 5 天·`unlink` 包 try/except，Mac 清·沙箱静默跳）；index.bak 钩子改**日键命名**（同日覆盖去重·42/日→1/日）；`.pre-*` 钩子 `move`→`copy2`+路由 `archived/_pre-snapshots/`+日键+轮换。修一 bug：轮换日键取**末组** 8 位（`.pre-` 快照日，非数据日）。py_compile + 两命名隔离测均过。
  现存积压清理（23M index.bak+13M .pre-*）另走·可逆。

- [x] **E7 · 转写覆盖率测量陷阱记 DVA GOTCHAS**（2026-07-21 挂 · 低优先 · **2026-07-23 完成**）
  长标题文件名截断丢 aweme_id → ID-join 覆盖率 49% 假象，稳健口径实测 ≈97%+。已落 `Projects/DVA/GOTCHAS.md` [RISK-20260721-001]（含稳健口径「按非零 .transcript.* 存在性计数」+ 反向对账正交提示）。

- [x] **五因风险温度：挖新因子 + 改计温 function**（2026-07-19 挂 · **Doctor 裁定** · 高优先 · **2026-07-23 回填结案**）

  **回填 2026-07-23**（Doctor 批「整条 [x] + 留尾巴」）：两条工作线 + 两个悬案均已落地，本轮核实归档，整条结案。
  - **① 挖新因子 ✅** — 2026-07-19 遗漏风险因子回测（`AI4ME/CC-遗漏风险因子回测-成交额与浮盈-20260719.md`），机理起点筛出两条，入 `config/risk_factors.json` 环境层（禁作看空计温、只作共振证据）：**a6 量能脆弱态**（创业板成交额 p99·双尾放大器·53 事件 lift 2.06·Fisher p=0.008）、**b6 浮盈集中度**（top5% 成交额占比 p95·24 事件 lift 2.20·**唯一过 20 事件门槛**）。
  - **② 改计温 function ✅** — commit `408d765`「S2 计温 function 两层重构：触发×环境+A6/B6 环境层+risk_function 单一真源（PRD 2026-07-19）」。旧「数因子个数→三态」换成 **触发层(F4/F5) × 环境层(F1/A6/B6)**，S2 口径自 20260720 生效。
  - **③ 悬案·温度带呈现 ✅** — 采「维持并标注证据基础」：k/n 显示（触发无共振 0/23·共振 3/21）+「样本薄·预注册中」注记（commit `b56f3eb`）。
  - **④ 悬案·过期标签 ✅** — 3.2/4.4/9.7% 三腿旧口径已从渲染文案清除，只剩两处 `#` 注释作机理说明。
  - **七问**：`docs/五因回测校准_20260721.md` 自带逐问对照表，07-22 会话已过验收（见 [[2026-07-22-五因regen验收与resume开声固化]]）。
  - **尾巴**（转下方新条）：触发层 F4(4事件)/F5(9事件) 仍 sub-threshold——新因子是在**环境层**加固共振，未在触发层根治「仅 F4 有意义」的病根。

  <details><summary>原始分析块（2026-07-19 挂时·可逆保留）</summary>

  **裁定原话**：「仅 F4 有意义，但意义不大，需要进一步挖掘因子，修改 function。」

  **当前成色**（事件级重估后，全部经修正口径）：

  | 因子 | 独立事件 | lift | fwd3(触发 vs 未触发) | 状态 |
  |---|---|---|---|---|
  | F1 隔夜外盘 | 54 | 1.15 | +0.16% vs +0.56% | 样本够 · **确证无效** |
  | F2 拥挤度 | 6 | 0.00 | — | 样本不足 |
  | F3 杠杆水位 | 9 | 0.87 | +1.24% vs +0.38% | **已结案：两方向皆追认** |
  | **F4 IPO虹吸** | **3** | 1.68 | −0.22% vs +0.45% | **唯一有意义，但薄** |
  | F5 外部紧缩 | 9 | 2.31 | +0.01% vs +0.42% | 样本不足 · 方向平 |

  计温层（F4+F5）全部证据基础 = **12 个独立事件**。五因无一达 20 事件门槛。

  **两条工作线**：

  1. **挖新因子** —— 现有五因中唯一没被推翻的是**机理判断**（F4 发行日程提前公告、信息未被收盘价吸收；F5 油价地缘外生持续；F1 开盘即定价；F3 T+1 追认）。**新因子的筛选起点应是机理而非统计**：先问「这条信息在收盘价里被吸收了吗」，再回测。凡答"已吸收/滞后"的直接不入选，省掉一轮回测。
  2. **改计温 function** —— 现行 function ＝「触发因子数 → 三态」（0→🟢 / ≥1→🟠 / 叠加F1→🔴）。若最终只剩 F4 一个有效因子，这个"数因子个数"的结构就没有意义了。**接手时先定义清楚 function 改造的范围**（是换分档逻辑、换权重、还是整体重构），Doctor 原话较简，需对齐。

  **硬约束**：新因子与新 function 一律须过 [[剑酒青丘/frameworks/回测设计七问]]，报告须让读者不查代码即可回答七问。尤其第 6 问（控制同期行情后的增量）——F3 就是栽在这一问上。

  **仍悬而未决**：温度带的**呈现形态**（下架 / 降级为因子状态列表 / 维持并标注证据基础 / 收缩到 F4 单因子）——Doctor 未选，选择是"先把东西做好"而非"先改怎么展示"。另注：三态旁标注的 3.2%/4.4%/9.7% 是**三腿口径的历史标定，已过期**（分档逻辑按触发数、不受影响，但标签失效）；F5 触发从 76 日缩到 12 日后 🟠 出现频率会明显下降，此变化尚无人标注。

  **相关**：纪要 v1.4 §五-C · [[通用教训]] G-X75/G-X76 · [[烛照九阴/GOTCHAS]] ERR-20260719-002

  </details>

- [x] **驾驶舱接回调级别读数（2026-07-23 核实：已上线·待 Doctor 终验 PRD[✓]）**（2026-07-19 挂 · Doctor 已批 PRD §二）
  PRD：`logs/checkpoints/2026-07-19_驾驶舱接回调级别读数_PRD.md`（17 条交付标准）。全局横幅·纯展示·常驻·复用暖色温度卡范式·落 `#tab-cockpit` 控制栏与 `#ck-pills` 之间。
  **2026-07-23 核实纠错**：本条 07-19 挂时写「代码一行未动·从零」，但 **07-21 数据层(cockpit_data.py 加 build_market_grade+payload market_grade 键)+展示层(artifact 横幅) 已落地、07-22 已部署上线**。本会话端到端复验全过：A1–A4（live `get_cockpit_payload` 返回 market_grade=L3/nn/hist/asof=20260722）· B1–B4（market_grade 在五函数体 0 命中·clocks 未变）· C1–C4（现网 artifact 横幅要件齐·DOM 内 0 禁词）· D1（py_compile OK）· E2（payload 应答+横幅在现网 HTML＝07-21 白名单阻塞已解、已部署）。今日 `adjustment_grade._mnt` 修复同惠及此数据源。
  **余项（Doctor）**：① 桌面肉眼终验横幅渲染（E2 [~]·CC 无法代观察）；② PRD 17 条 `[?]`→`[✓]` 由 Doctor 落。**清理候选**：`Database/龙鱼-标的分析库/_artifact_pending_longyu-holdings-board.html`（07-21 待推件）已被 07-22 现网版超越、成陈旧，建议移 archived（可逆·不删）。

- [x] **F4 阈值可达性预检**（2026-07-19 挂 · 低优先 · 回补前必做 · **2026-07-23 完成**）
  `200亿` 是绝对阈值。回补 2010+ 之前须先验历史滚动窗募资能否达量级——达不到则回补只增"未触发"、事件数不变，等于白干。
  **2026-07-23 预检结论**（ipo_daily 现覆盖 2024-01→2026-07·236 行·滚动 10 日历日现行口径）：
  ① 连当前注册制 era 都勉强触发——≥200亿 仅 5 触发日/236(2.1%)、~2 独立事件，几乎全靠单只巨型 IPO（长鑫 666亿@20260716 顶到 689亿峰值；次大 246亿）。**F4 薄样本是结构性、非数据缺口**。
  ② 历史可达性锁「发行制度」非「行情」（G-X75）：2012–2018 两次暂停(2012.11–2013.12/2015.7–2015.11)+小盘限价 era 基本到不了 200亿→回补白干；2010–2011(巨型银行 IPO)+2019 后(科创板/注册制大盘)能达但只在巨型簇集。
  ③ 绝对 200亿 跨 era 不可比：同 200亿 抽 2010 的~20万亿池 vs 2026 的~90万亿+ 池，相对冲击天差地别→固定阈值污染跨 era lift。
  **裁断**：绝对 200亿 回补＝白干+造不可比事件。要有意义**必须先把绝对阈值换相对值**再回补；即便如此 F4 仍会薄。**2026-07-23 Doctor 定：换相对阈值·出方案**（见下条）。

- [x] **F4 绝对阈值 → 相对阈值（选型 B·募资/成交额比）· 2026-07-23 落地**（Doctor 批「换相对阈值·选型 B·p95」）
  **已完成**：回补到位（ipo 2020-02+·成交额 2010+）→ 校准 p95(N10/M30/th0.045) → 改码四文件 + 单源 helper：`risk_function.py` 加 `f4_ratio_trigger()`（两端共用·G-X73）；`risk_factors.json` f4 换相对键(旧绝对降级 _deprecated·可回滚)；`calibrate_risk_factors.py`（load 成交额+F4块相对+扫描网格 ratio_th）；`gen_daily_report.py`（生产计算+展示相对口径）。三 py py_compile 过；calibrate 真跑权威＝可评1567/触发78/**14事件/lift2.63**/P(冰|触)10.3%（CC 独立复现曾得2.68·冰点标签口径微差·事件数一致·以真跑为准）。七问报告 `docs/五因回测校准_F4相对_20260723.md`（Q6 过：低成交额alone lift0·非伪代理；分子主导；跨4年散布）。regime：当前高流动性下长鑫666亿 ratio0.026<阈→F4 休眠(正解)。**余（Doctor 终端）**：`calibrate_risk_factors.py` 真跑重生成七问报告表 + `gen_daily_report.py` regen 让日报 F4 显新口径；git。仍 14<20＝方向真·样本不足档。
  <details><summary>原「等回补」计划（已完成·留档）</summary>
  **选型 B**：rolling-N 日募资 ÷ 近 M 日日均全市场成交额 ≥ 阈值 →「IPO 抽走≈几天成交额」。机理最直接（虹吸=抽流动性），2025+ 验证成立：高流动性 era（日均~2万亿）巨型 IPO 也只抽~2-3% 一天成交额，正解释 F4 现弱；低流动性 era 同额 ratio 更高=虹吸更咬。
  **数据纠错**：`daily_market.volume_trillion` 历史全 0/坏（ERR-20260719-003·勿用）；可用成交额 `market_amount_daily` 仅 2025+。故分子(ipo_daily 2024+)与分母(成交额 2025+)**都需回补**。
  **前置·Doctor 终端（tushare 下载·不在沙箱跑）**：`fetch_ipo.py --from 20100101` + `fetch_market_amount.py --from 20100101`（回补前先 `cp market_data.db → .bak_preF4backfill_{日}`）。
  **回补到位后·CC**：算相对口径校准（M/N/阈值网格）+ 出逐文件 diff。
  </details>

- [x] **重跑 F5 校准取两腿新 lift**（2026-07-19 完成）
  F5 两腿：lift **2.31** / 12 触发日 / **9 独立事件**。同日连修校准工具三处（F4 可评日缺数当未触发、扫描表 lift 基准不同源、判定改卡独立事件数）。

- [x] **F5 油价腿历史回补**（2026-07-19 完成 · 同日）
  Doctor 终端 yfinance 回补 BZ=F 4150 行 [20091201→20260717]，CC 真隔夜回测 3914 可评日。**三裁定**：5% 档**平反**（45 事件 lift 2.03，非过拟合，lift 沿网格单调）；3% 档**弱信号定论**（155 事件 lift 1.29，预期的"转正"未发生）；**跨区制首例**（四段 lift 全 >2：2.12/2.83/2.02/2.42）。纪要升 v1.6。报告：`AI4ME/F5油价腿回补/CC-F5油价腿长样本回测-20260719.md`。

- [x] **【G-X13 根治 C】全局偏好 Settings 镜像块合并进桌面端个人偏好**（2026-07-07 · 敬语「您」块已每轮注入生效）

- [x] **【G-X13 补丁 D】`brain-resume` 加 Step 0 读全局偏好镜像**（2026-07-07 · 新 skill 已覆盖安装）

- [x] **【brain-anchors】补召回词「暗色·卡片页 / dark card page / 龙鱼看板」**（2026-07-07）

- [x] Brain vault 目录结构初始化（2026-05-14）

- [x] graphify v0.7.16 安装（2026-05-14）

- [x] 知识种子：7 个项目 architecture 文件（2026-05-14）

- [x] 通用教训提炼（2026-05-14）

---

- [x] **给渊图跑 graphify**（832 nodes, $9.62）
  `cd ~/Documents/Database/行业研究 && graphify . --obsidian --obsidian-dir ~/Documents/Claude/brain/graphify/渊图`
  （需先确认 graphify 在 PATH：`export PATH="$PATH:~/.local/bin"`）

- [x] **给 DVA 跑 graphify**（1070 nodes, $0.85）
  `cd ~/Documents/Claude/Projects/DVA && graphify . --obsidian --obsidian-dir ~/Documents/Claude/brain/graphify/DVA`

- [x] **PEC G-06 至 G-14 认识论陷阱全量入 brain**（frameworks/陷阱-G-06-G-14.md，9 条全量）
  读取 `Projects/PEC/GOTCHAS.md` 后半部分，提炼入 `brain/PEC/frameworks/认识论框架.md`

## 已取消

> 取消 ≠ 完成。单列，免得混进完成清单虚增战果。

- [x] **EAL · v2.3 五项方法 gate（2026-08-19 随 v2.3 功成退役取消迁档）**：A 阶段成果与治理纪律由 v3 承接；慢牛漂移溯源不再追踪；B 阶段方案已 cancelled。

- [x] **EAL · gate 验收脚本 PRD（2026-08-19 随 v2.3 退役取消迁档）**：对象（v2.3 五项 gate 验收）随退役消失；若 v3 后续需 gate 判据机器化另立新案。

- [x] ~~F3 tushare 历史回补~~ —— **2026-07-19 取消**（Doctor 批）。正反两方向皆为追认，控制行情后零增量，回补只是把追认结论说得更响。见纪要 §五-C。

---

## Brain Vault 对接需求（2026-05-14 立 · 已全部达成）

> 原始需求文档：`brain/references/brain-对接需求-20260514.md`

> 完整需求文档：`brain/references/brain-对接需求-20260514.md`

### P0（不做则 brain 不能跑）

- [x] **REQ-A1** `/resume` 命令实装 — 读最近 3 个 log，输出摘要+建议

- [x] **REQ-A2** `/save` 命令实装 — 填模板写 logs/YYYY-MM-DD-主题.md

- [x] **REQ-C4 / REQ-E1** Projects ↔ brain 关联 + 项目骨架生成器 `register-project.sh`

- [x] **REQ-F1** 锚点触发机制（dva / 龙鱼五力 / 自检 / 天工开物 → 自动加载）

- [x] **REQ-G1** brain/ 纳入 git 版本管理（commit c65bf5e → github.com/fuxi4ai/C.C.）

### P1（关键体验）

- [x] **REQ-A3** `/note [主题]` 命令实装 — inbox/ 新建 + 采集态

- [x] **REQ-B1** frontmatter 验证脚本（`brain/.tools/validate-frontmatter.py`）

- [x] **REQ-B2** wikilink 回链索引（`brain/.index/backlinks.json`）

- [x] **REQ-B4** 全文/标签搜索（`brain/.tools/search.sh`）

- [x] **REQ-C1** Claude Code 对话导入（`import-chats.py` → chats/code/）

- [x] **REQ-D1** 记忆引擎决策（已定单轨纯文件 + ripgrep）（双轨文件+LanceDB vs 单轨文件）

- [x] **REQ-E2** 项目状态看板 Artifact（brain-vault-dashboard）

- [x] **REQ-F2** 所有 brain 注册项目补齐 GOTCHAS.md

### P2（锦上添花）

- [x] **REQ-B3** 孤儿笔记检测（`find-orphans.py`）（permanent/ 笔记 wikilink < 2 的标红）

- [x] **REQ-C2** Claude Web/App 手动导出指引（chats/README.md）

- [x] **REQ-C3** Graphify 集成手册（`run-graphify.sh` + references/graphify-集成.md）

- [~] **REQ-D2** 语义检索 API — 搁置（架构决策已排除 LanceDB）

- [x] **REQ-G2** 备份策略（references/备份策略.md + `backup-icloud.sh`）

