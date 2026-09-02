EESchema Schematic File Version 4
LIBS:power
LIBS:device
LIBS:74xx
LIBS:4xxx
LIBS:Connector_Generic
EELAYER 29 0
EELAYER END
$Descr A3 16535 11693
Sheet 1 8
Title "RX50 50-Channel Controller — 7-SHEET ROOT"
Comment1 "PRE-RELEASE / STRUCTURAL SCHEMATIC"
Comment2 "G1/G2 unresolved; firing-power implementation intentionally omitted"
Comment3 "Hierarchical sheet map for electrical review"
Comment4 "NOT FOR MANUFACTURING / NOT VALIDATED"
$EndDescr
Text Notes 700 700 0 120 ~ 24
RX50 — 7-SHEET ELECTRICAL SCHEMATIC ROOT
Text Notes 700 1000 0 65 ~ 13
Architecture only. Each sheet is independently reviewable; unresolved load/firing parameters remain TBD/HOLD.
$Sheet
S 900 1700 3600 1500
U 10000001
F0 "S01_MCU_CONTROL" 60
F1 "RX50_S01_MCU_CONTROL.sch" 60
$EndSheet
$Sheet
S 5000 1700 3600 1500
U 10000002
F0 "S02_RADIO_RS485" 60
F1 "RX50_S02_RADIO_RS485.sch" 60
$EndSheet
$Sheet
S 9100 1700 3600 1500
U 10000003
F0 "S03_OUTPUT_LOGIC" 60
F1 "RX50_S03_OUTPUT_LOGIC.sch" 60
$EndSheet
$Sheet
S 900 4000 3600 1500
U 10000004
F0 "S04_CONTINUITY" 60
F1 "RX50_S04_CONTINUITY.sch" 60
$EndSheet
$Sheet
S 5000 4000 3600 1500
U 10000005
F0 "S05_SAFETY_INTERLOCK" 60
F1 "RX50_S05_SAFETY_INTERLOCK.sch" 60
$EndSheet
$Sheet
S 9100 4000 3600 1500
U 10000006
F0 "S06_LOGIC_POWER" 60
F1 "RX50_S06_LOGIC_POWER.sch" 60
$EndSheet
$Sheet
S 5000 6300 3600 1500
U 10000007
F0 "S07_CONNECTORS" 60
F1 "RX50_S07_CONNECTORS.sch" 60
$EndSheet
Text Notes 900 5900 0 60 ~ 12
Cross-sheet contract: SR_* | OE_SAFE | MUX_A..D | MUX_EN | ADC_SENSE0..3 | ARM_REQ | FAULT_IN | INTERLOCK_OK | RS485_* | LORA_*.
Text Notes 900 6100 0 60 ~ 12
Output power/firing envelope is deliberately abstracted; no firing voltage/current/energy/pulse values are encoded.
Text Notes 900 8500 0 70 ~ 14
STATUS: STRUCTURAL SCHEMATIC — G1/G2 HOLD — NOT RELEASED
$EndSCHEMATC
