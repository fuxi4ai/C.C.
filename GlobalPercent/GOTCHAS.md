---
title: GlobalPercent · GOTCHAS（已知坑）
tags: [GlobalPercent, gotchas, Financial]
created: 2026-06-29
updated: 2026-06-29
status: active
type: resource
project: GlobalPercent
---

# GlobalPercent · GOTCHAS（已知坑）

> 排查超过一轮的问题都该记录在这里。CC 遇到报错并解决后**立即**回写，无需 Doctor 提示。
> 项目内还有一份实时错题本：`Claude/Projects/Financial/GlobalPercent/GOTCHAS.md`；这里是沉淀+索引。

## 格式

```
## [ERR-YYYYMMDD-NNN] 简要描述
**状态**: ✅ 已解决 / ⏳ 待解决
**优先级**: 🔴 高 / 🟡 中 / 🟢 低
```

---

## [RISK-20260629-001] Polymarket `oneDayPriceChange` 量纲未核 → 动量可能静默饱和
**状态**: ⏳ 待解决（需本机联网核一条真实行）
**优先级**: 🟡 中（但若踩中，headline 数字被静默打偏，影响面大）
**触发场景**: `index.py` 动量分 = `min(|change_24h| / momentum_ref(0.10), 1.0)`。`sources/polymarket.py:49` 直取 `oneDayPriceChange`。
**风险**: 若该字段返回的是**百分数（如 3.0 表示 3%）而非分数（0.03）**，则 `|3.0|/0.10` 远超 1、动量瞬间饱和到 100，凡 Polymarket 占比高的模块全读「最热」，总指数失真。Kalshi 侧已验证为 `last−prev` 概率点（量纲对），唯 Polymarket 这一处存疑。
**核实办法**: 本机 `curl 'https://gamma-api.polymarket.com/markets?limit=5&order=volume24hr&ascending=false&active=true&closed=false'`，看 `oneDayPriceChange` 实际取值范围（≈±0.0x ⇒ 分数、对；≈±x.x ⇒ 百分数、需在 `_shape` 里 /100 或调 `momentum_ref`）。沙箱白名单不含该域名，核不了。

## [GOTCHA-20260629-002] 一批修复改了未提交，悬在 initial commit 之后
**状态**: ⏳ 待解决（需 Doctor 终端 git）
**优先级**: 🟡 中
**触发场景**: `git status` 显示 `aggregator.py / publish.py / GOTCHAS.md / requirements.txt / test_publish.py` 已改 + `tests/test_aggregator.py` 新增，全未 commit（initial commit = `beffe24`）。
**风险**: 一旦 checkout/clone 丢这些修复。
**解决**: Doctor 终端 `git add -A && git commit`（CC 不在沙箱跑 git 写命令）。

## [GOTCHA-20260629-003] 百分位校准用全量历史、无滚动窗口
**状态**: ⏳ 待解决（设计改进）
**优先级**: 🟡 中（长期才显现）
**触发场景**: `store.percentile` 读 metric 全表算排名。
**风险**: 长期运行 regime 漂移——拿当下读数和远期分布比，「比过去 73% 热」失真。
**解决**: 加滚动窗口（近 N 点或近 90 天）。

## [NOTE-20260629-004] 沙箱白名单不含预测市场域名
**状态**: ✅ 已知边界
**优先级**: 🟢 低
**说明**: 本会话沙箱 `gamma-api.polymarket.com` / `api.elections.kalshi.com` 直连与走 3128 均返回 000（不在白名单）。真实数据冒烟与量纲核实只能本机做，或 Doctor 临时加白名单后在沙箱做。

## [RESOLVED-20260607] .venv 38M 入树 + 无 git 仓
**状态**: ✅ 已解决（2026-06-29 复核）
**说明**: 6-07 审计两条问题——38M macOS `.venv` 物理在树内、项目无 git 仓——复核时均已解决：`.venv` 已移出、`.gitignore` 覆盖、项目已纳入 git（`beffe24`）。

## [DOC-20260629-005] 文档测试数三处不一致
**状态**: ⏳ 待修（trivial）
**优先级**: 🟢 低
**说明**: PRD 写「21」、INDEX/STATUS 写「26」、实跑 = **28**。统一改 28。
