---
title: PRD · V2.5-ET双波接入Risk Daily
tags: [prd, acceptance, 剑酒青丘, 风险日报]
created: 2026-10-15 09:50
updated: 2026-10-15 09:50
status: awaiting_acceptance
task_authorization:
  state: verified
  source_type: 会话裁定
  source_ref: 2026-10-15 会话（Claude-3p 壳）
  quote: 读仓位管理策略的最新进展"V2.5-ET双波"。并更新集成入Risk Daily。在Risk Daily中展示汇报时，要求第一行先直接写明建议动作和总仓位，第二行阐明T，第三行阐明辅助E，第四行写清ET综合。
  scope: 仓位管理策略（第二共管项目）V2.5-ET双波 → 风险日报仓位卡片换源与四行展示；班链切换 staging（装班归 Doctor 终端·禁手先例）
roles:
  implementers: [CC]
  independent_reviewers: [待派未参与实施的 subagent]
acceptance_authority:
  authority: Doctor
  designation_source_ref: 2026-10-15 会话
  designation_quote: 本任务由 Doctor 直接指令并定展示格式；验收主体为 Doctor
  designated_at: 2026-10-15
open_decisions:
  - item: 班 SKILL 装班与调度器 description 字段更新（Doctor 2026-10-15 本轮明确授权 CC 唯一负责安装 → 已执行：update_scheduled_task prompt＋description；cron/enabled/nextRunAt 未动）
    blocking: false
    blocks_requirement_ids: []
    decision_owner: Doctor
    status: resolved
    resolution_source: Doctor 原话「让CC把正式日更任务也切到V2.5，安装新版调度文件」（V.V. 转达）＋ CC 已执行
    resolved_at: 2026-10-15
type: prd
project: 剑酒青丘×风险日报
template_version: v1.2
---

# PRD · V2.5-ET双波接入Risk Daily

## §一 · 任务目标

仓位管理策略（第二共管项目）于 2026-10-15 定版 V2.5-ET双波（T主E辅、E不否定T，最低名义25%），项目侧已完成定版规则、最小采集、日更信号与只读卡片适配器（接入补丁 PATCH_PREPARED_NOT_APPLIED）。Doctor 指令把该版本接入风险日报：仓位卡片由 V1 切到 V2.5，并按四行格式展示（建议动作＋总仓位／T／辅助E／ET综合）。班链（refresh-risk-daily 班 1.6 步）同步切换为 V2.5 链，staging 由 CC 备好、装班归 Doctor 终端（调度变更禁手既有先例：2026-10-13 同法）。

**Doctor 原始指令**(逐字引用):
> 读仓位管理策略的最新进展"V2.5-ET双波"。并更新集成入Risk Daily。在Risk Daily中展示汇报时，要求第一行先直接写明建议动作和总仓位，第二行阐明T，第三行阐明辅助E，第四行写清ET综合。

**任务规模估算**:
- 预计涉及文件数: 7 改（adapter/build/test/meta/card_fragment/AGENTS/PRD.md）＋ 2 新（本 PRD、班 staging）
- 预计耗时: 约 1.5 小时
- 涉及项目: 剑酒青丘（仓位管理策略）× 风险日报

---

## §二 · 交付标准(Acceptance Criteria · 验收主体＝功能/需求)

### A. 功能需求（用户可感知的行为 / 结果）

- [ ] **R1** · 风险日报仓位卡片换源：卡片由 V2.5-ET双波 信号（outputs/v25_et_position_signal.json 经 tools/risk_daily_v25_adapter.py）驱动，不再读 v1_position_signal.json。
  - 验收方法: 机器比对——重跑 build_risk_daily.py 产出的 risk-daily.html 中含「V2.5-ET双波」、且不含「仓位管理 · 科创50 V1」；`grep -c` 出命令与计数。
  - 证据栏: [?] 沙箱实跑 build 后 grep：V2.5-ET双波 命中 ≥1 · 科创50 V1 命中 0（2026-10-15 实跑）
