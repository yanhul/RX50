# RX50 DECISIONS

## Confirmed direction

- RX50 is a continuation of RX24, not a ground-up redesign.
- Target channel count: 50.
- Simultaneous multi-channel firing is required to be supported/evaluated.
- The old RX24 `MAX_CONCURRENT_FIRE = 1` constraint is obsolete for RX50.
- RX24 remains the baseline for comparison.
- Evidence-first engineering is mandatory.

## RX24 baseline decisions that may remain valid

These are baseline decisions, NOT automatically locked for RX50:
- STM32F103C8T6 MCU baseline.
- SX1278 / Ra-02 LoRa baseline.
- MAX3485 RS485 baseline.
- 74HC595-based output expansion concept.
- CD4067-based continuity measurement concept.
- Dedicated hardware safety/interlock concept.
- 3.3 V logic rail architecture.

## Decisions deliberately NOT carried forward

- Maximum concurrent firing = 1: NOT VALID for RX50.
- Any old firing-current or pulse assumptions: NOT VALID unless re-established from requirements/evidence.
- Any old simultaneous-load power budget: NOT VALID unless re-established.
- Any old 24-channel timing estimate: NOT VALID for 50 channels without recalculation.

## Decision status vocabulary

- LOCKED: explicitly approved and not currently under review.
- EVIDENCE-BACKED: supported by authoritative evidence but not necessarily architecturally frozen.
- HOLD: cannot be finalized yet.
- TBD: required information is missing.
- NEEDS RECHECK: historical information exists but must be verified before reuse.
