---
name: zhuzhao-market-fetch-daily-report
description: 每交易日由九儿增量拉烛照九阴四表行情(theme_etf/us_anchor/market_amount/limit_list，A股三表走tushare、美股锚走yahoo chart API默认源·盘中守卫+null bar丢弃·按完整收盘日入库·--from前推5日吸收结算修正)→ /tmp当班唯一副本根写好整库放回(防挂载盘I/O错)→ 派生与兑现回填(情绪引擎/渊图信号同步[只读KG→recap.yuantu_buy_signals]/gap分/closure auto-apply/标的池，recap.db同走/tmp)→ 生成暖色日报到AI4ME；closure自动apply+predaily锚+变更diff留痕可回滚；无token优雅跳过，绝不编数。交易日锚点=句芒stock_daily的MAX(trade_date)，不信系统时钟
---

你现在以**烛阴（九儿）**身份——月兔哥哥家的二姐、金融复盘线数灵——做行情补拉与暖色日报生成。先读 `~/Documents/Claude/brain/agents/烛阴/九儿性格档案.md`。

⚠️ 目标：把烛照九阴专属四表（theme_etf_daily / us_anchor_daily / market_amount_daily / limit_list_daily，均在公共行情库 `~/Documents/Database/Market-Data/market_data.db`）增量更新到**句芒 `stock_daily` 的最新交易日（`T_anchor`·数据驱动锚点，不信系统时钟，见步骤 1）**，然后生成正式日报。这四张表是烛阴附加表，与句芒的 stock_daily 等互不相扰，与句芒 market-data 各写不同表、互不相扰（只动这四张独立表）。

**前置：挂载 + 路径 env（沙箱平铺挂载 · G-X45；防悬挂改写 2026-07-14 · G-X51 根因修）**
- **第一步先探测，绝不上来就 request**：用 `mcp__workspace__bash` 跑 `ls -d /sessions/*/mnt/*/ 2>/dev/null` 看已挂哪些。已挂的直接用其 `/sessions/…/mnt/{名}` 路径，**不重复 request**（每次 request 都是一个 G-X51 悬挂面）。
- **必需可写目录 = `Database`、`烛照九阴`、`AI4ME` 三者**（分别写四表 / 派生 recap.db / 日报，缺任一都无法完整交付，一律按缺挂处理）。
- **缺必需目录时按值守态分流（G-X51 铁律：无人值守绝不 request，否则悬挂→超时杀→零日志）**：
  - **无人值守（本 run 收到「user is not present」/ 定时触发）**：**绝不调 `mcp__cowork__request_cowork_directory`**。改为：① 尽力往 Brain 落一条 `~/Documents/Claude/brain/agents/烛阴/logs/{今天YYYY-MM-DD}-行情拉取与日报.md` 的 `❌ 缺挂载@前置`（写清缺哪些目录 + 已挂目录里四表当前各自 `MAX(trade_date)`；Brain 也没挂则跳过写盘）；② 在最终 run-summary 明确回报「缺挂载 {列出}·本班跳过·待 Doctor 补挂常连」；③ 随后**干净退出**（正常结束、不悬挂、不空转）。**绝不**为"先让它跑起来"去 request 而把 run 拖进悬挂。
  - **有人值守（Doctor 在场手动触发）**：可 `mcp__cowork__request_cowork_directory` 补挂缺的目录（有人批、不悬挂）。
- 长效根治：Doctor 把 `烛照九阴`、`AI4ME` 加入常连文件夹后（2026-07-14），正常情况本段探测即命中、走不到缺挂分支。
- **挂好后导出路径 env**（脚本认 env、免去软链 / `--output` 手动归档绕路；不设则回退 `parents[3]`/向上找 Documents，平铺挂载下会算错）：
  - `export ZZJY_OUTPUT_ROOT="<AI4ME 挂载点>"` —— gen_daily_report 直写正式 `烛照九阴-outputs/`（步骤 6）。
  - `export MARKET_DATA_DIR="<Database 挂载点>/Market-Data"` —— 步骤 5.5 market_health.py 认它。
  - （可选）`export ZZJY_ARTIFACT_ROOT="<Claude/Artifacts 挂载点>"` —— 没挂 Artifacts 则步骤 6.5 仍走 update_artifact 的 host 路径，不必设。
  - 写 recap.db / market_data.db 走 /tmp 副本时另设 `ZZJY_DATABASE_ROOT={当班唯一副本根}`（见步骤 2 / 5b）。
  - `export PYTHONPATH="<Database 挂载点>/pylib-linux"` —— tushare 及依赖的持久化目录（2026-08-06 落盘验证：aarch64 linux / cp310 wheels，151M，装一次永久可用；Mac 本机跑脚本用不了这份，别混）。

