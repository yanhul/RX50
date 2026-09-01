# RX50 G4 RAW DATA TEMPLATES

Status: COMPLETE (Part E of batch G4-MEAS-BATCH-01)
Date: 2026-08-15
Rule: templates are empty measurement logs. NO values are inserted. Blank rows await execution.

Common fields: TEST_ID, DUT_ID, TRIAL, VDD, TEMP, CHANNEL, CONDITION, INPUT, OUTPUT, VALUE, UNIT, INSTRUMENT, INSTRUMENT_ID, CAL_STATUS, OPERATOR, DATE, TIME, REMARK.

---

## E1. T-G4-01 — RON (4-wire)

TEST_ID,DUT_ID,TRIAL,VDD,TEMP,CHANNEL,ITEST,VS_W,VALUE,UNIT,INSTRUMENT,INSTRUMENT_ID,CAL_STATUS,OPERATOR,DATE,TIME,REMARK
T-G4-01,DUT-001,1,3.3,25,0,,,,ohm,,,,,,,,,
T-G4-01,DUT-001,1,3.3,25,1,,,,ohm,,,,,,,,,
T-G4-01,DUT-001,1,3.3,25,2,,,,ohm,,,,,,,,,
T-G4-01,DUT-001,1,3.3,25,3,,,,ohm,,,,,,,,,
T-G4-01,DUT-001,1,3.3,25,4,,,,ohm,,,,,,,,,
T-G4-01,DUT-001,1,3.3,25,5,,,,ohm,,,,,,,,,
T-G4-01,DUT-001,1,3.3,25,6,,,,ohm,,,,,,,,,
T-G4-01,DUT-001,1,3.3,25,7,,,,ohm,,,,,,,,,
T-G4-01,DUT-001,1,3.3,25,8,,,,ohm,,,,,,,,,
T-G4-01,DUT-001,1,3.3,25,9,,,,ohm,,,,,,,,,
T-G4-01,DUT-001,1,3.3,25,10,,,,ohm,,,,,,,,,
T-G4-01,DUT-001,1,3.3,25,11,,,,ohm,,,,,,,,,
T-G4-01,DUT-001,1,3.3,25,12,,,,ohm,,,,,,,,,
T-G4-01,DUT-001,1,3.3,25,13,,,,ohm,,,,,,,,,
T-G4-01,DUT-001,1,3.3,25,14,,,,ohm,,,,,,,,,
T-G4-01,DUT-001,1,3.3,25,15,,,,ohm,,,,,,,,,
(duplicate block for VDD=5.0; additional TRIAL blocks and TEMP points as approved)

## E2. T-G4-02 — VIH/VIL @3.3 V

TEST_ID,DUT_ID,TRIAL,VDD,TEMP,CHANNEL,CONTROL_INPUT,INPUT_V,OUTPUT_STATE,OUTPUT_V,REFERENCE,HYSTERESIS,UNIT,INSTRUMENT,INSTRUMENT_ID,CAL_STATUS,OPERATOR,DATE,TIME,REMARK
T-G4-02,DUT-001,1,3.3,25,0,A,,,,,,,V,,,,,,,,
T-G4-02,DUT-001,1,3.3,25,0,B,,,,,,,V,,,,,,,,
T-G4-02,DUT-001,1,3.3,25,0,C,,,,,,,V,,,,,,,,
T-G4-02,DUT-001,1,3.3,25,0,D,,,,,,,V,,,,,,,,
T-G4-02,DUT-001,1,3.3,25,0,INH,,,,,,,V,,,,,,,,
(repeat blocks for each control input sweep; OUTPUT_STATE = ON/OFF at each INPUT_V)

## E3. T-G4-03 — ADC error vs RAIN

