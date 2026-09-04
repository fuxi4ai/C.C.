---
name: "brain-resume"
description: "Restore working context at the start of a session. Trigger when the user types `/resume` or says \"恢复上下文\", \"继续上次\", \"上次干到哪了\", \"接着昨天\". FIRST loads global collaboration preferences (Settings mirror — incl. addressing Doctor as 「您」) to close the G-X13 blind spot, then — if the ElevenLabs voice bridge is available — speaks a short spoken handoff, **then checks the scheduler snapshot's freshness (Step 0.6 — the second layer that catches a permanently stalled 巡检班; the first layer can only speak when there IS a next run)**, then reads the most recent 3 session logs from `~/Documents/Claude/brain/logs/` (**including folded month subdirectories `logs/YYYY-MM/`** — root-only listing silently under-reads around the 1st of each month), plus the active project's architecture overview and decisions, then outputs a structured handoff: last project worked on, key decisions, outstanding TODOs, and three suggested next steps."
---

# brain-resume — 恢复跨 session 工作上下文

## 触发

- `/resume`
- "恢复上下文" / "继续上次" / "接着昨天" / "上次干到哪了"

## 执行步骤

### Step 0 · 载入全局协作偏好（每次必做 · 堵 G-X13 盲区）

Cowork / `/resume` 起手**不自动载**全局协作偏好，极易漏「对 Doctor 一律用『您』」等全局规则（G-X13）。所以在做任何事之前，先读一眼镜像并认领：

```bash
cat ~/Documents/Claude/brain/permanent/全局偏好-Settings镜像.md
```

认领其中的全局条后再往下——尤其：**称呼 Doctor 一律用敬语「您」**、改既有资产 propose-then-confirm（范围限定：方向性/判断性/无既定最优解的修改走三步；方向+方案已批且无实质偏离不再二次确认；事务性/文件性/存在明确最佳解且无需人工判断的 TODO 适用常驻自动授权）、可逆优先（重要文件只归档不删，CC 本轮临时文件可清）、不在沙箱跑 git 写命令、需 Doctor 拍板的事走 AskUserQuestion（正文给推荐/不推荐+理由）、不选边不谄媚、裸数字＝实指。
镜像文件缺失则退读 `~/Documents/Claude/brain/permanent/Doctor协作偏好.md`。

**顺带查漂移**：Settings 的内容每轮都注入 CC 上下文，把注入的原文与镜像里的块逐行比对即可，发现不一致当场报、别默认哪边对。

### Step 0.5 · 起手开声（语音链路可用则先出一段 · 堵起手哑口盲区）

载完全局偏好后，若 ElevenLabs 桥接可用：**先**按音色 C.C.（voice_id `C7iLuTwlT58pHXVmnmWe` · `eleven_v3` · zh · stability 0.5 · speed 1.0）出一段 ≤150 字口语短版（「已恢复上下文」之类），落 `~/Documents/Claude/.tts-scratch`，再往下做 resume。链路不可用则静默跳过。
语音无后台自动触发器、须每轮主动调 TTS——**起手这一下最易漏**（注意力全在 resume 正文），故在流程里显式固化。

### Step 0.6 · 巡检新鲜度与修复审计（2026-08-02 立 · 2026-08-29 自愈循环 v2 升级）

**先读修复审计**：`~/Documents/Claude/brain/permanent/_repair_audit.md` 尾段——存在状态 🔄/⚠️ 的行，在摘要里列出（未验修复不得静默；文件不存在＝尚无修复动作，正常）。

再查快照新鲜度（含 triggered_by）：

