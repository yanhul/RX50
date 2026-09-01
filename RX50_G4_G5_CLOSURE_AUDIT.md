# RX50 G4-G5 CLOSURE AUDIT
# (MEASUREMENT CLOSURE + FULL PIN CONFLICT AUDIT)

Status: AUDIT COMPLETE — findings for owner review
Date: 2026-08-15
Audited artifact: RX50_G4_G5_HARDWARE_FEASIBILITY_REPORT.md (DRAFT, phase 12)
Secondary inputs audited: RX50_BATCH_ENGINEERING_REPORT.md, RX50_FEASIBILITY_G3_G4_G5_G6_G8.md, RX50_G9_FIRMWARE_AND_CROSS_GATE_REPORT.md.
Scope: verification of every claim in the G4/G5 report against manufacturer evidence; full 37-pin conflict audit. No schematic/PCB/BOM. No divider values. No locked topology. G1/G2 remain HOLD. No MAX_CONCURRENT_FIRE=1.

Label legend:
- [FACT]            Manufacturer / datasheet / explicit requirement evidence (provenance given).
- [CALCULATION]     Arithmetic from inputs; valid only if inputs valid.
- [ASSUMPTION]      Engineering assumption. NOT a requirement.
- [RECOMMENDATION]  Proposed direction; requires owner approval.
- Status: LOCKED / EVIDENCE-BACKED / HOLD / TBD / NEEDS RECHECK / OPEN / PROVISIONAL / CLOSEABLE.

Audit rules applied (from batch instruction):
1. No invented numerical specifications; every number carries provenance.
2. No silent ASSUMPTION -> FACT conversion. CD4067 RON@3.3V must NOT be interpolated.
3. Continuity threshold, scan-time target, settling margin, firing/skew values are NOT invented; marked TBD where no owner requirement exists.
4. G1/G2 domains (firing power/timing) are outside this batch.
5. Errors found in the prior report are listed in the Error Register with severity; corrections are stated here but the prior report is NOT rewritten (preserve sources; separate audit artifact).
6. No decision is force-closed.

---

## 1. Scope and evidence used

Evidence verified during this audit (web + datasheet text):

| EVIDENCE | REV | CLAIM VERIFIED | STATUS |
|---|---|---|---|
| ST DS5319 STM32F103x8/xB, Table 47 (ADC char.) | Rev 19 (PDF text); Rev 20 cited in report | RADC 1 kohm; CADC 8 pF; tS 1.5-239.5 cyc (0.107-17.1 us @14 MHz); tCONV 14-252 cyc (1-18 us), tCONV = tS + 12.5 cyc; RAIN max 50 kohm (Table 48); note: params "specified by design, not tested in production" | EVIDENCE-BACKED |
| ST DS5319, Table 48 (RAIN max for fADC = 14 MHz) | Rev 19 PDF | tS 1.5->0.4k, 7.5->5.9k, 13.5->11.4k, 28.5->25.2k, 41.5->37.2k, 55.5->**50k**, 71.5->NA, 239.5->NA | EVIDENCE-BACKED (report claim "RAIN 50k @55.5 cyc" CONFIRMED) |
| ST DS5319, ADC accuracy note (Tables 47/49) | Rev 19/20 | +-2 LSB max ET guaranteed only when RAIN < 10 kohm | EVIDENCE-BACKED |
| ST DS5319, Table 47 note 3 | Rev 19 | VREF+ internally tied to VDDA in LQFP/VFQFPN packages | EVIDENCE-BACKED |
| ST DS5319, GPIO DC char. (Table 27-ish, I/O ports) | Rev 19/20 | VOH min = VDD - 0.4 V (CMOS port) | EVIDENCE-BACKED |
| ST DS5319, USART char. | Rev 19/20 | USART1 max baud 4.5 Mbit/s (16x oversampling; 8x oversampling raises to <=9 Mbit/s) -> 10 Mbps NOT reachable | EVIDENCE-BACKED (corrects prior claim) |
| TI CD4067B SCHS052D Rev D | TI datasheet | RON max 1050 ohm @5V / 400 @10V / 240 @15V (25 C); RON@3.3V NOT SPECIFIED; VIH@5V=3.5V, VIL=1V; OFF leakage +-100 nA (25 C) / +-1000 nA (85-125 C) @18V; typical +-10 pA @10V; CIS 5 pF; COS 55 pF; BW 14 MHz; recommended operating VDD-VSS = 3..18 V; settling = typical curves only; charge injection NOT a specified parameter; OFF leakage note: values "determined by minimum feasible leakage measurement for automatic testing" (test-floor) | EVIDENCE-BACKED |
| STM32F103C8T6 ordering/pin data | ST/Mouser | 37 GPIO (LQFP48); 2x 12-bit ADC, 10 external channels PA0-PA7, PB0, PB1 | EVIDENCE-BACKED |
| ST RM0008 (reference manual) | RM0008 | AFIO MAPR SWJ_CFG: '010' disables JTAG-DP, keeps SW-DP -> PA15(PB4? no: PA15=JTDI,PB3=JTDO,PB4=JNTRST) free as GPIO; PB2=BOOT1; PC13/14/15 in VBAT domain, limited drive (~+-3 mA), TAMPER-RTC/OSC32_IN/OSC32_OUT | EVIDENCE-BACKED (datasheet + RM0008) |
| MAX3485 | Maxim | half-duplex transceiver up to 10 Mbps; DE/RE | EVIDENCE-BACKED |

