---
title: 渊图 · GOTCHAS（已知坑）
tags: [渊图, gotchas]
created: 2026-05-14
updated: 2026-08-27
status: active
type: resource
project: 渊图
---

# 渊图 · GOTCHAS（已知坑）

<!-- 2026-06-24 错题本积压复盘：3 条 ⏳ 已消化 →
     ERR-20260614-002 relation 死字段 ✅ 已净化（P2）；
     ERR-20260608-003 provenance 🟧 第①步已修+单测，第②步另立 PRD（P1）；
     ERR-20260614-001 TPU ✅ 已结案（谱系理顺单脉 + 伞节点 Doctor 定为保留世代锚）。
     当前开放 ⏳ = 0；待 Doctor 决策 = 1（ERR-003 第②步 kg_ingest 覆盖率根治 PRD 是否启动）。
     2026-06-24（二轮）：manifest `brain.gotchas` 3→1 回写（上轮只改本注释、漏回写 manifest 致看板仍显 3）；
     口径＝🟧/⏳/⬜ 未闭环计数，apply 后 =1（仅 ERR-003 第②步待PRD）。BACKLOG-20260624-001 方案就绪待 apply；派工健康埋点 ✅ 已做。
     2026-06-25：ERR-003 第②步 forward 已实装（Route A·非 PRD）→ ✅；BACKLOG-20260624-001 已 apply commit 9e9a259 → ✅。当前开放 🟧/⏳ = 0；唯一 followup = ERR-003 历史 207 孤儿回填（数据卫生·非坑）。看板 brain.gotchas 应随之 1→0（待重建 asset-dashboard.html）。
     2026-08-08 错题本复盘（GAI 计数 14 开放逐条现核）：真开放仅 1 条＝ERR-20260801-001（🟥 11 节点被吞待 Doctor 专场还原，TODO 段首在挂）；
     12 条 NOTE/认知类实质已闭、因缺标准 **状态** 行（或状态写在「类型」行/关键词不在闭集）被计数误开 → 逐条补状态行（✅ 已沉淀/已根治/已知约束），条目留档不迁；
     NOTE-20260718-002 重号拆分——「重指边去重」改号 NOTE-20260718-004（「研报数字回原报告」保留原号：决策记录×3、日志×3、核实札记×2 共 8 处引用零断链）。
     当前开放 🟥 = 1（ERR-20260801-001）。计数口径提醒：本文件计数器按 `## [` 切块、认行首 `**状态**` 行的 ✅ 系关键词——新条目务必按模板写状态行。
     2026-08-15 畸形收口：ERR-20260801-001 已还原+核验闭环（08-13 还原 · 08-15 收口）→ 当前开放 🟥/⏳ = 0。
     2026-08-20 错题本积压复盘（Doctor「审查并修复」批全案 · 看板口径 gotchas=3）：三条消化——
     NOTE-20260819-002（🔄 已修·CC 独立复核背书·✅ 待 Doctor 落签——第 13 项门禁在盘）；
     NOTE-20260819-001（✅ 已销账——Doctor 批全案确认 · description 空=0 实读）；
     NOTE-20260816-002（状态词「已固化流程」不在计数闭集被误开 → 回写 ✅）。
     另 FIX-20260626-001「待 apply」过时尾巴摘除（canonical _meta 留痕在盘）。当前开放 = 0（NOTE-002 待落签算 1 条待 Doctor 动作）。 -->


> 排查超过一轮的问题都该记录在这里。CC 遇到报错并解决后**立即**回写，无需 Doctor 提示。
> 实时操作日志写在项目目录的 `Projects/渊图/GOTCHAS.md`；这里是沉淀+索引。

## 格式

```
## [ERR-YYYYMMDD-NNN] 简要描述
**状态**: 🔄 待修复/已修待验 / ⚠️ 已知风险；✅ 已修复（**仅由 Doctor 或指定独立验收方落，实施者不得自标**）（⏳ 旧状态词 2026-08-26 迁移专场退役）
**优先级**: 🔴 高 / 🟡 中 / 🟢 低
**触发场景**:
**错误信息**:
**解决方案**:
**预防措施**:
```

---

<!-- 在下方追加新条目 -->

## [NOTE-20260819-002] 今日帕米尔批 QA 漏跑「半空节点」检查——3 个 desc+props 双空节点过门入图

**状态**: ✅ 已修复（Doctor 2026-08-26 /todo 问答板落签「③落签✅销账」· CC 代记留痕 · 证据：`rules/kg_promote.py` L32-42 第 13 项实读在盘 · 自测 5/5 记录核 · canonical 零误动）＋ **预防门禁第 13 项已实装**（2026-08-19 Doctor 批 · `kg_promote.py` 新节点 description/props 双空断言 · 自测 5/5：双空硬拦×2 / 半空提示不拦 / 正常通过 / 悬挂回归 · canonical 零误动）
**优先级**: 🟡 中
**触发**: 2026-08-19 帕米尔 3 篇 batch QA 场——CC 沙箱 QA 跑了结构 8 项/数组元素/desc 缩减/span 缺失率，**漏跑第 10 项「半空节点」检查**；今日批 3 个新节点（`concept_SixAxisForceSensorPriceRange`/`concept_MetalStrainGaugeTechRoute`/`concept_MEMSSixAxisForceSensor`）desc 与 props 双空仍通过 promote 门（kg_promote 门本身不含半空检查——半空属 CC 沙箱 QA 清单职责）。
**根因**: ① kg_promote 一键门与 CC 沙箱 QA 清单职责边界不清——门内 12 项无半空检查，半空检查靠 CC 每次手工记得跑；② CC 本场漏跑（QA 清单执行无 checklist 强制）。
**影响面**: 3 个空壳节点入 canonical（数据在 raw 源文件中不丢，图谱侧 desc/props 层缺失）。
**修复**: 2026-08-19 具身手术内补 desc/props（源=帕米尔 08-19 六维力纪要实读）。**追记（审查员留痕①）**: 补壳首版误写非 schema 键 `desc`——节点描述字段是 **`description`**（消费端读此键），且术前 3 节点 description 已非空（仅 props 空，「双空」判定本身有误）；独立审查发现后已合并补丁（新内容并入 description、删 desc 键，全图 desc 键残留 0）。**教训**: 图谱节点字段名以 schema 为准（description 非 desc），改前先读一个存量节点样例。
**预防门禁**: 建议 kg_promote 门内加第 13 项「新节点 desc/props 双空断言」（与第 12 项 span 同位置）——候选，待 Doctor 批；或 CC QA 清单固化为脚本一条命令（qa 脚本化）。
**同族/来源**: NOTE-20260819-001（desc 空挂账）· Boss老白 P2「空壳节点补全」同族。→ 2026-08-19 具身智能线手术场。

## [NOTE-20260819-001] Boss老白 P2 存量 4 节点 desc 空——本批撞 id 转 update 暴露

**状态**: ✅ 已销账（2026-08-20 Doctor 批全案确认 · 证据：canonical 实读 4977 节点 description 空 = 0，4 节点均已非空——自然回填完成）
**优先级**: 🟢 低
**触发**: 2026-08-19 帕米尔 3 篇入库，胜宏 PCB 篇 LLM 把 4 个存量节点当「新节点」输出（`concept_RubinSwitchTrayMaterialShare` / `product_NvidiaVR200` / `concept_SupernodeSwitchTrayCompetition2026` / `concept_MSAPYieldGapTechnologicalAccumulation`），kg_ingest span 校验警告「缺失 4」→ 合并时 id 撞 canonical 存量转 update（存量豁免，第 12 项实算 0/36 过）。
**根因**: 4 节点为 Boss老白 P2 批（08-16）产出，desc 层为空（props 有料 2~12 键——信息未丢，仅缺 desc 叙述层）；08-16 批「空壳节点补全」未覆盖 desc 空形态。
**影响面**: 4 节点 desc 为空；不影响结构校验与查询（props/边完整）。
**建议修法**: 下批 LLM 触及或手工 patch 时补 desc；或并入未来「desc 空节点全图扫描」专项（与 NOTE-20260815-001 desc 质量族同族）。
**预防门禁**: 第 10 项「半空节点」检查若扩为全图存量扫描可提前暴露；当前只查本批新增。
**来源**: 2026-08-19 帕米尔 3 篇入库 QA 场。

## [NOTE-20260815-001] batch LLM 缩写覆盖既有富 desc——QA 第 11 项已固化（`rules/check_desc_shrink.py`）

**状态**: ✅ 已修 + 已配检测脚本（2026-08-15 · 15 节点恢复/合并；`rules/check_desc_shrink.py` 落仓并自测通过——对未修 _v2 报出 15 处、对 canonical 报 0）**优先级**: 🟡 中

**触发**: 08-15 帕米尔 15 篇 batch 后沙箱 QA，抽查沃尔德篇「更新节点 120」（异常大）时发现 `company_Apple` desc 228→23 字。全量扫出 **15 个节点** desc 被缩写覆盖（阈值：缩短 >10% 且 >30 字），最重的几个：`company_Apple`（韬定律 N2 客户身份/UALink 创始全丢）、`concept_HumanoidRobotVisionPerception`（三条技术路线细节丢）、`concept_TauLawHardwareImplementation`（器件/封装/系统三层体系丢成一句话）。另有 `concept_AIInfraHardwareDemandPeak2027` 的 props 被清空成 {}。

**真因**: LLM 对 update 节点写缩写 desc，`kg_merge` 的顶层 description 是整替换（NOTE-20260626-001 的深合并只保护 properties/_meta）；**8+1 项校验（悬挂/自环/重复/非法 type/大小写/半空/超集/数组元素）没有一项查 desc 缩减**——半空检查只查「desc 为空」，不查「变短」。

**处置**: 12 个纯退化恢复 base desc；3 个新 desc 带增量信息合并保留（三星天津 2026 底 +20% 产能、三环工程能力/成本良率、MLCC 转换比 4 倍→迭代后 5-6 倍）；props 恢复 1。

**预防**:
- **已固化**：`rules/check_desc_shrink.py`（QA 第 11 项「desc 不缩减断言」）——对比 base 与 candidate，`len(desc) < 90% × base 且差额 >30 字` 即报，退出码 1（2026-08-15 自测：对未修 _v2 准确报出本批 15 处、对 canonical 报 0）；
- 编号注记：质检门第 10 项已被 08-15 三轮专场占用（file 存在性断言），本条检测为第 11 项；
- 或 kg_merge 对 description 做「patch 短于 base 则保 base」保护——触入库主链，另议；
- 与 ERR-20260719-001 同族：LLM 逐节点自由裁量、部分对部分错，混合污染难查。本批沃尔德篇 120 个 update 里只有少数出问题，若无阈值扫描极易整批漏过。

**追记 2026-09-05（同族第 4 次复发 · 六篇批 · 形态升级：整段替换而非缩写）**: 98 个 update 中 **16 个 desc 被 LLM 整段重写**（15 处需合并 + 1 处语义等价）——如 `company_Yingliu` 身份句（西门子 H 级叶片中国独家/卡脖子补位）被「更新：…」数据句整段顶掉；`concept_LuxshareGoogleOpticalCooperation` 旧口径（2026 入 AVL·LPO 独家·月 12 万只）与新口径（审厂验证中·2027Q2 批量）并存才完整。**`check_desc_shrink.py` 只命中 1/16**——它只查「变短」（<90%×base 且 >30 字），不查「替换且变长」。CC 以「base/v2 互含审计」（互不为子串即列）全量扫出，base 主+增量合并修复（`outputs/cc_qa_fix_20260905.py`）。**预防门禁候选**：check_desc_shrink 增「整段替换检测」模式（互不含即报·人工甄别增量追加），属工具功能新增——待 Doctor 批。**应升格**：同族第 4 次（08-15/08-27/08-30/09-05），按合同登记「应升格通用教训」（LLM 对 update 节点逐节点自由重写事实载体族），升格由 Doctor 裁。**来源**：2026-09-05 帕米尔六篇批入库 QA 场。

## [NOTE-20260814-001] 手工 patch update_nodes 的 `updated_at` 必须放条目顶层（放 properties 里会被静默 kept_base）

**状态**: ✅ 已实证修复 **优先级**: 🟡 中

**触发**: 2026-08-14 NV CPO 量产 patch 首跑 promote，Merge Diff 报 `Nodes Updated (2) (kept_base)`——props 一条没落地、仅 data_sources 追加，且脚本零报错。复读 canonical 才发现 props 未变。

**真因**: `kg_merge._merge_node` 的时戳闸读 `patch_node.get("updated_at")`（**顶层**字段）。DUV 旧样例（`_v3_20260728_国产DUV量产_manual.json`）把 `updated_at` 放进了 properties → 顶层解析为空 → patch_ts=datetime.min < base_ts → 静默走 kept_base 分支。当时无人复读 props，该 patch 的 update 实际从未生效（历史副作用未知，属 ERR-20260718-002 族「宣称完成未核」）。

**规则**:
- 手工 patch 的 update_nodes 条目：`updated_at` 放**顶层**（与 id 同级），properties 只放事实 props。
- patch 落盘前用真函数预检：`from kg_merge import _merge_node; _merge_node(base, u)[1]` 必须 == `"took_patch"`；或 promote 后看 Merge Diff 的 `(kept_base/took_patch)` 标注，kept_base 即未生效。
- 首跑 kept_base 不丢数据（data_sources 已并、边已入、边幂等），修 patch 后二跑即补齐，无需回滚；`_merge_data_sources` 按 (file, reference) 去重，重跑无重复追加。

## [NOTE-20260801-001] 接入 Kimi K3 作审查腿：四个坑与一条真相源（`/v1/models` ＞ 任何文档）

**状态**: ✅ 已沉淀（2026-08-08 复盘补标 · 原标 🟢 已跑通 2026-08-01 · 凭证在 `Database/.env` 的 `KIMI_*`）
- **可用配置（实测）**：`KIMI_BASE_URL=https://api.moonshot.ai/anthropic` · `KIMI_MODEL=kimi-k3` · 认证 **`auth_token=` 与 `api_key=` 两种都收**（官方文档只提 `ANTHROPIC_AUTH_TOKEN`，实测 `x-api-key` 也通）。可直接复用 `anthropic` SDK，**无需适配层**。
- **坑 1 · 模型名带 `[1m]` 是 Claude Code 客户端语法，API 层不认**。官方 `guide/claude-code-kimi` 页给的是 `kimi-k3[1m]`（`/status` 显示的那个名），直接打 API 会 404。**API 真名是裸 `kimi-k3`**。⇒ 文档没错，是**把 CLI 场景的值用到了 API 场景**。
- **坑 2 · `404 ≠ 认证失败`**。Moonshot 用**同一条消息**表示两种原因：`Not found the model X or Permission denied`。看到 404 别急着怀疑 key——它恰恰说明**认证已过**（key 错会 401）。
- **坑 3 · 两个端点模型名不同**。OpenAI 端点 `/v1` 用 `kimi-k3`；Claude Code 文档的 Anthropic 端点写 `kimi-k3[1m]`。照 Quickstart 抄名字去打 `/anthropic` 会踩坑。
- **坑 4 · thinking 关不掉**。`/v1/models` 返回 `supports_thinking_type: "only"`、`reasoning_efforts.default_effort: "max"`。实测 content blocks = `['thinking','text']`，**一个四字回答消耗 output 130 token、其中 thinking 112（约 86%）**。⇒ 按 `$15/M` 输出计价时**必须把 thinking 算进去**；`valid_efforts` 含 `low`，降本可从这里入手（怎么在 anthropic 端点传该参数**未测**）。
- **✅ 真相源**：`curl https://api.moonshot.ai/v1/models -H "Authorization: Bearer $KEY"` 返回**该账号此刻**的模型列表 ＋ `context_length` ＋ `think_efforts` ＋ `supports_thinking_type`。**比任何文档权威**——本次四个坑里有三个是靠它一次定案的。⇒ **接任何新模型的第一步都该是列模型，而不是读文档抄配置。**
- **顺带实测**：缓存命中 `cache_read_input_tokens` 生效（$0.30/M vs $3/M ＝ 1/10 价）⇒ 审查腿应把 system prompt 与 canonical 子图固定在前缀复用。
- **同族**：[[通用教训]] `G-X111`（二手名单/数字）——本条是它在「官方文档」上的变体：**文档是一手的，但「文档写的场景」和「我要用的场景」是两回事**。

