---
title: 已装 skill 清单
tags: [skill, index, 维护, 真源镜像, 重装手册]
created: 2026-06-30
updated: 2026-07-01
status: active
type: permanent
---

# 已装 skill 清单（真源镜像 + 重装手册 · 唯一真源）

> **本文件是 skill 清单的唯一真源**：既是「切环境该装什么」的真源镜像，也是「备份在哪、怎么装」的重装手册。
> **2026-07-01 合并**：原 `Vault/SKILLS_MANIFEST.md` 已并入本文件（以 brain 为主），那份降为指向本文件的指针，勿再各记一份。
> 状态图例：✅ 已装　⏳ 待装　🚫 本环境不适用（Codex/图生线）。**各环境实时装机状态**以本表「装机」列为准（截至 2026-07-01 官方桌面环境）。

> 每个工作环境的 skill 目录独立，切环境（桌面官方 ↔ gateway/Claude-3p ↔ Claude Code CLI ↔ 换机）就要重装一遍。

---

## A · 自制 brain skills（源 `brain/.skills/`，备份 `Vault/archived/brain/`）

| 装机 | Skill | 触发 | 用途 | 备份 `.skill` |
|:---:|-------|------|------|-----------|
| ✅ | `brain-resume` | `/resume` · "恢复上下文" | 跨 session 拉回工作状态 | `archived/brain/brain-resume.skill` |
| ✅ | `brain-save` | `/save [主题]` · "存档" | 落盘会话 + 提供 git 命令（v2.6，per-agent 归位） | `archived/brain/brain-save.skill` |
| ✅ | `brain-note` | `/note [主题]` · "起一条笔记" | inbox/ 采集态 | `archived/brain/brain-note.skill` |
| ✅ | `brain-anchors` | 关键词监听（dva·龙鱼五力·渊图·白泽…） | 自动加载项目/数灵上下文 | `archived/brain/brain-anchors.skill` |
| ✅ | `brain-prd` | `/prd [任务简称]` · "立PRD" | 开工前对齐 + 起草交付标准 PRD | `archived/brain/brain-prd.skill` |
| ✅ | `brain-consolidate` | `/consolidate` · "固化记忆" | brain 日志蒸馏入 permanent | `archived/brain/brain-consolidate.skill` |

6 个 2026-07-01 官方环境全部重装到位（从现源重打包、frontmatter 引号合规、`brain/.skills/` 镜像同步刷新）。**已弃用**：`_DEPRECATED_brain-commands`（早期合并版，存档可删）。

---

## B · 自制其他 skills（源 `brain/.skills/`）

| 装机 | Skill | 触发 | 用途 | 备份 `.skill` |
|:---:|-------|------|------|-----------|
| ✅ | `gsap-frontend` | 硬专名 "GSAP/gsap/GreenSock" | GSAP 前端动画（主干 + 5 references；粘性生效） | `brain/.skills/gsap-frontend.skill` |
| ⏸ | `handshake-consumer` | 定时/手动 | 方案 B 跨 AI 握手消费端——**方案 B 搁置，暂不装** | `brain/.skills/handshake-consumer.skill` |

`gsap-frontend` 2026-07-01 官方重装（v2.1，基于 greensock/gsap-skills 蒸馏）。

---

## C · 第三方设计线（taste pack · 来源 `github.com/Leonxlnx/taste-skill`，备份 `Vault/archived/taste-skills/`）

Claude Cowork 可用（纯设计指导，不依赖图像生成）：

| 装机 | Skill | 用途 |
|:---:|-------|------|
| ✅ | `design-taste-frontend` | Senior UI/UX 规范，三旋钮系统（DESIGN_VARIANCE/MOTION/DENSITY） |
| ✅ | `minimalist-ui` | Editorial 极简风（金融项目推荐） |
| ✅ | `high-end-visual-design` | 高端 agency 视觉标准（字体/间距/阴影/动画） |
| ✅ | `full-output-enforcement` | 禁默认截断/占位符/偷懒 |
| ✅ | `redesign-existing-projects` | 审计改造现有站点到高端质感 |
| ✅ | `stitch-design-taste` | 为 Google Stitch 产 DESIGN.md 设计系统 |
| ⏳ | `industrial-brutalist-ui` | 野兽派工业风（BETA·**待装**，在 `Vault/taste-skills/`） |

### C-Codex · 图生线 🚫 本 Cowork 环境不适用（2026-07-01 移至 `Vault/Codex/`）

这些依赖 agent **原生图像生成**（GPT/Codex 能力）；Claude Cowork 无图像生成工具、装了空转，故从 taste-skills 分出、独立成 `Vault/Codex/`。要用请到 Codex/GPT 端。同源 `Leonxlnx/taste-skill`。

`gpt-taste`（GPT/Codex 严格变体）· `image-to-code`（含 CODEX-SPECIFIC 段）· `imagegen-frontend-web` · `imagegen-frontend-mobile` · `brandkit`

---

## D · 其他第三方设计 skills

| 装机 | Skill | 来源 / 备份 | 用途 |
|:---:|-------|------|------|
| ✅ | `emil-design-eng` | `github.com/emilkowalski/skill` · `Vault/archived/emil/` | Emil Kowalski 动画/微交互 12 条原则 |
| ✅ | `impeccable` | `Vault/archived/impeccable/` | UI 全面审计/改造（含 23 个 slash 命令） |
| ⏳ | `frontend-design` | 存疑（旧清单列过、无本地源、当前未见） | 待核是否真装过 |

---

## E · 系统级 / 官方 skills（Tier 1 · 跟环境走，本地备份 `Vault/archived/system-skills/`）

理论上 Max/官方账户下自动可用；丢失先从 Settings 面板重启用，再不行从 `Vault/archived/system-skills/` 重装。

