# M003E G4 OWNER DECISION RECORDING

- Mission: M003E — Owner Decision Recording
- Date: 2026-08-15
- Status: COMPLETE (decision recording + project control only; no measurements, no verification fabrication, no M004 authorization)

## Executive Status

Following M003D (GATE STOP) and the engineering review, the owner supplied explicit decisions for D-01 and D-03, and a policy record for D-02. M003E records them verbatim, updates project control, and applies the minimum G4 protocol/template deltas. It does NOT declare T-G4-06 safe, does NOT authorize M004, does NOT close G4, does NOT close C-20b, and does NOT modify RX50 architecture (D-03 is explicitly fixture/test-procedure scope).

**M004 remains NOT AUTHORIZED**: T-G4-06 still lacks a selected physical current-limit element, its physical verification, and E6 CURRENT_LIMIT evidence.

## D-01 Owner Decision

- **OWNER DECISION: APPROVED — D-22 proposal.**
- Approved convention: `<TEST_ID>_<DUT_ID>_N<channel_or_node>_TR<seq>.<ext>` (example `T-G4-04_DUT-001_N12_TR01.CSV`).
- Now an OWNER-APPROVED G4 data-handoff convention. Convention NOT altered by the harness.
- Recorded in DECISION_REGISTER.md as D-22 status OWNER-APPROVED (D-01, M003E).

## D-03 Owner Decision

- **OWNER DECISION: APPROVED — OPTION B** (5 V fault / ADC routing).
- For G4 5 V characterization: characterize CD4067/channel-side behavior as required by the protocol; do NOT expose the 5 V-referenced sense node directly to the STM32 ADC input; do NOT invent an attenuation or clamp network; ADC observations requiring the valid STM32 ADC voltage range must be performed under an appropriate supply/test condition; preserve the CD4067-side 5 V vs MCU ADC characterization distinction.
- **FIXTURE/TEST-PROCEDURE decision only. NOT a final RX50 architecture decision.**
- Recorded in DECISION_REGISTER.md as D-23, status OWNER-APPROVED — FIXTURE/TEST-PROCEDURE (NOT architecture).

## D-02 Owner Policy / Pending Physical Verification

- **OWNER DECISION: DO NOT LOCK A NUMERICAL CURRENT-LIMIT ELEMENT VALUE YET.**
- Verified authoritative bound remains `|I_fault| ≤ 5 mA` (tighter STM32 ADC-pin injection-current abs max; EV-47/EV-45). This is a MAXIMUM PERMISSIBLE fault-injection bound, NOT the selected test current.
- Operator steps required (owner mandate):
  1. construct/identify the actual F3 fault path;
  2. select the current-limiting element;
  3. verify the resulting worst-case current;
  4. physically verify the installed element;
  5. record the verification in E6 `CURRENT_LIMIT`;
  6. only then permit T-G4-06 execution.
- Until then: `T-G4-06 = BLOCKED`. No fake E6 verification record created.
- Recorded in DECISION_REGISTER.md as D-24, status OWNER POLICY RECORDED — NUMERICAL ELEMENT VALUE PENDING PHYSICAL FIXTURE VERIFICATION. NOT represented as a locked component value.

## C-20b Status

**OPEN.** C-20b is NOT closed. D-03 Option B is a G4 fixture/test-procedure decision and does not resolve the architecture-level contradiction (STM32 VOH 2.9 V < CD4067 VIH@5 V 3.5 V; 5 V control path vs 3.3 V path). Architecture lock state UNCHANGED. No edit made to CONTRADICTION_REGISTER.md for C-20b.

## Decision Register Changes

- DECISION_REGISTER.md:
  - Status vocabulary extended with `OWNER-APPROVED` (explicit owner decision; may be fixture/test-procedure scope) vs `LOCKED` (recorded in DECISIONS.md).
  - D-22 → OWNER-APPROVED (D-01 waveform naming).
  - D-23 (NEW) → OWNER-APPROVED (D-03 Option B, fixture/test-procedure only).
  - D-24 (NEW) → OWNER POLICY RECORDED — NUMERICAL ELEMENT VALUE PENDING PHYSICAL FIXTURE VERIFICATION (D-02).
