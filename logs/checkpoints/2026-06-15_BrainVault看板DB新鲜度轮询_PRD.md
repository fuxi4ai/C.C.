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
  | DVA-视频数据库 | `Database/Douyin/DVA-Database/indexes/watchlist.json` · 信号=**读其中"最近更新时间记录"字段**（非目录 mtime） | 字段**待 Doctor 稍后实现**（现仅有顶层 `updatedAt` + 每作者 `addedAt`，无"最近更新"字段） | 🔒 路径已锁 · ⏳ **依赖 Doctor 落字段后对接** |
  | 白泽大宗-商品数据库 | `Database/宏观-大宗商品/business_breakdown.db`（单文件，非整目录、非 macro_prediction.db）· 信号=文件 mtime | 2026-06-02 21:54（实测陈旧 13 天 · **更新情况 Doctor 从管线侧对接**） | ✅ 已锁（阈值待管线就绪后定） |
  | 剑酒青丘-行情数据库 | `Database/Market-Data/market_data.db`（公共行情主库，句芒维护·日更）· 信号=文件 mtime | 2026-06-15 02:27 | ✅ 已锁 |

**任务规模估算**：
- 预计涉及文件：3 个（`brain/.tools/dashboard-snapshot.py`、`Artifacts/brain-vault-dashboard/index.html`、`Scheduled/refresh-brain-vault-dashboard/SKILL.md`）+ 1 处 cron 配置（经 scheduled-tasks 工具改，非 git）。
- 预计耗时：1–2 小时。
- 涉及项目：Brain Vault Dashboard · Database（只读 4 库 mtime）。

---

## §二 · 交付标准（Acceptance Criteria · 全可验证 · 全留 [ ] 待执行填三态）

### A. 文件层面

- [ ] `dashboard-snapshot.py` 新增读取 4 库新鲜度的函数，并在输出 JSON 顶层新增 `db_freshness` 字段：`Grep "db_freshness" brain/.tools/dashboard-snapshot.py` ≥ 2 matches
  - 证据栏(CC 填)：
- [ ] `index.html` 新增"数据库新鲜度"区块（独立 section + 容器 id，如 `id="db-freshness"`）：`Grep "db-freshness" Artifacts/brain-vault-dashboard/index.html` ≥ 1 match
  - 证据栏(CC 填)：
- [ ] 本 PRD 文件存在于 `brain/logs/checkpoints/2026-06-15_BrainVault看板DB新鲜度轮询_PRD.md`（`ls` 可见）
  - 证据栏(CC 填)：

### B. 一致性层面

- [ ] 快照 JSON 的 `db_freshness` 数组**恰好 4 条**，每条 `name`/`path` 与 §一映射表 Doctor 锁定后的 4 库一致：`python3 dashboard-snapshot.py | python3 -c "import json,sys; d=json.load(sys.stdin); assert len(d['db_freshness'])==4"` 退出码 0
  - 证据栏(CC 填)：
- [ ] 看板渲染的 4 个新鲜度卡片来源于 `db_freshness` 数据（非 HTML 硬编码库名/时间）：`Grep` index.html 中 4 库的"最后更新时间"字符串 = 0 matches（即时间值不写死在 HTML）
  - 证据栏(CC 填)：

### C. 功能层面

- [ ] `python3 brain/.tools/dashboard-snapshot.py` 跑通输出合法 JSON，`db_freshness` 每条含 `{name, path, last_update(ISO8601), age_hours(数值), threshold_hours(数值), stale(bool)}` 六字段：上条断言脚本扩展校验六字段存在，退出码 0
  - 证据栏(CC 填)：
- [ ] 新鲜度信号取自该库路径下数据文件的**最新 mtime**，排除 `.DS_Store`/`.fuse_hidden*`/`*-journal`/`.git/`：脚本内含对应排除逻辑，对 `烛照九阴/recap.db` 输出的 `last_update` = 实测 mtime（±1 分钟）
  - 证据栏(CC 填)：
- [ ] 某库 `age_hours > threshold_hours` 时 `stale=true`，看板该卡片渲染为红色告警样式（复用现有 `.h-critical`/红色 class）
  - 证据栏(CC 填 · 视觉需 Doctor 打开看板确认 → 填 `[~]` 标"Doctor 需测试")：
- [ ] AI 健康简报的 askClaude prompt 输入纳入 `db_freshness`，并要求"对 stale=true 的库点名提醒"：`Grep "db_freshness\|新鲜度\|超期" Artifacts/brain-vault-dashboard/index.html` 命中 prompt 段
  - 证据栏(CC 填)：
- [ ] `refresh-brain-vault-dashboard` 任务调度改为 `0 8,20 * * *`（每日 08:00+20:00）且 enabled：`mcp__scheduled-tasks__list_scheduled_tasks` 显示该 cronExpression
  - 证据栏(CC 填)：
- [ ] `refresh-brain-vault-dashboard/SKILL.md` 的扫描步骤已含"调用 dashboard-snapshot.py 并写回看板新鲜度"：`Grep "db_freshness\|新鲜度" Scheduled/refresh-brain-vault-dashboard/SKILL.md` ≥ 1 match
  - 证据栏(CC 填)：

