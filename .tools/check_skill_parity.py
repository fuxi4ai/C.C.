#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_skill_parity.py — brain-* skill 发布链「四端对拍」只读核检器

背景：brain-* skill 的发布链是 canonical → portable → `.skill` 包 → `save_skill`(runtime)。
四端必须同版，实测最易出的三类偏差：
  ① content 带 frontmatter 传给 save_skill ⇒ runtime 出「双 frontmatter 块」
  ② YAML 双引号标量里写裸反斜杠 ⇒ frontmatter 解析失败（通用教训 G-X187）
  ③ 末端换行差异（属已知归一化，放行）

判定口径：
  · 仓内三端（canonical / portable / 包内）必须**逐字节一致**
  · runtime 与 canonical 的差异**只允许末端空白行**
  · 各端 frontmatter 必须 `yaml.safe_load` 通过
  · runtime 不得出现重复 frontmatter 块

用法：
    python3 brain/.tools/check_skill_parity.py [--docs DIR] [--runtime DIR]
                                               [--name brain-todo ...] [--strict] [--quiet]
    DOCS_DIR / SKILL_RUNTIME_DIR 环境变量等效。
    runtime 目录不可达时默认**只降级为警告**（仍核仓内三端）；加 --strict 则视为失败。

退出码：0 = 无实质分歧 · 1 = 发现分歧 · 2 = 环境不可用（缺 PyYAML / 找不到 .skills）

