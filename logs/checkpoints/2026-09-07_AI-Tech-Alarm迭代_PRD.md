---
title: PRD · AI-Tech-Alarm 迭代（VV 请求 · 消费端接通 v2 + 七主题迁移 + EAL 绑定）
tags: [prd, acceptance, 风险日报, 剑酒青丘]
created: 2026-09-07 01:10
updated: 2026-09-07 01:10
status: awaiting_acceptance
task_authorization:
  state: verified
  source_type: 会话裁定
  source_ref: 2026-09-07 会话（VV 投递迭代请求 20260906 之后）
  quote: "Doctor 转发 VV 迭代请求原文：『Alarm 是 CC 在维护，给她发一个迭代请求，发之前只读其 Risk Daily 下的 AI Tech Alarm 标签页』；AskUserQuestion 裁定：『VV 的 AI-Tech-Alarm 迭代请求，批准实施到什么范围？』→ Doctor 选「全量分阶段实施（推荐）」"
  scope: 按 VV 文档第 3-7 节全量实施：消费端接通 v2 版本化数据 + 五轴/象限语义修正 + 七主题迁移 + EAL 固定版本只读引用 + 按 VV 第 7 节验收标准回读；真实产品取舍随时报 Doctor 裁
roles:
  implementers: [CC（本场 2026-09-07）]
  independent_reviewers: [未参与实施的独立 subagent（执行后派）]
acceptance_authority:
  authority: Doctor
  designation_source_ref: 2026-09-07 会话
  designation_quote: "Doctor 为验收方（会话中未另行指定独立验收方）"
  designated_at: 2026-09-07
open_decisions:
  - item: 本地提醒清单是否实施（VV 第 7 节标「如果实施」，属可选）
    blocking: false
    blocks_requirement_ids: []
    decision_owner: Doctor
    status: open
    resolution_source:
    resolved_at:
  - item: yuantu-alarm-weekly 班（周一 09:07 PT）与 v2 层的关系/迁移（ALARM_LAYER 称「v1 所述每周运行不能当作已迁移的证明」）——本次不动班，只消费数据侧；班若写旧 watchlist 会触发 alarm_store 校验漂移，需 Doctor 知悉
    blocking: false
    blocks_requirement_ids: []
    decision_owner: Doctor
    status: open
    resolution_source:
    resolved_at:
type: prd
project: 风险日报
template_version: v1.2
---

# PRD · AI-Tech-Alarm 迭代（VV 请求）

## §一 · 任务目标

Doctor 要解决的问题：美国主要机构用什么框架理解 AI 标的价值、各自预期、何时观察；Alarm 要帮助回答「现在最值得观察什么新信息，它会检验哪条机构假设」。VV 2026-09-06 迭代请求指出核心缺口：Risk Daily 的 AI Tech Alarm 标签页仍是 2026-07-27 静态快照，未消费 watch/ 下已建的 v2 版本化数据（alarm_store.py · current.json → revision r-1e7945f2e9575482a337629f），且五轴/象限图的测量含义需修正、七主题需按迁移表迁移、机构基准需由 EAL 固定版本只读提供。

**Doctor 原始指令**(逐字引用):
> "VV 的 AI-Tech-Alarm 迭代请求，批准实施到什么范围？（这是功能性大改，批准后我立 PRD 并按 VV 第 7 节验收标准执行）" → Doctor 答："全量分阶段实施（推荐）"

（上游委托原文：VV 文档 §0「本请求据此交给 C.C. 维护实现，V.V. 不修改 Risk Daily、Alarm 或 Claude Brain……需要真实产品取舍时由 Doctor 裁定，常规实现由维护方推进。」）

**任务规模估算**:
- 预计涉及文件数: ~9（build_risk_daily.py 改造 · 新渲染器 render_alarm_tab.py · revisions 新 pack 1 个 · 旧快照归档 1 · EAL 研究页引用核验 · PRD 本件 · 变更同步件）
- 预计耗时: 数小时 · 分三阶段（1 消费端接通 → 2 r2 贯通+六项迁移 → 3 EAL 绑定+验收）
- 涉及项目: 风险日报 · Database/行业研究 watch（只读+import 新 revision）· 剑酒青丘 EAL（只读引用）

---

## §二 · 交付标准(Acceptance Criteria · 验收主体＝功能/需求)

### A. 功能需求（用户可感知的行为 / 结果）

