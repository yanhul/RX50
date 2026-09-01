# RX50 G9 FIRMWARE ARCHITECTURE AND CROSS-GATE TIMING/RESOURCE MODEL

Status: DRAFT (batch phase 9 output)
Date: 2026-08-15
Input: RX50_BATCH_ENGINEERING_REPORT.md, RX50_FEASIBILITY_G3_G4_G5_G6_G8.md, G1 Evidence Register, G4 Evidence Retrieval
Scope: G9 firmware architecture for 50 channels + cross-gate consistency (G3/G4/G5/G6/G8/G9). G1/G2 remain HOLD. No schematic/PCB/BOM. No locked decision.

Label legend:
- [FACT]            Manufacturer / datasheet / explicit requirement evidence.
- [CALCULATION]     Arithmetic derived from inputs; valid only if inputs are valid.
- [ASSUMPTION]      Engineering assumption. NOT a requirement.
- [RECOMMENDATION]  Proposed direction; requires owner approval.
- Status: LOCKED / EVIDENCE-BACKED / HOLD / TBD / NEEDS RECHECK / OPEN / PROVISIONAL.

---

## 1. Executive Summary

- G9 firmware architecture for 50 channels is **structurally feasible** on the STM32F103C8T6, consistent with the G3/G4/G5/G6/G8 feasibility findings. All quantities here are structural/lower-bound because NO implementation code exists; nothing is claimed as a measured fact.
- Channel state is a **7-byte output shadow** (56 bits for 7x 74HC595, 6 spare bits forced OFF) plus a 50-entry continuity result set. [CALCULATION, ASSUMPTION 1:1 fan-out — NOT locked]
- Output update is **atomic by construction**: shift full frame, latch once (RCLK), with OE blanked by the hardware interlock path. This supports the RX50 simultaneous requirement at logic level; true firing simultaneity is G1/G2. [FACT/RECOMMENDATION]
- Output update latency is dominated by shift time (e.g., 56 bits at 9 MHz SPI = ~6.2 us) [CALCULATION]; this is OUTPUT-UPDATE latency, NOT simultaneous-fire timing — the latter is exclusively G1.
- Continuity scan scheduling is modeled symbolically. ADC conversion time is bounded by datasheet (tCONV 1-18 us); MUX settling is NOT guaranteed by the CD4067 datasheet -> **TBD/measurement**. [FACT -> TBD]
- Safety state machine proposed: BOOT -> SAFE -> ARM_REQUEST -> ARMED -> FIRE_AUTHORIZED -> FIRE_EXECUTION -> POST_FIRE, with FAULT sink. Timeout values are NOT invented; any timeout is G1/owner evidence. [RECOMMENDATION]
- No firmware value depends on a firing current/pulse/energy/voltage number. The G1 dependency audit (Section 9) lists exactly what firmware must NOT decide.
- No MAX_CONCURRENT_FIRE=1 anywhere. No schematic, PCB, BOM, or locked pin map.

## 2. G9 Architecture

### 2.1 Channel state representation
- 50 channels, IDs 0..49. [FACT — DECISIONS.md target]
- Proposed representation: per-channel state enum (OFF/ON/INHIBIT/FAULT) in a 50-byte table, PLUS a 7-byte output-shadow bitmask that is the ONLY source for the SR frame. [RECOMMENDATION]
- Rationale: a canonical shadow register decouples logical channel state from the physical shift frame, so the frame is always generated from one source of truth. [ASSUMPTION/RECOMMENDATION]

### 2.2 Output shadow register
- 7 bytes = 56 bits; bits 0..49 map to channels 0..49; bits 50..55 forced to 0 (OFF) always. [CALCULATION, ASSUMPTION 1:1 — NOT locked]
- Shadow updates are write-to-shadow-then-latch; no partial-frame latch. [RECOMMENDATION]

