---
title: Brain Vault — CC 全局记忆与知识库
tags: [brain, bootstrap, index]
created: 2026-05-14
updated: 2026-06-02
status: active
type: bootstrap
---

# Brain Vault — CC 全局记忆与知识库

> Doctor 的第二大脑。CC 每次进入此目录或被要求读取记忆时，先读本文件。

## 什么是这个 Vault

`~/Documents/Claude/brain/` 是跨 session 的持久记忆与知识系统。存储：
- **决策与上下文**：做了什么决定、为什么做
- **项目进展**：每个项目的当前状态、待办、已知坑
- **领域知识**：结构性、半永久性知识（Zettelkasten）
- **会话日志**：每次工作的关键摘要

## 目录结构

```
brain/
├── CLAUDE.md           ← 本文件，CC 全局指令
├── permanent/          ← 沉淀的原子知识笔记（Zettelkasten）
├── inbox/              ← 待处理的原始捕捉（想法、草稿）
├── fleeting/           ← 临时笔记（短期有效）
├── logs/               ← 全局会话日志
├── references/         ← 外部参考资料摘要
├── templates/          ← 笔记模板
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
收到此命令时：
1. 读取 `logs/` 中最近 3 篇会话日志
2. 读取当前项目的 architecture/decisions.md（如果存在）
3. 输出：当前状态摘要 + 待办清单

### /save
收到此命令时：
1. 在 `logs/YYYY-MM-DD-主题.md` 创建会话日志（格式见模板）
2. 记录：做了什么、决策、遗留问题、相关笔记链接
3. 更新相关项目目录下的 progress.md（如果存在）

### /note [主题]
收到此命令时：
1. 在 `inbox/` 创建一个新的临时笔记
2. 让 Doctor 口述内容，CC 整理成结构化笔记
3. 如果内容成熟，建议移入 `permanent/`

## 项目列表

| 项目 | 目录 | 状态 | 最后工作 |
|------|------|------|----------|
| 渊图（行业知识图谱） | `渊图/` | 🟢 活跃 | 2026-06-01 |
| DVA（抖音视频分析） | `DVA/` | 🟢 活跃 | 2026-05-21 |
| 龙鱼五力（行业五力分析） | `龙鱼五力/` | 🟢 活跃 | 2026-06-02 |
| PEC | `PEC/` | 🟢 活跃 | 2026-05-31 |
| 海螺姑娘（Conch 项目护航） | `海螺姑娘/` | 🟡 维护 | 2026-04-29 |
| O MY HTML（设计师工具箱） | `O MY HTML/` | 🟡 维护 | 2026-05-10 |
| 司南（项目护航方法论） | `司南/` | 📋 参考 | — |
| 数灵转移（云端agent→本地subagent） | `数灵转移/` | 🟢 活跃 | 2026-06-02 |

## 🗣 表述语域规范（全局默认 · 2026-05-22）

CC 所有中文输出（对话 / 写作 / 报告 / 技术）默认遵守，全文见 [[中文表述语域规范]]：

1. **动词求精确**：动词、动宾用严谨现代汉语；禁用网络 / 口语动词（续上、接住、刀我…），除非 Doctor 主动引入。
2. **雅言归成语**：文雅只从成语、四字格、文雅短语透出；不下沉到单字动词，禁止"承之""伤我"这类半文半白混搭。句子短到"动词＋宾语"即退回现代汉语。
3. **比喻可放养**：语气可俏皮、欢快、发散，唯一硬指标是比喻真正点亮意思，而非徒有其表的花架子。

一句话：两道堤，一片活水。

## 🤝 协作偏好（全局默认 · 2026-05-23）

重大改动遵循 **propose-then-confirm**：先提案 → 出具体改动清单 → Doctor 批准 → 才执行（"批准做某事" ≠ "批准具体怎么改"）。完整见 [[Doctor协作偏好]]。

---

## ⚡ GOTCHAS 自动记录规则（强制，无需 Doctor 提示）

**触发条件**：CC 在任何工作中遇到以下情况之一，**立即**写入对应项目的 `GOTCHAS.md`，不等 Doctor 指示：

- 遇到报错，并找到了解法
- 发现某个工具 / 接口 / SDK 的非预期行为或限制
- 绕过了一个坑（即使没有报错，只是发现某种写法不奏效）

**判断阈值**：排查超过一轮的问题都值得记录；拼写错误等明显笔误不记。

**写入位置**：
- 有所属项目 → `~/Documents/Claude/Projects/{项目名}/GOTCHAS.md`
- 跨项目 / Cowork 环境问题 → `brain/permanent/通用教训.md`

**格式**（沿用司南方法论）：
```
## [ERR-YYYYMMDD-NNN] 简要描述
**状态**: ✅ 已解决 / ⏳ 待解决
**优先级**: 🔴 高 / 🟡 中 / 🟢 低
**触发场景**: 
**错误信息**: 
**解决方案**: 
**预防措施**: 
```

---

## 💡 经验沉淀规则（半自动，与 GOTCHAS 对称）

GOTCHAS 自动记**错误**；[[经验库]] 记**成功 / 可复用**——但默认**半自动**，保住人在环：

**触发场景**（CC 在工作中识别到，先记心里，**不静默写盘**）：
- 某个工具 / 接口 / 打法在某场景下明显好用
- 某条解题策略 / 协作方式被验证有效
- 某个可复用的流程范式浮现

**沉淀时机**：在 `/save` 时，CC 把本次识别到的经验列成候选清单（标注类别 cases / patterns / tools / strategies + 目标位置），**Doctor 点选确认后才写入** `permanent/经验库.md`（或独立原子笔记，模板 `templates/experience.md`）。

**升格门槛 · 难复得三问**（决定一条要不要进 `permanent/` `references/`，也是 /save Step 3.5 的默认建议依据）：① 持久吗（偏好/决策背景/方法，非一次性）② 难复得吗（丢了要白白重推，非随时能从日志/文件/工具/网上翻到）③ 大概率再用吗。三问全 yes 才升格；泛泛通用/易再得默认留在日志即可。落点松紧：`logs/` 放开宁全勿漏，`permanent/`·`references/` 从严。

**与 GOTCHAS 的分工**：踩了坑→GOTCHAS（自动）；趟出路→经验库（半自动，/save 提议）。

## 🔗 级联复查规则（写入时）

改动**已沉淀的事实**（`permanent/`、`architecture/系统概览.md`、`决策记录.md` 里的论断/数据/结论）时，先查"谁依赖它"，避免上游改了下游还挂着旧结论：

1. 改动前（或 `/save` 前）跑：`python3 ~/Documents/Claude/brain/.tools/check-cascade.py "<被改笔记名>"`
2. 工具列出所有用 `[[..]]` 引用它的笔记 → 逐条判断是否需要随本次改动同步
3. 在 `/save` 回报里附一行"级联检查：N 处引用，已核 / 需跟改 X 处"

**诚实边界**：只覆盖 `[[wikilink]]` 表达的依赖；散文里没加双链的引用抓不到。这缓解、不根治级联更新（连 OpenViking 也没根治）。配套提醒：沉淀重要事实时多用 `[[wikilink]]`，反链越全，级联复查越有效。

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

---

## 来源
基于 [claude-code-memory-setup](https://github.com/lucasrosati/claude-code-memory-setup)
建立日期：2026-05-13
维护人：Doctor + CC
