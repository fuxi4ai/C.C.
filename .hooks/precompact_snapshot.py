#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
brain PreCompact hook —— 上下文压缩前的工作状态快照

读 stdin(JSON: {session_id, transcript_path, cwd, hook_event_name, trigger}) →
在 Claude Code 压缩历史之前，把"我们刚才在做什么"写成一份确定性快照到
inbox/_auto/precompact-<时间>.md（append-only 暂存区），防止关键状态被压缩丢掉。
同时向 stdout 打印一行回执（会被注入到压缩后的上下文里）。

边界（对齐 brain 哲学）：
  · 只写 inbox/_auto/（暂存区），绝不写 logs/ 或 permanent/，绝不跑 git。
  · 内容是机器可得的事实（改动文件清单 / 最近意图），不做 LLM 总结。
  · fail-safe：任何异常静默 exit 0。
"""
import sys
import os
import json
import datetime

MAX_FILES = 40
MAX_PROMPTS = 4


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

    trigger = data.get("trigger", "?")          # manual / auto
    cwd = data.get("cwd", "")
    tpath = data.get("transcript_path", "")
    sid = (data.get("session_id", "") or "")[:8]

    here = os.path.dirname(os.path.abspath(__file__))
    brain = os.path.dirname(here)
    auto = os.path.join(brain, "inbox", "_auto")

    edits, prompts = _scan_transcript(tpath)

    now = datetime.datetime.now()
    stamp = now.strftime("%Y-%m-%d-%H%M%S")
    try:
        os.makedirs(auto, exist_ok=True)
    except Exception:
        sys.exit(0)

    fn = os.path.join(auto, f"precompact-{stamp}.md")
    body = []
    body.append("---")
    body.append(f"title: 压缩前快照 {stamp}")
    body.append("tags: [auto, precompact, snapshot]")
    body.append(f"created: {now.strftime('%Y-%m-%d')}")
    body.append("status: active")
    body.append("type: auto-snapshot")
    body.append("---")
    body.append("")
    body.append(f"# 压缩前工作状态快照 — {stamp}")
    body.append("")
    body.append(f"**触发**：PreCompact（{trigger}）  |  **会话**：{sid}")
    body.append(f"**工作目录**：{cwd}")
    if edits:
        body.append("")
        body.append(f"## 本会话改动的文件（{len(edits)}）")
        for f in list(edits)[:MAX_FILES]:
            body.append(f"- {f}")
    if prompts:
        body.append("")
        body.append("## 最近的用户意图（节选）")
        for p in prompts[-MAX_PROMPTS:]:
            body.append(f"- {p}")
    body.append("")
    body.append("> 自动生成 · 仅供恢复参考 · 可被 /consolidate 蒸馏或手动删除。")

    try:
        with open(fn, "w", encoding="utf-8") as f:
            f.write("\n".join(body) + "\n")
    except Exception:
        sys.exit(0)

    sys.stdout.write(
        f"📌 已在压缩前快照工作状态 → inbox/_auto/{os.path.basename(fn)}"
        f"（{len(edits)} 个改动文件）。如需完整恢复可读该文件或 /resume。\n"
    )


def _scan_transcript(tpath):
    """从 transcript JSONL 提取：改动文件集合 + 用户文本意图列表。"""
    edits = []
    seen = set()
    prompts = []
    if not tpath or not os.path.exists(tpath):
        return edits, prompts
    try:
        with open(tpath, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                except Exception:
                    continue
                msg = obj.get("message", obj) if isinstance(obj, dict) else {}
                role = (obj.get("type") if isinstance(obj, dict) else "") or (
                    msg.get("role", "") if isinstance(msg, dict) else ""
                )
                content = msg.get("content") if isinstance(msg, dict) else None
                if isinstance(content, str):
                    blocks = [{"type": "text", "text": content}]
                elif isinstance(content, list):
                    blocks = content
                else:
                    blocks = []
                for b in blocks:
                    if not isinstance(b, dict):
                        continue
                    bt = b.get("type")
                    if bt == "tool_use":
                        name = b.get("name", "")
                        inp = b.get("input", {}) or {}
                        fp = inp.get("file_path") or inp.get("path") or ""
                        if name in ("Edit", "Write", "MultiEdit", "NotebookEdit") and fp:
                            if fp not in seen:
                                seen.add(fp)
                                edits.append(fp)
                    elif bt == "text" and role == "user":
                        t = (b.get("text") or "").strip().replace("\n", " ")
                        if t and not t.startswith("<"):
                            prompts.append(t[:200])
    except Exception:
        pass
    return edits, prompts


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
    sys.exit(0)
