---
title: 风险日报 · GOTCHAS（已知坑）
tags: [风险日报, gotchas]
created: 2026-07-27
updated: 2026-11-17
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
**状态**: ✅ 已修复（未参与实施的审核者代签 · 2026-11-10 · PASS_WITH_LIMITS；依据 11-09 周班自然运行的盘上实据，简报原文未读，限制见文末「追记 2026-11-10」）
**沿革**: ⏳ 待 2026-11-09 周班自然验（修复已全部落地：迁移/归档/提案队列 11-05 · 两班判级基线改 revision + 云端 prompt 改引镜像 11-07；验后由未参与实施的审核者落 ✅）〔2026-11-08 至 11-10 的状态原文〕← ⚠️ 已知风险（迁移、归档、提案队列已做，未参与实施的审核者判 PASS_WITH_LIMITS · 2026-11-05；下列限制未修，云端 prompt 与 11-09 周班未验证）
**预防门禁（2026-11-07 Doctor 批 P1 · 由审核者限制 ①③ 提炼）**: ① `alarm_store.py import` 是唯一发版入口——发版前须有对应 `proposals/pending/*.json` 经 `alarm_proposals.py check` 通过并由 Doctor 复核，不得直接 import 手写 revision（程序级 proposal_id 关联属功能性改动，另裁）；② 任何改动 alarm/ 的会话收尾必跑 `python3 -B alarm/test_no_drift.py`，不只在周班跑。
**优先级**: 🔴 高
**触发场景**: 2026-11-05 渊图门禁加固提交时发现 `watch/alarm_watchlist.jsonl` 工作树与 HEAD 不同。
**硬证据/最小复现**: HEAD 版 sha `ce6ce1bb…`，规定的冻结 SHA `e47732e8…`；把漂移版放入隔离副本实跑 `alarm_store.py verify` 得 `legacy SHA-256 mismatch`，rc=2。`build_risk_daily.py` 读不了 revision 时 AI 面板缺失（实读；10 月到 11-04 面板是否真的缺失未核）。当前 revision 的 `as_of` 仍为 2026-09-07。
**根因**: 09-05 权威数据迁到 revision，但 `yuantu-alarm-*` 两班仍读写冻结文件；班次判级（watching/warming/triggered）在 revision schema 里没有落点；文件放在渊图仓库、班名带渊图前缀，归属不清；失配没有告警。11-04 恢复时 `46371439` 只提交了备份，恢复本体到 `0cd126ce` 才入库。写入者是这两班属推断，未逐条核对。
**影响面**: r5-grid（10-05）、r7-yencarry（10-19）两段判断只留在 `alarm/legacy/drift_ce6ce1bb_20261103.jsonl`，未外核，不是现行数据，待 Doctor 定是否发版。
**修复**: Doctor 2026-11-05 裁：归风险日报、改名改位置、旧文件归档、判断进提案队列。① 迁到 `Projects/Financial/风险日报/alarm/`，旧目录归档 `行业研究/archived/2026-11-05/watch_迁至风险日报/`（只读），原处只留 `MOVED.md`；消费端只认新路径，无回退。② 冻结输入改名 `legacy/alarm_watchlist_frozen_v1.jsonl`，权限 444。③ `alarm_proposals.py`（check/build）与 `proposals/`。④ `test_no_drift.py`。⑤ Cowork 改班名与提示词（`inbox/Cowork请求二-…`）。
**限制**（审核者实跑）: ① 人工复核只靠班次提示词，程序不阻止谁跑 import，revision 也不记 proposal_id。② 阈值和指标由提案自定，恒真阈值只能靠人看摘要。③ `test_no_drift` 只防疏忽，只在周班收尾跑；不查 `.claude` 内容、`MOVED.md` 内容、alarm 根杂文件和 drift 证据；`ALARM_WATCH_DIR` 可指向归档（实搜无人设置）。④ 未被引用的 source 能进 pack，摘要不显示（低）。⑤ `~/.codex/skills/equity-thesis` 副本仍写旧路径，读不到时会报错。⑥ Gateway 同名班正文仍是旧版写文件步骤，须保持停用。⑦ 未验证：云端 prompt、真实班次运行、真实 import、`build_risk_daily` 全链路。
**预防门禁**: `python3 -B alarm/test_no_drift.py`；迁移权威数据时同批迁写者。
**追记（同日 · 发版）**: Doctor 复核摘要后发 `r-7d1bb3b6…`，父版 `r-a52c…`。r5、r7 回源后判 `signal_observed`，不沿用漂移版的 `triggered`；旧记录的 ¥5.34T 对不上，弃用。发版副作用（实读 `narrative_score.py`）：评估绑定 revision，错配即 HARD，普通构建沿用上次有效评估并标陈旧，下次带复核构建自动重绑。遗留：两班第 3 步以 `legacy.status` 为基线，而 legacy 永久冻结，发版也更新不了它，会每周重复报升级，已请 Cowork 改为比当前 revision 的信号状态。EAL 研究页仍钉旧 revision。
**追记（同日）**: Cowork 实测云端 VM 里冻结文件权限为 600，只读检查必然失败，周班会每次误报。已改为只提示；防漂移判据是内容 SHA，权限不随 git 走。本机 444 仅防手滑，云端无此保护。
**来源**: 2026-11-05 Code 标签会话，实跑实读。
**追记 2026-11-07**: Doctor 裁 18A：两班判级基线已改 revision（`live/risk-daily-alarm-weekly` 与 `risk-daily-alarm-earnings-season` 镜像步骤 1/3：基线＝`alarm_store.py export` 当前 revision 的 `scenario_status` 与 `signals[].status`，`legacy.status` 退为历史参考；回执 `brain/inbox/Cowork回执-请求三-判级基线改revision-2026-11-07.md`；云端 prompt 同步归 Doctor），待 11-09 周班自然验。
**追记 2026-11-10（独立核验代签 · 审核者未参与实施 · PASS_WITH_LIMITS）**: 11-09 周班自然运行的盘上实据——① 实读 `alarm/proposals/pending/2026-11-09_r6-shovelseller.json`：`created_by=risk-daily-alarm-weekly`、`created_at_utc=2026-11-09T17:11:28Z`（文件 mtime 11-09 09:11 PST 相符）、`base_revision_id=r-7d1bb3b624d16aa439523951`＝现行 revision；pending 仅此一件，无 r5、r7 提案。② 实跑（只读）`alarm_store.py verify` rc=0、`"verified":true`；`export` 得 r5-grid、r7-yencarry 均 `signal_observed`（`r5-grid-pjm-shortfall`、`r7-yencarry-mof-weekly` 为 met）；`alarm_proposals.py check proposals/pending/*.json` rc=0。③ 实跑 `python3 -B alarm/test_no_drift.py`：7 项 OK、rc=0；冻结输入 SHA 前 16 位 `e47732e86d245746`。④ 班只写了提案：alarm/ 其余文件 mtime 均停在 11-05，`git status -- alarm` 仅该提案一件未跟踪。**限制**：(a) 周班简报原文在云端会话里，本机读不到，「首行报 revision_id」未核，只有提案的 `base_revision_id` 作旁证；`_repair_audit.md` ts=2026-11-07T03:27 行以简报首行为判据，故该行未代签、仍 🔄。(b)「判级按 `signals[].status` 比较」属推断：r6 冻结 `legacy.status` 为 triggered 而班仍相对 revision 的 unknown 出了提案，r5、r7 未重复出；仅一次运行，属负向观察。(c) 云端 prompt 现文读不到（本环境读云端班列表得 0 条，不作任何方向的证据）。(d) earnings-season 班尚无自然运行证据。(e) 提案内容（8-K、10-Q 数值）未外核，是否发版归 Doctor。(f) 原「限制」①–⑥ 未修，仍然有效；⑦ 中「真实 import」之后的周班真实运行已见，其余未核。

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

> 以下条目逐字来自 `Projects/Financial/风险日报/GOTCHAS.md`（并入前 mtime 2026-11-05 12:45:16 UTC · 83 行 · sha256 前 16 位 `90cda27e78f59f0a`），编号体系保留原样；原文件已退为指针。

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
**状态**: ✅ 已修复（2026-11-07 未参与实施的审核者 subagent 独立复验 PASS 代签 · 证据：`ops/check_starfield_freshness.py` L28-37 `_resolve()` Mac 原生 + `/sessions/*/mnt/Documents` glob 双路径在盘；条目内建议修法① model_entry 已于 11-05 独立验收 PASS · 残留 ②③ 已挂问答板）
**沿革**: 🔄 已修待验（2026-09-17 Doctor 批「修探针+班步骤加门禁」· 实施已完·落签归 Doctor）
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
**升级注记 2026-11-05（同一审核者）**: 判定 **PASS_WITH_LIMITS → PASS**。依据：(a) **闭**——证据来源＝Doctor 在 Mac 终端（主机 yuetudeMacBook-Air）实跑 `cd ~/Documents/Claude/Projects/Financial/风险日报 && env -u KG_API_KEY python3 -c 'import model_entry as m; print(bool(m.load_key()))'` 回显 `True`，由 Doctor 贴回会话转交，**非审核者实跑**、审核者未见原始终端；Mac 上无 `/sessions/*` 挂载且已 unset env，该 True 只能来自 `Path.home()/Documents/Database/.env` 通道，即 Mac 原生通道已实测可用。(d) **未闭、降为不阻断附注**——Doctor 已提交 commit `edded54`（审核者未跑 git，仅读 `.git/logs/HEAD` 见 `edded54197d4… commit: fix(model_entry): 密钥路…` 一行，确认提交存在），但该提交记录的是修后状态，不能回溯证明 `.bak_2026-11-05_keypath` 等于修前原件；不阻断理由：现文件全部行为（取 key 四向、跳过不可读、exit 3 先于网络、API/回包逻辑实读）均直接对现文件实测，不依赖备份真伪，且备份 mtime（11-04 09:57）与 11-04 验收注记所述 L24 写死一致。升级时复核：`model_entry.py` md5 前缀 `8f07b0f583a0`、mode -rwx、mtime 12:37:05，与复验时同一文件未再变动。今后改动面核对以 git 为准。
**追记 2026-11-07**: 残留 ②③ 已按 Doctor 裁 17A 实施，已独立复验（两轮 PASS · 见段末）——（**旁证 2026-11-07 11:34Z**：正式目录带复核 build 在本沙箱 rc=0 · REVIEW_ACCEPTED · market_sessions us/cn=2026-11-06，即 ② 的沙箱 glob 兜底在生产路径实跑通过；非代签）② `market_pressure.py` 新增 `_default_documents_root()`（env `RISK_DAILY_DOCUMENTS_ROOT` → `~/Documents`（含 Database 才取）→ `/sessions/*/mnt/Documents` glob 取最新，与 `ops/check_starfield_freshness.py` `_resolve` 同款），`snapshot()` 默认根改走它、显式 `documents` 优先；③ `narrative_review.py` `prepare()` 加 `documents=None` 透传 `market_snapshot(documents=…)`，CLI `prepare [out] --model M --documents ROOT`（原无 argparse，仅 prepare 分支加 argparse；apply 分支未动）、`-h/--help` 显示两参数。验证：两件 `py_compile` 过；`--help`/`prepare --help` 均列 --model/--documents；沙箱 `env -u RISK_DAILY_DOCUMENTS_ROOT` 下 `_default_documents_root()` 解析到 `/sessions/…/mnt/Documents`、snapshot us/cn 均 available(2026-11-06)；`prepare /tmp/… --model test-model --documents <挂载点>` rc=0、包内 binding.model=test-model。备份 `_bak/market_pressure.py.bak_2026-11-07_17A`、`_bak/narrative_review.py.bak_2026-11-07_17A`。 → 2026-11-07 审核者复验 PASS（两件 compile 过；`--help`/`prepare --help` 列 --model/--documents；`env -u RISK_DAILY_DOCUMENTS_ROOT` 下解析到 `/sessions/…/mnt/Documents`〔本 VM `~/Documents` 为挂载点 symlink 走第二级；另以 HOME=/tmp/fakehome 验 glob 第三级同样解析到挂载点〕；snapshot 默认根 us/cn 可取） **✅ 二次独立复验 2026-11-07 ~17:50Z（落签者=另一未参与实施的审核者 subagent · /tmp/rd17a 隔离 · 结论与上段一致 PASS）**：补证 ① 改动面 diff——market_pressure 3 hunk / narrative_review 6 hunk，`market_binding/run_model/apply/_resolve_pricing/_apply_locked` 函数体无差异；② 四向实跑含负向（HOME=/nonexistent + glob 置空 → 返回 `/nonexistent/Documents`、snapshot us/cn unavailable 不崩）、`snapshot(documents=<不存在>)` 不回退默认根、无参 `prepare` 向后兼容 rc=0、`apply` 无参 rc=2；③ 11-04 三层根因 ①②③ 现全闭合，build 侧 L126/L132 显式传 `documents=DOCS`；④ 会话名/`assert` 计数 0。**附注（不阻断）**：(a) 原追记「apply 分支未动」应改口为「apply 分支仅 usage 文案改引 `USAGE` 常量（L329/L341），校验/落盘逻辑未动」；(b) `_default_documents_root()` 的 `sorted(glob, key=os.path.getmtime)` 若候选在 glob 与 getmtime 之间消失会抛 `FileNotFoundError` 且在 `snapshot()` try 之外（与 `check_starfield_freshness._resolve` 同款同险）——生产 build 显式传根不受影响，可选 `key=lambda p: getmtime(p) if exists(p) else 0`；(c) env 根不校验属「显式优先、fail-visible」设计选择。局限：Mac 原生 `/Users` 宿主未在 VM 实跑（第二级代码路径已经 symlink 走通）；备份原件无版本库可对。

## [ERR-20261107-001] narrative_events.json 字段自相矛盾：`crwv-leverage-0630` precision=day 但 published="2026-08"（月粒度）
**状态**: ✅ 已修复（2026-11-07 未参与实施的审核者 subagent 独立复验 PASS_WITH_LIMITS 代签 · 证据：data 文本/JSON 语义 diff 各仅 precision 一处且 published 仍 "2026-08"；validate_events 备份数据报「precision=day…非日粒度」且 clean 34=现数据 34（只报不剔）、现数据 0 precision 错；test_narrative_score 57 PASS/0 FAIL、test_narrative_digestion 9 OK；compute 只读对拍修前后 score 76.0/base 61.8/per_actor 全同。限制：现评估 input.events_hash 仍绑旧表（=备份哈希），普通构建将沿用上次有效评估标陈旧直至下次带复核构建重绑；validate 任一 error 即令 compute 不可判（既有语义，非剔样本而是整次回退））
**沿革**: ⚠️ 已知风险（2026-11-07 独立审查者 subagent 发现 · CC 登记 · 事件内容修订不在 PRD 2026-11-07_叙事消化度 范围） → 🔄 已修待验（2026-11-07 Doctor 批 P0①②：① `data/narrative_events.json` crwv-leverage-0630 precision day→month（备份 `data/_bak/…bak_2026-11-07_precision`）；② `narrative_score.py` validate_events 加 precision↔published 粒度一致性门禁（只报不剔·避免改评分样本）+ `test_narrative_score.py` 2p/2p' 负向用例，57/57；待未参与实施的审核者复验代签）
**优先级**: 🟢 低（叙事消化度模块靠 `len(published)<10` 兜住并计入 excluded，结果正确；但 `dates.precision` 不可信）
**触发场景**: `narrative_digestion.load_events` 读 `data/narrative_events.json` actors.funding.events[]，事件 `crwv-leverage-0630` 的 `dates`={published:"2026-08", precision:"day"}。
**硬证据**: 实读 json；模块输出 `excluded=[crwv-leverage-0630: precision='day' published='2026-08'（非日/分钟精度）]`；独立审查 R3 对账 confirming 19 = 簇内 18 + excluded 1。
**根因**: 事件登记时 precision 字段未随 published 粒度填写（人工/模型回填漏校验）；narrative_score.py 自检未校验 precision 与 published 长度一致性。
**影响面**: 任何按 `precision` 字段分流的消费者会把月粒度日期当日粒度用；当前已知消费者仅叙事消化度（已兜住）。
**建议修法**: ① 把该事件 precision 改为 "month"（事件内容修订 · 需 Doctor 批）；② `narrative_score.py` 自检加「precision=day ⇒ len(published)==10」校验，fail-visible。
**预防门禁**: 事件源回源更新（班步骤 2）写入后跑 narrative_score 自检；自检加该规则后此类不再静默。
**来源**: 2026-11-07 PRD 叙事消化度 Step 7.5 独立审查 · CC 登记

