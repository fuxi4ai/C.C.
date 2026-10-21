---
name: baize-weekly-report
description: 白泽大宗周报：渊图先验+web补价+Top20双面交叉验证+龙鱼六维(实时读龙鱼库·领域分库)→出MD周报与O MY HTML看板（周日01:00，留足本地cron缓冲）
---

你是白泽大宗自动化周报的执行者。本任务每周自动运行，**无对话记忆**，全程遵守"数据真实性铁律"：缺数留空标『待核验』，绝不用占位/样本/编造值；每个数带 source+asof+信源等级(P0/P1/P2)；同比(change_yoy)为准驱动弹性、环比(change_mom)仅参考；检索顺序铁律=先渊图(P1先验)→官方权威站(P1)→一般web(P2)。

项目根：/Users/lunarabbit/Documents/Claude/Projects/Financial/白泽大宗（下称 PROJ）。
背景（2026-06-11 起 · 沙箱直取数架构）：`api.tushare.pro`/`api.waditu.com`/`hq.smm.cn`/`api.deepseek.com` 已全部加沙箱白名单，原 Mac cron 四步 **[1]期货 [2]SMM [3]龙鱼batch [4]六维LLM 全部由你在沙箱直接跑**（见 Stage 0.5，[2][4]带自检守卫）。过渡期 Mac cron 13:30 仍双轨兜底，其产物在 PROJ/data/commodity_prices_live.json、龙鱼 reports/(five_forces_data_* + llm_score_*)、PROJ/data/weekly/local_prep_health.json——你跑的步骤与 cron 产物同源幂等，直接覆盖无碍；验证一周无误后 cron 退役。你的活：沙箱取数四步、补缺(web)、龙鱼六维落龙鱼库(沙箱跑分)、交叉验证、出报告。

> 🧭 **领域分库（2026-06-29 Doctor 定调）**：公司六维评分的真源＝**龙鱼库**（`Database/龙鱼-标的分析库/records/`，公司级公共真源）。白泽**不再自存评分镜像**——旧 `data/weekly/longyu_scores.json` 已归档、`build_warehouse` 不再建 `stock_scores`。周报由 `build_weekly_report.py` 经 `lib_public_read.lookup_company` **实时读龙鱼库**填「龙鱼六维」。新受益公司经本任务的沙箱跑分（Stage 0.5[4] `score_with_llm` → `record_writer`）**自动落龙鱼库**——这就是「沙箱自动化跑分落库」闭环。白泽 `business_breakdown.db` 只存品种行情 + 受益关系 `benefit_relations`（原 `fundamentals` 表改名）。

**前置：挂载 + 路径 env（gateway 平铺挂载 · 见通用教训 G-X45）**
- 沙箱默认可能只挂 Brain → 用 `mcp__cowork__request_cowork_directory` 把 `~/Documents/Database`、`~/Documents/Claude/Projects/Financial/白泽大宗`、`~/Documents/AI4ME`、`~/Documents/Claude/Artifacts` 挂进来再开工。
- **挂好后导出路径 env**（脚本认 env、免去「向上找 Documents」/「HOME 拼接」在平铺挂载下算错；Mac 原生不设 env、照旧回退，零影响）：
  - `export BAIZE_OUTPUT_ROOT="<AI4ME 挂载点>"` —— build_weekly_report（Stage 3）直写 `白泽大宗-outputs/` 看板、sync_to_cowork_artifact（Stage 4）取源都认它。
  - `export BAIZE_DATABASE_ROOT="<Database 挂载点>"` —— 龙鱼库 records 实时读六维、龙鱼 batch/六维 LLM、weekly_health（Stage 3.5 读 records）、longyu_health（Stage 3.5 龙鱼库自检）、business_breakdown.db 全认它。**不设则六维全显「待跑分」**（龙鱼库路径算错）。
  - `export BAIZE_ARTIFACT_ROOT="<host 可见挂载点>"` —— sync_to_cowork_artifact（Stage 4）把转换后 HTML 写到它下的 `baize-weekly-dashboard/index.html`。⚠️ **Artifacts 目录常因受保护挂不上**——此时**别留空**（留空会落到沙箱本地 `~/Documents/Claude/Artifacts`，host 读不到、update_artifact 的 html_path 拿不到文件，2026-07-01 实跑教训 G-X45）；改**指到一个已挂载的 host 可见目录**（如 AI4ME 挂载点下，`export BAIZE_ARTIFACT_ROOT="<AI4ME 挂载点>/_artifact_stage"`），让产物落在 host 能读到处。
  - 写 business_breakdown.db 走 /tmp 副本时另设 `BAIZE_BUSINESS_DB=/tmp/...`（优先级高于 BAIZE_DATABASE_ROOT）。

