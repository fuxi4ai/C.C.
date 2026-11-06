---
title: 星空 · GOTCHAS（已知坑 · canonical）
tags: [星空, gotchas, index]
created: 2026-07-24
updated: 2026-11-05
status: active
type: resource
project: 星空
---

# 星空 · GOTCHAS（已知坑 · canonical）

> 本文件是 星空（Starry Skies）项目坑的落地处（REQ-F2 补建，2026-07-24）。
> **编号**：`[BUG-YYYYMMDD-NNN]`（代码）/ `[INFRA-…]`（环境·链路）/ `[RISK-…]`（已知风险）。**状态**：✅ 已修复（**仅由 Doctor 或指定独立验收方落，实施者不得自标**）/ 🔄 待修复·已修待验 / ⚠️ 已知风险。

## 条目

## [BUG-20260813-001] #info 的 overflow-y:auto 连带裁掉卡外伪元素 → 热区失效（折叠坞冷区根因）
**状态**: ✅ 已修复（2026-08-13 四改：改用独立元素 `#info-edgezone`）
**优先级**: 🔴 高
**触发场景**: 全景看点卡右缘 44px 热区用 `#info::after { right:-44px; width:44px }` 实现，实测悬停无效——卡与收合线之间出现「冷区」。
**真因**: `#info` 自带 `overflow-y: auto`，CSS 规则下 `overflow-x` 连带计算为 `auto`——伪元素伸出滚动容器外的部分被整体裁剪（绘画+命中测试都裁），44px 热区从未生效。
**解决**: 卡外热区一律用独立 fixed 元素（`#info-edgezone`），不受卡 overflow 裁剪；热区高度由 JS 同步卡的 `offsetHeight`（伪元素在 scroll 容器里还会随滚动内容移动，独立元素无此病）。
**预防**: 凡「伸出滚动容器边界的伪元素热区/手柄」必先查容器 overflow；两区相邻的 hover 切换另见 BUG-20260813-002。

## [BUG-20260813-002] 纯 CSS hover/:has 切换热区几何有指针跨界竞态 → 改 JS 状态机
**状态**: ✅ 已修复（2026-08-13 五改：JS 标记状态机 + body.info-open）
**优先级**: 🔴 高
**触发场景**: 热区随卡开合变几何（收起 8px 悬浮带 / 打开 44px 整段），若用 `body:has(#info:hover)` 切换——指针从卡跨入间隙的瞬间 `#info:hover` 变 false → 热区回缩 → 指针落空 → 卡收起（冷区或抖动）。
**真因**: hover 状态切换与几何切换同帧竞态，纯 CSS 无「指针离开 A、进入 B」的容错窗口。
**解决**: JS 状态机——mouseenter/mouseleave 布尔标记（overCard/overZone）+ 统一 `syncDock()` 驱动 `body.info-open` 类（开合 + 热区范围两件事同源）；焦点态 `.expanded` 并入同一函数。
**预防**: 交互元素几何随 hover 状态变化且两个热区相邻时，优先 JS 标记状态机；纯 CSS :hover 只适合单元素、几何不变的场景。

## [BUG-20260909-001] 渲染注释与实现脱节（JS 行尾注释「颜色 ×2.6 + size ×1.7」vs shader 实际无增益/×1.3）→ 行为状态误判
**状态**: ✅ 已修复（✅ 2026-10-23 错题本消化 · 未参与实施的审核 subagent 落签 · Doctor 2026-10-23 问答板授权 · 证据：starscape-template-pec.html L860 注释已改「高亮节点尺寸 ×1.3（2026-10-23 错题本消化同步 · 09-08 裁定 1.7→1.3）」且 L861 实现 `sizeMul = 1.0 + starHighlight * 0.3` 与注释一致 · 全文件「×1.7」零命中、「×2.6」零命中 · L891 shader 注释「峰值系数 1.6/1.0 → 1.4/0.85」与实现 L894-895（`1.0 + vHighlight * 1.4 * hiGlow` / `1.0 + vHighlight * 0.85 * hiLift`）一致）
**优先级**: 🟡 中
**触发场景**: 2026-09-09 Doctor 报「PEC 星空选中组的星点亮逻辑掉了」→ CC 排查实读：shader 注释写明 09-08 裁定「选中不再跟随变亮」（实现正确执行了裁定，逻辑没掉、是被裁的）；但 JS 搜索段行尾注释仍残留更早版本的行为描述「极亮（颜色 ×2.6 + size ×1.7 + halo 扩散）」——与 shader 实际（无颜色增益 · size ×1.3 · 散射雾）不符。注释与实现双处脱节，诱导「逻辑掉了」的误判。
**真因**: 视觉迭代裁定频繁反转（30+ 轮），同一行为（highlight 渲染）的描述散落在 shader 内注释与 JS 行尾注释多处，改渲染时只同步了 shader 侧、未 grep 全文清零旧数值描述。
**解决**: 本轮已修——shader 注释改为 09-09 新裁定（selLift 光通量增益 ×1.0/1.5/2.0），JS 搜索段注释同步为实际行为（光通量 ×2.0 + size ×1.3 + halo 柔和扩散 + 呼吸闪烁 + 散射雾）。
**预防**: 改渲染参数/行为时，grep 旧数值描述（如「×2.6」「×1.7」）全文件清零；行为真源在 shader，JS 侧注释尽量不写数值、只写语义（「极亮」）或指 shader。
**来源**: 2026-09-09 Doctor 报「选中组的星点亮」→ CC 实读定位 · 模板 `Projects/星空/prototypes/starscape-template-pec.html`



