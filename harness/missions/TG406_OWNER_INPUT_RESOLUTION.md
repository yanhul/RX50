# T-G4-06 OWNER INPUT RESOLUTION

- Batch: Owner Input Resolution — T-G4-06 / F3 fault-injection path (single batch, no engineering loop)
- Date: 2026-08-15
- Status: COMPLETE (resolution only — no redesign, no measurement, no M004 authorization, no invented values, no new mission)

## 1. Source-of-Truth Reviewed

Fresh repository reads (authoritative; no conversation-memory substitution):

- project_state.md; DECISION_REGISTER.md; DECISIONS.md; OPEN_ISSUES.md; CONTRADICTION_REGISTER.md; EVIDENCE_REGISTER.md
- M003A, M003B, M003C, M003D, M003E, M003F, M003G, F3_FINAL_ENGINEERING_PACKAGE
- RX50_G4_MEASUREMENT_EXECUTION_PROTOCOL.md (§8 safety, §14 T-G4-06)
- RX50_G4_TEST_MATRIX.md (T-G4-06 row)
- RX50_G4_EXECUTION_SEQUENCE.md (§1.5, §4.6, §5.3, §10.2)
- RX50_G4_RAW_DATA_TEMPLATES.md (E6)
- RX50_G4_CLOSURE_EVIDENCE_PLAN.md (§T-G4-06)
- RX50_G4_PROTOCOL_AUDIT.md (A-07)
- RX50_G4_MEASUREMENT_START_PACK.md (TASK 2, owner approval record)
- RX50_G4_OWNER_DECISION_SHEET.md (1.1–1.6, 2.1–2.4)
- RX50_G4_OPERATOR_EXECUTION_BRIEF.md
- RX50_SCHEMATIC_NET_REGISTER.md (EMPTY); RX50_SCHEMATIC_ARCHITECTURE_LOCK.md (NOT LOCKED)
- measurements/T-G4-06_CURRENT_LIMIT_SAFETY_RECORD.md (NOT VERIFIED / INCOMPLETE)

Targeted verification (grep across repo): no numerical fault test level, no short reference, no fault-source interface, no current-measurement point, no injection mechanism is defined anywhere for T-G4-06.

## 2. Existing Owner Decisions

| ID | Decision | Status | Source |
|---|---|---|---|
| D-01 | Waveform convention `<TEST_ID>_<DUT_ID>_N<channel_or_node>_TR<seq>.<ext>` | OWNER-APPROVED | M003E (D-22) |
| D-03 | Option B — 5 V-referenced sense node MUST NOT be connected to STM32 ADC during 5 V characterization; no attenuation/clamp invented | OWNER-APPROVED (fixture/test-procedure only) | M003E (D-23) |
| D-02 | Do NOT lock a numerical current-limiter value from the ≤5 mA bound; actual F3 path determines the limiter; physical verification mandatory | OWNER POLICY — value PENDING physical verification | M003E (D-24) |
| Start pack 1.1 | F1/F2/F3 topology-level build APPROVED | OWNER-APPROVED | start pack owner record |
| Start pack 1.4 | Temperature = ambient only | OWNER-APPROVED | start pack owner record |
| Start pack 1.5 | Single DUT (characterization) | OWNER-APPROVED | start pack owner record |
| Start pack 1.2/1.3/1.6 | Operator AUTHORIZED to select + record TEST VALUEs (ITEST, ADC ladder, node termination, measurement protection) — recorded and VERIFIED before use | OWNER-APPROVED (delegation) | start pack owner record |
| Group 2 | Settling / isolation / continuity thresholds declined → characterization-only | OWNER-APPROVED | start pack TASK 5 |

Safety bound (VERIFIED, NOT a test value): **|I_fault| ≤ 5 mA** (governing = STM32F103 IINJ(PIN) ±5 mA, EV-47; CD4067 IS/ID ±20 mA, EV-45); ΣIINJ ≤ ±25 mA (EV-47b); ADC node VIN ≤ 4.0 V (EV-48). This bound is NOT converted to `I_test = 5 mA`.

