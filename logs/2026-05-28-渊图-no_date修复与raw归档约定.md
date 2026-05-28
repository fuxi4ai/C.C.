---
title: 会话日志 2026-05-28 — 渊图 no_date 修复与 raw 归档约定
tags: [log, 渊图]
created: 2026-05-28
updated: 2026-05-28
status: active
type: log
project: 渊图
---

# 会话日志 — 2026-05-28

**项目**：渊图
**主题**：quarterly_recheck no_date warning 根因修复 + raw 已手工入库归档目录约定

---

## 触发场景

Doctor 在 macOS 终端重跑 4 篇 batch failed 研报（CPU 扩容 / 盛科通信 / 中科微至 / deep-research-report），每次输出尾部都报同一条警告：

```
⚠️  无 data_sources date 的节点: 1 条（跳过未处理）
   · 兴森科技 ABF 收入预测（2026E）
```

4 次重跑都报同一节点，但 4 篇研报主题完全不同——明显是 base 图谱里的孤立节点 + 全图谱 quarterly_recheck 顺带暴露。

## 完成的工作

1. **根因诊断**：
   - `metric_XinsenABFRevenue2026E` 是 2026-05-18 review_hold 修复批次（hold_fix_2026_05_18 "节点错配 A-2"）新建的 metric 节点
   - 数据源 `data_sources` 只有 `{source, reference, confidence}` 三字段，无 date
   - **唯独**它带 `_meta.temporal.effective_window_days=90`，所以 `quarterly_recheck.py:91` 不会 `continue` 跳过；其余两条同批 metric（Taiyo / VeriSilicon）没打 temporal 故警告静默
   - `quarterly_recheck.py:get_last_updated()` 从 `data_sources[i].reference`/`vintage` 用 `DATE_RE = (20\d{2})[\.\-/](\d{1,2})[\.\-/](\d{1,2})` 抽日期，reference 写的是边 id（`from rel_XinsenABFCustomerRamp2026_Xinsen`）抓不到

2. **3 节点 data_sources 补 date**（用 Edit 工具直接改 canonical JSON）：
   - `metric_XinsenABFRevenue2026E`：date `2026-04-01` / data_vintage `2026-04`（继承自源边 `rel_XinsenABFCustomerRamp2026_Xinsen`）
   - `metric_TaiyoCCLPriceHike2025`：date `2026-04-26`（继承自 `rel_Taiyo_HighSpeedCCL_price`，预防性补）
   - `metric_VeriSiliconNPUProjectProfit`：date `2026-05-13`（继承自 `rel_VeriSilicon_BytedanceSelfDesignNPUGen1_Profit`，预防性补）
   - 每节点 reference 字符串末尾嵌入 `(YYYY-MM-DD)` 供 regex 抽取
   - 每节点 `_meta.date_backfill_2026_05_28` 审计字段记录 inherited_from / source_vintage / reason / reviewer

3. **实战验证**：Doctor 在 macOS 终端跑 3 篇重跑（CPU / 盛科 / 中科微至），quarterly_recheck 输出 `active 269 · expired 5 · ever_continuing 4`，**no_date 桶清零** ✓。第 4 篇 `deep-research-report.md` 仍 60s+ timeout（两个通道都试过）。

4. **deep-research-report.md 处置**：
   - 决策记录 2026-05-23 已说明这篇是 NVL72 BOM 拆解的 raw 研究材料，结构性增量（4 节点 5 边）已**手工 patch 入库**
   - 文本含 Notion footnote 引用 `【N†L行号】` + 4 张巨型 BOM 表格 + 大量按规则不入图谱的高时效价值数据（$7.8M / ASP / 涨幅% / 股票代码），LLM batch 通道处理会硬产违规边 + 推理 budget 撑爆 timeout
   - 处置：建立 **`raw/已手工入库/` 归档子目录**新约定，Doctor 执行 `mv` 把这篇移入
   - `CLAUDE.md` raw 目录结构补该目录说明
   - `渊图_GOTCHAS.md` § 数据质量 新增条目预防后续同类语料污染 batch

5. **GOTCHAS.md 两条新条目**（`docs/渊图_GOTCHAS.md` § 数据质量）：
   - "手工建 metric 节点缺 data_sources date，quarterly_recheck 持续报 no_date warning"
   - "已手工 patch 入库的 raw 语料留在 Obsidian Industrial/ 会被 batch 反复重处理 + LLM timeout"

## 做出的决策

