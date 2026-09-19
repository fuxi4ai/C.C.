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

- **⚠ 单向发布（2026-08-18 Doctor 立 · 2026-09-19 Doctor 扩程至全部 7 个 brain-\*）**：**canonical = `brain/.skills/{名}/SKILL.md`**；本目录 `portable/skills/{名}/SKILL.md`、`.skill` 包、Cowork/Claude-3p 安装副本及 plugin cache 均为**只读派生消费端，禁止独立编辑**。发布链：`Brain canonical → portable → .skill → save_skill 运行时安装 → 新会话回读验证`，每层回读 SHA 一致。
  - **动线（改任一 brain-\* skill 一律照此走）**：① 改 `brain/.skills/{名}/SKILL.md` → ② 同步 `portable/skills/{名}/SKILL.md` → ③ 重打 `brain/.skills/{名}.skill` → ④ `save_skill`（content 只传 frontmatter 后正文、metadata 走参数，否则双 frontmatter）→ ⑤ 新会话回读验证。
  - **扩程理由（2026-09-19）**：08-18 原判射程写明「仅 brain-prd，其他 brain skills 仍按旧纪律」→ 实为**两套规则并存（G-X151 双轨家族）**；且「账号为主」意味着 brain 仓内**没有 canonical**，权威指向一个不可 diff、不可回读核的运行时。触发 = 2026-09-18/19 夜复扫一小时内抓到**两次三面漂移**（brain-todo 副本未同步、brain-consolidate 包落后真源 66 行），证明必须有**仓内锚**。**存量 TODO「统一收敛」由此关闭。**
  - ⚠ **方向变更不影响内容**：扩程前夜按旧方向发布的 brain-save v3.5 与 brain-todo v2.1，四端（canonical/portable/包/账号）内容同版，**无需回滚或重发**；此后一律从 canonical 起手。
- ~~**Cowork 账号里改了 brain-\* skill ⇒ 必须重导出本目录**~~（2026-08-02 旧纪律 · **已 superseded**：账号侧不再是权威，改 skill 从 canonical 起手）
- ~~本目录改了 ⇒ dev 侧即时生效（symlink）；Cowork 侧需 `save_skill` 带回账号。~~（**已 superseded**：本目录降为派生，不应作为编辑点；dev 侧 symlink 仍即时生效，但它消费的是派生）
- ~~冲突时谁算数：**Cowork 账号为主**~~（2026-08-02 Doctor 定 · **2026-09-19 起 7 个 brain-\* skill 统一以 canonical 为准**，本句整条退休）
- 本快照基线：2026-08-02，6 个 SKILL.md 共 73,496 字节，导出时 diff 6/6 一致。
