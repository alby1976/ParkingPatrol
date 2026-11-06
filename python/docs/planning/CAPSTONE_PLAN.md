# DATA120 — Preliminary Research and Modeling Plan

**Working title:** Exploring Unusual Repeat-Parking Observation Patterns

**State:** Proposed plan for student review, not a completed analysis or an instructor-approved assessment submission.

## 1. Context and research question

Staff manually inspect a customer-only parking lot, recording observed plates and date/time through Google Forms; the Sheet and Apps Script system processes the rounds. Exact arrival and departure times are **not recorded**. A vehicle may come and go between inspections. Staff, tenants, and service providers are not authorized to park in the customer area, but repeated observations do not independently prove a person's role or misuse.

**Primary research question:**

> To what extent can features derived from intermittent, manually recorded vehicle sightings identify unusual repeat-sighting patterns, compared with a simple transparent rule, after accounting for staff inspection frequency?

**Objective:** Learn Python/pandas/ML using real-world observational-data constraints and produce transparent *review priorities*, not enforcement decisions.

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
- **Local secrets**: Store non-public configuration/secret values in ignored `python/.env`, created from committed placeholder-only `python/.env.example`. Reference Google credential JSON by a path to secure storage **outside the repo**. Follow [ENV_SETUP.md](ENV_SETUP.md).
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

See [ARCHITECTURE.md](ARCHITECTURE.md). Tests should replace Google access with a synthetic reader and verify that feature logic never contacts Google directly.

## 6. Implementation discipline — test-driven development

Apply [TDD_GUIDE.md](TDD_GUIDE.md) to all new Python functionality and bug fixes:

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
| E. Baseline | Example: 3+ **distinct observed dates** in 30 days | Transparent review-priority indicator |
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
- `ARCHITECTURE.md` — low-coupling/high-cohesion design and dependencies
- `src/google_sheets_reader.py` — authorized read-only Google Sheets import into pandas
- `src/cleaning.py` — implemented normalization of approved pseudonymous checks/sightings; not a plate anonymizer
- `tests/test_cleaning.py` — synthetic cleaning edge cases (execution pending)
- `src/features.py` — modular features with docstrings
- `tests/test_features.py` — synthetic edge-case tests
- `notebooks/02_model_comparison.ipynb` — baseline/ML comparison
- `reports/` — public-safe charts and student-authored findings
- `DATA_DICTIONARY.md` — source mapping, derived-feature definitions, and limitations

Cleaning and its synthetic test module are now implemented. Other listed analysis modules and notebooks remain planned; no model or live Sheets connection exists yet.

## 11. Approval and integrity checkpoints

- [ ] Confirm assessment-specific rules for GAI assistance with the instructor.
- [ ] Student reviews and accepts this AI-generated **planning proposal**, and read/accept times are recorded in `AI_USE_LOG.md`.
- [ ] Obtain approval for direct Google Sheets API access and privacy requirements before connection.
- [ ] Confirm least-privilege API permissions and secure credentials stored outside Git.
- [ ] Keep all identifiable records and secrets out of public Git and GAI services.
- [ ] Map actual form/sheet fields before implementing the ingestion module.
- [ ] Follow and document RED → GREEN → REFACTOR cycles for new implementations.
- [ ] Choose the ML approach based on label availability and dataset size.
- [ ] Test effects of incomplete and irregular staff inspections.
- [ ] Cite third-party datasets, algorithms, code, and permitted AI assistance.

No live Google Sheets connection, production integration, fitted model, validation outcome, or instructor approval is claimed here.
