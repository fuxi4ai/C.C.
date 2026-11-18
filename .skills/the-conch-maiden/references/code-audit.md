# conch · 代码审计（`--code` · 2.0.0）

> 2026-11-17 Doctor 令：project-review 由指针升为 conch 的第二种模式，与文件健康审查及整理同走 SKILL.md 七步，默认 dry-run，子代理复查，经 Doctor 同意后 apply。
> 真源：`~/Documents/Claude/Projects/海螺姑娘/project-review/SKILL.md`（v3.0，审核维度、启发式规则 HEU-001～009 的定义以它为准）；数据生成器 `project-review/review_agent.py`；人工检查清单 `project-review/review_checklist.md`（在 project-review 根目录，不在 references/ 下）。

## 第 2 步 · 审查（只读）

1. **定 PRD**：有 `--prd` 用它；否则在目标目录找 `PRD*.md`，再在 `brain/logs/checkpoints/` 找文件名含项目名的 `*_PRD.md`；多个用 AskUserQuestion 让 Doctor 选；没有就跳过 L0/L1，并在汇报里写明「无 PRD，只审 L2/L3」。
2. **跑数据生成器**（只写 `$TMPDIR`）：
   ```bash
   cd "$TMPDIR" && python3 -B ~/Documents/Claude/Projects/海螺姑娘/project-review/review_agent.py -p "<目标>" --prd "<PRD>" -o "$TMPDIR/review_data.json" -q
   ```
   没有 PRD 时去掉 `--prd "<PRD>"`。脚本只写 `-o` 指定的文件（`review_agent.py` 唯一的写入在输出 JSON）。报错：照实报错误原文后停止。
3. **语义审查**（CC 读 JSON 与源码，不只看脚本结论）：
   - L0 PRD 交付标准是否真正完成；L1 缺失功能的影响与优先级；L2 十维质量与密度；L3 启发式规则之外的盲区。
   - 对照 `review_checklist.md` 逐项过一遍。
   - 读项目 GOTCHAS 的 🔄/⚠️ 开放条目，核对代码现状：已修未落签的、仍未修的、修法与登记不符的。
   - 「多想一步」四问（project-review SKILL Step 4）：核心用户最需要什么、数据量翻十倍还能不能跑、有没有单点故障、三个月后会后悔没做什么。
4. dry-run 阶段**不跑**项目测试：测试运行器本身会写缓存（pytest 的 `.pytest_cache/`、Python 的 `__pycache__/`），测试也可能写库或调外部接口。汇报里列出准备跑哪些测试；跑测试放到第 6 步 apply（修复前后各跑一次）。

## 第 3 步 · 汇报

每条：`文件:行` · 问题 · 证据（代码摘录或 PRD 条文）· 修法（改哪里、怎么改）· 影响面 · 需要补的测试 · 是否改变对外行为。按 🔴 必须修（功能缺失、安全、数据风险）/ 🟡 建议补充 / 🟢 优化排序。改变功能语义或对外行为的条目标「方向性」，第 5 步单独问。

## 第 4 步 · 子代理复查

按 project-review 的「审核者四原则」（严格、客观、逻辑性强、证据性强）派一个未参与审查的子代理：给它目标目录、PRD 路径、`$TMPDIR/review_data.json` 与问题清单，让它独立读代码，逐条判「成立 / 不成立 / 存疑」，并找清单外的盲区。复查结论并入汇报。

## 第 6 步 · apply（只做 Doctor 同意的条目）

- 改前：通用纪律 1、2（快照、查并发）；被改文件备份到同目录 `_bak/<原文件名>.bak_YYYY-MM-DD_<语义>`（`[ -e 备份 ] || cp …`）。
- 改动面只限同意的条目；声明的改动与实际 diff 逐条对上（damper）。
- 每条修复配一个能看见原问题的测试或复现；跑项目测试，失败就停下报告，不弱化断言、不跳过校验来求通过。
- 新发现的坑按 GOTCHAS 自动登记规则写项目 GOTCHAS（新条只标 🔄 或 ⚠️）。

## 第 7 步 · 核验

未参与实施的子代理读 diff、跑测试、回读实际消费端；实施者只报「已改、自验结果、待独立验收」。功能性修复的验收归 Doctor 或其指定方；PRD 里的 checkbox 按 PRD 合同，不代勾。commit 与 push 交 Doctor 终端。

## 不做

- 不在 `~/Documents/Codex/Project Mirror` 内审计或修改。
- 不改 PRD 文本与 checkbox。
- 不改定时班 prompt、不改跨项目 owner 线的代码（只出派工卡）。
- 不顺手重构、不改格式化风格等清单外内容。
