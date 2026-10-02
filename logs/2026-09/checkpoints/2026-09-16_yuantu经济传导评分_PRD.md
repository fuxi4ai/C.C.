---
title: PRD · yuantu_scoring 经济传导评分改造
tags: [prd, acceptance, 渊图, 龙鱼五力]
created: 2026-09-16 21:30
updated: 2026-09-17
status: delivered
task_authorization:
  state: verified
  source_type: 问答板
  source_ref: 问答板 2026-09-16 4A（Doctor 勾选「按候选改」）
  quote: "评分已在龙鱼消费链上，「关联≠受益」是语义缺陷：保留相关度/覆盖分、另建经济传导路径（受益方向/收入利润暴露/客户验证/替代路线/兑现时间）只让有经济含义的有向路径影响受益判断 + 验证用例（新增同义词不跳变）+ 缓存键含图谱哈希"
  scope: Database/行业研究/yuantu_scoring.py + test_yuantu_scoring.py；不动 scoring/*_scores.json 人工分值、不动五力引擎消费端、不动 τ 锚集
roles:
  implementers: [CC(本场)]
  independent_reviewers: [未参与实施 subagent]
acceptance_authority:
  authority: Doctor
  designation_source_ref: Settings 全局条「事实性非功能性修复的验收（2026-09-01）」——功能性（评分行为语义）验收归 Doctor
  designated_at: 2026-09-01
open_decisions: []
type: prd
project: 渊图 / 龙鱼五力
template_version: v1.2
---

# PRD · yuantu_scoring 经济传导评分改造

## §一 · 任务目标

渊图 GOTCHAS NOTE-20260911-002（VV 独立审计 2.3 节）：yuantu_scoring 以无向化图距+度参与公司结构评分（关联≠受益），且 `_GRAPH_CACHE` 一次加载、图谱版本更新后不失效。问答板 4A Doctor 裁「按候选改」：

① 保留相关度/覆盖分（tau_key/稀缺/替代/成熟/浮现度/甄别六维不动）；② 另建经济传导路径维度 `economic_transmission`（ET，0-10）——只让有经济含义的**有向**边影响受益判断：受益方向（supplies/used_in/enables/part_of/causes 加权出边）+ 下游采用方（supplies/used_in 出边去重目标×1.5 cap3）为正项，外部约束（constrains 入边）/兑现门槛（constrains 出边→event_）/替代压力（competes_with 去重）为负项；③ 验证用例固化：「新增同义词/引用但无经济新事实时，经济排名不跳变」（持久化负向测试）；④ 缓存键含输入文件指纹（realpath+mtime_ns+size），图谱版本更新缓存自动失效。

**评分公式变更**：weighted_total += ET×1.0（scoring_version v1.1→v1.2）；六维共享维度逐位不变（真图回归锚）。**影响面**：总分上限 105→115，tier 阈值不变——分数只升不降，接近阈值的公司可能升档（升档=原覆盖分被低估的受益面补正，方向与修复意图一致）。

## §二 · 交付标准

- [✓] **R1** · 经济传导维度接入：dimensions 新增 economic_transmission（score/benefit_raw/customers/constraints_in/realization_gates/alternative_pressure），weighted_total 加 ET×1.0，scoring_version=v1.2
  - 证据: 真图实跑 14 家评分库全接通 · get_company_score 回读字段齐
- [✓] **R2** · 验证用例（候选定式）：新增非经济边（is_a 等同义词/引用）→ ET 不跳变；新增经济边（supplies）→ ET 响应上升
  - 证据: test A1/A2 断言过（6.3 vs 6.3 · 6.3→7.1）
- [✓] **R3** · 缓存失效门禁：图谱文件改写后 _load_graph 重载（指纹变化即失效），不拿旧图评新司
  - 证据: test B1a（同指纹命中）/B1b（改写后重载）断言过
- [✓] **R4** · ET 语义完整：无经济信号=0 · 正项加权+cap · 负项扣分 · clamp[0,10]
  - 证据: test C1-C4 断言过
- [✓] **R5** · 共享维度回归：tau_key/scarcity/replacement/maturity/graph_degree/integrity 与原公式逐位一致，weighted_total 差=ET 且仅=ET
  - 证据: test D1 真图抽样 13 家全一致（实跑）
- [✓] **N1** · 兼容性：消费端 five_forces_engine_v3 只读 weighted_total/tier/wuli 字段（实读 1309 行）——加法维度零破坏；wuli_consumable_fields/contract 字段不动
  - 证据: 消费端源码实读 + healthcheck ok 回读
- [✓] **X1** · 测试与语法：py_compile 过 + test_yuantu_scoring.py 全过
  - 证据: 实跑 9 断言 0 失败（exit 0）

## §2.5 · 执行清单

| task_id | 过程项 | task_status | 证据 |
|---|---|---|---|
| T1 | 立 PRD | done | 本文件 |
| T2 | Edit yuantu_scoring.py（有向图构建+ET 维度+指纹缓存+文档） | done | Edit 落盘 · py_compile 过 |
| T3 | 新增 test_yuantu_scoring.py（验证用例+缓存失效+ET 语义+真图回归） | done | 9 断言全过（2 处测试预期订正：单槽缓存/下游采用方语义） |
| T4 | GOTCHAS NOTE-20260911-002 状态更新 + 评分方法文档 §3.5 口径注记 | done | 🔄 已修待验（不自标✅）· 文档注记落盘 |
| T5 | git 命令贴 Doctor 终端 | todo | 收尾合并命令块 |

## §三 · 非交付项

- 不包含：scoring/*_scores.json 人工分值调整；τ 锚集（TAU_ANCHORS）改动；tier 阈值调整；五力引擎消费端代码改动；coupling_contract 版本升版（加法维度保持 coupling-v2 兼容）。

## §四 · 状态

| 时间 | 从 → 到 | 谁 | 依据 |
|---|---|---|---|
| 2026-09-16 21:30 | draft → in_progress | CC | 问答板 4A 已裁方向·直接立卷实施 |
| 2026-09-16 22:10 | in_progress → awaiting_acceptance | CC | 独立复验（未参与实施 subagent）PASS：R1-R5/N1/X1 七条全绿 · competes_with 去重疑点排除（双向双边=1 实跑）· 真图 3 家抽查 total 差=ET 精确 |
| 2026-09-17 | awaiting_acceptance → delivered | Doctor | 会话令「落签批」（CC 代记）· R1-R5/N1/X1 七条全 [✓] |

## §五 · 变更记录

- 2026-09-16 21:30 CC: 立 PRD（问答板 4A 授权）· 消费端 1309 行实读（只读 total/tier/wuli·加法零破坏）
- 2026-09-16 22:10 CC: 独立复验 PASS 落卷——建议项两条已评估：C4 clamp 上限测试弱覆盖（真图英维克 ET=10.0 实证补齐·测试留待后续增厚）、海光 node 不在图谱属存量数据缺口（非本改造引入）
- 2026-09-17 Doctor 落签（会话令「落签批」·CC 代记）：R1-R5/N1/X1 七条全 [✓] · authority=Doctor
