---
name: event-attribution-watch
description: EAL v3 数据链日更班：行情更新→sealed 快照→manifest-gated exact registry→冻结 XNYS 日历→DAILY_SHADOW→fresh candidate→事后归因 loop→artifact；仅 ID-C 描述性研究，因果、业务与 system closure 保持未签
---

# EAL v3 数据链日更班（L2-a · 2026-08-21 Doctor 裁「保持数据库更新」）

本任务作为 EAL（Event Attribution Ledger）v3 数据链值守班。本班只负责机械消费链：行情写库 → sealed 快照 → manifest-gated exact registry → 冻结 XNYS 日历 → DAILY_SHADOW 重跑 → fresh candidate 落库 → 事后归因循环 → 重渲染 artifact → Gateway 推送 → 简报。EAL research baseline v1 已获研究边界内批准；因果有效性、业务落地、production registry 资格、完整 PRD 与 system closure 均未据此签署，严禁扩张结论。

## 硬纪律（违者即事故）

- **不编数**：任何取数失败/数据未 final 都诚实输出，绝不编造或回填近似值。
- **关键边界 fail-closed**：输入身份、schema、SPY 主数据、registry/manifest/selector、生产库与 create-only 边界失败时立即停；可选行情或派生产物失败按下述白名单自修循环处理，不能因非关键格式问题放弃已经可完成的归因任务。**永不自修代码、冻结件或治理输入。**
- **写库纪律**：主库采集使用目标库同目录 staging → 原子替换主库（`update_attribution_db.py` 已内置）；生产库 `attribution.db` 的 schema **不动**（v3 表不上生产，这是 Doctor 裁的范围）。
- **不跑 git**：本班不 commit 不 push（写库造成的 git M 属日常，由 Doctor 处理）。
- **日历语义**：交易日历是预注册的——只可从下述 exact-pinned 冻结日历截取前缀，不得生成 session、手写节假日/开收市时间，或在看到价格后「补认」交易日。
- **回读判据**：Gateway artifact 平台会注入 405B `cowork-artifact-meta` 包装块，全文件 SHA 与 canonical 必然不同；回读必须 payload 级（剥包装块后逐位比对）。
- **沙箱不可达即贴命令**：Gateway store 路径沙箱读不到；班内 MCP 工具可用（update_artifact / update_scheduled_task）。
- **无人值守纪律（2026-09-18 Doctor 裁修法①）**：本班在无人值守会话运行，**不得调用任何需要人工批准的工具**——`allow_cowork_file_delete` 无人批准会令整班会话静默卡死、Step 2–8 全不执行（2026-09-16 实例，NOTE-20260916-001）。需人工的动作一律改为「留证据 → 停班 → 简报里贴 Doctor 终端可复现命令」。挂载类 `request_cowork_directory` 不在此列（其余日更班长期实证可用）。

## 环境

- 主库：`~/Documents/Database/宏观研究体系/EAL/attribution.db`（v2.3 旧表 + `prices_daily` / `prices_intraday`；行数每班实读，不写死历史值）
- v3 包：`~/Documents/Claude/Projects/Financial/宏观研究体系/EAL/backtest/eal_v3/`（仅标准库；声明支持与本轮实际 Python 版本必须分别记录，不把未覆盖运行时说成已验收）
- 封存目录惯例：`~/Documents/Database/宏观研究体系/EAL/eal_v3_sealed_YYYYMMDD/`
- consumer config 模板：`~/Documents/Claude/Projects/Financial/宏观研究体系/EAL/backtest/eal_scheduled_consumer_v1/config-template.v1.json`（bytes=`1736`，SHA-256=`045e0792bb3da6ce514611fe5733a7fae2d00bc116487842bc2b87fa4220169f`）
- XNYS 冻结日历：`~/Documents/Claude/Projects/Financial/宏观研究体系/EAL/backtest/eal_v3/coding_work/_vv_staging/phase4_inputs/calendar-xnys-frozen-20261231.v2.csv`（bytes=`13764`，SHA-256=`ddb4367c02acc21815680155298c102ec2408a65fe579661f1f58a877f8a8e97`）
- token：`~/Documents/Database/.env`（`update_attribution_db.py` 自行读取，勿打印 token）

