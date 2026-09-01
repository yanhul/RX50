# T-G4-06 — STM32 ADC/Input Pin Current Limit Test Gate

**Template type:** Test gate — verification specification
**Status:** PROTOCOL DEFINITION (not a measurement result)
**Author:** M006.3
**Date:** 2026-08-15
**References:** C-22, EV-47, OI-15, C-20b

---

## 1. PURPOSE

T-G4-06 is intended to verify that STM32F103 ADC input pins and other non-5V-tolerant digital input pins in the RX50 circuit are not subjected to current injection exceeding the manufacturer's absolute maximum rating under any expected operating condition, including fault conditions (e.g., a 5 V-referenced sense node forward-biasing the internal ESD protection diode on a 3.3 V-supplied pin).

This test gate exists because the continuity/sense path routes external signals to the STM32 ADC through a CD4067 analog multiplexer, and a 5 V-referenced sense node has been identified (C-20b) that could exceed both the VIN voltage limit and the injection current limit if connected without attenuation or clamping.

---

## 2. GOVERNING EVIDENCE

T-G4-06 is governed by **EV-47**, which is referenced in C-22 as the source of the IINJ current injection limit.

| Item | Status |
|---|---|
| EV-47 | **ABSENT** from this repository. Content unknown. |
| C-22 | Records that "Governing T-G4-06 current limit (IINJ ±5 mA, EV-47) unaffected." |

### Historical value

The value **IINJ = ±5 mA** is mentioned in C-22 as the governing limit for T-G4-06. This is a:

**HISTORICAL CONCLUSION — UNDERLYING EVIDENCE ABSENT**

The ±5 mA value originates from a prior analysis context (M003C) and is not independently verifiable from any evidence stored in this repository. EV-47 — the evidence item that would contain the authoritative specification — does not exist as a file in `evidence/`.

---

## 3. TEST SCOPE

### 3.1 DUT / input pin under test

The test shall apply to each STM32F103 pin in the RX50 circuit that:
- Is a non-5V-tolerant (non-FT) input or I/O pin (see OI-15 for verification of which pins are non-FT)
- Is connected to the CD4067 common I/O node (the sense node)
- May be exposed to current injection from an external voltage source that exceeds VDD or goes below VSS

**Known pins in scope (from historical context):**
- ADC input pins connected to the CD4067 common I/O via the sense node
- Any additional non-FT GPIO pin that is part of the continuity measurement path

**Note:** The exact pin list is TBD until the RX50 schematic is available and OI-15 (VIN pin-down) is closed.

### 3.2 Injection direction(s)

Two injection directions shall be considered:

| Direction | Condition | Hazard |
|---|---|---|
| **Positive injection** | External voltage > VDD (e.g., 5 V sense node on 3.3 V supply) | Current flows into the pin through the upper ESD protection diode to VDD |
| **Negative injection** | External voltage < VSS (e.g., negative transient on sense node) | Current flows out of the pin through the lower ESD protection diode to VSS |

The test gate shall verify that the RX50 circuit **prevents** both injection directions from exceeding the manufacturer's absolute maximum current rating.

### 3.3 Measurement points

| Point | Description |
|---|---|
| Pin voltage (V_PIN) | Voltage at the STM32 input pin, measured relative to VSS |
| Pin current (I_PIN) | Current flowing into the pin (positive = into pin, negative = out of pin) |
| VDD pin of STM32 | Supply voltage — injection current may flow into VDD through ESD diode; monitor for VDD rise |
| Series resistance | Voltage drop across any series resistance between the external node and the STM32 pin |

### 3.4 Required instrumentation

| Capability | Specification | Purpose |
|---|---|---|
| DC voltage source | 0–6 V, ±0.5% accuracy | Simulate external voltage on sense node (e.g., 5 V, 3.3 V, intermediate) |
| DC current measurement | Resolution ≤1 µA, range ±10 mA | Measure pin injection current |
| DC voltage measurement | Resolution ≤1 mV, accuracy ±0.1% | Measure pin voltage and series resistance drop |
| Series resistor (known value) | If a protection resistor is present in the RX50 circuit, measure its actual value | Calculate expected current from applied voltage |
| Current-limiting protection | Resistor or PTC in series with test source | Prevent damage to DUT if injection limit is exceeded during characterization |