## [ERR-20260801-001] LLM 写坏 JSON：11 个完整节点被吞进另一节点的 `aliases` 数组，静默丢失 26 天，连过四批 QA

**状态**: ✅ 已还原+收口闭环（2026-08-13 大活专场还原 · 双 subagent 审查通过；2026-08-15 收口场核验四件）

**结案（2026-08-15 收口）**：① 08-13 已还原——11 节点入图（10 独立 + `device_Delphilaser_TGV` 并入 `company_DRLaser`，旧 id 入 aliases 可逆留痕）+ 15 边 + 6 update + host 字段恢复（`_restored_by: restore_swallowed_nodes_2026_08_13` 留痕 11 节点）。② 08-15 收口四件：QA 六项全绿 + 全图畸形扫描 0；6 个度 0 孤儿补边问答板 10 题 9 批 1 不批（`concept_XinsenOpticalMSAPOrderStatus` 留自然回填）；被困 14 条价格入价格层（817→831）+ host 清 5 个 patch 残留键；provenance 归正 27 处（07.05→07.01 · 会议日期改名批）。canonical **4069/4587**（+9 边）。PRD `logs/checkpoints/2026-08-15_渊图畸形节点还原场_PRD.md`。下方为原始诊断，留档。
- **优先级**：高——**不是数据错误，是数据不存在**；且暴露的 QA 盲区会让同类事故继续无人发现
- **触发场景**：2026-08-01 帕米尔 9 篇入库做沙箱 QA 时，「半空节点」检查揪出 `concept_XinsenBTSubstrateCustomerShare` 顶层 `description=None`，展开才发现病灶。
- **病灶**：该节点 `aliases` 是 **15 元素数组，其中 12 个是 dict**——
  - `[0][1][2]` 是字符串，但 `[1]` = `"兴森BT客户],\n      "`（被截断 ＋ 字面换行）、`[2]` = `"category\": \"场景"`（本该是 key 的文本）
  - `[3]` 是**该节点自己的** `description` / `properties` / `data_sources`（故顶层 description 为空）
  - `[4]~[14]` 是 **11 个完整节点**：`concept_XinsenS3BTExpansionCXMTSamsungLocked` · `concept_XinsenOpticalMSAPOrderStatus` · `concept_XinsenABFSubstrateOrderMix` · `metric_XinsenABFSubstrateRevenue2027E` · `metric_XinsenBTSubstrateRevenue2027E` · `concept_ABFSubstrateDomesticFilmSubstitution` · `company_HongchangElectronics` · `product_XinsenGlassCoreSubstrate` · `concept_BTSubstrateMarginUpsideScenario` · `concept_ABFSubstrateMarginUpsideScenario` · `device_Delphilaser_TGV`
- **实测**：① 这 11 个 id 在 canonical 里**一个都不存在**（丢失 11/11）；② 被吞节点 `created_at` 全为 `2026-07-06`、来源 `2026.07.05-帕米尔研究：封装载板…` ⇒ **07-06 那批入库时就坏了**；③ **全图仅此一例**；④ **07-13 / 07-18 / 07-21 / 07-28 四批 QA 全部漏过**。
- **为何四批 QA 全漏**：8 项校验查的是**悬挂边 / 自环 / 重复边 / 非法边 type / 非法点 type / 大小写重复 / 半空 / 超集断言**——**没有一项查 JSON 结构合法性**。畸形节点在结构校验眼里是「一个 type/name 齐全、只是 description 为空」的正常节点。
- **连带**：`device_Delphilaser_TGV` 正是 `brain/渊图/architecture/系统概览.md`「前缀治理 · 未决：待帝尔激光命名治理批」指向的节点——**它根本不在图里**，那条待办一个月来指向一个不存在的实体（且 `type=company` 而前缀 `device_`，还原时一并归正）。
- **解决方案（未执行）**：把 `aliases[3]` 的字段提回顶层；`aliases[4]~[14]` 还原为独立节点；`aliases` 只留两个真别名。**还原前必须先判**：canonical 悬挂=0 暗示指向这 11 个的边也一并丢失 ⇒ 大概率是 **11 个孤儿节点（度 0）**，补边需逐个对原文，是内容工作非机械还原。
- **预防措施（该做但未做）**：**给沙箱 QA 加第 9 项——数组字段元素类型断言**。`aliases` 的元素必须是 `str`；`data_sources` 的元素必须是规定形状的 dict。出现「整节点」立即报。一行 assert 的事，却是这 26 天里唯一能发现它的方式。
- **同族**：`ERR-20260721-002`（LLM 造孤儿边/非法 type 复发）——同为「LLM 产出畸形、靠 QA 兜」，但那些 8 项查得到，本条查不到。与 [[通用教训]] `G-X118`（静默成功）同构：**改动写进了一个真实存在、看起来正常、却没人读的位置**。

## [NOTE-20260728-001] 贴出的入库命令＝已启动的开关——贴命令后不得再穿插会改 canonical 的手工 patch 流程
**状态**: ✅ 已沉淀（规则已立 2026-07-28 · 2026-08-08 复盘补标）
**类型**: 📝 流程教训（CC 协作·并行基线）**优先级**: 🟡 中

**触发**: 2026-07-28 CC 上一轮把 6 篇 batch 命令贴给 Doctor 后，本轮又与 Doctor 走「DUV 追新闻→手工 patch→promote」流程，且指令写「先 patch 后 batch 串行」。实际 Doctor 已按前一轮贴的命令起跑 batch（03:02 出 _v2·基线 3474），DUV patch 03:06 才落 canonical（→3476）——_v2 不含 DUV，直接 promote 会丢 +2 节点/+5 边。**07-06 CoWoS 并行基线坑的复现**，只是这次两个动作都出自 CC 自己贴的命令。

**处置**: CC 沙箱把 DUV patch 叠合到 _v2 之上生成 final，断言 final ⊇ canonical（零丢失）+ 8 项 QA 后才放行 promote。另：kg_merge_safe 被双跑（多行粘贴/重复粘贴），幂等 Δ+0 无害——幂等性再次兜底（NOTE-20260617-001 族系），但不能指望每个脚本都幂等。

**规则**:
- **命令一经贴出，就当它已被执行**——之后若要插入任何会改 canonical 的手工 patch，必须先与 Doctor 确认前一条命令是否已跑/正在跑，或改为把 patch 排到 batch 收口之后；
- 凡「手工 patch 与 batch 同日并行」，promote 前必做**三方计数对账**：pre-batch 基线 vs _v2 vs 当前 canonical——canonical ≠ _v2 的 base 即触发叠合流程（patch 合到 _v2 之上 + 超集断言），沿 07-06 CoWoS 先例；
- 时序判定用**磁盘证据**（backups 时间戳、_v2 文件名时间、index mtime），不靠会话记忆推断（NOTE-20260719-001 同源）。

## [ERR-20260721-001] promote 门无 `set -e` → 结构断言失败仍 `cp` 覆盖，脏图被放行到生产
**状态**: ✅ 已解决（2026-07-21·修门 + 按备份链回退重跑）**优先级**: 🔴 高

**触发**: 帕米尔 8 篇入库的 promote 环节，结构断言已判定不通过，但脚本仍继续执行到 `cp` 覆盖 canonical，把未过校验的脏图放行到生产图谱。

**真因**: promote 脚本未 `set -e`（或关键断言未 `exit 1`）——断言失败只打印告警不中断流程，后续 `cp` 无条件执行。**「校验通过」与「cp 覆盖 canonical」之间没有硬闸**，校验形同虚设。

**处置**: 按备份链回退（`bak_pre_promote_20260721_093535`），修 promote 门（断言失败即中断、绝不触达 cp），重跑至 8 项结构 QA 全绿再落盘。

**预防**:
- promote / 合并 / 覆盖类**破坏性脚本一律 `set -euo pipefail`**，关键断言失败显式 `exit 1`；
- 在「校验」与「cp 覆盖」之间加**硬闸**：断言不过绝不触达落盘命令；
- 同族教训——烛照九阴 S2 ERR-20260721-001（zhuzhao grade_section 静默吞噬）同为「**失败必须 fail-loud、不得静默继续**」，跨项目同一天两次栽在静默失败上，值得作为通用戒律。

## [ERR-20260721-002] LLM 造孤儿目标边 / 啰嗦公司 id / 非法边 type + 非法点 type 复发 → 沙箱 8 项 QA 拦下
**状态**: ✅ 已解决（2026-07-21·沙箱 8 项 QA 定点修 5 边 / 3 点）**优先级**: 🟡 中

**触发**: 帕米尔 8 篇入库后跑沙箱 8 项结构 QA，逮到入库 LLM 复发的多类结构缺陷。

**症状**:
- **孤儿目标边**——边指向未建的节点；
- **啰嗦 / 不规范公司 id**——富信电子 id 归正（股票代码 688662）；
- **非法边 type + 非法点 type**——超出 schema v3 允许集。

**处置**: 沙箱 8 项 QA 全部拦在 promote 之前，定点修 **5 边 / 3 点**后再放行；点 type 归正、结构 8 项全 0。

**预防**:
- 这是 **ERR-20260624-001 族系（LLM 结构缺陷）的又一次复发**——沙箱 8 项 QA 是 promote 前最后一道拦网，**不可跳过**；
- 与 ERR-20260721-001 **配套才闭环**：QA 拦得住的前提，是 promote 门真的会因断言失败而中断——门若漏（ERR-001），QA 逮到也白逮。

**追记 2026-09-05（同族复发 · 六篇批 · 三型全犯）**: ① **孤儿目标边 6 条**——4 条 id 错形（`company_TFC`→`company_TFCOptical` · `company_Mellanox`→`company_NvidiaMellanox` · `concept_1p6TOpticalModulePowerRange` 误造×2→`product_1dot6TOpticalModule`）+ 2 条引用未建节点（`company_AAOI` 被 3 条边引用却未建节点→QA 补建公司节点）；② **方向反置 3 条（新形态）**——「A 委托 B 代工」被写成 A -supplies-> B（Coherent→天孚、AAOI→汇绿、AAOI→德科立 全反），**desc 里写着正确关系、8 项结构 QA 查不出**，须语义核（本场凭 desc-方向矛盾逮到）；③ 半成品节点 1 个（`concept_NvidiaRubinOrthogonalBackplane` type/name 双空·无 span·与存量 `concept_NVOrthogonalBackplane` 重复·NOTE-20260826-001 同族）→ 删节点+事实并入存量。全部拦在 promote 前修复。**预防门禁候选**：supplies 边 desc 含「委托/代工/下达订单」时校验 desc 主语==source（方向语义核并入 QA 清单）——待 Doctor 批。**来源**：2026-09-05 帕米尔六篇批入库 QA 场。

## [ERR-20260719-001] 二次生成摘要的相对年份系统性偏移 → 入库 LLM 不做统一裁决、逐节点各自猜 → 同篇内**混合污染**
**状态**: ✅ 已归正（2026-07-19，7 节点 / 3 边，canonical 3384/3903 守恒）**优先级**: 🔴 高

**触发**: Doctor 阅读 `2026.07.18-国泰海通：超节点产业化突破与技术演进.md`（P2）时发现「大量混入 25 年时间节点，同时使用未来/预期，弄不清是过时信息还是笔误」。

**真因（两层，缺一不可）**:
1. **raw 层**——该篇 §1-9 摘要为二次生成，把专家原话的「今年 / 明年 / 去年」系统性映射为 **2025 / 2026 / 2024**，**整体倒退一年**。16 段 A 答案正文**零个绝对年份**（全为相对表述），所有绝对年份都是摘要层自己加的。
2. **入库层**——`kg_ingest` 面对「摘要说 2025 / 文件名 2026.07.18」这一矛盾，**没有做统一裁决**，而是逐节点各自猜：产出了错的 `concept_SupernodeMarketScaleChina2025`，同时又产出了对的 `metric_B300ServerPrice.price_2026h1`。

**★ 危险点：混合污染比全错更难查**。全错会显得突兀，混合污染里对的那部分反而给错的那部分背书，肉眼扫一遍容易判「大体没问题」。与 ERR-20260718-001「分裂型幽灵」同族——**同一篇里部分对、部分错，是渊图目前最难自动发现的一类**。

**核实方法（可复用）**: 用**外部硬锚**反推相对年份基准，四项一致才采信——① 昇腾 950PR 2026-Q1 推出、2026-04 量产（文中「已小批量供货」）；② 950DT 原定 2026-Q4、现确定 8 月上线（文中「8 月拿商用片、9 月末–10 月中下旬批量交付」）；③ 智谱 GLM-5.2 于 2026-06 发布（文中「下半年若出现 GLM 5.2 级别爆点」）；④ x86 CPU 2026 年两轮涨价累计 40%-50%（文中「今年已涨价两轮」）。→ 确认 **今年=2026 / 明年=2027 / 去年=2025**。
另有**内部自证**：摘要 §6 写「2026 年行业最大问题在供给侧」，其对应 Q10 原话是「**明年**行业最大的问题…」，在「今年=2025」假设下二者不可能同真。
另有**同批语料旁证**：`2026.07.12-超节点交换机`篇同样用今年/明年，入库时被正确解读为 2026。

**处置**: raw 摘要层 13 处 +1 年归正 + 顶部加校勘头（Q&A 段未动）；图谱走 `mapping/fix_guotai_year_20260719.py`——4 节点改 id（旧 id 入 aliases）+ 3 边端点同步（边 id 留旧）+ 7 节点 1 边 name/desc/props 归正 + `_meta.年份归正_20260719` 审计留痕。守恒 3384/3903、旧 id 零残留、非目标对象逐字节守恒。

**预防**:
- ① **凡 raw 是「二次生成摘要」而非逐字纪要，入库前必先做相对年份基准校验**——判据：正文出现绝对年份但同篇 Q&A/正文用相对词，即为高危；
- ② **凡节点 id 带年份，入库后比对该年份与来源文件名年份**，差值 ≠ 0 即人工复核（本例四个节点差值分别为 −1/−1/−1/−1，机器一扫即出）；
- ③ 入库 LLM 遇到「文档内年份」与「文件名年份」冲突时**不应逐节点自由裁量**——考虑在 prompt 里显式给出文件日期并要求统一基准，或后处理告警（沿 ERR-20260718-001「prompt 是请求、后处理是保证」的结论）；
- ④ 高时效判断先看**外部硬锚**（产品路线图 / 发布时间 / 涨价周期），别只靠文内自洽。

**Q10 标题特例（Doctor 2026-07-19 裁定改）**: Q&A 段唯一的绝对年份出现在 **Q10 标题**「是否会卡住 2026 年的交付」，而 A10 答的是「**明年**…」。值得留意的是，这处**表面上是支持「今年=2025」的反向证据**（若今年=2025，问 2026 而答「明年」恰好自洽）。判为偏移残留的理由：① 四项外部锚是硬事实，Q10 标题是软推断，不能用软的推翻硬的；② Q 标题带脚注编号、系二次归纳而非专家原话；③ 16 段 A 正文一个绝对年份都没有，唯独 Q 标题冒出一个，形态上更像转换产物。**已改为 2027 年**。
**方法论留痕**: 遇到与主结论相冲的单点证据，**先分清它是硬锚还是软推断**再决定权重，不要因为「有反例」就动摇整条证据链，也不要因为结论已定就把反例藏起来不报。

## [NOTE-20260719-001] 档案把「已完成」记成「未决」——待办清单的过时方向与 ERR-20260718-002 相反，同样危险
**状态**: ✅ 已沉淀（规则已立 2026-07-19 · 2026-08-08 复盘补标）
**类型**: 📝 流程教训（档案卫生）**优先级**: 🟡 中

**触发**: 2026-07-19 Doctor 说「都做」，CC 准备执行挂在档案里的「会议日期改名批（32/276 篇待对齐）」。跑 dry-run 得到 **「没有需要改名的文件」**。