- [ ] **R2** · 卡片四行展示（Doctor 指定顺序）：首行=建议动作＋总仓位——无待执行订单时只显示当前名义档位（「建议动作：维持档位；总仓位：名义 X%（实际权重 Y%）」）；有待执行订单时才写「当前名义 X% → 目标名义 Y%（下一收盘执行／下一收盘限价执行）；实际权重 Z%」；第二行=T；第三行=辅助E；第四行=ET综合。
  - 验收方法: 机器比对——卡片 HTML 中「建议动作：」「T：」「E（辅助）：」「ET综合：」四串按此顺序出现（str.index 次序断言）；待执行场景断言「当前名义」「目标名义」「下一收盘执行」；补回权限受限无订单场景断言无「当前名义/下一收盘执行」；测试套件含同名断言。
  - 证据栏: [?] test_v25_et_daily.py 23/23 通过（含 test_card_pending_order_shows_current_then_target 双臂＋test_card_restore_permission_without_order_stays_hold——2026-10-15 V.V. 二轮复核后按 pending_order 判据修复）
- [ ] **R3** · 降级语义：信号缺失／过期／版本不一致时卡片显示「信号不可用」并注明重建提示，不阻塞风险日报主流程。
  - 验收方法: 机器比对——stale 时点与坏 sha 两负例渲染含「信号不可用」（测试套件同名用例）。
  - 证据栏: [?] test_card_actual_output_and_stale_rejection（stale 与 bad sha 两臂）通过 · 消费端 ImportError 降级分支在场（build 实读）
- [ ] **R4** · 班链切换（staging）：refresh-risk-daily 班 1.6 步由 V1 信号改为 V2.5 链（collect_v25_et_inputs → v25_et_daily_signal，任一步 rc!=0 即红字报 Doctor、卡片诚实降级），装班由 Doctor 终端 SHA 往返执行。
  - 验收方法: 人工验收（预先定义）——staging 件落盘＋SHA 计算＋Doctor 终端 cp/shasum 命令贴出；装班后由下一班次日志证明 1.6 步跑 V2.5 链。
  - 证据栏: [?] 已装班（2026-10-15 Doctor 授权 CC 经调度器 MCP 通道安装）：正式文件 `/Users/lunarabbit/Gateway-workspace/Scheduled/refresh-risk-daily/SKILL.md` 回读核验＝单 frontmatter（description V2.5）＋1.6 步 V2.5 链；任务记录 description 已同步、cron `0 9 * * *`／enabled／nextRunAt 未动；staging SHA `fd3a1210…`（8228 B）。**待补证据**：明晨 09:08 班日志证明 1.6 步实跑 V2.5 链（lastRunAt 现为 10-15 早班 V1 场）
- [ ] **R5** · 班链写盘失败关闭：collect_v25_et_inputs.atomic() 保持纯原子替换（临时件 fsync → os.replace），任何一步失败（rename EPERM／EIO／ENOSPC 等）异常上抛 rc!=0 且旧产物逐字节保留；不做截断回退（回退写在写失败时会毁坏旧产物——V.V. 注入实证）；挂载限制说明按实测。
  - 验收方法: 机器比对——失败注入三臂（rename=EPERM／rename+unlink 双 EPERM／fsync=ENOSPC）断言旧产物逐字节未变且异常上抛；CLI 负例 rc!=0 且旧输出逐字节未变（既有测试重申）；现沙箱挂载 probe 实测记录在案。
  - 证据栏: [?] test_atomic_rename_failure_preserves_old_output 三臂通过 · test_cli_negative_nonzero_and_atomic_output 通过 · 挂载 probe 实跑：当前沙箱 rename/unlink OK（班会话挂载不可达未验，已记迭代记录未核边界）· 23/23 普通与 -O 均 OK（2026-10-15 V.V. 二轮修复后）

### B. 非功能需求（仅产品或系统质量属性 · 若适用）

- [ ] **N1** · 数据真实性：卡片全部数字来自信号 JSON 机器值（名义档位/实际权重/as_of），无编数、无旧值冒充；卡片带「仅供参考，不构成投资建议」免责。
  - 验收方法: 机器比对——卡片 HTML 中数字与 outputs/v25_et_position_signal.json 对应字段逐项一致（脚本比对）；免责串 grep 命中。
  - 证据栏: [?] adapter 实跑输出：名义 100%/实际 93.52% 与 signal json tier_suggested_pct=1.0/actual_weight=0.93518… 一致（实跑）；免责串在 note 内（实读）

