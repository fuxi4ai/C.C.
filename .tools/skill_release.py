#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""技能版本治理（2026-11-04 Doctor 立）：账号放薄壳，正文读 canonical；安全靠版本比对，不依赖运行时「读不到就停」。

正文版本＝canonical SKILL.md 的内容哈希，改了内容就是新版本，不靠人记得改号；只改正文无需重传。
须重传的只有三种：壳版本落后（STUB_VERSION）、触发描述变了（frontmatter）、账号不是薄壳。
发布台账 .skills/_release_ledger.jsonl 记录每个发布过的正文版本。注册表写 "account": "full" 的技能放完整副本。

  python3 skill_release.py status [--brief]   # 退出码 0=全部同步 1=有待处理 2=账号副本读不到
  python3 skill_release.py release            # 同步 portable、重打 .skill、记台账、产出待上传 zip
  python3 skill_release.py record-current     # 把 canonical 现状记入台账，不改其他文件（初始化用）
环境变量：DOCS_DIR（默认 ~/Documents）、SKILL_ACCOUNT_DIR（默认取最新的账号技能目录）
"""
from __future__ import annotations

import datetime, glob, hashlib, importlib.util, json, os, pathlib, shutil, sys, zipfile

HERE = pathlib.Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("parity", HERE / "check_skill_parity.py")
parity = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(parity)

DOCS = pathlib.Path(os.environ.get("DOCS_DIR") or os.path.expanduser("~/Documents"))
BRAIN = DOCS / "Claude/brain"
SKILLS = BRAIN / ".skills"
PORTABLE = BRAIN / "portable/skills"
LEDGER = SKILLS / "_release_ledger.jsonl"
OUT = DOCS / "Claude/临时文件/skill-release"
SYNCED = "已同步"
STUB_VERSION = "2"
STUB_BODY = """
<!-- skill-stub: v{ver} 正文真源在 brain/.skills，勿在此写正文 -->

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


def frontmatter(raw: bytes, account_name=None, src=None) -> str:
    text = raw.decode("utf-8", "replace")
    if account_name and src and account_name != src:
        text = text.replace(f'name: "{account_name}"', f'name: "{src}"', 1)
    end = text.find("\n---", 3)
    return text[:end + 4] if text.startswith("---") and end != -1 else ""


def stub_text(src: str, name: str, canon: bytes) -> str:
    head = frontmatter(canon)
    if name != src:
        head = head.replace(f'name: "{src}"', f'name: "{name}"', 1)
    return head + "\n" + STUB_BODY.format(ver=STUB_VERSION, name=name, src=src)


def registry():
    return json.loads((SKILLS / "_registry.json").read_text(encoding="utf-8"))["skills"]


def account_root():
    env = os.environ.get("SKILL_ACCOUNT_DIR")
    if env is not None:
        return pathlib.Path(env) if env and pathlib.Path(env).is_dir() else None
    roots = [pathlib.Path(p) for p in glob.glob(os.path.expanduser(
        "~/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/*/*/skills"))]
    return max(roots, key=lambda p: p.stat().st_mtime) if roots else None


def norm(raw: bytes, account_name: str | None = None, src: str | None = None) -> str:
    """比较前归一：末端空白行；账号名与目录名大小写不同的还原 name 行。"""
    text = raw.decode("utf-8", "replace").rstrip("\n")
    if account_name and src and account_name != src:
        text = text.replace(f'name: "{account_name}"', f'name: "{src}"', 1)
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def read(p: pathlib.Path):
    return p.read_bytes() if p.is_file() else None


def ledger_versions():
    seen = {}
    if LEDGER.is_file():
        for line in LEDGER.read_text(encoding="utf-8").splitlines():
            if line.strip():
                row = json.loads(line)
                seen.setdefault(row["skill"], set()).add(row["sha256"])
    return seen


def pack_files(src: str):
    root = SKILLS / src
    for p in sorted(root.rglob("*")):
        if p.is_file() and p.name != ".DS_Store" and ".bak" not in p.name and "__pycache__" not in p.parts:
            yield p, p.relative_to(root)


def pack_skill_md(src: str):
    pkg = SKILLS / f"{src}.skill"
    if not pkg.is_file():
        return None
    with zipfile.ZipFile(pkg) as z:
        for n in z.namelist():
            if n.endswith("/SKILL.md") and n.count("/") == 1:
                return z.read(n)
    return None