**真相**: 该批 **07-18 当天 11:48 / 11:59 已两次 `--apply` 执行完毕**，`backups/` 里躺着 `行业知识图谱_完整数据库.json` / `index.json` / `commodity_prices.jsonl` 三面各两份 `bak_pre_rename_meeting.20260718_*` 为证。实测 276 篇 md 中 32 篇正文带会议日期、**与文件名 100% 一致（不一致 = 0）**，正是改名后的应有状态。档案记的「32/276 篇**待对齐**」是把「32 篇带会议日期」误写成「32 篇不一致」，且做完后没回写状态。

**为何值得单独记**: ERR-20260718-002 记的是「**做了的事被并发会话回退**」；本条是它的**镜像**——「**做完了但档案还写着未决**」。两者方向相反，危害却同构：前者让人以为做了其实没做，后者让人以为没做其实做了。后者若不先核实就照做，轻则空跑，**重则对已处理数据二次施加同一变换**（改名批若真有匹配项，二次跑会把已对齐的日期再挪一次）。本次是脚本的幂等性（检测到 0 命中即退出）兜住了，不能指望每个脚本都这么写。

**规则**:
- **执行任何挂在档案里的待办前，先跑 dry-run / 先查 `backups/` 有无同名 tag**，用**磁盘证据**确认状态，不信档案的文字描述。
- **破坏性批处理脚本必须幂等**：先检测再动手，0 命中即干净退出，不做无条件变换。
- 档案里的数字型待办（「N 篇待处理」）**写清楚 N 的口径**——本例「32」实为「带会议日期的总数」，被读成「不一致的数量」，一字之差。
- 批次做完**当天回写档案状态**，与「入库后自动同步档案」（2026-06-24 Doctor 定）同等对待。

**附带查法留痕（可复用）**: 判断某篇 provenance 缺失是不是本次操作造成的，**比对操作前后两版图谱**——「操作前无、操作后也无」＝ 历史孤儿（ERR-20260608-003 族系），与本次无关；「操作前有、操作后无」＝ 本次漏同步。本例 5 篇缺口经此法确认全属前者，改名批五面同步无遗漏。

**追记 2026-08-22（第四实例 · 渊图 08-19 具身智能线手术）**: 手术分两阶段执行——stage1 移出 119 节点/147 边 → 4964/5542；embodied2 patch 续按门禁移启元族 4 节点/3 边 → 终态 **4960/5539**。档案（系统概览/决策记录）只回写 stage1 数字，直到 08-20 调研情报局场实测 base 4960/5539 才暴露 −4/−3。证据链：commit `a58e35c` message 自证「canonical 4960/5539 · 墓碑123节点150边」+ 墓碑文件实测 removed_nodes=123/removed_edges=150 + 双快照（`bak_pre_patch_embodied2_20260819_070307`=4964/5542 vs `bak_pre_gsprops_20260819_084355`=4960/5539）差集恰为启元族 4 节点 3 边。**教训增量**：多阶段手术/批次的档案回写必须以**最终 commit 的计数**为准，不得以中途快照数字回写；commit message 里的计数是自证锚。

## [ERR-20260709-001] kg_ingest 自动 base 查找不扫 mapping/ → 新终端未设 KG_BASE_JSON 即失败
**状态**: ✅ 已解决（绕过）**优先级**: 🟡 中
**要点**: 新登录 shell `python3 kg_ingest.py --batch` 报「未找到知识图谱 JSON」。根因 `find_latest_kg` 只扫 `~/Downloads`+行业研究根、**不扫 `mapping/`**，而 canonical 在 mapping/ 下；历史靠 profile 里 export `KG_BASE_JSON` 才隐性跑通。修：命令默认带 `--base mapping/行业知识图谱_完整数据库.json`（不依赖环境变量）。**详**: `Database/行业研究/渊图_GOTCHAS.md` [ERR-20260709-001]

## [NOTE-20260709-001] CC 拼既有工具命令别从源码 grep 臆造参数——先查历史日志实敲命令
**状态**: ✅ 已沉淀（规则已立 2026-07-09 · 2026-08-08 复盘补标）
**类型**: 📝 流程教训（CC 协作）**优先级**: 🟡 中
**要点**: CC 拼渊图入库命令两次臆测两次错（文件列表式命令 vs 真实 `--batch` 扫目录；`DEEPSEEK_API_KEY` vs 真实 `KG_API_KEY`），根因都是从散落/过时源码 grep 拼参数、没核 main() 也没照历史实敲命令。取信序＝历史 logs 实敲命令 > `--help`/main() 现行 argparse > 源码推断。附元教训：落盘类动作宣称完成前必 grep/stat 复核（本坑上轮曾假完成）。**详**: `Database/行业研究/渊图_GOTCHAS.md` [NOTE-20260709-001]

## [NOTE-20260702-002] 渊图BT基板产业链A股缺口——供应商节点全为台股
**状态**: ✅ 已知约束（缺口如实登记 2026-07-02 · 待国产 BT 标的语料补上时回填升级为有解 · 2026-08-08 复盘补标）
**类型**: 📝 数据缺口（如实记录）**优先级**: 🟡 中
**现象**: 查"BT基板对应公司"时，图谱里 BT基板的直接 supplies 节点（欣兴电子 Unimicron、南亚电路板、景硕科技）全是台湾上市公司，**没有任何一家纯正 A 股 BT基板标的**。
**处理**: A股这条线只能靠兴森科技（长鑫是其BT载板第一大客户，锁定S3工厂一半产能）和深南电路（存储相关BT基板需求助力广州基板厂盈亏平衡）的BT关联业务间接覆盖，不是独立一批公司。按数据真实性铁律**如实告知缺口，不强行拉一家不精确的A股标的凑数**。
**预防**: 未来做"BT基板对应A股公司"一类检索时，直接引用本条，不必重新 search 一遍才发现缺口；若后续帕米尔/研报语料补上国产BT基板玩家（如兴森/深南以外的独立标的），及时回填本条并升级为有解状态。

## [NOTE-20260702-001] ABF载板三套梯队口径易混淆，须分开引用
**状态**: ✅ 已沉淀（口径澄清 2026-07-02 · 2026-08-08 复盘补标）
**类型**: 📝 认知澄清（非错误）**优先级**: 🟡 中
**现象**: "ABF载板第一梯队"这个问法背后其实挂着图谱里三套不同维度的梯队节点，容易被误当成同一件事引用：
1. **全球ABF载板第一梯队**（技术/产能双料龙头）：揖斐电 Ibiden（"全球领先ABF基板供应商"）、新光电气 Shinko Electric（节点原话"属于全球第一梯队"）、欣兴电子 Unimicron（属性直接标 `market_position: 第一梯队`）。
2. **国产ABF载板厂商竞争格局**（华为海思供应链内部口径，节点 `国产ABF载板厂商竞争格局`）：`hisilicon_tier1_supplier`=兴森科技（24层/系统良率85%）、`tier2`=深南电路（20层/良率82%）、`tier3`=迪景半导体（珠海越亚）。节点原文明确"与国际一线大厂在良率和层数上仍有约一至两年的差距"——国产Tier1不等于全球第一梯队。
3. **mSAP光模块PCB竞争格局**（节点 `光模块PCB竞争格局（mSAP）`，服务1.6T光模块而非CPU/GPU封装载板）：Tier1=鹏鼎、深南电路、欣兴/景硕；Tier2=方正科技、胜宏科技、生益科技、景旺电子。深南电路和欣兴电子在这条线上也是Tier1，但产品和客户群与ABF封装载板不同。
**预防**: 引用"ABF载板梯队"前先确认问的是哪一套口径（全球 vs 华为供应链内部 vs mSAP光模块PCB），三者节点独立、不能互相替代引用，尤其"国产Tier1"不能直接等同"全球第一梯队"。

## [NOTE-20260628-001] update_nodes/update_edges 改 properties 必带 updated_at，否则深合并不生效
**状态**: ✅ 已沉淀（合并语义规则已立 2026-06-28 · 2026-08-08 复盘补标）
**类型**: 📝 数据卫生（合并语义坑）**优先级**: 🟡 中
**触发**: 2026-06-28 央视华工入库 patch，A·`concept_COUPEGen2Production` update_node 只写 id+properties+data_sources（未写 `updated_at`）。kg_merge_safe dry-run 报 7 改、看似成功，但 in-memory 读盘核验发现 COUPE 新 props **没合进去**（仍 4 个），仅 data_sources 并了（1→2）。
**真因**: `kg_merge._merge_node` 按 `updated_at` 判新旧——patch 无 updated_at → `_parse_ts("")` 视为极早 < base_ts → 走 **kept_base** 分支（只 append data_sources、**不调 `_deep_merge_dict_fields`**）。NOTE-20260626-001 的深合并只接在 **took_patch** 分支。同批 `company_HGTech` 因 base 本身无 updated_at（两边都空、不满足 patch_ts<base_ts）才侥幸走 took_patch、props 正常合并——纯属巧合。
**解决**: 给两个 update_node 补 `updated_at=2026-06-28`（≥base）→ 强制走 took_patch → COUPE props 4→8 正确深合并、描述/其余字段不动、HGTech 旧 props 全保留。
**预防**: ① **凡 update_nodes/update_edges 改 properties/_meta，patch 必带 `updated_at` 且 ≥ base 的 updated_at**，否则深合并静默失效；② 落盘前别只信 kg_merge_safe 的 diff 动作标签（kept_base/took_patch），必 **in-memory 跑 merge(dry_run=False) 读盘核验目标子键真在**（注意 `merge(dry_run=True)` 只算 diff、不返回已应用图，核验要用 dry_run=False 的内存结果，不写盘）。属 NOTE-20260626-001 族系。

## [FIX-20260625-001] 中兴微张冠李戴：误记「中科曙光旗下」实为中兴通讯子公司（ERR-20260602-001 族系）
**状态**: ✅ 已 apply 落盘（2026-06-25，canonical 2700/3248，读盘核验全绿：错边 target=company_ZTECorp、desc 已改中兴通讯、0 重复 0 悬挂）**优先级**: 🟡 中
**触发**: F9000 入库 kb 查重时撞见——`company_ZTEMicro`（中兴微）description 写「中科曙光旗下交换芯片公司」+ 错边 `rel_ZTEMicro_Dawning`（中兴微 --part_of--> 曙光；_meta relabel_2026_05_16 还以 0.95 置信"误确认"该隶属）。
**核查/解决**: 2026-06-25 联网坐实 中兴微（Sanechips，深圳市中兴微电子）= 中兴通讯（ZTE，000063）控股子公司，前身 1996 年中兴 IC 设计部，与曙光无隶属。图谱已有 `company_ZTECorp`（中兴通讯）作正确锚。错源 = 2026-05-03 国产交换芯片研报把集采名单「中兴/华为/盛科」的"中兴"误并曙光。id/name/aliases 本就对，错的仅 description 与边 target。patch `mapping/_v3_20260625_ZTEMicro_fix.json`：update_nodes 修 description + 补 parent/stock_code；update_edges 把 `rel_ZTEMicro_Dawning` 的 target 改指 `company_ZTECorp`、desc/evidence 同步、_meta 记 supersedes；边 id 留旧（Doctor 定·仅内部标签）。Δ +0/+0，dry-run took_patch✅。
**预防**: 入库后跑 `name_code_consistency_check`；研报里集采/名单类多公司并列（中兴/华为/盛科）易被 ingest 误并到相邻实体——建公司隶属（part_of）边前核 evidence 原文 + 联网坐实母子关系。

## [FIX-20260623-001] 张冠李戴修正须 name/aliases/边/desc 全字段同改（非只改 description）
**状态**: ✅ 已立规 **优先级**: 🟡 中
**触发**: `metric_ShengyiElectronicsRevenueForecast` 06-18 修张冠李戴时只改了 description（胜宏→生益电子）+ _meta，但 name「胜宏科技收入预测」、aliases[胜宏/VG/300476]、`measured_by` 边 source=`company_VictoryGiant`(胜宏) 全未改 → name_code_consistency_check 每次 recheck 持续报 2 条告警，入库 batch 也带出告警。
**核查/解决**: 2026-06-23 联网坐实 Shengyi Electronics=生益电子 688183（纯 PCB 厂·Nomura BUY/TP RMB90·上调 2026E）、胜宏=Victory Giant 300476；归位：id 本就 `ShengyiElectronics` 语义正确**不动**，只归正 name/aliases + `measured_by` 边 source→`company_Shengyidianzi` + 两边 desc 胜宏→生益电子 + _meta 审计。告警清零。
**预防**: 修近名/张冠李戴节点时，**name + aliases + 引用边(source/target/desc) + description + properties.stock_code 全字段一并核改**，不能只改 description；改完必跑 `name_code_consistency_check` 确认清零。属 ERR-20260602-001 / FIX-20260619-001 族系。

## [FIX-20260619-001] 公司实体辨识坑：近名/英文名张冠李戴 + 母子混挂（ERR-20260602-001 族系总条）
**状态**: ✅ 已批量清（dedup 54 簇审阅 commit `1e55bee`）**优先级**: 🔴 高
**触发**: V4 Pro 入库时按英文名/拼音建公司节点，常把**另一家公司的英文名**当 id 或 name，或把母子/同集团公司事实混挂到一个节点。本轮深度审阅查实多例：
- **id 英文名指向另一家公司**（张冠李戴）：`company_Eoptolink` name 标"中际旭创"实为**新易盛(300502)**（Eoptolink=新易盛）；`company_IluvatarCoreX` name 标"燧原科技"实为**天数智芯**（Iluvatar CoreX=天数智芯，8 条边错记到燧原账上）；`company_NewPhotonics` name 标"光迅科技"实为**以色列硅光初创**（与光迅 Accelink 002281 无关）；`company_Taiyo` 的 alias"Taiyo"实为**太阳诱电**（节点本体是台光电材 EMC 2383）；`company_TongfangPhotonics` id"同方"误导（本体是光库科技 300620）。
- **母子/同集团混挂**：`company_Shengyi`（生益电子 688183）历史混挂 8 条**胜宏科技(300476)**边 + 3 条**生益科技(600183)**边——胜宏当时无独立节点。
- **错 alias**：`company_Xinxing` 挂"景硕"（景硕=Kinsus 3189 是另一家）；`company_BoqianNewMaterials` 描述串"铂科新材"（铂科 300811≠博迁 605376）。
**核查/解决**: 张冠李戴**禁按边数自动选 survivor**（会把对的边并进错实体）；必**逐边读边描述定归属 + 联网坐实英文名↔实体**，再决定改名/拆/并。本轮：Eoptolink→新易盛＋拆易飞扬建 Gigalight＋1017 布归旭创；IluvatarCoreX 8 边并入既有 `company_Tianshu`、伟测 FT 归燧原；生益电子拆出胜宏 `company_VictoryGiant`。
**预防**: ① 建公司节点前 kb 查重（同实体异 id）；② 入库后跑 `name_code_consistency_check`；③ 易混中文公司 id 用「4 字简称全拼」（见通用教训 G-X22）；④ 登记易混英文名对照表（Eoptolink=新易盛 / IluvatarCoreX=天数智芯 / Enflame=燧原 / NewPhotonics=以色列 / Taiyo=太阳诱电 / 光库=Advanced Fiber Resources / 光迅=Accelink）。

**追记 2026-08-28（景旺↔鹏鼎混标 · 同族第 N 次复发 · C 档手术修复）**: 3 条边 `rel_Jingwang_*` id 带景旺、source 却挂 `company_Pengding`（鹏鼎）、desc 全系景旺（08-20 景旺调研真源）——LLM 把景旺信息挂到另一 PCB 厂鹏鼎节点上；连带 `rel_Jingwang_RubinMidplane` 把 Rubin Midplane 挂到人形机器人 `product_Midplane`（同名歧义）。C 档手术已修（重指+歧义重指+去重合并+删 2 污染边，墓碑可逆）。同族复发已满足升格条件（海光/海思/生益/胜宏/光迅/鹏鼎-景旺…），**✅ 2026-08-28 Doctor 裁「升格通用教训」→ 已登记 [[通用教训]] G-X161（CC 执行留痕）**。

