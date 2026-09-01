# RX50 G4 MEASUREMENT EXECUTION PROTOCOL

Status: PROTOCOL DRAFT — FOR OWNER APPROVAL (no measurements executed)
Date: 2026-08-15
Batch: G4-MEAS-PROTOCOL-01
Purpose: convert RX50_G4_CLOSURE_EVIDENCE_PLAN.md into an executable hardware test protocol.
Domain: G4 only. G5 pin-map locking, schematic/PCB/BOM, divider values, thresholds, and firing parameters remain OUT OF SCOPE. G1/G2 HOLD. No MAX_CONCURRENT_FIRE=1.

Label legend:
- [FACT]            Manufacturer datasheet / explicit owner requirement.
- [CALCULATION]     Derived directly from verified facts.
- [ASSUMPTION]      Temporary test assumption. NOT a requirement.
- [RECOMMENDATION]  Engineering proposal requiring owner approval.
- [TBD]             Not yet defined.
- Status: LOCKED / EVIDENCE-BACKED / HOLD / TBD / NEEDS RECHECK / OPEN / PROVISIONAL / CLOSEABLE / MEASUREMENT PENDING / CHARACTERIZATION ONLY.

Evidence discipline: every numerical parameter carries provenance. Unverifiable values are written TBD / NEEDS MEASUREMENT / OWNER DECISION. No number is filled from engineering intuition.

---

## 1. Purpose

Provide an executable, evidence-disciplined measurement protocol for G4 (continuity measurement feasibility). Executing this protocol produces the raw data, processed data, and decision records required to close G4 by evidence (per owner direction: close G4 with evidence before locking G5). [RECOMMENDATION]

## 2. Scope

In scope:
- Direct measurement of CD4067 RON at 3.3 V and 5 V (no interpolation).
- CD4067 VIH/VIL behavior at 3.3 V supply.
- STM32F103 ADC accuracy vs source impedance (1 k / 10 k / 50 k ohm regions).
- CD4067/network settling (characterization).
- OFF-channel leakage effect vs channel count (3.3 V / 5 V).
- Cross-channel isolation blast radius.
- Data register, uncertainty handling, conflict handling, closure gate.

Out of scope (HARD):
- G5 pin-map locking; schematic; PCB; BOM; final connector selection.
- Final/resistor design values (fixture values are recorded, not design values).
- Continuity thresholds, settling thresholds, scan-time requirements, isolation requirements.
- Firing voltage/current/pulse/energy/skew; any G1/G2 conclusion.
- CD4067 RON@3.3V inference from 5/10/15 V datasheet points.
- Declaring G4 closed without actual measurement evidence.

## 3. Inputs and source documents

| ARTIFACT | ROLE |
|---|---|
| RX50_G4_G5_CLOSURE_AUDIT.md | Audited facts + corrected bounds (source-of-truth register) |
| RX50_G4_CLOSURE_EVIDENCE_PLAN.md | Closure roadmap + register template + gating rules |
| RX50_G4_G5_HARDWARE_FEASIBILITY_REPORT.md | Candidate topology descriptions (A/B/C), pin candidates |
| RX50_BATCH_ENGINEERING_REPORT.md | G4/G5 feasibility claims, risks |
| RX50_FEASIBILITY_G3_G4_G5_G6_G8.md | Cross-gate feasibility context |
| RX50_G9_FIRMWARE_AND_CROSS_GATE_REPORT.md | Firmware scheduling context (scan-time model) |
| ST DS5319 (Rev 19/20), Table 47/48/49 | RADC 1 kohm; CADC 8 pF; tS 1.5-239.5 cyc; tCONV = tS + 12.5 cyc; RAIN max 50 kohm @ tS=55.5 cyc, fADC=14 MHz; +-2 LSB ET guarantee at RAIN < 10 kohm; VREF+ tied VDDA (LQFP48); VOH min = VDD - 0.4 V |
| TI CD4067B SCHS052D Rev D | RON max 1050/400/240 ohm @5/10/15 V; VIH@5V 3.5 V; OFF leakage +-100 nA (25 C) / +-1000 nA (85-125 C) @18 V; typ +-10 pA @10 V; settling typical curves only; charge injection not specified; recommended VDD-VSS 3-18 V |

## 4. Test philosophy

