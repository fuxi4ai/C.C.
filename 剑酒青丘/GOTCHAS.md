---
title: 剑酒青丘 · GOTCHAS（已知坑 · 索引）
tags: [剑酒青丘, gotchas, index]
created: 2026-07-24
updated: 2026-08-17
status: active
type: resource
project: 剑酒青丘
---

# 剑酒青丘 · GOTCHAS（已知坑 · 索引）

> 剑酒青丘＝金融取数/回测基础设施（`infrastructure/取数工具/` 下 adjustment_grade / market_health / snapshot 等）。本文件是本项目坑的落地处。
> **编号**：`[BUG-YYYYMMDD-NNN]`（代码）/ `[INFRA-…]`（环境·链路）/ `[RISK-…]`（已知风险）。**状态**：🔄 待修复/已修待验 · ⚠️ 已知风险 · ✅ 已修复（**仅由 Doctor 或指定独立验收方落，实施者不得自标**）。

## 条目

### [BUG-20260723-001] `adjustment_grade.py._mnt()` 硬编码 `../×6` 回推根，沙箱平铺挂载下溢出到 `/` → 日报级别读数占位
**状态**：✅ 已修复（2026-07-23）
**优先级**：🟡 中
**触发场景**：烛照九阴日报定时班（九儿·平铺挂载）级别读数栏显示「不可用」；`gen_daily_report.grade_section()` subprocess 调 `剑酒青丘/infrastructure/取数工具/adjustment_grade.py --json` 两分支皆败降级。
**根因**：`_mnt()` 用 `HERE + ../×6` 回推「Documents 等价根」。平铺挂载下 `剑酒青丘` 直挂 `/mnt/剑酒青丘`、层级更浅，`../×6` 溢出经 `/mnt`→`/sessions`→`/`，于是 `/Database/.env`、`/Database/Market-Data/...` 全落空。手动/全树沙箱班正常（`../×6` 恰好落对），易误判一次性瞬态。
**修复**：`_mnt` 前置 `_find_root()`——① `ZZJY_MNT_ROOT` env 兜底优先；② 自愈：从本文件逐级上找「含 Database 子目录的最近祖先」作根；③ 回退原 `../×6`。宿主机/全树检测与旧逻辑逐字一致（正路零改动），平铺沙箱落 `/mnt`。三布局隔离测试 + 真脚本 `--json`(L3·confirm True) 均过。
**同族/来源**：升为跨项目通则 [[通用教训]] G-X88（G-X45/G-X63 平铺挂载路径族·第二次同族复发）；manifestation 侧见 [[烛照九阴/GOTCHAS]] GOTCHA-20260723-001。→ brain/logs/2026-07-23-级别读数占位修复与待办批量推进.md

## 跨项目通用教训

- 跨项目脚本靠相对层级（`../×N` / `parents[N]`）回推根目录的，一律换「探测含标志子目录的祖先」——见 [[通用教训]] G-X88（平铺挂载路径族）。

### [BUG-20260817-001] 面板 dropna+reset_index 后仍用原始 grid 下标取窗 → CAR 窗口系统性后移一日
**状态**：✅ 已修复（2026-08-17 · VV 验收逮出）
**优先级**：🔴 高
**触发场景**：EAL 2-P CAR 重算脚本——`df = df.dropna().reset_index(drop=True)` 之后，仍用 `idx = {d:i for i,d in enumerate(原始grid)}` 映射事件日到面板行号。首行 pct_change 为 NaN 被删，行号整体错位 → 全部事件窗口取到 [t+1, t+4] 而非 [t, t+3]。
**根因**：两套坐标系混用——映射表基于原始 grid、取值基于 reset 后面板，中间隔着一次 dropna。
**修复**：按 date 直接索引（`dl = list(df['date']); i = dl.index(ds)`），弃用下标映射表。VV 抽查三处全命中后落盘。**强化（2026-08-17 VV 四轮）**：事件窗必须按 date 键定位，并有玩具交易日历性质测试（假日/缺行/乱序面板仍得正确窗）。
**同族/来源**：G-X111（不凭印象）变体——下标错位是「结构变了但引用没跟着变」；与 G-X148（数值 db 实读）同场暴露。→ logs/2026-08-15-EAL方法论重构v1.4至v2.2.md · PRD 2026-08-17_EALv2.3五项gate收口_PRD.md

