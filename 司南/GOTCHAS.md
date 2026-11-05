---
title: 司南 · GOTCHAS（已知坑）
tags: [司南, gotchas]
created: 2026-05-14
updated: 2026-05-14
status: active
type: resource
project: 司南
---

# 司南 · GOTCHAS（已知坑）

> 排查超过一轮的问题都该记录在这里。CC 遇到报错并解决后**立即**回写，无需 Doctor 提示。
> 实时操作日志写在项目目录的 `Projects/司南/GOTCHAS.md`；这里是沉淀+索引。

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
**状态**: 🔄 待修复/已修待验
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
**状态**: ⚠️ 已知风险
**优先级**: 🔴 高
**触发场景**: 2026-11-04 迁移完整性检查（/resume 场 · 只读）。指令卡〇c 定「推看板 8 班＋巡检周班＋sessions 盘点留 Gateway」，同时云端 14 班绑本机 Mac、须官方 app 在线（device bridge）。brain 既有铁律「两壳只能单开」（`司南/Gateway-Official适配/Gateway-Official适配.md` 八律 #3、`回切操作卡.md` L45）。
**错误信息（硬证据 · 盘上 mtime 实读 UTC）**: Gateway 班今日产物全部停在 15:08–15:31（＝07:08–07:31 PST，烛阴日志自述「定时触发 07:09 PST，早于 cron 名义 10:00」＝开 app 补跑昨日漏班）：recap 课件入库 15:08 · 课件审核 15:08 · 句芒行情 15:08 · 烛照日报 15:13 · cockpit.db 15:19 · risk-daily.html 15:31。此后 cron 名义 09:00/09:30/10:00/11:00 PT 各班均无追加（日志「同日二次触发追加复核段」未见、mtime 未动）；guanxing Gateway 班（07:30 PT）当日无产物。⇒ 推断 07:3x PST 起 Gateway app 未运行（与官方 app 单开），留 Gateway 的 10 班当日起实际停摆。**单开的成因（app 级互斥 vs 习惯性单开）未核**。
**解决方案**: 待 Doctor 裁（方向性）：①实测两 app 能否同时常开；②若互斥，推看板 8 班需另择落点（如手动推/改看板形态/等平台给定时任务 update_artifact）或回到整壳切换；③回切操作卡补云端触发器回切段（现卡 10-21 版，零云端内容）。
**预防措施**: 混合部署前先核「两边调度器是否能同时在线」；切壳后首日按 cron 名义时刻抽查一班产物 mtime，别只看「班已启用」。另：Doctor 打开 Gateway app 去停班时，app 启动会先补跑漏班（今日 07:0x 实证）——写库类 6 班可能在停之前先补跑一次，与云端双写。
**来源**: 2026-11-04 /resume 场「继续迁移完整性检查」
**进展（2026-11-04 19:35 UTC）**: Doctor 确认两 app 不可能同开（单开成因＝app 级互斥，已核）。Doctor 裁「留官方，推看板班也上云」：推看板 8 班改为云端照跑、推送入待推队列 `brain/.tmp/pending-artifact-push.jsonl`、交互会话补推；云端启用 22（21 定时 + 1 按钮触发）；回切操作卡已补云端段。仍待：Doctor 停 Gateway 24 班、各班首跑核对、scheduler-weekly-audit / sessions-monthly-audit 无云端可行形态（暂停，/resume 兜底）。


## [ERR-20261104-004] 经验索引只扫 brain/{项目}/GOTCHAS.md，漏掉 Projects/ 下的 canonical GOTCHAS，/resume 把开放条目报成 0
**状态**: ⚠️ 已知风险
**优先级**: 🟡 中
**触发场景**: 2026-11-04 夜 Code 标签 /resume 后重建经验索引，核对当日新条目时发现。
**硬证据/最小复现**: `.tools/build_experience_index.py` L118 取 `os.path.join(BRAIN, d, "GOTCHAS.md")`。重建后索引总览「白泽大宗：11 条（开放 0）」，`Projects/Financial/白泽大宗/GOTCHAS.md` 实有 12 条 `## [ERR`、状态行 🔄/⚠ 6 条；ERR-20261104-001（哨兵）在索引内命中 0。
**根因**: 生成器按 brain 目录枚举来源，未覆盖 canonical 落在 Projects/ 的项目。
**影响面**: 白泽大宗确认受影响；`Projects/` 下风险日报 3 条、星空 2 条、DVA 2 条、EAL 1 条是否已被 brain 侧覆盖未核。/resume 的「经验召回」会低报开放数。
**修复/建议修法**: 生成器增加 Projects/ 下 canonical GOTCHAS 来源，并处理与 brain 同名件的去重；属行为变更，待 Doctor 批。
**预防门禁**: 重建后对拍各来源 `## [ERR` 计数与索引条数；引用「开放 0」前先核该项目 canonical 位置。
**来源**: 2026-11-04 Code 标签会话，实读生成器与两份 GOTCHAS。
