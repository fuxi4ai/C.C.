---
title: brain/.skills — 2 个 brain skill
tags: [skill, brain, install]
created: 2026-05-14
updated: 2026-05-14
status: active
type: resource
---

# brain/.skills — 2 个 brain skill

## 清单

| Skill | 触发 | 用途 |
|-------|------|------|
| `brain-commands` | `/resume` · `/save` · `/note` | 显式命令套件：恢复 / 存档 / 笔记 |
| `brain-anchors` | `dva` · `龙鱼五力` · `自检` · `天工开物` · `渊图` · `海螺姑娘` · `政治经济学` · `司南` · `O MY HTML` · `光通信` | 关键词自动加载项目上下文（隐式监听） |

## 设计分工

- **显式 / slash 命令** 合并为一个 `brain-commands`——用户主动喊，主题一致
- **隐式 / 关键词监听** 单独留 `brain-anchors`——触发模式根本不同，独立 description 更精准

参考 Cowork 自带 skill：`pdf` 一个 skill 含读/创/合/拆多个子动作，但都属一个主题域。

## 安装

### 方式 A · Finder 双击（推荐）

打开 Finder，按 `Cmd + Shift + G` 粘贴：
```
~/Documents/Claude/brain/.skills/
```

依次双击：
- `brain-commands.skill`
- `brain-anchors.skill`

每次 Cowork 会弹"Save skill"对话框，确认即可。

> ⚠️ APIYI 转接模式下 Save skill 卡片不会弹——切回 Cowork 原生界面再装。

### 方式 B · 终端复制到用户 skill 目录

```bash
mkdir -p ~/Library/Application\ Support/Claude/skills/
cp -r ~/Documents/Claude/brain/.skills/brain-{commands,anchors} \
       ~/Library/Application\ Support/Claude/skills/
```

重启 Cowork 即生效。

## 验证安装

新开一个 session，第一句话说 `/resume`。若 CC 主动读 `~/Documents/Claude/brain/logs/` 并输出"上次工作 / 关键决策 / 遗留待办 / 建议下一步"四段结构 → 装成功。

## 清理沙箱遗留垃圾（Doctor 在 Mac 终端跑一次）

沙箱无法删除合并前的旧文件，请手动清理：
```bash
cd ~/Documents/Claude/brain/.skills/
rm -rf _DEPRECATED_brain-{resume,save,note}{,.skill}
rm -f _TRASH_zi*
```
