# RX50 G4 MEASUREMENT START PACK

Status: COMPLETE (batch G4-MEAS-START-01)
Date: 2026-08-15
Purpose: convert the completed G4 package into the MINIMUM practical information to physically execute T-G4-01..06. No re-design, no broad audit, no invented measurements/values/requirements. G5 NOT locked.

---

## TASK 1 — Minimum owner input (classification)

| # | DECISION (from Owner Decision Sheet) | CLASSIFICATION | ONE-LINE REASON |
|---|---|---|---|
| 1.1 | Fixture approach (F1/F2/F3 topology-level build) | MANDATORY BEFORE FIRST MEASUREMENT | physical build gate; no test runs without a fixture |
| 1.2 | Test resistor values | MANDATORY ONLY FOR SPECIFIC TEST | needed only for T-G4-03 ladder, T-G4-05 node termination, T-G4-06 current limit; NOT for T-G4-01/02; default = operator-selected + recorded (characterization) |
| 1.3 | ITEST (T-G4-01) | MANDATORY ONLY FOR SPECIFIC TEST | only T-G4-01; default = operator-selected within DUT absolute-max bounds + recorded |
| 1.4 | Temperature coverage | CAN BE DEFERRED | ambient-only (recorded) is an accepted characterization condition; soak optional later |
| 1.5 | DUT sample count | CAN BE DEFERRED | start with single DUT = characterization; multiple units addable later |
| 1.6 | Available instruments (IDs + calibration status) | MANDATORY BEFORE FIRST MEASUREMENT | provenance is a hard constraint; cannot log without identifying instruments |
| 2.1-2.4 | Settling / isolation / continuity thresholds, margin | CAN BE CHARACTERIZATION-ONLY | execution explicitly allowed without them |

## TASK 2 — Fixture values (test vs design)

| VALUE | TEST / DESIGN | EVIDENCE JUSTIFICATION | STATUS |
|---|---|---|---|
| Ladder ~1k / 10k / 50k (T-G4-03) | TEST | nominal points justified: 10k = DS5319 +-2 LSB guarantee boundary; 50k = DS5319 Table 48 RAIN max @ tS=55.5 cyc; 1k = low-impedance reference | exact units = OWNER TEST VALUE REQUIRED (select, measure, record); not a design value |
| Node termination Z_effective (T-G4-05) | TEST | needed to compute I_effective = delta_V/Z; else I_EFFECTIVE = NOT ESTABLISHED | OWNER TEST VALUE REQUIRED (or operator-selected, measured, recorded) |
| Switch-state observation load (T-G4-02) | TEST | output must be terminated to be observable as a state | OWNER TEST VALUE REQUIRED (high-Z or known R; operator-selected + recorded) |
| Fault-injection current-limit element (T-G4-06) | TEST (protection) | bounded by DUT/ADC absolute-max ratings (DS5319/SCHS052D rows NEEDS RECHECK) | OWNER TEST VALUE REQUIRED (or operator-selected within bounds, recorded) |
| ITEST (T-G4-01) | TEST | bounded by DUT absolute-max ratings (NEEDS RECHECK); value is a recorded test condition | OWNER TEST VALUE REQUIRED / operator-selected + recorded |
| Calibration reference resistor (DMM verify) | TEST | known-value unit for pre/post reference checks | operator-selected, recorded |
| Divider values (Rth) | DESIGN | OUT OF SCOPE for G4; no design value invented here | NOT REQUIRED FOR G4 TESTS |

## TASK 3 — Test start order

| TEST | CAN START NOW? | BLOCKER | REQUIRED INPUT | DEPENDENCY |
|---|---|---|---|---|
| T-G4-01 RON | NO (until owner 1.1+1.6) | F1 build; DMM+cal; ITEST selection | fixture approval; instruments; ITEST (operator-selected ok) | none (first) |
| T-G4-02 VIH/VIL | after T-G4-01 | same F1 | same + switch-state load choice | F1; T-G4-01 |
| T-G4-03 ADC vs RAIN | after F2 + ladder | ladder values | resistor values (owner or operator-selected+recorded) | F2; ladder |
| T-G4-05 leakage | after F3 + node termination | node termination value | Z_effective (owner or operator) | F3 |
| T-G4-04 settling | after T-G4-05 | scope + low-C probe | none (captures) | F3; scope |
| T-G4-06 isolation | after T-G4-04/05 | current-limit value | current-limit element (owner or operator) | F3 |

