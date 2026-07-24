---
title: Brain Vault TODO
tags: [todo]
created: 2026-05-14
updated: 2026-07-21
status: active
type: log
---

# TODO

## 待办

- [x] **定时 run 级别读数占位 → 根因已定位并修（2026-07-23 结案·待下班验证）**（2026-07-21 挂 · 时间敏感）
  **定论：定时链路确复发**——07-23 10:11 定时班日报仍占位「级别读数不可用」（非一次性瞬态）。根因＝跨项目 `剑酒青丘/adjustment_grade.py` 的 `_mnt()` 硬走 `../×6`，沙箱平铺挂载下溢出到 `/` → `grade_section` 两分支皆败降级；app.log 无痕系 stderr 落定时会话而非 app.log。**已修**（Doctor 批准·自愈式+env 兵底）：`_find_root()` 改探测「含 Database 子目录的祖先」作根，Mac 正路零改动、平铺沙箱落 `/mnt`；三布局隔离测试 + 真脚本 `--json`(L3·confirm True) 均过。详见 [[烛照九阴/GOTCHAS]] GOTCHA-20260723-001。
  **留验证**：下一工作日（07-24）10:00 定时班后，确认日报「回调级别读数」栏出真读数（非占位）即彻底结案；仍占位则回看 `剑酒青丘` 那班是否实际挂载/env。

- [ ] **brain-save skill Step 5 的 `git add -A` 默认待审查/改**（2026-07-23 挂 · Doctor 授权仅记待办·暂不改 skill）
  Step 5 默认 `git add -A && commit && push`，在工作树积压未提交改动时会混入范围不明的改动（DVA offsite 收尾实例 · 参 [[通用教训]] G-X83 / DVA GOTCHAS GIT-20260723-001）。建议默认流程改为「先探后加」：
  ```
  git status --short
  git add <明确文件列表>
  git diff --cached --check
  git diff --cached --stat
  ```
  只有确认工作树全部改动均属本次保存范围，才允许 `git add -A`。**改 skill 须走 Settings > Capabilities**，本条只记待办、不擅改。

> 下面 6 条为 2026-07-21 文件系统健康自检产出（Doctor 批「全部挂 TODO」）。清理执行明细见 `~/Documents/_to_delete_20260721/_MANIFEST.md`（观察期至 2026-08-20）。

- [x] **E1 · DVA 空转写重跑 ASR（2026-07-24 VV 执行完成·13 条确证真静音）**（2026-07-21 挂 · 自检产出 · 中优先）
  **2026-07-24 结案**：VV 经握手层执行——13/13 从 fuxi 取回（SHA-256 逐条一致）→ 重提交 sensevoice-v1 → **全部 `EmptyOutput`（无可识别语音）**，现各带 `asr_status:"empty"` 的 `.transcript.json`，从「无定性 0 字节假完成」变「已确证真静音」。真相：这批是 SansanYe AI 画面/音乐视频 + 老石 122s「沉浸式开箱」ASMR，本就无解说，非丢失转写。dva_asr 幂等已凭 .json 定性不再重跑。回传 `4AI/Shake hands/to CC/VV回传-E1空转写取回重ASR-20260724.md`。VV 未碰 DB/canonical/正本（守握手层）。
  **孤儿破案（第14条）**：`764710303268505`（15 位）＝**文件名截断**丢 id 的真视频 `7647103032685055247`（SansanYe《CHRONOS HUNTER》新片预告·offsite=1）——DYD 80 字截断坑活实例（[[DVA/GOTCHAS]] RISK-20260721-001）。因截断未 DB-匹配而漏批。**待办**：这第 14 条同样取回+ASR（AI 电影预告·大概率也无语音·低优）；截断转写文件名宜改回全 id。
  反向对账「有转写无视频」（投知/卷宇宙）另账未动。
  SansanYe×9/老石×2/AI个体指南×1 等 0 字节转写＝假完成标记。
  **2026-07-24 核实**：实为 **14 个 0 字节转写**（SansanYe×11 / 老石谈芯×2 / AI个体指南×1）。其中 **13 个 offsite=1**（删源已删本地 mp4·元数据 json 留·**已避开路径假阳性坑**核实：file_path 存的是视频文件夹非 mp4，误判「在」）→ **须先 fuxi 取回再 ASR**；另 1 个 `764710303268505`（短 id）＝DB 孤儿、不在 aweme 表，单独查。**取回清单**：`outputs/E1_取回清单_20260724.tsv`（aweme_id/作者/offsite_uri/本地目标）。
  **好消息**：`dva_asr.py` 的 E1 核心坑**已修**（284-294/410 行·内容感知幂等：0 字节判未完成自动重转，无需手删）。**无批量取回脚本**（recovery_drill 只 verify）。
  **Doctor 终端序列**：① 按清单 scp 从 fuxi 取回 13 mp4 → 各自 file_path 文件夹；② `dva_asr.py --author-dir Downloaded/{作者}/post/ --sec-uid …`（SansanYe/老石/AI个体三个作者，幂等自动重转 0 字节）；③ 孤儿 764710303268505 单独处理（删空转写或重映射）。反向对账「有转写无视频」（投知/卷宇宙）另账。