执行步骤：

【Stage 0.5 · 沙箱直取数（[1]期货 + [3]龙鱼 batch）】bash 每条命令独立（无 cwd/env 延续）、单条 45s 上限。**注意：每条命令在独立 bwrap 中、die-with-parent——nohup 后台进程不跨调用存活，绝不可用「后台跑+轮询」模式**；长任务必须**分片**：每条 bash 调用同步跑完一小块（如 batch 每次一只股，约 40s）。先做环境三件套（文件系统跨调用持久，整个任务会话做一次即可）：
```bash
ln -sfn "$HOME/mnt/Documents" "$HOME/Documents"   # GOTCHA-014：脚本里 ~/Documents 路径在沙箱不成立，symlink 桥接
mkdir -p ~/.tushare && grep '^TUSHARE_TOKEN=' "$HOME/Documents/Database/.env" | cut -d= -f2- | tr -d '"' | tr -d "'" | tr -d '\n' > ~/.tushare/token   # 龙鱼约定 token 路径（printf 语义,无尾换行）
pip install tushare --break-system-packages -q   # 沙箱每会话全新
```
[1] 期货价：`cd PROJ && python3 scripts/data_collection/fetch_futures_prices.py`（merge 语义，保留其它品种）。
[3] 龙鱼 batch：ts_code 清单取法同 weekly_local_prep.sh L49（从 stocks_fundamentals.json 提取，即大宗受益榜）。**★ 常更标的不并入此处**——由独立「**龙鱼标的库周更任务**」负责双 scorer 周更（deepseek 子项 + claude top-down），见接手指南「常更标的接入」节；白泽只评自己的大宗受益公司。**每条 bash 调用跑一只**：`cd Database/行业研究/consumers/龙鱼五力 && timeout 43 python3 batch_score.py <一只ts_code>`（timeout_ms 设 45000；超时的股重试一次，仍失败则该股标『待引擎』继续）。**增量阈值＝『过龄≥1周』**（2026-06-25 Doctor 定）：查 reports/，**最新 five_forces_data 产物分龄 <7 天的股跳过、≥7 天（或无产物）才重核**——慢变量周更，跳本周内重复、杀每周全量重跑的浪费。注意：引擎 `_connect` 已支持 https_proxy 隧道（2026-06-11 补丁）——若见成批 ENGINE_FAILED/「找不到标的」，先怀疑代理/网络而非 ts_code（GOTCHA-013 变体：鉴权/网络失败会被吞成"找不到标的"）。
[2][4] 已于 2026-06-11 加白名单（hq.smm.cn / api.deepseek.com），但**先自检再跑**（白名单是会话启动快照，403 即回退）：
`curl -s -o /dev/null -w '%{http_code}' --connect-timeout 8 https://hq.smm.cn/` 与同法测 `https://api.deepseek.com/`——非 000/403 才继续。
[2] SMM 现货：`cd PROJ && python3 scripts/data_collection/fetch_smm_h5.py --fetch --merge`（纯 stdlib urllib，自动走代理）。自检失败 → 钨/稀土并入 Stage 1 web 补价。
[4] 六维 LLM（**沙箱自动化跑分落龙鱼库**）：对 reports/ 里有 five_forces_data 但 **llm_score 缺失或最新分龄≥7 天**（同『过龄≥1周』阈值）的股，**每条 bash 调用评一只**：
`cd 龙鱼五力 && KG_API_KEY=$(grep '^KG_API_KEY=' ~/Documents/Database/.env | cut -d= -f2-) timeout 43 python3 score_with_llm_apiyi.py <ts> --engine-json $(ls -t reports/five_forces_data_<ts>_*.json | head -1) --api-key-env KG_API_KEY --base-url https://api.deepseek.com/anthropic --model deepseek-v4-pro --save`
`score_with_llm` 评完即 `record_writer.upsert_analysis` **落龙鱼库 records**（公司级真源）——这就是新受益公司六维进库的唯一通路。单票历史耗时 30-45s 贴上限：超时重试一次，仍超时该股留『待跑分』继续，不阻塞。
> **⚡ 六维并行加速（2026-06-25 实测·Doctor 同意）**：六维 LLM 走 DeepSeek、**不占 Tushare IP slot**，故可**一片多只并行**（同一 bash 调用内 `... --save >/tmp/llm_$c.log 2>&1 &` 后台多只 + `wait`）。实测 **10 并发、单片 ~24s 全成**，把 28 只六维从 ~28 次调用压到 ~3 片。各 `score_with_llm` 写独立 `llm_score_<ts>_<时间戳>.json` 并各自落龙鱼库，无写冲突。**注意：仅六维腿可并行**——[3] 引擎腿（batch_score→Tushare）**必须串行**（TushareClient 单 IP slot，并行多连接会被拒）。引擎腿提速只能加大单片只数（实测 4-5 只/片 ~35-43s 安全）。
读 local_prep_health.json 仍照旧——过渡期 Mac cron 双轨，谁的产物新用谁的（reports/ 按时间戳自然取最新）。

