#!/usr/bin/env python3
"""
transcript_search.py — 真相层检索（v2）

在 brain/chats/transcripts/**/*.jsonl.gz 里按关键词（默认不分大小写的子串）或正则检索。
- 日期过滤与显示一律按本机时区。
- 默认新的在前（--oldest-first 反过来）。
- 同一条消息出现在多个文件里（续接会话会复制历史）按 uid 去重，只报一次。
- 单个抽取件损坏时跳过并在 stderr 告警，不影响其余检索。

用法：
  transcript_search.py 关键词
  transcript_search.py 'G-X2[0-9]+' --regex
  transcript_search.py 关键词 --since 2026-11-01 --until 2026-11-19 --role user --kind text
  transcript_search.py 关键词 --source cowork3p --session 80ba8a3f --limit 20 --width 200
  transcript_search.py 关键词 --count
查无结果返回 0 条、退出码 0。
PRD：brain/logs/checkpoints/2026-11-19_真相层_PRD.md
"""
import argparse
import fnmatch
import gzip
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

DEFAULT_DST = Path(os.path.expanduser("~")) / "Documents" / "Claude" / "brain" / "chats" / "transcripts"


def local_dt(ts):
    if not ts:
        return ""
    try:
        return datetime.fromisoformat(ts.replace("Z", "+00:00")).astimezone().strftime("%Y-%m-%d %H:%M:%S")
    except Exception:
        return ts[:19]


def _header(p):
    try:
        with gzip.open(p, "rt", encoding="utf-8") as g:
            return json.loads(g.readline())
    except Exception:
        return None


def _sort_key(h, p, oldest_first):
    """新的在前：按会话最后一条时间排；旧的在前：按第一条时间排。读不了 header 的按文件名兜底。"""
    if not h:
        return p.name
    return (h.get("first_ts") if oldest_first else h.get("last_ts")) or p.name


def _load_records(p, oldest_first):
    try:
        with gzip.open(p, "rt", encoding="utf-8") as g:
            lines = g.readlines()
    except Exception as e:
        print(f"⚠ 抽取件读不了，已跳过：{p} · {e.__class__.__name__}", file=sys.stderr)
        return None
    recs = []
    for i, line in enumerate(lines):
        try:
            obj = json.loads(line)
        except Exception:
            continue
        if not (i == 0 and obj.get("type") == "header"):
            recs.append(obj)
    if not oldest_first:
        recs.reverse()
    return recs


def iter_files(root, oldest_first=False, since=None, until=None):
    """按会话时间排序逐个给出 (路径, header, 记录)。给了 since/until（本机日期）时，先看 header 的起止时间，
    整个会话落在范围外的不解压正文——检索只读窗口内的会话。"""
    items = []
    for p in Path(root).rglob("*.jsonl.gz"):
        h = _header(p)
        if h and (since or until):
            last, first = local_dt(h.get("last_ts"))[:10], local_dt(h.get("first_ts"))[:10]
            if since and last and last < since:
                continue
            if until and first and first > until:
                continue
        items.append((p, h))
    items.sort(key=lambda x: _sort_key(x[1], x[0], oldest_first), reverse=not oldest_first)
    for p, h in items:
        recs = _load_records(p, oldest_first)
        if recs is None:
            continue
        yield p, h or {}, recs


_NOTE_PATH = re.compile(r"(?:^|[/\\\s\"'`])(?:brain/)?(?:logs|permanent)/[^\s\"'`]*\.md")
_NOTE_TOOLS = {"Write", "Edit", "MultiEdit", "Read", "NotebookEdit", "Grep", "Glob"}


def _note_tool_ids(recs):
    """会话里读写 brain 笔记（logs/、permanent/ 下的 .md）的工具调用 id：Write/Edit/Read 的 file_path，或 Bash 命令里点到这些文件。"""
    ids = set()
    for r in recs:
        if r.get("kind") != "tool_use":
            continue
        t = r.get("text") or ""
        tool = r.get("tool") or ""
        if tool in _NOTE_TOOLS:
            m = re.search(r'"(?:file_path|path)"\s*:\s*"([^"]+)"', t)
            if m and re.search(r"brain/(?:logs|permanent)(?:/|$)", m.group(1)):
                ids.add(r.get("tool_use_id"))
        elif "bash" in tool.lower() and re.search(r"brain/(?:logs|permanent)(?:/|\b)", t):
            ids.add(r.get("tool_use_id"))  # Claude Code 的 Bash 与 Cowork 的 mcp__workspace__bash 都算；只认 brain 下的 logs/permanent
    ids.discard(None)
    return ids


def _path_tool_ids(recs, paths):
    """读写指定文件（路径子串）的工具调用 id：Write/Edit/Read 的 file_path、Bash 命令里点到它。"""
    ids = set()
    for r in recs:
        if r.get("kind") != "tool_use":
            continue
        t = r.get("text") or ""
        if any(x in t for x in paths):
            ids.add(r.get("tool_use_id"))
    ids.discard(None)
    return ids