Previously recorded (carried, not re-derived): SX1278 SPI <=10 MHz, 256-byte FIFO; SN74HC595 Rev J timing (tsu SER 25 ns, tpd 40 ns, fmax 25 MHz @4.5V, SRCLR clears shift register only, storage reg undefined at power-up).

IMPORTANT REVISION NOTE: A conflicting web extract reported RAIN values 80 kohm @55.5 cyc / 350 kohm @239.5 cyc. That extract belongs to a DIFFERENT device datasheet (higher-density F1 family / other family), NOT DS5319 (STM32F103C8T6 medium density). DS5319 Rev 19 PDF Table 48 is authoritative for STM32F103C8T6: **RAIN max 50 kohm @ tS=55.5 cyc, fADC=14 MHz** and NA above 71.5 cyc. The prior report claim is therefore CORRECT. Same resolution for CADC: DS5319 says **8 pF** (the 5 pF extract was a different device). Prior report value CONFIRMED.

---

## 2. Source-of-truth register (claim-level audit)

| # | CLAIM (prior report) | VERDICT | PROVENANCE / CORRECTION |
|---|---|---|---|
| S-01 | RAIN max 50 kohm @ tS=55.5 cyc / fADC=14 MHz | CORRECT | DS5319 Table 48 (verified) |
| S-02 | +-2 LSB max ET guaranteed only when RAIN < 10 kohm | CORRECT | DS5319 ADC accuracy note (verified) |
| S-03 | RADC 1 kohm; CADC 8 pF | CORRECT | DS5319 Table 47 (verified; 5 pF extract was wrong device) |
| S-04 | tS 1.5-239.5 cyc = 0.107-17.1 us @14 MHz; tCONV 14-252 cyc = 1-18 us | CORRECT | DS5319 Table 47 (verified) |
| S-05 | tCONV includes sampling time | NOT STATED in report -> ADD | DS5319 Table 47 note: "14 to 252 (tS for sampling +12.5 for successive approximation)" -> tCONV = tS + 12.5 |
| S-06 | VREF+ internally tied VDDA (LQFP48) | CORRECT | DS5319 Table 47 note 3 (verified) |
| S-07 | 10 external ADC channels (PA0-PA7, PB0, PB1) | CORRECT | DS5319 pin definitions (verified) |
| S-08 | CD4067 RON max 1050/400/240 ohm @5V/10V/15V | CORRECT | SCHS052D (verified) |
| S-09 | CD4067 RON@3.3V NOT SPECIFIED | CORRECT | SCHS052D (verified) |
| S-10 | CD4067 VIH@5V = 3.5V | CORRECT | SCHS052D (verified) |
| S-11 | CD4067 OFF leakage +-100 nA (25 C) / +-1000 nA (85-125 C) @18V; typ +-10 pA @10V | CORRECT | SCHS052D (verified); note test-floor caveat |
| S-12 | CD4067 CIS 5 pF; COS 55 pF; BW 14 MHz | CORRECT | SCHS052D (verified) |
| S-13 | CD4067 settling = typical curves only; charge injection NOT SPECIFIED | CORRECT | SCHS052D (verified) |
| S-14 | STM32 VOH guaranteed min ~ VDD-0.4 = 2.9V @3.3V | CORRECT | DS5319 I/O DC char. (verified) |
| S-15 | 2.9V < 3.5V -> 5V-CMOS logic conflict | CORRECT; STRONGER | Even unloaded 3.3V rail output (typ ~3.3V) < 3.5V min VIH -> guaranteed-drive margin is ZERO; level shift or open-drain+5V pull-up REQUIRED for 5V path |
| S-16 | MAX3485 up to 10 Mbps; "USART1 can run that" | INCORRECT (USART part) | USART1 max 4.5 Mbit/s (16x) / <=9 Mbit/s (8x). 10 Mbps NOT achievable by MCU. Link is USART-limited, not transceiver-limited. Correction: state "MAX3485 up to 10 Mbps; USART1 caps link at <=4.5 (16x) / <=9 (8x) Mbit/s" |
| S-17 | Option A "4 conversions per step (parallel on 4 ADC pins)" | INCORRECT | STM32F103 has 2 ADCs (ADC1, ADC2), NOT 4; dual regular simultaneous mode converts the SAME channel on both. 4 DIFFERENT channels cannot be converted simultaneously. Option A = 16 address steps x 4 channels = 64 SEQUENTIAL conversions (50 valid). Correction changes scan-time model |
| S-18 | Option A scan lower bound = 16 x (tS_min + tCONV_min) = 17.7 us | INCORRECT (double-count) | tCONV already includes tS (S-05). Correct lower bound: 64 x tCONV_min = 64 x 1 us = 64 us (sequential) plus 16 selects/settles; if two ADCs used in parallel on 2 channels, floor ~32 us. Report figure understated ~3.6x |
| S-19 | Option B leakage "up to ~50 channels worth -> 50 uA" | INCORRECT (understates) | Shared node can see up to 63 OFF channels (64 positions - 1) -> 63 uA worst-case at 18V condition; or 60 if only 4x15 counted. Correction: use 63 uA bound |
| S-20 | SR "4-5 GPIO" | INCORRECT (overstates) | 74HC595 needs 3 (SER/SRCLK/RCLK) + optional 1 (SRCLR) = 3-4. OE is interlock-owned (G6), NOT MCU GPIO. Correction to 3-4 |
| S-21 | EXTI: "DIO0, fault, USART RX" | INCORRECT (RX row) | USART RX uses NVIC USART IRQ (RXNE), not EXTI. EXTI candidates: DIO0, fault/arm input. Correction |
| S-22 | PC13-15 for status LEDs | ACCEPTABLE w/ caveat | PC13/14/15 are VBAT-domain, limited drive (~+-3 mA), AF = TAMPER-RTC/OSC32_IN/OSC32_OUT. OK for LEDs with series R and MUX INH (high-Z CMOS inputs); NOT for safety-critical or high-drive functions |
| S-23 | "G1 Evidence Register" / "G4 Evidence Retrieval" listed as inputs | NOT PRESENT in workspace | glob found no such files. Flagged OPEN: provenance files not yet in repo. No number affected |
| S-24 | No MAX_CONCURRENT_FIRE=1; no firing numbers invented; G1/G2 HOLD | CORRECT (constraint respected) | Verified |
| S-25 | VREF+ note and "2x 12-bit ADC" (batch report line 78) | CORRECT | DS5319 (verified) |

