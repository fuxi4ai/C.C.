---
name: "brain-dream"
description: "brain 的离线记忆整理（dream）。每天由 Cowork 定时班触发，也可手动：/brain-dream 或说「做梦」「dream 一下」。对照真相层（原始会话）核对新日志里的事实，经独立 subagent 复核后只追加订正注或做有边界的事实订正；新增、合并、退役与注入层改动只进提案队列；每周日额外自动触发 consolidate，跑到拟改动清单即停。不跑 git、不删文件、不改注入层与技能。"
---

# brain-dream — 离线记忆整理

> **为什么有这个技能**：Anthropic《The components of agent memory》（2026-11-06）把记忆分成原始记录、记忆笔记、记忆表示、注入上下文四层，用离线的 dreaming 在层间核对与整理：拿原始记录核对笔记、修正写错的事实、合并重复、退役陈旧、把要紧的提升到注入层。brain 的对应物：真相层（原始会话，`chats/transcripts/`）＝原始记录；`logs/`、`permanent/`、各项目 GOTCHAS＝笔记；经验索引与 wikilink＝表示；注入层＝`~/.claude/CLAUDE.md`、`~/CLAUDE.md`、`brain/CLAUDE.md`、`brain/portable/claude-code/CLAUDE.md` 与 `permanent/全局偏好-Settings镜像*.md`。旧版龙宫梦境（OpenClaw，2026-06-02 退役）代码已不在盘上，本技能按「代码舍弃、设计借鉴」重建，不用它的关键词抽取、前 30 字查重、整份重写 MEMORY.md。
>
> **分工**：`/save` 是单场写入；本技能是每日的轻档核对与提案；`brain-consolidate` 是重档跨库整理，每周由本技能自动触发到「拟改动清单」为止，落盘仍等 Doctor 批。
>
> **授权依据**：全局规则「GOTCHAS 自动登记合同」默认禁止自动修改被审文档；本技能的 Step 3 事实订正是 **Doctor 2026-11-19 裁定的具名例外**（原话：「事实订正自动，新增进提案」），射程只到下文「硬边界」第 5 条，超出射程的一律转提案。
>
> PRD：`logs/checkpoints/2026-11-19_Dream技能_PRD.md`

## 触发

- 每天 04:30 由 Cowork 定时班触发（排在 03:40 真相层每日抽取之后）。
- 手动：`/brain-dream`、「做梦」「dream 一下」。（`~/.cc-switch/skills/` 里另有一个同名思路的 `dream` 技能，写的是 Doctor 已禁用的 MEMORY.md，不是本技能。）

## 硬边界（先读，全程遵守）

**只许写这些**：
1. 当日报告 `logs/dream/YYYY-MM-DD-dream.md`（同日再跑则在文末追加一节「第 N 次运行」）。
2. 提案队列 `permanent/_dream_proposals.md`（只追加）。
3. 审计台账 `permanent/_dream_audit.jsonl`（只追加）。
4. 运行状态 `permanent/_dream_state.json`（只由 `dream_collect.py --mark-processed / --mark-run` 写）。
5. Step 3 经独立复核成立的事实订正，**射程**：
   - 日志：只在**文末追加订正注**，原文一字不改；同一处已有订正注就不再追加。
   - permanent：只限 `permanent/` 下文件名不以 `_` 开头的 `.md`，且**不含**规则类与索引类笔记（`全局偏好-Settings镜像*.md`、`Doctor协作偏好.md`、`数据真实性铁律.md`、`GOTCHAS与经验沉淀规则.md`、`brain-vault规范.md`、`经验索引.md`、`项目总览.md`）；只改**数字、路径、日期、编号**这四类，不改状态标记（✅🔄⚠️ 等）、不改引号里的原话、不改决策与规则的表述。
   - 项目 GOTCHAS：同上四类，不碰「状态」行。
   - 改前先备份到同目录 `_bak/<原文件名>.bak_YYYY-MM-DD_dream订正`；同名已存在就依次加 `-2`、`-3`，**绝不覆盖已有备份**。
6. 按 GOTCHAS 自动登记合同登记硬证据确认的实错：项目 canonical GOTCHAS、`permanent/通用教训.md`（全局规则已授权；新条目只能标 🔄 或 ⚠️）。
7. 周日 Step 6 的产出：`logs/checkups/YYYY-MM-DD_consolidate_冲突清单_vN.md` 与 `..._Step2拟改动清单_vN.md`（N 取当日未用的最小号，不覆盖）。

