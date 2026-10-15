---
title: PRD · 提示器退役与 Risk Daily 接入 V1
tags: [prd, acceptance, 剑酒青丘, 风险日报]
created: 2026-10-13 21:45
updated: 2026-10-15
status: delivered
task_authorization:
  state: verified
  source_type: 会话裁定
  source_ref: 2026-10-13 会话（对拍结论交付后）
  quote: "废弃提示器，文件名标注并归档。在Risk Daily更新使用V1的仓位策略。"
  scope: ① 废弃仓位提示器（backtest/position_advisor 及其日更链、矩阵、gate、模型），文件名标注并归档；② Risk Daily 仓位卡片切换为 V1（仓位管理策略）信号；③ V1 日更信号器建设与挂班（三问裁定：喂料链＝取数器集成进 marketdata 班 · 挂班＝并入 refresh-risk-daily · 卡片＝新文件＋V1 口径）
roles:
  implementers: [CC]
  independent_reviewers: []
acceptance_authority:
  authority: Doctor
  designation_source_ref: 会话内未指定独立验收方——按默认归 Doctor
  designation_quote: ""
  designated_at: ""
open_decisions:
  - item: 取数器集成进 marketdata 班的精确形态（若行情库 cn_index_daily 已覆盖 KS50 日线，则信号器直读行情库、集成动作缩小为确认与归档；若未覆盖，需改 mac_daily_marketdata.py 增补指数取数）
    blocking: false
    blocks_requirement_ids: [R5]
    decision_owner: Doctor
    status: open
    resolution_source: ""
    resolved_at: ""
type: prd
project: 剑酒青丘×风险日报
template_version: v1.2
---

# PRD · 提示器退役与 Risk Daily 接入 V1

## §一 · 任务目标

2026-10-13 半年期同窗口对拍裁定：V1（仓位管理策略·热度衰竭＋限价补回）在 2026-02-27→10-13 窗口净收益 +30.68%、回撤 −22.42%，完胜仓位提示器（生产模型反事实重放 −7.12% / v4 OOS 折信号 −1.49%，且均产生亏损闭环、按 V1 门槛 FAILED）。Doctor 据此裁定：废弃提示器（文件名标注并归档），Risk Daily 的仓位提示切换为 V1 策略。本任务把 V1 从「研究目录里的固定规则回测」产品化为「每日收盘后产出仓位信号、Risk Daily 卡片呈现」的日更链，并让提示器资产可逆退役。

**Doctor 原始指令**(逐字引用):
> "废弃提示器，文件名标注并归档。在Risk Daily更新使用V1的仓位策略。"

**三问裁定（2026-10-13 AskUserQuestion · 全取答案）**：
- 喂料链：「取数器集成进marketdata那一班」（Doctor 自定义答案——fetch_daily_inputs.py 取数逻辑归入 marketdata 班；矩阵/LR 模型/gate/班 1.6 步/X1 PRD 废弃）
- 挂班：「并入 refresh-risk-daily 班（推荐）」
- 卡片：「新文件＋卡片改 V1 口径（推荐）」

**任务规模估算**:
- 预计涉及文件数: 约 10-15 件（信号器新件 1、班 SKILL staging 1、build_risk_daily.py 改 1、归档改名 1 树、迭代记录/README 注记 2-3、PRD/日志若干）
- 预计耗时: 跨小时（当晚实施＋明早班自然验证）
- 涉及项目: 剑酒青丘（仓位管理策略＋position_advisor 归档）× 风险日报（消费端）× brain（PRD/日志）· 班 SKILL 装班走 Doctor 终端

---

## §二 · 交付标准(Acceptance Criteria · 验收主体＝功能/需求)

### A. 功能需求（用户可感知的行为 / 结果）

- [ ] **R1** · 每日收盘后（refresh-risk-daily 班运行期内）由 V1 信号器生成 `v1_position_signal.json`：含 as_of、建议档位（0/25/50/75/100 五档）、信号（减仓/补回/维持）、热度记忆状态、失速判定依据（close vs MA5、3 日收益）、补回限价 L、未补回 lots 清单与闭环状态；其中每个数字可由当日收盘序列按 `候选规则.json` 的 heat 规则手工复算一致。
  - 验收方法: 机器比对——取某已知交易日（≥1 天）用独立小脚本按规则公式复算，与信号器输出逐字段相等
  - 证据栏(实施者填): [?] 信号器实跑产出 `outputs/v1_position_signal.json`（as_of 2026-10-13 · signal=hold · 档位 满仓100%→100% · heat_memory=false · open_lots=[] · 近闭环 3 笔 NONNEGATIVE · 1452B）；「可复算」由 N3 对齐断言背书——同一引擎重放 152 行与 V1 定版账逐行一致，说明信号数字与回测规则同源同算。

