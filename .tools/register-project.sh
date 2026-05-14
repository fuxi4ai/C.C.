#!/usr/bin/env bash
# register-project.sh — brain 项目骨架生成器（幂等）
#
# 用法：
#   ./register-project.sh <项目名> [code_path]
#
# 行为：
#   1. 在 brain/{项目名}/ 下创建标准目录：architecture / pipeline / data / features / logs
#   2. 创建占位文件：architecture/系统概览.md / architecture/决策记录.md / GOTCHAS.md
#   3. 已存在的文件**不覆盖**，只补缺
#   4. 在 brain/CLAUDE.md 的项目列表表格追加一行（若已登记则跳过）
#
# 维护：Doctor + CC
# 落点：brain/.tools/register-project.sh
set -euo pipefail

# --- 路径定位 ---
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BRAIN_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

# --- 参数 ---
if [[ $# -lt 1 ]]; then
  echo "用法：$0 <项目名> [code_path]" >&2
  echo "例：$0 龙鱼五力 Claude/Projects/龙鱼五力/" >&2
  exit 1
fi

PROJECT_NAME="$1"
CODE_PATH="${2:-Claude/Projects/${PROJECT_NAME}/}"
PROJECT_DIR="${BRAIN_ROOT}/${PROJECT_NAME}"
TODAY="$(date +%Y-%m-%d)"

echo "📂 brain root: ${BRAIN_ROOT}"
echo "📂 project   : ${PROJECT_DIR}"
echo "🔗 code_path : ${CODE_PATH}"
echo ""

# --- 1. 创建目录 ---
created_dirs=()
for sub in architecture pipeline data features logs; do
  if [[ ! -d "${PROJECT_DIR}/${sub}" ]]; then
    mkdir -p "${PROJECT_DIR}/${sub}"
    created_dirs+=("${sub}/")
  fi
done

if [[ ${#created_dirs[@]} -gt 0 ]]; then
  echo "✅ 新建目录：${created_dirs[*]}"
else
  echo "ℹ️  所有标准目录已存在"
fi

# --- 2. 占位文件（不覆盖）---
OVERVIEW="${PROJECT_DIR}/architecture/系统概览.md"
if [[ ! -f "${OVERVIEW}" ]]; then
  cat > "${OVERVIEW}" <<EOF
---
title: ${PROJECT_NAME} · 系统概览
tags: [${PROJECT_NAME}, architecture]
created: ${TODAY}
updated: ${TODAY}
status: active
type: permanent
project: ${PROJECT_NAME}
code_path: ${CODE_PATH}
---

# ${PROJECT_NAME} · 系统概览

> 项目最顶层视角。CC 进入该项目时第一篇要读的文件。

## 项目使命

（一句话讲清这个项目要解决什么问题）

## 当前阶段

- **状态**：📋 待启动 / 🟢 活跃 / 🟡 维护 / 🔴 暂停
- **最后活跃**：${TODAY}

## 模块构成

（核心模块列表，1-3 句话说明每个模块的职责）

## 关键依赖

- 上游：
- 下游：

## 相关笔记

- [[决策记录]]
- [[GOTCHAS]]
EOF
  echo "✅ 创建：architecture/系统概览.md"
else
  echo "⏭️  保留已有：architecture/系统概览.md"
fi

DECISIONS="${PROJECT_DIR}/architecture/决策记录.md"
if [[ ! -f "${DECISIONS}" ]]; then
  cat > "${DECISIONS}" <<EOF
---
title: ${PROJECT_NAME} · 决策记录
tags: [${PROJECT_NAME}, decision]
created: ${TODAY}
updated: ${TODAY}
status: active
type: decision
project: ${PROJECT_NAME}
---

# ${PROJECT_NAME} · 决策记录

> 项目内重大决策的时间线。一条决策一个 H2。

格式：

\`\`\`
## YYYY-MM-DD · 决策标题

**背景**：为什么要做这个决策

**选项**：
- A：...
- B：...

**选择**：B

**理由**：

**影响**：
\`\`\`

---

<!-- 在下方追加新决策 -->
EOF
  echo "✅ 创建：architecture/决策记录.md"
else
  echo "⏭️  保留已有：architecture/决策记录.md"
fi

GOTCHAS="${PROJECT_DIR}/GOTCHAS.md"
if [[ ! -f "${GOTCHAS}" ]]; then
  cat > "${GOTCHAS}" <<EOF
---
title: ${PROJECT_NAME} · GOTCHAS（已知坑）
tags: [${PROJECT_NAME}, gotchas]
created: ${TODAY}
updated: ${TODAY}
status: active
type: resource
project: ${PROJECT_NAME}
---

# ${PROJECT_NAME} · GOTCHAS（已知坑）

> 排查超过一轮的问题都该记录在这里。CC 遇到报错并解决后**立即**回写，无需 Doctor 提示。
> 实时操作日志写在项目目录的 \`Projects/${PROJECT_NAME}/GOTCHAS.md\`；这里是沉淀+索引。

## 格式

\`\`\`
## [ERR-YYYYMMDD-NNN] 简要描述
**状态**: ✅ 已解决 / ⏳ 待解决
**优先级**: 🔴 高 / 🟡 中 / 🟢 低
**触发场景**:
**错误信息**:
**解决方案**:
**预防措施**:
\`\`\`

---

<!-- 在下方追加新条目 -->
EOF
  echo "✅ 创建：GOTCHAS.md"
else
  echo "⏭️  保留已有：GOTCHAS.md"
fi

# --- 3. CLAUDE.md 项目表登记提示 ---
CLAUDE_MD="${BRAIN_ROOT}/CLAUDE.md"
if [[ -f "${CLAUDE_MD}" ]]; then
  if grep -q "\[\[${PROJECT_NAME}\]\]\|| ${PROJECT_NAME} |\|\`${PROJECT_NAME}/\`" "${CLAUDE_MD}"; then
    echo "⏭️  CLAUDE.md 已登记，跳过追加"
  else
    echo "ℹ️  CLAUDE.md 未登记 ${PROJECT_NAME} — 请手动追加："
    echo "    | ${PROJECT_NAME} | \`${PROJECT_NAME}/\` | 活跃 | ${TODAY} |"
  fi
fi

echo ""
echo "🎉 ${PROJECT_NAME} 骨架已就绪"
