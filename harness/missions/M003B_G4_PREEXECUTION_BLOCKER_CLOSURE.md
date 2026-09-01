# M003B G4 PRE-EXECUTION BLOCKER CLOSURE

- Mission: M003B — G4 Pre-Execution Blocker Closure
- Date: 2026-08-15
- Status: COMPLETE
- Result: FINDINGS ONLY (no measurements fabricated, no closure declared, no test executed, no design/schematic/PCB/BOM/firmware change, no G4 or G5 lock)

## Executive Status

M003A left three pre-execution blockers:

1. **EV-45 — CD4067B absolute-max current row** `NEEDS RECHECK` (bounds ITEST for T-G4-01).
2. **EV-44 / DS5319 ADC-pin absolute-max row** `NEEDS RECHECK` (bounds the T-G4-06 fault-injection current limit).
3. **T-G4-06 fault-injection current limit** `BLOCKED — CURRENT LIMIT NOT VERIFIED` (element value + verification record absent).
4. Minor: **T-G4-04 waveform file-naming scheme** undefined.

M003B resolved the datasheet-bound blockers from official manufacturer sources (TI SCHS052D Rev D for CD4067B; ST DS5319 Rev 19/20 for STM32F103x8/xB). All governing absolute-max bounds are now **VERIFIED**:

- CD4067B source/drain continuous current IS/ID: **abs max ±20 mA**; recommended operating **±10 mA** (SCHS052D Rev D, Absolute Maximum Ratings / Recommended Operating Conditions).
- STM32F103 **IINJ(PIN) ±5 mA** (any non-FT pin, abs max), **ΣIINJ(PIN) ±25 mA** (DS5319 Table 7, Rev 19/20).
- STM32F103 **VIN abs max on non-5V-tolerant pins = VSS−0.3 to 4.0 V** (DS5319 Table 6, Rev 18/19 text verified).

Consequently the T-G4-06 fault-injection bound is **≤ ±5 mA** (ADC pin governs, being tighter than CD4067 IS/ID ±20 mA). The `BLOCKED — CURRENT LIMIT NOT VERIFIED` label is removed for the **bound**; what remains is a recorded, mandatory pre-run **operator action** (owner decision sheet 1.3): select the current-limit element value within the verified bound, physically verify it, and record it before T-G4-06. The overall readiness gate is therefore **READY WITH OWNER DECISION** (the two owner decisions are the T-G4-04 naming convention approval and the 5V-fault routing decision; test values remain operator-authorized TEST VALUEs).

## Current RX50 G4 State

- G4 gate: `CLOSURE BLOCKED — REQUIRED RAW EVIDENCE NOT PRESENT` (M002; unchanged — raw evidence still does not exist).
- Measurement readiness (M003A): was `NOT READY` on three procedural gaps (EV-45 unverified, ADC-pin abs-max unverified, T-G4-06 current limit unverified) + minor waveform-naming gap. M003B closes the three datasheet-bound gaps and supplies a naming proposal.
- Owner decisions (start pack 2026-08-15): F1/F2/F3 build APPROVED; ambient only; single DUT; operator-authorized TEST VALUEs; Group-2 thresholds declined → characterization-only; T-G4-06 current limit MUST be verified BEFORE execution.

## B-01 — ITEST governing limit (T-G4-01)

### Status: RESOLVED (bound VERIFIED; value = operator TEST VALUE action)

**Evidence (hierarchy level 3 — manufacturer datasheet):**

| Item | Value | Source |
|---|---|---|
| CD4067B IS/ID source/drain continuous current — ABSOLUTE MAX | **±20 mA** | TI SCHS052D Rev D, Absolute Maximum Ratings |
| CD4067B IS/ID source/drain continuous current — RECOMMENDED OPERATING | **±10 mA** | TI SCHS052D Rev D, Recommended Operating Conditions |
| CD4067B ISEL/IEN logic control input pin current — ABSOLUTE MAX | ±30 mA | TI SCHS052D Rev D, Absolute Maximum Ratings |
| CD4067B VS/VD source/drain voltage — ABSOLUTE MAX | VSS−0.5 to VDD+0.5 V | TI SCHS052D Rev D, Absolute Maximum Ratings |
| CD4067B VDD−VSS supply — ABSOLUTE MAX | −0.5 to 20 V | TI SCHS052D Rev D, Absolute Maximum Ratings |
| CD4067B VDD−VSS supply — RECOMMENDED OPERATING | 3 to 18 V | TI SCHS052D Rev D, Recommended Operating Conditions |