## [ERR-20261106-001] FOMC 卡「结果 · 观星✓/✗」用最新会前读数对上一场旧结果打分——会后预测对会前结果的假命中
**状态**: ✅ 已修复（2026-11-07 未参与实施的审核者 subagent 独立复验 PASS 代签 · 证据：diff `_bak/build_risk_daily.py.bak_2026-11-07_16A` 仅 L841→L841-843 一处 hunk；编译过；审核者自建 /tmp 隔离副本 + `RISK_DAILY_DOCUMENTS_ROOT=<挂载点>` 实跑 build rc=0，产物 FOMC 卡「✅ 结果：hike（2026-09-16 FOMC 加息 25bp …）· 市场主判✓」、全文 `观星✓/✗` 计 0（gx_asof 2026-11-06 > meeting 2026-09-16）；正式目录无文件被改。**正式产物追记 2026-11-07 11:34Z**（Doctor 令手动重推 · CC 实跑）：正式目录 `build_risk_daily.py --review-command model_entry.py --review-model deepseek-chat` rc=0 · REVIEW_ACCEPTED · `dashboard/risk-daily.html` sha256 `4505a0d3…`（与 `data/envelopes/2026-11-07.envelope.json` 一致）· 正式产物「观星✓/✗」计 0、FOMC 卡显「结果：hike」· artifact risk-daily 已推（综合温度 27 平静·分子均值 187/7）
**沿革**: 🔄 待修（2026-11-06 L1 专场独立复核 subagent 发现 · CC 实读复核登记 · 不在 L1 改动范围、未修）→ 🔄 已修待验（2026-11-07 Doctor 裁 16A：`build_risk_daily.py` L841-843 加 `_gx_aligned = gx_policy 存在 and _mx.meeting 存在 and str(gx_asof) <= str(_mx["meeting"])`，仅对齐时拼「· 观星✓/✗」，否则只显「结果：{_oc}」；市场主判角标未动。验证：`py_compile` 过；/tmp 隔离副本 `RISK_DAILY_DOCUMENTS_ROOT` 指挂载点实跑 build rc=0，产物 FOMC 卡「✅ 结果：hike（2026-09-16…）· 市场主判✓」、`观星✓/✗` 计数 0（观星读数 11-06 > 会期 09-16 → 不打分）；正式目录产物（改前）同处仍见「观星✓」作对照。备份 `_bak/build_risk_daily.py.bak_2026-11-07_16A`。正式产物待 11-08 班自然重建）
**优先级**: 🟢 低（信息层角标；不进判定/触发/温度）
**触发场景**: `build_risk_daily.py` 约 L840 `_ocline`：`'观星✓' if _gxp == _oc else '观星✗'`——`_gxp` 取自最新 `fed_prediction_*.json`（2026-11-05 会前读数，对象是 12-08~09 会），`_oc` 取自 `fomc_market_exp.json.outcome`（2026-09-16 会的实际结果 hike）。两者不同会期却被直接比对。
**硬证据**: 2026-11-06 隔离重建产物 `risk-daily.html` 渲染「✅ 结果：hike（2026-09-16 FOMC 加息 25bp…）· 观星✓」；`fomc_market_exp.json` 实读 `meeting=2026-09-16, outcome=hike`，观星 json `date=2026-11-05, policy=hike`。✓ 由会期错配偶然产生，若观星读数换成 hold 则会显 ✗，同样无意义。
**根因**: outcome 槽按「上一场结果」手填并长期留存，而观星读数按最新文件 glob；比对处未按会期对齐，也无 outcome 过期判定。
**影响面**: 仅 FOMC 卡 `fomc_exp_c` 角标；读者可能把 ✓ 当成观星模型命中记录（与 G-X94「8 样本方向真不确证」纪律相悖）。
**建议修法**: ① 比对前要求 `_mx['meeting']` 与观星 json 中对应会期一致（观星 json 现无会期字段 → 以 `date <= meeting` 的最后一份读数为准），否则不打分；或 ② outcome 过期（下一场会前窗开启）即只显结果、不显 ✓/✗。
**预防门禁**: 跨文件比对一律先对齐键（会期/日期），再比值。
**来源**: 2026-11-06 金融线脑暴17项 L1 专场 · 独立复核 subagent（未参与实施）发现 · CC 实读确认。

## [ERR-20261110-001] AI 复核多次采样有效率过低：近三次带复核构建有效样本 1/3、1/3、0/3（今日两次全灭→REVIEW_REJECTED）
**状态**: 🔄 已修待验（2026-11-10 同日诊断＋修复，见文末「诊断与修复」；验收归 Doctor）
**优先级**: 🔴 高
**触发**: 2026-11-10 实施投资级恶化利差阈值后改了 `narrative_events.json`（Meta 事件补 `ig_signal`）→ events_hash 变 → 须带复核构建重绑。连跑两次均 `REVIEW_REJECTED: 全部复核样本无效`，面板转「待重检（沿用有效评估）」，AI 61.6 沿用 11-09 评估。
**硬证据**: `data/narrative_review_samples.jsonl`——11-08 17:09Z `n_valid=1`、11-09 17:13Z `n_valid=1`（各 3 份请求）；今日两次构建日志 `/tmp/rd_build.log`、`/tmp/rd_build2.log`（拒绝的构建不落 samples 日志）。
**失败形态（两类，均早于今日改动）**: ① `model_entry.py` 退出码 5＝模型输出非法 JSON（第 133–139 行，疑截断或混入非 JSON 文本，未取原文核）；② 校验拒绝：`funding critical_basis 含非字符串元素` 并带出 HARD「市场担忧引用须来自本轮有效维度依据」。
**影响面**: ① 多次采样形同单样本——11-08 班只有 1 份有效样本却按「多数票」定判级，chosen funding=82（该份是否判 critical 未核）；② 事件表一改就易长期陈旧；③ 日更 AI 读数实际由偶然通过的那一份决定。
**根因**: 未定位（未取模型原始输出）。候选：输出长度仍超限；模型把 critical_basis 写成对象；v22 指令后输出结构更复杂。
**建议修法（待 Doctor 裁）**: 先落盘失败样本原文（stderr/截断片段）再定修法；可选方向——有效样本 <2 时补采、或 n_valid=1 不得单独判 critical。
**预防门禁**: 带复核构建报告须含 n_valid；n_valid<2 连续两班即告警。
**来源**: 2026-11-10 风险日报投资级恶化阈值实施场 · CC 实读样本日志与构建日志。
**诊断与修复（2026-11-10 · Doctor 裁「先诊断再定」后批三项）**: 失败样本原文落 `data/narrative_review_failures.jsonl`（新增诊断日志，model_entry 在非法 JSON 时输出 stop_reason/usage/首尾片段）。三类根因：① 截断——模型回抄事件 facts/evidence，写满 8000 token（`stop_reason=max_tokens`）→ 适配层加「只写 event_id、不得回抄事件内容」，上限 12000；② 依据写成 `{event_id, transmission_channel}` 对象 → `repair_sample` 只取 id；③ 融资维判 critical 但依据无生效通道 → 连带整份作废 → 改为只去掉 critical、分数压到 74（Doctor 裁）。修后首跑 `REVIEW_ACCEPTED`、有效 2/3、两份样本均触发融资降级（模型引 Oracle 发债定价与 CoreWeave 收益率作 critical 依据，二者未标通道）；仍有 1 份在 12000 上限下截断（28.6k 字符），回抄未根绝。测试 143/0。

**追记（2026-11-13 /todo · 未参与实施的审核者诊断 · 状态维持 🔄）**: 修复后 4 次带复核构建 n_valid＝2/3、2/3、**1/3（11-11 17:10）**、**1/3（11-12 17:10）**，两次 1/3 是两种失败模式。**模式 A 截断（修法未击中）**：failures.jsonl 第 3–6 行均 `stop_reason=max_tokens`、output 12000，head 以 `"input": {"prepared_at_utc"…"binding"` 开头、tail 为事件对象——模型把整个精简输入包抄进顶层 `input`；因指令要求 input「逐字等于 input_template」（narrative_review.py:146）而 `model_entry.py:72-75` 精简包白名单不含 `input_template`，适配层又写「绑定字段必须原样回填」（:71/:84）；11-10 的「不得回抄 claim/facts」只管依据字段，上限 8000→12000 只推迟截断；指令「8000 token 内闭合」（:148）已与 12000 不一致（置信度：机制高、主因中高）。**模式 B 日间限幅拒绝（新）**：11-12 三样本 demand 54/42/42，锚点为 11-11 选中的单样本 58，42 超 ±15 一分；加速豁免要求 refuting 事件发布日晚于旧评估 UTC 日（`_published_between` :170-180/:205-212），CRWV 11-10 发布不算新；F16 去锚（previous_assessment=None）而 bounded_check 逐样本对单样本锚比 ⇒ 正常采样离散被随机拒（置信度高）。**影响**：11-12 唯一有效样本判 funding critical 82，面板由 11-11 非 critical 跳红 82，同日另两份无原文可核（bounded 失败不写 failures.jsonl、被拒构建不写 samples.jsonl）。**建议修法（未实施，方向性归 Doctor）**：① 由系统填 `input`、不要模型回显（退一步：把 input_template 送进精简包并明说勿复制）；② bounded_check 移到共识之后或以上一轮多样本中位为锚；③ bounded 失败与被拒构建也落诊断；④ n_valid<2 补采、n_valid=1 不得单独判 critical。

**修复与验收（2026-11-13 · Doctor 批「四项一起修」）**: 实施者 subagent 改 `narrative_review.py` / `model_entry.py` / `narrative_score.py`（备份 `.bak_2026-11-13_sampling`）：① input 由系统写入、模型不回显，token 上限统一为常量 12000；② bounded_check 移到共识后只核选中样本，锚为上一轮多样本中位（`bounded_anchor`）；③ bounded 失败与所有拒绝出口均落诊断 / rejected 行；④ n_valid<2 补采（≤2 份）、补采后仍 1 份则降为非 critical 并留痕（分数不动）。测试 180/0、data/ 前后 0 差。未参与实施的验收者 **PASS_WITH_LIMITS**，无硬阻断；限制：截断是否根除待首个真实班次看 failures.jsonl；下一班中位锚实际等于 11-12 单样本（来源标签 `prev_median` 有误导，宜加记 n_valid）；单样本降级口径 Doctor 2026-11-13 裁「维持分数不动」（与 11-10「缺通道压到 74」分属不同情形）；最坏 5 份请求约 15 分钟、班次外层超时未核。状态：🔄 已修待验（功能性，最终验收归 Doctor）。

**自然证据追记（2026-11-15 · CC 实读 `data/narrative_review_samples.jsonl` 末两行与 `data/narrative_review_failures.jsonl` 末 4 行 · 状态维持 🔄）**: 修后两次真实日更班均 `accepted`、`n_valid=2`——11-13 17:10Z 首轮只得 1 份、补采 2 份（`n_requested=5`、`n_topup=2`）后过；11-14 17:08Z 首轮 3 中 2、未补采。**截断已不再出现**：两班 4 条失败均非 `max_tokens`（2 条 `invalid`、1 条网络 `RemoteDisconnected` exit 4、另 1 条 `invalid`）；补采班最后样本落盘 17:10:50Z，未见超时迹象。**残留失败模式（新形态，未修）**：3 条 `invalid` 中 2 条为模型把**报道级事件**（`openai-first-close-1106`、`openai-round-target-cut`）写进 funding critical_basis——校验剔除该 id 后，`outlook.event_ids` 仍引用它，连带触发 HARD「市场担忧引用须来自本轮有效维度依据」，整份作废；另 1 条为 HARD「缺市场担忧、延续、定价或证伪条件」。同期 `funding_critical_downgraded` 分别为 2、1。**是否改为「剔除后同步从 outlook 引用里去掉、不整份作废」属校验语义变更，待 Doctor 裁。**

**残留形态修复（2026-11-15 · Doctor 裁「改为剔除不作废」· CC 实施，待独立复验与 Doctor 功能验收）**: 读码订正机制：作废并非担忧段引用本身出错，而是 `validate_assessment`（narrative_score.py:713-715）见 critical_basis 含不可撑事件即 `continue` **整维剔除**，担忧段引用的融资维事件随之不在有效依据内，才连带 HARD。故修法落在修复层、不改校验：`narrative_review.py` `repair_sample()` 新增一段——critical=true 时把本维内不可撑 critical 的 id 从 critical_basis 去掉（basis_confirming 不动，报道型仍可作维度依据），计入 repaired；非融资维去空则 critical 改否、分数不动；融资维去空或去后无生效通道的交既有「缺通道降级」（压到 74）；不存在的 id、非字符串元素不动、仍交校验拒绝。只走 run_model 路径，手工 apply 不经此处。担忧段引用无须另改。测试新增 12f–12k，186/0、生产 data/ 与 dashboard/ 前后 0 差（16a）；变异两处（删整段 → 12h/12i/12j 失败；删「非融资维去空改否」→ 12j 失败）。备份 `_bak/narrative_review.py.bak_2026-11-15_weakstrip`、`_bak/test_narrative_score.py.bak_2026-11-15_weakstrip`。**自然验证**：下一次日更（11-15 17:05Z 起）看 samples.jsonl 的 `input_repaired` 与 failures.jsonl 是否还出现「不可撑 critical」型 invalid。

**独立复验（2026-11-15 · 未参与实施的审核者 subagent）**: PASS_WITH_LIMITS——① 改动面：`diff` 对 `_bak/*.bak_2026-11-15_weakstrip`，`narrative_review.py` 仅 `repair_sample()` 内新增 18 行、测试仅追加 12f–12k，无其他改动；生产调用点仅 `narrative_review.py:427`（run_model 采样路径），手工 apply 不经此处。② 机制：读 `validate_assessment` 确认原链条为「critical_basis 含不可撑 id → 整维 `continue` → 担忧段引用不在有效依据 → HARD → 任一 errs 即整份作废」；修复在校验前剔 id，切断该链，校验本身未改。③ 内存重放（真实事件表、以现 `narrative_assessment.json` 为底，不写盘）：11-14 s3 形态 cb=[crwv-cds-peak-1015, openai-round-target-cut, cloud-meta-outlook-negative] 修前 HARD、修后剔 openai-round-target-cut、funding 82 critical 保留（cloud-meta 提供 ig_deterioration 通道）、整份 0 错；11-13 s2 形态（含 openai-first-close-1106）同样修后通过；仅报道型、报道型+无通道强证据两例均走缺通道降级 74。④ 负向：非字符串元素、跨维 id、本维不存在 id、critical=false 带弱 cb、重复强 id 均不动、仍被校验拒绝。⑤ 实跑 `python3 -B test_narrative_score.py` 186 PASS / 0 FAIL，16a 通过；临时副本 5 种变异（删整段、去融资豁免、幽灵 id 也剔、一律改否、连 basis_confirming 一起剔）各被 12h/12i/12j/12k 至少一条抓到，副本已删。**限制**：(a) 剔除只判「本维存在且不可撑」，不判是否在 basis_confirming 内——弱 id 在 critical_basis 但不在 basis_confirming、或弱 id 重复时，原本另报的子集/去重错误被一并消解（实跑两例修后通过）；结果方向保守（只少不多），但属轻微超出「只剔不可撑」字面；(b) 剔除计数并入 `repaired` → samples.jsonl 的 `input_repaired`，与依据对象→id 的形状修复混计，自然验证时无法单凭该字段区分，需对照 failures.jsonl；(c) 11-13 s1「缺市场担忧、延续、定价或证伪条件」型失败不在本修复范围；(d) 真实班次效果待 11-15 17:05Z 起自然验证。功能验收仍归 Doctor。

**复验限制①收口（2026-11-15 · CC）**: 剔除前加结构闸——critical_basis 有重复或含不在 basis_confirming 内的 id 时修复层不动、照旧交校验拒绝，不再顺带消掉这两类结构错。新增 12l/12m，188/0；变异（删结构闸）→ 12l、12m 失败。限制②（剔除计数与形状修复同计 `input_repaired`）未改：自然验证以 failures.jsonl 不再出现「不可撑 critical」型 invalid 为准。状态维持 🔄（功能验收归 Doctor）。

---

## [ERR-20261112-001] 云端托管页小字发细发淡：云端加载到 Google 在线字体，侧栏加载不到、回退本机思源宋体
**状态**: ✅ 已验收（2026-11-15 · 未参与实施的审核者 subagent 独立核验：`strip_webfont()` 在两子页循环与主页各调用一次、条数≠3 或删后残留即 `die()` 且写盘在全部校验之后，负向两例实跑 exit 1；对现原件（sha 8a7d8ecb，内含 6 处 googleapis）内存重放三页 sha 5892bf87/58b2f9c4/d1be339e ＝ 盘上 artifact/manifest/published.json，三页 `fonts.googleapis.com`/`fonts.gstatic.com` 均 0 处；事实性非功能修复由审核者代签）（原：🔄 已修待验 · 2026-11-12 同日修复；Doctor 目验「通过」；拆分器复验 PASS_WITH_LIMITS 见 `brain/TODO.md`「看板推送改为云端班自推」子行）
**优先级**: 🟡 中
**触发**: 2026-11-12 风险日报三页（主页 / AI Tech Alarm / EAL 星空）首次推上 claude.ai 托管页，Doctor 目验发现正文小字（9.5–11px）比侧栏版细、淡。
**硬证据**: ① 容器内 playwright 逐文本节点对拍：原件 vs 「外壳+片段」，字号/字重/字色/行高设定值差异 0（主页 165 条、AI 560 条、EAL 17 条）；② 旧片段 `document.fonts` 载入 `Noto Serif SC 400/600/700`，删引用后载入列表为空；③ Doctor 两张截图（侧栏＝正确、云端＝错误小字）；④ 八个托管页中只有这三页引用 `fonts.googleapis.com`。
**根因**: 页面 `<head>` 引 Google Fonts 的 Noto Serif SC。侧栏（桌面端）内容安全策略不放行，字体栈落到本机已装的思源宋体——这才是一直以来的「正确观感」；托管页放行 fonts.googleapis.com / fonts.gstatic.com，实际用了 Google 下发的同款字体文件，笔画更细。设定值相同、字体文件不同。
**影响面**: 仅云端托管页观感；本地原件与侧栏不受影响。
**修法（Doctor 点头）**: `brain/.tools/artifact_split_risk_daily.py` 加 `strip_webfont()`，三页片段删掉 Google Fonts 的三条 `<link>`（两条 preconnect + 一条样式表），不是恰好三条或删后仍有残留即 exit 1、三页都不写。原件不动。备份 `.bak_2026-11-12_pre-localfont`。
**预防门禁**: 新看板上云前查是否引用在线字体；对拍只比设定值查不出这类差异，必须有人眼目验或比 `document.fonts` 载入列表。
**已知限制**: 未装思源宋体的设备（如手机）落到 Songti SC / 系统衬线体，粗细可能与电脑不同。
**来源**: 2026-11-12 看板上云场 · Doctor 目验 + CC 实跑对拍。

