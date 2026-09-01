# RX50 G4 DATASHEET FACT REGISTER

Status: COMPLETE (Part B of batch G4-MEAS-BATCH-01)
Date: 2026-08-15
Sources: TI CD4067B SCHS052D Rev D; ST STM32F103x8/xB DS5319 Rev 19 (text verified) / Rev 20 (cited in prior reports); ST RM0008 (reference manual, cited).
Rule: numbers are taken from verified datasheet text/web excerpts from this session; anything unverifiable is marked NEEDS RECHECK. No value is filled from memory.

GUARANTEE TYPE legend: GUARANTEED (datasheet min/max spec) / TYPICAL / DESIGN-SPEC (specified by design, not tested in production) / CHARACTERIZATION (evaluated by characterization, not tested in production) / GRAPH-ONLY (curve, no tabulated guarantee) / NOT-SPECIFIED.

---

## B1. TI CD4067B (SCHS052D Rev D)

| PARAMETER | VALUE | UNIT | TABLE/SECTION | CONDITION | GUARANTEE TYPE | DESIGN CONSEQUENCE | CONFIDENCE |
|---|---|---|---|---|---|---|---|
| RON (max) | 1050 | ohm | Electrical char. (switches) | VDD-VSS = 5 V, 25 C | GUARANTEED (max) | 5 V path source impedance input; feeds Rth+RON+rtrace < 10 k | HIGH (verified) |
| RON (max) | 400 | ohm | same | VDD-VSS = 10 V, 25 C | GUARANTEED (max) | reference only (10 V not a candidate supply) | HIGH |
| RON (max) | 240 | ohm | same | VDD-VSS = 15 V, 25 C | GUARANTEED (max) | reference only | HIGH |
| RON (max) | 1200 | ohm | same (temp columns) | VDD-VSS = 5 V, 85 C | GUARANTEED (max) | 5 V path at elevated temp | HIGH (verified) |
| RON (max) | 1300 | ohm | same (temp columns) | VDD-VSS = 5 V, 125 C | GUARANTEED (max) | 5 V path at high temp | HIGH (verified) |
| RON @ 3.3 V | NOT SPECIFIED | - | entire datasheet | VDD-VSS = 3.3 V | NOT-SPECIFIED | RON@3.3 V MUST be measured (T-G4-01); interpolation forbidden | HIGH (verified) |
| VIH | 3.5 | V | Electrical char. | VDD = 5 V | GUARANTEED (min) | 5 V-control VIH conflict vs 3.3 V logic (VOH 2.9 V < 3.5 V) | HIGH (verified) |
| VIL | 1.0 | V | Electrical char. | VDD = 5 V | GUARANTEED (max) | reference for 5 V-control low level | HIGH (verified) |
| VIH/VIL @ 3.3 V | NOT SPECIFIED | - | datasheet | VDD = 3.3 V | NOT-SPECIFIED | VIH/VIL@3.3 V MUST be measured (T-G4-02) | HIGH (verified) |
| OFF leakage (max) | +-100 | nA | Electrical char. | VDD-VSS = 18 V, 25 C | GUARANTEED (max, 18 V condition) | upper bound input; NOT a 3.3/5 V guarantee | HIGH (verified) |
| OFF leakage (max) | +-1000 | nA | same | VDD-VSS = 18 V, 85/125 C | GUARANTEED (max, 18 V condition) | theoretical bounds 15 uA / 63 uA built on this (18 V test condition) | HIGH (verified) |
| OFF leakage (typ) | +-10 | pA | same | 10 V | TYPICAL | typical path negligible; not guaranteed | HIGH (verified) |
| OFF leakage note (2) | test-floor | - | footnote | "minimum feasible leakage measurement for automatic testing" | NOTE | 18 V max is a soft, test-floor bound at lower supply; real 3.3/5 V behavior = measurement | HIGH (verified) |
| Supply range (rec. op.) | 3 .. 18 | V | Recommended operating | VDD - VSS | GUARANTEED (operating range) | 3.3 V supply is WITHIN operating range (permission ok; value of RON open) | HIGH (verified) |
| CIS (input cap) | 5 | pF | Electrical char. | typ | TYPICAL | part of node capacitance estimate | HIGH (verified) |
| COS (output cap) | 55 | pF | Electrical char. | typ | TYPICAL | part of node capacitance estimate | HIGH (verified) |
| Bandwidth | 14 | MHz | Electrical char. | typ | TYPICAL | not a settling guarantee | HIGH (verified) |
| Settling time | not specified | - | datasheet | - | GRAPH-ONLY | settling MUST be measured (T-G4-04); tpd is NOT settling | HIGH (verified) |
| Charge injection | not a specified parameter | - | datasheet | - | NOT-SPECIFIED | typical note ~65 mV coupling from INH/address; not guaranteed | HIGH (verified) |
| Absolute max (switch/input current, VDD limits) | see datasheet | - | Absolute max ratings | - | GUARANTEED (bound) | bounds ITEST selection (T-G4-01) and fault-injection current (T-G4-06) | NEEDS RECHECK (exact rows during PDF check) |

