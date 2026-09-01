# RX50 SCHEMATIC PIN CONFLICT REPORT

Status: **PROVISIONAL** — carries prior audit findings; NOT a final schematic audit
Date: 2026-08-15
Batch: RX50 SCHEMATIC CLOSURE BATCH (Phase E input)
Basis: RX50_G4_G5_CLOSURE_AUDIT.md Section 9 (37-pin audit) and Section 12 (SPI) — evidence-based findings carried forward, NOT a new lock.

## Findings (candidate maps, PROVISIONAL)

| # | SEVERITY | PIN / AREA | FINDING | STATUS |
|---|---|---|---|---|
| C-01 | WATCH | PA4 (SPI1_NSS) | monitor-ADC use is safe ONLY while SPI1 stays entirely unused (latent dual-use) | PROVISIONAL |
| C-02 | CONDITIONAL | PA15/PB3/PB4 (JTDI/JTDO/JNTRST) | usable as GPIO only after SWJ_CFG='010' (JTAG off, SWD kept) | PROVISIONAL |
| C-03 | CONDITIONAL | PB2 (BOOT1) | usable as GPIO only when BOOT0=0 (main-flash boot) | PROVISIONAL |
| C-04 | CONDITIONAL | PC13/14/15 | VBAT domain, limited drive (~+-3 mA); LEDs/INH ok; not safety-critical; conflicts with future LSE/RTC | PROVISIONAL |
| C-05 | NO CONFLICT | continuity ADC (PA0-3 or PA0) | never reassigned to SPI/USART in candidates | PROVISIONAL |
| C-06 | NO CONFLICT | LoRa SPI2 (PB12-15), RS485 USART1 (PA9/10), SR (PB3-5) | no overlap in candidates | PROVISIONAL |

## Statement

- No HARD conflict exists in the candidate maps under the four conditional rules (Section 9.1 of the closure audit). [STATUS]
- These findings are PROVISIONAL and tied to candidate maps; they become part of a FINAL audit only after the G5 pin map is locked. No pin is locked here. [STATUS]

---

G5 = PROVISIONAL / NOT LOCKED | G4 = MEASUREMENT PENDING | G1/G2 = HOLD