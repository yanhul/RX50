# M003G F3 ELECTRICAL SPECIFICATION / BUILD SHEET

- Mission: M003G — F3 Electrical Specification / Build Sheet
- Date: 2026-08-15
- Status: COMPLETE (specification audit — no physical build, no measurements, no fabrication of missing requirements, no T-G4-06/M004 authorization, no architecture change)

## Executive Status

M003F produced a conceptual F3 fixture (textual topology + current-limit constraint) without selecting any electrical value. M003G converts that concept into a buildability test. **Result: F3 is NOT buildable from the repository alone — an operator would be forced to guess safety-critical connections. The deliverable of this mission is the precise list of unresolved requirements (option 2 of the brief), NOT a completed build sheet.** No value is invented to mask a gap.

What IS specified: the fault is functionally defined (short/force a source channel, read victims, current-limited), the safety limit is verified (|I_fault| ≤ ±5 mA, EV-47 governing), the current-limit element is MANDATORY (A-07 / execution sequence §1.5), fault injection is LAST (§4.6) and removed FIRST on shutdown (§10.2), and the 5 V sense node must not reach the STM32 ADC (D-03 Option B, M003E).

What is MISSING (REQUIREMENT MISSING, none invented): the **test level** (what voltage/current/stimulus), the **fault source interface** (type, terminals, polarity, max source condition), the **short reference** (short to what), the **return path** for fault current, the **injection connection/disconnection mechanism**, and the **current measurement point**.

**T-G4-06 remains BLOCKED. M004 remains NOT AUTHORIZED.**

## 1. Source-of-truth inventory

| Item | Location | Status |
|---|---|---|
| M003E owner decisions (D-01/D-02/D-03) | harness/missions/M003E_G4_OWNER_DECISION_RECORDING.md | COMPLETE |
| M003F fixture design | harness/missions/M003F_F3_TG4-06_FIXTURE_DESIGN.md | COMPLETE |
| T-G4-06 protocol | RX50_G4_MEASUREMENT_EXECUTION_PROTOCOL.md §14 | COMPLETE |
| G4 test matrix | RX50_G4_TEST_MATRIX.md row T-G4-06 | COMPLETE |
| G4 execution sequence | RX50_G4_EXECUTION_SEQUENCE.md §1.5 (A-07), §4.6, §5.3, §10.2 | COMPLETE |
| E6 raw-data template | RX50_G4_RAW_DATA_TEMPLATES.md E6 | COMPLETE (FAULT_TYPE short/force; CURRENT_LIMIT mandatory) |
| G4 closure evidence plan | RX50_G4_CLOSURE_EVIDENCE_PLAN.md §T-G4-06 | COMPLETE |
| Protocol audit (A-07) | RX50_G4_PROTOCOL_AUDIT.md A-07 | COMPLETE |
| EVIDENCE_REGISTER | evidence/EVIDENCE_REGISTER.md (EV-45/47/47b/48/49) | VERIFIED |
| DECISION_REGISTER | decisions/DECISION_REGISTER.md (D-22/23/24) | COMPLETE |
| OPEN_ISSUES | open_issues/OPEN_ISSUES.md (OI-21/22) | COMPLETE |
| CONTRADICTION_REGISTER | harness/state/CONTRADICTION_REGISTER.md (C-20b/22) | COMPLETE |
| Schematic net register | RX50_SCHEMATIC_NET_REGISTER.md | EMPTY / BLOCKED |
| Architecture documents | RX50_SCHEMATIC_ARCHITECTURE_LOCK.md (+ SHEET_DEFINITION, RELEASE_GATE) | NOT LOCKED / BLOCKED / NOT RELEASED |
| F1/F2/F3 build documentation | none exists beyond protocol §7 topology + M003F | ABSENT (no build sheet anywhere) |

## 2. Buildability test

Test applied per connection: WHAT connects? / TO WHAT? / THROUGH WHAT? / UNDER WHAT CONDITION? / WHAT IS THE RETURN PATH? / HOW IS IT DISCONNECTED?