- [?] **R1** · 实际消费端接通：重建 dashboard/risk-daily.html 后，AI Tech Alarm 标签页内容来自 `Database/行业研究/watch/current.json` 指向的 revision（r-1e7945f2e9575482a337629f），不再 iframe 07-27 静态快照
  - 验收方法: 跑 build_risk_daily.py 重建 → 提取 risk-daily.html 中 AI 标签页内嵌 HTML → 与 revisions/<id>.json 字段逐项比对（r2 三家 OCF-购买PP&E 数值 19,639/1,746/−8,821 在场；「基准日 2026-07-27」旧文案不在场）；同时旧快照已归档（见 R5）
  - 证据栏: 沙箱实跑 build exit 0（91451 chars）；正则提取 `const AI_HTML=...` JSON 解转义后与 ai_tech_alarm_tab.html **逐字一致**（41593B==41593B · 独立审查员重建复验同值）；成品内 grep：revision id 在场、-8821/19639/1746 在场、「基准日 2026-07-27」0 命中、「杀伤力评分」0 命中
- [?] **R2** · 语义修正落盘：标签页保留七主题 r1-r7、五轴权重滑块、象限图与深棕/琥珀视觉；综合分标注「研究关注优先级（主观）」；U 不再以 1–10 分冒充「未定价比例」，改为显示定价证据状态（无证据=unknown 显式）；P 为主观可能性等级（带日期条件），不呈现为百分比；象限横轴=真实观察窗口/距观察日时间（无窗口=「窗口未定」带，不保留固定「数日内」）
  - 验收方法: 重建后提取内嵌 HTML：grep 旧语义词形（如「杀伤力评分」作分数宣称、「未定价比例」「概率 %」）0 命中；新标注词形在场；quadrant 数据源来自 revision window 字段
  - 证据栏: 成品 grep：「杀伤力评分」0、「未定价比例」0、「基准日 2026-07-27」0；「研究关注优先级（主观）」在场、「窗口未定」带在场（SVG rect）；象限横轴数据源=alarms[].window_days（window 文本 dated 解析，无法解析→未定带）；U 列渲染为 pricing_status 徽标（unknown=未核虚线样式）；P 表头注「等级·非百分比」（AXES 描述「非校准概率、非百分比」）
- [?] **R3** · 每观察项信息列齐：主体/标的、观察指标、下一确认窗口、基准类型与版本、最近事实、当前证据状态、影响的估值假设；r2 的 any/all/sum 三档分开显示（AMZN 单家负显示为「单家命中」，不显示为三家全负）；无合格机构基准时显示「仅有事实观察，暂不能判定预期差」；过期未核窗口显示「窗口已过，待核结果」
  - 验收方法: 提取内嵌 HTML 逐项核对 r2 渲染：三家单季数值、signal_observed（单家）与 threshold_met（全三家）状态区分在场；unknown 六项有显式「未核」样式
  - 证据栏: 内嵌 HTML 含 r2 专表（MSFT/META/AMZN 三家 OCF/现金购买PP&E/cash FCF/公司口径四列）；徽标「any 单家转负：已现（AMZN）」「all 三家转负：未成立」「sum 合计转负：未转负」；「仅有事实观察，暂不能判定预期差」在场；「窗口已过，待核结果」守卫在场（self-test 负向用例断言）；每主题展开卡含观察方式/改变哪条假设/失效证据/信号表/状态五区
- [?] **R4** · EAL 固定版本只读引用：标签页含机构基准入口（跳转/引用 EAL `valuation-b2215c2db8dd75b474ec8d23` 固定版本），不重算机构共识、不改写 EAL 资料；版本号在标签页可见可溯
  - 验收方法: 内嵌 HTML grep 版本号 valuation-b2215c2… 命中；入口文件在盘（EAL_VALUATION_DESK.html / ALARM_EAL_RESEARCH.html）
  - 证据栏: tab 完整版本号 1 处（caveat 数据版本行）+ pin 区「EAL 固定版本只读引用」文案（未带全 id · 审查员 L1 指出，措辞已如实）；入口文件在盘（/sessions/…/剑酒青丘/backtest/ 两 HTML 实测存在且 EAL 文件内版本号命中）；Alarm 侧无任何「共识/surprise」计算逻辑（渲染器只读引用）
