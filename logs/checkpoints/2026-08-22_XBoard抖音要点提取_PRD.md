---
title: PRD · XBoard 抖音要点提取
tags: [prd, acceptance, 科技资讯看板]
created: 2026-08-22 10:30
updated: 2026-08-22 22:44
status: delivered  # draft / in_progress / blocked / awaiting_acceptance / delivered / cancelled
task_authorization:
  state: verified
  source_type: 会话裁定
  source_ref: 2026-08-22 会话（本场）
  quote: 「X Board中"老毛聊交易"和"投知君君买方视角"，DVA不是会分析嘛，是否有每篇视频的精简总结，如果没有的话，X Board读快照更新的时候，能否加工每篇视频，在详情页用"要点"的形式呈现出来？」＋ AskUserQuestion 裁定「生成器内联+缓存（推荐）」＋「全量 718 篇（推荐）」＋ 范围修订「不需要补之前的，把之后形成的机制弄了就行」
  scope: X-Board 抖音两列详情页要点机制——新增提取器与缓存、生成器渲染要点块、每日班增量提取；不含存量回补
roles:
  implementers: [CC（提取器/生成器改造/班 prompt/验收）]
  independent_reviewers: [待派·未参与本场开发的 Task subagent]
acceptance_authority:
  authority: Doctor
  designation_source_ref: Doctor 为默认验收方（本场未另行指定独立验收方）
  designation_quote: 无独立验收方指定记录——验收方=Doctor
  designated_at: 2026-08-22
open_decisions: []
type: prd
project: 科技资讯看板（跨 DVA 数据链）
template_version: v1.2
---

# PRD · XBoard 抖音要点提取

## §一 · 任务目标

X-Board 抖音两列（老毛聊交易/投知君君买方视角）的详情页目前显示「摘要」=字幕前 260 字符截断（`dy_summary()`），不是总结。DVA 侧 analyzerLevel1/2 模块已移除（dva.js 恒为 null）、Level2 覆盖率 0%，没有现成的每篇精简总结可用。本任务建立「要点提取」机制：此后回流的新视频自动提取 3-5 条要点（主题/核心观点/关键数据/结论），详情页以「要点」块呈现；无要点的存量视频保持 260 字开头回退。**不做存量 718 篇回补**（Doctor 范围修订），仅建机制。

**Doctor 原始指令**(逐字引用):
> 「X Board中"老毛聊交易"和"投知君君买方视角"，DVA不是会分析嘛，是否有每篇视频的精简总结，如果没有的话，X Board读快照更新的时候，能否加工每篇视频，在详情页用"要点"的形式呈现出来？」
> AskUserQuestion Q1（方案）: 「生成器内联+缓存（推荐）」
> AskUserQuestion Q2（范围·后续修订）: 「全量 718 篇（推荐）」→ Doctor 修订: 「不需要补之前的，把之后形成的机制弄了就行」

**任务规模估算**:
- 预计涉及文件数: 5（extract_points.py 新 · points/ 缓存目录新 · gen_xboard_artifact.py 改 · xboard-daily-repush 班 prompt 改 · X-BOARD-OPERATIONS.md 改）
- 预计耗时: 约 1-2 小时
- 涉及项目: 科技资讯看板（X-Board 生成器 · 无 git）＋ 数据库 Douyin 只读

---

## §二 · 交付标准(Acceptance Criteria · 验收主体＝功能/需求)

### A. 功能需求（用户可感知的行为 / 结果）

- [✓] **R1** · X-Board 抖音详情页：机制上线后新回流的视频，点开详情页显示「要点」块（3-5 条 bullet 列表），不再只显示 260 字开头
  - 验收方法: 存在 ≥1 篇带要点缓存的视频 → 重建 artifact → 打开详情页目验「要点」块渲染；或机器比对生成的 HTML 含该视频的要点文本
  - 证据栏(实施者填): 样例篇 7676084633146035507（老毛 08-20）真实提取 5 条要点落缓存 → 生成器重建 → items-data 该 item points 字段含 5 条 → HTML 含「要点」容器（id=d-points 与 points-cap 各 1）→ update_artifact 推送 → Gateway 消费端 `Artifacts/x-board/index.html` Grep 命中「连续止损源于更高维度判断」（要点文本逐字在盘）。**渲染路径缺陷已修复（独立审查逮出 · 2026-08-22）**：douyin 分支曾有无条件兜底隐藏致要点块不可见——已删误置两行、X 分支补隐藏；重建后静态核验 JS 顺序（if 分支显示要点 L15-18 → else 回退 L20-23 → open L43 后无任何隐藏）→ 重推 SHA efadbaacb091 → 消费端 Grep 命中 `setHidden("d-points", false)` 显示语句
