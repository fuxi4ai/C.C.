---
title: consolidate 2026-11-22 · Step 2 拟改动清单 v1
tags: [consolidate, 记忆治理, checkup]
created: 2026-11-22
updated: 2026-11-22
status: active
type: log
---

# consolidate 2026-11-22 · Step 2 拟改动清单 v1（每周自动运行 · 未落盘 · 待 Doctor 批）

> 依据：`logs/checkups/2026-11-22_consolidate_冲突清单_v1.md`（独立复核 PASS_WITH_LIMITS）。本清单只列拟动作，**一律未执行**；Step 3 落盘、Step 4 修剪索引、Step 5 git 在交互会话中经 Doctor 批后做。

## 批 α · 冲突修正（有权威源可判）

### α-① 注入层（逐条前后原文 · structural）

1. **M1** `.skills/brain-consolidate/SKILL.md:3`（＋portable 同行）description：前「本 skill 只定义流程，绝不自动跑；」→ 后「本 skill 只定义流程，交互外不落盘；每周日由 brain-dream 自动跑到 Step 2 拟改动清单即停；」（其余不动；改后量字数 ≤1024，G-X270；走 `skill_release.py release`。注意正文 v1.4 记「description 冻结约定」——是否破冻结由 Doctor 定）。
2. **M2** `portable/claude-code/CLAUDE.md:51`：前「扩至全部 7 个 brain-* skill」→ 后「扩至全部 8 个 brain-* skill（含 brain-dream）」；同行命令列表是否补 /todo 一并定。改后 Doctor 终端 cp 到 `~/.claude/CLAUDE.md`。
3. **N1** Settings 注入块：Doctor 到 Cowork Settings 重贴 `permanent/全局偏好-Settings镜像.md:26` 末句（11-20 新增提交命令 && 合并句）；随后 `维护注记` 补 11-20 条、TODO L307 并入对拍清单（6＋1 处）。
4. **N2** `.skills/brain-anchors/SKILL.md:3` description 纪律锚补「改动面」（与 M1 同批发布，量 1024 字）。
5. **M5（低）** `portable/claude-code/CLAUDE.md:34` 句末补「云端班可用 RemoteTrigger 读（只回前 20 条，见 G-X275）」。

### α-② 记忆正文与项目文档

6. **M2** `permanent/已装skill清单.md:24,78`「7 个」→「8 个」；K 段 :242 补 brain-dream 行；:244 旧 dream 行注明「与 2026-11-19 新建的 brain-dream 不同」。
7. **M2/N4** `.skills/README.md:12,22` 改 8 个并补登 brain-dream、audit、equity-thesis、graphify（技能目录说明，非技能正文）。
8. **M3** `permanent/通用教训.md:4069-4075` G-X269 成员清单补 G-X275、G-X282；G-X279 是否属成员待核后补。
9. **M7（低）** `permanent/全局偏好-Settings镜像-维护注记.md:97` 后加追记：canonical 现为 `permanent/数据真实性铁律.md:25`，brain/CLAUDE.md:62 仅指针，portable 无「金融」条（原文不改）。
10. **M6/N3** 日志订正注（由下次 brain-dream 按 Step 3 做，不在本批）：`logs/2026-11-20-云端定时班四处改班.md:40`、`logs/2026-11-20-DVA回流班排期订正与提交命令合并规则.md:40`「注入层仍缺 5 句」沿用 11-18 早观察；`logs/2026-11-19-ElevenLabs语气标签.md:20,32` 已被同日新规取代。

## 待 Doctor 裁（方向 / 授权）

- **M4** `Settings镜像.md:26`「不在沙箱跑任何 git 子命令」是否加「Cowork」限定（portable:31、协作偏好:96 已限定；11-20 DVA 会话出现误读）。推荐：加限定——误读已实际发生，且与已批的 11-06 E4 口径一致。
- **M1** 是否为此破 description 冻结约定。推荐：破——description 每轮在场，与正文 v1.4 相反的「绝不自动跑」会误导。

## 待核（本批不动）

- **M8** 云端班数：等巡检班重生成 `_cloud_trigger_health.json` 后，与 W1（TODO L323）及「list_triggers 4 页」疑点一并定，再改 `TODO.md:128`、适配卡 :20，并补登 brain-dream-daily。

## 批 β · dream 提案队列（`permanent/_dream_proposals.md` 待批 DRM 条目）

- **DRM-20261121-1231-01** 云端 Cowork 会话不进真相层 → `chats/README.md` 已知局限＋brain-dream Step 2 增「真相层未覆盖」类（技能改动待批）。
- **DRM-20261122-1231-02** 通用教训升格：多写方/多维记录的去重键须含全部区分维度（龙鱼 ERR-20261122-001 ＋ 渊图 ERR-20260608-002 同族）。
- **DRM-20261122-1231-03** brain 侧 `PEC/GOTCHAS.md` 索引补 G-31～G-47。

## 不动 / 只报

- validate-frontmatter 错误 8、警告 14 未逐条读（本次未核明细）；find-orphans 健康度 58%，孤儿清单不在本批。
- 已归档件 `定时任务巡检机制.md:237`、`定时任务清单.md:68` 的旧口径属历史，不改。