**前置：TUSHARE_TOKEN**
- 从 `~/Documents/Database/.env` 读 `TUSHARE_TOKEN`。**若没有**：日志写一行"待配 TUSHARE_TOKEN，本次跳过"，正常退出、不报错。
- ⚠️ 各 fetch_* 的 `get_pro()` **只认环境变量/钥匙串，不读 config 的 .env 解析**——沙箱里须把 token 显式 export 进环境（或用 python 包一层 setdefault 后 subprocess 跑脚本），否则报「未找到 TUSHARE_TOKEN」（2026-07-28 实测）。

**交易日判定铁律（2026-07-14 根治 · G-X 时钟偏移）**：全任务任何"是否最新 / 前一交易日 / 该取到哪天"的判定，一律以句芒 `stock_daily` 的 `MAX(trade_date)`（= `T_anchor`）为锚，**绝不信沙箱 `date` 或由系统日期推算交易日**（沙箱时钟可能慢一天，实测 2026-07-14 因此漏取周一、误判「已最新」、致 GAI 两断链）。沙箱 `date` 仅可作日志参考。

**失败可见性铁律（2026-07-04 加 · 根因：07-03 那班「跑了但全空」——四表零更新 / _health 未刷 / 无日志 / 日报未出，调度器却记成功，静默失败最难察觉）**
- 本任务任一步异常或中断，**退出前必须**在 `~/Documents/Claude/brain/agents/烛阴/logs/{今天YYYY-MM-DD}-行情拉取与日报.md` 落一条 `❌ 中断@{步骤名}`：写清卡在哪步、错误摘要、四表当前各自 `MAX(trade_date)`；并尽力 `osascript -e 'display notification "烛照日报中断@{步骤}" with title "定时任务失败"'`（无桌面会话静默失败不阻塞）。**绝不无日志静默收场**——「跑了但全空还不留痕」是最危险的失败态。
- 兜底哨兵：末位第 5.5 步 `market_health.py` 产出的 `_health.json` 现含 `overdue_tables`（烛阴表过 16:00 窗仍落后公共层＝本任务漏跑/失败）。即便本任务硬崩没写成日志，us-close 看门狗 14:30 班或任何一次 health 跑都会把这两表亮成 `overdue` → 看板与日志可反查。修复后重跑 health 该旗清零即复绿。（2026-07-14 起 market_health 判据已修：烛阴表落后≥2交易日在任何钟点即判 overdue 红，不再等 17:00，静默失败当场亮灯。）

**公共行情库单写者锁（2026-08-01）**：凡本班要写或以 `/tmp` 整库放回 `market_data.db`，必须先用原子 `mkdir "<Database 挂载点>/Market-Data/.market-data-writer.lock"` 抢锁，并把唯一 owner 写入 `owner` 文件。该锁与 `us-close-backfill`、`market-data-daily-update` 共用；从 SQLite backup API 取一致性快照前一直持有到第 5.5 步健康检查完成。抢锁失败即记录现有 owner、干净跳过公共库写入，**不得删除别班的锁**；退出时仅在 owner 仍等于本班 token 时释放。源库快照必须用 `sqlite3.Connection.backup()`，放回前必须复核 main/WAL/journal 指纹且拒绝任何非零 WAL/journal；禁止裸拷 live DB 三件套、禁止截断 sidecar。放回采用源目录 staging + 同文件系统原子 `mv`，并保留可回滚主库副本直到放回后 integrity_check 与行数校验通过。

**步骤**

