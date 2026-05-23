---
title: Doctor 协作偏好
abstract: "重大改动须 propose-then-confirm：先出具体改动清单 → Doctor 批准 → 才执行；分级批准、可逆优先"
tags: [偏好, 协作, workflow]
created: 2026-05-23
updated: 2026-05-23
status: active
type: permanent
---

# Doctor 协作偏好

> CC 与 Doctor 协作的稳定工作方式，跨项目通用。新 session 应默认遵守。

## 核心：propose-then-confirm（先提案，后执行）

涉及**改动**（改文件、改系统、改流程，尤其动既有资产）时，遵循三步：

1. **提案**：先给优劣对比 / 方案，必要时分级（A/B/C 档）并标注成本·收益·风险。
2. **出具体改动清单**：批准方向后，**再给一份逐文件的具体改动清单**（动哪些文件、新增/改/归档什么、即时生效 vs 需重装、是否需 Mac 跑 git），等二次确认。
3. **才执行**：清单点头后才动手。Doctor 原话："一切改动同意后才可执行"。

> 关键细节：**"批准做某件事" ≠ "批准具体怎么改"**。即使 Doctor 已说"做 A1"，仍要先出 A1 的具体改动清单再落盘。

## 配套习惯

- **分级批准**：方案分档给，让 Doctor 按性价比挑（用 AskUserQuestion 多选最佳）。
- **可逆优先**：不删文件（弃用走 `status: archived` 或 `_DEPRECATED_` 改名）；大面积改写历史的动作（如记忆固化）双重门控、先出 diff。
- **诚实边界**：方案的局限直说（如级联复查只覆盖 wikilink 依赖）。
- **git / 网络硬约束**：CC 不在沙盒跑 git 写命令、不在沙盒跑下载/ASR——构造命令贴给 Doctor 在 Mac 终端跑。

## 相关

- [[CLAUDE]] · 全局规则
- [[通用教训]] · 工程通用陷阱