**文档**：`docx` · `xlsx` · `pptx` · `pdf` · `pdf-reading`
**通用**：`consolidate-memory`（针对 MEMORY.md，与自制 `brain-consolidate` 共存·后者声明"取代"避免抢戏）· `schedule`（定时任务）· `setup-cowork`（初设）· `skill-creator` · `full-output-enforcement`
**研究**：`deep-research`
**斜杠命令型**：`init` · `review` · `security-review`
**其他备份**：`conch`（`archived/system-skills/conch.skill`，`/conch` 项目整理）

---

## F · 海螺项目内自制 skill（2026-07-01 扫出·本清单原漏记）

源在 `Projects/海螺姑娘/`，**当前未作 Cowork skill 装**——Doctor 决定**先用一用、积累经验再适配**（合 G-X10「规则从失败里长」）。想装先修 frontmatter 引号 + 重打包。

- `conch`（`/conch` 项目维护，有 `Projects/海螺姑娘/conch-v0.2.skill` 包）
- `meditation`（brain 体检，已被 `brain-monthly-checkup` 定时任务直调 `meditation.py`，未必需作 skill）
- `project-review`（关键迭代按 PRD 审代码）

---

## G · 工作环境与 skill 安装机制映射

| 工作环境 | 安装机制 | 备注 |
|----------|---------------|------|
| **Claude 桌面应用（官方版·当前）** | 双击 `.skill` → 系统弹卡片 → "Save skill" → `~/Library/Application Support/Claude/skills/<name>/` | bundle id `com.anthropic.claudefordesktop`；不支持自定义 base_url。**frontmatter 无引号也能装**（比 gateway 宽松，Doctor 2026-07-01 更正） |
| **Cowork / Claude-3p（gateway 模式）** | **Settings → Skills 入口手动选 `.skill`**（plugin 体系）；落内部 plugin 缓存，用户态目录不可见 | 应用本体 `~/Library/Application Support/Claude-3p/skills/` **不扫**；`~/.claude/skills/` 也死路。present_files 卡片不弹 Save 按钮 → 交付附 `open -R` 一键定位 |
| **Claude Code CLI** | `~/.claude/skills/<name>/`（与 gateway 共用文件系统） | 走 `ANTHROPIC_BASE_URL` |

**切环境踩坑教训**：① 2026-06-30 上午：自制 skill 只装桌面、`.skill` 没落 brain → 切 gateway 丢失、源找不回 → 对策：`.skill` 必落 `brain/.skills/`。② 2026-06-30 晚：Cowork 装 skill 非 `~/.claude/skills/` 直放，实测不读；正解 Settings 手动选。

---

## H · 加载约定（避免技能污染）

- **设计项目**（O MY HTML、前端 UI）：按需激活 C/D 栏设计 skills（taste-skills、emil、impeccable）。
- **非设计项目**（DVA、龙鱼五力、渊图、PEC、金融线）：**不激活**设计 skills，保持后端/数据风格。

---

## I · 维护偏好（与 [[Doctor协作偏好]] 同步）

1. **`.skill` 包必落 `brain/.skills/`**：自制 skill 定稿即打成 `.skill`（zip 改名）放 `brain/.skills/<name>.skill`——跨环境唯一真源，brain 在就能一键复装。
2. **改 skill 源后必重打包**：运行时走已装缓存，改源不重装不生效。改完 present_files 交付（gateway 弹不出卡片则让 Doctor 去 Settings 装，附 `open -R`）。
3. **切工作环境后第一件事**：对照本清单逐栏重装自制 skill（A/B）；系统级（E）一般跟环境走。
4. **Cowork frontmatter 范式（gateway 硬约束）**：`name:`/`description:` 值必须 `"..."` 包裹、内部 `"` 转义 `\"`，否则 gateway plugin parser 报 `frontmatter missing name or description`。**官方桌面版无此限**（2026-07-01 Doctor 更正）。详见 [[通用教训]] G-X43 / ERR-20260630-COWORK-FRONTMATTER。

---

## J · 切环境完整重装 SOP

1. 切账户/环境后，试 Tier 1（如对话里试 `/conch`）；不可用则 Settings 重启用，再不行从 `Vault/archived/system-skills/` 重装。
2. 自制 skill（A/B）从 `brain/.skills/` 重装（gateway 走 Settings）；对照本表逐个。
3. 设计线（C/D）按需从 `Vault/archived/taste-skills/`、`Vault/archived/emil|impeccable/` 重装；优先 `impeccable` / `design-taste-frontend` / `full-output-enforcement`。
4. **Codex/图生线在 `Vault/Codex/`——本环境不适用、勿装。**
5. 定时任务 / artifacts 另见 [[切环境复原清单]]（skill 只是其中一类）。

---

## 来源

- **taste-skills/**（设计品味合集）：`github.com/Leonxlnx/taste-skill`
- **emil/**：`github.com/emilkowalski/skill`
- **system-skills/**：Anthropic/Cowork 提供，本地打包备份（2026-05-14）
- **brain/**、**gsap-frontend**、**海螺三 skill**：自制

---

## 相关笔记

- [[切环境复原清单]]（切环境要复原的 5 类总索引，skill 是其一）
- [[Doctor协作偏好]]（skill 打包/安装偏好出处）
- [[通用教训]] G-X43（Cowork frontmatter 范式）
- [[项目总览]]（anchor 触发依赖 brain-anchors 在装）
- logs/2026-06-30-gateway切换善后-skill与artifacts补迁.md（本清单初立 + frontmatter 根因）
- logs/2026-07-01-切回官方-重建定时任务与skill.md（官方环境重装 + Vault 合并）