## [BUG-20260913-001] Safari 阴影过渡伪影三件套——透明阴影/filter 上下文/大模糊过渡均画黑环（2026-09-13 EAL 星空黑环四修闭环）
**状态**: ✅ 已修复（2026-09-13 Doctor 目验「不在了，解决了」· CC 代记留痕）
**优先级**: 🟡 中
**触发场景**: EAL 星空（risk-daily 第三标签）事件星悬停柔晕在 Safari 出现「离星一段距离的黑色外环」。
**真因**: 三因叠加——① 默认态 transparent 色 box-shadow 过渡中间帧被 Safari 画黑；② 元素 filter（hover brightness + 呼吸动画 brightness）建立渲染上下文，大模糊阴影离屏合成出深色边缘；③ 大模糊半径（0→42px）box-shadow 过渡插值本身有伪影。
**解决**: ① 透明阴影改类别色零扩展（`0 0 0 0 var(--star)`）；② hover 与 keyframes 的 filter 全清（亮度由柔晕+芒光承担）；③ 广域柔晕弃用 box-shadow，改 :before 伪元素 `transform:scale(1→2.8)` 展开——transform/opacity 过渡无伪影路径。
**预防**: 星空家族视觉改动凡涉及「悬停发光/柔晕」，默认走 scale 绕行方案；新增大模糊阴影过渡前先查本条三件套。
**来源**: 2026-09-13 EAL 星空视觉调参场 · logs/2026-09-13-EAL星空流线空修复.md · 经验库 EXP-20260913-005-T

## [NOTE-20260913-001] 星核参数复用裁定——PEC 参数适合小星图、渊图参数适合大图景（2026-09-13 实读双 shader 对比）
**状态**: ✅ 已沉淀
**优先级**: 🟢 低
**触发**: 2026-09-13 Doctor 令「参考渊图-星空现在的实现」→ 实读对比渊图/PEC 两现役产物后裁定 EAL 用 PEC 参数。
**真因/事实**: 渊图（08-13 定稿）核 `smoothstep(0,0.10)`、halo 0.50、pow 1.5——光体发散，为 700+ 节点大图景能看清；PEC（09-09 定稿）核 0.05、halo 0.44（09-08 Doctor 亲裁再收窄 30%）、pow 1.85——小而锐、静止克制，「散射交给 bloom」。EAL 22 颗星+页面 K 线为主角 → 选 PEC。
**预防**: 星空家族下次派生选参数先查本条；小星图（<50 星、有主视觉）用 PEC 参数，大图景用渊图参数。
**来源**: 2026-09-13 EAL 星空视觉调参场 · 经验库 EXP-20260913-006-P

## [NOTE-20261101-002] 星空板「数据段替换」未生效——推送件仍为旧口径数据（发布链同族 · 与 10-20 谱系事故/10-19 位置复用族并列）
**状态**: ✅ 已修复（2026-11-01 独立复验 PASS：数据段口径 6089/7816·11-01 与 canonical 对拍一致 · 未参与实施的审核者代签）
**优先级**: 🟡 中
**触发**: 2026-11-01 错题本消化场执行 Doctor「推」（星空板同步重推）时，对拍发现 11-01 凌晨场声称「重跑管线 6089 星点/7816 边·口径 10-26 → 数据段替换组装 → update_artifact 推送」，但 store 实际数据段为旧口径。
**硬证据**: `Claude/临时文件/yuantu-starry-skies_store_2026-11-01.html`（11-01 场推送件留档）与 `render-archive/yuantu-starry-skies-v3-full-inlined.html`（10-21 版）starscape-data 段**逐字节相同**（meta subtitle=2026-10-20 · nodes=6013 · edges=7708），全文仅差 cowork-artifact-meta 包装 520 字节；「6089」在推送件中**零出现**；盘上无 11-01 场新 store JSON 产物（未落盘）。渲染引擎直接消费 starscape-data 段（`JSON.parse(getElementById('starscape-data').textContent)`）。
**根因**: 数据段替换未生效——新 store 跑出（6089/7816 数字与本次重跑吻合，证明管线当时确实跑过）但未进入最终推送件；推送件仍复用 10-21 旧 html 仅加包装层。日志所述与实际推送件不符。
**影响面**: 星空板 10-21 起展示 10-20 口径旧数据，缺 10-26 帕米尔批 +83 节点的星图呈现，与 canonical（7294/7917）脱节 6 天。Doctor 10-21 目验「正常」仅证渲染正常、不证数据口径。
**建议修法**: 已当场修复——本场重跑布局（沙箱 OOM → 分块等价实现 `outputs/layout_starscape_chunked.py` · seed 42 · iters 100）+ 数据段替换 + 三段结构断言 + node --check 9 段 + update_artifact（updatedAt 11-02T05:18Z）；推送件现为 6089/7816 · 口径 2026-11-01。
**预防门禁**: ① 星空板推送前必对拍成品 starscape-data 段 meta.subtitle/kpis 与当批 canonical 口径；② 数据段替换后必 grep 新口径数字（如「6089」）在成品中在场，替换无效=数字缺席当场显形；③ 管线中间产物（store JSON）落盘留痕，勿只存内存/scratch。
**来源**: 2026-11-01 错题本消化场「推」环节实读发现 · 修复证据 `outputs/starscape_store_20261101.json` + `outputs/yuantu-starry-skies_store_2026-11-01v2.html`
**复验注记（2026-11-01 · 未参与实施的审核者代签）**: 判据①—④实跑全绿——新 store 实读 6089 节点/7816 边 · meta.subtitle 含 2026-11-01 · 0 节点缺 position · id 无重复；成品 html starscape-data 段 JSON.parse 得 6089/7816 · subtitle 2026-11-01 · 「6089」在场（旧件 0 命中）· 与旧件段（6013/7708 · 2026-10-20）逐字节不同；canonical 实读 7294 节点/7917 边 · raw sha256 f0e7c4ea…与裁定逐位一致 · store 节点 id 集合与边对集合同 canonical 经 min-degree1+非 expired 独立过滤（6089/7816）逐项相等 · 抽样 10 id 全命中；消费端 list_artifacts yuantu-starry-skies updatedAt 2026-11-02T05:18:52Z ≥ 05:00Z · 部署件 6089×2/6013×0

