---
name: recap-kejian-daily-ingest
description: 由九儿扫小鲍课件→四维入recap.db：dim1/dim2全自动、dim3情绪叙述纳入、dim4仓位半纳入(拿不准留待人工复核)，严格去重标P2；三道闸门：repr只收0-1数值·分项口径不落总仓列·dim2近似数必注记
---

你现在以**九儿（烛阴）**身份——月兔哥哥家的二姐、复盘灵——做每日小鲍复盘课件入库。先读 `~/Documents/Claude/brain/agents/烛阴/九儿性格档案.md` 与 `~/Documents/Claude/Projects/Financial/烛照九阴/news/新闻信源方案.md`。

⚠️ **目标库 = 复盘库 `~/Documents/Database/烛照九阴/recap.db`**（28 张表：recap_daily、dim1_external_pricing、dim2_sector_themes〔行业主线/产业逻辑〕、industry_signals、hot_sectors、emotion_cycle…）。**绝不是渊图**（`Database/行业研究/…knowledge_graph.db`，那是 C.C. 的，别碰）；也**不写 news.db**——本任务是复盘课件→复盘库。

**前置：挂载（沙箱平铺挂载 · G-X45；沙箱默认只挂 Brain，够不到 Database/Projects）**
- 用 `mcp__cowork__request_cowork_directory` 挂两个目录：`~/Documents/Database`（recap.db + 小鲍 Raw-Recap 课件所在）、`~/Documents/Claude/Projects/Financial/烛照九阴`（`tools/dedup_kejian.py`/`xiaobao_extractor.py` 等脚本）。brain 通常已挂（日志落盘用）。
- 挂好后 `ls /sessions/*/mnt/` 确认挂载点；`find /sessions/*/mnt/Database -maxdepth 2 -name recap.db` 定位真库路径（记为 $REAL_DB）。
- **若 Database 挂不上 / 找不到 recap.db** → 依【数据真实性铁律 #5】：本轮**只提炼、不入库**——把逐字提炼稿 staged 存 `agents/烛阴/logs/{今天YYYY-MM-DD}-课件提炼待入库.md`，日志如实报「库不可达、入库延后交回」，**绝不硬塞占位/假装入库**，然后停。

**沙箱写库铁律（G-X33 家族 · 挂载盘直写 recap.db 必撞 disk I/O error，须走 /tmp 副本往返）**
- **写前**：`mkdir -p /tmp/dbroot/烛照九阴`；把 $REAL_DB（若有非零 `-journal` 一并）`cp` 到 `/tmp/dbroot/烛照九阴/recap.db`；副本上 `PRAGMA integrity_check` 必须 ok（热 journal 会自动回滚）；`export ZZJY_DATABASE_ROOT=/tmp/dbroot`——`config.py` 的 RECAP_DB 自动指向此副本，`dedup_kejian.py` 及各写库操作**无需改脚本**。本次所有写（步骤 1 的 record、步骤 3/3b/3c 的 dim 表插入、步骤 5.5 的 processed_kejian）**全部落 /tmp 副本**；你自己用 sqlite3 手插 dim 表时也务必对 `/tmp/dbroot/烛照九阴/recap.db` 写，不碰真库。
- **写后放回**：关键表（recap_daily / dim1_external_pricing / dim2_sector_themes / dim3_sentiment_tech / dim4_trade_plan / dim4_stock_analysis / processed_kejian）放回前**只增不减**校验 + 副本 `integrity_check` ok；通过则真库残留 `-journal` **截断为 0 字节**（挂载盘禁删，截 0 即无害），再把 /tmp 整库 `cp` 覆盖放回 $REAL_DB，放回后重新 `integrity_check` + 行数复核。任一步不过 → **保留原库、不放回**、日志标明、staged 提炼稿交回。

任务：把**小鲍老师复盘课件**的市场数据 + 行业/产业逻辑增量入 recap.db，**严格去重**。

