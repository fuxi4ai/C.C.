#!/usr/bin/env python3
"""Fail-closed resolver for the EAL registry consumed by event-attribution-watch."""

from __future__ import annotations

import argparse
import hashlib
import importlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import sys
from datetime import date, datetime
from typing import Any


HEX_64 = re.compile(r"^[0-9a-f]{64}$")
MANIFEST_LINE = re.compile(r"^([0-9a-f]{64})  ([^\r\n]+)$")
REGISTRY_NAME = re.compile(r"^frozen-event-registry-v3\.2-(\d{8})([^/]*)\.jsonl$")
SCHEMA_REL = "schemas/frozen-event-registry-v3.schema.json"
CONTRACT_REL = "contracts.py"


class SelectorFailure(Exception):
    def __init__(self, code: str, message: str, **details: Any) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.details = details


def require(condition: bool, code: str, message: str, **details: Any) -> None:
    if not condition:
        raise SelectorFailure(code, message, **details)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def require_regular(path: Path, *, label: str) -> os.stat_result:
    try:
        info = path.lstat()
    except FileNotFoundError as exc:
        raise SelectorFailure("EAL_SELECTOR_INPUT_MISSING", f"{label} is missing", path=str(path)) from exc
    require(not stat.S_ISLNK(info.st_mode), "EAL_SELECTOR_SYMLINK_REJECTED", f"{label} must not be a symlink", path=str(path))
    require(stat.S_ISREG(info.st_mode), "EAL_SELECTOR_NOT_REGULAR_FILE", f"{label} must be a regular file", path=str(path))
    return info


def safe_relative_path(text: str) -> PurePosixPath:
    require("\\" not in text, "EAL_CONSUMER_MANIFEST_INVALID", "manifest paths must use POSIX separators", path=text)
    path = PurePosixPath(text)
    require(not path.is_absolute(), "EAL_CONSUMER_MANIFEST_INVALID", "manifest path must be relative", path=text)
    require(text == path.as_posix() and text not in {"", "."}, "EAL_CONSUMER_MANIFEST_INVALID", "manifest path is not canonical", path=text)
    require(".." not in path.parts, "EAL_CONSUMER_MANIFEST_INVALID", "manifest path escapes the EAL root", path=text)
    return path


def resolve_inside(root: Path, relative: str) -> Path:
    candidate = root.joinpath(*safe_relative_path(relative).parts)
    resolved_root = root.resolve(strict=True)
    resolved_candidate = candidate.resolve(strict=False)
    require(
        resolved_candidate == resolved_root or resolved_root in resolved_candidate.parents,
        "EAL_SELECTOR_PATH_ESCAPE",
        "resolved path escapes the EAL root",
        path=str(candidate),
    )
    return candidate


def parse_manifest(path: Path) -> tuple[dict[str, str], int]:
    info = require_regular(path, label="consumer manifest")
    raw = path.read_bytes()
    require(raw.endswith(b"\n"), "EAL_CONSUMER_MANIFEST_INVALID", "consumer manifest must end with a newline", path=str(path))
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise SelectorFailure("EAL_CONSUMER_MANIFEST_INVALID", "consumer manifest is not UTF-8", path=str(path)) from exc
    entries: dict[str, str] = {}
    for line_number, line in enumerate(text.splitlines(), start=1):
        match = MANIFEST_LINE.fullmatch(line)
        require(match is not None, "EAL_CONSUMER_MANIFEST_INVALID", "manifest line is not canonical", line=line_number)
        observed_sha, relative = match.groups()
        safe_relative_path(relative)
        require(relative not in entries, "EAL_CONSUMER_MANIFEST_DUPLICATE_PATH", "manifest contains a duplicate path", path=relative, line=line_number)
        entries[relative] = observed_sha
    require(entries, "EAL_CONSUMER_MANIFEST_INVALID", "consumer manifest is empty", path=str(path))
    return entries, info.st_size


def verify_manifest_tree(root: Path, entries: dict[str, str]) -> None:
    for relative, expected_sha in entries.items():
        path = resolve_inside(root, relative)
        require_regular(path, label="manifest artifact")
        observed_sha = sha256_file(path)
        require(
            observed_sha == expected_sha,
            "EAL_CONSUMER_MANIFEST_TREE_MISMATCH",
            "an artifact does not match CURRENT_SHA256SUMS",
            path=relative,
            observed=observed_sha,
            expected=expected_sha,
        )


def strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise SelectorFailure("EAL_REGISTRY_DUPLICATE_JSON_KEY", "JSON object contains a duplicate key", key=key)
        result[key] = value
    return result


