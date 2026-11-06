# DATA120 Architecture — Python 3.13

**Status:** Proposed learning architecture; student reading and acceptance pending. This design intentionally keeps the Google Forms/Sheets/Apps Script application separate from the Python coursework.

## Main goal: low coupling, high cohesion

- **Low coupling:** changing the Google Sheets API adapter should not require changing feature calculations or models.
- **High cohesion:** each component has a focused reason to change.
- **Simple over clever:** favor functions/dataclasses where appropriate; add interfaces/classes only when they improve testing or comparison.

## Conceptual component diagram

```text
Google Sheet (existing)             Synthetic data (tests)
         |                                  |
         v                                  v
 GoogleSheetsReader                  SyntheticReader
         |                                  |
         +------ DataReader Protocol ------+
                         |
                 injected into
                         v
                    Pipeline
                         |
                SchemaValidator
                         |
                  FeatureBuilder
                         |
              ScoringStrategy Protocol
                    /          \
                   v            v
              RuleBaseline   AnomalyModel
                    \          /
                      Evaluator
                         |
              aggregate-only results
```

**Dependency rule:** Pipelines, features, models and tests do **not** import Google API client classes. Only the Google adapter knows authentication and network behavior.

## Suggested design patterns

| Pattern | Use in DATA120 | Benefit |
| --- | --- | --- |
| **Adapter / Repository** | `GoogleSheetsReader` and `SyntheticReader` satisfy the same small reader contract | Offline reproducibility and easy change of data source |
| **Dependency injection** | Supply a reader/strategy to a pipeline instead of constructing one inside | Replace live services with test doubles |
| **Strategy** | `RuleBaseline` versus exploratory anomaly model | Compare methods without editing import code |
| **Pipeline** | Explicit data load → validation → features → scoring → evaluation | Transparent, teachable execution |
| **Dataclass** | Immutable configuration and typed results where helpful | Less hidden state |

Do **not** force a class for every function. The entry-point script can assemble dependencies once; notebooks call the same reusable functions.

## Proposed modules (not implemented)

```text
python/src/
  ports.py                  # Python 3.13 typing.Protocol interfaces
  google_sheets_reader.py   # external adapter; read-only Sheets API
  synthetic_reader.py       # no network; synthetic fixtures
  cleaning.py               # implemented: deterministic cleanup + normalized checks/sightings
  validation.py             # additional validation (planned)
  features.py               # pure pandas feature calculations
  modeling.py               # interchangeable rules/ML strategies
  evaluation.py             # honest comparison without violation claims
  pipeline.py               # orchestration, receives injected components
```

## Cleaning and normalization boundary

`src/cleaning.py` is implemented as a **pure pandas** function, `normalize_observations(checks, sightings)`, returning `CleanResult(checks, sightings, issues)`. The Google Sheets adapter and synthetic reader will feed this function *after* removing/replacing real plate identifiers in an authorized private environment.

It uppercases and trims pseudonymous IDs/check/area identifiers, parses timestamps into `America/Edmonton`, normalizes completion values, preserves completed empty checks, deduplicates same-vehicle/check/area rows, and quarantines invalid/conflicting records with issue codes and row positions (no source values). It rejects obviously unsafe raw-plate columns but is **not an anonymization tool** and cannot guarantee detection of all sensitive information. It does not infer arrivals, departures, custody, or violations.

A future pipeline will inject a reader, apply normalization, and separately handle warnings before feature calculation; no direct Google API dependency is imported by the cleaner. Synthetic test cases live in `tests/test_cleaning.py`. Tests have not been run in Python 3.13 yet.

## Same-day review rule + unsupervised strategy

Implemented independently of Google access in [../../src/pattern_detection.py](../../src/pattern_detection.py):
1. `build_vehicle_day_features(checks, sightings)` — calculate local-day features from cleaned, already-pseudonymized observations;
2. `mark_repeat_check_suspicious(features)` — deterministic threshold (2+ distinct check IDs on one day);
3. `score_anomalies(features)` — exploratory scikit-learn IsolationForest scoring (disabled on insufficient data);
4. `combine_review_signals(frame)` — report separate rule/anomaly sources.

The code does not write back to Apps Script or Google Sheets. Use as an experimental Strategy-pattern candidate only after a student-reviewed design and independent model evaluation. See [SUSPICIOUS_PATTERN_MODEL.md](../planning/SUSPICIOUS_PATTERN_MODEL.md).

## Configuration and secret handling

- Use `python/.env` for local secrets/settings; only commit the blank [`.env.example`](../../.env.example).
- Centralize environment access in a small `settings.py` configuration module; use `python-dotenv` to load it, then inject settings into the Google Sheets adapter. Keep model and feature modules independent of `.env` and Google credentials.
- For the Google Sheets API, use OAuth or service-account credential files in approved private storage outside Git. **Never store the actual Google account password.**
- Do not log/print secrets, embed them in Jupyter notebooks, or commit token caches and credential JSON.
- Follow [ENV_SETUP.md](../guides/ENV_SETUP.md) and review Git exclusions before commits.

## Development process: TDD

**Required for future changes:** define a testable behavior, write and run a deliberately failing synthetic test (**RED**), implement only the necessary behavior (**GREEN**), then improve structure with all tests still passing (**REFACTOR**). See [TDD_GUIDE.md](../guides/TDD_GUIDE.md).

Use protocol-based fake readers to test the pipeline without a Google connection, and test failure paths for missing credentials/schema changes without exposing secrets. Unit tests should dominate; a real Sheets API integration test is a separate, permission-controlled step. Keep TDD evidence and student acceptance separate.

The already committed `cleaning.py` and `test_cleaning.py` were not originally built using a verified RED → GREEN cycle. Baseline them before future changes; do not make retrospective TDD claims.

## Testability and controls

- Python **3.13** runtime for local environment, notebooks, and tests.
- Use standard GIL-enabled CPython initially; experimental free-threaded mode is not needed.
- No Google credentials in code, notebooks, public logs or tests.
- Reject or report missing/incomplete checks instead of assuming vehicle departure.
- No claim that anomaly score represents the probability of illegal parking.
- Run synthetic fixture tests without Google access; optionally test a separately authorized read-only connection after explicit approval.
- No automatic model-to-Sheet writeback, citations to fabricated sources, or automated ticketing/towing.

## Sources

- Python 3.13 release notes: https://docs.python.org/3/whatsnew/3.13.html
- Python typing protocols: https://docs.python.org/3/library/typing.html#typing.Protocol
- scikit-learn installation: https://scikit-learn.org/stable/install.html

The instructor's assessment requirements override this suggested design where they differ.
