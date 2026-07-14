---
title: 龙鱼五力 · GOTCHAS（已知坑）
tags: [龙鱼五力, gotchas]
created: 2026-05-14
updated: 2026-05-14
status: active
type: resource
project: 龙鱼五力
---

# 龙鱼五力 · GOTCHAS（已知坑）

> 排查超过一轮的问题都该记录在这里。CC 遇到报错并解决后**立即**回写，无需 Doctor 提示。
> 实时操作日志写在项目目录的 `Projects/龙鱼五力/GOTCHAS.md`；这里是沉淀+索引。

## 格式

```
## [ERR-YYYYMMDD-NNN] 简要描述
**状态**: ✅ 已解决 / ⏳ 待解决
**优先级**: 🔴 高 / 🟡 中 / 🟢 低
**触发场景**:
**错误信息**:
**解决方案**:
**预防措施**:
```

---

<!-- 在下方追加新条目 -->

## [EXP-20260625-001] 在 Cowork 沙箱端到端实跑龙鱼引擎 + DeepSeek 评分
**状态**: ✅ 已解决（实测德明利 001309.SZ 通）
**优先级**: 🟢 低（操作经验）
**触发场景**: 想在 Cowork 沙箱里直接跑 `five_forces_engine_v3.py` + `score_with_llm.py` 做连通性/打分实测，而非只贴命令给 Doctor 终端。
**关键点**:
- **白名单**：本会话沙箱已含 `api.tushare.pro` / `api.waditu.com` / `hq.smm.cn` / `api.deepseek.com`（先 `curl -s -o /dev/null -w '%{http_code}'` 自检：非 000/403 才继续；白名单是会话启动快照 = GOTCHA-022）。
- **Tushare token**：~~引擎 `_load_token()` **不读** `TUSHARE_TOKEN` 环境变量~~（※2026-06-27 更正：此条已过时——引擎现 `_load_token()` 顺序为 **① `TUSHARE_TOKEN` env（优先）→ ② macOS Keychain → ③ `FF_TOKEN_PATH` 文件**，**读 env**。沙箱最简：`export TUSHARE_TOKEN=$(grep '^TUSHARE_TOKEN=' /sessions/<id>/mnt/Database/.env | cut -d= -f2- | tr -d '"' | tr -d "'" | xargs)` 后直跑引擎，本会话冒烟 600118 实测通）。文件降级仍可用 `$HOME/.tushare/token` 或 `FF_TOKEN_PATH=Claude/Env/tushare.token`。
- **`~` 陷阱（叠加 GOTCHA-014）**：沙箱里 `~`/`$HOME` = `/sessions/<id>/`，**不是**挂载盘 `/sessions/<id>/mnt/Documents/`。`source ~/Documents/Database/.env` 会静默读空 → token 写空 → 报「找不到标的」（非代码错）。.env 必须用 mnt 绝对路径。引擎 `REPORT_DIR` 同理落到沙箱本地 home（产物不在挂载盘，实测无碍）。
- **DeepSeek key**：`score_with_llm.py` 的 `KEY_ENV_CANDIDATES` 首位 `KG_API_KEY`，`export KG_API_KEY=$(grep ... .env ...)` 后脚本自动命中，无需 `--api-key-env`。
- **45s 切分**：引擎 leg（~9s）与 DeepSeek leg（~22s，thinking:disabled）串起来可能逼近沙箱 bash 45s 上限 → 先 `engine --save --json-only` 落 JSON，再 `score_with_llm.py --engine-json <file>` 分两段跑。
**预防措施**: 沙箱实跑前先跑连通性 curl 自检 + 确认用 mnt 绝对路径读 .env；长链路拆 engine/score 两段。

