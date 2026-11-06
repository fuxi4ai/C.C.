---
title: 风险日报 · GOTCHAS（已知坑）
tags: [风险日报, gotchas]
created: 2026-07-27
updated: 2026-11-05
status: active
type: resource
project: 风险日报
---

# 风险日报 · GOTCHAS（已知坑）

> 排查超过一轮的问题都记这里。CC 遇错解决后立即回写。

## 格式

```
## [ERR-YYYYMMDD-NNN] 简要描述
**状态**: 🔄 待修复/已修待验 / ⚠️ 已知风险；✅ 已修复（**仅由 Doctor 或指定独立验收方落，实施者不得自标**）（⏳ 旧状态词 2026-08-26 迁移专场退役）
**优先级**: 🔴 高 / 🟡 中 / 🟢 低
**触发场景** / **错误信息** / **解决方案** / **预防措施**
```

---

## [ERR-20260727-001] VoteHub Polling API 返回裸数组，非文档写的 {"polls":[...]}
**状态**: ✅ 已解决
**优先级**: 🟡 中（动 VoteHub / 类似 beta API 必踩）
**触发场景**: `fetch_taco_components.py` 用 VoteHub 取特朗普支持率（`GET api.votehub.com/polls?poll_type=approval&subject=donald-trump`）落 TACO 代理的净支持率分项。终端 --fetch 后 FRED 两项进库、**APPROVAL_NET 没进**。
**错误信息**: 脚本 `json.loads(body).get("polls", [])` —— VoteHub 官方文档示例写响应是 `{"polls":[...]}`，**实际返回的是裸数组 `[...]`**（beta 口径已变）。对 list 调 `.get` 抛 `AttributeError` → 被外层 try 吞 → 该 series 0 行、静默缺失。
**解决方案**: 兼容两种形状——`_d=json.loads(body); polls = _d if isinstance(_d, list) else _d.get("polls", [])`。poll 对象结构确认：`end_date` + `answers:[{"choice":"Approve","pct":..},{"choice":"Disapprove","pct":..}]`（pct 为 float）；按 end_date 聚合日度净支持率(Approve−Disapprove)。
**预防措施**: ①第三方 beta API 别信文档的响应形状，先 `isinstance` 兜底 list/dict 两种；②脚本里单 series 取数失败**不该静默吞**——外层 try 打印「✗ 原因」已能暴露（本次 Doctor 未贴该行输出、靠 --check 见缺行才发现）；③排障口诀同 [[经验库]] EXP-20260725-001-P：先取一小片真实响应看结构，别照文档拍。
**旁证**: VoteHub `from_date` 语义＝end_date≥该日；2026-07-15 起返回 `[]`（民调周级滞后，最新 approval end_date 到 6 月底/7 月初），非 bug。

---

## [ERR-20260727-002] 沙箱测代理/白名单连通性会误判：3128 全 000 是假象
**状态**: ✅ 已解决（认知纠偏）
**优先级**: 🟢 低（但每次核白名单必踩）
**触发场景**: 白名单开通后想在沙箱验 VoteHub/FRED 是否放行，用 `curl -x http://localhost:3128 ...` 测 → 两源全 HTTP 000。
**错误信息**: 000 被误读为「白名单没生效/源不可达」。
**解决方案**: `localhost:3128` 是**定时任务侧**的代理，**本会话沙箱没挂这个代理** → 走 3128 必然 000（连不上代理本身），与白名单无关。改**直连**（不带 -x）测：VoteHub 200、FRED 301，可达。
**预防措施**: ① 沙箱直连 ≠ 定时任务代理路径——白名单管的是**代理路径**，沙箱直连测不到它，要验白名单只能看**下一班定时任务的 fetch 步**或 **Doctor 终端 `--probe`**（公网直连）；② 沙箱核「数据能不能取到」用直连即可，核「白名单/代理放行」得换环境；③ 别把 3128 的 000 当白名单失败的证据。

---

## [ERR-20260727-003] 石刻浮层可见性偶合 danger 类：非 danger 卡的浮层被 overflow:hidden 裁切
**状态**: ✅ 已解决
**优先级**: 🟡 中（新增任何石刻浮层必踩）
**触发场景**: 上线「退」石刻（首个冷色浮层·亮在 geo near/taco none 等**非 danger** 卡上），Doctor 肉眼见「退字被裁了」。
**错误信息**: 无报错——纯视觉裁切。`.scard{overflow:hidden}`，仅 `.scard.danger{overflow:visible}` 放开；而危(fired)/烈(红杀伤)/兆(必伴上游 hd)历来**恰好都只长在 danger 卡上**，偶合掩盖了缺陷；「退」首个亮在普通卡上即暴露（半出卡外的部分被裁）。
**解决方案**: 加 `.scard.badged{overflow:visible;z-index:4}`（styleguide §04 本就有此款）；卡片模板改为**有任何浮层即挂 badged 类**（`const bz=dzb(...)` 先算再判 `${bz?' badged':''}`）。
**预防措施**: ① 新增视觉元素时别只在「历史同类出现过的卡型」上验——**在最普通的卡上验一次**；② 「某特性恰好总与另一特性同现」的隐性偶合是潜伏 bug 温床，解耦时（本例：badge 与 danger 解耦）必须重查依赖链；③ styleguide 有 `.badged` 先例说明原作者早知此坑——落地时漏抄了，抄范式要抄全。

## [ERR-20260727-004] `north_flow` 表存的是**成交额**不是净流入——当资金流向用必错
**状态**: ✅ 已解决（认知纠偏）
**优先级**: 🟡 中（凡想做「北向资金剂量/流向」必踩）
**触发场景**: 化合物回测 C1 想给「抽水烈度」加北向净流出剂量分项，查 `market_data.north_flow`（833 行·2023-01→2026-07）。
**错误信息**: 无报错——数值全是大正数（如 2026-07-24：north_money 283837 / hgt 136054 / sgt 147782，且 hgt+sgt≈north_money）。若当净买入读，会得出「每天都在大幅净流入」的荒谬结论。
**解决方案**: 该表实为**沪深股通成交额**（买+卖）。**2024-08-18 起交易所已停止披露每日净买入**，只留成交额与季度持股——**净流入序列在库内不存在、也无法从该表推导**。北向剂量/流向类因子一律**不可做**（R1 里「北向低=流出」的旧结论亦建立在 2024-08 前的口径上，只在那段窗口有效）。
**预防措施**: ① 见到「金额型」字段先做**量纲/符号体检**（全正、无负值、分项之和≈总量 → 十有八九是成交额而非净额）；② 政策性口径变更（停披）比字段更名更隐蔽，用之前先查披露制度是否仍在；③ 要做真北向流向需另找源（季度持股变动/托管数据），非本库范围。

