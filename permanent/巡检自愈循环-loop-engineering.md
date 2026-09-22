---
title: 巡检治理 · 四执行面快照与自愈循环
abstract: "定时任务巡检治理四合一现状版（2026-09-17 Doctor 批 consolidate 方案②）：Mac 侧四执行面快照+git diff 变更检测 · 周班悖论两层解法 · 自愈循环 L0-L3（白名单/审计层/永不自动清单）· 任务清单「不变」架构与铁律 · 诊断卡模板附录。历史底稿：定时任务巡检机制_v1_pre-migration · 定时任务清单_v1_pre-migration · 巡检诊断卡模板_v1_pre-migration · 本文件_v2_pre-migration"
tags: [巡检, 自愈循环, 治理, 定时任务, brain]
created: 2026-08-29
updated: 2026-09-17
status: active
type: permanent
related: [通用教训, Doctor协作偏好, _scheduler_snapshot]
---

# 巡检治理 · 四执行面快照与自愈循环

> **一句话**：把「定时任务现状」从靠记忆和日志拼，改成一条命令拉；把「谁改了什么」交给 `git diff`；把「坏了谁修」交给预注册白名单自愈循环——修什么、怎么修，永远以机器证据为验收。
>
> **⚠ 覆盖边界（先读这条）**：本机制只覆盖 **Doctor 的 Mac**。已知至少还有第五个执行面：**DVA 的 fuxi Windows 侧**（`E:\AI\DVA\ops\`——refill/采集/分析/轮巡健康告警，有独立 failure/log/summaries 目录与自己的告警节奏）。脚本完全够不到它（跨机器）。一个声称覆盖全面的巡检机制，若自己有未声明的盲区，比没有机制更危险。凡说「定时任务都查过了」，一律补一句「Mac 侧」。
>
> **合并史**：2026-09-17 由四件合并（Doctor 批）——[[定时任务巡检机制]]（四执行面快照 · 2026-08-02 立）+ 本文件 v2（自愈循环 · 2026-08-29 批准）+ [[定时任务清单]]（架构与铁律）+ [[巡检诊断卡模板]]（现为附录 A）。三个原名文件保留为 archived 底稿（顶部有指针行）；四份 `_vN_pre-migration` 副本为合并前原文。

---

## 1 · 病根：为什么要有它（不是需求，是病）

2026-08-01 一天之内，CC 关于定时任务的结论**被推翻三次**：

| CC 说的 | 实际 | CC 的信息来自 |
|---|---|---|
| 「backfill 周一 13:34 验四失败面」 | 班已改 14:30 且不再写库（重构为只读看门狗） | 08-01 凌晨的日志 |
| 「双写者职责未理清」 | zhuzhao 当天已加单写者锁 | 07-31 的日志 |
| 「launchd 有 2 个 job」 | 3 个，第三个（`com.zhuzhao.usclose`）不在任何清单里 | 08-01 凌晨的清单 |

三条都有出处、都自洽——因为它们都是从**日志**拼出来的，而日志是历史。与 2026-07-31 挖出的「Documents 死树」是同一个病的两面：死树＝记了但没人读；本病＝读了，但读到的不是现在。⇒ **根治方向不是让人记得更牢，而是让「现状」可被一条命令拉出来。**

---

## 2 · 快照机制：四执行面

```bash
python3 ~/Documents/Claude/brain/.tools/scheduler_snapshot.py
```

**必须在 Mac 原生跑**——沙箱只挂 `~/Documents`，读不到 live 树与 `~/Library/LaunchAgents/`。

输出两份**固定文件名**：`brain/permanent/_scheduler_snapshot.json`（机器 / git diff）· `_scheduler_snapshot.md`（人）。**只读保证**：除自己这两个输出外不写任何东西；不跑 git 子命令；`launchctl print` 与 `crontab -l` 都是只读查询。

### 四个执行面（均在 Mac）

| 面 | 位置 | 记什么 |
|---|---|---|
| ① Cowork live 树 | `~/Claude's workspace/Scheduled/`（本壳）；Kimi 壳 store 在 `~/Documents/Claude/Scheduled/` | 每班 SKILL mtime/行数/sha12/name/description |
| ② Documents 死树 | `~/Documents/Claude/Scheduled/`（Kimi 主壳时代为 live 位） | 目录数 · 与 live 同名者 · 仅死树有 · 内容分叉 |
| ③ launchd | `ops/*.plist`（源）↔ `~/Library/LaunchAgents/`（装机） | 排期 · 入口程序 · 源↔装机 sha · 实际加载态与 last exit code |
| ④ crontab | `crontab -l` | 是否真为空 |

