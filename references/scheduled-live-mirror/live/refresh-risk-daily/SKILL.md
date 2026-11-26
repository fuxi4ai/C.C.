---
name: refresh-risk-daily
description: 每日刷新「风险日报」artifact（FedWatch 会前槽自动取数 → fetch TACO 外部分项·禁代理 → 星空快照新鲜度探针 → V2.5-ET双波 仓位信号 → 股权溢价指数原子 → 股票供给增发预案补额（尽力而为·缺额即不可计算） → AI Tech Alarm 事件源定向回源更新（四维度 P0/P1·未核保留）→ prepare V17 包→model_entry DeepSeek 判读→build 校验落盘·失败回退标陈旧）→ update_artifact；挂载盘 SQLite 一律走 /tmp 副本回写
---

每日刷新「风险日报」artifact。自包含步骤：

0. （FedWatch 会前槽自动取数）用 WebSearch 查最新 CME FedWatch 读数——中文一轮（如「CME 美联储观察 加息25个基点概率 维持利率不变概率」+ 当月会议月份词），英文一轮（如「CME FedWatch FOMC rate hike probability」+ 当月会议时间词）；必要时 WebFetch 打开 1-2 个源原文核实（金十 flash / 格隆汇 / 证券之星 / Investing / Nasdaq 等财经媒体转述的 CME 官方读数）。规则：
   - **双源对拍**：≥2 个独立源读数一致（对应档位差 ≤5pp）才写；仅 1 个源或源间冲突 → 不写，输出一行「FedWatch fetch skipped: 原因」。
   - **新鲜度护栏**：最新读数的 as_of 若不新于槽内 as_of（周末/节假日无新读数属常见），跳过不写，输出「FedWatch skip: 无更新（槽内 as_of 已最新）」。
   - **写盘**：先读 `~/Documents/Claude/Projects/Financial/风险日报/fomc_market_exp.json` 现状；只更新 `p_hike` / `p_hold` / `p_cut` / `as_of` / `source` 五个字段；`note` 的**人类叙事段保留不动**，仅在尾部追加一行「🤖 自动取数 YYYY-MM-DD: hold X% / hike Y% / cut Z% · 源A/源B」；机器行只增不删、保留最近 5 行、超出截断最旧机器行。`meeting` / `outcome` / `outcome_note` / `_usage` 一律不碰。
   - 三档数字必须合计 ≈100；**绝不编数**。source 注明「自动取数·多源转述」口径。
   - 写盘后回读 JSON：可解析、三档合计 100、as_of 已前进，才算完成。

1. （TACO 代理·尽力而为）在沙箱跑 TACO 外部分项取数：`python3 ~/Documents/Claude/Projects/Financial/风险日报/scripts/fetch_taco_components.py --fetch`（拉 FRED 房贷 MORTGAGE30US / 汽油 DGASUSGULF·GASREGW / 通胀 EXPINF1YR·T10YIE + VoteHub 特朗普净支持率 → 落 data/taco_components.db，供下一步 build 算 TACO 原子的 6 分项代理 pain）。**不要加 HTTPS_PROXY / HTTP_PROXY=http://localhost:3128**——2026-07-31 实测该端口无人监听，带上必 Connection refused；api.stlouisfed.org 与 api.votehub.com 在沙箱内直连可达。**取不到/超时/报错就记一行「TACO fetch skipped: 原因」并跳过**，绝不阻塞后续构建、绝不编数；build 会自动用已有数据算 N/6 代理并诚实标注分项数。