- [✓] **R2** · 无要点缓存的存量视频详情页保持回退行为（260 字开头摘要）不变
  - 验收方法: 取 1 篇无缓存存量视频 → 详情页显示 260 字开头、无「要点」块；HTML 比对回退分支
  - 证据栏(实施者填): 重建后 items-data 实测——16 篇抖音 item 中 1 篇有 points、15 篇 points 空且 summary 非空（回退样例「做交易，永远别让情绪指挥你！」summary 261 字符=260+省略号）✓ 与「转写」字样 0 同时满足
- [✓] **R3** · 每日班（xboard-daily-repush）自动为当日新回流视频提取要点——先跑 extract_points.py 增量再生成看板
  - 验收方法: 班 prompt 含提取段（update_scheduled_task 落盘）＋ 手动跑一次增量提取 exit 0（当日新篇 0 篇时输出「无新篇」属正常）
  - 证据栏(实施者填): update_scheduled_task 已改（prompt+description·含提取段与「严禁存量回补」边界）· 手动实跑 `extract_points.py --new-only` →「候选 103 篇 · 待提取 0 · 存量跳过 103 · 无新篇可提取 · 退出 0」exit 0

### B. 非功能需求（仅产品或系统质量属性）

- [✓] **N1** · 可靠性：单篇提取失败不阻塞看板生成——提取器失败篇跳过（或写 error 标记），生成器对无缓存篇一律回退 260 字开头
  - 验收方法: 人工构造 1 篇坏字幕/超时 → extract 不中断 → 生成器正常产出
  - 证据栏(实施者填): 负向实测已发生——首跑样例因 DeepSeek thinking 模式耗尽输出额度返回 parse_fail（llm-fail），脚本未崩溃、未落缓存、重试后成功；生成器在该状态下正常产出（written 670072 chars · 45 items）
- [✓] **N2** · 数据质量：要点只从该篇字幕提取，不引入外部知识——prompt 硬约束「只从字幕提取、禁脑补数字」
  - 验收方法: prompt 文本含该约束（可复核）＋ 抽 1 篇人工比对要点与字幕无外源事实
  - 证据栏(实施者填): extract_points.py 的 prompt 含「硬约束：只从字幕内容提取，不得引入字幕以外的知识；数字必须逐字引用字幕原值」· 样例篇 5 条要点逐条比对字幕（1127 字符）全部源自原文（主题/连续止损归因/离场三步/十笔降额）无外源事实

### C. 任务专属（自定义）

- [✓] **X1** · 机制锚日期可配置——`--since` 参数（默认 2026-08-22），存量回补可随时放开
  - 验收方法: `--since 2026-08-01 --dry-run` 输出应含存量候选篇（证明开关有效），正式回补仍待 Doctor 裁
  - 证据栏(实施者填): 实跑 `--since 2026-08-01 --dry-run` → 候选 103 篇 · 待提取 15 篇（列出 08-02~08-17 老毛篇标题与日期）· 不调 LLM ✓；班 prompt 已写「严禁 --all 或调早 --since 做存量回补（回补须 Doctor 另行裁定）」

### 分轨签核（v1.3 · 客观轨总 ✓ + 审查员背书 · 总签必须可审计）

- 客观轨总签（覆盖 R1/R2/R3/N1/N2/X1）：
  - covered_requirement_ids: [R1, R2, R3, N1, N2, X1]
  - authority: Doctor
  - designation_source_ref: PRD frontmatter acceptance_authority（默认验收方）· 本场 AskUserQuestion 总签
  - signed_at: 2026-08-22 22:44（北京时间 · 07:44 PDT）
  - result: PASS——六条客观轨全部 [✓]
  - reviewer_evidence_ref: 独立审查员背书记录（2026-08-22 · subagent a707df93ba7d53e1b · R2/R3/N1/N2/X1 成立 · R1 修复后复验通过）
- 原则轨（结论/裁定类）共 0 条：开发中 Doctor 已拍板（方案 A/范围修订）均走变更记录，不重复列原则轨

**独立审查员背书记录（2026-08-22 · Task subagent a707df93ba7d53e1b · 未参与开发）**：
- 裁定：R2/R3/N1/N2/X1 成立；R1 首审不成立（JS 渲染顺序缺陷——douyin 分支误置的无条件兜底隐藏致要点块不可见、空详情体），CC 已修复并复验——重建后逐行核验 douyin 分支 L15-18 显示/L20-23 回退/L43 open 后零隐藏 + 消费端 Grep 命中显示语句（SHA efadbaacb091）。
- 验证动作：① 重跑 extract --new-only（exit 0·0 新篇）② 重跑 --since 2026-08-01 --dry-run（候选 14·不调 LLM）③ 生成器 /tmp 副本重跑（670072 chars·45 items）④ 5 条要点 vs 1127 字字幕逐条溯源（全源自字幕）⑤ 读两脚本+班 SKILL.md+运维 §9.5 全文 ⑥ Gateway 消费端 Grep。
- 附带发现（不阻断）：样例篇提取参数非默认（create_time 08-20 早于锚，系开发期指定提取）；PRD 证据计数时点漂移（缓存落盘前后 103→102/15→14）；提取器 exit 2 区分度弱（班 prompt 纪律兜底）；--new-only 纯显式开关。

