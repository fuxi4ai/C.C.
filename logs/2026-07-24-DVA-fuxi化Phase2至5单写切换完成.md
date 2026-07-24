---
title: 会话日志 2026-07-24 — DVA fuxi 化 Phase 2-5 · 单写切换完成
tags: [log, DVA, 跨AI协作, fuxi化]
created: 2026-07-24
updated: 2026-07-24
status: active
type: log
project: DVA（× CC↔VV 握手层）
---

# 会话日志 — 2026-07-24（DVA fuxi 化 Phase 2-5 · 单写切换完成）

**项目**：DVA
**主题**：接同日《Phase1落盘与Phase2部署包》——2A→2C 验证、Phase 3 迁移（三缺口+pointers 回填）、Phase 4 dry-run、**Phase 5 单写切换完成**、harvest_one 点单机制
**前一篇**：[[2026-07-24-DVA-fuxi化Phase1落盘与Phase2部署包]]

---

## 完成的工作（与 VV 逐闸迭代 · 五轮修复全部「拦截→修复→重打→通过」）

### Phase 2A/2B/2C（bundle 链 125210Z→130142Z→131318Z）
- **UTF-8 固化**（VV 2A 拦获 GBK 崩溃）：run_refill/shadow_run 加 `PYTHONUTF8/PYTHONIOENCODING`。
- **dva.js 透传 5 硬点**（开放点①兑现）：DYD_DIR/TRANS_DIR homedir 硬编、固定 `/tmp` 临时 config（改 session 唯一）、`python3` 别名 ×3（改 `DVA_PYTHON`）、config 底本读死（改 `DVA_DYD_CONFIG`）、反斜杠注入（统一正斜杠）。
- **DB 守卫 env 化**（VV 2B 首跑被守卫正确拦下）：douyin_database/watchlist 的 `EXPECTED_DB_ROOT` 改 env 优先——守卫语义不变（env≠config 仍拒），三态测过。RISK-20260617-001 前提（采集只在 Mac）失效 → 条目状态演进。
- **bundle 闭包缺口**（VV 2B 二跑拦获）：白名单声明失真（tools/ 三件写成根路径）+ 缺失软告警被 tail 吞 + SHA 不查 require 闭包——三重失守三重修（实况化/硬错误/解包后 `node dva.js` smoke 闸）。立 BUG-20260724-002。
- 2B 真实端到端过：老毛聊交易 limit=1，下载→Qwen3 本地 ASR 739 字→DB/索引，`source=qwen3-asr-1.7b-local-fuxi`，二跑全 skip 幂等，生产 0 污染。2C：DVA-Refill 注册（周三/六 05:00·register 即 Disabled）、dry-run 绿、双实例锁拒 exit=2。
- Cookie 由 Doctor 授权、VV 经 SSH stdin 注入 fuxi config（23 项·ACL 收紧·全程不回显）。

### Phase 3 数据迁移（工具对 + 三缺口修复）
- `export_data_bundle.py`（Mac 侧·SQLite backup API 快照）+ `import_data_bundle.py`（fuxi 侧六步对账·非空拒绝）+ `tar_compat.py`（3.8+ 逐成员安检 shim·UTF-8 stdio 固化）。mock 闭环含篡改拒/穿越拒/非空拒。
- **关键修正（CC 对 VV 方案）**：aweme 表补 offsite 三列不能只 `ADD COLUMN DEFAULT 0`——三列全 0 会让 fuxi 判重把已外移 1556 条当「本地缺失未归档」**恢复性重下 ~20GB**。真相源定位=`DVA-ops/state/pointers/`（两阶段提交产物），export 在快照上回填（backfilled 1388 / unmatched 168=DYD 建库前视频·预期），import 增验 `count(offsite=1)==manifest.backfilled` 防「列在全0」假完备。
- 首轮真实导入：9,389 文件/382MB 六步全过（canonical 在 fuxi Python 3.10.9 直跑）。

