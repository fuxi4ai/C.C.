#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""技能版本治理（2026-11-04 Doctor 立）：账号放薄壳，正文读 canonical；安全靠版本比对，不依赖运行时「读不到就停」。

正文版本＝canonical 技能目录的内容哈希（含附属文件），改了内容就是新版本，不靠人记得改号。
只改正文无需重传。须重传的只有：账号不是薄壳、壳内容与当前应有内容不符（含 description 变化）。
发布台账 .skills/_release_ledger.jsonl 记录发布过的版本。注册表写 "account": "full" 的技能放完整副本。

  python3 skill_release.py status [--brief]   # 退出码 0=全部同步 1=有待处理 2=账号副本读不到 3=检查本身出错
  python3 skill_release.py release            # 同步 portable、重打 .skill、记台账、产出待上传 zip
  python3 skill_release.py record-current     # 把 canonical 现状记入台账，不改其他文件（初始化用）
环境变量：DOCS_DIR（默认按脚本位置推算）、SKILL_ACCOUNT_DIR（默认取最新的账号技能目录）、SKILL_CODE_DIR（默认 ~/.claude/skills）
"""
from __future__ import annotations

import datetime, glob, hashlib, importlib.util, io, json, os, pathlib, re, shutil, sys, zipfile

HERE = pathlib.Path(__file__).resolve().parent
BRAIN = pathlib.Path(os.environ["DOCS_DIR"]) / "Claude/brain" if os.environ.get("DOCS_DIR") else HERE.parent
SKILLS = BRAIN / ".skills"
PORTABLE = BRAIN / "portable/skills"
LEDGER = SKILLS / "_release_ledger.jsonl"
OUT = BRAIN.parent / "临时文件/skill-stub"
SYNCED = "已同步"
STUB_MARKER = b"<!-- skill-stub:"
STUB_BODY = """
<!-- skill-stub: 正文真源在 brain/.skills，勿在此写正文 -->

# {name}（薄壳）

本文件不含流程。先读正文，再严格按正文执行，不要凭记忆或本文件的描述行事。

1. 按顺序找第一个存在的正文文件，用能读到本机 Mac 文件的工具读取（有 `device_bash` 时用它 `cat`，云端容器内的 Read 读不到 Mac）：
   - `~/Documents/Claude/brain/.skills/{src}/SKILL.md`
   - `$HOME/mnt/Documents/Claude/brain/.skills/{src}/SKILL.md`
   - `$HOME/mnt/Brain/.skills/{src}/SKILL.md`
   - `$HOME/mnt/brain/.skills/{src}/SKILL.md`
