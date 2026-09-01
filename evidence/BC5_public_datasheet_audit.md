# BC5 Public Datasheet Evidence Audit

Status: `AUDIT INPUT ONLY — NOT A PASS`

## Scope

This artifact records independently retrievable manufacturer documentation relevant to RX50 feasibility questions. It does **not** constitute owner authorization, safety authorization, measured evidence, or a frozen design.

## Sources

1. STMicroelectronics STM32F103 documentation identifies DS5319 as the medium-density performance-line datasheet for STM32F103 devices, and the manufacturer provides the STM32F103x8/xB datasheet. This establishes provenance for the MCU documentation only.
   - https://www.st.com/en/microcontrollers-microprocessors/stm32f103/documentation.html
   - https://www.st.com/resource/en/datasheet/stm32f103c8.pdf
2. Texas Instruments CD4067B product documentation identifies the device as a 16:1 analog multiplexer and links the CD40x7B datasheet Rev. D. TI's current product page lists single-supply options including 3.3 V and documents the device's specified characteristics. The datasheet itself must be used for any parameter-level acceptance decision.
   - https://www.ti.com/product/CD4067B
   - https://www.ti.com/lit/gpn/CD4097B

## Audit conclusion

Public manufacturer documentation is available and provenance is established for these two component families. However, this is **insufficient to mark BC5 PASS** because the current authoritative queue contains no BC5 evidence and explicitly has owner authorization, safety authorization, and frozen state unset. No measured firing-power evidence is inferred from datasheets.

## Required next evidence

- Exact BC5 acceptance criteria from the authoritative project record.
- Any required measured/validated evidence not supplied by public datasheets.
- Explicit owner authorization and safety authorization where required by the project gate.
- A frozen candidate only after the applicable gate is actually satisfied.