### Phase 4 + Phase 5（单写切换 · Doctor 批今晚窗口）
- P4 真数据 dry-run 全绿。P5 四问拍板（今晚切/现场确认 Codex automation）。
- 切换完成态：Codex automation `dva-16469639bf3b`=**PAUSED**；Mac crontab 无 DVA 条目；`FROZEN-20260724.md` 落 Database/Douyin；Mac 生效配置改名 `dva.root.json.frozen-20260724`；`dva_config.js` 移除 LEGACY fallback（无配置 **exit 78 物理守卫**·三态验证）；终版包 `135000Z`（SHA 696675c0…8bd1）六步对账过、offsite=1388 精确一致；首轮 fuxi 数据整树保留 `data.first-round-20260724`；**DVA-Refill=Ready，NextRun 2026-07-25 05:00，单写成立**。
- 首轮数据 shadow/2A/2B 产物不并生产（隔离纪律）。

### harvest_one 点单机制（Doctor 批「ssh 一行」方案）
- 新 `tools/fuxi/harvest_one.ps1`：Mac 一行 ssh 发起单作者采集；`-Url` 自动抽 sec_uid、`-AuthorB64` 防 ssh 中文乱码、`-AddWatch` 进常更表；与定时班共用 `refill.lock` 全局串行。单视频链路未验证、暂不开放（防单链不 seed 坑）。

## 做出的决策

| 决策 | 原因 | 影响 |
|------|------|------|
| P5 窗口=今晚现在切（Doctor 批） | 明早 05:00 首班即实战验证；回滚=重启 crontab 一行 | 一天内 Phase 0→5 收官 |
| offsite 迁移=加列**+pointers 回填**（修正 VV 的默认0方案） | 全 0 触发判重状态机恢复性重下 ~20GB | export 回填+import 计数对账双闸 |
| 首轮/终版两轮制（终版=停写后重导）代替增量同步 | 300MB 重打成本低于增量逻辑复杂度 | 终版 135000Z 为权威基准 |
| 点单机制=ssh 一行+harvest_one.ps1（非 inbox 队列/人肉转） | 零新基建、同步可见输出；与定时班同锁防并发 | Doctor 日常入口保住 Mac |
| bundle 白名单缺失=硬错误、构建输出禁 tail 截断读 | 软告警+管道截断=零告警（闭包断链根因②） | 打包器永久防线 |

## 遗留问题 / 待办

- [ ] **07-25 05:00 fuxi 首个生产班核验**（LastTaskResult=0 / summary level / exit_code / warning_hits·warning 按 WARNING 原样报）
- [ ] Phase 6 观察期：≥2 定时周期（07-25 + 07-29）+ 一次 F:\ 备份恢复演练 → 报 Doctor
- [ ] DVA 仓最终提交批待跑（dva_config 守卫+Phase3 工具+harvest_one 等·命令已给）
- [ ] VV 验证 harvest_one（-Limit 1 + 锁互斥）；单视频点单链路待 shadow 验证后开放
- [ ] Phase 7（Mac 旧副本/first-round 数据/shadow 清理）另行申请，观察期后
- [ ] E2 余项：memory.md 并回真实 CODEX_HOME + `$CODEX_HOME/` 目录清理（automation 已 PAUSED，确认闸过）
- [ ] 分析层（Level1/LLM）仍在 Mac、未迁——后议

## 相关笔记

- [[2026-07-24-DVA-fuxi化Phase1落盘与Phase2部署包]]（同日前篇·实施包与 Phase1）
- 握手层本段：`to CC/` VV 回执 ×6（2A/2B守卫/2B闭包/2B2C完成/P3三缺口/P3P4完成/P5完成）·`to VV/` CC 交付 ×7
- `Projects/DVA/GOTCHAS.md`：BUG-20260724-002 · RISK-20260617-001 演进
- 实施包 §7（切换八步全兑现）
