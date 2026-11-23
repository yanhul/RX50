from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path

MODULE = Path(__file__).resolve().parents[1] / "aios" / "adapter.py"
SPEC = importlib.util.spec_from_file_location("rx50_aios_adapter", MODULE)
adapter = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(adapter)


def _root(tmp_path: Path) -> Path:
    for name in adapter.REQUIRED:
        path = tmp_path / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("source evidence\n", encoding="utf-8")
    return tmp_path


def _record(raw: Path) -> dict:
    return {
        "test_id": "T-G4-01",
        "dut_id": "DUT-001",
        "trial": 1,
        "vdd": "3.3 V",
        "temperature": "25 C",
        "channel": "CH1",
        "condition": "measured",
        "input": "fixture input",
        "output": "measured output",
        "value": "1.2",
        "unit": "ohm",
        "instrument": "DMM",
        "instrument_id": "DMM-001",
        "calibration_status": "in_calibration",
        "operator": "operator",
        "date": "2026-11-23",
        "time": "12:00:00Z",
        "raw_data_ref": str(raw.relative_to(raw.parents[2])),
        "raw_data_sha256": "sha256:" + hashlib.sha256(raw.read_bytes()).hexdigest(),
    }


def test_arbitrary_file_does_not_satisfy_physical_evidence(tmp_path: Path):
    root = _root(tmp_path)
    physical = root / "evidence" / "physical"
    physical.mkdir(parents=True)
    (physical / "README.md").write_text("measurements pending", encoding="utf-8")
    result = adapter.execute(problem="test", workdir=root)
    assert result["status"] == "BLOCKED"
    assert "manifest missing" in result["reason"]


def test_manifest_requires_real_raw_artifact_and_digest(tmp_path: Path):
    root = _root(tmp_path)
    physical = root / "evidence" / "physical"
    physical.mkdir(parents=True)
    raw = physical / "t-g4-01.csv"
    raw.write_text("test_id,value\nT-G4-01,1.2\n", encoding="utf-8")
    manifest = {"schema_version": 1, "measurements": [_record(raw)]}
    (physical / "measurements.json").write_text(json.dumps(manifest), encoding="utf-8")
    result = adapter.execute(problem="test", workdir=root)
    assert result["status"] == "PASS"
    assert any("physical_measurement:T-G4-01" in ref for ref in result["evidence_refs"])


def test_manifest_cannot_reference_outside_physical_directory(tmp_path: Path):
    root = _root(tmp_path)
    physical = root / "evidence" / "physical"
    physical.mkdir(parents=True)
    raw = root / "outside.csv"
    raw.write_text("value\n1\n", encoding="utf-8")
    record = _record(raw)
    manifest = {"schema_version": 1, "measurements": [record]}
    (physical / "measurements.json").write_text(json.dumps(manifest), encoding="utf-8")
    result = adapter.execute(problem="test", workdir=root)
    assert result["status"] == "BLOCKED"
    assert "stay under evidence/physical" in result["reason"]


def test_raw_artifact_digest_mismatch_is_blocked(tmp_path: Path):
    root = _root(tmp_path)
    physical = root / "evidence" / "physical"
    physical.mkdir(parents=True)
    raw = physical / "t-g4-01.csv"
    raw.write_text("value\n1\n", encoding="utf-8")
    record = _record(raw)
    record["raw_data_sha256"] = "sha256:" + "0" * 64
    manifest = {"schema_version": 1, "measurements": [record]}
    (physical / "measurements.json").write_text(json.dumps(manifest), encoding="utf-8")
    result = adapter.execute(problem="test", workdir=root)
    assert result["status"] == "BLOCKED"
    assert "SHA-256 mismatch" in result["reason"]
