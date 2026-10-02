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
  ② 每个命中给**预分类**：`待判` / `资料层·须指针` / `记录·留痕` / `记录·按路径`；
     **凡收窄匹配或按路径分类的规则，都在报告里显式打印**（见 `report()` 的声明段）；
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
import pathlib
import re
import sys

HOST = os.environ.get("PEC_SCAN_HOST", "/Users/lunarabbit/Documents/Claude/")
if not HOST.endswith("/"):
    HOST += "/"

# ── 已废规则串（「当时是规则、现已被裁改」的字面） ────────────────────────────
# 每项：pat（字面或正则）· 废于何时 · 现行为何 · 备注
RETIRED = [
    {"pat": "五列", "since": "2026-10-01",
     # ⚠ **域护栏**（2026-10-02 加 · 承未参与实施的独立复验者）：`五列` 是**子串**，
     #   跨域撞车已在盘上实测为假阳性（`brain/permanent/经验库.md` 的「三五列」＝烛照
     #   `engine_*` 的列数、`2026-07-30-情绪周期反转日标注层.md` 同）⇒ 须与 **PEC 语境词同现**。
     #   ⚠ **这是精度护栏、不是缩面**：扫描面未缩、件数未减；且本护栏**在报告里显式声明**
     #   （见 `report()` 的「串表护栏」段），不静默。
     "now": "四列（入场表单第 4 档「作为原因／条件出现 ❌」已随 Doctor 裁删）",
     "require": ("B1", "入场表单", "表单", "S8", "归位", "候选面")},
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
    # ⚠ 2026-10-02 扩面（承 Doctor 令「直接开」那三个面外面 · 由独立复验者 Q5 报出）：
    #   此前只扫 `logs/*/checkpoints` ⇒ **月折主日志、`checkups/`、`permanent/` 全在面外**。
    #   ⚠ 必须**替换**而非叠加：`brain/logs` 已含 checkpoints/checkups/月目录 ⇒
    #   若与旧的 checkpoints 项并存会**重复扫同一批件**（独立复验者专门核过「无重复根」）。
    "brain/logs",
    "brain/PEC",
    "brain/permanent",
]
SKIP_DIR_PARTS = {".git", "_bak", "archived", "__pycache__", "node_modules",
                  ".ruff_cache", "dist", ".pytest_cache"}
SKIP_SUFFIX = (".pyc", ".png", ".jpg", ".jpeg", ".gif", ".pdf",
               ".zip", ".tar", ".gz", ".sqlite3", ".db", ".xlsx")
# ⚠ 备份件过滤用**模式式**：`endswith(".bak")` 漏掉 `.bak_p1b_2026-09-29` / `.bak_audit_...`
#   一类命名（2026-10-02 由未参与实施的独立复验者逮出 —— 新增的根级 `checkpoints` 根
#   **全部收益 +16 命中都落在 6 个此类备份件里、且全归「史层」静默**，即零真价值）。
SKIP_RE = re.compile(r"\.bak($|[_.])")

# ⚠ 2026-10-02：**`史层` 档已删除** —— 它结构性不可达：`SKIP_DIR_PARTS` 先把
#   `archived/`／`_bak/`／`_DEPRECATED_` 目录整片吃掉，`SKIP_RE` 再把 `.bak*` 件吃掉
#   ⇒ 该档只能收 0，**留一个永远空的列会误导**（承未参与实施的独立复验者报出）。
#   原 `HIST_PATH_RE` 一并删除（其中的 `\.bak` 已成死代码）。
#   这些层的排除**改为由两条 skip 规则显式承担**，并在报告中以「已剪枝 N 件」声明。
#
# ⚠ 同日新增 **`记录·按路径`**（承 Doctor 令扫「三个面外面」后暴露）：`brain/logs/**`
#   是**按构造即记录**的层（会话日志 ＋ `checkups/` 体检/复验报告）—— 它们**天然引述**
#   被讨论的串，把它当「待判」是**范畴错误**。
#   **⚠ 但 `checkpoints/` 必须排除**：起手包与 PRD 住在那儿，**是现行执行件**，不是记录。
#   **本分类不等于缩面**：件仍在扫描面内、仍逐条列出（`--all`）、仍计入 `【命中】`；
#   只是**不进「需处置」集**。**该规则在报告里显式声明。**
LOG_RECORD_RE = re.compile(r"^brain/logs/")


