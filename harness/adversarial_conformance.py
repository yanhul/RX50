#!/usr/bin/env python3
"""Runtime adversarial conformance for the RX50 control plane."""
from __future__ import annotations
import importlib.util
import json
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_controller():
    spec = importlib.util.spec_from_file_location("rx50_controller_under_test", ROOT / "harness" / "controller.py")
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    return mod


def run_with_state(mod, queue_obj, state_obj):
    with tempfile.TemporaryDirectory() as td:
        d = Path(td); q = d / "queue.json"; s = d / "state.json"
        q.write_text(json.dumps(queue_obj)); s.write_text(json.dumps(state_obj))
        mod.QUEUE = q; mod.STATE = s
        return mod.main(), json.loads(s.read_text())


def test_terminal_tamper():
    mod = load_controller()
    rc, _ = run_with_state(mod, {"queue": []}, {"terminal": True, "terminal_reason": "FORGED"})
    assert rc != 0, "FORGED terminal state was accepted"


def test_evidence_bypass():
    mod = load_controller()
    rc, state = run_with_state(mod, {"queue": [{"id": "x", "status": "AUDIT_REQUIRED", "evidence": [], "owner_authorized": True, "safety_authorized": True, "frozen": True}]}, {"terminal": False})
    assert state.get("result", "").startswith("BLOCKED:"), f"evidence bypass was accepted: {state}"


if __name__ == "__main__":
    failures = []
    for test in (test_terminal_tamper, test_evidence_bypass):
        try: test()
        except Exception as exc: failures.append(f"{test.__name__}: {exc}")
    if failures:
        print("AIOS_ADVERSARIAL: BLOCKED")
        print("\n".join("- " + x for x in failures))
        raise SystemExit(1)
    print("AIOS_ADVERSARIAL: PASS")
