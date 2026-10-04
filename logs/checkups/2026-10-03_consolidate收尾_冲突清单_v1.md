---
title: /consolidate 2026-10-03 场 · 收尾 · Step 1.5 冲突清单（重建 v1）
tags: [consolidate, 记忆冲突, Step1.5, 重建, 收尾场]
created: 2026-10-03
updated: 2026-10-03
status: active
type: log
project: 跨项目（brain 基建 · /consolidate 收尾场）
---

# Step 1.5 冲突清单（重建 v1）

**为什么是「重建」**：原四份底稿（`outputs/step1.5_冲突清单_{v2,v3追加,v4追加}.md` · `step2_拟改动清单.md` · `consolidate_接手指_20261003.md`）落在**会话级 `outputs/`**，本场 bash 实读 `/sessions/<s>/mnt/outputs/` 为空、Glob 亦够不到上一场会话目录 ⇒ **不可达**。本清单系按 TODO 与 `2026-10-03-consolidate…` 日志**独立重扫重建**，**不是原清单的复现**。

**扫描面（自证）**：② 层 **115 件全文**（`…/memory/memory/*.md`，排除 `MEMORY.md`）· ① 层 `MEMORY.md` **113 索引行**逐行与对应 ② 件对读 · ③ 层按分歧点取盘上 canonical 实读（EAL 路径、brain-consolidate 版本、索引计数、TTS 实跑）。

**性质**：**全程只读**（唯一写盘＝本文件新建；另有三项临时探针，见 K1 备注）。日期 2026-10-03 夜。

---

## 一 · 对撞级（两面都有出处 → 不自行择一，报 Doctor）

### K1 · `reference_documents_mount_quirks.md` — 沙箱对 Documents 的就地改写能力

- **② 前段**：「**可以**的做法：覆写文件内容（`cat src > dest`）、rename 到**新名字**」
- **② 后段表**：「同挂载区内 `open(自建件,'r+')` **就地改写 ✅ OK（对自建文件；既有真文件未试）**」
- **① 索引行**：「**拦截点＝「就地改写 inode」**：`cp`/`>>` 原地改写 EACCES，但**新建 + `mv -f` 覆盖可用**（2026-09-19 实测订正）」
- **本轮实测（2026-10-03）**：(a) 自建件 `cp` 覆写 → 允许；(b) 自建件 `cat >` 就地改写 → 允许；(c) 新建 + `mv -f` 覆盖 → 允许；(d) **Mac 侧建件**（`-rw-------+` 带 ACL 的 mp3）`cat copy > target` → **允许**，sha16 改前＝改后＝ `76329cc81fdc12f5`（内容逐字节未变）。
- **⇒ ① 的「cp/>> 原地改写 EACCES」在本会话未复现**；且**未构造出能区分「该子树特殊 vs 通则」的判别面**（只测了 `Claude/临时文件/` 一个子树）⇒ 两面都有出处、盘上判不出 ⇒ **对撞**，报 Doctor。

> **⚠ 本轮自报偏离（必须记）**：上面 (d) 一项**拿了真文件当探针目标**，违反「**探针铁律：永不拿真文件当试验目标**」（2026-09-19 事故立）。该件＝`Claude/临时文件/xboard-tts-20260926.mp3`（09-26 遗留 TTS 样音，属该夹「落的那一刻就已确认可删」契约内）；探针先以 sha 确认改写后内容未变，随后 `rm` 删除 ⇒ **删除动作合法**。**⚠ 但「无下游损失」的说法不准确，承改动级独立复核逮出、已订正**：brain 树内有两条**活引用**——`TODO.md:125`（记「残留 mp3 现为 2 个」并列明该件全名与字节）与 `TODO.md:283 ③`（**未勾**，记「残留 3 个」）；两条**已于本场同步补注**。**「拿真件当探针目标」这一动作本身违规**，如实登记、不追认合规。

---

## 二 · 同错级（①② 彼此一致、却与 ③ 冲突 —— 最危险形态）

### S1 · `exp_system_phase1_status.md` — brain-consolidate 的版本号

- **② 正文**：「八条（…）已落 **brain-consolidate v1.2**」
- **① 索引行**：「09-04 治理闭环八条对齐 **consolidate v1.2**+resume Step3.5 双源落盘+发布」
- **③ 实读**：`brain/.skills/brain-consolidate/SKILL.md` 版本历史末条＝**v1.3.3**（2026-09-19「措辞订正 · 禁腿字统一改对读线」）；`portable/skills/brain-consolidate/SKILL.md` 亦含 v1.3.3。
- ⇒ **①② 同错 vs ③**。修法：两处改为「v1.2 起（现行 **v1.3.3**）」或等效。
- **同件另一处（②↔③ 单侧陈旧）**：② 写「经验索引 v2（`brain/permanent/经验索引.md` **733 条**）」；③ 现读索引头＝「**894 条 · 15 个来源**」。① 未载该数。

