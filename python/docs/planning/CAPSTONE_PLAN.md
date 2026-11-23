# DATA120 — Preliminary Research and Modeling Plan

**Working title:** Exploring Unusual Repeat-Parking Observation Patterns

**State:** Proposed plan for student review, not a completed analysis or an instructor-approved assessment submission.

## 1. Context and research question

Staff manually inspect a customer-only parking lot, recording observed plates and date/time through Google Forms; the Sheet and Apps Script system processes the rounds. Exact arrival and departure times are **not recorded**. A vehicle may come and go between inspections. Staff, tenants, and service providers are not authorized to park in the customer area, but repeated observations do not independently prove a person's role or misuse.

**Primary research question:**

> To what extent can features derived from intermittent, manually recorded vehicle sightings identify unusual repeat-sighting patterns, compared with a simple transparent rule, after accounting for staff inspection frequency?

**Objective:** Learn Python/pandas/ML using real-world observational-data constraints and produce transparent *review priorities*, not enforcement decisions.

## Suspicious review-label requirement

The requested baseline is **two or more distinct completed or recorded area-check events containing the same vehicle on a single Edmonton-local calendar day**, not two repeated entries in one check and not two proven arrivals. This is a *suspicious review indicator*, not a confirmed violation. The new exploratory IsolationForest model can independently flag unusual vehicle-day observation patterns. Store `rule_suspicious`, `anomaly_suspicious`, `suspicious`, and `flag_source` separately so users understand the explanation.

See [SUSPICIOUS_PATTERN_MODEL.md](SUSPICIOUS_PATTERN_MODEL.md). Python module and synthetic tests exist; connection to live Sheets, production validation, prospective model evaluation and write-back are **not** implemented.

## Human verification and blacklisting (separate from ML)

A suspicious vehicle is **not automatically a violator**. An authorized staff member must independently verify whether parking rules were breached. Only an explicitly **confirmed violation** may lead to a blacklisted status. On-site ticketing/tagging must be performed by properly authorized staff and recorded as a separate manual action, not triggered by ML. Findings of `no_violation` or `inconclusive` do not blacklist a vehicle.

See [HUMAN_VERIFICATION_WORKFLOW.md](HUMAN_VERIFICATION_WORKFLOW.md). `src/verification.py` contains proposed pure records for human findings and reported manual actions; it is not connected to production Google Sheets or an enforcement system. Use verified outcomes to evaluate the research model only after appropriate authorization, without treating model predictions as ground truth.

## 2. Testable analysis questions (student to select)

- Which observed vehicles appear on many **distinct local dates** within a rolling 30-day window?
- How much do the resulting rankings change after adjusting for the **number of completed area checks**?
- Do an explainable rules baseline and an unsupervised model identify similar unusual patterns?
- Are patterns stable over time, across areas, and under reasonable feature/window changes?

No claim about true offender-prediction accuracy can be made without separately verified labels.

## 3. Unit of analysis

- **Raw record:** one vehicle sighting within one parking-area check.
- **Check record:** one survey of a specific area, including empty completed surveys.
- **Model row:** one pseudonymous vehicle × area × historical cutoff date, built only from sightings/checks **up to that cutoff**; define an evaluation schedule in advance.
- Time zone: `America/Edmonton`.
- Evaluation windows: start with 30 days; test 14/60 days as sensitivity checks if the dataset supports them.
- Deduplicate repeated entries for the same vehicle, check, and area while retaining an issue count for data-quality reporting.

## 4. Planned direct Google Sheets → Python connection

**The DATA120 Python model will be linked to the existing Google Sheet** using the Google Sheets API, subject to instructor, business privacy, and student review requirements. This is a planned read-only integration, not an installed connector.

