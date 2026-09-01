# M002 G4 EVIDENCE AUDIT

- Mission: M002 — G4 Evidence Availability & Closure Audit (data-gated)
- Date: 2026-08-15
- Status: COMPLETE
- Result: FINDINGS ONLY (NO design changes; NO raw data manufactured)

## Executive Status

**G4 CLOSURE BLOCKED — REQUIRED RAW EVIDENCE NOT PRESENT.**

All six required raw datasets (T-G4-01..06 / E1-E6) are ABSENT. The repository contains the full measurement protocol, test matrix, execution sequence, raw-data templates (empty), operator brief, and closure engine — but zero ingested measurement rows, zero instrument exports, zero waveform files, and no operator/date provenance records. Previous reports explicitly state "NO DATA INGESTED" and "Total rows ingested: 0". No file in the repository claims a measurement was performed, so no `REPORT CLAIM ONLY` upgrade applies; the correct classification for every dataset is ABSENT.

The closure audit's datasheet-level corrections (C-01, C-02, C-04) are confirmed as MODEL/DERIVATION corrections with verified inputs; they do NOT close any measurement-gated G4 item.

## Evidence Availability Matrix

| Test | Evidence Found | Classification | Traceability | Status | Closure Impact |
| ---- | -------------- | -------------- | ------------ | ------ | -------------- |
| T-G4-01 | E1 template (empty); RX50_G4_RON_RESULTS.md "NO DATA INGESTED" | ABSENT (protocol + template only) | None (0 rows) | BLOCKED | RON@3.3 V / 5 V cannot close; RAIN<10 kΩ viability check cannot run |
| T-G4-02 | E2 template (empty); raw register "0 rows" | ABSENT (protocol + template only) | None (0 rows) | BLOCKED | VIH/VIL@3.3 V margin vs 2.9 V cannot close |
| T-G4-03 | E3 template (empty); RX50_G4_ADC_RESULTS.md "NO DATA INGESTED" | ABSENT (protocol + template only) | None (0 rows) | BLOCKED | ±2 LSB @ RAIN<10 kΩ per-point verification cannot run |
| T-G4-04 | E4 template (empty); RX50_G4_SETTLING_RESULTS.md "0 captures" | ABSENT (protocol + template only) | None (0 waveform refs) | BLOCKED | Settling characterization cannot close; scan-time model stays unmeasured |
| T-G4-05 | E5 template (empty); RX50_G4_LEAKAGE_RESULTS.md "NO DATA INGESTED" | ABSENT (protocol + template only) | None (0 rows) | BLOCKED | Leakage regime (typ vs max) at 3.3/5 V cannot close |
| T-G4-06 | E6 template (empty); RX50_G4_ISOLATION_RESULTS.md "NO DATA INGESTED" | ABSENT (protocol + template only) | None (0 rows; current-limit log missing) | BLOCKED | Blast-radius characterization cannot close |

Supporting confirmation: `RX50_G4_RAW_EVIDENCE_REGISTER.md` (rows ingested 0), `RX50_G4_PROCESSED_RESULTS.md` (RAW DATA PRESENT? NO for all), `RX50_G4_EVIDENCE_QUALITY_REPORT.md` (rows assessed 0), `RX50_G4_DATASHEET_CONFLICT_REGISTER.md` (conflicts logged 0), `RX50_G4_CLOSURE_ENGINE.md` (items 1-6 MEASUREMENT PENDING), `RX50_G4_CLOSURE_REPORT.md` (G4 = MEASUREMENT PENDING). No CSV/TXT/log/instrument/scope files exist anywhere in the repository.

---

## T-G4-01

### Test ID
T-G4-01 — CD4067 RON @ 3.3 V (and 5 V)

### Purpose
(protocol wording) Measure CD4067 RON at VDD=3.3 V and 5 V per channel, per supply, per temperature; record min/max/mean/spread. No interpolation from the datasheet 5/10/15 V points.

### Required Evidence
Measured RON values (16 channels × VDD 3.3/5 V × ≥3 trials), 4-wire method, ITEST provenance, VDD, temperature, instrument, cal status, operator, date (closure engine item 1).

