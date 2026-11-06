#!/usr/bin/env python3
"""EAL gate 验收脚本（VV 判据机器化 · PRD 2026-08-17 · 判据集外置 eal_gate_checks.json）

一键跑完整验收链：gate 全绿是「A 阶段完成」声明的**必要不充分条件**（VV 仍终审）。
路径解析：优先 env EAL_DOCUMENTS_ROOT（沙箱覆盖），缺省 ~（Mac 原生）。
解释器解析（判据集 v1.1 · 2026-11-06 Doctor 批）：env EAL_GATE_PYTHON → 判据集 environment.python_cmd
（相对 root·存在才用）→ PATH python3；判据 1/2/3 统一用解析出的解释器。环境不就绪 → 判据 1 FAIL，
判据 2/3 不空跑、直接 FAIL（fail-closed，不降 WARN）。
指路门禁（v1.1）：判据集 paths.* 指向的 .md 若 frontmatter `type: pointer` 且键不在 pointer_keys → 判失效 FAIL；
判据 5 为双判据：ledger_pointer 指路有效（type: pointer + 正文含真本相对路径）+ ledger_md 真本指纹。
输出契约：每项 [PASS/FAIL/WARN] + FAIL 精确证据行；汇总行；任一 FAIL → exit 1。
WARN 不改变退出码，但汇总行明示「未达全 PASS，不可声明完成」——仅按 exit code 判读的调用方须注意。
用法：python3 eal_gate_check.py [--checks /path/to/json]
"""
import json, os, re, sys, subprocess, hashlib, argparse, unicodedata

EXIT_OK = 0
EXIT_FAIL = 1

def _root():
    env = os.environ.get("EAL_DOCUMENTS_ROOT")
    if env:
        return os.path.normpath(env)
    return os.path.expanduser("~")

def _p(root, rel):
    return os.path.join(root, rel)

def _run(cmd, cwd, timeout, env=None):
    """run subprocess; return (exitcode, stdout, stderr)"""
    try:
        r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True,
                           timeout=timeout, env=env)
        return r.returncode, r.stdout, r.stderr
    except OSError as e:  # FileNotFoundError / PermissionError（非可执行或目录路径）等一律不崩溃、给证据
        return -127, "", f"command not runnable: {e}"
    except subprocess.TimeoutExpired:
        return -124, "", f"timeout after {timeout}s"

def _lines_ok(text):
    return len(re.findall(r": OK$", text, re.M))

def _nfc(s):
    return unicodedata.normalize("NFC", s)

# ---- 解释器解析（v1.1）----
def _resolve_python(cfg, root):
    """返回 (interpreter, source)。顺序：env EAL_GATE_PYTHON → cfg python_cmd（相对 root，存在才用）→ PATH python3"""
    env = os.environ.get("EAL_GATE_PYTHON")
    if env:
        return env, "env EAL_GATE_PYTHON"
    rel = cfg.get("environment", {}).get("python_cmd")
    if rel:
        cand = rel if os.path.isabs(rel) else _p(root, rel)
        if os.path.isfile(cand) and os.access(cand, os.X_OK):
            return cand, f"判据集 python_cmd（{rel}）"
    return "python3", "PATH python3"

def _ver_tuple(s):
    parts = re.findall(r"\d+", s)
    return tuple(int(x) for x in parts[:3]) + (0,) * (3 - len(parts[:3]))

def _in_range(ver, spec):
    """spec 形如 '>=3.10,<3.14'；只支持 >=,>,<=,<,==,!= 的逗号合取（不引入 packaging 依赖）"""
    v = _ver_tuple(ver)
    for clause in spec.split(","):
        clause = clause.strip()
        m = re.match(r"(>=|<=|==|!=|>|<)\s*([\d.]+)$", clause)
        if not m:
            return False
        op, bound = m.group(1), _ver_tuple(m.group(2))
        n = len(re.findall(r"\d+", m.group(2)))
        vv = v if op in (">=", ">", "<=", "<") else v[:n]
        bb = bound if op in (">=", ">", "<=", "<") else bound[:n]
        ok = {">=": vv >= bb, ">": vv > bb, "<=": vv <= bb, "<": vv < bb,
              "==": vv == bb, "!=": vv != bb}[op]
        if not ok:
            return False
    return True

