---
title: consolidate 2026-11-16 · Step 2 拟改动清单 v1
tags: [consolidate, 记忆治理, checkup]
created: 2026-11-16
updated: 2026-11-16
status: active
type: log
---

# consolidate 2026-11-16 · Step 2 拟改动清单 v1

> 依据：[[2026-11-16_consolidate_冲突清单_v2]]（v2.1，两轮独立复核，第二轮 PASS_WITH_LIMITS）＋ 11-06～11-16 共 35 篇日志实读。**本清单未落盘任何改动，等 Doctor 批。**
> 三类门禁：冲突修正＝structural；蒸馏＝permanent（批即质量背书）；GOTCHAS 本轮无新实错需登记。

## 批 α · 冲突修正（陈旧项，有权威源可判）

### α-① 注入层（逐条列前后原文）

**α1 · `brain/portable/claude-code/CLAUDE.md` L34（K1a，随 Q1 裁定定稿）**
- 改前：「Code 标签虽有 `scheduled-tasks` 工具，但与 Cowork 不是同一处（2026-11-06 核：本机并无 `~/.claude/scheduled-tasks/` 目录，原写路径撤）——**读到 0 不代表 Cowork 为空，也不在此建班**，定时与看板推送走 Cowork 侧；」
- 改后（Q1 取推荐时）：「Code 标签的 `scheduled-tasks` 与 Cowork 注册表不是同一处——**读到的只是本机班，不代表 Cowork 为空**；原则上不在此建班，现有一个限期例外 `update-all-tech-reversal-watch`（`~/.claude/scheduled-tasks/` · 2026-11-11 Doctor 批 · 停班条件见 `brain/TODO.md`）；」

**α2 · 同文件 L55（K1b/K2 段首）**
- 改前：「**日常任务在 Code 标签执行；Artifacts（看板）与定时任务由 Cowork 管理。**」
- 改后：「**日常任务在 Code 标签执行；定时任务由 Cowork 管理（本机限期班除外）；看板分两类：托管页（名称带 (Cloud)）由定时班自推、Code 会话可原地更新，侧栏看板由 Cowork 管理。**」

**α3 · 同文件 L57（W1）**
- 改前：「定时任务只在 Cowork 侧跑；24 个班的操作说明镜像在 …」
- 改后：「定时任务在 Cowork 侧（官方云端 trigger）跑，班数以 `brain/permanent/_cloud_trigger_health.json` 为准；操作说明镜像在 …」

**α4 · 同文件 L58（K2）**
- 改前：「Code 标签没有 `update_artifact`：不在此推看板、不用 `publish_files` 另建同名页面；要推时请 Doctor 到 Cowork 交互会话说「补推看板」（队列 …）。」
- 改后：「托管页（登记在 `brain/.tmp/artifact-publish/hosted-pages.json`）按 slug 原地更新（`edit_version` / `publish_files` 带 slug），**不另建同名页面**；侧栏看板（龙鱼个股库、PEC 星空、渊图星空）Code 标签没有 `update_artifact`，要推时请 Doctor 到 Cowork 交互会话说「补推看板」（队列 …）。」
- α1–α4 写 portable 源后，**由 Doctor 在终端 cp 到 `~/.claude/CLAUDE.md`**（沙箱禁写原件）。

**α5 · `brain/CLAUDE.md` L24（K7）**：「实际 18 个项目目录与 `agents/ portable/ …`」→「实际 19 个项目目录与 `agents/ consoles/ portable/ …`」

**α6 · `.skills/brain-anchors/SKILL.md` L78–79（K9，示例句）**：`Projects/龙鱼五力/RULES.md` → `Database/行业研究/consumers/龙鱼五力/RULES.md`（两处）

**α7 · `.skills/brain-resume/SKILL.md` L133（K8）**：「余 **4** 个：MiroFish · 数灵转移 · 星空 · 称象」→「余 **4** 个：MiroFish · 数灵转移 · 称象 · 宏观研究体系（2026-11-16 实核：星空 11-13 已补建）」；`.skills/brain-save/SKILL.md` L179 历史表不改，后加一行 2026-11-16 实核。
- α6/α7 走 skill 发布链：改 canonical → 同步 portable → `skill_release.py release`（只改正文，预计无需上传）。

### α-② 记忆正文与项目文档

