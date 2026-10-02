#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_edit_context.py — 改动上下文回扫器（damper 族 1 的机械面）

【治什么】
改完一处之后，**同一结论常常以另一形态活在别处**（换措辞 / 换栏位 / 换节 / 换视角）。
按「改了的那句话」去搜，搜不到变体；而「回扫该处所在段落」原先只是一条纪律——纪律拦不住。
本工具把它做成一个能跑的扫。

【它做什么】
1) 与快照 diff，算出**改动点**（新增/删除/替换的行）；
2) 对每个改动点，展开它的**所在段落**（连续非空块），或它的**整个表格行 / 列表项**；
3) 从改动块里抽出**关键串**（「」『』内的引文、**加粗**、`反引号`），
   在全文件搜这些串 —— **凡出现在「本次未改的行」上的，全部报出**（这就是「别处还活着几处」）；
4) 在展开段落内标出**断言线索行**：全称/量词词表 · 计数数字 · 点名单 · 交叉引用（:NNN / 文件:行号）。

【它明确不做】（别指望它替你做判断）
- **不判真伪**：它只把候选摊到你眼前。数字对不对、全称句成不成立、两处是否真的相抵 —— 全都得你自己读。
- **不判语义**：换措辞活着的旧文，它**搜不到**（那正需要人读；它只能靠第 3 步的引文/加粗串捞到一部分）。
- **不改文件**：纯只读。
- **不认识你的段落语义**：它按「连续非空行」切块，markdown 的复杂嵌套（表格内换行等）会切得不准。

【效力分级】**提示器，非闸**（同 scope_guard.sh）。不跑等于零。

用法
----
    # 推荐：配合 scope_guard.sh 的快照
    brain/.tools/scope_guard.sh snap 目标文件.md fixA     # 改之前
    ...改...
    python3 brain/.tools/check_edit_context.py 目标文件.md --snap 目标文件.md.fixA.bak

    # 无快照时：只做全文关键串扫描（无「改动点」信息，价值较低）
    python3 brain/.tools/check_edit_context.py 目标文件.md

    # 只看某一段落（手工指定范围）
    python3 brain/.tools/check_edit_context.py 目标文件.md --lines 100-140

    # 自检
    python3 brain/.tools/check_edit_context.py --self-test
