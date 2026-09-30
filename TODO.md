---
title: Brain Vault TODO
tags: [todo]
created: 2026-05-14
updated: 2026-09-30
status: active
type: log
---

# TODO

## 待办

> **〔2026-09-30 问答板裁定批 · 全 20 题取推荐〕** 板件 `临时文件/问答板_2026-09-30-0001.html` · 答案串逐题全 A。**Q1–Q5（修复审计 5 行落签）已当场执行**——`permanent/_repair_audit.md` 现 **17 行全 ✅ · 0 🔄 · 0 破行**。**Q6–Q20 的裁决与派生动作记录如下**（本行为裁定留痕，不是待办条；派生动作以各自条目为准）：
>
> - **Q6 · `D-14` 同族计数口径** → 按「**次数＝同一根因独立复发轮次**」计，**不按受影响文件数**。⇒ 已作为口径定案；下次引用 G-40／G-38 的「第 N 次」时照此。
> - **Q7 · `B-11` 归口** → **归 P3 机制项**，连同「审计剩余未修项对账」一并处理（不单独立条）。
> - **Q8 · `check_dataset_parity.py`** → **暂不升闸，维持只报**（先攒误报率数据）。
> - **Q9 · `build_ir_sample.py:165` 口径分裂** → **归 P3**，按「合并到 QC 单一来源」推进（不就地删检查）。
> - **Q10 · `G-37`** → **签升格**，**并同批订正其正文状态行**（`GOTCHAS.md:1496` 仍写「一条未执行」）。
> - **Q11 · PEC 总纲版本号** → **冻在下一版**：先发一版带 `version` 字段的，再冻（非立即冻当前内容）。
> - **Q12 · EAL 余尾条** → **按档内裁定撤项**（①②④ 一并处理）。**③⑤ 余量另立小条**（见下）——**⚠ 本条解释留痕**：Q12A 字面只覆盖 ①②④，若您的本意是连 ③⑤ 一起撤，请一句话纠正。
> - **Q13 · `brain-todo` 复装** → **现在复装**：走 `.skills/brain-todo.skill`，**不跑 `save_skill`**。**属您终端动作**（命令见报）。
> - **Q14 · 巡检周班** → **(a)(b) 都改**：班加「跑不了脚本时读上次快照并出简报」兜底 ＋ 验收判据承认「人工按班交接原文带参跑」。**改班 prompt 走您终端 SHA 往返**（先出 staging）。
> - **Q15 · 龙鱼 ds 检测挂班** → **挂进周更班**。**改班 SKILL 走您终端 SHA 往返。**
> - **Q16 · EAL T2 池** → **扩 `GDP_SECOND` ＋ OPEC `release_code` 闭集**。属可执行工作项。
> - **Q17 · VV 知会两件** → **两件都知会**（走 `知会VV-*.md` 落库目录）：① X-Board 数据侧 shape 统一；② codex-brain-* skill 分叉。属可执行工作项。
> - **Q18 · 渊图高盛四条尾** → **② 起第六轮复验收口**；③④ 挂观察；① 等 PDF。
> - **Q19 · PEC `专题研究/`** → **保留**（跨案脉络件不属单一案例目录），不并 CS-08。
> - **Q20 · 隔离区两条目录** → **保留**（属可回退留档），不归档不删。

- [ ] **EAL · 余量（③⑤）（2026-09-30 由问答板 Q12A 裁定后另立 · 承原「EAL 余尾批发」条）**：原条经裁 **①②④ 撤项**，余量两项保留跟踪：**③ 2-R 全局传播至 Gateway 版本文件**（`versions/1786977170792.html` 仍 v2.2，**在 store 内 ⇒ 未核**）；**⑤ 生产库读者切换仍待裁**。

