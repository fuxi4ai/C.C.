#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
brain SessionStart hook —— 轻量上下文自动加载（只读注入，零写入）

读 stdin(JSON: {session_id, transcript_path, cwd, hook_event_name, source}) →
向 stdout 打印一段【紧凑】的"上次工作"上下文。Claude Code 会在 exit 0 时把
stdout 注入到会话开头，于是你不必每次手动 /resume 也能恢复大致状态。

设计原则（对齐 brain 哲学）：
  · 只读：不写 logs/permanent/任何文件，不跑 git。
  · 节制：刻意保持小体积（视频下一集就是"token 经济学"），只给"指路牌"，
    完整交接仍由 /resume 这个 LLM skill 完成。
  · fail-safe：任何异常都静默 exit 0、不注入，绝不打断会话启动。

路径自解析：脚本位于 brain/.hooks/，brain 根目录 = 上一级，不写死 /Users/...
"""
import sys
import os
import json
import glob
import re

# 每类条目的上限（token 控制）
MAX_LOGS = 3
MAX_DRAFTS = 5
MAX_TODO = 6


def main():
    raw = ""
    try:
        if not sys.stdin.isatty():
            raw = sys.stdin.read()
    except Exception:
        raw = ""
    try:
        data = json.loads(raw) if raw.strip() else {}
    except Exception:
        data = {}
    source = data.get("source", "")  # startup / resume / clear / compact

    here = os.path.dirname(os.path.abspath(__file__))
    brain = os.path.dirname(here)               # .hooks/ 的上一级 = brain/
    logs_dir = os.path.join(brain, "logs")
    inbox_auto = os.path.join(brain, "inbox", "_auto")
    todo = os.path.join(brain, "TODO.md")

    out = []
    out.append("=== brain 自动上下文（SessionStart hook · 只读注入）===")
    if source:
        out.append(f"(触发来源: {source})")

    # 1) 最近 N 篇会话日志（只列标题，不读全文）
    logs = sorted(
        glob.glob(os.path.join(logs_dir, "*.md")),
        key=lambda p: _safe_mtime(p),
        reverse=True,
    )[:MAX_LOGS]
    if logs:
        out.append("最近会话日志：")
        for p in logs:
            title = _frontmatter_field(p, "title") or os.path.basename(p)
            out.append(f"  · {title}")
        proj = _frontmatter_field(logs[0], "project")
        if proj and proj.lower() not in ("", "null", "none"):
            out.append(
                f"活跃项目：{proj}（细读：说\"深入{proj}\"，或读 brain/{proj}/architecture/）"
            )
    else:
        out.append("（logs/ 暂无会话日志）")

    # 2) 未固化的自动草稿提醒（Stop / PreCompact hook 留下的安全网）
    drafts = sorted(glob.glob(os.path.join(inbox_auto, "*.md")))
    if drafts:
        out.append(
            f"⚠️ 有 {len(drafts)} 条未固化的自动草稿在 inbox/_auto/，"
            f"建议先 /save 或 /consolidate 再继续："
        )
        for d in drafts[:MAX_DRAFTS]:
            out.append(f"  · inbox/_auto/{os.path.basename(d)}")
        if len(drafts) > MAX_DRAFTS:
            out.append(f"  · …还有 {len(drafts) - MAX_DRAFTS} 条")

    # 3) TODO 顶部待办
    todo_items = _todo_head(todo, MAX_TODO)
    if todo_items:
        out.append("TODO（顶部）：")
        for t in todo_items:
            out.append(f"  {t}")

    out.append("提示：完整交接用 /resume；收工存档用 /save。")
    out.append("=== 上下文结束 ===")

    sys.stdout.write("\n".join(out) + "\n")


# ---------- helpers ----------

def _safe_mtime(p):
    try:
        return os.path.getmtime(p)
    except Exception:
        return 0


def _read(p, n=1500):
    try:
        with open(p, "r", encoding="utf-8", errors="ignore") as f:
            return f.read(n)
    except Exception:
        return ""


def _frontmatter_field(p, key):
    txt = _read(p, 1500)
    m = re.search(r"^---\s*(.*?)\s*---", txt, re.S | re.M)
    block = m.group(1) if m else txt
    mm = re.search(rf"^{re.escape(key)}\s*:\s*(.+)$", block, re.M)
    if not mm:
        return ""
    val = mm.group(1).strip().strip('"').strip("'")
    # tags 形如 [log, PEC] 时取不到 project，这里只处理标量字段
    return val


def _todo_head(p, maxn):
    txt = _read(p, 4000)
    out = []
    for ln in txt.splitlines():
        s = ln.strip()
        if s.startswith("- [ ]") or s.startswith("- [x]"):
            out.append(s)
            if len(out) >= maxn:
                break
    return out


if __name__ == "__main__":
    try:
        main()
    except Exception:
        # 永不打断会话启动
        pass
    sys.exit(0)
