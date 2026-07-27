---
title: 风险日报 · GOTCHAS（已知坑）
tags: [风险日报, gotchas]
created: 2026-07-27
updated: 2026-07-27
status: active
type: resource
project: 风险日报
---

# 风险日报 · GOTCHAS（已知坑）

> 排查超过一轮的问题都记这里。CC 遇错解决后立即回写。

## 格式

```
## [ERR-YYYYMMDD-NNN] 简要描述
**状态**: ✅ 已解决 / ⏳ 待解决
**优先级**: 🔴 高 / 🟡 中 / 🟢 低
**触发场景** / **错误信息** / **解决方案** / **预防措施**
```

---

## [ERR-20260727-001] VoteHub Polling API 返回裸数组，非文档写的 {"polls":[...]}
**状态**: ✅ 已解决
**优先级**: 🟡 中（动 VoteHub / 类似 beta API 必踩）
**触发场景**: `fetch_taco_components.py` 用 VoteHub 取特朗普支持率（`GET api.votehub.com/polls?poll_type=approval&subject=donald-trump`）落 TACO 代理的净支持率分项。终端 --fetch 后 FRED 两项进库、**APPROVAL_NET 没进**。
**错误信息**: 脚本 `json.loads(body).get("polls", [])` —— VoteHub 官方文档示例写响应是 `{"polls":[...]}`，**实际返回的是裸数组 `[...]`**（beta 口径已变）。对 list 调 `.get` 抛 `AttributeError` → 被外层 try 吞 → 该 series 0 行、静默缺失。
**解决方案**: 兼容两种形状——`_d=json.loads(body); polls = _d if isinstance(_d, list) else _d.get("polls", [])`。poll 对象结构确认：`end_date` + `answers:[{"choice":"Approve","pct":..},{"choice":"Disapprove","pct":..}]`（pct 为 float）；按 end_date 聚合日度净支持率(Approve−Disapprove)。
**预防措施**: ①第三方 beta API 别信文档的响应形状，先 `isinstance` 兜底 list/dict 两种；②脚本里单 series 取数失败**不该静默吞**——外层 try 打印「✗ 原因」已能暴露（本次 Doctor 未贴该行输出、靠 --check 见缺行才发现）；③排障口诀同 [[经验库]] EXP-20260725-001-P：先取一小片真实响应看结构，别照文档拍。
**旁证**: VoteHub `from_date` 语义＝end_date≥该日；2026-07-15 起返回 `[]`（民调周级滞后，最新 approval end_date 到 6 月底/7 月初），非 bug。

---

## [ERR-20260727-002] 沙箱测代理/白名单连通性会误判：3128 全 000 是假象
**状态**: ✅ 已解决（认知纠偏）
**优先级**: 🟢 低（但每次核白名单必踩）
**触发场景**: 白名单开通后想在沙箱验 VoteHub/FRED 是否放行，用 `curl -x http://localhost:3128 ...` 测 → 两源全 HTTP 000。
**错误信息**: 000 被误读为「白名单没生效/源不可达」。
**解决方案**: `localhost:3128` 是**定时任务侧**的代理，**本会话沙箱没挂这个代理** → 走 3128 必然 000（连不上代理本身），与白名单无关。改**直连**（不带 -x）测：VoteHub 200、FRED 301，可达。
**预防措施**: ① 沙箱直连 ≠ 定时任务代理路径——白名单管的是**代理路径**，沙箱直连测不到它，要验白名单只能看**下一班定时任务的 fetch 步**或 **Doctor 终端 `--probe`**（公网直连）；② 沙箱核「数据能不能取到」用直连即可，核「白名单/代理放行」得换环境；③ 别把 3128 的 000 当白名单失败的证据。

---

<!-- 在下方追加新条目 -->
