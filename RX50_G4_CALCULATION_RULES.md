# RX50 G4 CALCULATION RULES (CALCULATION ENGINE)

Status: COMPLETE (Part F of batch G4-MEAS-BATCH-01)
Date: 2026-08-15
Rule: no fabricated uncertainty. No extrapolation outside measured conditions. No conversion of characterization into a manufacturer guarantee.

---

## F1. T-G4-01 — RON processing

- RON_ch = V_SW / ITEST [per trial, 4-wire] [CALCULATION]
- MIN = min over trials(ch, VDD, temp); MAX = max; MEAN = arithmetic mean; MEDIAN = middle order statistic (optional, reported if useful). [CALCULATION]
- SPREAD = MAX - MIN (per channel) and channel-to-channel variation = MEAN over trials per channel vs overall. [CALCULATION]
- Output: per-channel table + min/max/mean/spread per (VDD, temp). Result is CHARACTERIZATION; NOT "production guaranteed" (single/multi DUT labeled). [CONSTRAINT]
- Uncertainty: not fabricated; record instrument spec + repeatability; else UNCERTAINTY = NOT ESTABLISHED. [CONSTRAINT]
- Design feed: measured worst-case RON (MAX over all measured) is used ONLY in RTH + RON + RTRACE < 10 kohm, where 10 kohm is the DS5319 +-2 LSB guarantee condition. No additional margin invented; margin (if desired) = OWNER DECISION. [FACT -> CALCULATION]

## F2. T-G4-02 — VIH/VIL processing

- VIH = lowest input voltage at which the switch state transitions OFF->ON (defined output condition); VIL = highest input voltage at which state returns (per recorded termination/reference). [CALCULATION from raw sweep]
- Hysteresis = VIH - VIL (if observable; datasheet gives no hysteresis spec). [CALCULATION]
- Margin_high = VOH_min(STM32) - VIH_measured = 2.9 V - VIH_measured (VOH_min = VDD-0.4 = 2.9 V @3.3 V). Margin_low = VIL_measured - VOL_max(STM32) (VOL from DS5319, exact drive row NEEDS RECHECK). [FACT -> CALCULATION]
- No required-margin value is invented; margin is reported. PASS/FAIL only if an owner requirement exists. [CONSTRAINT]

## F3. T-G4-03 — ADC error processing

- Full scale = VDDA (VREF+ internally tied to VDDA, LQFP48). [FACT]
- EXPECTED_CODE = round( APPLIED_V_MEASURED / VDDA_MEASURED x (2^12 - 1) ), using the INSTRUMENT-MEASURED applied voltage, not the nominal setting. [CALCULATION (A-09)]
- MEASURED_CODE = raw ADC code (12-bit). [RAW]
- ERROR_LSB = | MEASURED_CODE - EXPECTED_CODE |. [CALCULATION]
- Region classification by RECORDED measured RAIN value (not nominal): A = RAIN < 10 k (datasheet-guaranteed domain: expect <=2 LSB); B = 10 k <= RAIN <= 50 k (characterization); C = RAIN > 50 k or outside Table 48 domain (exploratory, document only). [FACT -> CALCULATION (A-10)]
- The test reports per-point error; it does NOT claim to extend the manufacturer guarantee. [CONSTRAINT]
- Report: per (RAIN point, voltage point) error LSB; trials stats (mean/max); ADC config (tS, fADC=14 MHz, VDDA). [CONSTRAINT]

## F4. T-G4-04 — Settling processing

- Settling time = time from transition to the waveform entering and staying within the owner-defined band (if band exists); otherwise recorded as raw waveform + measured "settle to <x of final" is NOT computed (no invented percentage). [CONSTRAINT]
- Characterization output: initial/final voltage, transient peak, waveform, per-capture settling time ONLY if a band is owned. [CONSTRAINT]
- Propagation delay (tpd) is NOT settling time. [CONSTRAINT]
- Scan-time compliance is NOT derived from settling unless an owner scan-time requirement exists. [CONSTRAINT]
- Probe loading recorded as fixture contribution; do not claim node settling excludes probe loading unless stated. [CONSTRAINT (A-04)]

## F5. T-G4-05 — Leakage processing

- DELTA_V = REF_V - NODE_V (recorded per N_OFF). [CALCULATION]
- I_EFFECTIVE = DELTA_V / Z_EFFECTIVE, computed ONLY if Z_EFFECTIVE is measured/known and recorded; otherwise I_EFFECTIVE = NOT ESTABLISHED. [CONSTRAINT]
- Regime classification: compare DELTA_V to measurement floor (recorded); values at/below floor = "below measurement floor" (NOT "typical ~pA"). [CONSTRAINT (A-05)]
- Theoretical bounds (reference only, NOT 3.3/5 V predictions): Option A node up to 15 OFF channels -> 15 uA; Option B shared node up to 63 OFF -> 63 uA, both at the datasheet 18 V test condition using the 1 uA/channel max. [FACT -> CALCULATION]
- No linear-with-supply claim unless measured. [CONSTRAINT]

## F6. T-G4-06 — Isolation processing

- DELTA per (source, victim) = MEASURED_STATE - EXPECTED_STATE (or voltage delta). [CALCULATION]
- Blast radius characterization by population: same-MUX, cross-MUX, shared-node. [CALCULATION]
- No isolation dB / voltage / percentage / resistance requirement is invented; if no owner criterion, output is blast radius only. [CONSTRAINT]

## F7. General rules

- All stats are simple statistics of recorded values; trial counts recorded. [CALCULATION]
- Uncertainty: record instrument specified accuracy, resolution, repeatability, fixture contribution (incl. probe C_in), environment; if not quantifiable -> UNCERTAINTY = NOT ESTABLISHED. Instrument resolution is NOT total uncertainty. [CONSTRAINT]
- Datasheet conflict -> DATASHEET CONFLICT RECORD (see protocol Section 18); measurement never "corrected". [CONSTRAINT]