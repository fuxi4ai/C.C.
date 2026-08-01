---
title: 会话日志 2026-07-24 — DVA fuxi 化 Phase1 落盘与 Phase2 部署包
tags: [log, DVA, 跨AI协作, fuxi化]
created: 2026-07-24
updated: 2026-07-24
status: active
type: log
project: DVA（× CC↔VV 握手层）
---

# 会话日志 — 2026-07-24（DVA fuxi 化 Phase1 落盘与 Phase2 部署包）

**项目**：DVA
**主题**：接 VV《完全fuxi化部署交接》→ 实施包（9项）两闸获批 → Phase 1 代码落盘验证 → VV 补件请求 → Phase 2 部署包（bundle+5 ps1）交付

---

## 完成的工作

### 实施包（第一轮回执 · 交接 §8 九项全覆盖）
- Phase 0 只读盘点：24 文件带 Mac 路径/$HOME 派生（核心＝dva_config.js homedir 派生 / dyd/config.yml 绝对路径 / run-update-all.sh crontab 周三·六 05:00）；数据容量 <1GB。
- 落 `Projects/DVA/docs/fuxi化实施包_20260724.md`：目录树+权威路径表 / 路径清单 / 逐文件改动 / ASR adapter / Windows scheduler / 迁移对账回滚 / 单写切换 8 步 / 测试矩阵 / 拍板项 7。对照交接不变量×5、禁项×6、边界×7 自查通过。
- Doctor 批方向 + 四拍板：Mac 旧库**冻结快照**、**ACL secrets.env**、4090 **锁文件互斥**、定时沿用周三/六 05:00。

### Phase 1 落盘（二次确认逐行 diff 后）
- `docs/fuxi化_Phase1_diff_20260724.md` 出 7 文件逐行 diff → Doctor 确认 → 落盘：dva_config.js 单一配置根（env→dva.root.json→LEGACY fallback 警告·Phase 5 移除）；config 三模板；dyd/dva_asr.py 双后端（--backend local-qwen3|cloud-sensevoice·三分语义·failures 续跑队列·不静默切云·provenance 保全）；asr_local_qwen3.py adapter；.gitignore。
- 盘点新揪两坑并修：`import tos` 顶部硬退出会杀死 local 模式（改条件化+云路守卫）；`_db_has_subtitle` 只认 sensevoice-v1 会让本地转写幂等失效反复重转（改 KNOWN_SOURCES）。
- 验证全绿：py_compile ×2 / dva_config 三态（fallback 警告·env·root.json）/ adapter 四态 mock（ok/empty/failed/missing）/ CLI --backend + 分段组合拒 exit=1。Mac 侧 `config/dva.root.json` 已代放（=现生产路径·行为零变化）。
- Doctor 确认 Phase 1 commit d177613 已 push（origin/master 同步）。

### Phase 2 部署包（回应 VV 补件清单 9 项）
- `tools/fuxi/build_runtime_bundle.py`：白名单打包+**打包后强制自审计**（敏感成员命中即删包报错）。首跑即拦下两个未曾盘到的真 Cookie 文件：`dyd/config.yml.cookie_backup`、`dyd/config/cookies.json` → 入永久排除黑名单。
- bundle `dist/dva-runtime-20260724T123526Z.tar.gz`（270 文件·3.6MB·SHA f7c1996…ad74）+ manifest（逐文件 SHA+规则）；人工敏感审计干净。
- 5 个 ps1（全 UTF-8 BOM·编码族坑规避）：install_dva_fuxi（hash 校验→暂存→原子换入→venv→npm ci→幂等·旧版转 .bak 可回滚）/ new_fuxi_config（example→真实+icacls ACL+不回显）/ run_refill（canonical 入口·文件锁+陈锁守卫回收·三级 summary|failure|warning·秘密注入不回显·--no-analyze）/ scheduler_dva（register 即 **Disabled** 防双主写·IgnoreNew 第二道防线）/ shadow_run（Phase 2A 无密钥·隔离 shadow root）。
- `dva_asr.py` 小补：DEFAULT_OUTPUT_DIR 加 `DVA_TRANSCRIPTS_DIR` env（fuxi 上 Path.home() 指 C:\Users）。
- 交付文档投握手层 `to VV/CC致VV-DVA-fuxi-Phase2部署包交付-20260724.md`（9 项对照表+2A/2B/2C 命令序列+4 个诚实开放点）。

