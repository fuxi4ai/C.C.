#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""风险日报 发布拆分器（2026-11-12 立 · Doctor 裁「拆成三页」· 配合 artifact_fragment.py 使用）。

原件 risk-daily.html 约 45.6 万字符，并用两个 iframe（srcdoc）内嵌了两份完整 HTML 文档，
通用片段生成器按「通读上限」与「含 iframe」直接拒绝。本工具只读原件（不改不动），拆成三个托管页：
  risk-daily                 主页（风险总览 + 股权溢价指数；原 AI / EAL 两个标签页改成链接卡片）
  risk-daily-ai-alarm        AI Tech Alarm（原 AI_HTML 常量里的那份文档）
  risk-daily-eal-starfield   EAL 事件星空（原 EAL_HTML 常量里的那份文档）
做法：
  1. 子页面：把大脚本里的 const AI_HTML="…"; / const EAL_HTML="…"; 按 JSON 字符串字面量解码成完整文档，
     各自交 artifact_fragment.build() 去壳。交之前在 <head> 开头补一条「外壳中和」样式（见 neutralize）：
     发布工具的外壳给 body 设了白底、黑字、14px 无衬线；子页面若把底色/字色/字体写在 :root 上、靠 body 继承
     （EAL 星空就是），不中和就会变成白底黑字。<meta name="color-scheme"> 会被 build() 连同其它 meta 去掉，
     这里先转成等价的 :root{color-scheme:…}。子页面自己的样式、脚本、链接一律原样。
  2. 主页：从大脚本里删掉两个常量行、两条 srcdoc 赋值、aiframe 自适应高度那段；两个 iframe 各换成一张链接卡片
     （沿用页面已有的 .acard 与配色变量，普通 <a target="_blank">）。其余内容与脚本逐字保留，再交 build()。
     标签切换逻辑（showTab）不动：它只切 .pane 的 hidden，与 iframe 无关。
- 输出：brain/.tmp/artifact-publish/<三个 id>/ 下各有 artifact.html 与 manifest.json。
- 确定性：同一输入 → 同一输出。
- fail-closed（exit 1，三页都不写）：常量/赋值/自适应高度代码/iframe 的数量或形态与预期不符、字符串解码失败、
  删改后主页仍残留对它们的引用、子文档里又套了 iframe、color-scheme 的 meta 写法不认识、build() 拒绝、
  任一页超过通读上限、链接卡片不是恰好两张、托管页地址与 hosted-pages.json 登记不一致。
  Google Fonts 的 <link> 不是恰好三条或删后仍有残留（三页都删在线字体，回退本机字体，2026-11-12）。
  三页全部在内存里算完、检查完，才开始第一次写盘。