2. 读到后，正文的路径若写 `~/Documents/...` 而本环境不存在，换成上一步实际命中的根目录；正文提到同目录文件时，以正文所在目录为基准。
3. 全部读不到：报告「技能正文不可达：{name}」并列出已试路径，然后停止。
"""


CHANNELS = {"release", "code-only", "canonical-only", "portable-only"}


def registry():
    skills = json.loads((SKILLS / "_registry.json").read_text(encoding="utf-8"))["skills"]
    bad = [f"{s}={c.get('channel')}" for s, c in skills.items() if c.get("channel") not in CHANNELS]
    if bad:
        raise ValueError("注册表 channel 不合法：" + "、".join(bad))
    return skills


def account_root():
    env = os.environ.get("SKILL_ACCOUNT_DIR")
    if env is not None:
        return pathlib.Path(env) if env and pathlib.Path(env).is_dir() else None
    roots = [pathlib.Path(p) for p in glob.glob(os.path.expanduser(
        "~/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/*/*/skills"))]
    return max(roots, key=lambda p: p.stat().st_mtime) if roots else None


def rename_fm(raw: bytes, old: str, new: str) -> bytes:
    """只改 frontmatter 的 name 行，兼容带引号与不带引号。"""
    if old == new:
        return raw
    return re.sub(rf'^name:\s*["\']?{re.escape(old)}["\']?\s*$'.encode(), f'name: "{new}"'.encode(), raw, count=1, flags=re.M)


def keep(rel: pathlib.PurePath) -> bool:
    return rel.name != ".DS_Store" and not re.search(r"\.bak(_|$)", rel.name) and "__pycache__" not in rel.parts


def dir_tree(root: pathlib.Path) -> dict:
    if not root.is_dir():
        return {}
    return {p.relative_to(root).as_posix(): p.read_bytes() for p in sorted(root.rglob("*"))
            if p.is_file() and keep(p.relative_to(root))}


def pack_tree(src: str) -> dict:
    """读 .skill 成员。包内顶层目录可能是 <名>/，旧包也可能直接在根。"""
    pkg = SKILLS / f"{src}.skill"
    if not pkg.is_file():
        return {}
    out = {}
    with zipfile.ZipFile(pkg) as z:
        for n in z.namelist():
            if n.endswith("/"):
                continue
            rel = n[len(src) + 1:] if n.startswith(f"{src}/") else f"__root__/{n}"
            out[rel] = z.read(n)
    return out


def digest(tree: dict) -> str:
    """版本号：SKILL.md 去末端换行后与附属文件一起算，上传造成的末端空行差异不算新版本。"""
    h = hashlib.sha256()
    for rel in sorted(tree):
        data = tree[rel].rstrip(b"\n") if rel == "SKILL.md" else tree[rel]
        h.update(rel.encode() + b"\0" + data + b"\0")
    return h.hexdigest()


def ledger_versions():
    seen = {}
    if LEDGER.is_file():
        for line in LEDGER.read_text(encoding="utf-8").splitlines():
            if line.strip():
                row = json.loads(line)
                seen.setdefault(row["skill"], set()).add(row["sha256"])
    return seen


def frontmatter(raw: bytes) -> bytes:
    end = raw.find(b"\n---", 3)
    return raw[:end + 4] if raw.startswith(b"---") and end != -1 else b""


def stub_bytes(src: str, name: str, canon: bytes) -> bytes:
    head = rename_fm(frontmatter(canon), src, name)
    return head + b"\n" + STUB_BODY.format(name=name, src=src).encode()


def code_link_problem(src):
    code = pathlib.Path(os.environ.get("SKILL_CODE_DIR") or os.path.expanduser("~/.claude/skills"))
    if not code.is_dir():
        return None  # 云端或沙箱没有这个目录，属预期
    name = "qa" if src == "QA" else src
    link = code / name
    if not link.is_symlink():
        return "Code 链接缺失或不是链接"
    target = link.resolve()
    if target not in ((PORTABLE / src).resolve(), (SKILLS / src).resolve()):
        return "Code 链接指向不对"
    return None


def state_of(src, cfg, root, seen):
    tree = dir_tree(SKILLS / src)
    canon = tree.get("SKILL.md")
    if canon is None:
        return "canonical 缺失"
    if cfg.get("portable") and dir_tree(PORTABLE / src) != tree:
        return "待发布"
    if pack_tree(src) != tree:
        return "待发布"
    cur = digest(tree)
    if cur not in seen.get(src, set()):
        return "待发布"
    if root is None:
        return "账号未核"
    state = account_state(src, cfg, root, seen, tree, canon, cur)
    if state == SYNCED and (cfg.get("portable") or src == "QA"):
        return code_link_problem(src) or SYNCED
    return state


def account_state(src, cfg, root, seen, tree, canon, cur):
    name = cfg.get("account_name", src)
    acc_tree = dir_tree(root / name)
    acc = acc_tree.get("SKILL.md")
    if acc is None:
        return "待上传（账号缺失）"
    if cfg.get("account", "stub") == "full":
        norm_tree = {**acc_tree, "SKILL.md": rename_fm(acc, name, src)}
        a = digest(norm_tree)
        if a == cur:
            return SYNCED
        return "待上传（账号落后）" if a in seen.get(src, set()) else "待上传（账号副本不是任何已发布版本）"
    if STUB_MARKER not in acc:
        return "待上传（账号还不是薄壳）"
    if set(acc_tree) != {"SKILL.md"}:
        return "待上传（账号目录有多余文件）"
    if acc.rstrip(b"\n") == stub_bytes(src, name, canon).rstrip(b"\n"):
        return SYNCED
    if rename_fm(frontmatter(acc), name, src) != frontmatter(canon):
        return "待上传（触发描述已变）"
    return "待上传（壳内容不是最新）"


def unregistered(reg):
    names = set()
    for base in (SKILLS, PORTABLE):
        if base.is_dir():
            names |= {d.name for d in base.iterdir() if d.is_dir() and (d / "SKILL.md").is_file()
                      and not d.name.startswith(("_", "."))}
    return sorted(names - set(reg))


def status(brief=False):
    reg, root, seen = registry(), account_root(), ledger_versions()
    rows = [(s, state_of(s, c, root, seen)) for s, c in reg.items() if c["channel"] == "release"]
    pending = [(s, st) for s, st in rows if st != SYNCED]
    extra = unregistered(reg)
    if brief:
        msg = f"技能版本：{len(rows) - len(pending)}/{len(rows)} 已同步"
        if pending:
            msg += "；" + "；".join(f"{s} {st}" for s, st in pending)
        if extra:
            msg += "；未登记：" + "、".join(extra)
        print(msg)
    else:
        print(f"账号目录：{root if root else '读不到'}")
        for s, st in rows:
            print(f"{s:<20}{digest(dir_tree(SKILLS / s))[:8]:<10}{st}")
        for s, c in reg.items():
            if c["channel"] != "release":
                print(f"{s:<20}{'—':<10}不发布（{c['channel']}）")
        for s in extra:
            print(f"{s:<20}{'—':<10}未登记：请写入 .skills/_registry.json")
    if extra or any(st != "账号未核" for _, st in pending):
        return 1
    return 2 if pending else 0


def record(src, sha, note):
    row = {"ts": datetime.datetime.now().astimezone().isoformat(timespec="seconds"),
           "skill": src, "version": f"{datetime.date.today().isoformat()}-{sha[:8]}", "sha256": sha, "note": note}
    with LEDGER.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


def record_current():
    reg, seen = registry(), ledger_versions()
    for s, c in reg.items():
        tree = dir_tree(SKILLS / s)
        if c["channel"] == "release" and "SKILL.md" in tree and digest(tree) not in seen.get(s, set()):
            record(s, digest(tree), "初始化")
    return status()


def check_valid(src, raw):
    # yaml 依赖只有发布时才需要，status 不受它影响
    spec = importlib.util.spec_from_file_location("parity", HERE / "check_skill_parity.py")
    parity = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(parity)
    except SystemExit as e:  # 缺 PyYAML 时 parity 会退出；别和「账号读不到」的退出码 2 混淆
        raise RuntimeError("发布校验需要 PyYAML") from e
    text = raw.decode("utf-8", "replace")
    fm, err = parity.parse_fm(text)
    if err:
        return f"frontmatter 解析失败：{err}"
    if not isinstance(fm, dict):
        return "frontmatter 不是映射"
    if str(fm.get("name", "")).lower() != src.lower():
        return f"name 与目录名不符：{fm.get('name')!r}"
    if not str(fm.get("description", "")).strip():
        return "description 为空"
    if parity.dup_frontmatter(text):
        return "重复 frontmatter 块"
    if STUB_MARKER in raw:
        return "canonical 不得是薄壳"
    return None


def write_zip(path: pathlib.Path, members: dict):
    """先写内存再原子替换，中途失败不留半个包。"""
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        for n, data in members.items():
            z.writestr(n, data)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_bytes(buf.getvalue())
    os.replace(tmp, path)


def release():
    reg, root = registry(), account_root()
    targets = {s: c for s, c in reg.items() if c["channel"] == "release"}
    problems = [f"{s}: {e}" for s in targets
                for e in [check_valid(s, dir_tree(SKILLS / s).get("SKILL.md", b""))] if e]
    if problems:
        print("✗ 未发布，先修：\n  " + "\n  ".join(problems))
        return 1
    seen = ledger_versions()
    for s, c in targets.items():
        tree = dir_tree(SKILLS / s)
        if c.get("portable"):
            pdir = PORTABLE / s
            for rel, data in tree.items():
                dst = pdir / rel
                if not dst.is_file() or dst.read_bytes() != data:
                    dst.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(SKILLS / s / rel, dst)
                    print(f"同步 portable：{s}/{rel}")
            for rel in set(dir_tree(pdir)) - set(tree):
                (pdir / rel).unlink()  # portable 是单向派生，多余文件 git 可回溯
                print(f"移除 portable 多余文件：{s}/{rel}")
        if pack_tree(s) != tree:
            write_zip(SKILLS / f"{s}.skill", {f"{s}/{rel}": data for rel, data in tree.items()})
            print(f"重打包：{s}.skill")
        cur = digest(tree)
        if cur not in seen.get(s, set()):
            record(s, cur, "release")
            seen.setdefault(s, set()).add(cur)
            print(f"记台账：{s} {cur[:8]}")
    # 只清本工具按注册表产出的包，别的文件一律不动
    for c_s, c in targets.items():
        old = OUT / f"{c.get('account_name', c_s)}.zip"
        if old.is_file():
            old.unlink()
    if root is None:
        print("账号目录读不到，无法判断要传哪些，未产出上传包")
        return 2
    upload = []
    for s, c in targets.items():
        st = state_of(s, c, root, seen)
        if not st.startswith("待上传"):
            continue
        name = c.get("account_name", s)
        tree = dir_tree(SKILLS / s)
        if c.get("account", "stub") == "full":
            members = {f"{name}/{rel}": (rename_fm(d, s, name) if rel == "SKILL.md" else d) for rel, d in tree.items()}
        else:
            members = {f"{name}/SKILL.md": stub_bytes(s, name, tree["SKILL.md"])}
        write_zip(OUT / f"{name}.zip", members)
        upload.append(f"{name}.zip")
    print(f"待上传（{len(upload)}）：{OUT}" if upload else "无待上传")
    for u in upload:
        print(f"  {u}")
    return 0


def main():
    args = sys.argv[1:]
    cmd = args[0] if args else "status"
    try:
        if cmd == "status":
            return status("--brief" in args)
        if cmd == "release":
            return release()
        if cmd == "record-current":
            return record_current()
    except Exception as e:  # noqa: BLE001 — 坏数据也要给出一行可读结论
        print(f"技能版本：检查本身出错（{type(e).__name__}: {str(e)[:120]}）")
        return 3
    print(__doc__)
    return 3


if __name__ == "__main__":
    sys.exit(main())