1. Three-state outcome logic: PASS / FAIL / INCONCLUSIVE. PASS requires an owner requirement that the measurement satisfies; FAIL requires an owner requirement the measurement violates; INCONCLUSIVE covers absent requirement, excessive uncertainty, or insufficient evidence. "Looks good" is never PASS; "no requirement" is never FAIL. [CONSTRAINT]
2. Measurements record, not correct. Discrepancies vs datasheet produce a DATASHEET CONFLICT RECORD; the measurement is never "corrected". [CONSTRAINT]
3. Every value recorded with provenance (instrument, conditions, operator, date). [CONSTRAINT]
4. Characterization data is labeled CHARACTERIZATION ONLY where no owner requirement exists. [CONSTRAINT]
5. No threshold, target, or requirement is invented; each is TBD / OWNER DECISION until owned. [CONSTRAINT]

## 5. DUT definition

- DUT-A: CD4067B (one or more sample units; sample count = owner decision). Each unit tagged with a DUT_ID. [RECOMMENDATION]
- DUT-B: STM32F103C8T6-based board exposing at least one ADC pin (e.g., PA0) and GPIO for address/INH control. Board identity recorded (board rev / identifier). [ASSUMPTION]
- Sample classification: single DUT = characterization evidence; multiple DUTs = sample characterization. Classification stated in the evidence package. [CONSTRAINT]

## 6. Instrumentation requirements

Capability requirements (not specific part numbers; actual IDs + calibration status recorded):

| INSTRUMENT | REQUIRED CAPABILITY | NOTES |
|---|---|---|
| DC source / bench PSU | controllable VDD 3.3 V and 5 V; metered voltage/current | stable during measurement; source contact resistance recorded |
| DMM | 4.5+ digit; DCV + low-resistance / current measurement | 4-wire (Kelvin) preferred for RON; calibration status recorded |
| Oscilloscope | adequate bandwidth (>=100 MHz class) and single-shot capture for settling | probe type recorded (e.g., 10x passive); waveform files referenced |
| Calibrated resistor set | values selected and recorded per test (OWNER TEST VALUE - TBD) | not design values |
| Temperature control | ambient recorded; optional soak at owner-approved temperature | owner decision |
| Address/control driver | STM32 GPIO or controlled function generator for A/B/C/D and INH | slew/levels recorded for T-G4-02 |

Instrumentation availability = owner decision (section 22). UNCERTAINTY = NOT ESTABLISHED until instrument spec sheets + fixture contribution are recorded (section 17).

## 7. Fixture topology (conceptual)

- CD4067B DUT with address inputs (A/B/C/D) and INH controllable from the STM32 (or bench generator).
- STM32F103C8T6 ADC observation path on one pin (e.g., PA0) reading the CD4067 common (X) or channel (Y) node per test.
- Known test termination (calibrated resistors, values selected + recorded; OWNER TEST VALUE - TBD) between the source and the DUT channel input.
- Instrument connections: Kelvin/4-wire to the DUT channel terminals for RON; scope probe on the ADC node for settling.
- Controllable supply: VDD = 3.3 V / 5 V; VDDA = 3.3 V for the STM32.

No schematic, PCB, final resistor values, or connector selection is produced in this protocol. [CONSTRAINT]

## 8. Test safety / handling constraints

- ESD handling: CD4067B and STM32 are CMOS; use wrist strap / grounded mat; DUT ID and handling noted. [ASSUMPTION]
- Power sequencing: connect fixture power rails and verify before energizing DUT; do not apply address/input signals while supply off. [ASSUMPTION]
- ADC input protection: do not exceed VREF+/VDDA range on the ADC pin during fault/short tests (T-G4-06); current limited by fixture (values recorded). [CONSTRAINT]
- Thermal: record ambient for every trial; if 85 C soak is approved, allow stabilization time (owner decision) before reading. [TBD]
- Operator notes: one operator per session, recorded; any anomaly logged immediately. [CONSTRAINT]

---

## 9. T-G4-01 — CD4067 RON @ 3.3 V / 5 V

Objective: directly measure CD4067 channel ON resistance at 3.3 V and 5 V. RON@3.3 V is NOT interpolated. [CONSTRAINT]

Conditions:
- Supply: VDD = 3.3 V and VDD = 5 V. [FACT (needed to feed topology)]
- Temperature: owner-approved coverage (e.g., ambient; optional 85 C soak). [TBD]
- Channels: all 16 (0..15). [CONSTRAINT]

