# RX50 Connector / Net Closure — STRICT AUTO

Status: `OPEN — NO PHYSICAL CONNECTOR LOCK`

This artifact closes only what can be established from the current architecture documents. It intentionally does not invent a physical connector pinout.

## Required logical interfaces

| Interface | Logical signals | Closure |
|---|---|---|
| SWD | SWDIO, SWCLK, reset boundary | Reserved; physical pinout OPEN |
| LoRa | SPI2 + NSS/RST/DIO0 | Logical interface present; physical connector OPEN |
| RS485 | TX/RX/DE + bus boundary | Logical interface present; connector/polarity OPEN |
| Continuity | ADC_SENSE[0..3] + MUX_A[0..3] + MUX_EN | Logical interface present; channel connector OPEN |
| Output | OUTPUT[0..49] | Logical interface only; firing-stage connector OPEN |

## Strict closure rules

- A logical net is not a physical connector pin.
- No connector numbering is invented.
- No board-to-harness pinout is locked without an authoritative connector specification.
- `OUTPUT[0..49]` remains architecture-only and does not define a firing circuit.

## Current decision

`NOT READY TO LOCK`.

The correct next artifact is a connector specification/evidence input. Until that exists, the controller must treat connector closure as OPEN rather than fabricate a pinout.