| Net / Node | From | To | Series element | Switch/state | Return | Evidence | Status |
|---|---|---|---|---|---|---|---|
| VDD supply | bench PSU (3.3 V / 5 V set-points) | CD4067B VDD + DUT rail | none | PSU output ON | PSU return → VSS (common) | protocol §6/§7; execution seq. §2.1 | SPECIFIED (set-points; value = 3.3/5 V) |
| VDDA supply | bench PSU (3.3 V) | STM32F103 VDDA | none | PSU output ON | PSU return → VSS | protocol §7 | SPECIFIED |
| VSS / ground | PSU return | CD4067 VSS, STM32 VSS, fixture common | none | hard connection | common star ground | protocol §7; execution seq. §3.1 | SPECIFIED (functional; physical layout = operator build detail) |
| Address/INH control | STM32 GPIO OR controlled function generator | CD4067 A/B/C/D, INH | none | GPIO / generator state (slew+levels recorded for T-G4-02) | driver → GND | protocol §7, §10; execution seq. §3.2 | SPECIFIED (driver set allowed; levels recorded) |
| ADC observation | CD4067 common (X) or channel (Y) node | STM32 ADC pin (e.g. PA0) | none (direct sense) | fixed sense path | ADC internal → VSS | protocol §7; D-03 Option B (M003E) | SPECIFIED for 3.3 V; 5 V runs constrained (5 V-referenced sense node NOT connected directly to ADC) |
| Scope probe | ADC node | oscilloscope | probe input capacitance C_in (recorded, low-C) | probe connect | probe ground → fixture ground | protocol §7; E4; execution seq. §1.6 (A-04) | SPECIFIED |
| Node termination (shared T-G4-05) | node | termination reference | Z_effective (known/recorded TEST VALUE) | hard or removable | termination reference node (NOT explicitly defined) | test matrix T-G4-05; start pack TASK 2 | PROPOSED — reference node for termination not explicitly specified |
| **Fault-injection path** | FAULT SOURCE (type unspecified) | SOURCE_CH terminal on DUT CD4067B network | CURRENT-LIMIT ELEMENT (mandatory; value/type = TEST VALUE, none selected) | injection connection mechanism UNSPECIFIED (manual/relay/plug) | **REQUIREMENT MISSING** | protocol §14, §8; A-07; execution seq. §1.5/§4.6/§10.2; M003F | **BLOCKED / REQUIREMENT MISSING** |

### Buildability verdict

**F3 is NOT buildable as specified.** The fault-injection path (row 8) is safety-critical (it determines fault current into the ADC node) and its source interface, short reference, return path, connection mechanism, and current measurement point are unspecified. An operator building F3 today would have to guess all of these. Per the brief, this mission therefore delivers the unresolved-requirements list (section 6) rather than a build sheet.

## 3. T-G4-06 fault condition (three items, kept separate)

### 3.1 Functional requirement

What electrical fault must be created? **A controlled fault applied to a selected source channel (SOURCE_CH) in the CD4067B network, per FAULT_TYPE ∈ {short, force}, then other channels (VICTIM_CH) are read to determine the blast radius.** Populations: same-MUX / cross-MUX / shared-node. (protocol §14; test matrix T-G4-06; E6 FAULT_TYPE; closure plan §T-G4-06 "short one channel; read neighboring/other channels").

- Specified: functional mechanism, victim set, populations, per-(source,victim) ≥ 3 trials. STATUS: DERIVED.

### 3.2 Test level

What voltage/current/stimulus is required? **NOT SPECIFIED.** The protocol (§14) requires "force/short/terminate it per the approved fixture condition" — no approved fixture condition exists in the repository. For a "force": no voltage or current magnitude is given. For a "short": no reference (short to VSS? VDD? another channel?) is given. For "terminate": no termination impedance is given. E6 FAULT_TYPE lists the mechanisms but not their levels. M003F deliberately did not invent a level; M003G records the gap instead.

**`TEST LEVEL REQUIREMENT MISSING`**

### 3.3 Safety limit

Maximum permitted fault current: **|I_fault| ≤ ±5 mA** (governing = STM32F103 IINJ(PIN) ±5 mA, EV-47, tighter than CD4067 IS/ID ±20 mA abs / ±10 mA rec, EV-45). Aggregate cap ΣIINJ(PIN) ±25 mA (EV-47b). ADC-node voltage must stay within VIN abs max VSS−0.3..4.0 V (EV-48). Current-limit element is MANDATORY (A-07; execution sequence §1.5); value recorded in E6 CURRENT_LIMIT. STATUS: VERIFIED (bounds) — element value pending physical verification (D-02, M003E).

