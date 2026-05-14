# Brain Vault — CC 全局记忆与知识库

> Doctor 的第二大脑。CC 每次进入此目录或被要求读取记忆时，先读本文件。

## 什么是这个 Vault

`~/Documents/Claude/brain/` 是跨 session 的持久记忆与知识系统。存储：
- **决策与上下文**：做了什么决定、为什么做
- **项目进展**：每个项目的当前状态、待办、已知坑
- **领域知识**：结构性、半永久性知识（Zettelkasten）
- **会话日志**：每次工作的关键摘要

## 目录结构

```
brain/
├── CLAUDE.md           ← 本文件，CC 全局指令
├── permanent/          ← 沉淀的原子知识笔记（Zettelkasten）
├── inbox/              ← 待处理的原始捕捉（想法、草稿）
├── fleeting/           ← 临时笔记（短期有效）
├── logs/               ← 全局会话日志
├── references/         ← 外部参考资料摘要
├── templates/          ← 笔记模板
├── chats/
│   ├── code/           ← 从 Claude Code 导入的对话
│   └── web/            ← 从 Claude Web/App 导入的对话
├── graphify/           ← 代码库知识图谱（graphify 生成）
│   └── 渊图/
└── 渊图/               ← 渊图项目专属
    ├── architecture/   ← 架构决策
    ├── pipeline/       ← 数据流、脚本逻辑
    ├── data/           ← 数据模型、schema
    ├── features/       ← 功能规划
    └── logs/           ← 项目会话日志
```

## Zettelkasten 规则

### 笔记创建
- 使用 wikilinks：`[[笔记名]]`（不用 markdown 链接）
- 每个笔记必须有 YAML frontmatter
- 文件名用 kebab-case 或简洁中文：`知识图谱-节点类型.md`
- 每个 permanent 笔记只含一个概念（原子性）
- 每个笔记至少 2 个 wikilinks（密度链接）

### 标准 frontmatter
```yaml
---
title: 笔记标题
tags: [项目, 主题]
created: YYYY-MM-DD
updated: YYYY-MM-DD
status: active        # active | archived | draft
type: permanent       # permanent | fleeting | log | resource | decision
---
```

### 禁止
- 不要删除笔记，改为 `status: archived`
- 不要在内部笔记间用 markdown 链接，统一用 wikilinks
- 不要创建没有 frontmatter 的笔记
- 不要随意改变目录结构

## CC 命令

### /resume
收到此命令时：
1. 读取 `logs/` 中最近 3 篇会话日志
2. 读取当前项目的 architecture/decisions.md（如果存在）
3. 输出：当前状态摘要 + 待办清单

### /save
收到此命令时：
1. 在 `logs/YYYY-MM-DD-主题.md` 创建会话日志（格式见模板）
2. 记录：做了什么、决策、遗留问题、相关笔记链接
3. 更新相关项目目录下的 progress.md（如果存在）

### /note [主题]
收到此命令时：
1. 在 `inbox/` 创建一个新的临时笔记
2. 让 Doctor 口述内容，CC 整理成结构化笔记
3. 如果内容成熟，建议移入 `permanent/`

## 项目列表

| 项目 | 目录 | 状态 | 最后工作 |
|------|------|------|----------|
| 渊图（行业知识图谱） | `渊图/` | 🟢 活跃 | 2026-05-04 |
| DVA（抖音视频分析） | `DVA/` | 🟢 活跃 | 2026-05-06 |
| 龙鱼五力（行业五力分析） | `龙鱼五力/` | 🟢 活跃 | 2026-04-29 |
| 政治经济学 | `政治经济学/` | 🟢 活跃 | 2026-05-12 |
| 海螺姑娘（Conch 项目护航） | `海螺姑娘/` | 🟡 维护 | 2026-04-29 |
| O MY HTML（设计师工具箱） | `O MY HTML/` | 🟡 维护 | 2026-05-10 |
| Optical communication（光通信产业链） | `Optical communication/` | 📋 参考 | — |
| 司南（项目护航方法论） | `司南/` | 📋 参考 | — |

## ⚡ GOTCHAS 自动记录规则（强制，无需 Doctor 提示）

**触发条件**：CC 在任何工作中遇到以下情况之一，**立即**写入对应项目的 `GOTCHAS.md`，不等 Doctor 指示：

- 遇到报错，并找到了解法
- 发现某个工具 / 接口 / SDK 的非预期行为或限制
- 绕过了一个坑（即使没有报错，只是发现某种写法不奏效）

**判断阈值**：排查超过一轮的问题都值得记录；拼写错误等明显笔误不记。

**写入位置**：
- 有所属项目 → `~/Documents/Claude/Projects/{项目名}/GOTCHAS.md`
- 跨项目 / Cowork 环境问题 → `brain/permanent/通用教训.md`

**格式**（沿用司南方法论）：
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

## 图谱导航规则（Graphify）

有 graphify 图谱的项目，CC 应优先：
1. 查询 `graphify/{项目}/graph.json` 理解代码结构
2. 查询 vault 了解决策和上下文
3. 最后才直接读源代码

**当前有图谱的项目**：

| 项目 | 节点 | 路径 |
|------|------|------|
| DVA | 1070 节点 / 2203 边 / 65 community | `graphify/DVA/graphify-out/graph.json` |
| 渊图 | 832 节点 / 多边 / N community | `graphify/渊图/graphify-out/graph.json` |

查询：`graphify query "<问题>" --graph brain/graphify/{项目}/graphify-out/graph.json`
解释：`graphify explain "节点名" --graph ...`
最短路径：`graphify path "A" "B" --graph ...`


## 文件落点规则（Doctor 定，2026-05-14）

CC 创建/保存任何文件时，按以下规则选位置：

| 类别 | 落点 |
|---|---|
| **项目相关工作文件**（某个具体项目的代码、文档、产物、log） | 当前挂载的项目文件夹内；若挂载的是 `Documents/`，落到 `Documents/Claude/Projects/{项目名}/` 对应位置 |
| **全局工作文件**（跨项目工具、规则、代码、brain 系统、CC 自身配置） | `Documents/Claude/` 下相应位置 |
| **给 Doctor 的最终报告 / 交付物** | `Documents/AI4ME/` |
| **临时草稿 / 试跑脚本** | session 临时区（用户不可见） |

判断标尺：
- 文件**只服务于一个具体项目** → 项目相关工作文件
- 文件是**跨项目的工具/规则/代码/记忆系统组件** → 全局工作文件
- 文件是**给 Doctor 看的最终成果**（报告、总结、提案、可交付文档） → AI4ME
- 二义性大 → 主动问 Doctor 一次

---

## 来源
基于 [claude-code-memory-setup](https://github.com/lucasrosati/claude-code-memory-setup)
建立日期：2026-05-13
维护人：Doctor + CC