### D. 自审层面

- [ ] 反偏置：对 4 库的 `stale` 阈值是否合理做一次复核（DVA 当前为 manual·不定期更新，避免设过严导致常红误报）——结论写入 §F 阈值表
  - 证据栏：

### E. 沟通层面

- [ ] /save 已触发 + 落 `brain/logs/`
  - 证据栏：
- [ ] git commit 命令已贴给 Doctor（brain 仓 + 若动 Database 仓；CC 不在 sandbox 跑 git，遵 G-X2；≥2 仓合并成一个 code block 分段连发）
  - 证据栏：
- [ ] 看板 artifact 经 `update_artifact` 更新（非手改挂载文件即算）
  - 证据栏：

### F. 任务专属（自定义）

- [ ] **新鲜度信号定义**落地（**两类信号**）：
  - 证据栏：
  - 类型一·文件 mtime（3 库）：烛照九阴 recap.db / 白泽 business_breakdown.db / 剑酒 market_data.db 取**该文件本体 mtime**；排除清单见 C。
  - 类型二·字段读取（DVA）：从 `Database/Douyin/DVA-Database/indexes/watchlist.json` 读 Doctor 稍后落的"最近更新时间记录"字段（字段名/层级待 Doctor 对接确认）；**字段未就绪前**该卡片显示"待对接/无数据"，**不参与红色告警**（防误报常红）。
- [ ] **每库超期阈值**（`threshold_hours`）写成脚本内可配置常量，采用下列**默认值（待 Doctor 调）**：
  - 证据栏：
  - 提案默认：烛照九阴 recap = **30h**（日更06:00，留缓冲）；剑酒 行情库 = **50h**（交易日更新，覆盖周末）；白泽大宗-商品 = **待定**（Doctor 管线侧对接更新情况后再定，实测现陈旧13天）；DVA = **待 Doctor 字段就绪后定**（当前 manual·不定期，先不报红）
- [ ] 看板新鲜度区块对每库展示：库名 + 最后更新时间 + 距今（如"14h 前"/"13 天前"）+ 健康/超期色块
  - 证据栏：

---

## §三 · 非交付项（范围排除）

- 不包含：brain 知识库本体（.md 笔记）的"快照自动刷新"作为独立诉求——Doctor 仅要 4 库新鲜度（注：refresh 改 2 次/天 cron 会顺带刷新 brain 项目健康度快照，属副产品，不单列为目标，现有项目健康度逻辑不改动）。
- 不包含：外部推送通知（邮件/IM）——Doctor 选"显示+红色告警+AI点名"，未选外部推送。
- 不包含：读取 DB 内部 `max(trade_date)` 等业务级口径校验——本次仅文件 mtime 新鲜度，业务级留待将来。
- 不包含：删除/重构看板现有其他模块（数灵协作板、项目状态、TODO、悬空 wikilink）。
- 不包含：在沙箱跑 git 写命令 / ASR / 下载（遵硬约束，相关命令贴给 Doctor 终端跑）。

**外部依赖（非 CC 本次交付，但影响验收完整度）**：
- **DVA 新鲜度字段**：依赖 Doctor 在 `watchlist.json` 落"最近更新时间记录"字段并告知字段名/层级；未就绪前 DVA 卡片为"待对接"占位、不报红。字段就绪后再做一次小对接（读字段 + 设阈值）。
- **白泽 商品库更新情况**：Doctor 从数据管线侧对接（看板侧只读 business_breakdown.db mtime，被动反映）；白泽阈值待管线节奏明确后再定。

---

## §四 · 状态

- [x] 进行中（立 PRD · 起草稿 · 时间：2026-06-15 10:54）
- [ ] 待 Doctor 验收（CC 已对所有交付标准填三态 · 时间：____）
- [ ] 已交付（Doctor 已把所有 `[?]` 转为 `[✓]` · 时间：____）
- [ ] 已取消（Doctor 显式取消 · 时间：____ · 原因：____）

---

## §五 · 变更记录

- 2026-06-15 10:54 CC：立 PRD 起草稿 · 含 §二 共 16 条交付标准（全留 [ ]）· doctor_decision: 待 · 含 2 处"待 Doctor 锁路径" + 1 处"待 Doctor 调阈值"
- 2026-06-15 11:10 CC：Doctor 锁定 4 库确切路径（白泽=宏观-大宗商品/business_breakdown.db；剑酒=Market-Data/market_data.db；烛照=烛照九阴/recap.db；DVA=Douyin/DVA-Database/）· §一映射表已更新 · 仍待 Doctor 审/改/批 + 调阈值（尤其白泽商品库实测陈旧13天、DVA 当前 manual）
- 2026-06-15 11:20 CC：按 Doctor 反馈修订两处信号源——① DVA 改读 `indexes/watchlist.json` 的"最近更新时间记录"字段（Doctor 稍后落字段，列为外部依赖，未就绪前不报红）；② 白泽更新情况由 Doctor 从管线侧对接，看板侧仅被动读 business_breakdown.db mtime。§一/§F/§三 已同步 · 仍待 Doctor 审/改/批
