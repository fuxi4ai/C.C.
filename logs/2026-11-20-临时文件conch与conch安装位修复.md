---
title: 会话日志 2026-11-20 — 临时文件 conch 与 conch 安装位修复
tags: [log, 海螺姑娘]
created: 2026-11-20
updated: 2026-11-20
status: active
type: log
project: 海螺姑娘
---

# 会话日志 — 2026-11-20

**项目**：海螺姑娘（conch）· 牵涉 PEC、brain 云端班镜像
**时长**：约 00:45–01:30
**主题**：`/conch 临时文件` 全流程，以及 `/conch` 安装位被 cc-switch 换成旧版的排查与修复。过程细节见 [[2026-11-20-临时文件conch审查]]。

## 完成的工作

- 起手 `/conch` 未加载：`~/.claude/skills/the-conch-maiden` 链接缺失。随后出现的链接指向 cc-switch 存的 v0.1.0（2026-04-29）旧提示词版；本场按 brain 真源 v2.4.2 走 dry-run，未照旧版执行。
- `/conch 临时文件`：审查 44 顶层项；子代理复查 PASS_WITH_LIMITS（补漏 5）；Doctor 选择框四题全取推荐。
- apply：AJA ms0763 原件迁 PEC `sources/` 并改两处引用；7 件证据件进 `散落归档文件/`（附来源清单）；348 件进 fuxi 回收站（上传、SHA 一致、INDEX 登记、本机暂存已删，保留至 2026-12-05）；云端班 `refresh-asset-dashboard` 第 4 步改为「固定保留 → 两道阳性对照 → 按名字查引用（含 `logs/checkpoints`）→ 读取报错即整轮跳过」；README 订正；TODO 销账 4 处、新挂收尾条。
- 独立核验首轮 FAIL（漏改 PEC `制度与规范文本.md:257` 与摘录 379 行末；清空流程三缺陷），修后复验 PASS_WITH_LIMITS，限制项修毕。
- 登记海螺 GOTCHA-20261120-001（临时目录放着被现行文档引用的证据件 · 🔄）；GOTCHA-20261112-001 复发追记与修复记录（已修待验）。
- Doctor 终端修复安装位：cc-switch 旧副本归档为 `~/.cc-switch/archived/the-conch-maiden.archived_2026-11-20`，原位链到 brain 真源；CC 实读两级 readlink 与 cmp 一致。
- 回答「之前几次 conch 跑的哪一版」：11-17 起各场为真源 1.4.0 → 2.4.x（日志版本号与步骤痕迹佐证），11-20 凌晨 00:40–00:52 安装位被换，只有本场加载到旧版。
- 提交（Doctor 终端）：PEC `6652808`；brain `cb096ecb`、`e1bb4d31`、`33f885cb`；海螺姑娘 `1615778`、`6fb6162`。

## 做出的决策

| 决策 | 原因 | 影响 |
|------|------|------|
| AJA 原件迁 PEC `sources/`（进 git） | 唯一本地副本、被 PEC 按路径引用；散落归档无出口 | PEC 仓 +11 MB |
| 云端班清空前加引用检查 | 有人值守清空可能成功，会删掉被引用件 | 被引用件跳过并回报，需 conch 迁出 |
| 删除走 fuxi 回收站而非 README 的直接清空 | conch 规则；少数件只此一份 | 15 天可撤回 |
| cc-switch 位置改为指向 brain 的链接（不删 cc-switch 条目） | 保持 cc-switch 管理面不变，内容来自真源 | 自动同步会否覆盖待核 |

## 遗留问题 / 待办

- [ ] 首次有人值守清空时核对引用检查生效（已在 `TODO.md`「临时文件 conch 收尾」③）。
- [ ] 下次 `/conch` 起手 `readlink` 核安装位（海螺 GOTCHA-20261112-001 预防门禁）。
- [ ] 回收站包 2026-12-05 期满按 INDEX 精确包名清理（不归 CC）；快照 `brain/backups/linshi-conch-pre-2026-11-20.tar.gz` 去留待 Doctor 定。
- 第 4 步开头「挂两个叶子目录」与 11-13 起整挂 Documents 的前置不一致，旧问题，未改。

## 相关笔记

- [[2026-11-20-临时文件conch审查]]
- [[海螺姑娘/architecture/系统概览]]