- [?] **R5** · 旧资产归档保留：ai_tech_alarm_snapshot.html 移入 风险日报/archived/（可回看），build_risk_daily.py 不再引用其路径；旧 revision 与冻结迁移输入 watchlist 保留在盘（alarm_store 机制）
  - 验收方法: ls archived/ 含快照件；grep build_risk_daily.py 无旧快照路径引用；重建后标签页无 07-27 快照内容
  - 证据栏: archived/ai_tech_alarm_snapshot_20260727.html 在盘（17260B · mtime 08-11）；build_risk_daily.py grep「AI_SNAP」「ai_tech_alarm_snapshot」0 命中（envelope_emit 同 0）；成品标签页无 07-27 内容；alarm_watchlist.jsonl（冻结输入）与 revisions/ 未动
- [?] **R6** · 顶部 AI_RISKS 卡片同源接通：build_risk_daily.py 顶部 AI 卡片与标签页同读 v2 revision（单一真源），不再读 alarm_watchlist.jsonl 旧输入；总览其他模块不受影响
  - 验收方法: 重建后顶部卡片内容与标签页数据同源一致（同 revision）；watchlist 读取引用从 build 脚本移除（grep 0 命中）；总览其他分项（TACO/r7 等）渲染不变
  - 证据栏: build 输出「AI 面板数据：alarm_store v2 · revision r-1e7945f2e9」+「AI面板 7」；build grep「alarm_watchlist.jsonl」读取逻辑 0 命中（仅注释残留说明已降级）；TACO 4/6 分项、原子 6/分子 7/化合物 3 照常渲染；ai_watch_note 带 revision 前缀
- [?] **R7** · r2 最小完整贯通（数据侧新 revision）：经 alarm_store.py import 发布新 pack——r2 同季度现金 FCF any/all/sum、具名机构基准（花旗共识/Epoch 预测原文+日期+公司池）或明确缺口、窗口、来源与计算链；previous_revision_id 链接 r-1e7945f2…
  - 验收方法: alarm_store.py verify 通过；current.json 指向新 revision；回读 revision 字段核 r2 结构与来源
  - 证据栏: 09-05 首版已贯通（r2 evidence_status=verified · signals 3 条含 test{metric_id,op,value}+source_ids+observed_at · metrics 15 条三家 OCF/现金PP&E/cash FCF/company FCF · sources 5 个带 locator）；本场发布新 revision `r-a52c920ddee516a44fe74d13`（previous_revision_id=r-1e7945f2 ✓ · verify PASS · 23 单测 OK · SHA 对拍一致）；机构基准缺口在渲染层显式（「仅有事实观察，暂不能判定预期差」+ EAL 固定版本引用——具名机构观点归 EAL 展示，Alarm 不重算）；any/all/sum 三档徽标在 tab（any 已现 AMZN · all 未成立 · sum 未转负）
- [?] **R8** · 六项迁移（r1/r3-r7）：按 VV §5 迁移表逐项入新语义——每主题观察方式与误读消除（如 r1 单家会计变更≠全 Mag7 下修；r3 性能迭代≠上一代残值失效；r5 规划容量≠投运容量）；有新证据才改状态，历史叙事不升级为已核事实；r7 保留已核触发规则版本与条件
  - 验收方法: revision 内逐主题 signals/notes 结构核（含误读消除表述）；grep 旧误读表述 0 命中；状态字段仅 r6 为 triggered（既有事实），其余按证据水平
  - 证据栏: 七主题 signals/scenario/invalidation 结构在（09-05 已落 5/7 完整误读消除：r2 单家≠三家、r3 性能跃升≠减值、r4 日历年份≠触发时点、r5 规划容量≠投运容量、r7 共振≠因果+不沿用旧日期）；本场补强 2 处（r1 invalidation 加「单家公司会计变更不等于整个 Mag7 同时下修，也不直接等同现金流恶化」、r6 加「对传闻的确认、否认、更正分别改变状态」）→ 新 revision r-a52c920d 落盘；legacy 折叠区保留全部历史原文（含 r6 triggered 旧判、r7 已核触发规则版本与条件）不冒充当前已核；当前 scenario_status 均按 signals 证据水平重算（r2=signal_observed 唯一非 unknown）；渲染器 tab 无旧误读表述（「杀伤力评分/未定价比例/基准日 07-27」grep 0 命中）