【Stage 0 · 渊图先验】用 bash 读 /Users/lunarabbit/Documents/Database/行业研究/mapping/行业知识图谱_完整数据库.json，对 13 种商品(碳酸锂/稀土/黄金/铜/原油/氦气/钨/六氟化钨/光模块-800G/光模块-1.6T/高多层板/HVLP铜箔/液冷服务器)检索相关节点的结构判断(供给收紧/供需缺口/见顶约束等)与其 data_sources[].confidence_level + data_vintage。记下每商品结构先验(P1)，用于判 persistence_type/dimensions 与交叉验证。

【Stage 1 · 补价 + 定位受益公司】
1) 读 PROJ/data/commodity_prices_live.json，看本地 cron 已写入哪些新鲜价（含 [1]期货 [2]SMM 钨/稀土）。读 data/weekly/local_prep_health.json 看各步是否跑成。
   注：SMM h5(钨/稀土)应已由 Stage 0.5 步骤[2]（或过渡期 Mac cron）merge 进 live store；若 [2] 自检失败且 health 显示 cron 侧也失败，则把钨/稀土并入下条 web 补价。
2) 对 cron(期货[1]/SMM[2]) 仍未覆盖、仍缺价的商品，按检索顺序(渊图无现货数→官方权威站 SGE/广期所/SMM/Mysteel/生意社/百川/卓创(特气)/中钨在线(钨)/包头所=P1，否则一般web=P2)用 WebSearch 找当前现货价+同比+环比；只填查得到、可引用的，写 CSV 到 PROJ/data/weekly/web_fill_本周.csv，再运行：
   cd PROJ && python3 scripts/data_collection/refresh_commodity_prices.py --from-csv data/weekly/web_fill_本周.csv
   **CSV 列（含新增两列）**：name,change_yoy,change_mom,price,unit,persistence_type,dimensions_passed,credibility,source,**confidence,asof**。
   - **confidence（必填·0-100）**：你(LLM)对该价/同比可靠性的判断——源权威性×时效×口径一致性×与多源是否吻合。清洁近月权威价→70-90；偏旧或锚算→40-60；口径冲突/勉强→<40。渲染层据此显置信徽（绿≥70/黄45-69/红<45）。
   - **asof（必填）**：填真实源采集日(如 2026-05-21)，**勿冒充今天**。现货/特气 web 价新鲜度阈值已放宽至 90 天(期货 P0 仍 30 天)，故近两月权威价可入；超期或同比无法洁净核验的，**不写 CSV**，改走下条 probe。
   该脚本 **MERGE 语义**：保留本地 cron 的 Tushare 期货 P0 价，只新增/覆盖你 CSV 里的商品。缺价商品留空——绝不编。
