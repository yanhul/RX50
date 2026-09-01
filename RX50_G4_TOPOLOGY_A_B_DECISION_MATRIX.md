# RX50 G4 TOPOLOGY A vs B DECISION MATRIX

Status: COMPLETE (Part G of batch G4-MEAS-BATCH-01)
Date: 2026-08-15
Rule: A or B is NOT selected arbitrarily. Cells use only evidence available at the date of this batch; where evidence is absent the cell reads UNKNOWN / MEASUREMENT PENDING. Final choice = UNDECIDED until measurements exist and the owner records the decision.

| CRITERION | TOPOLOGY A (4x CD4067 -> 4 ADC pins) | TOPOLOGY B (4x CD4067 -> 1 shared ADC node) | EVIDENCE | STATUS | ADVANTAGE | RISK | REQUIRED MEASUREMENT | DECISION |
|---|---|---|---|---|---|---|---|---|
| Source impedance (RON) | single RON path per ADC node; Rth + RON + rtrace | single RON, or 2x RON if 2nd-stage MUX; worse for RAIN<10k | RON@5V 1050 ohm max (SCHS052D); RON@3.3V NOT SPECIFIED | MEASUREMENT PENDING (RON@3.3 V) | A: one RON per path | B: series RON hurts 10 k budget | T-G4-01 | UNDECIDED |
| Leakage population | per-MUX node sees own 15 OFF channels -> 15 uA theoretical (18 V condition) | shared node sees up to 63 OFF -> 63 uA theoretical (18 V condition) | SCHS052D leakage; audit correction E-04 | EVIDENCE-BACKED (theoretical bounds) | A: bounded per node | B: 4x accumulation on one node | T-G4-05 (3.3/5 V actual) | A favored on bound |
| Settling path | independent per-node RC; parallel settles | single shared node settles once per address step | no guaranteed settling in datasheet | MEASUREMENT PENDING | A: per-node isolation of settle | B: shared-node coupling | T-G4-04 | UNDECIDED |
| Isolation / blast radius | fault limited to one MUX group | single point affects all 50 | audit Section 7; structural | EVIDENCE-BACKED (structural) | A: group-level containment | B: system-level single point | T-G4-06 | A favored (structural) |
| ADC source impedance budget | 4 channels, each must meet <10 k | 1 channel; series RON (B, 2nd stage) pressures budget | DS5319 +-2 LSB @ RAIN<10 k | EVIDENCE-BACKED (constraint) | A: easier per-path budget | B: harder path | T-G4-01 + T-G4-03 | UNDECIDED |
| Channel population / address steps | 16 addr steps x 4 ch = 64 slots, 50 valid; 14 masked | 50 sequential measurements | structural; report scan model (corrected ~64 us / ~32 us) | EVIDENCE-BACKED (model, corrected) | A: parallel coverage of 4 ch/step | B: single channel per step | none (model) | UNDECIDED |
| Wiring / fixture complexity | 4 sense traces + 4 ADC pins | shared node + per-MUX enable (or 2nd stage) | structural | EVIDENCE-BACKED (structural) | B: fewer ADC pins | A: 4 traces; B: more enable GPIO | none | B favored (wiring) |
| MCU resource impact | uses 4 of 10 ADC pins (Map A) | uses 1 of 10 ADC pins; more GPIO (4 addr + 4 en + optional 2nd-stage) | DS5319; audit (SR 3-4 GPIO corrected) | EVIDENCE-BACKED | B: ADC budget preserved | B: GPIO pressure; A: ADC pressure | none | UNDECIDED |
| Failure / blast radius | per-MUX common-node fault contained | shared-node fault affects all channels | audit Section 7 | EVIDENCE-BACKED (structural) | A: containment | B: single point | T-G4-06 | A favored |

## End state

A RECOMMENDED: NO (structurally favored on leakage/isolation/ADC-budget, but RON@3.3 V and settling not yet measured)
B RECOMMENDED: NO (structurally favored on wiring/ADC-pin count, but shared-node leakage/isolation risk)
**UNDECIDED** — final choice requires: T-G4-01 (RON@3.3 V), T-G4-04 (settling), T-G4-05 (leakage at 3.3/5 V), T-G4-06 (isolation), plus owner topology decision. [STATUS: UNDECIDED]