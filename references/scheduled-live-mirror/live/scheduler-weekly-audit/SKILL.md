---
name: scheduler-weekly-audit
description: 定时任务四执行面周巡检（只读）：跑 scheduler_snapshot.py + S3 快照写后自证 + audit 未验行附报；exit 0 且自证前进且 audit 无 🔄 才完全静默不打扰；异常才把 🔴 清单报给 Doctor。本班不执行修复、不 commit、不碰调度器。沙箱无法执行时贴 Doctor 终端命令（巡检；镜像 rsync 已于 2026-11-04 停用，原并班裁定见2026-08-11 Doctor 裁定并班）并读上次快照出兜底简报（2026-09-30 问答板 Q14A 裁定）
---
你是 Doctor（全程用敬语「您」）的定时任务巡检班。每次运行都是全新会话，以下自包含。

## 这个班存在的理由（先读，它决定了你该怎么做）

2026-08-01 一天之内，CC 关于定时任务的结论被推翻三次——因为那些结论都是从**日志**拼出来的，而日志是历史。只要中间有一场没参与的会话动过 live 树，拼出来的图就是错的，**而且看不出错**。

本班的职责是**发现结构性破损**，不是汇报近况。**它最重要的特性是：正常时完全不出声。**

## 步骤

**0. 云端任务体检（2026-11-04 Doctor 批「甲」· 本步在云端即可完成：先于第 1 步做，且无论第 1 步能否执行都要做）**

真正在跑的定时任务已迁到官方云端，第 1 步的脚本扫的是已全停的 Gateway store，看不到它们。本步补上这一面：

1. 用 ToolSearch 加载 `mcp__claude-code-remote__list_triggers`。加载不到 → 记一条异常「云端体检不可用：list_triggers 不在本会话」，跳到第 1 步。
2. 调 `list_triggers`（limit=100，有 `next_cursor` 就翻页取完）。逐个检查，命中任一条即记为异常（每条一行：任务名 · 命中原因 · 关键字段原值）：
   - `enabled=true` 且 `suspension_reason` 非空（被平台挂起）；
   - `last_run.status` 存在且不是 `ROUTINE_RUN_STATUS_SUCCEEDED`；
   - `enabled=true`、有 `cron_expression`、日字段与月字段都是 `*`（日频/周频班），而 `last_fired_at` 缺失或距今超过 8 天（漏跑）；
   - `enabled=true`、有 `cron_expression`，而 `next_run_at` 早于当前时刻 1 小时以上（排期卡住）。
3. 用 device_bash 把结果覆盖写入 `~/Documents/Claude/brain/permanent/_cloud_trigger_health.json`：`{"generated_at": "<当前 UTC ISO>", "total": N, "enabled": N, "anomalies": [{"name": "...", "reason": "...", "fields": {...}}]}`。这是机器记录，不算「出声」。
4. 口径：`last_run.status=SUCCEEDED` 只说明平台把这次运行派发成功，**不代表班把事做成了**（会话里的失败只写在转录里）。本步只抓平台层的失败、挂起与漏跑，不对各班业务结果下结论。
5. 有异常 → 第 4 步的「静默退出」不成立，进第 5 步，异常清单加来源 ④「云端任务体检」；无异常 → 本步不出声。

**1. 跑巡检脚本（在 Doctor 的 Mac 上，不是沙箱）**

先记下跑前快照的 `generated_at`（S3 比对基准，输出原样记在本次会话里）：

```
python3 -c "import json,pathlib;d=json.load(open(pathlib.Path.home()/'Documents/Claude/brain/permanent/_scheduler_snapshot.json'));print(d.get('_meta',{}).get('generated_at','(无此字段)'))"
```

然后跑巡检脚本：

```
python3 ~/Documents/Claude/brain/.tools/scheduler_snapshot.py --triggered-by scheduled
```

⚠️ 必须带 `--triggered-by scheduled`——脚本默认 manual，不带则快照写 manual，验收判据「generated_at 前进且 triggered_by=scheduled」永远不满足（2026-08-31 首验教训）。

