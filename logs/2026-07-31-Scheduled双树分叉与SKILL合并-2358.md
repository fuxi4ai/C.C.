---
title: 会话日志 2026-07-31 — Scheduled 双树分叉 · 两份 SKILL 合并 · DeepSeek 模型选型
tags: [log, 烛照九阴, 白泽大宗, brain, 剑酒青丘]
created: 2026-07-31
updated: 2026-07-31
status: active
type: log
project: 烛照九阴 / 白泽大宗 / brain（跨）
---

# 会话日志 — 2026-07-31（第三场 · 沙箱 09:37–23:58 PDT）

**项目**：烛照九阴 ＋ 白泽大宗 ＋ brain ＋ 剑酒青丘
**主题**：DeepSeek 模型选型（切 flash → 查明无需切 → 回 pro）→ 处理待办撞上 **`~/Claude's workspace/` 与 `~/Documents/Claude/` 两棵 Scheduled 树分叉**，07-30 的 SKILL 改动全落在死树上

> **⚠ 日期口径**：文件名与 frontmatter 用**沙箱本地（美西 PDT）07-31**。同日第三篇，故加 `-2358`。

---

## 完成的工作

### 一 · DeepSeek 模型选型 —— 查明「必须换」的前提不成立

- **起点**：Doctor 转来 DeepSeek 文档「Responses API 仅支持 `deepseek-v4-flash`，`pro` 待 2026-08 初」，要求改 env 里的模型。
- **第一个发现：模型型号根本不在 env 里**。`Database/.env` 只有 `KG_API_KEY`，**没有 `KG_MODEL`**；型号散在脚本硬编码默认值。而且两条链行为不一致——`extract_factor.py` 经 `config.load_env` 读 `.env`（**能配**），`weekly_local_prep.sh` **只 grep `KG_API_KEY`、不读 `KG_MODEL`**（**配了也不生效**），可 `docs/WORKFLOW_周报自动化.md` L55 却写着「如需改在 .env 里设」——**那句一直是空头支票**。
- **第二个发现：那条限制不管我们**。官方文档（`api-docs.deepseek.com/guides/responses_api`）证实：DeepSeek 有**三条并列的路**——`/chat/completions`（OpenAI 兼容）· `/anthropic/v1/messages`（**本项目走这条**）· `/responses`（**为 Codex 而设**，「仅 flash」写在它自己那一篇顶部）。侧栏里 Responses 与 Anthropic 是两篇独立 guide。
- **三组探针实测**（`scripts/automation/probe_deepseek_model.py`，照生产请求体构造，Doctor 终端跑）：

  | 组 | 模型 | `thinking` | 结果 | `content` 类型 | in/out |
  |---|---|---|---|---|---|
  | A | flash | `disabled` | ✅ 1.27s | `['text']` | 12/1 |
  | B | flash | 不传 | ✅ 1.39s | **`['thinking','text']`** | **91/16** |
  | C | **pro** | `disabled` | ✅ 1.26s | `['text']` | 12/1 |

- **C ✅ ⇒ pro 在 Anthropic 兼容端点仍可用，「被迫迁移」不成立**。Doctor 遂定**改回 pro**（理由：8 月初 pro 就回 Responses 了，注释与兜底都别动，只让 `.env` 成为唯一切换点）。
- **B 推翻了我自己的预设**：我原写的分支是「A❌/B✅ ⇒ `thinking` 参数是雷，`call_deepseek` 判据要由『base_url 含 deepseek』收窄为『且 model 含 pro』」。实测 flash **也吐 `thinking` 块** ⇒ **判据不但不该收窄、现在这个写法正好对**。若按直觉去「优化」，等于给 flash 关掉补丁、单票打回 45s 撞沙箱上限。
- **落地**：`weekly_local_prep.sh` 补三档取值（环境变量 → `.env` → 内置兜底 `deepseek-v4-pro`，`bash -n` 通过 + 三档模拟实测）；`.env` 加 `KG_MODEL=deepseek-v4-pro`（Doctor 终端）；`白泽大宗/GOTCHAS.md` **GOTCHA-023 追记**（flash 同为推理模型、勿收窄判据、thinking 的 token 代价首次量化 7.6×、Responses vs Anthropic 端点澄清）。**注释与文档一律不动**（Doctor 定：pro 要回来了）。

