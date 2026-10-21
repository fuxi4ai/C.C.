---
title: PRD · 渊图星空 Newly Emerged 分类与日期滑块
tags: [prd, acceptance, 星空, 渊图]
created: 2026-10-20 20:5x
updated: 2026-10-20 20:5x
status: awaiting_acceptance
task_authorization:
  state: verified
  source_type: 会话裁定
  source_ref: 本会话 2026-10-20（/resume 后 Doctor 直接下达功能需求）
  quote: "渊图-星空，在产业供需信号组加一组分类：'Newly Emerged'即某天及之后新出现的产业信号（增量信息）。在搜索框下生成一条'日期滑块'，由一条微微可见的渐变横向细线，和一颗亮星组成。可以拖动以改变日期。"
  scope: yuantu-starry-skies artifact 的 Newly Emerged 分类 + 日期滑块；星空项目管线/模板改造 + store 推送
roles:
  implementers: [CC]
  independent_reviewers: []  # 待派（未参与实施的 subagent · 交验收前补）
acceptance_authority:
  authority: Doctor
  designation_source_ref:
  designation_quote:
  designated_at:
open_decisions:
  - item: 信号发出日期取数规则（文件名最早日期 → fallback data_vintage 完整日期 → created_at）系 CC 对 Doctor「能否定位到文件名代表的信号发出节点」的落实方案，待 Doctor 验收/目验时确认
    blocking: false
    blocks_requirement_ids: []
    decision_owner: Doctor
    status: open
    resolution_source:
    resolved_at:
type: prd
project: 星空
template_version: v1.2
---

# PRD · 渊图星空 Newly Emerged 分类与日期滑块

## §一 · 任务目标

渊图星空（yuantu-starry-skies artifact）目前市场信号组只有三类静态分类（需求暴增/供应冲击/持续失衡），无法按时间观察「增量」。本任务在信号组新增第 4 分类 **Newly Emerged**——由一条日期滑块决定阈值 D，凡「信号发出日期 ≥ D」的产业信号点亮为天蓝色超新星；并在搜索框上方新增可拖动的日期滑块（渐变细线 + 亮星）。数据语义：信号发出日期 = 该节点来源文件名中的日期（Doctor 指定方向），用于观察新批入图带来的增量信息。

**Doctor 原始指令**(逐字引用):
> "渊图-星空，在产业供需信号组加一组分类：'Newly Emerged'即某天及之后新出现的产业信号（增量信息）。在搜索框下生成一条'日期滑块'，由一条微微可见的渐变横向细线，和一颗亮星组成。可以拖动以改变日期。"
> 〔改稿 · 本会话〕"在搜索框下生成一条'日期滑块'——改在搜索框上方生成"
> 〔AskUserQuestion 裁定 · 本会话〕日期字段方向："能否定位到文件名代表的信号发出节点"；NE 样式："极亮天蓝色超新星，选中此组时其他星进一步暗化并取消其他星的鼠标悬停显示"

**实查依据（CC · 本场实跑）**：canonical 7211 节点中信号节点 63 个，63/63 有 `data_sources.file`、62/63 文件名含可提取日期（跨度 2026-02-08 → 2026-08-16）；`market_signal.tagged_at` 全部为 2026-05-17 一次性标注（不可用）；`data_vintage` 覆盖更广但粒度不一（2026/2026-04/2026-04-16）且有占位值。

**任务规模估算**:
- 预计涉及文件数: 5（canonical_to_starscape.py · starscape-template.html · render 产物 · render-archive 发布源 · 本 PRD）
- 预计耗时: 2-3 小时（管线重跑 ~2 分钟 + 模板改造 + 推送验证）
- 涉及项目: 星空（模板/管线/artifact）· 渊图（canonical 只读）

---

## §二 · 交付标准(Acceptance Criteria · 验收主体＝功能/需求)

### A. 功能需求（用户可感知的行为 / 结果）

- [?] **R1** · 信号面板出现第 4 个分类按钮「Newly Emerged」，与现有三组同交互模式（点击开/关该星层，默认不亮），按钮显示当前日期下的 NE 数量
  - 验收方法: 人工验收（artifact 左下信号面板第 4 按钮在场、点击可点亮/熄灭）+ 机器证据（渲染 HTML 含 data-cat="newly_emerged" 按钮 + 截图）
  - 证据栏: 终稿 HTML 含 `data-cat="newly_emerged"` 按钮与 `sb-count-newly` 计数（1:1 DOM 核验过）；通用 toggle 对 NE 类别 no-op、由 NE 专属监听读态应用；默认无 active、层初始 hidden（沿 10-10「默认不亮」）；截图已生成（宿主侧 · CC 视觉不可见 → 目验归 Doctor）
