---
title: 会话日志 2026-05-15 — 星空 P0→P2 · Starry Skies 从无到有
tags: [log, 星空, Starry Skies, design-project, three-js, knowledge-graph]
created: 2026-05-15
updated: 2026-05-15
status: active
type: log
project: 星空
---

# 会话日志 — 2026-05-15

**项目**：星空（Starry Skies）— 新建设计项目
**主题**：从晨鹊声开新设计项目，到 P0 设计冻结 + P1 brain 原型 + P2 渊图工业级压测全部跨过
**时长**：单日长 session

---

## 完成的工作

### 一、新建设计项目 · 星空
- `Projects/星空/` 文件夹建立，定位：**通用概念-关系数据库星河化引擎**
- 参考资料就位：IMG_2523/2524.PNG（知识星河参考图）· 23.jpg（arkclaw 2D 对照）· 渊图 tarball
- 写 `reference/REF-001-知识星河-design-language.md`（14KB · 视觉语言完整规范）

### 二、PRD v0.1 → v0.2
- 写 `PRD.md` v0.1（245 行 · 10 节 · 数据契约 + 染色策略 + MVP 切片 + 8 开放问题）
- 渲染 PRD 为 viewable 视图（visualize widget · 可点击答 Q 的按钮卡片）
- Doctor 撕 Q1（英文名 Starry Skies · 致敬拜伦）+ Q8（分层 anchor）
- Doctor 整理 §0 决策记录拆为「Doctor 已定 6 条」 + 「CC 推荐默认 7 条」两表
- PRD 升 v0.2，含决策记录、4 桶染色（concept/entity/phenomenon/synthesis/default）、硬约束 vs 弹性、MVP 四阶段

### 三、brain-anchors 全局轻量化改造（顺带做的）
- 加载强度分两档：轻量 stub vs 重型
- Doctor 分类：轻量 4（DVA · 龙鱼五力 · 光通信 · 星空）/ 重型 7（自检 · 天工开物 · 渊图 · 海螺姑娘 · PEC · 司南 · O MY HTML）
- 新建 `brain/星空/星空.md` stub（35 行）
- 改 `brain/.skills/brain-anchors/SKILL.md` 表格 + 行为规则段

### 四、P1 · brain vault 小而美原型 ✓
- 写 `tools/brain_to_starscape.py`（313 行 · 适配器：解 frontmatter + wikilinks + 3D force layout）
- 修 cycle-aware BFS depth 算法
- 写 `prototypes/starscape-template.html` 视觉模板（604 → 938 行 · 含 Three.js r128 + Bloom + UI 浮层 + 焦点交互）
- 写 `tools/render.py`（40 行 · 模板注入）
- 产出 `brain-starry-skies-v1.html` · 68 节点 / 120 边

### 五、视觉语言迭代 5 轮（与 Doctor 边看边调）
1. v1 → 光球感重 → v2 收核扩晕
2. v2 氲过 → v3 接 UnrealBloomPass（镜头泛光）但仍过
3. v3 → v4 对比知识星河参考：sharp shader + light bloom
4. 玻璃按钮：纯色 → 玻璃透明 → 曲线渐变 + 4 层叠加（顶光唇 / 椭圆高光 / 暗腰 / 底光）
5. 按键化：胶囊托盘 + 独立圆角键 + 外浮阴影 + 按压回弹

### 六、P2 · 渊图工业级压测 ✓
- 写 `tools/yuantu_to_starscape.py`（342 行 · graphify-output 适配 + 渊图行业分类器）
- 12 工业类型 → 4 语义桶 → 后改为 5 行业（光通信 / AI算力 / 半导体封装 / 材料能源 / 其他）
- 15 relation 类型 → 4 类流光（蓝青因果 / 嫩绿供应链 / 琥珀张力 / 品紫受益）
- 5 hyperedges 作 chips 显示在节点详情卡

### 七、P2 视觉再迭代
- 等距 layout → 4 杠杆破解（边权重 · 同社区斥力 ×0.30 · 跨社区边 ×0.05 · hub 阻尼）
- 9 算法社区聚类 → 改为 5 行业聚类（避免色相杂乱）
- 调参 4 轮：community_pull 0.42→0.90 / inter_strength 280→100 / 比例 0.73→1.55
- 直线边 → quadratic Bezier 曲线（12 段）
- 曲线方向：纯外凸（球壳感）→ 35% 外凸 + 65% 随机
- 流光速度减半（drives 0.42→0.20）
- 软相似边分级：0.12 → 0.05（68% 软边变背景雾）
- 控制点作为 shader attribute · 流光也走 Bezier 轨迹

