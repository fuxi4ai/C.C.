# 定时任务 · 四执行面现状快照

> 由 `brain/.tools/scheduler_snapshot.py` 生成于 2026-08-02T10:43:57-07:00，**只读**。

> **本文件纳入 git；跑完 `git diff` 即知自上次快照以来什么变了** —— 无论改动来自 Doctor、别的会话还是 CC 自己。

> 镜像步：镜像已同步：31 文件（更新 0 · 移除 0） · Artifacts：9 个（拷 0 · 清单全量）


## 面① Cowork live 树（19 个）

| taskId | SKILL mtime | 行数 | sha | 描述 |
|---|---|---|---|---|
| `agents-memory-meditation` | 2026-07-05 10:46 | 17 | `448e281ca97b` | 每周日 09:05 由句芒对 brain/agents 做数灵记忆体检（meditation 兜底），查人格冲突/记忆错位/漏记断链/归位合规，出报告 |
| `baize-breakout-sentinel` | 2026-07-09 03:50 | 32 | `e5b1f2139180` | 白泽每日哨兵：突破扫描 + 观察窗信号A/B/C2全生命周期（预注册规则自动记账） |
| `baize-weekly-report` | 2026-07-31 23:56 | 114 | `756ff01971b0` | 白泽大宗周报：渊图先验+web补价+Top20双面交叉验证+龙鱼六维(实时读龙鱼库·领域分库)→出MD周报与O MY HTML看板（周日01:00，留足本地cron缓冲） |
| `brain-monthly-checkup` | 2026-07-05 10:46 | 41 | `b484f5d271d7` | 每月 1 号 09:00 跑 meditation 心灵与记忆健康自检：折叠上月 logs + 记忆指标 + 数灵人格层 + 警告 |
| `cockpit-snapshot` | 2026-07-30 06:03 | 18 | `6c33680aedea` | 影子驾驶舱夜间快照:三时钟状态落 cockpit.db(append-only)+ OOS 台账成熟(次一自然日) |
| `event-attribution-watch` | 2026-07-30 01:14 | 34 | `2ddfd4f56421` | 事件归因验证班：采集上一美股交易日数据→事件日判定→收盘级归因→与注册量级带对准→提案制汇报（剑酒青丘·解释层） |
| `longyu-weekly-dualscorer` | 2026-08-01 22:28 | 43 | `840a7a7c574f` | 龙鱼标的库周更：常更标的每周双scorer打分(deepseek子项+claude top-down)落库+对比校正队列+刷新个股库看板artifact |
| `market-data-daily-update` | 2026-08-01 06:34 | 62 | `b98e2afdacf9` | 每交易日由句芒增量更新Market-Data行情到最近已收盘交易日=当日(收盘后第一时间;须在上游Tushare当日入库完成之后);去重+防空壳,取空则次日按缺口自动补回;下游白泽哨兵/次日晨报读到当日收盘;沙箱经代理+… |
| `recap-kejian-daily-ingest` | 2026-07-30 06:02 | 30 | `4da3a77db942` | 由九儿扫小鲍课件→四维入recap.db：dim1/dim2全自动、dim3情绪叙述纳入、dim4仓位半纳入(拿不准留待人工复核)，严格去重标P2 |
| `recap-kejian-review` | 2026-07-31 23:56 | 33 | `60d437adc0d4` | 每天09:30由句芒审核九儿课件入库：去重/数据合理性/P2标签/归位，扩审dim3(禁行情倒灌)与dim4仓位(归一/词表/待复核不重不漏)，出审核日志 |
| `refresh-asset-dashboard` | 2026-08-01 22:31 | 48 | `bf8a87844666` | 重扫并刷新海螺姑娘全局资产看板（survey→重建HTML→update_artifact），日更；挂载已收敛为 Projects+Database 两目录，覆盖 13/14 project |
| `refresh-risk-daily` | 2026-07-31 10:03 | 21 | `2baa154d130d` | 每日刷新「风险日报」artifact（fetch TACO 外部分项·禁代理 → build_risk_daily.py → update_artifact；挂载盘 SQLite 一律走 /tmp 副本回写） |
| `repair-finance-chain` | 2026-07-05 10:46 | 33 | `97b9b07f274a` | 看板星图「审查并修复」按钮触发：诊断金融数据链路断链节点→只跑已知安全幂等修复→破坏性/网络/git 改动只给 Doctor 命令不自动跑 |
| `scheduler-weekly-audit` | 2026-08-02 01:21 | 64 | `33e8c3ead816` | 定时任务四执行面周巡检（只读）：跑 scheduler_snapshot.py，exit 0 则完全静默不打扰；exit 1 才把 🔴 异常清单报给 Doctor。绝不自动修、不 commit、不碰调度器 |
| `touzhijunjun-perspective-refresh` | 2026-08-01 22:28 | 63 | `139923b77c15` | 投知君君视角层增量提炼+反共识纠偏+图谱候选核实（自检增量·不自动promote），周三/周六17:00 |
| `us-close-backfill` | 2026-08-01 09:12 | 118 | `aae001d8f84e` | 美股收盘补数班的只读看门狗——写库已迁本机 launchd(com.zhuzhao.usclose 14:00 PT)，本班 14:30 只核对两表水位与新鲜度并出简报，绝不写库(G019)；异常只给 Doctor 终端… |
| `yuantu-alarm-earnings-season` | 2026-08-02 00:20 | 16 | `e8bcb5aedf35` | 渊图警报监控·财报季加密（1/4/7/10月周四）核验折旧脚注/FCF/capex |
| `yuantu-alarm-weekly` | 2026-07-22 23:52 | 16 | `2a486321e9fe` | 渊图警报监控·常态每周核验 AI 科技股未定价危险时点 |
| `zhuzhao-market-fetch-daily-report` | 2026-08-02 00:59 | 92 | `ff0f5e557188` | 每交易日由九儿增量拉烛照九阴四表行情(theme_etf/us_anchor/market_amount/limit_list，A股三表走tushare、美股锚走yahoo chart API默认源·盘中守卫+null … |

⚠ cron 列缺失：见 `_gaps`。

## 面② Documents 死树

✅ ✅ 已归档（改名不删）

## 面③ launchd（源 2 · 装机 6）

| Label | 排期 | 已加载 | last exit | 装机 mtime |
|---|---|---|---|---|
| `com.google.GoogleUpdater.wake` | — | True | 0 | 2026-07-01 09:22 |
| `com.google.keystone.agent` | — | False | — | 2026-07-01 09:22 |
| `com.google.keystone.xpcservice` | — | False | — | 2026-07-01 09:22 |
| `com.zhuzhao.marketdata` | [{"Weekday": 1, "Hour": 2, "Minute": 30}, {"Weekday": 2, "Hour": 2, "Minute": 30}, {"Weekday": 3, "Hour": 2, "Minute": 30}, {"Weekday": 4, "Hour": 2, "Minute": 30}, {"Weekday": 5, "Hour": 2, "Minute": 30}] | True | 0 | 2026-07-22 22:12 |
| `com.zhuzhao.usclose` | [{"Weekday": 1, "Hour": 14, "Minute": 0}, {"Weekday": 2, "Hour": 14, "Minute": 0}, {"Weekday": 3, "Hour": 14, "Minute": 0}, {"Weekday": 4, "Hour": 14, "Minute": 0}, {"Weekday": 5, "Hour": 14, "Minute": 0}] | True | 0 | 2026-08-01 09:01 |
| `netdisk_service` | — | True | (never | 2025-03-15 02:42 |

✅ 源与装机全部一致

## 面④ crontab

为空 ✅