### 3.4 Separation statement

The three are distinct and NOT merged: functional fault (defined) ≠ test level (MISSING) ≠ safety limit (verified bound). The safety limit is a ceiling, not a test level — the harness will not treat ≤ ±5 mA as "the" stimulus.

## 4. Fault source

### 4.1 Source type

The protocol (§14) and E6 permit multiple mechanisms: **force / short / terminate**. No single source type is pinned. The harness preserves this flexibility. **Recommendation only (not a spec):** a bench source able to apply a short and a low-voltage force, used in series with the mandatory current-limit element. This is a proposal; the actual type selection is an operator/owner decision recorded as a TEST VALUE.

### 4.2 Interface specification

| Item | Determination | Status |
|---|---|---|
| Source type | force / short / terminate all permitted; none pinned | MULTIPLE METHODS PERMITTED (recommendation only) |
| Source terminals | not defined anywhere | `REQUIREMENT MISSING` |
| Polarity | not defined (fault can be to VSS or VDD; not specified) | `REQUIREMENT MISSING` |
| Return | return path for fault current not defined (VSS? PSU return? separate?) | `REQUIREMENT MISSING` |
| Connection sequence | order constraint only: fault injection LAST (§4.6); removed FIRST on shutdown (§10.2) | PARTIAL — sequence constraint SPECIFIED; electrical connect sequence REQUIREMENT MISSING |
| Max allowed source condition | bounded by safety limit (≤ ±5 mA at fault node; ADC node ≤ 4.0 V, EV-48) | BOUNDED (limit verified) — exact max source setting = TEST VALUE |
| Measurement point | where fault current is measured/verified (series current read vs computed) | `REQUIREMENT MISSING` |

No item is invented. Anything unsupported is marked `REQUIREMENT MISSING`.

## 5. Current-limit path (electrical requirement trace)

```text
SOURCE
  ↓
CURRENT LIMITER          (MANDATORY, series; worst-case |I| ≤ ±5 mA; value/type = TEST VALUE; E6 CURRENT_LIMIT recorded)
  ↓
INJECTION SWITCH / CONNECTION   (mechanism UNSPECIFIED — how the fault connects to SOURCE_CH and is disconnected)
  ↓
SOURCE_CH                (source channel terminal on DUT CD4067B network; fault injected here)
  ↓
DUT                      (CD4067B, single unit — decision 1.5; victims read on their node)
  ↓
RETURN                   (REQUIREMENT MISSING — return path for fault current not defined)
```

### Trace items

| Element | Requirement | Evidence | Status |
|---|---|---|---|
| SOURCE | must apply short or force; level recorded per trial; must not drive fault node above the verified bounds | protocol §14; EV-47/48 | INTERFACE REQUIREMENT MISSING (§4.2) |
| CURRENT LIMITER | MANDATORY series element; ensures worst-case |I_fault| ≤ ±5 mA (EV-47) and ΣIINJ ≤ ±25 mA (EV-47b); element identified, installed, physically verified pre-run, recorded in E6 CURRENT_LIMIT + safety record; type/value = operator/owner TEST VALUE (none selected) | A-07; execution seq. §1.5; M003B; M003E D-02 | MANDATORY (mechanism) — VALUE/TYPE = TEST VALUE (pending physical selection) |
| INJECTION SWITCH / CONNECTION | must allow safe connect AND disconnect (removed FIRST at shutdown §10.2); mechanism (manual removable, relay, plug) unspecified | execution seq. §10.2 | `REQUIREMENT MISSING` |
| SOURCE_CH | test point on the source channel terminal of the DUT network | test matrix T-G4-06; M003F | SPECIFIED (functionally) |
| DUT | single CD4067B unit; victims read on their node | decision 1.5; protocol §14 | SPECIFIED |
| RETURN | return path for fault current (to VSS / PSU return / separate node) | — | `REQUIREMENT MISSING` |

### Electrical requirement imposed by M003G (no value invented)

1. The current-limit element MUST limit worst-case fault current into the fault node to **≤ ±5 mA** and respect **ΣIINJ ≤ ±25 mA** (EV-47/EV-47b).
2. The fault node voltage must remain within **VSS−0.3 .. 4.0 V** at the STM32 ADC pin (EV-48); for 5 V-condition runs the 5 V-referenced sense node is NOT connected directly to the ADC (D-03 Option B).
3. The element value/type is an operator/owner TEST VALUE to be physically verified and recorded; M003G does NOT compute or select it.
4. Fault injection is connected LAST and disconnected FIRST (execution sequence §4.6 / §10.2).

