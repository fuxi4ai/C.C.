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
  ps -Ao pid,command | grep -E '[g]it ' || true
  echo "   （多半是某编辑器的 Git 集成在后台。等它结束、或关掉后重试）"
  exit 2
fi

# 2. 无 git 进程 → index.lock 是残留，安全清理
if [ -f .git/index.lock ]; then
  echo "🔓 清理 stale 锁: $REPO/.git/index.lock"
  rm -f .git/index.lock
fi

# 3. 提交
git add -- "$@"
git commit -m "$MSG"
git push
echo "✅ 提交并推送完成: $MSG"
