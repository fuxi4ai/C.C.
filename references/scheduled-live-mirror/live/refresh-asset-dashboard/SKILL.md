---
name: refresh-asset-dashboard
description: 重扫并刷新海螺姑娘全局资产看板（survey→重建HTML→update_artifact→conch清空盘点），日更；整挂 Documents（2026-11-13 起，不搭 shim），盘点数按当轮 manifest 实算（占位节点恒跳过） + brain 治理计数/项目活跃度回写
---

刷新「海螺姑娘 · 全局资产管理」看板（global-asset-inventory）。这是"真正的重新扫描"，依次执行四步，全程只读项目、只写 manifest 与看板 HTML，**不在 sandbox 跑任何 git 写命令**：

**前置：挂载核对 + 路径 env（整挂 Documents · 2026-11-13 改）**

本班随任务整挂 `Documents`：海螺引擎与 manifest（`Claude/Projects`）、各库节点（`Database`）、brain 治理计数与项目活跃度的数据源（`Claude/brain`）、科技资讯看板（`Codex`）都在同一个根下。不分开挂载，不搭 symlink shim，不在会话里临时补任何链接。开工先实看挂载：

```bash
ls /sessions/*/mnt/
D="$HOME/mnt/Documents"
for p in Claude/Projects Database Codex Claude/brain; do [ -d "$D/$p" ] && echo "OK $p" || echo "MISSING $p"; done
```

第一行应只列出 `Documents` 一项，后四行应全是 `OK`。出现 `MISSING`，或 `mnt` 下实际是分开挂载（没有整个 `Documents`）→ 简报贴出上面命令的实际输出后**停**，不搭 shim、不申请扩大文件权限。

三个 env 直接指向 Documents 根。前两个供 `_expand_health_path` 解析 manifest 里 `${VAR}/rest` 占位；第三个 `CONCH_DOCUMENTS_ROOT` 是引擎 `_find_documents_root` 的 ⓪ 优先级——缺它或指错时 survey 会把 project 全部跳过却仍 exit 0，属静默降级，必须避免：

```bash
D="$HOME/mnt/Documents"
export CONCH_DOCUMENTS_ROOT="$D"
export CONCH_DATABASE_MOUNT="$D/Database"
export CONCH_BAIZE_MOUNT="$D/Claude/Projects/Financial/白泽大宗"
```

- ⚠ 沙箱 bash 每次调用独立、env 不跨调用存续：**上面四行必须分别与 step 1 的 survey 命令、step 2 的 build 命令写进同一个 bash 调用**（两步都要带全；step 1 的代码块已自带）。
- 目录不存在的 project 会被 conch 优雅标记 unscannable，不报错；env 未导出则相应 health_file 跳过、不点亮新鲜度（也不污染 status）。**2026-08-01 起看板会给这些节点打「未扫描」灰标 + 页脚计数**，跳过不再隐形——但仍应先查清原因，别让灰标常驻。

1. **全局盘点重写 manifest**：把下面整块原样放进一个 bash 调用里跑（它自带路径 env，先从当轮 manifest 实算期望值，再跑 survey，最后断言）：

