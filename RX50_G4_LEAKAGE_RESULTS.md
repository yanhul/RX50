# RX50 G4 LEAKAGE RESULTS (T-G4-05)

Status: NO DATA INGESTED
Date: 2026-08-15
Batch: G4-EVIDENCE-CLOSURE-01

## Raw data

- Rows ingested (E5): 0. N_OFF sweep, node voltages, reference voltages, Z_effective: NOT RECEIVED. [MEASUREMENT PENDING]

## Results

| POPULATION | N_OFF | DELTA_V | I_EFFECTIVE | REGIME |
|---|---|---|---|---|
| Option A (per-MUX node) | 0..15 | NOT AVAILABLE | NOT ESTABLISHED | NOT AVAILABLE |
| Option B (shared node) | 0..63 | NOT AVAILABLE | NOT ESTABLISHED | NOT AVAILABLE |

## Discipline statements

- I_EFFECTIVE = NOT ESTABLISHED for all cells (no Z_effective data; no delta data). [CONSTRAINT]
- Datasheet OFF-leakage bounds (15 uA / 63 uA at the 18 V test condition) are THEORETICAL REFERENCES, NOT measured 3.3/5-V predictions; no measured comparison exists. [CONSTRAINT]
- No linear-with-supply scaling is assumed. [CONSTRAINT]
- Regime classification (typ vs max) cannot begin until data is above the measurement floor (floor not yet logged). [STATUS]