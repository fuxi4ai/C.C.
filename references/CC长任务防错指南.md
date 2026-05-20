---
title: CC 长任务防错指南
tags: [reference, gotchas, 长任务, 防错, API错误]
created: 2026-05-20
updated: 2026-05-20
status: active
type: reference
parent: brain/permanent/通用教训
upstream: anthropic-api-errors-cheatsheet.md
---

# CC 长任务防错指南

> **场景**:Doctor 委托长时间无人监督的大型任务(凌晨批量 / "自主进行不用问询" / 跨小时连续工作) · CC 中途报错 → 进度丢失 → 浪费时间。
>
> **元规则**:**不依赖"不出错" · 依赖"出错也能从最近 checkpoint 继续"**。
>
> **上游权威**:`brain/references/anthropic-api-errors-cheatsheet.md`(完整 API 错误清单)· **本文档** = 长任务场景的实战提炼。

---

## §一 · 核心方法论:Checkpoint 机制(★★★ 必读)

长任务最大的风险**不是哪类错误码** · 而是**错误 → 进度丢失** 的传导链。Checkpoint 机制是唯一的根本防御。

### 1.1 什么是"独立工作单元"

可以独立落盘的最小完整产出物:
- ✓ 写完一个哲学家条目(15 KB)= 一个工作单元
- ✓ 完成一个章节的修订(framework v1.1 → v1.2)= 一个工作单元
- ✓ 跑完一个 batch 文件入库(37 个 PDF)= 一个工作单元
- ✗ "想了 5 分钟下一步怎么做" = 不是工作单元(没产出)
- ✗ "改了 3 个文件第 1 个的第 5 行" = 不是工作单元(不完整)

### 1.2 Checkpoint 三铁律

**铁律 1 · 每完成一个独立工作单元 → 立即落盘**
- 不积累 2 个以上未落盘单元
- 落盘 = Write/Edit 到 `~/Documents/Claude/...` 实体文件 · **不是**在 CC 上下文里"记着"
- 写完即落盘 · 不等"做完一批一起落"

**铁律 2 · 每 5-10 个工作单元 → 写一个"进度标记"文件**
- 路径建议:`~/Documents/Claude/brain/logs/checkpoints/{任务名}-progress.md`(或项目内部 PROGRESS.md)
- 内容:**已完成清单 + 当前工作单元 + 下一步队列 + 关键决策**
- 作用:即便 CC 崩溃 / 上下文丢失 / 报错中断,Doctor 或下一个 CC 会话能从这份 PROGRESS.md 续上

**铁律 3 · 高风险操作前 → 先写一个 dry-run 草稿落盘**
- 如批量 sed / 跨多文件 Edit / rm 类操作:**先 Write 一份"将要执行的命令清单 + 影响文件列表"到 logs/ · 再实际执行**
- 即便操作失败 · 也能从清单恢复

### 1.3 检查点的"颗粒度"

不能太密(每分钟写 progress)也不能太疏(整个会话末尾才落):

| 任务长度 | Checkpoint 频率 |
|---|---|
| < 30 分钟 / 单一文件改 | 完成时落盘即可 · 不需 progress 文件 |
| 30-120 分钟 / 跨文件改 | 每 3-5 个工作单元写一次 progress(覆盖式) |
| 2-6 小时 / 跨子项目改 | 每 5-10 单元写一次 progress · 每小时强制写一次 |
| > 6 小时 / 凌晨连续任务 | 每个工作单元都立即落盘 · 每 5-10 单元写 progress · **每 30 分钟强制写一次 progress + Doctor 监控点**(发消息或写 ping 文件) |

---

## §二 · 长任务的 6 类高频错误 · 分级防御

### A · 上下文耗尽(★★★ 最致命)

**报错**:
- `400 invalid_request_error · Prompt is too long`
- `Error during compaction: Conversation too long`

**为什么对长任务最致命**:整段会话死锁 · 连 `/compact` 都跑不动 · 必须 Esc 回退几轮 · 之前几轮的工具调用产出全部"在 CC 记忆里" 但不在文件 · 全丢

**长任务诱因**:
- 大量 Read 大文件(每个 2000+ 行)累积
- 多 MCP server 连接(每个吃几 K-几十 K token system prompt)
- 长对话 + 没有 /compact
- 反复读相同文件(应该 cache 在 CC 自己上下文 · 但 CC 会"忘"于是重读)

**防御**:
1. **主动监控**:每完成 5-10 个工作单元 · 跑一次 `/context`(若不可直接调用 · 至少心算估算:大文件读次数 × 行数)
2. **大文件用 head_limit / offset**:`Grep --head_limit 250` · `Read --limit 200`(不读 2000 行全文)
3. **不读大目录的 ls**:Glob 比 Bash ls 高效 · 避免一次列 1000+ 文件
4. **关闭不用的 MCP**:任务开始前 Doctor 关闭无关 MCP(Claude in Chrome 等)
5. **主动 /compact**:对话感觉"长"(估算 100K+ token)立即 /compact
6. **死锁兜底**:若已 `Conversation too long for compaction` · **Esc 回退几轮再 /compact** · 不要继续往里塞内容

