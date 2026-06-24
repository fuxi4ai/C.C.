---
title: 会话日志 2026-06-24 — DVA作者表迁入GAI(L3)·BVD退役·GAI被刷新冲掉后修构建管线治本
tags: [log, 海螺姑娘]
created: 2026-06-24
updated: 2026-06-24
status: active
type: log
project: 海螺姑娘
---

# 会话日志 — 2026-06-24

**项目**：海螺姑娘（Global Asset Inventory）
**主题**：DVA 常更作者表迁入 GAI 作 L3 全屏 modal；BVD 退役（可逆替代）；GAI 被 refresh 管线重建冲掉手工特性 → 修构建管线治本

---

## 完成的工作

### 一 · DVA 常更作者表迁入 GAI（三级）
- 设计方案：L1 DVA-Database 库卡 → L2 详情侧栏 →（点「📖 常更作者表 ›」）L3 全屏暖 modal（承 BVD dva-sheet 宋体范式）。三级=「地图→资产摘要→数据集钻取」，关键是 L3 全屏独立 surface、L2 一键直达，不是层层套娃。
- 实现：manifest 加 `dva_authors[]`（8 作者快照·照搬 BVD）；DVA-Database 节点加**通用钩子** `detail_view:"dva_authors"`（将来 recap.db/market_data.db 可复用）；移植 dva-overlay/sheet CSS + 渲染 JS + 采集总览；openCard 对 detail_view 节点出钻取按钮；Esc/遮罩关闭。

### 二 · BVD 退役（可逆替代）
- Doctor 选「我来删」artifact（CC 无删 artifact 工具）。CC 负责删前安全网：① 归档原件 → `Projects/海螺姑娘/_archive/brain-vault-dashboard_index_20260624.html`（叠加 artifact 自带 versions/ 双保险）；② `refresh-brain-vault-dashboard` 任务 `enabled:false` 暂停（无删任务工具，暂停即可逆）+ 描述标退役；③ 盘点单收尾标各模块去向。

### 三 · GAI 被刷新冲掉 → 修构建管线治本（本会话重点）
- **事故**：Doctor 报「GAI 刷新了一下把数灵刷没了」。诊断：手工特性（数灵/brain/错题本告警/DVA L3）只改在 **artifact 本身**，而 `refresh-asset-dashboard`（每日08:10 + 🔄按钮）从源头管线（`build_asset_dashboard.py` 读 `asset_manifest.json` → 重建 HTML → update_artifact）重建，把手工注入全冲掉。**这正是上一次 /save 标的遗留风险，未及时治本就被冲。**
- **即时恢复**：outputs 工作副本是最新全量、且 manifest status/freshness 与刚 survey 的线上版完全一致 → 直接回推零损失。
- **治本（Doctor 选「现在就修管线」）**：① 验证 `cmd_survey` 只就地改 node 的 status/freshness + 顶层 generated、整体 json.dump 回写——**不重建不删别的字段**，故源 manifest 加 agents/dva_authors/brain 会被保留；② `asset_manifest.json` 源补 agents(4)/agents_note/dva_snapshot/dva_authors(8) + 14 节点 brain + DVA-Database detail_view（从已验证 artifact 合并，只加不动既有 status）；③ `build_asset_dashboard.py` 的 `HTML=r"""…"""` 模板用**已验证 artifact 反推**（剥 cowork-artifact-meta 块、manifest-data 内容换回 `__MANIFEST__` 占位），Python 头/尾不动——避免手抄几十处；④ 沙箱实跑构建→产物含数灵/brain/错题本/DVA L3、JSON/JS 合法、渊图告警在→update_artifact 推管线产物，线上=管线输出闭环。
- 备份：`asset_manifest.json.bak.20260624_pipeline`、`build_asset_dashboard.py.bak.20260624_pipeline`。海螺项目无 git。

## 做出的决策

| 决策 | 理由 |
|------|------|
| DVA 表作 L3 全屏 modal，不塞 L2 侧栏 | 表大·320px 侧栏挤；钻取应独立 surface |
| L3 入口走通用 `detail_view` 钩子 | 将来其他库表级钻取复用同一机制，不为 DVA 特例化 |
| BVD 退役用「归档+暂停」可逆替代，artifact 由 Doctor 删 | CC 无删 artifact/删任务工具；守不删/可逆 |
| GAI 手工特性必须并进构建管线（源+脚本），不能只改 artifact | artifact 是管线**产物**；改产物下次 rebuild 必冲掉 |
| 用已验证 artifact 反推构建模板，而非手抄 | 模板与 artifact 同构；反推零差错、省几十处手改 |
| 先验证 survey 回写保留新字段，再往源加数据 | 若 survey 重建会冲掉，则方案不成立——前置验证 |

## 遗留问题 / 待办

- [ ] 可选：手动触发一次 `refresh-asset-dashboard` 当场验证刷新后数灵仍在（否则等明早 08:10）。
- [ ] brain 计数口径统一接进 survey/refresh（去掉「6 项未跟踪 + 沿用 BVD 值」临时态，治本回填）。
- [ ] BVD artifact 待 Doctor 在 Cowork 界面删除（原件已归档·可逆）。
- [ ] artifact 的 description/meta 由 refresh 任务的 update_artifact 管理，本次手设的描述可能被刷新重置——非阻塞。

## 相关笔记

- [[海螺姑娘]] · `Artifacts/global-asset-inventory/index.html` · `dashboard/build_asset_dashboard.py` · `data/asset_manifest.json`
- `Projects/海螺姑娘/BVD退役盘点单_20260624.md`
- 前序：[[2026-06-24-GAI并入BVD数灵与错题本告警]]
