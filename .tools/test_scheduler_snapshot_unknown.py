#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
持久化测试 · 快照面③ 窗口外 unknown 降黄 ＋ 源↔装机判词中立化 ＋ EAL 源目录登记（2026-11-13 加）
=====================================================================================
锁三件事：
  ① 面③ pmset 日志窗口覆盖不到 exp（无法判定）→ state=unknown_window → level=yellow，
     issue 含「日志窗口外·无法判定」；窗口内事件史判「在运行」→ 仍 red（负例防过宽）；
     pmset 本身不可读 → 仍 unknown → red（不放宽）。
  ② 源↔装机 sha 不一致的判词不再预设「改了源没重装」，改为中立「源与装机件不一致」。
  ③ OPS_DIRS 含 EAL plist 源目录（~/Documents 写法）。

跑法：  python3 -B .tools/test_scheduler_snapshot_unknown.py
安全性：夹具在 tempfile 下自建自删；pmset 用打桩替换，不碰真 LaunchAgents / 真 plist / 真 pmset。
"""
import importlib.util
import os
import plistlib
import shutil
import sys
import tempfile
import types
from datetime import datetime, timedelta
from pathlib import Path
from unittest.mock import patch

TOOL = Path(__file__).resolve().parent / "scheduler_snapshot.py"
SPEC = importlib.util.spec_from_file_location("ss_unknown_under_test", TOOL)
SS = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(SS)

OK = True
FIXED_NOW = datetime(2026, 9, 22, 12, 0)


def check(desc, cond, extra=""):
    global OK
    print(f"  {'✓' if cond else '✗'} {desc}" + (f"   {extra}" if extra else ""))
    if not cond:
        OK = False


class _FixedClock:
    @classmethod
    def now(cls, tz=None):
        return FIXED_NOW
    fromtimestamp = staticmethod(datetime.fromtimestamp)
    fromisoformat = staticmethod(datetime.fromisoformat)
    strptime = staticmethod(datetime.strptime)


def _pmset_stub(text=None, exc=None):
    def run(*a, **k):
        if exc:
            raise exc
        return types.SimpleNamespace(stdout=text, returncode=0)
    return run


def pm(t, kind):
    return f"{t:%Y-%m-%d %H:%M:%S} +0800 {kind}  \tsome detail"


def test_machine_state_at():
    print("\n① machine_state_at（真函数，pmset 打桩）")
    exp = datetime(2026, 9, 21, 2, 30)
    # 正例 A：pmset 日志近 30 天内无事件（日志只覆盖更早/为空）→ unknown_window
    with patch.object(SS.subprocess, "run", _pmset_stub("header only\nnothing here\n")):
        st, why = SS.machine_state_at(exp)
    check("窗口内无任何事件 → unknown_window", st == "unknown_window", f"{st} · {why}")
    check("  └ 判词含「日志窗口外·无法判定」", "日志窗口外·无法判定" in why)
    # 正例 B：日志最早事件晚于 exp 且不是 Start（exp 早于覆盖起点）→ unknown_window
    txt = "\n".join([pm(datetime(2026, 9, 21, 6, 0), "Wake"), pm(datetime(2026, 9, 21, 9, 0), "Sleep")])
    with patch.object(SS.subprocess, "run", _pmset_stub(txt)):
        st, why = SS.machine_state_at(exp)
    check("exp 早于日志覆盖起点（首事件 Wake）→ unknown_window", st == "unknown_window", f"{st} · {why}")
    check("  └ 判词含「日志窗口外·无法判定」", "日志窗口外·无法判定" in why)
    # 负例 C：窗口内 exp 前最后事件为 Start → on（仍判红的前提）
    txt = "\n".join([pm(datetime(2026, 9, 20, 22, 0), "Start")])
    with patch.object(SS.subprocess, "run", _pmset_stub(txt)):
        st, why = SS.machine_state_at(exp)
    check("窗口内 exp 前最后事件 Start → on（不得被降级）", st == "on", f"{st} · {why}")
    # 负例 D：pmset 不可读 → 仍 unknown（不属窗口外，不放宽）
    with patch.object(SS.subprocess, "run", _pmset_stub(exc=FileNotFoundError("pmset"))):
        st, why = SS.machine_state_at(exp)
    check("pmset 不可读 → 仍 unknown（不归窗口外）", st == "unknown", f"{st} · {why}")
    # 负例 E（2026-11-13 验收补）：pmset 返回码非 0 / 输出为空 → 仍 unknown（红），不落窗口外黄
    def _rc(rc, out):
        return lambda *a, **k: types.SimpleNamespace(stdout=out, returncode=rc)
    for rc, out in ((1, ""), (0, ""), (0, None), (1, "garbage")):
        with patch.object(SS.subprocess, "run", _rc(rc, out)):
            st, why = SS.machine_state_at(exp)
        check(f"pmset rc={rc} stdout={out!r} → 仍 unknown", st == "unknown", f"{st} · {why}")


def make_plist(d: Path, label, sched, stdout_path):
    p = d / f"{label}.plist"
    p.write_bytes(plistlib.dumps({"Label": label, "StartCalendarInterval": sched,
                                  "ProgramArguments": ["/usr/bin/true"],
                                  "StandardOutPath": stdout_path}))
    return p


@patch.object(SS, "datetime", _FixedClock)
def test_levels_and_wording(tmproot: Path):
    print("\n② scan_launchd 定级（真 machine_state_at · pmset 打桩）＋ ③ 判词中立化")
    la, ops = tmproot / "LaunchAgents", tmproot / "ops"
    la.mkdir(); ops.mkdir()
    old = (FIXED_NOW - timedelta(days=3)).timestamp()
    make_plist(la, "com.zhuzhao.missed", {"Hour": 10, "Minute": 1}, str(tmproot / "m.log"))
    (tmproot / "m.log").write_text("x"); os.utime(tmproot / "m.log", (old, old))
    saved = (SS.LAUNCH_AGENTS, SS.OPS_DIRS, SS.launchctl_loaded)
    SS.LAUNCH_AGENTS, SS.OPS_DIRS = la, [ops]
    SS.launchctl_loaded = lambda label: {"loaded": True, "state": "not running", "last_exit_code": "0"}
    try:
        with patch.object(SS.subprocess, "run", _pmset_stub("header only\nno events\n")):  # 2026-11-13：空输出现判「不可读」红，窗口外用例改为有输出无事件
            f = {x["label"]: x for x in SS.scan_launchd()["staleness"]}.get("com.zhuzhao.missed", {})
        check("正例：日志窗口外 → level=yellow（非 red）", f.get("level") == "yellow", f"level={f.get('level')}")
        check("  └ 仍报出，issue 写明「日志窗口外·无法判定」", "日志窗口外·无法判定" in f.get("issue", ""))
        txt = pm(datetime(2026, 9, 22, 8, 0), "Wake")   # exp=09-22 10:01，前最后事件 Wake → on
        with patch.object(SS.subprocess, "run", _pmset_stub(txt)):
            f = {x["label"]: x for x in SS.scan_launchd()["staleness"]}.get("com.zhuzhao.missed", {})
        check("负例：窗口内确属应跑未跑（机器在运行）→ 仍 red", f.get("level") == "red", f"level={f.get('level')}")

        # ③ 源↔装机 sha 不一致的判词
        make_plist(ops, "com.zhuzhao.drift", {"Hour": 10, "Minute": 1}, str(tmproot / "d.log"))
        p = make_plist(la, "com.zhuzhao.drift", {"Hour": 10, "Minute": 1}, str(tmproot / "d.log"))
        d = plistlib.loads(p.read_bytes()); d["EnvironmentVariables"] = {"PYTHONDONTWRITEBYTECODE": "1"}
        p.write_bytes(plistlib.dumps(d))
        with patch.object(SS.subprocess, "run", _pmset_stub("header only\nno events\n")):  # 2026-11-13：空输出现判「不可读」红，窗口外用例改为有输出无事件
            cons = {x["label"]: x["issue"] for x in SS.scan_launchd()["consistency"]}
        iss = cons.get("com.zhuzhao.drift", "")
        check("sha 不一致 → 报出", bool(iss), iss[:80])
        check("  └ 判词中立：含「源与装机件不一致」", "源与装机件不一致" in iss)
        check("  └ 不再预设方向：不含「改了源没重装」", "改了源没重装" not in iss)

        # ③b EAL 前缀纳入（com.eal.*）：源↔装机比对 ＋ 应跑未跑 都要覆盖
        make_plist(ops, "com.eal.postevent-native", {"Hour": 10, "Minute": 1}, str(tmproot / "e.log"))
        pe = make_plist(la, "com.eal.postevent-native", {"Hour": 10, "Minute": 1}, str(tmproot / "e.log"))
        de = plistlib.loads(pe.read_bytes()); de["EnvironmentVariables"] = {"X": "1"}
        pe.write_bytes(plistlib.dumps(de))
        (tmproot / "e.log").write_text("x"); os.utime(tmproot / "e.log", (old, old))
        make_plist(ops, "com.other.x", {"Hour": 10, "Minute": 1}, str(tmproot / "o.log"))
        po = make_plist(la, "com.other.x", {"Hour": 10, "Minute": 1}, str(tmproot / "o.log"))
        do = plistlib.loads(po.read_bytes()); do["EnvironmentVariables"] = {"X": "1"}
        po.write_bytes(plistlib.dumps(do))      # 同样分叉，但前缀不在 OURS ⇒ 不得报
        txt = pm(datetime(2026, 9, 22, 8, 0), "Wake")
        with patch.object(SS.subprocess, "run", _pmset_stub(txt)):
            r = SS.scan_launchd()
        ce = {x["label"]: x["issue"] for x in r["consistency"]}.get("com.eal.postevent-native", "")
        se = {x["label"]: x for x in r["staleness"]}.get("com.eal.postevent-native", {})
        check("com.eal.* 进入源↔装机比对（sha 不一致被报出、判词中立）",
              "源与装机件不一致" in ce, ce[:60])
        check("com.eal.* 进入应跑未跑检查（窗口内在运行 → red）", se.get("level") == "red",
              f"level={se.get('level')}")
        check("负例：非项目前缀 com.other.* 仍不纳入",
              "com.other.x" not in {x["label"] for x in r["consistency"]})
    finally:
        SS.LAUNCH_AGENTS, SS.OPS_DIRS, SS.launchctl_loaded = saved


def test_ops_dirs():
    print("\n④ OPS_DIRS 登记 EAL plist 源目录")
    want = Path.home() / "Documents/Claude/Projects/Financial/宏观研究体系/EAL/调度/eal-post-event-native"
    check("OPS_DIRS 含 EAL 源目录（~/Documents 写法）", want in SS.OPS_DIRS, f"{[str(x) for x in SS.OPS_DIRS]}")
    check("原烛照九阴 ops 目录仍在（不误删）",
          Path.home() / "Documents/Claude/Projects/Financial/烛照九阴/ops" in SS.OPS_DIRS)


def main():
    tmproot = Path(tempfile.mkdtemp(prefix="ss_unknown_test_"))
    print("持久化测试 · 面③ 窗口外 unknown 降黄 / 判词中立化 / EAL 登记")
    try:
        test_ops_dirs()                 # 先跑：其余用例会临时改 OPS_DIRS（finally 还原）
        test_machine_state_at()
        test_levels_and_wording(tmproot)
    finally:
        shutil.rmtree(tmproot, ignore_errors=True)
    print(f"\n{'✅ 全过' if OK else '❌ 有失败项'}")
    return 0 if OK else 1


if __name__ == "__main__":
    sys.exit(main())
