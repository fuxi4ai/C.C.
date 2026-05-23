---
title: 会话日志 2026-05-23 — MiroFish 调研与 DeepSeek 成本模型
tags: [log, 工具调研]
created: 2026-05-23
updated: 2026-05-23
status: active
type: log
project: 工具调研（MiroFish）
---

# 会话日志 — 2026-05-23

**项目**：工具调研（MiroFish）｜ 关联锚点：PEC（仅成本算例引用，未改 PEC 内容）
**主题**：MiroFish 调研与 DeepSeek 成本模型

---

## 完成的工作

- GitHub 检索 `mirofish`：定位真项目 = `666ghj/MiroFish`（盛大孵化，~33K stars，曾登 GitHub Trending 第一）；`github.com/mirofish` 是空壳组织页；另有 fork `nikmcfly/MiroFish-Offline`、`amadad/mirofish-cli`。
- 扒透仓库源码：README(中/英)、`.env.example`、`backend/app/config.py`、`backend/app/services/*`、`requirements.txt`/`pyproject.toml`、`docker-compose.yml`、`package.json`。
- 厘清架构：五步流水线（图谱构建 → 环境/人设 → 双平台模拟 → ReportAgent 报告 → 深度互动），仿真内核 = CAMEL-AI 的 OASIS（camel-oasis 0.2.5 + camel-ai 0.2.78），记忆层 = Zep Cloud，LLM 走 OpenAI 兼容 SDK。
- 厘清外部依赖：**只需两个云服务**——LLM API（OpenAI 兼容，主成本）+ Zep Cloud（记忆图谱，必需，有免费档）；可选 `LLM_BOOST_*` 副模型；**自身不需要单独 embedding/向量库**（Zep 云端处理）。
- 产出文档：`~/Documents/MiroFish-原理解读与云API部署指南.md`（十节：总览/原理/架构/外部API/选型/成本/部署/最小例子/坑/链接）。
- 加载 PEC 锚点上下文（系统概览 + GOTCHAS），据此算「PEC 中等体量预测」在 MiroFish 上用 DeepSeek 的成本，并把成本模型追加进文档第六节。

## 做出的决策

| 决策 | 原因 | 影响 |
|------|------|------|
| LLM 首选 DeepSeek（deepseek-chat） | OpenAI 兼容、2026 价极低（输入~¥0.2/M、输出~¥2/M、缓存~¥0.02/M）、中文好 | 中等体量单次 LLM ≈ ¥2–10 |
| 成本主体 = N×R（agent 数 × 轮数） | 决策调用线性乘积，是唯一大头 | 省钱靠压 N 和 R；先小后大 |
| Zep 是真正的瓶颈成本 | DeepSeek 压到几块后，记忆 episode 计费易超免费档 | 中等体量以上需 Flex ~$25 充值 |
| 不把本次写入 PEC 项目状态（不更新 PEC 系统概览最后活跃） | 本次是外部工具评估，非 PEC 框架推进 | 避免污染 PEC 精心维护的 last-active |
| MiroFish 输出定位为「情景生成器/假设来源」 | 按 PEC G-04 事后拟合 / G-01 万能概念 / G-10 框架自我保护 | 宜喂 predictions-register，不直接当 dated 预测 |

## 成本模型快照（DeepSeek · 含一次性开销）

| 规模 | N×R | 决策数 | LLM 估价 |
|------|-----|--------|----------|
| 小（试跑） | 30×10 | 300 | <¥1 |
| 中 | 100×20 | 2,000 | ¥2–10 |
| 大 | 500×30 | 15,000 | ¥15–60 |

> 中等体量 Token 预算 ≈ 输入 6.4M / 输出 0.6M；prompt 缓存命中后输入可再降。Zep 另计。

## 遗留问题 / 待办

- [ ] 若要实跑：在 Mac 上 `git clone` + 配 `.env`（DeepSeek + Zep）+ `npm run setup:all` + `npm run dev`（前端 3000 / 后端 5001）。Python 卡 3.11–3.12，用 uv。
- [ ] 第一次用「30 agent × ≤10 轮 + Zep 免费档」探真实单次消耗，再放大。
- [ ] 注意 AGPL-3.0：若改造后对外做 SaaS，需开放修改源码。
- [ ] 待定：是否把 MiroFish 作为 PEC predictions-register 的「情景生成器」纳入工作流（需评估其涌现结论与结构推导的认识论对接）。

## 相关笔记

- [[系统概览]]（PEC）
- [[GOTCHAS]]（PEC · G-01/G-04/G-10）
- 产出文档：`~/Documents/MiroFish-原理解读与云API部署指南.md`
- 仓库：https://github.com/666ghj/MiroFish
