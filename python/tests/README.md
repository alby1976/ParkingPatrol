# Synthetic-data tests (planned)

Proposed tests for later student-led implementation:
- Duplicate vehicle entries in a single completed check count once.
- The same plate with different issuing jurisdictions remains distinct.
- Empty completed checks contribute to observation opportunity, not sightings.
- Incomplete and other-area checks never establish absence.
- No future records leak into a historical cutoff.
- Daylight saving time and missing timestamps are handled explicitly.

Do not use actual identifiable parking records as GitHub test fixtures.
