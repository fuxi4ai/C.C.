---
title: Codex 自动化层（真源结构与判读）
tags: [codex, automation, 环境, 参考]
created: 2026-09-22
updated: 2026-09-22
status: active
type: reference
---

# Codex 自动化层 — 真源结构与判读

> **一句话**：Codex 的定时任务/自愈 heartbeat 的真源是 `~/.codex/automations/{id}/automation.toml`；那本 2.8 MB 的 `.codex-global-state.json` **是状态不是配置**。
> 2026-09-22 定位（DVA 自愈链诊断场 · 全链只读实读）。

## 一、真源在哪（别找错地方）

| 路径 | 是什么 | 陷阱 |
|---|---|---|
| `~/.codex/automations/{id}/automation.toml` | **配置真源**（调度、prompt、状态） | —— |
| `~/.codex/automations/{id}/memory.md` | 该 automation **跑过**会写 | ⚠ **不能反推**：没写 ≠ 没跑（见 §4） |
| `~/.codex/.codex-global-state.json` | 2.8 MB **状态/会话文本**，含大段 chat | 关键词命中的可能是聊天正文里的引用，**不是配置** |
| `~/.codex/session_index.jsonl` | 线程索引（`id` / `thread_name` / `updated_at`） | 似乎**只在改名或建档时追加**，不能当「每次运行都留痕」的铁证 |
| `~/.codex/logs_2.sqlite` · `thread_history_1.sqlite` · `state_5.sqlite` | 日志/线程历史 | 体积 **710 MB / 1.35 GB / 178 MB** —— 别乱翻 |

⛔ **探测铁律：禁止对 `~/.codex` 做递归 grep**。整个目录 **4.4 GB**，一次 `grep -rls` 就能把终端挂死（本场实测踩过，Doctor 不得不 `⌃C`）。要查就读**单个 TOML** 或对**单个文件** grep。

## 二、`automation.toml` 字段

```toml
version = 1
id      = "dva-fuxi-mac"
kind    = "heartbeat"          # heartbeat | cron
name    = "DVA 有界自愈闭环"
prompt  = "……"                  # 实际行为契约都在这里，语义以它为准
status  = "ACTIVE"             # ACTIVE | PAUSED
rrule   = "FREQ=DAILY;BYHOUR=3;BYMINUTE=15"
notification_policy = "failed_runs_only"
target_thread_id = "01a0aec7-…"   # 运行落在哪条 Codex thread
created_at / updated_at           # 毫秒 epoch
```

## 三、`rrule` 的写法规律（判「能不能触发」的关键）

**在跑的四家一律用裸 RRULE，时间写在 `BYHOUR`/`BYMINUTE` 里，按 Mac 本地时间解释**：

| id | rrule |
|---|---|
| `automation` | `FREQ=DAILY;BYHOUR=5,17;BYMINUTE=30` |
| `usdjpy-15` | `FREQ=DAILY;BYHOUR=6,18;BYMINUTE=30` |
| `dva-2` | `FREQ=WEEKLY;BYDAY=WE,SA;BYHOUR=7;BYMINUTE=0` |
| `after-hours-2` | `FREQ=WEEKLY;BYDAY=SU,MO,TU,WE,TH;BYHOUR=18;BYMINUTE=45` |

- **本地时间实证**：`automation` 的 5:30/17:30 与既有记录「Codex automation 05:30/17:30 **PT**」严丝合缝。
- ⚠ **`DTSTART;TZID=…` 前缀的写法与在跑者不同形**——`dva-fuxi-mac` 原本写作
  `DTSTART;TZID=Asia/Shanghai:20260919T181500\nRRULE:FREQ=DAILY;INTERVAL=1`，
  其 `RRULE` 里**没有任何 BYHOUR/BYMINUTE**，触发时刻全押在 `DTSTART` 那一行。2026-09-19 由 VV 改型为 `FREQ=DAILY;BYHOUR=3;BYMINUTE=15`（PT 03:15 ＝ 北京 18:15），**09-20 首验触发成功**。
- ⚠ **冬令时漂移（全体共性）**：BYHOUR 按 Mac 本地时间 ⇒ 一律硬编码 PT 的班次在 PST 生效后**整体后移 1 小时**（PT 03:15 由北京 18:15 变 19:15）。不是某个 automation 的问题。

## 四、判读三个坑（本场踩过）

1. **`notification_policy = "failed_runs_only"` 是通知策略，不是执行筛选器** —— 它只管「要不要吵人」，与「跑不跑」无关。语义证据在同一个 TOML 的 `prompt` 里（「没有变化且不需用户行动时保持安静；只在完成、实质变化、失败或需要输入时通知」）。**字段名 ≠ 语义**（→ [[通用教训]] G-X191）。
2. **`memory.md` 缺失不能证明「从未运行」** —— 反例：`dva-fuxi-mac` 跑过却没写 `memory.md`。要判「跑没跑」得看该 automation **自己的证据面**（如 DVA 那套看 `dva-codex-supervision/state.json` 的 `observedAt`）。**样本同向不等于必然**（→ G-X190）。
3. **`.codex-global-state.json` 里 grep 到关键词不等于找到了配置** —— 本场 `failed_runs_only` 在该文件命中 6 次，但那是嵌在**字符串值**里的聊天文本；配置正文在 `automations/`。

## 五、本机 automation 清单（截至 2026-09-22）

| id | kind | status |
|---|---|---|
| `automation` | heartbeat | ACTIVE |
| `after-hours-2` | heartbeat | ACTIVE |
| `usdjpy-15` | heartbeat | ACTIVE |
| `dva-2` | heartbeat | ACTIVE |
| `dva-fuxi` | cron | **PAUSED** |
| `dva-fuxi-mac` | heartbeat | ACTIVE |
| `eal-shadow-only-18-10` | cron | **PAUSED** |

## 相关

- [[DVA自愈链]]（该链的消费者就是这里的 `dva-fuxi-mac`）
- [[通用教训]] **G-X190 / G-X191 / G-X192**
- 与 brain 侧调度器（`~/Gateway-workspace/Scheduled/`）是**两个独立的执行面**，别混。
