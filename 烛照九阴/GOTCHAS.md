---
title: 烛照九阴 · GOTCHAS（已知坑）
tags: [烛照九阴, gotchas]
created: 2026-07-19
updated: 2026-08-26
status: active
type: resource
project: 烛照九阴
---

# 烛照九阴 · GOTCHAS（已知坑）

> 排查超过一轮的问题都该记录在这里。CC 遇到报错并解决后**立即**回写，无需 Doctor 提示。
> 本文件 2026-07-19 补建——此前 烛照九阴 缺 GOTCHAS.md（REQ-F2 标了 [x] 但漏了本项目）。

## 格式

```
## [ERR-YYYYMMDD-NNN] 简要描述
**状态**: 🔄 待修复/已修待验 / ⚠️ 已知风险；✅ 已修复（**仅由 Doctor 或指定独立验收方落，实施者不得自标**）（⏳ 旧状态词 2026-08-26 迁移专场退役）
**现象** / **根因** / **判别信号** / **正确做法** / **来源**
```

---

## [ERR-20260722-002] 生成器「已部署到 Cowork artifact」日志误导——写的是非规范本地镜像，非 live 真身

**状态**: ✅ 已解决（根因坐实 + 生成器误导文案已正名 2026-07-22；ARTIFACT_ROOT 是否统一为可选优化、非缺陷，暂不动）

**现象**：手动跑 `gen_daily_report.py`（正式模式）日志打「🚀 已部署到 Cowork artifact → ~/Documents/Claude/Artifacts/...」，看着像 live 卡片更新了，但 Cowork 卡片其实没变——非手工 `update_artifact` 不动。

**根因坐实**（2026-07-22，`readlink` 确认**非软链**）：
- `config.ARTIFACT_ROOT = <Documents>/Claude/Artifacts`（`config.py:52`，`PROJECT_ROOT.parents[3]`）——生成器 `_deploy_to_artifact` 写这里。
- Cowork **真身**按 `list_artifacts` 的 `path` 落在 `~/Claude's workspace/Artifacts/{id}/index.html`（本环境 Cowork 工作区，另一物理目录；疑自 06-30 gateway 切换后与 Documents 镜像脱钩，参 [[artifact存储机制]]）。
- 两者不同源 → 生成器的文件写只更新**非规范镜像**，Cowork 不读它。

**关键澄清（勿再误判）**：**live 卡片并非不更新**——定时链 SKILL（`Scheduled/zhuzhao-market-fetch-daily-report` step 6.5）每天独立做 §6.5 兼容转换后调 `update_artifact` 推真身，日更正常。缺陷只在**生成器自身的文案**：`_deploy_to_artifact` 的 `🚀 已部署到 Cowork artifact` 日志 + `无需手工 update_artifact` 注释（gen_daily_report.py ~line1405）给手动运行者**假信心**。

**判别信号**：改了报告、生成器打「已部署」，但 Cowork 卡片不变；手工 `update_artifact` 后才变。

**正确做法**：更新 live 卡片**只认 `update_artifact`**（daily 走 step 6.5；手动改后须自己补一发 `update_artifact`，html 取生成器写出的自包含 index.html）。**已改（2026-07-22 · Doctor 批）**：生成器 `_deploy_to_artifact` docstring/日志/meta 描述 + line44 注释已正名——日志由「🚀 已部署到 Cowork artifact」改「🪞 已写本地 artifact 镜像（非 live·真身走 update_artifact）」、meta 改「定时链 step 6.5 经 update_artifact 推送」、docstring 明写此目录非 live 真身。逻辑零改、py_compile 过。**仍开放（可选优化·非缺陷）**：是否把 `ARTIFACT_ROOT` 指向真身或删镜像——直写 `~/Claude's workspace/Artifacts` 能否被 Cowork 认、manifest 刷不刷均未验，Doctor 定「暂不动」。

**来源** → logs/2026-07-22-成交额口径纠偏与条幅两行artifact推送.md · [[artifact存储机制]]

---

## [ERR-20260722-001] 日报把 market_amount_daily 成指代理当「两市/全市场成交额」显示——系统性低估约2成

**状态**: ✅ 已解决（2026-07-22 换源）

**现象**：Doctor 第一性原理核成交额，发现日报「两市总成交额」07-21 显 2.38万亿，与新闻全市场读数（~2.97万亿）差约 0.5–0.6万亿。

**根因**：`gen_daily_report.py` 取 `market_amount_daily.total_trillion`＝「沪成指+深成指」**指数成分股**加总代理（漏北交所+深市非成分股），却标签「两市总成交额」「全市场成交额」。逐日比全口径低约 **0.5–0.6万亿 / ~20%**，非常稳定。该代理还喂 `kcap()` 容量模型 → K_cap 长期偏紧、主线放行偏少（kcap 经验表 1/2/3万亿本是全口径心智，Doctor 2026-07-22 确认）。

**判别信号**：日报成交额比同日新闻全市场读数低约 0.5–0.6万亿（~2成）即中招；或对照 `daily_market.volume_trillion` 差一个恒定 gap。

**正确做法**：日报成交额统一取 `daily_market.volume_trillion`（全A含北交所）+ `WHERE volume_trillion>0`（挡 ERR-20260719-003 的历史 0-fill）；显示+K_cap 同源；标签「全市场成交额」名实相符；kcap 不重标（全口径心智）。历史长序列量能研究仍按 ERR-20260719-003 用 index_research.db。

**来源** → logs/2026-07-22-F4虹吸窗口20到10与ipo_date误标修正.md（同日 A 档换源）· 决策记录 2026-07-22 F4 条

---

## [ERR-20260719-003] daily_market.volume_trillion 历史全 0 非 NULL——名义覆盖 1584 日实际仅 32 日

**状态**: ✅ 已解决（2026-08-09 全量回补收口 · A2 双综指口径）

**收口（2026-08-09）**：旧段 1552 行（20200102→20260602）全量回补、0 值清零。口径 **A2 = 000001.SH + 399106.SZ 双综指**（tushare index_daily，千元→万亿）；对 20260603 起 B 本地加总口径（全A含北交所）实测缝差 -0.6~-0.8%（10/10 近期样本；残差即北交所量级——双综指不含、B 池含）。**daily_market.volume_trillion 自此 = 本地可回测的真全市场成交额长序列（2020+，旧段缺北交所 <1%）**；下文「连带」「正确做法」中与之冲突的旧指引以本收口为准。教训加一条：初版脚本（08-08）合成口径含 399001.SZ——本条早已警示其不可用于历史（2015-05 成分 40→500 扩容断点 + 成分股非全市场），起草时未读全条目、docstring「预计 <2%」亦未先实测；幸 dry-run 口径校验当场逮住（10/10 样本 -20~23%），换双综指重填覆盖。工具：`剑酒青丘/infrastructure/取数工具/refill_daily_market_volume_a2_20260809.py`（v1 已 _DEPRECATED_）；快照 `market_data.db.bak_20260808_volume` / `bak_20260809_volume_a2` 留档至 08-15 批次清理。**注意**：本条只解数据缺口；风险日报「成交额定源裁定（甲案）」的前提「volume_trillion 仅 2026-06 起」已破——甲案是否修订另案请 Doctor 裁。

**现象**：对该列做滚动 252 日分位，近期分位恒≈1.0——历史 0 垫底，任何近期值都是"史高"。

**根因**：`volume_trillion` 20260603 起才回填（与 stock_daily 扩容同日启动的 enrich），之前 1552 行填 **0 而非 NULL**——缺数当 0（ERR-20260719-002 同族，这次是在数值列上）。

**连带**：`market_amount_daily.total_trillion` 是「沪+深成指」**指数加总代理**（0717=2.12 vs 真两市 2.67 万亿，缺北交所+深市非成分），且仅 2025+。~~本地不存在可回测的真两市成交额历史序列~~（2026-08-09 起失效：`daily_market.volume_trillion` 已回补为 2020+ 真全市场序列，见本条目收口）。

**判别信号**：`SELECT COUNT(*) FROM daily_market WHERE volume_trillion>0` 与总行数比对（32 vs 1584）；或分位分布中位=1.0。

**正确做法**：用前先查非零覆盖；长历史量能研究改用 `index_research.db` 的 **000001.SH**（沪市全市场口径，2010+ 稳定）或 **399006.SZ**（创业板，与标签同体）指数 amount；**深成指 399001.SZ amount 有 2015-05 成分 40→500 扩容断点，不可用于历史**。（2026-08-09 收口后：2020+ 全市场研究首选 `daily_market.volume_trillion` 本列——旧段 A2 双综指、新段本地加总，缝差 <1%；2010+ 更长历史仍走 index_research.db。）

**回补路径**：tushare 大盘接口（Doctor 终端跑，非沙箱）。

**来源** → `AI4ME/CC-遗漏风险因子回测-成交额与浮盈-20260719.md` §二（2026-07-19 首轮跑数中被分位分布异常暴露）

---