- **Source**: Existing Google Sheet populated by Google Forms and Apps Script, including check/round metadata where available.
- **Authentication**: Approved Google OAuth credentials or dedicated service account with read-only sharing, stored securely outside Git; use the least-privilege `spreadsheets.readonly` scope. Do not use a Google account password.
- **Local secrets**: Store non-public configuration/secret values in ignored `python/.env`, created from committed placeholder-only `python/.env.example`. Reference Google credential JSON by a path to secure storage **outside the repo**. Follow [ENV_SETUP.md](../guides/ENV_SETUP.md).
- **Import**: Future `src/google_sheets_reader.py` loads approved worksheets into pandas DataFrames. Never commit raw downloaded rows or cache them in public repository files.
- **Processing**: Validate timestamps, check completeness, duplicates and source schemas; pseudonymize plate/jurisdiction values within an approved restricted environment before model analysis.
- **Operation**: Initially run the Python pipeline manually for coursework. Any recurring connection or write-back would require a separate design and explicit approval. No auto-ticketing, towing, or operational feedback loop.
- **Resilience**: Include a synthetic local-data mode and meaningful messages for missing credentials, API errors, or changed Google Sheet columns.

### Proposed connection stages

```text
Google Form → Google Sheets / Apps Script [production]
                        |
            Sheets API (read-only)
                        |
       Python connector (restricted)
                        |
        pandas validation + safe IDs
                        |
           features → ML experiment
                        |
      aggregate charts and course report
```

## 5. Python 3.13 architecture and design quality

- Runtime: **CPython 3.13**. Record exact dependency versions in a reproducible environment snapshot when work begins.
- **High cohesion**: a module/class handles one main job (read, validate, engineer features, fit/score, evaluate); avoid oversized manager classes.
- **Low coupling**: higher-level analysis should depend on small interfaces/protocols, not Google Sheets implementation details.
- **Adapter/Repository pattern**: interchangeable read-only Google Sheets and synthetic-data readers.
- **Dependency injection**: pass a data source to the analysis pipeline at construction or call time.
- **Strategy pattern**: compare explainable rule scores and experimental ML without rewriting data loading.
- **Pipeline separation**: notebooks orchestrate reusable functions and do not contain essential business logic.
- No global mutable state, implicit network calls at import time, or model training with side effects.
- Keep `.env` loading in one configuration module and inject typed settings into the Google Sheets adapter; do not couple feature/model classes to environment variables.
- Start simple: prefer plain functions or dataclasses over classes when an abstraction would add complexity without testability.

See [ARCHITECTURE.md](../architecture/ARCHITECTURE.md). Tests should replace Google access with a synthetic reader and verify that feature logic never contacts Google directly.

## 6. Implementation discipline — test-driven development

Apply [TDD_GUIDE.md](../guides/TDD_GUIDE.md) to all new Python functionality and bug fixes:

1. Define a student-approved behavior/acceptance criterion with synthetic data.
2. **RED:** write and run a `pytest` test that demonstrably fails for the correct reason.
3. **GREEN:** add the minimum implementation, rerun focused/related tests.
4. **REFACTOR:** improve low coupling/high cohesion and rerun the full suite.
5. Record real test commands/results, disclose material AI assistance, and await student reading and acceptance before the next substantive step.

Prioritize cleaning edge cases, field mapping, a fake Sheets reader, feature computation, leakage prevention, baseline and anomaly-model behavior. The existing cleaning module predates this TDD policy and must not be claimed as test-first. No tests were run merely by adding this policy.

## 7. Proposed Python workflow

| Phase | Student learning task | Output |
| --- | --- | --- |
| A. Sheets connectivity and data audit | Configure authorized read-only connection, map headers and completed-check coverage | Source mapping and quality summary |
| B. Data cleaning and normalization | Standardize check IDs, area labels, pseudonymous IDs, datetimes and completion flags; quarantine invalid records and de-duplicate within checks | Reproducible cleaned data plus an issue report |
| C. pandas exploration | Summarize sightings/checks over days, hours, and areas | Descriptive tables and charts |
| D. Features | Count unique check sightings and distinct dates; measure completed-check opportunity | Reproducible feature table |
| E. Baseline | **2+ distinct observed checks on the same day**; retain 30-day distinct-day summary as an additional feature | Transparent suspicious review signal |
| F. ML | Explore IsolationForest or clustering **only if sample size and variation are adequate** | Unusual-pattern score/group, not violation likelihood |
| G. Evaluation | Check sensitivity, stability over later periods, false-alarm potential, and comparison with baseline | Honest method comparison |
| H. Communicate | Explain what the features mean, limitations, privacy, and decisions that require a human | Student-authored report/presentation |

