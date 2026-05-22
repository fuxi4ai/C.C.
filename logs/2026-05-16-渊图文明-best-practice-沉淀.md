---
title: 会话日志 2026-05-16 — 渊图 + 文明 best practice 沉淀
tags: [log, 星空, PEC, best-practice, 闪耀星感, spiral-galaxy]
created: 2026-05-16
updated: 2026-05-16
status: active
type: log
project: 星空
---

# 会话日志 — 2026-05-16（续）

**项目**：星空 ↔ PEC
**主题**：把今天的两份成品（渊图 dense 范本 + 文明 sparse 范本）固化为 best_practice
**接续**：本日上半场 [[2026-05-16-政经星云-从球面到地图]]

---

## 完成的工作

### 一、配色第三轮 · v3.0 闪耀星感
- 参考渊图 5 行业色板 (#4FC3F7 / #76E0A8 / #FFC857 / #E879C8 / #D6DEE8) 的 HSL L≈65 + S≈70 "星亮带"
- 把 政经 9 文明色全提到同一亮度档：
  - 中华 朱砂深 #B23B36 → **#F26345 闪耀朱砂**
  - 伊斯兰 苔绿 #4A8F6C → **#76E0A8 翡翠绿（直接借渊图嫩绿，两项目色板呼应）**
  - 大和-日本 #E5A4C2 → **#F09BC6 闪耀樱粉**
  - 印度 #DC8A45 → **#FFA94D 闪耀藏红**
  - 斯拉夫 #C1A45E → **#FFCD5A 闪耀蜜金**
  - 欧洲 #7C6CBC → **#A89BEC 闪耀薰衣紫**
  - 犹太 #5288B5 → **#5DBDF0 晶蓝**
  - 盎撒-英国 #8B3743 → **#D04B5C 闪耀酒红**
  - 盎撒-美国 #4F71A8 → **#7AA0E8 闪耀靛蓝**
  - 现代病 #C95440 → **#FF7A6E 闪耀珊瑚红**

### 二、C 演化为旋臂星系（不再是垂直时间柱）
- 替换 layout_C_geographic：9 文明按地理方位作 9 条旋臂（东 0° / 东北 -40° / 北 -80° / ...）
- 旋臂内：千年级近核 / 当代级远端（时间作径向距离）
- 框架核 8 F-XX 内圈 + 子项就近卫星
- 现代病作"游星"悬于受影响文明的中段臂上方

### 三、索引归一化解决"文明缺千年级"问题
- 发现：european / jewish / indian / islamic 没有千年级节点，最古才数百年级 → 自然远离核
- 改用每条臂内 index-based t（不是 time-absolute t）→ 每条臂统一从 R_INNER 贴核到 R_OUTER 远端

### 四、跳掉 force_settle 实现真整体性
- 力学层的 inter-civ repulsion 把臂根从核心推开
- 直接跳过 force settle，纯锚定 + Gaussian 散射
- 核 R 1-18、臂 r_min 5-22，**多个臂内端钻进核内**（chinese 7 / japanese 5 / islamic 13）
- 平均核-臂间隙：-3（接气）

### 五、银河盘扁平化
- DISC_Y 12 → 4（Y 厚度大压缩）
- R_OUTER 145 → 175（XZ 直径扩张）
- 加 Y_FLATTEN=0.18 强制压扁
- 扁平比 Y/XZ：0.51 → **0.09**（薄盘）

### 六、星辉/星晕扩散 + 主要关系加粗
- sparse profile：size `11+m·16` → **`13+m·19`** · bloom 0.95 → **1.15**
- 新增 `STRONG_TYPES`（cross_civ_analog / applies / dual / reinforces）alpha 0.22（默认 0.12）
- 56 条"主要关系"边视觉加粗：8 跨文明对照 + 8 框架应用 + 12 对偶 + 28 强化

### 七、框架核拉开避免糊
- 核心环 R 9 → 14
- Framework 节点散射 sigma 5 → 8
- 核 XZ 范围从 1-18 → **1-24**，54 节点散开成清晰小星团

### 八、分类栏 UI 收尾
- 先误判做了拖动 → Doctor 纠正
- 改成定高 max-height 360px + overflow-y auto（短栏 + 滚动条）
- 不论窗口高度，filter 都是 360px 紧凑栏，不再侵占顶部标题

### 九、归档 + best_practice
- outputs/ 留两份生产文件：`yuantu-starry-skies-v1.html` + `integrated-C.html`
- outputs/archive/ 收 8 份历史版本
- **建 `best_practice/` 文件夹**：
  - `渊图.html`（dense 范本 · 高密度行业图谱）
  - `文明.html`（sparse 范本 · 多 type 整合图谱）
  - `README.md`（关键参数 + 切换 dense/sparse 指引 + 未来项目复制流程）

---

## 做出的决策

| 决策 | 原因 | 影响 |
|---|---|---|
| 配色第三轮统一到"闪耀星感" | 退火气 v2.1 把饱和压太低，星点暗；要找回 渊图的"宇宙感" | 10 色全部 L≈70 + S≈70，bloom 后辉光自然 |
| 伊斯兰直接借渊图嫩绿 #76E0A8 | 两个项目色板视觉呼应，将来同窗能感觉是"一家" | 跨项目色彩语言一致性 |
| C 旋臂星系取代时间柱 | Doctor 看完时间柱觉得不够整体感 | 9 文明的旋臂叙事 = 知识从核辐射出去 |
| 索引归一化 vs 绝对时间 | 缺千年级文明（欧洲）会被甩到外圈断了完整性 | 损失绝对时间对齐，换"每文明都有完整故事弧" |
| 跳掉 force settle | 力学的 inter-rep 把臂根推离核 | 纯锚定布局，几何确定但缺自然涨缩—配合 _gauss 散射弥补 |
| Y_FLATTEN 0.18 强制压扁 | force layout 后 Y 又被推散到 ±90，需要强制收 | 银河盘形态确定，俯视清晰 |
| sparse profile 单独加亮 | 364 节点稀疏，与 渊图 170 高密度需要不同视觉档 | 数据集只需在 meta 标 brightness_profile = "sparse" 即可 |
| STRONG_TYPES alpha 0.22 加粗 | 项目最贵的学术关系（跨文明对照、对偶）应该显著 | 不加粗就被一般边淹没；加粗后这些关系视觉跳出 |
| 分类栏定高 360px | 13 个分类自然 470px 会挡标题 | 永远 360px 紧凑栏 + 滚动条 |
| best_practice 文件夹固化两份范本 | 之前散在 outputs/，迭代多次容易丢成品 | 渊图 dense + 文明 sparse 作为永久参考，README 给参数清单 |

---

## 遗留问题 / 待办

### 数据可视化扩展
- [ ] 整合数据集还有 4 个子集没单独可视化：framework_tree 单独成图 / cross_civ_network 焦点版 / modern_diseases 三联画 / historical_timeline 时间轴版
- [ ] friendly 版（dual-layer label）切换功能：让用户切换学术术语 ↔ 大众友好用语
- [ ] 28 条 cross_references 现在用了一部分，gene_to_event 等还可深化

### 视觉细节
- [ ] 文明 hub 节点 hover 时其旋臂高亮，其他暗下去
- [ ] 跨文明对照边 hover 高亮其连接的两个文明
- [ ] 时间维度作为第二视图模式（toggle "旋臂式" ↔ "时间柱式"）

### 技术债
- [ ] integrated_to_starscape.py 已 750+ 行，layout 函数应该拆出 layouts.py
- [ ] template 1100+ 行，CSS/JS 分块
- [ ] 4 个 layout（A/B/C/D）共用代码可以抽公共

### 兜底
- [ ] best_practice/README.md 可考虑作 brain 永久笔记（pull 到 brain/permanent/）

---

## 相关笔记

- [[星空 best_practice 范本]] · `Projects/星空/best_practice/`
- [[2026-05-16-政经星云-从球面到地图]] · 本日上半场
- [[2026-05-15-星空-v1.1-周边UI升级]] · v1.1 七处升级
- [[2026-05-15-星空-P0-P2-Starry-Skies-从无到有]] · P0-P2 起点
- [[PEC 系统概览]] · v2.20
- [[星空 PRD]]
- [[星空 GOTCHAS]]
- [[文明基因星云 数据 v2.0]] · Doctor 金标准
- [[PEC 可视化整合数据集 v1.0]] · 6 子集整合