1.5. （星空快照新鲜度探针 · 2026-09-16 Doctor 批装 · 2026-09-17 双路径修复+复核门禁 · GOTCHAS ERR-20260916-001）在沙箱跑 `python3 ~/Documents/Claude/Projects/Financial/风险日报/ops/check_starfield_freshness.py`——读 EAL_STARFIELD.html 内嵌快照的 market_as_of，与 XNYS 冻结日历的「最近已收盘交易日」比对，落后 >1 个交易日即告警（检测滞后从周巡检 7 天缩到 1 天）。探针已修双路径（Mac 原生 HOME/Documents 优先 + 沙箱 /sessions/*/mnt/Documents glob 兜底·多残留取最新，同 r7_yen_watch.py 款），正常时沙箱输出即真值。输出 `STARFIELD_FRESH=OK …` 才无事；`STALE` / `MISSING` / `UNPARSEABLE` / `NO_CALENDAR` / `UNKNOWN` 任一 → **先复核再报**：先用 Glob/Read 文件工具实核 Mac 侧路径 `~/Documents/Claude/Projects/Financial/Event-Attribution-Ledger/backtest/EAL_STARFIELD.html`（独立于沙箱挂载通道）——文件实存而探针异常，则系挂载/通道问题，记「探针异常·复核实况 OK」不红字（2026-09-16/17 两次 MISSING 均为此类伪报）；确认真异常（文件实缺/STALE/UNPARSEABLE 等）才在当日简报首行红字「⚠️ EAL 星空快照异常：{探针输出原文}」报 Doctor。**本检查非阻断**（恒 exit 0）——星空快照停更不等同风险数据停更，日报本体继续构建，绝不因探针结果跳过后续步骤。

1.6. （V2.5-ET双波 仓位信号 · 2026-10-15 Doctor 裁「更新集成入 Risk Daily」· 项目接入补丁正式应用）在沙箱跑：
   export MARKET_DB="$(ls -d /sessions/*/mnt/Documents/Database/Market-Data/market_data.db 2>/dev/null | head -1)"
   python3 ~/Documents/Claude/Projects/Financial/剑酒青丘/仓位管理策略/tools/collect_v25_et_inputs.py
   python3 ~/Documents/Claude/Projects/Financial/剑酒青丘/仓位管理策略/tools/v25_et_daily_signal.py
   - 链：最小采集（只读行情库 cn_index_daily:000688.SH＋SSE 官方日历 → inputs/v25_et_daily/market.json）→ 日更信号（T主E辅、E不否定T → outputs/v25_et_position_signal.json，风险日报「仓位」卡片数据源）。
   - 失败语义：任一步 rc!=0 → 记一行「V2.5 仓位信号 skipped: 原因」，**当日简报首行红字报 Doctor**（仓位卡片数据源停更，卡片自降级「信号不可用」），继续后续构建；绝不编数、绝不用旧值冒充当日信号。
   - 只读公共数据库、只写 仓位管理策略/inputs|outputs 下文件；重跑无害（信号 generated_at 会前进）。
   - E 证据（inputs/v25_et_daily/external_evidence.json）人工维护，本班不写入；缺失/过期时信号器自动退回 E=UNKNOWN，不阻塞 T。
   - calendar 缓存复用 inputs/v25_et_daily/market.json 内日历；缓存过期需 Tushare trade_cal（与市场班同通道）；行情库无当日 KS50 → collect fail-closed（市场班 fetch_ks50_index 每日维护）。
   - ⚠ 提示器已退役归档（2026-10-13）；V1 信号工具保留为历史文件，本班不再跑。