def search(root, pattern, regex=False, since=None, until=None, role=None, kind=None,
           session=None, source=None, limit=50, width=160, oldest_first=False, exclude_notes=False, patterns=None,
           exclude_paths=None):
    pats = patterns or [pattern]
    rxs = [(pt, re.compile(pt if regex else re.escape(pt), re.IGNORECASE)) for pt in pats]
    hits, seen = [], set()
    for p, h, recs in iter_files(root, oldest_first, since, until):
        if source and not fnmatch.fnmatchcase(h.get("source") or "", source):
            continue
        if session and session not in (h.get("session_id") or "") and session not in (h.get("source_rel") or ""):
            continue
        skip_ids = _note_tool_ids(recs) if exclude_notes else set()
        if exclude_paths:
            skip_ids |= _path_tool_ids(recs, exclude_paths)
        for r in recs:
            if skip_ids and r.get("tool_use_id") in skip_ids:
                continue
            if exclude_paths and r.get("kind") == "tool_result" and any(x in (r.get("text") or "") for x in exclude_paths):
                continue  # Grep 等输出里带着这篇文件的路径，也是在复述它
            when = local_dt(r.get("ts"))
            day = when[:10]
            if since and day and day < since:
                continue
            if until and day and day > until:
                continue
            if role and r.get("role") != role:
                continue
            if kind and r.get("kind") != kind:
                continue
            text = r.get("text") or ""
            for pt, rx in rxs:
                m = rx.search(text)
                if not m:
                    continue
                uid = r.get("uid")
                key = (uid, pt)
                if uid:
                    if key in seen:
                        continue
                    seen.add(key)
                a = max(0, m.start() - width // 3)
                hits.append({"pattern": pt, "time": when, "session_id": h.get("session_id"), "source": h.get("source"),
                             "title": h.get("title"), "role": r.get("role"), "kind": r.get("kind"),
                             "tool": r.get("tool"), "queued": r.get("queued", False), "file": str(p),
                             "snippet": text[a:a + width].replace("\n", " ⏎ ")})
                if limit and len(hits) >= limit:
                    return hits
    return hits


def main(argv=None):
    ap = argparse.ArgumentParser(description="真相层检索")
    ap.add_argument("pattern", nargs="?", default=None)
    ap.add_argument("--patterns-file", help="每行一个检索词，一次扫描查多个（Dream 批量核对用）")
    ap.add_argument("--exclude-path", action="append", default=[], metavar="路径子串",
                    help="只排除读写这一篇文件的记录（工具调用、其结果、输出里带该路径的结果）；可重复。Dream 核对单篇日志时用")
    ap.add_argument("--exclude-notes", action="store_true",
                    help="排除读写 brain 笔记（logs/、permanent/ 下 .md）的工具调用及其结果，避免拿笔记自己当出处")
    ap.add_argument("--root", default=os.environ.get("TRANSCRIPT_DST", str(DEFAULT_DST)))
    ap.add_argument("--regex", action="store_true")
    ap.add_argument("--since", help="本机日期 YYYY-MM-DD（含）")
    ap.add_argument("--until", help="本机日期 YYYY-MM-DD（含）")
    ap.add_argument("--role", choices=["user", "assistant", "notification"])
    ap.add_argument("--kind", choices=["text", "tool_use", "tool_result"])
    ap.add_argument("--source", help="来源标签，支持通配：code / cowork / cowork3p / 'fuxi-*'")
    ap.add_argument("--session")
    ap.add_argument("--limit", type=int, default=50, help="0 = 不限")
    ap.add_argument("--width", type=int, default=160)
    ap.add_argument("--oldest-first", action="store_true")
    ap.add_argument("--count", action="store_true")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    if not Path(a.root).is_dir():
        print(f"❌ 真相层目录不存在：{a.root}（先跑 transcript_ingest.py）")
        return 2
    pats = None
    if a.patterns_file:
        try:
            pats = [l.strip() for l in Path(a.patterns_file).read_text(encoding="utf-8").splitlines() if l.strip()]
        except OSError as e:
            print(f"❌ 检索词文件读不了：{a.patterns_file} · {e.__class__.__name__}")
            return 2
        if a.pattern:
            pats.insert(0, a.pattern)
    if a.regex:
        for pt in (pats or [a.pattern] if a.pattern else []):
            try:
                re.compile(pt)
            except re.error as e:
                print(f"❌ 正则写坏了：{pt!r} · {e}")
                return 2
    if not a.pattern and not pats:
        print("❌ 需要检索词或 --patterns-file")
        return 2
    hits = search(a.root, a.pattern, a.regex, a.since, a.until, a.role, a.kind, a.session, a.source,
                  0 if a.count else a.limit, a.width, a.oldest_first, a.exclude_notes, pats,
                  a.exclude_path or None)
    if a.count:
        print(f"命中 {len(hits)} 条 · {len({h['session_id'] for h in hits})} 个会话")
        return 0
    for h in hits:
        if a.json:
            print(json.dumps(h, ensure_ascii=False))
        else:
            tag = f"{h['role']}/{h['kind']}" + (f"[{h['tool']}]" if h.get("tool") else "") + ("·插话" if h.get("queued") else "")
            print(f"{h['time']} | {h['source'] or '?'}:{(h['session_id'] or '')[:8]} | {tag} | {h['snippet']}")
    if not a.json:
        print(f"— 共 {len(hits)} 条" + ("（已达 --limit 上限）" if a.limit and len(hits) >= a.limit else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