### Evidence Found
E1 template rows (empty); RON results table all NOT AVAILABLE; raw register "0 rows".

### Evidence Classification
ABSENT (protocol + template only)

### Verification Status
BLOCKED

### Closure Impact
Cannot close: RON@3.3 V design value, Rth + RON + RTRACE < 10 kΩ viability check, and topology (A vs B) input.

---

## T-G4-02

### Test ID
T-G4-02 — CD4067 VIH/VIL @ 3.3 V supply

### Purpose
(protocol wording) Determine CD4067 VIH/VIL at VDD=3.3 V (not in datasheet); compute margin vs STM32 GPIO VOH≥2.9 V / VOL≤0.4 V.

### Required Evidence
Input-voltage sweep per control input (A/B/C/D, INH) with defined output termination; VIH, VIL, hysteresis if observable; VDD, temp, instrument, operator, date (closure engine item 2).

### Evidence Found
E2 template rows (empty); no sweep data.

### Evidence Classification
ABSENT (protocol + template only)

### Verification Status
BLOCKED

### Closure Impact
Cannot close: 3.3 V path control-margin check. Note: the 5 V path VIH conflict (2.9 V < 3.5 V) is a datasheet-level DEFINITIVE conflict, independent of this test (see CD4067 Closure Review).

---

## T-G4-03

### Test ID
T-G4-03 — STM32F103 ADC accuracy vs RAIN

### Purpose
(protocol wording) Verify ±2 LSB max total error holds at RAIN < 10 kΩ (DS5319 guarantee); document behavior above 10 kΩ (regions A/B/C), multi-point across the ADC range.

### Required Evidence
Multi-point applied-voltage trials (≥5 per point) with recorded measured RAIN, applied voltage, VDDA, ADC clock = 14 MHz, tS = 55.5 cyc for the ~50 kΩ point, expected/measured code, error LSB, region by measured RAIN (closure engine item 3).

### Evidence Found
E3 template rows (empty); ADC results table all NOT AVAILABLE.

### Evidence Classification
ABSENT (protocol + template only)

### Verification Status
BLOCKED

### Closure Impact
Cannot close: per-point ADC error evidence; the ±2 LSB @ RAIN<10 kΩ claim remains a datasheet guarantee, NOT a project measurement.

---

## T-G4-04

### Test ID
T-G4-04 — CD4067 + network settling

### Purpose
(protocol wording) Measure settling after address / INH / channel-to-channel transitions, scope on the ADC node; characterization only (no owner band exists).

### Required Evidence
Oscilloscope waveform captures (≥5 per transition type) with waveform file references, probe C_in/type, scope settings, initial/final voltage, transient peak, settling time (closure engine item 4).

### Evidence Found
E4 template rows (empty); settling results table all NOT AVAILABLE; WAVEFORM_FILE references: NONE.

### Evidence Classification
ABSENT (protocol + template only)

### Verification Status
BLOCKED

### Closure Impact
Cannot close: settling characterization; scan-time model remains unmeasured (only the datasheet-derived floor bounds exist).

---

## T-G4-05

### Test ID
T-G4-05 — OFF-channel leakage effect vs channel count

### Purpose
(protocol wording) Measure node error vs OFF-channel count at VDD 3.3 V and 5 V; classify regime vs datasheet bounds (Option A 15 µA/node, Option B 63 µA/node at the 18 V condition); I_EFFECTIVE only if Z_EFFECTIVE known.

### Required Evidence
N_OFF sweep, node/ref voltages, delta, Z_EFFECTIVE (or I_EFFECTIVE = NOT ESTABLISHED), measurement floor, VDD, temp, instrument (closure engine item 5).

### Evidence Found
E5 template rows (empty); leakage results table all NOT AVAILABLE.

### Evidence Classification
ABSENT (protocol + template only)

### Verification Status
BLOCKED

### Closure Impact
Cannot close: measured leakage regime at 3.3/5 V. The 15/63 µA values are THEORETICAL bounds at the 18 V datasheet test condition (EV-13), NOT measured predictions.

---

## T-G4-06

