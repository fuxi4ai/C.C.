---
title: PRD · EAL加SOX响应轨
tags: [prd, acceptance, 剑酒青丘, EAL]
created: 2026-09-04 14:00
updated: 2026-09-04 14:00
status: in_progress
task_authorization:
  state: verified
  source_type: 会话裁定
  source_ref: 2026-09-04 本会话（早场 NFP 分析后）
  quote: "因为我们的持仓集中在高景气AI相关标的中，所以，有必要照这个数据对EAL进行迭代，加入SOX，使EAL除了对大盘的解释和预测，也能够更清晰的解释和预测半导体方向所受的影响和传导机理。"
  scope: 响应轨先行——^SOX 加入数据/归因/展示三层，描述性 shadow 同口径；本轮不扩 registry（半导体事件族另开）
roles:
  implementers: [CC(本场)]
  independent_reviewers: [待派未参与实施的 subagent]
acceptance_authority:
  authority: Doctor
  designation_source_ref: 待指定（Doctor 未指定独立验收方时默认 Doctor 亲自验收）
  designation_quote: ""
  designated_at: ""
open_decisions:
  - item: AskUserQuestion 两题裁定（响应轨先行/不扩 registry）——已裁，记入授权
    blocking: false
    blocks_requirement_ids: []
    decision_owner: Doctor
    status: resolved
    resolution_source: "AskUserQuestion 2026-09-04：「响应轨先行（推荐）」「本轮不扩 registry（推荐）」"
    resolved_at: 2026-09-04
  - item: 班 prompt 更新（Gateway store 沙箱不可读）——执行路径=Doctor 终端 SHA 往返（staging 草案 CC 备）
    blocking: false
    blocks_requirement_ids: [R4]
    decision_owner: Doctor
    status: resolved
    resolution_source: 2026-09-05 实读班 SKILL 全文：ticker 列表真源在 `update_attribution_db.py` L27（沙箱可写），班 prompt 无需改动；R4 改为验收 updater TICKERS + 班后 ^SOX 前进（见 §四 变更记录）
type: prd
project: 剑酒青丘 / EAL
template_version: v1.2
---

# PRD · EAL加SOX响应轨

## §一 · 任务目标

**动机**：持仓集中在高景气 AI 相关标的（光通信/半导体链），EAL 现市场轨仅 SPY/QQQ/^VIX——2026-09-04 NFP 案例（SPY -0.4% vs SOX +3.4%，背离 3.8pp）证明大盘轨看不到半导体分层响应，而这正是持仓最需要的信息缺口。

**范围**：^SOX 作为响应轨加入三层——①每日班 loop 归因（market_response 加 SOX 键，同口径 close_to_close_pp / horizon 0·1·3·5）；②engine targets 加 ^SOX（shadow/cluster 渲染自动带出，render_results.py 动态遍历 targets 无需改）；③prices_daily 历史回填（2026-02-28 至今日频 OHLC）+ 班每日拉取。方法合同、estimands、registry、schema 结构均不动。

**Doctor 原始指令**(逐字引用):
> "因为我们的持仓集中在高景气AI相关标的中，所以，有必要照这个数据对EAL进行迭代，加入SOX，使EAL除了对大盘的解释和预测，也能够更清晰的解释和预测半导体方向所受的影响和传导机理。"

**分叉裁定**（AskUserQuestion 2026-09-04 · 已批推荐项）：「SOX 深度=响应轨先行」「半导体事件族=本轮不扩 registry」。

**任务规模估算**:
- 预计涉及文件数: 4（loop 脚本改 ~10 处 · engine targets 1 处 · 回填脚本新写 · 班 prompt 换文）
- 预计耗时: 3-5 小时（含 Doctor 终端回填与班 prompt SHA 往返）
- 涉及项目: 剑酒青丘 / EAL

---

## §二 · 交付标准(Acceptance Criteria · 验收主体＝功能/需求)

### A. 功能需求（用户可感知的行为 / 结果）

