#!/usr/bin/env bash
# backup-icloud.sh — rsync brain/ 到 iCloud Drive 镜像
#
# 用法：
#   bash backup-icloud.sh             # 跑一次
#   crontab：0 3 * * * bash ~/Documents/Claude/brain/.tools/backup-icloud.sh
#
# 设计：
#   - 增量 rsync（删旧的）
#   - 排除 .gitignore 列出的内容
#   - 输出日志到 brain/.tools/backup.log

set -euo pipefail

SRC="${HOME}/Documents/Claude/brain"
DST="${HOME}/Library/Mobile Documents/com~apple~CloudDocs/brain-mirror"
LOG="${SRC}/.tools/backup.log"

mkdir -p "${DST}"

TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

# 排除清单（与 .gitignore 同源）
EXCLUDES=(
  --exclude='.DS_Store'
  --exclude='.git/'
  --exclude='.index/'
  --exclude='graphify/*/cache/'
  --exclude='.obsidian/workspace.json'
  --exclude='.obsidian/workspace-mobile.json'
  --exclude='*.swp'
  --exclude='*.swo'
  --exclude='*~'
  --exclude='.tmp/'
)

{
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "[${TIMESTAMP}] backup-icloud.sh 开始"
  echo "  src: ${SRC}"
  echo "  dst: ${DST}"
  echo ""

  rsync -av --delete "${EXCLUDES[@]}" "${SRC}/" "${DST}/brain/" 2>&1 | tail -10

  echo ""
  echo "[${TIMESTAMP}] 完成。文件数：$(find "${DST}/brain" -type f | wc -l)"
  echo ""
} | tee -a "${LOG}"
