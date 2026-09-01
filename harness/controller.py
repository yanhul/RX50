#!/usr/bin/env python3
"""RX50 evidence-state controller.

This controller only moves between evidence states. It never creates engineering
numbers, authorizes hardware, or promotes an unaudited candidate.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUEUE = ROOT / "state" / "bc_queue.json"
STATE = ROOT / "state" / "controller_state.json"
MAX_ITERATIONS = 8


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    queue = load(QUEUE)
    state = load(STATE) if STATE.exists() else {"iteration": 0}
    iteration = int(state.get("iteration", 0)) + 1

    if iteration > min(MAX_ITERATIONS, int(queue.get("max_iterations", MAX_ITERATIONS))):
        result = "ITERATION_LIMIT"
    else:
        item = queue.get("queue", [{}])[0]
        evidence = item.get("evidence", [])
        owner = bool(item.get("owner_authorized", False))
        safety = bool(item.get("safety_authorized", False))
        frozen = bool(item.get("frozen", False))

        if item.get("status") != "AUDIT_REQUIRED":
            result = "HOLD"
        elif not evidence:
            result = "BLOCKED: NO EVIDENCE"
        elif not owner:
            result = "NOT AUTHORIZED: OWNER"
        elif not safety:
            result = "NOT AUTHORIZED: SAFETY"
        elif not frozen:
            result = "NOT LOCKED"
        else:
            result = "HOLD: PROMOTION REQUIRES REGISTERED AUDIT"

    raw = QUEUE.read_bytes()
    state = {
        "iteration": iteration,
        "result": result,
        "queue_sha256": sha256_bytes(raw),
    }
    STATE.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
    print(result)
    print("queue_sha256=" + state["queue_sha256"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
