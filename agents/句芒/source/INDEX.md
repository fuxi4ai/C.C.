# 📂 全局索引

> **加载时机**: Session 伊始加载，知道什么在哪里找

---

## 📄 核心配置（根目录）

| 文件 | 内容 |
|------|------|
| `AGENTS.md` | 工作区规则（全局认知 + 任务处理规则，146 行） |
| `SOUL.md` | 句芒 · 活泼俏皮版 |
| `USER.md` | 月兔哥哥的信息 |
| `IDENTITY.md` | 身份信息 |
| `MEMORY.md` | 长期记忆 |
| `TOOLS.md` | 工具笔记 |
| `HEARTBEAT.md` | 心跳配置 |
| `README.md` | 项目说明 |
| `TODO.md` | 待办事项 |
| `CHANGELOG.md` | 变更日志 |
| `INDEX.md` | 本文件 |
| `GOTCHAS.md` | 全局错题本 |

## 两段式披露

| 层级 | 加载时机 | 内容 |
|------|----------|------|
| **第一段** | Session 伊始 | AGENTS.md（全局认知 + 任务规则） + INDEX.md（导航） |
| **第二段** | 调用项目时 | 项目内 INDEX.md → 按需加载 README/PRD/GOTCHAS/SKILL |

## 🔥 热区

| 目录 | 内容 | 需加载文件 |
|------|------|------------|
| `skills/` | 34 个技能模块 | 各有 INDEX.md + README/SKILL + GOTCHAS + PRD |
| `tools/` | mootdx 行情工具 | README.md + GOTCHAS.md + PRD.md + INDEX.md |
| `scripts/` | 21 个 Python 脚本 | README.md + GOTCHAS.md + PRD.md + INDEX.md |
| `quant_research/` | 量化研究（2 个项目） | 各有 INDEX.md + README/SKILL + GOTCHAS + PRD |
| `database/` | 行情数据库 202MB | README.md |

## ❄️ 冷区

| 目录 | 内容 |
|------|------|
| `archive/` | 项目归档 + 规则参考 |
| `backup/` | 量化策略备份 |
| `data_history/` | 198MB 个股日线 JSON（843 只） |

## 📁 通用

| 目录 | 内容 |
|------|------|
| `docs/` | 文档 + 核心系统架构 + 规则参考 |
| `memory/` | 每日日记 |
| `temp/` | 临时文件 |
| `PDF 提取/` | 8 篇 PDF 提取内容 |
| `.trash/` | 回收站（30 天） |

## 📊 TOS 共享库

| 别名 | 路径 | 维护人 |
|------|------|--------|
| Quantitative | `shared database/Quantitative/` | 句芒 |
| Macroeconomics | `shared database/Macroeconomics/` | 白泽 |
| Post-Market Recap | `shared database/Post-Market Recap/` | 烛阴 |
| Fundamental | `shared database/Fundamental/` | 龙鱼儿 |
| Industrial | `shared database/Industrial/` | C.C. |