## [ERR-20260719-002] 校准工具把 F4「无 IPO 数据的日子」静默记成「未触发」——可评日虚高 2.6 倍，lift 被低估

**状态**: ✅ 已解决（2026-07-19 修 `calibrate_risk_factors.py`）

**现象**：`五因回测校准_20260719.md` 里 F4 可评日 **1581**，而同表 F1/F3/F5 只有 610/606/610。且 F4 阈值扫描 400亿/500亿 档显示 **n=0 触发**，与纪要「滚动20日 max=712亿」直接矛盾。

**根因（两处，独立）**：

1. **缺数当未触发**。原码只在**整张 ipo 表为空**时返 `None`（不可评）：
   ```python
   if not DATA["ipo"]: out["F4"] = None
   else: s = sum(...); out["F4"] = bool(s >= th)   # 表非空 → 每天都可评
   ```
   而 `ipo_daily` 实际只覆盖 **20240102 → 20260716**。2020–2023 约 970 个交易日无数据、滚动和恒为 0 → 判成 `False`「未触发」。
   **F1/F3/F5 本来就是对的**（都用 `anyN` 标记本窗口内是否真有数据点），**只有 F4 这一支漏了**。

2. **样本终点切掉了唯一的尾部事件**。全样本里滚动20日历日募资 ≥400亿 的**只有 20260716 一天（712.2亿，长鑫科技单笔 666亿）**，第二名 20260701 仅 376.6亿。而校准样本终点是 20260714——差两天，正好排除。纪要 §一 明写「F4 尾部几乎由长鑫科技单笔 666亿 驱动」，故那份报告的 F4 描述的是**一个没有它自己主导事件的世界**。

**影响**：

| | 错误值 | 修正后应为 |
|---|---|---|
| F4 可评日 | 1581 | ~610 |
| F4 触发率 | 2.1% (33/1581) | ~5.4% (33/610) |
| F4 lift | 1.55 | ~1.70（基准从全样本 3.9% 回到窗口内 ~3.59%） |

注意方向：**lift 是被低估而非高估**，F4 比报告显示的更有区分力。

**判别信号**：单因子表里某因子的「可评日」显著高于同表其他因子，而其数据源覆盖并不更长。

**正确做法**：按 F5 的写法判可评——检查**本窗口与数据覆盖区间是否有交集**，无交集返 `None`。已实装：
```python
_lo_cov, _hi_cov = min(ipo), max(ipo)
if d <= _lo_cov or lo >= _hi_cov: out["F4"] = None
```
**附带收益**：若 `ipo_daily` 某天起停更，F4 会自动转「不可评」而非静默「未触发」——把静默失败变成显式缺口。

**边界**：只影响 F4 的**统计口径**，不影响日报的当日实时判定（日报读的是当日真实 ipo 数据，不走本回测路径）。

**同族**：[[通用教训]] G-X75（相减前确认两边可比——「无数据」与「未触发」不是一回事）· G-X67（静默截断）· G-X8（已落盘假象）。**元讽刺**：本条是在验证 G-X75 那次改动所产出的报告里发现的。

**来源** → logs/2026-07-19-口径对齐-龙鱼订正与F5债腿降层.md

---

## [ERR-20260719-001] stock_daily 的票池 2026-06-03 从「前 800」扩到全市场，跨此日的截面统计会被宇宙切换污染

**状态**: ✅ 已解决（口径已明确，做法已定）

**这不是缺数，是设计。** `Market-Data/market_data.db` 的 `stock_daily` 研究范围由 Doctor 设定为**市值/流动性靠前的约 800 只 + 渊图内浮现的额外标的**——不是全市场快照。2026-06-03 起扩容到全市场。

**实测边界**（read-only 查 `market_data.db`）：

| 年份 | distinct ts_code |
|---|---|
| 2020 | 736 |
| 2021 | 759 |
| 2022 | 803 |
| 2023 | 826 |
| 2024 | 833 |
| 2025 | 878 |
| 2026 | **5541** |

按日定位：**2026-06-03 当天 876 → 5511，一日跳 +4635**。2026-05 及以前月份稳定在 878~882。

**危害**：任何**跨 2026-06-03** 的**截面占比类**统计，分母凭空变大 6.3 倍——市场宽度、涨跌家数占比、创新低占比、高位股占比、集中度，全部失真。而且**不报错**：脚本照跑、图照出，只是 6 月 3 日那天所有比例指标出现一个纯人造的台阶。

**判别信号**：任何按日的「XX 占比」时间序列在 2026-06-03 出现无法用行情解释的断层；或 `count(distinct ts_code) group by trade_date` 在该日跳变。

**正确做法**：跨期截面统计**必须锁固定宇宙**——先取一个在全区间都有数据的票池再统计。回调级别判别器即锁 **729 只固定池**（`AI4ME/回调级别判别/`），这是范式，不是特例。**只做 2026-06-03 之后的分析可以用全市场**，但要在产物里写明起始日，否则下一个人接手会跨回去。

**边界**：本条只约束**截面占比**类统计。个股时间序列（单只票的价格/成交）不受影响——扩容只加票、不改已有票的历史。

**来源** → `logs/2026-07-18-回调级别判别器.md`（坑首次暴露）· 本条 2026-07-19 由 Doctor 确认设计意图并补全边界日期

---

## [ERR-20260721-001] zhuzhao 任务 /tmp 副本域下 `DATABASE_ROOT.parent` 拼第三方路径全部失效——A6 断更 / B6 不可读 / 级别读数块消失,三症同根

**状态**: ✅ 已解决(2026-07-21 修 gen_daily_report.py ×3 + calibrate_risk_factors.py ×1 + config b6.universe;Doctor 批清单后落地)

**现象**:S2 首份日报(数据日 20260720)三症并发:①A6「最新分位 p91(数据截至 2026-07-17·当日缺→不可评)」;②B6「缺数·分位不可得(stock_daily/宇宙不可读)」;③回调级别读数块整体消失(全文 0 处渲染)。温度「共振1/1」——环境层三盏仅 F1 可评;B6 实际 p96 本应亮灯,当晚真值应为「共振2/3」,读数被低估。

**根因**:zhuzhao 日更任务按 0623 管线 PRD 走 /tmp 副本域(`ZZJY_DATABASE_ROOT` 覆盖 `config.DATABASE_ROOT`)。凡以 `DATABASE_ROOT.parent` 拼「Database/ 之外的第三方路径」者,任务域下全部指向不存在的 /tmp/...:

- grade_section 的 adjustment_grade.py 路径 → subprocess 双分支 FileNotFoundError 被 `except: continue` 静默吞掉 → **`--update` 从未在定时 run 里执行过** → index_research.db 断更在 0717 → A6 当日缺;
- B6 的 universe_fixed.json 路径 → json.load OSError → 「不可读」。

A6 自身的 index_research.db 路径用 OUTPUT_ROOT(PROJECT_ROOT 锚)→ 读到真库,只是库没人更新。**数据本体全程无缺**:stock_daily 更到 0720、729 池当日截面 727 只、B6 只读复现 3.4s 出数(p96)。0718 部署当天的「三分支实测」全部跑在开发环境真路径下,任务域首个交易日(0720)即翻车——**开发环境实测 ≠ 任务沙箱域实测**(G-X8/G-X51 同族)。

**判别信号**:日报 A6/B6/级别块任意组合「不可评/不可读/消失」,而同款命令终端手动跑一切正常;`index_research.db` 的 max(trade_date) 落后 `stock_daily`。

**正确做法**:任务域内引用 Database/ 之外的资产,锚一律取 `PROJECT_ROOT`(脚本真实位置)或 `OUTPUT_ROOT`,禁用 `DATABASE_ROOT.parent`;config `b6.universe` 语义=相对 OUTPUT_ROOT。凡新增跨域路径,须在 `ZZJY_DATABASE_ROOT=/tmp/空目录` 模拟下断言可达再上线。静默吞噬按 0714 根治口径改 fail-loud(stderr 一行 + 日报灰字占位)。

**断点回补**:2026-07-21 Doctor 终端 `adjustment_grade.py --update --json` 一次补齐三指数 0720+0721(各 +2 行),同时反证 token/网络/接口全程无恙。

**来源** → 本场会话(2026-07-21,日志待 /save)· 承 [[2026-07-19-口径对齐-龙鱼订正与F5债腿降层]] S2 线 · PRD B 组 B1/B2 的数据链前提

**补注（2026-07-21 · 四件核验闭环时发现）**：修复上线后仍撞到 ③ 的一个**新变体**——最新正式报（0721·某次自动生成）级别读数块显示 fail-loud 占位「级别读数不可用」，而**工具与数据本身健康**：只读 `adjustment_grade.py --json` 当场返回 `L3(急跌型)·confirm=true·dd244 -15.69·ep14`。即：路径修复已生效（占位=显式化起效、非静默消失），但**某次自动生成进程里 subprocess 两分支仍全败**，根因未定（已排除 `ZZJY_DATABASE_ROOT` 覆盖——工具不吃该 env）。**Doctor 终端真实 shell 重跑 `python3 tools/gen_daily_report.py` 即补齐 L3**。教训：占位≠数据坏；「手动 regen 正常 ≠ 定时链路正常」，定时环境是否复发须在下次 10:00 run 后查 stderr `[grade_section]` 行确认。

