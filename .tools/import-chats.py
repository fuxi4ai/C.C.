#!/usr/bin/env python3
"""
import-chats.py — 把 Claude Code / Cowork 的 session jsonl 导成 brain/chats/code/ 下的 markdown

用法：
  import-chats.py                    # 列出可导的 session（不写文件）
  import-chats.py --all              # 全部导入
  import-chats.py --session <uuid>   # 只导某个 session
  import-chats.py --since 2026-05-13 # 只导该日期之后的

数据源：
  ~/.claude/projects/<mangled-path>/<session-uuid>.jsonl

输出：
  ~/Documents/Claude/brain/chats/code/<date>-<ai-title-or-uuid8>.md
  含 frontmatter + 用户/助手对话的清洁 markdown
"""
import os
import json
import sys
import argparse
import re
from pathlib import Path
from datetime import datetime

HOME = Path(os.path.expanduser("~"))

# 优先级：env var > Mac 路径 > 沙箱 mnt 路径
def _detect_src():
    env = os.environ.get("CLAUDE_CHATS_SRC")
    if env and Path(env).exists():
        return Path(env)
    for cand in [HOME / ".claude" / "projects", HOME / "mnt" / ".claude" / "projects"]:
        if cand.exists():
            return cand
    return HOME / ".claude" / "projects"  # 默认（不存在时报错）

def _detect_dst():
    env = os.environ.get("BRAIN_ROOT")
    if env:
        return Path(env) / "chats" / "code"
    for cand in [HOME / "Documents" / "Claude" / "brain",
                 HOME / "mnt" / "Documents" / "Claude" / "brain"]:
        if cand.exists():
            return cand / "chats" / "code"
    return HOME / "Documents" / "Claude" / "brain" / "chats" / "code"

SRC_ROOT = _detect_src()
DST_ROOT = _detect_dst()

def slugify(text, maxlen=40):
    """把 ai-title 转成文件名安全的 slug"""
    if not text:
        return ""
    text = re.sub(r'[\\/:*?"<>|]', '-', text)
    text = re.sub(r'\s+', '-', text)
    text = text.strip('-')
    return text[:maxlen]

