---
title: MiroFish · 锚点 stub
tags: [MiroFish, anchor, 工具]
created: 2026-05-23
updated: 2026-06-16
status: active
type: stub
---

# MiroFish · 锚点 stub

> 群体智能仿真预测引擎（OASIS 驱动）。本地源码部署，DeepSeek + Zep。
> **命中锚点「MiroFish」时：CC 直接把下面的「启动命令」代码块贴给 Doctor，无需多问。**

## 🚀 启动命令（命中即贴这个）

```bash
cd ~/Documents/Claude/Projects/MiroFish && npm run dev
```

启动后浏览器打开 http://localhost:3000（后端 API 在 5001）。

## 重装/首次依赖（仅在报缺依赖时用）

```bash
cd ~/Documents/Claude/Projects/MiroFish && npm run setup:all && npm run dev
```

## 关键事实

- 部署路径：`~/Documents/Claude/Projects/MiroFish`
- LLM：DeepSeek（`deepseek-chat`，OpenAI 兼容）｜ 记忆：Zep Cloud
- Python：用 uv 钉 3.12（系统 3.13 不兼容 camel-oasis / camel-ai）；`backend/.python-version=3.12`
- 配置：仓库根目录 `.env`（DeepSeek + Zep key + `OASIS_DEFAULT_MAX_ROUNDS=10`，**无** `LLM_BOOST_*`）
- 省钱：成本主体 = agent 数 × 轮数；首跑用小种子 + ~30 agent + ≤10 轮，再去 DeepSeek/Zep 后台核实消耗
- 定位提醒：输出是「情景生成器/假设来源」，非已验证预测器（咬合 PEC G-01/G-04/G-10）

## GOTCHAS · 本地补丁（2026-06-16 · 让它真能跑）

> 这几处只在本机 `.venv`/`scripts`/`frontend`，**没进 git**；尤其 `recsys.py` 在 `.venv` 内，**`uv sync`/重装依赖会覆盖**，覆盖后照此重打。

1. **twhin 模型走本地**（HF 国内连不上、hf-mirror 又不支持 xet 协议）：
   - 已 `git clone https://hf-mirror.com/Twitter/twhin-bert-base ~/models/twhin-bert-base`（git+lfs 直连，绕过失败的 metadata HEAD）。
   - 改 `backend/.venv/lib/python3.12/site-packages/oasis/social_platform/recsys.py` **两处** `from_pretrained("Twitter/twhin-bert-base")` → `"/Users/lunarabbit/models/twhin-bert-base"`（`get_twhin_tokenizer` / `get_twhin_model`）。**⚠ uv sync 会覆盖、需重打。**
2. **emoji 写崩防护**：`backend/scripts/run_twitter_simulation.py:111` + `run_reddit_simulation.py:111` 的 `FileHandler(...)` 加 `errors='replace'`（agent 发 🇺🇸🇮🇱 的 surrogate 触 `UnicodeEncodeError` 拖死进程）。
3. **UI 起跑硬编码**：`frontend/src/components/Step3Simulation.vue:402` `enable_graph_memory_update: true→false`（关 Zep 实时写，防 300/min 限流拖慢/卡死）。注：同处 `platform:'parallel'` 也写死，要单平台得改这里或直接 `curl POST /api/simulation/start`。
4. **不想下模型的替代**：OASIS recsys 改 `RANDOM`/`REDDIT` 零模型依赖；或只跑 **reddit 单平台**天然绕开 twhin。
5. **正确部署路径**：`~/Documents/Claude/Projects/MiroFish`（旧 stub 写的 `~/Documents/projects/MiroFish` 已失效·2026-06-16 修）。后端口 5001、前端 3001/3000。

## 相关

- 指南：`~/Documents/MiroFish-原理解读与云API部署指南.md`
- 配置参考：`~/Documents/MiroFish-env配置参考.txt`
- 部署日志：[[2026-05-23-MiroFish本地部署落地]]
- 调研日志：[[2026-05-23-MiroFish调研与DeepSeek成本模型]]
- 仓库：https://github.com/666ghj/MiroFish
