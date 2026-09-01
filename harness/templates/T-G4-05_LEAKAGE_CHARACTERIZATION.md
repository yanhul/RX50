# T-G4-05 — CD4067 Leakage Characterization Protocol

**Template type:** Test gate — measurement protocol
**Status:** PROTOCOL DEFINITION (not a measurement result)
**Author:** M006.1
**Date:** 2026-08-15
**References:** C-20c, C-04, C-20b, G-05

---

## 1. OBJECTIVE

Characterize the off-channel leakage current of the CD4067 analog multiplexer(s) at the actual RX50 operating supply voltages, to determine whether leakage at those voltages differs from the datasheet specification at 18 V.

**Why this measurement is needed:**

- **C-20c** (UNRESOLVED): "Measured leakage regime at 3.3/5 V unknown (datasheet bounds at 18 V condition only)." The existing contradiction register records that no measured data exists.
- **C-04** (resolved for theoretical bound only): The theoretical worst-case leakage of 63 µA at 18 V was calculated from SCHS052D datasheet leakage. C-04 explicitly states: *"Measured leakage at 3.3/5 V remains UNRESOLVED — MEASUREMENT/EVIDENCE MISSING (T-G4-05)."*
- **C-20b** (open): 5 V path testing (required for the level-shift vs 3.3 V decision) is blocked until this characterization exists.
- The continuity/ADC measurement architecture depends on knowing the summed leakage of all OFF channels onto the shared sense node. Without actual leakage at the operating voltage, the continuity measurement floor cannot be validated.

---

## 2. TEST ARTICLE

### Required configuration

A CD4067 (SCHS052D series) installed in a circuit representative of the RX50 continuity measurement path.

### What is known (from historical context)

| Item | Source |
|---|---|
| Device under test is CD4067 (SCHS052D per Ti/formerly TI) | C-20b, C-04 (HISTORICAL CONCLUSION — UNDERLYING EVIDENCE ABSENT; SCHS052D datasheet not in repository) |
| Device operates from a supply rail that is either 3.3 V or 5 V | C-20b, C-20c |
| At least one CD4067 handles channel selection for continuity/ADC measurement | C-04 (63 OFF channels implies ≥63 channels, consistent with multiple CD4067 stages or a single 16:1 mux with additional stages) |

### What is unknown

- Actual RX50 circuit topology (schematic not present in repository)
- Whether a single CD4067 (16:1) or cascaded mux bank is used
- Whether the continuity circuit uses Option A or Option B topology (referenced in C-02, C-04 but not defined in repository)
- Pull-up/pull-down resistor values on the sense node
- Whether the sense node includes any series resistance or clamping (C-20b notes "no sense-node attenuation defined")
- Protection circuitry between CD4067 common I/O and STM32 ADC pin

**If the actual RX50 circuit is unavailable, use a CD4067 device on a test fixture that reproduces:**
- The same supply voltage (3.3 V or 5 V, tested separately)
- The same unselected-channel termination (all unselected channels connected to the voltage-under-test source, not floating)
- A load impedance on the common I/O representative of the ADC input impedance (RAIN + CADC path, approximately 50 kΩ + 8 pF — HISTORICAL CONCLUSION — UNDERLYING EVIDENCE ABSENT, per C-10, C-11)

---

## 3. OPERATING CONDITIONS

### Voltage points to test

Only those points already identified in the repository:

| Test point | Voltage | Rationale | Source |
|---|---|---|---|
| V1 | **3.3 V** | STM32 MCU supply voltage; primary CD4067 operating candidate | C-20b, C-20c |
| V2 | **5.0 V** | Secondary CD4067 operating candidate (if 5 V path is used) | C-20b, C-20c |

### Additional voltage points

The SCHS052D datasheet specifies leakage at **18 V** only (HISTORICAL CONCLUSION — UNDERLYING EVIDENCE ABSENT; not confirmed from datasheet in repository). If the datasheet becomes available and specifies curves or additional points (e.g., 10 V, 15 V), those may be added. Do not invent intermediate points.

