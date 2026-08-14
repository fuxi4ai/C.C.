# 研究笔记 · 华为AI链全景+自研栈 (2026-05-31)
信源分级: P0=官方公告/政府; P1=顶级投行/专家纪要/拆解实验室/官方技术白皮书(self_reported标注); P2=媒体/国内券商

## U1 · SiCarrier 甄别 [证据充分]
- **2024-12-05 BIS 联邦公报 FR-2024-12-05 (Vol.89 Issue234, doc 2024-28267)**: SiCarrier + SwaySure 入实体清单。理由: significant risk of contributing to Huawei's indigenous advanced-node IC production (military modernization). [P0 govinfo.gov]
- **"Huawei Starlight Engineering Department"(华为星光工程部门) = SiCarrier 别名之一(BIS官方列示)**；现由 深圳重大产业投资集团(Shenzhen Major Industry Investment Group) 全资持有。[P0/P1]
- 与华为 2012 Lab 互换人员+专利；华为转移约十余项专利给 SiCarrier；雇工程师直接参与华为项目。[P1 nomadsemi/Reuters转述]
- SwaySure: presumption of denial。
- 与既有渊图决策吻合(2026-05-29 log: SiCarrier=华为星光分拆, BIS列为华为别名)。
- 图谱现状: 重复节点 company_SiCARRIER(深圳市新凯来技术有限公司) + company_SiCarrier(SiCarrier 新凯来,华为系设备整合商) → dedup
- 源: govinfo.gov FR-2024-12-05; en.wikipedia.org/wiki/SiCarrier; nomadsemi.com; trendforce

## U2 · 华为自研全栈 [证据充分 · 图谱全缺失]
华为昇腾 AI 全栈(hiascend.com 官方, self_reported P1):
- 硬件/架构层: 达芬奇架构 DaVinci(3D Cube矩阵单元) → 昇腾310(推理)/910(训练)/950/Atlas
- 芯片使能层: CANN(Compute Architecture for Neural Networks, 编译器+算子库+调优) 对标 NVIDIA CUDA
- AI框架层: MindSpore 昇思(全场景开源) 对标 PyTorch/TensorFlow
- 应用使能层: MindX/ModelArts
- OS层: openEuler 欧拉(2019华为开源, 2021捐赠开放原子开源基金会; 装机>1000万套; 中国新增服务器OS市场~50%; 支持鲲鹏/昇腾/x86/龙芯) [openeuler.org+IDC P1]
源: hiascend.com; openeuler.org; openatom.org; IDC

## U3 · 制造供应层 [证据充分]
- **TechInsights 拆解确认 昇腾910C = SMIC N+2 7nm**; 双 910B die chiplet 封装; SMIC 约60%良率; 2025 ramp。[P1 TechInsights/DCD/SemiAnalysis]
- 图谱已有 company_SMIC_South -[supplies]-> product_Ascend910_950, company_SMIC_South -[constrains]-> company_HWJ → TechInsights 作证据补强
- CXMT↔华为: 长鑫HBM3 目标对标昇腾970, 2027Q2量产, 现验证阶段 → 维持 hedged, 不建硬supplies边(沿用2026-05-29决策)
- 数据质量: product_CXMT_HBM3 -[supplies]-> company_Shengteng(升腾) 疑似"昇腾"错写公司, 标记待核

## 信源汇总(P1+)
- govinfo.gov FR-2024-12-05 (BIS Entity List, SiCarrier/SwaySure) [P0]
- en.wikipedia.org/wiki/SiCarrier; nomadsemi.com [P1/P2佐证]
- hiascend.com (华为昇腾官方全栈) [P1 self_reported]
- openeuler.org / openatom.org / IDC [P1]
- techinsights.com / datacenterdynamics.com / semianalysis.com (910C=SMIC 7nm) [P1]