### 二 · `us-close-backfill` 首跑核验 —— 跑了，零写入

- `lastRunAt` 由「字段不存在」变为 `2026-07-31T20:34:45Z`（＝13:34 PDT，准点）⇒ **首跑确实发生了**。
- 但库里查不到它的任何一行：`us_anchor_daily` 07-31 **0 行**；`intl_index_daily` 07-31 只有 5 行且**全是读数语义腿**（futures/macro/kr），`us_stock` 与 `overnight` **各 0**。07-27~07-30 全部行 `updated_at` 都是 `17:04:xx UTC`＝**10:04 PDT 主班 zhuzhao** 写的，**无一行落在 20:34 UTC**。
- 直接后果：`US10Y` 07-31 库里是 **4.74**，写于 13:04 ET（**美股未收盘的盘中快照**），backfill 本该在 16:34 ET 用真收盘覆盖，没覆盖。
- **最可能的原因（已证一半）**：该 SKILL 前置只有 `cd ~/Documents/Claude/Projects/Financial/烛照九阴 2>/dev/null || cd /mnt/烛照九阴` 两个硬编码候选，**在当前沙箱形态下都不存在**（实测 `HOME=/sessions/{sess}`，真实路径是 `$HOME/mnt/Documents/...`）。对照 `zhuzhao` 的 live SKILL **有完整挂载探测段**（`ls -d /sessions/*/mnt/*/` 先探再用）——有探测的活着，没探测的一进门就摔。**未证**：跑班 agent 是否自行恢复；决定性证据是首跑简报（未取到）。

### 三 · ★ 发现两棵 Scheduled 树，07-30 的改动全落在死树上

- **起因**：想读 `us-close-backfill` 的 SKILL，发现 `list_scheduled_tasks` 给的路径是 **`~/Claude's workspace/Scheduled/`**，而沙箱只挂 `~/Documents` ⇒ **CC 够不到 live 树**。
- **`readlink -f` 两边不同 ⇒ 真·两棵独立的树**，非软链：

  | | `~/Claude's workspace/Scheduled/` | `~/Documents/Claude/Scheduled/` |
  |---|---|---|
  | 目录数 | **20**（含 `_archived`） | 14 |
  | 调度器读 | ✅ | ✗ |
  | 仅此侧有 | 8 个班 | **0 个** |

- **决定性测试**（用 07-30 日志记的具体改动去 grep）：

  | | live 树 | Documents 树 |
  |---|---|---|
  | `5f`（zhuzhao 终检步） | **0** | 2 |
  | `ingest-check`（review 初检） | **0** | 2 |
  | SKILL.md mtime | **07-30 06:02** | 07-30 22:32 / 22:33 |

  ⇒ **07-30 晚上那次 SKILL 改动，从来没进过生产。**
- **脚本侧与 SKILL 侧的分离证据**：`_health.json` 里 `phase` 与 `db_mtime_at_check` 两个字段**都在**（`recap_health.py` 在 `Projects/` 下、真路径，改动生效），但 `phase` **恒为 `"manual"`**——因为 live 班里没有 5f，永远产不出 `eod-final`。**一个改动，脚本那半落地、SKILL 那半蒸发。**
  - 且该文件此刻正在自证过期：`generated 07-31T09:39`、`db_mtime_at_check 07-30T22:02`，而 `recap.db` 实际 mtime 已是 **07-31 10:06** ⇒ 报告已被后续写库作废。**这正是 07-30 加那个字段要检测的情形，字段生效了。**
- **全量盘点**（6 个班两边内容不同 · 8 个仅 live 有 · **0 个仅 Documents 有**）：
  - **改动落在死树的 3 个**：`baize-weekly-report`（Documents 07-09 · 比 live 新 **22 天**）· `recap-kejian-review`（07-30）· `zhuzhao-market-fetch-daily-report`（07-30）
  - **Documents 侧陈旧、无害的 3 个**：`market-data-daily-update` · `recap-kejian-daily-ingest` · `refresh-asset-dashboard`