### [BUG-20260817-002] statsmodels SARIMAX 漏设 trend='c' → 无截距规格 AIC 全错；pvalues 按位置取值取错参数
**状态**：✅ 已修复（2026-08-17 · VV 验收逮出）
**优先级**：🟡 中
**触发场景**：EAL G5 local-level 候选梯——`SARIMAX(y, exog=X, order=(1,0,0))` 未设 `trend='c'`，跑出无截距 AIC（196.057/196.956），与含截距权威值（190.116/191.996）差 6+；且 `pvalues[0]` 取到 exog 第一列（ΔVIX）的 p 而非 AR 系数 φ 的 p（正确 φ=0.0325·p=0.696）。
**根因**：SARIMAX 默认 trend='n'（无截距），与 OLS 的隐含截距习惯冲突；pvalues 的索引是参数名（'ar.L1'）不是位置。
**修复**：一律显式 `trend='c'`；p 值用 `pvalues.get('ar.L1')` 具名取值。（衍生：滚动窗状态空间拟合默认优化器偶发不收敛→加 BFGS(maxiter=500) 重试逻辑入码，否则逐窗独立跳过致共同窗样本漂移·2026-08-17 七修）**强化（2026-08-17 VV 四轮）**：显式截距、参数具名访问、完整预测方差、统一优化器与共同窗——五者缺一即规格合同不完整。
**同族/来源**：宣称「数值差源于面板细节」被 VV 证伪——实为规格漏截距；教训：**模型规格默认值先查文档再跑**，不凭 OLS 习惯类推。→ 同上

### [RISK-20260817-001] 事件簇纪律执行漏：重叠窗漏合并交易日
**状态**：✅ 已修复（2026-08-17 · VV 验收逮出）
**优先级**：🔴 高
**触发场景**：EAL 2-Q 簇账——6/15 MOU 与 6/17 FOMC 事件窗重叠，按簇纪律应合并六个唯一交易日 [6/15-6/23]，实际只算了 6/15 起 4 日，漏 6/22、6/23 → 簇账 +2.47 应为 **+0.1774**、段内残差 −5.00 应为 **−2.7087**。
**根因**：写规则时立了 non-overlapping 纪律（规则书 L53），执行时按「事件起 4 日」机械取窗，未检查相邻事件窗重叠。
**修复**：簇窗先算所有成员事件的 [0,+3] 窗并集、取唯一交易日。（衍生教训：重叠窗内的个体事件 CAR 一律 ◌不可分离，不得引用个体值支撑锚裁定——FOMC 6/17 与 6/15 重叠·净样本归零即此例·2026-08-17 五修）**强化（2026-08-17 VV 四轮）**：簇窗＝所有成员窗的**交易日集合并**；重叠个体不得单独归因。
**同族/来源**：规则立了但执行不引用——与「局部修全局漏」同根。→ 同上

