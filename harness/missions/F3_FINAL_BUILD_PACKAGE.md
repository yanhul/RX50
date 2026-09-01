# RX50 F3 FINAL BUILD PACKAGE
# T-G4-06 FAULT-INJECTION FIXTURE

- Package: F3 FINAL BUILD PACKAGE (build-oriented; follows T-G4-06 OWNER RE-DELEGATION — FINAL RESOLUTION)
- Date: 2026-08-15
- Status: COMPLETE (build package only — no physical build, no measurement, no M004 authorization, no RX50 architecture modification, no invented values)

## 0. Owner Re-Delegation (recorded verbatim, D-25)

The owner explicitly re-delegates OD-1..OD-4 to the operator as TEST VALUE / operator implementation choices:

| OD | Re-delegated item | Operator action |
|----|-------------------|-----------------|
| OD-1 | REQUIRED TEST LEVEL | select and record the actual T-G4-06 fault stimulus as TEST VALUE |
| OD-2 | SHORT REFERENCE | select and record the electrical reference for the short as TEST VALUE / fixture implementation choice |
| OD-3 | FAULT SOURCE INTERFACE | select and record the source type, terminals, polarity and allowable source condition as fixture TEST VALUE |
| OD-4 | CURRENT MEASUREMENT POINT/METHOD | select and record the method and point used to verify \|I_fault\| ≤ 5 mA |

Constraints (binding on the operator, preserved verbatim from the owner):
1. Never convert the ≤5 mA safety bound into I_TEST = 5 mA.
2. Never invent a numerical component value.
3. Every selected item must be explicitly labelled TEST VALUE or fixture implementation choice, never design requirement.
4. Actual current-limiter element must still be physically verified.
5. E6 CURRENT_LIMIT remains mandatory.
6. Injection LAST.
7. Removal FIRST.
8. 5 V-referenced sense node must not connect directly to STM32 ADC.
9. No RX50 architecture modification.
10. No measurement.
11. No M004 authorization.

This package builds on F3_FINAL_ENGINEERING_PACKAGE.md and TG406_OWNER_INPUT_RESOLUTION.md / TG406_OWNER_DELEGATION_CLOSURE.md. With OD-1..OD-4 re-delegated, the previous BLOCKED gate is cleared at the decision level. Recorded in DECISION_REGISTER.md as D-25 (OWNER-APPROVED — OPERATOR RE-DELEGATION).

## 1. Four quantities (kept separate — never converted)

| # | Quantity | Value / Status | Status |
|---|----------|----------------|--------|
| 1 | REQUIRED TEST LEVEL | NOT pre-set — OPERATOR TEST VALUE (OD-1 re-delegation, D-25) | OPERATOR TEST VALUE |
| 2 | SAFETY LIMIT | \|I_fault\| ≤ 5 mA (EV-47 governing / EV-45); ΣIINJ ≤ ±25 mA (EV-47b); ADC node VIN ≤ 4.0 V (EV-48) | VERIFIED BOUND (not a test level) |
| 3 | SELECTED CURRENT-LIMITER VALUE | NOT pre-set — OPERATOR TEST VALUE determined by ACTUAL F3 path (D-02/D-24), physically verified | OPERATOR TEST VALUE (pending physical) |
| 4 | MEASURED FAULT CURRENT | NO MEASUREMENT EXISTS | MEASUREMENT PENDING (verification not yet run) |

`|I_fault| ≤ 5 mA` is the SAFETY BOUND. It is NOT `I_test = 5 mA`. No conversion anywhere.

## 2. T-G4-06 fault definition (protocol §14 terminology preserved)

- Fault source: SOURCE_CH — a selected channel in the CD4067B network (E6 SOURCE_CH).
- Fault victim: VICTIM_CH — other channels read out (E6 VICTIM_CH).
- Fault mechanism: FAULT_TYPE ∈ {short, force} (E6); "force/short/terminate per the approved fixture condition" (protocol §14).
- Source node: SOURCE_CH terminal on the DUT CD4067B network (fixture test point).
- Victim nodes: same-MUX / cross-MUX / shared-node (POPULATION, E6).
- Injection direction: fault injected into the source-channel node; victims read on their node; injection LAST (execution seq. §4.6).
- Normal state: EXPECTED_STATE (e.g., ON) per row (E6).
- Fault state: SOURCE_CH shorted/forced through the current-limited path; victims measured (MEASURED_STATE) (E6).
- Expected observation: DELTA = MEASURED_STATE − EXPECTED_STATE per (source,victim); blast-radius characterization only (no isolation criterion — characterization-only).
- Required recovery: remove fault-injection connections FIRST (§10.2), then power down, disconnect ADC pin loads.

