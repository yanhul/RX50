# RX50 DECISION REGISTER

- Generated: 2026-08-15 by M001. Shared source of truth for decisions.
- Status vocabulary: LOCKED / OWNER-APPROVED / EVIDENCE-BACKED / HOLD / TBD / NEEDS RECHECK / BASELINE-ONLY / PROVISIONAL / OPEN.
- OWNER-APPROVED = explicit owner decision recorded in a mission report; may be fixture/test-procedure scope (not necessarily an RX50 architecture decision). LOCKED = explicitly approved + recorded in DECISIONS.md.
- Rule: no decision may be recorded as LOCKED without explicit owner approval + evidence path.
- Note: root DECISIONS.md remains the canonical locked-decision file; this register is the index/audit view.

## Locked decisions (D-01..D-06, from DECISIONS.md)

| ID | Decision | Status | Evidence / source |
|---|---|---|---|
| D-01 | RX50 is a continuation of RX24, not a ground-up redesign | LOCKED | DECISIONS.md (owner direction) |
| D-02 | Target channel count = 50 | LOCKED | DECISIONS.md |
| D-03 | Simultaneous multi-channel firing required to be supported/evaluated | LOCKED | DECISIONS.md |
| D-04 | RX24 MAX_CONCURRENT_FIRE=1 is obsolete for RX50 | LOCKED | DECISIONS.md |
| D-05 | RX24 remains the baseline for comparison | LOCKED | DECISIONS.md |
| D-06 | Evidence-first engineering is mandatory | LOCKED | DECISIONS.md |

## Baseline-only decisions (NOT locked for RX50; re-verify before reuse)

| ID | Decision | Status | Evidence / source |
|---|---|---|---|
| D-07 | MCU STM32F103C8T6 baseline candidate | BASELINE-ONLY / NEEDS RECHECK | PROJECT_CONTEXT.md |
| D-08 | LoRa SX1278 / Ra-02 baseline | BASELINE-ONLY / NEEDS RECHECK | PROJECT_CONTEXT.md |
| D-09 | RS485 MAX3485 baseline | BASELINE-ONLY / NEEDS RECHECK | PROJECT_CONTEXT.md |
| D-10 | 74HC595 output-expansion concept | BASELINE-ONLY / NEEDS RECHECK | PROJECT_CONTEXT.md |
| D-11 | CD4067 continuity-MUX concept | BASELINE-ONLY / NEEDS RECHECK | PROJECT_CONTEXT.md |
| D-12 | Dedicated HW safety/interlock concept | BASELINE-ONLY / NEEDS RECHECK | PROJECT_CONTEXT.md |
| D-13 | 3.3 V logic rail architecture | BASELINE-ONLY / NEEDS RECHECK | PROJECT_CONTEXT.md |
| D-14 | Input 3S Li-ion 9.0-12.6 V | PROVISIONAL (re-verify at power design) | PROJECT_CONTEXT.md |

## Explicitly NOT carried forward

| ID | Decision | Status |
|---|---|---|
| D-15 | Any firing-current / pulse / energy / voltage / timing value | NONE SPECIFIED — HOLD (do not invent) |

## Derived / proposal status (NOT locked)

