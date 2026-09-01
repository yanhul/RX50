# RX50 G4 ADC RESULTS (T-G4-03)

Status: NO DATA INGESTED
Date: 2026-08-15
Batch: G4-EVIDENCE-CLOSURE-01

## Raw data

- Rows ingested (E3): 0. Measured resistor values, applied voltages, ADC codes, ADC clock, sample time, VDDA: NOT RECEIVED. [MEASUREMENT PENDING]

## Results

| REGION | CONDITION | EXPECTED_CODE | MEASURED_CODE | ERROR_LSB |
|---|---|---|---|---|
| A | RAIN < 10 kohm | NOT AVAILABLE | NOT AVAILABLE | NOT AVAILABLE |
| B | 10 kohm <= RAIN <= 50 kohm | NOT AVAILABLE | NOT AVAILABLE | NOT AVAILABLE |
| C | RAIN > 50 kohm / outside characterized condition | NOT AVAILABLE | NOT AVAILABLE | NOT AVAILABLE |

## Discipline statements

- ADC configuration verification (fADC = 14 MHz, tS, VDDA) against the stated test condition: DEFERRED until data received. [STATUS]
- The 50-kohm value is a sampling-feasibility bound (DS5319 Table 48), NOT an accuracy guarantee; this is preserved and no accuracy claim exists. [CONSTRAINT]
- Region classification will use the RECORDED measured RAIN value, not nominal. [CONSTRAINT]