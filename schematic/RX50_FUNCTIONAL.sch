EESchema Schematic File Version 4
LIBS:power
LIBS:device
LIBS:74xx
LIBS:4xxx
LIBS:Connector_Generic
LIBS:MCU_ST_STM32F1
LIBS:RF_Module
LIBS:Interface_UART
EELAYER 29 0
EELAYER END
$Descr A3 16535 11693
Sheet 1 1
Title "RX50 50-Channel Controller — FUNCTIONAL SCHEMATIC"
Comment1 "Evidence-backed architecture; unresolved G1/G2 values remain HOLD/TBD"
Comment2 "NOT RELEASED / NOT VALIDATED / NOT FOR MANUFACTURING"
Comment3 "50 logical channels; simultaneous multi-channel firing preserved"
Comment4 "OE is hardware-interlock owned; firing stage intentionally not specified"
$EndDescr
Text Notes 700 700 0 120 ~ 24
RX50 FUNCTIONAL SCHEMATIC — ARCHITECTURE / PRE-RELEASE
Text Notes 700 950 0 65 ~ 13
This artifact is an electrical-functional schematic, not a manufacturing release. No unsourced firing voltage/current/pulse/energy/timing/protection values are included.
Text Notes 700 1100 0 55 ~ 11
firing voltage: TBD / HOLD. firing current: TBD / HOLD. No firing-stage value is released by this functional schematic.
$Comp
L MCU_ST_STM32F1:STM32F103C8Tx U1
U 1 1 1
P 3200 3300
F 0 "U1" H 2750 4850 50 0000 C CNN
F 1 "STM32F103C8T6" H 3200 1750 50 0000 C CNN
	1    3200 3300
	1 0 0 -1
$EndComp
Text Notes 2450 5350 0 55 ~ 11
PROPOSED G5 MAP (NOT LOCKED): SPI2 PB13/14/15 + NSS PB12; LoRa RST PB11/DIO0 PB10; USART1 PA9/PA10 + DE PA8; ADC PA0..PA3; MUX ADDR PB4..PB7; MUX EN PB8; SWD PA13/PA14.
$Comp
L RF_Module:RA-02 U2
U 1 1 2
P 7400 2400
F 0 "U2" H 7000 2950 50 0000 C CNN
F 1 "SX1278 / RA-02" H 7400 1850 50 0000 C CNN
	1    7400 2400
	1 0 0 -1
$EndComp
Text Label 6400 2100 2 50 ~ 0
SPI2_SCK
Text Label 6400 2200 2 50 ~ 0
SPI2_MISO
Text Label 6400 2300 2 50 ~ 0
SPI2_MOSI
Text Label 6400 2500 2 50 ~ 0
LORA_NSS
Text Label 6400 2600 2 50 ~ 0
LORA_RESET
Text Label 8400 2400 0 50 ~ 0
LORA_DIO0
$Comp
L Interface_UART:MAX3485 U3
U 1 1 3
P 7400 4100
F 0 "U3" H 7000 4650 50 0000 C CNN
F 1 "MAX3485" H 7400 3550 50 0000 C CNN
	1    7400 4100
	1 0 0 -1
$EndComp
Text Label 6400 3900 2 50 ~ 0
USART1_TX
Text Label 6400 4000 2 50 ~ 0
USART1_RX
Text Label 6400 4300 2 50 ~ 0
RS485_DE
Text Label 8400 4000 0 50 ~ 0
RS485_A
Text Label 8400 4200 0 50 ~ 0
RS485_B
Text Notes 6700 4850 0 50 ~ 10
Half-duplex RS485. Link speed is MCU-limited; no unsupported rate claim.
$Comp
L 74xx:74HC595 U4
U 1 1 4
P 10700 2600
F 0 "U4" H 10700 3380 50 0000 C CNN
F 1 "74HC595 #1" H 10700 3280 50 0000 C CNN
	1    10700 2600
	1 0 0 -1
$EndComp
$Comp
L 74xx:74HC595 U5
U 1 1 5
P 12600 2600
F 0 "U5" H 12600 3380 50 0000 C CNN
F 1 "74HC595 #7" H 12600 3280 50 0000 C CNN
	1    12600 2600
	1 0 0 -1
