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

- [x] **给渊图跑 graphify**（832 nodes, $9.62）
  `cd ~/Documents/Database/行业研究 && graphify . --obsidian --obsidian-dir ~/Documents/Claude/brain/graphify/渊图`
  （需先确认 graphify 在 PATH：`export PATH="$PATH:~/.local/bin"`）

- [x] **给 DVA 跑 graphify**（1070 nodes, $0.85）
  `cd ~/Documents/Claude/Projects/DVA && graphify . --obsidian --obsidian-dir ~/Documents/Claude/brain/graphify/DVA`

- [x] **政治经济学 G-06 至 G-14 认识论陷阱全量入 brain**（frameworks/陷阱-G-06-G-14.md，9 条全量）
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
- [x] **REQ-G1** brain/ 纳入 git 版本管理（commit c65bf5e → github.com/fuxi4ai/C.C.）

### P1（关键体验）

- [x] **REQ-A3** `/note [主题]` 命令实装 — inbox/ 新建 + 采集态
- [x] **REQ-B1** frontmatter 验证脚本（`brain/.tools/validate-frontmatter.py`）
- [x] **REQ-B2** wikilink 回链索引（`brain/.index/backlinks.json`）
- [x] **REQ-B4** 全文/标签搜索（`brain/.tools/search.sh`）
- [x] **REQ-C1** Claude Code 对话导入（`import-chats.py` → chats/code/）
- [x] **REQ-D1** 记忆引擎决策（已定单轨纯文件 + ripgrep）（双轨文件+LanceDB vs 单轨文件）
- [x] **REQ-E2** 项目状态看板 Artifact（brain-vault-dashboard）
- [x] **REQ-F2** 所有 brain 注册项目补齐 GOTCHAS.md

### P2（锦上添花）

- [x] **REQ-B3** 孤儿笔记检测（`find-orphans.py`）（permanent/ 笔记 wikilink < 2 的标红）
- [x] **REQ-C2** Claude Web/App 手动导出指引（chats/README.md）
- [x] **REQ-C3** Graphify 集成手册（`run-graphify.sh` + references/graphify-集成.md）
- [~] **REQ-D2** 语义检索 API — 搁置（架构决策已排除 LanceDB）
- [x] **REQ-G2** 备份策略（references/备份策略.md + `backup-icloud.sh`）

