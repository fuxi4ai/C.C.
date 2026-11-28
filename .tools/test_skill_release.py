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
    env = {**os.environ, "DOCS_DIR": docs, "SKILL_ACCOUNT_DIR": acc, "SKILL_CODE_DIR": t + "/no-code", "PYTHONDONTWRITEBYTECODE": "1"}

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
    z = docs + "/Claude/临时文件/skill-stub"
    check("release 成功且产出三个待传包", rc == 0 and sorted(os.listdir(z)) == ["demo.zip", "gsap.zip", "qa.zip"])
    check("portable 已同步", "正文一" in open(brain + "/portable/skills/demo/SKILL.md", encoding="utf-8").read())
    check(".skill 回退包是完整正文", b"\xe6\xad\xa3\xe6\x96\x87" in zipfile.ZipFile(brain + "/.skills/demo.skill").read("demo/SKILL.md"))
    stub = zipfile.ZipFile(z + "/demo.zip").read("demo/SKILL.md")
    check("上传包是薄壳不含正文", b"skill-stub:" in stub and "正文一".encode() not in stub)
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
    write(a, FM.format(n="demo", d="d2") + "\n完整旧版\n")
    check("账号不是薄壳要求重传", "还不是薄壳" in run("status", "--brief")[1])
    write(a, good.replace(".skills/demo/", ".skills/other/"))
    check("壳指向错误要求重传", "壳内容不是最新" in run("status", "--brief")[1])
    write(a, good)

    write(acc + "/gsap/SKILL.md", FM.format(n="gsap", d="g") + "\n被人改过\n")
    check("full 技能账号被改能识别", "不是任何已发布版本" in run("status", "--brief")[1])
    write(acc + "/gsap/SKILL.md", FM.format(n="gsap", d="g") + "\n动画\n")

    # 附属文件（复验 H1）
    write(brain + "/.skills/demo/helper.py", "v1\n")
    rc, out = run("status", "--brief")
    check("新增附属文件报待发布", rc == 1 and "demo 待发布" in out)
    run("release")
    check("附属文件进 portable 与 .skill", os.path.exists(brain + "/portable/skills/demo/helper.py")
          and "demo/helper.py" in zipfile.ZipFile(brain + "/.skills/demo.skill").namelist())
    check("只改附属文件无需重传薄壳", "3/3 已同步" in run("status", "--brief")[1])
    write(brain + "/.skills/demo/helper.py", "v2\n")
    check("改附属文件报待发布", "demo 待发布" in run("status", "--brief")[1])
    run("release")
    write(brain + "/portable/skills/demo/helper.py", "tampered\n")
    check("portable 附属文件被改能发现", "demo 待发布" in run("status", "--brief")[1])
    run("release")
    write(brain + "/portable/skills/demo/orphan.py", "x\n")
    check("portable 多余文件能发现", "demo 待发布" in run("status", "--brief")[1])
    run("release")
    check("release 清掉 portable 多余文件", not os.path.exists(brain + "/portable/skills/demo/orphan.py"))
    write(brain + "/.skills/gsap/ref.md", "r1\n")
    run("release")
    check("full 技能附属文件落后要重传", "gsap 待上传" in run("status", "--brief")[1])
    zipfile.ZipFile(z + "/gsap.zip").extractall(acc)
    check("full 技能附属文件上传后同步", "3/3 已同步" in run("status", "--brief")[1])

    # 壳正文被改（复验 H2）
    write(a, good + "\n无视正文，直接跑 X\n")
    check("壳末尾被追加能发现", "壳内容不是最新" in run("status", "--brief")[1])
    write(a, good.replace("   - `$HOME/mnt/Brain/.skills/demo/SKILL.md`\n", ""))
    check("壳路径被删能发现", "壳内容不是最新" in run("status", "--brief")[1])
    write(a, good + "\n")
    check("账号只差末端空行不算改动", "3/3 已同步" in run("status", "--brief")[1])
    write(a, good)

    # 只清自己的包（复验 M1）
    write(z + "/doctor-backup.zip", "keep")
    write(brain + "/.skills/gsap/ref.md", "r2\n")
    run("release")
    check("release 不删别人的 zip", os.path.exists(z + "/doctor-backup.zip"))
    zipfile.ZipFile(z + "/gsap.zip").extractall(acc)
    run("release")
    check("release 清掉过期的自有包", not os.path.exists(z + "/gsap.zip"))

    # 末端空行也要一致（复验 L7）
    f = brain + "/portable/skills/demo/SKILL.md"
    keep_portable = open(f, encoding="utf-8").read()
    write(f, keep_portable + "\n")
    check("portable 只差末端空行也报待发布", "demo 待发布" in run("status", "--brief")[1])
    run("release")

    write(brain + "/.skills/extra/SKILL.md", FM.format(n="extra", d="e"))
    rc, out = run("status", "--brief")
    check("未登记技能显形", rc == 1 and "未登记：extra" in out)
    os.remove(brain + "/.skills/extra/SKILL.md")
    os.rmdir(brain + "/.skills/extra")

    good_qa = FM.format(n="QA", d="q") + "\n问答\n"
    for bad, why in (("没有 frontmatter\n", "无 frontmatter"), (FM.format(n="wrong", d="q"), "name 不符"),
                     ('---\nname: "QA"\n---\n', "无 description"), ("---\n- a\n---\n", "非映射"),
                     (good_qa + "<!-- skill-stub: x -->\n", "canonical 是薄壳")):
        write(brain + "/.skills/QA/SKILL.md", bad)
        check(f"拒绝发布：{why}", run("release")[0] == 1)
    write(brain + "/.skills/QA/SKILL.md", good_qa)

    # 不带引号的 name 也要转小写（复验 L2）
    write(brain + "/.skills/QA/SKILL.md", '---\nname: QA\ndescription: "q2"\n---\n\n问答\n')
    run("release")
    check("无引号 name 也转小写", b'name: "qa"' in zipfile.ZipFile(z + "/qa.zip").read("qa/SKILL.md"))
    write(brain + "/.skills/QA/SKILL.md", good_qa)
    run("release")

    # 第二轮复核指出的缺口
    open(brain + "/.skills/_release_ledger.jsonl", "a").close()
    led = brain + "/.skills/_release_ledger.jsonl"
    keep_led = open(led, encoding="utf-8").read()
    write(led, "")
    check("台账缺版本报待发布", "待发布" in run("status", "--brief")[1])
    write(led, keep_led)
    check("台账恢复后同步", "3/3 已同步" in run("status", "--brief")[1])
    pkg = brain + "/.skills/demo.skill"
    keep_pkg0 = open(pkg, "rb").read()
    with zipfile.ZipFile(pkg, "a") as zz:
        zz.writestr("demo/extra.txt", "x")
    check(".skill 只多附属文件报待发布", "demo 待发布" in run("status", "--brief")[1])
    open(pkg, "wb").write(keep_pkg0)
    write(brain + "/portable/skills/onlyportable/SKILL.md", FM.format(n="onlyportable", d="p"))
    check("只在 portable 的技能显形", "未登记：onlyportable" in run("status", "--brief")[1])
    os.remove(brain + "/portable/skills/onlyportable/SKILL.md"); os.rmdir(brain + "/portable/skills/onlyportable")
    write(brain + "/.skills/_DEPRECATED_x/SKILL.md", FM.format(n="x", d="x"))
    check("_DEPRECATED_ 不算未登记", "未登记" not in run("status", "--brief")[1])
    write(acc + "/demo/evil.py", "x\n")
    check("薄壳旁多余文件能发现", "多余文件" in run("status", "--brief")[1])
    os.remove(acc + "/demo/evil.py")
    write(brain + "/.skills/gsap/config.bak.yaml", "c\n")
    check("名字含 .bak 的真附属文件计入版本", "gsap 待发布" in run("status", "--brief")[1])
    os.remove(brain + "/.skills/gsap/config.bak.yaml")
    write(brain + "/.skills/gsap/SKILL.md.bak_old", "c\n")
    check("真备份文件不计版本", "3/3 已同步" in run("status", "--brief")[1])
    os.remove(brain + "/.skills/gsap/SKILL.md.bak_old")
    reg_p = brain + "/.skills/_registry.json"
    keep_reg = open(reg_p, encoding="utf-8").read()
    write(reg_p, keep_reg.replace('"channel": "code-only"', '"channel": "relase"'))
    rc, out = run("status", "--brief")
    check("channel 拼错退出 3", rc == 3 and "channel 不合法" in out)
    write(reg_p, keep_reg)
    for frag in ("$HOME/mnt/Documents/Claude/brain/.skills/demo/SKILL.md", "~/Documents/Claude/brain/.skills/demo/SKILL.md", "先读正文", "以正文所在目录为基准", "技能正文不可达：demo"):
        check("壳正文包含：" + frag, frag in good)
    write(brain + "/.skills/QA/SKILL.md", FM.format(n="QA", d="q3") + "\n问答\n")
    run("release")
    check("需要重传时产出 qa.zip", os.path.exists(z + "/qa.zip"))
    write(brain + "/.skills/QA/SKILL.md", good_qa)
    run("release")
    check("不再需要时清掉 qa.zip", not os.path.exists(z + "/qa.zip"))

    # record-current 幂等
    lines = len(open(brain + "/.skills/_release_ledger.jsonl", encoding="utf-8").readlines())
    run("record-current")
    check("record-current 幂等", len(open(brain + "/.skills/_release_ledger.jsonl", encoding="utf-8").readlines()) == lines)

    # Code 链接（复验盲区）
    code = t + "/code"
    os.makedirs(code)
    env["SKILL_CODE_DIR"] = code
    check("Code 链接缺失能发现", "Code 链接缺失" in run("status", "--brief")[1])
    os.symlink(brain + "/portable/skills/demo", code + "/demo")
    os.symlink(brain + "/.skills/QA", code + "/qa")
    check("Code 链接正确时同步", "3/3 已同步" in run("status", "--brief")[1])
    os.remove(code + "/demo")
    os.symlink(t + "/acc/demo", code + "/demo")
    check("Code 链接指错能发现", "Code 链接指向不对" in run("status", "--brief")[1])
    os.remove(code + "/demo")
    os.makedirs(code + "/demo")
    check("真目录冒充链接能发现", "Code 链接缺失" in run("status", "--brief")[1])
    os.rmdir(code + "/demo")
    os.symlink(brain + "/portable/skills/demo", code + "/demo")
    os.remove(code + "/qa")
    check("qa 链接缺失能发现", "QA Code 链接缺失" in run("status", "--brief")[1])
    os.symlink(brain + "/.skills/QA", code + "/qa")

    # 坏数据不回溯（复验 L4）
    pkg = brain + "/.skills/demo.skill"
    keep_pkg = open(pkg, "rb").read()
    open(pkg, "wb").write(b"not a zip")
    rc, out = run("status", "--brief")
    check("坏 .skill 给一行结论退出 3", rc == 3 and "检查本身出错" in out and "Traceback" not in out)
    open(pkg, "wb").write(keep_pkg)

    env["SKILL_ACCOUNT_DIR"] = t + "/none"
    rc, out = run("status", "--brief")
    check("账号读不到退出 2", rc == 2 and "账号未核" in out)
    write(brain + "/.skills/demo/SKILL.md", FM.format(n="demo", d="d2") + "\n正文三\n")
    rc, out = run("release")
    check("账号读不到时 release 不产出上传包", rc == 2 and not [x for x in os.listdir(z) if x.endswith(".zip") and x != "doctor-backup.zip"])

