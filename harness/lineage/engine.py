#!/usr/bin/env python3
"""Append-only RX50 lineage with explicit observation/evaluation separation."""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LOG = ROOT / "harness" / "lineage" / "records.jsonl"
SCHEMA_VERSION = 2

REQUIRED = {
    "schema_version",
    "lineage_id",
    "generation",
    "candidate",
    "parent_artifacts",
    "delta",
    "observation",
    "claims",
    "contradictions",
    "constraints",
}

EXECUTION_FIELDS = ("effect_id", "attempt_id", "receipt_id", "provider")
EVALUATION_FIELDS = (
    "evaluator_id",
    "evaluator_version",
    "policy_version",
    "evidence_refs",
    "test_results",
    "verdict",
)


def _hash(value: object) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def _validate_execution(execution: object) -> None:
    if execution is None:
        return
    if not isinstance(execution, dict):
        raise ValueError("execution must be an object")
    missing = [field for field in EXECUTION_FIELDS if field not in execution]
    if missing:
        raise ValueError("execution binding missing fields: " + ",".join(missing))

    effect = execution["effect_id"]
    attempt = execution["attempt_id"]
    receipt = execution["receipt_id"]

    # UNKNOWN is an explicit absence of execution evidence, not a fabricated ID.
    if receipt != "UNKNOWN" and (effect == "UNKNOWN" or attempt == "UNKNOWN"):
        raise ValueError("known receipt requires known effect_id and attempt_id")
    if attempt != "UNKNOWN" and effect == "UNKNOWN":
        raise ValueError("known attempt requires known effect_id")


def _validate_evaluation(record: dict) -> None:
    evaluation = record.get("evaluation")
    if evaluation is None:
        return
    if not isinstance(evaluation, dict):
        raise ValueError("evaluation must be an object")
    missing = [field for field in EVALUATION_FIELDS if field not in evaluation]
    if missing:
        raise ValueError("evaluation missing fields: " + ",".join(missing))
    if evaluation["verdict"] not in {"PASS", "FAIL", "BLOCKED", "INCONCLUSIVE", "UNKNOWN"}:
        raise ValueError("unsupported evaluation verdict")
    if evaluation["verdict"] == "PASS" and not evaluation["evidence_refs"]:
        raise ValueError("PASS evaluation requires evidence_refs")
    if evaluation["verdict"] == "PASS" and not evaluation["test_results"]:
        raise ValueError("PASS evaluation requires test_results")
    execution = record["observation"].get("execution")
    if evaluation["verdict"] == "PASS" and execution and execution.get("receipt_id") == "UNKNOWN":
        raise ValueError("PASS evaluation requires a receipt")


def validate_record(record: dict) -> None:
    missing = sorted(REQUIRED - record.keys())
    if missing:
        raise ValueError("missing lineage fields: " + ",".join(missing))
    if record["schema_version"] != SCHEMA_VERSION:
        raise ValueError("unsupported lineage schema_version")
    if "verdict" in record:
        raise ValueError("verdict belongs only inside evaluation")
    if record.get("evaluation", {}).get("verdict") == "PASS":
        execution = record["observation"].get("execution")
        if execution and execution.get("status") in {"FAILED", "UNKNOWN"}:
            raise ValueError("failed or unknown execution cannot have PASS evaluation")
    if not isinstance(record["observation"], dict):
        raise ValueError("observation must be an object")
    _validate_execution(record["observation"].get("execution"))
    _validate_evaluation(record)


def append(record: dict) -> dict:
    validate_record(record)
    entry = dict(record)
    entry["record_hash"] = _hash(record)
    entry["recorded_at"] = datetime.now(timezone.utc).isoformat()
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, sort_keys=True) + "\n")
    return entry


def read_all() -> list[dict]:
    if not LOG.exists():
        return []
    return [json.loads(x) for x in LOG.read_text(encoding="utf-8").splitlines() if x.strip()]
