---
title: 会话日志 2026-11-19 — ElevenLabs语气标签
tags: [log, 声音, ElevenLabs, TTS]
created: 2026-11-19
updated: 2026-11-19
status: active
type: log
project: 跨项目（CC 声音系统）
---

# 会话日志 — 2026-11-19

**项目**：跨项目（CC 声音系统）
**主题**：ElevenLabs 语气标签（音频标签）查证、试读、落规则
**前情**：同一会话前半段为 AI4ME conch 与二期第一批迁移，记录见 `logs/2026-11-19-AI4ME-conch审查.md`。

## 完成的工作

- 按 Doctor 令查 ElevenLabs 官网的语气用法，实读三页：Text to Speech 产品说明页、Best practices · Prompting Eleven v4、博客 Audio Tags 101。结论：`eleven_v4` 与 `eleven_v3` 都支持方括号音频标签，官方推荐 v4；v4 不支持 SSML `<break>`，也没有 Style、Speed 滑杆。
- 试读：Sweet Goumang（`VNLlELapPTcQhldOfjgv`）· `eleven_v4` · zh · stability 0.5 · speed 1.0，一句中文里插 `[happy]`、`[sighs]`、`[whispers]` 三个标签。生成、播放成功，音频播完即删（实跑）。Doctor 听判「效果很好」。
- Doctor 裁「照草案写」后落改两处：
  - `permanent/CC声音档案.md`：新增 §语气标签（实测范围、用法三条、停顿靠标点、来源）；`updated` 改为 2026-11-19；§沿革补一行。
  - `portable/claude-code/CLAUDE.md`：朗读条加指针「可加语气标签（少用、只写声音，规则见 `permanent/CC声音档案.md` §语气标签）」。
  - 改前备份：`permanent/_bak/CC声音档案.md.bak_2026-11-19_audio-tags`、`portable/claude-code/_bak/CLAUDE.md.bak_2026-11-19_audio-tags`（均被 `.gitignore` 的 `_bak/` 排除）。
- 未参与实施的子代理独立核验：PASS。新节与草案逐字一致，两文件无草案外改动，指针能对上标题，Settings 镜像里没有「语气标签」字样。
- Doctor 终端：`diff` 只显示第 36 行一处 → cp 到 `~/.claude/CLAUDE.md`，`cmp` 通过 → brain 提交 `f7696f6f`（2 个文件，14 行新增、2 行删除）并已推送。
- /save 顺手订正 TODO L31 的过时括注：「Finder 替身待 Doctor 建」改为已建，补上提交号。

## 做出的决策

| 决策 | 原因 | 影响 |
|------|------|------|
| 规则正文放 `CC声音档案.md`，Code 朗读条只放一句指针 | 声音档案是朗读参数的跨会话凭据；只放指针，免得两处各改各的 | 新会话从 Code 朗读条就能找到规则 |
| Cowork／Settings 镜像不动 | Cowork 默认音色 Hiddleston-CN 没在标签上测过，写进去属于未核 | Cowork 侧暂不用标签，要用得先试听 |
| 用法定为「少用（每轮 2～3 个）、只写声音、配音色」 | 照官方「要避开的」三条，Doctor 同意 | 朗读时标签只在语气真变的地方加 |

## 遗留问题 / 待办

- 标签只在 Sweet Goumang 上测过一句；Hiddleston-CN、C.C. 未测。要在 Cowork 侧启用，得先试听（只是条件，不单列为 TODO）。
- 新规则从下一个会话起才进注入层；本会话注入的还是旧朗读条。
- AI4ME 相关的待办（11:10 PT 后回读 cockpit.db、第二批烛照、11-27 前管制阶梯页更新）已在 TODO L31，本日志不重复。

## 相关笔记

- [[CC声音档案]]
- [[全局偏好-Settings镜像]]

## 记忆分拣（Doctor 勾选）

- ✅ 1 替身后缀补进两份方案：烛照九阴、白泽大宗二期方案的替身步骤各加一句——英文系统实测生成「目标名 alias」，建后 `ls` 看实际名、`mv -n` 改名、`test -f`/`test -d` 确认。查重：经验库、通用教训检索「替身|alias」0 条相关命中（只有渊图实体 aliases 字段）。
- ✗ 2 TTS 文件名带方括号（不推荐，未勾）：只留在本日志——ElevenLabs 输出文件名截取正文开头，本场为 `tts_[happ_…mp3`，删除时路径须加引号。
