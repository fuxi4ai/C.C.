---
name: "brain-save"
description: "Persist the current session as a structured log entry in the brain vault. Trigger when the user types `/save` or `/save [主题]` or `/save @{数灵} [主题]` or says \"存档本次会话\", \"记一笔\", \"落盘\", \"存档今天\". Fills the session-log template, then writes to `~/Documents/Claude/brain/logs/YYYY-MM-DD-{主题}.md`. **per-agent 模式**：出场者为数灵（白泽/烛阴/句芒）时改落 `agents/{灵}/logs|memory/`，绝不混进 CC 或别的灵。**CC MUST NOT run any git subcommand in sandbox** — provides commit+push commands for Doctor's terminal, and MUST probe for in-progress rebase/merge/cherry-pick first (v2.8). **写 `permanent/经验库.md` 或 `通用教训.md` 时必须定位到对应 `##` 节插入、禁 append 文件尾；编号先 grep 探再取 max+1，禁心算（v3.0）。勾掉的 TODO 条目整块迁入 `references/TODO-已完成归档.md`；判断性勾项 CC 只搬运已勾的、不代打 ✓（G-X4 · v3.1），客观 TODO 证据硬按常驻授权代勾留痕（G-X136）。Step 4 项目状态同步遇 `architecture/系统概览.md` 不存在时必须明确报告、禁静默跳过、禁自动补建 stub（v3.2 · v3.2.1 订正名单）。**"
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
- **理由上聊天、选项保简洁(v2.6)**:每条候选的「**推荐 / 不推荐 + 难复得三问理由**」**写在 /save 的聊天正文**里讲清楚、让 Doctor 据此判;AskUserQuestion 的 option 只放简洁标签(推荐/不推荐 + 一句话主题),**别把理由只埋进 description**。
- **选项必带（推荐/不推荐）标签(v2.7·硬性 · v3.3 订正位置)**:每个 option 的 **label 文字尾部**直接跟（推荐）或（不推荐）——**写在选项后面，不许只放 description**（控件里 description 可能折叠/不显眼，label 才是一眼处）。这是 [[Doctor协作偏好]]「待裁事项的呈现方式」全局规则在本 skill 的实例——**不限 /save，凡 CC 给 Doctor 的待裁选择题一律照此**(详细理由上正文 + 多选 + 选项 label 尾部加推荐标签)。Doctor 明示(2026-06-14 立 · 2026-08-02 订正位置)。

**只有 Doctor 勾选确认的条目才写入**;未勾的不落盘(留在 Step 3 日志即可)。

**⛔ 写入位置铁律(v3.0 · 2026-07-30 立)——「归哪类」不等于「写到哪」**

上面只规定了**目标文件与类别**,没规定**插到文件的哪一处**,于是历次 /save 一路 append 到文件末尾。实测代价:`经验库.md` 267 条里 **137 条(51%)** 落在了与自身类别不符的位置,`## 相关` 收尾节被压在 640 行之下,`strategies` 节沦为杂物间。**光靠"标了类别"防不住,必须规定落点**:

- **写 `permanent/经验库.md`** → 定位到该条类别对应的 `## {cases|patterns|tools|strategies}` 节,**插入该节最后一条之后、下一个 `## ` 之前**。**绝不 append 到文件尾**(文件尾是 `## 相关`,那是收尾节)。
  - 新条目**一律用编号后缀编码类别**:`### [EXP-YYYYMMDD-NNN-P]` = patterns · `-T` = tools · `-S` = strategies · cases 无后缀。**后缀是权威**;`**类别**:` 字段是旧写法,新条不必再写(存量保留)。
  - 插入前先 `grep -n '^## ' permanent/经验库.md` 拿到节边界,别凭记忆。
  - **取号必先探,禁凭「今天第几条」心算**:`grep -o "EXP-{今天日期}-[0-9]\{3\}" permanent/经验库.md | sort -u` 取当日已用序号,新号 = **max+1**。**并发会话各自心算必撞号**——实测存量已有 **14 组重复编号**(每组两条内容毫不相干),其中 6 组已被外部引用、**11 处引用因此歧义**(如 `EXP-20260707-001-P` 名下同时挂着「Cowork 多卡看板性能」和「弱势 regime 禁用底部扳机」)。编号是引用锚点,撞号＝锚点失效。
