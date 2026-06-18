---
title: 会话日志 2026-06-18 — DVA download-only 模式 + 麦橘/SansanYe 采集进表
tags: [log, DVA]
created: 2026-06-18
updated: 2026-06-18
status: active
type: log
project: DVA
---

# 会话日志 — 2026-06-18

**项目**：DVA
**主题**：新增 watchlist `download-only` 模式 + 麦橘MERJIC/SansanYe 采集与进常更表

---

## 完成的工作

- 为 **SansanYe**（首条消息称「新作者」，sec_uid `MS4w…rh-BF`）构造 transcribe-only 全量下载+转写命令链：沙箱外 Mac 跑，`number.post=0`=全部，按 sec_uid 反查 `_data.json` 自动识别真实昵称目录，逐步复刻 `harvest --transcribe-only`（绕开 `--limit 0` 被 `||5` 吞的坑）。
- 答复「能否同时再开一个」：定位两处并发共享态雷——`/tmp/dva_new_author.yml` 撞名、`dyd/dy_downloader.db` 单 sqlite 无 WAL/busy_timeout 跨进程写会 `database is locked`；给出并发安全变体（每作者独立 `/tmp` config + `database_path` 隔离，纯 config 覆盖不动既有文件）。倾向：串行更稳（ASR 是云端异步、并发不线性提速）。
- 麦橘MERJIC 一次性「只下载」命令（DYD `post:0`，无 ASR，带并发隔离）。
- **新增 watchlist `download-only` 模式**：仅改 `dva.js` 6 处纯增量——`handleHarvestCommand` 加 `--download-only` 解析 + 下载后短路返回（跳过 seed/ASR/import）；`handleUpdateAllCommand` 加 `download-only` 分支（push `--download-only`、analyze 标 skip）；help 文案 + watch add 用法串。`node --check` 通过。
- 给出 SansanYe(transcribe-only)/麦橘(download-only) 的 `watch add` 命令 + DVA 仓 commit 命令（均 Mac 跑，CC 不在沙箱碰 git）。

## 做出的决策

| 决策 | 原因 | 影响 |
|------|------|------|
| SansanYe = 首条「新作者」同一 sec_uid | 核实其 `_data.json` `nickname=SansanYe`、sec_uid 与首条 URL 一致 | 麦橘+SansanYe 进表里 SansanYe 的 sec_uid 已得，无需再问 Doctor |
| 麦橘进表选「新增 download-only 档」而非将就 transcribe-only | 麦橘是 AI 绘画/教程类非财经，且 Doctor 明说「只下载」；transcribe-only 仍会花 ASR 钱 | 实现新 mode；SansanYe 仍走 transcribe-only |
| download-only 仅改 dva.js、不改 watchlist.js | `watch add --mode` 自由字符串透传存储，watchlist 无需校验改动 | 改动最小、可逆 |
| Step 4 只更新 DVA.md 索引活跃日期，不动系统概览详细 ASR 笔记 | 概览「最后更新」是富信息（北京区 OSS 卡点），不该被通用句覆盖 | 可逆优先 |

## 遗留问题 / 待办

- [ ] Doctor 在 Mac 终端跑：麦橘首次全量下载 / SansanYe+麦橘 `watch add` / DVA 仓 `git commit`。
- [ ] **ASR 链路北京区 OSS 白名单**（系统概览载 2026-06-14：DashScope 结果走 `*.oss-cn-beijing.aliyuncs.com`，待 Doctor 放行 bj 区或 `*.aliyuncs.com`）——若仍未放行，SansanYe 的 transcribe-only **转写步骤可能卡住**，需先确认白名单状态。
- [ ] 文档同步（`使用流程.md`/`README.md` 的 mode 说明）本次按约定未动，待 Doctor 发话再出清单。

## 相关笔记

- [[DVA]]
- [[2026-06-14-DVA-ASR端到端复验卡北京区OSS]]