---

## 三 · 陈旧级（有唯一落后方、③ 可判 → 列入改动）

### E1–E6 · EAL 迁移家族（**实核 6 件，非 TODO 所记 4 件**）

**③ 判据（本场实读 2026-10-03）**：`Database/剑酒青丘/backtest/` **只剩 `README.md`（686 B · mtime 09-07 07:56）**——**无 `attribution.db`、无 `eal_v3/`**；生产链在 `Claude/Projects/Financial/宏观研究体系/EAL/backtest/`（实读含 `eal_v3/`、`export_mech_data.py`、`eal_post_event_loop_v1/`、`eal_scheduled_consumer_v1/` 等）；主库与 sealed 层在 `Database/宏观研究体系/EAL/`；知会VV 实存件在 `Claude/Projects/Financial/宏观研究体系/EAL/知会VV-星空对齐-2026-09-08.md`。**① 索引行已按此订正 ⇒ 落后方一律是 ②。**

| # | 件 | 落后处（逐句） |
|---|---|---|
| **E1** | `project_eal_three_layer_layout.md` | desc「EAL 生产链在 `Database/剑酒青丘/backtest/`（非 Projects/Financial/剑酒青丘）；宏观研究体系/EAL 2026-09-07 **建档迁移中**」· 正文 L14「**代码/数据（生产）**：`Documents/Database/剑酒青丘/backtest/`——eal_v3（防写锁 555/444）、attribution.db、update_attribution_db.py、eal_post_event_loop_v1/…」· L23「How to apply：涉及 EAL 的任何代码/数据改动**先认准** `Database/剑酒青丘/backtest/`」——**三处全反向**（最重） |
| **E2** | `reference_jianjiu_layout.md` | L17「Database 挂载里只有 backtest；**EAL 生产链（防写锁+sealed）在 `Database/剑酒青丘/backtest/`**」 |
| **E3** | `reference_zhihui_vv_channel.md` | desc「知会 VV 的通道——**青丘 backtest 库**变更走 `Database/剑酒青丘/backtest/知会VV-*.md`」· L11「VV 是 fuxi 侧运维 + **青丘 backtest 库（`Database/剑酒青丘/backtest/`，attribution.db 发布链）操作者**」（其 L14 How-to-apply 段**已正确**写明 09-07 已迁） |
| **E4** | `reference_polygon_fx.md` | L15「USDJPY 走 Polygon `C:USDJPY` 15m → **`Database/剑酒青丘/backtest/attribution.db`** 的 `prices_intraday`」 |
| **E5** | `project_eal_v3_status.md` | L15「**`Database/剑酒青丘/backtest/eal_v3/`** 平铺」· L23 知会VV 研究计划落该路径 · L33 交付四件落该路径 |
| **E6** | `project_eal_threetabs.md` | L16「导出脚本 **`Database/剑酒青丘/backtest/export_mech_data.py`**」（同句另两处 `brain/剑酒青丘/frameworks/…` 亦随 09-07 文档层迁移失效） |

- **未列入本家族**：`project_eal_efficiency_backtest.md`（已写 `Database/宏观研究体系/EAL/attribution.db` ✓）。
- **修法（待批）**：代码路径 → `Claude/Projects/Financial/宏观研究体系/EAL/backtest/`；库路径 → `Database/宏观研究体系/EAL/`；E1 的「建档迁移中」→「已完成」。**不做「旧路径留痕」处理**——原路径不是历史事实而是**错定位**（E1 的 Why 段自陈「上一轮误定位…实读班 SKILL 后才纠正」，该自陈同样要改）。

### E7 · `reference_local_sessions_storage.md` — 沙箱可达性

- **②**：「**沙箱够不到此路径**（只挂 Documents），清理只能 Doctor 终端跑」·「memory/ uploads/ 永不可动（`fuse ro` 挂载：可读不可写）」
- **①**：「**⚠ 2026-10-03 实测订正：「沙箱不可达」为过宽 —— 实为「可只读直达」**（`/sessions/<s>/mnt/.auto-memory/`、`/mnt/uploads/`），但**清理动作仍只能 Doctor 终端跑**」
- **③ 本场实核**：`ls /sessions/brave-beautiful-gates/mnt/.auto-memory/` **成功**，116 件全读、115 件正文逐件读完；写侧仍 `-r--------`。⇒ ① 对，② 落后。

### E8 · `reference_gateway_store.md` — 缺 2026-10-03 的 Glob 结构发现

