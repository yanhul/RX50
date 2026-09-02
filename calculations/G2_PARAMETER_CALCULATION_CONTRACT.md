# RX50 G2 Calculation Contract

This file defines how engineering calculations must be performed once approved source parameters exist. It intentionally contains no ignition operating values.

## Required record

Every calculation must record:

1. `calculation_id`
2. `purpose`
3. `input_parameter_ids`
4. source/evidence references for every input
5. formula/model
6. units
7. assumptions
8. computed result
9. uncertainty/sensitivity where applicable
10. reviewer
11. approval state
12. timestamp / commit

## Prohibited shortcuts

- No numerical value copied from an unrelated e-match.
- No RX24 numerical value inherited merely because the architecture is related.
- No distributor/marketplace value promoted to manufacturer evidence.
- No typical/nominal internet value used as a design requirement.
- No calculated result treated as a measured or manufacturer-certified value.

## Verification gates

`INPUTS_COMPLETE -> SOURCE_TRACEABLE -> FORMULA_REVIEWED -> CALCULATION_REPRODUCIBLE -> ENGINEERING_REVIEW`

If any gate fails: `HOLD`.

## Safety boundary

This contract does not prescribe ignition voltage, current, energy, pulse duration, waveform, or driver sizing. Those inputs remain controlled engineering data and must enter the registry through the evidence/approval process.
