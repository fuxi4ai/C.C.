---
name: brain-anchors
description: Auto-load full project context when Doctor's anchor keywords appear in conversation. Trigger when the user's message contains any of these anchors — "dva" / "DVA", "龙鱼五力", "自检", "天工开物", "渊图" / "行业图谱", "海螺姑娘", "政治经济学", "司南", "O MY HTML", "光通信" — Claude stops the current task and reads the corresponding project's architecture, decisions, and gotchas before responding, so the answer is grounded in that project's accumulated context rather than generic knowledge.
---

# brain-anchors — 锚点触发自动加载

## 触发与对应读取

收到 Doctor 的消息时，扫描以下关键词。命中任何一个，**立即**停下当前任务，先读对应文件，再继续响应。

| 关键词 | 触发读取（按顺序） |
|--------|-------------------|
| `dva` / `DVA` | `brain/DVA/architecture/系统概览.md`<br>`brain/DVA/architecture/决策记录.md`<br>`brain/DVA/GOTCHAS.md`<br>`Projects/DVA/CLAUDE.md`（若存在）<br>`Projects/DVA/GOTCHAS.md`（若存在） |
| `龙鱼五力` | `brain/龙鱼五力/architecture/系统概览.md`<br>`brain/龙鱼五力/architecture/决策记录.md`<br>`brain/龙鱼五力/GOTCHAS.md`<br>`Projects/龙鱼五力/RULES.md`（若存在） |
| `自检` | `Projects/龙鱼五力/RULES.md`（严格用户视角标准化检查流程） |
| `天工开物` | `Vault/天工开物.md`（设计项目启动咒语） |
| `渊图` / `行业图谱` | `brain/渊图/architecture/系统概览.md`<br>`brain/渊图/architecture/决策记录.md`<br>`brain/渊图/GOTCHAS.md`<br>`Database/行业研究/CLAUDE.md`（若存在） |
| `海螺姑娘` / `Conch` | `brain/海螺姑娘/architecture/系统概览.md`<br>`brain/海螺姑娘/architecture/项目概要.md`（若存在）<br>`brain/海螺姑娘/GOTCHAS.md` |
| `政治经济学` | `brain/政治经济学/architecture/系统概览.md`<br>`brain/政治经济学/frameworks/认识论框架.md`（若存在）<br>`brain/政治经济学/GOTCHAS.md`<br>`Projects/政治经济学/GOTCHAS.md`（若存在） |
| `司南` | `brain/司南/architecture/系统概览.md`<br>`brain/司南/方法论概要.md`（若存在）<br>`brain/司南/GOTCHAS.md` |
| `O MY HTML` / `omy` | `brain/O MY HTML/architecture/系统概览.md`<br>`brain/O MY HTML/GOTCHAS.md`<br>**额外**：可加载 `Vault/taste-skills/` 和 `Vault/emil/`（设计 skills） |
| `光通信` / `Optical communication` | `brain/Optical communication/architecture/系统概览.md`<br>`brain/Optical communication/光通信产业链概要.md`（若存在）<br>`brain/Optical communication/GOTCHAS.md` |

## 行为规则

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
