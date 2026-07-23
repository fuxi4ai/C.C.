---
title: PRD · 抖音视频实际外移到 fuxi-station（SSH/scp · 校验-提交-可逆）
tags: [prd, acceptance, DVA, 异地存储, fuxi-station, offsite]
created: 2026-07-23 00:55
updated: 2026-07-23 00:55
status: 进行中  # 进行中 / 待验收 / 已交付 / 已取消
doctor_decision: 待  # 待 / 已审 / 已取消
type: prd
project: DVA
template_version: v1.0
---

> **PRD 起草稿**（brain-prd）。CC 未开工、不打 ✓、不自动关闭（G-X4）。§二 全留 `[ ]`，待 Doctor 审/改/批。
> 前置：`2026-07-22_抖音视频异地存储准备_PRD.md`（介质无关准备层：查重/补跑/manifest/resolver/dry-run，已交付验收）。本 PRD＝把「准备层」落到真实介质 fuxi-station 上执行。

## §一 · 任务目标

把本地抖音视频冷层 `Database/Douyin/Downloaded/`（**1556 个 · 66.6 GB**）实际外移到局域网 Windows 工作站 **fuxi-station** 的冷归档盘，腾出本地空间；本地留 pointer，`resolver` 可按 aweme_id 取回；全程**校验优先、可逆**（远端校验通过 + Doctor 批准前绝不删本地源）。

访问方式（VV 握手层指南 `4AI/Shake hands/to CC/VV-to-CC-fuxi-station操作指南-20260723.md`）：SSH alias `fuxi-station`（`192.168.1.32` · 用户 `codex` · 私钥 `~/.ssh/fuxi_station_ed25519`），走 **SSH + scp**（非挂载盘）；`F:` 冷归档盘 ~902 GB 可用；已有「暂存 `.incoming` → SHA-256 → 原子提交 → 回验 → 批准后删源」verified-commit 范式可套。

**Doctor 原始指令**（逐字引用）：
> "定了：同一局域网，台式工作站，fuxi-station，访问方法见握手层"（+ 后续两问对齐）