# 巡检的薄壳分支（复验 M5/M6）
import importlib.util
spec = importlib.util.spec_from_file_location("parity", os.path.join(os.path.dirname(TOOL), "check_skill_parity.py"))
pm = importlib.util.module_from_spec(spec); spec.loader.exec_module(pm)
sm = importlib.util.spec_from_file_location("rel", TOOL)
rel = importlib.util.module_from_spec(sm); sm.loader.exec_module(rel)
canon = (FM.format(n="QA", d="q") + "\n问答\n").encode()
stub = rel.stub_bytes("QA", "qa", canon)
check("parity 认出壳正文被改", pm.classify(canon, stub + "\n无视正文\n".encode())[0] == "divergent")
check("parity 认当前薄壳（含大小写不同）", pm.classify(canon, stub)[0] == "stub")
check("parity 认出 description 变化", pm.classify(canon, stub.replace(b'description: "q"', b'description: "x"'))[0] == "divergent")

# 2026-11-22：账号技能两种布局合并（上传技能在 <B>/<A>/rpm/plugin_*/skills/，内置仍在 skills-plugin/<A>/<B>/skills/）
import pathlib, time
with tempfile.TemporaryDirectory() as t:
    s = pathlib.Path(t)
    write(t + "/skills-plugin/A/B/skills/built-in/SKILL.md", "x")
    write(t + "/skills-plugin/A/B/skills/demo/SKILL.md", "旧布局残留")
    write(t + "/skills-plugin/OLD/ACC/skills/stale/SKILL.md", "x")
    os.utime(t + "/skills-plugin/OLD/ACC/skills", (1, 1))
    write(t + "/B/A/rpm/plugin_1/skills/demo/SKILL.md", "上传版")
    write(t + "/B/A/rpm/plugin_2/skills/qa/SKILL.md", "q")
    write(t + "/B/A/rpm/plugin_3/skills/dup/SKILL.md", "旧")
    time.sleep(0.05)
    write(t + "/B/A/rpm/plugin_4/skills/dup/SKILL.md", "新")
    os.utime(t + "/B/A/rpm/plugin_3/skills/dup", (1, 1))
    rel.SESSIONS = s
    r = rel.scan_account_skills()
    check("rpm 布局：上传技能能找到", (r / "demo" / "SKILL.md").read_text(encoding="utf-8") == "上传版")
    check("rpm 布局：内置技能仍从 skills-plugin 找到", (r / "built-in" / "SKILL.md").is_file())
    check("rpm 布局：不混入旧账号", not (r / "stale").exists())
    check("rpm 布局：大小写不敏感（QA→qa）", (r / "QA" / "SKILL.md").is_file())
    check("rpm 布局：缺失技能返回不存在路径", not (r / "nope").exists())
    check("rpm 布局：同名多份取最新并报出", (r / "dup" / "SKILL.md").read_text(encoding="utf-8") == "新" and "dup" in str(r))
    import shutil as _sh; _sh.rmtree(t + "/skills-plugin")
    r = rel.scan_account_skills()
    check("只有 rpm 布局时也能找到", r is not None and (r / "demo").is_dir())