1.7. （股权溢价指数风险原子 · 2026-10-20 Doctor 令「注册进 Risk Daily」· 日频拼接口径）在沙箱跑：
   pip3 install --break-system-packages --quiet tushare akshare pandas 2>&1 | tail -1
   python3 ~/Documents/Claude/Projects/Financial/风险日报/fetch_erp_atom.py
   python3 ~/Documents/Claude/Projects/Financial/风险日报/render_erp_detail.py
   - 链：fetch 取 Tushare 沪深300 PE_ttm＋akshare 中国10Y（降级链：akshare→中债官网→前值+陈旧标记）→ 乐咕月频历史（2005-04 起）×1/1.04 校准 → 60 月滚动分位 → 两把尺分数（相对尺：分位 50/25/0 记 0/75/100 分；绝对尺：溢价 4.7/2.8/−2.48 记 0/75/100 分；取较大；不进综合温度；取数陈旧、文件生成超过 6 小时、取数日落后于行情库时不出分并写明原因）→ data/erp_atom.json；逐日留存追加到 data/erp_atom_history.jsonl；render 生成 dashboard/erp_atom_detail.html（第四标签页「股权溢价指数」srcdoc 源）。
   - 失败语义：取数内部自动降级（前值+陈旧标记）不红字；两脚本任一 rc!=0 → 记一行「ERP atom skipped: 原因」，当日简报红字报 Doctor，**绝不阻塞后续构建**；卡片与详情页自降级（「数据不可用」/前值陈旧标记）。
   - 只写 风险日报/data/erp_*.json|.csv、data/erp_atom_history.jsonl（逐日留存：只追加，同一取数日只留一条）与 dashboard/erp_atom_detail.html；重跑无害（generated_at 前进；同日重跑不重复写留存）。dashboard/erp_atom_detail.html 首行记着所用 erp_atom.json 的 as_of 与 generated_at；第 3 步构建器嵌图前比对，不同份就自己重跑一次 render 重写这个文件，仍不同份或 render 出错则第四页不放曲线图、写明原因，不放旧图（2026-11-26 · GOTCHAS ERR-20261126-001）。所以本步 render 失败时，第 3 步仍会再画一次。
   - 另：第 3 步构建器本身另外会读写 `data/erp_zone_alerts.jsonl`（股权溢价分区提示的已提示记录，只追加）。
   - pip 安装耗时约 1-2 分钟属正常；装失败 → 记「ERP atom skipped: pip 失败」并继续。
   - 沙箱直连 Tushare/akshare，勿设代理（与市场班同通道；akshare 走英为财情）。