**Optional supervised alternative:** If an independently verified, appropriately authorized outcome dataset becomes available, compare a simple classifier (e.g. logistic regression or decision tree) to the baseline. Review labeling policy, class imbalance, leakage, and chronological testing before training. Operational AI/manual review flags are **not** automatically reliable truth labels.

## 8. Proposed features (not yet implemented)

- `sightings_30d`: unique vehicle-check appearances in 30 days
- `distinct_days_30d`: distinct local dates seen
- `distinct_weeks_30d`: distinct local calendar weeks seen
- `first_to_last_seen_days_30d`: elapsed days from first to last **observation**, not stay length
- `complete_area_checks_30d`: number of comparable completed checks in this area and window
- `observed_check_fraction_30d`: number of completed checks in which vehicle was seen / total completed comparable area checks (nullable when none)
- `observation_hour_diversity_30d`: number of distinct recorded hour buckets with sightings, only if timestamps are reliable
- `area_count_30d`: number of distinct areas where recorded (for per-vehicle cross-area summary)

**Data leakage protection:** Do not use future sightings or future operational statuses when constructing a historical feature row.

## 9. What success will and will not mean

A useful capstone should demonstrate **correct reproducible feature calculations**, honest descriptive visualizations, a justified ML technique, and interpretation of why model findings differ from a simple rule. Check changes in review rankings when inspection schedules differ. Validate with chronological holdout periods where possible.

Do **not** report "85% accuracy detecting illegal parkers" without verified external ground truth; anomaly scores, clusters, and rule flags are not legal or factual violation labels. The final judgment about a particular vehicle remains with a properly authorized human using additional evidence.

## 10. Proposed deliverables

- `notebooks/01_exploration.ipynb` — pandas exploratory work
- `../architecture/ARCHITECTURE.md` — low-coupling/high-cohesion design and dependencies
- `src/google_sheets_reader.py` — authorized read-only Google Sheets import into pandas
- `src/cleaning.py` — implemented normalization of approved pseudonymous checks/sightings; not a plate anonymizer
- `tests/test_cleaning.py` — synthetic cleaning edge cases (execution pending)
- `src/pattern_detection.py` — implemented same-day repeat-check rule and exploratory anomaly scoring
- `tests/test_pattern_detection.py` — synthetic behavior tests (focused local run: 8 passed; GitHub version not independently tested)
- `src/features.py` — modular future features
- `tests/test_features.py` — synthetic edge-case tests
- `notebooks/02_model_comparison.ipynb` — baseline/ML comparison
- `reports/` — public-safe charts and student-authored findings
- `DATA_DICTIONARY.md` — source mapping, derived-feature definitions, and limitations

Cleaning and its synthetic test module are now implemented. Other listed analysis modules and notebooks remain planned; no model or live Sheets connection exists yet.

## 11. Approval and integrity checkpoints

- [ ] Confirm assessment-specific rules for GAI assistance with the instructor.
- [ ] Student reviews and accepts this AI-generated **planning proposal**, and read/accept times are recorded in `../ai/AI_USE_LOG.md`.
- [ ] Obtain approval for direct Google Sheets API access and privacy requirements before connection.
- [ ] Confirm least-privilege API permissions and secure credentials stored outside Git.
- [ ] Keep all identifiable records and secrets out of public Git and GAI services.
- [ ] Map actual form/sheet fields before implementing the ingestion module.
- [ ] Follow and document RED → GREEN → REFACTOR cycles for new implementations.
- [ ] Choose the ML approach based on label availability and dataset size.
- [ ] Test effects of incomplete and irregular staff inspections.
- [ ] Cite third-party datasets, algorithms, code, and permitted AI assistance.

No live Google Sheets connection, production integration, fitted model, validation outcome, or instructor approval is claimed here.

