---
tags: [DVA, log, cron, 哨兵]
date: 2026-06-14
created: 2026-06-14
updated: 2026-06-14
type: log
title: DVA 常更表自动更新（cowork 计划任务）
status: 失败
---

# DVA 常更表自动更新 — 哨兵日志

## 结果
**失败**。本轮 0 位作者成功，新增视频 0、字幕 0。

## 经过
- 环境自检全部通过：vendored 依赖（aiohttp/aiofiles/aiosqlite/rich/yaml/dateutil/gmssl）导入 OK；node_modules 在位；`dyd/.env.dva` 凭证文件存在。
- `node dva.js update-all --no-analyze` 启动正常，进入【作者 1/6】老毛聊交易 的 harvest 流水线（DYD 下载，limit=20）。
- 在 DYD 下载步骤失败并终止。

## 失败项与原因
1. **域名解析失败（主因）** — DYD 请求 `www.douyin.com:443` 报错：
   `Cannot connect to host www.douyin.com:443 ssl:default [Temporary failure in name resolution]`
   即沙箱无法解析 douyin.com。**douyin.com 域名很可能未加入沙箱白名单**，导致所有抖音采集无法进行。
2. **disk I/O error（次生）** — 用户信息拉取失败后 DYD 数据库写入报 `disk I/O error`，属网络失败后的连带异常，非独立问题。
3. Playwright 未安装告警（`connectOverCDP 不可用`）— 历史性告警，不阻断主流程，可忽略。

## 建议给 Doctor
- **核心**：在沙箱网络白名单中加入抖音相关域名（至少 `www.douyin.com`，可能还需 `*.douyinpic.com` / `*.douyinvod.com` / volces / dashscope）。当前白名单不含 douyin.com，自动采集无法运行。
- 若域名已在白名单仍解析失败，需检查沙箱 DNS 配置。
- 待白名单修好后重跑本计划任务；分析步仍由 Doctor 手动在 Mac 跑。

## 补充观察
- 后台 `nohup ... &` 的子进程在 bash 调用结束后未存活（沙箱每次 bash 调用相互独立），故首轮后台日志只有表头。实际错误经前台 `timeout 30` 手动复现确认。下次可考虑前台分段跑，但本质问题是网络白名单，先解决该项。
