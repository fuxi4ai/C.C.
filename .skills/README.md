---
title: brain/.skills — 4 个 brain skill
tags: [skill, brain, install]
created: 2026-05-14
updated: 2026-05-14
status: active
type: resource
---

# brain/.skills — 4 个 brain skill

## 清单

| Skill | 触发 | 用途 |
|-------|------|------|
| `brain-resume` | `/resume` · "恢复上下文" | 跨 session 拉回工作状态 |
| `brain-save` | `/save [主题]` · "存档" | 落盘会话 + git commit |
| `brain-note` | `/note [主题]` · "起一条笔记" | inbox/ 采集态 |
| `brain-anchors` | `dva` · `龙鱼五力` · `自检` · `天工开物` · `渊图` · ... | 关键词自动加载项目上下文 |

## 设计哲学

**前 3 个独立 skill**（Doctor 习惯用命令收尾）：
- 每个 description 聚焦单一命令，Cowork 路由更准
- 装也独立装，挂也独立挂，互不污染

**brain-anchors 单独**：触发模式是隐式监听（关键词），跟前 3 个 slash 命令逻辑分离。

`_DEPRECATED_brain-commands`：之前合并版的存档，可手动删。

## 安装

### 方式 A · Finder 双击 .skill 文件

打开 Finder，`Cmd + Shift + G` 粘贴：
```
~/Documents/Claude/brain/.skills/
```

依次双击：
- `brain-resume.skill`
- `brain-save.skill`
- `brain-note.skill`
- `brain-anchors.skill`

每次 Cowork 弹"Save skill"对话框，确认。

> ⚠️ APIYI 转接模式下卡片不会弹——切回 Cowork 原生界面再装。

### 方式 B · 终端复制到用户 skill 目录

```bash
mkdir -p ~/Library/Application\ Support/Claude/skills/
cp -r ~/Documents/Claude/brain/.skills/brain-{resume,save,note,anchors} \
       ~/Library/Application\ Support/Claude/skills/
```

重启 Cowork。

## 验证

新开 session，分别试：
- `/resume` 或 "恢复上下文" → 应输出"上次工作/关键决策/遗留待办/建议下一步"
- `/save 测试` → 应在 `brain/logs/` 写出 `YYYY-MM-DD-测试.md`
- `/note 测试想法` → 应在 `brain/inbox/` 起新文件并进入采集态

## 如果 `/save` 这种 slash 形式不响应

Cowork 不一定把 `/{name}` 路由给同名 skill（slash command 和 skill 是两个机制）。
排查路径：
1. **先试中文触发词**："存档今天" / "恢复上下文" / "起一条笔记"——如果这些工作，说明 skill 装了但 slash 路由没生效
2. **改走真正的 slash command**：把 SKILL.md 内容也放一份进 `~/.claude/commands/save.md` 等位置（Claude Code 兼容路径）。这一步需要确认 Cowork 是否支持，待 Doctor 决定后再做

## 清理沙箱遗留

```bash
cd ~/Documents/Claude/brain/.skills/
rm -rf _DEPRECATED_brain-commands _DEPRECATED_brain-commands.skill
```
