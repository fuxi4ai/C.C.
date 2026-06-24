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
**状态**: ✅ 已解决 / ⏳ 待解决
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
