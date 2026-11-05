#!/usr/bin/env python3
"""gitcheck.py push 判定的持久化负向测试（G-X83 · 2026-11-05）：pack-refs/gc 后不得误报。需要本机 git，只写临时目录。"""
import contextlib, importlib.util, io, os, pathlib, subprocess, sys, tempfile

sys.dont_write_bytecode = True
SRC = pathlib.Path(__file__).resolve().parent.parent / ".skills/brain-resume/gitcheck.py"
spec = importlib.util.spec_from_file_location("gitcheck", SRC)
gc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gc)
ENV = dict(os.environ, GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@t", GIT_COMMITTER_NAME="t", GIT_COMMITTER_EMAIL="t@t")


def git(cwd, *a):
    subprocess.run(["git", *a], cwd=cwd, env=ENV, check=True, capture_output=True)


def commit(repo, msg):
    with open(os.path.join(repo, "f.txt"), "a") as f:
        f.write(msg + "\n")
    git(repo, "add", "f.txt")
    git(repo, "commit", "-m", msg)


fails = []


def check(name, got, want):
    ok = got == want
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {got!r}")
    if not ok:
        fails.append(name)


with tempfile.TemporaryDirectory(prefix="gitcheck_test_") as td:
    bare, repo, solo = (os.path.join(td, x) for x in ("o.git", "r", "s"))
    git(td, "init", "--bare", "-b", "main", bare)
    git(td, "init", "-b", "main", repo)
    git(repo, "remote", "add", "origin", bare)
    commit(repo, "one")
    git(repo, "push", "-u", "origin", "main")
    gd = os.path.join(repo, ".git")
    check("松散 ref · 已同步", gc.unpushed(gd), [])
    git(repo, "pack-refs", "--all")
    check("pack-refs 后 · 已同步（旧版误报无远端）", gc.unpushed(gd), [])
    commit(repo, "two")
    check("分支松散、远端已打包 · 未 push", gc.unpushed(gd), ["main"])
    git(repo, "pack-refs", "--all")
    check("全部打包 · 未 push", gc.unpushed(gd), ["main"])
    git(repo, "push")
    check("远端松散覆盖打包旧值 · 已同步", gc.unpushed(gd), [])
    git(repo, "gc", "--quiet")
    check("gc 后 · 已同步", gc.unpushed(gd), [])
    git(td, "init", "-b", "main", solo)
    commit(solo, "one")
    git(solo, "pack-refs", "--all")
    check("无远端 · 打包后仍报无远端", gc.unpushed(os.path.join(solo, ".git")), None)
    # gc 后 HEAD 只在 pack 里：完整流程不崩，且 tree 与 git 一致（修前 idx 偏移表、对象头都读错）
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=repo, capture_output=True, text=True).stdout.strip()
    tree = subprocess.run(["git", "rev-parse", "HEAD^{tree}"], cwd=repo, capture_output=True, text=True).stdout.strip()
    check("gc 后 HEAD 确实不是松散对象", os.path.exists(os.path.join(gd, "objects", head[:2], head[2:])), False)
    check("gc 后 tree 与 git 一致", gc.commit_tree_sha(gc.read_obj(gd, head)), tree)
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        gc.check(repo)
    check("gc 后 staged 判定", "staged-uncommitted: none" in buf.getvalue(), True)
    check("gc 后 worktree 判定", "worktree modified (内容级): 0" in buf.getvalue(), True)

print("FAILED: %s" % fails if fails else "全部 PASS")
sys.exit(1 if fails else 0)