```bash
cd "$HOME/mnt/Documents/Claude/Projects/海螺姑娘" || exit 1
D="$HOME/mnt/Documents"
export CONCH_DOCUMENTS_ROOT="$D"
export CONCH_DATABASE_MOUNT="$D/Database"
export CONCH_BAIZE_MOUNT="$D/Claude/Projects/Financial/白泽大宗"
OUT="${CONCH_SURVEY_OUT:-data/asset_manifest.json}"
python3 -c 'import json
P=[n for n in json.load(open("data/asset_manifest.json",encoding="utf-8"))["nodes"] if n.get("kind")=="project"]
ph=[n.get("id") for n in P if "（待落）" in (n.get("path") or "")]
print("期望 · project 总数",len(P),"· 占位",len(ph),ph,"· 盘点",len(P)-len(ph),"· 跳过",len(ph))' || exit $?
if [ "$OUT" = "-" ]; then
  CHK="${CONCH_SURVEY_TMP:-$HOME/conch_survey_stdout.json}"
  python3 conch_engine.py survey --manifest data/asset_manifest.json --out - > "$CHK"
else
  CHK="$OUT"
  python3 conch_engine.py survey --manifest data/asset_manifest.json --out "$OUT"
fi
rc=$?
echo "survey exit=$rc"
[ "$rc" -eq 0 ] || exit "$rc"
python3 -c 'import json,sys
P=[n for n in json.load(open(sys.argv[1],encoding="utf-8"))["nodes"] if n.get("kind")=="project"]
ph=sorted(n.get("id") for n in P if "（待落）" in (n.get("path") or ""))
un=sorted(n.get("id") for n in P if (n.get("conch") or {}).get("scanned") is not True)
ok=(un==ph and len(P)>len(ph))
print("实际 · project 总数",len(P),"· 盘点",len(P)-len(un),"· 跳过",len(un),un,"·","一致" if ok else "不一致")
sys.exit(0 if ok else 1)' "$CHK"
rc=$?
echo "断言 exit=$rc"
[ "$rc" -eq 0 ] || exit "$rc"
```

   （survey 遍历项目总览各项目目录做只读盘点 + 读各资产 `health_file` 指向的 `_health.json`，把健康/新鲜度回写 `data/asset_manifest.json`；并回写 brain 治理计数 [tracked 项目的 todos/gotchas]、项目活跃度 [brain logs 文件名日期→freshness.last]、数灵 logs/last 现数。**纯增量**：obsolete_count 只作信息、绝不自动改策展 status，不臆造 edges；brain 未挂载时计数保留上轮值并打警告）。
   **盘点口径（从当轮 manifest 实算，不写死数字）**：占位节点＝`kind` 为 `project` 且 `path` 含「（待落）」的节点（无实体目录，恒跳过属正常）；**期望跳过数＝占位节点数，期望盘点数＝project 总数−占位节点数**。代码块先打印「期望 · …」，跑完 survey 后回读产物打印「实际 · …」并断言：`conch.scanned` 不为 true 的 project 必须恰好是那些占位节点。正常班（不设 `CONCH_SURVEY_OUT`）survey 还会打印一行「✓ survey 完成：盘点 X 个 project，跳过 Y 个」，X、Y 也须分别等于期望盘点数与期望跳过数。2026-11-13 实算为 18 个 project、1 个占位（数灵转移）→ 盘点 17、跳过 1，仅作提示，以当轮实算为准。
   `survey exit` 非 0、`断言 exit` 非 0、「实际」行写「不一致」、X/Y 与期望不符、报「未能定位 Documents 根目录」、盘点 0 个、或打印「⚠ brain 未挂载」警告 → 简报写明期望值、实际值与未扫描节点清单后**停，不执行步骤 2–4**；不带病继续，不搭 shim。
   只读核验（仅供人工排查，正常班不用）：跑代码块前 `export CONCH_SURVEY_OUT=-`，survey 改为只输出 JSON、不写回 manifest、不追加运行历史，JSON 落在 `$HOME/conch_survey_stdout.json`（Documents 之外），断言照常；该模式下引擎不打印「✓ survey 完成」那一行。
   **brain 计数合理性校验**：回报时 tracked 项目里 todos+gotchas 非零应 ≥5 个（全 0 = 计数链断了，回查 brain 挂载）；渊图/烛照九阴 错题本 ≥3 属已知真实积压、会亮青碧告警晕，不是故障。
   注：survey 会按各节点 `expect_days`（未声明则默认 14 天）判自检产物是否陈旧，超期的 healthy 节点自动降 stale（金光）。这是设计行为，不是故障；若某节点被误判，改 manifest 里它的 `expect_days` 而非关掉规则。

