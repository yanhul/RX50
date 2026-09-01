# RX50 G4-G5 HARDWARE FEASIBILITY REPORT

Status: DRAFT (batch phase 12 output)
Date: 2026-08-15
Input: RX50_BATCH_ENGINEERING_REPORT.md, RX50_FEASIBILITY_G3_G4_G5_G6_G8.md, RX50_G9_FIRMWARE_AND_CROSS_GATE_REPORT.md, G1 Evidence Register, G4 Evidence Retrieval.
Scope: G4 continuity hardware feasibility + G5 MCU resource/pin-map candidate. G1/G2 remain HOLD. No schematic/PCB/BOM. No locked decision.

Label legend:
- [FACT]            Manufacturer / datasheet / explicit requirement evidence.
- [CALCULATION]     Arithmetic from inputs; valid only if inputs valid.
- [ASSUMPTION]      Engineering assumption. NOT a requirement.
- [RECOMMENDATION]  Proposed direction; requires owner approval.
- Status: LOCKED / EVIDENCE-BACKED / HOLD / TBD / NEEDS RECHECK / OPEN / PROVISIONAL / CLOSEABLE.

Key evidence reused (provenance in earlier reports):
- TI CD4067B SCHS052D Rev D: RON max 1050 ohm @5V, 400 ohm @10V, 240 ohm @15V (25 C); RON@3.3V NOT SPECIFIED; VIH@5V = 3.5V; OFF leakage +-100 nA (25 C) / +-1000 nA (85-125 C) @18V, +-10 pA typ @10V; CIS 5 pF; COS 55 pF; BW 14 MHz; settling = typical curves only, NO guaranteed value; charge injection NOT SPECIFIED.
- ST DS5319 Rev 20 Sec 5.3.18: RADC 1 kohm; CADC 8 pF; tS 1.5-239.5 cyc (0.107-17.1 us @14 MHz); tCONV 14-252 cyc (1-18 us); RAIN max 50 kohm @ tS=55.5 cyc/fADC=14 MHz; +-2 LSB max ET guaranteed only when RAIN < 10 kohm; VREF+ internally tied VDDA (LQFP48); 10 external ADC channels (PA0-PA7, PB0, PB1).
- TI SN74HC595 Rev J: tsu SER 25 ns; tpd SRCLK->QH' 40 ns; tsu SRCLK^->RCLK^ 19 ns; tw 20 ns; fmax 25 MHz @4.5V; storage register undefined at power-up; SRCLR clears shift register only.
- SX1278: SPI up to 10 MHz; packet engine up to 256 bytes; 256-byte FIFO.
- MAX3485: half-duplex up to 10 Mbps; DE/RE.
- STM32F103 SPI1 (APB2) up to 18 Mbit/s; SPI2 (APB1).

---

## 1. Executive Summary

- G4 topology: THREE candidates evaluated (A = 4x CD4067 -> 4 ADC; B = 4x CD4067 -> 1 ADC via shared node/2nd stage; C = alternatives). **Option A is structurally preferred** (best isolation, single RON path per ADC, bounded per-MUX leakage) but is NOT locked. [CALCULATION/RECOMMENDATION]
- G4 source impedance: the decisive datasheet fact is **RAIN < 10 kohm for +-2 LSB guaranteed accuracy**. Both 5V and 3.3V CD4067 paths have a hard obstacle:
  - 5V supply: **VIH@5V = 3.5V conflicts with 3.3V logic guaranteed VOH (~2.9V)** -> needs level shifting or open-drain + 5V pull-up. [FACT -> conflict]
  - 3.3V supply: **RON@3.3V NOT SPECIFIED** -> cannot be used as guaranteed value; measurement required. [FACT -> NEEDS MEASUREMENT]
