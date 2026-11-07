# DATA120 — Git Commit Messages for AI Coding Assistants

Use the repository-wide [`.gitmessage.txt`](../../../.gitmessage.txt) when preparing commits; the earlier [COMMIT_TEMPLATE.txt](../../COMMIT_TEMPLATE.txt) is retained for reference. The template is **suggested structure**, not proof that a change is correct, independently created, tested, or acceptable under course assessment rules.

## Before generating a commit message

1. Read `python/AGENTS.md` and the academic-integrity documents.
2. Inspect the **actual staged diff** (`git diff --cached`) and `git status`. Do not describe work absent from the diff.
3. Check for sensitive content before staging or committing: no real licence plates, customer details, raw exports, tokens, secrets, or keys.
4. Check which tests really ran and what they reported; never claim a pass without evidence.
5. If AI helped generate code, documentation, analyses, or the message itself, represent that assistance accurately. For material AI help, run `python python/log_ai_use.py add --tool "Tool (model if known)" --activity "Work performed"` or update `../ai/AI_USE_LOG.md` directly if you cannot execute code. Follow [AI_LOGGING_GUIDE.md](../ai/AI_LOGGING_GUIDE.md) and the [mandatory read/accept gate](../ai/AI_REVIEW_GATE_GUIDE.md). Do not begin another substantive task before the student explicitly confirms both reading and acceptance. Log entries **do not replace** required formal AI citations/disclosures.
6. Ask the student to review the message and changes. Do not invent user approvals or assert that assignment-specific AI use is permitted without confirmation.

## Configure the commit message template (Windows PowerShell)

From the **repository root**, run:

```powershell
git config --local commit.template .gitmessage.txt
```

This affects this local clone only. Verify:

```powershell
git config --local --get commit.template
```

Then use `git commit` (without `-m`) to open the editor with the template. If Git does not open an editor, configure your preferred `core.editor` first. **GitHub does not automatically apply the template to web-created commits or connector-written commits.** AI assistants writing commits through an API should follow the same structure manually.

To turn the template off:

```powershell
git config --local --unset commit.template
```

## Test-driven development evidence

For new Python features and bug fixes, include a truthful TDD section when drafting commit messages (see [TDD_GUIDE.md](TDD_GUIDE.md)):

```text
TDD evidence:
- RED: focused test command and observed expected failure (or Not run)
- GREEN: command and observed pass/failure (or Not run)
- REFACTOR: regression suite command and result (or Not run)
```

Do not manufacture any output; completing a commit does not establish a passing test or student approval.

## Conventional subject

```text
type(scope): imperative summary
```

Common types: `feat`, `fix`, `docs`, `test`, `refactor`, `chore`, `build`, `ci`, `perf`.

Examples (illustrative, not claims of completed work):
- `docs(data120): document observation-data limitations`
- `feat(features): count distinct observed dates per window`
- `test(features): cover incomplete-check edge cases`

Use a short subject; explain **why**, actual **changes**, genuine **RED/GREEN/REFACTOR evidence**, **documentation**, **privacy/security**, **AI assistance**, and **related sprint/issue** in the body. Mark inapplicable sections as `N/A` and unexecuted tests as `Not run`. Do not include confidential data in messages: commit messages are part of public Git history.

## AI assistant prompt

> Review the actual staged diff, applicable `python/AGENTS.md` rules, and test output. Draft a Git commit message using `python/COMMIT_TEMPLATE.txt`. Explain what changed, why, and what validation actually ran. State any AI contribution accurately and do not claim independent authorship, test results, approval, or course permission that is unverified. Do not include private data. Return the message for student review before committing.

## Responsibility

The student decides what to stage, verifies the resulting commit, and independently completes the assessed analysis. Assignment-specific instructor rules take precedence over this guide.