## 每班流程（按序，任一步失败即停并简报）

### 1 · 行情写库（含缺口回补）

```bash
python3 ~/Documents/Claude/Projects/Financial/宏观研究体系/EAL/backtest/update_attribution_db.py
```

Yahoo 日线近 10 天自动回补缺口（如 08-19/20）、15m 回看 3 天、Massive/Polygon 补 USDJPY 15m、FRED（DGS2/DGS10）由外部通道另行增补。exit 0 且新鲜度验收通过才算数；若 Yahoo 当日日线未出（盘中 finality 不足），如实记录并继续用可得的已收盘数据，`CALENDAR_INCOMPLETE` 等 exclusion 由引擎诚实输出。读回核验：`prices_daily` 的 MAX(trade_date) 应达到最近已收盘美股交易日。

**重试语义（2026-09-18 Doctor 裁修法① · 挂载盘 I/O 失败时）**：直接以 fresh attempt 重跑，**不得先清理上一轮残留**——`update_attribution_db.py` 的 staging 名含 pid/随机串（`.{target}.next-{pid}`、`attribution-inc-<random>.db`，均 `dir=target.parent`），锁为 `fcntl.flock(LOCK_EX|LOCK_NB)` 咨询锁（进程退出即释放），**残留不阻塞重试**（实证：2026-09-14 孤儿四项在盘逾四日，其后的 09-15/09-17/09-18 三班照常跑通）。残留一律**留在原处**并在简报中列出，交 Doctor/CC 场次集中处置；**严禁在班内发起任何删除**。

### 2 · sealed 快照（MIGRATION.md 合同）

建立当班唯一 `snapshot_dir` 与不存在的 `sealed_db`。不要假定系统安装了 `sqlite3` CLI；用 Python 标准库 `sqlite3` Online Backup API，从 `mode=ro` 的 `attribution.db` 连接备份到 `/tmp` fresh staging。关闭连接后要求：source 前后 SHA 一致、staging `journal_mode=delete`、`PRAGMA integrity_check=ok`、无 `-wal/-shm`。再用 `O_CREAT|O_EXCL` create-only 复制到 `sealed_db`，`fsync` 后逐字节 SHA 回读、再次只读 integrity check，最终 `chmod a-w`。挂载盘 I/O 失败可保留到 `_failed_attempt_N_*` 后以 fresh staging 重试，禁止覆盖同名 sealed、禁止直接复制活跃 WAL 主文件。记录 source 前后 SHA、sealed SHA、表/行数、最大 SPY `trade_date` 与方法进 `seal-evidence-YYYYMMDD.json` 和简报。

### 3 · manifest-gated registry selector（硬门）

**严禁用 glob、目录排序或“最新日期版”选择 registry。** 每班先运行 Gateway 侧只读 selector；它从 `CURRENT_SHA256SUMS` 解析下列唯一、精确的 consumer pin，并回读 manifest 全树、target bytes/SHA、regular-file/non-symlink、JSON schema、38 行与 EAL runtime contract。若 manifest 缺项/重复、hash 漂移、schema/行数不符，或目录出现同日/更新但未获本 consumer pin 明确授权的 registry，均以非零退出并立即停班。

