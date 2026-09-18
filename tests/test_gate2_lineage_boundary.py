import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENGINE_PATH = ROOT / "harness" / "lineage" / "engine.py"

spec = importlib.util.spec_from_file_location("lineage_engine", ENGINE_PATH)
engine = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = engine
spec.loader.exec_module(engine)


def base_record():
    return {
        "schema_version": 2,
        "lineage_id": "L1",
        "generation": 1,
        "candidate": "BC5",
        "parent_artifacts": [],
        "delta": "observation",
        "observation": {
            "kind": "controller_observation",
            "controller_result": "BLOCKED: NO EVIDENCE",
            "evidence": [],
            "tests": {},
            "execution": {
                "effect_id": "UNKNOWN",
                "attempt_id": "UNKNOWN",
                "receipt_id": "UNKNOWN",
                "provider": "UNKNOWN",
            },
        },
        "claims": [],
        "contradictions": [],
        "constraints": [],
    }


def test_lineage_without_evaluation_is_observation_only():
    record = base_record()
    engine.validate_record(record)
    assert "evaluation" not in record
    assert "verdict" not in record


def test_effect_attempt_receipt_bindings_are_explicit_unknown_when_absent():
    record = base_record()
    execution = record["observation"]["execution"]
    assert execution == {
        "effect_id": "UNKNOWN",
        "attempt_id": "UNKNOWN",
        "receipt_id": "UNKNOWN",
        "provider": "UNKNOWN",
    }
    engine.validate_record(record)


def test_missing_receipt_cannot_support_verified_pass():
    record = base_record()
    record["observation"]["execution"] = {
        "effect_id": "effect-1",
        "attempt_id": "attempt-1",
        "receipt_id": "UNKNOWN",
        "provider": "test",
    }
    record["evaluation"] = {
        "evaluator_id": "eval",
        "evaluator_version": "1",
        "policy_version": "policy-1",
        "evidence_refs": ["EV-1"],
        "test_results": ["PASS"],
        "verdict": "PASS",
    }
    try:
        engine.validate_record(record)
    except ValueError as exc:
        assert "receipt" in str(exc)
    else:
        raise AssertionError("missing receipt bypassed PASS evaluation")


def test_fake_top_level_verdict_is_rejected():
    record = base_record()
    record["verdict"] = "PASS"
    try:
        engine.validate_record(record)
    except ValueError as exc:
        assert "inside evaluation" in str(exc)
    else:
        raise AssertionError("top-level verdict bypassed evaluation boundary")


def test_fake_evaluation_verdict_is_rejected():
    record = base_record()
    record["evaluation"] = {
        "evaluator_id": "eval",
        "evaluator_version": "1",
        "policy_version": "policy-1",
        "evidence_refs": ["EV-1"],
        "test_results": ["PASS"],
        "verdict": "CERTIFIED",
    }
    try:
        engine.validate_record(record)
    except ValueError as exc:
        assert "unsupported evaluation verdict" in str(exc)
    else:
        raise AssertionError("unsupported verdict accepted")


def test_execution_failure_after_observation_cannot_be_promoted_to_pass():
    record = base_record()
    record["observation"]["execution"] = {
        "effect_id": "effect-1",
        "attempt_id": "attempt-1",
        "receipt_id": "receipt-1",
        "provider": "test",
        "status": "FAILED",
    }
    record["evaluation"] = {
        "evaluator_id": "eval",
        "evaluator_version": "1",
        "policy_version": "policy-1",
        "evidence_refs": ["EV-1"],
        "test_results": ["PASS"],
        "verdict": "PASS",
    }
    try:
        engine.validate_record(record)
    except ValueError as exc:
        assert "failed or unknown execution" in str(exc)
    else:
        raise AssertionError("failed execution was promoted to PASS")


def test_known_receipt_requires_effect_and_attempt():
    record = base_record()
    record["observation"]["execution"] = {
        "effect_id": "UNKNOWN",
        "attempt_id": "UNKNOWN",
        "receipt_id": "receipt-1",
        "provider": "test",
    }
    try:
        engine.validate_record(record)
    except ValueError as exc:
        assert "known receipt" in str(exc)
    else:
        raise AssertionError("receipt binding escaped effect/attempt lineage")


def test_old_state_plus_new_controller_fails_closed():
    controller = (ROOT / "harness" / "controller.py").read_text()
    assert "STATE_SCHEMA_VERSION = 2" in controller
    queue = json.loads((ROOT / "state" / "bc_queue.json").read_text())
    old_state = {"iteration": 1, "phase": "YIELD", "terminal": False}
    # Reproduce the semantic compatibility check against a pre-fence state.
    spec = importlib.util.spec_from_file_location("rx50_controller", ROOT / "harness" / "controller.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    ok, reason = mod.validate_state_compatibility(old_state, queue)
    assert not ok
    assert "compatibility fence" in reason


def test_state_schema_mismatch_fails_closed():
    controller = importlib.util.spec_from_file_location("rx50_controller_schema", ROOT / "harness" / "controller.py")
    mod = importlib.util.module_from_spec(controller)
    sys.modules[controller.name] = mod
    controller.loader.exec_module(mod)
    queue = json.loads((ROOT / "state" / "bc_queue.json").read_text())
    state = {"compatibility": {
        "state_schema_version": 1,
        "queue_schema_version": 1,
        "controller_code_revision": mod.CONTROLLER_CODE_REVISION,
        "policy_revision": mod.POLICY_REVISION,
    }}
    ok, reason = mod.validate_state_compatibility(state, queue)
    assert not ok and "state_schema_version mismatch" in reason


def test_policy_mismatch_fails_closed():
    controller = importlib.util.spec_from_file_location("rx50_controller_policy", ROOT / "harness" / "controller.py")
    mod = importlib.util.module_from_spec(controller)
    sys.modules[controller.name] = mod
    controller.loader.exec_module(mod)
    queue = json.loads((ROOT / "state" / "bc_queue.json").read_text())
    state = {"compatibility": {
        "state_schema_version": mod.STATE_SCHEMA_VERSION,
        "queue_schema_version": mod.QUEUE_SCHEMA_VERSION,
        "controller_code_revision": mod.CONTROLLER_CODE_REVISION,
        "policy_revision": "rx50-policy-old",
    }}
    ok, reason = mod.validate_state_compatibility(state, queue)
    assert not ok and "policy_revision mismatch" in reason
