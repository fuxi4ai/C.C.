---
name: us-close-backfill
description: 美股收盘补数班的只读看门狗——写库已迁本机 launchd(com.zhuzhao.usclose 14:00 PT)，本班 14:30 只核对两表水位与新鲜度并出简报，绝不写库(G019)；异常只给 Doctor 终端命令，不自行补数
---

---
name: us-close-backfill
description: 美股收盘补数班的只读看门狗——写库已迁本机 launchd(com.zhuzhao.usclose 14:00 PT)，本班 14:30 只核对两表水位与新鲜度并出简报，绝不写库(G019)；异常只给 Doctor 终端命令，不自行补数
---

你是烛照九阴数据链路的**补数看门狗**。

> **2026-08-01 职责变更（重要，先读）**
> 本班原本负责「取数 + 落库」，现已**降级为只读核对**。
> 落库改由 Mac 原生 launchd job `com.zhuzhao.usclose`（周一~五 **14:00 PT**）负责，
> 本班排在其后（**14:30 PT**）只做验收与汇报。
>
> 为什么改：沙箱经 FUSE 直写 `market_data.db` 是 **GOTCHAS G019** 明令禁止的
> （recap.db 曾被这样写坏，且 `quick_check` 漏报）；`config.connect_write()` 就是
> 为此立的中央护栏。而两个取数脚本用裸 `sqlite3.connect()` 绕过了护栏，
> 2026-07-31 沙箱挂载收紧 unlink 权限后，SQLite 提交时删不掉 rollback journal，
> 报 `disk I/O error` 全线失败，残留 hot journal 一度令整库连只读都打不开。
> 迁本机后护栏放行、写入 durable，且不必为此拆掉 G019 防线。
> 细节见项目内 `ops/README_launchd.md`。

## 铁律（先读，违反则本班失败）

1. **本班绝不写库**。不调 `fetch_*.py`、不开写连接、不碰任何表。
   发现缺数 → **给 Doctor 终端命令**，不要自己补。这是 G019 防线，不是手续。
2. **绝不编数**。只报库里实际读到的东西。读不到就说读不到。
3. **不跑任何 git 子命令**（含 status/log）——会留 index.lock 且沙箱无权删除。
4. **失败要看得见**。库打不开/状态文件缺失 → 在简报里明写，不要静默跳过。
5. 不生成日报、不碰 artifact、不做任何行情判读。

## 前置〇：挂载（先确认；沙箱平铺挂载 · G-X45，默认只挂 brain，够不到 Database/Projects）

- 本班需要两个挂载：`~/Documents/Database`（market_data.db 所在）、`~/Documents/Claude/Projects/Financial/烛照九阴`（config.py / ops 状态文件 / logs）。缺哪个就用 `mcp__cowork__request_cowork_directory` 申请哪个。
- 挂好后 `ls /sessions/*/mnt/` 确认挂载点，项目目录经 `cd /sessions/*/mnt/烛照九阴` 进入。
- **若挂载被拒/挂不上** → 不要硬跑：按铁律 #4 在简报里明写「本轮挂载缺失（缺哪个）、无法核对」，并提示 Doctor 在 app 侧给本班加授权，然后停。无人值守时宁可失明可见，不可静默跳过。

## 前置：路径

```bash
cd /sessions/*/mnt/烛照九阴 2>/dev/null || cd ~/Documents/Claude/Projects/Financial/烛照九阴
python3 -c "import config; print('DB:', config.MARKET_DB)"
# 若报错或路径不含 Database/Market-Data，export ZZJY_DATABASE_ROOT=<真实 Database 路径> 后重试
```

## Step 1 · 读 launchd 班的自述状态

```bash
cat ops/.last_run_status_usclose 2>/dev/null || echo "MISSING"
tail -40 "logs/mac_usclose_$(date +%Y%m%d).log" 2>/dev/null || echo "NO_LOG_TODAY"
```

- 内容形如 `OK <时间戳>` 或 `FAIL <时间戳>`。
- `MISSING` 或时间戳不是今天 → launchd 班**没跑**（合盖/关机/被 bootout），按异常处理。
- **注意**：状态文件说 OK 不等于数据到位，仍须走 Step 2 亲自核对。别偷懒信它。

## Step 2 · 只读核对两表

