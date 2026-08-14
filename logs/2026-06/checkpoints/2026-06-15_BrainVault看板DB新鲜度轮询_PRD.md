---
title: PRD · Brain Vault 看板 · 4 库新鲜度轮询
tags: [prd, acceptance, Brain Vault Dashboard, Database]
created: 2026-06-15 10:54
updated: 2026-06-15 10:54
status: 进行中  # 进行中 / 待验收 / 已交付 / 已取消
doctor_decision: 待  # 待 / 已审 / 已取消
type: prd
project: Brain Vault Dashboard
template_version: v1.0
---

> 本文件为 **起草稿**，待 Doctor 审/改/批。CC 不据此开工、全程不打 `[✓]`、不自动关闭。
> 三态：`[?]` 我认为已达成+证据 / `[!]` 未达成+原因 / `[~]` 不确定+需 Doctor 判断；`[✓]` 只 Doctor 能打。

---

# PRD · Brain Vault 看板 · 4 库新鲜度轮询

## §一 · 任务目标

**动机**：现有 Brain Vault Dashboard 的"心灵健康度"只覆盖 brain vault 内部（项目活跃度分级 + Haiku AI 健康简报），数据靠 🔄 按钮**手动**触发 `refresh-brain-vault-dashboard`（当前 Manual only）。Doctor 名下 4 个真实业务数据库**是否按时被每日/每周管线更新**，目前是监控盲区——管线哪天没跑成、库变陈旧，看板看不出来。本次为看板新增"4 库更新新鲜度巡检"，**每日 2 次**自动巡检并在某库超期未更新时**红色告警 + AI 简报点名**。

**范围**：① 扩展 `dashboard-snapshot.py` 读取 4 库的最新更新时间（新鲜度），输出到快照 JSON；② 看板 `index.html` 新增"数据库新鲜度"卡片区 + 超期红色告警；③ AI 简报输入纳入新鲜度并在超期时点名；④ 把 `refresh-brain-vault-dashboard` 从 Manual 改为 **2 次/天 cron（08:00 + 20:00）**。

**Doctor 原始指令**（逐字引用）：
> "CC，开发需求，AI powered Artifact "Brain Vault Dashboard"需要进化。先记录/更新PRD。需求：除了检查/展示心灵健康度，还要实现"数据库"的更新时间的轮询（2次/天）。"
>
> 对齐追问后 Doctor 点名："我来点名，Documents/Database里面的"白泽大宗-商品数据库"、"剑酒青丘-行情数据库"、"烛照九阴-复盘数据库"、"DVA-视频数据库"，只要这4个的最新更新时间（新鲜度）就好"

**对齐结论摘要**（2026-06-15 经 AskUserQuestion 确认）：
- **轮询对象**：Documents/Database/ 下 4 个库的"最新更新时间（新鲜度）"——仅此 4 个，不含 brain 知识库本体。
- **实现机制**：复用现有 `refresh-brain-vault-dashboard` 任务（不新建独立任务）。
- **告警口径**：显示每库「最后更新 + 距今」；超期标红 + AI 简报点名。
- **轮询时点**：08:00 + 20:00（晨间管线跑完后 + 晚间兜底）。

**关键事实 / 硬约束**（毒舌纪律已摆明）：
- 网页 artifact 关闭即停、打开才跑，**无法自轮询**。"2 次/天"只能落在 scheduled task（cron）上；看板只负责"打开时读取并展示巡检结果"。
- **4 库路径映射**（据 `Database/README.md` 权威指引 + 实地 mtime 核验，2026-06-15）：

  | Doctor 点名 | 真实路径（2026-06-15 Doctor 锁定） | 新鲜度信号(实测最新 mtime) | 状态 |
  |---|---|---|---|
  | 烛照九阴-复盘数据库 | `Database/烛照九阴/recap.db` · 信号=文件 mtime | 2026-06-14 17:50 | ✅ 已锁 |
  | DVA-视频数据库 | `Database/Douyin/DVA-Database/indexes/watchlist.json` · 信号=每作者 **`lastUpdatedAt`**，库级取 enabled 作者的 **max(lastUpdatedAt)** | 字段已补（2026-06-15 03:59）；当前所有 `lastUpdatedAt`=`null`（schema 就绪、尚未首次跑出数据） | ✅ 已锁（逻辑可落地；数据待首次更新跑出非 null） |
  | 白泽大宗-商品数据库 | `Database/宏观-大宗商品/business_breakdown.db` · 信号=`ingest_meta` 表 **max(`last_success_at`)** over sources（非文件 mtime） | ✅ 表已建（6 source，`last_status` 全 ok），最新 `last_success_at`=2026-06-15T12:22:11 | ✅ 已锁（可落地） |
  | 剑酒青丘-行情数据库 | `Database/Market-Data/market_data.db`（公共行情主库，句芒维护·日更）· 信号=文件 mtime | 2026-06-15 02:27 | ✅ 已锁 |

