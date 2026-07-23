---
title: 会话日志 2026-07-23 — AI Tech Alarm Scoring 改名与台积电Capex注意事项
tags: [log, 渊图, Cowork-artifact]
created: 2026-07-23
updated: 2026-07-23
status: active
type: log
project: 渊图（Cowork artifact 侧）
---

# 会话日志 — 2026-07-23

**项目**：渊图警报 / Cowork artifact `ai-tech-alarm-scoring`
**主题**：AI Tech Alarm Scoring 改名 + 台积电 Capex 常驻注意事项

---

## 完成的工作

- 定位资产：「Ai Tech Alarm Scoring」= Cowork artifact（id `ai-tech-alarm-scoring`），源文件 `~/Claude's workspace/Artifacts/ai-tech-alarm-scoring/index.html`；Documents 里另有一份无 meta 的导出副本 `AI科技股-警报时点-杀伤力评分.html`（未动）。
- 加常驻注意事项：header 新增琥珀色 pin 条「台积电 Capex 指引=上游先行信号，早于 Mag7 财报；上修＝下游 AI capex 加码坐实，下修/不及预期＝需求见顶预警；用作 5 时点未定价度交叉验证锚，不单独计分」。经 `update_artifact` 生效，meta 描述也同步补入。
- 改名 Ai→AI：工具层无 rename 接口，最终由 Doctor 在终端用 python3 改 Application Support 内部 `artifacts.json` 的 name 字段（带备份），打印 `updated 1 entry(ies)`，退出应用重开后侧栏显示「AI Tech Alarm Scoring」。

## 做出的决策

| 决策 | 原因 | 影响 |
|------|------|------|
| 注意事项只落 artifact，不进 watchlist/不做第 6 时点 | Doctor 选推荐项；台积电 Capex 是先行信号非崩盘时点，性质与现有 5 条不同 | 可逆、不碰 Database/行业研究，无 git 落盘负担 |
| 改名走 Doctor 终端手改 manifest（带备份） | Cowork artifact 无 rename 接口，唯一落点是应用内部 artifacts.json | 达成改名且可回退；碰应用内部状态，重开生效 |

## 遗留问题 / 待办

- [ ] Doctor 重开 Claude 桌面应用后确认侧栏名已变为「AI Tech Alarm Scoring」；若被应用回写覆盖则需另想办法。
- [ ] 若日后要台积电 Capex 主动周度核验，再考虑登记进 `alarm_watchlist.jsonl`（本次未做）。

## 相关笔记

- [[渊图]]
- [[yuantu-alarm-weekly]]
