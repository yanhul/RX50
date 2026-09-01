# RX50 F3 FINAL ENGINEERING PACKAGE
# T-G4-06 / PRE-M004 CONSOLIDATED BATCH

- Package: F3 FINAL ENGINEERING PACKAGE — T-G4-06 / PRE-M004 (single consolidated artifact, replaces a sequential M003G→M003H workflow)
- Date: 2026-08-15
- Status: COMPLETE (engineering package only — no physical build, no measurements, no E6 fabrication, no M004 authorization, no G4 closure, no architecture change)

This package performs the ENTIRE T-G4-06 F3 engineering analysis in ONE PASS from the current repository state. It does NOT create an intermediate mission. No value is invented to mask a gap; every gap is recorded explicitly.

---

## SECTION 0 — OWNER DECISIONS PRESERVED (verbatim, not overwritten)

| ID | Decision | Content | Source |
|---|---|---|---|
| D-01 | Waveform naming convention | `<TEST_ID>_<DUT_ID>_N<channel_or_node>_TR<seq>.<ext>` (e.g., `T-G4-04_DUT-001_N12_TR01.CSV`); WAVEFORM_FILE = exact filename; original filenames preserved on handoff | OWNER-APPROVED, M003E (D-22) |
| D-03 | Option B — 5 V / ADC routing | 5 V-referenced sense node MUST NOT be connected directly to the STM32 ADC input during 5 V characterization; NO attenuation/clamp network invented; ADC observations requiring valid STM32 ADC range performed under an appropriate supply/test condition; preserve CD4067-side 5 V vs MCU ADC distinction | OWNER-APPROVED (fixture/test-procedure only, NOT architecture), M003E (D-23) |
| D-02 | Current-limiter element policy | DO NOT lock a numerical current-limiter value merely from the ≤5 mA safety bound; the ACTUAL F3 path determines the limiter; physical verification is MANDATORY; |I_fault| ≤5 mA is a maximum permissible bound, NOT the selected test current | OWNER POLICY RECORDED — value PENDING physical fixture verification, M003E (D-24) |

These decisions are binding on this package and are NOT altered.

---

## SECTION 1 — EVIDENCE EXTRACTION

Source-of-truth read fresh from the repository (registers, missions M003A–M003F, G4 package). Repository evidence is authoritative; no conversation memory is substituted.

| ID | Fact | Value | Source | Status |
|---|---|---|---|---|
| EV-45 | CD4067B source/drain continuous current IS/ID | ±20 mA ABS MAX / ±10 mA recommended operating; control-input pins ISEL/IEN ±30 mA | TI SCHS052D Rev D (Absolute Max / Rec. Op.) | VERIFIED |
| EV-47 | STM32F103 IINJ(PIN) any non-FT pin | ±5 mA | ST DS5319 Table 7 | VERIFIED |
| EV-47b | STM32F103 ΣIINJ(PIN) total injected current | ±25 mA | ST DS5319 Table 7 | VERIFIED |
| EV-48 | STM32F103 VIN abs max non-FT pin | VSS−0.3 .. 4.0 V | ST DS5319 Table 6 | VERIFIED |
| EV-49 | Datasheet identity/revision | DS5319 Rev 20 (CD00161566), STM32F103C8/STM32F103C8T6; secondary render rejected | ST product page; C-22 | VERIFIED (authority level) |
| — | Governing T-G4-06 fault-injection bound | **≤ ±5 mA** = min(EV-47, EV-45); ΣIINJ aggregate cap ±25 mA | derived from EV-47/EV-45 | VERIFIED (derived) |

### Extracted from G4 package (authoritative text, not rewritten)

