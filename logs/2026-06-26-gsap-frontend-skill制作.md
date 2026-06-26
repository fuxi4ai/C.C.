---
title: 会话日志 2026-06-26 — gsap-frontend skill 制作
tags: [log, skill, gsap]
created: 2026-06-26
updated: 2026-06-26
status: active
type: log
project: 跨项目/工具
---

# 会话日志 — 2026-06-26

**项目**：跨项目（个人 skill 库工具）
**主题**：基于官方 greensock/gsap-skills 做一个自己的合并版 .skill

---

## 完成的工作

- 查清 greensock/gsap-skills 是什么：GSAP 官方 AI skills 仓库（MIT，9.9k star，8 个 SKILL.md，Agent Skills 格式）；确认 Webflow 收购后所有插件免费、无需 auth token。
- 应 Doctor 要求克隆该仓库下来打包给 Doctor 自己装（`gsap-skills.zip`）。
- 与 Doctor 对齐：要做「自己版本」的 GSAP 前端 skill，交付 .skill 安装包。
- 回答 Doctor 追问「官方为何拆 8 个」，据此修正方案方向。
- 写出合并版 `gsap-frontend` skill：精简主干 SKILL.md（core/timeline/easing/stagger/matchMedia/性能/反模式）+ 5 个 references（scrolltrigger/react/frameworks/plugins/utils）按需加载。
- 用 skill-creator 的 quick_validate + package_skill 校验并打包成 `gsap-frontend.skill`，已过 validator。
- Doctor 安装成功，已出现在可用列表（`anthropic-skills:gsap-frontend`）；Doctor 决定「先用着」，暂不跑评测。

## 做出的决策

| 决策 | 原因 | 影响 |
|------|------|------|
| 自制版做「精简主干 + references 渐进式披露」，不拍平成单个胖文件 | 拍平会丢掉官方拆分的全部好处（任何 GSAP 问题都灌全部上下文） | 单入口、保住上下文经济 |
| 触发词写得偏激进（只描述效果也触发） | skill 通病是「该触发不触发」，宁可往前压 | 可能抢戏；已告知 Doctor 可回收 |
| 不在沙箱 clone/zip 到 outputs 挂载点，改 /tmp 做再 cp | outputs 挂载点不支持 git/zip 的 lock+rename | 见 GOTCHAS 候选 |
| 暂不跑 skill-creator 评测闭环 | Doctor 选择先用着 | v1 凭判断蒸馏，未评测 |

## 遗留问题 / 待办

- [ ] gsap-frontend skill 是 v1（未跑评测）；若实际用着「该触发不触发」或某 reference 不顺手，回收触发词 / 配 2–3 个测试 prompt 跑一轮再定稿。
- [ ] 沙箱临时目录里的 `gsap-skills/`（官方克隆）与 `gsap-frontend/` 源——会话结束即清，无需保留。

## 相关笔记

- [[O MY HTML]]
- [[skill-creator]]
