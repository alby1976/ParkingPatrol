# DATA120 Guided Sprint Calendar — Recovery Revision (November 16, 2026)

**Presentation:** Tuesday December 8, 2026. **Final submission:** Friday December 11, 2026. **Internal analysis and figure freeze:** Friday December 4, 2026.

**Status:** Revised implementation proposal awaiting student reading and acceptance; dates are targets, not claims of completion. Retain the original session IDs S01–S31 for issue traceability.

**Working rhythm:** weekdays 60–90 minutes, Saturdays 2–3 hours, Sundays OFF (November 8, 15, 22, 29 and December 6).

## How to use this plan

Start each session: **"Guide me through DATA120 session SXX, one step at a time, using the recovery sprint calendar."** Follow [CHATGPT_SPRINT_COACH.md](CHATGPT_SPRINT_COACH.md). Use one small action per message and ask the student to paste real terminal results.

Session rhythm: recall → define proof of done → one test-first coding task or analysis step → review/commit → explicit student reading and acceptance. Do not assign a second substantive task until the approval gate is satisfied.

## Verified starting point (November 15)

- **S01 completed and accepted:** Python 3.13.14 environment and safe Git checks.
- **S02 core artifacts verified and outline accepted:** 29 previously reported passing Python tests; synthetic 10-day run created 18 checks and 448 fictional sightings; eight-slide Markdown outline committed as `f8857eb` and accepted November 15. Check issue #2's remaining criteria before closing.
- **S03–S08:** no complete session evidence in the tracker. This is a verification gap, not proof that all code is absent. Audit existing cleaning, detection and tests before writing anything new.
- **Existing code:** cleaning, synthetic generation, same-day rule and exploratory Isolation Forest code exist; they must be tested on the shared comparison features before claiming a finished model.
- **No verified:** authorized live Google Sheets import, LOF comparison, evaluated model findings, charts, final slide deck, or prospective accuracy. The extra per-plate-status work is not on the capstone critical path.

## Sprint A — Historical baseline and recovered prerequisites (November 6–14)

| ID | Original date | Original task | Recovery disposition |
| --- | --- | --- | --- |
| S01 | Fri Nov 6 | Python, Git, secrets exclusion | **Completed/accepted** |
| S02 | Sat Nov 7 | Tests, fictional generator, eight-slide outline | **Core outputs verified; outline accepted.** Review #2 closure criteria separately |
| S03 | Mon Nov 9 | Headers-only Google Sheets data dictionary | **Carry forward as a bounded schema check**; no private rows |
| S04 | Tue Nov 10 | Fake read-only adapter TDD | **Defer unless needed**; do not block synthetic ML |
| S05 | Wed Nov 11 | Bad credentials/schema/API errors | **Defer with adapter**; remains unverified |
| S06 | Thu Nov 12 | Authorized live read-only import or synthetic fallback | **Use synthetic fallback by default** until authorization is verified |
| S07 | Fri Nov 13 | Cleaning tests and early slides | **Audit existing cleaning/tests**; early slide outline done |
| S08 | Sat Nov 14 | Fictional cleaning/features walkthrough | **Carry forward to S09** if no evidence |
| — | Sundays Nov 8, 15 | **REST** | No make-up work |

## Sprint B — Recovery plus baseline and models (November 16–21)

| ID | Date | Revised task | Proof of done |
| --- | --- | --- | --- |
| S09 | **Mon Nov 16** | **Recovery gate:** inspect current src/tests, issue #2–#5 evidence; confirm or mark S03–S08 gaps. Audit cleaning and shared vehicle/check feature schema using synthetic records only | Short gap checklist; real `pytest` baseline output if run; specific next coding target; no private records |
| S10 | **Tue Nov 17** | Test-first shared vehicle-by-analysis-window features (unique check sightings, distinct observed dates, completed comparable checks, observed fraction); ensure time zone and missing-check logic | RED/GREEN/REFACTOR evidence, deterministic synthetic feature table |
| S11 | **Wed Nov 18** | Verify 2-distinct-check same-local-day rule and deduplication on those data, then implement/test LOF with valid small-sample neighbor bounds | Focused tests; rule and LOF scoring evidence |
| S12 | **Thu Nov 19** | Run/test existing Isolation Forest using the same feature rows as LOF; handle degenerate and small datasets | Reproducible side-by-side scores/flags; test evidence |
| S13 | **Fri Nov 20** | Produce initial rule-vs-LOF-vs-Isolation Forest table and one labeled comparison chart; replace presentation Slides 4–6 placeholders only with verified methods | Public-safe synthetic demonstration and documented limitations |
| S14 | **Sat Nov 21** | **Hard scope gate:** assess actual evidence, keep kNN strictly optional and only start it after the baseline, LOF, Isolation Forest, tests and core presentation evidence are complete; decide whether to retain two ML methods or baseline + one reliable model; rehearse an early walkthrough | Recorded scope decision, unblocked work plan, student approval |

