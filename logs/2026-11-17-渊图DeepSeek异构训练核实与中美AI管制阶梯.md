---
title: 会话日志 2026-11-17 — 渊图 DeepSeek 异构训练核实与中美 AI 管制阶梯
tags: [log, 渊图]
created: 2026-11-17
updated: 2026-11-17
status: active
type: log
project: 渊图
---

# 会话日志 — 2026-11-17

**项目**：渊图（跨：AI4ME 交付页）
**主题**：中国训练芯片可用性 → DeepSeek 混卡训练口径核实 → 补节点四道手术 → 三情景公司映射 → 美方升级空间 → 管制阶梯页

---

## 完成的工作

- **Q1 昇腾可用性**：答前沿训练可用性与「海外租不到先进制程算力」的影响量级（带 E 级）。
- **Q2 核实**「DeepSeek 混用 H/B/国产卡，≤3T 参数可控、≥3.5T 需纯 B 卡集群」：源文只写「参数」，没有区分总参数和激活参数；R2 在昇腾上训练失败的说法出自 FT，经 Tom's Hardware 2025-08-14 转述，信源为匿名知情人；T-Rex 论文（arXiv 2607.20145）只证明后训练及 V4-Flash 运筹方向的继续预训练，**不证明基座预训练**在昇腾上完成；MFU 34.22% 为作者自报。
- **Q3 补节点（四道手术，全部走 kg_promote）**：
  - 第一道 `outputs/surgery_20261117_deepseek_hetero_train.py`：在 concept_DeepSeekHeterogeneousTraining 上追加内容，加 3.0/3.5 两条口径锚；新建 concept_AscendV4PostTrainingTRex，再加两条边（used_in / enables）。
  - 第二道 `surgery2_…_auditfix.py`：独立复验查出 2 处 provenance 挂错——FT 出处挂在了 Epoch 页上，「华为牵头」实出自 Implicator、不在 HF 页。处理：新增 Tom's Hardware 转述 FT 的 cite，并订正三处措辞。
  - 第三道 `surgery3_…_wording.py`：description 只追加订正句；Epoch 条目的 note 改成逐字原句。
  - 第四道 `surgery4_…_edgefix.py`：修两条边的 HF reference 与 enables 边的 evidence；TRex 节点描述追加订正；Epoch 条目括注改为「所引报道 Tom's Hardware, 2025-08-14」（**报道日 ≠ 事件日**，这一处是我第三道自己写错的）。
  - 结果：canonical 7653 节点 / 8232 边，sha 97c8f191cf2e7e08；四轮复验均 PASS_WITH_LIMITS。
  - Doctor 分两批提交：行业研究 c83d15bf → 292a9722；brain 93feb74 → 1606240。我已回读核对，已提交版本的 sha ＝ 97c8f191。
- **GOTCHAS 追记**（`brain/渊图/GOTCHAS.md`）：
  - NOTE-20261110-001 同根第 2 次：第 18 项把 `_caliber_` 伴随键（`…_caliber_industry_src`）误判为冲突值。
  - NOTE-20261105-009：第 19 项会把「只改 reference」判为新 cite，web 源须加 cite_overrides。
- **决策记录 / 系统概览**：已加 11-17 条目，计数与印章同步更新。
- **Q4 三情景公司映射**（无反制 / 磷化铟反制 / 稀土全面反制）：按产业列出中美公司受正面或负面影响的情况（E0/E2 分级）。
- **Q5 美方 AI 领域升级空间**：给出 L0–L4 阶梯，并独立审视 Doctor 的命题「稀土是相对终极反制，只有美方打出王牌中方才会用」。审视结论：主干成立；需修正两点——4 月起对 7 种稀土的许可从未暂停，镓锗锑对美禁令暂停到 11-27 到期；稀土更像是可分档的梯子，而不是单发王牌。
- **Q6 发布页面**「中美 AI 管制升级阶梯」：https://claude.ai/artifact/8Jk4ob6DBqkBS5pYYi2emk （slug 3b2a27a1-c775-41bb-bc9c-ddf89b015daf · 仅 owner 可见）；本地源 `~/Documents/AI4ME/中美AI管制升级阶梯/index.html`；内置浏览器预览过一次。

## 做出的决策

| 决策 | 原因 | 影响 |
|------|------|------|
| T-Rex 单独建节点，不把昇腾 MFU 并进异构训练节点 | 论文只覆盖后训练与运筹 CPT，口径和「基座预训练」不同 | 防止「昇腾已能训 V4」的误读 |
| 3.0/3.5T 阈值单位写「源文未区分总参数/激活参数」 | 源文只写「参数」，加「总参数」是推断 | 第 22 项口径锚合规，不夹带 E0 |
| Epoch 条目去 provenance_kind、另挂 Tom's Hardware cite FT | Epoch 原文未提 FT，原来的挂法是归属错误 | 转述链可回溯 |
| 管制阶梯页不登记 hosted-pages.json | 该登记表只收 (Cloud) 定时自推页 | 更新需手动，同链接原地改 |

## 遗留问题 / 待办

- [ ] enables 边 description 里的「基座预训练」措辞（未改，属可选收口）。
- [ ] 两条门禁 GOTCHA 的修法提案：第 18 项伴随键豁免、第 19 项「只改 reference」不算新 cite。待 Doctor 裁。
- [ ] 管制阶梯页时效：2026-11-27 镓锗锑暂停到期、2027-01-10 两项暂停到期、BIS 远程访问规则 90 天宽限，到期后页面状态须手动更新（无定时班）。

## 相关笔记

- [[渊图/GOTCHAS]] · [[渊图/architecture/决策记录]] · [[渊图/architecture/系统概览]]

## 记忆分拣（Doctor 点选）

- ✅ 写入：`permanent/通用教训.md` G-X112 ⑧ 下追记「报道日≠事件日」同根复发（判据补 (d) 日期括注标签须与出处对上）。
- 未选（留日志）：第 18 项伴随键升格通用教训；管制阶梯 permanent 概念卡。
- 遗留待办已挂 `TODO.md` 待办段首条。
