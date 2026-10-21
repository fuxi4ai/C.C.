---
title: Gateway-Official适配（司南子项目）
tags: [司南, Gateway-Official适配, 模式切换, index]
created: 2026-10-21
updated: 2026-10-21
status: active
type: index
project: 司南/Gateway-Official适配
---

# Gateway-Official 适配

> 司南子项目：**Gateway 壳与官方 Claude 桌面端之间切环境/切登录模式的护航知识线**。核心命题＝注册表不随环境走 × 文件层≠注册表层 × 两壳只能单开 × 落后方定位后按真源对齐。本文件夹只放沿革与索引，**文件本体留真源位**（沿 2026-07-06 订阅分发裁定：搬动=断链+破惯例）。

## 历史沿革（五站 · 2026-06-30 → 2026-10-21）

| 时点 | 事件 | 关键教训/产物 |
|---|---|---|
| 2026-06-30 | Anthropic 封禁 → 切 Gateway 善后 | skill 只装应用不随环境走（gsap 丢失重做）；Cowork frontmatter 引号范式（G-X43）；官方 4 artifact 方案 A 整搬（manifest+Chromium Partition LevelDB） |
| 2026-07-01 | 订阅恢复 → 切回官方 | `list_scheduled_tasks=0` 注册表归零重建（10 班+6 skill）；4 artifact「抢救原本体」复原（孤儿文件夹坑：Library manifest 清、Documents 本体未清、受保护挂不了）；**切环境复原清单**立档（五类：定时任务/skills/artifacts/网络白名单/挂载）；G-X44（官方默认拒绝+逐域名白名单 vs Gateway 开放出网）、G-X45（scheduled 内 request_cowork_directory 自动挂载可行）；时区与中立语境（账号安全纪律） |
| 2026-07-31 | 官方侧默认目录变更 → 双树分叉 | 官方 store 从 `~/Documents/Claude/` 变到 `~/Claude's workspace/`，07-30 的 SKILL 改动全落死树（「静默成功」教训：工具的可见范围决定它写到哪）；readlink 证两棵独立树；合并装回 |
| 2026-08-02/03 | 数据根迁 Gateway-workspace | 19 班+6 artifact 真身迁出 Documents（保护跟随 store 位置、改 setting 只重写注册表指针）；「归并 Cowork 目录」否决（注册表分裂是结构性的）；**回切操作卡**立档（disable 先行 / rsync 方向不可反 / 字节级终封 diff）；命名 vendor 中立 |
| 2026-10-21 | 反向适配（Gateway→官方 · 进行中） | 差异定位：官方侧落后（19 旧班+9 板 vs Gateway 24 班+10 板）；文件级备份+复制完成（镜像刷平/双壳 config 备份/manifest 快照/官方侧 pre_sync 快照/rsync 终封 24/24 OK/影子树归档）；**注册步待官方订阅开通**；新教训：写入延迟 flush 第 3 例（真机 git 瞬时干净≠未落盘）、凭证 E-004 |

## 切环境方法要点（八律 · 浓缩自历次实战）

1. **注册表不随环境走**——切壳后 `list_scheduled_tasks`/`list_artifacts` 判据直接给真相，文件树≠注册表。
2. **文件层≠注册表层**——两个 store 是两棵真树（readlink 证），改动落在调度器不读的那棵＝死树。
3. **两壳只能单开**——切换第一动作＝旧侧 disable 全部班（不删，留可逆底牌），防同日双跑写同一批库。
4. **rsync 覆盖即切换**——前提＝prompt 双壳通用+cron 一致+文件结构同为 `{taskId}/SKILL.md`；方向不可反、dry-run 核清单（--delete 会删目标侧独有件）、实跑后字节级终封。
5. **保护跟随 store 位置**——store 迁到哪，沙箱挂载/写入保护跟到哪；改 setting 只重写注册表指针、不搬文件。
6. **artifact 复原＝抢救原本体重注册**——孤儿文件夹（manifest 清、本体未清、受保护挂不了）里的 index.html 就是最新本体；重跑生成器是备选。
7. **网络白名单双轨**——官方沙箱默认拒绝+逐域名加白（取数班 Run now 逐个放行）；Gateway 开放出网。
8. **真机落盘判据**——沙箱写完别当场下「已落盘/未落盘」结论，真机侧隔时二次核验（写入延迟可达十几分钟）。

## 文件索引（真源指针 · 文件本体不在本文件夹）

**方法件（SOP）**
- `permanent/切环境复原清单.md` —— 五类复原项总索引（7-01 立 · 历次复原实战验证）
- `references/scheduled-live-mirror/回切操作卡.md` —— disable 先行/rsync 命令/终封 diff 脚本（8-02 立 · 10-21 反向适配原样复用）

**台账与快照**
- `references/scheduled-live-mirror/artifact_manifest_2026-10-21.md` —— 两侧 artifact 10 vs 9 板差异台账
- `references/scheduled-live-mirror/official_pre_sync_2026-10-21/` —— 官方侧旧 19 班+_archived 快照（git 内 · 0615ad6）
- `TODO.md` —— 模式切换挂账条（2026-10-21 立 · 含官方订阅开通后六步恢复清单）

**历史日志（6 篇）**
- `logs/2026-06/2026-06-30-gateway切换善后-skill与artifacts补迁.md`
- `logs/2026-06/2026-06-30-定时任务迁移与网络模型核查.md`
- `logs/2026-07/2026-07-01-切回官方-重建定时任务与skill.md`
- `logs/2026-07/2026-07-31-Scheduled双树分叉与SKILL合并-2358.md`
- `logs/2026-08/2026-08-02-E验收与19班迁Kimi壳.md`
- `logs/2026-08/2026-08-03-数据根迁Gateway-workspace.md`

**配套治理**
- `permanent/定时任务清单.md` · `permanent/已装skill清单.md` —— 类 1/类 2 复原真源镜像
- 通用教训：G-X43（frontmatter 范式）· G-X44（白名单）· G-X45（自动挂载）· G-X48（挂载盘 zip）· G-X53（Documents 连坐）
- 记忆条目：gateway-store-protection · gateway-artifact-wrapper · documents-mount-quirks · workspace_folders · kimi_shell

## 当前状态（2026-10-21）

- ✅ 差异定位 · ✅ 文件级备份（双仓 commit 全绿 + pre_sync 快照）· ✅ 文件级复制（终封 24/24 OK）· ✅ 影子树归档
- ⏳ 官方壳注册新 5 班（disable 态）+ 19 班 enabled 核验 + Settings/MCP 对齐 + artifact 重推 —— **全部待官方订阅开通**
- Gateway 侧运行面零改动，24 班照常值守

## 边界

- 本子项目管「切环境的方法与档案」；不管订阅开通、账号管理、两壳的产品决策。
- 增量铁律：真源文件一律改原位，本文件夹只更新沿革/索引，不制造第二份真源。
