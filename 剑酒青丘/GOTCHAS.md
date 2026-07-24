---
title: 剑酒青丘 · GOTCHAS（已知坑 · 索引）
tags: [剑酒青丘, gotchas, index]
created: 2026-07-24
updated: 2026-07-24
status: active
type: resource
project: 剑酒青丘
---

# 剑酒青丘 · GOTCHAS（已知坑 · 索引）

> 剑酒青丘＝金融取数/回测基础设施（`infrastructure/取数工具/` 下 adjustment_grade / market_health / snapshot 等）。本文件是本项目坑的落地处。
> **编号**：`[BUG-YYYYMMDD-NNN]`（代码）/ `[INFRA-…]`（环境·链路）/ `[RISK-…]`（已知风险）。**状态**：✅ 已修复 / 🔄 待修复 / ⚠️ 已知风险。

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