**任务规模估算**：
- 预计涉及文件：3 个（`brain/.tools/dashboard-snapshot.py`、`Artifacts/brain-vault-dashboard/index.html`、`Scheduled/refresh-brain-vault-dashboard/SKILL.md`）+ 1 处 cron 配置（经 scheduled-tasks 工具改，非 git）。
- 预计耗时：1–2 小时。
- 涉及项目：Brain Vault Dashboard · Database（只读 4 库 mtime）。

---

## §二 · 交付标准（Acceptance Criteria · 全可验证 · 全留 [ ] 待执行填三态）

### A. 文件层面

- [?] `dashboard-snapshot.py` 新增读取 4 库新鲜度的函数，并在输出 JSON 顶层新增 `db_freshness` 字段：`Grep "db_freshness" brain/.tools/dashboard-snapshot.py` ≥ 2 matches
  - 证据栏(CC 填)：`grep -c db_freshness = 2`（函数 `db_freshness()` 定义 + main 输出 `"db_freshness": db_freshness(db_root, now_utc)`）。
- [?] `index.html` 新增"数据库新鲜度"区块（独立 section + 容器 id，如 `id="db-freshness"`）：`Grep "db-freshness" Artifacts/brain-vault-dashboard/index.html` ≥ 1 match
  - 证据栏(CC 填)：`grep -c db-freshness = 2`（`<section class="db-section">` 含 `<div class="db-grid" id="db-freshness">` + CSS）。
- [?] 本 PRD 文件存在于 `brain/logs/checkpoints/2026-06-15_BrainVault看板DB新鲜度轮询_PRD.md`（`ls` 可见）
  - 证据栏(CC 填)：`ls` 命中该路径。

### B. 一致性层面

- [?] 快照 JSON 的 `db_freshness` 数组**恰好 4 条**，每条 `name`/`path` 与 §一映射表 Doctor 锁定后的 4 库一致：`python3 dashboard-snapshot.py | python3 -c "...assert len(d['db_freshness'])==4"` 退出码 0
  - 证据栏(CC 填)：全量脚本运行 exit 0；`db_freshness` len=4，names=['烛照九阴-复盘','剑酒青丘-行情','白泽大宗-商品','DVA-视频']，path 与 §一锁定一致。
- [?] 看板渲染的 4 个新鲜度卡片来源于 `db_freshness` 数据（非 HTML 硬编码库名/时间）
  - 证据栏(CC 填)：卡片容器在静态 markup 中为**空**（`grep` 命中 `id="db-freshness"></div>`），4 卡片由 `renderDbFreshness()` 从 `DATA.db_freshness` 动态生成；库名/时间仅存在于数据块 `<script id="snapshot-data">`（设计内的数据源，由 refresh 任务刷新），不写死在展示 markup 中。
  - 说明：若按字面 grep 某时间串会命中数据块 JSON（数据源本身），此为设计预期；"不硬编码"指卡片 markup 不写死，已满足。

### C. 功能层面

- [?] `python3 brain/.tools/dashboard-snapshot.py` 跑通输出合法 JSON，`db_freshness` 每条含 `{name, path, last_update(ISO8601), age_hours, threshold_hours, stale}` 六字段，退出码 0
  - 证据栏(CC 填)：单元测试断言 `need<=set(r)` 对 4 条全通过；实测 last_update 形如 `2026-06-15T01:50:19+08:00`、age_hours 数值、stale 布尔。
