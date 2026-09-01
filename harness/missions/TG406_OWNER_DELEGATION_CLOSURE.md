# T-G4-06 OWNER DELEGATION CLOSURE

- Batch: T-G4-06 Owner Delegation Closure (determine whether OD-1..OD-5 are covered by EXISTING delegation; no engineering, no values invented, no measurements, no M004 authorization)
- Date: 2026-08-15
- Status: COMPLETE

## 1. Repository Authority

Delegation and constraint language is taken verbatim from these authoritative documents (fresh reads):

- `RX50_G4_MEASUREMENT_START_PACK.md` — TASK 2 (fixture value table), owner approval record (1.1–1.6)
- `RX50_G4_OWNER_DECISION_SHEET.md` — Group 1 (1.1–1.6), Group 2, start condition
- `RX50_G4_OPERATOR_EXECUTION_BRIEF.md` — owner-approved conditions + TEST VALUE protocol + run card gates
- `RX50_G4_EXECUTION_SEQUENCE.md` — §1.5 (A-07 mandatory current-limit element), §4.6 (fault injection LAST), §10.2 (remove fault connections FIRST)
- `decisions/DECISION_REGISTER.md` — D-22, D-23, D-24
- `harness/missions/M003E_G4_OWNER_DECISION_RECORDING.md` — D-01/D-02/D-03 owner records
- `harness/missions/TG406_OWNER_INPUT_RESOLUTION.md` — OD-1..OD-5 definitions
- `harness/missions/F3_FINAL_ENGINEERING_PACKAGE.md`

**Canonical delegation text (verbatim):**

> Start pack TASK 2 (T-G4-06): "Fault-injection current-limit element (T-G4-06) | TEST (protection) | bounded by DUT/ADC absolute-max ratings | OWNER TEST VALUE REQUIRED (or operator-selected within bounds, recorded)"
>
> Start pack owner approval record: "1.2/1.3/1.6 | Test values + instruments | operator AUTHORIZED to select + record ITEST, ADC ladder, node termination, measurement protection — each recorded as TEST VALUE and VERIFIED before use; no design value or requirement inferred"
>
> Operator execution brief (owner-approved conditions): "Test values: operator SELECTS and RECORDS as TEST VALUE: ITEST, ADC ladder, node termination, measurement protection. Every value VERIFIED before use. No design value or requirement inferred."
>
> Operator brief TEST VALUE protocol: "Every selected value is labeled TEST VALUE in the log (never 'design value'). Value verified before use: measure/confirm with the DMM; record the measured value. No requirement is created by a test value."

Safety bound (NOT a test value): **|I_fault| ≤ 5 mA** (EV-47 governing / EV-45), ΣIINJ ≤ ±25 mA (EV-47b), ADC node VIN ≤ 4.0 V (EV-48). Not convertible to `I_test`.

## 2. OD-1 Resolution — REQUIRED TEST LEVEL

**Question:** Can operator select/record the T-G4-06 fault stimulus under the existing TEST VALUE delegation?

**Search result:** The explicit delegation enumerates exactly: **ITEST, ADC ladder, node termination, measurement protection.** The fault-injection current-limit element ("measurement protection", start pack TASK 2) is delegated as a TEST VALUE — but that is the protection element, NOT the fault stimulus level. No delegation anywhere covers the magnitude of the applied force/short/terminate stimulus.

**Resolution: `OWNER DECISION REQUIRED`**

The fault stimulus level (force V/I magnitude, terminate impedance) is not among the delegated items. The 5 mA safety bound is not a stimulus and is not converted to a test level.

## 3. OD-2 Resolution — SHORT REFERENCE

**Question:** Is the short reference explicitly delegated?

**Search result:** The delegation list (ITEST, ADC ladder, node termination, measurement protection) contains no short reference. Protocol §14 defines "short" as a mechanism but no electrical reference. No document delegates "short to VSS / VDD / another channel."

**Resolution: `OWNER DECISION REQUIRED`**

Not assumed to VSS, VDD, or another channel.

## 4. OD-3 Resolution — FAULT SOURCE INTERFACE

**Question:** Is source selection delegated to operator?

**Search result:** The delegated items (ITEST, ADC ladder, node termination, measurement protection) do not include the fault source. No document delegates source type, terminals, polarity, or allowable source condition. Protocol §14 and the E6 FAULT_TYPE permit multiple mechanisms (short/force) but no source is selected.

**Resolution: `OWNER DECISION REQUIRED`**

No existing delegation covers source selection.

## 5. OD-4 Resolution — CURRENT MEASUREMENT POINT

**Question:** Is measurement-method selection delegated?

**Search result:** "Measurement protection" (start pack TASK 2) is the current-limit element — a protection element, not a measurement method/point. E6 requires CURRENT_LIMIT to be recorded but does not define where/how |I_fault| is measured. Protocol §16 defines I_eff = delta_V / Z for T-G4-05 leakage, not for the T-G4-06 fault-current verification. No delegation authorizes the operator to choose the fault-current measurement point/method.

