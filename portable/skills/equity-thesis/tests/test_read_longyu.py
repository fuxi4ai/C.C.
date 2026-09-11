"""CLI acceptance tests; all mutations use temporary fixture copies."""
import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "read_longyu.py"
REAL_RECORD = Path("/Users/lunarabbit/Documents/Database/龙鱼-标的分析库/records/01879.HK_曦智科技.json")

# Financial values and metadata transcribed from the actual 01879.HK record,
# analysis date 2026-08-24; not synthetic current financial facts.
FIXTURE = {
    "ts_code": "01879.HK", "name": "曦智科技", "latest": "2026-08-24",
    "updated_at": "2026-08-24", "analyses": [{
        "analysis_date": "2026-08-24", "打分日期": "2026-08-24",
        "scorer": "claude", "source": "龙鱼库周更·CC自上而下维度级",
        "reviewer": "research-CC", "engine_facts": {},
        "six_dim": {"政策与监管(5)": 3.0, "技术变革与供需(35)": 23.0,
                    "竞争格局与产业链(25)": 13.0, "新赛道与未来预期(15)": 9.5,
                    "估值与安全边际(15)": 1.5, "财务健康与风险(5)": 2.5},
        "total": 52.5, "rating": "谨慎",
        "_meta": {"双scorer制度_周更": {
            "scorer": "claude", "method": "维度级整体判分·兑现折扣·维度正交·财务引擎真值",
            "caliber": "v2·维度正交+议价毛利率(2026-07-06锁)"}},
    }],
}


class ReaderTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / "record.json"
        self.fixture = copy.deepcopy(FIXTURE)

    def run_cli(self, fixture=None, raw=None, as_of="2026-09-10", expected="01879.HK"):
        self.path.write_text(raw if raw is not None else json.dumps(
            self.fixture if fixture is None else fixture, ensure_ascii=False), encoding="utf-8")
        before = self.path.read_bytes()
        before_mtime = self.path.stat().st_mtime_ns
        cmd = [sys.executable]
        if sys.flags.optimize:
            cmd.append("-O")
        cmd += [str(SCRIPT), "--record", str(self.path), "--expected-code", expected,
                "--as-of", as_of]
        result = subprocess.run(cmd, capture_output=True, text=True, check=False)
        self.assertEqual(before, self.path.read_bytes(), "Input content changed")
        self.assertEqual(before_mtime, self.path.stat().st_mtime_ns, "Input mtime changed")
        self.assertEqual(["record.json"], sorted(p.name for p in self.path.parent.iterdir()))
        return result, json.loads(result.stdout if result.returncode == 0 else result.stderr)

    def assert_error(self, code, **kwargs):
        result, output = self.run_cli(**kwargs)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "")
        self.assertEqual(output["error"]["code"], code)

    def test_actual_current_record_readonly(self):
        # A real source read, then a tmp copy is passed to the CLI.
        before = hashlib.sha256(REAL_RECORD.read_bytes()).hexdigest()
        actual = json.loads(REAL_RECORD.read_text(encoding="utf-8"))
        result, output = self.run_cli(fixture=actual)
        self.assertEqual(result.returncode, 0)
        self.assertEqual(output["ts_code"], "01879.HK")
        self.assertEqual(before, hashlib.sha256(REAL_RECORD.read_bytes()).hexdigest())

    def test_fixture_date_age_facts_and_caliber(self):
        result, output = self.run_cli()
        self.assertEqual(result.returncode, 0)
        item = output["latest_by_scorer"][0]
        self.assertEqual(item["total"], 52.5)
        self.assertEqual(item["age_calendar_days"], 17)
        self.assertEqual(item["caliber"], FIXTURE["analyses"][0]["_meta"]["双scorer制度_周更"]["caliber"])
        self.assertTrue(any("engine_facts_missing" in w for w in item["warnings"]))
        self.assertIsNone(item["comparable_previous"])

    def test_duplicate_keys_at_root_and_nested(self):
        for raw in ('{"ts_code":"01879.HK","ts_code":"01879.HK"}',
                    '{"x":{"a":1,"a":2}}'):
            with self.subTest(raw=raw):
                self.assert_error("duplicate_key", raw=raw)

    def test_nonfinite_anywhere(self):
        for token in ("NaN", "Infinity", "-Infinity", "1e999"):
            with self.subTest(token=token):
                self.assert_error("nonfinite_number", raw='{"x":' + token + '}')

    def test_wrong_identity(self):
        self.assert_error("identity_mismatch", expected="01878.HK")

    def test_malformed_json(self):
        self.assert_error("invalid_json", raw='{"unclosed":')
        self.assert_error("invalid_json", raw='{"huge":' + '9' * 5000 + '}')

    def test_dates(self):
        for date in ("2026-02-30", "2026-9-10", "tomorrow", None):
            with self.subTest(date=date):
                self.fixture["analyses"][0]["analysis_date"] = date
                self.assert_error("invalid_date")
        self.fixture = copy.deepcopy(FIXTURE)
        self.assert_error("invalid_date", as_of="2026-02-30")

    def test_dimension_bounds(self):
        for value in (-0.1, 5.1):
            self.fixture["analyses"][0]["six_dim"]["政策与监管(5)"] = value
            self.assert_error("score_out_of_range")

    def test_conflicting_scoring_date_rejected(self):
        self.fixture["analyses"][0]["打分日期"] = "2026-10-01"
        self.assert_error("date_mismatch")

    def test_real_partial_and_unscored_records(self):
        for name in ("688313.SH_仕佳光子.json", "300394.SZ_天孚通信.json", "09992.HK_泡泡玛特.json"):
            with self.subTest(name=name):
                actual = json.loads((REAL_RECORD.parent / name).read_text())
                result, output = self.run_cli(fixture=actual, expected=actual["ts_code"])
                self.assertEqual(result.returncode, 0)
                if actual["analyses"]:
                    engine = next(x for x in output["latest_by_scorer"] if x["raw_scorer"] == "engine")
                    self.assertEqual(engine["score_status"], "partial")
                    self.assertIsNone(engine["total"])
                    self.assertIsNone(engine["comparable_previous"])
                    self.assertTrue(any(x["score_status"] == "complete" for x in output["latest_by_scorer"]))
                else:
                    self.assertEqual(output["score_availability"], "unavailable")

    def test_partial_total_cannot_be_invented(self):
        self.fixture["analyses"][0]["six_dim"]["政策与监管(5)"] = None
        self.assert_error("partial_total")
        self.fixture["analyses"][0]["total"] = None
        self.assertEqual(self.run_cli()[1]["latest_by_scorer"][0]["score_status"], "partial")

    def test_all_unknown_dimensions_are_unavailable(self):
        entry = self.fixture["analyses"][0]
        entry["six_dim"] = dict.fromkeys(entry["six_dim"])
        entry["total"] = None
        _, output = self.run_cli()
        self.assertEqual(output["score_availability"], "unavailable")
        self.assertEqual(output["latest_by_scorer"][0]["score_status"], "unavailable")
        self.assertIsNone(output["latest_by_scorer"][0]["comparable_previous"])

    def test_empty_latest_only_for_empty_placeholder(self):
        self.fixture["latest"] = ""
        self.assert_error("invalid_date")
        self.fixture["analyses"] = []
        self.assertEqual(self.run_cli()[1]["score_availability"], "unavailable")

    def test_explicit_unknown_scorer_and_caliber_not_comparable(self):
        for label in ("unknown", "UNKNOWN", "未核"):
            self.fixture = copy.deepcopy(FIXTURE)
            self.fixture["analyses"][0]["scorer"] = label
            self.add_entry(scorer=label)
            item = self.run_cli()[1]["latest_by_scorer"][0]
            self.assertFalse(item["scorer_known"])
            self.assertEqual(item["raw_scorer"], label)
            self.assertIsNone(item["comparable_previous"])
            for entry in self.fixture["analyses"]:
                entry["scorer"] = "claude"
                entry["_meta"]["双scorer制度_周更"]["caliber"] = label
            item = self.run_cli()[1]["latest_by_scorer"][0]
            self.assertIsNone(item["caliber"])
            self.assertIsNone(item["comparable_previous"])

    def test_boolean_not_score(self):
        self.fixture["analyses"][0]["six_dim"]["政策与监管(5)"] = True
        self.assert_error("invalid_number")

    def test_total_mismatch_and_tolerance(self):
        self.fixture["analyses"][0]["total"] = 52.6
        self.assert_error("total_mismatch")
        self.fixture["analyses"][0]["total"] = 52.50000001
        self.assertEqual(self.run_cli()[0].returncode, 0)

    def test_exact_dimensions(self):
        self.fixture["analyses"][0]["six_dim"]["unexpected"] = 0
        self.assert_error("invalid_dimensions")

    def test_analyses_object_requirement(self):
        self.fixture["analyses"] = ["not an object"]
        self.assert_error("invalid_analysis")
        self.fixture["analyses"] = {}
        self.assert_error("invalid_analyses")

    def add_entry(self, day="2026-09-01", scorer="claude", caliber=None):
        item = copy.deepcopy(FIXTURE["analyses"][0])
        item["analysis_date"] = item["打分日期"] = day
        item["scorer"] = scorer
        if caliber is not None:
            item["_meta"]["双scorer制度_周更"]["caliber"] = caliber
        self.fixture["analyses"].append(item)
        return item

    def test_future_excluded_and_root_latest_not_selector(self):
        self.add_entry("2026-10-01")
        self.fixture["latest"] = "2026-10-01"
        _, output = self.run_cli()
        self.assertEqual(len(output["future_excluded"]), 1)
        self.assertEqual(output["latest_by_scorer"][0]["analysis_date"], "2026-08-24")
        self.assertFalse(output["root_latest_used_for_selection"])

    def test_future_malformed_still_fails(self):
        item = self.add_entry("2026-10-01")
        item["total"] = 99
        self.assert_error("total_mismatch")

    def test_all_future_is_explicit(self):
        _, output = self.run_cli(as_of="2026-08-01")
        self.assertEqual(output["latest_by_scorer"], [])
        self.assertIn("no_analysis_on_or_before_as_of", output["warnings"])

    def test_same_scorer_caliber_distinct_dates_comparable(self):
        self.add_entry()
        _, output = self.run_cli()
        item = output["latest_by_scorer"][0]
        self.assertEqual(item["analysis_date"], "2026-09-01")
        self.assertEqual(item["comparable_previous"]["analysis_date"], "2026-08-24")

    def test_mixed_caliber_not_comparable(self):
        self.add_entry(caliber="different-v3")
        _, output = self.run_cli()
        self.assertIsNone(output["latest_by_scorer"][0]["comparable_previous"])

    def test_empty_and_ambiguous_caliber(self):
        entry = self.add_entry(caliber="")
        self.assertIsNone(self.run_cli()[1]["latest_by_scorer"][0]["comparable_previous"])
        entry["_meta"]["other"] = {"caliber": "x"}
        entry["_meta"]["third"] = {"caliber": "y"}
        self.assertIsNone(self.run_cli()[1]["latest_by_scorer"][0]["caliber"])

    def test_raw_scorers_separate_and_missing_unknown(self):
        self.add_entry(scorer="deepseek")
        self.add_entry(scorer="codex")
        self.add_entry(scorer="Claude")
        unknown = self.add_entry()
        del unknown["scorer"]
        _, output = self.run_cli()
        self.assertEqual({x["scorer"] for x in output["latest_by_scorer"]},
                         {"claude", "deepseek", "codex", "Claude", "unknown"})
        unknown_output = next(x for x in output["latest_by_scorer"] if not x["scorer_known"])
        self.assertIsNone(unknown_output["raw_scorer"])
        self.assertIsNone(unknown_output["comparable_previous"])

    def test_tie_preserved_without_arbitrary_winner(self):
        self.add_entry("2026-08-24")
        _, output = self.run_cli()
        self.assertEqual(len(output["latest_by_scorer"]), 2)
        self.assertTrue(all(x["comparable_previous"] is None for x in output["latest_by_scorer"]))

    def test_missing_engine_facts(self):
        del self.fixture["analyses"][0]["engine_facts"]
        _, output = self.run_cli()
        self.assertIsNone(output["latest_by_scorer"][0]["engine_facts"])
        self.assertTrue(any("engine_facts_missing" in w for w in output["latest_by_scorer"][0]["warnings"]))

    def test_missing_required_argument_structured(self):
        result = subprocess.run([sys.executable, str(SCRIPT)], capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(json.loads(result.stderr)["error"]["code"], "invalid_arguments")


if __name__ == "__main__":
    unittest.main()