- [ ] **DVA ASR 云→本地迁移（SenseVoiceSmall·Doctor 批·执行中）**（2026-07-24 挂）
  fuxi 有本地算力 → 甩掉云管线（DashScope key + 火山 TOS + OSS 白名单坑 + 计费 + 网络脆弱）。选型＝阿里开源 `iic/SenseVoiceSmall`（同现云端 sensevoice 家族·中文用例与云版实用等价·FunASR 一行调用·Windows CUDA/CPU 均支持）。方案 `Projects/DVA/docs/ASR本地化迁移方案_20260724.md`。
  **次序（先部署后写码后验收·同 F4 纪律）**：① fuxi 装 `funasr==1.3.22`+modelscope、下载 `iic/SenseVoiceSmall`(~1GB)、最小验证（Doctor/VV 终端·沙箱做不了下载）；② 真实抖音音频本地 vs 云抽样对比；③ CC 改 dva_asr 加 `--backend local`（云默认不动·本地 opt-in·出 diff 待批·装好模型才可测）；④ E1 13 条作首批本地跑验收 → 全面切本地（云留兜底）；⑤ 更新 VV 请求为本地口径（已加前瞻 1b 标注）。
  **CC 现在不改 dva_asr**：沙箱无模型不可测。

- [ ] **E2 · $CODEX_HOME 字面目录根因修复 + 归位（2026-07-24 CC prep 完成·执行待 Doctor Codex App）**（2026-07-21 挂 · 低优先）
  Documents 根 `$CODEX_HOME/`＝变量未展开 bug，内含 automation「DVA 定期补库」memory.md（有价值）。顺序：Codex App 侧确认 automation dva-16469639bf3b 已停用 → memory.md 并回真实 CODEX_HOME → bug 目录进隔离区 → 修 automations 里未展开的变量引用。确认前不动（否则目录再生）。
  **2026-07-24 CC 核实**：`$CODEX_HOME/` 内容＝`.DS_Store` + `automations/dva-16469639bf3b/memory.md`（仅此一文件有值）。真实 CODEX_HOME 沙箱内 `~/.codex` 未命中（在 Doctor Mac 侧·CC 定不了）。**memory.md 6 行内容存档防丢**：
  > `# DVA 定期补库 memory` · 2026-07-11 按要求仅执行一次 `Database/Douyin/DVA-ops/run_refill_watchlist.sh`；latest.json：status=success/exit_code=0/authors_ok=8/8/warning_count=0；摘要 `DVA-ops/summaries/refill-watchlist-20260711-112202-3308.md`；耗时~30s；期间一次 `/bin/ps: Operation not permitted` 告警但状态未受影响。
  **待 Doctor（Codex App 侧·CC 做不了）**：① 确认 automation `dva-16469639bf3b` 已停用（否则目录再生）；② 告知真实 CODEX_HOME 路径。之后 CC 可给 mv 命令：memory.md 并回真实 CODEX_HOME → `$CODEX_HOME/` 整目录移 `_to_delete/隔离区` → 修 automations 里未展开的 `$CODEX_HOME` 变量引用（根治再生）。**沙箱不动**（删/移挂载盘受限 + 停用未确认前动了会再生）。

