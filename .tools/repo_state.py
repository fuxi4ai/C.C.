#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""repo_state.py — **不跑任何 git 子命令**的工作区状态报告器（只读）

## 为什么需要它

本仓（以及多个姊妹仓）有一条硬约束：**沙箱内禁跑任何 git 子命令**——连
`git status` / `git log` 这类「看起来只读」的也不行。理由是实测的：
`git status` 会**刷新索引并创建 `.git/index.lock`**，而沙箱**无权删除**该锁
（`unable to unlink '.git/index.lock': Operation not permitted`），残留 0 字节孤儿锁
会让 Doctor 终端的 commit 直接报 `Another git process seems to be running`。

但「禁跑」不等于「不需要知道仓况」。本工具用**纯 Python 读 `.git/index` 二进制**，
给出 /save、/todo、收尾对账都需要的那几项，**全程零 git 子进程、不写 `.git/`**。

## 它报什么（全部来自实读，非估算）

| 项 | 判据 | 可信度 |
|---|---|---|
| 已跟踪但内容变了 | 对每个 index 条目**重算 git blob sha1**（`sha1("blob <len>\\0" + 内容)`）并与 index 内记录值比对 | **精确**（不是 mtime/size 近似） |
| index 有记录但盘上没了 | 条目路径 `os.path.exists` 为假 | 精确 |
| 未跟踪 | 走遍工作区，取不在 index 路径集里的文件 | **见下方 ignore 限制** |
| 工作区文件数 / index 条目数 | 计数 | 精确 |

## 它**不能**报什么（诚实边界，别越界使用）

1. **「index 里记录的」≠「HEAD 里提交的」**。本工具只读 `.git/index`（暂存区快照），
   **不读 `.git/objects`**。所以它答不了「相对 HEAD 有没有 staged 改动」。
   若 `index` 的 mtime 与末次 commit 时刻对齐，可作为「暂存区已随 commit 落地」的
   **间接**旁证 —— 那是旁证，不是证明。
2. **ignore 判定是简化子集**。`_simplified_ignored()` 只处理 `dir/`、`*.ext`、
   纯文件名、以及以 `/` 结尾的目录形式，走 `fnmatch`；**未实现** gitignore 的完整语义
   （`!` 取反、`**`、前导 `/` 锚定、嵌套 `.gitignore`、`.git/info/exclude`、
   以及「父目录被忽略则子文件全忽略」的传递规则）。⇒ **不得用它断言「这个文件是否被
   git 忽略」**；要定论，请构造 `git check-ignore -v <paths>` 交 Doctor 终端跑。
   输出里这一组**始终带「简化匹配·仅供参考」标记**。
3. **不解 delta / pack**。只读 index，不解析 packfile；故拿不到历史。
4. **不判半开状态**。rebase/merge/cherry-pick 的探测请直接 `ls`/`cat` `.git/` 下
   `rebase-merge/` `rebase-apply/` `MERGE_HEAD` `CHERRY_PICK_HEAD` `REVERT_HEAD`
   `BISECT_LOG`，以及 `cat .git/HEAD` 看是否 `ref: refs/heads/...`。

## 用法

    python3 brain/.tools/repo_state.py [--root DIR] [--json] [--no-ignore-filter]
    python3 brain/.tools/repo_state.py --self-test

退出码：`0` 报告出；`2` 环境错（`.git/index` 读不到 / 不是 git 仓）。

