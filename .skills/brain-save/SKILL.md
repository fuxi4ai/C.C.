---
name: brain-save
description: Persist the current session as a structured log entry in the brain vault. Trigger when the user types `/save` or `/save [主题]` or says "存档本次会话", "记一笔", "落盘", "存档今天". Fills the session-log template with what was done, decisions, outstanding issues, related notes, then writes to `~/Documents/Claude/brain/logs/YYYY-MM-DD-{主题}.md`. Updates the project's last-active date if a project is identified. Commits to git when `brain/.git/` exists.
---

# brain-save — 把本次会话存档到 brain

## 触发

- `/save`（无参数 → CC 自己总结主题）
- `/save [主题]` 或 `/save [项目名]`
- "存档本次会话" / "记一笔" / "落盘这次工作" / "存档今天"

## 执行步骤

### Step 1 · 总结主题

如果用户给了参数，用作 `{主题}`；否则 CC 从本次对话中提炼出一个 5-15 字的主题。
如果主题对应某个 brain 已注册项目，把项目名也记下用于 Step 4。

### Step 2 · 决定文件名

```
~/Documents/Claude/brain/logs/YYYY-MM-DD-{主题}.md
```
同一天同主题多次 /save → 追加 `-HHmm`：
```
~/Documents/Claude/brain/logs/YYYY-MM-DD-{主题}-HHmm.md
```

### Step 3 · 填模板写日志

读 `~/Documents/Claude/brain/templates/session-log.md` 作为模板。

填入：
- `title`：会话日志 YYYY-MM-DD — {主题}
- `tags`：[log, {项目名（如有）}]
- `created` / `updated`：今日
- `status`：active
- `type`：log
- `project`：（如指明）

正文段落（模板不存在用 fallback）：

```markdown
# 会话日志 — YYYY-MM-DD

**项目**：{项目名 / 跨项目}
**主题**：{主题}

---

## 完成的工作
（具体动作，列表，每条一句话）

## 做出的决策
（决策内容 + 理由）

## 遗留问题 / 待办
- [ ] ...

## 相关笔记
- [[wikilink]]
```

### Step 4 · 同步项目状态（如指明项目）

更新 `~/Documents/Claude/brain/{项目名}/architecture/系统概览.md` 中"最后活跃"字段为今日。

### Step 5 · Git 提交（如已 init）

```bash
if [ -d ~/Documents/Claude/brain/.git ]; then
  cd ~/Documents/Claude/brain
  git add -A
  git commit -m "session: {主题} {date}"
fi
```
没有 .git 跳过，**不报错**。

### Step 6 · 回报

```
✅ 已存档
📁 logs/YYYY-MM-DD-{主题}.md
{若 commit：📌 已提交：{commit hash 前 7 位}}

一句话摘要：{20 字内}
```

## 边界

- 主题里去除 `/`、`\`、`:` 等危险字符
- session-log.md 模板缺失用 fallback
- git 失败不影响落盘