**Resolution: `OWNER DECISION REQUIRED`**

Measuring a resistor voltage is not assumed; no delegation supports it.

## 6. OD-5 Resolution — INJECTION MECHANISM

**Question:** Can operator choose a removable mechanism provided: (a) injection occurs LAST, (b) removal occurs FIRST, (c) current limiter remains in series, (d) physical verification is performed?

**Search result — all four conditions are EXISTING repository constraints, not new decisions:**
- (a) Injection LAST — execution sequence §4.6 ("T-G4-06 ... fault injection last (current-limited)"). [ORDER]
- (b) Removal FIRST — execution sequence §10.2 ("Remove fault-injection connections first (F3)"). [RECOMMENDATION → operator constraint]
- (c) Current limiter in series — A-07 / execution sequence §1.5 (mandatory current-limit element in the fault-injection path). [CONSTRAINT]
- (d) Physical verification — D-02 (M003E): verify worst-case current, physically verify installed element, record E6 CURRENT_LIMIT. [OWNER POLICY — MANDATORY]

The physical mechanism (jumper / wire / switch / relay / connector) is NOT specified by the repository; the owner approved the F1/F2/F3 topology-level build (start pack 1.1) and delegated fixture implementation to the operator. The mechanism selection is an implementation detail of that approved build, constrained by (a)–(d).

**Resolution: `RESOLVED BY EXISTING DELEGATION`** — operator implements a removable connection mechanism under the approved F3 build (start pack 1.1), subject to the four repository constraints (a)–(d). No owner decision required for the mechanism itself.

## 7. Existing Delegations Actually Supporting Each Resolution

| OD | Item | Existing Delegation | Supports? | Constraint / Evidence |
|----|------|--------------------|-----------|----------------------|
| OD-1 | Fault stimulus level | NONE (delegation enumerates ITEST, ADC ladder, node termination, measurement protection only) | NO — OWNER DECISION REQUIRED | 5 mA bound is a safety limit, not a stimulus |
| OD-2 | Short reference | NONE | NO — OWNER DECISION REQUIRED | no short-to-anything defined |
| OD-3 | Fault source interface | NONE | NO — OWNER DECISION REQUIRED | source type/terminals/polarity not delegated |
| OD-4 | Current measurement point | NONE (protection ≠ measurement method) | NO — OWNER DECISION REQUIRED | E6 records CURRENT_LIMIT; point/method undefined |
| OD-5 | Injection mechanism | Start pack 1.1 (F1/F2/F3 topology-level build APPROVED) + execution seq. §4.6/§10.2 + A-07/§1.5 + D-02 | YES — resolved by existing delegation | removable mechanism subject to (a) LAST, (b) FIRST, (c) limiter in series, (d) physical verification |
| (support) | Current-limit element type + value | start pack TASK 2 ("operator-selected within bounds, recorded"); D-02 | YES — operator TEST VALUE (value pending actual F3 path) | worst-case |I_fault| ≤ ±5 mA; physically verified; E6 CURRENT_LIMIT |

## 8. Remaining Owner Decisions

| ID | Decision | Minimum Information Needed |
|----|----------|----------------------------|
| OD-1 | REQUIRED TEST LEVEL | Specify the fault stimulus level (force V/I magnitude, terminate impedance), OR explicitly re-delegate stimulus selection to the operator as a recorded TEST VALUE. |
| OD-2 | SHORT REFERENCE | Specify the reference for "short" (e.g., VSS / VDD / a specific node), OR explicitly re-delegate. Do not leave VSS assumed. |
| OD-3 | FAULT SOURCE INTERFACE | Specify source type / terminals / polarity / allowable source condition, OR explicitly re-delegate source selection to the operator as a TEST VALUE. |
| OD-4 | CURRENT MEASUREMENT POINT | Specify where/how |I_fault| ≤ 5 mA is verified, OR explicitly re-delegate the measurement method to the operator. |

OD-5 requires no owner decision (closed by existing delegation in Section 6).

## 9. Final Gate

`BLOCKED — OWNER DECISION REQUIRED`

OD-1, OD-2, OD-3, OD-4 are not covered by any existing delegation. OD-5 is resolved by existing delegation. No electrical value was invented; the 5 mA safety bound was not converted to a test level. No new mission is created.

After the four remaining owner decisions are supplied (or explicitly re-delegated), the operator may proceed to the F3 FINAL BUILD PACKAGE with the current-limit element selected from the actual F3 path, physically verified, and recorded in E6 CURRENT_LIMIT + `measurements/T-G4-06_CURRENT_LIMIT_SAFETY_RECORD.md`. M004 remains NOT AUTHORIZED.

END T-G4-06 OWNER DELEGATION CLOSURE.