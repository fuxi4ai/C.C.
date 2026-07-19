---
title: Brain Vault TODO
tags: [todo]
created: 2026-05-14
updated: 2026-07-07
status: active
type: log
---

# TODO

## 待办

- [ ] **扫一遍还有几个 brain 注册项目缺 `GOTCHAS.md`**（2026-07-19 挂 · 低优先）
  烛照九阴是撞见才发现没有的，REQ-F2 当年标了 `[x]`「所有 brain 注册项目补齐 GOTCHAS」，说明当时可能只漏了它、也可能不止。
  `for d in ~/Documents/Claude/brain/*/; do [ -f "$d/GOTCHAS.md" ] || echo "缺: $d"; done`
  （Doctor 未表态，CC 按「不升 permanent、挂 TODO 即可」的默认处理）

- [x] **重跑 F5 校准取两腿新 lift**（2026-07-19 完成）
  F5 两腿：lift **2.31** / 12 触发日 / **9 独立事件**。同日连修校准工具三处（F4 可评日缺数当未触发、扫描表 lift 基准不同源、判定改卡独立事件数）。

- [ ] **F5 油价腿历史回补**（2026-07-19 挂 · 中优先 · Doctor 批）
  布伦特走 yfinance（**非 tushare**，零积分），现覆盖 20240102 起、可回溯十余年。标签侧创业板指已有 2010 起数据（`AI4ME/回调级别判别/index_research.db` 399006.SZ 3917 日）。
  预期：3% 档现 21 事件 → 扩样本后约 130+ 事件，可把"擦线"变成定论。
  **注意**：这是全表唯一「方向对 + lift>1 + 事件数接近门槛」的格子（3% 档 lift 1.16 / fwd3 −0.78%）；现行 5% 档 lift 2.31 更漂亮但只有 9 事件、fwd3 +0.01%（不跌只是不涨），疑似选在过拟合点。

- [ ] **F4 阈值可达性预检**（2026-07-19 挂 · 低优先 · 回补前必做）
  `200亿` 是绝对阈值。回补 2010+ 之前须先验历史滚动20日募资能否达到该量级——达不到则回补只增"未触发"、事件数不变，等于白干。且期间跨 IPO 暂停（2012–2014/2015）、科创板注册制（2019）、全面注册制（2023）——**跨的是发行制度不是行情**（G-X75）。要补多半得把绝对阈值改成相对值（占流通市值比或滚动分位）。

- [x] ~~F3 tushare 历史回补~~ —— **2026-07-19 取消**（Doctor 批）。正反两方向皆为追认，控制行情后零增量，回补只是把追认结论说得更响。见纪要 §五-C。

- [x] **给渊图跑 graphify**（832 nodes, $9.62）
  `cd ~/Documents/Database/行业研究 && graphify . --obsidian --obsidian-dir ~/Documents/Claude/brain/graphify/渊图`
  （需先确认 graphify 在 PATH：`export PATH="$PATH:~/.local/bin"`）

- [x] **给 DVA 跑 graphify**（1070 nodes, $0.85）
  `cd ~/Documents/Claude/Projects/DVA && graphify . --obsidian --obsidian-dir ~/Documents/Claude/brain/graphify/DVA`

- [x] **PEC G-06 至 G-14 认识论陷阱全量入 brain**（frameworks/陷阱-G-06-G-14.md，9 条全量）
  读取 `Projects/PEC/GOTCHAS.md` 后半部分，提炼入 `brain/PEC/frameworks/认识论框架.md`

## 已完成

- [x] **【G-X13 根治 C】全局偏好 Settings 镜像块合并进桌面端个人偏好**（2026-07-07 · 敬语「您」块已每轮注入生效）
- [x] **【G-X13 补丁 D】`brain-resume` 加 Step 0 读全局偏好镜像**（2026-07-07 · 新 skill 已覆盖安装）
- [x] **【brain-anchors】补召回词「暗色·卡片页 / dark card page / 龙鱼看板」**（2026-07-07）
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

