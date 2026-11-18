# conch · 处理手段：归档（文件健康审查及整理）

> 自 SKILL.md 1.4.0 原第 2、3 步与「其他模式」原样迁入（1.5.0 拆分，正文未改）。通用纪律与确认节点见 SKILL.md。
> 2.0.0 起归档不再是独立模式，是「文件健康审查及整理」的处理手段之一（总则 `file-health.md`）。没有 `--apply` 参数了：文中「带 / 没有 `--apply`」读作「Doctor 是否已在 SKILL.md 七步第 5 步同意」；「按『输出』格式」指本文件末节的归档预演摘要格式；第 3 步第 4 点的确认并入七步第 5 步；第 2 步末「汇报后结束」在 2.0 里指停在七步第 3 步，等第 4 步复查与第 5 步同意，不是整个流程结束。末节 `--rollback`、`--init` 也按 SKILL.md 运行模式走：先报将移回的文件或将生成的配置内容，子代理复查，Doctor 同意后才执行。
> 注意：SKILL.md 通用纪律第 4 条要求归档前跨项目、按三种写法扫消费方，比下方第 3 步第 2 点只在目标目录内 grep 更宽，以通用纪律为准。

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

## 手工归档单个文件（引擎不判陈旧时）

> 2.1.0 补（X-Board 首例）。引擎的 `archive --apply` 只移走它判为陈旧的文件；审查判定该归档、而引擎不判陈旧的单件（如已执行的一次性补丁），经 Doctor 同意后手工移动：

1. 目标 `<目标>/archived/<原文件名>.archived_YYYY-MM-DD`，已存在就加 -2、-3，不覆盖；`mkdir -p archived` 后 `mv -n`（目标已存在就不移），再 `cmp` 快照里的原件确认字节相同。
2. 引擎不会为它写 `.conch_audit.log`，不能用 `--rollback` 回滚：在项目迭代记录（或 README 迭代记录）与会话日志里各记一行「原路径 → 归档路径 · 日期 · 理由」；回滚＝把文件移回原路径。
3. 移动前照常按通用纪律第 4 条扫引用；有现行引用的不归档。

## 其他模式

- `--explain <相对路径>`：`... --scope "<目标>" explain <相对路径>`，报得分和理由。
- `--rollback <session_id>`：先向 Doctor 确认 session_id 与目标目录，再 `cd "<目标>" && ... --scope "<目标>" rollback <session_id>`，回读文件已回到原位。
- `--init`：`... --scope "<目标>" init` 生成 `.conchconfig.yml`（已存在则不覆盖；`--force` 只在 Doctor 明确要求时用）。

## 归档预演摘要格式（1.x 原 SKILL.md「输出」节，原样迁入）

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
