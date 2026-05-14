---
title: 会话日志 2026-05-15 — brain看板-snapshot化与治理
tags: [log, brain, dashboard, snapshot, build-backlinks]
created: 2026-05-15
updated: 2026-05-15
status: active
type: log
project: brain-vault
---

# 会话日志 — 2026-05-15

**主题**：brain-vault-dashboard 从假数据到真治理
**关联文件**：`brain-vault-dashboard` artifact / `MAX_HANDOFF.md` / `references/brain-对接需求-20260514.md` / `.tools/build-backlinks.py` / `permanent/AI生图方法论-城市浮雕系列.md` / `渊图,龙鱼五力,政治经济学/architecture/系统概览.md`

---

## 完成的工作

### 看板修复（4 轮迭代）
1. **字段适配**：grep 从 `(最后活跃|最后工作)` 扩展为也匹配 `**最后更新**`，加 frontmatter `updated:` fallback；GOTCHAS 兼容 `architecture/已知坑.md`
2. **健壮化**：路径自动探测（候选 + glob），加项目卡健康度色条（绿/黄/红/灰）
3. **修 JS bug**：`String.raw` 模板里的 bash `${CANDIDATES[@]}` 被 JS 当成插值表达式解析失败，整个 `<script>` 没跑——改成内联 `for c in "..." "..." "..."` 绕开 `${...}`
4. **400 后改 snapshot 模式**：`mcp__workspace__bash` 在 artifact 上下文被 MCP 层 400 拒（系统级工具不在 connector 白名单），改成生成时一次性抓数据烤进 HTML 当 JSON 字面量

### 配色调整
- 棕（amber-600 #ca8a04）→ 亮橙（orange-500 #f97316）→ 温润焦糖琥珀（amber-700 #b45309）
- 配奶油浅底 #fef3c7 + 深巧克力字 #78350f，跟 stone 暖灰底协调

### 数据治理（4 步）
- **A** 渊图/龙鱼五力 系统概览补正文 `**最后更新**：2026-05-14`，看板 src 从 frontmatter 改为正文
- **B** 政治经济学日期 `2026-05-12（v2.10 状态同步）` 拆为日期独行 + `**当前版本**：v2.10`
- **C** GOTCHAS 计数改严 `^## \[ERR-[0-9]`，过滤掉模板格式示例段（7 项目假 GOTCHAS 1 → 0）
- **D** 修 build-backlinks.py 排除 inline code/fenced code、跳过 logs/chats、加 path-style wikilink；修 `permanent/AI生图方法论` 4 条带路径坏链 + `[[APIYI 转接模式]] → [[apiyi-transit-mode]]`；陷阱-G-06-G-14 内 9 条 `[[G-XX]] → [[陷阱-G-06-G-14#G-XX]]` self-section link

### handoff 归档
- `MAX_HANDOFF.md` 6 条验收 [x] + status: archived + 归档说明
- `references/brain-对接需求-20260514.md` 10 条 [x] + status: archived + 归档说明（中途文件被 python `open('w')` 误清空，git restore 救回再走 cp 路线）

---

## 做出的决策

| 决策 | 原因 | 影响 |
|------|------|------|
| Dashboard 改 snapshot 模式（不靠 live bash） | artifact 上下文 `mcp__workspace__bash` 被 MCP 层 400 拒；系统级工具不在 connector 白名单 | 看板要刷新需用户在聊天里说"刷新看板"，CC 重抓数据 + update_artifact |
| snapshot 计数排除 logs/templates/.skills | logs 是历史定格 / templates 是占位 / .skills 是示例文档；不该当 active TODO | TODO 81 → 4，看板真实化 |
| build-backlinks 跳过 logs/chats 来源的 dangling | 同样原因；历史导入数据的坏链不是 active 治理范围 | dangling 16 → 0 |
| GOTCHAS grep 加数字约束 `[ERR-[0-9]` | 模板里有 `## [ERR-YYYYMMDD-NNN]` 格式示例，被旧规则误算 | 7 个项目假 GOTCHAS 全清，改规则不动文件 |
| 文件改写统一走 cp /tmp 路线 | macOS 受保护文件上 python `open('w')` 会先 truncate 再失败、留 0 字节文件；cp 能直接覆盖 | 中途丢了 brain-对接需求-20260514.md 全文，git restore 救回；之后所有改写无事故 |

---

## 遗留问题 / 待办

无（A/B/C/D + 归档全闭环）。后续触发刷新只需 `/save` 后说"刷新看板"。

可选进阶（不急）:
- [ ] 政治经济学 4 条真 TODO 何时消化（陷阱-G-06-G-14 元机制识别四步骤）
- [ ] DVA 9 天没动是真停滞还是只是没 touch `**最后更新**` —— 要么真做、要么改 status: stable

---

## 相关笔记

- [[陷阱-G-06-G-14]]
- [[apiyi-transit-mode]]
- [[O MY HTML/architecture/方法论]]
- [[O MY HTML/architecture/系统概览]]

