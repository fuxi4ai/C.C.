#!/usr/bin/env python3
"""
validate-frontmatter.py — 扫描 brain/ 所有 .md 校验 YAML frontmatter

用法：
  python3 validate-frontmatter.py [--fix-dates] [--quiet]

输出：
  - 缺 frontmatter 的文件
  - 缺必需字段的文件（title / tags / created / updated / status / type）
  - 字段值非法的文件（status 不在白名单，type 不在白名单，日期格式错）
  - 摘要统计

规则来自：brain/CLAUDE.md § frontmatter
"""

import os
import re
import sys
import argparse
from pathlib import Path
from datetime import datetime

BRAIN_ROOT = Path(os.path.expanduser("~/Documents/Claude/brain"))
SCRIPT_DIR = Path(__file__).resolve().parent
if not BRAIN_ROOT.exists():
    BRAIN_ROOT = SCRIPT_DIR.parent  # fallback：从 .tools/ 推算

REQUIRED_FIELDS = ["title", "tags", "created", "updated", "status", "type"]
VALID_STATUS = {"active", "archived", "draft"}
VALID_TYPE = {"permanent", "fleeting", "log", "resource", "decision", "spec", "index", "reference", "handoff", "bootstrap"}
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

# 跳过这些目录（非笔记内容）
# agents/ 数灵自治区（source 只读 / memory archive 历史定格 / per-agent logs 各灵自理）
# logs/checkpoints/ 中途 progress 文件 · .hooks/ 基础设施 —— 2026-06-11 consolidate 决议
SKIP_DIRS = {".git", ".obsidian", ".index", ".tools", ".skills", ".hooks", "graphify",
             "agents", "checkpoints", "_DEPRECATED", "_TRASH"}

# 颜色
RED = "\033[91m"
YEL = "\033[93m"
GRN = "\033[92m"
DIM = "\033[2m"
RST = "\033[0m"


def parse_frontmatter(text: str):
    """返回 (frontmatter_dict, body)；若无 frontmatter 返回 (None, text)"""
    if not text.startswith("---"):
        return None, text
    end = text.find("\n---", 3)
    if end == -1:
        return None, text
    raw = text[3:end].strip()
    fm = {}
    for line in raw.splitlines():
        if ":" not in line:
            continue
        k, _, v = line.partition(":")
        fm[k.strip()] = v.strip()
    return fm, text[end + 4:]


def check_file(path: Path):
    """返回 list[(level, msg)]，level ∈ {ERROR, WARN}"""
    issues = []
    try:
        text = path.read_text(encoding="utf-8")
    except Exception as e:
        return [("ERROR", f"读文件失败：{e}")]

    fm, _ = parse_frontmatter(text)
    if fm is None:
        issues.append(("ERROR", "缺 frontmatter（不是以 --- 开头或没有闭合）"))
        return issues

    for field in REQUIRED_FIELDS:
        if field not in fm:
            issues.append(("ERROR", f"缺字段：{field}"))

    # templates/ 是脚手架：豁免值白名单(status/type)与日期检查（占位符是正常的）
    is_template = "templates" in path.parts

    if not is_template and "status" in fm:
        st = fm["status"].strip()
        if st not in VALID_STATUS:
            issues.append(("WARN", f"status='{st}' 不在白名单 {sorted(VALID_STATUS)}"))

    if not is_template and "type" in fm:
        tp = fm["type"].strip()
        if tp not in VALID_TYPE:
            issues.append(("WARN", f"type='{tp}' 不在白名单 {sorted(VALID_TYPE)}"))

    if not is_template:
        for date_field in ("created", "updated"):
            if date_field in fm:
                v = fm[date_field].strip()
                if not DATE_RE.match(v):
                    issues.append(("WARN", f"{date_field}='{v}' 不符合 YYYY-MM-DD"))

    return issues


def walk_md(root: Path):
    for p in sorted(root.rglob("*.md")):
        parts = p.relative_to(root).parts
        if any(seg in SKIP_DIRS or seg.startswith("_DEPRECATED") or seg.startswith("_TRASH") for seg in parts):
            continue
        yield p


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--quiet", action="store_true", help="只打印有问题的文件")
    parser.add_argument("--root", default=str(BRAIN_ROOT), help="brain root")
    args = parser.parse_args()

    root = Path(args.root)
    if not root.exists():
        print(f"{RED}brain root 不存在：{root}{RST}", file=sys.stderr)
        sys.exit(2)

    total = 0
    clean = 0
    error_files = 0
    warn_files = 0

    print(f"{DIM}扫描根目录：{root}{RST}\n")

    for md in walk_md(root):
        total += 1
        rel = md.relative_to(root)
        issues = check_file(md)
        if not issues:
            clean += 1
            if not args.quiet:
                print(f"  {GRN}✓{RST} {rel}")
            continue

        has_error = any(lvl == "ERROR" for lvl, _ in issues)
        if has_error:
            error_files += 1
            mark = f"{RED}✗{RST}"
        else:
            warn_files += 1
            mark = f"{YEL}!{RST}"
        print(f"  {mark} {rel}")
        for lvl, msg in issues:
            tag = f"{RED}ERROR{RST}" if lvl == "ERROR" else f"{YEL}WARN {RST}"
            print(f"      {tag}  {msg}")

    print()
    print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"  总扫描：{total} 个 .md 文件")
    print(f"  {GRN}干净：{clean}{RST}    {YEL}警告：{warn_files}{RST}    {RED}错误：{error_files}{RST}")
    print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

    sys.exit(1 if error_files > 0 else 0)


if __name__ == "__main__":
    main()
