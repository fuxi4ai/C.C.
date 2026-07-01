---
title: 会话日志 2026-06-30 — gateway 切换善后 · skill 与 artifacts 补迁
tags: [log, gateway迁移, skill, artifact, brain自维护]
created: 2026-06-30
updated: 2026-06-30
status: active
type: log
project: 跨项目（brain 自维护 + 工作环境迁移）
---

# 会话日志 — 2026-06-30

**项目**：跨项目（brain 自维护 + Anthropic 中国封禁后 Doctor 切 gateway 善后）
**主题**：gsap-frontend skill v2 → v2.1 重做 · Cowork frontmatter 范式发现 · 官方工作区 4 个 artifact 跨环境迁移

> 接续同日上午多篇 log 后的 brain 维护流程线；与渊图/烛照九阴线并行。

---

## 完成的工作

### 一、上下文恢复与节点诊断
- `/resume` 读最近 3 篇 log（烛照九阴外部定价栏、离岸 CNH 汇率栏、日报着色+渊图 region 对接），活跃项目识别为烛照九阴 + 渊图。
- Doctor 问"当前是不是走 apiyi"——沙箱内拿不到 Claude 桌面应用 API base_url，给 Doctor `lsof` + `curl --noproxy "*"` 两路诊断；查得**官方 API + 本地 1082 代理 → 193.112.190.220:1460（腾讯云段翻墙节点），apiyi 未参与**。

### 二、回忆装过的 skills
- 通读 `brain/.skills/README.md`、2026-06-14 + 2026-06-26 两篇 log、当前 available_skills 列表，整理 Doctor 历史装过的 skills 三栏（自制 brain 6 个 + 自制 gsap-frontend + 官方/三方一批）。
- 关键发现：v1 `gsap-frontend` 切 gateway 后丢失，因当时**只装在桌面应用、`.skill` 包没落 brain**——这正是后续重做 v2 的导火索。

### 三、《已装 skill 清单》立档
- 新建 `permanent/已装skill清单.md`，A 自制 brain / B 自制其他 / C 官方三方 / D 环境映射 / E 维护偏好 五栏，wikilinks 8 处。
- MEMORY.md 索引补一条 + 新建 auto memory `reference_skill_truth.md`（跨环境真源 + frontmatter 范式 + 备份对策）。

### 四、gsap-frontend v2 重做（基于 greensock/gsap-skills MIT）
- 沙箱 `git clone` 超时——改用 `web_fetch` 拉 README + AGENTS.md + llms.txt 三件官方导航文档，蒸馏出 v2 内容。
- 结构沿用 v1「精简主干 + 5 references」：主干 SKILL.md（core API + timeline + scrolltrigger 速览 + matchMedia + 性能 + 6 条反模式铁律）+ `references/{scrolltrigger,react,frameworks,plugins,utils}.md`。
- 触发词收窄到 GSAP 硬专名（按 Doctor 拍板），SKILL.md 顶部明写"粘性生效——触发后整轮默认 GSAP 模式，不重复判定"。
- 强调 Webflow 收购后 GSAP 全免费事实（不再要 Club 会员/auth token/私有 registry）。
- 在 `/tmp` 打包成 `gsap-frontend.skill`（16484 字节），cp 回 `brain/.skills/gsap-frontend.skill`。

### 五、gsap-frontend v2 → v2.1：Cowork frontmatter 范式根因排查
- v2 包 present_files 贴给 Doctor 后**装不上**，第一版误诊为 references/ 子目录或路径问题。
- 第二轮误指挥 Doctor `cp -r ~/.claude/skills/`——又**死路**（gateway 不读这个目录）。
- Doctor 贴上次会话粘贴的完整对话历史（含同日上午 6 个 brain skill 安装连环战），**真根因明朗**：
  - **Cowork plugin parser 不接受 YAML plain scalar**——`name:` `description:` 值必须用 `"..."` 双引号包裹，description 内部所有 `"` 必须转义为 `\"`，否则报 `SKILL.md frontmatter missing name or description`。
  - **Cowork/Claude-3p 装 skill 走 Settings 入口（plugin 体系）**——不读 `~/Library/Application Support/Claude-3p/skills/`、也不读 `~/.claude/skills/`，手动塞这两条都是死路。
- 改 `brain/.skills/gsap-frontend/SKILL.md` frontmatter 为 Cowork 范式 → `/tmp` 重打包 → cp 回 brain（v2.1，16491 字节）→ Doctor 从 Settings 装上 ✅。

### 六、Cowork frontmatter 范式发现的三处固化
- `permanent/已装skill清单.md` D 栏校正（之前误标 gateway 路径为 `~/.claude/skills/`）+ E 栏新增第 4 条"Cowork frontmatter 范式硬约束"。
- `permanent/通用教训.md` 接 G-X42 后立 **G-X43**（双星 ★★ · 2026-06-30）：完整记录症状、根因、frontmatter 范式、装 skill 走哪条路、与 G-X34 同族。
- Auto memory `reference_skill_truth.md` 大改重写（跨环境矩阵 + frontmatter 范式 + 备份对策）。

### 七、协作偏好新条款（Doctor 明示）
- `permanent/Doctor协作偏好.md`「更新 skill 后打包给 Doctor 直接安装覆盖」段下方加对偶条「gateway 模式下交付 skill 必附 `open -R` 命令」（present_files 卡片不弹"Save skill"按钮，Doctor 要自己去 Settings 装，`open -R` 帮他一键 Finder 定位文件）。
- Auto memory 同步新建 `feedback_skill_delivery_gateway.md`。

