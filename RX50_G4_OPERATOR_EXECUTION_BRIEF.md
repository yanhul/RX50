# RX50 G4 OPERATOR EXECUTION BRIEF (RUN CARD)

Status: READY TO MEASURE (owner input complete, 2026-08-15)
Date: 2026-08-15
Purpose: operator-facing run card for T-G4-01..06. Physical data = MEASUREMENT PENDING until executed and logged. No design value / no requirement is created by any test value.

## Owner-approved conditions (verbatim intent)

- Fixture: F1/F2/F3 topology-level build APPROVED.
- Temperature: AMBIENT ONLY, recorded per trial.
- DUT: SINGLE unit (characterization). Multiple units deferred.
- Test values: operator SELECTS and RECORDS as TEST VALUE: ITEST, ADC ladder, node termination, measurement protection. Every value VERIFIED before use. No design value or requirement inferred.
- T-G4-06: fault-injection current limit VERIFIED before T-G4-06.
- Group 2 thresholds: absent -> characterization-only results.

## TEST VALUE protocol (mandatory)

1. Every selected value is labeled TEST VALUE in the log (never "design value").
2. Value verified before use: measure/confirm with the DMM; record the measured value.
3. No requirement (pass/fail threshold, scan-time, settling band, margin) is created by a test value.
4. If a value is questioned later, its TEST VALUE label and verification record stand as the provenance.

## Instrument log (fill before first measurement)

- PSU: ID ___ / cal ___ / set-points 3.3 V & 5 V verified with DMM: ___ / date ___
- DMM: ID ___ / cal ___ / 4-wire verified on reference resistor: ___ / ref value ___
- Scope (needed for T-G4-04): ID ___ / cal ___ / probe type ___ / probe C_in ___ / BW ___
- Operator name(s): ___ (recorded per trial)

## Run order and per-test gates

| ORDER | TEST | FIXTURE | PRE-RUN GATE |
|---|---|---|---|
| 1 | T-G4-01 RON | F1 | ITEST selected + recorded as TEST VALUE; Kelvin wired; DMM 4-wire verified |
| 2 | T-G4-02 VIH/VIL | F1 | switch-state observation load selected + recorded |
| 3 | T-G4-03 ADC vs RAIN | F2 | ladder values selected, measured, recorded as TEST VALUE; ADC config (fADC=14 MHz, tS) set; VDDA verified |
| 4 | T-G4-05 leakage | F3 | node termination Z_effective selected, measured, recorded (else I_EFFECTIVE = NOT ESTABLISHED) |
| 5 | T-G4-04 settling | F3 | scope probe compensated; C_in + BW recorded |
| 6 | T-G4-06 isolation | F3 | current-limit element VERIFIED before run (owner requirement); value recorded |

## Per-test checklist

- T-G4-01: 16 ch x VDD 3.3/5 x >=3 trials; log E1; compute RON=V_SW/ITEST, min/max/mean/spread. [CALCULATION]
- T-G4-02: control sweep @3.3 V; log E2; report VIH/VIL + margin vs 2.9 V; hysteresis if observable.
- T-G4-03: points ~1k/10k/50k (measured values); >=5 trials; log E3; EXPECTED_CODE from measured applied V / VDDA; region A/B/C by measured RAIN.
- T-G4-05: N_OFF sweep 0..15; log E5; delta_V; I_effective only if Z known; classify above measurement floor only.
- T-G4-04: transitions address/INH/channel; >=5 captures; log E4 with WAVEFORM_FILE; characterization only (no threshold).
- T-G4-06: same-MUX / cross-MUX victims; >=3 trials per pair; log E6; blast radius only (no isolation criterion).

## End-of-session

- Complete all log rows (blank mandatory field = trial INVALID). [CONSTRAINT]
- Remove fault-injection connections first; power down.
- Log any datasheet conflict into a DATASHEET CONFLICT RECORD (never "correct" the measurement).
- Assemble evidence package (12 items, protocol Section 20).
- Fill the G4 closure statement template (RX50_G4_CLOSURE_ENGINE.md). Do NOT pre-declare closure.

---

G4 = READY TO MEASURE
G5 = NOT LOCKED
G1/G2 = HOLD
FIRING = OUT OF SCOPE