## 12. November 16 recovery implementation plan and unchanged deadlines

**Recovery proposal status:** This revision was prepared November 16, 2026 and awaits student reading and acceptance. It changes the work order, not the assessment deadlines or the prior schedule-approval record. See the revised [S01–S31 calendar](GUIDED_SPRINT_SESSIONS.md) for session dates.

### Actual progress versus unverified tasks

- **Verified:** Python 3.13.14; student-reported full regression 29 passed; generator `--days 10 --seed 120` produced 18 inspections and 448 fictional sightings; complete eight-section presentation outline committed as `f8857eb` and accepted November 15.
- **Exists but requires fit-for-purpose audit:** `src/cleaning.py`, `src/pattern_detection.py`, synthetic-generator code, same-day check rule, exploratory Isolation Forest and their tests. Existence is **not** evidence of a completed cross-method comparison.
- **Not verified:** live authorized Sheets reader, completed S03–S08 sessions, unified feature matrix, LOF experiment, evaluated results, readable figures or final slide deck.
- **Carry-forward rather than start-over:** inspect existing code and tests before adding an adapter or replacing cleaning logic. Existing issue #3–#5 acceptance criteria remain in place, but dependent work can use the synthetic-only path.

### Dependency-first minimum viable research experiment

```text
Reproducible fictional observations + inspection/check metadata
     ↓ validate timestamps, area, completeness, duplicates
Comparable vehicle × analysis-window feature table
     ↓ shared inputs, explicit cutoff, no leakage
Transparent 2-distinct-check same-day review rule
     ↓
LOF (if small-sample safeguards work)  +  Isolation Forest (existing, re-evaluate)
     ↓ same input rows / transparent parameters and rankings
Synthetic-only comparison + authorized aggregate coverage assessment
     ↓ sensitivity, caveats, no pseudo-accuracy
2–3 public-safe figures + student interpretation + rehearsed slide deck
```

**Core minimum columns:** pseudonymous vehicle/area/window cutoff, unique completed/comparable checks with an observed sighting, distinct local dates, number of completed comparable area inspections, observed check fraction (nullable if denominator zero), optional observation-hour diversity when reliable. Same-check duplicates count once; checks not observed or not performed do not imply a vehicle was absent or continuously parked.

**Comparison contract:** baseline and all retained ML models consume the same pseudonymous observation window and appropriately normalized numeric features. The rule uses distinct same-local-day inspection IDs. LOF must bound `n_neighbors` below the eligible sample count; tiny/constant feature matrices require a clear skip/fallback rather than a deceptive anomaly flag. Isolation Forest should be rerun on the identical feature table. Explain model rankings instead of claiming probability of violations.

**Evaluation contract:** use time-bounded features with no future inspection/status leakage. Assess changes in rankings under plausible LOF-neighbor/Isolation-Forest settings and inspection frequencies. If only limited real data are available, report that; keep synthetic demonstration and real-data evidence separate. Historical `Violator` status means previously verified ticket and must never be inferred from a new anomaly. No accuracy/precision/recall claims without independent authorized labels.

### Recovery gates and implementation sequence

| Gate | Target | Work | Acceptance evidence / fallback |
| --- | --- | --- | --- |
| **G0: Audit and unblock** | **Mon Nov 16** | Review existing source/tests, S02–S08 evidence, check column dictionary/header-only mapping. Run actual baseline tests before edits. | Gap checklist and test log. Live Google Sheets remains optional; use fiction-only reader if not approved. |
| **G1: Features and baseline** | **Nov 17–18** | TDD shared vehicle/check feature calculations and verify the existing 2-distinct-check rule. | Synthetic edge cases, zero/one completed check, duplicate check entries, DST/local-day tests and RED/GREEN/REFACTOR. |
| **G2: Model comparison** | **Nov 18–20** | Add/test LOF with safeguards; reuse/test Isolation Forest on identical features; obtain comparison table and first chart. | Reproducible parameters and rankings; labels only mean review priority. |
| **G3: Scope decision** | **Sat Nov 21** | Keep optional kNN distance-based anomaly scoring strictly off critical path; only attempt it if baseline, LOF, Isolation Forest, evaluation and deck are ready. If capacity constrained, retain baseline plus one tested model. | Student accepts an explicit scope decision; no made-up second model. |
| **G4: Evaluation and slides** | **Nov 23–28** | Evaluate coverage, sample limitations, temporal leakage and sensitivity; create 2–3 public-safe charts; write conclusions and first visual deck. | Student-authored interpretation and rehearsed first draft. |
| **G5: Reproducible freeze** | **Nov 30–Dec 4** | Verify AI/APA rules, tests, chart reproducibility, slides, presenter notes, offline demo; freeze analysis **Fri Dec 4**. | Documented version/commit, actual tests, rehearsed artifact. |
| **G6: Delivery** | **Dec 5–11** | Rehearse Dec 5 and 7, present **Tue Dec 8**, apply feedback, audit and submit **Fri Dec 11**. | Delivery/submission evidence. No work on Sun Dec 6. |

