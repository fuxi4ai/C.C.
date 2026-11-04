---
title: 司南 · GOTCHAS（已知坑）
tags: [司南, gotchas]
created: 2026-05-14
updated: 2026-05-14
status: active
type: resource
project: 司南
---

# 司南 · GOTCHAS（已知坑）

> 排查超过一轮的问题都该记录在这里。CC 遇到报错并解决后**立即**回写，无需 Doctor 提示。
> 实时操作日志写在项目目录的 `Projects/司南/GOTCHAS.md`；这里是沉淀+索引。

## 格式

```
## [ERR-YYYYMMDD-NNN] 简要描述
**状态**: 🔄 待修复/已修待验 / ⚠️ 已知风险；✅ 已修复（**仅由 Doctor 或指定独立验收方落，实施者不得自标**）（⏳ 旧状态词 2026-08-26 迁移专场退役）
**优先级**: 🔴 高 / 🟡 中 / 🟢 低
**触发场景**:
**错误信息**:
**解决方案**:
**预防措施**:
```

---

<!-- 在下方追加新条目 -->

## [ERR-20261104-001] 官方壳 Code 标签与 Cowork 标签是两个执行面，适配卡只按 Cowork 写
**状态**: 🔄 待修复/已修待验
**优先级**: 🟡 中
**触发场景**: 2026-11-04 Doctor 在官方订阅的 Code 标签要求核查 Gateway→官方迁移，指令卡的注册表、skill、artifact 步骤均按 Cowork 写。
**错误信息**: Code 标签 `list_scheduled_tasks` 返回 0；`list_artifacts`（claude-artifacts）返回空；工具集无 `update_artifact`、`request_cowork_directory`；工具说明写明任务存于 `~/.claude/scheduled-tasks/`；24 个活班 prompt 中 16 个依赖 Cowork 工具或沙箱路径（镜像关键词扫描，未实跑）。
**解决方案**: Doctor 裁定班与看板留 Cowork；指令卡增「〇 · 执行面订正」节。Cowork 注册表现状仍待该标签实读。
**预防措施**: 切环境核查前先确认执行面（Cowork / Code / Gateway）；不用 Code 标签的注册表读数判定 Cowork；复原清单与沿革须按执行面区分。