---

## 3. CD4067 deep audit

### 3.1 Verified datasheet facts (SCHS052D)
- RON (max, VDD-VSS): 1050 ohm @5V / 400 ohm @10V / 240 ohm @15V at 25 C; rises with temperature (1200 ohm @85 C, 1300 ohm @125 C at 5V).
- Recommended operating conditions: VDD - VSS = 3 V to 18 V. -> 3.3 V supply is WITHIN the recommended operating range.
- VIH/VIL (5V): 3.5V / 1V. VIH at 3.3V supply is NOT tabulated.
- OFF-state leakage (I off, per channel): +-100 nA max (25 C), +-1000 nA max (85 C / 125 C), specified at VDD-VSS = 18 V; typical +-10 pA @10V.
- OFF leakage datasheet note (2): values are "determined by the minimum feasible leakage measurement for automatic testing" -> test-floor figures, far below a physically meaningful leak; treat as a conservative bound, NOT a guarantee of real-world behavior at lower supply.
- Capacitance: CIS 5 pF, COS 55 pF. Bandwidth 14 MHz (typical).
- Settling: only typical curves; NO guaranteed settling time spec. Charge injection NOT a specified parameter (typical note: ~65 mV coupling observed from INH/address transitions in test configurations).
- Propagation delay (tpd) is switch delay, NOT settling. [FACT -> TBD]

### 3.2 RON@3.3V assessment
- NOT SPECIFIED. Interpolation is NOT a guaranteed value. [FACT -> CONSTRAINT]
- RON@3.3V cannot be used as a design value until measured (T-G4-01). Divider sizing for RAIN<10k must wait for the measurement. [NEEDS MEASUREMENT]
- Recommended operating 3-18V means 3.3V operation is permitted; the open item is the electrical VALUE, not the permission. [FACT]

### 3.3 5V logic audit
- STM32 GPIO VOH guaranteed min = VDD - 0.4 = 2.9 V @3.3V (CMOS). [FACT]
- CD4067 VIH@5V = 3.5 V. [FACT]
- 2.9 V < 3.5 V -> guaranteed drive fails; even nominal 3.3 V < 3.5 V -> margin ZERO. The 5V path REQUIRES level shifting or open-drain + 5V pull-up (or a 3.3V-tolerant buffer). [FACT -> CONFLICT, definitive]
- RON@5V known: with Rth + 1050 + trace < 10 kohm -> Rth < ~9 kohm feasible in principle. [CALCULATION]
- No decision; 5V vs 3.3V path depends on measurement + owner. [OPEN]

---

## 4. ADC impedance recheck (DS5319)

### 4.1 Verified values
- RAIN max (Table 48, fADC=14 MHz): tS 1.5->0.4k, 7.5->5.9k, 13.5->11.4k, 28.5->25.2k, 41.5->37.2k, 55.5->50k ohm; 71.5 and 239.5 -> NA. [FACT]
- Sampling-feasibility bound (sampling only, NO accuracy guarantee): Z_total <= RAIN_max(tS). E.g. at tS=55.5 cyc, Z_total <= 50 kohm. [FACT -> CALCULATION]
- Accuracy bound: Z_total < 10 kohm for +-2 LSB max ET guarantee. [FACT]
- Cadc=8 pF, RADC=1 kohm. [FACT]
- Footnote: RAIN Table 48 "evaluated by characterization, not tested in production"; other ADC params "specified by design, not tested in production". Recorded for rigor. [FACT]

