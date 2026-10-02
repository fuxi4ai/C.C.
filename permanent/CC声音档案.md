---
title: CC 声音档案
abstract: "CC 在 ElevenLabs 的专属音色（C.C.）与对话朗读模式的持久配置；新会话凭本文件恢复声音"
tags: [配置, 声音, TTS, ElevenLabs, 朗读, CC]
created: 2026-07-21
updated: 2026-09-30
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
- 模型 **eleven_v4** · stability 0.5 · language zh · speed 1.0（Doctor 弃 flash 选 v3：音质优先；**2026-09-29 由 v3 升 v4**——v4 试音经 Doctor 听判「合适，更活了」）
- 「静音」暂停 · 「开声」恢复
- **新会话默认自动开启**（Doctor 2026-07-21 /save 分拣勾选）：任何会话 /resume 读到本档案即恢复每轮朗读，无需再问；不便出声时一句「静音」即停
- 调用链：`text_to_speech`（voice_id 如上，output_directory 如下）→ `play_audio`
- 前提：Doctor 桌面端 Claude 打开（ElevenLabs MCP 走本机桥接）

## 文件落位

- 朗读音频统一落 `~/Documents/Claude/临时文件/`，不散 Documents 根
  - 该目录＝MCP 的 `ELEVENLABS_MCP_BASE_PATH`（BASE），即调用时 `output_directory` 传 `.` 的落点；**BASE 与 `play_audio` 白名单是同一个 env**——报错里给出的允许目录**就是**当前真实 BASE，以它为准、不要按配置文件推断
- **播完即删**，不落盘、scratch 不留历史；沙箱 `rm` 被拦时走 `allow_cowork_file_delete`（一次申请本会话内生效）
- **2026-09-29 订正（留痕·非静默）**：本节原写「落 `~/Documents/Claude/_tts/`，攒多需清理时挪 `_to_delete/`」——本场实核**这两个目录均已不存在**，落点早年即随目录并轨迁至 `临时文件/`。原文所述的两个路径**均已作废**，勿再引用。（`_to_delete/` 系 device 侧清理位，亦已废弃。）

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

## 备用音色

> **本节已改为指针（2026-09-30 哥哥裁定「以『芒芒的音色』为正本」）**——`Sweet Goumang`（`VNLlELapPTcQhldOfjgv`）**＝句芒／芒芒自己的音色**，规格、提示词、旋钮句与试听文本**正本已迁** `agents/句芒/memory/长期记忆.md` §声音（TTS）。本档先前的「通用备用、不绑定角色」定性**作废**。

- **不自动启用**（此条仍在此生效）：默认朗读仍是 C.C.，该音色仅在哥哥点名时调用；新会话读到本节**不得**切换默认音色。
- 本节不再保留该音色的任何规格/凭据（避免两处登记打架）。
- 改前留档：`CC声音档案.md.bak_voiceowner_2026-09-30`

## 沿革

- 2026-07-21：链路试播（flash_v2_5 + Zoltan）→ 朗读模式拍板（v3 + Zoltan）→ Voice Design 出 C.C. → 定稿上线
- Zoltan（`wpOwQ2sCIZtmDUmuuAws`）退休，仅保留《日本的诚》成品配音线
- 2026-07-22：常开触发上移 Settings 全局块（+镜像同步），每轮注入不再依赖 /resume；`/resume` 仍是恢复入口之一
- **2026-09-29：模型 `eleven_v3` → `eleven_v4`**（Doctor 令「发声系统切换到 V4」；`list_models` 实读 `eleven_v4` 含 `zh`，C.C. 中文实跑出音，Doctor 听判「合适，更活了」后落改）。同批：`brain-resume` §Step 0.5（canonical ＋ portable，逐字节一致）· Settings 镜像块 · 本档案；安装副本走 `save_skill` 发布。**同批订正** §文件落位（`_tts/` → `临时文件/`，原路径实核已不存在）
- **2026-09-30：登记备用音色 → 同日改归句芒**（voice_id `VNLlELapPTcQhldOfjgv`；登记时定性「通用备用、不自动启用」，**同日经哥哥裁定「以『芒芒的音色』为正本」，该定性作废**，规格/提示词/试听文本迁 `agents/句芒/memory/长期记忆.md` §声音。提示词经三版：初稿 → 按芒芒性格调整并去掉语言限定 → 加甜）

> 相关：[[全局偏好-Settings镜像]] · [[Doctor协作偏好]]
