#!/usr/bin/env python3
"""
gitcheck.py — 纯文本 git 同步状态核验（brain-resume Step 3.5 配套）
只读 .git/ 目录（index/HEAD/对象库/logs/HEAD/refs），绝不执行任何 git 子命令。
用法: python3 gitcheck.py <repo1> [repo2 ...]
     每个 repo 输出: HEAD 摘要 / staged 判定（index tree vs HEAD tree）/
     worktree 内容级改动文件 / 未 push 判定 / 最近 commit 列表 / 未跟踪文件前 15 行。
局限: pack 里的 delta 对象会拒读（commit/tree 极少 delta）;
     .gitignore 规则不解析，未跟踪列表需人眼过滤。
"""
import os, sys, struct, zlib, hashlib

def read_loose(gitdir, sha):
    p = os.path.join(gitdir, 'objects', sha[:2], sha[2:])
    if os.path.exists(p):
        return zlib.decompress(open(p, 'rb').read())
    return None

def read_pack_single(gitdir, sha):
    packdir = os.path.join(gitdir, 'objects', 'pack')
    if not os.path.isdir(packdir):
        return None
    for idxname in sorted(os.listdir(packdir)):
        if not idxname.endswith('.idx'):
            continue
        idxdata = open(os.path.join(packdir, idxname), 'rb').read()
        if idxdata[:4] != b'\xfftOc':
            continue
        ver = struct.unpack('>I', idxdata[4:8])[0]
        if ver != 2:
            continue
        fan = struct.unpack('>256I', idxdata[8:8 + 1024])
        b = int(sha[:2], 16)
        lo = fan[b - 1] if b > 0 else 0
        hi = fan[b]
        n = fan[255]
        start = 8 + 1024
        target = bytes.fromhex(sha)
        found = None
        for i in range(lo, hi):
            s = idxdata[start + i * 20: start + (i + 1) * 20]
            if s == target:
                found = i
                break
        if found is None:
            continue
        off_base = start + n * 20
        off = struct.unpack('>I', idxdata[off_base + found * 4: off_base + found * 4 + 4])[0]
        if off & 0x80000000:
            big_idx = off & 0x7fffffff
            big_base = off_base + n * 4
            off = struct.unpack('>Q', idxdata[big_base + big_idx * 8: big_base + big_idx * 8 + 8])[0]
        pack = open(os.path.join(packdir, idxname[:-4] + '.pack'), 'rb').read()
        b0 = pack[off]
        typ = (b0 >> 4) & 7
        sz = b0 & 15
        shift = 4
        i = off + 1
        while True:
            b = pack[i]; i += 1
            sz |= (b & 0x7f) << shift
            shift += 7
            if not (b & 0x80):
                break
        if typ in (6, 7):
            raise RuntimeError('pack delta object, cannot verify: ' + sha)
        return zlib.decompressobj().decompress(pack[i:])
    return None

def read_obj(gitdir, sha):
    return read_loose(gitdir, sha) or read_pack_single(gitdir, sha)

def resolve_head(gitdir):
    head = open(os.path.join(gitdir, 'HEAD')).read().strip()
    if head.startswith('ref: '):
        ref = head[5:]
        p = os.path.join(gitdir, ref)
        if os.path.exists(p):
            return open(p).read().strip()
        pr = os.path.join(gitdir, 'packed-refs')
        if os.path.exists(pr):
            for line in open(pr):
                line = line.strip()
                if line.endswith(ref):
                    return line.split()[0]
    return head

def commit_tree_sha(data):
    nul = data.index(b'\x00')
    rest = data[nul + 1:]
    end = rest.index(b'\n\n') if b'\n\n' in rest else len(rest)
    for line in rest[:end].decode().split('\n'):
        if line.startswith('tree '):
            return line[5:]
    return None

def parse_index(gitdir):
    data = open(os.path.join(gitdir, 'index'), 'rb').read()
    assert data[:4] == b'DIRC'
    ver, n = struct.unpack('>II', data[4:12])
    off = 12
    entries = []
    for i in range(n):
        if ver in (2, 3):
            (csec, cnsec, msec, mnsec, dev, ino, mode, uid, gid, size) = struct.unpack('>IIIIIIIIII', data[off:off+40])
            sha = data[off+40:off+60]
            flags = struct.unpack('>H', data[off+60:off+62])[0]
            nl = flags & 0x0FFF
            base = 62 if ver == 2 else 64
            name_start = off + base
        else:
            raise RuntimeError('index ver %d unsupported' % ver)
        if nl == 0x0FFF:
            nl = struct.unpack('>I', data[name_start:name_start+4])[0]
            name_start += 4
            base += 4
        name = data[name_start:name_start+nl].decode('utf-8', 'replace')
        entry_len = base + nl + 1  # +1 = NUL 终止符
        if entry_len % 8:
            entry_len += 8 - (entry_len % 8)
        entries.append({'mode': mode, 'sha': sha, 'mtime': msec, 'size': size, 'name': name})
        off += entry_len
    return entries

