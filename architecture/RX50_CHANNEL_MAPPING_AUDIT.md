# RX50 Channel Mapping Audit — STRICT AUTO

Status: `PROVISIONAL — CONSISTENT`

## Coverage

- Logical channels: 0..49
- Continuity MUX banks: 4 × 16 positions = 64 positions
- Output shift-register bits: 7 × 8 = 56 positions

## Deterministic logical allocation

| Logical range | Continuity bank | MUX positions | Output register bits |
|---|---|---|---|
| CH00..CH15 | MUX0 | 0..15 | Q0..Q15 |
| CH16..CH31 | MUX1 | 0..15 | Q16..Q31 |
| CH32..CH47 | MUX2 | 0..15 | Q32..Q47 |
| CH48..CH49 | MUX3 | 0..1 | Q48..Q49 |

Unused continuity positions: MUX3 positions 2..15 (14 positions).
Unused shift-register bits: Q50..Q55 (6 bits).

## Strict checks

1. Every logical channel 0..49 has exactly one continuity position.
2. Every logical channel 0..49 has exactly one output bit.
3. No logical channel is assigned twice.
4. Spare positions/bits are explicitly identified and must not be silently reused.
5. This mapping is documentation-level and does not define a firing electrical stage.

## Result

`PASS` for logical coverage and uniqueness at the architecture level.

Final physical connector mapping, GPIO lock, electrical characteristics, and safety authorization remain OPEN.
