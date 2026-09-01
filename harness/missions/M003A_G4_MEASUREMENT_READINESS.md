# M003A G4 MEASUREMENT READINESS

- Mission: M003A — G4 Measurement Readiness & Execution Pack (pre-measurement readiness audit)
- Date: 2026-08-15
- Status: COMPLETE
- Result: FINDINGS ONLY (no measurements fabricated, no closure, no feasibility declared, no topology/G5 locked)

## Executive Status

The repository contains a **complete and internally consistent G4 measurement package** (protocol, protocol audit, fact register, test matrix, execution sequence, raw-data templates E1-E6, calculation rules F1-F7, owner decision sheet, start pack, closure engine). The owner has recorded decisions for every Group-1 item (fixture F1/F2/F3 build APPROVED; temperature = ambient only; DUT = single unit; test values delegated to the operator as recorded TEST VALUEs; Group-2 thresholds declined → characterization-only).

The repository itself declares `G4 = READY TO MEASURE` (operator brief, start pack). **M003A does NOT confirm that as full execution readiness.** Two execution-critical procedural items remain unresolved in the repository:

1. **T-G4-06 fault-injection current limit is not defined/verified/recorded** → per mission rule this is `BLOCKED — CURRENT LIMIT NOT VERIFIED`; T-G4-06 must not be executed until it is.
2. **ITEST selection bound (T-G4-01) is unverified**: the SCHS052D absolute-maximum current row is flagged `NEEDS RECHECK` (EV-45), and no datasheet PDF is resident in the workspace to verify it.

Therefore the overall readiness gate is **NOT READY** (narrowly — the gaps are closable at execution start, not structural). T-G4-02, T-G4-03, T-G4-05 are individually READY; T-G4-01 and T-G4-04 are READY WITH MISSING PROCEDURAL DETAIL; T-G4-06 is NOT READY.

## M002 Blocker Review

| M002 blocker | Repository status | M003A verdict |
|---|---|---|
| Fixture preparation | F1/F2/F3 topology-level build APPROVED (start pack owner record); build steps defined (execution sequence §1) | RESOLVED (documentation); physical build = operator action |
| ITEST definition | Owner authorized operator selection; value not yet chosen/recorded; bound = SCHS052D abs-max row, `NEEDS RECHECK` (EV-45) | OPEN (procedural): value = operator action; bound verification missing |
| Ladder resistor values | Nominal points justified (~1k/10k/50k; start pack TASK 2); exact units operator-selected + measured + recorded | RESOLVED (method); values = operator action |
| Temperature coverage | Owner approved: AMBIENT ONLY, recorded per trial (start pack owner record; decision sheet 1.4) | RESOLVED |
| Measurement provenance | Templates E1-E6 + instrument log define all required fields (protocol §15; run card instrument log) | RESOLVED (defined); fill = operator action |
| Oscilloscope waveform capture | Method + records defined (protocol §12; matrix; E4 template); probe C_in recorded; ≥5 captures/transition | MOSTLY RESOLVED — minor: no waveform file-naming scheme (see T-G4-04) |
| T-G4-06 current-limit verification | Mandatory pre-run (owner record: "MUST be verified BEFORE T-G4-06"); value/log NOT present | OPEN — BLOCKED (execution must not start for T-G4-06) |
| G4 Evidence Retrieval material | Referenced as report input (closure audit E-09); file ABSENT in workspace | OPEN (evidence artifact; OI-16) — not execution-critical |

---

## T-G4-01 Readiness

### TEST PURPOSE
Measure CD4067 RON at VDD = 3.3 V and 5 V, per channel (0..15), per supply; record min/max/mean/spread. No interpolation from the 5/10/15 V datasheet points.

### REQUIRED HARDWARE
CD4067B DUT(s) (DUT_ID tagged), controllable address A/B/C/D + INH (STM32 GPIO or generator), bench supply 3.3 V/5 V, Kelvin/4-wire terminals.

### REQUIRED INSTRUMENTATION
- DMM: 4.5+ digit, DCV + low-resistance/current, 4-wire (Kelvin) preferred (protocol §6). No model invented.
- Bench PSU: controllable VDD 3.3 V and 5 V, metered (protocol §6).

### REQUIRED FIXTURE
Fixture F1 (DUT bench): CD4067B + address/INH control + supply + Kelvin terminals (execution sequence §1). F1 build APPROVED by owner.

