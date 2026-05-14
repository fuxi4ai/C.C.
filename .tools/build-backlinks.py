#!/usr/bin/env python3
"""
build-backlinks.py — 扫所有 .md 提取 [[wikilink]]，生成回链索引

用法：
  python3 build-backlinks.py [--orphans]

输出：
  brain/.index/backlinks.json
      {
        "笔记 A": {
          "incoming": ["来源文件1.md", "来源文件2.md"],
          "outgoing": ["指向的笔记 B", "笔记 C"]
        },
        ...
      }
  brain/.index/orphans.txt    （--orphans 时）
      未被任何笔记引用的 permanent/ 笔记列表

  brain/.index/dangling.txt
      指向不存在笔记的 wikilink 列表（编辑参考）
"""

import json
import os
import re
import sys
import argparse
from pathlib import Path
from collections import defaultdict

BRAIN_ROOT = Path(os.path.expanduser("~/Documents/Claude/brain"))
SCRIPT_DIR = Path(__file__).resolve().parent
if not BRAIN_ROOT.exists():
    BRAIN_ROOT = SCRIPT_DIR.parent

INDEX_DIR = BRAIN_ROOT / ".index"
SKIP_DIRS = {".git", ".obsidian", ".index", ".tools", ".skills", "graphify"}

# [[Target]] 或 [[Target|Alias]] 或 [[Target#Anchor]]
WIKILINK_RE = re.compile(r"\[\[([^\]\|#]+)(?:#[^\]\|]+)?(?:\|[^\]]+)?\]\]")


def is_skip(p: Path, root: Path) -> bool:
    parts = p.relative_to(root).parts
    return any(seg in SKIP_DIRS or seg.startswith("_DEPRECATED") or seg.startswith("_TRASH") for seg in parts)


def walk_md(root: Path):
    for p in sorted(root.rglob("*.md")):
        if not is_skip(p, root):
            yield p


def note_name(p: Path) -> str:
    """笔记名 = 不带 .md 的文件名（Obsidian wikilink 习惯）"""
    return p.stem


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--orphans", action="store_true", help="额外报告无入链 permanent 笔记")
    parser.add_argument("--root", default=str(BRAIN_ROOT))
    args = parser.parse_args()

    root = Path(args.root)
    INDEX_DIR.mkdir(exist_ok=True)

    # 第一遍：建立 name → file path + path_set
    name_to_file = {}
    all_notes = []
    path_set = set()  # 相对路径含 .md
    for p in walk_md(root):
        name = note_name(p)
        rel = str(p.relative_to(root))
        all_notes.append(rel)
        path_set.add(rel)
        name_to_file.setdefault(name, []).append(rel)

    # 第二遍：扫 wikilink
    backlinks = defaultdict(lambda: {"incoming": set(), "outgoing": set()})
    dangling = []

    for p in walk_md(root):
        source = note_name(p)
        source_rel = str(p.relative_to(root))
        try:
            text = p.read_text(encoding="utf-8")
        except Exception:
            continue
        # 去掉 frontmatter，避免误把 yaml 里的方括号当 wikilink
        if text.startswith("---"):
            end = text.find("\n---", 3)
            if end != -1:
                text = text[end + 4:]

        # 剥 fenced code block（```...```）和 inline code（`...`），避免误识别示例 [[xxx]]
        text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
        text = re.sub(r"`[^`\n]+`", "", text)

        targets = WIKILINK_RE.findall(text)
        for t in targets:
            t = t.strip()
            if not t:
                continue
            backlinks[source]["outgoing"].add(t)
            backlinks[t]["incoming"].add(source_rel)
            # 解析顺序：path 形式（A/B/C → A/B/C.md）→ stem
            resolved = None
            if (t + ".md") in path_set:
                resolved = t + ".md"
            elif t in path_set:
                resolved = t
            elif t in name_to_file:
                resolved = name_to_file[t][0]
            if resolved is None:
                # logs/ 和 chats/ 是历史定格内容，不算活跃 dangling
                src_top = source_rel.split("/")[0]
                if src_top not in {"logs", "chats"}:
                    dangling.append(f"{source_rel}  →  [[{t}]]")

    # 序列化
    out = {}
    for k in sorted(backlinks.keys()):
        out[k] = {
            "incoming": sorted(backlinks[k]["incoming"]),
            "outgoing": sorted(backlinks[k]["outgoing"]),
        }

    backlinks_path = INDEX_DIR / "backlinks.json"
    backlinks_path.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")

    # dangling
    dangling_path = INDEX_DIR / "dangling.txt"
    dangling_path.write_text(
        "# 指向不存在笔记的 wikilink\n# 生成于 build-backlinks.py\n\n" + "\n".join(dangling),
        encoding="utf-8"
    )

    # orphans（仅 --orphans 时）
    orphan_lines = []
    if args.orphans:
        for p in walk_md(root):
            if "permanent" not in p.relative_to(root).parts:
                continue
            name = note_name(p)
            inc = backlinks.get(name, {}).get("incoming", set())
            if not inc:
                orphan_lines.append(str(p.relative_to(root)))
        orphans_path = INDEX_DIR / "orphans.txt"
        orphans_path.write_text(
            "# 无入链的 permanent 笔记（孤儿）\n# 生成于 build-backlinks.py --orphans\n\n" + "\n".join(orphan_lines),
            encoding="utf-8"
        )

    # 摘要
    total_notes = len(all_notes)
    total_with_outgoing = sum(1 for v in out.values() if v["outgoing"])
    total_with_incoming = sum(1 for v in out.values() if v["incoming"])
    total_dangling = len(dangling)

    print(f"📚 backlinks.json 已生成（{len(out)} 个节点）")
    print(f"   总笔记：{total_notes}")
    print(f"   有出链：{total_with_outgoing}")
    print(f"   有入链：{total_with_incoming}")
    print(f"   悬空链接：{total_dangling}")
    if args.orphans:
        print(f"   permanent 孤儿：{len(orphan_lines)} → orphans.txt")
    print(f"")
    print(f"📁 索引目录：{INDEX_DIR.relative_to(root) if INDEX_DIR.is_relative_to(root) else INDEX_DIR}")


if __name__ == "__main__":
    main()