## [NOTE-20260617-001] kg_merge_safe --apply 日志"Δ+0/skipped"是幂等噪音，须读盘核验
**状态**: ✅ 已沉淀（认知澄清 2026-06-17 · 2026-08-08 复盘补标）
**类型**: 📝 认知澄清（非错误）**优先级**: 🟡 中
**现象**: 跑 `kg_merge_safe.py <patch>`（非 dry-run）落盘第二批时，日志同时报"Nodes Skipped (3): ID 已存在→改为 update""Edges Updated/Skipped""Δ +0 节点/+0 边"，又报"合并后 canonical: 2383/2882"——自相矛盾。
**真相**: 实际落盘**正确**（2380/2876 → 2383/2882，+3/+6）。日志的 skipped/Δ+0 是 merge 报告逻辑的幂等性噪音（疑似对已合并的中间态又比了一次），**不代表没写入**。
**规则**: 落盘后**别信合并日志的增量数**，一律**读盘核验**——`json.load` canonical 数实际节点/边数 + 断言新节点/新边在库 + 0 悬挂/0 重复/边 id 唯一。三批均按此核验通过。
**预防**: promote 工作流固定加"读盘核验"步（见 [[经验库]] EXP-20260617-004-P）。

**追记 2026-09-01（知芯批 · 幂等兜底救命实例）**: 知芯小批入库命令块被重复执行——01:05 完整跑过（promote+commit `07a8bccd` 成功）、02:19 又贴一遍；第二遍 kg_merge_safe 全部走「ID 已存在→改为 update」幂等路径，Δ+0/+0、canonical 等价、三元组重复 0、备份 `bak.20260901_021950` 冗余无害。证据=reflog 时间戳+双备份件。警示不变：幂等兜底救了场，但「命令块重复执行」模式本身有风险——换不幂等的脚本就是另一回事（与 NOTE-20260728-001「贴出的命令=已启动的开关」同族）。

## [FIX-20260617-001] raw/ 被 .gitignore 忽略 → 视角层提炼成品须放 wiki/(tracked)
**状态**: ✅ 已处理 **优先级**: 🟡 中
**触发**: 投知君君视角层先把"产业逻辑 raw 摘录 + 反共识纠偏录"放 `raw/视角/投知君君/`；Doctor 第一批 commit 时 git 提示 `raw` 被 .gitignore（第16行 `raw/`）忽略——提炼成品没进版本控制、只在本地。
**核查**: raw/ 全局 ignore 是设计（原始字幕/暂存料不入 git，老石谈芯 raw 同样不跟踪）；但**提炼成品价值高于原始料**，不该随 raw/ 被忽略。手工 patch json（mapping/_v3_*manual.json）同样被 ignore，属预期（canonical 为已提交真相）。
**解决**: 提炼成品（`_产业逻辑raw.md` / `_反共识纠偏录.md`）`mv` 进 `wiki/视角/投知君君/`（wiki/ tracked），卡片 source/INDEX 引用同步改向；raw/视角/投知君君/ 仅留 README 指针。
**预防**: 视角层"提炼成品进 wiki/（tracked）、原始料留 raw/（ignored）"作为归位铁律。

## [ERR-20260614-002] relation 旧字段历史遗留（schema v3 称已删实未净）
**状态**: ✅ 已净化（2026-06-24，一次性脚本删 2755 条，type 逐边断言不变）**优先级**: 🟢 低
**结案（2026-06-24 复盘 P2）**: 删 relation 死字段 2755→0；节点/边数不变 3263 条、type 字段 100% 覆盖且逐边比对未动、边 id 顺序不变。备份 `backups/…bak_pre_relclean.20260624_142719`。下方为原始诊断，留档。
**触发**: 2026-06-14 帕米尔7篇入库做全图 8 项校验时，发现 2862 条边里 2777 条仍带 `relation` 旧字段（值如 relates_to/evolves_from/used_in）
**核查**: canonical=2777 / _v2=2777 → **本批 0 新增**；属 canonical 既有遗留。schema v3 决策记录称"relation 字段删除 1155 条"，但实际仅删了"同时有 type+relation 的那批"，大量边的 relation 字段从未清。权威字段 `type` 全图干净（0 非法 type、11 种 schema 内），下游 wiki/kb 均读 type，故不影响分析正确性
**绕过**: 入库 QA 只校验 type 字段；relation 视为死字段忽略
**根治待办**: 若要彻底净化，写一次性脚本 `del e['relation']`（全图扫，注意先备份+断言 type 不动），与 schema v3 决策对齐。非紧急
**详**: 本批未动，留待专门 pass

## [NOTE-20260614-001] kg_ingest --batch 的 _v2 输出是全量图，非增量 patch
**状态**: ✅ 已沉淀（认知澄清 2026-06-14 · 2026-08-08 复盘补标）
**类型**: 📝 认知澄清（非错误）**优先级**: 🟢 低
**要点**: `kg_ingest.py --batch --base <canonical>` 的输出 `mapping/_v2_<ts>_N篇.json` 已是 base+增量**滚动合并后的全量图**（含全部 canonical 节点/边 + 新增），不是 add_nodes 式增量 patch。因此：① 所谓"merge 入 canonical"实为**带备份的 promote**（断言全量图 ⊇ canonical 后覆盖）；`kg_merge_safe` 的 patch 格式闸（要 add_nodes 四键）**不适用**于全量图；② QA 时 delta = `_v2 − canonical`（集合差算新增），8 项校验直接跑全量图。
**实例**: 2026-06-14 帕米尔7篇，_v2=2365/2862 = canonical 2286/2786 + 79/76；CC 修补后 promote 到 2367/2860。下次 batch 别再把 _v2 当增量 patch 喂 kg_merge_safe。

## [ERR-20260531-002] kg_merge 默认不回写 canonical，多 patch 必须链式
**状态**: ✅ 已解决 **优先级**: 🔴 高
**触发场景**: 同日多 patch 各自以原始 canonical 为 base 分别 merge → 后者不含前者节点，merge 报"新建/更新 0"，节点丢失
**解决方案**: 链式 merge（前者 `--output` 临时文件当后者 base，末条 `--output` 回写 canonical），merge 后核对节点/边数等于预算值
**预防措施**: 报告"Doctor 操作"节给链式命令+预期数字；"新建/更新 0"视为告警
**详**: Database/行业研究/渊图_GOTCHAS.md

## [ERR-20260531-003] kg_ingest max_retries=0 致端点抖动时整批全跳过
**状态**: ✅ 已解决 **优先级**: 🔴 高
**触发**: batch 21篇 PDF 每篇~10s Connection error, 0 patch
**真因**: 端点瞬时抖动 + max_retries=0 不重试(非key/PDF/参数问题, 已 curl+诊断脚本 C1-C4 排除)
**解决**: client 加 max_retries=4(KG_MAX_RETRIES可覆盖)+timeout=120; 幂等安全(失败篇未标kg_processed,可重跑)
**预防**: LLM客户端永不 max_retries=0; 整批0 patch=基础设施故障先测端点
**详**: Database/行业研究/渊图_GOTCHAS.md

## [ERR-20260602-001] 生益/胜宏近名张冠李戴(3处)+名↔代码校验脚本
**状态**: ✅ 全闭环（2修+拆分落地+建校验；原「Shengyi_PCB 提案待apply」子项 2026-06-25 核 canonical 确认已并/拆净）**优先级**: 🔴 高
**触发**: ingest混淆 生益(Shengyi)/胜宏(Shenghong)拼音 + 生益科技600183(母CCL)/生益电子688183(子PCB)母子公司
**3错节点**: ShengyiElectronics·Shengyi_PCB→均已并/拆净（2026-06-25 核 canonical：两旧 id 皆不在；现 company_Shengyidianzi 生益电子 + company_VictoryGiant 胜宏 独立并存，FIX-20260619-001 拆分落地）;真胜宏Shenghong(300476)独立
**解决**: 建 rules/name_code_consistency_check.py(代码↔name+拼音↔name自洽校验);入库后跑作delta gate
**预防**: 易混公司登记校验表;修正走dry-run+防误伤断言(禁动生益科技/真胜宏)
**详**: Database/行业研究/渊图_GOTCHAS.md

**⇒ 2026-08-31 同族新实例追记（CC 实读 canonical · Doctor 中微提问场）——中微公司三节点并存**：`company_Zhongwei`（度 9 · 04-03 建 · aliases AMEC/688012.SH · 富节点）/ `company_AMEC`（**度 0 孤岛** · 08-16 建 · desc「国产半导体设备龙头，受益于长鑫扩产」）/ `company_AMEC_TSV`（度 1 · 08-16 建 · HBM TSV 深硅刻蚀语境）——三节点 name 同为「中微公司」、aliases 均含 AMEC、无墓碑无合并记录。**根因**：08-16 Boss老白 198 篇批入库时 LLM 建公司节点前查重不充分（同批已有 HBF 伪公司 5 节点、长江存储双胞胎先例，均已并入本体）。**影响面**：中微的边分散三 id（9+0+1），kb 检索/聚合/wik 卡按 id 漏记；度 0 孤岛节点零引用。**建议修法**：并三为一（度高者 company_Zhongwei 主 · desc 并入 · 旧 id 入 aliases · 边重指 · 墓碑）——沿 08-28 C 档手术范式，手术动作归 Doctor 令。**预防门禁候选**：kg_ingest 新建公司节点时 aliases ∩ 存量 aliases 非空即判撞存量转 update（现仅 LLM 自行查重，AMEC 对 Zhongwei 未认出）。**⇒ 2026-09-01 /todo Doctor 裁「中微手术现在做」→ 已执行**：并 company_AMEC（度0）+company_AMEC_TSV（度1）入 company_Zhongwei（度 9→10）· desc/aliases/data_sources 并集（aliases 增「中微半导体」）· 1 边重指（rel_company_AMEC_TSV_process_HBM_TSV source→Zhongwei）· 墓碑 `_tombstones/2026-09-01_zhongwei_merge.json` · 手术记录 `mapping/_v3_20260901_中微三节点合并_手术记录.json` · 备份 bak_surgery_zhongwei_20260901_034342 · props 并集断言逮 _region_src 冲突（治理元键·保主节点 code）· 复检全绿（5191/5823·悬挂0/自环0/非法type0/旧id零残留）。状态：🔄 已修待验（实施者不自标 ✅）。

## [ERR-20260608-001] 价格层并发写竞态：price_extract 与 kg_ingest 钩子不可同时跑
**状态**: ✅ 已知约束 **优先级**: 🔴 高
**触发**: 两者都向 `prices/commodity_prices.jsonl` append；并发时各自读 pre-state 再写 → 撞键/丢点（本次 kg_ingest 价格钩子与源码编辑赶在一起，致 53 条混入 + 部分预测点被吞）
**解决**: 顺序跑、不并发；价格层唯一写入口 `price_query.append_prices()`（去重+重建快照）
**预防**: 回填期间不跑新文档 kg_ingest；分工 kg_ingest 管新文档、price_extract 只做一次性回填

## [ERR-20260608-002] 价格去重键漏 horizon → 现价/预测同日撞键误并
**状态**: ✅ 已解决 **优先级**: 🔴 高
**触发**: 去重键 (commodity,grade,price_type,as_of,source_file) 不含 horizon → 同篇同商品同类型同日的"现价/历史对比"与"预测"被判重复，后者被丢（典型：MLCC基粉 涨跌幅 历史+10% vs 预测+10%）
**解决**: 去重键 / 快照键(rebuild_latest) / _price_id 全部加入 horizon；price_query + price_extract 同步修；已污染数据清层重建（重置种子 21 条→Doctor 重跑回填）
**预防**: 价格 schema 凡区分时态（现价/预测/历史对比）的维度都须进去重键

## [ERR-20260608-003] kg_merge 去重并入已有节点时不 union provenance → 已处理研报"零来源"
**状态**: ✅ 根治闭环（2026-06-25）——第①步 _merge_data_sources 复合键 (file,reference)；第②步 forward cite 指纹走 Route A（kg_ingest 加 cite_nodes 槽 + _cite_nodes_to_updates 纯函数 + 零足迹告警，单测 3/3、第①步回归 4/4），原拟「另立高风险 PRD」由更轻的 Route A 取代。残留仅历史 207 孤儿回填，降级为数据卫生 followup（forward-only 观察期）**优先级**: 🟡 中
**进展（2026-06-24 复盘 P1）**: 第①步落地——`kg_merge._merge_data_sources` 去重键 `reference` → `(file, reference)` 复合键，根治「同 reference 不同 file 被吞」；加 `tests/test_kg_merge_provenance.py` 4 测全过（含旧逻辑复现 ERR-003 对照）。**残留第②步**：某报告仅「提到」已存在实体、未改属性时 kg_ingest 不把它写进 patch → merge 层无源可 union，需改 kg_ingest patch 生成 + provenance 覆盖率门槛告警，触及入库主链、风险高，**另立 PRD**。下方为原始诊断。
**触发**: 建生料关系图时发现 37 篇已 `kg_processed=true` 的研报在 canonical 里无任何节点/边 `data_sources.file` 记到 → 抽样核对其实体（碳化硅/华工/800G/电子布等）都已在图谱、但来源记的是别篇
**真因**: kg_merge 合并时实体若已存在→并进已有节点，却**不把本篇 file union 进 data_sources**；报告"处理过"却查不到当过来源
**影响**: 按 file 反查溯源的下游全漏记（生料图谱/信源覆盖/研报审计）；低估热门实体来源广度；误判已入库为未入库
**绕过**: 生料图侧加"内容回链"（扫正文匹配枢纽名补连，弱连接），覆盖 114→154/169，非根治
**根治**: kg_merge 去重并入时 union data_sources（按 file+reference 去重，注意置信度/vintage 合并、防膨胀）；加单测+provenance 覆盖率门槛
**详**: Database/行业研究/渊图_GOTCHAS.md [ERR-20260608-003]

## [ERR-20260609-001] 龙鱼六维:技术供需维把赛道β/嘴炮指引当公司兑现致虚高
**状态**: ✅校准 **优先级**: 🔴高
**触发**: 德科立72虚高(Doctor质疑嘴炮型)→校准62/谨慎
**根因**: 技术供需维用"赛道需求大"代替"公司自身订单/份额已兑现",把未落地期权当现实
**解决**: 三维(技术供需/竞争/新赛道)打"兑现折扣",分β(行业)vs α(公司),只为已兑现给高分;先过降级核查法(EXP-20260609-003-P)
**预防**: regime零容忍业绩下,ROE极低+靠guidance的设上限;同分段横向校验
**详**: Database/行业研究/渊图_GOTCHAS.md

## [ERR-20260611-merge] kg_merge 漏 --output 致 canonical 未更新 → kg_merge_safe.py 固化
**状态**: ✅修正（2026-06-11 卡点修复批次）**优先级**: 🔴高
**触发**: Doctor 跑 kg_merge 漏 `--output`，4 次默认输出时间戳文件、canonical 未动；commit 信息(2279/2777)与实际提交图谱(2227/2718)错位
**解决**: 新建 `Database/行业研究/kg_merge_safe.py`——输出强制指向 canonical（无漏写可能）+ merge 前自动备份 backups/ + patch 格式闸（缺 add_nodes 等四键拒绝合并，防错文件静默合 0 条）+ merge 后重读盘校验节点/边只增不减 + 打印与实际图谱强一致的 commit 命令。**今后合并一律用 safe 包装，不再裸跑 kg_merge.py**
**详**: kg_merge_safe.py 头注释；自测三关（合并/拒错/真库 dry-run）通过