- **写 `permanent/通用教训.md`** → 新条追加到**文件末尾的 G-X 区**。标题格式 **`## [G-Xnn] 标题`——带方括号,且方括号后直接跟标题、不加 `·` 分隔**。2026-07-30 已把 31 条全统一成这个形态(此前 G-X74~96 那 21 条写作 `## G-Xnn · 标题`,两种混用会让 `[[通用教训#G-Xnn]]` 锚点时灵时不灵)。
  - **前 8 个主题节(数据治理/代码工程/… · 粗体条目、无独立编号)是历史层,只读不追加**。新知识一律进 G-X 区。
  - 取号同经验库:`grep -oE '^## \[G-X[0-9]+\]' permanent/通用教训.md | sort -V | tail -1` 看已用到几号,取 **max+1**,**别心算**——G-X100 与 G-X106 就撞过一次,靠事后 /consolidate 才发现,而那时已有两处历史引用指错。
- **通则**:凡目标文件内部有分节结构,写入前先读节标题、定位对应节;**"追加到文件末尾"只在文件确实以待追加区结尾时才合法**。

> 这条是 /consolidate 2026-07-30 从存量里反推出来的:结构崩塌不是某次写错,是**默认落点缺省**在几个月里累积的必然结果。不改这条,清理完过几个月还会再崩一次。

**⛔ 完成即迁(v3.1 · 2026-07-30 立)——上面管「写进来往哪放」,这条管「勾掉了往哪去」**

`TODO.md` 里一条办完了,**就地打勾但不搬走**,几个月后就成了:39KB 文件里 **70% 是已完成条目**,11 条真待办淹在 44 条已完成里,而 `/resume` 每场都要把整篇读进 context——token 花在已经做完的事上。规矩:

- **勾掉一条 → 把它整块(标题行 + 其下所有缩进正文)移进 `references/TODO-已完成归档.md` 的 `## 已完成` 段**,按完成日期倒序。`brain/TODO.md` 只留 `- [ ]`。
- **取消 ≠ 完成**:`~~删除线~~` 或写明「取消」的条目,进归档文件的 `## 已取消` 段单列,别混进完成清单虚增战果。
- **⚠ 打勾分轨(G-X4/G-X136)**:客观、机器可验证 TODO(证据硬)**凭盘上可复核证据直接代勾留痕**(常驻授权,不占 PRD checkbox);判断性勾项——迁移已勾条目是搬运可做,给未勾条目打勾是判定,只列清单报给 Doctor 或指定独立验收方。核实中发现「疑似已办完但没勾」的,只列清单报 Doctor,由 Doctor 勾。条目自带「CC 不代勾」字样的,若属客观可验证且证据硬,按常驻授权代勾并留痕;若属判断性,碰都不碰。
- **写新 TODO 条时想一层**:这件事该进 `brain/TODO.md`(跨项目/需 Doctor 拍板)还是项目自己的 `{项目}/TODO.md`(纯项目内工程)?**两处都写会漂移、只写一处会漏**——实测 DVA 两处各记各的、完全不重叠。落点不确定时问 Doctor,别默认往 brain 塞。
- **待办必须进 TODO,不能只写在当日日志的「遗留待办」里**。`/resume` 只读最近 3 篇日志 + TODO;写在日志里的待办,一旦滑出 3 篇窗口就永久不可见。活例:抖音口播稿的审稿待办只写在 2026-07-21 日志里,**9 天没被任何一次 resume 拿到**,直到 /consolidate 翻 inbox 才捞出来。

> 设计意图:借鉴 OpenViking 的 session-commit 自动提取,但保留人在环——CC 提议分拣(带判据默认值),Doctor 拍板。
> 关联规则见 `~/Documents/Claude/brain/CLAUDE.md`「经验沉淀规则」。

