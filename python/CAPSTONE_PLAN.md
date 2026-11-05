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
- **Authentication**: Approved Google OAuth credentials or dedicated service account with read-only sharing, stored securely outside Git; use the least-privilege `spreadsheets.readonly` scope.
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

## 5. Proposed Python workflow

| Phase | Student learning task | Output |
| --- | --- | --- |
| A. Sheets connectivity and data audit | Configure authorized read-only connection, match column headers, missing values, completed-check coverage | Source map and quality summary | Match real column headers, missing values, completed-check coverage | Source map and quality summary |
| B. pandas exploration | Summarize sightings/checks over days, hours, and areas | Descriptive tables and charts |
| C. Features | Count unique check sightings and distinct dates; measure completed-check opportunity | Reproducible feature table |
| D. Baseline | Example: 3+ **distinct observed dates** in 30 days | Transparent review-priority indicator |
| E. ML | Explore IsolationForest or clustering **only if sample size and variation are adequate** | Unusual-pattern score/group, not violation likelihood |
| F. Evaluation | Check sensitivity, stability over later periods, false-alarm potential, and comparison with baseline | Honest method comparison |
| G. Communicate | Explain what the features mean, limitations, privacy, and decisions that require a human | Student-authored report/presentation |

**Optional supervised alternative:** If an independently verified, appropriately authorized outcome dataset becomes available, compare a simple classifier (e.g. logistic regression or decision tree) to the baseline. Review labeling policy, class imbalance, leakage, and chronological testing before training. Operational AI/manual review flags are **not** automatically reliable truth labels.

## 6. Proposed features (not yet implemented)

- `sightings_30d`: unique vehicle-check appearances in 30 days
- `distinct_days_30d`: distinct local dates seen
- `distinct_weeks_30d`: distinct local calendar weeks seen
- `first_to_last_seen_days_30d`: elapsed days from first to last **observation**, not stay length
- `complete_area_checks_30d`: number of comparable completed checks in this area and window
- `observed_check_fraction_30d`: number of completed checks in which vehicle was seen / total completed comparable area checks (nullable when none)
- `observation_hour_diversity_30d`: number of distinct recorded hour buckets with sightings, only if timestamps are reliable
- `area_count_30d`: number of distinct areas where recorded (for per-vehicle cross-area summary)

**Data leakage protection:** Do not use future sightings or future operational statuses when constructing a historical feature row.

## 7. What success will and will not mean

A useful capstone should demonstrate **correct reproducible feature calculations**, honest descriptive visualizations, a justified ML technique, and interpretation of why model findings differ from a simple rule. Check changes in review rankings when inspection schedules differ. Validate with chronological holdout periods where possible.

Do **not** report "85% accuracy detecting illegal parkers" without verified external ground truth; anomaly scores, clusters, and rule flags are not legal or factual violation labels. The final judgment about a particular vehicle remains with a properly authorized human using additional evidence.

## 8. Proposed deliverables

- `notebooks/01_exploration.ipynb` — pandas exploratory work
- `src/google_sheets_reader.py` — authorized read-only Google Sheets import into pandas
- `src/features.py` — modular features with docstrings
- `tests/test_features.py` — synthetic edge-case tests
- `notebooks/02_model_comparison.ipynb` — baseline/ML comparison
- `reports/` — public-safe charts and student-authored findings
- `DATA_DICTIONARY.md` — source mapping, derived-feature definitions, and limitations

These are **planned filenames**; no notebook or model exists yet.

## 9. Approval and integrity checkpoints

- [ ] Confirm assessment-specific rules for GAI assistance with the instructor.
- [ ] Student reviews and accepts this AI-generated **planning proposal**, and read/accept times are recorded in `AI_USE_LOG.md`.
- [ ] Obtain approval for direct Google Sheets API access and privacy requirements before connection.
- [ ] Confirm least-privilege API permissions and secure credentials stored outside Git.
- [ ] Keep all identifiable records and secrets out of public Git and GAI services.
- [ ] Map actual form/sheet fields before implementing the ingestion module.
- [ ] Choose the ML approach based on label availability and dataset size.
- [ ] Test effects of incomplete and irregular staff inspections.
- [ ] Cite third-party datasets, algorithms, code, and permitted AI assistance.

No live Google Sheets connection, production integration, fitted model, validation outcome, or instructor approval is claimed here.
