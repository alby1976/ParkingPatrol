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

## 12. Presentation and submission schedule (2026)

- **December 8, 2026 (Tuesday): DATA120 presentation.**
- **December 11, 2026 (Friday): final project submission.**
- **Internal target December 4:** freeze the analysis, figures, and demonstration so the December 8 presentation can be rehearsed. December 9–11 is reserved for final revisions and submission, not first-time implementation.

| Dates | Deliverable | Required review |
| --- | --- | --- |
| Nov 6–12 | Read-only Sheets import design; normalize data and test securely with synthetic fixtures | Verify API authorization, no secrets or raw plates in Git |
| Nov 13–19 | Observation features, two-check rule, independent human review representation and synthetic unit tests | Review complete vs incomplete check handling |
| Nov 20–26 | Pilot Isolation Forest on available real history only if authorized and suitable; run separate synthetic demonstration | Flag exploratory findings as anomalies, never true offences |
| Nov 27–Dec 3 | Compare rule versus ML, inspect review usefulness and limitations; produce student-authored charts | Confirm data sources, test evidence, citations, AI-use disclosure |
| Dec 4–7 | Freeze graphs and model version; rehearse presentation, verify offline demonstration | Record approval before substantial new steps |
| Dec 8 | Present DATA120 mini capstone | Present results and uncertainty clearly |
| Dec 9–11 | Incorporate appropriate feedback and submit the final report/code by Dec 11 | Final privacy, integrity, citation and Git review |

**Current evidence constraint (as of November 5):** approximately 10 days of actual parking observations, 38 spaces, typically one or two survey rounds a day. Continue collecting real observations separately; do not pretend that fictional data extends the real observation period.

### Synthetic data generator (implemented)

Use [SYNTHETIC_DATA_GUIDE.md](SYNTHETIC_DATA_GUIDE.md) and `python/src/synthetic_data.py` to create reproducible fictional 10-, 45- or 90-day scenarios using pseudonymous identifiers. The generator models a maximum of 38 recorded spots at each check, one/two daily inspections, optional incomplete rounds, and repeated vehicles. It **does not** simulate genuine parking violations, prove offender-detection accuracy, or produce real plates. Generated CSV files go under ignored `python/generated/` and must not be mixed with actual records in reported results.

Focused local synthetic-generator tests: **6 passed** with Python 3.13.5. The full repository test suite and live Sheets integration have not been verified for this addition.