def parse_session(jsonl_path):
    """读 jsonl 提取 ai_title + 时间戳范围 + 对话条目"""
    ai_title = None
    first_ts = None
    last_ts = None
    turns = []  # [(role, ts, content_str)]

    with open(jsonl_path, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                d = json.loads(line)
            except Exception:
                continue
            t = d.get('type')

            if t == 'ai-title':
                ai_title = d.get('aiTitle')
                continue

            ts = d.get('timestamp')
            if ts:
                if first_ts is None or ts < first_ts:
                    first_ts = ts
                if last_ts is None or ts > last_ts:
                    last_ts = ts

            if t == 'user':
                msg = d.get('message', {})
                content = msg.get('content', '')
                if isinstance(content, list):
                    parts = []
                    for c in content:
                        if c.get('type') == 'text':
                            parts.append(c.get('text', ''))
                        elif c.get('type') == 'tool_result':
                            tr = c.get('content', '')
                            if isinstance(tr, str):
                                parts.append(f"[tool_result] {tr[:200]}")
                    content = '\n'.join(parts)
                if isinstance(content, str) and content.strip():
                    turns.append(('user', ts, content))

            elif t == 'assistant':
                msg = d.get('message', {})
                content = msg.get('content', [])
                if isinstance(content, list):
                    parts = []
                    for c in content:
                        if c.get('type') == 'text':
                            parts.append(c.get('text', ''))
                        elif c.get('type') == 'tool_use':
                            tn = c.get('name', '?')
                            parts.append(f"_[使用工具：{tn}]_")
                    content_str = '\n'.join(p for p in parts if p)
                    if content_str.strip():
                        turns.append(('assistant', ts, content_str))

    return {
        'ai_title': ai_title,
        'first_ts': first_ts,
        'last_ts': last_ts,
        'turns': turns,
        'jsonl_path': jsonl_path,
    }

def fmt_md(session_id, session_data):
    """渲染为 brain 笔记格式"""
    title = session_data['ai_title'] or f"Session {session_id[:8]}"
    date = (session_data['first_ts'] or '')[:10] or datetime.now().strftime('%Y-%m-%d')
    last_date = (session_data['last_ts'] or '')[:10]

    fm = [
        '---',
        f'title: {title}',
        f'tags: [chat, claude-code]',
        f'created: {date}',
        f'updated: {last_date or date}',
        f'status: archived',
        f'type: log',
        f'source: claude-code',
        f'session_id: {session_id}',
        '---',
        '',
        f'# {title}',
        '',
        f'> Claude Code 对话存档 · {date} → {last_date}',
        f'> session: `{session_id}`',
        '',
        '---',
        '',
    ]

    for role, ts, content in session_data['turns']:
        speaker = 'Doctor' if role == 'user' else 'CC'
        # 简化时间戳
        time_part = (ts or '')[11:19] if ts else ''
        fm.append(f'### {speaker}  {time_part}')
        fm.append('')
        fm.append(content.strip())
        fm.append('')

    return '\n'.join(fm)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--all', action='store_true', help='导出全部 session')
    ap.add_argument('--session', help='只导某个 session uuid')
    ap.add_argument('--since', help='只导该日期之后（YYYY-MM-DD）')
    ap.add_argument('--dry-run', action='store_true', help='不写文件，只列')
    args = ap.parse_args()

    if not SRC_ROOT.exists():
        print(f"❌ Claude Code 数据目录不存在：{SRC_ROOT}")
        sys.exit(2)

    # 扫所有 .jsonl
    jsonls = list(SRC_ROOT.rglob('*.jsonl'))
    if not jsonls:
        print(f"⚠️  {SRC_ROOT} 下没找到 .jsonl")
        sys.exit(0)

    # 收集 session 元数据
    sessions = []
    for jp in jsonls:
        sid = jp.stem
        sd = parse_session(jp)
        sessions.append((sid, sd))

    # 排序：最新 first_ts 优先
    sessions.sort(key=lambda x: x[1]['first_ts'] or '', reverse=True)

    # 过滤
    if args.session:
        sessions = [s for s in sessions if args.session in s[0]]
    if args.since:
        sessions = [s for s in sessions if (s[1]['first_ts'] or '')[:10] >= args.since]

    if not sessions:
        print('(过滤后无 session)')
        sys.exit(0)

    # 列表
    if not args.all and not args.session and not args.dry_run:
        print('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')
        print(f'  发现 {len(sessions)} 个 session（数据源：{SRC_ROOT}）')
        print('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')
        for sid, sd in sessions[:20]:
            date = (sd['first_ts'] or '?')[:10]
            title = sd['ai_title'] or '(无标题)'
            turns = len(sd['turns'])
            print(f"  {date}  {sid[:8]}  {turns:3d} 轮  {title[:40]}")
        if len(sessions) > 20:
            print(f"  ... 还有 {len(sessions) - 20} 个")
        print()
        print('选项：')
        print('  --all                  全部导入')
        print(f'  --since {datetime.now().strftime("%Y-%m-%d")}      只导今天')
        print('  --session <uuid 前8位>  只导某个')
        return

    DST_ROOT.mkdir(parents=True, exist_ok=True)

    # 导入
    count = 0
    for sid, sd in sessions:
        date = (sd['first_ts'] or datetime.now().isoformat())[:10]
        slug = slugify(sd['ai_title']) or sid[:8]
        fname = f"{date}-{slug}.md"
        dst = DST_ROOT / fname

        if args.dry_run:
            print(f"  → would write: {dst}  ({len(sd['turns'])} 轮)")
            count += 1
            continue

        if dst.exists():
            print(f"  ⏭️  已存在：{fname}")
            continue

        md = fmt_md(sid, sd)
        dst.write_text(md, encoding='utf-8')
        print(f"  ✅ {fname}  ({len(sd['turns'])} 轮)")
        count += 1

    print()
    print(f'━━ 共处理 {count} 个 session ━━')
    print(f'  输出：{DST_ROOT}')


if __name__ == '__main__':
    main()