ITEST is a DC/continuous current through a selected channel (Sx→D). The governing absolute-max bound is **±20 mA** (IS/ID); to stay within recommended operating conditions use **≤ ±10 mA**. The concrete ITEST value remains an **operator-selected TEST VALUE** (owner decision sheet 1.3), to be chosen within the verified bounds and recorded per trial in E1.

**M003A linkage:** the `NEEDS RECHECK` on EV-45 is cleared (see Evidence Added). T-G4-01 readiness upgrades from `READY WITH MISSING PROCEDURAL DETAIL` to `READY` (bound verified; value = recorded operator action).

## B-02 — T-G4-06 current limit (fault-injection path)

### Status: BOUND VERIFIED (≤ ±5 mA); element value + physical verification = mandatory pre-run operator action

**Governing absolute-max bounds (hierarchy level 3):**

| Limit | Value | Source | Role |
|---|---|---|---|
| STM32F103 IINJ(PIN) on ADC pins (non-FT) — abs max | **±5 mA** | DS5319 Table 7 | **GOVERNING (tighter)** |
| STM32F103 ΣIINJ(PIN) total — abs max | ±25 mA | DS5319 Table 7 | aggregate budget |
| CD4067B IS/ID source/drain current — abs max | ±20 mA | SCHS052D Rev D | channel path |
| STM32F103 VIN on non-FT pin — abs max | VSS−0.3 to 4.0 V | DS5319 Table 6 | ADC-pin voltage stress |

**Derived bound (hierarchy level 5):** the fault-injection current into the ADC node/pin must be **≤ ±5 mA** (min of the two absolute-max values: MCU IINJ(PIN) ±5 mA vs CD4067 IS/ID ±20 mA). ΣIINJ(PIN) ±25 mA is the aggregate cap if multiple pins are simultaneously injected.

**What M003B does NOT declare:** M003B does not select the physical current-limit element value. Per owner decision sheet 1.3 and the mandatory pre-run gate (owner record: "MUST be verified BEFORE T-G4-06"), the operator must:

1. Select the current-limit element value ≤ ±5 mA (derived bound above).
2. Physically verify the element in the F3 fault-injection path.
3. Record value + verification (E6 `CURRENT_LIMIT` field; closure engine item 6).

The `BLOCKED — CURRENT LIMIT NOT VERIFIED` label applied to the **bound** is removed; the same label remains **in force for execution** until the operator's verification record exists. Execution of T-G4-06 is NOT authorized by M003B.

**ADC accuracy interaction (DS5319 §5.3.12/5.3.13):** positive injection within IINJ(PIN)/ΣIINJ(PIN) limits does not affect ADC accuracy; negative injection on analog pins reduces accuracy and is to be avoided. This is recorded as a characterization constraint, not resolved as a pass/fail criterion.

## ADC-Pin Stress Check (F3 path; T-G4-05 / T-G4-06)

### Status: LIMITS VERIFIED; PATH PROTECTION = OPERATOR-VERIFIED PRE-RUN (mandatory)

- ADC pins PA0–PA7 on STM32F103C8T6 are **standard (non-5V-tolerant)** pins: abs max VIN = VSS−0.3 to **4.0 V**; IINJ(PIN) = **±5 mA**; ΣIINJ(PIN) = **±25 mA**.
- The F3 fixture's current-limit element is the protection mechanism; the repository has no schematic/PCB and no recorded element value, so **board-level protection is NOT demonstrated by the repo**. M003B therefore does NOT claim the ADC is protected by the fixture — the operator's physical verification (mandatory pre-run) is the evidence that will establish it.
- **5V-path interaction (flagged, not resolved):** any 5 V-level fault forced directly onto an ADC pin would exceed the verified VIN abs max of 4.0 V. 5V-path fault scenarios (T-G4-05 VDD=5 V; T-G4-06 source forcing) must keep the ADC node within VIN; this is the same architectural surface as contradiction C-20b (5 V control path) and is logged below.

