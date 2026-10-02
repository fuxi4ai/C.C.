---
title: 会话日志 2026-09-17 — Claude Code 体检与维护
tags: [log, CC环境维护]
created: 2026-09-17
updated: 2026-09-17
status: active
type: log
project: 跨项目（CC 自身环境）
---

# 会话日志 — 2026-09-17

**项目**：跨项目（CC 自身运行环境维护）
**主题**：Claude Code 体检与维护（版本库清理 / /doctor 全项 / 自动更新报警消除 / caixin MCP 移除）
**出场者**：CC 自身（无数灵唤名）

---

## 完成的工作

- **版本库清理**：确认 `claude update` 无需执行（安装版 2.1.274 = npm latest）。旧版本目录 `2.1.223`（260M）移入 `~/.Trash/claude-versions-20260917/`，未用 `rm`；保留 `2.1.272` 作回滚点。版本库 665M → 405M。首次 `mv` 被 auto 模式分类器拦截（Permission），Doctor 授权后拆分执行通过。
- **15 天观察期登记**：到期日 2026-10-02，写入 `~/.claude/projects/-Users-lunarabbit/memory/pending-maintenance.md` 并挂进该目录 `MEMORY.md` 索引。已说明本模式无跨会话定时器（CronCreate 会话级、上限 7 天），机制为被动命中。
- **/doctor 全项体检**（检查 0–9，只读先行）：
  - 检查 0 安装健康：单一 native 安装、PATH 正常、无 npm 残留、6 个配置文件全部 `jq empty` 通过、3 个数灵定义 frontmatter 合法无碰撞、10 个 SKILL.md 全部可解析 → **无发现**。
  - 检查 1：`caixin-data` MCP 33 天零调用且工具 schema **常驻非延迟加载**（~750 est. tokens）；`dream`/`graphify` 闲置 → 停用。brain-* 系列判为保留（Doctor 自建工作流、间歇性使用）；`brain-anchors` 的 1112 字符描述是锚词表、**不剪**。`claude-hud` 虽计数为 0 但 statusLine 实际调用其 cache 目录 → 保留。
  - 检查 2：查出**材料级矛盾**——`~/.claude/CLAUDE.md`（brain 真源）与 `~/CLAUDE.md` 各自声称是记忆的「唯一真源」。已按 `memory/brain-vs-memory.md` 裁定修正。
  - 检查 3：`~/CLAUDE.md` 删可推导内容（源码目录树 12 行、`OS: Darwin 24.6.0`（**且已过期**，实际 25.5.0）、`Shell: zsh`、Node 具体版本号、`.claude/` 表行）。7,894 → 7,023 字符。六段纪律与阿里云镜像条全部保留并逐项核验。
  - 检查 4：判定**不迁移**——证据契约属行为护栏，懒加载存在「该管时没加载」失效模式，省 550 est. tokens 不值。
  - 检查 5：`retry-guard.sh`（每次 Bash 阻塞）中位 62ms 健康，但窗口内 **1 次撞 5s 超时**（`hook_cancelled` + `timedOut`）；`read-tracker.sh` 70ms 健康；`bug-detector.sh` 无耗时记录（静默成功不落盘），配置检查判为轻量。
  - 检查 7：native 官方端点 `downloads.claude.ai` 从本机 shell **二次 12s 超时**；npm 侧旁证 2.1.274 与安装版一致。
  - 检查 8：`permissions.defaultMode` 三级作用域均未设 → 写入用户级 `"auto"`。
  - 检查 9：窗口内 6 次拒绝**无一符合白名单条件**（`cd` ×4 中 3 次是 `automode-unavailable` 瞬态；`mkdir`/`python3` 属写操作与解释器执行，永不进白名单）→ 无提案。
- **自动更新 ✘ 报警消除**：grep native 二进制定位机制——横幅由本体渲染，数据源 `~/.claude/.last-update-result.json`（二进制内 `L()` 返回该路径、`E()` 读其状态）；`DISABLE_AUTOUPDATER` 为本体认识的开关。遂在 `~/.claude/settings.json` 的 `env` 设 `DISABLE_AUTOUPDATER=1`，并将陈旧 state 文件移为 `.bak-doctor-20260917`。新进程验证：`Last update attempt: none recorded`、`No installation issues found.`
- **caixin-data MCP 移除**：先把配置块备份至 `~/.claude/backup-mcp-caixin-data-20260917.json`（权限 600，含 1 项 env，值未打印），再以 `claude mcp remove caixin-data -s user` 由应用自己写 `~/.claude.json`（避开手改的并发覆盖风险）。用户级 `mcpServers` 现为空。

## 做出的决策

