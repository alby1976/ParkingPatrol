# Synthetic-data tests

Implemented: `test_cleaning.py` uses synthetic identifiers to test normalization, deduplication, incomplete/empty checks, check conflicts, unknown links, and daylight-saving validation.

Run with `python -m pytest python/tests/test_cleaning.py` in the project Python 3.13 environment. Execution has not been verified yet.

Additional tests for future development:
- Duplicate vehicle entries in a single completed check count once.
- The same plate with different issuing jurisdictions remains distinct.
- Empty completed checks contribute to observation opportunity, not sightings.
- Incomplete and other-area checks never establish absence.
- No future records leak into a historical cutoff.
- Daylight saving time and missing timestamps are handled explicitly.

Do not use actual identifiable parking records as GitHub test fixtures.