### 三类一致性（价值所在）

1. **死树 ↔ live 内容分叉**——改了看起来生效、实则没进调度器（07-31 ERR 原型）；
2. **plist 源 ↔ 装机位 sha**——改了源没重装＝死树分叉的 launchd 版；
3. **装机 ↔ 实际加载**（`launchctl print`）——装了文件 ≠ 已加载。

### git diff 就是变更检测器

输出用固定文件名且纳入 git：`python3 scheduler_snapshot.py && git diff permanent/_scheduler_snapshot.json`。**diff 里出现的每一行都是自上次快照以来真实发生的变化**——无论改动来自谁。系统不需要知道是谁改的，只需要能发现变了。基线 commit `e13f414`（2026-08-02）。

### 显式缺口（`_gaps` 字段，静默缺失是这套机制要消灭的东西）

1. **Cowork 班的 cron 表达式**——只有 `list_scheduled_tasks` 这个 MCP 工具给得了，脚本拿不到，快照里 `cron` 恒为 null，**由 CC 调工具回填**。勿把 null 当成「没有 cron」。
2. **`notifyOnCompletion`**——`list_scheduled_tasks` 不返回（2026-07-30 实测），但 `update_scheduled_task` 可以设：读不到 ≠ 设不了。
3. **新鲜度判据的盲区**——快照 `generated_at` 新旧区分不了「谁写的」：手动跑一次脚本快照就新了，双向都会骗人（08-02 两个方向各错一次）。根治已实装（自愈循环 S2）：`_meta` 加 `triggered_by` 字段（scheduled/manual，周班跑必须传 `--triggered-by scheduled`）。判「周班活着没有」以 `list_scheduled_tasks` 的 `lastRunAt` 为准——triggered_by 只作判别辅助，不替代 lastRunAt。

---

## 3 · 输出契约：正常时一个字都不打印

**巡检必然退化**——跑一个月后所有人都会习惯性略过摘要（G-X119「两问的答案总是『核过了、没隐患』就是套话信号」同源）。解药只有一个：**正常时不出声**。

| 模式 | 行为 |
|---|---|
| 默认 | 无异常 → 零输出，exit 0；有异常 → 清单写 stderr，exit 1 |
| `-a` | 连 🟡 级也报 |
| `-v` | 打印四面全摘要（人工排查用） |

**🔴 必须出声**：live 树读不到 · 某班没有 SKILL.md · **班消失了**（对比上次快照；新增不报）· launchd 自有 job 未加载/上次退出码非 0/源↔装机不一致 · 仅死树有的班。
**🟡 默认不出声**：死树内容分叉（已知无害存量）· crontab 非空。第三方 launchd（Google Updater/网盘等）一律不报。

**分工：脚本报「破损」，git 报「变化」**——变化本身不算异常，每次改班脚本都喊一嗓子两周内必被无视。唯一例外「班消失」：git diff 虽能看见，但没人盯着 diff 找减号，误删代价不对等，故脚本自己出声。

---

## 4 · 定期化：周班设计与那个悖论

> **巡检定时任务的东西，自己也是个定时任务。它坏了谁发现？**

