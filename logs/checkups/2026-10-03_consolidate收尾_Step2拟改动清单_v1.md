---
title: /consolidate 2026-10-03 场 · 收尾 · Step 2 拟改动清单（v1 · 待 Doctor 批）
tags: [consolidate, Step2, 拟改动清单, 收尾场, 待批]
created: 2026-10-03
updated: 2026-10-03
status: active
type: log
project: 跨项目（brain 基建 · /consolidate 收尾场）
---

# Step 2 拟改动清单 · v1（**待 Doctor 批，未落盘**）

**依据**：`logs/checkups/2026-10-03_consolidate收尾_冲突清单_v1.md`（重建 v1 ＋ 第八章独立复核定稿）。
**门禁**：本清单属 **structural**（改既有记忆资产、影响面含「每轮注入」层）。**未批不动**。批 3（原延后项）本轮**不碰**。
**回退点**：① ② 两层仍在 `…/local-agent-mode-sessions/{acct}/{ws}/memory/memory/`，**不在 brain 仓内、无 git 回退** ⇒ 落盘时**逐件先抄原文到 `brain/backups/`** 作回退点。

---

## 批 5 · 事实性订正（**③ 层可判 · 建议批**）

### 5-A · EAL 迁移家族 —— 7 件 · 路径订正

**③ 判据**：`Database/剑酒青丘/backtest/` 现**只剩 `README.md`**（其正文自陈迁移并写「禁止在此创建 attribution.db」）；生产件实存 `Claude/Projects/Financial/宏观研究体系/EAL/backtest/`；库与 sealed 层在 `Database/宏观研究体系/EAL/`；文档层在 `…/EAL/frameworks/`。

| # | 件 | 改什么（**仅改无日期锚的现状句**） |
|---|---|---|
| 5A-1 | `project_eal_three_layer_layout.md` | desc「生产链在 `Database/剑酒青丘/backtest/`…**建档迁移中**」→ 新址＋「已完成」；**正文四处**：L13 文档层 frameworks 两件 · L14 生产层整段 · L22「Why」的误定位自陈 · L23「How to apply：先认准 `Database/剑酒青丘/backtest/`」 |
| 5A-2 | `reference_jianjiu_layout.md` | L17 末句「EAL 生产链（防写锁+sealed）在 `Database/剑酒青丘/backtest/`」→ 新址 |
| 5A-3 | `reference_zhihui_vv_channel.md` | desc ＋ L11 的「青丘 backtest 库（`Database/剑酒青丘/backtest/`）」→ 新址（其 L14 已正确，不动） |
| 5A-4 | `reference_polygon_fx.md` | L15 库路径 → `Database/宏观研究体系/EAL/attribution.db`（**③ 已只读验：`prices_intraday` 68553 行 · `C:USDJPY` 在表 ✓，规则本体不动、只改路径**） |
| 5A-5 | `project_eal_v3_status.md` | **仅 L15**「v3 落地事实：`Database/剑酒青丘/backtest/eal_v3/` 平铺」（无日期锚）→ 新址。**L23/L33 带日期锚的过去事件记录不动**（可择机加「旧址」标注，非本轮） |
| 5A-6 | `project_eal_threetabs.md` | L16 导出脚本路径 → 新址。**L18 带日期锚的 VV 知会稿路径不动** |
| 5A-7 | `project_eal_naming.md` | L31「md 真源 `brain/剑酒青丘/frameworks/事件归因台账.md`」→ `…/EAL/frameworks/事件归因台账.md`；L57「台账『规则书』当前版本 **v1.3.1**」→ **v2.3** |
| 5A-8 | `project_eal_v3_status.md:35` · `project_eal_threetabs.md:18` | **仓身份/旧址标注**——`Database/剑酒青丘` 有 `.git`、`Database/宏观研究体系/EAL` 无、`Claude/Projects/Financial/宏观研究体系/` 有。**归 5A 附带，标为待定** |

