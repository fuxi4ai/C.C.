---
title: 司南 · GOTCHAS（已知坑）
tags: [司南, gotchas]
created: 2026-05-14
updated: 2026-11-14
status: active
type: resource
project: 司南
---

# 司南 · GOTCHAS（已知坑）

> 排查超过一轮的问题都该记录在这里。CC 遇到报错并解决后**立即**回写，无需 Doctor 提示。
> 本文件即权威（原写「实时操作日志在 `Projects/司南/GOTCHAS.md`」，该文件不存在 · 2026-11-05 审计订正）。

## 格式

```
## [ERR-YYYYMMDD-NNN] 简要描述
**状态**: 🔄 待修复/已修待验 / ⚠️ 已知风险；✅ 已修复（**仅由 Doctor 或指定独立验收方落，实施者不得自标**）（⏳ 旧状态词 2026-08-26 迁移专场退役）
**优先级**: 🔴 高 / 🟡 中 / 🟢 低
**触发场景**:
**错误信息**:
**解决方案**:
**预防措施**:
```

---

<!-- 在下方追加新条目 -->

## [ERR-20261104-001] 官方壳 Code 标签与 Cowork 标签是两个执行面，适配卡只按 Cowork 写
**状态**: ✅ 已修复（2026-11-07 未参与实施的审核者 subagent 独立复验 PASS 代签 · 证据：指令卡 L32 已有「〇 · 执行面订正」节、L93 云端启用 22 为独立审核者 list_triggers 实读口径）
**优先级**: 🟡 中
**触发场景**: 2026-11-04 Doctor 在官方订阅的 Code 标签要求核查 Gateway→官方迁移，指令卡的注册表、skill、artifact 步骤均按 Cowork 写。
**错误信息**: Code 标签 `list_scheduled_tasks` 返回 0；`list_artifacts`（claude-artifacts）返回空；工具集无 `update_artifact`、`request_cowork_directory`；工具说明写明任务存于 `~/.claude/scheduled-tasks/`；24 个活班 prompt 中 16 个依赖 Cowork 工具或沙箱路径（镜像关键词扫描，未实跑）。
**解决方案**: Doctor 裁定班与看板留 Cowork；指令卡增「〇 · 执行面订正」节。Cowork 注册表现状仍待该标签实读。
**预防措施**: 切环境核查前先确认执行面（Cowork / Code / Gateway）；不用 Code 标签的注册表读数判定 Cowork；复原清单与沿革须按执行面区分。

