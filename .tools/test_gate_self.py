#!/usr/bin/env python3
"""eal_gate_check.py 自身 fail-fast（PRD 2026-08-17 §二 D：注入破坏后 gate 必报 FAIL）

十七用例（2026-11-06：v1.1 立 5 例 → VV 一轮 R1～R4 后 10 例 → VV 二轮 R1/R3 后 17 例）：
① 指纹缺失必 FAIL · ② denylist 命中必 FAIL · ③ manifest 失配必 FAIL
· ④ ledger_md 指回指路 stub（type: pointer）必 FAIL（判据集 v1.1 指路门禁 · 2026-11-06 Doctor 批）
· ⑤ ledger_pointer 指向非 pointer 文件（指路链断裂）必 FAIL（v1.1 双判据负向）
· ⑥ mirror 正文 denylist 命中必 FAIL（R1 · 隔离 mirror 注入 `<p>建议上修</p>` + 重算 manifest 行）
· ⑦ mirror 勘误语境按合同豁免、不误报（R1 正向 · 注入行含 exempt_line_keywords → 完整 gate 仍 exit 0）
· ⑧ 真本路径只在 pointer 的 frontmatter 出现、正文指错目标 → 必 FAIL（R2）
· ⑨ 真本副本 frontmatter 写 `type: pointer # 注释`（合法 YAML 行尾注释）→ 必判 pointer、FAIL（R3）
· ⑩ 真本副本 `type: "pointer`（引号不闭合、不可靠解析）→ 必 FAIL、不默认放行为真本（R3）
· ⑪ 真本副本 `type: "po\\u0069nter"`（双引号转义，标量值＝pointer）→ 判 pointer、FAIL（二轮 R3）
· ⑫ 真本副本有起始 `---` 但无闭合分隔符 → bad、FAIL（二轮 R3）
· ⑬ 真本副本闭合分隔符落在 4096 B 读取上限之外 → bad、FAIL（二轮 R3）
· ⑭ 对照：真本副本无 frontmatter（纯正文）→ plain，完整 gate exit 0（二轮 R3 正向）
· ⑮ 对照：真本副本 `type: framework` 正常闭合 → plain，完整 gate exit 0（二轮 R3 正向）
· ⑯ mirror 同行双标题 `<h2>勘误注</h2><h2>现行结论</h2>` 后一行命中 → 必 FAIL（二轮 R1）
· ⑰ mirror 分行双标题（同上拆两行）后一行命中 → 必 FAIL（二轮 R1）
每例：隔离副本（判据集 json 与被注入文件均落临时目录；真本/指路副本按 EAL 根布局 `EAL/frameworks/` + `EAL/archive/x/` 成对构造，
指路正文指向副本真本，使判据 5 只因被测分支而 FAIL）→ 以 --checks 指向副本跑**完整** gate → 断言退出码与证据行。
框架自身不用 assert 语句（-O 会剥离）；判定一律显式 raise AssertionError。
优化模式（R4）：子进程显式传播父进程的 -O 层数（sys.flags.optimize），起手实测子进程 optimize 并打印；
父子不一致即中止——「-O 下 N/N」才真正证明 gate 在优化模式下的行为。
Run: python3 test_gate_self.py / python3 -O test_gate_self.py（都应 exit 0）；
     --only 11,12,16 只跑指定用例（定向复验用；汇总行标明「子集」，不作全集证据）。
"""
import argparse, hashlib, json, os, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
GATE = os.path.join(HERE, "eal_gate_check.py")
CHECKS = os.path.join(HERE, "eal_gate_checks.json")
OPT_FLAGS = ["-O"] * sys.flags.optimize          # R4：显式传播优化层数

def _root():
    env = os.environ.get("EAL_DOCUMENTS_ROOT")
    if env:
        return os.path.normpath(env)
    home = os.path.expanduser("~")
    if not os.path.isdir(os.path.join(home, "Documents")):
        sys.exit("前置条件不满足：EAL_DOCUMENTS_ROOT 未设且 ~/Documents 不存在——"
                 "沙箱请 export EAL_DOCUMENTS_ROOT=<Documents 根>")
    return home

def _p(rel):
    return rel if os.path.isabs(rel) else os.path.join(_root(), rel)

