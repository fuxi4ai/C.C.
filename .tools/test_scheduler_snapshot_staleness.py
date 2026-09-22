#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
持久化负向测试 · 快照面③「应跑未跑」检查（2026-09-22 加）
=========================================================
锁两件事：
  ① `expected_last_fire()` 的排期推算 —— 尤其 **launchd Weekday 语义**
     （0/7=周日、1=周一…6=周六）到 Python `weekday()`（0=周一…6=周日）的映射。
     这条映射错了会在周末静默误报，正是 G-X122 最怕的那种。
  ② `scan_launchd()` 的四道防误报闸：grace 窗 / running / 无 StandardOutPath / /tmp 落点。

动机（实撞）：2026-09-22 快照只显示 `com.zhuzhao.marketdata` last exit=1，
而该 job 在 09-17/09-18/09-21 三个交易日**脚本从未被启动**（自管日志无文件），
本面对「漏跑」零可见度 —— 是漏报，不是报错。

跑法：  python3 .tools/test_scheduler_snapshot_staleness.py
安全性：全程只读仓库；夹具在 tempfile 目录下自建自删，不碰真 LaunchAgents / 真 plist。
"""
import importlib.util
import os
import plistlib
import shutil
import sys
import tempfile
from datetime import datetime, timedelta
from pathlib import Path

TOOL = Path(__file__).resolve().parent / "scheduler_snapshot.py"
SPEC = importlib.util.spec_from_file_location("ss_under_test", TOOL)
SS = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(SS)          # 模块级只有常量与函数定义，导入即安全（无写盘）

OK = True


def check(desc, cond, extra=""):
    global OK
    print(f"  {'✓' if cond else '✗'} {desc}" + (f"   {extra}" if extra else ""))
    if not cond:
        OK = False


def dt(s):
    return datetime.strptime(s, "%Y-%m-%d %H:%M")


# ───────────────── ① expected_last_fire 纯函数 ─────────────────
def test_expected_last_fire():
    print("\n① expected_last_fire · 排期推算与 Weekday 映射")
    D = "2026-09-22"                      # 周二（09-19 周六 → 09-20 周日 → 09-21 周一 → 09-22 周二）
    tue_only = {"Weekday": 2, "Hour": 2, "Minute": 30}                 # 仅周二
    mon_fri = [{"Weekday": w, "Hour": 2, "Minute": 30} for w in (1, 2, 3, 4, 5)]   # 真实 marketdata 排期
    cases = [
        # 单条 Weekday=2：最近一次「周二 02:30」——注意周日/周一/周六都只能回溯到上周二
        ("仅周二 · 周二 10:00 → 当日 02:30", tue_only, f"{D} 10:00", f"{D} 02:30"),
        ("仅周二 · 周一 01:00 → 上周二 02:30（09-15）", tue_only, "2026-09-21 01:00", "2026-09-15 02:30"),
        # 周一~五列表：weekday 映射与「取最近一次」的正式用例
        ("周一~五 · 周二 10:00 → 当日 02:30", mon_fri, f"{D} 10:00", f"{D} 02:30"),
        ("周一~五 · 周一 01:00 → 上周五 02:30", mon_fri, "2026-09-21 01:00", "2026-09-18 02:30"),
        ("周一~五 · 周日 12:00 → 上周五 02:30", mon_fri, "2026-09-20 12:00", "2026-09-18 02:30"),
        ("周一~五 · 周六 12:00 → 上周五 02:30", mon_fri, "2026-09-19 12:00", "2026-09-18 02:30"),
        ("周一~五 · 周五 03:00 → 当日 02:30", mon_fri, "2026-09-18 03:00", "2026-09-18 02:30"),
        # 每日排期
        ("每日 09:00 · 当日 10:00 → 当日 09:00", {"Hour": 9, "Minute": 0}, f"{D} 10:00", f"{D} 09:00"),
        ("每日 09:00 · 当日 08:00 → 前一日 09:00", {"Hour": 9, "Minute": 0}, f"{D} 08:00", "2026-09-21 09:00"),
    ]
    for desc, sched, now_s, want in cases:
        got = SS.expected_last_fire(sched, dt(now_s))
        check(desc, got == dt(want), f"got={got}")

    print("  边界（判不了就不判，方向应偏保守）")
    check("缺 Hour → None（不猜）", SS.expected_last_fire({"Minute": 30}, dt(f"{D} 10:00")) is None)
    check("空排期 → None", SS.expected_last_fire(None, dt(f"{D} 10:00")) is None)
    check("非 dict → None", SS.expected_last_fire("garbage", dt(f"{D} 10:00")) is None)
    # launchd 允许键写成数组（{"Weekday":[1,5]}）——必须返回 None 而非 int(list) 抛异常，
    # 否则 scan_launchd() 会把整个快照脚本打断（2026-09-22 复验逮到的潜伏崩溃面）
    arr_cases = [
        ("Weekday 为数组", {"Weekday": [1, 5], "Hour": 2, "Minute": 30}),
        ("Hour 为数组", {"Hour": [2, 14], "Minute": 30}),
        ("Minute 为数组", {"Hour": 2, "Minute": [0, 30]}),
        ("Day 为数组", {"Day": [1, 15], "Hour": 9, "Minute": 0}),
    ]
    for desc, sched in arr_cases:
        try:
            got = SS.expected_last_fire(sched, dt(f"{D} 10:00"))
            check(f"{desc} → None 且不抛异常", got is None, f"got={got}")
        except Exception as e:
            check(f"{desc} → None 且不抛异常", False, f"抛了 {type(e).__name__}: {e}")
    # 月级排期超出 70 天回溯窗 → None（保守：不判红，不会误报）
    far = SS.expected_last_fire({"Month": 10, "Day": 1, "Hour": 9, "Minute": 0}, dt(f"{D} 10:00"))
    check("70 天窗外的月级排期 → None（保守不误报）", far is None, f"got={far}")


# ───────────────── ③ classify_machine_state（纯函数）─────────────────
def test_classify_machine_state():
    print("\n③ classify_machine_state · 机器状态归因（含 kern.boottime 判别不了的那一例）")
    E = datetime(2026, 9, 21, 2, 30)            # 复现 09-21 02:30 那个落空的排期
    cases = [
        ("exp 前最后一次是 Start → on",
         [(datetime(2026, 9, 20, 22, 0), "Start")], "on"),
        ("exp 前最后一次是 Wake → on",
         [(datetime(2026, 9, 20, 22, 0), "Start"), (datetime(2026, 9, 21, 1, 0), "Wake")], "on"),
        ("exp 前最后一次是 Sleep → asleep",
         [(datetime(2026, 9, 20, 22, 0), "Start"), (datetime(2026, 9, 20, 23, 0), "Sleep")], "asleep"),
        ("exp 之前无事件、之后才 Start → off（＝09-21 真实形状：整夜关机）",
         [(datetime(2026, 9, 21, 6, 50), "Start")], "off"),
        # ★ 核心判别例：**exp 之后重启过**。
        #   kern.boottime 只会给出「最近一次开机 = 09-21 06:50 > exp」，据此降级就会**误判成
        #   「机器没开」并掩盖真漏跑**；按事件史判则是「exp 时机器在运行」⇒ 真漏跑 ⇒ 红。
        ("★ exp 后重启过，但 exp 时机器在运行 → on（不得被最近一次开机骗到）",
         [(datetime(2026, 9, 20, 22, 0), "Start"), (datetime(2026, 9, 21, 6, 50), "Start")], "on"),
        ("空事件 → unknown（不猜）", [], "unknown"),
    ]
    for desc, ev, want in cases:
        got, why = SS.classify_machine_state(E, ev)
        check(desc, got == want, f"got={got} · {why[:60]}")

    print("  残余盲区如实标注")
    got, why = SS.classify_machine_state(E, [(datetime(2026, 9, 20, 23, 0), "Sleep")])
    check("只有 Sleep 记录时如实说「在睡眠」", got == "asleep" and "睡眠" in why, why[:60])
def make_plist(d: Path, label, sched, stdout_path):
    body = {"Label": label, "StartCalendarInterval": sched,
            "ProgramArguments": ["/usr/bin/true"]}
    if stdout_path is not None:
        body["StandardOutPath"] = stdout_path
    p = d / f"{label}.plist"
    p.write_bytes(plistlib.dumps(body))
    return p


def test_scan_launchd(tmproot: Path):
    print("\n② scan_launchd · 防误报四道闸 + 正报")
    la = tmproot / "LaunchAgents"
    la.mkdir()
    ops = tmproot / "ops"
    ops.mkdir()
    now = datetime.now()
    recent = (now - timedelta(minutes=1)).timestamp()
    old = (now - timedelta(days=3)).timestamp()

    # 四个 job，各验一道闸
    make_plist(la, "com.zhuzhao.fresh", {"Hour": 0, "Minute": 1}, str(tmproot / "fresh.log"))
    (tmproot / "fresh.log").write_text("x")
    os.utime(tmproot / "fresh.log", (recent, recent))

    make_plist(la, "com.zhuzhao.missed", {"Hour": 10, "Minute": 1}, str(tmproot / "missed.log"))
    (tmproot / "missed.log").write_text("x")
    os.utime(tmproot / "missed.log", (old, old))

    make_plist(la, "com.zhuzhao.noout", {"Hour": 0, "Minute": 1}, None)

    make_plist(la, "com.zhuzhao.tmplog", {"Hour": 0, "Minute": 1}, "/tmp/some_job.log")

    SS.LAUNCH_AGENTS = la
    SS.OPS_DIRS = [ops]
    SS.launchctl_loaded = lambda label: {"loaded": True, "state": "not running", "last_exit_code": "0"}
    # 机器状态归因打桩为「在运行」——闸①-④ 的断言只反映「漏没漏跑」本身，
    # 不受跑本测试时的真实机器状态影响（真实查询走 pmset，另用专门段落验）。
    SS.machine_state_at = lambda exp: ("on", "测试桩：机器在运行")

    res = SS.scan_launchd()
    stal = {f["label"]: f for f in res["staleness"]}

    check("fresh（mtime 新）→ 不判", "com.zhuzhao.fresh" not in stal)
    check("missed（mtime 3 天前）→ 🔴 应跑未跑",
          stal.get("com.zhuzhao.missed", {}).get("level") == "red",
          f"{stal.get('com.zhuzhao.missed', {}).get('issue', '')[:60]}")
    check("noout（无 StandardOutPath）→ ⚠ 无法判定，不判红",
          stal.get("com.zhuzhao.noout", {}).get("level") == "yellow")
    check("tmplog（日志在 /tmp）→ ⚠ 无法判定，不判红",
          stal.get("com.zhuzhao.tmplog", {}).get("level") == "yellow")

    print("  闸② running 与闸① grace 窗")
    SS.launchctl_loaded = lambda label: {"loaded": True, "state": "running", "last_exit_code": "1"}
    res2 = SS.scan_launchd()
    check("state=running → 全部跳过", res2["staleness"] == [], f"n={len(res2['staleness'])}")

    SS.launchctl_loaded = lambda label: {"loaded": True, "state": "not running", "last_exit_code": "0"}
    # 刚过点火时刻 1 分钟（< grace 45 分）→ 不判
    just = (now - timedelta(minutes=1)).replace(second=0, microsecond=0)
    make_plist(la, "com.zhuzhao.grace", {"Hour": just.hour, "Minute": just.minute},
               str(tmproot / "grace.log"))
    (tmproot / "grace.log").write_text("x")
    os.utime(tmproot / "grace.log", (old, old))
    res3 = SS.scan_launchd()
    check("刚过点火 <45min → 不判（grace 窗）",
          "com.zhuzhao.grace" not in {f["label"] for f in res3["staleness"]})

    print("  非本项目 label 不纳入")
    make_plist(la, "com.google.something", {"Hour": 0, "Minute": 1}, str(tmproot / "g.log"))
    res4 = SS.scan_launchd()
    check("com.google.* 被排除", "com.google.something" not in {f["label"] for f in res4["staleness"]})

    print("  闸⑤ 机器状态归因：漏跑**要报**，由原因定级（2026-09-22 Doctor 裁定）")
    # 复现实撞形状：02:30 排期落空、真因是机器整夜关机。裁定＝仍要报出，只是原因先查。
    make_plist(la, "com.zhuzhao.night", {"Hour": 2, "Minute": 30}, str(tmproot / "night.log"))
    (tmproot / "night.log").write_text("x")
    os.utime(tmproot / "night.log", (old, old))     # mtime 明显落后；机器若在运行就该判红
    for st, want_lvl in [("on", "red"), ("unknown", "red"),
                         ("asleep", "yellow"), ("off", "yellow")]:
        SS.machine_state_at = lambda exp, s=st: (s, f"测试桩：{s}")
        r5 = SS.scan_launchd()
        chk = {f["label"]: f for f in r5["staleness"]}.get("com.zhuzhao.night", {})
        check(f"machine_state={st} → {want_lvl}", chk.get("level") == want_lvl,
              f"level={chk.get('level')}")
        check(f"  └ state={st} 仍**报出**（不得静默）", bool(chk))
        check(f"  └ state={st} 判词带机器状态归因", "机器状态：" in chk.get("issue", ""))
    # ★ 关键反向断言：睡眠/未开机只是不判红，**不得连带把别的 job 也放过**
    SS.machine_state_at = lambda exp: ("off", "测试桩：off")
    r6 = SS.scan_launchd()
    check("off 状态下，另一个 job 的判定不受影响（闸不过宽）",
          "com.zhuzhao.night" in {f["label"] for f in r6["staleness"]},
          f"labels={sorted({f['label'] for f in r6['staleness']})}")
    SS.machine_state_at = lambda exp: ("on", "测试桩：机器在运行")

    print("  兼容性：结构键齐备（真断言：四个键一个都不能少）")
    check("返回 {sources, installed, consistency, staleness} 四键齐全",
          set(res) == {"sources", "installed", "consistency", "staleness"}, f"keys={sorted(res)}")


def main():
    global OK
    tmproot = Path(tempfile.mkdtemp(prefix="ss_stale_test_"))
    print("持久化负向测试 · 快照面③「应跑未跑」")
    try:
        test_expected_last_fire()
        test_classify_machine_state()
        test_scan_launchd(tmproot)
    finally:
        shutil.rmtree(tmproot, ignore_errors=True)
    print(f"\n{'✅ 全过' if OK else '❌ 有失败项'}")
    return 0 if OK else 1


if __name__ == "__main__":
    sys.exit(main())