## [ERR-20260614-001] TPU 在 evolves_from 裂成两分量 + 重复节点，待 dedup
**状态**: ✅ 已结案（2026-06-24）**优先级**: 🟢 低
**复盘核验+收口（2026-06-24）**: ① **重复节点已清**——codename_map 列的 6 个旧重复/张冠李戴节点（GoogleTPUv10Humufish / TPUV8AX / TPUV8X / GoogleTPUv8Zebrafish / GoogleTPUv7Ironwood / GoogleTPUv7eSunfish）逐一核对均已不在 canonical，06-19 dedup 已落地。② **「大小写两套」非重复而是两层粒度**：`TPUV6/V8/V9`=世代锚、`GoogleTPUv7/v8i/v8t/v10`=型号变体，图中 `v8t/v8i --part_of--> TPUV8` 结构本就对，不机械合并（ERR-001 自身铁律：张冠李戴禁自动选 survivor）。③ **谱系已理顺单脉**：删 3 条冗余/隔代 `evolves_from`（TPUV9→{GoogleTPUv7, v8t, v8i}）+ v10 改承 v9，世代脊成单线 `V6←v7←V8←V9←v10`，v8t/v8i 降生自 v7 + part_of V8；边 3263→3260，备份 `bak_pre_tpulineage.20260624_143139`。④ **伞节点框架决策（Doctor 2026-06-24 定）**：`TPUV8` **保留为 v8 世代锚**（维持 v8t/v8i part_of），不并入 v8i。下方为原始诊断。
**触发**: 建技术先进度 family 时发现 谷歌TPU 在 evolves_from 子图里裂成两个连通分量——小写 `product_GoogleTPUv7/v8i/v8t/v9_Pumafish…` 与大写 `product_TPUV6/V7/V8/V9`；且 `product_TPUv8t` 与 `product_GoogleTPUv8t` 名称同为「谷歌TPU v8t（训练版）」疑似重复节点
**影响**: 同一代际被拆成两套 id；按 family 聚合/溯源会低估关联；先进度对齐时需手工合并为一条 family（已在 tech_eras.json `family_google_tpu` 合并处理，不受影响）
**根治待办**: 跑 dedup 把大小写两套 TPU 节点按代际对齐合并、删重复 v8t（注意 union data_sources，见 ERR-20260608-003）
**详**: Database/行业研究/mapping/tech_eras.json review_notes

## [ERR-20260609-001b] α折扣串维重复扣分→维度正交修正
**状态**: ✅修正 **优先级**: 🔴高
**触发**: ERR-001把"利润未兑现"同时扣技术+竞争+财务三维(扣三次);Doctor纠:财务问题只扣财务,技术好不扣技术,订单好不扣竞争,扩产对齐供需是好事
**解决**: 维度正交归因——负面信息先归一个维只在该维扣;扩产/重资产爬坡默认中性偏正;但竞争维真问题(源杰单客户/联讯链内循环)仍保留
**详**: Database/行业研究/渊图_GOTCHAS.md

## [FIX-20260615-001] 三环集团 id 拼音误植 Sanhua→Sanhuan（系统性近名坑）
**状态**: ✅ 已修复 **优先级**: 🟡 中
**触发**: 跑龙鱼五力时发现三环集团节点 id 为 `company_SanhuaGroup`——"Sanhua" 是三花（智控,002050,制冷/汽车热管理/机器人执行器）的拼音，三环应为 Sanhuan。属 ERR-20260602-001 同类近名坑。
**核查**: name「三环集团」正确、内容(MLCC/离型膜/洁美/南充德阳)确系三环、图谱内**无三花智控节点**故零碰撞——错的仅 id 串与 alias「Sanhua Group」。误植系统性：连带 4 个 concept/metric 节点 id 同误。
**方案B(彻底·Doctor 批)**: 5 个 id 全 Sanhua→Sanhuan + 9 边/12 端点同步 + alias 修正并补真别名(潮州三环/CCTC/300408) + 加 properties.stock_code 与 disambiguation 防混 + wiki 卡 sanhuagroup.md→sanhuangroup.md。
**安全纪律**: 备份 backups/…preSanhuanRename + 断言节点2367/边2860守恒+无残留+无悬挂+body仅公司节点改。沙箱删不了旧 wiki，交 Doctor `git rm`。
**预防**: 入库后跑 rules/name_code_consistency_check.py；易混公司(三环Sanhuan/三花Sanhua)登记防误。

## [FIX-20260616-001] 盛科重复节点 company_Centec / company_CenturyCore（ERR-20260602-001 同类）
**状态**: ✅ 已落盘核验（2026-06-25 核 canonical：company_CenturyCore 已不在、company_Centec 保留并挂全 10 节点边系，去重生效）**优先级**: 🟡 中
**触发**: 入交换芯片结构增量时发现盛科通信有两个节点——`company_Centec`（挂集采/SwitchTray 边）与 `company_CenturyCore`（挂 supplies Switch256T/512T、competes 博通/中兴微、enables from DualVendorPolicy 边），同实体重复。
**核查**: 两节点 aliases 都含「盛科」；CenturyCore 的 competes_with 博通边与 Centec 既有 `rel_Centec_BroadcomCompete` 重叠。零代码碰撞（非近名拼音错，是纯重复实体）。
**方案(Doctor 批 · 保 Centec)**: `mapping/dedup_centec_20260616.py`——重指 5 边(CenturyCore→Centec)、与既有同向同型边去重合并 data_sources、合并 props/aliases/data_sources(补真别名盛科通信/Centec Communications/688702)、删 CenturyCore 节点。备份 backups/…dedupCentec + 守恒断言(节点 -1 / 无残留 CenturyCore / 无悬挂 / 无重复边 / 无关节点逐字节守恒)。
**预防**: 公司入库前先 kb 查重（同实体异 id）；入库后跑 name_code_consistency_check。

## [派工·非坑] ⚡ 更新健康埋点（派工v1 · 2026-06-24）
**状态**: ✅ 已做（2026-06-24）**优先级**: 🟡 中
**落地**: 写 `scripts/write_health.py`（可复用 stamp，跑结构校验→写 `mapping/_health.json`：updated_at=canonical mtime、update_ok=全绿则 true）+ 已生成首版 `_health.json`（全绿 2713/3260）；`asset_manifest.json` 渊图KG 节点补 `health_file`。看板「渊图KG」卡即点亮「更新时刻 +（无错误/报错）」。固化建议：把 write_health() 接进 kg_merge_safe 落盘成功分支，未来每跑自动刷新（未做，留待动既有码时一并）。
**详**: `Claude/Projects/海螺姑娘/dashboard/UPDATE_HEALTH_派工_v1.md`（任务卡 ⑤）；原待办见 git 历史。

## [BACKLOG-20260624-001] 非规范前缀节点 + 剂泰科技/METiS 生物子图串入（2026-06-24 复盘：实况比记录严重，脚本就绪待 apply）
**状态**: ✅ 已 apply 落盘（2026-06-25，commit 9e9a259）——节点 2713→2699、边 3260→3246，MITMediaLab 保留+剥离、equipment_ 纳入允许集、milestone_×3→event_/market_×1→concept_ **优先级**: 🟡 中（原记 🟢，复盘上调）
**复盘订正实况（2026-06-24）**: 记录原写「6 前缀 + 2 疑串入」，实测**非规范前缀 18 个**、**生物串入为整篇`剂泰科技：全球独家AI纳米递送平台`报告的 15 节点子图**（远超记录）。
- **前缀 18 拆分**：`equipment_`×12（制造设备类·type=equipment·成体系）→ Doctor 裁定**纳入允许集**（已改 `kg_ingest.py` known_prefixes/KNOWN_PREFIXES 加 equipment，不动图）；`milestone_`×3（OCS认证/量产订单/盈利兑现）→ `event_`；`market_`×1（OpticalChipTestEquipment）→ `concept_`；`technology_`×2（LipidBert/高通量LNP）属下方 bio 子图，随删。
- **bio 串入子图 15 节点**（剂泰/睿正/科拓/菁童/MITMediaLab + 陈红敏/赖才达 + MTS004/108 + LipidBert/高通量LNP + 非肝靶向/心肌靶向/双轮模式/LNP专利）：全溯源同一篇剂泰科技研报，属生物医药/mRNA递送，非渊图 AI 硬件域。
**裁定（Doctor 2026-06-24）**: ① equipment_ 纳入允许集；② 边界点 `company_MITMediaLab` **保留+剥离**剂泰 data_source/bio 边（保住手工补的「电液纤维肌肉」合法关联），其余 14 节点删；③ `TFLNPhotonicChip`(薄膜铌酸锂光子芯片) 是正当光子内容**勿误删**（仅 substring 撞 LNP）。
**落地**: `mapping/cleanup_yuantu_bio_prefix_20260624.py`（归档子图→archived/ + 备份 + 守恒断言 + 删14+改4前缀）dry-run 全过：节点 2713→2699、边 3260→3246、MITMediaLab 仍连电液纤维肌肉、前缀改名同步 16 边端点。**待 Doctor 终端 `--apply` + git**。
**预防**: kg_ingest 已校 type↔id 前缀∈允许集（本次把 equipment 纳入唯一真相集）；建公司/技术节点前先 kb 查重 + 核 data_source 主题域，防跨项目（生物/AI硬件）串入。属 ERR-20260602-001 族系的「跨域串入」变体。

## [FIX-20260626-001] 盛合 CoWoS-L 口径矛盾：节点 prop 与 supplies 边冲突（粒度+时效错配，非真矛盾）
**状态**: ✅ 已 apply（2026-08-20 读盘复核：canonical `concept_DomesticCoWoSLPackagingLandscape` `_meta.校对_盛合CoWoSL粒度时效_2026_06_26` 留痕在盘——原「待 Doctor 终端 apply」尾巴为过时状态）**优先级**: 🟡 中
**触发**: Doctor 追问「盛合也部分上混合键合了么」→ CC 核图谱发现 `concept_DomesticCoWoSLPackagingLandscape` prop「盛合承接 CoWoS-S，不涉及 950/960 CoWoS-L」与 `rel_Shenghejingwei_supplies_HiSilicon`（含 950PR）/ `rel_Shenghejingwei_Supplies_Ascend950PR`（封测）冲突。
**核查**: 非真矛盾。旧口径 P1 = 帕米尔 2025-05-31（一年前·prop 标 undated）；新口径 P1 = 帕米尔 2026-04-27 / 2026-06-22。**950PR = 入门级小尺寸 CoWoS ≠ 950/960 旗舰大尺寸 CoWoS-L**——盛合承接 950PR 入门级，旗舰大尺寸归华为自有产线（Tier1 领先约 3 个月）。混合键合方面：盛合唯一连接是麒麟2026 一单（P2 华泰，2026 秋季未上市），确凿量产仍是 2.5D micro-bump 20μm。
**解决**: 精修 prop 为分粒度口径 + 加 `_meta.校对_盛合CoWoSL粒度时效_2026_06_26`，保留全部边。patch `mapping/_v3_20260626_盛合校对_manual.json`，纯 update 计数 2702/3254 不变。
**预防**: prop 带时态/粒度（入门级 vs 旗舰）须显式 as_of；近名/口径冲突先比 data_vintage 再判、新覆旧；同实体多批次入库做交叉口径核对。属 ERR-20260602-001 族系。

## [NOTE-20260626-001] kg_ingest 后续薄 patch 把既有公司节点「瘦身」：desc 精简 + props 清空成 {}
**状态**: ✅ 已根治（2026-06-26 深合并实装+单测 4/4 · 2026-08-08 复盘补标）
**类型**: 📝 数据卫生（回归）→ ✅ 已根治（2026-06-26 深合并实装）**优先级**: 🟡 中
**根治（2026-06-26）**: `kg_merge._deep_merge_dict_fields` 对 `properties`/`_meta` 改子键并集深合并（patch 子键胜出、base 独有保留），took_patch 分支节点+边均接入。薄/空 props patch 不再冲掉富 props。单测 `tests/test_kg_merge_deepmerge.py` 4/4（含空 props、子键覆盖、_meta 并集、富 props 不丢）；provenance 既有单测 4/4 回归通过。代价：无法再经 patch 删子键（本库 props 累加事实，可接受；删走专门脚本）。下方为原始诊断，留档。
**现象**: `company_Shenghejingwei` 在 2026-06-22「950 产能」批次后 updated_at=2026-06-24，desc 仅剩 3 句、`properties={}`；而 wiki 卡（2026-06-23 快照）仍存 46 条 props——**卡比节点全**。
**真因**: kg_merge `_merge_node` 在 patch 胜出时 `merged=deepcopy(patch_node)` 后只保留 base 中 patch **未提供**的顶层 key；若本批 LLM 产出薄 patch **带了** `properties`（哪怕是 {} 或少量），整块替换掉旧富 props（top-level 替换、非深合并）。
**绕过/解决**: 从 wiki 06-23 快照回填 desc + 46 props（本次已做，保留 06-24 新增的「2025 管理问题」事实）。
**预防**: ① 入库后抽查热门节点 props 是否被薄 patch 冲淡；② 富节点 props 以 wiki 卡为快照备份源；③ 治本选项：kg_merge `properties`/`_meta` 改深合并（patch 缺的子 key 保留 base）——触及入库主链，另议立项。

## [NAMING-20260628-001] 命名规范铁律：禁裸拼音简称 id + 三路审计对账法（ERR-20260602-001 族系总治理）
**状态**: ✅ 已立律 + 配检测脚本 + 12 组真重复合并落地（2026-06-28，canonical 2767/3337）**优先级**: 🔴 高
**触发**: Doctor「不允许再出现 company_xiandao/company_tongmei 这种简写节点名」。裸拼音简称 id 光看无法唯一定位实体（先导有微电子/集团/基电/智能多家；通美有 AXT/北京通美/金瑞佳业），是张冠李戴温床。
**核查法（Doctor 定）**: 开 **3 个独立 subagent 同任务核查、互不喂结论**，CC 对照三方结论差异 → 对分歧点做二次重点核查（联网+desc）。本次成效：三路共识 9 组真重复 + 二次核查坐实 3 组（天弘=Celestica/长光华芯幽灵节点/铟杰=英杰），并**驳回 1 个误并**（利森诺克 Lisenoke ≠ 力森诺科 Lisennock=Resonac——靠 Showa「为利森诺克供铜箔」的矛盾识破，单路会误并）。
**落地**: ① 合并 12 组（海光/海思/Meta/台光三合一/中兴微/鼎泰高科/通美/新凯来/鑫耀=新耀/天弘=Celestica/长光华芯/铟杰=英杰）；② 改名纠错（升腾删 Enflame 别名归华为昇腾·910C 实为昇腾；GUC 正名创意电子·清「世界先进/世芯」错挂）；③ 立**命名规范铁律**写进 `Database/行业研究/CLAUDE.md`（禁裸简称 id/上市带 code/大小写唯一/外企用全称）；④ 配检测脚本 `rules/bare_alias_check.py`（[1] 大小写重复必修·[2] 裸简称清单·[3] 近名兄弟簇），接 batch 后跑。治理后 [1]=0、33 组近名兄弟人工扫均为合理母子/不同实体。
**遗留**: 利森诺克真身（独立 CCL 厂·联网未坐实）；宝德 PowerLeader 液冷描述疑张冠李戴（待回研报）；222 单义裸简称登记黑名单渐进改；先锐科技英文待核。
**预防**: 新建 company 节点遵铁律；batch 后强制跑 bare_alias_check.py；易混/族系实体（先导/通美/住友/三菱/鼎泰/海光/海思/台光/中兴微/生益…）建节点前 kb 查重 + 联网坐实英文名↔实体。属 ERR-20260602-001 / FIX-20260619-001 族系总治理条。

