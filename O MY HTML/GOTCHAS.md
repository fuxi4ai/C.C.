---
title: O MY HTML · GOTCHAS（已知坑）
tags: [O MY HTML, gotchas]
created: 2026-05-14
updated: 2026-07-06
status: active
type: resource
project: O MY HTML
---

# O MY HTML · GOTCHAS（已知坑）

> 排查超过一轮的问题都该记录在这里。CC 遇到报错并解决后**立即**回写，无需 Doctor 提示。
> 实时操作日志写在项目目录的 `Projects/O MY HTML/GOTCHAS.md`；这里是沉淀+索引。

## 格式

```
## [ERR-YYYYMMDD-NNN] 简要描述
**状态**: ✅ 已解决 / ⏳ 待解决
**优先级**: 🔴 高 / 🟡 中 / 🟢 低
**触发场景**:
**错误信息**:
**解决方案**:
**预防措施**:
```

---

<!-- 在下方追加新条目 -->

## [ERR-20260706-001] Artifact 是静态快照——改文件不刷新，必须走 update_artifact
**状态**: ✅ 已解决
**优先级**: 🔴 高
**触发场景**: 改看板 HTML（直接 Edit `index.html` 或生成器写文件）后，Cowork 侧栏/artifact 仍显示旧版；单点 Reload 也不生效。
**错误信息**: 无报错。注册清单 `updatedAt` 停在旧时间，视图看旧版；Reload 只重拉数据、不重读磁盘 HTML。
**解决方案**: 必须走 `mcp__cowork__update_artifact(id, html_path=…)` 推送。`html_path` 必须落在 **outputs 或已连接目录（如 ~/Documents）内的完整 HTML**；直接指向 `~/Claude's workspace/Artifacts/{id}/index.html`（artifact 自身路径）会被拒「outside this session's workspace」。推完用 `list_artifacts` 看 `updatedAt` 变新确认。
**预防措施**: 看板改动流程固定为「改文件/跑生成器 → `update_artifact` 推 → 验 updatedAt」。**直接改文件 ≠ 刷新**。先例：烛阴 `logs/2026-06-25-信号方向场与星空D>S.md`（「星空 artifact 刷新必须走 update_artifact」）、白泽 `logs/2026-06-12-周报日报转Artifact.md`（「Artifact 为静态快照，不随重渲自更」）。

## [ERR-20260706-002] 客户端 sectorOf 重算无条件覆盖 payload 分类字段
**状态**: ✅ 已解决
**优先级**: 🔴 高
**触发场景**: 把行业/分类真源从客户端 `sectorOf(industry)` 上移到数据层（生成器 payload 直接带 `sector/seg`），但看板 JS 里仍留着加载时 `DATA.forEach(d=>{ d.sector=sectorOf(d.industry); … })` 的**无条件重算**。
**错误信息**: 无报错。按行业分组时新板块（AI硬件等）标的落入「其他」或从分组消失——**无论刷不刷新、推没推 update_artifact 都错**，因为 bug 在渲染时机：payload 正确的 sector 被加载脚本当场冲掉（空 industry→'其他'，对不上新表的→掉出分组）。
**解决方案**: 删除或条件化该行 `if(!d.sector) d.sector=sectorOf(d.industry); if(!d._q) d._q=…`，让 payload 值优先。同步修生成器模板 `board_template.html`。
**预防措施**: 分类真源上移到数据层时，**必须清掉客户端同名字段的无条件重算**。方法论铁律：**UI 分组/显示不对，第一步读「这个值在渲染时到底怎么算出来的」完整链路，别停在「数据文件是对的」就去猜缓存**——数据对≠渲染对，中间那段 JS 会变换。
