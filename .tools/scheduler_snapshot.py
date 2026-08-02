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

LIVE_TREE = HOME / "Claude's workspace" / "Scheduled"          # Cowork 调度器真读的树
DEAD_TREE = HOME / "Documents/Claude/Scheduled"                # 历史遗留，调度器不读
DEAD_ARCHIVED_GLOB = "_DEPRECATED_Scheduled_*"                 # 归档后的名字（可逆优先：改名不删）
LAUNCH_AGENTS = HOME / "Library/LaunchAgents"                  # launchd 装机位
OPS_DIRS = [                                                   # plist 源文件所在处
    HOME / "Documents/Claude/Projects/Financial/烛照九阴/ops",
]
OUT_JSON = HOME / "Documents/Claude/brain/permanent/_scheduler_snapshot.json"
OUT_MD = HOME / "Documents/Claude/brain/permanent/_scheduler_snapshot.md"


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
    dirs = sorted(p.name for p in DEAD_TREE.iterdir() if p.is_dir())
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


# ───────────────────── 汇总 ─────────────────────

def main():
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
    }

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(snap, ensure_ascii=False, indent=1, sort_keys=False),
                        encoding="utf-8")

    # ── 人读版 ──
    L = []
    L.append(f"# 定时任务 · 四执行面现状快照\n")
    L.append(f"> 由 `brain/.tools/scheduler_snapshot.py` 生成于 "
             f"{snap['_meta']['generated_at']}，**只读**。\n")
    L.append("> **本文件纳入 git；跑完 `git diff` 即知自上次快照以来什么变了** —— "
             "无论改动来自 Doctor、别的会话还是 CC 自己。\n")

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

    OUT_MD.write_text("\n".join(L) + "\n", encoding="utf-8")

    # 控制台摘要
    print(f"✅ 快照已生成")
    print(f"   {OUT_JSON}")
    print(f"   {OUT_MD}")
    print(f"\n面① Cowork live : {len(cowork)} 个班")
    print(f"面② Documents死树: {'⚠ 仍在 ' + str(d.get('dir_count')) + ' 个目录' if d.get('exists') else '✅ 已清'}"
          + (f"（内容分叉 {len(d['content_diverged'])}）" if d.get("content_diverged") else ""))
    print(f"面③ launchd      : 源 {len(lg['sources'])} · 装机 {len(lg['installed'])}"
          + (f" · ⚠ 一致性问题 {len(lg['consistency'])} 处" if lg["consistency"] else " · ✅ 一致"))
    print(f"面④ crontab      : {cr['note']}")
    if lg["consistency"]:
        print("\n⚠ launchd 源↔装机不一致（＝死树分叉的 launchd 版）：")
        for f in lg["consistency"]:
            print(f"   {f['label']}: {f['issue']}")


if __name__ == "__main__":
    main()