## [ERR-20261112-002] EAL 事件星空「数据与阅读方式」弹窗里夹一处字面 `...`
**状态**: ✅ 已验收（2026-11-15 · 未参与实施的审核者 subagent 独立核验：源头 11-12 02:38 PT 修改后，`EAL_STARFIELD.html`（11-13 21:09 PT 重建）与 `risk-daily.html`（11-14 09:08 PT 构建）正常形 `</section>...<section` 与转义形 `<\/section>...<section` 均 0 处，「行情与版本」各 1 处且其前紧接 `</section><section`（转义形同），备份含 1 处、现源头 0 处；事实性非功能修复由审核者代签）（原：🔄 已修待验 · 2026-11-12 Doctor 裁「修」，源头第 250 行删字面 `...`，备份 `.bak_2026-11-12_pre-ellipsis`，派生文件待下次构建后回读）
**优先级**: 🟢 低
**触发**: 2026-11-12 发布前通读 EAL 星空子页时发现；弹窗两个 `<section class="detail-section">` 之间原样显示三个点。
**硬证据**: `risk-daily.html` 的 `EAL_HTML` 常量解码后即含 `…回测。</p></section>...<section class="detail-section"><h3>行情与版本</h3>`（实读解码文档，1 处）；托管页同位置同文。**原件就有，不是拆分上云造成的。**
**根因**: 未定位。疑为生成 EAL 星空页的模板/拼接处留下的省略占位。
**影响面**: 侧栏与云端都会显示；纯观感。
**建议修法**: 查 EAL 星空页生成器对应模板，删掉占位。
**预防门禁**: 生成后 grep `</section>...<section`。
**附 · 待核（不是已证实的错）**: 同页行情更新到 2026-11-09，但带日期的事件最晚是 2026-09-30，默认视窗内没有事件星。是事件线断更还是本就无新事件，未核。
**来源**: 2026-11-12 看板上云场 · 发布前通读（subagent）+ CC 实读原件复核。

## [ERR-20261112-003] 子页里的相对链接在托管页上是死链（AI Alarm 三条、EAL 星空「研究台」两处）
**状态**: ✅ 已验收（2026-11-15 Doctor 裁「接受残留并落签」· 已知限制：AI 页三条入口只挡鼠标，键盘 Tab 聚焦后回车仍会跳死链——按 11-12「只加样式、不改脚本」口径接受）｜原：🔄 已修待验（2026-11-12 Doctor 裁「修」，取修法①：拆分器 `neutralize_deadlinks()` 给云端片段末尾加一条样式——AI 页三条本地入口保留文字、不可点；EAL 页 `a[href^="/research"]` 隐藏。只加样式，不删改正文脚本，原件不动；形态不符即 fail-closed；备份 `.bak_2026-11-12_pre-deadlink`）｜2026-11-12 独立复验 PASS_WITH_LIMITS（未参与实施的 subagent）
**优先级**: 🟢 低
**触发**: 2026-11-12 三页拆出上云后，子页成为独立托管页。
**硬证据**: AI Tech Alarm 页脚本把 `lnk-research` / `lnk-desk` / `lnk-eal-db` 的 href 设为 `../Financial/Event-Attribution-Ledger/backtest/*.html`（实读片段）；EAL 星空页两处 `href="/research"`（实读）。均为原件既有写法。
**根因**: 这些链接假定页面从本地文件系统或研究台服务打开；托管页（以及侧栏 iframe）里没有这些路径。
**影响面**: 点了打不开；不影响其余内容。
**可选修法**: ① 云端版隐藏这几条链接；② 目标页也上云后改指托管地址；③ 保持现状。
**来源**: 2026-11-12 看板上云场 · 发布前通读（subagent）+ CC 实读复核。

---

## [ERR-20261113-001] `test_narrative_score.py` 测试 4d 非封闭：跑一次就联网改写生产缓存 `data/bbb_oas.json`

**状态**: ✅ 已修复（2026-11-13 实施者 subagent 修：4d 段与 _stage14 替换 `BBB_OAS_FILE` 并打桩 `refresh_bbb_oas`，新增 16a 封闭性断言；未参与实施的验收者 PASS——180/0、M2 变异可被 16a 抓到、整仓快照 0 差；事实性非功能修复由验收 subagent 代签）
**优先级**: 🟡 中
**触发**: 2026-11-13 /todo 审核者为 PRD F14–F17 二审实跑 `python3 -B test_narrative_score.py`，`data/bbb_oas.json` 被改写（mtime 11-13 10:12:01Z，`fetched_at_utc` 变 11-13，`last_date` 11-11）。
**硬证据**: 测试 4d（test_narrative_score.py:230/237）调 `nr.run_model` → `prepare()` → `ns.refresh_bbb_oas()`（narrative_score.py:311 起）；该路径未替换 `BBB_OAS_FILE`（替换补丁到第 629 行才生效），故真实联网拉 FRED 并覆盖生产文件；旧版本（11-12 拉取）已被覆盖、无备份。
**影响面**: 任何人跑测试都会改写生产缓存；本次内容为同一序列新拉，当日班次会跳过，无数值事故。
**建议修法**: 4d 段同样替换 `BBB_OAS_FILE`，或替换 `refresh_bbb_oas`；补一条断言「测试前后生产 data/ 目录无改动」。
**预防门禁**: 测试套件开跑前后对 `data/` 做 mtime/sha 快照比对，有差即 FAIL。
**来源**: 2026-11-13 /todo 未参与实施的审核者实跑发现（其足迹自报）。

---

## [ERR-20261113-002] F14 market_data 来源校验用不分大小写子串匹配：`ICE` 命中 price / notice / service，`TRACE` 命中 retrace

**状态**: ✅ 已验收（2026-11-15 Doctor 裁「按现状验收」· 偏严误拒连写一项接受，生产出现连写形态时再补白名单）｜原：🔄 已修待验（2026-11-13 实施者 subagent 改 `narrative_score.py:56-69` 词边界＋全大写缩写大小写敏感，:218 调用；验收者 PASS_WITH_LIMITS——负例全拒、正例全过、生产事件无误拒；限制：偏严会误拒 ICEBofA / S&P500 / 8-Ks 等连写，小写 moody / fitch 放行；改变校验行为，最终验收归 Doctor）
**优先级**: 🟡 中
**触发**: 2026-11-13 /todo PRD F14–F17 二次独立审查。
**硬证据**: `narrative_score.py:198-203` 校验 claim/facts/locator 中写明 `MARKET_DATA_VENDORS`（:55）来源；审核者内存探测（不落盘）：claim 写「某公司债券 price 大跌」「notice 显示走阔」「service 指标」时 `_v4_event_error` 返回 None（放行），去掉这些词才拒。
**影响面**: 未写真实行情供应商的 market_data 事件可通过校验，进而具备 critical_eligible（:256-259）资格；当前生产两条（Tradeweb / ICE）为真实来源，未见误放行实例。
**建议修法**: 改词边界或大小写敏感匹配；补负向测试（price / notice / service / retrace 均须拒）。
**预防门禁**: 供应商名单匹配一律走词边界正则，并纳入测试。
**来源**: 2026-11-13 /todo 未参与实施的审核者只读审查。

## [ERR-20261115-001] `Codex/风险日报/AI Tech Alarm/` 是 11-05 迁移前的旧副本，按名字搜 AI Tech Alarm 会先撞到它

**状态**: ✅ 已验收（2026-11-15 · 未参与实施的审核者 subagent 核：原位置 `ls` 报不存在，`archived/AI Tech Alarm.archived_2026-11-15` 存在、`find -type f` 31 个、`du` 1.8M，按名搜 `*tech*alarm*`（排除 archived/.git）不再命中 Codex 下目录，现行 `Projects/Financial/风险日报/alarm/`（含 `研究/`）在，班次镜像与 `Projects/Financial/风险日报` 无旧路径引用；事实性处置由审核者代签）｜原：已处置待核（2026-11-15 Doctor 裁「移入 archived」：CC 将旧目录整体移至 `~/Documents/Codex/风险日报/archived/AI Tech Alarm.archived_2026-11-15`，移前移后均 31 个文件、1.8M；移前查过班次镜像、`Projects/Financial/风险日报` 代码与 LaunchAgents，均无引用。注：移前该目录 mtime 为 2026-11-15 03:30，当日有过写入，来源未核）
**触发**: 2026-11-15 Doctor 令把两篇研究稿移入「AI Tech Alarm」并核有无独立文件夹；`find -iname "*tech*alarm*"` 只命中 `Codex/风险日报/AI Tech Alarm/`（含 `研究/` 子目录），现行目录 `Claude/Projects/Financial/风险日报/alarm/` 名字不含 tech，按名搜不到。
**硬证据**: `git -C ~/Documents/Codex status` 显示该目录整批未跟踪（`??`）、末次提交 `bfdc90eb` 2026-11-04；`brain/风险日报/architecture/系统概览.md` 写明「AI Tech Alarm 自 2026-11-05 归本项目（`Projects/Financial/风险日报/alarm/`）」。
**根因**: 11-05 迁移只迁了数据和代码，旧目录未归档也未加弃用标记；目录名比现行目录更「像」。
**影响面**: 任何按名定位 AI Tech Alarm 的会话或分支，可能把产物写进旧副本或读到过期数据。本次已在动手前核出，未误写。
**建议修法**: 旧目录按归档规矩移入 `archived/` 或改名加 `_DEPRECATED_`（须 Doctor 批，属 Codex 仓）；或在其根下放一份 README 指向现行目录。
**预防门禁**: 定位 AI Tech Alarm 一律从 `风险日报/architecture/系统概览.md` 取路径，不按目录名搜。
**来源**: 2026-11-15 AI 中控台会话（`logs/2026-11-15-todo分流与AI中控台G3算力经济账.md`）。

## [NOTE-20261115-002] 模拟「换一个日期构建」时不要把 `datetime.datetime` 整个换成子类——进程段错误退出（exit 139）

**状态**: ⚠️ 已知风险（已绕过；成因未核）
**优先级**: 🟢 低
**触发场景**: 2026-11-15 综合温度边际变化的端到端核验要「换一个北京日期再构建一次」，证明留存文件按日新增一条。首版做法：包一层启动脚本，把 `datetime.datetime` 替换成 `now()` / `utcnow()` 整体平移一天的子类，再 `runpy.run_path("build_risk_daily.py", run_name="__main__")`。
**硬证据/最小复现**: 在项目副本里跑该启动脚本，进程退出码 139，标准输出与标准错误均为空、无 Traceback；留存行已经写出（`data/temp_history.jsonl` 出现 2026-11-16、2026-11-17 两条），但退出码非 0，核验项 B3 判 FAIL。环境 Python 3.13.3。
**根因**: 未核。只知道出在替换 `datetime.datetime` 类之后的某一步（留存写入之后），未用 faulthandler 定位。
**影响面**: 仅测试与核验脚手架。生产构建不替换任何类，不受影响。
**修复/建议修法**: 改为只在副本里把构建器 `bj_now` 那一行的 `hours=8` 换成 `hours=8 + 24 * N`，另存为 `_build_shifted.py` 再跑（`ops/verify_marginal_e2e.py` 的 `build(shift_days=…)`；替换不是恰好一处就停）。改后 B3 通过，退出码 0。
**预防门禁**: 需要拨业务时钟的核验，一律改副本里 `bj_now` 一行，不动 `datetime` 类。
**来源**: 2026-11-15 风险日报边际变化第一段实施场 · CC 实跑。

## [ERR-20261115-003] 综合温度边际变化：两端参与均值的分子不是同一批时，差值照常显示——成分变化被当成温度变化

**状态**: 🔄 已修待验（2026-11-15 同日修；复验与 Doctor 功能验收未完成）
**优先级**: 🟡 中
**触发场景**: 2026-11-15 边际变化第一段首轮独立复核（未参与实施的审查员）。核验脚本「换一个日期再构建」一步把业务时钟拨到 11-17，`ipo_coverage` 最大 `scan_end=20261116`，新股虹吸变「◌不可判」；当前六分子口径由 19 变成五分子均值 22。
**硬证据/最小复现**: 行情一点没变，页面三项却从 `1日 ▼−3 · 5日 → 0 · 20日 ▼−6` 变成 `1日 → 0 · 5日 ▲+3 · 20日 ▼−3`。复现：`temp_history.compute_marginal` 的当前值里把 `ipo` 置空，参照日用六分子回补。git 历史里 2026-09-07、09-08 两版快照只有 1 个分子可判、综合 79，同类情形更极端。
**根因**: 综合温度是「可观测分子」的均值，少一个分子均值就跳。首版只在折叠区写了一句「两端参与均值的分子数不同」，卡面照常给差值。实施者自验时见过这句提示，没有把它当缺陷。
**影响面**: 任一分子某日不可判（新股覆盖闸不过、AI 评估缺失等）时，当日与此后以该日为参照的各项变化值失真。未上线，无生产影响。
**修复/建议修法**: `compute_marginal` 改为比较两端参与均值的分子集合（回补参照时当前一侧去掉 AI），集合不同则该项显示「◌不可判」并写明缺哪个分子，两端数值留在数据里备查；两端同缺同一个分子视为同口径。同批顺修三处小项：留存行类型坏掉（如 `composite` 是字符串）改按坏行跳过，不再让整块不可用；升温最多分子一行写明哪些分子因一端缺数未参与比较；`recompute_six(today=…)` 的新股窗不再先截到数据日。
**预防门禁**: 单测 `Marginal.test_member_mismatch_is_na_not_a_delta`、`test_top_riser_names_molecules_left_out`、`Retention.test_bad_lines_skipped_not_fatal`；核验脚本 B6。后续新增「相对历史的变化」类读数时，先问两端口径是否同一批成员。
**来源**: 2026-11-15 风险日报边际变化第一段 · 独立复核回报（PASS_WITH_LIMITS · 实错 1–4）。
**Doctor 裁定（2026-11-15 23:20 选择窗）**: 分子不齐时显示「◌不可判」（即现行实现）。未取的两个备选：照常给差值加短标；只在两端共有的分子上重算差值。
**复验（2026-11-15 · 未参与实施的审查员）**: PASS_WITH_LIMITS，自造 16 种情形全部等于手算，五种回退变异单测都报错；状态维持 🔄（功能验收归 Doctor）。

## [NOTE-20261115-004] `test_narrative_score.py` 每跑一次在系统临时目录留下一个含 `bbb_oas.json` 的目录

**状态**: 🔄 待修复（未动；不在本场任务范围）
**优先级**: 🟢 低
**触发场景**: 2026-11-15 边际变化独立复核，审查员清理足迹时发现 `/tmp/claude-501/` 下有不属于自己的 `tmp*` 目录。
**硬证据/最小复现**: `ls /tmp/claude-501/tmp*/` 可见多个只含 `bbb_oas.json` 的目录（11-15 08:03、08:07、08:09、22:41、22:47 等，与各次跑测试的时刻对应）。CC 于 23:13 核实后顺手删了这些目录里的 `bbb_oas.json`（都是测试用的缓存副本），空目录还在，可按目录创建时刻对上；`test_narrative_score.py:635` 为 `_tmpd = tempfile.mkdtemp()`，全文未见对应的清理。
**根因**: 该处用 `mkdtemp()` 而不是 `TemporaryDirectory()` 上下文，测试结束不删。
**影响面**: 只占系统临时目录，不碰项目与行情库；长期积累。
**修复/建议修法**: 改用 `tempfile.TemporaryDirectory()`，或在文件末尾 `shutil.rmtree(_tmpd, ignore_errors=True)`。
**预防门禁**: 测试收尾比对系统临时目录有无本进程新建的残留。
**来源**: 2026-11-15 独立复核回报（足迹一节）· CC 实读 `ls` 与源码行核实。

## [NOTE-20261116-001] Tushare 离岸汇率日线的日期是 K 线起点：`fx_cnh_daily` 的日期比北京交易日早一天，最新一行可能是没走完的 K 线