---

## [ERR-20260722-001] `market_data.db` 中断写留下热日志(-journal) → 只读(mode=ro)打开报 `attempt to write a readonly database`,日报 regen 取数当场崩

**状态**: ✅ 已解决(2026-07-22 · Doctor 终端 `sqlite3 <db> "PRAGMA quick_check;"` 触发自动回滚,-journal 清除,regen 跑通)

**现象**:`gen_daily_report.py` regen 在 `gather()` 第一句 `md.execute("SELECT trade_date,etf_code,pct_chg FROM theme_etf_daily …")` 即抛 `sqlite3.OperationalError: attempt to write a readonly database`。诡异点:是 **SELECT**、且连接明明是**只读**打开(`sqlite3.connect(f"file:{MARKET_DB}?mode=ro", uri=True)`,脚本 line 296)。

**根因**:`Database/Market-Data/market_data.db` 旁挂一个 **9.4MB 的 `market_data.db-journal`(回滚日志)**——上游一次写入(大概率句芒行情更新)**写到一半被中断**,留下「热日志」。SQLite 打开一个带热日志的库时,**必须先回滚这条半截事务**才能给出一致视图;而 `mode=ro` 只读态**写不了**(回滚要写主库),于是把「我需要写但写不了」报成 `attempt to write a readonly database`。**不是文件权限问题**——库(600)与目录对属主可写,`os.access(...,W_OK)` 为真。

**判别信号**:① 报错落在**只读连接的 SELECT** 上、措辞是「readonly database」——十有八九是热日志,不是 chmod;② 库目录里有 `*.db-journal`(回滚模式) 或未 checkpoint 的 `*.db-wal`;③ 同库同命令换读写方式打开就好。

**正确做法(修复)**:让 SQLite **读写打开一次触发标准崩溃恢复**——Doctor 终端 `sqlite3 <db> "PRAGMA quick_check;"`(读写默认打开 → 回滚半截事务 + 删 -journal + 顺带查完整性)。回滚会**丢弃那次没写完的更新**(库回到上一致状态,安全);之后让上游更新重跑补数即可。**铁律:切勿手动 `rm` 掉 -journal**——那会丢失回滚信息、直接毁库。CC 不在沙箱对生产库跑写命令(挂载盘=Doctor 真实 Documents,沙箱写即写真库),恢复命令一律交 Doctor 终端。**动前先 `lsof`/`ps` 确认没有进程正在写该库**,别在活事务上回滚。

**与 07-21 的互链(强候选·未坐实)**:ERR-20260721-001 补注里「某次自动生成 subprocess 两分支全败、级别读数不可用、根因未定」——**极可能同一失败类**:热日志/中断写落在挂载盘 DB,只读打开崩溃恢复失败。惟当时是 `adjustment_grade` 读 `index_research.db`、今日是 `gen_daily_report` 读 `market_data.db`,**不同库**,故只标强候选、非同一实例坐实。下次定时 run 若再现,先查目标库有无 `*-journal/*-wal`。

**上游隐患(待另治)**:热日志说明句芒行情更新链路存在**中断写**风险(被 kill / 崩 / 挂载抖动)。根治应在更新脚本:写入包事务 + 完成即 checkpoint/清 journal;或换 WAL 并定期 `wal_checkpoint(TRUNCATE)`。归入 disk-I/O 家族 TODO。

**来源** → brain/logs/2026-07-22-五因regen验收与resume开声固化.md · 承 [[2026-07-21-级别读数占位根因定位与语音链路坐实]] disk-I/O 线


## [ERR-20260722-003] 沙箱经 FUSE 整库写回，大表(stock_daily)不 durable 落 Mac 真实盘 → 日报隔天退回

**状态**: ✅ 已根治（2026-07-22 写库迁 Mac 原生 launchd · plist 指向 `ops/mac_daily_marketdata.py` 在产、.sh 版已弃归档 · 2026-08-08 复盘补标；通用层 FUSE 隐患由「沙箱写库优先交 Mac 原生侧」规覆盖）

**现象**：Doctor 报「复盘日报 artifact 落后一天」。07-23 中午库里 `stock_daily`/五张烛照表停 07-21、唯 `daily_market` 到 07-22。句芒 07-22 日志明写当时已把 07-22 落进 stock_daily（+5526、原子 mv、immutable 复读验过 max=20260722），但 **Doctor 自己 Mac 原生盘复核仍 stock_daily=20260721**。

**根因**：句芒/九儿写库走「整库拷 /tmp → 改 → `mv` 覆盖回挂载盘」。这条 mv 覆盖经 Cowork 的 FUSE 桥回写 Mac 真实文件时**大写入不 durable**：5526 行的 stock_daily 新页没落住、1 行的 daily_market 侥幸落住 → 单表回退。**非 Tushare 缺数、非日报逻辑 bug、非读缓存陈旧**（Doctor 原生盘亲测坐实是"写没落住"＝A 类）。

**判别信号**：① 某表沙箱内写完复读 OK、隔数小时/换进程读又退回旧值；② 大表退回、同库小表存活＝页级部分持久化特征；③ 到 Mac 原生盘复核最新交易日即定 A(写没落)/B(读脏)。

**正确做法（根治）**：写库任务挪回 **Mac 原生 launchd**（本机 ext 写即 durable、无 /tmp mv、无 FUSE），沙箱侧改只读消费。见 `烛照九阴/ops/`（Phase 1）+ [[烛照九阴/architecture/决策记录]] 2026-07-22 迁移条。**缓解（未采）**：写锁 + mv 后 fsync + 丢缓存新连接复读重试。

**同族**：disk-I/O 家族（ERR-20260719-003 历史 0-fill · 五因场热日志 -journal）· 句芒「放回必 cp→原子 mv、绝不 cp 盖原文件」。**来源** → brain/logs/2026-07-22-日报隔天退回根治与Mac原生Phase1.md

## [ERR-20260728-005] 同库两个「全市场成交额」定义相差 25%，无一处注明（同名异义）
**状态**: ✅ 已裁定（2026-07-28 甲案·Doctor 批）：按用途定源＋禁跨源——分位/比值/回测类锁 `market_amount_daily.total_trillion`、水平显示/容量类锁 `daily_market.volume_trillion`；见 `Database/Market-Data/MANIFEST.md`「双源定源裁定」节。（2026-08-08 复盘补同步：本条「待择一」系档案滞后——甲案同日已批、状态行未回写，NOTE-20260719-001 族）（**2026-08-09 乙案修订·Doctor 批**：成交额条改为 2020+ 全锁 `volume_trillion`，`market_amount_daily` 降 2010 前长史专用+对撞监控；甲案「少计属口径特征非误差」前提被实测证伪——两源比值日摆 1.18–1.79、252 日分位差中位 3.2pp/max 29.4pp。阈值分位等效重锚 0.045→0.030 等，详见 MANIFEST 定源裁定节）
**优先级**: 🔴 高（任何「全市场成交额分位」选错源结论即偏 25%）
**触发场景**: `daily_market.volume_trillion`（≡SUM(stock_daily.amount)/1e9·全A逐股加总·20260727=2.089万亿）vs `market_amount_daily.total_trillion`（tushare 沪深两市官方口径·同日 1.6649万亿），系统性 +25~26%。
**解决方案（临时）**: 已在 `Database/Market-Data/MANIFEST.md` 加「同名异义警示」节；正式择一并统一消费方待 Doctor 裁。
**预防措施**: 新表引入时先做「同名概念对撞检查」；25% 级安静偏差比全 0 伪列更危险（后者一眼可穿）。

## [ERR-20260728-006] 涨跌停家数双源不一致（差 3–22%），远超 MANIFEST 声明的 ±2 家
**状态**: ✅ 已裁定（2026-07-28 甲案·Doctor 批）：`emotion_cycle` 存量链锁 `daily_market.limit_up/down` 不换（390 天分位历史自洽·换源=断代重校）；新增用途一律 `limit_list_daily`（个股级清单真源·连板梯队必经）；见 `Database/Market-Data/MANIFEST.md`「双源定源裁定」节。（2026-08-08 复盘补同步：本条「待择一」系档案滞后——甲案同日已批、状态行未回写）
**优先级**: 🟡 中
**触发场景**: `daily_market.limit_up/limit_down` vs `limit_list_daily` 计数：0723 涨停 127 vs 116、0727 119 vs 111、0720 跌停 257 vs 210（差 22%）。日报快照与 emotion_cycle 走 daily_market 支。
**预防措施**: 同上「同名异义对撞检查」；emotion 引擎若换源须整体重校分位。

