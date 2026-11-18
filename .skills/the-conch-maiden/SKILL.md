---
name: conch
description: Use this skill ONLY when the user explicitly types the slash command /conch (with a leading slash). Do NOT trigger on the plain word "conch" appearing in conversation. Two modes, both dry-run by default: (1) file health review and organization — one review covering stale files, multi-version files, finished communication files, backtests, naming, directory layout, retired projects and health scores, then each finding is handled the way it needs (tidy, archive, migrate, retire, optimize); (2) code audit (`--code`) — PRD coverage, code quality and blind-spot review via project-review. Each run reports the problems and the planned handling, has a subagent re-check them, and applies only what Doctor approves. File deletions go to the fuxi-station recycle bin (retire mode has two documented exceptions).
---

# Conch（海螺姑娘）· 文件健康审查及整理 ／ 代码审计

> 版本 2.0.0（2026-11-17）。正文真源＝`~/Documents/Claude/brain/.skills/the-conch-maiden/SKILL.md`（本文件）与同目录 `references/`；安装形态：`~/.claude/skills/the-conch-maiden` 为指向本目录的链接，不在那里改。发布登记 `code-only`（只在 Code 侧经链接加载，不往 Cowork 账号传）。
> 引擎：`~/Documents/Claude/Projects/海螺姑娘/conch_engine.py`；代码审计数据生成器：`~/Documents/Claude/Projects/海螺姑娘/project-review/review_agent.py`。项目档案：`brain/海螺姑娘/`；坑库：`Projects/海螺姑娘/GOTCHAS.md`。
> v 历史：1.0.0 以 v0.2 引擎版为底重写，替换 2026-04-30 的提示词版（GOTCHA-20261112-001）；同日修引擎两处误判（-002 新旧判反、-003 日期在前的备份被当无语义 .bak）。1.1.0 引擎 `scan`/`archive` 加 `--all` 全量清单与「合计待移」行，`protect: []` 与行内列表可正确解析（-004）。1.1.1 第 1 步加禁区：`Codex/Project Mirror` 不作为目标（Doctor 定）；同日引擎修 GOTCHA-20261113-001～005（现行版本、小数版本、空文件、引用检查、中段 `_old_`）。1.2.0 归档件改名 `<原文件名>.archived_YYYY-MM-DD` 平铺 `archived/`，同名循环查重、rollback 不覆盖（-006，Doctor 定）。1.3.0 第 3 步改为「全量预演 → 逐条核查 → 处理存疑与误判 → 确认 → 执行」，无误才 apply（Doctor 定）。1.4.0 新增 `--tidy` 整理模式与引擎只读子命令 `tidy-scan`（2026-11-17 Doctor 定，首例 EAL）：多版本合并归一并在文首落迭代记录、已完成沟通件删除、回测分诊、命名按项目范式统一；删除走 fuxi 回收站。归档模式不变。 1.5.0 改为文件整理与健康检查的总入口（2026-11-17 Doctor 令「所有文件整理，健康检查的流程对齐进 conch skill」，选择窗定：五种模式、meditation 与 project-review 只挂指针、细则拆 `references/`、本轮不改引擎）：原归档、整理两模式正文原样迁入 `references/archive.md`、`references/tidy.md`，回收站细则独立为 `references/recycle-bin.md` 并补三批实操；新增迁移（`references/migrate.md`）、退出（`references/retire.md`）、健康检查（`references/health.md`，接海螺健康度评分与三档一键优化）三模式；新增「通用纪律」一节。旧版全文备份 `_bak/SKILL.md.bak_2026-11-17_v1.5-split`。 2.0.0 五种模式并为两种（2026-11-17 Doctor 令「将 conch 的 5 种模式合并成 2 种：文件健康审查及整理，和代码审计，两种全部默认 dry-run，然后汇报哪里有问题、准备怎么处理，同时 subagent 复查，经我同意后 apply」「将整理、归档等统一整合为文件健康审查及整理，需要整理的整理，需要归档的归档」）：归档、整理、迁移、退出、健康检查并为「文件健康审查及整理」，一次审查、逐条按需处理（总则 `references/file-health.md`，原五份细则降为处理手段）；project-review 由指针升为「代码审计」模式（`references/code-audit.md`）；两模式共用七步流程；参数去掉 `--apply`、`--tidy`、`--migrate`、`--retire`、`--health`，新增 `--code`、`--prd`。1.5.0 全文备份 `_bak/SKILL.md.bak_2026-11-17_v2.0-twomode`。

