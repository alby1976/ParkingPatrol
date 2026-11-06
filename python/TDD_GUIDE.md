# DATA120 — Test-Driven Development (TDD) Guide

**Status:** Proposed workflow, awaiting student reading and acceptance. Applies to the Python 3.13 capstone only; does not change production Google Apps Script.

## The red → green → refactor loop

1. **RED — Write the test first.** Express one observable behavior in a tiny synthetic `pytest` test. Run it and verify it fails *for the intended missing behavior*, not an import error or a broken test.
2. **GREEN — Implement just enough.** Add the smallest Python code to make the new test pass. Run the focused test and existing related tests.
3. **REFACTOR — Improve the design.** Remove duplication, improve names, retain low coupling and high cohesion. Run the tests again; verify they still pass.
4. **REVIEW — Record evidence.** Capture commands run, results (pass/fail), limitations and meaningful AI assistance in the commit description and AI-use log. Present material for reading and acceptance before the next substantive step.

```text
Requirement / acceptance criterion
              |
       Write synthetic test
              |
       RED: expected failure
              |
        Minimal code change
              |
        GREEN: tests pass
              |
      Refactor without changing behavior
              |
         Tests pass again
              |
       Student reads and accepts
```

This cycle applies to **new features, bug fixes, integration adapters, and cleaning rules**. Test-first means actually running the failing test, rather than simply committing a test and implementation together and claiming TDD happened. Never fabricate evidence of a red or green run.

## Testing pyramid for ParkingPatrol DATA120

| Level | Examples | No real credentials? |
| --- | --- | --- |
| Unit (most tests) | Normalize identifiers/timestamps, reject ambiguous dates, calculate distinct sighting days | Yes |
| Component | Pipeline with injected synthetic reader; verify checks/sightings stay separate | Yes |
| Contract | Sheets reader maps expected header/schema, handles empty ranges and API errors using a fake client | Yes |
| Authorized integration (few tests) | Read-only Google Sheets request against a dedicated test sheet | Requires explicit authorization; skip by default |
| ML evaluation | Reproducibility, fixed seeds, train/test chronology and prevention of future-data leakage | Yes, with synthetic fixtures |

**Do not use actual licence plates or private Google Sheet rows in automated GitHub tests.** A mocked Sheets adapter must never need a private `.env`.

## Python 3.13 commands

From the repository root, with an installed Python 3.13 virtual environment:

```powershell
.\.venv\Scripts\python.exe -m pytest python/tests -q
.\.venv\Scripts\python.exe -m pytest python/tests/test_cleaning.py -q
```

Run the focused test during RED, focused + related tests during GREEN, and the full test suite after REFACTOR. Document whether each command actually ran and its result.

## Naming and design

- Use `test_*.py` for test files, `test_*` for test functions, and `pytest` for assertions/fixtures.
- Keep externally observable behavior as the testing target; avoid tests that rigidly enforce implementation details.
- The Google Sheets API adapter sits at the edge; inject a fake reader for tests. Feature engineering and models must not depend on Google credentials.
- Design test inputs around **synthetic** vehicle IDs; no raw plates in public fixtures.
- Include negative cases: blank IDs, duplicate checks, incomplete/empty rounds, unknown check references, DST ambiguity, dataset schema changes, and zero observations.
- Reproduce bugs by writing a failing regression test **before** fixing the bug.
- Use small commits tied to one behavior, with useful commit messages and honest validation.

## Existing work adoption

The `src/cleaning.py` and `tests/test_cleaning.py` files already existed before TDD was adopted. Do **not** describe those earlier changes as test-first. Baseline their tests and, when altering a cleaning behavior in future, start with a failing regression test and follow RED → GREEN → REFACTOR.

## Student learning / academic integrity

A coding assistant may teach TDD, suggest a test plan, and help explain failures *within the instructor's assignment-specific GAI rules*. The student must independently understand, verify and interpret results. Log AI contributions and obtain explicit reading and acceptance confirmation per [AGENTS.md](AGENTS.md) and [AI_REVIEW_GATE_GUIDE.md](AI_REVIEW_GATE_GUIDE.md).

For every meaningful cycle, the commit message should include:

```text
TDD evidence:
- RED: command and observed expected failure (or "not run")
- GREEN: command and observed result (or "not run")
- REFACTOR: command and observed result (or "not run")
```

**No tests were run while preparing this guide.**
