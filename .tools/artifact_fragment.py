#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""看板发布片段生成器（2026-11-12 立 · Doctor 批「其余 6 块看板照 X Board 模式迁」）。

定时会话自带的 Artifact 工具会给发布的文件包一层 HTML 外壳（自带 body{margin:0;font:14px …}）。
本工具只读一份完整的看板 HTML 原件，产出去掉外层 <!DOCTYPE>/<html>/<head>/<body> 的片段：
  <浏览器默认值复位 style> + <head 里除 meta/title 外的内容，原样> + <body 行内样式转成的 style> + <body 内容，原样>
- 原件不改不动；输出到 brain/.tmp/artifact-publish/<id>/artifact.html 与 manifest.json。
- 确定性：同一输入 → 同一输出。
- fail-closed（exit 1，不写任何产物）：外层结构不符、<body> 带行内样式以外的属性、含 iframe、
  外链脚本/样式不在托管页允许的来源内、片段超过通读上限。超限或含 iframe 的看板需要各自的拆分器，本工具不硬发。
用法：python3 artifact_fragment.py --src <原件.html> --id <看板 id> [--max-chars 300000]
"""
import argparse, glob, hashlib, json, os, re, sys

# 外壳自带 body{margin:0;font:14px 无衬线}。复位成浏览器默认值，让页面自己的样式照原样生效。
# 复位规则的优先级高于页面里的 *{…}，所以页面若用 *{margin:0} 清边距，复位里就不能再写 margin。
RESET_FONT = "html{font-size:16px}body{font:16px serif}"
STAR_RULE = re.compile(r"(?:^|[}\s,])\*\s*(?:,[^{}]*)?\{([^}]*)\}")
OK_SCRIPT = ("https://cdnjs.cloudflare.com/", "https://cdn.jsdelivr.net/npm/", "https://unpkg.com/",
             "https://cdn.tailwindcss.com", "https://code.jquery.com/", "https://cdn.plot.ly/")
OK_LINK = ("https://fonts.googleapis.com", "https://fonts.gstatic.com")
HEAD = re.compile(r"<head(?:\s[^>]*)?>(.*?)</head>", re.S | re.I)
BODY = re.compile(r"<body(\s[^>]*)?>(.*)</body>", re.S | re.I)
META = re.compile(r'<script type="application/json" id="cowork-artifact-meta">.*?</script>', re.S)


def die(msg):
    sys.exit("fragment FAIL（fail-closed，未写出产物）：" + msg)


def brain_root():
    cands = [os.environ.get("BRAIN_ROOT")] + sorted(glob.glob("/sessions/*/mnt/Documents/Claude/brain")) \
        + [os.path.expanduser("~/Documents/Claude/brain")]
    for c in cands:
        if c and os.path.isdir(os.path.join(c, ".tools")):
            return c
    die("无法定位 brain 根目录")


def build(doc, max_chars):
    h, b = HEAD.search(doc), BODY.search(doc)
    if not h or not b or h.end() > b.start():
        die("找不到 <head>…</head> 与 <body>…</body>")
    pre = re.sub(r"<!doctype html>|<html(?:\s[^>]*)?>", "", META.sub("", doc[:h.start()]), flags=re.I)
    mid = doc[h.end():b.start()]
    post = re.sub(r"</html>", "", doc[b.end():], flags=re.I)
    if pre.strip() or mid.strip() or post.strip():
        die("外层结构里有预期之外的内容")
    head = re.sub(r"<meta\b[^>]*>|<title>[^<]*</title>", "", h.group(1), flags=re.I)
    attrs, body = (b.group(1) or "").strip(), b.group(2)
    body_style = ""
    if attrs:
        m = re.fullmatch(r'style="([^"<>{}]*)"', attrs)
        if not m:
            die("<body> 带行内样式以外的属性：%s" % attrs[:80])
        body_style = "<style>body{%s}</style>\n" % m.group(1)
    css = "\n".join(re.findall(r"<style[^>]*>(.*?)</style>", doc, re.S | re.I))
    star = " ".join(STAR_RULE.findall(css))
    if re.search(r"\bfont(?:-size|-family)?\s*:", star):
        die("页面用 *{…} 设了字体，复位规则会盖掉它（需专用处理）")
    margin = "" if re.search(r"\bmargin\s*:\s*0", star) else "body{margin:8px}"
    reset = "<style>" + RESET_FONT + margin + "</style>"
    # <html lang> 影响中文字形与排版宽度；外壳的 <html> 不带 lang，用一行脚本补回
    lang = re.search(r'<html\b[^>]*\blang="([A-Za-z-]+)"', doc[:h.start()], re.I)
    lang_fix = '<script>document.documentElement.lang="%s"</script>\n' % lang.group(1) if lang else ""
    frag = reset + "\n" + lang_fix + head.strip("\n") + "\n" + body_style + body.strip("\n") + "\n"
    if re.search(r"<iframe\b", frag, re.I):
        die("页面含 iframe，本工具不支持（需专用拆分器）")
    for src in re.findall(r'<script\b[^>]*\bsrc=["\']([^"\']+)', frag, re.I):
        if not src.startswith(OK_SCRIPT):
            die("外链脚本不在托管页允许的来源内：%s" % src[:100])
    for href in re.findall(r'<link\b[^>]*\bhref=["\']([^"\']+)', frag, re.I):
        if not href.startswith(OK_LINK):
            die("外链样式/资源不在托管页允许的来源内：%s" % href[:100])
    if "<!doctype" in frag.lower():
        die("片段里残留 doctype")
    if len(frag) > max_chars:
        die("片段 %d 字符，超过通读上限 %d（需专用拆分器瘦身）" % (len(frag), max_chars))
    return frag


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--id", required=True)
    ap.add_argument("--max-chars", type=int, default=300000)
    a = ap.parse_args()
    if not re.fullmatch(r"[a-z0-9][a-z0-9_-]*", a.id):
        die("看板 id 只能是小写字母、数字、连字符、下划线")
    src = os.path.expanduser(a.src)
    if not os.path.isfile(src):
        die("原件不存在：%s" % src)
    raw = open(src, "rb").read()
    frag = build(raw.decode("utf-8"), a.max_chars)
    out = os.path.join(brain_root(), ".tmp", "artifact-publish", a.id)
    os.makedirs(out, exist_ok=True)
    open(os.path.join(out, "artifact.html"), "w", encoding="utf-8").write(frag)
    man = {"id": a.id, "source": a.src, "source_sha256": hashlib.sha256(raw).hexdigest(),
           "artifact_sha256": hashlib.sha256(frag.encode("utf-8")).hexdigest(), "artifact_chars": len(frag)}
    open(os.path.join(out, "manifest.json"), "w", encoding="utf-8").write(
        json.dumps(man, ensure_ascii=False, indent=1) + "\n")
    print("fragment ok · %s · %d chars · source sha %s · artifact sha %s" % (
        a.id, len(frag), man["source_sha256"][:8], man["artifact_sha256"][:8]))


if __name__ == "__main__":
    main()
