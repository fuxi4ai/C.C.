#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""面⑤ 挂载检查：不是会话环境（没有 mnt 目录）时报「不适用」，不得报「缺」；
会话环境里目录缺、乃至 Documents 整个没挂上，仍须报缺（通用教训 G-X190 追记 2026-11-10）。
只用临时目录（把模块 HOME 指过去），不碰真实文件。
  PYTHONDONTWRITEBYTECODE=1 python3 -B test_scheduler_snapshot_mounts.py
  GEN=<旧版路径> python3 -B test_scheduler_snapshot_mounts.py   # 负向验证：旧版应在「非会话环境」各条失败
"""
import glob, importlib.util, os, sys, tempfile
from pathlib import Path

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
GEN = os.environ.get("GEN") or os.path.join(HERE, "scheduler_snapshot.py")


def load():
    spec = importlib.util.spec_from_file_location("scheduler_snapshot_under_test", GEN)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    fails = []

    def check(name, ok):
        print(("PASS " if ok else "FAIL ") + name)
        if not ok:
            fails.append(name)

    SS = load()
    names = [n for n, _ in SS.MOUNT_MARKERS]
    verdict = getattr(SS, "mounts_verdict", None)
    check("存在单一判词函数 mounts_verdict", callable(verdict))
    if not callable(verdict):          # 旧版：按旧渲染逻辑折算，让后面的断言测到旧行为本身
        def verdict(mt):
            missing = [k for k, ok in mt.items() if not ok]
            return ("missing" if missing else "ok"), missing

    def scan(home):                    # 走默认路径（不传 roots），HOME 指向临时目录
        SS.HOME = Path(home)
        return SS.scan_mounts()

    in_session = bool(glob.glob("/sessions/*/mnt"))   # 本测试若在沙箱里跑，/sessions 根是真实存在的
    with tempfile.TemporaryDirectory() as home:
        # ① 非会话环境（没有 mnt 目录，Mac 原生终端）→ 不适用，不报缺
        if in_session:
            print("SKIP 非会话环境三条（当前在 /sessions 沙箱内，无法构造）")
        else:
            mt = scan(home)
            check("非会话环境：五项全为 None", list(mt) == names and all(v is None for v in mt.values()))
            check("非会话环境：判词＝na 且缺项为空", verdict(mt) == ("na", []))
            # 真实目录都在 ~/Documents 也不该影响：它不是挂载根
            (Path(home) / "Documents/Claude/brain").mkdir(parents=True)
            (Path(home) / "Documents/Claude/brain/TODO.md").write_text("x", encoding="utf-8")
            check("非会话环境：~/Documents 下有文件仍是 na", verdict(scan(home))[0] == "na")

        # ② 会话环境但 Documents 整个没挂上（只有 mnt）→ 最严重的缺挂，必须报缺五项
        (Path(home) / "mnt").mkdir()
        mt = scan(home)
        check("有 mnt 无 Documents：五项全为 False", all(v is False for v in mt.values()))
        check("有 mnt 无 Documents：判词＝missing 且列全五项", verdict(mt) == ("missing", names))

        # ③ Documents 挂了但是空的 → 仍报缺五项
        root = Path(home) / "mnt" / "Documents"
        root.mkdir()
        check("有根但空：判词＝missing 且列全五项", verdict(scan(home)) == ("missing", names))

        # ④ 只补一个标记 → 该项 True，其余仍缺
        (root / "Claude/brain").mkdir(parents=True)
        (root / "Claude/brain/TODO.md").write_text("x", encoding="utf-8")
        mt = scan(home)
        check("补 brain 标记：brain=True", mt["brain"] is True)
        check("补 brain 标记：其余四项仍缺", verdict(mt) == ("missing", [n for n in names if n != "brain"]))

        # ⑤ 每项各补第一个标记 → 全挂载
        for _, markers in SS.MOUNT_MARKERS:
            p = root / markers[0]
            p.parent.mkdir(parents=True, exist_ok=True)
            if not p.exists():
                p.write_text("x", encoding="utf-8")
        check("全部补齐：判词＝ok", verdict(scan(home)) == ("ok", []))

    # ⑥ 旧调用形态兼容：空 dict 沿旧行为算 ok（staleness 测试夹具用 {}）
    check("空 dict 沿旧行为＝ok", verdict({}) == ("ok", []))
    # ⑦ 混合（部分 None 不应出现，但出现时不得被当成不适用）
    check("混合 None/False：仍报缺", verdict({"a": None, "b": False}) == ("missing", ["b"]))

    print(f"\n{'全部通过' if not fails else f'{len(fails)} 项失败'}")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
