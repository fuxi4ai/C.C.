#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).with_name("resolve_registry_from_manifest.py")
SPEC = importlib.util.spec_from_file_location("selector_under_test", SCRIPT)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("cannot load selector")
SELECTOR = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = SELECTOR
SPEC.loader.exec_module(SELECTOR)


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


class SelectorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory(prefix="eal-selector-test-")
        self.root = Path(self.temp.name) / "eal_v3"
        (self.root / "coding_work").mkdir(parents=True)
        (self.root / "schemas").mkdir()
        self.registry_rel = "coding_work/frozen-event-registry-v3.2-20260827_vv.jsonl"
        self.row = {"event_id": "fixture-one", "schema_version": "eal-event-registry-v3.2"}
        self.registry_bytes = (json.dumps(self.row, sort_keys=True, separators=(",", ":")) + "\n").encode()
        (self.root / self.registry_rel).write_bytes(self.registry_bytes)
        self.schema = {
            "additionalProperties": False,
            "properties": {"event_id": {"minLength": 1, "type": "string"}, "schema_version": {"const": "eal-event-registry-v3.2"}},
            "required": ["event_id", "schema_version"],
            "type": "object",
        }
        self.schema_bytes = (json.dumps(self.schema, sort_keys=True, separators=(",", ":")) + "\n").encode()
        (self.root / SELECTOR.SCHEMA_REL).write_bytes(self.schema_bytes)
        self.contract_bytes = b'SCHEMA_VERSION = "eal-event-registry-v3.2"\n\ndef load_registry(path):\n    import json\n    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]\n    return rows, []\n'
        (self.root / SELECTOR.CONTRACT_REL).write_bytes(self.contract_bytes)
        self.write_manifest()

    def tearDown(self) -> None:
        self.temp.cleanup()

    def entries(self) -> list[tuple[str, str]]:
        return [
            (digest(self.contract_bytes), SELECTOR.CONTRACT_REL),
            (digest(self.registry_bytes), self.registry_rel),
            (digest(self.schema_bytes), SELECTOR.SCHEMA_REL),
        ]

    def write_manifest(self, entries: list[tuple[str, str]] | None = None) -> None:
        rows = entries if entries is not None else self.entries()
        (self.root / "CURRENT_SHA256SUMS").write_text("".join(f"{sha}  {path}\n" for sha, path in rows), encoding="utf-8")

    def command(self, *, optimize: bool = False) -> list[str]:
        command = [sys.executable]
        if optimize:
            command.append("-O")
        command.extend([
            "-B", str(SCRIPT), "--eal-root", str(self.root), "--expected-registry-rel", self.registry_rel,
            "--expected-sha256", digest(self.registry_bytes), "--expected-bytes", str(len(self.registry_bytes)),
            "--expected-rows", "1", "--expected-schema", "eal-event-registry-v3.2",
            "--expected-schema-sha256", digest(self.schema_bytes), "--expected-contract-sha256", digest(self.contract_bytes),
        ])
        return command

    def run_selector(self, *, optimize: bool = False) -> subprocess.CompletedProcess[str]:
        return subprocess.run(self.command(optimize=optimize), text=True, capture_output=True, check=False)

    def reject_code(self) -> str:
        completed = self.run_selector()
        self.assertEqual(completed.returncode, 2, completed.stderr)
        return json.loads(completed.stderr)["code"]

    def test_positive_and_optimized_outputs_match(self) -> None:
        normal = self.run_selector()
        optimized = self.run_selector(optimize=True)
        self.assertEqual(normal.returncode, 0, normal.stderr)
        self.assertEqual(optimized.returncode, 0, optimized.stderr)
        self.assertEqual(normal.stdout, optimized.stdout)
        payload = json.loads(normal.stdout)
        self.assertFalse(payload["policy"]["glob_selection"])
        self.assertEqual(payload["registry"]["rows"], 1)

    def test_missing_registry_manifest_entry(self) -> None:
        self.write_manifest([entry for entry in self.entries() if entry[1] != self.registry_rel])
        self.assertEqual(self.reject_code(), "EAL_CONSUMER_MANIFEST_ENTRY_MISSING")

    def test_duplicate_manifest_path(self) -> None:
        entries = self.entries()
        entries.append(entries[1])
        self.write_manifest(entries)
        self.assertEqual(self.reject_code(), "EAL_CONSUMER_MANIFEST_DUPLICATE_PATH")

    def test_manifest_registry_hash_mismatch(self) -> None:
        entries = [("0" * 64, path) if path == self.registry_rel else (sha, path) for sha, path in self.entries()]
        self.write_manifest(entries)
        self.assertEqual(self.reject_code(), "EAL_CONSUMER_MANIFEST_HASH_MISMATCH")

    def test_registry_bytes_hash_mismatch(self) -> None:
        (self.root / self.registry_rel).write_bytes(self.registry_bytes + b"\n")
        self.assertEqual(self.reject_code(), "EAL_ATTESTED_FILE_HASH_MISMATCH")

    def test_registry_symlink_rejected(self) -> None:
        target = self.root / "coding_work/real.jsonl"
        target.write_bytes(self.registry_bytes)
        (self.root / self.registry_rel).unlink()
        (self.root / self.registry_rel).symlink_to(target)
        self.assertEqual(self.reject_code(), "EAL_SELECTOR_SYMLINK_REJECTED")

    def test_row_count_mismatch(self) -> None:
        command = self.command()
        command[command.index("--expected-rows") + 1] = "2"
        completed = subprocess.run(command, text=True, capture_output=True, check=False)
        self.assertEqual(completed.returncode, 2)
        self.assertEqual(json.loads(completed.stderr)["code"], "EAL_REGISTRY_ROW_COUNT_MISMATCH")

    def test_wrong_schema_version(self) -> None:
        changed = dict(self.row, schema_version="eal-event-registry-v9")
        changed_bytes = (json.dumps(changed, sort_keys=True, separators=(",", ":")) + "\n").encode()
        (self.root / self.registry_rel).write_bytes(changed_bytes)
        self.registry_bytes = changed_bytes
        self.write_manifest()
        self.assertEqual(self.reject_code(), "EAL_REGISTRY_SCHEMA_INVALID")

    def test_duplicate_json_key(self) -> None:
        changed_bytes = b'{"event_id":"a","event_id":"b","schema_version":"eal-event-registry-v3.2"}\n'
        (self.root / self.registry_rel).write_bytes(changed_bytes)
        self.registry_bytes = changed_bytes
        self.write_manifest()
        self.assertEqual(self.reject_code(), "EAL_REGISTRY_DUPLICATE_JSON_KEY")

    def test_unattested_newer_registry_rejected(self) -> None:
        (self.root / "coding_work/frozen-event-registry-v3.2-20260828.jsonl").write_bytes(self.registry_bytes)
        self.assertEqual(self.reject_code(), "EAL_UNATTESTED_NEWER_REGISTRY")

    def test_attested_newer_registry_requires_explicit_pin_update(self) -> None:
        newer_rel = "coding_work/frozen-event-registry-v3.2-20260828.jsonl"
        (self.root / newer_rel).write_bytes(self.registry_bytes)
        self.write_manifest(self.entries() + [(digest(self.registry_bytes), newer_rel)])
        self.assertEqual(self.reject_code(), "EAL_SELECTOR_EXPECTED_REGISTRY_STALE")

    def test_malformed_manifest_rejected(self) -> None:
        (self.root / "CURRENT_SHA256SUMS").write_text("not canonical\n", encoding="utf-8")
        self.assertEqual(self.reject_code(), "EAL_CONSUMER_MANIFEST_INVALID")


if __name__ == "__main__":
    unittest.main(verbosity=2)
