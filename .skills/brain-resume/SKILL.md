---
name: brain-resume
description: Restore working context at the start of a session. Trigger when the user types `/resume` or says "恢复上下文", "继续上次", "上次干到哪了", "接着昨天". Reads the most recent 3 session logs from `~/Documents/Claude/brain/logs/`, plus the active project's architecture overview and decisions, then outputs a structured handoff: last project worked on, key decisions, outstanding TODOs, and three suggested next steps.
---

# brain-resume — 恢复跨 session 工作上下文

## 触发

- `/resume`
- "恢复上下文" / "继续上次" / "接着昨天" / "上次干到哪了"

## 执行步骤

### Step 1 · 读最近 3 篇会话日志

```bash
ls -t ~/Documents/Claude/brain/logs/*.md | head -3
```
把这 3 个文件全文读入。

### Step 2 · 识别活跃项目

从日志的 `project:` frontmatter、文件名主题、或正文中提取最近活跃的项目名（DVA / 龙鱼五力 / 渊图 / O MY HTML / 政治经济学 / 海螺姑娘 / 司南）。

若识别到，读：
```
~/Documents/Claude/brain/{项目名}/architecture/系统概览.md
~/Documents/Claude/brain/{项目名}/architecture/决策记录.md
~/Documents/Claude/brain/{项目名}/GOTCHAS.md
```

### Step 3 · 扫 TODO 顶部

读 `~/Documents/Claude/brain/TODO.md` 的"待办"段。

### Step 4 · 输出结构化摘要

```
**上次工作**：{项目名} · {日期}

**关键决策**（最多 3 条）：
- ...

**遗留待办**（最多 5 条）：
- [ ] ...

**建议下一步**（3 条具体动作）：
1. ...
2. ...
3. ...

需要我从哪一项开始？
```

## 边界

- `logs/` 为空 → "brain 还没有会话日志。要不要我读 `permanent/项目总览.md` 给你看 8 个项目的整体状态？"
- 识别不到项目 → 只输出全局摘要，问 Doctor 想进入哪个项目
- **不**一次性读项目全部文档——只读 architecture/系统概览/决策记录/GOTCHAS
- 所有路径用绝对 `~/Documents/Claude/brain/...`