## [ERR-20261104-002] 改 MCP config 的顺序给反：指令卡写「改完 ⌘Q 重启」，与已沉淀的「先退出→再改→再启动」冲突
**状态**: ✅ 已修复（2026-11-04 未参与实施的审核者 subagent 独立核验代签 · 签字分轨事务性项）
**优先级**: 🟡 中
**触发场景**: 2026-11-04 官方壳改 `ELEVENLABS_MCP_BASE_PATH`（→ `~/Documents/Claude/临时文件`）+ 补 `ELEVENLABS_MODEL_ID=eleven_v4`。CC 照 `references/scheduled-live-mirror/官方端适配指令卡-2026-11-04.md` 第三步第 3 项（「改完 ⌘Q 完全重启」）给出命令，Doctor 在 app 运行中改了 `~/Library/Application Support/Claude/claude_desktop_config.json`。
**错误信息**: 尚无报错；风险＝运行中的 app 退出时按内存副本回写 config，改动被完整复原（2026-09-23 Claude-3p 壳实证：改后新路径 0 命中、文件回到改前 2588 B）。改后实测落点仍为 `~/Documents` 根（未重启，属预期）。
**解决方案**: 正确顺序＝先 ⌘Q 退出 app → 回读 config（若被复原则重跑改配）→ 再启动 → 新一轮 TTS 实测落点＋播放。指令卡第三步第 3 项须按此序订正。
**预防措施**: 凡改长驻进程持有的配置文件，先退出消费方再改（同族：`海螺姑娘/architecture/决策记录.md` 2026-09-19 条坑 (a)、`permanent/经验库.md` 同族化归「默认先怀疑输入被回写」）；给 Doctor 改配命令前先 grep brain 该配置的既往坑。
**来源**: 2026-11-04 /resume 场（Doctor 指「brain 里找」后回查得出）
**进展（2026-11-04 10:36 PST · 实测）**: 退出后回读官方 config——改动仍在、**本次未复现回写 (a)**（12240B · BASE＝`临时文件` · MODEL_ID＝`eleven_v4`）；重启后 `output_directory="."` 实测落 `~/Documents/Claude/临时文件/`、play_audio 通过 ⇒ BASE＋白名单已切。未定：不传 model_id 时默认模型是否为 eleven_v4（Doctor 听感报「音色不对」，显式 v4 A/B 待 Doctor 回听）。指令卡第三步第 3 项顺序订正仍待做。
**进展（2026-11-04 10:4x PST）**: 显式传 `model_id=eleven_v4` 的 A/B 段 Doctor 回听「没问题」⇒ 音色差异来自默认模型，env `ELEVENLABS_MODEL_ID` 未作默认生效（原因未核；对策＝调用一律显式传 model_id，Settings 本已写明）。指令卡第三步第 3 项已按正确顺序订正并注执行结果；TODO 模式切换条 ⑥ 同步。待未参与实施的审核者独立核验后落签。

## [ERR-20261104-003] 混合方案（云端 14 班 + Gateway 留 10 班）与「两壳只能单开」冲突：官方 app 开着时 Gateway 班不跑
**状态**: ✅ 已修复（2026-11-07 未参与实施的审核者 subagent 独立复验 PASS 代签 · 证据：混合方案已被 Doctor 裁「留官方、推看板班也上云」取代，指令卡 L60 与 TODO.md L48 同载「Gateway 24 班已全停、云端已启用」，余项归 TODO L48）
**优先级**: 🔴 高
**触发场景**: 2026-11-04 迁移完整性检查（/resume 场 · 只读）。指令卡〇c 定「推看板 8 班＋巡检周班＋sessions 盘点留 Gateway」，同时云端 14 班绑本机 Mac、须官方 app 在线（device bridge）。brain 既有铁律「两壳只能单开」（`司南/Gateway-Official适配/Gateway-Official适配.md` 八律 #3、`回切操作卡.md` L45）。
**错误信息（硬证据 · 盘上 mtime 实读 UTC）**: Gateway 班今日产物全部停在 15:08–15:31（＝07:08–07:31 PST，烛阴日志自述「定时触发 07:09 PST，早于 cron 名义 10:00」＝开 app 补跑昨日漏班）：recap 课件入库 15:08 · 课件审核 15:08 · 句芒行情 15:08 · 烛照日报 15:13 · cockpit.db 15:19 · risk-daily.html 15:31。此后 cron 名义 09:00/09:30/10:00/11:00 PT 各班均无追加（日志「同日二次触发追加复核段」未见、mtime 未动）；guanxing Gateway 班（07:30 PT）当日无产物。⇒ 推断 07:3x PST 起 Gateway app 未运行（与官方 app 单开），留 Gateway 的 10 班当日起实际停摆。**单开的成因（app 级互斥 vs 习惯性单开）未核**。
**解决方案**: 待 Doctor 裁（方向性）：①实测两 app 能否同时常开；②若互斥，推看板 8 班需另择落点（如手动推/改看板形态/等平台给定时任务 update_artifact）或回到整壳切换；③回切操作卡补云端触发器回切段（现卡 10-21 版，零云端内容）。
**预防措施**: 混合部署前先核「两边调度器是否能同时在线」；切壳后首日按 cron 名义时刻抽查一班产物 mtime，别只看「班已启用」。另：Doctor 打开 Gateway app 去停班时，app 启动会先补跑漏班（今日 07:0x 实证）——写库类 6 班可能在停之前先补跑一次，与云端双写。
**来源**: 2026-11-04 /resume 场「继续迁移完整性检查」
**进展（2026-11-04 19:35 UTC）**: Doctor 确认两 app 不可能同开（单开成因＝app 级互斥，已核）。Doctor 裁「留官方，推看板班也上云」：推看板 8 班改为云端照跑、推送入待推队列 `brain/.tmp/pending-artifact-push.jsonl`、交互会话补推；云端启用 22（21 定时 + 1 按钮触发）；回切操作卡已补云端段。仍待：Doctor 停 Gateway 24 班、各班首跑核对、scheduler-weekly-audit / sessions-monthly-audit 无云端可行形态（暂停，/resume 兜底）。