**追记（2026-11-04 · 同根复发第 2 次 · 布局 OOM）**：官方云端模式下 `device_bash` 跑在 Mac 侧 Linux 虚拟机（**3.9 GB 内存、无 swap**），`canonical_to_starscape.py -d 1 --iters 100` 对 6089 节点整图布局被 **OOM 杀掉（只回「Killed」、data.json 0 字节）**——11-01 那次的「沙箱 OOM」在新环境照样复现。**本次处置**：canonical 与脚本 stage 到云端容器（8 GB）整图跑 334 s → 数据段替换进 render-archive 发布件 → 推送回读逐字节一致。**下次刷新**：要么照此走云端容器，要么用 11-01 的分块等价实现 `outputs/layout_starscape_chunked.py`（seed 42 · iters 100），**别在 device_bash 里直接整图跑**。来源：[[2026-11-04-云端迁移自检与巡检修复]]

---

## 自 Projects 侧并入（2026-11-05 · Doctor 裁 1A：brain 为 canonical）

> 以下条目逐字来自 `Projects/星空/GOTCHAS.md`（并入前 mtime 2026-11-05 15:11:28 UTC · 219 行 · sha256 前 16 位 `d23287adacceca03`），编号体系保留原样；原文件已退为指针。

## P1 调试中沉淀的坑

### G-01 · BFS-from-sources 是 wikilink 图唯一稳定的 depth 算法
原始用拓扑松弛算最长路径，在 brain 这种环密集 wikilink 图上 depth 会爆到 60+。改成 BFS-from-sources（深度 = 从无入边节点出发的层数）才稳定，结果 max_depth=3，符合实际。

### G-02 · Shader halo + UnrealBloomPass 不能同时大
两个都开大就"氲过头"，画面糊成一片。最终配方：shader 做主（核 1.0 / 晕 0.85 / pow 1.5），bloom 做抛光（strength 0.55 / radius 0.35 / threshold 0.15）。

### G-03 · 玻璃按钮做"按键化"的关键是外阴影
单纯的 inset 高光 + 描边只能做出"贴纸"感。要真"键浮起来"必须加 `0 1px 2px rgba(0,0,0,.45)` 极淡外下阴影。这是 REF-001 反模式清单里禁止的"drop shadow"——但那是面板级别禁止；按键级别的物理浮起例外。

### G-04 · `position: fixed` 不能丢
重写 `#control` 时去掉了 `class="panel"`，连带丢了 `position: fixed`，导致按钮滑出文档流。改重写元素的样式时要单独 verify 定位声明。

### G-05 · 按钮等宽用 `min-width + justify-content: center`
不要用 `flex: 1` 来等宽——胶囊是 `inline-flex`，shrink-to-content，flex 等分会失败。设 min-width 取最长按钮的宽度即可。

### G-06 · brain wikilink 解析的命名风格不齐
35 个未解析 wikilink 都因为 Doctor 用 `[[项目名 + 空格 + 文件名]]` 风格，与实际文件 title/stem 不匹配。后续 P2/P3 适配器要做：
1. 按 title 解析
2. 按文件名 stem 解析
3. 按 "项目名 + 空格 + stem" 拼合查询
4. 按 path-style `[[项目名/architecture/系统概览]]` 解析

