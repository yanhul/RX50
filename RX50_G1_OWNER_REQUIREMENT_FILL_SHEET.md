# RX50 G1 OWNER REQUIREMENT FILL SHEET
# BATCH: G1-OWNER-REQ-01
# DATE: 2026-08-15

STATUS:
G1 = HOLD
G2 = HOLD
G4 = READY TO MEASURE
G5 = PROVISIONAL / NOT LOCKED
G6 = HOLD

PURPOSE:
Thu thập requirement thực tế của owner cho khả năng firing multi-channel
của RX50.

HARD RULES:
- Không tự điền số.
- Không kế thừa số từ RX24 nếu owner chưa xác nhận.
- Không suy ra requirement từ khả năng linh kiện.
- Không biến engineering recommendation thành owner requirement.
- Không có evidence -> TBD / OPEN.
- Mọi numerical value phải có SOURCE hoặc được owner xác nhận.
- G1 requirement không được dùng để đóng G4.
- Không thiết kế firing-power subsystem trong batch này.

==================================================
R-01 — SIMULTANEOUS FIRING CHANNEL COUNT
==================================================

OWNER INPUT:
[                                      ]

Định nghĩa:
- Số kênh tối đa cần kích hoạt trong cùng một firing event.
- Có phải toàn bộ 50 kênh hay một nhóm nhỏ hơn?
- Có nhiều firing profile không?

REQUIRED:
- Numerical value / bounded range / TBD
- Nếu range: upper bound phải rõ.

SOURCE / EVIDENCE:
[                                      ]

STATUS:
OPEN / OWNER-CONFIRMED / TBD

IMPACT:
G2 firing-power sizing
G8 hardware feasibility
G9 firmware scheduling

==================================================
R-02 — LOAD ENVELOPE
==================================================

LOAD TYPE:
[                                      ]

OWNER / FIELD LOAD:
[                                      ]

AVAILABLE DATASHEET:
[                                      ]

Required parameters IF AVAILABLE:
- Load resistance: [ ]
- Required firing current: [ ]
- Operating voltage: [ ]
- Load tolerance: [ ]
- Number of loads simultaneously active: [ ]

SOURCE:
[                                      ]

Nếu chưa có dữ liệu:
STATUS = TBD / MEASUREMENT REQUIRED

Không dùng giá trị RX24 để điền.

==================================================
R-03 — PULSE PARAMETERS
==================================================

Required firing waveform:

Peak / required current:
[                                      ]

Pulse width:
[                                      ]

Voltage during firing:
[                                      ]

Energy requirement:
[                                      ]

Tolerance:
[                                      ]

SOURCE:
[                                      ]

RULE:
Các giá trị phải đến từ:
- load datasheet
- firing procedure
- validated measurement
- hoặc explicit owner requirement.

Không suy ra từ MOSFET/battery.

STATUS:
OPEN / EVIDENCE-BACKED / TBD

==================================================
R-04 — DEFINITION OF "SIMULTANEOUS"
==================================================

OWNER DEFINITION:

Firing event window:
[                                      ]

Maximum permitted channel-to-channel skew:
[                                      ]

Trigger reference:
[                                      ]

Does simultaneous mean:
[ ] same firmware command
[ ] same electrical event
[ ] within specified timing window
[ ] other: __________

SOURCE / RATIONALE:
[                                      ]

STATUS:
OPEN / OWNER-CONFIRMED / TBD

NOTE:
R-04 belongs to G1 timing ownership.
Do not derive it from MCU execution speed.

==================================================
R-05 — FIRING RAIL ARCHITECTURE
==================================================

Battery source:
[                                      ]

Battery voltage range:
[                                      ]

Dedicated firing rail:
[ ] YES
[ ] NO
[ ] TBD

Logic rail relationship:
[                                      ]

Allowed firing-rail voltage deviation:
[                                      ]

Required behavior during simultaneous firing:
[                                      ]

SOURCE:
[                                      ]

STATUS:
OPEN / OWNER-CONFIRMED / TBD

==================================================
R-06 — TRANSIENT / PROTECTION REQUIREMENTS
==================================================

Maximum permitted rail sag:
[                                      ]

Maximum permitted transient:
[                                      ]

Short-circuit behavior:
[                                      ]

Over-current behavior:
[                                      ]

Protection requirement:
[                                      ]

Recovery behavior:
[                                      ]