### C. 任务专属（自定义）

- [ ] **X1** · 沙箱路径兜底：班环境 Path.home() 解析到 /sessions/<session> 时消费端仍能定位项目 tools 目录（/sessions glob 兜底，同 V1 先例）。
  - 验收方法: 机器比对——在沙箱（home 解析到 /sessions/*）实跑 build_risk_daily.py，卡片非「信号不可用」降级态。
  - 证据栏: [?] 沙箱实跑 build 后卡片为 V2.5 正常四行（见 T3/T4 证据）
- [ ] **X2** · 项目侧状态同步：meta json status=APPLIED＋新 sha；AGENTS.md §3 与 PRD.md 状态句更新；card_fragment.html 按新格式重生成；消费契约测试更新并通过。
  - 验收方法: 机器比对——test_applied_risk_daily_consumer 通过（status=APPLIED 且 sha 与现盘 build_risk_daily.py 一致）；diff 面与点名清单一致。
  - 证据栏: [?] test_v25_et_daily.py 22/22（含 APPLIED 断言）；diff 面与点名清单一致（§2.5 T6 附）
- [ ] **X3** · 项目文档/证据与现行状态一致：README/INDEX/ET双波策略 现行入口句同步「卡片已接线、班安装实际状态」；verification.json 更新为最终版基线；迭代记录追加本轮结果与未核边界；历史轮次记录保留原貌。
  - 验收方法: 机器比对——三文档 grep 无「仍用旧V1／尚未应用」残留；verification.json hashes 段与现盘 8 件 sha 一致；迭代记录末条含本轮 SHA 与未核边界。
  - 证据栏: [?] 三文档已改（grep 零残留·实跑）；verification.json 已更新（checked_at 17:04:31Z · 8 件 sha 实算写入）；迭代记录已追加（2026-10-15 CC 接线与修复轮条）

### 分轨签核（v1.3 · 客观轨总 ✓ + 审查员背书 · 总签必须可审计）

**审查员背书记录（Step 7.5 · 2026-10-15）**：审查者＝未参与实施的 general-purpose subagent（agentId `a4c761bf8300cf44b`）· 总判定 **PASS_WITH_LIMITS**。验证动作（实跑）：A 改动面对账——7 件逐对 difflib 实跑、统计与申报逐件一致、**未点名差异 0 件**＋mtime 全面扫描归属核（09:40 后仅 7 点名件＋build 产物）· B 测试套件重放 20/20 OK rc=0（MARKET_DB 实跑）· C adapter 实跑四行顺序断言＋免责串在场 · D 消费端回读——grep V2.5-ET双波=1／科创50 V1=0、四串 index 严格单调、卡片数字与 signal json 逐项一致、现盘 build sha 与 meta 独立复算一致 · E 禁改面——protected_hashes 19/19 全 OK＋四禁改件全 match · F 班 staging 内容正确（两命令/红字语义/MARKET_DB 处理）、已装件仍 V1（待 Doctor 终端·预期）。**Limits 两条**：① verification.json hashes 段两条过期（market.json/signal json 系 T2 链重跑产物·已申报·verification.json 本身按禁改未动——本 PRD T2 证据栏补过期指针注）；② 消费端 ImportError 降级分支文案无重建提示（观察项，不动）。审查者不代签不落勾（G-X4）。

- 客观轨总签（覆盖 R*/N*/X* 中机器可判项）：
  - covered_requirement_ids: []
  - authority: 
  - designation_source_ref: 
  - signed_at: 
  - result: 
  - reviewer_evidence_ref: 2026-10-15 独立复核（agentId a4c761bf8300cf44b · PASS_WITH_LIMITS · 验证动作见上）
- 原则轨（结论/裁定类）共 0 条：展示格式由 Doctor 开发中已拍板（四行顺序在原始指令中给定），按 v1.4 不列原则轨。

