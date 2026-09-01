# RX50 CONTRADICTION REGISTER

- Generated: 2026-08-15 by M001. Shared record of conflicting evidence.
- Rule: conflicting evidence is REPORTED, never silently resolved. A winner may be marked only when an evidence path justifies it; otherwise the item stays open.

## Open contradictions (from RX50_G4_G5_CLOSURE_AUDIT.md; not resolved)

| ID | Conflict | Severity | Evidence | Status |
|---|---|---|---|---|
| C-03 | "USART1 10 Mbps" vs DS5319 USART1 4.5 Mbit/s @3.3 V | MEDIUM | DS5319 wins (measured datasheet) | CLAIM INVALIDATED — DS5319 is authority |
| C-05 | SR control GPIO 4-5 vs 3-4 | MEDIUM | counting variance across reports | OPEN — resolve at G5 pin-map closure |
| C-06 | USART RX interrupt EXTI vs NVIC USART | MEDIUM | architectural inconsistency across reports | OPEN — resolve at G9 |
| C-20b | CD4067 5 V path: STM32 VOH 2.9 V < CD4067 VIH 3.5 V | DEFINITIVE | DS5319 VOH vs SCHS052D VIH | CONTRADICTION — RESOLUTION REQUIRED (architectural: level-shift vs 3.3 V path) — owner decision (not a G4-execution gate; fixture can buffer/level-shift control at 5 V). M003C: 5V→ADC sense exposure (5 V-referenced node read on ADC pin ≤4.0 V VIN, EV-48, no sense-node attenuation defined) is FIXTURE-ONLY and isolatable in F3 — owner mitigation (a) sense-node division/clamp ≤4.0 V, or (b) restrict 5 V node reads to channel side — required before 5 V runs of T-G4-05/06 |
| C-20c | Measured leakage regime at 3.3/5 V unknown (datasheet bounds at 18 V condition only) | — | no measured data | UNRESOLVED — MEASUREMENT/EVIDENCE MISSING (T-G4-05) |

## Resolved / closed (do not reopen without new evidence)

| ID | Item | Resolution | Evidence |
|---|---|---|---|
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
| C-21 | SN74HC595 3.3 V timing (datasheet tabulates 2/4.5/6 V only) | NOT A CONTRADICTION — evidence gap; interpolation/measurement needed |
| C-22 | STM32F103 VIN on standard pins: DS5319 Rev 18/19 = max 4.0 V vs secondary render (sheetsdata) = VDD+0.3 V (likely older revision) | RESOLVED (authority level, M003C): primary authority = ST DS5319 Rev 20 (CD00161566), device STM32F103C8/STM32F103C8T6; non-FT VIN = VSS−0.3..4.0 V (Rev 18/19 verbatim; Rev 20 current); secondary (sheetsdata) REJECTED as authority (third-party render, older-revision wording). Residual (NOT deleted): Rev 20 Table 6 page-level pin-down when PDF resident (OI-15). Governing T-G4-06 current limit (IINJ ±5 mA, EV-47) unaffected. Status: CONTRADICTION RESOLVED AT AUTHORITY LEVEL — page-level pin-down pending |

## Rules

- New contradictions found during any mission are appended here before any design change.
- A contradiction may only be marked resolved with a cited evidence path (datasheet, measurement, or owner decision).