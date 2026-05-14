---
title: Max 接手包
tags: [handoff, max, implementation]
created: 2026-05-14
updated: 2026-05-14
status: active
type: spec
---

# Brain Vault 实施接手包 — 给 Max

> 你是 CC，Doctor 的知己。本文是你接手 brain vault 后续实施工作的完整说明。
> 读完本文 + `brain/CLAUDE.md` + `brain/references/brain-对接需求-20260514.md`，然后按优先级开干。

---

## 0. 背景（30 秒版）

Doctor 建好了 `~/Documents/Claude/brain/`（Obsidian Zettelkasten + Graphify 架构），
完成了目录骨架、CLAUDE.md、模板、知识种子。
今天的任务：实施 21 条对接需求，让 brain 从"脚手架"变成"真正跑起来的系统"。

---

## 1. 五项已拍板决策（不用再问 Doctor）

| 编号 | 需求 | 决策 |
|------|------|------|
| D1 | REQ-C4 Projects↔brain 关联 | **方案 A**：brain/{项目名}/ 存档案，代码留 Projects/ |
| D2 | REQ-D1 记忆引擎 | **单轨纯文件**，ripgrep 搜索，不上 LanceDB |
| D3 | REQ-G1 Git Remote | **私有 GitHub**（⚠️ 需 Doctor 先建仓库提供 URL）|
| D4 | REQ-F1 锚点触发 | **Cowork Skill**（写 .skill 文件，Doctor 安装）|
| D5 | REQ-A1/A2/A3 命令形态 | **Cowork Skill**（写 .skill 文件，Doctor 安装）|

完整决策背景见 `brain/references/架构决策-20260514.md`。

---

## 2. 实施清单（按优先级）

### P0 · 立即开干（无需等 Doctor）

#### ① REQ-E1 · 项目骨架生成器 `register-project.sh`

写 `brain/.tools/register-project.sh`，传入项目名自动生成：
```
brain/{项目名}/
├── architecture/
│   ├── 系统概览.md     ← frontmatter + 基本信息占位
│   └── 决策记录.md
├── pipeline/
├── data/
├── features/
├── logs/
└── GOTCHAS.md          ← 空文件，含标准格式注释
```
同时在 `brain/CLAUDE.md` 的项目列表表格里追加该项目一行。

#### ② REQ-C4 · 为 6 个项目生成 brain 骨架

渊图已有，对其余 6 个跑 register-project.sh：
`DVA` / `O MY HTML` / `Optical communication` / `司南` / `政治经济学` / `海螺姑娘` / `龙鱼五力`

生成后，从各项目的 README / PRD / GOTCHAS 里提取关键信息，填入 `architecture/系统概览.md`（参考已有的 `brain/渊图/architecture/系统概览.md` 格式）。

各项目源文件位置：
- DVA：`~/Documents/Claude/Projects/DVA/`
- O MY HTML：`~/Documents/Claude/Projects/O MY HTML/`
- 政治经济学：`~/Documents/Claude/Projects/政治经济学/`
- 龙鱼五力：`~/Documents/Claude/Projects/龙鱼五力/`
- 海螺姑娘：`~/Documents/Claude/Projects/海螺姑娘/`
- 司南：`~/Documents/Claude/Projects/司南/`
- Optical communication：`~/Documents/Claude/Projects/Optical communication/`

#### ③ REQ-F2 · 所有 brain 注册项目补齐 GOTCHAS.md

register-project.sh 会自动创建，但渊图/DVA 等已有 brain 目录的项目需手动补：
`brain/渊图/GOTCHAS.md`、`brain/DVA/GOTCHAS.md` 等（如果还没有）。

#### ④ REQ-A1/A2/A3 + REQ-F1 · 写 Skill 文件

在 `brain/.skills/` 目录下创建以下 4 个 skill：

**`brain/.skills/brain-resume/SKILL.md`**
触发：用户说 `/resume` 或"恢复上下文"
行为：
1. 列出 `brain/logs/` 按时间倒序前 3 个文件并全部 Read
2. 如果能识别项目，Read `brain/{项目}/architecture/系统概览.md` 和 `决策记录.md`
3. 输出：上次工作的项目 / 关键决策 / 遗留待办 / 建议下一步（3条）