## 运行模式（Doctor 定 · 2026-11-17）

> 「默认 dry-run 模式，然后汇报哪里有问题，准备怎么处理，同时 subagent 复查，经我同意后 apply。」

这是 conch 唯一的运行模式，两种模式、每一次调用都照此走，没有任何参数能跳过：
1. **默认 dry-run**——先只读审查，不改任何文件；
2. **汇报**——哪里有问题、准备怎么处理；
3. **同时 subagent 复查**——未参与审查的子代理独立复查问题与方案，结论随汇报一起给；
4. **经 Doctor 同意后 apply**——只执行同意的条目。

下文「七步流程」是这四点的展开（第 1 步定目标，第 7 步 apply 后回读核验）。

## 两种模式

| 模式 | 调用 | 审查什么（dry-run） | 怎么处理（经 Doctor 同意后 apply） | 细则 |
|---|---|---|---|---|
| **文件健康审查及整理** | `/conch [--scope <路径>]` | 陈旧件、版本链、多版本并存、散落备份、已完成沟通件、回测目录、命名违规、目录结构与归属、退出候选、健康度评分、GOTCHAS 状态与标准文件 | 每条问题按性质处理：需要整理的整理（合并归一、删沟通件、回测分诊、改名），需要归档的归档，需要迁移的迁移，该退出的退出，manifest 与 GOTCHAS 状态行按确认档动作同步；删文件进回收站（退出的「删本地靠远端留底」「删软链接」两种例外见 `references/retire.md`） | `references/file-health.md`（总则），处理手段见其中路由表 |
| **代码审计** | `/conch --code [--scope <路径>] [--prd <PRD 路径>]` | L0 PRD 交付标准、L1 功能覆盖、L2 代码质量十维、L3 PRD 精神盲区，对照项目开放 GOTCHAS | 按同意的条目改代码、补测试；功能性修复的验收归 Doctor | `references/code-audit.md` |

工具命令：`--explain <相对路径>`、`--rollback <session_id>`、`--init` 见 `references/archive.md` 末节，同样按运行模式走：`--explain` 只读，直接报；`--rollback` 先读 `.conch_audit.log` 报将移回哪些文件，`--init` 先报将生成的 `.conchconfig.yml` 内容，两者都经子代理复查、Doctor 同意后才执行。1.x 的 `--apply`、`--tidy`、`--migrate`、`--retire`、`--health` 不再区分模式：一律按「文件健康审查及整理」走，且不跳过 dry-run 与同意步骤。

**同属海螺「自检工具家」、不在本技能内的**（只列指针）：记忆与心灵健康 `Projects/海螺姑娘/meditation/SKILL.md`（`meditation.py`，月度班 `brain-monthly-checkup`）。

## 七步流程（两种模式共用）

