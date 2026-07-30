---
title: 2026-05 日志归档说明
tags: [meta, 归档]
created: 2026-07-30
updated: 2026-07-30
status: active
type: meta
---

# 2026-05 日志归档说明

本目录的 **98 篇**日志原先都在 `logs/` 根目录，于 **2026-07-30** 折叠至此。

## 路径映射

历史文本（会话日志正文、`chats/` 导入存档、决策记录等）中出现的旧路径：

```
logs/2026-05-XX-{主题}.md          ← 旧
logs/2026-05/2026-05-XX-{主题}.md  ← 现
```

**全库约 194 处正文引用刻意未改。** 理由：这些字串绝大多数是**历史留痕**——正文写的是"当时那个文件在哪儿"，改了反而失真；且批量替换正文路径正是 `经验库` EXP-20260729-006-S 记的那个坑（71 个 provenance ghost 差点被批量改坏真实文件名）。读到对不上的路径时，按上表换算即可。

**`[[2026-05-XX-{主题}]]` 形式的 wikilink 不受影响**——Obsidian 按文件名解析，与目录位置无关。同理，日志间互引一律用**纯文件名 wikilink、不带 `logs/` 前缀**，这样以后再折叠也不会断（2026-07-30 已把残留的 6 处带路径写法统一改掉）。

## 为什么 05 月是手工补的

`Projects/海螺姑娘/meditation/meditation.py` 的 `fold_logs()` 由 `brain-monthly-checkup` 每月 1 号自动跑，但它**只折叠上一个自然月**（硬编码 `previous_month`）。该自动化上线晚于 2026-05，所以 05 月成了唯一漏网的月份——06 月是 07-01 自动折的，07 月将由 08-01 自动折。本次补跑复用的正是同一个 `fold_logs` 函数，未另写逻辑。

## 同期修掉的两个非递归读取

折叠会让"只扫 `logs/` 根目录"的代码看不见历史。2026-07-30 一并修正：

- `.tools/dashboard-snapshot.py` — `project_last_active()` 的日志源加上 `logs/YYYY-MM/`。**此处从 2026-07-01（06 月折叠）起就已失准**，不是本次折叠引入的。
- `brain-resume` SKILL.md Step 1 — `ls -t` 加上子目录，否则**每月 1 号前后会静默读不满 3 篇**。

两处都刻意**没用全递归**：那会把 `checkpoints/`（PRD，其中 33 篇含 `project:` frontmatter）和 `checkups/`（月度体检报告）混进"会话日志"，属语义变更而非修 bug。

## 相关

- [[通用教训]] · [[经验库]] EXP-20260729-006-S（批量替换前先分四类）
- `Projects/海螺姑娘/meditation/meditation.py` · `Scheduled/brain-monthly-checkup/SKILL.md`