**状态**: 🔄 已修待验（2026-11-16 夜专场：取数脚本、库内历史行、风险日报回补文件与基线文档同场改完，见末段「专场实施」；功能验收归 Doctor）。原状态：⚠️ 已知风险（既有「人民币贬值」分子的输入未动；新表 `cn_liquidity_daily.usdcnh_spot` 已按北京交易日重标）
**优先级**: 🟡 中
**触发场景**: 2026-11-16 国内流动性读数第二段，给「离岸减在岸」取离岸历史时逐行看 Tushare `fx_daily`（`USDCNH.FXCM`）。
**硬证据/最小复现**: Tushare 返回 2026-11-08（周日）有行、`tick_qty` 65627，11-06（周五）与 11-07 无行；11-13（周五）`tick_qty`＝1，11-14（周六）95，11-15（周日）3728 且当时仍在变。即标 D 的那根覆盖 D 纽约 17:00 到 D+1 纽约 17:00，对应北京的下一个工作日。库内 `recap.db.fx_cnh_daily` 最新行 `('20261112', 6.6727)`，写入时间 2026-11-13T18:08 北京；同一根 K 线在 11-16 实取的买卖收盘中间价是 6.674745。上一行 20261111 库内 6.6733，与实取中间价 6.673325 相符。
**根因**: FXCM 日线以纽约 17:00 为界，Tushare 的 `trade_date` 标的是起点日。`ZZ/scripts/fetch_fx_cnh.py` 在北京傍晚取数时，最新那根还没走完，取到的是盘中值；之后该行不再更新（「不再更新」由库内值与现取值不同推断，该脚本的写入语句本场未读）。
**影响面**: 风险日报「人民币贬值」分子的温度（USDCNH 分位）与 7 日变动震动：日期整体早一个交易日，最新一行是盘中快照而不是收盘。量级是几十个点，不改变分位的大致位置；与在岸序列逐日相减时会错一天。写入方是烛照九阴的班，本条登记在读数方。
**修复/建议修法**: 由 `fetch_fx_cnh.py` 的维护方决定是否重标日期、是否只写走完的 K 线并回补最新行。本场未改该脚本与该表。
**预防门禁**: 取数工具 `fetch_cn_liquidity.py` 的 `redate_fxcm` 与测试 `Parsers.test_fxcm_bars_are_redated_to_beijing_day`。凡用境外报价商日线与境内交易日对齐，先看周末有没有行。
**来源**: 2026-11-16 本场实跑（Tushare `fx_daily` 2026-11-01～11-16 逐行）与 `recap.db` 只读对照；`Projects/Financial/风险日报/docs/2026-11-15-国内流动性数据源实测表.md` 第 6 节。
**追记（2026-11-16 第三段国内宏观场 · 同根复发，已造成一项核验不过）**: `recap.db` 在 2026-11-16 10:08 PST 被日更改写，`fx_cnh_daily` 的 20261112 一行由 6.6727 变成 6.6747（`updated_at` 2026-11-16T18:08:38）。第一段的回补文件 `data/temp_backfill.jsonl` 把 2026-11-12 标为定稿（`stable_through: 2026-11-12`），现库重算该日人民币贬值分子由 7 变 9、六分子综合由 22 变 23，于是 `ops/verify_marginal_e2e.py` 的 F3「回补文件里已定稿的日子与现库重算一致」判 FAIL（34 PASS / 1 FAIL，退出码 1）。实跑复现：用工作区的 `temp_history.build_backfill` 对现库重算，134 个定稿日里只有这一天、只有 fx 一个分子不同；`temp_history.py` 与回补文件本场未改（`git diff` 为空、回补文件修改时间仍是 11-15 23:06）。**状态**：🔄 待修复，归第一段——要么重跑 `python3 temp_history.py backfill` 让文件跟上现库（会改生产读的回补值），要么把定稿线再往前收一天；两者都改到第一段已复核的东西，本场未动，待 Doctor 裁。页面上凡以 11-12 为参照日的边际变化项，在重生成之前与现库差 1。
**再追记（2026-11-16 同日 · Doctor 回复「收紧定稿线并重生成」后）**: 已修待验。根因比「汇率末行」更一般：定稿线取的是各输入末行日期里最早的那天，可一条序列的末行可能还没定——这次重生成时，本就标暂定的 11-13 除人民币分子外，油价分子也由 63 变 62，布伦特 20261113 一行确实被改写过（当日写前备份里是 96.23，现库 95.84）；杠杆分子由 3 变 1 则是两融 11-13 的新行到了，属于输入未到齐，不是末行被改写（初稿把两融也说成被改写，第三次复核查出后订正）。修法：`temp_history.stable_through` 改为「末行日期里最早那天的前一个交易日」，末行那天及以后都标暂定；重生成 `data/temp_backfill.jsonl`（136 条，定稿线 2026-11-12，暂定 11-13、11-16；定稿日里只有 11-12 的值变了，其余 133 天逐条相同）。`ops/verify_marginal_e2e.py` 恢复为 PASS 35 / FAIL 0。预防门禁：`test_temp_history.py` 的 `Recompute.test_finalised_days_survive_a_rewrite_of_a_stable_line_series_last_row`（参与定稿线的序列末行被改写后定稿日逐条不变）、`test_each_of_the_five_series_takes_part_in_the_stable_line`（油价、汇率、两融、成交额、情绪各自参与定稿线）与 `test_backfill_marks_days_with_lagging_inputs_provisional`。残留，届时 F3 会再报：新股募资表 `ipo_daily` 是事件表、不参与定稿线，而它最近几行每天被滚动重写，数值一旦被改写或补录，定稿日的新股分子会变；任何一条序列倒数第二行及更早的行被事后订正；回补文件不会自动重生成，暂定日不会自动转定稿。同一位审查员只读复核这一步为 PASS_WITH_LIMITS；`fetch_fx_cnh.py` 写入未走完 K 线这件事本身没动（归烛照九阴的班）。给「不再变」下定义时，要问的是每条输入的每一行什么时候才算定，不是它有没有出现。

**修复草稿与撤回（2026-11-16 /todo · Doctor 批「修 fetch_fx_cnh 日期重标」后又裁「先撤回，另开专场一次做完」）**：实施代理在 `Projects/Financial/烛照九阴/scripts/fetch_fx_cnh.py` 加 `redate_fxcm`（与剑酒青丘 `fetch_cn_liquidity.redate_fxcm` 2024-01-01～2026-12-31 逐日 0 不一致，重标后与 `usdcnh_spot` 共同 112 日 0 不一致）；独立复验判映射正确、上线 FAIL——库内 tushare 136 行历史未迁移、未挡没走完的 K 线，日更 20 日窗一跑即新旧口径混存、留周末孤行，F3 定稿日 134 个里 8 个变。已用备份还原脚本（与 HEAD 一致），草稿留 `scripts/_bak/fetch_fx_cnh.py.bak_2026-11-16_redate-draft`。专场顺序：补「没走完不写」闸 → 备份 recap.db → 删 `source='tushare'` 行后 `--from 20260610` 重灌 → 重生成 `data/temp_backfill.jsonl` → 复跑 `ops/verify_marginal_e2e.py`；下游 `calibrate_risk_factors.py`、白泽 `fetch_cn_inputs_tushare.py` 一并核。状态维持 ⚠️。

**专场实施（2026-11-16 夜 · 代码、历史、下游同场收口）**：
- **脚本**（`烛照九阴/scripts/fetch_fx_cnh.py`，以草稿为底）：`redate_fxcm(rows, now_bj)` 与剑酒青丘参考同签名同口径——周日至周四起点记次日、周五周六残根丢弃；补 (a) 北京 T+1 07:00 前没走完不写（按 UTC+8 绝对时刻判，不依赖本机时区）；(b) Doctor 2026-11-16 裁「单边报价拒写，与参考一致」（实测 2024-01-01～2026-11-16 共 893 根单边 0 次，买卖价差中位 36 点、最大 105 点）；(c) `parse_ymd` 严格校验（8 位 ASCII 数字且格式化回去等于原串），坏日期整批不写，`--from` 同样校验。查询起点前推 3 天、按北京日 ≥ start 过滤。新测试 `烛照九阴/tests/test_fetch_fx_cnh_redate.py` 23 条（首版 17 条，复验后补 6 条；含与参考实现 2023-12-25～2026-12-31 在四个时刻逐日一致；参考件不在场则跳过该条）。
- **库**：先备份 `Database/烛照九阴/_bak/recap.db.bak_2026-11-16_fx-redate`（`.backup`，integrity ok，sha256 `e6a8b836…`）；单事务内删 `source='tushare'` 136 行（20260610～20261115）并按新口径重灌 114 行（北京日 20260610～20261116），周末行 0；再跑一次 `fetch_fx_cnh.py --from 20260610`，值逐行不变。与 `market_data.cn_liquidity_daily.usdcnh_spot` 共同 113 日、差值超过 0.6 点的 0 个。dim1 58 行未动。
- **回补文件**：`风险日报/data/temp_backfill.jsonl` 重生成（旧版备份 `data/_bak/temp_backfill.jsonl.bak_2026-11-16_fx-redate`）。定稿日 134 个里汇率分子变 71 个、综合值变 39 个，其余五个分子 0 差异；定稿线仍 2026-11-12。（含两个暂定日在内全 136 天为汇率分子变 73 个、综合值变 40 个，与撤回时复验推演的「73 个」一致；暂定日 11-16 另有油价 54→51，是布伦特当日行 22:00 被改写，与本修复无关。）
- **核验**：`ops/verify_marginal_e2e.py` 首跑 F3 PASS，但 **G1 FAIL**——`docs/2026-11-15-六七月行情复盘基线.md` §4 逐日表是旧口径算的，76 天里 37 天汇率分子、23 天综合① 不同（最多差 3）。Doctor 2026-11-16 裁「§4 表改新值、旧值进勘误」：§4 的 37 行只改 ①、②、汇率 三列（② 按 (六分子和+79)/7，原表 76 行用旧回补逐行复算均一致），文末加 §13 勘误（逐行原值→新值；§3、§4 统计行、§6、§9、§10 正文不改，按新口径的派生数字列在 §13.2、§13.3）；核验脚本未动。复跑 35 PASS / 0 FAIL。`test_temp_history.py` 通过。
- **口径变化带出的事实（待 Doctor 看）**：新口径下 05-06～08-14 综合① 最高 65（05-06），06-22 由 66 变 64；综合高危线 66 是按 06-22 的 66 定的（风险日报仓 `2e8fdd9`），按新口径窗口内没有一天到 66。是否调整归 Doctor。
- **下游核对**：风险日报 `build_risk_daily.py` 汇率分子——样本由 194 行变 172 行（去掉周末行），7 日变动按日历取不受影响；现库读数：分位 5→3、7 日变动 −0.0017→−0.0047、震动 2→5，最新一行由 20261115（周日标、盘中）变 20261116。`temp_history.py` 已随回补重算。烛照 `gen_daily_report.py` 近 7 行：不再出现周六周日日期；定时班北京凌晨 02:04 跑时北京 T 那根没走完，最新一行是 T−1 的完整 K 线（旧口径同样标 T−1，但实为 T 的盘中值），F5 汇率腿年龄护栏不受影响。烛照 `calibrate_risk_factors.py` 是手动只读工具：旧数据按「≤D」取汇率实为北京 D+1 那根，有一天前视；新数据只剩隔夜（北京 D 那根 D+1 06:00 才收），已出的校准报告按旧口径。白泽 `fetch_cn_inputs_tushare.py` 只在文档字符串里写了 usd_cny 可取自该表，代码不读，无影响。风险日报 `envelope_emit.py` 只查 `emotion_cycle` 日期，无影响。风险日报 `ops/replay_composite.py`、`replay_composite_v2.py` 从现库重算，已提交的 R18 回放报告数字按旧口径、现库复现不出（未重跑）。剑酒青丘 `outputs/audit_wuyin_ks50_20261017.py` 是一次性审计脚本，未核。实施者漏核、复验补出：EAL 回测 `secondary_bands_20261116/freeze_inputs.py`（见下「隐患」①）。
- **独立复验（2026-11-16 · 未参与实施的 subagent，全程只读）**：PASS_WITH_LIMITS。脚本与参考实现在 1840 个时刻、2023-12-28～2027-01-02 逐日 0 不一致；库内 tushare 114 行＝区间内全部工作日，与 Tushare 实时重标 0 不一致，与 `usdcnh_spot` 共同 113 日 0 不一致（旧口径同口比对 91 日里 90 日不一致）；dim1 与其余 34 张表与备份逐表哈希相同；回补对现库重算 0 差异；核验 35/0。查出的实错：§13 勘误漏列 §9、§6 与 §10 算术事实的新口径数字，「没改的」一句漏了 §6、§9，且误称 §4 汇率列有触发态——已重生成 §13（补 §13.3），G1 仍 PASS；6 处测试空档已补 6 条测试（共 23 条），对应 6 个变异全部抓住。这两处订正已送同一审核者增量复验（结论见下行）。
- **增量复验（同一审核者）**：基线文档 PASS（§13 之前正文与上一版逐字相同，§13.3 数字逐项重算全对）、测试 PASS（23 条无假阳性，27 个变异抓住 24 个；未抓住的 3 个里 2 个是两道日期校验互为冗余的等价变异，1 个是「默认当前时刻用错时区」无测试钉住，代码现为 `datetime.now(BJ)`，低风险）。审核者另指出 §3 表 07-06 档位应由警戒翻为平静而 §13.2 未写明——已补一句（只此一行，未再送审）。审核者判断已登记的四项隐患都不会让 2026-11-17 的班次出错（推断）。
- **复验指出、本场未处理的隐患**：① 另一会话的 EAL 回测 `Projects/Financial/风险日报/research/backtest/secondary_bands_20261116/freeze_inputs.py`（2026-11-17 自 EAL 迁入） 在 22:48:07 冻结输入，比重灌（22:51）早 3 分钟，`Projects/Financial/风险日报/research/研究材料/raw/2026-11-16-secondary-bands/inputs.json` 与其 `results.json` 是旧口径汇率（含 23 个周日行），需告知该会话；② 风险日报留存 `data/temp_history.jsonl` 唯一一条（数据日 11-16）汇率分子 7 是旧口径（新口径 3），综合取整同为 22，会作为 11-17 的 1 日、约 11-23 的 5 日、约 12-14 的 20 日边际参照；③ 手动跑 `--backfill-dim1` 会插入 3 个以前被旧周日 tushare 行挡住的 dim1 周日行（20260726、20260830、20261011），存量 dim1 另有 15 个周日行（不在本场范围）；④ 脚本只请求一次，远早的 `--from` 可能撞接口单次行数上限（参考实现按年分段），现 140 根无碍；⑤ 坏日期报错会让烛照日报班「任一步报错不放回」，当班 recap.db 不写回（Doctor 所批「宁停不写错日期」的代价）。
- **预防门禁**：上述 23 条测试；凡改数据口径（日期、单位、去重），代码、历史迁移、下游定稿文件与冻结基线同场做完（G-X268 同族实例）。

## [NOTE-20261116-002] 外汇交易中心的几条历史接口是滚动短窗：DR007 全天加权值断采超过三个月就补不回来

**状态**: ⚠️ 已知风险
**优先级**: 🟡 中
**触发场景**: 2026-11-16 数据源实测，找 DR007 全天加权值与一年期同业存单收益率的历史。
**硬证据/最小复现**: `…/data/currency/prr-chrt.csv`（DR001、DR007、DR014 走势文件）只有 2026-08-13～2026-11-13；`/ags/ms/cm-u-dlrp/PrDlyBltn`（回购日报按日期查）返回 `startDate: 2026-11-02`，查 2026-06-22 为 0 条；`/ags/ms/cm-u-bk-currency/ClsYldCurvHis`（收盘收益率曲线）2026-08-03 有值、2026-07-10 及更早 0 条。能回溯多年的是 `FrrHis`（回购定盘利率，2017-06 已有 FDR007）与 `CcprHisNew`（中间价，单次查询限一年内）。
**根因**: 这些是网站页面自用的数据地址，不是对外承诺的数据服务，只保留页面展示需要的窗口（推断）。
**影响面**: `cn_liquidity_daily` 的 `dr007`、`dr001` 两条序列只能从 2026-08-13 起逐日累积，目前 63 行，不足以算分位；装班前或班停超过三个月，中间的日子永久缺失。回放窗口（04-27～08-15）拿不到 DR007 全天加权值。
**修复/建议修法**: Doctor 2026-11-16 裁：定盘利率 FDR 承担历史与分位，页面如实标 FDR；DR 全天加权值并列显示并逐日累积。装班后把这两条序列的行数增长列入日常自检。
**预防门禁**: `fetch_dr` 的列位自检（走势文件最新一日的 DR007 必须等于同日日报里的加权利率，否则拒写）；读数模块对历史不足 120 个观测的读数不给档位。
**来源**: 2026-11-16 本场实跑；实测表第 1 节 R5 各行。
**追记（2026-11-16 真实库回补后）**: 同根复发一次。库副本首次取数时走势文件起点是 2026-08-13（63 行）；Doctor 回补真实库时起点已滚到 2026-08-17（62 行），08-13、08-14 两日的 `dr007`、`dr001` 真实库永久没有。硬证据：两库 `cn_liquidity_daily` 逐键比对，只在库副本的键正是这 4 行（另 1 行是只有最新值的掉期点）。连带实错：CC 把「2026-08-13」写死进了读数模块的展示说明、回放报告正文与实测表，回补后与真实库不符——已改为按库实读（`cn_liquidity.py`、`ops/replay_cn_liquidity.py`），报告按真实库重出。预防：滚动窗口数据源的起止日一律从库里读，不写进代码与正文；交付用的回放报告以真实库为输入生成，库副本版只作开发期核对。

## [NOTE-20261116-003] 政策利率在 2026-11-02 换锚：凡写「相对 7 天逆回购利率」的读数，此后没有锚

