---
name: brain-anchors
description: Auto-load full project context when Doctor's anchor keywords appear in conversation. Trigger when the user's message contains any of these anchors — "dva" / "DVA", "龙鱼五力", "自检", "天工开物", "渊图" / "行业图谱", "海螺姑娘", "PEC" / "政治经济学", "司南", "O MY HTML", "星空" / "Starry Skies" — Claude stops the current task and reads the corresponding project's architecture, decisions, and gotchas before responding, so the answer is grounded in that project's accumulated context rather than generic knowledge.
---

# brain-anchors — 锚点触发自动加载

## 触发与对应读取

收到 Doctor 的消息时，扫描以下关键词。命中任何一个，**立即**停下当前任务，先读对应文件，再继续响应。

| 关键词 | 触发读取（按顺序） |
|--------|-------------------|
| `dva` / `DVA` | **轻量 stub**：`brain/DVA/DVA.md`（index，含项目定位 + 深读入口）<br>深读触发：Doctor 显式说"深入 DVA" / "细读 DVA" / 进入 `Projects/DVA/` 实际工作时<br>深读时再加载：`brain/DVA/architecture/系统概览.md` · `决策记录.md` · `GOTCHAS.md` · `Projects/DVA/CLAUDE.md` · `Projects/DVA/GOTCHAS.md` |
| `龙鱼五力` | **轻量 stub**：`brain/龙鱼五力/龙鱼五力.md`（index 文件，含项目定位 + 深读入口）<br>触发深读条件：Doctor 显式说"深入龙鱼五力" / "细读龙鱼五力" / 进入 `Projects/龙鱼五力/` 实际工作时<br>深读时再加载：`brain/龙鱼五力/architecture/系统概览.md` · `决策记录.md` · `GOTCHAS.md` · `Projects/龙鱼五力/RULES.md` |
| `自检` | `Projects/龙鱼五力/RULES.md`（严格用户视角标准化检查流程） |
| `天工开物` | `Vault/天工开物.md`（设计项目启动咒语） |
| `渊图` / `行业图谱` | `brain/渊图/architecture/系统概览.md`<br>`brain/渊图/architecture/决策记录.md`<br>`brain/渊图/GOTCHAS.md`<br>`Database/行业研究/CLAUDE.md`（若存在） |
| `海螺姑娘` / `Conch` | `brain/海螺姑娘/architecture/系统概览.md`<br>`brain/海螺姑娘/architecture/项目概要.md`（若存在）<br>`brain/海螺姑娘/GOTCHAS.md` |
| `PEC` / `政治经济学` | `brain/PEC/architecture/系统概览.md`<br>`brain/PEC/frameworks/认识论框架.md`（若存在）<br>`brain/PEC/GOTCHAS.md`<br>`Projects/PEC/GOTCHAS.md`（若存在） |
| `司南` | `brain/司南/architecture/系统概览.md`<br>`brain/司南/方法论概要.md`（若存在）<br>`brain/司南/GOTCHAS.md` |
| `O MY HTML` / `omy` | `brain/O MY HTML/architecture/系统概览.md`<br>`brain/O MY HTML/GOTCHAS.md`<br>**额外**：可加载 `Vault/taste-skills/` 和 `Vault/emil/`（设计 skills） |
| `星空` / `Starry Skies` | **轻量 stub**：`brain/星空/星空.md`（index，含项目定位 + 深读入口）<br>深读触发：Doctor 显式说"深入星空" / "细读星空" / 进入 `Projects/星空/` 实际工作时<br>深读时再加载：`Projects/星空/PRD.md` · `Projects/星空/reference/REF-001-知识星河-design-language.md` · `Projects/星空/GOTCHAS.md`（若存在） |

## 行为规则

### 加载强度分两档

- **轻量 anchor**：只读 stub index（数十行）；让 CC 知道项目存在、位置、一句话定位，不污染对话上下文。命中时**仅**读 stub 文件，深读条件单列在表中（Doctor 显式要求 / 进入项目目录工作时触发）。当前轻量：`DVA` · `龙鱼五力` · `星空`
- **重型 anchor**（旧默认）：直接读 architecture/系统概览/决策记录/GOTCHAS。仍为大多数项目使用。

### 通用规则

1. **不打断 Doctor**——只在内部静默加载，加载完直接给出有上下文的答复
2. **命中多个**——按出现顺序全部加载
3. **文件不存在**——跳过该文件，不报错
4. **设计项目（O MY HTML）vs 非设计项目**——只在 O MY HTML 触发时考虑设计 skills，其他项目**不要**激活 taste-skills/emil
5. **加载范围**——只读 architecture/系统概览/决策记录/GOTCHAS，**不**自动深入 pipeline/data/features 子目录（按需深入）

## 触发示例

- Doctor 说 "DVA 那边视频分析的节点要不要拆开" → 命中 `DVA`，先读 brain/DVA/ 三个核心文件再回答
- Doctor 说 "帮我用龙鱼五力分析一下宁德时代" → 命中 `龙鱼五力`，读 brain/龙鱼五力/ + Projects/龙鱼五力/RULES.md
- Doctor 说 "需要走一遍自检" → 命中 `自检`，读 Projects/龙鱼五力/RULES.md
- Doctor 说 "今天画板上画一个 dashboard" → 命中 `天工开物`（隐式）—— 实际上需要 Doctor 显式喊 `天工开物`；不显式则**不**自动激活设计 skills

## 不触发的情况

- "dvd"、"data"、"DJVU" 等含 d/v 但语义无关的词
- 在引用历史对话或讨论项目命名时（CC 需要轻判断："Doctor 在询问 vs 在引用"）
