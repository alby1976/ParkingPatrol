# DATA120 documentation index

This directory groups coursework documentation by responsibility. The repository's Python entry point is [../README.md](../README.md), and coding assistants must follow [../AGENTS.md](../AGENTS.md).

## Planning
- [Capstone plan](planning/CAPSTONE_PLAN.md) — research goals, methods, deliverables
- [Data dictionary](planning/DATA_DICTIONARY.md) — observation schemas and feature definitions
- [Suspicious-pattern rule and unsupervised ML](planning/SUSPICIOUS_PATTERN_MODEL.md) — rule threshold, model indicators, limits

## Architecture
- [System architecture](architecture/ARCHITECTURE.md) — Python 3.13 design, low coupling and high cohesion

## Practical guides
- [Test-driven development](guides/TDD_GUIDE.md) — RED, GREEN, REFACTOR
- [Git commit messages](guides/GIT_COMMIT_GUIDE.md) — AI-assisted commit format
- [Local environment setup](guides/ENV_SETUP.md) — ignored `.env` and safe `.env.example`

## Course policies
- [Academic integrity and GAI policy](policies/ACADEMIC_INTEGRITY_AND_COURSE_POLICIES.md)
- [Citations, copyright and privacy checklist](policies/CITATIONS_COPYRIGHT_PRIVACY_CHECKLIST.md)

## AI transparency
- [Generative AI Use Log](ai/AI_USE_LOG.md) — contributions and student review timestamps
- [AI logging workflow](ai/AI_LOGGING_GUIDE.md)
- [Student reading/acceptance gate](ai/AI_REVIEW_GATE_GUIDE.md)

**Unmoved by design:** `python/README.md`, `python/AGENTS.md`, `python/log_ai_use.py`, `python/requirements.txt`, `python/.env.example`, `python/COMMIT_TEMPLATE.txt`, the `src/` code, and `tests/`. Keeping these in standard/discoverable locations avoids breaking tools and local configuration. The operational Apps Script is untouched.

**Current status:** Document reorganization awaits student reading and explicit acceptance. No Python tests have been run as part of this documentation refactor.