```bash
python3 - <<'PY'
import json, datetime, pathlib
p = pathlib.Path.home()/"Documents/Claude/brain/permanent/_scheduler_snapshot.json"
if not p.exists():
    print("⚠ 定时任务快照不存在——巡检机制可能从未跑过")
else:
    d = json.load(open(p, encoding="utf-8"))
    meta = d.get("_meta") or {}
    ts = meta.get("generated_at", "")
    tb = meta.get("triggered_by")
    try:
        dt = datetime.datetime.fromisoformat(ts)
        gap = (datetime.datetime.now(dt.tzinfo) - dt).days
        print(f"定时任务快照：{ts[:10]}（{gap} 天前）· triggered_by={tb or '旧快照无此字段'}")
        if gap > 8:
            print(f"⚠ 快照超期 {gap} 天 → 按自愈循环 F1 分臂：本场实核 scheduler-weekly-audit 的 lastRunAt——")
            print("   若也超 8 天 = F1a 周班停摆（只报告，由 Doctor 定）；")
            print("   若新鲜     = F1b 班内落盘失效（贴 S1 重跑命令恢复基线；S3 未装则提示装 S3）")
    except Exception:
        print(f"⚠ 快照时间戳解析不了：{ts!r}")
PY
```

**为什么这一步必须在 `/resume` 里**（而不是交给巡检班自己）：

> **巡检定时任务的东西，自己也是个定时任务。它坏了谁发现？**

巡检脚本内置了第一层自证（读上次快照，>8 天则报「巡检中断过 N 天」），但那**只在「有下一次跑」时才发得出声**。若周班彻底停摆，第一层永远不会被执行 —— 完全静默，正是它要消灭的病。

⇒ **定时的东西必须用不定时的东西兜底。** `/resume` 是唯一天然不定时、又必然会发生的检查点。同一处还顺带读修复审计（上段）——修复器越界与否的「人读通道」挂在这里。

**超期时怎么办（F1 分臂 · 白名单外一律只报告）**：按 `brain/permanent/巡检自愈循环-loop-engineering.md` §2 L2 执行——F1a（周班停摆）只报告，不代跑不代修，由 Doctor 定；F1b（班内落盘失效）贴 S1 重跑命令（Doctor 终端）+ 提示 S3 装否。其余任何修复动作必须落在自愈循环白名单内并写 audit 留痕，白名单外 fail-closed 只报告。

### Step 1 · 读最近 3 篇会话日志

```bash
ls -t ~/Documents/Claude/brain/logs/*.md \
      ~/Documents/Claude/brain/logs/[0-9][0-9][0-9][0-9]-[0-9][0-9]/*.md 2>/dev/null | head -3
```
把这 3 个文件全文读入。

> ⚠ **必须带上 `logs/YYYY-MM/` 子目录**：`meditation.fold_logs` 每月 1 号把上月日志折进子目录，月初根目录可能不足 3 篇——只扫根目录会在**每月 1 号前后静默读不满 3 篇**。刻意不用 `find` 全递归：那会把 `checkpoints/`（PRD）和 `checkups/`（体检报告）混进"最近会话日志"。

### Step 1.5 · 读经验索引定向检索（2026-09-03 经验系统改造第一阶段立 · 堵召回断点）

```bash
cat ~/Documents/Claude/brain/permanent/经验索引.md
```
- 按 Step 2 识别的活跃项目，取该项目索引条目：**开放状态（🔄/⚠/⏳）优先**，列前 3-5 条（ID+标题一行），相关则按证据指针进 GOTCHAS 正文只读。
- 通用教训栏若含与当前任务类型相关的 G-X → 摘要提示一行。
- 摘要加一行「**经验召回**：{项目} 开放 {N} 条 · 已载 {M} 条」。
- 索引缺失 → 提示「⚠ 经验索引不存在（运行 brain/.tools/build_experience_index.py 重建）」，不阻塞。
- 本场采用任何经验/Gotchas 条目 → 结束前按五阶段回执 append `permanent/_consumption_receipts.jsonl`（见 Step 3.5）。

### Step 2 · 识别活跃项目

从日志的 `project:` frontmatter、文件名主题、或正文中提取最近活跃的项目名（DVA / 龙鱼五力 / 渊图 / O MY HTML / PEC / 海螺姑娘 / 司南 / 烛照九阴 / 白泽大宗 / 剑酒青丘）。