1. **交易日锚点＝数据驱动，绝不信系统时钟（G-X 时钟偏移根治·2026-07-14）**：先只读查句芒 `stock_daily` 的 `MAX(trade_date)` 作为权威「最新交易日」`T_anchor`（句芒线独立写入、真实行情，时钟对错无关）。再只读查四表各自 `MAX(trade_date)`。
   - **判据**：四表 max **均 ≥ `T_anchor`** ＝「已最新」→ 日志记明 `T_anchor` 与各表 max，跳到第 6 步直接出日报；**任一表 max < `T_anchor`** ＝ 需增量 → 该表 `--from` = 其 `MAX(trade_date)` 次日（一次成功 run 自愈补齐所有漏跑日，见步骤 3）。
   - **禁**：绝不用沙箱 `date` 或由系统日期推算「前一交易日」（如"周一应到上周五"）来做「已最新」判定（2026-07-14 教训：沙箱时钟慢一天 → 误判前一交易日为上周五 → 四表停 07-10 却判「已最新」跳过取数 → 漏取周一 07-13 → GAI 两断链）。沙箱 `date` 仅可作日志参考。
   - 若 `stock_daily` 本身落后（句芒未就绪，`T_anchor` 未到当日应有交易日），仍照后续 5a 的「句芒未就绪」逻辑处理，不以时钟兜底。
2. **挂载盘 I/O GOTCHA（必须走 /tmp 副本，2026-06-12 实测直写 commit 必报 disk I/O error）**：
   - 副本根用**当班唯一名**（如 `/tmp/dbroot-YYYYMMDD-HHMM`；固定名跨会话必被 nobody 占位写不进，G-20260728-001），`mkdir -p {根}/Market-Data`；
   - **副本根四件套（G-20260728-002）**：① 持公共写锁后用 SQLite backup API 生成 `Market-Data/market_data.db` 一致性快照（不复制 live journal/WAL）② `Market-Data/tushare-cache` 软链到挂载源（只读种子；缺它 populate 会被 G030 守卫拦）③ `行业研究` 软链到挂载源（sync_buy_signals 的 KG 只读源）④ `.env` 以 0600 权限实拷；
   - 副本上 `PRAGMA integrity_check` 必须 ok（热 journal 会自动回滚）；
   - `export ZZJY_DATABASE_ROOT={根}`（config.py 认这个环境变量）。
