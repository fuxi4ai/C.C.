---
title: 会话日志 2026-06-26 — GOTCHAS 消化与看板级联归零·海螺纳入 git
tags: [log, 渊图, DVA, 海螺姑娘]
created: 2026-06-26
updated: 2026-06-26
status: active
type: log
project: 跨项目（渊图 / DVA / 海螺姑娘）
---

# 会话日志 — 2026-06-26

**项目**：跨项目（渊图 / DVA / 海螺姑娘）
**主题**：渊图 GOTCHAS 消化四条翻 ✅ + 海螺看板 gotchas 计数级联归零 + 海螺姑娘纳入版本控制

---

## 完成的工作

- **渊图 GOTCHAS 消化四条翻 ✅**（均核 canonical / git 实况坐实，非盲信注释）：
  - `ERR-20260608-003`（provenance）：第②步 forward cite 指纹 06-25 已用 Route A 实装（kg_ingest `cite_nodes` 槽 + 单测 3/3），原拟「另立高风险 PRD」被更轻的 Route A 取代 → ✅；残留仅历史 207 孤儿回填，降级数据卫生 followup。
  - `BACKLOG-20260624-001`（剂泰 bio 子图剔除）：06-25 已 apply commit `9e9a259`（节点 2713→2699、边 3260→3246）→ ✅。
  - `FIX-20260616-001`（盛科去重）：核 canonical 实况 `company_CenturyCore` 已不在、`company_Centec` 保留挂全 10 节点边系 → 去重已落盘 → ✅。
  - `ERR-20260602-001` 子项「Shengyi_PCB 提案待apply」：核 canonical `Shengyi_PCB`/`ShengyiElectronics` 皆不在，现 `company_Shengyidianzi`（生益电子）+`company_VictoryGiant`（胜宏）独立并存，FIX-20260619-001 拆分已落地 → ✅。
  - 顶部注释补 2026-06-25 一行；其余 grep 命中的「根治待办」均为已 ✅ 结案条目里留档原始诊断，按 G-X12 不算待办，未动。
- **海螺看板 gotchas 计数级联归零**：`data/asset_manifest.json` 渊图 1→0、DVA 2→0；重建 `asset-dashboard.html` 后验证内嵌 manifest 14 节点 gotchas 全 0（告警不渲染）。
  - 纠错：验证指标 `grep "错题本积压"` 恒为 8（该串在 JS 模板 `ccPrompt` 内，与数据无关）；正确指标是数内嵌 manifest `gotchas>0` 节点数。
- **DVA 计数口径裁定 + 索引对齐**：核权威库 `Projects/DVA/GOTCHAS.md`（48 条），实况＝0 条 actionable 🔄 + 2 条 ⚠️（RISK-20260617-001 已接受 / INFRA-20260618-003 won't-fix）。Doctor 定口径「actionable-only」→ DVA 计数 2→0；`brain/DVA/GOTCHAS.md` 索引把 `BUG-20260505-003` 🔄→✅ 对齐权威库（索引滞后纠偏）。
- **渊图 / brain 两仓确认早已落盘**：终端 git 报错系我命令路径写错（脚本真实在 `consumers/龙鱼五力/` 非根）+ 部分早期会话已提交；四目标文件 git 全干净。brain `f1c2387` 收 DVA 索引那一处新改动。
- **海螺姑娘纳入版本控制**：写最小 `.gitignore`（仅挡 `__pycache__`/`*.py[cod]`/`.DS_Store`/`*.tmp`），git init + 首提交 + 推 `github.com/fuxi4ai/Conch-Lady`（Doctor 终端跑，已 done）。

## 做出的决策

| 决策 | 原因 | 影响 |
|------|------|------|
| GOTCHAS 翻 ✅ 前必核 canonical/git 实况 | 注释/状态行可能滞后；翻牌只为对齐库内实况，避免误伤或虚标 | 四条均逐一坐实再翻 |
| ERR-003 把「机制坑」判 ✅、「历史回填」单列非坑 followup | 机制已补且有单测；回填是数据卫生另一道题，混一起则永远翻不了身 | 跳出「翻/不翻」二元 |
| DVA 计数口径＝actionable-only（⚠️ 已接受/won't-fix 不计积压） | gotchas 字段喂「需复盘消化」提示；⚠️ 已拍板不修、无可消化 | DVA 2→0，与渊图口径一致 |
| 海螺看板重建命令交 Mac 终端跑（不沙箱跑） | 脚本用 `PROJ.parents[2]` 推 `~/Documents` 读库 health_file，沙箱挂载路径会解析错、丢数据库卡健康注入 | build 脚本路径假设在沙箱下失效，须真机跑 |
| 海螺姑娘首提交走最小 ignore、保留 .bak/.skill/历史 | 首提交是把 git 前历史一次性纳入，排除内容反丢历史，合可逆优先 | 日后想瘦身随时 ignore + `git rm --cached` |

## 遗留问题 / 待办

- [ ] ERR-003 历史 207 孤儿 provenance 回填（按 06-25 计划搁置：先观察新 forward cite 机制召回质量再定脚本，连带 72 篇 None-source 数据卫生）
- [ ] brain 仓另有与本次无关的未提交项：`logs/checkpoints/2026-06-25_*_PRD.md`（两处改动）+ `agents/烛阴/logs/2026-06-25-受益标的六维分对齐.md`（未跟踪）——Doctor 自行决定是否提交
- [ ] 渊图 monorepo 未跟踪的 06-25 龙鱼五力跑批报告产物（`consumers/龙鱼五力/reports/five_forces_data_*` / `llm_score_*`）是否入库——另议

## 相关笔记

- [[渊图]] · [[DVA]] · [[海螺姑娘]] · [[Doctor协作偏好]] · [[通用教训]]
