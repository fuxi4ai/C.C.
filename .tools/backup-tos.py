#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""backup-tos.py — 数据层核心档 → 火山引擎 TOS（对象存储）
（CC 2026-07-18；Doctor 裁定：整条 crontab 停、数据层走 TOS、工具由 CC 定 → 选 Python SDK）

为什么是 Python SDK 而非 tosutil/rclone：
  ① tosutil 不在 homebrew、需手动下二进制，且其文档页客户端渲染、CC 无法验准语法；
  ② 本脚本用 Python 的 sqlite3.backup() 出一致性快照，连 sqlite3 CLI 都不依赖；
  ③ 与 fetch_*.py 同源，将来挂 launchd 或并进日更链都顺手。整条链只需 `pip3 install tos`。

备份范围（~118MB，只收「不可再生」的）：
  1. recap.db                 ~4.5MB  几个月课件沉淀（industry_signals/dim1-4/emotion_cycle），API 拉不回
  2. Raw-Recap/              ~112MB  235 份原始课件 = recap.db 的上游来源，比 recap.db 更根本
  3. business_breakdown.db   ~0.6MB
不收：Douyin(66G)/YouTube（可重下）｜Market-Data(2.4G)（tushare 可重拉）｜*.bak(2.0G)（本地回滚锚）
      ｜龙鱼-标的分析库/（自身是 git 仓且有远端 fuxi4ai/longyu-analysis-lib）

凭证：~/Documents/Database/.env（该目录非 git 仓，天然不会被提交）
  必需 TOS_ACCESS_KEY / TOS_SECRET_KEY / TOS_ENDPOINT / TOS_BUCKET
  可选 TOS_REGION（缺省从 endpoint 推导）/ TOS_PREFIX（默认 zzjy-data）

用法：
  pip3 install tos                      # 一次性
  python3 backup-tos.py --dry-run       # 快照+比对，不联网上传
  python3 backup-tos.py                 # 真传（增量：size 相同即跳过）
  python3 backup-tos.py --full          # 强制全量重传