- G4 settling: datasheet gives NO guaranteed settling for CD4067 (typical curves only) -> settling is TBD/measurement. Propagation delay is NOT settling. [FACT -> TBD]
- G4 leakage: worst-case OFF-channel leakage is datasheet-boundable (15 channels x +-1000 nA = up to 15 uA per MUX node at 85-125 C / 18V condition, conservative) and can shift a 10 kohm sense node by ~150 mV worst-case; typical (+-10 pA @10V) is negligible -> must be measured. [CALCULATION + TBD]
- G5 MCU closure: STM32F103C8T6 has adequate GPIO (37), ADC (10 ext channels), SPI (2), USART (3), timers (4), EXTI, DMA (7ch), RAM (20 KB), Flash (64 KB) for the candidate architecture. **Tightest resource remains ADC channels** (continuity + monitoring ~5-7 of 10). [CALCULATION]
- Two candidate pin maps (A: 4-ADC continuity; B: 1-ADC continuity) are presented. Both keep SWD, avoid SPI1<->ADC conflict by placing LoRa on SPI2, keep RS485 on USART1, keep continuity ADC on non-SPI pins. NOT locked. [RECOMMENDATION]
- No MAX_CONCURRENT_FIRE=1. No firing current/pulse/energy/voltage/timing invented. No firing-power feasibility conclusion reached (G2 domain). [CONSTRAINT respected]

## 2. G4 topology candidates

| OPTION | MUX COUNT | ADC COUNT | GPIO | SETTLING PATH | LEAKAGE PATH | SOURCE IMPEDANCE | COMPLEXITY | RISKS | STATUS |
|---|---|---|---|---|---|---|---|---|---|
| A: 4x CD4067 -> 4 ADC (shared address, common enable) | 4 | 4 | 4 addr + 1 common enable = 5 (or 4 addr + 4 en = 8) | 1 RON path per ADC node: Rth(divider) + RON + trace | Per-MUX common node sees only its own 15 OFF channels; MUX groups isolated from each other | Z = Rth + RON per channel; target Rth + RON < 10k | Low-moderate; 4 ADC channels consumed; 16 address steps cover 64 slots (50 used, 14 spare) | 4 ADC channels used; accuracy per node; RON@3.3V unknown | **FEASIBLE candidate, preferred** (not locked) |
| B: 4x CD4067 -> 1 ADC (shared node via per-MUX INH, or 2nd-stage MUX) | 4 (+1 if 2nd stage) | 1 | 4 addr + 4 en = 8 (+ 4 2nd-stage select if used) | 1 RON (per-MUX enable) or 2x RON in series (2nd stage) | Shared node accumulates leakage from all 4 MUXes (conservative up to ~50 channels worth) | Z = Rth + RON (+RON2) -> worse than A | Higher; more GPIO; shared-node coupling | Series RON hurts RAIN<10k; shared-node leakage; single-point fault affects all | FEASIBLE but less preferred (not locked) |
| C: alternatives (different MUX family w/ RON@3.3V; hierarchical; longer tS) | varies | varies | varies | varies | varies | varies | varies | Replacing part is NOT allowed in this batch (instruction); longer tS does NOT restore guaranteed accuracy above RAIN 10k | Not selected; documented OPEN |

Notes:
- Option A maps naturally to the 10 external ADC channels of STM32F103C8 (PA0-PA7, PB0, PB1). [FACT -> CALCULATION]
- 16 address steps x 4 = 64 positions >= 50 channels; the 14 unused addresses are masked in firmware. [CALCULATION, ASSUMPTION 1:1 fan-out — NOT locked]
- No option is locked; final choice waits on RON@3.3V measurement and owner topology decision. [RECOMMENDATION]

## 3. ADC / source-impedance analysis

### 3.1 Facts
- RAIN max 50 kohm @ tS=55.5 cycles / fADC=14 MHz: maximum source impedance for correct sampling at the longest used sampling time. [FACT — DS5319]
- Accuracy +-2 LSB max total error guaranteed ONLY when RAIN < 10 kohm. [FACT — DS5319]
- RADC = 1 kohm; CADC = 8 pF. [FACT — DS5319]
- tS = 1.5-239.5 cycles = 0.107-17.1 us @14 MHz; tCONV = 14-252 cycles = 1-18 us. [FACT — DS5319]
- VREF+ internally tied to VDDA on LQFP48 -> ADC full scale = VDDA. [FACT — DS5319]
- CD4067 RON: max 1050 ohm @5V, 400 ohm @10V, 240 ohm @15V (25 C); RON rises with temperature. RON @3.3V NOT SPECIFIED. [FACT — SCHS052D]

