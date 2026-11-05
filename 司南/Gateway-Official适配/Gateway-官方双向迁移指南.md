---
title: Gateway ⇄ 官方 双向迁移指南
tags: [司南, Gateway-Official适配, 模式切换, SOP, runbook]
created: 2026-11-05
updated: 2026-11-05
status: active
type: sop
project: 司南/Gateway-Official适配
---

# Gateway ⇄ 官方 双向迁移指南

> **用途**：在 Gateway 壳（Claude-3p）与官方 Anthropic 订阅（Claude 桌面端 · 云端定时任务）之间整壳切换时，照本页走一遍即可，不必翻历史日志。
> **取材**：六站沿革（06-30 → 11-01）+ 2026-11-04/05 正式切官方的实操 + 同日两轮迁移完整性自检。
> **证据口径**：标「实测」＝11-04/05 在官方侧实跑实读过；标「未实测」＝按真源与机理推断，下次切换时补证。方向 A（Gateway→官方）已实战；方向 B（官方→Gateway）在云端化之后**尚未实战**。
> **真源关系**：本页是整合版流程。§4 B1–B5 的原文真源是 `references/scheduled-live-mirror/回切操作卡.md`「附 · 云端定时任务回切」；两处冲突时以回切卡为准，并回报 Doctor 订正本页。

---

## 0 · 三条前提（先读）

1. **两个 app 不能同开**（Doctor 2026-11-04 确认）。切换＝整壳切换，不存在「云端跑一半、Gateway 跑一半」的混合态（司南 ERR-20261104-003）。
2. **Gateway app 一打开就会补跑漏掉的班**（2026-11-04 07:0x 实证）。写库班若对侧当日已跑过，会重复写——所以切换时点要挑在当日写库班之前，切完别随手再开旧 app。
3. **注册表不随环境走**。文件在、不等于任务在；任务在、不等于跑成了。每一步都以平台对象按 id 回读为准（G-X248）。

---

## 1 · 两侧差异速查

| 维度 | Gateway（Claude-3p 壳） | 官方订阅（云端定时任务） |
|---|---|---|
| 执行引擎 | DeepSeek API 映射（11-01 定版） | Claude（任务可钉模型，如 `claude-opus-5-5`） |
| 定时任务存放 | 本地 store `~/Gateway-workspace/Scheduled/{taskId}/SKILL.md`，app 面板启停 | claude.ai 账号级云端任务：`list_triggers` / `create_trigger` / `update_trigger` / `delete_trigger` / `fire_trigger`；prompt 存服务器端 `prompt` 字段，**不读本地 SKILL.md** |
| 运行位置 | 本机沙箱 | 绑定 Mac，跑在 Mac 侧 Linux 虚拟机（3.9 GB 内存、无 swap · 实测）；Mac 休眠或 app 未开则跑不了 |
| 文件夹挂载 | 平铺：`/sessions/*/mnt/<目录名>`，可用 `request_cowork_directory` 临时挂（G-X45） | 整挂 `Documents` 于 `$HOME/mnt/Documents`；`$HOME/mnt` 只读，补不出旧平铺挂载点；无 `request_cowork_directory` / `mcp__cowork__*`；命令一律 `mcp__remote-devices__device_bash`（实测） |
| 文件读写工具 | Read / Edit / Write 直接落盘 | Read / Edit / Write 作用于云端容器，**不落 Mac**；改文件只能走 device_bash |
| 出网 | 开放出网（G-X44） | 账号白名单；取数域名须在列（DeepSeek、SMM 已由 Doctor 11-04 确认通） |
| 删除 | 挂载盘 rm 默认被拦 | 同样 `Operation not permitted`；无人值守班**不得**请求删除权限（会卡死），用截 0 字节 / mv 改名 |
| 看板推送 | 班内原生推 | 云端班会话里**没有** `update_artifact`（实测）→ 班只登记补推队列 `brain/.tmp/pending-artifact-push.jsonl`；Doctor 在交互会话说「补推看板」，CC 按 stage → SendUserFile → `update_artifact` 三步推 |
| 运行结果通知 | — | 云端会话可用 `PushNotification`；`create_trigger` 的 `notifications` 只能建时设（实测） |
| skills 安装 | Gateway 应用内装（frontmatter 须双引号，G-X43） | 官方 Customize > Skills > Upload，账号级 |
| 镜像脚本 | `scheduler_snapshot.py` `MIRROR_ENABLED=True`（Gateway store → brain live 镜像） | `MIRROR_ENABLED=False`（11-04 起，否则会用 Gateway 旧版冲掉 live/ · ERR-20261104-005） |
| 班正文真源 | Gateway store | 8 个推看板班：`references/scheduled-live-mirror/live/<班>/SKILL.md`；其余班：云端 prompt（＝前置段 + Gateway 原文） |
| 终端 `claude` | cc-switch 写入的 `ANTHROPIC_*` 走本地代理 | 11-04 已清（备份 `~/.claude/settings.json.bak_ccswitch_2026-11-04`） |
| 会话树 | `~/Library/Application Support/Claude-3p/`（11-04：1233 场 · 21 GB，冻结待冷归档） | `~/Library/Application Support/Claude/local-agent-mode-sessions/`（11-04：730 场 · 3.1 GB） |
| claude 评分器口径（龙鱼双评分） | 随壳 DeepSeek Pro → 与 deepseek 评分器**同源** | Claude Opus 5.5 → 恢复**异源**；deepseek 评分器始终走 `api.deepseek.com`，两侧不变 |

