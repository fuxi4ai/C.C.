#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""定时任务 · 四执行面现状快照（只读）

为什么有这个脚本
----------------
2026-08-01 一天之内，CC 关于定时任务的结论被推翻了三次：
  · 「backfill 周一 13:34 验四失败面」→ 班已改 14:30 且不再写库
  · 「双写者职责未理清」            → zhuzhao 当天已加单写者锁
  · 「launchd 有 2 个 job」          → 实为 3 个，第三个不在任何清单里
每一条都**有出处、看起来自洽**——因为它们都是从**日志**拼出来的，而日志是历史。
只要中间有一场没参与的会话动过 live 树，拼出来的图就是错的。

这与 2026-07-31 挖出的「Documents 死树」是同一个病的镜像：
  死树 = 记了但没人读；本病 = 读了，但读到的不是现在。

**根治思路不是让人记得更牢，是让「现状」可被一条命令拉出来。**
输出用**固定文件名**并纳入 git —— 于是「谁改了什么」不需要任何额外机制：
`git diff` 就是变更检测器，无论改动来自 Doctor、别的 CC，还是本人。

必须在 Mac 原生跑
-----------------
沙箱只挂 `~/Documents`，读不到 `~/Claude's workspace/`（live 树）与
`~/Library/LaunchAgents/`（launchd 装机位）。本脚本要一次拿全，只能在 Mac 上跑。

    python3 ~/Documents/Claude/brain/.tools/scheduler_snapshot.py

覆盖不到的一块（需 CC 补）
--------------------------
Cowork 班的 **cron 表达式**只有 `list_scheduled_tasks` 这个 MCP 工具能给，
脚本拿不到。快照里该字段留 `null`，由 CC 调工具后回填。
**这一块的缺失是显式的，不是静默的**——见输出里的 `_gaps`。

只读保证
--------
除自己的两个输出文件外，不写任何东西；不跑 git 子命令；不碰调度器。
`launchctl print` 是只读查询。

输出契约：**正常时一个字都不打印**
----------------------------------
巡检会退化——跑一个月后所有人都会习惯性略过那几行摘要（同 G-X119：
「两问的答案总是没问题」就是它变成套话的信号）。故：

    无异常 → **零输出**，exit 0
    有异常 → 异常清单写 stderr，exit 1
    -v/--verbose → 打印四面全摘要（人工排查时用）

