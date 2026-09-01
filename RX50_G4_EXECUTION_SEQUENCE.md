# RX50 G4 EXECUTION SEQUENCE

Status: COMPLETE (Part D of batch G4-MEAS-BATCH-01)
Date: 2026-08-15
Goal: execute the six G4 tests with minimal rewiring and a single verified fixture set.

## Fixture reuse map

- Fixture F1 (DUT bench): CD4067B + controllable address/INH + supply + Kelvin terminals. Used by: T-G4-01 (RON), T-G4-02 (VIH/VIL). No rewiring between them except switching from 4-wire sense to control sweep.
- Fixture F2 (ADC path): STM32F103C8T6 board, ADC pin, calibrated ladder + supply + stable reference. Used by: T-G4-03 (ADC accuracy).
- Fixture F3 (combined node): CD4067B MUX network + ADC node + scope probe. Used by: T-G4-05 (leakage), T-G4-04 (settling), T-G4-06 (isolation). T-G4-05 and T-G4-06 share the node termination; T-G4-04 only adds the scope probe.

Rewiring minimization: F1 for T-G4-01/T-G4-02; F2 standalone for T-G4-03; F3 for T-G4-05 -> T-G4-04 -> T-G4-06 (one node, no rewire between them). [RECOMMENDATION]

## 1. Fixture preparation sequence

1. Build F1, F2, F3 at topology level (no schematic/PCB). [CONSTRAINT]
2. Select + record test resistor values (OWNER TEST VALUE - TBD); measure them with the DMM and record measured values. [OWNER GROUP 1]
3. Tag DUT(s) with DUT_ID; record board revision for F2. [CONSTRAINT]
4. Wire Kelvin/4-wire sense for F1 RON ports; keep lead/contact resistance low. [RECOMMENDATION]
5. Provide mandatory current-limit element in the fault-injection path of F3 (value recorded). [CONSTRAINT (A-07)]
6. Prepare scope with low-C probe; record probe C_in and bandwidth settings. [CONSTRAINT (A-04)]

## 2. Instrument verification sequence

1. PSU: verify VDD set-points at 3.3 V and 5 V with the DMM; record. [RECOMMENDATION]
2. DMM: self-cal/calibration status recorded; verify a reference resistor (e.g., a known-value unit) before use. [RECOMMENDATION]
3. Scope: probe compensation check; record channel bandwidth/probe factor. [RECOMMENDATION]
4. Record instrument IDs + calibration status in the log. [CONSTRAINT]

## 3. DUT initialization

1. Power sequence: connect rails, verify, then enable DUT supply; do not apply signals with supply off. [CONSTRAINT]
2. Set CD4067 INH per test plan; reset address to a known state. [RECOMMENDATION]
3. For F2: load the ADC firmware (config: fADC=14 MHz, tS recorded); perform ADC self-calibration per DS5319 recommendation. [FACT]
4. Record ambient temperature and any soak plan (owner Group 1). [CONSTRAINT]

## 4. Test order (execution sequence)

1. T-G4-01 (RON) on F1 — no ADC involvement. [ORDER]
2. T-G4-02 (VIH/VIL) on F1 — reuse F1, switch to control sweep. [ORDER]
3. T-G4-03 (ADC accuracy) on F2 — standalone ADC path. [ORDER]
4. T-G4-05 (leakage) on F3 — node + termination. [ORDER]
5. T-G4-04 (settling) on F3 — add scope probe only. [ORDER]
6. T-G4-06 (isolation) on F3 — fault injection last (current-limited). [ORDER]

Rationale: RON first (isolates DUT switch behavior), control logic second, ADC path third (independent), then node-level tests grouped to avoid rewiring; fault injection last to protect the fixture. [RECOMMENDATION]

## 5. Supply transitions

1. Between 3.3 V and 5 V runs: allow stabilization (owner-approved soak), re-verify the reference/calibration point, then read. [CONSTRAINT (A-08)]
2. Record supply settling and any drift. [RECOMMENDATION]
3. For VDD = 5 V runs (T-G4-01 RON@5 V channel-side; T-G4-05/T-G4-06 5 V condition): the 5 V-referenced sense node MUST NOT be connected directly to the STM32 ADC input. Owner decision D-03 OPTION B (M003E): characterize CD4067/channel-side behavior at 5 V; do NOT expose the 5 V-referenced sense node to the ADC; do NOT invent an attenuation/clamp network; any ADC observation requiring the valid STM32 ADC range is performed under an appropriate supply/test condition (e.g., 3.3 V). [CONSTRAINT — owner decision D-03 (M003E), Option B]

## 6. Temperature transitions

1. If 85 C soak approved: stabilize before reading (owner decision on duration); record reached temperature. [TBD / OWNER]
2. Cool-down and re-read ambient for drift assessment if required. [RECOMMENDATION]

## 7. Calibration / reference checks

1. Re-verify the reference resistor / ADC full-scale reference (VDDA) at the start, between supply transitions, and at session end. [CONSTRAINT]
2. Any drift flagged in the uncertainty record. [CONSTRAINT]

## 8. Raw-data capture sequence

1. Per test, use the Part E template row-by-row; fill all applicable fields; blank mandatory field = trial INVALID. [CONSTRAINT]
2. Capture scope waveforms for T-G4-04 with file references. [CONSTRAINT]
3. Record instrument-measured applied voltage (not nominal) for T-G4-03 EXPECTED_CODE. [CONSTRAINT (A-09)]

## 9. Repeat sequence

1. Minimum trials per the Part C matrix (>=3 for T-G4-01/02/05/06; >=5 for T-G4-03; >=5 captures for T-G4-04). [CONSTRAINT]
2. Repeats spread across the session to capture drift. [RECOMMENDATION]

## 10. Shutdown sequence

1. Complete all register rows; close open trial blocks. [CONSTRAINT]
2. Remove fault-injection connections first (F3). [RECOMMENDATION]
3. Power down supplies; disconnect ADC pin loads. [RECOMMENDATION]
4. Assemble evidence package (Part H/Closure Engine, 12 items). [CONSTRAINT]

## Task separation

- MUST physically measure: T-G4-01, T-G4-02, T-G4-03, T-G4-04, T-G4-05, T-G4-06. [STATUS]
- CAN be calculated (after raw data): RON stats; ERROR_LSB; delta_V and I_effective (if Z known); settling-time stats; blast-radius stats. [CALCULATION]
- CAN be checked against datasheet (where applicable): RON@5 V vs 1050 ohm max (25 C); VIH@5 V=3.5 V reference; OFF leakage 18 V-condition bounds (15 uA/63 uA, labeled theoretical); RAIN Table 48 50 kohm sampling bound. [STATUS]
- REQUIRES OWNER DECISION: ITEST, ladder values, temp coverage, sample count, instruments (GROUP 1); settling/isolation/continuity thresholds (GROUP 2). [STATUS]
- NOT REQUIRED FOR G4: G5 pin-map locking, G1/G2 conclusions, firing values, schematic/PCB/BOM/divider design values. [CONSTRAINT]