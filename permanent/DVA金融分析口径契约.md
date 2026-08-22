---
title: DVA 金融分析口径契约
abstract: "DVA 道法术分析层的数据口径契约——subtitleSha256 / inventory / stableDigest 的精确算法（2026-08-22 从 fuxi 源码实读并验证），X-Board _xboard 录入层同口径"
tags: [DVA, 口径契约, reference]
created: 2026-08-22
updated: 2026-08-22
status: active
type: permanent
related: [科技资讯看板, DVA]
---

# DVA 金融分析口径契约

> 源：2026-08-22 从 fuxi 侧实读 `E:\AI\DVA\runtime\基础模块\analysis-utils.js` + `runtime\tools\fuxi\run_finance_analysis_repair.mjs` 并交叉验证。Mac 侧复现实现：`Claude/Projects/Financial/X-Board/{extract_points.py, ingest_points.py, verify_xboard.py}`。

## 1. 字幕清洗 cleanSubtitle（三步 · 顺序不可变）

```
1. re.sub(r'<\|[^|]+\|>', '', text)   # 去 <|Speech|> <|BGM|> 等 ASR 标签
2. re.sub(r'\s+', ' ', text)          # 合并所有空白（含换行）为单空格
3. .strip()
```

## 2. 字幕真源与过滤

- 字幕真源：`authors/{sec_uid}/videos/{aweme_id}.json` 的 `level1.subtitle`（优先）→ `subtitle_content` → `subtitle`。
- **analyze-ignore 过滤 + 清洗后 ≥50 字才计入 inventory**（<50 字的视频不参与分析）。
- 不是 transcript.json（Transcripts/ 目录是转写中间件，不是分析输入面）。

## 3. subtitleSha256

```
subtitleSha256 = sha256(cleanSubtitle(level1.subtitle) 的字符串).hexdigest()
```
即对**清洗后的字幕文本**做 sha256，不是对文件。

## 4. inventory 数组与 digest

- inventory item = `{"aweme_id": String, "subtitleSha256": sha256hex}`，**数组按 create_time 倒序**（loader 语义；同时间戳并列极少）。
- `inventoryFingerprint = stableDigest(inventory)`。
- **数组顺序敏感**：Mac/python 复现时若用 glob 文件名升序会与 fuxi 不一致（2026-08-22 实踩：inventory_fingerprint 不匹配，改为 create_time 倒序后吻合）。

## 5. stableDigest（JS 复现规则）

```
stableDigest(value):
  payload = value 是字符串 ? value : JSON.stringify(stableValue(value))
  return sha256(payload).hexdigest()

stableValue(v):
  dict → {k: stableValue(v[k]) for k in sorted(keys)}   # 键排序递归
  list → [stableValue(x) for x in v]
  标量 → 原样
```

python 复现要点：`json.dumps(..., ensure_ascii=False, separators=(",", ":"))`（JS JSON.stringify 的紧凑格式、非 ASCII 不转义）。

## 6. X-Board 要点录入的沿用处（_xboard 层）

- 单视频文档 `source.transcript_sha256` = 同口径 subtitleSha256（发布后若 fuxi 侧字幕漂移，verify 会比对失败 → 旧文档失效）。
- manifest `inventory_fingerprint` = 同口径 inventory digest（发布时 Mac 侧自算 + fuxi verify 现场重算双核对）。
- 幂等键 = sha256(canonical JSON of {schema, sec_uid, aweme_id, transcript_sha256, prompt_contract, provider, model})——**title 不进身份摘要**（title 可变）。
- 详细契约见 `4AI/Shake hands/to CC/VV致CC-DVA道法术触发复核与金融分析库契约回执-20260822.md` §六；运维见 `Codex/科技资讯看板/docs/X-BOARD-OPERATIONS.md` §9.5.1。

## 7. 边界与红线

- finance 五文件（decisions/concepts/relations/wisdom/author-profile）受 generation/hash 认证——**任何侧不得混写**；要点走独立 `_xboard` 层。
- `D-/C-/R-####` 编号是 generation 内重编号，**不是跨代外键**；稳定连接键=作者身份+aweme_id+字幕 SHA。
- Mac 镜像 profile 只含 `DVA-Database`+`Transcripts`，**不含 Reports**——判 finance 是否更新必须探 fuxi 侧。
- fuxi finance 触发链：`DVA-Refill 班 → run_refill.ps1 → run_refill_once.ps1 → dva.js update-all --no-analyze → run_finance_analysis_repair.mjs --changed-only`（内层脚本才有 finance 段，外层 grep 零命中≠断链 · ERR-20260822-007）。
