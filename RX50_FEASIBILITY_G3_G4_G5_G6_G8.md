# RX50 FEASIBILITY — G3 / G4 / G5 / G6 / G8

Status: DRAFT (batch phase 7 output)
Date: 2026-08-15
Input: RX50_BATCH_ENGINEERING_REPORT.md + PROJECT_CONTEXT.md / DECISIONS.md / OPEN_ISSUES.md
Scope: feasibility for G3, G4 (architecture level), G5, G6, G8. G1/G2 remain HOLD. No schematic, PCB, BOM, no locked decision.

Label legend:
- [FACT]            Manufacturer / datasheet / explicit requirement evidence.
- [CALCULATION]     Arithmetic from inputs above.
- [ASSUMPTION]      Engineering assumption. NOT a requirement.
- [RECOMMENDATION]  Proposed direction; requires owner approval.
- Status: LOCKED / EVIDENCE-BACKED / HOLD / TBD / NEEDS RECHECK / OPEN / PROVISIONAL.

---

## 1. Executive summary

- G3 (output expansion): **feasible at logic level**. 7x SN74HC595 (56 bits) covers 50 channels under the 1:1 fan-out assumption — labeled CALCULATION, NOT locked. The 74HC595 storage-register architecture inherently gives simultaneous multi-bit update (one RCLK edge updates all chips). SR control needs only 4-5 shared GPIO, independent of channel count.
- G4 (continuity): **feasibility plausible, not closed**. CD4067 RON @3.3 V is NOT specified by TI; the blocking item is a hardware measurement of RON + settling. ADC accuracy (RAIN <10 kΩ) is respected only if divider + MUX RON stay under ~10 kΩ. No part selection, no divider values, no schematic.
- G5 (MCU): STM32F103C8T6 **appears sufficient** for RX50 under the same 1:1 assumption. Tightest resource is ADC (10 channels on LQFP48; ~6-7 needed). Proposed pin map avoids conflicts (SPI2 for LoRa keeps SPI1/ADC pins free). MCU change is NOT proposed; if ADC ever runs out, topology alternatives exist.
- G6 (safety): RX24 concept (dedicated logic + MCU arm path + outputs default OFF) is **retained as baseline**, but multi-channel authorization, RF-loss window, and stale/duplicate handling are **OPEN/HOLD** — they need owner evidence. A safety-critical FACT: SN74HC595 storage register is NOT cleared by SRCLR and is undefined at power-up, so OE-high blanking is mandatory.
- G8 (protocol): 50-channel representation is **feasible**: a 7-byte bitmask covers channels 0..49 (plus group/broadcast). LoRa payload and RS485 capacity are sufficient. Simultaneous-fire timing semantics are NOT defined here (G1 owns timing).
- No gate is LOCKED. No MAX_CONCURRENT_FIRE=1 is used. No firing current/pulse/energy/timing is invented (G1/G2 HOLD respected).

## 2. G3 result — Output expansion

### 2.1 Register count
- 50 channels / 8 per register = 7 registers (ceil(50/8)=7), 56 bits total, 6 spare. [CALCULATION, ASSUMPTION 1:1 fan-out — NOT locked]
- Spare 6 bits must be held at a defined safe state (0 = OFF) by firmware, or reserved for expansion. [RECOMMENDATION]

### 2.2 Cascade timing (SN74HC595, TI SCLS041J, Rev J, Oct 2021)
Facts (VCC = 4.5 V, SN74HC595 column):
- tsu SER before SRCLK↑ = 25 ns max. [FACT]
- tpd SRCLK -> QH' = 40 ns max (cascade propagation). [FACT]
- tsu SRCLK↑ before RCLK↑ = 19 ns max (data stable into storage register). [FACT]
- tw SRCLK/RCLK high or low = 20 ns min. [FACT]
- fmax/fclock = 25 MHz max (single device). [FACT]
- th SER after SRCLK↑ = 0 ns. [FACT]

