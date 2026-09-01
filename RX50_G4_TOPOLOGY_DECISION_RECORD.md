# RX50 G4 TOPOLOGY DECISION RECORD

Status: UNDECIDED
Date: 2026-08-15
Batch: G4-EVIDENCE-CLOSURE-01

## Decision state

- Topology A vs B: **UNDECIDED**. No measurement data exists to inform the decision; the owner decision is measurement-gated (RX50_G4_TOPOLOGY_A_B_DECISION_MATRIX.md). [STATUS]

## Required inputs before a decision can be recorded

| INPUT | STATUS |
|---|---|
| T-G4-01 measured RON (worst-case into RTH + RON + RTRACE < 10 k) | MEASUREMENT PENDING |
| T-G4-04 settling characterization | MEASUREMENT PENDING |
| T-G4-05 leakage at 3.3/5 V vs N_OFF | MEASUREMENT PENDING |
| T-G4-06 isolation blast radius | MEASUREMENT PENDING |
| Owner topology decision (A / B + rationale) | OWNER DECISION REQUIRED (after data) |

## Discipline

- A or B is NOT selected arbitrarily; no force-closing. UNDECIDED stands until evidence + owner record exist. [CONSTRAINT]