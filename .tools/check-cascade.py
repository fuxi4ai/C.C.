#!/usr/bin/env python3
"""
check-cascade.py — 改动某条已沉淀事实前，列出"谁引用了它"（级联复查抓手）

用法：
  python3 check-cascade.py <笔记名|路径> [--no-rebuild]

行为：
  1. 默认先跑 build-backlinks.py 刷新 .index/backlinks.json（保证不读到过期反链）
     —— 加 --no-rebuild 跳过刷新，直接读现有索引（更快但可能过期）
  2. 读 backlinks.json，打印该笔记的 incoming（哪些笔记用 [[..]] 引用了它）
  3. 提示：逐条判断这些引用方是否需要随本次改动同步

边界（诚实声明）：
  只能抓到用 [[wikilink]] 表达的依赖；散文里没加双链的引用抓不到。
  这缓解、不根治级联更新问题。
"""

import json
import subprocess
import sys
import argparse
from pathlib import Path

BRAIN_ROOT = Path(__file__).resolve().parent.parent
INDEX = BRAIN_ROOT / ".index" / "backlinks.json"
BUILD = BRAIN_ROOT / ".tools" / "build-backlinks.py"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("note", help="笔记名（不含 .md）或路径")
    ap.add_argument("--no-rebuild", action="store_true", help="跳过反链刷新，直接读现有索引")
    args = ap.parse_args()

    # 笔记名 = 去掉目录与 .md 后缀的 stem（与 build-backlinks 的 note_name 一致）
    name = Path(args.note).stem

    if not args.no_rebuild:
        if BUILD.exists():
            print("🔄 刷新反链索引 …")
            try:
                subprocess.run([sys.executable, str(BUILD)], check=True,
                               capture_output=True, text=True)
            except subprocess.CalledProcessError as e:
                print(f"⚠️  反链刷新失败（继续读旧索引）：{e.stderr or e}")
        else:
            print(f"⚠️  找不到 {BUILD}，直接读现有索引")

    if not INDEX.exists():
        print(f"❌ 索引不存在：{INDEX}\n   先跑：python3 {BUILD}")
        sys.exit(1)

    data = json.loads(INDEX.read_text(encoding="utf-8"))
    entry = data.get(name)

    print(f"\n🔗 级联复查 · [[{name}]]")
    print("=" * 48)

    if not entry or not entry.get("incoming"):
        print("✅ 无入链：没有笔记用 [[..]] 引用它，本次改动无已知级联影响。")
        print("   （注意：散文里未加双链的引用抓不到，仍需肉眼扫一遍。）")
        return

    incoming = entry["incoming"]
    print(f"⚠️  有 {len(incoming)} 处引用它，逐条判断是否需要随本次改动同步：\n")
    for i, src in enumerate(incoming, 1):
        print(f"  {i}. {src}")
    print("\n👉 复查清单：上面每个文件里凡提到 "
          f"[[{name}]] 的论断，确认是否仍成立 / 需不需要跟改。")
    print("   边界：只覆盖 [[wikilink]] 依赖，散文裸引用需另行肉眼扫。")


if __name__ == "__main__":
    main()
