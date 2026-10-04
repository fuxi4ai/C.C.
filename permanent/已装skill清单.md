---
title: 已装 skill 清单
tags: [skill, index, 维护, 真源镜像, 重装手册]
created: 2026-06-30
updated: 2026-09-19
status: active
type: permanent
---

> **2026-09-19 更新**：A/B 段对齐——补 `brain-todo`、`问答板` 两行（此前漏记）；备份列由已禁用的 `Vault/archived/brain/*.skill` 改指 `brain/.skills/{名}.skill`；canonical 口径扩至全部 7 个 brain-\*（见 A 段首注）。

# 已装 skill 清单（真源镜像 + 重装手册 · 唯一真源）

> **本文件是 skill 清单的唯一真源**：既是「切环境该装什么」的真源镜像，也是「备份在哪、怎么装」的重装手册。
> **2026-07-01 合并**：原 `Vault/SKILLS_MANIFEST.md` 已并入本文件（以 brain 为主），那份降为指向本文件的指针，勿再各记一份。
> 状态图例：✅ 已装　⏳ 待装　🚫 本环境不适用（Codex/图生线）。**各环境实时装机状态**以本表「装机」列为准（截至 2026-07-01 官方桌面环境）。

> 每个工作环境的 skill 目录独立，切环境（桌面官方 ↔ gateway/Claude-3p ↔ Claude Code CLI ↔ 换机）就要重装一遍。〔**注（2026-10-03）**：本句系 2026-06 立、为当时实况；**其中「Claude Code CLI ↔ Claude-3p」这一对是否真属不同目录 —— 未核**，见订正④①。〕

---

## A · 自制 brain skills（源 `brain/.skills/{名}/SKILL.md` ＝ **canonical**，备份/重装取 `brain/.skills/{名}.skill`）

> **⚠ 口径（2026-09-19 Doctor 扩充）**：7 个 brain-\* skill 的 canonical 全部 = `brain/.skills/{名}/SKILL.md`；`portable/skills/`、`.skill` 包、各环境安装副本、plugin cache 均为**只读派生**。原「Cowork 账号为主」裁定对 7 个全部退休。
> **⚠ Vault 旧包已禁用**：`Vault/archived/brain/*.skill`（5 件 · 2026-06-30 一批）**不得用于重装**——照旧清单装过会得到六月版。重装一律取本目录 `.skills/{名}.skill`。
> **⚠ 本表 2026-09-19 对齐**：补 `brain-todo`（此前漏记）；各「用途」列括注的版本号可能落后于现行版（如 brain-save 已 v3.5），**以 canonical 文件 frontmatter/正文为准**。

| 装机 | Skill | 触发 | 用途 | 备份 `.skill` |
|:---:|-------|------|------|-----------|
| ✅ | `brain-resume` | `/resume` · "恢复上下文" | 跨 session 拉回工作状态 | `brain/.skills/brain-resume.skill` |
| ✅ | `brain-save` | `/save [主题]` · "存档" | 落盘会话 + 提供 git 命令（per-agent 归位） | `brain/.skills/brain-save.skill` |
| ✅ | `brain-note` | `/note [主题]` · "起一条笔记" | inbox/ 采集态 | `brain/.skills/brain-note.skill` |
| ✅ | `brain-anchors` | 关键词监听（dva·龙鱼五力·渊图·白泽…）**＋纪律锚（审核者·复核·复审·复验·独立复核·核验·审计·挑错·对拍·二审·改动面·damper → 加载 damper）** | 自动加载项目/数灵上下文；**兼作 damper 的手动兜底路由** | `brain/.skills/brain-anchors.skill` |
| ✅ | `brain-prd` | `/prd [任务简称]` · "立PRD" · "起草PRD" · "写交付标准" | 立 PRD——功能/需求验收基线，不是审批单 | `brain/.skills/brain-prd.skill` |
| ✅ | `brain-consolidate` | `/consolidate` · "固化记忆" | brain 日志蒸馏入 permanent | `brain/.skills/brain-consolidate.skill` |
| ✅ | `brain-todo` | `/todo` · "处理待办" · "清 TODO" | 漏挂对账 + 逐条现核 + 六类分流 + 勾完才落盘（v2.1 目标模式） | `brain/.skills/brain-todo.skill` |

6 个 2026-07-01 官方环境全部重装到位（从现源重打包、frontmatter 引号合规、`brain/.skills/` 镜像同步刷新）。**已弃用**：`_DEPRECATED_brain-commands`（早期合并版，存档可删）。

### A2 · 新立（2026-10-02 · **未进发布链，待 Doctor 装**）

| 装机 | Skill | 触发 | 用途 | 备份 `.skill` |
|:---:|-------|------|------|-----------|
| ✅ | `damper`（减震器） | **关键词**：审核者 · 复核 · 复审 · 复验 · 独立复核 · 核验 · 审计 · 挑错 · 对拍；**改动前**：对既有资产的修复／订正／补正／加固／收口／落地／重判／指针替换类修改 | 改动面纪律——治「改这个动作顺手带出的新毛病」· **十一族（含「多改」「修红反噬」「处方缺件」三个方向）** ＋ 改前/改中/改后三阶段动作 ＋ 顺手机制六型 ＋ 新错回灌通道 | `brain/.skills/damper.skill` |

