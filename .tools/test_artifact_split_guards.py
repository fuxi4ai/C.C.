#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""两个看板拆分器的守卫负向测试（2026-11-12 立 · GOTCHAS 烛照九阴 ERR-20261112-001 / 风险日报 ERR-20261112-001、-003）。

在临时 BRAIN_ROOT 里跑，不碰盘上产物。每个坏输入必须 exit≠0 且不写出任何 artifact.html；好输入必须 exit 0。
用法：python3 test_artifact_split_guards.py     全过 exit 0，否则 exit 1
"""
import glob, os, re, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
BRAIN = os.path.dirname(HERE)
DOCS = os.path.dirname(os.path.dirname(BRAIN))
ZZ_SRC = os.path.join(DOCS, "AI4ME/烛照九阴-outputs/artifact/zhuzhao-jiuyin-daily.html")
RD_SRC = os.path.join(DOCS, "Claude/Projects/风险日报/dashboard/risk-daily.html")
fails = []


def run(tool, html, want_ok, name):
    tmp = tempfile.mkdtemp(prefix="splitguard_")
    try:
        os.makedirs(os.path.join(tmp, ".tmp", "artifact-publish"))
        os.makedirs(os.path.join(tmp, ".tools"))  # brain_root() 认「含 .tools 的目录」
        shutil.copy(os.path.join(BRAIN, ".tmp/artifact-publish/hosted-pages.json"), os.path.join(tmp, ".tmp/artifact-publish/"))
        src = os.path.join(tmp, "src.html")
        open(src, "w", encoding="utf-8").write(html)
        r = subprocess.run([sys.executable, os.path.join(HERE, tool), "--src", src], env=dict(os.environ, BRAIN_ROOT=tmp),
                           capture_output=True, text=True)
        wrote = glob.glob(os.path.join(tmp, ".tmp/artifact-publish/*/artifact.html"))
        ok = (r.returncode == 0 and wrote) if want_ok else (r.returncode != 0 and not wrote)
        print("%s %-34s exit=%d 产物=%d  %s" % ("PASS" if ok else "FAIL", name, r.returncode, len(wrote),
                                               (r.stderr or r.stdout).strip().splitlines()[-1][:90] if (r.stderr or r.stdout).strip() else ""))
        if not ok:
            fails.append(name)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def sub1(pat, rep, s, what):
    out, n = re.subn(pat, rep, s, count=1)
    if n != 1:
        sys.exit("测试夹具失效：%s 在原件里找不到，先更新本测试" % what)
    return out


zz = open(ZZ_SRC, encoding="utf-8").read()
T = "artifact_split_zhuzhao.py"
run(T, zz, True, "烛照·原件")
run(T, sub1(r'(\.version\s*=\s*["\'])5\.6\.0(["\'])', r"\g<1>9.9.9\2", zz, "版本串"), False, "烛照·版本串改 9.9.9")
i = zz.index("Apache Software Foundation")
j = zz.index(";", i + 5000)
run(T, zz[:j] + "; " + zz[j + 1:], False, "烛照·库体被改而版本不变")
run(T, re.sub(r"data:image/[a-z0-9.+-]+;base64,[A-Za-z0-9+/]{50000,}={0,2}", "data:image/png;base64,AAAA", zz), False, "烛照·题图缺失")

rd = open(RD_SRC, encoding="utf-8").read()
T = "artifact_split_risk_daily.py"
run(T, rd, True, "风险日报·原件")
run(T, sub1(r'<link rel="preconnect" href="https://fonts\.googleapis\.com">', "", rd, "主页字体 preconnect"), False, "风险日报·字体 link 少一条")
run(T, sub1(r'getElementById\(\\"lnk-desk\\"\)', r'getElementById(\\"lnk-desk2\\")', rd, "AI 页 lnk-desk"), False, "风险日报·AI 页入口改名")
run(T, sub1(r'<a class=\\"research-link\\" href=\\"/research\\"', r'<a class=\\"research-link\\" href=\\"/desk\\"', rd, "EAL 页研究台链接"), False, "风险日报·EAL 研究台链接改址")

print("—— %d 项失败" % len(fails) if fails else "—— 全部通过")
sys.exit(1 if fails else 0)
