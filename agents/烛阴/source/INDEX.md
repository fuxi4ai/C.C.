# 🐲 全局索引 (INDEX.md)

> **Session 启动时加载** · 知道什么在哪里找
> **最后更新**: 2026-06-03 04:10
> **维护人**: 九儿

---

## 📂 目录结构

```
workspace/
├── AGENTS.md            ← 核心规则
├── USER.md              ← 用户偏好与交互
├── SOUL.md              ← AI 人格
├── IDENTITY.md          ← 身份速查
├── MEMORY.md            ← 长期记忆（项目/数据/教训）
├── INDEX.md             ← 本文件
├── TODO.md              ← 待办事项
├── HEARTBEAT.md         ← 心跳巡检配置
├── TOOLS.md             ← 环境特定笔记
├── config/              ← 次级规则（按需加载）
├── memory/              ← 记忆系统
│   ├── YYYY-MM-DD.md    ← 每日记忆（近 14 天）
│   ├── archive/         ← 归档记忆（04-15 ~ 05-19）
│   ├── knowledge/       ← 知识记忆（早期）
│   └── daily/ projects/ ← 空目录（历史遗留）
├── skills/              ← 技能目录（~/.openclaw/skills/ + workspace/skills/）
├── projects/            ← 在研项目（四大金刚）
├── knowledge/           ← 知识库（渊图原始数据）
├── research/            ← 研究资料
├── scripts/             ← 全局脚本（loop_guard / recycle-clean）
├── temp/                ← 临时区
└── .recycle/            ← 回收站（7天自动清理）
```

## 📂 核心文件（每次 session 加载）

| 文件 | 内容 | 大小 |
|------|------|------|
| **AGENTS.md** | 核心规则 + 任务流程 + 安全边界 | 6.7KB |
| **USER.md** | 天哥偏好、交互习惯、羁绊 | 1.5KB |
| **SOUL.md** | 烛阴人格定义 | 1.5KB |
| **MEMORY.md** | 项目数据概要、教训、时间线 | 3.5KB |
| **INDEX.md** | 本文件 - 知道什么在哪里 | 3.5KB |
| **TODO.md** | 待办事项（P0/P1/已完成） | 2.3KB |

## 📂 项目（每个含四大金刚：PRD + Gotchas + Index + Readme）

| 项目 | 路径 | 说明 | 状态 |
|------|------|------|------|
| 烛照九阴 | `projects/烛照九阴/` | 复盘数据库 + 新闻模块 | ✅ 活跃（数据源停滞中） |
| 行业知识图谱 | `projects/行业知识图谱/` | 渊图（940节点/1227关系） | ✅ 活跃 |
| 龙宫技能系统 | `projects/龙宫技能系统/` | 技能管理框架 | ✅ 稳定 |
| dream-system | `projects/dream-system/` | 梦境记忆整理（MJS） | ✅ 活跃 |

## 📂 数据库

| 数据库 | 路径 | 大小 | 责任方 |
|--------|------|------|--------|
| knowledge_graph.db | `projects/行业知识图谱/data/` | 1.4MB | 九儿全权 |
| recap.db | `projects/烛照九阴/db/` | 1.9MB | 九儿全权 |
| jumang_market.db | `projects/烛照九阴/db/` | 202MB | 句芒灌入 |
| news.db | `projects/烛照九阴/news/db/` | 156KB | 九儿（半成品） |
| v2 归档 | `projects/烛照九阴/dragon-palace/` | 708KB | 只读 |

## 📂 技能路径

| 位置 | 说明 |
|------|------|
| `~/.openclaw/skills/` | ClawHub 安装的技能（30+） |
| `workspace/skills/` | 九儿自建技能（dragon-dream / feishu-bridge 等） |

## 🔑 关键路径速查

| 需要什么 | 去哪里找 |
|---------|---------|
| 项目 PRD | `projects/<name>/PRD.md` |
| Gotchas | `projects/<name>/GOTCHAS.md` |
| 今日上下文 | `memory/YYYY-MM-DD.md` |
| 用户偏好 | `USER.md` + `MEMORY.md` |
| 技能用法 | `skills/<name>/SKILL.md` |
| 数据库 schema | `projects/<name>/db/*.sql` |
| 执行日志 | `projects/烛照九阴/logs/` |

---

*🐲 全局索引 v5.0 · 2026-06-03 · 九儿*