## [ERR-20260728-007] `daily_market.max_consecutive` 与 `emotion_cycle.total_volume` 为 volume_trillion 同族伪列（未登记过）
**状态**: ✅ 已定性（勿用）（2026-08-09 注：`volume_trillion` 本体已 A2 回补修复、ERR-20260719-003 收口，并从 MANIFEST 伪列黑名单摘帽；本条对 `max_consecutive` / `seal_rate` / `total_volume` 继续有效）
**优先级**: 🟡 中
**触发场景**: `max_consecutive` 首个非零 20260603（此前全 0 非 NULL·与 ERR-20260719-003 同族同源）；`emotion_cycle.total_volume` 284/390 行为 0（与 seal_rate 死列同家）。
**预防措施**: 伪列黑名单从单列扩为族：volume_trillion / max_consecutive / seal_rate / total_volume；回测取列前先做「量纲/符号/覆盖/披露制度」四查。

## [ERR-20260728-008] north_flow 语义翻转日精确定位 20240819，且 daily_market.north_money 为同一污染的镜像列
**状态**: ✅ 已定性（补充 ERR-20260727-004）
**优先级**: 🟡 中
**触发场景**: 20240816 net=−6774.99 → 20240819 起 north_money ≡ hgt+sgt（买卖成交总额·2025-26 零负值）。`daily_market.north_money` 与其同日完全相等＝同污染。
**解决方案**: 净额语义 2024-08-19 前有效；此后仅可作「北向参与度/活跃度」用且须重命名语义；镜像列同禁。

## [ERR-20260731-001] `intl_index_daily::US10Y`(^TNX) 与 FRED `DGS10` 是**同名异义三轴**——平日差 0~1bp 骗过校准，**事件日劈 5bp**
**状态**: ✅ 已定性（2026-07-31 财政部方法论页坐实，由「时点语义」升格为三轴；**同日分时实测订正轴Ⅰ 的时点方向，升 v3**，详见 [[剑酒青丘/frameworks/事件归因台账]] P-11 v3）
**优先级**: 🔴 高（任何把本地 ^TNX 当「官方 10Y 收盘」用的归因/回测结论都可能整条作废）
**触发场景**: 2026-07-29（FOMC 决议日）同一个「10Y 收盘」，两源差 **5bp**——FRED `DGS10` ＝ **4.67**，本地 `intl_index_daily` code=US10Y(^TNX) ＝ **4.62**。逐日对表：

| 日期 | DGS10 | 本地 ^TNX | 差 |
|---|---|---|---|
| 07-20 / 21 / 22 / 23 / 24 / 27 / 28 | 4.60 / 4.63 / 4.67 / 4.71 / 4.69 / 4.65 / 4.61 | 4.60 / 4.63 / 4.66 / 4.70 / 4.68 / 4.64 / 4.60 | **0~1bp** |
| **07-29（决议日）** | **4.67** | **4.62** | **5bp** ⚠ |

**根因（同名异义·三轴 · ERR-20260728-005 家族 · v2 按财政部原文坐实 · v3 按分时实测订正轴Ⅰ）**: **Ⅰ时点轴**——`DGS10` 输入为纽约联储 *at or near 3:30 PM*（官方措辞带弹性，非硬 15:30）取得，`^TNX` 是 **Cboe Indices 15:00 ET 收市**。**⚠ 方向订正（v3 · 2026-07-31 实测）**：v2 原写「`^TNX` 是 CBOE **16:00 收盘**」，由此得到的「`DGS10` 早、`^TNX` 晚」**与事实相反**——`^TNX` 时段为 **08:20–15:00 ET**，`DGS10` 取数反而**晚约 30 分钟**，箭头掉头。实测（Yahoo chart `meta`）：`exchangeTimezoneName=America/Chicago` · `gmtoffset=-18000` · regular `12:20→19:00 UTC`＝08:20–15:00 ET；07-29 末根 `18:59 UTC`＝**14:59 ET＝4.622**，与库中 close 4.62 一致 ⇒ **库里存的是 15:00 ET 收市读数**。「16:00」当初无任何来源，是按美股收盘惯例默认的，同属「没核口径就用」。**Ⅱ报价 vs 成交轴**——`DGS10` 输入是 *indicative, bid-side market price quotations (not actual transactions)*＝指示性买方报价、明文非成交，`^TNX` 由成交推得，事件日尾盘报价与成交本就不同步；**Ⅲ插值 vs 单券轴**——`DGS10` 是 par yield curve（monotone convex）插值出的常年期构造值，未必对应任何真实券（H.15 脚注 9），`^TNX` 跟单一标的。平日尾盘无事三轴均不显形，事件日一起显形。**坑源注**：H.15 页自述 *closing market bid yields*、财政部方法论页写 *at or near 3:30 PM* 快照——两官方页措辞打架，只读 H.15 必然读成「收盘价」；本条口径以财政部方法论页为准。

**⚠ 4.67 vs 本地全日高 4.655 落差（判据 v3 · 2026-07-31 分时实测后重写 · 本议题结案）**: ① **全日高订正为 4.655 @ 12:15 ET**（v2 记 4.651 @ 12:10 系二手转述；实测 1m/5m 双口径一致。差 0.4bp / 5 分钟，不影响结论）。② **轴Ⅲ 结论不变**：`DGS10` 是插值构造值，没有义务落进 `^TNX` 日内区间，v1 判据「落不进去 ⇒ 某一侧数据有问题」维持作废。③ **v2 保留的用途「重取分时测时点轴贡献」查明不可行，结案**——15:30 ET 时 `^TNX` 已收市（15:00 ET），**该时刻不存在报价**，此测量在本源上**结构性做不到**，非数据缺失。要测须换源：CME `ZN=F` 或现券 tick。④ **方向可解释、量级未证**：07-29 路径 12:15 高 4.655 → 14:49 低 4.610 → 14:59 收 4.622（末 10 分钟反弹中）；若 15:00→15:30 延续动能，`DGS10` 达 4.67 需再涨约 **4.8bp**。**此为外推、非实测**，按「禁止用代理值外推权威值」只记「方向可解释、量级未证」，不得当已核事实引用。剩余落差按轴Ⅱ/Ⅲ 记口径差，非数据错误。

**判别信号**: ① 同一标的两个源在**平静期**高度贴合，却在**事件日/数据日**突然劈开 → 十有八九是时点语义差，不是数据错；② 差值方向恒定（本例 FRED 系统性 ≥ 本地 0~1bp）说明是**口径偏置**而非随机噪声。

**正确做法**:
- **归因账引用美债收益率一律以 H.15 / FRED 为权威源**；本地 `^TNX` 仅作**时效代理**（H.15 T+1 发布、代理可当日取），引用必须标口径。
- **禁止用代理值外推权威值**。本例活体教训：H.15 尚未发布 07-29 时，CC 用本地 4.62 ＋「近 5 日差 0~1bp」外推「FRED ≈4.62~4.63」并当作**已核事实**写进提案 P-09 与 case study，隔日取到真值 4.67，**整条提案作废**（CC 第三次撤回）。官方源没出就写「未发布」。
- **跨源校准的有效期只到下一个事件日**——「N 天差 0~1bp」不构成事件日仍成立的证据，事件日必须单独复核。
- 两源差 **>2bp** 的交易日标「**源分歧**」，两值并列、不取单值入序列。

**与 G033 的关系**: G033 管「同一张表里读数语义腿 vs 收盘语义腿」（**表内**分层），本条管「同一标的跨库两个源的时点口径」（**跨源**分层）。两者叠加意味着 `US10Y` 这条腿有**双重语义风险**：既可能取到盘中读数、又与官方 CMT 口径不同源。

**来源** → brain/logs/2026-07-31-*（2Y终核与P-09撤回）· [[剑酒青丘/frameworks/事件归因台账]] §六 P-11/P-12 · 同族 ERR-20260728-005（全市场成交额两口径差 25%）

## [ERR-20260811-001] 内联 echarts 大 HTML 找 body/切片：`h.find("<body")` 会误中 echarts JS 字符串，真 body 在首个 `</script>` 后
**状态**: ✅ 已定性（2026-08-11 手机卡切片两次踩中后定位）
**优先级**: 🟡 中（凡要解析/切片烛照九阴日报这类「1MB echarts 全内联」的单文件 HTML 就绕不开）
**触发场景**: 做 9:16 手机卡要切日报结构。`h.find("<body")` 命中 @849272——那是 echarts toolbox saveAsImage 代码里的字符串 `'<body style="margin:0;">...'`，不是真 body；真 body 在 @2054693。接着 html.parser 切结构又吐垃圾伪标签 `<e.length;r++){var>`——内联 echarts JS 里的 `<` 被当标签解析。
**根因**: 烛照日报把 ~1MB echarts 库整段内联在 `<script>`（@164→1033604），里面含 `<body`、`<div`、大量 `<` 比较符。任何「全文找标签 / 正则定位 / 不剥 script 的 parser」都会被这些字符串带偏。
**正确做法**:
- 找真 body：取**第一个 `</script>` 之后**的 `<body`（`h.find("<body", h.find("</script>"))`）；`</body>` 用 `rfind`。
- 切 top-level 结构前**先 `re.sub(r"<script[\s\S]*?</script>","",body)` 剥掉内联脚本**（`<template>`/`<style>` 同理），否则 echarts JS 里的 `<` 会被 HTMLParser 当开标签、吐出 `<e.length...` 伪节点。
- 定位各 section 用**带 id 的锚点**（`<h2 id="sec-main"/sec-gap/sec-opp"`）或唯一类名（`.rr-band`/`.p0-strip`），别用会被 CSS/字符串撞中的裸文本。
**来源** → brain/logs/2026-08-11-手机卡916模块点名与终卡.md