---

## 2 · 方法要点（八律 + 本次新增七条）

八律见索引页 `Gateway-Official适配.md`，仍全部有效。云端化后新增：

9. **建成要按 id 回读**：create / update 的回执不算数，`list_triggers` 按 id 读到 `enabled`、`cron`、`folders_state` 才算（G-X248）。
10. **`last_run.status=SUCCEEDED` 只代表派发成功**：fired 到 finished 只有 3–6 秒。跑没跑成看产物、简报、库的新写入。
11. **`fire_trigger` 附加的 text 会被当成数据、不执行**：要让班多做一步（探针、体检），写进 prompt 本身。
12. **`folders` 和 `notifications` 只能建时设**：`create_trigger` 带 `folders` 会弹批准卡，Doctor 不批就不生效；`update_trigger` 只能改 name / cron / enabled / model / prompt / run_once_at。要改这两项＝新建 → 回读 → 再删旧。
13. **`update_trigger` 由主会话直接调**：subagent 调要走审批，无人应答就卡住。
14. **Mac 侧虚拟机内存小**：重计算（如星空布局）放云端容器跑，再把结果写回（星空 NOTE-20261101-002 第 2 次即此）。
15. **写库班不许双跑**：先停旧侧，再开新侧；只读、幂等的班可以短暂重叠。

---

## 3 · 方向 A：Gateway → 官方（2026-11-04 实战版）