### REQUIRED SETUP VALUES
| Value | Status |
|---|---|
| ITEST | operator-selected within DUT absolute-max bounds + recorded (OWNER TEST VALUE; decision sheet 1.3). Bound row `NEEDS RECHECK` (EV-45) |
| VDD 3.3 V / 5 V | already specified |
| Channels 0..15, temp ambient | already specified |
| Temperature coverage | already specified (ambient only) |

### REQUIRED PROVENANCE
TEST_ID, DUT_ID, TRIAL, VDD, TEMP, CHANNEL, ITEST, V_SW, VALUE, UNIT, INSTRUMENT, INSTRUMENT_ID, CAL_STATUS, OPERATOR, DATE, TIME, REMARK (E1 header; protocol §15/§9).

### RAW DATA FORMAT
E1 CSV template (RX50_G4_RAW_DATA_TEMPLATES.md), one row per trial.

### ACCEPTANCE / CLOSURE CRITERIA
`NO OWNER THRESHOLD FOUND` (PASS/FAIL = NOT AVAILABLE). Closure criterion = T-G4-01 evidence exists with provenance (closure engine item 1); feeds Rth + RON + RTRACE < 10 kΩ constraint.

### READINESS STATUS
READY WITH MISSING PROCEDURAL DETAIL — ITEST absolute-max bound (SCHS052D) unverified; otherwise all owner decisions recorded and method defined.

---

## T-G4-02 Readiness

### TEST PURPOSE
Determine CD4067 VIH/VIL at VDD = 3.3 V (not in datasheet); compute margin vs STM32 VOH ≥ 2.9 V / VOL.

### REQUIRED HARDWARE
CD4067B on F1, control-input sweep (A/B/C/D, INH), defined output termination (operator-selected + recorded).

### REQUIRED INSTRUMENTATION
DMM/source for sweep + scope or generator for state observation (protocol §6; matrix). No model invented.

### REQUIRED FIXTURE
Fixture F1 (reuse from T-G4-01; no rewiring except 4-wire sense → control sweep).

### REQUIRED SETUP VALUES
| Value | Status |
|---|---|
| VDD = 3.3 V | already specified |
| Switch-state observation load | operator-selected + recorded (TEST VALUE; A-06 correction) |
| Input slew / levels | recorded |
| Temperature | already specified (ambient) |

### REQUIRED PROVENANCE
VDD, TEMP, input voltage, switch state, output voltage, reference, hysteresis (if observable), channel, instrument, trial (E2 header).

### RAW DATA FORMAT
E2 CSV template.

### ACCEPTANCE / CLOSURE CRITERIA
`NO OWNER THRESHOLD FOUND` (no control-margin requirement → INCONCLUSIVE unless owner requirement exists). Closure criterion = T-G4-02 evidence + margin computed (closure engine item 2).

### READINESS STATUS
READY

---

## T-G4-03 Readiness

### TEST PURPOSE
STM32F103 ADC error vs source impedance (RAIN) at ~1k / ~10k / ~50k; regions A/B/C by RECORDED measured RAIN; multi-point across the ADC range.

### REQUIRED HARDWARE
STM32F103C8T6 board exposing an ADC pin (e.g., PA0) with ADC firmware (fADC = 14 MHz, tS configurable, tS = 55.5 cyc for the ~50k point); calibrated resistor ladder.

### REQUIRED INSTRUMENTATION
Calibrated resistor set; DMM for applied voltage; ADC readout (MCU firmware) (protocol §6).

### REQUIRED FIXTURE
Fixture F2 (ADC path): STM32 board + ADC pin + calibrated ladder + supply + stable reference (execution sequence §1). F2 build APPROVED.

### REQUIRED SETUP VALUES
| Value | Status |
|---|---|
| Ladder ~1k/10k/50k nominal | justified (10k = ±2 LSB boundary; 50k = Table 48 RAIN max; 1k = low-Z reference); exact units = operator-selected, measured, recorded |
| ADC clock | already specified: 14 MHz fixed |
| tS | 55.5 cyc at ~50k point; recorded elsewhere |
| VDDA | verified + recorded |
| Applied voltage points | multi-point across range (A-02); points = operator TEST VALUE |

### REQUIRED PROVENANCE
RAIN_MEASURED, APPLIED_V (instrument-measured), VDDA, SAMPLE_TIME_CYC, ADC_CLOCK_MHZ, EXPECTED_CODE, MEASURED_CODE, ERROR_LSB, REGION + common fields (E3 header).

