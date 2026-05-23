---
title: 会话日志 2026-05-23 — 记忆系统对标OpenViking与五项优化落地
tags: [log, brain]
created: 2026-05-23
updated: 2026-05-23
status: active
type: log
project: brain系统
---

# 会话日志 — 2026-05-23

**项目**：brain 记忆系统（跨项目 meta）
**主题**：DVA 抖音单视频转字幕 + brain 记忆系统对标 OpenViking 与五项优化落地

---

## 完成的工作

- DVA：确认抖音单视频转写必须在 Mac 跑（沙盒对抖音/volces/dashscope DNS 解析全失败），给出 `harvest-links.js` 三行命令；Doctor 在 Mac 跑通并回传字幕。
- 读字幕（OpenViking 设计概览），对标 brain 记忆系统，产出逐维度优劣对比 + 分级优化建议（A/B/C 三档）。
- Doctor 批准 A1+A2+A3+B（B1+B2）；CC 先出具体改动清单，二次确认后执行。
- **A1 分级加载标准化**：7 个 `系统概览.md` 加 `abstract`(L0)、6 个补「何时深入」(L1→L2 门)、星空 stub 加 abstract、`CLAUDE.md` 立《分级加载约定 L0/L1/L2》。
- **A2 经验库**：新建 `permanent/经验库.md`（cases/patterns/tools/strategies + 3 真实种子）、`templates/experience.md`、`CLAUDE.md`《经验沉淀规则》（半自动）。
- **A3 级联复查**：新建 `.tools/check-cascade.py`（实测 3 例通过）、`CLAUDE.md`《级联复查规则》。
- **B2 半自动 commit**：`brain-save` 加 Step 3.5「记忆分拣提议」(v2.1)，重打包 `brain-save.skill`。
- **B1 记忆固化**：新建 `brain-consolidate` skill（双重门控，只定义流程不自动跑），打包 `brain-consolidate.skill`。
- 自检：索引重建 0 悬空 / 0 孤儿；改动文件 frontmatter 全绿；两 `.skill` 包验证合法且含新内容。

## 做出的决策

| 决策 | 原因 | 影响 |
|------|------|------|
| 借鉴 OpenViking 分级加载/agent 自我记忆/session-commit | 思想契合，但落到 brain 的纯文件 + 人在环模型 | A1/A2/B2 |
| C 档不做（向量检索/每条三文件/替换日志） | 规模小 + 人工策展，性价比不足；维持纯文件 D2 决策 | 明确边界 |
| 经验沉淀走半自动（/save 提议、Doctor 点选） | 与 GOTCHAS 自动记错误对称，保人在环 | A2/B2 |
| B1 固化双重门控（建 skill 但绝不自动跑） | 会大面积改写历史，须最谨慎 | 每次先出 diff 待批 |

## 遗留问题 / 待办

- [ ] Doctor 在 Mac 终端跑 git commit+push（brain 仓库）
- [ ] Doctor 重装 brain-save / brain-consolidate 两个 skill（已 install 即生效）
- [ ] B1 固化尚未实跑；待 Doctor 喊 `/consolidate` 再出 diff
- [ ] `CLAUDE.md` 无 YAML frontmatter（pre-existing 校验 ✗），是否补 frontmatter 待定

## 相关笔记

- [[经验库]]
- [[通用教训]]
- [[项目总览]]
- [[CLAUDE]]