## [ERR-20260813-001] Safari 不吃 `display:grid`：手机卡壳内可见 grid 容器须全转 flex
**状态**: ✅ 已定性（2026-08-13 手机卡打磨实测三连踩：GAP 标签列 → row2 图表 → 四联条依次在 Safari 上下堆叠；同文件 Chrome headless 渲染正常）
**优先级**: 🔴 高（手机卡在 Safari 是第一查看环境；任何新增 grid 布局都会重蹈）
**触发场景**: 手机卡壳（`#zzcard` 内嵌报告 + zz-card-css）里用 `display:grid` 的容器——`.zzgrid .zzrow`（GAP 左列）、`.row2`（情绪图×容量表）、`.snapshot-band`（四联条）、`.liquidity-grid`（成交额×满载）——在 Safari 全部失效为普通流/行内，布局上下堆叠；同文件 Chrome 无头渲染完全正常。缓存已排除（换文件名重开同样复现）。
**根因**: 未深挖 WebKit 具体缺陷（规则字节干净、括号配平、Safari 26 理应支持 grid）；从工程角度判为「本环境 Safari 对 body 内嵌 `<style>` 中 grid 规则的选择性失效」。
**正确做法**:
- 壳内**可见布局容器一律 flex**：`.row2` 用定宽百分比（`width:calc(54% - 6px)` 等比，勿依赖 flex-grow 让图表固有宽度干扰）；左列 gutter 用 `flex:0 0 {px}` 固定宽 + `justify-content:center`。
- 改完必验双端：Chrome 无头渲染 + Safari 真机刷新（本坑 Chrome 全绿、Safari 全崩，只看一端必漏）。
- 隐藏模块（`.zzh{display:none}`）内的 grid 不必动——不渲染不害事。
**来源** → brain/logs/2026-08-13-手机卡终卡打磨与兑现闸门回测落地.md

## [ERR-20260813-002] `<b>` 标签的 `font-weight:bolder` 是**相对值**：父级提重后子级漂移一档
**状态**: ✅ 已定性（2026-08-13 手机卡加粗后「情绪周期与市场快照」h2 与「满载」b 明显不同重）
**优先级**: 🟡 中（凡给容器整体加粗/改字重就会触发）
**触发场景**: body `font-weight` 400→700 后，「满载」等 `<b>` 文本从 Bold 变成 Heavy（900），而显式写 700 的 h2 停在 Bold——两处视觉明显不同重，Doctor 报「字体变了」。查规则链条：h2 与 b 的 font-family 完全同栈，唯一差异在字重。
**根因**: 浏览器 UA 默认样式里 `<b>,<strong>` 是 `font-weight:bolder`（**相对父级**的档位），不是绝对 bold。父级 400 时 b=700；父级 700 时 b=900。改容器字重不动 `<b>`，它就跟着漂。
**正确做法**:
- 要让某元素与 `<b>` 视觉同重，按其**实际解析值**显式对齐（本例 h2 700→900），别写「和 b 一样 bold」。
- 容器加粗时，逐元素核对 `<b>/<strong>` 是否漂移；要钉死就用显式数值（700/900）。
- 与 ERR-20260731-001 同族：**相对语义 vs 绝对语义**——bolder 是相对、bold 是绝对，命名像、行为不同。
**来源** → brain/logs/2026-08-13-手机卡终卡打磨与兑现闸门回测落地.md

## [ERR-20260819-001] dim4_trade_plan.position_repr 数值列落定性文本（类型污染）——07-08 首犯、07-18 修、08-02/03/05 复发、08-19 档2 全量清空

**状态**: ✅ 已修复（Doctor 2026-08-19 落签——哥哥「同意」。句芒档2清空 3 行 repr 文本 + dim2 补近似注记 2 行；九儿按 06-28/07-07 双先例清空 08-03 min/max 分项口径、ingest SKILL 落三道闸门根治；G-X152 通用教训已升格）

**优先级**: 🟡 中（喂回测的仓位数值列混入文本，错一个污染一串）

**触发场景**: dim4_trade_plan 入库时把定性表述写进 position_repr（REAL 语义数值列）；判别：`SELECT date FROM dim4_trade_plan WHERE position_repr IS NOT NULL AND typeof(position_repr) NOT IN ('real','integer')`。

**硬证据/最小复现**: 修前该查询返回 3 行——2026-08-02「中等仓位(定性·未给总仓位数字)+浮动仓10%-20%」、2026-08-03「硬科技20%-40%+其他轮动板块约20%试探·总仓低水位运行(定性)」、2026-08-05「中等/适中仓位(定性·原文未给总仓位数字)+避免满仓」；修后 0 行。

**根因**: 规约文本与实际口径打架——07-18 订正注记「repr 应为数值」（07-08 行经哥哥批准移 position_band）未落成入库侧闸门；08-02 起实际口径演化为「repr=代表性表述、回测只读 min/max」，九儿连续落文本，审查班 08-02/03/05 三次报「只报不改」等裁。2026-08-18 哥哥立档2协议裁死：repr 文本行清空为 NULL（现行口径回测只读 min/max），定性说明归 position_band / 待复核清单。

**影响面**: 仓位数值列类型污染（下游 float 读取静默强转 0.0 或报错）；08-03 行还叠加「分项仓位当总仓」口径张力（min=0.2/max=0.4 系硬科技分项 20%-40%、非总仓）——同日九儿按 06-28/07-07 双先例清空（见待复核清单订正回执，哥哥可一句话推翻）。

**修复/建议修法**（2026-08-19 句芒已执行）: 3 行 repr 清 NULL，定性文本原样保留于各 position_band 与待复核清单判读；备份 `recap.db.bak_20260819_prefix句芒`，/tmp 副本往返（G-X33），证据四件套见 `agents/句芒/logs/2026-08-19-课件入库审核.md`「修复记录」。**入库侧根治已落**（2026-08-19 哥哥交九儿优化执行）: ingest SKILL 落三道闸门——闸①repr 只接受 0-1 数值（定性文本→position_band/raw、repr=NULL）；闸②分项/子仓/条件情景数字不落总仓数值列（06-28/07-07 双先例）；闸③dim2 涨跌停近似数必落【近似注记】至 supply_demand_pattern。证据见 `agents/烛阴/logs/2026-08-19-闸门优化.md`。

**预防门禁**: 每班 dim4 审查必跑 typeof 检查（已纳入复发扫描）；同根复发追记本条目、不新增。

**来源**: agents/句芒/logs/2026-08-19-课件入库审核.md · agents/句芒/logs/2026-07-08-课件入库审核.md（首报）· 2026-08-18 哥哥立修复协议（档2）

**应升格通用教训**（同族第二次复发·07-08→08-02/03/05）: 已升格 **G-X152**（`brain/permanent/通用教训.md`，2026-08-19 哥哥「你来决定」授权九儿执笔）——「数值列不得落定性文本与分项口径，入库侧落类型+口径双闸」。✅ 已于 2026-08-19 由 Doctor 落签（哥哥「同意」）。

---

## [ERR-20260820-001] 日报风险区「逾期未启动信号」把条目级负状态升维成板块级——热门已启动板块被列进「等轮动」名单

**状态**: 已修待验（2026-08-20 实施完成 · 待 Doctor 或指定独立验收方验；实施者不自签 ✅）

**实施留痕**（2026-08-20 · Doctor 裁 C 案后执行）：`gen_daily_report.py` L963-967 改——① 文案精确化：「逾期未兑现锚点信号 N 条——单条信号锚存疑，板块整体启动状态见兑现状态区」；② 聚合过滤：只列该锚逾期未兑现条目占比 ≥30% 的锚（HAVING 子查询），列表空则走「分散于各板块（无板块占比超 30%）」分支。自验证据：py_compile 通过 · live DB 只读复算（原口径 56 条/15 锚 vs 新口径过滤后空列表·最高占比券商 22.2%）· `--output /tmp` 试跑 exit=0 渲染出新文案、旧文案零残留。**生产生效路径**：正式产物已重生成（AI4ME·旧报快照 _pre-snapshots/）+ live artifact 已推（updatedAt 08-20T17:27Z·SHA 02bbc425… 三层一致）；git 收口已核实（Doctor 终端跑·gitcheck.py 实核：brain `b625d488` / 烛照九阴 `9af7fbcb` 两 commit 在 HEAD 链·push 已同步）。**待验项**：Doctor/独立验收方目验 live 卡片风险区文案（实施者不自签 ✅）。

