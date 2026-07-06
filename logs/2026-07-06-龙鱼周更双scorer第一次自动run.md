# 2026-07-06 · 龙鱼周更双scorer · 首次自动 run（longyu-weekly-dualscorer）

> 类型：Cowork Scheduled 自主任务 · 执行者：CC（research-CC）· 项目：龙鱼五力

## 做了什么

- **deepseek 腿**：常更 A股 19/19 全部成功（score_subitems.py --write --save-pack，无超时无『待跑分』）。腾讯（00700.HK）按制度不跑。
- **claude 腿**：19/19 读缓存包（kg卡位/top5出货/估值分位/财务真值）按 v2 口径判分落库（write_claude_score.py，scorer=claude，不覆盖 deepseek）。
- **对比校正**：build_dual_compare.py → `对比校正/全库_对比_20260706.md`，覆盖 92 只，待校正队列 16 只（本周常更占 7）。本周 7 条的 CC归因 已按「分歧解决方法论」填入文件。
- **趋势**：score_trend.py → `趋势/常更标的_分数趋势_20260706.md`，deepseek 腿 19 条已全 v2 可信；claude 腿仍混杂口径（本周为 claude v2 第 1 个点，可信趋势还需 1-2 周累积）。

## 关键发现

1. **本周常更分歧全部为 Δ>0（deepseek 普遍高于 claude v2）**——与制度预设的「deepseek 严 / claude 松」相反，是系统性信号：deepseek 子项锚点在「行业β/卡位叙事」上兑现折扣不足。
2. **诊断结论（7 条）**：
   - 错误(deepseek)：奥比中光 +26（营收+6.2% 却按人形机器人赛道β打高供需）、华工科技 +22.5（毛利率19.8%↓仍给高议价/供需）、中芯国际 +18.5（偏错误，营收+8%/净利+0.4% 兑现弱）。
   - 真分歧（共存）：联讯仪器 +18、胜宏科技 +16、长飞光纤 +15、炬光科技 +16（偏真分歧，建议锚点补盈利质量校验）。
3. **建议修方法（待 Doctor 审）**：score_subitems.py ANCHORS 增两条——① 供需子项须以公司营收/出货增速为兑现证据（赛道β≠公司兑现）；② 毛利率<25%且下行 → 议价子项封顶 2。修完重跑奥比/华工/中芯三只验证回归。
4. **趋势边际（deepseek 可信口径）**：⚑无（运营Δ≥3 无标的）；升——中际旭创 运营Δ+2（供需/出货强化，现分 87 组内最高）；**降——铖昌科技 运营Δ−6（组内唯一显著转弱，军品交付节奏拖累）**，值得盯。

## 遗留

- [ ] deepseek 锚点修正案（上面两条）待 Doctor 批 → 修后重跑三只验证收敛。
- [ ] claude 腿 v2 第 2 个点下周日产生，之后 claude 趋势才可信。
- [ ] 队列中 9 条非常更标的（振华科技 −29 等）是旧 claude 分（06-27）vs 新 deepseek 分的跨期对比，归因暂缓，待该批 claude 分重打后再诊断。

## Self-audit

- 数据真实性：两腿 19/19 全真实落库，无拍脑袋分；claude 判分全部基于缓存包真值（毛利率/增速/分位/KG）。
- 纪律遵守：财务维取引擎 breakdown；估值分位只入估值维；议价先看毛利率再看供需；未覆盖任何 deepseek 条目。
- 环境备注：沙箱 /tmp/packs 无写权限 → 用 LYW_PACK_DIR 重定向（会话级目录，缓存包不持久，不影响落库产物）；build_dual_compare/score_trend 需 HOME 指向挂载盘（已处理，首跑误写沙箱 home 已清理）。
- 未打任何 PRD ✓（✓ 只 Doctor 打）。

## Git（Doctor 在 macOS 终端跑）

```bash
cd ~/Documents/Claude/brain && git add logs/2026-07-06-龙鱼周更双scorer第一次自动run.md && git commit -m "log: 龙鱼周更双scorer首次自动run（19只双腿落库+队列归因+趋势）" && git push
```
