# RX50 G4 EVIDENCE QUALITY REPORT

Status: NO EVIDENCE RECEIVED
Date: 2026-08-15
Batch: G4-EVIDENCE-CLOSURE-01

## Assessment

- Evidence rows assessed: 0. The quality flags below cannot be evaluated because no raw data was supplied. [STATUS]

| QUALITY FLAG | ROWS AFFECTED | RESULT |
|---|---|---|
| Missing provenance | 0 | NOT ASSESSED (no rows) |
| Missing instrument ID | 0 | NOT ASSESSED |
| Missing calibration status | 0 | NOT ASSESSED |
| Missing temperature | 0 | NOT ASSESSED |
| Missing DUT ID | 0 | NOT ASSESSED |
| Missing trial number | 0 | NOT ASSESSED |
| Unverified test value | 0 | NOT ASSESSED |
| Impossible / out-of-range condition | 0 | NOT ASSESSED |
| Inconsistent units | 0 | NOT ASSESSED |
| Duplicate / incomplete rows | 0 | NOT ASSESSED |

## Rule

- When data is ingested, any row failing a quality check is marked INVALID and REMAINS VISIBLE (never silently repaired). [CONSTRAINT — active on future ingest]
- Test values must carry the TEST VALUE label + verification record (per owner authorization). [CONSTRAINT]

## Operator requirement

Supply filled templates E1-E6 (or equivalent CSV) with all common + test-specific fields; only then can quality assessment and processing begin. [STATUS]