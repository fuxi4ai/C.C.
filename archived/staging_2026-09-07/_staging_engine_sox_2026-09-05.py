"""Deterministic daily event-shock shadow engine for EAL v3.

This first vertical slice measures a descriptive cluster-level daily shadow.
It never labels that shadow a causal total effect, never decomposes overlapping
events, and never treats same-day channels as controls. Intraday HFI and pooled
local projections remain later, gated stages.
"""

from __future__ import annotations

import math
import sqlite3
import statistics
from collections import defaultdict
from contextlib import closing
from dataclasses import asdict, dataclass
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from .canonical import canonical_sha256, sha256_file
from .clock import Session, effective_trade_date_interval, load_calendar, previous_trade_date
from .clusters import EventCluster, cluster_events
from .contracts import EventRecord, load_registry, validate_control_registry
from .errors import EALFailure, require


ENGINE_VERSION = "3.0.0-shadow.7"


DEFAULT_CONFIG: dict[str, Any] = {
    "schema_version": "eal-model-contract-v3.2",
    "engine_version": ENGINE_VERSION,
    "window_spec_id": "daily-0-1-3-5-v1",
    "calendar_version": "required-frozen-calendar-v1",
    "tzdata_version": "system-zoneinfo-recorded-by-caller",
    "horizons": [0, 1, 3, 5],
    "overlap_horizon": 5,
    "baseline_lookback": 60,
    "baseline_min_observations": 20,
    "market_data_as_of_utc": "REQUIRED",
    "market_data_snapshot": {
        "snapshot_id": "REQUIRED",
        "database_sha256": "REQUIRED",
        "source_version": "REQUIRED",
        "quality_status": "sealed_final",
        "observed_at_utc": "REQUIRED",
    },
    "data_finality_lag_hours": 24,
    "share_denominator_min_pp": 0.25,
    "controls": [],
    "targets": [
        {"ticker": "SPY", "kind": "return_pp", "role": "headline", "orientation": "higher_is_favorable"},
        {"ticker": "^VIX", "kind": "return_pp", "role": "response", "orientation": "neutral"},
        {"ticker": "CL=F", "kind": "return_pp", "role": "response", "orientation": "neutral"},
        {"ticker": "DGS2", "kind": "change_bp", "role": "response", "orientation": "neutral"},
        {"ticker": "DGS10", "kind": "change_bp", "role": "response", "orientation": "neutral"},
        {"ticker": "SMH", "kind": "return_pp", "role": "response", "orientation": "neutral"},
        {"ticker": "^SOX", "kind": "return_pp", "role": "response", "orientation": "neutral"},
    ],
    "sample_gates": {
        "case_only_max": 2,
        "directional_max": 5,
        "preliminary_max": 9,
        "provisional_min": 10,
        "candidate_min": 20,
        "minimum_independence_groups": 3,
    },
}


@dataclass(frozen=True)
class PriceSeries:
    ticker: str
    kind: str
    closes: dict[str, float]
    missing_dates: frozenset[str]
    source_versions: frozenset[str]

    def one_day_change(self, previous_date: str, current_date: str) -> float:
        previous = self.closes[previous_date]
        current = self.closes[current_date]
        if self.kind == "return_pp":
            require(previous > 0 and current > 0, "EAL_INVALID_PRICE", "price-return target requires positive closes", ticker=self.ticker, date=current_date)
            return (current / previous - 1.0) * 100.0
        if self.kind == "change_bp":
            return (current - previous) * 100.0
        raise EALFailure("EAL_CONFIG_INVALID", "unknown target kind", {"ticker": self.ticker, "kind": self.kind})

    def cumulative_change(self, previous_date: str, horizon_date: str) -> float:
        previous = self.closes[previous_date]
        current = self.closes[horizon_date]
        if self.kind == "return_pp":
            require(previous > 0 and current > 0, "EAL_INVALID_PRICE", "price-return target requires positive closes", ticker=self.ticker, date=horizon_date)
            return (current / previous - 1.0) * 100.0
        if self.kind == "change_bp":
            return (current - previous) * 100.0
        raise EALFailure("EAL_CONFIG_INVALID", "unknown target kind", {"ticker": self.ticker, "kind": self.kind})


