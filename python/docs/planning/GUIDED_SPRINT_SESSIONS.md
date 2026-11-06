# DATA120 Guided Sprint Calendar

**Presentation:** Tuesday Dec 8, 2026. **Submission:** Friday Dec 11. **Internal analysis freeze:** Friday Dec 4.

**Working rhythm:** weekdays 60–90 minutes, Saturdays 2–3 hours, Sundays OFF (Nov 8, 15, 22, 29 and Dec 6). This is a proposal for student review, not a record of completed work.

## Session format

Begin each session by saying to ChatGPT: **"Guide me through DATA120 session SXX, one step at a time, using the GitHub sprint calendar."** Follow [CHATGPT_SPRINT_COACH.md](CHATGPT_SPRINT_COACH.md) for the reusable prompt and approval rules.

Each session: 5 minutes recall → 10 minutes define done → up to 55 minutes hands-on TDD/research → 10 minutes review/commit → stop for human reading and acceptance. Saturday: two focus blocks with a break, followed by slide work.

## Sprint A: Foundation + slides (Nov 6–14)

| ID | Date | Task | Proof of done |
|---|---|---|---|
| S01 | Fri Nov 6 | Verify Python 3.13, local Git checkout and secrets exclusion | Version commands and safe Git status recorded |
| S02 | Sat Nov 7 | Run baseline tests and synthetic 10-day generator; draft 8-slide skeleton | Test outputs and slide outline |
| — | Sun Nov 8 | **REST** | No project work |
| S03 | Mon Nov 9 | Map private Google Sheet column **headers only** to data dictionary | Header mapping, no private rows |
| S04 | Tue Nov 10 | RED–GREEN–REFACTOR for fake read-only Sheets adapter | Synthetic test evidence |
| S05 | Wed Nov 11 | Test invalid credentials, changed headers, API errors | Focused regression outcomes |
| S06 | Thu Nov 12 | Authorized read-only connection, or synthetic fallback if not approved | Non-identifying schema/count summary |
| S07 | Fri Nov 13 | Clean/normalize tests and slides 1–2 | Results and first slides |
| S08 | Sat Nov 14 | Synthetic data through cleaning and features; slide 3 | Reproducible walkthrough |

## Sprint B: Baseline + two ML models (Nov 16–21)

| ID | Date | Task | Proof of done |
|---|---|---|---|
| — | Sun Nov 15 | **REST** | No project work |
| S09 | Mon Nov 16 | Test-first one-vehicle/analysis-window features, accounting for completed inspections | Feature schema + tests |
| S10 | Tue Nov 17 | Test 2-distinct-check same-day suspicious baseline | Synthetic examples and chart |
| S11 | Wed Nov 18 | Implement/test LOF with small-sample safeguards | LOF test results |
| S12 | Thu Nov 19 | Compare Isolation Forest using exactly the same features | Comparable outputs |
| S13 | Fri Nov 20 | Combine rule, LOF, Isolation Forest comparisons; slides 4–6 | Comparison chart and slides |
| S14 | Sat Nov 21 | **Scope gate:** drop optional kNN if behind; if needed prioritize baseline + one reliable model. Rehearse slides | Recorded scope decision |

## Sprint C: Evaluation + charts (Nov 23–28)

| ID | Date | Task | Proof of done |
|---|---|---|---|
| — | Sun Nov 22 | **REST** | No project work |
| S15 | Mon Nov 23 | Privately audit actual observation days and completed checks | Aggregate data-quality counts |
| S16 | Tue Nov 24 | Evaluate on later observations if possible; check temporal leakage | Evaluation limitations documented |
| S17 | Wed Nov 25 | Test LOF neighbor choice and Isolation Forest parameter sensitivity | Stability plot |
| S18 | Thu Nov 26 | Compare to independently verified human outcomes only if authorized | Qualified review analysis or honest limitation |
| S19 | Fri Nov 27 | Create 2–3 clearly labeled, public-safe figures; slide 7 | Checked charts |
| S20 | Sat Nov 28 | Write your interpretation, slide 8 and first full slide walkthrough | Complete first presentation draft |
| — | Sun Nov 29 | **REST** | No project work |

## Sprint D: Finish presentation (Nov 30–Dec 7)

| ID | Date | Task | Proof of done |
|---|---|---|---|
| S21 | Mon Nov 30 | Check rubric, citations, permitted AI use and attribution | Submission checklist |
| S22 | Tue Dec 1 | Simplify slides to one concept per visual | Legible slide deck |
| S23 | Wed Dec 2 | Run appropriate regression tests; verify reproducibility | Actual command outputs |
| S24 | Thu Dec 3 | Timed verbal rehearsal; create static demo screenshots | Rehearsal notes and backups |
| S25 | Fri Dec 4 | **FREEZE** model, results, charts, presentation version | Recorded presentation version |
| S26 | Sat Dec 5 | Full timed presentation + Q&A practice | Dry-run completion |
| — | Sun Dec 6 | **REST** | No project work |
| S27 | Mon Dec 7 | Final rehearsal and backup check; no new models | Presentation go/no-go checklist |

## Presentation and submission

| ID | Date | Task |
|---|---|---|
| S28 | Tue Dec 8 | Deliver presentation; capture questions and feedback |
| S29 | Wed Dec 9 | Incorporate appropriate feedback with regression tests |
| S30 | Thu Dec 10 | Final report, documentation, privacy, APA and AI disclosure audit |
| S31 | Fri Dec 11 | Submit by the instructor's required time; retain confirmation |

## Hard limits and fallback

The real dataset is approximately 10 days from a 38-space lot, normally inspected once or twice per day. Synthetic 45/90-day data is for testing and demonstrations and **must never be represented as actual collected observations**. Prioritize two-check rule, LOF and Isolation Forest; kNN is optional. If behind on Nov 21, drop kNN. If still behind, prioritize one well-evaluated unsupervised model plus baseline rather than three incomplete methods.

A suspicious flag is only a human review signal, not an actual violation. No model triggers blacklisting, ticketing or towing. Keep real plates, credentials and raw observations out of public Git.

See the [Capstone Plan](CAPSTONE_PLAN.md) and [Sprint Progress Tracker](SPRINT_PROGRESS.md).
