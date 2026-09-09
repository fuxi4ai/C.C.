---
title: PRD · PEC 图谱升级与星空 Artifact
tags: [prd, acceptance, PEC]
created: 2026-09-08 07:45
updated: 2026-09-08 07:45
status: delivered
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

- [?] **R7** · 学者谱系全量入图（2026-09-08 Doctor 裁「全量抽取入图」· 新增需求）：7 案例学者谱系文件全部具名学者抽取为 concept 节点（文明 culture 归属 + case derives_from scholar 挂靠边），图规模 262→667 节点/692 边，星空文明星云成型
  - 验收方法: 节点/边规模实读；QA 全绿；独立复验对拍抽查
  - 证据栏: 实跑——concept 418（旧 13+学者 405 · same_as 6 条归旧 id 不新建）；derives_from 436；QA exit 0 全绿；可复现 SHA 0efd53cc…；星空 667 星点/692 边/十大文明簇（中华 148 最大）；独立复验 PASS_WITH_LIMITS（14 条对拍全过 · F1: 6 条 culture=null 宁 null 不猜 · F2: 口径 425 vs 436 · F3: 呈现层键名差异无数据损失）

### 分轨签核（v1.3 · 客观轨总 ✓ + 审查员背书 · 总签必须可审计）

- 客观轨总签（覆盖 R1/R2/R3/R4/R6/N1/N2/X1/X2 机器可判项；R5 的 manifest 注册亦为机器可判，视觉目验归 Doctor 人工）：
  - covered_requirement_ids: [R1, R2, R3, R4, R5, R6, R7, N1, N2, X1, X2]
  - authority: Doctor
  - designation_source_ref: 2026-09-08 会话（Doctor 自任验收方）
  - signed_at: 2026-09-08
  - result: 通过
  - reviewer_evidence_ref: 独立复验背书见本卷（学者批 a33510eb8265a0729 PASS_WITH_LIMITS + 哲学家批 a9ad8b529c27031b4 PASS_WITH_LIMITS · 复验后修复项均已闭环）；Doctor 目验通过（「很好了」「验收通过」）
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
| 2026-09-08 18:30 | awaiting_acceptance → delivered | CC 转录 | Doctor 总签「验收通过」（2026-09-08 会话原话）· 覆盖全部 requirement（分轨签核六字段齐）· checkbox 保持 [?] 保留实施者未自签审计链 |

---

## §五 · 变更记录