def _validate_config(config: dict[str, Any]) -> dict[str, Any]:
    require(
        set(config) == set(DEFAULT_CONFIG),
        "EAL_CONFIG_INVALID",
        "model contract fields must match the registered schema exactly",
        missing=sorted(set(DEFAULT_CONFIG) - set(config)),
        extra=sorted(set(config) - set(DEFAULT_CONFIG)),
    )
    require(config.get("schema_version") == "eal-model-contract-v3.2", "EAL_CONFIG_INVALID", "unsupported model contract", observed=config.get("schema_version"))
    for field in ("engine_version", "window_spec_id", "calendar_version", "tzdata_version"):
        require(isinstance(config.get(field), str) and config[field].strip(), "EAL_CONFIG_INVALID", f"{field} must be a non-empty string")
    require(config["engine_version"] == ENGINE_VERSION, "EAL_ENGINE_VERSION_MISMATCH", "config engine_version does not match executable code", configured=config["engine_version"], executable=ENGINE_VERSION)
    as_of_raw = config.get("market_data_as_of_utc")
    require(isinstance(as_of_raw, str) and as_of_raw != "REQUIRED", "EAL_CONFIG_INVALID", "market_data_as_of_utc must be explicitly frozen")
    try:
        as_of = datetime.fromisoformat(as_of_raw.replace("Z", "+00:00"))
    except ValueError as exc:
        raise EALFailure("EAL_CONFIG_INVALID", "market_data_as_of_utc is invalid", {"value": as_of_raw}) from exc
    require(as_of.tzinfo is not None and as_of.utcoffset() is not None, "EAL_CONFIG_INVALID", "market_data_as_of_utc must be timezone-aware")
    normalized_as_of = as_of.astimezone(timezone.utc)
    require(
        normalized_as_of <= datetime.now(timezone.utc),
        "EAL_FUTURE_ATTESTATION",
        "market_data_as_of_utc cannot attest to a future observation time",
        market_data_as_of_utc=normalized_as_of.isoformat(),
    )
    config["market_data_as_of_utc"] = normalized_as_of.isoformat()
    snapshot = config.get("market_data_snapshot")
    require(isinstance(snapshot, dict), "EAL_CONFIG_INVALID", "market_data_snapshot must be a sealed-snapshot object")
    snapshot = dict(snapshot)
    config["market_data_snapshot"] = snapshot
    snapshot_fields = {"snapshot_id", "database_sha256", "source_version", "quality_status", "observed_at_utc"}
    require(set(snapshot) == snapshot_fields, "EAL_CONFIG_INVALID", "market_data_snapshot fields must match the registered schema exactly", missing=sorted(snapshot_fields - set(snapshot)), extra=sorted(set(snapshot) - snapshot_fields))
    for field in ("snapshot_id", "source_version"):
        require(isinstance(snapshot.get(field), str) and snapshot[field].strip() and snapshot[field] != "REQUIRED", "EAL_CONFIG_INVALID", f"market_data_snapshot.{field} must be explicitly frozen")
    snapshot_sha = snapshot.get("database_sha256")
    require(isinstance(snapshot_sha, str) and len(snapshot_sha) == 64 and all(character in "0123456789abcdef" for character in snapshot_sha), "EAL_CONFIG_INVALID", "market_data_snapshot.database_sha256 must be a lowercase SHA-256")
    require(snapshot.get("quality_status") == "sealed_final", "EAL_CONFIG_INVALID", "market data snapshot must be sealed_final", observed=snapshot.get("quality_status"))
    snapshot_observed_raw = snapshot.get("observed_at_utc")
    require(isinstance(snapshot_observed_raw, str) and snapshot_observed_raw != "REQUIRED", "EAL_CONFIG_INVALID", "market_data_snapshot.observed_at_utc must be explicitly frozen")
    try:
        snapshot_observed = datetime.fromisoformat(snapshot_observed_raw.replace("Z", "+00:00"))
    except ValueError as exc:
        raise EALFailure("EAL_CONFIG_INVALID", "market_data_snapshot.observed_at_utc is invalid", {"value": snapshot_observed_raw}) from exc
    require(snapshot_observed.tzinfo is not None and snapshot_observed.utcoffset() is not None, "EAL_CONFIG_INVALID", "market_data_snapshot.observed_at_utc must be timezone-aware")
    normalized_snapshot_observed = snapshot_observed.astimezone(timezone.utc).isoformat()
    require(normalized_snapshot_observed == config["market_data_as_of_utc"], "EAL_CONFIG_INVALID", "sealed snapshot observation time must equal market_data_as_of_utc", snapshot_observed_at_utc=normalized_snapshot_observed, market_data_as_of_utc=config["market_data_as_of_utc"])
    snapshot["observed_at_utc"] = normalized_snapshot_observed
    finality_lag = config.get("data_finality_lag_hours")
    require(isinstance(finality_lag, int) and not isinstance(finality_lag, bool) and finality_lag >= 0, "EAL_CONFIG_INVALID", "data_finality_lag_hours must be a non-negative integer")
    horizons = config.get("horizons")
    require(isinstance(horizons, list) and horizons, "EAL_CONFIG_INVALID", "horizons must be a non-empty list")
    require(all(isinstance(item, int) and not isinstance(item, bool) and item >= 0 for item in horizons), "EAL_CONFIG_INVALID", "horizons must be non-negative integers")
    require(horizons == sorted(set(horizons)), "EAL_NONCANONICAL_INPUT_ORDER", "horizons must be sorted and unique")
    require(0 in horizons, "EAL_CONFIG_INVALID", "horizons must include event day 0")
    require(isinstance(config.get("targets"), list) and config["targets"], "EAL_CONFIG_INVALID", "at least one target is required")
    target_names: set[str] = set()
    for target in config["targets"]:
        require(isinstance(target, dict), "EAL_CONFIG_INVALID", "target specification must be an object")
        require(set(target) == {"ticker", "kind", "role", "orientation"}, "EAL_CONFIG_INVALID", "target fields must match the registered schema exactly", target=target)
        require(target.get("kind") in {"return_pp", "change_bp"}, "EAL_CONFIG_INVALID", "invalid target kind", target=target)
        require(target.get("role") in {"headline", "response"}, "EAL_CONFIG_INVALID", "invalid target role", target=target)
        require(target.get("orientation") in {"higher_is_favorable", "lower_is_favorable", "neutral"}, "EAL_CONFIG_INVALID", "invalid target orientation", target=target)
        ticker = target.get("ticker")
        require(isinstance(ticker, str) and ticker, "EAL_CONFIG_INVALID", "target ticker is required")
        require(ticker not in target_names, "EAL_CONFIG_INVALID", "duplicate target ticker", ticker=ticker)
        target_names.add(ticker)
    require("SPY" in target_names, "EAL_CONFIG_INVALID", "SPY headline target is required")
    require(
        sum(1 for target in config["targets"] if target["role"] == "headline") == 1
        and next(target for target in config["targets"] if target["role"] == "headline")["ticker"] == "SPY",
        "EAL_CONFIG_INVALID",
        "SPY must be the sole headline target",
    )
    headline_target = next(target for target in config["targets"] if target["role"] == "headline")
    require(headline_target["kind"] == "return_pp", "EAL_CONFIG_INVALID", "SPY headline must use return_pp")
    require(headline_target["orientation"] == "higher_is_favorable", "EAL_CONFIG_INVALID", "SPY headline orientation must be frozen as higher_is_favorable")
    require(all(target["orientation"] == "neutral" for target in config["targets"] if target["role"] == "response"), "EAL_CONFIG_INVALID", "response targets must use neutral orientation in the daily shadow")
    require(isinstance(config.get("controls"), list), "EAL_CONFIG_INVALID", "controls must be a JSON list")
    registered_controls = validate_control_registry(config["controls"])
    require(
        not registered_controls,
        "EAL_CONTROL_IMPLEMENTATION_UNAVAILABLE",
        "the daily shadow does not yet implement adjusted pre-treatment controls; use an empty control registry",
        controls=registered_controls,
    )
    for field in ("overlap_horizon", "baseline_lookback", "baseline_min_observations"):
        require(isinstance(config.get(field), int) and not isinstance(config[field], bool) and config[field] >= 0, "EAL_CONFIG_INVALID", f"{field} must be a non-negative integer")
    require(
        config["overlap_horizon"] == max(horizons),
        "EAL_CONFIG_INVALID",
        "one cluster registry must use the widest reported horizon",
        overlap_horizon=config["overlap_horizon"],
        maximum_horizon=max(horizons),
    )
    require(config["baseline_min_observations"] >= 2, "EAL_CONFIG_INVALID", "baseline requires at least two observations")
    require(config["baseline_lookback"] >= config["baseline_min_observations"], "EAL_CONFIG_INVALID", "baseline lookback must cover minimum observations")
    denominator = config.get("share_denominator_min_pp")
    require(
        isinstance(denominator, (int, float))
        and not isinstance(denominator, bool)
        and math.isfinite(float(denominator))
        and float(denominator) > 0,
        "EAL_CONFIG_INVALID",
        "share denominator threshold must be finite and positive",
    )
    gates = config.get("sample_gates")
    require(isinstance(gates, dict), "EAL_CONFIG_INVALID", "sample_gates must be an object")
    required_gates = {"case_only_max", "directional_max", "preliminary_max", "provisional_min", "candidate_min", "minimum_independence_groups"}
    require(set(gates) == required_gates, "EAL_CONFIG_INVALID", "sample_gates fields are incomplete", missing=sorted(required_gates - set(gates)), extra=sorted(set(gates) - required_gates))
    require(all(isinstance(gates[name], int) and not isinstance(gates[name], bool) and gates[name] >= 1 for name in required_gates), "EAL_CONFIG_INVALID", "sample gates must be positive integers")
    require(
        gates == DEFAULT_CONFIG["sample_gates"],
        "EAL_CONFIG_INVALID",
        "sample gates must exactly match the registered model contract",
        expected=DEFAULT_CONFIG["sample_gates"],
        observed=gates,
    )
    require(
        gates["case_only_max"] < gates["directional_max"]
        < gates["preliminary_max"]
        < gates["provisional_min"]
        and gates["provisional_min"] <= gates["candidate_min"],
        "EAL_CONFIG_INVALID",
        "sample gates are not monotonic",
    )
    require(gates["provisional_min"] == gates["preliminary_max"] + 1, "EAL_CONFIG_INVALID", "provisional_min must immediately follow preliminary_max")
    return config


def _lexists(path: Path) -> bool:
    try:
        path.lstat()
    except FileNotFoundError:
        return False
    return True


