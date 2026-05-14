#!/usr/bin/env bash
# run-graphify.sh — 给 brain 注册项目跑 graphify 生成代码图谱
#
# 用法：
#   bash run-graphify.sh               # 列可跑列表 + 状态
#   bash run-graphify.sh <项目名>      # 跑某一个
#   bash run-graphify.sh --all         # 跑所有有源代码路径的项目
#
# 前置：
#   - graphify 已安装（npm i -g graphify 或源码 build）
#   - 在 PATH 里（建议 ~/.local/bin）

set -euo pipefail

BRAIN="${HOME}/Documents/Claude/brain"

# 项目源码路径映射（与 brain/{项目}/architecture/系统概览.md 的 code_path 一致）
declare -A SRC_PATH=(
  ["DVA"]="${HOME}/Documents/Claude/Projects/DVA"
  ["渊图"]="${HOME}/Documents/Database/行业研究"
  ["龙鱼五力"]="${HOME}/Documents/Claude/Projects/龙鱼五力"
  ["O MY HTML"]="${HOME}/Documents/Claude/Projects/O MY HTML"
)
# 注：海螺姑娘/政治经济学/司南/Optical communication 多为文档类，跳过

ALL=("DVA" "渊图" "龙鱼五力" "O MY HTML")

run_one() {
  local p="$1"
  local src="${SRC_PATH[$p]:-}"
  if [[ -z "$src" ]]; then
    echo "❌ ${p}：无源码路径登记，跳过"
    return 1
  fi
  if [[ ! -d "$src" ]]; then
    echo "❌ ${p}：源码目录不存在 ${src}"
    return 1
  fi
  local dst="${BRAIN}/graphify/${p}"
  mkdir -p "${dst}"
  echo "🔄 ${p}：graphify ${src} → ${dst}"
  if ! command -v graphify &>/dev/null; then
    echo "❌ graphify 未在 PATH。试：export PATH=\"\$PATH:\$HOME/.local/bin\""
    return 1
  fi
  cd "${src}"
  graphify . --obsidian --obsidian-dir "${dst}"
  echo "✅ ${p} 完成"
}

if [[ $# -eq 0 ]]; then
  echo "可跑项目列表（与状态）："
  for p in "${ALL[@]}"; do
    src="${SRC_PATH[$p]}"
    dst="${BRAIN}/graphify/${p}"
    if [[ -d "${dst}" && $(ls "${dst}" 2>/dev/null | wc -l) -gt 0 ]]; then
      echo "  ✅ ${p}  →  ${dst}（已生成）"
    else
      echo "  ⏳ ${p}  →  ${src}（待跑）"
    fi
  done
  echo ""
  echo "用法：bash $0 <项目名>  或  bash $0 --all"
  exit 0
fi

if [[ "$1" == "--all" ]]; then
  for p in "${ALL[@]}"; do
    run_one "$p" || true
    echo ""
  done
  exit 0
fi

run_one "$1"
