# Reusable Python code (planned)

Proposed modules (not yet implemented):
- `google_sheets_reader.py`: approved **read-only Google Sheets API** connection returning pandas DataFrames without writing data back
- `load_data.py`: private/local synthetic input for offline tests or development
- `validation.py`: schema, dates, duplicates and check completeness
- `features.py`: rolling features calculated without using future observations
- `modeling.py`: transparent baseline and optional introductory ML

All functions should have clear names and Google-style docstrings. Keep production Apps Script unchanged.