- **T-G4-06 protocol (protocol §14):** objective = "determine fault/readout blast radius"; method = "select one channel; force/short/terminate it per the approved fixture condition; read other channels; repeat across channel positions". Populations: A same-MUX, B different-MUX groups, C shared-node topology where applicable. Record: source channel, victim channel, expected state, measured state, delta, VDD, temperature, channel count, fixture condition. Do NOT invent an isolation dB/voltage/percentage/resistance requirement. If no owner isolation criterion: classification = CHARACTERIZATION ONLY. (All marked ASSUMPTION/CONSTRAINT in the protocol.)
- **E6 template (raw-data templates §E6):** TEST_ID, DUT_ID, TRIAL, VDD, TEMP, SOURCE_CH, VICTIM_CH, POPULATION, FAULT_TYPE (short/force), CURRENT_LIMIT, EXPECTED_STATE, MEASURED_STATE, DELTA, UNIT, INSTRUMENT, INSTRUMENT_ID, CAL_STATUS, OPERATOR, DATE, TIME, REMARK. `CURRENT_LIMIT` is MANDATORY for all fault injection. ≥3 trials per (source,victim) pair.
- **Test matrix (T-G4-06):** inputs = fault injection on source channel (force/short with mandatory current limit, value recorded); controlled = VDD, temperature, fault type, current limit, victim selection; measured = victim channel output vs expected, delta; instrument = DMM/ADC readout; datasheet comparison = none (no isolation spec); owner requirement = none yet; PASS/FAIL = NOT AVAILABLE; default = CHARACTERIZATION ONLY; physical measurement REQUIRED.
- **Closure evidence plan (§T-G4-06):** setup = "short one channel; read neighboring/other channels"; measure = change in other channels' readings (Option A within MUX group and across MUXes; Option B shared node); decision logic = blast-radius characterization; isolation spec TBD (owner).
- **Execution sequence:** §1.5 mandatory current-limit element in F3 fault-injection path (value recorded); §4.6 fault injection LAST (current-limited); §5.3 D-03 Option B constraint (5 V-referenced sense node not connected directly to ADC); §10.2 remove fault-injection connections FIRST at shutdown, then power down, disconnect ADC pin loads.
- **Protocol audit A-07 (LOW):** make the current-limit element MANDATORY for all force/short tests; limit value = OWNER TEST VALUE - TBD and recorded; ADC pin protection per DS5319 absolute ratings. Applied in execution sequence §1.5.
- **Owner decision sheet 1.3 / start pack TASK 2:** test values (incl. fault-injection current-limit element) are operator-authorized TEST VALUEs, selected within bounds, measured, recorded, and verified before use.
- **Net register / architecture:** EMPTY / NOT LOCKED / SHEET DEFINITION BLOCKED / RELEASE GATE NOT RELEASED — no RX50 net or schematic exists; every fault-path element is fixture-only.

---

## SECTION 2 — REQUIREMENT EXTRACTION

| Requirement | Determination | Evidence | Status |
|---|---|---|---|
| T-G4-06 measures cross-channel isolation blast radius | DEFINED functionally (fault a source channel; read victims) | protocol §14; test matrix; closure plan | DERIVED |
| Fault is created by force/short (per approved fixture condition) with a MANDATORY current-limit element | DEFINED (mechanism) | protocol §14; E6 FAULT_TYPE; A-07; execution seq. §1.5 | DERIVED |
| Fault current limited to ≤ ±5 mA (governing) and ΣIINJ ≤ ±25 mA | VERIFIED BOUND | EV-47, EV-47b, EV-45 | VERIFIED |
| Fault injection connected LAST, removed FIRST | ORDER CONSTRAINT | execution seq. §4.6 / §10.2 | DERIVED |
| E6 CURRENT_LIMIT recorded for all fault injection | MANDATORY FIELD | E6 template; execution seq. | DERIVED |
| 5 V-referenced sense node NOT connected directly to STM32 ADC (5 V runs) | OWNER-APPROVED CONSTRAINT | D-03 Option B (M003E); execution seq. §5.3 | OWNER-APPROVED |
| No isolation dB/voltage/percentage/resistance requirement invented; no owner criterion → CHARACTERIZATION ONLY | CONSTRAINT | protocol §14 | DERIVED |
| ≥3 trials per (source,victim) pair | CONSTRAINT | E6 template; test matrix | DERIVED |
| Actual limiter value determined by ACTUAL F3 path + physical verification (not chosen from the bound) | OWNER POLICY | D-02 (M003E) | OWNER POLICY — value pending |
| **REQUIRED TEST LEVEL (electrical stimulus for force/short)** | **NOT SPECIFIED** | protocol §14 defines mechanism only; no approved fixture condition, no voltage/current level, no short reference exists | **REQUIREMENT MISSING** |

