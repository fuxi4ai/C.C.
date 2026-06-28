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
