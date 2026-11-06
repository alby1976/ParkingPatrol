# DATA120 Mini Capstone — Parking Observation Patterns

> **Status:** Planning material generated with AI; **student reading and acceptance pending**. Course-specific AI permission also needs to be confirmed. See [AI_USE_LOG.md](docs/ai/AI_USE_LOG.md).

## In one sentence

Use Python and machine learning to examine **unusual patterns in manually observed vehicle sightings**, while never claiming that a repeated sighting proves unauthorized parking.

**The planned Python model will connect to Google Sheets to retrieve authorized observation data using a read-only connection.** This link is a future implementation, not currently live. The Python model will not alter the production Google Sheet or deploy to Apps Script.

This folder is a **coursework sandbox**. The working Google Forms → Google Sheets → Apps Script parking patrol system remains in `apps-script/` and is not modified by this capstone.

## Research question

**To what extent can features derived from intermittent, manually recorded vehicle sightings identify unusual repeat-sighting patterns, compared with a simple transparent rule, after accounting for how often staff inspect the parking areas?**

This is a question about **pattern discovery and review prioritization**, not predicting actual violations unless trustworthy, independently verified outcome labels become available.

## How the data travels

```text
STAFF walk through parking lot
                 |
    Google Form observations
                 |
     Google Sheet + Apps Script         [existing operational system]
                 |
   AUTHORIZED read-only Sheets API
                 |
     Restricted access to Sheet
                 |
   Private Python data connector        [new DATA120 component]
                 |
    Pseudonymize / validate locally
                 |
      Python DATA120 workspace          [separate research workflow]
                 |
   pandas → charts → features → ML
                 |
   validation → report → presentation
```

**Important:** The parking observations do not record actual arrival or departure times. A missing observation is not always an absence. Staff check frequency changes how often a plate can be seen.

## Directory map

```text
python/
├── README.md                 ← start here
├── docs/                     ← documents grouped by subject
│   ├── planning/             ← research and data dictionary
│   ├── architecture/         ← design and interfaces
│   ├── guides/               ← setup, Git, TDD
│   ├── policies/             ← academic integrity and privacy
│   └── ai/                   ← AI disclosures and approval logs
├── requirements.txt          ← initial dependencies
├── .env.example              ← safe template only (tracked)
├── .env                      ← local secrets (ignored, never committed)
├── AGENTS.md                 ← AI-agent and academic-integrity instructions
├── notebooks/                ← exploratory and modeling notebooks (future)
├── src/                      ← cleaning.py implemented; Sheets/ML modules planned
├── tests/                    ← synthetic normalization tests implemented
└── reports/                  ← public-safe figures/report outline (future)
```

Other governance documents and instructions already in this directory remain applicable. Folder-specific README files keep the proposed folders in Git; no model or private dataset has been added.

## First-time setup from the repository root

```powershell
git pull origin main
Copy-Item python/.env.example python/.env
# Edit python/.env locally; never put credentials in Git
py -3.13 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r python/requirements.txt
.\.venv\Scripts\python.exe -m jupyter lab
```

Use **CPython 3.13** for all local development, notebooks and tests. `py -3.13` requires the Windows Python launcher and an installed Python 3.13; alternatively invoke the installed 3.13 interpreter explicitly. Check `.venv\\Scripts\\python.exe --version` before installing dependencies. The local `.venv` is ignored by Git.

Read [ENV_SETUP.md](docs/guides/ENV_SETUP.md) before adding any Google Sheets credentials. The `.env.example` contains no secrets; `python/.env` and real credential JSON files are excluded from Git. Do not use your Google account password to authenticate the Sheets API.

## Object-oriented architecture

Use **low coupling and high cohesion** (assuming "high collision" meant "high cohesion"). Each small class/module has one clear responsibility, communicates through well-defined types and protocols, and can be replaced/tested independently. Avoid unnecessary layers for a mini capstone.

- **Repository/Adapter:** Google Sheets reader and synthetic fixture reader implement a shared read interface.
- **Dependency injection:** Supply a reader to the analysis service, rather than importing a concrete Google API client into every module.
- **Strategy:** Swap a transparent rules baseline and an exploratory anomaly detector behind a narrow model interface.
- **Pipeline:** Explicit validate → transform → features → model → evaluation steps, with immutable configuration where appropriate.

See [ARCHITECTURE.md](docs/architecture/ARCHITECTURE.md) for a diagram and design principles. These are design goals; no production integration is implemented yet.

## Suspicious checks and unsupervised pattern exploration

- **Deterministic rule:** pseudonymous vehicle recorded in **two or more distinct checks on the same Edmonton-local day** becomes `rule_suspicious` for *review*. Duplicate entries within one check do not count as two events.
- **Unsupervised experiment:** IsolationForest may mark additional unusual vehicle-day feature combinations as `anomaly_suspicious`. This is not a calibrated probability of misuse.
- **Combined review view:** `flag_source` identifies `rule`, `anomaly`, or `rule+anomaly`; no model output triggers enforcement.
- Implemented in [src/pattern_detection.py](src/pattern_detection.py), tested with synthetic cases in [tests/test_pattern_detection.py](tests/test_pattern_detection.py). No live Google Sheets connection or deployment.
- Read [the pattern-model design](docs/planning/SUSPICIOUS_PATTERN_MODEL.md) and confirm the proposed interpretation of an "event" as one distinct survey/check.

