# RX50 G5 PIN MAP FINAL

Status: **NOT LOCKED** — G5 remains PROVISIONAL
Date: 2026-08-15
Batch: RX50 SCHEMATIC CLOSURE BATCH (Phase B)
Rule (owner direction): close G4 by evidence BEFORE locking G5. G4 has no measurement data -> G5 pin map is NOT finalized. No pin assignment is locked in this file.

## Candidate pin maps (PROVISIONAL only — NOT final)

Reference: RX50_G4_G5_CLOSURE_AUDIT.md Section 9 (candidate maps A/B) and RX50_G4_G5_HARDWARE_FEASIBILITY_REPORT.md. These remain CONDITIONAL candidates and are NOT locked.

## Conditional rules that a final map must satisfy (carried from audit)

1. SWJ_CFG = '010' (JTAG off, SWD kept) to free PA15/PB3/PB4. [CONSTRAINT]
2. BOOT0 strapped low to free PB2 as GPIO. [CONSTRAINT]
3. SPI1 left entirely unused so PA4 (SPI1_NSS) monitor-ADC use stays conflict-free (latent watch). [CONSTRAINT]
4. PC13-15 limited to status LEDs / high-Z INH lines (VBAT domain, ~+-3 mA drive); not for safety-critical functions. [CONSTRAINT]
5. OE of the 74HC595 is interlock-owned (G6), NOT an MCU GPIO. [CONSTRAINT]
6. Continuity ADC allocation depends on topology A/B (undecided) -> PA0-3 (A) or PA0 (B). [CONSTRAINT]

## Statement

- No pin assignment is locked. [STATUS]
- GPIO/ADC/MUX/control/OE/INH allocation is deferred until: G4 evidence-backed + topology A/B owner decision + G6 authorization evidence. [STATUS]

---

G5 = PROVISIONAL / NOT LOCKED | G4 = MEASUREMENT PENDING | G1/G2 = HOLD