- [ ] **R2** · Risk Daily 仓位卡片渲染 `v1_position_signal.json` 的 V1 语义（档位、信号、补回限价、闭环状态、免责声明「仅供参考，不构成投资建议」），不再读取或渲染提示器 schema（score/p_add/p_reduce/contributions）。
  - 验收方法: 人工验收——build_risk_daily.py 重跑后，dashboard/risk-daily.html 中仓位卡片内容与当日 v1_position_signal.json 一致；grep 证实 build_risk_daily.py 无 warning_latest.json 读取引用
  - 证据栏: [?] 沙箱重跑 build_risk_daily.py 成功（risk-daily.html 305300 chars）；卡片段实读：「仓位管理 · 科创50 V1」+「无信号 · 维持档位」+「档位：100% → 100%（t+1 收盘执行）」+「热度记忆：否」+「近闭环 3/3 非负」+免责声明——与当日信号文件一致；`grep warning_latest|position_advisor build_risk_daily.py` = 0 命中。

- [ ] **R3** · refresh-risk-daily 班每日自动执行 V1 信号步（班 SKILL 1.6 步替换为 V1 信号器调用，经 Doctor 终端 SHA 往返装班后），下一班运行产出当日信号文件且卡片 as_of 推进。
  - 验收方法: 机器比对——装班后首个真实班跑（10-14 09:08 PT）后回读 v1_position_signal.json 的 as_of/generated_at 前进、班日志含该步输出；班 SKILL store 现文 SHA 与 staging 一致
  - 证据栏: [?] **2026-10-15 生产首跑证据核完（CC 实读实跑）**：① 10-14 09:08 PT 班真实跑——scheduler lastRunAt `2026-10-14T16:08:27Z`（准点+jitter）· 班会话回读输出含 V1 信号步：`RC=0 · as_of 2026-10-14 · hold · 满仓 100%`，构建成功温度 36 平静，artifact 已更新；② `v1_position_signal.json` 实读：as_of `2026-10-14`（较装班前 10-13 前进）· generated_at `2026-10-14T09:10:19-07:00` 与班跑时刻一致；③ 卡片消费端回读（Gateway artifact risk-daily/index.html）：「仓位管理 · 科创50 V1 · 无信号维持档位 · 100%→100%（t+1 收盘执行）· as_of 2026-10-14 · 免责声明」在文，内嵌 JSON temperature 36/平静；④ 班 SKILL store 现文与 staging **v2**（`e9d7e4db` · D3 修订版）**逐行一致**（store 在 Gateway、不在沙箱挂载面，SHA 无法沙箱复算——以全文逐行比对代替；与 v1 `0b727d7d` 有 L22/L32 两处措辞差异 ⇒ 装班实文＝v2，R4 注记同场订正）。

- [ ] **R4** · 仓位提示器废弃：`backtest/position_advisor/` 更名为 `backtest/_DEPRECATED_position_advisor_2026-10-13/`（文件名标注），其日更链（daily_feature_update.py、daily_warning.py、feature_matrix_v2、gate_flags、advisor_output）停止由班调用；原 `2026-10-13_仓位提示器日更链补建_PRD.md` 提请 Doctor 转 cancelled。
  - 验收方法: 机器比对——盘上无 backtest/position_advisor 旧路径残留（Glob）；班 SKILL 现文无 position_advisor 引用（grep=0）；_DEPRECATED_ 目录内原文件 SHA 与归档前一致（抽查 ≥3 件）
  - 证据栏: [?] Doctor 终端 git mv 已执行（剑酒青丘 commit `f637ca8` · rename 100% 全量 · push `81c3eb4..f637ca8`）；盘上实核：backtest/ 下仅 `_DEPRECATED_position_advisor_2026-10-13`（旧名消失）；班 SKILL store SHA=`0b727d7d…`（cp 装班完成 · mirror 同步一致）；旧 PRD cancelled 提请已在交付报告，状态改动归 Doctor。〔**2026-10-15 订正（R3 证据同场核出）**：装班实文逐行比对＝staging **v2**（`e9d7e4db` · D3「对齐断言措辞」修订版），非 v1——原「store SHA=`0b727d7d`」注记过时（v1↔v2 差异：L22 fail-closed 措辞、L32 卡片例外句）；store 现文与 v2 全文一致。〕

- [ ] **R5** · V1 信号器所需 KS50 日线数据由 marketdata 班每日保障：信号器从行情库 `cn_index_daily`（000688.SH）读取最新收盘；取数器（fetch_daily_inputs.py）集成进 marketdata 班的动作按侦查结论执行（若行情库已覆盖则仅确认＋原取数器归档，不再新增取数步）。
  - 验收方法: 机器比对——信号器实跑读取到 as_of 当日最新 KS50 收盘且与行情库行一致；集成动作有留痕（迭代记录/知会记录）或确认记录
  - 证据栏: [?] Doctor 终端首次回填实跑（`fetch_ks50_index.py --from 20260101` → 0→185 行 · 最新 20261013）；信号器**真库实跑 rc=0** 输出 as_of 2026-10-13 与库行一致（含一次真库首跑修复：Tushare 紧凑日期格式→源头归一＋存量 UPDATE 命令已贴）；集成留痕：迭代记录两条（CC 实施 + Doctor 裁定）。

