EESchema Schematic File Version 4
EELAYER 29 0
EELAYER END
$Descr A3 16535 11693
Sheet 5 8
Title "RX50 S04 — Continuity / ADC"
Comment1 "4 x CD4067 candidate topology"
Comment2 "G4 OPEN"
Comment3 "No production divider/threshold values"
Comment4 "NOT FOR MANUFACTURING"
$EndDescr
Text Notes 700 700 0 110 ~ 22
S04 — CONTINUITY / ADC
Text Notes 700 1000 0 60 ~ 12
Candidate topology: four 16:1 CD4067 groups, common address/control, four independent sense outputs to ADC.
Text Notes 700 1350 0 60 ~ 12
CONTROL: MUX_A, MUX_B, MUX_C, MUX_D, MUX_EN. SENSE: ADC_SENSE0..ADC_SENSE3.
Text Notes 700 1700 0 60 ~ 12
G4 OPEN: CD4067 RON at the intended logic condition is not yet closed by authoritative evidence/measurement.
Text Notes 700 2050 0 60 ~ 12
Divider/source impedance, ADC thresholds, settling, leakage and continuity classification remain TBD until evidence closes G4.
Text Notes 700 2450 0 65 ~ 13
GATE: G4 OPEN. This sheet is architectural, not a validated measurement circuit.
$EndSCHEMATC
