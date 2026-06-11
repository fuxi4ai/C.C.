#!/usr/bin/env python3
"""dashboard-snapshot.py — 为 Brain Vault Dashboard artifact 生成 snapshot JSON。

用法：python3 dashboard-snapshot.py [--root BRAIN_ROOT]
输出：stdout 打印 JSON（喂给 artifact 的 <script id="snapshot-data">）

规则沿袭 2026-05-15 治理决议：
- TODO 计数排除 logs/templates/references/chats/.skills/.index
- GOTCHAS 严格匹配 ^## \[ERR-[0-9]（排除模板示例）
- 悬空 wikilink 调 build-backlinks.py（其内部已跳过 logs/chats）
- 项目最后活跃：max(日志, 正文**最后更新**, frontmatter updated)，标注来源
维护：CC。落点：brain/.tools/dashboard-snapshot.py
"""
import argparse, json, re, subprocess, sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

EXCLUDE_TOP = {"agents", "chats", "fleeting", "graphify", "inbox", "logs",
               "permanent", "references", "templates", "白泽大宗", "烛照九阴"}
TODO_EXCLUDE_PARTS = {"logs", "templates", "references", "chats", ".skills", ".index", ".tools"}
DATE_RE = re.compile(r"(\d{4}-\d{2}-\d{2})")

AGENT_PROFILES = [
    {"glyph": "🦌", "name": "白泽", "nick": "小白", "rank": "大哥", "color": "#2563eb",
     "persona": "风度翩翩 · 雅言 · 敬称“老师”", "duty": "宏观线 — 白泽观星 · 白泽大宗", "call": "唤名：白泽 / 小白"},
    {"glyph": "🐉", "name": "烛阴", "nick": "九儿", "rank": "二姐", "color": "#dc2626",
     "persona": "温柔可爱 · 亲昵“哥哥” · 自称九儿", "duty": "复盘线 — 烛照九阴 · 新闻模块", "call": "唤名：烛阴 / 九儿"},
    {"glyph": "🌱", "name": "句芒", "nick": "芒芒", "rank": "三妹", "color": "#16a34a",
     "persona": "活泼俏皮 · 亲昵“哥哥”", "duty": "行情/量化线 — 技术工具 + 审查 + 记忆守护 + Market-Data", "call": "唤名：句芒 / 芒芒"},
    {"glyph": "🪔", "name": "C.C.", "nick": "守灶人", "rank": "老幺", "color": "#d97706",
     "persona": "务实温和 · 敬称“老师” · 守 brain + 调度兄姐", "duty": "非金融 + 开发 — PEC · 渊图 · 龙鱼五力 · 星空 · 数灵转移", "call": "本机 · 全局 logs/"},
]


def latest_date_in_name(paths):
    best = None
    for p in paths:
        m = DATE_RE.search(p.name)
        if m and (best is None or m.group(1) > best):
            best = m.group(1)
    return best


def project_last_active(root, proj, log_files):
    candidates = []  # (date, src)
    # 1) 日志：文件名含项目名，或 frontmatter project: 含项目名
    for lf in log_files:
        hit = proj in lf.name
        if not hit:
            try:
                head = lf.read_text(encoding="utf-8", errors="ignore")[:500]
                hit = re.search(r"^project:.*" + re.escape(proj), head, re.M) is not None
            except OSError:
                hit = False
        if hit:
            m = DATE_RE.search(lf.name)
            if m:
                candidates.append((m.group(1), "日志"))
    # 2) 正文 **最后更新** / 最后活跃 / 最后工作（系统概览）
    overview = root / proj / "architecture" / "系统概览.md"
    texts = []
    if overview.exists():
        texts.append(overview)
    stub = root / proj / f"{proj}.md"
    if stub.exists():
        texts.append(stub)
    for t in texts:
        try:
            body = t.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        m = re.search(r"\*\*(?:最后更新|最后活跃|最后工作)\*\*[：:]\s*(\d{4}-\d{2}-\d{2})", body)
        if m:
            candidates.append((m.group(1), "正文"))
        m = re.search(r"^updated:\s*(\d{4}-\d{2}-\d{2})", body, re.M)
        if m:
            candidates.append((m.group(1), "frontmatter"))
    if not candidates:
        return None, None
    candidates.sort(key=lambda c: c[0], reverse=True)
    return candidates[0]


