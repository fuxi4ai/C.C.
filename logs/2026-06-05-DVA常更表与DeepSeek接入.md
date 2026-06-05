---
title: 会话日志 2026-06-05 — DVA 常更表 + 一键更新 + DeepSeek 接入
tags: [log, DVA]
created: 2026-06-05
updated: 2026-06-05
status: active
type: log
project: DVA
---

# 会话日志 — 2026-06-05

**项目**：DVA
**主题**：常更作者表 + 一键批量更新 + 分析 LLM 切 DeepSeek V4 Pro

---

## 完成的工作

- 新增 `基础模块/watchlist.js`：常更作者表读写（getWatchlist / addAuthor / removeAuthor / getActiveAuthors），落盘 `DB_ROOT/indexes/watchlist.json`。
- `dva.js` 加 `dva watch add/remove/list` 子命令 + `dva update-all`（别名 watch update / update-watchlist），注册路由、补 printHelp。
- 批量更新逻辑：遍历常更表，每位作者**子进程隔离**跑 `harvest`（视频→入库→ASR→注入）→ `analyze-level1`，默认每作者 20 条，逐作者容错 + 末尾汇总。
- 把 4 位作者写入常更表：老毛聊交易、投知君君买方视角、卷宇宙漫谈、黑盒调查局。
- 分析 LLM 默认切 DeepSeek V4 Pro：`llm-client.js` / `dva_config.js` 默认改 `deepseek-v4-pro` + `https://api.deepseek.com/anthropic`；引入 DVA 专属变量 `DVA_LLM_API_KEY/BASE_URL/MODEL`，优先级压过全局 APIYI 的 `ANTHROPIC_*`。
- 修真 bug：`chat()` 原写死 `content[0].text`，推理模型首块是 thinking → 取到空串；改为按 type 挑 text 块拼接（ERR-20260605-001）。
- `mind-extractor.js` 元数据标签 `llm-claude-sonnet` → `llm-extraction`（中性名）。
- 写 cron wrapper `run-update-all.sh`（PATH/凭证/日志自包含），含 macOS 完全磁盘访问等 SETUP；建周三/周六 05:00 桌面提醒任务后又按 Doctor 要求删除（改用 Mac 原生 crontab）。
- 回写：CHANGELOG v6.6、brain 决策记录 ×2、brain GOTCHAS ×1。

## 做出的决策

| 决策 | 原因 | 影响 |
|------|------|------|
| 批量更新对每作者 spawn 子进程 | harvest 内部多处 process.exit，主进程内 await 会被单作者失败终止整批 | 单作者失败不影响其余，可逐作者汇总 |
| 常更表用 CLI 子命令管理 + JSON 落盘 | Doctor 选「CLI 子命令」，每作者默认 20 条 | watchlist.json 人类可读，可命令可手改 |
| DeepSeek 设为代码默认值（非仅 env） | Doctor 要 DeepSeek 做标准 API，覆盖 cron+交互两条路径 | 唯一必填缩到 key；ANTHROPIC_API_KEY 须换 DeepSeek key |
| 引入 DVA_LLM_* 专属变量 | 全局 ANTHROPIC_BASE_URL 指向 APIYI，会盖掉 DeepSeek 默认 | DVA 与其他 APIYI 项目隔离，互不干扰 |

## 遗留问题 / 待办

- [ ] Doctor 在 Mac 装 crontab：`0 5 * * 3,6 ~/Documents/Claude/Projects/DVA/run-update-all.sh`
- [ ] 给 `/usr/sbin/cron` 开完全磁盘访问权限（否则读不到 ~/Documents，静默失败）
- [ ] 确认 `~/.dva_secrets` 用 DVA_LLM_* 变量名、key 为 DeepSeek 官方平台签发（非 APIYI 令牌）
- [ ] 治本建议（旧）：给 `harvest-links.js` 末尾补 seed，单链接产物不再成 import 孤儿

## 相关笔记

- [[DVA]] · [[系统概览]] · [[决策记录]] · [[GOTCHAS]]