| 项 | 文件 | 改法 |
|---|---|---|
| α8（K1b/K2） | `permanent/Doctor协作偏好.md` L219 | 两侧分工条追记「2026-11-11 本机限期班例外」「2026-11-12 看板上云：托管页由班自推、Code 可原地更新；侧栏三块仍 Cowork 手推」，原文保留 |
| α9（K2） | `.skills/console/SKILL.md` L135 | 「不推看板、不建定时班（归 Cowork 侧）」→「侧栏看板与定时班归 Cowork 侧；托管页可原地更新，不新建」（走发布链） |
| α10（K2） | `references/scheduled-live-mirror/官方端适配指令卡-2026-11-04.md` §〇 L34 | 段首加「已由 2026-11-12 看板上云取代（见文末注记）」，原文保留 |
| α11（K2） | `permanent/artifact存储机制.md` | 文首加一段「托管页机制」指针：`hosted-pages.json`、`brain/.tools/artifact_fragment.py`、拆分器、EXP-20261111-002-P/003-T |
| α12（K3） | 协作偏好 L392、L422–425；`科技资讯看板/architecture/系统概览.md` L22 | X-Board 推板链改为 `split_publish.py` v3 → 托管页 X Board (Cloud)；L422 补托管页原地更新 |
| α13（K4） | `permanent/已装skill清单.md` K 段 | gsap 已链；conch 链 `.skills/the-conch-maiden`；补 console、update；`synced/` 登「性质待核」 |
| α14（K5） | `permanent/巡检自愈循环-loop-engineering.md` §9.2、§四执行面表 | §9.2 改现状（Gateway 已停、云端 trigger）；执行面表补「Code 本机班（限期）」 |
| α15（K6） | `permanent/项目总览.md` EAL 行 | 「brain 无目录」→「brain 侧 `宏观研究体系/architecture/决策记录.md`（系统概览缺）」 |
| α16（K11） | 协作偏好 L106 | 追记「2026-11-04 起改为跑 `skill_release.py release`，只传它列出的包；射程＝brain-\* 7 个＋damper＋gsap＋conch（其余见已装skill清单）」，原文保留 |
| α17（K14） | `permanent/动手前卡.md` L23 第 10 条 | 「沙箱不跑任何 git 子命令」→「Cowork 沙箱不跑任何 git 子命令；Code 标签 / Mac 原生可跑只读 git，commit/push 仍交 Doctor 终端」 |
| α18（K15） | `permanent/经验库.md` EXP-20261021-004-P 的 11-15 追记 | 补一句「共管文件模式下回测交 V.V.（2026-11-15/16 两轮做法）」 |
| α19（K16） | `TODO.md` L93 第④项 | 删「推送到手」，注「Doctor 2026-11-10 撤销推送判据（`_repair_audit.md` L392）」 |
| α20（K10） | `TODO.md` L300 | 待重贴 Settings 由 2 句补到 4 句（加备份命名、过期文件命名） |

## 待 Doctor 裁（方向/授权）

- **Q1（K1b）**：Code 本机建班——只登记限期例外（推荐），还是改规则允许 Code 建班。
- **Q2（K12）**：巡检豁免条工具名 `update_scheduled_task` → 云端 `update_trigger`，射程不变（仍只限 `scheduler-weekly-audit` 的 description）。
- **Q3（K13）**：`通用教训.md` 新条位置——brain-save 规则改为「新条按编号平铺追加到文件尾、分类节只放索引」以合实际（推荐），还是保留规则、另开专场按节重排 191 条。与 `TODO.md` L27 合并。
- **W1**：第 25 个云端班是哪个，需 Doctor 在 Cowork 侧 `list_triggers` 取名单；本批 α3 先改成不写裸数。

## 批 β · 蒸馏（permanent，批即质量背书）

| 项 | 要点 | 证据（日志） | 落点 |
|---|---|---|---|
| D1 | 定时班直接读项目工作区，未验收的改动当天就上线；动手前查班表、在副本上改完再放进工作区、接入改动不阻塞构建 | 11-14 风险日报四维度卡 / 烛照隔日关注 / XBoard，11-16 风险日报边际变化（项目级仅风险日报 ERR-20261116-008） | `通用教训.md` 新条，带三项目成员清单 |
| D2 | Code 标签环境限制总条目（G-X263/264/266/267 ＋ `~/.claude.json` 沙箱不可写） | 11-10、11-15×2、11-16×2；G-X264 11-16 复发原因正是按项目召回漏扫 | `通用教训.md` 新总条目，列成员 |
| D3 | 给 Doctor 的终端命令块坑的成员清单（G-X134/229/265/106/154/83/257），并把 11-12「括号包、`; echo exit=$?` 吞退出码」并入 G-X265 | 11-06、11-07、11-12、11-13、11-15、11-16 | `动手前卡.md` 第 10 条扩一行指针 ＋ G-X265 追记 |
| D4 | 派出的审核者/分支越界（删他人文件、curl 绕 robots、越简报改主库）；派工简报逐条列禁手、越界即自报 | 11-10、11-13、11-14、11-15 | G-X236 追记 |
| D5 | V.V. 成果「有价值的参考，不需要盲从，择优录取」（Doctor 11-11 原话） | 11-11、11-14、11-15 | `permanent/跨AI协作握手层.md` 追记 |
| D6 | 巡检周班不以手机推送为验收判据（Doctor 11-10） | `_repair_audit.md` L392 | `巡检自愈循环-loop-engineering.md` 验收判据处补一句 |
| 升格 | G-X211「代理指标冒充判据」（日志标「应升格候选」）；经验库 EXP-20260819-001-T ⑨「skill description ≤1024」同族二次 → 立通用教训；G-X257 状态行由「首次登记」改为已追记 3 次 | 11-10×2、11-15 | 各自原条 |

**另需 Doctor 裁一句（不在本批）**：G-X202「FAIL 两次后停止自行修补」——两次 FAIL 后「换方法继续修」是否合规（11-11、11-14×2 三例）。

## 不动 / 只报

- frontmatter 错误 3：`logs/2026-10/2026-10-08-FCC节后判别-目标文件缺失.md`（历史件）；`logs/2026-11-08-龙鱼双scorer周更.md`、`logs/2026-11-15-龙鱼双scorer周更.md` 由云端周班生成、模板缺字段——根改在班 prompt（Cowork 侧）。
- 孤儿 9 篇均为 `_pre-migration` 与 `_` 开头的机器件，按惯例不动。
- `permanent/通用教训.md.bak_2026-11-13_gx236` 未放 `_bak/`：存量不自动改名，只报。
- 编号漂移：G-X 定义 265 个、引用无悬空；EXP、各项目 GOTCHAS 编号无重复。
