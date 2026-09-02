#!/usr/bin/env python3
"""Append-only provenance recorder for RX50 engineering iterations.

This records evidence and deltas; it cannot alter requirements, safety gates,
contradiction policy, evidence hierarchy, acceptance criteria, or terminal rules.
"""
from __future__ import annotations
import hashlib, json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LOG = ROOT / "harness" / "lineage" / "records.jsonl"
REQUIRED = {"generation", "candidate", "parent_artifacts", "delta", "evidence", "tests", "verdict", "contradictions", "constraints", "claims"}

def _hash(value: object) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()

def append(record: dict) -> dict:
    missing = sorted(REQUIRED - record.keys())
    if missing:
        raise ValueError("missing lineage fields: " + ",".join(missing))
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
