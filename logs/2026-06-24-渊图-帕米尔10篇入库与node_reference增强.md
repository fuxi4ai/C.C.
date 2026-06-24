---
title: 会话日志 2026-06-24 — 渊图帕米尔10篇入库 + node_reference 判别字段增强
tags: [log, 渊图]
created: 2026-06-24
updated: 2026-06-24
status: active
type: log
project: 渊图
---

# 会话日志 — 2026-06-24

**项目**：渊图（+ 海螺资产看板两条 issue 校正 · 烛照 recap 残留核查）
**主题**：帕米尔 10 篇入库（2613→2711/3262）；入库前给 kg_ingest 的 node_reference 加英文/代码判别锚 + 碰撞过滤（治近名张冠李戴源头）

---

## 完成的工作

### 一 · node_reference 增强（治近名张冠李戴的源头）
- 诊断根因：`kg_ingest.build_node_reference` 早就注入「现有节点」top-120，但每行**只给 id+中文名+category，漏了英文 aliases 和股票代码**——模型见研报里的英文名/代码时无判别锚 → 生益/胜宏、Eoptolink/新易盛那族张冠李戴的源头。图谱 472 家公司：aliases 覆盖 91%（429/472），但 stock_code 仅 16/472。
- 改 `build_node_reference`：每行附 `⟨aliases, stock_code⟩`；并加**碰撞过滤**——alias 若命中「另一家公司」的正名/代码则不注入（从全量 nodes 建碰撞集，高精度·不怕顺序）。
- 眼验当场逮到污染：`company_Tianshu(天数智芯)` aliases 含 `Enflame/燧原科技`（dedup 残留），注入即制造张冠李戴。碰撞过滤滤掉「燧原科技」（中文正名碰撞），但「Enflame」是别名级碰撞、故意不扩（防误删真主）。
- 写 `fix_tianshu_alias_20260624.py` 定向微清天数智芯的 Enflame/燧原科技 alias（备份+守恒断言）。

### 二 · 坏 run 复盘 + 干净重跑
- 首轮入库（Doctor 跑）出三处异常叠加：① 两个 _v2 chunk **不链式**（5篇+4篇各挂 canonical、零重叠）；② 静默跳了**高速EML**1篇（思特威同款）；③ chunk1 建在清 Tianshu 前、带毒基线。查实毒未真触发误连（这几篇没正面碰燧原）。
- 裁定：放弃坏 run，**整批重跑**。写 `unmark_rerun_20260624.py`：清 10 篇 index 标记 + 归档两个坏 chunk 进 `mapping/_badrun_20260624/`（不删·可逆）+ 备份 index。
- 干净重跑（Doctor 单次跑完）：滚动链式正常 _5篇 2657→_10篇 2713，10 篇全捕获，`name_code_consistency_check` **✅ 无告警**（增强 + 清毒见效）。

### 三 · 沙箱 8 项校验 + 本批 7 处修补
- delta gate ✅（_v2 ⊇ canonical）、10 篇全捕获、name↔code 无告警。
- 本批新引入 7 处修补（`fix_batch_20260624.py`·备份+修后自检全绿）：① 悬挂 `昇腾950→product_H20` 重指 `product_NvidiaH200`（H200 已存·desc 支持）；② 删 TGV电镀自环；③ `鲲鹏 constrained_by ARM壁垒`→`ARM壁垒 constrains 鲲鹏`（非法 type 改向）；④ 填半空节点 `concept_MLCCDeliveryLeadtime`(type/name 都 None→concept/MLCC交付周期)；⑤ dedup 3 重复边；⑥⑦ 合并两个重复公司 `TongfuMicroelectronics→Tongfu`、`SourcePhotonicsRevenue2026Q1→SourcePhotonics`（索尔思那个 0 边孤儿）。
- promote：2711/3262 落 canonical（备份+⊇断言），wiki 补卡，Doctor git push。

### 四 · 海螺资产看板两条陈旧 issue 校正（顺带）
- `SMM/web补价`：三坑核实=陈旧——gzip(GOTCHA-024 已修)/SEO标题(GOTCHA-026 稀土摘走web)/代理墙(设计约束非bug)，钨补价正常(asof 06-18)。manifest 改 healthy·issues[]·freshness 重写。结案记入白泽 GOTCHAS 更新日志。
- `recap.db`：wal/shm 残留=彻底根治——journal_mode=DELETE(结构上不再产)·目录零残留·integrity ok。manifest 改 healthy·issues[]。
- 看板 issues 现已全清零，仅剩 market_data.db 一个 stale。

## 做出的决策

| 决策 | 理由 |
|------|------|
| 判别字段补进 canonical 让 node_reference 顺带注入，而非另起平行 prompt 对照表 | 单一真源·自动同步·不漂移；reasoning model 会自信传播表里的错，表必须干净 |
| 碰撞过滤只索引公司正名+代码（高精度），不扩到别名级 | 别名级碰撞顺序依赖、可能误删真主的合法英文名；残留（如 Enflame-on-天数）归 canonical 清 |
| 坏 run 整批重跑而非手工合并两个不链式 chunk | 三异常叠加（不链式+静默跳+带毒），手工合并正是历史出事的脆弱手术；重跑 10 篇短纪要 API 便宜 |
| batch 必须单次不打断跑 | 坏 run 根因=中断/重复调用致各 chunk 挂 canonical 不链式 |
| 6 旧存非规范前缀节点（含 LipidBert/LNP）归 backlog | 非本批引入；LipidBert/LNP 疑 MiroFish 串入渊图，剔除需单独核 |

## 遗留问题 / 待办

- [ ] **backlog（已记 GOTCHAS）**：6 个非规范前缀节点 `market_/technology_/milestone_*` 前缀↔type 不一致待规范化；其中 `technology_LipidBertModel`、`technology_HighThroughputLNPPlatform` 是生物 LNP/LipidBert，疑 MiroFish 内容串入渊图，是否剔除单独核。
- [ ] stock_code 仅 16/472——可 backfill（tushare+易混表种子）让 node_reference 代码锚更全（中等项目）。
- [ ] 海螺看板剩 market_data.db 一个 stale（派生表落后）。
- [ ] 剑酒青丘 10 个 .fuse_hidden 旧版代码孤儿（本会话已出归档命令，待 Doctor 跑）。

## 相关笔记

- [[渊图]] · [[经验库]]（新增 EXP-20260624-001-T FUSE 孤儿处置）
- `kg_ingest.py build_node_reference`（增强）· `mapping/fix_tianshu_alias_20260624.py`、`unmark_rerun_20260624.py`、`fix_batch_20260624.py`
- 前序：[[2026-06-23-渊图-帕米尔7篇入库与修补]]
- 海螺：`Projects/海螺姑娘/data/asset_manifest.json`（SMM/recap.db 两节点校正）