---

## SECTION 3 — T-G4-06 FAULT DEFINITION

Preserving the protocol's terminology (source channel / victim channel / fault type / population / expected state / measured state / delta).

| Item | Determination | Source | Status |
|---|---|---|---|
| Fault source | A channel selected as SOURCE_CH in the CD4067B network | protocol §14; E6 SOURCE_CH | DERIVED |
| Fault victim | Other channels read out as VICTIM_CH to observe blast radius | protocol §14; E6 VICTIM_CH | DERIVED |
| Fault mechanism | FAULT_TYPE ∈ {short, force}; "force/short/terminate it per the approved fixture condition" | protocol §14; E6 | DERIVED (mechanism); electrical level NOT specified |
| Source node | SOURCE_CH terminal on the DUT CD4067B network (fixture test point) | test matrix; E6 | DERIVED (functional) |
| Victim nodes | same-MUX / cross-MUX / shared-node per POPULATION | protocol §14; E6 POPULATION | DERIVED |
| Injection direction | Fault injected into the source-channel node; victims read on their node; injection LAST | execution seq. §4.6 | DERIVED |
| Normal state | EXPECTED_STATE (e.g., ON) recorded per row | E6 EXPECTED_STATE | DERIVED |
| Fault state | SOURCE_CH shorted/forced through the current-limited path; victims measured (MEASURED_STATE) | E6 FAULT_TYPE / MEASURED_STATE | DERIVED |
| Expected observation | DELTA = MEASURED_STATE − EXPECTED_STATE per (source,victim); blast-radius characterization | E6 DELTA; calculation rules F6 | DERIVED |
| Required recovery | Remove fault-injection connections FIRST; power down; disconnect ADC pin loads | execution seq. §10.2-3 | DERIVED |
| **REQUIRED TEST LEVEL** | **NOT SPECIFIED** — no electrical level for force/short/terminate exists | protocol §14 | **REQUIRED TEST LEVEL NOT SPECIFIED** |

### Four-quantity separation (never converted into each other)

| # | Quantity | Value | Status |
|---|---|---|---|
| 1 | REQUIRED TEST LEVEL | NOT SPECIFIED | `REQUIRED TEST LEVEL NOT SPECIFIED` — operator/owner TEST VALUE must be supplied+recorded; harness does not invent |
| 2 | SAFETY LIMIT | \|I_fault\| ≤ 5 mA (governing; ΣIINJ ≤ 25 mA) | VERIFIED BOUND (EV-47/EV-47b/EV-45) |
| 3 | SELECTED CURRENT-LIMITER VALUE | NOT SELECTED | OWNER POLICY (D-02): actual F3 path determines it; physical verification mandatory |
| 4 | MEASURED FAULT CURRENT | NO MEASUREMENT EXISTS | MEASUREMENT PENDING — physical verification record absent |

`|I_fault| ≤ 5 mA` is the SAFETY BOUND. It is NOT `I_test = 5 mA`. No conversion is made anywhere in this package.

---

## SECTION 4 — ELECTRICAL PATH ANALYSIS (BUILDABILITY)

Test per connection: WHAT connects / TO WHAT / THROUGH WHAT / UNDER WHAT CONDITION / RETURN PATH / HOW DISCONNECTED. A connection is specified only if the operator can build it without guessing.