一个只依赖自己的巡检器，停摆时完全静默——这正是它要消灭的病。解法两层，缺一不可：

**第一层 · 巡检班自证**：脚本读上次快照 `generated_at`，距今 >8 天则报 🔴「巡检中断过 N 天」。班每周跑，正常间隔 7 天；漏跑后下次自己喊出来。
**第二层 · `/resume` 兜底**：第一层挡不住「永远停摆」。brain-resume Step 0.6 每次 Doctor 开工都查快照新鲜度，不依赖任何定时机制。

⇒ **定时的东西用不定时的东西兜底**，这是唯一能跳出悖论的结构。

### 周班形态（现行 · 2026-08-30 起）

| | |
|---|---|
| 排期 | 周日 20:00 PDT（`0 20 * * 0` · taskId `scheduler-weekly-audit`） |
| 动作 | 跑脚本 → **S3 写后自证**（回读 `generated_at` 比对，不前进即报 🔴）→ 读 `_repair_audit.md` 尾段（存在 🔄 未验行列入异常清单附报）→ 只读报异常 |
| exit 0 | 静默。不通知、不 commit（每周空 commit 会污染 git 历史；班跑没跑由快照 mtime 证明） |
| exit 1 | 通知 Doctor，附 stderr 异常清单 + `_scheduler_snapshot.md` 路径 |
| 不做 | 不自动修、不自动 commit、不碰调度器——**2026-08-29 起按 §5 自愈循环分梯豁免**：白名单内预注册修复动作不受此条约束，白名单外仍 fail-closed 只报告 |

> **⚠ 上表「动作」列在本环境有一步是死代码（2026-09-22 实撞 · 必须知道）**
>
> 班的步骤 1 要求「在 Mac 原生跑巡镖脚本」，但**本壳的定时班跑在沙箱里**——它读不到 `~/Gateway-workspace`（store 保护区）。班按自身 prompt 明文处理：「报『本班无法在当前环境执行』→ 把两段命令原样贴给 Doctor → **干净退出**」。
>
> ⇒ **步骤 2–5（含 S3 写后自证、读 audit、出简报）在本环境走不到**。09-21 那次的班会话实录即如此：零脚本执行、零快照读写、只贴命令退出。
>
> **两条后果**：
> 1. **「班跑没跑」不能由「快照有没有前进」证明**——快照只能由 Doctor 终端带 `--triggered-by scheduled` 手动跑才会前进；`triggered_by=scheduled` 因此**不是「班自动跑过」的证据**，而是「有人按班交接的原文跑了」。F1a/F1b 判据读它时要带上这层理解。
> 2. **⚠ 级异常没有送达口**：班不出简报，而它的系统通知只对 🔴 发。故面③ 的黄条（如「机器当时在睡眠/未运行」「日志落 /tmp 无法判定」）**改由 `brain-resume` Step 0.6 附报**（2026-09-22 Doctor 裁「把 ⚠ 也列进简报」）。修这一支需要改 store 里的班 prompt（走 Doctor 终端 SHA 往返），**尚未做**。

---

## 5 · 自愈循环（L0–L3 + 审计层 · 2026-08-29 Doctor 批准）

**背景**：「只报告不动手」是 2026-08-02 立规时规避 13 条历史失败族（认知失真/静默成功 G-X118/修一漏三 G-X141/一字之差改坏生产/记成功≠真成功 G-X51/正路绿≠负路对 G-X150/修一处漏一处/误报毁告警 G-X122/命令=开关/占位符 G-X134/双轨并存 G-X151/glob 拾取 G-X162/实施者自签 G-X4）的一次性最优解，代价是修复永远等 Doctor。自愈循环目标：**在保留全部门的前提下，把「机器可证、射程限定、可回退」的那部分修复还给循环**。

**悖论第二叉（有写权就变成需要被巡检的东西）靠三条同时成立的约束消解**：

