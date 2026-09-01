# RX50 Interface Consistency Audit — STRICT AUTO

Status: `PASS WITH OPEN ITEMS`

This is a documentation-level consistency audit. It does not authorize a build-ready firing circuit, establish physical measurements, or freeze safety-critical parameters.

| Interface | Current state | Result | Required before lock |
|---|---|---|---|
| STM32 ↔ SX1278 SPI2 | Provisional | CONSISTENT | Final GPIO/pin-map evidence |
| STM32 ↔ MAX3485 | Provisional | CONSISTENT | Final DE/RE and connector mapping |
| STM32 ↔ 74HC595 chain | Provisional | CONSISTENT | Final GPIO allocation and OE safety boundary |
| STM32 ↔ CD4067 banks | Provisional | CONSISTENT | Electrical suitability evidence at intended VCC |
| CD4067 → ADC | 4-bank architecture | CONSISTENT | Settling/source-impedance validation |
| 50 channels → MUX banks | 4 × 16:1 | CONSISTENT | Final channel-to-MUX mapping |
| 50 channels → 74HC595 | 7 × 8-bit | CONSISTENT | Final output mapping; 6 spare bits documented |
| SWD | Reserved | CONSISTENT | Preserve reservation in final pin map |

## Strict rules

1. `PROVISIONAL` is not `LOCKED`.
2. Datasheet-derived calculations may support design claims but are not physical measurements.
3. A value unavailable from a datasheet at the intended operating condition must remain `NOT PROVEN`; no interpolation is permitted unless the manufacturer explicitly provides the relationship.
4. Firing-stage electrical values remain outside this architecture document.
5. Safety/owner authorization remains an independent gate.

## Auto decision

No new interface contradiction was found in the current provisional net register. Continue to the next concrete closure item rather than manufacturing a PASS for an unresolved electrical property.