- [?] 新鲜度信号按 §F 两类取（mtime 类 2 库 / 库内读取 2 库）：mtime 类排除 `.DS_Store`/`.fuse_hidden*`/`*-journal`/`.git/`（直指单 .db 文件本体，无 journal 干扰），对 `烛照九阴/recap.db` 输出 `last_update` = 实测 mtime（±1 分钟）；库内读取类未就绪输出占位且 `stale=false`
  - 证据栏(CC 填)：recap.db 输出 `2026-06-15T01:50:19+08:00` = `ls` mtime 一致；白泽 ingest_meta 取 max(last_success_at)=`2026-06-15T12:40:12`（detail `6源·6ok`）；DVA `last_update=null`（detail `6作者·未跑`）、`stale=false`。
- [~] 某库 `age_hours > threshold_hours` 时 `stale=true`，看板该卡片渲染红色告警样式
  - 证据栏(CC 填)：**逻辑已验**——脚本 `stale = age_h > threshold_hours`；渲染 `cls = db.stale ? 'stale' : ...`，CSS `.db-card.stale{border-left-color:#dc2626;background:#fef2f2}` + 红 badge 存在。**当前 4 库均未超期/无数据，无现成红色样本**。→ **需 Doctor 打开看板目视确认红色样式**（或等某库真超期时验证）。
- [?] AI 健康简报 askClaude prompt 纳入 `db_freshness` 并要求对 stale=true 点名
  - 证据栏(CC 填)：payload 含 `db_freshness: DATA.db_freshness`（grep=1）；prompt 第 3) 条含 "stale=true（超期未更新）...务必点名提醒"（grep `stale=true`=1），并注明 last_update=null 不报警。
- [?] `refresh-brain-vault-dashboard` 任务调度改为 `0 8,20 * * *`（每日 08:00+20:00）且 enabled
  - 证据栏(CC 填)：`list_scheduled_tasks` 显示该任务 `cronExpression="0 8,20 * * *"`、`enabled=true`、nextRunAt 2026-06-15T12:05Z（=20:05 GMT+8）。
- [?] `refresh-brain-vault-dashboard/SKILL.md` 步骤已含调用 snapshot 并写回新鲜度
  - 证据栏(CC 填)：`grep -cE 'db_freshness|新鲜度' SKILL.md = 4`（描述 + 步骤1 自动包含说明 + 步骤5 报告 stale 库 + 注意条）。

### D. 自审层面

- [?] 反偏置：对 4 库的 `stale` 阈值是否合理做一次复核（DVA 当前为 manual·不定期更新，避免设过严导致常红误报）——结论写入 §F 阈值表
  - 证据栏：已复核。烛照=30h（日更06:00+缓冲）、剑酒=50h（交易日+周末）、白泽=30h（ingest_meta 现日更）、DVA=168h 且 last_update=null 期间一律不报红（脚本 `stale=false`）。代码层兜底：任何缺失/异常/无记录均降级为 `stale=false`，杜绝误报常红。**白泽/剑酒/DVA 阈值仍待 Doctor 按真实管线节奏微调（见 §F 待调标注）**。

### E. 沟通层面

- [~] /save 已触发 + 落 `brain/logs/`
  - 证据栏：待本次交付经 Doctor 验收后触发 /save（按流程在验收节点落盘）。
- [?] git commit 命令已贴给 Doctor（brain 仓；CC 不在 sandbox 跑 git，遵 G-X2）
  - 证据栏：见本次回报末尾 code block（仅 brain 仓：snapshot.py + index.html 副本 + SKILL.md + PRD；Database 仓未改动，无需 commit）。
- [?] 看板 artifact 经 `update_artifact` 更新（非手改挂载文件即算）
  - 证据栏：`mcp__cowork__update_artifact(id=brain-vault-dashboard)` 返回 "Artifact updated"。

### F. 任务专属（自定义）

