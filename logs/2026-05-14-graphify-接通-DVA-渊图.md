---
title: 会话日志 2026-05-14 — graphify 接通 DVA + 渊图
tags: [log, brain, graphify, deepseek, dva, 渊图]
created: 2026-05-14
updated: 2026-05-14
status: active
type: log
project: Brain Vault
---

# 会话日志 — 2026-05-14 · graphify 接通

**项目**：Brain Vault / DVA / 渊图
**主题**：graphify + DeepSeek V4 接通，DVA + 渊图 图谱生成完成

---

## 完成的工作

### Skill 拆分（接续上一段）
- `/save` 在 Cowork 上 slash 路由验证成功（先前不通是合并版 description 多意图模糊）
- 拆出 3 个独立 SKILL.md（brain-resume / brain-save / brain-note），重新打包 .skill
- brain-commands 改名 `_DEPRECATED_` 留存

### graphify 接 DeepSeek
- 错误命令排查：`graphify .` / `graphify --obsidian` 都不是正确语法
- 实际 API：`graphify extract <src> --out <dst> --backend claude --model <name>`
- DeepSeek 提供 Anthropic 兼容端点 `https://api.deepseek.com/anthropic`
- key 落到 `.tools/.env.graphify`（已 .gitignore 排除）
- 第一次用 `deepseek-v4-pro` 失败：`'ThinkingBlock' object has no attribute 'text'`（thinking 内容块兼容性问题）
- 改 `deepseek-chat`（V3，无 thinking）→ 通过

### 两个项目图谱
- DVA：148 code + 79 LLM 调用 → 1070 nodes / 2203 edges / 65 community / $0.85
- 渊图：8 code + 603 docs+papers → 832 nodes / N edges / ?communities / $9.62
- 总成本 $10.47，跑时 ~30 分钟

---

## 做出的决策

| 决策 | 内容 |
|------|------|
| graphify backend | 走 DeepSeek 的 Anthropic 兼容端点（`/anthropic`），不走原生 OpenAI 兼容路径 |
| model 选择 | `deepseek-chat`（V3）而非 `deepseek-v4-pro`（thinking 不兼容 graphify v0.7.16） |
| key 存放 | `.tools/.env.graphify` + `.gitignore` 加 `.env*`、`*.key` 黑名单 |
| graphify-out 进 git | 进，约 2MB / 项目，纯 JSON 易于 diff |

---

## 遗留问题 / 待办

只剩 1 条：
- [ ] **PEC G-06~G-14 认识论陷阱入 brain** —— 需 Doctor 口述 + `/note` 整理

### 已知坑
- graphify `--out` 文档说会写到 `<DIR>/graphify-out/`，实际 v0.7.16 行为正常（验证）
- DeepSeek Anthropic 兼容端点对 thinking 模型有兼容性问题 → 用 `deepseek-chat` 规避
- `ThinkingBlock` 错误的根因是 graphify v0.7.16 假定所有 content block 都有 `.text` 属性 → 上游应支持 `BlockType` 判断

---

## 安全建议

`sk-3fe87...` key 已暴露在本次对话历史中，建议：
1. 去 [platform.deepseek.com](https://platform.deepseek.com) 撤销该 key
2. 重新生成，更新 `.tools/.env.graphify` 那一行

---

## 相关笔记

- [[2026-05-14-P0-P2-全量交付]] — 今天前半段（brain 系统主体）
- [[2026-05-14-max-p0-实施]] — 详细技术过程
- [[graphify-集成-20260514]] — graphify 集成文档（已校正命令语法）
- [[DVA]]
- [[渊图]]
