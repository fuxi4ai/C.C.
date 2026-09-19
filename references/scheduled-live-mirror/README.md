---
title: scheduled-live-mirror — Cowork live 定时任务只读镜像
abstract: "live Scheduled 树（gateway 调度器私有目录，2026-08-02 自 Cowork 旧根迁入）的 rsync 单向镜像，git 跟踪，供开发者模式与审计读取"
tags: [定时任务, 镜像, portable]
created: 2026-08-02
updated: 2026-09-18
status: active
type: reference
related: [巡检自愈循环-loop-engineering, portable/README]
---

# scheduled-live-mirror — gateway live 定时任务的只读镜像（原 Cowork）

**真源**：`~/Gateway-workspace/Scheduled/`（2026-08-02 自 `/Users/lunarabbit/Claude's workspace/Scheduled/` 迁入，D14；保护跟随 store——开发者模式与沙箱都够不到，沙箱挂载根被管理员限制在 `~/Documents`）。

**本目录** = rsync 单向镜像（live → `live/` 子目录），git 跟踪 ⇒ 「哪个班的 prompt 变了」一条 `git diff` 可见——与巡检治理机制（`permanent/巡检自愈循环-loop-engineering.md` §2）的「git 当变更检测器」同一思路。

## 刷新（只能 Doctor 终端跑）

```bash
# ⚠ 方向不可反：源=live 树，目的=本镜像。反了会用旧镜像毁掉 live 树。
rsync -a --delete ~/Gateway-workspace/Scheduled/ ~/Documents/Claude/brain/references/scheduled-live-mirror/live/
```

## artifacts/ 子目录（2026-08-02 追加 · 第四输出）

**真源**：`~/Gateway-workspace/Artifacts/`（2026-08-17 收敛为 **7 个 artifact**：longyu-holdings-board 并入个股库、touzhijunjun-workflow 无消费点，Doctor 裁不补建；实测 241M 里 ~97% 是 Cowork 自管的 `versions/` 回滚历史）。
本镜像只收各家 `index.html` 当前态：**7 总数＝≤1M 全拷（5 家）+ >1M sha-only（2 家）**；>1M 只在 `_artifacts_manifest.txt` 记 `sha12+字节+mtime`（zhuzhao-jiuyin-daily · yuantu-starry-skies——正文备份责任在生成器：`烛照九阴/tools/gen_daily_report.py` 在 git，星空可由渊图 canonical 重生成）。`versions/`、`thumbnail.png` 刻意不入。
**dev 模式怎么用**：5 个纯 HTML 双击即看；`global-asset-inventory` 含 `window.cowork` 按钮（跑班/刷新类），dev 模式下按钮死、内容仍可读。
清单另一职能：**Artifacts 自此是巡检看得见的第六个执行面**——盘上有/manifest 无的幽灵（今日实例 `touzhijunjun-workflow`）靠清单 diff 现形。

## 纪律

- 本目录**只读参考**。改班走 Cowork 侧（`update_scheduled_task` 或侧栏），改完重刷镜像。
- 刷新时机：改任何班之后；或随 `/save` 顺手；**常态化刷新已并入周巡检班**（2026-08-11 Doctor 裁「巡检＋镜像 rsync 刷新」并班——巡检班只产出 rsync 命令、由 Doctor 终端实跑，巡检器本身仍只读、章程未破；2026-08-02 立此目录时挂的「待 Doctor 另议」由此决议关闭）。
- ⇒ **镜像最多可滞后 store 约 7 天**（2026-09-18 实测实例：`refresh-risk-daily/SKILL.md` 的 store 侧 09-17 更新，直到 09-18 手动刷镜像才回流）。**任何一方读镜像下判断（含 CC 场、审计、staging 起草）前，先按上文命令与 store 对拍 SHA**；对拍不过即镜像滞后，先刷新再动手——否则判断建立在旧文上。
- 与 `~/Documents/Claude/Scheduled/`（07-31 查明的死树，Doctor 定先标死不动）无关系；那棵树不因本镜像的存在而获得豁免。
