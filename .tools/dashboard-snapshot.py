#!/usr/bin/env python3
"""dashboard-snapshot.py — 为 Brain Vault Dashboard artifact 生成 snapshot JSON。

用法：python3 dashboard-snapshot.py [--root BRAIN_ROOT]
输出：stdout 打印 JSON（喂给 artifact 的 <script id="snapshot-data">）

规则沿袭 2026-05-15 治理决议：
- TODO 计数排除 logs/templates/references/chats/.skills/.index
- GOTCHAS 数「未消化的坑」：权威库 Projects/<proj> 优先 + brain 补，按 ID 去重，只计状态 🔄/⚠️/⏳
- 悬空 wikilink 调 build-backlinks.py（其内部已跳过 logs/chats）
- 项目最后活跃：max(日志, 正文**最后更新**, frontmatter updated)，标注来源
维护：CC。落点：brain/.tools/dashboard-snapshot.py
"""
import argparse, json, re, subprocess, sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

EXCLUDE_TOP = {"agents", "chats", "fleeting", "graphify", "inbox", "logs",
               "permanent", "references", "templates", "白泽大宗", "烛照九阴", "MiroFish", "数灵转移",
               "司南", "海螺姑娘"}
TODO_EXCLUDE_PARTS = {"logs", "templates", "references", "chats", ".skills", ".index", ".tools"}
DATE_RE = re.compile(r"(\d{4}-\d{2}-\d{2})")

# 金融项目（数灵金融线三条）——snapshot 的 EXCLUDE_TOP 把它们踢出常规 projects，
# 这里单列以喂「星空」面板（项目星）。Doctor 定案 2026-06-22：白泽大宗/烛照九阴/剑酒青丘。
FINANCE_PROJECTS = ["白泽大宗", "烛照九阴", "剑酒青丘"]

# 金融线数据链路（数据源 → 数据库 → 项目）——手工策划，Doctor 核过 2026-06-22。
# 喂星图三环 + 生成 .index/finance-chain-status.json（库级 fresh/broken）。
# sources = 外部原料/上游（可被多库共享）；consumes = 该项目跨库读取的「别人的库」（交叉调用）。
FINANCE_CHAINS = [
    {"project": "烛照九阴", "database": "烛照九阴-复盘",
     "sources": ["四维度复盘课件", "渊图"],
     "consumes": ["剑酒青丘-行情"]},  # 复盘拉四表行情(Market-Data)→日报，复用 daily_market/stock_tracking
    {"project": "剑酒青丘", "database": "剑酒青丘-行情",
     "sources": ["Tushare"], "consumes": []},
    {"project": "白泽大宗", "database": "白泽大宗-商品",
     "sources": ["Gangtise edb", "Tushare", "渊图", "龙鱼五力", "SMM/web补价", "管线 JSON"],
     "consumes": []},  # 直连 tushare_pro 取期货/龙鱼，不走行情库
]
# 孤库：有数据源但不在金融执掌线（无项目产出方）
FINANCE_ORPHAN_DBS = [
    {"database": "DVA-视频", "sources": ["抖音"]},
]

# 反哺边（离心·跨线回流）：DVA 金融作者(投知君君)反常识/视角料 → 渊图视角层。
# 手工策划，Doctor 核过 2026-06-22。与 feed/own/cross 区别渲染。
FINANCE_FEEDBACK = [
    {"from": "DVA-视频", "to": "渊图", "label": "反常识/视角料反哺（投知君君→渊图视角层）"},
]