def _require_no_sqlite_sidecars(db_path: Path) -> None:
    candidates = [db_path.with_name(db_path.name + suffix) for suffix in ("-wal", "-shm", "-journal")]
    present = [str(path) for path in candidates if _lexists(path)]
    require(
        not present,
        "EAL_DB_SNAPSHOT_UNSEALED",
        "SQLite sidecars are forbidden; freeze a checkpointed main-file snapshot before estimation",
        database=str(db_path),
        sidecars=present,
    )


def _load_prices(db_path: Path, targets: list[dict[str, str]]) -> dict[str, PriceSeries]:
    _require_no_sqlite_sidecars(db_path)
    uri = f"{db_path.as_uri()}?mode=ro"
    result: dict[str, PriceSeries] = {}
    # sqlite3.Connection.__exit__ manages the transaction but does not close
    # the handle.  Explicit closing matters for batch research runs.
    with closing(sqlite3.connect(uri, uri=True)) as database:
        database.execute("PRAGMA query_only = ON")
        journal_row = database.execute("PRAGMA journal_mode").fetchone()
        journal_mode = str(journal_row[0]).casefold() if journal_row else "unknown"
        require(
            journal_mode != "wal",
            "EAL_DB_SNAPSHOT_UNSEALED",
            "WAL-mode databases must be checkpointed into a frozen main-file snapshot",
            database=str(db_path),
            journal_mode=journal_mode,
        )
        data_version_before = int(database.execute("PRAGMA data_version").fetchone()[0])
        database.execute("BEGIN")
        table = database.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='prices_daily'").fetchone()
        require(table is not None, "EAL_DB_SCHEMA_MISSING", "prices_daily table is missing", path=str(db_path))
        columns = {
            row[1]
            for row in database.execute("PRAGMA table_info(prices_daily)").fetchall()
            if len(row) >= 2 and isinstance(row[1], str)
        }
        required_columns = {"ticker", "trade_date", "close", "source"}
        require(
            required_columns <= columns,
            "EAL_DB_SCHEMA_MISSING",
            "prices_daily is missing required columns",
            path=str(db_path),
            missing=sorted(required_columns - columns),
        )
        for target in targets:
            ticker = target["ticker"]
            rows = database.execute(
                "SELECT trade_date, close, source FROM prices_daily WHERE ticker=? ORDER BY trade_date, source",
                (ticker,),
            ).fetchall()
            require(rows, "EAL_PRICE_SERIES_MISSING", "target has no daily prices", ticker=ticker)
            closes: dict[str, float] = {}
            missing_dates: set[str] = set()
            seen_dates: set[str] = set()
            source_versions: set[str] = set()
            for trade_date, close, source in rows:
                require(
                    isinstance(trade_date, str)
                    and trade_date
                    and trade_date == trade_date.strip(),
                    "EAL_PRICE_DATE_INVALID",
                    "daily price trade_date must be a non-empty canonical string",
                    ticker=ticker,
                    trade_date=trade_date,
                )
                try:
                    parsed_date = date.fromisoformat(trade_date)
                except ValueError as exc:
                    raise EALFailure(
                        "EAL_PRICE_DATE_INVALID",
                        "daily price trade_date is invalid",
                        {"ticker": ticker, "trade_date": trade_date},
                    ) from exc
                require(
                    parsed_date.isoformat() == trade_date,
                    "EAL_PRICE_DATE_INVALID",
                    "daily price trade_date must use canonical YYYY-MM-DD form",
                    ticker=ticker,
                    trade_date=trade_date,
                )
                require(
                    isinstance(source, str) and source.strip(),
                    "EAL_PRICE_SOURCE_INVALID",
                    "daily price source must be a non-empty string",
                    ticker=ticker,
                    trade_date=trade_date,
                )
                source_versions.add(source.strip())
                require(trade_date not in seen_dates, "EAL_DUPLICATE_PRICE_KEY", "ticker/date appears under multiple sources", ticker=ticker, trade_date=trade_date, source=source)
                seen_dates.add(trade_date)
                if close is None:
                    missing_dates.add(trade_date)
                    continue
                require(
                    isinstance(close, (int, float)) and not isinstance(close, bool),
                    "EAL_INVALID_PRICE",
                    "daily close must be a numeric SQLite value",
                    ticker=ticker,
                    trade_date=trade_date,
                    observed_type=type(close).__name__,
                )
                number = float(close)
                require(math.isfinite(number), "EAL_NONFINITE_INPUT", "daily close must be finite", ticker=ticker, trade_date=trade_date)
                closes[trade_date] = number
            result[ticker] = PriceSeries(ticker, target["kind"], closes, frozenset(missing_dates), frozenset(source_versions))
        data_version_after = int(database.execute("PRAGMA data_version").fetchone()[0])
        database.execute("ROLLBACK")
        require(
            data_version_after == data_version_before,
            "EAL_INPUT_CHANGED_DURING_RUN",
            "SQLite data_version changed during the read snapshot",
            before=data_version_before,
            after=data_version_after,
        )
    _require_no_sqlite_sidecars(db_path)
    return result


def _event_excluded_dates(
    clusters: list[EventCluster],
    sessions: list[Session],
    *,
    maximum_horizon: int,
) -> set[str]:
    """Return every session that can contain an event-window outcome.

    The clustering horizon answers whether two events are independently
    identifiable.  It is not necessarily the longest reported outcome
    horizon.  Baselines must exclude the latter as well, otherwise a later
    event can learn its descriptive baseline from an earlier event's +5 response.
    """

    excluded: set[str] = set()
    for cluster in clusters:
        last_index = min(
            len(sessions) - 1,
            max(cluster.end_index, cluster.start_index + maximum_horizon),
        )
        for index in range(cluster.start_index, last_index + 1):
            excluded.add(sessions[index].trade_date)
    return excluded


def _baseline_changes(
    series: PriceSeries,
    sessions: list[Session],
    *,
    before_index: int,
    excluded_dates: set[str],
    lookback: int,
    as_of_utc: datetime,
    finality_lag_hours: int,
) -> tuple[list[float], list[str], list[str], list[str], list[str]]:
    changes: list[float] = []
    candidates: list[str] = []
    missing: list[str] = []
    unfinalized: list[str] = []
    excluded: list[str] = []
    start = max(1, before_index - lookback)
    for index in range(start, before_index):
        current_date = sessions[index].trade_date
        previous_date = sessions[index - 1].trade_date
        if current_date in excluded_dates or previous_date in excluded_dates:
            excluded.append(current_date)
            continue
        candidates.append(current_date)
        final_at = sessions[index].close_utc + timedelta(hours=finality_lag_hours)
        if as_of_utc < final_at:
            unfinalized.append(current_date)
            continue
        if previous_date not in series.closes or current_date not in series.closes:
            missing.append(current_date)
            continue
        change = series.one_day_change(previous_date, current_date)
        require(math.isfinite(change), "EAL_NONFINITE_DERIVED_CHANGE", "derived daily change is non-finite", ticker=series.ticker, trade_date=current_date)
        changes.append(change)
    return changes, candidates, missing, unfinalized, excluded


