EESchema Schematic File Version 4
EELAYER 29 0
EELAYER END
$Descr A3 16535 11693
Sheet 6 7
Title "RX50 S05 — Hardware Safety Interlock"
Comment1 "OE ownership / inhibit boundary"
Comment2 "G6 OPEN"
Comment3 "No firing-power parameters"
Comment4 "NOT FOR MANUFACTURING"
$EndDescr
Text Notes 700 700 0 110 ~ 22
S05 — HARDWARE SAFETY INTERLOCK
Text Notes 700 1000 0 60 ~ 12
Inputs: ARM_REQ, FAULT_IN. Status: INTERLOCK_OK. Output-control authority: OE_SAFE.
Text Notes 700 1350 0 60 ~ 12
OE_SAFE is hardware-owned. Firmware may request state changes but cannot be sole authority to enable outputs.
Text Notes 700 1700 0 60 ~ 12
Fault/open/inhibit conditions must force the output stage into the disabled state.
Text Notes 700 2050 0 60 ~ 12
Exact logic implementation remains subject to component evidence and review; no unsupported timing or electrical values are inserted.
Text Notes 700 2450 0 65 ~ 13
GATE: G6 OPEN.
$EndSCHEMATC