# 星图节点一句话概要（Doctor 2026-06-22 手写·点击节点卡显示）。键＝节点名(项目/库/源)。
FINANCE_NODE_DESC = {
    # 项目
    "白泽大宗": "大宗商品基本面研究（数灵·白泽/小白·宏观线）",
    "烛照九阴": "复盘 / 新闻线（数灵·烛阴/九儿）",
    "剑酒青丘": "行情 / 量化线（数灵·句芒/芒芒）",
    # 数据库
    "白泽大宗-商品": "大宗商品基本面库（期货/现货/库存/评分）",
    "烛照九阴-复盘": "每日复盘库（四表行情 + 课件）",
    "剑酒青丘-行情": "Market-Data 行情库（Tushare 期货/股票）",
    "DVA-视频": "抖音常更作者视频分析库（字幕 + 8 层智慧萃取）",
    # 数据源
    "渊图": "行业图谱知识库（节点-边图谱 + 价格层）",
    "Tushare": "行情数据源（期货/股票 API）",
    "Gangtise edb": "商品/宏观数据（edb）",
    "龙鱼五力": "产业链五力分析源",
    "SMM/web补价": "有色/商品现货补价（SMM + web）",
    "四维度复盘课件": "复盘方法论课件源",
    "管线 JSON": "周更管线产出的真源 JSON",
    "抖音": "抖音视频原料（DYD 下载）",
}


def build_finance_chain(dbf):
    """用实时 db_freshness 给链路叠加库级状态：broken = 库 stale 或 last_update 缺失。"""
    by_name = {d["name"]: d for d in dbf}

    def status_for(dbname):
        d = by_name.get(dbname)
        if not d:
            return {"last_update": None, "age_hours": None, "threshold_hours": None,
                    "stale": False, "broken": True, "detail": "库未在巡检表"}
        broken = bool(d.get("stale")) or d.get("last_update") is None
        return {"last_update": d.get("last_update"), "age_hours": d.get("age_hours"),
                "threshold_hours": d.get("threshold_hours"), "stale": bool(d.get("stale")),
                "broken": broken, "detail": d.get("detail", "")}

    chains = [dict(project=c["project"], database=c["database"], sources=list(c["sources"]),
                   consumes=list(c.get("consumes", [])), **status_for(c["database"]))
              for c in FINANCE_CHAINS]
    orphans = [dict(database=o["database"], sources=list(o["sources"]),
                    **status_for(o["database"])) for o in FINANCE_ORPHAN_DBS]
    # 反哺边叠加库级状态（broken 跟随起点库）
    feedback = [dict(**fb, broken=status_for(fb["from"])["broken"]) for fb in FINANCE_FEEDBACK]
    return {"chains": chains, "orphan_databases": orphans,
            "feedback_edges": feedback, "node_meta": dict(FINANCE_NODE_DESC)}

AGENT_PROFILES = [
    {"glyph": "🦌", "name": "白泽", "nick": "小白", "rank": "大哥", "color": "#2563eb",
     "persona": "风度翩翩 · 雅言 · 敬称“老师”", "duty": "宏观线 — 白泽观星 · 白泽大宗", "call": "唤名：白泽 / 小白"},
    {"glyph": "🐉", "name": "烛阴", "nick": "九儿", "rank": "二姐", "color": "#dc2626",
     "persona": "温柔可爱 · 亲昵“哥哥” · 自称九儿", "duty": "复盘线 — 烛照九阴 · 新闻模块", "call": "唤名：烛阴 / 九儿"},
    {"glyph": "🌱", "name": "句芒", "nick": "芒芒", "rank": "三妹", "color": "#16a34a",
     "persona": "活泼俏皮 · 亲昵“哥哥”", "duty": "行情/量化线 — 技术工具 + 审查 + 记忆守护 + Market-Data", "call": "唤名：句芒 / 芒芒"},
    {"glyph": "🪔", "name": "C.C.", "nick": "守灶人", "rank": "老幺", "color": "#d97706",
     "persona": "务实温和 · 敬称“老师” · 守 brain + 调度兄姐", "duty": "非金融 + 开发 — PEC · 渊图 · 龙鱼五力 · 星空", "call": "本机 · 全局 logs/"},
]


def latest_date_in_name(paths):
    best = None
    for p in paths:
        m = DATE_RE.search(p.name)
        if m and (best is None or m.group(1) > best):
            best = m.group(1)
    return best


