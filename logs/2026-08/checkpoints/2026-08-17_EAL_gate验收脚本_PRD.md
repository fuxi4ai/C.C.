---
title: PRD · EAL gate 验收脚本（VV 判据机器化）
tags: [prd, acceptance, 剑酒青丘]
created: 2026-08-17
updated: 2026-11-06
status: awaiting_acceptance
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

- [~] `brain/.tools/eal_gate_check.py`（Python 3 标准库 + 已装依赖·无新依赖）——已落盘·沙箱实跑·独立复验 PASS_WITH_LIMITS
- [~] `brain/.tools/eal_gate_checks.json`（判据集 v1·外置：fingerprints / denylist / 数值期望 / 豁免清单）——已落盘·含两级豁免（段级/行级）· **2026-11-06 升 v1.1**（Doctor 批三项：双判据 / 版本区间+可配置解释器 / pointer 门禁；数值期望串逐字未动）
- [~] `backtest/repro_v23/test_failfast.py` 由 gate 直接调用（已是产物·gate 集成而已）——gate 判据 3 实跑普通与 -O 双模式 exit 0

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

- [~] 沙箱实跑 gate：8/8 PASS、退出 0；`test_gate_self.py` 3/3 绿（注入破坏全部被抓）——✅ 2026-09-18 达成：gate 8/8 PASS exit 0 · self 3/3 绿（判据漂移经 Doctor 裁修订后复跑全绿）
- [ ] Doctor Mac 原生跑同脚本 exit 0（含沙箱层一致结论）——未跑；**2026-11-06 核明前置**：本机无 Python 3.10、无 statsmodels（任何解释器），须先按 `repro_v23/requirements.lock.txt` 建 venv（默认落点 `~/.venvs/eal-repro-v23`，或 `export EAL_GATE_PYTHON=`解释器）再跑 `python3 ~/Documents/Claude/brain/.tools/eal_gate_check.py`；命令块见 2026-11-06 专场交付
- [~] 2026-11-06 Doctor 终端建 venv（uv · CPython 3.10.20 · lock 10 包）后沙箱同机复跑：**gate 8/8 PASS · exit 0**（判据 1/2/3 真 PASS 路径已实跑覆盖：17 期望串逐位复得）——实施者自验 · `[✓]` 归 Doctor/VV
- [~] 2026-11-06 判据集 v1.1 沙箱复跑：**5 PASS · 0 WARN · 3 FAIL · exit 1**——判据 5 转 PASS（指路 stub 有效 + 真本 18 指纹全在）；FAIL 1/2/3 全为「复现环境未就绪」（机器级前置，见上行）；`test_gate_self.py` **5/5** 普通与 -O 双模式 exit 0（实施者自验 · 独立审核结论见 §五 2026-11-06 行）
- [ ] VV 审阅判据集 **v1.1** 完整性并终验签字（gate 全绿是必要不充分条件的第一次实战）——判据集 v1.1 待 VV 审阅（v1 → v1.1 改动面见 §五 2026-11-06 行）
- [~] 判据集增补流程首演：VV 下一轮任一新判据 → CC 代收落 json+PRD 变更记录 → Doctor 批——本场两处漂移+判据 8 形态变迁即首演素材（Doctor 2026-09-18 已裁：判据按现文修订〔156.538→156.5·删双截止日·mirror 侧 156.4 冻结口径适配〕+判据 8 改 v3 形态〔默认 preflight-only+授权 token〕）

## §五 · 变更记录