### 3.2 Case 1: CD4067 powered at 5 V
- Control from STM32 3.3V: STM32 GPIO VOH (guaranteed) ~ VDD - 0.4 = 2.9V; CD4067 VIH @5V = 3.5V. **2.9V < 3.5V -> guaranteed VOH does NOT meet VIH.** [FACT -> CONFLICT]
- Mitigation options: level shifter, or open-drain + pull-up to 5V, or a 3.3V-tolerant buffer — requires added components. Not decided. [RECOMMENDATION]
- RON@5V known (1050 ohm max). With Rth(divider) budget so Rth + 1050 + trace < 10k -> Rth < ~9k. Achievable in principle. [CALCULATION]
- Consequence: 5V path adds a level-shifting requirement; still feasible but with extra hardware. [ASSUMPTION/RECOMMENDATION]

### 3.3 Case 2: CD4067 powered at 3.3 V
- RON@3.3V is NOT specified by the manufacturer. **Interpolation is NOT a guaranteed value.** [FACT — CONSTRAINT]
- Control at 3.3V: VIH@3.3V is not in the datasheet (characterized at 5/10/15V) -> also needs verification. [FACT -> NEEDS MEASUREMENT]
- Measurement requirement: determine RON@3.3V (per channel, over temperature) before this path can be assessed. [NEEDS MEASUREMENT]

### 3.4 Symbolic model (no divider values chosen)
- Z_total = Rth(divider) + RON(MUX) + R_trace. [CALCULATION]
- Accuracy target: Z_total < 10 kohm (for +-2 LSB max ET). [FACT -> design constraint]
- Sampling-feasibility bound: Z_total <= 50 kohm (sampling only, no accuracy guarantee). [FACT]
- So the design must satisfy Z_total < 10k for the continuity threshold to be guaranteed accurate. Divider values NOT selected in this batch. [CALCULATION — no divider values locked]

## 4. Leakage analysis

### 4.1 Datasheet facts
- OFF-state leakage +-100 nA max (25 C), +-1000 nA max (85-125 C), specified at VDD-VSS = 18 V. [FACT — SCHS052D]
- Typical +-10 pA @ 10V. [FACT — SCHS052D]
- At 3.3V/5V supply, the 18V max is a conservative upper bound (leakage scales down with supply, but no spec at 3.3/5V). [ASSUMPTION — conservative]

### 4.2 Upper-bound CALCULATION
- Option A: per-MUX common node sees 15 OFF channels: worst-case 15 x 1000 nA = **15 uA** (at 85-125 C, 18V condition). [CALCULATION]
- Voltage error on sense node: V_err = I_leak x Z_total. With Z_total ~ 10 kohm -> 150 mV; with Z_total ~ 1 kohm -> 15 mV. [CALCULATION]
- Option B: shared node conservative upper bound = up to ~50 channels worth -> 50 uA worst-case (higher than A). [CALCULATION]
- Typical path: 15 x 10 pA = 150 pA -> negligible. [CALCULATION]
- Consequence: the spread between worst-case max and typical is ~5 orders of magnitude -> **cannot be resolved from datasheet alone; must be measured**. [FACT -> NEEDS MEASUREMENT]

### 4.3 What CAN be bounded vs NOT
- BOUNDED (datasheet): per-channel OFF leakage max at 18V; node accumulation by channel count. [FACT/CALCULATION]
- NOT BOUNDED: leakage at 3.3V/5V actual supply; part-to-part; temperature behavior between datasheet points; effect on final divider network. [TBD -> measurement]
- No safety requirement created; only FACT/CALCULATION/OPEN items. [CONSTRAINT respected]

## 5. Settling analysis