- [x] **E3 · artifact 保存钩子节流**（2026-07-21 挂 · **2026-07-23 完成·分级 B**）
  `gen_daily_report.py` 每次保存落 2.1MB 全量 index.bak 无轮换（曾单日 42 份）+ 日报 `.pre-*` 同源双倍。**已改**（deletion-free·挂载盘禁删适配）：新增 `_rotate_backups()`（跨日保 5 天·`unlink` 包 try/except，Mac 清·沙箱静默跳）；index.bak 钩子改**日键命名**（同日覆盖去重·42/日→1/日）；`.pre-*` 钩子 `move`→`copy2`+路由 `archived/_pre-snapshots/`+日键+轮换。修一 bug：轮换日键取**末组** 8 位（`.pre-` 快照日，非数据日）。py_compile + 两命名隔离测均过。
  现存积压清理（23M index.bak+13M .pre-*）另走·可逆。

- [ ] **E4 · 备份策略统一 gz + 轮换**（2026-07-21 挂 · **2026-07-23 分级 B 部分：recap 走 Mac 清理·gz 转换留待分级 C**）
  Market-Data gz 快照已示范（~75MB/份，较裸 .bak 省 3.2 倍）；拟裸 .bak 复制流全面转 gz；recap predaily/preingest 双钩子同日去重；`bak_fxdeprecate_20260717`（253MB）等观察期锚随新策略自然轮换出局。
  **2026-07-23 进展（分级 B）**：recap predaily 已按日键 cp（同日自动覆盖），跨日清理**沙箱禁删** → 给 Doctor Mac 清理命令（保最近 N 份），不塞沙箱 SKILL。
  **2026-07-24 分级 C 复核（Doctor 批做 C）· CC 反建议缩范围**：清点后大户＝**两个 ~240MB market_data .bak**（`bak_fxdeprecate_20260717` 旧观察锚 + `bak_preF4backfill_20260723` F4 回补锚·已验证）＝空间 99% 在这俩；recap .bak 仅 ~4MB×7、已被 B 的轮换管着。故「裸 .bak **全面转 gz** 的代码改造」**边际极低**（无高频裸 .bak 钩子·snapshot_market_db.py 早已 gz），reader/回滚复杂度不值当。**CC 建议只做 backlog 压缩、不改代码**：`gzip` 那两个 240MB 锚（Mac·gzip 删原文件沙箱做不了）→ 省 ~320MB。preF4backfill 锚 F4 已验证可考虑直接删（可逆起见先 gz 留着）。命令见交付回报。

- [x] **E7 · 转写覆盖率测量陷阱记 DVA GOTCHAS**（2026-07-21 挂 · 低优先 · **2026-07-23 完成**）
  长标题文件名截断丢 aweme_id → ID-join 覆盖率 49% 假象，稳健口径实测 ≈97%+。已落 `Projects/DVA/GOTCHAS.md` [RISK-20260721-001]（含稳健口径「按非零 .transcript.* 存在性计数」+ 反向对账正交提示）。

- [ ] **dyd 侧 dy_downloader.db 旧副本核实**（2026-07-21 挂 · 低优先 · Doctor 定「留原地挂 TODO」· **2026-07-23 核实：不移**）
  `Claude/Projects/DVA/dyd/dy_downloader.db`（110MB，07-13）比 ops 活跃本体（`DVA-ops/runtime/`，07-18）旧 5 天；核 dyd 本地开发流是否还读它——不需要则移隔离区，避免开发误用旧库。
  **2026-07-23 核实结论**：① dyd fork 自己的开发代码（`config/default_config.py`/`cli/main.py`/`asr_clean.py`/`storage/database.py`/`refresh-cookie.py`）**确引用本地 dy_downloader.db**——非孤儿，dyd 本地开发流在读它 → **按可逆优先，不移**。
  **2026-07-24 悬案解决**：「ops 活跃本体」定位到 **`Database/Douyin/DVA-ops/runtime/dy_downloader.db`**（07-23 08:43·活跃·含 offsite 列，非 Projects 下故前次没找到）。dyd 副本（07-13·无 offsite 列）确是**旧开发库**。**待 Doctor 拍板**：dyd 本地开发流是否改指向 `DVA-ops/runtime` 活跃库（架构选型）；不改则 dyd 旧库留原地（已定不移）。

