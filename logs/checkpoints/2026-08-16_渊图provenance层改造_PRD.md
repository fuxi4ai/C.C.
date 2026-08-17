---
title: PRD 2026-08-16 渊图 provenance 层改造
tags: [prd, 渊图, provenance]
created: 2026-08-16
updated: 2026-08-16
status: 草案待批
type: prd
project: 渊图
---

# PRD · 渊图 provenance 层改造（source_span / enrichment_source）

## 一、目标

让图谱每个节点/边可计算地追溯到「源文哪个片段」，外部知识补充与源文提取严格分层。VV 盲审的总问「ASR、DeepSeek 提取层与最终事实节点之间，为何缺少可计算的 provenance 边」即本 PRD 要回答的问题。

## 二、背景

2026-08-16 Boss老白 131 篇转录入库后，我方普查（断言层 61% 准确）+ VV 盲审（忠实层 25%）联合暴露：多数错误穿透入库门，根因是**提取产物没有精确到片段的 provenance**——外部知识注入（enrichment）与源文提取混层、无法机械校验「这条断言源文里到底有没有」。

## 三、交付标准（可验证）

1. **source_span 强制**：kg_ingest 提取 prompt 要求每个节点/边携带 `source_span`（源文中的原文摘录，50-200 字，或明确 `"span": "全文概括"` 时标注）；后处理校验：`source_span` 文本必须能在源文中找到（允许 ASR 归一化后的模糊匹配）。
2. **enrichment_source 分层**：LLM 提取时若使用了外部知识（源文中无），必须显式标 `enrichment_source: "model_knowledge"` 或具体来源；无标注的节点视为「源文提取」，QA 抽查 span 不存在即告警。
3. **门**：kg_promote 新增第 12 项断言——本批新节点 `source_span` 缺失率 ≤ 5%（存量节点豁免，回填另批）。
4. **回填**：Boss老白批 972 个新节点已有 provenance 字段（file 级），span 级回填分主题批进行（另立排期，不在本 PRD 范围）。

## 四、验收方式（VV 最终验收门 · 2026-08-16 VV 结项回执定义，取代初稿口径）

管线改造完成后：**从原始转录重新生成 24 个样本**（不复用本轮任何定向补丁），逐一检查五维：

1. `source_span` 存在且能在源文中定位
2. `enrichment_source` 与源文提取严格分层（无标注的源外内容=失败）
3. 关系方向与谓词正确（part_of/used_in/evolves_from/measured_by/constrains/is_a/competes_with 主客体与类型）
4. 实体归一（ASR 错名不得实体化）
5. 时间键一致（ID 年份/季度 vs description vs source）

**重跑 24 样本全绿 = 系统性闭环**；任一维度复现本轮错误类型 = 验收失败、回炉管线。

## 五、变更记录

| 日期 | 变更 | 状态 |
|---|---|---|
| 2026-08-16 | 草案（CC 起 · 待 Doctor 审） | 待批 |
| 2026-08-16 | §四 验收方式按 VV 结项回执升级为「重跑 24 样本五维验收门」 | 待批 |
| 2026-08-16 | Doctor 裁定：不搞第三次审计，直接推本 PRD（重跑验收天然覆盖全样本） | 待批 |
| 2026-08-16 | **Doctor 批准开工**（AskUserQuestion 全票推荐项） | ✅ 已批 |
| 2026-08-17 | 交付：kg_ingest 五处改造 + kg_promote 第 12 项 + 24 样本重跑五维验收通过（错误复发 0 例）· 验收报告 raw/核实/2026-08-16-Boss老白24样本重跑验收报告.md | ✅ 已交付 |