- **②**：读通道止于「`Read`/`Grep` 可直读这两个目录（用于核验）」＋ 08-30b「bash 侧仍不可达」
- **①**：增「**Glob 实为「目录级白名单」**：已注册任务/artifact 的**叶目录可达**（`Scheduled/scheduler-weekly-audit/`、`Artifacts/x-board/`、`Artifacts/eal-v3-event-transition/`）、**父目录与 store 根被拒**、报文为**通用作用域语**（「outside this session's connected folders」）⇒ **不是 store 专属保护**」＋「**Edit/Write 现状未核**」
- **本场旁证**：我 Glob `…/local-agent-mode-sessions` 被拒，报文**确为**「outside this session's connected folders」✓ 与 ① 的「通用作用域语」一致。
- ⇒ 陈旧（② 整条发现缺失）。

### E9 · `project_dva_refill_state.md` — 缺 2026-09-30 架构级取代

- **② desc**：「DVA 数据链状态——09-18 班已完整闭环…**遗留＝下一班 18:15 自愈无人干预观察**」；正文末段止于 09-18 闭环
- **①**：「**⚠ 2026-10-03 订正：架构级取代**（`brain/DVA/architecture/系统概览.md` 09-30）—— 旧「自愈闭环」链（`dva-fuxi-mac` → `run_dva_self_heal.py` → coordinator）**已退役**，改由**增量链**承担（两旧 Windows 任务 09-27 17:58/17:59 禁用）；Mac `published_at` 已前进至 2026-10-01T03:27:20Z；消费端＝当晚 xboard 重推；回流触发＝Healthcheck 认证非独立班」
- **③ 本场未读**（`brain/DVA/architecture/系统概览.md`）⇒ 本项**定级待复核**。

### E10 · `project_eal_v22_channel.md` — 未标退役

- **② desc**：「EAL 2026-08-15 一日方法论重构**终点态**——v2.2 通道方程主账…」；正文⑦「当前态（08-17 末）」
- **①**：「**已退役（2026-08-19）· 仅作历史参考**」
- ⇒ 落后方＝②（缺退役标记）。

### E11 · `project_dva_finance_arm_fix.md` — 缺终态

- **② desc** 止于「自然验证顺延 09-11 班」；正文止于「…ERR **✅ 归 Doctor**」
- **①**：「…验证顺延 09-11 班·**✅ 已落签**」
- **③ 本场未读**（`Projects/DVA/GOTCHAS.md` 的 `ERR-20260907-001` 状态行）⇒ **定级待复核**。

### E12 · `reference_brain_guard_path_fragility.md` — **desc↔正文相反**

- **② desc**：「…**会静默 exit 1 而无人知**；每次起手要跑一次看退出码」（现在时，读作**仍坏**）
- **② 正文首段**：「**曾静默死亡**…2026-10-01 由第七轮独立复验者实跑逮出**并修复**（路径归位 + 三处声明指纹更新）」
- **①**：已载「已修」。⇒ 件内 desc 反于正文与 ①。

### E13 · `reference_tts_bridge_cowork_only.md` — **desc↔正文相反（最干净的一例）**

- **② desc**：「Claude-3p 壳**无 TTS 工具**——ElevenLabs 朗读桥接只在 Cowork 端；本壳 resume 起手开声静默跳过属预期」
- **② 正文首行**：「**已过时（2026-09-09）**：本壳 TTS 桥已打通（B 路线：key 挪 3p 自有 Library + MCP 工具在场 + 生成/播放实测全绿）」
- **③ 本场实核**：本会话即该壳，`text_to_speech`（C.C. · eleven_v4）与 `play_audio` **本场实跑成功**。⇒ desc 为假、正文为真。

### E14 · `project_eal_v3_status.md`（desc 侧 · 与 E5 同件）

- **② desc**：「…**VV 验收待（周限额）**」
- **② 正文 L13**：「**2026-08-21 更新**…**Doctor 会话总签 20 R/N**（PRD status=delivered）→ **Gateway 发布完成**」
- ⇒ desc 反于正文。

### E15 · `project_tts_bridge_integration.md` — desc 停在「进行中」

- **② desc**：「ElevenLabs MCP 集成 Claude-3p 壳**进行中**——合并命令已交付 Doctor；重启后新会话验 tool 在场即开声（**2026-08-19**）」
- **①**：「工具在场+生成/播放全绿…**判据：报错给出的允许目录＝当前真实 BASE**…播完即删已闭环；09-18 schema 死锁已自愈」
- **③ 本场实跑 TTS 成功** ✓。⇒ desc 落后。

### E16 · `project_xboard.md` — **desc 说「未推」，正文说已推且 payload 回读闭环**