> **补充（2026-06-28 · 联瑞/东威/盛和跑分案再实证）**：本条再次踩到——直跑 `batch_score.py 688300.SH` **首发即 `ENGINE_FAILED`**，直跑引擎暴露真因 `FileNotFoundError: ~/.tushare/token`，即**引擎没拿到 token**。根因＝`batch_score.py` docstring 和龙鱼系统概览那句「沙箱经 localhost:3128 + Database/.env token 实跑」**易误读为「自动读 .env」**，实则引擎只读 `TUSHARE_TOKEN` **环境变量**、不自动 source .env 文件。**正解一行**：`cd consumers/龙鱼五力 && set -a; . <mnt>/Database/.env; set +a; export HTTPS_PROXY=http://localhost:3128 HTTP_PROXY=http://localhost:3128 && python3 batch_score.py <codes>`。实证 688300/688700/600392 三连 OK。**判别信号**：batch 全 `ENGINE_FAILED` 且直跑引擎报 `~/.tushare/token` not found ＝ 没 export token，不是网络/积分问题。

---

## [NOTE-20260706-001] 引擎财务维对周期股「盈利能力」假阳性（GM 口径失真 + 跨周期 ROE 均值）
**状态**: ⏳ 待解决（已识别·需人工 overlay 兜底；引擎口径修正待评估）
**优先级**: 🟡 中（周期股/价差型标的必踩）
**触发场景**: 用引擎跑周期性行业（存储模组/面板/大宗加工）的价差型公司，财务维 `financial_score` 自动打分。
**现象**: 江波龙 301308.SZ（2026-07-06）引擎财务维把「盈利能力」子项打满 1.0/1，evidence＝「ROE 均值=23.0%>15% ✅；毛利率上升趋势(55.53%)↑」。但——
- **GM 55.53% 口径失真**：报表实际毛利率 2023=8.19%/2024=19.05%/2025Q3=18.92%，从无 55% 量级（疑 Tushare `grossprofit_margin` 口径异常或取值错期，同族 ERR-20260602-002 三费口径坑）。
- **ROE 均值 23% 含周期顶点**：15 期均值被 2026Q1 顶点（ROE 39.4%）拉高，掩盖 2023 下行 ROE −13.01%。
两者叠加让引擎把"周期顶点的 β"误判成"稳定的盈利能力"——引擎本身几乎落入**假定价权陷阱**。
**判别信号**: 周期性行业 + 财务维盈利能力满分 + 引擎 GM 远高于最近报表披露值（或明显不符行业常识）→ 别信 auto 分，人工核最近 4-8 季报表毛利率 + 看 ROE 是否穿越周期。
**解决方案（当前）**: 人工 overlay——按 EXP-20260706-003-P「毛利率穿越周期看」核实，江波龙人工六维修正为 47.5/回避（引擎 auto 会高估）。GM 落库时加 `gm_flag` 标注口径异常（见 records/301308.SZ_江波龙.json.engine_facts）。
**预防措施**: 引擎财务维「盈利能力」子项对周期股应改用「近 N 季报表 GM + 穿越周期 ROE（含最近一个完整下行）」而非跨期均值/单点趋势；口径修正前，跑周期股一律人工复核该子项。

---

