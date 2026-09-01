# RX50 Evidence Requirements Matrix — STRICT AUTO

Status: `OPEN — EVIDENCE COLLECTION PLAN`

This matrix separates claims that can be established from authoritative documentation from claims that require physical measurement or owner authorization.

| Claim | Allowed evidence | Current state | Closure condition |
|---|---|---|---|
| MCU identity / baseline | Authoritative datasheet | FACT | Datasheet revision recorded |
| GPIO alternate functions | Authoritative MCU datasheet | PROVISIONAL | Pin assignment reviewed and locked |
| 74HC595 logic/timing | Manufacturer datasheet | PROVISIONAL | Intended VCC and timing requirements verified |
| CD4067 RON at intended VCC | Manufacturer data explicitly covering intended VCC | NOT PROVEN | Direct applicable specification or physical characterization |
| CD4067 leakage / crosstalk | Applicable manufacturer data + physical test where required | NOT PROVEN | Acceptance test evidence |
| ADC source/settling behavior | MCU ADC requirements + circuit calculation + measurement where required | NOT PROVEN | Calculated and/or measured acceptance evidence |
| Connector pinout | Authoritative connector/harness specification | OPEN | Approved pinout document |
| Safety interlock behavior | Owner/safety requirement + verification evidence | OPEN | Authorized requirement and test evidence |
| Firing-stage electrical parameters | Approved engineering requirements + controlled validation | OPEN | Separate safety/engineering gate |

## Strict evidence rules

- Datasheet values are not measurements.
- A datasheet value at another supply voltage must not be relabeled as a measurement at the intended voltage.
- No interpolation is accepted as `RON @ 3.3 V measured`.
- Missing evidence remains `NOT PROVEN` or `OPEN`.
- CI success does not close hardware evidence gates.

## Next action

Use this matrix to drive artifact requests and audits. Do not invent missing measurements or connector data.
