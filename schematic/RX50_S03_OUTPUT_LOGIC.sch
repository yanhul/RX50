EESchema Schematic File Version 4
EELAYER 29 0
EELAYER END
$Descr A3 16535 11693
Sheet 4 8
Title "RX50 S03 — 50-Channel Output Logic"
Comment1 "7 x 74HC595 logical storage for 50 channels"
Comment2 "Output power stage intentionally abstracted"
Comment3 "OE owned by hardware interlock"
Comment4 "NOT FOR MANUFACTURING"
$EndDescr
Text Notes 700 700 0 110 ~ 22
S03 — 50-CHANNEL OUTPUT LOGIC
Text Notes 700 1000 0 60 ~ 12
7 x 74HC595 = 56 storage bits; CH00..CH49 are logical channels; spare storage bits remain disabled by policy.
Text Notes 700 1350 0 60 ~ 12
CONTROL: SR_SER, SR_SRCLK, SR_RCLK, SRCLR. OE is hardware-interlock-owned.
Text Notes 700 1700 0 60 ~ 12
POWER/IGNITION STAGE: represented only as an abstract boundary. No firing voltage/current/energy/pulse value is encoded.
Text Notes 700 2050 0 60 ~ 12
Power-up storage state must not create an enabled output; hardware blanking remains mandatory.
Text Notes 700 2450 0 65 ~ 13
GATE: G3/G6 PROVISIONAL. Driver qualification is external to this sheet.
$EndSCHEMATC
