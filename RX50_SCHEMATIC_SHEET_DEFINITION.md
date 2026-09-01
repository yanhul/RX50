# RX50 SCHEMATIC SHEET DEFINITION

Status: **BLOCKED — NOT DEFINED**
Date: 2026-08-15
Batch: RX50 SCHEMATIC CLOSURE BATCH (Phase D)
Rule: no sheet hierarchy / component allocation / net architecture can be locked while architecture (Phase D input) is itself unlocked.

## Sheet definition state

- Sheet hierarchy: NOT DEFINED. [BLOCKED]
- Component/function allocation per sheet: NOT DEFINED. [BLOCKED]
- Power domains (logic 3.3 V; firing rail; input rail): NOT DEFINED (firing rail requirements absent, G1/G2 HOLD). [BLOCKED]
- Safety states (default-OFF, OE, interlock): NOT DEFINED (G6 authorization evidence absent). [BLOCKED]
- Net architecture: NOT DEFINED (requires sheets). [BLOCKED]

## What must close before this file can be filled

1. RX50_SCHEMATIC_ARCHITECTURE_LOCK.md -> LOCKED (requires G4 evidence + topology A/B + G5 pin map + G1/G2).
2. G5 pin map final -> LOCKED.
3. G1/G2 requirement closure -> EVIDENCE-BACKED.

## Statement

No schematic sheet is defined. Nothing in this file is a component selection or net. Re-run this phase after the listed prerequisites close. [STATUS]

---

G4 = MEASUREMENT PENDING | G1/G2 = HOLD | G5 = PROVISIONAL / NOT LOCKED