- 不删任何文件，不改原件，不改 artifact_fragment.py。
用法：python3 artifact_split_risk_daily.py [--src <原件.html>] [--max-chars 300000]
"""
import argparse, hashlib, json, os, re, sys

sys.dont_write_bytecode = True  # import 同目录模块时不往 .tools/__pycache__ 里添文件
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import artifact_fragment  # noqa: E402

DEFAULT_SRC = "Projects/风险日报/dashboard/risk-daily.html"  # 相对 <Documents>/Claude；清单里也按相对路径记，不带会话目录
MAIN_ID, AI_ID, EAL_ID = "risk-daily", "risk-daily-ai-alarm", "risk-daily-eal-starfield"
# 三个托管页地址（2026-11-12 建，登记在 brain/.tmp/artifact-publish/hosted-pages.json；两处不一致即 fail-closed）
URLS = {MAIN_ID: "https://claude.ai/artifact/HksT4v7iLnd6wwNNcgBQoD",
        AI_ID: "https://claude.ai/artifact/FVfaj7n3LCNoSFA7QpCCig",
        EAL_ID: "https://claude.ai/artifact/FCXvHk1SZAbjU3zPAbDuUm"}
# 子页面：(看板 id, 常量名, iframe 的 id, 卡片上的名字)
SUBS = ((AI_ID, "AI_HTML", "aiframe", "AI Tech Alarm"),
        (EAL_ID, "EAL_HTML", "ealframe", "EAL 事件星空"))
# aiframe 自适应高度那段（同源 srcdoc 直读 scrollHeight）。逐字钉住：原件这段一变就停下来让人看
FIT = ("(function(){const f=document.getElementById('aiframe');const fit=()=>{try{const d=f.contentDocument;"
       "if(!d||!d.documentElement)return;f.style.height=Math.max(900,d.documentElement.scrollHeight+4)+'px';}catch(e){}};\n"
       " f.addEventListener('load',()=>{fit();try{new ResizeObserver(fit).observe(f.contentDocument.body);}"
       "catch(e){setInterval(fit,800);}});})();\n")
CONST_FMT = r'^const %s=("(?:[^"\\\n]|\\.)*");\n'
ASSIGN_FMT = "document.getElementById('%s').srcdoc=%s;\n"
PANE_FMT = r'(<div id="pane-%s" class="pane" hidden>)<iframe class="aiframe" id="%s" title="[^"<>]*"></iframe>(</div>)'
CARD_FMT = ('<div class="acard" data-split-link="%s" style="margin-top:14px">'
            '<div class="arow" style="margin-top:0;font-size:14px">%s 已拆到独立页面 · '
            '<a href="%s" target="_blank" rel="noopener" style="color:var(--acc);font-weight:700;text-underline-offset:3px">打开</a></div>'
            '<div class="asmall">托管页单页有体量上限，这块面板单独成页；与本页由同一份原件、同一次拆出。</div></div>')
HEAD_OPEN = re.compile(r"<head(?:\s[^>]*)?>", re.I)
CS_META = re.compile(r'<meta\s+name="color-scheme"\s+content="([a-z ]+)"\s*/?>', re.I)
CS_ANY = re.compile(r"<meta\b[^>]*color-scheme[^>]*>", re.I)
# 外壳给 body 设了 background:#fff;color:#000;font:14px 无衬线。没被外壳包着的页面里，body 这三样都是
# 「继承 html / 透明」。这条样式放在子页面 <head> 最前（build() 的复位之后、页面自己的样式之前），页面自己写了的照样盖过它
NEUTRAL = "body{font:inherit;color:inherit;background:transparent}"


def die(msg):
    sys.exit("split FAIL（fail-closed，未写出产物）：" + msg)


def default_src(brain):
    # brain 根是 <Documents>/Claude/brain，原件在 <Documents>/Claude/Projects/… 下
    return os.path.join(os.path.dirname(brain), DEFAULT_SRC)


def cut_once(text, piece, what):
    """从 text 里删去恰好出现一次、且独占整行的 piece（含行尾换行）。"""
    n = text.count(piece)
    if n != 1:
        die("%s 应恰好一处，实际 %d 处" % (what, n))
    i = text.index(piece)
    if i and text[i - 1] != "\n":
        die("%s 不是独占一行" % what)
    return text[:i] + text[i + len(piece):]


def neutralize(doc, what):
    """子文档 <head> 开头补外壳中和样式；color-scheme 的 meta 转成等价 CSS（build() 会去掉所有 meta）。"""
    metas = CS_META.findall(doc)
    if len(metas) != len(CS_ANY.findall(doc)) or len(metas) > 1:
        die("%s：color-scheme 的 meta 写法不认识或不止一个" % what)
    css = NEUTRAL + (":root{color-scheme:%s}" % metas[0].strip().lower() if metas else "")
    heads = HEAD_OPEN.findall(doc)
    if len(heads) != 1:
        die("%s：<head> 开标签应恰好一个，实际 %d 个" % (what, len(heads)))
    m = HEAD_OPEN.search(doc)
    return doc[:m.end()] + "\n<style>" + css + "</style>" + doc[m.end():]


# 在线字体：托管页允许加载 Google Fonts，侧栏不允许——侧栏一直回退到本机思源宋体（Doctor 认定的正确观感）。
# 云端若加载 Google 下发的 Noto Serif SC，笔画更细、小字发虚（2026-11-12 Doctor 目验 + 裁定去掉）。
# 所以三页片段都删掉 Google Fonts 的 <link>，让云端与侧栏一样回退本机字体。原件不动。
WEBFONT_LINK = re.compile(r'<link\b[^>]*\bhref="https://fonts\.(?:googleapis|gstatic)\.com[^"]*"[^>]*>\n?')


def strip_webfont(frag, what):
    """删掉片段里的 Google Fonts <link>（恰好三条：两条 preconnect + 一条样式表）；删后不得再有任何引用。"""
    hits = WEBFONT_LINK.findall(frag)
    if len(hits) != 3 or sum('rel="stylesheet"' in h for h in hits) != 1:
        die("%s 的 Google Fonts <link> 应恰好三条（两条 preconnect + 一条样式表），实际 %d 条" % (what, len(hits)))
    out = WEBFONT_LINK.sub("", frag)
    for bad in ("fonts.googleapis.com", "fonts.gstatic.com"):
        if bad in out:
            die("%s 删掉在线字体 <link> 后仍残留「%s」" % (what, bad))
    return out


def build(doc, max_chars, what):
    """调 artifact_fragment.build()；它拒绝时把是哪一页补进报错，照旧 exit 1。"""
    try:
        return artifact_fragment.build(doc, max_chars)
    except SystemExit as ex:
        die("%s 被片段生成器拒绝 —— %s" % (what, ex.code))


def split(html, max_chars):
    """完整原件 -> {看板 id: (片段, 附加清单字段)}。任何一步不符即 fail-closed。"""
    if "\r" in html:
        die("原件含回车符（CR），行结构与预期不符")
    main, out = html, {}
    for bid, const, frame, label in SUBS:
        # 1) 常量行：恰好一行 const X="…"; 字面量按 JSON 字符串解码
        pat = re.compile(CONST_FMT % const, re.M)
        hits = pat.findall(main)
        if len(hits) != 1 or len(re.findall(r"\bconst\s+%s\b" % const, main)) != 1:
            die("常量 %s 应恰好一行 const %s=\"…\";，实际匹配 %d 处" % (const, const, len(hits)))
        try:
            sub = json.loads(hits[0])
        except ValueError as ex:
            die("常量 %s 不能按 JSON 字符串字面量解码：%s" % (const, ex))
        if not isinstance(sub, str) or not re.match(r"\s*<!doctype html>", sub, re.I):
            die("常量 %s 解码后不是一份完整 HTML 文档" % const)
        if re.search(r"<iframe\b|\bsrcdoc\s*=", sub, re.I):
            die("子文档 %s 里又套了 iframe / srcdoc" % const)
        main = pat.sub("", main, count=1)
        # 2) srcdoc 赋值行
        main = cut_once(main, ASSIGN_FMT % (frame, const), "%s 的 srcdoc 赋值" % frame)
        # 3) iframe -> 链接卡片
        ppat = re.compile(PANE_FMT % (frame[:-5], frame))
        if len(ppat.findall(main)) != 1:
            die("标签页 pane-%s 里的 <iframe id=\"%s\"> 应恰好一个且形态如预期" % (frame[:-5], frame))
        card = CARD_FMT % (bid, label, URLS[bid])
        main = ppat.sub(lambda m: m.group(1) + card + m.group(2), main, count=1)
        frag = build(neutralize(sub, const), max_chars, "子页面 %s" % bid)
        frag = strip_webfont(frag, "子页面 %s" % bid)
        out[bid] = (frag, {"from_constant": const, "constant_literal_chars": len(hits[0]),
                           "decoded_doc_chars": len(sub),
                           "decoded_doc_sha256": hashlib.sha256(sub.encode("utf-8")).hexdigest()})
    # 4) aiframe 自适应高度代码
    main = cut_once(main, FIT, "aiframe 自适应高度代码")
    # 5) 主页自检：不残留 iframe、常量、srcdoc 赋值与对两个框的脚本引用；标签页与切换函数都还在
    #    （样式表里 .aiframe / #aiframe 几条规则与注释原样留着，已无元素命中）
    for bad in ("<iframe", "AI_HTML", "EAL_HTML", ".srcdoc", "contentDocument",
                "getElementById('aiframe')", "getElementById('ealframe')",
                'getElementById("aiframe")', 'getElementById("ealframe")'):
        if bad in main:
            die("删改后的主页仍残留「%s」" % bad)
    if CS_ANY.search(main):
        die("主页带 color-scheme 的 meta，build() 会把它去掉（需专用处理）")
    for need, n in (("window.showTab=function(t){document.querySelectorAll('.pane').forEach(", 1), ('<div id="pane-ai" class="pane" hidden>', 1),
                    ('<div id="pane-eal" class="pane" hidden>', 1), ("onclick=\"showTab('ai')\"", 1),
                    ("onclick=\"showTab('eal')\"", 1), ("data-split-link=", 2)):
        if main.count(need) != n:
            die("主页里「%s」应恰好 %d 处，实际 %d 处" % (need, n, main.count(need)))
    frag = build(main, max_chars, "主页 %s" % MAIN_ID)
    frag = strip_webfont(frag, "主页 %s" % MAIN_ID)
    for bid in (AI_ID, EAL_ID):
        if frag.count('href="%s" target="_blank" rel="noopener"' % URLS[bid]) != 1:
            die("主页片段里指向 %s 的链接不是恰好一处" % bid)
    out[MAIN_ID] = (frag, {"links": {AI_ID: URLS[AI_ID], EAL_ID: URLS[EAL_ID]},
                           "removed_chars": len(html) - len(main)})
    for bid, (f, _) in out.items():
        if len(f) > max_chars:  # build() 已查过；这里再守一道，防 build() 的口径日后改变
            die("%s 片段 %d 字符，超过通读上限 %d" % (bid, len(f), max_chars))
        if f.encode("utf-8").decode("utf-8") != f:
            die("%s 片段无法按 UTF-8 写出" % bid)
    return out


def check_registry(brain):
    """hosted-pages.json 若在，三个地址必须与本文件里写的一致（防链接指到别的页）。不在则不查。"""
    p = os.path.join(brain, ".tmp", "artifact-publish", "hosted-pages.json")
    if not os.path.isfile(p):
        return
    try:
        reg = json.load(open(p, encoding="utf-8"))
    except ValueError as ex:
        die("hosted-pages.json 读不出来：%s" % ex)
    for bid, url in URLS.items():
        got = (reg.get(bid) or {}).get("url")
        if got != url:
            die("托管页地址与 hosted-pages.json 不一致：%s 本工具 %s ≠ 登记 %s" % (bid, url, got))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src")
    ap.add_argument("--max-chars", type=int, default=300000)
    a = ap.parse_args()
    brain = artifact_fragment.brain_root()
    src = os.path.expanduser(a.src) if a.src else default_src(brain)
    if not os.path.isfile(src):
        die("原件不存在：%s" % src)
    raw = open(src, "rb").read()
    try:
        html = raw.decode("utf-8")
    except UnicodeDecodeError as ex:
        die("原件不是 UTF-8：%s" % ex)
    check_registry(brain)
    pages = split(html, a.max_chars)
    src_sha = hashlib.sha256(raw).hexdigest()
    mans = {}
    for bid in (MAIN_ID, AI_ID, EAL_ID):
        frag, extra = pages[bid]
        man = {"id": bid, "source": a.src or "Claude/" + DEFAULT_SRC, "source_sha256": src_sha,
               "artifact_sha256": hashlib.sha256(frag.encode("utf-8")).hexdigest(), "artifact_chars": len(frag),
               "hosted_url": URLS[bid], "split_of": MAIN_ID}
        man.update(extra)
        mans[bid] = json.dumps(man, ensure_ascii=False, indent=1) + "\n"
    # —— 以下才开始写盘（三页都已算完、查完）——
    base = os.path.join(brain, ".tmp", "artifact-publish")
    for bid in (MAIN_ID, AI_ID, EAL_ID):
        out = os.path.join(base, bid)
        os.makedirs(out, exist_ok=True)
        open(os.path.join(out, "artifact.html"), "w", encoding="utf-8").write(pages[bid][0])
        open(os.path.join(out, "manifest.json"), "w", encoding="utf-8").write(mans[bid])
    sha = lambda bid: hashlib.sha256(pages[bid][0].encode("utf-8")).hexdigest()[:8]
    print("split ok · main %d chars sha %s · ai %d chars sha %s · eal %d chars sha %s · source %d chars sha %s" % (
        len(pages[MAIN_ID][0]), sha(MAIN_ID), len(pages[AI_ID][0]), sha(AI_ID),
        len(pages[EAL_ID][0]), sha(EAL_ID), len(html), src_sha[:8]))


if __name__ == "__main__":
    main()