| 决策 | 原因 | 影响 |
|------|------|------|
| 修复方式选"data_sources 补 date 字段 + reference 嵌入日期"而非"改 quarterly_recheck 增加 date 字段直查通道" | 数据侧补全比代码侧加分支更稳健；reference 嵌入日期让现有 regex 直接生效，零代码改动；审计可 grep 回滚 | 3 节点 data_sources 永久补全；后续手工建 metric 须遵守相同约定 |
| 同批 hold_fix_2026_05_18 创建的 Taiyo / VeriSilicon 一并预防性补 date | 同结构缺陷，避免后续给它们打 temporal 时复现警告；一锅端成本极低 | 3 节点而非 1 节点修复；GOTCHAS 沉淀的预防规则覆盖整批 review_hold_repair 同类 |
| `deep-research-report.md` 移到 `raw/已手工入库/` 而非删除或加 `.skip` 后缀 | 保留语料归档；建立"已手工 patch 入库的 raw 语料"目录约定（未来玻璃芯/韬定律等 manual patch 输入语料可统一沉淀）；目录名比后缀语义更清晰 | 新增 raw 子目录约定；CLAUDE.md + GOTCHAS 同步说明 |
| 不入库 `deep-research-report.md` 剩余内容（按规则不入：$7.8M / ASP / 涨幅% / 股票代码 / 投资排序） | 2026-05-23 决策记录原则——高时效价值数据、ODM 毛利率、投资排序按规则不入图谱；LLM batch 通道反复 timeout 是症状不是原因，强行入库会污染图谱 | 第 4 篇视为已入库（结构性增量手工 patch 覆盖），batch 队列实际处理 17/17 |

## 遗留问题 / 待办

- [ ] **下次入库前确认 XinsenABF 状态机正常**：date `2026-04-01` + window 90 天 = expiry `2026-06-30`，今天 5-28 应该是 `active`（剩 33 天），跑下一篇研报时 quarterly_recheck 自动更新 `temporal.status` 字段，留意有没有意外的 expired/expiring（应该没有）
- [ ] **`deep-research-report.md` 未来若出现 NVL72 后续披露/Q4 业绩**：考虑是否需要在 `raw/已手工入库/` 旁追加补丁 raw 而非反复跑同一文件
- [ ] **批量入库 LLM 输出"中文 id / 缺 type / source 漏前缀造成自环"3 类小坑**：本次 batch 仅 2 处修补，但属 V4 Pro 输出系统性偏差。决策记录 2026-05-28F 已沉淀方法论，未来批量入库后可自动跑一个"V4 Pro 输出体检"短脚本（grep 中文 id / null type / source==target）
- [ ] **3 个新 metric 节点（TaiyoCCLPriceHike2025 / XinsenABFRevenue2026E / VeriSiliconNPUProjectProfit）需要做 wiki 卡吗**：度数低（XinsenABF 度=1，Taiyo 度=1，VeriSilicon 度=1），按 wiki_autogen "度≥4" 阈值不会生成；保持低度数仅供 kb 检索时召回即可

## 记忆分拣提议（Step 3.5）

请 Doctor 点选确认入库；未选中条目不落盘：

### 候选 1 · 决策类 → `brain/渊图/architecture/决策记录.md`
**追加一节 2026-05-28（C 段后或独立条目）**：「`metric` 节点 data_sources date 字段约束 + `raw/已手工入库/` 归档目录约定」——浓缩决策成因 + 修复方法 + 预防规则。约 80-120 字。

### 候选 2 · 经验/模式类 → `brain/permanent/经验库.md`
**新增一条 pattern**：「批量入库后产生的孤立 metric 节点缺 date 字段会让全图谱 quarterly_recheck 持续报警，原因不在新入库研报而在 base 图谱历史遗漏——遇到"每次重跑都报同一条"先怀疑 base 而非增量」。可复用于未来"重复警告但与本次输入无关"类问题的快速定位。

### 候选 3 · 规则/约定类 → `brain/渊图/`（既有规则或新文件）
**raw 目录新约定**：`raw/已手工入库/` 收录决策记录里写"手工构建 patch / 不走 LLM batch"的 raw 语料。是否单独建一个 `brain/渊图/conventions/raw目录约定.md` 沉淀？还是仅在 `决策记录.md` 当条目里说明？

### 候选 4 · 工具心得 → `brain/permanent/经验库.md`（tools 类）
**Edit 工具直接改 canonical JSON 的稳态边界**：3 节点局部修改用 Edit 工具的 old_string 唯一锚定法（包含 `reference` 字段值确保唯一）成功；超大 JSON 文件（111000 行）整文件 Read + Write 不可行，但 grep 定位 + Edit 局部修改是稳健替代。

**不建议入库的条目**（CC 自评）：
- "Edit 工具要求先 Read" → 工具机制，非项目经验，跳过
- "DeepSeek 单次 timeout 60s" → 决策记录 2026-05-28F 已沉淀，不重复
- "category_origin A-1/A-2/A-3 后缀唯一可作 Edit 锚点" → 一次性技巧，价值低

## 相关笔记

- [[2026-05-28-渊图-韬定律金刚石散热与甄别]] · 同日早段会话
- [[渊图/architecture/决策记录]] · 2026-05-17 review_hold 联合审计 / 2026-05-18 15 条 review_hold 清算 / 2026-05-23 NVL72 入库
- [[渊图/architecture/系统概览]]
- [[渊图/GOTCHAS]]