### Step 4 · 同步项目状态(如指明项目)

更新 `~/Documents/Claude/brain/{项目名}/architecture/系统概览.md` 中"最后活跃"字段为今日。

**★ 文件不存在则明确报告,禁静默跳过(v3.2 · 2026-07-31 立 · 名单经 v3.2.1 逐项对表订正)**

**实测缺口(2026-07-31 按 `permanent/项目总览.md` 逐项对表)**:

| | |
|---|---|
| `项目总览.md` 注册 | **15** 个 |
| **有** `architecture/系统概览.md` | **8** 个:DVA · GlobalPercent · O MY HTML · PEC · 司南 · 海螺姑娘 · 渊图 · 龙鱼五力 |
| 注册项目里**缺** | **7** 个:MiroFish · 剑酒青丘 · **数灵转移** · 星空 · 烛照九阴 · 白泽大宗 · 称象 |
| 另有目录但**未进总览** | **风险日报**(2026-07-30 补建 `风险日报.md` stub,总览 15 行里没有它)——**同样缺** |
| ⇒ 实际无系统概览的目录 | **8 个** |

Step 4 对这些项目**一直是无声空转、无人察觉**,`dashboard-snapshot.py` 的项目卡也因此少一个信息源。改法:

- 落盘前先探路径(`ls ~/Documents/Claude/brain/{项目名}/architecture/系统概览.md`)。
- **存在** → 照旧更新"最后活跃"字段为今日。
- **不存在** → **不建、不猜、不跳过**,在 Step 6 回报里明写一行:
  `⚠ Step 4 空转:{项目}/architecture/系统概览.md 不存在,最后活跃未同步(补写需梳理项目全貌,待 Doctor 定)`
- **刻意不自动补建 stub**:系统概览是要人读的项目全貌,自动生成一个空壳会把"这个项目没有全貌文档"从**显性缺失**变成**隐性谎报**,比空转更糟——空转至少还留着一个可被发现的洞。
- 报告后**不追问、不自行补写**;补写这 8 份系统概览是独立议题,由 Doctor 择时另开。
- **上表是快照、不是权威**:引用前先自己跑一遍 `ls -d */architecture/系统概览.md`(拿"有"的集合)与 `grep -oE '\[\[[^]|]+' permanent/项目总览.md`(拿注册集合)两条命令对差集,**别照抄本表**——这正是下面那条教训的内容。

> **本条自身是 G-X111「立规矩时要扫同族实例」连栽三次的活体注脚**:
> ① 2026-07-31 首次只报了"风险日报缺",没扫同族;
> ② 同场 /save 走到 Step 4 才发现烛照九阴也缺,补扫又揪出另外 5 个,遂写进 TODO;
> ③ **本 skill 的 v3.2 初稿直接照抄了 TODO 那份名单**——而那份名单把未注册的「风险日报」算进 7 个、漏掉了已注册的「数灵转移」,总数碰巧对上、成员错一个。
> 三次都不是算错,是**拿二手名单当已核事实**。与金融线「4.70 错在日期 / 4.66 错在时点 / US10Y 错在语义」同一病根:**取一个数(或一份名单)之前先问它承诺的是什么,并重取一次对照**。

---

### Step 5.0 · ★ 仓库状态前置探测(v2.8 新增 · 硬闸 · 早于一切 git 命令)

**在生成任何 commit 命令之前**,必须先探测目标仓库是否处于「未完成操作」中。以下任一命中即为**半开状态**:

| 探测项 | 含义 |
|---|---|
| `.git/rebase-merge/` 目录存在 | interactive rebase 进行中 |
| `.git/rebase-apply/` 目录存在 | rebase / `git am` 进行中 |
| `.git/MERGE_HEAD` 存在 | merge 冲突未解 |
| `.git/CHERRY_PICK_HEAD` 存在 | cherry-pick 冲突未解 |
| `.git/REVERT_HEAD` 存在 | revert 冲突未解 |
| `.git/BISECT_LOG` 存在 | bisect 进行中 |
| `.git/HEAD` 内容**不是** `ref: refs/heads/...` | detached HEAD |

