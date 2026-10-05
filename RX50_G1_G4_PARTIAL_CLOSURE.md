# RX50 G1/G4 PARTIAL CLOSURE — NON-AUTHORITATIVE

Status: PARTIAL / NOT PROMOTABLE
Purpose: record closure work that can be completed without inventing owner requirements or physical measurements.

## G1 — what is actually closed

| Sub-gate | Status | Evidence | Consequence |
|---|---|---|---|
| Candidate product identity | VERIFIED | `evidence/G1_WEB_VERIFICATION_2026-09-02.md` | Manufacturer/product traceability exists for candidate families. |
| Exact electrical load envelope | OPEN | Same evidence explicitly says authoritative current electrical data is incomplete. | No current/pulse/resistance requirement may be locked. |
| Simultaneous/worst-case channel requirement | OPEN | `RX50_G1_OWNER_REQUIREMENT_FILL_SHEET.md` remains unfilled. | No simultaneous-fire power or timing design may be promoted. |

G1 terminal state remains HOLD.

## G4 — what is actually closed

| Sub-gate | Status | Evidence | Consequence |
|---|---|---|---|
| ADC source-impedance rules | VERIFIED analytically | `RX50_G4_G5_CLOSURE_AUDIT.md` / DS5319 evidence | Use <10 kohm as the guaranteed ±2 LSB condition; 50 kohm is sampling feasibility, not accuracy guarantee. |
| CD4067 RON@3.3 V | OPEN / MEASUREMENT REQUIRED | Manufacturer does not specify it. | No 3.3 V RON value may be interpolated. |
| 5 V CD4067 logic compatibility | CONDITIONAL CONFLICT VERIFIED | STM32 guaranteed VOH relation vs CD4067 VIH@5 V | Requires an evidenced interface decision; no remedy selected. |
| Settling | OPEN / MEASUREMENT REQUIRED | CD4067 gives typical curves, not a guaranteed settling specification. | No settling margin may be promoted from calculation. |
| Leakage at actual RX50 supply | OPEN / MEASUREMENT REQUIRED | `PHASE2_EVIDENCE_CLOSURE.md` C-20c | Datasheet 18 V leakage bounds cannot be transferred to 3.3/5 V. |
| ADC accuracy vs measured RAIN | OPEN / MEASUREMENT REQUIRED | `RX50_G4_ADC_RESULTS.md`: 0 rows ingested | No physical ADC accuracy result exists. |
| Fixture/raw-data discipline | READY | `RX50_G4_RAW_DATA_TEMPLATES.md` | Measurement can be executed without changing acceptance semantics. |

G4 terminal state remains MEASUREMENT_PENDING.

## Legal next actions

1. G1: obtain authoritative electrical envelope for the selected exact initiator and owner-approved simultaneous requirement.
2. G4: execute the existing T-G4-01..06 fixture measurements and ingest raw rows with DUT/trial/VDD/TEMP/instrument/calibration/operator/time provenance.
3. Until then, keep AIOS result BLOCKED.

## Prohibited promotion

This document MUST NOT convert:
- candidate product identity -> electrical requirement;
- datasheet bound -> RX50 measured result;
- calculation -> physical measurement;
- working envelope -> owner requirement;
- partial closure -> G1/G4 VERIFIED.