def _source_identification_eligibility(cluster: EventCluster) -> tuple[str, str]:
    """Grade the source design that a future estimator could exploit.

    This daily shadow estimator itself is always capped at ID-C.  Separating
    source eligibility from estimate identification prevents an exact event
    timestamp from silently upgrading a daily close-to-close estimate into a
    high-frequency quasi-experiment.
    """

    if len(cluster.events) != 1:
        return "not_eligible", "overlapping daily cluster has no separable source-design eligibility"
    event = cluster.events[0].event
    if event.purity != "clean" or event.timestamp_precision != "minute":
        return "not_eligible", "source inputs fail the clean minute-precision preconditions"
    if event.family in {"macro", "monetary_policy"} and event.scheduled and event.shock_value is not None and event.shock_unit in {"surprise_sigma", "target_bp", "path_bp"}:
        return "potential_ID_A_inputs", "candidate inputs only; full clock/source/expectation and high-frequency gates are not implemented"
    if event.family == "geopolitical" and event.shock_value is not None and event.shock_unit == "severity_grade":
        return "potential_ID_B_inputs", "candidate inputs only; full source-provenance and high-frequency gates are not implemented"
    return "not_assessed", "daily shadow does not assign a source-design identification grade"


def _baseline_moments(history: list[float]) -> tuple[float, float]:
    """Compute sample moments without avoidable intermediate overflow.

    Older CPython ``statistics.stdev`` implementations square deviations in
    the input scale.  Finite observations around 1e157 can therefore overflow
    internally even when their mathematically correct standard deviation is
    still a representable float.  Keep the ordinary path byte-for-byte stable,
    and use max-absolute scaling only when that implementation detail raises.
    """

    try:
        return statistics.fmean(history), statistics.stdev(history)
    except OverflowError:
        scale = max(abs(value) for value in history)
        if scale == 0.0:
            return 0.0, 0.0
        normalized = [value / scale for value in history]
        return statistics.fmean(normalized) * scale, statistics.stdev(normalized) * scale


def _target_effect(
    cluster: EventCluster,
    series: PriceSeries,
    target: dict[str, str],
    sessions: list[Session],
    excluded_dates: set[str],
    config: dict[str, Any],
) -> dict[str, Any]:
    start_index = cluster.start_index
    require(start_index > 0, "EAL_BASELINE_HISTORY_MISSING", "cluster lacks a prior session", cluster_id=cluster.cluster_id)
    previous_date = sessions[start_index - 1].trade_date
    as_of = datetime.fromisoformat(config["market_data_as_of_utc"])
    maximum_horizon = max(config["horizons"])
    last_member_index = max(item.start_index for item in cluster.events)
    final_index = last_member_index + maximum_horizon
    available_final_index = min(final_index, len(sessions) - 1)
    expected_window_indices = list(range(start_index, available_final_index + 1))
    window_price_indices = [start_index - 1, *expected_window_indices]
    window_missing = [
        sessions[index].trade_date
        for index in window_price_indices
        if as_of >= sessions[index].close_utc + timedelta(hours=config["data_finality_lag_hours"])
        and sessions[index].trade_date not in series.closes
    ]
    window_unfinalized = [
        sessions[index].trade_date
        for index in window_price_indices
        if as_of < sessions[index].close_utc + timedelta(hours=config["data_finality_lag_hours"])
    ]
    history, baseline_candidates, baseline_missing, baseline_unfinalized, baseline_excluded = _baseline_changes(
        series,
        sessions,
        before_index=start_index,
        excluded_dates=excluded_dates,
        lookback=config["baseline_lookback"],
        as_of_utc=as_of,
        finality_lag_hours=config["data_finality_lag_hours"],
    )
    minimum = config["baseline_min_observations"]
    snapshot_audit = {
        "market_data_snapshot_id": config["market_data_snapshot"]["snapshot_id"],
        "market_data_snapshot_database_sha256": config["market_data_snapshot"]["database_sha256"],
        "market_data_source_version": config["market_data_snapshot"]["source_version"],
        "observed_price_sources": sorted(series.source_versions),
    }
    baseline_complete = not baseline_missing and not baseline_unfinalized
    baseline_audit = {
        "baseline_complete": baseline_complete,
        "baseline_candidate_n": len(baseline_candidates),
        "baseline_used_n": len(history),
        "baseline_missing_dates": sorted(baseline_missing),
        "baseline_unfinalized_dates": sorted(baseline_unfinalized),
        "baseline_excluded_registered_event_dates": sorted(baseline_excluded),
    }
    if window_missing:
        return {
            "ticker": series.ticker,
            "status": "not_estimable",
            "reason": "missing_event_window_prices",
            "reason_code": "EAL_EVENT_WINDOW_PRICE_MISSING",
            **snapshot_audit,
            **baseline_audit,
            "window_missing_dates": sorted(window_missing),
            "window_unfinalized_dates": sorted(window_unfinalized),
            "horizons": [],
        }
    if final_index >= len(sessions):
        return {
            "ticker": series.ticker,
            "status": "not_estimable",
            "reason": "event_window_outside_frozen_calendar",
            "reason_code": "EAL_EVENT_WINDOW_CALENDAR_INCOMPLETE",
            **snapshot_audit,
            **baseline_audit,
            "window_missing_dates": [],
            "window_unfinalized_dates": sorted(window_unfinalized),
            "horizons": [],
        }
    if baseline_missing:
        return {
            "ticker": series.ticker,
            "status": "not_estimable",
            "reason": "missing_pre_event_baseline_prices",
            "reason_code": "EAL_BASELINE_PRICE_MISSING",
            **snapshot_audit,
            **baseline_audit,
            "window_missing_dates": sorted(window_missing),
            "window_unfinalized_dates": sorted(window_unfinalized),
            "horizons": [],
        }
    if baseline_unfinalized:
        return {
            "ticker": series.ticker,
            "status": "open",
            "reason": "unfinalized_pre_event_baseline_prices",
            "reason_code": "EAL_BASELINE_NOT_FINAL",
            **snapshot_audit,
            **baseline_audit,
            "window_missing_dates": sorted(window_missing),
            "window_unfinalized_dates": sorted(window_unfinalized),
            "horizons": [],
        }
    if len(history) < minimum:
        return {
            "ticker": series.ticker,
            "status": "not_estimable",
            "reason": "insufficient_pre_event_baseline",
            "reason_code": "EAL_BASELINE_INSUFFICIENT_OBSERVATIONS",
            **snapshot_audit,
            "baseline_n": len(history),
            **baseline_audit,
            "window_missing_dates": sorted(window_missing),
            "window_unfinalized_dates": sorted(window_unfinalized),
            "required": minimum,
            "horizons": [],
        }
    try:
        baseline_mean, baseline_sd = _baseline_moments(history)
    except (OverflowError, statistics.StatisticsError) as exc:
        raise EALFailure("EAL_NONFINITE_BASELINE", "baseline moments could not be computed", {"cluster_id": cluster.cluster_id, "ticker": series.ticker, "type": type(exc).__name__}) from exc
    require(math.isfinite(baseline_mean) and math.isfinite(baseline_sd), "EAL_NONFINITE_BASELINE", "baseline moments are non-finite", cluster_id=cluster.cluster_id, ticker=series.ticker)
    rows: list[dict[str, Any]] = []
    daily_path: list[tuple[int, float]] = []
    for index in expected_window_indices:
        horizon = index - last_member_index
        elapsed_sessions = index - start_index + 1
        horizon_date = sessions[index].trade_date
        if previous_date not in series.closes or horizon_date not in series.closes:
            break
        data_final_at = sessions[index].close_utc + timedelta(hours=config["data_finality_lag_hours"])
        if as_of < data_final_at:
            break
        observed = series.cumulative_change(previous_date, horizon_date)
        if series.kind == "return_pp":
            try:
                expected = (math.pow(1.0 + baseline_mean / 100.0, elapsed_sessions) - 1.0) * 100.0
            except OverflowError as exc:
                raise EALFailure(
                    "EAL_COMPOUND_OVERFLOW",
                    "registered descriptive baseline compound path overflowed",
                    {"cluster_id": cluster.cluster_id, "ticker": series.ticker, "elapsed_sessions": elapsed_sessions},
                ) from exc
            require(math.isfinite(expected), "EAL_COMPOUND_OVERFLOW", "registered descriptive baseline compound path is non-finite", cluster_id=cluster.cluster_id, ticker=series.ticker, elapsed_sessions=elapsed_sessions)
        else:
            expected = baseline_mean * elapsed_sessions
        shadow_gap = observed - expected
        require(all(math.isfinite(value) for value in (observed, expected, shadow_gap)), "EAL_NONFINITE_OUTPUT", "daily shadow gap is non-finite", cluster_id=cluster.cluster_id, ticker=series.ticker, horizon=horizon)
        sessions_from_cluster_start = index - start_index
        daily_path.append((horizon, shadow_gap))
        if horizon >= 0 and horizon in config["horizons"]:
            reference_se = baseline_sd * math.sqrt(elapsed_sessions)
            metric_id = "daily_shadow_compound_gap" if series.kind == "return_pp" else "daily_shadow_level_gap"
            row = {
                    "horizon": horizon,
                    "horizon_anchor": "last_cluster_member_effective_trade_date",
                    "elapsed_sessions_from_cluster_start": sessions_from_cluster_start,
                    "trade_date": horizon_date,
                    "data_final_at_utc": data_final_at.isoformat(),
                    "data_finality_status": "final",
                    "metric_id": metric_id,
                    "observed_path_change": round(observed, 8),
                    "registered_baseline_path_change": round(expected, 8),
                    "shadow_gap_value": round(shadow_gap, 8),
                    "reference_se": round(reference_se, 8),
                    "reference_interval_95": [
                        round(shadow_gap - 1.96 * reference_se, 8),
                        round(shadow_gap + 1.96 * reference_se, 8),
                    ],
                }
            row[metric_id] = round(shadow_gap, 8)
            rows.append(row)
    available = {row["horizon"] for row in rows}
    required_final_at = (
        sessions[final_index].close_utc + timedelta(hours=config["data_finality_lag_hours"])
        if final_index < len(sessions)
        else None
    )
    finality_complete = required_final_at is not None and as_of >= required_final_at
    complete = (
        all(horizon in available for horizon in config["horizons"])
        and finality_complete
        and not window_missing
        and not window_unfinalized
    )
    if not rows:
        return {
            "ticker": series.ticker,
            "status": "open",
            "reason": "data_finality_lag_not_elapsed",
            "reason_code": "EAL_EVENT_WINDOW_NOT_FINAL",
            **snapshot_audit,
            "baseline_n": len(history),
            **baseline_audit,
            "window_missing_dates": sorted(window_missing),
            "window_unfinalized_dates": sorted(window_unfinalized),
            "horizons": [],
        }
    trough_day, trough = min(daily_path, key=lambda item: item[1])
    peak_day, peak = max(daily_path, key=lambda item: item[1])
    half_recovery: int | None = None
    full_recovery: int | None = None
    if trough < 0:
        for horizon, value in daily_path:
            if horizon <= trough_day:
                continue
            if half_recovery is None and value >= trough / 2.0:
                half_recovery = horizon - trough_day
            if value >= 0:
                full_recovery = horizon - trough_day
                break
    result = {
        "ticker": series.ticker,
        "role": target["role"],
        "orientation": target["orientation"],
        "status": "final" if complete else "open",
        "reason": None if complete else "data_finality_lag_not_elapsed",
        "reason_code": None if complete else "EAL_EVENT_WINDOW_NOT_FINAL",
        "market_data_as_of_utc": config["market_data_as_of_utc"],
        "data_final_at_utc": required_final_at.isoformat() if required_final_at is not None else None,
        "unit": "pp" if series.kind == "return_pp" else "bp",
        "baseline_method": "trailing_non_registered_event_mean",
        "baseline_limitation": "unregistered_event_contamination_not_ruled_out",
        "descriptive_baseline_path_rule": "compound_daily_mean" if series.kind == "return_pp" else "add_daily_mean",
        "baseline_n": len(history),
        **baseline_audit,
        "window_missing_dates": sorted(window_missing),
        "window_unfinalized_dates": sorted(window_unfinalized),
        **snapshot_audit,
        "baseline_mean": round(baseline_mean, 8),
        "baseline_sd": round(baseline_sd, 8),
        "horizons": rows,
        "min_shadow_gap": round(trough, 8),
        "time_to_min_from_last_member": trough_day,
        "max_shadow_gap": round(peak, 8),
        "time_to_max_from_last_member": peak_day,
    }
    if target["role"] == "headline" and target["orientation"] == "higher_is_favorable":
        result.update(
            {
                "max_adverse_shadow_gap": round(trough, 8),
                "time_to_trough": trough_day,
                "max_favorable_shadow_gap": round(peak, 8),
                "time_to_peak": peak_day,
                "half_recovery_sessions_from_trough": half_recovery,
                "full_recovery_sessions_from_trough": full_recovery,
                "recovery_status": "not_applicable" if trough >= 0 else ("recovered" if full_recovery is not None else "right_censored"),
            }
        )
    return result