### Test ID
T-G4-06 — Cross-channel isolation

### Purpose
(protocol wording) Short one channel; measure change in other channels' readings; characterize blast radius (same-MUX, cross-MUX, shared-node). No isolation spec exists (characterization only).

### Required Evidence
Source/victim measurements (≥3 trials per pair), fault type, mandatory verified current-limit value, expected/measured state, delta (closure engine item 6).

### Evidence Found
E6 template rows (empty); isolation results table all NOT AVAILABLE; current-limit verification log NOT RECEIVED.

### Evidence Classification
ABSENT (protocol + template only)

### Verification Status
BLOCKED

### Closure Impact
Cannot close: isolation blast-radius characterization.

---

## C-01 Review

- Previous conflict: claim of "4 parallel ADC conversions" (Option A scan model) vs STM32F103C8T6 which has 2 ADCs.
- Current evidence: DS5319 — 2x 12-bit ADC; dual regular simultaneous mode converts the SAME channel on both. 4 different channels cannot be converted simultaneously (closure audit S-17 / E-01).
- Resolution: the previous claim is INVALIDATED by datasheet evidence; model corrected to 64 sequential conversions (16 steps × 4) or 2×32 with both ADCs.
- Status: **RESOLVED at model level (datasheet evidence)**. Measurement of actual scan timing is still ABSENT (not a contradiction — an evidence gap). Do not treat the corrected floor as a measured fact.

## C-02 Review

- Previous conflict: continuity scan floor 17.7 µs vs ~64 µs.
- Source comparison: 17.7 µs = 16 × (tS_min + tCONV_min) — double-counts tS because tCONV already includes sampling (DS5319 Table 47 note: tCONV = tS + 12.5).
- Corrected derivation: Option A floor = 16 × 4 × tCONV_min = 16 × 4 × 1 µs = 64 µs (1 ADC, sequential); ~32 µs with 2 ADCs; Option B = 50 × 1 µs = 50 µs. All floors omit select/settle/software.
- Resolution: one derivation was arithmetically wrong; the conflict is RESOLVED by correction of inputs/formula, not by measurement.
- Status: **RESOLVED (derivation correction; DS5319 Table 47/48 inputs)**. No measured scan time exists; no owner scan-time requirement exists — so this is a model correction, NOT a design or measurement closure.

## C-04 Review

- Previous conflict: Option B leakage "~50 µA" vs 63 µA.
- Source comparison: shared node sees up to 63 OFF channels (64 positions − 1); at the 18 V datasheet condition, 63 × 1000 nA = 63 µA worst-case. The 50 µA figure undercounted channels.
- Resolution: bound corrected to 63 µA (closure audit S-19 / E-04).
- Status: **RESOLVED for the theoretical bound (datasheet input)**. The measured leakage at 3.3/5 V is still **UNRESOLVED — MEASUREMENT/EVIDENCE MISSING** (T-G4-05 required). No measured comparison exists; the 18 V bound is NOT a 3.3/5 V prediction.

---

## CD4067 Closure Review

| Item | Datasheet position (EV-id) | Protocol test | Closure status |
|---|---|---|---|
| RON @3.3 V | NOT SPECIFIED (EV-11); 5/10/15 V max 1050/400/240 Ω verified (EV-10) | T-G4-01 | DATASHEET-SUPPORTED BUT MEASUREMENT-CLOSURE PENDING |
| VIH/VIL @3.3 V | NOT SPECIFIED; @5 V VIH=3.5 V verified (EV-12) | T-G4-02 | DATASHEET-SUPPORTED BUT MEASUREMENT-CLOSURE PENDING |
| Settling | typical curves only, NO guaranteed value; charge injection NOT specified (EV-15) | T-G4-04 | DATASHEET-SUPPORTED BUT MEASUREMENT-CLOSURE PENDING |
| Leakage | OFF ±100 nA (25 °C)/±1000 nA (85-125 °C) @18 V; typ ±10 pA @10 V (EV-13); test-floor caveat | T-G4-05 | DATASHEET-SUPPORTED BUT MEASUREMENT-CLOSURE PENDING (transfer to 3.3/5 V is ASSUMPTION) |
| Signal level | VOH(min)=2.9 V @3.3 V (DS5319) < VIH@5 V=3.5 V → 5 V path DEFINITIVE conflict; 3.3 V supply within recommended 3-18 V (EV-12) | T-G4-02 | CONTRADICTION — RESOLUTION REQUIRED (architectural: level-shift vs 3.3 V path; owner decision, not measurement) |
| ADC interaction | RAIN<10 kΩ for ±2 LSB guarantee; RAIN 50 kΩ @55.5 cyc sampling bound (EV-04/05) | T-G4-03 | DATASHEET-SUPPORTED BUT MEASUREMENT-CLOSURE PENDING |
| Temperature | RON rises: 1200 Ω@85 °C / 1300 Ω@125 °C @5 V (closure audit §3.1) | T-G4-01 | coverage decision (25 °C only vs 85 °C soak) = OWNER |