## 3. Resolved Inputs

| ID | Item | Resolution | Source | Status |
|----|------|------------|--------|--------|
| IN-1 | Fault mechanism (short / force / terminate) | E6 FAULT_TYPE ∈ {short, force}; protocol §14: "force/short/terminate it per the approved fixture condition" — mechanisms permitted, electrical reference NOT defined | E6 template; protocol §14 | DEFINED (mechanism) / reference UNDEFINED |
| IN-2 | Current-limiter element — mandatory? | YES, mandatory series element in F3 fault-injection path, value recorded | A-07; execution seq. §1.5 | MANDATORY |
| IN-3 | Current-limiter element — type? | NOT specified (no P/N, no type) | full repo search | NOT SPECIFIED |
| IN-4 | Current-limiter element — value? | NOT specified; must be determined by ACTUAL F3 path + physical verification | D-02 (M003E) | OWNER/OPERATOR TEST VALUE PENDING ACTUAL F3 PATH |
| IN-5 | Physical verification required for limiter? | YES, mandatory pre-run: identify path, select element, verify worst-case current ≤ ±5 mA, physically verify installed element, record E6 CURRENT_LIMIT + safety record | D-02; M003E; M003B; safety record | MANDATORY (operator-executed, not yet done) |
| IN-6 | Fault injection sequence | Connected LAST (§4.6); removed FIRST at shutdown (§10.2) | execution seq. | ORDER CONSTRAINT — DEFINED |
| IN-7 | E6 CURRENT_LIMIT recording | MANDATORY for all fault injection | E6 template | DEFINED |
| IN-8 | 5 V condition / ADC exposure | D-03 Option B: 5 V-referenced sense node not connected directly to STM32 ADC | D-23 (M003E); execution seq. §5.3 | OWNER-APPROVED |
| IN-9 | Node-termination reference (T-G4-06) | T-G4-06 shares the F3 node termination with T-G4-05 (execution sequence §1 reuse map: "T-G4-05 and T-G4-06 share the node termination"). Value already delegated to operator as TEST VALUE (start pack: operator AUTHORIZED to select + record node termination) | execution seq. §1; start pack owner record | OPERATOR TEST VALUE (delegated) — value not yet selected |

## 4. Owner Decisions Still Required

| ID | Decision | Why Required | Minimum Information Needed |
|----|----------|--------------|----------------------------|
| OD-1 | REQUIRED TEST LEVEL | No numerical electrical test level exists anywhere in the repository (protocol §14, test matrix, E6, execution sequence, start pack, decision sheet, missions). The 5 mA safety bound is a ceiling, NOT a test level and must not become I_test. | State the electrical stimulus for the fault (e.g., force voltage or current magnitude; or terminate impedance; or approve a specific level), or explicitly re-delegate selection to the operator as a recorded TEST VALUE |
| OD-2 | SHORT REFERENCE | Repository defines the "short" mechanism but NOT its electrical reference (short to VSS / VDD / another channel is not stated). Not assumed. | State the reference for "short" (e.g., to VSS, to VDD, to a specific node), or explicitly re-delegate to the operator |
| OD-3 | FAULT SOURCE INTERFACE | No source instrument/type, terminals, polarity, or allowable source condition is specified. Not assumed from convenience. | State source type (or permit operator choice), terminals, polarity, and allowable source condition, or re-delegate to operator as TEST VALUE |
| OD-4 | CURRENT MEASUREMENT POINT | Repository does not define where |I_fault| is measured to verify ≤ 5 mA. Measuring resistor voltage is NOT assumed without explicit support. | State the measurement point/method (e.g., series DMM current mode at a defined node), or re-delegate to operator |
| OD-5 | INJECTION CONNECTION / DISCONNECTION MECHANISM | Repository mandates order constraints (§4.6 last, §10.2 first) but not the physical mechanism (jumper/wire/switch/relay/connector). | Confirm operator-implemented removable connection satisfies the order constraints, or specify a mechanism |

