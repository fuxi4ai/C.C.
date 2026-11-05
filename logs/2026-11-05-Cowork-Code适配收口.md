---
title: 会话日志 2026-11-05 — Cowork-Code适配收口
tags: [log, 模式切换, 官方端适配, skill治理, 龙鱼五力]
created: 2026-11-05
updated: 2026-11-05
status: active
type: log
project: 模式切换
---

# 会话日志 — 2026-11-05

**项目**：跨项目（Gateway→官方后的 Cowork/Code 适配）＋ 龙鱼五力（顺带修复）
**主题**：Cowork-Code 适配收口（11-04 20:58 PST 起，官方 Code 标签）
**结论**：Code 侧收口；Cowork 核对与新会话验证转出，未完成项在 `brain/TODO.md` 模式切换条。

---

## 完成的工作

- **分工入档**：Artifacts 与定时任务归 Cowork，日常任务在 Code（`Doctor协作偏好.md`、`portable/claude-code/CLAUDE.md`）。Code 上下文无 Settings 全局块，已在引导里补「实施与验收要点」子集。
- **经验索引扩面**（ERR-20261104-004 ✅ Doctor 验收）：生成器原只扫 `brain/{项目}/GOTCHAS.md`，白泽大宗被报成开放 0。现含 Projects 白名单 6 个来源、四种条目格式，总览分列开放与未标。两轮独立复验（FAIL→PASS_WITH_LIMITS）。
- **快照脚本停用 Gateway 镜像**（ERR-20261104-005 🔄）：「停用」此前只改了文档，脚本每次运行仍覆盖 `live/` 与 `artifacts/`。现 `MIRROR_ENABLED=False`，README、定时任务清单、周班镜像件、回切卡同步。云端 prompt 是否还有 rsync 未核。
- **清 cc-switch 残留**：`~/.claude/settings.json` 删 10 个 `ANTHROPIC_*` 键（本地代理路由、占位 key、旧模型映射），备份 `settings.json.bak_ccswitch_2026-11-04`，回切卡记了恢复法。
- **技能治理**：账号放薄壳、正文读 canonical；Code 保留链接并补 `brain-todo`、`damper`、`qa`；本地 `pdf` 与旧 `/qa` 命令归档到 `~/.claude/skills-archived-2026-11-04/`。新增 `.skills/_registry.json`、`_release_ledger.jsonl`、`.tools/skill_release.py`，`status` 与账号逐字比对，`/resume` 跑 `status --brief`。9 个薄壳已上传，10/10 已同步（截图＋实读）。两轮独立复核均判 FAIL，属实项已修，修后未再复核。
- **记忆只用 Brain；Gotchas 要读**：`~/CLAUDE.md` 开场清单改指经验索引。旧 Code 记忆 `gotchas.md` 11 条逐字迁入通用教训 G-X237–G-X247。
- **G-X244 ✅ Doctor 验收**：16 只标的四接口实测，同期多行普遍存在，1264 个报告期有 5 期旧写法取到空值。引擎改优先取 `update_flag=1`（`07fa470d`），16 只财务分与分项不变；未比完整五力总分。
- **引擎 407**（ERR-20261105-001 🔄）：代理带账号时补认证头（`50c3ffd9`），Code 沙箱真实调用通过。
- **retry-guard 误判**（G-X238 追记）：指纹只取前 200 字符；Doctor 终端已改为完整参数哈希，备份 `retry-guard.sh.bak_2026-11-05`。

## 做出的决策

| 决策 | 原因 | 影响 |
|------|------|------|
| Artifacts、定时任务归 Cowork，日常在 Code（Doctor） | Cowork 左侧任务会话太乱 | Code 不推看板、不建班 |
| 清 cc-switch 的 `ANTHROPIC_*` 键（Doctor） | Code 标签不走它，留着只有旧模型映射风险 | 终端 `claude` 可能要重新登录 |
| Code 保留技能链接并补齐（Doctor） | 日常在 Code，改完即生效 | 同名项并存，无法消除 |
| 账号用薄壳，靠版本治理而非失败即停（Doctor） | 正文单一真源 | 跳过失败路径探针；只改正文不用重传 |
| 薄壳不带版本标记（Doctor） | 逐字比对已足够 | 无 |
| 技能告警只走 `/resume`（Doctor） | 不加进周巡检 | 不开 `/resume` 看不到偏差 |
| 记忆只用 Brain，Gotchas 要读（Doctor） | 内置记忆目录不是真源 | 开工查经验索引 |
| 「待 Doctor 提交、待班首跑」残留不算开放（Doctor） | 扩词表误报多 | 由状态行负责人更新 |
| `the-conch-maiden` 以本地为准（Doctor） | cc-switch 副本不再参照 | 无 |

## Doctor 的纠正（便签）

- 「为什么随便改目录？」：重写工具时把上传目录从 `skill-stub` 改成 `skill-release`，未说明，致其白传一次；已改回。
- 「Gotchas要读的」：删 `~/CLAUDE.md` 开场清单时连读 Gotchas 一起删了；已改指 Brain。
- 「使用薄壳，但是不依赖失败即停」：曾误解为放弃薄壳并开工，随后改回。

## 本场自身的错

- 两次把结果判断写早：与命令并行调用收尾，第一次迁移脚本实际已失败，事后更正。
- 曾说 4 个看板镜像可能回滚，核实后不成立，已更正。

## 遗留问题 / 待办

已同步 `brain/TODO.md` 模式切换条：Cowork 九项核对（最急：周班云端 prompt 是否还有 rsync）、11-05 10:00 PT 后复查 ERR-20261104-002、11-08 周班后看 `_cloud_trigger_health.json`、新会话验证。

- `司南/GOTCHAS.md` 的 ERR-20261104-006 不是本场写的，未提交，来源未核。
- 未修的低风险项：`.skill` 损坏不自愈、账号读不到时不查 Code 链接、账号目录按 mtime 选、`name` 大小写放行与 `description` 长度不查。
- 其余 8 个薄壳未实际触发；云端班读取路径未测；ERR-20261105-002 原因未确认。

## 相关笔记

- [[2026-11-04-云端全班直跑与三处修复]] · [[2026-11-04-云端定时任务第2批与切换清单]] · [[官方端适配指令卡-2026-11-04]] · [[回切操作卡]]
