---
title: 风险日报 · GOTCHAS（已知坑）
tags: [风险日报, gotchas]
created: 2026-07-27
updated: 2026-07-27
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
