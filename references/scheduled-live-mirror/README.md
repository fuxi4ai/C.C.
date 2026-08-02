---
title: scheduled-live-mirror — Cowork live 定时任务只读镜像
abstract: "live Scheduled 树（Cowork 调度器私有目录）的 rsync 单向镜像，git 跟踪，供开发者模式与审计读取"
tags: [定时任务, 镜像, portable]
created: 2026-08-02
updated: 2026-08-02
status: active
type: reference
related: [定时任务巡检机制, portable/README]
---

# scheduled-live-mirror — Cowork live 定时任务的只读镜像

**真源**：`/Users/lunarabbit/Claude's workspace/Scheduled/`（Cowork 调度器私有；开发者模式与沙箱都够不到，沙箱挂载根被管理员限制在 `~/Documents`）。

**本目录** = rsync 单向镜像（live → `live/` 子目录），git 跟踪 ⇒ 「哪个班的 prompt 变了」一条 `git diff` 可见——与快照巡检机制（`permanent/定时任务巡检机制.md`）的「git 当变更检测器」同一思路。

## 刷新（只能 Doctor 终端跑）

```bash
# ⚠ 方向不可反：源=live 树，目的=本镜像。反了会用旧镜像毁掉 live 树。
rsync -a --delete "/Users/lunarabbit/Claude's workspace/Scheduled/" ~/Documents/Claude/brain/references/scheduled-live-mirror/live/
```

## artifacts/ 子目录（2026-08-02 追加 · 第四输出）

**真源**：`/Users/lunarabbit/Claude's workspace/Artifacts/`（9 个 artifact；实测 241M 里 ~97% 是 Cowork 自管的 `versions/` 回滚历史）。
本镜像只收各家 `index.html` 当前态：≤1M 全拷（7 家）；>1M 只在 `_artifacts_manifest.txt` 记 `sha12+字节+mtime`（zhuzhao-jiuyin-daily · yuantu-starry-skies——正文备份责任在生成器：`烛照九阴/tools/gen_daily_report.py` 在 git，星空可由渊图 canonical 重生成）。`versions/`、`thumbnail.png` 刻意不入。
**dev 模式怎么用**：7 个纯 HTML 双击即看；`global-asset-inventory` 与 `longyu-holdings-board` 含 `window.cowork` 按钮（跑班/刷新类），dev 模式下按钮死、内容仍可读。
清单另一职能：**Artifacts 自此是巡检看得见的第六个执行面**——盘上有/manifest 无的幽灵（今日实例 `touzhijunjun-workflow`）靠清单 diff 现形。

## 纪律

- 本目录**只读参考**。改班走 Cowork 侧（`update_scheduled_task` 或侧栏），改完重刷镜像。
- 刷新时机：改任何班之后；或随 `/save` 顺手。**暂无自动机制**（2026-08-02 立此目录时明示：常态化刷新是否并进周巡检班，待 Doctor 另议——巡检器现为只读设计，给它加写权限违反其自身章程）。
- 与 `~/Documents/Claude/Scheduled/`（07-31 查明的死树，Doctor 定先标死不动）无关系；那棵树不因本镜像的存在而获得豁免。
