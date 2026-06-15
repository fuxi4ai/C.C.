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


# ── 4 库新鲜度巡检（PRD 2026-06-15）──────────────────────────────
# 信号源 Doctor 锁定（2026-06-15）：路径相对 Database/ 根
DB_FRESHNESS_SOURCES = [
    {"name": "烛照九阴-复盘", "type": "mtime",
     "path": "烛照九阴/recap.db", "threshold_hours": 30},
    {"name": "剑酒青丘-行情", "type": "mtime",
     "path": "Market-Data/market_data.db", "threshold_hours": 50},
    {"name": "白泽大宗-商品", "type": "ingest_meta",
     "path": "宏观-大宗商品/business_breakdown.db", "threshold_hours": 30},
    {"name": "DVA-视频", "type": "watchlist",
     "path": "Douyin/DVA-Database/indexes/watchlist.json", "threshold_hours": 168},
]

CST = timezone(timedelta(hours=8))


def _parse_ts(s):
    """解析时间戳→aware UTC datetime。结尾 Z=UTC；带 offset 用之；naive 视作 GMT+8。失败返回 None。"""
    if not s or not isinstance(s, str):
        return None
    s = s.strip()
    try:
        if s.endswith("Z"):
            return datetime.fromisoformat(s[:-1]).replace(tzinfo=timezone.utc)
        dt = datetime.fromisoformat(s)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=CST)
        return dt.astimezone(timezone.utc)
    except ValueError:
        m = DATE_RE.search(s)
        if m:
            return datetime.fromisoformat(m.group(1)).replace(tzinfo=CST).astimezone(timezone.utc)
        return None


def db_freshness(db_root, now_utc):
    """对 4 库取最新更新时间 → [{name,path,last_update,age_hours,threshold_hours,stale,detail}]。
    两类信号：mtime（文件本体）/ ingest_meta（max last_success_at）/ watchlist（enabled 作者 max lastUpdatedAt）。
    缺失或读取异常一律优雅降级为 last_update=None、stale=False（绝不误报红、绝不编数）。"""
    out = []
    for cfg in DB_FRESHNESS_SOURCES:
        p = db_root / cfg["path"]
        last_utc, detail = None, ""
        try:
            if not p.exists():
                detail = "路径缺失"
            elif cfg["type"] == "mtime":
                last_utc = datetime.fromtimestamp(p.stat().st_mtime, timezone.utc)
                detail = "文件 mtime"
            elif cfg["type"] == "ingest_meta":
                import sqlite3
                con = sqlite3.connect(f"file:{p}?mode=ro", uri=True)
                try:
                    rows = con.execute(
                        "SELECT last_success_at, last_status FROM ingest_meta").fetchall()
                finally:
                    con.close()
                ts = [t for t in (_parse_ts(r[0]) for r in rows) if t]
                if ts:
                    last_utc = max(ts)
                n_ok = sum(1 for r in rows if (r[1] or "").lower() == "ok")
                detail = f"{len(rows)}源·{n_ok}ok"
            elif cfg["type"] == "watchlist":
                data = json.loads(p.read_text(encoding="utf-8", errors="ignore"))
                authors = [a for a in data.get("authors", []) if a.get("enabled")]
                ts = [t for t in (_parse_ts(a.get("lastUpdatedAt")) for a in authors) if t]
                if ts:
                    last_utc = max(ts)
                detail = f"{len(authors)}作者" + ("·未跑" if not ts else "")
        except Exception as e:  # noqa: BLE001 — 任何异常都降级，不让单库拖垮整张快照
            detail = "读取异常:" + str(e)[:40]

        if last_utc is not None:
            age_h = round((now_utc - last_utc).total_seconds() / 3600, 1)
            stale = age_h > cfg["threshold_hours"]
            last_iso = last_utc.astimezone(CST).strftime("%Y-%m-%dT%H:%M:%S+08:00")
        else:
            age_h, stale, last_iso = None, False, None

        out.append({
            "name": cfg["name"], "path": cfg["path"],
            "last_update": last_iso, "age_hours": age_h,
            "threshold_hours": cfg["threshold_hours"], "stale": stale,
            "detail": detail,
        })
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=None)
    ap.add_argument("--db-root", default=None, help="Database/ 根，默认 brain 上两级的 Documents/Database")
    args = ap.parse_args()
    root = Path(args.root) if args.root else Path(__file__).resolve().parent.parent
    db_root = Path(args.db_root) if args.db_root else (root.parent.parent / "Database")

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

    now_utc = datetime.now(timezone.utc)
    now = now_utc.astimezone(CST)
    print(json.dumps({
        "timestamp": now_utc.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "local_time": now.strftime("%Y-%m-%d %H:%M") + " (GMT+8)",
        "notes": notes, "todos": total_todos, "dangling": dangling,
        "agents": agents, "projects": projects,
        "logs": [p.stem for p in log_files[:7]],
        "agentlogs": [e[1] for e in agent_log_entries[:3]],
        "toptodos": toptodos,
        "db_freshness": db_freshness(db_root, now_utc),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