def _base_cfg():
    with open(CHECKS, encoding="utf-8") as f:
        return json.load(f)

def _mutate(edits, workdir=None):
    """edits: callable(cfg)->None；写临时副本，返回副本路径"""
    cfg = _base_cfg()
    edits(cfg)
    fd, path = tempfile.mkstemp(suffix=".json", prefix="gate_self_", dir=workdir)
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=1)
    return path

def _child_optimize():
    r = subprocess.run([sys.executable, *OPT_FLAGS, "-c", "import sys;print(sys.flags.optimize)"],
                       capture_output=True, text=True, timeout=30)
    return int((r.stdout or "-1").strip() or -1)

def _run_gate(checks_path):
    env = dict(os.environ)
    env.setdefault("EAL_DOCUMENTS_ROOT", _root())
    argv = [sys.executable, *OPT_FLAGS, GATE, "--checks", checks_path]
    r = subprocess.run(argv, capture_output=True, text=True, timeout=900, env=env)
    return r.returncode, r.stdout

def _expect_fail(case_name, checks_path, expect_line):
    rc, out = _run_gate(checks_path)
    if rc == 0:
        raise AssertionError(f"[{case_name}] 注入破坏后 gate 仍 exit 0：\n{out[-1500:]}")
    if "FAIL" not in out:
        raise AssertionError(f"[{case_name}] exit={rc} 但输出无 FAIL：\n{out[-1500:]}")
    if expect_line is not None and expect_line not in out:
        raise AssertionError(f"[{case_name}] 输出缺预期证据行 {expect_line!r}：\n{out[-1500:]}")
    print(f"[PASS] {case_name}")

def _expect_pass(case_name, checks_path, expect_line):
    rc, out = _run_gate(checks_path)
    if rc != 0:
        raise AssertionError(f"[{case_name}] 正向对照被误报，gate exit={rc}：\n{out[-1500:]}")
    if expect_line is not None and expect_line not in out:
        raise AssertionError(f"[{case_name}] 输出缺预期证据行 {expect_line!r}：\n{out[-1500:]}")
    print(f"[PASS] {case_name}")

class _Case:
    """每例独立临时目录，退出时整目录删除"""
    def __init__(self, name, positive=False):
        self.name, self.positive = name, positive
    def __enter__(self):
        self.dir = tempfile.mkdtemp(prefix="gate_self_")
        return self
    def __exit__(self, *a):
        shutil.rmtree(self.dir, ignore_errors=True)
    def run(self, edits, expect_line):
        path = _mutate(edits, self.dir)
        (_expect_pass if self.positive else _expect_fail)(self.name, path, expect_line)

def _read(path):
    with open(path, encoding="utf-8", errors="replace") as f:
        return f.read()

def _write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)

# ---------- 原五例（判据集字段注入） ----------
def case1_fingerprint_missing():
    with _Case("① 指纹缺失必 FAIL") as c:
        c.run(lambda cfg: cfg["ledger_fingerprints"]["positive"].append(["GATE_SELF_BOGUS_FP_XYZ", 1]), "正向缺失")

def case2_denylist_hit():
    with _Case("② denylist 命中必 FAIL") as c:
        c.run(lambda cfg: cfg["ledger_fingerprints"]["denylist"].append("FOMC"), "denylist 命中")

def case3_manifest_mismatch():
    with _Case("③ manifest 失配必 FAIL") as c:
        c.run(lambda cfg: cfg["paths"].__setitem__("manifest_key", "gate-self-missing-key"), "manifest")

def case4_ledger_points_to_stub():
    with _Case("④ ledger_md 指回指路 stub 必 FAIL") as c:
        c.run(lambda cfg: cfg["paths"].__setitem__("ledger_md", cfg["paths"]["ledger_pointer"]), "指路 stub")

def case5_pointer_chain_broken():
    with _Case("⑤ ledger_pointer 非指路 stub 必 FAIL") as c:
        c.run(lambda cfg: cfg["paths"].__setitem__("ledger_pointer", cfg["paths"]["ledger_md"]), "非指路 stub")

