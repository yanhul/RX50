# RX50 Pin / Resource Audit — STRICT AUTO

Status: `PROVISIONAL — NO LOCK`

Purpose: audit the current provisional architecture for resource collisions without converting proposals into a locked hardware pinout.

## Deterministic checks

| Resource | Current proposal | Result |
|---|---|---|
| SWD | PA13 / PA14 | PASS — reserved |
| ADC sense | PA0–PA3 | PASS — four distinct candidates |
| MUX address | PB4–PB7 | PASS — four distinct candidates |
| MUX enable | PB8 | PASS — distinct from address candidates |
| RS485 | PA8–PA10 | PASS — no collision with ADC candidates |
| LoRa SPI2 | PB12–PB15 | PASS — no collision with MUX/RS485 candidates |
| LoRa RST/DIO0 | PB11/PB10 | PASS — no collision with SPI2 candidates |
| Shift-register GPIO | not assigned | OPEN — cannot audit final mapping |

## Capacity checks

- 4 × 16:1 MUX provides 64 selectable positions for 50 logical continuity channels. This is a capacity statement, not proof of electrical suitability.
- 7 × 74HC595 provides 56 serial bit positions for 50 logical outputs. Six positions are unused at architecture level.

## Strict findings

1. No collision exists among the currently proposed MCU resources listed above.
2. Final shift-register GPIO assignment remains OPEN and must not be inferred from “unused” pins without checking the complete MCU pin/function table.
3. CD4067 electrical behavior at the intended supply/logic conditions remains an evidence gap; this audit does not close it.
4. The output/firing stage remains intentionally undefined. No firing electrical parameters are introduced here.
5. Connector pinout and final harness mapping remain OPEN.

## Decision

`AUDIT PASS — PROVISIONAL ONLY` for the resources explicitly listed. No pin or topology lock is authorized by this artifact.

Next automatic action: cross-check any future pin assignment against this register and fail on duplicate allocation or unauthorized conversion of PROVISIONAL/OPEN rows to LOCKED.
