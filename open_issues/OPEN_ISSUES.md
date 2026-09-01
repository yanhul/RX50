# RX50 OPEN ISSUES REGISTER

- Generated: 2026-08-15 by M001. Index/audit view. Root OPEN_ISSUES.md remains canonical.
- Rule: no issue is silently closed or resolved; apparent duplicates are flagged POSSIBLE DUPLICATE — REVIEW REQUIRED and NOT merged.
- Status vocabulary: HOLD / FEASIBILITY HOLD / TBD / NEEDS RECHECK / OPEN / CLOSEABLE / MEASUREMENT PENDING.

## Canonical issues (OI-01..OI-08, mirror root OPEN_ISSUES.md)

| ID | Issue | Status | Gate | Note |
|---|---|---|---|---|
| OI-01 | Simultaneous-channel load envelope (count + validated load per channel) | HOLD / TBD | G1 (master) | owner evidence; no numbers invented |
| OI-02 | Firing-power subsystem (source, rail, transient, protection, distribution, thermal, PCB paths, fault isolation) | FEASIBILITY HOLD | G2 | symbolic framework exists (firing proposal Sec B) |
| OI-03 | Output expansion 24->50 (SR count, cascade timing, OE, reset state, simultaneous update) | NEEDS RECHECK | G3 | 7x SR = CALCULATION/ASSUMPTION, not locked |
| OI-04 | Continuity subsystem 50-ch (MUX topology, leakage, ADC loading, settling, scan time, isolation, firmware scheduling) | NEEDS RECHECK | G4 | MEASUREMENT PENDING |
| OI-05 | MCU resources (GPIO, timers, SPI, ADC, RAM, flash, IRQ, comms) | NEEDS RECHECK | G5 | pin map proposal NOT locked |
| OI-06 | Communications LoRa/RS485 (address + command 50-ch, packet/state) | NEEDS RECHECK | G8 | 7-byte mask feasible |
| OI-07 | PCB and connectors (mechanical arrangement, grouping, copper, returns, segregation) | TBD | G7 | — |
| OI-08 | Safety/interlock multi-channel (reset, unintended activation, partial command, comm loss, firmware fault, power fault, OE behavior, simultaneous authorization) | NEEDS RECHECK | G6 | authorization rule OPEN |

## Derived issues discovered by audit (OI-09..OI-20)

| ID | Issue | Status | Gate | Note |
|---|---|---|---|---|
| OI-09 | CD4067 RON @3.3 V unmeasured (NOT specified by TI) | OPEN / MEASUREMENT PENDING | G4 | blocking item |
| OI-10 | CD4067 settling time: typical curves only, no guaranteed value; charge injection NOT specified | OPEN / MEASUREMENT PENDING | G4 | blocking item |
| OI-11 | STM32F103 ADC ±2 LSB guaranteed only RAIN <10 kΩ; continuity source impedance vs MUX RON must satisfy | NEEDS RECHECK | G4/G5 | measurement |
| OI-12 | Multi-channel fire authorization rule | OPEN — owner/G1 | G6 | POSSIBLE DUPLICATE of OI-08 sub-item — REVIEW REQUIRED |
| OI-13 | "Simultaneous" definition + skew budget | OPEN — owner/G1 | G1/G2 | blocks hot-fire qualification |
| OI-14 | Dry-fire harness T-F-01..03 | CLOSEABLE (structure only) | G10 | can proceed independent of G1 |
| OI-15 | Datasheet PDFs not resident in workspace; references are web hits | OPEN | — | re-pin references before BOM/schematic |
| OI-16 | "G1 Evidence Register" and "G4 Evidence Retrieval" referenced by G9 report but absent as files | OPEN | G1/G4 | missing evidence artifact |
| OI-17 | "GLVN" referenced in prior context, not analyzed in this workspace | OPEN | — | needs owner clarification; not silently resolved |
| OI-18 | SX1278 payload ceiling 255 vs 256 — pin to datasheet section/page | NEEDS RECHECK | G8 | page reference |
| OI-19 | RX24 sequence/ACK and RF-loss timeout history not in context files | NEEDS RECHECK | G8/G6 | historical record missing |
| OI-20 | SN74HC595 timing tabulated only at 2/4.5/6 V — 3.3 V values need interpolation or measurement | NEEDS RECHECK | G3 | low risk |
| OI-21 | T-G4-06 current-limit element value + physical verification record (bound now VERIFIED ≤ ±5 mA, EV-47/EV-45) | OPEN / BLOCKED — owner policy recorded (M003E: DO NOT lock a numerical value yet); value + physical verification still pending | G4 | M003D: no value selected; safety record `measurements/T-G4-06_CURRENT_LIMIT_SAFETY_RECORD.md` created but **NOT VERIFIED / INCOMPLETE**; M003E: owner policy = |I_fault| ≤ 5 mA is a bound, NOT the selected test current; operator must identify F3 fault path, select element, verify worst-case current, physically verify, record E6 CURRENT_LIMIT; T-G4-06 BLOCKED until then |
| OI-22 | 5V-fault/leakage scenarios vs ADC pin VIN abs max 4.0 V (EV-48) — routing/attenuation | CLOSEABLE — owner decision RESOLVED (D-03 Option B, M003E); closure = execution constraint applied | G4/G5 | M003E: owner APPROVED Option B — characterize CD4067/channel-side at 5 V, do NOT expose 5 V-referenced sense node to STM32 ADC, no clamp/divider invented; execution sequence §5.3 constraint added. C-20b (architecture) remains OPEN separately — NOT closed by D-03 |

## Contradiction-linked issues

- See CONTRADICTION_REGISTER.md C-01..C-06; each open contradiction implies an issue to resolve before closure of the relevant gate.