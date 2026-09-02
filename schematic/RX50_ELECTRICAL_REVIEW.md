# RX50 Electrical Schematic Review Contract

Status: PRE-RELEASE / NOT VALIDATED / NOT FOR MANUFACTURING

## Sheet 1 — MCU / control / debug

Required review items:
- STM32F103C8T6 identity and package match repository evidence.
- Final GPIO map remains G5-controlled; current map is a proposal only.
- SWD ownership is separated from safety/output control.
- Reset/default-state behavior must be reviewed before release.

## Sheet 2 — LoRa / RS485

Required review items:
- SX1278/RA-02 interface mapping.
- MAX3485 UART/DE mapping.
- Power and logic-voltage compatibility must be backed by evidence before release.
- No unsupported communication-rate claim is permitted.

## Sheet 3 — output logic

The logical architecture preserves 50 channels using cascaded shift-register storage. Spare register bits must have a deterministic safe state. Hardware OE blanking remains outside MCU sole control.

The actual energized load-switch/firing stage is intentionally excluded while G1/G2 remain HOLD. This prevents the review artifact from becoming an unsupported operational firing design.

## Sheet 4 — continuity

Four independent CD4067 candidate paths are retained. Shared address control is structurally defined. Sense-node conditioning and ADC source impedance remain evidence-gated. CD4067 RON/settling behavior at the selected operating condition must be measured or explicitly supported by manufacturer evidence before validation.

## Sheet 5 — safety interlock

Required invariants:
- Default output state is disabled/blanked.
- Firmware request cannot by itself establish the enabled state.
- Fault/interlock loss forces the safe output condition.
- Authorization ownership and recovery behavior require G6 approval/evidence.

## Sheet 6 — power boundary

Logic power can be represented as an interface boundary. Firing-power generation, storage, switching, protection ratings, transient design, and current-path sizing remain G1/G2 HOLD and are not dimensioned here.

## Sheet 7 — connectors/channel interface

Channel grouping and connector pinout remain TBD until G1/G2/G5 requirements are authoritative. Do not infer connector ratings or channel wiring from RX24.

## ERC/review exit criteria

1. Every net has an intentional source/sink or documented external boundary.
2. No floating safety-control input is accepted without an explicit evidence-backed termination decision.
3. No unresolved power-domain conflict is hidden by a schematic label.
4. All provisional GPIO assignments are marked provisional until G5 closure.
5. G1/G2 HOLD prevents production release regardless of schematic/ERC cleanliness.