- [x] **brain 注册项目缺 `GOTCHAS.md` 补齐（2026-07-24 完成·REQ-F2 达成）**（2026-07-19 挂 · 低优先）
  烛照九阴是撞见才发现没有的，REQ-F2 当年标了 `[x]`「所有 brain 注册项目补齐 GOTCHAS」，说明当时可能只漏了它、也可能不止。
  `for d in ~/Documents/Claude/brain/*/; do [ -f "$d/GOTCHAS.md" ] || echo "缺: $d"; done`
  **2026-07-23 扫描结果**：真项目里缺 brain 侧 `GOTCHAS.md` 的有 **4 个：MiroFish / 剑酒青丘 / 星空 / 称象**。
  **2026-07-24 补建（Doctor 批）**：4 个 GOTCHAS.md 全建好。剑酒青丘 填真实 [BUG-20260723-001]（`_mnt` 平铺挂载坑·code 侧归位·交叉引 [[通用教训]] G-X88 + 烛照九阴 GOTCHA-20260723-001）；MiroFish/星空/称象 为骨架（frontmatter+术语+待追加）。REQ-F2「所有 brain 注册项目补齐 GOTCHAS」达成。

- [x] **重跑 F5 校准取两腿新 lift**（2026-07-19 完成）
  F5 两腿：lift **2.31** / 12 触发日 / **9 独立事件**。同日连修校准工具三处（F4 可评日缺数当未触发、扫描表 lift 基准不同源、判定改卡独立事件数）。

- [x] **五因风险温度：挖新因子 + 改计温 function**（2026-07-19 挂 · **Doctor 裁定** · 高优先 · **2026-07-23 回填结案**）

  **回填 2026-07-23**（Doctor 批「整条 [x] + 留尾巴」）：两条工作线 + 两个悬案均已落地，本轮核实归档，整条结案。
  - **① 挖新因子 ✅** — 2026-07-19 遗漏风险因子回测（`AI4ME/CC-遗漏风险因子回测-成交额与浮盈-20260719.md`），机理起点筛出两条，入 `config/risk_factors.json` 环境层（禁作看空计温、只作共振证据）：**a6 量能脆弱态**（创业板成交额 p99·双尾放大器·53 事件 lift 2.06·Fisher p=0.008）、**b6 浮盈集中度**（top5% 成交额占比 p95·24 事件 lift 2.20·**唯一过 20 事件门槛**）。
  - **② 改计温 function ✅** — commit `408d765`「S2 计温 function 两层重构：触发×环境+A6/B6 环境层+risk_function 单一真源（PRD 2026-07-19）」。旧「数因子个数→三态」换成 **触发层(F4/F5) × 环境层(F1/A6/B6)**，S2 口径自 20260720 生效。
  - **③ 悬案·温度带呈现 ✅** — 采「维持并标注证据基础」：k/n 显示（触发无共振 0/23·共振 3/21）+「样本薄·预注册中」注记（commit `b56f3eb`）。
  - **④ 悬案·过期标签 ✅** — 3.2/4.4/9.7% 三腿旧口径已从渲染文案清除，只剩两处 `#` 注释作机理说明。
  - **七问**：`docs/五因回测校准_20260721.md` 自带逐问对照表，07-22 会话已过验收（见 [[2026-07-22-五因regen验收与resume开声固化]]）。
  - **尾巴**（转下方新条）：触发层 F4(4事件)/F5(9事件) 仍 sub-threshold——新因子是在**环境层**加固共振，未在触发层根治「仅 F4 有意义」的病根。

  <details><summary>原始分析块（2026-07-19 挂时·可逆保留）</summary>

  **裁定原话**：「仅 F4 有意义，但意义不大，需要进一步挖掘因子，修改 function。」

  **当前成色**（事件级重估后，全部经修正口径）：

  | 因子 | 独立事件 | lift | fwd3(触发 vs 未触发) | 状态 |
  |---|---|---|---|---|
  | F1 隔夜外盘 | 54 | 1.15 | +0.16% vs +0.56% | 样本够 · **确证无效** |
  | F2 拥挤度 | 6 | 0.00 | — | 样本不足 |
  | F3 杠杆水位 | 9 | 0.87 | +1.24% vs +0.38% | **已结案：两方向皆追认** |
  | **F4 IPO虹吸** | **3** | 1.68 | −0.22% vs +0.45% | **唯一有意义，但薄** |
  | F5 外部紧缩 | 9 | 2.31 | +0.01% vs +0.42% | 样本不足 · 方向平 |

  计温层（F4+F5）全部证据基础 = **12 个独立事件**。五因无一达 20 事件门槛。

  **两条工作线**：

  1. **挖新因子** —— 现有五因中唯一没被推翻的是**机理判断**（F4 发行日程提前公告、信息未被收盘价吸收；F5 油价地缘外生持续；F1 开盘即定价；F3 T+1 追认）。**新因子的筛选起点应是机理而非统计**：先问「这条信息在收盘价里被吸收了吗」，再回测。凡答"已吸收/滞后"的直接不入选，省掉一轮回测。
  2. **改计温 function** —— 现行 function ＝「触发因子数 → 三态」（0→🟢 / ≥1→🟠 / 叠加F1→🔴）。若最终只剩 F4 一个有效因子，这个"数因子个数"的结构就没有意义了。**接手时先定义清楚 function 改造的范围**（是换分档逻辑、换权重、还是整体重构），Doctor 原话较简，需对齐。

  **硬约束**：新因子与新 function 一律须过 [[剑酒青丘/frameworks/回测设计七问]]，报告须让读者不查代码即可回答七问。尤其第 6 问（控制同期行情后的增量）——F3 就是栽在这一问上。

  **仍悬而未决**：温度带的**呈现形态**（下架 / 降级为因子状态列表 / 维持并标注证据基础 / 收缩到 F4 单因子）——Doctor 未选，选择是"先把东西做好"而非"先改怎么展示"。另注：三态旁标注的 3.2%/4.4%/9.7% 是**三腿口径的历史标定，已过期**（分档逻辑按触发数、不受影响，但标签失效）；F5 触发从 76 日缩到 12 日后 🟠 出现频率会明显下降，此变化尚无人标注。

  **相关**：纪要 v1.4 §五-C · [[通用教训]] G-X75/G-X76 · [[烛照九阴/GOTCHAS]] ERR-20260719-002

  </details>