### Explicit scope cuts

- **Keep optional:** kNN *distance-based unsupervised anomaly scoring* only if time permits after the baseline, LOF, Isolation Forest, tests, evaluation and presentation are ready. Standard supervised kNN classification is not the intended method. **Drop now:** other stretch ML methods, unneeded redesigns, auto-ticket/tow/write-back, additional Apps Script operational enhancements and general dashboards.
- **Defer unless available and authorized:** live read-only Google Sheets integration and its credential/error-path work; formal validation against confidential historical ticket data. A secure headers-only schema check may proceed without providing private rows.
- **Never cut:** privacy and data-access checks, TDD evidence for new Python behavior, a transparent baseline, at least one functioning appropriate ML comparison, honest interpretation, citations/disclosure requirements, and student review gates.
- **Escalate at Nov 21:** If two-model comparison is infeasible, prioritize baseline + one rigorously tested unsupervised experiment. Reduce algorithm breadth, not evidence quality.

### Implementation order by existing module

| Work area | Current basis | Next focused change | Issue |
| --- | --- | --- | --- |
| `src/cleaning.py` + tests | Existing implementation, regression previously passed | Audit feature input contract and gaps, not wholesale rewrite | [#4](https://github.com/alby1976/ParkingPatrol/issues/4) |
| `src/features.py` + `tests/test_features.py` | Proposed modules; verify whether added before creating | Implement deterministic comparable check denominators, local day, and cutoff; TDD | [#4](https://github.com/alby1976/ParkingPatrol/issues/4) |
| `src/pattern_detection.py` + tests | Existing same-day rule and exploratory Isolation Forest | Reuse, test on unified features and add LOF scoring if feasible | [#5](https://github.com/alby1976/ParkingPatrol/issues/5) |
| `src/google_sheets_reader.py` + fake tests | Planned; live authorization not verified | Defer live connection; maintain synthetic adapter boundary and headers-only dictionary | [#3](https://github.com/alby1976/ParkingPatrol/issues/3) |
| `reports/` + presentation | Eight-slide outline verified; findings pending | Comparison tables, figures, visual deck, reproducible results and rehearsal | [#7](https://github.com/alby1976/ParkingPatrol/issues/7), [#8](https://github.com/alby1976/ParkingPatrol/issues/8) |

### Fixed boundaries

- **Sundays OFF:** November 8, 15, 22, 29 and December 6. No catch-up assignments on Sunday.
- **Analysis freeze:** Friday December 4. **Presentation:** Tuesday December 8. **Submission:** Friday December 11 (check the instructor's actual hour).
- **Privacy:** real plates, raw records, credentials and identifying ticket history must remain outside the public repo and assistant context.
- **Academic integrity:** course-specific authorization for generative AI remains unverified; student must review each substantial change and personally own conclusions. Update AI_USE_LOG.md with actual activity and timestamps. Keep issues open until all criteria and review gates are evidenced.

## 13. Original approved schedule retained as historical baseline (November 6, 2026)

The student accepted the *original* schedule on November 6, 2026. The revised November 16 recovery plan above supersedes its **work ordering only**. The original fixed dates, target time allocation, and Sundays off remain valid.

- Presentation: Tuesday December 8, 2026.
- Final submission: Friday December 11, 2026.
- Internal analysis and figure freeze: Friday December 4, 2026.
- Sunday rest: November 8, 15, 22, 29 and December 6.
- Suggested time budget: weekdays 60–90 minutes; Saturdays 2–3 hours.

The historical S01–S31 session allocation appears in prior Git history and grouped GitHub issues; current session tasks are in [GUIDED_SPRINT_SESSIONS.md](GUIDED_SPRINT_SESSIONS.md).

**No new Python code, live data access, fitted ML comparison or tests are claimed by this documentation update.**

## 14. Assignment-rubric priority update — November 22, 2026

**Verified source:** Student-uploaded D2L *6. DAT 120 Mini Capstone Project* (2 pages). Point allocation: **ML model 40, coding 30, presentation 20, one-page summary 10**. The instructions call for data exploration and visualization, model training/validation and business interpretation, and accept a **Python script OR notebook**. A clearly documented **optional Jupyter notebook** could improve traceability for evaluators; it must reuse existing tested modules and should be dropped if it threatens the **December 4 freeze**. The presentation **must not exceed 10 minutes**; rehearse at 8–9 minutes as a planning margin. The completed paper and presentation go to the D2L *Mini capstone project* dropbox; verify whether code/notebook must be uploaded separately in the interface.

**Immediate evidence goals:** audit model evaluations and synthetic 10d/30d sensitivity; distinguish Isolation Forest's preset ~10% contamination from independent evidence of performance; document LOF's 20-neighbor duplicate-group safeguard, unscored versus zero anomalies, absent verified labels, correlated vehicle-day rows and inability to infer parking duration or illegal use. Add public-safe EDA charts and concise interpretations. Avoid synthetic-data inflation or unsupported accuracy, precision and recall claims.

**Dates:** retain Dec 4 internal freeze and Dec 11 assignment submission. Dec 8 is an **internal readiness target**; the five-page course outline places final presentations in Week 6, **December 9**. Confirm instructor's actual presentation appointment rather than asserting Dec 8. Sundays remain off. See the [updated guided sprint calendar](GUIDED_SPRINT_SESSIONS.md) and Issues #7–#10.

**Integrity:** Instructor-specific permitted GAI uses and required in-submission citation format remain unconfirmed. Log AI support, retain individual student analysis and verification, and keep raw identifiers out of public deliverables.

## 15. Student-confirmed inspection schedule and analysis correction (November 22, 2026)

- **First inspection:** normally 10:15–10:30 AM.
- **Second:** around 12:30 PM when inspector workload allows; sometimes **not performed**.
- **Third:** around 3:30 PM when time allows or parking-space complaints prompt it.
- **Completion:** every inspection that is actually performed completes its lot round. **A skipped check is not an incomplete check.**
- **Observed-absence operational convention:** a plate observed at an earlier completed inspection but not recorded at a later **completed** inspection is **assumed to have left by that later check**. It is not a verified departure time or parking duration; departure is unknown without a subsequent check, and a vehicle can leave/re-enter between checks.
- **Bias:** complaint-triggered and discretionary third checks are not random; same-day flagged counts must be interpreted relative to opportunities for inspection.

**Evidence gap / no automatic code changes:** Existing synthetic generator models one/two rounds at 09:00/15:00 with 5% incomplete checks, unlike the real workflow; historical published synthetic 10d/30d results and Slide 7 still reflect that earlier generator. Preserve them as historical baselines. Scheduled correction: S15 analyze assumptions; S16–S17 TDD of configurable 1–3 complete inspection rounds and optional simulation triggers if essential to the 40-point ML rubric; S18 compare results/coverage with earlier simulation; S19–S20 revise interpretation and public-safe visualizations if warranted. Use new output folders and do not silently overwrite accepted artifacts. Keep Dec 4 analysis freeze, rest Sundays, Dec 11 submission, and an under-10-minute presentation. Related: Issue #7; no sample-level real data to public GitHub.
