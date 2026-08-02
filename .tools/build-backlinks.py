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

# ── 三分法（2026-07-30 /consolidate 加）──────────────────────────────
# 解析不到的 wikilink 分三类，只有第三类才是真悬空：
#   ① 标记   —— 编号/概念，本就无对应文件（[[GE-02]] / [[GOTCHAS G019]] / [[C-12 纪律轴]]）
#   ② 跨库   —— 文件真实存在，但在 vault 外（Projects/ 下），Obsidian 解析不到而已
#   ③ 真悬空 —— 既非标记、全盘也找不到，才需要人去修
#
# ⚠ 刻意**不把 EXP- 列进标记族**：经验库条目有正确写法 [[经验库#EXP-…]],
#   裸写 [[EXP-…]] 是 bug（2026-07-30 修过 4 处）。放进白名单等于把真 bug 静默藏起来。
#   同理 ERR-/INFRA- 等 GOTCHAS 编号也不收——它们该写成 [[{项目}/GOTCHAS]] + 正文提编号。
MARKER_RE = re.compile(
    r"^("
    r"GE-\d"              # PEC 事件研究编号
    r"|CS-\d|C-\d|CR-\d"  # PEC 案例 / 框架 / 比较研究编号
    r"|G-X?\d"            # 通用教训编号
    r"|A\d\d"             # PEC 附件编号（A00 反偏置清单 等）
    r"|GOTCHAS\s"         # 「GOTCHAS G019」这类「文件名+条目号」写法
    r")"
)

# 跨库扫描根：brain 的父目录（Claude/），排除 vault 自身与不可能放笔记的目录
CROSSREF_SKIP = {".git", ".venv", "node_modules", "__pycache__", "brain", "Brain",
                 ".index", ".tools", ".skills", "_to_delete_20260721"}


def build_crossref_index(brain_root: Path) -> dict:
    """扫 vault 外的 .md，建 stem → 相对路径索引。用于把「跨库引用」与「真悬空」分开。"""
    outside = {}
    scan_root = brain_root.parent
    if not scan_root.exists():
        return outside
    for p in scan_root.rglob("*.md"):
        try:
            rel = p.relative_to(scan_root)
        except ValueError:
            continue
        if any(seg in CROSSREF_SKIP for seg in rel.parts):
            continue
        outside.setdefault(p.stem, str(rel))
    return outside


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

    # 跨库索引（vault 外真实存在的 .md）
    crossref_index = build_crossref_index(root)

    # 第二遍：扫 wikilink
    backlinks = defaultdict(lambda: {"incoming": set(), "outgoing": set()})
    dangling = []
    crossrefs = []
    markers = []

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
                # 2026-08-02 订正：任何路径段含 logs 都算（渊图/logs、agents/烛阴/logs 同性质），原先只认顶层
                src_parts = source_rel.split("/")
                if "logs" in src_parts or src_parts[0] == "chats":
                    continue
                # 三分法：标记 / 跨库 / 真悬空（见文件头 MARKER_RE 注释）
                if MARKER_RE.match(t):
                    markers.append(f"{source_rel}  →  [[{t}]]")
                elif t in crossref_index:
                    crossrefs.append(f"{source_rel}  →  [[{t}]]  ⇒  {crossref_index[t]}")
                elif t.split("/")[0] in {"Database", "AI4ME"}:
                    # 2026-08-02：路径式跨库（目标根在 ~/Documents 下、Claude/ 之外）——stem 索引永远配不上，
                    # 且沙箱挂载看不到该根、无法验存在性 ⇒ 按路径前缀归跨库，不当真悬空报
                    crossrefs.append(f"{source_rel}  →  [[{t}]]  ⇒  （路径式跨库 · 存在性未在本环境验证）")
                else:
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

    # dangling —— 只剩「真悬空」：既非编号标记、全盘也找不到
    dangling_path = INDEX_DIR / "dangling.txt"
    dangling_path.write_text(
        "# 真悬空 wikilink（既非编号标记、vault 内外都找不到对应文件）—— 这些才需要人去修\n"
        "# 标记类见 markers.txt · 跨库类见 crossref.txt\n"
        "# 生成于 build-backlinks.py\n\n" + "\n".join(dangling),
        encoding="utf-8"
    )

    # crossref —— 文件真实存在但在 vault 外，Obsidian 解析不到而已，不是错
    (INDEX_DIR / "crossref.txt").write_text(
        "# 跨库引用：目标文件真实存在，但在 Obsidian vault 之外（Projects/ 下）\n"
        "# 不是错误——除非把 vault 根上提，否则 [[ ]] 天然解析不到\n"
        "# 生成于 build-backlinks.py\n\n" + "\n".join(crossrefs),
        encoding="utf-8"
    )

    # markers —— 把 [[ ]] 当编号/概念标记用，本就无对应文件
    (INDEX_DIR / "markers.txt").write_text(
        "# 标记类 wikilink：[[ ]] 被当作编号/概念的强调记号，本就无对应文件\n"
        "# 识别规则见 build-backlinks.py 的 MARKER_RE（刻意不含 EXP-/ERR-，那些裸写是 bug）\n"
        "# 生成于 build-backlinks.py\n\n" + "\n".join(markers),
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
    print(f"   真悬空：{total_dangling}  → dangling.txt（这些才要修）")
    print(f"   跨库引用：{len(crossrefs)}  → crossref.txt（文件在 vault 外，非错误）")
    print(f"   编号标记：{len(markers)}  → markers.txt（[[ ]] 当记号用，本无文件）")
    if args.orphans:
        print(f"   permanent 孤儿：{len(orphan_lines)} → orphans.txt")
    print(f"")
    print(f"📁 索引目录：{INDEX_DIR.relative_to(root) if INDEX_DIR.is_relative_to(root) else INDEX_DIR}")


if __name__ == "__main__":
    main()
