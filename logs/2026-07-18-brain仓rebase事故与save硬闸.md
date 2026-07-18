---
title: 会话日志 2026-07-18 — brain 仓半开 rebase 事故与 brain-save v2.8 硬闸
tags: [log, brain, git, skill]
created: 2026-07-18
updated: 2026-07-18
status: active
type: log
project: brain
---

# 会话日志 — 2026-07-18

**项目**：brain（工具链自身）
**主题**：/save 撞上先前会话遗留的未完成 rebase → 事故收尾 → brain-save v2.8 补硬闸
**承接**：[[2026-07-18-渊图帕米尔15篇入库与provenance根治]]（本次事故发生在那次 /save 的 git 提交环节）

---

## 完成的工作

### 事故发现

- 渊图 /save 后按 skill Step 5 给出 `git add -A && git commit && git push`，Doctor 执行 → commit 成功（`8991c83`）但 **push 报 `fatal: You are not currently on a branch`**。
- 诊断发现不是普通 detached HEAD，是 **`interactive rebase in progress; onto 7e34c27`** —— 一个**先前会话遗留的未完成 rebase**（内容为「回调级别判别器+日报UI定版」「句芒课件入库审核」，属烛照九阴与句芒的工作，与本次渊图会话无关）。
- 我的 commit 落在 rebase 中间态的游离 HEAD 上，不属于任何分支。

### 事故收尾（Doctor 终端执行，CC 全程只读诊断）

1. `git tag save-20260718-provenance 8991c83` —— 先拴住游离 commit（无脑正确的第一步）
2. 判清 abort 的代价：三个待 pick 的 commit **都还挂在 `main` 上**（`main` = `4c92ea6` 未动），abort 不丢工作 → 建议 abort 而非 continue（原 rebase 意图无从确认）
3. `git rebase --abort` → `git cherry-pick save-20260718-provenance` → 我的 /save 接回 main
4. push 被拒（分叉 5 vs 1）→ `git pull --rebase`
5. **在 `logs/2026-07-18-回调级别判别器.md` 冲突** —— 这正是原 rebase 卡住的地方
6. 比对两版：本地 `e9ecaac` 是远端 `7e34c27` 的**超集**（多出「追加(同日 · 情绪周期春判据审查)」整段，含 Doctor 裁定「可以接受，维持现状不改」+ 预注册 0729 核春 fwd10）→ 取本地版
7. `git rebase --continue` → `Successfully rebased` → push `7e34c27..d5aa9d6` → 删临时 tag

### skill 补丁

- 写 **brain-save v2.8**，新增 **Step 5.0「仓库状态前置探测」硬闸**：`.git/rebase-merge` / `.git/rebase-apply` / `MERGE_HEAD` / `CHERRY_PICK_HEAD` / `REVERT_HEAD` / `BISECT_LOG` / detached HEAD 任一命中即停、不给 commit 命令、改报状态；**落盘（Step 3/4）照做**——文件写入与 git 提交是两件事。
- 附带两条：① 只读白名单补 `git ls-files` / `git branch -av`，并注明 `git --no-pager log` 才是通用写法（今天写反了直接报 `unrecognized argument`）；② Step 5 新增第 5 条——给 Doctor 的验证命令**盯内容标识、别盯会变的计数**。
- 打包 `brain-save.skill` + 裸 `SKILL.md` 交 Doctor 安装（skill 缓存只读，CC 改不了）。

---

## 做出的决策

| 决策 | 原因 | 影响 |
|------|------|------|
| 先 tag 再动任何 git 操作 | 游离 commit 只要有具名引用就丢不了，代价为零 | 后续 abort 无后顾之忧 |
| 选 abort 而非 continue | 原 rebase 意图无从确认，continue 会按未知意图产出历史；且经核实 abort 不丢工作（三个 commit 都还在 main 上） | main 回到干净状态，重新走一次 pull --rebase |
| 冲突取**本地版**、拒绝 `--skip` | 本地是远端超集，多出 4 行含 Doctor 裁定与预注册；git 的 hint 主动建议 `--skip`，照做即丢 | 春判据审查裁定保住 |
| 不用 `push -f` | 本地内容确是远端超集、强推一步到位，但 `7e34c27` 是另一机器/会话推的，强推改写他们看到的历史 | 多解一次冲突，换掉一个不必要的风险 |
| skill 只补「往半开仓库 commit」这一条 | G-X10：规则从失败里长、别提前写。今天只失败了这一件 | 未把「定期扫仓库状态」写进 /save（那是 brain_checkup 的职责） |

---

## 遗留问题 / 待办

- [ ] brain-save v2.8 待 Doctor 从 Settings → Capabilities 安装（本次 /save 加载的仍是 v2.7）
- [ ] 半开仓库的**主动发现**仍无人负责——v2.8 只保证 /save 不往里塞东西，不保证有人去收尾。若要根治需 brain_checkup 之类定期扫所有 brain 相关仓状态（G-X10 原则下暂不预写）
- [ ] 今天这个 rebase 是哪个会话开的、原本想做什么，至今未知；若那个会话还有后续意图需自行恢复

---

## 相关笔记

- [[2026-07-18-渊图帕米尔15篇入库与provenance根治]]
- [[通用教训]] · G-X2（sandbox 禁 git 写）· G-X68（先穷尽最平凡的解释）· G-X70（安装命令前确认渠道）
- [[经验库]]