### [RISK-20260817-002] 「局部修全局漏」+ 宣称完成未核（多轮验收反复）
**状态**：🔄 已修待独立验收（2026-08-17 VV 五轮终验：治理方向正确但 GOTCHAS 未进仓+状态自签 · 五轮整改中；**2026-08-18 VV 八轮：技术核心 PASS · 治理文本 BLOCK · 同根第三次复发——追加订正、上游旧文未替换**）
**优先级**：🟡 中
**触发场景**：EAL v2.3 VV 多轮验收——每轮修一处、漏多处引用（主规则区/关键发现/锚矩阵/P-24/迭代表/知会正文轮流出旧口径）；G5 的 expanding log score 未跑即写「候选梯跑完、结论变硬」；复现包未实跑即称「可执行」。
**根因**：勘误以「改对的那处」为中心，未以「全文旧值清零」为收口判据；宣称完成前未跑验收清单。
**修复/纪律**：① 勘误后必 `grep 旧值全文 = 0`（含否定语境逐一核对）才可称完成；② 任何「跑完/可执行/已复现」类表述前必须先实跑；③ 大改动配未参与开发的外部审查（本 session 已立为 EXP-20260815-008-P）；④ 载体同步验收只发布并验收**当前 index**；**~~（旧发布链表述 canonical→Brain→Gateway 已于 2026-08-18 VV 八轮 superseded——单一发布链以 INFRA-20260817-001 为准）~~**；**versions/latest 是 update_artifact 自动轮转的 N−1 历史副本，禁止人工覆盖、不参与同代判定**（2026-08-17 VV 二轮终验订正）。**升格（2026-08-17 VV 四轮）＝治理总条**：⑤ **实施者不得自签**——自然语言「PASS/闭环/全部通过」同属验收动作（G-X4 追记）；⑥ **第二次同根遗漏立即停止点修**，先做「概念 × 消费载体」影响面矩阵（G-X111 追记）。
**同族/来源**：G-X111 族（宣称完成未核）· G-X148（数值实读）· EXP-20260815-008-P。→ 同上

**追记（2026-08-18 · VV 八轮终验 · 同根第三次复发 · CC 登记留痕 · 八轮时点快照）**：技术核心（--dry-run 零写入/不变测试实跑/repro fail-fast/新段落）全 PASS，治理文本仍 BLOCK——五项旧绝对规则未退场：`Doctor协作偏好.md:31`「实施与验收分权」缺限定（字面覆盖客观 TODO）· `:187`「G-X4 ✓ 权仍在 Doctor·propose-then-confirm 三步链照旧」· `通用教训.md` G-X4 核心规则 4「CC 永远不允许打 ✓」· G-X10「打勾权仍 Doctor 独占」· G-X136 标题与主判据仍「仅 brain-todo 目标模式·不外溢·新场景须重新明示批准」· propose-then-confirm 主条目无例外；`CLAUDE.md:192` GOTCHAS 模板仍 `✅ 已解决/⏳ 待解决` 且缺根因/影响面/硬证据/来源；`GOTCHAS.md:14` 状态图例未写 ✅ 归属与 🔄 双义。**硬证据**：VV 八轮回执行号逐处实读核认（CC 实核 8/8 属实）。**根因同一**：追加订正、上游旧文未替换——七轮新段落落盘时未 grep 旧绝对表述全文清零。**影响面**：两套现行命令并存，执行侧无可判准；Settings 镜像与源档之间、G-X136 主判据与追记之间互相矛盾。**建议修法**：修复方案已出（P0 治理文本 14 处 + 升格通用教训「规则修订必须替换上游旧文·禁文末追记并存双轨」），待 Doctor 批。**预防门禁**：规则修订合入时必 `grep 旧表述全文 = 0`；治理文本改动列「改动处 × 引用处」影响面矩阵。**来源**：VV 八轮终验回执 · 2026-08-18 resume 场。

**追记二（2026-08-18 · VV 九轮终验 · 同根第四次复发 · BLOCK 治理传播）**：八轮修复已由 Doctor commit+push（`894ab9d`），主偏好与 Settings 镜像方向 PASS；但全仓传播 FAIL——PRD 模板其余行（47/54/128/151）与设计提案（105/117/204/214/283/317/373）仍是 Doctor 独占与「未来才下放」；portable skills（brain-prd/brain-todo/brain-save/brain-resume）与 portable CLAUDE.md 等**实际加载端**完全漏扫；通用教训 962/1039 仍简写「CC 永不打 ✓」；BUG-003 合同①「锁文件数目 ↔ manifest 行数」是伪合同；G-X150 仍写 10 用例（实为 13）。CC 八轮「全脑 grep 清零」只在 8 个主文件范围内扫，未把 portable/.skills/模板其余行纳入影响面矩阵——G-X151 判据②未执行。**九轮统一合同（单义 · 看本轮角色不看模型身份）**：① 客观 TODO 常驻授权代勾；② PRD `[✓]` 只由 Doctor 或明确指定、且未参与实施的独立验收方落；③ 实施者不得验收自己的改动；④ GOTCHAS 登记为常驻授权、状态仅 🔄/⚠️；⑤ CLAUDE.md GOTCHAS 自动登记是 Doctor 有意设计，不得撤回收紧。九轮修复（P0 全仓 + P1 superseded 指针 + 图例归属盘点）已实施，**待 VV 十轮复验**。**来源**：VV 九轮终验回执 · 2026-08-18 修复场。