探测命令(**只用 ls/cat 读文件,不跑任何 git 子命令**——见下方铁律边界):

```bash
cd ~/Documents/Claude/brain && \
  ls -d .git/rebase-merge .git/rebase-apply 2>/dev/null; \
  ls .git/MERGE_HEAD .git/CHERRY_PICK_HEAD .git/REVERT_HEAD .git/BISECT_LOG 2>/dev/null; \
  echo "HEAD: $(cat .git/HEAD)"; \
  ls .git/index.lock 2>/dev/null && echo "⚠ 残留 index.lock"
```

需要更细的状态时,以下也都是**纯文本文件**,`cat` 即可,无需 git:

| 想知道 | 读这个文件 |
|--------|-----------|
| rebase 原分支 | `.git/rebase-merge/head-name` |
| rebase 起点 | `.git/rebase-merge/orig-head` |
| 还剩哪些没 pick | `.git/rebase-merge/git-rebase-todo` |
| 某分支指向 | `.git/refs/heads/{分支}`(或 `.git/packed-refs`) |
| 远端分支指向 | `.git/refs/remotes/origin/{分支}` |

**沙箱做不到的**:某 commit 改了什么 / diff / log 图 —— 这些要解压 git 对象,**必须构造命令交 Doctor 终端跑**。

**命中任一 → 立即停下,不给 commit 命令**,改为向 Doctor 报告:

1. 仓库处于什么状态(哪个操作未完成、`onto` 哪个 commit、原分支是谁)
2. 涉及哪些 commit(只读探测:`cat .git/rebase-merge/git-rebase-todo`;需要 log 图则构造命令交 Doctor)
3. 明确告知:**Step 3/4 的落盘已完成,仅 git 提交待仓库状态恢复后再做**
4. 若 Doctor 要求先收尾,先帮他判清「abort 会不会丢东西」再给方案——**abort 前必须确认待重放 commit 是否已在远端/在其他分支上**

**为什么设为硬闸**:半开状态下 commit,新 commit 挂在**游离的 HEAD** 上、不属于任何分支;此时若执行 `git rebase --abort` / `git merge --abort`,该 commit **立即脱离引用**——只能靠 reflog 捞回,且前提是有人知道要去捞。

> **活体教训(2026-07-18)**:CC 未探测即按老流程给出 `git add -A && git commit && git push`。彼时 brain 仓正卡在一个**先前会话遗留的未完成 interactive rebase** 上,commit 落进游离 HEAD、push 直接失败。若当时顺手 `--abort`,本次 /save 的日志 + 三条记忆升格(G-X71 等 202 行)当场蒸发。事后收尾还牵出:待重放 commit 里有一份**本地版是远端超集**的日志(多出 4 行 Doctor 裁定),若按 git 的 hint 图省事 `git rebase --skip`,那段裁定也会一并丢失。
> 一句话:**skill 只探测「有没有 .git」是不够的,要探测「这个 .git 现在能不能安全写」**。

**边界**:探测只用只读命令;**发现异常不代表 /save 失败**——文件落盘(Step 3/4)与 git 提交是两件事,仓库状态异常不该阻止内容落盘,只阻止 commit 命令的生成。

### Step 5 · 贴 Git 命令给 Doctor(★★★ v2.0 升级 · 2026-05-20)

⚠️ **CC 绝对禁止在 sandbox 跑任何 git 子命令——包括 `status`/`log`/`diff`/`show` 等看似只读的**（铁律边界订正 · 2026-07-18 · 渊图 GOTCHAS ERR-20260718-002 追加条）。

**为什么连只读也禁**:`git status` 等命令会**刷新索引并创建 `.git/index.lock`**,而沙箱**无权删除**该锁(报 `unable to unlink '.git/index.lock': Operation not permitted`),残留 0 字节孤儿锁 → Doctor 终端 commit 直接报 `Another git process seems to be running`。「只读」指的是不改工作树,不等于不碰 `.git/`。

