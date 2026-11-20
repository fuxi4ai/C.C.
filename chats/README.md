---
title: chats/ — Claude 对话存档
tags: [chat, brain, import]
created: 2026-05-14
updated: 2026-11-19
status: active
type: resource
---

# chats/ — Claude 对话存档

跨端 Claude 对话归档区。两个子目录：

| 目录 | 来源 | 导入方式 |
|------|------|---------|
| `code/` | Claude Code · Cowork 桌面 | 自动（`import-chats.py`） |
| `web/` | Claude Web · iOS App | 手动（见下方流程） |
| `transcripts/` | 真相层（原始会话）：Claude Code + Cowork 原始记录 · C 档 | `transcript_ingest.py` 增量抽取 · **不进 git** |

## transcripts/ · 真相层（原始会话）（2026-11-19 立 · Doctor 批 C 档）

> 对外统一称「真相层（原始会话）」；目录名沿用 `chats/transcripts/`。

原始记录的长期留存库，是 brain 记忆层级的地基：日志、permanent 都是笔记，要核对「当时到底发生了什么」就查这里。Claude Code 默认只保留 30 天原始记录，过期即删；本库只增不减。

- **来源**（`--source 标签=路径` 可重复；不给则收默认三处）：
  - `code`：`~/.claude/projects`（Claude Code，含经 cc-switch 走 Claude Code 的其他模型会话）
  - `cowork`：`~/Library/Application Support/Claude/local-agent-mode-sessions`（官方 Cowork，约 2026-05～08）
  - `cowork3p`：`~/Library/Application Support/Claude-3p/local-agent-mode-sessions`（Gateway 模式 Cowork，约 2026-08～11）
  - fuxi 冷归档解压后用 `--source fuxi-YYYYMMDD=解压目录` 一次性收录（已收 `fuxi-20260811` 49 场、`fuxi-20261013` 235 场；之后不带 `--source` 的日常增量只跑默认三处，归档抽取件照留）
  - 除 `code` 外只收 `/.claude/projects/` 下的会话文件；`audit.jsonl`（带签名的审计日志，对话部分与会话文件重合，体积大头是思考片段流）与 `outputs/` 产物不收。
- **内容（C 档）**：对话文字（含助手忙时的中途插话 `queued`、后台任务回报 `role=notification`）+ 工具调用参数（每条上限 8KB）+ 工具结果（每条截前 2KB），逐条脱敏为 `[REDACTED:类别]`；subagent 的类型与任务描述并入 header；不含 thinking 与图片。
- **布局**：`transcripts/YYYY-MM/<首条本地日期>_<来源>_<会话文件名>_<路径哈希>.jsonl.gz`，首行 header；每条记录带 `uid`（消息 uuid#块序号）；`_state.json` 记增量状态。日期一律按本机时区。
- **保全**：源被清理后抽取件照留；源变小，或重抽结果不再覆盖旧件的全部消息（源被改写）时，旧件改名 `*.superseded-<时间>.jsonl.gz` 保留。状态文件损坏会自动另存并重建；同时只允许一个抽取进程（文件锁）。
- **每日任务**：本机 launchd `com.brain.transcript-ingest`，每天 03:40 增量抽取（源文件 `.tools/launchd/com.brain.transcript-ingest.plist`，日志 `~/Library/Logs/brain-transcript-ingest/`）；/save 只检查 `_state.json` 的 `last_run`，超过 48 小时告警。
- **手动抽取**：`python3 -I ~/Documents/Claude/brain/.tools/transcript_ingest.py`（增量；`--dry-run` 只报告；退出码 0 成功 / 1 有会话文件读失败（下次重试）/ 2 无可用来源 / 3 已有进程在跑 / 4 黑名单加载异常、本次未写；`--secret-sources ""` 会关闭黑名单，只用于排障，日常不要用）
- **检索**：`python3 -I ~/Documents/Claude/brain/.tools/transcript_search.py 关键词 [--patterns-file 多词文件] [--exclude-notes 排除读写笔记本身的记录] [--regex] [--since/--until 本机日期] [--role user|assistant|notification] [--kind] [--source] [--session] [--oldest-first] [--count]`；默认新的在前，同一消息跨文件重复只报一次。
- **测试**：`python3 -I ~/Documents/Claude/brain/.tools/test_transcript_ingest.py`
- **脱敏的四层**（按执行顺序）：
  1. **已知凭证黑名单**：运行时只在内存里读 `.tools/transcript_secret_sources.txt` 列出的本机凭证文件（Doctor 2026-11-19 授权），遮掉这些值本身及其 8 位以上片段（含两类以上字符、5 个以上不同字符的窗口；值里有 `: @ !` 等字符时分段取窗口）。只收键名像凭证、值形态像凭证的；`Authorization` 这类单词、主机名、占位串、localhost 连接串不收。**fail-closed**：清单不存在、一个值都没加载到、有凭证文件读不了、或文件数/值数比上次少，本次不写抽取件、退出码 4；有意变动时加 `--accept-secret-change` 更新基线。
  2. **形态规则**：各家密钥前缀（sk-、sk-ant-、sk_ 十六进制、gh*_、AKIA、AKLT、LTAI、glpat-、hf_、ntn_、AIza、xox、JWT、智谱 id.secret）、Bearer、`set_token(…)`/`pro_api(…)`、私钥块（含没有结束行的）、URL 内嵌口令；`sk-` 开头的 URL 词串（sk-hynix-…）不算。
  3. **键值规则**：令牌/密钥/口令类「键=值」（半角/全角冒号与等号、`secret key` 这类带空格键名、`***`/`…`/`<前N位隐藏>` 遮掩前缀）、中文键名（密码/口令/令牌/密钥…）、整词 `AK`/`SK`（值是路径时不算）、命令行参数 `--token 值`、值外包反引号/弯引号/直角引号、粗体键名 `**Token**:`、环境变量兜底值、.env 裸值、浏览器会话 cookie、令牌附近的长十六进制、独立 56 位十六进制。
  4. **高熵兜底**：≥32 位、只含字母数字与 `+ /`、大小写字母和数字俱全、香农熵≥4.5、单词片段占比≤40% 的串；前面是 SRI 哈希、`?v=`/`&list=`、`;base64,`/`data:` 的放行。