No generic datasheet expectation is substituted for a project measurement. Every protocol-required measurement item remains pending.

---

## Verified Derivations

Each shows INPUTS → FORMULA → RESULT with sourced inputs.

1. **tCONV = tS + 12.5 cycles** — INPUT: DS5319 Table 47 note → RESULT: 14..252 cycles = 1..18 µs @ fADC=14 MHz. VERIFIED (EV-03).
2. **Option A scan floor (1 ADC, sequential)** — INPUT: steps 16 (4 MUX × 16 positions, CALCULATION), conversions/step 4 (Option A), tCONV_min = 1 µs (EV-03) → 16 × 4 × 1 µs = **64 µs** + selects/settles omitted. VERIFIED CALCULATION (not a measured fact; no owner scan-time requirement).
3. **Option A scan floor (2 ADCs)** — 16 × 2 × 1 µs = **32 µs**. VERIFIED CALCULATION (dual ADC applies to 2 distinct channels at a time).
4. **Option B scan floor** — INPUT: 50 steps, tCONV_min 1 µs → 50 × 1 µs = **50 µs**. VERIFIED CALCULATION.
5. **Option A OFF-leakage bound** — INPUT: 15 OFF channels/MUX node, 1000 nA/channel max @18 V 85-125 °C (EV-13) → 15 × 1000 nA = **15 µA** per node (theoretical, 18 V condition). VERIFIED CALCULATION.
6. **Option B OFF-leakage bound** — INPUT: 63 OFF channels shared node, 1000 nA/channel → **63 µA** worst-case (theoretical, 18 V condition). VERIFIED CALCULATION. NOT a 3.3/5 V prediction.
7. **RAIN<10 kΩ accuracy constraint** — INPUT: DS5319 ±2 LSB guarantee condition (EV-05) → design constraint Rth + RON + RTRACE < 10 kΩ. VERIFIED (EV-05).
8. **Sampling-feasibility bound** — INPUT: DS5319 Table 48 RAIN max 50 kΩ @ tS=55.5 cyc, fADC=14 MHz (EV-04) → Z_total ≤ 50 kΩ for sampling only, WITHOUT ±2 LSB guarantee. VERIFIED (EV-04).

## Blocked Derivations

1. **RON@3.3 V value** → DERIVATION BLOCKED — INPUT EVIDENCE MISSING (T-G4-01; datasheet NOT SPECIFIED; interpolation forbidden by protocol).
2. **Settling time constant t_RC = RON × C_node** → DERIVATION BLOCKED — RON@3.3 V missing; C_node includes assumed trace capacitance (flagged ASSUMPTION, closure audit E-07); settling must come from T-G4-04.
3. **Measured VIH/VIL margin vs 2.9 V** → DERIVATION BLOCKED — INPUT EVIDENCE MISSING (T-G4-02).
4. **Actual continuity scan time / settling time** → DERIVATION BLOCKED — no raw measurements (T-G4-04).
5. **Node error from leakage at 3.3/5 V** → DERIVATION BLOCKED — Z_EFFECTIVE and delta data missing (T-G4-05); the 18 V bound is not transferable.

No assumed values were used to complete any table.

---

## Evidence Register Changes