### 5-B · desc 补时点 / 补结论（**6 件**）

| # | 件 | 改什么 |
|---|---|---|
| 5B-1 | `reference_tts_bridge_cowork_only.md` | desc「本壳**无 TTS 工具**…静默跳过属预期」→ 「**已过时**（09-09 B 路线打通）…」——**desc 当前为假、正文为真**（③ 旁证：本日 TTS 产物在盘） |
| 5B-2 | `project_xboard.md` | desc「**artifact 未推**」→ 「已推 09-26T16:09Z ＋ payload 级回读 True」 |
| 5B-3 | `project_eal_v3_status.md` | desc「**VV 验收待（周限额）**」→ 「08-21 Doctor 总签 20 R/N ＋ Gateway 已发布」 |
| 5B-4 | `feedback_subagent_signoff_authorization.md` | desc 08-29 口径 → 补 09-26 默认动作式（**正文已含，仅 desc 落后**） |
| 5B-5 | `reference_brain_guard_path_fragility.md` | desc 补「**已修（10-01）**」时点（desc 现读作仍坏） |
| 5B-6 | `project_tts_bridge_integration.md` · `project_eal_starfield_fix.md` | 两件 desc 补全（前者「进行中」→「全绿」；后者补 adapter 09-16 闭环） |

### 5-C · ② 层其余陈旧（**5 件**）

| # | 件 | 改什么 |
|---|---|---|
| 5C-1 | `reference_local_sessions_storage.md` | 「沙箱够不到此路径」→ 「**可只读直达**（`/sessions/<s>/mnt/.auto-memory/`、`/mnt/uploads/`）；清理仍只能 Doctor 终端」 |
| 5C-2 | `reference_gateway_store.md` | 补 **2026-10-03 Glob 目录级白名单**发现（叶目录可达 / 父目录与根被拒 / 报文为通用作用域语）＋「Edit/Write 现状未核」 |
| 5C-3 | `project_kimi_shell.md:27` | 「该目录对沙箱**永不可读（挂载必拒）**…勿试图读文件」→ 同 5C-2 口径 |
| 5C-4 | `project_dva_refill_state.md` | **仅 desc**（正文 L24 已有 09-30 架构级取代的订正）→ 补「旧自愈链已退役、改增量链」 |
| 5C-5 | `project_dva_finance_arm_fix.md` | desc/正文补终态：③ 已实读 `Projects/DVA/GOTCHAS.md` 状态行「✅ 已修复（Doctor 2026-09-17 /todo 落签小批勾）」 |
| 5C-6 | `exp_system_phase1_status.md` | 「经验索引 v2（**733 条**）」→ 现读 **894 条 · 15 个来源**（「v1.2」**不动**——复核判为绑定 09-04 动作的历史陈述，与 ③ 一致） |
| 5C-7 | `reference_ai_tech_alarm.md:11` | 源文件名 `ai_tech_alarm_snapshot.html` → `ai_tech_alarm_tab.html`（**同一订正的第三处落点**，另两处已改） |
| 5C-8 | `project_yuantu_verify_batch.md` · `project_eal_v3_status.md:23/33` · `project_eal_threetabs.md:18` | 计数/旧址**加时点标注**（「（09-13 当时）」「（旧址）」），低优先、纯防误读 |

### 5-D · ③ 侧新发现（**不在记忆层，但需 Doctor 一句**）

- **`brain/渊图/architecture/系统概览.md` 自身落后**：abstract（L3）与「最后更新」段（L17）仍写 **7120/7719（as-of 10-02）**，而 canonical 与 `_health.json` 均为 **7121/7722（10-03）**；同件另有 5297/5920、7092、6480/7103 等多代计数**无 as-of 标注**并列。**而 ① 偏偏指该件为「计数权威源」**。
- 建议：改 ③ 该件（**同批或另批**）＋ 或在 ① 改为「以 canonical JSON / `_health.json` 现读为准，系统概览为准据之一」。**属 ③ 层改动，请 Doctor 定是否并入本轮。**

