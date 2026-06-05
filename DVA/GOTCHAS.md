---
title: DVA · GOTCHAS（已知坑）
tags: [DVA, gotchas]
created: 2026-05-14
updated: 2026-05-14
status: active
type: resource
project: DVA
---

# DVA · GOTCHAS（已知坑）

> 排查超过一轮的问题都该记录在这里。CC 遇到报错并解决后**立即**回写，无需 Doctor 提示。
> 实时操作日志写在项目目录的 `Projects/DVA/GOTCHAS.md`；这里是沉淀+索引。

## 格式

```
## [ERR-YYYYMMDD-NNN] 简要描述
**状态**: ✅ 已解决 / ⏳ 待解决
**优先级**: 🔴 高 / 🟡 中 / 🟢 低
**触发场景**:
**错误信息**:
**解决方案**:
**预防措施**:
```

---

<!-- 在下方追加新条目 -->

## [ERR-20260605-001] 推理模型回复被读成空串（content[0] 是 thinking 块）
**状态**: ✅ 已解决
**优先级**: 🔴 高
**触发场景**: 切换分析 LLM 为 DeepSeek V4 Pro 后，`node 基础模块/llm-client.js` 自检报「连接失败，详情 undefined，完整错误 undefined」。
**错误信息**: 无异常抛出（故错误对象为 undefined）；healthCheck 因回复不含 "OK" 判 false，而该路径未设 error 字段，打印成 undefined。
**根因**: `llm-client.js` 的 `chat()` 写死取 `response.content[0]?.text`。deepseek-v4-pro 是**推理模型**，Anthropic 兼容格式下 content[0] 是 `thinking` 块（无 .text），真正答案在后面的 `text` 块 → 取到空串。影响所有分析调用，非仅自检。
**解决方案**: `chat()` 改为 `content.filter(b=>b.type==='text')` 拼接所有 text 块，兜底回退 content[0].text；同时修 healthCheck「已连通但回复未含 OK」路径，把实际返回文本带出来，不再丢 undefined。
**预防措施**: 接入任何兼容 Anthropic 协议的模型时，不要假设 content[0] 即文本；推理模型 content 数组首块多为 thinking。按 type 取块。