- [ ] **触发层 F4/F5 仍 sub-threshold（五因结案留尾）**（2026-07-23 挂 · 低优先 · 承上条结案）
  五因两层重构后，环境层 A6/B6 已加固共振，但**触发层仍只有 F4(4 独立事件)/F5(9 独立事件) 两个 sub-threshold 因子**，均未过 20 事件门槛——「仅 F4 有意义」的病根是**用共振层缓解、非触发层根治**。无需主动挖数，随行情自然积事件；等 F4/F5 任一过 20 事件门槛后重跑校准复核，或出现新的强机理触发候选时再议。

- [x] **驾驶舱接回调级别读数（2026-07-23 核实：已上线·待 Doctor 终验 PRD[✓]）**（2026-07-19 挂 · Doctor 已批 PRD §二）
  PRD：`logs/checkpoints/2026-07-19_驾驶舱接回调级别读数_PRD.md`（17 条交付标准）。全局横幅·纯展示·常驻·复用暖色温度卡范式·落 `#tab-cockpit` 控制栏与 `#ck-pills` 之间。
  **2026-07-23 核实纠错**：本条 07-19 挂时写「代码一行未动·从零」，但 **07-21 数据层(cockpit_data.py 加 build_market_grade+payload market_grade 键)+展示层(artifact 横幅) 已落地、07-22 已部署上线**。本会话端到端复验全过：A1–A4（live `get_cockpit_payload` 返回 market_grade=L3/nn/hist/asof=20260722）· B1–B4（market_grade 在五函数体 0 命中·clocks 未变）· C1–C4（现网 artifact 横幅要件齐·DOM 内 0 禁词）· D1（py_compile OK）· E2（payload 应答+横幅在现网 HTML＝07-21 白名单阻塞已解、已部署）。今日 `adjustment_grade._mnt` 修复同惠及此数据源。
  **余项（Doctor）**：① 桌面肉眼终验横幅渲染（E2 [~]·CC 无法代观察）；② PRD 17 条 `[?]`→`[✓]` 由 Doctor 落。**清理候选**：`Database/龙鱼-标的分析库/_artifact_pending_longyu-holdings-board.html`（07-21 待推件）已被 07-22 现网版超越、成陈旧，建议移 archived（可逆·不删）。

