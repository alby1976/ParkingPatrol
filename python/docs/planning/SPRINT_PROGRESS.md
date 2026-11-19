# DATA120 Sprint Progress

S01 environment checks were verified from student-provided PyCharm terminal screenshots and **S01 is completed** following explicit student reading and acceptance on November 7, 2026 at 21:38:57 MST. S02's baseline tests, synthetic generation, and eight-slide presentation outline are verified; **the complete outline was accepted on November 15, 2026**. Remaining S02/Issue #2 closure checks are not marked complete merely from this approval. S03–S31 are not verified as completed.

See [calendar](GUIDED_SPRINT_SESSIONS.md) and [coach instructions](CHATGPT_SPRINT_COACH.md).

For each session, record ID, date, objective, actual minutes, tests observed, changed files, presentation progress, next task, and review decision. Sundays remain free.

## S01 — Environment checks (observed by November 7, 2026)

- Status: **Completed** — student read and accepted the verified summary on 2026-11-07T21:38:57-07:00.
- Verified output: `python --version` returned `Python 3.13.14`; prompt showed active `.venv`.
- Verified Git output: `git status --short --branch` showed `main...origin/main` and `?? .idea/` at the time checked. This does not prove the branch is synchronized with the live remote.
- Verified ignore-rule output: `git check-ignore -v .idea/` identified `.gitignore:26`, and `git check-ignore -v python/.env` identified `.gitignore:17`.
- Caution: The observed `?? .idea/` entry predates the later ignore checks; if needed, re-run Git status to confirm that current output is clean. Ignore rules do not retroactively untrack previously tracked secrets.
- Code changes: None observed; tests: Not run / not applicable for environment checks; Python installer via `py` launcher was not available, but active Python 3.13.14 works.
- AI coaching/review ID: `s01-environment-20261107` (**Accepted**; read and decision timestamps both 2026-11-07T21:38:57-07:00).
- Related issue: [#2](https://github.com/alby1976/ParkingPatrol/issues/2) (keep issue open; S02 is still pending).
- Next: S02 baseline tests and synthetic data/slide outline on a **non-Sunday** day after required review.

## S02 — Baseline tests and synthetic data (in progress, November 9–10, 2026)

- **Status:** In progress. The privacy-test correction is accepted; the 10-day synthetic generator and complete eight-slide outline are **verified**; outline approval recorded on November 15, 2026. S02 issue-level acceptance criteria remain to be reviewed before closing #2.
- **Environment:** Python 3.13.14; pytest 9.2.0 in active `.venv` (student terminal output).
- **TDD evidence:** The initial full run reported 27 passed / 2 failed. A historical DST fixture was already corrected in the version tracked by Git. The unknown-check test's contradictory assertion was repaired, then strengthened with fictional ID `PRIVATE_TEST_CHECK_987654` and a diagnostic schema assertion; RED reproduced, GREEN focused 1 passed in 0.69 seconds, and full regression **29 passed in 2.00 seconds**.
- **Verified commit:** [d29b1238](https://github.com/alby1976/ParkingPatrol/commit/d29b1238efea0e445edd3fedfcab811c5f90ea87), `test(cleaning): check invalid IDs stay hidden`, referencing [issue #4](https://github.com/alby1976/ParkingPatrol/issues/4).
- **Approval:** student explicitly read and accepted privacy-test correction; AI review ID `s02-privacy-20261110`; read/accept time `2026-11-10T21:47:38-06:00`.
- **Next:** run existing 10-day synthetic data generator, then create slide outline. Keep S02 and grouped issue #2 open until all acceptance criteria are satisfied. Sundays remain rest days.

### S02 presentation and synchronization verification — November 12, 2026

- **Synthetic generation verified:** `python python/src/synthetic_data.py --days 10 --seed 120` returned **18 inspections, 448 fictional sightings**. Student confirmed both ignored CSVs in `python/generated/`; observations are synthetic, not real evidence.
- **Presentation milestone:** [PRESENTATION_OUTLINE.md](../../reports/PRESENTATION_OUTLINE.md) contains Slides 1–3: project/research question, staff observation collection, and real-vs-synthetic data. Actual file reviewed via staged diff; no private plates/credentials present.
- **Git commit:** [9b13643](https://github.com/alby1976/ParkingPatrol/commit/9b136431376b609a9d8c018f853d86484f616492), `docs(data120): add initial presentation outline`, `Refs #2`; one Markdown file, 49 insertions. Pushed to GitHub via merge [9312336](https://github.com/alby1976/ParkingPatrol/commit/93123369e8b8f88c1f2abd02d1f2946c4da047fe).
- **Local sync:** student ran `git status --short --branch` and observed only `## main...origin/main` (no tracked or untracked local changes shown).
- **Testing:** no tests executed for documentation-only presentation change; existing independently reported Python regression was 29 passed in 2.00 seconds.
- **AI review:** `s02-outline-20261112` is **Accepted**; the current outline commit message accurately describes pending review.
- **Remaining S02 work:** complete or revise the eight-slide skeleton and required approval. Keep [issue #2](https://github.com/alby1976/ParkingPatrol/issues/2) open; never close it for three slides alone.

### S02 full eight-slide outline accepted — November 15, 2026

- **Approved artifact:** [PRESENTATION_OUTLINE.md](../../reports/PRESENTATION_OUTLINE.md), complete outline for Slides 1–8; model findings still marked as pending.
- **Student GitHub commit:** [f8857eb](https://github.com/alby1976/ParkingPatrol/commit/f8857eb036d98f31cb02a37561e1145fdb29be0a), documentation only, `Refs #2`; verified on the remote repository.
- **AI review:** `s02-eight-slide-outline-20261115` **Accepted**; reading and acceptance confirmed together at `2026-11-15T21:15:51-06:00`.
- **Tests:** No new tests for the Markdown change; previous student full regression was 29 passed. The existing 10-day synthetic generation reported 18 checks and 448 fictional sightings.
- **Remaining:** Confirm all grouped Issue #2 acceptance criteria before changing its status. The outline is not a final presentation with evaluated model results. No new development scheduled on Sunday.

## Recovery rebaseline proposed — November 16, 2026 (awaiting student review)

- **Reason:** As of November 15, only S01 and S02's main deliverables have recorded verification; sessions S03–S08 do not have complete closeout evidence. That is an evidence gap of six scheduled sessions, not proof that no code was written.
- **Revised calendar:** [GUIDED_SPRINT_SESSIONS.md](GUIDED_SPRINT_SESSIONS.md), recovery commit `6745a90`.
- **Revised implementation plan:** [CAPSTONE_PLAN.md](CAPSTONE_PLAN.md), recovery commit `7a4a6f1`.
- **Immediate Monday Nov 16 gate:** inspect existing cleaning/pattern-detection/test modules and S02–S08 issues; run baseline tests and identify the smallest missing feature/test. No source changes or tests were executed while preparing this revision.
- **Revised priorities:** use fictional data without waiting for live Sheets credentials; build comparable completed-check features; verify two-check rule; test LOF/Isolation Forest against identical features; prepare evidence and public-safe charts.
- **Scope cut:** optional kNN is removed from the capstone critical path. New Apps Script deployment, write-back and enforcement automation stay out of scope. If by Nov 21 two ML models are unready, explicitly select baseline plus one reliable unsupervised model.
- **Hard dates unchanged:** Dec 4 analysis freeze, Dec 8 presentation, Dec 11 submission; Sundays Nov 22, 29 and Dec 6 remain off.
- **Approval:** The student explicitly **read and accepted** this revised plan on 2026-11-17T08:36:42-06:00 (America/Edmonton). Review ID `sprint-recovery-20261116`. This approves the schedule, not outstanding S03–S08 implementation or tests.
- **Git/issue caution:** GitHub-file edits may place remote `main` ahead of local PyCharm `main`; fetch/pull only after checking local status and avoiding overwriting uncommitted work.

## S09 — Recovery code audit accepted (November 18, 2026)

- **Status:** Audit completed and **explicitly accepted** by the student at `2026-11-18T22:01:13-06:00` (America/Edmonton); AI review ID `s09-audit-20261118`. This does not complete S03–S08 or close grouped Issue #4.
- **Actual baseline test command:** `python -m pytest python/tests -v`. Student supplied Windows 11 / Python 3.13.14 / pytest 9.2.0 terminal output: **33 passed in 18.36 seconds**, 0 failed.
- **Source inventory:** `cleaning.py`, `pattern_detection.py`, `staff_status.py`, `synthetic_data.py`, `verification.py`; five corresponding test modules. `features.py` and `test_features.py` not present in observed local inventory.
- **Reused functions:** `build_vehicle_day_features` (6 defined vehicle-day features), `mark_repeat_check_suspicious` (2 distinct observed checks/day), and `score_anomalies` (exploratory in-sample Isolation Forest with minimum eligible sample and data-quality checks).
- **ID audit:** The fictional generator creates unique `check_id` values in its single area; its tests assert uniqueness. Cleaning explicitly excludes a `check_id` reused in multiple areas and records `check_id_used_for_multiple_areas`. Student confirmed **no exact assertion** for that diagnostic in `python/tests/test_cleaning.py` using `Select-String`. This is a targeted regression-test gap, not a verified production fault.
- **Remaining:** Add RED-first synthetic collision/quarantine test, then audit/extend shared comparable-inspection feature schema for LOF and Isolation Forest; keep future exploratory/prospective enhancements (#12/#13), optional kNN, bootstrapping and external datasets off critical path.
- **Evidence boundaries:** These findings are from student-shared local code excerpts and pytest output; no code files were changed as part of S09 audit, and no live source data or secrets were shared.
- **Next step:** Begin one small TDD regression test for cross-area inspection-ID collision in S10 / Issue #4; ask student to approve the actual code change before implementation proceeds.

## S10 — Cross-area check-ID regression test accepted (November 18, 2026)

- **Scope:** First S10 test-only task, **accepted**, but S10 feature engineering and Issue #4 are **not completed**.
- **Test added:** `test_check_id_reused_across_areas_is_quarantined` in `python/tests/test_cleaning.py`; fictional EAST/WEST duplicated check ID is excluded, collision diagnostic recorded, linked sightings omitted. Existing cleaning implementation unchanged; this previously untested behavior passed on first run (not a RED→GREEN implementation cycle).
- **Student-observed results:** `python -m pytest python/tests/test_cleaning.py::test_check_id_reused_across_areas_is_quarantined -v`: **1 passed in 0.65s**. `python -m pytest python/tests -q`: **34 passed in 2.05s**. `git diff --cached --check` produced no output.
- **Git:** student committed and pushed [42ead3c](https://github.com/alby1976/ParkingPatrol/commit/42ead3c2117d3fa547daec0b0411aac99fd5e53b), `Refs #4`; GitHub remote commit verified. No private identifiers or operational data in the test.
- **AI review:** `s10-cross-area-20261118` **Accepted**, student explicitly confirmed reading and acceptance at `2026-11-18T22:58:16-06:00` (America/Edmonton).
- **Next:** safely synchronize local PyCharm main with updated remote documentation, then test-first review of shared comparable-completed-check features for LOF/Isolation Forest. Optional kNN, bootstrapping, external backup datasets, and future Issues #12/#13 stay deferred.

### S10 zero-completed-check regression accepted — November 18, 2026

- **Test:** `test_no_completed_checks_keeps_coverage_unknown` in `python/tests/test_pattern_detection.py`; all checks in the synthetic fixture marked incomplete, `SYN_B` retains one positive sighting, zero completed comparable checks and `NaN` observation fraction.
- **TDD evidence:** Initial student run failed `assert 2 == 0` because fixture retained two completed checks; corrected fixture passed focused **1 test in 1.17s** without production edits. Full suite **35 passed in 1.46s**, student reported; existing logic was confirmed, not newly implemented.
- **Git:** [4b8ccb8](https://github.com/alby1976/ParkingPatrol/commit/4b8ccb8a98473d2121cc803b5b1642f67bedb32c), `Refs #4`, uploaded and independently verified.
- **AI review:** `s10-zero-coverage-20261118` **Accepted** by explicit student reading/acceptance at `2026-11-18T23:41:40-06:00` America/Edmonton.
- **Remaining:** S10 feature-table design/comparison not done; grouped #4 remains open. Continue with a small audit/test for numeric feature eligibility for both LOF and Isolation Forest. Synchronize local Git first because AI log and tracker were updated remotely.