### 5.1 Term decomposition (NOT propagation delay)
- t_select: GPIO/address setup + MUX propagation delay (datasheet tpd) — this is switching time, NOT settling. [FACT — SCHS052D gives tpd only]
- t_RC: RON x C_node; C_node ~ COS(55 pF) + trace + CADC(8 pF). RON@5V max 1050 ohm x ~83 pF ~ 87 ns per tau; ~8.3 tau for 12-bit ~ 0.7 us. [CALCULATION with ASSUMPTION on trace C; NOT guaranteed]
- t_ADC_acquisition: tS 1.5-239.5 cyc = 0.107-17.1 us. [FACT]
- t_conversion: tCONV 14-252 cyc = 1-18 us. [FACT]
- t_software: scheduler/ISR overhead (implementation-bound). [ASSUMPTION]

### 5.2 Status
- CD4067 settling time has NO guaranteed datasheet value (typical curves only); charge injection NOT SPECIFIED. [FACT -> TBD]
- Therefore t_RC and any settling margin are **TBD/measurement**; do NOT treat the RC estimate as guaranteed. [CONSTRAINT respected]

## 6. Scan-time model

### 6.1 Symbolic model
- T_scan = Sum over steps (t_select + t_settle + t_acquire + t_convert + t_overhead). [CALCULATION]
- Option A: 16 address steps; 4 conversions per step (parallel on 4 ADC pins) -> 64 conversion slots, 50 valid. [CALCULATION/ASSUMPTION]
- Option B: 50 sequential measurements -> 50 conversions, 50 selects. [CALCULATION/ASSUMPTION]

### 6.2 Lower bounds (datasheet mins only)
- Option A: 16 x (tS_min + tCONV_min) = 16 x (0.107 + 1) us ~= 17.7 us (plus settle + software overhead). [CALCULATION — optimistic lower bound]
- Option B: 50 x (0.107 + 1) us ~= 55 us (plus settle + overhead). [CALCULATION — optimistic lower bound]
- Unknown terms: t_settle (measurement), t_overhead (implementation). [TBD]
- No scan-time requirement is set in this report (no owner requirement exists). [CONSTRAINT respected]

## 7. Channel isolation analysis

- One channel OPEN: that channel's divider/reading reflects the open condition; in Option A other channels on the same MUX are unaffected (their own divider nodes), other MUXes fully unaffected. [FACT-based, ASSUMPTION]
- One channel SHORT: affects that channel's divider node; if the short is on the MUX input side, Option A limits impact to that address position; a short on the MUX output/common node would affect that MUX's group (up to 16 channels). [ASSUMPTION/OPEN]
- Abnormal leakage: not boundable without a spec -> OPEN. [OPEN]
- MUX OFF leakage: boundable (Section 4). [CALCULATION]
- Fault on common ADC node (Option B): affects all 50 channels (single point). Option A reduces blast radius to one MUX group. [CALCULATION — isolation advantage of A]
- No safety requirement created; items labeled FACT/CALCULATION/ASSUMPTION/OPEN. [CONSTRAINT respected]

## 8. G5 MCU resource closure

| RESOURCE | CURRENT PROPOSAL | USED | AVAILABLE | MARGIN | CONFLICT | STATUS | EVIDENCE |
|---|---|---|---|---|---|---|---|
| GPIO | SR 4-5 + CD4067 5-8 + LoRa 3 + RS485 DE 1 + safety arm/fault 2 + LED 2 | ~25-27 | 37 | ~10 | none found in candidates | FEASIBLE (not locked) | DS5319; G3/G6/G8 |
| ADC | 4 continuity (Opt A) + 1-2 monitor = 5-6 | 5-6 | 10 ext (PA0-7,PB0,PB1) | ~4-5 | SPI1 would steal PA5-7 if used for SR/LoRa -> avoid | FEASIBLE, tightest | DS5319; G4 |
| SPI | LoRa SPI2 (PB13-15); SPI1 free | 1 | 2 | 1 | none (SPI2 avoids ADC pins) | FEASIBLE (not locked) | DS5319; SX1278 <=10MHz |
| UART | USART1 RS485 (PA9/10) + DE; 1 debug spare | 2 | 3 | 1 | none | FEASIBLE | DS5319; MAX3485 |
| Timers | 2-4 (scan sched, blanking/RCLK, link watchdog) | 2-4 | 4 | 0-2 | none | FEASIBLE | DS5319 |
| EXTI | DIO0, fault, USART RX | ~3 | EXTI0-15 | large | none | FEASIBLE | DS5319 |
| DMA | optional USART/SPI | 0-3 | 7 | large | none | FEASIBLE (optional) | DS5319 |
| RAM | shadow 7 B + channel 50 B + buffers + stack | est <=2 KB | 20 KB | large | none | FEASIBLE (structural est) | DS5319 |
| Flash | firmware (TBD) | TBD | 64 KB | TBD | none | NEEDS RECHECK (no code) | DS5319 |
| Watchdog | IWDG (HW) + WWDG (opt) | 1-2 | 2 | 1 | none | FEASIBLE | DS5319 |
| Debug pins | SWD PA13/PA14 | 2 | 2 (SWD) | 0 | keep SWD; PA15/PB3/PB4 free if JTAG off | FEASIBLE | DS5319 |
| Boot pins | BOOT0 strap; NRST | 0-1 | 1 | 0 | keep BOOT0 strap, NRST | FEASIBLE | DS5319 |