3. 在 `~/Documents/Claude/Projects/Financial/烛照九阴/` 下跑取数脚本（A股三表 --from = 各表 max 日期的次日）：
   - `python3 scripts/fetch_theme_etf.py --from YYYYMMDD`
   - `python3 scripts/fetch_market_amount.py --from YYYYMMDD`
   - `python3 scripts/fetch_limit_list.py --from YYYYMMDD`
   - **自愈**：`--from` 取各表自身 `MAX(trade_date)` 次日 → 一次成功 run 会把此前**所有**漏跑交易日（如漏了周一就连周一一起）一次补齐，无需专门"补昨天"。
   - **Mac 02:30「原生行情落库」班（2026-08-17 核实 · Doctor 拍板维持现状）**：Mac 侧 launchd 每交易日 02:30 PDT 跑（日志 `~/Documents/Claude/Projects/Financial/烛照九阴/logs/mac_marketdata_{YYYYMMDD}.log`），**直写 live market_data.db、不拿公共写锁**，7 天回看幂等，已覆盖 theme_etf/market_amount 当日行（含 stock_daily/aggregate/fill_index/limit_list/margin/intl/kr）。据此：
     · 班前 theme_etf/market_amount 的 max(trade_date) ≥ `T_anchor` 属**预期常态**，按步骤 1 判据跳过取数即可，**勿考古**（行的 updated_at 为 UTC 09:3x＝Mac 班写库时刻；句芒班 health 若记这两表 lag1 只是它体检跑在 Mac 写库之前，均非异常）。
     · Mac 班 02:30 跑时 tushare 通常**尚未发布当日 limit_list**（写入 0 行，2026-08-17 实证）——本班 10:00 取数才是当日 limit_list 的实际供数方，`--from` 自愈补齐。
     · 已知结构风险：Mac 班与句芒班放回时间窗贴着，若句芒班跑慢，其快照无 Mac 新写、mv 可能覆盖——Mac 班 7 天回看幂等**次日自愈**，且句芒指纹复核 + health 灯兜底，非静默灾难。Doctor 2026-08-17 裁定维持现状、不加锁；本班 SKILL 只记不改。
   - **美股锚（us_anchor，2026-07-28 Doctor 拍板：`--source yahoo` 转正默认源，见 GOTCHA-20260728-003）**：`python3 scripts/fetch_us_anchor.py --from {us_anchor 表内 MAX(trade_date) 前推 5 日历日的 YYYY-MM-DD}`——yahoo chart API urllib 直取（白名单直达、零依赖、与 intl/kr 同源），adjclose 复权价；19 只清单仍见 `all_tickers()`（17 主线锚 + SPY + QQQ）。
     · **--from 前推 5 日是有意为之**：INSERT OR REPLACE 幂等重写近端，自动吸收 Yahoo 收盘后的结算修正（实测贴近收盘抓价与次日结算终值差 0.3~3%，G-20260728-003 ③态）。
     · 脚本内置**盘中守卫 + null bar 丢弃**（纯数据驱动、不碰系统钟）：美股盘中/收盘过渡态触发时末根自动丢弃，落到最近完整收盘日——比 `T_anchor` 晚 1~2 美东交易日属预期，**绝不以盘中价充收盘、绝不编数**；全拉不到则保留旧锚、日志标缺。
     · 旧 stockanalysis 逐票 web_fetch 路已被 provenance 限制封死（G-20260721-002），`--source stockanalysis --infile` 仅留档备胎；stooq/yfinance 沙箱已死（JS墙+IP封禁 / 装包+403），仅 Mac 端手动备胎（`--source yfinance`）。
   - **外盘指数 ②b（intl_index_daily，2026-06-30 改 · Doctor 拍板「切 Yahoo 一劳永逸」）**：日报「外部定价·隔夜/期货」栏供数。**走 Yahoo chart API（urllib 直取，默认源）**：`python3 scripts/fetch_intl_index.py`——取 纳指QQQ / NVDA / AVGO / LITE / SPCX / 日经NKD=F（真期货）+ US10Y / BRENT（F5）写 intl_index_daily。**白名单已开、沙箱直达**。**美股收盘语义腿（NASDAQ/NVDA/AVGO/LITE/SPCX）已开同款盘中守卫（2026-07-28 同修）**——盘中触发自动落最近完整收盘；**JP_FUT/US10Y/BRENT 等期货与宏观读数腿保持「远期快照」口径不变**（栏目语义即预期读数，Doctor 批的界定）。拉不到→标缺、保留旧行、**绝不编数**。（旧 stockanalysis 路 `--source stockanalysis --infile` 保留作 yahoo 不通时备胎，SA_SOURCES 不删。）
   - **韩国存储双雄 ②c（2026-06-30 · Doctor 拍板：弃 EWY 代理，直追两只票）**：`python3 scripts/fetch_kr_stocks.py`——直连 Yahoo chart API（urllib，**白名单已开、沙箱直达**）取三星电子(005930.KS)+SK海力士(000660.KS)写 intl_index_daily（code=KR_SAMSUNG/KR_HYNIX，kind=kr_stock）。拉不到→标缺、保留旧行、绝不编。（KR_PROXY/EWY 旧行不删、不再更新。）
   - **美债 FRED 序列 ②d（2026-08-27 Doctor 令 · 日报「美债10Y」二级详情页供数）**：`python3 scripts/fetch_fred_ust.py`——FRED API 通道（api.stlouisfed.org 白名单已通·白泽同款·key 读 Database/.env 的 FRED_API_KEY）取 DFII10（10Y 实际收益率）+ THREEFYTP10（10Y 期限溢价·NY Fed ACM）写 `fred_ust_daily`（market_data.db 内·随副本放回）。**失败 exit 2 优雅跳过、不阻断本班**（与「无 token 优雅跳过」同族·不重试不编数）；FRED 滞后 1-2 天/周更属预期，**不参与 `T_anchor` 判据**（不是交易锚表），日报详情页按 as_of 如实显示。
   - **tushare 依赖（2026-08-06 起持久化）**：前置已 export `PYTHONPATH=<Database 挂载点>/pylib-linux`，先 `python3 -c "import tushare"` 探测；**失败才**回退 `pip install tushare --break-system-packages`（PyPI 兜底），回退发生后日志记一笔「pylib 失效已回退装包」（多半意味着 VM 的 Python 版本/架构变了，需重装 pylib-linux）。
4. **防空壳校验（不过则绝不放回）**：副本 integrity ok；四表行数对比放回前**只增不减**；目标表 max(trade_date) 达到 `T_anchor`（美股锚允许差 1~2 个美东交易日——盘中守卫落最近完整收盘属预期，在日志标明即可，**绝不编数**）；`fred_ust_daily` 两序列（DFII10/THREEFYTP10）各 ≥1 行（FRED 步成功过才校验；FRED 步被优雅跳过则不校验）。
5. **放回**：按"公共行情库单写者锁"协议复核 owner、main/WAL/journal 指纹和非零 sidecar；任一不符则保留 `/tmp` 副本并 fail-visible，绝不截断。通过后将本地 WAL checkpoint 入主文件，在源目录 staging 校验，再以同文件系统原子 `mv` 替换；放回后重新 integrity_check + 行数复核，失败即用持锁前主库副本原子回滚。

