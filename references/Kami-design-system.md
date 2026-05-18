---
title: Kami 紙 · AI Agent 文档设计系统（外部 skill）
tags: [reference, design-system, ai-skill, external]
created: 2026-05-15
updated: 2026-05-15
status: active
type: reference
external_source: https://github.com/tw93/kami
homepage: https://kami.tw93.fun/index-zh.html
author: tw93 (HiTw93)
---

# Kami 紙

> 面向 AI Agent 的文档设计系统 · 外部依赖
> 2026-05-14 Doctor 决策：O MY HTML 项目文档统一用 Kami 排版

## 本地 fallback 路径（项目内保留完整副本）

`Projects/O MY HTML/design-ref/kami/`（14 MB · 90 文件 · 含 SKILL.md + 10 份 references + 4 个 scripts + 模板/字体/图片）

— Project-Local Reference Fallback 策略（参照天工开物项目踩过的坑），避免 Cowork 装 skill 时只挂 SKILL.md 不保留子目录。

CC 用 Kami 排版时可直接 Read 本路径下的 reference 文件，不依赖任何外部 skill 安装环境。

## 装（外部 skill 路径）

```bash
# Claude Code
npx skills add tw93/kami -a claude-code -g -y

# Codex
npx skills add tw93/kami -a codex -g -y

# 通用 agent
npx skills add tw93/kami -a '*' -g -y
```

Claude Desktop：下载 [kami.zip](https://github.com/tw93/kami/releases/latest/download/kami.zip) → Customize > Skills > "+" > Create skill 上传。

## 用

直接告诉 Claude 自然语言（无需斜杠命令）：
- "帮我排版一份白皮书"
- "做一份简历"
- "把这份 README 排成 Kami 长文档"
- "做一份作品集 6 页"

## 核心设计哲学（8 条）

1. 页面底色 parchment `#f5f4ed`，**禁用纯白**
2. 强调色只有油墨蓝 `#1B365D`，**全文档不超过 5% 面积**
3. 所有灰色暖调（R ≈ G > B），**禁冷蓝灰**
4. 英文 serif 通吃；中文标题 serif、正文 sans
5. Serif 正文 400，标题 500，**不用合成 bold**
6. 行距三档：紧凑标题 1.1-1.3 / 密排 1.4-1.45 / 阅读 1.5-1.55
7. Tag 背景必须实色 hex，**禁 rgba**（WeasyPrint 双层矩形 bug）
8. 阴影只用 ring 或 whisper shadow，**不用硬 drop shadow**

## 输出类型（10 种模板 + 14 种 SVG 图表）

| 文档类型 | 适用 |
|---------|------|
| One-Pager | 简介 / 名片 / 概要 |
| Long Doc | 白皮书 / 研报 / 长文 |
| Letter | 正式信件 |
| Portfolio | 作品集 |
| Resume | 简历 |
| Slides | 幻灯片 |
| Equity Report | 个股研报 |
| Landing Page (zh/en) | 落地页 |
| Changelog | 更新日志 |
| Architecture / Flowchart / Bar Chart / Donut Chart / ... | 14 种内联 SVG |

## 与 O MY HTML 的关系

- **职责分工**：Kami 负责"AI 产出文档"层，O MY HTML 聚焦"城市浮雕 + 可交互可视化基底"层
- **设计哲学高度同构**：暖米底 + 单色克制 + 衬线层级 + 数值化预算
- **方法论借鉴**：Kami 已经把 color token / 字体层级 / 间距 / 反面示例工程化，我们方法论 v1.2 可参考其"决策速查表"格式

## 与城市浮雕系列的协作

```
城市浮雕（O MY HTML 内）：3D 微雕作底图 → 可交互可视化基底
       ↑                                          ↑
       │                                          │
       └─── 政经/渊图内容源头 ──────────┐         │
                                          │         │
       ┌──────────────────────────────────┘         │
       ↓                                            ↓
Kami（外部 skill）：把上述输出排成正式文档（白皮书 / 研报 / Slides）
```

## 关联

- [[O MY HTML/architecture/方法论]] · 城市浮雕系列定位章节
- [[O MY HTML/architecture/方法论]] · v1.1 与 Kami 同构对比
- [[政治经济学/architecture/系统概览]] · 文档输出可借 Kami 排版

---

_2026-05-14 入档 · 由 CC + Doctor 联合决策引入_
