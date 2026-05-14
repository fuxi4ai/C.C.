#!/usr/bin/env python3
"""
find-orphans.py — 找出孤立 / 弱链接的笔记

规则（Zettelkasten 健康度）：
  - 孤儿（orphan）：permanent/ 笔记**无任何入链**
  - 弱链接（weak）：permanent/ 笔记**出链 < 2**

依赖：先跑 build-backlinks.py 生成 .index/backlinks.json

用法：
  find-orphans.py                # 默认列出 orphan + weak
  find-orphans.py --orphan-only  # 只列孤儿
  find-orphans.py --weak-only    # 只列弱链接
  find-orphans.py --scope inbox  # 检查 inbox/ 而不是 permanent/

返回码：发现 ≥1 个 → 1（CI 可挂钩）；无 → 0
"""
import os
import json
import sys
import argparse
from pathlib import Path

BRAIN_ROOT = Path(os.path.expanduser("~/Documents/Claude/brain"))
SCRIPT_DIR = Path(__file__).resolve().parent
if not BRAIN_ROOT.exists():
    BRAIN_ROOT = SCRIPT_DIR.parent

INDEX = BRAIN_ROOT / ".index" / "backlinks.json"

RED = "\033[91m"
YEL = "\033[93m"
GRN = "\033[92m"
DIM = "\033[2m"
RST = "\033[0m"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--orphan-only", action="store_true")
    ap.add_argument("--weak-only", action="store_true")
    ap.add_argument("--scope", default="permanent", help="检查范围：permanent / inbox / fleeting / all")
    args = ap.parse_args()

    if not INDEX.exists():
        print(f"{RED}索引不存在：{INDEX}{RST}")
        print(f"{DIM}先跑：python3 {SCRIPT_DIR}/build-backlinks.py{RST}")
        sys.exit(2)

    backlinks = json.loads(INDEX.read_text(encoding="utf-8"))

    if args.scope == "all":
        scope_dirs = {"permanent", "inbox", "fleeting"}
    else:
        scope_dirs = {args.scope}

    # 列出 scope 内所有笔记
    notes = []
    for sd in scope_dirs:
        for p in (BRAIN_ROOT / sd).glob("*.md"):
            notes.append((p.stem, p.relative_to(BRAIN_ROOT)))

    if not notes:
        print(f"{DIM}{args.scope}/ 内无 .md 笔记{RST}")
        sys.exit(0)

    orphans = []
    weaks = []
    for name, rel in notes:
        node = backlinks.get(name, {"incoming": [], "outgoing": []})
        in_count = len(node["incoming"])
        out_count = len(node["outgoing"])
        if in_count == 0:
            orphans.append((name, rel, in_count, out_count))
        if out_count < 2:
            weaks.append((name, rel, in_count, out_count))

    print(f"{DIM}范围：{args.scope}/ · 共 {len(notes)} 篇笔记{RST}\n")

    found = 0
    if not args.weak_only and orphans:
        print(f"{RED}━ 孤儿（无入链）· {len(orphans)} 篇{RST}")
        for name, rel, ic, oc in orphans:
            print(f"  {RED}✗{RST} {rel}  {DIM}in={ic} out={oc}{RST}")
        print()
        found += len(orphans)

    if not args.orphan_only and weaks:
        # 排除已在 orphans 里的
        orphan_names = {n[0] for n in orphans}
        pure_weak = [w for w in weaks if w[0] not in orphan_names]
        if pure_weak:
            print(f"{YEL}━ 弱链接（出链<2）· {len(pure_weak)} 篇{RST}")
            for name, rel, ic, oc in pure_weak:
                print(f"  {YEL}!{RST} {rel}  {DIM}in={ic} out={oc}{RST}")
            print()
            found += len(pure_weak)

    if found == 0:
        print(f"{GRN}✓ {args.scope}/ 健康——无孤儿无弱链接{RST}")
        sys.exit(0)
    else:
        total = len(notes)
        print(f"{DIM}━ 健康度：{(total - found)}/{total} = {100*(total-found)//total}%{RST}")
        sys.exit(1)

if __name__ == "__main__":
    main()
