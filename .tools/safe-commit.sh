#!/usr/bin/env bash
# safe-commit.sh — 防 stale 锁的安全提交
# 用法: safe-commit.sh <repo_dir> <commit_msg> <file...>
#
# 逻辑:
#   1. 若有任何 git 进程在跑 → 不动锁、不提交，先报是谁（避免误删别人正持有的锁）
#   2. 无 git 进程时，index.lock 必为残留 → 清掉
#   3. git add 指定文件 → commit → push
# 只 add 显式传入的文件，绝不 -A，防止把别的会话/数灵改动混提（brain 归位铁律）。

set -uo pipefail

REPO="${1:?用法: safe-commit.sh <repo> <msg> <file...>}"; shift
MSG="${1:?需要提交信息}"; shift
if [ "$#" -lt 1 ]; then
  echo "❌ 至少指定一个要提交的文件" >&2
  exit 1
fi

cd "$REPO" || { echo "❌ 进不去 $REPO" >&2; exit 1; }

# 1. 真 git 进程在跑？任何 git 都先让路
if pgrep -x git >/dev/null 2>&1; then
  echo "⚠️  检测到 git 进程在运行，未动锁、未提交。先确认是谁占用："
  pgrep -x git | while read -r _p; do ps -p "$_p" -o pid=,command= 2>/dev/null; done
  echo "   （多半是某编辑器的 Git 集成在后台。等它结束、或关掉后重试）"
  exit 2
fi

# 2. 无 git 进程 → index.lock 是残留，安全清理
if [ -f .git/index.lock ]; then
  echo "🔓 清理 stale 锁: $REPO/.git/index.lock"
  rm -f .git/index.lock
fi

# 3. 提交（逐步把关，任一步失败如实报错，不谎报成功）
git add -- "$@" || { echo "❌ git add 失败" >&2; exit 1; }
git commit -m "$MSG" || { echo "❌ git commit 失败（可能无改动可提交）" >&2; exit 1; }
if git push; then
  echo "✅ 提交并推送完成: $MSG"
else
  echo "⚠️  本地 commit 已完成，但 push 失败（常见：远端领先，需先 git pull --rebase 再推）。本地提交已保留，不会丢。" >&2
  exit 1
fi
