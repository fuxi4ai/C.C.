---
title: 会话日志 2026-06-13 — 开发流程优化：brain-prd 与 save 双增强
tags: [log, 元方法论, 开发流程, brain-prd, brain-save, O MY HTML]
created: 2026-06-13
updated: 2026-06-13
status: active
type: log
project: 跨项目（brain 元方法论）+ O MY HTML
---

# 会话日志 — 2026-06-13

**项目**：brain 元方法论（开发流程优化）+ O MY HTML（试点）
**主题**：对照"毒舌产品经理 5.0"视频方法论优化项目开发流程，落成 brain-prd + brain-save 双增强

## 完成的工作

- **对照分析**：拆解视频方法论（轻流程 / 6 阶段 skill / 文档驱动 / agent 编排 / 自进化 / go 机制 / 三经验），与 brain 体系对照——发现独立收敛 ~80%，治理轴（PRD 三态、数据铁律、propose-then-confirm）brain 更成熟。提案 `references/视频方法论对照与开发流程优化-设计提案.md`。
- **阶段 1（文档级）**：`references/skill写作规范.md`（三段式骨架 + 厚薄判别尺 + 硬门禁）；`通用教训.md` 新增 **G-X10**。
- **阶段 2（机制级）**：
  - 新建 skill **brain-prd v1.2**：多轮对齐（禁阿谀逼问需求 + 三维问题库 + 对齐收口闸）+ 在场起草 PRD + **Step 7.5 独立审查闭环**（CC自审→独立子agent审→Doctor终审）。
  - **brain-save v2.4**：当下便签 + "规则/skill 该改"分拣类。
  - 打包 brain-prd / brain-save 为 .skill，Doctor 经 Save 卡片安装成功。
- **自检修订**：① signal 自进化机制经自检与 save→permanent 高度重复、save 不可退役 → **塌缩进 brain-save**，撤回 resume/consolidate 的 signal 改动、删 signals/ 文件夹；② "能即时写 GOTCHAS / 明示偏好"直写、只有"需抽象成通则"才走提案——判别尺＝要不要 CC 抽象。
- **O MY HTML 试点**（brain-prd 首次实跑）：补全 `系统概览.md` 三段（使命/模块/依赖）+ 收敛状态 🟡维护 + updated。PRD `logs/checkpoints/2026-06-13_OMYHTML系统概览补全_PRD.md` 全 13 条 Doctor **全 ✓ 已交付**。

## 做出的决策

| 决策 | 原因 | 影响 |
|------|------|------|
| 不照搬视频，只补净增量（PRD + SAVE） | brain 已有 ~80%，治理更成熟 | 改动收敛、不重复造轮子 |
| go-creator 落独立 skill brain-prd | 与 G-X4 分工清晰 | 大任务起手有对齐+起草器 |
| signal 自进化塌缩进 brain-save | 与 save→permanent 重复、save 不可退役 | 无平行管线，省机器 |
| 不 /save＝不想存档，便签不跨会话持久化 | Doctor 明确 | 无 signals/ 文件夹、无 resume 兜底 |
| 维持 propose-then-confirm 全局默认，不开自动执行白名单 | 研究项目假数/漂移代价高 | 拒绝视频"全自动+全放权" |
| brain-prd 接入独立审查子 agent | 视频"未参与开发的审查员"价值 | 三层验收闸，减 Doctor 负担 |
| 多 Agent 并跑暂不做 | 视频自身反对滥用、无具体瓶颈 | 留空待真实需求 |

## 遗留问题 / 待办

- [ ] 阶段 3 小尾巴（待批）：是否在 `CLAUDE.md` 加一行"当下便签随手记"捕捉提醒（bootstrap 慎改）。
- [ ] brain-prd 实战 3-5 次后评估"打勾权下放"前置条件（G-X4 §六）。
- [ ] O MY HTML 生图管线脚本仅"杭州·雪"落地，其余子项目 tools/ 待实装（非本次范围）。

## 记忆分拣提议（Step 3.5 · 请 Doctor 点选）

> 本次大部分长期记忆已即时落盘（G-X10 / skill写作规范 / brain-prd·save 源）。仅一条新经验候选：

- 【经验 · patterns】**独立审查子 agent 真能抓出 CC 自审漏掉的错**：O MY HTML 试点中，CC 自审 13 条全过，独立审查却查出"生图管线"路径写错（指了空的顶层 tools/）。**印证 Step 7.5"另一颗干净脑子"的价值**，非形式主义。→ 建议留 `permanent/经验库.md`（patterns）。难复得三问：持久✓ / 难复得✓（活体实证，丢了要重撞）/ 会再用✓ → **建议留**。

（其余如 G-X10、skill 写作规范均已落盘，不重复提。）

## 相关笔记

- [[视频方法论对照与开发流程优化-设计提案]]
- [[skill写作规范]]
- [[通用教训]]（G-X10）
- [[系统概览]]（O MY HTML）