def project_last_active(root, proj, log_files):
    candidates = []  # (date, src)
    # 1) 日志：文件名含项目名，或 frontmatter project: 含项目名
    for lf in log_files:
        hit = proj in lf.name
        if not hit:
            try:
                head = lf.read_text(encoding="utf-8", errors="ignore")[:500]
                hit = re.search(r"^project:.*" + re.escape(proj), head, re.M) is not None
            except OSError:
                hit = False
        if hit:
            m = DATE_RE.search(lf.name)
            if m:
                candidates.append((m.group(1), "日志"))
    # 2) 正文 **最后更新** / 最后活跃 / 最后工作（系统概览）
    overview = root / proj / "architecture" / "系统概览.md"
    texts = []
    if overview.exists():
        texts.append(overview)
    stub = root / proj / f"{proj}.md"
    if stub.exists():
        texts.append(stub)
    for t in texts:
        try:
            body = t.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        m = re.search(r"\*\*(?:最后更新|最后活跃|最后工作)\*\*[：:]\s*(\d{4}-\d{2}-\d{2})", body)
        if m:
            candidates.append((m.group(1), "正文"))
        m = re.search(r"^updated:\s*(\d{4}-\d{2}-\d{2})", body, re.M)
        if m:
            candidates.append((m.group(1), "frontmatter"))
    if not candidates:
        return None, None
    candidates.sort(key=lambda c: c[0], reverse=True)
    return candidates[0]


def count_todos(path, exclude_parts):
    n, items = 0, []
    for md in path.rglob("*.md"):
        if any(part in exclude_parts for part in md.relative_to(path).parts):
            continue
        try:
            body = md.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for line in body.splitlines():
            s = line.strip()
            if s.startswith("- [ ]"):
                n += 1
                items.append((md.stem, s[5:].strip()))
    return n, items


# 坑条目标题：## 或 ### + [PREFIX-日期-序号]，PREFIX ∈ ERR/BUG/INFRA/RISK（NOTE/P/OPS 非坑不计）
_GOTCHA_HDR = re.compile(r"^#{2,3}\s*\[((?:ERR|BUG|INFRA|RISK)-\d{6,8}-\d+)\]", re.M)
# 状态行兼容两种写法：**状态：**（冒号在加粗内，DVA）/ **状态**:（冒号在外，渊图）
_GOTCHA_STATUS = re.compile(r"\*\*状态\*\*[:：]?\s*(.+)|\*\*状态[:：]\*\*\s*(.+)")
_UNRESOLVED_MARKS = ("🔄", "⚠️", "⏳")  # 未闭环：待修复 / 已知风险 / 待解决·观察


def _gotcha_status(block):
    for line in block.splitlines()[1:6]:
        m = _GOTCHA_STATUS.search(line)
        if m:
            return (m.group(1) or m.group(2) or "").strip()
    return ""


def _is_unresolved(s):
    if not s or s.lstrip()[:1] == "✅":
        return False
    return any(k in s for k in _UNRESOLVED_MARKS)


def count_gotchas(root, proj):
    """数该项目「累计未消化的坑」：权威库 Projects/<proj>/GOTCHAS.md 为先，
    brain 索引/architecture 为补；按条目 ID 去重，只计状态含 🔄/⚠️/⏳ 的未闭环条目。"""
    cands = [root.parent / "Projects" / proj / "GOTCHAS.md",
             root / proj / "GOTCHAS.md",
             root / proj / "architecture" / "GOTCHAS.md",
             root / proj / "architecture" / "已知坑.md"]
    seen = {}
    for gp in cands:
        if not gp.exists():
            continue
        try:
            t = gp.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        ms = list(_GOTCHA_HDR.finditer(t))
        if not ms:
            continue
        bounds = [m.start() for m in ms] + [len(t)]
        for k, m in enumerate(ms):
            seen.setdefault(m.group(1), _is_unresolved(_gotcha_status(t[bounds[k]:bounds[k + 1]])))
    return sum(1 for v in seen.values() if v)


