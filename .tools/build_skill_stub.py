#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成账号技能的薄壳上传包：frontmatter 与 canonical 相同，正文只指向 canonical。
用法: python3 build_skill_stub.py <技能名> [输出目录]
回退: 上传 brain/.skills/<技能名>.skill（完整版）。
"""
import os, sys, zipfile

BODY = """
<!-- skill-stub: 正文真源在 brain/.skills，勿在此写正文 -->

# {name}（薄壳）

本文件不含流程。先读正文，再严格按正文执行，不要凭记忆或本文件的描述行事。

1. 按顺序找第一个存在的正文文件，用能读到本机 Mac 文件的工具读取（有 `device_bash` 时用它 `cat`，云端容器内的 Read 读不到 Mac）：
   - `~/Documents/Claude/brain/.skills/{name}/SKILL.md`
   - `$HOME/mnt/Documents/Claude/brain/.skills/{name}/SKILL.md`
   - `$HOME/mnt/Brain/.skills/{name}/SKILL.md`
   - `$HOME/mnt/brain/.skills/{name}/SKILL.md`
2. 读到后，正文的路径若写 `~/Documents/...` 而本环境不存在，换成上一步实际命中的根目录。
3. 全部读不到：报告「技能正文不可达：{name}」并列出已试路径，然后停止，不要凭记忆执行。
"""


def main():
    name = sys.argv[1]
    brain = os.path.expanduser("~/Documents/Claude/brain")
    out = sys.argv[2] if len(sys.argv) > 2 else os.path.expanduser("~/Documents/Claude/临时文件/skill-stub")
    text = open(f"{brain}/.skills/{name}/SKILL.md", encoding="utf-8").read()
    end = text.find("\n---", 3)
    if not text.startswith("---") or end == -1:
        sys.exit(f"{name}: canonical 没有 frontmatter")
    stub = text[:end + 4] + "\n" + BODY.format(name=name)
    os.makedirs(out, exist_ok=True)
    path = os.path.join(out, f"{name}.zip")
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr(f"{name}/SKILL.md", stub)
    print(path)


if __name__ == "__main__":
    main()
