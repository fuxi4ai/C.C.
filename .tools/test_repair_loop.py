#!/usr/bin/env python3
"""
test_repair_loop.py — 巡检自愈循环 fail-fast 负向测试（2026-08-29 · 设计 §5）
测四件事：F1 分臂判定 / triggered_by 验收判据（假绿灯回归）/ audit 行 schema / F3 授权调用形态。
无 assert（python -O 会删守卫）——用失败计数器，非零失败即 exit 1（G-X150）。
正常路径 exit 0 不证明 fail-fast：负向用例全在下面，每次跑都要过。
用法：python3 test_repair_loop.py   # exit 0=全过，1=有失败
"""
import datetime
import sys

FAIL = []


def check(name, cond, detail=""):
    if not cond:
        FAIL.append(f"{name} — {detail}")
    print(("PASS  " if cond else "FAIL  ") + name + (f"  [{detail}]" if detail else ""))


# ── F1 分臂（设计 §2 L2 表）────────────────────────────────────
THRESHOLD_DAYS = 8


def classify_f1(snapshot_age_days, last_run_age_days):
    """'F1a'（周班停摆）/ 'F1b'（班内落盘失效）/ 'F1-快照缺失' / 'ok'。阈值 8 天。"""
    if snapshot_age_days is None:
        return "F1-快照缺失"
    if snapshot_age_days <= THRESHOLD_DAYS:
        return "ok"
    if last_run_age_days is None or last_run_age_days > THRESHOLD_DAYS:
        return "F1a"
    return "F1b"


check("F1·双超期→F1a", classify_f1(11, 12) == "F1a")
check("F1·快照超期+lastRunAt新鲜→F1b（今日 live 病例同构）", classify_f1(11, 5) == "F1b")
check("F1·快照新鲜→ok", classify_f1(3, 12) == "ok")
check("F1·边界 8 天整→ok", classify_f1(8, 8) == "ok")
check("F1·边界 9 天快照+8 天班→F1b", classify_f1(9, 8) == "F1b")
check("F1·快照缺失（None）不得误报 F2 也不得崩溃", classify_f1(None, 12) == "F1-快照缺失",
      "快照不存在≠班消失，走「快照不存在」路径")
check("F1·快照超期+lastRunAt 缺失→按 F1a 保守处理", classify_f1(11, None) == "F1a")


# ── F1 验收判据：必须 triggered_by=scheduled（设计 §2 L3 · 假绿灯回归）──
def accept_f1(triggered_by, last_run_advanced, snapshot_advanced):
    """下次周窗内 lastRunAt 前进 + 快照前进，且 triggered_by=scheduled。"""
    return (triggered_by == "scheduled" and last_run_advanced and snapshot_advanced)


check("验收·scheduled+双前进→通过", accept_f1("scheduled", True, True))
check("验收·manual 快照不得被读成周班在跑（08-02 假绿灯回归）", not accept_f1("manual", True, True))
check("验收·scheduled 但 lastRunAt 未前进→不通过（G-X51 静默成功挡）", not accept_f1("scheduled", False, True))
check("验收·scheduled 但快照未前进→不通过", not accept_f1("scheduled", True, False))
check("验收·旧快照无 triggered_by 字段→不通过", not accept_f1(None, True, True))


# ── audit 行 schema（设计 §2 审计层六元组）──────────────────────
REQUIRED = ["ts", "trigger", "action", "rollback", "acceptance", "actor", "status"]
VALID_STATUS = {"🔄", "⚠️", "✅"}


def validate_audit_line(line):
    errs = []
    for k in REQUIRED:
        if k not in line or line[k] is None or str(line[k]).strip() == "":
            errs.append(f"缺/空字段 {k}")
    if line.get("status") not in VALID_STATUS:
        errs.append(f"非法状态词 {line.get('status')!r}")
    try:
        datetime.datetime.fromisoformat(line.get("ts", ""))
    except Exception:
        errs.append(f"ts 非法 {line.get('ts')!r}")
    return errs


_good = {"ts": "2026-08-29T10:00:00-07:00", "trigger": "快照超期11天", "action": "S1 贴命令",
         "rollback": "无写动作", "acceptance": "下次周班 lastRunAt 前进", "actor": "CC", "status": "🔄"}
check("audit·合法行 0 错误", validate_audit_line(_good) == [])
check("audit·缺 acceptance 报错", any("acceptance" in e for e in validate_audit_line({**_good, "acceptance": ""})))
check("audit·非法状态词报错", any("非法状态" in e for e in validate_audit_line({**_good, "status": "done"})))
check("audit·ts 非法报错", any("ts 非法" in e for e in validate_audit_line({**_good, "ts": "昨天"})))


# ── F3 授权调用形态（设计 §2 L2 · 白名单唯一形态）────────────────
WHITELIST_TASK = "scheduler-weekly-audit"
FORBIDDEN_PARAMS = {"prompt", "cronExpression", "fireAt", "enabled", "notifyOnCompletion"}


def allowed_update(task_id, params):
    """白名单唯一形态：仅 scheduler-weekly-audit + 仅 description 参数（且非空）。"""
    if task_id != WHITELIST_TASK:
        return False, "非白名单 taskId"
    if not params:
        return False, "空参数（空写无效动作）"
    bad = sorted(set(params) & FORBIDDEN_PARAMS)
    if bad:
        return False, f"禁传参数 {bad}"
    if not set(params).issubset({"description"}):
        return False, f"未知参数 {sorted(set(params) - {'description'})}"
    return True, ""


ok_, _ = allowed_update("scheduler-weekly-audit", {"description": "x"})
check("F3·白名单 taskId + 仅 description→放行", ok_)
r, why = allowed_update("market-data-daily-update", {"description": "x"})
check("F3·错靶 taskId→拒绝（负向）", not r, why)
r, why = allowed_update("scheduler-weekly-audit", {"description": "x", "prompt": "y"})
check("F3·携带 prompt 参数→拒绝（负向·盲写禁手）", not r, why)
r, why = allowed_update("scheduler-weekly-audit", {"cronExpression": "0 9 * * *"})
check("F3·改 cron→拒绝（排期变更=禁手）", not r, why)
r, why = allowed_update("scheduler-weekly-audit", {"enabled": False})
check("F3·改 enabled→拒绝（启停=禁手）", not r, why)
r, why = allowed_update("scheduler-weekly-audit", {})
check("F3·空参数→拒绝（空写无效动作）", not r, why)

# ── 收口 ──────────────────────────────────────────────────────
print("\n" + "=" * 44)
print(f"共 {len(FAIL)} 项失败")
if FAIL:
    for f in FAIL:
        print("  ✗ " + f)
sys.exit(1 if FAIL else 0)
