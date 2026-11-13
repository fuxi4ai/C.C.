---
name: conch
description: Use this skill ONLY when the user explicitly types the slash command /conch (with a leading slash). Do NOT trigger on the plain word "conch" appearing in conversation. Project-maintenance pass backed by conch_engine.py — dry-run scan by default, archive only on explicit approval, report back.
---

# Conch（海螺姑娘）· 项目整理

> 版本 1.3.0（2026-11-13）。正文真源＝`~/Documents/Claude/brain/.skills/the-conch-maiden/SKILL.md`；安装形态：`~/.claude/skills/the-conch-maiden` 为指向本目录的链接（2026-11-12 起，由 Doctor 终端改链接；改好之前 `/conch` 仍加载旧版），不在那里改。
> 引擎：`~/Documents/Claude/Projects/海螺姑娘/conch_engine.py`。项目档案：`brain/海螺姑娘/`；坑库：`Projects/海螺姑娘/GOTCHAS.md`。
> v 历史：1.0.0 以 v0.2 引擎版为底重写，替换 2026-04-30 的提示词版（GOTCHA-20261112-001）；同日修引擎两处误判（-002 新旧判反、-003 日期在前的备份被当无语义 .bak）。1.1.0 引擎 `scan`/`archive` 加 `--all` 全量清单与「合计待移」行，`protect: []` 与行内列表可正确解析（-004）。1.1.1 第 1 步加禁区：`Codex/Project Mirror` 不作为目标（Doctor 定）；同日引擎修 GOTCHA-20261113-001～005（现行版本、小数版本、空文件、引用检查、中段 `_old_`）。1.2.0 归档件改名 `<原文件名>.archived_YYYY-MM-DD` 平铺 `archived/`，同名循环查重、rollback 不覆盖（-006，Doctor 定）。1.3.0 第 3 步改为「全量预演 → 逐条核查 → 处理存疑与误判 → 确认 → 执行」，无误才 apply（Doctor 定）。

## 原则

- **默认只预演**。不带 `--apply` 只跑只读的 `detect` / `scan`，报完即停。
- **先预演、逐条核查，无误再 apply**（2026-11-13 Doctor 定）。即使带了 `--apply`，也必须先跑全量预演，把每个拟归档文件逐条核查完、清单里只剩确认过期的文件，再经 Doctor 确认后执行。引擎靠文件名和修改时间打分，会误判（海螺 GOTCHA-20261112-002、-003，20261113-001～005），核查不能省。
- **只移不删**。归档＝引擎把文件移进目标目录（`--scope`，即项目根）下的 `archived/`，改名为 `<原文件名>.archived_YYYY-MM-DD`（同日同名加 -2、-3，不覆盖），并写 `.conch_audit.log`，可按 session 回滚。
- **本技能只做归档**。不改代码、不改 GOTCHAS 状态、不覆盖已有文件、不写记忆。修复、补文件、记忆分拣走各自的常规流程（GOTCHAS 自动登记规则、`/save`），不在这里顺手做。
- 判定交给引擎；Doctor 不同意某个判定时，用 `explain` 给理由，不自行改判。

## 参数

`/conch [--scope <路径>] [--apply] [--explain <相对路径>] [--rollback <session_id>] [--init]`

## 第 1 步 · 定目标目录

1. 有 `--scope` 就用它。
2. 没有就看本会话实际读写过的项目目录（含 `.git/`、`CLAUDE.md`、`GOTCHAS.md`、`README.md` 之一的目录）：恰好一个直接用；多个用 AskUserQuestion 让 Doctor 选；一个都没有就问 Doctor 要路径，**不要猜**。
3. 绝不以 `~`、`~/Documents` 或 `~/Documents/Claude` 这类根目录为目标。
4. 绝不以 `~/Documents/Codex/Project Mirror` 及其下任何子目录为目标（2026-11-13 Doctor 定）：那是 V.V. 的项目桥与镜像工作区，里面的审计、回测产物按对照组命名，引擎会误判。`--scope` 指向那里，或会话里只碰过那里，就告诉 Doctor 不做，然后停。

宣布：`🐚 目标目录：<路径>`

## 第 2 步 · 预演（总是先跑）

```bash
cd "$TMPDIR" && python3 -B ~/Documents/Claude/Projects/海螺姑娘/conch_engine.py --scope "<目标>" detect
cd "$TMPDIR" && python3 -B ~/Documents/Claude/Projects/海螺姑娘/conch_engine.py --scope "<目标>" scan
```

- 用 `-B`，不在被扫目录留 `.pyc`。
- 引擎缺失或报错：照实报错误原文后停止，**不要退回按提示词手工整理**（旧版那样做在 brain / 知识图谱项目里不安全）。
- 只读补查（任选）：GOTCHAS 里状态为 🔄/⚠️ 的开放条数，缺哪些标准文件（README / GOTCHAS / TODO）。只报告，不动手。

