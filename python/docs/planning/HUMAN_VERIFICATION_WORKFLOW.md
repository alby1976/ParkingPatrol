# DATA120 — Human verification, blacklist, and on-site action records

**Status:** Proposed extension of the suspicious-pattern project; student reading and acceptance pending. Not connected to live Google Sheets or Apps Script and not an enforcement application.

## Important distinction: required staff Form selection

The new optional per-vehicle staff Form records a required **Unknown / Suspicious / Violator** category. These are *staff-reported categories*, even when someone selects “Violator”. They do not override this document's independent verification requirements, do not create a confirmed blacklist entry, and do not trigger ticketing or towing.

Python keeps these form reports in the separate `src/staff_status.py` research module, **not** the `ReviewOutcome` record. Never treat status selections as ground-truth labels for evaluation without independently checking the underlying evidence and necessary permissions. See [status setup](../../../docs/Per_Vehicle_Status_Setup.md).

## Business rule

A vehicle may first be marked **Suspicious** because it appeared in at least two separate same-day check events, or because an unsupervised algorithm identified an unusual observation pattern. This triggers a **human verification**, not a violation finding.

Staff or another properly authorized reviewer then checks evidence and parking rules. Their decision is one of:

| Human decision | Blacklisted? | Next step |
| --- | --- | --- |
| Confirmed violation | Yes, following an explicit recorded human finding | Authorized staff may separately ticket/tag on site according to applicable authority and procedures |
| No violation | No | Close or clear the suspicion as appropriate |
| Inconclusive / insufficient evidence | No | Keep under review or take no action; no enforcement solely on a model flag |

**Blacklisted** means a restricted operational status representing an independently verified violation. It is not an automatic ML label. Where a blacklist is maintained, establish review, correction, appeal, and retention procedures; future entries may require re-verification.

## End-to-end flow

```text
Existing Google Form → Google Sheet
              |
       Clean / normalize
              |
      Same-day rule OR ML anomaly
              |
         SUSPICIOUS
              |
        HUMAN VERIFICATION
          /      |      \
  Violation   No violation   Inconclusive
     |             |              |
 Confirmed &    Not blacklisted   Not blacklisted
 blacklisted
     |
 Authorized personnel may issue an on-site ticket / tag
     |
 Separate manual action record (who, when, reference)
```

Neither an AI prediction nor a repeated sighting confirms that a vehicle violates parking restrictions. Distinct checks may observe one uninterrupted stay.

## Python research module

`python/src/verification.py` provides **pure, offline, immutable records**:
- `record_review(...)`: accepts an explicit human `finding`, reviewer ID, timestamp, and private evidence reference; only confirmed violations become `blacklisted=True`.
- `record_manual_action(...)`: records a staff-reported `ticket` or `tag` after a confirmed violation, with staff ID, timestamp and private action reference. It does **not** create the ticket, notify a patrol service, or issue a tag.
- Human decisions and enforcement actions remain distinct from `rule_suspicious` and `anomaly_suspicious`.

Only pseudonymous, synthetic identifiers belong in public Git/test fixtures. Reviewer and evidence references for actual cases must stay in a secure, restricted operational system; the public capstone should contain only fake examples. A production implementation will need separately approved authorization, audit access, correction workflows, retention, and lawful enforcement procedures.

## Unsupervised versus human labels

The unsupervised model can learn which patterns are unusual **without using verified violation outcomes as training labels**. Independently reviewed decisions can later be used to **evaluate** whether anomaly flags led to useful human reviews, provided data use is permitted and the evaluation prevents time leakage. They must not be retroactively rebranded as predictions made by an unsupervised algorithm.

## TDD status

- `python/tests/test_verification.py` was authored before `python/src/verification.py`, using synthetic inputs.
- An attempt to execute the RED tests could not fetch the GitHub test file in the available runtime due to network/DNS restrictions. **Do not claim a verified failing RED run.**
- GREEN and REFACTOR test runs are **not verified**. The new code is a proposed implementation requiring a student-reviewed Python 3.13 test run before being relied upon.
- Recommended command: `python -m pytest python/tests/test_verification.py -q`, then `python -m pytest python/tests -q`.

Academic integrity and AI-use reporting rules apply. See [TDD guide](../guides/TDD_GUIDE.md) and [project AI log](../ai/AI_USE_LOG.md).
