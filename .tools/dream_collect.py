#!/usr/bin/env python3
"""
dream_collect.py — Dream 技能的收集器（v2 · 只读，--mark-* 只写 _dream_state.json）

列出待整理材料，供 brain-dream 技能逐项处理：
  · 待核对日志：brain/logs/ 下（不含 logs/dream、logs/checkpoints、logs/checkups、_bak）近 --max-days 天内改动过、
    且「内容哈希不在已处理台账里」的会话日志——台账按内容哈希记，跑一半中断或同日重跑都不会重复处理；
    日志后来被改动（哈希变了）才会再进来。
  · 窗口内的真相层（原始会话）会话：最后活动时间落在窗口内；默认不列 subagent（sidechain）会话，只计数。
  · 窗口内改动的 permanent 笔记（Step 4 写提案时参考）。
  · 真相层新鲜度：_state.json 的 last_run；解析失败单独报错，不混成「停摆」。
窗口：起点＝上次运行记录的 until；终点＝min(现在, 真相层 last_run)——晚于最近一次抽取的会话还没进真相层，
留给下一轮，避免核对时误判「查无出处」。首次或状态损坏取近 3 天；超过 --max-days 只取最近 max-days 天并写明跳过范围。

用法：
  dream_collect.py                               # 打印 JSON
  dream_collect.py --mark-processed <日志相对路径>...  # 每篇日志核对完就记一笔（可中断续跑）
  dream_collect.py --mark-run --until <ISO>      # 整轮跑完，按本轮窗口终点记运行
PRD：brain/logs/checkpoints/2026-11-19_Dream技能_PRD.md
"""
import argparse
import gzip
import hashlib
import json
import os
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

DEFAULT_BRAIN = Path(os.path.expanduser("~")) / "Documents" / "Claude" / "brain"
SKIP_LOG_DIRS = {"dream", "checkpoints", "checkups", "_bak"}


def _now():
    return datetime.now(timezone.utc)


def _parse(ts):
    """ISO 时间 → aware datetime。兼容 'Z' 与 '-0800' 这类不带冒号的时区（Python 3.9 的 fromisoformat 不认）。"""
    if not ts:
        return None
    s = str(ts).strip().replace("Z", "+00:00")
    s = re.sub(r"([+-]\d{2})(\d{2})$", r"\1:\2", s)
    s = re.sub(r"\.(\d{1,6})(?=[+-]\d{2}:\d{2}$|$)", lambda m: "." + m.group(1).ljust(6, "0"), s)  # Python 3.9 只认 3 或 6 位小数
    try:
        d = datetime.fromisoformat(s)
    except ValueError:
        return None
    return d if d.tzinfo else d.replace(tzinfo=timezone.utc)


def _sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load_state(brain):
    p = Path(brain) / "permanent" / "_dream_state.json"
    if not p.exists():
        return {}, "首次运行（无运行状态），按近 3 天建窗口"
    try:
        st = json.loads(p.read_text(encoding="utf-8"))
        if not isinstance(st, dict):
            raise ValueError
        return st, None
    except Exception:
        return {}, "运行状态文件损坏，按近 3 天重建窗口（已处理台账丢失，近 max-days 天的日志会重新核对）"


def save_state(brain, st):
    p = Path(brain) / "permanent" / "_dream_state.json"
    tmp = p.with_name(f"_dream_state.json.{os.getpid()}.tmp")
    tmp.write_text(json.dumps(st, ensure_ascii=False, indent=1, sort_keys=True), encoding="utf-8")
    os.replace(tmp, p)


def truth_layer(brain, now, stale_hours):
    root = Path(brain) / "chats" / "transcripts"
    info = {"root": str(root), "last_run": None, "stale_hours": None, "stale": True, "error": None}
    st = root / "_state.json"
    if not st.exists():
        info["error"] = "真相层状态文件不存在"
        return info
    try:
        raw = json.loads(st.read_text(encoding="utf-8")).get("last_run")
    except Exception:
        info["error"] = "真相层状态文件读不了"
        return info
    lr = _parse(raw)
    if lr is None:
        info["error"] = f"真相层 last_run 解析失败：{raw!r}"
        return info
    info["size_mb"] = round(sum(f.stat().st_size for f in root.rglob("*") if f.is_file()) / 1048576, 1)
    info["over_archive_threshold"] = info["size_mb"] >= 2048  # Doctor 2026-11-20：超过 2GB 归档至 fuxi-station
    info["last_run"] = lr.isoformat()
    info["stale_hours"] = round((now - lr).total_seconds() / 3600, 1)
    info["stale"] = info["stale_hours"] > stale_hours
    return info