```bash
selector_json="$(PYTHONDONTWRITEBYTECODE=1 python3 -B ~/Documents/Claude/Projects/Financial/宏观研究体系/EAL/调度/event-attribution-watch/resolve_registry_from_manifest.py \
  --eal-root ~/Documents/Claude/Projects/Financial/宏观研究体系/EAL/backtest/eal_v3 \
  --expected-registry-rel coding_work/frozen-event-registry-v3.2-20260827_vv.jsonl \
  --expected-sha256 283c947d4c93b1e26813895040d92af1ae8f9759a0bb2b1e3246589c370dfc92 \
  --expected-bytes 102899 \
  --expected-rows 38 \
  --expected-schema eal-event-registry-v3.2 \
  --expected-schema-sha256 3e98dfff7159ba4fedaf5e224f4c933c41aaaa96d091a90f2ee4eb11267c7e4a \
  --expected-contract-sha256 132cd7199d88e0b1e589ed18968435777315cf42a019313bad82d30e8269cf60)"
selector_exit=$?
test "$selector_exit" -eq 0 || exit "$selector_exit"
printf '%s\n' "$selector_json"
registry_jsonl="$(SELECTOR_JSON="$selector_json" PYTHONDONTWRITEBYTECODE=1 python3 -B -c 'import json, os; print(json.loads(os.environ["SELECTOR_JSON"])["registry"]["path"])')"
test -n "$registry_jsonl" || exit 2
```

把 selector JSON 中最终解析出的 `registry.path` 与 `registry.sha256` 原样记入班日志。扫 `attribution.db` news/events 表与宏观发布日历（FOMC/CPI/NFP 等）发现新事件时，只做事实核验与 `coding_notes`；**本班不得创建、覆盖、移动或自动切换 frozen registry，也不得修改 `CURRENT_SHA256SUMS` 或 consumer pin**。新 registry 必须走独立 promotion/attestation 与 selector pin 更新授权后，才能成为本班输入。

### 4 · exact-pinned 冻结日历前缀

先验证环境列出的 XNYS 冻结日历是 regular file、非 symlink，bytes/SHA 精确匹配；漂移即停。以 sealed DB 的最大 SPY `trade_date` 为 cutoff，要求该日存在于冻结日历；create-only 生成 `$snapshot_dir/calendar-frozen-YYYYMMDD.csv`，内容必须是 canonical header 加 `trade_date <= cutoff` 的逐字节行前缀。禁止自行计算节假日、DST 或早收市；canonical 已包含 Thanksgiving/Christmas early close。对冻结日历覆盖期内的 SPY 交易日做集合交叉核验，不一致即停，不猜。记录 source 与子集 SHA/bytes/行数。

### 5 · DAILY_SHADOW 重跑

先验证 consumer config 模板 bytes/SHA；create-only 写 `$snapshot_dir/config-frozen-YYYYMMDD.json`。只允许替换四处动态值：`market_data_as_of_utc`、`market_data_snapshot.snapshot_id`、`market_data_snapshot.database_sha256`、`market_data_snapshot.observed_at_utc`；前后删除这四处后 JSON 必须 exact 相等。所有时间为同一个本班 UTC 观测时刻，snapshot SHA 必须等于 sealed 回读 SHA。

```bash
eal_root=~/Documents/Claude/Projects/Financial/宏观研究体系/EAL/backtest/eal_v3
calendar_csv="$snapshot_dir/calendar-frozen-$(date +%Y%m%d).csv"
config_json="$snapshot_dir/config-frozen-$(date +%Y%m%d).json"
cd "$eal_root"
python3 -B scripts/run_event_study.py \
  --db "$sealed_db" \
  --registry "$registry_jsonl" \
  --calendar "$calendar_csv" \
  --config "$config_json" \
  --output "$snapshot_dir/daily-shadow-result-$(date +%Y%m%d).json"
```

输出路径必须绝对且目标不存在。记录结果输入身份、cluster/final/exclusion 计数；不能把 `CALENDAR_INCOMPLETE` 或 `BASELINE_INSUFFICIENT` 改写成成功样本。

### 6 · fresh candidate 落库（六参数 adapter）

先在 `/tmp` 建 fresh candidate work DB：从 sealed DB 用 Python Online Backup API 复制，关闭后核验 source SHA 未变、candidate `journal_mode=delete`、integrity ok、无 sidecar。**必须先显式应用 schema wrapper**；第一次输出 `action=applied`，第二次输出 `action=verified_existing` 且第二次前后 SHA 不变：