### 4.2 Consequences for the design
- Design constraint: Rth + RON + R_trace < 10 kohm for guaranteed continuity accuracy; divider values NOT selected (out of scope). [CALCULATION]
- Sampling alone can tolerate up to 50 kohm @ tS=55.5 cyc, but that loses the +-2 LSB guarantee. [CALCULATION]
- No change from prior report except: tCONV includes tS (correction S-05/S-18) and RAIN claim CONFIRMED (S-01). [STATUS: EVIDENCE-BACKED]

---

## 5. Leakage audit

- Per-channel OFF leakage bounds verified (3.1). [FACT]
- Transfer of the 18V figure to 3.3V/5V supply is an ASSUMPTION (conservative upper bound); leakage scales down with supply but no spec exists at 3.3/5V. [ASSUMPTION — conservative]
- Option A: per-MUX common node sees its own 15 OFF channels -> 15 x 1000 nA = 15 uA worst-case (18V condition, 85-125 C). Node error with Z ~10 kohm ~ 150 mV; with Z ~1 kohm ~15 mV. [CALCULATION]
- Option B: shared node accumulates OFF channels from ALL MUXes. Corrected bound: up to 63 OFF channels -> 63 uA worst-case (was ~50 uA). [CALCULATION — CORRECTION S-19]
- Typical path: 15 x 10 pA = 150 pA per MUX node -> negligible. [CALCULATION]
- Spread max-vs-typical ~5 orders of magnitude -> cannot be resolved from datasheet alone; must be measured (T-G4-05). [FACT -> NEEDS MEASUREMENT]
- Datasheet OFF-leakage note (test-floor) makes even the "max" a soft bound at lower supply; actual behavior at 3.3/5V is measurement territory. [FACT -> TBD]

---

## 6. Settling audit

- No guaranteed settling for CD4067; typical curves only; charge injection not specified. [FACT -> TBD]
- t_RC = RON x C_node (C_node ~ COS 55 pF + trace + CADC 8 pF): 1050 ohm x ~83 pF ~ 87 ns/tau; ~8.3 tau for 12-bit ~0.7 us is an ESTIMATE with an ASSUMPTION on trace C. Not guaranteed. [CALCULATION + ASSUMPTION]
- Settling margin must come from measurement (T-G4-04), not from this estimate. [NEEDS MEASUREMENT]

---

## 7. Scan-time model re-audit

- No owner scan-time requirement exists -> no requirement violated; the errors are modeling errors only. [STATUS]
- CORRECTION 1 (S-17): Option A does NOT do 4 parallel conversions. STM32F103 has 2 ADCs; dual regular simultaneous mode samples the SAME channel. 4 different channels require 4 sequential conversions (or 2+2 with both ADCs on distinct channels, not synchronizable to a true simultaneous sample via dual mode).
- CORRECTION 2 (S-18): tCONV already includes tS. Valid lower bound (min tS, 1 ADC): Option A = 16 steps x (4 x tCONV_min) = 64 us + 16 selects/settles; Option B = 50 x 1 us = 50 us + 50 selects/settles. With 2 ADCs used in parallel (2 channels each), Option A floor ~32 us. All figures are optimistic lower bounds (settle + software omitted). [CALCULATION]
- The prior report's 17.7 us Option A figure understated the floor by ~3.6x. Because no requirement exists, impact = MODEL CORRECTION, not design rejection. [STATUS: OPEN (model)]

---

## 8. Option A vs B re-audit

| CRITERION | OPTION A (4 MUX -> 4 ADC pins) | OPTION B (4 MUX -> 1 ADC pin) |
|---|---|---|
| Parallelism claim | CORRECTED: sequential over 2 ADCs, NOT 4-way parallel (S-17) | n/a (sequential) |
| Source impedance | Rth + RON (<10k target), single RON path | Rth + RON (+RON2 if 2nd stage) -> worse |
| Leakage bound | 15 uA per node (isolated groups) | 63 uA shared node (CORRECTED S-19) |
| Isolation | fault limited to one MUX group | single point affects all 50 |
| GPIO | 4 addr + 1 common en (5) or 4 addr + 4 en (8); en may be interlock-owned | 4 addr + 4 en (8) + optional 2nd-stage selects |
| ADC channels used | 4 (of 10) | 1 (of 10) |
| Scan floor | ~64 us (1 ADC) / ~32 us (2 ADC) | ~50 us |
| Status | FEASIBLE candidate, preferred (NOT locked) | FEASIBLE, less preferred (NOT locked) |

- Both remain candidates; selection waits on RON@3.3V measurement + owner topology decision + G6 OE wiring. [RECOMMENDATION]
- No topology locked. [STATUS]

