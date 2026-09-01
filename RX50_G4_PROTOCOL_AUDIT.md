# RX50 G4 PROTOCOL AUDIT

Status: COMPLETE (Part A + Part K of batch G4-MEAS-BATCH-01)
Date: 2026-08-15
Audited artifact: RX50_G4_MEASUREMENT_EXECUTION_PROTOCOL.md (all 23 sections)
Method: adversarial review against DS5319 Rev 19/20, SCHS052D Rev D, and the other G4 documents.
Discipline: findings are documented, NOT silently repaired. Corrected statements are captured here and reflected in the companion batch artifacts (TEST_MATRIX, CALCULATION_RULES, RAW_DATA_TEMPLATES, EXECUTION_SEQUENCE). The protocol itself is a batch input and is NOT rewritten; corrections are proposed for a protocol rev on owner approval.

Severity tally: CRITICAL = 0 | HIGH = 0 | MEDIUM = 6 | LOW = 4

---

## Part A — Findings

| ID | SEVERITY | SECTION | CURRENT STATEMENT | PROBLEM | CORRECTED STATEMENT | EVIDENCE BASIS | ACTION |
|---|---|---|---|---|---|---|---|
| A-01 | MEDIUM | 9 (T-G4-01) | "ITEST: OWNER TEST VALUE - TBD ... must not be chosen arbitrarily" | No constraint set linking ITEST to DUT current ratings / self-heating / V_SW magnitude. An arbitrary ITEST can measure RON outside datasheet test conditions or overload the switch. | ITEST must (a) be within the DUT Absolute Maximum Ratings for switch/input current (value from datasheet — NEEDS RECHECK), (b) keep V_SW small so the 4-wire reading reflects RON only, (c) limit self-heating (short measurement window). Value remains OWNER TEST VALUE - TBD, recorded per trial. | SCHS052D (absolute max table — verify row during PDF check); 4-wire method physics [CALCULATION] | Record in execution sequence; owner decision Group 1 |
| A-02 | MEDIUM | 11 (T-G4-03) | "verify +-2 LSB max ET at RAIN < 10k" (evidence-plan rule carried) | +-2 LSB max total error is a range-wide accuracy statement. A single applied-voltage point cannot substantiate it; any "verified +-2 LSB" claim from one point overstates the evidence. | Test multiple input-voltage points across the ADC range (e.g., low/mid/near-full-scale; exact points = OWNER TEST VALUE - TBD). Report error LSB per point. Claim is limited to "error <=2 LSB at the measured points", never "full range guarantee re-verified". | DS5319 Table 49 accuracy definition; ADC transfer function [FACT] | Applied in TEST_MATRIX (multi-point), CALCULATION_RULES |
| A-03 | MEDIUM | 11 (T-G4-03) | "record ADC configuration (ADC clock, sampling time, VDDA)" | Recording is required but not controlled: RAIN is only an isolated variable if all other ADC settings are FIXED across the three impedance points. | Fix ADC clock = 14 MHz and VDDA across all points; keep all ADC registers constant; tS fixed except the datasheet-specified tS=55.5 cyc for the ~50k point (Table 48). RAIN then varies alone. | DS5319 Table 47/48; controlled-experiment principle [FACT/CALCULATION] | Applied in TEST_MATRIX CONTROLLED VARIABLES |
| A-04 | MEDIUM | 12 (T-G4-04) | "probe type recorded" | Scope probe input capacitance (pF class) loads the CD4067 node and changes the settling RC; the measured waveform includes probe loading. Recording the probe alone does not bound this. | Record probe input-capacitance spec; state probe loading as a fixture contribution in uncertainty; prefer low-C (e.g., 10x passive with listed C_in) and report whether node settling excludes probe loading. | Measurement circuit loading physics [ASSUMPTION/CALCULATION] | Applied in EXECUTION_SEQUENCE, RAW_DATA_TEMPLATES (probe fields) |
| A-05 | MEDIUM | 13 (T-G4-05) | "regime classification (typical ~pA vs datasheet max ~100/1000 nA)" | Typical ~pA cannot be observed with a DMM-class measurement; the measurable floor is the instrument/measurement resolution. Claiming to classify the pA regime overstates verifiability. | State the measurement floor (instrument sensitivity + fixture). Classify only above the floor. Values below floor = "below measurement floor", NOT "typical". | Instrument sensitivity; measurement physics [ASSUMPTION] | Applied in TEST_MATRIX, CALCULATION_RULES |
| A-06 | MEDIUM | 10 (T-G4-02) | "observe the switch state" | "Switch state" needs a defined load/termination to be observable as an output voltage; otherwise the observation is undefined. | Terminate the observed channel output into a defined, recorded load (e.g., high-impedance scope/DMM input or a known resistor) and report output voltage vs a recorded reference. | Test method completeness [ASSUMPTION] | Applied in TEST_MATRIX, RAW_DATA_TEMPLATES |
| A-07 | LOW | 8 (safety) | "current limited by fixture (values recorded)" | The statement is passive; a mandatory current-limit element for the T-G4-06 fault-injection test is not explicit. | Make the current-limit element MANDATORY for all force/short tests; limit value = OWNER TEST VALUE - TBD and recorded; ADC pin protection per DS5319 absolute ratings. | DS5319 absolute max ratings (ADC pin); fault-injection safety [FACT/ASSUMPTION] | Applied in EXECUTION_SEQUENCE |
| A-08 | LOW | 9 (T-G4-01) | supply runs 3.3 V / 5 V | No stabilization/soak specified between supply transitions or re-check of the calibration reference after each transition. | Between supply changes: allow stabilization (owner-approved soak), re-verify the reference/calibration point, then read. | Test practice [ASSUMPTION] | Applied in EXECUTION_SEQUENCE |
| A-09 | LOW | 16 (calc rules) | "EXPECTED_CODE derived from applied voltage / full scale" | If the applied voltage is taken from its nominal setting instead of the instrument-measured value, a systematic offset enters ERROR_LSB. | Use the instrument-measured applied voltage at the pin for EXPECTED_CODE; record it. | Measurement accuracy practice [ASSUMPTION] | Applied in CALCULATION_RULES |
| A-10 | LOW | 11 (T-G4-03) | "~50 kohm" point | A nominal 50k fixture resistor can exceed 50k with tolerance and slip into the Table 48 NA domain (tS>55.5); the nominal value is not the test condition. | The RECORDED measured resistor value governs region classification, not the nominal value; if measured >50k, classify by the measured value and note the domain boundary. | DS5319 Table 48 [FACT] | Applied in CALCULATION_RULES, TEST_MATRIX |

