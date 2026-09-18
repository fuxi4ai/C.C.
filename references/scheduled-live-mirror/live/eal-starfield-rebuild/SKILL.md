---
name: eal-starfield-rebuild
description: EAL·SOX 事件星空快照日更重建（risk-daily 第三标签源）：行情守卫→沙箱标准链 build→对表验证；防快照冻结致「星星在、流线空」（2026-09-13 根因）
---

EAL · SOX 事件星空快照重建（风险日报第三标签的 iframe 源）。目的：星空页每次打开会按当天美东日期自动锚定「最近已收盘美股交易日」，若快照数据冻结、锚定日无 K 线，页面会只剩星星、零轴与 K 线整体不画（2026-09-13 根因故障）。本班每交易日收盘后重建快照，让数据跟住交易日。

步骤（只读库 + 写一个 HTML；不碰生产库、不改代码、不跑 git）：
1. 行情守卫（fail-visible）：只读生产库 attribution.db（沙箱路径 /sessions/*/mnt/Documents/Database/宏观研究体系/EAL/attribution.db，mode=ro），核 ^SOX 且 source='yahoo' 的 MAX(trade_date)；用冻结日历 /sessions/*/mnt/Documents/Claude/Projects/Financial/宏观研究体系/EAL/backtest/eal_v3/coding_work/_vv_staging/phase4_inputs/calendar-xnys-frozen-20261231.v2.csv 取「早于美东今天」的最后一行作为应有交易日。两者不等 → 输出一行「skip: 行情缺 {应有交易日}（库内 MAX={实际}）」并结束，不重建、不写任何文件。
2. 重建（沙箱标准链 EXP-20260908-001-T）：解析沙箱 Documents 挂载根（ls -d /sessions/*/mnt/Documents | head -1），cd 到其下 Claude/Projects/Financial/宏观研究体系/EAL/backtest，执行 EAL_DOCUMENTS_ROOT=<挂载根> python3 starfield_desk.py build。要求 exit 0 且输出 status=verified；失败重试至多 1 次，再失败即停并如实报告错误。
3. 对表验证：① node test_starfield_view.js 要求 fail=0；② 解析产物 EAL_STARFIELD.html 内嵌 JSON：market_as_of == 最近已收盘交易日、generated_at_utc 前进、candles 末根日期==该日；③ 机器复算页面锚定：内嵌 sessions 中「早于美东今天」的最后一日必须在内嵌 candles 中有 K 线（本故障判据，不过即视为重建失败）。任何一项不过 → 如实报告，不碰风险日报侧任何文件。
4. 简报（≤6 行）：MAX(trade_date) / candles 数 / market_as_of / generated_at / 单测与锚定断言结果 / 有无 skip。不推 risk-daily artifact——次日 09:08 refresh-risk-daily 班会自动嵌入最新快照。

边界：本班只读库、只写 backtest/EAL_STARFIELD.html（构建器原子写，ENTRY symlink 自动跟随）；不改生产库、不改代码、不跑 git、不碰调度器；异常只报告 Doctor，不自行修复。