Method (4-wire/Kelvin preferred):
- Force a known test current through the selected channel; measure the voltage across the switch (V_SW) with the DMM in 4-wire mode. [ASSUMPTION on method]
- ITEST: OWNER TEST VALUE - TBD (not specified numerically here; must not be chosen arbitrarily). If a value is proposed, it requires source evidence or owner approval. [TBD / OWNER DECISION]
- Minimize: lead resistance and contact resistance (Kelvin), fixture resistance (4-wire, low-loss routing), instrument burden (voltage measured with high-input-impedance mode), thermal drift (record temperature; short measurement window). [RECOMMENDATION]
- RON = V_SW / ITEST. [CALCULATION]

Record per trial: DUT_ID, channel, VDD, temperature, ITEST, V_SW, RON, instrument, instrument calibration status, trial number. [CONSTRAINT]

Output: per-channel table; min / max / mean / spread per supply and temperature. Result is characterization evidence, NOT "production guaranteed". [CONSTRAINT]

Decision rule:
- Feed measured worst-case RON into RTH + RON + RTRACE < 10 kohm, where the 10 kohm condition is the verified STM32 +-2 LSB guarantee (RAIN < 10 kohm, DS5319). [FACT -> CALCULATION]
- No additional margin is invented. If the owner requires an engineering margin, that margin is an OWNER DECISION and is recorded as such. [CONSTRAINT]

## 10. T-G4-02 — CD4067 VIH/VIL @ 3.3 V

Objective: determine actual control-input behavior at VDD = 3.3 V. Datasheet VIH/VIL@3.3 V is NOT assumed. [CONSTRAINT]

Conditions: VDD = 3.3 V; temperature recorded. [FACT]
Method:
- Sweep the control input voltage (A/B/C/D, and INH) while observing the switch state; record the switching transition; record hysteresis if observable. [ASSUMPTION]
- Test each relevant control input, or explicitly justify a sampling strategy (e.g., symmetric construction -> representative subset, justification recorded). [CONSTRAINT]

Record: VDD, temperature, input voltage, resulting switch state, channel/address condition, instrument, trial. [CONSTRAINT]

Comparison:
- STM32 GPIO guaranteed levels: VOH(min) = VDD - 0.4 V = 2.9 V at VDD=3.3 V; VOL(max) as per DS5319. [FACT]
- Required VIH margin is NOT invented; only measured margin vs 2.9 V is reported. [CONSTRAINT]

Decision classes:
- PASS: an owner-approved control-margin requirement exists and is met.
- FAIL: an owner-approved requirement exists and is violated.
- INCONCLUSIVE: no owner threshold exists -> report measured margin but do NOT declare architectural PASS. [CONSTRAINT]

## 11. T-G4-03 — STM32 ADC accuracy vs source impedance (RAIN)

Use verified DS5319 evidence:
- RADC = 1 kohm; CADC = 8 pF. [FACT]
- RAIN max characterization: 50 kohm at tS = 55.5 cycles, fADC = 14 MHz. This is a sampling-feasibility value, NOT an accuracy guarantee. [FACT]
- +-2 LSB maximum ET guaranteed only for RAIN < 10 kohm. [FACT]

Test source impedance points (approximately):
- ~1 kohm
- ~10 kohm
- ~50 kohm

Exact fixture resistor values are OWNER TEST VALUE - TBD; they are selected, calibrated, and RECORDED (not invented). [CONSTRAINT]

Procedure per condition:
- Apply a known voltage; record ADC raw code; calculate ideal code; calculate error in LSB; repeat sufficient trials (trial count recorded); record ADC configuration (ADC clock, sampling time, VDDA), temperature, resistor value, instrument. [ASSUMPTION on method]
- At the 50 kohm point, configure tS = 55.5 cycles / fADC = 14 MHz (the condition at which DS5319 Table 48 characterizes RAIN max = 50 kohm). [FACT -> test condition]
- At 1 k and 10 k points, record the configured tS (within the 1.5-239.5 cycle range); tS is a recorded test parameter. [ASSUMPTION]

Classify into regions:
- A. Datasheet-guaranteed region: RAIN < 10 kohm (expect +-2 LSB max ET).
- B. Characterization region: 10 kohm <= RAIN <= 50 kohm (accuracy documented, not guaranteed).
- C. Exploratory region: beyond 50 kohm or conditions outside Table 48 (documented only). [CONSTRAINT]