**变化本身不算异常**，交给 `git diff` 报——脚本只报**结构性破损**，
两者分工不重叠。唯一的例外是「班消失」：它可能是误删，故对比上次快照并出声。
"""
import hashlib
import json
import os
import plistlib
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

HOME = Path.home()

LIVE_TREE = HOME / "Gateway-workspace" / "Scheduled"            # 2026-08-17 VV 五轮 P0 + Doctor 批：Scheduled 唯一真源＝Gateway 壳（反转 08-11「不接 GATEWAY_TREE」裁定——Kimi 已 21 班全迁·旧 Cowork 树冻结降级是镜像失真根源）。保护跟随 store：沙箱永不可读，仅 Mac 原生可扫
LEGACY_LIVE_TREE = HOME / "Claude's workspace" / "Scheduled"    # 旧 Cowork 树 · 2026-08-17 起只留名不再镜像（曾为 LIVE_TREE 真源）
GATEWAY_TREE = LIVE_TREE                                        # 别名 · 兼容旧引用（原「待接扫描面」观察条已随真源接线消解）
DEAD_TREE = HOME / "Documents/Claude/Scheduled"                # 旧第三方 store 位 · 2026-08-02 已迁 GATEWAY_TREE。正常＝不存在；再现＝异常（有壳/有人在此重建 store）
DEAD_ARCHIVED_GLOB = "_DEPRECATED_Scheduled_*"                 # 归档后的名字（可逆优先：改名不删）
LAUNCH_AGENTS = HOME / "Library/LaunchAgents"                  # launchd 装机位
OPS_DIRS = [                                                   # plist 源文件所在处
    HOME / "Documents/Claude/Projects/Financial/烛照九阴/ops",
]
OUT_JSON = HOME / "Documents/Claude/brain/permanent/_scheduler_snapshot.json"
OUT_MD = HOME / "Documents/Claude/brain/permanent/_scheduler_snapshot.md"
MIRROR_DIR = HOME / "Documents/Claude/brain/references/scheduled-live-mirror/live"  # 第三输出 · live 镜像（2026-08-02 Doctor 批）
ARTIFACTS_TREE = HOME / "Gateway-workspace" / "Artifacts"   # 2026-08-17 VV 四轮 P0：真源＝Gateway 壳（旧 "Claude's workspace" 树已冻结·EAL 停留 08-01·会回滚 mirror）。沙箱不可读、仅 Mac 原生可扫
LEGACY_ARTIFACTS_TREE = HOME / "Claude's workspace" / "Artifacts"  # 旧 Cowork 树 · 正常＝冻结不回滚用；再现异常由检测层另报（2026-08-17 留名）
ART_MIRROR = HOME / "Documents/Claude/brain/references/scheduled-live-mirror/artifacts"  # 第四输出（2026-08-02 Doctor 批）
ART_CAP = 1_000_000   # index.html >1M 只记 sha 不拷正文（zhuzhao/yuantu 两大件，备份责任在生成器）


def sha(p: Path) -> str:
    try:
        return hashlib.sha256(p.read_bytes()).hexdigest()[:12]
    except Exception:
        return "?"


def mtime(p: Path) -> str:
    try:
        return datetime.fromtimestamp(p.stat().st_mtime).strftime("%Y-%m-%d %H:%M")
    except Exception:
        return "?"


def frontmatter(md: Path) -> dict:
    """取 SKILL.md 的 YAML frontmatter 里的 name / description（不引入 yaml 依赖）。"""
    out = {}
    try:
        text = md.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return out
    m = re.match(r"^---\n(.*?)\n---", text, re.S)
    if not m:
        return out
    for line in m.group(1).splitlines():
        if ":" in line and not line.startswith(" "):
            k, v = line.split(":", 1)
            out[k.strip()] = v.strip()
    return out


# ───────────────────── 面 ① Cowork live 树 ─────────────────────

def scan_cowork():
    items = []
    if not LIVE_TREE.exists():
        return {"_error": f"live 树不存在：{LIVE_TREE}"}, items
    for d in sorted(LIVE_TREE.iterdir()):
        # `_archived` 是 Cowork 自己的归档目录，不是班；下划线开头一律跳过
        if not d.is_dir() or d.name.startswith((".", "_")):
            continue
        skill = d / "SKILL.md"
        fm = frontmatter(skill) if skill.exists() else {}
        desc = fm.get("description", "")
        items.append({
            "taskId": d.name,
            "has_skill": skill.exists(),
            "skill_mtime": mtime(skill) if skill.exists() else None,
            "skill_sha12": sha(skill) if skill.exists() else None,
            "skill_lines": len(skill.read_text(encoding="utf-8", errors="replace").splitlines())
                           if skill.exists() else None,
            "name": fm.get("name"),
            "desc_head": (desc[:110] + "…") if len(desc) > 110 else desc,
            "cron": None,          # ← 只有 list_scheduled_tasks 给得了，CC 回填
        })
    return {}, items


# ───────────────────── 面 ② Documents 死树 ─────────────────────

def scan_dead(cowork_ids):
    if not DEAD_TREE.exists():
        arch = sorted((HOME / "Documents/Claude").glob(DEAD_ARCHIVED_GLOB))
        return {"exists": False,
                "archived_as": [p.name for p in arch] or None,
                "note": "✅ 已归档（改名不删）" if arch else "✅ 不存在"}
    # ⚠ 与 scan_cowork 的过滤保持一致：`_archived` 是 Cowork 自己的归档目录、不是班。
    #   这里漏过滤会让它在差集里冒充「仅死树有」，产生 RED 级误报——
    #   2026-08-02 首次真机验证即栽在此（修 scan_cowork 时没扫同族，G-X111）。
    dirs = sorted(p.name for p in DEAD_TREE.iterdir()
                  if p.is_dir() and not p.name.startswith((".", "_")))
    both, only_dead = [], []
    for n in dirs:
        (both if n in cowork_ids else only_dead).append(n)
    diverged = []
    for n in both:
        a, b = DEAD_TREE / n / "SKILL.md", LIVE_TREE / n / "SKILL.md"
        if a.exists() and b.exists() and sha(a) != sha(b):
            diverged.append({"taskId": n, "dead_mtime": mtime(a), "live_mtime": mtime(b),
                             "dead_sha12": sha(a), "live_sha12": sha(b)})
    return {
        "exists": True, "path": str(DEAD_TREE), "dir_count": len(dirs),
        "also_in_live": both, "only_in_dead": only_dead,
        "content_diverged": diverged,
        "note": "⚠ 死树仍在：改动落这里不会进生产（2026-07-31 ERR）。"
                "内容分叉项尤其危险——看起来改了，其实没进调度器。",
    }


# ───────────────────── 面 ③ launchd ─────────────────────

def launchctl_loaded(label):
    """只读查询该 label 是否真的被 launchd 加载（装了文件 ≠ 已加载）。"""
    try:
        r = subprocess.run(["launchctl", "print", f"gui/{os.getuid()}/{label}"],
                           capture_output=True, text=True, timeout=10)
        if r.returncode != 0:
            return {"loaded": False, "detail": "未加载（launchctl print 非 0）"}
        st = re.search(r"state\s*=\s*(.+)", r.stdout)   # 「not running」有空格，勿用 \S+
        last = re.search(r"last exit code\s*=\s*(\S+)", r.stdout)
        return {"loaded": True, "state": st.group(1) if st else None,
                "last_exit_code": last.group(1) if last else None}
    except FileNotFoundError:
        return {"loaded": None, "detail": "launchctl 不可用（非 macOS？）"}
    except Exception as e:
        return {"loaded": None, "detail": f"{type(e).__name__}: {e}"}


def scan_launchd():
    # 源 plist（项目里维护的）
    sources = {}
    for od in OPS_DIRS:
        if not od.exists():
            continue
        for p in sorted(od.glob("*.plist")):
            try:
                d = plistlib.loads(p.read_bytes())
                label = d.get("Label", p.stem)
            except Exception:
                label = p.stem
            sources[label] = {"src_path": str(p), "src_sha12": sha(p), "src_mtime": mtime(p)}

    # 装机位
    installed = {}
    if LAUNCH_AGENTS.exists():
        for p in sorted(LAUNCH_AGENTS.glob("*.plist")):
            try:
                d = plistlib.loads(p.read_bytes())
            except Exception:
                d = {}
            label = d.get("Label", p.stem)
            sched = d.get("StartCalendarInterval")
            installed[label] = {
                "installed_path": str(p), "installed_sha12": sha(p),
                "installed_mtime": mtime(p),
                "program": (d.get("ProgramArguments") or [d.get("Program", "?")])[0],
                "schedule": sched,
                "run_at_load": d.get("RunAtLoad"),
                "runtime": launchctl_loaded(label),
            }

    # 一致性：源 ↔ 装机（这是 launchd 版的「双树分叉」）
    # ⚠ 只查**本项目自有**的 label。系统与第三方 Agent（Google Updater / 网盘 /
    #   com.apple.* 等）本就不该有项目内源文件，混进来只会淹没真信号。
    OURS = ("com.zhuzhao.", "com.globalpercent.", "com.baize.", "com.yuantu.")
    findings = []
    for label in sorted(set(sources) | set(installed)):
        if not label.startswith(OURS):
            continue
        s, i = sources.get(label), installed.get(label)
        if s and not i:
            findings.append({"label": label, "issue": "❌ 有源无装机——改了但没安装，永不会跑"})
        elif i and not s:
            findings.append({"label": label, "issue": "⚠ 有装机无源——在跑但项目里没有可维护的源文件"})
        elif s["src_sha12"] != i["installed_sha12"]:
            findings.append({"label": label,
                             "issue": f"❌ 源↔装机不一致（src {s['src_sha12']} vs installed {i['installed_sha12']}）"
                                      f"——改了源没重装，等同死树分叉"})
    return {"sources": sources, "installed": installed, "consistency": findings}


# ───────────────────── 面 ④ crontab ─────────────────────

def scan_cron():
    try:
        r = subprocess.run(["crontab", "-l"], capture_output=True, text=True, timeout=10)
        if r.returncode != 0:
            return {"entries": [], "note": "crontab 为空或未设置 ✅"}
        lines = [l for l in r.stdout.splitlines() if l.strip() and not l.strip().startswith("#")]
        return {"entries": lines, "note": "⚠ 非空——第四执行面已启用" if lines else "为空 ✅"}
    except Exception as e:
        return {"entries": None, "note": f"查不到：{type(e).__name__}"}


# ───────────────────── 面 ⑤ 挂载检查（2026-08-13 看门狗挂载治理）─────────────
MOUNT_MARKERS = [
    ("Database", ["Database/Market-Data", "Database/龙鱼-标的分析库", "Database/.env"]),
    ("烛照九阴", ["Claude/Projects/Financial/烛照九阴/config.py"]),
    ("剑酒青丘", ["Claude/Projects/Financial/剑酒青丘/strategies", "Claude/Projects/Financial/剑酒青丘/docs"]),
    ("白泽大宗", ["Claude/Projects/Financial/白泽大宗/configs"]),
    ("brain", ["Claude/brain/TODO.md"]),
]

def scan_mounts():
    """检查定时班关键目录是否挂载。挂载是会话级、非任务级固化（2026-08-13 治理结论），
    缺挂载则定时班阻塞或静默失败。探测挂载根：$HOME/mnt/Documents/ 或 /sessions/*/mnt/Documents/。"""
    import glob as _g
    roots = [HOME / "mnt" / "Documents"]
    roots += [Path(p) / "Documents" for p in _g.glob("/sessions/*/mnt")]
    found = {}
    for name, markers in MOUNT_MARKERS:
        found[name] = any((r / m).exists() for r in roots for m in markers)
    return found

