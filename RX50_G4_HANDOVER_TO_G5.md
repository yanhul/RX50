# RX50 G4 -> G5 HANDOVER

Status: BLOCKED — NO EVIDENCE TO HAND OVER
Date: 2026-08-15
Batch: G4-EVIDENCE-CLOSURE-01
Rule: G5 handover occurs ONLY after G4 is genuinely evidence-backed. G4 is MEASUREMENT PENDING, so NO handover content exists. G5 pin-map locking is NOT performed in this batch. [CONSTRAINT]

## Carry-forward items (to be filled when G4 closes)

| ITEM | STATUS NOW | CONTENT WHEN AVAILABLE |
|---|---|---|
| Measured RON (3.3 V / 5 V, per channel) | MEASUREMENT PENDING | worst-case RON for RTH + RON + RTRACE < 10 k |
| ADC behavior (error vs RAIN, regions A/B/C) | MEASUREMENT PENDING | per-point ERROR_LSB; ADC config verified |
| Settling characterization | MEASUREMENT PENDING | settling time per transition (characterization only) |
| Leakage evidence (3.3/5 V vs N_OFF) | MEASUREMENT PENDING | delta_V; I_EFFECTIVE (if Z known); regime |
| Isolation evidence (blast radius) | MEASUREMENT PENDING | blast-radius matrix (same/cross MUX, shared node) |
| Topology A/B decision | UNDECIDED | owner decision + rationale |
| Unresolved risks | PENDING | carry forward any INCONCLUSIVE items |

## Discipline

- No handover value is fabricated. The handover reopens when the G4 closure gate is satisfied. [STATUS]

---

G5 = NOT LOCKED
G1/G2 = HOLD
FIRING = OUT OF SCOPE