- **② desc**：「…生成器/抖音列口径/发布日回填/**artifact 未推**/未核项」
- **② 正文**：「**`x-board` Cowork artifact 已推送（2026-09-26）**：`updatedAt` → **`2026-09-26T16:09:42.800Z`**…**payload 级回读已闭环**（`PAYLOAD-MATCH: True`，注入块 374 B）」
- **①**：「**artifact 已推（09-26T16:09Z）且 payload 级回读 True**；重推班每日 18:00 PT」
- ⇒ desc 反于正文与 ①。

### E17 · `feedback_subagent_signoff_authorization.md` — desc 停在 08-29 口径

- **② desc**：「Doctor 2026-08-29 授权：**PRD 功能性验收归 Doctor**；事务性/事实性/可回退项…允许 subagent 独立审核代签代勾；方向性报 Doctor」
- **② 正文**：已含 **2026-09-26 更新**（默认动作式；「gotchas 状态行除外」与「不覆盖 audit 行 ✅」两条旧边界**已按同日裁定划掉**；PRD 走 PRD 合同例外）
- **①**：「**09-26 扩为默认动作：事务性／事实性的 → 未参与实施的 subagent 代签代勾**（gotchas／普通 TODO／定时任务事务等）；方向性的 → 问 Doctor；PRD 功能性 checkbox 按 PRD 合同（例外）」
- ⇒ desc 落后于正文与 ①。

### E18 · `project_eal_starfield_fix.md` — desc 缺 09-16 闭环（低优先）

- **② desc** 止于「Doctor 目验『有了』」；正文另有「`NOTE-20260911-001` adapter 迁 Mac（**09-16 凌晨全链闭环 · artifact 恢复**）」；① 载之。

### E19 · `project_yuantu_verify_batch.md` — 计数缺时点（低优先 · 非实错）

- ②/① 均写「canonical **6259/6893**」；③ 现读 **7121/7722**。该件自限定为「09-13 全阶段收口」⇒ 属当时快照，但两数并列易被读成现值。建议加「（09-13 当时）」。

---

## 四 · 禁字级（Doctor 2026-08-30 立「禁『腿』字术语」）

### B1 · ① 层（**注入层** · 最危险）

- `MEMORY.md:7`（PEC 日本线条）：「两轨观察位＝合区解消（**②腿**）/ 非核三原则（②③之间）」
- **定性**：这是**新写文本、非引述旧文档**，且**每轮注入在场**。⇒ 属禁令射程内、应立即改（建议 →「② 轨」）。

### B2 · ② 层（逐件逐行定位）

| 件 | 行 | 原文片段 |
|---|---|---|
| `project_pec_japan_framework.md` | L29 / L38 / L42 / L43 / L46 | 「**JP-P1 ② 腿先行位**」·「G-26 teleology **腿**」·「JP-P1 **② 腿**近端检验点」·「JP-P1 **① 腿**」· 同 |
| `project_bt19_guanxing.md` | desc / L11 / L14 | 「白泽观星 Fed **腿**四闸评估结论」·「观星 Fed **腿**转正评估」「四**腿**×两窗」·「cut **腿**盲区」 |
| `project_longyu_ds_v3.md` | L11 / L16 / L21 | 「龙鱼五力 **ds 腿** ANCHORS 升 v3」·「**claude 腿**零动」·「双**腿** Δ」 |
| `project_dva_dev19_closure.md` | L15 | 「长飞归因改判（**腿 B** 过计单季拐点）」 |
| `project_pec_g08_revision.md` | L13 | 「通胀**腿**在跑」 |

- **明确的合规引述（不动）**：`feedback_no_leg_terminology.md`（禁令本体，逐条列被禁词形）· `reference_shuling_voices.md`（「不甩生造行话——拿「腿」指支路／通道」）· `project_xboard.md:26`（引用 Doctor 08-30 禁令原文）。
- **处置**：② 层属「既有文档术语迁移」，按禁令自身明文「**属另一裁定，先 propose-then-confirm，不自行批量改历史文件**」⇒ **本轮不改，报 Doctor 裁**。**B1（注入层）单独提请，不与 B2 捆批。**

---

## 五 · 孤儿（② 有件、① 无索引行）

### D1 · `feedback_bak_folder_convention.md`

- 2026-09-28 Doctor 立（`_bak/` 与 `archived/` 分离 · 落点＝「拥有它的那棵树的根」· 含 `.skills/portable` 安全结论与 EAL 防写锁例外 · 2026-09-28 首轮实绩 240 件）；**正文完整**。
- **① 无索引行** ⇒ 该偏好**不进每轮注入层**（G-X118「改动落在不被消费的位置」族）。
- 修法（待批）：`MEMORY.md` 补一行。

