# DATA120 — Preliminary Data Dictionary

**Status:** Proposed normalized research schema. These are *candidate analytical fields*, not a verified copy of Google Sheet column headers. Actual mappings must be checked **without uploading real plates or private rows**.

## Google Sheets as the Python data source

**Planned connection:** An authorized, read-only Google Sheets API client will retrieve selected worksheets from the existing Google Forms/Sheets/Apps Script system into Python pandas DataFrames. Map actual worksheet names and column headers before implementing the connector. Credentials, source rows and vehicle identifiers remain private and must never be committed to this public repository.

**Proposed extraction metadata (not necessarily columns already in the Sheet):**

| Field | Meaning |
| --- | --- |
| `sheet_name` | Name of source worksheet used for this import |
| `extracted_at` | Timestamp of the API retrieval |
| `source_row_number` | Optional internal location for error diagnosis; keep private |
| `schema_version` | Locally assigned version of the verified column mapping |

The connector should read both vehicle sightings and completed/empty area checks when such data is available. The operational Google Sheet is the **data source**, not the prediction output target.

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

## Staff-reported plate status — separate Form (new; NOT human verification)

A companion Google Form (see [administrator setup guide](../../../docs/Per_Vehicle_Status_Setup.md)) collects **one plate per response** with three required questions: `Plate`, `Province`, and `Staff-reported status` (choose **Unknown**, **Suspicious**, **Violator**). It is separate from the existing multi-plate inspection-round Form. The status response sheet holds raw private plate information and **must not** be copied into the public Python repository.

Before Python import, a future authorized adapter must pseudonymize `Plate + Province` within a restricted environment, map the Form response timestamp with an explicit timezone offset, and retain only the following columns:

| Python field | Meaning | Rule |
| --- | --- | --- |
| `vehicle_id` | Already-pseudonymized plate+province identity | Only approved opaque IDs; never raw plate |
| `staff_status` | Staff category: `unknown`, `suspicious`, `violator` | Required; no implicit verified status |
| `reported_at` | Offset-aware time of the staff category submission | The submission time, not the actual observation or violation time |

Implemented offline validation: `src/staff_status.py` → `normalize_staff_reports(reports)`. Synthetic tests in `tests/test_staff_status.py` cover missing statuses, unsupported categories, plate-like IDs, raw plate columns and timezone offsets. The actual Google Sheets read-only adapter and data join **remain unimplemented**.

**Do not treat `staff_status == "violator"` as `confirmed_violation`.** A staff assertion is not independently verified evidence, must not trigger blacklisting or enforcement, and must not be used as an unsupervised-model ground-truth label. Explicit independently verified outcomes remain separate in the human verification workflow. Avoid time leakage: never join future staff reports into historical feature rows.

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

## Normalization output (implemented)

The `src/cleaning.py` function accepts two pandas DataFrames with the **normalized proposed column headers** from the tables above; an actual Google Sheets-to-schema mapping remains to be implemented.

`normalize_observations(checks, sightings)` returns:
- `checks`: normalized `check_id`, `area_id`, `check_at` (Edmonton timezone), `check_complete` (bool).
- `sightings`: normalized `vehicle_id` (already pseudonymized), `check_id`, `area_id`, `observed_at` (Edmonton timezone), deduplicated per vehicle/check/area.
- `issues`: source table name, zero-based input row position and non-sensitive reason code. Invalid records are **excluded** from cleaned outputs, not silently corrected.

The normalizer accepts common boolean spellings such as yes/no, trims and capitalizes identifiers, and rejects ambiguous/nonexistent naive local times (for example, DST transition times) unless timestamps contain a reliable UTC offset. Contradictory duplicate check rows are quarantined. Completed checks with no vehicles remain in the checks table. No parking duration or actual absence is inferred. Real plate/jurisdiction identifiers must be pseudonymized *before* calling the normalizer; this module does not itself anonymize data. It does not read `.env` or Google Sheets and is safe to test with synthetic IDs.

## Same-day suspicion and exploratory anomaly fields

See [SUSPICIOUS_PATTERN_MODEL.md](SUSPICIOUS_PATTERN_MODEL.md).

| Field | Meaning |
| --- | --- |
| `day` | Calendar date of the **check timestamp**, interpreted in America/Edmonton |
| `same_day_distinct_checks` | Count unique check IDs recording the vehicle on that date |
| `rule_suspicious` | True when `same_day_distinct_checks >= 2` |
| `distinct_days_30d` | Number of days with sightings over the previous 30 local calendar days (inclusive) |
| `area_completed_checks_day` | Completed same-day check opportunities across areas in which the vehicle was seen |
| `observed_fraction_day` | Seen-in-completed-checks fraction over those comparable completed checks; null if none |
| `distinct_areas_day` | Areas containing positive sightings that day |
| `check_hour_span` | Hours between earliest and latest **check timestamps**, not parking duration |
| `anomaly_score` | Relative IsolationForest unusualness, not guilt probability |
| `anomaly_suspicious` | Exploratory ML outlier for staff review |
| `model_status` | Scored or reason the model did not score |
| `suspicious` | Rule or anomaly flagged; never a confirmed offender label |
| `flag_source` | Rule, anomaly, both, or none |

**Event definition:** Distinct area/check ID. A duplicate entry within the same check does not increase the count. A vehicle observed twice may have remained parked throughout. Incomplete checks can record positive sightings but cannot establish absence. Model training/scoring currently use a supplied snapshot and must not be treated as leakage-free prospective validation.

## Human verification outcomes (separate operational review data)

These fields represent **independently verified human decisions**, not outcomes inferred from the unsupervised model:

| Field | Meaning |
| --- | --- |
| `review_status` | `confirmed_violation`, `no_violation` or `inconclusive` |
| `reviewer_id` | Restricted opaque human-reviewer identifier |
| `evidence_ref` | Restricted private reference to independently checked supporting evidence |
| `reviewed_at` | Timezone-aware human review timestamp |
| `blacklisted` | True only when the human finding is a confirmed violation |
| `manual_action` | Separately recorded `ticket` or `tag` performed by authorized staff |
| `action_staff_id` | Restricted opaque ID of staff who actually recorded the action |
| `action_ref` | Private ticket/tag reference |
| `action_at` | Timezone-aware timestamp of the recorded action |

The Python research code only provides a representation of these decisions; it cannot verify that an actual staff member checked the evidence or issued a ticket. Do not upload real enforcement details to the public repository. See [HUMAN_VERIFICATION_WORKFLOW.md](HUMAN_VERIFICATION_WORKFLOW.md).

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
- [ ] Approved Google Sheets read-only access, private credentials and pseudonymization method
- [ ] Which worksheets contain sightings and completed/empty parking rounds
- [ ] Whether worksheet access and API quotas support the intended refresh frequency

This dictionary is a design aid, not proof that all fields are already collected.
