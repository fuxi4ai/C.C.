---
title: 会话日志 2026-11-19 — Database conch 审查与收尾（续）
tags: [log, 海螺姑娘, conch, DVA, 龙鱼五力]
created: 2026-11-19
updated: 2026-11-19
status: active
type: log
project: 海螺姑娘（conch）；涉及龙鱼五力、DVA
---

# 会话日志 — 2026-11-19（续）

**项目**：海螺姑娘（conch）；涉及龙鱼五力、DVA
**主题**：首次 /save 之后的收尾——龙鱼库空 `market_data.db` 查源与删除、V.V. 核验回执订正 TODO、`/conch Douyin-2nd`
**前情**：同主题首篇 `logs/2026-11-19-Database-conch审查与收尾.md`（其末节已记 `/conch Douyin-2nd` 的审查经过）。

## 完成的工作

- **龙鱼库 0 字节 `market_data.db`**：Doctor 指出它「像公共数据库」。CC 实测 Python `sqlite3.connect` 与 `sqlite3` 命令行打开不存在的路径都会留下 0 字节文件；龙鱼库代码与班说明镜像没有不带 `../Market-Data/` 的写法；cockpit-snapshot 班说明第 1 步是先 `cd` 到龙鱼库再跑，空文件 mtime 11-18 11:05:17 比 `cockpit.db` 末次写入晚 7 秒。推断为班里代理出简报时以裸文件名临时查库（未证，撤回条件是该次运行记录里查不到）。Doctor 定「给命令删掉」，终端按「是文件且 0 字节」守卫删除并回读。追记于 `龙鱼五力/GOTCHAS.md` ERR-20261119-001（仍 🔄），brain 提交 `eef0c2ce`。
- **V.V. 独立核验回执**（`4AI/Shake hands/to CC/VV致CC-Database登记独立核验与TODO订正-2026-11-19.md`）：CC 只读核对海螺仓本机与远端都是 `a84c539…`、含 `1d17523`、提交时间 19:36:43，据此订正 TODO「Database · conch 收尾」③④，brain 提交 `8bd1cc53`。回执所说「第四个消费方未列名」指 `Database/tools/build_manifest.py`。
- **`/conch Douyin-2nd`**：经过见首篇末节。Doctor 选择框定「挂 TODO 随 DVA 下批改」，目录零改动（复查者差额核验 26 个文件哈希与 mtime 全同），brain 提交 `73c1ad29`。
- **本次 /save 发现并订正 TODO 一处错**：「DVA · 单链接字幕汇总…」第 ② 步原写「重新打包部署到 fuxi（`build_runtime_bundle.py`）」，与 DVA 同日上午的源码归属裁定（生产正本在 Codex `Project Mirror/DVA/runtime/`、V.V. 维护，整包部署已停用，改生产代码走 CC 请求 → Doctor 转达 → V.V. 实施）冲突。已改为：Mac 仓 `harvest-links.js` 由 CC 改；fuxi 线由 CC 写请求、V.V. 改 runtime 副本并部署；两线同一窗口切换。首篇末节里「也打包在 fuxi 线运行」一句描述的是代码现状，部署方式以本条为准。错因：conch 第 1 步第 6 点要求先读项目决策记录，审查时没读 DVA 当日的决策记录。
- **答 Doctor 问**：Douyin-2nd 不是第二个数据库，是 2026-07-25 定位终稿定下的 Mac 单视频本地第二线产物目录；与 `Douyin/`（fuxi 回流镜像，`dva-refresh.sh` 整体刷新）物理分开，免得刷新冲掉；不写 DVA 业务库。2026-08-13 起 fuxi 单视频线开通，`dva-single.sh` 先走 fuxi，此后 Douyin-2nd 只在 fuxi 不可达或 `--force-local` 时新增（推断，未查运行记录）。

## 做出的决策

| 决策 | 原因 | 影响 |
|------|------|------|
| 删除龙鱼库 0 字节空库 | 无消费方、无内容；cockpit-snapshot 已停 | 生成方仍待 Cowork 侧运行记录坐实 |
| Douyin-2nd 命名问题挂 TODO、随 DVA 下批改 | 生成代码两线都在跑，只改 Mac 5 件会新旧混用 | 目录零改动；且被 Codex 三处按原路径使用，不得移动 |

## 遗留问题 / 待办

- 已在 TODO：DVA 单链接字幕汇总改横杠（第 14 行）；Database · conch 收尾（回收站 12-04 期满清理）。
- ERR-20261119-001 生成方待 Cowork 侧 11-18 cockpit-snapshot 运行记录坐实。
- Douyin-2nd 的 5 个视频没有 fuxi 备份；Codex Morning Post 钉了其中一个的 sha256。要不要备份未问 Doctor。

## 相关笔记

- [[通用教训]]
- [[文件健康要素集合]]