- **NO new raw evidence exists.** EV-30..EV-33 (Level-4 measurements) are NOT manufactured; they remain **MEASUREMENT PENDING**.
- No existing EV status changes: all Level-3 datasheet facts cited above were already VERIFIED (EV-03/04/05/10/11/12/13/15).
- Audit conclusion (absence confirmed across 6 result files + raw register + quality report + conflict register) is recorded here in M002 rather than as new EV rows.

## Contradiction Register Changes

- C-01: updated to **RESOLVED — model correction (DS5319 evidence: 2 ADCs, dual-mode = same channel)**. Measurement of actual scan timing remains absent (evidence gap, not a contradiction).
- C-02: updated to **RESOLVED — derivation correction (DS5319 Table 47: tCONV includes tS; floor 64 µs/32 µs/50 µs)**. No measured scan time exists.
- C-04: updated to **RESOLVED for the theoretical bound (63 µA, corrected)**; measured leakage at 3.3/5 V remains **UNRESOLVED — MEASUREMENT/EVIDENCE MISSING** (T-G4-05).
- No contradiction is deleted; no silent winner was chosen for any measurement-gated item.

## Open-Issue Changes

- No issue is closed. OI-04 (continuity), OI-09 (RON@3.3 V), OI-10 (settling), OI-11 (RAIN<10 kΩ) remain OPEN / MEASUREMENT PENDING.
- No new issue created: the audit confirms existing gaps (OI-16 "G4 Evidence Retrieval" file absent; provenance fields unfilled) and found no genuinely distinct new gap.

## G4 Closure Decision

Per closure item:

| Closure item | Status |
|---|---|
| CD4067 RON@3.3 V/5 V | BLOCKED — EVIDENCE MISSING (T-G4-01) |
| VIH/VIL@3.3 V | BLOCKED — EVIDENCE MISSING (T-G4-02) |
| ADC error vs RAIN | BLOCKED — EVIDENCE MISSING (T-G4-03) |
| Settling | BLOCKED — EVIDENCE MISSING (T-G4-04) |
| Leakage regime | BLOCKED — EVIDENCE MISSING (T-G4-05) |
| Isolation blast radius | BLOCKED — EVIDENCE MISSING (T-G4-06) |
| Datasheet-level bounds (15/63 µA, RAIN<10 kΩ, scan floors) | CLOSED — VERIFIED (datasheet-derived; model/derivation level only) |
| Topology A vs B owner decision | OPEN (measurement-gated; UNDECIDED) |
| 5 V path signal-level conflict | CONTRADICTION — RESOLUTION REQUIRED (architectural decision: level-shift vs 3.3 V path) |

**Overall G4 status: G4 BLOCKED — REQUIRED RAW EVIDENCE NOT PRESENT (missing test IDs: T-G4-01, T-G4-02, T-G4-03, T-G4-04, T-G4-05, T-G4-06).**

`G4 CLOSED` is NOT declared. G5 pin-map locking remains PROVISIONAL / NOT LOCKED.

## Missing Evidence

1. T-G4-01 raw RON rows (E1) — 0 rows.
2. T-G4-02 raw VIH/VIL sweep rows (E2) — 0 rows.
3. T-G4-03 raw ADC/RAIN rows (E3) — 0 rows.
4. T-G4-04 settling waveform files + rows (E4) — 0 captures, 0 file refs.
5. T-G4-05 raw leakage rows (E5) — 0 rows.
6. T-G4-06 raw isolation rows + current-limit verification log (E6) — 0 rows.
7. Provenance fields (instrument ID, cal status, operator, date) — unfilled.
8. G4 fixture values: ITEST, ladder values, settling band, temperature coverage — owner decisions, unrecorded.
9. "G4 Evidence Retrieval" / "G1 Evidence Register" files — referenced but absent (OI-16).

## Required Operator Actions