The test must NOT claim that measured performance extends the manufacturer's guarantee. [CONSTRAINT]

## 12. T-G4-04 — CD4067/network settling

Objective: measure actual settling after address transition, INH transition (if used), and channel-to-channel transition. Monitor the ADC node with the oscilloscope. [ASSUMPTION]

Record: old channel, new channel, initial voltage, final voltage, transient peak, settling waveform (file reference), measured settling time, scope bandwidth/settings, probe type, VDD, temperature. [CONSTRAINT]

CRITICAL: do NOT invent a +/-mV threshold, number of bits, settling percentage, or scan-time target. [CONSTRAINT]
- If owner threshold absent: settling result = CHARACTERIZATION ONLY. [CONSTRAINT]
- Separately state: "usable settling time cannot be converted into a PASS/FAIL scan-time requirement until owner scan-time and settling criteria exist." [RECOMMENDATION]
- Propagation delay is NOT used as settling time. [CONSTRAINT]

## 13. T-G4-05 — OFF-channel leakage

Use verified CD4067 evidence:
- OFF leakage: +-100 nA max at 25 C; +-1000 nA max at 85/125 C; specified at the datasheet's 18 V condition. [FACT]
- These are NOT guaranteed 3.3 V/5 V values. Transfer of the 18 V specification to 3.3 V/5 V is an ASSUMPTION (conservative bound). [ASSUMPTION]

Method:
- Measure actual node error at 3.3 V and 5 V at the owner-approved temperatures; sweep OFF-channel count (N_OFF). [ASSUMPTION]
- Record: N_OFF, node voltage, reference voltage, delta voltage, calculated equivalent current if the test topology permits (state the basis), channel, VDD, temperature. [CONSTRAINT]

Population distinction:
- Option A: maximum local OFF-channel population (per-MUX node, up to 15 OFF). [CALCULATION]
- Option B: shared-node OFF-channel population (up to 63 OFF). [CALCULATION]

Theoretical bounds (dataset test condition only):
- 15 channels -> 15 uA based on the 1 uA/channel upper bound. [CALCULATION]
- 63 channels -> 63 uA based on the 1 uA/channel upper bound. [CALCULATION]
These are THEORETICAL BOUNDS AT THE DATASHEET TEST CONDITION (18 V), NOT measured 3.3 V/5 V predictions. [CONSTRAINT]

- Do NOT claim leakage scales linearly with supply unless measured/evidenced. [CONSTRAINT]
- Outcome: regime classification (typical ~pA vs datasheet max ~100/1000 nA) and comparison vs the corrected theoretical bounds; threshold = owner (none invented). [STATUS]

## 14. T-G4-06 — Cross-channel isolation

Objective: determine fault/readout blast radius. [ASSUMPTION]

Method:
- Select one channel; force/short/terminate it per the approved fixture condition; read other channels; repeat across channel positions. [ASSUMPTION]

Separate populations:
- A. Same-MUX channels.
- B. Different-MUX groups.
- C. Shared-node topology where applicable. [CONSTRAINT]

Record: source channel, victim channel, expected state, measured state, delta, VDD, temperature, channel count, fixture condition. [CONSTRAINT]

- Do NOT invent an isolation dB / voltage / percentage / resistance requirement. [CONSTRAINT]
- If no owner isolation criterion: classification = CHARACTERIZATION ONLY. [CONSTRAINT]

---

## 15. Raw-data recording format

Structured tables; minimum fields:

| TEST_ID | DUT_ID | TRIAL | VDD | TEMP | CHANNEL | CONDITION | INPUT | OUTPUT | VALUE | UNIT | INSTRUMENT | INSTRUMENT_ID | CALIBRATION_STATUS | OPERATOR | DATE | TIME | REMARK |

T-G4-04 additions: WAVEFORM_FILE (reference to oscilloscope capture). [CONSTRAINT]
T-G4-03 additions:

| ADC_ID | ADC_CLOCK | SAMPLE_TIME | VDDA | EXPECTED_CODE | MEASURED_CODE | ERROR_LSB | RESISTOR_VALUE |

- Each row requires all applicable fields; blank mandatory fields mark the trial INVALID. [CONSTRAINT]
- The filled register lives in a dedicated evidence file (see section 20). [RECOMMENDATION]

## 16. Calculation rules

