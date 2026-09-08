---
title: PRD · PEC 图谱升级与星空 Artifact
tags: [prd, acceptance, PEC]
created: 2026-09-08 07:45
updated: 2026-09-08 07:45
status: awaiting_acceptance
task_authorization:
  state: verified
  source_type: 会话裁定
  source_ref: 2026-09-08 会话
  quote: "渊图是平行的另一个项目；现在单独更新PEC的图谱。1、把手工层升级成「复用渊图图基建 + PEC 专属 schema + QA + provenance」的正规图谱层，状态至今仍是「提案待批」——批准。2、批准的基础上检查是否有现成优化可做。3、更新完成后仿照渊图创建独立的Artifact。"
  scope: ①批准 2026-07-27 图谱化方案（schema v0.1 · 12 节点类/11 边类/13 项 QA/verdict 一等公民）；②实施中的现成优化由 CC 判断落地；③PEC 独立星空 Artifact（仿渊图范式）
roles:
  implementers: [CC 本场, 提取 subagent（verdict 链）]
  independent_reviewers: [未参与实施的 Task subagent（执行 Step 7.5 时指派）]
acceptance_authority:
  authority: Doctor
  designation_source_ref: 2026-09-08 会话（Doctor 即裁定方 · 沿用总签惯例）
  designation_quote: "（Doctor 自任验收方 · 本场指令即授权）"
  designated_at: 2026-09-08
open_decisions:
  - item: macro-facts-register 结构性事实入图（方案 §一 #9 半图化档）
    blocking: false
    blocks_requirement_ids: []
    decision_owner: Doctor
    status: deferred
    resolution_source: schema v0.1 的 12 节点类无 fact 类型、§2.2 未定义其承载——入图需 v0.2 schema 提案，不在本批批准范围
    resolved_at: 2026-09-08
  - item: facts/ 高时效时序旁路层（对标渊图 prices/ 范式）
    blocking: false
    blocks_requirement_ids: []
    decision_owner: Doctor
    status: deferred
    resolution_source: 同上一项 · v1.1 候选
    resolved_at: 2026-09-08
  - item: 旧图 20 种边收敛到 11 种闭集的逐条映射（含 actor-actor 关系族裁除）
    blocking: false
    blocks_requirement_ids: []
    decision_owner: Doctor
    status: resolved
    resolution_source: 方案 §2.1 约束 1「现有 20 种边收敛到 11 种」已批——映射表是实施细节，落构建器注释 + PRD §五 变更记录
    resolved_at: 2026-09-08
type: prd
project: PEC
template_version: v1.2
---

# PRD · PEC 图谱升级与星空 Artifact

## §一 · 任务目标

PEC 的知识图谱停在 05-21 的手工可视化层（graph-data.js 8 节点类/20 边类，与 09-08 现行内容层漂移 110 天），且 07-27 的「复用渊图图基建 + PEC 专属 schema」图谱化方案（当日已完成 IR 组样本试跑 57 节点/92 边/12 项 QA 全绿）停在「提案待批」。本任务：①按方案 schema v0.1 从现行真源（INDEX/GOTCHAS/predictions-register/case 目录）构建 PEC 正视图谱层（verdict 一等公民、provenance 全节点、13 项 QA）；②承接 07-27 试跑产物与旧图 56 节点（现成优化）；③仿渊图星空范式生成 PEC 独立星空 Artifact。

**Doctor 原始指令**(逐字引用):
> "渊图是平行的另一个项目；现在单独更新PEC的图谱。1、把手工层升级成「复用渊图图基建 + PEC 专属 schema + QA + provenance」的正规图谱层，状态至今仍是「提案待批」——批准。2、批准的基础上检查是否有现成优化可做。3、更新完成后仿照渊图创建独立的Artifact。"

**任务规模估算**:
- 预计涉及文件数: ~12（PRD 1 · 构建器 1 · QA 1 · verdicts 数据 1 · canonical JSON 1 · starscape 脚本 1 · 渲染 HTML 1 · 日志 1 · 回执 1 · git 命令块等）
- 预计耗时: 3-5 小时（侦查已完 · verdict 提取 subagent 并行）
- 涉及项目: PEC（Projects/PEC）· 星空（Projects/星空 渲染链复用）· brain（PRD/日志/回执）

---

## §二 · 交付标准(Acceptance Criteria · 验收主体＝功能/需求)

### A. 功能需求（用户可感知的行为 / 结果）