| 步 | 动作 | 判据 / 证据 |
|---|---|---|
| A0 | 确认官方订阅可用；Gateway 照跑不动 | — |
| A1 | **盘点**：Gateway 班清单与 cron（指令卡附表 · 24 班）；artifact 台账；官方侧 `list_triggers` 看是否已有他场建的任务 | 两侧清单对上；云端已有的旧任务先全部 `enabled=false` 并回查为 0 |
| A2 | **文件层备份**：brain 等仓贴命令给 Doctor 终端提交；Gateway store 不动（保底，也是 prompt 源头）；官方旧 store `~/Claude's workspace/Scheduled/` 冻结、不再同步 | 提交回执 |
| A3 | **账号层**：`ListSkills` 对 `permanent/已装skill清单.md`，缺的经 Customize > Skills > Upload 补；MCP 配置按「先退出 app → 改 → 再启动」（ERR-20261104-002） | skill 清单对齐 |
| A4 | **改 prompt**：每班开头加「运行环境前置」段（附录 A）；推看板班再加「看板推送改补推」段，并改为引用镜像真源 `live/<班>/SKILL.md`；巡检周班加第 0 步云端体检 | 改前存底稿（11-04 底稿在 `brain/.tmp/prompt-fix-2026-11-04/`） |
| A5 | **建任务**：`create_trigger`，`folders` 挂 `~/Documents`、`notifications.push=true`、暂停态；Doctor 批卡 | 按 id 回读：`folders_state` 非 NONE、`enabled=false`、cron 与附表一致 |
| A6 | **试跑**：先拿只读班做试点（11-04 `us-close-backfill` 19/19 通过）；写库班先 dry-run。⚠ 干跑别探脚本本体（白泽 ERR-20261104-001：`--help` 误触哨兵，覆盖了 state） | 简报 + 库零误写 |
| A7 | **切换**：Doctor 在 Gateway 面板停全部班 → 退出 Gateway app → CC 逐个 `update_trigger(enabled=true)` | `list_triggers` 回查 enabled 数＝应启用数；停班时刻后 Gateway 侧各写库目标零新写入 |
| A8 | **看板**：抢救 Gateway 侧最新本体（八律第 6 条），在交互会话推一次；无定时班刷新的看板维持手动推 | `update_artifact` 后回读，剥掉 `cowork-artifact-meta` 块逐字节比对一致；遇硬链接先 `cp` 断链 |
| A9 | **巡检兜底**：`scheduler-weekly-audit` 第 0 步只读 `list_triggers`，判挂起 / 非 SUCCEEDED / 日频周频超 8 天未触发 / next_run 过期 1 小时，写 `permanent/_cloud_trigger_health.json`，并 PushNotification | 首次按时运行后核 json 的 `generated_at` 前进 |
| A10 | **口径**：引擎变了的班打口径切换桩（11-04 为 claude 评分器打桩：`Database/龙鱼-标的分析库/趋势/_口径切换桩_2026-11-04_claude评分器换模型.md`）；班正文加切换注记 | 桩与注记沿革一致 |
| A11 | **收尾**：`MIRROR_ENABLED=False`；指令卡「第一步 1.1–1.3」标作废；cc-switch env 清（留备份）；Gateway 会话树冷归档挂待办 | 逐项回读 |
| A12 | **首跑验收**：首个完整交易日、首个周末周班、首个月班各核一次 | 见 §5 |

---

## 4 · 方向 B：官方 → Gateway（未实测 · 回切卡附段 + 本次自检补项）

**选时点**：避开当日写库班已跑完、Gateway 补跑又会重跑的窗口；最好在当日写库班之前切。

| 步 | 动作 | 判据 / 证据 |
|---|---|---|
| B0 | 交互会话先「补推看板」清空队列，或明确作废（Gateway 会重新生成） | 队列空 / 作废记录 |
| B1 | 官方 app 里 `list_triggers` 取全量 → 所有 `enabled=true` 的逐个 `update_trigger(enabled=false)`，**不删** | 回查 enabled=0（含 `sessions-monthly-audit`、`scheduler-weekly-audit`） |
| B2 | **先回写真源再开镜像**：云端期间改过的班，把改动同步回 `~/Gateway-workspace/Scheduled/<班>/SKILL.md`——推看板 8 班取 `live/<班>/SKILL.md`；其余班从 `list_triggers` 实读 prompt，**剥掉**「运行环境前置」段与「看板推送改补推」段后即 Gateway 原文 | 逐班 diff：Gateway store ＝ 云端正文 |
| B3 | B2 完成后才把 `scheduler_snapshot.py` 的 `MIRROR_ENABLED` 改回 `True`（顺序反了会用旧版冲掉 live/ · ERR-20261104-005） | 跑一次 S1，live/ 更新数符合预期 |
| B4 | 完全退出官方 app → 打开 Gateway app → 面板逐班启用 | 留意启动补跑；写库班看库里是否重复写 |
| B5 | 需要终端 `claude` 走 cc-switch：从 `~/.claude/settings.json.bak_ccswitch_2026-11-04` 恢复 `env` 段，或让 cc-switch 重写 | `claude` 能连通 |
| B6 | **口径桩**：claude 评分器 Claude → 随壳 DeepSeek，双评分重新**同源**，按 08-02 / 11-04 先例再打一根桩，班正文注记同步 | 桩已落、注记已改 |
| B7 | `sessions-monthly-audit` 的盘点对象改回 Gateway 会话树；增量基线重置 | 首跑报「新基线」 |
| B8 | `scheduler-weekly-audit` 第 0 步在 Gateway 下没有 `list_triggers` → 应报「不适用」而非报警（**未核**，回切时实测） | 首跑简报 |
| B9 | 首跑验收同 A12 | 见 §5 |

