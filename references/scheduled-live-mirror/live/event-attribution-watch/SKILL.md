---
name: event-attribution-watch
description: 事件归因验证班：采集上一美股交易日数据→事件日判定→收盘级归因→与注册量级带对准→提案制汇报（剑酒青丘·解释层）
---

事件归因验证班（剑酒青丘 · 解释层 overlay）。称呼用户为 Doctor，一律用「您」。目标：验证 brain 事件归因台账的注册签名与条件量级带——采集→判定→归因→对准→汇报；只提案、不擅改。

## 硬约束（每条都不可绕过）
- 不在沙箱跑任何 git 子命令（含 status/log——会残留 index.lock）；仓库状态只用 ls/cat 读 .git/ 纯文本。
- 不用 curl/python/requests 绕过 web_fetch 拉网络内容；web_fetch 失败只能改用 WebSearch 或把 curl 命令块写进简报交 Doctor 终端跑。
- 永不修改台账「注册表」的量级带/签名/可证伪条件——那需要 Doctor 明示批准；本班只能追加记账行与提案区条目。
- 缺数一律显式标「◌不可判」并附补数命令，禁止静默跳过或当成安全（fail-visible·缺数≠安全）。
- 永不在任何待办/PRD 上打 ✓ 收口（G-X4）。
- 时间判定先跑 date 对表（UTC/美东/北京），业务「今天/昨天」锚业务时区，不用沙箱本地日（G-X100/G-X105）。

## 步骤
1. 读 ~/Documents/Claude/brain/剑酒青丘/frameworks/事件归因台账.md 全文（注册表·记账表·提案区·变更记录·验证日历）。若该文件不存在或结构缺失，停止并在简报报告，不要自行重建。
2. 判定上一美股交易日（美东）是否事件日：用 WebSearch 查该日收盘综述（例 "stock market July 30 2026 close recap"）；再扫 FOMC/CPI/NFP 日历事件与重大地缘（袭击/报复/停火）、央行官员讲话头条。非事件日→跳到第 5 步，简报走精简版。
3. 采集该交易日收盘级数据，按序尝试并记录哪一级成功：
   ① stooq CSV（web_fetch）：https://stooq.com/q/d/l/?s=^spx&i=d 型（品种：^spx、^ndq、^dji、nvda.us、smh.us、^vix、cl.f、gc.f）；10Y/2Y 用 FRED：https://fred.stlouisfed.org/graph/fredgraph.csv?id=DGS10 与 id=DGS2（注意 FRED 有 T+1 滞后，滞后即标注）。
   ② stooq 失败→Yahoo chart 接口（query1.finance.yahoo.com/v8/finance/chart/…）——已知沙箱 web_fetch 可能返回空体（风险日报 GOTCHAS ERR-20260730-003），空体≠无数据，先当通道错。
   ③ 仍失败→该品种标 ◌，并在简报给出可直接粘贴的 Doctor 终端命令块：curl -sS --compressed -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36" "<url>" -o <file>。
4. 若为事件日→按 permanent/经验库.md 的 EXP-20260730-001-P「事件研究三件套」做收盘级归因：
   - 双时间戳：WebSearch 把每条事件的新闻发布时刻钉到分钟（注明来源与链接）；收盘级数据没有磁带戳，注明「分钟级深剖待补」并生成对应的分时 curl 命令块（参照 AI4ME/us_intraday_20260729/ 的命名惯例）交 Doctor。
   - 截面签名：2Y/10Y/金/油/VIX/半导体与台账注册指纹逐项比对，明确写出「谁动了、谁没动」。
   - 粗贡献估计＋恒等式对账：各因子收盘级贡献相加对实际指数涨跌，残差写明。
5. 慢变量（每天做）：AI 持续性缺口＝NVDA 与 SMH 相对 SPX 的当日超额（可得则记，不可得标 ◌）。
6. 对准：逐因子与注册量级带比对——带内且签名符合→记账表追加一行（标✓）；带外或签名违例→写入台账「六、提案区」（格式：日期｜因子｜实测值｜建议（新带或分类审查）｜证据），不动注册表本体。
7. 产出三件：
   ① 用 Edit 工具更新台账 md：记账表新行、提案区（如有）、artifact 快照时间同步说明；
   ② 重新生成 artifact：按暖色·警示页范式（米底 #f6efe0/墨 #3a3126/朱 #b23b2e/青碧 #2e7d6e/驼 #a3763f/边线 #e6dbc4；serif 标题；◌ 表不可判；变更记录区只增不减）把台账全量渲染为自包含 HTML（:root{color-scheme:light}），**章节顺序固定（Doctor 裁定）：一·函数式归因曲线（首节）→ 二·注册表 → 三·记账表 → 四·提案区 → 五·变更记录 → 六·验证日历**。归因曲线为定型视觉语法（铁律）：横轴＝盘中或收盘级时间、水平零轴，各因子累计贡献 f(t)＋灰虚残差，Σ因子＋残差≡实际指数；线型编码固定——**色域＝结构性持续因子**（AI持续性·青蓝 #4a7ba6 域／证伪退款·青碧 #2e7d6e 域／杂质·浅灰域）、**金细线（#b8912c·1.4px）＝事件性**（地缘·报复夜）、**细虚线＝不确定性**（ƒ·朱红 #b23b2e 1.4px 虚线／残差·灰虚）、**墨线独粗＝实际指数**。事件日用当日数据重算重绘；非事件日保留最近事件日版并标注日期。写好 HTML 后用 mcp__cowork__update_artifact 更新 id=event-attribution-ledger（该工具若为 deferred 先 ToolSearch 加载）；
   ③ 给 Doctor 简报（≤10 行）：昨日是否事件日／新记账行／对准结果／新提案（如有，注明「批准后才改带并写变更记录」）／缺数与待跑命令块／下一验证窗。
8. 权重带的任何更改：只能由 Doctor 在后续会话批准后、由那次会话执行（改注册表＋变更记录追一行：日期·因子·旧带→新带·依据·批准语原文）。本定时班永不执行本步。
9. 若台账 md 本班有改动，简报末尾附 brain 仓 git 命令块（cd ~/Documents/Claude/brain → git status --short → git add 仅本班改动文件 → git diff --cached --check → git commit -m "剑酒青丘: 事件归因值守记账 {日期}" → git push），交 Doctor 终端，禁 git add -A。