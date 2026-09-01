# RX50 PROJECT STATE

- Generated: 2026-08-15 by M001 bootstrap (discovery/prepare only; no design changes).
- Evidence hierarchy (1 = most authoritative): 1 locked RX50 decisions -> 2 explicit requirements -> 3 manufacturer datasheets -> 4 verified measurements -> 5 derived calculations -> 6 assumptions -> 7 proposals -> 8 previous AI conclusions.

## 1. Identity

| Item | Value | Evidence |
|---|---|---|
| Target | RX50: 50 output channels, simultaneous multi-channel firing to be supported/evaluated | DECISIONS.md |
| Baseline | RX24 (NOT automatically valid for RX50) | PROJECT_CONTEXT.md |
| Working mode | Evidence-first engineering | DECISIONS.md |

## 2. Locked decisions (only evidence-backed, from DECISIONS.md)

1. RX50 is a continuation of RX24, not a ground-up redesign.
2. Target channel count = 50.
3. Simultaneous multi-channel firing is required to be supported/evaluated.
4. RX24 `MAX_CONCURRENT_FIRE = 1` is obsolete for RX50 (NOT carried forward).
5. RX24 remains the baseline for comparison.
6. Evidence-first engineering is mandatory.
7. No firing-current / pulse / energy / voltage / timing value is carried forward. All firing-dependent items are HOLD until G1 closes.

Baseline components (STM32F103C8T6, SX1278/Ra-02, MAX3485, 74HC595 concept, CD4067 concept, HW interlock concept, 3.3 V logic rail) are BASELINE ONLY / NEEDS RECHECK for RX50 — NOT locked.

## 3. Gate status map (as of M001; no gate changed by M001)

| Gate | Subject | Status |
|---|---|---|
| G1 | Load envelope (master gate) | HOLD — owner evidence required (R-01..R-10 fill sheet exists, empty) |
| G2 | Firing-power subsystem | FEASIBILITY HOLD |
| G3 | Output expansion (74HC595) | NEEDS RECHECK — logic-level feasible (CALCULATION, 1:1 assumption, NOT locked) |
| G4 | Continuity | BLOCKED — REQUIRED RAW EVIDENCE NOT PRESENT (T-G4-01..06 absent; 0 rows ingested). Measurement PACK ready. Readiness: M003A = NOT READY; M003B = READY WITH OWNER DECISION (bounds verified); M003C = M004 NOT AUTHORIZED; M003D = GATE STOP; M003E = owner decisions D-01 (naming) + D-03 (Option B) OWNER-APPROVED; D-02 owner policy recorded (|I_fault| ≤ 5 mA bound, value NOT locked); **M004 NOT AUTHORIZED** — T-G4-06 lacks selected element + physical verification + E6 CURRENT_LIMIT; C-20b stays OPEN. No RX50 architecture change — D-03 is fixture/test-procedure only |
| G5 | MCU + pin map | PROVISIONAL / NOT LOCKED |
| G6 | Safety / interlock | NEEDS RECHECK — multi-channel authorization OPEN (owner/G1) |
| G7 | PCB / connectors | TBD |
| G8 | Protocol / command semantics | NEEDS RECHECK — 50-ch representation feasible (7-byte mask) |
| G9 | Firmware | Structural feasibility only; NO code exists |
| G10 | Test / validation | TBD — must derive from G1 |

## 4. Blockers (owner/data-gated, not harness-gated)

1. G1 load envelope — master blocker for firing power, timing/skew semantics, and multi-channel authorization.
2. CD4067 RON @3.3 V + settling time — NOT specified by manufacturer; G4 hardware measurement required (RAIN <10 kΩ rule for guaranteed ±2 LSB ADC accuracy).
3. Multi-channel authorization rule — owner/G6 decision.
4. RF-loss / stale / duplicate / ACK timeout values — owner/G1.
5. Datasheet PDFs are NOT resident in the workspace; component references are extracted web hits (verify before pinning a reference).

## 5. Harness status

- Structure: created by M001 (harness/, evidence/, decisions/, open_issues/, measurements/, calculations/, reports/).
- State: project_state.md, DECISION_REGISTER.md, OPEN_ISSUES.md, EVIDENCE_REGISTER.md, CONTRADICTION_REGISTER.md present.
- Registers are shared sources of truth for numeric/design data; derived values must not be quoted from one-off report text.

## 6. Next actions (recommendations only; owner decides priority)

