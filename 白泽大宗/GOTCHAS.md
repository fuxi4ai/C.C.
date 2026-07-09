---
title: 白泽大宗 · GOTCHAS
tags: [白泽大宗, gotchas]
created: 2026-06-10
updated: 2026-07-09
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