### RAW DATA FORMAT
E3 CSV template (≥5 trials per point).

### ACCEPTANCE / CLOSURE CRITERIA
`NO OWNER THRESHOLD FOUND` (no continuity accuracy requirement → per-point report; PASS/FAIL = NOT AVAILABLE). Datasheet reference: region A expect ≤2 LSB (DS5319 guarantee) — claim limited to measured points (A-02). Closure criterion = T-G4-03 evidence (closure engine item 3).

### READINESS STATUS
READY

---

## T-G4-04 Readiness

### TEST PURPOSE
Measure settling after address / INH / channel-to-channel transitions on the ADC node; characterization only (no owner band).

### REQUIRED HARDWARE
F3 node (CD4067 MUX network + ADC node) + oscilloscope probe.

### REQUIRED INSTRUMENTATION
Oscilloscope ≥100 MHz class, single-shot capture; low-C probe, probe C_in recorded (protocol §6; A-04). Scope settings recorded (not prescribed by the repo — no minimum sample rate/record length specified).

### REQUIRED FIXTURE
Fixture F3 (combined node): CD4067B MUX network + ADC node + scope probe (execution sequence §1). Adds scope probe only to the T-G4-05 node.

### REQUIRED SETUP VALUES
| Value | Status |
|---|---|
| Transition types (address/INH/channel) | already specified |
| ≥5 captures per transition | already specified |
| Probe C_in + type | recorded (A-04) |
| Waveform file reference | field exists (E4); file-naming scheme NOT defined → `PROCEDURAL GAP` (minor) |
| Settling band | `NO OWNER THRESHOLD FOUND` → characterization only |

### REQUIRED PROVENANCE
WAVEFORM_FILE, PROBE_C_IN, PROBE_TYPE, SCOPE_SETTINGS, OLD_CHANNEL, NEW_CHANNEL, TRANSITION_TYPE, INITIAL_V, FINAL_V, PEAK_V, SETTLING_TIME, VDD, TEMP (E4 header).

### RAW DATA FORMAT
E4 CSV template + referenced waveform files.

### ACCEPTANCE / CLOSURE CRITERIA
`NO OWNER THRESHOLD FOUND` (settling band absent → CHARACTERIZATION ONLY; no scan-time compliance derived). Closure criterion = T-G4-04 captures exist (closure engine item 4).

### READINESS STATUS
READY WITH MISSING PROCEDURAL DETAIL — waveform file-naming scheme undefined; scope capture parameters are recorded-not-prescribed (both minor, characterization-only impact).

---

## T-G4-05 Readiness

### TEST PURPOSE
Measure node error vs OFF-channel count (N_OFF 0..15 for Option A node) at VDD 3.3 V and 5 V; regime classification above the measurement floor; compare vs theoretical bounds (15 µA / 63 µA at the 18 V condition).

### REQUIRED HARDWARE
CD4067B (Option A per-MUX node; Option B shared node only if that fixture is built) + node termination.

### REQUIRED INSTRUMENTATION
DMM (measurement floor recorded) (protocol §6).

### REQUIRED FIXTURE
Fixture F3 (node + termination).

### REQUIRED SETUP VALUES
| Value | Status |
|---|---|
| Node termination Z_effective | operator-selected + measured + recorded; else I_EFFECTIVE = NOT ESTABLISHED |
| N_OFF sweep 0..15 (A); 0..63 (B, if built) | already specified |
| VDD 3.3 / 5 V, ambient | already specified |
| Measurement floor | recorded |

### REQUIRED PROVENANCE
N_OFF, NODE_V, REF_V, DELTA_V, Z_EFFECTIVE, I_EFFECTIVE, MEAS_FLOOR + common fields (E5 header).

### RAW DATA FORMAT
E5 CSV template (≥3 trials per N_OFF).

### ACCEPTANCE / CLOSURE CRITERIA
`NO OWNER THRESHOLD FOUND` (no leakage/node-error requirement; regime classification above floor only — A-05). Theoretical 15/63 µA bounds are reference at the 18 V condition, NOT pass/fail. Closure criterion = T-G4-05 evidence (closure engine item 5).

### READINESS STATUS
READY

---

## T-G4-06 Readiness

### TEST PURPOSE
Cross-channel isolation blast radius: short/force one channel, read victims; populations same-MUX, cross-MUX, shared-node.

