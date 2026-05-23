---
title: OpenViking · Agent 记忆系统设计要点
abstract: "字节开源 Agent 记忆系统：层级虚拟 FS + 三层分级加载 + 目录递归检索 + 自动记忆提取；级联更新仍未解"
tags: [resource, agent-memory, OpenViking, 对标]
created: 2026-05-23
updated: 2026-05-23
status: active
type: resource
source: 抖音「每日AI评论」视频字幕（OpenViking，字节跳动 Agent 开源记忆系统）
---

# OpenViking · Agent 记忆系统设计要点

> 字节跳动开源的 Agent 专用记忆系统。摘自视频字幕，作为 brain 记忆系统的对标基线。
> brain 的取舍见 [[架构决策-20260514]] D6。

## 它针对的 5 个痛点（点名主流 coding-agent，如 Claude Code）

1. 记忆量有硬上限（active recall 扫描上限约 200 文件，超出忽略；平面清单越长，模型注意力越散，准确率降）
2. 检索是单次判断，无探索/回溯/多步下钻
3. 记忆平铺无结构（偏好/项目/工具经验混在一个平面清单，须同时判类型与相关性）
4. token 消耗无精细控制（要么读全文费 token，要么只看摘要丢信息，缺中间粒度）
5. agent 执行经验不自动沉淀（只记用户偏好，不记"哪个工具/策略在什么场景有效、哪些错误反复出现"）

## 它的 5 个解法

1. **层级虚拟文件系统**统一管理所有上下文：顶层 `resources`（外部资源）/ `user`（用户长期记忆）/ `agent`（agent 自我学习记忆）；统一 URI，可 ls/find/tree；目录天然带层级 + 描述，相关信息自然聚类。
2. **三层分级加载**（核心）：每个目录节点有 L0 abstract（~100 token，一句话判相关）/ L1 overview（~2000 token，做"要不要深入"决策）/ L2 完整内容（确认才加载）；写时三层同生，读时按需取。**实测输入 token 降 83–96%**。
3. **目录递归检索**替代平面向量搜索：全局在 L0/L1 搜出高分目录 → 目录内下钻 → 分数传播（子节点继承父目录得分）→ 收敛检测（连续 3 轮不变停）。"先找对书架，再找书"。
4. **检索轨迹可视化**：层级 → 检索是可追踪路径，出问题可逐步诊断（全局没找对目录？子搜漏了？分数传播权重错？）。
5. **自动记忆提取 + 自我迭代**：session commit 在对话结束时由 LLM（MemoryExtractor）提取记忆，分 8 类——用户侧 profile/preferences/entities/events，agent 侧 cases/patterns/tools/skills，每条生成 L0/L1/L2；另有七段式 working memory，按段做 keep/update/append 而非整篇重写。

**整体数据**：任务完成率 +43–49%，输入 token 降 83–96%（双改善 = 靠更精准找信息，非塞更多信息）。

## 未解的难题：级联更新

上游事实变了，下游依赖能否自动更新（MAIM 论文测：所有系统准确率仅 **3%**）。OpenViking **不能直接解**——有 relations 机制存 URI 关联，但**只在检索时发现，不在写入时触发级联**。层级结构让相关事实聚在同目录，递归进入时有机会一起看到、读时发现不一致，但依赖模型推理，非系统级保证。

## 与 brain 的对照（速记）

- brain 已有：真实 Obsidian FS + git；anchor 两档加载 ≈ 分级思想；ripgrep + wikilink 反链 + anchor 路由 ≈ "先找书架"；GOTCHAS 自动记错误；不可变会话日志。
- 借鉴落地：见 [[CLAUDE]] 分级加载约定 / [[经验库]] / brain-save v2.1 / brain-consolidate。
- brain 的相对优势：wikilink 反链是**写时可发现**的依赖图（[[CLAUDE]] 级联复查规则用它），起点比 OpenViking 的 relations 高。

## 相关

- [[架构决策-20260514]] · D6 取舍
- [[经验库]] · 分级加载范式种子
- [[CLAUDE]] · 三节新规则
