# RX50 WORKING ENGINEERING ENVELOPE — G1/G4 BRIDGE

Status: WORKING / NON-AUTHORITATIVE
Purpose: unblock engineering preparation without pretending owner requirements or physical measurements exist.

## Rules
- This document MUST NOT close G1, G2, G4, G5 or G6.
- Every value below is a test/design placeholder, not an owner requirement.
- No RX24 firing-power number is inherited.
- Any value used in a schematic or PCB decision must be replaced by owner/datasheet/measurement evidence.

## G1 provisional test envelope
Use bounded scenarios rather than inventing a production requirement:
- concurrency: sweep 1, 2, 4, 8, 16, 25, 50 channels;
- load: characterize the actual load connected to the DUT before electrical sizing;
- pulse: characterize the actual firing waveform at the load and record peak current, pulse width, voltage and energy;
- timing: measure actual channel skew at the same electrical event; do not infer from MCU instruction timing;
- rail: record battery/firing-rail voltage during each concurrency point;
- protection: capture rail sag/transient and fault response.

Acceptance status: TBD until owner defines the required operating point.

## G4 execution order
1. Fixture identity + calibration evidence.
2. CD4067 RON at the actual VDD used by the design, including 3.3 V if that is the candidate.
3. VIH/VIL of the control path at the actual logic voltage.
4. ADC error versus measured RAIN across the intended input range.
5. Settling after address/channel transitions; preserve waveform files.
6. Off-channel leakage.
7. Cross-channel isolation/fault-injection cases.

## Promotion rule
Raw measurements may promote a G4 sub-test only when DUT, trial, VDD, temperature, instrument, calibration status, operator, timestamp and raw result are present.

## Immediate engineering consequence
Until measurements exist:
- placement/routing may be prepared structurally but must not claim electrical feasibility;
- no firing-current copper width, MOSFET rating, connector rating, thermal limit or simultaneous-fire PASS may be promoted;
- G1 remains owner/evidence gated;
- G4 remains measurement gated.
