#!/usr/bin/env python3
"""Read one Longyu record without importing engines or changing the database."""
import argparse
import datetime as dt
import json
import math
from pathlib import Path
import re
import sys

DIMENSIONS = {
    "政策与监管(5)": 5,
    "技术变革与供需(35)": 35,
    "竞争格局与产业链(25)": 25,
    "新赛道与未来预期(15)": 15,
    "估值与安全边际(15)": 15,
    "财务健康与风险(5)": 5,
}


class RecordError(ValueError):
    def __init__(self, code, message):
        super().__init__(message)
        self.code = code


def fail(code, message):
    raise RecordError(code, message)


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            fail("duplicate_key", f"Duplicate JSON key: {key}")
        result[key] = value
    return result


def reject_constant(value):
    fail("nonfinite_number", f"Non-finite JSON constant: {value}")


def finite_tree(value, location="$"):
    if isinstance(value, float) and not math.isfinite(value):
        fail("nonfinite_number", f"Non-finite number at {location}")
    if isinstance(value, dict):
        for key, item in value.items():
            finite_tree(item, f"{location}.{key}")
    elif isinstance(value, list):
        for index, item in enumerate(value):
            finite_tree(item, f"{location}[{index}]")


def date_value(value, field):
    if not isinstance(value, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        fail("invalid_date", f"{field} must be YYYY-MM-DD")
    try:
        return dt.date.fromisoformat(value)
    except ValueError:
        fail("invalid_date", f"Invalid calendar date in {field}: {value}")


def number(value, field):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        fail("invalid_number", f"{field} must be a finite number")
    try:
        valid = math.isfinite(value)
    except OverflowError:
        valid = False
    if not valid:
        fail("nonfinite_number", f"{field} must be a finite number")
    return value


def known_label(value):
    return isinstance(value, str) and value.strip().casefold() not in {
        "", "unknown", "unavailable", "n/a", "none", "null", "未知", "未核", "待定"
    }


def caliber_of(meta):
    """Keep raw caliber spelling; never normalize equivalent-looking versions."""
    found = []

    def visit(value, path):
        if isinstance(value, dict):
            for key, item in value.items():
                if key == "caliber" and isinstance(item, str) and item.strip():
                    found.append({"path": path + [key], "value": item})
                else:
                    visit(item, path + [key])
        elif isinstance(value, list):
            for index, item in enumerate(value):
                visit(item, path + [index])

    visit(meta, ["_meta"])
    values = {item["value"] for item in found}
    single = next(iter(values)) if len(values) == 1 else None
    return (single if known_label(single) else None), found


def validate_analysis(value, index):
    label = f"analyses[{index}]"
    if not isinstance(value, dict):
        fail("invalid_analysis", f"{label} must be an object")
    day = date_value(value.get("analysis_date"), f"{label}.analysis_date")
    if "打分日期" in value:
        scoring_day = date_value(value["打分日期"], f"{label}.打分日期")
        if scoring_day != day:
            fail("date_mismatch", f"{label}: analysis_date and 打分日期 must agree")
    dimensions = value.get("six_dim")
    if not isinstance(dimensions, dict) or set(dimensions) != set(DIMENSIONS):
        fail("invalid_dimensions", f"{label}.six_dim must contain exactly the six canonical keys")
    for key, maximum in DIMENSIONS.items():
        if dimensions[key] is None:
            continue
        score = number(dimensions[key], f"{label}.six_dim.{key}")
        if not 0 <= score <= maximum:
            fail("score_out_of_range", f"{label}.six_dim.{key} must be in [0, {maximum}]")
    if any(score is None for score in dimensions.values()):
        if value.get("total") is not None:
            fail("partial_total", f"{label}: incomplete dimensions cannot support a total")
    else:
        total = number(value.get("total"), f"{label}.total")
        if not math.isclose(total, sum(dimensions.values()), rel_tol=1e-9, abs_tol=1e-6):
            fail("total_mismatch", f"{label}.total does not reconcile with six_dim")
    scorer = value.get("scorer")
    if scorer is not None and not isinstance(scorer, str):
        fail("invalid_scorer", f"{label}.scorer must be a string or null")
    meta = value.get("_meta", {})
    if not isinstance(meta, dict):
        fail("invalid_meta", f"{label}._meta must be an object")
    facts = value.get("engine_facts")
    if facts is not None and not isinstance(facts, dict):
        fail("invalid_engine_facts", f"{label}.engine_facts must be an object or null")
    return day


def summarize(value, index, as_of):
    day = date_value(value["analysis_date"], "analysis_date")
    meta = value.get("_meta", {})
    caliber, fields = caliber_of(meta)
    raw_scorer = value.get("scorer")
    known_scorer = known_label(raw_scorer)
    facts = value.get("engine_facts")
    warnings = []
    missing_dimensions = [key for key, score in value["six_dim"].items() if score is None]
    score_status = ("unavailable" if len(missing_dimensions) == len(DIMENSIONS)
                    else "partial" if missing_dimensions else "complete")
    if missing_dimensions:
        warnings.append("incomplete_scores: null is unknown; total and trend unavailable")
    if not known_scorer:
        warnings.append("scorer_unknown: do not infer claude from missing scorer")
    if caliber is None:
        warnings.append("caliber_unknown_or_ambiguous: trend comparison unavailable")
    if not facts:
        warnings.append("engine_facts_missing: scores do not establish current financial facts")
    elif any(item is None for item in facts.values()):
        warnings.append("engine_facts_incomplete: null fields remain unknown")
    result = {key: value.get(key) for key in (
        "analysis_date", "source", "reviewer", "engine_facts", "report_path",
        "six_dim", "total", "rating", "thesis", "打分日期",
    )}
    result.update({
        "record_index": index,
        "scorer": raw_scorer if known_scorer else "unknown",
        "raw_scorer": raw_scorer,
        "scorer_present": "scorer" in value,
        "scorer_known": known_scorer,
        "caliber": caliber,
        "caliber_fields": fields,
        "_meta": meta,
        "age_calendar_days": (as_of - day).days,
        "score_status": score_status,
        "missing_dimensions": missing_dimensions,
        "warnings": warnings,
        "comparable_previous": None,
    })
    return result


def read_record(path, expected_code, as_of):
    if not isinstance(expected_code, str) or not expected_code.strip():
        fail("invalid_expected_code", "expected-code must be a nonempty exact security identifier")
    cutoff = date_value(as_of, "as_of")
    try:
        with Path(path).open("r", encoding="utf-8") as handle:
            record = json.load(handle, object_pairs_hook=unique_object, parse_constant=reject_constant)
    except (OSError, UnicodeError) as exc:
        fail("read_error", str(exc))
    except json.JSONDecodeError as exc:
        fail("invalid_json", str(exc))
    except RecordError:
        raise
    except ValueError as exc:
        # Includes Python's integer digit-limit rejection for hostile JSON.
        fail("invalid_json", str(exc))
    finite_tree(record)
    if not isinstance(record, dict):
        fail("invalid_root", "Record root must be an object")
    if record.get("ts_code") != expected_code:
        fail("identity_mismatch", f"Expected {expected_code!r}, got {record.get('ts_code')!r}")
    analyses = record.get("analyses")
    if not isinstance(analyses, list):
        fail("invalid_analyses", "analyses must be a list of objects")
    for field in ("latest", "updated_at"):
        if field in record:
            if field == "latest" and record[field] == "" and not analyses:
                continue
            date_value(record[field], field)
    groups = {}
    excluded = []
    for index, entry in enumerate(analyses):
        day = validate_analysis(entry, index)
        if day > cutoff:
            excluded.append({"record_index": index, "analysis_date": day.isoformat(),
                             "raw_scorer": entry.get("scorer")})
            continue
        # Preserve spelling and distinguish absent from explicit null/unknown.
        key = ("scorer" in entry, entry.get("scorer"))
        groups.setdefault(key, []).append(summarize(entry, index, cutoff))
    output = []
    for entries in groups.values():
        latest_date = max(item["analysis_date"] for item in entries)
        newest = [item for item in entries if item["analysis_date"] == latest_date]
        for item in newest:
            if len(newest) > 1:
                item["warnings"].append("same_scorer_date_tie: no arbitrary winner or trend")
            elif item["scorer_known"] and item["caliber"] and item["score_status"] == "complete":
                prior = [old for old in entries if old["analysis_date"] < latest_date
                         and old["caliber"] == item["caliber"]
                         and old["score_status"] == "complete"]
                if prior:
                    prior_date = max(old["analysis_date"] for old in prior)
                    matches = [old for old in prior if old["analysis_date"] == prior_date]
                    if len(matches) == 1:
                        old = matches[0]
                        item["comparable_previous"] = {key: old[key] for key in (
                            "record_index", "analysis_date", "raw_scorer", "caliber",
                            "_meta", "source", "reviewer", "report_path", "total",
                        )}
                    else:
                        item["warnings"].append("previous_date_tie: comparison unavailable")
            output.append(item)
    output.sort(key=lambda item: (item["scorer"], item["analysis_date"], item["record_index"]))
    return {
        "status": "ok", "record_path": str(Path(path).resolve()),
        "ts_code": record["ts_code"], "name": record.get("name"), "as_of": as_of,
        "root_latest": record.get("latest"), "root_latest_used_for_selection": False,
        "analysis_count": len(analyses), "future_excluded": excluded,
        "latest_by_scorer": output,
        "score_availability": ("unavailable" if not output or all(x["score_status"] == "unavailable" for x in output) else
                               "complete" if all(x["score_status"] == "complete" for x in output)
                               else "partial"),
        "warnings": ([] if output else ["no_analysis_on_or_before_as_of"]),
        "limitations": "Historical scores only; no current facts refresh, engine execution, or business trend inference. As-of filters record dates only: without a frozen historical snapshot or ingestion clock it does not establish point-in-time backtest eligibility.",
    }


class Parser(argparse.ArgumentParser):
    def error(self, message):
        fail("invalid_arguments", message)


def main(argv=None):
    parser = Parser(description=__doc__)
    parser.add_argument("--record", required=True)
    parser.add_argument("--expected-code", required=True)
    parser.add_argument("--as-of", default=dt.date.today().isoformat())
    try:
        args = parser.parse_args(argv)
        result = read_record(args.record, args.expected_code, args.as_of)
    except (RecordError, RecursionError) as exc:
        error = {"status": "error", "error": {
            "code": getattr(exc, "code", "excessive_nesting"), "message": str(exc)}}
        print(json.dumps(error, ensure_ascii=False, allow_nan=False), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, allow_nan=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