# ───────────────────── 异常检测 ─────────────────────

def mirror_live_tree(dry=False):
    """第三输出 · live 树镜像 → brain（2026-08-02 Doctor 批 a 案）。
    章程不变：只读 live、只写 brain 内自有输出目录，不修、不 commit、不碰调度器。
    --delete 语义（镜像里删 live 已不存在的）不违反「不删文件」——镜像在 git 里，删除可见可回溯。
    dry=True（2026-08-17 VV 五轮要求）：只列将更新/移除清单，不落盘。"""
    import shutil
    if not LIVE_TREE.exists():
        return "live 树不可读，镜像跳过"
    live_files = {p.relative_to(LIVE_TREE) for p in LIVE_TREE.rglob("*") if p.is_file()}
    removed, copied = 0, 0
    would_remove, would_copy = [], []
    for p in [x for x in MIRROR_DIR.rglob("*") if x.is_file()]:
        if p.relative_to(MIRROR_DIR) not in live_files:
            if dry:
                would_remove.append(str(p.relative_to(MIRROR_DIR)))
            else:
                p.unlink(); removed += 1
    for rel in sorted(live_files):
        src, dst = LIVE_TREE / rel, MIRROR_DIR / rel
        if (not dst.exists()) or sha(src) != sha(dst):
            if dry:
                would_copy.append(str(rel))
            else:
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dst); copied += 1
    if dry:
        return f"[dry-run] live 镜像：将更新 {len(would_copy)} 件 · 将移除 {len(would_remove)} 件（不落盘）\n  更新: {sorted(would_copy)}\n  移除: {sorted(would_remove)}"
    MIRROR_DIR.mkdir(parents=True, exist_ok=True)
    return f"镜像已同步：{len(live_files)} 文件（更新 {copied} · 移除 {removed}）"