### G-23 · canonical_to_starscape 的 min_degree 过滤对零度节点无效（2026-09-08 · PEC 复用逮出 · 原误标 G-07 与 L53 撞号，2026-11-05 审计订正 改号）
`parse_kg` 里 `kept = {nid for nid, d in deg.items() if d >= min_degree}`——`deg` 只含边端点，**孤立节点（度 0）根本不在 deg 里**，无论 min_degree 传 0 还是 1 都被无条件排除。PEC 星空首渲 262 节点只剩 173（89 个孤立节点静默丢失），`--min-degree 0` 也救不回。渊图管线没触发过（其图无孤立节点），复用者必踩。
**修法**：`kept = {n["id"] for n in g["nodes"] if deg.get(n["id"], 0) >= min_degree}`——已在 `tools/pec_to_starscape.py` 修复；原版 `canonical_to_starscape.py` 保留原样（渊图语义下无影响），复用者自行对照。
**预防**：转换器输出后必比对「输入节点数 vs 输出节点数」，不等则列差集核对是否预期过滤。

## P2 待解决（开 P2 时再细看）

- [ ] 1000 节点级 force layout 的性能（80 iter × O(N²) = 6.4M 对计算，可能慢）
- [ ] 高密度边渲染：`LineSegments` 在 1155 边时是否要 BufferGeometry 分块
- [ ] 渊图 graph.json 的 `community` 字段如何映射到 `by_community` 染色模式
- [ ] 渊图节点的 `file_type=code` vs `doc` 与类型字典的对接

---

## P2 调试中沉淀的坑

### G-07 · "关系"作为节点类别是语义错误
五桶系统的 `relation` 桶（含解决方案 / 标准）让 Doctor 迷惑——节点应该是名词，关系是边。
**修复**：`relation` → `synthesis 综合`，桶里装"由多个其他概念合成出来的高阶物"。brain 的 `permanent` 也归这一桶（跨项目沉淀的合成知识）。

### G-08 · 行业 ≠ 算法社区
渊图的 9 个 Louvain 社区是"产业 × 切面"的混合（同一社区可能既有公司也有问题也有材料），染色后视觉杂乱。
**修复**：用 keyword + hyperedge 把节点重新分到 5 个语义行业桶（光通信/AI算力/半导体封装/材料能源/其他），force layout 也改按行业聚类。比例 0.77 → 1.55。

### G-09 · Force-directed 的等距副作用
F-R 默认让所有节点保持 ~k 距离的"个人空间"，整张图像盐粒平铺，没有"星云"感。
**修复**：4 个杠杆同时拉：
- 边权重（如有）放大 attractive 力 0.5 + w*1.5
- 同社区斥力 ×0.30（让自己人贴紧）
- 跨社区边 attractive ×0.05（不让外人拽散）
- 高 magnitude 节点在迭代后半段位移除以 mass（hub 压阵脚）

### G-10 · 小社区会被 inter-push 撕开
inter_strength 调高一律拉开间距，但 12 节点的"材料能源"会被四面八方推到 span 110。
**修复**：inter_strength 280 → 100；intra-pull 0.42 → 0.90，让小簇的向心力大于被推力。最终 span 平均 65，比例 1.55。

### G-11 · 流光速度太快像激光打靶
首版 drives 0.42 看起来太机械。
**修复**：所有速度减半至 0.09-0.20 范围，配合 shader 的 life-cycle fade（边缘 8%-92% 之外淡入淡出），看起来像"知识慢慢流动"。

### G-12 · 直线边像数据中心接线
直线 + 静态 = 网络拓扑图。
**修复**：quadratic Bezier 12 段曲线 + 每边一个稳定 pseudo-random 弯曲方向（hash01(ei) 种子）+ bow 0.12-0.30 长度。曲线朝外 35% / 随机 65%——既有整体扩张感又有变化。

### G-13 · 曲线引入的 sub-segment 焦点失效
每条边变 12 段后，原本"按 ei*2 索引更新 alpha"的焦点逻辑失效。
**修复**：维护 `edgeOfSegment` 映射，焦点态时遍历所有 sub-vertex 反查 ei。

### G-14 · 流光也得跟着曲线
流光粒子的 vertex shader 还在用 `mix(start, end, t)` 直线插值——光点跑直线，边走曲线，对不上。
**修复**：shader 改成 quadratic Bezier 公式 `omt*omt*P0 + 2*omt*t*P1 + t*t*P2`，把控制点作为第三个 attribute `ctrlPos` 喂进去。

---

## 关键参数 cheat sheet（v1 调好的值，未来再做新数据集时的起点）

| 参数 | 值 | 出处 |
|---|---|---|
| Force layout 迭代 | 140 次 | 比 80 多 50% 让收敛彻底 |
| 冷却率 | 0.97/iter | 比 0.95 慢 |
| target_radius | 160 | 渊图 170 节点 |
| 同社区斥力 ×= | 0.30 | 让自己人贴紧 |
| 跨社区 attractive ×= | 0.05 | 不让外人拽散 |
| 社区向心 community_pull | 0.90 | 强 |
| 社区互斥 inter_strength | 100 | 弱（被小簇承受） |
| Bezier 曲线段数 SEG | 12 | 平滑足够 |
| Bezier 弯度 bow / 边长 | 0.12 ~ 0.30 | 随机 |
| 弯曲方向 | 35%外凸 + 65%随机 | 兼顾秩序与变化 |
| 流光最快速度 (drives) | 0.20 | 减半后 |
| 流光最慢速度 (演进至) | 0.09 |  |
| 星点 size 公式 | 6 + mag * 11 | mag 1.10-3.14 → 18-40px |
| 星点核 smoothstep | 0.10 | 锐利硬核 |
| 星点晕 pow | 1.5 | 含蓄 |
| Bloom strength | 0.55 | 浅泛 |
| Bloom radius | 0.35 |  |
| Bloom threshold | 0.15 | 只让亮核泛 |