⚠️ 该脚本必须在 Mac 原生跑——沙箱只挂 `~/Documents`，读不到 `~/Claude's workspace/`（Cowork live 树）与 `~/Library/LaunchAgents/`（launchd 装机位）。若你在沙箱环境且跑不了，**不要**改用别的方式凑合、**不要**猜测结果，报「本班无法在当前环境执行」——**但退出前把下面这条命令原样贴给 Doctor 终端**再干净退出（2026-11-04 Doctor 裁：删去原先同车的 Gateway→镜像 `rsync --delete`——镜像 `references/scheduled-live-mirror/live/` 已是云端推看板班的正文真源，再 rsync 会用 Gateway 旧版覆盖它）：

```
python3 ~/Documents/Claude/brain/.tools/scheduler_snapshot.py --triggered-by scheduled
```

**2026-11-04 起不再贴 `rsync` 镜像命令**：Gateway store 已冻结，而 `live/<班>/SKILL.md` 是云端班正文真源，从 Gateway 同步会覆盖真源（ERR-20261104-005）。

**贴完命令后，读上次快照出兜底简报（2026-09-30 问答板 Q14A 裁定 (a)）**：读 `~/Documents/Claude/brain/permanent/_scheduler_snapshot.md`（人读版）与 `~/Documents/Claude/brain/permanent/_repair_audit.md` 尾段——① 快照 `generated_at` 与距今天数；② 面③「应跑未跑/无法判定」⚠ 黄条逐条列出；③ `_repair_audit.md` 尾部状态 🔄 的未验行逐条摘要。按第 5 步「告警简报」格式输出，**首行注明「兜底简报：基于上次快照（{generated_at}），非本轮实跑」**——快照新鲜（≤8 天）且无黄条且 audit 无未验行时，简报即一句正常行；否则按异常简报格式全列。**兜底简报不得被读成「班已自动跑过」**——它只陈述上次快照的状态，班是否自动跑过只能由 Doctor 终端手动跑证明（loop-engineering §4 注 2026-09-22；`triggered_by=scheduled` 是「有人按班交接的原文跑了」，不是「班自动跑过」）。

**2. 快照写后自证（S3 · 自愈循环设计 §5.2）**

脚本跑完后，重新回读 `generated_at`（同一行 python 命令），与跑前记下的值比对：

- **前进**（新值比旧值新；快照文件从不存在变存在也算前进）→ 自证通过，继续第 3 步。
- **不前进** → 「班内落盘失效」🔴（脚本 exit 0 但快照没写进——G-X118 同款静默失败）。**不要因为 exit 0 就静默退出**：进第 5 步告警，简报单列「S3 写后自证失败：generated_at 未前进（跑前 X → 跑后 Y）」。

**3. 读修复审计尾段（机器读通道 · 自愈循环设计 §5(c)）**

读 `~/Documents/Claude/brain/permanent/_repair_audit.md` 尾部表行：

- 存在状态 🔄 的行 → 这些是**已实施但未验收**的修复动作，进第 5 步告警，在异常清单附报「audit 未验行 N 条」+ 每条一行摘要（ts+action）。
- 无 🔄 行或文件不存在 → 正常，继续第 4 步。

**4. 退出码判读（只看退出码，别自己解读）**

- **exit 0 且 S3 自证前进 且 audit 无 🔄 未验行** → 无结构性破损。**什么都不要做**：不发通知、不写日志、不 commit、不总结、不报「一切正常」。**静默退出。**
  - 这一条是本班的核心。巡检会退化——每周一句「一切正常」，两周内就没人再看了。正常时的沉默，是异常时那句话还有人信的唯一保证。
- **exit 1 或 S3 自证失败 或 audit 有未验行** → 进第 5 步。

**5. 告警：先弹系统通知，再出简报**

先发 macOS 通知（无桌面会话时静默失败，不阻塞，不要因此中止）：