- DECISIONS.md (root, canonical locked file): NOT edited — D-01/D-03 are fixture/procedure-level decisions, not RX50 architecture lock decisions.

## G4 Protocol Changes

Minimum deltas applied to reflect approved D-01 and D-03:

1. **RX50_G4_RAW_DATA_TEMPLATES.md (E4, T-G4-04 settling):** added the owner-approved waveform filename convention note after the E4 capture note: `<TEST_ID>_<DUT_ID>_N<channel_or_node>_TR<seq>.<ext>`, WAVEFORM_FILE = exact filename, original filenames preserved on handoff.
2. **RX50_G4_EXECUTION_SEQUENCE.md (§5 Supply transitions):** added constraint (owner decision D-03 Option B) that for VDD = 5 V runs (T-G4-01 RON@5 V channel-side; T-G4-05/T-G4-06 5 V condition), the 5 V-referenced sense node MUST NOT be connected directly to the STM32 ADC input; no attenuation/clamp network invented; ADC observations requiring valid STM32 ADC range are performed under an appropriate supply/test condition (e.g., 3.3 V).

No new resistor values invented. F3 NOT redesigned. No locked architecture document was edited (net register, architecture lock, sheet definition, release gate unchanged — all remain EMPTY/NOT LOCKED/BLOCKED as before).

## Open-Issue Changes

- **OI-22 (5V → ADC exposure) → CLOSEABLE**: owner decision RESOLVED (D-03 Option B, M003E); closure = execution constraint applied (execution sequence §5.3). Note: C-20b remains OPEN separately — not closed by D-03.
- **OI-21 (T-G4-06 current-limit element) → OPEN / BLOCKED**: owner policy recorded (M003E), but numerical value + physical verification still pending; T-G4-06 blocked until F3 element selected + physically verified + E6 CURRENT_LIMIT recorded.
- D-01 procedural blocker: resolved (D-22 approved + E4 note applied). No dedicated OI row existed for it; recorded here.
- No issue closed beyond OI-22's CLOSEABLE status; no duplicates merged.

## Contradiction Changes

- CONTRADICTION_REGISTER.md: **no change.** C-20b retains its OPEN status (independent architecture issue). C-22 remains RESOLVED AT AUTHORITY LEVEL (M003C), unchanged. No new contradictions logged by M003E.

## M004 Authorization

**M004 NOT AUTHORIZED.**

Reason (owner mandate): T-G4-06 still lacks (a) selected physical current-limit element, (b) physical verification, (c) E6 CURRENT_LIMIT evidence. The owner decisions in M003E are decision/policy records, NOT measurement authorization. M004 cannot yet be authorized for the full T-G4-01..06 execution package.

## Remaining Physical Actions

1. Construct/identify the actual F3 fault-injection path (physical fixture).
2. Select the current-limiting element from that path.
3. Verify the resulting worst-case current against the |I_fault| ≤ 5 mA bound (EV-47/EV-45).
4. Physically verify the installed element.
5. Record the verification in E6 `CURRENT_LIMIT` and complete `measurements/T-G4-06_CURRENT_LIMIT_SAFETY_RECORD.md` (currently NOT VERIFIED / INCOMPLETE).
6. Only then permit T-G4-06 execution and proceed toward M004 measurement authorization.

These are operator/owner physical actions. The harness cannot perform or fabricate them.

## Final Gate

### OWNER-APPROVED

- D-01 (waveform naming, D-22)
- D-03 (5 V fault / ADC routing — Option B, fixture/test-procedure only)

### OWNER POLICY / PENDING VERIFICATION

- D-02 (T-G4-06 current-limit element: bound |I_fault| ≤ 5 mA; numerical element value NOT locked, pending physical fixture verification)

### STILL OPEN

- C-20b (architecture-level 5 V control path contradiction)

### BLOCKED

- T-G4-06 until physical current-limit verification (E6 CURRENT_LIMIT evidence)

### M004

`M004 NOT AUTHORIZED`

### NEXT MISSION

`M004 PRE-RUN PHYSICAL VERIFICATION` — construct/identify the actual F3 fault path, select the current-limit element, verify the worst-case current, physically verify the installed element, and record the E6 CURRENT_LIMIT evidence required before T-G4-06. This is NOT the measurement mission. Do not execute M004 automatically.

END MISSION M003E.