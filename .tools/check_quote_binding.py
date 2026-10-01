#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_quote_binding.py —— 引录绑定检查（**写入侧 lint** · 2026-09-30 Doctor 批立 · v2）

## 它治什么

2026-09-30 CS-05 场一次会话内**同根四犯**：写中文散文时把**自己的转述／标签**也套上引号，
而项目体例（`Projects/PEC/文明基因/判据/文明基因系统.md` §四 4.5）规定
**引号形只用于逐字引录、且须紧跟 `文件:行号`；转述一律不加引号（裸写）**。
后果：核对工具按引录去核、必然核不到；人眼也看不出来（语法正常）。
**本工具已在同场实时逮出第 4 次复发** —— 它就是为此存在的。

## 与 verify_citations.py 的分工

| | `verify_citations.py` | **本工具** |
|---|---|---|
| 定位 | **提示器**（自陈「红要人核、绿不能当通过」） | **写入侧 lint（机械 · 红即拦）** |
| 跨件引用 | 走 WARN 旁路（一个字节都不核） | 照核（用 `--extra` 补路径根） |
| 启发式 | 有（散文名绑定、候选集筛选） | 无 |
| 裸 `:NNN` 简写 | 不进分母 | **不进分母，但至少披露条数**（见下「边界」） |

## 检查四项（任一不过 ⇒ exit 1）

- **A · 绑定**：每一处 `「…」` 必须在**同一行**、且在其**之后的第一个** `` `文件:行号` `` 上**逐字**找得到。
  （v1 只要求「同行任一处出处」——那会让同一行的任一出处为全行所有引号背书，已被第二轮审核者
  用夹具 F5／F5b 击穿；v2 改为**就近唯一绑定**。）
- **A2 · 配对**：每行的 `「` 与 `」` 必须等数（未闭合的引号会让该处检查**静默失效**，F3 实证）。
- **B · 可达**：每一处 `` `文件:行号` `` 都要——文件存在 · 行号在界内 · 所指行**非空行**。
- **C · 结构**：每行加粗标记与反引号成对（**先剥代码段再数**，避免 `` `**` `` 假报）。
- **D · 覆盖面声明**：凡出现**覆盖面声明**（`已全部`／`全部处理`／`已改 N 处`／`逐处改到`／`已逐处`）者，
  该行须**同句或紧邻处给出被点名的条目**（≥1 处 `文件:行号`，或 ≥2 个顿号/斜杠分隔的条目名，或显式写
  `以独立枚举为准`）。**立项理由**：`[G-X151]` 追记二（2026-09-30）——「影响面宣称已清」**次日即复发、同一项目连犯三次**，
  而处方早已写在 canonical 里 ⇒ **纪律层拦不住，须机械层**。

## 用法

    python3 check_quote_binding.py --target <md> --corpus <dir> [--extra <dir> ...]
    python3 check_quote_binding.py --self-test

路径解析：相对路径**先按 cwd 解析**，再依次按 `--corpus` / `--extra`；**若 cwd 与某个 root 上
同名件同时存在，会打印 `AMBIG` 提示**（v1 静默取 cwd，被 F16 逮出）。

## 退出码

    0 = 全过     1 = 有未过项     2 = 配置错误

## 已知边界（**如实标 · 未修** —— 引用本工具结论时须连带）

1. **A 仍是字面判定**：它只证「这串字面在那行上」，**不证「那行支持该断言」**（本场已两度发生
   「在界内＋非空＋内容不符」的引用错，本工具**原理上抓不到**）。
2. **裸 `:NNN` 简写不进分母**：本工具只认反引号包裹的 `` `文件.ext:行号` ``。文中若用
   裸 `:NNN` 承接前文文件名，**既不能拦也不逐条报**——只在结尾**披露条数**（`BARE`），
   供人决定是否回头补全路径。这是**已知的、与 `verify_citations.py` 同形的盲区**。