**追记三（2026-08-18 · 校准轮 ×2 + 执行轮 · 同根第五次复发）**：十轮校准 BLOCK（功能验收结构与存量迁移方案未补齐），PARTIAL 校准后又补一轮（授权模型/单向发布链方向通过，功能验收结构/存量迁移补齐后签字 PARTIAL 转执行授权）。**CC 证据错更正**：校准轮盘点称三轮清洗 PRD 变更记录「重复行」——实为 grep+tail 两命令输出同一行 140 的假阳性，盘上仅一行，**不登记 Edit 重发事故**（VV 十轮实读订正）。**十轮合同执行**：PRD＝功能/需求验收基线不是审批单——G-X4 规则 1/2/6/7 重写（立卷判据三要件/直接立卷/验收主体功能需求证据≠标准/Doctor 指定独立验收方+审查员只有背书权）、G-X10 去「只审一眼改批」、G-X136 补钉（客观代勾仅限 PRD 外）；偏好新立「PRD 立卷与验收边界」条；模板 v1.2（§二 三区+追踪字段/§2.5 执行清单 task_status/单一生命周期 draft→in_progress↔blocked→awaiting_acceptance→delivered|cancelled/frontmatter task_authorization+acceptance_authority+open_decisions）；brain-prd v1.5 canonical 重写并三层发布（canonical=portable=.skill 包 SHA 4b77717f… 一致 + Cowork save_skill 更新）；canonical 裁定落两个 README（「Cowork 账号为主」superseded·仅限 brain-prd）。存量 PRD 11 份五类分流处置表已出待 Doctor 批。**待**：VV 十一轮复验 · Claude-3p 侧 .skill 安装与 plugin cache 回读（Doctor 终端）· 存量处置表执行 · 其他 brain skills 漂移收敛专场。**来源**：VV 十轮校准回执 ×2 · 2026-08-18 执行场。

**追记四（2026-08-18 · VV 十一轮 · 同根第六次复发——仓内发布通过、运行时发布失败）**：十轮只验了仓内三层 SHA，没回读**真实消费端**——Claude-3p plugin cache 实际 SHA `26828c31…` ≠ canonical `4b77717f…`，且 save_skill 把完整 SKILL.md（含 frontmatter）作 content 传入 → **双 frontmatter** + 外层 description 路由语义漂移（缺触发词）。十一轮修复：save_skill **重发**（content 只传 frontmatter 后正文、name/description 严格取 canonical）；模板双轨状态治理（§2.5 改无 checkbox 表格 task_id|task_status|evidence、§四 改 current_status+变更历史、frontmatter status 唯一真源、blocked 仅全部剩余需求被阻断、关闭条件=逐项验收或合法总签覆盖、roles 与 acceptance_authority 指定三字段）；活跃旧合同替换（通用教训 :108 关键模板示例改功能主体、:162 补指定独立验收方、「PRD 判断性 gate」→「PRD 内任何 checkbox」三处）；设计提案**全文 superseded**（status 改+banner+模板停止引用）。**教训固化（G-X151 同族第六次）**：发布链验证必须到**实际运行时消费端**（plugin cache 回读 + 新会话路由实测），「仓内 SHA 三层一致」≠ 发布完成；save_skill 的 content 只传正文、metadata 走参数，否则双 frontmatter。**待**：VV 十二轮复验 · plugin cache 单 frontmatter 回读 + 全新会话 `/prd` 路由实测（Doctor 终端）。**来源**：VV 十一轮终验回执 · 2026-08-18 修复场。