> **来历**：2026-10-02 立。Doctor 令「复核专项——把复核中提炼的 gotchas 去重、整合、再精炼成一个关于复核/审核者的新 skill」，判据由 Doctor 收窄为「**大部分是改的时候因为一些失误『顺手改出的新毛病』**」。
> **语料**：`brain/logs/checkups/` 2026-09-29–10-02 的 24 份复核件 ＋ 改动痕迹反查（备份件与提交记录）；双 subagent 采集出 52 ＋ 6 条实例，聚类成**九族**，**36 例带出处写进 skill**。
> 〔**2026-10-03 · v2.0 起为十一族／40 例**（补族 10「修红反噬」· 族 11「处方缺件」）—— 上一行的「九族 / 36 例」是 **10-02 那一版的实况**，按历史留痕**保留不改**，此处只挂同期指针。〕
> **四轮独立复核（均由未参与实施的 subagent 执行，四轮全判 `PASS_WITH_LIMITS`）**：一轮 11 项（F1–F11）→ 二轮 8 项（N1–N8）→ 三轮 6 项（新1–新6）→ 四轮 2 实缺陷 ＋ 4 观察。**每轮都在本 skill 自己身上逮出它自己列的族**——最刺眼的是「族 1 标题的最高级」连续三轮出问题、「同一结论以另一形态活在同一文件另一节」。**收敛 11→8→6→2**，且第四轮的 2 条**全部落在上一版刚改过的行**、未改动部分零新发现；审核者结论「不再追加纯文档复核轮」，**安装建议 GO_WITH_FIXES · blocker 无**。⇒ **本件的病历本身是本件最有说服力的部分**（全部留痕在件内 `## 修订记录`）。
> **Doctor 两条指令（2026-10-02 追加）已落地**：①「回扫该处所在段落」做成**可执行工具** `brain/.tools/check_edit_context.py`（427 行 · 自检 18/18 · 豁免守卫经变异检验有齿）；② skill 内新增 **§二「顺手是怎么发生的（相似性分型）」**（六型相似性 ＋ 反直觉结论「刚改过的那几行是高危区」）与 **§七「新错回灌」生长通道**，并据此立 **族 8「凭记忆构造替换操作数」**（同日 3 例，依据即该通道「同根同日 ≥3 次」）；③ **一处结构性纠正**——Doctor 指出「**不是单说不要漏改的问题，还有『多改』、『改了不该改的东西』的问题**」⇒ 六型**只覆盖「漏改」一个方向**，本版据此新增 **§二 2.3「两个方向」**（多改 vs 漏改对照）＋ **族 9「多改（动了点名范围之外）」**（五子形态 ＋ **准入判据**），§五 改前由四件扩为**五件**（新增**禁改清单** ＋ **重写阈值**）。
> **⚠ 状态（2026-10-02 终）**：**四端全部对齐、逐字节一致 ✓** —— canonical ＝ `portable/skills/damper/SKILL.md` ＝ 包内件 ＝ **runtime 安装副本**，`check_skill_parity.py --path… --all --name damper` **实跑 rc=0**（四端指纹均 `283f94f9`，机器判定「仓内三端一致 · 四端一致 ✓」）。canonical **465 行 / 52486 B / sha256 `283f94f913441dc4…`**；包 `brain/.skills/damper.skill` sha256 全串 `967ea773e2be2ed0343e8e6fbefb9abc6d0ac270cdc63e867dbd013d583ca8fd`。
> **✅ 本行现为「已装」**（装机列已翻 ✅）。**本仓头一次四端这么干净**——前三例 runtime 均有缺口（`brain-save` description 缺 2 字节 · `brain-todo` 正文缺 95 字符），本次走 `.skill` 包安装、**未跑 `save_skill` 长正文**，故无丢字。
> ⚠ **一处自犯留痕（供后人核对）**：本轮写上面这条状态时，我先写下了「装机列见上表 ⏳ 待改 ✅」——**把待办写进注里却没去改那一列**（族 7「声称做了但没做」的形态）；由改后自核当场逮出，已同批补改。
> **⏳ 仅剩一项未验**：**关键词路由的自动触发**——「skill list 可见 / 能手动加载」**不等于**「说『复核』它会自动起手」。本仓 `brain-prd` 有先例（cache 更新过但真实路由仍须单独实测）。⇒ **待下次全新会话，说一句带「复核／审核者」的话验它。**
> **来源** → `brain/.skills/damper/SKILL.md`（含四轮复核发现与逐版修补留痕）· 论证层见同目录 `机制与约束条目详解.md`
> **命名**：2026-10-02 由 `change-guard` 改名 **`damper`（减震器）**（Doctor 令）——取工程义「吸收振荡、不让它传下去」，对应本 skill 的职能：把「顺手」的冲击吸掉、不让它传到文档里。⚠ **清单显示名由目录名决定**（2026-09-26 实测），故目录名、frontmatter `name`、本表名三者必须一致；**本 skill 从未安装，改名无旧副本需回收**。