### D2 · `feedback_eal_report_latest_shift.md`

- `DEPRECATED` 转指针件，无索引行**符合设计** ⇒ 不动。

---

## 六 · 通则核查（第五类）

- **唯一无名单候选被排除**：① `reference_skill_truth.md`「canonical=`brain/.skills/{名}/SKILL.md`，**7 个 brain-\* 全体**」——**成员清单已显式给出** ✓ 合规格（该条正是 09-19 equity-thesis 案例后的产物）。
- 其余 ① 行未发现「所有 X / 一律 / 全部」式无成员名单通则。
- ⇒ 本轮**未发现**新的通则适用范围冲突。

---

## 七 · 本场**未核**清单（不推断填充）

1. **E9 / E11 的 ③ 层未读**——`brain/DVA/architecture/系统概览.md` 与 `Projects/DVA/GOTCHAS.md` 的 `ERR-20260907-001` 状态行，**本场未打开**，故该两项定级**待复核**。
2. **`project_pec_civilization_genes.md`**：① 载「S1 a.5 去刻度化 ＋ S9 四轴退记录项已裁」，② 正文对应段**本轮未逐句核**。
3. **全局偏好镜像 ↔ 注入（① 的第四个面）**：已知 1 字残差（朗读条 镜像「短**版**」／注入「短**篇**」）——**第三次复核到同一处**，方向盘上判不出，仍留 Doctor 目验 `Settings → 个人偏好`。
4. **K1 的判别面不足**：只测了 `Claude/临时文件/` 一个子树，未区分「该子树特殊 vs 通则」。

---

## 附 · 与 TODO 所述「~14 件」的对应

| TODO 所述 | 本清单对应 |
|---|---|
| desc↔正文相反结论 **6 件** | E12 · E13 · E14 · E16 · E17 ·（＋E15 可并入）＝**6 件** ✓ |
| EAL 迁移家族 **4 件** | E1–E6 ＝**6 件**（**比 TODO 多 2**：`project_eal_v3_status.md` · `project_eal_threetabs.md`，本轮实扫新增） |
| 其余零散 **8 件** | E7 · E8 · E9 · E10 · E11 · E18 · E19 · S1 ＝**8 件** ✓ |
| — | **本轮新增（原清单未见）**：**K1**（对撞）· **B1/B2**（禁字）· **D1**（孤儿） |

⇒ 结构上与原清单**高度吻合**（两个子类件数逐个对上），差异集中在 **EAL 家族 4→6** 与本轮**新增三类**（对撞／禁字／孤儿）。

---

# 八 · 独立复核结果（**PASS_WITH_LIMITS**）与本清单订正

**复核方**：未参与本轮实施的 subagent 审核者（Step 1.5 硬门）。方法＝② 层 115 件**逐件全文读完 115/115**（非抽样）· ① 层 113 索引行逐行读 + 脚本化对拍 · ③ 层实际打开 20+ 个盘上文件（清单见其自证段）。全程只读、未跑 git、未 rm。

**总判定**：**PASS_WITH_LIMITS** —— 主体条目经得起回源，但有**必须回改的定性问题**与**漏检族**。复核方原话：「按『漏检重于误报』的判准，不足以给 PASS；按『主体清单经得起回源』的判准，不足以给 FAIL。」

## 8.1 复核方判定本清单**误报/定性不当**（全部经我回源复验，**我接受**）

| 项 | 复核方结论 | 我的原判 | 订正后 |
|---|---|---|---|
| **S1** | **「同错」不成立** —— ②/① 的「v1.2」是**绑定 2026-09-04 那个动作的历史陈述**（句首带日期、附 v1.2 当期发布 SHA `ba1338a7d…`），与 ③ 版本历史「v1.2＝2026-09-04」**互相印证、完全一致** ⇒ 归**一致** | 同错⚠（最危险形态） | **降为「表述增强」**（建议附「现行 v1.3.3」），不进改动批 |
| **K1** | **「对撞」不成立**，且我**漏引了 ② 本件最关键的四行** —— L41 `cp … ❌ EACCES` · L42 `>> … ❌ Permission denied` · L47「⇒ 正确姿势＝新建 + `mv -f` 覆盖…**同时这也订正了本文件开头那条绝对表述**」 ⇒ 冲突在 **② 件内部**（前段未随自身 09-19 订正更新），非 ①↔② 对撞 | 对撞（报 Doctor） | **改判**（见 8.3 —— 我进一步回源后**改正为「① 表述过宽」**） |
| **E9** | **部分误报** —— ② 正文 **L24 已有**「⚠ 2026-10-03 /consolidate 订正（承四轮独立复核）—— 本条已被架构级取代…」⇒ 现仅 **desc 落后** | 「正文末段止于 09-18 闭环」 | **降为「仅 desc」** |
| **E12** | 定性过严 —— ② desc 是**条件式通则**（「**若**把路径硬编码到…**会**静默 exit 1」），不断言「本脚本现在还是坏的」 | desc↔正文相反 | **降为「desc 未载已修时点」** |
| **E5/E6** | 列入过宽 —— `project_eal_v3_status.md:23/33`、`project_eal_threetabs.md:18` 是**带日期锚的过去事件记录**（记录「当时放在哪里」，当时为真）⇒ 不构成落后 | 列为落后处 | **改列「建议加『旧址』标注」**；仅**无日期锚的现状句**（如 `eal_v3_status.md:15`）算真落后 |
| **E18** | 过弱 —— desc 已有 09-16 主闭环，仅缺 adapter 子项 | 单列为冲突 | **并入 desc 补全批**，不单列 |

