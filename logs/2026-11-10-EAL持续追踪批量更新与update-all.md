---
title: 会话日志 2026-11-10 — EAL持续追踪批量更新与update-all
tags: [log, 宏观研究体系, EAL]
created: 2026-11-10
updated: 2026-11-10
status: active
type: log
project: 宏观研究体系
---

# 会话日志 — 2026-11-10

**项目**：宏观研究体系 · EAL（兼 update skill）
**主题**：EAL 持续追踪批量更新体系搭建、首轮实跑与 `/update all`
**日期口径**：本机 PST 11-09 至 11-10 晚（北京 11-10 至 11-11）

---

## 完成的工作

- 新建 EAL 持续追踪标准 `EAL/frameworks/持续追踪更新标准.md`：现行案例研究范式、传导逻辑 L1–L12、信息渠道、四类对象（每日台账／量化锚／检验节点／政策快照）的格式、双模型协议、FedWatch 读法。
- 新建 `EAL/backtest/tracking/`：`eal_track.py`（check／list／fetch-ohlc／anchor／policy／dual）、`registry.json`、`test_eal_track.py`（现 34 测试）；update skill 增「批量模式」。
- FedWatch 读数：先判「读不到」，经 Doctor 指出前一日 Fable 会话成功，按 1200×1500 视口＋滚动读法读到；登记 EAL-F001。
- 量化锚 QA-20261103-001：D1–D5 三源对拍（Tushare／东财／新浪），终判 **confirmed**，`anchors.jsonl` 写 review 与终判（备份 `.bak_20261110_183756_track`）。
- 核实行情入库定时班最早可得时点（Tushare daily 约 17:00、index_daily 实测 16:38 可得、limit_list_d 17:08–18:30 之间、margin T+1 约 09:05；定时班 02:30 PST＝北京 18:30）；Doctor 裁「保持不动」。
- 11-09 台账：双模型分歧→裁决；独立审核三轮（macro 应按事件表转写 CPI/PPI、括号注与事件表最终修订相反）后写入。
- `/update eal` 批量实跑：政策快照（12-09 会议加息 25bp 85.1%、50bp 14.9%，回算差 0.76pp 一致）写入；11-10 台账为单模型（DeepSeek 门禁不过），会话采用 Claude 结果补做、订正四处后写入；三个事件节点写入 `node_checks.jsonl`（N-02 未触发、N-03 无新信息、H1H3 已证实且摘要合并两方依据）。
- 修代码缺陷四处并登记 GOTCHAS：EAL-T001（待分类事件被写「无新增」）、T002（按链接去重吞掉同源多主张）、T003（节点一致只比 status，摘要取单方 → 改为另存 `summary_deepseek`）、T004（提示词缺宏观/政策分类边界）。
- `/update all`：按 market data → EAL → research files 预检，只执行未更新到位的项；EAL 加 `dual --all-nodes`（不看到期日、当天已核跳过），到期型节点可登记 `since`。独立复审 PASS_WITH_LIMITS。
- Doctor 已提交：宏观研究体系 d1a1ffd、c65995b、8a8b345、ae61ad4；brain cd89a36、530d33d（均未推送）。

## 做出的决策

| 决策 | 原因 | 影响 |
|------|------|------|
| 批量更新范围＝每日台账＋量化锚＋检验节点＋政策路径；双模型盲跑、分歧裁决；锚判定由脚本算、独立核验后写 | Doctor「按推荐开工」 | eal_track.py 与标准件的骨架 |
| 行情入库定时班保持 02:30 不动，急用时手动跑 | 提前会让 limit_list 缺一天、夏令时漂移、与句芒 01:30 Cowork 班冲突 | launchd 未改 |
| 提示词保留宏观/政策分类边界（policy 只收规则或制度动作） | QCR §0.5 与范式 §8 的 11-06 先例；两模型共用提示词同向错分 | EAL-T004 |
| 节点一致时另存 DeepSeek 摘要，不改一致判定 | 改动小、依据不丢 | EAL-T003，标准 §4.2 补字段 |
| `/update all` 中 research 与 EAL 节点未到期也跑 | Doctor 选「未到期也跑」（不推荐项），换取及时性 | 每次全量跑，成本高；当天已核的跳过 |

## 遗留问题 / 待办

- [ ] 6 个本地提交未推送（宏观研究体系 4 个、brain 2 个），推送归 Doctor。
- [ ] `summary_deepseek` 分支无单元测试覆盖（node_item 是闭包，测不到）。
- [ ] 到期型节点到期前判「已证实」、到期后可能重查成「未触发」，提示词不带历史结果（已知风险）。
- [ ] 门禁按来源名计数，同源通稿（如星岛/凤凰）可能被算成两个独立来源。
- [ ] `/update all` 尚未实跑；节假日误判时编排器写 0 行的表现、18:30 各表可得只有 11-10 一天样本，均未核。
- [ ] FedWatch 会议日期未与 federalreserve.gov FOMC 日历逐一核对。
- [ ] VV 运行回执请求信（`4AI/Shake hands/to VV/CC致VV-EAL全量采集运行回执请求-20261109.md`）待 Doctor 转交。
- [ ] 审核 subagent 两次越出只读约束（删他人测试临时目录、建 shasum 基线文件），`/tmp/claude-501/rv_sha_before.txt` 等残留未删。

## 相关笔记

- [[通用教训]]
- [[经验库]]
- 项目 GOTCHAS：`Projects/Financial/宏观研究体系/EAL/GOTCHAS.md`（EAL-F001、T001–T004）