- [?] **新鲜度信号定义**落地（**两类信号**）：
  - 证据栏：`DB_FRESHNESS_SOURCES` 4 条配置 + `db_freshness()` 实现：mtime 类直 stat 文件本体；ingest_meta 类只读连库取 max(last_success_at)；watchlist 类读 enabled 作者 max(lastUpdatedAt)。单元测试 4 库输出符合预期（见 §二C 证据）。
  - 类型一·文件 mtime（2 库）：烛照九阴 `recap.db` / 剑酒 `market_data.db` 取**该文件本体 mtime**；排除清单见 C。
  - 类型二·库内读取（2 库）：① 白泽——`sqlite3 business_breakdown.db` 读 **`ingest_meta` 表 max(`last_success_at`)** over sources（表已建·可落地；另可把任一 source `last_status`≠ok 透传给 AI 简报）；② DVA——读 `indexes/watchlist.json` 每作者 **`lastUpdatedAt`**，库级取 enabled 作者 **max(lastUpdatedAt)**（字段已就绪；全 null 时显示"尚无更新记录"）。**库内信号全空前**该卡片显示"待对接/无数据"，**不参与红色告警**（防误报常红）。
- [?] **每库超期阈值**（`threshold_hours`）写成脚本内可配置常量，采用下列**默认值（待 Doctor 调）**：
  - 证据栏：`threshold_hours` 已作为每条 source 的常量字段（grep=7）；当前值 烛照30/剑酒50/白泽30/DVA168。
  - 提案默认：烛照九阴 recap = **30h**（日更06:00，留缓冲）；剑酒 行情库 = **50h**（交易日更新，覆盖周末）；白泽大宗-商品 = **30h**（ingest_meta 现为日更·今早 12:22 成功，按日更留缓冲·待 Doctor 确认节奏）；DVA = **168h/7天**（字段已就绪，manual·不定期，全 null 期间不报红）
- [?] 看板新鲜度区块对每库展示：库名 + 最后更新时间 + 距今（如"14h 前"/"13 天前"）+ 健康/超期色块
  - 证据栏：`renderDbFreshness()` 每卡渲染 库名 + badge（✓新鲜/⚠超期/待对接）+ "最后更新：..." + `fmtAge()` 距今（分钟/小时/天）+ 阈值 + detail/path；色块由 `.db-card`/`.stale`/`.nodata` 左边框区分。

---

## §三 · 非交付项（范围排除）

- 不包含：brain 知识库本体（.md 笔记）的"快照自动刷新"作为独立诉求——Doctor 仅要 4 库新鲜度（注：refresh 改 2 次/天 cron 会顺带刷新 brain 项目健康度快照，属副产品，不单列为目标，现有项目健康度逻辑不改动）。
- 不包含：外部推送通知（邮件/IM）——Doctor 选"显示+红色告警+AI点名"，未选外部推送。
- 不包含：读取 DB 内部 `max(trade_date)` 等业务级口径校验——本次仅文件 mtime 新鲜度，业务级留待将来。
- 不包含：删除/重构看板现有其他模块（数灵协作板、项目状态、TODO、悬空 wikilink）。
- 不包含：在沙箱跑 git 写命令 / ASR / 下载（遵硬约束，相关命令贴给 Doctor 终端跑）。

**外部依赖（非 CC 本次交付，但影响验收完整度）**：
- ~~DVA 新鲜度字段~~：✅ **已就绪**（2026-06-15 03:59 Doctor 补 `lastUpdatedAt`）。
- ~~白泽 `ingest_meta` 表~~：✅ **已就绪**（2026-06-15 Doctor 建表，6 source·全 ok·最新 last_success_at 12:22:11）。
- **零外部依赖**：4 库信号源全部锁定可落地，本次可一次实做全部 4 库。

---

## §四 · 状态

- [x] 进行中（立 PRD · 起草稿 · 时间：2026-06-15 10:54）
- [x] 待 Doctor 验收（CC 已对所有交付标准填三态 · 时间：2026-06-15 13:00 · 独立子 agent 复核超时→CC 跑独立验证批次兜底，详见变更记录）
- [ ] 已交付（Doctor 已把所有 `[?]` 转为 `[✓]` · 时间：____）
- [ ] 已取消（Doctor 显式取消 · 时间：____ · 原因：____）

---

## §五 · 变更记录

