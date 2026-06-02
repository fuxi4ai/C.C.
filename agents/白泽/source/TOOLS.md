# TOOLS.md - 工具与基础设施配置

> **用途：** 数据源、凭证、系统服务的技术配置笔记
> **最后更新：** 2026-06-03

---

## 📊 数据库

### 本地数据库
| 数据库 | 位置 | 用途 | 大小 |
|:-------|:-----|:-----|:-----|
| 业务拆分库 | `data/business_breakdown.db` | 标的业务拆分数据 | 110KB |
| Tushare 缓存库 | `data/tushare.db` | API 数据本地缓存 | 532KB |
| 估值库 | `data/valuation.db` | 个股每日估值 | 127KB |
| 宏观预测库 | `projects/baize-astrology/data/macro_prediction.db` | 观星预测数据 | 25KB |
| 梦境状态 | `data/dragon-dream/dream-state.json` | 梦境运行状态 | <1KB |

### TOS 共享库
| 数据库 | 路径 | 维护人 |
|:-------|:-----|:-------|
| Macroeconomics | `tos://dragonpalace/shared database/` | 白泽 |
| Post-Market Recap | 同上 | 烛阴 |
| Quantitative | 同上 | 句芒 |
| Fundamental | 同上 | 龙鱼儿 |
| Industrial | 同上 | C.C. |

---

## 🔌 API 数据源

| 数据源 | 状态 | 说明 |
|:-------|:----:|:-----|
| Tushare Pro | ✅ | 积分>5000，全接口权限 |
| 阿里云百炼 | ✅ | 主用 coding-plan |
| Notion API | ✅ | 数据库同步 |
| GitHub API | ✅ | 仓库管理 |

---

## 🔐 凭证存储

**位置：** `.secrets/`（权限 600）

| 文件 | 用途 |
|:-----|:-----|
| `bailian_coding_plan.env` | 百炼 Coding-Plan（主用） |
| `github_token.env` | GitHub API |
| `notion_token.env` | Notion API |
| `tushare_token.env` | Tushare Pro |
| `vault.key.bak` | Vault 加密密钥备份 |

**加密工具：** `scripts/vault.py` (AES-256)

---

## 🧠 记忆系统

| 组件 | 位置 | 说明 |
|:-----|:-----|:-----|
| 日志文件 | `memory/YYYY-MM-DD.md` | 每日原始日志 |
| 长期记忆 | `MEMORY.md` | 精选长期记忆 |
| LanceDB | `~/.openclaw/memory/lancedb/` | 向量数据库（自动回忆） |

---

## 🌉 飞书 Bridge

| 字段 | 值 |
|:-----|:---|
| App ID | ✅ 已配置（见 `.secrets/`） |
| Gateway Token | ✅ 已配置（见 `.secrets/`） |
| 状态 | ✅ 运行中 |

---

*白泽 · TOOLS.md v2.0 · 2026-06-03*