TEST_ID,DUT_ID,TRIAL,VDD,TEMP,RAIN_MEASURED,RAIN_UNIT,APPLIED_V,VDDA,SAMPLE_TIME_CYC,ADC_CLOCK_MHZ,EXPECTED_CODE,MEASURED_CODE,ERROR_LSB,REGION,INSTRUMENT,INSTRUMENT_ID,CAL_STATUS,OPERATOR,DATE,TIME,REMARK
T-G4-03,F2-BOARD,1,3.3,25,,,,14,55.5,14,,,,,A,,,,,,,,
T-G4-03,F2-BOARD,1,3.3,25,,,,14,55.5,14,,,,,B,,,,,,,,
T-G4-03,F2-BOARD,1,3.3,25,,,,14,55.5,14,,,,,C,,,,,,,,
(multi-point blocks across input range; >=5 trials per point; RAIN_MEASURED = recorded measured resistor value, not nominal)

## E4. T-G4-04 — Settling (waveform referenced)

TEST_ID,DUT_ID,TRIAL,VDD,TEMP,OLD_CHANNEL,NEW_CHANNEL,TRANSITION_TYPE,INITIAL_V,FINAL_V,PEAK_V,SETTLING_TIME,UNIT,PROBE_C_IN,PROBE_TYPE,SCOPE_SETTINGS,WAVEFORM_FILE,OPERATOR,DATE,TIME,REMARK
T-G4-04,DUT-001,1,3.3,25,0,1,address,,,0,,us,,,10x,,,,,,
T-G4-04,DUT-001,1,3.3,25,1,0,address,,,0,,us,,,10x,,,,,,
T-G4-04,DUT-001,1,3.3,25,0,8,channel,,,0,,us,,,10x,,,,,,
T-G4-04,DUT-001,1,3.3,25,0,1,INH,,,0,,us,,,10x,,,,,,
(>=5 captures per transition type; WAVEFORM_FILE mandatory; PROBE_C_IN recorded)
Waveform file naming (owner-approved D-01, M003E): <TEST_ID>_<DUT_ID>_N<channel_or_node>_TR<seq>.<ext> (e.g., T-G4-04_DUT-001_N12_TR01.CSV); WAVEFORM_FILE = exact filename; original filenames preserved on handoff

## E5. T-G4-05 — OFF-channel leakage

TEST_ID,DUT_ID,TRIAL,VDD,TEMP,CHANNEL,N_OFF,NODE_V,REF_V,DELTA_V,Z_EFFECTIVE,I_EFFECTIVE,UNIT,MEAS_FLOOR,INSTRUMENT,INSTRUMENT_ID,CAL_STATUS,OPERATOR,DATE,TIME,REMARK
T-G4-05,DUT-001,1,3.3,25,0,0,,,,,,V,,,DMM,,,,,,,
T-G4-05,DUT-001,1,3.3,25,0,1,,,,,,V,,,DMM,,,,,,,
T-G4-05,DUT-001,1,3.3,25,0,5,,,,,,V,,,DMM,,,,,,,
T-G4-05,DUT-001,1,3.3,25,0,15,,,,,,V,,,DMM,,,,,,,
(Option B block: N_OFF up to 63 if shared-node fixture built; I_EFFECTIVE = NOT ESTABLISHED if Z_EFFECTIVE not known; MEAS_FLOOR recorded)

## E6. T-G4-06 — Cross-channel isolation

TEST_ID,DUT_ID,TRIAL,VDD,TEMP,SOURCE_CH,VICTIM_CH,POPULATION,FAULT_TYPE,CURRENT_LIMIT,EXPECTED_STATE,MEASURED_STATE,DELTA,UNIT,INSTRUMENT,INSTRUMENT_ID,CAL_STATUS,OPERATOR,DATE,TIME,REMARK
T-G4-06,DUT-001,1,3.3,25,0,1,same-MUX,short,,ON,,,mV,,DMM,,,,,,,
T-G4-06,DUT-001,1,3.3,25,0,2,cross-MUX,short,,ON,,,mV,,DMM,,,,,,,
T-G4-06,DUT-001,1,3.3,25,0,0,shared-node,force,,ON,,,mV,,DMM,,,,,,,
(>=3 trials per (source,victim) pair; CURRENT_LIMIT mandatory for all fault injection)