### 2.3 74HC595 shift/update mechanism
- Shift 56 bits on SER with SRCLK; assert RCLK once after last bit (tw >= 20 ns, tsu SRCLK↑->RCLK↑ >= 19 ns at 4.5 V). [FACT — TI SCLS041J]
- Shift clock may be GPIO bit-bang or SPI1 MOSI; see Section 7 for the SPI1-vs-SPI2 analysis. [RECOMMENDATION]
- Latch is atomic across all 7 devices because all RCLK are tied together. [FACT]

### 2.4 OE/blanking control
- OE high = outputs 3-state (blanked); OE low = enabled. [FACT]
- Firmware requests blanking; the HARDWARE interlock drives the OE line so a firmware fault cannot enable outputs. Firmware must never be the sole OE owner. [RECOMMENDATION]
- Blank around RCLK to prevent any glitch window. [RECOMMENDATION]

### 2.5 Continuity state storage
- Result per channel: pass/fail bitmask (7 bytes) plus optional per-channel raw ADC value (50 x 2 bytes if retained). [RECOMMENDATION]
- Storage choice affects RAM only (Section 7); no structural constraint. [CALCULATION]

### 2.6 Channel numbering 0..49
- One canonical map: protocol bitmask bit index = shadow bit index = SR frame bit position. Any deviation (e.g., reversed shift order) must be resolved at one defined mapping point. [RECOMMENDATION]
- This is a consistency requirement across G3 (frame), G8 (mask), G9 (firmware). [FACT-based consistency]

### 2.7 ARM / DISARM state
- Firmware keeps an arm state variable MIRRORING a hardware arm latch; the hardware interlock is authoritative. [RECOMMENDATION]
- DISARM must be able to be forced by hardware (power-loss, fault) independent of firmware. [RECOMMENDATION]

### 2.8 Fire-command state
- A pending fire command holds the validated channel mask + sequence + state. Only one pending fire command is accepted at a time (single-fire transaction), regardless of channel count. [RECOMMENDATION — not a concurrency limit on firing, a transaction model]
- NOT an RX24-style MAX_CONCURRENT_FIRE=1 constraint; this limits command transactions, not simultaneous channels. [CONSTRAINT respected]

### 2.9 Fault state
- Fault register per fault class (see Section 5.3 / G6); latched until cleared by a valid clear command after returning to a safe state. [RECOMMENDATION]

### 2.10 RF-loss state
- Link watchdog: if no valid link frame within an owner-defined window, transition toward SAFE. Window value = G1/owner, NOT invented. [RECOMMENDATION, OPEN]

### 2.11 Reset / power-loss behavior
- On any reset: outputs held blanked (OE high via hardware), shadow cleared, arm cleared, state = BOOT then SAFE. [RECOMMENDATION]
- Storage register undefined at power-up -> OE must be high before MCU runs. Hardware responsibility. [FACT]

### 2.12 Command acknowledgement
- ACK for accepted commands (sequence echoed). NAK for rejected commands with reason. [RECOMMENDATION]
- ACK itself is a normal protocol frame (Section 5). [RECOMMENDATION]

### 2.13 Duplicate / replay handling
- Monotonic sequence per link; reject sequence <= last accepted; freshness window = G1/owner. [RECOMMENDATION, OPEN]

### 2.14 Watchdog / error recovery
- IWDG feeds only from the main loop (not from interrupt-only), so a stuck loop trips reset -> safe state. [RECOMMENDATION]
- Error recovery = reset to BOOT/SAFE, not in-place recovery of a mid-fire state. [RECOMMENDATION]

## 3. Output timing (G3 x G9)

### 3.1 Symbolic model
- T_shift = N_bits / f_shift, where N_bits = 56 (7x 74HC595). [CALCULATION]
- T_update = T_shift + T_rclk + T_blank_overhead. T_rclk >= 20 ns pulse; tsu SRCLK->RCLK >= 19 ns. [FACT]
- Atomicity: shift frame while OE blanked; pulse RCLK; release OE. Partial-frame output impossible because storage register only updates on RCLK. [FACT]