def _cluster_payload(
    cluster: EventCluster,
    series_by_ticker: dict[str, PriceSeries],
    sessions: list[Session],
    excluded_dates: set[str],
    config: dict[str, Any],
) -> dict[str, Any]:
    source_grade, source_grade_reason = _source_identification_eligibility(cluster)
    effects: list[dict[str, Any]] = []
    for target in config["targets"]:
        effect = _target_effect(cluster, series_by_ticker[target["ticker"]], target, sessions, excluded_dates, config)
        effect["role"] = target["role"]
        effect["orientation"] = target["orientation"]
        effects.append(effect)
    headline = next(item for item in effects if item["role"] == "headline")
    headline_status = "closed" if headline["status"] == "final" else ("open" if headline["status"] == "open" else "excluded")
    purity_clean = all(item.event.purity == "clean" for item in cluster.events)
    headline_clean_flag = headline_status == "closed" and purity_clean
    if headline_status != "closed":
        headline_clean_reason = f"headline_status={headline_status}"
    elif not purity_clean:
        headline_clean_reason = "member_purity_not_clean"
    else:
        headline_clean_reason = None
    for effect in effects:
        target_reportable = (
            effect["status"] == "final"
            and purity_clean
            and headline_status != "excluded"
        )
        if target_reportable:
            target_degradation: list[str] = []
        elif effect.get("reason_code"):
            target_degradation = [str(effect["reason_code"])]
        elif not purity_clean:
            target_degradation = ["EAL_CLUSTER_SOURCE_NOT_CLEAN"]
        else:
            target_degradation = ["EAL_CLUSTER_HEADLINE_NOT_CLEAN"]
        effect.update(
            {
                "identification_grade": "ID-C" if target_reportable else "ID-U",
                "source_confidence": source_grade,
                "statistical_precision": (
                    "descriptive_reference_interval"
                    if effect.get("horizons")
                    else "not_estimable"
                ),
                "degradation_codes": target_degradation,
            }
        )
        for horizon in effect.get("horizons", []):
            horizon_reportable = purity_clean and headline_status != "excluded"
            horizon.update(
                {
                    "identification_grade": "ID-C" if horizon_reportable else "ID-U",
                    "source_confidence": source_grade,
                    "statistical_precision": "descriptive_reference_interval",
                    "degradation_codes": (
                        []
                        if horizon_reportable
                        else [
                            "EAL_CLUSTER_SOURCE_NOT_CLEAN"
                            if not purity_clean
                            else "EAL_CLUSTER_HEADLINE_NOT_CLEAN"
                        ]
                    ),
                }
            )
    members = [
        {
            "event_id": item.event.event_id,
            "title": item.event.title,
            "canonical_event_id": item.event.canonical_event_id,
            "episode_id": item.event.episode_id,
            "independence_group_id": item.event.independence_group_id,
            "event_identity_sha256": item.event.identity_sha256,
            "family": item.event.family,
            "purity": item.event.purity,
            "transition": item.event.transition,
            "effective_trade_date": item.effective_trade_date,
            "shock_value": item.event.shock_value,
            "shock_unit": item.event.shock_unit,
            "severity_rubric_version": item.event.severity_rubric_version,
            "classification_id": item.event.classification_id,
            "taxonomy_version": item.event.taxonomy_version,
            "subtype": item.event.subtype,
            "expected_direction": item.event.expected_direction,
            "severity_ordinal": item.event.severity_ordinal,
            "classifier_type": item.event.classifier_type,
            "classifier_version": item.event.classifier_version,
            "classified_at_utc": item.event.classified_at_utc.isoformat(),
            "classification_rationale_ref": item.event.classification_rationale_ref,
            "source_ref": item.event.source_ref,
            "first_public_ts_utc": item.event.first_public_ts_utc.isoformat() if item.event.first_public_ts_utc else None,
            "timestamp_precision": item.event.timestamp_precision,
            "first_public_lower_utc": item.event.first_public_lower_utc.isoformat(),
            "first_public_upper_utc": item.event.first_public_upper_utc.isoformat(),
            "clock_quality": item.event.clock_quality,
            "source_published_at_raw": item.event.source_published_at_raw,
            "source_timezone": item.event.source_timezone,
            "fact_schema_version": item.event.fact_schema_version,
            "fact_payload": item.event.fact_payload,
            "classification_input_sha256": item.event.classification_input_sha256,
            "state_type": item.event.state_type,
            "state_before": item.event.state_before,
            "state_after": item.event.state_after,
            "state_before_trade_date": item.event.state_before_trade_date,
            "state_known_at_utc": item.event.state_known_at_utc.isoformat(),
            "state_rule_version": item.event.state_rule_version,
            "state_snapshot_sha256": item.event.state_snapshot_sha256,
            "state_source_kind": item.event.state_source_kind,
            "state_source_ref": item.event.state_source_ref,
        }
        for item in cluster.events
    ]
    # A daily shadow gap is not itself an identified structural effect.
    # Therefore even a one-event cluster must not be rendered as a mechanical
    # 100% contribution.  A future registered effect model may populate this
    # field after passing its own identification and denominator gates.
    share: float | None = None
    share_reason = (
        "overlap_unidentified"
        if len(cluster.events) > 1
        else "registered_effect_model_required"
    )
    return {
        "cluster_id": cluster.cluster_id,
        "cluster_identity_sha256": cluster.cluster_identity_sha256,
        "cluster_identity_material": cluster.cluster_identity_material,
        "cluster_rule_version": cluster.cluster_rule_version,
        "start_trade_date": sessions[cluster.start_index].trade_date,
        "end_trade_date": sessions[cluster.end_index].trade_date,
        "last_member_effective_trade_date": max(item.effective_trade_date for item in cluster.events),
        "cluster_family": cluster.family,
        "state_type": members[0]["state_type"] if len({item["state_type"] for item in members}) == 1 else "mixed",
        "transition": cluster.transition,
        "headline_status": headline_status,
        "headline_clean_flag": headline_clean_flag,
        "headline_clean_reason": headline_clean_reason,
        "separation_status": cluster.separation_status,
        "separation_reason_code": cluster.separation_reason_code,
        "component_weights": None,
        "component_weights_reason": "overlap_unidentified" if len(cluster.events) > 1 else "not_a_multi_component_cluster",
        "estimate_identification_grade": "ID-C" if headline_clean_flag else "ID-U",
        "estimate_identification_reason": "daily close-to-close descriptive headline shadow" if headline_clean_flag else headline_clean_reason,
        "source_identification_eligibility": source_grade,
        "source_identification_eligibility_reason": source_grade_reason,
        "members": members,
        "targets": effects,
        "model_implied_share_of_shadow_gap": share,
        "share_reason": share_reason,
    }