### 3.5 Test conditions

**Supply voltage:** The STM32 shall be powered at its normal operating voltage (3.3 V). Both powered and unpowered (VDD = 0 V) conditions shall be tested, because injection during unpowered operation may cause different failure modes.

**External voltage:** Apply external voltage to the pin under test through a known series resistance (the actual RX50 circuit's series resistance, or a representative value if the circuit is unavailable). Sweep the external voltage from 0 V up to the maximum voltage present in the RX50 system (5 V, per C-20b, or higher if another rail exists).

**Series resistance:** Measure or specify the total series resistance between the external voltage source and the STM32 pin. The actual RX50 continuity circuit series resistance is **unknown** (schematic not present). If testing without the actual circuit, use a range of series resistance values to characterize the injection current for different protection scenarios.

**Ambient temperature:** Record ambient temperature. Do not control temperature for this test.

### 3.6 Data to record

| Field | Description |
|---|---|
| Test ID | T-G4-06-NNN |
| Pin under test | STM32 pin name/number |
| VDD (V) | STM32 supply voltage |
| V_ext (V) | Applied external voltage |
| R_series (Ω) | Series resistance between V_ext and STM32 pin |
| V_pin (V) | Measured voltage at STM32 pin |
| I_inj (µA) | Measured injection current into pin (+ = into pin) |
| VDD measured (V) | Measured VDD rail voltage during injection |
| Temperature (°C) | Ambient temperature |
| Notes | Anomalies, ESD event, latch-up indication, measurement uncertainty |

### 3.7 Repeatability

If injection current > 1 µA is observed, repeat the measurement three times at the same condition. If the measured current varies by more than ±10%, investigate contact resistance, oxide contamination, or intermittent ESD events.

---

## 4. PASS/FAIL

**No verified pass/fail threshold is defined in this test gate specification.**

The repository contains:

- A **HISTORICAL CONCLUSION** that IINJ = ±5 mA (per C-22, EV-47), but:
  - EV-47 is **absent** from this repository
  - The STM32F103 datasheet (DS5319) that would confirm this value is **absent** from this repository
  - The ±5 mA value has been labelled a historical conclusion and is not independently verifiable

**Until the governing evidence is obtained, this test gate cannot establish a verified pass/fail criterion.**

---

## 5. SAFETY

**WARNING:** This test involves applying external voltages to STM32 input pins. Injection current exceeding the manufacturer's absolute maximum rating may cause:

- Latch-up (destructive — may require power cycle or may permanently damage the device)
- ESD structure damage
- Metal migration in the input protection structure
- Reliability degradation

**The test must not intentionally exceed a manufacturer-confirmed absolute maximum current rating unless an appropriately controlled qualification procedure exists.**

This test gate does **not** define such a qualification procedure. If the test setup does not include current-limiting protection (e.g., a series resistor sized to limit current to ≤1 mA even under fault conditions), do not apply external voltages directly to STM32 pins.

**Recommended protection:** Always include a series resistor between the external voltage source and the STM32 pin. Calculate the resistor value such that even under worst-case voltage (5 V), the current is limited to ≤1 mA until the actual absolute maximum rating is confirmed from the datasheet.

---

## 6. EVIDENCE STATUS

### Verified repository facts (Level 1–2)

| Fact | Source |
|---|---|
| T-G4-06 is referenced as the test gate for STM32 input current limit | CONTRADICTION_REGISTER.md, C-22 |
| EV-47 governs the current limit for T-G4-06 | CONTRADICTION_REGISTER.md, C-22 |
| EV-47 does not exist in this repository | Directory check — `evidence/` is empty |
| OI-15 (VIN pin-down) is open and must be resolved before the definitive pin list for this test can be established | OI-15_STM32_VIN_PIN_DOWN.md |
| A 5 V-referenced sense node exists that could inject current into the STM32 ADC pin | CONTRADICTION_REGISTER.md, C-20b |

### Historical conclusions (Level 8 — not verified, underlying evidence absent)

| Conclusion | Source | Missing evidence |
|---|---|---|
| IINJ = ±5 mA | C-22 (from EV-47, via M003C) | EV-47 absent; DS5319 absent |
| STM32 non-FT VIN max = 4.0 V | C-22 (from DS5319 Rev 18/19/20, via M003C) | DS5319 absent |

### Missing evidence

| Evidence | Required for | Status |
|---|---|---|
| EV-47 | Confirms the IINJ absolute maximum current rating | **ABSENT** |
| DS5319 (STM32F103 datasheet) | Confirms IINJ in Absolute Maximum Ratings table; confirms pin VIN limits | **ABSENT** |
| RX50 schematic | Identifies which STM32 pins are on the sense node; identifies existing series resistance and protection circuitry | **ABSENT** |

### TBD owner requirements

| Requirement | Status |
|---|---|
| Maximum acceptable injection current for RX50 design | UNKNOWN — no owner requirement exists |
| Protection circuit design (series resistor, clamp, or isolator) | UNKNOWN — C-20b lists options but no decision made |
| Allowable injection current during unpowered operation | UNKNOWN — no requirement exists |

---

## 7. CLOSURE CONDITIONS

T-G4-06 may be closed **only** when ALL of the following are true:

1. **EV-47** has been obtained and is stored in `evidence/`.
2. **DS5319** (STM32F103 datasheet, current revision) has been obtained and is stored in `evidence/`.
3. The Absolute Maximum Ratings table in DS5319 has been read, and the IINJ limit has been confirmed (or corrected) from the authoritative source.
4. The RX50 continuity circuit schematic is available, and the series resistance between every external node and every STM32 input pin has been calculated.
5. For each STM32 input pin in the continuity path, the expected worst-case injection current under all operating conditions (powered and unpowered) has been calculated and shown to be below the verified IINJ limit.
6. If any condition produces injection current exceeding the verified limit, a mitigation has been implemented (series resistor, clamp, level-shift, or isolation) and verified by measurement.
7. **OI-15** is closed (VIN pin-down verified).
8. A test report documents pass/fail for each pin under each condition.

---

## 8. LIMITATIONS

The following cannot be concluded from this test gate specification alone:

1. **The ±5 mA value is not verified** — until EV-47 and DS5319 are obtained, do not treat ±5 mA as a confirmed limit.
2. **The pin list is incomplete** — without the RX50 schematic and OI-15 closure, the exact set of pins requiring current-limit verification is unknown.
3. **The external voltage is assumed to be 5 V** (from C-20b), but if the RX50 circuit contains any higher-voltage node (e.g., 12 V or 24 V firing supply), additional injection paths may exist that are not covered by this specification.
4. **This specification does not test ESD event injection** (sub-microsecond transients). It addresses DC and steady-state injection only.
5. **This specification does not define a qualification procedure for exceeding the absolute maximum rating.** Intentional over-stress testing requires a separate, controlled qualification plan.

---

## REFERENCES

| Reference | Type | Relationship to T-G4-06 | Status in repository |
|---|---|---|---|
| CONTRADICTION_REGISTER.md (C-22) | Contradiction register | Origin — references EV-47 as governing T-G4-06 | Exists |
| CONTRADICTION_REGISTER.md (C-20b) | Contradiction register | Identifies 5 V→ADC sense exposure — the injection path that T-G4-06 must address | Exists |
| EV-47 | Evidence item | Governing evidence for IINJ limit | **ABSENT** |
| EV-48 | Evidence item | Governing evidence for ADC pin VIN limit | **ABSENT** |
| DS5319 | Manufacturer datasheet | STM32F103 datasheet containing IINJ and VIN limits | **ABSENT** |
| OI-15 | Open issue | VIN pin-down — prerequisite for definitive pin list | Exists (harness/open_issues/OI-15_STM32_VIN_PIN_DOWN.md) |
| T-G4-05 | Test gate template | Related leakage characterization test gate | Exists (harness/templates/T-G4-05_LEAKAGE_CHARACTERIZATION.md) |
| SCHS052D | Manufacturer datasheet | CD4067 datasheet (the mux in the injection path) | **ABSENT** |