## [ERR-20260718-001] LLM 把正文首行「XX-学习材料（MMDD）」当文件名写进 data_sources.file → provenance 静默失配
**状态**: ✅ **已根治闭环（2026-07-18 当日）** **优先级**: 🔴 高
**根治落地**: `kg_ingest._enforce_source_filename(patch, filename)` —— patch 解析后、cite/价格钩子/merge **之前**，强制把所有 `data_sources.file` 覆写为真实文件名，**不采信 LLM 输出**。LLM 编造的原值留痕在 `ds['_file_llm_said']`，改写数 >0 即打 WARNING，作为长期监控指标（本次 15 篇里 3 篇跑偏，非偶发）。
**为何选后处理而非改 prompt**：prompt 是请求、后处理是保证；且同文件的 cite 路径（`_cite_ds`）一直是代码直写 filename，从未产生幽灵，可作对照佐证。
**安全性论证**：一个 patch 只对应一篇文档，filename 唯一，不存在「合法引用其他文档」情形（LLM 只看得到这一篇）；跨文档 data_sources union 发生在 kg_merge 阶段，不受影响。
**测试**: `tests/test_enforce_source_filename.py` 18/18（含分裂型真假混杂、标题型/日期型两种篡改、6 类边界）；既有 provenance 4/4 + deepmerge 4/4 回归通过。
**历史数据清理**: 本批归正 86 处 + 绿的谐波 49 处 + 历史幽灵 A/B/D1 共 2116 处；幽灵总量 371 种/4487 处 → **287 种/2371 处**。剩余多为已归档 PDF、`web:` 网页源、以及归一化后有多候选的歧义项（机器分不出，**宁可不修**）。
<!-- 以下为原始诊断，留档 -->
**原状态**: 🟧 本批已归正（86处），根治待立项
**触发**: 2026-07-18 帕米尔15篇 batch，六氟丁二烯篇报「provenance 零足迹」。查证发现节点确已抽出（6节点/6边），但 `data_sources.file` 写的是 LLM 自造的名字，按 file 反查匹配不上。
**真因**: `kg_ingest` 让 LLM 自行产出 `data_sources.file` 字段，而 LLM **不知道真实文件名**，于是拿文档正文首行的「XX-学习材料（MMDD）」或**处理当天日期**去编。本批 3 篇中招 86 处：
- 六氟丁二烯 14 处**全错**（用了处理当天 `2026.07.18`，真实文件 `07.12`）
- 磷化铟 41 处幽灵 / 16 处真名 —— **分裂**
- 超节点交换机 31 处幽灵 / 26 处真名 —— **分裂**
**★ 告警盲区**: `provenance 零足迹` 告警只在**该篇一处都没记对**时触发。磷化铟/交换机因为有部分节点记对了，**告警不响、静默漏过** —— 这是比坑本身更危险的部分。
**波及历史**: 上一批（2026-07-13）绿的谐波篇同样中招，幽灵 `2026.07.12-帕米尔研究：减速器学习材料：绿的谐波人形订单超30万台.md` 49 处**已进 canonical**。全图另有 373 个对不上磁盘的 file 名，但多数应属文件移动/归档/Notion hash 清理，**不可一概算篡改**，需专项审计逐个配对。
**影响**: 不伤图谱结构正确性（节点/边/type 全对），只污染按 file 反查的溯源链——正是 ERR-20260608-003 当初要根治的伤害，从另一个口子漏回来。
**本批处置**: `mapping/fix_batch15_20260718.py` [7] 按显式映射归正 86 处，加 `_file_corrected_by` 审计字段。
**根治方向（待立项）**: `data_sources.file` **改由代码强制写入传入的真实文件名，不让 LLM 产出该字段**——LLM 本来就无从知道文件名，没有任何理由让它自由发挥。触及入库主链，单独立项。
**关键澄清（Doctor 2026-07-18）**: 正文（MMDD）**不是 LLM 编造**，是文档标注的**会议日期**；文件名日期是**纪要发布/获取日期**（Doctor 无法参加所有会议，会议与纪要之间有 1-7 天延迟）。语义上会议日期更准 → 另立「会议日期改名批」对齐 32 篇。**但改名修不了本坑**：LLM 连标题一起重写成「XX-学习材料」，日期对上标题仍对不上，两件事必须解耦。
**预防**: ① batch 后除看零足迹告警外，**必须主动扫「幽灵 file」**（`data_sources.file` ∉ 磁盘真实文件 ∪ index）——告警抓不到分裂型；② 逐篇核对「本篇真实文件名被记为来源的次数」，为 0 或异常偏低即中招。

## [NOTE-20260718-003] raw/ 混着「老石谈芯」视频转录，与帕米尔纪要**日期常撞车**——按日期配对文件必错配
**状态**: ✅ 已沉淀（配对规则已立 2026-07-18 · 2026-08-08 复盘补标）
**类型**: 📝 数据事实（配对陷阱）**优先级**: 🔴 高
**触发**: 2026-07-18 修历史幽灵 file 时，想用「幽灵名的日期段 + 该日磁盘文件唯一」来自动配对。实测直接错配：
- `2025.05.31-帕米尔研究：先进封装：学习材料.md` → 配到 `2025.05.31-老石谈芯-宝马竟然想靠这个技术弯道超车…`
- `2026.06.15-帕米尔研究：玻璃基板学习材料.md` → 配到 `2026.06.15-老石谈芯-中国市场，对于遥遥领先的英伟达…`
- `2026.06.08-帕米尔研究：碳化硅衬底-学习材料.md` → 同日只有老石谈芯转录
**真因**: `raw/视角/老石谈芯/` 下有大量视频转录，文件名同样是 `YYYY.MM.DD-` 前缀，**与帕米尔纪要共用日期命名空间**且数量可观，「该日唯一文件」这个条件经常由老石谈芯的篇目满足。
**正确做法**: 配对**必须日期 + 主题双重校验**——从两侧文件名剥掉停用词（帕米尔研究/学习材料/调研/纪要…）后算字符重合率，要求 ≥60% **且显著领先次优**（≥+0.25）才采信。实测该规则把 8-9 种错配全部拦下，只放行 10 种主题 100% 重合的。
**附带坑**: 主题词切分若用 `len>=2` 过滤，会把**单字主题**（「钨」「膜」）滤成空集、误判为零重合——`2026.06.15-帕米尔研究：钨-学习材料.md` 一度被判无匹配，实际对应 `钨价企稳反弹`。改用字符级重合后正确。
**预防**: 凡在 `raw/` 下做「按文件名/日期自动配对」的操作，先确认候选集里有没有老石谈芯（及其他视角类转录）。属 FIX-20260619-001「张冠李戴禁自动配对，必逐边核」在**文件层**的同构表现。

## [NOTE-20260718-004] 重指边去重必须只作用于被重指的边，否则误伤显式声明的重复边组（原号 NOTE-20260718-002 · 2026-08-08 复盘重号拆分改此号）
**状态**: ✅ 已沉淀（规则已立 2026-07-18 · 2026-08-08 复盘补标）
**类型**: 📝 流程教训（CC 自查）**优先级**: 🟡 中
**触发**: 写 `fix_batch15_20260718.py` 时，TPU 合并段的去重循环遍历了**全部**边（用一个 `seen_keys` 累积），结果把 [3] 段本该显式处理、且要**把 description 并入 properties** 的两组重复边提前**裸删**，信息丢失。dry-run 计数 `tpu_edge_deduped: 4`（预期 2）暴露了它。
**解决**: 拆成两步——重指阶段**只重指不去重**；去重统一推迟到 [3b]，且 survivor 优先取「未被本脚本重指」的既有边，被撞边的 `description` 存进 `keep.properties`、`data_sources` 并集合并。
**预防**: ① 凡「合并节点后重指边」的脚本，去重范围**必须限定在 touched 集合内**；② dry-run 的计数与预期不符**即视为 bug**，别放过（本次正是靠 4≠2 逮到）；③ 去重一律「保留最丰富 + 信息并入 + data_sources 并集」，不裸删（沿 2026-05-23 完整性清理立的规矩）。

## [NOTE-20260712-001] kg_merge_safe.py 不吃 `--base`（与 kg_ingest.py 参数面正相反）——贴错旗标 argparse 直接报错、merge 空转
**状态**: ✅ 已澄清 **优先级**: 🟢 低
**触发场景**: 2026-07-12 特斯拉 patch promote，CC 给 Doctor 构造终端命令时写成 `python3 kg_merge_safe.py <patch> --base mapping/行业知识图谱_完整数据库.json`。两条 merge 命令（dry-run + 正式）argparse 均报 `error: unrecognized arguments: --base …`、**未执行**（无害：canonical 早已在本会话 promote 到 3125/3683，读盘核验 + git tree clean 佐证）。
**根因**: 两脚本参数面**相反**、极易交叉记混——`kg_merge_safe.py` 签名仅 `[-h] [--dry-run] patch`，base=canonical **已内建强制指向**（见 ERR-20260611-merge：safe 包装就是为「输出强制指向 canonical 无漏写」而生），**不接 --base**；而 `kg_ingest.py --batch` 反而**必须**带 `--base mapping/行业知识图谱_完整数据库.json`（见 ERR-20260709-001：find_latest_kg 不扫 mapping/）。
**预防**: 构造命令前认准脚本——**promote/merge** 走 `kg_merge_safe.py <patch> [--dry-run]`（无 --base）；**ingest 批处理**才带 --base。贴 Doctor 终端前对一眼 usage，避免整轮终端往返空转。

## [NOTE-20260718-002] 研报数字必回原报告看信源标注——转述链最先丢的是时间限定词
**状态**: ✅ 已沉淀（信源定级规则已立 2026-07-18 · 2026-08-08 复盘补标 · 原重号拆分：本条保留原号，「重指边去重」改 NOTE-20260718-004）
**类型**: 📝 数据卫生（信源定级）**优先级**: 🟡 中
**触发**: 2026-07-18 核实比亚迪电子光模块，「800G 月产能 5 万只」这一广泛流传的数字，追到底是开源证券 2025-09 研报原文「2025 **年内**产能 5 万**片**/月」经东财财富号「股问观值」转述后的变形。所有二次传播均可回溯至同一句话。
**三处损耗**（按危害排序）：
① **时间限定词丢失**——「年内」消失后，**年度目标伪装成既成现状**。最隐蔽、危害最大。
② 量词漂移——「片」→「只」。
③ 单源伪装共识——一句话经自媒体扩散后被引为「市场普遍认为」。
**规则**:
- 引用研报数字前，**必须回到原报告看它自己的信源标注**（据公司交流 / 据公司公告 / 券商测算），据此定级：管理层口径→P1；券商自行测算→P3。拿不到原文的，一律标「**P2·单源转述·信源类型未知**」，不得升级。
- 转述文本里凡出现「年内」「有望」「预计」「目标」等限定词，**入库时必须原样保留**，不得压缩成陈述句。CC 本轮初稿即因删「年内」二字把目标写成现状。
- 同一数字若所有二次传播都能回溯到同一篇，即为**单源**，**不因传播广度升级**。
**配套**: 与「高时效数据不入 canonical」铁律配套——高时效数字即便只入 props 注记，**限定词与信源类型也须一并写入**。
**同批次副产**: 同一核实还撞出**分部口径矛盾**——2025H1 分部「新型智能产品」72.09 亿（其中数据中心相关 10 亿）vs FY2025 年报分部「AI 算力基础设施」9.43 亿，H1 已 10 亿而全年 9.43 亿，必非同口径。教训：**跨期引用分部数据前先确认分部划分未变**，公司常在年报重划分部。属 FIX-20260626-001（粒度/时效错配）族系。
**详**: `Database/行业研究/raw/核实/2026-07-18-比亚迪杀入光模块传闻核实札记.md`

## [ERR-20260718-002] 并发会话覆盖：CC 改 brain 文件后被另一会话的 git 提交无痕回退
**状态**: ✅ 已复现并定位 **优先级**: 🔴 高
**触发**: 2026-07-18 本会话用 Edit 工具改 `渊图/GOTCHAS.md`（加 NOTE）+ `渊图/architecture/决策记录.md`（加决策条）+ 两处 frontmatter `updated`，工具均报成功。Doctor 终端 `git add/commit` 却报 **`nothing to commit, working tree clean`**。
**核查**: 沙箱 grep 确认两处改动**盘上根本不存在**（NOTE 计数 0、决策条计数 0、frontmatter 仍为旧值 2026-07-09 / 2026-05-14）。git 报 clean 是**正确的**，错的是 CC。
**真因**: 同日另有会话在动渊图（提交 `d5aa9d6 session: 渊图帕米尔15篇入库与provenance根治 2026-07-18`），该提交**包含 `渊图/GOTCHAS.md`**，把本会话的编辑覆盖/回退。会话中途 CC 曾收到「文件被外部修改」提示（frontmatter 从 2026-07-18 变回 2026-07-09），**当时未察觉那就是回退信号**。
**连带**: 同一并发会话把 canonical 从 **3207/3746 promote 到 3384/3903**，导致本会话三份文档记录的 `canonical_at_time: 3207/3746` 与 patch 的 `_base` 断言集体过期。
**规则**:
- **落盘类动作宣称完成前必 grep/stat 复核**（NOTE-20260709-001 元教训的再次实证，本轮 CC 连犯两次：说「已落」两次均未核）。
- 收到「文件被外部修改」提示时，**必须立即 diff 确认自己的改动是否还在**，不可默认「外部改动与我无关」。
- 动 brain tracked 文件前先 `git log --oneline -3 -- <file>` 看当日是否有并发会话触碰；写完到 Doctor commit 之间若跨越较长时间，commit 前重新核验。
- 引用 canonical 计数前**当场读盘**，不沿用会话早期读到的值——并发 promote 会让它在会话中途改变。
**预防**: 长会话中 brain 文件的「改 → 报告 → Doctor 提交」链条越长，被并发覆盖的窗口越大；高价值改动应**改完立刻请 Doctor 提交**，不要攒到会话末尾。

**追加（同日 · CC 二次踩坑 · 铁律边界订正）**: 铁律「不在沙箱跑 git 写命令」的边界被 CC 划错——以为只禁写命令，于是跑了 `git status --short` 做落盘核验。**`git status` 会刷新索引并创建 `.git/index.lock`，而沙箱无权删除**（输出末尾已有 `warning: unable to unlink '.git/index.lock': Operation not permitted`，CC 当时未理会），残留 0 字节孤儿锁，导致 Doctor 终端 commit 报 `Another git process seems to be running`。
- **订正后的铁律：沙箱内不跑任何 git 子命令，包括 `status`/`diff`/`log` 等看似只读的**。
- 需核验落盘一律用 `grep` / `stat` / `ls`；需看仓库状态则构造命令交 Doctor 终端。
- 残留锁处理：确认无真 git 进程后 `rm -f .git/index.lock`（本次锁为 0 字节、ps 无 git 进程，安全删除）。

**追加二（同日 · 交付格式教训）**: CC 把「拟写入文件的 Markdown 正文」放进代码块给 Doctor 过目，Doctor 误当命令粘进终端，触发一串 `command not found`（无副作用）。**规则：代码块只放可执行命令；给 Doctor 审阅的文档正文用引用块或普通段落呈现，并显式标注「这是文件内容，不是命令」。** 更根本的是——**文件内容应由 CC 自己写入，不该让 Doctor 手工搬运**。

## [ERR-20260814-001] xlsx recalc.py 沙箱超时 → soffice convert 等效重算绕过
**状态**: ✅ 已解决 **优先级**: 🟡 中
**触发**: xlsx skill 生成带公式工作簿（CPO 评分表 v2，52 公式）后，沙箱跑 recalc.py 验证公式缓存——profile 创建环节反复超时（29s/119s/100s/180s 四次全断），pkill soffice 无效，重建 xlsx 后复现。LibreOffice 首次启动 profile 初始化在沙箱里卡死。
**解决方案**: 绕过 recalc.py——`soffice --headless --convert-to 'xlsx:Calc MS Excel 2007 XML' 目标.xlsx`（LibreOffice 加载时自动重算公式并写缓存，等效重算）；python openpyxl data_only 读缓存与手算对照，全对后 cp 覆盖原文件；再 openpyxl 双视图扫描确认 52 公式保留、0 错误值。
**预防措施**: ①沙箱验证带公式 xlsx 优先走 soffice convert 路径，recalc.py 只作备选；②convert 写回会**去掉无空格 sheet 名的引号**（='附注'!$B$2 → =附注!$B$2），跨表公式完整性检测勿用精确前缀匹配（会误报「跨表公式=0」），直接抽查公式单元格内容即可。

## [NOTE-20260816-001] kg_promote 丢失检查不豁免改名——改名批绕一键门直改 canonical
**状态**: 🟢 已知边界 **优先级**: 🟡 中
**触发**: Boss老白批 QA 把 7 个非规范前缀节点（device_×4 / eqpt_×3）改名 equipment_ 后走 kg_promote——被「丢失旧内容=7」拦下：旧 id 只入 aliases 不出现在节点 id 集合，kg_promote 的 `lost = canonical_ids - batch_ids` 检查无 aliases 豁免。
**真相/裁定**: kg_promote 的丢失检查设计目标=防合并丢内容，改名不在其语义内。改名批（id 变更 + 边端点同步 + aliases 留旧）的正确路径 = 单进程直改 canonical + 先 cp 备份 + 同进程复检（悬挂/自环/非法 type/节点 id 重复）+ 写回复校 + wiki regen，不走一键门。
**预防/可选根治**: 若日后改名批频繁，可给 kg_promote 加 `--allow-renames` 参数（lost 检查时对出现在任意节点 aliases 里的旧 id 豁免）；当前按直改路径走，不改门。

