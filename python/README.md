# DATA120 Mini Capstone — Parking Observation Patterns

> **Status:** Planning material generated with AI; **student reading and acceptance pending**. Course-specific AI permission also needs to be confirmed. See [AI_USE_LOG.md](AI_USE_LOG.md).

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
├── CAPSTONE_PLAN.md          ← question, hypotheses, method, evaluation
├── DATA_DICTIONARY.md        ← original/proposed data fields and features
├── requirements.txt          ← initial dependencies
├── AGENTS.md                 ← AI-agent and academic-integrity instructions
├── AI_USE_LOG.md             ← AI contribution + review/acceptance record
├── notebooks/                ← exploratory and modeling notebooks (future)
├── src/                      ← Sheets connector + Python ML logic (future)
├── tests/                    ← synthetic tests for feature calculations (future)
└── reports/                  ← public-safe figures/report outline (future)
```

Other governance documents and instructions already in this directory remain applicable. Folder-specific README files keep the proposed folders in Git; no model or private dataset has been added.

## First-time setup from the repository root

```powershell
git pull origin main
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r python/requirements.txt
.\.venv\Scripts\python.exe -m jupyter lab
```

Using `py -3` requires the Windows Python launcher; if unavailable use `python -m venv .venv`. Python **3.11 or 3.12** is a conservative course setup target (check instructor's environment). The local `.venv` is ignored by Git.

## Planned learning order

1. **Identify real Sheet column names without sharing records.** Write a source-to-dictionary mapping.
2. **Implement a read-only Google Sheets API connector**, after consent, secure credentials, privacy controls, and student approval; load data into pandas in memory. Use restricted scopes and least privilege. Do not store credentials in Git.
3. **Create synthetic data** with completed and incomplete checks.
4. **Explore with pandas**: counts by date, area, hour, and inspection frequency.
5. **Build observation-aware features** such as distinct days seen.
6. **Compare a transparent baseline** against an exploratory unsupervised ML method (if data volume supports it).
6. **Evaluate stability and practical interpretability**, discuss limitations, and prepare a student-authored report.

See [CAPSTONE_PLAN.md](CAPSTONE_PLAN.md) for details. Model type is provisional until data quality and course assessment rules are confirmed.

## Privacy and academic integrity

This repository is **public**: do not commit raw plates, time-stamped operational exports, private vehicle-ID mappings, credentials, or confidential evidence. Use synthetic demo records. Any real data must remain in approved private storage, outside Git, with authorized access and appropriate retention.

The University of Calgary allows GAI only as specified for each assessment. AI output supports learning, not a substitute for the student's analysis. All material assistance must be logged and cited as required. See [ACADEMIC_INTEGRITY_AND_COURSE_POLICIES.md](ACADEMIC_INTEGRITY_AND_COURSE_POLICIES.md), [AGENTS.md](AGENTS.md), and [AI_REVIEW_GATE_GUIDE.md](AI_REVIEW_GATE_GUIDE.md).

No AI result will authorize a ticket, tow, or allegation of parking misconduct.

## Reference documents

- [Generative AI use log](AI_USE_LOG.md)
- [AI logging instructions](AI_LOGGING_GUIDE.md)
- [AI reading and acceptance checkpoint](AI_REVIEW_GATE_GUIDE.md)
- [Citations, copyright and privacy checklist](CITATIONS_COPYRIGHT_PRIVACY_CHECKLIST.md)
- [Git commit message template](COMMIT_TEMPLATE.txt) and [guide](GIT_COMMIT_GUIDE.md)
