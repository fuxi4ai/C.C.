---
title: consolidate 2026-11-22 · Step 1.5 记忆冲突清单 v1
tags: [consolidate, 记忆治理, checkup]
created: 2026-11-22
updated: 2026-11-22
status: active
type: log
---

# consolidate 2026-11-22 · Step 1.5 冲突清单 v1（每周自动运行 · brain-dream 周日触发）

> 窗口 2026-11-16（上次固化）→ 2026-11-22。全程只读。扫描由一个只读 subagent 执行（实施方），独立复核见文末。行号以 2026-11-22 盘面为准。
> Step 1 盘点：logs 递归 1046 篇（根目录 106）、permanent 54 篇、inbox 5；`find-orphans.py` 健康度 31/53＝58%；`validate-frontmatter.py` 975 件：干净 953、警告 14、错误 8（明细未逐条读，未核）。

## A. 上轮（11-16）K1–K16 现状

K1a/K1b、K2、K3、K5、K6、K7、K8、K9、K11–K16 均已修（11-16 当场 α/β 两批落盘）；K4 已修但有新缺口（M2）；K10 部分修（TODO L307：11-18 晚 Doctor 报已重贴，待 Cowork 新会话逐行对拍）；W1「第 25 个云端班是哪个」仍挂 TODO L323。

## 同错

| # | 事实 | ① 注入层 | ② 记忆正文 | ③ 权威源 | 处置建议 |
|---|---|---|---|---|---|
| M2 | brain-* skill 个数（brain-dream 漏登） | `portable/claude-code/CLAUDE.md:51`「扩至全部 7 个 brain-* skill」 | `permanent/已装skill清单.md:24,78`「7 个」；K 段 `:242` 无 brain-dream；`:244`「dream 🚫已退…由 brain-consolidate 取代」易与新 brain-dream 混淆 | `.skills/_registry.json:11` 有 brain-dream（release/portable）；盘上 `.skills/brain-dream`、`portable/skills/brain-dream`；`_release_ledger.jsonl:60-62`。另 `.skills/README.md:12,22` 仍写 7 个（③ 自身落后） | 按注册表改 8 个；① 逐条列前后原文待批、Doctor 终端同步 `~/.claude/CLAUDE.md`；② 补行并在 :244 注明新旧 dream 不同；README 补登 |

## 陈旧

| # | 落后方 | 权威源 | 改法 |
|---|---|---|---|
| M1（注入层，优先） | `.skills/brain-consolidate/SKILL.md:3` description（portable 同）「绝不自动跑」，每轮技能列表在场 | 同文件正文 `:20` 每周自动运行（2026-11-19 Doctor 裁）；`brain-dream/SKILL.md` | 改 description 为「交互外不落盘；每周由 brain-dream 自动跑到 Step 2 清单即停」；须 ≤1024 字（G-X270）；走发布链（技能改动待 Doctor 批，正文 v1.4 记有 description 冻结约定） |
| M5（低） | portable `:34`「scheduled-tasks 与 Cowork 注册表不是同一处——读到的只是本机班」 | `通用教训.md:4155-4166` G-X275：Code 标签可用 RemoteTrigger 读云端班（只回前 20 条） | ① 补指向 G-X275 的一句 |
| M6 | `logs/2026-11-20-云端定时班四处改班.md:40`「注入层仍缺 5 句，待 Doctor 重贴」 | `permanent/全局偏好-Settings镜像-维护注记.md:99`：11-18 晚 Doctor 报 done、待对拍；TODO L307 | 推断该句沿用 11-18 早的观察；给日志加订正注（需真相层核实观察时点后由 dream 做）；下次 Cowork 新会话对拍 6＋1 处 |
| M7（低） | `维护注记.md:97` 指「brain/CLAUDE.md 数据真实性铁律第 6 条」「portable 金融真实性条」 | `数据真实性铁律.md:25` 为现第 6 条；brain/CLAUDE.md:62 只剩指针；portable 无「金融」 | 带日期注记只加追记 |

## 通则