Special checks:
- LoRa: SX1278 SPI <= 10 MHz; SPI2 (APB1) can run <= 10 MHz; NSS/RST/DIO0 on GPIO/EXTI. [FACT -> CALCULATION]
- RS485: MAX3485 up to 10 Mbps; USART1 can run that; DE/RE GPIO. [FACT -> CALCULATION]
- 74HC595: 4-5 GPIO, no timer needed for shift (bit-bang or SPI). [FACT -> CALCULATION]
- CD4067: 4-8 GPIO for address/enable (Option A = 5 with common enable). [CALCULATION]
- ADC monitoring: battery/rail on remaining ADC channels (e.g., PA4, PB0/PB1). [CALCULATION]
- Safety/interlock: arm + fault GPIO; OE handled by interlock hardware, not MCU-direct. [RECOMMENDATION]
- LED/status: 2 GPIO (PC13-PC15 available). [CALCULATION]
- SWD: PA13/PA14 kept for debug; disabling JTAG frees PA15, PB3, PB4. [FACT — DS5319 alternate functions]

## 9. Candidate pin maps (NOT locked)

### 9.1 Common base (both maps)
- LoRa on SPI2: PB13 SCK, PB14 MISO, PB15 MOSI, PB12 NSS, PB11 RST, PB10 DIO0 (EXTI).
- RS485 on USART1: PA9 TX, PA10 RX, PA8 DE.
- SR chain: SER/SRCLK/RCLK on non-ADC GPIO (e.g., PB3/PB4/PB5, free after JTAG-off or used as GPIO), OE via interlock.
- CD4067 address: PB6/PB7/PB8/PB9 (4 lines).
- Safety: arm + fault input on spare GPIO (e.g., PB2 if not BOOT1-dependent, or PA15/PB3/PB4).
- SWD: PA13/PA14. BOOT0 strap. NRST with pull-up.
- Status LEDs: PC13/PC14/PC15.
- Monitor ADC: PA4 (battery), PB0/PB1 (rail) — depending on map.

### 9.2 Pin Map A (continuity Option A: 4-ADC)
- Continuity ADC: PA0, PA1, PA2, PA3 (CD4067 outputs MUX1-4).
- Monitor ADC: PA4, PB0, PB1 (battery + rails); PA5/PA6/PA7 spare (reserved; NOT used by SPI to protect ADC budget).
- Uses ~4 of 10 ADC for continuity + 1-3 monitor. [CALCULATION]
- Conflict check: none between continuity ADC (PA0-3), SPI2 (PB12-15), USART1 (PA9/10). [CALCULATION]

### 9.3 Pin Map B (continuity Option B: 1-ADC shared sense)
- Continuity ADC: PA0 (shared sense node).
- Monitor ADC: PA4, PB0, PB1 (and PA1-PA3 spare).
- CD4067 enable: PB6-PB9 address + 4 INH/enable lines (PC13, PC14, PC15 + PB2) -> more GPIO used than Map A. [CALCULATION]
- Trade-off: fewer ADC channels used, but shared-node leakage/isolation worse and more GPIO consumed. [CALCULATION/RECOMMENDATION]

