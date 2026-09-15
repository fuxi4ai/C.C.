# 定时任务 · 四执行面现状快照

> 由 `brain/.tools/scheduler_snapshot.py` 生成于 2026-09-14T04:49:07-07:00（triggered_by=scheduled），**只读**。

> **本文件纳入 git；跑完 `git diff` 即知自上次快照以来什么变了** —— 无论改动来自 Doctor、别的会话还是 CC 自己。

> 镜像步：镜像已同步：30 文件（更新 0 · 移除 0） · Artifacts：10 个（拷 0 · 清单全量）


## 面① Cowork live 树（24 个）

| taskId | SKILL mtime | 行数 | sha | 描述 |
|---|---|---|---|---|
| `agents-memory-meditation` | 2026-08-11 09:01 | 17 | `dbc6ca59c8b6` | 每周由句芒对 brain/agents 做数灵记忆体检（meditation 兜底），查人格冲突/记忆错位/漏记断链/归位合规，出报告 |
| `baize-breakout-sentinel` | 2026-08-12 18:56 | 32 | `dca78b053024` | 白泽每日哨兵：突破扫描 + 观察窗信号A/B/C2全生命周期（预注册规则自动记账） |
| `baize-weekly-report` | 2026-09-11 07:05 | 118 | `ceb38eb5b8ad` | 白泽大宗周报：渊图先验+web补价+Top20双面交叉验证+龙鱼六维(实时读龙鱼库·领域分库)→出MD周报与O MY HTML看板（周更） |
| `brain-monthly-checkup` | 2026-08-11 09:01 | 41 | `f5b2a3680c56` | 每月初跑 meditation 心灵与记忆健康自检：折叠上月 logs + 记忆指标 + 数灵人格层 + 警告 |
| `cockpit-snapshot` | 2026-08-12 18:59 | 18 | `6c33680aedea` | 影子驾驶舱夜间快照:三时钟状态落 cockpit.db(append-only)+ OOS 台账成熟(次一自然日) |
| `eal-starfield-rebuild` | 2026-09-13 19:29 | 14 | `10c2e219deb3` | EAL·SOX 事件星空快照日更重建（risk-daily 第三标签源）：行情守卫→沙箱标准链 build→对表验证；防快照冻结致「星星在、流线空」（2026-09-13 根因） |
| `event-attribution-watch` | 2026-09-07 07:51 | 6 | `83363c6f631f` | EAL v3 数据链日更班：行情更新→sealed 快照→manifest-gated exact registry→冻结 XNYS 日历→DAILY_SHADOW→fresh candidate→事后归因 loop→a… |
| `guanxing-fed-daily` | 2026-08-14 08:34 | 44 | `04ac1fa71745` | 白泽观星 Fed 腿日更：每日跑 fetch_fed_inputs_fred.py --predict 取最新 FRED 读数并出会前读数快照（fed_inputs + fed_prediction 落盘），新鲜度守卫+… |
| `longyu-equity-thesis-weekly` | 2026-09-11 05:53 | 29 | `3fc4f3607996` | 每周六 14:00 PT 用 equity-thesis 技能对龙鱼持仓标的逐个做个股定性研究并落盘 equity-thesis/，22:00 双 scorer 周更班重建看板时自动带出 |
| `longyu-weekly-dualscorer` | 2026-08-24 20:09 | 50 | `bd7c9385ff0f` | 龙鱼标的库周更：常更标的每周双scorer打分(deepseek子项+claude top-down)落库+对比校正队列+刷新个股库看板artifact |
| `market-data-daily-update` | 2026-08-12 18:56 | 63 | `1897e9d46465` | 每交易日由句芒增量更新Market-Data行情到最近已收盘交易日=当日(收盘后第一时间;须在上游Tushare当日入库完成之后);去重+防空壳,取空则次日按缺口自动补回;下游白泽哨兵/次日晨报读到当日收盘;沙箱经代理+… |
| `r7-threshold-recal` | 2026-09-07 08:16 | 17 | `b5f804200b2b` | 一次性：r7 USDJPY 急动阈值 v0 复校（首个实战🔴或两个月后之约） |
| `recap-kejian-daily-ingest` | 2026-08-19 21:17 | 39 | `c8e77b367088` | 由九儿扫小鲍课件→四维入recap.db：dim1/dim2全自动、dim3情绪叙述纳入、dim4仓位半纳入(拿不准留待人工复核)，严格去重标P2；三道闸门：repr只收0-1数值·分项口径不落总仓列·dim2近似数必注… |
| `recap-kejian-review` | 2026-08-18 20:43 | 58 | `a7b27cef563b` | 每天09:30由句芒审核九儿课件入库：去重/数据合理性/P2标签/归位，扩审dim3(禁行情倒灌)与dim4仓位(归一/词表/待复核不重不漏)；全量自动修（两档机制·护栏：备份+证据+不自标✅）+次日复发扫描，出审核日志 |
| `refresh-asset-dashboard` | 2026-09-13 00:31 | 58 | `2e5dedf48bbe` | 重扫并刷新海螺姑娘全局资产看板（survey→重建HTML→update_artifact→conch清空盘点），日更；挂载 Projects+Database+brain+4AI 四目录，覆盖 14/15 projec… |
| `refresh-risk-daily` | 2026-09-12 22:59 | 28 | `08daf3e059b6` | 每日刷新「风险日报」artifact（FedWatch 会前槽自动取数 → fetch TACO 外部分项·禁代理 → build_risk_daily.py → update_artifact；挂载盘 SQLite 一… |
| `repair-finance-chain` | 2026-08-10 21:16 | 33 | `97b9b07f274a` | 看板星图「审查并修复」按钮触发：诊断金融数据链路断链节点→只跑已知安全幂等修复→破坏性/网络/git 改动只给 Doctor 命令不自动跑 |
| `scheduler-weekly-audit` | 2026-09-01 00:23 | 98 | `77b0be1a427c` | 定时任务四执行面周巡检（只读）：跑 scheduler_snapshot.py + S3 快照写后自证 + audit 未验行附报；exit 0 且自证前进且 audit 无 🔄 才完全静默不打扰；异常才把 🔴 清单报给… |
| `touzhijunjun-perspective-refresh` | 2026-08-11 09:01 | 63 | `11d11fbca3dc` | 投知君君视角层增量提炼+反共识纠偏+图谱候选核实（自检增量·不自动promote），周两更 |
| `us-close-backfill` | 2026-08-12 21:34 | 136 | `cce5b8eded4c` | 美股收盘补数班的只读看门狗——写库已迁本机 launchd(com.zhuzhao.usclose 14:00 PT)，本班 14:30 只核对两表水位与新鲜度并出简报，绝不写库(G019)；异常只给 Doctor 终端… |
| `xboard-daily-repush` | 2026-08-22 06:57 | 55 | `5581f03c32da` | X 看板每日自动重推——18:00 PT 先增量提取抖音要点（extract_points.py --new-only·存量不补）再跑生成器并推 Cowork artifact x-board（2026-08-22 Do… |
| `yuantu-alarm-earnings-season` | 2026-08-10 21:15 | 16 | `e8bcb5aedf35` | 渊图警报监控·财报季加密（1/4/7/10月周四）核验折旧脚注/FCF/capex |
| `yuantu-alarm-weekly` | 2026-08-10 21:15 | 16 | `8cc9ea07b8ba` | 渊图警报监控·常态每周核验 AI 科技股未定价危险时点 |
| `zhuzhao-market-fetch-daily-report` | 2026-08-27 02:12 | 98 | `a070c81fc8fc` | 每交易日由九儿增量拉烛照九阴四表行情(theme_etf/us_anchor/market_amount/limit_list，A股三表走tushare、美股锚走yahoo chart API默认源·盘中守卫+null … |

⚠ cron 列缺失：见 `_gaps`。

## 面② Documents 死树

✅ ✅ 不存在

## 面③ launchd（源 3 · 装机 8）

| Label | 排期 | 已加载 | last exit | 装机 mtime |
|---|---|---|---|---|
| `com.fuxi4ai.audit-harness.dispatch` | — | True | 0 | 2026-09-12 02:18 |
| `com.google.GoogleUpdater.wake` | — | False | — | 2026-07-01 09:22 |
| `com.google.keystone.agent` | — | False | — | 2026-07-01 09:22 |
| `com.google.keystone.xpcservice` | — | False | — | 2026-07-01 09:22 |
| `com.zhuzhao.ipo-rolling` | {"Hour": 9, "Minute": 0} | True | 0 | 2026-09-12 23:40 |
| `com.zhuzhao.marketdata` | [{"Weekday": 1, "Hour": 2, "Minute": 30}, {"Weekday": 2, "Hour": 2, "Minute": 30}, {"Weekday": 3, "Hour": 2, "Minute": 30}, {"Weekday": 4, "Hour": 2, "Minute": 30}, {"Weekday": 5, "Hour": 2, "Minute": 30}] | True | 0 | 2026-07-22 22:12 |
| `com.zhuzhao.usclose` | [{"Weekday": 1, "Hour": 14, "Minute": 0}, {"Weekday": 2, "Hour": 14, "Minute": 0}, {"Weekday": 3, "Hour": 14, "Minute": 0}, {"Weekday": 4, "Hour": 14, "Minute": 0}, {"Weekday": 5, "Hour": 14, "Minute": 0}] | True | 0 | 2026-08-12 21:21 |
| `netdisk_service` | — | False | — | 2025-03-15 02:42 |

✅ 源与装机全部一致

## 面④ crontab

⚠ 非空——第四执行面已启用
- `SHELL=/bin/zsh`
- `TZ=America/Los_Angeles`
- `30 18 * * 0-4 /usr/bin/env bash "/Users/lunarabbit/Documents/Codex/After Work/scripts/run-morning-post-cycle.sh" primary >> "/Users/lunarabbit/Documents/Codex/After Work/work/ops/morning-post-scheduler.log" 2>&1`
- `30 20 * * 0-4 /usr/bin/env bash "/Users/lunarabbit/Documents/Codex/After Work/scripts/run-morning-post-cycle.sh" recovery >> "/Users/lunarabbit/Documents/Codex/After Work/work/ops/morning-post-scheduler.log" 2>&1`

## 面⑤ 挂载检查（2026-08-13 看门狗挂载治理）

⚠ **缺挂载 5 个**：Database、烛照九阴、剑酒青丘、白泽大宗、brain——定时班跑前需补挂，否则阻塞/静默失败
