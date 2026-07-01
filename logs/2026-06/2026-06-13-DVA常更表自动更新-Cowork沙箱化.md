---
title: 会话日志 2026-06-13 — DVA常更表自动更新·Cowork沙箱化
tags: [log, DVA]
created: 2026-06-13
updated: 2026-06-13
status: active
type: log
project: DVA
---

# 会话日志 — 2026-06-13

**项目**：DVA
**主题**：把 DVA 常更表更新从「哑火的本机 cron + 只读哨兵」改造成「Cowork 计划任务自动采集+转写」

---

## 完成的工作

- 诊断现状：`dva-update-all-reminder` 原本只是只读哨兵（查本机 cron 跑没跑）；本机 cron 自 6/10 起从未部署成功（`Projects/DVA/logs/cron/` 至今不存在），常更表数据落后≥1 周。
- 定 scope：与 Doctor 对齐为**只下载+转写、分析手动**（分析步的 DeepSeek key 在 `~/.dva_secrets`，沙箱只挂载 Documents、读不到；TOS/DashScope key 在 `dyd/.env.dva` 可读）。
- 摸清链路依赖：node v22 + ffmpeg + python3 在沙箱在位；下载步 `dyd/run.py` 需 py 包 aiohttp/aiofiles/aiosqlite/rich/pyyaml/python-dateutil/gmssl；转写 `dva_asr.py` 仅标准库走 REST（无需额外包）；运行命令 `node dva.js update-all --no-analyze`。
- 把任务从哨兵改写为自动执行任务（in-place 改 prompt+description+notifyOnCompletion）。
- vendored python 依赖到挂载盘持久目录 `dyd/.sandbox_pydeps`（39M，7 包导入全 ok），加进 `dyd/.gitignore`；任务运行时 `export PYTHONPATH` 指向它，**运行时不碰 pypi**。
- 冒烟测试 `dva watch list`（只读、不下载/不耗 ASR）通过：HOME 覆盖在真实配置加载器里生效，读到 6 位作者（老毛聊交易/投知君君/卷宇宙漫谈/黑盒调查局/独夫之心/浪浪Insight），watchlist 路径正确解析到挂载盘。

## 做出的决策

| 决策 | 原因 | 影响 |
|------|------|------|
| 三坑解法定型 | ①bash 单命令 45s 上限 → 后台 nohup + 轮询日志（进程跨调用存活，只约束单命令不约束总时长）②沙箱 os.homedir()=/sessions/<会话> 非 Mac 家目录 → `export HOME=挂载根` 修正（config.db.root 用 homedir 拼）③沙箱每次全新 → py 依赖 vendored 进挂载盘 + PYTHONPATH，免 pypi 白名单 | 三条均为**跨项目通用**的 Cowork 沙箱化模式 |
| 分析步永远 --no-analyze | DeepSeek key 在家目录沙箱不可达；TOS/DashScope 在 Documents 可达 | 采集+转写全自动，分析留 Doctor 手动在 Mac 跑 |
| 凭证就地用不迁移 | dyd/.env.dva 已在 Documents 可 source | 无需 Doctor 动 key |

## 遗留问题 / 待办

- [ ] Doctor 点「Run now」做端到端真跑验证（会真下载+耗少量 ASR）：确认抖音 cookie 仍有效、TOS/DashScope 凭证可用。下次自动触发周三 6/17 05:08。
- [ ] 冒烟告警 `Playwright未安装，connectOverCDP不可用`——浏览器 cookie 刷新可选通道；若真跑时下载报 cookie 错可能与此有关，待观察。
- [ ] vendored 依赖含 native ext(aiohttp/pyyaml)，绑定沙箱 Python 3.10.12；若沙箱镜像升级 python 版本，导入会失败 → 任务已内置自检报警，届时重新 vendor。
- [ ] 本机 cron 方案可考虑废弃（已被 Cowork 任务取代），run-update-all.sh 暂留。

## 后续状态更新（同日·首跑后复盘）

- **首跑失败**，暴露两堵墙，部分推翻原设计：
  1. **沙箱网络=HTTP 代理(localhost:3128)强制白名单**：本地 DNS(getent)一律失败属正常；代理对 douyin `curl` 返回 **403**。**关键澄清(Doctor)**：白名单**需新会话才生效**——当前会话早于加白名单，故 403；并非 douyin 加不进。→ 新会话里 douyin 应可通；且 DVA aiohttp 下载器默认不走代理，需在 dyd 配置里指定 proxy=http://localhost:3128。
  2. **后台进程不跨 bash 调用存活（实测确认·环境约束·新会话不变）**：30s 纯写文件 nohup 进程，下一调用只 2 行且 PID 已死。→ **"后台+轮询绕 45s"方案作废**（经验库 EXP-20260613-005-P 已标⛔已证伪）。长任务(下载+ASR 数分钟·不可分段)不适合沙箱。
- **任务现状**：显示名已改 `DVA Update`（SKILL.md name 字段）；Doctor **驳回了"暂停任务"**的改动，任务保持启用（会定时触发并失败，直到改路线）。
- **下一步（新对话 /resume 后）**：① 先在新会话验证 douyin 经代理是否已通(`curl -I https://www.douyin.com`)；② 若通，试 dyd 配置加 proxy + 评估能否把 update-all 拆成 ≤45s 分段由 agent 逐段驱动；③ 若仍受 45s/无后台所阻 → **回退 Mac 本地 launchd 自动化**（douyin 通、无 45s 限、cookie/凭证/依赖现成，最初该走的路）。
- 开场建议：「resume；DVA Update 转 Mac launchd（或先验证 douyin 新会话是否已通）」。

## 相关笔记

- [[系统概览]]（DVA）
- 任务文件：`Scheduled/dva-update-all-reminder/SKILL.md`
- 脚本：`Projects/DVA/run-update-all.sh`（旧本机 cron 方案，待废）
