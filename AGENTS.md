# Project Instructions

These instructions apply to the **entire repository**, including application code, tests, fixtures, and Python utility scripts. The more specific instructions in [python/AGENTS.md](python/AGENTS.md) also apply to work under `python/`. A documentation standard does **not** authorize unrelated changes to operational code.

## Python Documentation Standard

For every Python source file **created or modified** in this project:

- Follow **PEP 257** conventions.
- Use **Google-style docstrings** for modules, classes, methods, and functions.
- Preserve existing program behavior when a task is documentation-only.
- Preserve existing type hints.
- Do not claim a design pattern that the implementation does not actually use.

Every Python module must begin with a module-level docstring using this structure:

```python
"""Module summary.

Brief explanation of what this module does and its responsibility within
the application.

Design Pattern:
    <Design pattern intentionally used by this module, or "None".>

Pattern Rationale:
    Explain why this pattern is appropriate, what problem it solves, and
    how it improves maintainability, extensibility, testability, or
    separation of concerns. If no pattern is used, explain that briefly.

Typical Usage:
    Explain how this module is normally used and how it fits into the
    overall application.
"""
```

For **public** classes, methods, and functions, include Google-style sections when applicable:

```python
def example_function(value: str) -> bool:
    """Brief description of the function's purpose.

    Add additional explanation when needed to explain behavior or
    architectural intent.

    Args:
        value: Explain what the value represents.

    Returns:
        Explain what the returned value means.

    Raises:
        ValueError: Explain when the exception is raised.

    Examples:
        >>> example_function("example")
        True
    """
```

Use these sections as appropriate:

- `Args:`
- `Returns:`
- `Raises:`
- `Attributes:`
- `Examples:`
- `Note:`

When a class participates in a design pattern, identify that pattern in its class docstring when it helps explain the architecture. Document **why code exists**, not merely what its statements literally do.

Avoid redundant documentation:

```python
def get_name():
    """Get the name."""
```

Prefer meaningful documentation:

```python
def get_name() -> str:
    """Return the normalized applicant name used for permit matching."""
```

If a design pattern spans several modules, identify each module's **actual** role in that pattern, such as interface/protocol, abstract base class, concrete strategy, adapter, factory, repository, service, facade, or client. Do not repeat the full pattern explanation in every method.

### Documentation-only changes

When modifying an existing file only to update documentation:

- Do **not** refactor the implementation.
- Do **not** rename functions, classes, or variables.
- Do **not** reorganize modules.
- Do **not** alter executable behavior or type hints.
- Update obsolete or inaccurate documentation when necessary.

### Documentation quality

Documentation must be suitable for both an academic software project and a professional codebase. A new developer should be able to determine:

1. What the module does.
2. Where it belongs in the application.
3. What design pattern it actually uses, if any.
4. Why the pattern was chosen.
5. How the module is normally used.
6. What its public API does.
7. What its inputs and outputs represent.
8. What exceptions, assumptions, side effects, or edge cases matter.

### Verification checklist

Before finishing a Python documentation task, verify that:

- Every affected Python module has the required module-level docstring.
- Every affected public class, method, and function has an accurate docstring.
- Design-pattern claims match the real implementation.
- Type hints and executable statements are unchanged in documentation-only work.
- The existing relevant tests still pass, except for already-documented expected failures.

Run the tests when the environment is available; **never claim they passed if they were not run**. For documentation-only edits, perform a diff review and test the behavior if possible. This instruction applies prospectively to files created or modified; it is **not** a request to rewrite every existing source file now.


## Repository-wide Git Commit Messages

Use the accepted [commit message template](.gitmessage.txt) for Git commits across this repository. Follow `type(scope): imperative summary` and describe the real purpose, changes, test results, applicable PEP 257/Google-style documentation verification, privacy/security review, AI assistance, and related sprint/issue. Include RED/GREEN/REFACTOR evidence for new Python behavior when applicable. State `Not run` or `N/A` rather than inventing outcomes. Do not put actual plate numbers, personal data or credentials into public commit history.

Configure once per local clone from the repository root:

```powershell
git config --local commit.template .gitmessage.txt
```

Then use `git commit` (without `-m`) to open the editor with the template. GitHub web/API commits do not automatically apply local templates; use the same conventions manually. For DATA120 review gates, follow [python/AGENTS.md](python/AGENTS.md) and the existing AI use log.

## Issue-driven DATA120 workflow

For planned DATA120 work, find the existing issue in the [issue/session index](python/docs/planning/GITHUB_ISSUE_WORKFLOW.md) before starting; search open and closed issues before creating another. Include the actual session ID(s), planned date(s), and `Refs #N` in partial/review-pending commits. Use `Closes #N` only when the whole issue's acceptance criteria, relevant checks and explicit student read/accept gate are satisfied. Closing keywords in commits close issues when the commit reaches the default branch (`main`); they do not enforce student review. Do not close a grouped issue after just one session. Use one reference per affected issue; never invent issue numbers or approval. Unplanned work should reuse a relevant issue or explain `N/A`. Preserve Sundays off and all DATA120 deadlines, privacy, TDD and course-permission requirements.

## Mandatory AI-agent issue lookup and automatic commit linking

For **every AI-assisted change and commit**, including Git CLI commits, GitHub API/connector commits, and pull-request commits, the agent—not the student—must perform the following steps:

1. **Before preparing or making the commit**, identify the current S01–S31 sprint session or task, read the [DATA120 issue/session index](python/docs/planning/GITHUB_ISSUE_WORKFLOW.md), and actively **search GitHub's open and closed issues** for matching scope, session and acceptance criteria. Do not rely only on memory, a suggested number or the index; confirm the actual issue exists and check its current status. For unrelated repository tasks search for the appropriate issue too.
2. **Reuse an existing matching issue**, rather than creating a duplicate. If multiple issues apply, use a separate reference for each issue actually affected by the commit. If no issue fits, create a narrowly scoped issue **only when authorized**; otherwise flag the missing issue for review **before committing**. Never invent a number or substitute an unrelated issue to satisfy the requirement.
3. **Automatically write the confirmed references into the commit message body**, with `Refs #N` for partial work, work awaiting required student review, or an issue that should remain open. This is a non-closing reference.
4. Use `Closes #N` **only** when the *entire issue's* acceptance criteria and required tests/documentation/privacy checks have actually been satisfied, explicit student reading **and** acceptance have been logged for the relevant material, and closure is intended. A single finished session does not close a grouped issue. Beware: on GitHub, closing keywords on commits reaching the default branch can close the issue immediately.
5. For a local `git commit`, fill out `.gitmessage.txt`. For GitHub REST/API/connector-generated commits, supply the identical reference text **directly in the API commit message**; local commit templates do not apply automatically. For pull requests, reference the issue in the PR body as well and ensure actual commits remain traceable.
6. **After committing**, report the actual commit SHA and GitHub URL, linked issue number and URL, observed test results (or `Not run`), and AI-use log review status. Verify that the resulting commit message contains the correct references; do not claim GitHub has linked or closed the issue without verification.
7. Respect Python TDD, the [AI read/accept gate](python/docs/ai/AI_USE_LOG.md), academic integrity, private-data restrictions, approved December deadlines, and Sundays off. A matching issue does **not** grant permission for unapproved work or bypass review.

For planning-only or bookkeeping changes, reference the existing workflow issue when it genuinely matches (currently [#1](https://github.com/alby1976/ParkingPatrol/issues/1)); do not close it merely for updating an agent policy. If no appropriate issue exists, explain the blocker rather than guessing.