- 2026-09-08 07:45 CC: 立 PRD · 8 条交付标准（R1-R6/N1-N2/X1-X2）· task_authorization 已记录（Doctor 本场三指令逐字）
- 2026-09-08 07:45 CC: 设计决策记录——① level 取值沿用试跑 7 值闭集（六档+case「正式立案」）；② 落盘 Projects/PEC/ 根目录（方案 §三 已裁「与四大金刚同级」）；③ 星空渲染复用 starscape-template.html（08-13 版）+ render.py 注入链，PEC 类型染色适配；④ 旧图 20 种边收敛映射（founds→derives_from · exemplifies/tests→supports/challenges 逐条判 · partial_supports→supports · actor 关系族/时序/来源→事件等非 schema 语义裁除）；⑤ 试跑「lint 更便宜」发现反向吸收：纪律审计收益内建为 QA+构建报告（X2），不另起 lint；⑥ macro-facts 层 deferred（open_decisions）
- 2026-09-08 08:30 CC: 实施完成——① registers 挂靠对象按 07-27 试跑先例放宽为 framework/subpath/clause（试跑已含 reg-IRP6-F04/reg-IRP6-SP05，方案 §2.3 表格窄义不覆盖实操）；② 证据补边 35 条（仅 INDEX/组头/desc 显式关系：F-05→H-05、GE-13→H-15、C-19↔H-15、C-17↔G-27、C-15 refines C-06、C-20 refines C-05 等）；③ EC 编外案入图按方案 §一 #6 执行（EC README「不入可视化」边界系旧数据集约定·早于方案·按后批方案为准）；④ 星空复验发现 CDN 白名单风险（EXP-20260810-002-T 教训）→ 全内联 three.js 8 件后 update_artifact 重推；⑤ 复验 subagent 背书 PASS（2 发现：docstring 括注已修 · CDN 信息级已闭环）
- 2026-09-08 09:40 CC: Doctor 裁定 R5 延伸迭代——Market Signals 换 PEC 类别特质：AskUserQuestion 两问裁「轴 C 混合 + Ruling Signals」。实施：pec_to_starscape.py 加信号计算（验证/证伪/在窗/纪律活点四类 · 图内确定性 · 构建时定格 · 一跳传播至挂靠案例 · discipline 不外传）；模板 copy 按钮区 3→4 层（SIG_META/SIGNAL_ALIAS_MAP/搜索通用词同步换 PEC 语义 · 旧键清零）；重建+内联+update_artifact 已推。信号实测：18 节点带信号（GE-02 三态齐亮 · IR-P5.b 四类集齐 · 纪律活点 6 个=IR-P3 概率变动链+IR-P5.b 双读对）。目验归 Doctor。
- 2026-09-08 10:10 CC: Doctor 三裁落地——①稀疏图选中加亮：updateStarVisibility 复用 starHighlight 通道（选中组 ×1.7 放大+呼吸+亮度×2.6+光晕扩散 · 未选中 alpha 0.30→0.22）· exitFocus 回填筛选态；②学者/行为者文明双属性（AskUserQuestion 裁「落地+大西洋色」）：pec_to_starscape.py 加 CULTURE 归属表（actor 14 全归 · concept 13 全归 · 跨国组织 MIC/GlobalFinance/G7/NATO→atlantic 新色 0x7FB2D9 · 双国籍 Turchin/Soros 归美）· 引力 comm 用 culture||type · 模板 colorForNode 接线（星点/边/卡片 6 处）· filter 仍按 12 类型分组；③verdict 品紫→月白灰 0x9AA3B2（解除与纪律活点信号同色）· clause→浅青灰 0xB3C7CC 提亮。实测：26 节点归 8 文明簇（质心清晰分置）。已知取舍：filter 行圆点仍显示类型色（行为者行橙点/学者行紫点）、星点显文明色——双属性本意的外观代价，如需圆点也文明化另议。目验归 Doctor。
- 2026-09-08 10:30 CC: Doctor 视觉四裁落地——①未选中组不再压暗（保持全部态 1.0 亮度、不压灰），区分度全部由选中发光承载；②选中发光光晕柔和化：fragment shader 去 0.5 半径硬切（球体感根源）改 0.40→0.70 软边缘收口+高亮时 halo 幂 1.75→1.45 更柔，亮度增益（×1.6）与放大呼吸不变；③交互：「全部」行改 toggle——无选中时点击=全体选中（所有组发光），再点=全体取消选中；④选中组关系线 ×3 提亮（PEC 边基线 ALPHA_HARD=0.12 太淡，提亮后 0.36 可见），未相关边保持基线；exitFocus 边恢复改由 updateStarVisibility 统一接管。渲染+内联+推送 ✓。目验归 Doctor。
- 2026-09-08 10:45 CC: Doctor 视觉五裁落地——①Ruling Signals 四钮默认不勾选（去 active class · 图层初始 visible=false · 点击按钮才开启）；②「全部」行亮条反转：全体选中时与各组一起亮、取消时一起灭（无选中态=全灭 · allRow 初始去 active）。渲染+内联+推送 ✓。目验归 Doctor。
- 2026-09-08 11:00 CC: Doctor 视觉六裁落地——①线组选中提亮 ×3→×2.5；②新增「选中最小提亮」：highlight=1 时若颜色 luma <0.9 则等比抬至 0.9（保持色相）——学者等暗色组选中后不再不明显；焦点上下游半亮 0.5 不触发。渲染+内联+推送 ✓。目验归 Doctor。
- 2026-09-08 11:15 CC: Doctor 视觉七裁落地——问题定性修正为「星的大小（发光范围）非亮度」：行为者/学者/子路径/文明星基数小（低度数→小 magnitude→几像素点尺寸），×1.7 放大后发光范围仍撑不起。新增「选中最小发光范围」：highlight>0.5 时 gl_PointSize 地板 12px（光晕随点尺寸缩放，范围同步撑开）；焦点上下游半亮不触发。渲染+内联+推送 ✓。目验归 Doctor。
- 2026-09-08 11:30 CC: Doctor 视觉八裁落地（二档突出）——①小星要超过一般星而非追平：选中全体再放大 ×1.35 + 点尺寸地板 12→14px；②最小亮度兜底 0.9→1.05（选中星绝对亮度高于一般亮星）；③新增选中饱和度增强 40%（mix 向纯色推）——亮色更靠近本组颜色、不再泛白。渲染+内联+推送 ✓。目验归 Doctor。
- 2026-09-08 11:45 CC: Doctor 视觉九裁落地（回退八裁·按组分档）——Doctor 裁「最小那些组需要加、其他组不需要、有些组过亮，回退重来」：新增 per-star starBoost 通道 + SMALL_BOOST_TYPES（行为者/学者/子路径/文明桶 14 桶）——小组选中 ×1.35+14px 地板+亮度兜底 1.05+饱和 +40%；其他组回退七裁基准（12px 地板+0.9 兜底，大星不触发=原样）。渲染+内联+推送 ✓。目验归 Doctor。
- 2026-09-08 12:30 CC: Doctor 裁「学者谱系全量抽取入图」——新增交付标准 R7（见 §二·R7）；subagent 提取 7 案例谱系文件 411 位学者（CS-05 172/CS-08 112/CS-03 62 等）→ concept 节点+文明 culture+case derives_from scholar 边（same_as 6 条归旧 id）；图 262→667 节点/692 边；QA 全绿+可复现（SHA 0efd53cc…）；星空重渲（十大文明簇成型：中华 148/盎撒美 94/日本 83/欧陆 21/盎撒英 20/伊斯兰 19/斯拉夫 18/犹太 14/印度 5/大西洋 3）；独立复验（新 subagent·未参与提取）PASS_WITH_LIMITS——F1 轻微：6/411 条 culture=null（张夏准/姆本贝/诺曼/德罗西斯/凯瑟琳·田村/Eraldo Konrad · 无闭集槽或文件信息不足·宁 null 不猜）；F2 轻微：星空 culture 节点实读 425（非口径 436）；F3 信息：呈现层键名差异无数据损失。14 条抽查对拍全过。
- 2026-09-08 12:45 CC: Doctor 目验再裁「兜底亮度使文明星团过亮」——小组增强删 1.05 亮度兜底（400+ 学者选中时过亮），只保留 ×1.35+14px 尺寸增强与饱和度 +40%，亮度回基础 0.9 档。渲染+内联+推送 ✓。另 Doctor 报「有学者与文明不匹配」——待 Doctor 点名具体错配项后修 culture（6 null 条为已知清单）。目验归 Doctor。
- 2026-09-08 13:20 CC: Doctor 两裁落地——①案例主星条件退场（「子星多时星团本身即构成文明」）：文明学者数 ≥25 时 case 主星 hidden（CS-05 中华/CS-03 美/CS-08 日退场·节点与边保留保引力结构·渲染恒不可见；CS-01/02/07/09/10/11 与 GE/CR/EC 保留主星）；②学者重要性分级（Doctor 指认「每文明做过分级」→ 实查落在跨文明哲学史条目 ★ 体系）：philosopher_grades.json 提取 148 条（★★★21/★★82/★45），与学者谱系重叠 20 位+旧 13 中 2 位（康德/波普尔）挂 importance → 星图 magnitude 加成（★★★+1.0/★★+0.6/★+0.25）+ starLuma 亮度通道（★★★1.30/★★1.15）——孔子/老子/庄子/王阳明/伊本·赫勒敦等顶级学者在星团中鹤立。**注**：哲学史 148 条中未入学者谱系者（黑格尔/马克思/柏拉图等）属哲学史子项目入图另批，已挂账。渲染+内联+推送 ✓。目验归 Doctor。
- 2026-09-08 13:35 CC: Doctor 目验逮出退场残影——退场主星的 147 条学者边仍渲染成线汇聚团；接「边退场」：hidden 端点边基线 alpha=0 + 焦点循环排除。推送 ✓。
- 2026-09-08 13:40 CC: Doctor 裁「恢复主星」——撤回案例主星退场（数据层 hidden 逻辑移除，CS-05/CS-03/CS-08 主星与全部案例节点、边恢复显示；模板侧 hidden 处理代码保留无害）。学者重要性分级保留。渲染+内联+推送 ✓。目验归 Doctor。
- 2026-09-08 13:50 CC: Doctor 裁「学者层换血+三层结构」——①案例学者 411 位暂时退役（INCLUDE_CASE_SCHOLARS=False 可逆开关·数据保留）；②跨文明哲学史哲学家 124 位+哲学思想 197 条入图（philosophers.json/ideas.json subagent 提取·全量对拍 321/321）；③三层边 case→idea→phil。图 580 节点/682 边 · 独立复验 PASS_WITH_LIMITS（V-1: 齐泽克 culture null 悬空一条三层链·后修）。推送 ✓。
- 2026-09-08 14:15 CC: Doctor 框架确认+文明基因层落地——Doctor 澄清「文明基因=每文明自己的多个具体基因（非 F-07 框架星）」并提出「文明-文明基因/哲学-文明基因和哲学对应的学者」框架（CC 确认可行·盘上三层雏形即此）；实施：①GENES 策展表 25 个基因节点（生存基因/选民意识/律法传统/普通法/渐进主义/议会主权/帝国的否认/二阶基因/天命例外论/大一统/教化/士人批判自觉/实用综合/心理凝聚力合法性/自愿信息茧房/宿敌建构/合法性壳/拿来主义/国运豪赌/信仰共同体/抵抗叙事/第三罗马/强人传统/程序完备主义/态C半吊子整合）· case derives_from gene + gene derives_from 代表学者（孔子/董仲舒/荀子/洛克/休谟/本居宣长/伊本赫勒敦/杜金/康德 等盘中哲学家；留空者挂账补学者）；②复验 V-1 修复：齐泽克 culture 补 european（philosophers+ideas 各 1 条）；③QA provenance 放行 case-studies README。图 580→605 节点/719 边 · QA 全绿 · 渲染+内联+推送 ✓。目验归 Doctor。
- 2026-09-08 14:30 CC: Doctor 视觉十裁落地——①星系形态：community_pull 0.55→0.28 + 簇间推力 180→220 + iters 80→100——文明星团不再压成球，由三层边结构自然长成星系（主星 hub 居中·基因/思想中环·学者外缘）；②文明基因中间色：colorForNode 对 gene_ 节点同色调向深空 lerp 45%——星团内色彩分层（主星/思想纯色·基因中间色）。渲染+内联+推送 ✓。目验归 Doctor。
- 2026-09-08 14:45 CC: Doctor 方向性重构落地「以文明为核心重构引力框架」——①新布局引擎 compute_civilization_layout：阶段1 文明质心（case 主星）+保留组 FR（文明间斥力+边引力）；阶段2 每文明成员绕质心 Fibonacci 球面**全向**三层壳（质心主星→中壳基因/思想→外壳学者/行为者·非单向非边链）；阶段3 学者间引力=外壳学者按关联思想聚类相邻取点（同思想学者相邻）· 跨文明桥接边预留；②工具星退役：SP-01~09 hidden（原则 F/假设 H/反偏置 C/认识论 G 保留）；③布局可复现性修复：Python hash() 有 PYTHONHASHSEED 随机化→stable_hash(zlib.crc32)；④parse 给 case 主星补 culture 字段（星系锚点）。实测：中华星系中壳 34 节点距质心 86-95/外壳 20 节点 154-170 均匀球面、星系间距 401、两跑 SHA 一致。渲染+内联+推送 ✓。目验归 Doctor。
- 2026-09-08 15:00 CC: Doctor 裁「星系分开一点」——内外双环设计：外环=9 文明质心 Fibonacci 球面均匀拉开（R=235·质心最小间距 257 结构性保证·不再靠 FR 随机挤出）；内环=方法论星带（保留组 F/H/G/C/P/V 等内球 FR·半径≤110 约束·「观察台居中、文明星系环绕」）；星系壳半径内收一档（中壳 42+5√n 封 110/外壳 +38+4√n 封 165）；末尾整体归一化保形状。实测：各星系间隙 +75~+123（欧洲最挤 +75）· 两跑 SHA 一致。渲染+内联+推送 ✓。目验归 Doctor。
- 2026-09-08 15:15 CC: Doctor 裁「文明多属性归组」——基因/哲学/学者的 culture 字段接入筛选匹配（多属性）：①typeCounts 文明行计数=主星+全体 culture 成员；②星点匹配 type 或 culture 命中皆高亮——选「中华」组时 CS-05 主星+34 基因思想+20 学者行为者一起亮；③边提亮同样按端点 culture 命中。渲染+内联+推送 ✓。目验归 Doctor。
- 2026-09-08 15:20 CC: Doctor 裁「F-07 文明基因工具星退役」——F-07 节点 hidden（每文明已有具体基因层 gene_×25，F-07 作为分析工具与 SP 工具星一并隐退·其 applies 边同步不显示·图数据保留可逆）。渲染+内联+推送 ✓。目验归 Doctor。
- 2026-09-08 15:25 CC: Doctor 裁「Esc 重置视角」——Esc 优先级链：①焦点态→退出焦点；②UI 隐藏态→恢复 UI；③无选中态（activeTypes 空）→重置视角（相机回初始位 540/240/540+target 复位+恢复自转 700ms 平滑）。原独立 UI 恢复 listener 并入链。渲染+内联+推送 ✓。目验归 Doctor。
- 2026-09-08 15:30 CC: Doctor 裁「文明基因统一青碧色」——gene_ 节点全图统一 0x1abc9c 青碧（替代同色调压暗 45% 中间色：基因层跨文明一眼可辨·与文明色思想/学者层形成统一叠层）。渲染+内联+推送 ✓。目验归 Doctor。
- 2026-09-08 15:35 CC: Doctor 裁「哲学/思想统一青绿色」——idea_ 节点全图 0x76E0A8 青绿（与基因青碧 0x1abc9c 同族分阶：中壳两层色阶分明·学者层保持文明色）。渲染+内联+推送 ✓。目验归 Doctor。
- 2026-09-08 15:40 CC: Doctor 裁「选中晕散增强」——高亮态 shader：实心核半径 0.09→0.04 且强度 -45%、halo 幂 1.75→1.30 更柔更散、新增广域柔外晕 halo2（0.70 范围·2.6 幂·高亮专属 0.35 权重）——选中组呈雾状晕散而非光球；非高亮态基本不变。渲染+内联+推送 ✓。目验归 Doctor。
- 2026-09-08 15:45 CC: Doctor 裁「点选聚焦」——refreshFilter 后新增 focusOnSelection：选中组（含文明多属性匹配）节点质心=相机目标，700ms 平滑飞近（距离 ×0.45·保持朝向）+停自转；无选中/全体选中不动；与 Esc 重置视角联动（Esc 恢复初始位+自转）。渲染+内联+推送 ✓。目验归 Doctor。
- 2026-09-08 15:50 CC: Doctor 裁「选中组线稍微提亮」——边提亮系数 ×2.5→×2.75。渲染+内联+推送 ✓。目验归 Doctor。
- 2026-09-08 15:55 CC: Doctor 反馈「青绿像白色」——0x76E0A8 薄荷白绿在 additive 光晕叠加下泛白，换翡翠青绿 0x2ECC71（更饱和·抗白化·与基因青碧 0x1abc9c 保持一青一绿）。渲染+内联+推送 ✓。目验归 Doctor。
- 2026-09-08 16:00 CC: Doctor 裁「选中发光不改颜色」——移除颜色通道放大路径（×1.6 增益/亮度兜底 0.9/饱和 mix 1.4 全删）——选中星颜色恒为本色（vColor×vLuma），发光由同色光晕增强（halo 系数 0.55→0.75·外晕 0.35→0.55）与 alpha 增益（×1.5）承担；小组保留尺寸增强。渲染+内联+推送 ✓。目验归 Doctor。
- 2026-09-08 16:05 CC: Doctor 反馈「光球感还是重」——选中态：实心核强度 55%→25%、halo 幂 1.30→1.05（近线性·纯雾状渐变）、范围 0.62→0.66 微扩、外晕权重 0.55→0.60；未选中态 halo 幂 1.75→1.85 同步柔化。渲染+内联+推送 ✓。目验归 Doctor。
- 2026-09-08 16:10 CC: Doctor 裁「选中颜色通道保留一点」——加回温和增益 ×1.22（介于 16:00 全移除与最初 ×1.6 泛白之间：颜色基本本色·微微提亮）。渲染+内联+推送 ✓。目验归 Doctor。
- 2026-09-08 16:15 CC: Doctor 反馈「光球感还在·缩小发光体积」——光晕覆盖半径整体收窄 ~30%：discard 0.72→0.55、halo 范围 0.62→0.44、外晕 0.70→0.52、软边 0.40/0.70→0.30/0.53。渲染+内联+推送 ✓。目验归 Doctor。
- 2026-09-08 16:20 CC: Doctor 裁「调亮非选中态」——星：halo 系数 0.80→0.95 + 非选中基础外雾 0.15（原仅选中）；线：ALPHA_SOFT 0.05→0.10 · HARD 0.12→0.20 · STRONG 0.22→0.32。渲染+内联+推送 ✓。目验归 Doctor。
- 2026-09-08 16:25 CC: Doctor 裁「选中散射化」——实心核强度 25%→10%、半径 0.06→0.05 微缩、散射外雾权重 0.45→0.55：选中发光几乎全为散射光雾。渲染+内联+推送 ✓。目验归 Doctor。
- 2026-09-08 16:30 CC: Doctor 问「星本体本应多少体积」——实查：模板自带 dense（floor 6/slope 11）与 sparse（floor 13/slope 19）两档，注释明示 sparse 给低密度图；PEC 一直走默认 dense。CC 曾按「低密度」推断切 sparse、推送被 Doctor 拒绝，Doctor 裁「重整后的密度不低」→ 回退 dense（16:25 基线恢复）。教训：density 档选择看实际节点密度非节点总数印象。渲染+内联+推送 ✓。目验归 Doctor。
- 2026-09-08 16:35 CC: Doctor 裁「核恢复 0.05+光球感根因=边缘渐变不足」——①选中实心核恢复本体规格（半径 0.05·强度 100%·选中发光叠加于完整星体）；②softEdge 渐变带 0.30-0.53→0.10-0.54 拉宽（去光球感的正确手法：边缘柔渐变而非缩核）。渲染+内联+推送 ✓。目验归 Doctor。
- 2026-09-08 16:40 CC: Doctor 裁「不要光球·要散射」——根因：点精灵径向渐变怎么调都是圆盘；选中态叠加真实散射层：①指数扩散雾 exp(-d/0.16)（无圆边长尾）②十字星芒（沿 UV 轴细长光芒·打破圆对称）——星点核+散射雾+星芒组合。渲染+内联+推送 ✓。目验归 Doctor。
- 2026-09-08 16:45 CC: Doctor 裁「取消十字星芒」——选中散射层只保留指数扩散雾（星芒 spike 全删）。渲染+内联+推送 ✓。目验归 Doctor。
- 2026-09-08 16:55 CC: Doctor 同意「散射分工方案」——①镜头级 bloom strength 0.55→0.95 · radius 0.35→0.50（画面级辉光扩散·PEC 密度低需强 bloom）；②选中个体光斑收敛：放大 ×1.7→×1.3、小组地板 14→12、小组 ×1.35→×1.25——「星点小而锐·散射大而柔」分工（渊图散射感实为密度涌现·无独立散射设计）。渲染+内联+推送 ✓。目验归 Doctor。
- 2026-09-08 17:00 CC: Doctor 裁「翡翠再向青碧靠一点点」——思想色 0x2ECC71→0x29C87C（向 0x1abc9c 靠 25%）。渲染+内联+推送 ✓。目验归 Doctor。
- 2026-09-08 17:05 CC: Doctor 裁「思想与预测命题换色」——idea_ → 琥珀 0xFFC857 · prediction → 青绿 0x29C87C（TYPE_COLOR 同步·filter 行点自动跟随）。渲染+内联+推送 ✓。目验归 Doctor。
- 2026-09-08 17:10 CC: Doctor 裁「选中聚焦改大尺度定位主星」——focusOnSelection：选中含 case 主星（文明组）→目标=主星位置（anchorIdx 优先）；否则组质心；相机距离 ×0.45→×0.9 保持远景不缩进。渲染+内联+推送 ✓。目验归 Doctor。
- 2026-09-08 17:15 CC: Doctor 裁「非选中再加亮·选中不再跟随变亮」——亮度不分选中态：halo 1.15+外雾 0.25 恒定·颜色零增益（×1.22 移除）；选中区分只靠散射雾/放大/呼吸。渲染+内联+推送 ✓。目验归 Doctor。
- 2026-09-08 17:20-17:45 CC: Doctor 系列视觉裁收口（逐轮：非选中再提亮 halo 1.4/外雾 0.35+线三档上调→Esc 修复「UI 默认隐藏致重置不生效」一步到位→btn-reset 按钮=清空组选择+深空远景→拉近三档定稿 1034「距离正好」→Esc 渐进退出（第一按取消选择保原位·第二按重置）→组排序（案例研究→事件→行为者→文明[中华/美国/斯拉夫-苏俄/欧洲/犹太/日本+其余]→方法论资产→数据资产·工具星行隐藏））。全部渲染+内联+推送 ✓。Doctor 目验「很好了」。
- 2026-09-08 18:00 CC: 收尾闭环——①PRD 本卷补齐变更记录至 17:45；②会话日志补视觉迭代段；③git 命令块重新构造（brain 仓+PEC 仓·星空无 git）；④消费回执已 append（学者批前一行·本场同一 task 不重复）。待 Doctor 总签（客观轨总 ✓+R5/R7 目验）与 git 执行。
- 2026-09-08 17:20 CC: Doctor 裁「再次增加非选中亮度」——星 halo 1.15→1.4+外雾 0.25→0.35；线 HARD 0.20→0.30 · STRONG 0.32→0.45 · SOFT 0.10→0.16。渲染+内联+推送 ✓。目验归 Doctor。
- 2026-09-08 17:25 CC: Doctor 裁「重置视角远景全览」——Esc 重置相机 540/240/540→700/300/700（距离 790→1034）。渲染+内联+推送 ✓。目验归 Doctor。
- 2026-09-08 17:30 CC: Doctor 裁「重置视角再拉远」——相机 700/300/700→900/380/900（距离 1034→1328）。渲染+内联+推送 ✓。目验归 Doctor。
- 2026-09-08 17:35 CC: Doctor 裁「重置视角再拉远两档」——相机 900/380/900→1500/600/1500（距离 1328→2205）。渲染+内联+推送 ✓。目验归 Doctor。