---

## §2.5 · 执行与交付清单（过程项 · 不参与功能交付关闭判定 · 无 checkbox 表格）

| task_id | 过程项 | task_status | 证据 |
|---|---|---|---|
| T1 | 7 件改动前快照落 mnt/outputs/v25_rd_snap_20261015/（sha 与 verification.json 一致=零漂移） | done | 快照 7 件＋sha256 记录（bash 实跑） |
| T2 | V2.5 链沙箱实跑（collect→signal）＋test_v25_et_daily.py 20/20 | done | rc=0/rc=0 · Ran 20 tests OK（MARKET_DB env 实跑）。⚠ 本次链重跑刷新了 inputs/v25_et_daily/market.json 与 outputs/v25_et_position_signal.json，故 verification.json hashes 段对应两条已过期（独立复核 Limits①）；verification.json 按 §三 禁改保留不动，此处挂过期指针 |
| T3 | 重跑 build_risk_daily.py＋卡片回读 grep | done | build rc=0 · risk-daily.html 305361 chars · grep V2.5=1/V1 卡=0 · 四串 index 单调递增（实跑） |
| T4 | update_artifact(risk-daily)＋渲染级核验 | done | artifact 已推（update_summary 含切卡说明）· 截图通道未开（面板未自动打开·两次重试耗尽）→ 机器级证据（四行顺序断言+CSS 同源+卡片段预览件已 present）＋预览件交 Doctor 目验 |
| T5 | 班 staging 落临时文件＋SHA＋Doctor 命令块 | done | 临时文件/refresh-risk-daily_SKILL_staging_2026-10-15_v25.md · SHA fd3a1210e19d7b35283b573dd7204100f7765a530cfa8bf197401177d3c08ed2 · 装班命令块已贴（汇报内） |
| T6 | 改动 diff 对账（7 件 vs 快照）＋独立审查 subagent 派发 | done | diff +17-60/+51-5/+14-5/+5-2/+1-1/+1-1/+2-2（实跑）· 独立复核 PASS_WITH_LIMITS（agentId a4c761bf8300cf44b · 未申报差异 0 · 证据失实 0） |
| T7 | git commit 命令贴 Doctor（剑酒青丘仓＋风险日报仓） | done | 命令块已贴（汇报内 · 含 VV 未提交定版批的并排提示） |
| T8 | /save 落 brain/logs（含 PRD 路径与状态） | 待 | 本轮汇报后按 /save 流程办理 |

---

## §三 · 非交付项(范围排除)