2b) **web_probe.json（待核验商品的探价注记）**：对查不到洁净同比/无公开现货报价者(如钨口径冲突、光模块属组件ASP、液冷/铜箔/高多层板无现货指数)，**不要硬填 CSV**；改写 PROJ/data/weekly/web_probe.json：{"generated","probes":[{"name","price_hint","yoy_hint","confidence","tier","asof","source","note"}]}。这些只作参考注记进报告「数据缺口」区(带置信徽)，**不进弹性测算**。铁律：宁标低置信留待核验，绝不让勉强数冒充真值驱动受益榜。
3) 运行 cd PROJ && python3 scripts/analysis/run_full_analysis_v4_1.py 生成当日分析报告(确认 live 模式、受益榜正确)。

【Stage 1.6 · 持续性度量 + 实测β（2026-07-09 回测重构·中长趋势发现器定位·失败不阻塞）】
1) `cd PROJ && python3 scripts/analysis/compute_persistence.py` —— 数据驱动持续性（期货 4 商品 Tushare 周度 yoy 序列 + 其余商品 warehouse 快照史）→ `data/weekly/persistence_metrics.json`：连续>20%周数(喂弹性分持续性系数)、⚡本周新突破、篮子20日市场确认。**弹性分 v2 依赖此文件**；缺失时报告自动退回渊图 persistence_type 判断（系数塌到 0.5，榜仍能出）。
2) `cd PROJ && python3 scripts/analysis/compute_realized_beta.py` —— 实测商品β（周度回归·2024起）→ `data/realized_beta.json`，受益榜「β」校准列。慢变量，**失败沿用上周文件即可**。
注：传导系数（demand_elasticity 档1v2）为慢变基本面，由 `compute_elasticity_tier1.py` 维护，**周任务不重算**；只有 revenue_ratio/purity 等基本面核校更新后才手动重跑。

【Stage 1.5 · 龙鱼个股库同步（领域分库 2026-06-29：公司六维=龙鱼库公司级真源，已无 ingest 镜像步）】受益榜位为 Top 20，但**仅鲜价商品的真实标的可入榜**（缺价不算、不以占位股凑数）；标的池与六维/估值分均取自龙鱼五力个股库。
1) ~~同步六维到 longyu_scores.json~~ **【已弃用】**——领域分库后周报由 build_weekly_report 经 `lib_public_read.lookup_company` **实时读龙鱼库 records**（公司级真源），无需再 ingest 镜像。要让某股六维进榜，**确保它在龙鱼库有评分**即可：Stage 0.5[4] 的六维 LLM 评分（`score_with_llm`）已经 `record_writer.upsert_analysis` **自动落龙鱼库 records**——这就是「沙箱自动化跑分落库」。某股龙鱼库无评分则周报留『待跑分』，绝不以分位充总分。
2) 扩充标的池(凑向 20，可选)：从龙鱼个股库导出受益股，按模板(sync_longyu_universe.py --template)填入 P0/P1 来源后，
   python3 scripts/data_collection/sync_longyu_universe.py --expand-universe data/weekly/universe_add.csv  # upsert 进 stocks_fundamentals.json + business_breakdown(受益关系)
   缺 data_source/priority 的行会被拒收（铁律）。**新受益 ts_code 入池后，须经 Stage 0.5[1/3] batch_score 拉数 + [4] 六维 LLM 评分 → 自动落龙鱼库**，榜上其六维方能填入（沙箱自动化闭环）。鲜价补齐 + 标的入库后，榜自然向 20 收敛。
   注：龙鱼**财务/估值评分**(batch_score.py)与**六维 LLM**(score_with_llm_apiyi.py)均沙箱可跑（见 Stage 0.5）——若某股分值缺，可即时补跑；补不上的如实留『待跑分』，不阻塞出报告。