### G-15 · 软相似边是视觉噪声的主犯
渊图 609 条边里 415 条 (68%) 是 `semantically_similar_to` / `relates_to`，它们是上下文背景而非真关系。第一版给所有边同 alpha 0.12，全屏看就是"线和星差不多多"，杂乱。
**修复**：两级 alpha——软相似边 0.05（背景雾），硬关系边 0.12（结构骨架）；同步在 `edgeBaseAlphas` 数组里记录每条边的原始 alpha，焦点退出时按边类型恢复而非粗暴重置。

---

## "买椅子配地毯" 周边 UI 升级沉淀

### G-16 · UI 元素也要跟主体匹配
星点视觉过了高水准后，周围的 logo / KPI / 卡片 / 按钮全部"配不上"了。一次把 7 处全升级：logo 真发光星（后改为 3 星轨道）/ KPI 数字下加发丝下划线 + 列间圆点分隔 / 类型过滤 hover 脉动 + 活动行 inset 高光 / 全景看点卡内容大增（行业 bar + Top 3 hub + 超图 chips + 4 屏轮播）/ 焦点卡上下游加关系类型 pill + 本体 type chip / Tooltip 玻璃化 / 操作提示由 5 个 kbd chips（后删除）

### G-17 · "关系"在节点和边的语义切换
焦点卡的上下游列表原本只显示"节点名"。Doctor 反馈："看不清和上下游的关系类型"。修复：每条目末尾加 22 种 relation 的中文 pill（驱动/依赖/供应/采购自/制造/竞争/替代/约束/受益于/演进至/使能/相似/相关/需要/监管/产出 等）；focusOnIdx 函数的 incoming/outgoing 数组结构从 `[idx]` 改为 `[{idx, rel}]`，渲染层据此呈现。

### G-18 · 玻璃卡也要"浮起来"
之前焦点卡用通用 `.panel` 样式贴在右边框。Doctor 要"透明玻璃板材质"。修复：
- right: 32 → 44px（离右边框）
- 加 4 层玻璃叠加（顶光 radial + 顶光唇 inset 1px + 底光唇 + 0.5px 内描边）
- **外阴影 0 4px 24px rgba(0,0,0,.45)** 让卡片从星空中浮起
- border-radius 10 → 14px

### G-19 · 视觉重心配平靠相机偏移
右侧焦点卡占 ~340px，左侧 filter 占 ~230px，差出 110px → 整体右倾。修复：相机 + OrbitControls target 一起向右偏 6 世界单位（屏幕上 stars 整体左移 ~75px）；底部胶囊 `left: 50%` → `calc(50% - 35px)` 跟着左移。这个改法的妙处是 autoRotate 仍然以新 target 为中心旋转，不会破坏交互。

### G-20 · 三层字体系统：印刷 × 读数 × 控件
借 kami 的 TsangerJinKai02 仓耳今楷做主 serif，配 jsdelivr CDN 的 JetBrains Mono。三层语义：
- **Serif（仓耳今楷）**：logo h1 / 焦点节点 h2 / Top hub 节点名 / 上下游链路节点名 / 全景大数字 / 分类组名 / 按钮 / 搜索框 — 概念有文学厚度
- **Mono（JetBrains Mono）**：所有数值（KPI / stats / magnitude / count）— 望远镜读数感
- **Sans（PingFang）**：副标 small caps / breadcrumb / 关系 pill — 现代锚点对比

Doctor 不商业分享 → serif fallback 链精简为 `"TsangerJinKai02", serif`，去掉所有 Source Han / Songti / Charter 防御性 fallback。

---

## 数据现实 + 操作铁律（2026-06-22 焦点卡改版沉淀）

### G-21 · 渊图 starscape 节点字段现实：只有信号/时效有料，89% 节点是"裸节点"
做焦点卡改版时审计 yuantu v3-full 的 2145 个节点字段，发现可用的增量信息极少：
- `signal_categories`：仅 **99/2145 ≈ 11%** 节点非空（persistent_imbalance 55 / supply_shock 54 / demand_surge 38）
- `temporal_*`（status/window/expiry）：**226 ≈ 11%**（active 222 + ever 4；其中 90 个与信号节点重叠）
- `project` / `source` / `status` / `tags`：**全 0/2145 空**——焦点卡底部「额外」区（项目/状态）+ tagChips 对 yuantu **从不渲染**
- **89%（1910 个）节点既无信号也无时效**，只剩 id/name/type/breadcrumb/magnitude/depth/position

