# Anthropic API 报错速查手册

> 资料来源：platform.claude.com、code.claude.com、support.claude.com 官方文档 + 2026 年社区资料
> 整理日期：2026-05-20

---

## 一、并发 / 工具相关报错

### 1. 工具并发错误 —— `API Error: 400 due to tool use concurrency issues`

Claude Code 官方错误参考表里专门列出的一类 400 报错，归在 **Tool use or thinking block mismatch** 小节。同一类报错的三种典型措辞：

- `API Error: 400 due to tool use concurrency issues. Run /rewind to recover the conversation.`
- `API Error: 400 ... unexpected tool_use_id found in tool_result blocks`
- `API Error: 400 ... thinking blocks ... cannot be modified`

**真正含义**：发回 API 的对话历史里，`tool_use` / `tool_result` / `thinking` 这三种块的顺序和配对状态被打乱了。最常见的触发点是工具调用被中途打断、或者某一轮内容在流式输出中途被编辑。

**硬性规则**：

- 每个 `tool_use` 块必须紧跟一个对应 `tool_use_id` 的 `tool_result` 块；
- 每个 `tool_result` 块的 `tool_use_id` 必须能在上一条 assistant 消息里找到对应的 `tool_use`；
- thinking 块一旦写入历史就不能被改动。

**恢复方式**：

- Claude Code 中：`/rewind` 或连按两次 Esc 回滚到错误那一轮之前；
- 自己写 SDK：在拼装下一轮消息时把"孤儿" `tool_use` / `tool_result` 一并删掉。

### 2. 与工具并发量真正相关的限制

服务端**不**直接限制"一次请求里能挂几个 tool"，而是用客户端这一侧的工具调用并发把账户打到 429。

| 变量 | 默认值 | 作用 |
|---|---|---|
| `CLAUDE_CODE_MAX_TOOL_USE_CONCURRENCY` | — | 收到 429 时官方建议调小，并同时减少并行 subagent |
| `CLAUDE_CODE_MAX_RETRIES` | 10 | 自动重试次数 |
| `API_TIMEOUT_MS` | 600000 ms (10 min) | 单次请求超时 |

Anthropic 用**令牌桶 (token bucket)** 算法，限制是 RPM/ITPM/OTPM 三维而非固定并发数；瞬时突发只要不打穿令牌桶就允许。

另有一条**加速度限制 (acceleration limit)**：组织用量出现陡峭抬升时，即便没到稳态上限也会先扔 429。官方建议 60 秒内逐步爬坡，而不是一开始就 100 路并发。

---

## 二、429 速率限制报错的精确限制

429 = `rate_limit_error`，响应里一定带：

- `retry-after`（秒）
- `anthropic-ratelimit-*` 系列 header —— 告诉你是 RPM / ITPM / OTPM 哪一根撞了

### Build Tier 阶梯（2026 年 5 月数据，Messages API）

| Tier | 累计充值门槛 | 单月消费上限 |
|---|---|---|
| Tier 1 | $5 | $100 |
| Tier 2 | $40 | $500 |
| Tier 3 | $200 | $1,000 |
| Tier 4 | $400 | $200,000 |
| Monthly Invoicing | 联系销售 | 无上限 |

### 各 Tier 的 RPM / ITPM / OTPM（每模型族独立计量）

**Tier 1**

| 模型 | RPM | ITPM | OTPM |
|---|---|---|---|
| Opus 4.x | 50 | 500,000 | 80,000 |
| Sonnet 4.x | 50 | 30,000 | 8,000 |
| Haiku 4.5 | 50 | 50,000 | 10,000 |

**Tier 2**

| 模型 | RPM | ITPM | OTPM |
|---|---|---|---|
| Opus 4.x | 1,000 | 2,000,000 | 200,000 |
| Sonnet 4.x | 1,000 | 450,000 | 90,000 |
| Haiku 4.5 | 1,000 | 450,000 | 90,000 |

**Tier 3**