# ── 4 库新鲜度巡检（PRD 2026-06-15）──────────────────────────────
# 信号源 Doctor 锁定（2026-06-15）：路径相对 Database/ 根
DB_FRESHNESS_SOURCES = [
    {"name": "烛照九阴-复盘", "type": "mtime",
     "path": "烛照九阴/recap.db", "threshold_hours": 30},
    {"name": "剑酒青丘-行情", "type": "mtime",
     "path": "Market-Data/market_data.db", "threshold_hours": 50},
    {"name": "白泽大宗-商品", "type": "ingest_meta",
     "path": "宏观-大宗商品/business_breakdown.db", "threshold_hours": 192},  # 周更(周日14:30单轨,cron已退役)→8天阈值,只在真漏跑周日时报警(Doctor 2026-06-16)
    {"name": "DVA-视频", "type": "watchlist",
     "path": "Douyin/DVA-Database/indexes/watchlist.json", "threshold_hours": 168},
]

CST = timezone(timedelta(hours=8))


def _parse_ts(s):
    """解析时间戳→aware UTC datetime。结尾 Z=UTC；带 offset 用之；naive 视作 GMT+8。失败返回 None。"""
    if not s or not isinstance(s, str):
        return None
    s = s.strip()
    try:
        if s.endswith("Z"):
            return datetime.fromisoformat(s[:-1]).replace(tzinfo=timezone.utc)
        dt = datetime.fromisoformat(s)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=CST)
        return dt.astimezone(timezone.utc)
    except ValueError:
        m = DATE_RE.search(s)
        if m:
            return datetime.fromisoformat(m.group(1)).replace(tzinfo=CST).astimezone(timezone.utc)
        return None


def db_freshness(db_root, now_utc):
    """对 4 库取最新更新时间 → [{name,path,last_update,age_hours,threshold_hours,stale,detail}]。
    两类信号：mtime（文件本体）/ ingest_meta（max last_success_at）/ watchlist（enabled 作者 max lastUpdatedAt）。
    缺失或读取异常一律优雅降级为 last_update=None、stale=False（绝不误报红、绝不编数）。"""
    out = []
    for cfg in DB_FRESHNESS_SOURCES:
        p = db_root / cfg["path"]
        last_utc, detail = None, ""
        try:
            if not p.exists():
                detail = "路径缺失"
            elif cfg["type"] == "mtime":
                last_utc = datetime.fromtimestamp(p.stat().st_mtime, timezone.utc)
                detail = "文件 mtime"
            elif cfg["type"] == "ingest_meta":
                import sqlite3
                con = sqlite3.connect(f"file:{p}?mode=ro", uri=True)
                try:
                    rows = con.execute(
                        "SELECT last_success_at, last_status FROM ingest_meta").fetchall()
                finally:
                    con.close()
                ts = [t for t in (_parse_ts(r[0]) for r in rows) if t]
                if ts:
                    last_utc = max(ts)
                n_ok = sum(1 for r in rows if (r[1] or "").lower() == "ok")
                detail = f"{len(rows)}源·{n_ok}ok"
            elif cfg["type"] == "watchlist":
                # Doctor 2026-06-16：DVA 新鲜度 = 常更表(watchlist)在册作者的"真实最近更新"——
                # 逐个去同目录 global-index.json 查 per-author updatedAt 取 max。
                # （注：watchlist per-author lastUpdatedAt 自 2026-06 起已有值——但库级新鲜度仍按
                #   Doctor 2026-06-16 决议用 global-index updatedAt 取 max；per-author 更新时刻另由
                #   dva_authors() 取 watchlist.lastUpdatedAt 喂常更作者日报。顶层 updatedAt 仅 refill 才动、不用。）
                data = json.loads(p.read_text(encoding="utf-8", errors="ignore"))
                en = [a for a in data.get("authors", []) if a.get("enabled")]
                gi_auth = {}
                try:
                    gi = json.loads((p.parent / "global-index.json").read_text(encoding="utf-8", errors="ignore"))
                    if isinstance(gi.get("authors"), dict):
                        gi_auth = gi["authors"]
                except Exception:
                    gi_auth = {}
                ts = [t for t in (_parse_ts((gi_auth.get(a.get("sec_uid")) or {}).get("updatedAt")) for a in en) if t]
                if ts:
                    last_utc = max(ts)
                if last_utc is None:                      # 兜底：global-index 查不到 → 退回常更表顶层 updatedAt
                    last_utc = _parse_ts(data.get("updatedAt"))
                detail = f"{len(en)}作者" + ("" if last_utc else "·未跑")
        except Exception as e:  # noqa: BLE001 — 任何异常都降级，不让单库拖垮整张快照
            detail = "读取异常:" + str(e)[:40]

        if last_utc is not None:
            age_h = round((now_utc - last_utc).total_seconds() / 3600, 1)
            stale = age_h > cfg["threshold_hours"]
            last_iso = last_utc.astimezone(CST).strftime("%Y-%m-%dT%H:%M:%S+08:00")
        else:
            age_h, stale, last_iso = None, False, None

        out.append({
            "name": cfg["name"], "path": cfg["path"],
            "last_update": last_iso, "age_hours": age_h,
            "threshold_hours": cfg["threshold_hours"], "stale": stale,
            "detail": detail,
        })
    return out


