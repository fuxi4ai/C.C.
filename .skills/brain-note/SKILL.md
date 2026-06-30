---
name: "brain-note"
description: "Start a structured note-capture session in the brain inbox. Trigger when the user types `/note [主题]` or `/note` or says \"起一条笔记\", \"记个想法\", \"捕捉这个\", \"新开一条笔记\". Creates a new file in `~/Documents/Claude/brain/inbox/{主题}.md` from the default-note template, then enters capture mode — Claude listens, structures user dictation into the note in real time, asks targeted follow-ups, and on maturity suggests promoting it to `permanent/`."
---

# brain-note — Inbox 笔记采集

## 触发

- `/note [主题]`
- `/note`（无参数 → 先问主题）
- "起一条笔记" / "记个想法" / "捕捉这个" / "新开一条笔记"

## 执行步骤

### Step 1 · 确定主题

有参数用参数；无参数先问："这条笔记的主题是什么？（一句话）"

### Step 2 · 检查重复

```bash
ls ~/Documents/Claude/brain/inbox/*{主题}*.md ~/Documents/Claude/brain/permanent/*{主题}*.md 2>/dev/null
```
若已有相近笔记 → "已有 `{文件名}`，要追加进它、还是新开一条？"

### Step 3 · 创建文件

读 `~/Documents/Claude/brain/templates/default-note.md` 作为模板。

写入：`~/Documents/Claude/brain/inbox/{主题}.md`

frontmatter：
- `title`: {主题}
- `tags`: [inbox]
- `created` / `updated`: 今日
- `status`: draft
- `type`: fleeting

正文先放 `# {主题}` + 空行。

### Step 4 · 进入采集态

回："📝 inbox/{主题}.md 已开始，你说我整理。"

然后**听 Doctor 口述**：
1. 把口述按结构整理（小标题、列表、关键词加粗）
2. 追加到该 inbox 文件
3. 出现概念实体主动加 `[[wikilink]]`
4. **不照搬原话**——结构化

### Step 5 · 成熟度判断

每写完一段自检：
- 是否包含一个完整的原子概念？
- 是否至少 2 个 `[[wikilink]]`？
- 是否有清晰的"主张/事实/经验"中至少一项？

三项都 ✓ 提示：
"这条已经成型了，要不要 promote 到 `permanent/{主题}.md`？"

### Step 6 · 退出采集态

用户说"好了" / "存档" / "/note end" → 停止追加，做最终摘要回报。

## 边界

- 文件名清理：去掉 `/`、`\`、`:`
- 默认 type `fleeting`；promote 时改 `permanent`
- 采集态里**不要**每段都确认——批量整理，定期问"还要继续吗？"
