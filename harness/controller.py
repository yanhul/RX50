#!/usr/bin/env python3
"""RX50 durable evidence-state controller.

The controller is the control plane. It never invents engineering numbers,
authorizes hardware, resolves contradictions silently, or promotes an unaudited
candidate. It persists a checkpoint so a later invocation can resume safely.
"""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUEUE = ROOT / "state" / "bc_queue.json"
STATE = ROOT / "state" / "controller_state.json"
MAX_ITERATIONS = 8


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def checkpoint(state: dict, **changes) -> dict:
    state.update(changes)
    state["updated_at"] = datetime.now(timezone.utc).isoformat()
    STATE.parent.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return state


def main() -> int:
    queue = load(QUEUE)
    state = load(STATE) if STATE.exists() else {
        "phase": "OBSERVE",
        "iteration": 0,
        "retry_count": 0,
        "terminal": False,
    }

    # OBSERVE: load the authoritative queue and verify the persisted checkpoint.
    queue_sha = sha256_bytes(QUEUE.read_bytes())
    previous_queue_sha = state.get("previous_queue_sha256")
    if previous_queue_sha and previous_queue_sha != queue_sha:
        state = checkpoint(state, phase="OBSERVE", queue_changed=True, iteration=0)
    else:
        state = checkpoint(state, phase="OBSERVE", queue_sha256=queue_sha)

    if state.get("terminal"):
        print("TERMINAL:" + str(state.get("terminal_reason", "unspecified")))
        return 0

    items = queue.get("queue", [])
    item = items[0] if items else {}
    evidence = item.get("evidence", [])
    owner = bool(item.get("owner_authorized", False))
    safety = bool(item.get("safety_authorized", False))
    frozen = bool(item.get("frozen", False))
    status = item.get("status")

    # Policy gates are evaluated before the iteration budget. A persisted retry
    # counter must never mask a stronger safety/evidence BLOCKED decision.
    if status != "AUDIT_REQUIRED":
        result = "HOLD"
        reason = "queue item is not in AUDIT_REQUIRED state"
    elif not evidence:
        result = "BLOCKED: NO EVIDENCE"
        reason = "required evidence is missing"
    elif not owner:
        result = "HOLD: OWNER APPROVAL REQUIRED"
        reason = "owner authorization is false"
    elif not safety:
        result = "HOLD: SAFETY APPROVAL REQUIRED"
        reason = "safety authorization is false"
    elif not frozen:
        result = "HOLD: NOT LOCKED"
        reason = "required frozen state is false"
    else:
        iteration = int(state.get("iteration", 0)) + 1
        limit = min(MAX_ITERATIONS, int(queue.get("max_iterations", MAX_ITERATIONS)))
        if iteration > limit:
            result = "HOLD: ITERATION_LIMIT"
            reason = "iteration limit reached; resume only after new evidence/state change"
        else:
            result = "HOLD: REGISTERED AUDIT REQUIRED"
            reason = "promotion requires the registered audit path"
        state = checkpoint(state, phase="DECIDE", iteration=iteration)

    # ACT/VERIFY: this controller records a decision boundary; engineering
    # edits are intentionally outside the controller and remain approval-gated.
    state = checkpoint(state, phase="VERIFY", result=result, last_error=reason)
    state = checkpoint(state, phase="PERSIST", result=result)
    state = checkpoint(
        state,
        phase="YIELD",
        previous_queue_sha256=queue_sha,
        current_item=item.get("id"),
    )
    print(state["result"])
    print("phase=" + state["phase"])
    print("queue_sha256=" + state["queue_sha256"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