def sessions(brain, since, until, include_sidechain=False):
    root = Path(brain) / "chats" / "transcripts"
    out, side, unreadable = [], 0, []
    for p in sorted(root.rglob("*.jsonl.gz")) if root.is_dir() else []:
        try:
            with gzip.open(p, "rt", encoding="utf-8") as g:
                h = json.loads(g.readline())
        except Exception:
            unreadable.append(str(p.relative_to(root)))
            continue
        last = _parse(h.get("last_ts"))
        if last is None or not (since <= last <= until):
            continue
        if h.get("sidechain") and not include_sidechain:
            side += 1
            continue
        out.append({"file": str(p.relative_to(root)), "source": h.get("source"), "session_id": h.get("session_id"),
                    "title": h.get("title"), "first_ts": h.get("first_ts"), "last_ts": h.get("last_ts"),
                    "counts": h.get("counts")})
    out.sort(key=lambda x: x.get("last_ts") or "")
    return out, side, unreadable


def _log_day(rel, mtime):
    """日志的「事情发生日」：文件名里的 YYYY-MM-DD 与修改时间取较早者。"""
    m = re.search(r"(20\d{2}-\d{2}-\d{2})", Path(rel).name)
    d = mtime
    if m:
        try:
            nd = datetime.strptime(m.group(1), "%Y-%m-%d").astimezone()  # 文件名里的日期是本机日期，按本机零点算
            d = min(d, nd)
        except ValueError:
            pass
    return d


def pending_logs(brain, processed, now, max_days):
    base = Path(brain) / "logs"
    cutoff = now - timedelta(days=max_days)
    out = []
    for p in base.rglob("*.md") if base.is_dir() else []:
        rel = p.relative_to(base)
        if SKIP_LOG_DIRS & set(rel.parts[:-1]):
            continue
        try:
            m = datetime.fromtimestamp(p.stat().st_mtime, timezone.utc)
        except OSError:
            continue
        if m < cutoff:
            continue
        sha = _sha(p)
        key = str(rel)
        if processed.get(key) == sha:
            continue
        out.append({"path": key, "mtime": m.isoformat(), "sha256": sha, "seen_before": key in processed,
                    # 检索出处的起点：按这篇日志自己的日期往前 3 天，不用本轮窗口（积压日志的会话早于窗口）
                    "search_since": (_log_day(key, m) - timedelta(days=3)).astimezone().strftime("%Y-%m-%d"),
                    # 本轮不处理，下一轮就会超出 max-days 退出待办
                    "expiring": m < cutoff + timedelta(days=1)})
    return sorted(out, key=lambda x: x["mtime"], reverse=True)  # 新的在前


def changed_permanent(brain, since, until):
    base = Path(brain) / "permanent"
    out = []
    for p in base.rglob("*.md") if base.is_dir() else []:
        rel = p.relative_to(base)
        if "_bak" in rel.parts:
            continue
        m = datetime.fromtimestamp(p.stat().st_mtime, timezone.utc)
        if since <= m <= until:
            out.append({"path": str(rel), "mtime": m.isoformat()})
    return sorted(out, key=lambda x: x["mtime"])