> **⚠ 2026-09-26 一处已知 runtime 偏差（`brain-save` · 无害 · 刻意不修）**：当日经 `save_skill` 重装 **v3.7** 时——**正文 47147 B 逐字节全等**（runtime `f689c39f…` vs canonical `5cd5784e…`，仅尾随换行差 1 字节），但 **description 尾部少 2 字节的 `` `**` ``**（runtime 996 字 / canonical 998 字），系**传参时漏写该收尾加粗标记**。**影响＝零**（description 只是触发索引；且该 `**` 落在 YAML 双引号标量内，是普通字符）。**刻意不重修**：`save_skill` 只能**整体重传**，为 2 字节再传一次 45 KB，**有把已经逐字节正确的正文传歪的风险——期望收益为负**。⇒ **日后 `check_skill_parity.py` 报 `brain-save`「runtime 分歧」时，看本条即可，不必再查**；真要对齐，走 `.skills/brain-save.skill` 包由 Doctor 复装（那条路是逐字节的）。
>
> **⚠ 2026-09-29 补记（第 2 处 · `brain-todo` · **形态不同、有实质缺口、非无害**）**：当日 skill 发布链**全量四端对拍**（7 个 brain-\*）暴露第二处 runtime 偏差。**上条是 description 缺 2 字节（影响＝零）；本条是正文缺 95 字符。** 实读：`brain-todo` 安装副本的 **M5 行尾部被截**，缺的正是「**签字分轨：事实性的签字/验收 → 开未参与实施的审核者 subagent 落签，方向性 → 直接问 Doctor（2026-09-19 Doctor 立）**；AskUserQuestion 选项 label 尾部钉（推荐/不推荐）」**及其出处栏**（`G-X4 · G-X136 · brain-save v3.3 · 2026-09-17 · 2026-09-19`）。**数据**：canonical `26686 B / 266 行 / sha 16539af4` vs runtime `26515 B / 267 行 / sha d81a8fa8`——差 171 B ＝ 95 字符正文 ＋ 尾随空行归一。**根因指向** `save_skill` 第四跳的「LLM 复述长正文」漂移（该风险本身已登记于 [[Doctor协作偏好]] 发/收段）：26 KB 正文丢字，落在**表格长行**上。**⚠ 判据订正（本条最重要的一点）**：上条末句写的「日后 `check_skill_parity.py` 报 `brain-save`『runtime 分歧』时看本条即可，不必再查」，**不适用于本条**——它把「runtime 分歧」整体当成了已知无害项，会让**正文缺口**被一并跳过。⇒ **改为**：见 parity 报分歧，**先判差在 description（触发索引·影响低）还是正文（规则本体·可能是真缺口）**。**可靠修法**：**仓内三端一致（canonical ＝ portable ＝ 包内 `16539af4`，parity 实跑确认）⇒ 包是逐字节正确的**，走 `.skills/brain-todo.skill` 由 Doctor 复装即可对齐；**不建议**再跑一次 `save_skill` 长正文复述（**风险大于收益**——正可能制造第二处同类缺口）。**另附订正**：上条引的 SHAs **两端均已过时**（canonical `5cd5784e…` → 现 `7a0e7248…`；runtime `f689c39f…` → 现 `272d82dd…`）——**现象仍成立，但所引指纹已不能用于回读核对**；且本场实测 `brain-save` 当前差异＝description 缺尾 `**`（983→981 字）＋ 尾随空行 1 字节，与上条所述**同现象**，未生新变。**来源** → logs/2026-09-29-发声系统切eleven_v4.md

---

## B · 自制其他 skills（源 `brain/.skills/`）

| 装机 | Skill | 触发 | 用途 | 备份 `.skill` |
|:---:|-------|------|------|-----------|
| ✅ | `gsap-frontend` | 硬专名 "GSAP/gsap/GreenSock" | GSAP 前端动画（主干 + 5 references；粘性生效） | `brain/.skills/gsap-frontend.skill` |
| ⏸ | `handshake-consumer` | 定时/手动 | 方案 B 跨 AI 握手消费端——**方案 B 搁置，暂不装** | `brain/.skills/handshake-consumer.skill` |
| ✅ | `问答板`（机器名 `QA`） | 「问答板」· `/qa` | 多裁定项收成单文件暖色 HTML 对齐页（**2026-09-19 补记**；真源即 `brain/.skills/问答板/`，不在 portable 链上） | `brain/.skills/问答板.skill` |

> **⏸ 另有一个不在本链的已装技能（2026-09-19 补记）**：**`equity-thesis`**（个股定性研究）——
> **canonical 在 Codex 侧**：`Codex/Infrastructure/skills/equity-thesis/`（**VV 维护**，CC 不覆写）；
> CC 侧 `brain/portable/skills/equity-thesis/` 是**单向接收的落盘副本**（与交接包 + Codex canonical sha256 三方一致），**无 `.skill` 包**；桌面侧经 `save_skill` 注册为 `equity-thesis`。
> 2026-09-11 经 Doctor 投递交接包装毕（来源提交 `bf21616`）；后续版本从 Codex canonical **单向重新交接**。
> ⚠ **别把「portable 是派生」的通则套到它身上反推上游**——它的上游是 Codex，不是 `.skills/`。

> **⚠ 三族 skill 的「portable 是什么」各不同（2026-09-19 立）**：① **brain-\* 7 个** → portable 是 `.skills/{名}/SKILL.md` 的派生；② **equity-thesis** → portable 是 **Codex canonical** 的派生；③ **gsap-frontend / 问答板 / handshake-consumer** → 不在 portable 链上。**别用一条通则套三族。**

`gsap-frontend` 2026-07-01 官方重装（v2.1，基于 greensock/gsap-skills 蒸馏）。

---

## C · 第三方设计线（taste pack · 来源 `github.com/Leonxlnx/taste-skill`，备份 `Vault/archived/taste-skills/`）

Claude Cowork 可用（纯设计指导，不依赖图像生成）：

| 装机 | Skill | 用途 |
|:---:|-------|------|
| ✅ | `design-taste-frontend` | Senior UI/UX 规范，三旋钮系统（DESIGN_VARIANCE/MOTION/DENSITY） |
| ✅ | `minimalist-ui` | Editorial 极简风（金融项目推荐） |
| ✅ | `high-end-visual-design` | 高端 agency 视觉标准（字体/间距/阴影/动画） |
| ✅ | `full-output-enforcement` | 禁默认截断/占位符/偷懒 |
| ✅ | `redesign-existing-projects` | 审计改造现有站点到高端质感 |
| ✅ | `stitch-design-taste` | 为 Google Stitch 产 DESIGN.md 设计系统 |
| ⏳ | `industrial-brutalist-ui` | 野兽派工业风（BETA·**待装**，在 `Vault/taste-skills/`） |