没有 `--apply` → 按「输出」格式汇报后**结束**。

## 第 3 步 · 归档（仅 `--apply`）

1. **全量预演**：跑 `... --scope "<目标>" scan --all` 取全量清单（`archive` 移走的是「拟归档 ∪ 版本链超额」两张清单的并集，默认输出各有截断）。核对**去重后**的文件数与输出末行「archive --apply 将移走合计: N」一致（同一文件可能同时出现在两张清单里，行数之和会大于合计）；对不上就停下报告。
2. **逐条核查**（只读，每个文件都要做，不抽查）：
   - 引用：`grep -rn --exclude-dir=archived --exclude-dir=_bak -F "<文件名>" "<目标>"`；`.py` 另查 `import <模块名>`/`from <模块名>`；代码动态拼名的（如 `label + '_daily.csv'`）按目录里生成它的脚本判断。
   - 版本：引擎说「有更新同伴」的，打开新旧两份确认新版确实取代了旧版（不是并行的独立测试、不是新版仍 import 旧版）。
   - 用途：看所在目录与 README，排除审计证据、回测或实验产物、对照组、`outputs/final/` 定稿、数据集、被调度或 manifest 指向的文件。
   - 空文件：确认不是占位、锁、日志输出目标、包标记。
   - 列成表给 Doctor：文件 · 引擎理由 · 核查结论（确认过期 / 存疑 / 误判）· 证据一句。
3. **存疑与误判一律不归档**。属于引擎规则缺陷的误判，按 GOTCHAS 自动登记规则登记到海螺 GOTCHAS；本技能不改引擎。
4. **确认**：用 AskUserQuestion 让 Doctor 选：归档已确认的 N 件 / 只归档其中一部分 / 取消。选「一部分」就再问 Doctor 要哪几件，N 改为这几件的件数。清单为 0 件，或核查后没有可确认的文件，就报告后结束，不执行。
5. **写 protect 并复核**：先备份 `.conchconfig.yml`（按命名规则放 `_bak/`；没有该文件就先 `init`，见下）。**误判**的文件长期写进 `protect:`（它们本来就不是旧件）；**存疑**的和本次没选中的只是本次排除，也写进 `protect:`，执行完第 7 步后从备份恢复配置，不让它们长期留在 protect 里，下次仍会被列出、重新核查。写成多行列表（`protect:` 换行后逐行 `  - "<glob>"`）。重跑 `scan --all`：清单必须与 Doctor 确认的文件逐一相同、合计等于 N；不一致就停下报告、恢复配置，不执行。
6. 执行：
   ```bash
   cd "<目标>" && python3 -B ~/Documents/Claude/Projects/海螺姑娘/conch_engine.py --scope "<目标>" archive --apply --yes
   ```
   `cd` 到目标目录再跑，稳妥起见（GOTCHA-20261106-003 的相对路径问题已修，这里仍保持同一习惯）。
7. 回读：数 `.conch_audit.log` 末行 `moved` 的条数（`tail -1 .conch_audit.log | python3 -c 'import json,sys;print(len(json.load(sys.stdin)["moved"]))'`），核对与清单一致，并抽查 `archived/` 下对应的 `.archived_<日期>` 文件确实存在（按日期 grep 会把同日早先的归档也算进去，不能用来计数）；从输出或 `.conch_audit.log` 末行取 session_id。然后按第 5 步恢复配置（保留误判那几条 protect），回读确认。
8. 只跑一次。失败就报错误原文，按第 5 步恢复配置后停止，不重试。

## 其他模式

- `--explain <相对路径>`：`... --scope "<目标>" explain <相对路径>`，报得分和理由。
- `--rollback <session_id>`：先向 Doctor 确认 session_id 与目标目录，再 `cd "<目标>" && ... --scope "<目标>" rollback <session_id>`，回读文件已回到原位。
- `--init`：`... --scope "<目标>" init` 生成 `.conchconfig.yml`（已存在则不覆盖；`--force` 只在 Doctor 明确要求时用）。

## 输出

在对话里汇报，不另写报告文件：

```
🐚 Conch 报告 · <日期>
目标：<路径>　类型：<project_type>　配置：<有/无 .conchconfig.yml>
扫描 <N> 个文件 · 拟归档 <N> · 版本链超额 <N>
拟归档：
  - <文件> — <理由>
（预演，未改动任何文件）｜ 已归档 <N> 个 → archived/（*.archived_<日期>）· session <id>
开放 GOTCHAS：<N> 条（只读统计）　缺少标准文件：<列表或「无」>
```

## 不做的事（与旧版的区别）

- 不按 `☐` 找坑、不把条目改成 ✅（✅ 只由 Doctor 或未参与实施的审核者落）。
- 不往脚本里插 argparse / `main()`，不改任何代码。
- 不重写「内容少」的已有文件。
- 不写 `~/.claude/projects/*/memory/`（记忆只落 Brain）。
- 不在阶段之间跳过确认。