【Stage 2 · 双面交叉验证】对弹性 Top 20 受益公司，逐家三路取证：
- 渊图侧(P1)：该商品/公司的结构性支撑或约束(用 Stage 0 结果)。
- 龙鱼侧：**读龙鱼库公司真源**（build_weekly_report 已实时读 records：财务分/PE·PB 分位/六维/评级/thesis）；缺则标"待跑分"。**名称一致性闸**：ts_code 命中但记名≠本公司，退『待跑分』，不张冠李戴(见 GOTCHA-016 赣锋/雅化)。
- 新闻侧(WebSearch)：分别搜「公司名 受益/涨价/业绩/扩产」(成立面) 与「公司名 减持/停产/不及预期/回调/风险/库存」(证伪面)，各取 2-3 条，标信源等级(权威媒体/交易所=P1，一般=P2)。
判「量价背离」(价涨但量/份额/业绩未跟上？)。给裁决：成立/存疑/证伪 + 置信度(高/中/低)。
写成 PROJ/data/weekly/crossval.json，schema 见 PROJ/data/weekly/crossval.sample.json：{"generated":"YYYY-MM-DD","companies":[{"name","commodity","verdict":"成立|存疑|证伪","confidence":"高|中|低","divergence":"...","support":[{"tier":"P1|P2","text","source"}],"refute":[{...}]}]}。
> **web 不可用时（2026-07-01 实跑遇 WebSearch 拒返）**：绝不编造新闻面。按下面**三级降级**处理：
> 1. **首选 WebSearch**：成立面/证伪面各搜 2-3 条（原流程）。
> 2. **WebSearch 拒返时 → 改走 web_fetch 公告兜底（2026-07-01 新增·已验证）**：WebSearch 在 CLI/gateway 常被拦，但 `mcp__workspace__web_fetch` 通。改抓**东方财富公告 API**（服务端 JSON·交易所披露＝**P1**，比一般 web 更权威）：
>    - ① 生成 URL 清单：`cd PROJ && python3 scripts/data_collection/fetch_announcement_evidence.py urls`（按需 `--names a,b` 或 `--limit N` 只取榜上公司）。脚本打印 `code6<TAB>name<TAB>url` 并写 `data/weekly/_ann_manifest.json`。
>    - ② 对清单每个 url 调 `mcp__workspace__web_fetch`，响应**原样**存到 `data/weekly/_ann_raw/<code6>.txt`。
>    - ③ 解析为 P1 证据：`python3 scripts/data_collection/fetch_announcement_evidence.py parse --days 30` → 出 `data/weekly/ann_evidence.json`（按利多/利空关键词分桶）。
>    - ⚠️ **关键词分桶只是线索**：务必逐条**读标题原文**再定性（脚本已带否定语境过滤如「解除质押」，但仍可能误判）；公告只覆盖**披露事件面**（减持/质押/扩产/订单/计提/业绩预告等），**媒体观点面仍 best-effort**。据此填 crossval 的 support/refute（标 P1 + source + 披露日）。
>    - 巨潮 cninfo 公告查询可作第二 P1 源（同理 web_fetch JSON）；前端渲染站（财联社/雪球等 Next.js）抓回是空壳，**别抓门户首页、只抓服务端 JSON 接口**。
> 3. **web_fetch 也拿不到时 → 沿用旧 crossval**：若既有 crossval.json 仍新鲜（≤7 天、带 P1/P2 来源、过校验 gate）且本周价格数据同源，可沿用既有裁决并在收尾摘要里**如实说明「本轮 web 未刷新、沿用 N 天龄 crossval」**；下轮恢复再刷新。
> 无论走到哪级，**绝不编造**：查不到的公司新闻面留空、标『待核验』。

【Stage 2.5 · crossval 校验 gate（2026-06-24 新增·必跑）】写完 crossval.json 立即校验：`cd PROJ && python3 scripts/reports/validate_crossval.py`。退出 0=合格放行；退出 1=不合格（漏 name/verdict/divergence、support/refute 缺 tier/text/source 引用、verdict=成立/证伪 却缺正反面）→ 按打印的逐条问题**补全 crossval.json 后重校**，再进 Stage 3。（build_weekly_report 已内置同一 gate：crossval 存在但不合格会**中止 build**、拒绝静默渲染「待补」；crossval 缺失则允许·留空待补。）

