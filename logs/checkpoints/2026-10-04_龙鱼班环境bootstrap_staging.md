# 龙鱼周更班 SKILL.md 环境段 bootstrap · staging（2026-10-04 · Q5A 裁定）

**✅ 已应用（2026-10-04 · Doctor 终端执行 + CC 回读核验）**：改前 SHA `bd7c9385ff0f3e311d5868e22e17c977aa47af45ffefbc2d1fca7dda607e2514` → 改后 SHA `b3a893628aa44d28301c528a69401162150239c6fd447db6ac6fbeb826e6af2b`；diff 差异行 17（＝新增 16 行 bootstrap ＋ `cd` 行改写 1 行，其余 9 行公共被对齐）——CC 回读 live 件：环境块与新块逐字一致、全文其余一字未动；备份 `SKILL.md.bak_envboot_20261004` 在旁。**自然验证：今晚 22:01 PT 周更班**（跑通 27/27 且无手工桥接字样即闭环）。

**裁定**：Doctor 问答板 5A「写入环境段」。属调度资产（活班 prompt 在 `~/Gateway-workspace/Scheduled/longyu-weekly-dualscorer/SKILL.md`）⇒ **CC 只出 staging，改动走 Doctor 终端，SHA 往返验收**（沙箱禁手不变）。

**改动范围**：仅「## 环境」代码块**整块替换**（旧块 13 行 → 新块 27 行）；其余正文一字不动。改完用 `diff` 对拍应只有该块。

## 旧块（逐字 · 现 live 文）

```
cd ~/Documents && set -a; . Database/.env; set +a
# 代理探测化（G-X 2026-08-01）：沙箱镜像不保证有 localhost:3128。
# 写死 export 会让首只标的报出误导性的「找不到标的」（实为代理 connection refused）。
curl -s -x localhost:3128 -m 3 -o /dev/null https://api.tushare.pro \
  && export HTTPS_PROXY=localhost:3128 HTTP_PROXY=localhost:3128 \
  || echo "代理不可用→直连（正常，勿修）"
# pack 目录（G-X 2026-08-01）：/tmp/packs 属主可能是 nobody 不可写；
# LYW_PACK_DIR 是 score_subitems.py 原生支持的 env。
export LYW_PACK_DIR=$HOME/packs; mkdir -p $HOME/packs
mkdir -p ~/.tushare && grep '^TUSHARE_TOKEN=' Database/.env | cut -d= -f2- | tr -d '"'"'"' \n' > ~/.tushare/token
```

## 新块（逐字 · 直接粘贴替换）

```
# 沙箱路径 bootstrap（2026-10-04 补 · 路径坑第 4 次同根复发 NOTE-20260813-001）：
# 沙箱 ~/Documents 可能不存在或指向错误 → 桥接到挂载点（symlink 跨调用持久），
# 再显式 export 四个库位 env（免 expanduser 落空）。
if [ ! -d ~/Documents/Database ]; then
  D=$(ls -d /sessions/*/mnt/Documents ~/mnt/Documents 2>/dev/null | head -1)
  if [ -n "$D" ]; then
    [ -e ~/Documents ] && [ ! -L ~/Documents ] && mv ~/Documents ~/Documents.bak_sandbox
    ln -sfn "$D" ~/Documents
  fi
fi
DOC_ROOT=$(cd ~/Documents 2>/dev/null && pwd -P) || { echo "⚠ Documents 挂载点不可达，本轮无法落库"; exit 1; }
export LYW_LIB="$DOC_ROOT/Database/龙鱼-标的分析库/records"
export LYW_COMPARE_DIR="$DOC_ROOT/Database/龙鱼-标的分析库/对比校正"
export LYW_TREND_DIR="$DOC_ROOT/Database/龙鱼-标的分析库/趋势"
export CHANGGENG_JSON="$DOC_ROOT/Database/龙鱼-标的分析库/常更标的.json"
cd "$DOC_ROOT" && set -a; . Database/.env; set +a
# 代理探测化（G-X 2026-08-01）：沙箱镜像不保证有 localhost:3128。
# 写死 export 会让首只标的报出误导性的「找不到标的」（实为代理 connection refused）。
curl -s -x localhost:3128 -m 3 -o /dev/null https://api.tushare.pro \
  && export HTTPS_PROXY=localhost:3128 HTTP_PROXY=localhost:3128 \
  || echo "代理不可用→直连（正常，勿修）"
# pack 目录（G-X 2026-08-01）：/tmp/packs 属主可能是 nobody 不可写；
# LYW_PACK_DIR 是 score_subitems.py 原生支持的 env。
export LYW_PACK_DIR=$HOME/packs; mkdir -p $HOME/packs
mkdir -p ~/.tushare && grep '^TUSHARE_TOKEN=' Database/.env | cut -d= -f2- | tr -d '"'"'"' \n' > ~/.tushare/token
```

## 应用步骤（Doctor 终端）

```bash
# ① 改前取 SHA
shasum -a 256 ~/Gateway-workspace/Scheduled/longyu-weekly-dualscorer/SKILL.md
# ② 用编辑器打开，把「## 环境」代码块整块替换为新块（其余一字不动）
# ③ 改后取 SHA 并回贴两个 SHA 给 CC 对拍留痕
shasum -a 256 ~/Gateway-workspace/Scheduled/longyu-weekly-dualscorer/SKILL.md
```

## 设计要点（验收口径）

- **核心是 symlink 桥接**（跨 bash 调用持久；bash 各调用独立、env export 不跨调用）——`~/Documents/Database` 不存在即桥接，覆盖「无 ~/Documents」与「指向错误」两种形态。
- **env export 是同调用冗余**（`LYW_LIB` 等四个库位、`LYW_PACK_DIR` 同款），并让路径不依赖 `expanduser`。
- **挂载形状候选**：`/sessions/*/mnt/Documents` 与 `~/mnt/Documents` 都试；若该壳实际形状不同，把 `D=` 那行改指实际挂载路径（staging 已把候选写全，一般不用改）。
- **fail-closed**：挂载点不可达 → 明确报错 exit 1，不再走到「首只落库 FileNotFoundError」的误导性报错。
- **验证**：今晚 22:01 PT 周更班自然验证（若班跑通 27/27 且无「ln -s 桥接」类手工修复字样，即闭环；在此之前只算「已改」）。