## SCHS052D Check (TI CD4067B)

Verified from the official TI product page (www.ti.com/lit/gpn/CD4067B; SCHS052D Rev D, published 2003, revised Aug 2024):

| Parameter | Value | Section |
|---|---|---|
| ISEL or IEN — logic control input pin current (EN, Ax, SELx) | −30 to 30 mA | Absolute Maximum Ratings |
| VS or VD — source or drain voltage (Sx, D) | VSS−0.5 to VDD+0.5 V | Absolute Maximum Ratings |
| **IS or ID (CONT) — source or drain continuous current (Sx, D)** | **−20 to 20 mA** | **Absolute Maximum Ratings** |
| VDD − VSS supply | −0.5 to 20 V | Absolute Maximum Ratings |
| TJ / Tstg | 150 / −65..150 °C | Absolute Maximum Ratings |
| **IS or ID (CONT)** | **−10 to 10 mA** | **Recommended Operating Conditions** |
| VDD − VSS | 3 to 18 V | Recommended Operating Conditions |
| VS or VD | VSS to VDD | Recommended Operating Conditions |

Closes EV-45. No CD4067B value contradicts the earlier fact register rows (RON, leakage, VIH/VIL, capacitance — unchanged).

## DS5319 / MCU Check (ST STM32F103x8/xB)

Verified from ST DS5319 (Rev 18/19 text verified; Rev 20 is the currently published revision, cited in prior reports):

| Parameter | Value | Source |
|---|---|---|
| VIN input voltage, 5 V-tolerant pin | VSS−0.3 to VDD+4.0 V | Table 6 |
| VIN input voltage, any other (non-FT) pin | VSS−0.3 to 4.0 V | Table 6 |
| IIO output current sunk/source by any I/O pin | ±25 mA | Table 7 |
| **IINJ(PIN) injected current, any other pin** | **±5 mA** | **Table 7** |
| **ΣIINJ(PIN) total injected current** | **±25 mA** | **Table 7** |
| IINJ functional susceptibility, any other pin | −5/+5 mA | Table 34/35 |
| IVDD / IVSS | 150 mA | Table 7 |
| ADC accuracy: positive injection within IINJ/ΣIINJ limits | does not affect accuracy | §5.3.12/5.3.13, ADC accuracy note |
| ADC accuracy: negative injection on analog pins | reduces accuracy; avoid / Schottky recommendation | §5.3.12/5.3.13, ADC accuracy note |

Adds EV-47 (IINJ) and EV-48 (VIN non-FT). EV-44 is clarified: EV-44 in EVIDENCE_REGISTER.md is the **STM32F103 VOL exact row** (GPIO output level, drive condition) — it is NOT the ADC-pin absolute-max row; M003A referenced "EV-44" for the DS5319 ADC-pin abs-max; the correct IDs are EV-47/EV-48 (new). EV-44 remains `NEEDS RECHECK` (VOL drive-condition row only).

## T-G4-04 Waveform Naming

### Status: PROPOSED (awaiting owner approval — NOT locked)

Repository has only the `WAVEFORM_FILE` field (E4 template row 52); no file-naming convention exists anywhere. Proposed minimum convention, preserving TEST_ID, DUT_ID, channel/node, and capture sequence:

```
<TEST_ID>_<DUT_ID>_N<channel_or_node>_TR<seq>.<ext>
example: T-G4-04_DUT-001_N12_TR01.CSV
```

- `<TEST_ID>` = `T-G4-04` (stable).
- `<DUT_ID>` = DUT tag as logged in E4 (e.g., `001`).
- `N<channel_or_node>` = channel/node under test (e.g., `N12` = channel 12; `NSHARED` if shared-node capture).
- `TR<seq>` = capture sequence number within that transition (01, 02, ...).
- Original filenames are preserved on handoff per the Data Handoff Protocol; `WAVEFORM_FILE` in E4 = the exact filename.