def is_log_record(rel: str) -> bool:
    return bool(LOG_RECORD_RE.search(rel)) and "checkpoints" not in rel.split("/")


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
                if fn.endswith(SKIP_SUFFIX) or SKIP_RE.search(fn):
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


def hit(line: str, r: dict) -> bool:
    """**唯一命中判据**（`scan()` 与 `self_test()` 共用）。

    ⚠ 2026-10-02 抽出（承未参与实施的独立复验者 **E-C-1**）：此前 `self_test` 把域护栏逻辑
    **重抄了一遍**、不调生产路径 ⇒ 停用 `scan()` 里的 `require` 闸，自检**仍全绿 rc=0**
    ——**齿是假的**。这与本仓 `G-X188`（自测走内部路径、没走真实入口）**同型**。
    ⇒ 判据只此一处；自检改调它 ＋ 另加**入口级**自测（走真 `scan()`）。
    """
    ok = re.search(r["pat"], line) is not None if r.get("regex") else r["pat"] in line
    if not ok:
        return False
    # **域护栏**（非缩面）：须与 PEC 语境词同现，专治跨域子串撞车
    if r.get("require") and not any(w in line for w in r["require"]):
        return False
    return True


def classify(line, log_path=False, datalayer=False):
    """单行 → 预分类（scan 与 self_test 共用同一把尺）。
    顺序有意：① **按路径即记录**（`brain/logs/**`，排 `checkpoints/`）；② 带留痕标记 → 记录；
    ③ **资料层（`raw/` 日期件）单列**（不静默）；④ 其余待判。
    """
    if log_path:
        return "记录·按路径"
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
        log_path = is_log_record(rel)
        datalayer = bool(DATALAYER_PATH_RE.search("/" + rel))
        for no, line, infence in strip_fences(txt.splitlines()):
            if infence:
                continue
            for r in RETIRED:
                if not hit(line, r):
                    continue
                hits.append({"file": rel, "line": no, "pat": r["pat"],
                             "since": r["since"], "now": r["now"],
                             "klass": classify(line, log_path, datalayer),
                             "text": line.strip()[:160]})
    return files, hits