> (a) **写权受限**：只允许执行 §5.2 预注册白名单内修复动作，且只碰「巡检机制自己」的资产。技术性强制靠「授权调用形态」——每个动作写明可用工具与参数形状（如 F3 只允许 `update_scheduled_task` 且只传 description 参数、taskId 必须 exact-pin 字面值），§7 负向测试把越权形态做成非零拒绝；白名单外一律 fail-closed 回「只报告」。射程＝调用形态收敛＋事后留痕，不是结构保证。
> (b) **写必留痕**：每次修复动作写一行 append-only audit log（`brain/permanent/_repair_audit.md`，schema 见 §5.4），含时间戳/触发证据/动作/回退点/验收判据/实施者/状态。audit 经 Doctor commit 后于 git diff 显形；**读侧以文件本体为准，不依赖 git**。
> (c) **留痕必被读——且读有双通道，不与叉一同死**：① 人读通道＝brain-resume Step 0.6 读 audit 尾段并报新鲜度；② 机器读通道＝周班 prompt 读 audit 尾段，存在 🔄 未验行则列入异常清单附报（走 exit 1 通道，不破坏「正常零输出」契约）。

⇒ 修复器的写权不再是隐形权力，而是「每写必留痕、留痕必被双通道读」。**验收判据优先写成「下一次运行自证」的谓词**——修复失败 ⇒ 快照继续过期 ⇒ 触发条件再度成立，**检测即验收**。

### 5.1 L0 · 诊断（永远允许 · 只读 · 先于一切修复）

- 探针集（全部只读）：`list_scheduled_tasks` · 快照 `generated_at` · gitcheck · **G-X51 取证法**（`list_sessions` + `read_transcript` 查班死因）· launchd/crontab 由 Doctor 侧跑（命令贴出，不代跑）。
- 每次诊断落「诊断卡」（模板见附录 A，append-only，时间戳+证据指针+未确诊项清单）。诊断卡须粘贴探针**原始输出块**，禁转述——证据必须可重放。
- **死因未确诊，不进 L2**（G-X141 硬门）。诊断卡判语只允许「确诊/未确诊」二分，不许写「疑似即修」。

### 5.2 L1 · 自愈（白名单 · 幂等 · 可回退）

| 编号 | 动作 | 射程 | 触发 |
|---|---|---|---|
| S1 | 快照刷新：贴一条 Doctor 终端命令重跑 `scheduler_snapshot.py`（沙箱读不到 live 树，此步**永远**走 Doctor 终端） | 快照两文件（脚本自身只读保证） | 快照超期 |
| S2 | 新鲜度判据修正：快照 `_meta` 加 `triggered_by` 字段，脚本侧一行改动（已实装） | scheduler_snapshot.py 一行 | 方案批准后一次性实施 |
| S3 | 周班 prompt「快照写后自证」步：跑完脚本必须回读 `generated_at` 比对，不前进即报 🔴（已实装） | 周班 prompt 一个步骤段 | 方案批准后一次性实施 · 走 Doctor 终端 SHA 往返（F3p） |

### 5.3 L2 · 修复（预注册失败模式表 · 字段级最小 diff · 写后回读）