| ID | Decision | Status | Evidence / source |
|---|---|---|---|
| D-16 | OE-high (3-state) blanking as output-inhibition mechanism; storage register undefined at power-up | EVIDENCE-BACKED (TI SCLS041J) + RECOMMENDATION for design | RX50_FEASIBILITY_G3_G4_G5_G6_G8.md |
| D-17 | SR count = 7, MUX count = 4 (1:1 fan-out) | CALCULATION / ASSUMPTION — NOT locked | BATCH_ENGINEERING / FEASIBILITY reports |
| D-18 | Pin-map proposal (LoRa on SPI2, RS485 USART1, continuity Option A/B) | PROPOSAL — NOT locked | FEASIBILITY G5 / G9 |
| D-19 | Continuity topology A vs B | OPEN — no selection made | G4 TOPOLOGY matrix (OPEN) |
| D-20 | "Simultaneous" definition (command-edge vs threshold-within-skew) | OPEN — owner/G1 | FIRING_DESIGN_PROPOSAL_FOR_REVIEW |
| D-21 | Segmented firing command chain (requirement->authorization->interlock->SR+OE->switch; firmware never sole gate) | RECOMMENDATION — awaiting owner approval | FIRING_DESIGN_PROPOSAL_FOR_REVIEW Sec D |
| D-22 | G4 waveform file-naming convention (D-01): `<TEST_ID>_<DUT_ID>_N<channel_or_node>_TR<seq>.<ext>` (e.g., T-G4-04_DUT-001_N12_TR01.CSV); WAVEFORM_FILE = exact filename; original filenames preserved on handoff | OWNER-APPROVED (D-01, M003E) | owner decision M003E (2026-08-15): APPROVED — D-22 proposal, do not alter; owner-approved G4 data-handoff convention; template note applied |
| D-23 | G4 5 V fault / ADC routing (D-03): OPTION B — for G4 5 V characterization, characterize CD4067/channel-side behavior as required by protocol; do NOT expose the 5 V-referenced sense node directly to the STM32 ADC input; do NOT invent an attenuation/clamp network; ADC observations requiring valid STM32 ADC range performed under an appropriate supply/test condition; preserve CD4067-side 5 V vs MCU ADC distinction | OWNER-APPROVED — FIXTURE/TEST-PROCEDURE DECISION (NOT an RX50 architecture decision) | owner decision M003E (2026-08-15): APPROVED — Option B; execution sequence updated (5 V runs must not connect 5 V-referenced sense node to STM32 ADC) |
| D-24 | G4 T-G4-06 current-limit element numerical value (D-02) | OWNER POLICY RECORDED — NUMERICAL ELEMENT VALUE PENDING PHYSICAL FIXTURE VERIFICATION | owner decision M003E (2026-08-15): DO NOT LOCK a numerical current-limit element value yet; bound |I_fault| ≤ 5 mA is a maximum permissible bound (EV-47/EV-45), NOT the selected test current; operator must identify F3 fault path, select element, verify worst-case current, physically verify installed element, record in E6 CURRENT_LIMIT, then permit T-G4-06 |
| D-25 | T-G4-06 operator re-delegation (OD-1..OD-4): OD-1 REQUIRED TEST LEVEL (operator selects/records fault stimulus as TEST VALUE); OD-2 SHORT REFERENCE (operator selects/records electrical reference for short as TEST VALUE / fixture implementation); OD-3 FAULT SOURCE INTERFACE (operator selects/records source type, terminals, polarity, allowable source condition as fixture TEST VALUE); OD-4 CURRENT MEASUREMENT POINT/METHOD (operator selects/records method+point to verify \|I_fault\| ≤ 5 mA) | OWNER-APPROVED — OPERATOR RE-DELEGATION (TEST VALUE / fixture implementation; NOT design requirements) | owner decision (T-G4-06 OWNER RE-DELEGATION — FINAL RESOLUTION, 2026-08-15): re-delegates OD-1..OD-4 to the operator with constraints — never convert ≤5 mA bound into I_TEST=5 mA; never invent a numerical component value; every selected item labelled TEST VALUE or fixture implementation (never design requirement); current-limiter element still physically verified; E6 CURRENT_LIMIT mandatory; injection LAST; removal FIRST; 5 V-referenced sense node not connected directly to STM32 ADC; no RX50 architecture modification; no measurement; no M004 authorization |

## Rules

- This register is updated at every gate close / new decision; root DECISIONS.md updated only with owner approval.
- No silently resolved conflict: any conflicting evidence is logged in CONTRADICTION_REGISTER.md.
