# DATA120 AI Review and Acceptance Gate

For each AI-assisted DATA120 task, record the contribution in `AI_USE_LOG.md` and stop for two explicit student decisions: **I have read it**, followed by **I accept it** (or **I request changes**). Neither silence nor an assistant's judgment counts as confirmation. The log must record the date and time of both confirmations. Only acceptance unlocks the next substantive task.

## Local commands

From the repository root:

```powershell
python python/log_ai_use.py add --tool "ChatGPT (OpenAI)" --activity "Described proposed feature engineering"
python python/log_ai_use.py read --id ENTRY_ID
python python/log_ai_use.py accept --id ENTRY_ID
python python/log_ai_use.py check
```

Use `read` only following an explicit student's reading confirmation, and `accept` only following their explicit acceptance. After an explicit request for changes, use `reject --id ENTRY_ID`, then `revise --id ENTRY_ID` once revised material is ready. The revised work needs renewed reading and acceptance. All commands recording a human decision must reflect an actual human message.

Timestamps are captured when the local command is run, in `America/Edmonton` time. Do not invent or backdate timestamps. GitHub connectors without execution may update the log directly after confirmation only with a reliable timestamp; otherwise leave the time unverified and state the limitation.

## Boundaries

This workflow is followed by cooperating coding assistants; it is not server-enforced GitHub protection and cannot authenticate a student's identity or detect every instance of AI use. Historical activity must not be retroactively marked accepted. Student acceptance is not proof that AI use is permitted by the instructor or that the results are scientifically correct. Do not place sensitive or identifiable parking data in the public log.
