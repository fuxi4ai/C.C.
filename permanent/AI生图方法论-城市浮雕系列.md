---
title: AI 生图方法论 · 城市浮雕图谱系列
tags: [permanent, methodology, ai-image, image-generation]
created: 2026-05-15
updated: 2026-05-15
status: active
type: permanent
---

# AI 生图方法论 · 城市浮雕图谱系列

> 跨项目可复用知识资产 · 指针文件
> 完整版（10 章 · 15 KB）：[[O MY HTML/architecture/方法论]] · 项目内拷贝 `Projects/O MY HTML/METHODOLOGY.md`

## 适用项目

任何"AI 文生图 + 后期 + 系列化"的城市/地标主题。源：长沙·秋 / 杭州·雪。

## 一句话核心

- **prompt 1500 字节** + 三段构图 + palette accent budget + 删 Negative 段
- **API**：curl subprocess（不用 requests）+ 4xx 也 retry
- **safety 矩阵**：`low+1024×1024` / `low+1024×1792` 是 APIYI 仅有的稳路；medium/high 多数被拦
- **抽卡**：N=5 卡间 ≥ 30s · 5 维评分（风格凝聚力 > 细节精度）
- **调色**：image-2 edit subtle 档（用 "very mild" 不要 "deeper"）· 显式 PRESERVE 保护区
- **后期**：所有文字一律矢量上字，AI 写字必错

## 已知触发词速查

`twin towers` / `lone figure facing` / `no other people` / `muted crimson` / `Christmas red-green` → 全部规避

## 关键失败模式

- `Empty reply` / `HTTP 502` → retry，节点波动
- `HTTP 400 + shell_api_error` → APIYI 节流伪装，60s 后 retry 一次能通；第 2 次仍 400 才是真错
- 出图风格散 → prompt 太长，压到 ≤ 1500 字节

## 关联

- [[O MY HTML/architecture/系统概览]]
- [[O MY HTML/architecture/方法论]]（完整版）
- [[apiyi-transit-mode]]
- [[政治经济学/GOTCHAS]] —— 用 G-04 / G-12 评估方法论是否过拟合