Optimization: owner does NOT wait for optional settling/isolation/continuity thresholds (Group 2 defaults = characterization-only). First physically runnable pair = T-G4-01 + T-G4-02 on F1 once owner items 1.1 + 1.6 are answered and ITEST is selected (owner or operator).

## TASK 4 — Minimum start package

| ITEM | VALUE / STATUS | SOURCE | REQUIRED BEFORE START? | OWNER ACTION |
|---|---|---|---|---|
| DUT identity | DUT_ID tags (CD4067B units) + F2 board revision | protocol §5 | YES | assign + record |
| Sample count | default 1 (characterization) | decision sheet 1.5 | NO (defer) | approve or defer |
| Fixture approach | F1/F2/F3 topology-level build | decision sheet 1.1 | YES | approve build |
| Test resistor values | OWNER TEST VALUE — select, measure, record | decision sheet 1.2 / test matrix | YES for T-G4-03/05/06 (not 01/02) | supply or authorize operator selection |
| PSU requirements | 3.3 V and 5 V set-points, metered, verified with DMM | protocol §6 | YES | confirm availability |
| DMM requirements | 4.5+ digit, 4-wire (Kelvin), cal status logged | protocol §6 | YES | confirm + cal log |
| Oscilloscope requirements | >=100 MHz class, low-C probe, C_in recorded (only T-G4-04) | protocol §6 | NO (only for T-G4-04) | confirm |
| Temperature condition | ambient, recorded per trial | decision sheet 1.4 | NO (defer) | confirm/defer |
| Operator | recorded per trial | protocol §5/§15 | YES | assign |
| Data logging method | CSV templates E1-E6 (RX50_G4_RAW_DATA_TEMPLATES.md) | batch artifact | YES (ready) | use as log |
| Calibration status | recorded per instrument (spec + repeatability; else NOT ESTABLISHED) | protocol §6/§17 | YES | confirm/log |

## TASK 5 — Optional items (CAN BE DECIDED LATER)

- Settling acceptance threshold -> CHARACTERIZATION ONLY retained.
- Isolation acceptance threshold -> CHARACTERIZATION ONLY retained.
- Continuity pass/fail threshold -> PASS/FAIL = NOT AVAILABLE, results reported per point.
- Engineering margin on RTH + RON + RTRACE < 10k -> NO margin applied (datasheet 10k as-is).
- Temperature soak (e.g., 85 C) -> deferred; ambient-only start.
- Multiple DUT samples -> deferred; single-DUT characterization start.

## TASK 6 — Final start gate

**READY TO MEASURE** (owner input complete; physical data still MEASUREMENT PENDING until executed).

## Owner approval record (2026-08-15)

| # | DECISION | APPROVED VALUE |
|---|---|---|
| 1.1 | Fixture approach | F1/F2/F3 topology-level build APPROVED |
| 1.4 | Temperature coverage | ambient only |
| 1.5 | DUT sample count | single DUT (characterization) |
| 1.2/1.3/1.6 | Test values + instruments | operator AUTHORIZED to select + record ITEST, ADC ladder, node termination, measurement protection — each recorded as TEST VALUE and VERIFIED before use; no design value or requirement inferred |
| T-G4-06 | Fault-injection current limit | MUST be verified BEFORE T-G4-06 execution |

Group 2 thresholds: none supplied -> characterization-only retained (TASK 5 defaults stand).

---

G4 = READY TO MEASURE
G5 = NOT LOCKED
G1/G2 = HOLD
FIRING = OUT OF SCOPE