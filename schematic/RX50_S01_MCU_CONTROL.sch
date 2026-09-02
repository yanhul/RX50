EESchema Schematic File Version 4
EELAYER 29 0
EELAYER END
$Descr A3 16535 11693
Sheet 2 8
Title "RX50 S01 — MCU / CONTROL / DEBUG"
Comment1 "STM32F103C8T6 control boundary"
Comment2 "PROVISIONAL / G5 NOT LOCKED"
Comment3 "No firing-power parameters"
Comment4 "NOT FOR MANUFACTURING"
$EndDescr
Text Notes 700 700 0 110 ~ 22
S01 — MCU / CONTROL / DEBUG
Text Notes 700 1000 0 60 ~ 12
MCU: STM32F103C8T6. Control domains are separated from the hardware safety authority.
Text Notes 700 1400 0 60 ~ 12
CONTROL NETS: SR_SER, SR_SRCLK, SR_RCLK, SRCLR, MUX_A, MUX_B, MUX_C, MUX_D, MUX_EN.
Text Notes 700 1700 0 60 ~ 12
INTERFACE NETS: ARM_REQ, FAULT_IN, INTERLOCK_OK, OE_SAFE, RS485_TX/RX/DE, LORA_SPI/RESET/DIO.
Text Notes 700 2000 0 60 ~ 12
DEBUG: SWD. Firmware must not be sole authority for output enable.
Text Notes 700 2400 0 65 ~ 13
G5: GPIO mapping remains PROPOSED until evidence/approval closes the register.
Text Notes 700 2800 0 65 ~ 13
GATE: G5 PROVISIONAL. No numerical firing parameters are encoded.
$EndSCHEMATC