- [?] **R2** · NE 星层为极亮天蓝色超新星（独立于现有蓝六角/橙十字/金环的第四种星形与配色），点亮后与三类可并存
  - 验收方法: 人工验收（目验超新星形状与天蓝色调 + 与三类叠加不互相覆盖）+ 截图证据
  - 证据栏: SHAPE_SHADERS.nova 在场（8 射主芒+错相次芒+炽亮核+强辉 · 0x52D8FF · vColor×2.0 极亮、pulseMin 0.75）；独立 Points 层、AdditiveBlending、与三层几何互不覆盖；目验归 Doctor
- [?] **R3** · 搜索框上方出现日期滑块：一条微微可见的渐变横向细线 + 一颗亮星 knob，可拖动改变日期；滑块带当前日期与 NE 数量的可读标签；拖动时星层实时增删
  - 验收方法: 人工验收（拖动顺滑、标签随日期更新）+ 机器证据（DOM 存在 · 拖动改变内部日期状态 · 截图）
  - 证据栏: `#signal-slider` 位于 #control 上方（bottom 84px · 居中）；渐变细线（透明→0.30 白→透明）+ 亮星 knob（SVG 四芒+白核+dropshadow 辉光）；pointer 捕获拖动、xToDate/dateToX 往返、标签 `Newly Emerged · {date} · {n}`、localStorage 记忆（try/catch 降级）；node --check 语法过；目验归 Doctor
- [?] **R4** · NE 判定口径正确：信号发出日期 = 节点来源文件名提取日期（多文件取最早）；无文件名日期则 fallback `data_vintage` 完整日期 → `created_at`；63 个信号节点 100% 有值
  - 验收方法: 机器比对（python 独立从 canonical 计算各节点 emergence 值与页面内嵌数据 `signal_emerged_at` 逐节点一致 · 无空值）
  - 证据栏: 星场保留 62 信号节点（canonical 63 中 1 个 degree<1 被 min-degree 过滤）· 62/62 有 signal_emerged_at；独立抽样 10 节点 canonical 直算对拍 10/10 一致；日期范围 2025-05-30→2026-08-16；NE 计数五档锚（06-01→20 · 07-22→12 · 08-01→9 · 08-16→8 · 09-01→0）与内嵌数据直算一致
- [?] **R5** · 选中 NE 时，其他星进一步暗化（较常规更暗），且其他星的鼠标悬停不再显示提示（悬停静默）；取消选中恢复常态
  - 验收方法: 人工验收（选中 NE 后非 NE 星明显压暗 + 悬停无 tooltip；取消后恢复）+ 机器证据（代码路径：neActive 时 mousemove 对非 NE 星直接返回）
  - 证据栏: updateStarVisibility 并入 NE 暗化（非 NE 星 alphas≤0.14 < 常规 0.30、saturation 0.10 压灰）；mousemove hoverFilter = searchMatchSet ?? (neActive ? neSet : null)；搜索态优先（清空先置 null 再重算）；退出焦点/类型过滤均走同一函数恢复；目验归 Doctor
- [?] **R6** · 星空数据不含信号节点时（其他数据集共用模板），滑块与 NE 按钮不出现
  - 验收方法: 机器比对（无 signal_emerged_at 数据时滑块 display:none）
  - 证据栏: SIGNAL_EMERGED 非空才建层；否则走 else 支——sliderEl 维持 hidden class + neBtn display:none（代码路径在场 · 其他数据集未实跑，静态判定）
- [?] **R7** · 选中 NE 组时滑块自动定位到最新增量信息所在天（信号出现日期最大值，NE 集＝该日及之后的信号）
  - 验收方法: 人工验收（点击 NE 按钮 → 滑块跳到最新日 · 标签与 knob 位置更新）+ 机器证据（代码路径：neActive 时 neDate=SIGNAL_EMERGED[last] + rebuildNeLayer）
  - 证据栏: 代码在场（neBtn click 分支 · 十二调①）；最新出现日期＝2026-10-16（补打标签后 SIGNAL_EMERGED 最大值实算 · 该日 NE=1 颗 supply_shock 星）；实际键盘/点击交互归 Doctor 目验