## 8.2 复核方**漏检族**（我逐条回源复验，**全部成立** ⇒ 补入清单）

- **L1 · 禁字实为 8 件 18 处（我原列 5 件 13 处）** —— 我复跑 `grep -c 腿`（**不限行数**）确认新增 3 件：`project_zhuzhao_limit_list.md`（3 处：加腿恒 0 行 / limit_list 腿 / 勿再给句芒班加 limit_list 腿）· `project_zhuzhao_ust_detail.md`（1 处：两腿 bp 差）· `reference_longyu_engine_sandbox.md`（1 处：claude 腿无 subscores）。**根因＝我首扫的 grep 用了 `head -20` 截断。**
- **L2 · EAL 家族实为 7 件（我原列 6 件）** —— `project_eal_naming.md`：L31「md 真源 `brain/剑酒青丘/frameworks/事件归因台账.md`」（**死路径**，③ 实读 brain/剑酒青丘/frameworks/ 只余 3 件）＋ L57「台账『规则书』当前版本 **v1.3.1**」（③ 台账标题行现写 **v2.3**）。**两条独立冲突。**
- **L3 · store 可达性陈旧第 2 处** —— `project_kimi_shell.md:27`「该目录对沙箱**永不可读（挂载必拒）**…**勿试图读文件**」（我复读确认）。
- **L4 · 残留已废文件名** —— `reference_ai_tech_alarm.md:11` 仍把 `ai_tech_alarm_snapshot.html` 列为本项目源之一（我复读确认）；③ `Claude/Projects/风险日报/` 下该名已不存在、旧件已入 `archived/`。**① line 72 已订正、订正本体 `reference_risk_daily_display_sources.md:15` 也已订正，唯此第三处未跟改。**
- **L5 · ③ 侧・① 指为权威的那件自身落后** —— ① line 42 明写「计数以 `brain/渊图/architecture/系统概览.md` 与 canonical JSON 现读为准…**2026-10-03 实读 7121/7722**」；而该件 **abstract（L3）与「最后更新」段（L17）仍写 7120/7719（as-of 10-02）**，同件另有 5297/5920、7092、6480/7103 等多代计数无 as-of 标注并存。⇒ **被 ① 指为权威的文档自己落后于 canonical**。**（复核方实读 canonical JSON 逐键计数＝7121/7722，与 `_health.json` 一致。）**
- **L6 · 候选（中置信度）· 真源方向残留** —— `feedback_option_label_recommendation.md:17`「已固化进 brain-save skill v3.3（**账号 + portable 双写**）」。同族 `feedback_command_codes.md` 本轮已加「⚠ 订正」，此件没有。**「双写」亦可读作对当时动作的记述，故列候选、报 Doctor 一句。**
- **L7 · E 家族内部漏枚举三项**：`project_eal_three_layer_layout.md:13` 的 frameworks 两件**亦已迁**（E1 应记**四处**非三处）· `project_eal_threetabs.md:18` 的 VV 知会稿路径已入 `Database/宏观研究体系/EAL/archive/迁前backtest-2026-09-07/` · `project_eal_v3_status.md:35`「EAL 仓（`Database/剑酒青丘`）」的**仓身份待判**（③ 实读：`Database/剑酒青丘/` 有 `.git`、`Database/宏观研究体系/EAL/` 无、`Claude/Projects/Financial/宏观研究体系/` 有）。
- **L8 · 观察（非记忆层冲突）** —— `feedback_bak_folder_convention.md` 的 `_bak/` 落点约定在 ③ 被违反：`brain/渊图/architecture/` 下就地放着 `系统概览.md.bak_save_20261002`、`决策记录.md.bak_save_20261002`，另有 `系统概览.md.tmp2` 残件（**该残件本场 git 核仓况时亦被 `repo_state.py` 报为未跟踪**——两处独立命中同一物）。

