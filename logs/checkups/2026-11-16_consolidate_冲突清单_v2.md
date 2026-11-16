---
title: consolidate 2026-11-16 · Step 1.5 记忆冲突清单 v2.1
tags: [consolidate, 记忆治理, checkup]
created: 2026-11-16
updated: 2026-11-16
status: active
type: log
---

# consolidate 2026-11-16 · Step 1.5 冲突清单 v2

> **v2.1（2026-11-16 · 第二轮独立复核 PASS_WITH_LIMITS 后订正）**：「24 个班」挪入待核；K16 改指 TODO L93；K8 不改 brain-save 历史表；K15 降为陈旧·低、改法换补追记；K2 适配卡 §〇 归 ③ 自身陈旧；K13 与 TODO L27 合并。
>
> 窗口：2026-11-06（上次固化）→ 2026-11-16。v1 由 CC 列 3 条（C1–C3），第一轮独立复核判 **FAIL**（C1/C2 定级偏低、漏检 12 项）。本 v2 合并第一轮复核漏检项与日志实读代理的事实变更项；行号以 2026-11-16 盘面为准。全程只读，未改任何被核文件。

## 同错（①② 同口径、与 ③ 冲突）

| # | 事实 | ① 注入层 | ② 记忆正文 | ③ 权威源 | 处置建议 |
|---|---|---|---|---|---|
| K1b | Code 标签是否建定时班 | `~/.claude/CLAUDE.md`＝`portable/claude-code/CLAUDE.md` L34「也不在此建班」、L57「定时任务只在 Cowork 侧跑」 | `permanent/Doctor协作偏好.md` L219「Artifacts（看板）与定时任务由 Cowork 管理」；`.skills/console/SKILL.md` L135「不推看板、不建定时班」 | `TODO.md` L32：Code 本机班 `update-all-tech-reversal-watch` 为 Doctor 选择窗批的「限期例外」；`~/.claude/scheduled-tasks/` 自 11-11 存在 | **方向题，问 Doctor**：只登记限期例外，还是改规则 |
| K2 | Code 标签是否推看板 | 同上 L58「Code 标签没有 update_artifact：不在此推看板…要推时请 Doctor 到 Cowork」 | 协作偏好 L219；console SKILL L135；`permanent/artifact存储机制.md`（06-30，只讲侧栏，托管页机制在 ② 无落点） | `logs/2026-11-12-看板上云-七块迁移与风险日报字体修复.md` 决策表「看板上云…Doctor 裁」；适配卡 L203–256 注记；`.tmp/artifact-publish/hosted-pages.json`「定时班按链接原地更新，不新建」；Code 转录 11-14 两次 `publish_files`（X Board (Cloud)）。**③ 自身陈旧**：适配卡 §〇 L34「看板留 Cowork 推」段首未标被取代 | 改 ①②：托管页（Cloud）由班自推、Code 会话可原地更新，不新建同名页；龙鱼 / PEC 星空 / 渊图星空仍留侧栏、Cowork 手推。后半句「不用 publish_files 另建同名页面」保留 |
| K12 | 巡检豁免的工具名 | `permanent/全局偏好-Settings镜像.md` L101「仅 update_scheduled_task 的 description 参数」 | 协作偏好 L51 同口径 | 适配卡 L87：`scheduler-weekly-audit` 已是云端 trigger，改班走 `update_trigger` | **授权边界，问 Doctor**（危害低：豁免实际失效，不扩权） |

## 陈旧（有唯一落后方）