## [ERR-20261104-004] 经验索引只扫 brain/{项目}/GOTCHAS.md，漏掉 Projects/ 下的 canonical GOTCHAS，/resume 把开放条目报成 0
**状态**: ✅ 已修复（2026-11-04 Doctor 回复「ok」验收 · CC 代记；独立复验 PASS_WITH_LIMITS，限制见修法与会话报告）
**优先级**: 🟡 中
**触发场景**: 2026-11-04 夜 Code 标签 /resume 后重建经验索引，核对当日新条目时发现。
**硬证据/最小复现**: `.tools/build_experience_index.py` L118 取 `os.path.join(BRAIN, d, "GOTCHAS.md")`。重建后索引总览「白泽大宗：11 条（开放 0）」，`Projects/Financial/白泽大宗/GOTCHAS.md` 实有 12 条 `## [ERR`、状态行 🔄/⚠ 6 条；ERR-20261104-001（哨兵）在索引内命中 0。
**根因**: 生成器按 brain 目录枚举来源，未覆盖 canonical 落在 Projects/ 的项目。
**影响面**: 白泽大宗确认受影响；`Projects/` 下风险日报 3 条、星空 2 条、DVA 2 条、EAL 1 条是否已被 brain 侧覆盖未核。/resume 的「经验召回」会低报开放数。
**修复/建议修法**: 生成器增加 Projects/ 下 canonical GOTCHAS 来源，并处理与 brain 同名件的去重；属行为变更。已实施（首轮独立复验 FAIL 后补全）：生成器增 `PROJECT_SOURCES` 白名单（白泽大宗、白泽观星、风险日报、星空、海螺姑娘、EAL），解析 `[ID]`、`GOTCHA-NNN:`、`G-NNN —`、`- **EAL-… ·**` 四种条目；Projects 来源用 `project_status`（同行有开放词即判开放）；总览分列「开放／未标」；带状态行而未解析的标题写入索引头。DVA 历史副本、烛照九阴指针、PEC、O MY HTML 不纳入并在索引头写明。备份 `.tools/build_experience_index.py.bak_before_projsources_2026-11-04`，测试 `.tools/test_build_experience_index.py`。
**预防门禁**: 重建后看索引头 ⚠ 告警（来源缺失／解析为 0／未解析标题／编号重复），并对拍各来源条目数与索引条数；引用「开放 0」前先核该项目 canonical 位置。
**口径（2026-11-04 Doctor 裁）**: 「待 Doctor 提交、待班首跑」这类残留不算开放，生成器词表不扩；由状态行负责人更新状态行。
**来源**: 2026-11-04 Code 标签会话，实读生成器与两份 GOTCHAS。


