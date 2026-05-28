# brain hooks —— 把手动记忆仪式变成自动生命周期

> 来源：全栈观察员《Everything Claude Code》hook 系统那期（2026-05-24 DVA 单视频分析）。
> 视频核心洞见 = memory persistence 三件套（PreCompact 存 → Stop 写 → SessionStart 载）。
> 你的 brain 早就有这套，只是全靠手动（/save /resume /consolidate）。这三个 hook 把
> 其中**纯捕获/加载**的部分自动化，**不碰**需要理解和审批的部分（logs/permanent/git）。

## 三个 hook 各做什么

| Hook | 触发时机 | 行为 | 风险 |
|------|---------|------|------|
| `sessionstart_load.py` | 每次开/恢复会话 | **只读**注入：最近 3 篇日志标题 + 活跃项目 + 未固化草稿提醒 + TODO 顶部。让你不 /resume 也有大致上下文。 | 零（不写任何文件） |
| `precompact_snapshot.py` | 上下文压缩前 | 把"改了哪些文件 + 最近意图"快照到 `inbox/_auto/precompact-*.md`，防压缩丢状态。 | 低（只写暂存区） |
| `stop_capture.py` | 每次收工 | **安全网**：仅当本轮"有实质改动"且"未 /save"时，写一份 breadcrumb 到 `inbox/_auto/session-*.md` 并弹 macOS 通知提醒 /save。 | 低（只写暂存区） |

## 铁律（与 brain 哲学对齐）

- **只写 `inbox/_auto/`（append-only 暂存区）**，绝不写 `logs/` 或 `permanent/`。
- **绝不跑 git**（G-X2 硬约束）。commit 永远由你在终端手动跑。
- **不替你做语义总结**：正式日志仍由 `/save`（LLM skill + Step 3.5 记忆分拣）产出。
- **fail-safe**：任何异常都静默 exit 0，绝不打断会话或收工。
- 路径自解析（脚本位置的上一级 = brain 根），不写死 `/Users/...`。

## "如果我不 /save，hook 怎么知道何时该存？"

它用**确定性信号**判定，不猜、不调 LLM：统计本会话 transcript 里
`Edit/Write` 次数（默认 ≥2）或工具调用总数（默认 ≥8）。

- **没到阈值**（纯问答 / 小改）→ 什么都不做，不留痕、不打扰。
- **到了阈值且你已 /save**（本会话写过 `brain/logs/` 或敲过 `/save`）→ 跳过。
- **到了阈值但没 /save** → 它**不替你写正式日志**（那是你的 /save 该干的），
  而是：① 把一份 breadcrumb 落到 `inbox/_auto/` 当安全网（这样即便你忘了，
  本轮也丢不了）；② 弹通知提醒你回去 /save；③ 下次开会话时 SessionStart
  hook 会把"有未固化草稿"顶到你眼前。

一句话：**hook 只当安全网 + 提醒，不替你拍板。** 你仍是唯一往 logs/permanent 落盘的人。

## 安装（3 步，在 Mac 终端）

1. 合并配置：把 `settings.snippet.json` 里的 `hooks` 块并进 `~/.claude/settings.json`。
   - 若该文件还没有 `hooks` 键 → 直接把整块粘进去。
   - 若已有 `hooks` → 只把 `SessionStart` / `PreCompact` / `Stop` 三个数组项并进去，别整体覆盖。
   - 验证 JSON 合法：`python3 -m json.tool ~/.claude/settings.json`
2. 重启 Claude Code（hooks 在会话启动时载入）。
3. 自检：随便开个会话，应看到开头多了「=== brain 自动上下文 ===」注入块。

## 调参 / 开关（环境变量）

| 变量 | 默认 | 作用 |
|------|------|------|
| `BRAIN_HOOK_MIN_EDITS` | 2 | Stop：本会话 Edit/Write ≥ 此值算"实质" |
| `BRAIN_HOOK_MIN_TOOLS` | 8 | Stop：或工具调用总数 ≥ 此值算"实质" |
| `BRAIN_HOOK_NOTIFY` | 1 | Stop：是否弹 macOS 通知（设 0 关闭） |

想临时调高灵敏度门槛，可在 settings.json 的对应 hook 里加 `"env": {"BRAIN_HOOK_MIN_EDITS": "4"}`，
或在 shell 里 `export`。

## 卸载 / 临时停用

- 临时停：把 `~/.claude/settings.json` 里三个事件项删掉（或注释整段），重启。
- 彻底删：连同 `brain/.hooks/` 一起删。`inbox/_auto/` 里已生成的草稿是普通 md，可留可删。

## 维护建议

`inbox/_auto/` 是机器产物。建议定期（或在 `/consolidate` 时）扫一遍：有价值的
/save 成正式日志或蒸馏进 permanent，其余删掉。若不想让自动草稿进 git，可在
`brain/.gitignore` 加一行 `inbox/_auto/`。

---
建立：2026-05-24 · Doctor + CC · 配套视频 DVA 分析见本次会话