- [?] **R1** 每日班归因输出含 SOX 市场响应轨 → 预期：`event_day_attribution` 每条的 `market_response` 出现 "SOX" 键，含 `close_to_close_by_horizon`（h0/1/3/5）与 SPY 同口径 → 验收方法：沙箱实跑 loop（sealed 库 + ^SOX 测试数据）读输出 JSON → 证据：①测试断言（test L162-163）23/23 过；②生产 sealed 库实跑 15 行归因全部含 SOX 键 exit 0；③独立审查员实跑端到端输出 SOX block h0=0.75757576/h1=-0.37878788/h3=3.03030303/h5=2.65151515 unit=percentage_points → 状态：[?]
- [ ] **R2** artifact 半导体轨展示 → 预期：shadow/cluster 的 targets 出现 ^SOX 卡（与 SPY 对照，背离肉眼可读） → 验收方法：render_results.py 实跑后 HTML 含 "^SOX" 标识；或下次班 shadow 重跑后回读 artifact → 证据：待 engine cp + ^SOX 回填后 shadow 重跑 → 状态：[ ]
- [?] **R3** ^SOX 历史回填 → 预期：prices_daily 含 ^SOX 自 2026-02-28 至最新交易日日频 OHLC（与 SPY 同窗口可比） → 验收方法：只读 SQL `SELECT COUNT(*), MIN(trade_date), MAX(trade_date) FROM prices_daily WHERE ticker='^SOX'` → 证据：Doctor 终端实跑回填脚本（2026-09-05）：`✓ ^SOX 回填 137 行 · 2026-02-20 → 2026-09-04`（比 SPY 窗口还新一天 · 备份 attribution.db.bak_preSOX_20260905_0738 在盘） → 状态：[?]
- [ ] **R4** 班每日行情拉取含 ^SOX → 预期：update_attribution_db.py TICKERS 含 "%5ESOX" 且下一真实班跑后 ^SOX 最新 trade_date 前进 → 验收方法：班后只读 SQL 查 ^SOX MAX(trade_date) 且 triggered_by=scheduled → 证据：TICKERS 改动已落（L27 · 独立审查核仅此一处）；下次班 = 09-07 周一 → 状态：[ ]

### B. 非功能需求（性能 / 安全 / 可靠性 / 兼容性 / 数据质量）

- [?] **N1** 既有测试全绿 → 预期：`test_eal_post_event_loop.py` 与 `eal_v3/tests` 跑通 exit 0 → 验收方法：实跑测试套件 → 证据：loop 套件 23/23 exit 0（实跑）；eal_v3/tests contract 35/35·migration 19/19·legacy 7/7·acceptance 6/6·benchmark 两档 limits 内（独立审查员实跑 · caveat：跑在 canonical engine 上，staging cp 后建议重跑） → 状态：[?]
- [?] **N2** 口径一致性 → 预期：SOX 轨无新单位/新口径（close_to_close_pp · horizon 0/1/3/5 · 与 SPY 同款字段名） → 验收方法：输出 JSON 字段核 → 证据：独立审查实跑 SOX block 字段名与 SPY 同款（无 intraday_range_pp_h0 · 与 QQQ 同形符合声明范围） → 状态：[?]
- [?] **N3** fail-closed → 预期：^SOX 缺数据时班只走 `EAL_OPTIONAL_MARKET_DATA_MISSING` 警告路径不停班；SPY 硬门不变 → 验收方法：负向测试（^SOX 空数据跑 loop 警告出现且 exit 0） → 证据：新增 test_sox_missing_warns_not_blocks 通过 + 独立审查 A/B 实跑（status=completed_with_warnings · 警告确为 ticker=^SOX · SOX 键仍在 h0=None） → 状态：[?]

### C. 自定义验收

- [?] **X1** 描述性不越界 → 预期：含 SOX 轨的 attribution `causal_claim` 保持 `not_established` → 验收方法：输出 JSON 字段核 → 证据：causal_claim 硬编码+review 门+FORBIDDEN_CLAIMS 门均在；A/B 实跑 causal_claim 均 not_established，且 intensity 与 SPY 块在 SOX 有无时逐字节一致（SOX 不参与打分） → 状态：[?]

