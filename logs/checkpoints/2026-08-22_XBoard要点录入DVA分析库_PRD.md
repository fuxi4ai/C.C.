---
title: PRD · XBoard 要点录入 DVA 分析库
tags: [prd, acceptance, DVA, 科技资讯看板]
created: 2026-08-22 14:00
updated: 2026-08-22 22:44
status: delivered  # draft / in_progress / blocked / awaiting_acceptance / delivered / cancelled
task_authorization:
  state: verified
  source_type: 会话裁定
  source_ref: 2026-08-22 会话（本场）
  quote: 「交给VV去做，发个请求：1、复活；2、检查DVA金融分析数据库；3（这个我们自己做）、把X Board详情页产生的LLM要点分析，录入DVA金融分析数据库。」＋ VV 回执 §六 录入契约（_xboard 独立扩展层）＋ Doctor 裁「现在就开（推荐）」
  scope: Mac X-Board 要点缓存 → fuxi 侧 Reports/<author>/_xboard/ 单向发布（录入器开发+首代发布+班接入）
roles:
  implementers: [CC（录入器/首代发布/班接入/验收）]
  independent_reviewers: [待派·未参与本场开发的 Task subagent]
acceptance_authority:
  authority: Doctor
  designation_source_ref: Doctor 为默认验收方（本场未另行指定独立验收方）
  designation_quote: 无独立验收方指定记录——验收方=Doctor
  designated_at: 2026-08-22
open_decisions: []
type: prd
project: DVA（跨 X-Board）
template_version: v1.2
---

# PRD · XBoard 要点录入 DVA 分析库

## §一 · 任务目标

X-Board 详情页的 LLM 要点（Mac 侧 producer cache `Claude/Projects/Financial/X-Board/points/{aweme}.json`）目前只是呈现层缓存。按 Doctor 裁定「3（这个我们自己做）」，把要点录入 DVA 金融分析库。VV 回执 §六 给出契约：**不写 finance 五文件**（受 generation/hash 认证，混写会 hash 漂移），落独立扩展层 `Reports/<author>/_xboard/`（current pointer + 不可变 _generations + manifest，逐视频文档，fail-closed，单向发布 Mac→fuxi，不改现有镜像 profile）。VV 不建设录入器。

**Doctor 原始指令**(逐字引用):
> 「交给VV去做，发个请求：1、复活；2、检查DVA金融分析数据库；3（这个我们自己做）、把X Board详情页产生的LLM要点分析，录入DVA金融分析数据库。」
> AskUserQuestion（时机）: 「现在就开（推荐）」
> VV 回执 §六（契约基准）: `4AI/Shake hands/to CC/VV致CC-DVA道法术触发复核与金融分析库契约回执-20260822.md`

**任务规模估算**:
- 预计涉及文件数: 5（ingest_points.py 新 · fuxi verify 脚本随推送 · 班 prompt 改 · X-BOARD-OPERATIONS.md 补 §9.5 · PRD 本体）
- 预计耗时: 约 1-2 小时
- 涉及项目: X-Board（Mac 侧录入器）＋ DVA（fuxi 侧 _xboard 层，只读五文件）

---

## §二 · 交付标准(Acceptance Criteria · 验收主体＝功能/需求)

### A. 功能需求（用户可感知的行为 / 结果）

- [✓] **R1** · 录入器把 Mac points 缓存组为 generation 并单向发布到 fuxi `Reports/<author>/_xboard/_generations/<gen>/`（by-aweme v1 文档 + manifest v1），发布后 current.json 指向新代
  - 验收方法: 首代发布后 ssh 回读 fuxi `_xboard` 树——current.json 在盘且 generation_id 匹配、by-aweme 文档数与 manifest entries 一致
  - 证据栏(实施者填): 首代 `xb-20260822T135424Z` 发布成功（老毛 1 文档）· ssh 回读树：`_generations\xb-20260822T135424Z\{manifest.json(1002B), by-aweme\7676084633146035507.json(1128B)}` 在盘 · current.json 在盘且 generation_id=xb-20260822T135424Z、point_document_count=1。⚠ 首跑曾因 Move-Item 非终止错误产生「current 指向空代」违约态，已手动修复 fuxi 结构 + 脚本加固（-ErrorAction Stop + Test-Path 断言）后复验在盘结构正确
