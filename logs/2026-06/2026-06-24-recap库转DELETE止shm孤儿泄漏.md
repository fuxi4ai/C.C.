---
title: 会话日志 2026-06-24 — recap库转DELETE止shm孤儿泄漏
tags: [log, 烛照九阴]
created: 2026-06-24
updated: 2026-06-24
status: active
type: log
project: 烛照九阴
---

# 会话日志 — 2026-06-24

**项目**：烛照九阴
**主题**：recap.db WAL→DELETE 模式切换 + 清 .fuse_hidden（-shm）孤儿

## 完成的工作

- 诊断 Doctor 提的「recap.db-wal/-shm 残留」：实测 `recap.db-wal`=0 字节（已 checkpoint）、`integrity_check=ok` → 该残留本身无害、无数据风险，属「库正常被打开」态。
- 定位真问题：`Database/烛照九阴/` 下 **82 个 `.fuse_hidden`**（每个 32KB，字节头 `18e2 2d00` = SQLite WAL-index/`-shm`），系 WAL 库在 FUSE 会话里未干净关闭、被 FUSE 改名遗留的 `-shm` 孤儿，日期跨 6-15→6-23。
- 沙箱尝试 `PRAGMA journal_mode=DELETE` → `disk I/O error`，之后连只读也报错，`rm .fuse_hidden` 被拒（`Operation not permitted`），且失败尝试反让计数 81→82。判定沙箱 FUSE 处理不了 WAL 退出/unlink，**停手改原生**。
- 中途一度误判 `.fuse_hidden` 「可能是挂载假象」，经 Doctor 原生 `ls` 核出 82 个真盘实体文件，纠回第一判断（确是真盘垃圾）。
- Doctor 在 macOS 终端原生执行：`integrity_check=ok`、`journal_mode` 切成 `delete`、`recap.db-wal` 消失；清掉 82 个 `.fuse_hidden` + `recap.db-shm` + `Projects/db` 空壳 wal，剩余 0，目录只剩 `recap.db`。
- 改码 `tools/recap_db.py` `get_conn()`：`journal_mode=WAL`→`DELETE` + 加 `busy_timeout=5000`；Doctor commit `2fc97ce`。

## 做出的决策

| 决策 | 原因 | 影响 |
|------|------|------|
| recap.db 改 DELETE 单文件模式（弃 WAL） | 复盘库几乎无并发读写；WAL 的 `-shm` 反而是 FUSE 下 `.fuse_hidden` 泄漏源 | 从源头堵住孤儿；单文件利备份/同步；代价是并发撞锁概率略升，由 `busy_timeout=5000` 兜底 |
| 直连工具的 busy_timeout 暂不铺 | 避免一次动十几个文件、scope 失控 | 真撞 lock 再补 |
| 库锁/unlink 类 fs 操作不在沙箱做 | 沙箱 FUSE 实测会报 I/O error 并再生孤儿 | 一律构造命令交 Doctor 原生终端 |

## 遗留问题 / 待办

- [ ] 观察 DELETE 模式下是否出现 `database is locked`；若有，给十几个直连工具（signal_winrate_backtest / gen_daily_report / stock_extractor 等）统一加 `busy_timeout`。
- [ ] `com.apple` 后台进程（Spotlight/QuickLook 类，PID 当时 28944）只读开着 recap.db——无害，若 `-shm` 复现可留意。

## 相关笔记

- [[烛照九阴]]