1. **定目标**：见下文「第 1 步」。宣布模式与目标目录。
2. **审查（dry-run，只读）**：按模式细则跑检查，不改任何文件（审查产物只写 `$TMPDIR`）。
3. **汇报**：给出问题清单，每条写——位置、问题、证据（命令输出或文件:行）、准备怎么处理（哪种手段、改什么）、可逆方式、风险。按 🔴 必须处理 / 🟡 建议处理 / 🟢 可选 排序。引擎或脚本的线索要逐条核查后才进清单，核查不了的标「存疑」。
4. **子代理复查**：与汇报同时，开一个**未参与审查**的子代理独立复查问题清单与处理方案：逐条判「成立 / 不成立 / 存疑」、方案是否稳妥、有没有漏项（给它目标目录、清单与原始数据，不给结论倾向）。复查结论并入汇报；不成立的条目从拟处理清单里拿掉，存疑的不处理。
5. **Doctor 同意**：用 AskUserQuestion 问——按方案全部处理 / 只处理其中一部分 / 取消；方向性问题（研究边界、命名取向、删除方式、是否改代码行为）单独问，给推荐与理由。清单为 0 条就报告后结束。
6. **apply**：只执行 Doctor 同意的条目，按细则里对应手段的执行步骤做；先快照、查并发（通用纪律 1、2）。失败报错误原文后停止，不重试。
7. **回读与核验**：回读每条是否落实；开未参与实施的子代理实读核验（第 4 步的复查者同样未参与实施，可由它做差额核验）；实施者只报「已改、自验结果、待独立验收」。

## 原则

- **默认 dry-run**：两种模式的第 2、3、4 步都不改文件；没有 Doctor 在第 5 步的明确同意，不进第 6 步。健康度预览只写 `$TMPDIR`；回写 manifest 与看板的 `rescan` 也算 apply，要等同意。
- **先预演、逐条核查，无误再 apply**（2026-11-13 Doctor 定）。引擎靠文件名和修改时间打分，会误判（海螺 GOTCHA-20261112-002、-003，20261113-001～005），核查不能省。
- **归档只移不删**：归档＝引擎把文件移进目标目录（`--scope`，即项目根）下的 `archived/`，改名为 `<原文件名>.archived_YYYY-MM-DD`（同日同名加 -2、-3，不覆盖），并写 `.conch_audit.log`，可按 session 回滚。删除只用于整理与退出里 Doctor 同意的条目：删文件一律走回收站（`references/recycle-bin.md`）；退出里「删本地、靠远端留底」（先实测远端同步）与「删软链接、真身不动」两种不经回收站，见 `references/retire.md`。
- **文件健康审查及整理不改代码逻辑**：可改文档内容（合并、迭代记录、引用跟改）；迁移时可改代码与配置里的路径常量、路径推算表达式（如 `parents[N]` 改为按名字查找）、链接与引用；例外是 Doctor 同意的清单里明列的项目校验脚本（如命名规则随范式改动时同步其校验器）。不改 GOTCHAS 状态（确认档 `gotchas_status_sync` 例外，见「不做」）、不覆盖已有文件、不写记忆。退出只处置对象本身，并更新指向它的索引。
- **代码审计只改同意的条目**：不顺手重构、不扩大改动面（damper 改动面纪律）；不为让测试通过而弱化校验。
- 判定交给引擎与审查证据；Doctor 不同意某个判定时，用 `explain` 或证据给理由，不自行改判。修复、补文件、记忆分拣不在清单里的，走各自的常规流程（GOTCHAS 自动登记规则、`/save`）。

## 通用纪律（凡 apply 都适用）

