# RX50 AGENT RULES

## Mission

You are working on RX50 as a continuation of an RX24 engineering project.

Your job is to perform evidence-driven engineering analysis and project work, not to invent missing specifications.

## Mandatory rules

1. Never invent numerical specifications.
2. Never invent manufacturer evidence.
3. Never invent a part number when the source is unavailable.
4. Clearly label assumptions; prefer TBD/HOLD when an assumption would affect safety or architecture.
5. Treat RX24 as baseline, not as automatically valid for RX50.
6. RX50 has a simultaneous multi-channel firing requirement; do not reintroduce the obsolete RX24 single-channel concurrency constraint.
7. Before editing a design artifact, inspect the relevant baseline and explain the delta.
8. Preserve source files and use Git so changes can be reviewed and reverted.
9. For safety-critical changes, ask for approval before committing the change to the design.
10. When evidence conflicts, report the conflict instead of choosing silently.
11. Separate facts, calculations, assumptions, and recommendations.
12. Prefer manufacturer datasheets, explicit requirements, measurements, and test results.
13. Do not claim that a design is validated unless the required evidence/test exists.

## Workflow

READ -> INVENTORY -> EVIDENCE CHECK -> DELTA ANALYSIS -> PROPOSE -> APPROVAL -> EDIT -> TEST -> REVIEW

For large tasks, work in batches and leave a concise status artifact after each batch.

## First RX50 task

Perform a baseline delta audit from RX24 to RX50.

Do not modify schematic, PCB, firmware, or BOM during the first audit.

## RX50 ENGINEERING RULES (harness, added by M001)

Compatibility: the 12 rules below are compatible with the 13 Mandatory rules above (no conflicts identified; they add the harness registers as shared sources of truth and flagging labels). Where a rule overlaps, the stricter wording applies.

1. No unsourced numerical claims. Any value not traceable to a requirement, measurement, or datasheet is flagged `UNVERIFIED NUMERICAL CLAIM`.
2. No invented part numbers or manufacturer evidence.
3. No fake/paraphrased quotes from datasheets; quote the source section/page when a value is pinned.
4. No invented requirements.
5. Evidence resolution hierarchy (1 = most authoritative): 1 locked RX50 decisions -> 2 explicit requirements -> 3 manufacturer datasheets -> 4 verified measurements -> 5 derived calculations -> 6 assumptions -> 7 proposals -> 8 previous AI conclusions.
6. Registers in this repo (decisions/, evidence/, open_issues/, harness/state/CONTRADICTION_REGISTER.md) are the shared sources of truth for numeric/design data; do not quote one-off report text as authoritative.
7. Never present a derived calculation as a measured fact.
8. Do not edit a design artifact without inspecting the relevant baseline and explaining the delta.
9. Do not move existing files merely for organization; register any new location instead.
10. When evidence conflicts, do not pick a winner silently — log `CONTRADICTION DETECTED` in CONTRADICTION_REGISTER.md and report it.
11. An unsourced design decision is itself a flag: `UNVERIFIED NUMERICAL CLAIM` or `CONTRADICTION` as appropriate.
12. Do not claim a design is validated without the required evidence/test existing.

Harness locations: missions `harness/missions/<ID>_<NAME>.md`, templates `harness/templates/`, state `harness/state/`, evidence `evidence/`, decisions `decisions/`, open issues `open_issues/`, measurements `measurements/`, calculations `calculations/`, reports `reports/`.