### 八、收尾
- P1 + P2 各产出冻结快照（`*-v1-frozen.html`）
- 写 `GOTCHAS.md` · 111 行 · 15 条调试沉淀 + 参数 cheat sheet 17 行
- PRD §7 P1 + P2 标记 ✓
- brain stub `星空.md` 进度同步更新

---

## 做出的决策

| 决策 | 原因 | 影响 |
|------|------|------|
| 英文名 **Starry Skies** | 致敬拜伦 *She Walks in Beauty* "Of cloudless climes and starry skies" | dark and bright 在节点光与真黑底间相遇——视觉哲学注脚 |
| 项目本质：**视觉模板 + 数据契约**组合 | 故意放弃通用性以换取一种视觉语言的极致 | 任何"概念-关系"数据库可零代码改动喂入 |
| MVP 路径 P1 → P2 = brain → 渊图 | Doctor 选：小快验视觉 → 工业级压测 | 视觉语言跨领域复用通过 |
| 单文件 HTML 模板（不做 npm/pip 包） | 匹配 Doctor O MY HTML 工作流 | 双击即开、邮件可发、Notion 可嵌 |
| brain-anchors 分层加载（star + 龙鱼五力 + DVA + 光通信 轻量） | 不污染所有对话上下文 | 轻量 anchor 在 brain-vault 通用模式落定 |
| 渊图行业分类用 keyword + hyperedge | 算法社区是产业×切面混合，染色杂乱 | 5 行业语义桶清晰可辨 |
| Force layout 按行业聚类（不按算法社区） | Doctor 视觉验证：行业色块需聚成 5 团 | 比例从 0.73 升到 1.55 |
| 软相似边 alpha 减半至 0.05 | 415/609 是软边，与硬关系视觉冲突 | 画面从"接线图"清爽为"骨架星河" |
| 曲线边代替直线 + 弯曲方向随机化 | 直线感像数据中心，纯外凸像球壳 | 星轨、引力轨道的"宇宙感" |
| 关系类型 → 流光颜色 + 速度 | 把 17 种 relation 表达为视觉信号 | 网络拓扑变成"流动的血脉" |
| **"关系"作为节点桶是语义错误** | 关系本应是边，节点应是名词 | bucket 重命名为 synthesis 综合 |

---

## 遗留问题 / 待办

### P3 待办（不急）
- [ ] 写 `Projects/星空/README.md` 给外部使用者
- [ ] 在 brain-anchors 注册「星空」深读触发条件
- [ ] 把 brain 适配器也加上 v2 layout（cross-cluster edge dampening · hub damping）—— 顺手就能让 brain 星河也享受 P2 的 visual upgrade
- [ ] PRD `meta.title / kpis / coloring / type_palette / terms / locale` 参数化测试（验证消费者覆盖）

### 已知问题
- [ ] 渊图 P2 中"光通信"行业 span 仍偏大（106）—— hub 节点跨行业连接多
- [ ] 35 个未解析 wikilinks（brain 适配器的"项目名 + 空格 + 文件名"风格未覆盖）—— 影响轻微，但 P3 适配器要修

### 进阶（不在 MVP 内）
- [ ] 移动端适配（先桌面）
- [ ] 用户上传 JSON 的 SaaS 入口
- [ ] 边类型差异化更精细（虚线/点状线 visual 渲染）

---

## 相关笔记

- [[星空 stub]] · `brain/星空/星空.md`
- [[REF-001 知识星河设计语言]] · `Projects/星空/reference/`
- [[Starry Skies PRD v0.2]] · `Projects/星空/PRD.md`
- [[星空 GOTCHAS]] · `Projects/星空/GOTCHAS.md`（15 条调试沉淀）
- [[brain-anchors 加载强度分两档]] · `brain/.skills/brain-anchors/SKILL.md`
- [[O MY HTML 方法论]]（参考：Doctor 单文件 HTML 交付的范式）
- [[渊图引擎 PRD]]（P2 数据源）

