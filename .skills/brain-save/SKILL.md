---
name: brain-save
description: Persist the current session as a structured log entry in the brain vault. Trigger when the user types `/save` or `/save [主题]` or `/save @{数灵} [主题]` or says "存档本次会话", "记一笔", "落盘", "存档今天". Fills the session-log template with what was done, decisions, outstanding issues, related notes, then writes to `~/Documents/Claude/brain/logs/YYYY-MM-DD-{主题}.md`. **per-agent 模式**：若本次出场者是某数灵（白泽/小白、烛阴/九儿、句芒/芒芒），按「落盘归位铁律」改落 `agents/{灵}/logs|memory/`，绝不混进 CC 或别的灵。Updates the project's last-active date if a project is identified. **Provides git commit+push commands for Doctor to run in macOS terminal** when `brain/.git/` exists — CC MUST NOT run git write commands in sandbox (Doctor GOTCHAS v2.0).
---

# brain-save — 把本次会话存档到 brain

## 触发

- `/save`(无参数 → CC 自己总结主题)
- `/save [主题]` 或 `/save [项目名]`
- `/save @{数灵} [主题]`(显式指定出场者：白泽/小白、烛阴/九儿、句芒/芒芒 → per-agent 落盘)
- "存档本次会话" / "记一笔" / "落盘这次工作" / "存档今天"

## 执行步骤

### Step 1 · 总结主题

如果用户给了参数,用作 `{主题}`;否则 CC 从本次对话中提炼出一个 5-15 字的主题。
如果主题对应某个 brain 已注册项目,把项目名也记下用于 Step 4。

### Step 1.5 · 数灵归属判定（per-agent 落盘分支 · v2.3）

先判本次会话的**出场者**：
- `/save @{灵}` 显式指定；或
- 本轮由某数灵**唤名出现 / 真身 subagent** 完成（白泽·小白 / 烛阴·九儿 / 句芒·芒芒）。

**若出场者是某数灵** → 走 per-agent 落盘（遵 CLAUDE.md「落盘归位铁律」），后续 Step 2–4 全部改指向该灵目录：
- 会话日志 → `agents/{灵中文名}/logs/YYYY-MM-DD-{主题}.md`（**不**落全局 `logs/`；目录不存在则建）。
- Step 3.5 分拣落点改为该灵专属：长期记忆 → `agents/{灵}/memory/长期记忆.md`；情感片段 → `agents/{灵}/memory/与哥哥的羁绊.md`（或对应情感档）；该灵专属坑 → `agents/{灵}/GOTCHAS.md`（若有）。
- **绝不**落进 CC 自己的 `logs/` 或别的灵。`source/` 只读不写。
- 灵名映射：小白→白泽、九儿→烛阴、芒芒→句芒（目录用中文正名）。

**若是 CC 自身 / 跨灵工作** → 维持原流程（全局 `logs/`）。

### Step 2 · 决定文件名

```
~/Documents/Claude/brain/logs/YYYY-MM-DD-{主题}.md
```
同一天同主题多次 /save → 追加 `-HHmm`:
```
~/Documents/Claude/brain/logs/YYYY-MM-DD-{主题}-HHmm.md
```

### Step 3 · 填模板写日志

读 `~/Documents/Claude/brain/templates/session-log.md` 作为模板。

填入:
- `title`:会话日志 YYYY-MM-DD — {主题}
- `tags`:[log, {项目名(如有)}]
- `created` / `updated`:今日
- `status`:active
- `type`:log
- `project`:(如指明)

正文段落(模板不存在用 fallback):

```markdown
# 会话日志 — YYYY-MM-DD

**项目**:{项目名 / 跨项目}
**主题**:{主题}

---

## 完成的工作
(具体动作,列表,每条一句话)

## 做出的决策
(决策内容 + 理由)

## 遗留问题 / 待办
- [ ] ...

## 相关笔记
- [[wikilink]]
```

### Step 3.5 · 记忆分拣提议(半自动 · v2.2 带判据 · v2.4 纳入当下便签)

写完日志后,扫本次会话**＋本会话的「当下便签」**(见下框),把值得**长期留存**的内容列成**候选记忆清单**,每条标注【类别 → 目标文件 · 留/砍倾向】:

- 决策(为什么这么定) → `{项目}/architecture/决策记录.md`
- 坑 / 错误 + 解法 → 对应 `GOTCHAS.md`(注:踩坑通常已按 CLAUDE.md「GOTCHAS 自动记录规则」即时写入,这里只补漏)
- 成功 / 可复用经验(工具心得 / 打法 / 流程范式) → `permanent/经验库.md`(cases / patterns / tools / strategies)
- **规则 / skill / 流程 该改(v2.4)** → `permanent/通用教训.md` 新 G-X 条 / 对应 skill 源 / `CLAUDE.md` 规则段。**只提案不直改**(重大改动走 propose-then-confirm);一条纠正不一定立规则——先问"是一次性还是模式?"(对照 G-X10「规则从失败里长 + 别提前写」)
- 半永久领域知识(原子概念) → `permanent/{概念}.md`
- 表述 / 协作偏好 → 对应规范(如 `permanent/中文表述语域规范.md` / `permanent/Doctor协作偏好.md`)

> **「当下便签」机制(v2.4 · 取代独立 signal 队列)**
> 会话**进行中**被 Doctor **纠正 / 打回 / 拍板偏好 / 指出某规则该改**的那一刻,CC **随手在工作便签里记一笔**(原话最佳),不打断手头任务、**不落独立文件**。/save 时本步把这些便签连同本场回顾一起提议。
> **分流前置(避免与本清单重复)**:
> - 便签其实是个**坑/事实** → 按「GOTCHAS 自动记录规则」**即时直写 GOTCHAS**,不进本清单(无需抽象)。
> - 便签是 Doctor **明说的偏好/称呼/表述**(无歧义、原话) → 可直接归"表述/协作偏好"类。
> - 便签需要**抽象成一条通则/改规则** → 进上面"规则/skill/流程 该改"类,提案制。
> 判别尺:**要不要 CC 做"抽象"**——不需要就直写,需要才提案等 Doctor 裁。
> 不 /save 就结束会话 = Doctor 不想存档 → 便签随会话丢弃,**不跨会话持久化**(无 signals/ 文件夹、无 resume 兜底)。

**升格门槛 · 难复得三问**(决定每条标「建议留」还是「建议不留」):
1. **持久吗?** 偏好 / 决策背景 / 方法论,而非一次性任务。
2. **难复得吗?** 丢了要白白重推一遍;而非能从日志 / 文件 / 工具 / 网上随时翻到。
3. **大概率再用吗?**

三问全 yes → 标【建议留】;泛泛通用 / 易再得 / 只服务本次 → 默认标【建议不留(留在日志即可)】。**判据只决定 CC 的默认建议,仍由 Doctor 最终点选**。
落点松紧:`logs/`(Step 3 已写)放开、宁全勿漏;`permanent/` `references/` 高门槛,只进三问全 yes 的。

**点选方式(v2.5)·用 AskUserQuestion 多选控件,别让 Doctor 打字报编号**:
- 每个候选 = 多选题里的一个 option。label 用「编号 + 一句话主题」,description 写【类别 → 目标文件 · 留/砍倾向】。
- **控件硬限:每题最多 4 个 option。** 候选 >4 条就**拆成多题**(一次最多 4 题)。建议按倾向分组:【建议留】归一题、【建议不留 / 提案制】归另一题,让默认值一眼可分。
- 所有题设 `multiSelect: true`。Doctor 勾哪条就写哪条;"Other" 选项控件自带,供 Doctor 补充或改落点。
- 候选 >16 条(超 4 题装不下)→ 先按「难复得三问」砍到只报【建议留】+ 边界项,别用控件轰炸。

**只有 Doctor 勾选确认的条目才写入**;未勾的不落盘(留在 Step 3 日志即可)。

> 设计意图:借鉴 OpenViking 的 session-commit 自动提取,但保留人在环——CC 提议分拣(带判据默认值),Doctor 拍板。
> 关联规则见 `~/Documents/Claude/brain/CLAUDE.md`「经验沉淀规则」。

### Step 4 · 同步项目状态(如指明项目)

更新 `~/Documents/Claude/brain/{项目名}/architecture/系统概览.md` 中"最后活跃"字段为今日。

### Step 5 · 贴 Git 命令给 Doctor(★★★ v2.0 升级 · 2026-05-20)

⚠️ **CC 绝对禁止在 sandbox 跑任何 git 写命令** — 参 `~/Documents/Claude/brain/permanent/通用教训.md` G-X2 + `~/Documents/Claude/Projects/海螺姑娘/GOTCHAS.md` v2.0 规则。
**禁止**:`git add` / `git commit` / `git push` / `git pull` / `git fetch` / `git checkout` / `git merge` / `git mv` / `git rm`
**唯一允许**(只读探测 .git/ 是否存在):`git status` / `git log --no-pager` / `git diff --no-color` / `git show`