def mirror_artifacts(dry=False):
    """第四输出 · Artifacts 当前态镜像（2026-08-02 Doctor 批）。只收 index.html；
    versions/ 是 Cowork 自管回滚历史（实测占 Artifacts 总量 ~97%）、thumbnail 可再生，均不入。
    超 ART_CAP 只记清单行——变没变靠 sha 进 git diff，正文由生成器兜底。
    副产品 _artifacts_manifest.txt 使 Artifacts 成为本机制看得见的第六个执行面。
    dry=True（2026-08-17 VV 七轮要求）：只算计划，不 mkdir/copy/unlink/写清单。"""
    import shutil
    if not ARTIFACTS_TREE.exists():
        return "Artifacts 树不可读，跳过"
    lines, copied = [], 0
    would = []
    for d in sorted(ARTIFACTS_TREE.iterdir()):
        f = d / "index.html"
        if not d.is_dir() or not f.exists():
            continue
        size = f.stat().st_size
        mode = "copy" if size <= ART_CAP else "sha-only"
        lines.append(f"{d.name}\t{size}\t{sha(f)[:12]}\t{mode}\t{mtime(f)}")
        dst = ART_MIRROR / d.name / "index.html"
        if mode == "copy":
            if (not dst.exists()) or sha(f) != sha(dst):
                if dry:
                    would.append(f"copy {d.name}/index.html")
                else:
                    dst.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(f, dst); copied += 1
        elif dst.exists():
            if dry:
                would.append(f"sha-only 清正文 {d.name}/index.html")
            else:
                dst.unlink()   # 曾拷过后来超限：清正文，只留清单行
    manifest_text = ("# name\tbytes\tsha12\tmode\tmtime —— 由 scheduler_snapshot.py 周更；盘上有/清单无的幽灵靠本清单 diff 现形\n"
        + "\n".join(lines) + "\n")
    if dry:
        return f"[dry-run] Artifacts：{len(lines)} 个（将拷 {len(would)} · 清单将全量重写 {len(lines)} 行）——不落盘\n  {sorted(would)}"
    ART_MIRROR.mkdir(parents=True, exist_ok=True)
    (ART_MIRROR / "_artifacts_manifest.txt").write_text(manifest_text, encoding="utf-8")
    return f"Artifacts：{len(lines)} 个（拷 {copied} · 清单全量）"


