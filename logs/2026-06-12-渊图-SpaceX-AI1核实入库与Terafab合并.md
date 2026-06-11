---
title: 会话日志 2026-06-12 — 渊图-SpaceX AI1核实入库与Terafab合并
tags: [log, 渊图]
created: 2026-06-12
updated: 2026-06-12
status: active
type: log
project: 渊图
---

# 会话日志 — 2026-06-12

**项目**：渊图
**主题**：SpaceX AI1 算力卫星新闻核实 → raw 札记 → 单篇入库单核 → Terafab 近重复对合并

## 完成的工作

- 核实 2026-06-08 SpaceX AI1 演讲（Musk + Ian Dahl，X 视频，IPO 前三天）：150 kW 峰值/120 kW 持续、110 m² 双面液冷辐射板（1,400 W/m²）、光伏 250 W/m²（~600 m²）、70 kW/吨、600 km 晨昏 SSO、两颗原型星 2027 年初、Gigasat 2027 年底量产
- CC 独立工程核算：参数自洽 ✓、光伏保守合理 ✓、散热在物理极限边缘（需板面 75–80°C、≈ISS 面密度 8 倍、未在轨验证）⚠️、70 kW/吨大概率虚高 1.5–2.5×（自底向上 3.5–5 吨）❌
- 成本核：SemiAnalysis TCO 口径太空 ~$8.7 vs 地面 ~$2.4/hr/GPU（机房资本 17×，主因 5 年 vs 15 年寿命）；基准 2040 年打平，"Musk 情形"（地面电力卡死）30 年代初近打平，机制是稀缺溢价非纯成本；其质量假设 ~30 kW/吨已比 Musk 保守，"2040 打平"已计入重量虚高
- 落 raw 札记 → 移入 MD 通道（`2026.06.12-内部研究：…`，命中 _DOCTOR_KEYWORDS → 内部学习材料 P1）→ Doctor 终端跑 ingest → CC 单核：修 AIO1→AI1 id（节点+9 边 id）、is_a 方向反转改 used_in、properties 加 self_reported/CC核算 区分注；清价格层 2 条 value=None 垃圾点 + rebuild_latest；8 项结构校验全 0 → 替换 canonical **2279/2777 → 2287/2786** → wiki +1（spacexai1satellite，9 度）
- Terafab 近重复对合并：`concept_TeslaTerafabProject`(兴业4-19) + `concept_IntelTerafabJV`(Barron's 4-17/内部研究6-12) → `concept_TerafabAIChipFab`（中性名，3 信源、8 aliases、merge_note 留痕），3 边重指 → **2286/2786**；防误伤断言+悬挂/重复边/名↔代码校验全过；快照 backups/*_pre_terafab_merge
- GOTCHAS 回写 2 条：ERR-20260612-001（kg_merge_safe 格式闸拒收 ingest 全图产出；实证 ingest 产出合入语义=校验后替换）、ERR-20260612-002（价格钩子误收 CC 估算值）

## 做出的决策

| 决策 | 原因 | 影响 |
|------|------|------|
| CC 札记定级走"内部研究"→内部学习材料 P1 | _DOCTOR_KEYWORDS 为 Doctor 自有材料设计的通道，名正言顺；Musk 自报参数在节点 properties 内单独标 self_reported（华为先例） | 后续 CC 核实类札记沿用此命名 |
| ingest 全图产出不走 kg_merge_safe，走校验+替换 | safe 格式闸只认手工 patch 四键；6-11 合入文件即全图（2279/2777=canonical），替换才是历来实际语义 | 双轨写入 GOTCHAS，根治方案待 Doctor 定 |
| 单篇 9 边人工核替代 kg_rel_classify | 沙箱 45s 跑不动 LLM 分类；9 条边逐条对 11-schema 人工核（修 1 条方向） | 仅限单篇小批量；大批仍走 relclf |
| Terafab 合并新建中性 id 而非保留旧 id | 两旧名各有误导（非纯 Tesla 项目、非 Intel 合资主体） | 旧 id 仅存于 merge_note 文字 |

## 遗留问题 / 待办

- [ ] Doctor 终端跑行业研究仓 git 提交（命令已贴）
- [ ] kg_merge_safe 根治方案：加全图分支 or CLAUDE.md 写明双轨（ERR-20260612-001）
- [ ] 渊图 CLAUDE.md「新研报入库流程」第 5 步与实际语义不符，待更新
- [ ] 沙箱 45s 上限：跨调用后台进程不存活（bwrap --die-with-parent），LLM 类脚本一律贴命令给 Doctor 终端

## 相关笔记

- [[渊图系统概览]]
- raw 札记：`Database/行业研究/raw/Obsidian Industrial/2026.06.12-内部研究：SpaceX算力卫星AI1核实札记.md`
- wiki：`Database/行业研究/wiki/spacexai1satellite.md`