# DVA 常更作者日报 · 全数据驱动 (Doctor 2026-06-22 方案②)。
# 每作者实时计数 + 按 mode(目标管线) 算状态。数据源：
#   - downloaded：Douyin/Downloaded/<nickname>/post 下递归 mp4 计数（实拍视频文件）
#   - ingested：global-index per-author videoCount（回退 authors/<sec>/videos/ 计数）
#   - transcribed/pending/unchecked：读 per-video json 的 subtitle_status（已识别/待识别/未检查）
#   - level1：per-video json 有 level1 分析的条数
#   - mode（watchlist）：full=全链 / transcribe-only=转写 / download-only=仅下载 → 决定完成判据
#   - last_update：watchlist.lastUpdatedAt（管线上次成功拉取该作者，逐人不同·名实相符）
# 不用 global-index updatedAt（索引重建时间·聚簇·混历史作者）。
DVA_WATCHLIST_PATH = "Douyin/DVA-Database/indexes/watchlist.json"
DVA_GLOBALINDEX_PATH = "Douyin/DVA-Database/indexes/global-index.json"
DVA_AUTHORS_DIR = "Douyin/DVA-Database/authors"
DVA_DOWNLOAD_DIR = "Douyin/Downloaded"
DVA_TOL = 3  # 「完成」容差：落后 ≤ 此数视作追平（防一拉新视频就从完成闪成进行中）


def _dva_dl_count(post_dir):
    if not post_dir.is_dir():
        return 0
    return sum(1 for f in post_dir.rglob("*") if f.suffix.lower() == ".mp4" and f.is_file())


def _dva_load_ignore(author_dir):
    """读 analyze-ignore.json，等价 dva.js loadAnalyzeIgnore：
    返回 (ids:set, patterns:[compiled re])。无文件 → (空, 空)。"""
    p = author_dir / "analyze-ignore.json"
    ids, pats = set(), []
    if not p.is_file():
        return ids, pats
    try:
        raw = json.loads(p.read_text(encoding="utf-8", errors="ignore"))
    except Exception:
        return ids, pats
    for it in (raw if isinstance(raw, list) else (raw.get("ids") or raw.get("ignore") or [])):
        aid = it if isinstance(it, str) else (it or {}).get("aweme_id")
        if aid:
            ids.add(str(aid))
    for it in ([] if isinstance(raw, list) else (raw.get("patterns") or [])):
        pat = it if isinstance(it, str) else (it or {}).get("pattern")
        if not pat:
            continue
        try:
            pats.append(re.compile(pat, re.IGNORECASE))  # 等价 new RegExp(p, 'i')
        except re.error:
            pass
    return ids, pats


def _dva_excluded_count(post_dir, ids, pats):
    """下载区 *_data.json 中命中排除规则的条数（id 精确 或 desc 命中任一正则）。"""
    if not post_dir.is_dir() or (not ids and not pats):
        return 0
    n = 0
    for f in post_dir.rglob("*_data.json"):
        if f.name.endswith("_comments.json"):
            continue
        try:
            d = json.loads(f.read_text(encoding="utf-8", errors="ignore"))
        except Exception:
            continue
        aid = str(d.get("aweme_id") or d.get("awemeId") or "")
        desc = d.get("desc") or d.get("title") or ""
        if (aid and aid in ids) or any(rx.search(desc) for rx in pats):
            n += 1
    return n