## [ERR-20261104-005] 「停用 Gateway→镜像」只改了文档，`scheduler_snapshot.py` 每次运行仍覆盖 live/ 与 artifacts/
**状态**: ✅ 已修复（2026-11-07 未参与实施的审核者 subagent 独立复验 PASS 代签 · 证据：scheduler_snapshot.py L493 MIRROR_ENABLED=False、两镜像函数提前返回，test_scheduler_snapshot_no_mirror.py 实跑 6/6 PASS）
**优先级**: 🔴 高
**触发场景**: 2026-11-04 夜核对适配未闭项。指令卡写明 `live/<班>/SKILL.md` 是云端班正文真源、须停用 Gateway→镜像，并作废了 1.1 的 rsync。
**硬证据/最小复现**: 旧版 `main()` 无条件调用 `mirror_live_tree()`（从 `~/Gateway-workspace/Scheduled` 覆盖 live/，并 unlink Gateway 没有的文件）与 `mirror_artifacts()`。20:50 快照自述「Artifacts：10 个（拷 4）」；工作区 4 个 artifacts/index.html 的 SHA 与 Gateway 全等。`test_scheduler_snapshot_no_mirror.py` 对旧版 5 项 FAIL。
**根因**: 裁定只落到指令卡与 rsync 命令，没有追到同样执行镜像的脚本（影响面未列全，G-X151 族）。
**影响面**: 20:50 那次运行未改动 live/（更新 0 · 移除 0），文件级与 Gateway 全等；更早的运行有没有冲掉未提交改动，无证据。一旦修改 live/，下一次 S1 就会把改动冲掉。README、定时任务清单与周班 prompt 里的 rsync 同样危险：本地文档已改，云端 prompt 须在 Cowork 核改。**停用的代价**：`_artifacts_manifest.txt` 冻结在 11-04 20:50，幽灵检测失效；`eal_gate_check.py` 判据 6 要求盘上文件与 manifest 一致，`render-event-attribution-artifact.mjs --write` 改动镜像后会 FAIL（读码推断，未实跑）；manifest 如何处理归 Cowork 侧（2026-11-04 Doctor：定时任务和 Artifacts 交给 Cowork）。
**修复/建议修法**: 增 `MIRROR_ENABLED=False`，两个镜像函数提前返回；面① 标题注明 Gateway 已冻结；回切卡补恢复步骤。备份 `.tools/scheduler_snapshot.py.bak_before_nomirror_2026-11-04`。
**预防门禁**: `.tools/test_scheduler_snapshot_no_mirror.py`（HOME 指向临时目录）。
**附带发现**: `test_scheduler_snapshot_staleness.py` 在本沙箱新旧版都报失败，因夹具落在 `/tmp` 下被判「日志落 /tmp」，非本次引入（独立审核者换 TMPDIR 后新旧版全过）。
**来源**: 2026-11-04 Code 标签会话。

## [ERR-20261104-006] 「先备份再覆盖」的固定名命令被判定「重跑也无妨」，重跑后旧版备份被冲掉
**状态**: ✅ 已修复（未参与实施的 subagent 独立核验代签 · 2026-11-05 · 判定：PASS_WITH_LIMITS）（2026-11-05 00:41 Doctor 终端已还原备份；实读 SHA-256 前 16 位 `98b4d81eff085d50`、4559 B，与重跑前记录一致；安装位 `860820684dff4a59`、9401 B 未动，与 portable 逐字节一致）
**优先级**: 🟢 低
**触发场景**: 2026-11-04 更新 `~/.claude/CLAUDE.md`。命令为 `cp 安装位 安装位.bak_2026-11-04 && cp portable 安装位`。CC 回报时写「末尾的 cp 重跑也无妨」，Doctor 随后重跑。
**硬证据/最小复现**: 重跑前备份 SHA-256 前 16 位为 `98b4d81eff085d50`（4559 B）；重跑后备份与安装位同为 `860820684dff4a59`（9401 B），mtime 同为 23:41:24。
**根因**: 备份目标是固定文件名，第二次执行时「安装位」已是新版，于是用新版覆盖旧备份。CC 只判断了覆盖安装位这一半是幂等的，漏看备份这一半。
**影响面**: 仅这一个备份文件。旧版内容未丢：`git show 06bb8e8:portable/claude-code/CLAUDE.md` 的哈希与字节数均与旧备份一致。安装位本身正确。
**修复/建议修法**: 从 `06bb8e8` 取回旧版写回备份文件（`~/.claude/` 不在 CC 写入范围，由 Doctor 终端执行）。
**预防门禁**: 给 Doctor 的备份命令用不覆盖写法（`cp -n`）或带时间戳的文件名；声称「可重跑」前，逐段核对命令每一步在第二次执行时的结果。
**来源**: 2026-11-04 Code 标签会话。

