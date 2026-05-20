---
name: brain-save
description: Persist the current session as a structured log entry in the brain vault. Trigger when the user types `/save` or `/save [主题]` or says "存档本次会话", "记一笔", "落盘", "存档今天". Fills the session-log template with what was done, decisions, outstanding issues, related notes, then writes to `~/Documents/Claude/brain/logs/YYYY-MM-DD-{主题}.md`. Updates the project's last-active date if a project is identified. **Provides git commit+push commands for Doctor to run in macOS terminal** when `brain/.git/` exists — CC MUST NOT run git write commands in sandbox (Doctor GOTCHAS v2.0).
---

# brain-save — 把本次会话存档到 brain

## 触发

- `/save`(无参数 → CC 自己总结主题)
- `/save [主题]` 或 `/save [项目名]`
- "存档本次会话" / "记一笔" / "落盘这次工作" / "存档今天"

## 执行步骤

### Step 1 · 总结主题

如果用户给了参数,用作 `{主题}`;否则 CC 从本次对话中提炼出一个 5-15 字的主题。
如果主题对应某个 brain 已注册项目,把项目名也记下用于 Step 4。

### Step 2 · 决定文件名

```
~/Documents/Claude/brain/logs/YYYY-MM-DD-{主题}.md
```
同一天同主题多次 /save → 追加 `-HHmm`:
```
~/Documents/Claude/brain/logs/YYYY-MM-DD-{主题}-HHmm.md
```

### Step 3 · 填模板写日志

读 `~/Documents/Claude/brain/templates/session-log.md` 作为模板。

填入:
- `title`:会话日志 YYYY-MM-DD — {主题}
- `tags`:[log, {项目名(如有)}]
- `created` / `updated`:今日
- `status`:active
- `type`:log
- `project`:(如指明)

正文段落(模板不存在用 fallback):

```markdown
# 会话日志 — YYYY-MM-DD

**项目**:{项目名 / 跨项目}
**主题**:{主题}

---

## 完成的工作
(具体动作,列表,每条一句话)

## 做出的决策
(决策内容 + 理由)

## 遗留问题 / 待办
- [ ] ...

## 相关笔记
- [[wikilink]]
```

### Step 4 · 同步项目状态(如指明项目)

更新 `~/Documents/Claude/brain/{项目名}/architecture/系统概览.md` 中"最后活跃"字段为今日。

### Step 5 · 贴 Git 命令给 Doctor(★★★ v2.0 升级 · 2026-05-20)

⚠️ **CC 绝对禁止在 sandbox 跑任何 git 写命令** — 参 `~/Documents/Claude/brain/permanent/通用教训.md` G-X2 + `~/Documents/Claude/Projects/海螺姑娘/GOTCHAS.md` v2.0 规则。
**禁止**:`git add` / `git commit` / `git push` / `git pull` / `git fetch` / `git checkout` / `git merge` / `git mv` / `git rm`
**唯一允许**(只读探测 .git/ 是否存在):`git status` / `git log --no-pager` / `git diff --no-color` / `git show`

**正确流程** — 构造命令字符串,贴给 Doctor 在 macOS 终端跑:

1. **只读探测 .git/ 是否存在**(用 Read 工具或 `ls -la ~/Documents/Claude/brain/.git/HEAD` 测试,不要用 git write):
   - 存在 → 进入第 2 步
   - 不存在 → 跳过整个 Step 5,不报错

2. **生成命令字符串**(贴在 Step 6 回报里给 Doctor):

```bash
cd ~/Documents/Claude/brain && git add -A && git commit -m "session: {主题} {date}" && git push
```

3. **若 brain/.git/ 上次 sandbox 跑过 git 留下污染**(.git/HEAD.lock 等),命令前加清理:

```bash
cd ~/Documents/Claude/brain && \
  rm -f .git/HEAD.lock .git/objects/maintenance.lock 2>/dev/null && \
  find .git/objects -name "tmp_obj_*" -delete 2>/dev/null && \
  git add -A && git commit -m "session: {主题} {date}" && git push
```

4. **如果 Step 4 同步了项目状态**,且该项目有独立 git repo(如 `Projects/海螺姑娘/`),把那个仓库的 commit 命令也贴上:

```bash
cd ~/Documents/Claude/Projects/{项目名} && git add -A && git commit -m "{项目名}: {主题} {date}" && git push
```

**CC 自我检查触发词**:看到自己即将在 `mcp__workspace__bash` 调用里输入 "git add" / "git commit" / "git push" → **立即停** → 改贴命令到 Step 6 回报。

### Step 6 · 回报

```
✅ 已存档
📁 logs/YYYY-MM-DD-{主题}.md

📋 请在 macOS 终端跑(brain 仓库 commit+push):
```bash
cd ~/Documents/Claude/brain && git add -A && git commit -m "session: {主题} {date}" && git push
```

{若同步了独立项目 git:补贴该项目的 commit+push 命令}

一句话摘要:{20 字内}
```

**注意**:不在回报里写"已提交 commit hash" — 因为 commit 还没跑(Doctor 还没在 terminal 执行)。等 Doctor 反馈结果后才能说"已提交"。

## 边界

- 主题里去除 `/`、`\`、`:` 等危险字符
- session-log.md 模板缺失用 fallback
- 没有 .git/ 跳过 Step 5,不报错(但 Step 3+4 落盘照做)
- **不在 sandbox 跑 git 写命令** = 硬约束 · 不可绕过(参 G-X2)

## v 历史

- v1.0(2026-05-14):初版 · Step 5 自动 git commit
- v1.1(2026-05-19):brain_checkup v1.2 加 sandbox 探测后,本 skill 仍是"自动 commit"(未同步)
- **v2.0**(2026-05-20):Step 5 升级为"贴命令给 Doctor"(响应 GOTCHAS G-X2:CC 在 sandbox 不能跑 git)