### REQUIRED HARDWARE
CD4067B network (A: per-MUX; B: shared node if built) + fault-injection path with MANDATORY current-limit element.

### REQUIRED INSTRUMENTATION
DMM / ADC readout (protocol §6; matrix).

### REQUIRED FIXTURE
Fixture F3 (node shared with T-G4-05/T-G4-04; fault injection last, current-limited).

### REQUIRED SETUP VALUES
| Value | Status |
|---|---|
| Fault type (force/short) | already specified |
| Current-limit element | MANDATORY (A-07; execution sequence §1.5; owner record). Value = `BLOCKED — CURRENT LIMIT NOT VERIFIED` — NOT defined/verified/recorded |
| Current-limit bounds | DS5319 ADC pin abs-max + SCHS052D abs-max: both `NEEDS RECHECK` (EV-44/EV-45) |
| Victim selection (same-MUX / cross-MUX / shared-node) | already specified |
| ≥3 trials per pair | already specified |

### REQUIRED PROVENANCE
SOURCE_CH, VICTIM_CH, POPULATION, FAULT_TYPE, CURRENT_LIMIT, EXPECTED_STATE, MEASURED_STATE, DELTA + common fields (E6 header).

### RAW DATA FORMAT
E6 CSV template.

### ACCEPTANCE / CLOSURE CRITERIA
`NO OWNER THRESHOLD FOUND` (no isolation requirement → blast-radius characterization only). Closure criterion = T-G4-06 evidence + current-limit verification log (closure engine item 6; owner record).

### READINESS STATUS
NOT READY — `BLOCKED — CURRENT LIMIT NOT VERIFIED`. Execution must not be authorized for T-G4-06 until the current-limit element value is defined within verified datasheet bounds and the verification is recorded.

---

## Fixture Readiness

Repository content (execution sequence §1; protocol §7): F1 (DUT bench — CD4067B + address/INH + supply + Kelvin), F2 (ADC path — STM32 + ladder), F3 (combined node — MUX network + ADC node + scope probe). All three topologies are described at topology level; owner APPROVED the build. DUT, CD4067, STM32 board, ADC node, channel selection, supply rails, test points, current injection (F1), fault injection (F3), measurement points, grounding/wiring/probe connection are covered conceptually.

Missing: actual component values are TEST VALUES not yet selected/recorded (ladder resistors, node termination, current-limit element, ITEST, switch-state load) → `FIXTURE VALUE MISSING` for those (operator-selected + recorded at execution per owner authorization). No schematic/PCB exists (by design — topology level only). READY at documentation level; physical build + test-value selection are operator actions.

## Instrumentation Readiness

Instruments are specified by CAPABILITY, not model (protocol §6): PSU (3.3/5 V metered), DMM (4.5+ digit, 4-wire), oscilloscope (≥100 MHz, single-shot, low-C probe), calibrated resistor set, temperature control (ambient), address/control driver. No model invented. Operator logs IDs + calibration status before first measurement (run card instrument log). READY — operator action pending.

## Provenance Readiness

Defined fields (protocol §15, run card, E1-E6 headers): TEST_ID, DUT_ID, TRIAL, VDD, TEMP, CHANNEL, CONDITION/INPUT/OUTPUT, VALUE, UNIT, INSTRUMENT, INSTRUMENT_ID, CALIBRATION_STATUS, OPERATOR, DATE, TIME, REMARK + test-specific fields (RAIN_MEASURED, APPLIED_V, VDDA, tS, ADC clock, EXPECTED/MEASURED/ERROR_LSB/REGION; WAVEFORM_FILE, PROBE_C_IN; N_OFF, NODE_V, REF_V, DELTA_V, Z_EFFECTIVE, I_EFFECTIVE, MEAS_FLOOR; SOURCE_CH, VICTIM_CH, POPULATION, FAULT_TYPE, CURRENT_LIMIT, EXPECTED/MEASURED_STATE, DELTA). All are project-required (closure engine items 1-6, 9). READY — operator fills at execution.

## Raw Data / Template Readiness

E1-E6 CSV templates exist (RX50_G4_RAW_DATA_TEMPLATES.md), empty and log-ready, comma-delimited with header rows → suitable for later automated ingestion into the raw evidence register (RX50_G4_RAW_EVIDENCE_REGISTER.md ingestion state; protocol §20 evidence package). The ingest rule (raw rows appended as-is, invalid rows marked not repaired) is defined. No missing mandatory field identified in E1-E6 for their test purposes. READY.