| 模型 | RPM | ITPM | OTPM |
|---|---|---|---|
| Opus 4.x | 2,000 | 5,000,000 | 400,000 |
| Sonnet 4.x | 2,000 | 800,000 | 160,000 |
| Haiku 4.5 | 2,000 | 1,000,000 | 200,000 |

**Tier 4**

| 模型 | RPM | ITPM | OTPM |
|---|---|---|---|
| Opus 4.x | 4,000 | 10,000,000 | 800,000 |
| Sonnet 4.x | 4,000 | 2,000,000 | 400,000 |
| Haiku 4.5 | 4,000 | 4,000,000 | 800,000 |

### 几条容易踩的细节

- **Opus 4.x 跨版本合并计量**（4.7 / 4.6 / 4.5 / 4.1 / 4 共用一个池子）；Sonnet 4.x 也是 4.6 / 4.5 / 4 合并。换版本号绕不开限速。
- `cache_read_input_tokens` **不计入 ITPM**（除 Haiku 3.5 带 † 例外），所以 prompt caching 是把有效 ITPM 抬 3–10 倍最便宜的杠杆。
- `max_tokens` 不计入 OTPM，OTPM 按实际生成量实时扣，所以把 `max_tokens` 设大不会"偷"配额。
- "60 RPM" 实际是"1 RPS + 少量突发"，瞬时撞墙照样 429。
- Workspace 可以单独设比组织更低的限速，用于隔离批处理 vs 交互流量。
- 还有一种 429 不是因为你超额，而是**鉴权后的低 tier API key 抢占了订阅认证** —— 用 `/status` 检查活动凭据。

---

## 三、529 与其它 5xx —— 平台容量问题，不计你的配额

| 状态码 | type | 含义 |
|---|---|---|
| 500 | `api_error` | Anthropic 内部异常 |
| 503 | (无固定 type) | 偶发服务不可用，按 529 处理 |
| 504 | `timeout_error` | 处理超时，建议改用 streaming 或 Batches API |
| **529** | **`overloaded_error`** | **Anthropic 全局过载，与你的用量无关** |

### 529 关键差别

- `retry-after` **不可信**；
- 靠它重试解决不了问题。

**生产推荐策略**：指数退避 + jitter 重试 2–3 次后**切换提供方**（AWS Bedrock / GCP Vertex AI 的同款 Claude），三方各有独立配额。

Claude Code 内置最多 10 次自动重试 + 指数退避，重试完仍失败才会展示 `API Error: Repeated 529 Overloaded errors` 给用户。

---

## 四、其他常见报错速查（HTTP 错误码全集）

### 400 `invalid_request_error` — 请求格式/字段错

包含：

- 上面那条"tool use concurrency issues"
- Opus 4.7 / 4.6 / Sonnet 4.6 **不支持 prefill assistant message**
- `thinking.type.enabled is not supported`（Opus 4.7 必须改用 `thinking.type.adaptive` + `output_config.effort`）
- `max_tokens must be greater than thinking.budget_tokens`（thinking 预算吞掉了输出预算）
- `Extra inputs are not permitted`（**网关把 `anthropic-beta` header 吃掉了**）

### 401 `authentication_error` — API key / OAuth 问题

常见变体：

- `OAuth token revoked or expired`
- `This organization has been disabled`（stale `ANTHROPIC_API_KEY` 顶掉了订阅登录）

### 402 `billing_error` — 账单 / 支付问题

### 403 `permission_error` — Key 没有该资源权限

**注意**：「**Credit balance is too low**」这条错经常被官方文档归到这里，但实际**至少触发三种根因**：

1. 真没余额；
2. 选的模型需要更高 tier；
3. key 仍能鉴权但与计费账户脱钩（rotate key 即解）。

### 404 `not_found_error` — 资源/模型 ID 不存在

### 413 `request_too_large` — 请求体超字节数上限

| 端点 | 上限 |
|---|---|
| Messages API | 32 MB |
| Token Counting API | 32 MB |
| Batch API | 256 MB |
| Files API | 500 MB |

Claude Code 客户端层还另有一道 "Request too large (max 30 MB)"。

### 429 `rate_limit_error`

见第二节。

### 500 `api_error`

