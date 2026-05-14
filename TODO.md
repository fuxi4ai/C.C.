---
title: Brain Vault TODO
tags: [todo]
created: 2026-05-14
updated: 2026-05-14
status: active
type: log
---

# TODO

## 待办

- [ ] **给渊图跑 graphify**
  `cd ~/Documents/Database/行业研究 && graphify . --obsidian --obsidian-dir ~/Documents/Claude/brain/graphify/渊图`
  （需先确认 graphify 在 PATH：`export PATH="$PATH:~/.local/bin"`）

- [ ] **给 DVA 跑 graphify**
  `cd ~/Documents/Claude/Projects/DVA && graphify . --obsidian --obsidian-dir ~/Documents/Claude/brain/graphify/DVA`

- [ ] **政治经济学 G-06 至 G-14 认识论陷阱全量入 brain**
  读取 `Projects/政治经济学/GOTCHAS.md` 后半部分，提炼入 `brain/政治经济学/frameworks/认识论框架.md`

## 已完成

- [x] Brain vault 目录结构初始化（2026-05-14）
- [x] graphify v0.7.16 安装（2026-05-14）
- [x] 知识种子：7 个项目 architecture 文件（2026-05-14）
- [x] 通用教训提炼（2026-05-14）

---

## Brain Vault 对接需求（来自 brain-对接需求-20260514.md）

> 完整需求文档：`brain/references/brain-对接需求-20260514.md`

### P0（不做则 brain 不能跑）

- [x] **REQ-A1** `/resume` 命令实装 — 读最近 3 个 log，输出摘要+建议
- [x] **REQ-A2** `/save` 命令实装 — 填模板写 logs/YYYY-MM-DD-主题.md
- [x] **REQ-C4 / REQ-E1** Projects ↔ brain 关联 + 项目骨架生成器 `register-project.sh`
- [x] **REQ-F1** 锚点触发机制（dva / 龙鱼五力 / 自检 / 天工开物 → 自动加载）
- [ ] **REQ-G1** brain/ 纳入 git 版本管理（建私有 GitHub repo）

### P1（关键体验）

- [x] **REQ-A3** `/note [主题]` 命令实装 — inbox/ 新建 + 采集态
- [ ] **REQ-B1** frontmatter 验证脚本（`brain/.tools/validate-frontmatter.py`）
- [ ] **REQ-B2** wikilink 回链索引（`brain/.index/backlinks.json`）
- [ ] **REQ-B4** 全文/标签搜索（最简：ripgrep alias；推荐：Obsidian 已装 → 直接用）
- [ ] **REQ-C1** Claude Code 对话导入 → `chats/code/`
- [x] **REQ-D1** 记忆引擎决策（已定单轨纯文件 + ripgrep）（双轨文件+LanceDB vs 单轨文件）
- [ ] **REQ-E2** 项目状态看板 Artifact
- [x] **REQ-F2** 所有 brain 注册项目补齐 GOTCHAS.md

### P2（锦上添花）

- [ ] **REQ-B3** 孤儿笔记检测（permanent/ 笔记 wikilink < 2 的标红）
- [ ] **REQ-C2** Claude Web/App 对话导入 → `chats/web/`
- [ ] **REQ-C3** Graphify 集成（渊图 + DVA 先跑）
- [ ] **REQ-D2** 语义检索 API（依赖 REQ-D1）
- [ ] **REQ-G2** 备份策略（iCloud + git remote 双保险）

