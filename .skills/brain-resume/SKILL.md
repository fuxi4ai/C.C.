---
name: "brain-resume"
description: "Restore working context at the start of a session. Trigger when the user types `/resume` or says \"恢复上下文\", \"继续上次\", \"上次干到哪了\", \"接着昨天\". FIRST loads global collaboration preferences (Settings mirror — incl. addressing Doctor as 「您」) to close the G-X13 blind spot, then — if the ElevenLabs voice bridge is available — speaks a short spoken handoff, then reads the most recent 3 session logs from `~/Documents/Claude/brain/logs/`, plus the active project's architecture overview and decisions, then outputs a structured handoff: last project worked on, key decisions, outstanding TODOs, and three suggested next steps."
---

# brain-resume — 恢复跨 session 工作上下文

## 触发

- `/resume`
- "恢复上下文" / "继续上次" / "接着昨天" / "上次干到哪了"

## 执行步骤

### Step 0 · 载入全局协作偏好（每次必做 · 堵 G-X13 盲区）

Cowork / `/resume` 起手**不自动载**全局协作偏好，极易漏「对 Doctor 一律用『您』」等全局规则（G-X13）。所以在做任何事之前，先读一眼镜像并认领：

```bash
cat ~/Documents/Claude/brain/permanent/全局偏好-Settings镜像.md
```

认领其中的全局条后再往下——尤其：**称呼 Doctor 一律用敬语「您」**、改既有资产 propose-then-confirm（范围限定：方向性/判断性/无既定最优解的修改走三步；事务性/文件性/存在明确最佳解且无需人工判断的 TODO 适用常驻自动授权）、可逆优先（不删文件）、不在沙箱跑 git 写命令、需 Doctor 拍板的事走 AskUserQuestion（正文给推荐/不推荐+理由）、不选边不谄媚、裸数字＝实指。
镜像文件缺失则退读 `~/Documents/Claude/brain/permanent/Doctor协作偏好.md`。

### Step 0.5 · 起手开声（语音链路可用则先出一段 · 堵起手哑口盲区）

载完全局偏好后，若 ElevenLabs 桥接可用：**先**按音色 C.C.（voice_id `C7iLuTwlT58pHXVmnmWe` · `eleven_v3` · zh · stability 0.5 · speed 1.0）出一段 ≤150 字口语短版（「已恢复上下文」之类），落 `~/Documents/Claude/.tts-scratch`，再往下做 resume。链路不可用则静默跳过。
语音无后台自动触发器、须每轮主动调 TTS——**起手这一下最易漏**（注意力全在 resume 正文），故在流程里显式固化。

### Step 1 · 读最近 3 篇会话日志

```bash
ls -t ~/Documents/Claude/brain/logs/*.md \
      ~/Documents/Claude/brain/logs/[0-9][0-9][0-9][0-9]-[0-9][0-9]/*.md 2>/dev/null | head -3
```
把这 3 个文件全文读入。

> ⚠ **必须带上 `logs/YYYY-MM/` 子目录**：`meditation.fold_logs` 每月 1 号把上月日志折进子目录，月初根目录可能不足 3 篇——只扫根目录会在**每月 1 号前后静默读不满 3 篇**。刻意不用 `find` 全递归：那会把 `checkpoints/`（PRD）和 `checkups/`（体检报告）混进"最近会话日志"。

### Step 2 · 识别活跃项目

从日志的 `project:` frontmatter、文件名主题、或正文中提取最近活跃的项目名（DVA / 龙鱼五力 / 渊图 / O MY HTML / PEC / 海螺姑娘 / 司南）。

若识别到，读：
```
~/Documents/Claude/brain/{项目名}/architecture/系统概览.md
~/Documents/Claude/brain/{项目名}/architecture/决策记录.md
~/Documents/Claude/brain/{项目名}/GOTCHAS.md
```

### Step 3 · 扫 TODO 顶部

读 `~/Documents/Claude/brain/TODO.md` 的"待办"段。

### Step 3.5 · git 账核实（日志或 TODO 出现 git 待办时必做 · 堵「已跑当未跑」盲区）

Doctor 常在会话后自行把贴过的 git 命令跑掉、且不一定回来说（2026-08-15 实证：08-14 三场日志全写「git 待 Doctor 终端」，实际五仓已全部 commit）。因此**凡 Step 1 日志的遗留待办或 Step 3 TODO 里出现 git commit / push / 「待 Doctor 终端」类条目，先核实再开口**：

```bash
python3 ~/Documents/Claude/brain/.skills/brain-resume/gitcheck.py <repo1> [repo2 ...]
```

- **仓清单按日志项目筛**：brain `~/Documents/Claude/brain`；渊图 `~/Documents/Database/行业研究`；白泽观星 `~/Documents/Claude/Projects/Financial/白泽观星`；剑酒青丘回测报告 `~/Documents/Claude/Projects/Financial/剑酒青丘`；剑酒青丘数据 `~/Documents/Database/剑酒青丘`；白泽大宗 `~/Documents/Claude/Projects/Financial/白泽大宗`；风险日报（本地-only·无远端，脚本自动跳过 push 判定）。沙箱环境先按挂载映射翻译路径。
- 脚本**只读 .git/ 纯文本**（index/HEAD/对象库/logs/HEAD/refs），绝不跑任何 git 子命令——沙箱硬约束，Mac 原生也可跑（纯标准库）。
- **结果处置**：该仓 `staged-uncommitted: none` 且 `worktree modified: 0` → 视为已同步，摘要里**不再提出**该 git 待办；TODO 中对应条目的 git 子项**直接勾掉**（Doctor 2026-08-15 授权：已同步即勾，不必再问）——用 Edit 把状态行 `- [ ]` 改 `- [x]`，行尾留痕「已核实（gitcheck.py · YYYY-MM-DD）」，不整条删内容。有改动或未 push → **直接贴整合命令**（多仓合并一个 code block 分段连发），不写「待 Doctor 终端」空话。
- 说「已核实已提交」前答两问：①脚本真跑过没有；②内容级比对覆盖了 tracked 文件没有——mtime 探测不算数（挂载层 sub-second mtime 与 index 整秒缓存必误报，脚本内已做内容哈希兜底）。隐患：pack 里的 delta 对象脚本会拒读（commit/tree 极少 delta，实测五仓 HEAD 全可读）。

### Step 4 · 输出结构化摘要

```
**上次工作**：{项目名} · {日期}

**关键决策**（最多 3 条）：
- ...

**遗留待办**（最多 5 条）：
- [ ] ...

**建议下一步**（3 条具体动作）：
1. ...
2. ...
3. ...

需要我从哪一项开始？
```

## 边界

- `logs/` 为空 → "brain 还没有会话日志。要不要我读 `permanent/项目总览.md` 给您看 8 个项目的整体状态？"
- 识别不到项目 → 只输出全局摘要，问 Doctor 想进入哪个项目
- **不**一次性读项目全部文档——只读 architecture/系统概览/决策记录/GOTCHAS
- 所有路径用绝对 `~/Documents/Claude/brain/...`
- Step 0 全局偏好每次起手必载，不因"上次读过"跳过（会话间不延续）
- resume 起手第一轮默认开声（语音链路可用时）；不可用静默跳过
- Step 3.5 git 核实是「察觉到 git 待办」的前置条件：没核实不得把 git 待办当残留提给 Doctor；核实工具=skill 目录内 `gitcheck.py`（只读 .git 纯文本，禁 git 子命令）。已同步 → 不再提出 + 直接勾 TODO 对应条目（Edit 改状态行并留痕，Doctor 授权）