- **已知局限**（真相层只在本机、不进 git、不进 iCloud，暴露面不超过原始记录；但不要把它当作「已无密钥」的数据外发）：
  - 没在黑名单里的凭证只靠形态和键值规则：纯字母或纯小写的长密钥、16 位以下的令牌、没有键名也没有固定形态的裸串可能漏；含 `-`/`_` 的 base64url 串、含 `/` 不含 `+` 的串会被切段判定，可能绕过高熵兜底；拼在 `?v=`、`;base64,` 后面的串直接放行。
  - 凭证被轮换、旧值从凭证文件删掉后，之后重抽的旧会话不再按黑名单遮这个旧值，只靠形态规则。
  - 误伤不少：第五轮审查估计约八成 `[REDACTED]` 不是密钥（新闻文章 ID、sec_uid、锁令牌、文件哈希等），代价是这些内容检索不到。
  - 按 8 位窗口遮碎片，十六进制或 UUID 形态的值会和别处 UUID 偶然撞上 8 位，偶尔误遮。
  - 键值规则仍认不出：表格里的 `| token | 值 |`、`token 值`（无分隔符）、中段省略号 `abcd…wxyz`、键名后紧跟省略号的 `app_secret…：值`、只给前缀的预览；黑名单加载器读不了 YAML 写法、两行令牌文件、值含空格、短于 12 位的值。现有数据实扫无真残留。
  - 状态文件损坏后，黑名单基线从 `_secret_baseline.json` 取回，仍按「比上次少就停」执行。
- **体量上限**（2026-11-20 Doctor 定）：真相层超过 2GB 后，把最早的若干月抽取件打包归档到 fuxi-station `F:\Mac_Backup\cc_sessions\`（打包、双端哈希核对、再删本机，与会话冷归档同一流程）。Dream 每天报告体量，到线时写归档提案。
- **不出本机**：已进 `.gitignore`；`.tools/backup-icloud.sh` 已排除（见通用教训 G-X285）。
- **与 `code/` 的关系**：`import-chats.py`（2026-05-14）只留文字、按文件名去重、输出进 git，仅导过 1 篇；真相层不依赖它，旧工具与 `code/` 现有内容保留未动。
- PRD：`logs/checkpoints/2026-11-19_真相层_PRD.md`

## code/ · Claude Code 对话自动导入

### 数据源

Cowork 桌面端 / Claude Code 每个 session 会在 `~/.claude/projects/<mangled-path>/<session-uuid>.jsonl` 写下完整的对话流（user/assistant/tool_use 全在里面）。

### 导入

```bash
# 列出所有可导 session（不写文件）
python3 ~/Documents/Claude/brain/.tools/import-chats.py

# 全部导入
python3 ~/Documents/Claude/brain/.tools/import-chats.py --all

# 只导今天的
python3 ~/Documents/Claude/brain/.tools/import-chats.py --since 2026-05-14

# 只导某个 session（前 8 位 uuid）
python3 ~/Documents/Claude/brain/.tools/import-chats.py --session 53552140
```

输出：`chats/code/{YYYY-MM-DD}-{ai-title-slug}.md`，含 frontmatter + 时间戳。

### 增量导入

脚本已有去重——已存在的文件名跳过。可放进 /save skill 末尾让每次会话自动归档。

## web/ · Claude Web 手动导出

Anthropic Web 没暴露本地对话存储。导出有两条路：

### 方式 A · 浏览器复制粘贴

1. claude.ai 打开目标对话 → 右键全选 → 复制
2. 新建 `chats/web/YYYY-MM-DD-{主题}.md`，按 code/ 同样的 frontmatter 写
3. 粘贴对话内容，手动用 `### Doctor` / `### Claude` 分段

### 方式 B · Anthropic Data Export

[claude.ai/settings/data-privacy-controls](https://claude.ai/settings/data-privacy-controls) → "Request data export" → 下载邮件里的 zip → 用 `claude_web_to_md.py` 转（待实现）

## 增量更新建议

在 brain-save skill 末尾追加：
```bash
python3 ~/Documents/Claude/brain/.tools/import-chats.py --since $(date +%Y-%m-%d)
```
这样每次 /save 都会顺手把当天 Code session 归档进 chats/code/。

## GOTCHAS

- jsonl 里有 `tool_use` / `tool_result` 条目——脚本只保留文本，工具调用归约为 `_[使用工具：xxx]_` 占位
- 单个 session 长达数百轮也能处理（验证：本次 247 轮 → 48KB md 文件）
- 标题用 `ai-title` 字段（Claude 自动生成的会话标题）；没有则用 session_id 前 8 位