Anthropic 内部异常。

### 504 `timeout_error`

SDK 对非流式请求设的硬上限就是 **10 分钟**。

### 529 `overloaded_error`

见第三节。

---

## 五、与上下文 / 输入相关的高频 400 子类

| 错误信息 | 含义与处理 |
|---|---|
| `Prompt is too long` | 对话+附件超过模型上下文窗口。处理：`/compact` 压缩、`/clear` 清空、`/context` 查看占用、关掉没用的 MCP server |
| `Error during compaction: Conversation too long` | 上下文已经满到连 `/compact` 自己都跑不完。先 Esc 回退几轮再压缩 |
| `Image was too large` | 单图最长边 **8000 像素**；多图共存时单图最长边 **2000 像素**，否则 400 |
| `PDF too large` | 最多 **100 页 / 32 MB**；超过要拆页或先抽文本 |
| `request_too_large` (413) | 主要由粘贴超大文件触发 |

---

## 六、社区常见、但 Anthropic 自己不主动文档化的两个坑

1. **流式响应里返回 200 后再炸错** —— SSE 流中段失败不会走标准 4xx/5xx，要靠 event 流里的 `error` 事件捕获。
2. **网关 / 代理吞 `anthropic-beta` header** —— 直接表现为 400 `Extra inputs are not permitted`。要么修网关，要么客户端设 `CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS=1`。

---

## 七、可直接监控的响应 Header（生产推荐都打点）

- `retry-after`
- `anthropic-ratelimit-requests-limit` / `remaining` / `reset`
- `anthropic-ratelimit-input-tokens-limit` / `remaining` / `reset`
- `anthropic-ratelimit-output-tokens-limit` / `remaining` / `reset`
- Priority Tier 用户还有 `anthropic-priority-*` 系列

**实操建议**：在网关里看到 `input-tokens-remaining < 10% × limit` 时主动卸载低优先级流量（评测、后台分类），保住交互链路。

---

## 八、生产环境推荐落地清单

1. **早升 Tier**。 中量生产流量直接奔 Tier 3 / 4，不要等第一次 429 才补钱。
2. **开 prompt caching**。 长系统提示、RAG 上下文、tool definitions、对话历史都该缓存。有效 ITPM × 3–5。
3. **每次调用都包 backoff + jitter**。 上限 4–5 次重试。
4. **配 provider 兜底**。 Bedrock / Vertex 同款 Claude 用于 529 切换。
5. **打点 `retry_count` / `final_status` / `provider_used`**。 529 风暴通常很短，但只有图能告诉你。
6. **Workspace 级限速**。 防止跑批任务把交互 UX 饿死。

---

## 参考来源

- [Errors — Claude API Docs (官方)](https://platform.claude.com/docs/en/api/errors)
- [Rate limits — Claude API Docs (官方)](https://platform.claude.com/docs/en/api/rate-limits)
- [Error reference — Claude Code Docs (官方)](https://code.claude.com/docs/en/errors)
- [Our approach to rate limits for the Claude API — Claude Help Center (官方)](https://support.anthropic.com/en/articles/8243635-our-approach-to-api-rate-limits)
- [I'm encountering 429 errors — Claude Help Center (官方)](https://support.claude.com/en/articles/8114527-i-m-encountering-429-errors-and-i-m-worried-my-rate-limit-is-too-low-what-should-i-do)
- [Anthropic API Rate Limits + 429/529 Handling Guide (2026) — Respan](https://www.respan.ai/articles/anthropic-api-rate-limits)
- [Claude API Quota Tiers and Limits Explained 2026 — AI Free API](https://www.aifreeapi.com/en/posts/claude-api-quota-tiers-limits)
- [Tool result block missing corresponding tool use block — GitHub Issue #25959](https://github.com/anthropics/claude-code/issues/25959)
- [Context Window Overflow during file exploration — GitHub Issue #6358](https://github.com/anthropics/claude-code/issues/6358)
- [credit_balance_too_low despite sufficient credits — GitHub Issue #54839](https://github.com/anthropics/claude-code/issues/54839)