## 3. Final F3 topology (build-oriented textual schematic)

```text
FAULT SOURCE (OD-3: type/terminals/polarity/allowable condition = OPERATOR TEST VALUE;
             applies short or force; level recorded per trial as TEST VALUE)
     |
     |
CURRENT LIMITER (MANDATORY series element A-07/§1.5; type+value = OPERATOR TEST VALUE
                 from ACTUAL F3 path, NOT from the 5 mA bound; worst-case current
                 VERIFIED ≤ ±5 mA; element PHYSICALLY VERIFIED pre-run; recorded in
                 E6 CURRENT_LIMIT + measurements/T-G4-06_CURRENT_LIMIT_SAFETY_RECORD.md)
     |
     |
FAULT ENABLE / CONNECTION (OD-5 resolved: operator-implemented removable mechanism
                 under approved F3 build; connect LAST §4.6, remove FIRST §10.2;
                 limiter remains in series)
     |
     |
SOURCE_CH (source-channel terminal on the DUT CD4067B network; OD-2 short reference =
           OPERATOR TEST VALUE / fixture implementation — NOT assumed VSS/VDD/another channel)
     |
     |
DUT / VICTIMS (CD4067B network, single DUT; victims read on their node via DMM/ADC;
               populations same-MUX / cross-MUX / shared-node)
     |
     |
RETURN (return path for fault current = OPERATOR TEST VALUE / fixture implementation,
        dependent on the OD-2 short reference chosen — NOT invented here)
```

OD-4 measurement point/method is inserted at the fault-injection path where |I_fault| is verified (operator-selected, e.g., series current read at a defined node) — recorded as TEST VALUE, not assumed.

## 4. Buildability matrix (every safety-critical connection)

| Node | From | To | Series element | State | Return | Evidence | Status |
|---|---|---|---|---|---|---|---|
| VDD supply | bench PSU (3.3/5 V) | CD4067B VDD + DUT rail | none | PSU ON | PSU return → VSS | protocol §6/§7 | SPECIFIED |
| VDDA supply | bench PSU (3.3 V) | STM32F103 VDDA | none | PSU ON | PSU return → VSS | protocol §7 | SPECIFIED |
| VSS/ground | PSU return | CD4067 VSS, STM32 VSS, fixture common | none | hard | common ground | protocol §7 | SPECIFIED (layout = operator) |
| Address/INH | STM32 GPIO OR generator | CD4067 A/B/C/D, INH | none | GPIO/gen; slew+levels recorded | driver → GND | protocol §7/§10 | SPECIFIED |
| ADC observation | CD4067 common/channel node | STM32 ADC pin (e.g. PA0) | none | direct sense | ADC → VSS | protocol §7; D-03 | SPECIFIED 3.3 V; 5 V constrained (D-03 Option B) |
| Scope probe | ADC node | oscilloscope | probe C_in (low-C, recorded) | probe connect | probe GND → fixture GND | protocol §7; E4; A-04 | SPECIFIED |
| Node termination (shared T-G4-05) | node | termination reference | Z_effective (TEST VALUE) | hard/removable | ref node = TEST VALUE | test matrix T-G4-05; start pack | OPERATOR TEST VALUE (delegated) |
| Fault source | bench source (OD-3 TEST VALUE) | current-limiter input | none (source output) | per OD-3 | source return (OD-3/OD-2 dependent) | D-25 (OD-3) | OPERATOR TEST VALUE |
| Current limiter | source | fault enable | limiter element (OD-1-consistent TEST VALUE) | series hard | — | A-07; §1.5; D-02 | OPERATOR TEST VALUE (mandatory element; physically verified) |
| Fault enable | limiter | SOURCE_CH | operator removable connection | connect LAST/remove FIRST | — | §4.6/§10.2; D-25 (OD-5) | OPERATOR IMPLEMENTATION (delegated) |
| SOURCE_CH | fault enable | DUT channel terminal | short reference (OD-2 TEST VALUE) | fault applied | via OD-2 ref | D-25 (OD-2) | OPERATOR TEST VALUE |
| Fault-current measurement | at OD-4 point | DMM (current mode or computed) | OD-4 method | during verification | via DMM common | D-25 (OD-4); E6 CURRENT_LIMIT | OPERATOR TEST VALUE (mandatory pre-run verification) |
| DUT | SOURCE_CH/victims | network | none | single DUT | VSS common | decision 1.5 | SPECIFIED |

## 5. Operator TEST VALUE register (filled at build/verification — NOT pre-selected here)