**`brain/.skills/brain-save/SKILL.md`**
触发：用户说 `/save` 或 `/save [项目名]`
行为：
1. 用 `brain/templates/session-log.md` 模板填充本次会话
2. 写入 `brain/logs/YYYY-MM-DD-{主题}.md`（主题由 CC 从对话中总结）
3. 同一天多次 /save → 文件名加 `-HHmm` 区分
4. 若指明项目，同步更新 `brain/{项目}/architecture/系统概览.md` 的最后工作日期
5. 执行 `git add -A && git commit -m "session: {主题} {date}"` （如果 brain/ 已初始化 git）
6. 回报：日志路径 + 一句话摘要

**`brain/.skills/brain-note/SKILL.md`**
触发：用户说 `/note [主题]`
行为：
1. 用 `brain/templates/default-note.md` 创建 `brain/inbox/{主题}.md`
2. 进入采集态：用户口述，CC 实时整理成结构化笔记
3. 内容成熟时提示："要移入 permanent/ 吗？"

**`brain/.skills/brain-anchors/SKILL.md`**
触发：对话中出现以下关键词
行为：立即停下当前任务，先读完对应文件再继续响应

| 关键词 | 触发读取 |
|--------|---------|
| `dva` / `DVA` | `brain/DVA/architecture/` + `Projects/DVA/CLAUDE.md` + `Projects/DVA/GOTCHAS.md` |
| `龙鱼五力` | `brain/龙鱼五力/architecture/` + `Projects/龙鱼五力/RULES.md` |
| `自检` | `Projects/龙鱼五力/RULES.md` 严格用户视角标准化检查流程 |
| `天工开物` | `Vault/天工开物.md` |
| `渊图` / `行业图谱` | `brain/渊图/architecture/` + `Database/行业研究/CLAUDE.md` |

---

### P0 · 需 Doctor 先操作一步

#### ⑤ REQ-G1 · Git 版本管理

**Doctor 要做：** 在 GitHub 建一个私有仓库（名字随意，建议 `brain`），把仓库 SSH URL 告知 Max。

**Max 收到 URL 后做：**
```bash
cd ~/Documents/Claude/brain
git init
git add -A
git commit -m "init: brain vault 初始化 2026-05-14"
git remote add origin {Doctor 提供的 URL}
git push -u origin main
```
同时在 `brain/.gitignore` 写入：
```
.DS_Store
.index/
graphify/*/cache/
```

---

### P1 · 第二波

- **REQ-B1** `brain/.tools/validate-frontmatter.py` — 扫描所有 .md，检查 frontmatter 完整性
- **REQ-B2** `brain/.tools/build-backlinks.py` — 提取所有 `[[wikilink]]`，生成 `brain/.index/backlinks.json`
- **REQ-B4** `brain/.tools/search.sh` — ripgrep 封装，支持 `-t [tag]` / `-p [project]` / `-k [keyword]`
- **REQ-E2** 项目状态看板 — Cowork HTML Artifact，从 brain/ 读数据展示所有项目状态 + 最后工作日 + TODO 计数

---

### P2 · 第三波（不急）

- REQ-B3 孤儿笔记检测
- REQ-C1 Claude 对话导入管道
- REQ-C3 Graphify 集成（见 brain/TODO.md）
- REQ-G2 iCloud 备份策略

---

## 3. 关键路径文件索引

| 文件 | 用途 |
|------|------|
| `brain/CLAUDE.md` | 全局规则，读这里了解系统 |
| `brain/references/brain-对接需求-20260514.md` | 21条需求完整规格 |
| `brain/references/架构决策-20260514.md` | 5项已拍板决策 |
| `brain/permanent/项目总览.md` | 7个项目当前状态 |
| `brain/permanent/通用教训.md` | 跨项目 GOTCHAS 精华 |
| `brain/TODO.md` | 完整待办清单（含21条需求） |
| `~/Documents/Vault/SKILLS_MANIFEST.md` | Skill 清单 + 重装手册 |

---

## 4. 验收标准（完成后逐条过）

- [ ] `brain/.tools/register-project.sh` 可执行，跑一个项目验证输出结构正确
- [ ] 7个项目全部在 brain/ 有档案目录（含 GOTCHAS.md）
- [ ] `brain/.skills/` 下有 4 个 skill 目录，SKILL.md 内容完整可用
- [ ] `cd brain && git log` 有提交记录（需 Doctor 先建 GitHub repo）
- [ ] 干净 session 说 `/resume`，CC 输出最近工作摘要（需先安装 brain-resume skill）
- [ ] 说 `/save 测试`，`brain/logs/` 出现今日日志

---

建立日期：2026-05-14 | 维护人：Doctor + CC