def report(files, hits, all_hits=False, roots=None):
    pend = [h for h in hits if h["klass"] == "待判"]
    dat = [h for h in hits if h["klass"] == "资料层·须指针"]
    rec = [h for h in hits if h["klass"] == "记录·留痕"]
    logrec = [h for h in hits if h["klass"] == "记录·按路径"]
    print("═" * 78)
    print("PEC 已废规则串残留扫描 —— 提示器（非闸）")
    print("═" * 78)
    print(f"【扫描面】件 {len(files)} · 串 {len(RETIRED)} · 组合 {len(files) * len(RETIRED)}")
    # ⚠ 2026-10-02 改（承未参与实施的独立复验者 I4）：**印展开后的真实根**，不再印模式串 ——
    #   初版把 `SCAN_DIRS` 的模式串照印，**展开为空或不存在的根也照印** ⇒ 「扫描面」读数可虚。
    if roots:
        print(f"    展开后根 {len(roots)} 个：")
        for r in roots:
            print(f"      · {os.path.relpath(r, HOST)}")
    unmatched = [d for d in SCAN_DIRS if not glob.glob(os.path.join(HOST, d))]
    if unmatched:
        print(f"    ⚠ 未参与扫描（展开为空）：{unmatched}")
    # ⚠ 2026-10-02 补（承未参与实施的独立复验者 · 件 C）：**把剪枝数显式声明出来** ——
    #   `.bak*` 过滤一装，`brain/logs` 面内 70 件/58 处便**静默**移出了扫描面，
    #   而「**静默剪枝＝排除制造盲面**」正是本工具自己声称要治的病。⇒ 剪枝必须**可见**。
    pruned = 0
    for r in (roots or []):
        for dp, dns, fns in os.walk(r):
            dns[:] = [x for x in dns if x not in SKIP_DIR_PARTS]
            pruned += sum(1 for fn in fns if fn.endswith(SKIP_SUFFIX) or SKIP_RE.search(fn))
    if pruned:
        print(f"    （已剪枝 **{pruned}** 件：后备／二进制类 —— 依 `SKIP_SUFFIX` ＋ `SKIP_RE`。"
              f"**此数为声明项、非静默**）")
    # ⚠ **声明段**（2026-10-02 加）：本线的病是「**静默排除制造盲面**」⇒
    #   凡**收窄匹配**或**按路径分类**的规则，一律在此**显式打印**，不留给读者去读源码。
    gated = [r["pat"] for r in RETIRED if r.get("require")]
    if gated:
        print(f"    ⚠ **串表护栏（显式声明 · 精度护栏、非缩面）**：{gated}")
        print(f"       —— 该串仅在**与 PEC 语境词同现**时才算命中（`require`），"
              f"专治跨域子串撞车（实测：烛照 `engine_*` 的「五列」「三五列」）")
    print("    ⚠ **按路径判记录（显式声明 · 非缩面）**：`brain/logs/**`"
          "（**排 `checkpoints/`** —— 起手包与 PRD 是现行执行件，不按记录论）"
          " ⇒ 该层按构造即记录（会话日志 ＋ checkups 报告），**件仍在扫描面内、仍逐条列出（`--all`）、"
          "仍计入【命中】**，只是不进「需处置」集")
    print(f"【命中】{len(hits)} 处 —— 待判 {len(pend)} · 资料层·须指针 {len(dat)}"
          f" · 记录·留痕 {len(rec)} · 记录·按路径 {len(logrec)}")
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
        for tag, group in (("记录·留痕", rec), ("记录·按路径", logrec)):
            if not group:
                continue
            print(f"\n▼ {tag}（{len(group)} 处 · 仅列路径:行）")
            for h in group:
                print(f"    {h['file']}:{h['line']}  「{h['pat']}」")
    print()
    print("⚠ 预分类是启发式的：'待判' 里必有假阳性，'记录' 里也可能藏真残留 —— 红须人核、绿不能当通过。")
    return 1 if (pend or dat) else 0