def collect(brain, max_days=7, stale_hours=48, now=None, include_sidechain=False):
    now = now or _now()
    brain = Path(brain)
    st, note = load_state(brain)
    tl = truth_layer(brain, now, stale_hours)
    since = _parse(st.get("last_until")) or (now - timedelta(days=3))
    skipped = None
    if now - since > timedelta(days=max_days):
        skipped = {"from": since.isoformat(), "to": (now - timedelta(days=max_days)).isoformat()}
        since = now - timedelta(days=max_days)
    tl_last = _parse(tl["last_run"])
    until = min(now, tl_last) if tl_last else now
    if until < since:  # 真相层还没追上上次窗口：本轮会话窗口为空，等抽取补上后再算
        until = since
    sess, side, unreadable = sessions(brain, since, until, include_sidechain)
    return {
        "generated_at": now.isoformat(),
        "first_run": "processed" not in st and "baseline_at" not in st,
        "window": {"since": since.isoformat(), "until": until.isoformat(), "skipped": skipped, "note": note,
                   "capped_at_truth_layer": bool(tl_last and until == tl_last)},
        "truth_layer": tl,
        "sessions": sess,
        "sidechain_sessions": side,
        "unreadable": unreadable,
        "pending_logs": [dict(x, after_truth_layer=bool(tl_last and _parse(x["mtime"]) > tl_last))
                         for x in pending_logs(brain, st.get("processed", {}), now, max_days)],
        "permanent_changed": changed_permanent(brain, since, until),
    }


def mark_processed(brain, rels):
    st, _ = load_state(brain)
    proc = st.setdefault("processed", {})
    base = Path(brain) / "logs"
    done = []
    for r in rels:
        p = base / r
        if p.is_file():
            proc[r] = _sha(p)
            done.append(r)
    save_state(brain, st)
    return done


def baseline(brain, older_than_days, now=None):
    """首轮把较早的积压日志记为基线（不核对），避免几十篇积压挤爆预算、又在 max-days 后静默过期。"""
    now = now or _now()
    st, _ = load_state(brain)
    proc = st.setdefault("processed", {})
    base = Path(brain) / "logs"
    cutoff = now - timedelta(days=older_than_days)
    done = []
    for p in base.rglob("*.md") if base.is_dir() else []:
        rel = p.relative_to(base)
        if SKIP_LOG_DIRS & set(rel.parts[:-1]):
            continue
        if datetime.fromtimestamp(p.stat().st_mtime, timezone.utc) < cutoff and str(rel) not in proc:
            proc[str(rel)] = _sha(p)
            done.append(str(rel))
    st["baseline_at"] = now.isoformat()
    save_state(brain, st)
    return done


def mark_run(brain, until, now=None):
    now = now or _now()
    u = _parse(until)
    if u is None:
        raise SystemExit(f"--until 解析失败：{until!r}")
    st, _ = load_state(brain)
    st["last_until"] = u.isoformat()
    st["last_run"] = now.isoformat()
    save_state(brain, st)
    return st


def main(argv=None):
    ap = argparse.ArgumentParser(description="Dream 收集器")
    ap.add_argument("--brain", default=os.environ.get("BRAIN_ROOT", str(DEFAULT_BRAIN)))
    ap.add_argument("--max-days", type=int, default=7)
    ap.add_argument("--stale-hours", type=float, default=48)
    ap.add_argument("--include-sidechain", action="store_true")
    ap.add_argument("--mark-processed", nargs="+", metavar="日志相对路径")
    ap.add_argument("--mark-run", action="store_true")
    ap.add_argument("--until", help="--mark-run 时必填：本轮 window.until")
    ap.add_argument("--baseline-older-than", type=float, metavar="天",
                    help="首轮用：把修改时间早于 N 天的待核对日志记为基线（不核对）")
    a = ap.parse_args(argv)
    if not Path(a.brain).is_dir():
        print(json.dumps({"error": f"brain 目录不存在：{a.brain}"}, ensure_ascii=False))
        return 2
    if a.baseline_older_than is not None:
        done = baseline(a.brain, a.baseline_older_than)
        print(json.dumps({"baselined": len(done)}, ensure_ascii=False))
        return 0
    if a.mark_processed:
        print(json.dumps({"processed": mark_processed(a.brain, a.mark_processed)}, ensure_ascii=False))
        return 0
    if a.mark_run:
        if not a.until:
            print(json.dumps({"error": "--mark-run 需要 --until（本轮 window.until）"}, ensure_ascii=False))
            return 2
        st = mark_run(a.brain, a.until)
        print(json.dumps({"last_until": st["last_until"], "last_run": st["last_run"]}, ensure_ascii=False))
        return 0
    print(json.dumps(collect(a.brain, a.max_days, a.stale_hours, include_sidechain=a.include_sidechain),
                     ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