# ---------- R1：mirror denylist（隔离 mirror + 重算 manifest 行） ----------
def _isolated_mirror(c, inject_html):
    base = _base_cfg()
    src = _p(base["paths"]["mirror_index"])
    dst = os.path.join(c.dir, "mirror", "index.html")
    html = _read(src)
    if "</body>" in html:
        html = html.replace("</body>", inject_html + "\n</body>", 1)
    else:
        html += "\n" + inject_html + "\n"
    _write(dst, html)
    with open(dst, "rb") as f:
        raw = f.read()
    manifest = os.path.join(c.dir, "_artifacts_manifest.txt")
    _write(manifest, f"{base['paths']['manifest_key']}\t{len(raw)}\t{hashlib.sha256(raw).hexdigest()[:12]}\tcopy\tgate-self\n")
    def edits(cfg):
        cfg["paths"]["mirror_index"] = dst
        cfg["paths"]["manifest"] = manifest
    return edits

def case6_mirror_denylist_hit():
    with _Case("⑥ mirror 正文 denylist 命中必 FAIL（R1）") as c:
        c.run(_isolated_mirror(c, "<p>建议上修</p>"), "index.html denylist 命中")

def case7_mirror_exempt_context_passes():
    with _Case("⑦ mirror 勘误语境豁免不误报（R1 正向）", positive=True) as c:
        c.run(_isolated_mirror(c, "<p>勘误注：历史口径曾写「建议上修」，已按 v2.3 修正</p>"),
              "指纹同套全在 · denylist 零命中")

def case16_mirror_two_headings_same_line():
    with _Case("⑯ mirror 同行双标题后命中必 FAIL（二轮 R1）") as c:
        c.run(_isolated_mirror(c, "<h2>勘误注</h2><h2>现行结论</h2>\n<p>建议上修</p>"), "index.html denylist 命中")

def case17_mirror_two_headings_two_lines():
    with _Case("⑰ mirror 分行双标题后命中必 FAIL（二轮 R1）") as c:
        c.run(_isolated_mirror(c, "<h2>勘误注</h2>\n<h2>现行结论</h2>\n<p>建议上修</p>"), "index.html denylist 命中")

# ---------- 隔离 EAL 布局：frameworks/ 指路 stub + archive/x/ 真本副本（指路正文指向副本真本） ----------
def _isolated_eal(c, transform):
    """transform(text)->text 作用于真本副本全文；返回 edits（同时改 ledger_md 与 ledger_pointer）"""
    base = _base_cfg()
    text = _read(_p(base["paths"]["ledger_md"]))
    eal = os.path.join(c.dir, "EAL")
    ledger = os.path.join(eal, "archive", "x", "事件归因台账.md")
    ptr = os.path.join(eal, "frameworks", "事件归因台账.md")
    _write(ledger, transform(text))
    _write(ptr, "---\ntitle: 指路\nstatus: retired\ntype: pointer\n---\n\n# 已归档\n\n"
                "真本移入 `archive/x/事件归因台账.md`（路径相对 EAL 根）。\n")
    def edits(cfg):
        cfg["paths"]["ledger_md"] = ledger
        cfg["paths"]["ledger_pointer"] = ptr
    return edits

def _split_fm(text):
    if not text.startswith("---\n"):
        raise AssertionError("前置：真本无 frontmatter，用例无法构造")
    head, rest = text.split("\n---", 1)
    return head.split("\n"), rest

def _with_type(type_line):
    def t(text):
        lines, rest = _split_fm(text)
        lines = [ln for ln in lines if not ln.startswith("type:")] + [type_line]
        return "\n".join(lines) + "\n---" + rest
    return t

# ---------- R2：真本路径只在 frontmatter ----------
def case8_pointer_path_only_in_frontmatter():
    with _Case("⑧ 真本路径只在 pointer frontmatter、正文指错 → FAIL（R2）") as c:
        base = _base_cfg()
        ledger = _p(base["paths"]["ledger_md"])
        ptr = os.path.join(c.dir, "EAL", "frameworks", "事件归因台账.md")
        want_rel = os.path.relpath(ledger, os.path.join(c.dir, "EAL"))   # 同脚本 pointer_root_up=1 的算法
        _write(ptr, f"---\ntitle: 指路\ntype: pointer\nnote: \"{want_rel}\"\n---\n\n# 已归档\n\n真本见 `wrong-target.md`。\n")
        c.run(lambda cfg: cfg["paths"].__setitem__("ledger_pointer", ptr), "指路链断裂")