A third optional test point, **18 V**, may be added strictly for cross-validation against the published SCHS052D specification, **but only if** the test setup can safely apply 18 V without damaging other components in the path. If the test fixture is not rated for 18 V, skip this point and note the limitation.

### Voltage accuracy

Supply voltage shall be within ±1% of the target. Record the actual measured supply voltage at the CD4067 supply pin.

### Additional conditions to record

- Ambient temperature (see Section 8)
- Supply rail ripple (if measurable)

---

## 4. MEASUREMENT NODES

Three distinct leakage contributions exist. The protocol shall measure:

### 4.1 Individual channel leakage (OFF channel to common I/O)

Each channel, when unselected (address lines hold a different channel number), conducts leakage current from the channel I/O pin to the common I/O pin. This is the per-channel leakage.

**What to measure:** Current from the unselected channel pin to the common I/O pin, with the unselected channel pin held at the supply voltage (or test voltage) and the common I/O pin at the same potential.

### 4.2 Common-node leakage (summed)

When multiple channels are OFF simultaneously, all individual leakages sum at the common I/O node. This is the aggregate current that the continuity measurement circuit must tolerate.

**What to measure:** Total current flowing into the common I/O pin from all unselected channels simultaneously, with all channel pins held at the supply voltage.

### 4.3 Leakage into the continuity/sense node

If the continuity circuit applies a known voltage or current to the common I/O node (e.g., a pull-up resistor to a reference), the OFF-channel leakage acts as an error current that shifts the sensed voltage.

**What to measure:** The voltage shift at the common I/O node caused by aggregate leakage, measured against a known reference resistance. This is derived from 4.2 if the sense-node impedance is known.

### 4.4 Supply leakage

Measure CD4067 supply current (ICC) in static (unswitched) condition at each operating voltage, to confirm the device is not damaged and quiescent current is within expected range. Record but do not treat as a pass/fail item.

---

## 5. CHANNEL COVERAGE

### Requirement

**Test every channel individually** for per-channel leakage (Section 4.1), because:
- Manufacturing variance may produce asymmetric leakage across channels.
- A single high-leakage channel could dominate the aggregate even if the mean is low.
- The CD4067 has 16 channels (one device); a full sweep is feasible.

### Aggregate measurement

After individual characterization, measure the **summed leakage** with all channels OFF simultaneously (Section 4.2). This directly tests the worst-case condition for the continuity measurement.

### Statistical sampling

Do not use statistical sampling as a substitute. Every channel in a single test article shall be tested. If multiple CD4067 devices are used in the RX50 circuit (cascaded mux stages), each device shall be characterized separately.

---

## 6. INSTRUMENTATION

The following measurement capabilities are required. Do not interpret as specific model numbers or brands.

| Required capability | Specification | Purpose |
|---|---|---|
| **DC voltage source** | 0–20 V, ±1% accuracy, at least 10 mA output | Supply voltage for CD4067 and channel bias |
| **DC current measurement** | Resolution ≤10 nA, accuracy ±2% of reading or ±1 nA (whichever is larger), range 1 nA – 10 µA | Per-channel leakage measurement (expected <1000 nA per channel at 18 V per historical datasheet spec; lower at 3.3/5 V) |
| **DC voltage measurement** | Resolution ≤100 µV, accuracy ±0.1% | Sense-node voltage measurement |
| **Multiplexer address control** | 4 digital outputs (or binary-coded address) to select each of 16 channels | Channel selection; can be driven by STM32 GPIO, manual switches, or a function generator |
| **Temperature measurement** | Resolution ≤1 °C, accuracy ±2 °C | Ambient temperature recording |
| **Shielded test fixture** | Low-leakage insulation (>10 GΩ between adjacent traces) | Prevent fixture leakage from masking device leakage |
| **Data recording** | Automatic logging or manual spreadsheet | Per Section 9 data format |

### Alternative low-current measurement methods

If a picoammeter or source-measure unit (SMU) with ≤10 nA resolution is unavailable:

- **Voltage-droop method:** Force a known voltage through a known high-value resistor (e.g., 1 MΩ ±0.1%) and measure the voltage drop across it. The leakage current is I = V/R. This requires the resistor leakage to be <1 nA (use a low-leakage precision resistor).
- **Capacitive droop:** Disconnect the sense node from any source, float it, and measure the voltage drift rate. This gives combined leakage plus input capacitance effects. Less precise for absolute leakage.

If using an alternative method, record the method and its estimated measurement uncertainty.

---

## 7. TEST PROCEDURE

### 7.1 Preparation

1. Visually inspect the CD4067 test article for damage, solder bridges, or contamination.
2. Clean the test fixture with isopropyl alcohol and allow to dry. Contamination leakage can exceed device leakage.
3. Connect the CD4067 to the test fixture:
   - VDD pin → supply voltage
   - VSS pin → ground (0 V)
   - Inhibit pin → ground (device enabled)
   - All 16 channel I/O pins → individual accessible terminals
   - Common I/O pin → measurement node
   - Address lines (A, B, C, D) → digital control
4. Verify continuity of all connections before power-on.

### 7.2 Initial state verification

1. Apply VDD = 3.3 V.
2. Set address lines to select channel 0 (binary 0000).
3. Measure ICC (supply current). Record. Compare to historical SCHS052D quiescent current spec if datasheet is available. If ICC > 100 µA at 3.3 V, flag the device as possibly damaged and do not proceed.
4. Confirm that all other channels (1–15) are unselected by verifying no other channel shows continuity to common I/O.

### 7.3 Per-channel leakage measurement (unselected)

For each channel 0 through 15:

1. Select a **different** channel from the one under test (e.g., when measuring channel 3 leakage, select channel 0, or when measuring channel N, select (N+1) mod 16).
2. Apply the channel test voltage (same as VDD for this test point) to the channel I/O pin under test.
3. Force the common I/O pin to the same voltage (VDD).
4. Wait 1 second for settling.
5. Measure the current flowing from the channel I/O pin to the common I/O pin.
   - Polarity: current flowing INTO the common I/O from the channel is positive.
6. Record the measured current.
7. Repeat for channel 0 voltage condition: test voltage = 0 V (channel I/O at ground), common I/O at VDD/2 (or relevant bias) to characterize leakage asymmetry if the continuity circuit biases the common node at an intermediate voltage.

### 7.4 Aggregate leakage measurement (all channels unselected)

1. Set address lines to select a **nonexistent** channel (>15) if the CD4067 wraps around, or assert Inhibit = high to disable all channels (per SCHS052D logic — verify from datasheet). If Inhibit behavior is unavailable from datasheet, set address to a valid channel and exclude that channel from the aggregate.
2. Apply VDD to **all** channel I/O pins simultaneously.
3. Force the common I/O pin to VDD.
4. Wait 2 seconds for settling.
5. Measure total current flowing into the common I/O pin.
6. Record.

### 7.5 Repeat for 5.0 V supply

Repeat Sections 7.2–7.4 with VDD = 5.0 V. Do not exceed STM32 ADC VIN limit of 4.0 V on the common I/O node if the test fixture connects to an ADC pin (HISTORICAL CONCLUSION — UNDERLYING EVIDENCE ABSENT, per C-22). If the test fixture includes the STM32 ADC, use a voltage divider or clamp to prevent VIN > 4.0 V, or disconnect the ADC pin and measure on an isolated common I/O node.

### 7.6 Repeatability check

1. After completing all 16 channels at one voltage, repeat the measurement on channel 0.
2. If the second measurement differs from the first by more than 20%, flag the setup for drift or contamination and investigate before continuing.
3. Record the repeatability delta.

### 7.7 Cross-check point (optional 18 V)

