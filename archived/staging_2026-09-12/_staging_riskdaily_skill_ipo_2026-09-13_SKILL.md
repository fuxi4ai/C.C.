---
name: refresh-risk-daily
description: 每日刷新「风险日报」artifact（FedWatch 会前槽自动取数 → fetch TACO 外部分项·禁代理 → IPO 覆盖续期 → build_risk_daily.py → update_artifact；挂载盘 SQLite 一律走 /tmp 副本回写）
---

每日刷新「风险日报」artifact。自包含步骤：

0. （FedWatch 会前槽自动取数）用 WebSearch 查最新 CME FedWatch 读数——中文一轮（如「CME 美联储观察 加息25个基点概率 维持利率不变概率」+ 当月会议月份词），英文一轮（如「CME FedWatch FOMC rate hike probability」+ 当月会议时间词）；必要时 WebFetch 打开 1-2 个源原文核实（金十 flash / 格隆汇 / 证券之星 / Investing / Nasdaq 等财经媒体转述的 CME 官方读数）。规则：
   - **双源对拍**：≥2 个独立源读数一致（对应档位差 ≤5pp）才写；仅 1 个源或源间冲突 → 不写，输出一行「FedWatch fetch skipped: 原因」。
   - **新鲜度护栏**：最新读数的 as_of 若不新于槽内 as_of（周末/节假日无新读数属常见），跳过不写，输出「FedWatch skip: 无更新（槽内 as_of 已最新）」。
   - **写盘**：先读 `~/Documents/Claude/Projects/风险日报/fomc_market_exp.json` 现状；只更新 `p_hike` / `p_hold` / `p_cut` / `as_of` / `source` 五个字段；`note` 的**人类叙事段保留不动**，仅在尾部追加一行「🤖 自动取数 YYYY-MM-DD: hold X% / hike Y% / cut Z% · 源A/源B」；机器行只增不删、保留最近 5 行、超出截断最旧机器行。`meeting` / `outcome` / `outcome_note` / `_usage` 一律不碰。
   - 三档数字必须合计 ≈100；**绝不编数**。source 注明「自动取数·多源转述」口径。
   - 写盘后回读 JSON：可解析、三档合计 100、as_of 已前进，才算完成。

1. （TACO 代理·尽力而为）在沙箱跑 TACO 外部分项取数：`python3 ~/Documents/Claude/Projects/风险日报/scripts/fetch_taco_components.py --fetch`（拉 FRED 房贷 MORTGAGE30US / 汽油 DGASUSGULF·GASREGW / 通胀 EXPINF1YR·T10YIE + VoteHub 特朗普净支持率 → 落 data/taco_components.db，供下一步 build 算 TACO 原子的 6 分项代理 pain）。**不要加 HTTPS_PROXY / HTTP_PROXY=http://localhost:3128**——2026-07-31 实测该端口无人监听，带上必 Connection refused；api.stlouisfed.org 与 api.votehub.com 在沙箱内直连可达。**取不到/超时/报错就记一行「TACO fetch skipped: 原因」并跳过**，绝不阻塞后续构建、绝不编数；build 会自动用已有数据算 N/6 代理并诚实标注分项数。