def self_test():
    """负向自检**六式**：① 围栏内不入判 · ② 直述→待判 / 带留痕→记录 · ③ 按路径记录与资料层正反例（含排 checkpoints）· ④ 正则型串（**经 `hit()`**）· ⑤ 域护栏（**经 `hit()`**）· ⑥ **入口级**（造合成 HOST 走真 `scan()`：域护栏／按路径记录／资料层 三条接线）。
    ⚠ 计数声明须随实现同改（本行曾写「五式」而实跑已到 `[自检 6]`）——承独立复验者 ③-6 逮出。
    """
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

    for path, want_log, want_dat in [
            ("brain/logs/2026-09/2026-09-26-x.md", True, False),
            ("brain/logs/checkups/2026-10-02-y.md", True, False),
            ("brain/logs/2026-09/checkpoints/z.md", False, False),
            ("brain/logs/checkpoints/z.md", False, False),
            ("Projects/PEC/raw/2026-09-26_analysis_a.md", False, True),
            ("Projects/PEC/文明基因/判据/候选面.md", False, False)]:
        g1 = is_log_record(path)
        g2 = bool(DATALAYER_PATH_RE.search("/" + path))
        f = "✓" if (g1 == want_log and g2 == want_dat) else "✗"
        if g1 != want_log or g2 != want_dat:
            ok = False
        print(f"[自检 2] {f} {path}\n"
              f"           按路径记录={g1}(期望 {want_log}) · 资料层={g2}(期望 {want_dat})")

    # 自检 5：**域护栏**（`五列` 须与 PEC 语境词同现 —— 精度护栏、非缩面）
    #   ⚠ 改调**共享判据 `hit()`**（原版把护栏逻辑重抄一遍 ⇒ 假齿，见 E-C-1）
    gated = next(x for x in RETIRED if x.get("require"))
    for s, want in [("| **B1** | **五列**：教育／传承材料 |", True),
                    ("字段不多（三五列），手抄看起来完全够用", False),
                    ("`engine_*` 五列是**评测基线**", False)]:
        got5 = hit(s, gated)
        f = "✓" if got5 == want else "✗"
        if got5 != want:
            ok = False
        print(f"[自检 5] {f} 域护栏「{gated['pat']}」经 hit() 对「{s[:26]}」→ {got5}（期望 {want}）")

    # 自检 6 ★ **入口级**（承 E-C-1）：造合成 HOST，**走真 `scan()`**，
    #   验「域护栏接线」与「按路径记录接线」两条 —— 只调内部谓词不算数（G-X188）。
    import shutil as _sh
    import tempfile as _tf
    global HOST
    _old = HOST
    _td = _tf.mkdtemp(prefix="scanret_entry_")
    try:
        _r = pathlib.Path(_td) / "Projects" / "PEC"
        _r.mkdir(parents=True)
        (_r / "a.md").write_text(
            "| **B1** | **五列**：教育／传承材料 |\n"          # 行1 应命中（带语境）
            "| 快照字段不多（三五列），手抄够用 |\n"             # 行2 应被域护栏挡掉
            "| **B1** | **五列**：留存为记录 |\n",              # 行3 应命中
            encoding="utf-8")
        _l = pathlib.Path(_td) / "brain" / "logs" / "checkups"
        _l.mkdir(parents=True)
        (_l / "b.md").write_text("| **B1** | **五列** |\n", encoding="utf-8")   # 应按路径判记录
        _d = pathlib.Path(_td) / "Projects" / "PEC" / "raw"
        _d.mkdir(parents=True)
        (_d / "2026-09-26_analysis_c.md").write_text("| **B1** | **五列** |\n", encoding="utf-8")  # 应判资料层
        HOST = _td
        _files, _hits = scan()
        _got_gate = sorted(h["line"] for h in _hits if h["pat"] == "五列" and h["file"].endswith("a.md"))
        _cls_log = {h["klass"] for h in _hits if h["file"].endswith("b.md")}
        _cls_dat = {h["klass"] for h in _hits if h["file"].endswith("c.md")}
        _w1, _w2, _w3 = [1, 3], {"记录·按路径"}, {"资料层·须指针"}
        if _got_gate != _w1 or _cls_log != _w2 or _cls_dat != _w3:
            ok = False
            print(f"[自检 6] ✗ 入口级：命中行 {_got_gate}（期望 {_w1}）"
                  f" · 记录层 {_cls_log}（期望 {_w2}）· 资料层 {_cls_dat}（期望 {_w3}）")
        else:
            print(f"[自检 6] ✓ 入口级（真 scan()）：域护栏接线有效（命中行 {_got_gate}）"
                  f" · 按路径记录接线有效（{_cls_log}）· 资料层接线有效（{_cls_dat}）")
    finally:
        HOST = _old
        _sh.rmtree(_td, ignore_errors=True)

    r = next(x for x in RETIRED if x.get("regex"))
    for s, want in [("否则 ⇒ **候选**", True), ("否则 ⇒ 候选", True),
                    ("其余情形 ⇒ 见 `2.0（五）` 二值表", False)]:
        got3 = hit(s, r)   # ⚠ 改调**共享判据**（原重抄 `re.search` ⇒ M6 残余假齿，承独立复验者逮出）
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
    ap.add_argument("--all", action="store_true", help="连「记录·留痕」与「记录·按路径」也逐条列出")
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
    return report(files, hits, a.all, roots)


if __name__ == "__main__":
    sys.exit(main())
