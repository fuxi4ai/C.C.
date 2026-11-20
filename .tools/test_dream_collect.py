#!/usr/bin/env python3
"""dream_collect v2 的行为测试（临时目录 + 合成数据）。运行：python3 -I ~/Documents/Claude/brain/.tools/test_dream_collect.py"""
import contextlib
import gzip
import importlib.util
import io
import json
import os
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

spec = importlib.util.spec_from_file_location("dc", Path(__file__).resolve().parent / "dream_collect.py")
DC = importlib.util.module_from_spec(spec)
spec.loader.exec_module(DC)
NOW = datetime(2026, 11, 20, 12, 0, tzinfo=timezone.utc)


def iso(d):
    return d.isoformat().replace("+00:00", "Z")


class T(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.b = Path(self.tmp.name) / "brain"
        (self.b / "permanent").mkdir(parents=True)
        (self.b / "logs").mkdir(parents=True)
        self.tl = self.b / "chats" / "transcripts" / "2026-11"
        self.tl.mkdir(parents=True)

    def tearDown(self):
        self.tmp.cleanup()

    def sess(self, name, last, title="t", sidechain=False, last_ts=True):
        h = {"type": "header", "title": title, "source": "code", "session_id": name, "sidechain": sidechain,
             "first_ts": iso(last - timedelta(hours=1)), "counts": {"text": 1}}
        if last_ts:
            h["last_ts"] = iso(last)
        with gzip.open(self.tl / name, "wt", encoding="utf-8") as g:
            g.write(json.dumps(h) + "\n")

    def touch(self, rel, when, text="x"):
        p = self.b / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")
        os.utime(p, (when.timestamp(), when.timestamp()))

    def tl_state(self, raw):
        (self.b / "chats" / "transcripts" / "_state.json").write_text(json.dumps({"last_run": raw}), encoding="utf-8")

    def test_window_capped_at_truth_layer_and_filters(self):
        DC.mark_run(self.b, iso(NOW - timedelta(days=1)), now=NOW - timedelta(days=1))
        self.tl_state("2026-11-20T03:40:00-0800")  # = 11:40Z，带不带冒号的时区都要能解析
        self.sess("a.jsonl.gz", NOW - timedelta(hours=5), "新会话")
        self.sess("late.jsonl.gz", NOW - timedelta(minutes=10), "抽取后才结束的会话")
        self.sess("b.jsonl.gz", NOW - timedelta(days=3), "旧会话")
        self.sess("s.jsonl.gz", NOW - timedelta(hours=4), "子代理", sidechain=True)
        self.sess("n.jsonl.gz", NOW - timedelta(hours=4), "无末次时间", last_ts=False)
        r = DC.collect(self.b, now=NOW)
        self.assertFalse(r["truth_layer"]["stale"])
        self.assertIsNone(r["truth_layer"]["error"])
        self.assertTrue(r["window"]["capped_at_truth_layer"])
        self.assertEqual([s["title"] for s in r["sessions"]], ["新会话"])
        self.assertEqual(r["sidechain_sessions"], 1)

    def test_pending_logs_ledger_and_skip_dirs(self):
        self.touch("logs/2026-11-20-x.md", NOW - timedelta(hours=2))
        self.touch("logs/dream/2026-11-20-dream.md", NOW - timedelta(hours=1))
        self.touch("logs/checkpoints/2026-11-19_x_PRD.md", NOW - timedelta(hours=1))
        self.touch("logs/checkups/c.md", NOW - timedelta(hours=1))
        self.touch("logs/2026-11/2026-11-18-y.md", NOW - timedelta(days=2))
        self.touch("logs/2026-11-01-old.md", NOW - timedelta(days=19))
        r = DC.collect(self.b, now=NOW)
        self.assertEqual(sorted(x["path"] for x in r["pending_logs"]), ["2026-11-20-x.md", "2026-11/2026-11-18-y.md"])
        DC.mark_processed(self.b, ["2026-11-20-x.md"])
        r = DC.collect(self.b, now=NOW)
        self.assertEqual([x["path"] for x in r["pending_logs"]], ["2026-11/2026-11-18-y.md"], "处理过的不再出现（中断续跑、同日重跑）")
        self.touch("logs/2026-11-20-x.md", NOW - timedelta(hours=1), text="后来改过")
        r = DC.collect(self.b, now=NOW)
        x = [l for l in r["pending_logs"] if l["path"] == "2026-11-20-x.md"]
        self.assertTrue(x and x[0]["seen_before"], "内容变了才重新进来，并标明以前处理过")

    def test_stale_and_parse_errors(self):
        self.tl_state(iso(NOW - timedelta(hours=60)))
        self.assertTrue(DC.collect(self.b, now=NOW)["truth_layer"]["stale"])
        self.tl_state("不是时间")
        r = DC.collect(self.b, now=NOW)["truth_layer"]
        self.assertIn("解析失败", r["error"])
        (self.b / "chats" / "transcripts" / "_state.json").unlink()
        self.assertIn("不存在", DC.collect(self.b, now=NOW)["truth_layer"]["error"])

    def test_future_truth_layer_last_run(self):
        self.tl_state(iso(NOW + timedelta(hours=2)))
        r = DC.collect(self.b, now=NOW)
        self.assertEqual(r["window"]["until"], NOW.isoformat(), "真相层时间在未来时终点取现在")

    def test_window_truncated_and_state_errors(self):
        DC.mark_run(self.b, iso(NOW - timedelta(days=10)), now=NOW - timedelta(days=10))
        r = DC.collect(self.b, max_days=7, now=NOW)
        self.assertEqual(r["window"]["since"], (NOW - timedelta(days=7)).isoformat())
        self.assertIsNotNone(r["window"]["skipped"])
        (self.b / "permanent" / "_dream_state.json").write_text("{坏", encoding="utf-8")
        r = DC.collect(self.b, now=NOW)
        self.assertIn("损坏", r["window"]["note"])
        self.assertEqual(r["window"]["since"], (NOW - timedelta(days=3)).isoformat())

    def test_mark_run_uses_until(self):
        DC.mark_run(self.b, iso(NOW - timedelta(hours=8)), now=NOW)
        r = DC.collect(self.b, now=NOW + timedelta(hours=1))
        self.assertEqual(r["window"]["since"], (NOW - timedelta(hours=8)).isoformat())

    def test_cli(self):
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(DC.main(["--brain", str(self.b / "nope")]), 2)
            self.assertEqual(DC.main(["--brain", str(self.b), "--mark-run"]), 2, "缺 --until 要拒绝")


    def test_search_since_newest_first_expiring(self):
        self.touch("logs/2026-11-13-old-topic.md", NOW - timedelta(days=6, hours=12))
        self.touch("logs/2026-11-20-new.md", NOW - timedelta(hours=1))
        r = DC.collect(self.b, now=NOW)
        paths = [x["path"] for x in r["pending_logs"]]
        self.assertEqual(paths, ["2026-11-20-new.md", "2026-11-13-old-topic.md"], "新的在前")
        old = r["pending_logs"][1]
        self.assertEqual(old["search_since"], "2026-11-10", "按日志自己的日期往前 3 天，不按本轮窗口")
        self.assertTrue(old["expiring"])
        self.tl_state(iso(NOW - timedelta(hours=2)))
        r2 = DC.collect(self.b, now=NOW)
        self.assertTrue(r2["pending_logs"][0]["after_truth_layer"], "晚于最近一次抽取写的日志，其会话还没进真相层")
        self.assertFalse(r["pending_logs"][0]["expiring"])

    def test_until_when_truth_layer_behind(self):
        DC.mark_run(self.b, iso(NOW - timedelta(hours=2)), now=NOW - timedelta(hours=2))
        self.tl_state(iso(NOW - timedelta(hours=26)))  # 抽取落后于上次窗口终点
        r = DC.collect(self.b, now=NOW)
        self.assertEqual(r["window"]["until"], r["window"]["since"], "真相层没追上时窗口为空，不前推")

    def test_baseline_and_first_run(self):
        self.touch("logs/2026-11-10-a.md", NOW - timedelta(days=5))
        self.touch("logs/2026-11-20-b.md", NOW - timedelta(hours=3))
        self.assertTrue(DC.collect(self.b, now=NOW)["first_run"])
        done = DC.baseline(self.b, 2, now=NOW)
        self.assertEqual(done, ["2026-11-10-a.md"])
        r = DC.collect(self.b, now=NOW)
        self.assertFalse(r["first_run"])
        self.assertEqual([x["path"] for x in r["pending_logs"]], ["2026-11-20-b.md"])

    def test_parse_variants(self):
        for raw in ["2026-11-19T23:45:21-0800", "2026-11-20T07:45:21.92Z", "2026-11-20T07:45:21.924Z", "2026-11-20T07:45:21+00:00"]:
            self.assertIsNotNone(DC._parse(raw), raw)

if __name__ == "__main__":
    unittest.main(verbosity=2)
