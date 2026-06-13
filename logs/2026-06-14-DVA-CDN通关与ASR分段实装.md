---
title: 会话日志 2026-06-14 — DVA CDN通关与ASR分段实装
tags: [log, DVA]
created: 2026-06-14
updated: 2026-06-14
status: active
type: log
project: DVA
---

# 会话日志 — 2026-06-14

**项目**：DVA
**主题**：接续 6/14「沙箱采集撞 CDN 白名单墙」——复测确认 CDN 通关、修两处 infra 坑、实装 ASR submit/poll 分段绕 45s

---

## 完成的工作

- **CDN 白名单复测通关**：跑 `tools/sandbox-cdn-retest.sh`，CDN 域探针全放行（`v5-dy-o-detect.zjcdn.com→404`、`v5-hl-ws-ov-coldy.zjcdn.com→403`、`www.douyin.com→200`，均 CDN/源站回码非代理 `000`）；真实下载 3 条 mp4（7.8M/8.4M/14M），`ffprobe` 校验均为完整 ISO MP4（时长 129/137/152s）、属主当前会话用户、单条 limit=1 `Success 1/100.0%`。**6/14 的致命 CDN 墙已彻底解除**。
- **修复 retest 脚本两坑**（先修再装的"修"）：
  - MNT 自动定位：旧逻辑按层数上溯算错 + `ls /sessions|head -1` 兜底 → 抓到陈旧会话名 `admiring-dreamy-heisenberg` → `cd dyd` Permission denied。改为从脚本绝对路径截 `${SELF%%/mnt/*}/mnt`，加 `[ -d $MNT/Documents ]` 自检。
  - db 属主 readonly：`/tmp/dy_downloader.db` 是 6/13 残留、属主 `nobody` → `attempt to write a readonly database`。改 `database_path=/tmp/dva_retest_$$_$(date +%s).db` 唯一路径。
  - 顺手让 step4 产物检查 honor `$DLPATH` 覆盖。修后重跑全绿。
- **回写 GOTCHAS**（权威源 `Projects/DVA/GOTCHAS.md`）：`-001` CDN 墙标 ✅已解除；新增 `-004`(下载通关)/`-005`(MNT 定位)/`-006`(readonly db)/`-007`(ASR 链路 tos SDK + TOS/OSS 白名单依赖)。头部"最后更新"→2026-06-14。
- **实装 ASR submit/poll 分段**（"装"）：`dva_asr.py` 加 `--submit`（提取→上传 TOS→提交 ASR→落盘 `{task_id,tos_key,输出路径}` 状态文件后秒回）和 `--poll-once`（有界 ≤`--max-seconds`(默认40) 轮询；未完退出码 10 pending、完成则写字幕+清 TOS+删状态）。新增助手 `_compute_out_paths`/`_write_transcript_outputs`/`poll_asr_task_once`/`_default_state_path`，全程模式重构为共用、行为不变。编译/导入/flag/幂等跳过/音频提取均自测过。
- **vendor 缺失的 tos SDK**：`.sandbox_pydeps` 当初只 vendor 了 run.py 下载依赖、漏了 ASR 的 `tos`（6/13「仅标准库」判断证伪——它确实 import tos 传音频）。`pip install tos -t .sandbox_pydeps` 已补、`import tos` OK。
- **实测暴露 ASR 第二堵白名单墙**：`--submit` 跑到上传即 `Tunnel connection failed: 403`。探针确认 `dragonpalace.tos-cn-shanghai.volces.com→000`、`tos-cn-shanghai.volces.com→403`（TOS 被挡）、`dashscope-result-sh.oss-cn-shanghai.aliyuncs.com→000`（结果 OSS 被挡）；`dashscope.aliyuncs.com→404`（ASR API 已放行）。

## 做出的决策

| 决策 | 原因 | 影响 |
|------|------|------|
| 推翻 6/14「通配白名单未必能稳救 CDN」的悲观判断 | 复测实证：Doctor 加通配后 CDN 轮换域全放行、mp4 真实下载 100% | 沙箱采集（下载环节）确定可行，路线锁定"沙箱化"而非回退 launchd |
| ASR 绕 45s 用 submit/poll 两段 + 状态落盘，而非后台进程 | 6/13 已证伪"后台进程跨 bash 调用存活"；但**挂载盘文件**跨调用持久（下载产物即证） | 长异步任务的通用沙箱范式：状态落盘 + agent 逐段驱动 |
| TOS 清理推迟到 finalize（不在 submit 删） | DashScope 异步处理期间仍需拉取 TOS 音频 URL，submit 即删会让任务取不到文件 | 与全程模式 try/finally 即时清理不同，分段模式 TOS 生命周期跨两段 |
| ASR 跑不通判为"白名单依赖"而非代码 bug | 代码路径自测到上传边界全 OK，403 来自代理拒绝 CONNECT | 与 CDN 同套路：待 Doctor 放行 2 域 + 新会话，非改代码 |

## 遗留问题 / 待办

- [ ] **Doctor 给沙箱代理加白名单 + 开新会话**：`*.volces.com`（TOS 上传）、`*.oss-cn-shanghai.aliyuncs.com`（DashScope 结果 OSS 下发）。这是 DVA 沙箱全链路第三类域（①下载 ②ASR API 已通 ③转写 TOS/OSS 待放行）。
- [ ] 放行后端到端复验 `dva_asr.py --submit` → `--poll-once`（拿到完整字幕、TOS 清理、状态文件删除）。
- [ ] 通后把 ASR 分段接回 `update-all`/harvest 链路（agent 逐段驱动 watchlist 各视频），DVA Update 定时任务才真正端到端自动。
- [ ] 注：tos 等 vendored 依赖含 native ext，绑沙箱 Python 3.10.12，镜像升级需重 vendor（任务已内置自检）。

## 相关笔记

- [[系统概览]]（DVA）
- 上篇日志：[[2026-06-14-DVA沙箱采集撞CDN白名单墙]]
- 权威坑库：`Projects/DVA/GOTCHAS.md`（[INFRA-20260614-004~007]）
- 复测脚本：`Projects/DVA/tools/sandbox-cdn-retest.sh`
- 分段实现：`Projects/DVA/dyd/dva_asr.py`（`--submit`/`--poll-once`）