$EndComp
Text Label 9700 2300 2 50 ~ 0
SR_SER
Text Label 9700 2400 2 50 ~ 0
SR_SRCLK
Text Label 9700 2500 2 50 ~ 0
SR_RCLK
Text Label 9700 2700 2 50 ~ 0
SRCLR
Text Notes 9800 3750 0 55 ~ 11
7 x 74HC595 total = 56 storage bits; channels CH00..CH49 use 50 bits; spare bits CH50..CH55 must remain OFF. U4 and U5 are endpoint representatives; U6..U10 are the five intervening identical devices.
Text Notes 9800 3950 0 55 ~ 11
SER -> U4 -> U5 -> ... -> U10 cascade. RCLK common. OE is NOT MCU-owned; it is driven by the hardware interlock.
Text Label 11600 2300 0 50 ~ 0
SR_QH_CHAIN
Text Label 13600 2600 0 50 ~ 0
CH49
Text Notes 9700 4250 0 55 ~ 11
IMPORTANT: 74HC595 storage register power-up state is undefined; hardware OE blanking is mandatory until a valid frame is shifted/latch sequence is complete.
$Comp
L 4xxx:4067 U11
U 1 1 6
P 10700 6200
F 0 "U11" H 10700 7280 50 0000 C CNN
F 1 "CD4067B #1" H 10700 7180 50 0000 C CNN
	1    10700 6200
	1 0 0 -1
$EndComp
$Comp
L 4xxx:4067 U12
U 1 1 7
P 13300 6200
F 0 "U12" H 13300 7280 50 0000 C CNN
F 1 "CD4067B #4" H 13300 7180 50 0000 C CNN
	1    13300 6200
	1 0 0 -1
$EndComp
Text Notes 9200 7850 0 55 ~ 11
Continuity candidate: 4 x 16:1 CD4067, shared address A/B/C/D, four independent sense outputs to ADC0..3. U13/U14 omitted graphically as identical middle units.
Text Notes 9200 8050 0 55 ~ 11
G4 OPEN: CD4067 RON at 3.3 V is not specified; settling is not guaranteed. Do not assign divider values or production thresholds until measurement closes G4.
Text Label 9400 5500 2 50 ~ 0
MUX_A
Text Label 9400 5600 2 50 ~ 0
MUX_B
Text Label 9400 5700 2 50 ~ 0
MUX_C
Text Label 9400 5800 2 50 ~ 0
MUX_D
Text Label 9400 6000 2 50 ~ 0
MUX_EN
Text Label 11800 6200 0 50 ~ 0
ADC_SENSE0
Text Label 14400 6200 0 50 ~ 0
ADC_SENSE3
$Comp
L Connector_Generic:Conn_01x08 J1
U 1 1 8
P 3100 7100
F 0 "J1" H 3018 7617 50 0000 C CNN
F 1 "SWD / DEBUG" H 3018 7526 50 0000 C CNN
	1    3100 7100
	1 0 0 -1
$EndComp
Text Notes 2300 8050 0 55 ~ 11
SWD: PA13/PA14. Keep debug ownership separate from safety outputs.
$Comp
L Connector_Generic:Conn_01x10 J2
U 1 1 9
P 5500 7100
F 0 "J2" H 5418 7717 50 0000 C CNN
F 1 "LOGIC / POWER INTERFACE" H 5418 7626 50 0000 C CNN
	1    5500 7100
	1 0 0 -1
$EndComp
Text Notes 4550 8050 0 55 ~ 11
Power sheet boundary: input protection, 3V3 regulator and firing-power domain are intentionally not dimensioned here. G1/G2 HOLD.
$Comp
L Connector_Generic:Conn_01x08 J3
U 1 1 10
P 7900 7100
F 0 "J3" H 7818 7617 50 0000 C CNN
F 1 "SAFETY INTERLOCK" H 7818 7526 50 0000 C CNN
	1    7900 7100
	1 0 0 -1
$EndComp
Text Label 6900 6900 2 50 ~ 0
ARM_REQ
Text Label 6900 7000 2 50 ~ 0
FAULT_IN
Text Label 6900 7100 2 50 ~ 0
OE_SAFE
Text Label 6900 7200 2 50 ~ 0
INTERLOCK_OK
Text Notes 6500 8050 0 55 ~ 11
G6: hardware interlock owns OE blanking. Firmware may request state changes but cannot be sole authority to enable outputs.
Text Notes 700 9000 0 70 ~ 14
GATE STATUS: G1 HOLD | G2 HOLD | G3 FEASIBLE / NOT LOCKED | G4 OPEN (RON@3V3 + settling) | G5 PROPOSAL / NOT LOCKED | G6 OPEN RULES | G8 STRUCTURALLY FEASIBLE
Text Notes 700 9300 0 60 ~ 12
No manufacturing values are implied by this functional schematic. Any value not backed by repository evidence remains TBD/HOLD.
$EndSCHEMATC