### 3.2 Numbers only where evidence exists
- SPI1 max 18 Mbit/s (ST datasheet, APB2). [FACT]
- SX1278 SPI max 10 MHz (Semtech datasheet note). [FACT]
- Example (illustrative, NOT a decision): if the SR frame is shifted at 9 MHz, T_shift = 56 / 9e6 = 6.2 us. [CALCULATION under that assumption]
- At bit-bang 1 MHz: T_shift = 56 us. [CALCULATION under that assumption]
- These are OUTPUT-UPDATE latencies, NOT simultaneous-fire timing. G1 owns fire timing. [CONSTRAINT respected]

### 3.3 Latch / OE timing (SN74HC595, 4.5 V)
- tw SRCLK/RCLK >= 20 ns; tsu SRCLK↑ before RCLK↑ = 19 ns max; ten/tdis OE->Q = 37/50 ns max. [FACT]
- These impose no practical scheduling burden (nanoseconds vs microsecond shifts). [CALCULATION]

### 3.4 Update atomicity & interrupts
- If shifting is interrupt-driven or DMA-driven, the RCLK pulse must be generated only after the FULL frame completes (e.g., SPI TxComplete IRQ, not per-byte). [RECOMMENDATION]
- Disable the continuity-scan timer or any interrupt that could interleave mid-frame, OR make the frame copy atomic (copy shadow to a locked buffer before shifting). [RECOMMENDATION]
- Partial shift does not reach outputs until RCLK (FACT), so interrupt interleaving during SHIFT is tolerable; interleaving during RCLK is not. [FACT-based]

## 4. Continuity scheduling (G4 x G9)

### 4.1 Symbolic scan model
- scan cycle per measurement step = t_select + t_settle + t_acquire + t_convert + t_overhead. [CALCULATION-scope]
- Option A (4 MUX parallel, 4 ADC channels, shared address): 16 address steps per full scan of 64 positions (covers 50). [CALCULATION, ASSUMPTION]
- Option B (1 ADC, 4 enables): 50 sequential measurements per full scan. [CALCULATION, ASSUMPTION]
- Full scan time = N_steps x (cycle). N_steps = 16 (Option A) or 50 (Option B). [CALCULATION]

### 4.2 Evidence-based bounds
- ADC sampling time tS = 1.5..239.5 cycles (0.107..17.1 us @ fADC=14 MHz). [FACT — DS5319]
- ADC conversion tCONV = 14..252 cycles (1..18 us @ 14 MHz). [FACT — DS5319]
- ADC accuracy +/-2 LSB max ET guaranteed only when RAIN < 10 kOhm. [FACT — DS5319]
- CD4067 settling time: only typical curves, NO guaranteed value; charge injection NOT specified. [FACT — SCHS052D]

### 4.3 What stays TBD / measurement
- MUX analog settling time is NOT guaranteed -> the scan cycle's t_settle must be determined by hardware measurement (G4 fixture). Keep TBD until measured. [TBD]
- Do NOT reuse RX24 continuity timing (PROJECT_CONTEXT.md line 44). [FACT — rule]
- No ADC source-impedance value is asserted until the G4 fixture closes RON@3.3V / RAIN<10k. [TBD]

### 4.4 Scheduling overhead
- Software overhead per step (GPIO select, ADC start, ISR handling) is structural; bound it by a periodic scan task rather than tight back-to-back loops. [RECOMMENDATION]
- Continuity scan must yield to output update and safety paths (see Section 3.4). [RECOMMENDATION]

## 5. Communication / command timing (G8 x G9)

### 5.1 50-channel bitmask & command size
- Mask = 7 bytes. Example frame: cmd + seq + 7-byte mask + params + CRC ~= 12-15 bytes. [CALCULATION, ASSUMPTION]
- Both links fit this trivially: LoRa payload engine up to 256 bytes; RS485 up to 10 Mbps. [FACT]
- SX1278 SPI up to 10 MHz -> a 15-byte payload upload to FIFO is tens of microseconds. [CALCULATION]