### 9.4 Comparison
- Map A: better isolation, parallel scan speed, bounded leakage, but consumes 4 ADC channels (still within 10). [CALCULATION]
- Map B: fewer ADC channels, but single point of failure on shared node and higher leakage accumulation. [CALCULATION]
- No final selection: depends on RON@3.3V measurement + owner topology decision + G6 OE wiring. [RECOMMENDATION]

## 10. SPI architecture comparison

| OPTION | LoRa | SR | PIN EFFECT | CLOCK | CS | DMA | INTERRUPT | ADC PRESERVATION | FIRMWARE COMPLEXITY | STATUS |
|---|---|---|---|---|---|---|---|---|---|---|
| A: LoRa SPI1, SR GPIO | SPI1 (PA5-7) | GPIO bit-bang (SER/SRCLK/RCLK) | Uses PA5-7 (ADC5-7) for LoRa; SR on non-ADC GPIO | SPI1 up to 18 MHz (LoRa <=10 MHz) | PA4 NSS | optional | DIO0 EXTI | Loses PA5-7 as ADC; continuity can use PA0-4+PB0-1 (7 avail) | low | FEASIBLE candidate |
| B: LoRa SPI2, SR SPI1 | SPI2 (PB13-15) | SPI1 MOSI/SCK (PA7/PA5) + GPIO RCLK | Uses PB12-15 for LoRa; PA5/PA7 for SR SCK/MOSI | SPI2 <=10 MHz (LoRa); SPI1 up to 18 MHz (SR) | PB12 NSS + SR RCLK GPIO | optional | DIO0 EXTI | Loses PA5/PA7 (ADC5/7) for SR; PA0-4+PB0-1 still usable (7 avail) | moderate | FEASIBLE candidate |
| C: shared SPI | shared bus, separate NSS | same SPI | same pins as A | must serve both; contention | 2 NSS | complex | DIO0 EXTI + SPI | same as A | high (bus arbitration, no mixing SR/LoRa frames) | NOT preferred |

- Recommendation: **Option B (LoRa SPI2, SR via SPI1 or GPIO)** preserves the ADC pin budget best and keeps LoRa on a dedicated SPI. GPIO bit-bang for SR is simplest and lowest-risk; SPI1-for-SR is optional if shift speed matters. [RECOMMENDATION — NOT a locked decision]
- SX1278 SPI <= 10 MHz is satisfied by both SPI1 and SPI2. [FACT -> CALCULATION]
- No decision locked; final choice with owner after G4 topology and G6 OE wiring are fixed. [CONSTRAINT respected]

## 11. Cross-gate conflicts

- G3 <-> G4: SR GPIO and CD4067 GPIO are separate (SR on PB3-5, CD4067 on PB6-9/PC13-15 in candidates) -> no conflict. [CALCULATION]
- G3 <-> G5: SR needs 4-5 GPIO; available. No conflict. [CALCULATION]
- G4 <-> G5: candidate pin maps reserve PA0-PA3 (or PA0) for continuity ADC. **Map A does NOT cause continuity to lose ADC channels**; Map B uses fewer. Verified: continuity ADC is not reassigned to SPI/USART in either candidate. [CALCULATION — key check]
- G5 <-> G6: OE is interlock-driven (hardware), not MCU; arm/fault GPIO allocated. No conflict. [RECOMMENDATION]
- G5 <-> G8: LoRa SPI2 + USART1 RS485; no pin overlap. [CALCULATION]
- G5 <-> G9: timers/EXTI/DMA adequate; scheduling (scan vs SR update vs comm) handled at firmware level (G9 report Section 3.4/4.4). No resource conflict. [CALCULATION]
- No GPIO/ADC/timer/SPI/UART/IRQ/DMA/safety/scheduling conflict found under the candidates. [CALCULATION]

## 12. Measurement plan (G4 gaps)