## Temperature Coverage

Owner decision recorded: **AMBIENT ONLY, recorded per trial** (decision sheet 1.4; start pack owner record; operator brief). Protocol's optional 85 °C soak is explicitly deferred (start pack TASK 5). No competing temperature requirement found in the repository — no contradiction to create. RESOLVED.

## Procedural Gaps

1. SCHS052D absolute-max current row unverified (`NEEDS RECHECK`, EV-45) — bounds ITEST (T-G4-01) and the T-G4-06 current limit. Datasheet PDF not resident in workspace.
2. DS5319 ADC-pin absolute-max row unverified (`NEEDS RECHECK`, EV-44) — bounds the T-G4-06 current limit.
3. T-G4-06 current-limit value + verification log absent — `BLOCKED — CURRENT LIMIT NOT VERIFIED`.
4. T-G4-04 waveform file-naming scheme undefined (field exists; convention absent) — minor.
5. "G4 Evidence Retrieval" file referenced but absent (OI-16) — evidence artifact, not execution-critical.

## Owner Decisions Required

- None outstanding: Group-1 decisions (fixture F1/F2/F3, temperature ambient, single DUT, test-value delegation, instruments) are all recorded in the start pack owner approval record. Group-2 thresholds were explicitly declined → characterization-only.
- (Recorded for completeness) Any future margin on RTH + RON + RTRACE < 10 kΩ and any future settling/isolation/continuity thresholds would require owner decision.

## Operator Actions Required

1. Build F1, F2, F3 at topology level (approved); tag DUTs with DUT_ID; record F2 board revision.
2. Verify instruments (PSU set-points with DMM; DMM 4-wire on reference resistor; scope probe compensation); log IDs + calibration status.
3. Select + measure + record test values as TEST VALUE: ITEST (within datasheet bounds), ladder resistors, node termination Z_effective, switch-state load, measurement protection.
4. Verify the T-G4-06 fault-injection current-limit element and record its value + verification (mandatory pre-run gate).
5. Fill instrument log and every E1-E6 row; attach T-G4-04 waveform files.
6. Record ambient temperature per trial; apply ADC config (fADC = 14 MHz, tS = 55.5 cyc at ~50k).
7. Assemble the 12-item evidence package (protocol §20) and fill the closure statement (not pre-declared).

## Execution Sequence

Constructed from RX50_G4_EXECUTION_SEQUENCE.md + run card (no new test steps added; two items made explicit):

1. Fixture preparation (F1/F2/F3 build; test values selected+recorded; Kelvin wiring; current-limit element installed).
2. Instrument verification (PSU set-points, DMM reference, scope compensation; IDs + cal logged).
3. Provenance recording (instrument log; DUT_ID; operator).
4. Pre-test checks (power sequencing; INH/address reset; ADC self-cal per DS5319; ambient temperature recorded; supply transition stabilization/re-reference per A-08).
5. T-G4-01 (RON, F1).
6. T-G4-02 (VIH/VIL, F1 — control sweep).
7. T-G4-03 (ADC vs RAIN, F2).
8. T-G4-05 (leakage, F3).
9. T-G4-04 (settling, F3 + scope probe).
10. T-G4-06 (isolation, F3 — fault injection LAST; current-limit verified BEFORE this step).
11. Raw-data preservation (all rows complete; waveform files referenced; conflict records created if applicable).
12. Data handoff to Harness (below).

Ordering is unambiguous in the repo (execution sequence §4). No ordering ambiguity found. Sequence note: the repo orders leakage before settling before isolation on F3 to minimize rewiring; this is preserved.

## Data Handoff Protocol

1. Operator returns the FILLED E1-E6 templates (CSV, as-is original rows; no summarization) + the instrument log + T-G4-04 waveform files (original filenames preserved) + the 12-item evidence package (protocol §20).
2. Harness ingests rows into the raw evidence register as-is (rows appended unmodified; INVALID flagged, never repaired — raw evidence register ingestion rule).
3. Harness runs F1-F7 processing, quality checks, measured-vs-datasheet conflict logging, and re-evaluates closure engine items 1-9.
4. The Harness MUST NOT accept a manually summarized number (e.g., a single "RON = 3.5 kΩ" figure) in place of the original raw rows where the protocol requires raw evidence. Summary values without raw backing are `REPORT CLAIM ONLY`.
5. Provenance, test IDs, measurement conditions, and waveform file references must survive the handoff intact; any gap is flagged as `RAW DATA PRESENT — TRACEABILITY INCOMPLETE`.

