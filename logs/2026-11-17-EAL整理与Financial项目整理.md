---
title: 会话日志 2026-11-17 — EAL整理与Financial项目整理
tags: [log, 宏观研究体系, 风险日报, 海螺姑娘, GlobalPercent]
created: 2026-11-17
updated: 2026-11-17
status: active
type: log
project: 宏观研究体系
---

# 会话日志 — 2026-11-17

**项目**：跨项目（EAL 为主；风险日报、海螺姑娘、GlobalPercent、Financial 根目录）
**主题**：EAL 文件架构梳理与整理、目录改名、风险日报迁入 Financial、Financial 清理、conch 1.4.0 整理模式

## 完成的工作

- **EAL 架构梳理**：报告 `AI4ME/2026-11-17-EAL文件架构梳理.md`；处置清单 `AI4ME/2026-11-17-EAL整理处置清单.md`；改名切换方案 `AI4ME/2026-11-17-EAL改名切换方案.md`。
- **EAL 内部整理**：锚定-跟随三组 v1/v1.1 合并为单件（规则卡、回测结果、回测口径登记），方法论、对位、资管阿宝方法论文首加「## 迭代记录」并提炼旧版有价值信息；已完成的沟通件（两份给 V.V. 的委托等）删除；回测按有用、归档、删除三类处置；命名统一为日期后置（`.conchconfig.yml` `date_style: suffix`，校验脚本加 DATE_PREFIX/VER_SUFFIX 检查）。
- **EAL 目录归一**：`cases/` 并入 `case-studies/`（README 含字段契约 v1、INDEX 两张表，校验按 type 取必填键）；`archived/` 并入 `archive/eal_v3-failed-pass1-2026-08-25/`；`治理/` 提炼进 GOTCHAS（新增 G-028～G-030，补登 G-019/023/027；G-019～G-030 每条首行「- 导航：…」指向 EAL 原文件）后删除。
- **EAL 改名**：`Projects/Financial/宏观研究体系/EAL/` → `Projects/Financial/Event-Attribution-Ledger/`，git 仓根随迁（远端 Hongguan-Research，提交 `080258a`、`1f1296b` 已推送）；伞目录 README 提炼四段并入 EAL README「沿革」节后删除；CC 侧现行引用全部跟改，冻结证据与历史记录不改。
- **launchd**：`com.eal.postevent-native` 路径改新址，`StartInterval` 300 → 900（Doctor 令「太频繁了」），FORMAT.md 同步。
- **风险日报迁入 Financial**：`Projects/风险日报/` → `Projects/Financial/风险日报/`；6 处按层级推算根目录的写法改为按名字找 `Documents`；EAL 链接改 `../Event-Attribution-Ledger/`；高位旁证、次级档位两组冻结回测自 EAL 迁入 `research/`（带 README，raw 只留本地）。
- **Financial 清理**：GlobalPercent 本地副本删除（本地与 origin 同为 `2ba3326`，靠 GitHub 留底，归档回执移至 `brain/GlobalPercent/`）；创新药科技轮动、备查区删除；`协作架构与开发需求_20260610` 移入 `brain/references/` 作历史快照；`Financial/README.md` 按现状重写为 7 项目索引（旧版在 `Financial/_bak/`）。
- **回收站**：三批进 fuxi `F:\Mac_Quarantine\_to_delete_20261117{,b,c}\`（39 / 11 / 185 件），远端 SHA 均一致，INDEX 第 16–18 行登记，保留至 2026-12-02。
- **conch 1.4.0**：`conch_engine.py` 新增 `tidy_scan()` 与 `tidy-scan [--json]`；`test_conch_tidy.py` 18 例；SKILL 加 `--tidy` 模式（合并归一、沟通件删除、回测分流、命名统一、回收站删除）；GOTCHA-20261117-001 及两条追记（分段路径、层级推算）。
- **跨侧**：V.V. 与 Cowork 的改动由 CC 写请求、Doctor 转达；Cowork 4 个风险日报班与 3 个 EAL 班的镜像已核实为新路径。
- **独立核验**：EAL 改名、风险日报迁移、第三批清理均经未参与实施的子代理核验；改名残留 4 处被查出并修复，经验索引已重建。

## 做出的决策

| 决策 | 原因 | 影响 |
|------|------|------|
| EAL 边界＝凡能归为「事件对行情的影响」的都留 EAL，其他项目只读取（Doctor 定） | 防止同类研究散落多个项目 | 高位旁证、次级档位两组迁风险日报；其余留 EAL |
| 删除一律走 fuxi 回收站，按精确名单，保留 ≥15 天（Doctor 定） | 可逆优先 | 本机暂存在两端 SHA 一致后才删；远端清理不归 CC |
| 两处嵌套分两步：先改项目文件夹，数据根 `Database/宏观研究体系/EAL` 以后另约（Doctor 选择窗） | 数据根牵动 V.V. 的 Codex 采集，需停写窗口 | 数据根仍是旧名 |
| 旧路径不留兼容链接，一次切断（Doctor 选择窗） | 留链接会让旧路径永远有人用 | 消费方必须一次改齐，靠核验兜底 |
| 命名统一为日期后置（Doctor 选择窗） | 与既有范式一致 | 校验脚本与 conch 配置随改 |
| 风险日报纳入 Financial（Doctor 令） | Financial 是金融项目总目录 | 远端 Risk-Daily 不变 |
| GlobalPercent 删本地靠 GitHub；创新药科技轮动、备查区进回收站（Doctor 选择窗） | 均已退出使用 | Financial 下只剩 7 个活跃项目 |

## 踩坑与教训（已登记处见括号）

- 目录迁移的消费方扫描只查完整路径串会漏：分段拼接（`run_step7_native.py`）与按层级推算（风险日报 6 处 `parents[N]`）各漏过一次（海螺姑娘 GOTCHA-20261117-001 两条追记）。
- 删前判「无引用」失误两次：`repro_v23`（brain eal_gate_check 在用）、`anchor_follow/archive`（重放证据），均已移回。
- zsh 管道末段 `while read f` 覆盖外层变量，把整个备查区挪进暂存区；185 件 SHA 核对一致（通用教训 G-X229 追记）。
- fuxi ssh 默认 shell 是 PowerShell 5.1，cmd 语法报错；Add-Content 遇末尾无换行会粘行（经验库 EXP-20260822-002-T 追记）。
- Doctor 重跑组合命令覆盖了 `LaunchAgents/_bak` 备份：备份步骤须「已存在则跳过」（本场未登记，见记忆分拣）。
- 方案承诺的 `eal-pre-rename` 快照未做，已如实记入 EAL 迭代记录。
- **/save 时发现的未决点**：风险日报迁移时，剑酒青丘 `仓位管理策略/inputs/tool_evidence_20261013.json` 的 `canonical` 路径与两份 `回测报告/2026-07-27_*` 的「原始路径」抬头也被改成了新路径——前者是证据文件，与「冻结证据不改路径」不一致，是否退回待 Doctor 定。

## 遗留问题 / 待办

已并入 `TODO.md`「EAL 目录整理与 conch 1.4.0 收尾」条：
- [ ] 核实 V.V. 已修三处旧路径：`~/.codex/automations/dva-mac/automation.toml`（每日 06:30）、`usdjpy-15/memory.md` L175/177/181、烛照九阴日报 `研究结论.md` L144。
- [ ] 09:05 PT 风险日报定时构建后核对产物与星空快照，并请审核者独立复核迁移；17:40 PT EAL 班后核验交接单与 Mac 端第 7 步（15 分钟轮询）。
- [ ] Doctor 在 Cowork 重传 `临时文件/skill-stub/brain-save.zip`。
- [ ] EAL 数据根迁移（第二步，需 V.V. 先改 Codex 采集，另约停写窗口）。
- [ ] 剑酒青丘证据 JSON 路径是否退回（见上）。
- [ ] anchor_follow 9 组 v1/v1.1 并存是否处置；conch 1.4.0 功能验收（归 Doctor）。
- [ ] fuxi 三批回收站 2026-12-02 期满后按精确名单清理（远端删除不归 CC）。

## 相关笔记

- [[宏观研究体系/architecture/决策记录]] · [[风险日报/architecture/决策记录]] · [[海螺姑娘/architecture/决策记录]] · [[GlobalPercent/architecture/决策记录]]
- [[通用教训]] G-X229 · [[经验库]] EXP-20260822-002-T
- EAL `迭代记录.md` 2026-11-17 各条 · EAL `GOTCHAS.md` G-019～G-030

## 后段（同日）：conch 1.5.0 → 2.0.0 与 X-Board 首次审查

- **conch 1.5.0**（Doctor 令「所有文件整理，健康检查的流程对齐进 conch skill」）：五种模式总入口、细则拆 `references/`、通用纪律十条；独立核验 PASS_WITH_LIMITS，修正后差额复核 PASS。
- **conch 2.0.0**（Doctor 令「5 种模式合并成 2 种：文件健康审查及整理、代码审计……默认 dry-run，汇报问题与处理方案，同时 subagent 复查，经我同意后 apply」「需要整理的整理，需要归档的归档」；又令「这是 conch 的运行模式」）：SKILL.md 开头立「运行模式」节；新增 `references/file-health.md`（审查清单 A–F、路由表）与 `references/code-audit.md`；`--rollback`、`--init` 也按运行模式走。两轮独立核验修正 4 处实错后差额复核 PASS_WITH_LIMITS，末轮三处措辞小改未送复核。记录：`brain/海螺姑娘/architecture/决策记录.md`、`Projects/海螺姑娘/CHANGELOG.md`。
- **X-Board 首次 `/conch` 审查**（2.0.0 首例）：dry-run 9 条，子代理复查 PASS_WITH_LIMITS（负责方一条不成立：`Doctor协作偏好.md`「X-Board 分工」有原话）。Doctor 同意五条并已 apply：`split_publish.py.bak_2026-11-12_v2` 移入 `_bak/`；`_patch_xboard_prompt_2026-10-01.py` 归档到 `archived/`；`Financial/README.md` X-Board 负责方改写；海螺资产清单新增 `X-Board` 节点与「科技资讯看板 → X-Board」边（预览 86 分 A；manifest 备份 `Projects/海螺姑娘/_bak/asset_manifest.bak_2026-11-17_xboard-node.json`）；X-Board `README.md` 按现状重写（旧版 `_bak/README.md.bak_2026-11-17_rewrite`）。快照 `brain/backups/xboard-pre-conch-2026-11-17.tar.gz`。apply 后独立核验 PASS_WITH_LIMITS，所提出处、新鲜度日期、`hosted_assets.json` 描述三处已修。
- **新坑**：海螺 GOTCHA-20261117-002（`build_asset_dashboard.py` 带 `--help` 也会重建 HTML）、-003（`cmd_survey` docstring 过时）。
- **未决**：抖音要点外发 DeepSeek 按协作偏好须单次授权，而 `xboard-daily-repush` 每日自动跑 `extract_points.py --new-only`——日常班是否算常设授权，待 Doctor 定。