## 5. Inputs That Are Operator TEST VALUES

These are SEPARATE from safety limits and from the owner decisions above. The operator is already AUTHORIZED (start pack 1.2/1.3/1.6; D-02) to select, measure, record, and verify before use:

| Input | Delegation Source | Constraint | Status |
|---|---|---|---|
| Current-limiter element type + value | start pack 1.2/1.3/1.6; D-02 | value determined by ACTUAL F3 path; worst-case |I_fault| ≤ ±5 mA; physically verified; recorded in E6 CURRENT_LIMIT + safety record | TEST VALUE (pending physical selection) |
| Node-termination Z_effective + reference | start pack 1.2 (TASK 2) / 1.3; shared with T-G4-05 (execution seq. §1) | known/recorded; I_EFFECTIVE only if Z known | TEST VALUE (delegated) |
| ITEST (T-G4-01) | decision sheet 1.3 | within DUT abs-max; recorded per trial | TEST VALUE (delegated) — NOT a T-G4-06 input |
| ADC ladder (T-G4-03) | start pack TASK 2 | values measured + recorded | TEST VALUE (delegated) — NOT a T-G4-06 input |

Safety limit is NOT an operator TEST VALUE: **|I_fault| ≤ 5 mA** is the VERIFIED maximum permissible bound (EV-47/EV-45) and is not selectable by anyone.

## 6. Inputs That Are NOT Applicable

| Item | Determination | Why |
|---|---|---|
| Node termination as an independent T-G4-06 decision | NOT carried as an owner decision | The F3 reuse map proves the dependency (execution seq. §1: T-G4-05 and T-G4-06 share node termination) and the owner already delegated its value to the operator as a TEST VALUE. Marked OPERATOR TEST VALUE (IN-9), not N/A — it is part of F3 but requires no new owner decision. |
| Temperature coverage | N/A for this batch | Already resolved (ambient only, start pack 1.4). |
| DUT sample count | N/A for this batch | Already resolved (single DUT, start pack 1.5). |
| Waveform naming (D-01) | N/A for this batch | Already OWNER-APPROVED (M003E). |
| 5 V → ADC routing (D-03) | N/A for this batch | Already OWNER-APPROVED (Option B). |

## 7. F3 Buildability Gate

`BLOCKED — OWNER INPUT REQUIRED`

The fault-injection path (SOURCE → LIMITER → FAULT ENABLE → SOURCE_CH → DUT → RETURN) cannot be built without guessing until OD-1 (test level), OD-2 (short reference), OD-3 (fault-source interface), and OD-4 (current measurement point) are answered; OD-5 (injection mechanism) requires owner confirmation of operator implementation. The current-limiter element (IN-2..IN-5) and node termination (IN-9) are already delegated operator TEST VALUEs.

## 8. M004

`M004 NOT AUTHORIZED`

## 9. Next Action

Minimum owner decisions required (no new engineering mission):

1. **OD-1 REQUIRED TEST LEVEL** — specify the fault stimulus level, or explicitly re-delegate to operator as a recorded TEST VALUE.
2. **OD-2 SHORT REFERENCE** — specify the reference for the "short" mechanism (or re-delegate).
3. **OD-3 FAULT SOURCE INTERFACE** — specify source type/terminals/polarity/allowable condition (or re-delegate).
4. **OD-4 CURRENT MEASUREMENT POINT** — specify where |I_fault| is measured (or re-delegate).
5. **OD-5 INJECTION MECHANISM** — confirm operator-implemented removable connection satisfies §4.6/§10.2 order constraints (or specify a mechanism).

When these five are answered (or explicitly re-delegated), the operator may proceed with the pre-run physical verification of the current-limiter element (select from actual F3 path, verify ≤ ±5 mA, record E6 CURRENT_LIMIT + safety record). Only then is T-G4-06 execution / M004 measurement authorization considered.

END T-G4-06 OWNER INPUT RESOLUTION.