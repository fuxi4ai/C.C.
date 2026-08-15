---
title: 会话日志 2026-08-15 — 渊图AnthropicQ2财报追新闻
tags: [log, 渊图]
created: 2026-08-15
updated: 2026-08-15
status: active
type: log
project: 渊图
---

# 会话日志 — 2026-08-15

**项目**：渊图
**主题**：Anthropic Q2 财报追新闻（props 注记批）

## 完成的工作

- 追新闻检索 + 多源核实：Bloomberg 08-15 报 Q2 初步营收 >$11.5B（同比 +14x、环比 Q1 $4.73B）、调整后营业利润首度转正、5 月 run-rate $47B、6-01 秘密提交 S-1（大摩/高盛牵头、目标 10 月 Nasdaq）
- 图谱摸底：live 读盘 4069/4578，Anthropic 子图 27 节点命中，确认今日新闻均不在图、raw/核实/ 无既存札记（无竞写）
- Doctor 批「札记 + props 注记」后落盘：札记 `raw/核实/2026-08-15-Anthropic Q2财报与IPO进度核实札记.md` + patch `mapping/_v3_20260815_AnthropicQ2财报_manual.json`（纯 update ×2：run-rate 节点 +6 props as_of 分层、company_Anthropic +6 props IPO hedged）
- 沙箱 dry-run：双 took_patch、四道闸全过、内存深合并核验旧值保留 + desc 未动；Doctor 终端 promote 02:49，canonical **4069/4578 不变（+0/+0）**、健康埋点 ok、备份 bak.20260815_024900
- 档案三件套回写并 grep 核验：系统概览「最后更新」前段 + 决策记录新条目 + 项目日志 `logs/2026-08-15-AnthropicQ2财报核实.md`

## 做出的决策

| 决策 | 原因 | 影响 |
|------|------|------|
| 落点「札记 + props 注记」（Doctor 批推荐项） | Q2 财务数字=高时效铁律不入事实层；run-rate 概念节点已在图（4 月 $30B），新值时点分层沿韬定律「绝对值仅 props」先例；IPO 秘密提交=已发生结构事实但上市未落地，沿 07-13 光库收购「进行中事件」先例 hedged | 两节点各 +6 props；canonical 计数 +0/+0 |
| 不新建节点、不动 desc | run-rate 节点 name/desc 锚定 4 月时点，改 desc 破坏「不同时点判断并存」（MiniMax 先例）；IPO 事件等落地再升 | 零结构变动 |

## 遗留问题 / 待办

- 无新 TODO。升级触发器随札记跟踪（S-1 公开→复核口径 / 10 月上市落地→event 或 props 升级 / Q2 终值修订→更新 props），沿「传闻核实札记触发器」惯例不挂 TODO。

## 相关笔记

- [[渊图/architecture/决策记录]]
- 项目日志：`logs/2026-08-15-AnthropicQ2财报核实.md`
- 核实札记：`Database/行业研究/raw/核实/2026-08-15-Anthropic Q2财报与IPO进度核实札记.md`
