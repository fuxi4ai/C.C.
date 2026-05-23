---
name: brain-consolidate
description: "brain 原生记忆固化——把只增不减的会话日志蒸馏进 permanent，去重合并、修过期日期、修剪索引。触发：用户说 `/consolidate` 或 `/固化记忆` 或「固化记忆」「整理记忆」「记忆固化」「蒸馏日志」。双重门控：本 skill 只定义流程，绝不自动跑；每次运行先产出『拟改动 diff』给 Doctor 过目，批准后才落盘。取代通用 consolidate-memory（那个针对 MEMORY.md，与 brain 的 logs/permanent/inbox 结构不符）。"
---

# brain-consolidate — brain 原生记忆固化

> 对 brain vault 做一次反思性整理：把成熟、反复出现的会话日志蒸馏成长期知识，去重、修时间引用、修剪索引。
> brain 的日志是**只增不减**的工作史（现已数十篇），本 skill 负责把其中"可复用的"沉淀进 `permanent/`，让未来 session 不必翻全部日志就能定位。

## 触发

- `/consolidate` / `/固化记忆`
- "固化记忆" / "整理记忆" / "记忆固化" / "蒸馏日志"

## ⛔ 双重门控（最重要，不可绕过）

1. 本 skill 只**定义流程**，**绝不**在被加载时自动执行整理。
2. 每次真正运行,必须先产出**「拟改动 diff」清单**(改哪些文件、新增/归档/合并了什么)给 Doctor 过目;**Doctor 批准后才落盘**。
3. 因为它会动到大量既有笔记,这是 brain 维护动作里唯一会**大面积改写历史**的,务必最谨慎。

## 执行步骤

### Step 1 · 盘点（只读，不改）

- 列 `logs/`(按时间)、`permanent/`、`inbox/`;读 `permanent/项目总览.md`
- 跑只读诊断:
  ```bash
  python3 ~/Documents/Claude/brain/.tools/build-backlinks.py --orphans
  python3 ~/Documents/Claude/brain/.tools/validate-frontmatter.py
  ```
- 标记:哪些日志要点反复出现(值得蒸馏)、哪些 permanent 重叠(可合并)、哪些是一次性已过期内容、哪些时间引用是相对词("上周""本季度")

### Step 2 · 产出「拟改动 diff」清单（给 Doctor，等批准）

把下面四类拟动作列清单,**先不落盘**:
- **蒸馏**:成熟/反复出现的日志要点 → 提炼为 `permanent/` 原子笔记,或并入 [[通用教训]] / [[经验库]]
- **去重合并**:同主题 permanent 笔记合并,保留信息更全那份的路径
- **归档(非删除)**:一次性、已过期的内容把 frontmatter 改 `status: archived`,**绝不删文件**
- **修时间引用**:相对时间("下周""本季度")→ 绝对日期

### Step 3 · 落盘（Doctor 批准后）

- 按批准清单执行;**沙盒铁律:只 rename / `os.replace` 覆盖,绝不 unlink**(参 [[通用教训]] / DVA INFRA-20260521-003)
- 归档用改 `status: archived`,不移动/删除
- 蒸馏出的新笔记遵循 [[CLAUDE]] 的 Zettelkasten 规则(frontmatter 齐全、≥2 wikilinks、原子性)+ 分级加载约定(先写 `abstract` L0)

### Step 4 · 修剪索引

- 重跑 `build-backlinks.py --orphans`(刷新反链/孤儿/悬空链接)
- 必要时更新 `permanent/项目总览.md`(移除指向已归档内容的指针、补新增重要笔记)
- 让 `项目总览.md` 一行一条、控制在可一屏扫完

### Step 5 · git(贴命令给 Doctor,不在 sandbox 跑)

⚠️ 同 brain-save v2.0 硬约束:**CC 绝不在 sandbox 跑 git 写命令**。构造命令字符串贴给 Doctor 在 macOS 终端执行:

```bash
cd ~/Documents/Claude/brain && git add -A && git commit -m "consolidate: 记忆固化 {date}" && git push
```

### Step 6 · 回报

```
✅ 记忆固化完成
   蒸馏 N 条日志要点 → permanent / 经验库 / 通用教训
   合并 M 组重复笔记 · 归档 K 篇过期日志(status: archived)
   修时间引用 X 处 · 索引已重建(孤儿 a / 悬空 b)
📋 请在 macOS 终端跑:
   cd ~/Documents/Claude/brain && git add -A && git commit -m "consolidate: 记忆固化 {date}" && git push
```

## 边界 / 区别

- **vs 通用 consolidate-memory**:那个针对通用 `MEMORY.md` 模型,与 brain 的 `logs/permanent/inbox` 结构不符;brain 一律用本 skill。通用版不删除(无 unlink 规则),仅不再用于 brain。
- **vs brain-save**:brain-save 是单次会话**写入**(/save);brain-consolidate 是跨多篇日志的**回顾蒸馏**(/consolidate),频率低、动作重、需 Doctor 逐项批。
- 保留"耐查的":偏好、决策背景、找谁办什么;丢弃"易再得的":能从 calendar/docs/工具随时拉到的。

## v 历史

- v1.0(2026-05-23):初版 · brain 原生固化流程 · 双重门控 · 取代通用 consolidate-memory 在 brain 的角色