**Nov 16–21 fallback:** If the shared feature table is delayed, prioritize a correctly tested two-check baseline and **one** reproducible unsupervised experiment. Do not invent LOF results or force a second model into the presentation. Do not use live Sheet access as a prerequisite for synthetic model research.

## Sprint C — Evidence, evaluation, figures and first deck (November 23–28)

| ID | Date | Revised task | Proof of done |
| --- | --- | --- | --- |
| S15 | Mon Nov 23 | Audit observation/check coverage, publicly using aggregates only; if live access remains unapproved, evaluate fictional records and explicitly label them | Coverage/inspection-frequency table, clear data provenance |
| S16 | Tue Nov 24 | Evaluate temporal leakage, incomplete checks and later-period stability when observations suffice | Date-bounded analysis and limitations; no fabricated accuracy |
| S17 | Wed Nov 25 | Model sensitivity: LOF neighbors if LOF retained; Isolation Forest settings if retained; assess ranking stability | Small public-safe sensitivity figure or documented insufficiency |
| S18 | Thu Nov 26 | Check whether independently verified historical tickets are available and authorized for evaluation; otherwise write the absence-of-ground-truth limitation | Approval decision or clear limitation; historical status ≠ new violation |
| S19 | Fri Nov 27 | Complete 2–3 privacy-safe figures, with synthetic versus real sources clearly separated; replace Slide 7 placeholder | Verified charts with captions and axes |
| S20 | Sat Nov 28 | Student writes findings, limitations and Slide 8 conclusions; assemble first full visual slide deck and rehearse walkthrough | Complete draft deck, cited actual outcomes and student interpretation |
| — | Sun Nov 22, Nov 29 | **REST** | No project work |

## Sprint D — Reproducibility and presentation readiness (November 30–December 7)

| ID | Date | Revised task | Proof of done |
| --- | --- | --- | --- |
| S21 | Mon Nov 30 | Verify assignment rubric, APA/AI requirements and authorized data use; resolve outstanding privacy/permission decisions | Checklist; unconfirmed rules explicitly marked |
| S22 | Tue Dec 1 | Make slides accessible and visual; one concept per slide and presenter notes | Legible presentation draft |
| S23 | Wed Dec 2 | Full regression, deterministic data demo, requirements and instructions verification | Actual command/output evidence, no implied test passes |
| S24 | Thu Dec 3 | Timed rehearsal, screenshots and offline fallback | Timed run and backup |
| S25 | **Fri Dec 4** | **FREEZE:** models, figures, conclusions, slides and reproducible revision | Saved version/commit and approved freeze checklist |
| S26 | Sat Dec 5 | Full presentation and Q&A rehearsal | Dry-run notes |
| — | Sun Dec 6 | **REST** | No course work |
| S27 | Mon Dec 7 | Final backup and rehearsal only; no new experiments | Go/no-go checklist |

## Delivery (December 8–11)

| ID | Date | Work |
| --- | --- | --- |
| S28 | Tue Dec 8 | Present verified outcomes and limitations |
| S29 | Wed Dec 9 | Record feedback, make only justified changes with regressions |
| S30 | Thu Dec 10 | Report, README, privacy, citations and AI use disclosure audit |
| S31 | Fri Dec 11 | Submit by actual course deadline and retain submission confirmation |

## Nonnegotiable safeguards and prioritization

1. **Critical path:** synthetic data → cleaned comparable inspections → shared vehicle-level features → same-day rule → at least one genuinely evaluated ML model → charts → student conclusions → rehearsed presentation.
2. **Optional/off critical path:** kNN **distance-based anomaly scoring** is an accepted stretch goal only if time remains after the baseline, LOF, Isolation Forest, evaluation and presentation deliverables. Also defer new Apps Script deployment, automated write-back/towing, full live Sheets production integration, large dashboards and generalized infrastructure.
3. Real observations (~10 days, 38 stalls, usually 1–2 check rounds daily) cannot validate offender-detection accuracy. Synthetic observations are fictional demonstrations, never treated as real or as ground-truth violations.
4. No raw plates, credentials or private rows in GitHub, assistant prompts, charts or logs; require approved access before touching the live Sheet. Use `America/Edmonton` for local-day rules.
5. All new Python behavior follows TDD RED → GREEN → REFACTOR. Record actual test commands, AI use, issue refs, and student read/accept before closing grouped issues.
6. **Remaining schedule is compressed, not extended:** never shift the December 4 freeze, December 8 presentation, December 11 submission or Sunday rest dates.

See [CAPSTONE_PLAN.md](CAPSTONE_PLAN.md), [SPRINT_PROGRESS.md](SPRINT_PROGRESS.md) and [GITHUB_ISSUE_WORKFLOW.md](GITHUB_ISSUE_WORKFLOW.md).