def tree_entry_sha(entries_in_dir):
    content = b''
    for e in sorted(entries_in_dir, key=lambda x: x['name'] + ('/' if x['mode'] == 0o40000 else '')):
        content += ('%o' % e['mode']).encode() + b' ' + e['name'].encode() + b'\x00' + e['sha']
    return hashlib.sha1(b'tree %d\x00' % len(content) + content).digest()

def index_nested_tree(entries):
    def build(subentries):
        out, dirs = [], {}
        for e in subentries:
            if '/' in e['name']:
                d, rest = e['name'].split('/', 1)
                dirs.setdefault(d, []).append(dict(e, name=rest))
            else:
                out.append(e)
        for d, children in dirs.items():
            out.append({'mode': 0o40000, 'name': d, 'sha': build(children)})
        return tree_entry_sha(out)
    return build(entries).hex()

def blob_hash(path):
    content = open(path, 'rb').read()
    return hashlib.sha1(b'blob %d\x00' % len(content) + content).hexdigest()

def unpushed(gitdir):
    """比较 refs/heads/* 与 refs/remotes/*/*；无远端返回 None"""
    heads_dir = os.path.join(gitdir, 'refs', 'heads')
    remotes_dir = os.path.join(gitdir, 'refs', 'remotes')
    heads = {}
    for root, dirs, files in os.walk(heads_dir):
        for f in files:
            p = os.path.join(root, f)
            rel = os.path.relpath(p, heads_dir)
            heads[rel] = open(p).read().strip()
    remotes = {}
    if os.path.isdir(remotes_dir):
        for root, dirs, files in os.walk(remotes_dir):
            for f in files:
                p = os.path.join(root, f)
                rel = os.path.relpath(p, remotes_dir).split('/', 1)[-1]
                remotes[rel] = open(p).read().strip()
    if not remotes:
        return None
    return [b for b, sha in heads.items() if remotes.get(b) != sha]

def check(repo):
    gitdir = os.path.join(repo, '.git')
    print('=' * 20, repo)
    head_sha = resolve_head(gitdir)
    cobj = read_obj(gitdir, head_sha)
    tree_sha = commit_tree_sha(cobj)
    print('HEAD:', head_sha[:10], 'tree:', tree_sha[:10])
    entries = parse_index(gitdir)
    idx_tree = index_nested_tree(entries)
    print('staged-uncommitted:', 'YES' if idx_tree != tree_sha else 'none')
    idx_map = {e['name']: e for e in entries}
    mods = []
    for e in entries:
        p = os.path.join(repo, e['name'])
        if not os.path.exists(p):
            mods.append(e['name'] + ' [MISSING]')
            continue
        if os.path.islink(p):
            continue
        st = os.stat(p)
        # 挂载层 sub-second mtime 会与 index 整秒缓存误报 → stat 不一致时用内容哈希定夺
        if int(st.st_mtime) != e['mtime'] or st.st_size != e['size']:
            if blob_hash(p) != e['sha'].hex():
                mods.append(e['name'])
    print('worktree modified (内容级): %d' % len(mods), mods[:20] if mods else '')
    up = unpushed(gitdir)
    if up is None:
        print('push 判定: 无远端（本地-only 仓）')
    elif up:
        print('push 判定: 未 push 分支:', up)
    else:
        print('push 判定: 已同步')
    logp = os.path.join(gitdir, 'logs', 'HEAD')
    if os.path.exists(logp):
        print('recent commits:')
        for l in open(logp).read().strip().split('\n')[-4:]:
            parts = l.split('\t')
            if len(parts) >= 2:
                print('  ', parts[-1])
    untracked = []
    for root, dirs, files in os.walk(repo):
        if '.git' in dirs:
            dirs.remove('.git')
        for f in files:
            rel = os.path.relpath(os.path.join(root, f), repo)
            if rel not in idx_map:
                untracked.append(rel)
    print('untracked (未过滤 ignore) %d:' % len(untracked))
    for u in sorted(untracked)[:15]:
        print('   ?', u)
    print()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    for repo in sys.argv[1:]:
        try:
            check(os.path.expanduser(repo))
        except Exception as ex:
            print('ERROR %s: %s' % (repo, ex))