**禁止**：跑任何 git 命令；删除或移动文件；改注入层（上面列的四个 CLAUDE.md 与 Settings 镜像两件）；改 `.skills/`、`portable/` 下的技能；把新记忆、合并、退役、规则或决策改动直接写进 permanent（这些只进提案队列）；为了让核对「通过」而改日志原文；改 `logs/checkpoints/` 里的 PRD。

## 执行步骤

### Step 0 · 定根与对表

- 先 `date`（含时区），不沿用记忆里的日期；判「是否周日」按本机时区。
- brain 根按顺序取第一个存在的：`~/Documents/Claude/brain` · `$HOME/mnt/Documents/Claude/brain` · `$HOME/mnt/Brain`。下文 `<brain>` 指它。

### Step 1 · 收集

```bash
python3 -I <brain>/.tools/dream_collect.py --brain <brain>
```

输出 JSON 的用法：
- `window`：本轮窗口。终点 `until` 封顶在真相层最近一次抽取时间——还没进真相层的会话留给下一轮。**记下 `window.until`，Step 7 要用。**
- `truth_layer`：`error` 非空（状态缺失或时间解析失败）或 `stale` 为 true（超过 48 小时没抽取）时，报告首行写「⚠ 真相层（原始会话）不可用：<原因>，每日抽取任务可能停了」，**跳过 Step 2–3**，继续 Step 4–7。
- `truth_layer.size_mb`：真相层体量。`over_archive_threshold` 为 true（≥2GB）时，写一条「归档」类提案：建议把最早的若干月抽取件打包归档到 fuxi-station `F:\Mac_Backup\cc_sessions\`（Doctor 2026-11-20 定的上限）；本技能不自己搬。
- `sessions`：窗口内有活动的主会话（子代理会话只计数在 `sidechain_sessions`）。
- `pending_logs`：待核对日志，新的在前。按内容哈希记账，处理过的不会再出现；`seen_before` 为 true 表示以前核对过、之后又被改过；`search_since` 是这篇日志检索出处的起点（按它自己的日期往前 3 天）；`after_truth_layer` 为 true 表示它写于最近一次抽取之后、相关会话还没进真相层——**本轮跳过，留到下一轮**；`expiring` 为 true 表示本轮不处理就会超出 7 天待办期。
- `first_run` 为 true（第一次运行，台账为空）：先把两天前的积压记为基线、不核对，免得几十篇积压挤爆预算后又在 7 天后静默过期：
  ```bash
  python3 -I <brain>/.tools/dream_collect.py --brain <brain> --baseline-older-than 2
  ```
  报告里写记了多少篇基线，然后重新跑一次收集。
- `permanent_changed`：窗口内改动的 permanent 笔记，Step 4 写提案时参考。

**本轮预算**：最多核对 12 篇日志（按列表顺序，新的在前），每篇最多 15 条陈述，全轮最多 150 条；超出的留在台账外，下一轮接着做。报告要写清：预算外留到下轮几篇、其中 `expiring` 的几篇（这些下一轮就会退出待办，不再核对）。窗口内既无会话也无待核对日志时，直接到 Step 4（周日仍要做 Step 6）。

### Step 2 · 用原始会话核对日志

对预算内的每篇日志，挑出**会被后来引用的事实性陈述**：数字与计数、文件路径、「已完成/已验证/已提交」这类状态、决策与 Doctor 原话、编号引用（G-X、EXP、ERR）。优先挑结论、决策和数字。

逐条用真相层检索找出处：

一篇日志的检索词写进一个临时文件（每行一个，放 `$TMPDIR`），一次扫描查完：

```bash
python3 -I <brain>/.tools/transcript_search.py --patterns-file <检索词文件> --exclude-path <该日志的文件名（不带目录）> --root <brain>/chats/transcripts --since <该日志的 search_since> --limit 0 --json
```

`--exclude-path` 只排除这一篇日志自己的写入、读取与带着它文件名的输出（用不带目录的文件名，`cd logs` 后再 `cat` 的读法也能排掉）（别的文件的 Edit、Write 是改动证据，要留）；`--since` 用这篇日志自己的 `search_since`，不用本轮窗口——积压日志的会话早于窗口，用窗口会漏掉出处。必要时再单独查：`--session 会话号前缀`、`--role user` 查 Doctor 原话、`--kind tool_result` 查工具实际输出。

**出处只认这些**：Doctor 的发言（`role=user` 的文本）；工具的实际输出（`tool_result`）；对**其他文件**的改动记录（Edit、Write 的参数，证明「改了哪里」）。**助手的叙述只当线索**——日志就是助手写的，拿助手的话证明助手的话等于自证，要顺着叙述去找对应的工具输出或 Doctor 原话。检索结果里仍看到在复述该日志原句的（例如别处转引），也不算。

每条归入三类之一：**一致**（出处支持）／**不一致**（出处与陈述冲突，记下会话号、时间、原文片段）／**查无出处**（真相层里找不到依据，可能是转述过度或记错）。只按检索到的原文判，不凭印象。

**记账时机**：一篇日志的陈述核完、它的 Step 3（订正注追加、转提案）也做完后，才记账——这样中途停下时没做完的会在下一轮重来，追加的订正注也算进记账时的内容哈希，不会让这篇日志因为多了订正注又被重新核对：

```bash
python3 -I <brain>/.tools/dream_collect.py --brain <brain> --mark-processed <该日志相对 logs/ 的路径>
```

### Step 3 · 事实订正（只针对「不一致」；逐篇做，做完这一篇再按 Step 2 末尾记账）

1. 派一个**未参与本次运行**的 subagent 独立复核：给它陈述原文、所在文件与行、候选出处的会话号，要求它自己去真相层检索原文后判定「订正成立 / 不成立 / 无法判定」，并给出应改成的准确表述。派单里不写你的结论。
2. **成立**，且落在「硬边界」第 5 条的射程内，才订正：
   - 日志：先在该日志里查有没有同一句原文的「订正注（dream」——有就跳过。没有就在文末追加：
     ```
     > **订正注（dream YYYY-MM-DD）**：原文「…」与原始会话不符——会话 <会话号前 8 位> <时间> 实为「…」。
     ```
   - permanent 或项目 GOTCHAS：按第 5 条备份后做最小改动，在该条末尾注明「dream YYYY-MM-DD 订正，依据会话 <会话号前 8 位>」。
   - 每处订正追加一行到 `permanent/_dream_audit.jsonl`：`{"time","file","line","old","new","evidence_session","evidence_time","reviewer":"<复核 subagent 的类型与任务描述>","result":"订正成立"}`。
3. 成立但超出射程（规则、决策、原话、状态行、规则类笔记等）：不改，写成「事实订正」类提案。
4. 不成立或无法判定：不改，写进报告。
5. 当前环境派不出独立 subagent：不订正，全部写成「事实订正」类提案。

### Step 4 · 写提案（只提不改）

从窗口内会话与日志里找下面四类，**查重后**追加到 `permanent/_dream_proposals.md`：

- **新记忆候选**：过「难复得三问」（持久、难复得、会再用）三问全是的决策、偏好、教训、方法；先查 `permanent/经验索引.md` 与相关笔记，已有的不提。
- **合并**：同根的条目（同一个坑、同一条规则写在两处）。
- **退役**：被更新的事实推翻、或已过期的条目。
- **注入层修改**：注入层里与现状不符的地方。

查重：提案队列里已有同一证据（同会话号、同文件同行）的条目就不再写。每条格式（编号用 `DRM-YYYYMMDD-HHMM-序号`，按本次运行时间取，避免并发撞号）：

```
### [DRM-YYYYMMDD-HHMM-NN] 一句话标题
- 类型：新记忆 / 合并 / 退役 / 注入层 / 事实订正 / 归档
- 内容：要加什么、合并哪几条、退役哪条、改成什么
- 理由：为什么（新记忆写三问各自的判断）
- 证据：会话号前 8 位 + 时间 / 日志路径与行
- 建议落点：具体文件与小节
- 状态：待批
```

「状态」只由 Doctor 批或拒时改成「已批 / 已拒」（在交互会话里，或每周 consolidate 落盘时一并处理），本技能不改。

### Step 5 · 登记实错

核对中由原始会话硬证据确认的实错（工具非预期行为、反复出现的坑等），按全局规则「GOTCHAS 自动登记合同」登记到所属项目 canonical GOTCHAS；跨项目的落 `permanent/通用教训.md`。新条目只能标 🔄 或 ⚠️。

### Step 6 · 每周 consolidate（本机时间周日的运行，无论有无新材料）

按 `brain-consolidate` 技能「每周自动运行」口径执行 Step 0 → Step 1 → Step 1.5（含独立复核）→ Step 2，并把提案队列里「待批」的 `DRM-*` 条目一并纳入 Step 2 拟改动清单，产出第 7 条那两份文件后**停止**，不进入落盘。派不出 Step 1.5 的独立复核者时，只产出冲突清单并在文首标「独立复核未做，按硬门不出 Step 2 清单」。报告里写清单路径与冲突条数。

### Step 7 · 写报告并记运行

报告 `logs/dream/YYYY-MM-DD-dream.md`（带 frontmatter：title、tags [dream, log]、created、updated、status: active、type: log），小节：
1. 窗口与来源：起止时间（注明是否封顶在真相层抽取时间）、真相层新鲜度与体量（MB）；窗口内主会话逐个列出标题、来源、时间范围，子代理会话只给个数。
2. 核对结果：本轮核了几篇日志、几条陈述；一致 / 不一致 / 查无出处各几条，不一致与查无出处逐条列；预算外留到下轮的日志几篇。
3. 已订正：逐条写文件、旧→新、证据会话、复核结论。
4. 新提案：编号与标题；队列里累计待批几条。
5. 每周 consolidate（仅周日）。
6. 未完成与原因。
7. 本次改动的文件清单（供 Doctor 提交）。

然后按本轮窗口终点记运行：

```bash
python3 -I <brain>/.tools/dream_collect.py --brain <brain> --mark-run --until <window.until>
```

**只有前面各步跑完（含「跳过」的正常分支）才记运行**；中途出错就不记，下次从同一窗口起点重来，已核完的日志靠台账不会重复处理。

### Step 8 · 回报

- 定时班（无人值守）：只输出报告路径和三行摘要（核对、订正、提案各几条）；不开选择窗，不问问题；git 提交命令不在这里跑，改动文件已列在报告里。
- 交互会话：给 Doctor 摘要，待批提案提醒他在合适时候过一遍。

## 出错时

- 收集脚本退出码非 0：报告写错误输出，不做后续，不记运行。
- 检索脚本读不了某个抽取件：它会跳过并告警，照常继续，在报告里记一笔。
- 订正时备份失败：不改原文件，该条转为提案。

## v 历史

- v1.0（2026-11-19 · Doctor 裁「在 Anthropic 文章基础上设计 Dream Skill，默认每日触发，每周自动触发一次 consolidate」；三问取推荐：周 consolidate 自动跑到出提案、事实订正经独立复核自动落而新增进提案、在 Cowork 定时班运行）：初版。
- v1.1（2026-11-19 · 首次独立审查 FAIL 后修订）：按内容哈希记已处理日志（中断续跑、同日重跑不重复订正）；窗口终点封顶在真相层抽取时间、记运行用本轮终点；出处排除笔记自身的读写记录（防自证）；permanent 订正限定为数字、路径、日期、编号四类并排除规则与索引类笔记、状态行与原话；备份同名加序号不覆盖；单轮预算 8 篇日志、60 条陈述；周日无论有无新材料都跑 consolidate，复核者不可用时不出 Step 2 清单；报告逐个列主会话；允许写清单补上 checkups 与 GOTCHAS；触发词改为 /brain-dream，去掉会撞 consolidate 的「整理记忆梦境」；写明授权依据为 Doctor 具名例外。
- v1.2（2026-11-20）：Step 2 改用检索脚本的 `--patterns-file` 一次扫描查完一篇日志、`--exclude-notes` 机械排除笔记自身的读写记录、`--since` 只解压窗口内会话（复审 N3 与自证问题的工具侧落地）。
- v1.3（2026-11-20 · 复审后修订）：检索出处的起点改为每篇日志自己的 `search_since`（按日志日期往前 3 天），修掉积压日志用窗口起点检索会漏出处、误判「查无出处」的问题；记账挪到该篇 Step 3 做完之后；`--exclude-notes` 换成只排除本篇的 `--exclude-path`，其他文件的改动记录保留为证据，助手叙述只当线索；首轮把两天前的积压记为基线；预算改为新的在前 12 篇、150 条，并报告即将过期的篇数；写于最近一次抽取之后的日志留到下一轮；窗口终点始终封顶在真相层抽取时间。
- v1.3.1（2026-11-20 · 第三次复核）：`--exclude-path` 改传不带目录的文件名——`/resume` 常用 `cd logs` 再 `cat 文件名` 读日志，带目录的路径匹配不到，日志会拿自己的文字当出处。
- v1.3.2（2026-11-20 · Doctor 定 N3「2G 后归档至 fuxi-station」）：报告写真相层体量；≥2GB 时写「归档」类提案，搬迁由 Doctor 批后在交互会话做。
