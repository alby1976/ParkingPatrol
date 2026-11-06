# DATA120 Generative AI Use Log

Use this file to **record assistance transparently**. AI assistants following [AGENTS.md](../../AGENTS.md) must append an entry for each material AI-assisted task using [log_ai_use.py](../../log_ai_use.py) or direct repository editing; see [AI_LOGGING_GUIDE.md](AI_LOGGING_GUIDE.md). This does not automatically detect AI use by every tool. The [reading/acceptance gate](AI_REVIEW_GATE_GUIDE.md) blocks the next substantive step for cooperating agents until the student has explicitly confirmed reading and acceptance; it does not authenticate the student or control unrelated tools. This is not permission to use AI in a restricted assessment, nor does this log substitute for formal citations required by the instructor.

## Assignment permission gate

| Item | Answer |
| --- | --- |
| Assignment or learning activity | DATA120 mini capstone — confirm exact title |
| Instructor AI instructions checked? | **Pending confirmation** |
| Permitted tasks / limits | **Pending confirmation** |
| Required disclosure/citation format | **Pending confirmation** |
| Instructor clarification (if needed) | Not yet recorded |

**Until confirmed:** Treat AI-drafted assignment material as a planning aid, not automatically as acceptable submitted work.

## Assistance history

| Date | Tool | What the tool helped with | Student's verification / independent contribution | Reference in submission |
| --- | --- | --- | --- | --- |
| 2026-11-04 | ChatGPT (OpenAI) | Suggested DATA120 Python directory organization, research question, preliminary modeling plan, data dictionary, and starter dependencies | Student must review, revise, and decide what to adopt | To be completed if used |
| 2026-11-04 | ChatGPT (OpenAI) | Drafted course-policy summary, AI-use log template, and citation/privacy checklist from student-provided syllabus excerpt | Student must compare against course outline and instructor guidance | To be completed if used |

| 2026-11-04 | ChatGPT (OpenAI) | Created an agent-invoked Python AI-use logging script and guide; updated AGENTS.md, Git commit guide, and README to require task-level logging | Student verification pending; tool workflow is not automatic detection of all AI use | Citation/disclosure pending |

| 2026-11-04 | ChatGPT (OpenAI) | Implemented requested explicit read/accept confirmation gate with timestamped statuses, agent instructions, and supporting documentation | Student explicitly confirmed reading and acceptance on 2026-11-05; see entry review-gate-20261104 | Citation/disclosure pending |

| 2026-11-05 | ChatGPT (OpenAI, GPT-6) | Regenerated DATA120 Python directory organization, primary research question, preliminary modeling plan, data dictionary and starter dependency list; added placeholder folder READMEs | Student reading and acceptance pending; see entry capstone-regeneration-20261105 | Citation/disclosure pending |

| 2026-11-05 | ChatGPT (OpenAI, GPT-6) | Revised Python DATA120 planning documents to specify planned restricted read-only Google Sheets API integration as the data source for pandas and ML | Revised material awaiting student reading and acceptance; capstone-regeneration-20261105 | Citation/disclosure pending |

| 2026-11-05 | ChatGPT (OpenAI, GPT-6) | Revised DATA120 plan, README, AGENTS.md, dependencies and architecture documentation for Python 3.13 and low-coupling/high-cohesion design patterns | Student review and acceptance pending for updated plan; capstone-regeneration-20261105 | Citation/disclosure pending |

| 2026-11-05 | ChatGPT (OpenAI, GPT-6) | Added placeholder-only python/.env.example, local environment setup guide, gitignore exception, python-dotenv dependency and configuration/credential instructions; no credentials created or exposed | Updated proposal pending student review and acceptance: capstone-regeneration-20261105 | Citation/disclosure pending |

| 2026-11-05 | ChatGPT (OpenAI, GPT-6) | Added python/src/cleaning.py to standardize already-pseudonymized sightings/checks and quarantine anomalies; wrote synthetic pytest cases and updated architecture, project, and data dictionary | Pending renewed reading and acceptance for capstone-regeneration-20261105; tests not yet executed | Citation/disclosure pending |

| 2026-11-05 | ChatGPT (OpenAI, GPT-6) | Added TDD_GUIDE.md and revised AGENTS.md, ARCHITECTURE.md, CAPSTONE_PLAN.md, README.md, tests guide, and commit guide to require test-first red-green-refactor workflow | Student reading and acceptance pending for capstone-regeneration-20261105; no tests were run for this documentation change | Citation/disclosure pending |

## Copy this row for each future use

| YYYY-MM-DD | Tool and model/version (if known) | Precise prompt/task and output used | What I independently verified/changed | In-text citation or appendix location |
| --- | --- | --- | --- | --- |

## AI material reading and acceptance register

AI-generated material must receive two **explicit student confirmations** before the agent can proceed to the next substantive step: (1) **Read**, then (2) **Accepted**. "Revision requested" remains blocked. Recorded times use `America/Edmonton` with UTC offset where available. Agents must never record reading or acceptance from silence, a generic acknowledgment, or their own judgment. For connector edits, do not invent a timestamp; if precise time is unavailable, leave it pending and use the local logger when the student confirms.

| Entry ID | Status | Logged at | Read confirmed at | Decision at | Material / scope | Student response |
| --- | --- | --- | --- | --- | --- | --- |
| review-gate-20261104 | Accepted | 2026-11-04 (time unavailable) | 2026-11-05T06:54:41-07:00 | 2026-11-05T06:54:41-07:00 | Implement two-stage reading and acceptance gate in DATA120 agent workflow, logger, and documentation | Student explicitly confirmed reading and acceptance in the same message; both confirmations recorded upon receipt. |

| capstone-regeneration-20261105 | Accepted | 2026-11-05T06:59:31-07:00 | 2026-11-05T21:48:39-07:00 | 2026-11-05T21:48:39-07:00 | DATA120 Python 3.13 plan with read-only Google Sheets, ignored .env, cleaning module, and mandatory test-driven development (RED-GREEN-REFACTOR); latest revision 2026-11-05T21:45:25-07:00 | Student explicitly confirmed reading and acceptance of revised TDD plan in one message; both confirmations recorded upon receipt. No test execution claimed. |

## Draft disclosure wording — customize only if the use was permitted

> Generative AI tools were used as permitted by the course instructions to assist with [specific tasks]. I independently checked the generated suggestions, implemented/verified [specific work], and performed the analysis and interpretation. The relevant uses are documented in the project AI use log and cited according to the course requirements.

**Do not paste this as a claim of compliance without confirming the actual assignment rules and citations.**

Course-provided guidance: https://conted.ucalgary.ca/info/writing.jsp
