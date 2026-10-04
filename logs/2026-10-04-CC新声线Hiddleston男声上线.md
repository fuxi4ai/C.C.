---
title: 会话日志 2026-10-04 — CC 新声线 Hiddleston 男声上线与默认切换
tags: [log, brain基建, TTS, 声音]
created: 2026-10-04
updated: 2026-10-04
status: active
type: log
project: 跨项目（brain 基建 · TTS 声线）
---

# 会话日志 — 2026-10-04

**项目**：跨项目（brain 基建 · TTS 声线）
**主题**：`/resume` 起手 → Loki/抖森闲聊 → **为 CC 定制第二声线「Hiddleston」男声**（两轮迭代）→ Doctor 裁「设为默认」→ 四处同步（Settings 镜像 / CC声音档案 / brain-resume 发布链 / 记忆层）→ Doctor 报 done
**时长**：00:2x → 01:4x PDT（约 1.5h）

---

## 完成的工作

- **/resume 起手**（00:2x）：快照 2026-09-27（6 天前）未破线 · 修复审计无未验行 · 黄条 1（`com.zhuzhao.ipo-rolling` 日志落 /tmp）· Settings 漂移仍只剩朗读条 1 字残差（短版/短篇）；摘要含 brain 仓 2 commit 未推待办。
- **声线定制**：Doctor 提出「为 CC 做一款男声——CC 性格 + 抖森式音色（绅士/英伦/好听/不快）」。第一轮 `text_to_voice` 三版预览被 Doctor 否掉（「伦敦腔」描述致中文读出老外腔）→ Doctor 裁「去地域词、只用抖森音色特点」→ v2 提示词交付 → Doctor 在 ElevenLabs 网站亲自生成，两轮迭代：① Hiddleston（`HRV5jGEhRPGls9DMLXiF` · 主推版·带朗读腔）② Hiddleston-CN（`FVvcH2MAGGpovILJcXEv` · v2 去朗读腔日常版——Doctor 裁「去朗读腔·更日常交流；重在好听/绅士/有教养/博学」）。v2 中文试读（绕口令＋十四行诗测音位）经 Doctor 听判「这般很好」。
- **初代中文测试版** `ugJYnTvWqslHn3gjUJJI`：由 Doctor 在网站删除/替换（CC 无删除端点；档案从未登记、零残留）。
- **默认切换四处同步**（Doctor 裁「设为默认吧，之前的保存为备选」）：① `全局偏好-Settings镜像.md` 朗读条改默认 Hiddleston-CN ＋ 备选 C.C. ＋ 10-04 注记；② `CC声音档案.md` 朗读模式段/第二声线节（含 v1/v2 提示词原文与沿革）；③ brain-resume §Step 0.5 发布链——canonical ＝ portable ＝ 包内件 `7d97ca3553eab9f4…`（16703 B）逐字节一致、`.skill` 包重打 `cff4b3143e003429…`/8737 B、save_skill 发布（技能列表实时刷新＝第一层消费证据）；④ auto-memory 索引行与 `reference_shuling_voices.md` 同步。
- Doctor 报「done」（Settings 重贴已做）→ 镜像注记留痕，验证待下一场新会话起手逐行 diff。

## 做出的决策

| 决策 | 原因 | 影响 |
|------|------|------|
| Doctor「设为默认吧，之前的保存为备选」 | v2 中文试读听判「这般很好」 | Settings 朗读条默认 Hiddleston-CN · C.C. 降备选（点名「用 C.C.」切回） |
| v2 描述去地域词（伦敦腔/British 全删） | 「伦敦腔」致中文读出老外腔（第一轮实测被否） | 只留音色特质：低沉软男中音 / 微沙绒感 / 绅士教养 / 博学 / 日常聊天非朗读腔 |
| 换默认声线＝四处同步（Settings 注入 ＋ skill ＋ 档案 ＋ 记忆） | 09-29 切 v4 时定的承力层判据「只改一处是空转」 | 本场为该判据的 voice 级切换首个实例 |

## 遗留问题 / 待办

- [ ] Settings 重贴验证：下一场新会话起手逐行 diff（镜像 ↔ 注入），漂移零即销账
- [ ] brain 仓 git 提交 ＋ push（含昨晚 2 commit 未推）

## 相关笔记

- [[CC声音档案]]（「第二声线」节为真源）
- [[全局偏好-Settings镜像]]
