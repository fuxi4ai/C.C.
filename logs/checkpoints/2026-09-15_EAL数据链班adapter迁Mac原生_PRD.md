---
title: PRD · EAL 数据链班 adapter 迁 Mac 原生
tags: [prd, acceptance, 剑酒青丘]
created: 2026-09-15 00:35
updated: 2026-09-15 00:35
status: in_progress  # draft / in_progress / blocked / awaiting_acceptance / delivered / cancelled
task_authorization:
  state: verified
  source_type: 会话裁定
  source_ref: 本会话 2026-09-15 00:2x PT · AskUserQuestion
  quote: 数据链班 adapter 守卫七连修复方案 → Doctor 选「方案①移 Mac 原生（推荐）」
  scope: EAL v3 数据链班 Step 7（zero-write guard loop + verify_run_manifest + eal_post_event adapter 写 production DB）迁 Mac 原生执行；沙箱班 Step 7 改交接+轮询；launchd 执行体安装；班 SKILL 双端同步
roles:
  implementers: [CC]
  independent_reviewers: [待派未参与实施 subagent]
acceptance_authority:
  authority: Doctor
  designation_source_ref: 未指定独立验收方 · 默认 Doctor
  designation_quote: 待补（Doctor 未指定）
  designated_at:
open_decisions:
  - item: launchd plist 安装 + Gateway store SKILL 同步（调度安装属禁手清单·需 Doctor 批并终端执行）
    blocking: true
    blocks_requirement_ids: [R1, R2, X1]
    decision_owner: Doctor
    status: open
    resolution_source:
    resolved_at:
  - item: Mac 班时点（推荐 18:35 PT·沙箱班 Step 6 完成后）与轮询超时（推荐 45 分钟）
    blocking: false
    blocks_requirement_ids: []
    decision_owner: Doctor
    status: open
    resolution_source:
    resolved_at:
type: prd
project: 剑酒青丘
template_version: v1.2
---

# PRD · EAL 数据链班 adapter 迁 Mac 原生

## §一 · 任务目标

数据链班（event-attribution-watch）Step 7 在沙箱 FUSE 挂载面第七次同族停班：zero-write guard 的 permission 组件要求 `chmod a-w` 持久生效，FUSE 下 fchmod 不落地（mode 恒 0o600）→ `permission_guard_completed=false` → REJECTED；另有 verify_run_manifest 因挂载层 st_dev 振荡 fail-closed。后果：artifact `eal-v3-event-transition` 自 09-04 起停更（用户可见）。Doctor 裁方案①：adapter 步骤移出沙箱至 Mac 原生执行——权限语义完整、守卫零弱化（VV/CC 共识第一推荐，NOTE-20260911-001 建议修法①）。

范围：Step 7 三段（`run_with_sqlite_zero_write_guard.py` 包裹的 post-event loop + `verify_run_manifest.py` + `adapters/eal_post_event.py` 写 production DB）整体迁 Mac launchd 原生执行；沙箱班 Step 7 改为「落交接清单 → 轮询 Mac 结果留痕 → 成功续 Step 8 / 超时或失败停班」；Step 8 artifact 推送与其余步骤留在沙箱班。守卫、eal_v3 生产代码、registry/selector/日历契约零改动。

**Doctor 原始指令**(逐字引用):
> 2026-09-15 AskUserQuestion「数据链班 adapter 守卫同族七连（09-01 起·挂 5 天未裁）的修复方案，现在裁吗？」→ Doctor 答：方案①移 Mac 原生（推荐）

**任务规模估算**:
- 预计涉及文件数: 新增 3（Mac 侧脚本 / 交接格式定义 / launchd plist）+ 改 2（班 SKILL Documents 真源 / store 消费端）+ 留痕 2（GOTCHAS / 班日志）
- 预计耗时: 1-2 小时（含 Doctor 终端操作与次班验证）
- 涉及项目: 剑酒青丘 / EAL · 宏观研究体系

---

## §二 · 交付标准(Acceptance Criteria · 验收主体＝功能/需求)

### A. 功能需求（用户可感知的行为 / 结果）

- [ ] **R1** · 数据链班 Step 7 在 Mac 原生环境跑通且零写守卫全组件通过——班简报/shift-log 出现 `permission_guard_completed=true`、adapter exit 0、global report `accepted`（不再出现 LOOP_SQLITE_GUARD_REJECTED 同族停班）
  - 验收方法: 次班（09-15 17:44 PT）后实读 shift-log：Step 7 结果为成功状态、production-zero-write-evidence 回读 status=verified 且 permission guard 成立
  - 证据栏:
- [ ] **R2** · artifact `eal-v3-event-transition` 恢复日更——次班后 updatedAt 前进且 payload 含当班 shadow 渲染结果（用户可见：EAL 事件面自 09-04 停更后恢复）
  - 验收方法: list_artifacts 实读 updatedAt > 09-14；回读 payload 级比对（剥 405B 包装块后与盘上渲染 HTML 逐位一致，G-X120）
  - 证据栏:
- [ ] **R3** · 失败路径 fail-closed：Mac 班失败或超时时，沙箱班停班、不推 artifact、简报附 Mac 留痕根因
  - 验收方法: 故障注入（Mac 班故意失败一次）或首个真实失败班观察：班简报明确失败+artifact 未推
  - 证据栏:
