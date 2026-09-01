# RX50 G4 PROCESSED RESULTS

Status: NO DATA INGESTED
Date: 2026-08-15
Batch: G4-EVIDENCE-CLOSURE-01
Rule: processed results exist ONLY from ingested raw data. With zero raw rows, there are zero processed results. No value is computed, estimated, or inferred.

| TEST | RAW DATA PRESENT? | PROCESSED OUTPUTS | STATUS |
|---|---|---|---|
| T-G4-01 RON | NO | min/max/mean/spread, channel-to-channel variation: NOT AVAILABLE | MEASUREMENT PENDING |
| T-G4-02 VIH/VIL | NO | VIH/VIL, hysteresis, margin vs 2.9 V: NOT AVAILABLE | MEASUREMENT PENDING |
| T-G4-03 ADC vs RAIN | NO | EXPECTED_CODE, ERROR_LSB, region A/B/C: NOT AVAILABLE | MEASUREMENT PENDING |
| T-G4-04 settling | NO | settling time per capture, stats: NOT AVAILABLE | MEASUREMENT PENDING |
| T-G4-05 leakage | NO | delta_V, I_EFFECTIVE, regime classification: NOT AVAILABLE | MEASUREMENT PENDING |
| T-G4-06 isolation | NO | delta stats, blast-radius matrix: NOT AVAILABLE | MEASUREMENT PENDING |

## Processing integrity statement

- No measurement fabricated; no RON interpolated; no threshold invented; no uncertainty invented; no scan-time derived. [CONSTRAINT — satisfied by absence of data]
- Processing will run from RX50_G4_CALCULATION_RULES.md (F1-F7) once raw rows exist. [STATUS]