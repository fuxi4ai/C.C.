---
title: 会话日志 2026-06-14 — DVA ASR端到端复验·卡北京区OSS
tags: [log, DVA]
created: 2026-06-14
updated: 2026-06-14
status: active
type: log
project: DVA
---

# 会话日志 — 2026-06-14

**项目**：DVA
**主题**：接续「ASR submit/poll 分段实装」——Doctor 加 TOS/OSS 白名单后端到端复验，定位最后一堵墙是 DashScope 结果 OSS 区域错配

---

## 完成的工作

- **白名单探针复验**：经代理 curl 三域，按「`000`=代理拒绝 / `200/403/404`=已穿透源站」判读——上次被挡的 `*.volces.com`（TOS）与 `*.oss-cn-shanghai.aliyuncs.com` 现均回 `403`（已放行），`dashscope.aliyuncs.com→404`（早通）。
- **复用 retest 脚本下载又踩 stale 坑**：`sandbox-cdn-retest.sh` 把临时配置写死 `/tmp/dva_retest.yml`，上次会话残留该文件属主非本用户 → `PermissionError` → 回落读旧 yml 指向 readonly db。改为**内联**下载、yml+db 都用唯一 `/tmp/dva_e2e_$$_ts` 路径绕过（与 GOTCHAS-006 同类，但这次是 yml 不是 db）。
- **改用已有视频测 ASR**：内联下载因磁盘已存在文件被 `Skipped`，遂直接取 `Downloaded/老毛聊交易/...7647130810704809254.mp4`（8MB）做被测体。
- **`--submit` 端到端通关**：音频提取(0.79MB) → 上传 TOS **OK** → 提交任务拿 `task_id=f646c88e...` → 状态落盘。**-007 的 TOS 403 墙随 `*.volces.com` 白名单彻底解除**。
- **直查 DashScope 任务**：`task_status = SUCCEEDED`，转写已完成；从响应里抓到结果 host = `dashscope-result-bj.oss-cn-beijing.aliyuncs.com`（北京区）。
- **`--poll-once` 卡在拉结果**：`Tunnel connection failed: 403 Forbidden`（**代理 CONNECT 拒绝**，非源站 403）。探针实证：sh 区 `403`（放行）、**bj 区 `000`（被挡）**——上次待办里 `*.oss-cn-shanghai` 是推测、区域猜错了。
- **持久化任务状态免重跑**：把 SUCCEEDED 任务的 state 从 /tmp（跨会话清）挪到挂载盘 `dyd/.asr_pending/7647130810704809254.json`，附 finalize 指引。
- **回写 GOTCHAS**：-007 改标「大部解除」；新增 **-008**（北京区 OSS 错配 + 代理回码判读铁律）；通用教训段补区域修正注。

## 做出的决策

| 决策 | 原因 | 影响 |
|------|------|------|
| 最后一堵墙判为白名单区域错配、非代码 bug | `--submit` 全通、任务 SUCCEEDED，仅 poll 拉 bj 区结果被代理 000 拒 | 待 Doctor 加 `*.oss-cn-beijing` + 新会话，零改代码 |
| 建议 Doctor 直接放 `*.aliyuncs.com` 而非逐区加 | 结果 OSS 区域可能随任务/模型路由变动，逐区猜会反复撞墙 | 一次放行覆盖全 OSS 区，免再猜区 |
| 任务状态挪挂载盘、不重下不重提交 | ASR 任务已在 DashScope 侧 SUCCEEDED 持久；transcription_url 24h 过期但 re-poll 重签 | 新会话 `--poll-once --state` 直接 finalize，省 ASR 配额+下载 |
| retest 脚本 yml 路径硬编码列为待修 | 与 db 同类 stale-属主坑，脚本只把 db 改唯一、漏了 yml | 下次顺手把 yml 也改唯一路径（见待办） |

## 遗留问题 / 待办

- [ ] **Doctor 加 `*.oss-cn-beijing.aliyuncs.com`（或更稳 `*.aliyuncs.com`）白名单 + 开新会话**。这是 DVA 沙箱全链路最后一堵墙。
- [ ] 放行后新会话直接 finalize：`python3 dva_asr.py --poll-once --sec-uid MS4wLjABAAAAzQQWlig6l3YHeqY94V3IWiHo5m19cS7yQ-V02_Rne7k --state dyd/.asr_pending/7647130810704809254.json`，确认拿到完整字幕 + TOS 清理 + 状态文件删除。
- [ ] 闭环后把 ASR 分段接回 `update-all`/harvest 链路，由 agent 逐段驱动 watchlist 各视频，DVA Update 定时任务才真正端到端自动。
- [ ] 修 `sandbox-cdn-retest.sh`：把硬编码 `/tmp/dva_retest.yml` 改唯一路径（与 db 一致），避免 stale-属主 PermissionError。

## 相关笔记

- [[系统概览]]（DVA）
- 上篇日志：[[2026-06-14-DVA-CDN通关与ASR分段实装]]
- 权威坑库：`Projects/DVA/GOTCHAS.md`（新增 [INFRA-20260614-008]）
- 待 finalize 任务：`Projects/DVA/dyd/.asr_pending/7647130810704809254.json`