## [NOTE-20260816-002] 转录语料断言准确率仅 61%——四类高发错误谱系（普查实证）
**状态**: ✅ 已固化闭环（2026-08-20 复盘回写 · 117 处订正落图 + CLAUDE.md「转录语料断言核查」节固化在盘 · 原状态词「已固化流程」不在 conch 计数闭集被误计为积压）**优先级**: 🟡 中
**触发**: Boss老白 131 篇视频转录（972 新节点）全量普查：459 条断言 ✓280（61%）✗65 △114。结构校验（悬挂/自环/type/重复）全部查不出这些——语义层污染。
**四类错误谱系**（按频率）:
1. **谐音名转写**（ASR 专有名词系统性弱项）：沛顿/睿力/王宁国/芯源微/盛美/是德/橙科微/哈默纳科/博睿康/北脑一号/鸿擎/星科/富临/舛冈富士雄——30+ 条，占 ✗ 近半
2. **机构张冠李戴**：HBF 联盟「美光」实为闪迪；ATI→ADI；豫资→豫信电科；SpaceX 卫星→Starcloud；ETS→BEST；GLM 取证方 OpenAI→Hugging Face
3. **方向反转**（最危险）：USPTO「驳回长存挑战」被写成「获正面回复」；JX 金属扩产 7-10 倍被写成「仅 20%」；「已发射 100 颗」实为 1 颗演示星；高盛看多被写成担心毛利见顶（庆桂铉观点张冠李戴）
4. **数字偏差**：美光涨幅 20%→60%/85%；133Tb/s→TB/s；16GB→Gb；份额 70%→55-58%；灵巧手成本占比 50%→15-25%；钽电容 200G→μF 级
**预防**: 已固化进 CLAUDE.md「转录语料断言核查」节——extract 后、promote 前对断言性节点核查（普查：分 8 组 subagent 并行；抽样：8-10 条可覆盖全部四类模式）。参数型数据（带宽/容量/时间表）准确率高，断言型表述错误率高——抽样时优先挑断言句。
**审计留痕**: 117 处订正落图（properties.verify_fix_20260816）；报告 raw/核实/2026-08-16-Boss老白普查核查报告.md；订正清单 outputs/bb_verify/fix_X.json + fix_D.json。

**分层归因（2026-08-16 回源比对实证 · Doctor 认可）**: 三层各有系统性贡献——① **ASR 层 ~35-40%**：专有名词谐音错字（9+ 个全命中转录原文）+ 英文缩写（RRAM→RDM、HBC→HPC、Tb/TB），特征=词表外词系统性同音错；② **语料层 ~30-35%**：转录忠实但主播口播即错——USPTO 方向反转、Starcloud「大约一百」（实 1 颗）、JX「只扩 20%」（官方 7-10 倍）、钽电容「两百G」，特征=方向反转+独家数字与官宣矛盾；③ **LLM 层 ~20-25%**：转录正确被 LLM 改错——闪迪→美光（刻板印象替换）、RDM→RDRAM（熟悉化修正，ASR+LLM 复合放大）、SK 份额 70%（源文无此表述，泛化知识混入）。**治理三路**：ASR 靠专有名词热词表；LLM 靠「忠实优先、禁知识补全」prompt 约束；**语料层的错修不掉，只能靠独立核查层兜底**（「promote 前断言核查」流程存在的根本理由）。

**追记 2026-08-22（德科立「谷歌300台」案例 · 同族新变体：调研测算语境→「已交付」事实）**：帕米尔 2026-06-24 硅光波导 OCS 调研 L59「德科立主攻硅光波导OCS，32端口产品**已交付谷歌300台**」被 research-帕米尔 2026-06-28 按事实入库（`metric_DekeliOCS32PortOrders2026` props google=300/delivered=300 + `company_Dekeli` desc），并与图内 `event_OCSVolumeOrder`（2026-06-09·「谷歌10台样品+英伟达10台」口径）**图内互斥**。Doctor 专项核查三步：① **时间窗比对**——官方 2026-04-03 异动公告（「样品交付与客户验证阶段·尚未取得批量订单」）与 2026-08-21 投资者关系记录（「尚未直接向谷歌供货·通过合作伙伴推进验证及未来小批量供应·2027 年内才可能有部分收入」）两次澄清均与「已交付300台」冲突，官方最新口径晚于纪要两个月仍持否认立场，**非时序窗口、属正面冲突**；② **原文追溯**——raw 原文确有此句、非入库转译变形，但位于「谷歌2026年采购量测算」段落（与 Lumentum 4000台/Coherent 1400台并列的**分配测算语境**），且该段测算与谷歌特邀报告口径（约1.5万台总量·自研系9000-12000台·外购约3000台）整体对不上；③ **交叉信源**——全部外部信源仅见「谷歌10台样机」（雪球/韭研公社多帖），300台无任何独立印证。**判定**：300台＝单一调研纪要的测算语境数字，与官方公告正面冲突，图谱侧应标存疑待修（修复方案待 Doctor 裁：A 修正为10台样品口径 / B 保留原文并标注调研口径未证实 / C 该篇纪要整体降级）。**当前状态**：🔄 图谱节点未动（被审资产只读），本追记为治理留痕。**变体要点（2026-08-22 Doctor 纠错订正）**：原文即「已交付」陈述句、入库忠实无变形——**错在语料层，不是入库层**：纪要撰写者把「测算/分配语境」写成「已发生事实」陈述（本条第②层「语料层的错修不掉」的新案例：非主播口播错，系纪要原文错）。入库层无从识别（原文无时态标记可辨），唯一可拦防线＝断言级数字与法定披露交叉核查（本次靠官方两次公告对撞发现）。原「信源定级缺『语境时态』校验维度」表述收回——语境在原文中不可辨识，该建议不可落地。

## [ERR-20260820-001] 光纤场 2 条边非标准格式直写 canonical——缺 id 阻塞后续一切 merge
**状态**: 🔄 已修待验（2026-08-21 Doctor 裁「补字段随本 patch 一起入」→ `fix_dirty_edges_20260820.py` 已执行：备份 `bak_pre_fixdirty_20260821_001249` · 复检缺 id=0/id 重复=0/悬挂=0 · 随 commit `1a0fff4` 一并提交。**预防门禁已实装（2026-08-21 当场闭环）**：`kg_merge_safe.check_edge_schema` 第 14 项（merge 前 fail-fast）+ `rules/kg_promote.py` 第 14 项同款 + 单测 4/4（test_kg_merge_guards.py 追加·沙箱内联等效执行）+ 事故备份负测精确复现 2 条 + CLAUDE.md 质检表 14 项同步。整体 ✅ 待独立验收，实施者不自签）
**优先级**: 🟡 中（阻塞面=全库后续 merge/promote）
**触发**: 2026-08-21 机构调研日记入库场：`kg_merge_safe.py --dry-run mapping/_v3_20260820_机构调研日记视频_manual.json` 报 `KeyError: 'id'`（kg_merge.py L149 `edge_index = {e["id"]: ...}` 构建时炸）——canonical 有 2 条边缺 id 字段。
**硬证据/最小复现**: `g['edges']` 扫描缺 id 边 = 2 条，均 created_by=research-CC、created_at=2026-08-20、source_file=「2026-08-20-光纤产业信号型号辨析札记.md」：① `concept_FiberProductLinePriceDivergence -constrains-> concept_FiberPricingUpside`；② `concept_HengtongNewPreformCapacity2027E -constrains-> concept_FiberPricingUpside`。字段用非标准 `desc`（非 description）+ `source_file`，缺 id/direction/weight/evidence/updated_at/data_sources。最小复现 = 任跑一次 kg_merge_safe --dry-run 即炸。
**根因**: 08-20 光纤札记场写 canonical 未走 kg_merge_safe 标准链路（无对应 `mapping/_v3_20260820_光纤*` patch 文件；backups 有 `bak_pre_promote_20260820_060826` 说明有 promote 动作；brain/logs 无该场日志——写入与留痕均缺失）。结构校验（悬挂/自环/type/重复）不查 id 存在性，脏边静默通过。
**影响面**: 阻塞后续一切 kg_merge/kg_promote（edge_index 按 id 构建）；按 08-20 概览 4977/5554 vs 实测 4978/5556 对账，光纤场贡献 +1 节点/+2 边（概念节点正常、仅边脏）。
**建议修法**: ① 2 条边补标准字段（id 按 `rel_source_type_target` 规则 · desc→description · 补 direction/weight/evidence/updated_at/data_sources，内容不动），随下一 patch 一起 promote；② 或该场重新走标准 patch 链路重建 2 边。①②均待 Doctor 裁（改别场产物+canonical 数据）。
**预防门禁**: kg_merge_safe/kg_promote 增「边 id 存在性 + 必填字段断言」（第 10 项之后）；直改 canonical 必须先过 merge_safe 校验；场次结束不留痕（无日志无 patch）应触发哨兵。**⇒ 2026-08-21 已落地（当场闭环）**：`kg_merge_safe.check_edge_schema`（L145 · merge 前 fail-fast）+ `kg_promote.py` 第 14 项同款 + CLAUDE.md 质检清单 14 项同步（commit `cb46d6948d`）。**未落地（仍开）**：「无日志无 patch 哨兵」未实装；第 14 项负向单测仅沙箱内联等效执行——tests/ 无持久化用例，待持久化（证据可重放门）。
**来源**: 2026-08-21 机构调研日记入库场 dry-run 阻塞（KeyError + 2 边 dump 硬证据）


## [ERR-20260823-001] 光迅双节点 + 「HiSilicon Optical」编造别名错并
**状态**: ✅ 已验收（2026-08-23 Doctor 裁方案 A「并入 Accelink」→ 手术脚本 `surgery_merge_guangxun_20260823.py` 已执行：删 `company_Guangxun` · 4 边迁入 `company_AccelinkTechnologies`（id 同步改）· 别名合并剔除「HiSilicon Optical」· desc 增量 + 帕米尔两条信源迁入 · 备份 `bak_surgery_guangxun_20260823_010203` · QA 全绿 · wiki 旧卡 `_DEPRECATED_guangxun_20260823.md` 改名。**✅ 2026-08-26 Doctor 终签**：四批打包独立验收（Doctor 裁「四批打包+独立 agent 复核」）——机器层十项九过 · 墓碑缺失异议 → Doctor 裁「补墓碑再销账」→ `mapping/_tombstones/2026-08-23_guangxun_merge.json` 已补〔dropped_node 提取自术前备份 · 4 边 id_map 留档〕· 判断层三问全部认可 · CC 代记留痕）
**优先级**: 🟡 中（检索/问答歧义 + 华为链「光迅」归属一度存疑）
**触发**: 2026-08-23 华为 OCS 链入库场：挂「光迅独家光交换模块」边前核 canonical，发现同公司双节点——`company_Guangxun`（2025-10-30 建 · aliases 含「HiSilicon Optical」）与 `company_AccelinkTechnologies`（2026-08-16 建）并存。
**硬证据/最小复现**: 实读两节点 aliases/desc/created 字段（上文摘录在案）；`grep -r "HiSilicon Optical" raw/` 全树零命中——唯一命中为我方 08-23 札记，即该别名无原文出处（疑 LLM 入库编造或错并）；海思光电子（HiSilicon Optoelectronics，华为海思旗下）≠ 光迅科技（Accelink，中国信科旗下），canonical 无海思光电子独立节点。
**根因**: 2025-10 帕米尔 OCS 解读篇入库时 LLM 把华为链另一实体名混入光迅 aliases；同公司双节点因两批（2025-10 帕米尔 / 2026-08 Boss老白）各自建节点、无「同名实体查重」门禁而未撞见。
**影响面**: 同实体信息分裂两处（Guangxun desc 薄 vs Accelink desc 富）；华为链「光迅」边归属悬而未决直至本场核实；下游 wiki/问答按 id 检索会漏一侧。
**建议修法**: 已按 Doctor 裁方案 A 执行（见状态行）。备选未用：方案 B 并入 Guangxun（id 非官方英文名·desc 薄）；方案 C 仅剔别名不合并（分裂状态残留）。
**预防门禁**: ① 入库 QA 增「同名实体检测」：company 节点按 name/别名交叉比对，同实体内外文名变体（Accelink/ACCELINK/光迅）归一；② aliases 元素须与节点实体同指（「X Optical」类公司名混入别家公司 aliases 即报）——现有 QA 无此项；③ 与 FIX-20260625-001（张冠李戴·误记归属）族域相近（实体错配）但形态不同（编造别名 vs 误记归属）——若实体错配族第三次出现，按合同升格通用教训（升格由 Doctor 裁，本条不自升）。
**来源**: 2026-08-23 本会话（华为 OCS 链入库 → 光迅边归属核实 → Doctor 令修正 → 方案 A 执行）
**追记 2026-09-01（同根复发 · 第 2 次 · 帕米尔 9 篇批）**: 同族再发 3 例——LLM 新建重复公司 `company_Jingzhida`（精智达 vs 存量 `company_JingZhiDa`）/`company_WeiceTechnology`（伟测 vs 存量 `company_Microtest`）/`company_LuxsharePrecision`（立讯 vs 存量 `company_Luxshare`）。**形态差异**：非编造别名，而是 node_reference 主题过滤窗口（120/5195）漏掉既有公司 → LLM 当新实体建节点。批内 QA 已并（边重指 11 · desc/props/aliases 并集 · dup 删除 · 备份 `.bak_ccfix_20260901` · 脚本 `outputs/cc_qa_fix_20260901.py`）→ promote 落盘 5298/5919 · 读盘核验 keeper 度 2/20/11 · 重复零残留。**预防门禁强化建议**：批内 QA「同名实体检测」此前仅靠 CC 手工（本次 3 例即手工逮到）——候选=固化进 QA 脚本（新 company 节点 name/aliases ∩ 存量 name/aliases 非空即报），与 ERR-20260602-001「aliases∩存量非空即判撞存量」门禁候选合并推进。**应升格通用教训**：实体错配族第三次出现（06-25 张冠李戴 / 08-23 编造别名 / 09-01 重复建节点）——按合同登记「应升格通用教训」（升格由 Doctor 裁，本条不自升）。
**追记 2026-09-01 深夜（同根复发 · 第 4 例 · 存量产品双节点 · 51.2T 问答场实读逮到）**: `product_Centec51dot2T`（2026-07-16 建 · 帕米尔 07-16 源 · 三星流片·双25.6T拼合·阿里 Q3/Q4 测试·2027Q1 应用）与 `product_Shengke51p2TSwitchChip`（2026-08-07 建 · 西部证券 08-07 源 · 2026-06 tapeout·双25.6T拼合·阿里 Q3/Q4 测试·2027Q1E 商用）为**同一产品（盛科 51.2T 双拼合方案）双节点**——硬证据：architecture 字段同为「双25.6T拼合」+ 测试/商用时间线三处一致 + desc 指同一实体。两批不同来源（帕米尔/西部证券）各自建节点未撞。**形态**：与批内 3 例同族（LLM 未查重新建），但发生在存量（07-16/08-07 两批），跨度 22 天未被任何 QA 发现。**处置**：本追记登记（预授权治理留痕）；合并手术归 Doctor 令（沿 08-28 C 档手术范式：度高者主·desc 并入·旧 id 入 aliases·边重指·墓碑）。**⇒ 2026-09-01 深夜整合手术已执行（Doctor 令）**：`product_Centec51dot2T` 并入 `product_Shengke51p2TSwitchChip`（边重指 6·三元组冲突 0·desc 合并 382 字含「双 25.6T 拼合 ≠ TH5 Ultra 原生 scale-up 单芯片」disambiguation + 回片时间线双口径注记·墓碑 `_tombstones/2026-09-01_centec51dot2t_merge.json`·备份+手术记录在盘·复检全绿 5297/5920）· 状态：🔄 已修待验（实施者不自标 ✅）。**关联**：两节点 desc 的口径差异（三星流片 vs 2026-06 tapeout；PFC 流控 vs OSA 生态定位）也是「拼合方案 vs 原生 scale-up 单芯片」概念混淆的图内表现——合并 desc 已写清 disambiguation。
**追记 2026-09-05（同根复发 · 第 5/6 例 · 六篇批）**: LLM 新建重复公司 2 例——`company_XiamenJinlu`（厦门金鹭 vs 存量 `company_XiamenGoldenEgret`）/`company_DingtaiGaoke`（鼎泰高科 vs 存量 `company_Dingtai`）。批内 QA 已并（各 1 边重指 · DingtaiGaoke 产能/结构 props 迁入 keeper · dup 删除 · 同批未 promote 无需墓碑）。另 `company_ZhongwuGaoxin`（中钨高新·株硬/金洲打包建节点）归正为株硬主体：金洲产能 props+50 倍供给边迁至存量 `company_JinzhouPrecision`，补 part_of 边（金洲精工→中钨高新）。修复脚本 `outputs/cc_qa_fix_20260905.py` · promote 落盘 5375/5996 · 复检全绿。**预防门禁**：批内 QA「新 company 节点 name/aliases ∩ 存量 name/aliases 非空即报」仍靠 CC 手工（09-01 已登记候选·本次再实证）——固化进 QA 脚本待 Doctor 批（与 ERR-20260602-001 候选合并推进）。**来源**：2026-09-05 帕米尔六篇批入库 QA 场。