1. **先快照**：动手前打 tar.gz 快照（放项目数据根 `backups/` 或 `brain/backups/`）；方案里承诺的快照要真做，没做就在迭代记录如实写。
2. **查并发**：动手前查目标目录近 2 小时有无别的会话写入（`find <目录> -type f -mmin -120`）；共管账本只做定点插入，不整篇重写。
3. **备份不被重跑覆盖**：给 Doctor 终端的命令里，备份一步写成 `[ -e 备份 ] || cp 原件 备份`；组合命令会被分段粘贴、重跑（通用教训 G-X120 2026-11-10、2026-11-17 两次复发）。备份按命名规则放同目录 `_bak/`：`<原文件名>.bak_YYYY-MM-DD_<语义>`。
4. **消费方扫描三种写法**：完整路径串、分段拼接、按层级推算，范围含 `~/.codex/automations`、`~/Library/LaunchAgents`、Cowork 班镜像（通用教训 G-X278；细则 `references/migrate.md` 第 1 步）。删除、归档、改名、迁移前都要扫，不只查目标目录内。
5. **冻结证据不改**：审读 JSON、`raw/`、记了脚本 SHA 的研究包、`archive/`、`_bak/`、只追加账本的旧条，路径与内容都是当时的事实；迁移时保持相对结构。
6. **跨侧改动不代做**：V.V.（Codex 侧）与 Cowork 云端班的改动，CC 写成可直接转达的请求，Doctor 转达；回执来了 CC 回读核对。
7. **终端命令按真实环境写**：本机 zsh（`while read` 会覆盖外层同名变量，G-X229）；fuxi 远端是 PowerShell 5.1（经验库 `EXP-20260822-002-T`）。
8. **独立核验**：执行完开未参与实施的子代理实读复核；实施者只报「已改、自验结果、待独立验收」。
9. **git 交 Doctor**：commit 与 push 由 Doctor 终端执行；提交清单逐文件列，不用 `git add -A`；仓根整体改名用改名配对清单 `--pathspec-from-file`。
10. **坑即登记**：引擎误判、工具非预期行为，按 GOTCHAS 自动登记规则写海螺 GOTCHAS；本技能不改引擎。

## 第 1 步 · 定目标目录

1. 有 `--scope` 就用它。
2. 没有就看本会话实际读写过的项目目录（含 `.git/`、`CLAUDE.md`、`GOTCHAS.md`、`README.md` 之一的目录）：恰好一个直接用；多个用 AskUserQuestion 让 Doctor 选；一个都没有就问 Doctor 要路径，**不要猜**。
3. 绝不以 `~`、`~/Documents` 或 `~/Documents/Claude` 这类根目录为目标。
4. 绝不以 `~/Documents/Codex/Project Mirror` 及其下任何子目录为目标（2026-11-13 Doctor 定）：那是 V.V. 的项目桥与镜像工作区，里面的审计、回测产物按对照组命名，引擎会误判。`--scope` 指向那里，或会话里只碰过那里，就告诉 Doctor 不做，然后停。

宣布：`🐚 目标目录：<路径>`

## 输出

在对话里汇报，不另写报告文件：

```
🐚 Conch 报告 · <日期> · <文件健康审查及整理 ｜ 代码审计>
目标：<路径>
审查：<跑了哪些检查，各自结果一句>
问题清单（<N> 条 · 🔴 <a> · 🟡 <b> · 🟢 <c>）：
  1. 🔴 <位置> — <问题>　证据：<…>　处理：<手段与改动>　可逆：<…>
  …
子代理复查：<PASS / PASS_WITH_LIMITS / FAIL> · 不成立 <x> · 存疑 <y> · 补漏 <z>
（dry-run，未改动任何文件）→ 待您同意后 apply
```

apply 之后再报一次：已处理 <N> 条（逐条落点）· 回滚方式 · 独立核验结论。各手段的原始输出格式（如归档预演的引擎摘要）见对应细则。

## 不做的事

- 不按 `☐` 找坑、不把条目改成 ✅（✅ 只由 Doctor 或未参与实施的审核者落）。例外：确认档 `gotchas_status_sync` 只把正文里已由 Doctor 或审核者落签的 ✅ 同步到状态行，须 Doctor 同意（`references/health.md` 第 3 步）。
- 文件健康审查及整理不往脚本里插 argparse / `main()`，不改代码逻辑（迁移改路径常量与路径推算表达式除外）；代码审计只改 Doctor 同意的条目。
- 不改 PRD 里的 checkbox（`[✓]` 由 Doctor 或指定独立验收方落）。
- 不重写「内容少」的已有文件。
- 不写 `~/.claude/projects/*/memory/`（记忆只落 Brain）。
- 不在阶段之间跳过确认；不改定时班；commit 与 push 交 Doctor。