- 2026-06-15 10:54 CC：立 PRD 起草稿 · 含 §二 共 16 条交付标准（全留 [ ]）· doctor_decision: 待 · 含 2 处"待 Doctor 锁路径" + 1 处"待 Doctor 调阈值"
- 2026-06-15 11:10 CC：Doctor 锁定 4 库确切路径（白泽=宏观-大宗商品/business_breakdown.db；剑酒=Market-Data/market_data.db；烛照=烛照九阴/recap.db；DVA=Douyin/DVA-Database/）· §一映射表已更新 · 仍待 Doctor 审/改/批 + 调阈值（尤其白泽商品库实测陈旧13天、DVA 当前 manual）
- 2026-06-15 11:20 CC：按 Doctor 反馈修订两处信号源——① DVA 改读 `indexes/watchlist.json` 的"最近更新时间记录"字段；② 白泽更新情况由 Doctor 从管线侧对接。§一/§F/§三 已同步 · 仍待 Doctor 审/改/批
- 2026-06-15 11:35 CC：按 Doctor 进一步指令再修订——白泽信号源由"文件 mtime"改为**读 `business_breakdown.db` 的 `ingest_meta` 表最新时间**；DVA 读 watchlist.json **"最近更新"字段**。实盘核验：白泽当前**无 `ingest_meta` 表**（仅 `update_log`，最新 2026-04-11 测试数据）、DVA 当前版本**无"最近更新"字段**——两者均列为待 Doctor 管线就绪后对接，不阻塞烛照/剑酒 2 库落地。§一/§二C/§F/§三 已同步 · 仍待 Doctor 审/改/批
- 2026-06-15 11:45 CC：Doctor 已补 DVA 字段——实盘核验 watchlist.json（2026-06-15 03:59 更新）每作者新增 `lastUpdatedAt` 等 `lastUpdate*` 字段（当前全 null·待首次跑）。DVA 信号锁定为 enabled 作者 max(`lastUpdatedAt`)，本次可落地（数据待首跑）。**外部依赖仅剩白泽 `ingest_meta` 表**。本次可实做 3 库（烛照/剑酒/DVA）+ 白泽占位。§一/§F/§三 已同步 · 仍待 Doctor 审/改/批
- 2026-06-15 13:05 CC：Step 7.5 独立复核——派出的独立子 agent 运行超时（5 次工具调用后 timeout，无终评）。CC 改跑独立验证批次兜底：①全量脚本 exit 0、db_freshness=4 条六字段齐；②recap.db mtime（2026-06-14 17:50 UTC）= 脚本输出 2026-06-15T01:50+08:00 精确一致；③ingest_meta 实存、max(last_success_at)=2026-06-15T12:40:12 与脚本一致；④健壮性：指向不存在库根→4 条全 last_update=None/stale=False/detail"路径缺失"、**不崩**；⑤HTML 元素/JSON/SKILL grep 全过。**唯一留给 Doctor 目视的是 C3 红色样式**（当前无超期样本）。建议：Doctor 可临时把某库阈值调到极小或等真超期，验证红色卡片+AI点名。
- 2026-06-15 13:00 CC：Doctor "开工" → 执行完成。扩 `dashboard-snapshot.py`（+`db_freshness()`+4库配置+时区解析）、看板加新鲜度区块+红色告警+AI点名、refresh 任务改 `0 8,20 * * *`+SKILL 更新、artifact 经 update_artifact 推送。§二 16 条已填三态：14×`[?]`（含证据）+ 2×`[~]`（C3 红色样式需 Doctor 目视 / E1 /save 待验收节点）。§四→待 Doctor 验收。下一步：独立子 agent 复核 → Doctor 终审打 ✓。CC 全程未打 ✓。
- 2026-06-15 11:55 CC：Doctor 已建白泽 `ingest_meta` 表——实盘核验通过（6 source：price_snapshots/stock_scores/fundamentals/crossval/web_probes/proxy_prices，`last_status` 全 ok，最新 `last_success_at`=2026-06-15T12:22:11）。白泽信号锁定为 max(`last_success_at`)。**4 库全部就绪、零外部依赖**，本次可一次实做全部 4 库。§一/§F/§三 已同步 · 仍待 Doctor 审/改/批
