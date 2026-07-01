#!/usr/bin/env python3
"""Shake Hands 机器握手通道 · consumer 辅助脚本（纯 stdlib）

职责：只做通用信封的**机械活**——扫描 / 校验 / checksum 重算 / run_id 幂等 / ack 滚动写入。
task 专属的落盘判断（追加哪个 wiki、是否 promote、git 命令）由 handshake-consumer skill
的指令让 agent 按 brain 铁律执行，不塞进本脚本。

路径 env 覆盖（G-X45 教训·兜 gateway 平铺挂载）：
  SHAKE_HANDS_ROOT   握手层根，默认 ~/Documents/4AI/Shake hands
                     gateway 平铺挂载下应设为挂载点（如 .../mnt/4AI/Shake hands）

用法：
  consume.py scan                      扫 inbound，输出 ready/skipped/rejected 分类清单
  consume.py verify <file>             单文件详细校验
  consume.py checksum <payload.json>   给 payload 算 canonical checksum（对拍/测试用）
  consume.py write-ack --task-id X --status ok --run-id R [--outputs '[..]'] [--dry-run]
"""
import argparse
import glob
import hashlib
import json
import os
import re
import sys
from datetime import datetime, timezone

SCHEMA_VERSION = "1.0"


def root():
    env = os.environ.get("SHAKE_HANDS_ROOT")
    if env:
        return env
    return os.path.expanduser("~/Documents/4AI/Shake hands")


def inbound_dir():
    return os.path.join(root(), "to CC", "scheduled")


def outbound_dir():
    return os.path.join(root(), "to VV", "scheduled")


