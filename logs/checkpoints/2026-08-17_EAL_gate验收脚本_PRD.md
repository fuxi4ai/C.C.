---
title: PRD · EAL gate 验收脚本（VV 判据机器化）
tags: [prd, acceptance, 剑酒青丘]
created: 2026-08-17
updated: 2026-08-17
status: 进行中
doctor_decision: 待
type: prd
project: 剑酒青丘（EAL）
template_version: v1.0
---

# PRD · EAL gate 验收脚本（VV 判据机器化）

## §一 · 任务目标

**动机**：VV 五轮手工终验（十修~十二修）暴露出同一个结构问题——「自动测试」角色缺位，「完成」声明没有机器判据。四角色配置（CC 提方法写正文执行修改／自动测试锁判据／VV 独立复算与终验／Doctor 方向与授权）中，唯一未落地的是自动测试。本 PRD 把 VV 已给出的判据固化为可重复执行的一键 gate。

**目标**：`brain/.tools/eal_gate_check.py` —— 一键跑完整验收链；**gate 全绿是「A 阶段完成」声明的必要不充分条件**（Doctor 2026-08-17 裁：VV 仍终审，gate 只机器化已知判据）。

**边界裁定（Doctor 2026-08-17 四项）**：
1. 先 EAL 专用·留扩展点（判据集外置文件，不做通用框架抽象）；
2. gate 全绿 ≠ 自动可签，VV 终审不变；
3. 确定性渲染器改造**不进本期**——人工渲染产物当黑盒验指纹，gate 留白盒接口；
4. 判据集增补＝VV 提新判据 → CC 代收落文件+变更记录 → Doctor 批后生效；CC 不得自主增补。

## §二 · 交付标准

### A. 产物

- [ ] `brain/.tools/eal_gate_check.py`（Python 3 标准库 + 已装依赖·无新依赖）
- [ ] `brain/.tools/eal_gate_checks.json`（判据集 v1·外置：fingerprints / denylist / 数值期望 / 豁免清单）
- [ ] `backtest/repro_v23/test_failfast.py` 由 gate 直接调用（已是产物·gate 集成而已）

### B. gate 检查项（判据集 v1·全部源自 VV 四轮终验原文）

1. **环境**：python3 为 3.10.x；`statsmodels.__version__ == 0.14.6`。
2. **复现**：实跑 `estimate_m4.py` 退出 0，输出含 M4 n=115·R²=.747183·adjR²=.737989·AIC=156.538；G5 AIC 190.116/191.996/194.667/198.225；φ=0.0327·p=0.6946；score .123814/.101065/.082497/.069569；`full: 4/4 converged, retry=0`；`rolling: expected=61, common=61`；`retry/failure/exception=0/0/0`。
3. **fail-fast**：实跑 `test_failfast.py` 10/10 绿。
4. **SHA**：`shasum -a 256 -c SHA256SUMS` 八项全 OK（不自哈希）。
5. **canonical 指纹**：台账 md 正向指纹（+0.1774/−2.7087/开放簇·截至 8/14/0 净（2 raw）/四项 AIC/四项 score/121 个似然贡献/冻结环境独立复得/仅机械描述/constructed-regressor/双截止日/CAR [0,+3] 已统一）全在；denylist（−4.92/+2.39/唯一持续类/建议上修/与 VV 逐位一致/190.115/rev8 未限定）零命中，历史语境带勘误标签的豁免清单放行。
6. **载体一致**：mirror `index.html` 同套指纹/denylist 校验（黑盒）；`_artifacts_manifest.txt` 该行 bytes/sha12 与盘上文件一致。
7. **快照真源**：`scheduler_snapshot.py` 静态检查 `ARTIFACTS_TREE` 指向 Gateway-workspace（防回滚）。
8. **发布器保险丝**：静态检查 `--write` 禁用分支与 previewRoot containment 存在；冒烟跑 `--preview` 越界路径 exit=1。

### C. 分层与可运行面

- 沙箱可跑：1~6、8（7 为静态检查·沙箱亦可）。
- Gateway active 自动检查**不在本期**（沙箱不可达）——gate 只验 mirror；Gateway 层由 update_artifact 后回读与周巡检班覆盖。gate 输出必须显式区分「已验/未验（需 Mac 原生）」两层。

### D. 输出契约

- 每项 PASS/WARN/FAIL；FAIL 给出精确证据行（文件:行号:匹配内容）。
- 汇总行：`gate: 8/8 PASS → 可声明"A 阶段完成"（VV 终审仍必需）`；任一 FAIL → 退出码非零，输出「不可声明完成」。
- gate 自身的 fail-fast：注入破坏（改一个指纹值/删一行 panel/篡改 denylist 豁免）后 gate 必报 FAIL——固化为 `test_gate_self.py` 冒烟（3 用例：指纹缺失必 FAIL·denylist 命中必 FAIL·manifest 失配必 FAIL）。

## §三 · 非交付项

- 确定性渲染器改造（另立 PRD；gate 黑盒验指纹、留白盒接口）
- B 阶段 G2/G3 的判据（G2/G3 落地时按同一判据集增补流程进 gate）
- 通用框架抽象（判据集 json 即扩展点，不做引擎化）
- Gateway active 自动层（沙箱不可达·Mac 原生/周巡检班另议）

## §四 · 验收方式

- [ ] 沙箱实跑 gate：8/8 PASS、退出 0；`test_gate_self.py` 3/3 绿（注入破坏全部被抓）
- [ ] Doctor Mac 原生跑同脚本 exit 0（含沙箱层一致结论）
- [ ] VV 审阅判据集 v1 完整性并终验签字（gate 全绿是必要不充分条件的第一次实战）
- [ ] 判据集增补流程首演：VV 下一轮任一新判据 → CC 代收落 json+PRD 变更记录 → Doctor 批

## §五 · 变更记录

- 2026-08-17 CC: 立 PRD · 四边界按 Doctor 裁定（EAL 专用·必要不充分·渲染器不进·VV 增补 Doctor 批）
