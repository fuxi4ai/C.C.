---
name: "brain-resume"
description: "Restore working context at the start of a session. Trigger when the user types `/resume` or says \"恢复上下文\", \"继续上次\", \"上次干到哪了\", \"接着昨天\". FIRST loads global collaboration preferences (Settings mirror — incl. addressing Doctor as 「您」) to close the G-X13 blind spot, then — if the ElevenLabs voice bridge is available — speaks a short spoken handoff, then reads the most recent 3 session logs from `~/Documents/Claude/brain/logs/`, plus the active project's architecture overview and decisions, then outputs a structured handoff: last project worked on, key decisions, outstanding TODOs, and three suggested next steps."
---

# brain-resume — 恢复跨 session 工作上下文

## 触发

- `/resume`
- "恢复上下文" / "继续上次" / "接着昨天" / "上次干到哪了"

## 执行步骤

### Step 0 · 载入全局协作偏好（每次必做 · 堵 G-X13 盲区）

Cowork / `/resume` 起手**不自动载**全局协作偏好，极易漏「对 Doctor 一律用『您』」等全局规则（G-X13）。所以在做任何事之前，先读一眼镜像并认领：

```bash
cat ~/Documents/Claude/brain/permanent/全局偏好-Settings镜像.md
```

认领其中的全局条后再往下——尤其：**称呼 Doctor 一律用敬语「您」**、改既有资产 propose-then-confirm、可逆优先（不删文件）、不在沙箱跑 git 写命令、需 Doctor 拍板的事走 AskUserQuestion（正文给推荐/不推荐+理由）、不选边不谄媚、裸数字＝实指。
镜像文件缺失则退读 `~/Documents/Claude/brain/permanent/Doctor协作偏好.md`。

### Step 0.5 · 起手开声（语音链路可用则先出一段 · 堵起手哑口盲区）

载完全局偏好后，若 ElevenLabs 桥接可用：**先**按音色 C.C.（voice_id `C7iLuTwlT58pHXVmnmWe` · `eleven_v3` · zh · stability 0.5 · speed 1.0）出一段 ≤150 字口语短版（「已恢复上下文」之类），落 `~/Documents/Claude/.tts-scratch`，再往下做 resume。链路不可用则静默跳过。
语音无后台自动触发器、须每轮主动调 TTS——**起手这一下最易漏**（注意力全在 resume 正文），故在流程里显式固化。

### Step 1 · 读最近 3 篇会话日志

```bash
ls -t ~/Documents/Claude/brain/logs/*.md | head -3
```
把这 3 个文件全文读入。

### Step 2 · 识别活跃项目

从日志的 `project:` frontmatter、文件名主题、或正文中提取最近活跃的项目名（DVA / 龙鱼五力 / 渊图 / O MY HTML / PEC / 海螺姑娘 / 司南）。

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

- `logs/` 为空 → "brain 还没有会话日志。要不要我读 `permanent/项目总览.md` 给您看 8 个项目的整体状态？"
- 识别不到项目 → 只输出全局摘要，问 Doctor 想进入哪个项目
- **不**一次性读项目全部文档——只读 architecture/系统概览/决策记录/GOTCHAS
- 所有路径用绝对 `~/Documents/Claude/brain/...`
- Step 0 全局偏好每次起手必载，不因"上次读过"跳过（会话间不延续）
- resume 起手第一轮默认开声（语音链路可用时）；不可用静默跳过
