---
title: chats/ — Claude 对话存档
tags: [chat, brain, import]
created: 2026-05-14
updated: 2026-05-14
status: active
type: resource
---

# chats/ — Claude 对话存档

跨端 Claude 对话归档区。两个子目录：

| 目录 | 来源 | 导入方式 |
|------|------|---------|
| `code/` | Claude Code · Cowork 桌面 | 自动（`import-chats.py`） |
| `web/` | Claude Web · iOS App | 手动（见下方流程） |

## code/ · Claude Code 对话自动导入

### 数据源

Cowork 桌面端 / Claude Code 每个 session 会在 `~/.claude/projects/<mangled-path>/<session-uuid>.jsonl` 写下完整的对话流（user/assistant/tool_use 全在里面）。

### 导入

```bash
# 列出所有可导 session（不写文件）
python3 ~/Documents/Claude/brain/.tools/import-chats.py

# 全部导入
python3 ~/Documents/Claude/brain/.tools/import-chats.py --all

# 只导今天的
python3 ~/Documents/Claude/brain/.tools/import-chats.py --since 2026-05-14

# 只导某个 session（前 8 位 uuid）
python3 ~/Documents/Claude/brain/.tools/import-chats.py --session 53552140
```

输出：`chats/code/{YYYY-MM-DD}-{ai-title-slug}.md`，含 frontmatter + 时间戳。

### 增量导入

脚本已有去重——已存在的文件名跳过。可放进 /save skill 末尾让每次会话自动归档。

## web/ · Claude Web 手动导出

Anthropic Web 没暴露本地对话存储。导出有两条路：

### 方式 A · 浏览器复制粘贴

1. claude.ai 打开目标对话 → 右键全选 → 复制
2. 新建 `chats/web/YYYY-MM-DD-{主题}.md`，按 code/ 同样的 frontmatter 写
3. 粘贴对话内容，手动用 `### Doctor` / `### Claude` 分段

### 方式 B · Anthropic Data Export

[claude.ai/settings/data-privacy-controls](https://claude.ai/settings/data-privacy-controls) → "Request data export" → 下载邮件里的 zip → 用 `claude_web_to_md.py` 转（待实现）

## 增量更新建议

在 brain-save skill 末尾追加：
```bash
python3 ~/Documents/Claude/brain/.tools/import-chats.py --since $(date +%Y-%m-%d)
```
这样每次 /save 都会顺手把当天 Code session 归档进 chats/code/。

## GOTCHAS

- jsonl 里有 `tool_use` / `tool_result` 条目——脚本只保留文本，工具调用归约为 `_[使用工具：xxx]_` 占位
- 单个 session 长达数百轮也能处理（验证：本次 247 轮 → 48KB md 文件）
- 标题用 `ai-title` 字段（Claude 自动生成的会话标题）；没有则用 session_id 前 8 位