"""

import argparse
import difflib
import pathlib
import re
import sys
import tempfile
import unittest

# ---- 词表（可扩）-------------------------------------------------------------
QUANTIFIERS = [
    "全部", "所有", "一切", "任何", "无一", "无一句", "都", "每", "各",
    "唯一", "仅", "恰好", "至少", "至多", "最多", "最少", "永远", "从不", "从不",
    "零", "没有一", "无一例", "一律", "毫无", "首个", "首次", "第一", "最大", "最小",
    "最高", "最低", "最常见", "最高频", "最爱", "绝大多数",
]

# 行内豁免标记：判定该处「该留」之后，把标记写进那一行，回扫便不再重复报它。
# 用法：在行末写 <!-- rescan-ok: 理由 -->
RESCAN_OK = "rescan-ok"
POINT_LISTS = re.compile(r"(第\s*[一二三四五六七八九十\d]+\s*[项条点处]|后两项|前三项|①②③④⑤|前两处|其余\d+处)")
XREF = re.compile(r"(?::\d{1,5}\b|[\w\-./]+\.(?:md|py|sh|json|tsv|plist):\d+)")
NUMERIC = re.compile(r"\d")
KEY_STRINGS = [
    re.compile(r"「([^」\n]{2,80})」"),
    re.compile(r"『([^』\n]{2,80})』"),
    re.compile(r"\*\*([^*\n]{2,80})\*\*"),
    re.compile(r"`([^`\n]{2,80})`"),
]
TRIVIAL = {",", "。", "：", "、", "）", "（", "-", "—", "|", "*", "**", "**\n"}


def read_lines(path):
    return pathlib.Path(path).read_text(encoding="utf-8", errors="replace").split("\n")


def changed_blocks(old_lines, new_lines):
    """返回改动点的 (起, 止) 闭区间列表（1-based，指向 new 的索引）。纯增/纯删都算。"""
    sm = difflib.SequenceMatcher(None, old_lines, new_lines, autojunk=False)
    blocks = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            continue
        if j2 > j1:                      # 新版里有内容的，取新版范围
            blocks.append((j1 + 1, j2))
        else:                            # 纯删除：挂在删除点前的行上
            blocks.append((max(j1, 1), max(j1, 1)))
    return blocks


def expand_paragraph(lines, start, end):
    """从改动点向上/向下扩到空行边界（连续非空块）；至少包含改动点自身。"""
    i = start - 1
    j = end - 1
    while i > 0 and lines[i - 1].strip():
        i -= 1
    while j < len(lines) - 1 and lines[j + 1].strip():
        j += 1
    return i + 1, j + 1


def extract_keys(text):
    keys = []
    for rx in KEY_STRINGS:
        for m in rx.finditer(text):
            s = m.group(1).strip()
            if len(s) >= 2 and s not in TRIVIAL:
                keys.append(s)
    # 去重保序；去掉被他串包含的短串（减少噪声）
    seen, out = set(), []
    for k in keys:
        if k in seen:
            continue
        seen.add(k)
        out.append(k)
    out = [k for k in out if not any(k != o and k in o for o in out)]
    return out


def flag_reason(line):
    """给一行判「它是不是断言线索行」，返回理由列表。"""
    why = []
    for q in QUANTIFIERS:
        if q in line:
            why.append(f"全称/量词「{q}」")
    if POINT_LISTS.search(line):
        why.append("点名单")
    if XREF.search(line):
        why.append("交叉引用")
    if NUMERIC.search(line):
        why.append("含数字")
    return why


def report(path, snap=None, only_lines=None, quiet=False):
    """核心分析。返回 (退出码, 报告文本, 结构化摘要)。退出码：0=跑通(不代表无发现)；2=输入错。"""
    p = pathlib.Path(path)
    if not p.exists():
        return 2, f"✗ 文件不存在：{path}\n", {}
    new_lines = read_lines(p)
    out = []

    if only_lines:
        a, b = only_lines
        blocks = [(a, b)]
        mode = f"手工指定行 {a}-{b}"
    elif snap:
        sp = pathlib.Path(snap)
        if not sp.exists():
            return 2, f"✗ 快照不存在：{snap}\n", {}
        old_lines = read_lines(sp)
        blocks = changed_blocks(old_lines, new_lines)
        mode = f"与快照 diff（快照 {sp.name}）"
    else:
        blocks = []
        mode = "无快照 · 仅全文关键串扫描"

    out.append(f"══ check_edit_context · {p.name}（{len(new_lines)} 行）══")
    out.append(f"模式：{mode}")

    if blocks:
        out.append(f"改动点：{len(blocks)} 处 → " + "、".join(f"L{a}" if a == b else f"L{a}-{b}" for a, b in blocks))
    else:
        out.append("改动点：无（未提供快照或未指定 --lines）")

    changed_line_set = set()
    for a, b in blocks:
        changed_line_set.update(range(a, b + 1))

    # ── ① 段落展开 ─────────────────────────────────────────────────────────
    if blocks:
        out.append("\n── ① 所在段落（回扫范围＝这里，不只是改动那几行）──")
        regions = []
        for a, b in blocks:
            ra, rb = expand_paragraph(new_lines, a, b)
            regions.append((ra, rb))
        # 合并重叠区间
        merged = []
        for ra, rb in sorted(regions):
            if merged and ra <= merged[-1][1] + 1:
                merged[-1] = (merged[-1][0], max(merged[-1][1], rb))
            else:
                merged.append((ra, rb))
        for ra, rb in merged:
            out.append(f"\n  ▸ 段落 L{ra}-{rb}")
            for n in range(ra, rb + 1):
                mark = "改" if n in changed_line_set else "  "
                why = flag_reason(new_lines[n - 1]) if new_lines[n - 1].strip() else []
                tag = f" ⚑{'/'.join(why)}" if why and n not in changed_line_set else ""
                out.append(f"    {n:>4} [{mark}] {new_lines[n-1][:150]}{tag}")

    # ── ② 关键串在别处还活着几处（族 1 的机械面）──────────────────────────
    out.append("\n── ② 本次改动的关键串，在「未改的行」上还剩几处 ──")
    key_text = "\n".join(new_lines[n - 1] for n in sorted(changed_line_set) if n <= len(new_lines)) \
        if changed_line_set else "\n".join(new_lines)
    keys = extract_keys(key_text)
    if not keys:
        out.append("  （没抽到引文/加粗/反引号串 ⇒ 本步无料。不代表性 1 无风险——换措辞的变体它搜不到。）")
    residues = 0
    exempted_total = 0
    for k in keys:
        hits = [n for n, ln in enumerate(new_lines, 1)
                if k in ln and n not in changed_line_set and RESCAN_OK not in ln]
        exempt = [n for n, ln in enumerate(new_lines, 1)
                  if k in ln and n not in changed_line_set and RESCAN_OK in ln]
        residues += len(hits)
        exempted_total += len(exempt)
        if hits:
            shown = "、".join(f"L{n}" for n in hits[:6]) + ("…" if len(hits) > 6 else "")
            out.append(f"  ⚠ 「{k}」→ 未改的行上还有 {len(hits)} 处（{shown}）")
            for n in hits[:3]:
                out.append(f"        L{n}: {new_lines[n-1].strip()[:130]}")
            if exempt:
                out.append(f"      ·同串另有 {len(exempt)} 处已豁免（{'、'.join('L'+str(n) for n in exempt[:6])}）")
        elif exempt:
            out.append(f"  · 「{k}」别处 {len(exempt)} 处已豁免（{'、'.join('L'+str(n) for n in exempt[:6])}）")
    if keys and residues == 0:
        out.append(f"  ✓ 抽到的 {len(keys)} 个关键串，在未改且未豁免的行上零残留（**这不等于安全**：换措辞的变体搜不到）")

    # ── ③ 段落内的断言线索（未改行上的）──────────────────────────────────
    if blocks:
        out.append("\n── ③ 段落内「未改但含断言线索」的行（要人读）──")
        n_hit = 0
        for n in sorted(changed_line_set):
            pass
        scan_set = set()
        for ra, rb in merged:
            scan_set.update(range(ra, rb + 1))
        for n in sorted(scan_set - changed_line_set):
            ln = new_lines[n - 1]
            if not ln.strip():
                continue
            why = flag_reason(ln)
            if why:
                n_hit += 1
                out.append(f"  · L{n} [{'/'.join(why)}]  {ln.strip()[:130]}")
        if n_hit == 0:
            out.append("  ✓ 段落内未改行无断言线索")

    # ── ④ 回扫清单 ────────────────────────────────────────────────────────
    out.append("""
