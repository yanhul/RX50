# RX50 Provisional Net Register

**Status:** `PROVISIONAL — ARCHITECTURE ONLY`

| Net / signal group | From | To | Status |
|---|---|---|---|
| MCU_SPI2_SCK/MISO/MOSI | STM32F103 | SX1278 | PROVISIONAL |
| LORA_NSS/RST/DIO0 | STM32F103 | SX1278 | PROVISIONAL |
| RS485_TX/RX/DE | STM32F103 | MAX3485 | PROVISIONAL |
| SR_SER/SRCLK/RCLK | STM32F103 | 74HC595 chain | PROVISIONAL |
| SR_OE | Hardware interlock | 74HC595 OE | OPEN — safety gate |
| SRCLR | Reset/control boundary | 74HC595 chain | PROVISIONAL |
| ADC_SENSE[0..3] | Continuity MUX bank | STM32 ADC | PROVISIONAL |
| MUX_A[0..3] | STM32 | CD4067 address inputs | PROVISIONAL |
| MUX_EN | STM32 / enable boundary | CD4067 bank | PROVISIONAL |
| CONTINUITY_CHANNELS[0..49] | Channel interface | MUX bank | ARCHITECTURE ONLY |
| OUTPUT[0..49] | 74HC595 / safety boundary | Output interface | OPEN — no firing-stage design |

## Rules

- No final GPIO lock is claimed by this register.
- No firing electrical values are specified.
- No connector pinout is specified.
- Any row marked OPEN must remain open until its evidence/owner gate is satisfied.
