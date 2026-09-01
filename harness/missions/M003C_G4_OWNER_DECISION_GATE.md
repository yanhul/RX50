# M003C G4 OWNER DECISION GATE

- Mission: M003C — G4 Owner-Decision & Pre-Measurement Gate
- Date: 2026-08-15
- Status: COMPLETE
- Result: FINDINGS ONLY / DECISION-GATE ONLY (no measurements performed, no G4 closure, no architecture locked, no T-G4-06 authorized)

## Executive Status

M003B closed the datasheet-bound blockers (EV-45, EV-47/EV-48) and left three owner-decision items: D-01 (waveform naming), D-02 (T-G4-06 current-limit element value + verification), D-03 (5 V fault routing / C-20b). M003C is a DECISION-GATE mission: it verifies, classifies, and records exactly what remains an owner decision, an architecture decision, or a fixture-only action. It does NOT self-approve any proposal, does NOT close C-20b, does NOT authorize T-G4-06, and does NOT declare G4 ready.

**Key conclusion: M004 NOT AUTHORIZED.** The G4 measurement procedures and provenance fields are complete (M004 conditions 1-2 MET), but: the T-G4-06 current-limit element value is not selected/verified (conditions 3-4 NOT MET), the 5 V → ADC sense exposure at VDD = 5 V is unresolved in the fixture plan (conditions 5, 7 NOT MET), and the required owner decisions are not recorded (condition 6 NOT MET). No RX50 architecture change is required to unblock G4 — every remaining item is a recorded owner decision and/or a fixture-level operator action.

## D-01 Waveform Naming

### STATUS: PROPOSED (no existing convention; not locked)

- **Existing convention?** NONE. Repository search (all `*.md`) finds only the `WAVEFORM_FILE` field (E4 template, RX50_G4_RAW_DATA_TEMPLATES.md line 52) and its mandatory/`PROBE_C_IN` notes (line 57). No file-naming scheme exists anywhere; no owner decision on naming exists. `PROPOSED` unless repository evidence proves otherwise — no such evidence exists.
- **Minimum convention proposal** (carried from M003B D-22, unchanged):

```
<TEST_ID>_<DUT_ID>_N<channel_or_node>_TR<seq>.<ext>
example: T-G4-04_DUT-001_N12_TR01.CSV
```

| Element | Source | Example |
|---|---|---|
| TEST_ID | stable test identifier | `T-G4-04` |
| DUT_ID | DUT tag as logged in E4 | `001` |
| channel/node | channel under test; `NSHARED` for shared-node capture | `N12` |
| capture sequence | capture number within that transition (01, 02, ...) | `TR01` |

- **Template delta (exact):** add one note line after E4 row 57 in RX50_G4_RAW_DATA_TEMPLATES.md: `Waveform file naming: <TEST_ID>_<DUT_ID>_N<channel_or_node>_TR<seq>.<ext> (e.g., T-G4-04_DUT-001_N12_TR01.CSV); WAVEFORM_FILE = exact filename; original filenames preserved on handoff.`
- **Owner action required:** approve or amend this convention. Impact is minor (characterization-only; waveforms can still be captured and referenced), but the convention must be fixed before the data-handoff naming is relied on.

## D-02 T-G4-06 Current Limit

### STATUS: OWNER DECISION REQUIRED (bound VERIFIED ≤ ±5 mA; element = FIXTURE-ONLY; value + verification not yet recorded)

Answering the six questions:

| # | Question | Answer | Evidence |
|---|---|---|---|
| 1 | Maximum permissible fault-injection current (authoritative evidence) | **≤ ±5 mA** — min of STM32F103 IINJ(PIN) ±5 mA (non-FT pin, abs max) and CD4067B IS/ID ±20 mA (abs max). ΣIINJ(PIN) aggregate cap ±25 mA. | EV-47, EV-47b, EV-45 (DS5319 Table 7; SCHS052D Rev D) |
| 2 | Current limit the G4 protocol requires | A MANDATORY current-limit element in the F3 fault-injection path, value recorded and VERIFIED BEFORE T-G4-06. No numeric value is specified — value is an owner/operator TEST VALUE bounded by the abs-max ratings. | A-07 (protocol audit); execution sequence §1.5; owner record 2026-08-15; start pack TASK 2 |
| 3 | Does the proposed fixture contain a current-limiting element? | YES by specification — the F3 fixture description mandates a current-limit element in the fault-injection path (value not defined). | execution sequence §1.5 |
| 4 | Can worst-case current be calculated from existing component values? | NO. The element value and fault-path impedance are not selected; no schematic exists (net register EMPTY). The LIMIT BOUND (≤ ±5 mA) is verified/derivable; the actual fixture worst-case current is NOT calculable until the element value is selected, measured, and recorded. | net register EMPTY; schematic BLOCKED |
| 5 | Is the limiting element part of the RX50 design? | NO — it is an F3 test-fixture element; RX50 product architecture defines no such element (no schematic, no nets). | net register EMPTY; architecture NOT LOCKED |
| 6 | Fixture-only or architecture change? | **FIXTURE-ONLY.** It is already mandated in the F3 fixture spec; adding/installing it does not change RX50 architecture. | execution sequence §1.5 |

- **Critical caveat:** M003C does NOT claim T-G4-06 is safe. The verified bound (≤ ±5 mA) is the maximum permissible fault-injection current, NOT a selected test value. T-G4-06 execution remains BLOCKED until (a) the element value is selected within the bound, (b) the element is physically verified in F3, and (c) the value + verification are recorded (E6 `CURRENT_LIMIT`; closure engine item 6).

## D-03 5 V Fault Routing / C-20b

### STATUS: OWNER DECISION REQUIRED (fixture-level 5 V→ADC exposure) + ARCHITECTURE DECISION REQUIRED (C-20b core, unchanged)

Investigation against the repository (no schematic exists):

| Question | Finding | Evidence |
|---|---|---|
| Where does the 5 V fault originate? | The bench PSU supplying VDD = 5 V to the CD4067B in the TEST FIXTURE (T-G4-01 VDD=5 V; T-G4-05 VDD=3.3/5 V; T-G4-06 VDD controlled). There is no 5 V net in any RX50 design. | test matrix; net register EMPTY |
| Which node does it reach? | In F3 the CD4067 channel/common node is biased from VDD through the node termination; the ADC node is read by the STM32 ADC pin. | protocol §7 (ADC observation path); execution sequence §1 (F3) |
| Can it reach the STM32 ADC pin? | **YES in F3 at VDD = 5 V** — the ADC node is directly read on an STM32 ADC pin (candidate PA0; Map A/B). A 5 V-referenced node would exceed the verified VIN abs max 4.0 V (EV-48) and the VDDA+0.3 V guidance for ADC-active pins. | EV-48; protocol §7 |
| What series/divider/protection elements exist? | NONE defined for the sense node. Z_effective is an operator TEST VALUE; the only mandated protection element is the T-G4-06 fault-injection current-limit element (A-07). No sense-node attenuation/clamp is specified anywhere. | protocol §7; execution sequence §1.5; start pack TASK 2 |
| Is the path physically present or only proposed? | **ONLY PROPOSED.** No schematic/PCB; net register EMPTY; sheet definition BLOCKED; architecture NOT LOCKED. | net register; sheet definition; architecture lock |
| Is the 5 V condition required by the G4 protocol? | **YES** — VDD = 5 V is a required test condition (T-G4-01 RON@5 V; T-G4-05 VDD=3.3/5 V; T-G4-06 VDD controlled). | protocol §9/§13/§14; test matrix |
| Fixture condition or RX50 architecture condition? | **TEST FIXTURE condition**, not an RX50 architecture condition: the architecture is not defined/locked, and sense-divider (Rth) values are explicitly OUT OF SCOPE for G4. | protocol §2; start pack TASK 2 |

**C-20b core (control path — STM32 VOH 2.9 V < CD4067 VIH@5 V 3.5 V):** an architecture-level conflict (level-shift vs 3.3 V-only path), definitive (even nominal 3.3 V < 3.5 V → zero guaranteed-drive margin). It remains OPEN — owner decision. It is NOT a G4-execution blocker: the F1/F3 fixture can drive the CD4067 control inputs at 5 V logic levels via a bench generator or a buffered/level-shifted driver (a fixture implementation detail), and T-G4-02 runs at 3.3 V only.

