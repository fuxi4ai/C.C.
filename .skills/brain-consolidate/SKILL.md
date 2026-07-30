---
name: "brain-consolidate"
description: "brain 原生记忆固化——把只增不减的会话日志蒸馏进 permanent，去重合并、修过期日期、修剪索引。触发：用户说 `/consolidate` 或 `/固化记忆` 或「固化记忆」「整理记忆」「记忆固化」「蒸馏日志」。双重门控：本 skill 只定义流程，绝不自动跑；每次运行先产出『拟改动 diff』给 Doctor 过目，批准后才落盘。Step 1 盘点须递归数 logs、先 date 对表、查编号漂移。取代通用 consolidate-memory（那个针对 MEMORY.md，与 brain 的 logs/permanent/inbox 结构不符）。"
---

# brain-consolidate — brain 原生记忆固化

> 对 brain vault 做一次反思性整理：把成熟、反复出现的会话日志蒸馏成长期知识，去重、修时间引用、修剪索引。
> brain 的日志是**只增不减**的工作史（数百篇），本 skill 负责把其中"可复用的"沉淀进 `permanent/`，让未来 session 不必翻全部日志就能定位。

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
  - ⚠ **`logs/` 要 `find` 递归数,不能只 `ls logs/*.md`**——已归档月份在子目录里(如 `logs/2026-06/`),只数根目录会漏一大半(2026-07-30 实测:根目录 229 篇 vs 递归 445 篇)
- 跑**只读**诊断:
  ```bash
  python3 ~/Documents/Claude/brain/.tools/find-orphans.py
  python3 ~/Documents/Claude/brain/.tools/validate-frontmatter.py
  ```
  > **v1.1 订正(2026-07-30)**:原写 `build-backlinks.py --orphans`,但该脚本**含 3 处写操作**(会刷新反链、改写笔记),放在"只读盘点"步骤名不副实——盘点尚未获批就先改了库。改用 `find-orphans.py`(已验只读)。`build-backlinks.py` 保留在 **Step 4 修剪索引**——那一步本就该写,用它正确。
- **跨日对表**:盘点前先 `date`(含业务时区),不要沿用会话开头的日期——consolidate 常发生在长会话尾部,跨日风险最高(G-X100)
- 标记:哪些日志要点反复出现(值得蒸馏)、哪些 permanent 重叠(可合并)、哪些是一次性已过期内容、哪些时间引用是相对词("上周""本季度")
- **查编号漂移**:并发会话可能重编过 `G-X` / `EXP-` 等编号,导致**历史引用静默指错**(写时是对的、被引用方事后变了)。查法:对同一编号 `grep -o "^#\+ \[\?G-X[0-9]\+"` 看有无重复标题,再全库 `grep` 该编号的引用处、核对语义是否仍匹配。**G-X101「引用前先核原文」防不住这类漂移**——它靠的正是 consolidate 这种跨库回顾

### Step 2 · 产出「拟改动 diff」清单（给 Doctor，等批准）

把下面四类拟动作列清单,**先不落盘**:
- **蒸馏**:成熟/反复出现的日志要点 → 提炼为 `permanent/` 原子笔记,或并入 [[通用教训]] / [[经验库]]
- **去重合并**:同主题 permanent 笔记合并,保留信息更全那份的路径
- **归档(非删除)**:一次性、已过期的内容把 frontmatter 改 `status: archived`,**绝不删文件**
- **修时间引用**:相对时间("下周""本季度")→ 绝对日期

**分批建议**:低风险项(修引用、改 skill 自身)与大面积项(日志归档、巨型文件分片、格式统一)**分场做**——后者应在 Doctor 精力充沛时批,不在长会话尾部推。

### Step 3 · 落盘（Doctor 批准后）

- 按批准清单执行;**沙盒铁律:只 rename / `os.replace` 覆盖,绝不 unlink**(参 [[通用教训]] / DVA INFRA-20260521-003)
- 归档用改 `status: archived`,不移动/删除
- 蒸馏出的新笔记遵循 [[CLAUDE]] 的 Zettelkasten 规则(frontmatter 齐全、≥2 wikilinks、原子性)+ 分级加载约定(先写 `abstract` L0)
- **批量替换前先分四类**:正文(可改)/ 标识符·文件名(绝不可改,改了断溯源)/ 别名(不改,职责是覆盖俗称)/ 留痕(不改,内容就是"原名是什么")。详 [[经验库]] EXP-20260729-006-S