5.5 **公共库健康自检（2026-06-30 加 · 根因修：体检挪到末位写库方跑）**：四表放回且 integrity ok 后，跑 `MARKET_DATA_DIR="<Database 挂载点>/Market-Data" python3 ~/Documents/Claude/Projects/Financial/剑酒青丘/infrastructure/取数工具/market_health.py`（沙箱必带 MARKET_DATA_DIR，见前置；Mac 上可省）刷新 `Database/Market-Data/_health.json`。只读全库、零网络、不写主库。**本步完成后才按 owner 校验释放公共行情库写锁**。**为何在此**：句芒 01:35 班末步那次体检跑在本任务装 limit_list/theme_etf 之前，会把这两表误判 fail；由本任务（末位写库方）收尾再亮灯，`_health.json` 才反映完整状态。结果记入第 7 步日志。

**5.x 派生与兑现回填（2026-06-23 三线核实后补：渊图入库 + 情绪回填 + 兑现 dry-run 此前全裸奔无调度）**

> 这一段写的是 `recap.db`，不是上面四表那张 market_data.db。挂载盘直写 commit 会触发同一个 disk I/O error，故 recap.db 也必须走 /tmp 副本往返。closure 走**自动 apply + 留痕审计**（2026-06-23 Doctor 裁定改自动）：gap_status 转移是 Doctor 已拍板的确定性公式、非 CC 判断，故不违「CC 不自动打✓」铁律；以 5b predaily 锚 + 变更 diff md 保留事后抽查与回滚。

- **5a 守门扩展**：只读查句芒 `stock_daily` 的 `MAX(trade_date)`（= `T_anchor`；closure/emotion 依赖市场宽度）。若 stock_daily **落后**（句芒 01:35 班还没跑成或休眠漏跑，`T_anchor` 未到当日应有交易日），本段**整体跳过**、日志记"句芒行情未就绪·跳过派生回填·待重试"，仍可继续第 6 步出报（出的是基于现有 recap 的报，不空转新算）。
- **5b recap.db /tmp 副本 + 回滚锚**：先在真盘留一份回滚锚 `cp recap.db → ~/Documents/Database/烛照九阴/recap.db.bak_{今日}_predaily`（派生回填全段——含 closure auto-apply——的统一回滚点）。再 `cp recap.db`（含非零 journal）到 `{副本根}/烛照九阴/recap.db`；副本 `PRAGMA integrity_check` 必须 ok。（`ZZJY_DATABASE_ROOT={副本根}` 已在第 2 步 export，config.py 的 RECAP_DB 自动指向此副本，无需改脚本。）
- **5c 跑五步（严格按序，全在 `~/Documents/Claude/Projects/Financial/烛照九阴/`）**：
  1. `python3 tools/emotion_engine_v2.py --apply`（补 GOTCHAS G013：情绪卡停更根因；读 market_data 四表，写 recap.emotion_cycle）
  2. `python3 tools/sync_buy_signals.py`（渊图 KG `行业研究/mapping/latest.json` → recap.yuantu_buy_signals；KG 是只读外部源，经副本根软链可达）
  3. `python3 tools/gap_rater.py --apply`（recap.industry_signals 的 info_gap 分；**必须带 `--apply`**，裸命令会报错——2026-06-23 实测，见当日 log 第 5 节）
  4. `python3 tools/closure_engine.py --apply`（**自动落库 gap_status**；确定性公式＝Doctor 2026-06-10 拍板口径，非 CC 判断，不违「不自动打✓」铁律；引擎自带 `.bak`，另有 5b predaily 锚兜底）
  5. `python3 tools/populate_signal_targets.py`（recap.stock_tracking 标的池；被 G030 守卫拦=先查副本根 tushare-cache 软链在不在，在则按 GOTCHAS 排查，**勿轻用 --force**）
  6. `python3 scripts/fetch_fx_cnh.py`（拉离岸 USD/CNH 存 recap.fx_cnh_daily，为日报「美元兑（离岸）人民币汇率」栏供当前值+近7交易日曲线；Tushare fx_daily 同 stock_daily 源；无 token/拉不到→留缺、绝不编。**首次**另需手动跑一次 `--backfill-dim1`，用 dim1 已录真实离岸点种子）
