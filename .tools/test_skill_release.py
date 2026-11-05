#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""skill_release.py 回归测试：DOCS_DIR 与 SKILL_ACCOUNT_DIR 都指向临时目录。"""
import json, os, subprocess, sys, tempfile, zipfile

TOOL = os.path.join(os.path.dirname(os.path.abspath(__file__)), "skill_release.py")
FM = '---\nname: "{n}"\ndescription: "{d}"\n---\n'
fails = []


def check(name, ok):
    print(("PASS " if ok else "FAIL ") + name)
    if not ok:
        fails.append(name)


def write(p, text):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8").write(text)


with tempfile.TemporaryDirectory() as t:
    docs, acc = t + "/docs", t + "/acc"
    brain = docs + "/Claude/brain"
    os.makedirs(acc)
    env = {**os.environ, "DOCS_DIR": docs, "SKILL_ACCOUNT_DIR": acc, "PYTHONDONTWRITEBYTECODE": "1"}

    def run(*a):
        r = subprocess.run([sys.executable, TOOL, *a], env=env, capture_output=True, text=True)
        return r.returncode, r.stdout + r.stderr

    write(brain + "/.skills/_registry.json", json.dumps({"skills": {
        "demo": {"channel": "release", "portable": True},
        "QA": {"channel": "release", "portable": False, "account_name": "qa"},
        "gsap": {"channel": "release", "portable": False, "account": "full"},
        "local": {"channel": "code-only"}}}))
    write(brain + "/.skills/demo/SKILL.md", FM.format(n="demo", d="d1") + "\n正文一\n")
    write(brain + "/.skills/QA/SKILL.md", FM.format(n="QA", d="q") + "\n问答\n")
    write(brain + "/.skills/gsap/SKILL.md", FM.format(n="gsap", d="g") + "\n动画\n")

    rc, out = run("status")
    check("未发布时报待发布且退出 1", rc == 1 and "待发布" in out)
    rc, out = run("release")
    z = docs + "/Claude/临时文件/skill-release"
    check("release 成功且产出三个待传包", rc == 0 and sorted(os.listdir(z)) == ["demo.zip", "gsap.zip", "qa.zip"])
    check("portable 已同步", "正文一" in open(brain + "/portable/skills/demo/SKILL.md", encoding="utf-8").read())
    check(".skill 回退包是完整正文", b"\xe6\xad\xa3\xe6\x96\x87" in zipfile.ZipFile(brain + "/.skills/demo.skill").read("demo/SKILL.md"))
    stub = zipfile.ZipFile(z + "/demo.zip").read("demo/SKILL.md")
    check("上传包是薄壳不含正文", b"skill-stub: v2 " in stub and "正文一".encode() not in stub)
    qa = zipfile.ZipFile(z + "/qa.zip").read("qa/SKILL.md").decode()
    check("QA 账号名小写、路径指原目录", 'name: "qa"' in qa and ".skills/QA/SKILL.md" in qa)
    check("full 技能上传完整版", "动画".encode() in zipfile.ZipFile(z + "/gsap.zip").read("gsap/SKILL.md"))

    for n, f in (("demo", "demo.zip"), ("qa", "qa.zip"), ("gsap", "gsap.zip")):
        zipfile.ZipFile(z + "/" + f).extractall(acc)
    rc, out = run("status", "--brief")
    check("上传后全部同步退出 0", rc == 0 and "3/3 已同步" in out)

    write(brain + "/.skills/demo/SKILL.md", FM.format(n="demo", d="d1") + "\n正文二\n")
    run("release")
    rc, out = run("status", "--brief")
    check("只改正文：发布后无需重传", rc == 0 and "3/3 已同步" in out)
    check("只改正文：没有产出待传包", os.listdir(z) == [])

    write(brain + "/.skills/demo/SKILL.md", FM.format(n="demo", d="d2") + "\n正文二\n")
    rc, out = run("status", "--brief")
    check("改了正文未发布时报待发布", rc == 1 and "demo 待发布" in out)
    run("release")
    rc, out = run("status", "--brief")
    check("改触发描述：要求重传", rc == 1 and "触发描述已变" in out)
    zipfile.ZipFile(z + "/demo.zip").extractall(acc)

    a = acc + "/demo/SKILL.md"
    good = open(a, encoding="utf-8").read()
    write(a, good.replace("skill-stub: v2 ", "skill-stub: v1 "))
    check("壳版本落后要求重传", "壳版本落后" in run("status", "--brief")[1])
    write(a, FM.format(n="demo", d="d2") + "\n完整旧版\n")
    check("账号不是薄壳要求重传", "还不是薄壳" in run("status", "--brief")[1])
    write(a, good.replace(".skills/demo/", ".skills/other/"))
    check("壳指向错误要求重传", "壳指向错误" in run("status", "--brief")[1])
    write(a, good)

    write(acc + "/gsap/SKILL.md", FM.format(n="gsap", d="g") + "\n被人改过\n")
    check("full 技能账号被改能识别", "不是任何已发布版本" in run("status", "--brief")[1])
    zipfile.ZipFile(z + "/gsap.zip").extractall(acc) if os.path.exists(z + "/gsap.zip") else write(acc + "/gsap/SKILL.md", FM.format(n="gsap", d="g") + "\n动画\n")

    write(brain + "/.skills/extra/SKILL.md", FM.format(n="extra", d="e"))
    rc, out = run("status", "--brief")
    check("未登记技能显形", rc == 1 and "未登记：extra" in out)
    os.remove(brain + "/.skills/extra/SKILL.md")
    os.rmdir(brain + "/.skills/extra")

    write(brain + "/.skills/QA/SKILL.md", "没有 frontmatter\n")
    rc, out = run("release")
    check("frontmatter 坏了拒绝发布", rc == 1 and "未发布" in out)
    write(brain + "/.skills/QA/SKILL.md", FM.format(n="QA", d="q") + "\n问答\n")

    env["SKILL_ACCOUNT_DIR"] = t + "/none"
    rc, out = run("status", "--brief")
    check("账号读不到退出 2", rc == 2 and "账号未核" in out)

print("\n全部通过" if not fails else f"\n{len(fails)} 项失败")
sys.exit(1 if fails else 0)
