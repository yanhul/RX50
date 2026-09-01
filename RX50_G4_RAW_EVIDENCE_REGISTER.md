# RX50 G4 RAW EVIDENCE REGISTER

Status: NO DATA INGESTED
Date: 2026-08-15
Batch: G4-EVIDENCE-CLOSURE-01
Rule (HARD): raw measurement data was NOT provided by the operator in this batch. No measurement is fabricated, estimated, interpolated, completed, or inferred. All registers remain empty until real data is supplied.

## Ingestion state

| REGISTER | TEMPLATE SOURCE | ROWS INGESTED | STATUS |
|---|---|---|---|
| E1 T-G4-01 (RON) | RX50_G4_RAW_DATA_TEMPLATES.md | 0 | MEASUREMENT PENDING |
| E2 T-G4-02 (VIH/VIL) | same | 0 | MEASUREMENT PENDING |
| E3 T-G4-03 (ADC vs RAIN) | same | 0 | MEASUREMENT PENDING |
| E4 T-G4-04 (settling) | same | 0 | MEASUREMENT PENDING |
| E5 T-G4-05 (leakage) | same | 0 | MEASUREMENT PENDING |
| E6 T-G4-06 (isolation) | same | 0 | MEASUREMENT PENDING |

## Required input for ingestion (operator)

For each test, provide the filled template (or equivalent CSV) with the common fields and test-specific fields:
- Common: TEST_ID, DUT_ID, TRIAL, VDD, TEMP, CHANNEL, CONDITION, INPUT, OUTPUT, VALUE, UNIT, INSTRUMENT, INSTRUMENT_ID, CAL_STATUS, OPERATOR, DATE, TIME, REMARK.
- E3 adds: RAIN_MEASURED, APPLIED_V (measured), VDDA, SAMPLE_TIME_CYC, ADC_CLOCK_MHZ, EXPECTED_CODE, MEASURED_CODE, ERROR_LSB, REGION.
- E4 adds: WAVEFORM_FILE, PROBE_C_IN, PROBE_TYPE, SCOPE_SETTINGS.
- E5 adds: N_OFF, NODE_V, REF_V, DELTA_V, Z_EFFECTIVE, I_EFFECTIVE, MEAS_FLOOR.
- E6 adds: SOURCE_CH, VICTIM_CH, POPULATION, FAULT_TYPE, CURRENT_LIMIT, EXPECTED_STATE, MEASURED_STATE, DELTA.

Ingestion rule: rows are appended as-is; no value is modified during ingest. Rows failing quality checks are marked INVALID and remain visible (never silently repaired). [CONSTRAINT]

## Current state

Total rows ingested: 0. Nothing to process. Re-run this batch when operator supplies the raw data. [STATUS: MEASUREMENT PENDING]