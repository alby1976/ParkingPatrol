# Reusable Python code (planned)

**Target interpreter:** Python 3.13.

Each module should have **one cohesive job** and communicate using narrow, typed interfaces. Keep external APIs at the edge so the analysis code is loosely coupled. See [../ARCHITECTURE.md](../ARCHITECTURE.md).

Proposed modules (not yet implemented):
- `settings.py`: load ignored `python/.env` with `python-dotenv` and validate settings in one place (planned)
- `ports.py`: small structural Protocols describing approved data-reader and scoring interfaces
- `google_sheets_reader.py`: approved **read-only Google Sheets API** connection returning pandas DataFrames without writing data back
- `load_data.py`: private/local synthetic input for offline tests or development
- `validation.py`: schema, dates, duplicates and check completeness
- `features.py`: rolling features calculated without using future observations
- `pipeline.py`: orchestration using dependency injection, no hardwired Google service
- `modeling.py`: transparent baseline and optional introductory ML

All functions should have clear names and Google-style docstrings. Keep production Apps Script unchanged.