SOURCE:
[                                      ]

STATUS:
OPEN / TBD

==================================================
R-07 — THERMAL / DUTY CYCLE
==================================================

Operating ambient:
[                                      ]

Maximum firing duration / sequence:
[                                      ]

Repeated firing requirement:
[                                      ]

Minimum interval between events:
[                                      ]

Maximum number of consecutive events:
[                                      ]

Thermal recovery requirement:
[                                      ]

SOURCE:
[                                      ]

STATUS:
OPEN / TBD

==================================================
R-08 — PCB CURRENT PATH REQUIREMENTS
==================================================

DO NOT FILL UNTIL R-01/R-02/R-03 ARE AVAILABLE.

Worst-case simultaneous channel count:
[DERIVED AFTER R-01]

Per-channel current:
[DERIVED AFTER R-02/R-03]

Worst-case aggregate current:
[CALCULATE ONLY AFTER INPUTS]

PCB constraints:
- Copper thickness: [ ]
- Layer availability: [ ]
- Connector current rating requirement: [ ]
- Mechanical constraints: [ ]

SOURCE:
[                                      ]

STATUS:
BLOCKED BY R-01/R-02/R-03

==================================================
R-09 — FAULT ISOLATION
==================================================

Single-channel fault behavior:

[ ] must not affect other channels
[ ] controlled degradation acceptable
[ ] system shutdown required
[ ] TBD

Fault types in scope:
[ ] open
[ ] short
[ ] MOSFET failure
[ ] wiring/load short
[ ] other: __________

Fault detection requirement:
[                                      ]

Required isolation behavior:
[                                      ]

SOURCE:
[                                      ]

STATUS:
OPEN / TBD

NOTE:
RX24 safety architecture may be INPUT EVIDENCE,
not automatically inherited requirement.

==================================================
R-10 — FIRING AUTHORIZATION / G6 INTERFACE
==================================================

Who/what authorizes simultaneous firing?
[                                      ]

Required authorization chain:
[                                      ]

Behavior on RF loss:
[                                      ]

Behavior on invalid command:
[                                      ]

Behavior on MCU reset:
[                                      ]

Behavior on safety-key removal:
[                                      ]

Behavior on communication corruption:
[                                      ]

G6 owner requirement / evidence:
[                                      ]

STATUS:
OPEN / TBD

==================================================
DEPENDENCY GRAPH
==================================================

R-01 ─┐
      ├──> firing event definition ──> G2 sizing
R-02 ─┤
      │
R-03 ─┤
      └──> worst-case electrical envelope

R-04 ───────────────> G1 timing requirement

R-05 ───────────────> G2 rail architecture
R-06 ───────────────> G2 protection
R-07 ───────────────> G2 thermal
R-08 ───────────────> PCB feasibility
R-09 ───────────────> safety/fault architecture
R-10 ───────────────> G6 authorization

==================================================
G1 CLOSURE RULE
==================================================

G1 MUST NOT close merely because fields are filled.

For each R-xx:

OWNER REQUIREMENT = YES/NO
SOURCE = PRESENT/MISSING
NUMERICAL VALUE = VERIFIED/TBD
EVIDENCE = PRESENT/MISSING
STATUS = OPEN/EVIDENCE-BACKED

G1 can proceed only when the requirements necessary for
firing-power feasibility are evidence-backed.

==================================================
CRITICAL AUDIT
==================================================

[ ] No RX24 firing value silently inherited
[ ] No simultaneous-channel count invented
[ ] No load resistance invented
[ ] No firing current invented
[ ] No pulse width invented
[ ] No energy requirement invented
[ ] No skew requirement invented
[ ] No battery voltage invented
[ ] No PCB current invented
[ ] No thermal duty cycle invented
[ ] No G2 conclusion
[ ] No G4 modification
[ ] No G5 lock
[ ] No G6 authorization conclusion

---

## INGESTION STATUS (this batch)

- Owner input received: NONE (all fields blank at time of save). [STATUS]
- All R-01..R-10: OPEN / TBD. [STATUS]
- R-08: BLOCKED BY R-01/R-02/R-03. [STATUS]
- G1 closure rule: not triggered (no requirement evidence-backed). [STATUS]
- Critical audit: all items comply (no number invented; nothing inherited). [STATUS]
- Action: owner fills the fields above; then this sheet becomes the G1 requirements register input for review. [RECOMMENDATION]