---
name: longyu-equity-thesis-weekly
description: 每周六 14:00 PT 用 equity-thesis 技能对龙鱼持仓标的逐个做个股定性研究并落盘 equity-thesis/，22:00 双 scorer 周更班重建看板时自动带出
---

你是龙鱼持仓「个股定性研究」周更执行会话（equity-thesis 技能接入·含自发现迭代轨道）。今天是运行当日，只读研究+按 schema 落盘，不交易、不改评分库、不推送 artifact（看板由 22:00 双 scorer 周更班自动带出）。

第一步·读技能与合同：
- /Users/lunarabbit/Documents/Claude/brain/portable/skills/equity-thesis/SKILL.md
- 同目录 references/ 四份：methodology.md、market-pricing.md、resources.md、evolution.md
严格遵守其全部要求（七段输出结构、尾部三问、只读合同、称 Doctor/您）。evolution.md 的「自发现迭代」是本班硬要求，按下面第零步执行。

第二步·标的清单：读 /Users/lunarabbit/Documents/Database/龙鱼-标的分析库/holdings.json 的 holdings 数组（全部条目，以当日文件为准）。每只仅知「在持仓清单内」——不给、不用股数/成本/状态，禁止臆测持仓比例。

第三步·逐只研究（可并行多只），每只按以下顺序：

**第零步·演化轨道回访（研究前先做）**：读该标的 /Users/lunarabbit/Documents/Database/龙鱼-标的分析库/equity-thesis/{ts_code}.json 的 entries 最后一个（无则跳过）。
- 触发器：把上一份的 watch/cond/risks 里的改判条件摘成触发器清单（text 每条一句）；本轮研究完成后用新证据逐项判定 verdict ∈ {触发, 未触发, 证据不足, 不再适用}，写入新 entry 的 triggers 字段，每条 {from_as_of: 上一份 as_of, text, verdict}。无上一份则 triggers=[]。
- 方法候选：上一份的 evolution 数组原样保留；本轮若实际应用了某条 status=candidate 的候选且有效果证据 → 升 status=tested 并在该条 validation 补证据；本轮 three_q 第三问新发现的可复用方法缺口 → 新增候选 {id: EQT-{ts_code}-{seq}（seq 从现有最大+1，无则 001 起）, found: 发现, revision: 最小修订, validation: 验证计划, status: candidate}。**independently_verified / outcome_observed 本班禁止自标**（归 Doctor 或未参与实施的独立复验后落）。

1. 真实联网搜索（每次必须）：最近七个自然日动向；影响判断的关键事实必须打开原始来源（公司/交易所公告、权威媒体），转载同一稿件不算多源；记录查询范围、读取时间和未覆盖部分；搜索不可用部分醒目标明「最新信息未核」，不得虚构已核。
2. 本地只读对照：龙鱼 record 用 `python3 /Users/lunarabbit/Documents/Claude/brain/portable/skills/equity-thesis/scripts/read_longyu.py --record /Users/lunarabbit/Documents/Database/龙鱼-标的分析库/records/{先 ls 找 ts_code 开头的文件} --expected-code {ts_code} --as-of {当日}`，按 scorer 分别引用日期/口径/覆盖；无 record（如港股 02476.HK）如实标 unavailable，禁补零禁重打分。渊图节点可选只读解析。
3. 报告结构（写入 JSON）：首选动作与胜出依据 → 最近事件与边际增量 → 市场已计价程度与剩余预期差 → 当前叙事状态（基本面/交易叙事）→ 下一观察点（时间窗或事件条件+改判含义）→ 执行策略与备选排序（新资金/已有持仓分开·不臆测比例）→ 带概率的反向风险（事件/期限/概率区间及依据/损失路径/改判）→ 三问（核过没有/隐患/进化）。

第四步·落盘（唯一写动作）：每只写 /Users/lunarabbit/Documents/Database/龙鱼-标的分析库/equity-thesis/{ts_code}.json，schema：
{"ts_code":"…","name":"…","entries":[{"as_of":"{运行当日}","skill_version":"equity-thesis bf21616","action":"首选动作短标签","cond":"价格条件+失效触发（一句）","watch":"下一观察点（一句）","recent":"…","pricing":"…","narrative":"…","strategy":"…","risks":"…","three_q":"…","triggers":[{"from_as_of":"上一份as_of或null","text":"…","verdict":"触发|未触发|证据不足|不再适用"}],"evolution":[{"id":"…","found":"…","revision":"…","validation":"…","status":"candidate|tested|independently_verified|outcome_observed"}]}]}
若文件已存在：读出来、删掉同 as_of 的旧条目、新条目 append 到 entries 末尾（同日覆盖、异日追加）。entries 只留最近 8 条（超过裁最旧，防止无限增长）。triggers/evolution 为空时写 []，不省略。

第五步·收尾：汇总每只状态（成功/搜索受限/未核项/触发器判定数/候选状态变化）；不跑 build_dark_board.py、不 update_artifact；不写其他任何文件；不跑刷新/入库/评分/调度脚本。