# ---------- R3：frontmatter 标量解析 / 闭合 ----------
def case9_pointer_with_trailing_comment():
    with _Case("⑨ 真本副本 `type: pointer # 注释` → 判 pointer、FAIL（R3）") as c:
        c.run(_isolated_eal(c, _with_type("type: pointer # 注释")), "指路 stub（frontmatter type: pointer）")

def case10_unparseable_type():
    with _Case("⑩ 真本副本 `type: \"pointer`（引号不闭合）→ FAIL 不放行（R3）") as c:
        c.run(_isolated_eal(c, _with_type('type: "pointer')), "type 声明不可解析")

def case11_escaped_pointer():
    with _Case("⑪ 真本副本 `type: \"po\\u0069nter\"`（转义）→ 判 pointer、FAIL（二轮 R3）") as c:
        c.run(_isolated_eal(c, _with_type('type: "po\\u0069nter"')), "指路 stub（frontmatter type: pointer）")

def case12_frontmatter_unclosed():
    with _Case("⑫ 真本副本 frontmatter 无闭合分隔符 → FAIL（二轮 R3）") as c:
        def t(text):
            lines, rest = _split_fm(text)
            return "\n".join(lines) + "\n" + rest.lstrip("\n")   # 去掉闭合 ---，正文直接接上
        c.run(_isolated_eal(c, t), "type 声明不可解析")

def case13_frontmatter_close_beyond_limit():
    with _Case("⑬ 真本副本闭合分隔符超出 4096 B 读取上限 → FAIL（二轮 R3）") as c:
        def t(text):
            lines, rest = _split_fm(text)
            lines.append("padding: " + "z" * 5000)
            return "\n".join(lines) + "\n---" + rest
        c.run(_isolated_eal(c, t), "type 声明不可解析")

def case14_no_frontmatter_passes():
    with _Case("⑭ 对照：真本副本无 frontmatter → plain，完整 gate exit 0（二轮 R3 正向）", positive=True) as c:
        def t(text):
            _, rest = _split_fm(text)
            return rest.lstrip("\n")
        c.run(_isolated_eal(c, t), "真本 事件归因台账.md 正向")

def case15_normal_framework_passes():
    with _Case("⑮ 对照：真本副本 `type: framework` 正常闭合 → plain，完整 gate exit 0（二轮 R3 正向）", positive=True) as c:
        c.run(_isolated_eal(c, _with_type("type: framework")), "真本 事件归因台账.md 正向")

CASES = {
    1: case1_fingerprint_missing, 2: case2_denylist_hit, 3: case3_manifest_mismatch,
    4: case4_ledger_points_to_stub, 5: case5_pointer_chain_broken,
    6: case6_mirror_denylist_hit, 7: case7_mirror_exempt_context_passes,
    8: case8_pointer_path_only_in_frontmatter,
    9: case9_pointer_with_trailing_comment, 10: case10_unparseable_type,
    11: case11_escaped_pointer, 12: case12_frontmatter_unclosed, 13: case13_frontmatter_close_beyond_limit,
    14: case14_no_frontmatter_passes, 15: case15_normal_framework_passes,
    16: case16_mirror_two_headings_same_line, 17: case17_mirror_two_headings_two_lines,
}

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default=None, help="逗号分隔用例号，如 11,12,16（定向复验；汇总行标「子集」）")
    args = ap.parse_args()
    sel = sorted({int(x) for x in args.only.split(",")}) if args.only else sorted(CASES)
    bad = [n for n in sel if n not in CASES]
    if bad:
        sys.exit(f"未知用例号 {bad}；可用 1～{len(CASES)}")
    child_opt = _child_optimize()
    print(f"self-test 模式：父进程 optimize={sys.flags.optimize} · 子进程 optimize={child_opt}（实测）· argv 前缀 {[sys.executable, *OPT_FLAGS]}")
    if child_opt != sys.flags.optimize:
        raise AssertionError(f"子进程优化层数 {child_opt} ≠ 父进程 {sys.flags.optimize}（R4 传播失败）")
    for n in sel:
        CASES[n]()
    tag = f"子集 {sel}" if args.only else "全集"
    print(f"test_gate_self: {len(sel)}/{len(sel)} PASS（{tag} · optimize={sys.flags.optimize}）")