【Stage 3 · 出报告】运行 cd PROJ && python3 scripts/reports/build_weekly_report.py
产出（2026-06-10 对齐脚本实际行为）：看板 HTML（dated + 定名版『白泽周报看板_最新.html』）落 /Users/lunarabbit/Documents/AI4ME/白泽大宗-outputs/（沙箱设了 BAIZE_OUTPUT_ROOT 即直写挂载点对应目录——见前置·G-X45）；周报 MD **单份滚动**落 PROJ/周报/白泽周报_最新.md（项目层每周覆盖，outputs 目录不再放 MD）。
注：local_prep_health.json 若为空 `{}`（未写成/被覆盖），按"健康未知"处理——以 live store 实际新鲜度为准，不臆断本地 cron 成败。
渲染层确定性，沙箱无人值守可跑；看板模板已对接 O MY HTML 设计语汇（米白纸底·墨黑·印章红/暖金/翠绿配色预算·Noto Serif SC 题款·浮雕卡片·同比/弹性条形可视化），无需另装设计工具。
报告含**七节 / 四维分析**：①本周价格 ②受益公司榜 Top 20（弹性条 + 龙鱼六维·财务·PE/PB分位 + 量价背离裁决一体）③**商品维度归因**（每鲜价商品涨价/环比/持续性/受益传导 Top + 风险旗标）④双面交叉验证逐家 ⑤**风险与配置建议**（按商品风险旗标 + 通用纪律，附「非投资建议」声明）⑥数据缺口 ⑦P0/个股库升级清单。六维/估值缺位一律『待跑分』，未满 20 家时榜尾如实说明原因。
若 live 模式为 empty(本地 cron 未跑成)，看板自动呈"待核验态"——明确提示"本地预备未生效"，并附 P0 升级命令(scripts/automation/weekly_local_prep.sh 或手动三步)。

【Stage 3.5 · 端到端健康自检（2026-06-24 新增·必跑）】出报告后跑：`cd PROJ && python3 scripts/reports/weekly_health.py`。只读自检本轮关键产物（鲜价 commodity_prices_live / **龙鱼库 records 在位**（沙箱设 BAIZE_DATABASE_ROOT 才找得到，见前置）/ 周报 MD / 双面 crossval）存在性 + 新鲜度（周更 >8 天=过期）+ crossval 合格性 → 写 `data/weekly/_health.json`（overall ok/stale/fail · 含 target_date 字段·A·sub1 · 2026-07-01 补）。缺关键产物=fail、过期=stale。产物供海螺姑娘资产看板 conch survey 读取 →「白泽产出库·business_breakdown.db」节点按健康发光告警（无需主动推送）。收尾摘要附 overall 与缺/过期产物。

