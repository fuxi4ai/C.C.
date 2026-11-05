#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""薄壳包结构正确；巡检认薄壳，frontmatter 不同则报分歧。全程在临时目录。"""
import importlib.util, os, subprocess, sys, tempfile, zipfile

H = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("parity", os.path.join(H, "check_skill_parity.py"))
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
fails = []


def check(name, ok):
    print(("PASS " if ok else "FAIL ") + name)
    if not ok:
        fails.append(name)


with tempfile.TemporaryDirectory() as d:
    subprocess.run([sys.executable, os.path.join(H, "build_skill_stub.py"), "brain-note", d], check=True, capture_output=True)
    z = zipfile.ZipFile(os.path.join(d, "brain-note.zip"))
    check("包内只有 <名>/SKILL.md", z.namelist() == ["brain-note/SKILL.md"])
    stub = z.read("brain-note/SKILL.md")
    canon = open(os.path.expanduser("~/Documents/Claude/brain/.skills/brain-note/SKILL.md"), "rb").read()
    check("frontmatter 可解析且单块", m.parse_fm(stub.decode())[1] in (None, "") and not m.dup_frontmatter(stub.decode()))
    check("正文含 canonical 路径与失败即停", b".skills/brain-note/SKILL.md" in stub and "技能正文不可达".encode() in stub)
    check("不含 canonical 正文", "Inbox 笔记采集".encode() not in stub)
    check("巡检判为薄壳", m.classify(canon, stub)[0] == "stub")
    check("description 不同报分歧", m.classify(canon, stub.replace(b'description: "', b'description: "X', 1))[0] == "divergent")
    check("无标记的改动仍报分歧", m.classify(canon, canon + b"\nextra\n")[0] == "divergent")
print("\n全部通过" if not fails else f"\n{len(fails)} 项失败")
sys.exit(1 if fails else 0)