```bash
candidate_work_dir="$(mktemp -d /tmp/eal-candidate-$(date +%Y%m%d).XXXXXX)"
candidate_work_db="$candidate_work_dir/candidate.sqlite"
test ! -e "$candidate_work_db"
# 先按上文用 Python sqlite3 Online Backup API 从 "$sealed_db" 备份到 "$candidate_work_db" 并验收。
python3 -B scripts/apply_eal_v3_schema.py --candidate-db "$candidate_work_db"
candidate_schema_sha="$(shasum -a 256 "$candidate_work_db" | awk '{print $1}')"
python3 -B scripts/apply_eal_v3_schema.py --candidate-db "$candidate_work_db"
test "$(shasum -a 256 "$candidate_work_db" | awk '{print $1}')" = "$candidate_schema_sha"
python3 -B scripts/load_eal_v3_results.py \
  --candidate-db "$candidate_work_db" \
  --market-database "$sealed_db" \
  --result-json "$snapshot_dir/daily-shadow-result-$(date +%Y%m%d).json" \
  --registry "$registry_jsonl" \
  --calendar "$calendar_csv" \
  --loaded-at-utc "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
```

落库后 runtime→SQL round-trip 由脚本自验，失败即停。关闭所有连接，要求 candidate integrity ok、无 sidecar；再用 `O_CREAT|O_EXCL` create-only 复制到 `$snapshot_dir/candidate-YYYYMMDD.sqlite`，`fsync`、SHA 与 integrity 回读一致后删除 `/tmp` work DB。挂载盘失败只可保留独立 failed-attempt 证据并用 fresh 目标重试，不得覆盖最终 candidate。

### 7 · 交接 Mac 原生执行（2026-09-15 Doctor 裁方案①「adapter 移 Mac 原生」· 守卫零弱化）

本班不再在沙箱内跑 post-event loop 与 production 写库——沙箱 FUSE 挂载面 fchmod 不落地（mode 恒 0o600）致 zero-write guard permission 组件同族七连 REJECTED（NOTE-20260911-001）。Step 7 三段（guard 包裹 loop / verify_run_manifest / eal_post_event adapter）已整体迁 Mac 原生执行体：`~/Documents/Claude/Projects/Financial/宏观研究体系/EAL/调度/eal-post-event-native/run_step7_native.py`（launchd `com.eal.postevent-native` · 每日 18:35 PT · 命令逐参数与原 Step 7 一致）。本班改为：落交接清单 → 轮询结果留痕 → 成功续 Step 8 / 超时或失败停班。格式见同目录 `FORMAT.md`。

#### 7a · 落交接清单

使用本班刚生成的 sealed DB 与 snapshot_dir 全路径；目标不存在才写（O_EXCL 语义），同名存在=上一班交接未消费，停班。sealed SHA 与 registry SHA 以 `shasum -a 256` 现算写入（registry 另受 Step 3 selector SHA 约束）。