**5 V→ADC sense exposure:** demonstrable in the test plan as written (5 V-referenced sense node read on a 4.0 V-limited ADC pin with no attenuation element defined). Because no RX50 design exists, this is NOT an "architecture issue" — it is **isolatable entirely within the test fixture** without changing RX50 architecture:
- Option (a): add sense-node division/clamping in F3 so the ADC pin stays ≤ 4.0 V (ideally ≤ VDDA+0.3 V) at VDD = 5 V; or
- Option (b): restrict 5 V characterization to the CD4067 channel side (as T-G4-01 already is — no ADC) and do not read the node on the ADC pin at VDD = 5 V (T-G4-05/T-G4-06 5 V runs would record channel-side/termination-side data only, or be deferred to the 3.3 V condition).

Verdict per mission rule: the 5 V exposure can be isolated within the test fixture → identified explicitly above. Owner must pick (a) or (b) before 5 V runs of T-G4-05/T-G4-06. C-20b core remains an architecture decision and is not closed by M003C.

## D-04 DS5319 Primary Source

### STATUS: VERIFIED (authority established; C-22 resolved to the extent possible — secondary source rejected)

- **Device identity:** STM32F103C8 (this project's candidate: STM32F103C8T6, LQFP48), STM32F103xx medium-density performance line, Arm Cortex-M3, 2.0–3.6 V supply. Confirmed on the official ST product page.
- **Manufacturer:** STMicroelectronics.
- **Official datasheet + revision:** DS5319 — STM32F103x8/STM32F103xB datasheet (document CD00161566), currently published **Rev 20** (st.com resource); Rev 18/19 text was page-captured for this session. Prior repo references cite Rev 19/20.
- **Relevant VIN / injection specs (Rev 18/19 verbatim text; Table 6/7/34):**
  - VIN "any other pin" (standard, 3 V-capable / non-FT): **VSS−0.3 to 4.0 V**.
  - VIN "5 V tolerant pin": VSS−0.3 to VDD+4.0 V.
  - IINJ(PIN) on any other pin: **±5 mA**; ΣIINJ(PIN): **±25 mA** (Table 7).
  - Functional susceptibility, any other pin: −5/+5 mA (Table 34).
  - ADC notes: positive injection within IINJ limits does not affect ADC accuracy; negative injection on analog pins reduces accuracy (avoid; Schottky recommendation).
- **Secondary source disposition:** the sheetsdata.com render ("VDD+0.3" for non-FT pins) is **REJECTED as authority**. Reasons: (1) third-party HTML re-render, not the manufacturer; (2) it reflects older-revision wording — current published DS5319 revisions specify a fixed 4.0 V upper bound (Rev 18/19 verbatim captured); (3) the governing constraint for the G4 current limit (IINJ ±5 mA) is identical across all sources, so the VIN discrepancy has zero impact on D-02. Note: ST guidance (community/AN4899) states that with an ADC input active the pin should stay below VDDA+0.3 V to avoid injection — consistent with the 4.0 V limit and stricter for ADC operation.
- **Why DS5319 has higher authority:** manufacturer primary datasheet (hierarchy level 3) with documented revision history, vs an unofficial third-party re-render with no revision identity.
- **Residual (not deleted):** exact Rev 20 Table 6 page-level pin-down when the PDF is resident (OI-15). C-22 is updated to reflect the authority finding; it is not silently deleted.

## Decision Matrix

| Decision | Current Status | Evidence | Proposal | Owner Decision Required | Architecture Impact |
|---|---|---|---|---|---|
| D-01 Waveform naming convention | PROPOSED | no existing convention (E4 WAVEFORM_FILE only; D-22) | `<TEST_ID>_<DUT_ID>_N<channel_or_node>_TR<seq>.<ext>` (e.g., T-G4-04_DUT-001_N12_TR01.CSV) + E4 note line | YES — approve/amend D-22 | none (template note only) |
| D-02 T-G4-06 current limit | OWNER DECISION REQUIRED (bound VERIFIED ≤ ±5 mA; element fixture-only) | EV-47/EV-47b/EV-45; A-07; execution sequence §1.5; owner record 2026-08-15 | element value selected within ≤ ±5 mA + physical verification + E6/closure-item-6 record | YES — value (owner or operator-delegated) + mandatory pre-run verification | NONE — fixture-only (F3 element already mandated) |
| D-03 5 V fault routing / C-20b | OWNER DECISION REQUIRED (fixture 5V→ADC exposure) + ARCHITECTURE DECISION REQUIRED (C-20b core) | protocol §7; no sense-node attenuation defined; net register EMPTY; EV-48; SCHS052D VIH vs DS5319 VOH | fixture: (a) sense-node division/clamp ≤4.0 V at VDD=5 V, or (b) restrict 5 V node reads to channel side; C-20b: level-shift vs 3.3 V-only path | YES — 5 V-read mitigation (a/b) + C-20b core | D-03 exposure: none (fixture-only); C-20b core: architecture (level-shift vs 3.3 V path) |
| D-04 DS5319 primary source | VERIFIED (authority established; C-22 partially resolved) | ST product page; DS5319 Rev 20 (CD00161566); Rev 18/19 verbatim | reject secondary (older-revision render); pin Rev 20 PDF when resident (OI-15) | NO (record only) | none |

## G4 Test Readiness

| Test | Status | Gate note |
|---|---|---|
| T-G4-01 RON | READY | bound verified (EV-45/EV-47); ITEST = operator TEST VALUE (owner-delegated, recorded); VDD=5 V RON is channel-side only (no ADC) |
| T-G4-02 VIH/VIL | READY | 3.3 V only; no 5 V / ADC exposure |
| T-G4-03 ADC vs RAIN | READY | F2 standalone; no 5 V on ADC path |
| T-G4-04 Settling | OWNER DECISION REQUIRED | waveform naming (D-01) approval; minor, characterization-only |
| T-G4-05 Leakage | OWNER DECISION REQUIRED | VDD=5 V condition → ADC-pin VIN exposure unresolved (D-03); 3.3 V portion READY |
| T-G4-06 Isolation | BLOCKED | current-limit element value + physical verification absent (D-02); plus D-03 exposure at VDD=5 V |

**Overall G4 execution: NOT AUTHORIZED** — an unresolved execution-safety decision (T-G4-06 current-limit verification) and an unresolved 5 V→ADC exposure remain.

## Remaining Blockers

1. **T-G4-06 current-limit element value + physical verification record** — bound VERIFIED ≤ ±5 mA (EV-47), but the element value is not selected, not physically verified, and not recorded. Mandatory pre-run per owner record 2026-08-15.
2. **5 V → ADC sense exposure at VDD = 5 V (T-G4-05/T-G4-06)** — no sense-node attenuation/clamp defined; owner must choose mitigation (a) or (b) in D-03.
3. **Owner decisions D-01, D-02, D-03** — not yet recorded.
4. (Informational, non-blocking) C-20b core (5 V control VIH) — architecture decision open; not a fixture-execution gate. OI-16 "G4 Evidence Retrieval" artifact still absent. EV-44 (VOL row) still NEEDS RECHECK.

## Required Owner Decisions

1. **D-01** — Approve/amend the waveform naming convention (proposal above; template delta pending).
2. **D-02** — Fix and authorize the T-G4-06 current-limit element value within the verified ≤ ±5 mA bound (owner or operator-delegated per decision sheet 1.3); record the mandatory physical verification before T-G4-06.
3. **D-03** — Choose the 5 V-node-read mitigation: (a) sense-node division/clamp in F3 keeping the ADC pin ≤ 4.0 V (ideally ≤ VDDA+0.3 V), or (b) restrict 5 V characterization to the CD4067 channel side (no ADC-pin reads at VDD = 5 V). Additionally record the C-20b core architecture decision (level-shift vs 3.3 V-only path) — an architecture decision, not a G4-execution gate.

## Architecture Impact

- **No RX50 architecture change is required to execute G4.** Every remaining G4 blocker is a recorded owner decision and/or a fixture-only action (F3 current-limit element; sense-node attenuation/clamp). The net register remains EMPTY and the schematic architecture NOT LOCKED — nothing in M003C adds, moves, or invents a net, component, or design value.
- **C-20b core is the only open architecture decision** (level-shift vs 3.3 V-only control path for a 5 V-powered CD4067). It is not a G4-execution gate and is NOT closed by M003C.
- **D-04** records the authoritative datasheet source (DS5319 Rev 20); no design change.

## M004 Authorization

Conditions checked against the repository + M003B/M003C evidence:

| # | Condition | Status |
|---|---|---|
| 1 | Required G4 measurement procedures complete | MET (protocol, matrix, sequence, start pack, brief, templates, closure engine) |
| 2 | Instrumentation/provenance fields defined | MET (E1-E6 headers, instrument log, protocol §15) |
| 3 | T-G4-06 current-limit mechanism explicitly defined | PARTIAL — mechanism (mandatory F3 element) defined; element VALUE not selected |
| 4 | T-G4-06 current limit verified against absolute limits | NOT MET — bound verified (≤ ±5 mA) but element value + physical verification record absent |
| 5 | C-20b leaves no unresolved unsafe 5 V → ADC path | NOT MET — 5 V→ADC sense exposure unresolved (D-03) |
| 6 | Required owner decisions explicitly resolved | NOT MET — D-01, D-02, D-03 not recorded |
| 7 | No execution-critical contradiction remains | NOT MET — 5 V→ADC exposure is execution-critical for 5 V runs of T-G4-05/06 (C-20b-linked); C-22 is authority-resolved and not execution-critical |

**M004 NOT AUTHORIZED.**

Blockers: (1) T-G4-06 current-limit element value + verification record; (2) unresolved 5 V → ADC sense exposure; (3) owner decisions D-01/D-02/D-03 unrecorded.

## Final Gate

### VERIFIED

- Maximum permissible fault-injection current = ≤ ±5 mA (min of IINJ(PIN) ±5 mA, EV-47, and CD4067 IS/ID ±20 mA, EV-45). [M003B; re-confirmed]
- CD4067B abs-max IS/ID ±20 mA / rec. op. ±10 mA; control-input pin ±30 mA (SCHS052D Rev D). [EV-45]
- STM32F103 IINJ(PIN) ±5 mA, ΣIINJ(PIN) ±25 mA, VIN non-FT ≤ 4.0 V (DS5319 Table 6/7, Rev 18/19 verbatim; Rev 20 current). [EV-47/47b/48]
- T-G4-06 current-limit mechanism = mandatory element in the F3 fault-injection path (fixture-only). [A-07; execution sequence §1.5]
- D-04: authoritative source = ST DS5319 Rev 20 (CD00161566), device STM32F103C8/STM32F103C8T6; secondary (sheetsdata) rejected.
- No RX50 schematic/net exists (net register EMPTY); 5 V condition is a G4 test-fixture condition, not an architecture condition.
- M004 conditions 1-2 MET; 3-7 NOT MET.

### PROPOSED

- D-01 waveform naming: `<TEST_ID>_<DUT_ID>_N<channel_or_node>_TR<seq>.<ext>` (D-22) — STATUS PROPOSED, awaiting owner approval. NOT locked.

### OWNER DECISION REQUIRED

1. D-01 — approve/amend waveform naming convention.
2. D-02 — fix + authorize T-G4-06 current-limit element value within ≤ ±5 mA; record mandatory physical verification before T-G4-06.
3. D-03 — choose 5 V-node-read mitigation: (a) sense-node division/clamp ≤ 4.0 V in F3, or (b) restrict 5 V characterization to the CD4067 channel side.

### ARCHITECTURE DECISION REQUIRED

- C-20b core: level-shift vs 3.3 V-only control path for a 5 V-powered CD4067 (owner decision; not a G4-execution gate). The 5 V→ADC sense exposure itself is fixture-only and does not require an architecture change.

### BLOCKED

- **T-G4-06 execution** — current-limit element value + physical verification record absent (bound verified ≤ ±5 mA).
- **T-G4-05 / T-G4-06 5 V condition** — until D-03 mitigation is chosen and implemented in the fixture.
- Overall G4 measurement start: NOT AUTHORIZED (M004 blocked).

### M004 AUTHORIZATION

**M004 NOT AUTHORIZED**

### NEXT MISSION

**M003D — G4 OWNER-DECISION RECORDING & T-G4-06 SAFETY GATE**: the smallest mission that converts D-01, D-02, D-03 from open items into recorded owner decisions (and applies the E4 naming template delta), and establishes the T-G4-06 current-limit element value + physical-verification record as the pre-run safety gate. Rationale: M004's conditions 3-7 are owner/fixture-gated, not evidence-gated; M003D is the minimal mission that records those decisions and the T-G4-06 safety record. When M003D completes with all three decisions recorded and the T-G4-06 verification logged, the follow-on is M004 — G4 DATA ACQUISITION / INGESTION. Do NOT execute M004 before M003D.

END MISSION M003C.