**替代方案**:
- 核验落盘 → `grep` / `stat` / `ls`
- 探测仓库状态 → 直接 `cat` `.git/` 下的纯文本文件(见 Step 5.0 表格)
- 需要 diff / log / commit 内容 → **构造命令交 Doctor 终端**,不自己跑

**残留锁处理**(若已误跑):确认 `ps` 无真 git 进程且锁为 0 字节后,交 Doctor 终端 `rm -f .git/index.lock`。

**正确流程** — 构造命令字符串,贴给 Doctor 在 macOS 终端跑:

0. **先过 Step 5.0 仓库状态探测**(v2.8 硬闸)。命中半开状态 → 停,不进入下面步骤。

1. **只读探测 .git/ 是否存在**(用 Read 工具或 `ls -la ~/Documents/Claude/brain/.git/HEAD` 测试,不要用 git write):
   - 存在 → 进入第 2 步
   - 不存在 → 跳过整个 Step 5,不报错

2. **生成命令字符串**(贴在 Step 6 回报里给 Doctor)——**默认「先探后加」,禁用 `git add -A`**(v2.9):

```bash
cd ~/Documents/Claude/brain
git status --short                      # 先探：看清工作树全部改动
git add <本次 /save 明确改动的文件列表>   # 后加：只加本次范围内的文件，逐个列清
git diff --cached --check               # 校验暂存无冲突标记/空白错误
git commit -m "session: {主题} {date}"
git push
```
> **为什么禁 `git add -A`**(v2.9·2026-07-23 挂 TODO·G-X83 / DVA GOTCHAS GIT-20260723-001)：工作树常积压**本次 /save 范围之外**的未提交改动（别的会话/定时班遗留），`-A` 会把它们**一并混入**这次 commit，造成范围不明、难回溯。CC 在 Step 3/4 已知道本次动了哪些文件 → 直接列进 `git add`；**只有确认工作树全部改动都属本次保存范围**，才允许 `git add -A`。

3. **若 brain/.git/ 上次 sandbox 跑过 git 留下污染**(.git/HEAD.lock 等),命令前加清理(仍先探后加):

```bash
cd ~/Documents/Claude/brain
rm -f .git/HEAD.lock .git/objects/maintenance.lock 2>/dev/null
find .git/objects -name "tmp_obj_*" -delete 2>/dev/null
git status --short
git add <本次明确改动的文件列表>
git diff --cached --check
git commit -m "session: {主题} {date}"
git push
```

4. **如果 Step 4 同步了项目状态**,且该项目有独立 git repo(如 `Projects/海螺姑娘/`),把那个仓库的 commit 命令也贴上(同样先探后加):

```bash
cd ~/Documents/Claude/Projects/{项目名}
git status --short
git add <该项目本次明确改动的文件>
git diff --cached --check
git commit -m "{项目名}: {主题} {date}"
git push
```

5. **给验证命令时,盯内容标识、别盯会变的计数**(v2.8)。
   形如 `grep -c "^## 追加" file` 这类**计数**只在当下成立,后续 commit 继续追加就会变,Doctor 照着核会误判"出问题了"。
   验证一律用**内容标识**(某关键短句在不在、某文件存不存在),它跨 commit 稳定。

**CC 自我检查触发词**:看到自己即将在 `mcp__workspace__bash` 调用里输入 "git add" / "git commit" / "git push" → **立即停** → 改贴命令到 Step 6 回报。

### Step 6 · 回报

```
✅ 已存档
📁 logs/YYYY-MM-DD-{主题}.md

📋 请在 macOS 终端跑(brain 仓库 commit+push · 先探后加·勿 -A):
```bash
cd ~/Documents/Claude/brain
git status --short
git add <本次明确改动的文件列表>
git diff --cached --check
git commit -m "session: {主题} {date}"
git push
```

{若同步了独立项目 git:补贴该项目的 commit+push 命令}
{若 Step 4 探到 architecture/系统概览.md 不存在:补贴那一行 ⚠ 空转报告}

一句话摘要:{20 字内}
```

