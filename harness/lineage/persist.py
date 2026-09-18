#!/usr/bin/env python3
"""Persist an RX50 controller observation as provenance only."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from engine import SCHEMA_VERSION, append, read_all

ROOT = Path(__file__).resolve().parents[2]
STATE = ROOT / "state" / "controller_state.json"
QUEUE = ROOT / "state" / "bc_queue.json"

UNKNOWN_EXECUTION = {
    "effect_id": "UNKNOWN",
    "attempt_id": "UNKNOWN",
    "receipt_id": "UNKNOWN",
    "provider": "UNKNOWN",
}


def load(path: Path, default):
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else default


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.exists() else "MISSING"


def main() -> int:
    state = load(STATE, {})
    queue = load(QUEUE, {})
    iteration = int(state.get("iteration", 0))
    item = (queue.get("queue") or [{}])[0]
    item_id = item.get("id", "none")
    result = state.get("result", "UNKNOWN")
    lineage_id = f"RX50:{iteration}:{item_id}:{result}"
    if any(str(x.get("lineage_id")) == lineage_id for x in read_all()):
        print(f"LINEAGE_EXISTS {lineage_id}")
        return 0

    record = {
        "schema_version": SCHEMA_VERSION,
        "lineage_id": lineage_id,
        "generation": iteration,
        "candidate": item_id,
        "parent_artifacts": item.get("parent_artifacts", []),
        "delta": item.get("delta", item.get("description", "controller audit boundary")),
        "observation": {
            "kind": "controller_observation",
            "controller_result": result,
            "evidence": item.get("evidence", []),
            "tests": {"queue_sha256": state.get("queue_sha256")},
            "execution": dict(UNKNOWN_EXECUTION),
            "controller_state_sha256": sha256_file(STATE),
        },
        "contradictions": item.get("contradictions", []),
        "constraints": item.get("constraints", []),
        "claims": item.get("claims", []),
    }
    append(record)
    print(f"LINEAGE_RECORDED {lineage_id}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