**状态**: ⚠️ 已知风险（本项目新读数已按 Doctor 裁定分段；其他项目里若有同类写法未查）
**优先级**: 🟡 中
**触发场景**: 2026-11-16 读央行公开市场业务交易公告原文，为「DR007 相对 7 天逆回购政策利率的偏离」找政策利率序列。
**硬证据/最小复现**: 公告〔2026〕第 210 号（10-30）仍是「7 天 1.40%」固定利率、数量招标；第 211 号（11-02）起为「隔夜 1.25%」固定利率、数量招标，7 天期改为「固定数量、利率招标、多重价位中标」，不再公布单一利率（第 220 号，11-13）。隔夜逆回购自 06-29（第 123 号）起已与 7 天期并行操作，当时公告不写利率。新华社 11-02 报道称之为政策利率换锚；央行 10-30 的换锚公告原文本场未读。
**根因**: 货币政策操作框架调整，属外部事实变化。
**影响面**: PRD R5 原文写的是 7 天口径。Doctor 2026-11-16 裁：10-30 及以前 7 天对 7 天，11-02 起隔夜对隔夜（FDR001 减隔夜逆回购利率），分位在拼接序列上算并标「跨口径」。隔夜口径至今只有 11 个观测。
**修复/建议修法**: 已在 `cn_liquidity.policy_anchor` 实现「哪条固定利率最近一次出现就以哪条为锚」，政策利率最多沿用 15 个公告日。若央行再次调整操作方式而新的固定利率没有出现（例如隔夜也改为利率招标），旧利率会被沿用最多 15 个公告日并照给档位（2025-01 以来两次固定利率之间的最大间隔是 9 个公告日，所以不能设得更短），沿用超过 3 个公告日时页面写明「政策利率沿用某日公告」；第 16 个公告日起读数停更，再过 3 个交易日显示降级。原稿写「不会沿用旧锚」是错的，独立复核用删去全部隔夜利率行的办法证伪后改正。
**预防门禁**: 测试 `RateDeviation.test_anchor_switches_to_overnight_leg`、`test_policy_rate_carried_at_most_15_notice_days`；公告解析器遇到不认识的写法报错而不是记 0（`OmoParser.test_unknown_notice_raises_not_zero`）。
**来源**: 2026-11-16 本场实读央行官网公告 463 个公告日（2025-01-02～2026-11-16）。

## [NOTE-20261116-004] 取数接口的四处非预期行为（国内流动性取数脚本首跑暴露）

**状态**: 🔄 已在取数脚本内处理，待独立验收
**优先级**: 🟢 低
**触发场景**: 2026-11-16 `fetch_cn_liquidity.py` 在临时库副本上首次回补 2025-01-01 至今。
**硬证据/最小复现**: ① 央行公告 2025-03-24 及更早的表头是「期限、操作量、操作利率」，金额在前、利率在后，首版解析器在这一篇报 `正文未写期限且无法与表对上` 并停下。② 雅虎 `CNH=X` 一年窗只返回 1 个点，接口自报 `validRanges: ['1d','5d']`，没有历史；`CNY=X` 有。③ Tushare `fund_share` 的 `fund_type` 列在 2025-01-06 对沪市 556 行为空、只有 53 行标 ETF，按该列筛 ETF 会让 2025 年初的沪市覆盖面缩到一成。④ Code 标签沙箱里 `ts.set_token()` 要往主目录写 `tk.csv`，报 `PermissionError`；`ts.pro_api(token)` 直接传参不落文件。
**根因**: 各源自身的历史格式与数据缺口；④ 是沙箱只允许写工作目录。
**影响面**: 只影响新取数脚本。①②③ 若不处理分别导致：早期公告全部解析失败、离岸序列为空、ETF 净申赎在 2025 年初严重低估。
**修复/建议修法**: ① 解析器补第二种表格写法；② 离岸改走 Tushare `fx_daily`；③ ETF 名单改以 `fund_basic` 为准（场内、股票型、名称含 ETF）；④ 脚本走 Tushare 的 HTTP 接口，不调用 `set_token`。
**预防门禁**: `test_fetch_cn_liquidity.py` 的 `OmoParser.test_old_table_layout_amount_before_rate`、`Parsers.test_etf_net_creation_and_split`；`etf_count` 序列逐日记录计入只数，覆盖面突变可见。
**来源**: 2026-11-16 本场实跑；实测表第 6 节。

## [ERR-20261116-005] 国内流动性取数与读数：独立复核查出的六处实错（雅虎在岸汇率日期与质量、真实库开关可绕过等）

**状态**: 🔄 已修待验（2026-11-16 同日修；复验与 Doctor 功能验收未完成）
**优先级**: 🟡 中
**触发场景**: 2026-11-16 第二段实施完成后，未参与实施的 subagent 做独立复核（PASS_WITH_LIMITS），全程只读，注入 73 个变异，抓住 59 个。
**硬证据/最小复现**: ① 雅虎 `CNY=X` 日线：`fetch_fx` 用接口当前的 `gmtoffset` 给全部历史标日期，英国夏令时段的时间戳是前一日 23:00 UTC，被标早一天；库副本里该序列周日 59 行、夏令时段 278 个 A 股交易日有 54 天无值。改对后与离岸序列日变动相关性仍是同日 −0.06、错后一日 +0.46（在在岸、离岸、中间价三条序列都有值的 443 个交易日上算；复验者在 483 个交易日上重算得同日 −0.06、错后一日 +0.38，方向一致），且 483 日里有 25 天出现毛刺（口径：单日变动超过 120 点且次日反向变动超过 80 点；复验者按「单日超百点且次日回吐过半」数得 26 天）。② `is_real(Path('…/Market-Data/MARKET_DATA.DB'))` 返回 False 而 `os.path.samefile` 为 True，不带 `--real` 就能写真实库且不取锁。③ `bond_treasure_issue_cninfo(start_date='20260612', …)` 里缴款日 06-22 为 0 行，起点放到 0601 才有 700 亿；配合先到为准，短窗口日更会把残缺的日合计写死。④ 回放报告写「顺延用的是公告日序列」，实际回放日之后按周一至周五近似，3 个回放日的「未来 7 日到期量」因此多计（04-27 为 2350 对 115）。⑤ 并列的 DR 全天加权值陈旧时没有任何标记，且可能与主读数不是同一口径腿。⑥ 长假期间参照日历按周一至周五补，读数被误标降级，说明文字「落后 N 个交易日」不属实。
**根因**: ① 实施者没有按星期分布检查过取回的序列，也没有拿第二条序列对过日期；「两者收盘时点相差约 2–3 小时」是没核过的话。②③ 联网取数函数没有离线测试，边界只在一次性全量回补下跑过。④⑤⑥ 证据栏与报告里的说法先于实现写成。
**影响面**: 真实库尚未回补，无生产影响。若带着 ① 回补，在岸与离岸减在岸两条读数整段错位，回放外汇两行失真。
**修复/建议修法**: ① Doctor 2026-11-16 裁外汇端改用中间价：在岸即期与离岸减在岸显示「数据源缺失」，另出人民币中间价与离岸减中间价；雅虎序列默认不取，日期换算改按交易所时区。② 判定改为同一文件即算并按目录名兜底。③ 查询起点前移 60 天后按缴款日截取。④ 改正报告并列出 3 日差异；页面口径写明长假前会多计。⑤ 并列值只在同腿时显示，陈旧写「已陈旧」。⑥ 说明文字写清哪几天是按周一至周五计的；误标降级本身未消除（没有未来节假日表）。
**预防门禁**: 取数测试 `test_yahoo_bars_dated_in_exchange_timezone`、`test_real_db_is_recognised_through_other_spellings`、`test_govbond_query_starts_60_days_earlier`、`test_margin_buy_needs_both_main_exchanges`、`test_yahoo_onshore_group_is_not_fetched_by_default`；读数测试 `ReviewRegressions.*` 六条；`test_replay_cn_liquidity.py` 四条；核验 D1p、D4p、G4（页面层）。新接一条日频序列时，先看它按星期的行数分布，再拿一条已知可靠的序列做领先滞后检验。
**来源**: 2026-11-16 独立复核回报（实错 1–8、未抓住的变异 14 个）；本场复核实与修复。
**复验（2026-11-16 · 同一位未参与实施的审查员）**: PASS_WITH_LIMITS——8 条里 6 条已修复，实错 3、实错 6 为披露到位、近似未改；首轮未抓住的 14 个变异现抓住 11 个；针对修复新注入 27 个抓住 21 个。复验另指出三处文档失实（相关性数字的样本没写、「仍未被测试抓住」清单过满、PRD 里一处「十四行」未改），已订正。复验之后补了四处测试钉子（离岸滞后与价差配对、备选误报口径、页面模板 class 白名单），这一小步未经独立复验。**仍未被任何测试抓住的变异**：DR 列位自检被去掉、中债曲线名不核对、`fetch_govbond` 仍用 `--from` 当查询起点（三处都在联网函数里）、到期量口径说明删掉「长假前会多计」、回放报告不列出与全日历不同的回放日。状态维持 🔄（功能验收归 Doctor）。

## [NOTE-20261116-006] 国家统计局网站有请求量防护：一小时内约 180 次请求后，列表页返回人机校验页（HTTP 200）

**状态**: ⚠️ 已知风险（取数脚本对列表页与稿件页的校验页都已识别，不绕过；稿件页这一半是独立复核指出后补的，见 ERR-20261116-010）
**优先级**: 🟡 中
**触发场景**: 2026-11-16 国内宏观读数第三段。为取 CPI、PPI 的发布日期，先探测翻了 28 页「最新发布」列表、抓了 50 篇稿件，随后取数脚本首跑又翻 28 页、抓 44 篇；紧接着复跑时第 1 页就解析不出条目。
**硬证据/最小复现**: `fetch_cn_macro.py` 复跑报 `FetchError: 国家统计局列表第 1 页解析不出条目`，退出码 1。直接请求 `https://www.stats.gov.cn/sj/zxfb/index.html` 得 HTTP 200、约 37KB、正文是 `Please enable JavaScript and refresh the page`，响应头带 `WZWS-RAY`；正常页面约 66KB。约十五分钟后单次复测恢复正常。央行网站同期翻了 39 页加约 60 篇稿件，未被拦。
**根因**: 网站防护按请求量触发（推断：阈值与时间窗未知，只知道本场约 180 次请求后触发）。HTTP 状态码仍是 200，不看正文会把校验页当成「列表改版」。
**影响面**: 只影响取数脚本的 price 组（CPI、PPI 发布日期与首发值）；money 组不受影响，已入库的行不受影响。首次全量回补请求量最大（约 28 页列表加 44 篇稿件），最容易撞上。
**修复/建议修法**: 已在脚本内处理：列表页是校验页则该组本轮失败并写明「不取、不绕过、过一阵重跑」，稿件页是校验页或取不到则那个月本轮不写、退出码 1、下轮再取，校验页不落缓存；对统计局的请求间隔由 0.25 秒放到 1 秒；库里已有的月份不再重取，复跑只读列表首页。回补命令带 `--cache-dir` 指到本场已抓好的稿件缓存，可再省 44 次请求。撞上了就等一阵重跑，重复执行无害。
**预防门禁**: 取数测试 `Parsers.test_challenge_page_is_recognised_not_parsed`、`MainSafety.test_rerun_passes_known_months_and_no_new_month_is_ok`、`test_empty_source_fails_and_keeps_existing_rows`（源返回空不当成「没有新数」）。给官网写抓取时，先定请求间隔与「已有的不重取」，再跑全量。
**来源**: 2026-11-16 本场实跑（探测脚本与取数脚本两次运行的输出、响应头）。

## [NOTE-20261116-007] Tushare 宏观接口不给发布日期，给的是取数时的现行值而不是首发值

**状态**: ⚠️ 已知风险（新表已把首发值单存一列，回放优先用首发值）
**优先级**: 🟡 中
**触发场景**: 2026-11-16 国内宏观数据源实测。回放必须按发布日期截面，先查 Tushare `cn_cpi`、`cn_ppi`、`cn_m`、`sf_month` 有没有发布日期字段。
**硬证据/最小复现**: 四个接口返回的字段只有所属月份（`month`）与数值，没有发布日期。与央行、统计局官网首发稿逐月对照（2024-12 至 2026-10 数据月）：M2 同比 23 个月全等；M1 同比 2024-12 首发稿是 −1.4%、Tushare 是 1.2%（央行自 2025 年 1 月数据起启用新修订的 M1 口径，稿件注 4 原文）；社融存量 23 个月里 8 个月差 0.01 至 0.02 万亿元；社融累计增量 2025-06 首发稿 22.83 万亿元、Tushare 22.8588；`sf_month` 2026-10 的 `inc_month` 是 11429，而累计值 10 月减 9 月是 11500。另：金十数据的发布日序列（akshare `macro_china_cpi_yearly` 等）停在 2025-08，不能用。
**根因**: Tushare 存的是数据的最新版本（推断），口径变更与事后订正会回写历史月份。
**影响面**: 任何拿 Tushare 宏观数做回放、回测的地方，都会用到当时并不存在的数；同比类影响小（本场窗口内全等），水平与增量类有订正。
**修复/建议修法**: `cn_macro_monthly` 设 `release_date`（官网发布列表日期，必填）与 `first_release`（官网首发稿正文数字，可空）两列；读数模块回放时优先取首发值，取不到才用现行值并标出；社融当月新增首发稿通常只给累计值，该项首发值为空，回放报告已写明。
**预防门禁**: 取数测试 `Assemble.test_money_first_release_differs_is_kept_both`、`test_price_without_release_date_is_not_written`；读数测试 `PointInTime.*` 三条。新接月频或季频数据时，先问「发布日期从哪来」「取到的是不是首发值」。
**来源**: 2026-11-16 本场实跑；`Projects/Financial/风险日报/docs/2026-11-16-国内宏观数据源实测表.md` 第 2、3 节。

## [ERR-20261116-008] 工作区就是生产：未提交、未验收的构建器改动被当天的定时班直接跑进了生产页面

**状态**: ⚠️ 已知风险（Doctor 2026-11-16 选择窗裁「保留，回补后自然显示」）
**优先级**: 🟡 中
**触发场景**: 2026-11-16 第三段页面接入。07:18 PST 在工作区改了 `build_risk_daily.py`（新增国内宏观读数区块，24 行）并放入 `cn_macro.py`，当时尚未独立复核、未提交。
**硬证据/最小复现**: `refresh-risk-daily` 班 09:07–09:18 PST 照常运行，`data/risk_snapshot.json` 与 `dashboard/risk-daily.html` 的修改时间是 09:18:55；生产快照里已有 `cn_macro`，`status=unavailable`，原因 `OperationalError: no such table: cn_macro_monthly`；生产页面含 `id="mq-row"`，显示「◌不可判 · 本轮不可用，其余读数不受影响」。综合温度与各触发态不受影响（端到端核验 A2、A3：接入前后同输入逐项相同）。托管页是否已随班推送未核。
**根因**: 定时班直接运行项目目录里的构建器，项目目录同时是开发工作区；没有「开发副本」与「生产目录」的隔离。前两段同样暴露在这个风险下，只是恰好没撞上班的时刻。
**影响面**: 任何在班运行前落进工作区的未验收改动都会上线。本次落进去的是信息层区块的「不可用」占位，按设计不阻塞、不改判定字段；若是会抛异常或改判定的改动，后果不同。
**修复/建议修法**: 本次按 Doctor 裁定保留，真实库回补后下一次构建即显示数值。往后改构建器这类生产入口文件，要么避开 09:08 PT 前后，要么先在副本里改完验完再一次性放进工作区；长期可考虑让班从已提交的版本运行（方向性改动，未提案）。
**预防门禁**: 动构建器之前先看当前时刻与班的时间表；接入类改动一律走「失败不阻塞」的写法并有注入失败的核验（本段 `ops/verify_cn_macro_e2e.py` E1–E5）。
**来源**: 2026-11-16 本场实读（文件修改时间、生产快照与页面内容）。

## [NOTE-20261116-009] 端到端核验脚手架的三个坑：基线默认取 HEAD、页面脚本截取段互相误伤、检索探针先漏后误

**状态**: 🔄 前两项已绕过，第一项的默认值未改（属第二段文件）
**优先级**: 🟢 低
**触发场景**: 2026-11-16 第三段接入后重跑第一、二段的端到端核验，并新写第三段核验。
**硬证据/最小复现**: ① `ops/verify_cn_liquidity_e2e.py` 的 `--before-ref` 缺省是 `HEAD`；第二段在 `12943ea` 提交后，HEAD 的构建器已含 `cn_liquidity`，不带参数运行会以「不是接入前的版本」退出，须显式给 `--before-ref ef08963`（本场照此运行，PASS 45 / FAIL 0）。② 第一、二段核验都把页面脚本从各自的注释标记截到 `// === 小卡渲染 ===`；新区块脚本首版插在这两者之间，落进了第二段 G4 的 class 白名单检查范围，新写法 `${r.cna?'na':''}` 不在白名单里。③ 第三段核验的「取数只有一处」检索，首版正则只认 `"接口名", {` 这一种写法，取数脚本改用 `_ts_nonempty(token, "cn_cpi", …)` 后一处都没认出（报 0 处）；放宽后又把核验脚本自己数了进去。
**根因**: ① 基线用了会随提交移动的引用；② 多个核验共用同一个结束标记；③ 探针只按当时的一种写法写，没有先拿「应当命中」与「应当不命中」的样例自检。
**影响面**: 只影响核验脚手架。① 不处理的话，第二段核验的文档命令在提交后不可直接重放。
**修复/建议修法**: ① 第三段核验的缺省基线钉成具体提交 `12943ea`；第二段那一处缺省值建议同样钉成 `ef08963`（未改）。② 新区块脚本移到 `// === 小卡渲染 ===` 之后、`// === 传导连线` 之前，不进前两段的截取范围。③ 正则改为两种调用写法都认，排除测试与核验脚本自身，并用观星脚本改动前后的两个版本做了命中与不命中的自检。两份既有核验脚本各加了一处忽略键 `cn_macro`（各 2 增 1 删）。
**预防门禁**: 新核验脚本的基线一律写具体提交；检索类检查先造一正一反两个样例跑通再用。
**来源**: 2026-11-16 本场实跑。

