#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""PEC 「已废规则串」残留扫描器 · 2026-10-02 建（承 Doctor 裁「停人肉轮次，改做机器扫残留」）

【为什么要它】
  CS-10 现行判据线连跑九/十轮独立复验，**每轮 FAIL 的都是同一条收尾判据**：
  「同源句全落点同扫」。第九轮逮 3 件漏扫、第十轮又拎出 6 条。
  根因不是"没扫"，是 **扫描面从未被枚举** —— 每轮都靠人肉想"该扫哪些地方"，
  而漏的总是同一类位置（非正文段 / 不在影响面清单里的件）。
  ⇒ 把「已废规则串 × 全库命中 × live/记录 预分类」做成**可重跑的一次性动作**。

【它怎么工作】
  ① 枚举**扫描面**（件 × 串）并**显式打印**——这一条是它的存在理由；
  ② 每个命中给**预分类**三档：`待判` / `记录·留痕` / `史层`；
  ③ **只把 `待判` 列为需处置**，另两档只计数（可 `--all` 全列）。

【边界 · 必读】
  · 它是**提示器，不是闸**：预分类是**启发式**，「待判」里必有假阳性，
    「记录」里也可能藏真残留 ⇒ **红须人核、绿不能当通过**。
  · 退出码：0＝扫完且无「待判」；1＝有「待判」；2＝配置错（fail-closed）。
  · **不判对错、不改任何文件**（只读）。

