# DATA120 Mini Capstone — Parking Pattern Analysis

This folder is for **DATA120 Python and machine-learning coursework**. It is separate from the operational Google Forms → Google Sheets → Apps Script parking workflow in the repository root.

## Project question

**Can patterns in manually observed parking sightings help staff prioritize vehicles for human review, without claiming that a vehicle is parked illegally?**

A staff member walks through a customer-only surface lot and records plates and observation date/time. Checks are intermittent; exact arrivals, departures, drivers, and customer status are not directly observed. Tenants, staff, and service providers are not permitted to use customer parking, but a plate's repeated appearance does not establish the driver's role or a parking violation.

## Data flow

```text
Staff walk-around
       |
Google Form → Google Sheet → Apps Script (existing production workflow)
                       |
            Restricted, approved export
                       |
              De-identify vehicle IDs
                       |
          Python / pandas (DATA120)
                       |
      Features → baseline → ML experiment
                       |
        Plots, evaluation, report
                       |
           Human-reviewed findings
```

**No automatic ticketing or towing from model output.** Findings are leads for verification, not evidence of misconduct.

## DATA120 deliverables

- [ ] Define the research question, objective, and success measures
- [ ] Confirm instructor expectations and allowed ML methods
- [ ] Prepare a de-identified or synthetic dataset
- [ ] Clean and explore sightings using pandas
- [ ] Engineer features without inventing departure times
- [ ] Establish an explainable, rules-based baseline
- [ ] Train an appropriate ML model, if reliable labels or sufficient anomaly data exist
- [ ] Evaluate with a time-based split and explicit limits
- [ ] Create readable charts, presentation, and final report

See [CAPSTONE_PLAN.md](CAPSTONE_PLAN.md) and [DATA_DICTIONARY.md](DATA_DICTIONARY.md).

## Getting started

1. Keep recording observations through the existing Google workflow; do not edit the production Apps Script for this assignment.
2. Start with **synthetic examples** until de-identification and export approval are established.
3. Create a Python virtual environment, then install packages:

   ```bash
   python -m venv .venv
   # Windows PowerShell:
   .venv\\Scripts\\python -m pip install -r python/requirements.txt
   ```

4. Add a notebook or script here when the dataset fields are confirmed.

## Data protection

Never commit raw licence plates, identifiable visit records, Google credentials, API keys, live spreadsheet exports, or mapping tables from pseudonymous IDs back to plates. Keep such material private and access-controlled. Because this is a **public repository**, use synthetic or carefully disclosure-reviewed aggregate results only. See the repository retention policy; the capstone export is not an excuse to keep production observations indefinitely.

## Important measurement limits

- One recorded plate means **seen at that check**, not an arrival.
- Several sightings do **not** prove continuous occupancy.
- Missing from a *complete* later check in the same area permits a **presumed absence** only, not an exact departure.
- Absence from an incomplete check, different area, or unobserved period is unknown.
- Frequency reflects staff checking schedules as well as parking behaviour.
- Without independently verified outcomes, **classification of actual offenders cannot be validated**. Consider anomaly detection or pattern clustering as exploratory learning rather than confirmed predictions.

## Course policies and coding-agent guidance

- [Academic integrity and course policies](ACADEMIC_INTEGRITY_AND_COURSE_POLICIES.md)
- [Generative AI use log](AI_USE_LOG.md)
- [Citations, copyright and privacy checklist](CITATIONS_COPYRIGHT_PRIVACY_CHECKLIST.md)
- [Instructions for AI coding agents](AGENT.md) (also discoverable through [AGENTS.md](AGENTS.md))

Assignment-specific instructor instructions control whether and how AI may assist with assessed work. The public repository is not a confidential assignment-submission space.
- [Git commit message template](COMMIT_TEMPLATE.txt) and [beginner's setup guide](GIT_COMMIT_GUIDE.md) for AI coding assistants