"""
import os, sys, re, json, sqlite3, shutil, argparse, datetime, traceback

HOME = os.path.expanduser("~")
ENV_FILE = os.path.join(HOME, "Documents/Database/.env")
DB_SRC = os.path.join(HOME, "Documents/Database")
SNAP = "/tmp/zzjy-dbsnap"
LOG = os.path.join(HOME, "Documents/Claude/brain/.tools/backup-tos.log")

DBS = [
    (os.path.join(DB_SRC, "烛照九阴/recap.db"), "recap.db"),
    (os.path.join(DB_SRC, "宏观-大宗商品/business_breakdown.db"), "business_breakdown.db"),
]
RAW_RECAP = os.path.join(DB_SRC, "烛照九阴/Raw-Recap")
SKIP_NAMES = {".DS_Store"}
SKIP_PAT = re.compile(r"\.bak|~\$|\.swp$|-wal$|-shm$|-journal$")

_lines = []


def log(msg):
    print(msg)
    _lines.append(msg)


def flush_log():
    try:
        with open(LOG, "a", encoding="utf-8") as f:
            f.write("\n".join(_lines) + "\n")
    except Exception:
        pass


def load_env():
    if not os.path.exists(ENV_FILE):
        log(f"✗ 缺 {ENV_FILE}")
        sys.exit(1)
    env = {}
    with open(ENV_FILE, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip().strip('"').strip("'")
    return env


def snapshot_dbs():
    """用 sqlite3.backup() 出一致性快照——并发写下也能得到完整副本，胜过直接拷活库。
    quick_check 不过就丢弃该快照、保留云端上一版，绝不用坏副本覆盖好副本。"""
    if os.path.isdir(SNAP):
        shutil.rmtree(SNAP)
    os.makedirs(SNAP, exist_ok=True)
    ok, failed = [], []
    for src, name in DBS:
        if not os.path.exists(src):
            log(f"  ⏭ 跳过（不存在）：{name}")
            continue
        dst = os.path.join(SNAP, name)
        try:
            s = sqlite3.connect(f"file:{src}?mode=ro", uri=True)
            d = sqlite3.connect(dst)
            s.backup(d)
            d.close()
            s.close()
            chk = sqlite3.connect(dst).execute("PRAGMA quick_check").fetchone()[0]
            if chk != "ok":
                log(f"  ✗ {name} quick_check={chk} → 丢弃快照，保留云端上一版")
                os.remove(dst)
                failed.append(name)
                continue
            mb = os.path.getsize(dst) / 1048576
            log(f"  ✓ {name} 快照 OK（{mb:.1f} MB）")
            ok.append((dst, f"db/{name}"))
        except Exception as e:
            log(f"  ✗ {name} 快照失败：{e} → 保留云端上一版")
            failed.append(name)
    return ok, failed


def collect_raw_recap():
    items = []
    if not os.path.isdir(RAW_RECAP):
        log(f"  ⏭ Raw-Recap 不存在，跳过")
        return items
    for root, dirs, files in os.walk(RAW_RECAP):
        dirs[:] = [d for d in dirs if not d.startswith(".")]
        for fn in files:
            if fn in SKIP_NAMES or SKIP_PAT.search(fn) or fn.startswith("."):
                continue
            p = os.path.join(root, fn)
            rel = os.path.relpath(p, RAW_RECAP)
            items.append((p, "Raw-Recap/" + rel.replace(os.sep, "/")))
    return items


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="快照+比对，不联网")
    ap.add_argument("--full", action="store_true", help="强制全量重传（不做 size 比对）")
    args = ap.parse_args()

    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    env = load_env()
    bucket = env.get("TOS_BUCKET")
    if not bucket:
        log(f"✗ .env 缺 TOS_BUCKET"); flush_log(); sys.exit(1)
    prefix = env.get("TOS_PREFIX", "zzjy-data").strip("/")

    log("━" * 42)
    log(f"[{ts}] backup-tos.py 开始  tos://{bucket}/{prefix}"
        + ("  (DRY-RUN)" if args.dry_run else "") + ("  (FULL)" if args.full else ""))

    endpoint = env.get("TOS_ENDPOINT", "")
    # ⚠️ 护栏（2026-07-18 实际踩到）：控制台「访问域名」给的是**桶域名**
    #    <bucket>.tos-<region>.volces.com，而 SDK 要的是**地域域名** tos-<region>.volces.com。
    #    填成前者 → SDK 再拼一次桶名 → <bucket>.<bucket>.tos-... 域名不存在，
    #    报成一堆 SSL EOF / http request timeout，从报错表面完全看不出是配置错。
    if bucket and endpoint.startswith(bucket + "."):
        _fixed = endpoint[len(bucket) + 1:]
        log(f"  ⚠ TOS_ENDPOINT 含桶名前缀，已自动剥离：{endpoint} → {_fixed}")
        log(f"    建议把 .env 的 TOS_ENDPOINT 直接改成 {_fixed}")
        endpoint = _fixed
    # region 缺省从 endpoint 推导：tos-cn-shanghai.volces.com → cn-shanghai
    region = env.get("TOS_REGION") or (re.sub(r"^tos-", "", endpoint.split(".")[0]) if endpoint else "")

    log("── SQLite 一致性快照 ──")
    db_items, db_failed = snapshot_dbs()
    raw_items = collect_raw_recap()
    items = db_items + raw_items
    total_mb = sum(os.path.getsize(p) for p, _ in items) / 1048576
    log(f"  待处理 {len(items)} 个对象，共 {total_mb:.1f} MB"
        f"（数据库 {len(db_items)} · 课件 {len(raw_items)}）")

    if args.dry_run:
        log("── DRY-RUN：不联网、不上传 ──")
        for _, k in items[:5]:
            log(f"    {k}")
        if len(items) > 5:
            log(f"    …… 另 {len(items)-5} 个")
        log(f"[{ts}] {'✅ 完成' if not db_failed else '⚠️ 快照有失败项：' + ','.join(db_failed)}")
        flush_log()
        sys.exit(1 if db_failed else 0)

    try:
        import tos
    except ImportError:
        log("✗ 未装 SDK：请先 `pip3 install tos`"); flush_log(); sys.exit(1)

    for k in ("TOS_ACCESS_KEY", "TOS_SECRET_KEY", "TOS_ENDPOINT"):
        if not env.get(k):
            log(f"✗ .env 缺 {k}"); flush_log(); sys.exit(1)

    client = tos.TosClientV2(env["TOS_ACCESS_KEY"], env["TOS_SECRET_KEY"], endpoint, region)

    def remote_size(key):
        """返回云端对象大小；不存在/查不到则 None（当作需要上传）"""
        try:
            r = client.head_object(bucket, key)
            for attr in ("content_length", "size", "object_size"):
                v = getattr(r, attr, None)
                if isinstance(v, int):
                    return v
        except Exception:
            pass
        return None

    def upload(path, key):
        """SDK 版本差异兜底：优先 put_object_from_file，退回 put_object(content=file)"""
        if hasattr(client, "put_object_from_file"):
            client.put_object_from_file(bucket, key, path)
        else:
            with open(path, "rb") as f:
                client.put_object(bucket, key, content=f)

    log("── 上传 TOS ──")
    up = skip = err = 0
    up_mb = 0.0
    for path, rel in items:
        key = f"{prefix}/{rel}"
        try:
            local = os.path.getsize(path)
            # 数据库每次必传（内容天天变、体积小）；课件按 size 比对增量
            if not args.full and rel.startswith("Raw-Recap/") and remote_size(key) == local:
                skip += 1
                continue
            upload(path, key)
            up += 1
            up_mb += local / 1048576
        except Exception as e:
            err += 1
            log(f"  ✗ {key}：{type(e).__name__}: {e}")
            if err <= 1:
                log("    " + traceback.format_exc().strip().splitlines()[-1])

    log(f"  上传 {up} 个（{up_mb:.1f} MB）· 跳过 {skip} 个（云端已一致）· 失败 {err} 个")
    bad = err or db_failed
    log(f"[{ts}] " + ("✅ 完成" if not bad else "⚠️ 有失败项——见上（绝不静默成功）"))
    flush_log()
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