def state_of(src, cfg, root, seen):
    canon = read(SKILLS / src / "SKILL.md")
    if canon is None:
        return "canonical 缺失"
    cur = norm(canon)
    if cfg.get("portable"):
        if norm(read(PORTABLE / src / "SKILL.md") or b"") != cur:
            return "待发布"
    pkg = pack_skill_md(src)
    if pkg is None or norm(pkg) != cur:
        return "待发布"
    if cur not in seen.get(src, set()):
        return "待发布"
    if root is None:
        return "账号未核"
    name = cfg.get("account_name", src)
    acc = read(root / name / "SKILL.md")
    if acc is None:
        return "待上传（账号缺失）"
    if cfg.get("account", "stub") == "full":
        a = norm(acc, name, src)
        if a == cur:
            return SYNCED
        return "待上传（账号落后）" if a in seen.get(src, set()) else "待上传（账号副本不是任何已发布版本）"
    if parity.STUB_MARKER not in acc:
        return "待上传（账号还不是薄壳）"
    if f"skill-stub: v{STUB_VERSION} ".encode() not in acc:
        return "待上传（壳版本落后）"
    if frontmatter(acc, name, src) != frontmatter(canon):
        return "待上传（触发描述已变）"
    if f".skills/{src}/SKILL.md".encode() not in acc:
        return "待上传（壳指向错误）"
    return SYNCED


def unregistered(reg):
    names = set()
    if SKILLS.is_dir():
        names = {d.name for d in SKILLS.iterdir() if d.is_dir() and (d / "SKILL.md").is_file()
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
            cur = read(SKILLS / s / "SKILL.md")
            print(f"{s:<20}{(hashlib.sha256(cur).hexdigest()[:8] if cur else '—'):<10}{st}")
        for s, c in reg.items():
            if c["channel"] != "release":
                print(f"{s:<20}{'—':<10}不发布（{c['channel']}）")
        for s in extra:
            print(f"{s:<20}{'—':<10}未登记：请写入 .skills/_registry.json")
    if extra or any(st != "账号未核" for _, st in pending):
        return 1
    return 2 if pending else 0


def record(src, sha, note):
    SKILLS.mkdir(parents=True, exist_ok=True)
    row = {"ts": datetime.datetime.now().astimezone().isoformat(timespec="seconds"),
           "skill": src, "version": f"{datetime.date.today().isoformat()}-{sha[:8]}", "sha256": sha, "note": note}
    with LEDGER.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


def record_current():
    reg, seen = registry(), ledger_versions()
    for s, c in reg.items():
        raw = read(SKILLS / s / "SKILL.md")
        if c["channel"] == "release" and raw is not None and norm(raw) not in seen.get(s, set()):
            record(s, norm(raw), "初始化")
    return status()


def check_valid(src, raw):
    text = raw.decode("utf-8", "replace")
    err = parity.parse_fm(text)[1]
    if err:
        return f"frontmatter 解析失败：{err}"
    if parity.dup_frontmatter(text):
        return "重复 frontmatter 块"
    if parity.STUB_MARKER in raw:
        return "canonical 不得是薄壳"
    return None


def write_pack(path: pathlib.Path, src: str, name: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for p, rel in pack_files(src):
            data = p.read_bytes()
            if rel.name == "SKILL.md" and rel.parent == pathlib.Path(".") and name != src:
                data = data.replace(f'name: "{src}"'.encode(), f'name: "{name}"'.encode(), 1)
            z.writestr(f"{name}/{rel.as_posix()}", data)


def release():
    reg, root = registry(), account_root()
    targets = {s: c for s, c in reg.items() if c["channel"] == "release"}
    problems = [f"{s}: {e}" for s, c in targets.items()
                for e in [check_valid(s, read(SKILLS / s / "SKILL.md") or b"")] if e]
    if problems:
        print("✗ 未发布，先修：\n  " + "\n  ".join(problems))
        return 1
    seen = ledger_versions()
    upload = []
    if OUT.is_dir():
        for old in OUT.glob("*.zip"):
            old.unlink()  # 本工具自己的产物；清掉上一轮，目录里只留这次要传的
    for s, c in targets.items():
        raw = read(SKILLS / s / "SKILL.md")
        cur = norm(raw)
        if c.get("portable"):
            for p, rel in pack_files(s):
                dst = PORTABLE / s / rel
                if read(dst) != p.read_bytes():
                    dst.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(p, dst)
                    print(f"同步 portable：{s}/{rel}")
        pkg = pack_skill_md(s)
        if pkg is None or norm(pkg) != cur:
            write_pack(SKILLS / f"{s}.skill", s, s)
            print(f"重打包：{s}.skill")
        if cur not in seen.get(s, set()):
            record(s, cur, "release")
            seen.setdefault(s, set()).add(cur)
            print(f"记台账：{s} {cur[:8]}")
        if state_of(s, c, root, seen) != SYNCED:
            name = c.get("account_name", s)
            if c.get("account", "stub") == "full":
                write_pack(OUT / f"{name}.zip", s, name)
            else:
                OUT.mkdir(parents=True, exist_ok=True)
                with zipfile.ZipFile(OUT / f"{name}.zip", "w", zipfile.ZIP_DEFLATED) as z:
                    z.writestr(f"{name}/SKILL.md", stub_text(s, name, raw))
            upload.append(f"{name}.zip")
    print(f"待上传（{len(upload)}）：{OUT}" if upload else "无待上传")
    for u in upload:
        print(f"  {u}")
    return 0


def main():
    args = sys.argv[1:]
    cmd = args[0] if args else "status"
    if cmd == "status":
        return status("--brief" in args)
    if cmd == "release":
        return release()
    if cmd == "record-current":
        return record_current()
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main())
