# RX50 Autonomous Evidence Loop

This automation is deliberately **evidence-management only**. It does not generate or authorize firing-circuit parameters, PCB changes, firmware changes, or safety-critical design decisions.

## Loop

`inventory evidence -> detect changes -> inspect project state -> HOLD/READY_FOR_REVIEW -> persist state`

Future agent integration must remain behind the existing RX50 rules:

- no invented numerical specifications;
- no invented manufacturer evidence;
- one conceptual change per proposed engineering hypothesis;
- provenance required;
- no OOS selection/tuning;
- owner/safety gates remain authoritative;
- bounded iterations;
- immutable artifact hashes.

An LLM may propose a mission or evidence request, but local validators remain authoritative.