| Node | From | To | Series element | State | Return | Evidence | Status |
|---|---|---|---|---|---|---|---|
| VDD supply | bench PSU (3.3/5 V set-points) | CD4067B VDD + DUT rail | none | PSU output ON | PSU return → VSS common | protocol §6/§7; execution seq. §2.1 | SPECIFIED |
| VDDA supply | bench PSU (3.3 V) | STM32F103 VDDA | none | PSU output ON | PSU return → VSS | protocol §7 | SPECIFIED |
| VSS/ground | PSU return | CD4067 VSS, STM32 VSS, fixture common | none | hard | common ground | protocol §7 | SPECIFIED (functional; physical layout = operator build detail) |
| Address/INH control | STM32 GPIO OR bench generator | CD4067 A/B/C/D, INH | none | GPIO/generator state; slew+levels recorded (T-G4-02) | driver → GND | protocol §7/§10 | SPECIFIED (driver set allowed) |
| ADC observation | CD4067 common (X) / channel (Y) node | STM32 ADC pin (e.g., PA0) | none (direct sense) | fixed sense path | ADC internal → VSS | protocol §7; D-03 Option B | SPECIFIED for 3.3 V; 5 V runs constrained (no 5 V-referenced sense node on ADC) |
| Scope probe | ADC node | oscilloscope | probe C_in (low-C, recorded) | probe connect | probe ground → fixture ground | protocol §7; E4; A-04 | SPECIFIED |
| Node termination (shared T-G4-05) | node | termination reference | Z_effective (recorded TEST VALUE) | hard/removable | termination reference node (not explicitly defined) | test matrix T-G4-05; start pack TASK 2 | PROPOSED — reference node unspecified |
| **Fault-injection path** | FAULT SOURCE (type unspecified) | SOURCE_CH terminal | CURRENT-LIMIT ELEMENT (mandatory; value/type = TEST VALUE, none selected) | injection connection mechanism UNSPECIFIED | **REQUIREMENT MISSING** | protocol §14; A-07; execution seq. §1.5/§4.6/§10.2 | **BLOCKED / REQUIREMENT MISSING** |

### Buildability verdict

**F3 is NOT buildable without operator/owner TEST VALUE selection for the eight items below.** The fault-injection path is safety-critical (it fixes fault current into the ADC node) and its source interface, short reference, return path, connection mechanism, and current measurement point are unspecified. An operator building F3 today must guess them.

| # | Unresolved requirement | Safety-critical | Status |
|---|---|---|---|
| 1 | T-G4-06 TEST LEVEL (force V/I; short reference; terminate impedance) | YES | `REQUIRED TEST LEVEL NOT SPECIFIED` — operator/owner TEST VALUE |
| 2 | Fault source interface (source type, terminals, polarity, max source condition) | YES | `REQUIREMENT MISSING` |
| 3 | Short reference (to VSS / VDD / other channel) | YES | `REQUIREMENT MISSING` |
| 4 | Return path for fault current | YES | `REQUIREMENT MISSING` |
| 5 | Injection connection/disconnection mechanism (manual/relay/plug) | YES | `REQUIREMENT MISSING` |
| 6 | Current measurement point (where |I_fault| is verified) | YES | `REQUIREMENT MISSING` |
| 7 | Current-limit element type + value | YES | TEST VALUE pending physical verification (D-02) |
| 8 | Node-termination reference node (shared T-G4-05) | NO | TEST VALUE (operator/owner) |

These remain in operator/owner ownership (decision sheet 1.2/1.3; M003E D-02). The harness does not fill them.

---

## SECTION 5 — F3 FINAL TOPOLOGY (build-oriented textual schematic)

```text
FAULT SOURCE (bench PSU / source; type = operator/owner TEST VALUE; short or force; level = TEST VALUE recorded per trial)
     |
     |
CURRENT LIMITER (MANDATORY series element, in fault-injection path; type+value = operator/owner TEST VALUE,
                 NOT derived from the ≤5 mA bound; worst-case current VERIFIED ≤ ±5 mA; physically verified pre-run)
     |
     |
FAULT ENABLE / CONNECTION (injection switch/connection; mechanism = operator/owner TEST VALUE;
                           connected LAST §4.6, disconnected FIRST §10.2)
     |
     |
SOURCE_CH (source-channel terminal on the DUT CD4067B network; fault injected here)
     |
     |
DUT / VICTIMS (CD4067B network, single DUT; victims read on their node via DMM/ADC;
               populations same-MUX / cross-MUX / shared-node)
     |
     |
RETURN (return path for fault current = operator/owner TEST VALUE, defined and recorded — REQUIREMENT MISSING today)
```