Cascade worst-case SRCLK period: tpd(SRCLK->QH') + tsu(SER) = 40 + 25 = 65 ns -> ~15.4 MHz max at 4.5 V. [CALCULATION]
- At 3.3 V the datasheet does not tabulate timing (only 2 / 4.5 / 6 V columns) -> exact 3.3 V values need interpolation or measurement. [FACT -> TBD]
- Practical shift clock is far below this (bit-bang ~1 MHz is ample), so cascade timing is NOT a feasibility constraint. [CALCULATION/ASSUMPTION]
- RCLK must be asserted >= 19 ns after the last SRCLK edge and held >= 20 ns. [FACT]

### 2.3 SRCLK / RCLK / LATCH behavior
- SRCLK and RCLK are both positive-edge triggered, with separate clocks. [FACT]
- Shifting changes ONLY the shift register; outputs change ONLY on an RCLK edge (data moves to the D-type storage register). [FACT]
- => One RCLK pulse updates all 7 chips' outputs simultaneously. This is a favorable FACT for the RX50 simultaneous requirement at logic level. (True firing simultaneity is G1/G2.) [FACT + note]

### 2.4 OE / blanking
- OE = high -> QA..QH high-impedance (3-state); OE = low -> outputs enabled. [FACT]
- ten (OE -> QA-QH) = 37 ns max; tdis = 50 ns max (4.5 V). [FACT]
- [RECOMMENDATION] OE is the hardware blanking line. It must be driven by the safety/interlock path (not directly by MCU GPIO) so that a firmware fault cannot enable outputs.

### 2.5 Reset / power-up state (SAFETY-RELEVANT FACT)
- SRCLR clears the SHIFT register only. The STORAGE register is NOT affected by SRCLR. [FACT]
- Power-up state of the storage register is UNDEFINED (no power-on reset on this device). [FACT]
- => Outputs cannot be assumed OFF at power-up; OE must be pulled to the blanking level (high) until valid data has been shifted and latched. [RECOMMENDATION]

### 2.6 Glitch / partial-update behavior
- A partial shift (mid-frame) does not reach outputs until RCLK is pulsed. [FACT]
- To prevent latching a partial frame: pulse RCLK only after all 56 bits are shifted, and/or blank OE around the RCLK edge. [RECOMMENDATION]

### 2.7 Simultaneous update
- Achieved by the storage-register latch structure: shift full frame, assert RCLK once, release OE. [FACT/RECOMMENDATION]

### 2.8 Interaction with hardware safety / interlock
- G3 and G6 agree: OE high = safe (outputs disabled); OE must default high on power-up/power-loss and be gated by the interlock. No conflict. [RECOMMENDATION]
- The interlock must also be able to force blanking independent of the MCU (dedicated logic path). [RECOMMENDATION]

### 2.9 G3 verdict
- Logic-level feasibility: YES. Control GPIO = SER + SRCLK + RCLK + OE (+ optional SRCLR) = 4-5 GPIO shared by all registers. [CALCULATION]
- Not locked: register count, exact OE/blanking wiring, and any SRCLR usage remain G3 design items.

## 3. G4 result — Continuity follow-up (feasibility only)

### 3.1 CD4067 RON @ 3.3 V — the blocking issue
- TI CD4067B (SCHS052D Rev D) does NOT specify RON at VDD-VSS = 3.3 V. RON max is given only at 5 / 10 / 15 V (1050 / 400 / 240 Ω at 25 °C). [FACT]
- VIH at 5 V = 3.5 V, so 3.3 V logic cannot drive a 5 V-powered CD4067 to guaranteed VIH without a level shifter. [FACT]
- RON tends to increase as VDD decreases -> at 3.3 V RON is expected higher than the 5 V value, but the exact value is NOT specified. [ASSUMPTION — must be measured]

### 3.2 RAIN 50 kΩ vs RAIN <10 kΩ (STM32F103, DS5319 Rev 20)
- RAIN max 50 kΩ is the maximum source impedance that still samples correctly at the maximum sample time (tS = 55.5 cycles, fADC = 14 MHz). [FACT]
- RAIN <10 kΩ is the condition under which the ±2 LSB max total error is GUARANTEED by the datasheet. [FACT]
- These are different conditions. For continuity thresholds that need guaranteed accuracy, total source impedance (divider Thévenin + MUX RON + traces) must be <10 kΩ. [CALCULATION]
- With CD4067 RON max 1050 Ω at 5 V, the divider can be sized so Rth + RON < ~10 kΩ. Feasible in principle. At 3.3 V, RON unknown -> measurement required. [CALCULATION/FACT]

### 3.3 Topology alternatives (evaluated, NOT selected)
- A) CD4067 at 5 V + level-shifted address/control: RON known (1050 Ω max) but adds level-shifter components and a VIH-rule violation to solve. [ASSUMPTION evaluation]
- B) CD4067 at 3.3 V: no level shift, but RON not specified -> must be measured; expected higher than 5 V value. [ASSUMPTION evaluation]
- C) Two-stage MUX (16:1 then 4:1): doubles RON in series -> worse impedance budget. Not preferred. [ASSUMPTION evaluation]
- D) Alternative analog-MUX family with RON specified at 3.3 V: plausible class of options, but the instruction is to NOT select a replacement part in this batch. Marked OPEN for G4 owner decision. [OPEN]
- E) Longer ADC sampling time (tS up to 239.5 cycles = 17.1 µs) to tolerate higher RAIN: supported by datasheet, but does NOT restore guaranteed ±2 LSB accuracy above 10 kΩ. [FACT]
- No divider values, no part selection, no schematic produced. [CONSTRAINT respected]

