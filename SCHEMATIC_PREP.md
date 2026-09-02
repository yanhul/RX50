# RX50 SCHEMATIC PREPARATION / GATE REPORT

Status: PRE-SCHEMATIC — engineering gates still open
Date: 2026-09-02

## Objective

Advance RX50 from the existing evidence/audit package toward a real schematic without inventing safety-critical electrical values.

## Current authoritative constraints

- Target: 50 channels.
- Simultaneous multi-channel firing must be supported/evaluated.
- RX24 is a baseline only; the old single-channel firing constraint is not carried forward.
- Firing/load envelope is not closed.
- Firing-power architecture is therefore not closed.
- CD4067 RON at 3.3 V is not specified by the manufacturer and requires measurement if that supply path is selected.
- A 5 V CD4067 control path cannot rely on the STM32 guaranteed 3.3 V VOH to satisfy the documented 5 V VIH; level shifting or another validated interface is required.
- ADC accuracy guarantee requires the source impedance condition documented in the existing audit; divider values must not be invented.

## Schematic partition

### Sheet 1 — MCU / control
Candidate baseline:
- STM32F103C8T6
- SWD
- reset
- clock
- 3.3 V logic
- SPI/USART interfaces

Status: architecture candidate; final pin map requires G5 closure.

### Sheet 2 — RF / RS485
Candidate baseline:
- SX1278 / Ra-02
- MAX3485
- MCU interface

Status: protocol and final pin assignment require G8/G5 closure.

### Sheet 3 — 50-channel output expansion
Candidate baseline:
- 74HC595 cascade concept
- shared SER/SRCLK/RCLK
- hardware output-enable/blanking path
- 50 logical output channels

Structural calculation: 50 channels require at least seven 8-bit registers if the 1:1 fan-out concept is retained.

Status: G3 candidate only. Actual firing/output stage is BLOCKED by G1/G2 load-envelope closure.

### Sheet 4 — Continuity measurement
Candidate baseline:
- four 16:1 CD4067 groups to cover 50 channels
- address/select control
- ADC sense paths

Preferred topology from existing G4 analysis: four isolated MUX sense nodes rather than a single shared ADC node.

Status: candidate only. CD4067 RON@3.3 V and settling are not manufacturer-guaranteed; measurement/decision required before pinning divider values or claiming ADC accuracy.

### Sheet 5 — Safety / interlock
Candidate baseline:
- dedicated hardware interlock
- output-enable ownership outside normal data shifting
- default-OFF behavior

Status: G6 review required for simultaneous activation authorization and fault behavior.

### Sheet 6 — Power / protection
Candidate baseline:
- input protection concept
- logic regulator concept
- separate firing-power domain concept

Status: firing-power portion BLOCKED by G1/G2. Do not place unverified current paths, protection ratings, copper requirements, or thermal values into a released schematic.

### Sheet 7 — Connectors / channel grouping
50-channel connector/channel grouping is not yet locked.

Status: G7 TBD.

## Gate matrix

| Gate | Subject | Status | Schematic impact |
|---|---|---|---|
| G1 | simultaneous load envelope | HOLD | blocks firing-power design |
| G2 | firing-power feasibility | HOLD | blocks output power stage |
| G3 | output expansion | NEEDS RECHECK | 74HC595 topology candidate available |
| G4 | continuity | NEEDS RECHECK | MUX topology candidate available; RON/settling open |
| G5 | MCU/pin map | NEEDS RECHECK | candidate only |
| G6 | safety/interlock | NEEDS RECHECK | safety net ownership must be closed |
| G7 | PCB/connectors | TBD | connector/grouping not locked |
| G8 | protocol | NEEDS RECHECK | command/address semantics not locked |

## Decision

Do NOT mark the RX50 schematic as RELEASED or VALIDATED.

A real released schematic cannot currently be completed without either:
1. closing the remaining gates with evidence/decisions, or
2. deliberately creating a draft schematic with every unresolved net/value explicitly marked TBD/HOLD.

The second route must not be represented as a production-ready design.

## Next action

Close G1/G2 and the remaining G3/G4/G5/G6/G8 decision points, then generate the actual EDA schematic and run connectivity/ERC review.