1.5 （IPO 覆盖续期·2026-09-13 起 · ERR-20260911-002 生产闭环 · Doctor 裁「挂 refresh-risk-daily」）在 build 之前续 IPO 采集覆盖证明，使当日生成的 IPO 卡可评（否则覆盖证明停在上一采集日 → 卡面 fail-closed 显示「◌不可判」）。步骤：
   1) token：`mkdir -p ~/.tushare && grep '^TUSHARE_TOKEN=' ~/Documents/Database/.env | cut -d= -f2- | tr -d '"' | tr -d "'" | tr -d '\n' > ~/.tushare/token`
   2) 整库副本：`mkdir -p /tmp/iporoot/Market-Data && cp <market_data.db 挂载点> /tmp/iporoot/Market-Data/market_data.db`（挂载盘 SQLite 铁律——写只在副本上做）。
   3) 起点：只读查 live 库 `SELECT MAX(scan_end) FROM ipo_coverage`——有值则 `--from <该日次日的 YYYYMMDD>`；无覆盖表则 `--from 20240101`（一次性全量回填）。
   4) 采集：`cd ~/Documents/Claude/Projects/Financial/烛照九阴 && ZZJY_DATABASE_ROOT=/tmp/iporoot python3 scripts/fetch_ipo.py --from <起点>`（fetch_ipo 的 config.MARKET_DB 随 ZZJY_DATABASE_ROOT 指向副本根；脚本会写 ipo_daily 增量 + ipo_coverage 覆盖证明含 events_hash）。
   5) 放回（与 zhuzhao 班同纪律·时间错开无并发）：备份 live `cp <live> <live>.bak_riskipo_YYYYMMDD`（若当日已有同款备份则跳过）→ `cp /tmp/iporoot/Market-Data/market_data.db <live>`（truncate 写允许）→ 只读打开 live 跑 `PRAGMA integrity_check` 必须 ok。
   6) 失败处理：取不到/token 缺/网络失败 → 记一行「IPO fetch skipped: 原因」并跳过，**绝不编数、绝不回退已有覆盖**；build 会按现有覆盖证明如实显示可评/不可判。
   - **时序注**：zhuzhao 班 10:03 PT 与本报 09:08 PT 各自「先拷 live 起步 → 写各自表 → 放回」，时刻错开，放回互不丢数；若某日发现两班时间重叠迹象（如 live 上刚有他人写入），先报告 Doctor 不硬放回。

2. 运行后端构建脚本：在沙箱跑 `python3 ~/Documents/Claude/Projects/风险日报/build_risk_daily.py`（它读 market_data.db / recap.db / PEC predictions-register / AI Tech Alarm 底层信号 / taco_components.db 等一手数据，重算风险原子（含 TACO）的温度/震动烈度，派生风险分子预警，生成 `dashboard/risk-daily.html` + `data/risk_snapshot.json`）。若脚本报错或某原子缺数据，如实贴出错误，**不要用旧数据蒙混、不要编造温度**。

3. 更新 artifact：调用 `mcp__cowork__update_artifact`，id='risk-daily'，html_path='/Users/lunarabbit/Documents/Claude/Projects/风险日报/dashboard/risk-daily.html'，update_summary 写「当日综合风险温度 {值} {带} · {日期}」。

4. 纪律：
   - 数据真实性铁律（温度全部来自脚本读的真实一手值，无估算冒充）；risk_overlay_not_alpha——只出风险读数，**不出任何交易/仓位/方向建议**。
   - **挂载盘 SQLite 铁律（2026-07-31 事故后立）**：`~/Documents` 是 FUSE 挂载，**不支持 unlink**（实测 EPERM）。SQLite 回滚日志的原子提交点正是删除 `-journal`，所以在挂载盘上直接开 rw 连接（`sqlite3.connect(path)` 不带 `mode=ro`）必然 `disk I/O error`，并留下 hot journal，反复累积即 `database disk image is malformed`（07-27/28/29 连续三天损坏的根因）。
     → 任何写库一律「拷到 /tmp 本地副本 → 在副本上 rw → 自检 integrity ok → 整库覆写回挂载」（truncate 写允许，rename/unlink 不允许）。fetch_taco_components.py 已按此改造（`_stage()` / `_commit_back()`）。纯 `mode=ro` 读挂载盘是安全的，无需改。
   - 若发现 `data/` 下残留 `*-journal` 文件，说明有人绕过了上一条：**报告给 Doctor，不要自行删**（沙箱也删不掉），并在当日输出里标明。
   - 卡面分项标注必须与实际参与数对账：`source` 里的「N/6分项参与」要等于 `taco_pain_from` 的复刻 N，被陈旧护栏剔除的分项须在「本次未参与」里点名。**禁止让缺席分项在花名册里冒充在场。**

跑完更新即可，无需额外分析或消息。
