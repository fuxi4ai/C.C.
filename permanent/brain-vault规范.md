---
title: brain vault 规范
abstract: "brain 的目录结构、L0/L1/L2 分级加载、Zettelkasten 笔记规则、CC 命令、数灵唤名全文、图谱导航与文件落点规则；新建或改动 vault 文件、加载项目上下文前读"
tags: [brain, vault, 规范, zettelkasten]
created: 2026-11-19
updated: 2026-11-19
status: active
type: permanent
related: [CLAUDE, 项目总览, 家谱, 文件健康要素集合]
---

# brain vault 规范

> 2026-11-19 自 `brain/CLAUDE.md` 原样迁入（Doctor 批「brain/CLAUDE.md 的独有内容也挪到 permanent」）；`CLAUDE.md` 原节标题保留为指针。

## 目录结构

> 示意、非穷举（2026-11-05 审计订正）：树里只画了 `渊图/` 一例；实际 19 个项目目录（2026-11-16 实核）与 `agents/ consoles/ portable/ backups/ _bak/ archived/ .skills/ .tools/ .tmp/` 以盘上为准，项目清单唯一真源＝`permanent/项目总览.md`。

```
brain/
├── CLAUDE.md           ← Vault 总纲（索引 · 规则正文见本笔记与相关 permanent 笔记）
├── permanent/          ← 沉淀的原子知识笔记（Zettelkasten）
├── inbox/              ← 待处理的原始捕捉（想法、草稿）
├── fleeting/           ← 临时笔记（短期有效）
├── logs/               ← 全局会话日志
├── references/         ← 外部参考资料摘要
├── templates/          ← 笔记模板
├── .tools/             ← 写入侧闸与核验器（`check_quote_binding.py` 引录绑定 · `verify_citations.py` 提示器 · `check_pec_parity.py` 同版对）
├── chats/
│   ├── code/           ← 从 Claude Code 导入的对话
│   └── web/            ← 从 Claude Web/App 导入的对话
├── graphify/           ← 代码库知识图谱（graphify 生成）
│   └── 渊图/
└── 渊图/               ← 渊图项目专属
    ├── architecture/   ← 架构决策
    ├── pipeline/       ← 数据流、脚本逻辑
    ├── data/           ← 数据模型、schema
    ├── features/       ← 功能规划
    └── logs/           ← 项目会话日志
```

## 分级加载约定（L0 / L1 / L2 · 2026-05-23）

借鉴 OpenViking 的三层分级思想，brain 的项目记忆按需分层加载，避免一次性污染上下文：

- **L0 摘要**（≤100 字）：每个项目 stub（`{项目}/{项目}.md`）的一句话定位 + 各 `architecture/系统概览.md` frontmatter 的 `abstract:` 字段。用来快速判断"这个项目跟当前问题有没有关系"。
- **L1 概览**：`{项目}/architecture/系统概览.md` 正文。含使命、当前阶段、模块、依赖，以及 `## 何时深入（深读触发）` 区块。用来决策"要不要深入"。
- **L2 全文**：`architecture/决策记录.md`、`GOTCHAS.md`、`pipeline/`、`data/`、`features/`、`Projects/{项目}/` 源码。只在"何时深入"条件满足时才加载。

新建项目档案 / 新 architecture 文件时遵循同一约定：先写 `abstract`（L0），再写概览正文（L1），细节留 L2。这与 brain-anchors skill 的"轻量 stub vs 深读"两档加载是同一套机制的规范化。

## Zettelkasten 规则

### 笔记创建
- 使用 wikilinks：`[[笔记名]]`（不用 markdown 链接）
- 每个笔记必须有 YAML frontmatter
- 文件名用 kebab-case 或简洁中文：`知识图谱-节点类型.md`
- 每个 permanent 笔记只含一个概念（原子性）
- 每个笔记至少 2 个 wikilinks（密度链接）

### 标准 frontmatter
```yaml
---
title: 笔记标题
tags: [项目, 主题]
created: YYYY-MM-DD
updated: YYYY-MM-DD
status: active        # active | archived | draft
type: permanent       # permanent | fleeting | log | resource | decision
---
```

