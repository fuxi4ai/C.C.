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
