---
title: 会话日志 2026-10-21 — 模式切换自检与Gateway-Official适配
tags: [log, 跨项目基建, 司南]
created: 2026-10-21
updated: 2026-10-21
status: active
type: log
project: 跨项目基建
---

# 会话日志 — 2026-10-21

**项目**：跨项目基建（Gateway↔Official 模式切换）× 司南
**主题**：Gateway→官方登录切换自检、差异定位、文件级备份复制、司南适配子项目立卷

---

## 完成的工作

- **/resume 起手**：快照 10-19 新鲜（scheduled）· 修复审计 21 行全 ✅ · Settings 注入零漂移；补登 GOTCHAS `NOTE-20261021-001`（market_signal 空壳 41 个 · ⚠️ 修法待裁）；未闭回执盘点 **79 条**（46 超 3 天）。
- **模式切换自检（Gateway→官方登录可行性）**：四层结论——文件层（brain/Projects/Database/Env）与 Mac 原生层（launchd 9 job+cron 4 条）无缝；配置层（Settings 两壳各一份·官方壳版本未核 / MCP 官方壳缺 MODEL_ID）需补；会话调度层（24 定时班+10 常驻板绑 Gateway 侧）是风险面。Gateway 壳实读：24 班、10 板、store 结构。
- **差异定位（Doctor 确认「不读同一目录」）**：官方侧＝8-02 旧 19 班+9 板（prompt 停在 8-02）；Gateway＝24 班+10 板；官方 config 实读（`coworkUserFilesPath=~/Claude's workspace` · 2 个用户 MCP · 无 `ELEVENLABS_MODEL_ID`）；凭证清单登记 **E-004**（ElevenLabs key 随 config 贴入对话）+ #7 行。
- **历史挖据（Doctor 提示「找默认目录变更」）**：五站沿革——6-30 切 Gateway 善后 / 7-01 切回官方重建 / 7-31 官方默认目录变更致双树分叉 / 8-02/03 数据根迁 Gateway-workspace / 10-21 反向适配；复用 `切环境复原清单` + `回切操作卡`。
- **文件级备份**：影子树归档（7 项死快照 → `_DEPRECATED_DocumentsShadow_20261021`）· 镜像 rsync 刷平 · 双壳 config `.bak_modeswitch_2026-10-21` · artifact manifest 快照落盘 · 官方侧 pre_sync 快照入仓（0615ad6 · 保住官方 `_archived/` 两件）。
- **文件级复制**：rsync Gateway store → 官方 store（exclude `_archived/`+过期一次性班）· **终封 24/24 OK**。
- **git**：brain 3 commit（448d800/e4fadd4/0615ad6）+ 风险日报 2 commit（e365de7/399aa28）全绿 push。
- **司南子项目立卷**：`司南/Gateway-Official适配/Gateway-Official适配.md`（沿革五站+切环境八律+文件真源索引+当前状态）· `司南.md` 入口加行 · 决策记录条目（选 B：文件留真源、只放索引）。
- **经验回灌**：写入延迟 flush 第 3 例追记 documents-mount-quirks memory（git 瞬时干净≠未落盘，延迟可达十几分钟）+ MEMORY.md 索引行更新。

## 做出的决策

| 决策 | 原因 | 影响 |
|------|------|------|
| 切换分两阶段：先定位差异 → 备份+复制+注册 | Doctor 令；文件级动作不激活官方侧 | 命令链按依赖排序：核 enabled → 归档 → 备份 → 复制 → 终封 → 注册 |
| 司南适配文件夹选 B（索引+沿革，文件留真源） | 沿 7-06 订阅分发裁定：搬动=断链+破惯例 | 子项目三件落盘，零断链 |
| rsync exclude `_archived/` + `eal-intraday-patrol-20261015` | 官方侧独有历史件保留；一次性班已过期 | pre_sync 快照兜底；终封全 OK |
| 注册步挂起（待官方订阅） | Doctor：官方订阅还没订，继续 Gateway | TODO 挂账（六步恢复清单）；Gateway 运行面零改动 |
| GOTCHAS 补登走「先核后修」 | 真机 git 瞬时干净疑云 | grep 实核确认在盘，免重复写入 |

## 遗留问题 / 待办

- [ ] 模式切换注册步（官方订阅开通后六步，见 TODO 挂账条）
- [ ] 未闭回执 79 条清账波（10-03 裁定②）
- [ ] 三件 PRD 验收（星空 NE / 股权溢价原子 / 化合物退役）＋ BT-26/27 决策记录勾选（归 Doctor）
- [ ] 风险日报仓收尾 commit（bak 3 件+DS_Store · 命令已贴）
- [ ] GOTCHAS 41 空壳修法待裁 · canonical 漂移对账

## 相关笔记

- [[司南/Gateway-Official适配/Gateway-Official适配]]
- [[切环境复原清单]] · [[回切操作卡]]
- [[凭证清单]] E-004 · [[TODO]] 模式切换挂账条
- 渊图 GOTCHAS NOTE-20261021-001
