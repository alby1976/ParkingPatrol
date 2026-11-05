# DATA120 Python Capstone — AI Agent Instructions (AGENTS.md)

Scope: All work in `python/`. These instructions **do not** authorize edits to the production `apps-script/` parking application.

## Purpose

Support a learner-led University of Calgary DATA120 mini capstone analyzing repeated parking sightings collected through the existing Google Forms → Google Sheets → Apps Script workflow. Focus on Python, pandas, explainable visualizations, cautious ML experiments, and a defensible report.

## Academic integrity: required first step

1. Read [ACADEMIC_INTEGRITY_AND_COURSE_POLICIES.md](ACADEMIC_INTEGRITY_AND_COURSE_POLICIES.md), [AI_USE_LOG.md](AI_USE_LOG.md), and [CITATIONS_COPYRIGHT_PRIVACY_CHECKLIST.md](CITATIONS_COPYRIGHT_PRIVACY_CHECKLIST.md) before suggesting assessment-related changes.
2. **Do not assume that AI-generated assignment work is permitted.** The course permits GAI only within each assignment's instructor-defined rules. Request/verify those rules before providing submission-ready AI-produced answers or interpretations. Planning, explanation, learning scaffolds, and code review must remain within permitted boundaries.
3. The student owns research choices, analysis, calculations, interpretation, and conclusions. Teach and explain; do not substitute GAI-generated judgment for the student's own work.
4. Log material AI assistance in `AI_USE_LOG.md`; do not falsely claim independent student authorship or claim that an AI-use log replaces formal disclosure/citation.
5. Cite permitted AI usage and third-party datasets, code, methods, references, visual assets, and reused personal work following assignment instructions (APA recommended in supplied policy). Check each citation against real sources. Never invent references.
6. Do not upload classmates' assignments or peer work to an AI system without explicit consent. Ask instructor if assignment-specific GAI permissions are unclear.

## Privacy, security, copyright

- This GitHub repository is **public**. Never commit actual licence plates, real timestamp/plate combinations, source Google Sheet exports, account details, API keys, credentials, reversible vehicle-to-plate mapping, or other sensitive personal/business data.
- Use synthetic data for examples and public tests. Treat de-identified/pseudonymous data as potentially re-identifiable; handle approved real data only in an access-controlled environment outside Git.
- Do not paste private production data or others' work into third-party GAI systems without necessary authorization.
- Check copyright and license before redistributing materials, code, figures, datasets, or course slides. Citation alone does not permit redistribution.
- Follow applicable data access, retention and deletion requirements; do not weaken the production app's protections.

## Scientific and statistical rules

- A manually recorded sighting establishes presence **at an observation**, not arrival, departure, continuous occupancy, noncustomer status, or a violation.
- Absence is meaningful only at the next **completed observation of the same area**; an unobserved interval is unknown.
- Account for staff check frequency, incomplete checks, duplicated plates in one check, jurisdictions, daylight saving time (America/Edmonton), and observation coverage.
- Never use operational statuses or AI-generated flags as independent ground-truth offender labels.
- Start with an explainable rules baseline; use supervised classification only with independently verified labels, or clearly frame clustering/anomaly detection as exploratory.
- Evaluate with chronology-aware splits, leakage checks, and honest discussion of false positives and bias. Never invent prediction accuracy.
- No model, rule, or GAI output may automatically order, justify, or trigger ticketing/towing. Require independent human verification and applicable authorization.

## Repository workflow

- Keep changes confined to `python/` unless the student explicitly authorizes broader integration.
- Do not modify or deploy `apps-script/` as part of routine DATA120 development.
- Prefer small, reviewable commits with clear messages; do not overwrite work.
- For all changes under `python/`, draft commit messages using [COMMIT_TEMPLATE.txt](COMMIT_TEMPLATE.txt) and the [Git commit guide](GIT_COMMIT_GUIDE.md). Inspect the actual staged diff; report test results truthfully; specify AI assistance accurately; never fabricate test results, user approval, or course compliance. Show the student the proposed message and changes for review before committing. The template is not a substitute for formal course AI citation/disclosure.
- Keep project documentation and the [DATA_DICTIONARY.md](DATA_DICTIONARY.md) updated when fields or assumptions change.
- Add lightweight tests for important data cleaning and feature calculations. Do not claim a test was run unless it was actually run.
- Prefer `pandas`, `numpy`, `matplotlib`, `scikit-learn` and standard-library modules; pin or document new dependencies.
- In examples use tiny synthetic datasets, descriptive variable names, type hints where useful, and clear Google-style docstrings.
- Separate learning experiments from any production enforcement workflow.

## Teaching and accessibility

The student prefers short, numbered, practical "dummies guide" steps, diagrams, minimal reading, and hands-on examples. Introduce one concept at a time; explain what each command does and show expected outputs. Make charts readable and describe the takeaway without pretending that plots establish guilt.

## Priorities

1. Confirm course/assignment AI permission.
2. Map actual permitted Google Sheet field names **without exposing real records**.
3. Design synthetic examples and a safe import boundary.
4. Explore data and build explainable features.
5. Compare justified model experiments to a transparent baseline.
6. Document methods, limitations, sources, AI use, and student-driven conclusions.

See [README.md](README.md) and [CAPSTONE_PLAN.md](CAPSTONE_PLAN.md) for current project scope.

## Instruction precedence

Applicable University of Calgary course and assignment requirements take precedence over this file. This file is the single canonical agent instruction document for `python/`.