def strict_json(raw: bytes, *, label: str) -> Any:
    try:
        text = raw.decode("utf-8")
        return json.loads(text, object_pairs_hook=strict_object, parse_constant=lambda value: (_ for _ in ()).throw(ValueError(value)))
    except SelectorFailure:
        raise
    except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
        raise SelectorFailure("EAL_REGISTRY_SCHEMA_INVALID", f"{label} is not strict JSON") from exc


def type_matches(value: Any, kind: str) -> bool:
    if kind == "null":
        return value is None
    if kind == "boolean":
        return isinstance(value, bool)
    if kind == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if kind == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if kind == "string":
        return isinstance(value, str)
    if kind == "object":
        return isinstance(value, dict)
    return False


def validate_format(value: str, expected: str, path: str) -> None:
    try:
        if expected == "date":
            parsed_date = date.fromisoformat(value)
            require(parsed_date.isoformat() == value, "EAL_REGISTRY_SCHEMA_INVALID", "date is not canonical", field=path)
        elif expected == "date-time":
            parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
            require(parsed.tzinfo is not None and parsed.utcoffset() is not None, "EAL_REGISTRY_SCHEMA_INVALID", "date-time lacks timezone", field=path)
        else:
            raise SelectorFailure("EAL_REGISTRY_SCHEMA_UNSUPPORTED", "schema uses an unsupported format", field=path, format=expected)
    except ValueError as exc:
        raise SelectorFailure("EAL_REGISTRY_SCHEMA_INVALID", "value does not match the declared format", field=path, format=expected) from exc


def validate_schema(value: Any, schema: dict[str, Any], path: str = "$") -> None:
    declared = schema.get("type")
    if declared is not None:
        choices = declared if isinstance(declared, list) else [declared]
        require(any(type_matches(value, kind) for kind in choices), "EAL_REGISTRY_SCHEMA_INVALID", "value has the wrong JSON type", field=path, expected=choices)
    if "const" in schema:
        require(value == schema["const"], "EAL_REGISTRY_SCHEMA_INVALID", "value differs from schema const", field=path)
    if "enum" in schema:
        require(value in schema["enum"], "EAL_REGISTRY_SCHEMA_INVALID", "value is outside schema enum", field=path)
    if isinstance(value, str):
        if "minLength" in schema:
            require(len(value) >= schema["minLength"], "EAL_REGISTRY_SCHEMA_INVALID", "string is shorter than minLength", field=path)
        if "pattern" in schema:
            require(re.search(schema["pattern"], value) is not None, "EAL_REGISTRY_SCHEMA_INVALID", "string does not match schema pattern", field=path)
        if "format" in schema:
            validate_format(value, schema["format"], path)
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if "minimum" in schema:
            require(value >= schema["minimum"], "EAL_REGISTRY_SCHEMA_INVALID", "number is below minimum", field=path)
        if "maximum" in schema:
            require(value <= schema["maximum"], "EAL_REGISTRY_SCHEMA_INVALID", "number is above maximum", field=path)
    if isinstance(value, dict):
        required = schema.get("required", [])
        missing = sorted(set(required) - set(value))
        require(not missing, "EAL_REGISTRY_SCHEMA_INVALID", "object lacks required fields", field=path, missing=missing)
        properties = schema.get("properties", {})
        if schema.get("additionalProperties") is False:
            extra = sorted(set(value) - set(properties))
            require(not extra, "EAL_REGISTRY_SCHEMA_INVALID", "object has additional fields", field=path, extra=extra)
        for key, child in properties.items():
            if key in value:
                validate_schema(value[key], child, f"{path}.{key}")
    for condition in schema.get("allOf", []):
        validate_schema(value, condition, path)
    if "if" in schema:
        try:
            validate_schema(value, schema["if"], path)
        except SelectorFailure:
            matched = False
        else:
            matched = True
        if matched and "then" in schema:
            validate_schema(value, schema["then"], path)
    if "not" in schema:
        try:
            validate_schema(value, schema["not"], path)
        except SelectorFailure:
            pass
        else:
            raise SelectorFailure("EAL_REGISTRY_SCHEMA_INVALID", "value matches a forbidden schema", field=path)


def load_attested_schema(path: Path, expected_schema: str) -> dict[str, Any]:
    require_regular(path, label="registry schema")
    raw_schema = strict_json(path.read_bytes(), label="registry schema")
    require(isinstance(raw_schema, dict), "EAL_REGISTRY_SCHEMA_INVALID", "registry schema must be a JSON object")
    observed = raw_schema.get("properties", {}).get("schema_version", {}).get("const")
    require(observed == expected_schema, "EAL_REGISTRY_SCHEMA_VERSION_MISMATCH", "schema artifact does not declare the expected registry version", observed=observed, expected=expected_schema)
    return raw_schema


