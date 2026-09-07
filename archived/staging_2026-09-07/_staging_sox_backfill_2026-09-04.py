#!/usr/bin/env python3
"""^SOX 历史回填 → attribution.db prices_daily
窗口与既有 SMH 对齐（2026-02-20 起）· 幂等 UPSERT（主键 ticker,trade_date,source）· source=yahoo 与既有行一致
运行前自动备份 attribution.db → attribution.db.bak_preSOX_YYYYMMDD_HHMM
"""
import json
import shutil
import sqlite3
import urllib.request
import datetime

DB = "/Users/lunarabbit/Documents/Database/剑酒青丘/backtest/attribution.db"
TICKER = "^SOX"
START = "2026-02-20"

now = datetime.datetime.now(datetime.timezone.utc)
stamp = now.strftime("%Y%m%d_%H%M")
backup = f"{DB}.bak_preSOX_{stamp}"
shutil.copy2(DB, backup)
print(f"✓ 备份 → {backup}")

period1 = int(datetime.datetime(2026, 2, 19, tzinfo=datetime.timezone.utc).timestamp())
period2 = int(now.timestamp()) + 86400
url = f"https://query1.finance.yahoo.com/v8/finance/chart/%5ESOX?period1={period1}&period2={period2}&interval=1d"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
data = json.load(urllib.request.urlopen(req, timeout=30))
result = data["chart"]["result"][0]
ts = result["timestamp"]
quote = result["indicators"]["quote"][0]

rows = []
for i, t in enumerate(ts):
    day = datetime.datetime.fromtimestamp(t, tz=datetime.timezone.utc).date().isoformat()
    if day < START:
        continue
    c = quote["close"][i]
    if c is None:
        continue
    o = quote["open"][i] if quote["open"][i] is not None else c
    h = quote["high"][i] if quote["high"][i] is not None else c
    l = quote["low"][i] if quote["low"][i] is not None else c
    rows.append((TICKER, day, float(o), float(h), float(l), float(c), 0.0, "yahoo", now.isoformat()))

con = sqlite3.connect(DB)
con.execute("BEGIN")
for r in rows:
    con.execute(
        "INSERT OR REPLACE INTO prices_daily (ticker,trade_date,open,high,low,close,volume,source,fetched_at) VALUES (?,?,?,?,?,?,?,?,?)",
        r,
    )
con.commit()
n, lo, hi = con.execute("SELECT COUNT(*), MIN(trade_date), MAX(trade_date) FROM prices_daily WHERE ticker='^SOX'").fetchone()
print(f"✓ ^SOX 回填 {n} 行 · {lo} → {hi}")
con.close()