1. Build/approve the G4 fixture (CD4067B + STM32F103 board on one ADC pin) and execute T-G4-01..06 per RX50_G4_MEASUREMENT_EXECUTION_PROTOCOL.md.
2. Record instrument ID, cal status, operator, date/time on every row (provenance, closure engine item 9).
3. Select + record ITEST (T-G4-01) within datasheet absolute-max bounds; keep V_SW small; record per trial.
4. Record measured (not nominal) ladder resistor values (T-G4-03).
5. Record probe C_in and scope settings; attach waveform files (T-G4-04).
6. Record Z_EFFECTIVE or accept I_EFFECTIVE = NOT ESTABLISHED (T-G4-05).
7. Verify + log the fault-injection current limit BEFORE T-G4-06 (mandatory).
8. Decide temperature coverage (25 °C only vs 85 °C soak).

## Architecture Decisions Required

1. Topology A vs B — after T-G4-01/04/05/06 data.
2. CD4067 supply path: 3.3 V vs 5 V + level-shift (2.9 V VOH < 3.5 V VIH conflict is definitive; decision, not measurement).
3. Owner thresholds: continuity pass/fail, settling band, scan-time target, isolation spec (none exist).
4. Whether G4 closure includes an 85 °C soak (thermal data budget).

## Final Gate

### VERIFIED

- All six T-G4 datasets are ABSENT (0 rows ingested, 0 captures, 0 waveform refs, no provenance) — verified by direct inspection of 6 result files, raw evidence register, processed results, evidence-quality report, datasheet conflict register, closure engine, and closure report.
- No CSV/TXT/instrument/scope file exists anywhere in the repository.
- Datasheet-level facts remain verified: RON 1050/400/240 Ω @5/10/15 V (EV-10); RON@3.3 V NOT SPECIFIED (EV-11); VIH@5 V 3.5 V vs VOH 2.9 V → 5 V path conflict (EV-12, EV-08); RAIN<10 kΩ for ±2 LSB (EV-05); tCONV = tS + 12.5 (EV-03); 15 µA / 63 µA theoretical leakage bounds at 18 V condition (EV-13).
- Verified derivations: scan floors 64 µs (A/1-ADC), 32 µs (A/2-ADC), 50 µs (B); corrected leakage bound 63 µA.
- C-01, C-02, C-04 resolved at model/derivation level with datasheet inputs.

### NOT VERIFIED

- Any measured RON@3.3 V, VIH/VIL@3.3 V, ADC error vs RAIN, settling, leakage, or isolation value — none exist.
- Actual continuity scan time — no measurement; floors are lower-bound calculations only.
- Leakage behavior at 3.3/5 V — datasheet bounds are 18 V test-condition figures, not predictions.

### BLOCKED

- G4 closure (all six measurement items) — required raw evidence absent.
- Topology A/B selection (measurement-gated).
- G5 pin-map locking (downstream of G4 closure per owner direction).

### CONTRADICTIONS

- 5 V path signal-level conflict (2.9 V < 3.5 V) — RESOLUTION REQUIRED (architectural decision).
- Measured-leakage regime at 3.3/5 V — UNRESOLVED — MEASUREMENT/EVIDENCE MISSING (T-G4-05).
- C-01, C-02, C-04: resolved at model level; no measured confirmation exists.

### REQUIRED OPERATOR ACTIONS

- Execute T-G4-01..06 and fill E1-E6 with full provenance (instrument, cal, conditions, operator, date); attach T-G4-04 waveform files; verify/log T-G4-06 current limit; decide fixture values (ITEST, ladder, temperature coverage).
- Supply the referenced-but-absent "G4 Evidence Retrieval" file if it exists.

### NEXT MISSION

**M003 — G4 DATA ACQUISITION & INGESTION** (operator executes T-G4-01..06; harness ingests E1-E6 into the raw evidence register, runs F1-F7 processing, quality checks, measured-vs-datasheet conflict logging, and re-evaluates closure items 1-9).

Rationale: G4 is data-blocked; the only legitimate next step is obtaining/ingesting that evidence. M003 is blocked on operator measurements, so it is the correct next mission only when data exists. Contingency: if the operator cannot measure yet, the fallback is the G1 requirement-elicitation mission (fill sheet) to unblock the master gate; M003 then runs when raw data arrives. No closure mission is fabricated.

END MISSION M002.
