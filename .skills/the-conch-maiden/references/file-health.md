# conch · 文件健康审查及整理（总则 · 2.0.0）

> 2026-11-17 Doctor 令：整理、归档、迁移、退出、健康检查统一为「文件健康审查及整理」——一次审查，**需要整理的整理，需要归档的归档**。流程即 SKILL.md 七步；本文件写第 2 步查什么、第 3 步每类问题用哪种手段处理。各手段的执行细节在下面路由表指向的文件里。

## 第 2 步 · 审查清单（只读，全部跑，结果都进汇报）

在 `cd "$TMPDIR"` 下跑，引擎一律 `python3 -B`，不在被扫目录留 `.pyc`。引擎缺失或报错：照实报错误原文后停止，不退回手工整理。

| # | 检查 | 命令或做法 | 产出的问题类型 |
|---|---|---|---|
| A | 项目类型与陈旧件 | `python3 -B ~/Documents/Claude/Projects/海螺姑娘/conch_engine.py --scope "<目标>" detect`；同上 `scan --all` | 拟归档、版本链超额 |
| B | 整理线索 | `python3 -B ~/Documents/Claude/Projects/海螺姑娘/conch_engine.py --scope "<目标>" tidy-scan --json` | 版本族（多版本并存）、散落备份、已完成沟通件候选、项目内无引用的回测目录、命名违规 |
| C | 健康度 | 目标在 `Projects/海螺姑娘/data/asset_manifest.json` 里有节点时：`python3 -B ~/Documents/Claude/Projects/海螺姑娘/conch_engine.py survey --out "$TMPDIR/survey_preview.json"`，读该节点 `score`（五维、总分、A–D）与扣分最多的维度 | 健康度偏低的维度、陈旧自检、策展值失准 |
| D | 结构与归属 | 读目录树与 README：只装了一个子项目的嵌套层、放错上级的目录、与项目边界不符的研究（如 EAL 边界：凡「事件对行情的影响」都留 EAL） | 迁移候选 |
| E | 退出候选 | 长期无修改、无 git 新提交、无定时班或 launchd、无消费方的项目、目录、文档；软链接与副本 | 退出候选 |
| F | 标准文件与坑库 | 缺 README / GOTCHAS / TODO；GOTCHAS 里 🔄/⚠️ 开放条数；正文已落签 ✅ 而状态行未同步的条目（`GAI_MANIFEST="$TMPDIR/survey_preview.json" PYTHONDONTWRITEBYTECODE=1 python3 -B ~/Documents/Claude/Projects/海螺姑娘/dashboard/optimize_actions.py run gotchas_stale_check <节点>`——指向 C 的预览，读当轮数据；不指向就读真 manifest 里上次回写的旧字段。`PYTHONDONTWRITEBYTECODE=1` 防止它 import 引擎时在海螺根写 `__pycache__`） | 补标准文件、状态行同步 |

**逐条核查**（进清单前，每条都做，不抽查）：引用按 SKILL.md 通用纪律第 4 条跨项目扫三种写法；版本类打开新旧两份确认新版确实取代旧版；用途类看所在目录与 README，排除审计证据、回测或实验产物、对照组、定稿、数据集、被调度或 manifest 指向的文件；空文件确认不是占位、锁、日志输出目标、包标记。细则同 `archive.md` 第 3 步第 2 点。

## 第 3 步 · 每类问题怎么处理（路由表）

| 问题类型 | 处理手段 | 执行细则 |
|---|---|---|
| 陈旧件、版本链超额（确认过期、无人引用） | **归档**：移入 `archived/`，可回滚 | `archive.md` 第 3 步 |
| 同一文件多版本并存、逐轮复核稿、散落快照 | **整理·合并归一**：合成一份现行件，文首落迭代记录，再删旧版 | `tidy.md` 规则 1 |
| 已完成的委托、知会、申请、请求、交付说明 | **整理·删除**（有用的一两句并入结果件迭代记录） | `tidy.md` 规则 2 |
| 回测目录 | **整理·回测分诊**：有引用的保留，被取代的删除，有历史意义的移入 `archive/` | `tidy.md` 规则 3 |
| 命名违规 | **整理·改名**并跟改引用 | `tidy.md` 规则 4 |
| 嵌套层、放错上级、边界外的研究 | **迁移** | `migrate.md` |
| 不再使用的项目、目录、文档、软链接 | **退出**：删本地靠远端留底 / 进回收站 / 移入 brain 快照 / 删链接 | `retire.md` |
| manifest 策展值失准、状态行未同步、缺标准文件 | **确认档优化动作**（`manifest_fix`、`gotchas_status_sync`、`fill_workfiles`） | `health.md` 第 3 步 |
| 看板与 manifest 需要刷新 | **`rescan`**（先备份 manifest，再 survey 与重建看板） | `health.md` 第 1 步 |
| 任何删除 | **回收站** | `recycle-bin.md` |
| 引擎误判、工具非预期行为 | 不处理文件，登记海螺 GOTCHAS | SKILL.md 通用纪律第 10 条 |

细则按清单里实际命中的手段读，用不到的不读（1.5.0「每次只读用到的那份细则」的 2.0 读法）。

一个对象可能同时命中几类（如旧回测既是版本链超额又是回测目录）：按路由表从上到下取最贴切的一种，汇报里写明为什么选它。

## 与各细则内确认步骤的关系

`archive.md` 第 3 步第 4 点、`tidy.md` 流程第 2 步、`migrate.md` 第 2 步、`retire.md` 第 1 步、`health.md` 确认档里的「交 Doctor 确认」，在 2.0 里都并入 SKILL.md 七步的第 5 步：一次汇报、一次同意，不逐手段重复问；子代理复查（第 4 步）排在同意之前。迁移的切换方案、退出的逐对象判定仍要写进汇报，供 Doctor 一并决定。细则里「先用 AskUserQuestion 问」的方向性问题，也放到第 5 步、子代理复查之后一起问。

## 汇报要点

问题清单按路由表分组：归档 / 整理 / 迁移 / 退出 / 优化动作 / 登记，各组给条数；健康度单列一段（节点得分、等级、扣分维度、与上次运行相比）。删除类条目注明进回收站与保留期。
