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

## [RISK-20260629-001] Polymarket `oneDayPriceChange` 量纲 → 已核实正确
**状态**: ✅ 已解决（2026-06-29 经官方 Gamma 文档核实）
**优先级**: 🟢（曾评 🟡，核实后无风险）
**触发场景**: `index.py` 动量分 = `min(|change_24h| / momentum_ref(0.10), 1.0)`。`sources/polymarket.py:49` 直取 `oneDayPriceChange`。
**结论**: Polymarket Gamma `oneDayPriceChange` 是**小数/价格点**（官方文档示例 `-0.02` = 价格在 0–1 标度上动 0.02，即 2 个百分点），**不是百分数**。故 `|0.02|/0.10` 量纲正确，**不需要 /100**。Kalshi 侧 `last−prev`（`*_dollars` 价差）同为 [0,1] 概率点，两源同标度，`momentum_ref=0.10` 自洽。曾担心的「百分数 3.0 饱和到 100」不成立。
**来源**: Polymarket Documentation — Gamma Markets API（docs.polymarket.com）。

## [GOTCHA-20260629-002] 一批修复改了未提交，悬在 initial commit 之后
**状态**: ⏳ 待解决（需 Doctor 终端 git）
**优先级**: 🟡 中
**触发场景**: `git status` 显示 `aggregator.py / publish.py / GOTCHAS.md / requirements.txt / test_publish.py` 已改 + `tests/test_aggregator.py` 新增，全未 commit（initial commit = `beffe24`）。
**风险**: 一旦 checkout/clone 丢这些修复。
**解决**: Doctor 终端 `git add -A && git commit`（CC 不在沙箱跑 git 写命令）。

## [GOTCHA-20260629-003] 百分位校准用全量历史、无滚动窗口
**状态**: ✅ 已解决（2026-06-29）
**优先级**: 🟡 中（长期才显现）
**触发场景**: `store.percentile` 读 metric 全表算排名。
**风险**: 长期运行 regime 漂移——拿当下读数和远期分布比，「比过去 73% 热」失真。
**解决**: `store.percentile`/`_history_values` 加 `window_days`；`config.calibration_window_days`（env `GP_CALIB_WINDOW_DAYS`，默认 90，0=全量）；`aggregator._calibrator` 传入。功能验证：200 天前老点被正确排除。

## [NOTE-20260629-004] 沙箱白名单不含预测市场域名
**状态**: ✅ 已知边界
**优先级**: 🟢 低
**说明**: 本会话沙箱 `gamma-api.polymarket.com` / `api.elections.kalshi.com` 直连与走 3128 均返回 000（不在白名单）。真实数据冒烟与量纲核实只能本机做，或 Doctor 临时加白名单后在沙箱做。

## [RESOLVED-20260607] .venv 38M 入树 + 无 git 仓
**状态**: ✅ 已解决（2026-06-29 复核）
**说明**: 6-07 审计两条问题——38M macOS `.venv` 物理在树内、项目无 git 仓——复核时均已解决：`.venv` 已移出、`.gitignore` 覆盖、项目已纳入 git（`beffe24`）。

## [DOC-20260629-005] 文档测试数三处不一致
**状态**: ✅ 已解决（2026-06-29）
**优先级**: 🟢 低
**说明**: 实跑 = **28**（新增 test_aggregator.py）。PRD/STATUS/INDEX 已统一改 28，INDEX 测试文件列表补 aggregator。

## [CODE-20260629-006] `_calibrator` 死分支删除
**状态**: ✅ 已解决（2026-06-29）
**优先级**: 🟢 低
**说明**: `aggregator._calibrator` 的 `mod:{metric}` 不可达分支删除（index.py 只校准 global，模块温度入库不校准）。
