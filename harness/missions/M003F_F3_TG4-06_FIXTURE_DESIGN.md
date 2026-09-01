# M003F F3 / T-G4-06 FAULT-INJECTION FIXTURE DESIGN

- Mission: M003F — F3 / T-G4-06 Fault-Injection Fixture Design
- Date: 2026-08-15
- Status: COMPLETE (engineering design only — no physical measurements, no E6 fabrication, no T-G4-06/M004 authorization, no G4 closure, no architecture modification)

## Executive Status

M003E established that no F3 fixture schematic exists. M003F produces the minimum physical F3 fixture design for T-G4-06 from the existing G4 protocol, test matrix, execution sequence, E6 template, protocol audit, closure evidence plan, and the verified manufacturer bounds (EV-45, EV-47/EV-47b/EV-48). The RX50 schematic net register is EMPTY and architecture NOT LOCKED, so every fault-path element is fixture-only — **no architecture change is required**.

**Fault-definition verdict: FUNCTIONAL FAULT DEFINITION DERIVED (not blocked); electrical injection level is an operator TEST VALUE, NOT invented.** The protocol defines the fault mechanism (short/force a source channel, read victims, current-limited) and the bound (≤ ±5 mA). It does NOT specify the injection voltage/current level — that is a recorded operator TEST VALUE per the owner's delegation (decision sheet 1.3; start pack TASK 2), exactly as M003E D-02 mandates. M003F does NOT assume a resistor value from the 5 mA bound.

**T-G4-06 remains BLOCKED. M004 remains NOT AUTHORIZED.** This design is the engineering basis for the subsequent `M004 PRE-RUN PHYSICAL VERIFICATION` mission (select element, verify worst-case current, physically verify, record E6 CURRENT_LIMIT) — the harness cannot fabricate that verification.

## 1. Source-of-truth inventory

| Item | Location | Status |
|---|---|---|
| T-G4-06 definition | RX50_G4_MEASUREMENT_EXECUTION_PROTOCOL.md §14 | COMPLETE (ASSIMILATION/ASSUMPTION markers) |
| T-G4-06 test matrix | RX50_G4_TEST_MATRIX.md row T-G4-06 | COMPLETE |
| Execution sequence | RX50_G4_EXECUTION_SEQUENCE.md §1.5 (A-07), §4.6, §10.2 | COMPLETE |
| E6 template | RX50_G4_RAW_DATA_TEMPLATES.md E6 | COMPLETE (CURRENT_LIMIT mandatory) |
| Protocol audit A-07 | RX50_G4_PROTOCOL_AUDIT.md | COMPLETE |
| Closure evidence plan T-G4-06 | RX50_G4_CLOSURE_EVIDENCE_PLAN.md §T-G4-06 | COMPLETE |
| Owner decisions | M003A/M003B/M003C/M003D/M003E; decision sheet 1.1/1.2/1.3; start pack 2026-08-15 | COMPLETE |
| RX50 schematic state | NET_REGISTER (EMPTY), ARCHITECTURE_LOCK (NOT LOCKED), SHEET_DEFINITION (BLOCKED), RELEASE_GATE (NOT RELEASED) | COMPLETE (all EMPTY/BLOCKED) |
| Current-limit safety record | measurements/T-G4-06_CURRENT_LIMIT_SAFETY_RECORD.md | NOT VERIFIED / INCOMPLETE |
| Component evidence (fault path) | EVIDENCE_REGISTER EV-45/EV-47/EV-47b/EV-48 | VERIFIED |

## 2. First task — define the fault

### Fault definition (from protocol §14 + test matrix + E6 + closure plan)

| Item | Determination | Source | Status |
|---|---|---|---|
| Fault source | A controlled fault (short or force) applied to a SOURCE_CH node in the CD4067B network | protocol §14 (short/force per approved fixture condition); E6 FAULT_TYPE | DERIVED — mechanism defined; electrical level = operator TEST VALUE |
| Fault victim | Other channels read out (VICTIM_CH) to observe blast radius | protocol §14; E6 VICTIM_CH | DERIVED |
| Source voltage | Not specified numerically; bounded by verified abs-max (VIN ≤ 4.0 V on ADC path, EV-48; fault current ≤ ±5 mA, EV-47) | M003B ADC-pin stress check; D-03 Option B (M003E) | BOUNDED — level = operator TEST VALUE (not invented) |
| Victim node | Per-population: same-MUX group, cross-MUX group, shared node (Option B) | protocol §14 populations; E6 POPULATION | DERIVED |
| Injection direction | Fault injected into the source channel node; victims read on their node; fault injection LAST (execution sequence §4.6) | execution sequence | DERIVED |
| Normal state | All channels at expected state (EXPECTED_STATE) | E6 EXPECTED_STATE | DERIVED |
| Fault state | SOURCE_CH shorted or forced through the current-limited path; victims measured (MEASURED_STATE) | E6 FAULT_TYPE short/force | DERIVED |
| Expected observation | DELTA = MEASURED_STATE − EXPECTED_STATE per (source, victim); blast radius | calculation rules F6 | DERIVED |
| Measurement node | Victim channel node via DMM/ADC readout; scope node for T-G4-04 | protocol §7, §14; E6 | DERIVED |
| Required recovery | Remove fault-injection connections first; power down; disconnect ADC pin loads | execution sequence §10.2-3 | DERIVED |