- [?] **R1** · `Projects/PEC/pec_graph.json` 生成，且 `pec_graph_qa.py` 13 项 QA（渊图继承 8 + PEC 专属 5 含双读一致性）输出全绿、退出码 0
  - 验收方法: 实跑 `python3 pec_graph_qa.py --input pec_graph.json`，读退出码与 QA 输出行
  - 证据栏: 实跑 2026-09-08——正路 `exit 0` + 输出「✅ 全绿（含 provenance 检查）」（WARN 62 条均为未到期无裁定预测·非僵尸）；负向注入 `--inject-zombie` `exit 1` + FAIL「僵尸预测 P-ZOMBIE-INJECTED」
- [?] **R2** · 四段咬合链全量入图：F-01~08、H-01~15、G-01~30、SP-01~09、C-01~21、全部案例（CS×9 + GE×8 + CR×3 + EC×4 + GE候选）、predictions-register 全部正式预测与 4 个候选区埋点均有节点；每个 prediction ≥1 条 adjudicates（僵尸预测=0）
  - 验收方法: QA 输出节点分布与僵尸预测检查（QA-1）；数量与 INDEX/register 现行编号对拍
  - 证据栏: 构建报告实跑——节点分布 framework 8/hypothesis 15/gotcha 27（G-15/19/20 按方案并入不立节点）/subpath 9（含 SP-09 埋点）/clause 24（C-01~21+C-12.2+CL×2）/case 25（CS9+GE9+CR3+EC4）/prediction 73（IR 8+非IR 53+XJ/TX/AIB 10+埋点05/06）/verdict 47；僵尸 FAIL=0（62 条 WARN 均下次复盘未到期或未定）
- [?] **R3** · 旧图承接：concept×13 / actor×12 / event×6 / source×1 四类节点全部迁移至新图（沿用 8 类不丢）；旧 20 种边类型收敛后全部落在 11 种闭集内（无非法边 type）
  - 验收方法: QA 边类型闭集检查全绿 + 构建器映射表（X1）覆盖 20 种旧 type
  - 证据栏: 节点分布实读 concept 13/actor 14（12 旧图+2 试跑补）/event 6/source 1 全在；QA 非法边 type=0；X1 映射表 grep 20/20 全有去向（含裁除族理由）
- [?] **R4** · 裁定链保真：IR-P5.b〔B〕双读并存（同 target+as_of+sub_claim 两个不同 reading，无「单一」）；IR-P3 概率变动链在图内可查（probability_moved=true 且带 guarded_by）
  - 验收方法: QA 双读一致性检查通过 + grep 指定节点字段实读
  - 证据栏: QA 双读 0 违规；pec_graph.json 实读 V-IR-P5.b-20260714-B严（严/证伪）与 -B宽（宽/未决）并存同 key；V-IR-P3-20260821-A（0.425·moved=true·guarded_by=[G-03,G-04]）与 -B（0.30·moved=true）链式不覆盖
- [?] **R5** · Cowork artifact manifest 出现 id=pec-starry-skies；打开为 PEC 星空交互页（meta.title 含 PEC、KPI 星点数=pec_graph.json 节点数、类型筛选/焦点卡可用）
  - 验收方法: list_artifacts 实读注册与 updatedAt；人工验收=Doctor 打开目验（视觉/交互）
  - 证据栏: list_artifacts 实读——pec-starry-skies 已注册（path Gateway-workspace/Artifacts/pec-starry-skies/index.html · createdAt 2026-09-08T14:11:19Z）；HTML 注入解析实跑：DATA 262 节点/281 边、meta.title「PEC · Starry Skies」、KPI 星点 262=canonical；JS `node --check` 语法 OK。**复验补强（EXP-20260810-002-T 教训）**：初版带 8 个 three.js CDN 外链会被 artifact 沙箱拦→白屏，已全内联（828KB · 外链清零 · 内联后数据/语法复验通过 · update_artifact 已推送）。目验归 Doctor
- [?] **R6** · provenance 全覆盖：pec_graph.json 每节点/边带 provenance[].file，且文件集合 ⊆ {INDEX.md, GOTCHAS.md, predictions-register.md, case README, graph-data.js, 图谱化方案, 构建器自注}
  - 验收方法: 脚本断言（QA 内建 provenance 检查）输出
  - 证据栏: QA provenance 检查全绿（来源闭集校验 0 越界）；构建器 node()/edge() 强制带 provenance 参数

### B. 非功能需求（仅产品或系统质量属性）

- [?] **N1** · 数据质量·可复现与 fail-fast：`pec_build_graph.py` 连续两次运行产出 SHA-256 一致；注入负向样本（如制造一条僵尸预测）时 QA 退出码非 0
  - 验收方法: 实跑两次 + shasum 比对；负向注入实跑读退出码
  - 证据栏: 补边后连跑两次 SHA 均为 `ce0db243b17226b37c5f0cbf7e1077e5551031b54350abcb9eddc8a2d8832c60`（补边前亦验过两次一致 588161e0…）；负向注入 exit 1
