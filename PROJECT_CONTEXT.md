# RX50 PROJECT CONTEXT

## Purpose

This workspace is the continuation of an existing RX24 engineering discussion.
RX24 is the baseline. RX50 is the new target: 50 output channels, with simultaneous firing capability as a requirement to be evaluated.

This file is a CONTEXT HANDOVER, not a fresh design specification.

## Working rules

- Do not invent component part numbers, electrical limits, current, timing, thermal limits, or other numerical specifications.
- Distinguish clearly between LOCKED, EVIDENCE-BACKED, HOLD, TBD, and NEEDS RECHECK.
- Treat previous RX24 decisions as baseline only; any item affected by scaling to 50 channels must be re-evaluated.
- Do NOT carry forward the old `MAX_CONCURRENT_FIRE = 1` constraint. RX50 explicitly requires evaluation of simultaneous multi-channel firing.
- Do not silently replace missing evidence with assumptions.
- Safety-critical changes require explicit review before implementation.
- Prefer manufacturer datasheets, measurements, and explicit requirements as evidence.
- Keep source evidence separate from engineering conclusions.

## RX24 baseline currently known

### Core architecture
- MCU: STM32F103C8T6, LQFP48.
- LoRa: SX1278 / Ra-02.
- RS485: MAX3485.
- Input: 3S Li-ion, nominal system range previously treated as 9.0–12.6 V.
- Reverse-polarity protection: AO4407A P-MOS.
- Input TVS: SMBJ15CA.
- Logic regulator: TPS562201 to 3.3 V.
- Output MOSFET baseline: IRLML6344.
- Output expansion baseline: 74HC595 shift registers.
- Continuity multiplexer baseline: CD4067.
- Safety/interlock logic uses dedicated logic gates and an MCU-controlled arm path.
- Architecture, pin assignment, safety concept, connector topology, and schematic sheets were previously treated as locked for RX24 Rev.A, subject to re-review where RX50 scaling affects them.

### RX24 continuity subsystem baseline
Previously discussed:
- Per-channel divider and post-MUX ADC network.
- ADC source impedance was identified as a design concern.
- CD4067 leakage and settling time were identified as relevant.
- Continuity scan timing was revised to a more conservative value during review.

For RX50, do not reuse old timing or channel-scaling conclusions without recalculation/evidence.

### RX24 firmware / control baseline
- Channel state is managed through shift-register based output expansion rather than requiring one MCU GPIO per output.
- Safety behavior was designed around outputs defaulting OFF on reset/power loss/firmware fault/RF loss.
- LoRa and RS485 are part of the control architecture.

## RX50 delta-review scope

The first engineering pass should classify each area as KEEP / MODIFY / REPLACE / TBD:

1. Output expansion: 24 -> 50 channels.
2. Shift-register count, cascade timing, OE/safety behavior.
3. MCU resource allocation and firmware channel map.
4. Continuity measurement and multiplexing for 50 channels.
5. Firing-power subsystem and simultaneous-channel capability.
6. Protection, power distribution, grounding, and PCB current paths.
7. Connectors and mechanical channel grouping.
8. RF/RS485 protocol capacity and channel addressing.
9. Firmware state machine, fault handling, and simultaneous-command handling.
10. Safety/interlock behavior under multi-channel operation.
11. Test and validation requirements.

## Important status

The firing-power subsystem was previously placed on FEASIBILITY HOLD because its actual commercial-load envelope and simultaneous-load requirements had not been sufficiently locked.

Therefore RX50 must NOT assume a firing-power design is already validated.

## What is NOT available as authoritative input

The historical RX24 work spans multiple ChatGPT sessions. This context is a consolidated handover, not a verbatim export of every historical message or every datasheet.

If an old decision is not represented here, mark it NEEDS RECHECK rather than reconstructing it from memory.

## Immediate next task

Create an RX50 delta audit against this baseline before making design changes.

The audit should identify:
- what can remain unchanged,
- what must scale,
- what must be redesigned,
- what evidence is missing,
- and which decisions must be made before schematic/PCB work.