def runtime_contract_check(root: Path, contract_path: Path, registry_path: Path, expected_schema: str, expected_rows: int) -> None:
    require_regular(contract_path, label="runtime contract")
    package_name = root.name
    module_name = f"{package_name}.contracts"
    parent_text = str(root.parent)
    prior_path = list(sys.path)
    try:
        sys.path.insert(0, parent_text)
        importlib.invalidate_caches()
        module = importlib.import_module(module_name)
        require(Path(module.__file__).resolve() == contract_path.resolve(), "EAL_RUNTIME_CONTRACT_LOAD_FAILED", "runtime contract resolved from an unexpected package", observed=module.__file__, expected=str(contract_path))
        require(getattr(module, "SCHEMA_VERSION", None) == expected_schema, "EAL_RUNTIME_CONTRACT_VERSION_MISMATCH", "runtime contract schema version drifted")
        loader = getattr(module, "load_registry", None)
        require(callable(loader), "EAL_RUNTIME_CONTRACT_LOAD_FAILED", "runtime contract lacks load_registry")
        records, exclusions = loader(registry_path)
    except SelectorFailure:
        raise
    except Exception as exc:
        raise SelectorFailure("EAL_REGISTRY_CONTRACT_INVALID", "registry failed the attested runtime contract", underlying_code=getattr(exc, "code", type(exc).__name__), underlying_message=str(exc)) from exc
    finally:
        sys.path[:] = prior_path
        for imported_name in list(sys.modules):
            if imported_name == package_name or imported_name.startswith(f"{package_name}."):
                sys.modules.pop(imported_name, None)
    require(len(records) == expected_rows, "EAL_REGISTRY_ROW_COUNT_MISMATCH", "runtime contract returned an unexpected row count", observed=len(records), expected=expected_rows)
    require(exclusions == [], "EAL_REGISTRY_CONTRACT_INVALID", "runtime contract produced registry exclusions", exclusions=exclusions)


def verify_attested_file(root: Path, entries: dict[str, str], relative: str, expected_sha: str, label: str) -> tuple[Path, int]:
    require(relative in entries, "EAL_CONSUMER_MANIFEST_ENTRY_MISSING", f"{label} is not attested by CURRENT_SHA256SUMS", path=relative)
    require(entries[relative] == expected_sha, "EAL_CONSUMER_MANIFEST_HASH_MISMATCH", f"{label} manifest hash differs from the pinned hash", path=relative, observed=entries[relative], expected=expected_sha)
    path = resolve_inside(root, relative)
    info = require_regular(path, label=label)
    observed_sha = sha256_file(path)
    require(observed_sha == entries[relative], "EAL_ATTESTED_FILE_HASH_MISMATCH", f"{label} bytes do not match CURRENT_SHA256SUMS", path=str(path), observed=observed_sha, expected=entries[relative])
    return path, info.st_size


def detect_registry_conflicts(root: Path, entries: dict[str, str], expected_relative: str) -> int:
    expected = PurePosixPath(expected_relative)
    match = REGISTRY_NAME.fullmatch(expected.name)
    require(match is not None, "EAL_SELECTOR_EXPECTED_PATH_INVALID", "expected registry filename is not versioned canonically", path=expected_relative)
    expected_date = match.group(1)
    directory = root.joinpath(*expected.parent.parts)
    checked = 0
    with os.scandir(directory) as siblings:
        for sibling in siblings:
            candidate = REGISTRY_NAME.fullmatch(sibling.name)
            if candidate is None or sibling.name == expected.name:
                continue
            checked += 1
            if candidate.group(1) < expected_date:
                continue
            relative = (expected.parent / sibling.name).as_posix()
            if relative in entries:
                raise SelectorFailure("EAL_SELECTOR_EXPECTED_REGISTRY_STALE", "a same-date or newer registry is attested; the consumer pin requires explicit review", expected=expected_relative, conflicting=relative)
            raise SelectorFailure("EAL_UNATTESTED_NEWER_REGISTRY", "a same-date or newer registry exists without manifest attestation", expected=expected_relative, conflicting=relative)
    return checked