### 5.2 RX processing time
- RX is interrupt-driven (DIO0 for LoRa, USART RXNE for RS485); parsing is bounded and fast (masked compares). Structural, no numeric assertion. [RECOMMENDATION/CALCULATION-scope]

### 5.3 RS485
- Half-duplex: DE/RE direction control; turnaround timing driven by MAX3485 enable/disable (up to ~120 ns enable, ~120 ns disable at 10 Mbps part). [FACT — MAX3485 datasheet]
- Not a scheduling constraint at typical baud rates. [CALCULATION-scope]

### 5.4 LoRa
- Airtime depends on SF/BW/CR/payload; no config is locked, so no airtime number is asserted. [TBD — config is G8/G9]
- FIFO 256 bytes; packet engine 256 bytes with CRC. [FACT]

### 5.5 ACK / timeout
- ACK frame carries echoed sequence; NAK carries reason code. [RECOMMENDATION]
- Timeout (for ack wait or link loss) is NOT defined here -> G1/owner. [OPEN]

### 5.6 Duplicate handling
- Sequence validation at parse time; reject stale/duplicate before any state change. [RECOMMENDATION]
- Freshness window value = G1/owner. [OPEN]

### 5.7 Constraint
- No timing tolerance for "simultaneous" is defined here. G1 owns: simultaneous event definition, channel count/event, allowable skew, load envelope. [CONSTRAINT respected]

## 6. Safety state machine (G6 x G9)

### 6.1 Proposed states (architecture level)
- BOOT: initialize, verify hardware interlock reports blanked; no outputs. -> SAFE.
- SAFE: outputs blanked; receives commands; ARM_REQUEST allowed.
- ARM_REQUEST: valid arm command + (owner-defined) authorization; on success -> ARMED.
- ARMED: may receive and validate fire commands; firing not yet authorized to execute.
- FIRE_AUTHORIZED: a validated fire command is accepted; pending single fire transaction armed.
- FIRE_EXECUTION: shift/latch/unblank sequence runs (Section 3); bounded.
- POST_FIRE: confirm completion, latch results, return to ARMED or SAFE per rules.
- FAULT: latched safe state; outputs blanked; requires valid clear sequence to leave.

### 6.2 Checks mapped to requirements
- reset -> SAFE (via BOOT): hardware OE high enforced. [FACT/RECOMMENDATION]
- watchdog -> SAFE/FAULT: IWDG trip resets to BOOT. [RECOMMENDATION]
- RF loss -> SAFE: link watchdog; window = G1/owner. [OPEN]
- invalid command -> no fire: CRC + mask validation before any state change. [RECOMMENDATION]
- partial packet -> no fire: frame-length and CRC check; no partial execution. [RECOMMENDATION]
- duplicate packet -> no unintended fire: sequence rejection. [RECOMMENDATION]
- stale command -> no unintended fire: freshness window = G1/owner. [OPEN]
- partial shift-register update -> outputs inhibited: OE blanked; storage register only updates on RCLK. [FACT]
- multi-channel authorization -> depends on G1 (channel count/event) + G6 rule (owner). [OPEN]

### 6.3 Timeouts
- NO timeout value is set in this report. Any timeout (arm validity, fire authorization expiry, RF-loss window, stale window) requires owner/G1 evidence. [CONSTRAINT respected]

## 7. MCU resource budget (G5 x G9)

No implementation code exists -> all sizes are LOWER-BOUND / STRUCTURAL estimates. Not measured facts. [CONSTRAINT respected]