## [ERR-20261116-010] 国内宏观取数、读数与回放：独立复核查出的六处实错与七处文档失实

**状态**: 🔄 已修待验（2026-11-16 同日修；Doctor 功能验收未完成）
**优先级**: 🟡 中
**触发场景**: 2026-11-16 第三段实施完成后，未参与实施的 subagent 做独立复核（PASS_WITH_LIMITS），全程只读，注入 106 个变异，抓住 83 个。
**硬证据/最小复现**: ① 中：`fetch_cn_macro.py` 的 `fetch_price` 里稿件页取不到或返回人机校验页时走 `except FetchError: first = None`，结果写入一行 `('202610', 0.7, None, '20261109')`，说明文字还写成「首发稿句式未登记」，入口退出码 0；网站恢复后复跑因「库里已有的月份不重取」而永远不补。`fetch_money` 取稿件时没传 `reject`，校验页超过 2000 字节会被写进缓存一直复用。② 低：「源返回空不当成没有新数」按组判——同组 CPI 有数、PPI 源返回空而库里有旧行时，输出「ppi_yoy 无新月份」、退出码 0。③ 低：社融存量同比稿件认不出时退出码仍是 0，装班后调度方看不见。④ 低：回放报告的计数几乎没有测试钉住，回放脚本 21 个变异漏 11 个（持平算进为正、未回撤计数取反、均值取成末值等）。⑤ 低：`ensure_table` 用 `executescript`，在事务之外先提交，首次写入中途失败会留下空表。⑥ 低：`cn_macro.compute(today="2026-11-16")` 传带横线的日期串时六项静默变成缺数。文档失实：实测表里 2026 年央行发稿时刻按稿件编号推断，全错（页内发布时间 22 期里 21 期不早于 15:00 收盘）；回放报告据此写「多在下午盘中或收盘后」过轻；三处行号在文件被别人增改后漂移；实测表「86 行」实为 85；NOTE-20261116-006 状态栏与 PRD「写前快照」两处说得过满；M1 同比标慢变量的依据「逐月变动幅度小」与数据相反（22 个月逐月变动绝对值均值 0.87 个百分点，五条同比里最大）。
**根因**: ① 写「稿件取不到时发布日仍可用、首发值留空」时，没有想到它与「已有月份不重取」「先到为准」合在一起会让空值永久化；联网函数当时没有离线测试。④ 报告由脚本内联算数，没有可单测的函数。文档失实的共同点是把没核过的推断（稿件编号等于发稿时刻、逐月变动小）写成了事实。
**影响面**: 真实库尚未回补，无生产影响。若带着 ① 回补又撞上网站防护，会以退出码 0 写入永久缺首发值的行，回放退回现行值。央行发稿时刻一处影响回放的读法：窗口内四次发布都在收盘后，按「收盘前可得」口径生效交易日应顺延一天。
**修复/建议修法**: ① 稿件取不到或被拦的月份本轮不写，记为「未写完」并让入口退出码为 1；央行稿件同样加校验页识别，校验页不落缓存。②「无新月份」改按序列判。③ 社融存量同比认不出、发布列表缺期、发布日期冲突都记为「未写完」，退出码 1。④ 把计数抽成 `event_stats`、`window_mean`、`vintage_counts`、`switches` 四个函数并补测试；复核漏掉的 11 个变异现全部抓住（自注 15 个抓住 15 个）。⑤ 建表改为在写入事务内逐条执行。⑥ 参照日统一去横线并校验，写法不对整块不可用。文档：实测表改用页内发布时间；回放报告事件表加「发布时刻」一列、第 5 节写明四次央行发布均不早于收盘；行号改为按引文检索；M1 的依据句改成如实说法并在登记表里提请 Doctor 留意。未做：对已入库的空首发值补值（先到为准不改写，句式未登记留下的空值要人工处理）；按「收盘前可得」口径另算一版回放。
**预防门禁**: 取数测试 `FetchOffline.*` 10 条（联网函数的离线测试：稿件被拦、取不到、句式不认识三种情形分别断言）、`Assemble.test_article_unavailable_month_is_not_written_and_is_incomplete`、`MainSafety.test_incomplete_months_give_exit_1_but_other_rows_are_written`、`test_no_new_month_is_judged_per_series_not_per_group`、`WriteGuards.test_first_write_failing_leaves_no_empty_table`；读数测试 `Fields.test_reference_date_spellings`；回放测试 11 条。写「取不到就留空」这类降级分支时，先问它和「不重取」「不改写」合在一起会不会把空值钉死。发布时间一类事实，以页面自己写的为准，不从编号、文件名里推。
**来源**: 2026-11-16 独立复核回报（实错 1–6、文档失实 1–7、未抓住的变异 23 个）；本场复核实与修复。
**复验（2026-11-16 · 同一位未参与实施的审查员）**: PASS_WITH_LIMITS——6 条实错全部判「已修复」，首轮最小复现与 6 个邻近情形均按新语义表现，文档订正逐项属实；首轮漏掉的 23 个变异重注抓住 17 个，针对修改新注入 53 个抓住 45 个。复验新指出五处低级问题：① 这次修改引入的新错——金融组在判断「库里是否已有」之前就把发布列表的日期冲突记成「未写完」，四条序列都已在库的月份遇到央行重挂同名稿时，每次复跑退出码都是 1；② 同类残余——稿件地址返回一张带标题、不含校验页标志句的拦截页时，仍被当成稿件，写入空首发值并落缓存；③ 回放第 5 节的句子只数了收盘后的次数却写「全部」，换个窗口会失实；④⑤ 两处文档小失实。已修：① 已在库的月份日期冲突只记说明；② 取回的页面里须有发布列表上的那个标题，否则按取不到处理、不落缓存（本机缓存的 82 篇真实稿件全部通过）；③ 改成「核到的 N 次里有 K 次不早于收盘」。补测试 `Assemble.test_date_conflict_on_already_stored_month_is_a_note_not_incomplete`、`FetchOffline.test_block_page_without_the_marker_sentence_is_not_taken_as_the_article`、`test_cached_challenge_page_is_refetched_not_reused`、`MainSafety.test_dry_run_with_incomplete_months_exits_1`。**这一小步未经独立复验。**仍未被测试抓住的：首轮遗留的 6 个接近等价的变异；同一条序列同时打印「无新月份」与「未写完」的文字矛盾未改。教训补一条：修一个分支时，把同一函数里别的分支对同一状态（这里是「库里已有」）的处理顺序一起看，不然修出不对称。状态维持 🔄（功能验收归 Doctor）。

## [ERR-20261116-011] 综合方式候选规则登记：量分把两项机械正相关的读数反向相加，总闸按构造几乎不触发
**状态**: ⚠️ 已知风险（v1.0 结果原样保留；是否另立新版待 Doctor 裁）
**优先级**: 🟡 中
**触发场景**: PRD 2026-11-15 第五段 R18。事前登记候选综合方式时，把量分定义为「未来 7 日逆回购到期量的分位」与「100 减近 5 日净投放的分位」的平均，本意是落实「到期量要扣续作」。
**硬证据/最小复现**: `Projects/Financial/风险日报/docs/2026-11-16-综合方式回放比较.md` 第 4 节资金状态表——检验窗 236 个交易日，「量价同高」在 60、75、90 三档门槛下均为 0 天；四种方式进入高档 0 次。独立复核的事后诊断：库内可算的 332 天里两项分位相关 +0.57；到期量分位 ≥75 的 77 天中净投放分位 ≤25 的 2 天、≥75 的 48 天；「未来 7 日到期量」与「近 5 个工作日毛投放」在 459 天里 297 天完全相等。
**根因**: ① 逆回购以 7 天期为主，未来一周的到期量本身就是过去一周的投放量，到期量高时净投放通常也高；把它与「净投放的反向」取平均，两项相互抵消。② 登记前没有先看这两项读数在定义上的关系，只看了它们各自的含义。③ 冻结前已有的数字（见顶两周到期量分位均值 92、净投放分位均值 78，量分约 57）已经指向这一点，实施者只看了价分那一行。④ 另一处：登记第 0 节写「没看过 8 月之后的综合温度」，而 `data/temp_backfill.jsonl` 早已含这段数据——「没看过」的陈述没有先查项目里有没有现成产物。
**影响面**: R18 的回放不能区分候选与现行；检验窗（2025-07-04 至 2026-10-19）已被看过，同一批读数的新版规则只能在此后新增的交易日上做事前检验。未进生产，页面与判级未变。
**修复/建议修法**: 不改 v1.0。若另立新版：量的一侧只用一项不与续作机械绑定的读数（如净投放本身，或到期量减去同期已公告的续作量），或直接用价的一侧；登记前先在「与检验无关」的层面核对所选读数之间的定义关系（恒等、差分、同源），并把冻结前能由已知数字推出的各分项取值逐项写给 Doctor。
**预防门禁**: 登记候选规则前的检查单三条——所选读数两两之间有没有定义上的恒等或差分关系；由已看过的数字能推出的每个分项取值都列出来；声称「没看过」的每一类数据先在项目里检索有没有现成文件。测试 `test_replay_composite.py` 32 条钉住的是规则实现，钉不住规则设计。
**来源**: 2026-11-16 主会话；独立复核回报「结构性问题的诊断」与「过满或失实的措辞」第 1 条；登记文件第 9 节。

**追记（2026-11-16 · v2.0 · 同根复发：冻结前的自查仍没查到结构性问题）**: 按上面三条检查单自查后冻结 v2.0（量分只用净投放的反向分位，价分改用 `rate_dev` 5 日变化的分位），说明窗回放后独立复核又查出三处：① 2026-11-02 政策利率换锚使 `rate_dev` 水平跳升约 8 个基点，其后 5 个交易日的 5 日变化跨两种口径，门槛 75 的 9 个同高日有 4 个、门槛 90 的 2 天全部来自这次拼接；② 量分 ≥75 的 89 天里 68 天落在每月 3 至 12 日，是月内日历变量，与价分的月末节奏反相；③ 换锚后操作以隔夜为主，5 日净投放对隔夜腿恒等于操作量的 5 日差，检验窗里的量分已换了含义。**硬证据**: `Projects/Financial/风险日报/docs/2026-11-16-综合方式候选规则登记-v2.md` 第 9 节；`docs/2026-11-16-综合方式回放比较-v2.md` 资金状态天数表下的「落在跨换锚日的同高天数」。**根因**: 自查只看了频次、相关与按日分布，没有按月内交易日序分桶，也没有把口径切换日前后单独拿出来看；登记里知道有换锚（写了「逐日表标出」），却没有推一步它对「变化量的分位」意味着什么。**预防门禁（补两条）**: 凡用变化量或差分作读数，先列出序列里所有口径切换日，把切换日之后一个差分窗内的值单独列出来看；凡用央行操作量、资金利率这类带固定月内节奏的序列，先按月内交易日序分桶看分布。另：冻结前送一次独立复核，只查定义与结构，不看与行情的对照。**状态**: ⚠️ 已知风险。

**追记（2026-11-16 晚 · 第三次 · 这次被冻结前的复核拦下）**: 高位状态机制登记草稿 v0.3（获利、承接、跟随）送冻结前独立复核，结论为现稿不宜冻结。实错三处：① 草稿第 1 节声明英伟达取 `intl_index_daily`，第 4 节的频次却是用 `us_anchor_daily.close_adj` 算的（起草脚本里一句「哪张表行数够就用哪张」），两表在 271 天里有 6 天状态不同；而 `us_anchor_daily` 恰有复权口径切换、来源切换与缺行，第 5 节「未发现切换日」对它不属实。② 2026-06-22「三项同时成立」依赖两个没写明的口径：分位取整（融资 60 日增幅分位原值 74.6）与使用当日融资余额（次日早上才可得）；按收盘时实际可得的数据，那天是两项，三项同时成立落在 06-23、06-24。③ 分位算法、涨幅基期、美股与 A 股日历对齐、数据晚到与缺行（`margin_daily` 缺 2026-09-30 一行）都没有写死，两个人照着实现会得到不同结果。**根因**: 起草时把「算频次的探索脚本」的口径当成了登记的口径，没有回头逐条对照；「当时可得」这一条在第一、二版回放里都做了，到状态机制上反而漏了。**处理**: 草稿不冻结，定义重写后再审；复核结论已记入决策记录同日条。**预防门禁（再补两条）**: 登记里每个数字都要能用登记写明的表和口径重算出来，起草脚本与登记条文不一致时以登记为准重算；凡是要在收盘后显示的读数，登记里逐项写明「当日显示时用哪一天的数」。**状态**: 🔄 待修复（草稿待重写）。

## [ERR-20261116-012] 核验脚本里拆分器的假 brain 目录少建 `.tools`：拆分器回落到真实 brain，覆盖了风险日报三页的真实暂存件

**状态**: 🔄 已修待验（暂存件已按发布哈希恢复；核验脚本已加隔离自检）
**优先级**: 🔴 高
**触发场景**: 2026-11-16 12:25 PST，PRD 2026-11-15 第五段 R17 的端到端核验脚本 `ops/verify_r17_e2e.py`（当时还在项目外的开发副本里）首跑。F 段照前三段核验的写法，建一个假 brain 目录、设 `BRAIN_ROOT` 指向它、对开发副本构建出的页面跑 `brain/.tools/artifact_split_risk_daily.py`。实施者抄这段时漏了 `(fake / ".tools").mkdir()` 一行。
**硬证据/最小复现**: 拆分器输出 `split ok`、退出码 0，假目录里却没有产物；真实的 `brain/.tmp/artifact-publish/{risk-daily,risk-daily-ai-alarm,risk-daily-eal-starfield}/` 下 `artifact.html` 与 `manifest.json` 的修改时间变成 12:25:11，`manifest.json` 的 `source` 是系统临时目录里的开发副本页面（`/tmp/claude-501/rd_r17_e2e_…/after/dashboard/risk-daily.html`），主页哈希 `efb06418…`，与 `published.json` 记的 `c105e451…` 不同。即：未验收的 R17 版式页面被拆进了真实暂存件。`published.json` 未被改写，托管页未被推送。
**根因**: `brain/.tools/artifact_fragment.py` 的 `brain_root()` 依次试 `BRAIN_ROOT`、会话挂载目录、`~/Documents/Claude/brain`，只认带 `.tools` 子目录的候选；`BRAIN_ROOT` 指向的目录没有 `.tools` 时不报错，直接回落到真实 brain。隔离全靠调用方记得建那个空目录，漏了也照常「成功」。前三段核验脚本各有这一行，所以没出过事。
**影响面**: 12:25 至约 12:27 之间，三页的真实暂存件是未验收的内容；这期间若有会话按 slug 从暂存件原地重推托管页，会把它推出去（未发生：`published.json` 的时间戳仍是 17:20:16Z 与 11-14）。所有「设 `BRAIN_ROOT` 跑拆分器或其他 `artifact_*` 工具」的脚本都有同样的坑。
**修复/建议修法**: ① 已做——先把被覆盖后的六个文件留证到会话暂存目录；在一个带 `.tools` 的假 brain 里对未变的生产页面（09:18:55 的构建，sha `6f4cba99…`）重跑拆分器，三页产物哈希与 `published.json` 逐一相同（`c105e451…`、`8565d441…`、`d1be339e…`）后，把这六个文件拷回真实暂存目录，回读哈希相同。`manifest.json` 是按同一原件重新生成的，覆盖前的原字节无从比对。② 已做——`verify_r17_e2e.py` 的 F 段补上 `.tools`，跑拆分器之前先用 `artifact_fragment.brain_root()` 确认解析到的是假目录（不是就停），跑完再核真实暂存件的修改时间与大小一个未动（F0）。③ 建议（未做，属 brain 工具的行为改动，待 Doctor 定）——`brain_root()` 在 `BRAIN_ROOT` 已设置却不合格时直接报错退出，不回落。
**预防门禁**: 核验脚本里凡调用会写 brain 的工具，先断言解析到的根是临时目录，跑完比对真实目录的修改时间；`verify_r17_e2e.py` 的 F0。抄脚手架时整段抄，不挑行。
**来源**: 2026-11-16 R17 实施场实跑（核验首跑日志 `Claude/临时文件/r17_dev/run1.log` 的 F1、F2 两条 FAIL；恢复前后的哈希比对在本场会话记录里）。该目录已于 2026-11-16 按 Doctor 令清理，首跑日志未留存。

## [ERR-20261116-013] R17 前置项与并读：独立复核查出旁注措辞过满、新增排版与 16 行读数共用兜底，另有五类变异核验与测试都抓不住

