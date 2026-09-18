# Gate 2 lineage schema

Schema version: **2**

The lineage record is append-only provenance. It separates what happened from what an evaluator concluded.

## Record

- schema_version: lineage schema revision.
- lineage_id: stable identity for this observation.
- generation, candidate, parent_artifacts, delta: experiment lineage.
- observation: raw/controller observation; never a promotion verdict.
- claims, contradictions, constraints: evidence context.
- evaluation (optional): evaluator-owned conclusion.

## Observation execution binding

observation.execution is present even when no real external execution exists:

- effect_id
- attempt_id
- receipt_id
- provider

Unknown values are represented by the literal UNKNOWN; they are not fabricated identifiers.

Binding invariants:

1. A known attempt_id requires a known effect_id.
2. A known receipt_id requires both a known effect_id and attempt_id.
3. receipt_id=UNKNOWN is valid for an observation-only record.
4. A PASS evaluation cannot use an unknown receipt.
5. An execution with status=FAILED or UNKNOWN cannot receive a PASS evaluation.

## Evaluation

When present, evaluation requires:

- evaluator_id
- evaluator_version
- policy_version
- evidence_refs
- test_results
- verdict

Allowed verdicts: PASS, FAIL, BLOCKED, INCONCLUSIVE, UNKNOWN.

A top-level verdict is forbidden. An observation without an evaluation is valid and remains only an observation.

## Durable state compatibility fence

Controller state must carry:

- state_schema_version
- queue_schema_version
- controller_code_revision
- policy_revision

A mismatch or missing fence causes HOLD: STATE_COMPATIBILITY_MISMATCH and does not mutate or advance durable state. Migration is explicit; the authority path does not auto-migrate old state.