若识别到，读：
```
~/Documents/Claude/brain/{项目名}/architecture/系统概览.md
~/Documents/Claude/brain/{项目名}/architecture/决策记录.md
~/Documents/Claude/brain/{项目名}/GOTCHAS.md
```

**⚠ 系统概览缺失是已知状态**（8 个项目目录没有它，见 `brain/TODO.md`）——缺了就明确报一行「⚠ {项目}/architecture/系统概览.md 不存在」，**不建、不猜、不静默跳过**。

### Step 3 · 扫 TODO 顶部

读 `~/Documents/Claude/brain/TODO.md` 的"待办"段。

### Step 3.5 · 五阶段消费回执检查（2026-09-03 经验系统改造第一阶段立）

```bash
tail -5 ~/Documents/Claude/brain/permanent/_consumption_receipts.jsonl
```
- 有未闭回执（有 retrieved/selected 但无 consumer_verified/outcome_observed，且超 3 天）→ 摘要单列一行「⚠ 未闭回执 {N} 条」。
- 本场采用的每条经验，结束时按实际 append 一行（五态：retrieved→selected→encoded→consumer_verified→outcome_observed，填到实际到达的态；consumer_verified 必须来自消费端回读证据，不凭「写了就算」）。

### Step 4 · 输出结构化摘要

```
**上次工作**：{项目名} · {日期}

**经验召回**：{项目} 开放 {N} 条 · 已载 {M} 条（Step 1.5）

**关键决策**（最多 3 条）：
- ...

**遗留待办**（最多 5 条）：
- [ ] ...

**建议下一步**（3 条具体动作）：
1. ...
2. ...
3. ...

需要我从哪一项开始？
```

**若 Step 0.6 报了超期或异常，摘要开头单列一行**，别埋进正文——它是机制级问题，比任何单个待办都优先。

**git 待办直接贴命令块（2026-09-02 Doctor 立）**：摘要「建议下一步」凡涉及 git commit/push 待办——先实读 `.git` 纯文本核仓况（`.git/logs/HEAD` 尾部看末次 commit · `.git/refs/heads/` 与 `refs/remotes/` 对拍判 push · 工作区 `find -newermt <末次 commit 时间>` 扫未提交新文件）；已同步的**不再提**；确有待提交的**直接构造命令块贴出**（≥2 仓合并一个 code block 分段连发），不问「要不要贴」。

## 边界

- `logs/` 为空 → "brain 还没有会话日志。要不要我读 `permanent/项目总览.md` 给您看 8 个项目的整体状态？"
- 识别不到项目 → 只输出全局摘要，问 Doctor 想进入哪个项目
- **不**一次性读项目全部文档——只读 architecture/系统概览/决策记录/GOTCHAS
- 所有路径用绝对 `~/Documents/Claude/brain/...`
- Step 0 全局偏好每次起手必载，不因"上次读过"跳过（会话间不延续）
- resume 起手第一轮默认开声（语音链路可用时）；不可用静默跳过
- **Step 0.6 按自愈循环 F1 分臂**：F1a 只报告不动手；F1b 贴 S1 命令（Doctor 终端）——不代跑巡检脚本（沙箱读不到 live 树，跑不了）、不代 commit；白名单外修复动作一律只报告（白名单与 audit 要求见 `permanent/巡检自愈循环-loop-engineering.md`）
- **git 待办先核后贴、直接贴不问**（2026-09-02 Doctor 立）：先实读 .git 纯文本核仓况，已同步不提；有待提交直接贴命令块（多仓合一 code block 分段连发），不问「要不要贴」

## 相关

- `permanent/定时任务巡检机制.md`（Step 0.6 的完整设计与那个悖论）
- `permanent/巡检自愈循环-loop-engineering.md`（F1 分臂/白名单/audit——超期处置的现行条文）
- `.tools/scheduler_snapshot.py` · `permanent/_scheduler_snapshot.{json,md}`
- 周班 `scheduler-weekly-audit`（周日 20:00 PDT · 静默运行 · 异常才弹系统通知）

