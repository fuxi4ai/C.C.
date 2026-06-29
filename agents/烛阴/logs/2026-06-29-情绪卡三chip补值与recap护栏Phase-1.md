---
title: 会话日志 2026-06-29 — 情绪卡三chip补值与recap护栏Phase-1
tags: [log, 烛照九阴]
created: 2026-06-29
updated: 2026-06-29
status: active
type: log
project: 烛照九阴
---

# 会话日志 — 2026-06-29

**项目**：烛照九阴（金融复盘线 · 烛阴域）
**出场者**：CC（在烛阴项目上做工程；Doctor 指 `/save @烛阴` → 落烛阴档）
**主题**：情绪卡三 chip 补真值 → recap.db 反复损坏排障 → 写库护栏 Phase-1

---

## 完成的工作

- **chip 补值（起点需求）**：日报情绪卡里「晋级率 / 涨停次日溢价 / 连板高度」三个 chip 此前是写死的纯标签。链路诊断：情绪引擎确实算了这三个变量（参与加权打分），但**既没落 emotion_cycle 表、也没传到日报**——两头都断（对比「涨停/跌停」两端都通才显值）。
- 改 `tools/emotion_engine_v2.py`（E1-E3）：`out` 行补 premium/height；schema 缺列则 ALTER 补 `jinji/premium/height`；UPSERT 接线三列（引擎一次 --apply 回填全史）。
- 改 `tools/gen_daily_report.py`（R1-R3）：`em` SELECT 加三列；`D["emotion"]` 加三键；chips 三标签换「带值 + None 兜底回退裸标签」。
- **解封验证**：跑前发现 recap.db 已损坏（详见下）。Doctor Mac 终端还原干净库 + 重跑后，三值落库验证成功——06-26：晋级率 9% / 次日溢价 +0.1% / 连板高度 6。
- **recap.db 反复损坏排障**：定位生成器（scheduled task `zhuzhao-market-fetch-daily-report` → `tools/gen_daily_report.py`）。现库 `malformed database schema (four_dimensions) - orphan index`；当日凌晨已坏过一轮（CORRUPT_0255 / recovered_0255）。
- **探针实测（沙箱）**：文件级 `cp` 覆盖 / `cp 新名+mv 原子替换` 整库放回挂载盘**都安全（各 10/10 ok）**；**对挂载盘库直接 live commit = 8/8 `disk I/O error` + 留热 -journal** → 推翻「cp 覆盖必坏」旧归因，真凶=live 写。
- **只读审计**：全仓写入口分级，护栏当时只在 `_ingest_25/26`（复制粘贴），连 `_ingest_28` 都漏。出 `docs/审计_DB写入口越界清单_20260629.md`（Tier-1 硬编码真盘无护栏 4 个 / Tier-2 走 config 无强制 15 个）。
- **护栏 Phase-1 落地**：`config.py` 加中央硬拒绝护栏 `connect_write(path)`；4 个 Tier-1 迁移（`_ingest_九儿_2026-06-28` / `dedup_kejian` / `xiaobao_position_write` / `bt_xiaobao_pos_3d`，其中 bt_ 只在 --commit 分支单开写连接，读连接不动）。py_compile + 护栏单测全过。
- **文档**：GOTCHAS.md G019 补「2026-06-29 探针复测 + 护栏集中化 Phase-1」更新。

## 做出的决策

| 决策 | 原因 | 影响 |
|------|------|------|
| chip 只补 Doctor 点名的 3 个，不补另 3 个裸 chip | Doctor 裁定（我提了「半图例半指标」一致性顾虑，Doctor 仍选只 3 个） | 该行口径保持现状 |
| 治本走「改生成器」而非手改 Artifact 快照 | 快照每日 07:00 重渲，手改会被覆盖；源头才持久 | 改两个 .py，Artifact 自动同步 |
| recap 还原基用 recovered_0255（至 06-25） | 干净且数据最全（industry_signals 到 06-25 vs preingest 到 06-21） | 06-26 课件维度增量需另行 re-ingest |
| 护栏选「硬拒绝」而非「自动重定向」 | 显式、无暗箱；自动重定向藏 bug、cp-back 仍需人做 | fail-loud 优于默默写坏 |
| 护栏 Phase-1 只做中央护栏 + 4 Tier-1；Tier-2/删旧护栏/cp-back卫生留 Phase-2 | blast radius 小、可审；Tier-2 可被 ZZJY_DATABASE_ROOT 重定向、没那么急 | Phase-2 待 Doctor 另起 |

## 遗留问题 / 待办

- [ ] **Phase-2**：Tier-2 共 15 文件写连接收口到 `config.connect_write`。
- [ ] **Phase-2**：中央护栏生效后，删 `_ingest_25/26` 里复制粘贴的旧护栏，统一到中央。
- [ ] **Phase-2**：cp-back 卫生写进日更 SKILL——放回前确认无 `-wal/-journal`、`cp 新名 + mv 原子替换`、放回后强制 `integrity_check`（非 quick_check）+ 失败自动回滚。
- [ ] 06-26 课件维度增量丢失，需要时跑 `tools/_ingest_九儿_2026-06-26.py` 补回（非阻塞）。
- [ ] recap.db.bak_20260629_emotionv2 是坏库的字节拷贝，可清理；Database/_swaptest_dir 已截 0，可在 Mac `rm -rf`。
- [ ] git：烛照九阴项目仓两个 commit 命令已贴 Doctor 终端待跑。

## 相关笔记

- [[审计_DB写入口越界清单_20260629]]
- [[GOTCHAS G019]]
