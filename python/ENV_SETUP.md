# DATA120 — local .env setup (Python 3.13)

The `python/.env` file holds **local configuration and secrets**. It must **never be committed or uploaded to GitHub**. Only [`.env.example`](.env.example), containing empty values and instructions, is tracked.

> A `.env` file is plaintext, not an encrypted password vault. Protect the workstation, filesystem permissions, backups, and account access. For more sensitive deployment scenarios, use an approved secrets manager. Do not send a real `.env` file to a generative AI assistant.

## One-time setup in Windows PowerShell (repository root)

```powershell
git pull origin main
Copy-Item python/.env.example python/.env
notepad python/.env
```

Fill the approved settings **only inside the local `python/.env`**, never in the sample:
- `GOOGLE_SHEETS_ID` — spreadsheet ID from the approved Sheet URL; do not publish actual private IDs needlessly.
- `GOOGLE_SHEETS_CREDENTIALS_FILE` — absolute path to an OAuth/service-account credentials JSON stored outside the Git working tree.
- `GOOGLE_SHEETS_READ_RANGE` — a permitted worksheet range such as `Observations!A:Z`, after real headers are verified.
- `GOOGLE_SHEETS_SCOPES` — keep the read-only scope.
- `PARKINGPATROL_PSEUDONYMIZATION_SECRET` — only if the reviewed privacy design needs a secret. Use a securely generated key, never a known demonstration value.

**Do not put your Google password in the file.** The Google Sheets API uses approved OAuth or service-account credentials. OAuth token caches and service-account JSON must also stay outside the public repository. A credential file's path is configuration; the credential file itself is sensitive.

## Check Git exclusions without exposing values

```powershell
git check-ignore -v python/.env
git status --short
```

The first command should print the matching ignore rule; `python/.env` must not appear as an added file. Use `git check-ignore -v python/.env.example` carefully: the sample should be trackable, not accidentally ignored.

**Important:** `.gitignore` protects *untracked* files. It does not untrack a secret already committed. If credentials were ever accidentally committed, stop and revoke/rotate them; removing the latest file alone does not erase Git history.

## Planned Python usage

The `python-dotenv` library reads the local file into environment variables. A future centralized settings module should load it explicitly and validate required values; pure analysis and ML modules should receive a typed configuration object rather than reading `os.environ` throughout the code.

```python
from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv(Path("python/.env"), override=False)
sheet_id = os.getenv("GOOGLE_SHEETS_ID")
if not sheet_id:
    raise RuntimeError("Set GOOGLE_SHEETS_ID in your local python/.env")
```

This is a setup illustration only; a live Google Sheets connector has not been implemented. Secrets should never be printed, logged, returned in exception messages, or placed in notebook outputs.

## Public repository policy

Only sanitized `.env.example` and documentation are committed. Do not put credentials, Google Sheet rows, raw plates, private exports, or pseudonymization lookups in public Git. Review each staged diff before commit. Follow [AGENTS.md](AGENTS.md), the course integrity rules, and the student acceptance gate.