def _dva_video_stats(vdir):
    """读 per-video json 统计 转写/level1。返回 (ingested, transcribed, pending, unchecked, level1)。"""
    if not vdir.is_dir():
        return (0, 0, 0, 0, 0)
    trans = pend = unchk = lv1 = total = 0
    for vf in vdir.glob("*.json"):
        total += 1
        try:
            v = json.loads(vf.read_text(encoding="utf-8", errors="ignore"))
        except Exception:
            unchk += 1
            continue
        s = v.get("subtitle_status")
        if s == "已识别":
            trans += 1
        elif s == "待识别":
            pend += 1
        else:
            unchk += 1
        if v.get("level1"):
            lv1 += 1
    return (total, trans, pend, unchk, lv1)


def _dva_state(mode, dl, ing, trans, lv1):
    if dl == 0 and ing == 0:
        return "待启动"
    if mode == "download-only":
        return "完成"
    caught = (dl - ing) <= DVA_TOL
    if mode == "transcribe-only":
        return "完成" if (caught and (ing - trans) <= DVA_TOL and ing > 0) else "进行中"
    if mode == "full":
        return "完成" if (caught and (ing - lv1) <= DVA_TOL and ing > 0) else "进行中"
    return "进行中"


def dva_authors(db_root):
    p = db_root / DVA_WATCHLIST_PATH
    out = []
    try:
        data = json.loads(p.read_text(encoding="utf-8", errors="ignore"))
    except Exception:
        return out
    gi_auth = {}
    try:
        gi = json.loads((db_root / DVA_GLOBALINDEX_PATH).read_text(encoding="utf-8", errors="ignore"))
        if isinstance(gi.get("authors"), dict):
            gi_auth = gi["authors"]
    except Exception:
        gi_auth = {}
    for a in data.get("authors", []):
        if not a.get("enabled"):
            continue
        nick = a.get("nickname") or a.get("sec_uid") or "?"
        sec = a.get("sec_uid") or ""
        mode = a.get("mode") or ""
        rec = {
            "nickname": nick, "category": a.get("category") or "", "mode": mode,
            "downloaded": 0, "ingested": 0, "transcribed": 0,
            "pending": 0, "unchecked": 0, "level1": 0, "excluded": 0, "state": "进行中",
        }
        try:
            post_dir = db_root / DVA_DOWNLOAD_DIR / nick / "post"
            rec["downloaded"] = _dva_dl_count(post_dir)
            ing, trans, pend, unchk, lv1 = _dva_video_stats(db_root / DVA_AUTHORS_DIR / sec / "videos")
            gc = (gi_auth.get(sec) or {}).get("videoCount")
            rec["ingested"] = gc if gc is not None else ing
            rec["transcribed"], rec["pending"], rec["unchecked"], rec["level1"] = trans, pend, unchk, lv1
            # 排除项（analyze-ignore.json，入库/ASR/分析三处共用）：下载里命中规则、永不入库的条数
            ig_ids, ig_pats = _dva_load_ignore(db_root / DVA_AUTHORS_DIR / sec)
            rec["excluded"] = _dva_excluded_count(post_dir, ig_ids, ig_pats)
            rec["state"] = _dva_state(mode, rec["downloaded"], rec["ingested"], trans, lv1)
        except Exception:
            pass  # 单作者异常降级，保留计数默认值、不拖垮快照
        last_utc = _parse_ts(a.get("lastUpdatedAt"))
        rec["last_update"] = last_utc.astimezone(CST).strftime("%Y-%m-%dT%H:%M:%S+08:00") if last_utc else None
        rec["status"] = a.get("lastUpdateStatus") or ""
        out.append(rec)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=None)
    ap.add_argument("--db-root", default=None, help="Database/ 根，默认 brain 上两级的 Documents/Database")
    args = ap.parse_args()
    root = Path(args.root) if args.root else Path(__file__).resolve().parent.parent
    db_root = Path(args.db_root) if args.db_root else (root.parent.parent / "Database")

    # 悬空 wikilink + 总笔记（复用 build-backlinks.py，只写 .index/）
    notes, dangling = -1, -1
    try:
        out = subprocess.run([sys.executable, str(root / ".tools" / "build-backlinks.py"), "--root", str(root)],
                             capture_output=True, text=True, timeout=120).stdout
        m = re.search(r"总笔记[：:]\s*(\d+)", out)
        if m: notes = int(m.group(1))
        m = re.search(r"悬空链接[：:]\s*(\d+)", out)
        if m: dangling = int(m.group(1))
    except Exception:
        pass
    if notes < 0:
        notes = sum(1 for _ in root.rglob("*.md"))

    logs_dir = root / "logs"
    log_files = sorted([p for p in logs_dir.glob("*.md")], key=lambda p: p.name, reverse=True)

    # 项目：顶层目录（带 stub 或 architecture），排除基础设施与数灵金融线
    projects = []
    for d in sorted(root.iterdir()):
        if not d.is_dir() or d.name.startswith(".") or d.name in EXCLUDE_TOP:
            continue
        if not ((d / f"{d.name}.md").exists() or (d / "architecture").is_dir()):
            continue
        last, src = project_last_active(root, d.name, log_files)
        tn, _ = count_todos(d, TODO_EXCLUDE_PARTS)
        projects.append({"name": d.name, "last": last, "src": src,
                         "todos": tn, "gotchas": count_gotchas(root, d.name)})
    projects.sort(key=lambda p: p["last"] or "0000", reverse=True)

    # 金融项目（喂星空·项目星）——绕开 EXCLUDE_TOP，对三条金融线单取最后活跃
    finance_projects = []
    for name in FINANCE_PROJECTS:
        d = root / name
        if not d.is_dir():
            continue
        last, src = project_last_active(root, name, log_files)
        finance_projects.append({"name": name, "last": last, "src": src})

    # 全局 TODO（项目 + permanent + inbox + TODO.md）
    total_todos, todo_items = count_todos(root, TODO_EXCLUDE_PARTS | {"agents"})
    toptodos = [{"src": src, "text": txt[:90]} for src, txt in todo_items[:8]]

    # 数灵
    agents = []
    agent_log_entries = []
    for prof in AGENT_PROFILES:
        a = dict(prof)
        if a["name"] == "C.C.":
            a["logs"] = None
            a["last"] = latest_date_in_name(log_files[:1])
        else:
            adir = root / "agents" / a["name"] / "logs"
            afiles = sorted(adir.glob("*.md"), key=lambda p: p.name, reverse=True) if adir.exists() else []
            a["logs"] = len(afiles)
            a["last"] = latest_date_in_name(afiles)
            for f in afiles[:3]:
                agent_log_entries.append((f.name, a["name"] + " · " + f.stem))
        agents.append(a)
    agent_log_entries.sort(reverse=True)

    now_utc = datetime.now(timezone.utc)
    now = now_utc.astimezone(CST)

    # 数据库新鲜度（算一次，复用给链路）+ 金融链路状态
    dbf = db_freshness(db_root, now_utc)
    finance_chain = build_finance_chain(dbf)

    # 另落一份 status json（Doctor 2026-06-22：可被别的工具消费）
    try:
        status_doc = {
            "updated": now_utc.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "local_time": now.strftime("%Y-%m-%d %H:%M") + " (GMT+8)",
            **finance_chain,
        }
        (root / ".index" / "finance-chain-status.json").write_text(
            json.dumps(status_doc, ensure_ascii=False, indent=2), encoding="utf-8")
    except OSError:
        pass

    print(json.dumps({
        "timestamp": now_utc.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "local_time": now.strftime("%Y-%m-%d %H:%M") + " (GMT+8)",
        "notes": notes, "todos": total_todos, "dangling": dangling,
        "agents": agents, "projects": projects,
        "finance_projects": finance_projects,
        "logs": [p.stem for p in log_files[:7]],
        "agentlogs": [e[1] for e in agent_log_entries[:3]],
        "toptodos": toptodos,
        "db_freshness": dbf,
        "finance_chain": finance_chain,
        "dva_authors": dva_authors(db_root),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