### Step 4 · 修剪索引

- 重跑 `build-backlinks.py --orphans`(刷新反链/孤儿/悬空链接)——**这一步本就要写,用它正确**
- 必要时更新 `permanent/项目总览.md`(移除指向已归档内容的指针、补新增重要笔记)
- 让 `项目总览.md` 一行一条、控制在可一屏扫完

### Step 5 · git(贴命令给 Doctor,不在 sandbox 跑)

⚠️ 同 brain-save 硬约束:**CC 绝不在 sandbox 跑任何 git 子命令**(含 `status`/`log` 等看似只读的——它们会创建沙箱无权删除的 `.git/index.lock`)。仓库状态一律 `ls`/`cat` 读 `.git/` 下纯文本。构造命令字符串贴给 Doctor 在 macOS 终端执行,**先探后加、禁 `git add -A`**:

```bash
cd ~/Documents/Claude/brain
git status --short
git add <本次 consolidate 明确改动的文件列表>
git diff --cached --check
git commit -m "consolidate: 记忆固化 {date}"
git push
```

### Step 6 · 回报

```
✅ 记忆固化完成
   蒸馏 N 条日志要点 → permanent / 经验库 / 通用教训
   合并 M 组重复笔记 · 归档 K 篇过期日志(status: archived)
   修引用漂移 X 处 · 索引已重建(孤儿 a / 悬空 b)
📋 请在 macOS 终端跑:(见 Step 5 先探后加模板)
```

## 边界 / 区别

- **vs 通用 consolidate-memory**:那个针对通用 `MEMORY.md` 模型,与 brain 的 `logs/permanent/inbox` 结构不符;brain 一律用本 skill。
- **vs brain-save**:brain-save 是单次会话**写入**(/save);brain-consolidate 是跨多篇日志的**回顾蒸馏**(/consolidate),频率低、动作重、需 Doctor 逐项批。
- 保留"耐查的":偏好、决策背景、找谁办什么;丢弃"易再得的":能从 calendar/docs/工具随时拉到的。
- **本 skill 独有的价值**:编号漂移、跨文件引用失效、归档结构不一致这类问题,**单场 /save 看不见**,只有跨库回顾才能发现。

## v 历史

- v1.0(2026-05-23):初版 · brain 原生固化流程 · 双重门控 · 取代通用 consolidate-memory 在 brain 的角色
- **v1.1**(2026-07-30):Step 1「盘点(只读)」四处加固,均由首次实跑本 skill 时**当场撞到**:
  1. **`build-backlinks.py` 换成 `find-orphans.py`** —— 前者含 3 处写操作,放在"只读盘点"里名不副实(盘点未获批就先改库),违背本 skill 的双重门控本意。`build-backlinks.py` 保留在 Step 4 修剪索引,那步本就该写
  2. **`logs/` 必须递归数** —— 已归档月份在子目录(`logs/2026-06/`),`ls logs/*.md` 实测只见 229 篇、`find` 见 445 篇,漏一半
  3. **盘点前先 `date` 对表** —— consolidate 多发生在长会话尾部,跨日风险最高;本次实跑即在此翻车(整场按 07-29 算,实为 07-30),而 G-X100 讲的正是这条
  4. **新增「查编号漂移」** —— 并发会话重编 `G-X`/`EXP-` 编号会让历史引用**静默指错**(写时是对的、被引用方事后变了)。本次实跑即发现 G-X100 被重编为 G-X106、两处历史引用漂移。G-X101「引用前先核原文」防不住这类,**正需 consolidate 这种跨库回顾兜底**
  另补:Step 2 加「分批建议」(大面积项别在长会话尾部推)、Step 3 加「批量替换前先分四类」、Step 5 同步 brain-save 的先探后加与禁跑 git 子命令口径
