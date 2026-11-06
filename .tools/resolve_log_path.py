#!/usr/bin/env python3
"""resolve_log_path — 把省略月目录的日志引用解析到盘上实际路径（2026-11-05 Doctor 裁 5A）。

约定：文内引用一律写 `logs/YYYY-MM-DD-主题.md`（或 `logs/checkpoints/…`、`logs/checkups/…`），
meditation 每月 1 号把上月日志折进 `logs/YYYY-MM/`（checkpoints/checkups 随月走）。
本函数先试原路径，再试插入 `YYYY-MM/` 月目录；都不在返回 None（不猜）。

用法：
  from resolve_log_path import resolve
  resolve("logs/2026-10-07-PEC-CS07全语料重提炼v2.0.md", brain_root)
  python3 resolve_log_path.py <引用路径> [brain_root]   # 命令行：打印解析结果或 MISSING（exit 1）
"""
import os, re, sys

_DATE = re.compile(r"(\d{4})-(\d{2})-\d{2}")

def candidates(ref: str):
    """返回按优先序排列的候选相对路径（不查盘）。"""
    ref = ref.replace("\\", "/").lstrip("./")
    if ref.startswith("brain/"):
        ref = ref[len("brain/"):]
    out = [ref]
    m = re.match(r"^logs/((?:checkpoints|checkups)/)?([^/]+)$", ref)
    if m:
        sub, base = m.group(1) or "", m.group(2)
        d = _DATE.search(base)
        if d:
            out.append(f"logs/{d.group(1)}-{d.group(2)}/{sub}{base}")
    return out

def resolve(ref: str, brain_root: str):
    for c in candidates(ref):
        p = os.path.join(brain_root, c)
        if os.path.exists(p):
            return p
    return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(2)
    root = sys.argv[2] if len(sys.argv) > 2 else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    r = resolve(sys.argv[1], root)
    print(r or "MISSING"); sys.exit(0 if r else 1)
