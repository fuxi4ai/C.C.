#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""经验索引生成器 v2——从 GOTCHAS/通用教训/经验库 扫描生成薄索引（非事实源 · 可重建 · 幂等）。
v2（2026-09-03 独立审查修复）：①覆盖 4 种条目格式（H2/H3/列表粗体/表格）；②纳入经验库 EXP 条目；③字段扩至 9 项。
用法:
  python3 build_experience_index.py          # Mac 终端（DOCS_DIR 默认 ~/Documents）
  DOCS_DIR=/sessions/xxx/mnt/Documents python3 build_experience_index.py   # 沙箱
产物: brain/permanent/经验索引.md + brain/permanent/_exchange_index.md
原则: 索引只含指针与状态摘要，正文真源=各项目 GOTCHAS.md / 通用教训.md / 经验库.md；索引可随时重建。
"""
import os, re, hashlib, datetime

DOCS = os.environ.get("DOCS_DIR") or os.path.expanduser("~/Documents")
BRAIN = os.path.join(DOCS, "Claude/brain")
PERM = os.path.join(BRAIN, "permanent")
OUT = os.path.join(PERM, "经验索引.md")
EXCH = os.path.join(PERM, "_exchange_index.md")

MACHINE_GATES = [
    "Database/行业研究/rules/kg_promote.py",
    "Database/行业研究/rules/check_desc_shrink.py",
    "Database/行业研究/rules/bare_alias_check.py",
    "Database/行业研究/rules/check_id_consistency.py",
    "Database/行业研究/rules/name_code_consistency_check.py",
    "Database/行业研究/consumers/龙鱼五力/check_ds_evidence.py",
    "Database/行业研究/consumers/龙鱼五力/test_check_ds_evidence.py",
]

TYPE_MAP = [("ERR", "故障"), ("BUG", "缺陷"), ("RISK", "风险"), ("INFRA", "设施"),
            ("FIX", "修复"), ("NOTE", "观察"), ("NAMING", "命名"), ("GOTCHA", "坑"),
            ("EXP", "经验"), ("G-", "教训"), ("G-X", "教训")]

def sha256(p):
    try:
        return hashlib.sha256(open(p, "rb").read()).hexdigest()[:16]
    except Exception:
        return "MISSING"

def status_of(body, title=""):
    """状态行 → 标题内嵌（白泽等格式·🔄 在 ✅ 前按出现序） → 正文头部窗口。"""
    m = re.search(r"\*\*状态\*\*:?\s*([^\n*]+)", body)
    if m:
        s = m.group(1)
    elif title:
        s = title
    else:
        s = body[:600]
    for mark in ("🔄", "⚠", "✅", "⏳"):
        if mark in s:
            return mark
    return "—"

def type_of(eid):
    for pre, t in TYPE_MAP:
        if eid.startswith(pre):
            return t
    return "其他"

def date_of(eid):
    m = re.search(r"(20\d{2})[.-]?(\d{2})[.-]?(\d{2})", eid)
    return m.group(1) + "-" + m.group(2) + "-" + m.group(3) if m else "—"

def machine_hint(body):
    return bool(re.search(r"(check_desc_shrink|bare_alias_check|kg_promote|kg_merge_safe|check_ds_evidence|第1[0-9]项|负向测试|断言|校验脚本|门禁|守卫|guard)", body))

entries = []

def add(proj, eid, title, body, fname):
    if "YYYYMMDD" in eid or "NNN" in eid:
        return
    entries.append({
        "proj": proj, "id": eid, "title": title.replace("|", "｜")[:64],
        "type": type_of(eid), "date": date_of(eid), "status": status_of(body, title),
        "mach": "✓" if machine_hint(body) else "-",
        "ptr": fname, "xside": "-", "body": body,
    })

def seg_until(txt, start, marker):
    body = txt[start:]
    nxt = re.search(marker, body, re.M)
    return body[:nxt.start()] if nxt else body

# 1) 各项目 GOTCHAS：H2 格式（渊图/烛照九阴/龙鱼五力/风险日报等）
for d in sorted(os.listdir(BRAIN)):
    p = os.path.join(BRAIN, d, "GOTCHAS.md")
    if not os.path.isfile(p):
        continue
    txt = open(p, encoding="utf-8").read()
    for m in re.finditer(r"^## \[([^\]]+)\]\s*(.*)$", txt, re.M):
        add(d, m.group(1), m.group(2).strip(), seg_until(txt, m.end(), r"^## \["), f"{d}/GOTCHAS.md")
    # H3 格式（剑酒青丘）
    for m in re.finditer(r"^### \[([^\]]+)\]\s*(.*)$", txt, re.M):
        add(d, m.group(1), m.group(2).strip(), seg_until(txt, m.end(), r"^### \[|^## \[|^## "), f"{d}/GOTCHAS.md")
    # 列表粗体格式（白泽大宗 G-01 等）
    for m in re.finditer(r"^- \*\*(G-\d+)\s+(.*?)\*\*", txt, re.M):
        add(d, m.group(1), m.group(2).strip(), seg_until(txt, m.end(), r"^- \*\*G-\d+|^## |^# "), f"{d}/GOTCHAS.md")
    # 表格索引格式（PEC G-01~G-14 全表索引行）
    for m in re.finditer(r"^\|\s*(G-\d+)\s*\|\s*([^|]+)\|\s*([^|]+)\|", txt, re.M):
        add(d, m.group(1), m.group(2).strip(), "", f"{d}/GOTCHAS.md 全表索引（正文在 Projects/PEC/GOTCHAS.md）")

# 2) 通用教训（粗体 G-X 行）
gl = os.path.join(PERM, "通用教训.md")
if os.path.isfile(gl):
    gl_txt = open(gl, encoding="utf-8").read()
    for m in re.finditer(r"^\*\*(G-X\d+)\s+(.*?)\*\*", gl_txt, re.M):
        add("通用教训", m.group(1), m.group(2).strip(), gl_txt[m.end():m.end()+1500], "permanent/通用教训.md")

# 3) 经验库 EXP（H3 · cases/patterns 分节）
exp = os.path.join(PERM, "经验库.md")
if os.path.isfile(exp):
    exp_txt = open(exp, encoding="utf-8").read()
    cur_sect = "经验库"
    for m in re.finditer(r"^## (cases|patterns)[^\n]*|^### \[(EXP-[^\]]+)\]\s*(.*)$", exp_txt, re.M):
        if m.group(1):
            cur_sect = m.group(1)
        else:
            add(f"经验库·{cur_sect}", m.group(2), m.group(3).strip(),
                seg_until(exp_txt, m.end(), r"^### \[|^## "), "permanent/经验库.md")

by_proj = {}
for e in entries:
    by_proj.setdefault(e["proj"], []).append(e)

now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
lines = [
    "# 经验索引（薄索引 · 非事实源 · 可重建 · v2）",
    "",
    f"> 生成：{now} · 生成器 brain/.tools/build_experience_index.py（v2）· 重跑幂等",
    "> 字段 9 项：条目ID · 类型 · 日期 · 状态 · 机器化 · 标题 · 证据指针 · 来源主体（节头） · 对侧状态（- 未见 / ⚑已预警 / ✓已复验）。",
    "> 状态闭集：✅已修复/已沉淀 · 🔄待修复/已修待验 · ⚠已知风险 · ⏳旧状态词 · —未标。触发条件=标题摘要；正文按指针取。",
    "> 覆盖：各项目 GOTCHAS（H2/H3/列表粗体/表格四格式）+ 通用教训 + 经验库 EXP。",
    "",
    f"## 总览（{len(entries)} 条 · {len(by_proj)} 个来源）",
    "",
]
for proj in sorted(by_proj):
    es = by_proj[proj]
    n_open = sum(1 for e in es if e["status"] in ("🔄", "⚠", "⏳"))
    lines.append(f"- {proj}: {len(es)} 条（开放 {n_open}）")
for proj in sorted(by_proj):
    lines.append(f"\n## {proj}")
    for e in by_proj[proj]:
        lines.append(f"- `{e['id']}` · {e['type']} · {e['date']} · {e['status']} · 闸{e['mach']} · {e['title'][:56]} · → {e['ptr']} · 对侧{e['xside']}")
open(OUT, "w", encoding="utf-8").write("\n".join(lines) + "\n")

GATES_META = {
    "Database/行业研究/rules/kg_promote.py": {
        "replay": "python3 rules/kg_promote.py <candidate> <base>（参数以 --help 为准）",
        "expect": "一键门全过：丢失 0/第 12 项 0%/双空 0/边 schema PASS/三元组 0",
        "last_run": "2026-09-01 渊图入库场（日志实据·全绿）", "note": "用法未在本场实跑·复验方首跑时核 --help"},
    "Database/行业研究/rules/check_desc_shrink.py": {
        "replay": "python3 rules/check_desc_shrink.py <base> <candidate>（参数以 --help 为准）",
        "expect": "exit 0 = 无 desc 缩减；对未修 _v2 报出 15 处、对 canonical 报 0",
        "last_run": "2026-09-01 渊图 QA 场（日志实据）", "note": "用法未在本场实跑"},
    "Database/行业研究/rules/bare_alias_check.py": {
        "replay": "python3 rules/bare_alias_check.py（参数以 --help 为准）",
        "expect": "大小写重复/裸简称/近名兄弟簇清单；无新增违例",
        "last_run": "2026-08 渊图入库 QA（日志实据）", "note": "用法未在本场实跑"},
    "Database/行业研究/rules/check_id_consistency.py": {
        "replay": "python3 rules/check_id_consistency.py（参数以 --help 为准）",
        "expect": "id 一致性 exit 0（187 条年份警告系存量噪音）",
        "last_run": "2026-08-25 渊图批（日志实据）", "note": "用法未在本场实跑"},
    "Database/行业研究/rules/name_code_consistency_check.py": {
        "replay": "python3 rules/name_code_consistency_check.py（参数以 --help 为准）",
        "expect": "name↔code 无告警",
        "last_run": "2026-09-01 渊图批（日志实据）", "note": "用法未在本场实跑"},
    "Database/行业研究/consumers/龙鱼五力/check_ds_evidence.py": {
        "replay": "python3 check_ds_evidence.py --date 2026-08-29",
        "expect": "有 ⚠ 即 exit 1（设计）；输出三档计数+锚出处",
        "last_run": "2026-09-03 本场实跑（109 只 · ⚠69）"},
    "Database/行业研究/consumers/龙鱼五力/test_check_ds_evidence.py": {
        "replay": "python3 test_check_ds_evidence.py",
        "expect": "5/5 PASS · exit 0",
        "last_run": "2026-09-03 本场 subagent 独立验收实跑（5/5 PASS）"},
}

ex = [
    "# CC 侧经验对侧索引（薄 · 供 VV 只读 · 可重建 · 非事实源）",
    "",
    f"> 生成：{now} · 生成器 brain/.tools/build_experience_index.py（v2）",
    "> 正文真源在 CC 侧 canonical（brain/ 各项目 GOTCHAS.md + permanent/通用教训.md + permanent/经验库.md），本文件只含定位指针，供跨系统预警与复验。",
    "",
    f"## 摘要（{len(entries)} 条）",
    "结构与 permanent/经验索引.md 相同（对侧对 brain 只读可直取）。",
    "",
    "## 机器闸清单（六字段：路径/SHA/可见性/重放命令/预期通过/最近运行）",
    "",
    "> 可见性统一为「Doctor 侧路径 · VV 可见范围外」——复验需经 Doctor 转达或受控镜像（正文不复制，保持 canonical 唯一）。",
    "",
]
for g in GATES_META:
    m = GATES_META[g]
    ex.append(f"- {g}")
    ex.append(f"  - sha256[:16]={sha256(os.path.join(DOCS, g))}")
    ex.append(f"  - 可见性: Doctor 侧路径 · VV 可见范围外")
    ex.append(f"  - 重放: {m['replay']}")
    ex.append(f"  - 预期通过: {m['expect']}")
    ex.append(f"  - 最近运行: {m['last_run']}" + (f" · ⚠{m['note']}" if m.get("note") else ""))
ex += [
    "",
    "## 对侧状态约定",
    "- 未见（默认 -） / ⚑已预警 / ✓已复验",
    "- 复验须带：命令 + 关键输出摘录 + 复验日期，回填至本地索引对应条目行（对侧列）。",
]
open(EXCH, "w", encoding="utf-8").write("\n".join(ex) + "\n")

print(f"本地索引：{OUT}（{len(entries)} 条）")
print(f"对侧索引：{EXCH}")
