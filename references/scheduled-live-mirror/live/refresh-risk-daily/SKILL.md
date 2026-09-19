---
name: refresh-risk-daily
description: 每日刷新「风险日报」artifact（FedWatch 会前槽自动取数 → fetch TACO 外部分项·禁代理 → 星空快照新鲜度探针 → build_risk_daily.py → update_artifact；挂载盘 SQLite 一律走 /tmp 副本回写）
---

每日刷新「风险日报」artifact。自包含步骤：

0. （FedWatch 会前槽自动取数）用 WebSearch 查最新 CME FedWatch 读数——中文一轮（如「CME 美联储观察 加息25个基点概率 维持利率不变概率」+ 当月会议月份词），英文一轮（如「CME FedWatch FOMC rate hike probability」+ 当月会议时间词）；必要时 WebFetch 打开 1-2 个源原文核实（金十 flash / 格隆汇 / 证券之星 / Investing / Nasdaq 等财经媒体转述的 CME 官方读数）。规则：
   - **双源对拍**：≥2 个独立源读数一致（对应档位差 ≤5pp）才写；仅 1 个源或源间冲突 → 不写，输出一行「FedWatch fetch skipped: 原因」。
   - **新鲜度护栏**：最新读数的 as_of 若不新于槽内 as_of（周末/节假日无新读数属常见），跳过不写，输出「FedWatch skip: 无更新（槽内 as_of 已最新）」。
   - **写盘**：先读 `~/Documents/Claude/Projects/风险日报/fomc_market_exp.json` 现状；只更新 `p_hike` / `p_hold` / `p_cut` / `as_of` / `source` 五个字段；`note` 的**人类叙事段保留不动**，仅在尾部追加一行「🤖 自动取数 YYYY-MM-DD: hold X% / hike Y% / cut Z% · 源A/源B」；机器行只增不删、保留最近 5 行、超出截断最旧机器行。`meeting` / `outcome` / `outcome_note` / `_usage` 一律不碰。
   - 三档数字必须合计 ≈100；**绝不编数**。source 注明「自动取数·多源转述」口径。
   - 写盘后回读 JSON：可解析、三档合计 100、as_of 已前进，才算完成。

1. （TACO 代理·尽力而为）在沙箱跑 TACO 外部分项取数：`python3 ~/Documents/Claude/Projects/风险日报/scripts/fetch_taco_components.py --fetch`（拉 FRED 房贷 MORTGAGE30US / 汽油 DGASUSGULF·GASREGW / 通胀 EXPINF1YR·T10YIE + VoteHub 特朗普净支持率 → 落 data/taco_components.db，供下一步 build 算 TACO 原子的 6 分项代理 pain）。**不要加 HTTPS_PROXY / HTTP_PROXY=http://localhost:3128**——2026-07-31 实测该端口无人监听，带上必 Connection refused；api.stlouisfed.org 与 api.votehub.com 在沙箱内直连可达。**取不到/超时/报错就记一行「TACO fetch skipped: 原因」并跳过**，绝不阻塞后续构建、绝不编数；build 会自动用已有数据算 N/6 代理并诚实标注分项数。

1.5. （星空快照新鲜度探针 · 2026-09-16 Doctor 批装 · 2026-09-17 双路径修复+复核门禁 · GOTCHAS ERR-20260916-001）在沙箱跑 `python3 ~/Documents/Claude/Projects/风险日报/ops/check_starfield_freshness.py`——读 EAL_STARFIELD.html 内嵌快照的 market_as_of，与 XNYS 冻结日历的「最近已收盘交易日」比对，落后 >1 个交易日即告警（检测滞后从周巡检 7 天缩到 1 天）。探针已修双路径（Mac 原生 HOME/Documents 优先 + 沙箱 /sessions/*/mnt/Documents glob 兜底·多残留取最新，同 r7_yen_watch.py 款），正常时沙箱输出即真值。输出 `STARFIELD_FRESH=OK …` 才无事；`STALE` / `MISSING` / `UNPARSEABLE` / `NO_CALENDAR` / `UNKNOWN` 任一 → **先复核再报**：先用 Glob/Read 文件工具实核 Mac 侧路径 `~/Documents/Claude/Projects/Financial/宏观研究体系/EAL/backtest/EAL_STARFIELD.html`（独立于沙箱挂载通道）——文件实存而探针异常，则系挂载/通道问题，记「探针异常·复核实况 OK」不红字（2026-09-16/17 两次 MISSING 均为此类伪报）；确认真异常（文件实缺/STALE/UNPARSEABLE 等）才在当日简报首行红字「⚠️ EAL 星空快照异常：{探针输出原文}」报 Doctor。**本检查非阻断**（恒 exit 0）——星空快照停更不等同风险数据停更，日报本体继续构建，绝不因探针结果跳过后续步骤。

2. 运行后端构建脚本：在沙箱跑 `python3 ~/Documents/Claude/Projects/风险日报/build_risk_daily.py`（它读 market_data.db / recap.db / PEC predictions-register / AI Tech Alarm 底层信号 / taco_components.db 等一手数据，重算风险原子（含 TACO）的温度/震动烈度，派生风险分子预警，生成 `dashboard/risk-daily.html` + `data/risk_snapshot.json`）。若脚本报错或某原子缺数据，如实贴出错误，**不要用旧数据蒙混、不要编造温度**。

3. 更新 artifact：调用 `mcp__cowork__update_artifact`，id='risk-daily'，html_path='/Users/lunarabbit/Documents/Claude/Projects/风险日报/dashboard/risk-daily.html'，update_summary 写「当日综合风险温度 {值} {带} · {日期}」。

4. 纪律：
   - 数据真实性铁律（温度全部来自脚本读的真实一手值，无估算冒充）；risk_overlay_not_alpha——只出风险读数，**不出任何交易/仓位/方向建议**。
   - **挂载盘 SQLite 铁律（2026-07-31 事故后立）**：`~/Documents` 是 FUSE 挂载，**不支持 unlink**（实测 EPERM）。SQLite 回滚日志的原子提交点正是删除 `-journal`，所以在挂载盘上直接开 rw 连接（`sqlite3.connect(path)` 不带 `mode=ro`）必然 `disk I/O error`，并留下 hot journal，反复累积即 `database disk image is malformed`（07-27/28/29 连续三天损坏的根因）。
     → 任何写库一律「拷到 /tmp 本地副本 → 在副本上 rw → 自检 integrity ok → 整库覆写回挂载」（truncate 写允许，rename/unlink 不允许）。fetch_taco_components.py 已按此改造（`_stage()` / `_commit_back()`）。纯 `mode=ro` 读挂载盘是安全的，无需改。
   - 若发现 `data/` 下残留 `*-journal` 文件，说明有人绕过了上一条：**报告给 Doctor，不要自行删**（沙箱也删不掉），并在当日输出里标明。
   - 卡面分项标注必须与实际参与数对账：`source` 里的「N/6分项参与」要等于 `taco_pain_from` 的复刻 N，被陈旧护栏剔除的分项须在「本次未参与」里点名。**禁止让缺席分项在花名册里冒充在场。**

跑完更新即可，无需额外分析或消息。