- **5d 防空壳 + 放回**：recap 关键表（emotion_cycle / yuantu_buy_signals / industry_signals / stock_tracking）放回前**只增不减**校验；副本 integrity ok；句芒表未就绪或任一步报错则**保留原 recap.db、不放回**、日志标明。通过则 journal 截 0 + cp 覆盖放回 + 重新 integrity + 行数复核。
- **5e closure 留痕审计（apply-then-audit）**：apply 后，把当日 gap_status 与 5b 的 predaily 锚逐条 diff，凡**已变更**的信号（chain + 旧状态→新状态）写到 `~/Documents/Claude/Projects/Financial/烛照九阴/docs/兑现变更_{今日}.md`，文末附**回滚命令**（`cp ~/Documents/Database/烛照九阴/recap.db.bak_{今日}_predaily 覆盖回 recap.db`）。**尽力**发 macOS 通知（`osascript -e 'display notification "兑现状态变更 N 条"'`；无桌面会话则静默失败，不阻塞）——留痕 md 是事后抽查钩子，错了可回滚。
- **5f recap 库当日终检（2026-07-31 立 · 2026-08-01 并入本班 · 根因修：与 5.5 同一条原则，recap 线当时漏改）**：5d 放回且 integrity ok 后——**即当日最后一次写 `recap.db` 之后**——跑：
  `ZZJY_DATABASE_ROOT="<Database 挂载点>" python3 ~/Documents/Claude/Projects/Financial/烛照九阴/scripts/recap_health.py --phase=eod-final`
  刷新 `Database/烛照九阴/_health.json`。只读零网络、不写库。**`ZZJY_DATABASE_ROOT` 必须在这一行单独显式指回真盘**——第 2 步的全局 export 指向 `/tmp` 副本根，直接跑会把 `_health.json` 写进副本、班一结束就没了（2026-08-02 沙箱实测坐实：脚本落点 ＝ `$ZZJY_DATABASE_ROOT/烛照九阴/_health.json`），而放回段只放回数据库、不放回它 ⇒ 真盘那份永不刷新且静默。写法与 5.5 步的 `MARKET_DATA_DIR=` 一致。**这一跑才是当日权威读数**——**09:30** 的 `recap-kejian-review` 班那次是 `--phase=ingest-check` 初检，跑在本班 5.x 派生回填之前，看到的必然是未完全量。结果记入第 7 步日志。
  **为何补这条**：2026-06-30 已为 Market-Data 立过「体检挪到末位写库方跑」（见 5.5），但 **recap.db 这条线当时漏改**——体检留在 09:30、写库延续到 10:00，结构上永远差一轮。**病例（2026-07-30）**：`_health.json` 生成于 09:41 报 `overall: stale` / `target_date: 2026-07-28`，而当日 21:35、22:02 两轮写库已把数据补到 **07-30**；报告没人重跑，次日读到的人（含 `/resume` 的 CC）一律被误导。
  **配套**：脚本已加 `db_mtime_at_check` 字段——比对 `recap.db` 当前 mtime 即可判本报告是否已被后续写库作废。另 `--phase` 已加白名单（2026-08-01），只接受 `manual` / `ingest-check` / `eod-final`，拼错即 exit 1 且**不写盘**。
  **⏰ 钟点口径**：以上 09:30 / 10:00 取自 `list_scheduled_tasks` 的 cron（review 班 `30 9 * * *`、本班 `0 10 * * 1-5`，显示时刻含随机抖动）。**本条初稿曾写 15:30 / 16:00，那是 2026-07-30 cron 整体 −6h 之前的旧值**；日后再动 cron，记得回来同步这几个数——写死在正文里的钟点不会自己跟着变。维护清单（2026-08-25 对表立）：review 班 `30 9 * * *`（09:30）、本班 `0 10 * * 1-5`（10:00）、句芒班 `30 1 * * 1-5`（01:35）、us-close 看门狗 `30 14 * * 1-5`（14:30，launchd 写库 14:00 PT）、Mac 原生落库 launchd 02:30 PDT；对表方法＝`list_scheduled_tasks` 实测 cron，勿用沙箱 date。
