---
title: portable — brain 对开发者模式的导出层
abstract: "brain（真源）→ ~/.claude（消费端）的单向导出：6 个 brain-* skill + dev 模式 bootstrap。安装用 symlink/cp，更新纪律见下。"
tags: [portable, claude-code, 数灵转移]
created: 2026-08-02
updated: 2026-08-02
status: active
type: reference
related: [数灵转移/architecture/决策记录, 全局偏好-Settings镜像]
---

# portable/ — brain → `~/.claude` 单向导出层

**方向**：brain（真源）→ `~/.claude`（消费端）。开发者模式想改 skill：直接改本目录（symlink 已连通），改动进 git；**不要**在 `~/.claude` 侧另存副本。

## 内容

| 项 | 安装方式 | 为什么 |
|---|---|---|
| `skills/brain-*` ×6 | `ln -s` 进 `~/.claude/skills/` | 单一真身在 brain，git 可 diff；机器上已有 dream→cc-switch 的 symlink 先例 |
| `claude-code/CLAUDE.md` | **cp**（非 symlink）到 `~/.claude/CLAUDE.md` | Claude Code 可能整文件重写，断 symlink 是静默的；copy 漂移风险低——内容只是指针 |
| 三灵运行档 | `ln -s` 指向 `brain/agents/{灵}/{灵}.agent.md` | 真身本就在 brain（2026-08-02 核实为最新版），不在本目录另存 |

安装/重装命令（幂等）见 brain 日志 2026-08-02 或直接重跑当日终端 block。

## 更新纪律

- **⚠ brain-prd 单向发布（2026-08-18 Doctor 裁 · supersedes 下条「Cowork 账号为主」· 仅限 brain-prd）**：`brain/.skills/brain-prd/SKILL.md` 为唯一内容真源；本目录 `portable/skills/brain-prd/SKILL.md`、`.skill` 包、Cowork/Claude-3p 安装副本及 plugin cache 均为**只读派生消费端，禁止独立编辑**。发布链：`Brain canonical → portable → .skill → 运行时安装 → 新会话回读验证`，每层回读 SHA 一致。其他 brain skills 仍按下方旧纪律，存量漂移另列 TODO 统一收敛。
- **Cowork 账号里改了 brain-* skill ⇒ 必须重导出本目录**，否则 dev 侧静默用旧版（G-X118 同族：改动落在不被消费的位置）。导出来源是 Cowork 只读缓存，任一 CC 会话可做，导出后 `diff` 校验逐字一致。
- 本目录改了 ⇒ dev 侧即时生效（symlink）；Cowork 侧需 `save_skill` 带回账号。
- 冲突时谁算数：**~~Cowork 账号为主~~（Doctor 2026-08-02 定 · brain-prd 已由 2026-08-18 canonical 裁定 superseded；其余 skill 仍适用）**。
- 本快照基线：2026-08-02，6 个 SKILL.md 共 73,496 字节，导出时 diff 6/6 一致。
