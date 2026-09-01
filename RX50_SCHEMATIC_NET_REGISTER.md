# RX50 SCHEMATIC NET REGISTER

Status: **EMPTY / BLOCKED**
Date: 2026-08-15
Batch: RX50 SCHEMATIC CLOSURE BATCH (Phase D)
Rule: nets are registered only from a defined sheet set. No sheet exists -> no net exists -> NO NET IS INVENTED.

## Register state

- Nets registered: 0. [STATUS]
- Net names, net architecture, power nets, signal nets: NONE DEFINED. [BLOCKED]

## What would populate this register (deferred)

- Logic power/ground nets (3.3 V domain) — defined only after sheet definition.
- Firing rail nets — defined only after G1/G2 requirements.
- Continuity sense nets (MUX common/channels) — defined only after topology A/B.
- Communication nets (LoRa SPI2, RS485 USART1) — candidate only, not registered.
- Control nets (address/INH/OE/SR) — candidate only, not registered.

## Statement

The net register is intentionally empty. Re-run after RX50_SCHEMATIC_SHEET_DEFINITION.md is populated. [STATUS]

---

G4 = MEASUREMENT PENDING | G1/G2 = HOLD | G5 = PROVISIONAL / NOT LOCKED