def count_todos(path, exclude_parts):
    n, items = 0, []
    for md in path.rglob("*.md"):
        if any(part in exclude_parts for part in md.relative_to(path).parts):
            continue
        try:
            body = md.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for line in body.splitlines():
            s = line.strip()
            if s.startswith("- [ ]"):
                n += 1
                items.append((md.stem, s[5:].strip()))
    return n, items


def count_gotchas(root, proj):
    n = 0
    for gp in [root / proj / "GOTCHAS.md",
               root / proj / "architecture" / "GOTCHAS.md",
               root / proj / "architecture" / "已知坑.md"]:
        if gp.exists():
            try:
                n += len(re.findall(r"^## \[ERR-[0-9]", gp.read_text(encoding="utf-8", errors="ignore"), re.M))
            except OSError:
                pass
    return n


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=None)
    args = ap.parse_args()
    root = Path(args.root) if args.root else Path(__file__).resolve().parent.parent

    # 悬空 wikilink + 总笔记（复用 build-backlinks.py，只写 .index/）
    notes, dangling = -1, -1
    try:
        out = subprocess.run([sys.executable, str(root / ".tools" / "build-backlinks.py"), "--root", str(root)],
                             capture_output=True, text=True, timeout=120).stdout
        m = re.search(r"总笔记[：:]\s*(\d+)", out)
        if m: notes = int(m.group(1))
        m = re.search(r"悬空链接[：:]\s*(\d+)", out)
        if m: dangling = int(m.group(1))
    except Exception:
        pass
    if notes < 0:
        notes = sum(1 for _ in root.rglob("*.md"))

    logs_dir = root / "logs"
    log_files = sorted([p for p in logs_dir.glob("*.md")], key=lambda p: p.name, reverse=True)

    # 项目：顶层目录（带 stub 或 architecture），排除基础设施与数灵金融线
    projects = []
    for d in sorted(root.iterdir()):
        if not d.is_dir() or d.name.startswith(".") or d.name in EXCLUDE_TOP:
            continue
        if not ((d / f"{d.name}.md").exists() or (d / "architecture").is_dir()):
            continue
        last, src = project_last_active(root, d.name, log_files)
        tn, _ = count_todos(d, TODO_EXCLUDE_PARTS)
        projects.append({"name": d.name, "last": last, "src": src,
                         "todos": tn, "gotchas": count_gotchas(root, d.name)})
    projects.sort(key=lambda p: p["last"] or "0000", reverse=True)

    # 全局 TODO（项目 + permanent + inbox + TODO.md）
    total_todos, todo_items = count_todos(root, TODO_EXCLUDE_PARTS | {"agents"})
    toptodos = [{"src": src, "text": txt[:90]} for src, txt in todo_items[:8]]

    # 数灵
    agents = []
    agent_log_entries = []
    for prof in AGENT_PROFILES:
        a = dict(prof)
        if a["name"] == "C.C.":
            a["logs"] = None
            a["last"] = latest_date_in_name(log_files[:1])
        else:
            adir = root / "agents" / a["name"] / "logs"
            afiles = sorted(adir.glob("*.md"), key=lambda p: p.name, reverse=True) if adir.exists() else []
            a["logs"] = len(afiles)
            a["last"] = latest_date_in_name(afiles)
            for f in afiles[:3]:
                agent_log_entries.append((f.name, a["name"] + " · " + f.stem))
        agents.append(a)
    agent_log_entries.sort(reverse=True)

    now = datetime.now(timezone(timedelta(hours=8)))
    print(json.dumps({
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "local_time": now.strftime("%Y-%m-%d %H:%M") + " (GMT+8)",
        "notes": notes, "todos": total_todos, "dangling": dangling,
        "agents": agents, "projects": projects,
        "logs": [p.stem for p in log_files[:7]],
        "agentlogs": [e[1] for e in agent_log_entries[:3]],
        "toptodos": toptodos,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