**CC 自查触发词**:看到自己即将"Read 第 5 个 2000 行的大文件"/"开第 3 个 MCP 工具"/"对话已超过 50 轮" → 停 → /compact 或落盘 progress

---

### B · 工具历史错乱(★★★ 极致命)

**报错**:
- `400 ... tool use concurrency issues. Run /rewind to recover`
- `400 ... unexpected tool_use_id found in tool_result blocks`
- `400 ... thinking blocks ... cannot be modified`

**为什么对长任务极致命**:整轮被废 · `/rewind` 回退到错前那轮 → 期间所有工具调用产出"在 API 历史里" 但 CC 看不到 · 不知道哪些已经做了 / 哪些没做

**长任务诱因**:
- 工具调用中途被打断(网络抖动 / Doctor 误操作 Esc / 服务端重启)
- 并发工具调用 + 部分失败 + 部分成功(tool_use/tool_result 配对错乱)
- thinking 块被尝试编辑(罕见 · 通常是 SDK 层问题)

**防御**:
1. **不在工具调用密集段做高风险操作**:批量 Edit / 跨文件 sed 之前 · 先把"将要做什么"写到 progress 文件落盘
2. **并发工具调用要谨慎**:同时发多个工具调用时 · 确保每个都是独立可恢复的 · 不互相依赖中间状态
3. **`/rewind` 恢复后**:**第一件事是读 progress 文件** · 不是凭记忆继续(记忆已经被 /rewind 截断)
4. **如果碰到 `unexpected tool_use_id`**:不要重试 · /rewind 或两次 Esc 回退到错前那轮

**CC 自查触发词**:报错含 "tool_use" / "tool_result" / "concurrency" → 不重试 → 走 /rewind 流程

---

### C · 速率限制 429(★★ 严重)

**报错**:`429 rate_limit_error` · header 含 `retry-after` + `anthropic-ratelimit-*`

**为什么对长任务严重**:长任务密集调用必撞 RPM/ITPM/OTPM 任意一根 · 或撞**加速度限制**(从静态飙升到 100 路并发会先扔 429)

**长任务诱因**:
- 一次性发 10+ 并行工具调用(并发突刺)
- 跨多文件批量改 · 没节流
- ITPM 累积(prompt 缓存没开 · 每轮重发完整 system prompt)

**防御**:
1. **加速度爬坡**:任务开始前 60 秒内**逐步增加并发度** · 不要一开始就 10 路并行
2. **限制单次并行工具数**:≤ 3-5 个(Claude Code 默认 `CLAUDE_CODE_MAX_TOOL_USE_CONCURRENCY` · 调小避免 429)
3. **prompt caching**:长系统提示 / tool definitions / 对话历史都该被缓存(`cache_read_input_tokens` 不计入 ITPM)→ 有效 ITPM × 3-10
4. **遇 429 看 retry-after**:**严格等够再重试** · 不要立即重试
5. **遇 429 看哪根撞了**:RPM(降并发) / ITPM(开缓存 + 减历史) / OTPM(拆分输出)

**CC 自查触发词**:看到自己即将一次发 5+ 工具调用 → 拆成 2-3 批 · 中间留间隔

---

### D · 平台过载 529(★★ 严重 · 不可控)

**报错**:`529 overloaded_error` · `retry-after` **不可信**

**为什么对长任务严重**:长任务在线时间长 → 撞到的概率高 · 且不受用户控制 · 不是你的配额问题是 Anthropic 全局问题

**防御**:
1. **指数退避 + jitter**:重试间隔 1s → 2s → 4s → 8s + ±20% 随机抖动 · 不要等距重试
2. **重试上限 2-3 次** · 不要无脑重试 10 次(Claude Code 默认 10 次 + 指数退避 · 但 SDK 自实现要设上限)
3. **必要时切提供方**:AWS Bedrock / GCP Vertex AI 同款 Claude 有独立配额(Cowork 用户做不到 · 这是 SDK 用户的方案)
4. **避开高峰时段**(美西 UTC-8 工作日白天最容易 529)· 凌晨任务时段(中国凌晨 = 美西下午)可能反而是峰段

**CC 自查触发词**:连续 3 次 529 → 暂停任务 → 写一个 progress 记录 "停在 X 位 · 待 Doctor 决定下一步" → 让 Doctor 来恢复

---

### E · 单步超时 504(★ 中等)

**报错**:`504 timeout_error`(非流式请求硬上限 10 min)

**为什么对长任务有影响**:单次推理输出过大(如一次性 Write 10000+ 行)会撞 · 撞了就整轮丢

**防御**:
1. **不让单次 Write 超过 1000 行**:大文件分多次 Write · 或者先 Write 骨架 → 多次 Edit 填血肉
2. **不让单次推理生成超过 5000 token**:大段内容 / 长报告 拆为多次输出
3. **大型 batch 用 Batches API**(SDK 层 · Cowork 用户做不到)