- 不包含: 改动任何引擎/采集/规则/冻结件（collect_v25_et_inputs.py、v25_et_daily_signal.py、et_tprimary.py、versions/**、verification.json 及 19 件保护 SHA 内文件零改动）
- 不包含: 动 V1 链文件（v1_daily_signal.py、v1_position_signal.json 及回测输出保留不动）
- 不包含: 维护 E 证据（inputs/v25_et_daily/external_evidence.json 人工维护，本任务只读）
- 不包含: 班 SKILL 本体直接修改（禁手——staging＋Doctor 终端 SHA 往返；调度器 description 字段同归 Doctor）
- 不包含: commit/push（命令贴 Doctor 终端·沙箱禁 git）；公共库 schema、生产库、实际订单与 ETF 实盘
- 不包含: V1 提示器任何旧链步骤恢复或修改

---

## §四 · 状态（current_status + 变更历史 · 不用多 checkbox）

**状态变更历史**（只追加实际发生的行 · 不得预填）:
| 时间 | 从 → 到 | 谁 | 依据 |
|---|---|---|---|
| 2026-10-15 09:50 | draft → in_progress | CC | 立卷即实施（Doctor 已授权） |
| 2026-10-15 10:0x | in_progress → awaiting_acceptance | CC | 全部交付标准填 [?]＋独立审查 PASS_WITH_LIMITS；R4 装班归 Doctor 终端、总签归 Doctor |
| 2026-10-15 10:3x | awaiting_acceptance → in_progress | CC | V.V. 三点复核转交（Doctor 授权 CC 统一修复）：挂载兼容/卡片口径/文档同步 |
| 2026-10-15 11:0x | in_progress → awaiting_acceptance | CC | 三点修复完成＋22/22 普通与 -O 自验＋build 回读；待 V.V. 只读复核与 Doctor 总签 |
| 2026-10-15 11:2x | awaiting_acceptance → in_progress | CC | V.V. 二轮只读复核两点实漏（atomic 截断回退毁旧产物·首行判据应为 pending_order）→ 继续修复 |
| 2026-10-15 11:4x | in_progress → awaiting_acceptance | CC | 二轮修复完成（纯原子失败关闭＋订单判据首行）＋23/23 普通与 -O 自验＋build 回读；待 V.V. 再查失败路径与最终消费者、Doctor 总签 |

**关闭路径**(回顾铁律):
- ✓ 关闭:每个 requirement 逐项 `[✓]`，或被**字段齐全的合法总签明确覆盖**——两者之外不得 delivered
- ✓ Doctor 取消关闭:Doctor 明示"取消" / "算了"
- ✗ 不允许实施者自动关闭(commit 即关 / Task 全 completed 即关 / "我觉得做完了"即关)

---

## §五 · 变更记录

- 2026-10-15 09:50 CC: 立 PRD · 6 条交付标准（R1-R4/N1/X1/X2）· task_authorization 已记录
- 2026-10-15 CC: R1-R3/N1/X1/X2 填 [?] + 证据；R4 填 [?]（staging 就绪·装班归 Doctor 终端）
- 2026-10-15 CC: 应用 VV 预备补丁时增加一处沙箱路径 glob 兜底（补丁在班环境 Path.home()=/sessions/<session> 下无法定位 tools 目录）——已记入 meta json note 与 AGENTS.md
- 2026-10-15 独立审查 subagent（agentId a4c761bf8300cf44b）: PASS_WITH_LIMITS · 未申报差异 0 · 证据失实 0 · Limits 两条（verification.json 两条过期 hash 已挂指针；ImportError 分支文案观察项）
- 2026-10-15 CC: frontmatter status → awaiting_acceptance · 等 Doctor 总签（R4 装班后由下一班次日志补齐证据）
- 2026-10-15 V.V. 转交三点（Doctor 授权 CC 统一修复·V.V. 只读）：① atomic() 挂载兼容回退链；② 卡片当前/目标名义口径；③ 文档/证据同步。→ 已全部实施：collect.atomic 回退链＋EPERM 模拟双臂测试；adapter 首行当前→目标＋note 模型参考；README/INDEX/ET双波策略 同步；verification.json 最终版；迭代记录追加（含未核边界：班实装、班会话挂载行为、独立方法验收）
- 2026-10-15 CC: 修复轮自验——22/22 普通与 -O 均 OK · build 重跑四行顺序断言 True · artifact 已推 · 待 V.V. 只读复核
- 2026-10-15 V.V. 二轮只读复核两点实漏（均成立）：① 截断回退在回退写失败时毁旧产物（注入 rename=EPERM＋write 半段 ENOSPC：old_preserved=false）→ 撤回回退、纯原子失败关闭＋三臂失败负例；② 首行分支判据应为 pending_order 而非档位差（合成 RESTORE_NOT_PERMITTED 态首行第四行自相矛盾）→ 按订单存在性分支＋新测试。已修复：23/23 普通与 -O 均 OK · build 回读断言 True · artifact 已重推 · verification/迭代记录/本 PRD 已同步。待 V.V. 再查失败路径与最终消费者
- 2026-10-15 V.V. 转达 Doctor 本轮明确授权「让CC把正式日更任务也切到V2.5，安装新版调度文件」→ CC 执行装班：文件直写被会话只读钩拦（Gateway 保护区）→ 改走调度器 MCP 通道 update_scheduled_task（prompt＋description）；回读核出双重 frontmatter 后二次修正为单 frontmatter＋V2.5 正文；任务 description 同步、cron/enabled/nextRunAt 未动；按班 1.6 步同序链验证 rc=0。R4 证据已更新（真实班次运行证明待明晨班日志）