3. **子串包含可「洗白」短引号**：`q in line` 是纯子串判定，汉字无词界 ⇒ 短引号（如 `「基因」`）
   可被 `基因库贡献` 满足。故 A 对长度 < 4 的引录**另报 `SHORT`**，请人核。
4. **路径遮蔽**：cwd 有同名件时优先取 cwd（v2 已加 `AMBIG` 提示，但**不阻断**）。
4b. **转述带引号有一个原理性盲区**：若那句转述的**字面恰好出现在所指行上**（纯合），本工具**判不出来**
   —— 它只做字面匹配。同形的另一面：**出处前置写法合法**（`` `f:n` 逐字：「…」 ``，本仓既有约定），
   故 A 采用**近邻绑定**（前后 10 字内，后置优先），而不是「只认紧跟在后的出处」。
5. **行号口径**：用 `splitlines()`，与编辑器一致，但 `\\x0b`/`\\u2028` 一类字符也会被当换行；
   本案语料实测无此类字符。
"""

import argparse
import pathlib
import re
import sys
import tempfile

QUOTE = re.compile(r"「([^」]*)」")
# 反引号内：路径（含扩展名）: 行号，行号后可有别的内容（防「尾随空格/说明」漏检）
CITE = re.compile(r"`([^`]*?\.[A-Za-z0-9]+):(\d+)[^`]*`")
BARE = re.compile(r"(?<![\w./-]):(\d+)\b")


def _load(p):
    try:
        return p.read_text(encoding="utf-8").splitlines()
    except Exception:
        return None


class Resolver:
    def __init__(self, roots):
        self.roots = [pathlib.Path(r) for r in roots]
        self.cache = {}
        self.ambiguous = []

    def resolve(self, rel):
        cwd_hit = None
        c = pathlib.Path(rel)
        if c.exists() and c.is_file():
            cwd_hit = c
        for r in self.roots:
            p = r / rel
            if p.exists() and p.is_file():
                if cwd_hit is not None and cwd_hit.resolve() != p.resolve():
                    self.ambiguous.append((rel, str(cwd_hit), str(p)))
                key = str(p)
                if key not in self.cache:
                    self.cache[key] = (p, _load(p))
                return self.cache[key]
        if cwd_hit is not None:
            key = str(cwd_hit)
            if key not in self.cache:
                self.cache[key] = (cwd_hit, _load(cwd_hit))
            return self.cache[key]
        return (None, None)


def check(target, roots):
    lines = _load(pathlib.Path(target))
    if lines is None:
        return None, [("2", target, 0, "target 不存在或读不了")]

    res = Resolver(roots)
    fail_a, fail_a2, fail_b, fail_c, short = [], [], [], [], []
    ok_a = ok_b = 0
    bare_total = 0

    for i, line in enumerate(lines, 1):
        cites = [(m.start(), m.end(), m.group(1), m.group(2)) for m in CITE.finditer(line)]
        bare_total += len(BARE.findall(CITE.sub("", line)))

        # --- A2 · 配对 ---
        if line.count("「") != line.count("」"):
            fail_a2.append((target, i, f"「×{line.count('「')} 」×{line.count('」')}"))

        # --- B · 可达 ---
        for _, _, rel, n in cites:
            real, src = res.resolve(rel)
            if real is None:
                fail_b.append((target, i, rel, n, "文件不存在（已试 cwd + 各 root）"))
            elif src is None:
                fail_b.append((target, i, rel, n, "文件在但读不了"))
            elif not (1 <= int(n) <= len(src)):
                fail_b.append((target, i, rel, n, f"行号越界（该件共 {len(src)} 行）"))
            elif not src[int(n) - 1].strip():
                fail_b.append((target, i, rel, n, "所指行是空行"))
            else:
                ok_b += 1

        # --- A · 绑定（近邻唯一：后置优先，前置亦合法）---
        GAP = 10       # 引录与其出处的最大间隔（字符数）
        def _bound(qstart, qend):
            for pos, end, rel, n in cites:                       # 后置优先
                if pos >= qend and pos - qend <= GAP:
                    return (rel, n)
            for pos, end, rel, n in cites:                       # 前置（出处前置写法）
                if end <= qstart and qstart - end <= GAP:
                    return (rel, n)
            return None

        for m in QUOTE.finditer(line):
            q = m.group(1)
            if not q:
                continue
            hit = _bound(m.start(), m.end())
            if hit is None:
                fail_a.append((target, i, q, f"近邻（前后 {GAP} 字内）无 `文件:行号`"))
                continue
            rel, n = hit
            real, src = res.resolve(rel)
            if real and src and 1 <= int(n) <= len(src) and q in src[int(n) - 1]:
                ok_a += 1
                if len(q) < 4:
                    short.append((target, i, q, f"引录过短（{len(q)} 字）——子串包含可能误判"))
            else:
                fail_a.append((target, i, q, f"近邻出处 `{rel}:{n}` 上逐字找不到"))

    # --- C · 结构 ---
    fail_c = []
    for i, line in enumerate(lines, 1):
        if line.strip():
            stripped = re.sub(r"`[^`]*`", "", line)
            if stripped.count("**") % 2:
                fail_c.append((target, i, "加粗标记不成对", f"剥代码段后 `**` × {stripped.count('**')}"))
            if line.count("`") % 2:
                fail_c.append((target, i, "反引号不成对", f"` × {line.count('`')}"))

    # --- D · 覆盖面声明（承 [G-X151] 追记二）---
    COVER = re.compile(r"已全部|全部处理|已改\s*\d+\s*处|逐处改到|已逐处")
    fail_d = []
    for i, line in enumerate(lines, 1):
        if not COVER.search(line):
            continue
        window = "\n".join(lines[i - 1:i + 2])
        has_cite = bool(CITE.search(window))
        names = re.findall(r"[\u4e00-\u9fffA-Za-z0-9\-_]{2,}", line)
        has_list = ("、" in line or "／" in line) and len(set(names)) >= 6
        has_disc = "以独立枚举为准" in window
        if not (has_cite or has_list or has_disc):
            fail_d.append((target, i, line.strip()[:90],
                           "覆盖面声明未见点名对账（无行号／无列举／无免责句）"))

    return {
        "ok_a": ok_a, "ok_b": ok_b, "bare": bare_total,
        "fa": fail_a, "fa2": fail_a2, "fb": fail_b, "fc": fail_c, "fd": fail_d,
        "short": short, "ambig": res.ambiguous,
    }, []


def self_test():
    cases = []
    with tempfile.TemporaryDirectory() as d:
        d = pathlib.Path(d)
        (d / "corpus").mkdir()
        (d / "corpus" / "src.md").write_text(
            "第一行普通文字\n第二行含目标串 甲甲甲 在此\n\n第四行 基因库贡献 一栏\n", encoding="utf-8"
        )

        def run(body):
            t = d / "t.md"
            t.write_text(body, encoding="utf-8")
            r, err = check(str(t), [str(d / "corpus")])
            return r

        def ok(res, expect):
            fa, fa2, fb, fc, fd = res["fa"], res["fa2"], res["fb"], res["fc"], res["fd"]
            if expect == "pass":
                return not fa and not fa2 and not fb and not fc and not fd   # pass 亦查 C/D
            if expect == "A":
                return bool(fa)
            if expect == "A2":
                return bool(fa2)
            if expect == "B":
                return bool(fb)
            if expect == "D":
                return bool(fd)
            return bool(fc)

        cases += [
            ("P1 正例·引录绑定成功", '「甲甲甲」`src.md:2`\n', "pass"),
            ("N1 负例·引录无出处", '「甲甲甲」\n', "A"),
            ("N2 负例·引录不在所指行", '「甲甲甲」`src.md:1`\n', "A"),
            ("N3 负例·转述带引号（无落点）", '这是「多元状态」的一读。\n', "A"),
            ("N4 负例·行号越界", '正文 `src.md:99`\n', "B"),
            ("N5 负例·指向空行", '正文 `src.md:3`\n', "B"),
            ("N6 负例·文件不存在", '正文 `nosuch.md:1`\n', "B"),
            ("P2 正例·转述裸写", '这是多元状态的一读。\n', "pass"),
            ("N7 负例·加粗不成对", '**开 ** 关**\n', "C"),
            ("P3 正例·代码段内 `**` 不假报", '正文 `**` 字面量。\n', "pass"),
            # —— v2 新增（对应第二轮审核者击穿的漏报边）——
            ("N8 负例·未闭合 「（A2·配对）", '正文写到「甲甲甲 就断了。\n', "A2"),
            ("N9 负例·近邻绑定：所指行不含该串即拦",
             '这是「多元状态」的一读，出处 `src.md:1`。\n', "A"),
            ("P4 正例·出处前置写法（本仓既有约定）",
             '`src.md:2` 逐字：「甲甲甲」\n', "pass"),
            ("N10 负例·子串洗白：短引号被长词满足不得算过（F5b 复现）",
             '「基因」这个标签，出处 `src.md:4`。\n', "pass"),   # 应过 A，但须进 SHORT
            ("N11 负例·行号后带尾随内容（B-4 复现）", '载于 `src.md:99 载体列` 一处。\n', "B"),
            ("N12 负例·大写扩展名（B-3 复现）", '载于 `nosuch.MD:1` 一处。\n', "B"),
            # —— v3 新增：D 项（覆盖面声明 · 承 [G-X151] 追记二）——
            ("N13 负例·覆盖面声明无点名对账", '本轮已全部处理完毕。\n', "D"),
            ("P5 正例·覆盖面声明带免责句", '本轮已全部处理（以独立枚举为准）。\n', "pass"),
            ("P6 正例·覆盖面声明带行号", '已改 3 处：`src.md:1` `src.md:2`。\n', "pass"),
        ]

        good = 0
        for name, body, expect in cases:
            res = run(body)
            if name.startswith("N10"):
                passed = not res["fa"] and bool(res["short"])       # A 过 + 必须报 SHORT
            else:
                passed = ok(res, expect)
            print(f"  {'✓' if passed else '✗'} {name}")
            good += 1 if passed else 0
        # ② 入口级：把 CLI 当子进程跑，断言 exit code（承 [G-X188] 追记 · 2026-10-01）
        #    为什么必须有这一段：D 项曾在 main() 里是死代码，而引擎级自测全绿。
        #    只测内部函数 = 测了引擎、没测闸门。
        import subprocess
        me = pathlib.Path(__file__).resolve()
        ok_f = d / "cli_pass.md"; ok_f.write_text("「甲甲甲」`src.md:2`\n", encoding="utf-8")
        ng_f = d / "cli_fail.md"; ng_f.write_text("本轮已全部处理完毕。\n", encoding="utf-8")
        entry = []
        def run_cli(fp):
            return subprocess.run([sys.executable, str(me), "--target", str(fp),
                                   "--corpus", str(d / "corpus")], capture_output=True, text=True)
        r1 = run_cli(ok_f)
        entry.append(("E1 入口级·正例应 exit 0", r1.returncode == 0, r1.returncode))
        # 按检查项各一例（承第五轮审核者 B4：原先只守 D，摘掉 C 的接入自测仍全绿）
        CASES = [
            ("EA A 项", "「甲甲甲」\n", "❌ A"),
            ("E2 A2 项", "写到「甲甲甲 就断了\n", "❌ A2"),
            ("EB B 项", "正文 `nosuch.md:1`\n", "❌ B"),
            ("EC C 项", "**开 ** 关**\n", "❌ C"),
            ("ED D 项", "本轮已全部处理完毕。\n", "❌ D"),
        ]
        for tag, body, mark in CASES:
            f = d / f"cli_{mark[-1]}.md"; f.write_text(body, encoding="utf-8")
            r = run_cli(f)
            entry.append((f"{tag}·入口级应 exit 1 且真拦（防死代码）",
                          r.returncode == 1 and mark in r.stdout, r.returncode))
        print()
        for name, passed, rc in entry:
            print(f"  {'✓' if passed else '✗'} {name}（exit={rc}）")
            good += 1 if passed else 0
        total = len(cases) + len(entry)
        print(f"\nself-test：{good}/{total} 通过（引擎级 {len(cases)} ＋ 入口级 {len(entry)}）")
        return 0 if good == total else 1


def main():
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("--target")
    ap.add_argument("--corpus")
    ap.add_argument("--extra", action="append", default=[])
    ap.add_argument("--self-test", action="store_true", dest="self_test")
    a = ap.parse_args()

    if a.self_test:
        sys.exit(self_test())
    if not a.target or not a.corpus:
        print("用法：--target <md> --corpus <dir> [--extra <dir> ...]  |  --self-test")
        sys.exit(2)
    if not pathlib.Path(a.target).exists():
        print(f"配置错误：target 不存在 {a.target}")
        sys.exit(2)
    if not pathlib.Path(a.corpus).exists():
        print(f"配置错误：corpus 不存在 {a.corpus}")
        sys.exit(2)
    if not any(pathlib.Path(a.corpus).rglob("*.md")):
        print(f"配置错误：corpus 内无 .md —— {a.corpus}")
        sys.exit(2)

    roots = [a.corpus] + a.extra
    res, err = check(a.target, roots)
    if err:
        print(f"配置错误：{err}")
        sys.exit(2)

    print(f"引录绑定检查：{pathlib.Path(a.target).name}")
    print(f"  roots: {roots}")
    print(f"  A·绑定  通过 {res['ok_a']} · 未过 {len(res['fa'])}")
    print(f"  A2·配对 未过 {len(res['fa2'])}")
    print(f"  B·可达  通过 {res['ok_b']} · 未过 {len(res['fb'])}")
    print(f"  C·结构  未过 {len(res['fc'])}")
    print(f"  D·覆盖面 未过 {len(res['fd'])}")
    print(f"  ⚠ 裸 `:NNN` 简写（**不进 A/B 分母**，仅披露）：{res['bare']} 处")
    if res["short"]:
        print(f"  ⚠ SHORT 过短引录（子串包含可能误判，请人核）：{len(res['short'])} 处")
        for t, i, q, why in res["short"]:
            print(f"      · L{i} 「{q}」—— {why}")
    for t, i, why in res["fa2"]:
        print(f"    ❌ A2 L{i} {why}")
    for t, i, q, why in res["fa"]:
        print(f"    ❌ A L{i} 「{q}」—— {why}")
    for t, i, rel, n, why in res["fb"]:
        print(f"    ❌ B L{i} `{rel}:{n}` —— {why}")
    for t, i, what, why in res["fc"]:
        print(f"    ❌ C L{i} {what} —— {why}")
    for t, i, snippet, why in res["fd"]:
        print(f"    ❌ D L{i} {why}\n         ▸ {snippet}")
    for rel, a1, a2 in res["ambig"]:
        print(f"    ⚠ AMBIG `{rel}` 在 cwd 与 root 各有一份，本工具取 root：{a1} ↔ {a2}")

    if not res["fa"] and not res["fa2"] and not res["fb"] and not res["fc"] and not res["fd"]:
        print("  ⇒ PASS（**仅证**字面绑定 · 配对 · 可达 · 结构；**不证语义支持**，也不覆盖裸 `:NNN`）")
        sys.exit(0)
    print("  ⇒ FAIL（写入侧拦截）")
    sys.exit(1)


if __name__ == "__main__":
    main()
