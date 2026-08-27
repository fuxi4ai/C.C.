---
title: 会话日志 2026-08-27 — 渊图 VeraRubin PTFE 材料核实
tags: [log, 渊图]
created: 2026-08-27
updated: 2026-08-27
status: active
type: log
project: 渊图
---

# 会话日志 — 2026-08-27

**项目**：渊图（行业知识图谱）
**主题**：Vera Rubin PTFE 材料对 PCB/CCL/电子布技术路线与中国公司影响——核实、深挖与分析

## 完成的工作

- 实读 canonical 图谱（5133 节点/5732 边）PTFE/正交背板/M9/M10/电子布节点簇：30+ 关键节点 desc/props 逐条读盘 + 核心边关系核验
- 联网核实 8+ 主题：SemiAnalysis Kyber 延迟细节、南亚塑胶 9/1 涨价公告、PTFE 树脂端全球格局（科慕/大金/东岳/昊华晨光/巨化/中英科技）、电子布 8 月价量、生益 PTFE 研发口径（S5300/IEC 61249-3-6）、联瑞新材半年报与募投、生益-联瑞股权沿革与关联交易、两家 08-27 行情估值
- 四轮追问逐层深挖：①PTFE 对三环节影响 ②「生益研发 PTFE」与联瑞口径核实 ③生益持股联瑞商业目的五层 ④联瑞能否入 NV 供应链 ⑤Kyber 延迟是否全链受损 ⑥生益 vs 联瑞投资价值比较
- 落盘核实札记 `Database/行业研究/raw/核实/2026-08-27-VeraRubin PTFE材料与CCL电子布影响核实札记.md`（§1-§11，含信源与触发器）

## 做出的决策

| 决策 | 原因 | 影响 |
|------|------|------|
| canonical 零改动，A/B/C 档补丁全部 propose 待 Doctor 裁 | 被审资产只读 + propose-then-confirm | 图谱 5133/5732 不动 |
| 「NV 6 月已选定 PTFE」自媒体口径判为压缩表述，维持图内「定型顺延 Q4」 | 与图内 08-03/08-25 口径冲突，自媒体惯把「立项验证」压缩成「已选定」 | 冲突收敛为「6 月定方向、Q4 定量产方案」 |
| 沪电 78 层认证、联瑞「过 NV 认证」等 P3 单源口径不入证据链只留触发器 | 与胜宏「独家」叙事互斥、无官方印证 | 证据链保持 P2 及以上 |
| Kyber 延迟判为「β 不受损、α 大洗牌」非全链受损 | 延迟实质=制造良率问题非需求消失；受益方=Vera Rubin 主代链/铜缆/AMD/Google | 分析框架固化进札记 §11 |

## 遗留问题 / 待办

- [ ] A 档补丁（PTFE 树脂端缺口：东岳/中英科技/Rogers/Chemours/Daikin/巨化/昊华补中昊晨光身份 + 2 概念节点）待 Doctor 裁
- [ ] B 档补丁（`concept_CCLPriceHikeCycle2026` 补南亚涨价 prop、`concept_M10CCLMaterialRoute` 补 M10 测试口径、`concept_PTFECCL` 补 IEC 标准 props、`company_Lianrui` 补募投 props）待 Doctor 裁
- [ ] C 档结构疑点（10 组双/三节点并存、2 条 Jingwang-id 边、1 条语义污染边、1 条方向疑点边）待并入 08-28 预核班靶点清单
- [ ] 08-28 18:00 PT 预核班 shenghong-h1-verify：胜宏半年报靶点①-⑥逐项核 + 本札记触发器
- [ ] 触发器：联瑞 Q3 关联交易执行额逼近 3.08 亿额度、台光 Q3 法说会 M10 配方、NV/OEM 官宣正交背板 BOM

## 相关笔记

- [[渊图]]
- [[渊图/architecture/系统概览]]
- `Database/行业研究/raw/核实/2026-08-27-VeraRubin PTFE材料与CCL电子布影响核实札记.md`
- `brain/TODO.md` 渊图·胜宏科技 M9/M10 认证法定披露校验窗口条
