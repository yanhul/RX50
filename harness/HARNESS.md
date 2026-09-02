# RX50 Durable Engineering Harness

## Control loop

`GOAL -> OBSERVE -> DECIDE -> ACT -> VERIFY -> PERSIST -> RESUME`

This harness governs engineering work. An agent may analyze and propose changes, but it cannot redefine RX50 requirements, evidence hierarchy, safety gates, approval gates, or terminal conditions.

## Fixed invariants

- `AGENTS.md` remains the governing policy.
- Evidence hierarchy and contradiction handling are immutable to the agent.
- No unsourced numerical/design claim becomes authoritative state.
- Safety-critical design edits require explicit approval before commit.
- Every action records what changed and the evidence used to justify it.
- Verification must inspect the resulting repository/artifact state; a successful command alone is not proof of design validity.
- A contradiction or missing required evidence produces `HOLD`, not a guessed resolution.
- Autonomous iterations are bounded. Repeated failure does not authorize speculative changes.
- Terminal states are explicit: `DONE`, `HOLD`, or `BLOCKED`.

## Durable checkpoint

Persist at least:

- mission/task ID
- phase
- iteration
- retry count
- current artifact/decision under review
- last action
- verification result
- evidence references
- contradiction status
- approval status
- last commit
- last CI run/conclusion
- terminal state/reason
- timestamp

## Resume

Every invocation begins by loading the checkpoint and re-observing the repository. It must verify the checkpoint against current files before continuing. If the previous action cannot be proven complete or idempotent, enter `HOLD`.

## Engineering lifecycle

`READ -> INVENTORY -> EVIDENCE CHECK -> DELTA ANALYSIS -> PROPOSE -> APPROVAL -> EDIT -> TEST -> REVIEW -> PERSIST -> RESUME`

GitHub Actions is the actuator/scheduler, not the authority. The durable state, evidence registers, and AGENTS.md define what may proceed.