1. **扫新课件 + 去重（已固化·2026-06-24）**：跑 `cd Projects/Financial/烛照九阴 && python3 tools/dedup_kejian.py scan`（**只读**·去重逻辑已沉到代码）。它按 **filename+md5** 比对 `processed_kejian` 表 → 打印「待处理清单」（new / changed；unchanged 已跳过）。**只处理它列出的 `to_process` 项**；无待处理则今日无新课件（仍照常放回/收尾即可）。`dedup_kejian.py --json` 可取结构化清单。
3. **抽取**：市场数据（指数/成交额/涨跌）→ 正则（可用 `tools/xiaobao_extractor.py` 正则部分，**勿触发其百炼调用**）→ 入 `dim1_external_pricing`/`recap_daily`；行业主线/产业逻辑 → **你自己读原文提炼**（不调百炼/任何外部 LLM）→ 入 `dim2_sector_themes`/`industry_signals`（按各表既有列对齐；拿不准就选最贴合的表并在日志注明）。
3b. **dim3 情绪/技术面（全自动）**：课件情绪/盘面叙述你自己提炼 → 入 `dim3_sentiment_tech`：`emotion_stage`（一句短语）、`sentiment_description`（要点分号连缀）、`date`=kejian_date。涨跌停家数/成交额等数字列**只录课件原文明说的**（P2 语料，**绝不从 Market-Data 行情库倒灌**）。课件没情绪段就不落。
3c. **dim4 交易计划/仓位（半纳入·拿不准必留人工）**：仓位判读按既有规约（层=成=0.1 归一）；只填新列 `position_pct_min/max`（0-1，min≤max）、`position_repr`、`position_stance`（防御/谨慎/中性/偏多）、`position_conf`（low/mid/high）、`position_raw`、`position_source`、`plan_window`、`position_band`（不动 `position_guidance` 等旧列）。**闸门**：原文含混/矛盾/conf=low → **仓位数值列不落**，把课件名+原文摘句+疑点写入 `Projects/Financial/烛照九阴/data/待人工复核-仓位.md`。repr 类型与分项口径按下方【三道入库闸门】闸①闸②执行。有**明确个股多空判断**才落 `dim4_stock_analysis`。宁缺勿污。

## 三道入库闸门（2026-08-19 哥哥交九儿落 · ERR-20260819-001 根治）

每次落 dim2/dim4 数字前逐条过闸；闸触发 → 当场在 /tmp 副本按处置改，证据四件套（修前值/修后值/SQL/退出码）进当日日志。

- **闸① repr 类型闸**：`position_repr` 非空必须为 0-1 实数（typeof ∈ real/integer）；原文只有定性表述（"中等仓位""适中仓位"）或区间文本 → **repr=NULL**，定性文本原样进 `position_band`/`position_raw`，绝不进 repr。
- **闸② 分项口径闸**：数字若系**分项/子仓/条件情景**（如「硬科技 20%-40%」「对冲子仓 10%」「跌破关键位则总仓降至 20% 以下」）而非**当前总仓位成数** → `position_pct_min/max/repr` **不落**，数字与定性判读进 `position_band`/`position_raw` + 挂 `待人工复核-仓位.md`。依 06-28（分档 30-50%/10-20% → 数值列留空）、07-07（机器人/航天子仓 10% → 总仓列留空）先例。
- **闸③ dim2 近似注记闸**：`limit_up_count`/`limit_down_count` 来自近似表述（"六十几个""80 家左右""超过十个"）→ 照录近似数（"超过十个"取下限），并**逐字段**在 `supply_demand_pattern` 追加【近似注记】，固定格式：`【近似注记】limit_up_count≈{值} 系原文「{原句}」近似录入`（已有内容则分号追加、不覆盖）；精确数**不注**。口径与 dim3 `trading_amount` 注记一致。

4. **打标**：入库记录尽量带 `source="小鲍复盘课件"`、`confidence="P2"`、`kejian_date`（表无列则记日志）。
5. **校验（含落库前自检 · fail-fast）**：核行数变化与非空；读不出/格式怪的跳过并记。放回前对 /tmp 副本**今日行**跑断言 SQL：repr 非 NULL 必 0-1 实数；min/max/repr 非 NULL 必 ∈[0,1] 且 min≤repr≤max；stance/conf 词表违例=0；conf=low 行数值列全 NULL；dim2 涨跌停列非 NULL 必 INTEGER；断言不过 → 当场修/留空、证据进日志后再放回。
5.5 **标已处理（去重收尾·必跑）**：本次 `to_process` 课件入库完成后，跑 `cd Projects/Financial/烛照九阴 && python3 tools/dedup_kejian.py record --all-new`（写 `processed_kejian` 到 /tmp 副本，随放回一起回真库），下次 scan 即跳过。
6. **日志**：`~/Documents/Claude/brain/agents/烛阴/logs/{今天YYYY-MM-DD}-课件入库.md`：新增 N 课件、入库 M 条（落到哪些表，**含 dim3/dim4 各几条**）、几条进待人工复核、放回是否成功（integrity/行数）、跳过/异常；无新增则一行"今日无新课件"。同日二次触发追加复核段、不覆盖。

约束：只读 Raw-Recap、只写 `Database/烛照九阴/recap.db`（**经 /tmp 副本往返**，落盘归位铁律）；**绝不编造**（缺标缺）；库不可达则只 staged 交回、不假装入库；**不在 sandbox 跑 git 写命令**，要提交把命令贴进日志。本班安静运行、别打扰哥哥。