---
title: 海螺姑娘 · GOTCHAS（已知坑）
tags: [海螺姑娘, gotchas]
created: 2026-05-14
updated: 2026-05-14
status: active
type: resource
project: 海螺姑娘
---

# 海螺姑娘 · GOTCHAS（已知坑）

> 排查超过一轮的问题都该记录在这里。CC 遇到报错并解决后**立即**回写，无需 Doctor 提示。
> 实时操作日志写在项目目录的 `Projects/海螺姑娘/GOTCHAS.md`；这里是沉淀+索引。

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

## [GOTCHA-20260624-001] 改 GAI artifact 本身无效——它是构建管线的产物，refresh 会冲掉手工改
**状态**: ✅ 已解决（修管线治本）
**优先级**: 🔴 高
**触发场景**: 手工编辑 `Artifacts/global-asset-inventory/index.html`（加数灵行/brain治理/错题本告警/DVA L3），下一次 `refresh-asset-dashboard`（每日 08:10 + 看板 🔄 按钮）触发后，手工特性全被冲没。
**根因**: GAI artifact 是**构建管线的产物**，不是真源。真源 = `dashboard/build_asset_dashboard.py`（HTML 模板）+ `data/asset_manifest.json`（数据）。refresh 任务跑 `survey → build_asset_dashboard.py 重建 HTML → update_artifact`，从源头重生，覆盖一切只改在 artifact 上的内容。
**解决方案**: 两头都补——① `asset_manifest.json` 源加数据（agents/dva_authors/brain/detail_view）；② `build_asset_dashboard.py` 模板加渲染（用已验证 artifact 反推：剥 meta 块、manifest 内容换回 `__MANIFEST__` 占位）；③ 先验证 `cmd_survey` 只就地改 status/freshness、不重建不删别的字段，故源加的字段会被保留。
**预防措施**: 凡看到 `Artifacts/*/index.html` 想改，先查它有没有 `dashboard/build_*.py` 这类生成器——有就改源（脚本+manifest），别改产物。改 artifact 只能当临时回退。配套通则见 [[通用教训]] G-X27。

## [GOTCHA-20260820-002] conch survey brain GOTCHAS 计数闭集关键字误杀未闭条目（假阴性）
**状态**: 🔄 待修复（2026-08-20 refresh-asset-dashboard 定时任务实锤 · 登记留痕 · 实施者不自签；应升格通用教训——同根逻辑此前已在渊图/龙鱼五力以假阳性方向出现）
**优先级**: 🟡 中
**触发场景**: `conch_engine.py` survey 回写 brain 治理计数（L841-852）：按 `## [` 分块 → 块前 600 字内取 `**状态**:` 行 → 状态行含 `✅/已解决/已根治/已修复/已关闭/已知` 任一关键字即判已闭跳过，否则 open_g += 1。
**硬证据/最小复现**（2026-08-20 实读盘核对，engine 判定 vs 实况）:
- DVA：3 条 `⚠️ 已知风险`（GOTCHAS.md L94/103/112）→ 状态行含「已知」→ 全被跳过 → manifest gotchas=0。真实未闭 3 ≥ 看板青碧告警阈值 3，告警被静默吞掉。
- 渊图：1 条 `🔄 已修待 Doctor 落签`（L54）→ 状态行内嵌「✅ 归 Doctor 落」字样 → 含 ✅ → 跳过 → manifest gotchas=0。
- 烛照九阴：1 条 `已修待验`（L330）→ 状态行内嵌「实施者不自签 ✅」→ 含 ✅ → 跳过 → manifest gotchas=0。
- 对照组（口径正常侧）：龙鱼五力 `🔄 待修复` L120 计入 1 ✓、风险日报 `⚠ 值守中` L93 计入 1 ✓——与 manifest 吻合，排除计数链整体断开。
**根因**: 闭集用「子串匹配」而非「状态词前缀匹配」。`已知` 关键字本意覆盖 `✅ 已知设计/已知边界` 类已闭状态词，但会误伤开状态词 `⚠️ 已知风险`；`✅` 关键字会误伤状态行正文里任何合法出现的 ✅ 字符（如「不自签 ✅」「✅ 归 Doctor 落」）。同根逻辑反向表现：渊图 GOTCHAS L22/L29 曾记录「状态词不在闭集被误开（假阳性）」，靠人工逐条补状态行消解——未治引擎匹配逻辑本身。
**影响面**: 看板错题本积压告警（≥3 青碧晕）与 GOTCHAS 徽章计数对「⚠️ 已知风险 / 状态行含 ✅ 注释」的条目系统性漏报，治理压力被静默低估。
**修复/建议修法**: 状态行判定改前缀匹配——以行首 `**状态**[:：]\s*` 后首个 token 为状态词，只有状态词以 ✅ 开头才算闭；`⚠️/🔄/⏳/已修待/待修` 等一律计入 open。修引擎前 propose-then-confirm（方向性改动），修后由 Doctor 或独立验收方落签。
**预防门禁**: ① 计数类正则改动必须配「假阳性+假阴性」双向用例（含状态行内嵌 ✅ 的样本）；② 每次 refresh 回报时对 tracked 节点抽样实读 1-2 个 GOTCHAS 状态行比对 manifest 计数。
**来源**: refresh-asset-dashboard 定时任务 2026-08-20 运行（conch_engine.py L841-852 实读 + 各项目 GOTCHAS.md 状态行实读）。
