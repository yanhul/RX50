# RX50 OPEN ISSUES

## High priority

### 1. Simultaneous-channel load envelope
Status: HOLD / TBD

Need an explicit requirement defining the number of channels that may fire simultaneously and the validated load envelope.

Do not invent current, pulse width, energy, or voltage requirements.

### 2. Firing-power subsystem
Status: FEASIBILITY HOLD

Must be re-evaluated for the RX50 simultaneous-channel requirement.

Questions include:
- source capability,
- rail architecture,
- transient behavior,
- protection,
- distribution,
- thermal constraints,
- PCB current paths,
- fault isolation.

Numerical values must come from requirements, measurements, or datasheets.

### 3. Output expansion
Status: NEEDS RECHECK

Determine the required number of 74HC595 devices or alternative architecture, cascade timing, OE behavior, reset state, and simultaneous output update behavior.

### 4. Continuity subsystem
Status: NEEDS RECHECK

50-channel scaling affects:
- MUX topology,
- leakage,
- ADC loading,
- settling,
- scan time,
- channel isolation,
- firmware scheduling.

### 5. MCU resources
Status: NEEDS RECHECK

Recalculate GPIO, timers, SPI, ADC, RAM, flash, interrupt, and communication requirements for 50 channels.

### 6. Communications
Status: NEEDS RECHECK

Verify that the existing LoRa/RS485 protocol and packet/state representation can safely address and command 50 channels.

### 7. PCB and connectors
Status: TBD

50-channel mechanical arrangement, connector count, grouping, copper strategy, return paths, and physical segregation need to be defined.

### 8. Safety
Status: NEEDS RECHECK

The RX24 hardware interlock concept is a baseline, but multi-channel operation requires a fresh review of:
- reset behavior,
- unintended activation,
- partial command reception,
- communication loss,
- firmware fault,
- power fault,
- output-enable behavior,
- simultaneous activation authorization.

## Rule

No issue above should be silently resolved by guessing.
