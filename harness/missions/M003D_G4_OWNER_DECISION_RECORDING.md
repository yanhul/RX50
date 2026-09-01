# M003D G4 OWNER DECISION RECORDING & SAFETY GATE

- Mission: M003D — G4 Owner-Decision Recording & T-G4-06 Safety Gate
- Date: 2026-08-15
- Status: COMPLETE (GATE STOP — owner decisions not yet supplied)
- Result: **M004 NOT AUTHORIZED**. None of D-01, D-02, D-03 has an explicit owner decision recorded in the repository. T-G4-06 safety record created but **NOT VERIFIED / INCOMPLETE**.

## Executive Status

M003D re-read the repository source-of-truth (registers, M003A/B/C, G4 protocol, templates, execution sequence, start pack, owner decision sheet, DECISIONS.md, OPEN_ISSUES.md). The repository contains **no explicit owner approval** for the three decisions M003C flagged as OWNER DECISION REQUIRED:

- **D-01 Waveform naming**: D-22 remains `PROPOSAL — awaiting owner approval`. No approval exists anywhere.
- **D-02 T-G4-06 current-limit value**: no value is selected or recorded; no physical verification exists; the safety record is `NOT VERIFIED`.
- **D-03 5 V → ADC mitigation**: neither Option A nor Option B is selected by the owner.

The owner's recorded approval (start pack 2026-08-15) delegates *operator* authority to select and record TEST VALUEs and verify them before use — it does **not** approve the waveform naming, does **not** supply a current-limit value, and does **not** choose a 5 V mitigation. Per the M003D critical rule, the harness stops at the gate rather than inferring what the owner would choose.

## D-01 Waveform Naming

### Existing Decision

- Proposal D-22 (DECISION_REGISTER.md:48): `<TEST_ID>_<DUT_ID>_N<channel_or_node>_TR<seq>.<ext>` (e.g., `T-G4-04_DUT-001_N12_TR01.CSV`); WAVEFORM_FILE = exact filename; original filenames preserved on handoff. Status: PROPOSAL — awaiting owner approval (NOT locked). Re-confirmed by M003C.
- The start pack owner approval record (2026-08-15) does not mention waveform naming.

### Decision Status

**D-01 OWNER DECISION MISSING.** No explicit owner approval or amendment exists in the repository.

### Applied Template Change

NOT APPLIED. The E4 naming note (RX50_G4_RAW_DATA_TEMPLATES.md, after line 57) is NOT added, because the proposed convention is not owner-approved. The E4 `WAVEFORM_FILE` field remains as-is (mandatory, exact filename).

## D-02 T-G4-06 Current Limit

### Approved Value

**NONE RECORDED.** The owner approved delegation of operator authority (start pack 1.2/1.3/1.6): operator may select and record the current-limit element as a TEST VALUE and verify it before use. That delegation is not itself a selected value. No element value exists anywhere in the repository (measurements/ empty; E6 0 rows; safety record field NOT SUPPLIED).

### Authoritative Bound

VERIFIED (M003B): fault-injection current must be **≤ ±5 mA** — min of IINJ(PIN) ±5 mA (EV-47, DS5319 Table 7) and CD4067 IS/ID ±20 mA abs / ±10 mA rec (EV-45, SCHS052D Rev D). ΣIINJ(PIN) ±25 mA aggregate cap (EV-47b). Evidence: EV-45, EV-47, EV-47b.

### Fixture Element

FIXTURE-ONLY: a mandatory current-limit element in the F3 fault-injection path (A-07; execution sequence §1.5). No element is identified/installed (no fixture build recorded; schematic net register EMPTY; F3 is conceptual/topology-level).

### Physical Verification

**ABSENT.** No physical verification exists. Checked against the mission's five required verification points:
1. Value within bound — NOT APPLICABLE (no value selected).
2. Fixture element identified — NO (none identified).
3. Element physically present/verified — NO (no build recorded).
4. Verification record (fixture, element identity, nominal value, measured value, method, instrument, date/operator, resulting calculation) — NO (safety record NOT VERIFIED / INCOMPLETE).
5. Traceable to E6 / closure item 6 — NO (E6 0 rows; closure engine item 6 MEASUREMENT PENDING).

### Verification Evidence

None in repository. New file `measurements/T-G4-06_CURRENT_LIMIT_SAFETY_RECORD.md` created (status NOT VERIFIED / INCOMPLETE) so the required fields are preserved and the absence is explicit.

### Safety Result

**D-02 NOT CLOSED.** T-G4-06 execution is NOT authorized. A resistor value in a document, a calculated current, or a datasheet value is NOT physical verification — none of these are fabricated here.

## D-03 5 V → ADC Mitigation

### Selected Option

**D-03 OWNER DECISION MISSING.** Neither Option A (sense-node division/clamping ≤4.0 V in F3) nor Option B (restrict 5 V characterization to the CD4067 channel side) is selected by the owner. The harness does NOT choose A or B.

### Fixture Procedure

NOT DEFINED (no owner choice to implement). The 5 V condition remains a required G4 test condition (T-G4-01 RON@5 V channel-side; T-G4-05 VDD=3.3/5 V; T-G4-06 VDD controlled), and the ADC node is read on the STM32 ADC pin (protocol §7 observation path on e.g. PA0). Until the owner selects a mitigation, no fixture procedure prevents the 5 V-referenced sense node from reaching the ADC pin.