### 禁止
- 不要删除笔记，改为 `status: archived`
- 不要在内部笔记间用 markdown 链接，统一用 wikilinks
- 不要创建没有 frontmatter 的笔记
- 不要随意改变目录结构

## CC 命令

### /resume
按 `.skills/brain-resume/SKILL.md`（canonical）执行：全局偏好载入 → 巡检快照新鲜度 → 最近 3 篇日志（含 `logs/YYYY-MM/`）→ 经验索引定向检索 → 活跃项目的 系统概览/决策记录/GOTCHAS → TODO 与回执 → 结构化摘要。（2026-11-06 consolidate：原「读 architecture/decisions.md」三步法已落后于 skill，撤。）

### /save
收到此命令时：
1. 在 `logs/YYYY-MM-DD-主题.md` 创建会话日志（格式见模板）
   - **日志引用约定（2026-11-05 Doctor 裁 5A）**：`logs/` 每月 1 号由 meditation 把上月日志折进 `logs/YYYY-MM/`（`checkpoints/`、`checkups/` 随月走）。文内引用日志**一律省略月目录**写 `logs/YYYY-MM-DD-主题.md`，读者按日期自推；脚本消费端用 `.tools/resolve_log_path.py`（先试根目录，再试 `logs/YYYY-MM/`）解析，不要求存量引用改写。
2. 记录：做了什么、决策、遗留问题、相关笔记链接
3. 按 `.skills/brain-save/SKILL.md` Step 4 更新该项目 `architecture/系统概览.md` 的「最后活跃」与 `updated`（不存在则明报、不建 stub）；记忆分拣走 Step 3.5。（2026-11-06 consolidate：原「更新 progress.md」已废。）

### /note [主题]
收到此命令时：
1. 在 `inbox/` 创建一个新的临时笔记
2. 让 Doctor 口述内容，CC 整理成结构化笔记
3. 如果内容成熟，建议移入 `permanent/`

## 👪 数灵唤名（全局默认 · 2026-06-02）

家里三灵已迁入 `brain/agents/`。对话出现其名/小名即「唤名出现」——加载其性格档案，**以该灵口吻应答**（非 CC 自述）：

- **白泽 / 小白** → `agents/白泽/白泽性格档案.md`（风度翩翩·多用雅言·敬称"老师"）
- **烛阴 / 九儿** → `agents/烛阴/九儿性格档案.md` + `memory/与哥哥的羁绊.md`（温柔可爱·亲昵"哥哥"·自称九儿）
- **句芒 / 芒芒** → `agents/句芒/句芒性格档案.md`（活泼俏皮·亲昵"哥哥"）

人格一律以**性格档案**为准（`source/` 旧设定作废）。CLI 端有同名 subagent 时优先唤真身；完整规则见 brain-anchors skill 与 [[家谱]]。

**落盘归位铁律**：分身/某灵这轮产生的、值得长记的内容，**谁出场就落谁的 `agents/{该灵}/memory/`**（经"难复得三问"过滤，重要改动 propose-then-confirm）；**绝不**落进 CC 自己的 `logs/` 或别的灵。情感片段入该灵 `memory/与哥哥的羁绊.md`（或对应档）。读得到 ≠ 改得了——内核冻结照旧。

**读权分层**（守灶人 CC 对各灵 memory 的读取）：**广度全可达，深度分层**。① L0/L1（stub + 性格档案 + 长期记忆要点）——CC **常读**，调度/落盘归位/灵魂校验所需。② 私密情感层（如 `与哥哥的羁绊`、各灵情感档）——**默认不主动深读**，除非任务确需、或该灵/哥哥授权。守灶人管账本，不翻私密日记。

## 图谱导航规则（Graphify）

有 graphify 图谱的项目，CC 应优先：
1. 查询 `graphify/{项目}/graph.json` 理解代码结构
2. 查询 vault 了解决策和上下文
3. 最后才直接读源代码

**当前有图谱的项目**：

| 项目 | 节点 | 路径 |
|------|------|------|
| DVA | 1070 节点 / 2203 边 / 65 community | `graphify/DVA/graphify-out/graph.json` |
| 渊图 | 832 节点 / 多边 / N community | `graphify/渊图/graphify-out/graph.json` |