- 2026-08-17 CC: 立 PRD · 四边界按 Doctor 裁定（EAL 专用·必要不充分·渲染器不进·VV 增补 Doctor 批）
- 2026-09-18 CC: 专场实施（Doctor /todo 批+「就在这另开专场」）——三产物落盘（eal_gate_check.py + eal_gate_checks.json 判据集 v1 + test_gate_self.py）· 路径适配 v2.3 资产新址（宏观研究体系/EAL 三层全迁后）· 沙箱实跑 5 PASS/1 WARN/2 FAIL：**两 FAIL=判据 v1 与台账现文漂移**（'156.538' 现文仅 156.5 四舍五入·'双截止日' 字面不在——台账为 v2.3 冻结真源不改，判据修订归 Doctor 裁）；WARN=判据 8 字面（--write 禁用分支/previewRoot）随 v2.3 退役形态消失，v3 发布链 fail-safe 已由「默认 preflight-only+授权 token」实现，判据 8 待增补流程更新。追加项①渊图 promote 第 15 项负向单测持久化已落（tests/test_kg_promote_gate15.py·一次通过·canonical 字节不变）；追加项② EAL dry-run 6 项增强——VV 十四轮报告原文不在盘（4AI/brain 双树 grep 零命中），转「判据集增补流程首演」报 Doctor。独立复验（未参与实施 subagent）初验 FAIL→7 缺陷修复→复验 PASS_WITH_LIMITS（残留两处已清）。status=blocked（判据漂移待裁）。
- 2026-09-18 CC: 判据修订裁定落地（Doctor 勾「判据按现文修订」+「判据 8 改 v3 形态」）——① 正向指纹 156.538→156.5、删「双截止日」；mirror 侧适配冻结快照口径（156.4 覆盖）；② 判据 8 改写为 v3 形态静态检查（preflight only + --authorization-token）→ WARN 消。复跑 **gate 8/8 PASS · exit 0** · self 3/3 绿。status=awaiting_acceptance（剩 Doctor Mac 原生同脚本跑 + VV 判据集审阅）。
- 2026-11-06 CC: 判据集修订专场（承 GOTCHAS 剑酒青丘 `NOTE-20261106-001` · 清账场提案 · Doctor 裁「先修判据集再终验」）——沙箱复现 v1 **4 PASS/4 FAIL**（判据 5 ledger_md 指 11-05 退役指路 stub 零命中；判据 1/2/3 本机无 statsmodels）。**边界④ 增补流程第二演**：CC 提三项 → Doctor AskUserQuestion 全批（推荐项）：① 判据 5 双判据（`ledger_md` 改指 archive 真本 + 新增 `ledger_pointer` 指路有效子检：type: pointer、正文含真本相对路径、真本存在非 pointer）；② `environment` 改 `python_range ">=3.10,<3.14"` + statsmodels 精确 0.14.6 + `python_cmd` 可配置（解析 env `EAL_GATE_PYTHON` → json → PATH；1/2/3 统一解释器；不就绪 → 1 FAIL 明文「复现环境未就绪」、2/3 不空跑 FAIL，不降 WARN）；③ 通用 pointer 门禁（paths.* 的 md 为 type: pointer 且不在 pointer_keys → FAIL；self 加 ④⑤ 负向用例）。数值期望串/denylist/豁免/override/判据 4/6/7/8 逐字未动。复跑 **5 PASS/3 FAIL**（FAIL 全为环境前置）· self 5/5。**事实订正**：09-18「8/8 PASS」出自当时 Cowork Linux 沙箱；本 Mac 从未有过复现环境（repro README 的 3.10.12 venv 不在盘上）——「Mac 原生跑 exit 0」须先建 venv。沙箱建 venv 受阻（代理 TLS），交 Doctor 终端。独立审核（未参与实施 subagent · 实读三文件 + diff v1 + 实跑 gate/self 两模式 + 负向探针 a~e）结论：**PASS_WITH_LIMITS**——三项合同全部成立、数值期望串键级比对 IDENTICAL、判据 4/6/7/8 零 hunk；两处边缘缺陷（非可执行解释器路径 `_run` 未捕 PermissionError 致崩溃；v1 `python_prefix` 兼容分支死路）已由 CC 同场修复并复验（`EAL_GATE_PYTHON=/etc/hosts` 不再崩溃、给判据 1 证据；v1 风格判据集 3.13 判 OK），修后 gate 5 PASS/3 FAIL · self 5/5 两模式 exit 0。**限制**：判据 1/2/3 的 PASS 路径（含 `_with_py` 实跑 estimate_m4/test_failfast 与数值串匹配）与 `python_cmd` 存在分支因本机无复现环境**未被实跑覆盖**，只经审读——这正是 Doctor Mac 原生跑要补的面。status 维持 awaiting_acceptance。
- 2026-11-06 CC（续）: Doctor 终端 `uv venv --python 3.10` 建 `~/.venvs/eal-repro-v23`（3.10.20）+ lock 装齐 → 沙箱同机复跑 **gate 8/8 PASS · exit 0**（3 分 04 秒），审核限制「1/2/3 PASS 路径未实跑」已消。剩：VV 审阅判据集 v1.1 + 终验签字；self-test 两模式复跑结果见 GOTCHAS 追记。
