---
title: 2026-09-11 龙鱼看板 equity-thesis 接入 PRD
tags: [prd, 龙鱼五力, equity-thesis, 看板, 周更]
created: 2026-09-11
updated: 2026-09-11
status: 进行中
type: prd
task_authorization: "Doctor 2026-09-11 指令「进化Artifact龙鱼看板，将equity-thesis接入标的的周更，并整合在二级详情页展示分析结果」+ 方向三问全批推荐（范围=持仓 / 形态=独立班错峰 / 详情页=侧栏扩展）"
---

# 龙鱼看板 equity-thesis 接入 PRD

## §一 背景与范围

- 源：Doctor 2026-09-11 指令；equity-thesis 技能（VV 交接 bf21616）本日已装并验收。
- 范围：① 看板二级详情（侧栏）新增「定性研究」区；② 独立周更班自动产出持仓标的的定性研究；③ 生成器把研究数据并入 PAYLOAD（不改评分库、不动版式真源纪律）。
- 明确不做：不改 records 评分库、不重打分、不交易、不改持仓表；equity-thesis 只写自己的新数据目录。

## §二 验收主体（功能/需求）

1. **侧栏展示**：点开任意持仓标的卡片，侧栏在「一句话判断」之后出现「个股定性研究」区——首选动作（带类型色标）+ 价格条件/失效触发 + 下一观察点 + 七段可展开 + 三问折叠 + 研究截至日期。无数据标的显示占位行（不空白）。
2. **周更产出**：独立班 `longyu-equity-thesis-weekly`（周六 14:00 PT，错峰于 22:00 双 scorer 周更班）对 holdings.json 全部持仓（当前 12 只）逐个跑 equity-thesis 流程（真实联网搜索+龙鱼只读对照），结果落 `Database/龙鱼-标的分析库/equity-thesis/{ts_code}.json`（entries 追加，同日覆盖）。
3. **看板数据链路**：`build_dark_board.py` 读 equity-thesis/ 最新条目挂进 PAYLOAD 每条 record 的 `research` 字段；模板从模板+数据派生，单行替换纪律不变；周更班重建时自然带出（无需改周更班 prompt）。
4. **首次填充**：本场手动跑全部持仓 12 只，重建+update_artifact 推送，消费端回读验证。
5. **自发现迭代轨道（2026-09-11 Doctor 批「补，同意」）**：schema 增 `triggers`（上一份 watch/cond/risks 改判条件→本轮逐项判定 触发/未触发/证据不足/不再适用）与 `evolution`（方法候选状态机 candidate→tested→independently_verified→outcome_observed；本班只许 candidate↔tested，verified/outcome 归 Doctor 或未参与实施的独立复验）；班 prompt 增第零步回访；侧栏增触发器回访徽章+候选状态计数。

## §2.5 执行清单（过程项）

- [~] 数据目录与 schema：`equity-thesis/{ts_code}.json`（ts_code/name/entries[]·每条含 as_of+七段+三问+skill 版本）——12 只全部落盘、JSON 校验 12/12 OK（实跑）
- [~] 生成器：build_payload 增读 equity-thesis/，record 增 `research` 字段（无则 null）——重建后 120 records 中 11 只带 research（实跑）
- [~] 模板：openCard 侧栏增「个股定性研究」区（内联样式·复用现有 tokens）——node --check 语法过 + DOM 文本断言过
- [~] 独立班：create_scheduled_task `longyu-equity-thesis-weekly`（周六 14:00 PT · 错峰于 22:00 周更班）已建 · next run 2026-09-12
- [~] 首次填充：12 只 subagent 并行研究（真实联网+龙鱼只读对照）· 落 JSON 12/12
- [~] 重建+推送+消费端回读：update_artifact 已推 · updatedAt 2026-09-11T09:18:53Z（list_artifacts 实读）· 本地 standalone 断言过 · Gateway 实际文件 payload 比对沙箱不可达（历史已知约束）
- [~] 演化轨道：schema triggers/evolution + 班 prompt 第零步 + 侧栏回访徽章（Doctor 批「补，同意」）——模板 JS 语法过 · 班 prompt 已更新（下次运行生效）· 看板重建待下次推送
- [ ] 独立验收（归 Doctor / Doctor 指定方；实施者不自签）——含视觉目验侧栏新功能区

## §三 关键设计约定

- 数据身份：文件名=ts_code（HK 保留前导零，如 02476.HK）；entries 按 as_of 追加、同日覆盖；每条目带 `skill_version` 溯源。
- 只读合同：研究过程读龙鱼 records（read_longyu.py）、风险卡、EAL 只读；写仅限 equity-thesis/ 目录。
- 隐私边界：子代理只被告知「该标的在持仓清单内」，不给股数/成本/状态（skill 原文「不臆测 Doctor 持仓」）；报告不写持仓比例。
- 港股（胜宏 02476.HK）：无 A 股引擎数据，龙鱼对照标 unavailable，其余流程照常。
- 版式真源纪律：模板改动=新功能区（属本轮授权），数据注入仍走单行 PAYLOAD 替换；改完跑一遍生成器验命中行数=1。

## §四 变更记录

- 2026-09-11 立卷（CC）· 方向三问 Doctor 批：持仓 12 只 / 独立班错峰 / 侧栏扩展
- 2026-09-11 实施完成（CC）：数据层 12/12 · 生成器+模板改造 · 班已建（next run 09-12）· 看板已推（updatedAt 09-11T09:18:53Z）· 独立验收待 Doctor
- 2026-09-11 演化轨道补装（Doctor 批「补，同意」）：triggers/evolution schema + 班 prompt 第零步 + 侧栏回访徽章；生效自下次班跑（当前 fireAt 一次性实跑用旧 prompt，其产出无新字段属预期，模板已兼容）
