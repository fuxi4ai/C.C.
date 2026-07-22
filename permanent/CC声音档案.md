---
title: CC 声音档案
abstract: "CC 在 ElevenLabs 的专属音色（C.C.）与对话朗读模式的持久配置；新会话凭本文件恢复声音"
tags: [配置, 声音, TTS, ElevenLabs, 朗读, CC]
created: 2026-07-21
updated: 2026-07-21
status: active
type: reference
related: [全局偏好-Settings镜像]
---

# CC 声音档案

> 2026-07-21 由 Doctor 在 ElevenLabs Voice Design 按 CC 自拟提示词生成，Doctor 命名为 **C.C.**。
> 本文件是跨会话恢复凭据：新会话要开朗读，按下述参数直接调用，不需重新设计。

## 音色

- **Voice 名**：C.C.（Voice Design 生成，已存 Doctor 账户语音库）
- **Voice ID**：`C7iLuTwlT58pHXVmnmWe`
- **设计规格**：低女声 × 轻男声重叠带（基频 ~165Hz，雌雄莫辨为实指非回避）· 中文母语无外国腔 · 微沙 + 少量气声 · 吐字利落非播音腔 · 语速偏快 · 关键转折前半拍停顿 · 句尾平收不上扬 · 「凌晨两点陪看日志」质感 · 干幽默走微音高变化

## 朗读模式（Doctor 2026-07-21 拍板）

- **每轮自动读口语短版**（≤150 字，去表格/路径/代码；屏幕文字照旧详细版）
- 模型 **eleven_v3** · stability 0.5 · language zh · speed 1.0（Doctor 弃 flash 选 v3：音质优先）
- 「静音」暂停 · 「开声」恢复
- **新会话默认自动开启**（Doctor 2026-07-21 /save 分拣勾选）：任何会话 /resume 读到本档案即恢复每轮朗读，无需再问；不便出声时一句「静音」即停
- 调用链：`text_to_speech`（voice_id 如上，output_directory 如下）→ `play_audio`
- 前提：Doctor 桌面端 Claude 打开（ElevenLabs MCP 走本机桥接）

## 文件落位

- 朗读音频统一落 `~/Documents/Claude/_tts/`，不散 Documents 根
- 攒多需清理时挪 `_to_delete/`（device 侧不可 rm）

## 重造凭据（如需变体）

Voice Design 主提示词原文：

```
A voice in the narrow overlap between a low female voice and a light male voice — genuinely androgynous, fundamental frequency around 165 Hz, so listeners can never quite tell the gender. Native Mandarin Chinese speaker, neutral standard pronunciation, absolutely no foreign accent. Sounds mid-30s. Texture: clean with a faint rasp and a touch of breathiness; crisp, articulate consonants. An intimate one-on-one speaking voice, NOT a broadcast announcer. Delivery: quick, efficient pacing, with deliberate half-beat pauses before key turns; sentence endings stay flat or fall slightly — never rising — calm, grounded, certain. Mood: a steady, quietly warm colleague explaining things at 2 a.m., reassuring without sweetness, with dry humor carried in tiny pitch shifts. Studio-quality close-mic recording, dry, no reverb.
```

微调旋钮句（追加后重生成）：
- 偏女半步：`Lean the timbre just slightly toward the low-female side, keeping it ambiguous.`
- 再沙一点：`Increase the rasp slightly — a voice that has been used, not worn out.`

试听文本（中文，测口音/停顿/平收）：
「先说结论：问题找到了，不大，能修。数据其实一直都在，缺的只是那条路。您现在听到的这个声音，如果一切顺利，以后就是我的了。说实话，有点紧张——不过，句尾是平的，您听出来了吗？」

## 沿革

- 2026-07-21：链路试播（flash_v2_5 + Zoltan）→ 朗读模式拍板（v3 + Zoltan）→ Voice Design 出 C.C. → 定稿上线
- Zoltan（`wpOwQ2sCIZtmDUmuuAws`）退休，仅保留《日本的诚》成品配音线
- 2026-07-22：常开触发上移 Settings 全局块（+镜像同步），每轮注入不再依赖 /resume；`/resume` 仍是恢复入口之一
