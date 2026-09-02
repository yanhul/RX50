# RX50 Multi-Sheet Schematic Index

Status: PRE-RELEASE / NOT VALIDATED / NOT FOR MANUFACTURING

This index decomposes the functional schematic into electrical review sheets. It does not close G1/G2 or authorize a firing-power implementation.

| Sheet | Scope | Gate | Release state |
|---|---|---|---|
| 1 | MCU / control / debug | G5 | PROVISIONAL |
| 2 | LoRa + RS485 | G5/G8 | PROVISIONAL |
| 3 | 50-channel output logic / 74HC595 | G3/G6 | PROVISIONAL; output power stage omitted |
| 4 | Continuity / CD4067 + ADC | G4/G5 | OPEN |
| 5 | Hardware safety interlock / OE ownership | G6 | OPEN |
| 6 | Logic power / protection boundary | G1/G2 | HOLD; no firing-power values |
| 7 | Channel/connectors / external interfaces | G1/G2/G5 | HOLD/TBD |

## Cross-sheet net contract

- `SR_SER`, `SR_SRCLK`, `SR_RCLK`, `SRCLR`: output-register control domain.
- `OE_SAFE`: hardware interlock-owned output blanking control. MCU is not sole authority.
- `MUX_A..D`, `MUX_EN`: continuity multiplexer control domain.
- `ADC_SENSE0..3`: independent continuity sense nodes; final divider/source impedance remains TBD until G4 evidence exists.
- `ARM_REQ`, `FAULT_IN`, `INTERLOCK_OK`: safety/control interface.
- `RS485_A`, `RS485_B`: external half-duplex communications.
- `LORA_*`: radio interface.

## G1/G2 boundary

The firing/load envelope, pulse requirements, simultaneous definition/skew, firing-rail architecture, transient/protection requirements, thermal/duty-cycle requirements, fault-isolation requirements, and authorization chain remain owner-input/evidence gates. No numerical value is inserted here.

## Review rule

A sheet may be structurally reviewed while G1/G2 are HOLD, but the overall design cannot be marked RELEASED or VALIDATED until the governing evidence and approval gates are closed.
