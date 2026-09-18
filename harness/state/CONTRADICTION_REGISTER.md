# RX50 CONTRADICTION REGISTER

- Generated: 2026-08-15 by M001. Shared record of conflicting evidence.
- Rule: conflicting evidence is REPORTED, never silently resolved. A winner may be marked only when an evidence path justifies it; otherwise the item stays open.

## Open contradictions (from RX50_G4_G5_CLOSURE_AUDIT.md; not resolved)

| ID | Conflict | Severity | Evidence | Status |
|---|---|---|---|---|
| C-03 | "USART1 10 Mbps" vs DS5319 USART1 4.5 Mbit/s @3.3 V | MEDIUM | DS5319 wins (measured datasheet) | CLAIM INVALIDATED — DS5319 is authority |
| C-05 | SR control GPIO 4-5 vs 3-4 | MEDIUM | counting variance across reports | OPEN — signal count corrected to 3-4; final MCU pin allocation still requires owner-approved G5 pin-map evidence |
| C-20b | CD4067 5 V path: conditional STM32 VOH(VDD) vs CD4067 VIH 3.5 V | HIGH | DS5319 Table 37 + Table 9; SCHS052D; RX50 project_state.md | EVIDENCE GAP — source arithmetic is valid conditionally, but RX50 3.3 V logic rail is baseline-only/not locked; owner VDD evidence required before promotion. Separate 5V→ADC sense exposure mitigation remains required before 5 V T-G4-05/06 runs |
| C-20c | Measured leakage regime at 3.3/5 V unknown (datasheet bounds at 18 V condition only) | — | no measured data | MEASUREMENT REQUIRED — T-G4-05 physical results and owner acceptance limit absent |

## Resolved / closed (do not reopen without new evidence)

| ID | Item | Resolution | Evidence |
|---|---|---|---|
| C-06 | USART RX interrupt routing | RESOLVED: USART RX uses NVIC USART RXNE; EXTI is reserved for external interrupt sources such as DIO0 and fault/arm. Historical EXTI wording is retained only as provenance. | `RX50_G4_G5_CLOSURE_AUDIT.md` §16/E-06; `RX50_G9_FIRMWARE_AND_CROSS_GATE_REPORT.md` §5.2/§7 |
| C-10 | RAIN 50 kΩ @ tS=55.5 cyc, fADC=14 MHz | CONFIRMED CORRECT (no conflict) | DS5319 Table 48 |
| C-11 | CADC = 8 pF | CONFIRMED CORRECT | DS5319 |
| C-12 | "80k / 350k" extract | DIFFERENT DEVICE, not applicable | source resolved |
| C-01 | "4 parallel ADC conversions" vs 2x ADC | RESOLVED (model correction, M002): STM32F103 has 2 ADCs; dual regular simultaneous mode converts the SAME channel; 4 distinct channels require sequential conversions. Scan floor corrected to 64 µs (1 ADC) / 32 µs (2 ADC). Actual scan timing still unmeasured (evidence gap, not a contradiction). | DS5319 (2 ADCs); M002 audit |
| C-02 | Continuity scan floor 17.7 µs vs ~64 µs | RESOLVED (derivation correction, M002): tCONV includes tS (tCONV = tS + 12.5, DS5319 Table 47); 17.7 µs double-counted. Corrected floors: A=64 µs (1 ADC) / 32 µs (2 ADC), B=50 µs — lower bounds, omitting select/settle/software. No measured scan time exists; no owner scan-time requirement exists. | DS5319 Table 47/48; M002 audit |
| C-04 | Continuity leakage Option B 50 µA vs 63 µA | RESOLVED for theoretical bound (M002): shared node up to 63 OFF channels x 1000 nA = 63 µA worst-case at 18 V condition. Measured leakage at 3.3/5 V remains UNRESOLVED — MEASUREMENT/EVIDENCE MISSING (T-G4-05). | SCHS052D leakage; closure audit S-19/E-04; M002 audit |

## Flagged but NOT yet classified (review required)

| ID | Item | Status |
|---|---|---|
| C-20 | GLVN (referenced in prior context, not analyzed here) | NOT ANALYZED — cannot rule in/out; owner clarification required |
| C-21 | SN74HC595 3.3 V timing (datasheet tabulates 2/4.5/6 V only) | EVIDENCE GAP — no authoritative 3.3 V guarantee; interpolation is not a guarantee; manufacturer evidence or measurement required |
| C-22 | STM32F103 VIN on standard pins: DS5319 Rev 18/19 = max 4.0 V vs secondary render (sheetsdata) = VDD+0.3 V (likely older revision) | RESOLVED (authority level, M003C): primary authority = ST DS5319 Rev 20 (CD00161566), device STM32F103C8/STM32F103C8T6; non-FT VIN = VSS−0.3..4.0 V (Rev 18/19 verbatim; Rev 20 current); secondary (sheetsdata) REJECTED as authority (third-party render, older-revision wording). Residual (NOT deleted): Rev 20 Table 6 page-level pin-down when PDF resident (OI-15). Governing T-G4-06 current limit (IINJ ±5 mA, EV-47) unaffected. Status: CONTRADICTION RESOLVED AT AUTHORITY LEVEL — page-level pin-down pending |

## Rules

- New contradictions found during any mission are appended here before any design change.
- A contradiction may only be marked resolved with a cited evidence path (datasheet, measurement, or owner decision).

## Phase 2 reconciliation provenance

- **C-05:** `RX50_G4_G5_CLOSURE_AUDIT.md` §13 and `RX50_S03_OUTPUT_LOGIC.sch` establish 3 mandatory SR signals plus optional `SRCLR`; `OE` is interlock-owned. `RX50_G5_PIN_MAP_FINAL.md` and `RX50_SCHEMATIC_NET_REGISTER.md` establish that final pin allocation remains unregistered and not locked.
- **C-06:** `RX50_G4_G5_CLOSURE_AUDIT.md` §16/E-06 and `RX50_G9_FIRMWARE_AND_CROSS_GATE_REPORT.md` §5.2/§7 classify USART RX as NVIC `RXNE`; EXTI is for external sources such as DIO0 and fault/arm. The former EXTI wording is retained as historical provenance only; C-06 is not simultaneously OPEN.
- **C-20b/C-20c/C-21:** detailed closure, decision matrix, measurement requirements, and verification invariants are in `PHASE2_EVIDENCE_CLOSURE.md`; C-20b remains an evidence gap until RX50 MCU VDD is authoritative/locked.