### 审查员背书（2026-09-05 · 独立 subagent 实跑复核）

- 审查者：未参与实施的独立 subagent（general-purpose · 28 次工具调用 · 只读纪律无违规）
- 结论：**PASS_WITH_LIMITS**——四改动文件核验通过、测试证据真实、SOX 无越界污染（grep 全文件仅 5 处 · intensity/findings 零污染）
- 验证动作摘录：实跑 23 测试 OK / py_compile 四文件 / diff 仅 1 hunk / 独立端到端 A/B 实跑（SOX 有无对照 · intensity 逐字节一致）/ eal_v3 全套件实跑
- 限制三条：①engine staging 未部署（待 Doctor 终端 cp）；②^SOX 历史回填未落（生产库 0 行）；③两处未声明副产物（见 §四 变更记录 09-05 注记）

---

## §2.5 · 执行清单（过程项 · 不参与功能交付关闭判定）

| task_id | task_status | evidence |
|---|---|---|
| T1 改 loop 脚本（OPTIONAL_TICKERS/SQL/attribution 组装加 SOX） | 完成 | 5 处 Edit 已落 · 独立审查 grep 核仅 5 处 SOX |
| T2 改 engine targets 加 ^SOX 条目 | 完成 | Doctor 终端 cp 部署（2026-09-05）· SHA 26534486… 与 staging 逐字一致 · 备份 engine.py.bak_preSOX_20260905 · 防写锁已恢复 |
| T3 写 ^SOX 历史回填脚本（Yahoo → prices_daily） | 完成 | Doctor 终端实跑：137 行 · 02-20 → 09-04 · 自带备份在盘 |
| T4 班行情拉取含 ^SOX | 完成（方案变更） | 班 prompt 不需改——ticker 列表在 `update_attribution_db.py` L27，沙箱直接改（%5ESOX）· 独立审查核仅此一处 |
| T5 测试（既有套件 + N3 负向） | 完成 | 23/23 exit 0（新增 1 负向测试）· eal_v3 全套件绿 |
| T6 自验填三态 | 完成 | §二 R1/N1/N2/N3/X1 填 [?]+证据 · R2/R3/R4 留 [ ] |
| T7 独立审查 subagent（未参与实施） | 完成 | PASS_WITH_LIMITS · 背书已落 §二 尾部 |
| T8 git commit 命令贴 Doctor（禁 add -A · 先探后加） | 待执行 | 见实施回报命令块 |

## §三 · 非交付项

- 不扩 registry：半导体行业事件族（NV 官宣/出口管制等）不入 EAL 事件库——Doctor 裁「本轮不扩」
- 不升级传导系数框架：方法合同不动，背离读数积累后再议（Doctor 裁「响应轨先行」）
- 不动 schema 结构：prices_daily 表结构不变（只加 ^SOX 行）；不新增表/索引
- 不做 SOX 预测模型：描述性 shadow 口径，不承诺因果权重与预测性
- 不动 SMH/CL=F/DGS2/DGS10 既有 targets 条目（engine 已预留，本轮只加 ^SOX）

## §四 · 变更历史

| 时间 | 变更 | 方式 |
|---|---|---|
| 2026-09-04 14:00 | 立卷（授权=会话裁定 · 分叉两题已裁推荐项） | CC 立卷 |
| 2026-09-05 01:30 | 实施完成 + 自验三态 + 独立审查 PASS_WITH_LIMITS。T4 方案变更：班 prompt 不动——ticker 列表真源是 `update_attribution_db.py` L27（沙箱直接改）。两处无害副产物接受（审查员判定）：①%5ESOX 连带 15m 写入 prices_intraday（无完整性门但无危害）；②loop coverage 的 market_tickers_available 将含 ^SOX（ALL_TICKERS 自然结果） | CC 实施 + 独立审查背书 |
| 2026-09-05 01:30 | open_decisions「班 prompt 更新」resolved：不需改班 prompt（见上） | CC 实读班 SKILL 全文判定 |