---

## §2.5 · 执行与交付清单（过程项 · 不参与功能交付关闭判定 · 无 checkbox 表格）

| task_id | 过程项 | task_status | 证据 |
|---|---|---|---|
| T1 | `X-Board/extract_points.py` 已建（提取+缓存+--new-only/--since+重试） | done | py_compile exit 0 · --new-only 实跑 exit 0 · thinking disabled 修复（2026-08-22 实测） |
| T2 | `X-Board/points/` 缓存目录已建且写入样例 | done | points/7676084633146035507.json 在盘（5 条要点·generated_at 2026-08-22T12:23Z） |
| T3 | `gen_xboard_artifact.py` 加 dy_points + 详情页要点块 + CSS | done | 重建 exit 0 · items-data 1 篇 points 非空 · HTML 含 d-points 容器 |
| T4 | xboard-daily-repush 班 prompt 更新（提取段） | done | update_scheduled_task 返回 prompt+description updated |
| T5 | X-BOARD-OPERATIONS.md 加要点提取运维节 | done | §9.5 已落盘（机制锚/回补开关/失败模式/验收锚） |
| T6 | 验收链路实跑（提取→生成→回读）+ PRD 证据回填 | done | R1-R3/N1/N2/X1 六条 [?]+证据 · Gateway 回读命中 |
| T7 | /save 触发 + 贴 PRD 路径（brain 留痕） | todo | 回报中建议 /save |

---

## §三 · 非交付项(范围排除)

- 不包含: 存量 718 篇（老毛 522 + 投知 196）要点回补——Doctor 明示「不需要补之前的」
- 不包含: DVA 侧 level2 分析重建（dva.js 分析模块已移除，重建属另批）
- 不包含: 生产版 Next.js 详情页同步（TODO「需动服务端 schema · 另批」）
- 不包含: 要点入库 canonical（要点是呈现层产物，渊图铁律不适用）
- 不包含: 全量批跑的首跑（仅跑 --new-only 增量链路验证）

---

## §四 · 状态（current_status + 变更历史 · frontmatter status 为唯一真源）

**状态变更历史**（只追加实际发生的行）:
| 时间 | 从 → 到 | 谁 | 依据 |
|---|---|---|---|
| 2026-08-22 10:30 | draft → in_progress | CC | 任务已授权（Doctor 本场裁定方案+范围修订）· 立卷后进入执行 |
| 2026-08-22 13:00 | in_progress → awaiting_acceptance | CC | 六条交付标准全填 [?]+证据 · 全链路实跑验收（提取→生成→Gateway 回读命中） |
| 2026-08-22 22:44 | awaiting_acceptance → delivered | Doctor | 总签（AskUserQuestion · 六条客观轨全部 [✓] · CC 代记留痕） |

---

## §五 · 变更记录

- 2026-08-22 10:30 CC: 立 PRD · 6 条交付标准（R1-R3/N1-N2/X1）· task_authorization 已记录（Doctor 原话 + 两轮 AskUserQuestion 裁定）
- 2026-08-22 CC: Doctor 范围修订「不需要补之前的，把之后形成的机制弄了就行」——§一 动机与 §三 非交付项同步；X1 机制锚日期即此裁定的落地载体
- 2026-08-22 CC: 首跑验收发现 DeepSeek thinking 模式耗尽输出额度（parse_fail 实测）→ 提取器加 thinking disabled + max_tokens 3000，修复后样例提取成功（5 条要点）
- 2026-08-22 CC: 六条全填 [?]+证据 → awaiting_acceptance
- 2026-08-22 CC: 独立审查（subagent a707df93）逮出 R1 阻断——douyin 分支误置无条件兜底隐藏（Edit old_string 匹配到同型序列误落位置）→ 修复（删误置两行+X 分支补隐藏）→ 重建复验（SHA efadbaacb091）→ update_artifact 重推 → 消费端 Grep 命中显示语句。教训记：同文件多处同型代码块的 Edit 必须带唯一上下文锚（已记 memory）
- 2026-08-22 CC: 独立审查背书记录落分轨签核小节；附带发现四条（样例参数/计数时点/exit2 区分度/--new-only 装饰性）如实保留
- 2026-08-22 22:44 Doctor: 总签——六条交付标准全部 [✓]（CC 代记留痕 · 分轨签核已落 · status → delivered）
- 2026-08-22 22:47 Doctor: 裁定存量 103 篇不回补——X1 机制锚保留作应急，回补通道不启用（销账留痕）
