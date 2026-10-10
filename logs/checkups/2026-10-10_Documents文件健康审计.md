---
title: Documents 全目录文件健康审计
tags: [checkup, 审计, 文件健康]
created: 2026-10-10
updated: 2026-10-10
status: active
type: log
---

# Documents 全目录文件健康审计（2026-10-10）

> 只读扫描 · 零修改 · 方法＝find 分目录分批落清单（FUSE 遍历慢，全树一次 find 超时，改为按一级目录分扫：4AI/AI4ME/Trips/Vault/Codex 一轮、Claude 按二级目录 20 个、brain maxdepth 7、Database maxdepth 6+9）→ python 聚合。**.git 已排除**。

## 一、总量

- **总文件 768,211 · 76.13 GB**（排除 .git；含 .git 为 79.2 万 / 86.1 GB）
- 一级目录 8 个：4AI · AI4ME · Claude · Codex · Database · Trips · Vault · __pycache__ ＋ 根散件 1 件

## 二、类别分布

| 类别 | 件数 | 体积 |
|---|---|---|
| 备份件（.bak*/backups/_bak/） | 465,596 | 47.9 GB |
| 其他 | 102,122 | 19.1 GB |
| 媒体 | 9,379 | 7.2 GB |
| 数据文件 | 48,178 | 6.2 GB |
| 打包件 | 292 | 2.0 GB |
| 归档件（archived/_DEPRECATED_） | 3,365 | 1.7 GB |
| 代码/页面 | 125,143 | 1.7 GB |
| 办公文档 | 764 | 1.5 GB |
| 无用·pyc 缓存 | 16,606 | 314 MB |
| 无用·fuse 残影 | 42 | 220 MB |
| Markdown | 17,245 | 144 MB |
| 日志 | 269 | 14 MB |
| 无用·DS_Store | 405 | 4 MB |
| 无用·DB 日志残片（-journal/-wal/-shm） | 50 | 3.4 MB |
| 复验/审计报告 | 173 | 2.7 MB |
| 无用·临时 | 297 | 0.4 MB |
| 无用·零字节 | 2,911 | 0 |

## 三、主要发现（按影响排序）

1. **`.dva-mirror/backups/` 17 代快照 · 25.3 GB**——Database 下 DVA 镜像链的备份代次（大代 ~2.4 GB×8＋小代 ~0.85 GB×9，两型交替）。最新代 2026-10-10。**清理口径归 Doctor**（DVA 增量链的备份策略）。
2. **Database 大库 .bak 727 件 · 22.5 GB**——attribution.db / market_data.db 等大库历史备份堆积（单件 GB 级）。其中按「备份体系四层」判据，属可再生的库备份。
3. **Codex 树 23.3 万件 · 17.3 GB**（排除 .git）——Project Mirror 活树，非问题。
4. **时间戳异常**：.dva-mirror 备份内大量文件 mtime=1970（「20736 天前」）——时间戳写入缺陷或 FUSE 异常，报 DVA 线留意。
5. **无用残留合计 ~540 MB**：pyc 1.66 万件 314MB · fuse 残影 42 件 220MB（同 FUSE 竞写族）· DS_Store 405 · DB 残片 50 · 临时 297 · **零字节 2,911 件**。
6. **Documents 根残留**：`eal-step1-tmp-lock-patch-2026-09-23.py`（一次性补丁脚本）+ 根级 `__pycache__/`。
7. **陈旧度健康**：>180 天仅 651 件（841MB 的大头是旧媒体/库）、>365 天 316 件 841MB——整体不严重。

## 四、未核（如实标）

- Codex 深树仅 maxdepth 6 覆盖第一轮（23.9 万件），更深层未穷尽——Codex 树体量按已扫值报。
- 「其他」类 19.1GB 未细分（多为 Codex 镜像的杂类文件与二进制）。
- 扫描期间（00:5x-01:1x）各生产班次/镜像链在运行，统计是**时点快照**。

## 五、处置建议（归 Doctor 裁 · 本轮零动作）

- A. dva-mirror 代次保留策略（现 17 代，建议定「保留最近 N 代」上限）
- B. Database 大库 .bak 归档/清理（按可逆优先：归档优先）
- C. 零字节 2,911 件与 pyc/fuse 残影的例行清理
- D. Documents 根残留两件处置