### Node/interface requirements

| Node | Requirement | Basis |
|---|---|---|
| FAULT SOURCE | able to apply short or force; level recorded per trial; must not drive the fault node beyond verified bounds (≤ ±5 mA; ADC node ≤ 4.0 V) | protocol §14; EV-47/EV-48 |
| CURRENT LIMITER | mandatory series element; worst-case |I_fault| ≤ ±5 mA (EV-47) and ΣIINJ ≤ ±25 mA (EV-47b); element identified, installed, physically verified pre-run, recorded in E6 CURRENT_LIMIT + safety record | execution seq. §1.5; A-07; M003B; M003E D-02 |
| FAULT ENABLE | connect LAST, disconnect FIRST (removable/manual/relay per operator TEST VALUE) | execution seq. §4.6 / §10.2 |
| SOURCE_CH | test point on the source channel terminal of the DUT network | test matrix T-G4-06 |
| DUT | single CD4067B unit; victims read on their node | decision 1.5; protocol §14 |
| RETURN | return path for fault current — MUST be defined and recorded by operator/owner (not present in repo) | — |
| ADC observation | D-03 Option B: 5 V-referenced sense node NOT connected directly to STM32 ADC; ADC reads at 3.3 V-condition or channel-side only | M003E D-23; execution seq. §5.3 |

---

## SECTION 6 — CURRENT-LIMIT DERIVATION

### 6.1 Safety bound (VERIFIED, hierarchy level 3→5)

| Limit | Value | Evidence | Role |
|---|---|---|---|
| STM32F103 IINJ(PIN) non-FT pin — abs max | ±5 mA | EV-47 (DS5319 Table 7) | **GOVERNING (tightest)** |
| STM32F103 ΣIINJ(PIN) total — abs max | ±25 mA | EV-47b (DS5319 Table 7) | aggregate cap |
| CD4067B IS/ID source/drain current — abs max | ±20 mA | EV-45 (SCHS052D Rev D) | channel path |
| CD4067B IS/ID — recommended operating | ±10 mA | EV-45 (SCHS052D Rev D) | rec. op. reference |
| STM32F103 VIN non-FT — abs max | VSS−0.3 .. 4.0 V | EV-48 (DS5319 Table 6) | ADC-node voltage stress |

**Derived safety bound:** worst-case fault-injection current into the fault node must be **≤ ±5 mA** = min(IINJ(PIN) ±5 mA, CD4067 IS/ID ±20 mA). Aggregate ΣIINJ(PIN) ≤ ±25 mA if multiple pins are simultaneously injected.

### 6.2 What M003F/M003G establish and what they do NOT

- ESTABLISHED: the safety bound (≤ ±5 mA), the mandatory series limiter, the constraint |I_fault| = f(source level, path impedance, limiter) must hold ≤ ±5 mA, the physical-verification requirement.
- NOT ESTABLISHED (and NOT invented here): the limiter element value, the source level, the short reference, the return path, and the measured fault current. Selecting a limiter from the 5 mA bound alone (e.g., "5 V / 5 mA → 1 kΩ") is explicitly FORBIDDEN by D-02: the ACTUAL F3 path determines the limiter, and the worst-case current must be VERIFIED against the bound.

### 6.3 Verification constraint (given to the operator, not a value)

Worst-case fault current = (source voltage − node voltage) / path impedance including limiter, measured at the defined current measurement point, must be ≤ ±5 mA across the chosen test level; recorded in E6 CURRENT_LIMIT and in `measurements/T-G4-06_CURRENT_LIMIT_SAFETY_RECORD.md`.

---

## SECTION 7 — ADC / CD4067 SAFETY ANALYSIS

