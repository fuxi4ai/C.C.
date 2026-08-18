#!/usr/bin/env python3
"""scheduler_snapshot.py --dry-run 零写入不变测试（2026-08-17 VV 七轮要求）。

跑 --dry-run 前后，对快照与镜像三处（_scheduler_snapshot.json/.md、
scheduled-live-mirror/live、scheduled-live-mirror/artifacts）做
「文件清单 × sha256 × mtime」快照，断言完全一致。
Mac 原生跑（Gateway 树可达）；沙箱跑退化为 absent 一致（仍验证脚本自身与退出码）。
"""
import os, sys, subprocess, hashlib
from pathlib import Path

HOME = Path.home()
DOC = HOME / "mnt" / "Documents"          # 沙箱挂载映射
if not DOC.exists():
    DOC = HOME / "Documents"               # Mac 原生
SNAP = DOC / "Claude/brain/.tools/scheduler_snapshot.py"
WATCH = [
    DOC / "Claude/brain/permanent/_scheduler_snapshot.json",
    DOC / "Claude/brain/permanent/_scheduler_snapshot.md",
    DOC / "Claude/brain/references/scheduled-live-mirror/live",
    DOC / "Claude/brain/references/scheduled-live-mirror/artifacts",
]


def snapshot():
    out = {}
    for root in WATCH:
        try:
            if root.is_file():
                s = root.read_bytes()
                out[str(root)] = ("f", hashlib.sha256(s).hexdigest(), int(root.stat().st_mtime))
            elif root.is_dir():
                for p in root.rglob("*"):
                    if p.is_file():
                        s = p.read_bytes()
                        out[str(p)] = ("f", hashlib.sha256(s).hexdigest(), int(p.stat().st_mtime))
            else:
                out[str(root)] = ("absent", None, None)
        except OSError:
            out[str(root)] = ("unreadable", None, None)
    return out


def main():
    before = snapshot()
    r = subprocess.run([sys.executable, str(SNAP), "--dry-run"], capture_output=True, text=True)
    after = snapshot()
    if r.returncode != 0:
        print(f"FAIL: --dry-run exit={r.returncode}")
        print((r.stderr or "")[-1500:])
        return 1
    diffs = [(k, before.get(k), after.get(k)) for k in set(before) | set(after) if before.get(k) != after.get(k)]
    if diffs:
        for d in diffs:
            print("CHANGED:", d)
        print("FAIL: --dry-run 不是零写入")
        return 1
    print(f"PASS: --dry-run 零写入（{len(before)} 项清单×sha×mtime 前后全等）· exit=0")
    print("  stdout 摘要:")
    print("\n".join("  " + ln for ln in (r.stdout or "").strip().splitlines()[-12:]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
