---
name: cockpit-snapshot
description: 影子驾驶舱夜间快照:三时钟状态落 cockpit.db(append-only)+ OOS 台账成熟(次一自然日)
---

影子驾驶舱夜间快照任务(PRD: brain/logs/checkpoints/2026-07-17_驾驶舱标签页_PRD.md)。

执行(用 bash,沙箱路径):
1. cd /sessions/<会话>/mnt/Database/龙鱼-标的分析库(以实际挂载路径为准;若 Database 未挂载,先用 request_cowork_directory 挂 ~/Documents/Database)
2. 先跑 `python3 snapshot_cockpit.py --dry-run` 看锚定交易日与覆盖数;
3. 再跑 `python3 snapshot_cockpit.py` 实写。

判读与纪律:
- 脚本以 market_data.db 的 MAX(trade_date) 为数据驱动锚,不信系统时钟;句芒日更(北京16:30)后运行即取到 T-0;若上游未更,本次写的是旧锚快照,幂等设计下次自愈,无需干预。
- 全部写入为 INSERT OR IGNORE:同锚重跑"新增 0"是正常幂等表现,不是故障。
- 绝不 UPDATE/DELETE cockpit.db(触发器会拒绝);绝不写 recap.db / market_data.db;绝不跑 git 写命令。
- 若报 disk I/O error:检查是否有残留 cockpit.db-journal 热文件,可用 python 截断为 0 字节后重跑(先 dry-run)。
- 输出简报:锚定日、覆盖标的数、三表新增行数、累计行数。仅在异常(连续两日锚不前进/新增 case 异常暴增/脚本报错)时在简报中显式标注 ⚠ 请 Doctor 关注。