---
name: repair-finance-chain
description: 看板星图「审查并修复」按钮触发：诊断金融数据链路断链节点→只跑已知安全幂等修复→破坏性/网络/git 改动只给 Doctor 命令不自动跑
---

你被 Brain Vault Dashboard 星图的「🔧 审查并修复」按钮触发，任务是审查并（在安全边界内）修复「金融线」数据链路里的**断链节点**。每次运行从零开始、无本会话记忆，以下自包含。

## 硬约束（不可违反）
- **不在沙箱跑 git 写命令、不下载视频/媒体、不跑 ASR**。这类操作一律构造命令贴给 Doctor 在 macOS 终端执行。
- **可逆优先 + propose-then-confirm**：任何破坏性/不可逆/改写既有数据的动作，**只诊断 + 给 Doctor 修复命令或方案**，绝不自动执行。
- 只有**已知安全且幂等**的本地修复才可自动跑（见下白名单）。拿不准＝不跑，转交 Doctor。
- 称呼 Doctor 用敬语「您」。

## Step 1 · 审查（诊断哪些库断链 + 根因）
1. 跑 `python3 ~/Documents/Claude/brain/.tools/dashboard-snapshot.py`，从输出 JSON 的 `finance_chain.chains` / `orphan_databases` 里找 `broken=true`（库 stale 或 last_update 缺失）的库。涉及四库：白泽大宗-商品 / 烛照九阴-复盘 / 剑酒青丘-行情 / DVA-视频。
2. 对每个断链库定位根因（读对应项目 GOTCHAS + 实际探查），常见：
   - **白泽大宗-商品**：残留 hot `-journal` → sqlite 只读打开需回滚而回滚要写 → `attempt to write a readonly database`（白泽 GOTCHA-027/028）。库文件在 `~/Documents/Claude/Projects/Financial/白泽大宗/`（具体路径以项目为准）。
   - **烛照九阴-复盘 / 剑酒青丘-行情**：当日行情未拉取/挂载盘 I/O 中断 → 对应 daily 任务 zhuzhao-market-fetch-daily-report / market-data-daily-update 没跑成。
   - **DVA-视频**：常更作者管线没跑（涉及下载+ASR）。

## Step 2 · 修复（仅白名单内自动跑）
**安全幂等修复白名单（可自动执行）：**
- 白泽大宗-商品 hot-journal/只读型断链：跑该项目的 `scripts/database/build_warehouse.py`（已内置「撞 disk I/O/readonly → 拷 /tmp→副本 ingest→残留 journal 截 0→整库 cp 回写」的幂等兜底，仿烛照九阴 /tmp 回写）。跑前先 `integrity_check`；这是非破坏性、可重入的。跑完确认库恢复只读可读。
- 任何只读诊断命令（integrity_check、读 ingest_meta、ls/stat）。

**不可自动、转交 Doctor（构造命令/方案，不执行）：**
- 烛照九阴-复盘 / 剑酒青丘-行情 行情库 stale：给 Doctor「手动补跑对应 daily 任务」的命令或建议在 Scheduled 面板重跑，不在本任务里拉 Tushare/改库。
- DVA-视频：给 Doctor `update-all` 补库命令（`~/Documents/Claude/Projects/DVA/run-update-all.sh`），**不**自动跑（含下载/ASR）。
- 任何需要 git commit/push、删文件、改写历史、或根因不在上述白名单的情形。

## Step 3 · 收尾
1. 若跑了白名单修复，重跑 `dashboard-snapshot.py` 让看板数据刷新（Doctor 回看板点右上 Reload 即见）。
2. 输出一份简报：**诊断**（每个断链库的根因）/ **已自动修复**（做了什么、结果）/ **待 Doctor 处理**（贴好可直接跑的命令 + 一句话理由）。没有断链库则回报「四库均新鲜，无需修复」。