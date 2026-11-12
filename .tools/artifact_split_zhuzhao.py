#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""烛照九阴日报 发布瘦身拆分器（2026-11-12 立 · 配合 artifact_fragment.py 使用）。

原件 zhuzhao-jiuyin-daily.html 约 221 万字符，通用片段生成器按通读上限直接拒绝。
本工具只读原件（不改不动），先瘦身、再交给 artifact_fragment.build() 去壳：
  1. echarts 外置到 CDN：定位唯一的内联 echarts 库 <script> 块（以 Apache 许可注释开头），
     从库源码解析版本号，整块换成 cdnjs 上同版本的 echarts.min.js 外链。
  2. 大图外置：≥ 5 万字符的 data:image/…;base64 写成 assets/<sha256前16位>.<ext>，页面改相对路径；
     小的 data URI（如内嵌字体）保留内联。
  3. 回填校验：外置路径换回原 data URI、CDN 标签换回原库块后，必须与原件逐字节相同。
  4. 瘦身后的完整文档交 artifact_fragment.build() 产出片段（去外层标签、复位样式、补 lang、来源白名单检查）。
- 输出：brain/.tmp/artifact-publish/zhuzhao-jiuyin-daily/ 下的 artifact.html、manifest.json、assets/。
- 确定性：同一输入 → 同一输出（资源按内容寻址命名）。
- fail-closed（exit 1，不写任何产物）：echarts 库块不是恰好一个、解析不到唯一版本号、
  大图类型未知、回填校验不过、build() 拒绝、片段里外链/外置引用数量不符。所有检查都在第一次写盘之前做完。
- 不删任何文件；历史资源留在 assets/ 里，当期清单见 manifest.json。
- 本工具不联网核对 CDN 文件；要核对 cdnjs 那份与内联那份是否等价，在能上网的终端跑 --check-cdn（只读、不写产物）。
用法：python3 artifact_split_zhuzhao.py [--src <原件.html>] [--max-chars 300000]
     python3 artifact_split_zhuzhao.py --check-cdn      下载 CDN 文件与内联库源码比对，只打印结论