**追记五（2026-08-18 · VV 十二轮 · 同根第七次复发——metadata 仍不同源）**：十一轮 save_skill 的 description 参数**没有逐字取 canonical**（漏 `/prd [任务简称]`、§2.5 措辞自改、删落盘路径句），runtime raw SHA `2f44b282…` 与 canonical 不一致——「metadata 严格取 canonical」空转一轮。十二轮修复：canonical description 先定稿（§2.5「无 checkbox 表格」+全触发词+落盘路径句）→ 三层重发（终态 SHA `131626bd…`）→ save_skill description **逐字复制 canonical frontmatter**。另修模板边缘逻辑（状态历史预填未发生转换、缺打回路径、§七 阻断语义冲突、总签缺 covered_requirement_ids 六字段、尾部过程 checkbox 自签后门）与现行旧句（通用教训 114/122/124、偏好代录段、brain-prd「不立 PRD 改变任务性质」）。**教训升级**：metadata 同步靠「逐字复制 + 回读比对」，不靠「凭印象一致」——人工重打 description 必漂移（G-X111 同族）。**待**：VV 十三轮复验 · Claude-3p 从新 .skill 包重装 + plugin cache 回读 description 逐字核对 + 全新会话路由实测。**来源**：VV 十二轮终验回执 · 2026-08-18 修复场。

**追记六（2026-08-18 · VV 十三轮 · 同根第八次复发——逐字同源仍不成立）**：save_skill 会**自动剥除 description 中 Markdown 反引号**（6 个），runtime parsed description 与 canonical raw 永不逐字相等。十三轮修复：**canonical description 去掉 6 个纯格式反引号**（/prd、/prd [任务简称]、落盘路径句各 2 个）→ 三层重发（SHA `108b43e5…`）→ save_skill v1.5.3。另修：状态唯一真源落净（模板 218/224/235/237+§五+brain-prd 闭环全部改「frontmatter status + §四 历史行」，§五 不再重复记状态迁移）；关闭合同统一（逐项 ✓ 或被字段齐全总签明确覆盖，G-X4 规则 5 同步）；Settings 镜像补「PRD 不授予也不撤销任务权限」条。**教训**：发布渠道的**归一化行为**（剥反引号）要在 canonical 侧先行适配——canonical 与 runtime 的等价关系以「归一化后逐字相等」为合同，canonical 尽量不带渠道会剥除的格式符。**待**：VV 十四轮复验 · 全新会话 `/prd` 与「写交付标准」两次路由触发实测。**来源**：VV 十三轮终验回执 · 2026-08-18 修复场。

**追记七（2026-08-18 · VV 14轮 · 同根第九次复发——关闭合同仍两句残留）**：十三轮改了 G-X4 规则 5 与模板关闭路径节，但**模板使用指南第 5 条（:40）与 brain-prd §3「不自动关闭」红线**仍写「全 ✓ 或取消」旧句，且已传播到 portable 与 .skill 包内——同一合同三处引用只改了两处（G-X151 判据②影响面矩阵执行仍不完整）。十四轮窄修：两句统一为「每个 requirement 逐项 [✓] 或被字段齐全合法总签明确覆盖；另一路径 Doctor 显式取消」→ 三层重发 SHA `f0437ea5…` → save_skill v1.5.4。**待**：VV 十五轮复验 · 全新会话两次路由触发实测（/prd、写交付标准）。**来源**：VV 十四轮终验回执 · 2026-08-18 修复场。

