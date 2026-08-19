---
title: PRD · Shakehands 已完成沟通记录清理
tags: [prd, acceptance, 4AI握手层]
created: 2026-08-19 00:00
updated: 2026-08-19 00:00
status: delivered
task_authorization:
  state: verified
  source_type: 会话裁定
  source_ref: 2026-08-18 会话（Doctor 原始指令 + AskUserQuestion 两道裁定 + B 档裁定）
  quote: "写交付标准：把Shackhands内的已完成沟通记录删除"（拼写纠正：shakehands）
  scope: 删除 to CC/ 与 to VV/ 中已处理完的沟通记录（31 封 + 2 个 .__wtest 测试残留），真删；存续契约文档、B 档未勾项、archived/、scheduled/ 均不删
roles:
  implementers: [CC (Claude)]
  independent_reviewers: [Task subagent（干净上下文·未参与实施）]
acceptance_authority:
  authority: Doctor
  designation_source_ref: 全局协作偏好「验收主体=Doctor 或 Doctor 指定且未参与实施的独立验收方」
  designation_quote: "PRD checkbox 实施者只填 [?]/[!]/[~]，[✓] 由 Doctor 或未参与实施的指定独立验收方落"
  designated_at: 长期生效（brain 常驻偏好）
open_decisions: []
type: prd
project: 4AI/Shake hands
template_version: v1.2
---

# PRD · Shakehands 已完成沟通记录清理

## §一 · 任务目标

**动机**：`4AI/Shake hands/` 是 CC↔VV 的握手信箱，当前 71 个文件里，DVA fuxi 化全链路（07-24/25 批次，Phase 5 单写切换已收口）等一批沟通记录早已处理完毕，仍堆在信箱根目录，与活跃沟通混在一起。Doctor 指令清空已完成沟通记录，让信箱只留活跃信件与存续契约。

**范围**：删除 `to CC/` 12 封 + `to VV/` 19 封已处理完的一次性沟通信件 + 2 个 `.__wtest` 测试残留，**真删（rm）**。判定口径经 Doctor 两轮裁定：① 范围 = to CC + to VV 中已处理完的信（archived/ 不动，存续契约文档不动）；② 方式 = 真删；③ B 档待定项 Doctor 勾选「Boss老白审计委托」一并删，其余 9 封（渊图 4 封、EAL 回测报告 3 封、EAL 审查回执 2 封）保留。

**Doctor 原始指令**(逐字引用):
> "写交付标准：把Shackhands内的已完成沟通记录删除"（后拼写纠正 "shakehands"）

**配套裁定记录**（2026-08-18 会话 AskUserQuestion）：
- 范围裁定："to CC + to VV 中已处理完的信（推荐）"（archived 历史不动、存续性契约文档不动）
- 方式裁定："真删（推荐）"
- B 档裁定：勾选 "Boss老白审计委托"；未勾「渊图 4 封」「EAL 回测报告 3 封」「EAL 审查回执 2 封（推荐保留）」→ 默认保留

**任务规模估算**:
- 预计删除文件数: 33（31 封 .md + 2 个 .__wtest）
- 预计耗时: <30 分钟（含独立审查）
- 涉及项目: 4AI/Shake hands（非 git 仓 · ls -a 已核无 .git）

---

## §二 · 交付标准(Acceptance Criteria · 验收主体＝功能/需求)

### A. 功能需求（用户可感知的行为 / 结果）

- [?] **R1** · `to CC/` 信箱打开后，12 封 DVA fuxi 批次回执（07-24/25）不再存在——即 Doctor 打开 `to CC/` 看不到这些已处理完的信
  - 验收方法: `ls "to CC/"` 输出与删除清单（PRD 附录）比对：12 个文件名 0 命中；删除前快照与删除后快照 diff 仅含这 12 个 + `.__wtest`
  - 证据栏: 实跑 `find . -name` 逐名查 12 个文件 → 全部 0 命中；独立审查员重跑同法 12 行 hits=0。快照 diff（outputs/shakehands_snapshot_before/after_20260819.txt）逐名恰等于删除清单
