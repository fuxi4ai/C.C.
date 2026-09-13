---
name: audit
description: 用固定只读探针审查代码、配置、JSON 和班次日志，自动派发、同 ID 回读并据发现继续追查。适用于 /audit、审计、核查与复验；不授予业务项目修改或生产执行权限。
---

# 审计 Harness（/audit）使用指南

> 本文件为可移植真源（brain/.skills/audit/）。Cowork 注册表副本经 save_skill 发布；修改真源后须按实际消费端回读确认同步。

固定只读审计工具链的入口技能。日常保持极轻：**写一个目标文件 → 自动执行 → 同 ID 回读**，无需人工跑原生命令。

## 适用

审计/核查类任务：文件与软链身份、JSON 字段差异、完整函数提取（含默认返回）、有界文本、SQLite 固定检查、报告勘误传播、教训召回。时间口径与业务规则由 CC 结合原文判断，不能把不存在的专用探针当成可调用操作。

先确定本次要回答的业务问题与范围，再选最少的相关证据。读到异常就追查入口、转换或消费者，提出可验证的最小修法。没有新疑点便收尾；不固定跑全套，不把回执成功当成业务正确。

## 使用三步

### 1. 写目标文件

路径：`~/Documents/AI4ME/Financial-Audit-outputs/harness-drop/inbox/{ts}_target.json`

```json
{"question": "一句话任务描述", "project": "CC Audit Harness", "targets": ["demo:sample.json"], "deadline_minutes": 2}
```

只写目标与所需 options，不手填 hash、请求 ID、schema。新观察由 CC 自动在 question 加本次 UTC 时间；相同内容会复用旧结果，仅改文件名不会触发新取证。deadline_minutes 必须在 (0,2]。

### 2. 等自动执行

launchd 监视 inbox，自动触发原生 CLI。**既往实测约数秒至 20 秒，非硬保证**；未见 dispatch 回执时继续查状态，**避免重复投递**。执行后 dispatch 目录出现 `{名}_{hash}_dispatch.json`，内含 request_id。

普通回执与 `_dispatch-error.json` 都查，按 target_file/target_digest 匹配本次目标。等待不无限循环：至本次 deadline 仍无回执且无 request_id，报告派发状态未核并保留原目标；有 ID 则只读查原请求。indeterminate 保持原状态，不能改写为成功或盲目重发。

### 3. 同 ID 回读

```bash
cat ~/Documents/Codex/Infrastructure/loop-engineering/runs/audit-harness/{request_id}/result.json
```

按 dispatch 件里的 request_id 回读。未完成时查同 ID status，不重复投递；已得到错误证据且改了假设/输入的后续调查可以发新目标。逐项读取 status 和 error.code；partial 中完成项继续使用。`lesson_retrievals` 有召回命中时才出现（最多 3 条，候选仅供参考）。

`python_symbol` 取完整函数；`text` 默认 200 行、最多 1000 行，truncated=true 时按 next_line 续读相关部分，不能声称已读全文。回执绑定当次快照；后来源文件变化时用原 inputs 对拍，不把旧回执冒充当前数据。

收尾时由 CC 自动记一次轻量反馈，无需 Doctor 填表：在本次 run 写 `task-feedback.json`，保留原 result/run-report/dispatch。七字段为 `request_id`、`result_sha256`（从 result.json 原字节计算）、`question`、`resolution`（answered/partial/blocked/unknown）、`blocked_at`（none/scope/data/execution/reasoning/external/unknown）、`human_handoff`（not_needed/needed/unknown）、`note`（一条证据或缺口）。按问题实际是否得到回答填写，不能用 completed 推导 answered。还可自行追查时不判需要人工接力。

原生 `status ID` 会校验并附上 `task_feedback`；Gateway 直接写后回读同文件核 ID/hash/七字段即可，程序校验结果未回读就不代称通过。反馈是 CC 自述，未写=unknown，格式坏不阻塞已取得证据；不据此升级 GOTCHAS、改派发状态或重新执行。原生端亦有 `feedback ID --question ... --resolution ... --note ...` 简便入口。

## 可用操作