- [?] **R9** · 两条置顶提醒改写：台积电 CAPEX（上修≠下游加码坐实、下修≠需求见顶——结合客户/产品/期间解释）；NVIDIA FY2027 Q2 10-Q 旧路标（先核已披露材料再定新状态，不「查词即宣布传闻成立」）
  - 验收方法: 内嵌 HTML 置顶区文本与上述验证边界逐句核对
  - 证据栏: tab header 两条 pin 实读——台积电条含「上修不直接等于下游 AI 加码『坐实』，下修不直接等于需求见顶」+「结合客户/产品/期间解释」；10-Q 条含「先核实已披露材料与实际合同内容，再决定新状态」+「不『只查词』即宣布某传闻成立」；旧「上游先行信号/可证伪路标」宣称文案已替换（grep 0 命中）

### B. 非功能需求（性能/安全/可靠性/兼容性/数据质量）

- [?] **N1** · 班环境可运行性：渲染器在 Gateway 班沙箱可跑——不写死会话名/绝对沙箱路径（风险日报 GOTCHAS ERR-20260804-001/ERR-20260807-001 坑族），路径经环境变量或相对推导；挂载盘文件只读、写临时产物走 /tmp
  - 验收方法: 沙箱实测渲染器跑通 exit 0 + 班环境同款参数形态（env 覆盖）冒烟
  - 证据栏: 本沙箱（会话名 jolly-busy-pasteur）实跑 render_alarm_tab.py exit 0 + --self-test PASS；路径解析=env 优先（ALARM_WATCH_DIR/RISK_DAILY_HOME/ALARM_RATE_OBS_FILE）→ glob 挂载通配（/sessions/*/…）→ Mac 原生，无写死会话名（grep 0 命中）；渲染器只读挂载盘、写产物单文件
- [?] **N2** · 数据质量铁律：unknown 不补 0/中性值/重归一化掩盖；缺失显式标注；企业债 0/5 覆盖显示为「未覆盖」不显示为 0 值；金融数字带来源+asof（v2 数据随源走）
  - 验收方法: 渲染输出 grep 无补 0 证据（对照 revision 字段 unknown 数一致）；利率口径（名义/实际）标注在场
  - 证据栏: self-test 负向用例「unknown 不补 0」（空样本渲染无伪数值）；tab 内「0/5 未覆盖」显式（不填 0）；10Y 标注「CMT 平价 · 指示性买方报价 · 约 15:30 ET 采样 · 非零息即期/远期」（4.78% · 2026-09-04）；U 列 unknown=未核徽标（revision pricing_status 全 unknown 与渲染一致）；数据行带 as_of/revision/sha256

### C. 任务专属（自定义）

- [?] **X1** · 回执 VV：完成后向 `4AI/Shake hands/to VV/` 投递回执——实现范围、资料版本（revision id + EAL valuation 版本）、真实消费端证据（重建+回读）、残余覆盖缺口、回滚点；不做额外审批副本
  - 验收方法: to VV/ 目录回执文件在盘，内容五要素齐全（VV 第 7 节要求）
  - 证据栏: `4AI/Shake hands/to VV/CC致VV-AI-Tech-Alarm迭代回执-20260907.md` 在盘（4103B · 独立审查员实读确认五要素齐全：实现范围/资料版本 r-a52c920d+sha256+valuation 版本/消费端证据逐字一致/残余缺口 5 条/回滚点 3 条）；无额外审批副本

### 分轨签核（v1.3 · 客观轨总 ✓ + 审查员背书 · 总签必须可审计）

> **审查员背书（2026-09-07）**：独立 subagent（agentId a3060e9f6ccceeb01 · 未参与实施）对照 PRD 全量实跑复核——build 重建 exit 0、AI_HTML 提取解转义逐字比对 41593B==41593B、renderer self-test ×2（含 env 覆盖冒烟）、alarm_store verify、23 单测实跑、canonical pack sha256 独立复算、legacy 7/7 与旧 revision 逐字一致（sort_keys 比对）、全量 grep、回执五要素通读。**结论：12 条全 PASS · LIMITS 3 条（L1 证据栏微过已订正 · L2 浏览器交互未实测（回执已自报·建议 Doctor 目验）· L3 台账滞后已回填）**。

- 客观轨总签（覆盖 R1-R9/N1/N2/X1 中机器可判项）：
  - covered_requirement_ids: []
  - authority:
  - designation_source_ref:
  - signed_at:
  - result:
  - reviewer_evidence_ref: 本 PRD「审查员背书」段（agentId a3060e9f6ccceeb01 · 2026-09-07）
- 原则轨（结论/裁定类）共 0 条：

---

## §2.5 · 执行与交付清单（过程项 · 不参与功能交付关闭判定）

| task_id | 过程项 | task_status | 证据 |
|---|---|---|---|
| T1 | PRD 落盘 brain/logs/checkpoints/2026-09-07_AI-Tech-Alarm迭代_PRD.md | done | 本文件 |
| T2 | 渲染器 render_alarm_tab.py 建于 风险日报/ | done | 在盘（self-test PASS · env 冒烟 PASS） |
| T3 | build_risk_daily.py AI 段改造（标签页+顶部卡片接渲染器） | done | build 实跑 exit 0 · AI_HTML 逐字一致 |
| T4 | 旧快照归档 archived/ + grep 旧路径 0 命中 | done | archived/ai_tech_alarm_snapshot_20260727.html |
| T5 | r2 新 pack import 经 alarm_store.py（previous_revision_id 链接）+ verify 通过 | done | r-a52c920d verified=true · 23 单测 OK |
| T6 | 六项迁移落新 pack | done | r1/r6 补强 2 处 · 5/7 已于 09-05 落 |
| T7 | 重建 risk-daily.html + 提取回读验证（VV 第 7 节六条验收） | done | 逐字一致 41593B · grep 清单全绿 |
| T8 | to VV 回执落 4AI/Shake hands/to VV/ | done | CC致VV-AI-Tech-Alarm迭代回执-20260907.md |
| T9 | git 命令贴 Doctor（风险日报仓 · brain 仓） | done | 命令块已贴（见会话） |
| T10 | /save + PRD status → awaiting_acceptance + 独立审查 | done | 独立审查 12 PASS · 背书落分轨签核 |

---

## §三 · 非交付项(范围排除)

- 不包含: 重构风险总览——总览其他模块（TACO/r7 等）保持原职责，仅 AI 卡片/标签页数据源切换并验证兼容影响（VV §3 末段）
- 不包含: 本地提醒清单、新增通知渠道、对外发送、调度安装或变更（VV §7.4 明示范围外；提醒清单列为 open_decisions 待 Doctor 裁）
- 不包含: 新建取数路线——企业债/利率数据采集沿用既有 EAL 全量采集（usdjpy-15），缺个券=缺覆盖不报失败（VV §6）
- 不包含: 在 Alarm 重算「机构共识」/surprise、反向改写 EAL 原始资料；EAL 字段扩展需求走 to VV 通道（VV §6）
- 不包含: 修改 alarm_store.py 本体（仅用其 import/export/verify 流程）；不把 schema v3 版本号当目标（VV §6 末段）
- 不包含: Gateway 端 artifact 配置/调度改动（更新仍由 refresh-risk-daily 班完成）
- 不包含: 对旧金融断言（r6 $105B/$250B 传闻等）作本轮真假裁决——只核验证方式与表达边界（VV §5 末段）

---

## §四 · 状态（current_status + 变更历史 · 不用多 checkbox）

**状态变更历史**（只追加实际发生的行 · 不得预填）:
| 时间 | 从 → 到 | 谁 | 依据 |
|---|---|---|---|
| 2026-09-07 01:10 | draft → in_progress | CC | Doctor 批「全量分阶段实施（推荐）」（2026-09-07 AskUserQuestion）|
| 2026-09-07 阶段 1+2 完成后 | in_progress → awaiting_acceptance | CC | 12 条全填 [?]+证据 · 独立审查 12 PASS（agentId a3060e9f6ccceeb01 · 背书落分轨签核）· 交 Doctor 落签 |

**关闭路径**(回顾铁律):
- ✓ 关闭: 每个 requirement 逐项 `[✓]`，或被字段齐全的合法总签明确覆盖
- ✓ Doctor 取消关闭
- ✗ 不允许实施者自动关闭

---

## §五 · 变更记录

- 2026-09-07 01:10 CC: 立 PRD · 12 条交付标准（R1-R9/N1/N2/X1）· task_authorization 已记录（AskUserQuestion 裁定）
- 2026-09-07 阶段 1 完成：R1/R2/R3/R4/R5/R6/R9/N1/N2 填 [?]+证据（渲染器 render_alarm_tab.py 新建 · build_risk_daily.py/envelope_emit.py 改造 · 旧快照归档 · 消费端逐字一致回读）
- 2026-09-07 阶段 2 完成：新 revision `r-a52c920ddee516a44fe74d13` 发布（r1/r6 误读消除补强 2 处 · previous_revision_id 链接 · verify PASS · 23 单测 OK）· R7/R8 填 [?]+证据