**条目级处置追记**（2026-08-21 · Doctor 裁「按锚抽审+批量退役」· 二次确认「改锚7+退役28+留观察21」· 执行修正后终值 56→27）：① **退役 29 条**（无锚 7：情绪周期/宏观/跨域——商业航天×2、创新药连板梯队、光伏反内卷+风电、黄金×2；过时封顶 21+沙特补漏 1：信达BD/流感/券商合并/银行PB/铝/CCL/印尼镍/稀土/航天事件等——全部 >120 日窗口封顶未兑现）——`status='retired'` 标记，closure `load_signals` 加退役过滤（引擎跳过不重算、gap_* 历史账保留、可回滚），台账 `docs/退役登记_20260821.tsv` 29 行；② **改锚 7 条**（`SIGNAL_THEME_OVERRIDE` kw 唯一子串精确匹配：硅片×3+靶材→半导体、四氯化硅→光模块、算力能源/SOFC→电力、半导体/光模块→半导体）——**6/7 条在正确锚下「起死回生」**（半导体锚已点亮 2 次·峰值 +24.9%~+32.0%、SOFC +11.9%、长鑫 +7.5%），坐实「错挂锚致『从未启动』误判」；四氯化硅改挂光模块后仍逾期（42 日 −19.8%，诚实保留）；③ **留观察 20 + 重算漂移 6**：30-120 日窗口内锚对条目保持观察，dry-run 全量重算新增 6 条刚跨 30 日（自然时间推进）；④ 生成器逾期查询加 `status != 'retired'`（56→27）；⑤ 日报重生成 + artifact 已推（2026-08-21）。**结构缺口修复**：closure 状态机自此有「锚失效出口」（退役态），计数不再只增不减。自验：副本库全链路 dry-run（tier_override=7 精确、退役残留 0、逾期 27 无一条早于 04-21）· Doctor 终端 apply 后现库核验（retired=29 · 逾期 27 · 审核表 1683 行）。**待验**：Doctor 目验日报黄条新数字与退役效果（实施者不自签 ✅）。

**触发**: 2026-08-20 Doctor 挑错复盘日报 artifact：风险区「逾期未启动信号 56 条（创新药,券商/金融,商业航天/卫星,有色金属,黄金/贵金属,AI软件/应用,光伏,电力/电网,稀土,机器人,新能源电池,钨/小金属,AI算力,光模块,半导体…）——逻辑存疑或等轮动」——Doctor 指出里面很多板块是**启动过的**，而非逾期未启动。

**硬证据**: ① `gen_daily_report.py` L963-967：`SELECT COUNT(*), GROUP_CONCAT(DISTINCT etf_anchor) FROM industry_signals WHERE gap_desc LIKE '%逾期%'` 聚合出板块列表；② `closure_engine.py` L254-265：`describe()` 中 `status=open 且 n_days>30` → 单条信号「⚠️逾期未启动（N日，累计x%）——逻辑存疑或锚不对」——是**单条信号锚失效判定**，非板块级状态；③ 板块聚合实核（`docs/兑现检测_审核表_20260820.tsv`，56 条 industry + 5 条 yuantu）：被列 15 板块兑现率 82-99%——新能源电池 157/159 兑现·149 点亮、AI算力 235/251、光模块 157/171、黄金 40/44、钨 28/29、稀土 13/14、有色 59/63、半导体 87/95、商业航天 83/93、机器人 56/68；且 61 行全部 relit_count=0、date_realized 空——条目级「从未启动」为真、板块级「未启动」为假。

**根因**: 呈现层聚合维度错配——条目级负状态（单条信号 30 日+未兑现）按 etf_anchor 升维成板块名单，文案「逾期未启动信号（板块列表）——逻辑存疑或等轮动」被读成板块级「没启动/等轮动」；条目级事实与板块级事实（绝大多数早已启动兑现）被混成一句。

**影响面**: 日报风险区黄条长期误导板块启动状态判断，Doctor 读报判断被带偏（用户可感知的功能性误导）。附发现：日报统计只查 `industry_signals`，yuantu_buy_signals 的同款 5 条逾期未启动不在口径内。

**建议修法**: 待 Doctor 裁——A 文案精确化（「逾期未兑现锚点信号 N 条（板块）——单条信号锚存疑，板块启动状态见兑现区」）；B 聚合层过滤（只列该板块逾期占比超阈值的板块）；C A+B。

**预防门禁**: 聚合呈现前核对「条目级状态」与「聚合维度文案」语义同层；改动上线后 Doctor 目验日报风险区。

**来源**: 2026-08-20 会话 Doctor 挑错 · `gen_daily_report.py` L963-967 · `closure_engine.py` L254-265 · `docs/兑现检测_审核表_20260820.tsv`（板块聚合实核）

---

## [ERR-20260826-001] dim1/dim3 同 kejian_date 重复入库——2025-10-19 与 2026-03-08 三对重复行（05-06/05-09 双轮回填无去重）

**状态**: 🔄 已修待验（2026-08-26 句芒档1 修复完成 · 待 Doctor 或指定独立验收方验；实施者不自签 ✅）

**优先级**: 🟡 中（同内容双行 → 按日 COUNT/聚合类下游统计双重计数，dim3 情绪序列两日被重复加权）

**触发场景**: 全表同日多行扫描：`SELECT date, COUNT(*) FROM dim1_external_pricing GROUP BY date HAVING COUNT(*)>1`（dim1 命中 2026-03-08；dim3 命中 2025-10-19、2026-03-08）。

**硬证据/最小复现**: 三对行除 id/created_at 外内容全同——dim1 2026-03-08: id 38（created 2026-05-06 18:13:23）与 id 45（created 2026-05-09 14:03:21）全列相同；dim3 2026-03-08: id 419 vs 462 全列相同；dim3 2025-10-19: id 331 vs 461 仅差 support_level（'3936' vs NULL，早期行更全）。修后 GROUP BY 复查 0 组。

**根因**: 2026-05-06 18:12-18:13 全量历史回填批（recap_daily ~105 行/dim2 ~106 行/dim3 ~106 行/dim1 30 行）落库后，2026-05-09 14:03 又跑一轮小批次补漏（recap_daily 2 行 + dim1 1 行 + dim3 2 行），补漏批对 dim1/dim3 未做「该 date 是否已有行」去重 → 同日双行。属 processed_kejian 去重表建立（或覆盖）之前的早期管线缺陷，非现行 ingest 引入。

**影响面**: dim1/dim3 按日读取的下游（四维度复盘、情绪周期研究）对 2025-10-19、2026-03-08 双计；dim3 2025-10-19 行的 support_level='3936' 仅存于早期行，若误删早期行会丢失该字段。

**修复/建议修法**（2026-08-26 句芒已执行）: 档1 当场修——保留早期行（id 38/331/419），删除后补重复行（id 45/461/462）；备份 `recap.db.bak_20260826_prefix句芒`，/tmp 副本往返（mktemp 换根·G-X96），放回走 cp→原子 mv（ERR-20260722-003），真库复验 integrity=ok、md5=91743c2db7473391bfd1574bada5f832、只增不减（dim1 180→179、dim3 212→210，其余表不变）。证据四件套见 `agents/句芒/logs/2026-08-26-课件入库审核.md`「修复记录」。未触碰 gap 跟踪列与 10:00 zhuzhao 班域。

**预防门禁**: 审查班六项审查「去重完整性」升级为**全表 GROUP BY date 扫描**（此前只查当日行，历史残留漏网至今）；入库侧现已有 processed_kejian filename+md5 双判 + 九儿断言自检，若再现同款（同 date 双行）说明现行去重失效，同根复发追记本条、不新增。

**来源**: agents/句芒/logs/2026-08-26-课件入库审核.md（二次触发复核段）· 本条目 2026-08-26 句芒课件入库审核班发现并修复

**追记 2026-09-01（同族新暴露·非复发 · 挂单待裁）**: 2026-09-01 句芒审核班将 GROUP BY date 扫描扩到 dim2_sector_themes 时新暴露历史残留——`2026-05-05`（id 158/184）与 `2026-05-06`（id 157/185）各两行。与 08-26 修掉的全同重复行**不同**：两行各含独有数据——05-11 批行（id 157/158）main_line/sub_themes/sectors_* 为 NULL 但 sector_logic/price_catalyst 带 KB-P2 知识库来源内容（电新周报/光刻机行业深度）；06-03 批行（id 184/185）为课件维度完整实体行。删任一行都会丢独有信息，合并方案（并入实体行保留 KB-P2 字段？按日期双行并存是否有下游依赖？）属判断性+不可逆，**本班未动库、挂单请 Doctor 裁**。已知下游 `scripts/enhance_with_jumang.py` L61 用 `WHERE main_line IS NOT NULL` 读取（仅命中实体行、不受双行影响）；其他下游未逐一排查（未核）。本班日志：`agents/句芒/logs/2026-09-01-课件入库审核.md`。


---

## [ERR-20260827-001] fetch_fred_ust.py 缺项目根 bootstrap——沙箱内 import config 失败 fallback 直写 live market_data.db（G019 同族·留热 journal）