1.8. （股票供给 · 增发预案补额（尽力而为）· 2026-11-20 Doctor 令「股票供给接入日报」· 生产接入登记第二项；**2026-11-24 Doctor 改按首次公告日计入**）在沙箱联网检索，产出增发读数文件，供第 3 步构建器（`build_risk_daily.py` 自己调用 `stock_supply.py`）读取。数据日＝公共行情库 `daily_market` 有成交额的最新交易日（北京日期，yyyymmdd）；**本期**＝上一个交易日之后（不含）至数据日（含）的自然日（周一的本期含上周六、周日）。
   - 背景：增发不再按申购日计，改按预案首次公告的那天、按预案写明的募集资金总额上限计。构建器自己用 Tushare `stk_seasoned` 列出本期首次公告的预案；约三成新预案在 Tushare 里没有拟募资额，本步就是从预案公告里把金额读出来补上。本文件里有、Tushare 还没列进来的预案，构建器也按本文件的标注计入（补 Tushare 入库滞后）；Tushare 取不到时，构建器改用本文件的列表（这时须 `coverage: "complete"`）。
   - 可选的捷径：本沙箱能直连 Tushare（令牌同第 1.7 步），可先用 `stk_seasoned`（`start_date`＝本期首日、`end_date`＝今天，再按 `first_ann_date` 落在本期筛）查出 `fo_raise_total` 为空的那几笔，优先补它们；查不了就按下一条把本期新预案都检一遍。
   - 检索：联网检索本期首次公告的上市公司向特定对象发行股票预案（董事会决议公告、「向特定对象发行股票预案」）。可查的出处：巨潮资讯、上交所、深交所、北交所公告。查询词举例：「向特定对象发行股票预案 <日期>」「董事会决议 向特定对象发行 募集资金总额不超过」。修订稿、更新稿不是首次公告，不记。
   - 每找到一笔，记下：代码（`ts_code`，必须写成 6 位数字加 `.SH`／`.SZ`／`.BJ`，如 688000.SH）、公司、首次公告日（`first_ann_date`）、预案写明的募集资金总额上限（元，`est_amount_yuan`）、出处链接。
   - 计入与否（与构建器同一口径，只计拟募资超过 10 亿元的竞价发行）：发行对象写「不超过 N 名」或只写「特定对象」「符合规定的投资者」的，标 `counted: true`（大股东参与竞价的也按全额计）；以下标 `counted: false` 并写明原因（`exclude_reason`）：发行对象是写明的具体单位或个人（锁价发行）；认购方含财政部；简易程序（含年度股东大会的「提请授权以简易程序发行」）；以资产认购。拟募资不超过 10 亿元的不计（Doctor 2026-11-24 定），但这条由构建器按金额判：竞价预案不论金额大小都照常标 `counted: true` 并写金额，不要因为金额小就标不计或不写。标不计的那几类也尽量写上金额：构建器按 Tushare 字段判计入与否，Tushare 若把它判成竞价又缺金额，就拿这里的金额补。
   - **首次公告金额未定（2026-11-26 Doctor「改在首次披露金额之日计入」· 风险日报 GOTCHAS NOTE-20261126-003）**：预案原文写明募集资金金额「尚未确定」（常见于重大资产重组的募集配套资金，只写「不超过交易对价的 100%」之类公式）的计入型预案，写一笔 `counted: false`、`amount_undetermined: true`、不写 `est_amount_yuan`（或写 null），`exclude_reason` 摘录原文里「尚未确定」那句，附出处；构建器当日按「首次公告未定金额，待首次披露金额之日计入」不计。只给 Tushare 没有金额的那笔这样写（Tushare 已有金额的按它计入首次公告日，不进 pending，以后也不写披露事项）。同时把它追加进 `~/Documents/Claude/Projects/Financial/风险日报/data/supply_amount_pending.json`（JSON 数组，每项 `{"ts_code","name","first_ann_date","sources"}`，同代码同首次公告日不重复追加；整文件 truncate 覆写）。
   - **往期未定金额、本期首次披露金额**：每天先读 `supply_amount_pending.json`，逐笔检索它是否在本期首次披露了募集资金金额（重组报告书（草案）、发行方案修订稿等写出具体上限的公告）。披露了就在读数里写一笔：`first_ann_date` 写原首次公告日（在本期之前），`amount_disclosed_date` 写首次披露金额的公告日（必须落在本期），`counted: true`，`est_amount_yuan` 取原文写明的上限，附出处；在 pending 里给这笔加 `"disclosed_date": "YYYYMMDD"`，**先不删**——同一数据日重跑时照样按它写读数；等以后某天的数据日已晚于 `disclosed_date`，再把它从 pending 删掉。本期 Tushare 已为同一代码新列出带金额的预案行、且对应的就是这次披露的，不写披露事项（免得计两次）。某天没跑、披露日落在了已过去的数据日：不补计，在 pending 里给这笔加 `"missed": "<原因>"` 并保留，交 Doctor 看。没有披露的留在 pending 里。终止的直接从 pending 删掉、不写读数。
   - 只有能说明本期首次公告的预案都已列出时才写 `coverage: "complete"`；否则写 `"incomplete"`，并在 `gaps` 里写明缺什么。coverage 只在 Tushare 取不到时才起作用；补金额不看它。**不确定就写 incomplete，不编数；金额只取预案原文写明的上限，读不到就不写这一笔。**
   - 写盘：`~/Documents/Claude/Projects/Financial/风险日报/data/supply_placement_reading.json`，一次整文件覆写，**不用临时文件改名**（见第 5 节：挂载盘只许 truncate 写，不许 rename/unlink）；写完回读一遍，确认 JSON 能解析、`data_date` 是当天的数据日。构建器只认数据日相同、生成于 24 小时内、`schema` 为 v2 的这份文件；**任何一笔的代码写法不对、首次公告日不在本期（带 `amount_disclosed_date` 的那种例外：首次公告日须在本期之前、披露日须在本期）、没有出处、没标计入与否，或标为计入却没有正数金额；`amount_undetermined` 写了却不是 `true`、或同时标计入、带金额；`amount_disclosed_date` 不在本期、或那笔没标计入、没带金额、又写了 `amount_undetermined`；同一代码同一首次公告日的披露事项写了不止一笔——整份文件都不用**（披露事项不要写 `amount_undetermined` 字段，写 false 也会作废），所以拿不准的那笔宁可不写。
   - 读数文件格式（`schema` 必须原样；下例中的代码与金额只示意字段写法，不是行情）：
     ```json
     {
       "schema": "supply_placement_reading/v2",
       "data_date": "20261124",
       "generated_at": "2026-11-24T09:05:00-08:00",
       "coverage": "incomplete",
       "gaps": "巨潮当日公告未检完",
       "searched_sources": ["巨潮资讯 本期公告检索：向特定对象发行股票预案、董事会决议公告"],
       "items": [
         {"ts_code": "000000.SZ", "name": "示例", "first_ann_date": "20261124", "est_amount_yuan": 1500000000,
          "basis": "预案公告拟募资上限", "counted": true, "sources": ["https://..."]},
         {"ts_code": "000001.SZ", "name": "示例二", "first_ann_date": "20261124", "est_amount_yuan": 800000000,
          "counted": false, "exclude_reason": "锁价发行（发行对象为控股股东）", "sources": ["https://..."]},
         {"ts_code": "000002.SZ", "name": "示例三", "first_ann_date": "20261124", "est_amount_yuan": null, "amount_undetermined": true,
          "counted": false, "exclude_reason": "重组配套募资，预案写明募集配套资金金额尚未确定", "sources": ["https://..."]},
         {"ts_code": "000003.SZ", "name": "示例四", "first_ann_date": "20261020", "amount_disclosed_date": "20261124",
          "est_amount_yuan": 3000000000, "basis": "重组报告书（草案）首次披露的募集配套资金上限", "counted": true, "sources": ["https://..."]}
       ]
     }
     ```
   - 失败语义：检索不可用就不写文件（或写 incomplete），记一行「股票供给增发补额 skipped: 原因」，继续后续构建。Tushare 金额齐全的日子不受影响；有一笔该计的预案缺金额时，构建器把增发写成缺口、分数显示「不可计算」，**不阻塞日报**。
   - 另：第 3 步构建器构建时会用 Tushare 取当期减持预案（只读；取不到或返回的表缺列都写「减持资料不足」，不阻塞），取到的原始行追加进本机文件 `data/supply_reduction_plans.jsonl`（不入库）。本步不执行这些，只写上面的读数文件。