- **`zhuzhao` 是真·双向分叉，绝不能单向覆盖**：live 独有「`T_anchor` 数据驱动锚点（07-14 时钟偏移根治）· us_anchor `--source yahoo` 转正（07-28）· 副本根当班唯一名（G-20260728-001）· 副本根四件套（G-20260728-002）· G-X51 无人值守绝不 request · echarts 已内联」；Documents 独有「5f 终检 · margin 五表 · guarantee_ratio」。**按 Documents 覆盖会一次性回退掉 07-14 与 07-28 的全部根因修复。**

### 四 · 合并并安装两份干净的 SKILL

- **`recap-kejian-review`**（33 行）：① `--phase=ingest-check` ＋ 初检/终检分层说明；② 07-30 病例块 ＋ `db_mtime_at_check` 用法；③ **时刻订正** `15:30→09:30`（本班）· `16:00→10:00`（zhuzhao）· `06:00→09:00`（ingest），并加口径注。
  - **③ 是本场额外查出的**：Documents 那版写的钟点是 **07-30 cron 整体 −6h 之前的旧时刻**，改 SKILL 的人没跟着改。自洽性佐证：文中病例说「`_health.json` 生成于 09:41」，正是 09:30 班加抖动的时间——**班早就在 09:30 跑了，只有文字停在 15:30**。
- **`baize-weekly-report`**（113 行）：① Stage 1.6 持续性度量 ＋ 实测β（07-09，弹性分 v2 依赖）；② 龙鱼 batch「常更标的不并入此处」分工；③ Stage 5 抬头「6 表 ＋ board_snapshots」——**顺带补上下面漏列的第 6 张表**（实测 `board_snapshots` 存在、131 行；07-09 改了抬头没改清单）。
- **安装已完成**（Doctor 终端）：live 树原文件先 `cp` 成 `.bak_20260731` 再覆盖；四项内容标识核验全过（`ingest-check`=2 · `09:30`=2 · `compute_persistence`=1 · `board_snapshots`=2）。`baize` 赶在**后天 01:09** 那次周报之前。

---

## 做出的决策

| 决策 | 原因 | 影响 |
|------|------|------|
| **模型改回 `deepseek-v4-pro`，只动 `.env` 一行** | C 组实测 pro 在 Anthropic 端点仍可用；且 8 月初 pro 就回 Responses | 注释/兜底/文档一律不动；型号轮换从此只改一处 |
| **`.env` 写显式 `KG_MODEL=deepseek-v4-pro`，而不是删掉该行** | 删掉则新加的「读 `.env`」分支永不执行＝未验证代码；留一行则每周报都在跑，坏了立刻暴露 | `EXP-20260731-004-P` 的反面用法；`grep` 一下即知当前跑什么 |
| **`.env` 由 Doctor 终端改，CC 不碰** | 该文件装 5 个密钥，按 `Env/README.md` 铁律密钥写入只在 Doctor 终端做 | 刻意不生成 `.bak`——复制一份等于多一处泄漏面 |
| **`zhuzhao` 不与另两份一起合，单开** | 它是双向分叉，且 margin/guarantee 归属需 Doctor 拍板 | 周一 10:03 前做完即可 |
| **`recap-kejian-review` 的时刻一并订正（超出「纯合并」）** | 那是会进生产的事实错误，且与本次改动同一处 | 标为改动③、可单独砍掉 |
| **Documents 死树暂不归档** | `zhuzhao` 合并还要拿它当素材 | 三份合完再统一改名 `_DEPRECATED_`、不删 |
| **合并文件先落 `_merge-staging-20260731/`，由 Doctor `cp` 装** | CC 写不到 live 树（沙箱只允许挂 `~/Documents`） | 附 `diff` 自检 + 内容标识核验 |

---

## 遗留问题 / 待办

> 主待办已挂 `brain/TODO.md`。此处只记未进 TODO 的。

