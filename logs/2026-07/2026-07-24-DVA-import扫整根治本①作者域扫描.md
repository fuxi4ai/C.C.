---
title: 会话日志 2026-07-24 — DVA import 扫整根治本①（作者域扫描）落地
tags: [log, DVA]
created: 2026-07-24
updated: 2026-07-24
status: active
type: log
project: DVA
---

# 会话日志 — 2026-07-24（import 扫整根治本① · 作者域扫描）

**项目**：DVA
**主题**：告警洪泛治本二选一——Doctor 裁「先①后②分两步」→ ① 采 1a 作者域扫描，改 Mac 源 dva.js（未部署，待 bundle/VV 验）
**承上**：[[2026-07-24-DVA-入口硬化与分析层迁移与旅行模式]]（三桶分级止血段·本次治本承接）

---

## 完成的工作

- **根因精确定位（比 TODO 描述更细）**：`handleImportTranscriptsCommand` 的 `walk(rootDir)` 扫**整个** `TRANS_DIR`；每个字幕文件解析不到 sec_uid 时在 `dva.js:1608` 打 `[无法定位作者]` 告警，而**这一步早于 `secUidFilter` 过滤（1612 行）**——故定时班即便只补一个作者、传了 secUid，全树 630 条跨作者孤儿仍逐条假红。且 harvest 调用点（原 1516 行）把**整根** `TRANS_DIR` 传了进去。
- **① 采 1a（作者域扫描）落 Mac 源**：`Projects/DVA/dva.js` harvest 第 3 步调用点，改为 `path.join(TRANS_DIR, authorName)` 作 import 扫描根，作者目录不存在时兜底退回整根；standalone `dva import-transcripts <dir> [sec_uid]` CLI 不改（整根手动导入保留）。
- **验证**：`node --check` 通过；改动含 4 行中文注释交代根因与兜底/CLI 不受影响。
- **交付物**：Mac 源单文件改动 + brain 仓委托 commit 命令（先探后加）+ DVA 仓 commit 命令（上一轮已给）。

## 做出的决策

| 决策 | 原因 | 影响 |
|------|------|------|
| 治本走「先①后②分两步」 | ①（缩扫描范围）改动小·可逆·止血成本低，先落地；②（孤儿集中裁决）工作量大，留①稳定后另起 | 本次只做①，孤儿依旧在野属已知局限 |
| ① 采 1a 作者域扫描（非 1b 函数内静默 orphan 告警） | 1a 真正「只扫本次作者目录」：噪声归零 + 省整树遍历；1b 保留整树遍历开销、只是静默，不如 1a 干净 | walk 只遍历 `TRANS_DIR/{authorName}/`，630 跨作者孤儿永不被访问 |
| CC 直改 Mac 源（Doctor 二次确认后） | Mac=源码仓（单写切换后 fuxi 为 runtime，源仍在 Mac）；改后经 bundle 部署 fuxi | 改动落 `Projects/DVA/dva.js`，非沙箱 git 写 |

## 遗留问题 / 待办

- [ ] **① 部署链**：重打 bundle → 部署 fuxi → VV 单作者 refill dry-run 验（known_orphan≈0 / other_warnings=0 / exit=0）+ standalone 全根 import 回归照常告警；07-29 那班读数落 known_orphan≈0 即①落地。
- [ ] **DVA 仓提交**：`Projects/DVA/dva.js` 本次改动可并入「DVA 仓最终提交批」或单独提（命令已给·先探后加）。
- [ ] **Codex 镜像同步待裁**：`Codex/Project Mirror/DVA/runtime/dva.js`（07-21 旧镜像）是否同改——若由源码仓单向生成则重生即可，各自维护则需同改。
- [ ] **②（孤儿字幕集中裁决）** 留①稳定后另起：有元数据的 seed 入库 / 无价值进忽略清单（彻底清账·工作量大）。

## 相关笔记

- [[2026-07-24-DVA-入口硬化与分析层迁移与旅行模式]]（三桶分级止血·本次治本承接）
- [[2026-07-24-DVA-fuxi化Phase2至5单写切换完成]]（单写切换·Mac=源码仓前提）
- `Projects/DVA/dva.js` `handleHarvestCommand` 第 3 步调用点（约 1513–1524 行）
- [[DVA/GOTCHAS]] INFRA-20260603-003（扫整根·本次为其治本①）
