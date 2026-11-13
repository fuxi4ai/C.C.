---
name: conch
description: Use this skill ONLY when the user explicitly types the slash command /conch (with a leading slash). Do NOT trigger on the plain word "conch" appearing in conversation. Project-maintenance pass backed by conch_engine.py — dry-run scan by default, archive only on explicit approval, report back.
---

# Conch（海螺姑娘）· 项目整理

> 版本 1.1.0（2026-11-12）。正文真源＝`~/Documents/Claude/brain/.skills/the-conch-maiden/SKILL.md`；安装形态：`~/.claude/skills/the-conch-maiden` 为指向本目录的链接（2026-11-12 起，由 Doctor 终端改链接；改好之前 `/conch` 仍加载旧版），不在那里改。
> 引擎：`~/Documents/Claude/Projects/海螺姑娘/conch_engine.py`。项目档案：`brain/海螺姑娘/`；坑库：`Projects/海螺姑娘/GOTCHAS.md`。
> v 历史：1.0.0 以 v0.2 引擎版为底重写，替换 2026-04-30 的提示词版（GOTCHA-20261112-001）；同日修引擎两处误判（-002 新旧判反、-003 日期在前的备份被当无语义 .bak）。1.1.0 引擎 `scan`/`archive` 加 `--all` 全量清单与「合计待移」行，`protect: []` 与行内列表可正确解析（-004）。

## 原则

- **默认只预演**。不带 `--apply` 只跑只读的 `detect` / `scan`，报完即停。
- **只移不删**。归档＝引擎把文件移进 `archived/<日期>/` 并写 `.conch_audit.log`，可按 session 回滚。
- **本技能只做归档**。不改代码、不改 GOTCHAS 状态、不覆盖已有文件、不写记忆。修复、补文件、记忆分拣走各自的常规流程（GOTCHAS 自动登记规则、`/save`），不在这里顺手做。
- 判定交给引擎；Doctor 不同意某个判定时，用 `explain` 给理由，不自行改判。

## 参数

`/conch [--scope <路径>] [--apply] [--explain <相对路径>] [--rollback <session_id>] [--init]`

## 第 1 步 · 定目标目录

1. 有 `--scope` 就用它。
2. 没有就看本会话实际读写过的项目目录（含 `.git/`、`CLAUDE.md`、`GOTCHAS.md`、`README.md` 之一的目录）：恰好一个直接用；多个用 AskUserQuestion 让 Doctor 选；一个都没有就问 Doctor 要路径，**不要猜**。
3. 绝不以 `~`、`~/Documents` 或 `~/Documents/Claude` 这类根目录为目标。

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

1. 先跑 `... --scope "<目标>" scan --all` 取全量清单（`archive` 移走的是「拟归档 ∪ 版本链超额」两张清单的并集，默认输出各有截断）。把两张清单逐条列给 Doctor（文件 + 引擎理由），并核对**去重后**的文件数与输出末行「archive --apply 将移走合计: N」一致（同一文件可能同时出现在两张清单里，行数之和会大于合计）；对不上就停下报告。然后用 AskUserQuestion 确认：全部归档 / 剔除部分后归档 / 取消。
   - 清单里有 `_vN` 文件、`.bak_*` 备份、或被代码/文档引用的文件（`grep -rn <文件名> <目标>` 有命中）→ 单独标出，提醒逐条看。
2. Doctor 要剔除的文件写进目标目录 `.conchconfig.yml` 的 `protect:`（没有该文件就先 `init`，见下）。写成多行列表（`protect:` 换行后逐行 `  - "<glob>"`）。改完重跑 `scan --all`，确认清单和合计都已变。
3. 执行：
   ```bash
   cd "<目标>" && python3 -B ~/Documents/Claude/Projects/海螺姑娘/conch_engine.py --scope "<目标>" archive --apply --yes
   ```
   `cd` 到目标目录再跑，稳妥起见（GOTCHA-20261106-003 的相对路径问题已修，这里仍保持同一习惯）。
4. 回读：`ls archived/<日期>/` 核对移走的文件数与清单一致；从输出或 `.conch_audit.log` 末行取 session_id。
5. 只跑一次。失败就报错误原文并停止，不重试。

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
（预演，未改动任何文件）｜ 已归档 <N> 个 → archived/<日期>/ · session <id>
开放 GOTCHAS：<N> 条（只读统计）　缺少标准文件：<列表或「无」>
```

## 不做的事（与旧版的区别）

- 不按 `☐` 找坑、不把条目改成 ✅（✅ 只由 Doctor 或未参与实施的审核者落）。
- 不往脚本里插 argparse / `main()`，不改任何代码。
- 不重写「内容少」的已有文件。
- 不写 `~/.claude/projects/*/memory/`（记忆只落 Brain）。
- 不在阶段之间跳过确认。