## B2. ST STM32F103x8/xB (DS5319 Rev 19/20)

| PARAMETER | VALUE | UNIT | TABLE/SECTION | CONDITION | GUARANTEE TYPE | DESIGN CONSEQUENCE | CONFIDENCE |
|---|---|---|---|---|---|---|---|
| RADC | 1 | kohm | Table 47 (ADC char.) | - | DESIGN-SPEC | ADC sample switch resistance | HIGH (verified) |
| CADC | 8 | pF | Table 47 | - | DESIGN-SPEC | node settling / sample charge | HIGH (verified) |
| tS (sampling time) | 1.5 .. 239.5 | cycles (0.107..17.1 us @14 MHz) | Table 47 | fADC = 14 MHz | DESIGN-SPEC | configurable sampling window | HIGH (verified) |
| tCONV (total conversion) | 14 .. 252 | cycles (1..18 us) | Table 47 | = tS + 12.5 cycles, fADC=14 MHz | DESIGN-SPEC | tCONV INCLUDES tS; no double-counting | HIGH (verified) |
| RAIN max (Table 48) | 0.4 / 5.9 / 11.4 / 25.2 / 37.2 / 50 | kohm | Table 48 | tS = 1.5 / 7.5 / 13.5 / 28.5 / 41.5 / 55.5 cycles, fADC=14 MHz | CHARACTERIZATION | sampling-feasibility bound ONLY; not accuracy | HIGH (verified) |
| RAIN max (Table 48) | NA | - | Table 48 | tS = 71.5 / 239.5 cycles | CHARACTERIZATION (NA) | no value above 55.5 cycles; classify by measured value | HIGH (verified) |
| Accuracy +-2 LSB max ET | guaranteed only RAIN < 10 | kohm | ADC accuracy note (Tables 47/49) | - | GUARANTEED | continuity accuracy requires Rth+RON+rtrace < 10 k; verify at multiple points (A-02) | HIGH (verified) |
| fADC | 0.6 .. 14 | MHz | Table 47 | - | GUARANTEED | fix at 14 MHz for the accuracy/RAIN tests | HIGH (verified) |
| fS (sampling rate) | 0.05 .. 1 | MHz | Table 47 | - | GUARANTEED | implicit (tS/tCONV) | HIGH (verified) |
| VREF+ | internally tied to VDDA | - | Table 47 note 3 | LQFP48 / VFQFPN packages | GUARANTEED (design) | ADC full scale = VDDA; EXPECTED_CODE uses measured VDDA | HIGH (verified) |
| VREF+ range | 2.4 .. VDDA | V | Table 47 | - | GUARANTEED | VDDA must be stable & recorded | HIGH (verified) |
| VOH (CMOS) | VDD - 0.4 | V | GPIO DC char. (CMOS ports) | min | GUARANTEED (min) | 2.9 V @3.3 V; vs CD4067 VIH@5V=3.5 V -> 5 V path needs level shift | HIGH (verified) |
| VOL (CMOS) | ~0.4 | V | GPIO DC char. (CMOS ports) | max (drive condition) | GUARANTEED (max) | reference for control low-level margin | NEEDS RECHECK (exact I/O current row during PDF check) |
| GPIO count | 37 | I/O | ordering info / pin def | LQFP48 | GUARANTEED | resource closure unchanged (SR 3-4 GPIO; OE interlock-owned) | HIGH (verified) |
| ADC channels (external) | 10 (PA0-PA7, PB0, PB1) | - | pin definitions | - | GUARANTEED | continuity + monitor budget | HIGH (verified) |
| ADC count | 2 (ADC1, ADC2) | - | block diagram | - | GUARANTEED | no 4-way parallel conversion (E-01 correction holds) | HIGH (verified) |
| USART1 max baud | 4.5 | Mbit/s | USART char. | 16x oversampling, fPCLK2 | GUARANTEED | RS485 link is USART-limited; 10 Mbps not reachable | HIGH (verified) |
| USART1 with 8x oversampling | up to 9 | Mbit/s | RM0008 (reference manual) | 8x oversampling | DESIGN-SPEC (RM) | still < 10 Mbps; not needed for G4 | NEEDS RECHECK (RM page) |
| Absolute max (ADC pin / VDD) | per datasheet | - | Absolute max ratings | - | GUARANTEED (bound) | bounds T-G4-06 fault-injection current limit | NEEDS RECHECK (rows during PDF check) |

## B3. Register conclusions

- Every G4 test block has a datasheet-anchored parameter and a guarantee type. [STATUS]
- The two NEEDS RECHECK rows (CD4067 absolute max current; STM32 VOL exact drive condition; USART 8x value) are procedural references, not design inputs for G4. [STATUS]
- No value is claimed for CD4067 RON@3.3 V or VIH@3.3 V — they remain MEASUREMENT PENDING. [STATUS]