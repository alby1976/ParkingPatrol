# Recording generative AI assistance — DATA120

**Goal:** AI coding assistants update [AI_USE_LOG.md](AI_USE_LOG.md) as part of their normal work, without requiring the student to type each disclosure.

## Required agent workflow

Whenever an AI assistant materially helps with DATA120 planning, code, debugging, documentation, visualizations, model analysis, or assessment preparation:

1. Check the assignment's specific GAI allowance before providing assessable work.
2. Describe **what AI actually did** and identify the tool/model when known.
3. From the repository root, run the logging command **during the same task**, before final commit or pull request.
4. Present the material to the student and require explicit read confirmation, then explicit acceptance, each recorded with its real timestamp. Run `python python/log_ai_use.py check` before the next substantive step. See [AI_REVIEW_GATE_GUIDE.md](AI_REVIEW_GATE_GUIDE.md).
5. Review the generated Markdown diff for accuracy and sensitive information, then include it in the relevant commit.
6. If unable to run the command (for example, via a GitHub connector only), **directly edit AI_USE_LOG.md** in the same task/commit.
7. Do not claim that a student verified material they have not yet verified: mark verification pending.
8. The student reviews the log and adds the required instructor-specified formal citation/disclosure before submission.

### Example command (PowerShell, from repository root)

```powershell
python python/log_ai_use.py add --tool "ChatGPT (OpenAI)" --activity "Explained feature engineering using synthetic examples"
```

The script timestamps entries in **America/Edmonton**, writes an Assistance history row and a pending review-register row, and blocks the next task until `read` followed by `accept` are recorded. It uses Python's standard library only.

### Limits of automation

**This is agent-workflow automation, not universal AI detection.** Git itself cannot determine if a change was AI-generated. AI assistants that ignore this instruction, tools that cannot read repository instructions, edits outside this workflow, or assistants without repository write access will not necessarily update the log. GitHub does not execute this script automatically merely because someone commits. Do not claim perfect coverage.

Never include real licence plates, raw parking observations, names, confidential prompts, keys, or sensitive data in the **public** log. A brief factual task description is sufficient.

The log records assistance; it is **not** proof that AI use was permitted, a substitute for APA/instructor citations, or evidence that the student independently validated any output.