### 3.4 ADC / topology resource impact (G4 <-> G5)
- Option A (4 MUX fully parallel, 4 sense outputs -> 4 ADC channels): 16 address steps per scan, 4 ADC channels, enable can be common (1 GPIO). [CALCULATION/ASSUMPTION]
- Option B (shared sense node, 4 independent enables): 1 ADC channel, 50 sequential reads, 8 GPIO (4 addr + 4 en). [CALCULATION/ASSUMPTION]
- Both fit the STM32F103C8 ADC budget (10 channels). No conflict. [CALCULATION]

### 3.5 G4 verdict
- Feasibility: PLAUSIBLE, NOT closed. Blocking item = CD4067 RON @3.3 V and settling time measurement (hardware fixture), plus choice of topology (OPEN). ADC accuracy rule (RAIN <10 kΩ) drives divider/MUX sizing.

## 4. G5 result — MCU resource / pin budget (STM32F103C8T6)

### 4.1 Device facts (ST DS5319 Rev 20 + ST/ST-approved summaries)
- LQFP48, 37 GPIO (PA0-15, PB0-15, PC13-15, PD0-1). [FACT]
- 64 KB Flash, 20 KB SRAM. [FACT]
- 2x 12-bit ADC, up to 10 external channels on this package (PA0-7, PB0, PB1). [FACT]
- 3 USART, 2 SPI, 2 I2C, USB, CAN. [FACT]
- 3 general-purpose timers + 1 advanced timer. [FACT]
- 7-channel DMA. [FACT]
- SWD/JTAG debug. [FACT]
- VREF+ internally tied to VDDA on LQFP48. [FACT]

### 4.2 Resource budget

| RESOURCE | RX24 (baseline) | RX50 requirement | Available | Margin | Status | Evidence |
|---|---|---|---|---|---|---|
| GPIO (SR chain) | 3-4 (3x595) | 4-5 (SER/SRCLK/RCLK/OE/SRCLR) shared | 37 | large | EVIDENCE-BACKED feasible | TI SCLS041J; CALC |
| GPIO (continuity) | ~6 (2x CD4067) | 5-8 (4 addr + 0-4 en) | 37 | large | feasible (open topology) | CALC |
| GPIO (LoRa ctrl) | NSS+RST+DIO0 = 3 | 3 (+3 SPI pins) | 37 | large | feasible | CALC |
| GPIO (RS485) | TX/RX/DE = 2-3 | same (USART + 1 DE) | 37 | large | feasible | CALC |
| GPIO (safety) | arm + fault | arm + fault input | 37 | large | concept only (OPEN rules) | context |
| ADC channels | 2-4 | ~5-7 (4 continuity + monitor) | 10 | moderate | feasible; tightest resource | DS5319 |
| SPI | 1 (LoRa) | 1 (LoRa) | 2 | large | feasible | DS5319 |
| USART | 1-2 | 1 (RS485) + 1 debug | 3 | large | feasible | DS5319 |
| Timers | 2-3 | 2-4 (scan timing, blanking/RCLK, watchdog) | 4 | adequate | feasible | DS5319 |
| Interrupts | EXTI DIO0, USART, ADC, fault | same set | EXTI0-15 | large | feasible | DS5319 |
| RAM | ~24 B state | 50 B state + LoRa FIFO 256 B + buffers | 20 KB | large | feasible | DS5319 |
| Flash | firmware ~TBD | firmware + LoRa lib + protocol | 64 KB | OK (footprint TBD) | NEEDS RECHECK (G9) | DS5319 |
| DMA | - | optional for USART/ADC | 7 ch | large | feasible | DS5319 |