### 7.1 ADC pin stress (F3 path; T-G4-05 / T-G4-06)

- ADC pins PA0–PA7 on STM32F103C8T6 are standard (non-5V-tolerant): VIN abs max = VSS−0.3 .. 4.0 V (EV-48); IINJ(PIN) = ±5 mA; ΣIINJ(PIN) = ±25 mA (EV-47/47b).
- Positive injection within IINJ/ΣIINJ limits does not affect ADC accuracy; negative injection on analog pins reduces accuracy (avoid; DS5319 §5.3.12/5.3.13 — recorded as characterization constraint).
- The F3 current-limit element is the protection mechanism. No schematic/PCB and no recorded element value exist → **board-level protection is NOT demonstrated by the repository**. The operator's mandatory pre-run physical verification is the evidence that will establish it. M003F/M003G do NOT claim the ADC is protected.

### 7.2 5 V path (D-03 Option B, OWNER-APPROVED)

- Any 5 V-level fault forced directly onto the ADC pin would exceed the verified VIN abs max 4.0 V (EV-48). This is the same architectural surface as C-20b and is logged there.
- Per D-03 Option B: during 5 V characterization (T-G4-05/T-G4-06 5 V runs), the 5 V-referenced sense node MUST NOT be connected directly to the STM32 ADC input; NO attenuation/clamp network is invented; ADC observations requiring valid STM32 ADC range are performed under an appropriate supply/test condition (e.g., 3.3 V). The CD4067-side 5 V vs MCU ADC distinction is preserved.

### 7.3 CD4067 constraints

- Fault path current on CD4067 channel stays within IS/ID abs max ±20 mA / rec. op. ±10 mA (EV-45) — automatically satisfied when the governing ≤ ±5 mA bound holds.
- Control-input pins: ISEL/IEN ±30 mA (EV-45) — not a fault-path element, recorded for completeness.

### 7.4 Safety sequence

1. Fault injection is connected LAST (§4.6) — protects the fixture during T-G4-01..05.
2. At shutdown, fault-injection connections are removed FIRST (§10.2), then power down, then disconnect ADC pin loads.

---

## SECTION 8 — BUILD SPECIFICATION

### 8.1 Buildable elements (operator can build without guessing)

| Element | Specification | Status |
|---|---|---|
| DUT | one CD4067B unit, DUT_ID tagged (decision 1.5) | SPECIFIED |
| VDD / VDDA / VSS | PSU set-points 3.3/5 V and 3.3 V; common ground | SPECIFIED |
| Address/INH | STM32 GPIO or bench generator; slew/levels recorded | SPECIFIED |
| ADC observation | ADC pin (e.g., PA0) reading CD4067 common/channel node; 3.3 V-condition; 5 V constrained by D-03 Option B | SPECIFIED (with D-03 constraint) |
| Scope probe | low-C probe, C_in recorded (T-G4-04) | SPECIFIED |
| Test values (limiter, source level, Z_effective, termination reference, fault type level) | operator/owner TEST VALUE, selected within bounds, measured, recorded, verified before use | TEST VALUE (decision sheet 1.3; D-02) |
| Fault-injection path (source interface, short reference, return, connection mechanism, measurement point) | NOT DEFINED in repo | REQUIREMENT MISSING (Section 4) |

### 8.2 Provenance (mandatory fields per row)

TEST_ID, DUT_ID, TRIAL, VDD, TEMP, SOURCE_CH, VICTIM_CH, POPULATION, FAULT_TYPE, CURRENT_LIMIT, EXPECTED_STATE, MEASURED_STATE, DELTA, UNIT, INSTRUMENT, INSTRUMENT_ID, CAL_STATUS, OPERATOR, DATE, TIME, REMARK (E6). Every row requires all applicable fields; blank mandatory field = trial INVALID (protocol §15).

### 8.3 Evidence package (protocol §20, 12 items)