| 失败模式 | 触发证据（硬） | 修复动作 | 验收判据（机器可验） | 回退 |
|---|---|---|---|---|
| F1a 快照超期**且**周班停摆 | `generated_at`>8天 **且** `lastRunAt`>8天 | 先 read_transcript 查死因（悬挂/权限/零产物）；确诊后才修；修不了（平台层）→ 只报告 | 下次周窗（周日 20:00 PDT ±24h）内 lastRunAt 前进 + 快照刷新 **且 triggered_by=scheduled** | 无写动作，天然可退 |
| F1b 快照超期**但**周班在跑（班内落盘失效） | `generated_at`>8天 **且** `lastRunAt`≤8天 | 诊断写路径（脚本写失败/落错位/G-X118 同款）→ S3 自证步加装（若尚未装）+ 贴 Doctor 命令重跑快照恢复基线 | 下次周班跑后 generated_at 前进 且 triggered_by=scheduled | 无沙箱写动作 |
| F2 班消失 | 快照 diff 出现减号 | 🔴 **只报告，永不自动重建**（建班=权限扩张） | Doctor 裁定 | — |
| F3 description 漂移 | `list_scheduled_tasks` 的 description 与镜像 SKILL.md frontmatter description 比对不一致（diff 落诊断卡） | `update_scheduled_task` **仅传 description 参数**、taskId exact-pin；pre-image＝list 逐字返回入 audit | post-image＝再 list 逐字比对一致 | 再 update 回 pre-image 原值 |
| F3p prompt 本体改动（含 S3 步插入） | 方案批准/设计变更 | **一律 Doctor 终端**：取回 store SKILL.md 全文+SHA → 沙箱改 → 贴回或 Doctor 执行 → 再取回+SHA 复验（G-X162 判据④既定路径）。**沙箱禁传 prompt 参数**（读不到本体=盲写，G-X118+一字之差族合体） | 取回 SHA 与贴回内容逐字比对 | Doctor 侧持原文可回退 |
| F4 launchd 源↔装机不一致 | 快照 🔴 | 只报告+贴命令（沙箱碰不到装机位） | Doctor 执行 | — |
| F5 死树分叉 | 快照 🟡 | 不动（已知无害存量，08-02 已判） | 快照持续亮灯 | — |

### 5.4 L3 · 验收（实施与验收分权）+ 审计层

- **修复完成 ≠ 修好**。验收只认机器证据，优先「下一次运行自证」谓词：`lastRunAt` 前进到预期窗口 / `generated_at` 前进且 triggered_by=scheduled（手动跑假绿灯是 08-02 实测双向都犯过的病）/ audit 行 schema 合规 / 回读比对逐字一致。
- F3/F3p 属中风险（动 live store 班）：由**未参与实施的 subagent** 独立复验（授权内可自主派）；复验报告仅作背书，不取得 ✓ 权。
- audit 行状态只允许 🔄/⚠️；✅ 只由 Doctor 或指定独立验收方落（G-X4）。**Doctor 08-29 授权「定时任务列入可代签代勾类别」指 TODO 销项，不覆盖 audit 行的 ✅ 落签**。
- `_repair_audit.md`：append-only（**用 Edit 尾段追加，不用 Write 覆写**——G-X107）。每行 schema（六元组）：`ts`(ISO) / `trigger`(硬证据) / `action`(动作+工具名+参数形状) / `rollback`(回退点) / `acceptance`(判据，必须含可跑命令或工具名) / `actor`(实施者) / `status`(🔄/⚠️/✅)。test_repair_loop.py 含 audit 行解析器，缺字段/空字段即报。
- audit 经 Doctor commit 后于 git diff 显形（G-X154：显形须等 commit，读侧以文件本体为准）——修复器的行为是**另一个被巡检对象**，叉二由此闭环。

---

## 6 · 永不自动清单（负向边界）

1. 不新建/删除定时班（含 create/delete_scheduled_task）——建班=权限扩张；
2. 不改任何班的 cron 排期（排期变更=调度权扩张）；
3. 不 enable/disable 任何班（状态变更除外：Doctor 已裁定的具体暂停/恢复场景）；
4. 不动 launchd 装机位、不 commit/push（沙箱 git 禁令照旧）；
5. **沙箱不传 prompt 参数**（读不到 store 本体=盲写）——prompt 任何改动一律 Doctor 终端 SHA 往返；「字段级 diff」仅在参数级实现（只传 description，不传 prompt）；
6. 不用 glob/日期排序拾取治理资产（G-X162）；
7. 未确诊死因不动手（G-X141）；
8. 修复后不自签「已修好」（G-X4）；
9. 不改告警分级口径（G-X122）；
10. 修复循环自身不新增定时班（它的触发点是 /resume 与周班——用不定时的东西兜底，不许再造一个需要被巡检的新班）。