| RESOURCE | ESTIMATED RX50 NEED (structural) | AVAILABLE | MARGIN | STATUS | BASIS |
|---|---|---|---|---|---|
| GPIO | ~27 digital + 6-7 ADC pins (proposal) | 37 | adequate | EVIDENCE-BACKED feasible | G5 proposal; DS5319 |
| ADC channels | 4 (continuity, Option A) + 1-2 (monitor) = 5-6 | 10 | moderate | feasible | DS5319; G4 |
| SPI | 1 (LoRa, SX1278 <= 10 MHz) + optional 1 (SR) | 2 | large | feasible | DS5319; SX1278 |
| UART | 1 (RS485) + 1 debug | 3 | large | feasible | DS5319 |
| Timers | 2-4 (scan scheduler, RCLK/blanking, link watchdog, timeout) | 4 | adequate | feasible | DS5319 |
| Interrupts | EXTI DIO0, USART RX, ADC EOC, fault, timer | EXTI0-15 + NVIC | large | feasible | DS5319 |
| RAM | shadow 7 B + channel table 50 B + continuity 7-100 B + buffers ~128-512 B + stack ~1-2 KB | 20 KB | large | feasible (estimate) | structural estimate |
| Flash | framework + LoRa driver + protocol + app; exact TBD | 64 KB | OK (footprint TBD) | NEEDS RECHECK (no code) | structural estimate |
| Stack | ~1-2 KB bare-metal typical (not asserted as measured) | part of 20 KB | large | ASSUMPTION | engineering norm, NOT fact |
| Channel state | 50 B table + 7 B mask | 20 KB | large | feasible | structural |
| Continuity buffer | 7 B result mask (or +100 B raw) | 20 KB | large | feasible | structural |
| Communication buffers | LoRa FIFO 256 B (in SX1278, not MCU) + RX/TX ~32-64 B each | 20 KB | large | feasible | SX1278 FACT; buffer sizes ASSUMPTION |
| Command buffers | 1-2 frames x 16-32 B | 20 KB | large | feasible | ASSUMPTION |
| Fault/event log | 0 if not required, or small ring (e.g., 64-256 B) | 20 KB | large | TBD (owner need) | structural |
| DMA | optional for SPI/USART/ADC | 7 ch | large | feasible | DS5319 |

Note: RAM/Flash figures are structural lower bounds; real sizes only after implementation. Do NOT cite them as measured. [CONSTRAINT respected]

## 8. Cross-gate conflicts

- G3 <-> G5: SR needs SER/SRCLK/RCLK + OE (4-5 GPIO). Proposal keeps these on non-ADC GPIO; no conflict. If SR used SPI1 MOSI instead, PA5-7 (ADC ch 5-7) are consumed -> NOT recommended unless ADC budget confirmed. [CALCULATION/RECOMMENDATION]
- G4 <-> G5: Option A needs 4 ADC channels (PA0-3 in proposal) + address/enable GPIO. Consistent. [CALCULATION]
- G6 <-> G5: OE via interlock (1 GPIO or none if pure HW) + fault input (1 GPIO). Consistent. [CALCULATION]
- G8 <-> G5: LoRa on SPI2 (PB13/14/15) + NSS/RST/DIO0; RS485 on USART1 (PA9/PA10) + DE. Consistent. [CALCULATION/RECOMMENDATION]
- G9 <-> all: firmware adds timer/IRQ/DMA/stack/buffer demand; budget above confirms margin. [CALCULATION]
- SPI1 vs SPI2 analysis: SX1278 needs <= 10 MHz; both SPI1 (APB2, up to 18 Mbit/s) and SPI2 (APB1, up to ~18 Mbit/s max clock; 36 MHz APB1) can supply <= 10 MHz. SPI2 keeps SPI1 pins (PA5-7) free for ADC. Recommendation: SPI2 for LoRa, SR bit-banged on non-ADC GPIO. NOT selected as locked decision; confirm at G5 closure. [RECOMMENDATION]
- No unresolvable conflict found under the current proposal. [CALCULATION]

## 9. G1 dependency audit