Every item below is selected, measured/verified, and recorded by the operator as TEST VALUE or fixture implementation choice (never a design requirement). No value is invented in this package.

| Item | OD / delegation | Allowed operator action | Constraint | Required evidence |
|------|-----------------|-------------------------|------------|-------------------|
| Fault stimulus level | OD-1 (D-25) | select + record actual stimulus as TEST VALUE | never = 5 mA (bound) | recorded per trial (E6 REMARK / TEST VALUE log) |
| Short reference | OD-2 (D-25) | select + record electrical reference (fixture implementation) | not assumed VSS/VDD/channel; chosen+recorded | recorded in build log |
| Source type / terminals / polarity / allowable condition | OD-3 (D-25) | select + record as fixture TEST VALUE | must apply short/force; must not drive fault node beyond verified bounds | recorded in build log |
| Current measurement point/method | OD-4 (D-25) | select + record method+point to verify \|I_fault\| ≤ 5 mA | method chosen, not assumed | verification record (safety record + E6) |
| Current-limiter element type + value | D-02/D-24; start pack TASK 2 | select from ACTUAL F3 path, measure, record | worst-case \|I_fault\| ≤ ±5 mA; ΣIINJ ≤ ±25 mA; physically verified | E6 CURRENT_LIMIT + safety record (NOT VERIFIED until run) |
| Node termination Z_effective + reference | start pack 1.2/1.3; shared T-G4-05 | select, measure, record | known/recorded; I_EFFECTIVE only if Z known | E5 rows (T-G4-05) |
| Fault-enable mechanism | OD-5 / start pack 1.1 | operator-implemented removable mechanism | injection LAST §4.6; removal FIRST §10.2; limiter in series | build log |

## 6. Constraints (binding, from owner re-delegation + existing decisions)

1. |I_fault| ≤ 5 mA is a maximum permissible safety bound, NEVER a test level (no I_test = 5 mA).
2. No numerical component value is invented in this package or by the harness; the operator selects+records values as TEST VALUEs.
3. Every selected item labelled TEST VALUE or fixture implementation choice.
4. Current-limiter element physically verified before T-G4-06.
5. E6 CURRENT_LIMIT mandatory for all fault injection.
6. Fault injection connected LAST (§4.6).
7. Fault-injection connections removed FIRST at shutdown (§10.2), then power down, disconnect ADC loads.
8. 5 V-referenced sense node NOT connected directly to STM32 ADC (D-03 Option B; execution seq. §5.3) — no clamp/attenuation invented.
9. No RX50 architecture modification (net register EMPTY; fixture-only).
10. No measurement performed in this package.
11. No M004 authorization.

## 7. Physical verification plan (mandatory pre-run, operator-executed)

1. Construct/identify the actual F3 fault-injection path (build at topology level; owner-approved F1/F2/F3 build).
2. Select + record OD-1..OD-4 TEST VALUEs and fixture implementation choices (Section 5).
3. Select the current-limiter element from the ACTUAL F3 path (value = TEST VALUE, not derived from 5 mA).
4. Verify worst-case fault current against |I_fault| ≤ 5 mA at the OD-4 measurement point (ΣIINJ ≤ ±25 mA respected).
5. Physically verify the installed element (identity, nominal value, measured value, method, instrument, date/operator, resulting calculation).
6. Record the verification in E6 CURRENT_LIMIT and complete `measurements/T-G4-06_CURRENT_LIMIT_SAFETY_RECORD.md` (currently NOT VERIFIED / INCOMPLETE).
7. Only then permit T-G4-06 execution (injection LAST, removal FIRST).

A document value, a calculation, or a datasheet value is NOT physical verification. This plan is operator-executed and must not be run automatically by the harness.

## 8. Final gate

**`READY FOR F3 FINAL BUILD PACKAGE`**

The four re-delegations (OD-1..OD-4, D-25) are sufficient to clear the decision-level blockers; OD-5 was already resolved by existing delegation. The build package is complete at the engineering level; the operator may now build F3 and perform the mandatory pre-run current-limit verification.

### Remaining conditions (not owner decisions — operator execution)

- Operator selects + records the OD-1..OD-4 TEST VALUEs and the current-limiter element at build/verification time.
- Physical current-limit verification is executed and recorded (E6 CURRENT_LIMIT + safety record).
- No measurement of T-G4-06 occurs until the current-limiter element is physically verified.

### NOT AUTHORIZED

- M004: `M004 NOT AUTHORIZED` — this is a build package, not a measurement authorization.
- No measurement, no E6 fabrication, no architecture change.

END F3 FINAL BUILD PACKAGE.