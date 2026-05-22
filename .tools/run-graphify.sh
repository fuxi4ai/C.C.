#!/usr/bin/env bash
# run-graphify.sh — 给 brain 注册项目跑 graphify 生成代码图谱
#
# 用法：
#   bash run-graphify.sh               列可跑列表 + 状态
#   bash run-graphify.sh <项目名>      跑某一个
#   bash run-graphify.sh --all         跑所有有源代码路径的项目
#
# 兼容：macOS 自带 bash 3.2（不用 associative array）
#
# 前置：
#   - graphify 已安装（v0.7.16+）
#   - 在 PATH 里（建议 ~/.local/bin）
#   - LLM API key 已配（ANTHROPIC_API_KEY 或 KIMI_API_KEY）
#
# 产物：
#   brain/graphify/{项目}/graphify-out/graph.json
#   brain/graphify/{项目}/graphify-out/report.md
#   brain/graphify/{项目}/graphify-out/GRAPH_TREE.html

set -eo pipefail   # 注：去掉 -u 避免 macOS bash 3.x 对 ${VAR:-} 的怪异行为

# 加载本地 env（含 LLM API key，不进 git）
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [ -f "${SCRIPT_DIR}/.env.graphify" ]; then
  # shellcheck source=/dev/null
  source "${SCRIPT_DIR}/.env.graphify"
fi

BRAIN="${HOME}/Documents/Claude/brain"

# 项目源码路径（与 brain/{项目}/architecture/系统概览.md 的 code_path 一致）
get_src_path() {
  case "$1" in
    "DVA")        echo "${HOME}/Documents/Claude/Projects/DVA" ;;
    "渊图")       echo "${HOME}/Documents/Database/行业研究" ;;
    "龙鱼五力")   echo "${HOME}/Documents/Claude/Projects/龙鱼五力" ;;
    "O MY HTML")  echo "${HOME}/Documents/Claude/Projects/O MY HTML" ;;
    *)            echo "" ;;
  esac
}

# 可跑列表（纯文档类项目（海螺姑娘/PEC/司南）不在列）
ALL_PROJECTS=("DVA" "渊图" "龙鱼五力" "O MY HTML")

run_one() {
  local p="$1"
  local src
  src=$(get_src_path "$p")
  if [ -z "$src" ]; then
    echo "❌ ${p}：无源码路径登记，跳过"
    return 1
  fi
  if [ ! -d "$src" ]; then
    echo "❌ ${p}：源码目录不存在 ${src}"
    return 1
  fi
  local dst="${BRAIN}/graphify/${p}"
  mkdir -p "${dst}"
  echo "🔄 ${p}：graphify ${src} → ${dst}"
  if ! command -v graphify >/dev/null 2>&1; then
    echo "❌ graphify 未在 PATH。试：export PATH=\"\$PATH:\$HOME/.local/bin\""
    return 1
  fi
  # 检测 API key（由 .env.graphify 加载）
  if [ -z "${ANTHROPIC_API_KEY:-}" ] && [ -z "${KIMI_API_KEY:-}" ]; then
    echo "❌ 未检测到 API key。"
    echo "   编辑 ${SCRIPT_DIR}/.env.graphify 配置 ANTHROPIC_API_KEY"
    return 1
  fi
  if [ -n "${ANTHROPIC_BASE_URL:-}" ]; then
    echo "🔗 backend: Anthropic 兼容 @ ${ANTHROPIC_BASE_URL}"
  fi
  if [ -n "${ANTHROPIC_MODEL:-}" ]; then
    echo "🤖 model: ${ANTHROPIC_MODEL}"
  fi
  cd "${src}"
  if [ -n "${ANTHROPIC_MODEL:-}" ]; then
    graphify extract "${src}" --out "${dst}" --backend claude --model "${ANTHROPIC_MODEL}"
  else
    graphify extract "${src}" --out "${dst}" --backend claude
  fi
  echo "✅ ${p} 完成"
}

if [ $# -eq 0 ]; then
  echo "可跑项目列表（与状态）："
  for p in "${ALL_PROJECTS[@]}"; do
    src=$(get_src_path "$p")
    dst="${BRAIN}/graphify/${p}"
    if [ -d "${dst}" ] && [ "$(ls "${dst}" 2>/dev/null | wc -l)" -gt 0 ]; then
      echo "  ✅ ${p}  →  ${dst}（已生成）"
    else
      echo "  ⏳ ${p}  →  ${src}（待跑）"
    fi
  done
  echo ""
  echo "用法："
  echo "  bash $0 <项目名>"
  echo "  bash $0 --all"
  exit 0
fi

if [ "$1" = "--all" ]; then
  for p in "${ALL_PROJECTS[@]}"; do
    run_one "$p" || true
    echo ""
  done
  exit 0
fi

run_one "$1"
