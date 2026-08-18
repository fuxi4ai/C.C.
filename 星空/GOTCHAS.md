---
title: 星空 · GOTCHAS（已知坑 · 索引）
tags: [星空, gotchas, index]
created: 2026-07-24
updated: 2026-07-24
status: active
type: resource
project: 星空
---

# 星空 · GOTCHAS（已知坑 · 索引）

> 本文件是 星空（Starry Skies）项目坑的落地处（REQ-F2 补建，2026-07-24）。
> **编号**：`[BUG-YYYYMMDD-NNN]`（代码）/ `[INFRA-…]`（环境·链路）/ `[RISK-…]`（已知风险）。**状态**：✅ 已修复（**仅由 Doctor 或指定独立验收方落，实施者不得自标**）/ 🔄 待修复·已修待验 / ⚠️ 已知风险。

## 条目

## [BUG-20260813-001] #info 的 overflow-y:auto 连带裁掉卡外伪元素 → 热区失效（折叠坞冷区根因）
**状态**: ✅ 已修复（2026-08-13 四改：改用独立元素 `#info-edgezone`）
**优先级**: 🔴 高
**触发场景**: 全景看点卡右缘 44px 热区用 `#info::after { right:-44px; width:44px }` 实现，实测悬停无效——卡与收合线之间出现「冷区」。
**真因**: `#info` 自带 `overflow-y: auto`，CSS 规则下 `overflow-x` 连带计算为 `auto`——伪元素伸出滚动容器外的部分被整体裁剪（绘画+命中测试都裁），44px 热区从未生效。
**解决**: 卡外热区一律用独立 fixed 元素（`#info-edgezone`），不受卡 overflow 裁剪；热区高度由 JS 同步卡的 `offsetHeight`（伪元素在 scroll 容器里还会随滚动内容移动，独立元素无此病）。
**预防**: 凡「伸出滚动容器边界的伪元素热区/手柄」必先查容器 overflow；两区相邻的 hover 切换另见 BUG-20260813-002。

## [BUG-20260813-002] 纯 CSS hover/:has 切换热区几何有指针跨界竞态 → 改 JS 状态机
**状态**: ✅ 已修复（2026-08-13 五改：JS 标记状态机 + body.info-open）
**优先级**: 🔴 高
**触发场景**: 热区随卡开合变几何（收起 8px 悬浮带 / 打开 44px 整段），若用 `body:has(#info:hover)` 切换——指针从卡跨入间隙的瞬间 `#info:hover` 变 false → 热区回缩 → 指针落空 → 卡收起（冷区或抖动）。
**真因**: hover 状态切换与几何切换同帧竞态，纯 CSS 无「指针离开 A、进入 B」的容错窗口。
**解决**: JS 状态机——mouseenter/mouseleave 布尔标记（overCard/overZone）+ 统一 `syncDock()` 驱动 `body.info-open` 类（开合 + 热区范围两件事同源）；焦点态 `.expanded` 并入同一函数。
**预防**: 交互元素几何随 hover 状态变化且两个热区相邻时，优先 JS 标记状态机；纯 CSS :hover 只适合单元素、几何不变的场景。