def canonical_checksum(payload):
    """对 payload 用 sort_keys + 紧凑分隔符 + UTF-8 序列化后算 sha256（与 schema 声明一致）。"""
    canonical = json.dumps(
        payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest()


def validate_envelope(env):
    """手写轻量校验（不依赖 jsonschema）。返回 errors 列表，空=通过。"""
    errors = []
    required = ["schema_version", "task_id", "produced_by", "produced_at", "run_id", "payload", "checksum"]
    for k in required:
        if k not in env:
            errors.append(f"缺必填字段: {k}")
    if errors:
        return errors
    sv = str(env["schema_version"])
    if sv.split(".")[0] != SCHEMA_VERSION.split(".")[0]:
        errors.append(f"schema_version 主版本不兼容: 期望 {SCHEMA_VERSION.split('.')[0]}.x 得到 {sv}")
    tid = env["task_id"]
    if not isinstance(tid, str) or not re.match(r"^[a-z0-9][a-z0-9-]*$", tid):
        errors.append(f"task_id 非法: {tid!r}")
    if not isinstance(env["payload"], dict):
        errors.append("payload 必须是对象")
    cs = env["checksum"]
    if not isinstance(cs, dict) or "algo" not in cs or "value" not in cs:
        errors.append("checksum 结构不完整（需 algo + value）")
    elif cs["algo"] != "sha256":
        errors.append(f"checksum.algo 不支持: {cs['algo']}")
    elif isinstance(env["payload"], dict):
        actual = canonical_checksum(env["payload"])
        if actual != cs["value"]:
            errors.append(f"checksum 不符: 声明 {cs['value'][:12]}… 重算 {actual[:12]}…")
    return errors


def ack_latest_path(task_id):
    return os.path.join(outbound_dir(), f"{task_id}.ack.latest.json")


def ack_prev_path(task_id):
    return os.path.join(outbound_dir(), f"{task_id}.ack.prev.json")


def last_consumed_run_id(task_id):
    p = ack_latest_path(task_id)
    if not os.path.exists(p):
        return None
    try:
        with open(p, encoding="utf-8") as fh:
            return json.load(fh).get("last_consumed_run_id")
    except Exception:
        return None


def cmd_scan(args):
    result = {"ready": [], "skipped_idempotent": [], "rejected": []}
    files = sorted(glob.glob(os.path.join(inbound_dir(), "*.latest.json")))
    for f in files:
        base = os.path.basename(f)
        try:
            with open(f, encoding="utf-8") as fh:
                env = json.load(fh)
        except Exception as e:
            result["rejected"].append({"file": base, "reason": f"JSON 解析失败: {e}"})
            continue
        errs = validate_envelope(env)
        if errs:
            result["rejected"].append({"file": base, "task_id": env.get("task_id"), "reason": "; ".join(errs)})
            continue
        tid, rid = env["task_id"], env["run_id"]
        last = last_consumed_run_id(tid)
        entry = {
            "file": base, "task_id": tid, "run_id": rid,
            "produced_at": env.get("produced_at"),
            "sample": bool(env.get("sample", False)),
            "n_actions": len(env.get("suggested_actions", [])),
        }
        if last is not None and rid == last:
            result["skipped_idempotent"].append({**entry, "reason": f"run_id 已消费({rid})"})
        else:
            result["ready"].append(entry)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return result


def cmd_verify(args):
    with open(args.file, encoding="utf-8") as fh:
        env = json.load(fh)
    errs = validate_envelope(env)
    out = {
        "file": args.file, "task_id": env.get("task_id"), "run_id": env.get("run_id"),
        "sample": bool(env.get("sample", False)), "valid": not errs, "errors": errs,
        "payload_keys": list(env.get("payload", {}).keys()) if isinstance(env.get("payload"), dict) else None,
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return out


def cmd_checksum(args):
    with open(args.file, encoding="utf-8") as fh:
        payload = json.load(fh)
    print(canonical_checksum(payload))


def cmd_write_ack(args):
    """滚动 ack.latest→ack.prev（copy-then-overwrite，只写不删），写新 ack.latest。"""
    tid = args.task_id
    os.makedirs(outbound_dir(), exist_ok=True)
    latest, prev = ack_latest_path(tid), ack_prev_path(tid)
    ack = {
        "schema_version": SCHEMA_VERSION,
        "task_id": tid,
        "acked_by": "C.C./Claude",
        "acked_at": datetime.now(timezone.utc).astimezone().isoformat(),
        "status": args.status,                                   # ok | failed | skipped
        "last_consumed_run_id": args.run_id or None,             # 幂等锚：消费成功的 run_id
        "consumed_outputs": json.loads(args.outputs) if args.outputs else [],
        "leftovers": json.loads(args.leftovers) if args.leftovers else [],
        "dry_run": bool(args.dry_run),
        "notes": args.notes or "",
    }
    rolled = False
    if os.path.exists(latest):                                   # 滚动：只写不删
        with open(latest, encoding="utf-8") as fh:
            old = fh.read()
        with open(prev, "w", encoding="utf-8") as fh:
            fh.write(old)
        rolled = True
    with open(latest, "w", encoding="utf-8") as fh:
        fh.write(json.dumps(ack, ensure_ascii=False, indent=2))
    print(json.dumps({"wrote": latest, "rolled_prev": rolled, "status": args.status,
                      "dry_run": ack["dry_run"]}, ensure_ascii=False, indent=2))


def main():
    ap = argparse.ArgumentParser(description="Shake Hands 机器握手 consumer 辅助脚本")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("scan")
    v = sub.add_parser("verify"); v.add_argument("file")
    c = sub.add_parser("checksum"); c.add_argument("file")
    w = sub.add_parser("write-ack")
    w.add_argument("--task-id", required=True)
    w.add_argument("--status", required=True, choices=["ok", "failed", "skipped"])
    w.add_argument("--run-id", default="")
    w.add_argument("--outputs", default="", help="JSON array 字符串：落盘产物路径清单")
    w.add_argument("--leftovers", default="", help="JSON array 字符串：遗留/待人工项")
    w.add_argument("--notes", default="")
    w.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    {"scan": cmd_scan, "verify": cmd_verify, "checksum": cmd_checksum, "write-ack": cmd_write_ack}[args.cmd](args)


if __name__ == "__main__":
    main()