**追记八（2026-08-18 · VV 十五轮 · 同根第十次复发——commit 已推但 TODO/交付命令仍停待执行 · CC 登记留痕）**：十五轮暴露的新增症状——Doctor 已完成十四轮 commit/push（`bc1e86f`）后，TODO 与已贴交付命令仍停在「待执行」，直到 VV 十五轮点名才勾。**纪律固化（VV 立）**：① 收口前必须重取 `HEAD`、`origin/main`、scoped worktree（gitcheck.py 实跑），已完成事项按 G-X136 客观代勾并**废止旧命令**；② 「grep=0」必须区分 **active hits=0** 与历史/superseded 命中，不得裸报全域清零（G-X151 判据①细化）；③ 发布证据必须分五层：canonical→portable→包内 SKILL→runtime metadata/归一化正文→fresh-session 实际 Skill 调用——skill list 可见或 cache 更新不能替代真实路由。**正例**：十四轮 commit 的客观代勾（gitcheck 实核 HEAD+worktree 后勾）是正确正例；fresh-session 未实测只是 PENDING，不得误记成完成或新故障。**连带三漏项已修**：`.skills/README.md` 与 `permanent/已装skill清单.md` 升 v1.5.4+SHA `f0437ea5…`；Vault 旧包 `Vault/archived/brain/brain-prd.skill`（包内 `065c5f0a…` 含旧合同）已改名 `_DEPRECATED_brain-prd.skill_v1.0_20260818`、清单改指 canonical 包；INFRA-20260817-001 降档注事实更正（live 真源已接 Gateway·保持待独立验收）。BUG-20260817-004 维持「部分修复」（结果对象生成与生产 renderer 未落地前不得升格）。**来源**：VV 十五轮终验回执 · 2026-08-18。

### [BUG-20260817-003] requirements.lock.txt 用 pip freeze 全量 = 错误依赖锁：含系统包、缺核心包
**状态**：🔄 已修待独立验收（2026-08-17 · 九修 · VV 终验阻断点 1 逮出 · 随 A 阶段待 VV 复核）
**优先级**：🟡 中
**触发场景**：EAL repro_v23 复现包首版 lock 用 `pip freeze` 全量快照——40 行里是 cloud-init/dbus-python 等 Ubuntu 系统包，缺 numpy/pandas/SciPy/statsmodels，干净环境 `pip install -r` 因 `cloud-init==26.1` 无解而失败。
**根因**：「全量 lock」= 环境快照 ≠ 依赖锁；依赖锁必须走传递依赖（核心四包+纯 Python 依赖）。
**修复/纪律**：lock 重写为传递依赖锁；声称「干净环境可装」前必须干净环境实装验证；「八文件包、七项 SHA 通过」类表述数清 payload 数。**强化（2026-08-17 VV 四轮 · 2026-08-18 VV 九轮订正三合同）**：干净环境实装、锁文件与 payload/SHA 一致性——**三个独立合同分别对账**：① `requirements.txt` 的顶层依赖全部由 lock 覆盖且版本一致；② `SHA256SUMS` 文件名集合与 payload 集合完全相等；③ 每个 payload 实算 SHA-256 与记录逐项一致。不得把三者混称「一一对应」（「锁文件数目 ↔ manifest 行数」是伪合同——lock 行数与 manifest 行数本无对应关系，VV 九轮指正）。**现状同步（VV 七轮）**：`SHA256SUMS` 八行覆盖八个 payload（estimate_m4/panel/FRED×2/requirements×2/README/test_failfast·不自哈希）。
**同族/来源**：RISK-20260817-002（宣称完成未核）。→ 同上