## Part A8 — cross-document contradiction check

- Closure audit (Section 18) vs protocol (Section 13): leakage bounds 15 uA / 63 uA are consistent (theoretical bounds at 18 V datasheet condition, corrected from the old ~50 uA). CONFIRMED CONSISTENT.
- Evidence plan (Section 6) vs protocol (Section 21): closure gate items align; protocol adds provenance to the gate. CONSISTENT.
- G4/G5 hardware report (Section 12) T-G4-03 criterion vs protocol: report says "verify +-2 LSB at RAIN<10k"; protocol narrows the claim to measured points (A-02). RESOLVED by A-02.
- No other contradictions found. [STATUS]

## Part A9 — verifiability audit

- T-G4-01 min/max/mean/spread: verifiable. [OK]
- T-G4-02 measured margin vs 2.9 V: verifiable. [OK]
- T-G4-03 error LSB per point: verifiable, multi-point required (A-02). [OK after A-02]
- T-G4-04 settling time: verifiable as measured waveform (characterization only). [OK]
- T-G4-05 "typical ~pA" regime: NOT verifiable with DMM-class floor (A-05). [CORRECTED]
- T-G4-06 blast radius: verifiable. [OK]

## Part A10 — requirement-introduction audit

- No continuity/settling/isolation/scan-time threshold is introduced by the protocol. All are TBD / OWNER DECISION. [OK]
- The 10 kohm source-impedance constraint in Section 9 is derived from the DS5319 +-2 LSB guarantee (a design constraint, not a new requirement). [OK — correctly labeled]

---

## Part K — Critical error hunt (final adversarial audit)

Pattern search across the full G4 package (protocol + this batch's artifacts):

1. Interpolated RON@3.3V: NOT FOUND — NO
2. Typical treated as guaranteed: NOT FOUND — NO
3. 18 V leakage treated as 3.3 V/5 V guarantee: NOT FOUND — NO (labeled ASSUMPTION)
4. 50 kohm RAIN treated as accuracy guarantee: NOT FOUND — NO
5. ADC conversion time double-counting: NOT FOUND — NO
6. Invented settling threshold: NOT FOUND — NO
7. Invented continuity threshold: NOT FOUND — NO
8. Invented isolation threshold: NOT FOUND — NO
9. Invented scan-time target: NOT FOUND — NO
10. Invented uncertainty: NOT FOUND — NO (NOT ESTABLISHED used)
11. Invented resistor values: NOT FOUND — NO (OWNER TEST VALUE - TBD)
12. Invented firing values: NOT FOUND — NO
13. Claiming measurement without measurement: NOT FOUND — NO (MEASUREMENT PENDING everywhere)
14. Single DUT treated as production guarantee: NOT FOUND — NO (labeled characterization)
15. G5 locked: NOT FOUND — NO
16. Accidental G1/G2 conclusion: NOT FOUND — NO
17. Incorrect GPIO accounting: NOT FOUND — NO (SR = 3-4 GPIO; OE interlock-owned)
18. Incorrect ADC topology interpretation: NOT FOUND — NO (2 ADCs; no 4-way parallel claim)
19. Incorrect CD4067 channel population/leakage calc: NOT FOUND — NO (15 / 63 bounds correct)
20. Statement not traceable to evidence: NOT FOUND for numbers; all TBD items traceable to "not yet owned". — NO

AUDIT RESULT: CRITICAL = 0 | HIGH = 0 | MEDIUM = 6 | LOW = 4
Corrections: A-01..A-06 (MEDIUM) and A-07..A-10 (LOW) are documented above; corrected statements are applied in the companion batch artifacts (TEST_MATRIX, CALCULATION_RULES, RAW_DATA_TEMPLATES, EXECUTION_SEQUENCE). No CRITICAL/HIGH findings exist; therefore no CRITICAL/HIGH correction block is required. [STATUS: CLEAN WITH DOCUMENTED CORRECTIONS]