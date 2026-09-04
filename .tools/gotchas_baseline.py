#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""规则库基线统计（只读）——2026-09-03 经验系统改造第一阶段交付面④ · v2 复用经验索引解析（单一真源）。
统计: 统一分类（日志/经验/Gotcha/规则）· 三级执行等级 · 活跃数/机器化率/待验年龄/同根复发/退役候选。
长期未命中当前不可测（GOTCHAS 无命中记录），标 N/A。
用法:
  python3 gotchas_baseline.py
  DOCS_DIR=/sessions/xxx/mnt/Documents python3 gotchas_baseline.py
产物: brain/permanent/_rules_baseline_2026-09-03.md
依赖: 同目录 build_experience_index.py（import 其解析函数，避免两处格式逻辑漂移）。
"""
import os, re, datetime, sys

DOCS = os.environ.get("DOCS_DIR") or os.path.expanduser("~/Documents")
BRAIN = os.path.join(DOCS, "Claude/brain")
OUT = os.path.join(BRAIN, "permanent", "_rules_baseline_2026-09-03.md")
TODAY = datetime.date(2026, 9, 3)

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_experience_index as bi

CATEGORY = {
    "通用教训": "规则", "经验库·cases": "经验", "经验库·patterns": "经验",
}
def cat_of(e):
    if e["proj"] in CATEGORY:
        return CATEGORY[e["proj"]]
    if e["type"] in ("故障", "缺陷", "风险", "设施", "修复", "观察", "命名", "坑"):
        return "Gotcha"
    if e["type"] == "经验":
        return "经验"
    if e["type"] == "教训":
        return "规则"
    return "Gotcha"

def date_of(e):
    d = e["date"]
    if d == "—":
        return None
    try:
        return datetime.date.fromisoformat(d)
    except Exception:
        return None

def negtest_hint(e):
    return bool(re.search(r"负向测试", e["body"]))

def flow_hint(e):
    return bool(re.search(r"(skill|SKILL|步骤|回执|receipt|wrapper|调度)", e["body"]))

def exec_level(e):
    if e["mach"] == "✓":
        return "机器强制"
    if flow_hint(e):
        return "流程强制"
    return "文本指导"

def recurrence_hint(e):
    return bool(re.search(r"(同族|同根|复发|第二次|第[二三]次|追记|镜像教训)", e["body"]))

entries = [e for e in bi.entries if "body" in e]
total = len(entries)
open_rows = [e for e in entries if e["status"] in ("🔄", "⚠", "⏳")]
closed = [e for e in entries if e["status"] == "✅"]
mach = [e for e in entries if e["mach"] == "✓"]
rec = [e for e in entries if recurrence_hint(e)]
lvl = {}
for e in entries:
    lvl.setdefault(exec_level(e), []).append(e)
neg = [e for e in entries if negtest_hint(e)]
retire_cand = [e for e in closed if date_of(e) and (TODAY - date_of(e)).days > 90]
aging = sorted([e for e in open_rows if e["status"] == "🔄" and date_of(e)],
               key=lambda x: -(TODAY - date_of(x)).days)[:10]
cat_n = {}
for e in entries:
    cat_n.setdefault(cat_of(e), 0)
    cat_n[cat_of(e)] += 1

L = [
    "# 规则库基线 · 2026-09-03（第一份 · 只读统计 · 可重跑 · v2 三级执行等级口径）",
    "",
    f"> 生成器 brain/.tools/gotchas_baseline.py（解析逻辑复用 build_experience_index.py · 单一真源）· 统计范围=CC 侧 brain/ 全域（GOTCHAS 四格式 + 通用教训 + 经验库 EXP）",
    "> 注意：与 VV 侧（Codex）统计口径独立，不直接合并数字。",
    "",
    "## 统一分类（VV 收敛口径：日志/经验/Gotcha/规则）",
    "",
]
for c in ("Gotcha", "规则", "经验"):
    L.append(f"- {c}: **{cat_n.get(c, 0)}** 条")
L += [
    f"- 日志: 不入本基线（事件记录层 · 见 brain/logs/ · 月折叠机制另行管理）",
    f"- 合计: **{total}** 条",
    "",
    "## 核心数字",
    "",
    f"- 开放（🔄/⚠/⏳）: **{len(open_rows)}**（🔄 {len([e for e in open_rows if e['status']=='🔄'])} · ⚠ {len([e for e in open_rows if e['status']=='⚠'])} · ⏳ {len([e for e in open_rows if e['status']=='⏳'])}）",
    f"- 已闭环（✅）: **{len(closed)}**",
    f"- 机器化迹象: **{len(mach)}**（{len(mach)/total*100:.0f}% · 启发式口径）",
    f"- 同根复发/追记迹象条目: **{len(rec)}**",
    f"- 退役候选（✅ 且 >90 天）: **{len(retire_cand)}**",
    "",
    "## 三级执行等级分布（2026-09-03 VV 收敛口径）",
    "",
    f"- 机器强制（校验器/schema/测试/门禁 · 违反即失败）: **{len(lvl.get('机器强制', []))}**",
    f"- 流程强制（skill/wrapper/调度步骤 · 执行须留回执）: **{len(lvl.get('流程强制', []))}**",
    f"- 文本指导（依赖 agent 主动读取 · 执行概率最低）: **{len(lvl.get('文本指导', []))}**",
    f"- 其中带负向测试（机器强制的强化证据）: **{len(neg)}**",
    "",
    "## 跨系统样本（交换层第一批数据）",
    "",
    "- `CC-机器闸-7件` · 来源=CC · 路径/SHA/可见性/重放命令/预期通过/最近运行 → `permanent/_exchange_index.md` · 对侧状态=待 VV 复验",
    "- `VV-resume召回缺口` · 来源=VV（2026-09-03 自检实况复现：/resume 未检索经验库/通用教训/核心 Gotchas）· 类型=流程规则样本 · 状态=待 VV 侧实施 · CC 侧对应修复已发布（brain-resume Step 1.5/3.5 · 待消费端回读验证）",
    "",
    "## 待验年龄 TOP 10（🔄 已修待验 · 按条目 ID 日期算龄）",
    "",
    "| 项目 | 条目 | 年龄(天) | 标题 |",
    "|---|---|---|---|",
]
for e in aging:
    L.append(f"| {e['proj']} | {e['id']} | {(TODAY - date_of(e)).days} | {e['title'][:40]} |")
if not aging:
    L.append("| — | 无已修待验条目 | | |")
L += [
    "",
    "## 长期未命中",
    "",
    "N/A —— GOTCHAS 无命中记录字段；本基线暂不可测。建议后续在回执机制（_consumption_receipts.jsonl）中顺带记录条目命中，下期基线可算。",
    "",
    "## 消费端回读标记",
    "",
    "- GOTCHAS 本体无此字段；回执层 `permanent/_consumption_receipts.jsonl` 现存 1 条未闭——consumer_verified 待下一场真实 /resume",
    "",
    "## 复查建议",
    "",
    "- 复查日期: 2026-10-03（+30 天）· 复查动作=重跑本脚本 diff 对比 + 待验/退役候选现状核 · 归 Doctor 提起或并入 /todo",
    "",
    "## 退役候选清单（✅ 且 >90 天 · TOP15）",
    "",
]
for e in sorted(retire_cand, key=lambda x: -(TODAY - date_of(x)).days)[:15]:
    L.append(f"- `{e['proj']}/{e['id']}` · {(TODAY - date_of(e)).days} 天 · {e['title'][:50]}")
if not retire_cand:
    L.append("- 无")
L.append("")
L.append("> 退役动作不自动执行——触发条件/替代门禁/消费者检查后归 Doctor 裁（本基线只标候选）。")
open(OUT, "w", encoding="utf-8").write("\n".join(L))
print(f"基线报告已落：{OUT}")
print(f"总数 {total} · 分类 {cat_n} · 开放 {len(open_rows)} · 机器化 {len(mach)} · 三级 { {k: len(v) for k, v in lvl.items()} } · 负向测试 {len(neg)} · 退役候选 {len(retire_cand)}")