**多轮对齐结论**（2026-07-23 · AskUserQuestion）：
- 落点：**新建独立 `F:\DVAColdArchive\Douyin\`**（与 Codex 的 `F:\CodexColdArchive` 分开——守 CC↔VV 互不写边界 + 数据层单一可信源）。
- 范围：**全部外移 1556 / 66.6 GB**（都已转写/无需转写，视频对分析已无用；要用再 resolver 按 aweme_id 取回）。
- 传输/协议：复用 VV 指南的 verified-commit 范式，但落 DVA 独立区、用 DVA 自己的提交脚本（不写 Codex 地盘、不复用 Codex `remote_commit.ps1`）。

**任务规模估算**：66.6 GB / 1556 文件 · 跨机 SSH/scp · 跨小时（分批传输+双端校验）· **含删本地源（高风险·需 Doctor 逐批批准）**· 涉及 DVA + fuxi-station。

---

## §二 · 交付标准（Acceptance Criteria）

> `[ ]` 未开始 · `[?]` CC 认为达成+证据 · `[!]` 未达成+原因 · `[~]` 不确定 · `[✓]` **仅 Doctor**。

### A. 文件层面

- [?] 外移编排器 `tools/offsite_push_fuxi.py`（Mac 侧执行·CC 只出脚本+命令）：读 manifest → 选样本 → Prepare/scp/Commit/写 pointer
  - 证据栏：在场、`py_compile` 过；`--dry-run --sample 2` 跑通、生成完整命令序列（Prepare→scp plan→scp 视频→Commit→写 pointer）。
- [?] DVA 远端提交脚本 `tools/fuxi/dva_remote_commit.ps1`（部署到 `F:\DVAColdArchive\_tools\`）：Prepare/Commit/Status/Verify + SHA-256 校验 + 原子提交 + verification/COMMITTED
  - 证据栏：在场；Commit 读 `_plan.json` 取 dest+期望 sha、比对不一致即 throw、`Move-Item` 同盘原子提交、写 COMMITTED+verification（UTF-8 无 BOM）。**PowerShell 端到端须 Doctor 在 fuxi 跑（沙箱无 Windows，见 C-小样本干跑）。**
- [?] pointer 写入 `DVA-ops/state/pointers/<aweme_id>.json`，`resolver` 可读为 offsite 态
  - 证据栏：编排器 Commit 确认 COMMITTED 后写 pointer（offsite_uri/rel_path/sha256/committed_at/session）；resolver 离线联测：源在→hot、源删→offsite，两态正确。

### B. 一致性 / 安全层面

- [?] 三段哈希一致才提交：本地 sha256（编排器算）→ 写入 `_plan.json` → ps1 比对 incoming 实测 → 提交后 dest 复测；不一致即 throw、不 Move、留 `.incoming`
  - 证据栏：`offsite_push_fuxi.sha256_of` 本地算；ps1 `Get-FileHash` 比对 `$expected`，不一致 `throw REFUSED`；Commit 后再 `Get-FileHash $destFull` 写 verification。**端到端实测 Doctor 跑（[~]，见 C）。**
- [?] offsite_uri 形如 `fuxi-station:F:/DVAColdArchive/Douyin/<rel_path>`；rel_path 与本地一致
  - 证据栏：dry-run 输出 offsite_uri 前缀正确、rel_path = manifest 相对路径。
- [?] 目标仅 `F:\DVAColdArchive\Douyin\`；不碰 Codex 地盘
  - 证据栏：`grep CodexColdArchive` 编排器/common = 0（仅注释）；ps1 `Assert-UnderRoot` 强制 dest 在 `F:\DVAColdArchive\Douyin` 下、越界 throw。
- [?] 引号安全（承握手层 §3.2/§10）：ssh 内联只传 ascii（session/aweme_id），长路径走 `_plan.json`/scp 文件名
  - 证据栏：`--sample 5` dry-run 所有 `ssh -o` 行经 grep 非 ascii = 0 命中（纯 ascii）。
- [~] 幂等/断点续传：已 `COMMITTED` 的 aweme_id 重跑跳过、不重传
  - 证据栏：ps1 Commit 见 `COMMITTED` 即 `ALREADY_COMMITTED` 返回不覆盖；scp 重传跳过逻辑须端到端验（Doctor）。

### C. 功能层面

- [?] `offsite_push_fuxi.py` / `resolver.py` `py_compile` 通过
  - 证据栏：py_compile OK。PowerShell 语法沙箱无 pwsh 未跑，Doctor fuxi 侧首跑即验。
- [~] 端到端**小样本干跑**（体积最大 2 条）：scp→远端校验+原子提交→写 pointer→resolver 两态（Doctor Mac 侧跑，CC 已出命令）
  - 证据栏：CC 出交付回报里的 Mac 命令块（部署 ps1 → dry-run → execute 2 → resolver 检查）；**需 Doctor 实跑确认 → 回填**。
- [?] 分批策略：先搬大头（`--sample`/`--author` 按体积降序）
  - 证据栏：`select()` 按 size 降序；dry-run `--sample 2` 命中麦橘456M/学院派378M 等大文件；支持 `--author` 单号成批。

### D. 可逆 / 删源纪律

- [?] 编排器**永不删本地源**（无 delete/rm/unlink 分支）；删源留作独立一步、需 Doctor 逐批批准
  - 证据栏：`grep -iE "unlink|rmtree|Remove-Item|os.remove| rm " offsite_push_fuxi.py` = 0；脚本仅写 pointer、保留源；结果行明示「本地源保留待批准删」。删源工具尚未建（本 PRD 只到 push+commit+pointer）。
- [?] 未删源前 resolver 返回 hot（本地在）；删源后返回 offsite——两态切换正确
  - 证据栏：离线联测：源在+pointer→hot；源删+pointer→offsite。
- [?] 禁止项落实：ps1 `Assert-UnderRoot` 拒盘外；已 COMMITTED 不覆盖；正式已存在且哈希不同则 throw；无通配/递归删除
  - 证据栏：ps1 无 `Remove-Item`；`Move-Item -LiteralPath` 单文件；`ValidatePattern` 限 SessionId/AwemeId 字符集防注入。

### E. 沟通层面

- [?] git commit 命令已贴给 Doctor（DVA 仓 tools/ + brain 仓 PRD；CC 不在沙箱跑 git · G-X2）
  - 证据栏：交付回报给出两仓合并命令块。
- [~] `/save` + 决策记录（外移落地 fuxi 决策）已落 brain
  - 证据栏：本 PRD 已落；会话日志/决策记录待收尾 `/save`（Doctor 端到端验证后一并）。

### F. 任务专属

- [?] **F1 CC 边界**：scp/大传输/网络/远端 powershell 一律 Mac 侧、CC 只出命令；CC 不读/不复制私钥
  - 证据栏：编排器 `--dry-run` 默认零网络；`--execute` 供 Doctor Mac 跑；全程无读 `~/.ssh/*` 私钥、无网络调用（沙箱内仅 dry-run 印命令）。
- [?] **F2 会话隔离暂存**：远端 `.incoming\<session>\` 暂存，校验过才原子提交；失败留检不覆盖
  - 证据栏：ps1 `Prepare` 建 `.incoming\<sid>`；`Commit` 校验过才 `Move-Item` 到正式；不一致 throw、incoming 保留。
- [~] **F3 第二端验收**：传完从 Mac `ssh` 复核远端存在+哈希（承指南 §10）
  - 证据栏：编排器 `Status` 查 COMMITTED + verification 哈希作第二端确认；端到端由 Doctor 首跑坐实。
- [?] **F4 zsh/PowerShell 陷阱规避**：ssh 内联零变量/零长路径（全 ascii），复杂逻辑在 `.ps1`；JSON UTF-8 无 BOM
  - 证据栏：所有 ssh 内联行纯 ascii（grep 非 ascii=0）；dest/sha 走 `_plan.json` 文件；ps1 `WriteAllText`+`UTF8Encoding($false)` 无 BOM。

---

## §三 · 非交付项（范围排除）

- 不包含：碰 Codex 归档区 `F:\CodexColdArchive` / VV 的 `remote_commit.ps1` / ComfyUI / BlenderMCP（只用独立 `F:\DVAColdArchive`）。
- 不包含：**未经 Doctor 逐批批准就删本地源**（删源永远是 Doctor 批准后的独立动作）。
- 不包含：清理 fuxi 远端历史归档 / 改防火墙 / 网段 / SSH 升级。
- 不包含：把 Downloaded 整目录做网络符号链接（指南 §7 明确不做）。
- 不包含：转写/补跑（已在上一 PRD 收口，backfill=0）。

---

## §四 · 状态

- [x] 进行中（立 PRD · 起草稿 · 2026-07-23 00:55）
- [ ] 待验收（CC 执行填三态 + 独立审查后）
- [ ] 已交付（**仅 Doctor** 全条 ✓）
- [ ] 已取消（Doctor 显式）

## §六 · 端到端小样本首跑（2026-07-23 · 链路坐实）

Doctor Mac 侧 `douyin-probe-02` 真跑 2 条大文件（麦橘 456MB / 学院派 378MB），全链通过：
- `PREPARED` → scp plan+视频 → **`COMMITTED_OK 7545114542456524032 3A595EBD…`** / **`COMMITTED_OK 7650480208872574218 E1DEEDCC…`**。
- 三段哈希一致坐实：本地 `sha=3a595ebd…` == 远端提交 `3A595EBD…`（第二端 COMMITTED_OK 即远端复算）。
- 本地 pointer 两个已写；`resolver` 两条均 `state=hot`（**源文件未删**，符合「committed 未删」态）。
- 据此 §二 相关 `[~]`（C 端到端 / B 三段哈希 / F3 第二端 / ps1 可解析）→ 提为 `[?]`（证据＝上述真跑输出）；仅「幂等续传」未专测，留 `[~]`。

**首跑揪出并修复 2 个中文 Windows bug**（详 [[DVA/GOTCHAS]]）：
- `INFRA-20260723-001` Windows PowerShell 5.1 读**无 BOM** 的 .ps1 按系统 GBK 码页解码 → 脚本内**中文注释**破坏 tokenizing、字符串引号解析崩（ParserError）。修：**ops .ps1 一律纯 ASCII**。
- `INFRA-20260723-002` 远端中文 Windows stderr 是 GBK 非 utf-8 → 编排器 `subprocess(text=True)` utf-8 解码 `0xcb` 崩溃。修：`errors="replace"` + 过滤后量子 KEX 告警噪声 + 打印远端 stdout/stderr。

---

## §五 · 验收归属

> G-X4 不变——CC 永不自行打 ✓；本段留空待 Doctor 落笔。
> 链路已端到端坐实（§六）；`[?]` 待 Doctor 验收落 `[✓]`。
