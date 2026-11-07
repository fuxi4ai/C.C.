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

1. **环境**：python3 为 3.10.x；`statsmodels.__version__ == 0.14.6`。〔现行 v1.1（2026-11-06 Doctor 批）：解释器按 env `EAL_GATE_PYTHON` → 判据集 `python_cmd` → PATH 解析；版本须 ∈ `>=3.10,<3.14`（候选运行范围，仅 3.10.20 已验，3.11～3.13 未验、不得宣称支持）；statsmodels 0.14.6 不变。〕
2. **复现**：实跑 `estimate_m4.py` 退出 0，输出含 M4 n=115·R²=.747183·adjR²=.737989·AIC=156.538；G5 AIC 190.116/191.996/194.667/198.225；φ=0.0327·p=0.6946；score .123814/.101065/.082497/.069569；`full: 4/4 converged, retry=0`；`rolling: expected=61, common=61`；`retry/failure/exception=0/0/0`。
3. **fail-fast**：实跑 `test_failfast.py` 10/10 绿。〔现行：该件已扩至 13 例，判据为普通与 `-O` 双模式 exit 0（2026-11-06 VV 实读 13/13）。〕
4. **SHA**：`shasum -a 256 -c SHA256SUMS` 八项全 OK（不自哈希）。
5. **canonical 指纹**：台账 md 正向指纹（+0.1774/−2.7087/开放簇·截至 8/14/0 净（2 raw）/四项 AIC/四项 score/121 个似然贡献/冻结环境独立复得/仅机械描述/constructed-regressor/双截止日/CAR [0,+3] 已统一）全在；denylist（−4.92/+2.39/唯一持续类/建议上修/与 VV 逐位一致/190.115/rev8 未限定）零命中，历史语境带勘误标签的豁免清单放行。
6. **载体一致**：mirror `index.html` 同套指纹/denylist 校验（黑盒）；`_artifacts_manifest.txt` 该行 bytes/sha12 与盘上文件一致。〔2026-11-06 VV R1：v1/v1.1 实现漏掉 mirror 侧 denylist，脚本修订后补齐，豁免语义同台账（`<h2+>` 段级 / 行级关键字）。〕
7. **快照真源**：`scheduler_snapshot.py` 静态检查 `ARTIFACTS_TREE` 指向 Gateway-workspace（防回滚）。
8. **发布器保险丝**：静态检查 `--write` 禁用分支与 previewRoot containment 存在；冒烟跑 `--preview` 越界路径 exit=1。〔现行（2026-09-18 Doctor 裁改 v3 形态）：静态检查 `execute_registry_promotion.py` 含 `preflight only` 与 `--authorization-token` 两标记（默认 preflight-only + 授权 token 必填）；原 `--write`/previewRoot 字面随 v2.3 退役。〕

### C. 分层与可运行面

- 沙箱可跑：1~6、8（7 为静态检查·沙箱亦可）。
- Gateway active 自动检查**不在本期**（沙箱不可达）——gate 只验 mirror；Gateway 层由 update_artifact 后回读与周巡检班覆盖。gate 输出必须显式区分「已验/未验（需 Mac 原生）」两层。

### D. 输出契约

- 每项 PASS/WARN/FAIL；FAIL 给出精确证据行（文件:行号:匹配内容）。
- 汇总行：`gate: 8/8 PASS → 可声明"A 阶段完成"（VV 终审仍必需）`；任一 FAIL → 退出码非零，输出「不可声明完成」。
- gate 自身的 fail-fast：注入破坏（改一个指纹值/删一行 panel/篡改 denylist 豁免）后 gate 必报 FAIL——固化为 `test_gate_self.py` 冒烟（3 用例：指纹缺失必 FAIL·denylist 命中必 FAIL·manifest 失配必 FAIL）。〔现行：2026-11-06 v1.1 升 5 例（＋ledger_md 指回 stub、指路链断裂）；同日 VV R1～R4 后升 **10 例**（＋mirror denylist 命中 FAIL、mirror 勘误语境豁免正向、真本路径仅在 frontmatter FAIL、`type: pointer # 注释` 判 pointer、`type: "pointer` 不可解析 FAIL）；子进程显式传播 `-O` 并起手实测子进程 optimize（R4）。〕
- 条件项「9. 路径有效性」：判据集 `paths.*` 指向的 `.md`（`ledger_md` 之外、键不在 `pointer_keys`）若 frontmatter `type: pointer` 或 type 声明不可解析 → 以第 9 行 FAIL 输出并退出非零；正常成功路径仍为 8 项、不出现此行（2026-11-06 VV 裁可留，须在此补明出现条件）。

