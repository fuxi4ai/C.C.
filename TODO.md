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

> 下面 6 条为 2026-07-21 文件系统健康自检产出（Doctor 批「全部挂 TODO」）。清理执行明细见 `~/Documents/_to_delete_20260721/_MANIFEST.md`（观察期至 2026-08-20）。

- [ ] **E1 · DVA 13 个空转写重跑 ASR**（2026-07-21 挂 · 自检产出 · 中优先）
  SansanYe×9/老石×2/AI个体指南×1 等 0 字节转写＝假完成标记（`dva_asr.py` 幂等只查存在不查大小，挡自动重转）；重跑须视频在场——**任何视频冷层外移前必须先完成本项**；连 `dy_downloader.db` 的 subtitleSource 状态一起核。附带反向对账「有转写无视频」（投知 183>179、卷宇宙 114>100）。

- [ ] **E2 · $CODEX_HOME 字面目录根因修复 + 归位**（2026-07-21 挂 · 低优先）
  Documents 根 `$CODEX_HOME/`＝变量未展开 bug，内含 automation「DVA 定期补库」memory.md（有价值）。顺序：Codex App 侧确认 automation dva-16469639bf3b 已停用 → memory.md 并回真实 CODEX_HOME → bug 目录进隔离区 → 修 automations 里未展开的变量引用。确认前不动（否则目录再生）。

- [ ] **E3 · artifact 保存钩子节流**（2026-07-21 挂 · 改生产脚本，届时单独出方案批）
  `gen_daily_report.py:1392` 每次保存落 2.1MB 全量 index.bak 无轮换（07-08 单日 42 份，且与日报侧 `.pre-*` 同一动作双倍落盘）；拟「同日只留末份 + 跨日轮换保 N」；`.pre-*` 同源同治（管线直落 `archived/_pre-snapshots/` + 轮换）。

- [ ] **E4 · 备份策略统一 gz + 轮换**（2026-07-21 挂 · 改生产脚本，同上单独批）
  Market-Data gz 快照已示范（~75MB/份，较裸 .bak 省 3.2 倍）；拟裸 .bak 复制流全面转 gz；recap predaily/preingest 双钩子同日去重；`bak_fxdeprecate_20260717` 等观察期锚随新策略自然轮换出局。

- [ ] **E7 · 转写覆盖率测量陷阱记 DVA GOTCHAS**（2026-07-21 挂 · 低优先）
  长标题文件名截断丢 aweme_id → ID-join 覆盖率 49% 假象，稳健口径实测 ≈97%+。防未来复测再踩。

- [ ] **dyd 侧 dy_downloader.db 旧副本核实**（2026-07-21 挂 · 低优先 · Doctor 定「留原地挂 TODO」）
  `Claude/Projects/DVA/dyd/dy_downloader.db`（110MB，07-13）比 ops 活跃本体（`DVA-ops/runtime/`，07-18）旧 5 天；核 dyd 本地开发流是否还读它——不需要则移隔离区，避免开发误用旧库。

- [ ] **扫一遍还有几个 brain 注册项目缺 `GOTCHAS.md`**（2026-07-19 挂 · 低优先）
  烛照九阴是撞见才发现没有的，REQ-F2 当年标了 `[x]`「所有 brain 注册项目补齐 GOTCHAS」，说明当时可能只漏了它、也可能不止。
  `for d in ~/Documents/Claude/brain/*/; do [ -f "$d/GOTCHAS.md" ] || echo "缺: $d"; done`
  （Doctor 未表态，CC 按「不升 permanent、挂 TODO 即可」的默认处理）

- [x] **重跑 F5 校准取两腿新 lift**（2026-07-19 完成）
  F5 两腿：lift **2.31** / 12 触发日 / **9 独立事件**。同日连修校准工具三处（F4 可评日缺数当未触发、扫描表 lift 基准不同源、判定改卡独立事件数）。

- [ ] **五因风险温度：挖新因子 + 改计温 function**（2026-07-19 挂 · **Doctor 裁定** · 高优先）

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

- [ ] **驾驶舱接回调级别读数 · 开工**（2026-07-19 挂 · Doctor 已批 PRD §二「批，开工」，但当日未动手）
  PRD：`logs/checkpoints/2026-07-19_驾驶舱接回调级别读数_PRD.md`（17 条交付标准）。
  已定：全局横幅 · 纯展示 · **常驻不隐藏**（L1 也显示）· 视觉直接复用日报温度卡范式（同为 `--bg:#f5f4ed` 暖色卡片页，§六 第 1 条已作废）。
  落点：`index.html` 的 `<div id="tab-cockpit">` 内，控制栏与 `#ck-pills` 之间。
  **代码一行未动**，从零开始。

- [x] **F5 油价腿历史回补**（2026-07-19 完成 · 同日）
  Doctor 终端 yfinance 回补 BZ=F 4150 行 [20091201→20260717]，CC 真隔夜回测 3914 可评日。**三裁定**：5% 档**平反**（45 事件 lift 2.03，非过拟合，lift 沿网格单调）；3% 档**弱信号定论**（155 事件 lift 1.29，预期的"转正"未发生）；**跨区制首例**（四段 lift 全 >2：2.12/2.83/2.02/2.42）。纪要升 v1.6。报告：`AI4ME/F5油价腿回补/CC-F5油价腿长样本回测-20260719.md`。

- [ ] **F4 阈值可达性预检**（2026-07-19 挂 · 低优先 · 回补前必做）
  `200亿` 是绝对阈值。回补 2010+ 之前须先验历史滚动20日募资能否达到该量级——达不到则回补只增"未触发"、事件数不变，等于白干。且期间跨 IPO 暂停（2012–2014/2015）、科创板注册制（2019）、全面注册制（2023）——**跨的是发行制度不是行情**（G-X75）。要补多半得把绝对阈值改成相对值（占流通市值比或滚动分位）。

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

