---
title: 会话日志 2026-08-17 — Boss老白普查VV盲审与provenance管线闭环
tags: [log, 渊图]
created: 2026-08-17
updated: 2026-08-17
status: active
type: log
project: 渊图
---

# 会话日志 — 2026-08-17

**项目**：渊图
**主题**：Boss老白 131 篇入库后：全量普查 → 三层归因 → VV 外部盲审 → 22 项定向修复 → provenance 管线改造 → 24 样本五维验收 → 全案结项

---

## 完成的工作

- **全量普查（抽查→普查）**：972 新节点分 8 组 subagent 并行 web 核查，459 条断言 ✓280（61%）✗65 △114；117 处订正落图（fix_X/fix_D 清单 + 单进程应用脚本）；报告落 raw/核实/
- **三层归因（回源比对实证）**：ASR 层 ~35-40%（谐音专有名词+缩写）· 语料层 ~30-35%（主播口播即错、方向反转类最危险）· LLM 层 ~20-25%（转录正确被改错：闪迪→美光刻板替换、RDM→RDRAM 熟悉化修正、泛化知识混入）——结论：语料层的错修不掉，独立核查层不可省
- **VV 外部盲审（握手层首次审计委托）**：24 样本盲审包（源文+产物，零我方结论）落 `4AI/Shake hands/to VV/`；chatgpt5.6sol 裁决 ✅6 ⚠️8 ❌10（忠实层 25%）；7 类系统性错误模式 + 6 项整改门 + 最终验收门定义；两轮回执全补文件尾
- **22 项定向修复**：边反向 6、谓词修正 2、删无据边 9、实体归一 2、时间键 1、enrichment 标注 2、修辞修 3——全落 canonical（复检全绿+备份）
- **provenance 管线改造**（PRD 批准后）：kg_ingest 五处（溯源纪律/span 字段模板/_validate_source_span/_fix_asr_misnames 26 组错名闸/_verify_cause_directions 双调用交叉校验）+ kg_promote 第 12 项（span 缺失率 ≤5% 硬闸）+ CLAUDE.md 核查节/四维质量模型 + check_id_consistency.py + 命名黑名单 ASR 错名表
- **24 样本零补丁重跑五维验收**：source_span 全可定位 / enrichment 无混层 / 关系方向无复发 / 实体归一生效 / 时间键无污染——**错误复发 0 例，系统性闭环达成**
- 验收途中追加两处修补：ASR 错名闸（LLM 忠实转录错名，prompt 治不了→后处理）、causes 交叉校验（样本 4 三次重跑三次反向，prompt 到边际→独立复核调用按 span 判向）
- 收尾：wiki 重建 793 卡、PRD 状态回写（已批/已交付）、验收报告落 raw/核实/、握手文件全案结项（994 行）

## 做出的决策

| 决策 | 原因 | 影响 |
|------|------|------|
| 普查架构=断言节点分 8 组 subagent 并行（Doctor 令抽查变普查后设计） | 972 节点全核不现实，断言性节点 216 个是错误高发区 | 459 条断言一天核完，117 处订正落图 |
| 不搞第三次审计（Doctor 同意） | 两轮审计已到边际递减；重跑验收天然覆盖全样本 | 预算花在管线改造+验收门 |
| VV 盲审处置=定向修+门分两批（Doctor 批推荐） | 全量退回重跑成本高且不保证改善 | 22 项修复止血 + 低成本门三件落地 + PRD 另批 |
| provenance PRD 批准开工（Doctor 批推荐） | 系统性问题根因=无精确 provenance | 管线五处改造 + 24 样本验收全绿 |
| causes 方向=双调用交叉校验（Doctor 批推荐） | 提示词迭代三次到边际（样本 4 三次反向），语义级弱项需机制兜底 | 交叉校验单测通过、验收通过 |
| 验收门按 VV 定义执行：零补丁重跑 24 样本五维检查 | VV 结项回执明确「重跑全绿才认定系统性闭环」 | 闭环达成，P2 晋升限制解除（VV 确认） |

## 遗留问题 / 待办

- [ ] LLM id 非确定性（重跑 id 漂移+偶发拼音杂名 WanYan）→ 观察清单，暂不动 canonical
- [ ] 存量 972 节点 source_span 回填（PRD 明确另批，不夹带）
- [ ] span 硬闸（第 12 项）对普通研报场景未实测——下次真实 batch 首验
- [ ] 样本 12/17 重跑产物 id 漂移，若将来以重跑产物替换 canonical 需 id 对表（另议）
- [ ] git 提交（两仓命令已贴 Doctor 终端，待跑）

## 相关笔记

- [[渊图/architecture/决策记录]] 2026-08-16 条
- PRD `logs/checkpoints/2026-08-16_渊图provenance层改造_PRD.md`（已批已交付）
- 验收报告 `Database/行业研究/raw/核实/2026-08-16-Boss老白24样本重跑验收报告.md`
- 普查报告 `Database/行业研究/raw/核实/2026-08-16-Boss老白普查核查报告.md`
- 握手文件 `4AI/Shake hands/to VV/CC致VV-Boss老白外部审计-20260816.md`（994 行全案留痕）
- 执行资产：outputs/ bb_audit_pack.py · cc_fix_vvaudit.py · cc_verify_rerun.py · cc_fix_verify_apply.py · bb_verify/