### Fault definition verdict

`FUNCTIONAL FAULT DEFINITION DERIVED` — NOT blocked. The protocol defines WHAT T-G4-06 tests (cross-channel isolation blast radius via current-limited short/force of a source channel) and the governing bound (≤ ±5 mA). The electrical injection level (voltage/current applied) is intentionally an OWNER/OPERATOR TEST VALUE recorded per trial, per decision sheet 1.3 and start pack TASK 2. M003F does NOT invent a fault level.

`FAULT DEFINITION BLOCKED` is NOT declared because the ambiguity that remains (exact injection level) is explicitly a recorded TEST VALUE in the existing framework, not an undefined test objective.

## 3. Identify the real RX50 path

### Element classification

| Element | Existing RX50 hardware | Fixture-only | Proposed | Basis |
|---|---|---|---|---|
| Fault source (bench PSU/source or short strap) | NO | YES | fixture bench instrument | no RX50 net exists (net register EMPTY) |
| Current limiter | NO | YES (mandatory A-07) | fixture element, value = operator TEST VALUE | execution sequence §1.5 |
| Fault injection node (SOURCE_CH terminal) | NO | YES | fixture test point on DUT network | no schematic; F3 conceptual (protocol §7) |
| DUT CD4067B network | NO (not part of RX50 product net; DUT under test) | YES | DUT = test article | protocol §7; start pack 1.5 (single DUT) |
| Victim read node | NO | YES | fixture measurement point | protocol §7, §14 |
| STM32 ADC observation path | NO (F2 is a standalone board; ADC path used for readout) | YES (F2 board in F3 combined node) | observation instrument | protocol §7; M003A F3 description |
| Node termination / Z_effective | NO | YES | operator TEST VALUE (recorded) | start pack TASK 2 |

**No element is part of existing RX50 hardware** (net register EMPTY, sheet definition BLOCKED, architecture NOT LOCKED). The fault is generated entirely within F3 → **FIXTURE-ONLY implementation, NO ARCHITECTURE CHANGE REQUIRED**. No component is silently added to RX50.

## 4. F3 topology (minimum fixture for T-G4-06)

### Textual schematic

```text
FAULT SOURCE (bench PSU / source; short strap; level = operator TEST VALUE)
    |
    |
CURRENT LIMITER (mandatory, series, in fault-injection path; value = operator TEST VALUE;
                 worst-case current verified ≤ ±5 mA; element physically verified pre-run)
    |
    |
FAULT INJECTION NODE (SOURCE_CH terminal on the DUT CD4067B network)
    |
    |
DUT / VICTIM (CD4067B network; victims read on their node via DMM/ADC; scope node shared with T-G4-04)
```

### Node and interface requirements

| Node | Requirement | Basis |
|---|---|---|
| FAULT SOURCE | bench source able to apply short or force; level recorded per trial; must not exceed the verified voltage/current bounds at the ADC node | protocol §14; EV-48 |
| CURRENT LIMITER | series element in the fault path; worst-case current into the fault node ≤ ±5 mA (governing EV-47); ΣIINJ budget ±25 mA respected; element identified, installed, physically verified, recorded in E6 CURRENT_LIMIT + safety record | execution sequence §1.5; M003B; M003E D-02 |
| FAULT INJECTION NODE | test point on the source channel terminal; fault injection LAST (after T-G4-05/T-G4-04) | execution sequence §4.6 |
| VICTIM READ NODE | DMM/ADC readout of victim channel state; populations same-MUX / cross-MUX / shared-node | protocol §14 |
| ADC OBSERVATION | per D-03 Option B: 5 V-referenced sense node NOT connected directly to STM32 ADC; ADC observations requiring valid STM32 range performed under an appropriate supply/test condition | M003E D-03; execution sequence §5.3 |
| RECOVERY | fault-injection connections removed FIRST; supplies then down; ADC loads disconnected | execution sequence §10.2-3 |