If the test fixture and instrumentation are rated for 18 V, and the datasheet has been obtained:
1. Repeat Sections 7.2–7.4 at VDD = 18 V.
2. Compare measured leakage per channel at 18 V against the SCHS052D datasheet specification of 1000 nA (HISTORICAL CONCLUSION — UNDERLYING EVIDENCE ABSENT). If the datasheet value differs from 1000 nA, compare against the actual datasheet value.
3. Use this cross-check to validate that the measurement setup produces results consistent with manufacturer data.

---

## 8. TEMPERATURE

### Requirements

| Parameter | Specification |
|---|---|
| Temperature control | **Not required** for initial characterization |
| Temperature recording | **Required** — ambient temperature must be measured and recorded with each measurement |
| Temperature range to report | Ambient laboratory temperature (typically 20–26 °C) |

### Rationale

The SCHS052D datasheet (HISTORICAL CONCLUSION — UNDERLYING EVIDENCE ABSENT) specifies leakage at 25 °C ambient. Without the datasheet, the temperature sensitivity coefficient is unknown. The initial characterization shall establish a baseline at the temperature of measurement. If the measured leakage at operating voltage is very high (>10% of the 18 V theoretical bound of 63 µA aggregate), a follow-up temperature sweep may be warranted. That decision is deferred until after initial measurement.

### Temperature to record
- Ambient air temperature near the DUT
- Case temperature of the CD4067 (if accessible)
- Instrument warm-up state (cold start or 30 min+ stabilized)

---

## 9. DATA FORMAT

Each measurement row shall be recorded in the following format. Multiple rows per test.

| Test ID | VDD (V) | Channel | Selected? | V_ch (V) | V_com (V) | I_leak (nA) | Temp (°C) | Method | Instrument/Range | Timestamp | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| T-G4-05-001 | 3.3 | 0 | NO | 3.3 | 3.3 | | 23.5 | Direct (SMU) | Keithley 2400 / 1µA range | 2026-08-15T10:00 | Baseline, channel 0, Vdd=3.3V |

### Column definitions

| Column | Description |
|---|---|
| Test ID | Sequential ID per measurement (T-G4-05-NNN) |
| VDD | CD4067 supply voltage (V) |
| Channel | Channel number under test (0–15, or ALL for aggregate) |
| Selected? | Whether the measured channel is the selected (ON) or unselected (OFF) channel. For aggregate, "ALL OFF" |
| V_ch | Voltage applied to channel I/O pin (V) |
| V_com | Voltage on common I/O pin (V) |
| I_leak | Measured leakage current (nA). Positive = into common I/O |
| Temp | Ambient temperature at time of measurement (°C) |
| Method | Measurement method (Direct, Voltage-drop, Capacitive-droop) |
| Instrument/Range | Instrument model (or type) and current range used |
| Timestamp | ISO 8601 date and time of measurement |
| Notes | Free text for anomalies, signs of drift, measurement uncertainty estimate |

### Summary table

After all individual measurements, produce a summary:

| VDD | Per-channel max leakage (nA) | Per-channel mean leakage (nA) | Aggregate all-OFF leakage (nA) | Temperature |
|---|---|---|---|---|
| 3.3 V | | | | |
| 5.0 V | | | | |
| 18 V (optional) | | | | |

---

## 10. PASS/FAIL

**No pass/fail leakage limit is defined in this protocol.**

The repository currently contains:
- **No owner-defined leakage requirement** at 3.3 V or 5 V operating conditions.
- **No specified maximum acceptable sense-node leakage** for the continuity measurement.
- A theoretical worst-case bound of 63 µA at 18 V (HISTORICAL CONCLUSION — UNDERLYING EVIDENCE ABSENT, derived from 63 channels × 1000 nA per C-04), which does not apply at 3.3 V or 5 V.
- An unresolved requirement gap documented in C-02: "no owner scan-time requirement exists."

**Until an owner leakage requirement is established**, the measured values shall be recorded and reported. Do not draw conclusions about acceptability from the measurement alone.

---

## 11. EVIDENCE TRACEABILITY

### Verified repository facts (Level 1–2)

