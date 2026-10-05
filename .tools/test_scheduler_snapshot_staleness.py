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
from unittest.mock import patch

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


# ───────────────── 固定注入时钟（2026-10-05 Doctor 批「只修测试·固定注入时钟，让结果可重复」）──
# 原 `test_scan_launchd` 用 `datetime.now()` 与固定排期 fixture（00:01 / 10:01 / 02:30）时间耦合：
# 在各自点火后 45 分钟 grace 窗内跑，闸①会把 fixture 整体跳过 ⇒ noout/tmplog（乃至 missed/night）
# 拿不到判定，出现 59/61 假红（2026-10-05 00:07 实撞，每日 00:01–00:46 等三个死窗）。
# 修法＝把被测模块的 `datetime` 钉在正午 12:00（远离全部 fixture 排期的 grace 窗），任意时刻跑结果相同。
FIXED_NOW = datetime(2026, 9, 22, 12, 0)


class _FixedClock:
    NOW = FIXED_NOW

    @classmethod
    def now(cls, tz=None):
        return cls.NOW if tz is None else cls.NOW.replace(tzinfo=tz)

    fromtimestamp = staticmethod(datetime.fromtimestamp)
    fromisoformat = staticmethod(datetime.fromisoformat)
    strptime = staticmethod(datetime.strptime)


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
def make_plist(d: Path, label, sched, stdout_path, stderr_path=None):
    body = {"Label": label, "StartCalendarInterval": sched,
            "ProgramArguments": ["/usr/bin/true"]}
    if stdout_path is not None:
        body["StandardOutPath"] = stdout_path
    if stderr_path is not None:
        body["StandardErrorPath"] = stderr_path
    p = d / f"{label}.plist"
    p.write_bytes(plistlib.dumps(body))
    return p


@patch.object(SS, "datetime", _FixedClock)   # 固定注入时钟：scan_launchd 内部的 datetime.now() 同被钉住
def test_scan_launchd(tmproot: Path):
    print("\n② scan_launchd · 防误报四道闸 + 正报")
    la = tmproot / "LaunchAgents"
    la.mkdir()
    ops = tmproot / "ops"
    ops.mkdir()
    now = FIXED_NOW
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

    print("  兼容性：结构键齐备（真断言：五个键一个都不能少）")
    check("返回 {sources, installed, consistency, staleness, tcc_suspect} 五键齐全",
          set(res) == {"sources", "installed", "consistency", "staleness", "tcc_suspect"},
          f"keys={sorted(res)}")