- [?] **R2** · `to VV/` 信箱打开后，19 封已处理完的信（14 封 DVA fuxi 执行件 + dev19 盲审对账回执 + Boss老白审计委托 + 回测库移交执行单 + 回测任务书 + 回测库整改放行 + P04 重算任务书 + fuxi化实施包回执）不再存在
  - 验收方法: 同 R1，比对删除清单中 to VV/ 的 19 个文件名 0 命中
  - 证据栏: 实跑 `find . -name` 逐名查 19 个文件 → 全部 0 命中；独立审查员重跑 19 行 hits=0
- [?] **R3** · 保留对象零误删：存续契约（collaboration-needs / CC致VV-协作需求 / PRD-定期更新-DVA / fuxi-station操作指南 / README×2 / spec/ / scheduled/ 全部）+ B 档未勾 9 封（渊图 4 + EAL 报告 3 + EAL 审查回执 2）完好在位，信箱功能不受影响
  - 验收方法: `find` 全树与保留清单（PRD 附录）逐一比对：每个保留文件存在且行数未变；删除前后两棵树 diff 恰好等于删除清单
  - 证据栏: 实跑 20 项逐一 `test -f` → 20 OK、缺失 0；独立审查员重跑 20 行全 OK 且 `wc -c` 字节数与删除前快照一致（FAILURES: 0）
- [?] **R4** · 测试残留清除：根目录与 `to CC/` 下两个 `.__wtest` 文件不再存在（隐藏文件，`ls -la` 可见）
  - 验收方法: `ls -la` 两目录输出无 `.__wtest`
  - 证据栏: 实跑 `find . -name '*wtest*'` → 空输出；独立审查员重跑同法 + `ls -la` 两目录均无
- [?] **R5** · scheduled 机器握手通道零扰动：`to CC/scheduled/*.latest.json`、`to VV/scheduled/`（需求文档 + ack.latest.json）与 spec/handshake-schema.json 未被删除，touzhijunjun 试点任务契约完好
  - 验收方法: 删除前后 scheduled/ 与 spec/ 的 find 输出逐行一致
  - 证据栏: 实跑 `find scheduled spec "to CC/scheduled" "to VV/scheduled" -type f | sort` → 恰 6 项与 PRD 附录逐名一致；独立审查员重跑字节数与删除前快照一致

### B. 非功能需求

不适用——本任务为文件清理，无性能/安全/可靠性/兼容性/数据质量属性。

### C. 任务专属（自定义）

无新增。

### 分轨签核（v1.3 · 客观轨总 ✓ + 审查员背书 · 总签必须可审计）

- 客观轨总签（覆盖 R1/R2/R3/R4/R5 · 全部机器可判）：
  - covered_requirement_ids: [R1, R2, R3, R4, R5]
  - authority:                Doctor
  - designation_source_ref:   2026-08-19 会话 Doctor 明示「签」——总 ✓ 签署（签署权与签署人均 Doctor · CC 仅代记留痕）
  - signed_at:                2026-08-19
  - result:                   通过
  - reviewer_evidence_ref:    # 独立审查员背书：Task subagent（agentId a00ee0f468d968179 · 2026-08-19 · 未参与实施）——实跑 find 逐名查（R1 12 行/R2 19 行全 hits=0）、20 项 test -f + wc -c 字节比对（全 OK）、find '*wtest*' 空输出、scheduled/spec 6 项逐名一致；全树 38 = 71 − 33；archived 16 封快照逐字节未动。结论：通过。审查报告全文在本会话工具输出中
- 原则轨（结论/裁定类）共 0 条：本任务纯文件事实核查，无结论/裁定类验收项。

---

## §2.5 · 执行与交付清单（过程项 · 不参与功能交付关闭判定 · 无 checkbox 表格）