## Human verification and on-site actions

A vehicle that triggers the rule or anomaly review indicator is **suspicious only**. An authorized human verifies whether a parking violation actually occurred. If verified, the vehicle may be recorded as **blacklisted**; any ticket or tag issued on site is a separate staff action with its own timestamp and reference. No Python module or ML model issues tickets or tags automatically.

See [Human Verification Workflow](docs/planning/HUMAN_VERIFICATION_WORKFLOW.md) and [verification.py](src/verification.py) for the proposed offline record design (not deployed).

## Test-driven development: required

All **future** Python feature work and bug fixes should use **RED → GREEN → REFACTOR**: first write and actually run a failing synthetic test, then write minimal implementation, then improve the code while tests still pass. Keep documented evidence of each phase and review results before advancing. See [TDD_GUIDE.md](docs/guides/TDD_GUIDE.md). The already-created cleaning module was not developed with verified TDD, so it is not retroactively described that way.

## Deadlines and synthetic data

- **Presentation:** Tuesday, December 8, 2026.
- **Submission:** Friday, December 11, 2026.
- **Internal analysis freeze:** December 4, 2026.
- [Approved milestone schedule](docs/planning/CAPSTONE_PLAN.md): **no work on Sundays**, prioritize **LOF + Isolation Forest**, and treat kNN as an optional stretch goal. Decide by **November 21** whether to drop kNN. Start presentation slides during the first week.
- [Synthetic data generator guide](docs/planning/SYNTHETIC_DATA_GUIDE.md).

Generate fictional observations without accessing Google Sheets:

```powershell
.\\.venv\\Scripts\\python.exe python/src/synthetic_data.py --days 10 --seed 120
.\\.venv\\Scripts\\python.exe -m pytest python/tests/test_synthetic_data.py -q
```

Synthetic 45/90-day examples support software testing and exploratory demonstrations, not claims about actual parking violations. Output stays in the Git-ignored `python/generated/` folder.

## Guided sprints with ChatGPT

Start with the [31-session calendar](docs/planning/GUIDED_SPRINT_SESSIONS.md), use the [ChatGPT coaching instructions](docs/planning/CHATGPT_SPRINT_COACH.md), and update the [sprint progress tracker](docs/planning/SPRINT_PROGRESS.md) with actual outcomes. Sundays are always free. ChatGPT should walk through one action at a time, use TDD, log AI assistance, and obtain explicit reading and acceptance before the next substantive step.

## Planned learning order

1. **Identify real Sheet column names without sharing records.** Write a source-to-dictionary mapping.
2. **Implement a read-only Google Sheets API connector**, after consent, secure credentials, privacy controls, and student approval; load data into pandas in memory. Use restricted scopes and least privilege. Do not store credentials in Git.
3. **Clean and normalize synthetic checks/sightings** using [src/cleaning.py](src/cleaning.py), then review the issue report before deciding what to exclude. Run `python -m pytest python/tests/test_cleaning.py`.
4. **Create synthetic data** with completed and incomplete checks.
5. **Explore with pandas**: counts by date, area, hour, and inspection frequency.
6. **Build observation-aware features** such as distinct days seen.
7. **Compare a transparent baseline** against an exploratory unsupervised ML method (if data volume supports it).
8. **Evaluate stability and practical interpretability**, discuss limitations, and prepare a student-authored report.

See [CAPSTONE_PLAN.md](docs/planning/CAPSTONE_PLAN.md) for details. Model type is provisional until data quality and course assessment rules are confirmed.

## Privacy and academic integrity

This repository is **public**: do not commit raw plates, time-stamped operational exports, private vehicle-ID mappings, credentials, or confidential evidence. Use synthetic demo records. Any real data must remain in approved private storage, outside Git, with authorized access and appropriate retention.

The University of Calgary allows GAI only as specified for each assessment. AI output supports learning, not a substitute for the student's analysis. All material assistance must be logged and cited as required. See [ACADEMIC_INTEGRITY_AND_COURSE_POLICIES.md](docs/policies/ACADEMIC_INTEGRITY_AND_COURSE_POLICIES.md), [AGENTS.md](AGENTS.md), and [AI_REVIEW_GATE_GUIDE.md](docs/ai/AI_REVIEW_GATE_GUIDE.md).

No AI result will authorize a ticket, tow, or allegation of parking misconduct.

## Reference documents

- [Generative AI use log](docs/ai/AI_USE_LOG.md)
- [AI logging instructions](docs/ai/AI_LOGGING_GUIDE.md)
- [AI reading and acceptance checkpoint](docs/ai/AI_REVIEW_GATE_GUIDE.md)
- [Citations, copyright and privacy checklist](docs/policies/CITATIONS_COPYRIGHT_PRIVACY_CHECKLIST.md)
- [Local .env and Google Sheets credential setup](docs/guides/ENV_SETUP.md)
- [Test-driven development guide](docs/guides/TDD_GUIDE.md)
- [Git commit message template](COMMIT_TEMPLATE.txt) and [guide](docs/guides/GIT_COMMIT_GUIDE.md)