- [?] **R8** · NE 选中时键盘 ←/→ 键改变滑块日期（±1 天 · 界内 clamp · 标签/星层实时更新）
  - 验收方法: 人工验收（按键日期步进）+ 机器证据（capture 相位 keydown · stopPropagation 阻断 OrbitControls 与输入框默认行为 · 搜索框聚焦时不拦截）
  - 证据栏: document keydown capture 监听在场（input 目标豁免）；JS 语法过；交互手感归 Doctor 目验
- [?] **R9** · NE 选中时键盘 ↑/↓ 键轮选当前 NE 星：选中星切入 focus 视角（相机滑移 + 焦点卡 + 链路高亮，与鼠标点选同款），名称行显示「{name} · k/n」，↑上一个 ↓下一个、循环
  - 验收方法: 人工验收（按键轮选 · focus 视角跟随 · 名称行更新）+ 机器证据（neList 按出现日期新→旧排序 · neSelectedIdx 取模循环 · focusOnIdx(neList[idx]) 调用在场）
  - 证据栏: 代码在场（十三调：轮选分支直呼 focusOnIdx）；neList 排序/取模实读核过；交互归 Doctor 目验

### B. 非功能需求

- [?] **N1** · 数据质量：发布产物中信号节点 emergence 值抽样对拍 canonical 100% 一致（含 62 个文件名日期 + 1 个 fallback 节点）
  - 验收方法: 机器比对（python 抽 10 个节点逐值对拍）
  - 证据栏: 独立抽样 10 节点 canonical 直算（文件名日期规则独立重实现）对拍 10/10 一致；62/62 非空；fallback 节点（近线HDD 等无文件名日期者）经 data_vintage 取到值

### C. 任务专属

- [?] **X1** · artifact 推送后渲染正常：节点/边计数与 10-19 推送一致（6013/7708）、既有三组信号计数不变、UI 无破相（截图核实）
  - 验收方法: 机器比对（数据计数）+ 人工验收（screenshot_artifact 截图目验）
  - 证据栏: 内嵌数据 6013/7708 · id 序列与 10-19 数据逐位一致（0 内容差异）⇒ 位置复用合法（seed 42 确定性）；三组信号计数不变（signal_categories 内容 0 差异）；JS 语法 node --check 过、script 标签 10/10 平衡、0 残留 CDN；截图已生成（宿主侧 · CC 视觉不可见 → 目验归 Doctor）

### 分轨签核（v1.3 · 客观轨总 ✓ + 审查员背书）

> **审查员背书记录（2026-10-20 20:5x · Step 7.5）**：审查者＝未参与实施的 general-purpose subagent（agentId a57c505c40da73f02 · 13 次工具调用 · 只读）。验证动作：A 数据口径独立重实现（62/62 逐 id 对拍 0 mismatch · 6013/7708 · subtitle 2026-10-19）· B UI 结构实读（按钮/五元素 1:1 · ui-hidden 含滑块 · R6 else 支在场）· C 主脚本按锚提取 node --check rc=0 + 与模板逐字节 diff=0（63114 bytes）+ script 10/10 + CDN 残留 0 + R5 静态路径在场 · D NE 计数五档独立计算 20/12/9/8/0 与证据全符 · E 管线提取规则实读一致（正则双形态实测）。**总判定 PASS_WITH_LIMITS**。限制清单 7 条：① WebGL 实际渲染/超新星视觉/暗化观感/拖动手感归 Doctor 目验 ② 交互仅静态验证未浏览器实跑 ③ PRD 证据两处措辞已订正（T9 字节数 · R6 分支表述）④ 正则潜在缺陷（年-月形态文件名可能误解析 · 现数据 273 处真实匹配 0 命中 · 管线已加月份/日期值域校验）⑤ 「文件名日期＝信号发出日」语义正确性不判（open_decisions 归 Doctor）⑥ 「与 10-19 一致」以 .bak 备份对拍佐证 ⑦ store 侧实际读取无法在此核验。审查员只有背书权、不打 ✓。

- 客观轨总签（覆盖 R2 机器部分 / R3 机器部分 / R4 / R6 / N1 / X1 机器部分）：
  - covered_requirement_ids: []
  - authority:
  - designation_source_ref:
  - signed_at:
  - result:
  - reviewer_evidence_ref:
- 原则轨（结论/裁定类）共 3 条：R1 交互质感 · R3 拖动手感与视觉 · R5 暗化程度是否合意 —— 验收方逐条 ✓

---