**状态**: 🔄 已修待验（**2026-09-01 Doctor 裁「根治」→ CC 实施三层防线**：① 顶部 `sys.path.insert(0, 项目根)` bootstrap——保证班域内 import config 成功、`config.MARKET_DB` 随 `ZZJY_DATABASE_ROOT` 指向 /tmp 副本根（主因消除）；② `_db_path()` 删 `except Exception` 静默 fallback——不再回退直写 live（fail-loud）；③ 写连接改走 `config.connect_write` 中央护栏——沙箱挂载盘（含 /sessions//mnt/）直写被拒（G019 兜底）。**全 scripts/ 扫查：唯本脚本缺 bootstrap**（其余 15 件均有）——四次复发同源收敛单文件。验证：py_compile ✓ · 班域模拟 `ZZJY_DATABASE_ROOT=/tmp/zzdbroot` → `_db_path=/tmp/zzdbroot/Market-Data/market_data.db` ✓ · 负向无 env 沙箱域 → connect_write 抛 RuntimeError 拒绝 live ✓。**实施者不自签**——待独立验收）

**现象**: 2026-08-27 10:00 定时班跑 `python3 scripts/fetch_fred_ust.py`（已 source env · ZZJY_DATABASE_ROOT=/tmp 副本根），FRED 取数两序列 [ok]（DFII10 +32 行 / THREEFYTP10 +30 行）但 `con.commit()` 抛 `sqlite3.OperationalError: disk I/O error`；随后 live `market_data.db` 出现 12824 字节热 journal、主文件 mtime 被改，任何只读打开 live 的进程报「attempt to write a readonly database」（热 journal recovery 需写权限，挂载盘写被 FUSE 拒）。

**根因**: 本脚本（2026-08-27 Doctor 令新增）顶部**无** `sys.path.insert(0, 项目根)` bootstrap（对照 `scripts/fetch_limit_list.py` L14 有）。`python3 scripts/xxx.py` 运行时 sys.path[0]=scripts/ 目录，`import config` ModuleNotFoundError → 被 `_db_path()` 的 `except Exception` 吞掉 → fallback `_docroot()` 沿父目录找到 `Database/.env` → 返回 **live 真盘** `market_data.db` → 挂载盘直写（GOTCHAS G019 同族）commit 必报 disk I/O error → 未提交事务 + 热 journal 残留。

**影响面**: ① live 库被未提交 REPLACE 事务部分写入（FRED 表 62 行无新观测，数据零损失）；② 热 journal 残留致后续任何打开 live 者（含本班放回前只读校验、句芒班、Mac 班）recovery 失败；③ 本班处置：先备份 live main+journal（`.bak_zhuzhao_20260827_prewrite` + `-journal`），staging 校验后原子 mv 换新 main，旧 journal park 为 `.STALE-20260827-zhuzhao-parked`，副本上以 `PYTHONPATH="$…/pylib-linux:$项目根"` 重跑 FRED 成功（exit 0）。

**建议修法**: `fetch_fred_ust.py` 顶部加同款 bootstrap（`sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))`）再 `import config`；并考虑把「import config 失败即 abort」改为不静默 fallback（或 fallback 前检查路径含 /sessions//mnt/ 即拒写，复用 connect_write 护栏）。

**预防门禁**: 新 scripts 上架前查「import config 前有无 bootstrap」；班内跑新脚本先 `python3 -c "import config; print(config.MARKET_DB)"` 确认指向副本根再放行。同族复发（另一脚本 fallback 直写 live）追记本条。

**来源**: 2026-08-27 zhuzhao 定时班实测 · agents/烛阴/logs/2026-08-27-行情拉取与日报.md · live 残留证据 `market_data.db-journal.STALE-20260827-zhuzhao-parked`

**追记 2026-08-31（同根第三次复发 · 通用教训坐实）**: 2026-08-31 zhuzhao 定时班第三次触发——`fetch_fred_ust.py` 无 bootstrap 直写 live market_data.db。与前两次不同：本次直写**成功**（未报 disk I/O error、未留热 journal，live integrity ok，fred_ust_daily 63→65 行）——挂载盘直写小事务可侥幸成功，比「报错留 journal」更隐蔽：若本班未察觉而用旧副本放回，live 的 FRED 新行会被回退 2 行（20260826→20260828 丢失）。本班处置：察觉后以 `PYTHONPATH="$pylib-linux:$项目根"` 在副本重跑 FRED 对齐（副本 20260828/65 行 = live 同值），放回无回退。三次复发坐实 2026-08-28 追记提出的通用教训升格：**任何无 bootstrap 直 `import config` 的脚本在班内必 fallback 直写真盘**——建议 Doctor 批一次扫修（grep 含 `import config` 且无 `sys.path.insert` 的 scripts）或 `_db_path()` 加写前路径护栏（含 `/sessions/` 即 abort，复用 connect_write）。条目状态维持 🔄 待修复，不自行闭环。

**来源（追记）**: 2026-08-31 zhuzhao 定时班实测 · agents/烛阴/logs/2026-08-31-行情拉取与日报.md · live fred_ust_daily 20260828/65 行（updated_at 2026-08-31 21:30 沙箱钟）

**追记 2026-09-01（同根第四次复发）**: 2026-09-01 zhuzhao 定时班第四次触发，模式回到初犯形态——`python3 scripts/fetch_fred_ust.py` 直写 live，`con.commit()` 报 `sqlite3.OperationalError: disk I/O error`（FRED 两序列 [ok] 打印后崩，exit 非 2 的优雅跳过而是事务崩溃），live 留 12824 字节热 journal（与 08-27/08-28 完全同尺寸同模式）。处置同 08-27 初犯：恢复验证（live main+journal 拷贝 /tmp 打开自动回滚 → integrity ok → 全表行数 vs 班前基线逐一相同 → 失败事务未污染主库，且真盘 main 指纹 md5 6d7432ff… 与快照时刻一致）→ journal park 为 `.STALE-20260901-zhuzhao-parked` → `PYTHONPATH="$pylib-linux:$项目根"` 绕行重跑副本成功（DFII10 +30 行至 20260828=2.42、THREEFYTP10 +25 行至 20260821=0.8682，净增 0 行=幂等重写）。**四次复发、两种病征（报错留 journal / 静默直写成功）全齐**：通用教训已从「应升格」到「坐实」再到「第四犯」，靠班内绕行只能止血不能断根——请 Doctor 裁一次根治（批扫修「import config 无 bootstrap」的 scripts，或 `_db_path()` 加写前路径护栏：路径含 `/sessions/` 或 `mnt/` 即 abort）。条目状态维持 🔄 待修复，不自行闭环。

**来源（追记）**: 2026-09-01 zhuzhao 定时班实测 · agents/烛阴/logs/2026-09-01-行情拉取与日报.md · live 残留证据 `market_data.db-journal.STALE-20260901-zhuzhao-parked`

---

## [ERR-20260828-001] SA 应急通道 QQQ 值写 code='NASDAQ'——与主路 ^NDX 同主键互覆风险（口径差 ~40 倍）

**状态**: 🔄 已修待验（2026-08-28 Doctor 裁「另立 code」（推荐项）→ 已改：`fetch_intl_index.py` SA 写入映射 `SA_WRITE_CODE={"NASDAQ":"NASDAQ_QQQ"}` + `gen_daily_report.py` 两处 QQQ fallback（主路 ^NDX 缺当日行时顶替并标注「主路^NDX缺·应急代理」）· 自验：py_compile 两文件 ✓ · /tmp 库副本跑真实 stockanalysis 分支 → 20260827 两列并存（NASDAQ=^NDX 29641.56 保留 + NASDAQ_QQQ=QQQ 530.5 独立写入）✓ · 实施者不自签）

**优先级**: 🟡 中（触发即污染：同主键 (trade_date,code) INSERT OR REPLACE → ETF 价混入指数点位列 → pct 链全废 + F1 外盘传导/展示栏读错量级）

**触发**: 2026-08-26 /todo 时发现 QQQ 值写入覆盖 ^NDX 行风险，Doctor 裁「并入 08-28 核验场一起裁」；2026-08-28 胜宏半年报核验场同场裁「另立 code」。

**硬证据/最小复现**: `scripts/fetch_intl_index.py` SA_SOURCES `"NASDAQ": ("QQQ", ...)` 写入 `code="NASDAQ"`（L~176 写分支）· 表 PK=(trade_date,code)（L67）· 主路 INDICES `"NASDAQ": ("^NDX", ...)` 同 code——SA 应急与 yfinance 主路同日同 code 即 REPLACE 互覆。两口径量级差：^NDX 指数点位 ~29,000 vs QQQ ETF 价 ~530（~55 倍）。DB 现状实读（2026-08-28）：最近 10 行全 ^NDX/source=yahoo，污染未兑现，属预防性根治。

**根因**: 08-25「QQQ ETF 代理退役·改指数本身」裁定只改了 yfinance 主路 symbol，SA 应急路（生产沙箱 yahoo 403 常态主路）仍以 QQQ 写同 code——两路同键不同口径的设计缺陷。