**再从 Gateway 切回官方（云端任务仍在、只是停着）**：Gateway 面板全停 → 退出 Gateway → Gateway 期间改过的班先 `update_trigger(prompt=…)` 写回云端、推看板班同步 live/ → `MIRROR_ENABLED=False` → 逐个 `enabled=true` 并回查 → 补口径桩。不需要重走 A3–A6。

---

## 5 · 双向检查清单（切完当天与首跑后各过一遍）

| # | 项 | 怎么核 | 通过判据 |
|---|---|---|---|
| 1 | 旧侧全停 | 官方：`list_triggers`；Gateway：面板 | 旧侧 enabled＝0 |
| 2 | 新侧全开 | 同上 | 启用数＝应启用数（11-04 官方侧为 24：23 原有 + sessions-monthly-audit） |
| 3 | 挂载 | 官方：回读 `folders_state`；首跑简报有无「挂载缺失」 | 无缺失 |
| 4 | 真源一致 | 推看板班 live/ ↔ 运行侧正文 diff | 只差前置段 / 补推段 |
| 5 | 镜像开关 | `grep MIRROR_ENABLED .tools/scheduler_snapshot.py` | 官方期 False / Gateway 期 True |
| 6 | 写库无双跑 | 切换时刻后旧侧写库目标的 mtime | 零新写入 |
| 7 | 看板 | `list_artifacts` 的 updatedAt；补推队列 | 前进；队列已清或已作废 |
| 8 | 口径桩 | 龙鱼 `趋势/_口径切换桩_*` | 本次切换有桩 |
| 9 | skills | `ListSkills` ↔ `已装skill清单.md` | 一致 |
| 10 | 巡检 | `_cloud_trigger_health.json`（官方期）/ S1 快照（Gateway 期） | `generated_at` 前进、无报警或报警已处理 |
| 11 | 首跑产物 | 交易日班、周班、月班各一 | 产物与简报齐、数值抽查对得上 |

---

## 6 · 已知坑速查

| ID | 一句话 |
|---|---|
| 司南 ERR-20261104-001 | 官方壳 Code 标签与 Cowork 标签是两个执行面，读数互不代表 |
| 司南 ERR-20261104-002 | 改 MCP 配置：先退出 app → 改 → 再启动 |
| 司南 ERR-20261104-003 | 混合方案与「两壳只能单开」冲突 |
| 司南 ERR-20261104-004 | 经验索引须同时扫 `Projects/` 下的 GOTCHAS |
| 司南 ERR-20261104-005 | `scheduler_snapshot.py` 镜像会覆盖 live/，靠 `MIRROR_ENABLED` 开关 |
| 白泽 ERR-20261104-001 | 干跑探 `--help` 误触哨兵本体，state 被覆盖 |
| 星空 NOTE-20261101-002 | 星空数据段替换须回读核验；Mac 侧虚拟机布局 OOM |
| G-X43 | Cowork skill frontmatter 须双引号 |
| G-X44 | Gateway 开放出网，官方默认拒绝 + 白名单 |
| G-X45 | Gateway 平铺挂载，路径层级与 Mac 不同 |
| G-X53 | 整挂父目录被拒＝父目录覆盖了受保护子目录 |
| G-X248 | 「已建 / 已生效」按 id 回读平台对象再说 |
| EXP-20261104-005-T | 云端定时任务运行环境要点（含平台事实六条） |

