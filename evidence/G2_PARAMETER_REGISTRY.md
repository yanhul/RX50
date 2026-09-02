# RX50 G2 Parameter Registry

Purpose: single traceability surface for parameters required by the driver architecture.

## Rule
A blank/TBD field is a deliberate state. It must not be replaced by inference, a generic internet value, a legacy RX24 value, or an AI recommendation.

| Parameter | Required for | Status | Evidence | Approval | Notes |
|---|---|---|---|---|---|
| Load family/model identity | compatibility | EVIDENCE_PENDING | TBD | TBD | CN common-market class is the scope; individual models require qualification |
| Manufacturer electrical envelope | compatibility | EVIDENCE_PENDING | TBD | TBD | authoritative manufacturer evidence required |
| Ignition operating voltage | driver design | HOLD | TBD | TBD | no value may be inferred |
| Ignition operating current | driver design | HOLD | TBD | TBD | no value may be inferred |
| No-fire / all-fire limits | safety boundary | HOLD | TBD | TBD | authoritative evidence required |
| Delivered ignition energy | driver design | HOLD | TBD | TBD | no value may be inferred |
| Pulse duration / waveform | driver design | HOLD | TBD | TBD | no value may be inferred |
| Simultaneous-load envelope | system design | HOLD | TBD | TBD | explicit RX50 requirement/evidence required |
| Continuity-test envelope | diagnostics | EVIDENCE_PENDING | TBD | TBD | keep separate from actuation path |
| Temperature/environment envelope | qualification | EVIDENCE_PENDING | TBD | TBD | source required |

## State machine

`UNREGISTERED -> EVIDENCE_PENDING -> EVIDENCE_REVIEW -> APPROVED -> QUALIFIED`

Any contradiction sends the parameter to `CONTRADICTION/HOLD` until resolved.

## Calculation rule
Derived values may only be generated from parameters whose source and approval state are recorded. A derived value is never evidence by itself.