# ---- 指路门禁（v1.1）----
_FM_RE = re.compile(r"\A---\s*\n(.*?)\n---", re.S)

def _frontmatter(path):
    try:
        head = open(path, encoding="utf-8").read(4096)
    except OSError:
        return None
    m = _FM_RE.match(head)
    if not m:
        return {}
    fm = {}
    for ln in m.group(1).splitlines():
        if ":" in ln:
            k, _, v = ln.partition(":")
            fm[k.strip()] = v.strip().strip('"').strip("'")
    return fm

def _is_pointer(path):
    fm = _frontmatter(path)
    return bool(fm) and fm.get("type") == "pointer"

def _pointer_violations(cfg, root):
    """paths.* 指向 .md 且键不在 pointer_keys：若 type: pointer → 判据集失效"""
    allow = set(cfg.get("pointer_keys", []))
    out = []
    for key, rel in cfg["paths"].items():
        if key in allow or not str(rel).endswith(".md"):
            continue
        ap = _p(root, rel)
        if os.path.isfile(ap) and _is_pointer(ap):
            out.append((key, rel))
    return out

def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--checks", default=None,
                    help="判据集 json 路径（默认与本脚本同目录 eal_gate_checks.json）")
    args = ap.parse_args(argv)

    here = os.path.dirname(os.path.abspath(__file__))
    json_path = args.checks or os.path.join(here, "eal_gate_checks.json")
    with open(json_path, encoding="utf-8") as f:
        cfg = json.load(f)
    root = _root()

    results = []  # (num, name, status, evidence)
    violations = _pointer_violations(cfg, root)
    viol_keys = {k for k, _ in violations}

    # ---- 1. 环境 ----
    py, py_src = _resolve_python(cfg, root)
    envc = cfg["environment"]
    spec = envc.get("python_range") or envc.get("python_prefix", "")
    rc, out, err = _run([py, "-c", "import platform;print(platform.python_version())"],
                        cwd="/tmp", timeout=30)
    py_ver = (out or "").strip().splitlines()[-1] if (out or "").strip() else None
    if py_ver is None:
        py_ok = False
    elif envc.get("python_range"):
        py_ok = _in_range(py_ver, spec)
    else:  # 兼容 v1 的 python_prefix 字面前缀（如 "Python 3.10"）：去 "Python " 后按版本号前缀比
        py_ok = py_ver.startswith(spec.replace("Python", "").strip())
    rc, out, err = _run([py, "-c", "import statsmodels;print(statsmodels.__version__)"],
                        cwd="/tmp", timeout=60)
    sm_ver = (out + err).strip().splitlines()[-1] if (out + err).strip() else "?"
    sm_ok = sm_ver == envc["statsmodels"]
    env_ready = py_ok and sm_ok
    if env_ready:
        results.append((1, "环境", "PASS",
                        f"python {py_ver}（{py} · {py_src}）∈ {spec} · statsmodels {sm_ver}"))
    else:
        ev = (f"复现环境未就绪：解释器 {py}（{py_src}）· python={py_ver or '不可运行:' + err.strip()[:60]}"
              f"（期望 {spec}）{'OK' if py_ok else 'FAIL'} · statsmodels={sm_ver}（期望 {envc['statsmodels']}）"
              f"{'OK' if sm_ok else 'FAIL'}；建环境见 repro_v23/README.md + requirements.lock.txt，"
              f"或 export EAL_GATE_PYTHON=<解释器>")
        results.append((1, "环境", "FAIL", ev))

    repro = _p(root, cfg["paths"]["repro_dir"])
    env_full = dict(os.environ)
    env_full.setdefault("EAL_DOCUMENTS_ROOT", root)

    def _with_py(cmd):
        return [py if c == "python3" else c for c in cmd]

    # ---- 2. 复现 ----
    if not env_ready:
        results.append((2, "复现", "FAIL", "前置判据 1 未过（复现环境未就绪）· 未实跑 estimate_m4.py"))
    else:
        rc, out, err = _run(_with_py(cfg["repro"]["cmd"]), cwd=repro,
                            timeout=cfg["repro"]["timeout_s"], env=env_full)
        missing = [s for s in cfg["repro"]["expected"] if s not in out]
        if rc == 0 and not missing:
            results.append((2, "复现", "PASS", f"estimate_m4.py exit 0 · {len(cfg['repro']['expected'])} 期望串全在（{py}）"))
        else:
            results.append((2, "复现", "FAIL",
                            f"exit={rc} · 缺失 {len(missing)} 串: {missing[:6]}{'…' if len(missing)>6 else ''}"
                            f"{' · stderr: ' + err.strip().splitlines()[-1][:120] if rc != 0 and err.strip() else ''}"))

    # ---- 3. fail-fast ----
    if not env_ready:
        results.append((3, "fail-fast", "FAIL", "前置判据 1 未过（复现环境未就绪）· 未实跑 test_failfast.py"))
    else:
        rc1, out1, err1 = _run(_with_py(cfg["failfast"]["cmd"]), cwd=repro,
                               timeout=cfg["failfast"]["timeout_s"], env=env_full)
        rc2, out2, err2 = _run(_with_py(cfg["failfast"]["cmd_o"]), cwd=repro,
                               timeout=cfg["failfast"]["timeout_s"], env=env_full)
        if rc1 == 0 and rc2 == 0:
            results.append((3, "fail-fast", "PASS", "test_failfast.py 普通与 -O 双模式 exit 0"))
        else:
            results.append((3, "fail-fast", "FAIL", f"普通 exit={rc1} · -O exit={rc2}"))

    # ---- 4. SHA ----
    rc, out, err = _run(cfg["sha"]["cmd"], cwd=repro, timeout=120)
    n_ok = _lines_ok(out)
    if rc == 0 and n_ok == cfg["sha"]["expect_lines_ok"]:
        results.append((4, "SHA", "PASS", f"shasum -c 八项全 OK"))
    else:
        results.append((4, "SHA", "FAIL", f"exit={rc} · OK 行 {n_ok}/{cfg['sha']['expect_lines_ok']}"))

    # ---- 5. canonical 指纹（v1.1 双判据：指路有效 + 真本指纹）----
    ledger = _p(root, cfg["paths"]["ledger_md"])
    pre_fail = []
    if "ledger_md" in viol_keys:
        pre_fail.append(f"ledger_md 指向指路 stub（frontmatter type: pointer）→ 判据集路径失效: {cfg['paths']['ledger_md']}")
    ptr_rel = cfg["paths"].get("ledger_pointer")
    if ptr_rel:
        ptr = _p(root, ptr_rel)
        up = int(cfg.get("pointer_contract", {}).get("pointer_root_up", 1))
        eal_root = os.path.dirname(ptr)
        for _ in range(up):
            eal_root = os.path.dirname(eal_root)
        want_rel = _nfc(os.path.relpath(ledger, eal_root))
        if not os.path.isfile(ptr):
            pre_fail.append(f"ledger_pointer 不存在: {ptr_rel}")
        elif not _is_pointer(ptr):
            pre_fail.append(f"ledger_pointer 非指路 stub（frontmatter 无 type: pointer）: {ptr_rel}")
        else:
            body = _nfc(open(ptr, encoding="utf-8").read())
            if want_rel not in body:
                pre_fail.append(f"ledger_pointer 正文未含真本相对路径 {want_rel!r}（指路链断裂）")
        if not os.path.isfile(ledger):
            pre_fail.append(f"ledger_md 真本不存在: {cfg['paths']['ledger_md']}")
    text = None
    if not pre_fail:
        try:
            text = open(ledger, encoding="utf-8").read()
        except OSError as e:
            pre_fail.append(f"台账不可读: {e}")
    if pre_fail:
        results.append((5, "canonical 指纹", "FAIL", " | ".join(pre_fail)))
    if text is not None:
        pos_fail = []
        for s, minc in cfg["ledger_fingerprints"]["positive"]:
            c = text.count(s)
            if c < minc:
                pos_fail.append(f"{s!r}={c}<{minc}")
        # 豁免两级：段级（##/### 标题含 exempt_section_keywords → 整段不查）
        #         + 行级（命中行本身含 exempt_line_keywords → 该行放行）
        sec_kw = cfg["ledger_fingerprints"]["exempt_section_keywords"]
        line_kw = cfg["ledger_fingerprints"]["exempt_line_keywords"]
        denylist_hits = []
        lines = text.splitlines()
        in_exempt = False
        for i, ln in enumerate(lines, 1):
            s = ln.strip()
            if s.startswith("##"):
                in_exempt = any(k in s for k in sec_kw)
                continue
            if s.startswith("# "):
                in_exempt = False
                continue
            if in_exempt:
                continue
            if any(k in ln for k in line_kw):
                continue
            for kw in cfg["ledger_fingerprints"]["denylist"]:
                if kw in ln:
                    denylist_hits.append(f"{kw!r} @ L{i}: {ln.strip()[:80]}")
        if not pos_fail and not denylist_hits:
            ptr_note = f" · 指路 stub 有效（{os.path.basename(ptr_rel)} → {want_rel}）" if ptr_rel else ""
            results.append((5, "canonical 指纹", "PASS",
                            f"真本 {os.path.basename(ledger)} 正向 {len(cfg['ledger_fingerprints']['positive'])} 项全在 · denylist 零命中{ptr_note}"))
        else:
            ev = []
            if pos_fail:
                ev.append(f"{os.path.basename(ledger)} 正向缺失: " + " / ".join(pos_fail[:5]))
            if denylist_hits:
                ev.append(f"{os.path.basename(ledger)} denylist 命中: " + " / ".join(denylist_hits[:5]))
            results.append((5, "canonical 指纹", "FAIL", " | ".join(ev)))

    # ---- 6. 载体一致（mirror 黑盒同套指纹 + manifest 对拍）----
    mirror = _p(root, cfg["paths"]["mirror_index"])
    manifest = _p(root, cfg["paths"]["manifest"])
    key = cfg["paths"]["manifest_key"]
    try:
        mbytes = os.path.getsize(mirror)
        sha12 = hashlib.sha256(open(mirror, "rb").read()).hexdigest()[:12]
    except OSError as e:
        results.append((6, "载体一致", "FAIL", f"mirror 不可读: {e}"))
        mbytes = sha12 = None
    if mbytes is not None:
        row = None
        try:
            for ln in open(manifest, encoding="utf-8"):
                parts = ln.rstrip("\n").split("\t")
                if parts and parts[0] == key:
                    row = parts
                    break
        except OSError as e:
            results.append((6, "载体一致", "FAIL", f"manifest 不可读: {e}"))
            row = None
        if row is not None:
            m_ok = (len(row) >= 3 and int(row[1]) == mbytes and row[2] == sha12)
            mtext = open(mirror, encoding="utf-8", errors="replace").read()
            ovr = cfg["ledger_fingerprints"].get("mirror_positive_overrides", {})
            pos_fail = [s for s, minc in cfg["ledger_fingerprints"]["positive"]
                        if mtext.count(ovr.get(s, s)) < minc]
            if m_ok and not pos_fail:
                results.append((6, "载体一致", "PASS",
                                f"manifest 行对拍（{mbytes} B · {sha12}）· 指纹同套全在"))
            else:
                ev = []
                if not m_ok:
                    ev.append(f"{os.path.basename(manifest)} 失配: 盘 {mbytes}/{sha12} vs 行 {row[1] if len(row)>1 else '?'}/{row[2] if len(row)>2 else '?'}")
                if pos_fail:
                    ev.append(f"{os.path.basename(mirror)} 指纹缺失: {pos_fail[:5]}")
                results.append((6, "载体一致", "FAIL", " | ".join(ev)))
        else:
            results.append((6, "载体一致", "FAIL", f"manifest 无 {key!r} 行"))

    # ---- 7. 快照真源 ----
    snap = _p(root, cfg["paths"]["snapshot_script"])
    try:
        stext = open(snap, encoding="utf-8").read()
    except OSError as e:
        results.append((7, "快照真源", "FAIL", f"脚本不可读: {e}"))
        stext = ""
    if stext:
        hit = [ln for ln in stext.splitlines()
               if "ARTIFACTS_TREE" in ln and "Gateway-workspace" in ln and "Artifacts" in ln]
        if hit:
            results.append((7, "快照真源", "PASS", f"ARTIFACTS_TREE→Gateway-workspace/Artifacts（{hit[0].strip()[:90]}）"))
        else:
            results.append((7, "快照真源", "FAIL", "ARTIFACTS_TREE 未指向 Gateway-workspace/Artifacts"))

    # ---- 8. 发布器保险丝 ----
    pub = _p(root, cfg["paths"]["publisher"])
    try:
        ptext = open(pub, encoding="utf-8").read()
    except OSError as e:
        results.append((8, "发布器保险丝", "FAIL", f"发布器不可读: {e}"))
        ptext = ""
    if ptext:
        missing = [m for m in cfg["publisher_static"]["expected_markers"] if m not in ptext]
        if not missing:
            results.append((8, "发布器保险丝", "PASS",
                            f"v3 形态静态标记全在: {cfg['publisher_static']['expected_markers']}"
                            f"（判据 8 经 2026-09-18 Doctor 裁改写为 v3 形态：默认 preflight-only+授权 token）"))
        else:
            results.append((8, "发布器保险丝", "FAIL",
                            f"静态标记缺失: {missing}（{os.path.basename(pub)}）"))

    # ---- 指路门禁兜底：ledger_md 之外的 paths.* md 若为 pointer，单列 FAIL（当前判据集无此类键，仅防未来增补漏查）----
    other = [(k, r) for k, r in violations if k != "ledger_md"]
    if other:
        results.append((9, "路径有效性", "FAIL",
                        "paths.* 指向指路 stub（type: pointer）→ 判据集失效: " + " / ".join(f"{k}={r}" for k, r in other)))

    # ---- 汇总 ----
    n_pass = sum(1 for r in results if r[2] == "PASS")
    n_warn = sum(1 for r in results if r[2] == "WARN")
    n_fail = sum(1 for r in results if r[2] == "FAIL")
    for num, name, status, ev in results:
        print(f"[{status}] {num}. {name}")
        if ev:
            print(f"        {ev}")
    print("未验（需 Mac 原生）：Gateway active 层自动检查（PRD §二 C 本期不覆盖）")
    if n_fail == 0 and n_warn == 0:
        print(f"gate: {n_pass}/{len(results)} PASS → 可声明「A 阶段完成」（VV 终审仍必需）")
        return EXIT_OK
    elif n_fail == 0:
        print(f"gate: {n_pass} PASS · {n_warn} WARN · 0 FAIL → 未达全 PASS，不可声明「A 阶段完成」")
        return EXIT_OK
    else:
        print(f"gate: {n_pass} PASS · {n_warn} WARN · {n_fail} FAIL → 不可声明完成（详见 FAIL 证据行）")
        return EXIT_FAIL

if __name__ == "__main__":
    sys.exit(main())