- [✓] **R2** · 幂等：全部条目幂等键与当前 current 代一致时重跑 no-op（不产生新代、不重写 current）
  - 验收方法: 同输入连续跑两次——第二次输出 no-op、fuxi `_generations` 目录数不增
  - 证据栏(实施者填): 首代发布后立即重跑 ingest_points.py →「幂等 no-op（与上次发布一致）」· fuxi `_generations` 仅 1 代（回读树实证）· `points/_last_published.json` 摘要 5d9b0693… 与发布时一致
- [✓] **R3** · fail-closed：Mac 预校验或 fuxi 回读校验任一失败，不落 `_generations`、不改 current（staging 可清理）
  - 验收方法: 人工篡改 staging 里 1 个文档的 points（制造 6 条）→ verify 拒绝、current 不变（比对前后 SHA）
  - 证据栏(实施者填): fuxi 侧人工建坏 staging（points 6 条+文件 SHA 不符）→ verify 输出「FAIL: 文件 SHA 与 manifest 不符 / points 条数 6 越界」· VERIFY_RC=1 · current.json SHA 前后一致（F1218B05…）· 坏 staging 已清

### B. 非功能需求（仅产品或系统质量属性）

- [✓] **N1** · 原子性：generation 完整入不可变目录后才原子替换 current.json（.tmp+Move）；失败不得留半代
  - 验收方法: 发布脚本内 staging→_generations 为 Move-Item；current 写 .tmp 后 Move；verify 在 move 之前全量 PASS 才执行
  - 证据栏(实施者填): 脚本实现在盘（verify PASS 才进发布段；current 经 .tmp 两段 Move；全部 Move/New 加 -ErrorAction Stop + 事后 Test-Path 断言）。⚠ 首跑曾暴露原子性缺陷（Move-Item 非终止错误静默吞掉 → current 指向空代），已修复并复验；此缺陷及其加固即 N1 的负向+正向证据链
- [✓] **N2** · 数据质量：每文档 3-5 条非空去重 points；aweme_id/时间/hash/schema 字段显式合法；manifest 逐文件 SHA-256 回读一致、entries 按 aweme 严格升序、计数一致
  - 验收方法: verify 脚本全项 PASS 输出（逐项打印）+ 首代回读抽查 1 个文档字段全合法
  - 证据栏(实施者填): 首代 verify 输出 VERIFY_PASS（entries:1 · inventory:520 · doc_ok:1 · inventory_fingerprint 45bfecaa… 与 manifest 一致〔经独立审查更正：54762c7b 系修复前旧失败轮现场值，在盘与重算一致值为 45bfecaa〕· manifest_digest 自校验过）；负向测试同脚本逮出「SHA 不符」「points 6 越界」两条

### C. 任务专属（自定义）

- [✓] **X1** · 不污染认证面：发布前后 finance 五文件（decisions/concepts/relations/wisdom/author-profile）SHA-256 逐一不变
  - 验收方法: 发布前 ssh 取五文件 SHA 清单，发布后复取比对（VV 契约「五文件 hash 不回漂」）
  - 证据栏(实施者填): 发布前基线（02423D12…/6BDA2E87…/04EEBB6E…/5BC5FF0E…/0246AD04…）与发布后复取**逐一逐位一致**（ssh 两次 Get-FileHash 实跑）

### 分轨签核（v1.3 · 客观轨总 ✓ + 审查员背书 · 总签必须可审计）

- 客观轨总签（覆盖 R1/R2/R3/N1/N2/X1）：
  - covered_requirement_ids: [R1, R2, R3, N1, N2, X1]
  - authority: Doctor
  - designation_source_ref: PRD frontmatter acceptance_authority（默认验收方）· 本场 AskUserQuestion 总签
  - signed_at: 2026-08-22 22:44（北京时间 · 07:44 PDT）
  - result: PASS——六条客观轨全部 [✓]
  - reviewer_evidence_ref: 独立审查员背书记录（2026-08-22 · subagent a0fdcfb8f3cb71bc5 · 六条全部成立）
- 原则轨（结论/裁定类）共 0 条：录入契约由 VV 给出（§六）、方向由 Doctor 裁，开发中无新分叉裁定

