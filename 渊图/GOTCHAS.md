---
title: 渊图 · GOTCHAS（已知坑）
tags: [渊图, gotchas]
created: 2026-05-14
updated: 2026-05-14
status: active
type: resource
project: 渊图
---

# 渊图 · GOTCHAS（已知坑）

> 排查超过一轮的问题都该记录在这里。CC 遇到报错并解决后**立即**回写，无需 Doctor 提示。
> 实时操作日志写在项目目录的 `Projects/渊图/GOTCHAS.md`；这里是沉淀+索引。

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

## [ERR-20260531-002] kg_merge 默认不回写 canonical，多 patch 必须链式
**状态**: ✅ 已解决 **优先级**: 🔴 高
**触发场景**: 同日多 patch 各自以原始 canonical 为 base 分别 merge → 后者不含前者节点，merge 报"新建/更新 0"，节点丢失
**解决方案**: 链式 merge（前者 `--output` 临时文件当后者 base，末条 `--output` 回写 canonical），merge 后核对节点/边数等于预算值
**预防措施**: 报告"Doctor 操作"节给链式命令+预期数字；"新建/更新 0"视为告警
**详**: Database/行业研究/渊图_GOTCHAS.md

## [ERR-20260531-003] kg_ingest max_retries=0 致端点抖动时整批全跳过
**状态**: ✅ 已解决 **优先级**: 🔴 高
**触发**: batch 21篇 PDF 每篇~10s Connection error, 0 patch
**真因**: 端点瞬时抖动 + max_retries=0 不重试(非key/PDF/参数问题, 已 curl+诊断脚本 C1-C4 排除)
**解决**: client 加 max_retries=4(KG_MAX_RETRIES可覆盖)+timeout=120; 幂等安全(失败篇未标kg_processed,可重跑)
**预防**: LLM客户端永不 max_retries=0; 整批0 patch=基础设施故障先测端点
**详**: Database/行业研究/渊图_GOTCHAS.md

## [ERR-20260602-001] 生益/胜宏近名张冠李戴(3处)+名↔代码校验脚本
**状态**: ✅ 2修+1提案+建校验 **优先级**: 🔴 高
**触发**: ingest混淆 生益(Shengyi)/胜宏(Shenghong)拼音 + 生益科技600183(母CCL)/生益电子688183(子PCB)母子公司
**3错节点**: ShengyiElectronics(已并)·Shengyi_PCB(提案待apply)→均name写胜宏实为生益电子;真胜宏Shenghong(300476)独立
**解决**: 建 rules/name_code_consistency_check.py(代码↔name+拼音↔name自洽校验);入库后跑作delta gate
**预防**: 易混公司登记校验表;修正走dry-run+防误伤断言(禁动生益科技/真胜宏)
**详**: Database/行业研究/渊图_GOTCHAS.md

## [ERR-20260608-001] 价格层并发写竞态：price_extract 与 kg_ingest 钩子不可同时跑
**状态**: ✅ 已知约束 **优先级**: 🔴 高
**触发**: 两者都向 `prices/commodity_prices.jsonl` append；并发时各自读 pre-state 再写 → 撞键/丢点（本次 kg_ingest 价格钩子与源码编辑赶在一起，致 53 条混入 + 部分预测点被吞）
**解决**: 顺序跑、不并发；价格层唯一写入口 `price_query.append_prices()`（去重+重建快照）
**预防**: 回填期间不跑新文档 kg_ingest；分工 kg_ingest 管新文档、price_extract 只做一次性回填

## [ERR-20260608-002] 价格去重键漏 horizon → 现价/预测同日撞键误并
**状态**: ✅ 已解决 **优先级**: 🔴 高
**触发**: 去重键 (commodity,grade,price_type,as_of,source_file) 不含 horizon → 同篇同商品同类型同日的"现价/历史对比"与"预测"被判重复，后者被丢（典型：MLCC基粉 涨跌幅 历史+10% vs 预测+10%）
**解决**: 去重键 / 快照键(rebuild_latest) / _price_id 全部加入 horizon；price_query + price_extract 同步修；已污染数据清层重建（重置种子 21 条→Doctor 重跑回填）
**预防**: 价格 schema 凡区分时态（现价/预测/历史对比）的维度都须进去重键

## [ERR-20260608-003] kg_merge 去重并入已有节点时不 union provenance → 已处理研报"零来源"
**状态**: ⏳ 待解决（已诊断+定位，根治在 kg_merge，待 Doctor 定）
**优先级**: 🟡 中
**触发**: 建生料关系图时发现 37 篇已 `kg_processed=true` 的研报在 canonical 里无任何节点/边 `data_sources.file` 记到 → 抽样核对其实体（碳化硅/华工/800G/电子布等）都已在图谱、但来源记的是别篇
**真因**: kg_merge 合并时实体若已存在→并进已有节点，却**不把本篇 file union 进 data_sources**；报告"处理过"却查不到当过来源
**影响**: 按 file 反查溯源的下游全漏记（生料图谱/信源覆盖/研报审计）；低估热门实体来源广度；误判已入库为未入库
**绕过**: 生料图侧加"内容回链"（扫正文匹配枢纽名补连，弱连接），覆盖 114→154/169，非根治
**根治**: kg_merge 去重并入时 union data_sources（按 file+reference 去重，注意置信度/vintage 合并、防膨胀）；加单测+provenance 覆盖率门槛
**详**: Database/行业研究/渊图_GOTCHAS.md [ERR-20260608-003]