> **〔2026-09-30 /todo 现核 · 条目事实性订正批（16 处）〕** 本轮对**待办段全部 66 条**逐条从盘上重取（4 簇并行独立核查，**不采信各条自带的旧注记**），查出「条目正文／自带注记**本身为假**或已漂」者 16 处。**凡涉及下列条目，均以本注为准**；**原条目正文一律未删改**——09-29 13:15 那轮就地改写曾整段删掉原条正文（承 `checkups/2026-09-29_todo落盘_独立复核.md` 的 F-1/F-2 逮出），本批不重蹈。
>
> 1. **〔剑酒青丘遗留仓〕注记为假** — 「`Database/剑酒青丘` 目录**现已不存在**」**不成立**：该目录**在盘**（真实目录、非符号链接，`.git` mtime 09-16 05:40），`find -type f` 排 `.git` 后 5 件。⇒ **原条「`.git/index` 1062 条 vs 盘上 3 件」的前提在原址即成立**，**不需要**「重定位到新址」；待裁项（reconcile／退役／加 `.gitignore` 或指针 stub）仍归您。注记另半段数字核对无误（`Projects/Financial/剑酒青丘` 218 件有 `.git` · `brain/剑酒青丘` 13 件无 `.git`）。
> 2. **〔PEC · CS-02 件 9 处〕不是 PEC 件的真问题** — 那 9 处的引文**逐字在 `历史时间线.md` 同号行**（`:107` 股份公司殖民／`:169` 金本位／`:180` 1902 英日同盟／`:216` 1945 工党／`:218` 苏伊士），`学者谱系.md` 这 5 行归一化后**确为空**。真因＝**件内裸简写 `:NNN`**（同一表既有 `历史时间线.md:130` 又有裸 `:107`）＋工具按「全文前置文件名」**弱归属**到 `学者谱系.md`。修法＝补 `历史时间线.md:` 前缀（单件、可逆）。**⚠ 另**：工具 docstring 自记「实测 CS-02 件 **4 处**」，与现跑 **9 条**不符；本场 `--gate all` 实跑得「已核 162/189 · **FAIL 15 · WARN 39**」。
> 3. **〔`all` 渠道在新体例件上仍无实测样本〕前提已不成立** — 盘上**已有**可跑的折中法/逐字引录版新体例件（CS-02，updated 2026-09-29），本场已实跑（见上条）。工具 `--gate help` 内同句仍在，应随实测定稿。长期观察属性保留。
> 4. **〔PEC · D4 重跑〕计数与路径双漂** — 条写 CS-05 证据层补全件「371 行 / 51983 B」，现读 **431 行 / 61792 B**（09-29 修订后）；条写 `raw/2026-09-26_analysis_文明基因原始提炼方法还原.md`，实件已迁 **`Projects/PEC/文明基因/方法论/`**（存根实在 `PEC/_bak/audit_2026-09-29_stubs/raw/`，**非** `raw/` 之下）。条内「载体名 27 条 · 语料内 13／语料外 14」经核**成立**。
> 5. **〔PEC · 门禁推进〕「亦未做阉割实验」须限定** — `Infrastructure/test_gene_qa.py:13` 明记 **2026-09-27 门禁推进时做过阉割实验**（逐条拆掉 chk 再跑；**当轮只阉 R6/G2/G5**，同 docstring 自陈未阉 G1/G3/G4）、**不是**本条所指的 13 项（渊图继承 8 ＋ PEC 专属 5）⇒ 只可说「这 13 项无任何持久化守卫」。
> 6. **〔X-Board 接管首日遗留〕数字二次漂移** — `ai_status` 空 **2148** 仍准；但现读 `historical_headlines` **7370** 行（注记 7315）、processed **5222**（注记 5167）——09-29 17:39 的刷新在注记取数之后又入 55 行。
> 7. **〔DVA · health 产物新落点〕注记字段归属有误** — 注记「manifest `last_scan 2026-09-29`」实为 **`DVA` 项目项**的 `conch.last_scan`，**`DVA-Database` 项无此字段**；该节点 `freshness.last` 实为 **2026-09-18**。（路径写作 `海螺姑娘/data/…`，实际在 `Projects/海螺姑娘/data/asset_manifest.json`。Mac 侧其余成立。）
> 8. **〔白泽仓既存积压清理〕** — 「同仓同类未跟踪**恰 5 件**」现为 **6 件**（另 5 件已在册，全部 mtime ≤ 08-31，非新落件）。「文件 33,145 B」✓、路径 `_bak/` 漂移 ✓、`.gitignore` 文本层仍命中该件 ✓。
> 9. **〔渊图 · 高盛调研场四条尾〕② 前提已过期、③ 当场可答** — ② 札记现文为**第五轮** PASS_WITH_LIMITS ＋「第六轮复验未执行」，**非**条写的「第四轮 · 修复待复验」；③ `prices/` **无**天数智芯拆股前后价点（仅芯片报价 2 条，node `company_Tianshu`，04-21/04-22 · 元/张）。**⚠ 本子项初版写反、已订正（承 2026-09-30 未参与实施的独立复核逮出）**：原写「**全库无 `_caliber_` 机制**（grep 0 命中）」**不实** —— 该机制**早已实装并挂 QA**（`Database/行业研究/CLAUDE.md:134/139` 定 `{指标}_caliber_{scope}_{时点}` 锚键规范、`rules/check_caliber_conflicts.py` 及其负向测试在场、QA 第 18 项、canonical 命中 4 次、全仓 **512 文件**命中）；**只有 `prices/` 层 0 命中**。⇒ 正确陈述＝「**机制早有，唯 `prices/` 层未采用**」——而这**正是原条真正要问的答案**。①④ 仍开。
> 10. **〔两份 EAL PRD 待验收〕① 计数口径失真** — 星空视觉迭代 PRD §二 实为 **9 ✓ / 0 [?]**（R1–R6/N1–N2/X1）；原注记「§四 18 ✓ / 4 [?]」系**全文件字符计数且误挂 §四**（§四无 checkbox），那 4 个 `[?]` 是 §四/§五**叙述里的字面提及**。② adapter 迁 Mac PRD：`awaiting_acceptance` ✓、§二 **8 条 [?]** ✓。
> 11. **〔DVA GOTCHAS 权威声明〕数字已漂** — Codex 镜像件现 **268,470 B · mtime 2026-09-29 13:29**（注记 267,570 B · 09:59）；最大编号仍 `ERR-20260929-002`、领先 Mac 侧 3 天 ✓；`brain/DVA/GOTCHAS.md:37` 自相矛盾句**仍在**（已列 C 类，见分流报告）。
> 12. **〔基建 · 5 个非 brain-\\* runtime skill〕源指针错 ＋ 现象再现** — 源应为 `logs/2026-09-19-接手渊图会话与skill发布链修复.md:71`，**非**条写的「签字分轨入Settings」篇。**且现象 2026-09-29 23:24:22 再现**：**恰那 5 件**在 **2.1 ms** 窗内被重写（schedule 2399 · setup-claude 3038 · setup-cowork 3069 · consolidate-memory 1983 · explain-usage 1384 B），逐件 frontmatter 单块完好、无损伤；同秒另有 `.auto-memory/MEMORY.md` 与该场 subagent jsonl 落笔 ⇒ **相关指向 harness 侧同步（未能确证，只报相关）**。
> 13. **〔基建 · 探针脚本自身出错四次〕源指针错** — 所引「消费回执未闭集合清账」篇 grep 该内容 **0 命中**；实录在 `permanent/经验库.md:3624`（含「三列表用四列比 ⇒ 27 行误报 26 行并据此向您发警报」）＋ `logs/2026-09-28-文明基因系统收敛与判据层整合.md:114`。事实成立。
> 14. **〔基建 · 5 件更早批次备份从未入册〕源指针错 ＋ 未核** — 同上篇 **0 命中**；实录在 `logs/2026-09-28-文明基因系统收敛与判据层整合.md:113`。所指应是 fuxi `F:\Mac_Backup\INDEX.md` 与 `todo-auto\` 批次；**fuxi ssh 本轮 publickey 被拒（key 不在会话）⇒ 5 件清单未核**。
> 15. **〔基建 · E 路 `Write` 被 harness 拒〕源指针错** — 所引「发声系统切 eleven_v4」篇 **0 命中**；实录在 `logs/2026-09-29-PEC完整审计与审计报告.md:44` ＋ `checkpoints/2026-09-29_PEC完整审计_PRD.md:110`。事实成立、**原因确未查**。
> 16. **〔PEC · 三小件〕③ 计数与盘不符** — `临时文件/` 残留 mp3 现为 **2 个**（`xboard-tts-20260926.mp3` 575,991 B · `xboard-tts-20260928.mp3` 397,941 B），**非**条写的 3 个；两者**均非本场生成**（属他场），未动。
>
> **⚠ 连带发现（供您裁）**：上列 **4 条源指针错（12–15）全部集中在 09-29 那批「漏挂补挂」条目上** —— 建议对该批其余条目的「源：」栏整体回查一次。

- [ ] **skill 发布链 · `brain-todo` 安装副本正文缺 95 字符（2026-09-29 /save 挂 · 源：`logs/2026-09-29-发声系统切eleven_v4.md` ＋ `permanent/已装skill清单.md` 同日补记）**：当日 skill 发布链**全量四端对拍**（7 个 brain-\*）暴露——`brain-todo` 的 **runtime 端 M5 行尾部被截**，缺「**签字分轨**（事实性的签字/验收 → 未参与实施的审核者 subagent 落签；方向性 → 问 Doctor）＋ AskUserQuestion 选项 label 尾部钉（推荐/不推荐）」**整段及其出处栏**（共 95 字符）。实读：canonical `26686 B / 266 行 / sha 16539af4` vs runtime `26515 B / 267 行 / sha d81a8fa8`。**根因**＝`save_skill` 第四跳「LLM 复述长正文」的漂移（26 KB 正文丢字，落在**表格长行**上）。**✅ 可靠修法已备**：仓内三端一致（canonical ＝ portable ＝ 包内）⇒ **包是逐字节正确的** ⇒ 走 `.skills/brain-todo.skill` 由 Doctor 复装即可对齐；**⚠ 别**再跑一次 `save_skill`——那正是制造这类缺口的那条路（风险大于收益）。**待裁**＝现在装还是择时。**同批勿重复处理**：`brain-save` 的 runtime 偏差属**已记录 · 无害 · 刻意不修**（`已装skill清单.md` L40），且本场实核其现象未变。

- [ ] **PEC · P2 收口残余 · 残余归 Doctor 部（2026-09-29 更新）**：**① 接线与 ②③ 三项已勾迁档**（见 `references/TODO-已完成归档.md`）。**仍开口的两条（归您）**：① **是否把 `check_dataset_parity.py` 升为「闸」**（现为构建期**只跑只报不阻断**；升闸＝行为语义变更）；② **`build_ir_sample.py` 与 QA 的口径分裂根治**——两者判据各写各的，根治＝合并到 QC 单一来源，归 P3。

> **⏸ fuxi-station 离线 · 需要 fuxi 的任务一律搁置至 2026-09-26（Doctor 2026-09-22 令）**——不推进、不计失败、不据离线态判错。受影响条目（已逐条加 ⏸ 标记）：DVA 自愈链终验（本段第 1 条，自带 09-26 回线补核清单）· 浪浪 partial 执行面 · DVA health 落点/回流写入者 · 渊图挂账批发②子项（`prices/*.bak_pre_clean_20260608` 待 fuxi 归档，条目未加标记）· X-Board ⑥（老毛/投知接 DVA 采集管线，同上）· DVA first-round 包清理（长期观察段）。回线后各按自带补核清单一次收口。**核过**：沙箱侧 `ping 192.168.1.32` 100% 丢包 + TCP/22 不通（04:42 PDT 实探），与 Doctor 所述一致。
>
> **解除（2026-09-26 03:0x PDT 实探 · CC）**：fuxi-station **已回线**——`ping 192.168.1.32` 2/2 · **0% 丢包** · rtt 4.4–6.4ms；`TCP/22` 返回 banner `SSH-2.0-OpenSSH_for_Windows_10.0 Win32-OpenSSH-GitHub`；`ssh Codex@192.168.1.32` 可登录（hostname `Fuxi-Station` · 北京 2026-09-26 18:11）。**上列五类搁置项自本条起解除搁置**，各按自带补核清单一次收口；DVA 一项已有 ⑦ 现核结果与 Doctor 当日裁决（先认证、再放行写动作）。


- [ ] **PEC · CS-02 件 9 处「引用指向空行」待查（2026-09-27 挂 · 源：同上）**：引文闸的反向包含 `sn[:30] in qn` 在**被引行是空行**时 `"" in 任意串` **恒真** ⇒ 这类引用**此前一律被静默放行**；修工具后**照出真案 9 处**（`raw/2026-09-26_analysis_CS02证据层补全_折中法.md` 引 `学者谱系.md:107/169/218` 等）。**是工具的判据缺陷、已登记工具 docstring；但那 9 处引用本身是不是 PEC 件的真问题，未查**（可能引文定位写错、也可能被引件该有内容而没内容）——**要查归 Doctor 定**。

- [ ] **`all` 渠道在新体例件上仍无实测样本（2026-09-27 挂 · 长期）**：引文闸（`--gate all`）的精度只在**旧体例**三案上量过（假红 67–76%）；新体例件盘上还没有 ⇒ **首个新案跑 `all` 时若红数异常，先取一条原文对拍，再判件错还是闸误**。



- [ ] **PEC · 审计报告修复轮 · 剩余归 Doctor 部（2026-09-29 更新）**：**主体 13 条已勾迁档**（见 `references/TODO-已完成归档.md`「已完成」段首）。**仍开口的只有两块**：① **P3 剩余**——`build_experience_index.py` 改读真源（**试做失败已回滚**，门槛＝干跑核覆盖 ≥37/37 且标题干净才许上线）· 闸「按本载 L2」→「按条载 L2」（`brain-anchors` 三端，**未实施**）· `parity` 扩面 · 导航层刷新触发器 · `provenance` 改锚文本；② **审计报告「剩余未修项」未列名**——须从 `AI4ME/PEC审计报告_2026-09-29.md` 逐条对账（93 条里哪些仍开）。**另**：`G-37` 状态仍 🔄、**升格草案待您签**（`GOTCHAS.md:1407`）。

- [ ] **PEC · D4 重跑（2026-09-26 开跑 · **折中法已裁 · 已解冻** · 源：`logs/2026-09-26-PEC阶段1清空与门禁收口.md` ＋ 本场）**：**本场完整经过**＝三轮复验 FAIL→PASS_WITH_LIMITS→FAIL（根因：晋 v2.2 判据集在「入场后如何计数」一段不足以一致裁决）→ 换尺失败（**「应当」「不可以」全语料 0 命中**）→ 换「载体身份判」小样 → 诊断出**案级语料结构性不足** → **Doctor 转令考古原始提炼方法** → **方法挖出（奠基期 05-09–05-12）** → **Doctor 裁「折中法」并给出全部落点**。**现行改法**：五段模板 ＋ **尺 A**（＝立案版机制链第二环「教育传承」＝B1 首列，**不新造尺**）＋ 「传承机制」段须给「**载体名 ＋ 出处位置**」· 落不到案级语料的挂 `[语料外]` ＋ 补外部权威出处 · **规模回到 5–6 条/文明**（25/88/120 皆换尺产物）。**⇒ 两项前置（术语-证据映射／传承文本语料）已撤销，D4 解冻。** **本场已交付**：`raw/2026-09-26_analysis_文明基因原始提炼方法还原.md`（方法还原＋两裁落点）· `raw/2026-09-26_analysis_CS01证据层补全_折中法样板.md`（**样板件 · 载体名 27 条全补完 · 语料内 13／语料外 14 · 外部核验耗 10 次检索**）· `raw/2026-09-26_analysis_CS05判定重跑.md`（v4 诚实快照）。**⚠ 进九文明前须定的两处硬缺口**：① **「命中位置须支持断言」未写进规格**——`找得到字符串` ≠ `该处支持该断言`（样板件已标 `Yad Vashem`／`Haganah` 两条命中但非支撑位）② **泛指条目**（「学校教育」「文学与电影」）**无具名载体、不可回查**，须单列一类。**同挂**：**D5 件**待落签 · 门禁侧 `丙`/`9(a)`/`9(b)`/`8(c)`/`G-1`~`G-5`/`D3` 待签（`文明基因现状与门禁.md` §B/§D · 2026-09-27 自沿革 §五 外移）· `G-31` 是否升格 · `§六 L301` stale 处置（**已实核确属 stale、已在形成史件标注**，处置方式待裁）。**✅ 已办**：形成史件 **13 处回改**（D6 三处 ＋ 自审 F5／F8 连带 ＋ G3／同义残留／钟摆型三写法）＋ §五整节／§十二 stale 标注 · 一次**自我纠正**留痕（曾误指探针编造「孙诒让」，实核在 `A01` L694）。
  **⇒ 2026-09-26 上午二场（本场）· 两处硬缺口已裁 ＋ 第一案（CS-05 中华）已跑完 ＋ 三轮独立复验闭环**：① **两处硬缺口 Doctor 已裁**——**「命中位置须支持断言」写进硬要求，形态＝逐字引录**（附该处原文逐字 ＋ 一句「为何支撑」，判别者只读那一行即可复核）；**泛指条目单列一类、不带入序列**（对齐 B2 处置）。② **CS-05 证据层补全件已落**：`raw/2026-09-26_analysis_CS05证据层补全_折中法.md`（371 行 / 51983 B）——六项按五段结构 · **逐字引录 61/61 机器核过**（§二 54 ＋ §四 7）· 载体表 21 行／具名载体 26 个 · **语料外 0** · 泛指条目 A1–A7 单列 · B1 落格标记已加到 §三 九行。③ **三轮独立复验（审核者均未参与实施）**：一轮 `PASS_WITH_LIMITS`（11 项）→ 回改 → 二轮 `PASS_WITH_LIMITS`（15 项，主指控＝「机器账目不可复现且自相矛盾」成立）→ 回改 → 三轮窄口径 `PASS_WITH_LIMITS`（**15/15 回改全部到位**；8 处新接缝**无一触及实质主张**）→ 三轮回改收口 + 机器核 61/61。④ **两条方法侧收成**：**载体名「反向抽法」**（先读语料自己怎么讲这些候选，再取载体）把语料外率由 CS-01 的 **50% 压到 0%**；**「逐字引录」这条硬要求必须配一个机器可跑的核验动作**，否则只是把判者自述换个格式——本轮该动作**逮出真错 3 处**（其中 2 处是实施者在回改中**新造**的）。⑤ **✅ 边界问题 1 已裁（Doctor 2026-09-26 · 按形态三分定列）**：**文本型＋制度型 → B1 第 1 列 ✅；物质型 → 第 2 列 ⚠ 登记但不计**。落 `§三.1 载体形态分类与落格`（含推导依据，**后七案照用**）。**两处尖点已标出、未自决**：**尖点一**＝罪己诏（字面是「诏令」正落第 2 列，本件按「被反复援引为问责语汇」判入首列）；**尖点二**＝天人感应／「君王死社稷」叙事／士人自我期许 三者介质为话语·叙事·观念，**不入三型**，本件暂同侧处理、**是否另立第四类归您**。另标**适用边界**：B1 五行字面判**候选**、本件把三分用在**载体**上（下移一层），两种读法在「载体全 ✅ ⇒ 候选 ✅」下同结论，**但若须严格判候选则全件要重挂一层**。
  **⇒ 同场 Doctor 追加两裁（收口 · 后七案照用）**：**(A) 三型统一入首列，判据换轴**——Doctor 原话「**因袭不也是一种主动传承么？重点在传承，不在教育的主动性。**」⇒ **判别器＝`规则二`「被重新选中」，不是「有没有人在教」**；**「物质型→第 2 列」与「制度型须能指出『被教』机制」两条限制一并撤销**，**尖点一（罪己诏）消解**。**连带**：§X.5「基础设施」重新拿到首列载体（大运河·长城·驰道·漕运），不再是「整条可能不达标」。**本件自曝**：首版给传承**偷加了主体要求**、并据此差点新增一格、差点判掉一整条——本场第二处「有判据、无执行动作」同型错。**(B) `读懂中国/` 定位＝P2 降级语料·线索层**：其真身＝**LLM 凭训练数据生成的导读＋节选**（该目录 README 自述「LLM 都懂·直接问就好」「❌ 文本提取/OCR/RAG」），**不是原典抽取**。四条纪律＝① 线索以 `[待核·P2线索]` **单列、不入载体表**；② **核到 P1 才升**；③ 接 **A02 三阶段审议** ＋「无可证伪条件者降为讨论记录」——**不新造链**；④ **禁当覆盖证明**——**实测反例：`崔杼` 在 `读懂中国/` 全层零命中**（它标着《左传》的那册里没有《左传》襄公二十五年的崔杼案）⇒ **覆盖率不可信**。**⚠ 带上成本**：「核到 P1」需联网，单价参照 CS-01（13 条耗 10 次检索），且**沙箱 WebSearch 有会话配额** ⇒ 后七案开工前须先估「线索条数 × 单价」。
  **(C) 「被教」透镜清扫（Doctor 令「按照传承的新原则走」· 同场执行）**：**★ 挖到本场最值钱的一条**——`GOTCHAS.md` **G-08 子条款「相似→传承跳跃（传承举证责任）」**（**2026-05-21 Doctor 裁** · 原 G-20 候选并入）原文即列出传承的**四种带指纹形态**：**「被引文本 / 被搬形制 / 被教正典 / **制度连续**」**。⇒ **「制度连续」自五月起就在合格清单内**，首版那句「须能指出『被教』机制」**不是判断失误，是与既有 canonical 规则相抵**（只认第三型、排除第四型）。**已清扫三件**：`raw/2026-09-26_analysis_CS05证据层补全_折中法.md`（模板行 ＋ §一 补判据行 ＋ §三.1 补「传递形式的合格清单」段 ＋ 3 处术语改「被教正典」）· `raw/2026-09-26_analysis_CS01证据层补全_折中法样板.md`（模板行 ＋ 尾注留痕）· `raw/2026-09-26_analysis_文明基因原始提炼方法还原.md`（模板行 ＋ 尾注留痕）。**⇒ 后七案操作定义（合成三层）**：载体入首列须同时满足 ① B1 首列（被录用为教育／**传承**材料，两者并列）② **G-08 子条款四型之一**（传递带指纹）③ **`规则二`**（≥2 个不同处境下的重新选中）。**✅ 已办**：**B1 第 2 列措辞「须另找『被教』证据」→「须另找『被传承』证据」**，Doctor 裁「同批改两处」已执行——`raw/2026-09-25_analysis_文明基因晋升系统与形成史.md` §14.5 本体（＋改动点留痕，该卷无变更记录节）＋ `brain/logs/checkpoints/2026-09-26_D4重跑起手包.md` 转述件。第三处转述在 `raw/2026-09-26_analysis_CS05判定重跑.md`——该件为**历史诚实快照（三轮未通过·不得作验收件）**，按「历史记录不改」**保留原样**（已在两处改动点注明，防后手误引）。⑥ **⚠ 六项的角色重判未做**（本件只补证据层，**不宣称升／降为「正式」**）——须待起手包 §五.1 的整组重判。⑦ **余七案顺序**：CS-02 → CS-03 → CS-08 → 再观 CS-07／09／10／11（**CS-01 已出样板件，自「先跑四文明」队列移除**——原决策表与遗留栏的自相矛盾据此消解）。

- [ ] **PEC · 门禁推进的未收口项（2026-09-27 挂 · 源：`logs/2026-09-27-门禁推进与提交块工具.md` ＋ 两轮独立复验残余）**：本轮把门禁从「**零调用方**」推进到「**构建时调用**」，但**只证到「能挡构建」，未证「会被跑到」** —— PEC 仓无 CI、无班次，触发频率仍等于「有没有人跑 builder」（**第 10 项「门禁无调用方」的下游同病**）。**同挂四项**：① **门禁自检的触发频率未解决**（同上）· ② **QA 里渊图继承 8 条 ＋ PEC 专属 5 条仍无任何持久化守卫** —— 静默拆掉无人知晓（17 例用例不守它们；亦未做阉割实验）· ③ **`G-X83` 追记里落的「候选清单分档」加固仍未实施** —— 下次 `make_commit_block.py` 照样把 133 件候选混在一起端出来，**完全可能再漏一次**（本场已漏过一次：6 件内容日志）· ④ **材料面报告两处小瑕（只登记未修）**：`rel` 恒以 `README.md` 起头且**不核其存在** · 报告打印在负向测试**之前**（门禁失败时仍吐面清单，噪声）。**⚠ 均待独立验收后 `✅`；实施者不自签。**

- [ ] **PEC · 川习会检验窗落盘件验收（2026-09-24 /save 挂 · 源：`logs/2026-09-24-川习会检验窗与四轮复验.md`）**：`Projects/PEC/raw/2026-09-24_analysis_川习会产出与JP-P1一腿检验读数.md` + `predictions-register.md` v2.17.2（JP-P1 ① 腿观测追加三）。**⚠ 签字的默认路由：事务性／事实性的由未参与实施的 subagent 代签；方向性的问 Doctor（**未参与实施的 subagent** 为必要限定）。** 须过目的**三处实质补充**：① **B2 的「倾向不构成回调 · 未决」判定**（依赖归因，而归因**未唯一确定**——财政约束 vs JP-P2b「美压」通道，两通道本窗同向不可分）；② **§四 的机制修正提案**（改的是 observable 的**因果设定**、非读数；原稿全称模态已撤回）；③ **§4.2 的 T1/T2/T3 三条推论**（**非预测 · 无置信度 · 不计命中率**）。**另**：全程四轮独立复验/三轮修复已闭环（一审 14 → 二审 12 → 三审 8 → 四审 6 → 五审收口），**但最后两处修复（register L426 G-30 借用注、L1246 重复枚举）只经自验、未再过独立复验**。

- [ ] **剑酒青丘遗留仓 · 路径已漂，须重定位（2026-09-29 /todo 现核订正）**：原条所指 **`Database/剑酒青丘` 目录现已不存在**；现行两处为 `Projects/Financial/剑酒青丘`（**218 件 · 有 `.git`**）与 `brain/剑酒青丘`（13 件 · 无 `.git`）。⇒ 原条「`.git/index` 1062 条 vs 盘上 3 件」的前提**须在新址重取**方能判（`reconcile / 退役 / 加 .gitignore 或指针 stub` 归您裁）。**⚠ 重取时注意**：`Projects/Financial/剑酒青丘` 是本项目 A 股策略线（芒芒），与 EAL 本体的三层布局不同（见 `permanent/剑酒青丘落点分工`）。

- [ ] **PEC 日本线 · 三处未决（2026-09-23 /save 挂 · 源：`logs/2026-09-23-联大周三国互动与日本意图三分类.md` ＋ PEC `raw/2026-09-23_analysis_日本执政层意图三分类与结构性权力定位.md`）**：① **川习会（09-24）产出**＝JP-P1 ① 腿登记 observable 的**真检验窗**——看日本对华姿态是否回调（09-23 读数＝缓和信号已到位但姿态未回调、系前置加固）；② **B2「对美议价是否被咨询」缺独立观测面**——⚠ 该判据当前**未被满足**（非「缺数据源」），要用得先找数据源或降级；③ **2028 参院改选时点与自民议席预期**＝修宪线的**实际变量**（决定参院 2/3 可达性），本场未查。**另两条已在 register 登记**：JP-P1 ② 腿近端检验点＝2027 春自民党大会「修宪 メド」；非核三原则在安保三文书改定中是否被写死＝②③ 之间独立观察位。

- [ ] **巡检 · 周班简报是死代码 + 面③ 黄条送达 + 快照判据口径（2026-09-22 /save 挂 · 源：`logs/2026-09-22-巡检补盲与行情链共模修复.md` ＋ `permanent/巡检自愈循环-loop-engineering.md` §4 注）**：① 周班跑不了脚本即按自身 prompt 明文「报无法执行 + 贴命令 + 干净退出」⇒ **步骤 2–5（含出简报）在本环境走不到**，故「快照前进」只能由 Doctor 终端手动跑证明，`triggered_by=scheduled` **不是「班自动跑过」的证据**。② 由此派生的两个待定：**(a)** 周班要不要改成「跑不了脚本时也能读上次快照并出简报」——需 store SKILL 改动（Doctor 终端 SHA 往返）；**(b)** 快照验收判据是否从「generated_at 前进且 triggered_by=scheduled」改为承认「人工按班交接原文带参跑」。③ 面③ 的 ⚠ 黄条**已**改由 `brain-resume` Step 0.6 附报（09-22 落盘·四端 `11ee480b`），周班侧是否重复由 (a) 一并定。


- [ ] **行情链 · 三处残留（2026-09-22 /save 挂 · 源：`logs/2026-09-22-巡检补盲与行情链共模修复.md`）**：① ~~**`trade_cal` 表要等下次 `ingest_stock_daily` 跑才落**~~ **✅ 2026-09-23 已落并验收（CC 代勾 · 证据硬）**——实读 `market_data.db`：表已建（16→17 表）· 字段 `cal_date/is_open` · **121 行** · 最新 `20260923`（含 09-19/09-20 周末 `is_open=0`）；`mac_marketdata_20260923.log` 原文 `✓ trade_cal：20260526→20260923 共 121 天（开市 86）` + `陈旧判定（市场时钟 = trade_cal · D0=20260923 · D1=20260922 · 截到 20260923）`、**「回退」字样零命中**、结论「各表均达到市场时钟所要求的档位」；`ops/.last_run_status = OK 2026-09-23 02:31:51`（launchd 02:30 点火成功＝09-21 关机漏跑后首次恢复）；② `ops/.last_run_status` 只留最后一行 ⇒ **同日重跑即抹掉失败记录**（已三次咬人），建议改追加式滚动 N 天或至少留 `.prev`；③ `ipo-rolling` 的 `StandardOutPath` 仍在 `/tmp` ⇒ 面③「应跑未跑」对它**零覆盖**（09-18 的 stdio 迁移只搬了 usclose/marketdata 两件），建议同批迁出。另：两套新增负向测试（快照 45 项 / 烛照 27 项）**不挂在任何班或巡检上**，回归保护全靠人手跑——是否挂班归 Doctor 定。





- [ ] **行业研究仓 · 工作区残余待裁（2026-09-18 /save 挂 · **2026-09-26 /todo 现核删失效子项**）**：watch/ 09-05 alarm_store 五件（`alarm_store.py` + `test_alarm_store.py` + `history/` + `revisions/` + `current.json`，**实读仍在盘**）、`docs/PROPOSAL-投知君君图谱候选.md`（09-16 改，**实读仍在盘**）——归属他场，提交/搁置归 Doctor 裁。~~`index.json.bak_2026-08-24` 与 `bak_20260821_pre_refill` 两删除~~ **（2026-09-26 现核：两文件均已不存在，该子项消）**。

- [ ] ⚠**〔前提已被取代 · 2026-09-29 /todo 现核 ＋ Doctor 裁「标取代·不执行」〕本条的「待授权执行两修法」不再执行**——09-29 DVA 线发生**架构级取代**：fuxi 已部署 `dva_incremental_pipeline.py`（`E:\AI\DVA\ops\manual\author-policy-20260929\` ＋ `backups/runtime-deployments`），Codex 侧 `Project Mirror/DVA/README.md`（09-29 09:56）明写「Refill/自愈/健康入口**统一到统一新增量协调器**、旧批次恢复协议**仅保留历史**、两个 DVA 运维自动化**保持 PAUSED**」；fuxi 上 `DVA-Refill`／`DVA-Healthcheck` 实测 **State=Disabled**。**保留一句待验（留待下一场现核）**：新链是否覆盖浪浪／是否仍有同症。以下为原始留痕（勿据以执行）。** **DVA · 自愈链两真根因已诊断未执行 + 终验顺延至 fuxi 回线（2026-09-22 更新 · 源：`logs/2026-09-18-龙鱼截图流与DVA金融线实核.md` ＋ Mac 侧 `Codex/Project Mirror/DVA/ops/state/dva-codex-supervision/`）**
  **① 三项新契约仍顺延**——Mac 去 `st_dev`／`MIRROR_MAC_DISPATCH_LOST`+链式退役／`Get-DvaWriterRole`，等「下一个走到 mirror 的班」（若 mirror 再 unknown 且 Mac 无 intent，先离线跑 `_require_prior_actions_settled`）。
  **② 18:15 自愈首验：跑起来了，但卡住**——09-19 班 `refill-cycle-20260919T090001620Z` FAILED/**75**（`FINANCE_PENDING_HANDOFF`，设计内退出码 · 非硬故障），17:08 留 `.pending` 票据无人认领。原 rrule 写法 `DTSTART;TZID=Asia/Shanghai:…` **未生效**（与在跑的四个 heartbeat 写法不同形）→ VV 09-19 改型为 `FREQ=DAILY;BYHOUR=3;BYMINUTE=15`（PT 03:15 ＝ 北京 18:15）→ **09-20 首验触发成功**（PT 03:59 落 plan ＝ 北京 18:59；`lastBusinessProgressAt` ＝ 北京 09-20 18:54）。⚠ 冬令时后固定 PT 03:15 会漂成北京 19:15（在跑的四家同病，本轮不改）。
  **③ 两个真根因（VV 均已诊断，两 plan 皆 `executionAuthorized=false`·`businessRuns=0`，未执行）**：㈠ **policy 时间戳比较 bug**——inspect 在自身 terminal journal 更新*前*捕获快照，policy 却拿 `observed_at` 比 inspect 的 `recordedAt`，不可能的次序 ⇒ 递归的无副作用检查链，**一个合法 writer 但永不产生业务动作**（修法：inspect 只比 `issuedAt`，业务动作保留 `recordedAt` 边界）；㈡ **enrollment 错配**——bootstrap 仍批准更旧的 release transaction，与已装 policy 不匹配 ⇒ 新 cycle 拿不到 coordinator enrollment（修法：certification-only core transaction ＋ bootstrap 升级，明文不动业务代码/数据/调度/原 FAILED/journal）。
  **④ 阻断面**：fuxi-station **出游离线至 09-26**；Mac 消费镜像停在 09-18 代次（`dva-mirror-20260918T191145Z-047034d0`·published 09-18T19:16:11Z）未再前进。09-20 班 fuxi 本地自主跑出 `lastAttempt` attempt 1 exit 0 **SUCCESS**（不依赖 Mac）；⚠ **但同一记录里该 cycle 的 `refill` 臂仍 `exit_code:75`/FAILED**（设计内退出码），两面对读、不得只引一面；09-20 北京 08:30 healthcheck FAILED/exit 2/blockerCount 3 **属离线所致、非班次实错**——勿据此判 09-19 恢复失败。
  **⑤ 09-26 补核已完成（CC 实读 · 北京 09-26 11:07）——结论是「系统性停摆，非单班漏点」**：逐项实况 ——
  · **票据兑现**：机制**正常**（每天生成 `{cycle}.json` + 写 locator；09-19 那条于 09-19 23:30:18 兑现）。**但七张票据全停在「等待诊断」**：`dva-failure-latest.json` 明写 `outcome=FAILED_REQUIRES_DIAGNOSIS` · **`diagnosis_owner="codex"`** · **`codex_diagnosis_required=true`** · `automatic_redispatch=false` · `business_runs=0` · `retry_owner="dva_self_heal_coordinator"`。⇒ **不是无人认领，是被指派给 codex 诊断、而诊断从未发生**。
  · **coordinator 终态**：**未推进**。Mac `state.json` 的 `coordinator` 仍是 `{closed:false, currentCycle:false, ordinal:1, status:"succeeded"}`（旧记录）；`businessEvidence.refill` 停在 09-20 cycle；**state.json mtime 停在 09-21 10:01 PT**（`observedAt` 未再前进）。
  · **Mac 镜像新代次**：**七天无新代次**——仍是 `dva-mirror-20260918T191145Z-047034d0`（published 2026-09-18T19:16:11Z），`.dva-fuxi-mirror.json` mtime 亦停 09-18 12:16。
  · **消费端回读**：同上一行，`Database/Douyin` 停在 09-18 代次。
  · **旁证**：09-20~09-25 **连续六班全部 FAILED/75**（`refill-cycle-*.json` 562 B 同形）；09-26 07:00 healthcheck **FAILED/exit 2**，关键字段 `refill_task_last_result=75` · `refill_cycle_success=false` · `refill_age_hours=398.8` · **`refill_summary_run_at` 停在 `2026-09-09T09:42:48Z`** · 诊断码 `HEALTH_RECONCILIATION_UNCERTAIN` + `FAILED_PARENT_TAIL_SOURCE_CHANGED`。
  ⇒ **待 Doctor 裁**：两个真根因（policy 时间戳 bug / enrollment 错配）的两个修法 plan **至今 `executionAuthorized=false`**，且均需部署到 fuxi（production mutation）、入口在 Codex 侧（`dva-fuxi-mac` automation + `run_dva_self_heal.py`，CC 有 darwin+路径双闸跑不了）。**是否授权 VV/Codex 现在执行这两个修法 → 见 2026-09-26 会话报裁**。
  **⑥ 验收性质提示**：Mac 侧 runtime 在 09-19 后有代码变更（`dva_self_heal_journal.py`·`freeze_dva_self_heal_release.py`·`dva_healthcheck_recovered.py`·`dva_mac_mirror_contract.py` ＋ 一批 tests）⇒ **该部分含功能性成分，归 Doctor 或 Doctor 指定且未参与实施的验收方**；纯事实部分（班次终态／镜像代次／消费端）可由未参与实施的 subagent 落签。
  **⑦ fuxi 回线当晚现核订正（CC 实读 · 2026-09-26 03:0x–03:2x PDT · 承 Doctor 裁「fuxi 回线收口」）——⑤ 的「系统性停摆」标题须收窄，两处已不成立**：**(a)** 「Mac `state.json` mtime 停在 09-21 10:01 · `observedAt` 未再前进」**已被推翻**——现读 `revision=64` · coordinator `succeeded` · `observedAt=2026-09-26T10:07:36Z` · `lastBusinessProgressAt=09:43:47Z`。**(b)** 不止「停在等诊断」：`refill-cycle-20260926T090001670Z` 的 **collection 阶段成功产出**（`collection.json` sha `d20b77c4a5a868c2…`），attempt 1 于 09:40:03Z exit 75 后 **90 秒（09:41:30Z）即建出 `finance-campaign-*`**——`handoff-receipt.json` 状态 **`METADATA_CREATED`**、campaign `status=resumable`·`finishedAt=null`、两位作者 `投知君君买方视角`／`老毛聊交易` 皆 `pending`·`slices=0`，而 `businessRuns=0 · modelCalls=0 · workerRuns=0 · published=false` ⇒ **元数据建齐、业务零动作**（G-X192 形状）。**(c) 本轮新定位 fuxi live 目录 ＝ `E:\AI\DVA`**：Windows 计划任务 `DVA-Refill`（每日北京 17:00 · `run_refill.ps1` · LastResult **75** · Next 09-27 17:00）与 `DVA-Healthcheck`（每日北京 07:00 · LastResult **2** · Next 09-27 07:00）；另有五个 `DVA-Credential-Canary-*` Ready 但 last 全停 09-15（观察项·未判）；**未发现** fuxi 侧自愈 coordinator 的独立计划任务。**(d) 关键订正**：09-25 那条 `fix(DVA): certify installed self-heal policy` **不是「未生效」而是「内容零变更」**——`dva-deploy-cert-policy-20260926-v1` 的 `state.json` **status=COMPLETED**，但其 `manifest.json` 唯一文件 `runtime/tools/fuxi/dva_self_heal_policy.py` 的 **`beforeSha256` 与 `sha256` 完全相同**（均 `2f4cecf2ab800ae5…`）；installed／before-backup／staging-core 三处 SHA 复核一致（46668 B · mtime **2026-09-20 19:02:46 北京**）⇒ **它是重签认证、不是补丁，结构上不可能修掉代码级根因**；且已装策略第 **657–666 行已含**「inspect 只比 `issuedAt`／业务动作保留 `recordedAt`」那条修法（是否即㈠之修法待 VV 确认）。**(e) Doctor 已裁（2026-09-26 03:2x PDT）：先认证、再放行写动作**；CC 已据此落执行件 `4AI/Shake hands/to VV/CC-to-VV-DVA认证半段授权-2026-09-26.md`（sha256 前缀 `7cd70d926d398302` · 含四问与实读证据表），**写动作未放行**，待 VV 只读认证回报后单独放行。**(f) 连带**：渊图批发②的 `Database/行业研究/prices/commodity_prices.jsonl.bak_pre_clean_20260608` 现核**仍在 Mac 原地、fuxi 上查无** ⇒ 归档未做。

- [ ] ⚠**〔前提已被取代 · 2026-09-29 /todo 现核 ＋ Doctor 裁「标取代·不执行」〕路线① 未按原样执行、且已被 09-29 新架构取代**（自愈链第二环的旧入口随 `dva_incremental_pipeline.py` 上线而改道；`DYD_HARVEST_PARTIAL` 在 Codex 镜像全树 **0 命中**，新链只输出 `status='success'|'partial'` 另一语义）。**仍成立的事实**：`Transcripts/浪浪Insight` 实数为 **79/79/0**，与 09-18 认证 `declaredCount=79` 精确吻合——**Mac 侧镜像自 09-18 未前进**。**保留一句待验**：新链是否覆盖浪浪、是否仍有同症（留待下一场现核）。**另**：附注「班次汇总表『最近更新』列口径可疑」——全盘**未定位到该表，未核**。以下为原始留痕（勿据以执行）。** **浪浪Insight · `partial` 常态化的处置待裁**（2026-09-22 挂 · 源：`logs/2026-09-22-DVA自愈链诊断与三条教训.md`）**：浪浪自 09-14 起每日班均判 `partial`（`DYD_HARVEST_PARTIAL_V1`：`coverage=visible_routes_incomplete`·两条 route `1128`/`6383` 均 `PostRoutePayloadMissing` 中途跳出），而**内容实际不缺**——`Transcripts/浪浪Insight` = **json 79 / txt 79 / other 0**，与 09-18 浏览器覆盖认证 `declaredCount=79`（endReached=true）**精确吻合**；三个失败列表（downloadFailed / metadataFailures / asrFailed）**全空**。⇒ **partial 已成常态、信号价值归零**：真漏一条新作品时症状完全相同，无人分得出（今天能断定不缺，只因 09-18 那次认证把数字钉住了）。两条互斥路待裁：**①** 让 recovery 自动跑（partial 每天自动转 complete，噪音消、真缺口重新有信号）——治本，但需先接通自愈链第二环（消费者已定位＝Codex automation `dva-fuxi-mac`，见 `permanent/DVA自愈链.md`）；**②** 承认「路由不全但浏览器覆盖完整」为正常态、班不再为它报 partial——改动小，但等于接受 API 路长期不全。**CC 倾向 ①**。**⇒ 2026-09-22 Doctor 裁：走 ①**（执行随 fuxi 09-26 回线，先接通自愈链第二环）。**另附一条待核**：班次汇总表的「最近更新」列口径可疑（对浪浪显示 09-14，而它 09-18 实际落过字幕）——已成功骗过 CC 一次（致我误报「零产出」），建议 DVA/Codex 侧核其取数口径。




- [ ] **PEC · 9-30 中评首读（2026-08-21 挂 · 源：`logs/2026-08-21-PEC美以伊60天窗与利益透镜复审.md`）**：IR-P3 新基准 / 僵持命题 / 镜像命题 / 行为走廊修订。**IR-P6 净读拍板已销 ✓〔2026-08-21 Doctor 拍「净读回中性」· register 已落 · `logs/2026-08-21-美债解法与财政巩固政治学.md` 场〕**。

- [ ] **EAL · VV 十四轮窄修（2026-08-18 已改 · 十四轮 commit `bc1e86f` 已推送 ✓〔已核实：gitcheck.py 2026-08-18 · HEAD=bc1e86f5c2 · worktree 0 · push 已同步〕· 留痕 commit `2d6bec2` 已推送 ✓〔VV 十五轮核〕· 十五轮追记 commit `1d104f3c` 已推送 ✓〔gitcheck 实核〕）**：八轮 `894ab9d` ✓、十轮 `0367ec2` ✓、十一轮 `ce63f3a` ✓、十二轮 `9857bd0` ✓、十三轮 `bc6bf3c` ✓（均 Doctor 推送 · 旧命令作废勿重跑）；关闭合同两句已统一 · 三层 SHA `f0437ea5…` · runtime cache 已 v1.5.4；十五轮同根追记（RISK-002 追记八）+ 三漏项（README×2 v1.5.4 · Vault 旧包 `065c5f0a…` 标 _DEPRECATED_ · INFRA-001 事实更正）已落。**✓ fresh-session 两次路由实测完成（08-18/19 两个全新会话 · CC 客观代勾 · 证据：会话一 `/prd 路由实测` 命中 brain-prd·关闭合同回答为 v1.5.4 新句·§1「不立≠撒手」口径实弹；会话二「写交付标准」自然语言触发·`2026-08-19_Shakehands清理_PRD.md` 在盘（frontmatter task_authorization 新字段·awaiting_acceptance 未自签·独立审查员背书）·删除实况 find 全树 38 与 PRD 声称一致）**。**待**：① Settings 已重贴（Doctor 2026-08-19 会话「done」· 含 PRD 立卷边界条新版）· 注入验证 ✅ 已核（2026-08-19 /resume 场逐行比对：块二存在 · 含 PRD 立卷边界条 · 无六轮旧措辞 · 漂移零）· 最终运行时签字待 VV；② ~~gateway 侧 /prd 路由是否纳入验收范围（Doctor 定）~~（✅ 2026-08-26 问答板 1B 裁「纳入验收范围」· CC 代记留痕）；③ VV 十六轮复验；④ ~~存量 PRD 处置表裁定进行中（下条）~~（✅ 2026-08-26 问答板 1D 现核闭环：08-19 场已按推荐全执行——2 delivered + 4 cancelled+superseded + 19 班 cancelled + gate 证据同步（`logs/2026-08-19-EALv3升级全链路与v2.3功成退役.md` L20）· 销账留痕）；⑤ ~~其他 brain skills 漂移收敛专场~~（**⇒ 2026-08-26 问答板 2E 裁「开」→ 侦查现核：现行规则面零漂移**——.skills//Doctor协作偏好/CLAUDE.md 模板全干净，仅剩旧句均在历史叙述引号内（通用教训 G-X136/G-X151 现象段、剑酒 GOTCHAS 追记）不应改 → 专场零动作 · 待您确认销账）；⑥ ~~`⏳` 活状态迁移专场（12 项目）~~（**⇒ 2026-08-26 问答板 2F 裁「开」→ 已执行**：图例 8 处（GlobalPercent/O MY HTML/司南/海螺姑娘/渊图/烛照九阴/风险日报/龙鱼五力）+ 真条目 1 处（GlobalPercent ⏳→⚠️ · git 已核实已提交〔gitcheck.py 2026-08-26 · brain HEAD 5ba6279e 含「问答板集中批执行(⏳迁移8图例…)」commit · worktree 0 · push 已同步〕）· 终验残留均为历史注释叙述不动 · 执行完自验 ✓ · 待独立验收）；⑦ ~~dry-run 测试 6 项增强并入 gate 判据集 PRD~~（⇒ 2026-08-26 /todo 合并注记：并入「EAL 余尾批发④」gate 验收脚本 PRD 候选，与渊图 promote 第 15 项负向单测同批待批，本处不再单列）。
  依据：VV 十五轮终验回执 · `剑酒青丘/GOTCHAS.md` RISK-002 追记八 · 08-18/19 两会话路由实测转录

- [ ] **白泽观星 · CN 腿首跑（2026-08-14 自 BT-19 条拆出 · Fed 腿日更 08-14 已入调度 guanxing-fed-daily）**：CN 腿 tushare --dry 对键→取数（Doctor 终端件）；烛照九阴 fomc_note 对接待 Fed 腿稳定后。

- [ ] **V.V. ferry · Fable 5 API 密钥/预算（2026-08-03 由 /todo 漏挂对账补挂 · 源：`logs/2026-08-03-哨兵班400风控二分定位.md`，承 08-02/08-03 场未变）**：Doctor 动作余项。（⇒ 2026-08-26 问答板 5A 裁：继续挂账等您）



- [ ] **龙鱼 · ds 腿引用数字检测机制（2026-08-20 补挂 · 源：NOTE-20260819-001 · 原 08-15 挂条已从 TODO 消失）**：ds/LLM 盲打 evidence 中具体数字（产能/订单/营收额/市占率）须能在 canonical/engine_facts 找到同源，找不到标 P3 降权或不采；机制化=校正/销账审计逐句对 canonical。同族两例：08-15 华工「2万样机」P3 当事实、08-19 海光「中芯产能」错链锚（华为链·海光代工实为三星）。**⇒ 2026-08-26 /todo Doctor 裁「暂缓」**：等校正/销账审计自然推进时顺带机制化（非阻塞项）。**⇒ 2026-08-30 裁定场「暂缓」前提被第三次复发推翻 · 机制化部分已实装（CC 实施 · 08-31 日志实据）**：check_ds_evidence.py 三档（无锚/P3当事实/旧锚）+ 持久化负向测试 5/5 PASS（当场逮 3 真 bug 已修）+ 实跑 08-29 ds 条目 ⚠67 提示级（真信号+泛短语噪声·附锚出处可人核）。另「错链」定性被 canonical 旧锚推翻：rel_Haiguang_SMIC_South（04-29 P1 未退役·desc 与 ds 引用逐字吻合）。**残余挂裁（归 Doctor）**：① 检测脚本是否挂进周更班（班 prompt 改动走 Doctor 终端 SHA 往返）；② ~~canonical 海光代工叙事时序冲突（中芯旧边 vs 05-16 起三星代工叙事·旧边退役或标时效）~~ ✅ 已闭环（09-01 海光旧边标时效已执行：desc 加 [04-29 口径·已过时] 前缀+_meta 注记 · commit `95d1fb0` 在链 · 2026-09-03 Doctor 裁确认标时效路线 · CC 代记留痕）。


- [ ] **X-Board · VV 知会数据侧 shape 统一（2026-08-24 挂）**：08-22 DVA refill 班镜像 ASR 管线切换（backend=local-qwen3/Qwen3-ASR-1.7B），老毛 16 篇转写变新 shape（顶层 text·无 sentences）——消费端已兼容（CC 08-24 改提取器+生成器），但数据侧 contract 未归位。知会 VV：镜像 shape 统一回 sentences 或正式发布新 contract；触发=VV 回执或镜像下次 shape 再变（若再变，兼容层会成新坑——见 08-24 问答板裁定记录）。

- [ ] ⚠**〔数字漂移 ＋ 子项状态订正 · 2026-09-29 /todo 现核〕**① 已裁已执行（X 看板自动重推班 `xboard-daily-repush` 18:00 PT 在跑）· 首次重推 payload 级回读 ✅ · 视觉目验 ✅ 已销。**② 数字漂移**：「981 条 pending AI 分析」**当场重数为 `ai_status` 空 2148 条**（`historical_headlines` 共 7315 行、processed 5167）。**③ 仍 open**：Sites 重发布（公开站点仍 08-19 旧构建）——`dist/` mtime 09-26、`app/generated/public-snapshot.json` 09-29（快照新于构建），GOTCHAS 最近发布记录仍是 2026-07-31 ⇒ **未发布**。**④ 已闭未勾**：`X-BOARD-OPERATIONS.md` §9 修正已由 **VV 2026-09-01 独立重放验收**（`GOTCHAS.md:355` NOTE-20260821-006 状态＝已解决）。**⑤** 「`twitter auth status` 命令校正」**未核**（无 `--help` 输出可对照）。** **X-Board · 接管首日遗留——**✅ 已裁（2026-08-22 Doctor 裁「每日 18:00 PT 一次」· scheduled task `xboard-daily-repush` 已建 · notifyOnCompletion · 首跑核 updatedAt+回读待今晚班后）**。一次性重推已执行（2026-08-21 深夜 · Doctor 批「由我执行重推」）：gen_xboard_artifact.py exit 0 → update_artifact x-board 已推（45 items/9 cols/669,380 chars · 两列新料在板）· payload 级回读 ✅ 已收口（2026-08-21 深夜 Doctor 终端实跑 `PAYLOAD-MATCH: True` · 剥平台 script 包装块后与 canonical 逐位一致）；视觉目验 ✅ 已通过（2026-08-21 深夜 Doctor「目验 ok」销账）；**；② 981 条 pending AI 分析（`npm run history:analyze` · 等 Codex 额度恢复）；③ Sites 重发布（公开站点仍 08-19 旧构建 · 归 Doctor/VV · ⇒ 2026-08-26 问答板 6C 裁：排期归您/VV）；④ X-BOARD-OPERATIONS.md §9 修正（先 build 再测 · 已记 GOTCHAS NOTE-20260821-006）✅ **已落盘待独立验收（2026-08-21 深夜 Doctor 批「批准 §9 修正」· NOTE 状态改已修待验）** + `twitter auth status` 命令校正（待 twitter --help 输出）；⑤ 生产版 Next.js 同步两列抖音（需动服务端 schema · 另批）；⑥ 老毛/投知接 DVA 定时采集管线（料止 07-29 · 另立项 · ⇒ 2026-08-26 问答板 6F 裁：另立项确认）⇒ **2026-08-22T05:13Z 镜像方案 2 首次手动原子回流 PUBLISHED（6,450 文件 · 双端证明 · 可原子回滚）——料已补至老毛 522/08-20、投知 196/08-18（CC 只读 SQL 实核一致）；自动定时回流班仍另立项。⇒ **2026-08-26 晚 fuxi 侧出错 · Doctor 修复后手动补跑回流（`dva-mirror-20260827T064311Z` · 6,573 文件 · 已发布）——实核（08-27 00:21）：老毛 videos JSON 538 件至 08-22、投知 198 件至 08-26（重推班已上板 · 投知两新件要点已提取）**。**

- [ ] **EAL · 扩列试水批收尾（2026-08-25 挂 · Doctor 裁「小步扩事件覆盖·宏观+地缘·专场」）**：batch1 编码完成——registry 9→11（+02-28 开战/+07-31 科威特·parse_event 11/11 PASS·既有 9 行逐位一致）；7 候选转化 2/7，5 exclusion 留池（notes 在盘）。**待**：① ~~班 prompt 的 registry 引用是否写死 08-21 版——Gateway store 沙箱不可读，需 Doctor 终端核；若写死需裁切换方案~~（✅ 2026-08-25 闭环：班 prompt 改句「沿用同目录最新日期版」+ update_scheduled_task 回读验证 ✓ + 08-24 班实际行为已取最新 input_identity 实证 · Doctor 2026-08-25 /todo 统一授权勾销 · CC 代记留痕）；② ~~新 registry 的 shadow 重跑（今晚班或 Doctor 终端）~~（✅ 2026-08-26 /todo 现核闭环：08-25 17:44 班产物 `daily-shadow-result-20260825.json` 实读 row_accounting frozen_events=11 · raw_events 11 · excluded 0 · engine shadow.7 · sealed 前后 production SHA 一致（只读班 ✓）· Doctor 2026-08-26 统一授权勾销 · CC 代记留痕）；③ T2 候选池沉淀（07-14 封锁需先订正台账主体归因 / OPEC 需扩 release_code 闭集 / 宏观日历件 FOMC 纪要族+8 月底 PCE 属可转最高优先级）；④ ~~剑酒青丘数据仓 git commit~~（✅ 2026-08-25 已核实：gitcheck.py 实跑 · HEAD 3ef976db 含两条扩列 commit〔batch1 4 件+班产 4 件〕· worktree 仅 attribution.db 值守班日常）。依据：`coding_work/code_expansion_batch1_20260825.py` + `frozen-event-registry-v3.2-20260825.jsonl` + `coding_notes-20260825.jsonl`。

- [ ] ⚠**〔已于 2026-09-30 裁 · 问答板 Q12A：按档内裁定撤项，①②④ 一并处理；③⑤ 余量已另立为本段「EAL · 余量（③⑤）」条 ⇒ 本行待迁 `TODO-已完成归档.md` 的「已取消」段，勿据以执行〕**：`references/TODO-已完成归档.md`「**已取消**」区已明写「EAL · v2.3 五项方法 gate…**慢牛漂移溯源不再追踪；B 阶段方案已 cancelled**」＋「gate 验收脚本 PRD…随 v2.3 退役取消迁档」；`checkpoints/2026-08-17_EAL-B阶段G2G3执行方案.md` frontmatter 亦 `status: cancelled`（G2 需求由 v3 clock 合同承接）⇒ **本条 ①② 的开口状态与档内裁定相抵**，建议按档内裁定**撤项或重述**。**④** 与 L159 重复且行文过期（该 PRD 实为 `awaiting_acceptance` 且 09-18 专场已开完，非「进行中」）。**③** Gateway 版本文件在 store 内 ⇒ **未核**。**⑤** 生产库读者切换仍待裁。** **EAL 余尾批发 ＋ `logs/2026-08-15-EAL方法论重构v1.4至v2.2.md` ＋ `logs/2026-08-21-EALv3总签发布与数据链班启用.md`）**：① B 阶段 G2（事件时钟 db schema）/G3（价格口径敏感性）另排；② 慢牛漂移 +12.96 逐日溯源；③ 2-R 全局传播至 Gateway 版本文件（versions/1786977170792.html 仍 v2.2）；④ gate 验收脚本 PRD 待批（`logs/checkpoints/2026-08-17_EAL_gate验收脚本_PRD.md` · status 进行中；**⇒ 2026-08-25 追加**：渊图 promote 第 15 项同三元组闸负向单测未持久化，并入本 PRD 候选 · 源：ERR-20260825-001；**⇒ 2026-08-26 /todo 再追加**：EAL dry-run 测试 6 项增强（VV 十四轮窄修⑦ 迁移至此），同批待批）；⑤ 数据链班残项核（~~行情缺口回补/sealed 在 Gateway 侧待 Doctor 终端核~~（✅ 2026-08-26 /todo 现核闭环：eal-v3-event-transition artifact updatedAt 08-26T04:45Z 实读 = 08-25 17:44 班已跑+推 ✓ · sealed-20260825 产物在盘（daily-shadow/seal-evidence production SHA before=after）✓ · Doctor 2026-08-26 /todo 问答板「数据链班 sealed 核」勾选由 CC 盘核代完 · CC 代记留痕）+ 生产库读者切换待另裁。

- [ ] **渊图挂账批发（2026-08-22 /todo 漏挂对账补挂 · Doctor 问答板全选 · 源：`logs/2026-08-15-渊图三轮清洗专场.md` ＋ `logs/2026-08-19-渊图具身智能线开线与图谱手术.md` ＋ `logs/2026-08-16-Boss老白全量下载与渊图P2入库.md` ＋ `logs/2026-08-17-Boss老白普查VV盲审与provenance管线闭环.md`）**：① ~~三轮清洗 PRD 原则轨 3 条待 Doctor 验收（status 进行中）~~（✅ 2026-08-26 Doctor /todo 问答板裁「现在验收」逐条 ✓：原则轨 2 条 [✓]（14 组分类处置认可+质检门口径认可·第 1 条已裁定不参与）+ §四 已交付 + 变更记录留痕；「CLAUDE.md 口径落盘」执行尾现核实已闭环（质检清单节 08-15 已立·本轮补第 15 项行）· CC 代记留痕）；② ~~前场积压 3 文件待判（index.json / prices/* / `mapping/_proposed_region_20260630.json` · 非本场产物）~~（✅ 2026-08-26 /todo 现核销账 · Doctor 裁「前提失效」：index.json 与 _proposed_region 均为活跃生产文件（08-25 当日仍有写入·入库/region 打标正常产物）；唯一残留 prices/*.bak_pre_clean_20260608 已 tar 待 fuxi 归档 · CC 代记留痕）；③ ~~kg_promote 第 13 项「新节点 desc/props 双空断言」待批（NOTE-20260819-002）~~（✅ 2026-08-26 Doctor /todo 问答板落签销账：08-19 已批已装 + 08-20 CC 独立复核背书（kg_promote.py L32-42 实读 · 自测 5/5 · canonical 零误动）· NOTE 状态行已 ✅ · CC 代记留痕）；④ 待回填包：4 Boss老白 desc 空（NOTE-20260819-001 · 待自然回填）【✅ desc 空 4 件已回填（2026-09-17 /todo 核：canonical `"desc": ""` 计数 0）】+ 本批缺 name 补全 + 畸形节点 id/name 注记 + 972 span 回填另批（⇒ 2026-08-26 问答板 8A 裁：等自然回填+另批）。⑤ ~~华为 OCS 链入库~~（✅ 2026-08-23 闭环 · Doctor 裁「全量一批」→ CC 执行 · 证据：patch `mapping/_v3_20260823_华为OCS链_manual.json` 5 节点/13 边 · canonical 5048/5630→5053/5643 实读 · 札记 `raw/核实/2026-08-22-华为OCS链核实札记.md` · QA 全绿 · 备份 `backups/行业知识图谱_完整数据库.json.bak.20260823_005205` · wiki 3 卡）。剩两尾：~~git commit 命令待 Doctor 终端跑~~（✅ 2026-08-25 已核实：gitcheck.py 实跑 · HEAD 582392c 含华为OCS入库 commit · worktree 0 · push 已同步 · 销账留痕）；~~光迅双节点疑点待 Doctor 裁~~（✅ 2026-08-23 Doctor 裁方案 A 并入 Accelink 已执行 · GOTCHAS ERR-20260823-001 · 备份+QA 全绿 · **✅ 2026-08-26 四批打包验收 Doctor 终签〔机器层九项过+墓碑已补（mapping/_tombstones/2026-08-23_guangxun_merge.json）+判断层全部认可〕· CC 代记留痕**）。

- [ ] **杂项 D 批发（2026-08-22 /todo 漏挂对账补挂 · Doctor 问答板全选 · 源：`logs/2026-08-15-龙鱼双scorer周更.md` ＋ `logs/2026-08-15-华工Rubin板载NPO定点传闻核实.md` ＋ `logs/2026-08-20-龙鱼销账与调研情报局视频入库.md` ＋ `logs/2026-08-21-烛照九阴风险竖条与逾期信号处置.md`）**：① ~~CPO 3 只升常更勾选（常更标的.json 未加 · 清单由常更标的审核.html 维护）~~（✅ 2026-08-26 Doctor /todo 裁「升常更」已执行：`Database/龙鱼-标的分析库/常更标的.json` 加 688313.SH 仕佳光子 + 300620.SZ 光库科技（天孚 300394.SZ 已在）· count 23→25 · updated 08-26 · 备份 .bak_20260826_add_cpo3 · 常更标的审核.html 清单同步待您目验 · CC 代记留痕）；② 华工 3.2T 官宣触发器 + 9 月底-10 月观察窗（备案通知书/PHIP）+ 招股书「直接对接北美客户」原文直读；③ DVA transcribe 长音频分段根治（BUG-20260819-001 · 待 Doctor/VV 裁修复方案 · ⇒ 2026-08-26 问答板 9A 裁：继续等 VV/您裁方案）；④ 烛照竖条灯 + 黄条 56→27 目验（08-21 班产物已推 ✓ · zhuzhao-jiuyin-daily updatedAt 08-21T17:23Z · 目验归 Doctor）。




- [ ] ⚠**〔前提已变 · 2026-09-29 /todo 现核〕落点问题已可指认、指向问题已自解**——fuxi 健康产物落 `E:\AI\DVA\ops\state\dva-healthcheck-latest.json`（09-27 08:30）＋ `ops\summaries\dva-health-*.md`；而 GAI manifest（`海螺姑娘/data/asset_manifest.json`）的 DVA-Database 项读的是 **Mac 侧** `Douyin/DVA-Database/_health.json`，该件现已补齐并被点亮（见本文件「DVA · `_health.json` 缺位」条）⇒ **「改指向」的前提不存在**。**回流写入者**：fuxi 计划任务清单里**未发现**独立的「回流」任务；两 DVA 任务现 Disabled。**残余**：旧回流链停摆、Mac 镜像停 09-18 —— 归 09-29 新链。** **DVA · health 产物新落点确认 + 回流写入者排查（2026-09-01 /todo 漏挂对账补挂 · 源：`logs/2026-08-31-氦气鲜价喂入与DVA库审计定案.md` · INFRA-20260901-001 观察项②③）**：fuxi 侧 health 落点确认后改 GAI manifest 指向；回流写入者疑 launchd——均需 fuxi 侧核。


- [ ] **EAL · ERR-20260828-001/002 落签（2026-09-01 /todo 漏挂对账补挂 · 源：`logs/2026-08-28-EAL验收链与消费治理.md` · 剑酒 GOTCHAS 实读 🔄 已确认待修复）**：001 索引 v6 与盘面漂移（修复＝VV 重生成 v6 或 Doctor 裁处置）·002 重放误报（无写入发生·前后 SHA 零变化）——落签按分轨：事务性／事实性的由未参与实施的 subagent 代签；方向性的问 Doctor。


- [ ] **DVA · dev/19 关闭裁定（2026-09-01 挂 · 源：`logs/2026-09-01-DVA盲审对账审计与EAL验收核验.md`）**：审计 verdict=FAIL（历史回执 `CC-to-VV-dev19-盲审对账回执-20260814.md` 经盘面实查不存在 · RECEIPT_NOT_FOUND）· 08-28 替代回执已签发（三分结论：historical FAIL / mechanical PASS / blind NOT_FULLY_EVIDENCED · SHA `9006a228…`）· 两处档案引用已修正（outbox README + 对比校正 L141）。**✅ 裁定已落（Doctor 2026-09-01「同意」以 08-28 替代回执关闭 dev/19 · 历史完整性 FAIL 为终态事实）** → 剩 VV/Codex 侧更新 DVA README 关闭状态（CC 不代勾 · 知会件 `4AI/Shake hands/to VV/CC-to-VV-dev19-关闭裁定知会-2026-09-01.md` 已备 · 经 Doctor 转交）。


- [ ] ⚠**〔诊断存疑 · 路径已漂 · 2026-09-29 /todo 现核〕**「不再被 ignore 拦截」这一子断言**与 `.gitignore` 文本相抵**——白泽仓唯一 `.gitignore`（无取反行）含 `*.bak_*`，文本层判该件**仍被命中**；定论须 `git check-ignore -v`（**本席禁 git，未跑**）。**已证成立的部分**：文件确在 `data/archived/stocks_fundamentals.json.bak_20260831_pre_source_fix`（**33,145 B** · ⚠ 原写「32,441 B」有误，那是同目录另一件 `…bak.20260709_025805_tier1v2` 的字节数——承落盘独立复核逮出）· 未跟踪 ✓ · 同仓同类未跟踪恰 **5** 件 ✓。**路径子项已漂**：`build_weekly_report.py.bak_audit20260728` 现实际在 `_bak/`（该目录 09-28 建），非原条写的 `scripts/reports/`。⇒ 剩下仍是**要不要 `git add` 入库**（您定）。**（⚠ 本行原条正文未逐字保留：本轮是「就地加注 ＋ 截断标题」，**非迁档**——改前全文见开工快照 `backups/todo-auto/2026-09-29-1315_TODO.md`；此偏差由落盘独立复核逮出，如实登记。）**



- [ ] **调度 UI 无保留签署缺口（2026-09-03 /todo 漏挂补挂 · 源：同上）**：独立验收方 Claude UI 回读超时——需一次只读回读或下一真实班历史补证。

- [ ] **PEC · 财政主导现象族框架落盘候选（2026-09-03 /todo 漏挂补挂 · 源：`logs/2026-09-01-G08修订与美财政主导十问.md`）**：久期争夺/关税通胀税/Fed 十问三侧面——待 Doctor 勾选落盘。

- [ ] **X-Board · 两条新条目上板销账（2026-09-03 /todo 漏挂补挂 · 源：`logs/2026-08-30-XBoard老毛停更诊断与外发授权.md`）**：回读 artifact 确认两条新条目上板即销账——重推班每日 18:01 PT 在跑 · artifact 目验归 Doctor。

- [ ] **白泽仓 · 既存积压清理（2026-09-03 /todo 漏挂补挂 · 源：`logs/2026-08-31-白泽库例行自查与VVgit桥研究.md`）**：weekly 产物/旧报告删除/3 个旧备份迁移——非上轮范围，留给 09-06 周日班或 Doctor 处置。

- [ ] **治理机制 · VV 知会 codex-brain-* skill 分叉（2026-09-05 /save 挂 · 源：本场经验治理闭环对齐）**：CC 只改了 Claude 侧 canonical/skill/runtime（Doctor 授权范围），`Codex Runtime Kit/skills/codex-brain-consolidate|resume` 副本未动——两侧分叉是授权结果、非漂移；是否知会 VV（时机/措辞）归 Doctor 裁。

- [ ] **PEC · 图谱 v1.1 候选（2026-09-08 挂 · 源：图谱化方案实施场 · PRD open_decisions）**：①macro-facts 结构性事实入图（schema 12 类无 fact 类型 · 需 v0.2 schema 提案：fact 节点类+挂靠边语义）；②facts/ 高时效时序旁路层（对标渊图 prices/）。触发=Doctor 提或 v0.2 schema 提案获批。




- [ ] **DVA · 09-10 班自然验证读 summary + 两个新疑点（2026-09-10 挂 · ERR-20260907-001 验证进展追记）**：① ~~09-10 班验证~~ 被 exit 79 挡停——**✅ 根因已修（09-10 07:19 PT 从 `runtime.bak.20260909-204409` 拷回 `dva_data_gate.py`+`rebuild_global_index.py` · `-DryRun` 全绿实读 · NOTE-20260820-003 第 6 次）· 验证顺延 09-11 17:00 CST 班**——判 finance 臂 exit 0 不再因空数组 FAIL，通过则 ERR-20260907-001 ✅ 按分轨落签：事务性／事实性的由未参与实施的 subagent 代签；方向性的问 Doctor；② cold_dedup audit 未认证 SUCCESS（healthcheck 唯一 blocker · 与 finance 无关）待查；③ Mac `DVA-Database/_health.json` 消失——**✅ 09-10 07:03 PDT 已恢复**（根因=自检脚本手动跑·refresh 替换目录冲掉产物未重跑；CC 沙箱重跑 dva_health.py exit 0 · overall=ok · 8/8 authors · gap 2d · 541B 落盘）；**治本待裁**：refresh 流程末尾嵌入自检（docstring 已预留此意）或挂定时——归 Doctor。

- [ ] **2026-10-02 到期**：确认 Claude Code CLI 无异常后清空 `~/.Trash/claude-versions-20260917/2.1.223`（260M · 旧版本回滚副本）。观察期自 2026-09-17 起 15 天（Doctor 定）。撤回：`mv` 回 `~/.local/share/claude/versions/`。另见 `~/.claude/projects/-Users-lunarabbit/memory/pending-maintenance.md`

- [ ] **ClaudeCode 体检遗留三件（2026-09-17 /todo 漏挂对账补挂 · 源：`logs/2026-09-17-ClaudeCode体检与自动更新报警消除.md`）**：① `~/CLAUDE.md` 的 `## Session Log Checklist` 与 Brain 两份开工清单分处两文件，是否合并归 Doctor 定；② `memory/environment.md` 可能抄了过期的 `Darwin 24.6.0`（~/.claude 下沙箱不可达·未核）；③ `DISABLE_AUTOUPDATER` 对 Cowork 桌面端是否生效未核（桌面端共用 ~/.claude，自更新失败会重写 state 文件、横幅复现）。


- [ ] **EAL · 删除授权死锁修法①已应用·待自然验证（承 NOTE-20260916-001 · 2026-09-18 晚场裁①并当晚应用）**：Doctor 2026-09-18 裁修法①（改班 SKILL 去交互）+ 范围「普查 24 班并修同族」——**已应用并核过**（Doctor 终端 23:09 实跑：store 对拍未滞后 → 备份+cp → 复验 store SHA = staging SHA `88018f86…`/`4b900c32…` → rsync 镜像刷新 → 终封 24 班全 OK；全库 `allow_cowork_file_delete` 实际调用点归零，仅存两句禁令）。staging 归档 `brain/archived/staging_2026-09-18/`。**唯一未闭项＝终验判据**：下一次真实挂载盘 I/O 失败时班应以 fresh attempt 重跑、保留残留、不再卡死（在此之前只算「已改」，不算验过）。同批顺带补回流 `refresh-risk-daily` 镜像（store 侧 09-17 更新漏回流，方向正确无覆盖损失）。预防门禁已登记应升格候选（调度班不动点＝班内零交互，升格归 Doctor）。背景：挂载瞬断 09-15/09-16 连续复发、尚未治。

- [ ] **EAL · gate 验收脚本 PRD 待终验（2026-09-17 /todo Doctor 勾「批」· **2026-09-18 专场已开完**）**：专场已实施——三产物落盘（`eal_gate_check.py` + 判据集 v1 + `test_gate_self.py`）· 判据两处漂移经 Doctor 裁修订后**沙箱实跑 gate 8/8 PASS · exit 0 · self 3/3 绿**；含渊图 promote 第 15 项负向单测持久化（`tests/test_kg_promote_gate15.py` 一次通过 · canonical 字节不变）。PRD `logs/2026-08/checkpoints/2026-08-17_EAL_gate验收脚本_PRD.md` **status=awaiting_acceptance**（§四已核文件本体）。**剩两项归 Doctor/VV**：① Doctor Mac 原生跑同脚本 exit 0（`python3 ~/Documents/Claude/brain/.tools/eal_gate_check.py`）；② VV 审阅判据集 v1 完整性并终验签字。判据集增补流程「首演」素材已由本次两处漂移 + 判据 8 形态变迁提供。

> **漏挂补挂批（2026-09-22 /todo 漏挂对账 · Doctor 裁「全补」· 源：09-16～09-19 五场日志，逐条注明）**——以下 **11 条**此前只留在日志里、从未进 TODO；本轮一次性补挂，后续按各自触发条件推进。（本行为导航头，不计入待办条数）

- [ ] **龙鱼 · 持仓看板 PRD 验收（2026-09-18 挂 · 4 天 · 源：`logs/2026-09-18-龙鱼截图流与DVA金融线实核.md`）**：`logs/checkpoints/2026-09-18_龙鱼持仓看板截图流与手填升级_PRD.md` **status=awaiting_acceptance**（八条交付标准 [?]+证据 · 独立审查「可背书」· LOW 1 条已修 · 首轮三截图真实落库已完成）。**⇒ 2026-09-22 Doctor 裁「龙鱼三件一次办」**——验收与另两件（四只推板 / 常更清单扩面）合并处理，见本段「龙鱼 · 四只补分推板待裁」条。

- [ ] **渊图 · 高盛调研场四条尾（2026-09-18 挂 · 4 天 · 源：`logs/2026-09-18-高盛半导体调研核实与股价归因.md`）**：① 高盛原文 PDF 获取后走 PDF 通道入语料池（`raw/Industrial Analysis pdfs/`，归 Doctor）；② 是否启第六轮收口复验 vs 直接落接受（文件现为「第四轮 PASS_WITH_LIMITS · 修复待复验」）；③ **`prices/` 层是否含天数智芯拆股前后价点、口径是否需 `_caliber_` 标注——本场未核**；④ 壁仞科技 09-14→09-18 超额 +12.59pp 归因未明。

- [ ] ⚠**〔前提已变 · 引用编号已漂 · 2026-09-29 /todo 现核〕**权威声明**已于 09-26 收敛**（`Claude/brain/DVA/GOTCHAS.md` 头部载「权威改判（2026-09-17 Doctor /todo 裁『权威改 Codex 镜像仓』）」＋ `Claude/Projects/DVA/GOTCHAS.md` 头部标「历史副本」）；且本条引的「最新 `ERR-20260911-001`」**已漂移**——Codex 镜像 `GOTCHAS.md`（267,570 B · 09-29 09:59）现至 **`ERR-20260929-002`**，领先 Mac 侧 3 天。**残余一行**：`Claude/brain/DVA/GOTCHAS.md` L35–37「## 权威日志入口」仍写「实时全量坑库：`Projects/DVA/GOTCHAS.md`——一切 BUG/INFRA/RISK 条目以此为准」，与同件头部**自相矛盾**（事务性，可顺手改）。**（⚠ 本行原条正文未逐字保留：本轮是「就地加注 ＋ 截断标题」，**非迁档**——改前全文见开工快照 `backups/todo-auto/2026-09-29-1315_TODO.md`；此偏差由落盘独立复核逮出，如实登记。）**

- [ ] **DVA · Codex 仓提交与 Fuxi staging 残件处置（2026-09-17 挂 · **2026-09-30 解除搁置并现核** · 源：同上日志）**：**⏸ 搁置已解除**——搁置条件（fuxi 回线）于 2026-09-26 实探满足（见本文件「解除（2026-09-26 03:0x PDT 实探 · CC）」段），本场（09-29 夜–09-30）另经 `ssh Codex@192.168.1.32` 实探复核通。**现核三项**：① **Codex 仓 commit+push 已同步**——`refs/heads/main` ＝ `refs/remotes/origin/main`（`a57bd719…`）、`chore/workspace-reconcile-20260719` 亦两端同号（`11392def…`），origin ref mtime 09-29 13:30（末 commit 13:29）；**⚠ 但工作树尚有 273 项 M/D**（`.git/index` 纯文本解析所得，**禁 git 未取权威读数**）⇒ 该子项**未闭**。② **fuxi staging 残件仍在**：`E:\AI\DVA\ops\staging` 实探 **75 个目录**，其中 `*20260917*` **16 个**仍在；`$env:TEMP` 尚有 **2 个** `dva-writer-role-test-*`（1789670610 / 1789670632）。③ Mac 侧 `/private/tmp` 候选包/脚本——沙箱 `/private/tmp` 是 VM 自身，**不可判 ⇒ 未核**。**处置权在您**（fuxi 远端删除与 Codex 仓提交均属禁手）。


- [ ] **两份 EAL PRD 待验收（2026-09-16 挂 · 源：`logs/2026-09-16-EAL星空与adapter迁Mac双线闭环.md` ＋ `logs/2026-09-16-EAL星空预期外视觉迭代与弹窗根治.md` · **2026-09-26 /todo 现核拆分**）**：**① 星空视觉迭代 PRD**（`logs/checkpoints/2026-09-16_EAL星空预期外视觉迭代_PRD.md`）——现核 **`status: delivered`**，§四 **18 ✓ / 4 [?]**；**② adapter 迁 Mac PRD**（`logs/checkpoints/2026-09-15_EAL数据链班adapter迁Mac原生_PRD.md`）——现核 **`status: awaiting_acceptance`**，§四 **3 ✓ / 9 [?]**。原文按「两份同态」记，实为**一 delivered 一 awaiting**。验收落 ✓ 归 Doctor。

- [ ] **治理 · 注入层两条缺口（2026-09-19 挂 · 3 天 · 源：`logs/2026-09-19-签字分轨入Settings与扩键验收.md`）**：① 注入层要不要标「判据系派生」——归 Doctor 裁；② **既有缺口（非本批引入）**：完整源 09-18「审核者 subagent 派发默认允许」条在注入块中 **0 命中**（审核者 F 登记）。

- [ ] **基建 · 5 个非 brain-\* runtime skill 被程序化批量重写、来源未明（2026-09-19 观察 · 3 天 · 同上日志）**：01:05:59 有 5 件（schedule / setup-claude / setup-cowork / consolidate-memory / explain-usage）在 7 毫秒内被批量重写；复核方逐件验过 frontmatter/行数/完整性未见损伤。**观察项，非待办**——再现时再查来源。

- [ ] **龙鱼 · 周更班 SKILL 未含沙箱 env 清单（2026-09-19 挂 · 3 天 · 源：`logs/2026-09-19-龙鱼双scorer周更班.md`）**：任务书 SKILL.md 未列 `LYW_LIB`／`LYW_COMPARE_DIR`／`LYW_TREND_DIR`——待 Doctor 裁是否补（提案制，未动）。

- [ ] **基建 · 两处 skill 的 git 探针文本该改（2026-09-23 /save 挂 · 提案制 · 源：`logs/2026-09-23-五仓提交与探针纠错.md` ＋ 通用教训 G-X83 同日两条追记）**：① `brain-resume` Step 3 现明写「工作区 `find -newermt <末次 commit 时间>` 扫未提交新文件」——**mtime 不是内容的代理**，2026-09-23 实证双向失效（漏报白泽 5 件内容真变 · 把符号链接报成假 dirty）；② `brain-save` Step 5 第 2 步现写「沙箱内则读 `.gitignore` 手判」——同日实证手判漏三条规则、**27 条被 ignore 路径写成命令致 commit 未生成而 push 空转**。建议改为：**内容级比对**（解析 `.git/index` 比对 blob SHA · 配方见 `permanent/经验库.md` `EXP-20260923-001-T`）＋ **ignore 交 `git check-ignore -v`**，沙箱内只报「候选（未过 ignore 判）」。属 skill 源改动（四端发布链），**提案制待 Doctor 批**，CC 未动。

> **漏挂补挂批（2026-09-26 /todo 漏挂对账 · Doctor 裁「全补」· 源：09-19～09-25 七场日志，逐条注明）**——以下 **11 条**此前只留在日志里、从未进 TODO；本轮一次性补挂。（本行为导航头，不计入待办条数）

- [ ] **X-Board · `常更标的审核.html` 入口缺位（2026-09-26 由 /todo 漏挂对账补挂 · 源：`logs/2026-09-22-todo分流·fuxi搁置与龙鱼三件.md`）**：周更班 SKILL 与 08-26 裁定均称「常更清单由 `常更标的审核.html` 维护」，但**全盘 find 零命中**——不在龙鱼库、不在 Projects、不在 brain；而 `常更标的.json` 已 count=30（09-22 更新）。⇒ 维护入口的实际位置/存废待核。


- [x] ~~**渊图 · `data_vintage` 是否增设「底层报告日期」字段**~~ **前提失效（2026-09-29 /todo 现核）**：**已有裁定且已落盘**——`Database/行业研究/CLAUDE.md` **L141** 起「## provenance 时点规范（**2026-09-19 Doctor 立**）」（⚠ 原写 L142，承落盘独立复核订正为 **L141**）明写**改规约、不增设 schema 字段**（reference 必写「来源方, 原报告日期」＋ `provenance_kind:"cite"`；不可得标「日期未核」；存量不强制回填）；canonical 三节点已按此补 `摩根士丹利, 2026-05-20`·cite ⇒ 原条的「增设字段」路线**已被否**。**残余**：`NOTE-20260718-002` 的升格（见 `brain/渊图/GOTCHAS.md` 该条状态行 —— ⚠ 原写「见下条 L191 面」是**悬空行引用**，承落盘独立复核逮出后改为内容指代）。（⚠ **原条正文未迁入归档件**——本轮系「就地作废 ＋ 删正文」，**故此处不写「原条保留于归档件」**（原写该句为**假**，承落盘独立复核逮出）；改前全文见开工快照 `backups/todo-auto/2026-09-29-1315_TODO.md`。）

- [ ] **渊图 · `NOTE-20260718-002` 追记状态行更新（2026-09-26 由 /todo 漏挂对账补挂 · 源：同上）**：promote 后应可推进其状态行（`brain/渊图/GOTCHAS.md` L517 段）。**不代签 ✅**，归 Doctor/指定验收方。


- [ ] **巡检 · 面③ `unknown` 判红盲区（2026-09-26 由 /todo 漏挂对账补挂 · 源：`logs/2026-09-22-巡检补盲与行情链共模修复.md`）**：`classify_machine_state()` 读 pmset 事件史，但 **pmset 日志滚动窗口外的历史取不到 → `unknown` → 判红**（可能噪音）；「睡眠 vs 关机」在窗口边缘亦可能混判。修法方向：窗口外降级为「不可判定但非红」或扩读 `system.log`——随第三轮独立复验一并看，归 Doctor 裁。

- [ ] ⚠**〔「已消」已被盘面反超 · 2026-09-29 /todo 现核当场重取〕**：现读该仓 **`M=6`**（`risk-daily.html` · `ai_kill_history.jsonl` · `latest-envelope.json` · `risk_snapshot.json` · `taco_components.db` · `fomc_market_exp.json`，mtime 全为 2026-09-29 09:09–09:11）· `D=0` · **未跟踪非 ignore 候选 4**（`data/envelopes/2026-09-26…29.envelope.json`，其中 **09-26/09-27 两封未随末次提交入库**）；**HEAD 已从 `c84768bc` 前进到 `3d5141da`**（末次＝「R 陈旧护栏注释订正＋当日班产物刷新」）；`.git/config` **无远端** ✓（本地-only 依旧）。⇒ 原「现核已消」的判断**触发条件已达**，属**日更节奏**而非积压（保留本行作触发式观察）。** **风险日报仓 · 12 改 + 8 未跟踪该场未处理，属其**日更节奏**而非积压。本场实读该仓 HEAD=`c84768bc`、无远端（Doctor 裁定本地-only）、**M=0 · D=0 · 未跟踪候选 0** ⇒ 已被后续班次/提交消化。保留一行留痕（触发=再现时再查）。

- [x] ~~**DVA · `_health.json` 缺位**~~ **前提失效（2026-09-29 /todo 现核）**：该文件**在场**——`Database/Douyin/DVA-Database/_health.json`（534 B · generated `2026-09-26T04:21:42-07:00` · overall ok · 8 作者/1 失败）；`海螺姑娘/data/asset_manifest.json` 的 DVA-Database 项 `status:"healthy"`、freshness「自检 ok·全表一致·2026-09-26T04:21」、last_scan 2026-09-29 ⇒ **已补齐并被 GAI 看板点亮**。原条「conch 班连续两轮报 `update_health` 5≠6」的解释＝登记当日 04:21 之后被会话 `zen-tender-cori` 补跑。（⚠ **原条正文未迁入归档件**——本轮系「就地作废 ＋ 删正文」，**故此处不写「原条保留于归档件」**（原写该句为**假**，承落盘独立复核逮出）；改前全文见开工快照 `backups/todo-auto/2026-09-29-1315_TODO.md`。）


- [ ] **白泽 · `.gitignore` 两条「过程产物」规则是否维持（2026-09-26 由 /todo 漏挂对账补挂 · 源：同上）**：09-23 那场反而证明这两条是**有效护栏**（替我挡下 27 条误入 add 清单）。现核实读两条仍在（`data/weekly/web_fill_*.csv` · `scripts/reports/v4.1 业务汇总版/白泽大宗完整分析报告_*.md`）。⇒ 是否维持归 Doctor 裁（CC 倾向维持）。

- [ ] **PEC · 审计修复轮收尾（2026-09-29 挂 · 源：`logs/2026-09-29-PEC审计修复轮与错题本治理.md` ＋ `AI4ME/PEC审计报告_2026-09-29.md` · 承 `G-37`）**：**P0 波全完 · P1 约 30/53**。**剩四项**：① ✅ **P1 余项 —— 已于同日执行并复核完毕（订正注 · 2026-09-29 11:3x）**：本条原列 **25** 条（原写「约 24 条」，**枚举实为 25**——G-40 同族的计数病，已订正）已随 **P1 批**（commit `4fe45c01`）＋ **修正轮**（`94741d0a`）落地，并进入复验射程：`_复验_P1批_PEC侧_2026-09-29.md` 逐条核 **15/15 在场**、其余 10 条由 `_P1批_修正轮_独立复验.md`（9 条主张）与 `…_修正轮二_窄口径复核.md`（5 处）覆盖，**本子项可销**。原列（留痕）：A-10 · A-13 · A-14 · A-15 · A-19 · A-21 · A-24 · B-10 · B-18 · B-19 · B-21 · B-22 · D-03 · D-04 · D-06 · D-07 · D-08 · D-09 · D-10 · D-11 · D-13 · D-15 · D-17 · E-03 · E-10 —— **⚠ D 族中咬 P2 裁定者（D-02 真源 · D-06 版本表）须先看裁定落点再动**；**且审计给的行号在六件上已全面失效**（实例：按 `门禁:30` grep `审议链` **零命中**，不是已修而是漂了），**每条须先重定位**。**⚠ 真正未认领的残余只有两条**：**`D-14`**（盘上从未修 · 见 `G-40`）与 **`B-11`**（孤儿 · 见 `G-40`）。② ~~**独立复验（P0＋P1 · 抽核 ≥20% 且含全部 🔴）**——实施者不自签，须**未参与实施**的 subagent。~~ ⇒ **2026-09-29 11:3x 全部完成（本场核销）**：**P1 侧**原已由 **4 份**未参与实施的独立报告覆盖（`Projects/PEC/_复验_P1批_PEC侧_2026-09-29.md`＝PEC 侧 **15 件全量**、逐件对 `.git` 父提交 blob 验基线 · `brain/logs/checkups/2026-09-29_P1批_brain星空侧_独立复验.md` · `…_P1批_修正轮_独立复验.md` · `…_P1批_修正轮二_窄口径复核.md`）——**故本条的真正缺口只有 P0 波**；本场补验 → `brain/logs/checkups/2026-09-29_P0波_独立复验.md`，判 **`PASS_WITH_LIMITS`**（零伪修复 · 四台校验器 exit 0 · **全 7 🔴 现核均闭合** · `.bak` 基线经 zlib 直读 `.git` 自证为真改前态 · **P0-8 的因果声称在 `mktemp` 隔离副本内被可决定性重放**：改前／改后 builder 产物 sha256 同值）＋ **10 条发现**。**其中三条须认领**：**`D-14`** 被写进「仍开已修」而**盘上从未修**（`GOTCHAS.md:1117` 与 `文明基因/沿革/文明基因现状与门禁.md:71` 仍写 `G-01…G-30`，现最大号 G-39）· 审计 **`P0-3` 整步消失**、其 `B-11` 残留仍在（`brain/logs/checkpoints/2026-09-29_文明基因三段重走_PRD.md:158` 仍写「`CS-02`／`CS-03`／`CS-08` 未开」）**且不在任何残余清单 ⇒ 孤儿** · 两处**现行**件仍写「唯一剩余 L3 候选 · 待 `CS-04` 亚美尼亚验证」（`可视化数据集/B1_F框架体系树_v1.0.json:86` · `整合数据集_v1.0.json:3327`）。**已按预授权登记**：`Projects/PEC/GOTCHAS.md` **新条 `G-40`**（修复批覆盖面无人对账）＋ **`G-38` 追记**（同根第四例：批自述的 `5／6` 与枚举 `6／7` 不符、「13 处」枚举实 18、INDEX 四／六处互斥、`raw/` 两件实 1 件）。**⇒ 2026-09-29 12:2x：修正轮已完成**（10 条发现的**事务性子集** · 累计 **编辑动作 23 次 / 受影响 10 件**（**只给两个可核数**：10 件＝`.bak_fix_2026-09-29` 全树计数（可数）；23 次＝实施者自记的**编辑动作**数（非盘面量）；**⛔ 不给「总处数／hunk 数」——口径未定；本日同类复发四例**（`18` 合计含读法假设〔一轮 `L-4`〕· `≠13 不随读法变` 被击穿〔三轮 `L3-1`〕· `19` 手写未复核〔自查〕· `净 hunk 21` 未复算〔自查〕）） · 独立复验**四轮**（含末批极窄核）全 `PASS_WITH_LIMITS`：`brain/logs/checkups/2026-09-29_修正轮P0发现_独立复验.md` · `…_修正轮二轮_窄口径复验.md` · `…_修正轮三轮_末核.md` · `…_修正轮末批_极窄核.md`；**末批之后再做的收窄系「只删绝对句、未新增断言」，仅自验**（实施者声明不再加句）；**唯一不可核项**：`TODO.md` 无 `.bak`，其本批改前态不可复原（末批 `L4-2`，**永久限项、如实登记**））。**残余（归您裁）**：`D-14` 的「同族第二次／第三次」**计数口径** · `B-11` 归口 · 审计剩余未修项。**⚠ 并行场（发声系统切 eleven_v4 线）同在本仓且均未提交——提交只能逐文件 add，禁 `-A`。**③ ✅ **P2 二十二项 —— 已于 2026-09-29 当日执行完毕**（**订正注 · 2026-09-29 11:3x**：本子项写于 07:3x 的当时态，其后同日已由 Doctor 问答板一次裁定〔答案串 22 题全取推荐〕并由修复轮执行完，跨 15 件 canonical、四轮独立复验；**残余只剩两项，改挂本文件「PEC · P2 收口残余」条**）。原列：**P2 二十二项裁定未执行**（B1 表迁 `§七` · 归类别目迁 `§2.0（六）` · 星云 `label_tech` 回写 38 处 · 整合数据集改脚本拼装＋回写 27 处 · builder/QA 时钟 · 旧图冻结宣告 · INDEX 补表 v2.39–v2.48 · GOTCHAS 真源改裁 · G-28 补正文条 …）——**建议另开一场并立 PRD**。④ **P3 九项**（原七 ＋ 本波新增两项：**经验索引生成器改读各项目真源**〔含真源声明表 ＋ **PEC 解析器** ＋ 围栏负向测试；**门槛＝干跑核覆盖 ≥37/37 且标题干净才许上线**〕· **闸从「按本载 L2」改「按条载 L2」**〔brain-anchors 三端〕）。**`G-37` 状态仍 🔄 待修复。**
- [ ] **【挂您名下】隔离区两条旧运行层目录处置（2026-09-29 由 /todo 漏挂对账补挂 · 源：`logs/2026-09-26-分轨改写与问答板改名QA.md`）**：`~/Library/Application Support/Claude-3p/skill-quarantine-20260926/` 两条目录，处置权在 Doctor（沙箱外）。
- [ ] **PEC · 总纲版本号冻结（2026-09-29 由 /todo 漏挂对账补挂 · 源：`logs/2026-09-28-文明基因系统收敛与判据层整合.md`）**：判据件「一夜改七轮，外面已有引用」⇒ **版本号该冻**；是否冻、冻在哪个版本，归 Doctor。
- [ ] **基建 · 探针脚本自身出错四次（2026-09-29 由 /todo 漏挂对账补挂 · 源：`logs/2026-09-28-消费回执未闭集合清账.md`）**：SQL 语法 · 漏路径前缀 · 列数比错 · 误读未跟踪件——**与「事实出错」表现完全相同，尚无任何机制区分**。（可考虑：探针脚本的**自检断言**或**双跑对拍**。）
- [ ] **基建 · 5 件更早批次备份从未入册（2026-09-29 由 /todo 漏挂对账补挂 · 源：同上）**：09-26 ×3 · 09-27 ×2 的批次备份**未登记进任何 index**；与「备份件处置」同批议。
- [ ] **基建 · E 路 `Write` 被 harness 拒而 A–D 未被拒（2026-09-29 由 /todo 漏挂对账补挂 · 源：`logs/2026-09-29-发声系统切eleven_v4.md`）**：同 harness、同目标目录，仅 E 路被拒，**原因未查**。
- [ ] **PEC · 三小件（2026-09-29 由 /todo 漏挂对账补挂 · 源：`logs/2026-09-29-PEC目录分类重组与可视化清查.md` ＋ `…-PEC架构优化与skill四端发布.md` ＋ `…-发声系统切eleven_v4.md`）**：① **`专题研究/` 名字系 CC 自定**——`日本线脉络_…` 若判其应归 `case-studies/CS-08_大和-日本文明/`，一句话可撤；② **`_迁移清单_20260929.md` 仍在 PEC 根**（工作件非 canonical）——**去向未定**；③ **`临时文件/` 残留 3 个 mp3**（另一场 resume 起手声 1 ＋ xboard 2）——按「朗读文件不落盘」宜清（**非本场生成，未动**）。

- [ ] **PEC · 09-28/09-29 场遗留漏挂批（2026-09-30 /todo 漏挂对账补挂 · 源：`logs/2026-09-28-文明基因判据收敛与子项目迁移.md` · `logs/2026-09-28-文明基因台账收敛与判据面重划.md` · `logs/2026-09-29-PEC图谱链收口与文明基因三段重走.md` · `logs/2026-09-29-PEC目录分类重组与可视化清查.md` · `logs/2026-09-29-PEC架构优化与skill四端发布.md`）**：以下各项**此前只留在日志里、TODO 与归档两处 grep 皆零命中**，一次性补挂（PEC 线另有「审计修复轮收尾」「D4 重跑」两条在册，本批为独立小项）：
  ① **子项目「🔒 收尾条件」待审 7 条**（A 类未复验 3 批 · B 类…）；
  ② **坐标根因未除**：主件内其余外部引用（审核者列出的后若干处）未同步；
  ③ **台账结构重整未落盘**：28 行含 4 行混装（`#16`／`#19`／`#20` 等）；
  ④ **`a.5` 定位**（判据 vs 非判据·记录项背景；**已收窄为二选一**）；
  ⑤ **「归档是否重启」**（等 `G-33` 修法）；
  ⑥ **T2 池内名单 v1 合成**（并集起步、不预设上限）；
  ⑦ **`T7`**：`CS-09_伊斯兰文明_文明基因清单.md` §一「元层」措辞待改；
  ⑧ **`G-35` / `G-36` 待独立复验**（`G-35` 🔄 已收口「已修改·自验结果·待独立验收」· `G-36` 🔄 已修待验；`✅` 按分轨走）。
  **⚠ 其中 ④⑤⑧ 系方向性/待签，归您；①②③⑥⑦ 属事务性。**

- [ ] **基建 · 09-28/09-29 场遗留漏挂批（2026-09-30 /todo 漏挂对账补挂 · 源：`logs/2026-09-28-消费回执未闭集合清账.md` · `logs/2026-09-28-文明基因系统收敛与判据层整合.md` · `logs/2026-09-29-PEC架构优化与skill四端发布.md` · `logs/2026-09-29-PEC完整审计与审计报告.md`）**：
  ① **`brain-consolidate` Step 6.5 写侧口径缺管辖**（其自述的写侧规则与 `_consumption_receipts.jsonl` 的**实际结算语义**未对齐——本场 Step 3.5 实测仍见结算行/修正行的口径分歧）；
  ② **`GOTCHAS.md:1263`（已签 R5 行）现存疑**：其关于 `graph-data.js` 的断言待复核；
  ③ **清账三条残差**：`STL-005` **顶替 `L73`** 的编号错位 · `L103` 台账项 · 第三项源日志未列全**须回读**；
  ④ **`make_commit_block.py` 无条件附 push**——而**风险日报仓无 remote**（Doctor 裁定本地-only）⇒ 该脚本对无远端仓会产出**跑不通的命令**；
  ⑤ **TCC 探针真机首考**：等 `scheduler_snapshot.py` 下次 Mac 原生跑（与 `permanent/_repair_audit.md` L33 同源，该行现仍 🔄）。

- [ ] **EAL · `engine.py.bak_preSOX_20260905` 待搬（2026-09-30 /todo 漏挂对账补挂 · 源：`logs/2026-09-28-文明基因判据收敛与子项目迁移.md`）**：该件在 `EAL/backtest/eal_v3/` 内，需搬离；**该目录有防写锁**（解锁 → 改 → 锁回），属 **Doctor 终端动作**。

- [ ] **基建 · Cowork 壳 ElevenLabs 条目无 MODEL 键（2026-09-30 /todo 漏挂对账补挂 · 源：`logs/2026-09-29-发声系统切eleven_v4.md`）**：本壳（Claude-3p）配置 `mcpServers.ElevenLabs` 的 `args` 串内**已含** `ELEVENLABS_MODEL_ID=eleven_v4`；而 **Cowork 壳配置实读「有 ElevenLabs 条目但无 MODEL 键」**——是否一并切 v4，归您裁（属授权面外，CC 未动）。

## 长期观察

> 纯等待 / 观察 / 暂缓 / 数据积累中——**不删、仍跟踪、不占「待办」计数**；触发条件成熟即回捞进待办。（2026-08-11 目标模式 Doctor 裁定建区 · 13 条自待办移入 + 1 条漏挂新挂 · 2026-08-26 /todo 归位：08-22 批发 5 条活跃待办移回待办段，观察 23 条随标题归位）

- [ ] **PEC · 十站清单实战首验（2026-09-01 /todo 漏挂对账补挂 · 2026-09-17 /todo Doctor 勾「移观察区」 · 源：`logs/2026-08-26-PEC专项学习与十站命令.md`）**：下次命题推演走一遍，检验场合分层执行一致性。触发=下一次 PEC 命题推演时自走。

- [ ] **龙鱼 · 曦智 01879.HK 买点信号观察（2026-08-23 挂 · Doctor 裁「放常更标的持续观察」 · 源：本场曦智产业地位四连问）**：定论「有实证的局部硬技术 + 执行力不弱的薄规模 + 行权价在外、有到期日的深虚值期权」；现价 309.2 **无买点**（PS ~90x 推算 · 对首日 886 是 -65.1% · 对中金目标价 362 是 -14.6%）。**触发回捞（任一即回）**：① 谷歌/头部云 per-job 动态重配产业化证据（论文/博客/供应商公告）；② 华为 OCS 整机放开卖明牌；③ 大客户结构健康化（前五大 78.9% 集中度下降/名单披露）；④ 收入拐点（季度 Scale-up 收入环比不塌且客户分散）。**dated 时点**：2026-10-28 基石解禁（897 万股/11.68% · 大股东解禁日期待核）——解禁后止跌＝压价腿为主，破位＝叙事腿权重升。**价格锚**：发行价 183.2 / 首日 886 / 08-23 报 309.2。近端触发器：今晚 22:01 PT 班首打分 + 周一班后核双腿（已挂待办条）。**09-10 深挖注记（Doctor 令）**：09-07 纳入港股通生效（上市仅 4 个月 · 稀缺 Scale-up 光互连标的）→ 成交额中枢从 8 月 ~0.3-0.6亿/日 抬至 2-6亿/日（5-10 倍 · 结构性流动性）；09-09 天量脉冲（+19.2% · 161 万股 · 6.0 亿港元 · 盘中 401）直接催化=09-08 夜美股光通信大涨（Lumentum+11%/Coherent+7.1%）+ 高通×亚马逊 1.6T 光连接；三段结构=入通预期提前炒作（09-03/04 放量）→ 生效日 sell-the-news（09-07 高开 400 收 337 跌 10.9%）→ 消息面二次点火（09-09）→ 09-10 回吐 -6.7% 净流出；H1 营收 7978 万 +284%/毛利率 65.8%/现金 28.6 亿。南向持股明细 hk_hold 未核到（数据缺）。近端风险=10-28 基石解禁 897 万股/11.68% 临近 + PS 仍 ~100x 级（推算）。**观察窗三层框架（09-10 定 · /save 分拣 C 落盘）**：① 路线级生态事件=主窗——scale-up 光互连采纳信号（谷歌 per-job 重配扩展 / 超节点级 OCS 产业采纳 / 华为 OCS 整机用途走向；scale-out 的 OCS 事件对曦智期权意义弱）；② 公司级技术/订单事件=验证窗（频率低·出现即重大）；③ 代理信号层=A 股 OCS 供应链（光库/天孚/仕佳）先行定价可当前哨；④ 可盯点=OCP OCS 控制接口标准化进展；⑤ 反证信号=头部云明确选 CPO 做 scale-up（挤压 OCS 期权）。细分锚收窄发生时（CPO vs OCS 分化事件）=观察窗拐点而非买点信号，买点仍归原四条件。**09-10 FCC 追记（/save 分拣）**：FCC 设备授权供应链最终规则落地未列光模块——旭创/新易盛/天孚未入 Covered List（8 月路透点名未落地）→ 光通信主题情绪利好，不进六维、不 lift 买点四条件；观察点：09-21 FNPRM 回复意见截止 · 10 月中下旬生效满月前后清单是否调整 · 第三轮提案（全组件+HBOM/SBOM 溯源）若落地对 OCS 供应链合规成本的影响。

- [ ] **白泽观星 · Δp_hike 事前窗方向一致性观察（2026-08-14 挂 · BT-19 结论档预注册观察）**：四腿×两窗 8/8 正 + T2 不坍缩，但闸3 置换 p=0.502 不过闸。**触发回捞**：样本更厚（2010+ 扩窗）或引擎迭代（cut 腿阈值/信号结构修复）后重跑四闸；若 Δp_hike 届时仍 8/8 且过置换闸 → 重新谈转正。依据：`Projects/Financial/白泽观星/reports/BT-19_四闸准入结论.md` 转正建议段 · `剑酒青丘/回测报告/2026-08-14_综合_观星转正评估.md` §三/§四。

- [ ] **brain · 系统概览缺口剩 5 份（2026-07-31 挂 · 收窄 2026-08-14 问答板 Q3A）**：烛照九阴/风险日报/剑酒青丘 3 份已补（08-13 在盘）；剩 MiroFish/数灵转移/星空/称象 4 份（白泽大宗概览已在盘 · 2026-09-01 /todo 现核剔除）——随各项目下次实质推进时顺带补。

- [ ] **风险日报 · C1 回测（2026-07-27 挂 · 2026-08-14 问答板 Q2A 移入）**：08-13 问答板裁「暂缓」——数据 fetch（解禁/定增日历·FOMC 日历·OMO 净投放·BZ=F 2010+ 回补）齐后开专场（含 harness 重写）；④⑤ 注记已落地部分保持。

- [ ] ⏸**【fuxi 侧清理 · 搁置至 2026-09-26】** **DVA · data.first-round-20260724 观察期后清理（2026-07-24 挂 · 收窄 2026-08-14 问答板 Q1A）**：旅行模式两件已全收口（快照回流 08-13 验收 + FROZEN 08-11 改写）；仅剩 fuxi 侧 first-round 数据包观察期后清理。

- [ ] **基建 · 看门狗挂载授权固化（2026-08-09 挂 · 2026-08-14 问答板 Q5B 暂缓移入）**：08-13 问答板裁「开专场查授权固化」——因 Gateway store 沙箱不可读，需 Doctor 侧配合查机制；暂缓，触发=挂载类阻塞再发或 Doctor 提起。

- [ ] **风险日报 · 成交额定源 2020+ 切 volume_trillion（2026-08-11 挂 · 2026-08-14 问答板 Q5B 暂缓移入）**：08-13 问答板已裁方向（2020+ 窗口分位/回测切 volume_trillion）——待挂载 Market-Data + 方法论复审后执行；触发=挂载就绪。**注记（2026-08-15 .bak 批次侦察补）**：`Database/Market-Data/` 下有 08-08 volume 动作手工快照两件——`market_data.db.bak_20260808_volume`（268.9MB）+ `MANIFEST.md.bak_20260808`（8.7KB）——非 git 仓、Doctor 裁定留到本条执行时一并处置（该条当前唯一既有底账）。

- [ ] **烛照九阴 · 手机卡范式固化进每日生成器（2026-08-14 补挂 · 问答板 Q7A 挂起）**：手机卡字号/字体/三列式/fit 范式已定稿落决策记录；生成器（gen_daily_report.py 卡片段）未实现——触发=生成器下次改动时顺带。

- [ ] **渊图 · FCC 光模块 Covered List 正式文本跟踪（2026-08-08 挂 · 入库裁定触发器）**：盯草案转正式文本三件事——「新型号」界定是否含 1.6T、实体认定（company-based）还是产地、有无过渡期/分阶段条款。文本落地即决：① 是否以 hedged（stage=reported/announced·P1）入「美国对华光模块准入限制」事件节点 + 与 1260H/Covered List 机制连边；② 札记「泰国=时间缓冲（一至三年）」判定证实/证伪；③ 中信「传闻版本落地概率偏低」是否重估。配套跟踪见札记 §7 共 9 条（9月中美AI对话 / Coherent·Lumentum·Fabrinet capex / 铟出口许可对美口径 / 旭创 TeraHop 进展等）。**⇒ 2026-08-19 旁线升级**：FCC 已于 07-28 把「先进机器人设备」（人形/四足/移动机器人整机）列入 Covered List 即时生效（已认证型号豁免·软件更新至 2029-01-01·零部件不在范围）——核实札记 `raw/核实/2026-08-19-FCC机器人禁令与特斯拉链供应商影响核实札记.md`（三花/拓普/绿的谐波无直接冲击·跟踪触发器=零部件扩展/原产地收紧）；机器人线已先于光模块线踩进 Covered List，光模块草案走向可参照此路径。
  依据：`Database/行业研究/raw/核实/2026-08-08-高盛1.6T上修与美国FCC限制传闻核实札记.md` §5/§7 · `logs/2026-08-08-渊图光模块双讯核实与对冲定性.md`

- [ ] **触发层 F4/F5 仍 sub-threshold（五因结案留尾）**（2026-07-23 挂 · 低优先 · 承上条结案）
  五因两层重构后，环境层 A6/B6 已加固共振，但**触发层仍只有 F4(4 独立事件)/F5(9 独立事件) 两个 sub-threshold 因子**，均未过 20 事件门槛——「仅 F4 有意义」的病根是**用共振层缓解、非触发层根治**。无需主动挖数，随行情自然积事件；等 F4/F5 任一过 20 事件门槛后重跑校准复核，或出现新的强机理触发候选时再议。

- [ ] **烛照九阴 · 情绪周期四季「提前发现」能力改造 → 等标注积累（2026-07-30 挂 · Doctor 定「引擎肯定要改，但改之前得先攒够数据/标注」）**
  **现状**：`tools/emotion_engine_v2.py` 的四季判定是**当日即出、无确认期**的同步读数，前瞻部件只有三个且都弱——`hint` 倾向（夏×高位→秋风险积累中 / 冬×极寒后→春机会孕育中）· 火热点（夏×分位≥80，命中 42%、中位先行 6.5 日）· 极寒（命中 75% 但**中位距离 0 日＝完全同步、零提前量**）。
  **已就位**：`docs/情绪周期_人工标注.tsv`（2026-07-30 立）——记 Doctor 人工判定的**市场反转日**（事件点，非季节；反转日 ≠ 季节起点），每条带标注当日引擎读数快照（season/cycle/score/level_pct/trend/**hint**）作评测基线。**引擎不读该文件**（叠加层已回退、代码零改动），纯真值标签仓。
  **首条样本**：`20260730 · reversal · up`（见底反转向上）——引擎当日读数「秋·cycle15」且 **hint 为空＝无任何预警**。Doctor 的机理依据（已入 `rationale` 列）＝**科技股跟随美股出清 + 知名基金爆仓（出清较彻底）+ 7.29 美股夜盘反转 → 7.30 A股跟随见底反转**。
  **⚠ 首条就暴露了方向性问题**：这三个依据**全在引擎输入之外**——八成分只吃 A股内部量价（晋级率/次日溢价/涨跌停/涨跌比/主线宽度/成交额/连板高度），**既无外盘腿、也无强制出清·杠杆爆仓腿**。所以引擎不是「算错」而是「看不见」。若样本反复指向同一缺口，改造方向可能不是调阈值/状态机，而是**补成分（外盘传导 + 出清烈度）**——但这需要标注积累来证实，现在只是一条 n=1 的观察，不作定论。
  **触发条件**：标注攒到可评测规模后（n 门槛待定，参考回测准入 20 事件门槛），写独立评测脚本算「引擎在真实反转前 N 天是否报过信号」→ 有了提前量基线才谈改判定。**在此之前不动引擎判定标准**（Doctor 定）。
  **下一步**：① 每次人工识别到反转日就追一行——`python3 tools/mark_reversal.py --date YYYYMMDD --direction up|down|unknown --rationale "…"`（2026-07-30 立·Doctor 授权 CC 定夺；自动抓 engine_* 快照钉死基线，重复日/非交易日会拒，落盘前留 .bak；回填确认 `--set-confirmed DATE 已确认|已证伪`）；② 攒够后立评测 PRD。

- [ ] **工作流值守 · 取数链路三件（2026-07-30 从当日三场日志补挂）**
  ① **us_anchor ×19 工作流值守**：沙箱 `web_fetch` 对 Yahoo chart 返回**空体**（Chrome 桥未连时无退路）→ 断供风险已入 GOTCHAS；若持续，改「构造 curl 命令交 Doctor 终端」方案固化进流程。
  ② ~~**us_anchor 手工 fetch 补 SPY 决定日反应**（滞后 2 天）~~ → **✅ 已完成（2026-08-08 /todo 现核 · Doctor 勾定，CC 代记留痕）**：`us_anchor_daily` MAX(trade_date)=20260807、7,500 行，已追平，无需手工补。
  ③ **TACO 复刻 3/6 掉线查因**。

- [ ] **烛照九阴 · `conviction` 回填未收口（2026-07-30 挂于日志 · 2026-07-31 补挂 TODO）**：`dim4_stock_analysis` ~~缺 13 个交易日~~ **日期缺口已收窄为 2 天（`07-03` / `07-10`）＋ conviction 空 99 行**（2026-08-08 /todo 现核 recap.db：总 499 行，原 13 天已回填 11 天）。手术方仍在进行，CC 未介入。

- [ ] **烛照九阴 · 07-30 晚间两轮写库无日志（2026-07-30 挂于日志 · 2026-07-31 补挂 TODO · 2026-08-03 /todo 收窄）**：21:35（两日入库）与 22:02（`hot_sectors` 回填 +241）**两事件当日日志仍无认领**（行情日志 0 命中已核）。~~课件入库日志记 `recap_daily=190` 而**实测 192**~~ → **此指控不实（2026-08-03 /todo 核）**：课件日志 L103 明记「recap_daily 190→192」、L105 记放回成功，首尾两态都在。待相关会话补记两事件。

- [ ] **EAL · 提案裁定队列（2026-08-08 由 /todo 漏挂对账补挂 · 源：`logs/2026-08-04-事件归因台账美化与v1.2入册.md` ＋ `logs/2026-08-06-回测库建成移交VV与台账v1.3.1闭合.md` · Doctor 2026-08-08 定：P 系列留周末专场）**：① ~~**P-20**（geo·降温兑现 VIX 分项第二样本违例 · 三选一：加水平条件／◌不可分离／回炉——裁前该因子暂停归因资格、记账行标 ◌）~~ **✅ ① 收口（Doctor 2026-08-11 /todo 统一授权勾定，CC 代记留痕）**：P-20 已裁选项一并落盘——台账 geo·降温兑现签名行实证「VIX 分项加水平条件（v1.2.1·P-20 选项一·Doctor 裁）」。② ~~**P-21**（宏观数据/贴现率腿立项——2-E 触发线已达）~~ **✅ ② 收口（同上）**：P-21 已裁 C 案并入册——台账实证「宏观驱动（v1.3·P-21 新设因子位·Doctor 裁 C 案）」+ §六 2-E 卡「三个遗漏因子全部入册」。③ ~~**P-22**（宏观驱动 @数据落地 股票腿通道归属 · 三选一：方向不定只锚量级／regime 子句／维持原签名记变体——08-07 NFP 首测已记证伪样本）~~ **✅ 收口（2026-08-12 /todo Doctor 裁①「股票腿方向不定」· CC 代记留痕）**：台账 v1.3.2 已落——@数据落地 股票腿改「方向不定·只锚量级·长端方向作通道判别器」；08-07 NFP 样本维持证伪样本留档、宏观驱动继续 n=0④ **量级带裁定**（六空带·须再攒 1-2 个独立事件轮，退款/降温各仅 1 轮——被数据积累阻塞）⑤ ~~台账 artifact v1.3.1/v2.8 渲染目验（artifact 08-07 19:34 PDT 已重绘 · 待 Doctor 目验）~~ **✅ ⑤ 收口（2026-08-11 Doctor 目验通过 · 口头勾定「球在我这的现在都做了」，CC 代记留痕）**；⑥ 封档观察：VIX/^TNX 数据源升档（Polygon Advanced/Indices）再议——当前封档。~~Kospi 笔误订正~~（**2026-08-08 Doctor 准，已改 2-C 原文 6,695.45→6,595.45**）· ~~斜纹区是否还原~~（**2026-08-08 Doctor 确认：不还原，退役定案**）。08-04 补数 curl ×4 大部已被值守班闭合或过时，作废不挂。

- [ ] **龙鱼 3 件（2026-08-08 由 /todo 漏挂对账补挂 · 源：`logs/2026-08-06-龙鱼白泽双库修复与空analyses审计.md`）**：① 真实浏览器目验龙鱼看板（泡泡玛特卡片/排序/弹窗/移动端——reviewer 认领，可随时开）② **氦气/六氟化钨 价格锚点仍过期**（⇒ 2026-08-10 /todo 现核收窄：`_health.json` 08-09 补跑产物——稀土/原油已鲜价；氦气 asof 04-16·115 天、六氟化钨 asof 06-12·58 天仍 stale，原「四品种」收窄为两品种）**⇒ ② 收口（Doctor 2026-08-11 /todo 统一授权勾定，CC 代记留痕）**：08-11 04:42 PDT commit `e3ef974` 落「氦气换卓创全国均价 919.64 + WF6 转 EVENT_DRIVEN 45 天阈」——现核 `_health.json`（08-11 生成）：氦气 asof 08-11·age 0、WF6 asof 07-14·28 天阈内；遗留小尾=WF6 07-14 为弱源待校。父条留 ①浏览器目验 ③泡泡玛特六维。③ 泡泡玛特六维研究（待研究标记，排期未定）。

- [ ] **EAL · v6 分层抽样重跑 4,136 + CC 交叉核对（2026-08-08 挂 · ⇒ VV 08-13 完成 4,136/4,136（v6.1 修 fragilityNote·37/37 测试）；CC 已交叉核对（313 mech vs 169 theme·重叠139·两口径自洽·报告落 mech-watch） · 源：`logs/2026-08-08-EAL口径v0.1收官.md`）**：（VV 侧）v6 分层抽样＋人工复核 → 正式重跑 4,136 条；其后 CC 交叉核对。口径 v0.1 收官后的正式验证步，活跃工作流，不挂易滑出视野。

- [ ] **渊图 · InP 专项遗留包（2026-08-09 由 /todo 漏挂对账补挂 · 源：`logs/2026-08-08-InP投资推演与源杰深析.md` ＋ `logs/2026-08-08-渊图InP衬底专项研究.md`）**：① ~~专项 7 条入库建议~~（✅ 2026-08-09 入库完成 · Doctor 勾定，CC 代记留痕 · 证据：commit `0961ad7`，图 0新/4更新/3边 + 价格层+3，canonical 3928/4429；原「Doctor 已定暂不入库」旧裁定已由 Doctor 本会话改判「入库，做」）；② ~~图内零度孤儿节点挂边~~（🔶 2026-08-09 收窄 · Doctor 勾定，CC 代记留痕：`material_Indium_Metal`/`metric_InPSubstrateGlobalCapacity`/`metric_InPSubstratePrice` 三节点已挂边（度 0→1，随 commit `0961ad7` 3 边），剩 `concept_InPSubstrateDopingTypes` 度仍 0 孤儿待挂）；③ 源杰表述修正：「100G EML 已商用·兑现度最高」→「CW 兑现主力、100G EML 小批量、200G 在验」；④ 源杰深析是否作增补附录落整合分析稿（待 Doctor 批）；⑤ 云锗长单精确额（5.7-8.55亿）/价格档（$800→$2300-2500）/住友43·AXT35·JX13 拆分凭压缩镜像待补强；⑥ Google 带头 CSP 多元化 InP 供应（jukan05 X）= P3 待核；⑦「27H2 缓解」(图内) vs「2030 仍 50% 缺口」(机构) 并列未收敛，待后续时点数据收敛；⑧ 市占率 45(P1·2025)/43(P2·2026-08) 双口径待收敛（reconciliation_note 已标 · 2026-08-09 InP 入库聚簇补挂 · 源：`logs/2026-08-09-InP衬底专项与入库.md`）；⑨ 松绑 `stage=reported` 待回访（政策若再收紧需更新图 · 2026-08-09 InP 入库聚簇补挂 · 源：同上）。

- [ ] **龙鱼 · 双 scorer 跟踪包（2026-08-09 由 /todo 漏挂对账补挂 · 源：`logs/2026-08-08-龙鱼双scorer周更.md`）**：① holdings-board 镜像页（Doctor 终端跑镜像脚本）；② 长飞光纤中报验证后回归判分（高增兑现→claude 上修向其回归；回落→deepseek 靠拢）；③ ~~海光信息双腿方向相反，下周重点复核（claude 升 / ds 降）~~ ✅ 2026-08-19 销账场复核完成：claude 60.0/ds 51.5 Δ−8.5 真分歧共存（Doctor 裁销账）；「claude 升/ds 降」系旧表述，实际 claude 72.5→61→60 下修收敛、ds 56.5→51.5 稳定；ds 供需端错链锚→龙鱼五力 GOTCHAS NOTE-20260819-001；④ **Kimi 基线 −8 初值 08-15 据实战复核（dated）**，定制度层最终平移量；⑤ 电科蓝天崩塌动因复核（中报/订单面），确认 −39 是否已充分定价；⑥ v2 点需 2–3 周累积后可信口径趋势才作数（当前多为混杂/跨口径，仅供参考）。

- [ ] **龙鱼 · 商业航天 30 只是否细分（2026-08-11 由 /todo 漏挂对账补挂 · 低优先开放问题 · 源：`logs/2026-08-11-龙鱼看板行业分组细分定稿.md`）**：行业分组细分定稿轮 Doctor 明示本轮不动、后续择时；触发点=Doctor 提起或下次看板改版时捎上。

- [ ] **龙鱼 · `classify_holdings.py` 一键分态分类器（2026-08-11 由 /todo 漏挂对账补挂 · 源：`logs/2026-08-10-龙鱼持仓板并入个股库与持仓迭代.md` ＋ `logs/2026-08-10-渊图星空常驻与观察点核验.md` · ⇒ Doctor 2026-08-11 裁「暂缓」）**：把持仓分态双轴规则（市值30万×利润率30%）固化成一键脚本免手判。规则已定稿在跑（决策记录 2026-08-10·当日16只按此重判、代码核验0不一致），分类器仅省手判、非阻塞。Doctor 裁暂缓——先不造工具；规则后续若微调再议。

- [ ] **龙鱼 · ds 腿光通信组运营Δ连续两周下行观察（2026-08-25 由 /todo 漏挂对账补挂 · 源：`logs/2026-08-22-龙鱼双scorer周更.md`）**：deepseek 腿对光通信组连续两周运营Δ下行（华工 -11/盛合 -7/旭创 -6/新易盛 -6，全v2可信）vs claude 腿稳定——若下周延续需双腿基线核对（暂归基线漂移，不动作）。触发回捞：下周 ds 腿运营Δ仍下行。

- [ ] **巡检脚本/镜像适配 Gateway store（2026-08-02 迁移副产 · 观察条 · 同日数据根迁出后改写）**：19 班 store 已迁 `~/Gateway-workspace/Scheduled/`（D14），`scheduler_snapshot.py` 的 `LIVE_TREE` 仍指 `~/Claude's workspace/Scheduled/`（Cowork store，19 班 disable 后冻结）。**新机制事实（2026-08-02 实测，改写本条的关键）**：保护**跟随 store**——`~/Gateway-workspace/Scheduled` 沙箱挂载同样被拒，故原设想「镜像脚本加第二源、沙箱自动化」**此路不通**；gateway 树的读取只有两条路：Mac 原生（`scheduler_snapshot.py` 已备 `GATEWAY_TREE` 常量、未接线）或 Doctor 终端 rsync 进镜像。**现状**：① `scheduler-weekly-audit` 已于 08-02 20:00:59 PDT 在本壳首点火（lastRunAt 实据），其产出/噪音表现待核——它在本壳跑脚本必报「live 树读不到」（`~/Claude's workspace` 沙箱不可达），每周一次的噪音 or 有价值告警，观察；② 巡检的 git diff 变更检测只见 Cowork 侧（冻结），**Kimi 侧班 prompt 变更无人盯**（如本次 longyu sed 修正即属此类）；③ `_DEPRECATED_Scheduled_20260802` 与新 live store 并存，`DEAD_ARCHIVED_GLOB` 语义待重估；④ `DEAD_TREE`（`~/Documents/Claude/Scheduled`）语义已改注释为「正常=不存在、再现=异常」。触发点：下次周巡检（08-09）后据实际表现定改法。**⇒ 2026-08-10 /todo 实测**：08-09 20:00 周巡检班在 Kimi 壳干净退出并贴 Doctor 终端命令（每周一次轻噪音，有「巡检中断自证」兜底、断档不被静默吞掉）；Doctor 20:18 原生跑 exit 0 无异常——但脚本 LIVE_TREE 扫的仍是冻结 Cowork 树，**Kimi 侧 gateway store 的班 prompt 变更依旧无人盯**（GATEWAY_TREE 常量备而未接线）。~~改法仍待 Doctor 定~~ **⇒ 2026-08-11 Doctor 定案：镜像 diff 线覆盖**——rsync 刷新并进周巡检班提醒（班 prompt 已改 · update_scheduled_task 落），镜像进 git 则 Kimi 侧班 prompt 变更一条 diff 可见；脚本不接 GATEWAY_TREE、零改动。08-16 周巡检班首验并班。
  依据：`logs/checkpoints/2026-08-02_19班迁Kimi壳与三级司法_PRD.md` §三 非交付项 · D13/D14 遗留

- [ ] **龙鱼 · claude 写库器口径标签升级裁定（2026-09-12 挂 · 源：`logs/2026-09-12-龙鱼五力双scorer周更.md`）**：write_claude_score.py 的 `_meta` caliber 仍写死「v2·维度正交+议价毛利率(2026-07-06锁)」，而判分纪律已演化至 v3（08-30 供需四补）/v4（09-03 公司级兑现口径）——本周 CC 判分实际按 v4 纪律执行但记录标签仍 v2（趋势工具按记录口径标，v2 序列连续性保住、标签语义失真）。待 Doctor 裁：升级写库器标签（会打断既有 v2 趋势序列连续读数）或维持 v2 标签+显式注记。

- [ ] **龙鱼 · 看板模板 meta 页头同步（2026-09-12 挂 · 源：`logs/2026-09-12-龙鱼五力双scorer周更.md`）**：board_template.html 的 meta description 仍写 95 标的/20 常更/10 持仓，实际 120/25/11（模板只由 Mac 就地运行 build_dark_board.py 时更新，沙箱只刷数据不碰版式）。Doctor Mac 跑一次 build_dark_board.py 即同步，非阻塞。

- [ ] **龙鱼 · 电科蓝天 Δ−19 真分歧共存观察（2026-09-12 挂 · 源：`logs/2026-09-12-龙鱼五力双scorer周更.md`）**：claude 62.5/ds 43.5，最大分歧维技术供需−10，诊断=真分歧共存（ds 小TAM折价 vs claude 垄断+航天认证壁垒）；申菱环境 Δ+35 属 63 天跨期不入队。触发回捞：未来 2-3 周若「小市场垄断型」（军品/宇航）标的反复出现 ds 供需端系统性低估 → 提修供需锚点（小TAM≠弱需求）。

- [ ] **brain 仓 · `.bak*` 残留归档（2026-09-26 挂 · 2026-09-29 /todo 现核当场重数 · 由本文件「待办」段移入）**：「**97 个 `.bak*`（8.62 MB）**」这个旧数**连续两轮漂移**——本场（2026-09-29 23:3x）实测 `find -name '*.bak*'`（排除 `.git`）＝ **133 件**；表观字节合计 **16,128,095 B ＝ 15,750 KB（≈15.38 MB）**（`du -ck` 块计 16,008 KB）。**⚠ 条目内原注记自称「132 件 / 15,864 KB」，两个数本场均复现不出** ⇒ 该计数随各场备份动作持续前进，**凡引用必须当场重数，禁转述**。**其余仍成立**：`.gitignore:42` ＝ `*.bak_*` 在场（41＝`*.bak_2*`、46＝`*.bak[0-9]*_*`）✓ · 自解析 `.git/index`（1668 条）内 `.bak` 路径**恰 11 条** ✓（3 个具名 `bak-doctor-20260917` ＋ 8 个均在 `archived/`）· 风险判断不变。**背景与已办**：`.gitignore` 原只覆盖极窄的 `*.bak_2*`，而工作树有近百个 `.bak*`；09-26 并行场已补 `*.bak_*` 覆盖（`gitignore` 对已跟踪文件无效，库内既有 11 个路径不受影响）；新备份自此不会被 `git add -A` 带入库。曾误带 4 个 `.skills/QA` 备份入索引，靠独立 commit 出库（`chore: 4 个 .skills/QA 备份移出索引（文件保留本地）`）。**⏳ 残留（低优先 · 已无风险）**：这些 `.bak*` 仍在盘上待处置——系分轨回退的「改前」证据 ＋ 各场 `.bak_save`/`note`/`fix` 留痕，**按可逆优先只能归档不删**；无明确时点触发，**归长期观察，不催**。

---

> **已完成 / 已取消条目** → [[TODO-已完成归档]]（`references/TODO-已完成归档.md`）。
> 2026-07-30 `/consolidate` 拆出：本文件此前 70% 体积是已完成条目，而 `/resume` 每场都要整篇读进来。
> **完成即迁**：勾掉一条后把它整块移进归档文件，别就地留着——这是 `brain-save` v3.1 的规矩。