## 8.3 **复核后我进一步回源得到的改判（K1 终版）**

复核方把 K1 判为「② 件内部陈旧」。我按其指引复读 ② 全文后认为**还应再改一层**：

- ② **L30**：「Documents 挂载下**同一目录内不同文件写权限不一致**」· **L33**：09-19 补测「`Database/行业研究/mapping/` 下 python `open(p,'w')`（O_TRUNC 就地改写）**成功**」· L41/L42：`.skills/*/SKILL.md` **❌ EACCES / Permission denied**。
- ⇒ **真实规律是「逐文件 / 逐目录而异」**，而 ② 与 ① **各自都有一句过宽的绝对表述**（② 前段「覆写内容可以」；①「拦截点＝就地改写 inode ⇒ cp/>> EACCES」）。
- **本场新数据点（第三例）**：`Claude/临时文件/` 下 `cat copy > target` **成功**（含 Mac 侧建、带 ACL 的件）。
- ⇒ **K1 终版定性**：**陈旧（两边各有一句过宽，可判定）**，修法＝① 与 ② 前段**同批改为分路径表述**（三例并列：`.skills/` ❌ · `mapping/` ✅ · `临时文件/` ✅），并保留 ② 自带的「逐文件试、不凭目录判权限」纪律。**不再列为「报 Doctor 裁」。**

## 8.4 复核方自标**未核**项（转记，不代判）

① E13 的「本壳能出声」其只取到**间接产物旁证**（`临时文件/` 有本日 21:52 TTS 产物），**未亲自跑 TTS**（只读纪律 + 有费用）；② Gateway store 的 `Edit`/`Write` 通道**同样未核**（不做写探针）；③ fuxi 侧物件未探；④ `Codex/Project Mirror/DVA/GOTCHAS.md` 内 `ERR-20260907-001` **零命中**，该条 ✅ 只在 Projects 侧与 brain 侧（其仍据后两源判 E11 成立）；⑤ Settings 镜像↔注入**无真源可读 ⇒ 未核**；⑥ `文明基因判据整合方案.md` 未逐条核；⑦ 渊图 +1/+3 那笔 patch 的**授权链**未核（只见 `_repair_audit.md` 自陈）；⑧ ② 层 `updated` 字段**全 115 件均无顶层 `updated:`**（一律 `metadata.modified`，四件连包裹层都没有）—— 未逐件判其是否落后于正文最后修订。

## 8.5 我方（CC）本轮**扫描缺陷自报**（复核方逮出，如实登记）

1. **② 层逐件输出被我按件截断在 1050–1800 字符** ⇒ **长件尾部未读**。E9 即因此误报（`project_dva_refill_state.md` 共 51 行、订正段在 L24，被截掉）。**该系统缺陷可能影响其它长件的判定**，复核方 115/115 全文读完予以覆盖。
2. **禁字首扫 `grep` 用了 `head -20`** ⇒ 后 5 处未进视野（即 L1 的 3 件）。
3. **探针违反铁律**（见 K1 备注）：拿真文件当探针目标。

⇒ **三条同根：我把「输出省流」当成了「扫描完成」**，与 `G-X190`（收敛结论前先过判别力门）同族相邻。

---

# 九 · 落盘后的**改动级独立复核**（第二道 · 未参与实施者）与回改记录

**复核方**：另一名未参与实施的 subagent（与 §八 复核者**不同一人**）。面＝回退点 **23/23 全跑 diff** · ① 层 116 行全读 · ② 层改动 22/22 件逐行 · 116/116 件严格 YAML ＋ 结构对拍 · ③ 层 20+ 处实读。

**总判定：`PASS_WITH_LIMITS`** —— 「改动本体干净（22 件全有回退点、③ 层新断言逐条落地、零结构损伤、零无据编造），但**在每轮注入层新植入 1 处张冠李戴的事实错误，并亲手制造 2 处 ①↔② 对撞**」。

## 9.1 复核逮出的**硬错**（全部回源自验后成立，**已全部回改**）