1. M003B — G4 PRE-EXECUTION BLOCKER CLOSURE — COMPLETE (2026-08-15): EV-45/CD4067B abs-max current ±20 mA abs / ±10 mA rec. verified; EV-47 IINJ(PIN) ±5 mA, ΣIINJ ±25 mA, EV-48 VIN 4.0 V added; T-G4-06 fault-injection bound ≤ ±5 mA derived; C-22 logged; D-22 waveform naming PROPOSED. Follow-on owner decisions: approve T-G4-04 naming; decide 5V-fault/ADC-pin routing (C-20b).
2. M003C — G4 OWNER DECISION GATE — COMPLETE (2026-08-15): M004 NOT AUTHORIZED. D-01 = PROPOSED; D-02 bound VERIFIED ≤ ±5 mA (element FIXTURE-ONLY, value + verification = owner decision, T-G4-06 BLOCKED); D-03 5V→ADC exposure fixture-only (owner mitigation (a) sense-node division/clamp ≤4.0 V, or (b) restrict 5 V reads to channel side) + C-20b core ARCHITECTURE DECISION REQUIRED; D-04 DS5319 Rev 20 = authority (C-22 resolved at authority level, secondary rejected). Tests: G4-01/02/03 READY, G4-04/05 OWNER DECISION REQUIRED, G4-06 BLOCKED. See harness/missions/M003C_G4_OWNER_DECISION_GATE.md.
3. M003D — G4 OWNER-DECISION RECORDING & T-G4-06 SAFETY GATE — COMPLETE (2026-08-15): **GATE STOP — M004 NOT AUTHORIZED**. D-01 OWNER DECISION MISSING; D-02 NOT CLOSED (no value, no physical verification); D-03 OWNER DECISION MISSING (no Option A/B); C-20b OPEN. Safety record created `measurements/T-G4-06_CURRENT_LIMIT_SAFETY_RECORD.md` (NOT VERIFIED). Required owner inputs before M004: (a) approve/amend D-22 naming; (b) select current-limit element value ≤ ±5 mA + physically verify + complete safety record; (c) choose D-03 Option A or B.
4. M003E — OWNER DECISION RECORDING — COMPLETE (2026-08-15): D-01 (naming, D-22) OWNER-APPROVED + E4 note applied; D-03 Option B OWNER-APPROVED (fixture/test-procedure only) + execution sequence §5.3 constraint added; D-02 owner policy recorded — numerical element value PENDING physical fixture verification; C-20b stays OPEN; OI-22 CLOSEABLE, OI-21 OPEN/BLOCKED. **M004 NOT AUTHORIZED**.
5. M003F — F3 / T-G4-06 FAULT-INJECTION FIXTURE DESIGN — COMPLETE (2026-08-15): fault definition DERIVED (short/force SOURCE_CH, read victims, current-limited); every fault-path element is FIXTURE-ONLY (net register EMPTY) → NO ARCHITECTURE CHANGE REQUIRED; F3 textual schematic + current-limit constraint (|I_fault| ≤ ±5 mA, EV-47/EV-45) designed WITHOUT inventing an element value; T-G4-06 BLOCKED; M004 NOT AUTHORIZED. See harness/missions/M003F_F3_TG4-06_FIXTURE_DESIGN.md.
6. M003G — F3 ELECTRICAL SPEC / BUILD SHEET — COMPLETE (2026-08-15): buildability test → **F3 NOT buildable from repo alone**. Deliverable = precise unresolved-requirement list (8 items): (1) T-G4-06 TEST LEVEL (force V/I, short reference, terminate impedance) `REQUIREMENT MISSING`; (2) fault-source interface (type/terminals/polarity/max source condition); (3) short reference; (4) return path; (5) injection connection/disconnection mechanism; (6) current measurement point; (7) current-limit element type+value (pending physical verification, D-02); (8) node-termination reference. All operator/owner TEST VALUEs per decision sheet 1.2/1.3 + M003E D-02 — harness does NOT invent them. Safety limit VERIFIED (|I_fault| ≤ ±5 mA, EV-47; ΣIINJ ±25 mA; ADC VIN ≤ 4.0 V). T-G4-06 BLOCKED; M004 NOT AUTHORIZED. See harness/missions/M003G_F3_ELECTRICAL_SPEC_BUILD_SHEET.md.
7. F3 FINAL ENGINEERING PACKAGE — T-G4-06 / PRE-M004 CONSOLIDATED — COMPLETE (2026-08-15): single consolidated package replacing a sequential M003G→M003H workflow. One pass over the full repo: evidence extraction, requirement extraction, T-G4-06 fault definition, electrical path/buildability, F3 topology, current-limit derivation (safety bound ≤ ±5 mA kept SEPARATE from test level/limiter value/measured current — four quantities never converted), ADC/CD4067 safety (D-03 Option B preserved), build spec, physical verification plan, final gate. Owner decisions D-01/D-02/D-03 preserved verbatim. T-G4-06 BLOCKED; M004 NOT AUTHORIZED. See harness/missions/F3_FINAL_ENGINEERING_PACKAGE.md.
8. T-G4-06 OWNER INPUT RESOLUTION — COMPLETE (2026-08-15): resolves ONLY missing owner/operator inputs for the F3 fault-injection path. Verdict: `BLOCKED — OWNER INPUT REQUIRED`. Minimum owner decision set = 5: OD-1 REQUIRED TEST LEVEL (no numerical level exists; 5 mA bound NOT converted to I_test); OD-2 SHORT REFERENCE (short-to-what undefined); OD-3 FAULT SOURCE INTERFACE (type/terminals/polarity/condition); OD-4 CURRENT MEASUREMENT POINT (where |I_fault| is verified); OD-5 INJECTION MECHANISM (confirm operator-implemented removable connection satisfies §4.6/§10.2). Already delegated operator TEST VALUEs: current-limiter element type+value (D-02, actual F3 path), node termination (shared with T-G4-05, execution seq. §1). N/A: temperature, DUT count, D-01, D-03. M004 NOT AUTHORIZED. See harness/missions/TG406_OWNER_INPUT_RESOLUTION.md.
9. T-G4-06 OWNER DELEGATION CLOSURE — COMPLETE (2026-08-15): audited OD-1..OD-5 against EXISTING delegation (start pack 1.1/1.2/1.3/1.6, TASK 2, decision sheet, operator brief). **OD-5 RESOLVED BY EXISTING DELEGATION** (operator implements removable injection mechanism under approved F3 build; constraints: injection LAST §4.6, removal FIRST §10.2, limiter in series A-07/§1.5, physical verification D-02). **OD-1 (test level), OD-2 (short reference), OD-3 (source interface), OD-4 (current measurement point) = OWNER DECISION REQUIRED** — none are among the delegated items (ITEST, ADC ladder, node termination, measurement protection); protection ≠ measurement method. Final gate: `BLOCKED — OWNER DECISION REQUIRED`. See harness/missions/TG406_OWNER_DELEGATION_CLOSURE.md.
10. T-G4-06 OWNER RE-DELEGATION — FINAL RESOLUTION — COMPLETE (2026-08-15): owner re-delegates OD-1..OD-4 to operator as TEST VALUE / fixture implementation (recorded DECISION_REGISTER D-25): OD-1 fault stimulus, OD-2 short reference, OD-3 source interface, OD-4 current measurement point/method. Constraints binding: no I_test=5 mA from the bound, no invented component values, every item labelled TEST VALUE, limiter physically verified, E6 CURRENT_LIMIT mandatory, injection LAST, removal FIRST, 5 V sense node not on ADC, no architecture change, no measurement, no M004 authorization. F3 FINAL BUILD PACKAGE produced (harness/missions/F3_FINAL_BUILD_PACKAGE.md) — Final Gate: `READY FOR F3 FINAL BUILD PACKAGE`.
11. M004 PRE-RUN PHYSICAL VERIFICATION (recommended next; NOT the measurement mission): operator selects/records OD-1..OD-4 TEST VALUEs, builds F3, selects current-limit element from actual path, verifies worst-case current ≤ ±5 mA, physically verifies installed element, records E6 CURRENT_LIMIT + completes `measurements/T-G4-06_CURRENT_LIMIT_SAFETY_RECORD.md`. Only then T-G4-06 / M004 measurement can proceed. Operator-executed; do NOT run automatically.
12. M004 — G4 DATA ACQUISITION / INGESTION (operator executes T-G4-01..06; ingest E1-E6, process, log conflicts). Runs ONLY after the F3 current-limit element is physically verified and E6 CURRENT_LIMIT recorded.
13. M005 — G1 REQUIREMENT ELICITATION (owner fills load envelope / simultaneity definition). Runs if G4 data is unavailable first.
14. M006 — G6 multi-channel authorization rule (owner evidence).
15. M007 — G8 protocol draft (mask/sequence/ACK/NAK/replay).
16. Any of the above may be reordered by the owner.