```bash
production_db="$HOME/Documents/Database/宏观研究体系/EAL/attribution.db"
handoff_json="$HOME/Documents/Database/宏观研究体系/EAL/eal-mac-handoff-$(date +%Y%m%d).json"
test ! -e "$handoff_json" || { echo "HANDOFF_EXISTS: $handoff_json"; exit 7; }
export HANDOFF_JSON="$handoff_json"
export SNAPSHOT_DIR="$snapshot_dir"
export SEALED_DB="$sealed_db"
export REGISTRY_JSONL="$registry_jsonl"
export CALENDAR_CSV="$calendar_csv"
export CONFIG_JSON="$config_json"
export SHADOW_RESULT_JSON="$snapshot_dir/daily-shadow-result-$(date +%Y%m%d).json"
export PRODUCTION_DB="$production_db"
export SHIFT_DATE="$(date +%Y%m%d)"
export HANDOFF_CREATED_UTC="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
export REGISTRY_SHA256="$(shasum -a 256 "$registry_jsonl" | awk '{print $1}')"
export SEALED_DB_SHA256="$(shasum -a 256 "$sealed_db" | awk '{print $1}')"
PYTHONDONTWRITEBYTECODE=1 python3 -B - <<'PY'
import json, os
h = {
    "handoff_version": 1,
    "shift_date": os.environ["SHIFT_DATE"],
    "created_at_utc": os.environ["HANDOFF_CREATED_UTC"],
    "snapshot_dir": os.environ["SNAPSHOT_DIR"],
    "sealed_db": os.environ["SEALED_DB"],
    "sealed_db_sha256": os.environ["SEALED_DB_SHA256"],
    "registry_jsonl": os.environ["REGISTRY_JSONL"],
    "registry_sha256": os.environ["REGISTRY_SHA256"],
    "calendar_csv": os.environ["CALENDAR_CSV"],
    "config_json": os.environ["CONFIG_JSON"],
    "shadow_result_json": os.environ["SHADOW_RESULT_JSON"],
    "production_db": os.environ["PRODUCTION_DB"],
}
path = os.path.expanduser(os.environ["HANDOFF_JSON"])
with open(path, "x", encoding="utf-8") as f:   # 'x' = create-only
    json.dump(h, f, ensure_ascii=False, indent=2)
print("handoff written:", path)
PY
```

#### 7b · 轮询结果留痕

```bash
result_json="$HOME/Documents/Database/宏观研究体系/EAL/eal-mac-handoff-$(date +%Y%m%d).result.json"
deadline=$(( $(date +%s) + 3600 ))
while [ ! -f "$result_json" ]; do
  [ "$(date +%s)" -ge "$deadline" ] && { echo "MAC_HANDOFF_TIMEOUT after 60min"; exit 7; }
  sleep 60
done
mac_status="$(RESULT_JSON="$result_json" PYTHONDONTWRITEBYTECODE=1 python3 -B -c 'import json,os; d=json.load(open(os.environ["RESULT_JSON"],encoding="utf-8")); ev=d.get("zero_write_evidence") or {}; print("OK" if d.get("status")=="success" and ev.get("status")=="verified" and ev.get("permission_guard_completed") is True else "BAD")')"
[ "$mac_status" = "OK" ] || { echo "MAC_STEP7_FAILED"; exit 7; }
```

#### 7c · 停班语义与简报

停班语义不变（fail-closed）：7a/7b 任一失败即停班、不推 artifact，简报附 handoff/result 文件内容与根因。Mac 班成功时，把 result 的 `loop_dir`、`attempts_used`、zero-write evidence 摘要记入简报。轮询期间本班不读取 mutable live DB（只读 result 文件），不碰 production DB。

Mac 侧执行体以原参数跑 zero-write guard（守卫零弱化）：production zero-write evidence 回读必须 `status=verified` 且 `permission_guard_completed=true`、目标 exact 等于 `attribution.db`、`journal_mode=delete`、read transaction/权限 guard 成立、主文件身份全等且全窗未见 WAL/SHM/journal——任一不满足即写 failed 留痕，本班 7b 判 `MAC_STEP7_FAILED` 停班。`completed_with_warnings` 语义由 Mac 班 adapter/verifier 输出承载，本班从 result 透传关键状态并带入简报。地缘日期级观察不进入 registry、不写 production DB、不建立因果结论。

### 8 · 重渲染 + Gateway 推送

```bash
python3 -B scripts/render_results.py --result-json "$snapshot_dir/daily-shadow-result-$(date +%Y%m%d).json" --output "$snapshot_dir/eal-v3-event-transition-artifact-v2-$(date +%Y%m%d).html"
```

（参数名以 `render_results.py --help` 实际为准。）然后用 MCP `update_artifact`（id=`eal-v3-event-transition`）推送新 HTML。回读验证：payload 级比对（剥 `cowork-artifact-meta` 包装块后与盘上 HTML 逐位一致）。