# ───────────────── ④ TCC 静默停摆指纹（前缀无关 · 2026-09-27 加）─────────────────
def test_tcc_fingerprint(tmproot: Path):
    """守卫须成对：N（该报）＋ P（不该报）。

    判据＝`loaded ∧ 退出码==78 ∧ stdout 或 stderr 落 TCC 保护区`。
    实撞原型：`com.fuxi4ai.audit-harness.dispatch`（`last exit code = "78:"` · stdout 落
    `~/Documents/Codex/...`）——与 〖剑酒青丘/GOTCHAS.md〗NOTE-20260918-001 的
    TCC 静默停摆签名吻合，却因**不在 OURS 前缀内**而从未被任何一面报出。
    故本段首要主张是**前缀无关**：正报例刻意用非项目前缀的 label。
    """
    print("\n④ TCC 静默停摆指纹（前缀无关）")
    la = tmproot / "tcc_agents"
    ops = tmproot / "tcc_ops"
    prot = tmproot / "protected"
    prot2 = tmproot / "protected2"
    outside = tmproot / "outside"
    for d in (la, ops, prot, prot2, outside):
        d.mkdir(exist_ok=True)
    SS.LAUNCH_AGENTS = la
    SS.OPS_DIRS = [ops]
    # 不依赖真实 HOME：把「保护区」钉到临时目录，正例写其内、反例写其外
    _saved_tcc = SS.TCC_PROTECTED
    SS.TCC_PROTECTED = (prot, prot2)
    SS.machine_state_at = lambda exp: ("on", "测试桩：机器在运行")
    SCHED = {"Hour": 0, "Minute": 1}          # 恒过 grace 窗，逼 面③ 与指纹两条路径都走到

    # ── 纯函数直测：钉契约本身 ──
    # 作业级用例在两点上覆盖不到：「不可判」（0 与 None 在调用点行为不可分）与「路径归一」
    # （`..` 形式不会自然出现在 plist 里）。故在此直接钉纯函数。2026-09-27 第四轮独立复验提示补。
    check("纯函数 _exit_code：`78:` 尾随冒号须剥成 78", SS._exit_code("78:") == 78)
    check("纯函数 _exit_code：`0` → 0（不得与 None 混）", SS._exit_code("0") == 0)
    check("纯函数 _exit_code：不可判一律 None（**不得**当 0、也不得当 78）",
          SS._exit_code(None) is None and SS._exit_code("") is None
          and SS._exit_code("EX_CONFIG") is None, f"{SS._exit_code(None)!r}")
    check("纯函数 _in_tcc：`..` 按**词法**归一 —— `<保护区>/../Codex/x.log` 判**区外**",
          SS._in_tcc(str(prot / ".." / "Codex" / "x.log")) is False)
    check("  └ 正对照：`<保护区>/../<保护区名>/o.log` 归一后回到区内 → True",
          SS._in_tcc(str(prot / ".." / prot.name / "o.log")) is True)

    def rt(loaded=True, code="0"):
        return lambda label: {"loaded": loaded, "state": "not running", "last_exit_code": code}

    # ── N 组：该报 ──
    SS.launchctl_loaded = rt(True, "78:")
    make_plist(la, "com.fuxi4ai.dispatch", SCHED, str(prot / "o.log"))          # 原型形状
    make_plist(la, "com.fuxi4ai.stderronly", SCHED, str(outside / "o.log"),     # 仅 stderr 在内
               stderr_path=str(prot / "e.log"))
    got = {f["label"]: f for f in SS.scan_launchd()["tcc_suspect"]}
    check("N：退出码 78: + stdout 落保护区 → 报（★ 且 label 非项目前缀）",
          "com.fuxi4ai.dispatch" in got, f"got={sorted(got)}")
    check("N：只有 stderr 落保护区 → 也报（stdio 成对，不只认 stdout）",
          "com.fuxi4ai.stderronly" in got, f"got={sorted(got)}")
    check("  └ stdio 清单只指保护区内的那一个",
          got.get("com.fuxi4ai.stderronly", {}).get("stdio_in_tcc") == [str(prot / "e.log")],
          f"{got.get('com.fuxi4ai.stderronly', {}).get('stdio_in_tcc')}")

    # ── P 组：四道反例（假阳性闸）──
    make_plist(la, "com.fuxi4ai.exit0", SCHED, str(prot / "o.log"))
    make_plist(la, "com.fuxi4ai.outside", SCHED, str(outside / "o.log"))
    make_plist(la, "com.fuxi4ai.exit1", SCHED, str(prot / "o.log"))
    SS.launchctl_loaded = rt(True, "0")
    g0 = {f["label"] for f in SS.scan_launchd()["tcc_suspect"]}
    check("P：退出码 0 + stdout 落保护区 → 不报", "com.fuxi4ai.exit0" not in g0, f"got={sorted(g0)}")
    # ★ 保护区闸必须在**码 78 之下**单独考。原版把这条与上一条挤在同一批 `rt(True,"0")` 里，
    #   于是它只把「退出码闸」又测了一遍、**从未考过保护区闸**——2026-09-27 第四轮独立复验
    #   逐条变异检验（把 `_in_tcc` 改恒真而用例不转红）逮出本用例为空转。已拆开并配同批正对照。
    SS.launchctl_loaded = rt(True, "78:")
    g78 = {f["label"] for f in SS.scan_launchd()["tcc_suspect"]}
    check("P：码 78: 但 stdio **全在保护区外** → 不报（★ 关键假阳性闸 · 78 下单独考）",
          "com.fuxi4ai.outside" not in g78, f"got={sorted(g78)}")
    check("  └ 同批正对照：码 78: 且 stdout 在保护区内 → 仍要报（防整批恒空＝假绿）",
          "com.fuxi4ai.dispatch" in g78, f"got={sorted(g78)}")
    SS.launchctl_loaded = rt(True, "1")
    check("P：退出码 1（非 78）+ stdout 落保护区 → 不报（本探针刻意只认 EX_CONFIG）",
          "com.fuxi4ai.exit1" not in {f["label"] for f in SS.scan_launchd()["tcc_suspect"]})
    SS.launchctl_loaded = rt(False, "78:")
    check("P：loaded=False → 不报（没加载的不算这条病）",
          not {f["label"] for f in SS.scan_launchd()["tcc_suspect"]}
          & {"com.fuxi4ai.dispatch", "com.fuxi4ai.stderronly"})
    SS.launchctl_loaded = rt(True, None)
    check("P：退出码 None（不可判）→ 不报 —— 既不得当 0、也不得当 78",
          "com.fuxi4ai.dispatch" not in {f["label"] for f in SS.scan_launchd()["tcc_suspect"]})

    # ── 异常检测层：必须是 RED（装了、加载了，却零输出地死着 —— 须出声）──
    SS.launchctl_loaded = rt(True, "78:")
    snap = {"_meta": {}, "cowork_live": {"tasks": []},
            "documents_dead_tree": {"exists": False, "content_diverged": [], "only_in_dead": []},
            "launchd": SS.scan_launchd(), "crontab": {"entries": []}, "mounts": {}}
    red, yellow = SS.detect_anomalies(snap, None)
    check("升级层：detect_anomalies 把它判 RED",
          any("疑似 TCC 静默停摆" in x for x in red), f"n_red={len(red)}")
    check("  └ 且不得只落在 yellow（只作提示＝仍会被忽略）",
          not any("疑似 TCC 静默停摆" in x for x in yellow))

    # ── 还原全局，免污染后续 ──
    SS.TCC_PROTECTED = _saved_tcc


def main():
    global OK
    tmproot = Path(tempfile.mkdtemp(prefix="ss_stale_test_"))
    print("持久化负向测试 · 快照面③「应跑未跑」+ TCC 停摆指纹")
    try:
        test_expected_last_fire()
        test_classify_machine_state()
        test_scan_launchd(tmproot)
        test_tcc_fingerprint(tmproot)
    finally:
        shutil.rmtree(tmproot, ignore_errors=True)
    print(f"\n{'✅ 全过' if OK else '❌ 有失败项'}")
    return 0 if OK else 1


if __name__ == "__main__":
    sys.exit(main())
