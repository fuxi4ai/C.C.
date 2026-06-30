---
title: Cowork Artifact 存储机制
tags: [artifact, cowork, claude-desktop, 存储, 机制]
created: 2026-06-30
updated: 2026-06-30
status: active
type: permanent
---

# Cowork Artifact 存储机制

> Claude 桌面应用（Anthropic 官方 / Claude-3p / gateway 客户端）的 artifact 体系是**双层结构**：上层 manifest 索引 + 下层 Chromium Partition 真身。摸清机制后才能做手动迁移、调试、跨环境复制等操作。

---

## 一、双层结构总览

| 层 | 文件/目录 | 作用 |
|----|----------|------|
| **Manifest** | `~/Library/Application Support/{Claude\|Claude-3p}/local-agent-mode-sessions/{workspaceId}/{accountId}/artifacts.json` | JSON 数组，每条 artifact 一个对象——记录元数据，**不含 HTML 内容也不含 path 字段** |
| **真身（HTML）** | `~/Library/Application Support/{Claude\|Claude-3p}/Partitions/cowork-artifact-{workspaceId}-{accountId}/Local Storage/` | Chromium Partition 的 LevelDB，artifact HTML 内容作为 Web Storage 键值对存进去 |

Partition 还顺带带了一堆 Chromium 周边目录（`Cache` `GPUCache` `Session Storage` `blob_storage` 等），多数是 cache、可忽略。真数据只在 `Local Storage`。

---

## 二、Manifest 字段范式

`artifacts.json` 顶层是 list，每项形如：

```jsonc
{
  "id": "zhuzhao-jiuyin-daily",          // kebab-case 唯一标识
  "name": "Zhuzhao Jiuyin Daily",         // 展示名
  "description": "最后更新 ... 烛照九阴复盘日报...",
  "createdAt": 1781278100863,             // ms 时间戳（int，非 ISO string）
  "updatedAt": 1782816822012,
  "isStarred": true,
  "versions": [1781278100863, 1781278444904, ...],  // 历史版本时间戳数组
  "createdBySessionId": "local_c8c57d89-…",
  "lastModifiedBySessionId": "local_c0498b3c-…"
}
```

**关键**：**无 `path` / `file` / `htmlPath` 字段**——manifest 不指向任何 HTML 文件，HTML 真身由 Chromium Partition 按 `id` 隐式定位（实测推断）。

---

## 三、Partition 目录命名规则

```
Partitions/cowork-artifact-{workspaceId}-{accountId}/
```

- `workspaceId` 和 `accountId` 都是 UUID
- **官方 Anthropic 桌面应用**：`workspaceId` `accountId` 由账号系统下发（如 `1b8ced31-…/b6de05fa-…`）
- **Claude-3p (gateway)**：用占位 UUID（如 `accountId=00000000-0000-4000-8000-000000000001`），workspaceId 由 Claude-3p 本地生成

切工作环境（官方账号 ↔ gateway）会让 workspaceId/accountId 全换，artifact partition 跟着另起一份、**与原账号互不可见**。

---

## 四、session 内的 `outputs/*.html` 不是 artifact

`local-agent-mode-sessions/{ws}/{acct}/local_{sessionId}/outputs/*.html` 通常远多于真 artifact 数（实例：167 个 HTML vs 4 个真 artifact）——这些是 CC 在某 session 内 Write 出来的中间产物（同一 artifact 多次迭代的 staging 版本、被 `mcp__cowork__create_artifact` 当 `html_path` 引用过）。**注册成 artifact 的那一刻才被 Chromium 写入 Local Storage**，之后 outputs/ 里的源文件即便删了 artifact 也还能开。

判别：`artifacts.json` 里能查到 id 才是真 artifact；outputs 里的 .html 只是源材料。

---

## 五、跨环境迁移要点（2026-06-30 教训）

切工作环境后想把旧账号的 artifact 搬到新账号，必须**同时迁两份**：

1. **Manifest**：`artifacts.json` cp 到新 workspace 目录
2. **Partition**：整个 `Partitions/cowork-artifact-{wsOld}-{acctOld}/` cp 到新位置、**目录名改为新 `{wsNew}-{acctNew}`**

```bash
SRC_WS="..." SRC_ACCT="..."
DST_WS="..." DST_ACCT="..."
cp "<srcWsDir>/artifacts.json" "<dstWsDir>/artifacts.json"
cp -R "Partitions/cowork-artifact-${SRC_WS}-${SRC_ACCT}" \
      "Partitions/cowork-artifact-${DST_WS}-${DST_ACCT}"
```

完事后 **Cmd+Q 完全退出**目标应用、重开 + 新会话——manifest 只在 session 启动时扫，热加载不生效。

### 风险点：Local Storage origin 卡死

Chromium Local Storage 按 **origin** 分隔，partition 内部 LevelDB 可能以旧 `workspaceId` 作为 origin 命名空间存数据。改 partition 目录名虽然让应用扫到了，但 LevelDB 里的旧 origin 数据可能跟新 origin 对不上、读不到——表现：list_artifacts 列出 4 个、但点开空白或报错。

**判定矩阵**：
| 现象 | 结论 |
|---|---|
| list 全有 + 点开能渲染 | 方案 A（cp+改名）成功 |
| list 全有 + 点开空白 | origin 卡死 → 走方案 B（解 LevelDB 抽 HTML、用 `mcp__cowork__create_artifact` 工具重注册），versions 历史会丢但内容能救 |
| 完全 list 不出 | manifest 路径/格式有差异 |

---

## 六、相关笔记

- [[已装skill清单]]（同期立 · 跨环境资产管理姊妹篇）
- [[Doctor协作偏好]]（gateway 模式 skill 交付偏好同期立）
- [[通用教训]] G-X43（Cowork frontmatter 范式 · 同期立 · 同属"Cowork 隐性约束"族）
- logs/2026-06-30-gateway切换善后-skill与artifacts补迁.md（机制刨出来的整个过程）
- 官方文档：`mcp__cowork__create_artifact` / `mcp__cowork__list_artifacts` / `mcp__cowork__update_artifact` 三件工具