## [ERR-20261105-001] 内联型云端班改 prompt 不回写 `live/` 镜像：3 班镜像落后云端（scheduler-weekly-audit 双向分叉）
**状态**: ✅ 已修复（2026-11-05 · 未参与实施的审核者 subagent 独立复核后落签 · 详见下方复核行）
**优先级**: 🟡 中
**触发场景**: 2026-11-05 五维审计（双源漂移维度）：`list_triggers` 实读 24 班云端 prompt，与 `references/scheduled-live-mirror/live/<班>/SKILL.md` 去 frontmatter 逐行 diff。15 个内联型班中 12 班零差异，3 班有差。
**硬证据/最小复现**: ① `market-data-daily-update`：云端步骤 3/6/7 为 11-04 试跑订正（直连 api.tushare.pro、`--db`、`MARKET_DB`/`DOTENV` env），镜像 mtime 10-16 仍写已不存在的 `09-tushare-pro`/`01-scripts`；② `us-close-backfill`：云端「前置〇」已改官方云端口径，镜像仍写 `request_cowork_directory` + `/sessions/*/mnt/烛照九阴`；③ `scheduler-weekly-audit`：云端（updated 11-05T04:41Z）含「0. 云端任务体检」整节 + PushNotification 段，镜像（mtime 11-05 05:46Z，**晚于云端**）无这两段但独有 ERR-20261104-005 引用句——两侧各有对方没有的内容。
**根因**: 引用型 9 班的真源在镜像、改镜像即生效；内联型 15 班的真源在云端 prompt，`update_trigger` 改完没有「回写镜像」这一步（Step 0 系从 `.tmp/scheduler-audit-step0-draft-2026-11-04.md` 草稿贴上云，草稿未并入镜像）。
**影响面**: 镜像是「24 班操作说明（只读参考）」与 Doctor 终端 SHA 往返的基准；失真后按镜像跑必失败（①②），或审计对拍时误判（③）。
**修复/建议修法**: ①② 已于 2026-11-05 以云端实读文本覆盖镜像对应段（备份 `.bak_2026-11-05_auditfix`）。③ 两选项：(a) 以云端为真源覆盖镜像并把 ERR-20261104-005 句并入；(b) 把该班改成引用型（wrapper 指镜像），此后只改镜像——需 `update_trigger`，属调度变更禁手，归 Doctor。
**预防门禁**: 凡 `update_trigger` 改内联型班的 prompt，同一轮必须回写 `live/<班>/SKILL.md` 并跑一次 diff（可复用本次 `/tmp/cmp.py` 思路：去 frontmatter + 去统一前置段后 difflib）；长期解法＝内联型班逐步改引用型，消灭第二真源。
**来源**: 2026-11-05 五维审计（审计员 A 只读报告 + 主会话 `list_triggers` 实读回写）。
**独立复核（2026-11-05 · 未参与实施的审核者 subagent）**: PASS_WITH_LIMITS — 本批 A-D 共 18 项复验：28 份 .bak 齐、diff 无越界、新指向全部在盘、三套测试全绿、镜像两班与云端 prompt 逐段一致、台账 NF==9 且 ⑧⑨⑩⑪→㉒㉓㉔㉕ 无误，17 项 ✓；第 11 项中 3 处「历史叙述路径」被当死链误换致语义反转（`DVA/architecture/决策记录.md` L200 与 `permanent/经验库.md` L473 的孤儿路径 `~/Documents/Claude/Documents/Database/` 本是故意写错的历史实例、现与「多一层 /Claude/」自相矛盾；`白泽大宗/周日工作流-接手指南.md` L122 把现役单一真源 `Database/宏观-大宗商品/business_breakdown.db` 写成「已归档·不再使用」，正确指向应为 `data/archived/business_breakdown.db.项目本地遗留_20260615`），须从同名 .bak 回滚该 3 行；限制：① 镜像比对为逐段目视、非机器 difflib；② 索引总条数实跑 1156（声明 1155，差 1 条疑为本批后他处新增，无基线快照不可归因）；③ DVA 索引仍判 BUG-20260819-001 为 🔄 系 status_of 既有 mark 优先序（🔄 先于 ✅）、非本批回归，但 DVA「开放 4」因此虚高 ≥1；④ 「24 班」计数未逐一复核（list_triggers 现为 26 条含 1 条一次性提醒与 11-05 07:05 新建的 Sessions monthly audit）；⑤ us-close 镜像开头双 frontmatter 为既有、未在本批范围。状态行保持 🔄（③ scheduler-weekly-audit 分叉待 Doctor）。
**复核后处置（2026-11-05 · 实施者）**: 第 11 项 3 处语义反转已处理——`DVA/architecture/决策记录.md` L200 与 `permanent/经验库.md` L473 的故意记录的错位路径从 `.bak_2026-11-05_auditfix` 逐行回滚；`白泽大宗/周日工作流-接手指南.md` L122 改指归档实名 `data/archived/business_breakdown.db.项目本地遗留_20260615`（在盘）。此三处订正由实施者自做，未经第二轮独立复核。
**独立复核 ②（2026-11-05 · 未参与实施的审核者 subagent）**: PASS_WITH_LIMITS — 问答板 12 项执行批（1A·2A·3A·4A·5A·6ABC·7A·8A·9A·10A·11A·12A）逐项实读实跑全 ✓，无 FAIL 项；③ 镜像↔云端对拍 零差异（list_triggers 实取 trig_011UyLtY1qyiTT1YbdJ5Q6Hz prompt · updated_at 2026-11-06T04:49:21Z · 去前置段后与镜像去 frontmatter 正文 112 行逐行 difflib 零差异 · 镜像含「0. 云端任务体检」「PushNotification」「ERR-20261104-005」）；限制：① 12A STL-168 consumer 第 1 项所指 `渊图/architecture/决策记录.md` 在落签后又被 11-05 法案入图批顶部插入 8 行，现 sha256 前16 为 3383cc8f（受理时值 dd2aafc1 经去插入行重算可复现）、所引 L2793 现为 L2801——回执为时点快照、指针已漂；② 12A STL-169 `outcome_observed:true` 偏满：原行 evidence 预告的「Fuxi 回线后冻结体系复跑」尚未发生（仅「加仓侧研究引用」支满足），建议改 null、未改文件；③ 6B 原位残留除 11-04/11-05 命名件外另有 `references/scheduled-live-mirror/official_pre_sync_2026-10-21/**/SKILL.md.bak_*` 9 件（冻结快照目录内、未动）；④ 1A 星空 Projects 指针 frontmatter 含两行 `updated:` 重复键；白泽大宗并入段较 Projects 备份少末尾 1 个空行（strip 后逐字节相等）；⑤ 4A updatedfill 备份实数 58（含 .skills/portable brain-save 两件）非 56；⑥ 2A 云端 prompt 系由 list_triggers 返回 JSON 人工转录入 /tmp 再比，非程序直取。

