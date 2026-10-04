#!/usr/bin/env bash
# PEC/brain 通用 · 「改动面自核」闸（scope guard）· 2026-10-01 立
#
# 【治什么】（承 Doctor 2026-10-01 令「把『顺手』这个毛病改了，这才是真收益」）
#   病名：**顺手扩改**——修 A 的时候，手已经在同一行/同一段/同一表里，
#   于是**连带改写了没被点名的兄弟格**，且那个格的值是**凭印象填的，不是回读源头的**。
#   2026-10-01 CS-10 现行判据件实例：修「蒙古遗产 干净通过→低空通过」时，
#   顺手把同句的「家长制」也写进了「低空通过」，而家长制的行动计数是 **3**（不是 2）。
#
# 【为什么纪律层拦不住】（本条与 `G-X151` 追记同源，是它的**编辑侧对偶**）
#   「顺手」的诱因是**我以为自己在搬运一个已知值，不认为自己在写断言**——
#   于是**回代验算的反射根本没被触发**。光说「要回代」没用，因为**触发条件本身失效了**。
#   ⇒ 必须换成**不依赖自省**的动作：**改前留副本、改后看改动面**。
#
# 【它怎么工作】
#   改前：`scope_guard.sh snap <文件> <标签>`
#   改后：`scope_guard.sh chk  <文件> <标签>`
#   chk 打印 diff 与**改动行数**，并给出判据：
#     **改动行数 == 本轮被点名的目标数 ⇒ 过；超出 ⇒ 超出部分即「顺手」，逐行说明或回退。**
#
# 【边界 · 必读】
#   · 它**不判对错**，只把改动面摊开给人看——**它是提示器，不是闸**。
#   · 它**拦不住 Edit 工具**（Edit 不过 shell）⇒ 它是**流程约定 + 事后摊面**，不是强制拦截。
#   · 快照落 `/tmp`（VM 内、随会话消失、不落用户盘、不进任何仓）。
#   · 快照键＝路径 hash 前缀＋文件名＋标签（同名件不互覆 · 2026-10-04 修）。
#
# 作者：CC · 2026-10-01 · 本脚本未经独立复验
set -uo pipefail

SNAPDIR="${SCOPE_GUARD_DIR:-/tmp/.scope_guard}"

die() { echo "scope_guard: $*" >&2; exit 2; }

# 快照键＝路径 hash 前缀 ＋ 文件名 ＋ 标签（2026-10-04 修：原键只有 basename ⇒ 同名件互覆且 chk 假绿）
_key() {
  local f="$1" tag="$2" h
  if command -v sha256sum >/dev/null 2>&1; then h=$(printf '%s' "$f" | sha256sum | cut -d' ' -f1)
  elif command -v shasum >/dev/null 2>&1; then h=$(printf '%s' "$f" | shasum -a 256 | cut -d' ' -f1)
  else h="ck$(printf '%s' "$f" | cksum | cut -d' ' -f1)"; fi
  printf '%s_%s.%s.bak' "${h:0:12}" "$(basename "$f")" "$tag"
}

cmd_snap() {
  local f="$1" tag="${2:-default}"
  [ -f "$f" ] || die "文件不存在：$f"
  mkdir -p "$SNAPDIR"
  cp -p "$f" "$SNAPDIR/$(_key "$f" "$tag")" || die "快照失败（挂载怪癖？试新建+mv）"
  echo "✓ 快照：$f → $SNAPDIR/$(_key "$f" "$tag")"
  echo "  （改完后跑：scope_guard.sh chk \"$f\" \"$tag\"）"
}

cmd_chk() {
  local f="$1" tag="${2:-default}"
  local b="$SNAPDIR/$(_key "$f" "$tag")"
  [ -f "$b" ] || die "无快照：$b（改前忘了 snap？）"
  [ -f "$f" ] || die "文件不存在：$f"

  local d
  d="$(diff -u "$b" "$f" || true)"
  if [ -z "$d" ]; then
    echo "⚠ 改动面＝0：本轮到 chk 时文件与快照**逐字节相同**。"
    echo "  ⇒ 要么没改（那就不用 chk），要么改在了别处——**请核实目标文件是否搞对**。"
    return 1
  fi

  local added removed
  added=$(printf '%s\n' "$d" | grep -c '^+[^+]' || true)
  removed=$(printf '%s\n' "$d" | grep -c '^-[^-]' || true)

  echo "── 改动面（$f · tag=$tag）────────────────────────────"
  printf '%s\n' "$d"
  echo "────────────────────────────────────────────────────"
  echo "增行 $added · 删行 $removed"
  echo
  echo "【判据】改动行数 **必须等于** 本轮被点名的目标数。"
  echo "  · 对得上 ⇒ 过。"
  echo "  · 有超出 ⇒ **超出部分就是「顺手」**：逐行说明它属不属于本轮目标；"
  echo '    不属于 ⇒ **回退它**，或**回读源头后再单独做一次**（`G-X189` 判据①）。'
  echo "  · ⚠ 本工具不判对错，只摊面 —— 提示器，不是闸。"
}