## [ERR-20260728-001] TACO 净支持率分项「伪月变动」：源停更时 1 月变动退化为 6 天变动、且停更满 30 天时 z 自跳
**状态**: ✅ 已解决（2026-07-28 审计修复）
**优先级**: 🔴 高
**触发场景**: VoteHub 民调停在 06-29（源侧断供），`_chg1m_at` 取 cur=06-29/old=06-23 的 6 天变动冒充「1 月变动」入 z（+0.94·pain 第二大正贡献）；07-29 起 cut 越过 06-29 → chg 恒 0 → z 跳 −0.35 → pain 零新闻自跌 ~3 分。
**解决方案**: `_TACO_COMPS` 加频率感知 `max_age`（日频10/汽油12/周频21/月频45/民调21 日历日），超龄分项剔出均值并在 `pain_from` 标 `剔陈旧:名N d`；同轮把 `_prep` 采样从「固定5行步长」改「按日历每7天」（旧法周频=每5周仅26点、月频=每5月仅27点，z 分母失真）。修后 07-27 态 pain 56→55（复刻5/6·剔净支持率28d）。
**预防措施**: 任何「变动型」复刻指标必须带每分项 max_age；`_prep` 类标准化窗一律按日历采样非按行采样。

## [ERR-20260728-002] 化合物卡 fail-open：任一输入缺失被静默显示为「未激活」＝缺数据装安全
**状态**: ✅ 已解决（2026-07-28 审计修复）
**优先级**: 🔴 高
**触发场景**: `_frail` 被 ipo 绑架（`_obs3` 要求三值齐备），ipo_daily 取数失败 → 三张化合物卡全部显「○未激活」；且 ipo_daily 是事件表，「近10日无行」无法区分「无新股」与「表停更」。
**解决方案**: 逐卡可观测性判定（`_cpd1_obs/_cpd2_obs/_frail_obs`），缺输入显「◌不可判·缺输入(...)·缺数≠安全」（act_key='na' 灰）；卡面加「ipo数据至{日期}」显性化数据截止。
**预防措施**: 一切激活/触发类判定的三值逻辑（激活/未激活/**不可判**）不得塌缩成二值；「缺数≠安全」为 fail-visible 通则（同族：白泽停更品种反拿满持续性、渊图停更无栏级告警——见审查报告 §〇-1）。

## [ERR-20260730-001] 相位判定用沙箱本地日：`date.today()`（美西）让事件时钟慢北京一天
**状态**: ✅ 已解决（2026-07-30 业务时钟换装）
**优先级**: 🔴 高（一切日历/窗口/年龄判定通用）
**触发场景**: 晨检议息卡：北京 07-30 已入结清日，卡片仍显「事前窗」。相位、缴税窗、ipo 截止、陈旧龄、快照 key 全用沙箱本地 `date.today()/datetime.now()`（美西尚在 07-29）。
**错误信息**: 无报错——页面完全正常，只有相位语义错一天（最难察觉的一类）。
**解决方案**: 新增 `bj_now()=datetime.utcnow()+timedelta(hours=8)` / `BJ_TODAY`，8 处调用点换装；generated 戳标「（北京）」；grep 验证零残留。**边界（Doctor 裁定）：沙箱系统时区保持美国不动，只在代码内换算业务时间。**
**预防措施**: 含「今天」语义的业务代码一律显式业务时钟，禁裸 `date.today()`；review 用 grep 这两个调用即查。通则版 → 通用教训 **G-X105**。

## [ERR-20260730-002] 抢跑开窗 start−3 撞数据滞后：窗内仅剩 1 个交易日，判型翻错
**状态**: ✅ 已解决（开窗改 start−5）
**优先级**: 🟡 中（事件窗×人肉源组合通用）
**触发场景**: 议息卡「抢跑实况」按事前窗 start−3 日历开窗累计，SPY 手工 fetch 滞后 2 天（us_anchor 至 07-27）→ 窗内只剩 1 个交易日（+0.02%），判型翻成「顺共识」，与实况（恐惧定价）相反。
**解决方案**: 开窗放宽至 start−5（BT-18 事前 5 日窗背书）→ SPY −1.11%/上证 −1.00%，判型归位。
**预防措施**: 开窗宽度 ≥ 窗定义 + 该源最大数据滞后；窄窗×人肉源先查「窗内实测点数」，≤1 点禁判型（fail-visible）。机理详见 决策记录 2026-07-30 议息卡节。

## [ERR-20260730-003] Yahoo chart API 经沙箱 web_fetch 返回空体——us_anchor ×19 人肉工作流断供风险
**状态**: ✅ 已关闭（✅ 2026-10-23 错题本消化 · Doctor 问答板裁『直接✅关』· 未参与实施的审核 subagent 落签 · 证据：G-X128 反爬演进定性 + us_anchor 19/19 至 20261022 · _health stale_days=0）
**优先级**: 🟡 中（若持续则升 🔴——us_anchor/TACO SPY 腿断供）
**触发场景**: 拉 07-29 美股分时：`query1/query2.finance.yahoo.com/v8/finance/chart/` 经沙箱 web_fetch 连续 6 次返回空体（带/不带 %5E、含 period 参数均试）；Chrome 桥未连接。同端点 Doctor 终端 `curl -A "Mozilla/5.0" --compressed` 一次成功。
**解决方案**: 当次走「构造 curl 命令交 Doctor 终端」（AI4ME/us_intraday_20260729/ 15 文件）。**根因未定**：可能是 Yahoo 对无 UA/无 cookie 抓取收紧，也可能是 web_fetch 对 application/json 的处理变化。
**预防措施**: ① 九儿 us_anchor ×19 与 intl_index_daily 同源——**下一班跑前先单只试拉**，空体即切终端 curl 批量方案（命令模板见本条触发场景）；② 情报源台账「手工 web_fetch ×19」行的失败表现补「空体≠无数据，先当通道错」（fail-visible/G-X104 同族：静默空与真空同貌）。

## [ERR-20261103-001] AI Tech Alarm 优先级口径分裂：表格 JS score() 分母固定 100 vs 渲染器 _priority 分母按有效轴
**状态**: ✅ 已闭（2026-11-05 · 未参与实施的审核者独立核验 PASS_WITH_LIMITS）← 原：🔄 已修待验（2026-11-05 JS 改读 priority 字段）
**优先级**: 🟡 中（同页表格分数与主面板「AI估值泡沫」分子不一致）
**触发场景**: 2026-11-03 为「最终风险值」头卡选口径时显形——头卡须与主面板同源，实测 JS 表格 `score()`（分母固定 100）与 Python `_priority`（分母＝有效轴权重和，U 无定价证据时 U 权重不计入分母）对同一数据产出 **63.0 vs 78.8**（r4 例）。表格显示 63.0、主面板 ai_top 吃 78.8，同页两数打架。
**错误信息**: 无报错——两种实现各自合法、注释语义相同（「U 无定价证据时贡献 0」），分母口径未写进注释。
**解决方案**: 本轮头卡直接读 `build_view_data` 的 `priority` 字段（Python 口径·与主面板同源），不在 JS 侧重算。两口径统一（改 JS score() 分母或改 _priority）属功能性改动，待 Doctor 裁。
**预防措施**: 派生字段（priority）只在一处算（渲染器 Python 侧），前端展示一律读字段、禁各写一份公式；同语义双实现必须共用一个分母定义并写进注释。
**修复记录（2026-11-05 · GAI 错题本积压场 · Doctor 批「风险日报口径统一」· 已修待验）**: `render_alarm_tab.py` 内嵌 JS `score(d)` 删去自带加权公式，改为只读渲染器 `priority` 字段（字段缺失→NaN 显式可见）；`--self-test` 加第 ⑤ 项（score() 须含 `d.priority`、不得含 `W.[SCUPV]`）。备份 `render_alarm_tab.py.bak_2026-11-05_priossot`。新版 self-test PASS rc=0；第 ⑤ 项判据对旧版判 FAIL。真数据新旧对照：7 条表格分全部上调为主面板同口径（r4 63.0→78.8 · r6 56.5→70.6 · r7 55.0→68.8 · r1 54.0→67.5 · r2 46.0→57.5 · r3 43.0→53.8 · r5 35.0→43.8），排序不变、颜色整体偏暖。`ai_tech_alarm_tab.html` / `dashboard/risk-daily.html` 未手工重建，待次日 `refresh-risk-daily` 班经正式链刷新。✅ 待未参与实施的审核者落签（Doctor 已指定 subagent 验收）。
**✅ 落签（2026-11-05 · 未参与实施的审核者 · 独立核验后自主落签）**: PASS_WITH_LIMITS——① diff 对 `render_alarm_tab.py.bak_2026-11-05_priossot` 仅两处：JS `score(d)` 4 行公式 → 只读 `d.priority`（非有限数 → NaN）、`_self_test` 加第 ⑤ 项；② `--self-test` rc=0（约 85 s）；⑤ 项判据对备份源文本判 FAIL、对新版 PASS；③ 真 revision 经 `build_view_data` 7 条 alarm 的 `priority` 全为 float（`_priority` 恒返回 float，den≤0 返 0.0），r4 78.8 / r6 70.6 / r7 68.8 / r1 67.5 / r2 57.5 / r3 53.8 / r5 43.8，旧公式复算 63.0/56.5/55.0/54.0/46.0/43.0/35.0，与修复记录一致；④ grep 旧公式 `W.U+(s.P`：Projects 下仅余生成物 `ai_tech_alarm_tab.html`、`dashboard/risk-daily.html`（各 1 处、`d.priority` 0 处）与 EAL 迁移留证旧件；`build_risk_daily.py` 的 `AXES_W` 只作 `ai_axes_w` 数据透传、无重算。限：两生成物未重建（待 refresh-risk-daily 班刷新后复 grep：`d.priority`≥1、旧公式 0）；⑤ 是源码静态断言、非 JS 执行测；self-test PASS 文案未列 ⑤；`color()`/`levelOf()` 阈值沿用旧刻度，表格整体偏暖。

<!-- 在下方追加新条目 -->

## [ERR-20261105-101] AI Tech Alarm 冻结输入被定时班改写：v2 迁移没迁班次，权威 revision 两个月无供料
**状态**: ⚠️ 已知风险（迁移、归档、提案队列已做，未参与实施的审核者判 PASS_WITH_LIMITS · 2026-11-05；下列限制未修，云端 prompt 与 11-09 周班未验证）
**优先级**: 🔴 高
**触发场景**: 2026-11-05 渊图门禁加固提交时发现 `watch/alarm_watchlist.jsonl` 工作树与 HEAD 不同。
**硬证据/最小复现**: HEAD 版 sha `ce6ce1bb…`，规定的冻结 SHA `e47732e8…`；把漂移版放入隔离副本实跑 `alarm_store.py verify` 得 `legacy SHA-256 mismatch`，rc=2。`build_risk_daily.py` 读不了 revision 时 AI 面板缺失（实读；10 月到 11-04 面板是否真的缺失未核）。当前 revision 的 `as_of` 仍为 2026-09-07。
**根因**: 09-05 权威数据迁到 revision，但 `yuantu-alarm-*` 两班仍读写冻结文件；班次判级（watching/warming/triggered）在 revision schema 里没有落点；文件放在渊图仓库、班名带渊图前缀，归属不清；失配没有告警。11-04 恢复时 `46371439` 只提交了备份，恢复本体到 `0cd126ce` 才入库。写入者是这两班属推断，未逐条核对。
**影响面**: r5-grid（10-05）、r7-yencarry（10-19）两段判断只留在 `alarm/legacy/drift_ce6ce1bb_20261103.jsonl`，未外核，不是现行数据，待 Doctor 定是否发版。
**修复**: Doctor 2026-11-05 裁：归风险日报、改名改位置、旧文件归档、判断进提案队列。① 迁到 `Projects/风险日报/alarm/`，旧目录归档 `行业研究/archived/2026-11-05/watch_迁至风险日报/`（只读），原处只留 `MOVED.md`；消费端只认新路径，无回退。② 冻结输入改名 `legacy/alarm_watchlist_frozen_v1.jsonl`，权限 444。③ `alarm_proposals.py`（check/build）与 `proposals/`。④ `test_no_drift.py`。⑤ Cowork 改班名与提示词（`inbox/Cowork请求二-…`）。
**限制**（审核者实跑）: ① 人工复核只靠班次提示词，程序不阻止谁跑 import，revision 也不记 proposal_id。② 阈值和指标由提案自定，恒真阈值只能靠人看摘要。③ `test_no_drift` 只防疏忽，只在周班收尾跑；不查 `.claude` 内容、`MOVED.md` 内容、alarm 根杂文件和 drift 证据；`ALARM_WATCH_DIR` 可指向归档（实搜无人设置）。④ 未被引用的 source 能进 pack，摘要不显示（低）。⑤ `~/.codex/skills/equity-thesis` 副本仍写旧路径，读不到时会报错。⑥ Gateway 同名班正文仍是旧版写文件步骤，须保持停用。⑦ 未验证：云端 prompt、真实班次运行、真实 import、`build_risk_daily` 全链路。
**预防门禁**: `python3 -B alarm/test_no_drift.py`；迁移权威数据时同批迁写者。
**追记（同日 · 发版）**: Doctor 复核摘要后发 `r-7d1bb3b6…`，父版 `r-a52c…`。r5、r7 回源后判 `signal_observed`，不沿用漂移版的 `triggered`；旧记录的 ¥5.34T 对不上，弃用。发版副作用（实读 `narrative_score.py`）：评估绑定 revision，错配即 HARD，普通构建沿用上次有效评估并标陈旧，下次带复核构建自动重绑。遗留：两班第 3 步以 `legacy.status` 为基线，而 legacy 永久冻结，发版也更新不了它，会每周重复报升级，已请 Cowork 改为比当前 revision 的信号状态。EAL 研究页仍钉旧 revision。
**追记（同日）**: Cowork 实测云端 VM 里冻结文件权限为 600，只读检查必然失败，周班会每次误报。已改为只提示；防漂移判据是内容 SHA，权限不随 git 走。本机 444 仅防手滑，云端无此保护。
**来源**: 2026-11-05 Code 标签会话，实跑实读。

## [ERR-20261105-102] test_narrative_score 第 4d 条失败（行情变化拒绝且评估未改）
**状态**: ✅ 已修复（未参与实施的审核者代签 · 2026-11-05 · 判定 PASS_WITH_LIMITS；真实带复核 build 未跑）
**优先级**: 🟡 中
**触发场景**: 2026-11-05 Alarm 迁移回归，`python3 -B test_narrative_score.py` 得 53 PASS / 1 FAIL，失败项 `4d 模型运行中行情变化则拒绝且评估未改`。
**硬证据/最小复现**: HEAD 隔离副本同样失败（实施者与审核者各跑一次），非迁移引入。
**根因**: 真实缺口，不是测试写错。2026-11-04 为修绑定错误，让 `run_model` 把开跑时的 `pricing` 传给 `apply`，`_resolve_pricing` 对显式值原样返回，模型运行期间行情变化不再被发现。
**影响面**: 11-04 起，模型运行期间若行情更新，评估可能基于旧行情落盘；窗口只有一次模型调用（上限 180 秒）。是否实际发生过未查。
**修复**: `run_model` 在模型返回后按 `documents` 重取行情，哈希变化或取数失败即作废；`build_risk_daily.py` 传 `documents=DOCS`，与生成行情同根，不重开 11-04 的错误。真实行情连取两次哈希一致（实跑）。
**限制**: `documents=None` 在沙箱默认根取不到行情时必拒，提示却写「行情已变化」；唯一生产调用已传 `DOCS`，并加 4d-0 锁定。
**预防门禁**: `test_narrative_score.py` 第 4d、4d-0 条。
**来源**: 2026-11-05 Code 标签会话，实跑。

---

## 自 Projects 侧并入（2026-11-05 · Doctor 裁 1A：brain 为 canonical）

> 以下条目逐字来自 `Projects/风险日报/GOTCHAS.md`（并入前 mtime 2026-11-05 12:45:16 UTC · 83 行 · sha256 前 16 位 `90cda27e78f59f0a`），编号体系保留原样；原文件已退为指针。

## [ERR-20260804-001] 沙箱内跑 fetch_taco_components.py 报「找不到 /sessions/Database/.env」
**状态**: ✅ 已解决（本轮绕过）
**优先级**: 🟡 中（每个 scheduled run 都会复发）
**触发场景**: Cowork 沙箱里直接 `python3 scripts/fetch_taco_components.py --fetch`
**错误信息**: `[FATAL] 找不到 /sessions/Database/.env`
**根因**: 脚本用 `DOCS = PROJ.parents[2]` 从 `__file__` 推 `~/Documents`，在 macOS 上成立；沙箱里脚本真实路径是 `/sessions/<session>/mnt/风险日报/scripts/...`，`parents[2]` 推出 `/sessions`，ENV 落到不存在的 `/sessions/Database/.env`。`/sessions` 目录无写权限，无法用 symlink 补。
**解决方案**: 把脚本拷到 /tmp，sed 改写两行绝对路径再跑（不改源文件）：
```bash
mkdir -p /tmp/taco_run && sed \
  -e 's|^PROJ = HERE.parent.*|PROJ = pathlib.Path("/sessions/relaxed-gallant-hawking/mnt/风险日报")|' \
  -e 's|^DOCS = PROJ.parents\[2\].*|DOCS = pathlib.Path("/sessions/relaxed-gallant-hawking/mnt")|' \
  /sessions/relaxed-gallant-hawking/mnt/风险日报/scripts/fetch_taco_components.py > /tmp/taco_run/fetch_taco_components.py
cd /tmp/taco_run && python3 fetch_taco_components.py --fetch
```
注意 `/sessions/<session>/` 前缀随 session 变化，照抄前先 `ls /sessions/` 确认。
**预防措施**: 根治应让脚本支持环境变量覆盖（如 `DOCS_ROOT`/`RISK_DAILY_HOME`），沙箱与 macOS 各传各的；未根治前 scheduled task 每轮按上方绕过跑。

## [SRC-20260807-001] VoteHub approval Feed 断更（信源侧）→ 净支持率换 Civiqs
**状态**: ✅ 已解决（换源 Civiqs·Doctor 2026-08-07 裁定）
**触发场景**: TACO 净支持率分项停在 2026-06-29，陈旧护栏每日剔除，TACO 长期 5/6
**定性证据**（2026-08-07 实核，非凭印象）: ①裸打 API 原始返回最新 end_date=06-29，与库内一致；②**整个 approval Feed 全停**（Supreme Court 06-04、Vance 06-08、Trump/Congress 06-29），不是特朗普单条；③slug 变体无端点迁移；④我方解析 1017 条仅丢 2 条垃圾行；⑤对照组中期竞选民调 `us-representative` 更新至 07-30——**VoteHub 有选择地只喂竞选民调，全国情绪类被放弃**。无停更公告；官网均值产品（2026-01-17 上线）无公开 API 端点。
**选型实测**: RCP 403 反爬 / Cook Political Datawrapper 冻结在 2025-05 / Silver Bulletin 付费墙 / RaceToTheWH Infogram 嵌图不可稳定解析；**Civiqs 唯一全过**：日频·免费·裸 UA 200·数据到当天。
**Civiqs 解析路径**（fetch_taco_components.py `fetch_approval_civiqs()`）: GET `civiqs.com/results/approve_president_trump?annotations=true&results=true&uncertainty=true`（~3.2MB HTML）→ `window.__remixContext` JSON → `state.loaderData["routes/_app.results_.$question"].related[]` 按 `job_description.name=="approve_president_trump_2025"` 定位当任期 run（**不硬编码下标**）→ `line_chart_data` 元素 `{"key":"Approve"/"Disapprove","values":[{date:epoch_ms,value:小数}]}` → net=(ap−dis)×100。主结果对象是**一任期** run（2017–2021），当任期在 related 里——别抓错。
**坑**: ①civiqs 偶发 502 Bad Gateway → `_get_retry` 指数退避；②口径断层：VoteHub 多民调均值末值 −18 vs Civiqs 单机构 RV 同日约 −22，**两序列不拼接**，z-score 各用各的历史；③build 侧双源回退 `_series_taco("APPROVAL_NET_CIVIQS") or _series_taco("APPROVAL_NET")`，护栏随日频源收紧 21→10 天。
**预防措施**: fetch 侧 fail-visible 校验（n<400 或最新日期 >7 天即抛错）；结构改版即断即暴露，不静默写可疑数。完整选型备忘：`docs/2026-08-07_净支持率替代源调研.md`。

## [ERR-20260807-001] 取数路径写死沙箱会话名 → 每日 r7 判读恒「不可用」
**状态**: ✅ 已解决（已根治，非绕过）
**优先级**: 🔴 高（每日 `refresh-risk-daily` 的 r7 数据判读持续失效）
**触发场景**: 每日班跑 `build_risk_daily.py` → `import r7_yen_watch` → `load_bars()`；或任何新 Cowork 会话里直接跑 `r7_yen_watch.py` / `calibrate_usdjpy.py`
**错误信息**: `r7 判读不可用: 找不到 attribution.db（候选路径：[..., '/sessions/beautiful-busy-mendel/mnt/...']）`（`data/risk_snapshot.json` 留证）
**根因**: 两脚本 `CANDIDATES` 把沙箱路径**写死成单个旧会话名** `beautiful-busy-mendel`。沙箱会话名每次随机（如 `nice-exciting-curie`），Mac 原生路径在 Linux 沙箱不存在，写死字符串必然跨会话失效。与 ERR-20260804-001 同类（沙箱路径随会话漂移），那条是 `parents[N]` 推导错、这条是写死字符串错。
**解决方案**: `CANDIDATES` 删掉写死条，改 glob 通配当前挂载并取最新（已改 `r7_yen_watch.py` / `calibrate_usdjpy.py`，沙箱实测 `load_bars` 成功、r7 判读恢复）：
```python
import glob
CANDIDATES = [
    "/Users/lunarabbit/Documents/Database/宏观研究体系/EAL/attribution.db",   # Mac 原生
] + sorted(glob.glob("/sessions/*/mnt/Documents/Database/宏观研究体系/EAL/attribution.db"),
           key=os.path.getmtime, reverse=True)   # 会话名随机→glob 通配；多个残留取最新
