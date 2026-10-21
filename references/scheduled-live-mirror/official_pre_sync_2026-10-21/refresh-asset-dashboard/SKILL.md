---
name: refresh-asset-dashboard
description: 重扫并刷新海螺姑娘全局资产看板（survey→重建HTML→update_artifact），日更；挂载已收敛为 Projects+Database 两目录，覆盖 13/14 project
---

刷新「海螺姑娘 · 全局资产管理」看板（global-asset-inventory）。这是"真正的重新扫描"，依次执行三步，全程只读项目、只写 manifest 与看板 HTML，**不在 sandbox 跑任何 git 写命令**：

**前置：挂载 + 路径 env（gateway 平铺挂载 · 见通用教训 G-X45 第三批 + 海螺 GOTCHA-20260708-001）**
- 用 `mcp__cowork__request_cowork_directory` 挂这**两个**目录（`~/Documents` 整挂会被 `Claude/Scheduled` 保护拦截，必须分开挂）：
  - `~/Documents/Claude/Projects`（**一并覆盖 海螺姑娘引擎/manifest 与 Financial/白泽大宗、剑酒青丘、烛照九阴，以及 DVA/PEC/星空/O MY HTML/司南/MiroFish/称象**——2026-08-01 由三目录收敛为两目录，此前逐个挂只覆盖 6/14 个 project）
  - `~/Documents/Database`（公共行情库 + 渊图 mapping 的 health_file 所在）
- **挂好后导出三个 env**。前两个供 `_expand_health_path` 解析 manifest 里 `${VAR}/rest` 占位；第三个 `CONCH_DOCUMENTS_ROOT` 是引擎 `_find_documents_root` 的 ⓪ 优先级——平铺挂载下无真实 Documents 祖先，**缺它则 survey 全跳过 14 个 project 却仍报「✓ 完成」（exit 0），属静默降级，必须避免**：
  ```
  M=<挂载点父目录，形如 /sessions/{session}/mnt>
  export CONCH_DATABASE_MOUNT="$M/Database"
  export CONCH_BAIZE_MOUNT="$M/Projects/Financial/白泽大宗"   # ⚠ 收敛后白泽在 Projects 挂载内，勿再指独立挂载点，指错则白泽新鲜度静默失效
  # CONCH_DOCUMENTS_ROOT 需先搭 symlink shim 根（按 ~/Documents 真实布局链入已挂载目录）：
  # ⚠ shim 根必须落在会话 $HOME，**勿用固定 /tmp 路径**——/tmp 跨会话持久但 uid 每会话轮换，
  #   旧会话残骸对新会话只读，`mkdir -p` 静默成功、到 `ln` 才报 Permission denied
  #   （海螺 GOTCHA-20260729-001，2026-07-30 已复发一次）
  S=$HOME/conch_docs
  rm -rf "$S" 2>/dev/null; mkdir -p "$S/Claude"
  ln -sfn $M/Projects  "$S/Claude/Projects"
  ln -sfn $M/Database  "$S/Database"
  # 会话若还挂了 Brain，也按真实布局链入：ln -sfn $M/Brain "$S/Claude/Brain"
  export CONCH_DOCUMENTS_ROOT="$S"
  ```
  挂载点路径形如 `/sessions/{session}/mnt/Projects`，可用 `ls /sessions/*/mnt/` 现场查。
- ⚠ 沙箱 bash 每次调用独立、env 不跨调用存续：**三个 export 必须分别与 step 1 的 survey 命令、step 2 的 build 命令写进同一个 bash 调用**（两步都要带全）。`$HOME/conch_docs` 路径确定，故 shim 只需在 step 1 搭一次，step 2 重新 export 三个 env 即可、无须重搭。
- 未挂到的项目目录会被 conch 优雅标记 unscannable，不报错；env 未导出则相应 health_file 跳过、不点亮新鲜度（也不污染 status）。**2026-08-01 起看板会给这些节点打「未扫描」灰标 + 页脚计数**，跳过不再隐形——但仍应先修挂载，别让灰标常驻。

1. **全局盘点重写 manifest**：在项目 `Claude/Projects/海螺姑娘/` 下跑
   `python3 conch_engine.py survey --manifest data/asset_manifest.json`
   （遍历项目总览各项目目录做只读盘点 + 读各资产 `health_file` 指向的 `_health.json`，把健康/新鲜度回写 `data/asset_manifest.json`；**纯增量**：obsolete_count 只作信息、绝不自动改策展 status，不臆造 edges）。
   **输出应为「盘点 N≥13 个 project，跳过 1 个」**——14 个 project 中仅「数灵转移」的 path 是字面占位 `Claude/Projects/（待落）`、无实体目录，恒跳过属正常。若报「未能定位 Documents 根目录」、盘点 0 个、或盘点数明显 <13，即前置 env/shim/挂载没带上，修复后重跑，勿带病继续。
   注：survey 会按各节点 `expect_days`（未声明则默认 14 天）判自检产物是否陈旧，超期的 healthy 节点自动降 stale（金光）。这是设计行为，不是故障；若某节点被误判，改 manifest 里它的 `expect_days` 而非关掉规则。

2. **重建看板 HTML**：在 `Claude/Projects/海螺姑娘/dashboard/` 下（同一 bash 调用内带全三个 env）跑
   `python3 build_asset_dashboard.py`
   （把刷新后的 manifest 重新嵌进 `dashboard/asset-dashboard.html`）。建成后必验注入数：
   `grep -o '"update_health"' asset-dashboard.html | wc -l` 应 = 6（**用 `-o` 计次数，勿用 `-c` 计行——内嵌 manifest 为单行，`-c` 恒报 1 造成假警报**）；
   另验 `grep -o '"scanned": true' asset-dashboard.html | wc -l` 应 ≥ 13。任一不达标即视为 build 失败、回查 env，勿以「HTML 生成成功」当成功。

3. **推送到 artifact**：用 `update_artifact` 工具，id=`global-asset-inventory`，html_path 指向 `Claude/Projects/海螺姑娘/dashboard/asset-dashboard.html`，update_summary 写「重扫刷新 · {今天日期}」。

完成后用一两句话回报：各状态分布（healthy / stale / needs_repair / broken 各几个）、有没有节点 overall=fail（即真出问题的库/管线）、有没有节点因自检超期被降 stale（附 age/expect）、以及本轮未扫描项数。若某步失败，如实说明哪步、什么错，不要假装成功。

注：本任务每天自动跑一次，也会被看板上的「🔄 重新扫描」按钮按需触发——两种触发执行内容相同。