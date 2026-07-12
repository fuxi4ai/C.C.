---
title: 会话日志 2026-07-11 — DVA常更表全量补库与Playwright坑修复
tags: [log, DVA]
created: 2026-07-11
updated: 2026-07-11
status: active
type: log
project: DVA
---

# 会话日志 — 2026-07-11

**项目**：DVA（抖音视频分析 · 常更表补库运维）
**主题**：常更表全量补库 → 撞 Playwright Chromium 缺失 → 修复 → 8/8 跑通；确认「转写按作者分类规则走」

---

## 完成的工作

- **确认口径**：厘清 update-all 全量补库时转写字幕逐作者按 `mode` 分发（源码 `handleUpdateAllCommand`：transcribe-only→`--transcribe-only`、download-only→`--download-only`、否则 full），mode 被 category 绑定，故「转写按分类规则走」成立。现状 8 位：金融 2(full)、PEC语料 4(transcribe-only)、设计 2(SansanYe=transcribe-only / 麦橘=download-only)。
- **发现 falsy 陷阱**：`update-all --limit 0`（本意=全部）被 `0 || null` 静默吞成默认 20（harvest 已修此坑、update-all 未修）。历史全补改用 `DVA_REFILL_LIMIT=9999` 绕过。
- **定位并修复根因**：`DVA_REFILL_LIMIT=9999` 首跑卡在【作者 2/8】、下载 0 条，报 `chromium-1228 / Google Chrome for Testing 不存在`。机理＝增量走 API 即可，历史全补需深翻页 → DYD 回落浏览器，而 Playwright 浏览器未装。用 **DVA venv 自己的 playwright**（`DVA-ops/runtime/venv/bin/playwright install chromium`，版本才匹配 1228；勿用 npx）装好 Chrome for Testing 149.0.7827.55。
- **小样验证 → 全量**：先 `DVA_REFILL_LIMIT=5` 验证 browser 错误归零、有视频入库（8/8 success），再上 `9999` 全量。
- **全量跑通**：8/8 采集成功、0 失败、browser 错误全程 0，用时约 67 分钟。mode 分发逐位复核正确。真正新增字幕仅 独夫+18、黑盒+3、老毛+1（历史此前已基本补齐，未触发大规模 ASR 花费）；麦橘 download-only 全程只下载。
- **记 GOTCHAS**：`DVA/GOTCHAS.md` 追加 ERR-20260711-001（✅ Playwright 缺失，含 preflight 不验浏览器的盲点）+ BUG-20260711-002（⏳ update-all `--limit 0` falsy 陷阱，根治=改源用 `Number.isFinite`）。
- **进度可观测三查法**：结构化状态 `state/runs/*.json`、实时 `tail -f` 最新 log、逐作者推进读 `watchlist.json` 时间戳；CC 侧可直接读挂载文件替 Doctor 报进度。

## 做出的决策

| 决策 | 原因 | 影响 |
|------|------|------|
| 历史全补用 `--limit 9999` 而非 `0` | update-all 的 `0\|\|null` falsy 陷阱把 0 吞成 20 | 绕过不改源；9999 覆盖作者专属 limit（>浪浪 1000）|
| 装 Chromium 用 venv playwright 而非 npx | Node 版 npx 装的版本可能对不上 DYD 的 python playwright 期望的 chromium-1228 | 版本匹配、一次装对 |
| 先小样(limit 5)验证再上 9999 | 避免又白跑半天 ASR | 小样 8/8 通过后才全量 |
| 金融 2 位 level1 分析暂不跑 | 本轮新增极少(老毛+1、投知 0)，level1 是全量重分析、耗 DeepSeek，性价比低 | 待金融作者放出实质增量再单跑 |
| BUG-20260711-002 改源根治延后 | 改源需 Doctor 授权；9999 绕过已够用 | GOTCHAS 标⏳待根治，未擅动源 |

## 遗留问题 / 待办

- [ ] **BUG-20260711-002 改源根治**：`handleUpdateAllCommand` 的 limit 解析改用 `Number.isFinite`，让 `--limit 0` 正确=全部（对齐 harvest）。需 Doctor 授权 CC 才动源。
- [ ] **金融 2 位 level1 分析**：待老毛/投知有实质增量时单跑（命令：cd Codex mirror + source deepseek-dva.env + `node dva.js analyze-level1 <作者>`，见 GOTCHAS BUG-20260703-001）。
- [ ] **refill 脚本 preflight 盲点**：只验 playwright python 包、不验浏览器 build 是否装 → 建议加 `chromium-*` 存在性校验（ERR-20260711-001 预防措施）。

## 相关笔记

- [[DVA]]
- DVA GOTCHAS：ERR-20260711-001（Playwright 缺失）· BUG-20260711-002（--limit 0 falsy）
- 承接：[[Doctor协作偏好]]（propose-then-confirm + 不在沙箱跑 git + AskUserQuestion 带推荐标签）