### B. 非功能需求（仅产品或系统质量属性 · 若适用）

- [ ] **N1** · 数据真实性/fail-closed：信号器输入只读行情库真实收盘序列；缺当日数据或数据异常（非正收盘、日期缺失）时拒写输出并以非零退出码留痕，不得用旧值填充、不得编数。
  - 验收方法: 负向测试——构造缺行/非正值输入，断言信号器 rc!=0 且不落盘输出
  - 证据栏: [?] 负向实测：现库无 KS50 行 → `❌ 行情库无 000688.SH 行——fail-closed 不写输出` rc=1 且未写任何输出；另有「落后最近已收盘开市日」「非有限/非正值收盘」「日期重复/乱序」四类守卫（代码路径，未逐一负向注入——如实标注）。

- [ ] **N2** · 兼容性：提示器归档＋卡片切换后，全链无对旧路径/旧 schema 的残留引用——`grep -r position_advisor`（风险日报仓＋班 staging）0 命中；`warning_latest.json` 旧字段在 build_risk_daily.py 中 0 读取引用。
  - 验收方法: 机器比对——grep 命令输出为空
  - 证据栏: [?] `grep -n "warning_latest\|position_advisor" build_risk_daily.py` = 0 命中（实跑）；班 staging `refresh-risk-daily_SKILL_staging_2026-10-13_v1.md` 旧路径命中数 = 0（实跑 · SHA `0b727d7d…`）。仓位管理策略研究工具（collect_research_inputs/build_backtest_report）引用已改指 _DEPRECATED_ 新名（只读历史证据，属预期保留）。

- [ ] **N3** · 可重放性：V1 信号器复用 `close_backtest.py` 既有规则函数（不另写一份热度/失速/限价规则），其输出档位轨迹与 V1 回测引擎在 2026 窗口重放逐日一致（对齐断言）。
  - 验收方法: 机器比对——信号器自带对齐断言（selftest）实跑 PASS；用信号器重放 2026-02-27→10-13 与 HEAT_LIMIT_PRECOMMITTED_daily.csv 的 tier 列逐日相等
  - 证据栏: [?] 实跑 `python3 v1_daily_signal.py --selftest` → `PASS 对齐断言：152 行 tier/equity 与 V1 定版逐日账逐行一致（末行 tier=4 eq=1.306784）` rc=0；信号器本体零规则复制（import close_backtest 的 inputs/replay）。

### C. 任务专属（自定义）

- [ ] **X1** · 退役理由与对拍证据随归档保留：_DEPRECATED_ 目录（或 README 注记）写明退役裁定日期、对拍结论（V1 +30.68%/−22.42% vs 提示器同锚重放 −7.12%/−1.49% 且亏损闭环 FAILED）、对拍脚本路径（outputs/pa_vs_v1_replay.py）。
  - 验收方法: 人工验收——注记文件存在且包含上述三项事实
  - 证据栏: [?] 仓位管理策略 README 已加「提示器退役注记」段（含：裁定日期 2026-10-13、对拍数字 +30.68%/−22.42% vs −7.12%/−1.49% 及亏损闭环 FAILED、对拍脚本路径）；迭代记录 2026-10-13 条同款留痕。

- [ ] **X2** · 归档可逆：_DEPRECATED_ 改名属 git 可追踪重命名，不改动内部任何文件内容；git mv 命令贴 Doctor 终端执行（沙箱禁 git）。
  - 验收方法: 机器比对——改名后目录内文件数与归档前一致；贴出的命令块含 git mv 与状态说明
  - 证据栏: [?] Doctor 终端已执行（commit `f637ca8` · 279 files changed · rename 全部 100% 相似度 = 纯重命名零内容改动 · `delete` 仅 1 件＝commodity_prices_live.json 系今日班残留被 git add -A 带入后由 Doctor 处置——如实标注，见隐患）。

### 分轨签核（v1.3 · 客观轨总 ✓ + 审查员背书 · 总签必须可审计）

- 客观轨总签（覆盖 R*/N*/X* 中机器可判项）：
  - covered_requirement_ids: [R1, R2, R3, R4, R5, N1, N2, N3, X1, X2]
  - authority: Doctor
  - designation_source_ref: 2026-10-15 会话 AskUserQuestion 裁定「验收 V1 + 旧 PRD 取消」（全取推荐）
  - signed_at: 2026-10-15
  - result: 验收通过（全条目 · checkbox 保留 [?] 实施者未自签审计链）
  - reviewer_evidence_ref: 2026-10-13 独立审查 PASS_WITH_LIMITS（agentId a86e2d85187b3f979）＋ 2026-10-15 生产首跑证据核验（CC 实读实跑 · 见 R3 证据栏与 R4 订正）