- [?] **N2** · 数据质量·源文件只读：构建前后 INDEX.md / predictions-register.md / GOTCHAS.md / graph-data.js / 知识图谱.html / validate-graph-sync.js 的 mtime+size 零变化
  - 验收方法: 构建前 ls -l 记录 → 构建后 ls -l 对拍
  - 证据栏: stat 实跑对拍——六件 mtime 与 size 与侦查时记录逐项一致（INDEX 08-26/347307 · register 08-31/228521 · GOTCHAS 09-02/122843 · graph-data 05-21/18589 · 知识图谱 05-21/21983 · validate 05-08/3597）

### C. 任务专属（自定义）

- [?] **X1** · 旧边收敛映射表落盘：20 种旧边 type 全部有去向（映射至 11 种之一或裁除并注明语义理由），作为构建器内文档化表
  - 验收方法: grep 构建器内映射表覆盖 20 个旧 type 名
  - 证据栏: `pec_build_graph.py` docstring 映射表实跑 grep——founds/supports/challenges/applies/exemplifies/tests/triggers/involves/precedes/analyzes/partial_supports/allies/aligns/hosts/references/is_subject_of/enables/leads/embedded_in/allied_to 20/20 全有去向（映射 9 族+裁除 11 族注明理由）
- [?] **X2** · 纪律审计报告：构建器输出「概率变动次数/总裁定数」「guards 边频次（哪条陷阱是活刀）」两指标（承接试跑 Q3 的机器可查收益）
  - 验收方法: 实跑构建器读报告段
  - 证据栏: 构建报告实跑——概率变动 2/47（V-IR-P3-20260821-A/B）；guards 频次 G-03×22 > G-28×9 > G-04×6 > G-08×4 > CL 清单×8 > G-01×2（活刀=G-03，与试跑发现一致）；带预留裁定 22 条

### 分轨签核（v1.3 · 客观轨总 ✓ + 审查员背书 · 总签必须可审计）

- 客观轨总签（覆盖 R1/R2/R3/R4/R6/N1/N2/X1/X2 机器可判项；R5 的 manifest 注册亦为机器可判，视觉目验归 Doctor 人工）：
  - covered_requirement_ids: []
  - authority:
  - designation_source_ref:
  - signed_at:
  - result:
  - reviewer_evidence_ref:
- 审查员背书（2026-09-08 · 未参与实施的 general-purpose subagent · agentId a21bf9bf7f111c034）：
  - 身份：独立 Task subagent（干净上下文 · 全程未改任何文件 · 复验后构建前后 SHA 零变动）
  - 验证动作（28 tool uses 实跑实读）：① QA 正路 exit 0/负向注入 exit 1 重跑；② 构建三连跑 SHA 全同 ce0db243… 且报告 diff 逐字节一致；③ 对拍抽查 6 组（IR-P3 概率链/IR-P5.b 四拆件/H-15+mir 边/旧图 desc 逐字/埋点-05 归位/源文件 mtime）；④ 映射表 20/20；⑤ artifact JSON 解析 262/281+色键四枚+占位符清零+JS 语法；⑥ 结构卫生断言（id 唯一/端点可达/边闭集/guards 纯 verdict）
  - 结论：**PASS** · 发现 2 项——①低危：docstring 裁除括注对 references/is_subject_of 表述不精确（已由实施者修正为「actor 关系族/时序/来源→事件/actor→concept 等非 schema 语义」）；②信息级：CDN 外链依赖（已触发内联修复 · 见 R5）
- 原则轨（结论/裁定类）共 0 条：本场开发中无首现验收裁定（schema/边收敛/落盘位置均为 07-27 已批方案与 Doctor 本场指令范围）

---

## §2.5 · 执行与交付清单（过程项 · 不参与功能交付关闭判定 · 无 checkbox 表格）