- `inspect_resource`：默认；kind 为 file/json/json_field_diff/python_symbol/text/sqlite，并受每个注册根的操作白名单限制。
- `verify_consumer_output`：报告与 findings 同源对拍、回读自产产物。
- `run_fixture_repro`：仅四个冻结适配器 `longyu-facts-replay`（龙鱼事实函数）、`guanxing-threshold-replay`（观星阈值 helper）、`baize-merge-replay`（白泽两行合并）、`ipo-funds-replay`（IPO 完整采集函数＋合成 API/内存库）。**必须显式写 `operation_id`，省略返回 `target_invalid`**；未支持的适配器同样返回 `target_invalid`，后端不可用是另一种情况。完整示例：

```json
{"question":"重放龙鱼事实函数","project":"CC Audit Harness","targets":[],"deadline_minutes":2,"operation_id":"run_fixture_repro","options":{"replay_adapter":"longyu-facts-replay"}}
```

## 边界与升级

- 已开放以下真实只读面，精确路径以宿主 `Codex/Infrastructure/loop-engineering/config/audit-resources.v1.json` 为准：

| root | 可读相对路径 |
|---|---|
| zhuzhao-ipo | fetch_ipo.py |
| baize-prices | scripts/data_collection/fetch_futures_prices.py；data/commodity_prices_live.json；src/core/data_source.py；data/stocks_fundamentals.json；scripts/analysis/run_full_analysis_v4_1.py；scripts/reports/build_weekly_report.py；data/weekly/boards/board_latest.json |
| longyu-source | write_claude_score.py；score_subitems.py |
| guanxing-cn | engine_cn.py；configs/models/china_macro_v3.yaml |
| eal-logs | 根目录 shift-log-*.md；不递归 |
| baize-output | 白泽周报看板_最新.html |
| zhuzhao-f4 | tools/gen_daily_report.py；tools/risk_function.py；config/risk_factors.json |
| risk-daily | build_risk_daily.py；data/risk_snapshot.json；dashboard/risk-daily.html |
| zhuzhao-output | 根目录烛照九阴日报_八位数字.html；不递归 |

例如 `targets:["zhuzhao-ipo:fetch_ipo.py"]`，`options:{"kind":"python_symbol","symbol":"fetch"}`；日志/YAML 用 text。EAL 新日志与标准日期命名的烛照日报可在授权根内发现，无需逐日登记。白泽链按期货入口→data_source/分析→周报 builder→快照/HTML；IPO 链按 fetch_ipo→F4 或风险日报 builder→相应产物追查。选相关段，不每次读完整链。找不到资源先核现行路径；需要越界时报告所缺资源，不自行扩权。生产库、凭据、records 与 sealed 未开放。

- 四个冻结适配器与 demo 可用。`completed` 只表示冻结行为对拍成立，可能正复现历史缺陷；不证明当前生产已修。真实链只读材料，未执行 builder/活跃库/浏览器；生成时间与源码版本分开核对。
- 学习：运行失败/修复自动捕获候选并同根去重。**业务错误可能伴随 completed 回执**：CC 须将实证发现写入单一 findings，查项目 canonical GOTCHAS 后同根追记或登记 🔄；未核根因保留 unknown。已有规则按相关项目定向召回，不全量灌入。
- 自迭代以实际失败为起点：确定性修法获授权后加入最小回归，行为教训留一句可检索规则。测试进入既有开发回归，不进每日前置清单；✅、通用升格和候选 commit 不自动做。
- 报告从同一 findings 生成；勘误同步结论、正文与行动建议。建议说明触发、影响、最小修法与验法，未知影响不写成事实。verify 只核序列化/文本同源，不代表浏览器显示或业务推断正确。
- **被审资源只读；运行记录、回执和候选区按约定写入**。金丝雀与故障注入不进每次运行。
- 安全可逆的工具自身故障先诊断、修复、重试；同方案连续失败应换假设。只有缺授权/关键输入、真正价值取舍或已无安全取证路径才请 Doctor 裁定。业务代码/数据修改须有授权，不因“审计”自动获得修复权限。
