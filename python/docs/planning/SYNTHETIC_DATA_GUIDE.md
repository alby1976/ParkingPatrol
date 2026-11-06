# DATA120 — Generating synthetic parking data (Python 3.13)

**Purpose:** Practice pandas, data cleaning, feature engineering, Isolation Forest, and TDD without sharing or altering real customer licence plates. This is entirely fictional data, not evidence of parking misconduct.

## Model of the real observation process

- Maximum **38 spaces** per inspection.
- Each calendar date has **one or two survey rounds** (default approximately 25% one-check days).
- Example inspection times are 9:00 AM and 3:00 PM in `America/Edmonton`.
- Some fictional vehicles recur across rounds/days; others vary.
- Occupancy is a **fictional adjustable probability**, not measured occupancy.
- Some checks may be incomplete. The generator preserves their completion status.
- A sighting is just a vehicle observed during that check. It is **not** a parking arrival, departure, stay duration, actual customer status, or offence.
- Synthetic IDs like `SYN_0001` are made-up identifiers, not real plates.
- Repeating records represent a *pattern*, not an independent ground-truth violation label.

## 1. Install Python dependencies

From the repository root in Windows PowerShell:

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r python/requirements.txt
```

If `.venv` already exists, do not recreate it; verify its Python version:

```powershell
.\.venv\Scripts\python.exe --version
```

## 2. Generate a 10-day pilot (similar duration to your current real history)

```powershell
.\.venv\Scripts\python.exe python/src/synthetic_data.py --days 10 --seed 120
```

The default results are saved locally to `python/generated/`:
- `synthetic_checks.csv`: `check_id`, `area_id`, `check_at`, `check_complete`
- `synthetic_sightings.csv`: `vehicle_id`, `check_id`, `area_id`, `observed_at`

This folder is deliberately ignored by Git. Do not commit generated row-level data even though it is fictional: keeping all data exports out of the public repo reduces accidental mixing with real data.

## 3. Generate 45 or 90 days to test future scenarios

```powershell
.\.venv\Scripts\python.exe python/src/synthetic_data.py --days 45 --seed 120
.\.venv\Scripts\python.exe python/src/synthetic_data.py --days 90 --seed 120
```

Each command **overwrites** the two CSVs in `python/generated/`. Supply a different `--output` directory if you want to preserve multiple scenario runs; keep that folder outside Git. A fixed `--seed` reproduces the same scenario.

Generate a second scenario with fewer checks and lower fictional occupancy:

```powershell
.\.venv\Scripts\python.exe python/src/synthetic_data.py --days 45 --seed 121 --one-check-probability 0.40 --occupancy-rate 0.50
```

The `capacity` defaults to 38 and the code refuses values above 38.

## 4. Run TDD tests

```powershell
.\.venv\Scripts\python.exe -m pytest python/tests/test_synthetic_data.py -q
.\.venv\Scripts\python.exe -m pytest python/tests -q
```

Existing tests check deterministic output for the same seed, 38-space capacity, one/two checks per day, Edmonton timestamps, duplicate-free check IDs, empty surveys, recurring synthetic vehicles and invalid configuration. **Do not claim the entire test suite passed unless it was run.**

## 5. Use the synthetic files with pandas

From the repository root:

```python
import pandas as pd

checks = pd.read_csv("python/generated/synthetic_checks.csv")
sightings = pd.read_csv("python/generated/synthetic_sightings.csv")
print(checks.head())
print(sightings.head())
```

Or import the generator directly:

```python
from pathlib import Path
import sys
sys.path.insert(0, str(Path("python/src").resolve()))
from synthetic_data import SyntheticConfig, generate_synthetic_data
data = generate_synthetic_data(SyntheticConfig(days=45, seed=120))
checks, sightings = data.checks, data.sightings
```

The direct Python API provides timestamp-aware DataFrames ready to send to the approved `cleaning.normalize_observations` function; reading CSV requires parsing datetime columns first.

## 6. Distinguish synthetic and real data in the presentation

**Never combine fictitious observations with your actual 10 days and present the result as a real-world sample.** Label every plot `SYNTHETIC` or `REAL (approved, de-identified)`. The simulation assumptions are chosen for teaching; they cannot validate how frequently actual customers violate parking rules or whether Isolation Forest accurately detects such violations. A useful capstone can show TDD, a rules baseline, anomaly-detection demonstrations, and transparent limitations without making unsupported accuracy claims.

## Test-driven development evidence for this addition

- **RED:** Focused pytest initially failed because the `synthetic_data` module did not exist.
- **GREEN:** After implementing the generator, one test failed because the test incorrectly assumed no incomplete checks under default settings. The test was corrected to set `incomplete_probability=0` explicitly; six focused tests then passed with Python 3.13.5 and pandas 2.2.3.
- **REFACTOR:** Documentation and code clarity were improved; full repository regression tests and GitHub CI are not verified here.
- **Example local run:** 10 days, seed 120: 18 checks and 448 fictional sighting rows, not real observations.

For the project timeline, see [CAPSTONE_PLAN.md](CAPSTONE_PLAN.md).