- RON = V_SW / ITEST (4-wire). [CALCULATION]
- ADC error (LSB) = |MEASURED_CODE - EXPECTED_CODE|; EXPECTED_CODE derived from applied voltage / full scale (full scale = VDDA, VREF+ internally tied VDDA on LQFP48). [FACT -> CALCULATION]
- Node leakage current estimate (T-G4-05): I_eff = delta_V / Z_effective, only if Z_effective is measured/known and stated; otherwise equivalent current = NOT ESTABLISHED. [CALCULATION / CONSTRAINT]
- Derived min/max/mean/spread are simple statistics of recorded values. [CALCULATION]
- No result is extrapolated outside measured conditions. [CONSTRAINT]

## 17. Measurement uncertainty / error handling

- Do NOT fabricate uncertainty numbers. [CONSTRAINT]
- Record: instrument specified accuracy, resolution, repeatability, fixture contribution (if known), environmental condition (temperature, humidity if relevant). [CONSTRAINT]
- If uncertainty cannot be quantified: UNCERTAINTY = NOT ESTABLISHED. [CONSTRAINT]
- Instrument resolution is NOT converted into total measurement uncertainty. [CONSTRAINT]
- Repeatability is assessed by multiple trials (trial count recorded); spread reported with the trials. [RECOMMENDATION]

## 18. Datasheet conflict handling

If a measured result differs from the datasheet, the measurement is NOT "corrected". Create a DATASHEET CONFLICT RECORD: [CONSTRAINT]

| DUT | PARAMETER | DATASHEET VALUE | DATASHEET REVISION | TABLE | MEASUREMENT | TEST CONDITION | POSSIBLE EXPLANATION | REPEAT STATUS | DISPOSITION |

Dispositions: REPEAT / ACCEPT MEASUREMENT / INVESTIGATE FIXTURE / CONTACT VENDOR / UNRESOLVED. [CONSTRAINT]
- Conflicts are logged into the evidence package and reported; they are never silenced. [CONSTRAINT]

## 19. PASS / FAIL / INCONCLUSIVE rules

Three-state logic is mandatory. [CONSTRAINT]
- PASS: owner requirement exists and the measurement satisfies it.
- FAIL: owner requirement exists and the measurement violates it.
- INCONCLUSIVE: measurement exists but requirement is absent, test uncertainty is excessive, or evidence is insufficient.
- Never convert "looks good" into PASS; never convert "no requirement" into FAIL. [CONSTRAINT]
- Each T-G4-xx result carries one of these three states (or CHARACTERIZATION ONLY where the state logic does not apply because no requirement exists). [CONSTRAINT]

## 20. Evidence package requirements

Minimum package before G4 can close:
1. Raw measurement data (register tables).
2. Processed data (min/max/mean/spread; error LSB; settling times).
3. Instrument information (IDs, calibration status, spec sheets referenced).
4. DUT identification (DUT_ID, revision, photos/fixture identification if available).
5. Test conditions (VDD, temperature, per trial).
6. Photographs or fixture identification if available.
7. Oscilloscope captures for T-G4-04 (waveform file references).
8. Datasheet references (DS5319, SCHS052D with revision + table).
9. Calculation sheet (methods from section 16).
10. Anomaly / conflict register (section 18).
11. Owner decisions (section 22).
12. Final G4 closure statement (section 21). [RECOMMENDATION]

## 21. G4 closure gate

The closure statement is filled only after the evidence package exists; "G4 CLOSED" is NOT pre-written. [CONSTRAINT]

Template:

```
G4 STATUS: OPEN / MEASUREMENT PENDING / EVIDENCE-BACKED / CLOSEABLE

T-G4-01: STATUS = ...  (measured RON@3.3V/5V present: YES/NO)
T-G4-02: STATUS = ...
T-G4-03: STATUS = ...
T-G4-04: STATUS = ...
T-G4-05: STATUS = ...
T-G4-06: STATUS = ...

TOPOLOGY: A / B / UNDECIDED

OPEN REQUIREMENTS: ...

DATASHEET CONFLICTS: ...

OWNER APPROVAL: ...

FINAL CLOSURE: ...
```

Gating rule (from RX50_G4_CLOSURE_EVIDENCE_PLAN.md Section 6): G4 -> EVIDENCE-BACKED / CLOSEABLE when all six measurements are present with provenance AND the owner records the topology decision (A vs B) with rationale. G5 pin-map locking is downstream and NOT performed in this batch. [RECOMMENDATION]