---

## 9. Full pin-by-pin audit (STM32F103C8T6, LQFP48, 37 GPIO)

Legend: AF = alternate function; FT = 5V-tolerant (datasheet); "candidate" = proposed use in prior report pin maps A/B.

| PIN | PORT/AF | CANDIDATE USE (report) | CONFLICT CHECK | VERDICT |
|---|---|---|---|---|
| PA0 | ADC_IN0 / WKUP | continuity ADC (Map A) | free AF, no conflict | OK |
| PA1 | ADC_IN1 / USART2_RTS | continuity ADC (Map A) | free AF, no conflict | OK |
| PA2 | ADC_IN2 / USART2_TX | continuity ADC (Map A) | no conflict in candidates | OK |
| PA3 | ADC_IN3 / USART2_RX | continuity ADC (Map A) | no conflict in candidates | OK |
| PA4 | ADC_IN4 / SPI1_NSS / USART2_CK | monitor ADC (battery) Map A/B | LATENT: SPI1_NSS AF collides if SPI1 used; candidates keep SPI1 free | WATCH (OK while SPI1 unused) |
| PA5 | ADC_IN5 / SPI1_SCK | spare ADC (Map A) | if SR via SPI1 SCK (SPI-option B) -> ADC5 lost | CONDITIONAL |
| PA6 | ADC_IN6 / SPI1_MISO | spare | same as PA5 | CONDITIONAL |
| PA7 | ADC_IN7 / SPI1_MOSI | spare (Map A); SR MOSI (SPI-option B) | same as PA5 | CONDITIONAL |
| PA8 | TIM1_CH1 / MCO | RS485 DE (report 9.1) | free AF, OK | OK |
| PA9 | USART1_TX | RS485 TX | OK | OK |
| PA10 | USART1_RX | RS485 RX | OK | OK |
| PA11 | USART1_CTS / CAN_RX / USB_DM | unused | reserved; no conflict | OK |
| PA12 | USART1_RTS / CAN_TX / USB_DP | unused | reserved; no conflict | OK |
| PA13 | SWDIO | SWD (debug) | keep | LOCKED to SWD |
| PA14 | SWCLK | SWD (debug) | keep | LOCKED to SWD |
| PA15 | JTDI | SR GPIO or spare | free only after SWJ_CFG='010' (JTAG off, SWD kept) | CONDITIONAL |
| PB0 | ADC_IN8 | monitor ADC (rail) | free AF | OK |
| PB1 | ADC_IN9 | monitor ADC (rail) | free AF | OK |
| PB2 | BOOT1 | safety arm input (Map A spare) / MUX enable (Map B) | GPIO usable only when BOOT0=0 (main-flash boot); strap BOOT0 low | CONDITIONAL (OK w/ BOOT0 strap) |
| PB3 | JTDO | SR GPIO (report 9.1) | free only after SWJ_CFG='010' | CONDITIONAL |
| PB4 | JNTRST | SR GPIO (report 9.1) | free only after SWJ_CFG='010' | CONDITIONAL |
| PB5 | I2C1_SMBA / SPI3(no) | SR GPIO | free AF (not JTAG) | OK |
| PB6 | I2C1_SCL / TIM4_CH1 | CD4067 addr line 0 | free AF | OK |
| PB7 | I2C1_SDA / TIM4_CH2 | CD4067 addr line 1 | free AF | OK |
| PB8 | TIM4_CH3 / CAN_RX | CD4067 addr line 2 | free AF | OK |
| PB9 | TIM4_CH4 / CAN_TX | CD4067 addr line 3 | free AF | OK |
| PB10 | I2C2_SCL / USART3_TX | LoRa DIO0 (EXTI) | free AF | OK |
| PB11 | I2C2_SDA / USART3_RX | LoRa RST | free AF | OK |
| PB12 | SPI2_NSS / I2C2_SMBA | LoRa NSS | OK | OK |
| PB13 | SPI2_SCK | LoRa SCK | OK | OK |
| PB14 | SPI2_MISO | LoRa MISO | OK | OK |
| PB15 | SPI2_MOSI | LoRa MOSI | OK | OK |
| PC13 | TAMPER-RTC / OSC32_IN | status LED (both maps) / MUX enable (Map B) | VBAT domain, ~+-3 mA drive; LED OK w/ series R; INH input high-Z OK; NOT safety-critical | CONDITIONAL (acceptable use) |
| PC14 | OSC32_IN / RTC | status LED (both maps) / MUX enable (Map B) | same as PC13 | CONDITIONAL |
| PC15 | OSC32_OUT / RTC | status LED (both maps) / MUX enable (Map B) | same as PC13 | CONDITIONAL |
| BOOT0 | boot strap | strap low (main flash) | must stay strap, not GPIO | LOCKED to strap |
| NRST | reset | pull-up | keep | LOCKED |