| # | 落后方（原文） | 权威源 | 改法 |
|---|---|---|---|
| K1a | ① CLAUDE.md L34「本机并无 `~/.claude/scheduled-tasks/` 目录」 | 目录自 11-11 存在 | 删此事实句（随 K1b 一起改） |
| K3 | ② 协作偏好 L392 X-Board 推板链「… → update_artifact → 回读」；L422–425 只写侧栏机制；③ `科技资讯看板/architecture/系统概览.md` L22「→ update_artifact」 | 11-11/12/14 日志：`split_publish.py` v3 → 托管页 X Board (Cloud) | 两处改为现链；L422 补「托管页用 edit_version / publish_files 原地更新」 |
| K4 | ② `permanent/已装skill清单.md` K 段：gsap-frontend「Code 未装」；the-conch-maiden「本地安装」；console、update 漏登；`synced/` 未登 | `ls -l ~/.claude/skills`：gsap 11-13 已链；conch 链 `.skills/the-conch-maiden`（`.skills/README.md` L68）；console/update 已链 `.skills/` | 按盘面改 K 段；`synced/` 性质未核，只登「待核」 |
| K5 | ② `permanent/巡检自愈循环-loop-engineering.md` §9.2「Kimi 壳（主 · 会 fire）」「19 班 enabled」；§四执行面表无 Code 本机班面 | 适配卡 L60「Gateway 24 班已全停，云端已启用」；K1b 本机班 | 改 §9.2 现状；执行面表补「Code 本机班（限期）」 |
| K6 | ② `permanent/项目总览.md` EAL 行「brain 无目录」 | `brain/宏观研究体系/architecture/决策记录.md`（11-06 起，11-16 更新） | 改为指向该目录 |
| K7 | ① `brain/CLAUDE.md` L24「实际 18 个项目目录」；目录清单无 `consoles/` | 盘上 19 个项目目录（多宏观研究体系）；`consoles/` 11-10 新增 | 改 19、补 `consoles/` |
| K8 | skill 正文 `.skills/brain-resume/SKILL.md` L133、`.skills/brain-save/SKILL.md` L179「余 4 个：MiroFish · 数灵转移 · 星空 · 称象」 | 盘面：星空 11-13 已补；宏观研究体系缺 | 只改 brain-resume L133 为 MiroFish · 数灵转移 · 称象 · 宏观研究体系；brain-save L179 是带日期的历史对表，**不改**，另加一行「2026-11-16 实核」（均走 skill 发布链） |
| K9 | ③ `龙鱼五力/architecture/系统概览.md` L49/L52、① `.skills/brain-anchors/SKILL.md` L78–79 示例写 `Projects/龙鱼五力/RULES.md` | 路径不存在；项目总览与概览 L13、anchors L16 为 `Database/行业研究/consumers/龙鱼五力/` | 改为实际路径（anchors 走发布链） |
| K10 | ① Settings 实际注入块比镜像少 4 句（推荐即默认、一轮即止、备份命名、过期文件命名） | `logs/2026-11-14-烛照隔日关注栏美化与两轮复验.md` L22 起手对拍 | Doctor 重贴；`TODO.md` L300 由 2 句补到 4 句 |
| K11 | ② 协作偏好 L106「每次改动任何 skill 的源…打包成 .skill…」（06-14） | `.skills/README.md` L69 薄壳治理（11-04 Doctor 立）、`~/.claude/CLAUDE.md` Skills 节「只改正文不用传」 | 改为「跑 skill_release.py release，只传它列出的包」，并补成员射程 |
| K14 | ② `permanent/动手前卡.md` 第 10 条「沙箱不跑任何 git 子命令」 | 协作偏好 git 条 2026-11-06 递进：Code/Mac 原生只读 git 允许，commit/push 仍交终端 | 补限定语「Cowork 沙箱」+「Code/Mac 原生只读可跑」 |
| K15（陈旧·低） | ② `permanent/经验库.md` EXP-20261021-004-P 的 11-15 追记「第二种模式 · 共管文件」未写回测归属 | 决策记录 L70「回测仍交 V.V.」（限小鲍课件一轮，沿用阿宝稿分工）；「统一」二字是 CC 在 11-15 日志原因列写的，不是 Doctor 原话 | 在 11-15 追记里补一句「共管文件模式下回测交 V.V.（2026-11-15/16 两轮做法）」；不改标题、不写「统一」 |
| K16 | ③ `TODO.md` L93 第④项仍把「`_cloud_trigger_health.json` 出现 · 推送到手」当 scheduler-weekly-audit 的自然证据 | `_repair_audit.md` L392：Doctor 11-10 撤销「收到推送」判据 | 删「推送到手」、注明撤销出处（`巡检自愈循环` 现状版未写此条属缺记录，转蒸馏候选，不算冲突） |

## 对撞（两边都有出处，不自行择一）

| # | 事实 | 甲 | 乙 | 处置 |
|---|---|---|---|---|
| K13 | `通用教训.md` 新条写在哪 | `.skills/brain-save` v3.0「定位到对应 ## 节插入、禁 append 文件尾」 | 文件实际结构：L688 起为平铺 `## [G-X…]`，G-X255–267 均在末尾（11-13、11-15 两篇日志指出口径不一致） | **问 Doctor**；此规则在 skill description（① 注入层），改则逐条列前后原文；与 `TODO.md` L27 已挂的同一裁定合并，不重复挂 |

## 一致（核过，不动）

两份 CLAUDE.md 逐字节相同；`~/CLAUDE.md` ＝ `.tmp/CLAUDE.home.2026-11-06.md`；项目总览 19 行；备份/过期命名三处同口径；Code 朗读音色三处一致；brain/CLAUDE.md 图谱节点数、数灵档案路径、`.tools` 列名均在。

## 待核

| # | 事实 | 三方 | 处置 |
|---|---|---|---|
| W1 | 云端定时班数 | ① CLAUDE.md L57「24 个班」；③ 适配卡 L163「共 24 班」、TODO L93（11-13）「24 个全 enabled」；机器记录 `permanent/_cloud_trigger_health.json`（2026-11-16T04:08Z）`total 25 · enabled 25`，日志 11-06 L53、11-15 L22 写「25 班」 | 第 25 个是哪个班未知（health 不列名，`list_triggers` 只在 Cowork 侧）；先请 Doctor 在 Cowork 取名单再定对撞还是陈旧；本轮 ① 先改为不写裸数、指向 health 文件 |

## 未扫面

Cowork 侧 MEMORY.md（`local-agent-mode-sessions/` 下无记忆索引目录）；各项目 GOTCHAS/决策记录内部互撞（只抽 2 份）；数灵 `agents/*/memory/` 对注入层；Settings 实块原文（只有对拍记录）；Codex automation 现状（无读权）。