Raw data, processed data, instrument info, DUT identification, test conditions, fixture identification/photos, oscilloscope captures (T-G4-04), datasheet references, calculation sheet, anomaly/conflict register, owner decisions, final G4 closure statement. Closure statement NOT pre-written; "G4 CLOSED" not used pre-emptively.

---

## SECTION 9 — PHYSICAL VERIFICATION PLAN (operator-executed, mandatory pre-run)

Order mandated by owner policy (M003E D-02) and the safety record:

1. Construct/identify the actual F3 fault-injection path (build at topology level — owner-approved F1/F2/F3 build).
2. Supply/record the unresolved items of Section 4: TEST LEVEL (force V/I, short reference, terminate impedance), fault-source interface, return path, injection connection mechanism, current measurement point, node-termination reference.
3. Select the current-limiting element from the ACTUAL path (value = operator/owner TEST VALUE; NOT chosen from the 5 mA bound alone).
4. Verify the resulting worst-case current against the |I_fault| ≤ 5 mA bound (EV-47/EV-45) at the defined measurement point.
5. Physically verify the installed element (identity, nominal value, measured value, method, instrument, date/operator, resulting calculation).
6. Record the verification in E6 `CURRENT_LIMIT` (all rows of fault injection) and complete `measurements/T-G4-06_CURRENT_LIMIT_SAFETY_RECORD.md` (currently NOT VERIFIED / INCOMPLETE).
7. Only then permit T-G4-06 execution (fault injection LAST per §4.6; remove FIRST at shutdown §10.2).

This verification is the evidence that establishes fixture protection. A document value, a calculation, or a datasheet value is NOT physical verification. This plan is operator-executed and MUST NOT be run automatically by the harness.

---

## SECTION 10 — FINAL GATE

### VERIFIED

- Governing fault-injection bound ≤ ±5 mA (EV-47/EV-45); ΣIINJ ≤ ±25 mA (EV-47b); ADC VIN ≤ 4.0 V (EV-48).
- Mandatory current-limit element in F3 fault-injection path (A-07; execution seq. §1.5).
- Fault injection LAST (§4.6), removed FIRST (§10.2); E6 CURRENT_LIMIT mandatory.
- D-03 Option B owner-approved (5 V sense node not connected to ADC); no clamp/attenuation invented.
- No RX50 net/schematic exists (net register EMPTY) → every fault-path element is FIXTURE-ONLY → NO ARCHITECTURE CHANGE REQUIRED.
- D-01 / D-03 / D-02 preserved verbatim (Section 0).

### REQUIREMENT MISSING / NOT SPECIFIED (recorded, not invented)

1. `REQUIRED TEST LEVEL NOT SPECIFIED` (force V/I; short reference; terminate impedance) — operator/owner TEST VALUE.
2. Fault-source interface, return path, injection connection mechanism, current measurement point — `REQUIREMENT MISSING`.
3. Current-limit element type + value — TEST VALUE pending physical verification (D-02).
4. Node-termination reference node — operator/owner TEST VALUE.

### BLOCKED

- **T-G4-06 execution** — TEST LEVEL + source interface + return + limiter verification all absent.
- **T-G4-05 / T-G4-06 5 V condition** — constrained by D-03 Option B (no 5 V sense node on ADC); 5 V channel-side characterization permitted.

### M004

**M004 NOT AUTHORIZED** — this package is engineering/design only; it does not authorize measurement.

### G4 / ARCHITECTURE

- G4: BLOCKED / MEASUREMENT PENDING (0 rows ingested).
- C-20b: OPEN (architecture decision, unchanged).
- RX50 architecture: UNCHANGED (net register EMPTY; architecture NOT LOCKED).

### NEXT ACTION (operator-executed, NOT automatic)

`M004 PRE-RUN PHYSICAL VERIFICATION` — supply/record Section 4 items, build F3, select the current-limit element from the actual path, verify worst-case current ≤ ±5 mA, physically verify the installed element, record E6 CURRENT_LIMIT, complete the safety record. Only then may T-G4-06 execute and M004 measurement proceed.

END F3 FINAL ENGINEERING PACKAGE.