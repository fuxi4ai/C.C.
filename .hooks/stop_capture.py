#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
brain Stop hook —— 收工自动捕获（安全网）+ 提醒 /save

读 stdin(JSON: {session_id, transcript_path, cwd, hook_event_name, stop_hook_active})。

这是回答 Doctor 的问题"如果我不 /save，你怎么知道什么时候该存？"的实现：
  1) 用【确定性信号】判定本会话是否"有实质改动"——统计 transcript 里 Edit/Write
     次数与工具调用总数（不调 LLM、不猜）。
  2) 若【无实质改动】或【本会话已经 /save 过】→ 什么都不做（不打扰、不留痕）。
  3) 若【有实质改动 且 未 /save】→ 只做两件安全的事：
       a. 把一份确定性 breadcrumb 写到 inbox/_auto/session-<日期>-<会话>.md
          （append-only 暂存区；每会话一份、刷新覆盖，不刷屏）。
       b. 首次发现时弹一条 macOS 通知，提醒你回 CC 里 /save。
  它【绝不】替你写 logs/ 或 permanent/（那需要 LLM 理解 = 你的 /save），
  【绝不】跑 git（G-X2 硬约束）。它只是"安全网 + 提醒"。

阈值/开关（环境变量，可在 settings.json 的 env 或 shell 里设）：
  BRAIN_HOOK_MIN_EDITS  默认 2   本会话 Edit/Write 次数 ≥ 此值 → 算实质
  BRAIN_HOOK_MIN_TOOLS  默认 8   或 工具调用总数 ≥ 此值 → 算实质
  BRAIN_HOOK_NOTIFY     默认 1   是否弹 macOS 通知（设 0 关闭）

永远 exit 0，绝不阻断收工。
"""
import sys
import os
import json
import datetime

MIN_EDITS = int(os.environ.get("BRAIN_HOOK_MIN_EDITS", "2") or 2)
MIN_TOOLS = int(os.environ.get("BRAIN_HOOK_MIN_TOOLS", "8") or 8)
NOTIFY = (os.environ.get("BRAIN_HOOK_NOTIFY", "1") or "1") == "1"

MAX_FILES = 40
MAX_PROMPTS = 5


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

    # 防止 Stop hook 触发的"继续"又再次触发 Stop（无限循环）
    if data.get("stop_hook_active"):
        return

    cwd = data.get("cwd", "")
    tpath = data.get("transcript_path", "")
    sid = (data.get("session_id", "") or "")[:8]

    here = os.path.dirname(os.path.abspath(__file__))
    brain = os.path.dirname(here)
    auto = os.path.join(brain, "inbox", "_auto")

    edits, prompts, n_tools, saved = _scan(tpath)

    material = (len(edits) >= MIN_EDITS) or (n_tools >= MIN_TOOLS)
    if not material or saved:
        return  # 无实质改动 或 已 /save → 不打扰、不留痕

    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d")
    sidpart = sid if sid else now.strftime("%H%M%S")
    try:
        os.makedirs(auto, exist_ok=True)
    except Exception:
        return

    # 每会话一份，刷新覆盖（避免一个会话多次 Stop 刷屏出几十个文件）
    fn = os.path.join(auto, f"session-{date}-{sidpart}.md")
    is_new = not os.path.exists(fn)

    body = []
    body.append("---")
    body.append(f"title: 自动捕获 {date} 会话 {sidpart}")
    body.append(f"tags: [auto, session-draft]")
    body.append(f"created: {date}")
    body.append(f"updated: {date}")
    body.append("status: draft")
    body.append("type: auto-draft")
    body.append("---")
    body.append("")
    body.append(f"# 自动捕获（未固化草稿）— {now.strftime('%Y-%m-%d %H:%M')}")
    body.append("")
    body.append(f"> ⚠️ 这是 Stop hook 的安全网产物，不是正式日志。请回 CC 里 **/save** "
                f"由 CC 总结成正式 logs/ 日志（含 Step 3.5 记忆分拣）。确认无用可删。")
    body.append("")
    body.append(f"**会话**：{sid or sidpart}  |  **工作目录**：{cwd}")
    body.append(f"**信号**：改动文件 {len(edits)} 个，工具调用 {n_tools} 次")
    if edits:
        body.append("")
        body.append("## 本会话改动的文件")
        for f in list(edits)[:MAX_FILES]:
            body.append(f"- {f}")
    if prompts:
        body.append("")
        body.append("## 用户意图（节选，首/尾）")
        picked = prompts[:2] + (["…"] if len(prompts) > 4 else []) + prompts[-2:] \
            if len(prompts) > 4 else prompts
        for p in picked[:MAX_PROMPTS]:
            body.append(f"- {p}")
    body.append("")

    try:
        with open(fn, "w", encoding="utf-8") as f:
            f.write("\n".join(body) + "\n")
    except Exception:
        return

    # 只在【首次】为这个会话建草稿时通知，避免每次 Stop 都弹
    if NOTIFY and is_new:
        _notify(
            f"{len(edits)} 个文件改动未固化",
            "建议回 CC 里 /save 存档本次会话",
        )


def _scan(tpath):
    """返回 (改动文件list, 用户意图list, 工具调用数, 是否已save)。"""
    edits = []
    seen = set()
    prompts = []
    n_tools = 0
    saved = False
    if not tpath or not os.path.exists(tpath):
        return edits, prompts, n_tools, saved
    logs_sep = os.path.join("brain", "logs").replace("\\", "/")
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
                        n_tools += 1
                        name = b.get("name", "")
                        inp = b.get("input", {}) or {}
                        fp = inp.get("file_path") or inp.get("path") or ""
                        if name in ("Edit", "Write", "MultiEdit", "NotebookEdit") and fp:
                            if logs_sep in fp.replace("\\", "/"):
                                saved = True  # 本会话写过 brain/logs/ → 视为已存档
                            if fp not in seen:
                                seen.add(fp)
                                edits.append(fp)
                    elif bt == "text" and role == "user":
                        t = (b.get("text") or "").strip().replace("\n", " ")
                        if not t or t.startswith("<"):
                            continue
                        prompts.append(t[:200])
                        head = t[:24]
                        if "/save" in head or "存档" in head or "落盘" in head:
                            saved = True
    except Exception:
        pass
    return edits, prompts, n_tools, saved


def _notify(title, message):
    try:
        import subprocess
        subprocess.run(
            ["osascript", "-e",
             f'display notification "{message}" with title "brain · {title}"'],
            timeout=5, check=False,
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
    except Exception:
        pass


if __name__ == "__main__":
    try:
        main()
    except Exception:
        # 永不阻断收工
        pass
    sys.exit(0)
