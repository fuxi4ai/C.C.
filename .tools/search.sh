#!/usr/bin/env bash
# search.sh — brain/ 全文搜索（ripgrep 封装）
#
# 用法：
#   search.sh -k <keyword>             普通关键词搜索（默认大小写不敏感）
#   search.sh -t <tag>                  按 frontmatter tag 搜
#   search.sh -p <project>              按 frontmatter project 字段搜
#   search.sh -T <type>                 按 frontmatter type 搜
#   search.sh -s <status>               按 frontmatter status 搜
#   search.sh -l <wikilink>             找所有引用了 [[wikilink]] 的笔记
#   search.sh -F                        交互式模糊查找文件名（需要 fzf）
#   search.sh <keyword>                 等价于 -k
#
# 选项：
#   -c                                  case-sensitive
#   -h                                  显示本帮助

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BRAIN_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

if ! command -v rg &>/dev/null; then
  echo "❌ ripgrep 未安装。macOS: brew install ripgrep" >&2
  exit 2
fi

# 默认参数
MODE=""
ARG=""
CASE_FLAG="-i"

usage() {
  grep '^# ' "$0" | sed 's/^# //'
  exit 0
}

while getopts "k:t:p:T:s:l:Fch" opt; do
  case $opt in
    k) MODE="keyword"; ARG="$OPTARG" ;;
    t) MODE="tag"; ARG="$OPTARG" ;;
    p) MODE="project"; ARG="$OPTARG" ;;
    T) MODE="type"; ARG="$OPTARG" ;;
    s) MODE="status"; ARG="$OPTARG" ;;
    l) MODE="wikilink"; ARG="$OPTARG" ;;
    F) MODE="fzf" ;;
    c) CASE_FLAG="" ;;
    h) usage ;;
    *) usage ;;
  esac
done

# 如果没有任何 -x，把第一个位置参数当 keyword
if [[ -z "${MODE}" ]]; then
  shift $((OPTIND - 1)) || true
  if [[ $# -ge 1 ]]; then
    MODE="keyword"
    ARG="$1"
  else
    usage
  fi
fi

# 公共 rg 选项
RG_OPTS=(
  --type md
  --glob '!.git/**'
  --glob '!.obsidian/**'
  --glob '!.index/**'
  --glob '!_DEPRECATED_*/**'
  --glob '!_TRASH_*'
  ${CASE_FLAG}
  -n
  -H
  --color always
)

cd "${BRAIN_ROOT}"

case "${MODE}" in
  keyword)
    echo "🔎 keyword: ${ARG}"
    rg "${RG_OPTS[@]}" -- "${ARG}" . || echo "(无匹配)"
    ;;
  tag)
    echo "🏷  tag: ${ARG}"
    # 匹配 frontmatter 中 tags: [..., ARG, ...]
    rg "${RG_OPTS[@]}" -U "^tags:.*\b${ARG}\b" . || echo "(无匹配)"
    ;;
  project)
    echo "📁 project: ${ARG}"
    rg "${RG_OPTS[@]}" "^project:.*${ARG}" . || echo "(无匹配)"
    ;;
  type)
    echo "🧬 type: ${ARG}"
    rg "${RG_OPTS[@]}" "^type:\s*${ARG}\s*$" . || echo "(无匹配)"
    ;;
  status)
    echo "📊 status: ${ARG}"
    rg "${RG_OPTS[@]}" "^status:\s*${ARG}\s*$" . || echo "(无匹配)"
    ;;
  wikilink)
    echo "🔗 引用 [[${ARG}]] 的笔记："
    # 转义可能的特殊字符
    ESC=$(printf '%s' "${ARG}" | sed 's/[][\\.*^$()+?{}|]/\\&/g')
    rg "${RG_OPTS[@]}" -- "\\[\\[${ESC}(\\||#|\\])" . || echo "(无匹配)"
    ;;
  fzf)
    if ! command -v fzf &>/dev/null; then
      echo "❌ fzf 未安装。macOS: brew install fzf" >&2
      exit 2
    fi
    find . -name "*.md" \
      -not -path './.git/*' \
      -not -path './.obsidian/*' \
      -not -path './.index/*' \
      -not -path './_DEPRECATED_*' \
      | fzf --preview 'cat {}'
    ;;
esac
