#!/usr/bin/env bash
# git-setup.sh — brain/ git 初始化 + 首推 GitHub
#
# 用法：在 Doctor 的 Mac 终端跑（不要在 Cowork 沙箱跑——沙箱无法管理 .git/index.lock）
#   bash ~/Documents/Claude/brain/.tools/git-setup.sh
#
# 前置条件：
#   - 已建 GitHub 私有仓库：https://github.com/fuxi4ai/C.C..git
#   - macOS Keychain 或 git credential helper 配好（首次 push 会弹出 GitHub 登录）
#
set -euo pipefail

BRAIN="${HOME}/Documents/Claude/brain"
REMOTE="https://github.com/fuxi4ai/C.C..git"

cd "${BRAIN}"

# 0. 清理沙箱遗留的半成品 .git
if [[ -d ".git_partial_REMOVE_ME" ]]; then
  echo "🧹 清理沙箱遗留的 .git_partial_REMOVE_ME"
  rm -rf ".git_partial_REMOVE_ME"
fi

# 1. 已是 git repo 就跳过 init
if [[ -d ".git" ]]; then
  echo "ℹ️  .git 已存在，跳过 init"
else
  echo "🚀 git init -b main"
  git init -b main
fi

# 2. 设置仓库内身份（沿用全局也行）
git config user.name "Doctor"
git config user.email "garciajessicadltis7409@gmail.com"
git config core.quotepath false

# 3. .gitignore 已由 CC 写好

# 4. add + commit（如果还没 commit 过）
if ! git rev-parse HEAD &>/dev/null; then
  echo "📝 首次提交"
  git add -A
  git commit -m "init: brain vault 2026-05-14"$'\n\n''Co-authored by Doctor + CC. Includes:'$'\n''- 8 项目骨架 (DVA/O MY HTML/Optical communication/司南/政治经济学/海螺姑娘/龙鱼五力/渊图)'$'\n''- 4 brain skills (resume/save/note/anchors)'$'\n''- register-project.sh 骨架生成器'
else
  echo "ℹ️  已有 commit 历史，跳过首次提交"
  echo "    若有未追踪文件，自行决定 git add -A && git commit"
fi

# 5. remote add origin
if git remote get-url origin &>/dev/null; then
  CURRENT=$(git remote get-url origin)
  if [[ "${CURRENT}" != "${REMOTE}" ]]; then
    echo "🔄 修正 remote origin：${CURRENT} → ${REMOTE}"
    git remote set-url origin "${REMOTE}"
  else
    echo "ℹ️  origin 已正确"
  fi
else
  echo "🔗 添加 origin"
  git remote add origin "${REMOTE}"
fi

# 6. push
echo ""
echo "📤 推送 main 到 origin（首次会弹 GitHub 登录）"
git push -u origin main

echo ""
echo "✅ brain vault 已上 GitHub"
echo "   仓库：${REMOTE}"
echo "   分支：main"
echo "   commit：$(git log -1 --format='%h - %s')"
