---
name: brain-commands
description: Brain vault command suite — `/resume` restores cross-session context, `/save [主题]` archives the current session to a structured log, `/note [主题]` opens a structured capture in the inbox. Trigger when the user's message starts with `/resume`, `/save`, or `/note`, or when they say "恢复上下文", "继续上次", "上次干到哪了", "存档本次会话", "记一笔", "落盘", "起一条笔记", "记个想法", "捕捉这个". Reads/writes inside `~/Documents/Claude/brain/` (logs/, inbox/, {项目}/architecture/), uses `~/Documents/Claude/brain/templates/` for note format, and commits to git when `brain/.git/` exists.
---

# brain-commands — Brain Vault 命令套件

> 一个 skill 涵盖三个显式命令：`/resume` · `/save` · `/note`。
> Brain vault 根目录：`~/Documents/Claude/brain/`

---

## 路由表（先判断意图）

| 用户说 | 走哪条 |
|---|---|
| `/resume` / "恢复上下文" / "继续上次" / "上次干到哪了" | → [§A · /resume](#a-resume) |
| `/save` / `/save [主题]` / "存档本次会话" / "记一笔" / "落盘" | → [§B · /save](#b-save) |
| `/note` / `/note [主题]` / "起一条笔记" / "记个想法" / "捕捉这个" | → [§C · /note](#c-note) |

如果用户的话同时沾到两条，问一句："你是想 /resume 还是 /save？"再继续。

---

## §A · /resume — 恢复跨 session 工作上下文 {#a-resume}

### 执行步骤

**Step 1 · 读最近 3 篇会话日志**
```bash
ls -t ~/Documents/Claude/brain/logs/*.md | head -3
```
把这 3 个文件全文读入。

**Step 2 · 识别活跃项目**
从日志的 `project:` frontmatter、文件名主题、或正文中提取最近活跃的项目名（DVA / 龙鱼五力 / 渊图 / O MY HTML / PEC / 海螺姑娘 / 司南 / Optical communication）。

若识别到，读：
```
~/Documents/Claude/brain/{项目名}/architecture/系统概览.md
~/Documents/Claude/brain/{项目名}/architecture/决策记录.md
~/Documents/Claude/brain/{项目名}/GOTCHAS.md   （存在则读）
```

**Step 3 · 扫 TODO 顶部**
读 `~/Documents/Claude/brain/TODO.md` 的"待办"段。

**Step 4 · 输出结构化摘要**
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

### 边界
- `logs/` 为空 → "brain 还没有会话日志。要不要我读 `permanent/项目总览.md` 给你看 8 个项目的整体状态？"
- 识别不到项目 → 只输出全局摘要，问 Doctor 想进入哪个项目
- **不**一次性读项目全部文档——只读 architecture/系统概览/决策记录/GOTCHAS

---

## §B · /save — 把本次会话存档到 brain {#b-save}

### 执行步骤

**Step 1 · 总结主题**
有参数用参数；无参数 CC 自己从对话中提炼 5-15 字主题。
若主题对应已注册项目，记下项目名用于 Step 4。

**Step 2 · 决定文件名**
```
~/Documents/Claude/brain/logs/YYYY-MM-DD-{主题}.md
```
同一天同主题多次 /save → 追加 `-HHmm`：
```
~/Documents/Claude/brain/logs/YYYY-MM-DD-{主题}-HHmm.md
```

**Step 3 · 填模板写日志**
读 `~/Documents/Claude/brain/templates/session-log.md` 作为模板，填入：
- `title`: 会话日志 YYYY-MM-DD — {主题}
- `tags`: [log, {项目名}]
- `created` / `updated`: 今日
- `status`: active
- `type`: log
- `project`: （如指明）

正文段落（如模板不存在，用以下 fallback）：
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

**Step 4 · 同步项目状态（如指明项目）**
更新 `~/Documents/Claude/brain/{项目名}/architecture/系统概览.md` 中"最后活跃"字段为今日。

**Step 5 · Git 提交（如已 init）**
```bash
if [ -d ~/Documents/Claude/brain/.git ]; then
  cd ~/Documents/Claude/brain
  git add -A
  git commit -m "session: {主题} {date}"
fi
```
没有 .git 跳过，**不报错**。

**Step 6 · 回报**
```
✅ 已存档
📁 logs/YYYY-MM-DD-{主题}.md
{若 commit：📌 已提交：{commit hash 前 7 位}}

一句话摘要：{20 字内}
```

### 边界
- 主题里去除 `/`、`\`、`:` 等危险字符，空格可保留或换成 `-`
- session-log.md 模板缺失用 fallback（见上）
- git 失败不影响落盘——日志写成功就算 /save 成功

---

## §C · /note — Inbox 笔记采集 {#c-note}

### 执行步骤

**Step 1 · 确定主题**
有参数用参数；无参数先问："这条笔记的主题是什么？（一句话）"

**Step 2 · 检查重复**
```bash
ls ~/Documents/Claude/brain/inbox/*{主题}*.md ~/Documents/Claude/brain/permanent/*{主题}*.md 2>/dev/null
```
若已有相近笔记 → "已有 `{文件名}`，要追加进它、还是新开一条？"

**Step 3 · 创建文件**
读 `~/Documents/Claude/brain/templates/default-note.md` 作为模板。
写入：
```
~/Documents/Claude/brain/inbox/{主题}.md
```
frontmatter：
- `title`: {主题}
- `tags`: [inbox]
- `created` / `updated`: 今日
- `status`: draft
- `type`: fleeting

正文先放 `# {主题}` + 空行。

**Step 4 · 进入采集态**
回："📝 inbox/{主题}.md 已开始，你说我整理。"

然后**听 Doctor 口述**：
1. 把口述按结构整理（小标题、列表、关键词加粗）
2. 追加到该 inbox 文件
3. 出现概念实体主动加 `[[wikilink]]`
4. **不照搬原话**——结构化

**Step 5 · 成熟度判断**
每写完一段自检：
- 是否包含一个完整的原子概念？
- 是否至少 2 个 `[[wikilink]]`？
- 是否有清晰的"主张/事实/经验"中至少一项？

三项都 ✓ 提示：
"这条已经成型了，要不要 promote 到 `permanent/{主题}.md`？我可以帮你迁过去并把 status 改成 active。"

**Step 6 · 退出采集态**
用户说"好了" / "存档" / "/note end" → 停止追加，做最终摘要回报。

### 边界
- 文件名清理：去掉 `/`、`\`、`:`，空格保留或换成 `-`
- 默认 type `fleeting`；promote 时改 `permanent`
- 采集态里**不要**每段都确认——批量整理，定期问"还要继续吗？"

---

## 通用约定

- 所有路径用绝对 `~/Documents/Claude/brain/...`，避免相对路径
- frontmatter 严格遵守 `brain/CLAUDE.md` 中定义的 schema
- 写入前若发现已存在同名文件，**不覆盖**——按 Step 提示用户决定
