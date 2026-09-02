#!/usr/bin/env python3
"""Persist a durable RX50 controller iteration as provenance only."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
from engine import append, read_all

ROOT = Path(__file__).resolve().parents[2]
STATE = ROOT / "state" / "controller_state.json"
QUEUE = ROOT / "state" / "bc_queue.json"


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
    experiment_id = f"RX50:{iteration}:{item_id}:{state.get('result', 'UNKNOWN')}"
    if any(str(x.get("experiment_id")) == experiment_id for x in read_all()):
        print(f"LINEAGE_EXISTS {experiment_id}")
        return 0

    record = {
        "experiment_id": experiment_id,
        "generation": iteration,
        "candidate": item_id,
        "parent_artifacts": item.get("parent_artifacts", []),
        "delta": item.get("delta", item.get("description", "controller audit boundary")),
        "evidence": item.get("evidence", []),
        "tests": {"controller_result": state.get("result"), "queue_sha256": state.get("queue_sha256")},
        "verdict": state.get("result", "UNKNOWN"),
        "contradictions": item.get("contradictions", []),
        "constraints": item.get("constraints", []),
        "claims": item.get("claims", []),
        "controller_state_sha256": sha256_file(STATE),
    }
    append(record)
    print(f"LINEAGE_RECORDED {experiment_id}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
