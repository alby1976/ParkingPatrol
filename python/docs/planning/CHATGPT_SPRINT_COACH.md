# ChatGPT Sprint Coach — DATA120

This is an interactive workflow. ChatGPT helps when you open the conversation; it cannot monitor work between chats without a separate automation.

## Start a session

Paste into ChatGPT:

> Guide me through DATA120 Sprint **SXX** in `alby1976/ParkingPatrol`. First read `python/AGENTS.md`, `python/docs/planning/GUIDED_SPRINT_SESSIONS.md`, and `python/docs/planning/SPRINT_PROGRESS.md` on GitHub. Check for pending AI approval gates. Give me **one simple action at a time**, tell me where to click or what command to run, and wait for my actual result. Use Python 3.13 and RED → GREEN → REFACTOR for code changes. Do not invent test outcomes. Use only invented IDs for public tests. Help me document progress, tests, Git commits and material AI assistance. Stop for separate reading confirmation and acceptance before any next substantive step.

Replace SXX with the chosen session ID. Do not assume a sprint is finished just because its calendar date has passed.

## Coaching routine

1. **Start (5–10 min):** read tracker and code state, show one goal and a definition of done.
2. **Hands-on (40–60 min):** one command or edit at a time, with expected output. Use synthetic tests and log actual RED, GREEN and REFACTOR results for code.
3. **Review (10–15 min):** inspect changed files and tests, check for secrets and real plate data, write a factual commit message.
4. **Approval:** log material AI help. The student explicitly confirms they read the generated material and separately accepts it or requests revision. Record both timestamps, and do not advance until accepted.

## Helpful short prompts

- `I am stuck on SXX. Give me one next troubleshooting step and show the expected result.`
- `Read my GitHub sprint tracker and tell me the last verified completed task and today's next task.`
- `Explain this Python function with three tiny synthetic records and an expected output.`
- `Help me write one failing pytest test first. Do not implement before I verify RED.`
- `Rehearse my DATA120 slides with one question at a time and point out one factual weakness.`

## Hard stop conditions

Never claim a test ran if no output was observed. Never expose credentials, raw plate data or private Google Sheets rows. If Google access is not approved, use the fake/synthetic adapter. Respect instructor-specific AI restrictions. Do not create an enforcement decision from an ML score. **Sundays are rest days**, so resume the next non-Sunday. If behind, drop optional kNN before reducing review or quality checks.

## S01 quick start

Open PowerShell from your ParkingPatrol working directory, check the installed Python 3.13 version and Git status, and verify the local `.env` is ignored. Ask the coach to provide and explain each command individually; paste only non-sensitive results. Finish with a factual entry in `SPRINT_PROGRESS.md` and the required AI read/accept checkpoint.