## Final Readiness Gate

| Readiness item | Status |
|---|---|
| Fixture readiness | READY (build approved; physical build + test values = operator action) |
| Instrument readiness | READY (capability-defined; IDs/cal to be logged) |
| T-G4-01 readiness | READY WITH MISSING PROCEDURAL DETAIL (ITEST abs-max bound unverified) |
| T-G4-02 readiness | READY |
| T-G4-03 readiness | READY |
| T-G4-04 readiness | READY WITH MISSING PROCEDURAL DETAIL (waveform naming; scope params recorded-not-prescribed) |
| T-G4-05 readiness | READY |
| T-G4-06 readiness | NOT READY — BLOCKED — CURRENT LIMIT NOT VERIFIED |
| Data-ingestion readiness | READY |

**OVERALL: NOT READY** — per mission rule, the project cannot be called ready while the T-G4-06 fault-injection current-limit verification is missing, and the ITEST/current-limit datasheet bounds are `NEEDS RECHECK`. This is a narrow, execution-start condition: T-G4-01..T-G4-05 can begin once the two datasheet bounds (EV-44/EV-45) are verified; T-G4-06 must wait for its current-limit element to be defined and verified. The repository's `READY TO MEASURE` declarations (operator brief, start pack) are consistent regarding OWNER input (complete) but overstate full execution readiness given the unresolved current-limit + ITEST-bound items.

### VERIFIED

- Complete, internally consistent G4 measurement package exists (protocol + 9 companion artifacts), audited clean (0 CRITICAL / 0 HIGH, 6 MEDIUM / 4 LOW corrections applied — protocol audit).
- All Group-1 owner decisions recorded (fixture F1/F2/F3 approved; ambient only; single DUT; operator-authorized TEST VALUEs; Group-2 = characterization-only).
- Owner approval record dated 2026-08-15 present in start pack.
- Test methods, instruments (by capability), provenance fields, E1-E6 templates, F1-F7 rules, and closure criteria are fully defined in the repository.
- No raw measurement exists (consistent with M002); no measurement was fabricated by M003A.

### READY

- T-G4-02, T-G4-03, T-G4-05 execution (all procedural requirements defined; owner decisions recorded).
- Fixture build instructions and instrument capability requirements.
- Data-ingestion path (templates + raw evidence register).

### OWNER DECISIONS

- None outstanding. (Future: engineering margin on the 10 kΩ constraint, settling/isolation/continuity thresholds — declined for now.)

### PROCEDURAL GAPS

1. SCHS052D absolute-max current row — `NEEDS RECHECK` (EV-45) — bounds ITEST and T-G4-06 current limit.
2. DS5319 ADC-pin absolute-max row — `NEEDS RECHECK` (EV-44) — bounds T-G4-06 current limit.
3. T-G4-04 waveform file-naming scheme — undefined (minor).
4. "G4 Evidence Retrieval" referenced file — absent (OI-16; evidence artifact).

### BLOCKED

- T-G4-06 execution — `BLOCKED — CURRENT LIMIT NOT VERIFIED` (current-limit element value + verification record absent; bounds unverified).
- Overall readiness gate = NOT READY until gaps 1-2 and the current-limit verification are closed.

### OPERATOR ACTIONS

- Build F1/F2/F3; verify instruments; select+measure+record TEST VALUEs; verify+record T-G4-06 current limit; execute T-G4-01..06 in the defined order; fill E1-E6 with provenance; attach waveform files; assemble the 12-item evidence package; hand back raw data per the Data Handoff Protocol.

### NEXT MISSION

**M003B — G4 PRE-EXECUTION BLOCKER CLOSURE**: verify the SCHS052D absolute-max current row and the DS5319 ADC-pin absolute-max row from the manufacturer PDFs (closing EV-44/EV-45), define + record the T-G4-06 fault-injection current-limit value and its verification, and define the T-G4-04 waveform file-naming scheme. Rationale: procedural gaps remain, so the next mission must resolve those blockers — not fabricate a closure mission. When M003B closes, the follow-on is M004 — G4 DATA ACQUISITION / INGESTION (operator executes, harness ingests).

END MISSION M003A.