### Current-limit element constraint (no value assumed)

- The governing bound is **|I_fault| ≤ ±5 mA** (min of STM32 IINJ(PIN) ±5 mA, EV-47, vs CD4067 IS/ID ±20 mA, EV-45). ΣIINJ ±25 mA aggregate cap (EV-47b).
- M003F does NOT select a resistor value (e.g., it does NOT assume "5 V / 5 mA → 1 kΩ"). Per M003E D-02, the element is selected from the ACTUAL F3 fault path by the operator, worst-case current is verified against the bound, and the element is physically verified pre-run.
- The design provides the verification constraint, not the value: worst-case fault current = (source voltage − node voltage) / element impedance, must be ≤ ±5 mA across the chosen fault level; measured with the DMM, recorded in E6 CURRENT_LIMIT.

### Safety/protection design

- Fault injection is LAST in the sequence to protect the fixture (execution sequence §4.6).
- The current-limit element is the ONLY protection mechanism; per M003B, board-level protection is NOT demonstrated by the repository — the operator's physical verification is the evidence that establishes it.
- 5 V-condition runs follow D-03 Option B: no 5 V-referenced sense node on the STM32 ADC pin.

## Component evidence on the proposed fault path

| Device | Role | Verified value | Evidence |
|---|---|---|---|
| STM32F103C8T6 (ADC pin) | victim read / ADC observation | IINJ(PIN) ±5 mA; ΣIINJ ±25 mA; VIN non-FT ≤ 4.0 V | EV-47, EV-47b, EV-48 (DS5319) |
| CD4067B (DUT network) | DUT / fault path switch | IS/ID ±20 mA abs / ±10 mA rec; ISEL/IEN ±30 mA | EV-45 (SCHS052D Rev D) |
| Current limiter (fixture) | fault-path protection | value = operator TEST VALUE (none selected; not invented) | M003E D-02; safety record NOT VERIFIED |
| Fault source (bench) | injection | level = operator TEST VALUE (none selected) | decision sheet 1.3; start pack TASK 2 |

No component ratings are invented. No part number is selected for the current limiter (source unavailable for a specific fixture element; selection deferred to operator physical verification).

## E6 / safety-record traceability

- E6 `CURRENT_LIMIT` is MANDATORY for all fault injection (RX50_G4_RAW_DATA_TEMPLATES.md E6); 0 rows ingested.
- Closure engine item 6 (isolation blast-radius evidence) MEASUREMENT PENDING.
- measurements/T-G4-06_CURRENT_LIMIT_SAFETY_RECORD.md: NOT VERIFIED / INCOMPLETE — to be completed by the operator with the actual element identity, nominal value, measured value, method, instrument, fixture, date, operator, calculated max current, applicable limits, pass/fail.

## Gate status

- **T-G4-06: BLOCKED** (current-limit element + physical verification + E6 evidence absent).
- **M004: NOT AUTHORIZED** (design only; no measurement authorization).
- **G4: BLOCKED / MEASUREMENT PENDING** (0 rows; not closed).
- **C-20b: OPEN** (architecture decision, unchanged).
- **RX50 architecture: UNCHANGED** (net register EMPTY; architecture NOT LOCKED).

## Remaining physical actions (operator/owner)

1. Build F3 at topology level (per this design; owner approved F1/F2/F3 build).
2. Construct/identify the actual fault-injection path; select the current-limit element.
3. Verify worst-case fault current ≤ ±5 mA against the actual path; physically verify the installed element.
4. Record element + verification in E6 CURRENT_LIMIT and complete the safety record.
5. Only then permit T-G4-06 execution (and subsequent M004 measurement authorization).

## Final Gate

- **FAULT DEFINITION**: DERIVED (functional); electrical injection level = operator TEST VALUE (not invented).
- **ARCHITECTURE CHANGE**: NONE REQUIRED (fixture-only).
- **T-G4-06**: BLOCKED (pending physical current-limit verification).
- **M004**: NOT AUTHORIZED.
- **NEXT MISSION**: `M004 PRE-RUN PHYSICAL VERIFICATION` — build/identify the F3 fault path, select and physically verify the current-limit element, verify worst-case current ≤ ±5 mA, record E6 CURRENT_LIMIT + complete the safety record. This is NOT the measurement mission and must not be executed automatically.

END MISSION M003F.