# Proposed parking data collection — inspections, ticket history, and verification

**Status:** Proposed future data design for ParkingPatrol; **not implemented** in the live Google Form/Sheet, Apps Script, or Python data connector. Student reading and acceptance pending. Related issues: [#11](https://github.com/alby1976/ParkingPatrol/issues/11) (staff status) and [#14](https://github.com/alby1976/ParkingPatrol/issues/14) (historical ticket context).

## Goal

Keep data entry easy during a complete staff walk-around while distinguishing (1) observations, (2) **independently verified prior tickets**, and (3) **reviews of a possible current incident**. These records are linked by a stable private vehicle identity, but they must not be conflated. A prior ticket or anomaly flag does not establish a current violation.

**Only invented examples and schema descriptions belong in this public repository.** Store real plates, plate jurisdictions, ticket evidence and personal information only in an access-controlled clinic system with authorized access and an approved retention policy. A production adapter must pseudonymize plate **plus jurisdiction** before any analysis export; do not publish the mapping or its secret.

## 1. Inspections (one row per *performed* lot walk-around)

| Proposed field | Example (fictional) | Meaning / collection rule |
| --- | --- | --- |
| `check_id` | `CHK_001` | Unique ID for one actually performed inspection |
| `area_id` | `LOT_A` | Area covered by this inspection (clinic has 38 stalls) |
| `check_at` | `2026-11-24 10:15-07:00` | **Recorded inspection reference/start time**, not every vehicle's exact observation minute |
| `check_complete` | `true` | Performed walk-around covered all stalls; omitted rounds are **not** incomplete records |
| `inspection_reason` | `routine` | `routine` or `customer_complaint`; record only if actually known |
| `check_finished_at` | *unknown* | Optional, only if staff actually record the finish time |
| `duration_minutes` | *unknown* | Derived from measured start/finish if available; do **not** substitute a synthetic average for real data |
| `recorded_by` | *restricted staff ID* | Optional accountability field; do not expose employee identity in public exports |

The first routine inspection usually begins 10:15–10:30 AM; the ~12:30 PM and ~3:30 PM checks are optional. A complaint when **no round is active** triggers an additional inspection. When a complaint arrives **during an active round**, that round satisfies it; do not create a duplicate check. Consider a separate complaint event table if multiple complaints need to be logged. Skipped inspections create no check row.

## 2. Vehicle sightings (one row per observed vehicle in a check)

| Proposed field | Example (fictional) | Meaning / collection rule |
| --- | --- | --- |
| `check_id` | `CHK_001` | Foreign key to `inspections.check_id` |
| `vehicle_id` | `SYN_0001` | Opaque, approved pseudonym for privately normalized plate + jurisdiction |
| `area_id` | `LOT_A` | Same area as the matching inspection |
| `observed_at` | `2026-11-24 10:15-07:00` | **Inspection reference time** if no individual sighting time was captured; never invent the minute |
| `time_precision` | `inspection_level` | `inspection_level` when the observation inherits `check_at`; `exact` only for an independently captured timestamp |
| `observation_source` | `staff_round` | Optional source provenance, if verified |

**Simplest staff workflow:** Begin a round, enter the observed plates, and submit the complete inspection. The software assigns `check_id` to every row and associates the shared inspection timestamp. An empty completed round must still be represented in the inspection table even when it has no sightings. Deduplicate one vehicle per check/area; repeated sightings in different checks remain separate.

`observed_at == check_at` under `inspection_level` does **not** mean all cars were seen at precisely that minute. The system never knows an actual vehicle arrival, departure, or parking duration merely from these sightings.

## 3. Historical tickets (restricted verified evidence; one row per prior ticket)

| Proposed field | Example (fictional) | Meaning / collection rule |
| --- | --- | --- |
| `historical_ticket_id` | `HIST_001` | Restricted internal record key |
| `vehicle_id` | `SYN_0001` | Same approved pseudonymous identity |
| `ticket_status` | `verified` | Confirmed by an authorized person checking original restricted ticket evidence |
| `ticket_at` | `2026-11-05 12:30-07:00` | Actual issued-at time, **if known**; never infer from status submission |
| `ticket_reference` | *restricted reference* | Private evidence pointer; never publish the real citation number |
| `verified_by` | *restricted staff ID* | Who authenticated the earlier ticket |
| `verified_at` | `2026-11-06 09:00-07:00` | When the earlier ticket was authenticated |

This table is distinct from the existing **Unknown / Suspicious / Violator** staff-status Form: `Violator` means a verified **historical** ticket, **not** guilt today. Maintain correction/revocation history where applicable. Unknown or missing evidence is **not** a verified negative. Keep each past ticket as a separate record rather than overwriting a single status; do not copy real historical ticket details into public GitHub.

## 4. Verification / review queue (one row per review case)

| Proposed field | Example (fictional) | Meaning / collection rule |
| --- | --- | --- |
| `review_id` | `REV_001` | Unique review case |
| `vehicle_id` | `SYN_0002` | Vehicle being reviewed |
| `review_reason` | `repeated_sightings` | Why queued (`repeated_sightings`, `anomaly_flag`, `staff_report`, etc.) |
| `flagged_at` | `2026-11-24 12:30-07:00` | When added to review queue, not first arrival |
| `review_status` | `pending` | Workflow status: `pending`, `reviewed`, or `closed` |
| `review_outcome` | *unknown* | **Separate** independent human finding: `confirmed_violation`, `no_violation`, or `inconclusive` |
| `reviewed_at` | *unknown* | Actual completion timestamp, if reviewed |
| `reviewer_id` | *restricted staff ID* | Who made the review decision |
| `evidence_ref` | *restricted reference* | Restricted supporting evidence |

Do not turn `suspicious` into a confirmed-violation training label. `pending` means the review has not been completed. If an authorized person later issues a ticket/tag or takes another permitted action, record it as a **separate manual action** with its own timestamp and private reference, using the existing [human verification workflow](HUMAN_VERIFICATION_WORKFLOW.md).

## 5. Optional complaint-event table (future extension)

| Proposed field | Example (fictional) | Meaning |
| --- | --- | --- |
| `complaint_id` | `CMP_001` | Unique complaint event |
| `complaint_at` | `2026-11-24 10:20-07:00` | Time complaint actually received |
| `reason` | `no_space_available` | Customer reports no available space; not evidence of an unauthorized vehicle |
| `handled_by_check_id` | `CHK_001` | Active or newly started inspection satisfying complaint |

An active inspection can handle a complaint without changing `inspection_reason = routine`. Separate complaint-event records allow multiple complaints to refer to one inspection; the present S17 **synthetic** generator supports at most one simulated complaint per day and does not implement this table.

## Future ML: keep evidence and predictions separate

- Build the initial two-check rule, Isolation Forest and LOF features from sightings and **completed inspection opportunities**, not status labels.
- Use verified prior tickets as **separate review context** for authorized staff. A previous ticket does not prove a fresh violation or trigger automatic ticketing/towing.
- For prospective or supervised analyses, only include ticket/status information **known by the evaluation cutoff**. Never use future verification or ticket records to label earlier predictions.
- Keep synthetic timing and duration assumptions out of operational data. Compare `inspection_level` versus truly `exact` timestamps only when such measurements actually exist.
- Use least-privilege access, documented retention/correction rules, and an audit trail for review decisions and enforcement actions; assess applicable legal/privacy requirements before deployment.

## Existing components and implementation status

- Existing proposal: [DATA_DICTIONARY.md](DATA_DICTIONARY.md) and [HUMAN_VERIFICATION_WORKFLOW.md](HUMAN_VERIFICATION_WORKFLOW.md).
- Implemented **offline** validation: `src/staff_status.py`, `src/verification.py`. These do not authenticate live ticket history or connect to the actual Google Sheet.
- This document is a **data-collection proposal only**. No production Google Form, Google Sheet, Apps Script, Python source, database, retention rule, or ML behavior is modified by this documentation commit.
- Student must review and accept the proposed fields and data-access constraints before implementing them. Related [Issue #11](https://github.com/alby1976/ParkingPatrol/issues/11), [Issue #14](https://github.com/alby1976/ParkingPatrol/issues/14).
