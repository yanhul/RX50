# RX50 G1/G4 SELF-PROGRESS PACK

Status: ENGINEERING-PROGRESS / NON-AUTHORITATIVE
Purpose: maximize closure without inventing owner requirements or physical measurements.

## 1. G1 — replace "waiting" with an executable qualification packet

The repository already has candidate-product traceability but no authoritative electrical envelope.
Therefore G1 is split:

- G1-ID: candidate/product identity = VERIFIED.
- G1-ELEC: exact current/pulse/voltage/load envelope = OPEN.
- G1-CONC: simultaneous/worst-case channel requirement = OPEN.
- G1-SKEW: physical simultaneity/skew budget = OPEN.

No production number is created.

### Qualification sweep to execute when hardware/load is available

For N = 1, 2, 4, 8, 16, 25, 50:
- record actual firing-rail voltage before/during/after event;
- record per-channel load current and voltage waveform;
- record pulse width and energy;
- record channel-to-channel skew;
- record source/return voltage drop;
- record thermal state and recovery interval.

Each row must carry DUT, trial, N, channel set, Vrail, temperature, instrument, calibration status, timestamp and raw-file reference.

The sweep is a test matrix, NOT a requirement.

## 2. G4 — close everything that is already analytically closeable

### G4-A ADC source impedance
The repository's registered evidence states that the <10 kohm condition is the guaranteed accuracy region and 50 kohm is only a sampling-feasibility bound.
Disposition: ANALYTICALLY VERIFIED; do not represent this as a physical RX50 measurement.

### G4-B 5 V logic interface
The source-derived VOH/VIH comparison establishes a conditional incompatibility when the MCU operating point and source conditions make VOH(min) below CD4067 VIH.
Disposition: CONDITIONAL CONFLICT VERIFIED; project VDD still must be locked before calling it an RX50-specific failure.

### G4-C 3.3 V CD4067 RON
No guaranteed 3.3 V RON value exists in the current evidence.
Disposition: MEASUREMENT REQUIRED.

### G4-D settling
Typical curves are not a guaranteed RX50 settling specification.
Disposition: MEASUREMENT REQUIRED.

### G4-E leakage
No RX50 operating-point physical leakage result exists.
Disposition: MEASUREMENT REQUIRED.

### G4-F ADC accuracy
`RX50_G4_ADC_RESULTS.md` records zero ingested rows.
Disposition: MEASUREMENT REQUIRED.

## 3. Dry-fire work that can proceed NOW

Before any hot-fire requirement exists, the control chain can be verified without a firing load:

T-F-01: BOOT -> SAFE -> ARM_REQUEST -> ARMED -> FIRE_AUTHORIZED -> FIRE_EXECUTION -> POST_FIRE.
T-F-02: verify 7x HC595 RCLK common-edge alignment.
T-F-03: fault injection must force OE/output-disable.
T-F-04: reset/power-up must leave outputs disabled.
T-F-05: duplicate/stale command must not create a second FIRE_EXECUTION.
T-F-06: RF-loss/fault path must enter FAULT sink.

These tests prove control/interlock behavior only. They do not prove firing power, load compatibility, simultaneity at the load, or G4 analog performance.

## 4. Promotion boundary

G1 remains HOLD until authoritative owner/product electrical envelope + simultaneous requirement exist.
G4 remains MEASUREMENT_PENDING until raw physical measurements exist.
AIOS engineering conformance remains BLOCKED.

This packet is deliberately useful without weakening any gate.