### C-Codex · 图生线 🚫 本 Cowork 环境不适用（2026-07-01 移至 `Vault/Codex/`）

这些依赖 agent **原生图像生成**（GPT/Codex 能力）；Claude Cowork 无图像生成工具、装了空转，故从 taste-skills 分出、独立成 `Vault/Codex/`。要用请到 Codex/GPT 端。同源 `Leonxlnx/taste-skill`。

`gpt-taste`（GPT/Codex 严格变体）· `image-to-code`（含 CODEX-SPECIFIC 段）· `imagegen-frontend-web` · `imagegen-frontend-mobile` · `brandkit`

---

## D · 其他第三方设计 skills

| 装机 | Skill | 来源 / 备份 | 用途 |
|:---:|-------|------|------|
| ✅ | `emil-design-eng` | `github.com/emilkowalski/skill` · `Vault/archived/emil/` | Emil Kowalski 动画/微交互 12 条原则 |
| ✅ | `impeccable` | `Vault/archived/impeccable/` | UI 全面审计/改造（含 23 个 slash 命令） |
| ⏳ | `frontend-design` | 存疑（旧清单列过、无本地源、当前未见） | 待核是否真装过 |

---

## E · 系统级 / 官方 skills（Tier 1 · 跟环境走，本地备份 `Vault/archived/system-skills/`）

理论上 Max/官方账户下自动可用；丢失先从 Settings 面板重启用，再不行从 `Vault/archived/system-skills/` 重装。

**文档**：`docx` · `xlsx` · `pptx` · `pdf` · `pdf-reading`
**通用**：`consolidate-memory`（针对 MEMORY.md，与自制 `brain-consolidate` 共存·后者声明"取代"避免抢戏）· `schedule`（定时任务）· `setup-cowork`（初设）· `skill-creator` · `full-output-enforcement`
**研究**：`deep-research`
**斜杠命令型**：`init` · `review` · `security-review`
**其他备份**：`conch`（`archived/system-skills/conch.skill`，`/conch` 项目整理）

---

## F · 海螺项目内自制 skill（2026-07-01 扫出·本清单原漏记）

源在 `Projects/海螺姑娘/`，**当前未作 Cowork skill 装**——Doctor 决定**先用一用、积累经验再适配**（合 G-X10「规则从失败里长」）。想装先修 frontmatter 引号 + 重打包。

- `conch`（`/conch` 项目维护，有 `Projects/海螺姑娘/conch-v0.2.skill` 包）
- `meditation`（brain 体检，已被 `brain-monthly-checkup` 定时任务直调 `meditation.py`，未必需作 skill）
- `project-review`（关键迭代按 PRD 审代码）

---

## G · 工作环境与 skill 安装机制映射

| 工作环境 | 安装机制 | 备注 |
|----------|---------------|------|
| **Claude 桌面应用（官方版·当前）** | 双击 `.skill` → 系统弹卡片 → "Save skill" → `~/Library/Application Support/Claude/skills/<name>/` | bundle id `com.anthropic.claudefordesktop`；不支持自定义 base_url。**frontmatter 无引号也能装**（比 gateway 宽松，Doctor 2026-07-01 更正） |
| **Cowork / Claude-3p（gateway 模式）** | **Settings → Skills 入口手动选 `.skill`**（plugin 体系）；落 **plugin 缓存** —— **沙箱内只读可见于 `<挂载根>/.claude/skills/`**（2026-10-03 实测：mode `0500` · **非符号链接** · 沙箱不可写） | 应用本体 `~/Library/Application Support/Claude-3p/skills/` **不扫**。⚠ **`~/.claude/skills/`（见下行 Claude Code CLI）与本行的 plugin 缓存是否同一目录 —— 未核**：据 **Doctor 终端实读**，该路径下**无 damper**，而 plugin 缓存下有 ⇒ **两层至少在该件上不同**（该终端读数本沙箱**不可复现**；诚实边界与反向线索见订正④①）。present_files 卡片不弹 Save 按钮 → 交付附 `open -R` 一键定位 |
| **Claude Code CLI** | `~/.claude/skills/<name>/`（「**与 gateway 共用文件系统**」系 2026-06 旧记，**未复验**；与上行 plugin 缓存的关系见订正④①） | 走 `ANTHROPIC_BASE_URL` |

**切环境踩坑教训**：① 2026-06-30 上午：自制 skill 只装桌面、`.skill` 没落 brain → 切 gateway 丢失、源找不回 → 对策：`.skill` 必落 `brain/.skills/`。② 2026-06-30 晚：Cowork 装 skill 非 `~/.claude/skills/` 直放，实测不读；正解 Settings 手动选。

---

## H · 加载约定（避免技能污染）

- **设计项目**（O MY HTML、前端 UI）：按需激活 C/D 栏设计 skills（taste-skills、emil、impeccable）。
- **非设计项目**（DVA、龙鱼五力、渊图、PEC、金融线）：**不激活**设计 skills，保持后端/数据风格。

---

## I · 维护偏好（与 [[Doctor协作偏好]] 同步）

