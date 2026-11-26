---
title: 风险日报独立发布班 · 建班指令卡（2026-11-25）
tags: [风险日报, 定时任务, 托管页]
created: 2026-11-25
status: active
type: reference
---

# 风险日报独立发布班 · 建班指令卡

> 来由：构建班读不完页面（风险日报坑库 NOTE-20261125-003）；子代理读发被自动模式分类器拦下（同条 11-25 夜追记）。Doctor 2026-11-25 选择窗裁「独立发布班」。新建定时班归 Cowork，Code 标签只备材料。

## 材料（本目录）

| 文件 | 用途 | 字符数 | sha256 前 16 位 |
|---|---|---|---|
| `risk-daily-publish-ai_prompt_2026-11-25.txt` | 新班 `risk-daily-publish-ai` 提示词 | 3717 | `7f3f5b9512b2c11f` |
| `risk-daily-publish-eal_prompt_2026-11-25.txt` | 新班 `risk-daily-publish-eal` 提示词 | 3700 | `e27812d7783d4c80` |
| `risk-daily-publish-main_prompt_2026-11-25.txt` | 新班 `risk-daily-publish-main` 提示词 | 3586 | `0be22292f046afa8` |
| `refresh-risk-daily_cloud-prompt_2026-11-25_publish-split.txt` | 构建班新提示词（看板推送段改为「交由发布班」） | 1823 | `98fc031b10d0c4c7` |

构建班现行提示词应为 4659 字、`3020911b8eca0bb4`，备份在 `live/refresh-risk-daily/_bak/cloud-prompt.bak_2026-11-25_subagent-publish.txt`。

## 贴给 Cowork 交互会话的指令（整段）

1. 核材料：上表四个文件的字符数与 sha256 前 16 位逐一对上，不符就停，回报 Code 侧。
2. 读构建班 `trig_01KGQ1PpMg9GZQVrQymJotak`（Refresh risk daily）的设置与提示词：提示词应为 `3020911b8eca0bb4`；记下它的绑定设备、挂载文件夹、模型、权限模式、连接器。
3. 新建三个定时班，设置都照抄构建班（同一台 Mac、同样挂载 `/Users/lunarabbit/Documents`、同模型、同权限模式、同连接器），只有名称、时刻、提示词不同：
   - `risk-daily-publish-ai`：每天太平洋时间 09:30，提示词＝`risk-daily-publish-ai_prompt_2026-11-25.txt` 全文；
   - `risk-daily-publish-eal`：09:40，提示词＝`risk-daily-publish-eal_prompt_2026-11-25.txt` 全文；
   - `risk-daily-publish-main`：09:50，提示词＝`risk-daily-publish-main_prompt_2026-11-25.txt` 全文。
   建完回读三个班的提示词 sha，与上表一致；记下三个 trigger id。
4. 先试跑，再改构建班：依次手动运行 ai、eal、main 三个新班（等前一个结束再跑下一个）。跑完回读：
   - 简报各一行（已发布 / 未变·跳过 / 失败）；
   - `~/Documents/Claude/brain/.tmp/pending-artifact-push.jsonl` 是否有 `task` 为 `risk-daily-publish-*` 的新行，有就抄 `fallback_reason`；
   - 三个目录 `published.json` 的 sha 是否等于各自 `manifest.json` 的 `artifact_sha256`。
5. 只有第 4 步里三页都「已发布」（或「未变·跳过」），才把构建班提示词改为 `refresh-risk-daily_cloud-prompt_2026-11-25_publish-split.txt` 全文（`update_trigger` 只改 prompt），回读 sha 应为 `98fc031b10d0c4c7`。有任何一页失败：构建班不改，保持现状，回报 Code 侧；新班先停用还是留着，由 Doctor 定。
6. 在风险日报坑库 NOTE-20261125-003 末尾追记一行：三个 trigger id、试跑结果、构建班是否已改（只追记，不改状态行）。

## 回退

- 构建班：把 `_bak/cloud-prompt.bak_2026-11-25_subagent-publish.txt` 全文用 `update_trigger` 写回，回读应为 `3020911b8eca0bb4`。
- 三个新班：停用即可（停用、删除由 Doctor 定）。

## 设计要点

- 每个发布班从全新上下文开始，只读一页、读完由本会话自己发布，不派子代理——与 11-24 构建班自发成功的做法同型。
- 发布班自己跑拆分器，所以不依赖构建班留下的拆分产物；内容没变就跳过，不花读的用量。
- 先确认今天的构建已落盘（快照 `generated` 晚于今天太平洋时间 09:00），没落盘就每分钟查一次、最多 20 分钟，仍没有就登记待推，不会静默停在旧版；原件修改不足 2 分钟再等 1 分钟，避免读到写到一半的文件。
- 失败照旧登记待推，`task` 写发布班名，便于和构建班区分。