---

## 7 · 验证方案（负向注入 · 持久化 · test_repair_loop.py）

1. **伪造快照超期** → F1 判定函数必须分臂（lastRunAt 也超期→F1a；新鲜→F1b），且不得误报 F2；
2. **伪造「lastRunAt 新鲜+快照旧」** → 必须判 F1b「班内落盘失效」而非「周班停摆」；
3. **triggered_by 假绿灯回归**：manual 快照不得被读成「周班在跑」，F1a/F1b 验收判据必须含 triggered_by=scheduled；
4. **F3 负向**：update 写错字段（错键/空串）→ 回读比对必须非零报错，audit 必须记录失败；
5. **越权负向（白名单外 fail-closed）**：诊断卡请求 F2/F4/排期变更/新建班 → 循环必须拒绝并回「只报告」；
6. **错靶负向**：F3 对**非周班 taskId** 发起 update → 必须拒绝；携带 prompt/cron/enabled/notifyOnCompletion 任一参数 → 必须拒绝；
7. **audit schema**：解析器对缺字段/空字段/非法状态词必须报错。

正常路径 exit 0 不证明 fail-fast——每条守卫配持久化负向用例。

---

## 8 · 批准文本（Doctor 侧换文 · 已生效 2026-08-29 · 供重贴 Settings 时引用）

> 巡检自愈循环 v2 已获批准。特批例外口径：授权不扩张清单中「调度安装或变更」的禁手，对本循环内预注册动作作如下豁免——仅限 `scheduler-weekly-audit` 一个 taskId，仅 `update_scheduled_task` 的 description 参数（prompt/cron/enabled/notifyOnCompletion 一律不经沙箱，prompt 改动走 Doctor 终端 SHA 往返）；新增/删除班、改排期、启停仍属禁手。修复动作必须落 `brain/permanent/_repair_audit.md` 留痕，验收判据凭机器证据（lastRunAt/generated_at 前进且 triggered_by=scheduled），✅ 落签仍只归 Doctor 或指定独立验收方。

---

## 9 · 任务清单「不变」部分（架构与铁律来由）

> 「会变的」（班数/cron 钟点/SKILL mtime/launchd job 数/死树目录数）以 `_scheduler_snapshot.md` 快照为准，本清单不再记；本节只留「不变的」解释性知识。

### 9.1 存储与机制

- **任务文件**：`~/Claude's workspace/Scheduled/{taskId}/SKILL.md`（本壳 live 树）；Kimi 主壳 store 在 `~/Documents/Claude/Scheduled/`（原「死树」位已复活为 live）。
- **读写边界（2026-08-01 实测订正）**：CC 对 live 树**读侧通**（宿主机 Read/Grep/Glob 直接读全文）、**写侧封死**（Write/Edit 拒、沙箱够不到、补挂被静默拒）——「CC 无法维护任何 live 定时班」收窄为「写侧封死」。只有安装那一步（cp 覆盖）仍必须 Doctor 终端做。写入路径：CC 备件落 staging → Doctor 终端 `.bak` 后 cp → 收尾 diff 确认逐字一致。
- **「光有 SKILL.md ≠ 任务已注册」**：SKILL.md 的 frontmatter 只有 name+description，调度信息（cronExpression/enabled/nextRunAt）在独立的注册表里。切环境后旧文件还在、注册表是空的 → `list` 返回 0，**必须用 `create_scheduled_task` 重建**。
- **jitterSeconds**：平台给每个任务加几分钟确定性偏移分散负载，正常；只要任务间相对顺序不乱即可。
- **cron 用 user 本地时区**（美西 PDT），不是 UTC。`list_scheduled_tasks` 返回的 `cronExpression` 字段是唯一权威——人类可读摘要可能漏（`30 8 * * 3,6` 摘要只显示 Wednesday），别信摘要。
- **prompt 文案「中立语境」规约**：去钟点/时段措辞（「06:xx」「开盘前」「早安」），只留数据逻辑；不显式标注地域。数据逻辑按「前一交易日」+交易日历判断，不绑钟点。代价：侧栏 description 可扫读性下降——折中＝保留「日更/每交易日/周更/月初」相对频率词。