### 9.1 Firmware must NOT decide (owned by G1):
1. Simultaneous channel count / event definition. [OPEN]
2. Firing pulse width / profile. [OPEN]
3. Firing current magnitude. [OPEN]
4. Firing energy budget. [OPEN]
5. Firing voltage/rail. [OPEN]
6. Allowable channel-to-channel skew. [OPEN]
7. Firing-power timing (when outputs must assert relative to a reference). [OPEN]
8. Load envelope (load class, impedance, tolerance). [OPEN]
- Consequently, FIRE_EXECUTION asserts outputs per the shadow/latch mechanism WITHOUT adding timing semantics; any required skew/window is parameterized (configurable constant), not hard-coded as a requirement. [RECOMMENDATION]

### 9.2 Firmware that CAN be completed independently (not G1-dependent):
- Channel state + shadow + SR driver + latch/OE sequencing (logic-level atomic update). [RECOMMENDATION]
- Continuity scan framework (select/settle/acquire/convert), with t_settle as a configurable constant pending G4 measurement. [RECOMMENDATION]
- Protocol framing, mask parsing, sequence/ACK/NAK, CRC. [RECOMMENDATION]
- LoRa/RS485 drivers, watchdog, boot/safe state machine, fault framework (taxonomy from G6 owner). [RECOMMENDATION]
- Diagnostic/telemetry frames. [RECOMMENDATION]
- All G1-owned values live in a single configuration module (constants), replaceable when G1 closes. [RECOMMENDATION]

## 10. KEEP / MODIFY / TBD

- KEEP (baseline concepts): STM32F103C8T6; LoRa (SX1278) + RS485 (MAX3485); 74HC595 expansion; CD4067 continuity; HW interlock + MCU arm path; outputs default OFF.
- KEEP with reinforcement: OE-high blanking is the canonical output-inhibition mechanism (storage register undefined at power-up). [FACT]
- MODIFY (firmware design, not locked): shadow-register model (7 B) + 50-entry channel table; atomic shift-latch-unblank sequence; single pending fire transaction; config-driven G1 constants; scan scheduling task.
- TBD / OPEN: continuity t_settle (measure); RF-loss/stale/arm windows (G1/owner); multi-channel authorization rule (G6/owner); fault taxonomy (G6/owner); SR drive path (SPI vs GPIO) and final pin map (G5); LoRa SF/BW/CR config (G8/G9); Flash/RAM exact usage (implementation); event-log need (owner).

## 11. Blocking issues

1. G1 load envelope — master blocker for fire timing/skew/authorization semantics. [HOLD]
2. CD4067 RON@3.3V + settling — blocks G4 scan timing closure; requires G4 hardware fixture. [HOLD/TBD]
3. Multi-channel authorization rule — blocks G6 final safety design and FIRE_AUTHORIZED semantics. [OPEN]
4. RF-loss / stale / ack timeouts — need owner/G1 values. [OPEN]
5. Firmware Flash footprint — soft risk; verified only after implementation. [NEEDS RECHECK]

## 12. Recommended next batch

1. G4 hardware fixture (CD4067 RON@3.3V/5V, settling, RAIN<10k on STM32F103 ADC) -> closes continuity scan timing and topology (A/B). Independent of G1. [PRIORITY]
2. Owner: G1 envelope numbers -> unlocks fire timing/skew, G6 authorization, and timeouts. [PRIORITY]
3. G8 protocol draft (frame layout, mask, group/broadcast, sequence/ACK/NAK, replay) — framing capacity already feasible. [PRIORITY]
4. G5 final pin map + SR drive decision (SPI2 for LoRa; SR bit-bang vs SPI1) based on G4 topology and G6 OE wiring. [NEXT]
5. G9 implementation skeleton: shadow/SR driver, scan scheduler, protocol parser, safety state machine with config-driven G1 constants. [NEXT]
6. Update OPEN_ISSUES.md / DECISIONS.md at each gate close. [PROCESS]