### 5-E · 结构项（**供批**）

- **`feedback_bak_folder_convention.md` 补 `MEMORY.md` 索引行**（现为孤儿 ⇒ 不进注入层，G-X118 族）。
- **`brain/渊图/architecture/` 下 `_bak/` 落点违规**：两件 `.bak_save_20261002` ＋ 一件 `系统概览.md.tmp2` 残件就地存放（与 `feedback_bak_folder_convention.md` 所立约定不符）⇒ 建议归位/清理，**归 ③ 层，另行**。

---

## 批 6 · ① 层（**注入层**）修正 —— 逐条前后原文（**每轮在场，必须看清改了哪几个字**）

### 6-1 · K1 终版：`reference_documents_mount_quirks.md` 条 —— 原绝对表述改分路径

- **① 现值（`MEMORY.md` 该件索引行）**：
  > 「Documents 挂载写入怪癖 — **拦截点＝「就地改写 inode」**：`cp`/`>>` 原地改写 EACCES，但**新建+`mv -f` 覆盖可用**（2026-09-19 实测订正）；zip 先出 /tmp 再 cat 覆写；残骸改 _DEPRECATED_；写入有穿透延迟；Doctor 贴回终端输出可能是重复执行的第 N 遍；**探针铁律：永不拿真文件当试验目标**（09-19 事故）」
- **拟改后**：
  > 「Documents 挂载写入怪癖 — **写权限逐文件/逐目录而异、勿一概而论**：`.skills/*/SKILL.md` 就地改写 **❌EACCES**（09-19）· `Database/行业研究/mapping/` python `open(w)` **✅**（09-19）· `Claude/临时文件/` `cat >` **✅**（10-03 实测）；**新建+`mv -f` 覆盖可用**；zip 先出 /tmp 再 cat 覆写；残骸改 _DEPRECATED_；写入有穿透延迟；Doctor 贴回终端输出可能是重复执行的第 N 遍；**探针铁律：永不拿真文件当试验目标**（09-19 事故）」
- **理由**：② 本件 L30 已自陈「同一目录内不同文件写权限不一致」、L33 已给成功反例（mapping/），而 ① 把 `.skills/` 的一例推广成了通则。**② 前段同步加订正标记**（其 L47 已自陈订正过开头那条）。

### 6-2 · B1 禁字：PEC 日本线条

- **① 现值（`MEMORY.md:7`）**：
  > 「…双轨门槛两维；两轨观察位＝**合区解消（②腿）**/ 非核三原则（②③之间）；检验点 2027 春自民党大会」
- **拟改后**：
  > 「…双轨门槛两维；两轨观察位＝**合区解消（② 轨）**/ 非核三原则（②③之间）；检验点 2027 春自民党大会」
- **理由**：Doctor 2026-08-30 立「禁『腿』字术语」。此句系**新写、非引述旧文档**，且**每轮注入在场**。
- **同批**：`MEMORY.md:23` 是**禁令条自身**（标题「禁「腿」字术语」＋ 引述被禁词形）——**建议不动**（属规则本体），请 Doctor 一句。

---

## 批 7 · 报 Doctor 裁（**方向性 · 不并入可自动执行批**）

