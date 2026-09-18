#!/usr/bin/env python3
"""EAL gate 验收脚本（VV 判据机器化 · PRD 2026-08-17 · 判据集外置 eal_gate_checks.json）

一键跑完整验收链：gate 全绿是「A 阶段完成」声明的**必要不充分条件**（VV 仍终审）。
路径解析：优先 env EAL_DOCUMENTS_ROOT（沙箱覆盖），缺省 ~（Mac 原生）。
输出契约：每项 [PASS/FAIL/WARN] + FAIL 精确证据行；汇总行；任一 FAIL → exit 1。
WARN 不改变退出码，但汇总行明示「未达全 PASS，不可声明完成」——仅按 exit code 判读的调用方须注意。
用法：python3 eal_gate_check.py [--checks /path/to/json]
"""
import json, os, re, sys, subprocess, hashlib, argparse

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
    except FileNotFoundError as e:
        return -127, "", f"command not found: {e}"
    except subprocess.TimeoutExpired:
        return -124, "", f"timeout after {timeout}s"

def _lines_ok(text):
    return len(re.findall(r": OK$", text, re.M))

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

    # ---- 1. 环境 ----
    rc, out, err = _run(["python3", "--version"], cwd="/tmp", timeout=30)
    py_ok = cfg["environment"]["python_prefix"] in (out + err)
    rc, out, err = _run(["python3", "-c",
                         "import statsmodels;print(statsmodels.__version__)"],
                        cwd="/tmp", timeout=60)
    sm_ver = (out + err).strip().splitlines()[-1] if (out + err).strip() else "?"
    sm_ok = sm_ver == cfg["environment"]["statsmodels"]
    if py_ok and sm_ok:
        results.append((1, "环境", "PASS", f"python 3.10.x · statsmodels {sm_ver}"))
    else:
        results.append((1, "环境", "FAIL",
                        f"python_prefix={'OK' if py_ok else 'FAIL'} · "
                        f"statsmodels={sm_ver}（期望 {cfg['environment']['statsmodels']}）"))

    repro = _p(root, cfg["paths"]["repro_dir"])
    env_full = dict(os.environ)
    env_full.setdefault("EAL_DOCUMENTS_ROOT", root)

    # ---- 2. 复现 ----
    rc, out, err = _run(cfg["repro"]["cmd"], cwd=repro,
                        timeout=cfg["repro"]["timeout_s"], env=env_full)
    missing = [s for s in cfg["repro"]["expected"] if s not in out]
    if rc == 0 and not missing:
        results.append((2, "复现", "PASS", f"estimate_m4.py exit 0 · {len(cfg['repro']['expected'])} 期望串全在"))
    else:
        results.append((2, "复现", "FAIL",
                        f"exit={rc} · 缺失 {len(missing)} 串: {missing[:6]}{'…' if len(missing)>6 else ''}"))

    # ---- 3. fail-fast ----
    rc1, out1, err1 = _run(cfg["failfast"]["cmd"], cwd=repro,
                           timeout=cfg["failfast"]["timeout_s"], env=env_full)
    rc2, out2, err2 = _run(cfg["failfast"]["cmd_o"], cwd=repro,
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

    # ---- 5. canonical 指纹 ----
    ledger = _p(root, cfg["paths"]["ledger_md"])
    try:
        text = open(ledger, encoding="utf-8").read()
    except OSError as e:
        results.append((5, "canonical 指纹", "FAIL", f"台账不可读: {e}"))
        text = None
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
            results.append((5, "canonical 指纹", "PASS",
                            f"正向 {len(cfg['ledger_fingerprints']['positive'])} 项全在 · denylist 零命中"))
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
