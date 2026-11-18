# conch · 健康度与优化动作（文件健康审查及整理 · 1.5.0 起）

> 接入海螺姑娘「文件系统健康度管理」（2026-11-06 PRD `brain/logs/checkpoints/2026-11-06_GAI升级文件系统健康度管理_PRD.md`，三期 Doctor 同日验收）。本文件只写怎么跑、怎么读、怎么交 Doctor；口径与动作表的真源在海螺项目，改口径先改真源。
> 2.0.0 起健康度评分是「文件健康审查及整理」审查清单 C、F 的一部分（总则 `file-health.md`）；第 1 步的回写（`rescan`）和第 3 步的确认档动作都属 apply，要等七步第 5 步同意。
> 海螺根：`~/Documents/Claude/Projects/海螺姑娘/`（下称 `H`）。

## 真源

| 内容 | 文件 |
|---|---|
| 健康度评分口径（五维、权重、A ≥ 85 · B ≥ 70 · C ≥ 50 · D < 50） | `H/dashboard/HEALTH_SCORE_SPEC.md`（现行 v1.1） |
| 一键优化三档动作表（自动 / 确认 / 禁手） | `H/dashboard/OPTIMIZE_ACTIONS.md` |
| 资产清单（单一真源） | `H/data/asset_manifest.json`；运行历史 `H/data/health_history.jsonl` |
| 看板 | `H/dashboard/asset-dashboard.html`（派生产物）；托管页 `global-asset-inventory` |
| 每日刷新班 | Cowork `refresh-asset-dashboard`（镜像 `brain/references/scheduled-live-mirror/live/refresh-asset-dashboard/SKILL.md`） |

## 第 1 步 · 盘点与评分（dry-run 只预览；回写在同意后）

```bash
cd ~/Documents/Claude/Projects/海螺姑娘 && python3 -B conch_engine.py survey --out "$TMPDIR/survey_preview.json"
cd ~/Documents/Claude/Projects/海螺姑娘 && python3 -B dashboard/optimize_actions.py run rescan <任一节点>
```

- 第一行是 dry-run 预览：`--out` 指向 manifest 以外的路径时不回写、不追加 history；再从该文件取各节点 score 做摘要。
- 第二行是回写（先备份 manifest 到 `_bak/`，再 survey 并重建看板 HTML），属 apply，等七步第 5 步同意。
- 回写用 `rescan` 动作，不直接跑 `conch_engine.py survey`：`survey` 自身不备份 manifest，备份在 `rescan` 里（`optimize_actions.py` `run_rescan`）。
- `build_asset_dashboard.py` 不解析参数，**带 `--help` 也会直接重建 HTML**（海螺 GOTCHA-20261117-002）；查用法读源码，不跑 `--help`。
- 看板推送不在 `rescan` 内。登记在 `brain/.tmp/artifact-publish/hosted-pages.json` 的托管页按 slug 原地更新，不另建同名页面；未登记的侧栏看板请 Doctor 到 Cowork 说「补推看板」。

## 第 2 步 · 读结果、交 Doctor

汇报：节点总数、A/B/C/D/未评分布、最差 5 项（只计 `basis="measured"`）、各节点扣分最多的维度、与上次运行（`health_history.jsonl` 末行）相比变化的节点。只读补查：各项目 GOTCHAS 里 🔄/⚠️ 开放条数，缺哪些标准文件（README / GOTCHAS / TODO）。

## 第 3 步 · 优化动作（`H/dashboard/optimize_actions.py`）

```bash
cd ~/Documents/Claude/Projects/海螺姑娘 && python3 -B dashboard/optimize_actions.py list --node <节点>
cd ~/Documents/Claude/Projects/海螺姑娘 && python3 -B dashboard/optimize_actions.py run <动作> <节点>
cd ~/Documents/Claude/Projects/海螺姑娘 && python3 -B dashboard/optimize_actions.py plan <动作> <节点> <参数，见下>
cd ~/Documents/Claude/Projects/海螺姑娘 && python3 -B dashboard/optimize_actions.py apply <动作> <节点> --yes <参数，见下>
cd ~/Documents/Claude/Projects/海螺姑娘 && python3 -B dashboard/optimize_actions.py rollback <rollback_ref>
```

- `plan` / `apply` 的 `--set 键=值` 只用于 `manifest_fix`；`gotchas_status_sync` 改用 `--ids 条目id,…`；其余动作两者都不带。
- **自动档**：`health_read`、`scan_dry`、`gotchas_stale_check`、`integrity_check` 只读，dry-run 阶段可直接跑；`rescan` 会回写 manifest 与看板，属 apply，等同意。
- **确认档**（`archive_apply`、`manifest_fix`、`gotchas_status_sync`、`fill_workfiles`）：`gotchas_status_sync` 只同步正文里已由 Doctor 或未参与实施的审核者落签的 ✅，不新判；dry-run 阶段只跑 `plan`（只读），方案进七步第 3 步汇报，第 5 步同意后才 `apply --yes`；审计写 `H/data/optimize_audit.jsonl`，含 `rollback_ref`。`archive_apply` 走 `references/archive.md` 第 3 步的逐条核查，不因为是面板动作就省。
- **禁手档**（删除、git、定时班变更、跨项目改 owner 代码、推送或改名 artifact）：只贴命令或清单与理由，由 Doctor 执行。
- 动作清单以 `OPTIMIZE_ACTIONS.md` 当前表为准，上面只是 2026-11-17 抄录；`optimize_actions.py check` 校验脚本白名单与表一致。

## 第 4 步 · 跟进

- 待修、断链的节点：按 `references/file-health.md` 对该项目审查出方案，并入七步第 5 步一次同意后才动手。
- 引擎误判、评分口径问题：登记海螺 GOTCHAS；改口径走 `HEALTH_SCORE_SPEC.md` 升版本号，再改代码（功能变更，归 Doctor 验收）。

## 不做

- 不把 `obsolete_count`（陈旧文件数）当待修：它只给「可选清理」提示，不升 needs_repair（海螺系统概览设计裁定）。
- 不在评分不满意时改 manifest 策展值凑分；策展值修正走确认档 `manifest_fix`。
- 不改定时班，不推侧栏看板。