1. **`.skill` 包必落 `brain/.skills/`**：自制 skill 定稿即打成 `.skill`（zip 改名）放 `brain/.skills/<name>.skill`——跨环境唯一真源，brain 在就能一键复装。
2. **改 skill 源后必重打包**：运行时走已装缓存，改源不重装不生效。改完 present_files 交付（gateway 弹不出卡片则让 Doctor 去 Settings 装，附 `open -R`）。
3. **切工作环境后第一件事**：对照本清单逐栏重装自制 skill（A/B）；系统级（E）一般跟环境走。
4. **Cowork frontmatter 范式（gateway 硬约束）**：`name:`/`description:` 值必须 `"..."` 包裹、内部 `"` 转义 `\"`，否则 gateway plugin parser 报 `frontmatter missing name or description`。**官方桌面版无此限**（2026-07-01 Doctor 更正）。详见 [[通用教训]] G-X43 / ERR-20260630-COWORK-FRONTMATTER。

---

## J · 切环境完整重装 SOP

1. 切账户/环境后，试 Tier 1（如对话里试 `/conch`）；不可用则 Settings 重启用，再不行从 `Vault/archived/system-skills/` 重装。
2. 自制 skill（A/B）从 `brain/.skills/` 重装（gateway 走 Settings）；对照本表逐个。
3. 设计线（C/D）按需从 `Vault/archived/taste-skills/`、`Vault/archived/emil|impeccable/` 重装；优先 `impeccable` / `design-taste-frontend` / `full-output-enforcement`。
4. **Codex/图生线在 `Vault/Codex/`——本环境不适用、勿装。**
5. 定时任务 / artifacts 另见 [[切环境复原清单]]（skill 只是其中一类）。

---

## 来源

