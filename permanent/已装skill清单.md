---
title: 已装 skill 清单
tags: [skill, index, 维护]
created: 2026-06-30
updated: 2026-06-30
status: active
type: permanent
---

# 已装 skill 清单

> 每个工作环境的 skill 目录是独立的，切环境（桌面官方 ↔ gateway ↔ Claude Code CLI）就要重装一遍。此清单是**真源镜像**，决定下次切环境时该补装什么。

---

## A · 自制 brain skills（brain vault 配套，源在 `brain/.skills/`）

| Skill | 触发 | 用途 | .skill 包 |
|-------|------|------|-----------|
| `brain-resume` | `/resume` · "恢复上下文" | 跨 session 拉回工作状态 | ✅ |
| `brain-save` | `/save [主题]` · "存档" | 落盘会话 + 提供 git 命令 | ✅ v2.6 |
| `brain-note` | `/note [主题]` · "起一条笔记" | inbox/ 采集态 | ✅ |
| `brain-anchors` | 关键词监听（dva·龙鱼五力·渊图·白泽…） | 自动加载项目/数灵上下文 | ✅ |
| `brain-prd` | `/prd [任务简称]` · "立PRD" | 开工前对齐 + 起草 PRD | ✅ |
| `brain-consolidate` | `/consolidate` · "固化记忆" | brain 日志蒸馏入 permanent | ✅ |

**已弃用**：`_DEPRECATED_brain-commands`（早期合并版，被前 4 个拆分替代，存档可删）

---

## B · 自制其他 skills

| Skill | 状态 | 备注 |
|-------|------|------|
| `gsap-frontend` | ⚠️ **未在装**（gateway 切换后丢失） | 2026-06-26 基于 greensock/gsap-skills 自制合并版（精简主干 SKILL.md + 5 个 references 渐进披露）。v1 触发词偏激进 + 未跑评测，重做时一并修正。**重做后须落 `brain/.skills/gsap-frontend.skill`** 避免再丢。 |

---

## C · 官方/三方 skills（当前 gateway 环境在装）

**文档处理**：`docx` · `xlsx` · `pptx` · `pdf` · `pdf-reading`

**前端/设计**：`frontend-design` · `design-taste-frontend` · `emil-design-eng` · `impeccable` · `minimalist-ui`

**通用**：
- `consolidate-memory`（Anthropic 自带，针对 `MEMORY.md`；与自制 `brain-consolidate` 共存，brain-consolidate 描述里已声明"取代它"以避免抢戏）
- `full-output-enforcement`（禁默认截断）
- `schedule`（创建/更新定时任务）
- `setup-cowork`（Cowork 初设）

**研究**：`deep-research`

**斜杠命令型**：`init` · `review` · `security-review`

---

## D · 工作环境与 skill 目录映射

| 工作环境 | skill 目录（host 路径） | 备注 |
|----------|------------------------|------|
| **Claude 桌面应用（官方版）** | `~/Library/Application Support/Claude-3p/.../skills/` | bundle id `com.anthropic.claudefordesktop`；不支持自定义 base_url |
| **Gateway 工作环境**（当前） | `~/.claude/skills/`（沙箱挂载在 `/sessions/.../mnt/.claude/skills/`） | 切换 base_url 至 gateway 后 skill 目录另立，**与桌面应用不互通**——只手装过一次的（如 v1 gsap-frontend）会缺失 |
| **Claude Code CLI** | `~/.claude/skills/`（与 gateway 共用） | 走 `ANTHROPIC_BASE_URL` |

**切环境踩坑教训（2026-06-30）**：自制 skill 当时只装在桌面应用、`.skill` 包没落 brain → 切到 gateway 后丢失、源也找不回。**对策**见下条协作偏好。

---

## E · 维护偏好（与 [[Doctor协作偏好]] 同步）

1. **`.skill` 包必落 `brain/.skills/`**：任何自制 skill 一旦定稿，**必须**把目录打成 `.skill`（zip 改名）放到 `brain/.skills/<name>.skill`。这是跨工作环境的**唯一**真源——切环境/换机器只要 brain 在就能一键复装。
2. **改 skill 源后必重打包**：运行时走已装缓存，改源不重装不生效。改完用 `present_files` 把 `.skill` 包贴对话框、Doctor 点 "Save skill" 一键覆盖。
3. **切工作环境后第一件事**：对照本清单 A/B 两栏，把所有自制 skill 重装一遍；C 栏官方 skill 一般跟环境走、不需手动迁。

---

## 相关笔记

- [[Doctor协作偏好]]（升格分拣呈现 + skill 打包安装两条偏好出处）
- [[项目总览]]（数灵/项目 anchor 触发依赖 brain-anchors 在装）
- [[经验库]]（skill 制作的几条 EXP）
- logs/2026-05-14-brain-vault-全面建设.md（4 个 brain skill 立项）
- logs/2026-06-13-开发流程优化-brain-prd与save双增强.md（brain-prd 立 + brain-save 升级）
- logs/2026-06-14-brain-save升级与skill打包偏好.md（v2.6 + "必打 .skill" 偏好沉淀）
- logs/2026-06-26-gsap-frontend-skill制作.md（v1 制作历程与待修订项）
