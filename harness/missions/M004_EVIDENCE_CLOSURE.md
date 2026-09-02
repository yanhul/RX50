# M004 — Evidence Closure / G5-G9 Readiness

## Goal
Advance RX50 without modifying schematic, PCB, firmware, or BOM until the remaining evidence/contradiction gates are closed by authoritative evidence or owner decision.

## Control boundary

This mission may inventory evidence, reconcile registers, define measurement procedures, and produce HOLD/BLOCKED findings. It may not approve or commit a safety-critical design change.

## Observe

Authoritative policy: `AGENTS.md` and `harness/HARNESS.md`.
Current contradiction register: `harness/state/CONTRADICTION_REGISTER.md`.
Current controller queue item: `BC5` in `state/bc_queue.json`.

## Closure targets

- C-05: SR control GPIO conflict — resolve only from authoritative pin-map evidence/owner decision.
- C-06: USART RX interrupt architecture conflict — resolve at the applicable architecture/firmware gate.
- C-20b: CD4067 5 V control/sense path — retain HOLD until level-shift/3.3 V control and ADC exposure are explicitly evidenced/decided.
- C-20c: CD4067 leakage at the intended operating voltage — requires manufacturer evidence at the applicable condition or measurement.
- C-21: SN74HC595 3.3 V timing evidence gap — obtain datasheet evidence or measurement; do not interpolate silently.
- C-22: STM32F103 VIN authority — use the current authoritative ST datasheet; retain the page-level pin-down as an evidence task until resident evidence is available.

## Required evidence actions

1. Inventory the exact source documents, revision, and relevant sections/pages.
2. Separate manufacturer facts, requirements, calculations, measurements, assumptions, and proposals.
3. Record any newly discovered conflict in `CONTRADICTION_REGISTER.md` before proposing a design change.
4. For each closure target, produce one of: `CLOSED`, `HOLD`, or `BLOCKED` with an evidence reference.
5. Do not treat absence of evidence as evidence of compatibility.
6. Do not change schematic/PCB/firmware/BOM as part of this mission.

## Verification

A mission is complete only when the repository contains an auditable closure report and the contradiction register remains consistent with that report.

## Terminal conditions

- `DONE`: all closure targets have authoritative evidence or explicit owner decisions and no unresolved safety-critical contradiction remains.
- `HOLD`: progress is possible only after owner approval, measurement, or missing authoritative evidence.
- `BLOCKED`: a required evidence path is unavailable and no safe inference is permitted.

## Resume

Persist the mission state and resume from the first unresolved closure target. Do not reset resolved items without new contradictory evidence.