### [RISK-20260817-003] 「artifact 双份同步」可直接判假——三处文件逐个实读才能声称同步
**状态**：🔄 已修待独立验收（2026-08-17 · 九修 · VV 终验阻断点 4 逮出 · 随 A 阶段待 VV 复核）
**优先级**：🔴 高
**触发场景**：八修宣称「artifact 双份 v2.3」——实读三处全假：brain 镜像仍旧 0.2400 基线/候选梯待跑/旧 FOMC；Gateway index 只改头尾标签、正文仍 v2.2；Gateway versions/1786977170792.html 连标签都是 v2.2 且与 index 哈希不同。
**根因**：只推了「自己记得的那处」，未把三处文件当清单逐项核。
**修复/纪律**：**~~（旧「两处全推（brain 镜像 + Gateway index）」表述已于 2026-08-18 VV 八轮 superseded——单一发布链以 INFRA-20260817-001 为准）~~** 声称同步前逐文件实读核验；**versions/*.html 由 update_artifact 自动轮转（更新前 index 的 N−1 回滚副本），禁止人工覆盖、不参与同代判定**（2026-08-17 VV 二轮终验订正）——与「结构改动须 artifact+prompt 双落」铁律互补：双落管机制、实读管宣称。**强化（2026-08-17 VV 四轮）**：统一发布链 **canonical→renderer→staging→校验→Gateway active→回读→snapshot/manifest**（权威定义见 INFRA-20260817-001）的**章节级回读规则**——发布后按章节逐级回读实际消费端，不比 hash 了事。
**同族/来源**：RISK-20260817-002（宣称完成未核）。→ 同上

### [BUG-20260817-004] 回归结果身份丢失——M4/M6 系数混写·R²/adjR² 混用·OLS/NW t 混用（2026-08-17 VV 四轮立）
**状态**：🔄 部分修复待独立验收（2026-08-17 · 十二修：台账 2-R/迭代表已按 canonical 重渲；**富版仍手工 patch、结果对象生成未实现、renderer 明示非生产**——VV 五轮指正降档）
**优先级**：🔴 高
**触发场景**：EAL 通道方程——M4 系数（0.113/0.108）与 M6 系数（0.143/0.098）在台账/PRD/富版间混写；「传导层主账」现行标题与 v2.3 滚动 β 残差并陈自相矛盾；R²=0.747183 与 adjR²=0.737989 及 OLS t 与 NW t 口径混用。
**根因**：回归结果没有身份绑定——跨规格手抄数值时丢失 model_id/n/cov_type/统计量名。
**修复/纪律**：每个结果必须绑定 `model_id / n / y / X / cov_type / statistic_name`；表格由结果对象生成，**禁止跨规格手抄**。
**同族/来源**：G-X111 载体版（事实分布多载体）· BUG-20260817-002（规格合同）· VV 四轮终验（方程区同代 BLOCK）

### [RISK-20260817-004] 构造回归量与统计零结果的识别边界（2026-08-17 VV 四轮立）
**状态**：🔄 已修待独立验收（2026-08-17 · 十二修 · 台账 v2.3 定位「同日通道共变（非因果）」+ constructed-regressor 边界落盘）
**优先级**：🔴 高
**触发场景**：AI_gap = r_SMH − r_SPY 右端含同期因变量，仍称「解释力/传导通道」；事件哑变量零结果写成「全部经通道传导」；相关增量写成通道坐实。
**根因**：描述性结果被写成机制与因果——没有识别设计的相关量不能给因果语域。
**修复/纪律**：RHS 含同期 Y 时强制标 `constructed-regressor · non-causal`；没有正式识别设计，只能写「待检机制假说」或「未检出条件增量」。
**同族/来源**：台账 v2.3 勘误（Pearl 中介边界）· G-X112（口径四问 · 数据语义类比）· **G-X95（源须先行独立信号·效应反推源＝镜像非因果）** · VV 四轮六根因表「因果边界失守」

### [BUG-20260817-005] 正常路径全绿不证明 fail-fast（2026-08-17 VV 四轮立）
**状态**：🔄 已修待独立验收（2026-08-17 · 十二修 · test_failfast.py 固化·SHA 八项含测试件；**五轮降档 → 五轮整改已补**：乱序/重复键/真实 -O 子进程三用例 + 框架去 assert + 负例错误族 marker 核验 + 版本守卫真实注入 → **13 用例双模式 13/13**；**七轮增强**：负例非零退出外必验错误族 marker·版本守卫改真实错误版本注入）
**优先级**：🔴 高
**触发场景**：三轮验收三种假闭环——① assert 守卫被 `python -O` 删除；② 最终 score 非有限（注入极大值 → −inf）仍 exit 0；③ 冻结输入删行（121→120）仍正常退出。
**根因**：把「当前机器跑通」误当「失败时能正确停下」。
**修复/纪律**：覆盖 `assert/-O`、最终 score 非有限、冻结输入漂移、非收敛、负向测试未固化五类；**每个不变量都有破坏性测试，并纳入复现包与 SHA**。
**同族/来源**：G-X150（本条跨项目升格）· RISK-20260817-002 · VV 二/三/四轮（fail-fast 三连 BLOCK）

### [INFRA-20260817-001] EAL 发布链多真源（2026-08-17 VV 四轮立）
**状态**：🔄 已修待独立验收（2026-08-17 · 十二修 · 发布器保险丝+previewRoot+candidate 移 staging+快照真源改 Gateway；**事实更正（2026-08-18 十五轮）**：live 镜像真源已接 Gateway（08-18 五轮整改完成 · 「仍用旧 Cowork Scheduled 真源」的降档注已不成立——更正事实、保持待独立验收））
**优先级**：🔴 高
**触发场景**：artifact 多代拼接（N−1 富版事实错代）、snapshot 脚本指旧真源（会回滚 mirror）、candidate 留生产目录成第二真源、preview 任意路径绕过保险丝。
**根因**：多份载体 + 多真源，发布链没有固化顺序。
**修复/纪律**：固化 **canonical→renderer→staging→校验→Gateway active→回读→snapshot/manifest**；禁止手拼历史版本、candidate 留生产目录、preview 绕保险丝。
**同族/来源**：G-X118 追记（回读消费者+再生不回滚）· RISK-20260817-003 · VV 四轮 P0-1/P1

### [RISK-20260819-001] shadow.7 错误族优先级依赖 runtime statistics 实现——3.10 收件端重跑 34/35（2026-08-19 接包重跑立）
**状态**：⚠️ 已知风险（包声明 CPython 3.11+ · 3.10 不在支持范围 · **生产候选 Mac CPython 3.13.3 已全套验证全绿 · 部署风险解除 · 测试注入脆弱点残留**）
**优先级**：🟡 中
**触发场景**：shadow.7 包收件端验包——沙箱 CPython 3.10.12 重跑 runtime tests 普通/-O 均 34/35：case 24「compound overflow」期望 `EAL_COMPOUND_OVERFLOW`，实际 `EAL_NONFINITE_BASELINE`；migration 19/19、legacy 7/7 双模式全绿。VV 本机 3.14.6 声称 35/35 全绿。
**硬证据**：sidecar/包内 SHA256SUMS/verify_package 全过（32 payloads/20 requirements/107 SQL objects）；case 24 最小复现 traceback 在案——engine.py L557 捕获 `statistics.stdev` 抛 `OverflowError: integer division result too large for a float` 后转 `EAL_NONFINITE_BASELINE`；3.10 探针脚本在盘。
**根因**：测试注入 `1e-155`（dates[9]）落在 baseline 窗口内，把 baseline 统计量先打炸；engine 的错误检查顺序 baseline(L557) 先于 compound(L576)；statistics 模块 3.13+ 重写导致同数据在 3.10/3.14 抛不同异常族——测试合同断言单一错误族，跨版本行为不定。
**影响面**：错误族优先级依赖 runtime statistics 实现；生产候选环境（Mac 原生）Python 版本未确认，若 <3.11 则该用例在目标环境失败；即便 3.11+ 全绿，测试注入方式横跨多个检查层是设计脆弱点。
**建议修法**：① 测试注入改为只污染事件窗（极端值移出 baseline 窗口）或 baseline 计算先行数值尺度守卫；② 生产候选版本确认（Mac 原生 python3 --version）后按真实版本重跑全套并记录版本+退出码；③ 接包验收必记录收件端 Python/SQLite 版本并与包声明比对。
**预防门禁**：错误族断言测试的注入数据不得横跨多个检查层；收件端重跑必须记录 runtime 版本三元组（Python/SQLite/operator CLI）。
**来源**：VV shadow.7 交接（2026-08-19）· CC 沙箱收件端重跑 · CC_APPLY §1
**状态注**：非 VV 实错（3.14 证据可信）；是否转修待 VV 十六轮或随生产吸收时一并处理，由 Doctor 裁。
**生产候选验证（2026-08-19）**：Doctor Mac 终端重跑——CPython 3.13.3 全套全绿：runtime 35/35（case 24 PASS）、migration 19/19、legacy 7/7 普通与 `-O` 双模式 exit=0；sidecar/包内 SHA256SUMS（32 项）/verify_package 全过。与沙箱 3.10 的 34/35 对照印证根因（statistics 实现差异）。生产候选 SQLite/operator CLI 版本三元组在 §3 数据迁移阶段补记。
