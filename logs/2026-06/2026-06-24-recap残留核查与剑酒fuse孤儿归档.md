---
title: 会话日志 2026-06-24 — recap复盘库残留核查 + 剑酒fuse孤儿辨认归档
tags: [log, 烛照九阴, 剑酒青丘]
created: 2026-06-24
updated: 2026-06-24
status: active
type: log
project: 烛照九阴
---

# 会话日志 — 2026-06-24

**项目**：烛照九阴（recap.db 残留收尾）+ 剑酒青丘（fuse 孤儿辨认）
**主题**：复盘库 wal/shm 残留真机核查；顺扫撞见剑酒 10 个 .fuse_hidden 辨明为旧版代码、归档处置

---

## 完成的工作

- **核 recap 复盘库残留**：只读扫，主库 `Database/烛照九阴/recap.db` 本体**无任何 -wal/-shm/.fuse_hidden** → DELETE 模式 + 上次真机清那轮已把复盘库本体收干净。Doctor 本题严格说**已基本归零**。
- **定位唯一真 -shm 孤儿**：`Projects/Financial/烛照九阴/db/.fuse_hidden000000cf00000001`（32768B，头 `18e2 2d00` = SQLite WAL-index 魔数；所在目录仅 schema.sql、无 live 库 → 死孤儿，0 数据可再生）。给原生终端 rm 命令（先验魔数再删）。
- **拦截误删**：全盘另有 10 个 `.fuse_hidden` 在 `剑酒青丘/strategies/` 下，**大小各异（4–18KB，非 32768）**。第一反应「全是 -shm」被验头推翻——它们是**真 Python 策略/回测代码**（带 shebang），FUSE 改名遗留的孤儿。若照「孤儿一律删」会删活代码，踩「不删/可逆」红线。
- **逐个 diff 辨明**（Doctor 选「先出 diff 报告再定」）：10 个孤儿与同目录现行正名 `.py` 比对，每个仅差 1–2 行，且差异**全是同一模式**——孤儿=优化前旧实现（`config.stock_universe`+逐股 `load_bars` / 无缓存 `return config.load_bars`），现行版=批量/缓存优化后（`iter_bars # ⚡批量` / `_bars_cache` 全表缓存 `load_all_bars`）。结论：孤儿唯一「独有」内容就是被性能重构主动替换掉的慢代码，现行版是其改进超集，**丢弃零损失**。
- **给处置命令**：合并一段原生终端 block——①清 recap 侧 -shm；②剑酒 10 孤儿先 `cp` 归档到 `Database/_archive/剑酒_fuse_orphans_20260624/`（保留相对路径）核对数量=10 后再 `find -delete`；③复核全树无 .fuse_hidden。沙箱不碰 FUSE 写。

## 做出的决策

| 决策 | 原因 | 影响 |
|------|------|------|
| recap 本题判「已基本归零」，不 overclaim「还有残留」 | 主库实测无 wal/shm，唯一 -shm 在 db 开发目录非 live 库 | 诚实收口；只剩 1 个无害死孤儿待清 |
| 剑酒 .fuse_hidden 验头/验内容后才定性，不信「孤儿=垃圾」直觉 | 验头发现是真 .py 代码，大小≠32768 → 非 -shm | 避免删活代码；分流为「代码孤儿」独立处置 |
| 剑酒孤儿走「归档后删」而非直接 rm | 守 Doctor 不删/可逆铁律；虽证明是旧版仍留退路 | 归档在 _archive，可随时拷回 |
| 两件事（recap -shm / 剑酒代码）全程分开讲、分开处置 | 同名 .fuse_hidden 但性质天差（垃圾 vs 代码），混为一谈即误删 | propose-then-confirm 守住 |

## 遗留问题 / 待办

- [ ] Doctor 在 macOS 终端跑合并命令：清 recap -shm + 剑酒 10 孤儿归档后删 + 复核全树无 .fuse_hidden。
- [ ] （观察项·继承）recap.db DELETE 模式下是否出现 `database is locked`；若有给直连工具统一加 busy_timeout。
- [ ] （可选·非本题）`Database/烛照九阴/` 下今日多个 `recap.db.bak_*_predelete` 备份可择期精简，非 wal/shm 残留。

## 相关笔记

- [[烛照九阴]] · [[剑酒青丘]]
- 归档落点：`Database/_archive/剑酒_fuse_orphans_20260624/`（待 Doctor 跑命令后生成）
- 前序：[[2026-06-24-recap库转DELETE止shm孤儿泄漏]]（DELETE 迁移 + 清 82 个 .fuse_hidden）
