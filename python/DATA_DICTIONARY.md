# DATA120 Proposed Data Dictionary

These are **proposed analytical fields**, not a claim that each currently exists in the live Google Sheet. Map them to real column names before implementing an importer.

| Field | Meaning | Caution |
| --- | --- | --- |
| `vehicle_id` | Pseudonymous plate + issuing jurisdiction identifier | Never commit original plate or a reversible lookup table |
| `observed_at` | Date/time staff recorded vehicle presence | Not an arrival timestamp |
| `check_id` | Unique staff parking check/round | Important for deduplication |
| `area_id` | Area within the lot | Compare absences only within the same area |
| `check_complete` | Whether staff completed the area survey | Incomplete checks cannot establish absence |
| `check_at` | Date/time of area check | Confirm available timestamps and time zone |
| `source_status` | Existing operational review status, if included | Not ground-truth violation label |
| `verified_outcome` | Independently confirmed review outcome, if available | Must be separately validated and appropriate for training |

### Derived features

| Feature | Definition |
| --- | --- |
| `sighting_count_30d` | Distinct vehicle/check appearances over previous 30 days |
| `distinct_days_30d` | Number of local calendar dates on which plate was observed |
| `observed_weeks_30d` | Number of local calendar weeks with sightings |
| `days_between_first_last` | Difference between first and last sighting dates; **not** occupancy |
| `complete_checks_area_30d` | Total completed comparable checks for that area and window |
| `observed_check_share_30d` | Sighted completed checks / all comparable completed checks; undefined if denominator is zero |

### Security and reproducibility

- Calgary observation timestamps should be interpreted in `America/Edmonton`, respecting daylight saving transitions.
- Keep pseudonymization secrets outside the repository; plain hashing of short licence-plate strings can be vulnerable to guessing.
- Use synthetic data in committed demos. Never upload production observations to a public repository.
- Do not infer identity, job role, illegality, or continuous duration from a licence-plate observation.
- Document the analysis cutoff, exclusions, missing observations, and number of checks.
