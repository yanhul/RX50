# RX50 Autonomous Evidence Harness

Evidence-first controller for the RX50 research lifecycle.

This repository deliberately does **not** contain a firing design, firing-power values, schematic, BOM, or hardware authorization. It only automates evidence-state handling.

## Rules

- Evidence is authoritative; absence of evidence produces HOLD/BLOCKED.
- No numerical engineering requirement is invented by the controller.
- Owner/safety authorization is never inferred.
- A candidate must be audited before promotion.
- Evidence artifacts are hashed before state transition.
- Iteration is bounded.

Current project evidence says the RX50 firing/load envelope remains HOLD and G4 measurement evidence is absent. The harness therefore must not promote a firing candidate from repository state alone.
