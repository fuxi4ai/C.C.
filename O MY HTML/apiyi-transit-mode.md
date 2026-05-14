---
title: APIYI 转接模式 · O MY HTML
tags: [O MY HTML, apiyi, image-gen, credentials]
created: 2026-05-14
updated: 2026-05-14
status: active
type: resource
project: O MY HTML
---

# APIYI 转接模式

## 是什么

APIYI 是 OpenAI API 的第三方转发服务，提供与 OpenAI 官方完全兼容的接口，
只需把 `base_url` 从 `https://api.openai.com/v1` 换成 `https://vip.apiyi.com`，
其余参数（model、messages、response_format 等）与官方完全一致。

## 用途

O MY HTML 项目用 APIYI 调用 `gpt-image-1`（即 chatgpt-image-2）做图像生成，
主要用于设计参考图、原型配图、品牌视觉素材生成。

## 凭证存放

- 实际 key：`Projects/O MY HTML/.env.omyhtml`（本地，不进 git）
- 模版：`Projects/O MY HTML/.env.omyhtml.example`
- 凭证清单：`brain/references/凭证清单.md` 第 6 条

## 使用方式

```bash
source ~/Documents/Claude/Projects/O\ MY\ HTML/.env.omyhtml
```

Python 调用示例：
```python
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("APIYI_KEY"),
    base_url=os.getenv("APIYI_BASE_URL", "https://vip.apiyi.com")
)

response = client.images.generate(
    model=os.getenv("APIYI_IMAGE_MODEL", "gpt-image-2-vip"),
    prompt="...",
    size="1024x1024",
    quality="high",
    n=1,
)
image_url = response.data[0].url
```

## 已知限制（GOTCHAS）

- `base_url` 不带 `/v1`，APIYI 端点自动处理版本路由
- APIYI 是转发服务，不保证与 OpenAI 最新 API 版本同步；遇到参数不认识时先查 APIYI 文档
- `response_format="b64_json"` 比 `url` 更稳定（url 有时效性）
- 计费按 token/图像数，与官方价格可能有差异，注意用量
- 若 APIYI 服务中断，fallback 到 Claude 原生图像能力（`claude-opus-4` 支持图像理解，但不支持生成）

## 相关

- [[凭证清单]] · 第 6 条
- `Projects/O MY HTML/CLAUDE.md` · 项目级指令