**追记（2026-11-14 · 同根新形态 · ⚠️ 已知风险）**: 引用型班也会分叉——班 prompt 的「看板推送」覆盖段（2026-11-12 起）取代了正文 Stage 4 的 `update_artifact` 写法，但 `live/<班>/SKILL.md` 正文的旧写法没标注。硬证据：2026-11-14 Code 侧只读镜像即判「白泽周班推不上」，同日 Cowork 补推场也据镜像提出同一疑虑；`RemoteTrigger get trig_01Q6uYGehyN5tpEnazW5ht1U` 实读线上 prompt（updated_at 2026-11-13T05:18Z）才见覆盖段、证伪该判断。镜像正文仍含 `update_artifact` 的班共 8 个（baize-weekly-report 4 处 · zhuzhao-market-fetch-daily-report 3 · event-attribution-watch / longyu-weekly-dualscorer / refresh-asset-dashboard / refresh-risk-daily 各 2 · longyu-equity-thesis-weekly / xboard-daily-repush 各 1，grep 计数）。已处置：baize 镜像 Stage 4 ② 前加「已被云端班规覆盖」注（备份 `_bak/SKILL.md.bak_2026-11-14_stage4-push-note` · Doctor 终端提交 890a147）；其余 7 班未动。预防门禁：判断定时班会怎么跑之前，先 `RemoteTrigger get` 读线上 prompt 的覆盖段，不凭镜像正文下结论；班 prompt 加覆盖段时，同轮在镜像对应步骤前标注。来源：2026-11-14 白泽大宗会话（agents/白泽/logs/2026-11-14-待核验四态与持续性断更修复及看板重渲.md）。

