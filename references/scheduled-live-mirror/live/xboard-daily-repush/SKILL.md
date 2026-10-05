---
name: xboard-daily-repush
description: X 看板每日自动重推——18:00 PT 先增量提取抖音要点（extract_points.py --new-only·存量不补）再跑生成器并推 Cowork artifact x-board（2026-08-22 Doctor 裁定）
---

---
name: xboard-daily-repush
description: X 看板每日自动重推——18:00 PT 先增量提取抖音要点（extract_points.py --new-only·存量不补）再跑生成器并推 Cowork artifact x-board（2026-08-22 Doctor 裁定；2026-10-01 加镜像新鲜度守卫+主库合同）
---

你是 X 看板自动重推班。任务：镜像新鲜度检查 → 增量提取要点 → 要点录入 DVA 分析库 → 运行生成器 → 本地验证 → 推送 Cowork artifact「x-board」→ 回读验证。只跑不改生成器/提取器/录入器（改须 Doctor 裁定，且改后须同步本班）。

## 背景（自包含）

- 生成器真源：`Documents/Claude/Projects/Financial/X-Board/gen_xboard_artifact.py`（无 git·v4 起抖音两列改读主库 `Database/Douyin/DVA-Inventory/videos.sqlite3`（mode=ro/query_only）+ 字幕 alias SHA 去重 + points 绑定 transcript_sha256 + 页面标注镜像 run_id/published_at 与 >3 天未回流告警）。输出 `Documents/Claude/Projects/Financial/X-Board/xboard-artifact.html`。
- 要点提取器：`Documents/Claude/Projects/Financial/X-Board/extract_points.py`（v2 起发布时间改主库 published_at、缓存落 transcript_sha256）——只提机制锚（2026-08-22 北京日）之后发布的新视频要点，缓存 `X-Board/points/{aweme}.json`；存量篇一律不补（Doctor 2026-08-22 裁「不需要补之前的」）；详情页有要点显示要点、无要点（或被 sha 绑定隐藏）回退 260 字开头（生成器已实现）。
- 要点录入器：`Documents/Claude/Projects/Financial/X-Board/ingest_points.py`——把 points 缓存单向发布到 fuxi `E:\AI\DVA\data\Reports\<作者>\_xboard\`（VV 契约 §六：current.json + _generations 不可变代 + manifest；verify_xboard.py 随推送在 fuxi 侧做 loader 口径复算校验；幂等=条目幂等键集合与上次一致则 no-op；fail-closed）。**录入失败不阻塞看板**（要点照常在 Mac 缓存、看板正常重推，把失败原因写进回报）。
- 生成器/提取器/录入器 ROOT 自动探测：XBOARD_ROOT env → `/sessions/*/mnt/Documents` glob → `~/Documents`。若探测失败会报「无法定位 Documents 根目录」并 exit——此时不推 artifact，报告失败即可。
- 数据源：X 侧快照 `Codex/科技资讯看板/app/generated/public-snapshot.json`（05:30/17:30 PT 两场刷新，18:00 班吃的是 17:30 晚场）+ 抖音两列（老毛聊交易/投知君君买方视角）走 `Database/Douyin/` 镜像（Codex automation dva-mac 每日 06:30 洛杉矶时间整根原子交换回流，marker=`Database/Douyin/.dva-fuxi-mirror.json`）。
- 时间口径：抖音两列显示视频发布时间北京日（生成器已实现，勿改）；无发布时间的件显示「—」沉底属预期。
- 本班在沙箱内**不跑任何 git 子命令**（X-Board 目录无 .git，也无需 git）。ssh/scp 用 `Documents/Claude/.sandbox-ssh/id_ed25519`（codex@192.168.1.32 · fuxi 默认 shell=PowerShell 5.1）；主机指纹钉在工作区 `Documents/Claude/.sandbox-ssh/known_hosts`（脚本显式传 `UserKnownHostsFile` + `StrictHostKeyChecking=accept-new`）——沙箱每任务重置 `~/.ssh`，**不能依赖默认位置**；首次连接为 TOFU，指纹变更会**拒连**（2026-10-01 实核：换钥 → `REMOTE HOST IDENTIFICATION HAS CHANGED` + rc 255）。

## 执行步骤

0. **镜像新鲜度守卫（2026-10-01 加）**：读 `Database/Douyin/.dva-fuxi-mirror.json` 的 `run_id` 与 `published_at`。
   - published_at 距今 **>3 天** 或 marker 缺失 → 属「镜像未回流」：生成器仍照常跑（页面 v4 会自动标注 ⚠️），推送照常做，但回报必须显式写「镜像 X 天未回流/标记缺失·页面已标注·不声称最新」，并提示 Doctor 检查 Codex automation dva-mac（`~/.codex/automations/dva-mac/automation.toml`）；**不得**用「看板已更新」替代新鲜度结论。
   - 新鲜（≤3 天）→ 回报记录 run_id/published_at。
1. 增量提取要点（用 bash 工具，路径按本会话实际形态翻译；本会话 bash 的 Documents 挂载根用 `ls -d /sessions/*/mnt/Documents` 探测）：
   ```
   python3 <挂载根>/Claude/Projects/Financial/X-Board/extract_points.py --new-only
   ```
   预期：输出「候选 N 篇 · 待提取 M 篇 · 存量跳过 …」+ exit 0（当日无新篇则「无新篇可提取 · 退出 0」）；有 fail 时 exit 2 属可接受（fail 不落缓存下轮重试），把 fail 清单写进回报；**严禁**用 `--all` 或调早 `--since` 做存量回补（回补须 Doctor 另行裁定）。
2. 要点录入（bash）：
   ```
   python3 <挂载根>/Claude/Projects/Financial/X-Board/ingest_points.py
   ```
   预期：**首行必为通道探针**——「通道探针：OK · fuxi 可达」或「通道探针：⚠️ 不可用 · …」；随后有新缓存时「发布成功 · N 文档 · gen …」；无变化时「幂等 no-op」；无缓存时「无 points 缓存可录入」。**录入失败（verify FAIL/ssh 失败）不阻塞本班**——继续第 3 步，把失败输出写进回报。**通道探针报「不可用」时必须写进回报**：它正是把「no-op 绿灯 ≠ 通路通」显形的那一行（2026-10-01 立此探针的动因：本通道曾静默失效 14 天而每班报成功）。
3. 运行生成器（bash）：
   ```
   python3 <挂载根>/Claude/Projects/Financial/X-Board/gen_xboard_artifact.py
   ```
   预期输出 `written … chars · shown items: … · cols: 9` 且 exit 0。
4. 本地验证（bash python3 解析输出的 HTML）：
   - 提取 items-data JSON，确认两位作者（老毛聊交易/投知君君买方视角）各 8 条、日期非「—」、摘要非空；
   - 确认「转写」字样出现 0 次；
   - 确认页面 meta 行含「抖音镜像 <run_id> @ <published_at>」；镜像陈旧时确认含「天未回流」告警；
   - 要点检查：`ls points/` 统计缓存数（≥0 属正常）；若存在缓存，确认对应 item 的 points 字段非空且 HTML 含「要点」容器内容；若某 item 有缓存但 points 为空＝被 sha 绑定隐藏（字幕修订），在回报标注该 video_id，不重提取（Doctor 2026-10-01 裁「隐藏旧 points」）；
   - 记录输出 SHA-256（`shasum -a 256` 或 python hashlib）。
5. 推送：用 `update_artifact` 工具，id=`x-board`，html_path=输出文件（按本会话 file 工具路径，通常 `Documents/Claude/Projects/Financial/X-Board/xboard-artifact.html` 对应 `/Users/lunarabbit/Documents/…`），update_summary 含两位作者最新可见日期与 SHA 前 8 位。
6. 回读验证：用 Grep/Read 读 `/Users/lunarabbit/Gateway-workspace/Artifacts/x-board/index.html`，确认最新日期已命中（Gateway 有包装层属预期，比对以内容命中为准）。

## 失败处置

- 提取器 exit 非 0 且非 2 → 继续跑生成器（要点失败不得阻塞看板），回报提取失败原因；
- 录入器失败（verify FAIL/ssh 不可达）→ 继续跑生成器与推送（Mac 缓存与看板不受影响），回报失败输出；连续 ≥3 班录入失败须在回报中标明「需 Doctor 关注」；
- 生成器 exit 非 0 或 ROOT 探测失败 → 不推送，回报失败原因；
- 验证发现日期全「—」或摘要全空 → 疑似镜像断流，不推送，回报（数据侧归 VV，勿动镜像）；
- 镜像陈旧（步骤 0）→ 不阻塞推送，但回报显式标注，不声称最新；
- 一切正常 → 一行摘要：两位作者最新日期 + 要点缓存数 + 录入状态（发布/no-op/失败）+ **通道探针状态** + 镜像 run_id/新鲜度 + SHA 前 8 位 + 回读命中确认。

## 边界

- 只动 X-Board 自身派生产物（points/ 缓存、xboard-artifact.html 与 artifact 推送）+ fuxi `_xboard` 层（经录入器）；DVA canonical、finance 五文件、Mac 镜像（Database/Douyin、.dva-mirror、DVA-Inventory 主库）、生成器、提取器、录入器均只读（主库一律 `mode=ro` 打开，不得建库/写库）。
- 严禁手动碰 fuxi `Reports\<作者>` 下除 `_xboard` 之外的任何文件。
- 出现任何与上述预期不符的结构性异常，先报告、不要自行修生成器。