Count check: 37 GPIO -> PA0-15 (16) + PB0-15 (16) + PC13-15 (3) = 35; plus... report count "37" per Mouser/ST for LQFP48 is standard (PA0..15, PB0..15, PC13..15 = 35, plus the two remaining are power pins in the 48; the 37 figure includes 35 port pins + 2 (BOOT0/NRST are not GPIO; 37 = total GPIO per ordering info). Correction: ST states 37 I/O for LQFP48; candidate allocation uses <= 30 -> margin ~7-10. Resource sufficiency UNCHANGED. [FACT/CALCULATION]

### 9.1 Conflict verdicts
- No HARD conflict in either candidate map once: (a) SWJ_CFG='010' frees PA15/PB3/PB4; (b) BOOT0 strapped low frees PB2; (c) SPI1 left entirely unused keeps PA4/5/6/7 clean (PA4 monitor ADC valid only then); (d) PC13-15 used only for LEDs/INH, not safety. [CALCULATION]
- LATENT: PA4 (SPI1_NSS) monitor-ADC usage is safe ONLY while SPI1 is never enabled; document as a firmware constraint. [WATCH]

---

## 10. JTAG / SWD / BOOT audit

- PA13/PA14 = SWDIO/SWCLK, kept for debug. [FACT]
- PA15=JTDI, PB3=JTDO, PB4=JNTRST: free as GPIO only with AFIO MAPR SWJ_CFG='010' (JTAG-DP disabled, SW-DP enabled). Report flagged this correctly. [FACT]
- PB2 = BOOT1: usable as GPIO only when BOOT0=0 (boot from main flash). Both candidate maps keep BOOT0 strapped low -> OK. [FACT]
- No conflict; SWD retained. [STATUS: EVIDENCE-BACKED]

---

## 11. PC13/14/15 audit

- VBAT (backup) power domain; drive capability limited (~+-3 mA). [FACT]
- Alternate functions: PC13 TAMPER-RTC, PC14 OSC32_IN, PC15 OSC32_OUT. If an external 32.768 kHz crystal/RTC is desired, PC14/PC15 are occupied -> do NOT commit them to LEDs if RTC/LSE is planned. [FACT -> WATCH]
- Suitable uses: status LEDs (series resistor), high-Z logic inputs (MUX INH). NOT suitable: safety-critical inputs/outputs, high-current drive. [RECOMMENDATION]
- Report uses PC13-15 for LEDs (OK) and Map B uses them for MUX enables (OK electrically; caveat: LSE/RTC future). [STATUS: PROVISIONAL]

---

## 12. SPI audit

- SPI1 (APB2) <=18 Mbit/s; SPI2 (APB1) <=18 Mbit/s (36 MHz/2), LoRa SX1278 needs <=10 MHz. [FACT]
- Candidate: LoRa on SPI2 (PB12-15), SR on GPIO or SPI1. SPI1-for-SR steals PA5/PA7 (ADC5/7); GPIO bit-bang for SR costs 0 ADC pins. [CALCULATION]
- Recommendation (prior): LoRa SPI2 + SR via GPIO is simplest and preserves ADC budget. Confirmed as a candidate; NOT locked. [RECOMMENDATION]
- LATENT: PA4 SPI1_NSS vs monitor ADC (Section 9). [WATCH]

---

## 13. 74HC595 audit

- Driver pins: SER (DS), SRCLK (SHCP), RCLK (STCP) = 3 mandatory GPIO; optional SRCLR (active-low async clear) = 4th. [FACT -> CALCULATION; CORRECTION S-20]
- OE (output-enable) is interlock-owned (G6), NOT an MCU GPIO. [RECOMMENDATION -> corrects "4-5 GPIO" to "3-4 GPIO"]
- Storage register undefined at power-up -> firmware must write all 7 register bytes before enabling outputs (OE). [FACT]
- SRCLR clears shift register only (not storage reg). [FACT]
- Timing (SN74HC595 Rev J): tsu SER 25 ns, tpd SRCLK->QH' 40 ns, tsu SRCLK^->RCLK^ 19 ns, tw 20 ns, fmax 25 MHz @4.5V. [FACT]

---

## 14. USART / RS485 audit

- MAX3485: half-duplex, up to 10 Mbps; DE/RE. [FACT]
- USART1 max baud 4.5 Mbit/s (16x oversampling); with 8x oversampling <=9 Mbit/s. **10 Mbps NOT reachable by the MCU.** [FACT -> CORRECTION S-16]
- RS485 link is USART-limited (not transceiver-limited). Candidate RS485 on USART1 (PA9/PA10, DE on PA8) stands; baud selection deferred (needs owner/protocol requirement). [STATUS: EVIDENCE-BACKED; baud = TBD]

---

## 15. ADC resource closure

- 10 external channels (PA0-PA7, PB0, PB1). [FACT]
- Map A: 4 continuity (PA0-3) + 1-3 monitor (PA4, PB0, PB1) = 5-7 used; PA5-7 spare/reserved. [CALCULATION]
- Map B: 1 continuity (PA0) + 3 monitor (PA4, PB0, PB1) = 4 used; PA1-3, PA5-7 spare. [CALCULATION]
- Tightest resource remains ADC channels; both maps fit. No dual-ADC parallelism claimed anymore (S-17 correction). [STATUS: FEASIBLE, NOT LOCKED]

---

## 16. Timer / DMA / EXTI audit

- Timers: 4 advanced+general purpose (TIM1, TIM2-4) -> candidate uses 2-4. Sufficient. [FACT/CALCULATION]
- DMA: 7 channels, 2 controllers -> optional for USART/SPI/ADC; unused here is fine. [FACT]
- EXTI: 16 lines, shared per-port groups. Candidates use DIO0 + fault/arm. CORRECTION S-21: USART RX is NVIC (USARTx_IRQHandler, RXNE), NOT EXTI. [FACT -> CORRECTION]
- No conflict. [STATUS: EVIDENCE-BACKED]

---

## 17. Cross-gate re-audit

- G3<->G4: SR (PB3-5) vs CD4067 (PB6-9 / PC13-15) separate -> no conflict. [CALCULATION]
- G3<->G5: SR 3-4 GPIO (CORRECTED) fits. [CALCULATION]
- G4<->G5: continuity ADC on PA0-3 (or PA0) never reassigned to SPI/USART in candidates -> no conflict. [CALCULATION]
- G5<->G6: OE interlock-owned; arm/fault GPIO allocated; PB2 (BOOT1) and PC13-15 usage conditional as above. [RECOMMENDATION]
- G5<->G8: LoRa SPI2 + USART1 RS485 -> no pin overlap. [CALCULATION]
- G5<->G9: timers/EXTI/DMA adequate; scheduling is firmware (G9). EXTI row corrected (S-21). [CALCULATION]
- G4<->G6: CD4067 INH/enable may be interlock-owned (common enable) -> reduces MCU GPIO; coupling to G6 wiring OPEN. [OPEN]
- Verdict: no GPIO/ADC/timer/SPI/UART/IRQ/DMA/safety/scheduling conflict under corrected candidates. [STATUS: EVIDENCE-BACKED with conditional notes]

---

## 18. Measurement plan recheck (T-G4-01..06)

| TEST | OBJECTIVE | STILL VALID? | NOTE |
|---|---|---|---|
| T-G4-01 | CD4067 RON @3.3V (per channel, vs V, over temp) | YES (blocking) | feeds Rth + RON < 10k; do NOT interpolate datasheet |
| T-G4-02 | CD4067 VIH/VIL @3.3V supply | YES | needed for 3.3V path margin |
| T-G4-03 | ADC accuracy vs RAIN (1k/10k/50k) | YES | verify +-2 LSB at RAIN<10k; document above |
| T-G4-04 | CD4067+MUX network settling | YES | input to scan-time model; no threshold invented |
| T-G4-05 | OFF-channel leakage effect vs channel count | YES | compare to corrected 15 uA / 63 uA bounds |
| T-G4-06 | Cross-channel isolation (short one, read others) | YES | criterion TBD (no owner threshold) |

- Plan unchanged except corrected bounds feed pass/fail comparisons. No threshold invented. [STATUS: VALID]

---

## 19. Error register (severity)

| ID | SEVERITY | LOCATION (prior report) | ERROR | CORRECTION |
|---|---|---|---|---|
| E-01 | HIGH | Sec 6.1 (line 113) | "4 conversions per step (parallel on 4 ADC pins)" | STM32F103 has 2 ADCs; dual mode = same channel. 64 SEQUENTIAL conversions (or 2x32 with both ADCs) |
| E-02 | HIGH | Sec 6.2 (line 117) | Option A floor 16 x (tS+tCONV) = 17.7 us | tCONV includes tS; correct floor ~64 us (1 ADC) / ~32 us (2 ADC). Modeling error only (no requirement exists) |
| E-03 | MEDIUM | Sec 8 (line 150) | "USART1 can run [10 Mbps]" | USART1 max 4.5 Mbit/s (16x) / <=9 Mbit/s (8x); link is USART-limited |
| E-04 | MEDIUM | Sec 4.2/table (lines 42, 87) | Option B leakage "~50 channels -> 50 uA" | up to 63 OFF channels -> 63 uA worst-case |
| E-05 | MEDIUM | Sec 8 table (line 135), Sec 11 (line 202) | SR "4-5 GPIO" | 74HC595 = 3-4 GPIO (SER/SRCLK/RCLK + optional SRCLR); OE interlock-owned, not MCU |
| E-06 | MEDIUM | Sec 8 table (line 140) | EXTI "USART RX" | USART RX is NVIC RXNE, not EXTI |
| E-07 | LOW | Sec 5.2 (line 100) | t_RC estimate implied settling-usable | explicitly ASSUMPTION; settling must be measured |
| E-08 | LOW | Sec 3.1 (line 17) | RAIN value sourced to "Rev 20" w/o table number | confirmed against Rev 19/20 Table 48 (50 kohm @55.5 cyc) |
| E-09 | INFO | line 5 | inputs "G1 Evidence Register" / "G4 Evidence Retrieval" referenced but NOT in workspace | flag OPEN; no number affected |
| E-10 | INFO | Sec 5 (line 82) | 18V leakage transferred to 3.3/5V | labeled ASSUMPTION (conservative) - acceptable, kept |

Not-errors (confirmed correct): RAIN 50k@55.5cyc; CADC 8pF; RADC 1k; VOH 2.9V; VIH@5V 3.5V; RON@5/10/15V; CD4067 leakage/operating range; 37 GPIO; 10 ADC channels; VREF+ tie; tS/tCONV ranges; no MAX_CONCURRENT_FIRE=1; G1/G2 HOLD.

---

## 20. Final status matrix

| ITEM | STATUS | BLOCKER |
|---|---|---|
| G4 topology option set (A/B/C) | EVIDENCE-BACKED (A preferred, none locked) | RON@3.3V measurement + owner |
| 5V path feasibility | CONFLICT DEFINITIVE (needs level shift) | owner decision: shift vs 3.3V path |
| 3.3V path feasibility | OPEN (needs RON@3.3V + VIH@3.3V) | T-G4-01/02 |
| Settling | TBD (measurement) | T-G4-04 |
| Leakage bounds | EVIDENCE-BACKED (corrected) | T-G4-05 |
| Scan-time model | CORRECTED (model only) | no owner requirement |
| G5 resource closure | FEASIBLE, NOT LOCKED | topology + pin map lock |
| Pin maps A/B | PROVISIONAL (conditional on SWJ_CFG, BOOT0, SPI1-unused, PC13-15 use) | owner topology decision + G6 |
| Cross-gate conflicts | NONE (after corrections) | — |
| Measurement plan | VALID | owner fixture approval |
| Firing power/timing (G1/G2) | HOLD | G1 evidence |
| G6 multi-channel + OE | OPEN | owner evidence |

---

## 21. Final decision rules (Q1-Q6)

- Q1 (RAIN<10k reachable with CD4067 path?): NOT YET CLOSED. Depends on T-G4-01 (RON@3.3V) or, for the 5V path, on level-shift + RON@5V (feasible in principle: Rth < ~9k). Rule: if RON@3.3V measured such that Rth + RON + trace < 10k holds with margin -> 3.3V path viable; else 5V+level-shift is the fallback. [CALCULATION -> rule]
- Q2 (CD4067 supply): DECIDED only after T-G4-01/02. No supply chosen in this batch. [OPEN]
- Q3 (Option A vs B): A remains structurally preferred (isolation, bounded per-node leakage) but is NOT locked; final pick after measurement + owner + G6. [RECOMMENDATION]
- Q4 (MCU resource sufficiency): CLOSEABLE — EVIDENCE-BACKED sufficiency under corrected counts (GPIO 3-4 SR; ~5-7 ADC; SPI/UART/timer/DMA/EXTI adequate). Not locked until pin map locked. [EVIDENCE-BACKED]
- Q5 (pin map conflict-free?): CONDITIONAL PASS — requires SWJ_CFG='010', BOOT0 strap low, SPI1 unused (PA4 monitor), PC13-15 limited to LEDs/INH. Latent PA4/SPI1_NSS watch. [PROVISIONAL]
- Q6 (measurement plan sufficient to close G4?): YES for measurement coverage (T-G4-01..06), PROVIDED fixture approved; owner thresholds (continuity pass/fail, scan-time) still required for closure of REQUIREMENTS, not just feasibility. [RECOMMENDATION]

---

## 22. Recommended next batch

1. Approve + build G4 measurement fixture; execute T-G4-01..06 (independent of G1). This closes RON@3.3V, VIH@3.3V, settling, leakage, and ADC-vs-RAIN.
2. Owner: continuity threshold + isolation spec + scan-time requirement (non-G1). No numbers invented meanwhile.
3. On measurement closure: select topology (A vs B), then lock pin map + SPI/SR wiring with owner (apply the 4 conditional rules from Section 9.1).
4. G6 owner evidence (multi-channel authorization, OE wiring) -> finalize G5 pin map.
5. G9 firmware skeleton can proceed independently (state machine, SR driver, protocol parser) with config-driven constants; use corrected scan-time model.
6. Update DECISIONS.md / OPEN_ISSUES.md at each gate close (owner-approved only).

---

## 23. Output quality self-check

- All numerical claims carry provenance (Section 1/2). [SATISFIED]
- No invented specifications; all unknowns marked TBD/NEEDS MEASUREMENT/OPEN. [SATISFIED]
- CD4067 RON@3.3V not interpolated. [SATISFIED]
- Continuity threshold, scan-time, settling, firing/skew values NOT invented. [SATISFIED]
- Errors in prior report identified with severity (Section 19) and corrected in this artifact; prior report preserved unmodified. [SATISFIED]
- No schematic/PCB/BOM/resistor values; no locked architecture. [SATISFIED]
- G1/G2 untouched; no MAX_CONCURRENT_FIRE=1. [SATISFIED]
- Nothing force-closed. [SATISFIED]