### 9.2 双壳几何（2026-08-02 起 · 用清单前必读）

| | Kimi 壳（主 · 会 fire） | Cowork（备 · 留底牌） |
|---|---|---|
| store | `~/Documents/Claude/Scheduled/` | `~/Claude's workspace/Scheduled/` |
| 状态 | 19 班 enabled | 19 班 disable（回切操作卡 §二） |
| artifact | 本壳 6 个 | 旧 8 个留档 |

回切：rsync 文件覆盖（⚠方向不可反）——操作卡 `references/scheduled-live-mirror/回切操作卡.md`。`_DEPRECATED_Scheduled_20260802` 是 07-01 的 11 班死账，别与 19 班混淆。

### 9.3 依赖链顺序与铁律来由（美西本地 · jitter 后相对顺序仍保持）

- 依赖链：行情 01:30（market-data）→ 入库 09:00（recap-ingest）→ 审核 09:30 → 日报 10:00（zhuzhao）→ 看板 11:30（asset-dashboard）。
- **`us-close-backfill` 刻意排在美股收盘（13:00 本地）之后**——zhuzhao(10:00) 出 A 股日报时美股未收盘，其 us_anchor 腿按盘中守卫只能写到前一交易日（**设计如此非 bug：宁可晚一天、绝不编一天**）。补数班收盘后用 `--from=max+1` 补齐，event-attribution-watch(17:40) 直接读库。**不挪 zhuzhao**：挪了打乱 cockpit/看板依赖并延后北京早晨的日报。
- `refresh-risk-daily`(09:00) 与 `recap-ingest`(09:00) 同刻并发，无共享写入目标，jitter 各自偏移；若日后锁竞争再错开。
- **星期漂移待核**：weekday 任务美西周一~五 → 目标时区周二~周六（美西周日无 cron → 目标时区周一清晨无专班）。若要目标每交易日清晨都有班，cron 星期域需纳入周日（待 Doctor 裁）。

### 9.4 Mac 本机 launchd（第二执行面 · 2026-08-01 首次入账）

- **「Mac 侧调度已退役」是错信念**：`crontab -l` 为空，但 launchd 仍在跑——`com.zhuzhao.marketdata` 周一~五 02:30 PDT（9 步，写公共行情库）。查法：`ls ~/Library/LaunchAgents/` · `cat {label}.plist` · `launchctl list | grep 关键字`（PID 为 `-`＝当前未在跑）。
- **顶层程序刻意用 `python3.13` 而非 bash**：launchd 的顶层程序即 TCC（完全磁盘访问）授权主体——用 bash 则主体是未授 FDA 的 bash，写 `~/Documents` 会被拦。新 launchd 班一律沿用此铁律。
- **失败可见性**：任一步非零退出 → 日志标 ❌ 且程序退出码非 0。唯一例外＝`guarantee_ratio` 不并入 ok（东财已知易 ChunkedEncodingError，下游 build_risk_daily 另有 R 陈旧护栏兜底）。
- **与 Cowork zhuzhao 班五表双写**（theme_etf/market_amount/limit_list/intl_index/kr）：INSERT OR REPLACE 幂等数据不会错，但**两个主人等于没有主人**——任一条挂了另一条替它补上，谁都不会发现。理清职责需连 zhuzhao 三路合并一起做，**只记录、不改造**（2026-08-01）。
- `margin_guarantee_ratio` 归属（2026-08-01 Doctor 定案）：并入 launchd 队（与 fetch_margin 同族、同 T+1 节奏、同消费方）；刻意不并回 zhuzhao 班——margin_daily 已有唯一主人（launchd 第 7 步）。

