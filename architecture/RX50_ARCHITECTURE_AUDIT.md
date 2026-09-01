# RX50 Architecture Audit — STRICT

Status: `PROVISIONAL — AUDIT PASS WITH OPEN ITEMS`

This audit checks the current architecture document for internal consistency. It does not authorize a build-ready firing circuit or close physical/safety validation.

## Checks

| Check | Result | Note |
|---|---|---|
| MCU baseline | PASS | STM32F103C8T6 identified as architecture baseline. |
| SWD reservation | PASS | PA13/PA14 reserved. |
| ADC allocation | PASS | PA0–PA3 are four candidate ADC inputs. |
| 4×16:1 continuity coverage | PASS | 64 selectable positions cover 50 logical channels with unused positions. |
| 7×74HC595 bit capacity | PASS | 7 registers provide 56 bit positions for 50 logical channels; six remain unused. |
| LoRa interface | PROVISIONAL | Candidate SPI2/control allocation only. |
| RS485 interface | PROVISIONAL | Candidate USART1/DE allocation only. |
| Shift-register pin assignment | OPEN | Final GPIO allocation is intentionally not locked. |
| CD4067 @3.3 V RON | NOT PROVEN | No interpolation from 5/10/15 V datasheet points permitted. |
| Continuity settling/leakage | NOT PROVEN | Physical characterization remains open. |
| Firing stage | OPEN | No firing-power values or build-ready firing circuit specified. |
| Safety authorization | OPEN | Owner/safety gate remains required. |

## Contradiction status

No new contradiction is introduced by the architecture document itself. The previously identified CD4067 3.3 V uncertainty remains explicitly OPEN rather than being silently resolved.

## Decision

The architecture is internally coherent enough to continue schematic-level documentation as `PROVISIONAL`. It is **not** a release/freeze approval and does not establish hardware validation.

Next autonomous step: use this audit to drive the provisional net register and identify any concrete pin/resource contradictions before attempting any lock.
