EESchema Schematic File Version 4
LIBS:power
LIBS:device
LIBS:74xx
LIBS:MCU_ST_STM32F1
EELAYER 29 0
EELAYER END
$Descr A4 11693 8268
Sheet 1 7
Title "RX50 50-Channel Controller — DRAFT / NOT FOR PRODUCTION"
Comment1 "Evidence-first draft; unresolved safety-critical values are explicitly TBD/HOLD"
Comment2 "RX24 baseline is not automatically valid for RX50"
Comment3 "Simultaneous multi-channel firing requirement; G1/G2 remain open"
Comment4 "Do not manufacture from this file"
$EndDescr
Text Notes 700 700 0 120 ~ 24
RX50 — SHEET 1/7 MCU / CONTROL (DRAFT)
Text Notes 700 1000 0 70 ~ 14
ARCHITECTURE ONLY: final pin assignment requires G5 closure.
Text Notes 700 1250 0 60 ~ 12
MCU candidate: STM32F103C8T6 / LQFP48. SWD, reset, clock and 3V3 domains reserved.
Text Notes 700 1500 0 60 ~ 12
Interfaces reserved: LoRa SPI, RS485 USART, 74HC595 control, CD4067 address/enable, safety interlock.
Text Notes 700 1750 0 60 ~ 12
UNRESOLVED: exact GPIO mapping, oscillator values, decoupling values, safety ownership.
Text Notes 700 2200 0 100 ~ 20
SHEET PARTITION
Text Notes 900 2500 0 70 ~ 14
1 MCU / CONTROL
Text Notes 900 2800 0 70 ~ 14
2 RF / RS485
Text Notes 900 3100 0 70 ~ 14
3 50-CHANNEL OUTPUT EXPANSION
Text Notes 900 3400 0 70 ~ 14
4 CONTINUITY / 4x 16:1 MUX CANDIDATE
Text Notes 900 3700 0 70 ~ 14
5 SAFETY / INTERLOCK
Text Notes 900 4000 0 70 ~ 14
6 POWER / PROTECTION
Text Notes 900 4300 0 70 ~ 14
7 CONNECTORS / CHANNEL GROUPING
Text Notes 700 4900 0 80 ~ 16
GLOBAL DESIGN GATES
Text Notes 900 5200 0 60 ~ 12
G1 simultaneous-load envelope: HOLD
Text Notes 900 5450 0 60 ~ 12
G2 firing-power feasibility: HOLD
Text Notes 900 5700 0 60 ~ 12
G3/G4/G5/G6/G8: candidate architectures, closure required before RELEASE
Text Notes 900 5950 0 60 ~ 12
This draft intentionally contains no invented firing current, pulse width, energy, voltage, timing, divider or protection ratings.
Text Notes 700 6700 0 100 ~ 20
STATUS: DRAFT — NOT RELEASED / NOT VALIDATED / NOT FOR MANUFACTURING
$EndSCHEMATC
