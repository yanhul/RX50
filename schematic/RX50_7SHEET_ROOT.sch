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
Comment3 "Hierarchical sheet interface contract"
Comment4 "NOT FOR MANUFACTURING / NOT VALIDATED"
$EndDescr
Text Notes 700 700 0 120 ~ 24
RX50 — 7-SHEET ELECTRICAL SCHEMATIC ROOT
Text Notes 700 1000 0 65 ~ 13
Architecture only. Sheet interfaces are explicit; unresolved load/firing parameters remain TBD/HOLD.
$Sheet
S 900 1700 3600 1500
U 10000001
F0 "S01_MCU_CONTROL" 60
F1 "RX50_S01_MCU_CONTROL.sch" 60
F2 "SR_*" O R 4500 1800 50
F3 "MUX_A..D" O R 4500 2000 50
F4 "MUX_EN" O R 4500 2200 50
F5 "ADC_SENSE0..3" I R 4500 2400 50
F6 "RS485_*" B R 4500 2600 50
F7 "LORA_*" B R 4500 2800 50
$EndSheet
$Sheet
S 5000 1700 3600 1500
U 10000002
F0 "S02_RADIO_RS485" 60
F1 "RX50_S02_RADIO_RS485.sch" 60
F2 "LORA_*" B L 5000 2000 50
F3 "RS485_*" B L 5000 2300 50
$EndSheet
$Sheet
S 9100 1700 3600 1500
U 10000003
F0 "S03_OUTPUT_LOGIC" 60
F1 "RX50_S03_OUTPUT_LOGIC.sch" 60
F2 "SR_*" I L 9100 2000 50
F3 "OE_SAFE" I L 9100 2300 50
F4 "CH00..CH49" O R 12700 2600 50
$EndSheet
$Sheet
S 900 4000 3600 1500
U 10000004
F0 "S04_CONTINUITY" 60
F1 "RX50_S04_CONTINUITY.sch" 60
F2 "MUX_A..D" I L 900 4300 50
F3 "MUX_EN" I L 900 4500 50
F4 "ADC_SENSE0..3" O R 4500 4700 50
$EndSheet
$Sheet
S 5000 4000 3600 1500
U 10000005
F0 "S05_SAFETY_INTERLOCK" 60
F1 "RX50_S05_SAFETY_INTERLOCK.sch" 60
F2 "ARM_REQ" I L 5000 4400 50
F3 "FAULT_IN" I L 5000 4600 50
F4 "INTERLOCK_OK" O R 8600 4800 50
F5 "OE_SAFE" O R 8600 5000 50
$EndSheet
$Sheet
S 9100 4000 3600 1500
U 10000006
F0 "S06_LOGIC_POWER" 60
F1 "RX50_S06_LOGIC_POWER.sch" 60
F2 "LOGIC_POWER" O R 12700 4500 50
F3 "GND_LOGIC" O R 12700 4700 50
$EndSheet
$Sheet
S 5000 6300 3600 1500
U 10000007
F0 "S07_CONNECTORS" 60
F1 "RX50_S07_CONNECTORS.sch" 60
F2 "CH00..CH49" B L 5000 6800 50
F3 "ARM_REQ" O L 5000 7000 50
F4 "FAULT_IN" O L 5000 7200 50
F5 "RS485_A/B" B L 5000 7400 50
$EndSheet
Text Notes 900 5900 0 60 ~ 12
Root interface contract: MCU owns logic requests; safety sheet owns OE_SAFE; continuity owns ADC sense; output logic exposes 50 logical channels.
Text Notes 900 6100 0 60 ~ 12
Output power/firing envelope is deliberately abstracted; no firing voltage/current/energy/pulse values are encoded.
Text Notes 900 8500 0 70 ~ 14
STATUS: STRUCTURAL / FUNCTIONAL SCHEMATIC — G1/G2 HOLD — NOT RELEASED
Text Notes 900 8700 0 55 ~ 11
Hierarchical pins define the cross-sheet contract; child-sheet labels must match before ERC/electrical release.
$EndSCHEMATC