| task_id | 过程项 | task_status | 证据 |
|---|---|---|---|
| T1 | 删除前全树快照（ls -laR）落 outputs/ 留档 | done | `outputs/shakehands_snapshot_before_20260819.txt` |
| T2 | 删除执行：31 封 .md + 2 个 .__wtest（rm） | done | 首轮 rm 被挂载拦（Operation not permitted）→ allow_cowork_file_delete 开 Documents 权限 → 重跑 rm -v 33 项全 removed；find -type f 71→38 |
| T3 | 删除后快照 + 与删除前 diff 比对：diff 恰好等于删除清单 | done | outputs/shakehands_snapshot_before/after_20260819.txt；ls 文本 diff 因块错位不可用 → 改逐名 find 0 命中验证（33 项全过） |
| T4 | 保留清单逐项存在性复核（find + 行数对照） | done | 20 项 test -f 全 OK；审查员加验 wc -c 与删除前一致 |
| T5 | 独立审查员（干净 Task subagent）对照本 PRD 复核并背书 | done | Task subagent a00ee0f468d968179 · 结论通过 · 发现 PRD 两处计数笔误已修订 |
| T6 | /save 触发 + brain-save 回报贴 PRD 路径与状态 | todo | 待 Doctor /save 或明示存档 |
| T7 | git：不涉及（4AI 非 git 仓，ls -a 已核） | done | `ls -a 4AI` 无 .git |

---

## §三 · 非交付项(范围排除)

- 不包含：`archived/` 内 16 封历史归档（Doctor 范围裁定明确不动；独立审查员核对快照逐字节未动）
- 不包含：B 档未勾 9 封——渊图 4 封（磷化铟 08-08 虽已入库但事件级入库未核到；HBM/盘中孔/存储层次三候选 canonical 零命中、是否评估拒绝未定论）、EAL 回测报告 3 封（台账 v1.3.1 已入册但逐条消化未核）、EAL 审查回执 2 封（A 阶段 BLOCK、B 阶段未开、v2.3 引用 v2.2 为权威稿）
- 不包含：存续契约文档与 scheduled/ 机器通道（touzhijunjun 试点进行中）
- 不包含：.DS_Store 等系统文件；不主动知会 VV（如需知会由 Doctor 定夺）
- 不包含：git 操作（非 git 仓；且沙箱禁 git 写命令）

---

## §四 · 状态（current_status + 变更历史 · 不用多 checkbox）

**状态变更历史**（只追加实际发生的行 · 不得预填）:
| 时间 | 从 → 到 | 谁 | 依据 |
|---|---|---|---|
| 2026-08-19 00:00 | （新建）→ in_progress | CC | Doctor 指令已授权 + 立卷即开工 |
| 2026-08-19 00:05 | in_progress → awaiting_acceptance | CC | R1-R5 全部填 [?]+证据 · 独立审查员背书通过 · 交 Doctor 终审 |
| 2026-08-19 | awaiting_acceptance → delivered | Doctor（CC 代记留痕） | 客观轨总签通过 · 2026-08-19 会话 Doctor 明示「签」· 连带裁定：真删不知会 VV |

**关闭路径**(回顾铁律):
- ✓ 关闭:每个 requirement 逐项 `[✓]`，或被字段齐全的合法总签明确覆盖
- ✓ Doctor 取消关闭:Doctor 明示"取消" / "算了"
- ✗ 不允许实施者自动关闭

---

## §五 · 变更记录

- 2026-08-19 00:00 CC: 立 PRD · 5 条交付标准（R1-R5 · 全部客观轨机器可判）· task_authorization 已记录（Doctor 原话 + 两道裁定 + B 档裁定）
- 2026-08-19 00:05 CC: R1-R5 全部填 [?] + 证据（find/test/diff 实跑）；独立审查员（Task subagent）背书通过；审查发现 PRD 两处计数笔误（archived 16 封非 18；保留清单标题计数）已修订；frontmatter status → awaiting_acceptance
- 2026-08-19 CC: Doctor 会话签署客观轨总 ✓（原话「签」）· result=通过 · status → delivered · 连带裁定「真删不用知会 VV」闭合（CC 代记留痕，签署权归 Doctor）