**Exact proposed template delta (RX50_G4_RAW_DATA_TEMPLATES.md, E4 block):** add one note line after row 57:
`Waveform file naming: <TEST_ID>_<DUT_ID>_N<channel_or_node>_TR<seq>.<ext> (e.g., T-G4-04_DUT-001_N12_TR01.CSV); WAVEFORM_FILE = exact filename; original filenames preserved on handoff.`

## Evidence Added

| ID | Fact | Value | Source | Status |
|---|---|---|---|---|
| EV-45 (resolved) | CD4067B absolute-max current IS/ID (CONT) | ±20 mA abs max / ±10 mA rec. op. | TI SCHS052D Rev D | **VERIFIED** (was NEEDS RECHECK) |
| EV-47 (new) | STM32F103 IINJ(PIN) on any other pin; ΣIINJ(PIN) | ±5 mA; ±25 mA | ST DS5319 Table 7 (Rev 19/20) | VERIFIED |
| EV-48 (new) | STM32F103 VIN abs max on non-FT pins | VSS−0.3 to 4.0 V | ST DS5319 Table 6 | VERIFIED (Rev 18/19 text; see C-22) |
| EV-44 (clarified) | STM32F103 VOL exact row (GPIO output) | row not yet pinned | DS5319 GPIO char. | NEEDS RECHECK (unchanged) |

EV-30..EV-33 (measurements) remain MEASUREMENT PENDING — no raw evidence exists yet.

## Open Issues Updated

- **T-G4-06 current-limit bound** — resolved at datasheet level (≤ ±5 mA; EV-47/EV-45); new open item: **element value selection + physical verification record = operator action, mandatory pre-run** (not a datasheet gap; cannot be closed by the harness without the physical record).
- **T-G4-04 waveform naming** — proposed convention; awaiting owner approval before it is applied to the E4 template.
- **5V-path vs ADC pin VIN abs max (4.0 V)** — new interaction flagged (linked to C-20b / C-22): 5 V fault forcing onto an ADC pin would violate the verified VIN abs max; routing decision required.
- **OI-16 "G4 Evidence Retrieval"** — still absent (unchanged; evidence artifact, not execution-critical).
- **EV-44 (VOL row)** — still `NEEDS RECHECK` (unchanged).

## Contradictions Found

| ID | Conflict | Severity | Status |
|---|---|---|---|
| C-22 (new) | STM32F103 VIN on standard pins: DS5319 Rev 18/19 = max 4.0 V vs secondary render (sheetsdata) = VDD+0.3 | LOW | **CONTRADICTION DETECTED** — primary (DS5319 Rev 18/19 text) preferred; not silently resolved; pin to DS5319 Rev 20 PDF when it is resident (OI-15). Governing current limit (IINJ ±5 mA) unaffected. |
| C-20b (existing) | CD4067 5 V path: STM32 VOH 2.9 V < CD4067 VIH 3.5 V | DEFINITIVE | still RESOLUTION REQUIRED (owner) — additionally, M003B notes the 5V-fault vs ADC pin VIN 4.0 V interaction as a second face of the same 5V-path surface. |

No new contradiction changes any numeric datasheet value used in G4; the CD4067B and STM32 abs-max values are consistent across sources.

## Owner Decisions Required

1. **Approve / amend the T-G4-04 waveform naming convention** (PROPOSED above; template delta pending).
2. **5V-path fault routing decision**: how 5V-level fault/leakage scenarios keep the ADC node within the verified VIN abs max (4.0 V) — or explicitly restrict 5 V characterization to the CD4067 channel side only. Ties to C-20b.
3. (None other outstanding) Group-1 decisions are recorded; Group-2 thresholds remain declined (characterization-only). Test values (ITEST, current-limit element value, ladder, Z_effective, switch-state load) are operator-authorized TEST VALUEs per decision sheet 1.3.

## Measurement Blockers Remaining

