#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_skill_parity.py 不带 --runtime 时应比对最新的账号副本（HOME 指向临时目录，不碰真实文件）。"""
import os, subprocess, sys, tempfile, time

TOOL = os.path.join(os.path.dirname(os.path.abspath(__file__)), "check_skill_parity.py")


def write(root, rel, text):
    p = os.path.join(root, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        f.write(text)


def main():
    with tempfile.TemporaryDirectory() as home:
        base = "Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin"
        write(home, f"{base}/old/x/skills/brain-demo/SKILL.md", "stale")
        time.sleep(0.05)
        write(home, f"{base}/new/y/skills/brain-demo/SKILL.md", "fresh")
        os.utime(os.path.join(home, f"{base}/old/x/skills"), (1, 1))
        for rel in ("brain/.skills/brain-demo/SKILL.md", "brain/portable/skills/brain-demo/SKILL.md"):
            write(home, "Documents/Claude/" + rel, "fresh")
        r = subprocess.run([sys.executable, TOOL, "--docs", os.path.join(home, "Documents")],
                           env={**os.environ, "HOME": home, "SKILL_RUNTIME_DIR": ""},
                           capture_output=True, text=True)
        out = r.stdout + r.stderr
        ok = "Traceback" not in out and f"{base}/new/y/skills" in out and "/old/x/" not in out
        print(("PASS" if ok else "FAIL") + " 默认比对最新账号副本")
        if not ok:
            print(out[-600:])
        return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