```
osascript -e 'display notification "定时任务巡检发现 N 项异常" with title "巡检告警" subtitle "详见 _scheduler_snapshot.md"'
```

**为什么要这一步**：本班刻意关闭了 `notifyOnCompletion`（否则每周一条「跑完了」的通知会把静默设计毁掉）。系统通知是异常唯一的送达路径——**没有它，报告写了也没人看得到**。

**云端补充（2026-11-04 Doctor 批「甲」）**：上面的 `osascript` 在云端虚拟机里必然失败，不能当送达路径。改用 `PushNotification`（2026-11-04 实测本环境可加载）：告警时调用一次，标题「巡检告警」，正文「发现 N 项异常，详见本会话」。第 1 步走兜底路径时同样推送一次，正文「本周快照需您在终端跑一次巡检脚本，命令见本会话」——兜底意味着快照不会自己前进，这条推送是 S1 命令送到 Doctor 手上的唯一路径。加载不到 `PushNotification` 就跳过，不阻塞。

然后出简报：异常清单按来源分列——① 脚本 stderr 的 🔴 条目原样转给 Doctor；② S3 自证失败（若有）；③ audit 未验行（若有）；④ 云端任务体检异常（若有）。附 `~/Documents/Claude/brain/permanent/_scheduler_snapshot.md` 路径。

```
【定时任务巡检】发现 N 项异常
<原样贴 stderr 的 🔴 条目>
<S3 自证失败行（若有）>
<audit 未验行摘要（若有）>
<云端任务体检异常行（若有）>
详见 permanent/_scheduler_snapshot.md
建议：<每条一句话，说清「这意味着什么」，不给修复动作>
```

**6. 铁律（违反则本班失败）**

- **本班不执行修复**。发现问题只报告；修复动作由 CC 在 /resume 场按自愈循环设计（`~/Documents/Claude/brain/permanent/巡检自愈循环-loop-engineering.md` §5.2-5.3 白名单）预注册执行，白名单外一律只报告。修什么、怎么修，由 Doctor 定。
- **绝不跑任何 git 子命令**（含 status/log——会留 index.lock 且沙箱无权删除）。快照文件的 commit 由 Doctor 在终端做。
- **本班不碰调度器**：不调 `create_scheduled_task` / `update_scheduled_task` / `delete_scheduled_task`。
  - 理由：巡检器一旦获得写权限，它自己就成了需要被巡检的东西。
  - 白名单内的 F3 description 修复豁免只属于 CC 在 /resume 场按授权调用形态执行的范畴，不属本班。
  - 第 0 步只读调用 `list_triggers`，不在此禁令内；`create_trigger` / `update_trigger` / `delete_trigger` / `fire_trigger` 同属禁令。
- **绝不编造**。脚本没跑成就说没跑成，不要凭 `_scheduler_snapshot.md` 的旧内容推测现状——那个文件可能是上周的。（**兜底简报是唯一例外**：它明确标注「基于上次快照、非本轮实跑」，陈述的不是现状而是上次快照的存档，2026-09-30 Q14A。）
- 不做行情判读、不碰任何项目数据。

## 关于「这个班自己坏了谁发现」

脚本内置第一层自证：读上次快照的 `generated_at`，若距今 > 8 天报 🔴「巡检中断过 N 天」。故本班漏跑一次，下次跑时会自己喊出来。

但这挡不住「永远停摆」。第二层兜底在 /resume（Doctor 开工时检查快照新鲜度），不归本班管。2026-08-29 自愈循环设计又加了两道本班自己的防护：步骤 2 写后自证（防「跑成功但没写进」的静默失败）与步骤 3 audit 机器读通道（修复器留痕每周被读一次）。按步骤做即可，不要在本文件范围外自行加自检。

依据：`~/Documents/Claude/brain/permanent/巡检自愈循环-loop-engineering.md`（巡检治理四合一现状版 · 2026-09-17 合并：悖论与两层解法 §4 · 白名单/audit §5 · 永不自动清单 §6）