- [x] **F5 油价腿历史回补**（2026-07-19 完成 · 同日）
  Doctor 终端 yfinance 回补 BZ=F 4150 行 [20091201→20260717]，CC 真隔夜回测 3914 可评日。**三裁定**：5% 档**平反**（45 事件 lift 2.03，非过拟合，lift 沿网格单调）；3% 档**弱信号定论**（155 事件 lift 1.29，预期的"转正"未发生）；**跨区制首例**（四段 lift 全 >2：2.12/2.83/2.02/2.42）。纪要升 v1.6。报告：`AI4ME/F5油价腿回补/CC-F5油价腿长样本回测-20260719.md`。

- [x] **F4 阈值可达性预检**（2026-07-19 挂 · 低优先 · 回补前必做 · **2026-07-23 完成**）
  `200亿` 是绝对阈值。回补 2010+ 之前须先验历史滚动窗募资能否达量级——达不到则回补只增"未触发"、事件数不变，等于白干。
  **2026-07-23 预检结论**（ipo_daily 现覆盖 2024-01→2026-07·236 行·滚动 10 日历日现行口径）：
  ① 连当前注册制 era 都勉强触发——≥200亿 仅 5 触发日/236(2.1%)、~2 独立事件，几乎全靠单只巨型 IPO（长鑫 666亿@20260716 顶到 689亿峰值；次大 246亿）。**F4 薄样本是结构性、非数据缺口**。
  ② 历史可达性锁「发行制度」非「行情」（G-X75）：2012–2018 两次暂停(2012.11–2013.12/2015.7–2015.11)+小盘限价 era 基本到不了 200亿→回补白干；2010–2011(巨型银行 IPO)+2019 后(科创板/注册制大盘)能达但只在巨型簇集。
  ③ 绝对 200亿 跨 era 不可比：同 200亿 抽 2010 的~20万亿池 vs 2026 的~90万亿+ 池，相对冲击天差地别→固定阈值污染跨 era lift。
  **裁断**：绝对 200亿 回补＝白干+造不可比事件。要有意义**必须先把绝对阈值换相对值**再回补；即便如此 F4 仍会薄。**2026-07-23 Doctor 定：换相对阈值·出方案**（见下条）。

- [x] **F4 绝对阈值 → 相对阈值（选型 B·募资/成交额比）· 2026-07-23 落地**（Doctor 批「换相对阈值·选型 B·p95」）
  **已完成**：回补到位（ipo 2020-02+·成交额 2010+）→ 校准 p95(N10/M30/th0.045) → 改码四文件 + 单源 helper：`risk_function.py` 加 `f4_ratio_trigger()`（两端共用·G-X73）；`risk_factors.json` f4 换相对键(旧绝对降级 _deprecated·可回滚)；`calibrate_risk_factors.py`（load 成交额+F4块相对+扫描网格 ratio_th）；`gen_daily_report.py`（生产计算+展示相对口径）。三 py py_compile 过；calibrate 真跑权威＝可评1567/触发78/**14事件/lift2.63**/P(冰|触)10.3%（CC 独立复现曾得2.68·冰点标签口径微差·事件数一致·以真跑为准）。七问报告 `docs/五因回测校准_F4相对_20260723.md`（Q6 过：低成交额alone lift0·非伪代理；分子主导；跨4年散布）。regime：当前高流动性下长鑫666亿 ratio0.026<阈→F4 休眠(正解)。**余（Doctor 终端）**：`calibrate_risk_factors.py` 真跑重生成七问报告表 + `gen_daily_report.py` regen 让日报 F4 显新口径；git。仍 14<20＝方向真·样本不足档。
  <details><summary>原「等回补」计划（已完成·留档）</summary>
  **选型 B**：rolling-N 日募资 ÷ 近 M 日日均全市场成交额 ≥ 阈值 →「IPO 抽走≈几天成交额」。机理最直接（虹吸=抽流动性），2025+ 验证成立：高流动性 era（日均~2万亿）巨型 IPO 也只抽~2-3% 一天成交额，正解释 F4 现弱；低流动性 era 同额 ratio 更高=虹吸更咬。
  **数据纠错**：`daily_market.volume_trillion` 历史全 0/坏（ERR-20260719-003·勿用）；可用成交额 `market_amount_daily` 仅 2025+。故分子(ipo_daily 2024+)与分母(成交额 2025+)**都需回补**。
  **前置·Doctor 终端（tushare 下载·不在沙箱跑）**：`fetch_ipo.py --from 20100101` + `fetch_market_amount.py --from 20100101`（回补前先 `cp market_data.db → .bak_preF4backfill_{日}`）。
  **回补到位后·CC**：算相对口径校准（M/N/阈值网格）+ 出逐文件 diff。
  </details>