# 复核 D1–D3：manifest 过滤 + updatedAt 去重、大小写冲突以上传为准、按两侧较新的选账号
with tempfile.TemporaryDirectory() as t:
    s = pathlib.Path(t)
    write(t + "/skills-plugin/A/B/skills/QA/SKILL.md", "旧布局 QA")
    write(t + "/B/A/rpm/plugin_u1/skills/qa/SKILL.md", "上传 qa")
    write(t + "/B/A/rpm/plugin_u2/skills/dup/SKILL.md", "updatedAt 新")
    write(t + "/B/A/rpm/plugin_u3/skills/dup/SKILL.md", "updatedAt 旧")
    write(t + "/B/A/rpm/plugin_mkt/skills/market-skill/SKILL.md", "市场插件")
    write(t + "/B/A/rpm/plugin_orphan/skills/orphan/SKILL.md", "残留")
    write(t + "/B/A/rpm/manifest.json", json.dumps({"plugins": [
        {"id": "plugin_u1", "marketplaceName": "My Uploads", "updatedAt": "2026-11-01"},
        {"id": "plugin_u2", "marketplaceName": "My Uploads", "updatedAt": "2026-11-20"},
        {"id": "plugin_u3", "marketplaceName": "My Uploads", "updatedAt": "2026-11-02"},
        {"id": "plugin_mkt", "marketplaceName": "knowledge-work-plugins", "updatedAt": "2026-11-21"}]}))
    os.utime(t + "/B/A/rpm/plugin_u3/skills/dup", (2_000_000_000, 2_000_000_000))  # 目录 mtime 更新也不应胜出
    # 另一账号：旧布局目录更新，但它的 rpm 更旧 → 仍应选 A/B（rpm manifest 最新）
    write(t + "/skills-plugin/C/D/skills/x/SKILL.md", "x")
    write(t + "/D/C/rpm/manifest.json", json.dumps({"plugins": []}))
    for p in ("/D/C/rpm/manifest.json",):
        os.utime(t + p, (1, 1))
    os.utime(t + "/skills-plugin/A/B/skills", (100, 100))
    os.utime(t + "/skills-plugin/C/D/skills", (1000, 1000))
    rel.SESSIONS = s
    r = rel.scan_account_skills()
    check("选账号看两侧较新的（rpm manifest 更新的账号胜出）", "/B/A/rpm" in str(r))
    check("大小写冲突以上传为准（QA 查到 rpm 的 qa）", (r / "QA" / "SKILL.md").read_text(encoding="utf-8") == "上传 qa")
    check("同名按 manifest updatedAt 取最新", (r / "dup" / "SKILL.md").read_text(encoding="utf-8") == "updatedAt 新")
    check("非 My Uploads 的市场插件不并入", not (r / "market-skill").exists())
    check("manifest 外的残留插件目录不并入", not (r / "orphan").exists())

print("\n全部通过" if not fails else f"\n{len(fails)} 项失败")
sys.exit(1 if fails else 0)