- [ ] **`zhuzhao` 三路合并**（周一 10:03 前）。**需 Doctor 拍板**：`margin_daily` / `margin_guarantee_ratio` 两步该归 zhuzhao 班，还是已移交别班？——实测 `margin_daily` 07-31 09:30 仍在更新（**有别的执行路径**），故不能按「live SKILL 没写＝没人跑」推断。
- [ ] **`us-close-backfill` 补挂载探测段**（照 zhuzhao 写法），周一 13:34 前。首跑简报若能翻到，可一锤定音。
- [ ] **`margin_guarantee_ratio`（维持担保比例 R）停在 07-27**，已 4 个交易日未更新、**越过它自己的「>3 交易日标 ⚠」阈值**。原因未分辨：结构性没人跑 vs 东财断流连续失败。
- [ ] **Documents 死树归档**（`_DEPRECATED_Scheduled_20260731/`，改名不删）——等三份合完。
- [ ] **07-30 的 DGS2/DGS10** 窗口早开（H.15 16:15 ET），本场一直没取。
- [ ] **`score_with_llm.py` 读的是 `DEEPSEEK_MODEL`/`FF_SCORE_MODEL`，不是 `KG_MODEL`**——现靠 `weekly_local_prep.sh` 显式传 `--model` 掩着；直接跑脚本会走它自己的默认 pro，与 `.env` 不一致。
- [ ] **CC 无法维护任何 live 定时班**（沙箱 allowed roots 只有 `~/Documents`）——这是本场分叉的结构性成因，值得单独想办法。

---

## 本场方法论

### 「静默成功」比「静默失败」更隐蔽

昨天立的 `EXP-20260731-004-P` 讲的是**静默失败**（规矩写了、执行时报错被吞）。今天这个是它的升级形态：**改动写进了一个真实存在、看起来完全正确、但没人读的位置**——没有报错，文件确实变了，`diff` 也能看到，只是调度器读的是另一棵树。

**成因**：CC 唯一能写的地方（`~/Documents`）不是调度器读的地方（`~/Claude's workspace`），而 CC 看不见后者、因此也不知道自己写错了地方。**工具的可见范围决定了它会把东西写到哪，而不是任务的正确落点决定的。**

### 我在本场自己犯的两次

1. **「`handshake-consumer-daily` 是 Documents 独有」** —— 照折行的 `ls` 输出拼的，拼漏了；实际两边都有且内容一致。
2. **「live SKILL 没写 margin ⇒ 一定没跑」** —— 实测 `margin_daily` 当天上午还在更新，**有别的执行路径**。按「SKILL 是唯一入口」推断，错了。

两次都是**拿不完整的信息当完整事实**，与前一场那五条失效前提同族。

### 预设分支被实测推翻，是探针设计的价值

三组对照里 **B 组的作用不是确认，是推翻**——推翻的还是我自己写在判读表里的分支。若只跑 A、C 两组（够回答「能不能切」），就会漏掉「flash 也是推理模型」这个事实，进而可能去「优化」掉一个正确的补丁。⇒ **设计对照组时，要专门放一组用来打自己的假设，而不只是验证结论。**

---

## 相关笔记

- `Projects/Financial/白泽大宗/GOTCHAS.md` **GOTCHA-023 追记（2026-07-31）**
- `Projects/Financial/白泽大宗/scripts/automation/probe_deepseek_model.py`（本场新建 · 探针常驻）
- `Projects/Financial/白泽大宗/scripts/automation/weekly_local_prep.sh`（KG_MODEL 三档取值）
- `~/Documents/Claude/_merge-staging-20260731/`（两份合并稿 · 已安装 · 可清）
- [[通用教训]] G-X114（量纲与传导）· G-X115（订正本身也要核）· [[经验库]] EXP-20260731-004-P（静默失败）
- 上游：logs/2026-07-31-US10Y口径终查与TODO五条失效前提-0937.md · logs/2026-07-31-2Y终核与P-09撤回.md
- 外部：[DeepSeek · Using the Responses API](https://api-docs.deepseek.com/guides/responses_api/) · [Using the Anthropic API](https://api-docs.deepseek.com/guides/anthropic_api)