**注意**:不在回报里写"已提交 commit hash" — 因为 commit 还没跑(Doctor 还没在 terminal 执行)。等 Doctor 反馈结果后才能说"已提交"。

**若 Step 5.0 命中半开状态**,Step 6 改为:

```
✅ 内容已落盘(Step 3/4 完成)
📁 logs/YYYY-MM-DD-{主题}.md

⚠️ git 提交暂缓 — brain 仓处于 {rebase/merge/cherry-pick} 进行中
   {说明涉及哪些 commit、原分支、onto 目标}
   在半开状态 commit 会挂进游离 HEAD,一旦 abort 即脱离引用。
   建议先收尾仓库状态,我可以帮您判 abort/continue 各会丢什么。

一句话摘要:{20 字内}
```

## 边界

- 主题里去除 `/`、`\`、`:` 等危险字符
- session-log.md 模板缺失用 fallback
- 没有 .git/ 跳过 Step 5,不报错(但 Step 3+4 落盘照做)
- **仓库半开(rebase/merge/cherry-pick 进行中)跳过 Step 5 的 commit 命令,但 Step 3+4 落盘照做**(v2.8)
- **不在 sandbox 跑 git 写命令** = 硬约束 · 不可绕过(参 G-X2)
- **写 permanent/ 下有分节结构的文件时先定位节、再插入**(v3.0);**编号先探再取**,不心算
- **勾掉的 TODO 条目整块迁入 `references/TODO-已完成归档.md`**(v3.1);**判断性勾项 CC 只搬运已勾的、不代打 ✓**(G-X4);客观 TODO 证据硬则按常驻授权代勾留痕(G-X136)
- **Step 4 遇 `architecture/系统概览.md` 不存在 → 明确报告,禁静默跳过、禁自动补建 stub**(v3.2)
- **引用 Step 4 那张缺口表前先自己跑命令重取差集,别照抄表**(v3.2.1)

## v 历史

- v1.0(2026-05-14):初版 · Step 5 自动 git commit
- v1.1(2026-05-19):brain_checkup v1.2 加 sandbox 探测后,本 skill 仍是"自动 commit"(未同步)
- **v2.0**(2026-05-20):Step 5 升级为"贴命令给 Doctor"(响应 GOTCHAS G-X2:CC 在 sandbox 不能跑 git)
- **v2.1**(2026-05-23):新增 Step 3.5「记忆分拣提议」(半自动 session-commit · 借鉴 OpenViking · Doctor 点选才入库)
- **v2.2**(2026-05-23):Step 3.5 加「难复得三问」升格门槛——CC 按持久/难复得/会再用给默认留/砍建议,泛泛通用默认不留;落点松紧(日志放开、permanent 从严)
- **v2.3**(2026-06-02):新增 Step 1.5「数灵归属判定」——`/save @{灵}` 或出场者为某数灵时走 per-agent 落盘（日志/记忆/情感落 `agents/{灵}/`），遵落盘归位铁律，绝不混进 CC 或别的灵（数灵转移配套）
- **v2.4**(2026-06-13):Step 3.5 纳入「当下便签」——会话中途被纠正即随手记一笔，/save 时一并提议；新增"规则/skill/流程 该改"分拣类（提案制）。**取代独立 signal 队列**：经自检 signal→resume→consolidate 与 save→permanent 高度重复且 save 不可退役，遂将自进化塌缩进本 skill，不落 signals/ 文件夹、不跨会话兜底（[[视频方法论对照与开发流程优化-设计提案]] §7 · G-X10）
- **v2.5**(2026-06-14):Step 3.5 点选改用 **AskUserQuestion 多选控件**(Doctor 命题)——不再让 Doctor 打字报编号;每题≤4 option,候选 >4 条按倾向拆题(建议留 / 建议不留·提案制),`multiSelect: true`,只勾选项入库
- **v2.6**(2026-06-14):Step 3.5 点选——推荐/不推荐+难复得三问理由**写聊天正文**、选择框只保留简洁标签(理由别只埋 description)。Doctor 明示
- **v2.7**(2026-06-14):Step 3.5 选项**硬性带（推荐/不推荐）标签**;并申明此呈现规则**不限 /save、适用 CC 给 Doctor 的一切待裁选择题**(挂 [[Doctor协作偏好]]「待裁事项的呈现方式」全局条)。Doctor 明示「选项后加（推荐/不推荐），更新 skills」
- **v2.8**(2026-07-18):**新增 Step 5.0「仓库状态前置探测」硬闸**——commit 命令生成前必查 `.git/rebase-merge`、`.git/rebase-apply`、`MERGE_HEAD`、`CHERRY_PICK_HEAD`、`REVERT_HEAD`、`BISECT_LOG`、detached HEAD;命中即停、改报状态,落盘照做但不给 commit。另加一条:Step 5 新增第 5 条——给 Doctor 的验证命令**盯内容标识、别盯会变的计数**。触发案:CC 未探测即给 commit,落进先前会话遗留的未完成 rebase,一次 /save 的 202 行内容险随 abort 蒸发(详见 Step 5.0 活体教训框)
- **v2.8.1**(2026-07-18 · 当日修正):v2.8 初稿写了「只读 git 白名单(`git status`/`log`/`show`…)」,**与同日另一会话订正的铁律直接冲突**——`git status` 会创建 `.git/index.lock` 而沙箱无权删除,残留孤儿锁致 Doctor 终端 commit 报 `Another git process seems to be running`(渊图 GOTCHAS ERR-20260718-002 追加条)。改为:**沙箱内不跑任何 git 子命令**;仓库状态一律 `ls`/`cat` 读 `.git/` 下纯文本(rebase-merge/head-name、orig-head、git-rebase-todo、refs/heads/*、refs/remotes/* 全是明文);需要 diff/log/commit 内容则构造命令交 Doctor。**幸而 Step 5.0 的探测设计本就基于文件读取,只需摘掉尾巴上多缀的那条 `git status`**
- **v2.9**(2026-07-24):**Step 5/6 的 commit 命令默认改「先探后加」、禁 `git add -A`**——`git status --short`(先探全部改动) → `git add <本次明确改动的文件列表>`(后加·只列本次 /save 范围) → `git diff --cached --check` → commit → push。四处模板(step2/3/4 + Step6 回报)全改。**根因**:工作树常积压本次范围外的未提交改动(别的会话/定时班遗留),`-A` 会一并混入、造成范围不明难回溯(G-X83 / DVA GOTCHAS GIT-20260723-001 · DVA offsite 收尾实例)。只有确认工作树全部改动都属本次保存范围才允许 `-A`。Doctor 授权(2026-07-23 挂 TODO → 2026-07-24 出新 skill 包)。
- **v3.0**(2026-07-30):**Step 3.5 新增「写入位置铁律」——规定了归哪类,还得规定写到哪**。原文只写「→ `permanent/经验库.md`(cases/patterns/tools/strategies)」,没规定插到文件哪一处,于是历次 /save 一路 append 到文件尾。`/consolidate` 实测代价:经验库 267 条里 **137 条(51%)** 落在与自身类别不符的位置、`## 相关` 收尾节被压在 640 行之下、`strategies` 沦为杂物间;通用教训 31 条 G-X 里 21 条标题漏了方括号致锚点时灵时不灵;更查出 **14 组重复编号**(并发会话各自心算「今天第 N 条」),其中 6 组已被引用、11 处引用歧义。新规:①经验库按类别定位到对应 `## ` 节、插该节末尾,**禁 append 文件尾**;②新条一律用编号后缀 `-P/-T/-S` 编码类别(后缀为权威,`**类别**:` 字段是旧写法);③**取号必先 grep 探当日/当前最大号取 max+1,禁心算**;④通用教训新条进文件末尾 G-X 区、标题格式 `## [G-Xnn] 标题`(带方括号、方括号后不加 `·`),前 8 个主题节为历史层只读不追加;⑤通则——目标文件有分节结构就先读节标题再定位,「追加到文件末尾」只在文件确实以待追加区结尾时才合法。**根因判定**:这不是某次写错,是**默认落点缺省**在几个月里累积的必然结果——不立这条,清理完过几个月还会再崩。
- **v3.1**(2026-07-30 · 同日):**新增「完成即迁」——v3.0 管「写进来往哪放」,本条管「勾掉了往哪去」**。实测:`TODO.md` 39KB 里 **70% 是已完成条目**(44 条 [x] vs 11 条 [ ]),其中 20 条就地打勾留在「待办」段没搬走,而 `/resume` 每场整篇读入。已拆:已完成/已取消/2026-05 对接需求整节 → `references/TODO-已完成归档.md`,`TODO.md` 39109→12681 bytes(瘦 68%),条目 56→56 零丢失。新规:①勾掉即整块迁归档 `## 已完成`(按日期倒序);②**取消 ≠ 完成**,进 `## 已取消` 单列;③**CC 只搬运已勾的、永不代打 ✓(G-X4)**——核实中发现「疑似已办完但没勾」的只列清单报 Doctor,带「CC 不代勾」字样的碰都不碰;④写新条时先想落点是 `brain/TODO.md` 还是 `{项目}/TODO.md`(实测 DVA 两处各记各的、完全不重叠),不确定就问;⑤**待办必须进 TODO,不能只写在当日日志的「遗留待办」里**——`/resume` 只读最近 3 篇日志,写在日志里的待办滑出窗口即永久不可见(活例:抖音口播稿审稿待办 9 天没被任何 resume 拿到)。
- **v3.2**(2026-07-31):**Step 4 加「文件不存在则明确报告」——止血,不补写**。实测多个注册项目缺 `architecture/系统概览.md`,Step 4 对它们一直**无声空转**、连带 `dashboard-snapshot.py` 项目卡少一个信息源。新规:落盘前 `ls` 探路径 → 存在则照旧更新;不存在则在 Step 6 回报明写 `⚠ Step 4 空转:{项目}/…系统概览.md 不存在,最后活跃未同步`,**不建、不猜、不跳过**。**刻意不自动补建 stub**——空壳会把"没有全貌文档"从显性缺失变成隐性谎报,比空转更糟;空转至少还留着一个可被发现的洞。补写是独立议题,由 Doctor 择时另开。
- **v3.2.1**(2026-07-31 · 当日订正):**v3.2 初稿的缺口名单是错的,已按 `项目总览.md` 逐项对表重列**。初稿写「15 个注册项目里 7 个缺(烛照九阴/风险日报/白泽大宗/剑酒青丘/MiroFish/星空/称象)」——**总数碰巧对、成员错一个**:「风险日报」有目录 stub 但**不在总览 15 行内**,而已注册的「**数灵转移**」被漏掉(它有 `architecture/` 三份文档、独独没有系统概览)。订正后:注册 15 个里缺 **7** 个(MiroFish/剑酒青丘/**数灵转移**/星空/烛照九阴/白泽大宗/称象),**另加未注册的风险日报,实际无系统概览的目录共 8 个**。**错因**:直接照抄 `brain/TODO.md` 里那份二手名单,没自己跑 `ls -d */architecture/系统概览.md` 与总览取差集——**G-X111 在同一件事上连栽第三次**。故本版在表下增一条硬规:**引用该表前先自己重取差集,别照抄表**。与金融线「4.70 错在日期 / 4.66 错在时点 / US10Y 错在语义」同病根:**二手数字/名单在用之前必须重取一次对照**。
- **v3.3**(2026-08-02):**（推荐/不推荐）标签位置钉死为「选项 label 尾部」**。v2.7 只说「label 或 description 显式写」,实测 /save 分拣把控件 description 当载体——而 description 在控件里不显眼/可能被截,「默认值一眼可分」的设计落空;Doctor 当场明示「把是否推荐写在问题选项后面」。规则不变、位置钉死(选项文字后面直接跟（推荐）/（不推荐）,不许只放 description);「不限 /save、适用一切待裁选择题」的申明照旧。同步:portable/skills 与账号 save_skill 同版更新(D11 更新纪律)。