## November 22 rubric-aligned sprint update (current priority; supersedes conflicting task emphasis above)

**Source:** D2L “6. DAT 120 Mini Capstone Project” (two pages), student supplied November 22. Rubric: **ML model analysis/evaluation 40 points; code quality 30; presentation 20; one-page summary 10**. Assignment explicitly accepts a **Python script or notebook** (a notebook is encouraged for visibility, **not mandatory**), requires an exploration/visualization and model-training/validation narrative, a **presentation under 10 minutes**, and upload of the completed paper and presentation to the **D2L Mini capstone project dropbox**. Course outline says final presentations in **Week 6, December 9**; the historical December 8 target is provisional until instructor/D2L confirms the actual presentation appointment. Final submission remains **December 11**. Keep the internal **December 4 analysis freeze** and Sundays off.

| Session / date | Rubric-aligned priority and evidence of done |
| --- | --- |
| **S15 Mon Nov 23** | **40-point ML audit:** review synthetic feature-table coverage, 10d/30d sample sizes, duplicated patterns, inspection limitations; record tables/visuals and no ground-truth labels. |
| **S16 Tue Nov 24** | Explain model fit/score workflow, the **in-sample** nature of Isolation Forest, leakage limits, and comparison with the transparent two-check rule; no unsupported accuracy metrics. |
| **S17 Wed Nov 25** | **Sensitivity/interpretation:** compare two-check 133/315 vs 409/965 and IF 32/315 vs 97/965; explicitly explain preset 10% IF contamination and why LOF scores are withheld for duplicate neighborhoods. Test additional configurations only if academically justified. |
| **S18 Thu Nov 26** | Independently verified outcomes if permitted/available; otherwise document absence of labels, tiny/duplicated effective variety, and limits on validation. Privacy audit. |
| **S19 Fri Nov 27** | Make **public-safe EDA and model comparison** plots/tables; optional lightweight notebook referencing existing tested Python modules instead of recoding model logic. Add notebook only if it helps the 40-point rubric and is finished on time. |
| **S20 Sat Nov 28** | Student interpretation: describe business utility, limitations, all three approaches, and actionable **human-review-only** implications; check notebook/script execution and explainability. |
| **Sun Nov 29** | **Rest — no sprint.** |
| **S21 Mon Nov 30** | Rubric evidence checklist (40/30/20/10); verify one-page summary, Python script or notebook, citations, AI-use restrictions, and source provenance. |
| **S22 Tue Dec 1** | Improve short, legible visuals/slides and notes; demonstrate data exploration → feature engineering → model comparison → limitations. Plan talk for **8–9 minutes**, leaving margin under hard **10-minute maximum**. |
| **S23 Wed Dec 2** | Reproduce analysis/scripts, full pytest, optional notebook **Run All** if present, check files open and contain only public-safe synthetic aggregates. |
| **S24 Thu Dec 3** | **Timed full rehearsal** with 10-minute stopwatch, Q&A on contamination and LOF; check PowerPoint/offline backup and D2L upload requirements. |
| **S25 Fri Dec 4** | Freeze models/data/figures/presentation and record reproducible Git SHA and versions. No new modeling features after this point unless necessary to correct errors. |
| **S26 Sat Dec 5** | Timed mock talk and Q&A; reduce content if talk exceeds **10 minutes**. |
| **Sun Dec 6** | **Rest — no sprint.** |
| **S27 Mon Dec 7** | Final timed rehearsal, citations, backup check, and presenter-specific date/time confirmation. |
| **S28 Tue Dec 8** | **Presentation readiness target only**, not verified official presentation date. Present only if instructor confirms this day; otherwise keep frozen slides ready for the official Week 6 slot (course outline lists Dec 9). |
| **S29 Wed Dec 9** | Official outline's Week 6 presentation marker; give presentation here if scheduled and record non-sensitive feedback, otherwise use day for final corrections. |
| **S30 Thu Dec 10** | Validate required submission items, repo/scripts or notebook, one-pager, deck, APA and GAI citations, model caveats, privacy; test D2L upload readiness. |
| **S31 Fri Dec 11** | Upload the **completed paper/one-pager and presentation** to D2L Mini capstone project dropbox (include script/notebook as required by assignment/submission UI); verify deadline time and retain private confirmation. |

**Priority gate:** 40-point ML interpretation/validation evidence first; 30-point clean/tested code next; 20-point **<10 minute** presentation; 10-point one-page related-work summary. A notebook may improve examiner visibility but must **not** replace the accepted script option or displace needed evidence/rehearsal. Continue human review and privacy safeguards. Git commits must use `Refs #7`, `Refs #8`, `Refs #9`, `Refs #10` as applicable and record verifiable test outcomes and AI assistance.