## §三 · 非交付项

- 确定性渲染器改造（另立 PRD；gate 黑盒验指纹、留白盒接口）
- B 阶段 G2/G3 的判据（G2/G3 落地时按同一判据集增补流程进 gate）
- 通用框架抽象（判据集 json 即扩展点，不做引擎化）
- Gateway active 自动层（沙箱不可达·Mac 原生/周巡检班另议）

## §四 · 验收方式

- [~] 沙箱实跑 gate：8/8 PASS、退出 0；`test_gate_self.py` 3/3 绿（注入破坏全部被抓）——✅ 2026-09-18 达成：gate 8/8 PASS exit 0 · self 3/3 绿（判据漂移经 Doctor 裁修订后复跑全绿）
- [✓] Doctor Mac 原生跑同脚本 exit 0（含沙箱层一致结论）——**2026-11-06 Doctor 终端实跑贴回：8/8 PASS · exit 0，判据 1 走 `~/.venvs/eal-repro-v23` 3.10.20 · 与同日沙箱复跑逐行一致 · Doctor 同日口令「代落 ✓」· CC 代记留痕**；原注：**2026-11-06 核明前置**：本机无 Python 3.10、无 statsmodels（任何解释器），须先按 `repro_v23/requirements.lock.txt` 建 venv（默认落点 `~/.venvs/eal-repro-v23`，或 `export EAL_GATE_PYTHON=`解释器）再跑 `python3 ~/Documents/Claude/brain/.tools/eal_gate_check.py`；命令块见 2026-11-06 专场交付
- [~] 2026-11-06 Doctor 终端建 venv（uv · CPython 3.10.20 · lock 10 包）后沙箱同机复跑：**gate 8/8 PASS · exit 0**（判据 1/2/3 真 PASS 路径已实跑覆盖：17 期望串逐位复得）——实施者自验 · `[✓]` 归 Doctor/VV
- [~] 2026-11-06 判据集 v1.1 沙箱复跑：**5 PASS · 0 WARN · 3 FAIL · exit 1**——判据 5 转 PASS（指路 stub 有效 + 真本 18 指纹全在）；FAIL 1/2/3 全为「复现环境未就绪」（机器级前置，见上行）；`test_gate_self.py` **5/5** 普通与 -O 双模式 exit 0（实施者自验 · 独立审核结论见 §五 2026-11-06 行）
- [ ] VV 审阅判据集 **v1.1** 完整性并终验签字（gate 全绿是必要不充分条件的第一次实战）——判据集 v1.1 待 VV 审阅（v1 → v1.1 改动面见 §五 2026-11-06 行）——**2026-11-06 VV 独立审阅：REQUEST_CHANGES 退回修订 R1～R4（见 §五 同日 VV 行），本项保持 `[ ]`**
- [~] 判据集增补流程首演：VV 下一轮任一新判据 → CC 代收落 json+PRD 变更记录 → Doctor 批——本场两处漂移+判据 8 形态变迁即首演素材（Doctor 2026-09-18 已裁：判据按现文修订〔156.538→156.5·删双截止日·mirror 侧 156.4 冻结口径适配〕+判据 8 改 v3 形态〔默认 preflight-only+授权 token〕）

## §五 · 变更记录

