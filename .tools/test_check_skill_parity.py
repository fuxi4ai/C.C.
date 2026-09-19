#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_skill_parity 的持久化负向测试（2026-09-19 立）

关键守卫必须有持久化负向测试——本文件为 `check_skill_parity.py` 的回归网。
在临时目录里搭最小四端夹具，逐个注入真实见过的失败形态，断言退出码与检出信息。

跑法：  python3 brain/.tools/test_check_skill_parity.py
退出码：0 = 全过；1 = 有用例失败
"""
from __future__ import annotations

import pathlib
import shutil
import subprocess
import sys
import tempfile
import textwrap
import zipfile

HERE = pathlib.Path(__file__).resolve().parent
CHECKER = HERE / "check_skill_parity.py"

FM = '---\nname: "brain-x"\ndescription: "示例 skill——触发：`/x`。"\n---\n'
BODY = "# brain-x\n\n正文一行。\n"


def build(root: pathlib.Path, *, body: bytes | None = None) -> tuple[pathlib.Path, pathlib.Path]:
    """搭 canonical / portable / 包 / runtime 四端一致的最小夹具。"""
    docs = root / "docs"
    skills = docs / "Claude/brain/.skills"
    portable = docs / "Claude/brain/portable/skills"
    runtime = root / "rt"
    skill = (FM + BODY).encode("utf-8")
    body = skill if body is None else body
    for d in (skills / "brain-x", portable / "brain-x", runtime / "brain-x"):
        d.mkdir(parents=True, exist_ok=True)
    (skills / "brain-x/SKILL.md").write_bytes(body)
    (portable / "brain-x/SKILL.md").write_bytes(body)
    with zipfile.ZipFile(skills / "brain-x.skill", "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("brain-x/SKILL.md", body)
    (runtime / "brain-x/SKILL.md").write_bytes(body)
    return docs, runtime


def run(docs: pathlib.Path, runtime: pathlib.Path, *extra: str):
    return subprocess.run(
        [sys.executable, str(CHECKER), "--docs", str(docs), "--runtime", str(runtime), *extra],
        capture_output=True, text=True,
    )


CASES = []


def case(name):
    def deco(fn):
        CASES.append((name, fn))
        return fn
    return deco


@case("四端一致 → rc 0")
def _clean(root):
    docs, rt = build(root)
    r = run(docs, rt)
    return r.returncode == 0, r


@case("runtime 仅差末端空行 → rc 0（已知归一化）")
def _eof(root):
    docs, rt = build(root)
    p = rt / "brain-x/SKILL.md"
    p.write_bytes(p.read_bytes() + b"\n")
    r = run(docs, rt)
    ok = r.returncode == 0 and "仅差末端空行" in r.stdout
    return ok, r


@case("runtime 内容分歧 → rc 1")
def _diverge(root):
    docs, rt = build(root)
    p = rt / "brain-x/SKILL.md"
    p.write_bytes(p.read_bytes().replace("正文一行".encode(), "正文两行".encode()))
    r = run(docs, rt)
    return r.returncode == 1 and "runtime 分歧" in r.stdout, r


@case("runtime 双 frontmatter 块 → rc 1")
def _dup(root):
    docs, rt = build(root)
    p = rt / "brain-x/SKILL.md"
    p.write_bytes((FM + (FM + BODY)).encode("utf-8"))
    r = run(docs, rt)
    return r.returncode == 1 and "重复 frontmatter 块" in r.stdout, r


@case("canonical frontmatter YAML 不合法（G-X187 形态）→ rc 1")
def _badyaml(root):
    bad = '---\nname: "brain-x"\ndescription: "路径 `F:\\Mac_Backup\\{项目}\\`。"\n---\n' + BODY
    docs, rt = build(root, body=bad.encode("utf-8"))
    r = run(docs, rt)
    return r.returncode == 1 and "frontmatter 解析失败" in r.stdout, r


@case("仓内三端不一致（portable 落后）→ rc 1")
def _inrepo(root):
    docs, rt = build(root)
    (docs / "Claude/brain/portable/skills/brain-x/SKILL.md").write_bytes(
        (FM + BODY + "新加一行。\n").encode("utf-8"))
    r = run(docs, rt)
    return r.returncode == 1 and "仓内三端不一致" in r.stdout, r


@case("runtime 不可达 → 默认 rc 0（只降级警告）")
def _nort(root):
    docs, _ = build(root)
    r = run(docs, root / "nonexistent")
    return r.returncode == 0 and "runtime 未核" in r.stdout, r


@case("runtime 不可达 + --strict → rc 1")
def _nort_strict(root):
    docs, _ = build(root)
    r = run(docs, root / "nonexistent", "--strict")
    return r.returncode == 1, r


@case("--name 过滤生效")
def _filter(root):
    docs, rt = build(root)
    r = run(docs, rt, "--name", "brain-y")
    return r.returncode == 0 and "brain-x" not in r.stdout, r


def main() -> int:
    print(f"# check_skill_parity 负向测试 · {len(CASES)} 例")
    failed = 0
    for name, fn in CASES:
        tmp = pathlib.Path(tempfile.mkdtemp(prefix="csp_"))
        try:
            ok, r = fn(tmp)
        except Exception as e:  # noqa: BLE001
            ok, r = False, None
            print(f"  ✗ {name} — 用例自身抛错：{type(e).__name__}: {e}")
        else:
            mark = "✓" if ok else "✗"
            print(f"  {mark} {name}" + ("" if ok else f"  (rc={r.returncode})"))
            if not ok and r is not None:
                print(textwrap.indent((r.stdout + r.stderr)[-500:], "      "))
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
        failed += 0 if ok else 1
    print()
    print(f"{'✓ 全过' if not failed else f'✗ {failed} 例失败'}（{len(CASES) - failed}/{len(CASES)}）")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