**来源** → 2026-10-03 damper 契约化场（本场两次实用于 brain 仓，替代 `git status`）。
"""

from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import os
import pathlib
import struct
import sys
import tempfile


# ────────────────────────────── index 解析 ──────────────────────────────

def parse_index(path: pathlib.Path):
    """解析 .git/index（DIRC v2/v3）。返回 (version, [entries])。

    v2/v3 条目布局：10×u32 + 20B sha + u16 flags [+ u16 ext] + path(NUL) + 8 字节对齐填充。
    v4 的前缀压缩未实现 —— 那种情形直接抛，不静默给错数据。
    """
    b = path.read_bytes()
    if b[:4] != b"DIRC":
        raise ValueError("不是 git index（缺 DIRC 魔数）")
    ver = struct.unpack(">I", b[4:8])[0]
    if ver not in (2, 3):
        raise ValueError(f"index 版本 v{ver} 未支持（本器只解 v2/v3；v4 用前缀压缩）")
    n = struct.unpack(">I", b[8:12])[0]
    i, out = 12, []
    for _ in range(n):
        if i + 62 > len(b):
            raise ValueError("index 截断（条目越界）")
        (_ct_s, _ct_n, mt_s, _mt_n, _dev, _ino, _mode, _uid, _gid,
         size, sha, flags) = struct.unpack(">IIIIIIIIII20sH", b[i:i + 62])
        j = i + 62
        e = j + 2 if (flags & 0x4000) else j          # 扩展标志
        while e < len(b) and b[e] != 0:
            e += 1
        out.append({
            "path": b[j:e].decode("utf-8", "replace"),
            "mtime": mt_s,
            "size": size,
            "sha": sha.hex(),
        })
        i += ((62 + (e - j) + 1) + 7) // 8 * 8          # NUL + 补到 8 的倍数
    return ver, out


def blob_sha1(fp: pathlib.Path) -> str:
    """git blob sha1 —— sha1("blob <len>\\0" + 内容)。这是 git 自己的定义，可逐位复算。"""
    d = fp.read_bytes()
    h = hashlib.sha1()
    h.update(b"blob %d\0" % len(d))
    h.update(d)
    return h.hexdigest()


# ──────────────────────────── 简化 ignore 匹配 ────────────────────────────

def load_simple_patterns(root: pathlib.Path):
    """读 .gitignore 的**简化子集**（见模块 docstring 的边界第 2 条）。"""
    pats = []
    f = root / ".gitignore"
    if not f.exists():
        return pats
    for line in f.read_text(encoding="utf-8", errors="replace").splitlines():
        s = line.strip()
        if not s or s.startswith("#") or s.startswith("!"):
            continue
        pats.append(s.lstrip("/"))
    return pats


def _simplified_ignored(rel: str, pats) -> bool:
    """**简化**匹配：整路径 fnmatch / basename fnmatch / 任一级目录名命中 `dir/` 形式。

    未实现 gitignore 完整语义 —— 只作提示，不作判据。
    """
    parts = rel.split("/")
    for p in pats:
        if p.endswith("/"):
            if p[:-1] in parts:
                return True
            continue
        if fnmatch.fnmatch(rel, p) or fnmatch.fnmatch(os.path.basename(rel), p):
            return True
        for k in range(1, len(parts)):
            if fnmatch.fnmatch("/".join(parts[k:]), p):
                return True
    return False


# ──────────────────────────────── 报告 ────────────────────────────────

def collect(root: pathlib.Path, ignore_filter: bool = True) -> dict:
    gi = root / ".git" / "index"
    if not gi.exists():
        raise FileNotFoundError(f"读不到 {gi} —— 该目录不是 git 仓（或无 index）")
    ver, ents = parse_index(gi)

    modified, gone = [], []
    for e in ents:
        fp = root / e["path"]
        if not fp.exists():
            gone.append(e["path"])
            continue
        try:
            if blob_sha1(fp) != e["sha"]:
                modified.append(e["path"])
        except OSError as ex:
            modified.append(f"{e['path']}  [读失败: {ex.__class__.__name__}]")

    tracked = {e["path"] for e in ents}
    unt_clean, unt_ignored = [], []
    pats = load_simple_patterns(root) if ignore_filter else []
    for dp, dns, fns in os.walk(root):
        if ".git" in dns:
            dns.remove(".git")
        for f in fns:
            rel = os.path.relpath(os.path.join(dp, f), root)
            if rel in tracked:
                continue
            (unt_ignored if (pats and _simplified_ignored(rel, pats)) else unt_clean).append(rel)

    return {
        "root": str(root),
        "index_version": ver,
        "index_entries": len(ents),
        "modified": sorted(modified),
        "missing_from_worktree": sorted(gone),
        "untracked": sorted(unt_clean),
        "untracked_simplified_ignored": sorted(unt_ignored),
    }


def render(r: dict) -> None:
    print(f"# repo_state（**未跑任何 git 子命令**）· root = {r['root']}")
    print(f"# index v{r['index_version']} · 条目 {r['index_entries']}")
    print(f"-- 已跟踪但内容变了（blob sha1 逐件复算）: {len(r['modified'])}")
    for x in r["modified"]:
        print("   M", x)
    print(f"-- index 有记录但盘上没了: {len(r['missing_from_worktree'])}")
    for x in r["missing_from_worktree"]:
        print("   D", x)
    print(f"-- 未跟踪（未被简化 ignore 命中）: {len(r['untracked'])}")
    for x in r["untracked"]:
        print("   ??", x)
    print(f"-- 未跟踪（**简化** ignore 命中 · 仅供参考，非 gitignore 判据）: "
          f"{len(r['untracked_simplified_ignored'])}")
    print("⚠ 本器只读 .git/index ⇒ **答不了「相对 HEAD 有无 staged 改动」**；"
          "ignore 判定为简化子集 ⇒ 要定论请交 Doctor 终端跑 `git check-ignore -v`。")


# ────────────────────────────── self-test ──────────────────────────────

def self_test() -> int:
    cases, ok = [], 0
    with tempfile.TemporaryDirectory(prefix="rs_selftest_") as td:
        root = pathlib.Path(td)

        # T1 · 缺 .git/index ⇒ 抛（不静默给空报告）
        try:
            collect(root)
            cases.append(("T1 无 .git/index ⇒ 应抛", False))
        except FileNotFoundError:
            cases.append(("T1 无 .git/index ⇒ 抛 FileNotFoundError", True))

        # 构造一个**最小合法 index**（v2 · 两条目），不依赖真 git
        gi = root / ".git"
        gi.mkdir(parents=True, exist_ok=True)
        (root / "a.txt").write_text("hello\n", encoding="utf-8")
        (root / "sub").mkdir()
        (root / "sub" / "b.txt").write_text("world\n", encoding="utf-8")
        (root / ".gitignore").write_text("*.bak_*\n_bak/\n", encoding="utf-8")
        (root / "x.bak_2026").write_text("bak\n", encoding="utf-8")

        def mk_entry(rel, content_bytes):
            h = hashlib.sha1()
            h.update(b"blob %d\0" % len(content_bytes))
            h.update(content_bytes)
            path = rel.encode()
            base = struct.pack(">IIIIIIIIII20sH", 0, 0, 0, 0, 0, 0, 0o100644, 0, 0,
                               len(content_bytes), bytes.fromhex(h.hexdigest()), len(path))
            pad = (8 - ((62 + len(path) + 1) % 8)) % 8
            return base + path + b"\0" + b"\0" * pad

        ents = (mk_entry("a.txt", b"hello\n") + mk_entry("sub/b.txt", b"world\n"))
        (gi / "index").write_bytes(b"DIRC" + struct.pack(">II", 2, 2) + ents)
        (gi / "HEAD").write_text("ref: refs/heads/main\n", encoding="utf-8")

        r = collect(root)
        cases.append(("T2 干净仓 ⇒ 0 处已跟踪改动", r["modified"] == [] and r["missing_from_worktree"] == []))
        cases.append(("T3 `x.bak_2026` 命中 `.gitignore` 的 `*.bak_*` ⇒ 归入「简化命中」组",
                      r["untracked_simplified_ignored"] == ["x.bak_2026"]))
        cases.append(("T4 未被简化命中的组只余 `.gitignore` 自身（夹具里它未被跟踪）",
                      r["untracked"] == [".gitignore"]))

        # 另加一个**不**被任何规则命中的散件 ⇒ 须落在未忽略组
        (root / "loose.json").write_text("{}\n", encoding="utf-8")
        r_loose = collect(root)
        cases.append(("T4b 新散件 `loose.json` 不命中任何规则 ⇒ 归入未忽略组",
                      sorted(r_loose["untracked"]) == [".gitignore", "loose.json"]))

        # 改一个被跟踪件 ⇒ 必须被 blob sha1 抓出
        (root / "a.txt").write_text("hello\nCHANGED\n", encoding="utf-8")
        r2 = collect(root)
        cases.append(("T5 改内容 ⇒ 报 M（blob sha1 非 mtime）", r2["modified"] == ["a.txt"]))

        # 删一个被跟踪件 ⇒ 报 D
        (root / "sub" / "b.txt").unlink()
        r3 = collect(root)
        cases.append(("T6 删文件 ⇒ 报 D", r3["missing_from_worktree"] == ["sub/b.txt"]))

        # 只改 mtime 不改内容 ⇒ **不得**误报
        os.utime(root / "a.txt", (0, 0))
        r4 = collect(root)
        cases.append(("T7 仅改 mtime ⇒ 仍报 M（因内容已改）；另建件验证纯 mtime 不误报",
                      r4["modified"] == ["a.txt"]))
        (root / "c.txt").write_text("same\n", encoding="utf-8")
        (gi / "index").write_bytes(b"DIRC" + struct.pack(">II", 2, 3) + ents +
                                   mk_entry("c.txt", b"same\n"))
        os.utime(root / "c.txt", (0, 0))
        r5 = collect(root)
        cases.append(("T8 仅 mtime 变、内容未变 ⇒ **不**报 M（本器与 mtime 法之别）",
                      "c.txt" not in r5["modified"]))

        # v4 index ⇒ 明确拒绝，不静默
        (gi / "index").write_bytes(b"DIRC" + struct.pack(">II", 4, 0))
        try:
            collect(root)
            cases.append(("T9 v4 index ⇒ 应拒绝", False))
        except ValueError:
            cases.append(("T9 v4 index ⇒ 抛 ValueError（不静默给错数据）", True))

    for name, good in cases:
        print(f"  {'✓' if good else '✗'} {name}")
        ok += 1 if good else 0
    print(f"\nself-test: {ok}/{len(cases)}")
    return 0 if ok == len(cases) else 1


def main() -> int:
    ap = argparse.ArgumentParser(description="不跑 git 子命令的工作区状态报告器（只读）")
    ap.add_argument("--root", default=".", help="仓根（默认当前目录）")
    ap.add_argument("--json", action="store_true", help="输出 JSON")
    ap.add_argument("--no-ignore-filter", action="store_true", help="不做简化 ignore 分组")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()

    if args.self_test:
        return self_test()

    root = pathlib.Path(args.root).expanduser().resolve()
    try:
        r = collect(root, ignore_filter=not args.no_ignore_filter)
    except FileNotFoundError as e:
        print(f"✗ {e}", file=sys.stderr)
        return 2
    except ValueError as e:
        print(f"✗ index 解析失败：{e}", file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps(r, ensure_ascii=False, indent=2))
    else:
        render(r)
    return 0


if __name__ == "__main__":
    sys.exit(main())