| 决策 | 原因 | 影响 |
|------|------|------|
| 旧版本走废纸篓而非 `rm`，且保留 `2.1.272` | 可逆优先；native 回滚靠把 symlink 指回旧目录，目录没了只能联网重下 | 少省 201M，换回滚能力 |
| **不撤** `DISABLE_AUTOUPDATER`，手动更新、不设提醒 | ✘ 触发条件是「有一次失败尝试」；后台更新只要在网络不通时刻跑一次横幅即复现。手动路径 Doctor 已验证可用，代价为零 | 从此无新版提醒，更新须主动跑 `claude update` |
| 记忆真源判给 brain，`memory/` 降为辅助记录 | 与 `memory/brain-vs-memory.md` 裁定及双轨声明一致 | `~/CLAUDE.md` 的 `## Identity` 段整段替换为 `## Memory` 段；身份与称呼交 `~/.claude/CLAUDE.md` 单点负责 |
| 检查 4 不做懒加载迁移 | 行为护栏懒加载＝静默失效风险 > 550 tokens 节省 | 常驻上下文保持现状 |
| `caixin-data` 直接 remove 而非逐项目 disable | Doctor 明示「省的每个对话都要打」；`/mcp disable` 实测只作用于执行时 cwd 所在项目 | 配置已删，恢复须按备份文件用 `claude mcp add` 重建 |
| 所有 settings 写入走 mktemp + 原子 replace + 备份 | 避免把值拼进 shell 命令行；避免半写坏文件 | 三份备份留作回滚入口 |

## 踩到的坑（本场实测）

- **`/mcp disable` 是按项目生效，且落在执行时的 cwd 项目**：Doctor 在 `~` 下执行，开关写进了 `projects["/Users/lunarabbit"].disabledMcpServers`，本项目 `Documents/Codex` 仍加载该 MCP。这也是最终改用 `claude mcp remove` 的直接原因。
- **横幅不会自动刷新**：清掉 state 文件后 ✘ 仍在，因当前会话进程读的是**启动时快照**，须退出重开。（缓存时机为推断，未从二进制取到调用上下文）
- **token 估算基准差异**：先前按字节/4 报数，规范是字符/4；中文文件两者差约 36%（`~/CLAUDE.md` 9,545 字节 / 7,023 字符）。中文真实密度高于字符/4，故两数当区间端点看。
- **`grep -I` 会跳过二进制**：首轮在 native 安装目录搜 "Auto-update failed" 零命中，误以为不是本体渲染；改 `grep -a` 后 3 处命中。

## 遗留问题 / 待办

- [ ] 重开一次会话以让 ✘ 横幅与已卸载的 caixin 工具一起从上下文消失
- [ ] 2026-10-02 到期：确认 CLI 无异常后清空 `~/.Trash/claude-versions-20260917`（260M；已登记在 `memory/pending-maintenance.md`，但按本场确立的真源规矩，该长期待办应改挂 brain/TODO.md）
- [ ] `~/CLAUDE.md` 的 `## Session Log Checklist` 未提 Brain（真源改判后不矛盾，但两份开工清单仍分处两文件）—— 是否合并待 Doctor 定
- [ ] `memory/environment.md` 可能抄了同一个过期的 `Darwin 24.6.0`
- [ ] `retry-guard.sh` 若再撞 5s 超时需查阻塞点
- [ ] 残留无害项：`projects["/Users/lunarabbit"].disabledMcpServers` 仍指向已删除的服务器（清它要手改 `~/.claude.json`，风险 > 收益，建议不动）
- [ ] Cowork 桌面端共用 `~/.claude`，若其自行发起更新并失败会重写 state 文件、横幅复现；`DISABLE_AUTOUPDATER` 对桌面端是否生效**未核**

## 回滚入口

| 备份 | 内容 |
|------|------|
| `~/.claude/settings.json.bak-doctor-20260917` | 今日任何改动之前 |
| `~/.claude/settings.json.bak2-doctor-20260917` | 加 `DISABLE_AUTOUPDATER` 之前（含 defaultMode + skillOverrides） |
| `~/CLAUDE.md.bak-doctor-20260917` | 精简之前（该文件不在 git 下，备份是唯一还原路径） |
| `~/.claude/.last-update-result.json.bak-doctor-20260917` | 陈旧失败状态（恢复它＝恢复那条 ✘） |
| `~/.claude/backup-mcp-caixin-data-20260917.json` | caixin MCP 配置（600 权限） |
| `~/.Trash/claude-versions-20260917/2.1.223` | 旧版本目录，观察期至 2026-10-02 |

## 相关笔记

- [[brain-vs-memory]]
- [[全局偏好-Settings镜像]]