**CC 自查触发词**:看到自己即将 Write 一个 > 1000 行的大文件 → 拆成多次:先 Write 骨架,再 Edit 填段

---

### F · 请求过大 413(★ 中等 · 少见)

**报错**:`413 request_too_large`(Messages API 32 MB · Claude Code 客户端 30 MB)

**为什么对长任务有影响**:单次工具调用喂入超大文件(如 base64 后的大图 / 大 PDF)

**防御**:
1. **不要一次 Read 单文件超过 5 MB**(Read 工具自动会拒,但要避免)
2. **大 PDF 分页读**:`Read --pages "1-5"` · 不要一次读 100 页 PDF
3. **大图压缩**:单图最长边 ≤ 2000 像素

**CC 自查触发词**:即将 Read 单文件 > 5 MB 或单图 > 2000 像素 → 改用分页/压缩

---

## §三 · 错误决策树(长任务专用)

```
报错出现
├─ 400 系列 → STOP · 不要重试
│  ├─ "Prompt too long" → /compact · 不行就 Esc 回退几轮 · 不行就重新会话
│  ├─ "tool use concurrency" → /rewind · 读 progress 文件恢复
│  ├─ "image too large" / "PDF too large" → 拆分 · 改读法
│  └─ 其他 400 → 告诉 Doctor · 不重试
│
├─ 401 / 402 / 403 (auth/billing) → STOP · 告诉 Doctor · 等他处理
│
├─ 413 → 拆分 · 不重试
│
├─ 429 → 看 retry-after · 等够再试 · 重试上限 3 次
│  └─ 重试 3 次仍 429 → 写 progress · 告诉 Doctor · 暂停
│
├─ 500 / 503 → 退避重试 1-2 次 · 不行写 progress 暂停
│
├─ 504 → 拆分输出 · 不要重试相同的大输出
│
└─ 529 → 指数退避 + jitter · 上限 2-3 次 · 仍失败写 progress 暂停 + 通知 Doctor
```

**核心原则**:**任何"不可重试就解决"的错误都必须写 progress 落盘 · 不能假装没发生继续往下走**。

---

## §四 · 长任务实战清单(给 CC 自己用)

### 任务开始时(60 秒内)

- [ ] 读 Doctor 既有基线(评级 / 颗粒度 / 哪些已经做过)→ 落档到对话上下文
- [ ] 估算任务规模:多少个工作单元 · 总文件数 · 预期耗时
- [ ] 决定 checkpoint 频率(参见 §1.3 表格)
- [ ] 写第一份 progress 文件骨架(任务名 + 总单元数 + 已完成 0 + 队列)
- [ ] 不要一开始就 10 路并发 · 加速度爬坡

### 任务进行中(每个工作单元)

- [ ] 工作单元完成 → 立即 Write/Edit 落实体文件(不是"记着")
- [ ] 单元完成 → 更新 progress 文件的"已完成"+1
- [ ] **每 5-10 单元 + 每 30 分钟** 强制重新生成 progress 文件
- [ ] 看到自己将"Read 第 5 个大文件" / "Write 1000+ 行" / "并行 5+ 工具调用" → 停 · 拆分
- [ ] 看到任何 4xx/5xx 报错 → 走 §三 决策树 · 不无脑重试

### 任务暂停 / 异常时

- [ ] 写最后一份 progress(标 status=paused / status=error)
- [ ] 记录"如何恢复":下一个 CC 会话读 progress 后第一步要做什么
- [ ] 必要时通知 Doctor(连续 3 次 529 / 任何 400 / 任何 401-403)

### 任务结束时

- [ ] 写最后一份 progress(标 status=completed)
- [ ] 给 Doctor self-audit(参 G-X1 第 5 条:本批新升档 N 位 / 偏差基线情况)
- [ ] 触发 brain-save(贴 git 命令给 Doctor 在 terminal 跑 · v2.0 规则)

---

## §五 · 与既有教训的关系

| 教训 | 关系 |
|---|---|
| **G-X1 自主任务质量纪律** | 本指南是 G-X1 的工程层延伸 · G-X1 防"质量坍塌" · 本指南防"进度丢失" · 两者一起构成长任务双保险 |
| **G-X2 sandbox git 禁忌** | 错误决策树里的"写 progress 落盘"自然走 Write 工具 · 不走 git · 不冲突 |
| **5/19 brain_checkup v1.2 sandbox 探测** | sandbox 探测保护脚本不写 git · 本指南保护 CC 自己不撞 API · 是两层防御 |

---

## §六 · 上游引用

完整 API 错误清单 + Tier / RPM / ITPM / OTPM 数据 + 生产监控建议 → `brain/references/anthropic-api-errors-cheatsheet.md`(Doctor 2026-05-20 上传 · 资料源 platform.claude.com 官方文档 + 2026 社区资料)

---

## v 历史

- v1.0(2026-05-20):基于 Doctor 上传 cheatsheet + Doctor 关切(长任务防错)初版