"""
import argparse, base64, hashlib, json, os, re, sys

sys.dont_write_bytecode = True  # import 同目录模块时不往 .tools/__pycache__ 里添文件
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import artifact_fragment  # noqa: E402

BOARD_ID = "zhuzhao-jiuyin-daily"
DEFAULT_SRC = "AI4ME/烛照九阴-outputs/artifact/zhuzhao-jiuyin-daily.html"  # 相对 Documents 根
CDN_FMT = "https://cdnjs.cloudflare.com/ajax/libs/echarts/%s/echarts.min.js"
BIG_URI_CHARS = 50000   # 整个 data URI 达到这个字符数才外置
LIB_MIN_CHARS = 200000  # echarts 库块的下限，防止把别的带许可注释的小脚本认成库
EXT = {"image/jpeg": "jpg", "image/png": "png", "image/gif": "gif", "image/webp": "webp", "image/svg+xml": "svg"}
URI = re.compile(r"data:(image/[a-z0-9.+-]+);base64,([A-Za-z0-9+/]+={0,2})")
SCRIPT = re.compile(r"<script\b([^>]*)>(.*?)</script>", re.S | re.I)
# echarts 的 UMD 尾部导出形如 t.version="5.6.0"；库里内含的 zrender 写的是对象键 version:"5.6.1"，不会被这条匹配
VERSION = re.compile(r"""[A-Za-z_$][\w$]*\.version\s*=\s*["'](\d+\.\d+\.\d+)["']""")


def die(msg):
    sys.exit("split FAIL（fail-closed，未写出产物）：" + msg)


def default_src(brain):
    # brain 根是 <Documents>/Claude/brain，原件在 <Documents>/AI4ME/… 下
    return os.path.join(os.path.dirname(os.path.dirname(brain)), DEFAULT_SRC)


def find_echarts(html):
    """返回 (整块起点, 整块终点, 库源码, 版本号)。不是恰好一个库块或解析不到唯一版本号即 fail-closed。"""
    hits = []
    for m in SCRIPT.finditer(html):
        attrs, body = m.group(1), m.group(2)
        if re.search(r"\bsrc\s*=", attrs, re.I) or len(body) < LIB_MIN_CHARS:
            continue
        lead = body.lstrip()[:1500]
        if lead.startswith("/*") and "Apache Software Foundation" in lead and "echarts" in body:
            hits.append(m)
    if len(hits) != 1:
        die("内联 echarts 库脚本块应恰好一个，实际 %d 个" % len(hits))
    m = hits[0]
    vers = sorted(set(VERSION.findall(m.group(2))))
    if len(vers) != 1:
        die("从 echarts 库源码里解析不到唯一版本号（找到：%s）" % (", ".join(vers) or "无"))
    return m.start(), m.end(), m.group(2), vers[0]


def slim_doc(html):
    """完整原件 -> (瘦身后的完整文档, echarts 信息, {相对路径: (原 data URI, 字节)})。"""
    s, e, lib, ver = find_echarts(html)
    block = html[s:e]
    cdn = CDN_FMT % ver
    tag = '<script src="%s"></script>' % cdn
    if tag in html or cdn in html:
        die("原件里已出现同一个 CDN 地址，回填无法保证唯一")
    doc = html[:s] + tag + html[e:]
    assets = {}

    def repl(m):
        if len(m.group(0)) < BIG_URI_CHARS:
            return m.group(0)
        mime = m.group(1)
        if mime not in EXT:
            die("未知的大图类型：%s" % mime)
        try:
            data = base64.b64decode(m.group(2), validate=True)
        except Exception as ex:
            die("大图 base64 解码失败：%s" % ex)
        rel = "assets/%s.%s" % (hashlib.sha256(data).hexdigest()[:16], EXT[mime])
        if rel in html:
            die("外置路径与原件已有文本相撞：%s" % rel)
        if rel in assets and assets[rel][0] != m.group(0):
            die("同一内容的大图出现了两种写法，回填不唯一：%s" % rel)
        assets[rel] = (m.group(0), data)
        return rel

    doc = URI.sub(repl, doc)
    # 回填校验：外置路径换回原 data URI、CDN 标签换回原库块，必须与原件一致
    back = doc
    for rel, (uri, _) in assets.items():
        back = back.replace(rel, uri)
    if back.count(tag) != 1:
        die("瘦身后的文档里 CDN 标签不是恰好一处")
    back = back.replace(tag, block)
    if back != html:
        die("回填校验失败：拆分不可逆")
    info = {"version": ver, "cdn_url": cdn, "inline_block_sha256": hashlib.sha256(block.encode("utf-8")).hexdigest(),
            "inline_block_chars": len(block), "inline_source_sha256": hashlib.sha256(lib.encode("utf-8")).hexdigest(),
            "inline_source_chars": len(lib)}
    return doc, info, assets, lib


def check_cdn(lib, info):
    """联网核对：CDN 文件与内联库源码（去首尾空白后）是否逐字节相同。只打印，不写产物。"""
    import urllib.request
    try:
        got = urllib.request.urlopen(info["cdn_url"], timeout=60).read()
    except Exception as ex:
        sys.exit("check-cdn FAIL：下载不到 %s（%s）" % (info["cdn_url"], ex))
    a, b = got.strip(), lib.encode("utf-8").strip()
    sa, sb = hashlib.sha256(a).hexdigest(), hashlib.sha256(b).hexdigest()
    if a == b:
        print("check-cdn ok · echarts %s · CDN 与内联逐字节相同（去首尾空白后）· %d 字节 · sha %s" % (
            info["version"], len(a), sa[:16]))
        return
    va = sorted(set(VERSION.findall(got.decode("utf-8", "replace"))))
    sys.exit("check-cdn DIFF：CDN %d 字节 sha %s（版本 %s）≠ 内联 %d 字节 sha %s（版本 %s）。"
             "不相同不等于不能用，但需人工确认是否同一构建" % (
                 len(a), sa[:16], ",".join(va) or "?", len(b), sb[:16], info["version"]))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src")
    ap.add_argument("--max-chars", type=int, default=300000)
    ap.add_argument("--check-cdn", action="store_true")
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
    doc, info, assets, lib = slim_doc(html)
    if a.check_cdn:
        check_cdn(lib, info)
        return
    # 去壳。build() 结构不符时自己 fail-closed 退出；此时尚未写过任何文件
    frag = artifact_fragment.build(doc, a.max_chars)
    # 片段自检：外链只应有那一个 CDN 脚本；每张外置图恰好被引用；不残留大号 data URI
    srcs = re.findall(r'<script\b[^>]*\bsrc=["\']([^"\']+)', frag, re.I)
    if srcs != [info["cdn_url"]]:
        die("片段里的外链脚本不是恰好一个 echarts CDN：%s" % srcs)
    for rel in assets:
        if frag.count(rel) < 1:
            die("片段里找不到外置图引用：%s" % rel)
    if any(len(m.group(0)) >= BIG_URI_CHARS for m in URI.finditer(frag)):
        die("片段里仍残留大号 data:image")
    if frag.encode("utf-8").decode("utf-8") != frag:
        die("片段无法按 UTF-8 写出")
    # —— 以下才开始写盘 ——
    out = os.path.join(brain, ".tmp", "artifact-publish", BOARD_ID)
    os.makedirs(os.path.join(out, "assets"), exist_ok=True)
    for rel, (_, data) in sorted(assets.items()):
        p = os.path.join(out, rel)
        if not (os.path.exists(p) and open(p, "rb").read() == data):
            open(p, "wb").write(data)
    open(os.path.join(out, "artifact.html"), "w", encoding="utf-8").write(frag)
    man = {"id": BOARD_ID, "source": a.src or src, "source_sha256": hashlib.sha256(raw).hexdigest(),
           "artifact_sha256": hashlib.sha256(frag.encode("utf-8")).hexdigest(), "artifact_chars": len(frag),
           "echarts": info,
           "assets": {rel: hashlib.sha256(d).hexdigest() for rel, (_, d) in sorted(assets.items())},
           "assets_bytes": {rel: len(d) for rel, (_, d) in sorted(assets.items())}}
    open(os.path.join(out, "manifest.json"), "w", encoding="utf-8").write(
        json.dumps(man, ensure_ascii=False, indent=1) + "\n")
    print("split ok · %s · artifact %d chars sha %s · echarts %s → CDN（内联块 %d chars sha %s）· assets %d · source sha %s" % (
        BOARD_ID, len(frag), man["artifact_sha256"][:8], info["version"], info["inline_block_chars"],
        info["inline_block_sha256"][:8], len(assets), man["source_sha256"][:8]))


if __name__ == "__main__":
    main()