| # | 通则 | 漏掉/含糊成员 | 处置 |
|---|---|---|---|
| M3 | `通用教训.md:4064-4078` G-X269 Code 标签环境限制成员清单 | G-X275（:4155）、G-X282（:4294）未入 | 按陈旧：补清单 |
| M4 | `Settings镜像.md:26`「不在沙箱跑任何 git 子命令」未限定哪个沙箱；portable `:31`、`动手前卡.md:23` 限定 Cowork 沙箱 | 11-20 DVA 会话据全局块改用 repo_state.py（误读迹象） | **待 Doctor 裁**（方向题：Settings 是否加「Cowork」限定） |

## 待核

- M8 云端班数：`_cloud_trigger_health.json` total 25（11-16 后未再生成）；11-20 新建 brain-dream-daily、11-19 停用 cockpit-snapshot ⇒ 推断现 26 班、启用 25；`TODO.md:128`「24 班启用」、适配卡 `:20`「24 班」陈旧；适配卡未登记 brain-dream-daily。待巡检班重生成 health 文件后与 W1 一并定。

## 一致（核过）

DVA 回流班 06:30 PT 三处一致；dva-mac-2/dva-2 已入 Codex自动化层；风险日报/EAL 迁移路径一致；项目数 19 一致；缺系统概览 4 项目一致；「金融禁止编造」正文一致。

## 编号漂移

通用教训标题式 G-X74–286 共 210 个无重号；粗体区 G-X2 两处为「补」非重号；G-X220 跳号无悬空引用。brain 下 17 份 GOTCHAS 标题 ID 无重号（渊图 001b 为正则误报）。PEC 用 G-NN 命名空间，本次未核。

## 扫描面

查了：portable CLAUDE.md、brain/CLAUDE.md、Settings 镜像与维护注记、brain-anchors/consolidate/dream/save 的 description；已装skill清单、协作偏好、巡检、项目总览、vault 规范、经验库、通用教训 ↔ _registry.json、.skills/README、适配卡、TODO、DVA/Codex 文档。日志细读 3 篇，其余 grep。
未查：`~/.claude/CLAUDE.md` 原件（只读 portable 镜像）；Settings 实际注入块、Cowork MEMORY.md、list_triggers 实况（Cowork 侧）；11-17～11-19 风险日报/conch 日志未逐篇细读；Projects/ 下项目仓 GOTCHAS；数灵 agents/*/memory。

## 独立复核

未参与扫描的 general-purpose subagent（a342a1d5）实读三层复核：**PASS_WITH_LIMITS**。
- 确认：M1、M2（补：:242 链接行无 brain-dream；portable:51 命令列表也漏 /todo）、M3（推断 G-X279 亦为漏成员）、M4、M6、M7、M8 成立。
- 误报/定级修正：M5 应为「一致＋缺指针」而非陈旧（改法不变）；M6 不是推断——`logs/2026-11-20-云端定时班四处改班.md:19` 自述观察来自 11-18 /resume，且同一旧说法重复于 `logs/2026-11-20-DVA回流班…md:40`；M8 另有疑点：`logs/2026-11-20-brain-dream每日班建班.md:21`「list_triggers 翻完 4 页」与 26 班不相容（页长未知），「26 班」不得写成事实。
- 漏检（并入 Step 2）：
  - **N1（陈旧 · 注入层）**：`Settings镜像.md:26` 11-20 新增「提交命令 && 合并」一句（`updated: 2026-11-20`），Cowork 实际注入块未重贴；`维护注记` 最新条只到 11-19，同步纪律断档。Code 侧经 portable:18 直读镜像、不受影响。
  - N2（陈旧 · 低）：`brain-anchors/SKILL.md:3` description 的纪律锚缺「改动面」，正文表有。
  - N3（陈旧 · 低）：`logs/2026-11-19-ElevenLabs语气标签.md:20,32`「少用、每轮 2～3 个」已被同日 `portable:35`、`CC声音档案.md:59,106`「默认用；≤3；≥三成轮次」取代。
  - N4（陈旧 · 低）：`.skills/README.md` 缺 audit、equity-thesis、graphify（注册表有）。
- 限制：`~/.claude/CLAUDE.md` 原件、Settings 实际注入、live list_triggers 不可见；11-17～11-19 风险日报/conch 日志正文只 grep；项目仓 GOTCHAS 与数灵 memory 未查。
