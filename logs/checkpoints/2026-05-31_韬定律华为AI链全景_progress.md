---
title: progress · 韬定律华为AI链全景+自研栈专项
task: 渊图 · 高度自主化韬定律研究(Doctor委托 3h)
created: 2026-05-31
status: completed_pending_doctor_merge
---

# 任务
Doctor 选定主攻：华为 AI 链全景 + 自研栈（"华为链最大结构缺口"）。
产出标准：P1+ 信源；有贡献的线索/结论 或 对现有数据集优化。
执行模式：手工 patch（research-CC，replicate _manual.json 范式），不跑 LLM-ingest（API key 在 Doctor 终端）。Doctor 终端跑 kg_merge + git。

# 容错约定（本任务）
- Write/Read 走宿主路径(/Users/lunarabbit/...)；bash 走 VM(/sessions/...)。脚本统一 bash heredoc 落 VM。
- WebSearch 每主题≤3次；失败退避重试≤2；连续失败→记录跳过不阻塞。
- 每个工作单元(节点组/研究主题)完成即落盘 research notes；每主题更新本 progress。
- 校验门未过不得宣布完成。

# 存量盘点结论(work unit 0 ✓)
- 自研软件/架构栈(达芬奇/CANN/MindSpore/openEuler) 全缺失 → 主补建对象
- SiCarrier 重复节点: company_SiCARRIER + company_SiCarrier → dedup
- CXMT 重复: company_CXMT + company_CXMT_Changxin；product_CXMT_HBM3 supplies 到 company_Shengteng(升腾, 疑似昇腾错写)
- 已有: 昇腾系/鲲鹏/HiSilicon/CloudMatrix/UnifiedBus/SMIC/CXMT/concept_HuaweiEDAAutonomyNarrative(甄别先例)
- patch 格式: report_meta + add_nodes + add_edges
- 图谱基线: 1857 节点 / 2223 边

# 工作单元队列
- [进行中] U1 SiCarrier甄别+BIS别名 研究
- [ ] U2 自研全栈研究
- [ ] U3 制造供应层证据
- [ ] U4 链主编排关联生态命题
- [ ] U5 手工patch author
- [ ] U6 校验门
- [ ] U7 报告+self-audit+交付

# 下一步(若中断从此续)
跑 U1 WebSearch(SiCarrier BIS Entity List Huawei alias) → 落 research_notes.md


# === 进度更新 2026-05-31(单会话长任务) ===
## 已完成工作单元
- U1 SiCarrier甄别+BIS别名 ✅ (BIS FR-2024-12-05 官方; 华为星光工程部门=别名)
- U2 自研全栈研究 ✅ (达芬奇/CANN/MindSpore/openEuler 全缺失→补建)
- U3 制造供应层 ✅ (TechInsights 910C=SMIC N+2 7nm)
- U4 链主编排关联生态命题 ✅
- U5 手工patch author ✅ → mapping/_v3_20260531_韬定律华为AI链全景_manual.json (8节点/20边, 含CUDA对标锚点)
- U6 校验门 ✅ 8项全过(首轮2悬挂端点CUDA/华大九天已修复后复跑通过); delta gate: 1857/2223 → 1865/2243(+8/+20)
- U7 报告+提案+交付 ✅

## 副发现(数据集优化线索)
- 存量20条重复边(同src-tgt-rel) ← 新发现,未入既往日志
- 存量2自环(rel_ChinaAITrainingToInference/rel_METiSCompetitors) ← 已知TODO
- SiCarrier重复节点: company_SiCARRIER(deg2)→并入 company_SiCarrier(deg6)
- CXMT重复节点: company_CXMT_Changxin(deg2)→并入 company_CXMT(deg8)
- product_CXMT_HBM3 -[supplies]-> company_Shengteng(升腾,疑似昇腾错写)
→ 均出"提案+dry-run", 不自动改(防错铁律3 高风险操作Doctor批准)

## 交付物
- mapping/_v3_20260531_韬定律华为AI链全景_manual.json (patch, 校验通过)
- outputs/韬定律华为AI链全景_研究报告_20260531.md
- outputs/韬定律华为AI链_数据集优化提案_20260531.md
- outputs/dedup_dryrun_20260531.py (Doctor终端跑)

## 下一步(Doctor)
1. 终端 review patch → python3 kg_merge.py mapping/行业知识图谱_完整数据库.json mapping/_v3_20260531_韬定律华为AI链全景_manual.json
2. python3 kg_rel_classify.py (可选,本patch已人工定rel) → python3 wiki_autogen.py (新增度≥4节点出卡)
3. dedup: python3 outputs/dedup_dryrun_20260531.py (先dry-run看清单)
4. git commit+push (见报告末)


# === 关键自我修正(甄别第7案) 2026-05-31 ===
初稿误判: 910C = SMIC 7nm制造 (据二手摘要)
核查实证(TechInsights+SemiAnalysis一手): 910B/910C 算力die以台积电7nm为主;
  华为经Sophgo规避采购~290万die,台积电被罚$1B;SMIC N+2可产并爬坡但良率2025偏低;
  台积电die库存~2026初耗尽后才全面转SMIC;真瓶颈=HBM(三星/海力士)。
处理: 不把错误"SMIC制造"写入图谱;改建 metric_Ascend910C_DieProvenance (die来源甄别),
  并修正研究报告结论4。→ 价值高于普通节点:与既有 metric_AscendHBMStockpile/SMIC_South constrains HWJ 闭环。
