# RX50 G2 — Driver Architecture Mission

Status: IN_PROGRESS / NON-OPERATIONAL DESIGN CONTRACT

## Goal
Advance RX50 from the locked common-market e-match requirement toward an implementation-ready driver architecture without inventing or authorizing ignition operating parameters.

## Governing policy
`AGENTS.md` remains authoritative. No numerical firing specification may be introduced without traceable evidence and approval.

## Closed-loop
`OBSERVE -> DECIDE -> ACT -> VERIFY -> PERSIST -> RESUME`

## Work packages

1. **Load-class interface**
   - Represent the supported load as an abstract electrical interface.
   - Track every required parameter as `REQUIRED`, `EVIDENCE_PENDING`, `APPROVED`, or `QUALIFIED`.
   - Keep manufacturer/model evidence separate from derived calculations.

2. **Channel architecture**
   - 50 independently addressable output channels.
   - Hardware inhibit/interlock remains upstream of channel actuation.
   - Define fault-containment and diagnostic boundaries.
   - Do not specify ignition voltage/current/energy/pulse values here.

3. **Control architecture**
   - MCU command -> authorization/interlock -> channel selection -> driver interface.
   - Firmware must fail safe when authorization is absent.
   - Driver interface must expose explicit disabled/inhibited state.

4. **Continuity/diagnostic architecture**
   - Keep continuity sensing electrically and logically distinct from the actuation path.
   - Record uncertainty and source impedance constraints as evidence items rather than guessed values.

5. **Parameter boundary**
   The following remain placeholders until authoritative evidence and engineering approval exist:
   - ignition voltage
   - ignition current
   - no-fire/all-fire limits
   - delivered energy
   - pulse duration/waveform
   - driver power/current capacity
   - simultaneous-load operating envelope

6. **Verification**
   Required checks:
   - no unverified numerical claim in design artifacts
   - no unqualified load promoted to supported
   - inhibit path cannot be bypassed by normal control flow
   - continuity path cannot silently become an actuation path
   - every numerical design input has provenance

## Terminal states

- `G2-HOLD`: required evidence or approval missing.
- `G2-READY-FOR-ENGINEERING-REVIEW`: architecture complete; unresolved operating parameters explicitly registered.
- `G2-QUALIFIED`: only after authoritative evidence, review, measurements/tests where required, and explicit approval.

The autonomous agent cannot move the project into `G2-QUALIFIED` by itself.