cmd_selftest() {
  local tmp; tmp="$(mktemp -d)"; local ok=0
  export SCOPE_GUARD_DIR="$tmp/snap"
  printf 'A\nB\nC\n' > "$tmp/f.md"
  cmd_snap "$tmp/f.md" t >/dev/null
  printf 'A\nB2\nC\n' > "$tmp/f.md"
  local out; out="$(cmd_chk "$tmp/f.md" t)"
  if printf '%s' "$out" | grep -q "增行 1 · 删行 1"; then
    echo "  ✓ 正常改动被正确量出（增行 1 · 删行 1）"; else echo "  ✗ 量测不对：$out"; ok=1; fi

  # 反向：无改动应报 0（注意 cmd_chk 故意 return 1，须 `|| true` 兜住 pipefail）
  cmd_snap "$tmp/f.md" t2 >/dev/null
  out="$(cmd_chk "$tmp/f.md" t2 || true)"
  if printf '%s' "$out" | grep -q "改动面＝0"; then
    echo "  ✓ 零改动被识别，且退出码为 1（告警级）"; else echo "  ✗ 零改动未被识别：$out"; ok=1; fi

  # 反向：无快照应 exit 2（⚠ die 用 exit，会把整个脚本带走 ⇒ **必须放子壳里**）
  if ( cmd_chk "$tmp/nonexist.md" zz ) >/dev/null 2>&1; then
    echo "  ✗ 无快照未报错"; ok=1
  else
    rc=$?; [ "$rc" -eq 2 ] && echo "  ✓ 无快照 fail-closed（rc=2）" || { echo "  ✗ 退出码非 2：$rc"; ok=1; }
  fi

  # 反向：多改动应被完整量出（守「超出即顺手」能看见）
  #   baseline A/B/C → A/B2/C2/D ⇒ -B +B2 -C +C2 +D＝**增行 3 · 删行 2**
  #   ⚠ 本行初版写「增行 2 · 删行 1」——**那是凭印象写的期望值，没数**，
  #     当场被自检逮红。**这是「顺手写数」毛病的又一个实例**，留痕于此。
  printf 'A\nB2\nC2\nD\n' > "$tmp/f.md"
  out="$(cmd_chk "$tmp/f.md" t)"
  if printf '%s' "$out" | grep -q "增行 3 · 删行 2"; then
    echo "  ✓ 超出目标的改动被完整量出（增行 3 · 删行 2）"; else echo "  ✗ 未完整量出：$out"; ok=1; fi

  # 回归：同名件互覆（2026-10-04 修 · 快照键含路径 hash 前缀）
  mkdir -p "$tmp/d1" "$tmp/d2"
  printf 'X1\n' > "$tmp/d1/SAME.md"; printf 'X2\n' > "$tmp/d2/SAME.md"
  cmd_snap "$tmp/d1/SAME.md" c >/dev/null
  cmd_snap "$tmp/d2/SAME.md" c >/dev/null
  printf 'X1b\n' > "$tmp/d1/SAME.md"
  out="$(cmd_chk "$tmp/d1/SAME.md" c)"
  if printf '%s' "$out" | grep -q "增行 1 · 删行 1"; then
    echo "  ✓ 同名件快照不互覆（各自对各自）"; else echo "  ✗ 同名件仍互覆：$out"; ok=1; fi
  out="$(cmd_chk "$tmp/d2/SAME.md" c || true)"
  if printf '%s' "$out" | grep -q "改动面＝0"; then
    echo "  ✓ 另一件零改动不受波及"; else echo "  ✗ 另一件受波及：$out"; ok=1; fi

  rm -rf "$tmp"
  echo "SELF-TEST $([ $ok -eq 0 ] && echo PASS || echo FAIL)"
  return $ok
}

case "${1:-}" in
  snap) shift; cmd_snap "$@" ;;
  chk)  shift; cmd_chk "$@" ;;
  --self-test) cmd_selftest ;;
  *) cat <<'USAGE'
scope_guard.sh · 改动面自核（治「顺手扩改」）

  scope_guard.sh snap <文件> <标签>     改前：留快照
  scope_guard.sh chk  <文件> <标签>     改后：摊开改动面 + 量改动行数
  scope_guard.sh --self-test            自检

判据：**改动行数 == 本轮被点名的目标数**；超出即「顺手」，须回退或回读源头后另做。
USAGE
     exit 1 ;;
esac