## [NOTE-20260901-002] 「OSA」系 OISA 之误——西部证券笔误被图内继承（1 节点 + 2 边 desc）

**状态**: 🔄 已修待验（2026-09-01 整合手术已执行：`concept_ScaleUpSwitchProtocolOSA` → `concept_ScaleUpSwitchProtocolOISA`（旧 id 入 aliases·name/desc 重写·边端点同步·边 id 留旧）+ `product_Shengke51p2TSwitchChip` desc「OSA→OISA」· 备份 `bak_surgery_centec_oisa_20260901_*` · 手术记录 `mapping/_v3_20260901_盛科曦智OISA整合_手术记录.json` · 复检全绿·实施者不自标 ✅）

**优先级**: 🟡 中（术语错误→按「OSA」检索/对齐漏掉 OISA 官宣与生态信息；下游消费端引用会传播错误术语）

**触发**: Doctor 裁「西部证券（郑宏达）为 P2 信源·独立核实」→ 核实发现中国移动协议实名 **OISA（智算开放互联协议）**；西部证券原文写「OSA」；图内 `concept_ScaleUpSwitchProtocolOSA` 节点（id/name/desc）+ 2 条边 desc（OSA 生态边×2）+ `product_Shengke51p2TSwitchChip` desc「基于 OSA 协议」均继承笔误。

**硬证据**: 中国移动 2025-08-25 中国算力大会 OISA 2.0 发布官宣 + 生态共建签约名单（盛科/燧原/壁仞/摩尔线程/昆仑芯/浪潮 · P1）+ 2026 移动云大会 OISA 卡间互联原型验证平台（C114 · P1）；西部证券 raw 原文在盘（2026.08.07 行 19/32/76 均写「OSA」）。核实札记 `raw/核实/2026-09-01-盛科51.2T与超节点交换芯片独立核实札记.md`。

**影响面**: 术语层失真——实体存在（OISA 协议真实），但按错误名检索会漏官宣信息；与盛科 51.2T 回片时间线冲突（西部证券「Q3 回片」vs 主流纪要「年底回片·2027H2 收入」）同源同场，札记 §四已列修复项。

**建议修法**: 节点 id 改 `concept_ScaleUpSwitchProtocolOISA`（旧 id 入 aliases · 沿 FIX-20260625-001）+ name/desc 同步 + 2 边 desc 同步 + `product_Shengke51p2TSwitchChip` desc「OSA→OISA」；与盛科双节点合并手术（ERR-20260823-001 第 4 例）打包成一个手术批，归 Doctor 令。

**来源**: 2026-09-01 盛科 51.2T 独立核实场（Doctor 裁 P2 核实 → 札记落盘 → 本条目登记）。


## [ERR-20260825-001] 帕米尔 08-25 批入库产生同三元组重复边——kg_promote 通道无「同三元组」闸
**状态**: ✅ 已验收（2026-08-25 Doctor 裁「删旧留新+补闸」→ 删边+补闸已执行，见下。**✅ 2026-08-26 Doctor 终签**：四批打包独立验收（机器层九项过 · 第 15 项闸源文在盘实读 · 判断层三问全部认可 · CC 代记留痕））
**优先级**: 🟡 中（重复边阻塞后续一切 kg_merge_safe 入库）
**触发**: 2026-08-25 Vera Rubin 实测入库场：`kg_merge_safe.py --dry-run mapping/_v3_20260825_VeraRubin实测_manual.json` 报「合并后全图存在 1 组同三元组重复边」——`constrains concept_InPSingleCrystalFurnaceBottleneck -> concept_InPCapacityExpansion` ×2。
**硬证据/最小复现**: 两条边 dump 在案——旧边 `rel_InPSingleCrystalFurnaceBottleneck_InPCapacityExpansion`（07-18 建·P2 帕米尔 07-14 源）；新边 `rel_EquipmentShortage_ExpansionBottleneck`（**2026-08-25 建**·P1 帕米尔 08-24 源·created_by=research-帕米尔）——即 08-25 帕米尔 6 篇批入库时 kg_ingest/kg_promote 生成了与 07-18 存量同三元组的重复边。最小复现 = 对 canonical 跑 `check_triple_duplicates` 即见 1 组。
**根因**: 同三元组检测（check_triple_duplicates·2026-08-15 三轮清洗专场立）只实装在 kg_merge_safe（merge 前全图计数）；**kg_promote 通道（rules/kg_promote.py）没有此闸**——batch 入库走 promote 不经 merge_safe，重复边静默入 canonical。
**影响面**: 存量清零断言被破坏；后续一切 kg_merge_safe 入库被拦（本场 Rubin patch 即被阻塞）；重复边进入下游 wiki/检索造成双答案。
**建议修法**: ① 删旧留新（新边 P1 源新·证据全）——Doctor 已裁；② kg_promote.py 补同三元组闸（与第 14 项 check_edge_schema 并列）——已执行。
**预防门禁**: promote 闸集与 merge_safe 闸集保持一致（至少同三元组+边 schema 两项）；batch 入库后跑一次全图 check_triple_duplicates 冒烟。
**追记 2026-08-27（同根复发 · 五篇批）**: 东材科技→台光电材 supplies 同三元组再发（旧边 07-18 PPO 树脂篇 vs 新边 08-26 覆铜板树脂篇）。第 15 项闸本次**拦住并成功预防**（promote 首跑被拒·canonical 未动）。新流程教训：**promote 门语义＝只增不改**（lost 检查管删），批内 QA 带「删边」语义时门必拒——两条路（还原旧边→第 15 项拦 / 删旧边→lost 拦）都走不通。正确路径＝删边手术脚本**前置**（备份 + 手术记录留档 + 补偿校验：candidate 新边带 merged_from 注记+ds 并集才放行删除），promote 纯增量两闸全过。处置：bak_surgery_dedup_20260827_233904 + `mapping/_v3_20260827_重复边去重_手术记录.json`。
**来源**: 2026-08-25 本会话（Vera Rubin 实测入库 → dry-run 阻塞 → 重复边 dump → Doctor 裁删旧留新+补闸）

## [NOTE-20260826-001] 独立复核发现结构瑕疵三观察（08-26 四批验收附知 · 非四批引入）
**状态**: ⚠️ 已知风险（观察中 · 修复方案待 Doctor 裁）
**优先级**: 🟢 低（不影响结构完整性——QA 八项全绿；影响面=下游过滤/检索/治理精度）
**触发**: 2026-08-26 渊图四批独立验收（Doctor 裁「四批打包+独立 agent 复核」）机器层 C 项全图 QA 时附报。
**硬证据/最小复现**: canonical 实读（复现命令见下）——① 全图 2 节点缺 type 且缺 created_at：`concept_HuaweiAscend`、`concept_AlibabaCloudMaaSBusinessModel`（独立复核按备份链差集定位为 08-25 promote 批产物）；② 5 个 `hospital_` 前缀节点 type=concept、created_at=2026-08-16（Boss老白批存量）：hospital_Huashan/Xuanwu/Xiangya/JiangxiProvincial/WannanTiantan——id 前缀语义与 type 字段双轨不齐；③ 存量边 `rel_NorthAmerica_SOE_Constrains_Guangxun`（2026-06-08 建 · concept_NorthAmericaSOEBackgroundBarrier -constrains-> company_NewPhotonics）id 残留「Guangxun」字样，source/target 均与 Guangxun 无关。
**根因**: ① 08-25 promote 批 2 节点 type/created_at 字段漏填（kg_promote 门禁无「type 必填」断言）；② 08-16 批节点 id 前缀与 type 命名双轨（前缀治理归 id、type 归 schema，两套规范未对齐）；③ 08-23 光迅手术脚本断言只拦「company_Guangxun」子串，未覆盖其他 id 形态中的 Guangxun 字样（该边先于手术存在且无需改动，属断言覆盖面观察非手术漏改）。
**影响面**: ① 下游按 type 过滤会漏读 2 节点；② hospital_ 前缀语义漂移影响按前缀治理的准确性；③ 边 id 语义残留致按 Guangxun 检索时误命中无关边。
**建议修法**: ① 2 节点补 type=concept + created_at（事务性 · 走 kg_merge_safe update 或一次性小 patch）；② 5 节点归入既有「畸形节点 id/name 注记」挂账（TODO 渊图挂账批发④）不动；③ 边 id 不动（id 不可改 · 可逆性优先），手术脚本断言由子串改 id 全集比对。
**预防门禁**: kg_promote 增「节点 type 必填」断言（第 16 项候选，与第 15 项同三元组闸同款）；手术脚本删除断言用 id 全集而非子串。
**追记 2026-08-27（同根复发 · 第 2 次 · 五篇批）**: 同型再发 2 例且更重——LLM 把新建节点误放 **update 槽**，产出 `concept_400mWCPOExternalLaser`/`concept_NvidiaCPOSwitchVendorLandscape` **name/type/created_at/aliases/span 五字段全缺**（仅 desc+props+ds 有料）。批内 QA 当场补全（原文定位 span 实句）。观察①存量 2 节点（HuaweiAscend/AlibabaCloudMaaS）修复方案仍待 Doctor 裁。**预防门禁第 16 项候选（kg_promote 节点 name/type/created_at 必填断言）仍未实装**——同族第二次复发，按 GOTCHAS 合同应登记「应升格通用教训」（升格由 Doctor 裁，本条不自升）。
**来源**: 独立复核 agent 报告（2026-08-26 · 四批验收 C 项附报）+ CC 独立复验（type/created_at/前缀/边四类实读全部坐实）

## [NOTE-20260828-001] 胜宏双节点合并手术漏迁 props——Shenghong 6 业务键随节点删除丢失（已从墓碑当场回填）

**状态**: 🔄 已修待验（2026-08-28 当场修复：propsfix 脚本从墓碑 dropped_node 回填 6 业务键入 VictoryGiant + 补 `h1_2026_claim_verification_note` · 读盘核验 22 props 键·计数守恒 5174/5796 · 备份 `bak_shenghong_propsfix_20260828_002902` · 实施者不自签）

**优先级**: 🟡 中（数据层静默丢失——结构 QA 全绿查不出 props 缺失，desc/边/别名均正常迁移，只有并集对比能发现）

**触发**: 2026-08-28 胜宏双节点手术（Doctor 裁「现在并」）——主手术脚本迁移了 8 边/aliases/desc，**漏迁源节点 6 个业务 props**（rubin_compute_tray_share_2026_pct=75 等）；读盘核验步对比 wiki 旧卡发现缺失。

**根因**: 手术脚本模板缺「props 并集断言」——历次手术惯例（08-15 dedup「props 取并集」/08-23 光迅「desc 增量+信源迁入」）未固化为模板断言，本轮手写脚本遗漏。

**影响面**: 若未发现：Rubin 份额/谷歌 TPUv8 份额/产能 props 永久丢失（仅存于 wiki 旧卡与墓碑），下游份额查询失真。

**修复**: 墓碑回填（墓碑含完整 dropped_node——可逆性设计兜底生效）；补丁键名撞名断言 fail-fast。

**预防门禁**: 手术脚本模板固定三步：① aliases 并集 ② desc 合并 ③ **props 并集断言**（源节点业务键全部迁入·撞名即 exit 1）；术后读盘核验清单加「props 键数 = 术前两节点并集数」。

**来源**: 2026-08-28 胜宏双节点合并手术场（outputs/surgery_merge_shenghong_20260828.py + propsfix 脚本）

**追记 2026-09-01（中微三节点并一手术 · 新变体实例）**: props 并集断言实弹逮住**治理元键冲突**——company_AMEC 的 `_region_src`="默认" vs 主节点 company_Zhongwei 的 `_region_src`="code"（同值不同源）。处置判据（新增）：**键名属治理元键（`_region_src` 等 `_` 前缀治理键）→ 保主节点值不覆盖；业务键冲突 → 仍 exit 1**。手术模板判据从「同值跳过」升级为「同值跳过 / 治理元键保主 / 业务键冲突拦死」三级。

## [NOTE-20260901-001] kg_ingest --batch 自动发现图谱失败——find_latest_kg 只扫根目录，canonical 在 mapping/ 子目录

**状态**: 🔄 已修待验（2026-09-01 当场修复：`find_latest_kg` 增加 `d/mapping` 级 glob（kg_ingest.py L1185-1192）· py_compile OK · 独立复刻测试 2/2 PASS〔mapping 级发现+canonical 优先压过 _v2 历史件 / 根级发现回归〕· 实施者不自标 ✅）

**优先级**: 🟡 中（batch 起跑即挂·零数据影响·但新 shell 必踩）

**触发**: 2026-09-01 21:48+ 渊图 9 篇帕米尔 batch 场——Doctor 终端 `python3 kg_ingest.py --batch`（无 --base/KG_BASE_JSON）→ exit「未找到知识图谱 JSON，请用 --base 指定路径」。

**错误信息**: 未找到知识图谱 JSON，请用 --base 指定路径

**根因**: `find_latest_kg` 只 glob 搜索目录**根级**的 `行业知识图谱_*.json`（~/Downloads + ~/Documents/Database/行业研究 根）；canonical 现居 `mapping/行业知识图谱_完整数据库.json` 子目录、根级无副本 → 发现失败。此前 batch 能跑，推测当时根级/Downloads 有历史副本（后被清理——机制依赖的隐性前置条件消失）。

**影响面**: batch 起跑即挂（本次显式 --base 绕过+代码修复双保险）；若 Downloads 有陈旧副本，自动发现会静默挑错 base（Downloads 目录本轮未核，风险仍开）。

**修复**: `find_latest_kg` 每个搜索目录加 `d/"mapping"` 级 glob；排序保证「完整数据库」压过 `_v2` 历史件（「完」>「v」lexicographic）。

**预防门禁**: 本轮已修代码；Downloads 陈旧副本检查（`ls ~/Downloads/行业知识图谱_*.json`）待 Doctor 顺手核——有则移走/归档。

**来源**: 2026-09-01 渊图 9 篇帕米尔 batch 场（CC 实读 kg_ingest.py L1185-1190/L1221-1233 定位根因）。

**追记 2026-09-01 22:18（同根第二次 · v1 修复排序假设翻车）**: v1 修复（mapping 级 glob）生效后首次真实 batch 仍选错 base——「空」(U+7A7A) 码点 >「完」(U+5B8C)，`行业知识图谱_空白模板.json` 字典序压过 canonical，batch 以 **15 节点模板**为 base 跑完全批 9 篇（node_reference 仅 0-17/15·LLM 查重失效·_v2 产物 125 节点不含 canonical 存量）。**处置**：canonical 零触碰（mtime/counts 5195/5829 不变·实核）；副作用已回滚（prices 截断 990→964〔断言行 964＝px_BT树脂_08-26 末行〕·price_processed 9 标记移除·index kg_processed 9 篇回退 false·latest.json 重建 947 条·三备份 `*.bak_pre_rerun_20260901` 在盘）；v2 修复＝显式排除模板＋显式优先「完整数据库」＋mtime 兜底（py_compile OK·测试 3/3 PASS 含真目录）；run1 两个 _v2 文件（`221406_5篇`/`221842_9篇`）**废弃·勿 promote**。**应升格通用教训候选**：字典序/隐式排序不得承载业务语义——与「日期格式先归一」（YYYYMMDD vs YYYY-MM-DD 整年错位）同族，本坑为该族第三次变体。