**状态**: 🔄 已修待验（订正后未再送审）
**优先级**: 🟡 中
**触发场景**: PRD 2026-11-15 第五段 R17，在项目外的开发副本上实施后送独立复核（未参与实施的 subagent，只读，PASS_WITH_LIMITS）。
**硬证据/最小复现**: ① 旁注首版写「两项各带固定的月内节奏……两项的口径都有变」：出处（`docs/2026-11-16-综合方式候选规则登记-v2.md` 第 9 节）没有「固定」；价的一侧出处讲的是 `rate_dev` 的 5 日变化，页面并排的是水平档位；量的一侧出处说的是「含义变了」，不是口径。② 让 `cn_liquidity._coread` 或 `_due_pre` 抛异常，`view.status` 变成 `unavailable`，整个流动性区块只剩一句不可用——新增的两行把既有 16 行一起带倒。③ 复核者 28 个变异里两边都没抓住 5 个：旁注加一句带「趋严」的话、按条件往旁注里拼「量价同高」、旁注里的日期改错、分位高于某值时换一种短标样式、详情页的前置项一节拿掉。④ 实施者自己的 14 个变异首轮全被抓住，订正后重跑发现「接入步骤改写分子」写在同一行分号后面就漏（断言只认行首赋值）。
**根因**: ① 任务书给的原句（「固定的月内节奏」「口径有变」）没有回出处逐字核，实施者又在上面加了具体化；自己另跑的只读统计（净投放低档 96 天里 74 天在每月 3 至 12 日）支持量的一侧，没有覆盖价的水平档位。② 沿用「view 里出错整块不可用」的既有兜底，没想到新增内容与既有内容应当各自失败。③ 文字类检查只有黑名单和关键词在场两种，结构类检查只看键名，页面检查只看语法层的 class 与颜色。
**影响面**: 均在开发副本内，未进工作区与生产页面。
**修复/建议修法**: 已做——旁注改写为带统计窗、点明价项显示的是水平而节奏出自 5 日变化、量项写「含义有变」、去掉「固定」；`view()` 里两处各包一层兜底，出错只让自己显示「本轮不可用」；模块内部失败时构建日志也带 ⚠；页面对缺 `items`、缺 `tag` 的结构设防。测试与核验补：旁注逐字钉住并把七处事实逐条绑到出处原文；25 种档位组合对整个并读结果做全等比较；页面新增脚本不许做数值比较、不许读分位；详情页说明有源码钉子并在核验里实际执行；接入步骤只许给 `snapshot["prereq"]` 赋值（行首与分号后都算）；「改回后消失」改为在注入过的同一棵树里重建。
**预防门禁**: `test_r17_prereq.py` 的 `test_head_and_note`、`test_output_is_fully_determined_and_never_adds_words_for_any_band_combination`、`test_failure_in_the_new_lines_does_not_take_down_the_sixteen_rows`、`test_step_is_non_blocking_and_before_snapshot_is_written`、`test_detail_panel_carries_the_prerequisite_note`；`ops/verify_r17_e2e.py` 的 C4、C4b、E5、E6、D13、G7b。写进页面的说明句，落笔前把每个事实对回出处原文，任务书里的原句也照此办理。
**来源**: 2026-11-16 R17 实施场；复核回报在主会话内（未单独落盘），其脚本在 `/tmp/claude-501/r17_review/`（系统临时目录，不保证留存）。

**核验脚手架另记三处（同场，已绕过）**: ① 用 difflib 取「改动后新增的字符」去查判断词时，整行搬动的旧行会被算成新增（两行区块标签里既有的「非预警器」被报成新增的「预警」）；改为：改动前有一模一样的行就不算新增，搬动并改过的行与被删行里最接近的一行做字符级对齐。② 给构建器传一份不合规的复核输出，它照常写出快照与页面，然后以退出码 1 报 `REVIEW_REJECTED`（既有行为）；拿它来造「上游原子不可判」时，断言要写「退出码 1 且页面已写出」，不能写「退出码 0」。③ 快照新增顶层键 `prereq` 后，前三段核验的「其余字段全量相同」会报仅一侧有，三份脚本各加一处忽略键（与第三段加 `cn_macro` 同一做法）。

## [NOTE-20261116-014] 情绪分缺数时按 0 处理，会落进「已触发」分支（R17 范围之外的旁见，实读未实跑）

**状态**: ⚠️ 已知风险（未修；是否处理待 Doctor 定）
**优先级**: 🟡 中
**触发场景**: R17 独立复核时旁见，实施者回读源码确认写法如此。
**硬证据/最小复现**: `Projects/Financial/风险日报/build_risk_daily.py` 的 `_mol_trig` 情绪分支 `s=v or 0`，随后 `if s>=75 or s<=20: return "fired"`；`_atom_trig` 内部市场分支 `s=market_direct or 0`，同一判断。读数为空时 `s` 为 0，满足 `s<=20`，返回已触发。未实跑复现：其后还有情绪季节定触发态的一步（读得到季节时会把这两处的触发态改写为季节决定的值），只有情绪分与季节同时读不到时，这个分支的结果才会留到页面上。
**根因**: 「缺数」与「读数为 0」没有分开；其他几个分子（新股虹吸、AI）缺数时返回不可判，这两处没有。
**影响面**: `recap.db` 的情绪分读不到时，情绪分子与内部市场原子可能显示已触发。也因此，R17 的「上游原子不可判」标记实际只在科技原子上可达——内部市场原子缺数时不会给出不可判，其下游四张分子卡不会出短标。
**修复/建议修法**: 缺数时返回不可判（与新股虹吸一致）。这会改触发规则，属判定层改动，须 Doctor 裁定后另开一步，不在 R17 内做。
**预防门禁**: 无（未修）。
**来源**: 2026-11-16 R17 独立复核回报第 6 节「范围之外的旁见」；实施者实读 `_mol_trig`、`_atom_trig`。

## [NOTE-20261116-015] 在副本上开发期间，工作区的同一个文件被别的会话改了：写入时不能整份覆盖，核验基线也跟着变

**状态**: 🔄 本次已绕过（做法未固化成工具）
**优先级**: 🟡 中
**触发场景**: 2026-11-16 R17。按 G-X268 的做法在项目外的副本上开发，基线是提交 `d5e1bb8`。Doctor 确认写入前约两分钟（21:17 PST），主会话按 Doctor 另一条指令在工作区改了 `build_risk_daily.py`（综合高危线 66，未提交）。
**硬证据/最小复现**: 写入前例行比对「工作区文件是否仍等于基线」，`build_risk_daily.py` 不等（两分钟前的同一比对还相等）；`git status` 显示 ` M build_risk_daily.py`，差异是 `band_composite` 一段、调用处一行、页首标签一行，另多出 `test_composite_band.py`。若照原计划整份拷入，这三处会被冲掉。
**根因**: 副本开发把「开发」与「生产」隔开了，但没有隔开「两个会话各自往生产里写」。副本的基线是开工那一刻的提交，写入时的工作区可能已不是它；备份、差异、核验基线全都默认了「工作区＝基线」。
**影响面**: 所有按 G-X268 在副本上开发、之后写回共用工作区的任务；同一文件上有未提交的别人改动时，提交也会混在一起。
**修复/建议修法**: 本次做法——① 写入脚本第一步断言每个待覆盖文件仍等于开发基线，不等就停；② 对不等的文件用 `git merge-file -p <工作区现状> <基线> <副本>` 做三方合并，并核对「合并件相对工作区现状的改动＝我的改动、相对副本的改动＝对方的改动」；③ 用「当时的工作区内容」拷一棵新树、换上合并件，在这棵树上把测试与核验重跑一遍，核验的改动前构建器取工作区现状（`ops/verify_r17_e2e.py --before-builder`）；④ 写入前再断言一次工作区没有又变；⑤ 提交时对共用文件只暂存自己的那部分（`git apply --cached <基于 HEAD 的补丁>`），并断言暂存的内容与副本逐字节相同；⑥ 用会话消息知会对方会动哪些位置。
**预防门禁**: 写回工作区的脚本一律带「待覆盖文件＝开发基线」的断言；发现不等先看 `git status` 与差异，不覆盖。
**来源**: 2026-11-16 R17 写入场实跑；主会话的跨会话通知（同场）。

**追记（2026-11-16 21:24 PST · 同场 · 跨会话消息交叉，写入过早，已退回）**: 我向主会话发了「你是否已停手」并同时向 Doctor 提了「等它停手还是现在写」之后，先到的是主会话**在读到我的问题之前**发出的一条通知（写入时在当时的工作区版本上应用差异、不整份覆盖）。我把它当成了对我那个问题的答复，于 21:22:36 写入；一分多钟后才收到它真正的回复：它的独立核验者正在只读核对工作区这份文件，请先不要写入。**硬证据**: 工作区在 21:22:36 至 21:24:19 之间含 R17 的改动；回退后 `build_risk_daily.py` 的 sha256 与写入前快照相同（`cb2dd3bc31e5306c…`），`git diff` 对它只剩主会话的 14 增 2 删，新增文件、截图与 `_r17` 备份均已移除；`data/`、`dashboard/` 的修改时间未变。写入期间在工作区跑的测试与四份核验全部通过（30 项；55、35、45、42），可作为合并件在工作区可用的旁证，但那次写入本身已撤销。**根因**: 自己提的问题还挂着，就按一条没有回答它的消息动了手；跨会话消息是排队送达的，对方发来的未必是对我上一条的回复。**做法**: 向别的会话或 Doctor 提出的问题在得到**针对该问题**的答复之前，不做它所问的那个动作；收到对方消息时先看它是否引用了我的问题。回退脚本同样带内容断言（待回退的文件必须仍是我写进去的内容，备份必须等于写入前快照），不盲目盖回。**状态**: 🔄。

**再追记（2026-11-16 21:35 PST · 按约定顺序重新写入）**: 主会话的改动提交为 `2e8fdd9` 并明确答复已停手之后，在 `2e8fdd9` 之上重新合并（对方核验后多了两行注释，先前的合并件作废），合并树上重验后于 21:31:55 写入；写入脚本断言 HEAD 为 `2e8fdd9`、暂存区为空、待覆盖文件相对 HEAD 无未提交改动。工作区实跑全部通过。共用文件此时相对 HEAD 只剩 R17 的改动，提交不再需要部分暂存。

## [ERR-20261116-016] 高位状态一行：独立复核查出留存追加会粘行丢记录、冻结件损坏时拖累三项，另有 16 个变异核验与测试都抓不住

**状态**: 🔄 已修待验（订正后未再送审；订正版经 Doctor 确认于 2026-11-16 23:38 PST 写入工作区，下文「未进工作区」指复核时的首版）
**优先级**: 🟡 中
**触发场景**: 2026-11-16 晚，按 `Projects/Financial/风险日报/docs/2026-11-16-高位状态机制登记.md`（v1.0）在项目外的开发副本上实现页面一行与逐日留存，自验（单测 40 条、端到端 68 项全过）后送独立复核（未参与实施的 subagent，只读，PASS_WITH_LIMITS）。口径、用语、判定字段三项复核均为零差异；下列是失败处理与核验盲区。
**硬证据/最小复现**: ① 中：`high_states.append_history` 用文本方式追加。留存文件末行完整但缺换行时，新记录粘在上一条后面，两条都读不出，返回值仍是 `appended: True, bad_lines: 0`，构建日志写「新增一条」；末行是写到一半的半行时，当次记录读不出，一天一班时这一天就丢了。② 低：`read_history` 用 `read_text`，文件里夹进非 UTF-8 字节后每次构建都报写入失败，直到人工处理；文件头带 BOM 时首行变坏行、同日会重复写。③ 低到中：冻结件或 `.meta.json` 内容损坏（不是 UTF-8、表头不对、收盘不是数、路径是目录、meta 不是 JSON 或不是对象）时三项都记不可判；登记第 1 节说明第三点只让「获利」不可判。④ 低：`SystemExit` 只在第一次 `H.load` 处接住；让 `States.__init__` 抛 `SystemExit`，构建退出码 1、不写快照与页面。⑤ 低：页面脚本对 `view.items` 里的空值不设防（抛 TypeError，这段脚本在主脚本前部，其后渲染全停）；`cls` 只转义尖括号不转义引号。⑥ 低：`_calc()` 把 `ops/` 插到 `sys.path` 最前并留在构建进程里。⑦ 文档串与注释三处说得偏满：「坏行跳过」不含上面 ①② 两种；「任何失败（…数据陈旧…）都落到不可判」不含行情库整体停更；样式注释「一律墨色，不按状态着色」而实际按状态换了深浅与粗细。⑧ 复核者 90 个变异里单测抓住 66、核验另抓住 8、两边都漏 16：写快照前按三项同时成立把综合档位改成「高危」；页面脚本在三项同时成立时去改综合档位的字或给整行加红底；成立的短标加近红底色与下划线、把某一行 `display:none`；行标里加「见顶预警」「已进综合温度」；短标、解释句不转义；去掉数组判断；模块内失败时日志不带 ⚠；市场时钟不筛成交额；快照里的纪律句改成「已纳入综合温度」；三项都不可判的日子不留存；快照数字只留一位小数；模块里把跟随门槛写成 `3 * 9` 再判一次。
**根因**: ① 追加照 `temp_history.append_live` 的写法写，默认「文件就是自己上次完整写完的样子」；自测只有「夹一行坏行」，那行后面带着换行。③ 注入只照任务书点名的三种情形（缺失、被改动、缺 meta）造，没有顺着 `read_frozen` 的执行顺序（先解析、后校验）把「解析就失败」这一类走一遍。④ 知道口径脚本用 `SystemExit` 报错（见 NOTE-20261116-017 ①），却只在已知会抛的那一处接。⑧ 页面检查的桩 DOM 只提供新一行自己的两个元素，脚本去改别的元素时桩返回空、检查看不见；样式只查了 `color:` 与几个固定色值；「口径只有一份」靠检索门槛数字守，换个写法就漏；三项同时成立的回放日没有做改动前后比对。
**影响面**: 均在开发副本内，未进工作区与生产页面。旁见（实读，未实跑复现）：`temp_history.append_live` 同样是文本追加、不补换行、不回读，`temp_history.jsonl` 有同一隐患——属本任务范围之外，未改。
**修复/建议修法**: 已做——追加改按字节写，末字节不是换行先补一个，写完回读、本条读不出即报错；读取按字节逐行解码容错并去掉文件头 BOM；带冻结件读失败且不是库自己报错时，不带冻结件再读一次，读得成就只让「获利」不可判并写原因；`compute`、`judge`、`build_step` 的兜底都接 `SystemExit`；页面脚本整段包 try，`items` 含空值即显示不可用，`cls` 走白名单，引号也转义；口径脚本改按路径加载，不动 `sys.path`；文档串与样式注释改成实际行为；快照与留存加市场时钟日 `market_day`。测试 40 条补到 50 条，核验 68 项补到 83 项。未做、待 Doctor 定——同一北京日首次构建时数据没到齐、同日重建后才显示真实状态的，留存只有首条（任务书定的「同日重建不增行」）；行情库整体停更时照旧显示库里最新交易日的状态（登记没有这条期限，页面写明数据日）。
**预防门禁**: `test_high_states.py` 的 `Retention.test_missing_final_newline_does_not_glue_records`、`test_non_utf8_bytes_and_bom_are_tolerated`、`test_readback_failure_is_reported`、`test_all_unknown_day_is_still_recorded`；`Compute.test_broken_frozen_or_meta_only_takes_profit_down`、`test_db_error_is_not_blamed_on_the_frozen_file`、`test_system_exit_inside_reference_is_contained`、`test_market_clock_ignores_days_without_turnover`；`Lines.test_module_never_rejudges`（成立与否只听口径脚本，分位取 0 到 100 都不再判）；`Builder.test_page_script_only_places_text`（脚本只许取自己的两个元素、每处插值都过转义或白名单）、`test_style_is_ink_only`（样式属性与取值逐项白名单）、`test_row_sits_right_under_the_composite_bar`（行标钉原文）；`ops/verify_high_states_e2e.py` 的 D1e–D3e（回放日也做改动前后比对）、E1d–E4d、E7x、E7y、E11、F4b、H5、H6。写「追加一行」先问：文件末尾不是换行怎么办、写完怎么知道读得回来。页面检查的桩要么提供全部元素并断言没被碰，要么在源码层限定脚本能取哪些元素。
**来源**: 2026-11-16 独立复核回报（在实施会话内，未单独落盘；其脚本与日志在 `/tmp/claude-501/rd_hs_review/`，系统临时目录，不保证留存）；本场复核实与修复。

## [NOTE-20261116-017] 高位状态实现场的六处坑：口径脚本用 SystemExit 报错、构建日比交易日晚一天、前几段核验的输入是活的，等