2. **重建看板 HTML**：在 `Claude/Projects/海螺姑娘/dashboard/` 下（同一 bash 调用内带全三个 env）跑
   `python3 build_asset_dashboard.py`
   （把刷新后的 manifest 重新嵌进 `dashboard/asset-dashboard.html`）。建成后必验注入数：
   先自推导应注入数 N（2026-11-07 Doctor 裁 7A：不再写死数字——N = manifest 里 `health_file` 非空、且按 build 同一解析规则能读到含时刻的 `_health.json` 的节点数；在 `dashboard/` 目录、三个 env 在场的同一 bash 调用内跑）：
   `N=$(python3 -c 'import json,os,re,pathlib;D=pathlib.Path.cwd().resolve().parents[3];R=re.compile(r"^\$\{([A-Z_][A-Z0-9_]*)\}/(.+)$");n=0
for x in json.load(open("../data/asset_manifest.json",encoding="utf-8"))["nodes"]:
  hf=x.get("health_file")
  if x.get("kind")!="database" or not hf: continue
  m=R.match(hf); p=(pathlib.Path(os.environ[m.group(1)])/m.group(2)) if (m and os.environ.get(m.group(1))) else (None if m else D/hf)
  try: d=json.load(open(p,encoding="utf-8")) if p and p.exists() else None
  except Exception: d=None
  if d and (d.get("updated_at") or d.get("generated") or d.get("checked_at")): n+=1
print(n)'); echo "N=$N"`
   再断言 `grep -o '"update_health"' asset-dashboard.html | wc -l` **== N**（N 应 ≥ 5；N=0 即 env/挂载没带上）（**用 `-o` 计次数，勿用 `-c` 计行——内嵌 manifest 为单行，`-c` 恒报 1 造成假警报**）；
   另验 `grep -o '"scanned": true' asset-dashboard.html | wc -l` 应 ≥ 14。任一不达标即视为 build 失败、回查 env，勿以「HTML 生成成功」当成功。

3. **推送到 artifact**：用 `update_artifact` 工具，id=`global-asset-inventory`，html_path 指向 `Claude/Projects/海螺姑娘/dashboard/asset-dashboard.html`，update_summary 写「重扫刷新 · {今天日期}」。

4. **conch 清空/盘点（两纪律目录 · 2026-09-12 Doctor 立 · 2026-09-19 迁至 `~/Documents/Claude/` 下）**：用 `mcp__cowork__request_cowork_directory` 挂**两个叶子目录**——`~/Documents/Claude/临时文件` 与 `~/Documents/Claude/散落归档文件`（单目录挂载可行）。**切勿改挂 `~/Documents/Claude` 整层**——那会把 brain vault 与 `.sandbox-ssh/`（SSH 私钥）一并暴露给无人值守班，属权限扩张；亦勿整挂 Documents。挂完用 `ls /sessions/*/mnt/` 现场查两个挂载路径。
   - **清空 `临时文件/`**（纪律=落时即确认可删 · 随 conch 周期清空 · 不需逐件审批）：先 `ls -A` 记下件数；然后
     `find "<临时文件挂载路径>" -mindepth 1 ! -name 'README.md' -exec rm -rf {} +`
     （README.md 是纪律正文，保留；**rm 若报 Operation not permitted，不得调用 `allow_cowork_file_delete`**——2026-09-16 实例：该工具在无人值守班会话里无人批准，会令整班静默卡死。此时**直接跳过本轮清空**，把「清空前 N 件 → 残留 M 件 + EPERM」如实记入回报，下轮自然重试）
     删后 `ls -A` 复验：应只剩 README.md 或为空。
   - **盘点 `散落归档文件/`**（纪律=只进不出 · 只归档不删）：只读——`ls -A` 记录件数与最旧 mtime，**不移动、不删除、不送 fuxi**（送 fuxi 的归档批次机制待 Doctor 立；本班只盘点并在回报中列件数）。
   - 回报：临时文件清空前 N 件 → 清空后残留 M 件（应 0 或仅 README）；散落归档现积压 K 件。

完成后用一两句话回报：各状态分布（healthy / stale / needs_repair / broken 各几个）、有没有节点 overall=fail（即真出问题的库/管线）、有没有节点因自检超期被降 stale（附 age/expect）、本轮未扫描项数、**brain 摘要（todos/gotchas 非零项目数 + 错题本告警≥3 名单 + 活跃度回写了几项）**、**conch 摘要（临时文件清空件数/残留、散落归档积压件数）**。若某步失败，如实说明哪步、什么错，不要假装成功。

注：本任务每天自动跑一次，也会被看板上的「🔄 重新扫描」按钮按需触发——两种触发执行内容相同。