## [ERR-20260710-001] 引擎增长指标喂单季触底 YoY → 误导 deepseek 盲打、系统性打低「触底→转正」拐点标的
**状态**: ✅ 已根治（2026-07-11 小改实装+验证）——引擎新增 `growth_period`/`growth_period_is_interim`/`tr_yoy_annual`/`netprofit_yoy_annual`（取最近 1231 年报期，不改既有 tr_yoy/netprofit_yoy 向后兼容）；score_subitems 打分提示加「增长口径铁律」优先年度、单季仅参考；`_facts` 补 np_yoy/annual/period 入库（今后可精确回扫）。**振华 000733.SZ 验证**：引擎单季 netprofit_yoy=−72.81%(20260331·interim) → 新增年度 netprofit_yoy_annual=**+5.69%**/tr_yoy_annual=+10.26%(20251231)，与 raw#4 FY25 +10%/+6% 吻合。根因＝`fetch_financial_indicators` 取 fina_indicator_vip 最新 end_date 累计 YoY，最新期为单季(Q1)时即窄口径。
**优先级**: 🟡 中（拐点/周期反转标的必踩 · NOTE-20260706-001 族系）
**触发场景**: 双 scorer 制度里 deepseek 自下而上盲打，引擎 `engine_facts.rev_yoy/np_yoy` 作为「供需兑现 / 增长-估值匹配」的关键锚。
**现象**: 振华科技 000733（2026-07-05 deepseek）引擎喂 `rev_yoy=-7.86% / np_yoy=-72.81%`，deepseek 据此判「负增长、需求疲软、未见兑现」→ 供需端 8/35、估值增长匹配 1/15 → 总分 43/回避。但 raw#4 第九节 **P0 实测 FY2025 营收 +10%/归母 +6% 已确认拐点**（2025Q3 单季 +15.78%/净利 +38.68%）。引擎那个 -72.81% 精确匹配 2025Q1 单季触底（全年最差季），是滞后/单季口径、与全年转正相反。
**影响**: 凡「触底季→全年转正」的拐点标的，供需维 + 估值增长匹配维被系统性打低；claude 用拐点叙事(72观察) vs deepseek 用触底数(43回避) → 29 分假分歧，其中约 −10(供需) + −5 的一半(估值) 属**数据口径错误、非视角**。
**判别信号**: 双 scorer 分歧巨大(>20) + deepseek evidence 出现「负增长/需求疲软」且引擎 np_yoy 深负、但最新年报 P0 为正增长 → 引擎增长口径取了单季/滞后期。
**解决方案（当前）**: 人工「错误校正」层——只弥合数据口径错误维(供需/估值增长匹配)、保留视角差异(竞争/新赛道)；振华校正后 deepseek 51/谨慎、claude 67/谨慎，收敛中枢 ~59。落 `records/000733.SZ_振华科技.json` 新增 `research-CC·错误校正` 条（**不覆盖原始盲打**）。**不手改 deepseek 盲打分以保独立盲打制度**。
**根治待办**: ① Doctor 终端核 `five_forces_engine_v3` 的 rev_yoy/np_yoy 取数 period（应取最新年报/TTM 且标注 period，非滞后单季）；② engine_facts 加 `growth_period` 字段显式标口径；③ batch 回扫同批航天 universe 拐点标的（凡 FY25 转正但引擎 np_yoy 深负者）是否同样被误伤。
**预防措施**: deepseek 盲打前引擎增长指标须与最新年报 P0 对齐并标 period；分歧归因先查「负增长前提」是否成立（核最新年报）再判视角 vs 错误。属 NOTE-20260706-001（引擎财务口径失真）族系。

---

## [NOTE-20260714-001] save_holdings 守恒校验挡增删 → 加/删标的须直改 holdings.json 源
**状态**: ✅ 已知（设计如此·非 bug）
**优先级**: 🟢 低（每次加删持仓标的会遇）
**触发场景**: 想通过看板 MCP `save_holdings` 或编辑面板增/删持仓标的。
**现象/根因**: `save_holdings` 带守恒校验「只数须与现有一致，防误覆盖」——它是给看板内联改股数/成本用的，**改只数（加/删标的，如 11→12 或 12→11）会被挡下**。
**解决方案**: 加/删标的**直接改源文件** `龙鱼-标的分析库/holdings.json`（唯一维护点·"变动只改此文件"），用主机 Read/Write/Edit，不走 save_holdings。看板 `get_board_payload` 实时读，改完即显。
**预防**: 常驻「编辑股数→0 自动删」若要落，需改 MCP（加 delete_holding / 放宽守恒校验）+ 重启 Desktop。

## [NOTE-20260714-002] 看板 seg/plate 来自 `_index/细分环节.json`（非 record 的 track）→ 新标的入库须补这张表
**状态**: ✅ 已知
**优先级**: 🟢 低（每次新标的入 records 会遇）
**触发场景**: 新标的写进 records 后，看板仍显示 seg=未归类。
**现象/根因**: `board_data.py` 的 seg/plate 从 `龙鱼-标的分析库/_index/细分环节.json` 的 `map[ts_code]` 取（`{板块,环节,label,name}`），**不读 record 的 `track` 字段**（track 只作展示文本）。record 有六维但缺这张表的映射 → 落「未归类」。
**解决方案**: 新标的入库时一并补 `_index/细分环节.json` 的 `map` 一条（如光库 300620.SZ → `{"板块":"AI硬件","环节":"光通信","label":"AI硬件｜光通信","name":"光库科技"}`）。
**预防**: 把「补 seg 映射」纳入入库 playbook 常规步（与 record_writer + build_index 并列）。
