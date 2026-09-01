# RX50 G4 CLOSURE EVIDENCE PLAN
# (MEASUREMENT CLOSURE ROADMAP + DATA REGISTER TEMPLATE)

Status: PLAN FOR OWNER APPROVAL (no measurements executed yet)
Date: 2026-08-15
Input: RX50_G4_G5_CLOSURE_AUDIT.md (Section 18), RX50_G4_G5_HARDWARE_FEASIBILITY_REPORT.md (Section 12).
Owner direction: "dong G4 bang evidence truoc, roi moi lock G5" -> G4 is closed ONLY with hardware evidence; G5 pin-map locking is downstream of G4 closure.
Scope: fixture definition (topology level), test procedures, pass/fail decision logic, evidence register template. No schematic/PCB/BOM. No divider values. No thresholds invented. G1/G2 HOLD. No firing values.

Label legend:
- [FACT] / [CALCULATION] / [ASSUMPTION] / [RECOMMENDATION]
- Status: LOCKED / EVIDENCE-BACKED / HOLD / TBD / NEEDS RECHECK / OPEN / PROVISIONAL / CLOSEABLE / MEASUREMENT PENDING

---

## 1. Purpose and gating rule

- G4 (continuity measurement feasibility) closes ONLY when the measurement results below are recorded with provenance and satisfy the decision rules in Section 6. [RECOMMENDATION]
- G5 pin-map/topology locking is BLOCKED by G4 closure (owner direction). [CONSTRAINT]
- This plan is operational: it defines WHAT to measure, HOW, and WHAT to record so that closure is evidence-gated. It does not invent values. [STATUS]

## 2. Non-negotiables

1. CD4067 RON@3.3V is NOT interpolated from the 5/10/15 V datasheet points; only measured values are used. [CONSTRAINT]
2. No continuity threshold, scan-time target, or settling margin is invented. Criteria are marked TBD where no owner requirement exists. [CONSTRAINT]
3. Every recorded value carries: instrument, conditions (VDD, temperature), trial count, operator, date. [CONSTRAINT]
4. If measurement contradicts a datasheet bound, the conflict is REPORTED, not silently resolved. [CONSTRAINT]
5. Reopen is allowed at any time if new evidence conflicts. [CONSTRAINT]

## 3. Fixture definition (topology level, NOT a schematic)

- DUT: one CD4067B unit (sample unit(s) recorded) + an STM32F103C8T6 board exposing at least one ADC pin (e.g. PA0). [ASSUMPTION on access to the chosen board]
- Supplies: bench PSU for VDD = 3.3 V and 5 V cases; VDDA for the STM32 at 3.3 V. [FACT on needs]
- Instruments (minimum): 4.5+ digit DMM (resistance/voltage), calibrated resistors ladder (values recorded, chosen by owner), oscilloscope (settling), temperature control or recorded ambient (25 C; optional 85 C soak). [RECOMMENDATION — instrument list is an assumption, not a spec]
- Control: MCU GPIO drives CD4067 A/B/C/D and INH; addresses stepped; a known termination on selected channels. [ASSUMPTION]
- Topology: continuity sense path model under test = Rth(divider) + RON + R_trace into ADC. Divider values intentionally ABSENT (out of batch scope). [CALCULATION]

## 4. Test procedures T-G4-01..06 (operational)

### T-G4-01 — CD4067 RON @ 3.3 V (and 5 V)
- Setup: VDD=3.3 V (repeat at 5 V); force small current through a selected channel; measure voltage drop across channel (4-wire preferred). [ASSUMPTION on method]
- Measure: RON per channel (16), per supply, per temperature (25 C; optional 85 C); record min/max/mean/spread. [FACT on what feeds topology]
- Record: table per Section 5.
- Decision logic: topology-viability check only — whether Rth + RON(max measured) + trace can satisfy the 10 k ohm accuracy constraint with margin; margin value TBD (owner). [CALCULATION -> rule]

### T-G4-02 — CD4067 VIH/VIL @ 3.3 V supply
- Setup: VDD=3.3 V; sweep control input voltage; observe channel switch state.
- Measure: VIH, VIL at 3.3 V supply (not in datasheet -> must be measured). [FACT -> NEEDS MEASUREMENT]
- Record: values + margin vs 3.3 V logic high/low (STM32 GPIO VOH>=2.9 V, VOL<=0.4 V). [CALCULATION]
- Decision logic: 3.3 V path control-margin check; threshold for acceptable margin TBD. [OPEN]

### T-G4-03 — STM32F103 ADC accuracy vs RAIN
- Setup: known calibrated resistor ladder into ADC pin; compare ADC code vs ideal. [ASSUMPTION on method]
- Measure: error in LSB at RAIN ~ 1 k / 10 k / 50 k ohm (exact ladder values recorded). [CALCULATION]
- Decision logic: verify +-2 LSB max ET holds at RAIN < 10 k ohm (datasheet guarantee); document deviation above 10 k. Criterion at 50 k = document-only (no requirement). [FACT -> rule]

