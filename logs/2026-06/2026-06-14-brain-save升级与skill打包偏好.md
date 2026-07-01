---
title: 会话日志 2026-06-14 — brain-save 升级与 skill 打包偏好
tags: [log, brain自维护]
created: 2026-06-14
updated: 2026-06-14
status: active
type: log
project: 跨项目
---

# 会话日志 — 2026-06-14

**项目**：跨项目（brain 自维护）
**主题**：brain-save v2.6 升级 + 两条协作偏好沉淀 + skill 打包交付

> 接续同日 logs/2026-06-14-技术先进度维度落地.md，本篇记其后的增量。

---

## 完成的工作

- 应 Doctor 反馈，brain-save Step 3.5 升级 **v2.6**：升格分拣的「推荐/不推荐 + 难复得三问理由」要写在 /save 聊天正文里，AskUserQuestion 选项只放简洁标签（理由别只埋 description）。改源 `Claude/Brain/.skills/brain-save/SKILL.md` + v 历史追加。
- 沉淀两条协作偏好到 `permanent/Doctor协作偏好.md`：① 升格分拣呈现方式（理由上聊天）；② 更新 skill 后打包成 `.skill` 贴对话框给 Doctor 一键安装覆盖、不让其手动去设置同步。
- 回退上一轮的「命名一致性」偏好条（Doctor 复核判定不推荐、一次性纠正易再得）。
- 兑现「打包安装」偏好：把 brain-save 目录打包成 `brain-save.skill` 经 present_files 贴出，供一键覆盖安装到 v2.6。

## 做出的决策

| 决策 | 原因 | 影响 |
|------|------|------|
| 升格分拣理由写聊天正文、选项保简洁 | Doctor 要看着理由判，别埋进控件描述 | brain-save v2.6；协作偏好备份 |
| 更新任何 skill 后打包 .skill 贴对话框给 Doctor 装 | 运行时走已安装缓存，改源不重装不生效；一键覆盖比手动设置同步省事 | 立为通用协作偏好，今后所有 skill 改动照此交付 |
| 命名一致性偏好回退、不入 permanent | 一次性纠正、易再得，按 G-X10 规则从失败里长不提前立 | 协作偏好该条删除，留日志即可 |

## 遗留问题 / 待办

- [ ] Doctor 在 macOS 终端提交 brain 仓库（命令见下）
- [ ] Doctor 点 brain-save.skill「Save skill」安装覆盖到 v2.6 使其生效
- [ ] （沿用上篇）渊图 TPU dedup、kg_ingest going-forward 打分、UI 拖动条可视化

## 相关笔记

- [[Doctor协作偏好]]
- logs/2026-06-14-技术先进度维度落地.md
- Claude/Brain/.skills/brain-save/SKILL.md（v2.6）
