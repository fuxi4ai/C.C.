# conch · 处理手段：迁移（文件健康审查及整理 · 1.5.0 起）

> 2026-11-17 首例：`Projects/Financial/宏观研究体系/EAL/` → `Projects/Financial/Event-Attribution-Ledger/`（合并嵌套、改名、git 仓根随迁），同日 `Projects/风险日报/` → `Projects/Financial/风险日报/`（迁入上级）。方案范本：`~/Documents/AI4ME/2026-11-17-EAL改名切换方案.md`。
> 2.0.0 起迁移是「文件健康审查及整理」的处理手段之一（总则 `file-health.md` 审查清单 D）；下方第 2 步的切换方案写进七步第 3 步的汇报（需要成文的先写 `$TMPDIR`），由第 5 步一并同意；**同意前不落 `~/Documents/AI4ME/` 文件**，要留档的在第 6 步 apply 时再写。方向性问题同样在第 5 步、子代理复查之后问。
> 适用：项目目录改名、合并嵌套层、迁入或迁出上级目录、数据根搬家。目标目录定法与禁区同 SKILL.md 第 1 步。

## 第 1 步 · 消费方扫描（只读，三种写法各给命中数）

按通用教训 G-X278 分三项扫，每项单列命中数；只查完整路径串、得 0 命中，不等于没有消费方。

1. **完整路径串**：旧路径全串，以及省略前缀的相对写法（如 `宏观研究体系/EAL/`）。
2. **分段拼接**：旧路径的各段名同时出现在一行或相邻几行（例：同一行同时含 `"宏观研究体系"` 与 `"EAL"`，`os.path.join` / `Path(…) / …`）。
3. **按层级推算**：`parents[N]`、单层或多层 `.parent`（如 `HERE.parent / "兄弟目录"`）、`dirname(…)`、`../` 相对链接（2026-11-17 风险日报迁移漏过单层 `.parent`，见 `brain/风险日报/GOTCHAS.md` ERR-20261117-002）。凡层级会因这次挪动而变的文件，逐个核对它推算出的根目录。

**扫描范围**：`~/Documents/Claude/`（brain 与全部项目）、`~/Documents/Database/`、`~/Documents/Codex/`（只读，改动走 V.V.）、`~/.codex/automations/`、`~/Library/LaunchAgents/`、Cowork 云端班镜像 `brain/references/scheduled-live-mirror/live/`。

**分类**：
- 现行引用（代码、调度、现行文档）→ 要改。
- 冻结证据与留痕（审读 JSON、`raw/`、`capture_manifest.json`、结果里记了脚本 SHA 的研究包、`archive/`、`_bak/`、只追加账本的旧条、brain `logs/`、数据根班日志）→ 不改；路径是当时的事实（通用教训 G-X120 2026-09-29 追记「留痕不改」）。只追加的账本另追加一条改名对照。
- 归 V.V.（Codex 侧）或 Cowork 云端班 → 不由 CC 改，写进第 2 步的请求。

## 第 2 步 · 切换方案（交 Doctor 确认）

写到 `~/Documents/AI4ME/YYYY-MM-DD-<项目>改名切换方案.md`，内容：

- Doctor 已裁定的方向（新名称、是否留兼容链接、分几步）与替换规则（哪些前缀替换、哪些一律不动）。
- 切换顺序表：步 · 谁（Doctor 终端 / CC / V.V. / Doctor 在 Cowork）· 动作。
- **切换窗口**：避开相关定时班——列出每个班的触发时刻（launchd、Codex 自动化、Cowork 云端班、本机限期班），窗口须让跨侧改动在下一次触发前完成。
- 三类改动清单：CC 侧（第 1 步的现行引用）、V.V. 侧（Codex 自动化与文件）、Cowork 云端班（班名与处数）。V.V. 与 Cowork 的部分由 CC 写成可直接转达的请求，Doctor 转达。
- 回退：反向移动的方法；**切换前快照**（`<项目>-pre-rename-YYYY-MM-DD.tar.gz`）。方案里承诺的快照要真做，做不了就在迭代记录如实写明（2026-11-17 首例漏做过一次）。

方向性问题（新名称、留不留兼容链接、数据根是否同批迁）先用 AskUserQuestion 问。

## 第 3 步 · 执行

1. Doctor 确认窗口、跨侧已就绪后，请 Doctor 终端停相关 launchd：`launchctl unload ~/Library/LaunchAgents/<label>.plist`。
2. 查近 2 小时有无并发写入（`find <目录> -type f -mmin -120`），有就先问 Doctor；打快照。
3. 移动：`.git`、`.claude` 随迁；两层合并时把外层 `.gitignore` 并入内层，去掉旧前缀，逐条核对规则没有丢（并入前后各列一次被忽略的路径，比对一致）。外层清空后再移除。
4. 改现行引用；按层级推算的写法优先改为按名字查找（如 `next((p for p in HERE.parents if p.name == "Documents"), <原回落>)`），不再写死层数。
5. 自验：跑项目自带校验与测试、相关项目的探针（如风险日报星空新鲜度）、brain 巡检与经验索引测试；被调度执行的脚本逐个解析路径常量，确认文件存在。
6. launchd：plist 改新路径后重载。命令里的备份一步写成 `[ -e 备份 ] || cp 原件 备份`——组合命令会被重跑，`cp` 会把已改过的件盖进备份（通用教训 G-X120 2026-11-10、2026-11-17 两次复发）。
7. 跨侧回执：Doctor 转达后，CC 回读 Cowork 镜像（刷新 `scheduled-live-mirror/live/`）与 V.V. 改过的文件，逐处核对新路径；未复核的写进 TODO。
8. 记录：项目 `迭代记录.md` 追加一条（含新旧路径对照）；brain 决策记录写一条；`brain/permanent/项目总览.md` 与项目 stub 更新路径；涉及技能正文里的路径（如 brain-save Step 4.5）走技能发布链。

## 第 4 步 · 核验与提交

- **独立核验**：开未参与实施的子代理，把第 1 步三种写法重扫一遍（范围相同），报残留与断链。2026-11-17 首例由核验查出 4 处残留。
- **git**：仓根整体改名时，所有文件在 git 里显示为「旧路径 → 新路径」。提交命令用改名配对清单 `git add --pathspec-from-file=<清单>`（清单放项目数据根 `backups/`），不用 `git add -A`——工作树里常有别的会话的未提交改动。commit 与 push 交 Doctor 终端。
- **首次实跑**：切换后第一次定时班跑完，核对产物与日志（新路径是否生效），并比对产物里的「不可用 / 缺数」清单是否比迁移前多；记入 TODO 直到核对完。

## 不做

- 不留兼容软链接，除非 Doctor 另定（留了，旧路径会一直有人用）。
- 不改冻结证据与留痕里的路径。
- 不替 V.V. 改 Codex 侧文件，不替 Doctor 改 Cowork 云端班。
- 不在 `~/Documents/Codex/Project Mirror` 内执行。
