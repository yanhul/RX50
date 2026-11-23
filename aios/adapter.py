"""AIOS workload adapter for RX50 engineering evidence/readiness.

Physical evidence is never inferred from the presence of a directory or file.
Only a validated measurements manifest that points to non-empty raw artifacts
can satisfy the physical-evidence gate.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

REQUIRED = (
    "AGENTS.md", "RX50_G1_G2_REQUIREMENT_CLOSURE.md",
    "RX50_G4_G5_CLOSURE_AUDIT.md", "RX50_G4_RAW_EVIDENCE_REGISTER.md",
)
PROVENANCE = {"producer": "yanhul/RX50", "adapter": "rx50.engineering@1"}
PHYSICAL_MANIFEST = Path("evidence/physical/measurements.json")
COMMON_FIELDS = {
    "test_id", "dut_id", "trial", "vdd", "temperature", "channel", "condition",
    "input", "output", "value", "unit", "instrument", "instrument_id",
    "calibration_status", "operator", "date", "time", "raw_data_ref", "raw_data_sha256",
}
ALLOWED_RAW_SUFFIXES = {".csv", ".json", ".png", ".jpg", ".jpeg", ".pdf", ".wfm", ".bin"}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _artifact_manifest(root: Path, evidence: tuple[str, ...]) -> str:
    artifact = root / "harness" / "state" / "rx50_engineering_evidence_set.json"
    artifact.parent.mkdir(parents=True, exist_ok=True)
    payload = {"kind": "rx50-engineering-evidence-set", "evidence_refs": list(evidence),
               "provenance": PROVENANCE}
    artifact.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return str(artifact.relative_to(root))


def _validate_physical_evidence(root: Path) -> tuple[list[str], list[str]]:
    manifest_path = root / PHYSICAL_MANIFEST
    if not manifest_path.is_file():
        raise ValueError("physical measurement manifest missing; raw hardware measurements have not been supplied")
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise ValueError("physical measurement manifest is not valid JSON") from exc
    if not isinstance(manifest, dict) or manifest.get("schema_version") != 1:
        raise ValueError("physical measurement manifest schema_version must be 1")
    records = manifest.get("measurements")
    if not isinstance(records, list) or not records:
        raise ValueError("physical measurement manifest contains no measurement records")

    evidence = [f"sha256:{PHYSICAL_MANIFEST.as_posix()}:{_sha256(manifest_path)}"]
    verified_refs: list[str] = []
    physical_root = (root / "evidence" / "physical").resolve()
    for index, record in enumerate(records):
        if not isinstance(record, dict):
            raise ValueError(f"measurement[{index}] must be an object")
        missing = COMMON_FIELDS - set(record)
        if missing:
            raise ValueError(f"measurement[{index}] missing fields: {sorted(missing)}")
        for key in COMMON_FIELDS - {"trial", "vdd", "temperature", "channel", "input", "output", "value"}:
            value = record.get(key)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"measurement[{index}] field {key} must be non-empty text")
        raw_ref = record["raw_data_ref"]
        if not isinstance(raw_ref, str) or not raw_ref.strip():
            raise ValueError(f"measurement[{index}] raw_data_ref must be non-empty")
        raw_path = (root / raw_ref).resolve()
        try:
            raw_path.relative_to(physical_root)
        except ValueError as exc:
            raise ValueError(f"measurement[{index}] raw_data_ref must stay under evidence/physical") from exc
        if raw_path.suffix.lower() not in ALLOWED_RAW_SUFFIXES or not raw_path.is_file() or raw_path.stat().st_size == 0:
            raise ValueError(f"measurement[{index}] raw data artifact missing, empty, or unsupported")
        digest = "sha256:" + _sha256(raw_path)
        if record["raw_data_sha256"] != digest:
            raise ValueError(f"measurement[{index}] raw data SHA-256 mismatch")
        evidence.append(f"sha256:{raw_ref}:{digest.removeprefix('sha256:')}")
        measurement_ref = f"physical_measurement:{record['test_id']}:{record['dut_id']}:{record['trial']}"
        evidence.append(measurement_ref)
        verified_refs.append(measurement_ref)
    return evidence, verified_refs


def execute(*, problem: str, workdir: str | Path = ".") -> dict[str, Any]:
    if not isinstance(problem, str) or not problem.strip():
        raise ValueError("problem must be non-empty")
    root = Path(workdir)
    missing = [name for name in REQUIRED if not (root / name).exists()]
    if missing:
        return {"status": "BLOCKED", "reason": "required engineering evidence files missing", "missing": missing,
                "artifact_refs": (), "evidence_refs": (), "verification_refs": (), "provenance": PROVENANCE}
    evidence = tuple(f"sha256:{name}:{_sha256(root / name)}" for name in REQUIRED)
    try:
        physical_evidence, physical_refs = _validate_physical_evidence(root)
    except ValueError as exc:
        artifact_ref = _artifact_manifest(root, evidence)
        return {"status": "BLOCKED", "reason": str(exc), "artifact_refs": (artifact_ref,),
                "evidence_refs": evidence, "verification_refs": ("requirements_coverage", "contradiction_check"),
                "provenance": PROVENANCE}
    evidence = evidence + tuple(physical_evidence)
    artifact_ref = _artifact_manifest(root, evidence)
    return {"status": "PASS", "problem": problem, "artifact_refs": (artifact_ref,),
            "evidence_refs": evidence,
            "verification_refs": ("requirements_coverage", "contradiction_check", "physical_measurements", "raw_artifact_hashes"),
            "provenance": PROVENANCE, "physical_evidence": physical_refs}


if __name__ == "__main__":
    print(json.dumps(execute(problem="AIOS RX50 engineering conformance"), indent=2))
