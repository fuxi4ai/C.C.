---
title: 白泽大宗 · GOTCHAS
tags: [白泽大宗, gotchas]
created: 2026-06-10
updated: 2026-08-06
status: active
type: resource
---

# 白泽大宗 GOTCHAS

- **G-01 周报 MD 位置**：`build_weekly_report.py` 的 MD 是**单份滚动**落 `PROJ/周报/白泽周报_最新.md`（每周覆盖、零历史）；AI4ME outputs 目录**只收看板 HTML**（dated + 定名版）。别再去 outputs 找 MD。（2026-06-10 修正 Scheduled SKILL.md 漂移）
- **G-02 local_prep_health.json 可能为空 `{}`**：Mac 侧 weekly_local_prep.sh 未跑成或被覆盖时如此。按"健康未知"处理——以 live store 实际新鲜度为准，不臆断 cron 成败。
- **G-03 build_weekly_report.py 验证法**：改模板后在沙箱镜像目录实跑验证（拷 PROJ 到 /tmp/verify/Documents/ 下保持 Documents 祖先名，脚本 `_documents_root()` 即自动指向镜像，不污染真实交付物）。2026-06-10 已用此法验证 06-09 改造：MD 与周日版同长、七节齐全、看板含待核验斜纹+置信徽。
- **G-04 配置权威源**：`configs/config_index.json` 为准（main_config=白泽大宗_v4.1.yaml）；CONFIG_INDEX.md 是人读摘要，曾滞后标 v3.0（2026-06-10 已同步，今后改配置两处一起动）。
- **G-05 tushare-cache 仅 27 只标的**：是白泽取数缓存，不是全市场名单，不可用于 ST 识别/全市场统计。
- **G-06 模板/artifact 字体壳分叉（技术债）**：看板 artifact `baize-weekly-dashboard` 的「系统中文衬线回退栈（Songti/STSong/SimSun）+ 去 Google Fonts 外链」只做在**产物侧手工壳**，**未并入** `_HTML_TMPL`。故每次从脚本重渲都得重套这层壳；下周日 Stage4 自动重渲若未先并模板，产出的 artifact 会缺系统回退栈（外链字体加载慢/失败时中文降级难看）。根治＝把这两项并进 `_HTML_TMPL`，让重渲直接产出 artifact 格式。（2026-07-09 涨价卡改多列时手工补壳发现）
- **G-07 沙箱直写挂载盘 db 留热 journal（2026-08-06 实撞）**：对本库 business_breakdown.db 直接 UPDATE，commit 半途 disk I/O error 留 41KB 热 journal，此后连只读 open 都报 disk I/O error（要回滚 journal 而写入被拦）。处置：`: > business_breakdown.db-journal` 清零 → 备份 cat 恢复 → 改库全程在 /tmp 副本做、`cat /tmp/x.db > 挂载路径` 覆写回；只读查询用 `file:...?mode=ro` URI。注意 /tmp+cat 已裁定**仅应急**（通用教训 G-X131），常规写库走停写窗口+backup API+原子替换+查并发。
- **G-08 真源 JSON 品种级 source 挂治理文本（2026-08-31 例行自查发现·当日处置）**：`data/stocks_fundamentals.json` 13/14 品种的 source 字段自 08-09 起挂着「年报/投资者问答(P0) · 待逐项标注采集日期」——「待逐项」是治理挂账文本，混进真源数据字段，随 warehouse 投影进 db 的 `benefit_relations.commodity_source`（47/48 行带挂账标记）。处置（Doctor 裁「按范本改口径」）：13 品种 source 改写为「年报/投资者问答(P0) · 披露期 2026-03~04」，核查事实留行级 `verified` 字段（30/48 行有 07-09 核查、18 行无，品种级不写核查句防以偏概全）；范本=覆铜板「2025年报(P0) · 渊图候选补采 2026-06-25」。**预防门禁**：挂账/待办文本不得进真源数据字段——治理欠账记 TODO/札记，数据字段只放事实口径；同类检查=改库前 grep 真源 JSON 的「待/暂/TODO」字样。
- **G-09 钨价 SMM 抓数量级错（2026-08-31 实撞 · 待修复）**：`commodity_prices_live.json` 钨条目 price=**1333 元/标吨**（asof 08-31 · SMM h5 黑钨精矿≥65%），与历史量级差 ~163 倍（proxy_prices 527500 元/标吨·06-12；config 锚 2025 年均 21.79 万/标吨），change_yoy 算出 **-99.4%**——钨价不可能跌 99%，系 SMM h5 抓数错误（疑 row_match 抓错行/单位，GOTCHA-026 稀土同族）。**放大器**：weekly_health 只查 asof 新鲜度不查量级合理性 → 错价带「age 0 新鲜」进入周报/弹性（-99.4% yoy 污染钨弹性排序），健康层不暴露。触发：2026-08-31 氦气喂入场 Doctor 报告+CC 实读坐实。**修法候选（归 Doctor）**：① 重抓 SMM 钨价核数；② 摘钨出 SMM 走中钨在线（信源图谱已列免费可爬·GOTCHA-026 同款处置）；③ fetch_smm_h5 加量级守卫（品种合理区间校验，偏离历史均值超阈值报警）。状态 🔄 待修复。