| task_id | 过程项 | task_status | 证据 |
|---|---|---|---|
| T1 | 侦查：方案全文+旧图三件+渊图基建+星空管线 | done | 方案 §二/§三/§五 实读 · graph-data.js 全文实读 · canonical_to_starscape.py/render.py/starscape-template.html 定位 |
| T2 | PRD 落盘 brain/logs/checkpoints/ | done | 本文件 |
| T3 | verdict 链提取 subagent 产出 verdicts_nonir.json（行号 provenance · 非 IR 组） | done | 53 预测/3 裁定/22 hints · 27,421B · 埋点-01 误挂已归位埋点-05 |
| T4 | IR 组试跑数据刷新至 register v2.15 | done | verdicts_ir.py 44 裁定 · 含 IR-P3 概率变动链与 IR-P5.b 双读 |
| T5 | pec_build_graph.py 落盘（12 节点类/11 边类/旧图迁移/映射表） | done | 262 节点/281 边 · SHA ce0db243… |
| T6 | pec_graph_qa.py 落盘（13 项 + provenance 检查 + 负向注入） | done | 正路 exit 0 · 负向 exit 1 |
| T7 | QA 全绿实跑 + 分布报告 | done | 输出见 R1/R2/X2 证据 |
| T8 | pec_to_starscape.py + render → pec-starry-skies.html | done | 175KB → 内联后 828KB · 外链清零 |
| T9 | create_artifact pec-starry-skies + list_artifacts 回读 | done | 注册 14:11:19Z · 内联版已 update_artifact 推送 |
| T10 | 独立复验 subagent（未参与实施 · 实跑实读） | done | PASS · 2 发现（1 已修 1 信息级）· 背书见分轨签核 |
| T11 | 源文件零修改核验（mtime/size 前后对拍） | done | 六件逐项一致（N2 证据） |
| T12 | git commit 命令贴 Doctor（PEC 仓 + 星空仓 + brain 仓） | done | 命令块已贴（见本场最终回报） |
| T13 | /save 会话日志 + 五阶段消费回执 | done | logs/2026-09-08-PEC图谱升级与星空Artifact.md · 回执行 appended |

---

## §三 · 非交付项(范围排除)

- 不包含: macro-facts-register 结构性事实入图（schema 12 类无 fact 类型 · v0.2 提案另批）
- 不包含: facts/ 高时效时序旁路层（对标渊图 prices/ · v1.1 候选）
- 不包含: raw/ 论证机理论文图化（方案 §一 #12 判 🔴 不可图化）
- 不包含: α/α′ 二阶自检入图（G-27 子条款所挡 · C-20 台账承载）
- 不包含: 与渊图共享图模型或实体合并（两图各自持有真相 · 仅单向 yuantu_ref 字段）
- 不包含: LLM 批量抽取（本轮构建器确定性抽取；LLM 辅助另批）
- 不包含: Artifact 自动刷新调度（静态快照 · 刷新=重跑+update · 调度另批）
- 不包含: 修改任何被审源文件（INDEX/register/GOTCHAS/旧图三件均只读）

---

## §四 · 状态（current_status + 变更历史 · 不用多 checkbox）

**状态变更历史**（只追加实际发生的行）:
| 时间 | 从 → 到 | 谁 | 依据 |
|---|---|---|---|
| 2026-09-08 07:45 | draft → in_progress | CC | 立卷即开工 · Doctor 本场指令已授权 |
| 2026-09-08 08:30 | in_progress → awaiting_acceptance | CC | 全部交付标准已填 [?]+证据 · 独立审查员背书 PASS（见分轨签核）· 交 Doctor/指定独立验收方终审 |

---

## §五 · 变更记录

- 2026-09-08 07:45 CC: 立 PRD · 8 条交付标准（R1-R6/N1-N2/X1-X2）· task_authorization 已记录（Doctor 本场三指令逐字）
- 2026-09-08 07:45 CC: 设计决策记录——① level 取值沿用试跑 7 值闭集（六档+case「正式立案」）；② 落盘 Projects/PEC/ 根目录（方案 §三 已裁「与四大金刚同级」）；③ 星空渲染复用 starscape-template.html（08-13 版）+ render.py 注入链，PEC 类型染色适配；④ 旧图 20 种边收敛映射（founds→derives_from · exemplifies/tests→supports/challenges 逐条判 · partial_supports→supports · actor 关系族/时序/来源→事件等非 schema 语义裁除）；⑤ 试跑「lint 更便宜」发现反向吸收：纪律审计收益内建为 QA+构建报告（X2），不另起 lint；⑥ macro-facts 层 deferred（open_decisions）
- 2026-09-08 08:30 CC: 实施完成——① registers 挂靠对象按 07-27 试跑先例放宽为 framework/subpath/clause（试跑已含 reg-IRP6-F04/reg-IRP6-SP05，方案 §2.3 表格窄义不覆盖实操）；② 证据补边 35 条（仅 INDEX/组头/desc 显式关系：F-05→H-05、GE-13→H-15、C-19↔H-15、C-17↔G-27、C-15 refines C-06、C-20 refines C-05 等）；③ EC 编外案入图按方案 §一 #6 执行（EC README「不入可视化」边界系旧数据集约定·早于方案·按后批方案为准）；④ 星空复验发现 CDN 白名单风险（EXP-20260810-002-T 教训）→ 全内联 three.js 8 件后 update_artifact 重推；⑤ 复验 subagent 背书 PASS（2 发现：docstring 括注已修 · CDN 信息级已闭环）