**影响**：任何想在卡片/feature 里展示"节点详情"的设计，对绝大多数节点都没料可填。想让普通节点也有"其他重要信息"，**必须改数据层**——`yuantu_to_starscape.py` 从 canonical 图谱多带字段（节点描述/产业环节/信号证据/股票代码），再重渲染。这是数据层限制，不是渲染层能补的。
**当前对策**：焦点卡「供需情况」区只在有 signal/temporal 时显示，无则自动收起（v3.15）。

### G-22 · 星空可视化改动须三处载体同步——它们是独立拷贝，改一处不自动同步
一次星空渲染产物的逻辑改动，涉及三份**互不联动**的文件：
1. 模板 `Projects/星空/prototypes/starscape-template.html`（源头，今后所有重渲染都带）
2. 当前产物 `Projects/星空/render-archive/yuantu-starry-skies-v3-full.html`（render-archive 里的成品）
3. Cowork artifact `Artifacts/yuantu-starry-skies/index.html`（**独立拷贝**，Doctor 浏览器实际打开的那个；改完须 `update_artifact` 落盘才生效）

**坑**：只改模板不会更新已有产物和 artifact；只改 artifact 下次重渲染会被模板覆盖回退。三者相关代码段当前完全一致，同一套 patch 可按锚点字符串统一套用。**改星空交互/卡片逻辑，默认三处同步**（除非 Doctor 明确只要其一验证）。

**⚠️ 追记（2026-10-19 · CC 实测 · 已知风险）**：G-22 的「三者相关代码段当前完全一致」**已不成立**——本轮改动前逐字节对拍：inlined 发布源 app JS 48,790 B vs 模板 app JS 50,766 B，首个差异在 focusOnIdx 尾部。**根因**＝模板此后吸收的 08-13 折叠坞迭代（`info.classList.add('expanded')`＋`syncDock()`、exitFocus 的 `remove('expanded')`＋`scrollTop=0`、Init 的 mouseleave 回卷与 dock 状态机）**从未同步进 inlined/artifact**；CSS 层同病——artifact 字体声明停在 G-20 仓耳今楷版（且 JetBrains Mono @font-face 指向 jsdelivr、被面板 CSP 挡、实际无效），模板早已是思源宋体链（2026-10-19 Doctor 令「默认字体用思源宋体」后三处已同步）。**本轮处置**＝逐串实读目标文件实际文本后做手术式 patch（默认全不点亮 / 「全部」二次点击取消全选 / 字体思源链三件），**未把模板独有迭代灌进 artifact**（扩权禁止）。**影响面**＝按旧口径「同一套 patch 三处统一套用」改星空会误灌或漏改。**建议修法**：① 三载体是否对齐（artifact 补折叠坞迭代 vs 模板回退）归 Doctor 裁；② 改前逐串实读目标文件文本，禁按「模板≈产物」假定构造 patch；③ 「完全一致」断言由盘上对拍脚本（模板 app 段 vs 产物 app 段逐字节 diff）取代。**来源**：2026-10-19 星空默认全不点亮与字体场（闸1 实测失败证据）。

