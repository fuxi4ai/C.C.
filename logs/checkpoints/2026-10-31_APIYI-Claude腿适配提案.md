---
title: 提案 — APIYI·Claude 腿适配（龙鱼双 scorer 跨模型独立性恢复）
tags: [提案, 龙鱼五力, APIYI, dualscorer, 引擎]
created: 2026-10-31
updated: 2026-10-31
status: 提案待批（未实施）
type: checkpoint
project: 龙鱼五力
---

# APIYI·Claude 腿适配提案

> **状态：提案待批，未实施。** 目标＝把 dualscorer 的 claude 腿从「随壳 DeepSeek Pro」接到 APIYI 转接的真 Claude，恢复双腿跨模型独立性。

## 背景与现状（盘上实读证据）

- **班**：`longyu-weekly-dualscorer`（cron `0 22 * * 6`，周六 22:00 PT；下一班 2026-11-01 22:00 PT）。双腿定义：deepseek 腿＝脚本自下而上子项累加；claude 腿＝LLM 自上而下维度级判分（`extract_packs_for_claude.py` 盲打包 → 班次当前模型判分）。
- **claude 腿执行模型沿革**：真 Claude（官方订阅时代）→ 2026-08-02 起 Kimi K3（班 SKILL 口径注记：赛道名保留，续 6 个月趋势序列；执行模型=Kimi K3）→ 当前随 Gateway 主引擎＝DeepSeek Pro（Doctor 2026-10-31 述）。
- **后果**：双腿现跑同一模型 ⇒ Δ 对比队列语义降级为「同模型双路径」，跨模型互证失效，「分歧解决方法论」失去前提。
- **目标格局（Doctor 2026-10-31 述）**：CC 主引擎＝Claude Desktop 映射 DeepSeek API；Claude 模型经 **APIYI 转接**补充。**该适配未做**——盘上 APIYI 落盘记录仅 `brain/O MY HTML/apiyi-transit-mode.md`（05-14 立，仅 gpt-image 图像生成用途），无 Claude 接线、凭证清单无对应条目。

## 改动面清单

| # | 改动面 | 内容 | 状态 |
|---|---|---|---|
| 1 | claude 腿执行机制 | 现结构无独立 API 调用、腿=随壳模型。需新增脚本（暂名 `score_claude_leg.py`）经 APIYI 调 Claude 判 pack，写 records `scorer="claude"`；落库沿 `LYW_*` env 约定 | 待设计 |
| 2 | 凭证与网络 | APIYI 现有 key 仅图像用途；**APIYI 模型目录是否含 Claude 未核**；沙箱出网 `vip.apiyi.com` 是否被 TLS 阻断（出口阻断记忆）**未核**；新凭证登记进 `凭证清单` | 待核 |
| 3 | 班 SKILL（store） | 口径注记（08-02 段）补沿革、第 3 步腿定义改写。⚠ store 最新版沙箱不可读、镜像停 10-04——**改前须 Doctor 终端核 store 现行版** | 待核后改 |
| 4 | 趋势打桩 | 切换点照 08-02 先例在 `Database/龙鱼-标的分析库/趋势/` 打桩；换腿初期 \|Δ\|≥15 入队潮按基线重置预期现象处理，逐只消化、收尾标注 | 待实施 |
| 5 | 制度文档同步 | `Database/行业研究/consumers/龙鱼五力/双scorer交叉打分制度.md` 腿定义段；「Kimi 基线 −8 平移量」旧校准层（对 Kimi 调）切真 Claude 后保留还是重校——待裁 | 待裁 |
| 6 | 降级路径 | APIYI 不可达时 claude 腿 **fail-closed**：本班只跑 ds 腿并报缺腿，**不得静默回落随壳模型**（否则双腿重新同源） | 待设计 |
| 7 | 仲裁位 / equity-thesis 班 | 08-02 旧记录「Kimi 一审/VV 二审/Fable 5 API 仲裁」之后无新落盘；equity-thesis 周更班引擎归属未核。是否同批适配——待裁 | 待裁 |

## 待 Doctor 裁（方向性）

- ~~Q1 切换时点~~ ✅ **2026-10-31 Doctor 裁：缓一周**——目标切换班＝2026-11-07 22:00 PT；本周完成三前提核验+打桩+制度同步。
- ~~Q2 equity-thesis 班~~ ✅ **2026-10-31 Doctor 裁：分批**——先 dualscorer 闭环验证一周，再议 equity-thesis 引擎方案。
- **Q3 仲裁位现状交底**：当前仲裁实际走什么、是否也迁 APIYI Claude——待 Doctor 说明（盘上无记录）。

## 实施前提（缺一不动手）

1. ~~APIYI Claude 模型可用性~~ **❌ 未满足（2026-10-31 沙箱实测）**：出网连通 ✅（vip.apiyi.com HTTP 200 · 0.6s · IP 38.129.137.227）；但当前 key 的 `GET /v1/models` 仅返回 `chatgpt-image-latest` 一个模型，**无 Claude**——待 Doctor 在 APIYI 侧确认/开通 Claude 模型权限。⚠ 另：探测输出中 key 主体字符曾暴露于会话，**建议轮换该 key**。
2. ~~store 现行 `longyu-weekly-dualscorer/SKILL.md` 实读~~ ✅ **已核（2026-10-31 Doctor 终端回读）**：口径注记仍为 08-02 Kimi K3 版（与 10-04 镜像逐字一致，无新沿革注记）⇒「Kimi→DeepSeek」换腿在 store 从未落盘、执行模型系壳级漂移。改班时注记须一次补两段沿革（Kimi K3→DeepSeek Pro、DeepSeek Pro→APIYI Claude）；
3. ~~沙箱出网 `vip.apiyi.com` 连通性~~ ✅ **已核**（2026-10-31 实测，见上）；
4. 制度文档与打桩先行，再切腿。

## 相关

- [[Kimi 壳与订阅格局]] · 模型路由模式记忆（Gateway/官方/APIYI 三层分工）
- `brain/references/scheduled-live-mirror/live/longyu-weekly-dualscorer/SKILL.md`（镜像 10-04 版，store 真源可能更新）
- `Database/行业研究/consumers/龙鱼五力/双scorer交叉打分制度.md`（制度真源）
- `brain/O MY HTML/apiyi-transit-mode.md`（APIYI 现有唯一落盘记录）
- TODO 挂账：龙鱼双 scorer 跟踪包④（Kimi 基线 −8 平移量）
