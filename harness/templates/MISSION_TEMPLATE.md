# RX50 MISSION TEMPLATE

Copy to `harness/missions/<ID>_<SHORT_NAME>.md`; replace `<...>` fields. Leave a status artifact after each batch (Workflow rule).

## Header

- Mission ID: `<MXXX>`
- Title: `<short name>`
- Date: `<YYYY-MM-DD>`
- Status: DRAFT / IN PROGRESS / COMPLETE
- Result: CHANGES MADE | NO CHANGES MADE | FINDINGS ONLY
- Input artifacts: `<list of source files read>`

## Mission definition

- Objective: `<one or two sentences>`
- Deliberately NOT in scope (prohibited): `<list; e.g., no schematic/PCB/BOM/firmware changes, no firing numbers invented>`
- Approval required before changes: `<YES for safety-critical / design artifacts / NO for discovery-prepare>`

## Evidence hierarchy (apply in this order)

1 locked decisions -> 2 explicit requirements -> 3 manufacturer datasheets -> 4 verified measurements -> 5 derived calculations -> 6 assumptions -> 7 proposals -> 8 previous AI conclusions.

## Workflow

READ -> INVENTORY -> EVIDENCE CHECK -> DELTA ANALYSIS -> PROPOSE -> APPROVAL -> EDIT -> TEST -> REVIEW

For large tasks: work in batches; after each batch record status in `harness/state/project_state.md`.

## Rules carried into every mission

1. No unsourced numerical claims -> tag `UNVERIFIED NUMERICAL CLAIM`.
2. No invented part numbers / manufacturer evidence / datasheet quotes.
3. No invented requirements.
4. No merging/closure of open issues; flag `POSSIBLE DUPLICATE — REVIEW REQUIRED`.
5. No silent winner on conflicting evidence -> `CONTRADICTION DETECTED` (log in CONTRADICTION_REGISTER.md).
6. Derived calculations are never presented as measured facts.
7. No design artifact edit without inspecting baseline + explaining delta.
8. Preserve sources; use Git; every safety-critical change needs approval.
9. No claim of validation without required evidence/test.
10. Do NOT reintroduce RX24 `MAX_CONCURRENT_FIRE=1` or any RX24 firing assumption.

## Final gate (include in report)

- VERIFIED findings (with evidence IDs)
- UNVERIFIED NUMERICAL CLAIMS
- CONTRADICTIONS (see register)
- OPEN ISSUES affected
- MISSING EVIDENCE / gaps
- Files created / modified / untouched
- Harness readiness: NOT READY | READY FOR G4/G5 EVIDENCE AUDIT
- Recommended next mission: `<exactly one, with rationale>`