只读：本脚本不写任何文件、不碰 git。
"""
from __future__ import annotations

import argparse
import difflib
import hashlib
import os
import pathlib
import sys
import zipfile

try:
    import yaml
except ImportError:  # pragma: no cover
    print("✗ 缺 PyYAML：pip install pyyaml（或 pip install --break-system-packages pyyaml）", file=sys.stderr)
    sys.exit(2)

RUNTIME_HINTS = (
    "{home}/.claude/skills",
    "{home}/Library/Application Support/Claude/skills",
    "{home}/Library/Application Support/Claude-3p/skills",
)


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def split_frontmatter(text: str):
    """返回 (frontmatter 文本, 正文, 是否解析出 frontmatter)。"""
    if not text.startswith("---"):
        return None, text, False
    end = text.find("\n---", 3)
    if end == -1:
        return None, text, False
    return text[4:end + 1], text[end + 4:], True


def dup_frontmatter(text: str) -> bool:
    """正文开头若又紧跟一个 frontmatter 形块（--- 后 3 行内出现 name:/description:），判为重复。"""
    _, body, ok = split_frontmatter(text)
    if not ok:
        return False
    lines = body.splitlines()
    i = 0
    while i < len(lines) and not lines[i].strip():
        i += 1
    if i >= len(lines) or lines[i].strip() != "---":
        return False
    for j in range(i + 1, min(i + 4, len(lines))):
        if lines[j].startswith(("name:", "description:")):
            return True
    return False


def parse_fm(text: str):
    fm, _, ok = split_frontmatter(text)
    if not ok:
        return None, "无 frontmatter"
    try:
        return yaml.safe_load(fm), None
    except Exception as e:  # noqa: BLE001
        return None, f"{type(e).__name__}: {str(e).splitlines()[0][:70]}"


def classify(canon: bytes, rt: bytes) -> tuple[str, str]:
    """返回 (类别, 说明)。类别 ∈ identical / eof-only / divergent。"""
    if canon == rt:
        return "identical", ""
    if canon.rstrip(b"\n") == rt.rstrip(b"\n"):
        return "eof-only", "末端空白行差异（已知归一化）"
    a = canon.decode("utf-8", "replace").splitlines()
    b = rt.decode("utf-8", "replace").splitlines()
    hunks = [x for x in difflib.unified_diff(a, b, lineterm="", n=0)
             if x[:1] in "+-" and x[:3] not in ("+++", "---")]
    detail = " | ".join(x[:90] for x in hunks[:4])
    if len(hunks) > 4:
        detail += f" …共 {len(hunks)} 行"
    return "divergent", detail


def pack_member(pkg: pathlib.Path) -> tuple[bytes | None, str]:
    if not pkg.exists():
        return None, "包不存在"
    try:
        with zipfile.ZipFile(pkg) as z:
            cands = [n for n in z.namelist() if n.endswith("SKILL.md")]
            if not cands:
                return None, "包内无 SKILL.md"
            if z.testzip() is not None:
                return None, "包 CRC 校验失败"
            return z.read(cands[0]), cands[0]
    except zipfile.BadZipFile:
        return None, "包不是合法 zip"


def main() -> int:
    ap = argparse.ArgumentParser(description="brain-* skill 四端对拍（只读）")
    ap.add_argument("--docs", default=os.environ.get("DOCS_DIR") or os.path.expanduser("~/Documents"))
    ap.add_argument("--runtime", default=os.environ.get("SKILL_RUNTIME_DIR") or "")
    ap.add_argument("--name", action="append", default=[], help="只核指定 skill（可多次）")
    ap.add_argument("--all", action="store_true",
                    help="核 .skills/ 下全部目录（含非 brain-* 家族；它们无 portable 链，差异属信息性）")
    ap.add_argument("--strict", action="store_true", help="runtime 不可达也算失败")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    brain = pathlib.Path(args.docs) / "Claude/brain"
    skills_dir = brain / ".skills"
    portable = brain / "portable/skills"
    if not skills_dir.is_dir():
        print(f"✗ 找不到 {skills_dir}", file=sys.stderr)
        return 2

    names = sorted(d.name for d in skills_dir.iterdir()
                   if d.is_dir() and (d / "SKILL.md").is_file())
    if not args.all:
        # 默认只核 7 个 brain-*（canonical 裁定的射程）；其余家族无 portable 链、不属本对拍
        names = [n for n in names if n.startswith("brain-") and not n.startswith("_DEPRECATED_")]
    if args.name:
        names = [n for n in names if n in set(args.name)]

    rt_root = None
    if args.runtime:
        rt_root = pathlib.Path(args.runtime).expanduser()
        if not rt_root.is_dir():
            rt_root = None
    else:
        for hint in RUNTIME_HINTS:
            p = pathlib.Path(hint.format(home=os.path.expanduser("~")))
            if p.is_dir():
                rt_root = p
                break

    problems: list[str] = []
    print(f"# brain-* skill 四端对拍 · {len(names)} 个")
    print(f"# docs     = {brain}")
    print(f"# runtime  = {rt_root if rt_root else '⚠ 不可达（本跑只核仓内三端）'}")
    print()
    hdr = f"{'skill':<20}{'canonical':<11}{'portable':<11}{'包内':<11}{'runtime':<11}判定"
    print(hdr)
    print("-" * len(hdr))

    for n in names:
        c_path = skills_dir / n / "SKILL.md"
        p_path = portable / n / "SKILL.md"
        c = c_path.read_bytes()
        p = p_path.read_bytes() if p_path.exists() else b""
        z, zinfo = pack_member(skills_dir / f"{n}.skill")

        rt = None
        if rt_root is not None:
            rp = rt_root / n / "SKILL.md"
            rt = rp.read_bytes() if rp.exists() else b""

        # 仓内三端
        if z is None:
            problems.append(f"{n}: {zinfo}")
            in_repo, in_repo_note = False, zinfo
        elif c == p == z:
            in_repo, in_repo_note = True, ""
        else:
            in_repo = False
            tiers = {"canonical": sha(c)[:8], "portable": sha(p)[:8], "包内": sha(z)[:8]}
            uniq = set(tiers.values())
            in_repo_note = " / ".join(f"{k}={v}" for k, v in tiers.items()) if len(uniq) > 1 else "差异"

        # runtime
        if rt is None:
            rt_cls, rt_note = "n/a", "runtime 不可达"
        elif not rt:
            rt_cls, rt_note = "missing", "runtime 缺该 skill"
        else:
            rt_cls, rt_note = classify(c, rt)

        verdict = ("仓内三端一致" if in_repo else "✗ 仓内不一致")
        if rt_cls == "identical":
            verdict += " · 四端一致 ✓"
        elif rt_cls == "eof-only":
            verdict += " · runtime 仅差末端空行"
        elif rt_cls == "n/a":
            verdict += " · runtime 未核"
        else:
            verdict += " · ✗ runtime 分歧"
        print(f"{n:<20}{sha(c)[:8]:<11}{(sha(p)[:8] if p else '—'):<11}"
              f"{(sha(z)[:8] if z else '—'):<11}{(sha(rt)[:8] if rt else '—'):<11}{verdict}")

        if not args.quiet:
            if not in_repo:
                print(f"    ✗ 仓内三端不一致：{in_repo_note}")
            if rt_cls == "eof-only":
                print("    · runtime 差异已归一（仅末端空白行）")
            elif rt_cls in ("divergent", "missing"):
                print(f"    ✗ runtime 分歧：{rt_note}")

        # frontmatter 体检（四端各自）
        for label, blob in (("canonical", c), ("portable", p), ("包内", z), ("runtime", rt)):
            if not blob:
                continue
            text = blob.decode("utf-8", "replace")
            _, err = parse_fm(text)
            if err:
                problems.append(f"{n}/{label}: frontmatter 解析失败 → {err}")
                print(f"    ✗ {label} frontmatter 解析失败：{err}")
            if dup_frontmatter(text):
                problems.append(f"{n}/{label}: 重复 frontmatter 块")
                print(f"    ✗ {label} 出现重复 frontmatter 块（save_skill 的 content 带了 frontmatter）")

        if not in_repo:
            problems.append(f"{n}: 仓内三端不一致（{in_repo_note}）")
        if rt_cls in ("divergent", "missing"):
            problems.append(f"{n}: runtime {rt_cls} → {rt_note}")

    print()
    if problems:
        print(f"✗ 发现 {len(problems)} 项问题：")
        for x in problems:
            print(f"   - {x}")
        return 1

    if rt_root is None and args.strict:
        print("✗ runtime 不可达（--strict）→ 未完成四端核验")
        return 1
    print("✓ 无实质分歧：仓内三端逐字节一致；runtime 仅余已知的末端空行归一化；各端 frontmatter 可解析。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