**状态**: 🔄 本次已绕过（③④ 的根未动）
**优先级**: 🟢 低
**触发场景**: 2026-11-16 晚，高位状态一行在项目外的开发副本上实施与核验。
**硬证据/最小复现**: ① `ops/calc_high_states.py` 的 `load` 在冻结件与公共库重叠日不一致时 `raise SystemExit(...)`。`SystemExit` 不是 `Exception` 的子类，构建器各接入步骤的 `except Exception` 接不住——直接调用会让整场构建退出、不写快照。② 定时班 17:05 UTC 是北京次日 01:05，构建器的 `BJ_TODAY` 比行情库最新交易日晚一天；登记说的「当日」若取 `BJ_TODAY`，科创 50 那天没有收盘，三项恒不可判。留存里 `date`（构建日）因此恒比 `asof`（交易日）晚一天，周末与节假日同一个 `asof` 会有多条。③ 前几段核验的输入不是冻结的：`verify_cn_liquidity_e2e.make_docs` 把真实 `Database/` 用符号链接接进临时目录。22:51 另一个会话重写了 `Database/烛照九阴/recap.db` 的离岸汇率日期并重生成了工作区的 `data/temp_backfill.jsonl`；开发副本里那份回补是 11:14 的旧件，`ops/verify_marginal_e2e.py` 在副本上由 35 项全过变成 PASS 32 / FAIL 3（F2 两条、F3）。换进工作区现行的回补文件与基线文档后 35 项全过（复核者实跑）。与高位状态的改动无关。④ `ops/verify_cn_liquidity_e2e.py`、`ops/verify_cn_macro_e2e.py` 取基线用 `git -C <树>`，没有 `--repo` 参数；在没有 `.git` 的副本上跑会取不到。⑤ `git --no-pager diff --no-index --check -- /dev/null <新文件>` 对任何新文件退出码都是 1，没有空白问题时也一样。⑥ 回放页（把行情库截到某一天再构建）只有高位状态一行是当日截面；页面其余部分用的是截断的库加今天的其他输入，综合温度等不是当日真实值（同一张 2026-05-06 回放页，前后两次构建综合温度分别是 50 与 49，其间汇率库被别的会话改过）。
**根因**: ① 参考脚本是给命令行用的，报错即退出是合理写法；接进构建器时换了调用环境。② 班次时刻跨了北京日界。③④ 核验脚手架默认「副本带 `.git`、真实库在核验期间不变」。⑤ `--no-index` 隐含「有差异即非零」。
**影响面**: ① 所有把命令行脚本接进构建器的做法；③ 所有在副本上隔一段时间重跑前几段核验的场合——FAIL 未必是本次改动造成的。
**修复/建议修法**: ① `high_states.py` 在读入、逐项判定、构建入口三层都显式接 `SystemExit`。② 「当日」取科创 50 最新收盘日，并与 `daily_market` 最新交易日对一下；留存两个日期都记，评估按 `asof`。③ 本次做法：写入工作区后在工作区重跑；副本上出 FAIL 先比对副本与工作区的 `data/` 是否同一版。建议（未做）：核验脚本把用到的库各拷一份快照再跑。④ 本次做法：设 `GIT_DIR=<真实仓>/.git`（只读，脚本里的 git 带 `--no-optional-locks`）。建议（未做）：两份脚本各加 `--repo`。⑤ 看输出是否为空，不看退出码。⑥ 回放截图注明「只有这一行是当日截面」。
**预防门禁**: `test_high_states.py` 的 `Compute.test_system_exit_inside_reference_is_contained`、`Retention.test_build_step_never_raises`（含 `SystemExit`）；`ops/verify_high_states_e2e.py` 的 E3、E11。
**来源**: 2026-11-16 高位状态实施场实跑；③ 的换件重跑出自独立复核回报。

## [ERR-20261116-018] 用可被订正的输入重算出的历史最高值来定线：汇率表一修，66 就不存在了
**状态**: ⚠️ 已知风险（Doctor 2026-11-16 23:43 PST 裁「维持 66」，生产未改；按现库这条线在历史上从未触发）
**优先级**: 🔴 高
**触发场景**: 2026-11-16 晚按「六分子回补的综合温度在 2026-06-22 达到 66、为一年多最高」把综合高危线由 75 降到 66（项目仓 `2e8fdd9`）。同晚 22:51 `recap.db.fx_cnh_daily` 按日期重标修复。
**硬证据/最小复现**: 修复前生成的 `docs/2026-11-16-综合方式回放比较-逐日.csv` 里 2026-06-22 为 66（汇率分子 22）；修复后重生成的 `data/temp_backfill.jsonl` 同日为 64（汇率分子 10，原始均值 64.5）。CC 23:42 PST 用 `temp_history.py` 重算：同日口径 5 月 6 日 65、6 月 22 日 64；生产近似时钟两天都是 65；保守可得时钟 60 与 61，最高 65。没有任何一天到 66。
**根因**: ① 定线用的是按「各输入当日到齐」的回补值，既不是当时可得的版本，输入还带着一个已登记未修的日期错位（NOTE-20261116-001）；② 线定在样本最大值上，任何一个分子变动几分就会让它落空；③ 综合温度取整是四舍六入五成双，64.5 取成 64，线正好卡在这种边界上。
**影响面**: 现行高危线 66 高于现库重算的全部历史值，放回 2026 年 6 月不会亮；此前向 Doctor 报告的「66 只报一次、在见顶前 6 日」已失效。页面当前综合温度在 22 上下，暂无显示上的影响。
**修复/建议修法**: 线的数值 Doctor 已裁维持 66。今后再议时，无论定多少，定线依据改用按可得时点重算的序列，并同时报「同日口径、生产近似时钟、保守时钟」三个数；不再把线定在样本最大值上。
**预防门禁**: 凡要拿历史重算值定线或下结论，先查输入表有没有已登记未修的问题（本例为 NOTE-20261116-001），有就先修或先标注；结论里写明生成时的数据版本，输入被订正后必须重算。
**来源**: 2026-11-16 晚主会话核对 V.V.《综合温度次级档位校准回测》v1.1 时发现；`brain/风险日报/architecture/决策记录.md` 同日补记条。

## [NOTE-20261117-001] 高位状态的端到端核验把「相对基线只增不改、档位与改动前相同」写成断言：之后任何一次合法的改线都会让它报红

**状态**: 🔄 五份核验已改为共用登记模块并逐点比较档位（追记四，待独立复核）；R17 核验 H1 的词表范围与流动性核验过期的缺省基线两处未动
**触发**: 2026-11-17 凌晨按 Doctor 令把综合警戒线由 50 改为 60 后，跑 `ops/verify_high_states_e2e.py`（基线 04e02e5）。
**硬证据**: 输出末行「PASS 80 / FAIL 3」：A6（构建器相对改动前只有插入，没有删改）、D2e、D3e（2026-06-22、06-23 截面下综合 50，由「🟠 警戒」变「平静」）。用 difflib 比较，04e02e5 到 HEAD 929c786 只有 4 处插入；到工作区多 1 处替换，正是 `COMPOSITE_WARN = 50` 改 `60` 这一行。今天的判定字段（A1）不变。
**根因**: 这份脚本是为「高位状态接入不改变任何判定」写的回归核验，基线固定在接入之前的提交；脚本又拒绝使用已含接入的提交作基线（第 207 行）。于是它只能回答「相对 04e02e5 有没有别的改动」，对之后有意的判定改动没有出口。
**影响面**: 此后重跑这份脚本恒为退出码 1，容易被读成高位状态这一行出了问题；另外它的三个历史截面只截了科创 50、成交、融资与英伟达，其余输入是当天的值，截面里的综合温度不能当作当日的生产值引用。
**建议修法**: 给脚本加一个明示的「已知判定改动」入口（例如先把基线构建器里的同一常量改成现值再比较），两处断言本身不放松；或把 A6、D*e 的口径改成「除登记在册的常量外逐项相同」。动脚本前先与写它的会话对齐。
**预防门禁**: 写「改动前后逐项相同」这类回归核验时，写明它保护的是哪一次改动、到哪个提交为止有效；改生产常量之前先跑一遍现有核验，把会因此变红的项列进改动说明。
**来源**: 2026-11-17 凌晨主会话；`brain/风险日报/architecture/决策记录.md` 2026-11-17 条。
**追记（2026-11-17 凌晨，同场）**: Doctor 答「同步脚本」后，`ops/verify_high_states_e2e.py` 加了 `KNOWN_JUDGMENT_CHANGES` 与检查项 A6k，原有断言未改，重跑 84 项全过。同场把另四份核验也跑了一遍，查出同族两处：① `ops/verify_r17_e2e.py` 的 H1 检索构建器相对 2e8fdd9 新增的**全部**字符（注释也算），词表里有「警戒」「下跌」，还有单字「松」「紧」「趋」；以后任何人在构建器里新写的注释只要带这些字就会让它报未通过。本次是改写注释避开的，脚本没有动。② `ops/verify_cn_liquidity_e2e.py` 的 `--before-ref` 缺省值是 HEAD，接入提交之后直接跑会以「HEAD 的构建器里已经有 cn_liquidity」退出，须手工给 `--before-ref ef08963`。两处都是「核验只在写它的那一刻成立」，应升格通用教训（同族第二次出现）。
**追记二（2026-11-17 凌晨，同场）**: 独立复核（只读，PASS_WITH_LIMITS）又指出两点。③ 另四份端到端核验的基线里综合警戒线还是 50，它们都用含综合档位的判定字段比较改动前后；综合温度落在 50 至 59 的日子重跑，会报未通过（读码推断，未实跑；今天综合 23，四份实跑全过）。稳妥的修法是把登记清单与套用函数放到公共模块，五份共用。④ 高位状态核验的三个历史截面现在综合是 49、50、50，都在平静档，改线之后没有任何场景落在 60 以上，端到端对综合档位线的敏感度比改线前低；可另加一个综合落在 60 至 65 的截面。已做的补强：A6k 加了「改动后同名赋值行只能有一行」，在副本里插一行覆盖常量会被 A6、A6k、D2e、D3e 报出（CC 实跑）。
**追记三（2026-11-17 凌晨，同场）**: 增量复核（只读，PASS_WITH_LIMITS）实跑证实一个仍在的口子：在构建器里插入 `COMPOSITE_WARN -= 5`，高位状态核验 84 项全过、退出码 0。三层同时不敏感——A6 只要求「只有插入」；回放日综合温度 49、50、50 不压线；`test_composite_band.py` 第 25 行的取数器只收 `ast.Assign`，增量赋值、带标注赋值、元组赋值都被跳过。逐行数同名赋值堵不完写法。建议修法：从改动后的构建器与套用登记项后的基线里各取出档位函数与相关常量，对 0 至 100 逐点比较档位；单测的取数器同样改成按行为取。状态：未修，已在脚本注释里写明。
**追记四（2026-11-17 凌晨，同场）**: Doctor 答「现在做」。新增 `ops/judgment_register.py`（登记的综合档位线、改动前快照的归一、逐点档位比较、源码层换行登记），五份端到端核验都接上，`test_composite_band.py` 加一条按行为取数的测试，另有 `test_judgment_register.py` 13 条。追记二③、追记三两处已修并实跑证实：截到 2026-06-22 的行情库（综合 50）上，旧的宏观核验报 A2、A3 未通过，新的全过；插入 `COMPOSITE_WARN -= 5` 时高位状态核验报 A6b 与单测未通过。仍未动的：追记①（R17 核验 H1 把构建器里新写的注释也算进去）、追记②（流动性核验缺省基线过期）、追记二④（没有综合落在 60 以上的截面）。以后再改综合档位线：改 `COMPOSITE_LINES`，并改写 `KNOWN_JUDGMENT_CHANGES` 的原条目。
**追记五（2026-11-17 凌晨，同场）**: 共用登记经第三、四两轮独立复核（PASS_WITH_LIMITS），又得两条须知。⑤ 高位状态核验的 E 段依赖「科创 50 已更新到行情库里最新交易日」：每天行情库更新到一半时（本次是 01:32 PST，`daily_market` 已到 11-17、科创 50 还在 11-16）重跑，会有约 12 项与代码无关的未通过。重跑前先查两张表的最新日期，或传一份状态一致的库副本。⑥ 共用登记的逐点比较是在核验进程里执行取出的语句：`SystemExit` 已按取不出处理，`os._exit(0)` 接不住——核验会以退出码 0、零输出结束，所以判定通过要同时看合计行；调用前临时改常量再改回也看不出来。两条都写进了 `ops/judgment_register.py` 的文档串，逻辑未再改。
**追记六（2026-11-17 /save）**: 已升格通用教训，见 `permanent/通用教训.md` G-X276「「改动前后逐项相同」的回归核验绑着固定基线，只在写它的那一刻成立」（Doctor 在分拣选择窗勾选）。

## [ERR-20261117-002] 迁入 Financial/ 后 `build_risk_daily.py` 的 `FINANCIAL = HERE.parent / "Financial"` 拼成 `Financial/Financial`，FOMC 日历与白泽观星预测读取失败

**状态**: 🔄 已修（2026-11-17 21:4x PST，CC），待下一次定时构建实跑确认与独立复核
**触发**: 2026-11-17 晚核对风险日报迁入 `Projects/Financial/` 后首次定时构建（09:09 PST 产物）。
**硬证据**: `data/latest-envelope.json` 的 `unavailable` 为 `fomc_calendar.json 文件不存在`、`fed_prediction_*.json 目录无匹配文件`；`data/risk_snapshot.json` 的 fomc 原子 `detail` 为「FOMC 日历读取失败: [Errno 2] No such file or directory」；迁移前最后一次提交的 envelope（`git show HEAD:data/latest-envelope.json`，11-10 版）`unavailable` 为空。两个文件实际都在（`Financial/烛照九阴/config/fomc_calendar.json` 存在；`白泽观星/reports/daily/` 下 93 个 `fed_prediction_*.json`）。
**根因**: 第 26 行无 env 分支用 `HERE.parent / "Financial"` 定位兄弟项目——迁移前 `HERE.parent` 是 `Projects/`，迁移后是 `Projects/Financial/`。迁移时的消费方扫描查了完整路径串、分段拼接和 `parents[N]`，这行是单层 `.parent` 拼兄弟目录，三类都没覆盖（同场修过的 6 处是 `parents[3]` 推算 Documents 根）。
**影响面**: 2026-11-17 这一期（北京 11-18）风险日报的 FOMC 事件时钟说明为读取失败，温度取代码默认值 20 / 尚有余量（显示为绿色「平静」，与当日正确的窗外值碰巧相同），这一行已写入 `data/temp_history.jsonl` 2026-11-18，历史里与真实读数分不出来；白泽观星美联储预期 7 个键缺失、卡面倒计时缺失，页面写「观星预测：待取」易被读成上游没取数。fomc 原子不进综合温度，综合温度 25 不受影响。其余原子的变化都是数据本身变动（独立复核逐个比对）。定时班镜像未设 `RISK_DAILY_DOCUMENTS_ROOT`，本期走的是无 env 分支（已证实）。单独打开 `ai_tech_alarm_tab.html` 时 EAL 链接正确；嵌入 `dashboard/risk-daily.html` 后相对链接按 dashboard/ 解析会错位，这是迁移前就有的问题（另挂 TODO）。
**修复**: 改为 `FINANCIAL = (DOCS/"Claude"/"Projects"/"Financial") if _documents_root else next((_p for _p in HERE.parents if _p.name == "Financial"), DOCS/"Claude"/"Projects"/"Financial")`（兜底原为 `HERE.parent`，扁平挂载下会静默算错，按独立复核建议改为 DOCS 下的固定路径）；备份 `Projects/Financial/风险日报/_bak/build_risk_daily.py.bak_2026-11-17_financial-path`；py_compile 通过，本机解析出 `Projects/Financial`、FOMC 日历存在、预测文件 93 个。未重跑构建（构建会写产物并由定时班推送）。
**独立复核**: 2026-11-17 晚，未参与实施的子代理只读复核 PASS_WITH_LIMITS——诊断成立（新增不可用来源只有这两项，均因迁移）；修法在本机、云端无 env、云端有 env 三种情况下路径都对；其余在用脚本未再发现迁移后失效的路径写法。限制：修复未经真实构建验证。
**另提设计问题（待 Doctor 定）**: FOMC 日历读取失败时用默认绿色读数并写入历史，日后若在事前窗或结清日出同类错会悄悄漏报；可考虑失败时温度记为不可判。
**预防门禁**: 目录迁移的消费方扫描，「按层级推算」一项要包括单层 `.parent` / `../` 拼兄弟目录的写法，不只 `parents[N]` 与多层（通用教训 G-X278 追记）；迁移后第一次实跑要核 envelope 的 `unavailable` 是否比迁移前多。
**来源**: `logs/2026-11-17-EAL整理与Financial项目整理.md`。

## [NOTE-20261118-001] `margin_daily` 缺 2026-09-30 一行（交易日历为开市，成交额表有这一天）

**状态**: ⚠️ 已知风险（未修）
**优先级**: 🟢 低
**触发场景**: 2026-11-18 起草《温度计迭代提案》（`Projects/Financial/风险日报/docs/2026-11-18-温度计迭代-提案.md`），独立核验复算融资余额与成交额之比时发现。
**硬证据/最小复现**: `Database/Market-Data/market_data.db` 只读实跑（2026-11-18）：`margin_daily` 在 20260929（25796.89 亿）之后直接是 20261008；`trade_cal` 中 20260930 的 is_open＝1；`daily_market` 20260930 有成交 1.45 万亿。
**根因**: 未查实。假设：`Projects/Financial/烛照九阴/scripts/fetch_margin.py` 只写沪深两所都到齐的完整日（L93、L102），09-30 当晚深交所数据未到被跳过；下一个交易日是长假后的 10-08，之后的增量抓取没有回头覆盖 09-30。撤回条件：查到 09-30 曾写入后又被删，或数据源当日本就没有这一天。
**影响面**: 按行数回看的融资读数（5 日、20 日变化，近 252 行分位）跨过这一天时，窗口实际多覆盖一个交易日；单日缺失，影响小。现行杠杆分子取最新一行，不受影响。
**修复/建议修法**: 生产方补跑 `fetch_margin.py` 覆盖 20260930（Doctor 终端或烛照九阴取数班），补后核对该行沪深两所字段齐全。
**预防门禁**: 抓取脚本收尾自检加一条：按 `trade_cal` 列出近 N 个交易日里 `margin_daily` 缺哪些日子，有缺即报。
**来源**: 2026-11-18 主会话（风险日报温度计迭代提案核验）。此前 ERR-20261116-011 的 11-16 追记（L541）顺带提过一句，未单列。