def detect_anomalies(snap, prev):
    """只报**结构性破损**，不报「变化」（变化交给 git diff，不重复）。

    分两级：RED 必须出声；YELLOW 可能正常，默认不出声（-a 才报）。
    宁可少报也不误报——误报会让人忽略，忽略等于没有巡检。
    """
    red, yellow = [], []

    # ── 第一层自证：巡检自己停摆了没有 ──
    # 悖论：巡检定时任务的东西自己也是定时任务，它坏了谁发现？
    # 这一条让「漏跑」在下一次跑时自己喊出来。挡不住「永远停摆」——
    # 那一半由 /resume 检查快照新鲜度兜底（定时的东西用不定时的兜底）。
    if prev:
        ts = (prev.get("_meta") or {}).get("generated_at")
        if ts:
            try:
                prev_dt = datetime.fromisoformat(ts)
                gap = (datetime.now(prev_dt.tzinfo) - prev_dt).days
                if gap > 8:                      # 周班间隔 7 天，留 1 天余量
                    red.append(f"**巡检中断过 {gap} 天**（上次快照 {ts[:10]}）——周班停摆？")
            except Exception:
                red.append(f"上次快照的 generated_at 解析不了：{ts!r}")

    cw = snap["cowork_live"]
    if cw.get("_error"):
        red.append(f"Cowork live 树读不到：{cw['_error']}")
    for t in cw.get("tasks", []):
        if not t["has_skill"]:
            red.append(f"班 `{t['taskId']}` 没有 SKILL.md")

    # 班消失＝可能误删（新增不报，那是正常操作）
    if prev:
        was = {t["taskId"] for t in prev.get("cowork_live", {}).get("tasks", [])}
        now = {t["taskId"] for t in cw.get("tasks", [])}
        for gone in sorted(was - now):
            red.append(f"班 `{gone}` 消失了（上次快照还在）——误删？")

    d = snap["documents_dead_tree"]
    if d.get("content_diverged"):
        yellow.append(f"死树内容分叉 {len(d['content_diverged'])} 个："
                      + "、".join(x["taskId"] for x in d["content_diverged"])
                      + "（已知状态：live 均较新，归档待定）")
    if d.get("only_in_dead"):
        red.append(f"**仅死树有**：{d['only_in_dead']} —— 这些改动从未进过调度器")

    lg = snap["launchd"]
    for f in lg.get("consistency", []):
        red.append(f"launchd `{f['label']}`：{f['issue']}")
    for label, i in lg.get("installed", {}).items():
        if not label.startswith(("com.zhuzhao.", "com.globalpercent.",
                                 "com.baize.", "com.yuantu.")):
            continue
        rt = i.get("runtime") or {}
        if rt.get("loaded") is False:
            red.append(f"launchd `{label}` **未加载**——装了但不会跑")
        ec = rt.get("last_exit_code")
        if ec not in (None, "0"):
            red.append(f"launchd `{label}` 上次退出码 **{ec}**（非 0）")

    if snap["crontab"].get("entries"):
        yellow.append(f"crontab 非空（{len(snap['crontab']['entries'])} 条）"
                      "——第四执行面已启用，需入账")

    return red, yellow


