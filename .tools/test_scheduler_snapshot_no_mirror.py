#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""快照脚本不得用冻结的 Gateway 目录覆盖 live/ 与 artifacts/（ERR-20261104-005）。
HOME 指向临时目录运行，不碰真实文件。
  python3 test_scheduler_snapshot_no_mirror.py
  GEN=<旧版路径> python3 test_scheduler_snapshot_no_mirror.py   # 负向验证：旧版应失败
"""
import os, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
GEN = os.environ.get("GEN") or os.path.join(HERE, "scheduler_snapshot.py")
MIRROR = "Documents/Claude/brain/references/scheduled-live-mirror"


def write(root, rel, text):
    p = os.path.join(root, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        f.write(text)


def read(root, rel):
    p = os.path.join(root, rel)
    return open(p, encoding="utf-8").read() if os.path.exists(p) else None


def main():
    fails = []

    def check(name, ok):
        print(("PASS " if ok else "FAIL ") + name)
        if not ok:
            fails.append(name)

    with tempfile.TemporaryDirectory() as home:
        write(home, "Gateway-workspace/Scheduled/a/SKILL.md", "---\ndescription: 旧\n---\nGateway 旧版\n")
        write(home, "Gateway-workspace/Artifacts/b/index.html", "Gateway 旧看板")
        write(home, MIRROR + "/live/a/SKILL.md", "云端真源\n")
        write(home, MIRROR + "/live/only-in-live/SKILL.md", "Gateway 没有的班\n")
        write(home, MIRROR + "/artifacts/b/index.html", "较新看板")
        r = subprocess.run([sys.executable, "-I", GEN, "--triggered-by", "scheduled"],
                           env={**os.environ, "HOME": home}, capture_output=True, text=True)
        check("脚本正常退出", r.returncode in (0, 1, 2))
        check("live 真源未被覆盖", read(home, MIRROR + "/live/a/SKILL.md") == "云端真源\n")
        check("Gateway 没有的班未被删除", read(home, MIRROR + "/live/only-in-live/SKILL.md") is not None)
        check("看板镜像未被覆盖", read(home, MIRROR + "/artifacts/b/index.html") == "较新看板")
        check("不再写看板清单", read(home, MIRROR + "/artifacts/_artifacts_manifest.txt") is None)
        snap = read(home, "Documents/Claude/brain/permanent/_scheduler_snapshot.md") or ""
        check("快照写明镜像已停用", "已停用" in snap)
        check("快照本体仍生成", "triggered_by=scheduled" in snap)
    print(f"\n{'全部通过' if not fails else f'{len(fails)} 项失败'}")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