### 4.3 Pin-conflict analysis (KEY finding)
- ADC channels are ONLY PA0-7, PB0, PB1 (10). PA5/6/7 also carry SPI1 (SCK/MISO/MOSI). If LoRa uses SPI1, those ADC channels are consumed. [FACT -> CALCULATION]
- [RECOMMENDATION] Use SPI2 (PB13/14/15) for LoRa + NSS PB12 + RST PB11 + DIO0 PB10. Then SPI1 pins stay free and PA0-4 + PB0-1 remain usable as ADC (7 channels). RS485 on USART1 (PA9 TX, PA10 RX) + DE on PA8 keeps PA2/PA3 free for ADC.
- Proposed allocation (PROPOSAL only, NOT locked): [ASSUMPTION/PROPOSAL]
  - LoRa: SPI2 PB13/14/15, NSS PB12, RST PB11, DIO0 PB10 (EXTI).
  - RS485: USART1 PA9/PA10, DE PA8.
  - Continuity Option A: ADC PA0-PA3 (4 sense), addr PB4-PB7, common enable PB8.
  - SR chain: SER/SRCLK/RCLK on PB3/PB6/PB7 (or non-ADC GPIO), OE via interlock.
  - Monitoring: PA4 (battery), PB0 or PB1 (rail). LEDs PC13/PC14.
  - Debug: PA13/PA14 (SWD). Keep BOOT0 strapped.
- Usable GPIO realistically ~33-35 (37 minus SWD minus HSE pins if used); needed ~27. Margin adequate. [CALCULATION/ASSUMPTION]

### 4.4 G5 verdict
- STM32F103C8T6 appears SUFFICIENT for RX50 under the 1:1 assumption. No MCU change proposed. [RECOMMENDATION]
- If ADC capacity ever becomes insufficient, mitigation without MCU change: continuity Option B (1 ADC), drop non-essential monitoring channels, or share address/enable lines. [RECOMMENDATION]
- Exact pin map is a G5 deliverable to be finalized with owner; not locked here. [TBD]

## 5. G6 result — Safety / interlock review

### 5.1 Retained RX24 baseline (PROVISIONAL)
- Dedicated hardware interlock logic + MCU-controlled arm path. [context]
- Outputs default OFF on reset / power loss / firmware fault / RF loss. [context]
- ARM/DISARM concept. [context]
- 74HC595 OE high = outputs disabled. [FACT — reinforces baseline]

### 5.2 Findings specific to 24 -> 50 and concurrent=1 removal
- Storage register undefined at power-up; SRCLR does not clear it -> OE-high blanking mandatory; cannot rely on any device power-on state. [FACT -> RECOMMENDATION]
- OE must be interlock-gated, not MCU-direct, so a firmware fault cannot enable outputs. [RECOMMENDATION]
- Partial shift-register update is contained by the storage latch (no output change until RCLK); combine with OE blanking around RCLK for defense in depth. [FACT/RECOMMENDATION]
- Multi-channel firing authorization: the old concurrent=1 single-channel gate is GONE. RX50 needs an explicit authorization rule for multi-channel commands. No owner evidence exists -> OPEN/HOLD. [OPEN]
- Distinction single-channel vs multi-channel authorization: may be appropriate, but it is a SAFETY DECISION requiring owner evidence -> OPEN. [OPEN]

