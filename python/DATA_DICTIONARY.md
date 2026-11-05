# DATA120 — Preliminary Data Dictionary

**Status:** Proposed normalized research schema. These are *candidate analytical fields*, not a verified copy of Google Sheet column headers. Actual mappings must be checked **without uploading real plates or private rows**.

## Source record concepts

| Suggested field | Type | Description | Critical caveat |
| --- | --- | --- | --- |
| `vehicle_id` | string | Private, keyed pseudonymous identifier for normalized plate **plus jurisdiction** | Never store the raw plate or secret in Git; synthetic IDs in public examples |
| `check_id` | string | Identifier for each staff inspection/check | Used to deduplicate observations |
| `area_id` | string | Part of lot inspected | Checks in another area cannot establish absence |
| `observed_at` | timezone-aware datetime | When a staff member observed the vehicle | **Not** arrival time |
| `check_at` | timezone-aware datetime | Timestamp associated with a check | A completed check can have zero observed vehicles |
| `check_complete` | nullable boolean | Whether area survey is confirmed complete | Null/incomplete is not evidence of absence |
| `record_source` | string | Origin, e.g. Form response vs reviewed export | Record lineage; confirm actual source columns |
| `operational_status` | string, optional | Existing assumed/potential/most-likely/confirmed review label | **Not** independently verified model target |
| `verified_outcome` | string, optional | Separate documented human-verified outcome | Only if authorized, definition and verification method recorded |

### Linked research tables (recommended)

**`checks`** (one row per check, including empty completed checks): `check_id`, `area_id`, `check_at`, `check_complete`.

**`sightings`** (one row per vehicle/check/area after deduplication): `vehicle_id`, `check_id`, `area_id`, `observed_at`.

Avoid reconstructing an empty check solely from the `sightings` table. Verify every `check_id` has a matching check record and that area and time agree.

## Engineered columns — one vehicle × area × cutoff

| Feature | Definition | Missing-value rule |
| --- | --- | --- |
| `sightings_30d` | Count of distinct vehicle/check observations during the prior 30 days | Zero with adequate documented coverage; otherwise context needed |
| `distinct_days_30d` | Number of distinct Edmonton-local dates when seen | Zero if no sightings |
| `distinct_weeks_30d` | Number of distinct local calendar weeks when seen | Zero if no sightings |
| `first_to_last_seen_days_30d` | Elapsed calendar days between first and last sightings | Null if fewer than two sightings |
| `complete_area_checks_30d` | Number of completed checks of the **same area** | Zero when no completed checks |
| `observed_check_fraction_30d` | Completed checks where observed / all completed same-area checks | Null if denominator is zero; do not treat as occupancy |
| `observed_hour_bins_30d` | Count of distinct local hour buckets of observed sightings | Null if timestamps unusable |
| `area_count_30d` | Distinct areas seen for same vehicle across the window | Vehicle-level feature; document join method |

**Window definition:** A cutoff must be defined once (e.g. `(cutoff - 30 days, cutoff]`); records after the cutoff must not enter features. For model comparison, consistently represent zero-sighting candidate vehicles and inspection opportunities, or disclose if the analysis is limited to previously sighted vehicles.

## Required data-quality checks

1. Plate identity: preserve jurisdiction, normalize carefully, and flag unreadable/ambiguous observations for human review.
2. Dates: timezone `America/Edmonton`; daylight saving changes; distinguish observation vs submission date.
3. Deduplication: same vehicle in same area/check counts once; do not merge distinct checks.
4. Coverage: missing/incomplete checks do not imply absence; include completed **empty** area checks.
5. Sampling bias: extra walk-arounds mean extra opportunities to observe a vehicle.
6. Validation: no inferred true driver identity, actual parking duration, or illegal parking outcome from these fields alone.
7. Security: never commit confidential row-level exports, raw plates, keys, or realistic linkable examples in this public repository.

## Still to confirm from the live system

- [ ] Exact Google Sheet headers and which sheet holds completed checks
- [ ] Whether each observation has area, check ID, and observed time separately
- [ ] How a completed **empty check** is represented
- [ ] Time zone and timestamp parsing conventions
- [ ] Whether independently validated review outcomes exist at all
- [ ] Approved export and pseudonymization method

This dictionary is a design aid, not proof that all fields are already collected.
