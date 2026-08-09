---
name: longyu-weekly-dualscorer
description: 龙鱼标的库周更：常更标的每周双scorer打分(deepseek子项+claude top-down)落库+对比校正队列+刷新个股库看板artifact
---

【口径切换注记 · 2026-08-02】本班自 2026-08-02 起迁入 Kimi K3 壳执行：第 3 步「claude 腿」**赛道名保留**（续 6 个月趋势序列之连续性），执行模型 = Kimi K3（原 research-CC / Fable 5）。切换点已在 `Database/龙鱼-标的分析库/趋势/` 打桩；换腿初期 |Δ|≥15 入队潮属**基线重置预期现象**，按「分歧解决方法论」逐只消化，并在收尾「方法订正」段显式标注。

每周日对「常更标的」跑龙鱼五力**双 scorer** 打分并落库对照+维护6个月趋势，最后刷新个股库看板 artifact。目标：常更标的（A股，港股如腾讯手工不跑）每周各产 deepseek（自下而上·子项累加）+ claude（自上而下·维度级）两套分，落龙鱼库、出对比+待校正队列、刷新6个月分数趋势、刷看板。制度文档：~/Documents/Database/行业研究/consumers/龙鱼五力/双scorer交叉打分制度.md（含「分歧解决方法论」铁律）。

## 环境（每会话一次；bash 各调用独立、无 cwd/env 延续、45s 上限、后台不跨调用存活→长任务分片、引擎腿串行）
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
脚本目录：`~/Documents/Database/行业研究/consumers/龙鱼五力`

## 步骤
1. 取常更 A股清单：`python3 -c "import json;d=json.load(open('$HOME/Documents/Database/龙鱼-标的分析库/常更标的.json'));print(' '.join(c for c in d['常更'] if c.endswith(('.SH','.SZ','.BJ'))))"`
2. **deepseek 腿（自下而上·自动）**：每条 bash 调用跑 1 只（~30s，引擎腿串行）：`cd ~/Documents/Database/行业研究/consumers/龙鱼五力 && timeout 40 python3 score_subitems.py <ts> --write --save-pack` → scorer=deepseek 条目（subscores+打分日期）+ 缓存包 $LYW_PACK_DIR/<ts>.json。超时重试一次，仍失败留『待引擎』继续。
3. **claude 腿（自上而下·你 CC 判分）**：读缓存包 `$LYW_PACK_DIR/<ts>.json`（kg_context 卡位 + business.top5 出货 + valuation_context 估值分位 + financial_score.breakdown 财务真值），按龙鱼 RULES 维度级判分：政策5/技术供需35/竞争25/新赛道15/估值15/财务5。**判分纪律**：① 兑现折扣（赛道β≠公司已兑现）；② 维度正交（净利润→只财务维、估值分位→只估值维，严禁串入供需/技术/竞争）；③ **议价/溢价先看毛利率(高且升=强溢价)、再看供需结构(供不应求=强溢价)，客户集中度≠议价弱**；④ 财务维取引擎 breakdown 合计；⑤ **次新股分位（ERR-20260801-001）：`valuation_context.pct_reliable=false` 时 pe_pct_3y/pb_pct_3y 已被引擎置空、并在 quantitative_signals 发⚠告警——此时相对估值一律以绝对 PE/PB/PS 判，禁据「分位低」给高分**。调 `python3 write_claude_score.py <ts> --six <政策> <技术供需> <竞争> <新赛道> <估值> <财务> --thesis "<一句话>" --pack $LYW_PACK_DIR/<ts>.json` → scorer=claude 条目，不覆盖 deepseek。
4. **对比校正**：`python3 build_dual_compare.py`（|Δ总分|≥15 进待校正队列）。
5. **刷新6个月趋势**：`python3 score_trend.py` → 落 `Database/龙鱼-标的分析库/趋势/常更标的_分数趋势_{date}.md`（两 scorer 6个月分数序列+边际Δ+驱动维+显著变动旗标）。**看边际变化趋势**：谁在升/降、由哪维驱动、有无拐点。
6. **刷新个股库看板 artifact**（GAI 项目卡·深色版 · 版式真源=artifact `longyu-stock-library`，本步只刷数据不碰版式）：
   - 跑 `python3 ~/Documents/Database/龙鱼-标的分析库/_index/build_dark_board.py`。定时沙箱够不到 artifact 文件，脚本会用 `_index/board_template.html`（Doctor 在 Mac 上跑过一次即 bootstrap）+ 本周新数据生成完整 HTML 到 `_index/龙鱼个股库看板_暗.html`。
   - 再用 `update_artifact` 推送：id=`longyu-stock-library`，html_path 指向 `~/Documents/Database/龙鱼-标的分析库/_index/龙鱼个股库看板_暗.html`，update_summary「双scorer周更刷新 · {今天}」。若 update_artifact 读不到该路径，仿 refresh-asset-dashboard 先 `request_cowork_directory` 挂 `~/Documents/Database/龙鱼-标的分析库` 再用挂载点绝对路径。
   - 若脚本提示"尚无 board_template.html（未 bootstrap）"，说明模板还没生成——**跳过推送**，在收尾里提示 Doctor 去 Mac 终端跑一次 `build_dark_board.py` 以 bootstrap 模板。
7. **收尾**：报告 ① 待校正队列（|Δ|≥15 + 两分 + 最大分歧维 + 你按「分歧解决方法论」的诊断：是错误〔修方法〕还是真分歧〔共存〕）；② **本周趋势显著变动标的（⚑）及边际驱动维**；③ 看板刷新结果（已推送 / 因未 bootstrap 跳过）；触发 /save 落档。

## 铁律
- 数据真实性：引擎/DeepSeek 失败留『待跑分』，claude 判分须据缓存包真实数据，不拍脑袋、不放水。
- 两 scorer 并存互不覆盖；scorer 字段区分（claude=research-CC / deepseek=DeepSeek-v4-pro·带subscores）。
- 常更清单唯一真源=`常更标的.json`（Doctor 用 常更标的审核.html 维护）；只跑其中 A股。
- **分歧解决方法论**（双scorer制度铁律）：分歧不简单按哪方来、不折衷；诊断错误→修判分方法（prompt/锚点/RULES）使错误方回归；真分歧（两方无硬伤）→共存。
- 6个月趋势=各记录 analyses[] 时间序列（周更累积、不删历史；趋势器按6个月窗口取）。
- **看板只刷数据不碰版式**：`build_dark_board.py` 只替换 artifact 里 `const PAYLOAD` 一行；CSS/JS（思源宋体·英文数字 Times·GAI 深色卡·左上角标记）以 artifact 为真源。模板 `board_template.html` 由 Mac 上的就地运行自动 bootstrap/更新；定时沙箱够不到 artifact 文件，只能靠模板 + update_artifact。
- **判分方法订正须显式标注**：若本轮因铁律补适用/口径修正造成周环比跳变（非基本面变化），必须在收尾里单列「方法订正」段，否则会污染6个月趋势的边际读数。
- 自主任务：结束写 self-audit，不打 PRD 的 ✓（✓ 只 Doctor 打）。