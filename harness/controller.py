#!/usr/bin/env python3
"""RX50 durable evidence-state controller; terminal authority is external."""
from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path

from terminal_authority import verify_terminal_attestation

ROOT = Path(__file__).resolve().parents[1]
QUEUE = ROOT / "state" / "bc_queue.json"
STATE = ROOT / "state" / "controller_state.json"

MAX_ITERATIONS = 8
STATE_SCHEMA_VERSION = 2
QUEUE_SCHEMA_VERSION = 1
CONTROLLER_CODE_REVISION = "rx50-controller-v2"
POLICY_REVISION = "rx50-policy-v1"


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


def expected_compatibility(queue: dict) -> dict:
    return {
        "state_schema_version": STATE_SCHEMA_VERSION,
        "queue_schema_version": queue.get("schema_version"),
        "controller_code_revision": CONTROLLER_CODE_REVISION,
        "policy_revision": POLICY_REVISION,
    }


def validate_state_compatibility(state: dict, queue: dict) -> tuple[bool, str]:
    if not isinstance(state, dict):
        return False, "state is not an object"
    compatibility = state.get("compatibility")
    if not isinstance(compatibility, dict):
        return False, "missing compatibility fence"
    expected = expected_compatibility(queue)
    for key, value in expected.items():
        if compatibility.get(key) != value:
            return False, f"{key} mismatch"
    if queue.get("schema_version") != QUEUE_SCHEMA_VERSION:
        return False, "queue schema_version mismatch"
    return True, "compatible"


def authorized_terminal(state):
    if not state.get("terminal"):
        return False
    try:
        verify_terminal_attestation(
            state,
            state.get("terminal_attestation"),
            os.environ.get("RX50_TERMINAL_AUTHORITY_SECRET", ""),
        )
        print("TERMINAL_AUTHORITY_VERIFIED")
        return True
    except Exception as exc:
        print("TERMINAL_AUTHORITY_HOLD:" + str(exc))
        return False


def main() -> int:
    queue = load(QUEUE)
    state = (
        load(STATE)
        if STATE.exists()
        else {
            "phase": "OBSERVE",
            "iteration": 0,
            "retry_count": 0,
            "terminal": False,
            "compatibility": expected_compatibility(queue),
        }
    )

    compatible, reason = validate_state_compatibility(state, queue)
    if not compatible:
        # Fail closed: do not mutate or advance incompatible durable state.
        print("HOLD: STATE_COMPATIBILITY_MISMATCH:" + reason)
        return 0

    queue_sha = sha256_bytes(QUEUE.read_bytes())
    previous_queue_sha = state.get("previous_queue_sha256")
    if previous_queue_sha and previous_queue_sha != queue_sha:
        state = checkpoint(state, phase="OBSERVE", queue_changed=True, iteration=0)
    else:
        state = checkpoint(state, phase="OBSERVE", queue_sha256=queue_sha)

    if state.get("terminal"):
        if authorized_terminal(state):
            print("TERMINAL:" + str(state.get("terminal_reason", "unspecified")))
            return 0
        checkpoint(
            state,
            phase="HOLD",
            result="HOLD: UNAUTHORIZED TERMINAL",
            last_error="persisted terminal state lacks valid external authority attestation",
        )
        return 3

    items = queue.get("queue", [])
    item = items[0] if items else {}
    evidence = item.get("evidence", [])
    owner = bool(item.get("owner_authorized", False))
    safety = bool(item.get("safety_authorized", False))
    frozen = bool(item.get("frozen", False))
    status = item.get("status")

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
        result = (
            "HOLD: ITERATION_LIMIT"
            if iteration > limit
            else "HOLD: REGISTERED AUDIT REQUIRED"
        )
        reason = (
            "iteration limit reached; resume only after new evidence/state change"
            if iteration > limit
            else "promotion requires the registered audit path"
        )
        state = checkpoint(state, phase="DECIDE", iteration=iteration)

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
