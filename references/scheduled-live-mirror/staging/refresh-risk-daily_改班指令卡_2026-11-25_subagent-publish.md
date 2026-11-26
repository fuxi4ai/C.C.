---
title: refresh-risk-daily 改班指令卡 · 发布改由子代理通读（2026-11-25）
tags: [风险日报, 定时任务, 托管页]
created: 2026-11-25
status: active
type: reference
---

# refresh-risk-daily 改班指令卡 · 发布改由子代理通读

> 来由：2026-11-25 09:00 PT 那班读不完页面、两页没发（风险日报坑库 NOTE-20261125-003）。Doctor 2026-11-25 选择窗批「按预览替换」「现在手动跑一次」。Code 标签不直接改云端班（设备签名与双轨分工），由 Cowork 交互会话执行本卡。

## 贴给 Cowork 交互会话的指令（整段）

1. 读新提示词：`~/Documents/Claude/brain/references/scheduled-live-mirror/staging/refresh-risk-daily_cloud-prompt_2026-11-25_subagent-publish.txt`，先核 sha256 前 16 位＝`231c45088abe52af`、字符数 5269；不符就停，回报 Code 侧。
2. 读线上班 `trig_01KGQ1PpMg9GZQVrQymJotak`（Refresh risk daily）的现行 prompt，sha256 前 16 位应＝`3020911b8eca0bb4`（字符数 4659；备份在 `live/refresh-risk-daily/_bak/cloud-prompt.bak_2026-11-25_subagent-publish.txt`）。不符＝有人改过，停下回报，不要覆盖。
3. 用 `update_trigger` 只改 prompt，内容＝第 1 步文件全文，原样不动。cron、启停、连接器都不碰。
4. 回读线上 prompt，sha256 前 16 位应＝`231c45088abe52af`；回执里应有「prompt re-signed by 月兔的MacBook Air」。
5. 立即运行一次该班（Doctor 已批）。跑完回读三处：
   - 简报里「看板已发布」一行，三页各是已发、未变还是失败；
   - `~/Documents/Claude/brain/.tmp/pending-artifact-push.jsonl` 有没有本次 `refresh-risk-daily` 的新行；有就抄 `fallback_reason` 原文；
   - `~/Documents/Claude/brain/.tmp/artifact-publish/{risk-daily,risk-daily-ai-alarm,risk-daily-eal-starfield}/published.json` 的 sha 与同目录 `manifest.json` 的 `artifact_sha256` 是否一致。
6. 把结果写回风险日报坑库 NOTE-20261125-003 末尾一行追记（只追记，不改状态）。

## 回退

把 `live/refresh-risk-daily/_bak/cloud-prompt.bak_2026-11-25_subagent-publish.txt` 全文用 `update_trigger` 写回，再回读线上 prompt，sha256 前 16 位应＝`3020911b8eca0bb4`。

## 改动面

只改「看板推送」段第 3 步 sha 核对之后的部分：发布前的通读与发布交给一页一个的新子代理，主会话只按回报判成败；读不完或子代理没有 Artifact 工具时照旧走第 5 步登记待推。其余文字逐字未动（差异见同目录新提示词与 `_bak` 备份对比）。