**🔴 订正（2026-10-19 夜 · CC 当场订正 · 状态 ✅ 已修复 · 2026-10-20 Doctor 目验落签）**：原追记有两处**定性错误**，据实订正如下。①「折叠坞从未同步进 inlined/**artifact**」——错。**store 谱系（artifact）一直含全部迭代**：08-13/14 折叠坞五轮、08-10 UI 隐藏，Doctor 当时逐轮签收的载体正是 artifact；10-10 场也是「从 store 拷出→手术→推回」（updatedAt 10-10T09:49Z）。缺折叠坞/UI 隐藏的只有 **render-archive 的 inlined 文件**——它是**旧谱系**（数据=2026-05-17 版 2466/3508），与 store 谱系（数据=2026-08-10 版 3108/4295）**根本不是同一文件族**。②「artifact 字体停在仓耳版」——错。store 谱系 10-10 时已是思源宋体链；仓耳版只存在于旧谱系。**事故经过**：10-19 上午 CC 未先取 store 实况对拍，误以 render-archive 旧谱系 inlined 为「当前发布源」手术并 update_artifact，**把 store 覆盖回 05-17 数据 + 无 UI 迭代版本**（丢 642 节点/787 边/两套交互）。Doctor 追问「版本没有回退吧」后当晚定位修复：以 10-10 store 实况备份（`临时文件/yuantu-starry-skies_artifact_2026-10-10.html.bak`，含包装块）为基线——剥 cowork-artifact-meta → 重放 10-10 信号默认不亮 4 处（三按钮去 active＋layer.visible=false）→ 叠加今日 10 处交互（默认全不点亮/全部 toggle）→ **17 项闸全过 + 逆向逐字节验证**（最终文件 = store 基线 + 10-10 四处 + 今日 10 处，零其他改动）→ 重新 update_artifact；render-archive inlined 同步覆盖为正确谱系。**预防门禁（本次教训）**：① 改星空 artifact 前**必须先从 store 取实况对拍**（更新源判定＝store 文件现盘 sha/数据段节点数/锚点矩阵，不得以 render-archive 任一文件假定为 store 现状——两个谱系并存且无联动）；② 手术基线选定后，先做「基线 vs store 实况」指纹比对（节点数/edges/subtitle/锚点计数），不等再动手；③ 若 store 实况拷贝不可得（store 沙箱不可读、超长行），从 `临时文件/` 的最近 artifact 备份或请 Doctor 终端 cp。**待验**：渲染级目验归 Doctor。**✅ 2026-10-20 Doctor 目验落签**：「目验通过，不卡」——6013 星点/7708 边渲染流畅；默认全不点亮、「全部」二次点击取消全选、折叠坞、UI 隐藏全部在位。（数据口径以刷新后 6013/7708 @ 2026-10-19 为准，早前注记所写 3108 系刷新前口径。）


## [ERR-20260705-001] 主星 shader 用 gl_VertexID → WebGL1 环境全黑
**状态**: ✅ 已解决
**优先级**: 🔴 高
**触发场景**: 更新渊图星空数据后 artifact 和双击 HTML 全黑（连主星都不渲染）。数据/语法/CDN/相机/坐标全查过没问题，误判方向多轮。
**错误信息**: 无 JS 报错表象（需 F12 console 才见 shader compile error）；`starMat` 顶点着色器含 `float pseudoRand = fract(sin(float(gl_VertexID) * 12.9898) * ...)`。`gl_VertexID` 是 **WebGL2 / GLSL ES 3.00 才有的内置变量**，Three.js r128 默认走 WebGL1（GLSL 1.00）→ 主星 shader 编译失败 → 主星几何体不渲染 → 全黑。同款问题在 searchHalo(758) 和 signalLayer(942) shader。
**为何时黑时不黑**: 取决于运行环境给 r128 的是 WebGL1 还是 WebGL2 context（浏览器/artifact 面板不同）；signalLayer 那处还叠加"仅当有 signal_categories 节点(n>0)才编译"，故空信号数据不触发、有信号数据触发——极易误判成"数据问题"。
**解决方案**: 三处 `gl_VertexID` 全换成 position 派生随机（WebGL1 兼容、每颗星位置固定→随机相位稳定、视觉等价）：
  `fract(sin(dot(position.xy, vec2(12.9898, 78.233))) * 43758.5453)`
**预防措施**: ① 星空模板 shader **禁用任何 WebGL2-only 内置**（gl_VertexID/gl_InstanceID/textureLod 等），除非显式 `new WebGLRenderer({...})` 强制 WebGL2 且验证目标环境支持。② 黑屏排查**第一步永远是让 Doctor 开 F12 console 读 shader/JS 报错**，别先盲猜数据——本次盲查十余轮才定位，console 一眼即见。

## [ERR-20260705-002] artifact 面板 CSP 挡外部 Three.js CDN → 面板黑（文件却正常）
**状态**: ✅ 已解决
**优先级**: 🟡 中
**触发场景**: 星空 HTML 双击文件能渲染，但推进 cowork artifact 面板后全黑。
**错误信息**: 面板 console 会报 CSP 拦截外部脚本；`THREE is not defined`。cowork artifact 面板 CSP **只放行 Chart.js / Grid.js / Mermaid（cdn.jsdelivr.net 指定版本）**，星空依赖的 Three.js r128（cloudflare）+ 7 个 examples/js 模块（jsdelivr）全被挡 → THREE 未定义 → 场景不建 → 黑。与 gl_VertexID(ERR-001) 是**两个独立黑屏**。
**解决方案**: 把外部依赖**全内联**进 HTML：`npm install three@0.128.0`（整包 ~30MB，首次可能超时、重试即可，本次 3s 完成）→ 读 `build/three.min.js` + `examples/js/{controls/OrbitControls, postprocessing/EffectComposer,RenderPass,ShaderPass,UnrealBloomPass, shaders/CopyShader,LuminosityHighPassShader}` → 逐个把 `<script src>` 换成 `<script>{内容}</script>`（内容里 `</script>`→`<\/script>` 转义）→ 得 2.44MB 自包含 HTML。星空维护两份：CDN 版（双击文件用，小）+ 内联版（喂 artifact，自包含）。
**预防措施**: ① 凡要喂 cowork artifact 面板的 WebGL/Three.js 页面，**必须内联所有非白名单库**（面板只放行 Chart/Grid/Mermaid）。② 内联版单独出文件，别覆盖 CDN 版。③ 若内联后面板仍黑 → 面板可能压根不支持 WebGL，退回"当文件用"。

## [NOTE-20261020-001] 内联替换切片偏移 8 字符 → 主脚本开标签被切成 `t>`（接缝 bug）
**状态**: 🔄 已修待验（本场实修 · 修复证据＝发布源主脚本与模板逐字节一致 63114B · node --check 过 · 独立审查员复核 diff=0；验收归 Doctor 或指定方）
**优先级**: 🟡 中（接缝类手术通用）
**触发场景**: 把模板渲染产物（CDN 版）内联化时：`new[cdn_end+len("<script>"):]` 从 CDN 段结束位置直接跳 8 字符——但 cdn_end 落在 CDN 行尾 `</script>` 之后，其后是 `\n\n<script>`，跳掉的是 `\n\n<scrip`，残留 `t>` 成为主脚本正文开头 → 全页 JS 语法错误（node --check 报 Unexpected token 'const'）。**HTML 标签仍 10/10 平衡、浏览器不报结构错，极易漏检**。
**根因**: 切片基准点与目标字符串错位——拿「CDN 段结束位置」当「主脚本开标签位置」。
**修法**: 先 `find("<script>", cdn_end)` 定位真实开标签，再 `new[m+len("<script>")+1:]`（连同换行）切片；替换后必跑「主脚本 node --check + 与模板逐字节 diff」两道闸。
**预防措施**: ① 接缝类手术（字符串切片拼接）落盘后必须 node --check 提取出的主脚本 + 与源模板逐字节 diff，两道全过才算完成；② 切片偏移一律先 find 锚点再算，禁止用上一段的 end 位置推算下一段的 start。
**来源**: 2026-10-20 渊图星空 NE 场（本场实踩实修 · 独立审查员复核背书）

## [NOTE-20261021-002] GLSL varying 声明必须在 main() 外——模板拼接 shader 的隐雷
**状态**: ✅ 已解决（本场实修 · 修复证据＝发布源主脚本与模板逐字节一致 · node --check 过 · 目验多轮无 shader 报错；2026-10-21 凌晨场）
**优先级**: 🟡 中（shader 模板拼接类通用）
**触发场景**: nova 星芒片段里写 `varying float vSeed;` 声明——该片段经 `${SHAPE_SHADERS.nova}` 插值进 fragment 模板的 `void main() { ... }` 体内。GLSL 的 varying 声明不允许出现在函数体内 → 语法错（artifact 面板黑/星层不渲染，且 console 才有报错）。
**根因**: 模板拼接的片段内容「看起来像独立 shader 文件」，实际插入点可能在 main 体内——声明语句与执行语句的合法位置不同。
**修法**: varying 声明一律放 fragment 模板头部（`void main()` 之前），片段内只写执行语句。
**预防措施**: ① shader 片段拼接后，逐片段核对「声明类语句（varying/uniform/attribute/函数定义）是否落在 main 外」；② 每轮渲染链必跑「主脚本 node --check」（JS 层）+ 目验（GLSL 层无 console 报错）。
**来源**: 2026-10-20/21 渊图星空 NE 场（本场实踩实修 · 十调前引入、当场修）

## [NOTE-20261101-001] 星位漂移根因——「位置复用」靠重跑复现不可达，基线已重置
**状态**: ⚠️ 已知风险（2026-11-01 Doctor 裁「接受现状」+「不需要星位固定，只要逻辑合理即可」：seed 42 全图重排版为新基线；**星位稳定不是需求，锚定方案弃置**）
**优先级**: 🟡 中（刷新管线通用）
**触发场景**: 2026-11-01 星空数据回补（canonical 10-26 帕米尔批 +83 节点）重跑布局，老节点星位全图重排（与 store 差 mean 256）。
**硬证据**: ① git 考古：星空仓 initial（09-28）/10-19/HEAD 三版脚本布局段逐字相同（seed 42、uniform(-100,100)、力参数）——**seed 从未变**；② 用 store 数据段顺序重放：位置差 mean 256；③ 用 canonical 10-19 版（行业研究仓 c1e5052b blob）重放：骤降至 16.41；④ 残余 16.41 来源＝刷新管线实际用 **--iters 100**（记忆有载「6000 点防欠收敛」「Mac 2min12s」），重放误用默认 80；100 轮在沙箱超 178s 宿主上限跑不动（当初在 Mac 原生跑）。
**根因**: 力导向布局对「节点数组顺序」极度敏感——seed 42 的 uniform 初始位置按数组顺序分配，canonical 每次入图/合并手术都会改写节点顺序 ⇒ 同 seed 同参数、顺序一变即收敛到完全不同的位形。10-20 场「位置复用」成立的前提是数据「逐位全等」（id 序列 0 差异），属条件巧合，**不是机制**。
**影响面**: 每次数据刷新若重跑布局，星图形态全变（老节点 98.6% 漂移 >50）；「seed 42 确定性」只保证同输入同输出，不保证不同输入下老节点位置稳定。
**建议修法（已被裁否，备选）**: canonical_to_starscape.py 加 `--anchor <json>`（{id: [x,y,z]}）：老节点坐标锁定不动、新节点自由布局——显式锚定而非重跑复现。
**预防门禁**: ① 刷新前先明确「本次数据是否允许星位变化」——允许则全量重跑（记录新基线）；不允许则必须走锚定（老坐标显式传入），禁止假定重跑能复现旧星位；② 重放/对拍布局必核对 iters 参数（100 非 80）；③ 沙箱 100 轮超时 → 布局类重跑走 Mac 原生或改锚定。
**来源**: 2026-11-01 星空数据回补场（CC 实跑重放三组对拍 · Doctor 目验报「seed 不是 42」触发考古 · Doctor 裁接受现状）
