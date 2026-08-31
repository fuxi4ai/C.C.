# 巡检修复审计（_repair_audit）

> 自愈循环审计层：append-only。每次修复动作一行，**用 Edit 尾段追加，不 Write 覆写**（G-X107）。
> 行 schema（六元组）：`ts`(ISO) / `trigger`(硬证据) / `action`(动作+工具名+参数形状) / `rollback`(回退点) / `acceptance`(判据·必须含可跑命令或工具名) / `actor`(实施者) / `status`(🔄/⚠️/✅)。
> 状态只允许 🔄/⚠️/✅；**✅ 只由 Doctor 或指定独立验收方落**（实施者不自签，G-X4）。未验行会被 brain-resume Step 0.6 人读通道 + 周班机器读通道读出。
> 2026-08-29 由自愈循环设计创建：`brain/permanent/巡检自愈循环-loop-engineering.md`。

| ts | trigger | action | rollback | acceptance | actor | status |
|---|---|---|---|---|---|---|
| 2026-08-29T11:20-07:00 | 设计获 Doctor 令（自愈循环 loop engineering）+ 独立审查 PASS_WITH_LIMITS 四条🔴已吸收 | 落盘设计 v2 `permanent/巡检自愈循环-loop-engineering.md` | 文件即文档，可 Edit 回退 | Doctor 批准（含 §8 换文）+ 独立复验 | CC(本场) | 🔄 |
| 2026-08-29T11:35-07:00 | S2 白名单动作（设计 §2 L1） | Edit `scheduler_snapshot.py`：`--triggered-by` 参数+`_meta.triggered_by`+人读头+自证报 triggered_by+docstring 换文（5 处） | git 未 commit 前可 Edit 还原；已 commit 按 git 回退 | `py_compile` 通过 + test_repair_loop.py 负向 + 下次周班快照带 triggered_by=scheduled | CC(本场) | 🔄 |
| 2026-08-29T11:45-07:00 | G-X151：旧「只报告」条文替换（skill 双源+permanent 文档） | Edit brain-resume SKILL.md 双源（portable 真源 + .skills 导出层，改前双向 diff 零漂移）Step 0.6 v2 + 边界条；Edit `定时任务巡检机制.md` §五.3/§九/§十 | 两文件均 git 未 commit，可 Edit 还原 | grep 旧词形 active hits=0 + 双源 diff 一致 + 独立复验 | CC(本场) | 🔄 |
| 2026-08-29T12:00-07:00 | 白名单外 0 动作（S3/F3p 属 Doctor 终端） | S3 周班 prompt 自证步：**未动**（store 沙箱不可读；取回命令已贴 Doctor） | — | Doctor 终端取回全文+SHA → 改 → 贴回 → 再取回+SHA 复验 | CC(本场) | 🔄 |
| 2026-08-30T05:53-07:00 | 08-30 待办①（S3 未装）+ Doctor resume 场选「1」 | S3+audit 机器读通道装：CC 落 staging `~/Documents/_staging_skillaudit_SKILL.md`（SHA 421f210b…）→ Doctor 终端 cp 至 store（shasum 相符=逐字一致）→ rsync 镜像同步（05:53 生效）；旧本体备份 `SKILL.md.bak_20260830_preS3`；旧表述换文（绝不自动修/绝不碰调度器：不调 update_scheduled_task/别自作主张加自检）+frontmatter description 换文 | `cp SKILL.md.bak_20260830_preS3 SKILL.md` + 再 rsync | CC Read 复验 store 96 行逐字一致（实读）+ shasum=421f210b… + 今晚 20:00 PDT 周班跑后 generated_at 前进且 triggered_by=scheduled | Doctor 终端(执行)+CC(起草/复验) | 🔄 |
| 2026-08-31T02:46-07:00 | 08-31 /resume 首验实读：周班已跑（lastRunAt 2026-08-31T03:01:04Z=周日 20:01 PDT）· 快照 generated_at=08-30T20:05:28-07:00 且 **triggered_by=manual** · 实读班 SKILL（store · 96 行 · 421f210b）步骤 1 命令未传 `--triggered-by scheduled`（脚本默认 manual · L425）→ 验收判据「generated_at 前进且 triggered_by=scheduled」结构性不满足（S2 脚本侧已装、S3 班 prompt 未接线） | 诊断留痕 · 修复=班 SKILL 步骤 1 命令加 `--triggered-by scheduled`（prompt 改动→Doctor 终端 SHA 往返 · staging 草案 CC 已备 `~/Documents/_staging_skillaudit_flagfix_2026-08-31_SKILL.md`） | 班 SKILL 现文在盘（shasum 421f210b0304 · 改前备份照 08-30 惯例） | 修复后下次周班快照 generated_at 前进且 **triggered_by=scheduled**（读 `permanent/_scheduler_snapshot.json` `_meta`） | CC(本场·/resume 实读) | 🔄 |

> ⚠️ 本表未 commit 前属本地唯一副本——git commit 由 Doctor 终端执行（沙箱 git 禁令）。