## 22. Open owner decisions (must be answered before physical measurement)

1. Fixture / ladders: resistor values (OWNER TEST VALUE - TBD), fixture implementation approach, DUT channel termination. [OWNER DECISION]
2. Settling criterion: +/-mV or bits band for T-G4-04 (else CHARACTERIZATION ONLY). [OWNER DECISION]
3. Continuity requirement: pass/fail threshold for continuity readings (if one exists). [OWNER DECISION]
4. Isolation requirement: isolation spec for T-G4-06 (else CHARACTERIZATION ONLY). [OWNER DECISION]
5. Temperature coverage: ambient only, or approved soak (e.g., 85 C), with stabilization time. [OWNER DECISION]
6. DUT sample count: single unit (characterization) vs multiple units (sample characterization). [OWNER DECISION]
7. Instrumentation availability: which instruments / calibration status are available for execution. [OWNER DECISION]

G5 decisions are NOT requested here. G5 remains downstream. [CONSTRAINT]

## 23. Test execution checklist

Pre-execution:
- [ ] Owner decisions (section 22) recorded.
- [ ] Fixture built at topology level; ladder values selected + recorded.
- [ ] Instruments verified; calibration status recorded.
- [ ] DUT(s) tagged with DUT_ID.
- [ ] Data register template prepared (section 15).
- [ ] Temperature coverage agreed.

Per-test:
- [ ] T-G4-01: 16 channels x 3.3 V x 5 V (x temperature), 4-wire, ITEST recorded, min/max/mean/spread computed.
- [ ] T-G4-02: control-input sweep at 3.3 V; margin vs 2.9 V reported; hysteresis if observable.
- [ ] T-G4-03: points ~1 k / 10 k / 50 k; tS and ADC clock recorded; regions A/B/C separated; error LSB per condition.
- [ ] T-G4-04: settling waveforms captured; waveform files referenced; characterization only if no threshold.
- [ ] T-G4-05: N_OFF sweep at 3.3 V / 5 V; bounds 15 uA / 63 uA labeled theoretical (18 V condition); regime classification.
- [ ] T-G4-06: same-MUX / cross-MUX / shared-node blast radius recorded; characterization only if no criterion.
- [ ] Every trial row filled; anomalies logged.

Post-execution:
- [ ] Uncertainty assessment recorded (NOT ESTABLISHED where not quantified).
- [ ] Datasheet conflict records created if applicable.
- [ ] Evidence package assembled (section 20, 12 items).
- [ ] G4 closure statement filled (section 21); NOT pre-declared closed.
- [ ] Critical audit checks (below) all answered NO.
- [ ] G5 pin-map lock NOT performed.

### Critical audit checks (before finalizing)

1. Did you interpolate CD4067 RON@3.3V? -> NO
2. Did you invent a continuity threshold? -> NO
3. Did you invent a settling threshold? -> NO
4. Did you invent a scan-time requirement? -> NO
5. Did you treat the 18 V leakage spec as a 3.3 V/5 V guaranteed value? -> NO (labeled ASSUMPTION)
6. Did you call 50 kohm an accuracy guarantee? -> NO (sampling-feasibility value only)
7. Did you forget that tCONV already includes tS? -> NO
8. Did you claim four simultaneous ADC conversions? -> NO
9. Did you claim USART1 can reach 10 Mbps? -> NO
10. Did you count 74HC595 OE as MCU GPIO? -> NO
11. Did you classify any assumption as fact? -> NO
12. Did you lock G5? -> NO
13. Did you touch G1/G2? -> NO
14. Did you introduce firing numbers? -> NO
15. Did you invent measurement uncertainty? -> NO

---

## OWNER APPROVAL BLOCK

Unresolved decisions that MUST be answered before physical measurement starts (G4 only; no G5 decisions requested):

1. **Fixture / ladders** — owner test values for test resistors and fixture approach.
2. **Settling criterion** — +/-mV or bits band for T-G4-04, or accept CHARACTERIZATION ONLY.
3. **Continuity requirement** — pass/fail threshold if one exists.
4. **Isolation requirement** — isolation spec for T-G4-06, or accept CHARACTERIZATION ONLY.
5. **Temperature coverage** — ambient only vs approved soak + stabilization time.
6. **DUT sample count** — single vs multiple CD4067 units.
7. **Instrumentation availability** — instruments + calibration status for execution.