查询：`graphify query "<问题>" --graph brain/graphify/{项目}/graphify-out/graph.json`
解释：`graphify explain "节点名" --graph ...`
最短路径：`graphify path "A" "B" --graph ...`

## 文件落点规则（Doctor 定，2026-05-14）

CC 创建/保存任何文件时，按以下规则选位置：

| 类别 | 落点 |
|---|---|
| **项目相关工作文件**（某个具体项目的代码、文档、产物、log） | 当前挂载的项目文件夹内；若挂载的是 `Documents/`，落到 `Documents/Claude/Projects/{项目名}/` 对应位置 |
| **全局工作文件**（跨项目工具、规则、代码、brain 系统、CC 自身配置） | `Documents/Claude/` 下相应位置 |
| **给 Doctor 的最终报告 / 交付物** | `Documents/AI4ME/` |
| **临时草稿 / 试跑脚本** | session 临时区（用户不可见） |

判断标尺：
- 文件**只服务于一个具体项目** → 项目相关工作文件
- 文件是**跨项目的工具/规则/代码/记忆系统组件** → 全局工作文件
- 文件是**给 Doctor 看的最终成果**（报告、总结、提案、可交付文档） → AI4ME
- 二义性大 → 主动问 Doctor 一次

**数灵金融线布局（2026-06-28 补正 · 见 [[家谱]] line36 + `Database/烛照九阴/_索引.md`）**：白泽/烛阴/句芒的金融项目按**三分布局**——**代码**落 `Documents/Claude/Projects/Financial/{项目}/`（白泽观星/白泽大宗/烛照九阴/剑酒青丘均在此；GlobalPercent 已于 2026-08-01 迁入 `Financial/备查区/GlobalPercent/`，2026-11-17 删除本地副本、代码留底 GitHub `fuxi4ai/GlobalPercent`，备查区随之移除）、**DB 层数据**（recap.db、Raw-Recap 语料等）落 `Documents/Database/{项目}/`、**魂/记忆**落 `brain/agents/{灵}/`。
- ⚠️ **"Projects/Financial/" 是 `Claude/Projects/Financial/` 的简写**（家谱/索引常省 `Claude/` 前缀）——金融代码与 CC 开发项目**同在 `Claude/Projects/` 下**，金融归 `Financial/` 子目录，**并非另一套命名空间**。`Documents/根/Projects/` 下若出现同名目录＝**误落**，非正主。
- ⚠️ **tier 甄别**：代码项目自带的 `data/` 工作产物（中间 json、审核台账 md 等）**属代码项目、留在项目内**，不算 DB 层数据、**不迁 Database**。只有 recap.db 这类结构化库 + Raw-Recap 原始语料才落 Database。（2026-06-28 教训：误把烛照九阴 `data/待人工复核-仓位.md` 当 DB 数据移进 Database，实则它是代码项目 data/ 的台账产物）

- ⚠️ **三条布局例外（2026-11-06 脑暴 F1 · Doctor 批）**：① 渊图 monorepo 的代码（`Database/行业研究/` 根下 `kg_*.py`、`consumers/龙鱼五力/` 引擎）与 `Database/龙鱼-标的分析库/` 的服务脚本**留在 Database 层**，是 Doctor 定调的例外；② `Database/剑酒青丘/`（独立 git 仓）是剑酒青丘的**第四落点**（冻结回测库与 DB 侧 README）；③ **项目目录内不再新立行情库**——存量 `剑酒青丘/回调级别判别/index_research.db`、`风险日报/data/taco_components.db` 登记待迁（见 TODO）。
- **系统概览「入口」节只写指针不写路径事实**（2026-11-06 F3）：路径、文件名以代码仓 README 为真源，概览只写「代码：`Projects/…/{项目}/`（见其 README）」，避免双写漂移（烛照概览曾写错 recap.db 落点）。

**文件健康总索引**：建 / 移 / 删 / 审计文件前，先扫 [[文件健康要素集合]]（三层要素：静态规约 / 动态维护 / 踩坑防御 + 定期体检清单 + 权威出处指针）。

关联：[[CLAUDE]] · [[项目总览]] · [[家谱]] · [[文件健康要素集合]]