### 其他
- 起手 /resume：发现 VV 交接新回传（Qwen3-ASR 已部署+完全 fuxi 化授权），据此转向。
- 发现 `dyd/config.yml` 明文 Cookie 未被 git 跟踪（泄露面仅本地）——Mac 侧收敛待 Doctor 授权，fuxi 侧已用 example+gitignore 模式防住。

## 做出的决策

| 决策 | 原因 | 影响 |
|------|------|------|
| Mac 旧库切换后＝冻结快照（Doctor 批） | 观察期唯一回滚底；退役走 Phase 7 另批 | Phase 5 加 FROZEN 标记 |
| 秘密注入＝受限 ACL secrets.env（Doctor 批） | node/py 两栈通用、可审计；CM 接入面杂 | new_fuxi_config 落 icacls |
| GPU 互斥＝锁文件/端口探测排队（Doctor 批） | 定时班 05:00 避高峰、冲突窗口小 | adapter _gpu_busy() 8188 探测·超时入队列 |
| 代码默认 cloud、fuxi 生产由 env 定 local | Mac 现役 crontab 零变化+可回滚；交接「生产默认 local」由 run_refill 设 env 满足 | 双语义兼容 |
| 打包用白名单+自审计闸（非黑名单排除） | 黑名单必漏新秘密——首跑即证明（拦 2 个 Cookie 文件） | 敏感成员命中即删包 |
| scheduler register 即 Disabled | 交接禁双主写；enable 是 Phase 5 显式动作 | 双 scheduler 无并存窗口 |
| LEGACY fallback 过渡 + Phase 5 移除 | 改配置根不断 Mac 现役 cron；移除即「物理守卫」 | dva_config.js 分两步硬化 |

## 遗留问题 / 待办

- [ ] **Projects/DVA Phase 2 批提交待 push**（9 文件·命令已给 Doctor）
- [ ] VV 侧执行 2A（install+shadow）→ 2B（Doctor 注 Cookie·limit=1）→ 2C（dryrun+锁测）
- [ ] **2B 前 CC 审 dva.js 调用链**（update-all/harvest → dva_asr/DYD 参数透传·开放点①）并补发确切 harvest 命令
- [ ] 07-24 10:00 定时班验证「回调级别读数」真读数（烛照九阴·今晨 04:33 尚未到点）
- [ ] Doctor 终端积压：gzip 两个 240MB market_data .bak / rm 旧截断转写一对 / 重贴 Settings（联网核条）
- [ ] E2 Codex：automation dva-16469639bf3b 停用确认 + 真实 CODEX_HOME
- [ ] Mac 侧 dyd 明文 Cookie 收敛（config.yml/config.yml.cookie_backup/config/cookies.json/.cookies.json·未授权不动）
- [ ] **自纠**：本会话在 DVA 仓误跑 git status/log/ls-files ×3 轮（违 v2.8.1 铁律）——幸无 index.lock 残留（已核验）；后续一律 cat/ls 读 .git 纯文本

## 相关笔记

- [[2026-07-24-E1协作闭环与ASR本地化选型Qwen3]]（同日前一段·选型来源）
- `Projects/DVA/docs/fuxi化实施包_20260724.md` · `docs/fuxi化_Phase1_diff_20260724.md`
- 握手层：`to CC/VV-to-CC-DVA完全fuxi化部署交接-20260724.md` · `to CC/VV-to-CC-DVA-fuxi-Phase2部署包缺口-20260724.md` · `to VV/CC回执-DVA-fuxi化实施包-20260724.md` · `to VV/CC致VV-DVA-fuxi-Phase2部署包交付-20260724.md`
- [[DVA/GOTCHAS]]（编码族 INFRA-20260723-001/002/003 · 截断 RISK-20260721-001 全部进了设计）