2. （AI Tech Alarm 事件源定向回源更新 · 信息自纠正第一步 · 2026-11-03 四目标优化接入）在沙箱：
   - 先读 `~/Documents/Claude/Projects/Financial/风险日报/data/narrative_events.json`（四维度：demand/returns/funding/delivery）逐事件核对 `next_check_utc` 是否已到期/三日内到期，再按四维度观察点定向 WebSearch 回源 P0/P1（机构评论用于选指标，公司/交易披露确认事实）：现金回报→大云财报/FCF/折旧指引；融资信用→发债定价与交割、OpenAI first close、Anthropic IPO、CoreWeave 再融资；付费需求→云收入/合同转收入；交付→可计费容量/交付延期。
   - **核到新事实或反证（P0/P1 可读源）才更新事件层**：新事件追加（event_id 唯一）、事实/时间/生命周期（developing/confirmed/cleared）更新、同一风险命题的新一代以 supersedes 覆盖旧代；更新后立即跑 `python3 ~/Documents/Claude/Projects/Financial/风险日报/narrative_score.py` 自检校验。**未核到合格源 → 原事件一字不动**，输出一行「事件源更新: 本轮无新 P0/P1 事实」。
   - **单名 CDS 报道读数（2026-11-26 Doctor 令「加进定时班」· 调研见 `~/Documents/Claude/Projects/Financial/风险日报/docs/2026-11-26-单名CDS数据来源-调研.md`）**：回源 funding 维度时，对甲骨文（Oracle）、CoreWeave、Meta 三家，顺带检索媒体报道里**写明数据商**的 5 年期 CDS 读数（如「据 Reuters，S&P Global Market Intelligence 数据」「Bloomberg 引 ICE Data Services」）。有新读数才登记，照下条 v4 合同与现有先例 `crwv-cds-peak-1015` 的写法：`fact_status: occurred`、`evidence_basis: market_data`、至少一条 `access: read` 的 P1 来源；`claim` 写「据〈媒体〉转述，〈数据商〉数据」，带观察日期与单位 bp；`facts` 注明盘中还是收盘，分不清就写「口径未注明」；峰值写明是峰值，不冒充当前值；同一天两家报道数字不同，两个都记、不取平均；只读到转载页时 `locator` 注明「转载」。**禁止**：直接读取或抓取 ICE、Markit 等数据商的报价页面（其条款禁止程序取数与复制）；把 CDS 读数当作 `spread_evidence`（债券利差口径，CDS 与债券之间有基差）；为凑序列补登没有新报道的日子。读数只进事件层，由模型评估时参考，不设单独的计分门槛。
   - **v4 事件登记合同（2026-11-08 Doctor 批 · 违反即被校验剔除、整次评分回退）**：新事件必须按 `~/Documents/Claude/Projects/Financial/风险日报/docs/事件登记合同-v4.md` 填 `fact_status`（occurred/forecast/contingent）；occurred 必填 `evidence_basis`（primary/market_data/report），report 型 claim 写「据〔源〕〔日期〕报道：…」，market_data 须注明数据来源（ICE/Tradeweb/交易所/发行公告/评级机构）；forecast 型 claim 写「〔谁〕于〔日期〕发布…」；contingent 必填 trigger_condition/lands_in/next_check_utc/on_expiry。融资维违约/重组、头部实验室融资确认失败、投资级借款人恶化按合同标 `transmission_channel`。一个源材料含多个原子事实时**拆成多条**并共享 family。写入后跑 `python3 ~/Documents/Claude/Projects/Financial/风险日报/narrative_score.py` 自检，errors 非空不得进入步骤 3。
   - **投资级恶化细分与利差证据（2026-11-10 Doctor 批）**：标 `transmission_channel: ig_deterioration` 的事件必须同时填 `ig_signal`——`rating_action`（评级/展望下调）、`issuance_pulled`（发债撤回/缩量）、`issuance_concession`（发债明显让价）、`spread`（利差相对 BBB 指数走阔）。缺填不报错，但该事件不算传导通道。
   - **利差型（`spread`）须附 `spread_evidence`**：`{instrument, maturity_years（8–12 年）, source, observations: [{date, spread_bp, index_oas_bp}] 连续 ≥5 个交易日, baseline?}`。`index_oas_bp` 取 `~/Documents/Claude/Projects/Financial/风险日报/data/bbb_oas.json` 同日值（FRED BAMLC0A4CBBB，不得自估）；利差取可读一手源（TRACE/发行公告/评级机构/交易所）。阈值：每日「利差 ÷ 指数 ≥ 2」或「(利差 − 指数) 较 92 天内 baseline 多走阔 ≥ 100bp」，连续 5 日。凑不齐 5 个交易日的数据就不标 `spread`，不得补估。**让价型（`issuance_concession`）须附 `issuance_evidence`**：`{instrument, source, date, spread_bp, index_oas_bp, maturity_years, prior?}`，门槛＝新发利差 ≥ 同日指数 2 倍，或较该发行人上一笔同期限（±2 年）发行多走阔 ≥ 100bp；利差取发行公告/424B2。自检后看快照 `ig_channel_checks` 确认是否生效。
   - contingent 事件若本轮核到一手官方文件（法案 bill number、FCC 文件、规则原文）→ 按政策阶梯改为 occurred·policy_stage=proposed（或更高），不得继续挂在提示区。
   - **范围只限 narrative_events.json**；绝不碰 `~/Documents/Claude/Projects/Financial/风险日报/alarm/` 下的 `legacy/`（冻结输入）、`current.json`、`revisions/`。