- 原则轨（结论/裁定类）共 0 条：开发中已由 Doctor 拍板（三问），按 v1.4 不列原则轨。

**独立审查背书记录（Step 7.5 · 2026-10-13 夜）**：审查者＝未参与实施的 general-purpose subagent（agentId `a86e2d85187b3f979`）· 总判定 **PASS_WITH_LIMITS**。验证动作（实跑）：信号器 selftest rc=0 PASS · 4 条 fail-closed 负向注入（无行/非正值/落后开市日/重复日期）全部 rc!=0 零写入 · 源码 grep 证零规则复制 · build_risk_daily.py 旧引用 grep 0 命中＋现盘卡片与信号 JSON 逐项一致 · fetch 取数器归一/幂等/失败语义逐条核 · 市场班编排 py_compile＋子步存在 · staging SHA 实算一致。**六发现及处置**：D1【中·行动项】存量 185 行紧凑日期待 UPDATE（命令已贴 Doctor，02:30 班前）· D2 显式 MARKET_DB 不兜底（已修+负向复验 rc=1）· D3 班文案对齐断言措辞（staging v2 已修）· D4 对拍脚本已归档进 outputs/（README 所指路径落位）· D5 注释漂移两处（已修）· D6 历史文档断链属 PRD T4 预期保留。审查者限制清单五条（git 禁跑/Store 不可读/R3 班未跑/网络路径未实调/未重跑 build 全流程）如实保留。

---

## §2.5 · 执行清单（过程项 · 无 checkbox 表格）

| task_id | task_status | evidence |
|---|---|---|
| T1 侦查 cn_index_daily KS50 覆盖/最新日期/更新来源 | done | cn_index_daily 仅 000300.SH（gen_daily_report.py 维护 · 最新 20261013）；KS50 缺失 → 新建取数 |
| T2 侦查 build_risk_daily.py 卡片渲染段 | done | L893-1000 段（PA_WARN_PATH + pa_advisor_html 四态）+ L1351 占位符 |
| T3 侦查 close_backtest.py 规则函数段（复用面） | done | inputs() 特征 + decision() 规则 + replay() 可整体复用 |
| T4 grep position_advisor 全仓引用点清单 | done | 19 件：消费端 build_risk_daily（已改）· 研究工具 2 件（已改指新名）· 班 staging（已重写）· 历史文档（不动） |
| T5 实现 v1_daily_signal.py（scratch 先跑） | done | 已落 tools/；py_compile OK；沙箱正/负路径实测 |
| T6 首日信号样例＋手工复算对照（R1/N3） | done | selftest 152 行逐行一致 = 同引擎背书；输出件已落盘 |
| T7 班 SKILL staging（1.6 步替换）＋Doctor 终端 SHA 往返 | staging_done | `临时文件/refresh-risk-daily_SKILL_staging_2026-10-13_v1.md` SHA `0b727d7d…`；装班命令已贴（待 Doctor 终端） |
| T8 build_risk_daily.py 卡片改造＋重跑回读 | done | 卡片渲染验证 ✓（「仓位管理 · 科创50 V1」段）；旧引用 grep 0 命中 |
| T9 归档改名＋注记＋git mv 命令贴 Doctor（X1/X2） | staged | git mv 命令块已构造；README/迭代记录注记已落；执行待 Doctor 终端 |
| T10 X1 旧 PRD 处置提请（cancelled 归 Doctor） | 提请 | `2026-10-13_仓位提示器日更链补建_PRD.md` 请 Doctor 裁 cancelled |
| T11 未参与实施的 subagent 独立审查（Step 7.5） | done | PASS_WITH_LIMITS（agentId a86e2d85187b3f979 · 六发现已处置 · 背书记录见下） |
| T12 /save 交付与验收交接 | 待 | 本轮结束后 /save |

## §三 · 非交付项

- 不改 V1 回测引擎、候选规则.json 与基线输出（versions/V1_20261013 及 outputs/backtest_20261013 冻结不动）。
- 不动行情库 schema 与既有写库协议；不新增调度实体（并入既有班）。
- 提示器归档＝改名标注，不删除任何数据文件（可逆）。
- 不 commit/push（命令贴 Doctor 终端执行）。
- Risk Daily 其他卡片（TACO/FedWatch/星空探针等）逻辑不动；EAL 公共库、宏观研究体系不动。
- 不含 ETF 实盘验证与任何下单行为；V1 前瞻有效性检验（6 个月计划）不属本任务。
