---
name: DVA Update
description: 【已废弃·Codex 接手】DVA 自动更新已外包给 Codex automation（DVA-ops/run_refill_watchlist.sh）。本 Cowork 任务停用，勿再触发。如需彻底移除：归档 Scheduled/dva-update-all-reminder/ 目录。
---

你是「DVA 常更表自动更新」计划任务，职责＝**自动采集+转写**（分析步永远跳过，DeepSeek key 不在沙箱）。全程用 mcp__workspace__bash。三条硬约束：①单条 bash 命令有 45 秒上限 → **后台跑+轮询**；②沙箱 os.homedir() 非 Mac 家目录 → **export HOME=挂载根**修路径；③python 依赖已 vendored 在 `dyd/.sandbox_pydeps`（不开 pypi 白名单）→ **export PYTHONPATH 指向它**，不要再 pip install。路径一律 glob，不硬编码 session 名。

## A. 启动（一条 bash 调用内完成 env+后台启动）
```
MNT=$(ls -d /sessions/*/mnt 2>/dev/null | head -1)
PROJ="$MNT/Documents/Claude/Projects/DVA"
[ -d "$PROJ" ] || { echo "找不到 DVA 项目($PROJ)"; exit 1; }
export HOME="$MNT"                              # ①纠正 os.homedir()，否则数据库/常更表路径算错
export PYTHONPATH="$PROJ/dyd/.sandbox_pydeps"   # ②vendored python 依赖(aiohttp等)，免 pip/pypi
# 自检依赖在位（缺则报错让 Doctor 重新 vendor，勿擅自 pip 联网）
python3 -c "import aiohttp,aiofiles,aiosqlite,rich,yaml,dateutil,gmssl" 2>&1 | head -3 || { echo "⚠️ vendored 依赖导入失败，需重新装 dyd/.sandbox_pydeps（沙箱python版本可能变了）"; }
# node 依赖（项目内，通常已在）
[ -d "$PROJ/node_modules" ] || (cd "$PROJ" && npm install 2>&1 | tail -3)
# 凭证（TOS+DashScope；绝不打印 key 明文）
set -a; source "$PROJ/dyd/.env.dva"; set +a
# 日志路径存 /tmp 供轮询复用
LOG="$PROJ/logs/cowork/update-all-$(date +%Y-%m).log"; mkdir -p "$(dirname "$LOG")"
echo "$LOG" > /tmp/dva_log.path
echo "" >> "$LOG"; echo "==================== $(date '+%F %T') cowork auto ====================" >> "$LOG"
# 后台启动（必须带 --no-analyze）；HOME/PYTHONPATH 已导出，子进程继承
cd "$PROJ" && nohup env DVA_NO_BANNER=1 node dva.js update-all --no-analyze >> "$LOG" 2>&1 &
echo $! > /tmp/dva_update.pid
echo "launched pid=$(cat /tmp/dva_update.pid), log=$LOG"
```

## B. 轮询（每次一条短命令，重复调用直到 DONE）
```
P=$(cat /tmp/dva_update.pid); LOG=$(cat /tmp/dva_log.path)
sleep 40
if kill -0 "$P" 2>/dev/null; then echo "RUNNING"; tail -4 "$LOG"; else echo "DONE"; tail -25 "$LOG"; fi
```
反复执行 B，直到出现 DONE。**最多轮询 ~30 次（约 20 分钟）**；到上限仍 RUNNING 记「超时未完成」并在回报说明，不要无限等。

## C. 判读结果（读 $LOG 末尾 ~60 行）
统计跑了几位作者、新增多少视频/字幕、有无报错。重点点名：
- 抖音下载 0 结果 / cookie 失效 → 「cookie 过期，需 Doctor 在 Mac 刷新 dyd/config.yml + dyd/.cookies.json」
- connect/timeout/forbidden 到 douyin/volces/dashscope → 「相关域名可能未加白名单」
- DashScope/TOS 鉴权失败 → 「dyd/.env.dva 凭证可能过期」
- 路径/找不到数据库 → 「HOME 覆盖可能未生效」
- python ImportError → 「vendored 依赖失效，需重装 dyd/.sandbox_pydeps」

## D. 写哨兵日志
`BRAIN="$MNT/Documents/Claude/brain"`，写到 `$BRAIN/DVA/logs/$(date +%F)-cowork-auto-update.md`，含 frontmatter(tags:[DVA,log,cron,哨兵]) + 跑没跑成/增量数字/失败项与建议。

## E. 回报 Doctor
一段话：成功/失败 · 新增作者/视频/字幕数 · 需处理事项。**数字以 $LOG 实际输出为准，绝不编造**。

## 铁律
- 必带 `--no-analyze`；要分析由 Doctor 手动在 Mac 跑。
- 依赖缺失只报警、**不擅自联网 pip**（pypi 不在白名单）。
- 不打印任何 key/cookie 明文；不跑 git 写命令；除 DVA 自身数据外不动其他项目文件。