- 2026-08-17 CC: 立 PRD · 四边界按 Doctor 裁定（EAL 专用·必要不充分·渲染器不进·VV 增补 Doctor 批）
- 2026-09-18 CC: 专场实施（Doctor /todo 批+「就在这另开专场」）——三产物落盘（eal_gate_check.py + eal_gate_checks.json 判据集 v1 + test_gate_self.py）· 路径适配 v2.3 资产新址（宏观研究体系/EAL 三层全迁后）· 沙箱实跑 5 PASS/1 WARN/2 FAIL：**两 FAIL=判据 v1 与台账现文漂移**（'156.538' 现文仅 156.5 四舍五入·'双截止日' 字面不在——台账为 v2.3 冻结真源不改，判据修订归 Doctor 裁）；WARN=判据 8 字面（--write 禁用分支/previewRoot）随 v2.3 退役形态消失，v3 发布链 fail-safe 已由「默认 preflight-only+授权 token」实现，判据 8 待增补流程更新。追加项①渊图 promote 第 15 项负向单测持久化已落（tests/test_kg_promote_gate15.py·一次通过·canonical 字节不变）；追加项② EAL dry-run 6 项增强——VV 十四轮报告原文不在盘（4AI/brain 双树 grep 零命中），转「判据集增补流程首演」报 Doctor。独立复验（未参与实施 subagent）初验 FAIL→7 缺陷修复→复验 PASS_WITH_LIMITS（残留两处已清）。status=blocked（判据漂移待裁）。
- 2026-09-18 CC: 判据修订裁定落地（Doctor 勾「判据按现文修订」+「判据 8 改 v3 形态」）——① 正向指纹 156.538→156.5、删「双截止日」；mirror 侧适配冻结快照口径（156.4 覆盖）；② 判据 8 改写为 v3 形态静态检查（preflight only + --authorization-token）→ WARN 消。复跑 **gate 8/8 PASS · exit 0** · self 3/3 绿。status=awaiting_acceptance（剩 Doctor Mac 原生同脚本跑 + VV 判据集审阅）。
- 2026-11-06 CC: 判据集修订专场（承 GOTCHAS 剑酒青丘 `NOTE-20261106-001` · 清账场提案 · Doctor 裁「先修判据集再终验」）——沙箱复现 v1 **4 PASS/4 FAIL**（判据 5 ledger_md 指 11-05 退役指路 stub 零命中；判据 1/2/3 本机无 statsmodels）。**边界④ 增补流程第二演**：CC 提三项 → Doctor AskUserQuestion 全批（推荐项）：① 判据 5 双判据（`ledger_md` 改指 archive 真本 + 新增 `ledger_pointer` 指路有效子检：type: pointer、正文含真本相对路径、真本存在非 pointer）；② `environment` 改 `python_range ">=3.10,<3.14"` + statsmodels 精确 0.14.6 + `python_cmd` 可配置（解析 env `EAL_GATE_PYTHON` → json → PATH；1/2/3 统一解释器；不就绪 → 1 FAIL 明文「复现环境未就绪」、2/3 不空跑 FAIL，不降 WARN）；③ 通用 pointer 门禁（paths.* 的 md 为 type: pointer 且不在 pointer_keys → FAIL；self 加 ④⑤ 负向用例）。数值期望串/denylist/豁免/override/判据 4/6/7/8 逐字未动。复跑 **5 PASS/3 FAIL**（FAIL 全为环境前置）· self 5/5。**事实订正**：09-18「8/8 PASS」出自当时 Cowork Linux 沙箱；本 Mac 从未有过复现环境（repro README 的 3.10.12 venv 不在盘上）——「Mac 原生跑 exit 0」须先建 venv。沙箱建 venv 受阻（代理 TLS），交 Doctor 终端。独立审核（未参与实施 subagent · 实读三文件 + diff v1 + 实跑 gate/self 两模式 + 负向探针 a~e）结论：**PASS_WITH_LIMITS**——三项合同全部成立、数值期望串键级比对 IDENTICAL、判据 4/6/7/8 零 hunk；两处边缘缺陷（非可执行解释器路径 `_run` 未捕 PermissionError 致崩溃；v1 `python_prefix` 兼容分支死路）已由 CC 同场修复并复验（`EAL_GATE_PYTHON=/etc/hosts` 不再崩溃、给判据 1 证据；v1 风格判据集 3.13 判 OK），修后 gate 5 PASS/3 FAIL · self 5/5 两模式 exit 0。**限制**：判据 1/2/3 的 PASS 路径（含 `_with_py` 实跑 estimate_m4/test_failfast 与数值串匹配）与 `python_cmd` 存在分支因本机无复现环境**未被实跑覆盖**，只经审读——这正是 Doctor Mac 原生跑要补的面。status 维持 awaiting_acceptance。
- 2026-11-06 CC（续）: Doctor 终端 `uv venv --python 3.10` 建 `~/.venvs/eal-repro-v23`（3.10.20）+ lock 装齐 → 沙箱同机复跑 **gate 8/8 PASS · exit 0**（3 分 04 秒），审核限制「1/2/3 PASS 路径未实跑」已消。剩：VV 审阅判据集 v1.1 + 终验签字；self-test 两模式复跑结果见 GOTCHAS 追记。
- 2026-11-06 CC（续二）: Doctor 终端原生实跑 `python3 ~/Documents/Claude/brain/.tools/eal_gate_check.py` → **8/8 PASS · exit 0**，输出与沙箱复跑逐行一致（沙箱层一致结论成立）。§四 该项证据齐、`[✓]` 待 Doctor 落；剩 VV 审阅 v1.1 + 终验签字。
- 2026-11-06 CC（续三）: §四「Doctor Mac 原生跑 exit 0」由 Doctor 口令「代落 ✓」落 `[✓]`（证据＝Doctor 终端实跑输出 8/8 PASS · exit 0），CC 代记。§四 剩一项：VV 审阅判据集 v1.1 + 终验签字。
- 2026-11-06 CC（续四）: venv 就位后 `test_gate_self.py` 真环境复跑：普通与 -O 均 **5/5 PASS · exit 0**（每用例实跑完整 gate；此前无环境时的 5/5 属弱证据，本次为硬证据）。本专场收口：§四 剩 VV 审阅 v1.1 + 终验签字一项。
- 2026-11-06 VV: 独立审阅判据集 v1.1 → **REQUEST_CHANGES（退回修订，本次不落终验 `[✓]`，NOTE-20261106-001 暂不转 ✅）**。VV 实跑：三文件与 `3e788d4` 一致、CPython 3.10.20 + lock 10 包匹配、真实完整 gate 8/8 PASS exit 0（103.7 s）、test_failfast 普通/-O 各 13/13。需修四项：**R1·P1** 判据 6 mirror 未执行 denylist（PRD §二 B.6 要求同套；隔离 mirror 注入 `<p>建议上修</p>` 并重算 manifest 后仍 8/8 PASS）；**R2·P2** 判据 5 指路正文检查读了整文件，真本路径只在 frontmatter `note:` 也通过；**R3·P2** `_frontmatter` 不剥行尾注释，`type: pointer # 注释` 被判非 pointer；**R4·P2** `test_gate_self.py` 子进程只传 `sys.executable` 未传 `-O`，「-O 5/5」只证父进程模式。三裁点答复：版本范围可保留 `>=3.10,<3.14` 作候选但不得宣称 3.11～3.13 已验；pointer 不加文件大小/关键词启发式、先修 R2 R3；条件第 9 项可留，须在输出契约补明出现条件与非零退出。另请同步 PRD 中版本、self 用例数与判据 8 现行描述。回执 `4AI/Shake hands/to CC/VV致CC-EAL-gate判据集v1.1独立审阅回执-20261106.md`；审阅证据 Codex `Project Mirror/剑酒青丘/research/EAL-gate-v1.1审阅-20261106/`（远端 `042f57a7`）。VV 未改任何受审文件。
- 2026-11-06 CC（续五）: 实读 `eal_gate_check.py` L93/L219/L294 与 `test_gate_self.py` L39，R1～R4 四项**属实**（CC 代记退回结论；修订待 Doctor 裁定场次后按边界④进行）。
- 2026-11-06 CC（续六 · 实施者留痕 · 待独立验收）: Doctor 裁「本场修完回信」→ 按 VV R1～R4 修订 `eal_gate_check.py` 与 `test_gate_self.py`（**判据集 json 逐字未动**，无语义变化）：R1 判据 6 对 mirror 执行同套 denylist（新 `_scan_denylist(text, fp, kind)` 为台账 md 与 mirror html 共用；html 以 `<h2+>` 开段、`<h1>` 复位、行级关键字放行，同行标题余文仍扫）；R2 判据 5 指路正文先 `_strip_frontmatter` 再核真本相对路径；R3 新 `_yaml_scalar` 处理引号与 ` #` 行尾注释，引号不闭合或 `[{|>&*!` 等非标量形态 → `_ptr_state`=bad → ledger_md/ledger_pointer 均明确 FAIL 不放行；R4 自测子进程 argv 前缀 `[sys.executable, *['-O']*sys.flags.optimize]`，起手实测子进程 `sys.flags.optimize` 与父进程不一致即中止并打印。自测 5 → 10 例（⑥ mirror denylist 命中 FAIL · ⑦ mirror 勘误语境豁免正向 exit 0 · ⑧ 真本路径仅在 frontmatter FAIL · ⑨ `type: pointer # 注释` 判 pointer FAIL · ⑩ `type: "pointer` 不可解析 FAIL），每例隔离临时目录、跑完整 gate。**自验（沙箱实跑 05:07～05:43）**：gate **8/8 PASS · exit 0**（判据 6 证据行新增「denylist 零命中」）；self 普通 **10/10 · exit 0**（子进程 optimize=0 实测）；self -O **10/10 · exit 0**（子进程 optimize=1 实测，argv 前缀含 `-O`）。§二 B.1/B.3/B.6/B.8 与 D 加「现行」注释并补判据 9 输出契约（历史原文保留）。独立审核与 VV 复审待。
- 2026-11-06 独立审核（未参与实施的审核者 subagent · 只读 + 自构探针 22 次隔离 gate 子进程 + 一次无缓存完整 gate 100 s）: **PASS_WITH_LIMITS**。R1～R4 均为代码级真实修复（R1 探针：注入 `建议上修` → 判据 6 FAIL 证据行；勘误语境 → PASS；h1/h2 复位有效。R2：frontmatter `note:` 含真本路径、正文指错 → 判据 5「已剥 frontmatter」FAIL。R3：`pointer # 注释`/多空格/`'pointer'  # c` 均判 pointer；`pointer#x` 判 plain（YAML 无空格井号非注释，正确）；`"pointer`/`[pointer]` → 不可解析 FAIL。R4：monkeypatch 捕获 argv，普通/-O/-OO 子进程 optimize 0/1/2 与父一致）。判据集 json 两版解析对拍逐字一致（规范化 sha12 `904d18b8f9c5`）；改动面仅两脚本。限制清单：① HTML 行级豁免可被滥用——把命中词追加到既有含「勘误」的行末、或全文压成单行即整体放行（minified 产物下行不是语义单位；改元素级豁免属判据语义变更 → 边界④ 请 VV/Doctor 裁）；② 末尾注入 `<h2>勘误注</h2>` 后全部尾部豁免（与 md 合同一致）；③ 标题文本不扫（md 侧同，预存）；④ `_frontmatter` 只读前 4096 B（预存）；⑤ `re.split` 位置参数 DeprecationWarning → **CC 同场改 `maxsplit=1`，`-W error` 下编译与探针通过**；⑥ 未核 3.11～3.13、Gateway active、外部消费者对第 9 行的解析。审核者另报「commit 9aaafc8 捎带无关文件」——CC 实读 `git show --stat 9aaafc8`：仅 4 件（两脚本 + 本 PRD + GOTCHAS），**无捎带**，审核者系与相邻 GAI 提交混看；该提交为 05:28 另场/终端所落，非本场 git 动作。
- 2026-11-06 VV（第二轮复审）: **REQUEST_CHANGES**——R2、R4 通过；R1、R3 仍有误放行。R1·P1：同一行多个标题时段状态只按首个标题迁移（`<h2>勘误注</h2><h2>现行结论</h2>` 同行后命中仍放行，分两行即正确 FAIL；无缓存完整 CLI 复现 8/8 PASS 98.0 s）；R3·P2：`type: "po\u0069nter"` 转义保留字面判 plain；有起始 `---` 但无闭合或闭合超 4096 B 读取范围返回 {} 判 plain——三种隔离台账均误报 8/8 PASS。裁：按出现顺序迁移全部标题状态（段级合同不变、不改元素级）；支持的标量形态正确解析、不支持转义 → bad；起始标记存在但不可靠解析 → bad/FAIL；4096 上限可留。补用例：同行/分行双标题各 FAIL；转义 pointer、未闭合、超限三例 FAIL + 无 frontmatter/正常 framework 两对照。VV 本轮普通/-O/-OO 各 18 项观察，真实完整 gate 8/8 98.3 s。回执 `4AI/Shake hands/to CC/VV致CC-EAL-gate-R1R4第二轮复审回执-20261106.md` · 证据 Codex `3cfe8fb9`。
- 2026-11-06 CC（续七 · 二轮修订 · 实施者留痕 · 待独立验收）: `_scan_denylist` html 分支改为 `finditer` 逐标题迁移状态、标题间正文各按当时状态扫（段级合同不变）；`_yaml_scalar` 双引号按 YAML 转义解码（单字符转义表 + \x/\u/\U，未知转义 → bad）、单引号 `''`；`_frontmatter` 有起始 `---` 但读取上限内无闭合 → 返回 bad → `_ptr_state`=bad → FAIL；`_FM_RE` 闭合分隔符须独占一行。自测 10 → **17 例**（⑪ 转义 pointer FAIL · ⑫ 未闭合 FAIL · ⑬ 闭合超 4096 FAIL · ⑭ 无 frontmatter 对照 exit 0 · ⑮ `type: framework` 对照 exit 0 · ⑯ 同行双标题 FAIL · ⑰ 分行双标题 FAIL），真本/指路副本改为成对隔离 EAL 布局（指路正文指向副本真本，判据 5 只因被测分支 FAIL）；新增 `--only` 定向复验开关（汇总行标「子集」）。单元探针：转义/未闭合/超限/同行反序/标题间正文全部按预期；真 stub=pointer、真本=plain。完整 gate 与自测结果待实跑回填。
- 2026-11-06 CC（续八 · 二轮修订实跑回填 · 实施者留痕 · 待独立验收）: 后台串行实跑（Mac 原生 python3 3.13 驱动，判据 2/3 子进程走 `.venvs/eal-repro-v23` 3.10.20）：完整 gate **8/8 PASS · exit 0**（06:27）；`test_gate_self.py --only 11..17` 普通 **7/7**、-O **7/7**（子进程 optimize 实测 0/1）；全集普通 **17/17**、-O **17/17**（06:52～07:48）。日志 `scratchpad/gate_run2_20261106.log`（会话临时区）。改动面：`.tools/eal_gate_check.py` sha256 前 12 位 `8f4efbea3cc7`、`.tools/test_gate_self.py` `27c40a972bac`；`eal_gate_checks.json` `2255badb30c2` 与 `9aaafc8` 一致（git diff 零改动）。独立审核结果另行追记。
- 2026-11-06 独立审核（二轮 · 未参与实施的审核者 subagent · 只读 + 单元探针，未重跑完整 gate）: **PASS_WITH_LIMITS**。R1 同行多标题：`finditer` 逐标题迁移属实（同行正/反序、`<h1>` 复位、`<h3>` 子节、大小写+属性标题、VV 原例同行/分行均各 1 命中；真实 mirror 注入 ⑯/⑰ 片段各 1 命中、基线 0）；R3 转义：`\x`/`\u`/`\U`/单引号 `''` 解码正确，未知转义、hex 不足、未闭合、引号后余文、流指示符均 bad，`pointer#x` 保持原值；R3 无闭合/超限：无闭合→bad、`----`→bad、`--- `（尾空格）与 `---` 紧接 EOF 算闭合、`note: a---b` 不误切、5000 字符填充→bad；七例构造属实（⑬ 闭合在第 5730 字符；期望串均来自 gate 真实输出；两脚本无 `assert`）；3.10 解释器 `py_compile` + import 探针结果一致；`eal_gate_checks.json` 零 diff。**限制（不阻断 · 留 VV/Doctor 裁）**：① `FM_READ_LIMIT=4096` 为文本模式 4096 **字符**而非字节（真实台账 4096 字符≈8207 B），文档/用例名「4096 B」口径不精确；② 无闭合但正文 4096 字符内恰有 `---` 水平线会被当闭合判 plain（YAML frontmatter 固有歧义，⑫ 成立依赖真实台账前 4096 字符无 `---` 行）；③ 标题内文本不扫（新 html 分支剔除全部标题正文，旧版只剔首标题）；跨行标题 `<h2>\n…</h2>` 不识别为标题（fail-closed 方向）；缩进 `  type: pointer` 当顶层键（fail-closed）；BOM 开头判无 frontmatter→plain。审核者披露：3.10 探针刷新了 `.tools/__pycache__/*.cpython-310.pyc`（git 忽略，未删）。