## 6. Unresolved requirements that prevent buildability (deliverable)

An operator CANNOT build F3 without guessing these. Each is a recorded gap, not a hidden value.

| # | Missing requirement | Safety-critical? | Blocks | Current status |
|---|---|---|---|---|
| 1 | T-G4-06 **test level** (force voltage/current magnitude; short reference; terminate impedance) | YES (defines stimulus magnitude) | §3.2 `TEST LEVEL REQUIREMENT MISSING` | OWNER/OPERATOR TEST VALUE — must be supplied or recorded |
| 2 | **Fault source interface**: source type selection, terminals, polarity, max source condition | YES | §4.2 `REQUIREMENT MISSING` | operator/owner selection + recording |
| 3 | **Short reference** (short to VSS / VDD / other channel) | YES | §3.2, §4.2 `REQUIREMENT MISSING` | operator/owner selection + recording |
| 4 | **Return path** for fault current | YES | §5 `REQUIREMENT MISSING` | must be defined (e.g., to VSS common) by operator/owner |
| 5 | **Injection connection/disconnection mechanism** | YES | §5 `REQUIREMENT MISSING` | mechanism must be defined so §10.2 (remove FIRST) is executable |
| 6 | **Current measurement point** (where |I_fault| is verified) | YES | §4.2 `REQUIREMENT MISSING` | must be defined to support E6 CURRENT_LIMIT |
| 7 | **Current-limit element type + value** | YES | §5 (mandatory element, value pending) | operator/owner TEST VALUE; physical verification pending (D-02) |
| 8 | Node-termination reference node for shared T-G4-05 (adjacent to T-G4-06 scope) | NO (characterization) | §2 row 7 PROPOSED | operator/owner TEST VALUE |

These eight items are the minimum that must be supplied/recorded before F3 is buildable without guessing. They remain in the ownership of the operator/owner per decision sheet 1.2/1.3 and M003E D-02; the harness does not and must not fill them.

## Gate status

- **T-G4-06: BLOCKED** (test level + source interface + return + element verification all missing).
- **M004: NOT AUTHORIZED** (no measurement authorization; spec audit only).
- **G4: BLOCKED / MEASUREMENT PENDING**.
- **C-20b: OPEN** (architecture, unchanged).
- **RX50 architecture: UNCHANGED** (net register EMPTY; architecture NOT LOCKED). F3 remains fixture-only; no ARCHITECTURE CHANGE REQUIRED.

## Recommended next action

The harness has now produced: M003F (conceptual fixture + constraints) and M003G (buildability audit + the exact list of gaps). The remaining gaps are operator/owner physical + value decisions, which the harness cannot make or fabricate. The natural next mission is the planned `M004 PRE-RUN PHYSICAL VERIFICATION`, executed by the operator: (1) supply/record items 1–8 of section 6, (2) build F3, (3) physically verify the current-limit element and worst-case current ≤ ±5 mA, (4) record E6 CURRENT_LIMIT + complete the safety record. That mission is operator-executed and must NOT be run automatically by the harness.

## Final Gate

- **BUILDABILITY**: F3 NOT buildable without operator/owner TEST VALUE selection for items 1–8 (section 6).
- **TEST LEVEL**: `TEST LEVEL REQUIREMENT MISSING` (recorded, not invented).
- **FAULT SOURCE INTERFACE**: `REQUIREMENT MISSING` (type/terminals/polarity/return/measurement point).
- **SAFETY LIMIT**: VERIFIED (|I_fault| ≤ ±5 mA, EV-47; ΣIINJ ≤ ±25 mA; ADC VIN ≤ 4.0 V, EV-48).
- **ARCHITECTURE CHANGE**: NONE REQUIRED (fixture-only).
- **T-G4-06**: BLOCKED. **M004**: NOT AUTHORIZED.
- **NEXT**: `M004 PRE-RUN PHYSICAL VERIFICATION` (operator-executed; supply items 1–8, build F3, verify current-limit element, record E6 CURRENT_LIMIT). Do not execute automatically.

END MISSION M003G.