| Fact | Source |
|---|---|
| T-G4-05 leakage measurement is required and unresolved | CONTRADICTION_REGISTER, C-20c, C-04 |
| No measured leakage data at 3.3/5 V exists in this repository | CONTRADICTION_REGISTER, C-20c, G-05 |
| No owner leakage requirement exists at operating voltages | CONTRADICTION_REGISTER, C-02 (scan-time requirement gap), C-04 (leakage gap) |

### Historical conclusions (Level 8 — not verified, underlying evidence absent)

| Conclusion | Source | What evidence is missing |
|---|---|---|
| CD4067 per-channel leakage at 18 V = 1000 nA | C-04 (from SCHS052D datasheet) | SCHS052D datasheet not in repository |
| CD4067 VIH at 5 V = 3.5 V | C-20b (from SCHS052D datasheet) | SCHS052D datasheet not in repository |
| 63 OFF channels maximum | C-04 (derived) | RX50 channel count not confirmed |
| 63 µA worst-case aggregate leakage at 18 V | C-04 (63 × 1000 nA) | Depends on both unverified historical values |
| RAIN = 50 kΩ, CADC = 8 pF | C-10, C-11 (from DS5319 Table 48) | DS5319 datasheet not in repository |

### Proposed test procedure (this document)

The measurement steps in Section 7 are a proposed protocol, not verified by execution. The protocol is subject to revision when:
- The actual RX50 continuity circuit schematic becomes available.
- The SCHS052D datasheet confirms or corrects the leakage characterization conditions.
- A test fixture is built and measurements are performed.

### Unknown requirements

| Requirement | Status |
|---|---|
| Maximum acceptable leakage at sense node | UNKNOWN — no owner requirement exists |
| Channel count for aggregate calculation | UNKNOWN — "63" is a historical conclusion not verified against RX50 design |
| Temperature range for leakage specification | UNKNOWN — no thermal requirement documented |
| Continuity threshold (resistance or voltage) | UNKNOWN — C-02 documentation gap |

---

## 12. LIMITATIONS

The following cannot be concluded from this protocol alone:

1. **Whether measured leakage is acceptable** — until an owner-defined leakage requirement exists at the relevant operating voltage, no pass/fail determination can be made.

2. **Whether the CD4067 is the correct mux choice** — the protocol characterizes one device; if the mux is replaced with a different part (e.g., a 3.3 V-compatible mux), new characterization is needed.

3. **Whether the continuity measurement is valid at the measured leakage** — depends on the specific continuity circuit topology (Option A vs Option B, per C-02, C-04), which is not defined in the repository.

4. **Whether leakage at 3.3 V/5 V is better or worse than at 18 V** — leakage in CMOS analog switches typically increases with temperature and may increase with lower supply voltage (due to weaker gate drive on OFF switches) or decrease (due to lower electric field). The direction cannot be predicted without the datasheet or measurement.

5. **Whether the test fixture introduces parasitic leakage** — fixture leakage must be characterized separately by measuring with no DUT installed. This protocol does not specify fixture qualification.

6. **Whether the measured leakage applies to all production units** — this protocol tests one or a small number of devices. Unit-to-unit variation is unknown without multiple samples.

7. **Whether the 5 V supply path is feasible** — C-20b (logic-level incompatibility) and C-20b (5 V→ADC sense exposure) must be resolved separately. This protocol measures leakage only; it does not address drive capability, level translation, or ADC overvoltage protection.

---

## REFERENCES

| Reference | Type | Status in repository |
|---|---|---|
| C-20c | Open contradiction | Exists in CONTRADICTION_REGISTER.md |
| C-04 | Resolved contradiction (partial) | Exists in CONTRADICTION_REGISTER.md |
| C-20b | Open contradiction | Exists in CONTRADICTION_REGISTER.md |
| G-05 | Evidence gap | Identified in previous analysis; no separate file |
| T-G4-05 | Test gate template | THIS DOCUMENT |
| SCHS052D | Manufacturer datasheet (CD4067) | ABSENT from repository |
| DS5319 | Manufacturer datasheet (STM32F103) | ABSENT from repository |