**正确流程** — 构造命令字符串,贴给 Doctor 在 macOS 终端跑:

1. **只读探测 .git/ 是否存在**(用 Read 工具或 `ls -la ~/Documents/Claude/brain/.git/HEAD` 测试,不要用 git write):
   - 存在 → 进入第 2 步
   - 不存在 → 跳过整个 Step 5,不报错

2. **生成命令字符串**(贴在 Step 6 回报里给 Doctor):

```bash
cd ~/Documents/Claude/brain && git add -A && git commit -m "session: {主题} {date}" && git push
```

3. **若 brain/.git/ 上次 sandbox 跑过 git 留下污染**(.git/HEAD.lock 等),命令前加清理:

```bash
cd ~/Documents/Claude/brain && \
  rm -f .git/HEAD.lock .git/objects/maintenance.lock 2>/dev/null && \
  find .git/objects -name "tmp_obj_*" -delete 2>/dev/null && \
  git add -A && git commit -m "session: {主题} {date}" && git push
```

4. **如果 Step 4 同步了项目状态**,且该项目有独立 git repo(如 `Projects/海螺姑娘/`),把那个仓库的 commit 命令也贴上:

```bash
cd ~/Documents/Claude/Projects/{项目名} && git add -A && git commit -m "{项目名}: {主题} {date}" && git push
```

**CC 自我检查触发词**:看到自己即将在 `mcp__workspace__bash` 调用里输入 "git add" / "git commit" / "git push" → **立即停** → 改贴命令到 Step 6 回报。

### Step 6 · 回报

```
✅ 已存档
📁 logs/YYYY-MM-DD-{主题}.md

📋 请在 macOS 终端跑(brain 仓库 commit+push):
```bash
cd ~/Documents/Claude/brain && git add -A && git commit -m "session: {主题} {date}" && git push
```

{若同步了独立项目 git:补贴该项目的 commit+push 命令}

一句话摘要:{20 字内}
```

**注意**:不在回报里写"已提交 commit hash" — 因为 commit 还没跑(Doctor 还没在 terminal 执行)。等 Doctor 反馈结果后才能说"已提交"。

## 边界

- 主题里去除 `/`、`\`、`:` 等危险字符
- session-log.md 模板缺失用 fallback
- 没有 .git/ 跳过 Step 5,不报错(但 Step 3+4 落盘照做)
- **不在 sandbox 跑 git 写命令** = 硬约束 · 不可绕过(参 G-X2)

## v 历史

- v1.0(2026-05-14):初版 · Step 5 自动 git commit
- v1.1(2026-05-19):brain_checkup v1.2 加 sandbox 探测后,本 skill 仍是"自动 commit"(未同步)
- **v2.0**(2026-05-20):Step 5 升级为"贴命令给 Doctor"(响应 GOTCHAS G-X2:CC 在 sandbox 不能跑 git)
- **v2.1**(2026-05-23):新增 Step 3.5「记忆分拣提议」(半自动 session-commit · 借鉴 OpenViking · Doctor 点选才入库)
- **v2.2**(2026-05-23):Step 3.5 加「难复得三问」升格门槛——CC 按持久/难复得/会再用给默认留/砍建议,泛泛通用默认不留;落点松紧(日志放开、permanent 从严)
- **v2.3**(2026-06-02):新增 Step 1.5「数灵归属判定」——`/save @{灵}` 或出场者为某数灵时走 per-agent 落盘（日志/记忆/情感落 `agents/{灵}/`），遵落盘归位铁律，绝不混进 CC 或别的灵（数灵转移配套）
- **v2.4**(2026-06-13):Step 3.5 纳入「当下便签」——会话中途被纠正即随手记一笔，/save 时一并提议；新增"规则/skill/流程 该改"分拣类（提案制）。**取代独立 signal 队列**：经自检 signal→resume→consolidate 与 save→permanent 高度重复且 save 不可退役，遂将自进化塌缩进本 skill，不落 signals/ 文件夹、不跨会话兜底（[[视频方法论对照与开发流程优化-设计提案]] §7 · G-X10）
- **v2.5**(2026-06-14):Step 3.5 点选改用 **AskUserQuestion 多选控件**(Doctor 命题)——不再让 Doctor 打字报编号;每题≤4 option,候选 >4 条按倾向拆题(建议留 / 建议不留·提案制),`multiSelect: true`,只勾选项入库