- **taste-skills/**（设计品味合集）：`github.com/Leonxlnx/taste-skill`
- **emil/**：`github.com/emilkowalski/skill`
- **system-skills/**：Anthropic/Cowork 提供，本地打包备份（2026-05-14）
- **brain/**、**gsap-frontend**、**海螺三 skill**：自制

---

## 相关笔记

- [[切环境复原清单]]（切环境要复原的 5 类总索引，skill 是其一）
- [[Doctor协作偏好]]（skill 打包/安装偏好出处）
- [[通用教训]] G-X43（Cowork frontmatter 范式）
- [[项目总览]]（anchor 触发依赖 brain-anchors 在装）
- logs/2026-06-30-gateway切换善后-skill与artifacts补迁.md（本清单初立 + frontmatter 根因）
- logs/2026-07-01-切回官方-重建定时任务与skill.md（官方环境重装 + Vault 合并）
> **brain-anchors 纪律锚批次（2026-10-02）部署对拍（机器证据）**：canonical ＝ portable ＝ `.skill` 包内 ＝ **runtime 安装副本** 四端 **逐字节一致 sha256 `288745a3b64729c2…`（15771 B）**；`check_skill_parity.py --docs <挂载根> --runtime <挂载根>/.claude/skills --name brain-anchors` → 四端列 **`288745a3 288745a3 288745a3 288745a3` · rc=0**（⚠ **不带 `--runtime` 的命令不足以支撑本结论**：该器默认 runtime 候选全在 `{home}` 下、沙箱里恒不可达，此时它仍打绿 rc=0——见 `ERR-20261002-003`／`-004`）；runtime 副本落盘 `2026-10-02 18:36:02`（**plugin 缓存** `<挂载根>/.claude/skills/brain-anchors/SKILL.md` —— 原文把该处指到 **Code CLI 那一层**〔**关键串按 PEC `G-35` 遮蔽，不逐字抄入留痕**〕，**层错了，已按 2026-10-03 实测订正**，见下方订正④）。⚠ **路由（是否会因「复核」自动起手）未验**——本会话注入的清单在起手即定格为旧版，须**全新会话**实测。
> **⚠ 订正（2026-10-03 · 承 CC 实读四端 sha256 对拍）**：本页上方两处「四端一致」陈述**均已过期**，且第 56 行一句**已不成立**——
> ① **`brain-anchors`**：canonical ＝ portable ＝ 包内 现为 **`c4e78e22` / 15777 B**（18:36 之后，纪律锚表行与触发示例由「九族 36 例」改述为「**十一族 40 例**」）；**runtime 安装副本仍为 `288745a3` / 15771 B** ⇒ **四端差 1 版**，新会话拿到的是旧措辞。
> ② **`damper`**：canonical ＝ portable ＝ 包内 现为 **`8dbb78e6` / 78338 B**（已长到**十一族**）；**runtime 安装副本仍是 `f240a5db` / 59199 B** ⇒ **差 2 版**。故第 51 行所记 `283f94f9` / 52486 B 为历史值；**第 56 行「本 skill 从未安装」为假**——runtime 副本实存于 **plugin 缓存** `<挂载根>/.claude/skills/damper/SKILL.md`（**原文把该处指到 Code CLI 那一层**〔**关键串按 PEC `G-35` 遮蔽**〕，**层错了** —— Mac 上该层路径下**并无 damper**，2026-10-03 终端实测；详见下方订正④）。
> ③ ⇒ **两个 skill 都需重新安装**（`.skill` 包均已重打、仓内三端齐整）；装完本页两行才能回签。
> **判据**：HEAD（`9d7d13f3`）树内 blob 与盘上文件**逐字节对拍 8/8 一致**（并据此确认当日那笔 commit 未丢件）——四项 sha 均可复算。
> **✅ 订正②已闭（2026-10-03 01:17–01:18 重装完成）**：两个 skill **四端均逐字节一致** —— `brain-anchors` **`c4e78e22db4d6210` ×4**（15777 B · runtime 落盘 01:17:37）· `damper` **`8dbb78e62e4fdfb2` ×4**（78338 B · runtime 落盘 01:18:04）。机器判据：`check_skill_parity.py --docs <挂载根> --runtime <挂载根>/.claude/skills --all` 输出表内两行**均为「仓内三端一致 · 四端一致 ✓」，且不在问题清单中**。（该跑的 **rc=1 系别家 skill 所致，与本两者无关**——见下条。）
> **⚠ 订正④（2026-10-03 03:31 · 承 Doctor 终端实测 ＋ CC 沙箱回读；**本块经未参与实施的独立复核，首轮判 FAIL，①③④ 与 G 段两行已按复核订正**）——「两层 runtime」分层 ＋ damper 复装落地**：
> ① **分层纠正（**范围受限版 · 承独立复核**）**：本页 193／196 两行把 runtime 副本的落点写成了 **Code CLI 那一层的路径**〔**关键串按 PEC `G-35` 遮蔽，不逐字抄入留痕**〕。**已核实的只有 (a)**：**plugin 缓存层** ＝ 本 3p 壳**加载**的副本，沙箱内**只读可见**于 `<挂载根>/.claude/skills/`（mode `0500` · **非符号链接** · 沙箱不可写 · 内容与本壳注入的 skill 清单 **1:1**）。**(b) Mac 上的 `~/.claude/skills/` 沙箱不可达**：据 **Doctor 终端实跑** `--runtime ~/.claude/skills --name damper` ⇒ **「runtime 缺该 skill」**，而同名件在 (a) 下存在 ⇒ **两层至少在该件上不同**。**⚠ 已核边界（2026-10-03 03:3x · 承 Doctor 终端探针）**：该终端读数本沙箱不可复现（另有未参与实施的复验者在**同刻**读数上另行支持了「至少在该件上不同」）。**至于 (a) 与 (b) 在别处是否同一目录 —— **已定案：不是**。**判据（Doctor 终端实跑 `ls -ld ~/.claude ~/.claude/skills && readlink -f ~/.claude/skills`）**：`/Users/lunarabbit/.claude/skills` 是**实体目录**（`drwxr-xr-x` · **12 条目** · mtime `2026-08-02 09:38` · `readlink -f` 回自身 ⇒ 非符号链接），而 (a) 侧为**独立 `fuse ro` 挂载 · 31 条目 · 含 damper** ⇒ **条目数不同＋有无 damper 不同＋mtime 不同**，三证同向。**（反向线索保留**：`<挂载根>/.claude/projects/` 挂着**本会话自己的实时 transcript**，形状与 Claude Code 的 `.claude/projects/` 树一致 —— 该线索指向「编排层构造形状」，**不翻本结论**，但说明「同源」不能靠形状推断。）⇒ **操作口径**：验 runtime 端**指向 (a)**；把 (b) 的结果当 (a) 的读数＝错。
> ② **damper 复装已落地**（2026-10-03 **03:29**）：经 **Settings → Skills 入口**装 `brain/.skills/damper.skill` ⇒ plugin 缓存副本刷新为 **`6812485d6893fb1c…` / 87157 B**（此前 `8dbb78e6` / 78338 B · mtime 01:18）。**机器判据**：`check_skill_parity.py --docs <挂载根>/Documents --runtime <挂载根>/.claude/skills --all --name damper` ⇒ 表内一行 **`6812485d 6812485d 6812485d 6812485d` · 「仓内三端一致 · 四端一致 ✓」**；另 `cmp` 与 canonical **逐字节相同**（87157 B）。⇒ **本页 199 行所记的 `8dbb78e6 ×4` 已被本行取代**（该行是其时点的真实读数，按留痕保留不改）。
> ③ **`brain-save` 的两侧版本（2026-10-03 · **承独立复核订正 —— 本条第一版把两侧写反了**）**：**canonical**（`724c0866` / 49029 B）＝「**一律**读 `.gitignore` 手判」**并明文禁跑 `git check-ignore`**；**runtime**（`272d82dd` / 48727 B）＝**旧版**「**有 git 环境者跑 `git check-ignore -v <paths>`**」。⇒ **含禁 git 明文的是 canonical，字面许可跑 git 的旧版在 runtime**。〔第一版写成「runtime 是一律手判版、canonical 是 check-ignore 版」，**两侧颠倒** —— 由未参与实施的复核者实读两侧正文逮出；根因＝读对拍器 **`runtime 分歧` 备注里那段 `-`／`+` 文本**时归错了侧（源码实读：该器 `difflib.unified_diff(a=canonical, b=runtime)` ⇒ **`-` 属 canonical、`+` 属 runtime**，我误把 `+` 侧当了 canonical）。〕⇒ **推论随之反转**：装上去是把 runtime **升到**已订正的安全版，**不是**「把规则冲突推进 runtime」；原「刻意不装」的理由**不成立**。（是否现在装仍由你定，但别再以那条为前提。）
> ④ **`brain-consolidate`**：canonical 与 runtime **仅差末端空行**（canonical 尾 `。\n`／runtime 尾 `。\n\n`，`rstrip(b'\n')` 后相等）⇒ **同一版 modulo 尾换行**，**非「差一版」**〔第一版措辞自相抵，已订正〕；无害，不单独重装。
> ⑤ **未验**：新包的路由（说一句带「复核／审核者」的话是否自动起手）—— 本会话 skill 清单**起手即定格**，须**全新会话**实测。
> **⚠ 订正⑤（2026-10-03 04:4x · 承 Doctor 复装 ＋ CC 沙箱回读）—— damper 再两跳，本条接续 ④②**：
> ① **04:38 复装**（Doctor 走 **Settings → Skills 入口**，界面提示 `Replaced damper`）：**四端逐字节一致** —— canonical ＝ portable ＝ 包内件 ＝ **runtime 安装副本** ＝ **`e6f92119…` / 76736 B**（runtime mtime `04:38` · `cmp` 与 canonical 逐字节相同 · `check_skill_parity.py --runtime <挂载根>/.claude/skills --all --name damper` 表内**四列同值 · 「仓内三端一致 · 四端一致 ✓」**）。⇒ **本页 199 行所记 `8dbb78e6 ×4` 与 ④② 的 `6812485d` 均已被取代**（各为其时点真值，按留痕保留不改）。
> ② **04:43 再落一句**（`--root` **覆盖而非叠加**的语义澄清 · 1 hunk）：canonical ＝ portable ＝ 包内 ＝ **`6848ca13…` / 76966 B**；**runtime 落后、且仅落后这一句** —— 纯文档澄清、**零行为差异** ⇒ **不必为此单独复装**，并入下次实质改动一起装。
> ③ **内容抽查（Doctor 界面所见 × 盘上）**：安装副本 §三 族 1 标题为「（**4 例**）」· 段内例数 **4** · 含本场新增的「**同义型 · 2026-10-03**」条 ⇒ **与 Doctor 界面所见吻合**。
> ④ **仍未验**：新包的路由（说一句带「复核／审核者」的话是否自动起手）—— 本会话 skill 清单**起手即定格**，须**全新会话**实测（同 ④⑤）。
> **⚠ 顺带实读（非本次改动 · 仅登记，未处置）**：同一跑 `--all` 报 **15 项问题**〔**时点读数 · 2026-10-03 04:4x 复跑已变 16** —— 多出的正是 `damper: runtime divergent`，由本页订正⑤② 自身造成 ⇒ **引用本数前先现跑**〕，全部落在**其它 skill**：`brain-save`（runtime 真分歧）· `brain-consolidate`（runtime 仅差末端空行，属已知归一化；⚠ **该器不计入问题清单**，原文随同列出仅备查）· 及 `QA`／`audit`／`gsap-frontend`／`handshake-consumer`／两个 `_DEPRECATED_*`（**portable 端为空或缺失**，其 hash 显示为 `e3b0c442`＝空文件指纹）。**未判**这些「缺 portable 端」是**设计如此**（非 brain-* 家族本就走 `.skill` 包）还是**真缺口**——沿既有 TODO「`QA` skill 不在 parity 射程内」另议。**本条只登记，不动手。**
>
> **⚠ 订正⑥（2026-10-03 05:25 初写 · **05:37 就地订正**（承 ⑰／⑱ 复验处方）· CC 沙箱回读 · 承 /resume 核）—— 本条取代订正⑤②的指纹读数**：**damper 04:49 定稿 ＝ `47f0df04` / 77113 B / 520 行**（canonical ＝ `portable/skills/damper/SKILL.md` ＝ 包内件，**三端逐字节同**；`sha256sum` 与包内件解压复算双侧同值）。订正⑤② 所记 **`6848ca13…` / 76966 B** 系 **04:43 中间态**的时点真值，**已被 04:49 的扩写取代**（按本页惯例：**旧行保留不改**）。
> **04:43 → 04:49 的实际动作 ＝ 同一行的扩写**（非新增第二处）：补上「**两子命令同吃此语义**」「**只有 `anchors` 打印实际扫根**（`citer` 连扫根都不打印）」「**两者都不校验覆盖完备性** —— 根给错或给少，闸不报警」。**相对其前一版（`e6f92119` / 76736 B，即 HEAD~1 `e0e2148b` 内所存那一版）的净差 ＝ 恰 +1 行**（对拍物 `SKILL.md.bak_rootfix_20261003_0443`，实核其 76736 B 与该版逐字节相同，故该「+1 行」不是估计值）。**runtime 仍 `e6f92119` / 76736 B**（04:38 装）⇒ **落后 canonical、且仅落后这一行**。⚠ **「零行为差异」须收窄（承 ⑰ 复核）**：本件**正文即操典**，这一句是**给调用者的规范性指引**（要求显式列全本批扫根），故「零差异」**只在「无代码改动」意义上成立**，不等于「不影响用法」—— 但**仍不必为此单独复装**（属文档级指引澄清，与该件既有「并入下次实质改动」口径一致）。
> **⚠ 留痕缺口 —— 本段初版结论有误，已按独立复核（`_repair_audit.md` ⑰）订正**：初版写「04:49 这一版在**全树零留痕**、**本行即其唯一盘上记录**」，**该结论不成立**。〔**初版错在哪**：我只扫了工作区（`find -newermt`，且命令行 **prune 掉 `.git`**）与 `grep` 明文字串，**没有回读 `.git/logs/HEAD`** —— 而该版**已于 `2026-10-03 05:18:52` 提交为 `1d60a60a`**（`refs/heads/main` 现值；commit message「damper: --root 覆盖语义澄清 + 注册档订正⑤」；`.git/COMMIT_EDITMSG` 另存「damper: --root 覆盖语义完整版（+1 行）+ 已装skill清单订正⑤」），**三端 blob 逐字节在库**。我 04:46 读过一次 HEAD、此后未再回读，**把旧读数当了现状** —— 族 6/7 同型，由**未参与实施的复核者**实读 `.git` 对象网逮出。〕⇒ **正确结论：04:49 版留痕完整、回退有据** —— 三端内容在 HEAD `1d60a60a` 内逐字节可取（`.skills/damper/SKILL.md` ＝ `portable/skills/damper/SKILL.md` ＝ blob `a16b13a6…`；`.skills/damper.skill` ＝ `0290a91e…`，包内件同 `47f0df04`）。**留痕语义内仍缺两件**（**⚠ 非穷尽枚举** —— 按 ⑱ 复验 L1 收窄：另有两项不在留痕面内，见本块前後两条 —— 派生端未同步该版、编辑操作者归因未核）：① **无会话日志、无审核件**（该版未走 /save、未过独立复验）；② **04:43 那个中间态（`6848ca13` / 76966 B）无任何物证** —— 全对象网 3340 枚散装对象 ＋ pack 全解 9709 枚中**均无 76966 B 目标件** ⇒ 该中间态**只存在于订正⑤② 的文字里**。
> **归因未核**：可复现的时序只有三条 —— `04:49:16.036` 改 skill → `04:49:31.947` 重打包（+15.9s）→ `04:49:32.217` 同步 portable（+0.27s）；初版另记的「+0.8s 改本页」**现已不可复现**（该 mtime 已被本次追加覆盖），且初版「盘上只见」**过窄** —— `05:18:52` 的 commit 与 `05:22:15` 的 `COMMIT_EDITMSG` 同在该归因面上（其 git 作者字段记 **Doctor**，属**弱证据**，不足以定论）。**04:49 那笔编辑的操作者：未核**（另有会话多线作业；沿本日早场「并发写入者」两条的口径：只登记、不代认领）。


> **⚠ 订正⑦（2026-10-03 22:3x 夜 · CC 沙箱回读 · 承 /consolidate 收尾场）—— damper §七 回灌批 + brain-anchors 派生计数同步**：
> ① **damper 回灌 7 项落地**（Doctor「全部批准」）：族 1/6/7/8/9 各加一例 ＋ 族 1 门禁补「派生链盘点」＋ 族 5 门禁补「快照清单逐件对账」＋ 族 9 子形态表补一行 ⇒ **族例 40 → 46**（族 1＝5 · 族 8＝4 · 族 9＝5 例·6 子形态）。经**改后独立复核判 PASS_WITH_LIMITS**（4 项必须回改已改：族 8 引言过期活文 · 「五种子形态索引」标签 · 逐字锚 · 跨件派生计数），回改后三端重打。**终态**：canonical ＝ portable ＝ 包内件 ＝ **`7c8f9ba7d402eaa4…` / 529 行 / 83,015 B**（⚠ 本行初写「530 行」系凭印象、未现数——落盘后 `wc -l` 实核 529，就地订正）。
> ② **runtime 落后**：安装副本仍 `e6f92119` / 76736 B（04:38 装）⇒ 落后 canonical **两个状态**（04:49 定稿 `47f0df04` ＋ 本批）。**复装归 Doctor**（Settings → Skills 入口装 `brain/.skills/damper.skill`）。
> ③ **brain-anchors 派生计数同步**：路由行「十一族 40 例」→「**46 例**」（本批族 1 门禁「派生链盘点」的直接执行）；三端重打 = `1a59793a38368da6…`。其 runtime 亦落后（`c4e78e22`），并入下次实质改动一起装。
> ④ **依据**：`brain/logs/checkups/2026-10-03_consolidate收尾_冲突清单_v1.md` §八/§九 ＋ 本批改后独立复核报告（会话内 subagent，未落盘——⚠ 该报告仅存在于本场会话，如需盘上留痕可要求落盘）。


> **⚠ 订正⑧（2026-10-03 22:4x · CC 沙箱回读 · 复装核验）**：**damper runtime 已复装、四端一致 ✅** —— 安装副本 `7c8f9ba7d402eaa466cf2486f7d8099ebac2e955a7d1ff59cd27a05d37467cbc`（完整 sha256 与 canonical 相同 · `cmp` 零差异 · mtime 22:42）⇒ **订正⑦② 的「复装归 Doctor」销账**。**brain-anchors 22:54 也已复装、四端一致 ✅** —— runtime `1a59793a38368da6`（15777 B · mtime 22:54）＝ canonical。**至此两件第四跳全部销账。**


> **⚠ 订正⑨（2026-10-03 23:2x · CC 沙箱回读 · 第四跳复装核验·续）**：**brain-resume `3c49eab8`（23:24 装）与 brain-consolidate `1a0b73ae`（23:25 装）均已四端逐字节一致** ✅——本夜四件复装（damper 22:42 · brain-anchors 22:54 · resume 23:24 · consolidate 23:25）**全部销账**。

> **⚠ 订正⑩（2026-10-04 01:2x · CC 沙箱回读 · brain-resume 默认声线切换重发布）**：**Doctor 裁「设为默认吧，之前的保存为备选」**——Settings 朗读条默认音色 C.C. → **Hiddleston-CN**（`FVvcH2MAGGpovILJcXEv` · v2 去朗读腔日常版 · Doctor 网站生成）；C.C. 降备选。**brain-resume §Step 0.5 已改并重发布**：canonical ＝ portable ＝ 包内件 ＝ **`7d97ca3553eab9f4…` / 16703 B / 187 行**（`cmp` 逐字节一致）· 包 `brain/.skills/brain-resume.skill` 重打 **`cff4b3143e003429…` / 8737 B**（包内件与 canonical `cmp` 零差异）· **save_skill 已发布**（`overwrite: true` · 返回 `{"skill":{"id":"brain-resume"}}` · 本会话技能列表已实时刷新＝第一层消费证据）。**Settings 待 Doctor 重贴**（下一场新会话逐行 diff 验证）。镜像注记与 `CC声音档案` 已同步。