No datasheet/evidence blocker remains. Remaining pre-run prerequisites are operator actions (owner-authorized):

1. Select + record ITEST within ±10 mA recommended (≤±20 mA abs) — T-G4-01.
2. Select current-limit element ≤ ±5 mA; physically verify in F3; record value + verification — **before T-G4-06**.
3. Build F1/F2/F3; verify instruments; record IDs/cal; fill E1-E6; attach T-G4-04 waveforms per the naming convention (once approved).

## Final Readiness Gate

| Readiness item | Status |
|---|---|
| T-G4-01 (ITEST bound) | READY (bound verified; value = operator action) |
| T-G4-02 | READY (unchanged) |
| T-G4-03 | READY (unchanged) |
| T-G4-04 | READY WITH MISSING PROCEDURAL DETAIL — naming convention proposed, awaiting owner approval |
| T-G4-05 | READY (unchanged) |
| T-G4-06 (current-limit bound) | BOUND READY — **execution still gated** on operator-selected element value + physical verification record |
| Datasheet-bound blockers (EV-45, EV-47/48) | CLOSED |
| Data ingestion | READY (unchanged) |

**OVERALL: READY WITH OWNER DECISION** — all pre-execution datasheet/evidence blockers from M003A are closed with verified manufacturer bounds; two owner decisions remain (T-G4-04 naming convention; 5V-fault/ADC-pin routing, linked C-20b). T-G4-06 must not be executed until the operator's current-limit element value + verification record exists. The project may NOT yet be called `READY FOR G4 MEASUREMENT` because the T-G4-06 current-limit value is still an unrecorded operator TEST VALUE and the two owner decisions are pending.

### VERIFIED

- CD4067B IS/ID continuous current abs max = ±20 mA; recommended operating = ±10 mA (SCHS052D Rev D). [EV-45]
- CD4067B control-input pin current abs max = ±30 mA; supply/voltage abs-max bounds (SCHS052D Rev D). [EV-45]
- STM32F103 IINJ(PIN) = ±5 mA (non-FT pins), ΣIINJ(PIN) = ±25 mA (DS5319 Table 7). [EV-47]
- STM32F103 VIN abs max on non-FT pins = VSS−0.3 to 4.0 V (DS5319 Table 6). [EV-48]
- Derived T-G4-06 fault-injection bound ≤ ±5 mA (min of EV-47 and EV-45).

### UNVERIFIED

- T-G4-04 waveform naming convention (PROPOSED; awaiting owner approval).
- T-G4-06 current-limit element value and its physical verification (operator action, mandatory pre-run).
- EV-44 (STM32F103 VOL exact drive-condition row) — still NEEDS RECHECK.
- DS5319 Rev 20 exact Table 6 wording (only Rev 18/19 text captured) — see C-22.

### OWNER DECISIONS REQUIRED

1. T-G4-04 waveform naming convention approval.
2. 5V-fault/ADC-pin VIN routing decision (link C-20b).
3. T-G4-06 current-limit element value (operator action under owner delegation 1.3).

### BLOCKED TESTS

- **T-G4-06** — execution NOT authorized until the current-limit element value is selected within ≤ ±5 mA, physically verified, and the verification record exists. (Bound itself is verified.)

### REMAINING MEASUREMENT PREREQUISITES

- Operator actions: build F1/F2/F3; verify instruments; select+record TEST VALUEs; verify+record T-G4-06 current limit; fill E1-E6; attach named waveforms; assemble the 12-item evidence package; hand back per the Data Handoff Protocol.

### NEXT MISSION

**M004 — G4 DATA ACQUISITION / INGESTION** (operator executes T-G4-01..06 in the defined order after the owner decisions above and the operator's pre-run verification; harness ingests E1-E6 as-is, runs F1-F7, logs measured-vs-datasheet conflicts, re-evaluates closure engine items 1-9). M004 is data-gated; if the owner prefers to run M005 (G1 requirement elicitation) or resolve C-20b first, M004 may be deferred — but M004 is the smallest mission that closes the remaining G4 evidence gap.

END MISSION M003B.