| # | 事项 | 我方建议 |
|---|---|---|
| **7-1** | **B2 · ② 层禁字迁移（实核 8 件 18 处）**：`project_pec_japan_framework`(5) · `project_bt19_guanxing`(3) · `project_longyu_ds_v3`(3) · `project_zhuzhao_limit_list`(3) · `project_dva_dev19_closure`(1) · `project_pec_g08_revision`(1) · `project_zhuzhao_ust_detail`(1) · `reference_longyu_engine_sandbox`(1) | 禁令自身明文「**若 Doctor 要求迁移既有文档术语，属另一裁定，先 propose-then-confirm，不自行批量改历史文件**」⇒ **本轮不改**。**建议：准，同批做**（措辞统一为「通道/支路/管线」）；三处合规引述（禁令本体 · `reference_shuling_voices` · `project_xboard:26`）不动。 |
| **7-2** | **L6 · `feedback_option_label_recommendation.md:17`「账号 + portable 双写」** | 中置信度：可读作「当时的动作记述」⇒ 也可能不需改。**建议：加一句「（09-19 已校正真源方向，见 `reference_skill_truth`）」**，不改原句。 |
| **7-3** | **批 4（蒸馏 4 候选 ＋ 归档登记）** | **原 4 候选随底稿一并不可恢复**。**建议：不盲补**（盲补易与已落条目重复），改**从本轮自产**提 1 条候选送质量确认——「**输出省流 ≠ 扫描完成**：逐件输出截断 / `grep` 加 `head` 会让「全扫」实际变成抽样，且**自己看不出来**」（本轮实证：因此误报 1 件、漏检 3 件；与 `G-X190` 判别力门同族相邻）。**是否立条、落哪条 G-X，请裁。** |
| **7-4** | **`brain/渊图/architecture/系统概览.md` 自身计数落后**（见 5-D） | 该件被 ① 指为权威源却自己落后（7120/7719 vs 7121/7722）。**建议：改 ③ 该件**（含给多代计数补 as-of 标注），**并另立 GOTCHAS**。**是否并入本轮，请裁。** |
| **7-5** | **本轮新增的 ③ 层改动**（5-E 的 `_bak/` 归位、5-D 的 ③ 改件） | 属 ③ 层（brain 仓内、有 git 回退）⇒ 与 ① ② 两层**回退性质不同**，**建议与记忆层分批**，避免一锅端。 |

---

## 批 8 · 本轮**不做**（附理由，供 Doctor 复核我的克制）

- **`E9` 正文** —— 已被上一场订正（我误报，复核逮出）。
- **`F:\Mac_Backup` / fuxi 侧任何物件** —— 跨机、非本轮记忆冲突面。
- **`Codex/**` 任何写入** —— 越界（VV 域）。
- **`.skills/**`、`portable/**`、`.skill` 包** —— 属**发布链域**，不属「记忆冲突」射程；且 09-26 已裁「不属全局替换射程、另报 Doctor 裁」。
- **批 3（原延后项）** —— 按原裁不动。
- **② 层「全文重写式」整理** —— 属大面积项，另场做（本技能 Step 2 分批建议）。

---

## 附 · 本轮改动计数（**现读现数**，落盘前复核）

| 批 | 件数 | 说明 |
|---|---|---|
| 批 5 | **约 20 件**（含 5-A 8 · 5-B 6 · 5-C 8 · 5-D 1 · 5-E 1，有重叠） | ② 层事实性订正 ＋ 1 件 ③ ＋ 1 条注入行 |
| 批 6 | **2 处**（均为 ① 层） | 逐条前后原文已列 |
| 批 7 | **5 项** | 报裁，不自动执行 |
| 批 8 | **0 件** | 不做 |

**⚠ 落盘后仍须**：由**未参与本轮实施**的 subagent 对**改动本身**再出一轮独立复核（TODO 明文要求），并回读消费端（下一场 `/resume` 的注入块即为 ① 层的真实消费端）。

---

# 执行状态（2026-10-03 夜 · Doctor「全部批准」）

**批 5 ✅ 批 6 ✅ 批 7 ✅（含 7-1 禁字·7-2 L6·7-3 批 4）** 已全部落盘并经独立复核；**批 8** 按原计划不动；**7-4/5-D（渊图侧）** 按 Doctor「专注 consolidate 和 damper」令未动。批 6 的 K1 终版（分路径表述）已落；批 5 的 EAL 家族 7 件、desc 补时点 6 件、其余陈旧 8 件全部落盘。