# ───────────────────── 汇总 ─────────────────────

def main():
    import argparse
    ap = argparse.ArgumentParser(description="定时任务四执行面巡检（只读 · 正常静默）")
    ap.add_argument("-v", "--verbose", action="store_true", help="打印四面全摘要")
    ap.add_argument("-a", "--all", action="store_true", help="连 YELLOW 级也报")
    ap.add_argument("--dry-run", action="store_true", help="零写入：只打印 live/Artifacts 镜像计划与只读扫描摘要，不写 snapshot/mirror/manifest、不 mkdir/copy/unlink（2026-08-17 VV 七轮要求）")
    args = ap.parse_args()

    if args.dry_run:
        # 真零写入：先出计划，再退出——不触碰 OUT_JSON/OUT_MD/MIRROR_DIR/ART_MIRROR
        live_plan = mirror_live_tree(dry=True)
        art_plan = mirror_artifacts(dry=True)
        err, cowork = scan_cowork()
        print("=== scheduler_snapshot --dry-run（零写入）===")
        print(f"只读扫描：cowork {len(cowork)} 班（path={LIVE_TREE}）")
        print(live_plan)
        print(art_plan)
        print("未写 snapshot/mirror/manifest · 未 mkdir/copy/unlink")
        return

    # 读上次快照（必须在覆盖之前）——用于检测「班消失」
    prev = None
    if OUT_JSON.exists():
        try:
            prev = json.loads(OUT_JSON.read_text(encoding="utf-8"))
        except Exception:
            prev = None

    err, cowork = scan_cowork()
    ids = {c["taskId"] for c in cowork}
    snap = {
        "_meta": {
            "generated_at": datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"),
            "host": os.uname().nodename,
            "generator": "brain/.tools/scheduler_snapshot.py",
            "readonly": True,
        },
        "_gaps": [
            "Cowork 班的 cron 表达式脚本拿不到（只有 list_scheduled_tasks MCP 工具能给）"
            "——cowork[].cron 恒为 null，由 CC 回填。此缺失是显式的，勿当成「没有 cron」。",
            "通知策略 notifyOnCompletion 同理，list_scheduled_tasks 亦不返回（2026-07-30 实测）。",
        ],
        "cowork_live": {"path": str(LIVE_TREE), "count": len(cowork), "tasks": cowork, **err},
        "documents_dead_tree": scan_dead(ids),
        "launchd": scan_launchd(),
        "crontab": scan_cron(),
        "mounts": scan_mounts(),
    }

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(snap, ensure_ascii=False, indent=1, sort_keys=False),
                        encoding="utf-8")

    mirror_note = mirror_live_tree()
    art_note = mirror_artifacts()

    # ── 人读版 ──
    L = []
    L.append(f"# 定时任务 · 四执行面现状快照\n")
    L.append(f"> 由 `brain/.tools/scheduler_snapshot.py` 生成于 "
             f"{snap['_meta']['generated_at']}，**只读**。\n")
    L.append("> **本文件纳入 git；跑完 `git diff` 即知自上次快照以来什么变了** —— "
             "无论改动来自 Doctor、别的会话还是 CC 自己。\n")
    L.append(f"> 镜像步：{mirror_note} · {art_note}\n")

    L.append(f"\n## 面① Cowork live 树（{len(cowork)} 个）\n")
    L.append("| taskId | SKILL mtime | 行数 | sha | 描述 |")
    L.append("|---|---|---|---|---|")
    for c in cowork:
        L.append(f"| `{c['taskId']}` | {c['skill_mtime'] or '—'} | {c['skill_lines'] or '—'} "
                 f"| `{c['skill_sha12'] or '—'}` | {(c['desc_head'] or '').replace('|','/')} |")
    L.append("\n⚠ cron 列缺失：见 `_gaps`。")

    d = snap["documents_dead_tree"]
    L.append(f"\n## 面② Documents 死树\n")
    if not d.get("exists"):
        L.append(f"✅ {d.get('note')}")
    else:
        L.append(f"⚠ **仍在** `{d['path']}` · {d['dir_count']} 个目录")
        L.append(f"- 与 live 同名：{len(d['also_in_live'])} · 仅死树有：{d['only_in_dead'] or '无'}")
        if d["content_diverged"]:
            L.append(f"- ❌ **内容分叉 {len(d['content_diverged'])} 个**（改了看起来生效、实则没进调度器）：")
            for x in d["content_diverged"]:
                L.append(f"  - `{x['taskId']}` 死树 {x['dead_mtime']} vs live {x['live_mtime']}")
        else:
            L.append("- 无内容分叉")

    lg = snap["launchd"]
    L.append(f"\n## 面③ launchd（源 {len(lg['sources'])} · 装机 {len(lg['installed'])}）\n")
    L.append("| Label | 排期 | 已加载 | last exit | 装机 mtime |")
    L.append("|---|---|---|---|---|")
    for label, i in lg["installed"].items():
        sc = i.get("schedule")
        sc_s = json.dumps(sc, ensure_ascii=False) if sc else "—"
        rt = i.get("runtime") or {}
        L.append(f"| `{label}` | {sc_s} | {rt.get('loaded')} | {rt.get('last_exit_code','—')} "
                 f"| {i['installed_mtime']} |")
    if lg["consistency"]:
        L.append("\n**⚠ 源↔装机一致性问题：**")
        for f in lg["consistency"]:
            L.append(f"- `{f['label']}` — {f['issue']}")
    else:
        L.append("\n✅ 源与装机全部一致")

    cr = snap["crontab"]
    L.append(f"\n## 面④ crontab\n\n{cr['note']}")
    if cr.get("entries"):
        for e in cr["entries"]:
            L.append(f"- `{e}`")

    mt = snap["mounts"]
    L.append(f"\n## 面⑤ 挂载检查（2026-08-13 看门狗挂载治理）\n")
    missing = [k for k, ok in mt.items() if not ok]
    if not missing:
        L.append("✅ 关键目录全部挂载（Database/烛照九阴/剑酒青丘/白泽大宗/brain）")
    else:
        L.append(f"⚠ **缺挂载 {len(missing)} 个**：{'、'.join(missing)}——定时班跑前需补挂，否则阻塞/静默失败")

    OUT_MD.write_text("\n".join(L) + "\n", encoding="utf-8")

    # ── 输出契约：正常静默、异常出声 ──
    red, yellow = detect_anomalies(snap, prev)
    if red or (args.all and yellow):
        print("⚠ 定时任务巡检发现异常：", file=sys.stderr)
        for x in red:
            print(f"  🔴 {x}", file=sys.stderr)
        if args.all:
            for x in yellow:
                print(f"  🟡 {x}", file=sys.stderr)
        print(f"\n  详见 {OUT_MD}", file=sys.stderr)

    # ⚠ 只有 RED 才改退出码。🟡 是「已知且已判定无害」，让它把 exit code 染成 1
    #   等于把周班每周都变成失败——那是把告警训练成噪声的另一条路。
    if red and not args.verbose:
        sys.exit(1)

    if not args.verbose:
        sys.exit(0)          # ← 正常：零输出

    # 控制台摘要（仅 --verbose）
    print(f"✅ 快照已生成")
    print(f"   {OUT_JSON}")
    print(f"   {OUT_MD}")
    print(f"\n面① Cowork live : {len(cowork)} 个班")
    print(f"面② Documents死树: {'⚠ 仍在 ' + str(d.get('dir_count')) + ' 个目录' if d.get('exists') else '✅ 已清'}"
          + (f"（内容分叉 {len(d['content_diverged'])}）" if d.get("content_diverged") else ""))
    print(f"面③ launchd      : 源 {len(lg['sources'])} · 装机 {len(lg['installed'])}"
          + (f" · ⚠ 一致性问题 {len(lg['consistency'])} 处" if lg["consistency"] else " · ✅ 一致"))
    _mt_missing = [k for k, ok in snap["mounts"].items() if not ok]
    print(f"面⑤ 挂载          : {'⚠ 缺 ' + '、'.join(_mt_missing) if _mt_missing else '✅ 关键目录全挂载'}")
    print(f"面④ crontab      : {cr['note']}")
    if lg["consistency"]:
        print("\n⚠ launchd 源↔装机不一致（＝死树分叉的 launchd 版）：")
        for f in lg["consistency"]:
            print(f"   {f['label']}: {f['issue']}")


if __name__ == "__main__":
    main()
