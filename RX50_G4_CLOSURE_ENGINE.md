# RX50 G4 CLOSURE ENGINE

Status: COMPLETE (Part H of batch G4-MEAS-BATCH-01)
Date: 2026-08-15
Rule: G4 is NOT declared closed without physical evidence. "CLOSED" is never used pre-emptively.

## Closure checklist (machine-readable)

| # | ITEM | STATUS |
|---|---|---|
| 1 | T-G4-01 evidence exists (RON@3.3 V/5 V, 4-wire, provenance) | MEASUREMENT PENDING |
| 2 | T-G4-02 evidence exists (VIH/VIL@3.3 V + margin) | MEASUREMENT PENDING |
| 3 | T-G4-03 evidence exists (ADC error LSB vs RAIN, multi-point) | MEASUREMENT PENDING |
| 4 | T-G4-04 evidence exists (settling captures) | MEASUREMENT PENDING |
| 5 | T-G4-05 evidence exists (node error vs N_OFF) | MEASUREMENT PENDING |
| 6 | T-G4-06 evidence exists (isolation blast radius) | MEASUREMENT PENDING |
| 7 | Topology decision recorded (A/B + rationale) | OWNER DECISION REQUIRED (measurement-gated) |
| 8 | Datasheet conflicts logged | READY (register exists; none logged yet) |
| 9 | Provenance complete (instrument, conditions, operator, dates) | READY (templates exist; fills pending) |

STATUS vocabulary: READY / MEASUREMENT PENDING / OWNER DECISION REQUIRED / BLOCKED / COMPLETE.

## G4_STATUS computation

- OPEN: nothing executed. (NOT current state)
- MEASUREMENT PENDING: all six tests planned, none executed, owner Group 1 inputs outstanding. (CURRENT)
- PARTIALLY EVIDENCED: 1-4 of the six tests have data. (future)
- CLOSEABLE: all six tests have data with provenance, conflicts logged, owner topology decision recorded. (future)
- EVIDENCE-BACKED: CLOSEABLE and the closure statement signed. (future)

## Current computed status

G4_STATUS = **MEASUREMENT PENDING** — items 1-6 pending physical measurement, item 7 pending owner decision, items 8-9 READY.

## Gate transition rules

- Items 1-6 move MEASUREMENT PENDING -> COMPLETE only when raw+processed data with provenance is filed in the evidence package. [CONSTRAINT]
- Item 7 moves OWNER DECISION REQUIRED -> COMPLETE only when the owner records A or B with rationale (after 1-6). [CONSTRAINT]
- Item 8: any measured-vs-datasheet divergence creates a DATASHEET CONFLICT RECORD; register stays READY until such a record exists, then -> COMPLETE (logged). [CONSTRAINT]
- Item 9 -> COMPLETE when every trial row has instrument/conditions/operator/date. [CONSTRAINT]
- G5 locking is NOT part of this engine; it is downstream and remains PROVISIONAL / NOT LOCKED. [CONSTRAINT]