### 9 · 简报（必做）

给 Doctor 极简简报：行情 MAX(trade_date) / sealed SHA / 有无新编码事件 / 簇状态（final 数、CALENDAR_INCOMPLETE 等 exclusion 数）/ candidate 名与行数 / 事后归因 loop 状态、attempt 数、宏观与地缘重大事件日覆盖、warning 与 root cause / artifact 已推。异常时贴 Doctor 终端可复现命令。

## 已知坑

- Registry selector：目录扫描只用于发现冲突并 fail-closed，不用于选取文件；manifest rotation 也不会自动切换本班输入，consumer pin 必须经独立授权显式更新。
- Config：只从 exact-pinned consumer 模板派生；不得沿用或 glob 选择上一班 config。
- Calendar：只截 exact-pinned canonical 的前缀；不得手写 session，尤其不得丢失 early close。
- SQLite 工具链：不要依赖环境中的 `sqlite3` CLI；Online Backup、integrity 与只读回读均使用 Python 标准库。candidate 在 loader 前必须先跑 schema wrapper。
- 平台包装层：artifact 全文件 SHA 对不上 canonical 是预期，payload 级比对才是判据（G-X120）。
- 大簇 CALENDAR_INCOMPLETE 是诚实状态：窗口缺日历/数据就报，不要为凑 final 缩窗。
- fresh candidate：O_EXCL 语义，同名存在即停，不覆盖。
- 沙箱无 git、无浏览器：截图目验留给 Doctor；沙箱不可达的路径贴命令不硬闯。

## 失败循环（根因报错 → 自修正 → 审查 → 重试）

每个可重试步骤最多 3 次；每次使用 fresh attempt/output，不覆盖前一轮证据。

1. **根因报错**：记录稳定错误码、失败阶段、实际证据、是否可恢复和下一动作。不得只写“运行失败”。
2. **定时任务自修正白名单**：数据库短暂 busy/locked 后重读同一快照；网络瞬断后重取；**挂载盘 I/O 失败后保留残留、以 fresh attempt 直接重跑（「清理残留」不在白名单内）**；派生产物缺失或审查失败后在 fresh attempt 全量重建；QQQ/VIX 可选维度缺失时降级为 SPY 主维度并留 warning；地缘 first-public clock 未闭合时只能进入明确标记的日期级观察通道。
3. **禁止自修**：不得改代码、registry、`CURRENT_SHA256SUMS`、consumer pin、selector、production DB schema、scheduler、冻结件或输入 hash；**不得发起删除，也不得调用任何需人工批准的工具**；不得把一个日期级地缘案例自动升格为 production-eligible。
4. **审查**：每次尝试后检查宏观/地缘覆盖、SPY 烈度、规律条目、有限值、因果措辞禁令和 artifact bytes/SHA。审查不通过视为本轮失败。
5. **重试/停止**：仅对白名单根因重试；成功或 `completed_with_warnings` 且设计目标审查通过才继续。三次仍失败，或遇非白名单根因，立即停班并在简报附 root-cause report。

## 2026-09-07 路径切换与交易日核验

Doctor 已授权三层迁移和定时任务重配。本文是本班唯一完整流程，平台任务仅加载本文；不得回退到旧 Database/剑酒青丘 路径。保持既有工作日 17:40 America/Los_Angeles 班次；17:44 属启动抖动。2026-09-07 为美股休市日，^SOX MAX 停在 2026-09-04 合乎日历，不能据此报漏采，也不能据此宣布 R4 新交易日水位验收。真实 R4 必须同时记录 triggered_by=scheduled 和首个新完整交易日 ^SOX 水位、来源、行数及重复检查；休市班只验调度与迁后消费，未取得的证据保持待验。所有生产采集仍共用 /tmp/event-attribution-ledger-update.lock，外层不叠加业务重试。
