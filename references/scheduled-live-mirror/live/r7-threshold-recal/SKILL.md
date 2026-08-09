---
name: r7-threshold-recal
description: 一次性：r7 USDJPY 急动阈值 v0 复校（首个实战🔴或两个月后之约）
---

r7 USDJPY 急动阈值 v0 复校（2026-08-07 立项时定的待办：首个实战🔴或约两个月后复校，这是后者）。

背景：风险日报项目的 r7 日元 carry 平仓螺旋有数据判读器（Polygon C:USDJPY 15m → attribution.db → r7_yen_watch.py → build_risk_daily），阈值是 v0，当时只用 5.2 个月历史（2026-03-01→08-06）校准。

步骤：
1. 读 /Users/lunarabbit/Documents/Claude/Projects/风险日报/mech-watch/机制扳机词表.md 的「r7 数据判读 v0」节，回顾定案口径：单向跌幅触发——4h 跌 ≥0.7%🟠/≥1.5%🔴 主触发，1h 跌 ≥0.5%/≥1.0% 速度辅证，两窗取重，回看 13h，跳空弃窗，72h 陈旧门控。
2. 查期间实战表现：跑 python3 /Users/lunarabbit/Documents/Claude/Projects/风险日报/mech-watch/r7_yen_watch.py --scan，看 2026-08-07 之后的触发日（尤其 🔴）；如有，对照当时行情/新闻判断真火还是误报。
3. 样本量闸门（先做这道）：跑重校准前先查数据跨度——SELECT (MAX(ts_utc)-MIN(ts_utc))/86400 AS span_days FROM prices_intraday WHERE ticker='C:USDJPY' AND interval='15m'。若 span_days < 约 200 天（6.5 个月），说明仍是 v0 同源数据、未到复校时机：直接出结论「样本仍不足、维持 v0」，附当前跨度天数+末棒日期，跳过后续分位对比，绝不硬调。
4. 重校准（仅当闸门通过）：跑 python3 /Users/lunarabbit/Documents/Claude/Projects/风险日报/mech-watch/calibrate_usdjpy.py（只读 /Users/lunarabbit/Documents/Database/剑酒青丘/backtest/attribution.db，C:USDJPY 15m），对比新分位与现阈值：🔴1.5% 的年化频次是否仍合理、🟠0.7% 月均触发是否仍约 2 天、1h 辅证阈同理。
5. 出结论给 Doctor：阈值「维持 / 调整」提案带数据依据。若调整，走 propose-then-confirm（先方案、批准后才改 r7_yen_watch.py 顶部的阈值常量），并同步更新词表「r7 数据判读」节与记忆 reference_polygon_fx（在记忆目录，先 Read 再改）。

约束：attribution.db 只读（运营质保归 VV，要动先知会 Doctor 转交）；沙箱内不跑任何 git 子命令；宁可结论「样本仍不足、维持 v0」也不硬调。