### 5.3 OPEN / HOLD safety items (owner evidence required)
1. RF-loss auto-disarm timeout. [OPEN — timing = G1/owner]
2. Simultaneous-fire authorization rule (who/what/confirmation required before a multi-channel command is executed). [OPEN — G1 + owner]
3. Stale/duplicate command freshness window. [OPEN — G1 + owner]
4. Fault taxonomy and per-fault action (which faults blank, which disarm, which latch). [OPEN]
5. Whether single-channel vs multi-channel need different authorization levels. [OPEN]
- None of these are silently resolved. [CONSTRAINT respected]

### 5.4 G6 verdict
- Concept retained and reinforced by G3 facts (OE blanking). Feasibility of the HARDWARE mechanism: YES. The safety RULES for multi-channel are OPEN/HOLD and block final safety design until owner evidence.

## 6. G8 result — Communication / protocol check

### 6.1 Channel addressing (0..49)
- 50 channels fit in 6 bits (0-63). [CALCULATION]
- A 50-channel arbitrary subset fits in a 7-byte bitmask (ceil(50/8)=7). [CALCULATION]
- Group codes (predefined subsets) and broadcast (all channels) are representable on top of the bitmask or via address types. [RECOMMENDATION]

### 6.2 Packet sizing
- Example command: cmd byte + sequence byte + 7-byte channel mask + parameters + CRC ≈ 12-15 bytes. [CALCULATION/ASSUMPTION]
- SX1278 LoRa: packet engine up to 256 bytes with CRC; 256-byte FIFO. [FACT] (Payload-length register is 8-bit, so practical max 255; exact ceiling vs 256 to be pinned to the SX1278 datasheet page — NEEDS RECHECK.) [FACT -> NEEDS RECHECK]
- RS485 MAX3485: half-duplex, up to 10 Mbps, DE/RE control; up to 32 transceivers on bus (unit-load limited). [FACT]
- Both links easily carry a 15-byte command frame. [CALCULATION]

### 6.3 Group / broadcast
- Broadcast = mask all-ones or dedicated broadcast address. Group = table-mapped mask expansion. Both feasible within the frame budget. [RECOMMENDATION]

### 6.4 Simultaneous-fire command semantics
- The protocol can represent an arbitrary set of channels to fire together (bitmask). [CALCULATION]
- Timing semantics (how "simultaneous" is defined/guaranteed end-to-end) are NOT set here — G1 is the source of timing requirements. [CONSTRAINT respected]
- The command must carry its own sequence/freshness info so safety (G6) can validate it. [RECOMMENDATION]

### 6.5 Sequence / acknowledgement
- RX24 sequence/ack scheme is not documented in the context files -> NEEDS RECHECK. [FACT]
- [RECOMMENDATION] Explicit monotonic sequence + acceptance ack for fire commands; required by G6 authorization.

### 6.6 Duplicate / replay handling
- Relevant over LoRa (shared medium). [ASSUMPTION]
- [RECOMMENDATION] Sequence validation + freshness window (window value = G1/owner). Duplicate/replay rejection to be part of the command state machine (G9).

### 6.7 LoRa time/throughput constraints
- LoRa airtime depends on SF / BW / CR / payload; for a ~15-byte frame at typical settings it is tens of ms. Exact values are NOT asserted here (config is a G8/G9 choice; timing semantics are G1). [CALCULATION-scope note; no invented numbers]
- RS485 latency is negligible relative to LoRa for a 15-byte frame at 10 Mbps or even 1 Mbps. [CALCULATION]

### 6.8 G8 verdict
- Representation and capacity for 50 channels: FEASIBLE (7-byte mask; LoRa/RS485 frames well within limits).
- Protocol semantics for simultaneous fire, sequence/ack, and replay are design items owned by G8+G6+G1; framing capacity is not a blocker.

## 7. Cross-gate conflicts