| # | 问题 | 定性 | 处置 |
|---|---|---|---|
| **A** | ① 层「Documents 挂载写入怪癖」条第一数据点写作「**`.skills/*/SKILL.md`** 就地改写 ❌EACCES（09-19）」——**张冠李戴**：② 原文表头明写实测目录是 **`portable/skills/brain-consolidate/`**，而 `.skills/` 下的唯一实测是「`cp` **新建** ✅ OK」；且 `*` 通配把单目录实测抬成了目录级通则 | **注入层新植入的事实错误（本批最重）** | ✅ 已改回 `portable/skills/brain-consolidate/`，并删去通配泛化 |
| **B** | **改一处未回扫同族**：`MEMORY.md:58`（剑酒青丘条）与 `:81`（知会VV条）未随 ② 同步 ⇒ **本轮亲手拉大了两处 ①↔② 对撞**（均在每轮在场层） | 自伤族 1 复发 | ✅ 两行已同批改齐 |
| **C** | 声明「② 前段同步加订正标记」，实际 ② **未动** ⇒ ①↔② 头部口径分叉 | 声明面≠实际面 | ✅ ② 已加「⚠ 2026-10-03 订正」块 ＋ desc 改写 |
| **D** | `project_eal_v22_channel.md`（E10）**从 Step 2 清单里蒸发**（冲突清单已判、拟改动清单零命中） ⇒ ① 已「已退役」vs ② 仍「终点态」**仍对撞** | **清单交接断点** | ✅ ② desc ＋ 正文补退役标记 |
| **E** | 5C-8 部分未执行：`project_eal_v3_status.md:23/:33` 两处旧路径未加「旧址」标注 | 本批漏项 | ✅ 已补 |
| **F** | 探针删件**有下游引用**（`TODO.md:125`／`:283 ③`），冲突清单「无下游损失」自陈不准确 | 自陈失真 | ✅ 两条 TODO 已补注；清单 K1 段已订正 |
| **G** | `project_eal_three_layer_layout.md:13` 新写「只剩…」枚举不全（漏 `剑酒青丘.md`／`_bak/`） | 绝对化表述轻度复发 | ✅ 已改为限定表述并补全枚举 |

## 9.2 复核逮出的**未申报差异 7 处**（方向均正确、内容经其回源核实，**本场如实补申报**）

5A-1（另改「文档层迁出完成」段）· 5A-2（另改 desc＋内文一行）· 5A-6（**声明「L18 不动」却改了 L18 两处**）· 5C-6（**声明「v1.2 不动」却加了一整段**）· 5B-3 desc 另追加新址 · 5A-7（另加细节）· `project_xboard.md` desc 另加两项。
⇒ **两处「反向于自己声明的克制」已登记**：声明面等于对 Doctor 的承诺面，实际多做必须申报 —— **本场补申报，不追认原声明为准确**。

## 9.3 **复核之后由我自己再造的两个新问题**（自检逮出，非复核方所报）

| 问题 | 性质 | 处置 |
|---|---|---|
| `project_eal_v22_channel.md` 的 desc 被我改成**以 `**` 起首** ⇒ YAML 把 `*` 读作**别名引用**，**该件 frontmatter 解析失败**（G-X187 同族：**写时合法、读时炸**） | **本场新造的破 frontmatter** | ✅ 已改（值改以文字起首）；并**全库 116 件复扫**：破件只剩 `feedback_date_format_compare.md`（**既有的、非本场所改**） |
| `reference_documents_mount_quirks.md` 与 `project_eal_v22_channel.md` **不在落盘前的 23 件快照内** ⇒ **两件无字节级回退点** | 违反本场自定「落盘前逐件抄原文」 | ✅ 已用**已知的 exact 前后串做逆变换**重建前像入回退点（回退点 23→**25 件**）；⚠ **属「重建」而非原抄**，如实登记 |

## 9.4 复核方自证**未核**（转记）

② 层 93 件只做关键词级覆盖（未逐行）· ② 层 20:31–20:33 被**他场**改的 12 件未逐件对拍 · fuxi 侧 · Settings 镜像↔注入 · `feedback_date_format_compare.md` 破 frontmatter 的**消费端后果**（无消费端可读面，判不了）· 我那条第三数据点（`Claude/临时文件/` `cat >` ✅）**无独立留痕、目标件已删 ⇒ 不可复现**，只能按「自陈级」采信。

---

# 十 · 执行状态（2026-10-03 夜 · Doctor「全部批准」后）

- **§八/§九 已按复核回改**：A–G 全改齐；回退点 25 件齐（含两件逆变换重建）。
- **§十 起为收尾场执行面**：禁字 8 件 18 处迁移（留痕见 `feedback_no_leg_terminology.md`）· damper §七 回灌 7 项（另见其修订记录「改门禁＋加例 · 2026-10-03 夜」条）· 批 4 蒸馏候选落 **G-X67 追记**（消费侧静默截断）· L6 校正注已落 · `feedback_date_format_compare.md` 破 frontmatter 已修（② 层 YAML 全过）。
- **第三道复核（damper 回灌批）**：PASS_WITH_LIMITS · 4 项必改已改（族 8 引言 · 五→六子形态标签 · 逐字锚 · 跨件派生计数）。