- [ ] **R4** · 交接与结果留痕可审计：沙箱班落交接清单（含当班 snapshot_dir/loop 输入路径），Mac 班落结果留痕（成功/失败+关键输出摘要），两者均落 Documents 盘、周巡检可读
  - 验收方法: 文件按定义格式存在于约定路径、字段核通过（machine 比对）
  - 证据栏:

### B. 非功能需求

- [ ] **N1** · 守卫零弱化：zero-write guard 在 Mac 原生以原参数运行，production-zero-write-evidence 回读 `status=verified`、目标 exact=attribution.db、journal_mode=delete、read transaction/permission guard 成立、主文件身份全等且全窗未见 WAL/SHM/journal
  - 验收方法: evidence JSON 字段逐项实读比对（与 SKILL Step 7 回读判据一致）
  - 证据栏:
- [ ] **N2** · 可靠性：沙箱班轮询 Mac 留痕的超时阈值在班 SKILL 内明确写出且轮询间隔合理（失败即停班，不无限等）
  - 验收方法: SKILL 实读含超时值与 fail-closed 行为
  - 证据栏:

### C. 任务专属

- [ ] **X1** · Mac 侧执行体已安装且被调度触发：launchd plist 装入 Mac 本机、`launchctl list` 回读可见、每日 18:35 PT 左右触发（沙箱班 Step 6 完成后）
  - 验收方法: Doctor 终端 `launchctl list | grep` + 首班触发证据（Mac 结果留痕时间戳）
  - 证据栏:
- [ ] **X2** · 班 SKILL 双端一致：Documents 真源（`调度/event-attribution-watch/SKILL.md`）与 Gateway store 消费端逐字一致（SHA 相同）
  - 验收方法: Doctor 终端 shasum 双端对拍（store 侧 SHA 由 Doctor 终端读）
  - 证据栏:

### 分轨签核（v1.3 · 客观轨总 ✓ + 审查员背书）

- 客观轨总签（覆盖 R1-R4/N1-N2/X1-X2）：
  - covered_requirement_ids: []
  - authority:
  - designation_source_ref:
  - signed_at:
  - result:
  - reviewer_evidence_ref:
- 原则轨（结论/裁定类）共 0 条（开发中分叉裁定走变更记录 · 2026-08-15 Doctor 立）

---

## §2.5 · 执行与交付清单（过程项 · 无 checkbox 表格）

| task_id | 过程项 | task_status | 证据 |
|---|---|---|---|
| T1 | Mac 侧脚本落盘：`~/Documents/Claude/Projects/Financial/宏观研究体系/EAL/调度/eal-post-event-native/run_step7_native.py`（Step 7 三段原样+读交接清单+写结果留痕） | done | 文件在盘（11.5KB）· py_compile OK · 负向测试 3 组全绿（无交接退 0/坏交接 fail 留痕退 2/幂等退 0） |
| T2 | 交接清单与结果留痕格式定义落盘（同目录 FORMAT.md） | done | 文件在盘（2.9KB） |
| T3 | 班 SKILL Documents 真源 Step 7 段改为交接+轮询（Edit·改前备份） | done | 214 行 · 旧段残留 0 · 新段锚点 3 · 备份 SKILL.md.bak_pre_macnative_20260915（17772B 与原一致） |
| T4 | launchd plist 草案落盘 + 贴 Doctor 终端命令（安装+load） | done | plutil OK · py_compile OK · launchctl list 回读 `- 0 com.eal.postevent-native`（Doctor 终端实跑 09-15 00:4x） |
| T5 | Gateway store SKILL 同步（Doctor 终端 SHA 往返） | done | store SHA=cacf0b6f…=staging=真源（Doctor 终端 shasum 输出） |
| T6 | 独立审查（未参与实施 subagent·只读重放） | todo | |
| T7 | 剑酒 GOTCHAS NOTE-20260911-001 状态行更新（修复已实施·🔄 已修待验） | done | 状态行已改 + 追记（2026-09-15 凌晨·方案①实施）已落 |
| T8 | git commit 命令贴 Doctor（宏观研究体系仓+Database 仓） | done | Doctor 终端实跑：brain f4b1e35 已 push（f2e35d8..f4b1e35）；宏观研究体系 9f1dc70 本地 commit（5 文件·无 remote 即止） |
| T9 | 次班（09-15 17:44 PT）验证 R1/R2 证据采集 | todo | |

---

## §三 · 非交付项(范围排除)

- 不包含: 修改 eal_v3 生产代码、zero-write guard、registry/selector/consumer pin/冻结日历（契约零改动）
- 不包含: 班时点/班次增删（现有 17:44 PT 数据链班不动；新增的 Mac 执行体是 launchd 本地班、不经过 Gateway 调度器）
- 不包含: Step 1-6/8/9 改造与 artifact 推送机制变更
- 不包含: 沙箱班与数据链的其它既有缺陷（星空班锚定语义已由 Doctor 裁「班移 21:00 PT」另行处理；NOTE-20260911-002 risk.py 赢面门独立待裁）

---

## §四 · 状态（current_status + 变更历史）

**状态变更历史**:
| 时间 | 从 → 到 | 谁 | 依据 |
|---|---|---|---|
| 2026-09-15 00:35 | draft → in_progress | CC | 立卷·Doctor 已裁方案①（AskUserQuestion 答） |

**关闭路径**: 每个 requirement 逐项 `[✓]` 或被字段齐全总签覆盖；或 Doctor 显式取消。

---

## §五 · 变更记录

- 2026-09-15 00:35 CC: 立 PRD · 含 8 条交付标准（R1-R4/N1-N2/X1-X2）· task_authorization 已记录