## [NOTE-20261105-001] 状态行写「✅ 已闭 ← 原：🔄 已修待验」会被经验索引判为开放
**状态**: ✅ 已修复（2026-11-07 未参与实施的审核者 subagent 独立复验 PASS_WITH_LIMITS 代签 · 证据：备份 diff 改动面仅限 status_of 切分/2A 文案/30A 射程与 rc 2，自写 8 例 status_of 全对，test_build 23/23、test_parity 9/9，`--name damper` rc 0 / `--name zzz_not_exist` rc 2，DOCS_DIR 重建后司南 1104-001/003/005、龙鱼 0819-001、海螺 0708-001、烛照 1008-003/1104-001、风险 1103-001、DVA 0819-001、EAL G-020/021/024 索引均 ✅；限：默认射程改后 `check_skill_parity.py` 无参跑因 QA/gsap-frontend/handshake-consumer 无 portable 而 rc 1，project_status() 未改仍靠写法甲）
**沿革**: 🔄 已修待验（2026-11-07 Doctor 裁乙·改生成器，实施者自验 6/6，待独立复验）
**优先级**: 🟢 低
**触发场景**: 2026-11-05 五维审计重建索引后，`DVA/GOTCHAS.md` `BUG-20260819-001` 等条正文状态行为「✅ 已闭（2026-11-05 …）← 原：🔄 已修待验（…）」，索引仍判 🔄，DVA「开放 4」虚高 ≥1。
**硬证据/最小复现**: `.tools/build_experience_index.py` `status_of()`：取状态行后按 `("🔄","⚠","✅","⏳","📌")` 顺序逐个 `in` 判，🔄 先命中即返回；`project_status()` 同理（OPEN_TOKENS 先于 CLOSED_TOKENS），注释自述「同一行既有开放词又有闭合词时判开放：宁可多报，不低报」。
**根因**: 生成器把「状态行里出现过的词」当「当前状态」，而落签惯例喜欢在同一行保留旧状态作沿革（「← 原：🔄」）。两者各自合理、合起来必误判。
**影响面**: 所有在状态行内保留旧状态词的 ✅ 条目（DVA 至少 2 条）；/resume Step 1.5 的「开放 N 条」计数。
**修复/建议修法**: 甲 · 写法侧——落签时把旧状态移到下一行「**沿革**:」，状态行只留当前 mark（不改生成器、不改设计初衷）；乙 · 生成器侧——状态行若含「← 原」/「原：」分隔，只取分隔符之前的部分判 mark。二者取一，归 Doctor 裁；本条只登记。
**来源**: 2026-11-05 五维审计（审计员 D 发现 · 独立复核 ① 第 15 项确认非本批回归）。