### 9.5 网络与路径

- **gateway/Claude-3p 开放出网**，取数域名开箱即通无需白名单（官方应用才是默认拒绝+逐域名加白）。定时任务沙箱策略理论上可能不同——最稳验证＝对某取数任务点一次「Run now」，既验真实出网又预批工具权限。
- **路径解析**：gateway 平铺挂载不还原 macOS 层级，脚本靠 `parents[N]` 定位兄弟目录会算错——解法＝脚本加 env 后门（有 env 用 env、无则回退，Mac 原生零影响），任务 prompt 补「前置：挂载+路径 env」块（G-X45）。env 表：烛照线 `ZZJY_*`/`MARKET_DATA_DIR`；白泽线 `BAIZE_*`；海螺 `CONCH_DOCUMENTS_ROOT`。

### 9.6 切环境重建 SOP

1. 新环境 `list_scheduled_tasks` 返回空 → 旧任务没带过来；2. 导出旧任务全文（find + cat 各 SKILL.md）；3. 逐个 `create_scheduled_task`（taskId/cron/description/完整 prompt 正文/notifyOnCompletion；ad-hoc 省略 cron）；4. `list` 核对 cronExpression 字段（别信摘要行）；5. 挑一个取数任务「Run now」验出网+预批权限；6. prompt 正文一字不差照搬旧 SKILL.md（规约极细，漏字会跑偏）。

---

## 附录 A · 诊断卡模板（L0 · 每次诊断照此落卡）

> 自愈循环 L0：一切修复前必有诊断卡。诊断卡 append 进本文件尾段（Edit 追加，不 Write 覆写）。判语只允许「确诊/未确诊」二分——未确诊不进 L2（G-X141）。

```markdown
## 诊断卡 {YYYY-MM-DDTHH:MM} · {一句话标题}

- **探针**（粘贴原始输出块，禁转述）：
  - `list_scheduled_tasks` 关键行（taskId/lastRunAt/nextRunAt/enabled）：
  - 快照摘录（generated_at / triggered_by / RED 清单）：
  - 其他探针（gitcheck / read_transcript 死因 / launchd〔Doctor 侧〕）：
- **比对**：{本次实跑 vs 上次基线，逐项}
- **判语**：确诊 / 未确诊（二分，二选一）
- **F 分臂**：F1a / F1b / F2 / F3 / F3p / F4 / F5 / 不触发（白名单外 = 只报告）
- **动作**：{白名单动作编号，或「只报告」}
- **audit 行**：{若触发修复动作，audit 行 ts 与此卡一致}
```

纪律：时间戳用本次会话实跑时间（先对表 G-X100/G-X125）；探针输出块原样粘贴——证据必须可重放，禁「我核过」式转述；未确诊项列入「未确诊清单」等下次探针或 Doctor 输入，不得猜。

---

## 相关

- 脚本：`brain/.tools/scheduler_snapshot.py` · 负向测试：`brain/.tools/test_repair_loop.py`
- 输出：`brain/permanent/_scheduler_snapshot.{json,md}`（固定名 · 纳入 git · 基线 `e13f414`）
- 审计：`brain/permanent/_repair_audit.md`（append-only · 六元组 schema）
- [[定时任务巡检机制]] / [[定时任务清单]] / [[巡检诊断卡模板]]（archived 底稿 · 2026-09-17 合并）
- 周班 prompt 全文：`references/scheduled-live-mirror/live/scheduler-weekly-audit/SKILL.md`（镜像 · 真源在 store）
- [[通用教训]] G-X44/45/51/53/103/107/111/116/117/118/119/122/134/141/150/151/154/162
- 合并执行场：logs/2026-09-17 记忆固化场