1. 50 outputs have enough resource? YES at logic level (7x595 = 56 bits; 4-5 GPIO). Real firing current/power is G1/G2, out of scope. [CALCULATION]
2. Continuity has enough ADC/resource? YES. ~5-7 of 10 ADC channels; both Option A (4 ADC) and Option B (1 ADC) fit. [CALCULATION]
3. G3 conflict with G6? NO — they agree on OE-high blanking and interlock-gated OE. The storage-register power-up fact strengthens the G6 default-OFF requirement. [FACT]
4. Protocol represents 50 channels? YES — 7-byte mask + group/broadcast. [CALCULATION]
5. Simultaneous command conflicts with safety? YES — OPEN ITEM: no multi-channel authorization rule exists (G1 + owner). Protocol capacity is ready; safety rule is not. [OPEN]
6. MCU pin allocation conflicts (LoRa/RS485/ADC/output/safety)? RESOLVABLE. The real conflict is SPI1 (PA5-7) vs ADC channels; mitigation = SPI2 for LoRa (proposal). No unresolvable conflict under the proposal. [RECOMMENDATION/CALCULATION]
7. Any assumption silently becoming a requirement? NO — 7 registers and 4 MUX remain labeled CALCULATION/ASSUMPTION (1:1 fan-out), not locked. [CONSTRAINT respected]
8. MAX_CONCURRENT_FIRE=1 used anywhere? NO — explicitly rejected (DECISIONS.md). [CONSTRAINT respected]
9. Old firing current/pulse/energy used? NO — G1/G2 HOLD; no firing numbers invented. [CONSTRAINT respected]

## 8. KEEP / MODIFY / TBD

- KEEP (baseline concept): 74HC595 output expansion; CD4067 continuity concept; STM32F103C8T6; dedicated hardware interlock + MCU arm path; outputs default OFF; LoRa + RS485 architecture; 3.3 V logic rail.
- KEEP with reinforcement: OE-high blanking as the hardware safety mechanism (now FACT-backed: storage register undefined at power-up).
- MODIFY (design items, not locked): SR register count (3 -> 7 under 1:1); continuity MUX count (2 -> 4 under 1:1); pin map proposal (SPI2 for LoRa, USART1 for RS485); scan topology A or B.
- TBD / OPEN: CD4067 RON@3.3 V measurement; continuity topology choice; multi-channel authorization rule; RF-loss window; stale/duplicate window; fault taxonomy; exact pin map; SX1278 payload ceiling page reference; LoRa SF/BW/CR config; Flash footprint (G9).

## 9. Blocking issues

1. G1 load envelope (unchanged master blocker) — gates firing power, timing semantics, and multi-channel authorization. [HOLD]
2. CD4067 RON @3.3 V + settling not specified — blocks G4 closure; requires hardware measurement fixture. [HOLD/TBD]
3. Multi-channel authorization rule missing — blocks G6 finalization. [OPEN]
4. LoRa/RS485 sequence-ack & replay semantics not defined — blocks G8/G9 protocol closure. [OPEN/NEEDS RECHECK]
5. Flash footprint unverified (G9) — only soft risk; no MCU change proposed yet. [NEEDS RECHECK]

## 10. Evidence gaps

- CD4067 RON vs VDD at 3.3 V and settling time (no datasheet guarantee) -> measurement.
- SN74HC595 timing at 3.3 V (datasheet tabs 2/4.5/6 V only) -> interpolation or measurement (low risk; not a bottleneck).
- SX1278 exact max payload ceiling (255 vs 256) -> pin to datasheet section/page.
- RX24 sequence/ack and RF-loss timeout -> NEEDS RECHECK from historical record; not in context files.
- STM32F103 Flash usage for the full RX50 firmware -> G9 estimate.
- Confirm ST F103 GPIO count on LQFP48 = 37 (multiple ST/ST-licensed sources agree) and 10 external ADC channels (DS5319).

## 11. Recommended next gates

1. G4 hardware fixture: measure CD4067 RON at 3.3 V and 5 V, settling, and verify RAIN <10 kΩ rule on the STM32F103 ADC -> closes G4 feasibility and picks topology (A or B). (Independent of G1.)
2. Owner evidence for G6 multi-channel authorization + RF-loss/stale windows (depends on G1 timing semantics).
3. G8 protocol draft (frame layout, bitmask, group/broadcast, sequence/ack, replay) — can proceed on capacity facts now; timing semantics inserted when G1 closes.
4. G5 final pin map based on chosen continuity topology and G6 OE/interlock wiring.
5. G9 firmware resource estimate (Flash/RAM/interrupts) to confirm G5 margins.
6. Revisit G1 (load envelope) as soon as owner can supply numbers — it remains the master gate for firing power, PCB, thermal, and safety authorization.