作者：CC · 2026-10-02 · 本脚本未经独立复验
"""
import argparse
import glob
import os
import re
import sys

HOST = os.environ.get("PEC_SCAN_HOST", "/Users/lunarabbit/Documents/Claude/")
if not HOST.endswith("/"):
    HOST += "/"

# ── 已废规则串（「当时是规则、现已被裁改」的字面） ────────────────────────────
# 每项：pat（字面或正则）· 废于何时 · 现行为何 · 备注
RETIRED = [
    {"pat": "五列", "since": "2026-10-01",
     "now": "四列（入场表单第 4 档「作为原因／条件出现 ❌」已随 Doctor 裁删）"},
    {"pat": r"否则\s*⇒\s*\*{0,2}候选", "since": "2026-10-01", "regex": True,
     "now": "其余情形 ⇒ 见 `2.0（五）` 二值判定表"},
    {"pat": "原因／条件出现", "since": "2026-10-01", "now": "该档已删（同上）"},
    {"pat": "原因/条件出现", "since": "2026-10-01", "now": "该档已删（同上）"},
    {"pat": "外生条件", "since": "2026-10-01",
     "now": "该档已撤 ⇒ 外生条件与其它候选同等过两门＋计数门"},
    {"pat": "移出基因序列", "since": "2026-10-01",
     "now": "先试判归属，判不出才单列"},
    {"pat": "跨文明层 ／ 集合体", "since": "2026-10-01",
     "now": "已拆成两行（与门禁 §B2「两个独立类目」对齐，共 9 类）"},
    {"pat": "2.0（七）", "since": "2026-10-01", "now": "该节不存在（2.0 止于（六））"},
]

# ── 扫描面 ──────────────────────────────────────────────────────────────────
# 现行层：PEC 项目树（排归档/备份）＋ brain 侧现行执行件
SCAN_DIRS = [
    "Projects/PEC",
    # ⚠ 用通配：月折目录会换。**首版写死 `brain/logs/2026-09/checkpoints`** ⇒ 与
    #   `check_pec_parity.py` 的 `KIT` 路径**同一种死法**（到 10 月即失明）——
    #   由 2026-10-02 未参与实施的独立复验者实跑逮出。**禁写死月份。**
    "brain/logs/*/checkpoints",
    "brain/logs/checkpoints",
    "brain/PEC",
]
SKIP_DIR_PARTS = {".git", "_bak", "archived", "__pycache__", "node_modules",
                  ".ruff_cache", "dist", ".pytest_cache"}
SKIP_SUFFIX = (".pyc", ".bak", ".png", ".jpg", ".jpeg", ".gif", ".pdf",
               ".zip", ".tar", ".gz", ".sqlite3", ".db", ".xlsx")

# 真退役层（**静默**：只计数、不逐条列 —— 这些层按纪律不追改）
HIST_PATH_RE = re.compile(r"(/|^)(archived|_bak|_DEPRECATED_)(/|$)|\.bak")

# ⚠ 2026-10-02 补（**本工具首跑自曝的同型缺陷**）：`raw/` 日期件**不算真退役层** ——
#   它们是「资料层」，**按纪律正文不追改但要挂过期指针**（本线反复栽的就是这类）。
#   首版把它们并进 HIST_PATH_RE ⇒ **静默吞掉**，而第十轮逮出的第 2 条恰恰住在
#   `raw/2026-09-26_analysis_CS05判定重跑.md`。**排除规则本身制造盲面 = 本工具要治的病。**
#   ⇒ 改为**单列一档 `资料层`，逐条列出**，不静默。
DATALAYER_PATH_RE = re.compile(r"/raw/\d{4}-\d{2}-\d{2}_")

# 「记录／留痕」行标记（命中行含任一个 ⇒ 预分类为「记录·留痕」）
RECORD_MARKERS = [
    "订正", "superseded", "过期指针", "原写", "原记", "此前", "曾", "已废",
    "历史", "记录", "来源", "复验", "审核", "审计", "勘误", "回顾", "旧文",
    "撤回", "作废", "改为", "现已", "不再", "已删", "已撤",
]


def expand_roots():
    """把 SCAN_DIRS 里含通配的项展开成真实目录（月折目录会换 ⇒ 禁写死月份）。"""
    out = []
    for d in SCAN_DIRS:
        out += sorted(glob.glob(os.path.join(HOST, d)))
    return [p for p in out if os.path.isdir(p)]


def iter_files():
    for root in expand_roots():
        for dp, dns, fns in os.walk(root):
            dns[:] = [x for x in dns if x not in SKIP_DIR_PARTS]
            if any(p in SKIP_DIR_PARTS for p in dp.split(os.sep)):
                continue
            for fn in fns:
                if fn.endswith(SKIP_SUFFIX):
                    continue
                yield os.path.join(dp, fn)


def strip_fences(lines):
    """产出 (行号, 行文本, 是否在代码围栏内)。"""
    infence = False
    for i, ln in enumerate(lines, 1):
        s = ln.lstrip()
        if s.startswith("```") or s.startswith("~~~"):
            yield i, ln, True
            infence = not infence
            continue
        yield i, ln, infence


def classify(line, hist_path, datalayer=False):
    """单行 → 预分类（scan 与 self_test 共用同一把尺）。
    顺序有意：① 真退役层静默；② 带留痕标记 → 记录；③ **资料层（raw 日期件）单列**（不静默）；④ 其余待判。
    """
    if hist_path:
        return "史层"
    if any(mk in line for mk in RECORD_MARKERS):
        return "记录·留痕"
    if datalayer:
        return "资料层·须指针"
    return "待判"


def scan(all_hits=False):
    files = list(iter_files())
    hits = []
    for path in files:
        try:
            txt = open(path, encoding="utf-8").read()
        except (UnicodeDecodeError, OSError):
            continue
        rel = os.path.relpath(path, HOST)
        hist_path = bool(HIST_PATH_RE.search("/" + rel))
        datalayer = bool(DATALAYER_PATH_RE.search("/" + rel))
        for no, line, infence in strip_fences(txt.splitlines()):
            if infence:
                continue
            for r in RETIRED:
                if r.get("regex"):
                    ok = re.search(r["pat"], line) is not None
                else:
                    ok = r["pat"] in line
                if not ok:
                    continue
                hits.append({"file": rel, "line": no, "pat": r["pat"],
                             "since": r["since"], "now": r["now"],
                             "klass": classify(line, hist_path, datalayer),
                             "text": line.strip()[:160]})
    return files, hits


def report(files, hits, all_hits=False):
    pend = [h for h in hits if h["klass"] == "待判"]
    dat = [h for h in hits if h["klass"] == "资料层·须指针"]
    rec = [h for h in hits if h["klass"] == "记录·留痕"]
    hist = [h for h in hits if h["klass"] == "史层"]
    print("═" * 78)
    print("PEC 已废规则串残留扫描 —— 提示器（非闸）")
    print("═" * 78)
    print(f"【扫描面】件 {len(files)} · 串 {len(RETIRED)} · 组合 {len(files) * len(RETIRED)}")
    for d in SCAN_DIRS:
        print(f"    · {d}")
    print(f"【命中】{len(hits)} 处 —— 待判 {len(pend)} · 资料层·须指针 {len(dat)}"
          f" · 记录·留痕 {len(rec)} · 史层 {len(hist)}")
    for tag, group, note in (
            ("待判", pend, "逐处判「live 断言该补指针」还是「其实合规」"),
            ("资料层·须指针", dat, "资料层（raw 日期件）—— 正文不追改，但**应挂过期指针**")):
        if not group:
            continue
        print()
        print(f"▼ {tag}（{len(group)} 处）—— {note}")
        cur = None
        for h in group:
            if h["file"] != cur:
                cur = h["file"]
                print(f"\n  ▸ {cur}")
            print(f"    :{h['line']}  「{h['pat']}」→ 现行：{h['now']}")
            print(f"           {h['text']}")
    if all_hits:
        for tag, group in (("记录·留痕", rec), ("史层", hist)):
            if not group:
                continue
            print(f"\n▼ {tag}（{len(group)} 处 · 仅列路径:行）")
            for h in group:
                print(f"    {h['file']}:{h['line']}  「{h['pat']}」")
    print()
    print("⚠ 预分类是启发式的：'待判' 里必有假阳性，'记录' 里也可能藏真残留 —— 红须人核、绿不能当通过。")
    return 1 if (pend or dat) else 0


def self_test():
    """负向自检三式：① 围栏内不入判 · ② 直述→待判 / 带留痕→记录 · ③ 史层路径正反例 · ④ 正则型串。"""
    import shutil
    import tempfile
    ok = True

    body = ("```\n五列（围栏内，不该被扫）\n```\n"
            "| **B1** | 入场表单 | **五列**：教育／传承材料（正文直述、无留痕标记）\n"
            "| **B1** | 入场表单 | 〔**订正 2026-10-01**：原写「五列」〕\n")
    tmpd = tempfile.mkdtemp(prefix="scanret_selftest_")
    p = os.path.join(tmpd, "case.md")
    open(p, "w", encoding="utf-8").write(body)
    got = [classify(ln, False)
           for _, ln, infence in strip_fences(open(p, encoding="utf-8").read().splitlines())
           if not infence and "五列" in ln]
    exp = ["待判", "记录·留痕"]
    print(f"[自检 1] 围栏跳过 ＋ 两类行分档：得到 {got} · 期望 {exp}")
    if got != exp:
        print("[自检 1] ✗ 分档不符"); ok = False
    else:
        print("[自检 1] ✓ 围栏内不入判 · 直述→待判 · 带留痕标记→记录")

    for path, want_hist, want_dat in [
            ("/Projects/PEC/archived/x.md", True, False),
            ("/Projects/PEC/_bak/y.md", True, False),
            ("/Projects/PEC/raw/2026-09-26_analysis_a.md", False, True),
            ("/Projects/PEC/文明基因/判据/候选面.md", False, False),
            ("/brain/logs/2026-09/checkpoints/z.md", False, False)]:
        g1 = bool(HIST_PATH_RE.search(path))
        g2 = bool(DATALAYER_PATH_RE.search(path))
        f = "✓" if (g1 == want_hist and g2 == want_dat) else "✗"
        if g1 != want_hist or g2 != want_dat:
            ok = False
        print(f"[自检 2] {f} {path}\n           史层={g1}(期望 {want_hist}) · 资料层={g2}(期望 {want_dat})")

    r = next(x for x in RETIRED if x.get("regex"))
    for s, want in [("否则 ⇒ **候选**", True), ("否则 ⇒ 候选", True),
                    ("其余情形 ⇒ 见 `2.0（五）` 二值表", False)]:
        got3 = re.search(r["pat"], s) is not None
        f = "✓" if got3 == want else "✗"
        if got3 != want:
            ok = False
        print(f"[自检 3] {f} 正则串「{r['pat']}」对「{s}」→ {got3}（期望 {want}）")

    print("[自检 4] ✓ 本自检只在 mktemp 目录内造件，未写任何盘上文件"
          if os.path.isdir(tmpd) else "[自检 4] ✗")
    shutil.rmtree(tmpd, ignore_errors=True)
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser(description="PEC 已废规则串残留扫描（提示器，非闸）")
    ap.add_argument("--all", action="store_true", help="连「记录·留痕」与「史层」也逐条列出")
    ap.add_argument("--self-test", action="store_true", help="跑负向自检")
    a = ap.parse_args()
    if a.self_test:
        return self_test()
    # ⚠ fail-closed（2026-10-02 补 · 首版**未实装**、docstring 却承诺了 rc=2 —— 由独立复验者逮出）：
    #   根不可达 ⇒ **静默绿 exit 0** 是本线反复踩的同族病。现：根一个都不存在 / 展开 0 件 ⇒ rc=2。
    roots = expand_roots()
    if not roots:
        print(f"[配置错] 扫描根一个都不存在：{SCAN_DIRS}\n"
              f"          HOST={HOST}（沙箱内请设 PEC_SCAN_HOST=<沙箱 Documents/Claude/>）",
              file=sys.stderr)
        return 2
    files, hits = scan()
    if not files:
        print("[配置错] 扫描根存在但展开出 0 个可读文件 —— 疑似根指错，或被 SKIP 规则整片吞掉",
              file=sys.stderr)
        return 2
    return report(files, hits, a.all)


if __name__ == "__main__":
    sys.exit(main())