def _sample_level(n: int, gates: dict[str, int]) -> str:
    if n <= gates["case_only_max"]:
        return "case_only"
    if n <= gates["directional_max"]:
        return "directional_exploration"
    if n < gates["provisional_min"]:
        return "preliminary_pooling"
    if n < gates["candidate_min"]:
        return "provisional_band"
    return "confirmation_candidate"


def _aggregate_bands(clusters: list[dict[str, Any]], config: dict[str, Any]) -> list[dict[str, Any]]:
    """Pool only closed-clean headline effects, with episode as the independent unit."""

    buckets: dict[
        tuple[str, str, str, str, str, str, str, int, str, str, str],
        list[tuple[str, str, str, float | None, float]],
    ] = defaultdict(list)
    for cluster in clusters:
        if len(cluster["members"]) != 1 or cluster["headline_status"] != "closed" or cluster["headline_clean_flag"] is not True:
            continue
        member = cluster["members"][0]
        shock = member["shock_value"]
        unit = member["shock_unit"]
        headline = next(item for item in cluster["targets"] if item["role"] == "headline")
        if headline["status"] != "final":
            continue
        for row in headline["horizons"]:
            rubric = str(member.get("severity_rubric_version") or "not_applicable")
            key = (
                "DAILY_SHADOW",
                config["window_spec_id"],
                headline["ticker"],
                row["metric_id"],
                member["family"],
                member["state_type"],
                member["state_rule_version"],
                member["transition"],
                row["horizon"],
                unit,
                rubric,
            )
            buckets[key].append(
                (
                    cluster["cluster_id"],
                    member["episode_id"],
                    member["independence_group_id"],
                    float(shock) if shock is not None else None,
                    float(row["shadow_gap_value"]),
                )
            )

    output: list[dict[str, Any]] = []
    gates = config["sample_gates"]
    for key in sorted(buckets):
        estimand_id, window_spec_id, target_series_id, metric_id, family, state_type, state_rule_version, transition, horizon, unit, rubric = key
        values = buckets[key]
        by_episode: dict[str, list[tuple[str, float | None, float]]] = defaultdict(list)
        for _, episode_id, independence_group_id, shock, impact in values:
            by_episode[episode_id].append((independence_group_id, shock, impact))
        episode_points: list[tuple[str, str, float | None, float]] = []
        for episode_id, points in sorted(by_episode.items()):
            shock_values = [point[1] for point in points if point[1] is not None]
            episode_points.append(
                (
                    episode_id,
                    points[0][0],
                    statistics.fmean(shock_values) if shock_values else None,
                    statistics.fmean(point[2] for point in points),
                )
            )
        for episode_id, points in by_episode.items():
            require(len({point[0] for point in points}) == 1, "EAL_INDEPENDENCE_GROUP_CONFLICT", "one episode maps to multiple independence groups", episode_id=episode_id)
        by_independence_group: dict[str, list[tuple[float | None, float]]] = defaultdict(list)
        for _, group_id, shock, impact in episode_points:
            by_independence_group[group_id].append((shock, impact))
        independent_points: list[tuple[str, float | None, float]] = []
        for group_id, points in sorted(by_independence_group.items()):
            shock_values = [point[0] for point in points if point[0] is not None]
            independent_points.append(
                (
                    group_id,
                    statistics.fmean(shock_values) if shock_values else None,
                    statistics.fmean(point[1] for point in points),
                )
            )
        n_clusters = len(values)
        n_episodes = len(episode_points)
        n = len(independent_points)
        if n <= gates["case_only_max"]:
            continue
        impacts = [item[2] for item in independent_points]
        level = _sample_level(n, gates)
        slope: float | None = None
        intercept: float | None = None
        slope_reason: str | None = "insufficient_independent_episodes"
        slope_points = [item for item in independent_points if item[1] is not None] if unit not in {"none", "raw"} else []
        distinct_shocks = {item[1] for item in slope_points}
        if len(slope_points) >= gates["provisional_min"] and len(slope_points) >= gates["minimum_independence_groups"] and len(distinct_shocks) >= 2:
            shock_mean = statistics.fmean(float(item[1]) for item in slope_points)
            impact_mean = statistics.fmean(item[2] for item in slope_points)
            denominator = sum((float(item[1]) - shock_mean) ** 2 for item in slope_points)
            require(denominator > 0, "EAL_SHOCK_DESIGN_RANK_DEFICIENT", "shock design has zero variation", family=family, state_type=state_type, transition=transition, horizon=horizon)
            slope = sum((float(item[1]) - shock_mean) * (item[2] - impact_mean) for item in slope_points) / denominator
            intercept = impact_mean - slope * shock_mean
            slope_reason = None
        elif len(slope_points) >= gates["provisional_min"] and len(slope_points) >= gates["minimum_independence_groups"]:
            slope_reason = "insufficient_shock_variation"
        elif unit in {"none", "raw"}:
            slope_reason = "shock_scale_not_poolable"
        mean = statistics.fmean(impacts)
        se = statistics.stdev(impacts) / math.sqrt(n) if n > gates["directional_max"] else None
        output.append(
            {
                "estimand_id": estimand_id,
                "window_spec_id": window_spec_id,
                "target_series_id": target_series_id,
                "metric_id": metric_id,
                "family": family,
                "state_type": state_type,
                "state_rule_version": state_rule_version,
                "transition": transition,
                "horizon": horizon,
                "shock_unit": unit,
                "shock_scale_version": rubric,
                "n_clean_closed_clusters": n_clusters,
                "n_episodes": n_episodes,
                "n_independence_groups": n,
                "pooled_observation_unit": "independence_group_mean_after_episode_mean",
                "sample_level": level,
                "unit": "pp",
                "mean_shadow_gap": round(mean, 8),
                "median_shadow_gap": round(statistics.median(impacts), 8),
                "mean_ci_95": [round(mean - 1.96 * se, 8), round(mean + 1.96 * se, 8)] if se is not None else None,
                "positive_shadow_gap_rate": round(sum(1 for value in impacts if value > 0) / n, 8),
                "severity_intercept": round(intercept, 8) if intercept is not None else None,
                "severity_beta": round(slope, 8) if slope is not None else None,
                "severity_beta_reason": slope_reason,
                "n_slope_independence_groups": len(slope_points),
            }
        )
    return output