## §2.5 · 执行与交付清单（过程项 · 无 checkbox 表格）

| task_id | 过程项 | task_status | 证据 |
|---|---|---|---|
| T1 | PRD 落盘 brain/logs/checkpoints/2026-10-20_渊图星空NewlyEmerged_PRD.md | done | 本文件（Write 落盘） |
| T2 | canonical_to_starscape.py 增加 signal_emerged_at 提取（文件名日期→vintage→created_at） | done | Edit 3 处 · 独立抽样 10/10 对拍 canonical |
| T3 | starscape-template.html：NE 按钮 + nova shader + 滑块 UI + 暗化/悬停静默 | done | Edit 9 处 · node --check 过 · DOM 1:1 |
| T4 | 管线重跑：canonical sha 核不变（b33f995c1568c5a1…）· 输出 6013/7708 | done | ⚠ sha 有漂移（见变更记录）· 星场内容与 10-19 全等 → 位置复用（seed 42 确定性），布局未重跑 |
| T5 | render.py + CDN 段内联替换（8 script 块锚点）· 发布源落盘 render-archive（改前 .bak） | done | out_final 4.92MB · 0 CDN 残留 · 备份 .bak_20261020_pre_ne · 首版接缝 bug 已修（见变更记录） |
| T6 | update_artifact 推送 + screenshot_artifact 截图核实 | done | 推送成功 · 截图生成但 CC 视觉不可见（目验归 Doctor） |
| T7 | /save 触发 + 落 brain/logs/ | todo | |
| T8 | git commit 命令贴 Doctor 终端（星空仓 local-only · 禁沙箱 git） | todo | |
| T9 | 模板 + 发布源两文件同步校验（逐段 diff） | done | 主脚本逐字节一致（发布源=模板 · 63114 bytes · 独立审查员复跑确认 diff=0） |

---

## §三 · 非交付项(范围排除)

- 不包含: canonical 图谱数据修改——信号发出日期为派生字段，只进星空管线产物，canonical 保持只读
- 不包含: 其他星空数据集（PEC/文明基因/整合等）的 NE 展示——模板共享但按 R6 数据门禁隐藏
- 不包含: 定时班自动刷新星空——维持静态快照型机制；未来新批入图的增量须重跑管线刷新（既有流程）
- 不包含: 搜索框本身及其搜索语义改动（滑块只在其上方新增；不新增搜索别名）
- 不包含: 既有三类信号的展示行为改动（默认不亮逻辑不变）

---

## §四 · 状态（current_status + 变更历史）

**状态变更历史**（只追加实际发生的行）:
| 时间 | 从 → 到 | 谁 | 依据 |
|---|---|---|---|
| 2026-10-20 20:5x | draft → in_progress | CC | 立卷即开工（任务已授权 · Doctor 原始指令 + 两问已裁） |
| 2026-10-20 21:0x | in_progress → awaiting_acceptance | CC | 独立审查 PASS_WITH_LIMITS（背书记录见 §二 分轨签核）· 待 Doctor/指定方终审 |

---

## §五 · 变更记录

