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

## Required development workflow (new work)

For future changes, use **test-driven development: RED → GREEN → REFACTOR**. Read [../TDD_GUIDE.md](../TDD_GUIDE.md).

1. Write a small `pytest` test of the intended behavior before implementing it.
2. Run it and confirm it fails for the intended reason (**RED**).
3. Implement the smallest working solution and rerun (**GREEN**).
4. Refactor, run focused and full tests, and record actual results (**REFACTOR**).
5. Log AI assistance and obtain student reading/acceptance before the next substantive step.

The existing cleaning tests were drafted alongside an implementation, not demonstrably test-first. Do not claim past TDD evidence. This document update has not run tests.