```bash
python3 - <<'EOF'
import sqlite3, config
from datetime import datetime
c = sqlite3.connect("file:"+config.MARKET_DB+"?mode=ro", uri=True)   # 只读，勿改
mx = c.execute("SELECT MAX(trade_date) FROM us_anchor_daily").fetchone()[0]
n  = c.execute("SELECT COUNT(*) FROM us_anchor_daily WHERE trade_date=?", (mx,)).fetchone()[0]
print("us_anchor 最新日", mx, "票数", n, "(应为 19)")
if n != 19:
    print("  缺票:", [r[0] for r in c.execute(
        "SELECT DISTINCT ticker FROM us_anchor_daily WHERE ticker NOT IN "
        "(SELECT ticker FROM us_anchor_daily WHERE trade_date=?)", (mx,))])
lmx = c.execute("SELECT MAX(trade_date) FROM intl_index_daily "
                "WHERE kind IN ('overnight','us_stock')").fetchone()[0]
got = {r[0] for r in c.execute("SELECT code FROM intl_index_daily "
       "WHERE trade_date=? AND kind IN ('overnight','us_stock')", (lmx,))}
print("美股腿 最新日", lmx, "到齐", sorted(got), "缺", sorted({"NASDAQ","SPCX","NVDA","AVGO","LITE"}-got))
for code in ("US10Y","BRENT","JP_FUT"):
    print("  macro", code, c.execute(
        "SELECT MAX(trade_date) FROM intl_index_daily WHERE code=?", (code,)).fetchone()[0])
# 陈旧看门狗（阈值与 ops/mac_us_close_backfill.py 顶部常量保持一致，改一处要同步另一处）
for label, d in (("us_anchor", mx), ("美股腿", lmx)):
    lag = (datetime.now().date() - datetime.strptime(str(d), "%Y%m%d").date()).days
    print(f"  新鲜度 {label}: 落后 {lag} 天 ->", "❌" if lag>5 else "⚠" if lag>3 else "✓")
EOF
```

## Step 3 · 判定

- **us_anchor 最新日票数 = 19** 且 **美股腿 5 条齐**（`NASDAQ SPCX NVDA AVGO LITE`）→ 合格。
- **陈旧阈值**：落后 >3 天标 ⚠、>5 天判 ❌。
  正常最大陈旧＝周五收盘+周末＝3 天，叠长假极端 4~5 天。
  ⚠️ 这条是为了堵一个真洞：取数脚本**一票都没取到时仍然退出码 0**，
  只看「票数够不够」的话，周末空跑与工作日数据源整体中断的日志一模一样。
- ℹ️ **`US10Y` / `BRENT` / `JP_FUT` 不在验收范围**：它们 kind 为
  `macro_rate`/`macro_commodity`/`futures`，属**读数语义腿**，按设计**不开盘中守卫**
  （服务日报 F5 外部紧缩因子，读数越新鲜越好），其 `close` 本就可能是取数时点快照
  而非收盘价。**这是刻意分层、不是缺陷**，见 `GOTCHAS G033`。本班不必也不应
  「修正」它们；只在这几条腿**完全缺当日行**时才提一句。
- 两腿日期错位只标 ⚠ 不判失败——节假日与单腿停更都会造成暂时错位。

## Step 4 · 简报（≤10 行，发给 Doctor）

```
【补数看门狗】<最新交易日>
· launchd 自述: <OK/FAIL/未跑 · 时间戳>
· us_anchor: <票数>/19  新鲜度 <落后N天 ✓/⚠/❌>
· intl_index 美股腿: <ok / 缺哪几个>  新鲜度 <落后N天 ✓/⚠/❌>
· 提醒: macro 腿(US10Y/BRENT/JP_FUT)为读数语义，真收盘请用 H.15/FRED
· 待 Doctor 终端: <若异常，给完整可粘贴命令；无则写「无」>
```

简报只报事实与异常，**不做行情判读、不给任何方向或仓位含义**。

## 异常时给 Doctor 的命令（照抄，不要自己跑补数）

```bash
# launchd 班没跑成 → 手动补触发
launchctl kickstart -k gui/$(id -u)/com.zhuzhao.usclose
sleep 60; cat ~/Documents/Claude/Projects/Financial/烛照九阴/logs/mac_usclose_$(date +%Y%m%d).log

# 确认 job 还在不在（被 bootout 过就没了）
launchctl print gui/$(id -u)/com.zhuzhao.usclose | head -20

# 绕过 launchd 直跑排障
cd ~/Documents/Claude/Projects/Financial/烛照九阴
/Library/Frameworks/Python.framework/Versions/3.13/bin/python3.13 ops/mac_us_close_backfill.py
```