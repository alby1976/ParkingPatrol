# DATA120 GitHub issue and session index

Created 2026-11-07 from the approved [guided sessions](GUIDED_SPRINT_SESSIONS.md) and [capstone plan](CAPSTONE_PLAN.md). Existing open/closed issue search returned no issues before creation. Ten issues replace 31 microissues: nine implementation/milestone groups and one workflow task. Milestones below are tracking issues, not native GitHub milestone objects.

Workflow setup: [#1](https://github.com/alby1976/ParkingPatrol/issues/1), AI review ID `issue-workflow-20261107` (Pending reading).

| Issue | Sessions and planned dates (2026) | Scope |
| --- | --- | --- |
| [#2](https://github.com/alby1976/ParkingPatrol/issues/2) | S01–S02 · Nov 6–7, 2026 | Foundation and early slide outline |
| [#3](https://github.com/alby1976/ParkingPatrol/issues/3) | S03–S06 · Nov 9–12, 2026 | Read-only Sheets adapter and safe import boundary |
| [#4](https://github.com/alby1976/ParkingPatrol/issues/4) | S07–S09 · Nov 13–16, 2026 | Cleaning and shared observation-window features |
| [#5](https://github.com/alby1976/ParkingPatrol/issues/5) | S10–S13 · Nov 17–20, 2026 | Two-check baseline, LOF and Isolation Forest comparison |
| [#6](https://github.com/alby1976/ParkingPatrol/issues/6) | S14 · Nov 21, 2026 | Milestone: November 21 scope decision |
| [#7](https://github.com/alby1976/ParkingPatrol/issues/7) | S15–S20 · Nov 23–28, 2026 | Evaluation, stability and student interpretation |
| [#8](https://github.com/alby1976/ParkingPatrol/issues/8) | S21–S25 · Nov 30–Dec 4, 2026 | Milestone: reproducible presentation and December 4 freeze |
| [#9](https://github.com/alby1976/ParkingPatrol/issues/9) | S26–S28 · Dec 5, 7–8, 2026 | Milestone: presentation readiness and December 8 delivery |
| [#10](https://github.com/alby1976/ParkingPatrol/issues/10) | S29–S31 · Dec 9–11, 2026 | Milestone: final audit and December 11 submission |

## How to work

Follow groups in session order. The adapter precedes integrated cleaning/features; the shared feature contract precedes model comparison; evaluated results feed the frozen deck. Slide preparation runs throughout. The Nov 21 scope gate uses actual progress; drop kNN if behind, then prioritize baseline plus one credible model if necessary.

Each issue lists every session date and clear acceptance criteria. Leave boxes unchecked until evidence exists. Record commands/results, safe artifacts, commit/PR links and student decisions; keep sensitive evidence outside public GitHub. Review existing modules before adding code. Update [SPRINT_PROGRESS.md](SPRINT_PROGRESS.md) only from actual student evidence. Issue creation has not advanced progress.

Use `Refs #N` for partial work or pending review. Use `Closes #N` only for full completion and satisfied review gates; see the [Git commit guide](../guides/GIT_COMMIT_GUIDE.md). A completed session does not close its whole group.

## Fixed constraints

- Sundays Nov 8, 15, 22, 29 and Dec 6: no coursework. A late session requires replanning within working days, not assumed completion.
- Dec 4: freeze analysis, models, figures and presentation version. Dec 8: present. Dec 11: submit by the instructor's required time (verify time; none is invented here).
- Python 3.13; RED/GREEN/REFACTOR evidence for every new behavior/fix, synthetic fixtures and fake readers. Documentation-only work reports tests as not run.
- Public issues, commit messages, screenshots and logs contain no real plates, private observations, credentials or sensitive submission receipts.
- Instructor-specific AI permission remains unconfirmed in the AI log. Student owns interpretations/conclusions. Record material AI help and stop for explicit read then acceptance before the next substantive task.
- Real and synthetic evidence remain separate; anomalies and repeated sightings do not prove violations. No automated enforcement or production Apps Script changes.