### 八、官方工作区 4 个 artifact 跨环境迁移
- 探查官方 Claude 应用 `~/Library/Application Support/Claude/local-agent-mode-sessions/{wsId}/{acctId}/`：
  - `artifacts.json` manifest 4 条 artifact（**真正注册数**，非 167 个 .html 中间产物）
  - manifest 字段：id / name / description / createdAt / updatedAt / isStarred / versions[]（时间戳数组）/ createdBySessionId / lastModifiedBySessionId
  - **无 path 字段**——artifact 真身在 Chromium Partition `Partitions/cowork-artifact-{wsId}-{acctId}/Local Storage`（LevelDB），不是文件。Partition 总体积 6.8M。
- 4 个 artifact 清单：⭐ `zhuzhao-jiuyin-daily`、⭐ `global-asset-inventory`、`baize-weekly-dashboard`、`yuantu-starry-skies`。
- 迁移方案 A（盲试）：
  1. 拷 `artifacts.json` → Claude-3p workspace 目录（`workspaceId=27a35443-…`、`accountId=00000000-…001`）
  2. 拷整个 Partition → 改目录名为新 `{wsId}-{acctId}`
  3. 重启 Claude-3p 验证
- Doctor 终端命令跑通，partition 6.8M 体积对得上，4 个 id 在新 manifest 里全部识别。**待重启验证 Local Storage origin 是否能正常读到内容**——风险点：LevelDB 内可能存了旧 workspaceId 作为 origin 命名空间，改目录名后访问会落到新 origin、可能读不到旧数据。

---

## 做出的决策

| 决策 | 原因 | 影响 |
|------|------|------|
| gsap-frontend v2 触发词收窄到 GSAP 硬专名 | Doctor 拍板「GSAP 触发，触发后整轮默认 GSAP，不需要再触发」——避免抢 frontend-design/emil/impeccable 的戏 | SKILL.md 顶部明写"粘性生效"段；纯效果描述（"加个淡入"）让给其他前端 skill |
| Cowork 自制 skill 的 SKILL.md frontmatter 一律按"双引号+转义"范式写 | Cowork plugin parser 不接受 YAML plain scalar（即便 YAML 1.2 合法）；过去 6 个 brain skill 全踩过、本次 gsap-frontend 又踩 | 立 G-X43 + 已装skill清单 E.4；所有自制 skill 一开始就按范式写 |
| gateway 模式交付 skill 必附 `open -R` 命令 | present_files 卡片不弹 Save skill，Doctor 必须去 Settings 装；`open -R` 比手动翻路径快 | Doctor协作偏好对偶条 + auto memory feedback 条；今后所有 gateway 下 .skill 交付一律 present_files + open -R 并行 |
| artifact 迁移先盲试方案 A（整盘搬+改目录名）而非方案 B（解 LevelDB 重注册） | 方案 A 30 秒可完工、失败成本低（Claude-3p 无 artifact 可丢、有备份）；方案 B 要破 Chromium LevelDB 格式、versions 历史会丢 | partition 已 cp 到 Claude-3p 改新 ID 目录、artifacts.json 已对位；待 Doctor Quit+重开验证 |
| /resume 阶段不读所有项目 architecture，只读最近 3 篇 log 出摘要 | brain-resume skill 范式规定；项目 architecture 按"何时深入"触发再加载，避免一次性灌爆上下文 | 本次接手快、精准（识别活跃项目=烛照九阴+渊图，不误读其他项目） |

---

## 遗留问题 / 待办

- [ ] **artifact 迁移验证**：Doctor Cmd+Q 完全退出 Claude-3p → 重开 + 新会话 → 用 `mcp__cowork__list_artifacts` 验证 4 个 artifact 都被识别、点开能正常渲染。
  - ✅ 列出且能渲染 → 方案 A 完胜，迁移完成
  - 列出但点开空白/报错 → Local Storage origin 卡死，需走方案 B（解 LevelDB 抽 HTML 重注册）
  - 完全列不出 → manifest 路径/格式有差异，需再查
- [ ] **Vault 收尾**（上次会话末尾遗留）：6 个 brain skill 从 `Vault/brain/` → `Vault/archived/brain/`、删两个 `_backup_20260630*`、更新 `SKILLS_MANIFEST.md`（删 APIYI 警告 + brain skill 从 1 个改到 6 个）。本次问过 Doctor 一次未明确批，并案与否待复定。
- [ ] **`gsap-frontend` 评测仍未跑**：v2.1 沿用 v1 哲学「先用着」；若实际用着触发不准 / reference 切分别扭，回收触发词 / 配 2-3 个测试 prompt 再跑评测。
- [ ] **artifact 迁移方案 A 验证结果固化**：成功 → 写成"已验证"经验 + 跨环境迁移 SOP；失败 → 写成 GOTCHAS + 启动方案 B。

---

## 相关笔记

- [[已装skill清单]]（本次新立）
- [[Doctor协作偏好]]（新增 gateway open -R 对偶条）
- [[通用教训]] G-X43（Cowork frontmatter 范式硬约束）
- [[brain-anchors]] · [[brain-save]] · [[brain-consolidate]]（已确认装在 Claude-3p）
- logs/2026-06-26-gsap-frontend-skill制作.md（v1 制作历程，本次 v2/v2.1 的前传）
- logs/2026-06-14-brain-save升级与skill打包偏好.md（"必打 .skill" 偏好出处）
- 上次会话粘贴的完整对话历史（Cowork frontmatter 根因发现的关键事件）