def _episode_recovery(clusters: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_episode: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for cluster in clusters:
        if len(cluster["members"]) == 1 and cluster["headline_status"] == "closed" and cluster["headline_clean_flag"] is True:
            member = cluster["members"][0]
            by_episode[member["episode_id"]].append(cluster)
    output: list[dict[str, Any]] = []
    for episode_id, rows in sorted(by_episode.items()):
        contracts = {
            (
                row["members"][0]["independence_group_id"],
                row["members"][0]["state_type"],
                row["members"][0]["state_rule_version"],
            )
            for row in rows
        }
        if len(contracts) != 1:
            output.append(
                {
                    "episode_id": episode_id,
                    "status": "not_estimable",
                    "reason": "incompatible_independence_or_state_contract",
                    "observed_contracts": [list(item) for item in sorted(contracts)],
                }
            )
            continue
        independence_group_id, state_type, state_rule_version = next(iter(contracts))
        entries = [row for row in rows if row["transition"] in {"entry", "escalation"}]
        exits = [row for row in rows if row["transition"] in {"exit", "easing"}]
        if not entries:
            output.append(
                {
                    "episode_id": episode_id,
                    "independence_group_id": independence_group_id,
                    "state_type": state_type,
                    "state_rule_version": state_rule_version,
                    "status": "not_estimable",
                    "reason": "missing_entry",
                }
            )
            continue
        if not exits:
            output.append(
                {
                    "episode_id": episode_id,
                    "independence_group_id": independence_group_id,
                    "state_type": state_type,
                    "state_rule_version": state_rule_version,
                    "status": "not_estimable",
                    "reason": "missing_exit_right_censored",
                }
            )
            continue
        valid_pairs: list[tuple[dict[str, Any], dict[str, Any]]] = []
        for entry in sorted(entries, key=lambda row: row["start_trade_date"]):
            entry_member = entry["members"][0]
            for exit_row in sorted(exits, key=lambda row: row["start_trade_date"]):
                exit_member = exit_row["members"][0]
                if exit_row["start_trade_date"] <= entry["end_trade_date"]:
                    continue
                if entry_member["state_after"] != exit_member["state_before"]:
                    continue
                valid_pairs.append((entry, exit_row))
                break
            if valid_pairs:
                break
        if not valid_pairs:
            output.append(
                {
                    "episode_id": episode_id,
                    "independence_group_id": independence_group_id,
                    "state_type": state_type,
                    "state_rule_version": state_rule_version,
                    "status": "not_estimable",
                    "reason": "no_time_ordered_state_continuous_entry_exit_pair",
                }
            )
            continue
        entry, exit_row = valid_pairs[0]
        entry_spy = next(item for item in entry["targets"] if item["ticker"] == "SPY")
        exit_spy = next(item for item in exit_row["targets"] if item["ticker"] == "SPY")
        if entry_spy["status"] != "final" or exit_spy["status"] != "final":
            output.append(
                {
                    "episode_id": episode_id,
                    "independence_group_id": independence_group_id,
                    "state_type": state_type,
                    "state_rule_version": state_rule_version,
                    "status": "not_estimable",
                    "reason": "entry_or_exit_spy_path_not_final",
                }
            )
            continue
        loss = abs(min(0.0, float(entry_spy["max_adverse_shadow_gap"])))
        rebound = max(0.0, float(exit_spy["max_favorable_shadow_gap"]))
        output.append(
            {
                "episode_id": episode_id,
                "independence_group_id": independence_group_id,
                "state_type": state_type,
                "state_rule_version": state_rule_version,
                "status": "final",
                "pairing_rule": "first_time_ordered_state_continuous_pair",
                "entry_cluster_id": entry["cluster_id"],
                "exit_cluster_id": exit_row["cluster_id"],
                "entry_max_adverse_pp": -loss,
                "exit_rebound_peak_pp": rebound,
                "recovery_ratio": round(rebound / loss, 8) if loss > 0 else None,
                "recovery_ratio_reason": None if loss > 0 else "entry_loss_not_negative",
            }
        )
    return output


def _aggregate_eligibility_ledger(clusters: list[dict[str, Any]]) -> list[dict[str, Any]]:
    ledger: list[dict[str, Any]] = []
    for cluster in clusters:
        if len(cluster["members"]) != 1:
            reason = "multi_member_cluster_not_pooled"
        elif cluster["headline_status"] != "closed":
            reason = f"headline_{cluster['headline_status']}"
        elif cluster["headline_clean_flag"] is not True:
            reason = str(cluster["headline_clean_reason"] or "headline_not_clean")
        else:
            reason = None
        ledger.append(
            {
                "cluster_id": cluster["cluster_id"],
                "eligible_for_descriptive_pool": reason is None,
                "reason": reason,
            }
        )
    return ledger


def _engine_tree_sha() -> str:
    root = Path(__file__).resolve().parent
    rows = []
    for path in sorted(root.glob("*.py"), key=lambda item: item.name):
        rows.append({"path": path.name, "sha256": sha256_file(path)})
    return canonical_sha256(rows)


def _require_event_metadata_observed_by(event: EventRecord, as_of_utc: datetime) -> None:
    timestamps: dict[str, datetime | None] = {
        "first_public_ts_utc": event.first_public_ts_utc,
        "first_public_lower_utc": event.first_public_lower_utc,
        "first_public_upper_utc": event.first_public_upper_utc,
        "classified_at_utc": event.classified_at_utc,
        "state_known_at_utc": event.state_known_at_utc,
        "expectation_known_at_utc": event.expectation_known_at_utc,
    }
    for field, observed_at in timestamps.items():
        if observed_at is None:
            continue
        require(
            observed_at <= as_of_utc,
            "EAL_EVENT_METADATA_AFTER_AS_OF",
            "frozen event metadata was not observable by the registered as-of time",
            event_id=event.event_id,
            field=field,
            observed_at_utc=observed_at.isoformat(),
            market_data_as_of_utc=as_of_utc.isoformat(),
        )


def run_event_study(
    *,
    db_path: str | Path,
    registry_path: str | Path,
    calendar_path: str | Path,
    config: dict[str, Any] | None = None,
) -> dict[str, Any]:
    config = _validate_config(dict(DEFAULT_CONFIG if config is None else config))
    db_source = Path(db_path).resolve()
    registry_source = Path(registry_path).resolve()
    calendar_source = Path(calendar_path).resolve()
    for source in (db_source, registry_source, calendar_source):
        require(source.exists() and source.is_file(), "EAL_INPUT_MISSING", "input file is missing", path=str(source))

    _require_no_sqlite_sidecars(db_source)
    hashes_before = {
        "database": sha256_file(db_source),
        "registry": sha256_file(registry_source),
        "calendar": sha256_file(calendar_source),
        "config": canonical_sha256(config),
        "engine": _engine_tree_sha(),
    }
    require(
        config["market_data_snapshot"]["database_sha256"] == hashes_before["database"],
        "EAL_MARKET_SNAPSHOT_MISMATCH",
        "sealed market-data snapshot hash does not match the input database",
        expected=config["market_data_snapshot"]["database_sha256"],
        observed=hashes_before["database"],
    )
    records, exclusions = load_registry(registry_source)
    diagnostics: list[dict[str, str]] = []
    sessions = load_calendar(calendar_source)
    frozen = [record for record in records if record.frozen]
    require(frozen, "EAL_NO_FROZEN_EVENTS", "registry has no frozen events eligible for estimation")
    registered_as_of = datetime.fromisoformat(config["market_data_as_of_utc"])
    for event in frozen:
        _require_event_metadata_observed_by(event, registered_as_of)
    mapped: list[tuple[EventRecord, str]] = []
    for event in frozen:
        require(event.first_public_ts_utc is not None, "EAL_CLOCK_MISSING", "frozen event lacks timestamp", event_id=event.event_id)
        trade_date = effective_trade_date_interval(
            event.first_public_lower_utc,
            event.first_public_upper_utc,
            sessions,
        )
        expected_state_date = previous_trade_date(trade_date, sessions)
        require(
            event.state_before_trade_date == expected_state_date,
            "EAL_STATE_LOOKAHEAD",
            "state snapshot is not the strict t-1 trading session",
            event_id=event.event_id,
            observed=event.state_before_trade_date,
            required=expected_state_date,
        )
        if event.legacy_trade_date and event.legacy_trade_date != trade_date:
            diagnostics.append(
                {
                    "event_id": event.event_id,
                    "code": "legacy_clock_mismatch",
                    "detail": f"{event.legacy_trade_date}->{trade_date}",
                }
            )
        mapped.append((event, trade_date))
    clusters = cluster_events(
        mapped,
        sessions,
        overlap_horizon=config["overlap_horizon"],
        window_spec_id=config["window_spec_id"],
    )
    prices = _load_prices(db_source, config["targets"])
    excluded_dates = _event_excluded_dates(
        clusters,
        sessions,
        maximum_horizon=max(config["horizons"]),
    )
    cluster_rows = [
        _cluster_payload(cluster, prices, sessions, excluded_dates, config)
        for cluster in clusters
    ]
    hashes_after = {
        "database": sha256_file(db_source),
        "registry": sha256_file(registry_source),
        "calendar": sha256_file(calendar_source),
    }
    _require_no_sqlite_sidecars(db_source)
    for name, observed in hashes_after.items():
        require(observed == hashes_before[name], "EAL_INPUT_CHANGED_DURING_RUN", "input changed during estimation", input=name, before=hashes_before[name], after=observed)

    aggregate_rows = _aggregate_bands(cluster_rows, config)
    recovery_rows = _episode_recovery(cluster_rows)
    aggregate_ledger = _aggregate_eligibility_ledger(cluster_rows)
    canonical: dict[str, Any] = {
        "schema_version": "eal-event-effects-v3.2",
        "engine_version": config["engine_version"],
        "method": "daily_cluster_compound_gap_shadow",
        "headline_estimand": "DAILY_SHADOW",
        "input_identity": hashes_before,
        "config": config,
        "row_accounting": {
            "raw_events": len(records),
            "frozen_events": len(frozen),
            "excluded_or_needs_coding": len([record for record in records if not record.frozen]),
            "clusters_total": len(clusters),
            "headline_closed_clusters": sum(row["headline_status"] == "closed" for row in cluster_rows),
            "headline_open_clusters": sum(row["headline_status"] == "open" for row in cluster_rows),
            "headline_excluded_clusters": sum(row["headline_status"] == "excluded" for row in cluster_rows),
            "headline_closed_clean_clusters": sum(row["headline_clean_flag"] is True for row in cluster_rows),
            "aggregate_eligible_clusters": sum(row["eligible_for_descriptive_pool"] is True for row in aggregate_ledger),
            "aggregate_rows": len(aggregate_rows),
            "recovery_rows": len(recovery_rows),
            "diagnostics": len(diagnostics),
        },
        "exclusions": sorted(exclusions, key=lambda item: (item["event_id"], item["reason"])),
        "diagnostics": sorted(diagnostics, key=lambda item: (item["event_id"], item["code"])),
        "clusters": cluster_rows,
        "aggregate_eligibility": aggregate_ledger,
        "aggregate_bands": aggregate_rows,
        "paired_episode_recovery": recovery_rows,
        "interpretation_guard": {
            "daily_layer_role": "descriptive_baseline_and_monitoring_only",
            "component_weights_for_overlap": "forbidden",
            "same_day_channels_are_outcomes_not_controls": True,
            "causal_claim": "not_established",
        },
    }
    canonical["result_id"] = canonical_sha256(canonical)
    audit = {
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "db_path": str(db_source),
        "registry_path": str(registry_source),
        "calendar_path": str(calendar_source),
    }
    return {"canonical": canonical, "audit": audit}