---

## 7 · 文件索引（真源指针）

- `references/scheduled-live-mirror/回切操作卡.md` —— 「附 · 云端定时任务回切」为 §4 B1–B5 真源
- `references/scheduled-live-mirror/官方端适配指令卡-2026-11-04.md` —— 〇b 调度面、〇c 切换清单与任务 id、附表 24 班 cron
- `references/scheduled-live-mirror/live/<班>/SKILL.md` —— 推看板 8 班正文真源
- `permanent/切环境复原清单.md` —— 五类复原项
- `permanent/_repair_audit.md` 第 38、39 行 —— 巡检周班与 9 班前置的修复留痕
- `permanent/_sessions_monthly_audit.md` —— 会话树基线
- `brain/logs/2026-11-04-云端迁移自检与巡检修复.md` —— 本次迁移自检日志
- `Database/龙鱼-标的分析库/趋势/_口径切换桩_2026-11-04_claude评分器换模型.md` —— 口径桩先例

---

## 附录 A · 云端班「运行环境前置」段模板（2026-11-04 晚 · 整挂 Documents 版）

> 来源：11-04 晚 9 班实装版底稿。以云端任务 prompt 实读为准；改模板时同步改本附录。

```
## 运行环境前置（官方云端 Cowork · 整挂 Documents）

- 本班绑定 Doctor 的 Mac。随任务挂载的是 Doctor 整个 `Documents` 文件夹，运行时位于 `$HOME/mnt/Documents`。所有命令用 `mcp__remote-devices__device_bash` 执行；正文里的 `mcp__workspace__bash` 也一律换成它。
- 不要调用 `request_cowork_directory` / `mcp__cowork__*`（新环境无此工具）。正文里「先挂载某目录」的步骤一律视为已挂载——它们都在 `Documents` 之下。
- 开工先跑路径垫片并核挂载：`[ -e ~/Documents ] || ln -sfn "$HOME/mnt/Documents" ~/Documents; ls -d "$HOME/mnt/Documents"`。不存在（多半是 Mac 休眠或 app 未开）→ 简报明写「本轮挂载缺失」后停，不硬跑。
- 旧平铺路径换算（`$HOME/mnt` 只读）：`Database` → `$HOME/mnt/Documents/Database`；`Claude` → `$HOME/mnt/Documents/Claude`；`Projects` → `$HOME/mnt/Documents/Claude/Projects`；`AI4ME` → `$HOME/mnt/Documents/AI4ME`；`brain` / `Brain` → `$HOME/mnt/Documents/Claude/brain`；其他名字在 `$HOME/mnt/Documents` 下用 `find -maxdepth 5` 定位。不要因为只看到 Documents 就判缺挂载。
- 正文里凡说用 Read / Edit / Write 读写文件，一律改用 device_bash——那几个工具作用于云端容器，改了不会落到 Mac。`present_files` 不可用：在简报里列出文件路径。
- 正文里写死的 `/Users/lunarabbit/Documents/...` 一律换成 `~/Documents/...`。
- 挂载点内 rm / rmdir / unlink 报 `Operation not permitted` 属预期：截 0 字节、mv 改名处理；不得请求删除权限或调用任何需人工批准的工具（无人值守会卡死）。
```

推看板班另加一段（要点）：不调 `update_artifact`；产出 HTML 后向 `brain/.tmp/pending-artifact-push.jsonl` 追加一行（ts / task / artifact_id / html_path / summary），简报写明「待补推」。