3. 运行后端构建脚本（含 AI Tech Alarm 四维度模型复核）：在沙箱跑
   python3 ~/Documents/Claude/Projects/Financial/风险日报/narrative_review.py prepare review-input.json
   python3 ~/Documents/Claude/Projects/Financial/风险日报/build_risk_daily.py --review-command ~/Documents/Claude/Projects/Financial/风险日报/model_entry.py --review-model deepseek-chat
   - prepare 生成 V17 模型复核输入包（绑定事件哈希/revision 身份/行情收盘/市场哈希）；build 自动调模型入口（stdin 读包 → DeepSeek API 判读 → stdout 出评估回包）→ 严格校验（绑定/时点/引用/权重）→ 落盘评估 → 评分 → 生成 dashboard/risk-daily.html + data/risk_snapshot.json。
   - 失败语义：模型入口失败/超时/回包校验拒绝（倒签、缺字段、引用非法等）或 KG_API_KEY 不可得 → build 自动回退保留上次有效评估并显著标陈旧（fail-visible：_review_errors/stale_fallback 注记在场），**不阻塞日报，保留这次带复核 build 的产物**；**禁止再跑无参 build 覆盖**（无参会清掉本轮失败注记）。
   - 若脚本报错或某原子缺数据，如实贴出错误，**不要用旧数据蒙混、不要编造温度**。
   - **读数库写入检查（2026-11-26 Doctor 令「改线上班」· GOTCHAS ERR-20261125-002）**：build 跑完后在沙箱跑
     `python3 -c "import json,os,datetime as d;r=json.load(open(os.path.expanduser('~/Documents/Claude/Projects/Financial/风险日报/data/risk_snapshot.json'))).get('readings_store') or {};b=r.get('build_id');m=round((d.datetime.now(d.timezone.utc)-d.datetime.strptime(b,'%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=d.timezone.utc)).total_seconds()/60) if b else None;st=r.get('status') if r.get('status')!='ok' or (m is not None and m<=120) else 'stale';print('READINGS_STORE=' + str(st) + ' · ' + str(r.get('reason') or ('写库 %s，距今 %s 分钟，累计 %s 次构建' % (b, m, r.get('builds')))))"`
     输出以 `READINGS_STORE=ok` 开头才无事；其余任何结果（`unavailable`、`None`、`stale`＝写库时刻距今超过 120 分钟或没有写库时刻，多半是本轮 build 没写出新快照、读到的是上一轮的；快照读不出）→ **当日简报首行红字「⚠️ 读数库本轮没有写入：{输出原文}」报 Doctor**。原因里出现「构建器不在生产目录」说明项目被搬动或改名，**不要设 `RISK_DAILY_READINGS_DB` 或 `RISK_DAILY_DOCUMENTS_ROOT` 去绕过门禁，也不要重跑 build 补写**，只报告。本检查不阻断：照常做第 4 步发布。