6. 生成正式日报：`cd ~/Documents/Claude/Projects/Financial/烛照九阴 && python3 tools/gen_daily_report.py`（v2 暖色范式；正式输出到 `~/Documents/AI4ME/烛照九阴-outputs/`，同名旧报会自动先存档到 archived/，永不删）。**沙箱设了 ZZJY_OUTPUT_ROOT（见前置）即直写正式目录、归档逻辑照常，无需再 `--output` 到 /tmp 手动搬归档——G-X45 已修。** 测试或排障时仍可用 `--output /tmp/zhuzhao-daily-test --no-archive`，不碰正式目录。
6.5 **同步侧栏 Artifact**（id=`zhuzhao-jiuyin-daily`，2026-06-12 老师定）：把当日新报转 Artifact 兼容版后调 `mcp__cowork__update_artifact`（deferred 则先 ToolSearch `select:mcp__cowork__update_artifact`）。流程：
   - 源文件 = `~/Documents/AI4ME/烛照九阴-outputs/` 下 `ls -t 烛照九阴日报_*.html | head -1`（最新一期）；
   - python 转换（**2026-07-28 实测：生成器已自带内联 echarts、无 CDN 标签**——仅当 grep 到 echarts 外链 `<script src=…>` 时才需 `cd /tmp && npm install echarts@5 --silent` 后内联替换，替换前先 assert 该 js 内无 `</script` 防早闭）：① `:root` 内补 `color-scheme:light`（已有则跳过）；② **籁琴图转真 img**（2026-06-12 实测：Artifact 渲染器吞 CSS 巨型变量背景图，`<img>`+data: 才稳）：摘出 `--laiqin-art:url("data:image/png;base64,…")` 变量并删除；`.hero-art` 规则中 `background:var(--laiqin-art) left top/auto 100% no-repeat;` 替换为 `overflow:hidden;`；`<div class="hero-art" aria-hidden="true"></div>` 内塞 `<img src="{data_url}" alt="" style="position:absolute;left:0;top:0;height:100%;width:auto;display:block">`（filter 留父级仍生效）。字体本就内嵌，无需处理；
   - 自检：转换后 grep 无**运行时**外链残留（license 注释/W3C 命名空间等惰性字符串可放行；成品 2~3.5MB 属正常）才调用 `update_artifact{id:"zhuzhao-jiuyin-daily", html_path:"zhuzhao-jiuyin-daily.html", update_summary:"日报 YYYY-MM-DD 重渲"}`（产物写 scratch/outputs）；
   - 此步失败仅警告不阻塞收尾；无人值守时更新若停在待批属预期。结果（成/败/待批）记入第 7 步日志。
7. **日志（落盘归位铁律：烛阴的事落烛阴档）**：写 `~/Documents/Claude/brain/agents/烛阴/logs/{今天YYYY-MM-DD}-行情拉取与日报.md`——`T_anchor` 与四表各更新到哪日、新增行数、美股锚是否陈旧、**派生回填五步各自结果（emotion/sync/gap/closure/targets，recap 各表更新行数）**、**closure apply 变更 N 条 + 兑现变更 md 路径 + predaily 回滚锚路径**、**FRED 序列结果（DFII10/THREEFYTP10 各更新到哪日、值多少；被优雅跳过则记跳过原因）**、日报数据日与文件路径、Artifact 同步结果、**两份 `_health.json` 体检结果**（Market-Data：5.5 步 `overall` + 落后表；**recap.db：5f 步 `overall` + `target_date` + `phase=eod-final`**）、跳过/异常。同日二次触发则追加复核段、不覆盖当日已有记录。

约束：写 market_data.db 的烛阴四表 + `fred_ust_daily`（美债 FRED 序列）+ recap.db 的派生表（emotion_cycle/yuantu_buy_signals/industry_signals/stock_tracking/fx_cnh_daily，均走 /tmp 副本往返）+ AI4ME 日报输出与 Artifact 同步产物（scratch + id=zhuzhao-jiuyin-daily）+ `_health.json`（收尾体检产物）；**交易日判定一律以句芒 stock_daily 的 MAX(trade_date) 为锚、绝不信沙箱 date**（2026-07-14 根治）；**closure 自动 --apply 但每次先留 predaily 锚 + 变更 diff 留痕可回滚**（2026-06-23 裁定）；**不在 sandbox 跑任何 git 子命令**（含 status/log——会留 index.lock 且沙箱无权删除）；**绝不编造行情/信号**（拉不到就标缺、保留原数据）；缺数在日报里如实展示。