- [x] ~~F3 tushare 历史回补~~ —— **2026-07-19 取消**（Doctor 批）。正反两方向皆为追认，控制行情后零增量，回补只是把追认结论说得更响。见纪要 §五-C。

- [x] **给渊图跑 graphify**（832 nodes, $9.62）
  `cd ~/Documents/Database/行业研究 && graphify . --obsidian --obsidian-dir ~/Documents/Claude/brain/graphify/渊图`
  （需先确认 graphify 在 PATH：`export PATH="$PATH:~/.local/bin"`）

- [x] **给 DVA 跑 graphify**（1070 nodes, $0.85）
  `cd ~/Documents/Claude/Projects/DVA && graphify . --obsidian --obsidian-dir ~/Documents/Claude/brain/graphify/DVA`

- [x] **PEC G-06 至 G-14 认识论陷阱全量入 brain**（frameworks/陷阱-G-06-G-14.md，9 条全量）
  读取 `Projects/PEC/GOTCHAS.md` 后半部分，提炼入 `brain/PEC/frameworks/认识论框架.md`

## 已完成

- [x] **【G-X13 根治 C】全局偏好 Settings 镜像块合并进桌面端个人偏好**（2026-07-07 · 敬语「您」块已每轮注入生效）
- [x] **【G-X13 补丁 D】`brain-resume` 加 Step 0 读全局偏好镜像**（2026-07-07 · 新 skill 已覆盖安装）
- [x] **【brain-anchors】补召回词「暗色·卡片页 / dark card page / 龙鱼看板」**（2026-07-07）
- [x] Brain vault 目录结构初始化（2026-05-14）
- [x] graphify v0.7.16 安装（2026-05-14）
- [x] 知识种子：7 个项目 architecture 文件（2026-05-14）
- [x] 通用教训提炼（2026-05-14）

---

## Brain Vault 对接需求（来自 brain-对接需求-20260514.md）

> 完整需求文档：`brain/references/brain-对接需求-20260514.md`

### P0（不做则 brain 不能跑）

- [x] **REQ-A1** `/resume` 命令实装 — 读最近 3 个 log，输出摘要+建议
- [x] **REQ-A2** `/save` 命令实装 — 填模板写 logs/YYYY-MM-DD-主题.md
- [x] **REQ-C4 / REQ-E1** Projects ↔ brain 关联 + 项目骨架生成器 `register-project.sh`
- [x] **REQ-F1** 锚点触发机制（dva / 龙鱼五力 / 自检 / 天工开物 → 自动加载）
- [x] **REQ-G1** brain/ 纳入 git 版本管理（commit c65bf5e → github.com/fuxi4ai/C.C.）

### P1（关键体验）

- [x] **REQ-A3** `/note [主题]` 命令实装 — inbox/ 新建 + 采集态
- [x] **REQ-B1** frontmatter 验证脚本（`brain/.tools/validate-frontmatter.py`）
- [x] **REQ-B2** wikilink 回链索引（`brain/.index/backlinks.json`）
- [x] **REQ-B4** 全文/标签搜索（`brain/.tools/search.sh`）
- [x] **REQ-C1** Claude Code 对话导入（`import-chats.py` → chats/code/）
- [x] **REQ-D1** 记忆引擎决策（已定单轨纯文件 + ripgrep）（双轨文件+LanceDB vs 单轨文件）
- [x] **REQ-E2** 项目状态看板 Artifact（brain-vault-dashboard）
- [x] **REQ-F2** 所有 brain 注册项目补齐 GOTCHAS.md

### P2（锦上添花）

- [x] **REQ-B3** 孤儿笔记检测（`find-orphans.py`）（permanent/ 笔记 wikilink < 2 的标红）
- [x] **REQ-C2** Claude Web/App 手动导出指引（chats/README.md）
- [x] **REQ-C3** Graphify 集成手册（`run-graphify.sh` + references/graphify-集成.md）
- [~] **REQ-D2** 语义检索 API — 搁置（架构决策已排除 LanceDB）
- [x] **REQ-G2** 备份策略（references/备份策略.md + `backup-icloud.sh`）