4. 更新 artifact：调用 `mcp__cowork__update_artifact`，id='risk-daily'，html_path='/Users/lunarabbit/Documents/Claude/Projects/Financial/风险日报/dashboard/risk-daily.html'，update_summary 写「当日综合风险温度 {值} {带} · {日期}」。

5. 纪律：
   - 数据真实性铁律（温度全部来自脚本读的真实一手值，无估算冒充）；risk_overlay_not_alpha——只出风险读数，**不出任何交易/仓位/方向建议**。⚠ 仓位卡片属既有例外（Doctor 2026-10-10 令：卡片自带「仅供参考，不构成投资建议」免责标注，只呈现、不做任何方向断言以外的加工）。股权溢价指数原子同纪律：只出读数、历史分位档位与两把尺分数（分数不进综合温度），不做方向断言。
   - **挂载盘 SQLite 铁律（2026-07-31 事故后立）**：`~/Documents` 是 FUSE 挂载，**不支持 unlink**（实测 EPERM）。SQLite 回滚日志的原子提交点正是删除 `-journal`，所以在挂载盘上直接开 rw 连接（`sqlite3.connect(path)` 不带 `mode=ro`）必然 `disk I/O error`，并留下 hot journal，反复累积即 `database disk image is malformed`（07-27/28/29 连续三天损坏的根因）。
     → 任何写库一律「拷到 /tmp 本地副本 → 在副本上 rw → 自检 integrity ok → 整库覆写回挂载」（truncate 写允许，rename/unlink 不允许）。fetch_taco_components.py 已按此改造（`_stage()` / `_commit_back()`）。纯 `mode=ro` 读挂载盘是安全的，无需改。
   - 若发现 `data/` 下残留 `*-journal` 文件，说明有人绕过了上一条：**报告给 Doctor，不要自行删**（沙箱也删不掉），并在当日输出里标明。
   - 卡面分项标注必须与实际参与数对账：`source` 里的「N/6分项参与」要等于 `taco_pain_from` 的复刻 N，被陈旧护栏剔除的分项须在「本次未参与」里点名。**禁止让缺席分项在花名册里冒充在场。**

跑完更新即可，无需额外分析或消息。