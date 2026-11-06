# Reusable Python code (planned)

**Target interpreter:** Python 3.13.

Each module should have **one cohesive job** and communicate using narrow, typed interfaces. Keep external APIs at the edge so the analysis code is loosely coupled. See [../ARCHITECTURE.md](../docs/architecture/ARCHITECTURE.md).

Module inventory (items marked planned are not implemented):
- `settings.py`: load ignored `python/.env` with `python-dotenv` and validate settings in one place (planned)
- `ports.py`: small structural Protocols describing approved data-reader and scoring interfaces
- `google_sheets_reader.py`: approved **read-only Google Sheets API** connection returning pandas DataFrames without writing data back
- `load_data.py`: private/local synthetic input for offline tests or development
- `cleaning.py`: **implemented** pure pandas normalization of approved pseudonymous observations and check rows; quarantines invalid data into non-sensitive issue codes
- `validation.py`: additional schema/quality validation (planned)
- `features.py`: rolling features calculated without using future observations
- `pipeline.py`: orchestration using dependency injection, no hardwired Google service
- `pattern_detection.py`: **implemented** same-day repeat-check review rule, observation features, and exploratory IsolationForest anomaly scoring
- `modeling.py`: other scoring strategies (planned)

All functions should have clear names and Google-style docstrings. Keep production Apps Script unchanged.

Run synthetic tests with `python -m pytest python/tests/test_cleaning.py` from the repository root, using the Python 3.13 environment. No Google connection is required.
