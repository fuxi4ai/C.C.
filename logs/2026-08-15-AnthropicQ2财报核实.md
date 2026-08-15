---
title: 2026-08-15 Anthropic Q2 财报核实（渊图追新闻）
tags: [渊图, log]
date: 2026-08-15
---

# 2026-08-15 Anthropic Q2 财报核实（渊图追新闻 · props 注记批）

**触发**：Doctor「渊图追一个新闻：Anthropic最新财报」。

## 核实结论（P 级）

- **Q2 2026 初步营收 >$11.5B**（Bloomberg，08-15）：同比至少 +14x（去年同期 $787M），环比 Q1 $4.73B。preliminary，可能修订。
- **调整后营业利润首次转正**——IPO 前关键里程碑（与此前预测 $5.59 亿/5.1% 一致）。
- **run-rate**：2025 底 $9B → 02 $14B → 03 $19B → 04 $30B（官方宣布）→ 05 **$47B**（Bloomberg 文件）。
- **IPO**：6-01 秘密提交 S-1（大摩/高盛牵头、小摩参与）；目标 10 月 Nasdaq，募资 >$60B；投资者建模估值 $2-3T。Polymarket 10 月概率 62%（08-12）。
- 全年预期（hedged）：FY26 营收 ~$60B；年底 run-rate $100-120B。

## 落点（Doctor 批「札记 + props 注记」）

- `concept_AnthropicRunRateRevenue2026` +6 props（as_of 分层，不覆盖 4 月 $30B）
- `company_Anthropic` +6 props（IPO 提交/窗口/承销/募资/估值，hedged）
- 不入事实层（高时效铁律）；不新建节点、不动 desc（MiniMax 先例）
- 札记：`raw/核实/2026-08-15-Anthropic Q2财报与IPO进度核实札记.md`

## 执行与核验

- patch `mapping/_v3_20260815_AnthropicQ2财报_manual.json`（纯 update ×2）
- 沙箱 dry-run：双 took_patch、四道闸全过；内存深合并核验新 props 落地 + 旧值保留 + desc 未动
- Doctor 终端 promote 02:49：canonical **4069/4578 不变**（+0/+0）、健康埋点 overall=ok、备份 `bak.20260815_024900`

## 触发器

1. S-1 公开 → 复核数字口径（总额/净额），差异大改 props
2. 10 月上市落地 → event 节点或 props 升级
3. Q2 终值修订 → 更新 props as_of

## 信源

Bloomberg（via Yahoo Finance）/ 界面 / 金十 / aaStocks（08-15）；TheStreet / Business Insider（IPO 提交）；CNBC / Anthropic 官方（04 月 TPU 协议背景，已在图谱）。