**紧接着跑龙鱼库自检**（G-X45 第三批 · 2026-07-01 新增·必跑）：
`python3 ~/Documents/Database/龙鱼-标的分析库/scripts/longyu_health.py`
—— 只读扫 records/*.json 最新 mtime → 写 `Database/龙鱼-标的分析库/_health.json`（overall ok/stale/fail，阈值 stale≥10d）。脚本认前置里导出的 `BAIZE_DATABASE_ROOT`（或独立 `LONGYU_DATABASE_ROOT`/`LONGYU_RECORDS`）。产物供海螺姑娘资产看板 conch survey 读取 →「龙鱼基本面库」节点按健康发光告警。收尾摘要末尾附一行「longyu health: {overall} · target={target_date} · n_records={N}」。

【Stage 4 · 精致看板呈现（工作流收尾·最后一步）】这是周日工作流的最终交付步，务必执行。（build_weekly_report 每次同时产「日期版 白泽周报看板_YYYYMMDD.html」与「定名版 白泽周报看板_最新.html」，二者内容同一；呈现用**定名版**，免日期跳变混淆。）
1) 打开 白泽周报看板_最新.html 自检版面——题款/印章、KPI 四宫、价格卡（鲜价含同比条+信源徽、缺价呈斜纹『待核验』）、受益榜弹性条、双面交叉验证卡、缺口区是否齐整且配色雅致；数据须与 MD 周报一致、无占位冒充。
2) 用 present_files **先呈定名版看板 白泽周报看板_最新.html，再呈 PROJ/周报/白泽周报_最新.md**（看板为主交付物，置于最前）。
3) 附一句话白泽口吻摘要：本周价格新鲜度（鲜价 N 种/全集 M 种）、受益 Top3、交叉验证 X 家成立/Y 家存疑/Z 家证伪/W 家待跑分。
4) **同步侧栏 Artifact**（id=`baize-weekly-dashboard`，2026-06-12 老师定 · 2026-06-14 改脚本化）：**务必执行——这是数据进侧栏看板的唯一通路，漏掉则卡片停在上次日期**（2026-06-14 实测：Stage 3 出活但本步漏跑，侧栏滞留 06-12）。两步：
   ① 跑同步脚本（一条 bash，幂等）：`cd PROJ && python3 scripts/reports/sync_to_cowork_artifact.py`（沙箱设了 BAIZE_OUTPUT_ROOT/BAIZE_ARTIFACT_ROOT 即认挂载点，见前置·G-X45；不设则回退 HOME/Documents、平铺挂载下会找不到源）。**⚠️ Artifacts 目录挂不上时（常见·受保护），务必先把 `BAIZE_ARTIFACT_ROOT` 指到一个 host 可见的挂载点（如 AI4ME 挂载点下），否则脚本会写到沙箱本地 `~/Documents/Claude/Artifacts`、下一步 update_artifact 的 html_path 读不到文件（2026-07-01 实跑教训 G-X45）。** 脚本自动：取定名版看板 → 注入 `cowork-artifact-meta`（name=白泽大宗综合周报 / 描述首句『更新时间：<北京时刻>』）→ 首行 dateline 改『更新时间：<北京时刻>』（D.date 变量保留供新鲜度计算）→ 删 Google Fonts 外链 + 本地字体回退 + 补 `color-scheme:light` → 写 `<BAIZE_ARTIFACT_ROOT>/baize-weekly-dashboard/index.html`。脚本打印 `OK 写: <绝对路径>` 与 `DESC ...` 行——记下写出路径供下一步。
   ② 调 `mcp__cowork__update_artifact`（deferred 则先 ToolSearch `select:mcp__cowork__update_artifact`）：`{id:"baize-weekly-dashboard", html_path:"<上一步脚本打印的 index.html 绝对路径·须 host 可见>", description:"<脚本打印的 DESC>", update_summary:"周报 YYYY-MM-DD 重渲"}`。
   自检：脚本 stderr 无 WARN（外链残留/未找到 token）才推送。此步失败仅警告不阻塞收尾，但**必须在收尾摘要里如实报「侧栏未同步」**，不可静默跳过。
（如需进一步美化或改版式，改 scripts/reports/build_weekly_report.py 的 _HTML_TMPL；勿在产物 HTML 上手改，否则下周重渲覆盖。）

【Stage 5 · 汇总只读层 ingest（additive · 失败不阻塞）】把本周散落 JSON 汇进**锁定的数据层宏观库** `~/Documents/Database/宏观-大宗商品/business_breakdown.db`（看板按此读 ingest_meta 判新鲜度；脚本默认即写此路径，读 JSON 仍走 PROJ/data）作查询/同比/完整性读模型——**只加表(6 warehouse 表 + ingest_meta；2026-07-09 增 board_snapshots 受益榜周快照·回测闭环)，不改 fetch/sync/build 任何连接器，不动该库既有表**。一条 bash（幂等·按 generated 周快照累积）：
```bash
cd PROJ && python3 scripts/database/build_warehouse.py
```
产出 6 表：price_snapshots / **benefit_relations**（原 fundamentals·受益关系） / crossval / web_probes / proxy_prices / **board_snapshots**（受益榜周快照·2026-07-09 增·回测闭环）。（**领域分库 2026-06-29**：`stock_scores` 评分镜像已弃用、不再构建——公司六维改读龙鱼库；库内旧 stock_scores 表冻结保留不 drop。）此步**失败仅警告不阻塞收尾**（如某挂载盘不支持 sqlite 直写——删 -journal 受限报 disk I/O error——则本步跳过，下次真机/可写环境补跑即可，不影响周报与看板交付；或走 /tmp 副本往返再 cp 回）。回退：`python3 scripts/database/build_warehouse.py --drop`。

收尾自检：报告里是否还有答不出来源的数？有则改回『待核验』。绝不让占位/样本数冒充真实行情。