### T-G4-04 — CD4067 + network settling
- Setup: step address (and INH) while scope monitors the ADC node; reference settle band TBD (owner threshold, e.g. X mV / N bits — NOT invented here). [ASSUMPTION; threshold TBD]
- Measure: time to settle within the TBD band, per channel. [TBD]
- Record: settling time per channel; note charge-injection/coupling transients. [FACT -> TBD]
- Decision logic: feeds scan-time model; no requirement violated until threshold exists. [STATUS]

### T-G4-05 — OFF-channel leakage effect vs channel count
- Setup: terminate all-but-one channel; measure node voltage error as OFF channel count increases; VDD 3.3 V and 5 V. [ASSUMPTION]
- Measure: node error vs OFF-channel count; compare to datasheet upper bounds (Option A 15 uA/node; Option B 63 uA shared node, corrected). [CALCULATION]
- Decision logic: report whether actual leakage is closer to typical (pA) or datasheet max (100 nA / 1000 nA) regime; no threshold invented. [STATUS]

### T-G4-06 — Cross-channel isolation
- Setup: short one channel; read neighboring/other channels. [ASSUMPTION]
- Measure: change in other channels' readings (Option A: within MUX group and across MUXes; Option B: shared node). [CALCULATION]
- Decision logic: blast-radius characterization; isolation spec TBD (owner). [OPEN]

## 5. Evidence register template (fill during execution)

| TEST | TRIAL | VDD (V) | TEMP (C) | CHANNEL | VALUE | UNIT | INSTRUMENT | OPERATOR | DATE | REMARKS |
|---|---|---|---|---|---|---|---|---|---|---|
| T-G4-01 | 1 | 3.3 | 25 | 0..15 | | ohm | | | | 4-wire |
| T-G4-01 | 1 | 5.0 | 25 | 0..15 | | ohm | | | | 4-wire |
| T-G4-02 | 1 | 3.3 | 25 | - | VIH= / VIL= | V | | | | |
| T-G4-03 | 1 | 3.3 | 25 | PA0 | err= | LSB | | | | RAIN= k |
| T-G4-04 | 1 | 3.3 | 25 | - | ts= | us | | | | band=mV(TBD) |
| T-G4-05 | 1 | 3.3 | 25 | node | err= | mV | | | | N_off= |
| T-G4-06 | 1 | 3.3 | 25 | - | dV= | mV | | | | short@ch |

- Each row requires provenance; partial fills are allowed but marked MEASUREMENT PENDING. [CONSTRAINT]
- On completion, rows migrate into a G4 evidence file with a closure statement (Section 6). [RECOMMENDATION]

## 6. G4 closure decision rule (evidence-gated)

G4 closes to "EVIDENCE-BACKED" when ALL of the following hold (else remains OPEN/MEASUREMENT PENDING):
1. T-G4-01 delivered RON@3.3V (and 5V) measured values with spread recorded. [MEASUREMENT]
2. T-G4-02 delivered VIH/VIL@3.3V with margin computed vs STM32 VOH/VOL. [MEASUREMENT]
3. T-G4-03 verified +-2 LSB at RAIN<10 k and documented behavior above. [MEASUREMENT]
4. T-G4-04 delivered measured settling (band = owner-defined). [MEASUREMENT + OWNER]
5. T-G4-05 delivered leakage-vs-count data and regime classification (typ vs max). [MEASUREMENT]
6. T-G4-06 delivered isolation blast-radius data. [MEASUREMENT]
7. Owner records the topology decision (A vs B) with rationale; no topology is locked before this step. [OWNER]
8. Any measured-vs-datasheet conflict is logged in the report (not silenced). [CONSTRAINT]

- After 1-8: G4 status -> EVIDENCE-BACKED / CLOSEABLE. G5 pin-map lock then proceeds (uses corrected counts: SR 3-4 GPIO, Option B leakage 63 uA, scan floors ~64 us/1-ADC or ~32 us/2-ADC). [CALCULATION -> RECOMMENDATION]
- Until 1-6: G5 stays PROVISIONAL; no pin map locked. [CONSTRAINT]

## 7. Open items (no number invented)

- Divider values / resistor ladder values for fixture: owner choice (recorded in register). [OPEN]
- Settling band, continuity threshold, scan-time target, isolation spec: owner requirements. [OPEN]
- Temperature coverage (25 C only vs 85 C soak): owner decision (data budget). [OPEN]
- Number of sample units: owner decision. [OPEN]

## 8. Recommended sequencing

1. Owner approves fixture plan + chooses ladder values / settle band / temperature coverage. [APPROVAL]
2. Execute T-G4-01..06; fill Evidence Register (Section 5). [EXECUTION]
3. Log conflicts; compute decision-rule items 1-6. [ANALYSIS]
4. Owner topology decision (A vs B). [OWNER]
5. G4 -> CLOSEABLE; then G5 pin-map lock batch. [FOLLOW-UP]