### Safety Result

5 V → ADC exposure at VDD = 5 V (T-G4-05 / T-G4-06) remains UNRESOLVED. Not isolatable by the harness without the owner decision; the owner must pick A or B before 5 V runs of T-G4-05/T-G4-06.

## C-20b Architecture Status

**OPEN.** C-20b (STM32 VOH 2.9 V < CD4067 VIH@5 V 3.5 V; 5 V control path vs 3.3 V path) remains an OPEN architecture decision (level-shift vs 3.3 V-only path). Per M003C separation, it is NOT forced into the M004 gate as a G4-execution blocker (the fixture can buffer/level-shift the control at 5 V). It is not LOCKED and not SUPERSEDED. Not resolved by M003D; no owner record exists.

## Decision Register Changes

- DECISION_REGISTER.md: NO explicit owner decisions exist to record. D-22 remains `PROPOSAL — awaiting owner approval (NOT locked)` with an M003C re-confirmation note appended. No LOCKED/EVIDENCE-BACKED status changes. No owner-approved entries invented.
- The three M003C decision items are recorded in this mission report as: D-01 OWNER DECISION MISSING / D-02 NOT CLOSED / D-03 OWNER DECISION MISSING.

## Open-Issue Changes

- OI-21 (T-G4-06 current-limit element value + physical verification): status updated to reflect M003D — no value selected, safety record created but NOT VERIFIED, T-G4-06 BLOCKED until owner/operator selects + verifies + records.
- OI-22 (5V → ADC exposure): status updated to reflect M003D — D-03 OWNER DECISION MISSING; Option A/B not chosen; 5 V runs of T-G4-05/06 blocked pending owner choice.
- No issue closed. No duplicates merged.

## Evidence Changes

- No new evidence records added. The mission brief (section 9) forbids creating evidence records for decisions alone, and no measurements exist (level-4 register remains all MEASUREMENT PENDING).
- New artifact registered (NOT evidence): `measurements/T-G4-06_CURRENT_LIMIT_SAFETY_RECORD.md` — a control/safety record with status NOT VERIFIED. Its new location is registered here (AGENTS.md rule 9).

## M004 Authorization Matrix

| Condition | Status | Evidence |
|---|---|---|
| 1. D-01 explicitly resolved | NOT MET | D-01 OWNER DECISION MISSING (D-22 PROPOSAL only) |
| 2. D-02 explicitly approved current-limit value | NOT MET | no value selected/recorded; owner delegated operator authority only (start pack 1.2/1.3/1.6) |
| 3. D-02 physical verification recorded | NOT MET | safety record NOT VERIFIED / INCOMPLETE; E6 0 rows |
| 4. Verified current limit within authoritative bound | NOT MET | bound verified (≤ ±5 mA, EV-47/EV-45) but no element value exists to hold to it |
| 5. D-03 explicitly resolved | NOT MET | D-03 OWNER DECISION MISSING (no Option A/B) |
| 6. Selected D-03 procedure prevents unsafe 5 V → ADC exposure | NOT MET | no mitigation selected; exposure unresolved at VDD = 5 V |
| 7. No execution-critical contradiction remains | NOT MET | unresolved 5 V → ADC sense exposure (C-20b-linked) for T-G4-05/06 at VDD = 5 V |
| 8. Required measurement procedures and provenance complete | MET | protocol §7/§9-15, E1-E6 templates, start pack, owner decision sheet, execution sequence complete |
| 9. No measurement data fabricated or pre-filled | MET | 0 rows ingested; templates empty; safety record explicitly NOT VERIFIED |

## Remaining Blockers

1. **D-01 OWNER DECISION MISSING** — waveform naming convention (approve or amend D-22); template delta pending.
2. **D-02 NOT CLOSED** — no current-limit element value selected; no physical verification; safety record NOT VERIFIED. (Owner or owner-delegated operator must select within ≤ ±5 mA, verify in F3, complete the safety record.)
3. **D-03 OWNER DECISION MISSING** — no Option A or B selection; 5 V → ADC exposure unresolved for T-G4-05/06 at VDD = 5 V.
4. **C-20b architecture decision OPEN** — level-shift vs 3.3 V-only path (owner decision; not a G4-execution gate, but remains open).
5. (Deferred, non-blocking for this gate) OI-16 "G4 Evidence Retrieval" artifact absent; EV-44 VOL row still NEEDS RECHECK; DS5319 Rev 20 PDF pin-down pending OI-15.

## Final Gate

**M004 NOT AUTHORIZED**

Exact remaining blockers: D-01 owner approval (waveform naming) missing; D-02 current-limit value unselected and unverified (safety record NOT VERIFIED); D-03 5 V → ADC mitigation not chosen; unresolved 5 V → ADC exposure at VDD = 5 V for T-G4-05/06; C-20b architecture decision open.

M004 may be authorized only when the owner supplies D-01, D-02 (value + physical verification recorded in the safety record), and D-03 decisions, and the 5 V exposure is closed.

END MISSION M003D.