def resolve(args: argparse.Namespace) -> dict[str, Any]:
    root = Path(args.eal_root)
    root_info = root.lstat()
    require(stat.S_ISDIR(root_info.st_mode) and not stat.S_ISLNK(root_info.st_mode), "EAL_SELECTOR_ROOT_INVALID", "EAL root must be a real directory", path=str(root))
    manifest_path = resolve_inside(root, "CURRENT_SHA256SUMS")
    entries, manifest_bytes = parse_manifest(manifest_path)
    expected_registry, registry_bytes = verify_attested_file(root, entries, args.expected_registry_rel, args.expected_sha256, "registry")
    require(registry_bytes == args.expected_bytes, "EAL_REGISTRY_BYTE_COUNT_MISMATCH", "registry byte count differs from the pinned count", observed=registry_bytes, expected=args.expected_bytes)
    schema_path, schema_bytes = verify_attested_file(root, entries, SCHEMA_REL, args.expected_schema_sha256, "registry schema")
    contract_path, contract_bytes = verify_attested_file(root, entries, CONTRACT_REL, args.expected_contract_sha256, "runtime contract")
    verify_manifest_tree(root, entries)
    schema = load_attested_schema(schema_path, args.expected_schema)
    raw_registry = expected_registry.read_bytes()
    require(raw_registry.endswith(b"\n"), "EAL_REGISTRY_SCHEMA_INVALID", "registry must end with a newline")
    lines = raw_registry.splitlines()
    require(len(lines) == args.expected_rows, "EAL_REGISTRY_ROW_COUNT_MISMATCH", "registry line count differs from the pinned count", observed=len(lines), expected=args.expected_rows)
    require(all(lines), "EAL_REGISTRY_SCHEMA_INVALID", "registry contains a blank row")
    for line_number, line in enumerate(lines, start=1):
        row = strict_json(line, label=f"registry row {line_number}")
        require(isinstance(row, dict), "EAL_REGISTRY_SCHEMA_INVALID", "registry row must be an object", line=line_number)
        validate_schema(row, schema, f"$[{line_number}]")
    runtime_contract_check(root, contract_path, expected_registry, args.expected_schema, args.expected_rows)
    conflicts_checked = detect_registry_conflicts(root, entries, args.expected_registry_rel)
    return {
        "manifest": {"bytes": manifest_bytes, "entry_count": len(entries), "path": str(manifest_path), "sha256": sha256_file(manifest_path), "verified_entry_count": len(entries)},
        "policy": {"exact_manifest_path_only": True, "glob_selection": False, "same_or_newer_conflicts_checked": conflicts_checked},
        "registry": {"bytes": registry_bytes, "path": str(expected_registry), "relative_path": args.expected_registry_rel, "rows": len(lines), "schema_version": args.expected_schema, "sha256": args.expected_sha256},
        "runtime_contract": {"bytes": contract_bytes, "path": str(contract_path), "sha256": args.expected_contract_sha256},
        "schema": {"bytes": schema_bytes, "path": str(schema_path), "sha256": args.expected_schema_sha256},
        "status": "resolved_manifest_attested_registry",
    }


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument("--eal-root", required=True)
    result.add_argument("--expected-registry-rel", required=True)
    result.add_argument("--expected-sha256", required=True)
    result.add_argument("--expected-bytes", required=True, type=int)
    result.add_argument("--expected-rows", required=True, type=int)
    result.add_argument("--expected-schema", required=True)
    result.add_argument("--expected-schema-sha256", required=True)
    result.add_argument("--expected-contract-sha256", required=True)
    return result


def main(argv: list[str] | None = None) -> int:
    try:
        args = parser().parse_args(argv)
        for field in ("expected_sha256", "expected_schema_sha256", "expected_contract_sha256"):
            value = getattr(args, field)
            require(HEX_64.fullmatch(value) is not None, "EAL_SELECTOR_ARGUMENT_INVALID", "expected hash must be lowercase SHA-256", argument=field)
        require(args.expected_rows > 0 and args.expected_bytes > 0, "EAL_SELECTOR_ARGUMENT_INVALID", "expected counts must be positive")
        print(json.dumps(resolve(args), ensure_ascii=False, sort_keys=True, separators=(",", ":")))
        return 0
    except SelectorFailure as exc:
        payload = {"code": exc.code, "details": exc.details, "message": exc.message, "status": "rejected"}
        print(json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")), file=sys.stderr)
        return 2
    except (OSError, ValueError) as exc:
        payload = {"code": "EAL_SELECTOR_IO_FAILURE", "details": {"error_type": type(exc).__name__}, "message": str(exc), "status": "rejected"}
        print(json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")), file=sys.stderr)
        return 3


if __name__ == "__main__":
    raise SystemExit(main())