**独立审查员背书记录（2026-08-22 · Task subagent a0fdcfb8f3cb71bc5 · 未参与开发）**：
- 裁定：**R1/R2/R3/N1/N2/X1 六条全部成立**——实跑重跑录入器（幂等 no-op · exit 0 · _last_published.json diff 一致 · fuxi 仅 1 代）；ssh 回读 _xboard 树三件 + 6 项哈希独立重算（inventory/transcript/幂等键/manifest_digest/manifest 字节/文档字节）全对在盘值与 fuxi Get-FileHash；current SHA=F1218B05… 与负向证据一致、坏 staging 已清；源码确认 verify 失败必 raise 且先于一切 Move/current、全部 Move/New 带 -ErrorAction Stop+Test-Path、current 经 .tmp 两段 Move；五文件 SHA 现取五前缀与基线逐一一致。
- 附带发现（均不阻断）：N2 证据栏 fingerprint 前缀转录瑕疵（已更正）；fuxi tmp verify 脚本无持久性要求（每次随推送重传）；班 description 未提录入步（正文步骤已含）。

---

## §2.5 · 执行与交付清单（过程项 · 不参与功能交付关闭判定 · 无 checkbox 表格）

| task_id | 过程项 | task_status | 证据 |
|---|---|---|---|
| T1 | `X-Board/ingest_points.py` 已建（组代/预校验/幂等/发布） | done | py_compile exit 0 · 首代发布成功 · 修复 Move 原子性缺陷后复验 |
| T2 | fuxi verify 脚本随首代推送（loader 口径复算） | done | verify_xboard.py 随推送 · 首代 VERIFY_PASS · 负向逮 2 错 |
| T3 | 首代发布（样例 7676084633146035507）成功 + 回读 | done | gen xb-20260822T135424Z 在盘 · current 指向 · 幂等重跑 no-op |
| T4 | xboard-daily-repush 班 prompt 加录入步 | done | update_scheduled_task 返回 prompt 更新 |
| T5 | X-BOARD-OPERATIONS.md §9.5 补录入契约段 | done | §9.5.1 已落盘 |
| T6 | PRD 证据回填 + 独立审查 + /save 建议 | done | 六条 [?]+证据 · 审查另派 · 回报建议 /save |

---

## §三 · 非交付项(范围排除)

- 不包含: 修改 finance 五文件或 `D-/C-/R-####` 编号体系（VV 契约红线）
- 不包含: 把 Reports/_xboard 纳入 Fuxi→Mac 镜像 profile（VV 明示另立镜像合同，不与录入器混做）
- 不包含: X-Board 改读 DVA _xboard canonical（继续读 Mac producer cache）
- 不包含: 存量 718 篇要点回补（Doctor 已裁「不需要补之前的」；录入器只录入已有 points 缓存）
- 不包含: 触发链「复活」（VV 复核未断、请求一已撤销）

---

## §四 · 状态（current_status + 变更历史 · frontmatter status 为唯一真源）

**状态变更历史**（只追加实际发生的行）:
| 时间 | 从 → 到 | 谁 | 依据 |
|---|---|---|---|
| 2026-08-22 14:00 | draft → in_progress | CC | 任务已授权（Doctor 本场裁定+时机批）· 立卷后进入执行 |
| 2026-08-22 15:30 | in_progress → awaiting_acceptance | CC | 六条交付标准全填 [?]+证据 · 首代发布+回读+幂等+fail-closed+五文件 SHA 全验收实跑 |
| 2026-08-22 22:44 | awaiting_acceptance → delivered | Doctor | 总签（AskUserQuestion · 六条客观轨全部 [✓] · CC 代记留痕） |

---

## §五 · 变更记录

- 2026-08-22 14:00 CC: 立 PRD · 6 条交付标准（R1-R3/N1-N2/X1）· task_authorization 已记录（Doctor 原话 + VV 契约 §六 + 时机裁定）
- 2026-08-22 CC: loader 口径实核（fuxi analysis-utils.js + run_finance_analysis_repair.mjs）：subtitleSha256=sha256(cleanSubtitle(level1.subtitle))（去 <\|…\|> 标签→空白合并→trim→≥50 字）· inventory 数组 create_time 倒序 · stableDigest 键排序
- 2026-08-22 CC: 首代发布踩三坑并修——① verify 参数个数错配（publish 传 4 个 verify 收 3 个）；② inventory_fingerprint 不匹配（inventory 排序：loader create_time 倒序 vs glob 升序，Mac+verify 双侧改为倒序）；③ **PowerShell Move-Item 非终止错误静默吞掉 → current 指向空代**（fuxi 手动修复结构 + 脚本全 Move/New 加 -ErrorAction Stop + 事后 Test-Path 断言）。教训已记入运维 §9.5.1
- 2026-08-22 CC: 六条全填 [?]+证据 → awaiting_acceptance
- 2026-08-22 22:44 Doctor: 总签——六条交付标准全部 [✓]（CC 代记留痕 · 分轨签核已落 · status → delivered）