```
**预防措施**: 沙箱取库路径**一律 glob 通配或 env 覆盖，绝不写死 `/sessions/<具体会话名>/`**——写死会话名是定时任务跨会话的定时炸弹。注意此 glob 依赖「定时任务持续挂载 `~/Documents`」；若日后改挂子目录，需把 glob 放宽或加 env 兜底。

## [NOTE-20260808-001] 本仓无 Git 远端：git push 恒报 "No configured push destination"——设计如此·本地仓，离机备份走 fuxi-station
**类型**: 📝 配置事实（非错误） **优先级**: 🟡 中
**现象**: 2026-08-08 晚 commit 256e55a（AI 面板 loader 单一真源化）后 `git push` 报 `fatal: No configured push destination.`——本仓从未配置任何 remote（非上游未设）。
**裁定**: Doctor 2026-08-08——**保持本地仓，不设 GitHub 远端**；离机备份走 **fuxi-station**（首发 tar+scp 至 `F:\Mac_Backup\risk-daily\`，常态化 rsync 待验 fuxi 侧有无 rsync）。
**⚠ 更正留痕**: 本条初稿误写「备份走旧队列④ rsync 镜像」——那条 rsync 实为 brain scheduled-live-mirror（Gateway store→brain），与本仓无关，当时本仓**没有任何**备份机制；Doctor 首次裁定基于该误述，当晚 CC 回源 08-03 日志原文后自纠、Doctor 重裁得上方结论。（凭二手队列摘要下断言、未回源，G-X111 同族。）
**操作含义**: ① CC 给本仓构造命令时 **commit 即止、不附 push**；② fuxi 首发备份未跑成前，所有 commit 是 Mac 本地单点——重要修复（如 256e55a）落仓后提醒 Doctor 跑备份；③ 工作树长期压有每日 build 产物（risk-daily.html / risk_snapshot.json / taco_components.db 等），且 docs/、mech-watch/ 尚未入库——本条随 GOTCHAS.md 首次入库。

## [NOTE-20260913-001] 第三标签「EAL 事件星空」快照冻结+页面按日重锚 → K 线空线 5 天（2026-09-13 修复）
**状态**: ✅ 已修复（2026-09-13 Doctor 目验通过落签 · CC 代记留痕；班首跑待周一晚自然验证）
**优先级**: 🟡 中
**触发场景**: 第三标签 iframe 内嵌 EAL_STARFIELD.html 快照；星空页 `viewForDate` 每次打开锚定「最近已收盘美股交易日」，快照数据自 09-08 构建后冻结 → 09-09 起锚定日无 K 线 → render 守卫 `g.base===null` 暂停零轴与 K 线 → 只剩事件星（「星星在、流线空」）。
**根因**: 快照无重建机制 × 页面按日重锚，两因相乘。与 brain/剑酒青丘/GOTCHAS.md NOTE-20260913-001 同条。
**修复**: 沙箱标准链重建（candles 137→141 · market_as_of 09-11）+ build_risk_daily.py 重跑重推；新建 eal-starfield-rebuild 班（工作日 18:15 PT · 行情守卫：库内 MAX(trade_date)≠最近已收盘交易日则 skip 不重建）。
**预防措施**: 星空快照更新与 EAL 数据链同频；「按日重锚」类快照必须配重建班；重建班前置行情守卫 fail-visible。

## [ERR-20260916-001] check_starfield_freshness.py 沙箱跑恒报 MISSING（HOME 解析错位·伪报）
**状态**: 🔄 已修待验（2026-09-17 Doctor 批「修探针+班步骤加门禁」· 实施已完·✅ 落签归 Doctor）
**优先级**: 🟡 中（每日 refresh-risk-daily 步骤 1.5 都会触发伪报）
**触发场景**: 沙箱跑 `ops/check_starfield_freshness.py`（2026-09-16 班首跑即中招）
**错误信息**: `STARFIELD_FRESH=MISSING starfield 文件不存在 · 报 Doctor`（exit 0 非阻断）
**定性证据**（2026-09-16 实核，非凭印象）: ① 探针 `STAR = pathlib.Path.home() / "Documents/..."` → 沙箱 HOME=`/sessions/cool-bold-wright`（`~/Documents` 不存在，挂载在 `/sessions/*/mnt/Documents`）→ 恒 MISSING；② Mac 侧文件实存（Glob 实核 `Financial/宏观研究体系/EAL/backtest/EAL_STARFIELD.html`）；③ 以 mnt 正确路径手动复刻探针逻辑实跑：`market_as_of=2026-09-15 · 最近已收盘=2026-09-15 · gap=0 → OK`——真实状态健康，MISSING 系伪报。
**根因**: 与 ERR-20260807-001 同族——沙箱路径假设错位（那条写死会话名、这条依赖 HOME）。探针在 Mac 终端跑正常（HOME=/Users/lunarabbit），在 Cowork 沙箱即伪报。
**建议修法**: r7_yen_watch.py 同款——CANDIDATES 双路径（Mac 原生 + `glob /sessions/*/mnt/Documents/...` 取最新）或支持 env 覆盖。
**预防措施**: 新增「沙箱跑」脚本必须过双路径自检；此探针修复前，每日班 MISSING 输出需先复核 Mac 侧文件存在性再报 Doctor（本轮已按此处理）。
**来源**: 2026-09-16 refresh-risk-daily 班 · CC 实跑实核
**复发追记 2026-09-17**: 班 1.5 步再报 MISSING（沙箱 HOME=`/sessions/compassionate-pensive-gauss`——会话名轮换，不影响伪报机制）。复核实核：`backtest/EAL_STARFIELD.html` 实存（253KB · mtime 09-16 21:03 · 当日 18:15 PT 重建班正常推进 market_as_of 09-15→09-16）；EAL 根级副本同 mtime 同 as_of，无分歧；日历 CSV 实存（218 行）；mnt 正确路径复刻探针逻辑：`market_as_of=2026-09-16 · 最近已收盘=2026-09-16 · gap=0 → OK`。当日首轮红字警报系未按预防措施先复核即原样转发（班 SKILL.md 步骤 1.5 未编码复核门禁），已向 Doctor 撤回。
**修复记录 2026-09-17**（Doctor 批「修探针+班步骤加门禁」）: ① 探针加 `_resolve()` 双路径——Mac 原生 HOME/Documents 优先 + `glob /sessions/*/mnt/Documents` 兜底·多残留取最新，同 r7_yen_watch.py 款；MISSING/NO_CALENDAR 分支改 None 安全。② 沙箱实跑验证：`STARFIELD_FRESH=OK as_of=2026-09-16 最近已收盘=2026-09-16 gap=0` exit 0 · 负向测试（强制 STAR=None）MISSING 分支正常 exit 0 · py_compile 过。③ 班 refresh-risk-daily 步骤 1.5 折入「先复核再报」门禁（Glob/Read 独立通道实核→伪报不红字→真异常才红字）并引用本条，update_scheduled_task 写后回读核验 frontmatter 与全文无误。
**复发追记 2026-11-04**（Doctor 令手动重推 · CC 实跑实核 · 同族第 4 例·跨 model_entry/market_pressure 两件）: 重推带复核 build 恒报 `REVIEW_REJECTED: 模型回包与当前行情输入绑定不符`（非竞态·必现）。三层根因：① `narrative_review.run_model` 调 `apply` 时**漏传 pricing** → apply 内 `_resolve_pricing(None)` 重跑 `market_snapshot()`，其默认 root=`Path.home()/Documents` 在沙箱落空（us/cn sessions 全 null），而 build 侧 `_ai_market=snapshot(documents=DOCS)` 经 `__file__` 解析到真根（us 2026-11-03/cn 2026-11-04）→ 两哈希必不同；② `model_entry.py load_key` 候选路径**写死旧会话名** `/sessions/pensive-gallant-goodall/...`（ERR-20260807-001 同族·写死会话名）且 `stat` 报 EPERM 直接崩（exit 1）→ 首轮 REJECT；③ `narrative_review.py` CLI `prepare` 不透传 model/pricing → 手动包 `binding.model=unavailable` 与模型按 instructions 回填的可核型号 `deepseek-chat` 不符 → 第二轮 REJECT。
**已修（本轮）**: ① narrative_review.py L180 补 `pricing=pricing`（一行·与 build 手动路径 L141 对齐·备份 `.bak_20261104_pricing`）；② 以 env `KG_API_KEY`（挂载 `.env` 本沙箱可读）+ `prepare(model="deepseek-chat", pricing=snapshot(documents=真根))` 绕开，重推完成——`REVIEW_ACCEPTED` · 评估 2026-11-04T12:11:10Z · funding 78 critical=True · artifact risk-daily 已推（综合温度 34 平静 · 快照 generated 04:13 PT）。
**建议修法（未实施·待裁）**: ① model_entry.py 候选路径改 `glob /sessions/*/mnt/Documents/Database/.env` 或仅 env 通道，禁写死会话名；② market_pressure.snapshot 默认 root 加沙箱 glob 兜底（同 check_starfield_freshness._resolve 款）；③ prepare CLI 透传 `--model/--documents`。⚠ **应升格通用教训**（沙箱路径错位族第 4 例·涉三件脚本）。
**来源**: 2026-11-04 凌晨手动重推 · CC 实跑实核 · L180 修复待独立验收（未参与实施的 subagent）
**✅ 独立验收注记 2026-11-04（落签者=未参与实施的审核者 subagent）**: 判定 **PASS**——事实性非功能修复，真实改动面=1 行=被点名目标面，无顺带改动。实跑实读证据：① `diff narrative_review.py.bak_20261104_pricing narrative_review.py` 唯一差异＝L180 `apply(...)` 补传 `pricing=pricing`；② 代码链实读：run_model L161 `prepare(..., pricing=pricing)` 与 L180 `apply(..., pricing=pricing)` 共用同一对象，`_resolve_pricing`（L219-223）对非 None 原样返回、`market_binding` 哈希同源；build 调用处 build_risk_daily.py L126 `_ai_market=snapshot(documents=DOCS)`/L132 传 `_ai_market`，与手动路径 L141 对齐；③ 失效机制实证：以默认 root 实跑 `market_snapshot()`（复刻修复前 `_resolve_pricing(None)` 路径）得 sessions `{us: None, cn: None}`、sha `aa039e80…` ≠ 评估落盘 `1b911e71…` ⇒ 绑定必异的机制成立；④ 落盘评估实读：`data/narrative_assessment.json` as_of_utc=2026-11-04T12:11:10+00:00 · input.model=deepseek-chat · actors.funding score=78 critical=True（basis 4 项）· market_sessions us=2026-11-03/cn=2026-11-04；`narrative_review_log.jsonl` 尾行 apply 阶段·errors 空；⑤ 快照实读：`data/risk_snapshot.json` generated=2026-11-04 20:13（北京）＝04:13 PT · composite_temperature=34 · ai_panel[0] 键清单无 stale_fallback/fallback_note（无回退注记）；⑥ 本追记三根因逐条对盘：①L180 属实 · ②model_entry.py L24 写死 `/sessions/pensive-gallant-goodall/...` 属实 · ③CLI prepare（L312）不透传属实 · market_pressure.snapshot L137 默认 root=`Path.home()/Documents` 属实。未实施项（建议修法①②③）系追记已披露的待裁项，不属本验收范围。
**现况复核 2026-11-05**（Doctor 令登记 · CC 实跑实核 · 非新故障，属上方建议修法①未实施的持续暴露）: ① `model_entry.py` L24 仍写死 `/sessions/pensive-gallant-goodall/mnt/Documents/Database/.env`，该目录本会话 `ls` 不存在；② 本沙箱 HOME=`/sessions/rcw-0149okhq9ft7xtwd3pwd55mg`，L23 候选 `Path.home()/Documents/Database/.env` 不存在，`.env` 实在 `$HOME/mnt/Documents/Database/.env`；③ `env -u KG_API_KEY python3 -c 'import model_entry as m; m.load_key()'` 实跑 → **None**（两候选全落空）→ main 走 L89-91 `sys.exit(3)`，带 `--review-command` 的 build 在此类会话复核必失败，AI 页停在「待模型复核」。**影响面**: 每日 `refresh-risk-daily` 若在非 `pensive-gallant-goodall` 会话且未注 `KG_API_KEY` 即复核失效；11-04 20:02Z 定时复核成功走的是哪条通道**未核**（env 注入或 Mac 原生 HOME）。**预防门禁（建议）**: 班前置一步 `load_key()` 自检，None 即 fail-visible 报出，禁静默降级。**状态**: ✅ 建议修法①已修·独立验收终判 PASS（2026-11-05，验收→复验→升级三注记见下）；建议修法②③仍待裁；⚠ 应升格通用教训（brain/permanent/通用教训.md「工具脚本写死 /sessions/{会话名}/ 路径 = 反模式」条已有通则，本仓三件实例未挂入，升格待 Doctor 质量确认）。
**修复记录 2026-11-05**（Doctor 批「现在修」· 建议修法① · 实施者=CC，不具本变更代签资格）: `model_entry.py load_key()` 候选改为 env `KG_API_KEY` 优先 → Mac 原生 `Path.home()/Documents/Database/.env` → `glob /sessions/*/mnt/Documents/Database/.env`（多残留按 mtime 取最新）；删写死会话名；`is_file()` 包 `try/except OSError` 防他会话残留 stat EPERM 崩。备份 `model_entry.py.bak_2026-11-05_keypath`。真实改动面＝load_key 内候选路径段（diff 两处：删 5 行增 12 行；验收后补：`read_text` 亦包 `try/except OSError`→跳过该候选，堵局限 (b)；同日更正原「4 行→11 行」计数笔误），未动 API 调用/回包逻辑。自验（实跑）: ① AST OK · 文件内 `pensive-gallant-goodall` 计数 0；② `env -u KG_API_KEY` → FOUND（len 35）；③ `KG_API_KEY=dummy` → 返回 env 值（env 优先）；④ `HOME=/nonexistent` → 仍 FOUND（glob 兜底）；⑤ 负向：HOME 错位 + glob 置空 → None，`main()` 打印「KG_API_KEY 不可得」exit 3（fail-visible 保留）。未调用 DeepSeek。建议修法②③（market_pressure 根目录兜底、prepare CLI 透传）**未实施**，仍待裁。待独立验收（未参与实施的 subagent）。
**✅ 独立验收注记 2026-11-05（落签者=未参与实施的审核者 subagent）**: 判定 **PASS_WITH_LIMITS**——真实改动面仅限 `load_key()` 候选路径段＋`is_file` 防崩，API 调用/回包/exit 码逻辑字节未动，四向实跑全符预期、fail-visible 保留。实跑实读证据：① `diff model_entry.py.bak_2026-11-05_keypath model_entry.py` 仅两处 hunk（L22-25→L22-28 候选路径、L27→L30-34 `is_file` try/except），其余 144→151 行无差异；main 中 `load_key()`/exit 3（现 L95-98）位于 `urllib.request.Request`/`urlopen`（L104/L113）之前；② `env -u KG_API_KEY` → 取到（len 35，经 glob 命中本会话 `/sessions/rcw-…/mnt/Documents/Database/.env`；本沙箱 `Path.home()/Documents/Database/.env` 不存在）；`KG_API_KEY=xxx` → 返回 env 值（len 3，env 优先）；`env -u KG_API_KEY HOME=/nonexistent` → 仍取到（len 35）；③ 负向：HOME=/nonexistent＋monkeypatch `glob.glob→[]` → `load_key()=None`；同条件 runpy 以 `__main__` 跑真脚本、stdin `{}`、`urlopen` 替换为抛 `NETWORK_REACHED` 桩 → stderr「KG_API_KEY 不可得」·进程 rc=3、桩未触发（未发任何网络请求）；坏 JSON stdin → rc=2；④ AST 可解析；文件内 `pensive-gallant-goodall` 计数 0（备份内 1）；`/sessions/` 下实列无该目录；项目内非 .bak 的 .py 无其他写死会话名；⑤ 记录对盘：ERR-20260807-001 / ERR-20260916-001 均为 GOTCHAS 实有标题（L31/L62）；现况复核所引备份 L23/L24/L89-91 与备份文件实读一致；通用教训实例追加所列 `r7_yen_watch.py`/`calibrate_usdjpy.py`（mech-watch/，均已 glob）、`check_starfield_freshness.py`（ops/，已有 `_resolve` glob）、`market_pressure.py`（L137 默认根＝env→`Path.home()/Documents`，未修）、`model_entry.py` 均实存且所述属实。局限：(a) Mac 原生 HOME 通道（/Users/…）与定时班实际注入环境未能在本 VM 实跑，只验了沙箱通道；(b) `is_file()` 之后的 `read_text()` 未包 try，若某 glob 候选可 stat 不可读且排序在前的候选均无 KG_API_KEY，仍会抛 PermissionError（exit 1，非 3）——排序 key 已把不可读者沉底，实际触发面窄；(c) 修复记录自述「diff 4 行→11 行」与实测不符（实为 5 行→12 行、两处 hunk），属计数笔误不影响结论；(d) 备份是否等于修改前原件无版本库可对（未跑 git），以备份内容与 11-04 验收注记所述 L24 写死一致为旁证；(e) 通用教训实例追加称「统一修法＝env→Mac 原生 HOME→glob」，与同条母规则「正确姿势＝向上找 Documents 祖先、别用 Path.home()」口径不一，建议 Doctor 裁定是否统一表述。
**复验注记 2026-11-05（同一审核者）**: (b) **闭**——`diff /tmp/model_entry.pre_b.py model_entry.py` 唯一差异＝L35 `read_text` 包 `try/except OSError: continue`（L35-39），AST OK、`pensive-gallant-goodall` 计数 0；实跑：① 正常 `env -u KG_API_KEY` → 取到（len 35）；② 构造 chmod 000 的 `a.env`（mtime 2030）＋可读 `b.env`，monkeypatch `glob.glob` 与 `os.access→True` 使不可读者排第一 → 读序 `[a.env, b.env]`、返回 b 的值（跳过成功），同条件修前副本 → 抛 PermissionError；③ 全部候选不可读（HOME=/nonexistent＋glob 仅 a.env），runpy 以 `__main__` 跑真脚本、stdin `{}`、`urlopen` 换抛错桩 → 「KG_API_KEY 不可得」rc=**3** 且桩未触发，修前副本同条件 rc=1（PermissionError）；文件仍可执行（-rwx，run_model 式 subprocess 直调 rc=2 于坏 JSON），未调 DeepSeek。(c) **闭**——修复记录已改「两处：删 5 行增 12 行」并注明 (b) 补丁与笔误更正；附注：含 (b) 后相对 `.bak_2026-11-05_keypath` 的累计差异为删 6 行增 17 行（151→155 行），记录按「初修＋补丁」分述，无矛盾。(e) **闭**——通用教训 L297 已改为「本仓实际采用的修法……与上文『向上找 Documents 祖先』是两种可行姿势，此处仅记实例、不改通则」，全文「统一修法」计数 0。GOTCHAS 其余行与验收前副本逐行一致。**总结论维持 PASS_WITH_LIMITS**（不升 PASS）：所余 (a) Mac 原生 HOME 通道/定时班实际环境未在本 VM 实跑——该候选行与修前同一行未改，风险低但属未实测通道，而定时班调用即走 `~/Documents/...` 路径；(d) 备份原件出处无版本库可对。两项均为环境限制，非本变更缺陷；如 Doctor 在 Mac 终端补跑一次 `env -u KG_API_KEY python3 -c 'import model_entry as m; print(bool(m.load_key()))'` 得 True，即可升 PASS。
**升级注记 2026-11-05（同一审核者）**: 判定 **PASS_WITH_LIMITS → PASS**。依据：(a) **闭**——证据来源＝Doctor 在 Mac 终端（主机 yuetudeMacBook-Air）实跑 `cd ~/Documents/Claude/Projects/风险日报 && env -u KG_API_KEY python3 -c 'import model_entry as m; print(bool(m.load_key()))'` 回显 `True`，由 Doctor 贴回会话转交，**非审核者实跑**、审核者未见原始终端；Mac 上无 `/sessions/*` 挂载且已 unset env，该 True 只能来自 `Path.home()/Documents/Database/.env` 通道，即 Mac 原生通道已实测可用。(d) **未闭、降为不阻断附注**——Doctor 已提交 commit `edded54`（审核者未跑 git，仅读 `.git/logs/HEAD` 见 `edded54197d4… commit: fix(model_entry): 密钥路…` 一行，确认提交存在），但该提交记录的是修后状态，不能回溯证明 `.bak_2026-11-05_keypath` 等于修前原件；不阻断理由：现文件全部行为（取 key 四向、跳过不可读、exit 3 先于网络、API/回包逻辑实读）均直接对现文件实测，不依赖备份真伪，且备份 mtime（11-04 09:57）与 11-04 验收注记所述 L24 写死一致。升级时复核：`model_entry.py` md5 前缀 `8f07b0f583a0`、mode -rwx、mtime 12:37:05，与复验时同一文件未再变动。今后改动面核对以 git 为准。
