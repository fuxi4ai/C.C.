#!/usr/bin/env python3
"""eal_gate_check.py 自身 fail-fast（PRD 2026-08-17 §二 D：注入破坏后 gate 必报 FAIL）

三用例：① 指纹缺失必 FAIL · ② denylist 命中必 FAIL · ③ manifest 失配必 FAIL。
每例：/tmp 篡改判据集副本 → 以 --checks 指向副本跑 gate → 断言 exit 非零且输出含 FAIL。
框架自身不用 assert 语句（-O 会剥离）；判定一律显式 raise AssertionError。
Run: python3 test_gate_self.py（普通与 -O 都应 exit 0）。
"""
import json, os, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
GATE = os.path.join(HERE, "eal_gate_check.py")
CHECKS = os.path.join(HERE, "eal_gate_checks.json")

def _root():
    env = os.environ.get("EAL_DOCUMENTS_ROOT")
    if env:
        return os.path.normpath(env)
    home = os.path.expanduser("~")
    if not os.path.isdir(os.path.join(home, "Documents")):
        sys.exit("前置条件不满足：EAL_DOCUMENTS_ROOT 未设且 ~/Documents 不存在——"
                 "沙箱请 export EAL_DOCUMENTS_ROOT=<Documents 根>")
    return home

def _mutate(edits):
    """edits: callable(cfg)->None；写 /tmp 副本，返回副本路径"""
    cfg = json.load(open(CHECKS, encoding="utf-8"))
    edits(cfg)
    fd, path = tempfile.mkstemp(suffix=".json", prefix="gate_self_")
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=1)
    return path

def _run_gate(checks_path):
    env = dict(os.environ)
    env.setdefault("EAL_DOCUMENTS_ROOT", _root())
    r = subprocess.run([sys.executable, GATE, "--checks", checks_path],
                       capture_output=True, text=True, timeout=900, env=env)
    return r.returncode, r.stdout

def _expect_fail(case_name, edits, expect_line):
    path = _mutate(edits)
    try:
        rc, out = _run_gate(path)
    finally:
        try:
            os.unlink(path)
        except OSError:
            pass
    if rc == 0:
        raise AssertionError(f"[{case_name}] 注入破坏后 gate 仍 exit 0：\n{out[-1500:]}")
    if "FAIL" not in out:
        raise AssertionError(f"[{case_name}] exit={rc} 但输出无 FAIL：\n{out[-1500:]}")
    if expect_line is not None and expect_line not in out:
        raise AssertionError(f"[{case_name}] 输出缺预期证据行 {expect_line!r}：\n{out[-1500:]}")
    print(f"[PASS] {case_name}")

def case1_fingerprint_missing():
    def edits(cfg):
        cfg["ledger_fingerprints"]["positive"].append(["GATE_SELF_BOGUS_FP_XYZ", 1])
    _expect_fail("① 指纹缺失必 FAIL", edits, "正向缺失")

def case2_denylist_hit():
    def edits(cfg):
        cfg["ledger_fingerprints"]["denylist"].append("FOMC")
    _expect_fail("② denylist 命中必 FAIL", edits, "denylist 命中")

def case3_manifest_mismatch():
    def edits(cfg):
        cfg["paths"]["manifest_key"] = "gate-self-missing-key"
    _expect_fail("③ manifest 失配必 FAIL", edits, "manifest")

if __name__ == "__main__":
    case1_fingerprint_missing()
    case2_denylist_hit()
    case3_manifest_mismatch()
    print("test_gate_self: 3/3 PASS")