- 2026-10-20 20:5x CC: 立 PRD · 含 8 条交付标准（R1-R6/N1/X1）· task_authorization 已记录 · 两问裁定原文已录 §一
- 2026-10-20 20:5x CC: 实查 canonical——63 信号节点文件名日期 62/63 可提取、tagged_at 全 2026-05-17 不可用、created_at 63/63 全覆盖（跨度 2025-05→2026-10-01）；取数规则定为「文件名最早日期 → vintage 完整日期 → created_at」，已登记 open_decisions 待 Doctor 验收确认
- 2026-10-20 20:4x CC: 管线/模板改造完成；canonical 现盘 sha 239f4311… 与系统概览记录的 b33f995c… 不一致（星场相关字段 0 差异、边集 0 差异——漂移在 desc/props 等星场无关字段，渊图决策记录无 10-20 条目可归因，**待 Doctor/V.V. 对账**，不阻断本任务）
- 2026-10-20 20:4x CC: 布局未重跑（本 VM 100 轮 >178s 宿主上限）——改用「同输入同种子确定性」论证：现盘解析节点 id 序列/内容/边集与 10-19 数据逐位全等 ⇒ 位置直接复用，等价于完整重跑
- 2026-10-20 20:4x CC: 内联替换首版接缝 bug（切片偏移 8 字符致主脚本开标签被切成 `t>`）被 node --check + 逐字节 diff 逮出，已重建修正（最终主脚本与模板逐字节一致）
- 2026-10-20 20:5x CC: store 推送成功（update_artifact）；截图已生成但本环境无法回传视觉 → 渲染级目验归 Doctor
- 2026-10-20 21:0x CC: Doctor 目验调参两条（原话「减少超新星的最大亮度范围（呼吸到最大的时候的星光大小），选中增量信息组的时候进一步暗化其他星」）——超新星 pulseMin 0.75→0.70、pulseAmp 0.55→0.28、sizeMul 2.9→2.5；NE 选中时非 NE 星 alphas≤0.14→0.08、saturation 0.10→0.06。模板 3 处改 → 重渲重推（主脚本 58774 bytes 与模板逐字节一致）。开发中拍板裁定，变更记录留痕、不进原则轨
- 2026-10-20 21:1x CC: Doctor 目验二调（原话「选中新增信息组后，其他星的亮度减到目前的50%」）——NE 选中时非 NE 星 alphas≤0.08→0.04（saturation 0.06 不变）。重渲重推（主脚本 58771 bytes 与模板逐字节一致）。开发中拍板裁定，变更记录留痕
- 2026-10-20 21:2x CC: Doctor 目验三调（原话「减到0.02」）——alphas≤0.04→0.02，重渲重推（主脚本 58759 bytes 与模板逐字节一致）。三调终值 0.02 留痕
- 2026-10-20 21:3x CC: Doctor 目验四调（原话「0.01」）——alphas≤0.02→0.01，重渲重推（主脚本 58759 bytes 与模板逐字节一致）。四调终值 0.01 留痕
- 2026-10-20 21:4x CC: Doctor 目验五调（原话「超新星不加过于生硬的星芒，而是自然散热的不规则星芒」）——nova shader 重写：角度微扰两波 + 3.0/5.7/9.1 非整数倍频叠波（疏密不一）+ 芒长调制 + 径向抖动（芒缘不直）+ pow 16→5.5 柔边 + 每星独立 vSeed 随机相（varying 声明移 fragment 头部，防 main 内声明语法错）。重渲重推（主脚本 59474 bytes 与模板逐字节一致）
- 2026-10-20 21:5x CC: Doctor 目验六调（原话「取消星芒的花样，只让他们随呼吸外发光即可」）——nova 改「炽亮核 + 柔辉」，辉半径由 pulseR=0.75+0.45·vPulse 随呼吸扩张；vSeed varying 全链路移除（vertex+fragment 头部）。重渲重推（主脚本 58504 bytes 与模板逐字节一致）。六调终态留痕
- 2026-10-21 00:5x CC: 补打标签专场后数据刷新（另一 PRD）——星空信号节点 62→158、NE 计数锚更新为 D=08-01→48 / 08-16→46 / 09-01→36 / 09-15→23 / 10-01→7、三分类 97/57/34（旧 32/36/22）。本 PRD 的 R4/N1 证据栏所记 62 节点口径为专场前的交付态；功能验收以最终交付态（158 信号）为准
- 2026-10-21 00:4x CC: Doctor 令三功能（原话「在选中NE组的时候，实现三个功能：1、自动定位到最新的增量信息所在天；2、实现键盘左右键改变日期的功能；3、实现键盘上下键选中当前日期不同NE星的功能。」）——新增 R7/R8/R9 验收条目并实施：① 激活即跳最新日（SIGNAL_EMERGED[last]）；② ←/→ ±1 天（capture keydown · 搜索框豁免 · stopPropagation 阻断 OrbitControls）；③ ↑/↓ 轮选 NE 星（neList 新→旧排序 · 高亮 + 名称行）。开发中拍板裁定，变更记录留痕
- 2026-10-21 00:5x CC: Doctor 问「NE 是否应排除 PI（新的 PI 可能是旧的 DS/SS）」——CC 实查：9-10 月 NE 中 5 颗 PI 星均为新量化缺口信息（无翻牌案例）· PI-only 29/57 颗 · PI 与 SS 出现日期分布同构（无「成熟态系统性滞后」模式）。**Doctor 裁「保留 PI 在 NE」（AskUserQuestion 取推荐）**——NE 口径定案：三类全含（DS/SS/PI），不做类别排除；同主题去重另立议题。无需改码，裁定留痕
- 2026-10-20 21:0x CC: §二 全 8 条填 [?] + 证据；§2.5 T1-T6/T9 done；待独立审查（Step 7.5）→ awaiting_acceptance → Doctor/指定方验收
