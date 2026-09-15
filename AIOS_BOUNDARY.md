# AIOS Boundary Contract — `RX50`

`RX50` is an evidence/engineering substrate. It does not own generalized system policy.

## Authority invariants

- **Policy owner:** repository engineering rules, evidence requirements, and the durable controller.
- **Agent authority:** propose/organize evidence work inside the registered queue only.
- **Safety authority:** explicit owner/safety authorization and frozen state are mandatory gates.
- **Durability:** controller state and lineage are persisted and resumable.
- **Contradictions/evidence:** missing evidence or unmet authorization remains BLOCKED/HOLD; it is not silently resolved.
- **Fail closed:** a registered audit path is required before promotion; iteration limits cannot mask stronger safety/evidence blocks.

## AIOS adoption status

| Boundary | Status |
|---|---|
| Observe → Decide → Act → Verify → Persist → Resume | IMPLEMENTED |
| Evidence/safety gates outside agent | IMPLEMENTED |
| Durable state + lineage | IMPLEMENTED |
| Explicit generalized permit/capability object | AIOS-CENTRAL |
| General contract/authority verifier | AIOS-CENTRAL |
| External-effect receipt/reconciliation layer | AIOS-CENTRAL |
| Central workload execution | AIOS-CENTRAL — pinned to `e2dc2c32bedf7de598b66e1bfe89f300fb83ccfc` |

RX50 does not grow a second incompatible control plane. The `aios/adapter.py` workload is executed by the central AIOS runner; RX50 remains responsible only for its engineering/evidence semantics and safety gates.

## Rule

Never convert an evidence gap, safety gap, contradiction, or missing authorization into PASS merely to advance the loop.