---

## 附录 · 删除清单与保留清单

**删除清单（33 项）**

to CC/（12）：
1. VV-to-CC-DVA-fuxi-Phase2部署包缺口-20260724.md
2. VV-to-CC-DVA完全fuxi化部署交接-20260724.md
3. VV回执-DVA-Playwright治本与老石探针异常-20260725.md
4. VV回执-DVA-fuxi-Phase2A-shadow-20260724.md
5. VV回执-DVA-fuxi-Phase2B-2C完成-20260724.md
6. VV回执-DVA-fuxi-Phase2B-DB守卫硬点-20260724.md
7. VV回执-DVA-fuxi-Phase2B-bundle模块闭包缺口-20260724.md
8. VV回执-DVA-fuxi-Phase3首轮导入与Phase4-dryrun完成-20260724.md
9. VV回执-DVA-fuxi-Phase3首轮真实数据三缺口-20260724.md
10. VV回执-DVA-fuxi-Phase5单写切换完成-20260724.md
11. VV回执-DVA-harvest_one首测两入口缺口-20260724.md
12. VV回执-DVA-点单入口修复复验与告警洪泛-20260724.md

to VV/（19）：
1. CC-to-VV-dev19-盲审对账回执-20260814.md
2. CC回执-DVA-fuxi化实施包-20260724.md
3. CC致VV-Boss老白外部审计-20260816.md
4. CC致VV-DVA-fuxi-2B就绪-20260724.md
5. CC致VV-DVA-fuxi-DB守卫修复-20260724.md
6. CC致VV-DVA-fuxi-Phase2部署包交付-20260724.md
7. CC致VV-DVA-fuxi-Phase3三缺口修复-20260724.md
8. CC致VV-DVA-fuxi-Phase3迁移工具-20260724.md
9. CC致VV-DVA-fuxi-Phase5执行单-20260724.md
10. CC致VV-DVA-fuxi-bundle闭包修复-20260724.md
11. CC致VV-DVA-harvest_one落位-20260724.md
12. CC致VV-DVA-依赖实况修复与退出路径-20260724.md
13. CC致VV-DVA-入口两缺口修复-20260724.md
14. CC致VV-DVA-分析层迁移-20260724.md
15. CC致VV-DVA-告警分级三桶落地-20260724.md
16. CC致VV-P04新口径重算方向①旧余量-20260806.md
17. CC致VV-事件归因回测库移交执行单-20260805.md
18. CC致VV-回测任务书-美股事件科技资讯发现-20260805.md
19. CC致VV-回测库整改放行-20260805.md

测试残留（2）：`./.__wtest`、`to CC/.__wtest`

**保留清单（20 项 · 必须零误删）**

to CC/（11）：`VV-to-CC-collaboration-needs.md`、`VV-to-CC-fuxi-station操作指南-20260723.md`、`2026.08.08-to-CC-DVA渊图-光模块磷化铟.md`、`VV-to-CC-渊图HBM物理机制候选增量-20260729.md`、`VV-to-CC-渊图盘中孔填充盖镀候选增量-20260729.md`、`VV-to-CC-渊图计算机存储层次候选增量-20260729.md`、`VV致CC-P04新口径重算对照报告-20260806.md`、`VV致CC-回测探索报告-方向2与4-20260806.md`、`VV致CC-回测探索报告-方向3与1初稿-20260806.md`、`VV回执-EAL-v2.2方法论外部审查-20260817.md`、`VV补充回执-EAL-v2.3版本错位与实证复核-20260817.md`

to VV/（3）：`CC致VV-协作需求.md`、`PRD-定期更新-DVA.md`、`README.md`

目录结构（6）：`README.md`、`scheduled/README.md`、`spec/handshake-schema.json`、`to CC/scheduled/touzhijunjun-perspective-refresh.latest.json`、`to VV/scheduled/CC致VV-投知君君握手改造需求.md`、`to VV/scheduled/touzhijunjun-perspective-refresh.ack.latest.json`