| TEST ID | OBJECTIVE | SETUP | MEASUREMENT | PASS/FAIL CRITERION | DEPENDENCY |
|---|---|---|---|---|---|
| T-G4-01 | CD4067 RON @3.3V | CD4067 powered 3.3V; force small current through selected channel; measure drop | RON per channel, vs V, over temp (25/85C) | criterion TBD (feeds topology decision; if RON keeps Rth+RON<10k feasible, OK) | none |
| T-G4-02 | CD4067 VIH @3.3V supply | sweep control voltage vs output switch state | VIH/VIL at 3.3V supply | criterion TBD (needs margin vs 3.3V logic high) | none |
| T-G4-03 | STM32F103 ADC accuracy vs RAIN | known resistor ladder into ADC pin; compare code vs ideal | error LSB at RAIN = 1k/10k/50k | verify +-2 LSB at RAIN<10k (datasheet); document deviation above | minimal ADC firmware |
| T-G4-04 | CD4067+MUX network settling | step address; scope on ADC node | time to settle within X mV | criterion TBD (input to scan-time model) | none |
| T-G4-05 | OFF-channel leakage effect | all-but-one channels terminated; measure node voltage | node error vs channel count | criterion TBD (compare vs datasheet bound) | none |
| T-G4-06 | Cross-channel isolation | short one channel; read others | change in other channels' readings | criterion TBD (no owner threshold) | none |

- No firing-related test. No threshold invented (criteria marked TBD where no requirement). [CONSTRAINT respected]

## 13. CLOSEABLE / OPEN / HOLD / TBD

- CLOSEABLE NOW (structural): G5 resource sufficiency for the candidate architecture; G4 topology option set defined; cross-gate pin/ADC/SPI conflicts absent; VIH@5V conflict identified and bounded. [EVIDENCE-BACKED/CALCULATION]
- EVIDENCE-BACKED: ADC params (DS5319), CD4067 RON@5/10/15V + VIH@5V + leakage max (SCHS052D), SR timing (SCLS041J), SX1278 SPI <=10MHz, MAX3485 <=10Mbps, STM32 SPI1/SPI2.
- FEASIBLE BUT NOT LOCKED: Option A topology (preferred), pin maps A/B, SPI option B (LoRa SPI2).
- NEEDS MEASUREMENT: CD4067 RON@3.3V, VIH@3.3V, settling, leakage, ADC-vs-RAIN verification.
- NEEDS OWNER REQUIREMENT: continuity thresholds/pass-fail, scan-time target (if any), isolation spec, G6 multi-channel authorization.
- BLOCKED BY G1: firing-power/simultaneous timing/skew semantics (none of this report touches firing values). [HOLD]
- BLOCKED BY OTHER GATE: final pin map selection depends on G4 topology decision (this batch) + G6 OE wiring + owner approval.
- Nothing is force-closed. [CONSTRAINT respected]

## 14. Remaining blockers

1. CD4067 RON@3.3V + settling + real leakage -> measurement (T-G4-01/02/04/05). Blocking G4 closure and final topology. [HOLD/TBD]
2. VIH@5V conflict resolution (level-shift vs 3.3V path) -> depends on measurement result + owner. [OPEN]
3. Continuity pass/fail thresholds and scan-time requirement -> owner requirement. [OPEN]
4. G6 multi-channel authorization + OE interlock wiring -> owner evidence. [OPEN]
5. G1 load envelope -> master blocker (firing domain only). [HOLD]

## 15. Recommended next batch

1. Build G4 measurement fixture and run T-G4-01..06 (independent of G1). This closes RON@3.3V, settling, leakage, and ADC-vs-RAIN -> enables topology selection.
2. Owner: continuity threshold requirement + isolation spec (small, non-G1).
3. On G4 closure: pick topology (A vs B), then lock pin map candidate + SPI architecture with owner.
4. G6 owner evidence (multi-channel authorization, OE wiring) -> then G5 pin map can be finalized.
5. G9 firmware skeleton can proceed independently (state machine, SR driver, protocol parser) with config-driven constants.
6. Update OPEN_ISSUES.md / DECISIONS.md at each gate close.