---
name: refresh-risk-daily
description: 每日刷新「风险日报」artifact（fetch TACO 外部分项·禁代理 → build_risk_daily.py → update_artifact；挂载盘 SQLite 一律走 /tmp 副本回写）
---

每日刷新「风险日报」artifact。自包含步骤：

1. （TACO 代理·尽力而为）在沙箱跑 TACO 外部分项取数：`python3 ~/Documents/Claude/Projects/风险日报/scripts/fetch_taco_components.py --fetch`（拉 FRED 房贷 MORTGAGE30US / 汽油 DGASUSGULF·GASREGW / 通胀 EXPINF1YR·T10YIE + VoteHub 特朗普净支持率 → 落 data/taco_components.db，供下一步 build 算 TACO 原子的 6 分项代理 pain）。**不要加 HTTPS_PROXY / HTTP_PROXY=http://localhost:3128**——2026-07-31 实测该端口无人监听，带上必 Connection refused；api.stlouisfed.org 与 api.votehub.com 在沙箱内直连可达。**取不到/超时/报错就记一行「TACO fetch skipped: 原因」并跳过**，绝不阻塞后续构建、绝不编数；build 会自动用已有数据算 N/6 代理并诚实标注分项数。

2. 运行后端构建脚本：在沙箱跑 `python3 ~/Documents/Claude/Projects/风险日报/build_risk_daily.py`（它读 market_data.db / recap.db / PEC predictions-register / AI Tech Alarm 底层信号 / taco_components.db 等一手数据，重算风险原子（含 TACO）的温度/震动烈度，派生风险分子预警，生成 `dashboard/risk-daily.html` + `data/risk_snapshot.json`）。若脚本报错或某原子缺数据，如实贴出错误，**不要用旧数据蒙混、不要编造温度**。

3. 更新 artifact：调用 `mcp__cowork__update_artifact`，id='risk-daily'，html_path='/Users/lunarabbit/Documents/Claude/Projects/风险日报/dashboard/risk-daily.html'，update_summary 写「当日综合风险温度 {值} {带} · {日期}」。

4. 纪律：
   - 数据真实性铁律（温度全部来自脚本读的真实一手值，无估算冒充）；risk_overlay_not_alpha——只出风险读数，**不出任何交易/仓位/方向建议**。
   - **挂载盘 SQLite 铁律（2026-07-31 事故后立）**：`~/Documents` 是 FUSE 挂载，**不支持 unlink**（实测 EPERM）。SQLite 回滚日志的原子提交点正是删除 `-journal`，所以在挂载盘上直接开 rw 连接（`sqlite3.connect(path)` 不带 `mode=ro`）必然 `disk I/O error`，并留下 hot journal，反复累积即 `database disk image is malformed`（07-27/28/29 连续三天损坏的根因）。
     → 任何写库一律「拷到 /tmp 本地副本 → 在副本上 rw → 自检 integrity ok → 整库覆写回挂载」（truncate 写允许，rename/unlink 不允许）。fetch_taco_components.py 已按此改造（`_stage()` / `_commit_back()`）。纯 `mode=ro` 读挂载盘是安全的，无需改。
   - 若发现 `data/` 下残留 `*-journal` 文件，说明有人绕过了上一条：**报告给 Doctor，不要自行删**（沙箱也删不掉），并在当日输出里标明。
   - 卡面分项标注必须与实际参与数对账：`source` 里的「N/6分项参与」要等于 `taco_pain_from` 的复刻 N，被陈旧护栏剔除的分项须在「本次未参与」里点名。**禁止让缺席分项在花名册里冒充在场。**

跑完更新即可，无需额外分析或消息。