**修复**: 另立 code（输入契约不动：九儿班 JSON 键仍 "NASDAQ"）→ 库内 NASDAQ 主列永为指数口径、NASDAQ_QQQ 应急列独立；消费端 fallback 保应急可用性（gen_daily_report L512/L540 两处，INTL_US_INDEX/F1 semi_codes/_EP_SYM 三消费点键不变零改动）。

**预防门禁**: ① 代理/口径替代类取数（ETF 代理指数、期货代理）写库前必核「同 code 是否已有不同口径写入方」，口径不同即另立 code 或显式合并策略；② 同一 code 下 symbol/kind 语义变更时走 Doctor 裁定并在 note 记版本。

**来源**: 2026-08-28 胜宏半年报核验场（Doctor 裁「另立 code」）· fetch_intl_index.py L147-156/L203-218 · gen_daily_report.py L512/L540 · 自验脚本 outputs 级命令（/tmp 副本 · 20260827 两列并存断言）

**追记 2026-08-28（同根第二次复发 · 应升格通用教训）**: 2026-08-28 10:00 zhuzhao 定时班再次触发——`fetch_fred_ust.py` 直写 live market_data.db，commit 报 disk I/O error，live 留下 12824 字节热 journal（与 08-27 完全同尺寸同模式）。处置同昨日：恢复副本验证（live main+journal 拷贝 /tmp 打开自动回滚 → integrity ok → 全表行数与班前基线逐一相同 → 证明失败事务未污染主库），journal park 为 `.STALE-20260828-zhuzhao-parked`，`PYTHONPATH=$pylib-linux:$项目根` 绕行重跑成功（DFII10 +32 行至 20260826=2.34、THREEFYTP10 +29 行至 20260821=0.8682）。同族二犯，按治理合同应升格通用教训：任何 scripts/ 下直接 `import config` 的脚本在 `python3 scripts/x.py` 形态运行时 sys.path[0]=scripts/，无 bootstrap 必 fallback 直写真盘——建议 Doctor 批一次扫修（grep 无 bootstrap 的脚本）或加 commit 前写路径护栏。条目状态维持 🔄 待修复，不自行闭环。

**来源（追记）**: 2026-08-28 zhuzhao 定时班实测 · agents/烛阴/logs/2026-08-28-行情拉取与日报.md · live 残留 `market_data.db-journal.STALE-20260828-zhuzhao-parked`

**追记 2026-09-02（历史口径混合 · 复发扫描新发现 · ⚠️ 已知风险）**: 句芒 09-02 审核班复发扫描扩查发现 `intl_index_daily` code='NASDAQ' 序列为**历史口径混合**——`20240102→20260812` 共 655 行 QQQ ETF 尺度（close 396.28~724 · source=yahoo · 系 08-25 裁定前「QQQ 代理」设计遗留），`20260813→20260901` 共 14 行 ^NDX 指数尺度（~29,000+）。**断点 20260813**：跨断点的任何时间序列/分位/回测研究将遭 ~40-70 倍跳变污染。本条「污染未兑现」仅对 08-28 修复后的新增行成立，对历史序列不成立。历史处置（重标口径/另立 code/归档旧段/加版本注记）属 Doctor 裁定——本班只读观测、不动库。另注：数据断点 20260813 早于 GOTCHAS 所记裁定日 08-25，切换实际执行日待核。

## [ERR-20260830-001] config.py 的 RAW_RECAP_DIR 从 DATABASE_ROOT 派生——误设 env 时漂移，record --all-new 静默扫空返回 0

**状态**: ⚠️ 已知风险（正常路径 Mac 原生不设 env、照旧向上找 Documents，不触发；仅人为设 `ZZJY_DATABASE_ROOT=/tmp/…` 时踩 · 待 Doctor 批修或裁定「输入目录独立 env」方案）
**优先级**: 🟡 中
**触发场景**: ingest 工作流设 `ZZJY_DATABASE_ROOT=/tmp/dbroot` 做隔离操作时，config.py 的 RAW_RECAP_DIR 随 DATABASE_ROOT 派生漂移至 /tmp 下不存在路径 → scan 扫空 → `record --all-new` 返回 0，误判「无新课件」。
**硬证据/最小复现**: 九儿 2026-08-30 ingest 日志（`agents/烛阴/logs/2026-08-30-课件入库.md`「过程备注」）：`ZZJY_DATABASE_ROOT=/tmp/dbroot` 后 record --all-new 首次返回 0；解法为 `ln -s` 真 Raw-Recap 至 /tmp/dbroot/烛照九阴/Raw-Recap 后 record 成功（260830 入库 17 条）。
**根因**: config.py 中 RAW_RECAP_DIR 系从 DATABASE_ROOT 派生（输入目录与输出目录未解耦）——输入侧（Raw-Recap 源文件）本应固定指真实库目录，不应随输出侧 env 漂移。
**影响面**: 只影响「误设 env」场景；不损坏数据（scan 扫空只是少处理，processed_kejian 未登记 → 下一班会补）。危险点在于**静默**：返回 0 无报错，若不看日志会漏判为当日无课件。
**修复/建议修法**: ① config.py 支持独立 env（如 `ZZJY_RAW_RECAP_DIR`）或 RAW_RECAP_DIR 默认值不依赖 DATABASE_ROOT；② record 命令在 scan 0 文件且 Raw-Recap 目录非空时告警（fail-loud）。
**预防门禁**: 任何「设 env 做隔离」的操作前，先确认输入路径是否随该 env 派生；scan 结果为 0 时对照目录 ls 再下「无新课件」结论。
**来源**: 2026-08-30 句芒审核班（转记自九儿 2026-08-30 课件入库日志「过程备注」· 九儿已建议登记，本班代登记，状态不自标 ✅）

## [ERR-20260901-001] 大盘涨跌幅用 510300 ETF 代理——连续三日与沪深300指数偏离 0.2pp+ + 显示 1 位小数抹平微跌

**状态**: 🔄 已修待验（2026-09-01 Doctor 裁「换指数真身」→ 实施：`scripts/fetch_index_daily.py` 新建（tushare index_daily 000300.SH → `cn_index_daily` 表）+ 内嵌进 `fetch_theme_etf.py`（同批原子拉取·班 prompt 零改动）+ `gen_daily_report.py` 快照/大盘曲线改读指数表（`IDX`）+ bench_note「沪深300指数」+ `pct_span` .1f→.2f。验证：负向（无表→「待取数」fail-closed·exit 0）+ 正向（/tmp 镜像灌真实值→快照 -0.30%·产物零「代理/510300」残留）。**实施者不自签**——待独立验收；回填与重生成命令已贴 Doctor 终端）

**优先级**: 🔴 高（日报首页市场快照直接误导：-0.0% 显示 vs 大盘真实 -0.16%~-0.30%；主线超额/板块图同源失真）

**触发**: 2026-09-01 Doctor 发现日报「大盘涨跌幅 -0.0% 沪深300代理」存疑。

**硬证据/最小复现**: 20260901 收盘——`theme_etf_daily` 510300.SH pct_chg=-0.02（tushare fund_daily 实拉复验一致·腾讯行情接口复验 close 4.684 无误）vs tushare index_daily 000300.SH pct_chg=-0.2951（华尔街见闻/汇通财经多源一致：沪深300 -0.30%·上证 -0.16%）。连续三日偏离：08-28 0.20pp / 08-31 0.21pp / 09-01 0.28pp。显示层：`pct_span` `{v:+.1f}` 把 -0.02 抹成「-0.0%」。

**根因**: ① 快照与大盘曲线用 ETF 市价代理指数——ETF 二级市场折溢价波动致代理失真（偏离根因未完全查明·疑似 510300 折溢价波动，如实标未核）；② 显示 1 位小数对 ±0.05 内的小幅波动产生「-0.0%」负零误导。

**影响面**: 日报首页「市场快照」与板块卡「大盘」曲线；主线超额基准（BENCHMARK ETF）口径未动——超额是「板块 ETF vs 大盘 ETF」同口径横向比较，保留 ETF 属有意设计（改动注释已写明）。

**修复**: 见状态行。回填：`python3 scripts/fetch_index_daily.py --from 20240101`（Doctor 终端·供曲线 20 日窗口）；此后每日班随 fetch_theme_etf 自动增量。

**预防门禁**: ① 代理/替代口径类取数（ETF 代理指数）上岗前必做真值偏离校验（如 |代理 pct − 真值 pct| > 0.1pp 即告警）——与 ERR-20260828-001 预防门禁同族（代理口径类二犯，应升格通用教训由 Doctor 裁）；② 展示层百分比禁 1 位小数（小值抹平/负零）；③ 快照与同页曲线必须同源同口径（防「-0.30% vs 曲线末点 -0.02%」自相矛盾）。

**来源**: 2026-09-01 本场（Doctor 提问 → 实拉 tushare fund_daily/index_daily + 腾讯行情 + 外部多源核对 → Doctor 裁「换指数真身」→ 实施+双向测试）