── ④ 回扫清单（机器到此为止，以下要人做）──
  □ ①段落里那些「未改但含线索」的行，逐行问：它跟我这次改的结论是同一件事吗？是 ⇒ 同族未回扫
  □ ②列出的残留处，逐处问：它是**该留的**（历史留痕/引文/另一主题）还是**该改的**？
      判「该留」⇒ 在那行末写 <!-- rescan-ok: 理由 -->，此后回扫不再重复报它（**别静默放过，要留下判定**）
  □ ③本次改动让**哪些先前报过的数**过期了？（族 3）
  □ ④我新写的话里有**全称/量词/点名单**吗？反证过了吗？（族 2）
  □ ⑤如果这是替换操作：`new_string` 里有没有**混进不属于此处的内容**？（族 8）
  □ ⑥报告里要不要加「未申报改动」栏？（族 7）""")

    return 0, "\n".join(out) + "\n", {
        "blocks": blocks,
        "keys": keys,
        "residues": residues,
        "exempted": exempted_total,
    }


# ── 自检 ──────────────────────────────────────────────────────────────────────
class SelfTest(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.TemporaryDirectory()
        self.p = pathlib.Path(self.d.name) / "t.md"

    def tearDown(self):
        self.d.cleanup()

    def _run(self, snap_text, new_text, **kw):
        if snap_text is not None:
            s = pathlib.Path(self.d.name) / "t.md.bak"
            s.write_text(snap_text, encoding="utf-8")
            kw["snap"] = str(s)
        self.p.write_text(new_text, encoding="utf-8")
        return report(str(self.p), **kw)

    # P 组（正向：应当报出）
    def test_P1_residue_same_string_elsewhere(self):
        """★ 核心用例：改了 A 处的引文串，B 处同串未改 ⇒ 必须报残留"""
        rc, txt, s = self._run("「甲结论」在 A。\n\n「甲结论」也在 B。\n", "「甲结论」在 A（已订正）。\n\n「甲结论」也在 B。\n")
        self.assertEqual(rc, 0)
        self.assertGreaterEqual(s["residues"], 1, "同串残留未报出")
        self.assertIn("未改的行上还有", txt)

    P1 = test_P1_residue_same_string_elsewhere

    def test_P2_quantifier_flagged_in_unmodified_line(self):
        """段落内未改行的全称/量词应被标出"""
        rc, txt, s = self._run("第一行。\n\n本仓全部条目均已核。\n这次我改了这句。\n", "第一行。\n\n本仓全部条目均已核。\n这次我改了这句话。\n")
        self.assertEqual(rc, 0)
        self.assertIn("全称/量词", txt)

    def test_P3_blocks_reported(self):
        rc, txt, s = self._run("a\nb\nc\n", "a\nB\nc\n")
        self.assertEqual(rc, 0)
        self.assertGreaterEqual(len(s["blocks"]), 1)

    def test_P4_lines_mode(self):
        self.p.write_text("x\n「子串」\n「子串」\n", encoding="utf-8")
        rc, txt, s = report(str(self.p), only_lines=(2, 2))
        self.assertEqual(rc, 0)
        self.assertIn("手工指定行", txt)

    # N 组（负向：应当不报）
    def test_N1_no_residue_when_unique(self):
        """改动串在别处不存在 ⇒ residues 必须为 0（防假阳性）"""
        rc, txt, s = self._run("「独此一处」在 A。\n", "「独此一处」在 A（已订正）。\n")
        self.assertEqual(s["residues"], 0, "不该报残留却报了")

    def test_N2_missing_file(self):
        rc, txt, _ = report(str(pathlib.Path(self.d.name) / "nope.md"))
        self.assertEqual(rc, 2)

    def test_N3_missing_snap(self):
        self.p.write_text("x\n", encoding="utf-8")
        rc, txt, _ = report(str(self.p), snap=str(pathlib.Path(self.d.name) / "nope.bak"))
        self.assertEqual(rc, 2)

    def test_N4_no_blocks_without_snap(self):
        """无快照 ⇒ 不得凭空造出改动点"""
        self.p.write_text("甲\n乙\n", encoding="utf-8")
        rc, txt, s = report(str(self.p))
        self.assertEqual(rc, 0)
        self.assertEqual(s["blocks"], [])

    def test_N5_key_strings_ignore_trivial(self):
        self.assertEqual(extract_keys("「」 ** ``"), [])

    def test_N6_identical_files_no_blocks(self):
        rc, txt, s = self._run("a\nb\n", "a\nb\n")
        self.assertEqual(s["blocks"], [])

    def test_P5_rescan_ok_exempts(self):
        """标了 rescan-ok 的残留不应再报（防回扫退化为每轮重读全库）。
        真实用法＝**先在那一行标好标记、之后再改别处**；故标记须在快照里就在。"""
        marked = "「甲乙」在 B。<!-- rescan-ok: 另一主题 -->\n"
        rc, txt, s = self._run("「甲乙」在 A。\n\n" + marked, "「甲乙」在 A（改）。\n\n" + marked)
        self.assertEqual(s["residues"], 0, "豁免行仍被计入残留")
        self.assertIn("已豁免", txt)

    def test_N7_exempt_only_applies_to_marked_line(self):
        """豁免只作用于标了的那一行；同串别处未标 ⇒ 仍须报"""
        marked = "「甲乙」在 B。<!-- rescan-ok: 留痕 -->\n"
        rc, txt, s = self._run("「甲乙」在 A。\n\n" + marked + "\n「甲乙」在 C。\n",
                               "「甲乙」在 A（改）。\n\n" + marked + "\n「甲乙」在 C。\n")
        self.assertGreaterEqual(s["residues"], 1, "未标的残留被一并豁免了")

    def test_N8_short_key_not_extracted(self):
        """长度 <2 的引文串按设计不抽（防噪声）——本用例锁住这个行为"""
        self.assertEqual(extract_keys("「串」在 A。"), [])
        self.assertNotEqual(extract_keys("「甲乙」在 A。"), [])

    def test_P6_summary_and_print_agree(self):
        """★ 摘要里的 residues 与打印文本必须同号。
        本工具自己犯过一次：两处各算一次、其中一处漏了豁免过滤
        ⇒ 打印说「零残留」而摘要报 1。此用例锁死该形态。"""
        marked = "「甲乙」在 B。<!-- rescan-ok: 留痕 -->\n"
        rc, txtA, sA = self._run("「甲乙」在 A。\n\n" + marked, "「甲乙」在 A（改）。\n\n" + marked)
        self.assertEqual(sA["residues"], 0)
        self.assertIn("零残留", txtA)

        self.p.write_text("「甲乙」在 A（改）。\n\n" + marked + "\n「甲乙」在 C。\n", encoding="utf-8")
        sn = pathlib.Path(self.d.name) / "t.md.bak"
        sn.write_text("「甲乙」在 A。\n\n" + marked + "\n「甲乙」在 C。\n", encoding="utf-8")
        rc, txtB, sB = report(str(self.p), snap=str(sn))
        self.assertGreater(sB["residues"], 0)
        self.assertNotIn("零残留", txtB, "residues>0 却打印了「零残留」")


def _self_test():
    """入口级自检（G-X188）：把 CLI 当子进程跑、断言退出码，而非只跑内部函数。"""
    import os
    import subprocess
    good = pathlib.Path(tempfile.mkdtemp(prefix="cec_self_"))
    f = good / "ok.md"
    f.write_text("甲\n乙\n", encoding="utf-8")           # 无快照 ⇒ rc 应为 0
    args = [sys.executable, __file__, str(f)]
    env = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}
    cases = [
        (0, args, "正常文件（无快照）应为 rc=0"),
        (2, [sys.executable, __file__], "缺参数应为 rc=2"),
        (2, [sys.executable, __file__, str(good / "nope.md")], "文件不存在应为 rc=2"),
        (2, [sys.executable, __file__, str(f), "--lines", "abc"], "非法 --lines 应为 rc=2"),
    ]
    fails = []
    for want, cmd, desc in cases:
        r = subprocess.run(cmd, capture_output=True, text=True, env=env)
        if r.returncode != want:
            fails.append(f"  ✗ {desc}：期望 rc={want}，实得 rc={r.returncode}")
    # 内部用例
    suite = unittest.TestLoader().loadTestsFromTestCase(SelfTest)
    res = unittest.TextTestRunner(verbosity=2).run(suite)
    ok = not fails and res.wasSuccessful()
    for x in fails:
        print(x)
    print(f"\n入口级 {len(cases) - len(fails)}/{len(cases)} 通过 · 内部用例 {res.testsRun - len(res.failures) - len(res.errors)}/{res.testsRun} 通过")
    print("SELF-TEST OK" if ok else "SELF-TEST FAILED")
    return 0 if ok else 1


def main(argv=None):
    ap = argparse.ArgumentParser(description="改动上下文回扫器（damper 族 1 的机械面）")
    ap.add_argument("path", nargs="?", help="要回扫的文件")
    ap.add_argument("--snap", help="scope_guard.sh snap 产生的 .bak 快照")
    ap.add_argument("--lines", help="手工指定范围，如 100-140")
    ap.add_argument("--self-test", action="store_true", help="跑入口级 + 内部自检")
    a = ap.parse_args(argv)

    if a.self_test:
        return _self_test()

    if not a.path:
        ap.print_help()
        return 2
    only = None
    if a.lines:
        m = re.match(r"^(\d+)-(\d+)$", a.lines.strip())
        if not m:
            print("✗ --lines 需形如 100-140", file=sys.stderr)
            return 2
        only = (int(m.group(1)), int(m.group(2)))
    rc, txt, _ = report(a.path, snap=a.snap, only_lines=only)
    sys.stdout.write(txt)
    return rc


if __name__ == "__main__":
    sys.exit(main())
