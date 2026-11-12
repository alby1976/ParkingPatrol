# Per-vehicle staff status form — setup and privacy guide

**State:** Code committed for student review; **NOT deployed or live-tested in Google Forms**. Use a restricted test copy before deploying to the clinic.

## Why there are two forms

The existing parking-round Form asks for a **multiline list of plates** for one area. One required dropdown on that Form would incorrectly apply the same classification to **every plate** in that response. To preserve the current operating workflow, the installer now creates a **second Form**, one plate per response.

| Form | What staff submit | Required fields |
| --- | --- | --- |
| Existing ParkingPatrol parking check | One inspection round: area, list of all plates, completion | Area; every vehicle recorded? |
| New ParkingPatrol per-vehicle staff status | **Exactly one plate** and a staff-reported category | **Plate, Province, Staff-reported status** |

The **Staff-reported status** dropdown allows **Unknown**, **Suspicious**, or **Violator**. It is required, and staff must explicitly select one. *Unknown* is the appropriate selection when evidence is insufficient. Google Forms does not automatically preselect it.

**Violator is the confirmed historical status for a vehicle previously issued a parking ticket.** Authorized staff must check the private prior-ticket record before selecting it; a Suspicious vehicle without a confirmed prior ticket is not a Violator. This status identifies a **past confirmed incident**, not a new violation today. The Form does not automatically issue a ticket, notify patrol, change the blacklist or train the AI model; a fresh enforcement action still requires independent review and authorization.

## What the installer changes

The new script [PlateStatus.gs](../apps-script/PlateStatus.gs) exposes `setupPlateStatusForm_(spreadsheet, properties)`. The existing [Code.gs](../apps-script/Code.gs) installer calls that function during `setupParkingPatrol()`. It saves the new form ID as the script property `PLATE_STATUS_FORM_ID`; rerunning installation repairs required questions without creating duplicates.

The **existing round-collection form remains untouched**, including its trigger and processing. The new status Form sends responses to the **same restricted spreadsheet**, normally in a separate Google Forms response tab. Its links are listed on the `Setup` tab. This is not a new production Sheet API sync or deployment.

## Administrator rollout (only after approval)

1. In a **test copy** of your restricted Google Sheet / Apps Script project, add `apps-script/PlateStatus.gs` alongside the updated `Code.gs`. GitHub updates do **not** automatically publish a Google Form. Verify the script ID and account authorization.
2. Run **ParkingPatrol → 1. Install / repair**, granting only the intended Google Forms/Sheets permissions.
3. Open the private `Setup` worksheet and find **Per-vehicle staff status form edit link**.
4. Confirm that **Plate**, **Province**, and **Staff-reported status** are all required, and that the status choices are **Unknown**, **Suspicious**, and **Violator**.
5. Restrict editors and responders to approved staff **before publishing or accepting responses**. Do not enable public access. Avoid sharing either form's edit link outside administrators.
6. Submit **fictional test data** (e.g. fake plate and province) and verify that a separate response worksheet receives that entry. Confirm a blank status is blocked, and that the original check-round Form continues working without interference.
7. Confirm an access-controlled retention, correction and deletion process **before live use**. The current 3-month operational cleanup does **not automatically purge entries from the separate Form responses**. Never assume that status reports inherit the main observation-retention controls.

If your Google account cannot publish or restrict form responders as required, stop deployment and have an administrator review the permissions.

## Planned Python data mapping (NOT a live connector)

The Form response tab contains sensitive raw values. Those **must stay private**. A future authorized read-only Sheets adapter, running in restricted local storage, should:

- Read `Timestamp`, `Plate`, `Province`, and `Staff-reported status` from the new Form response tab.
- Normalize and **pseudonymize** plate + province using approved private keying **before** it reaches the Python research layer.
- Convert the submission timestamp into an explicit, offset-aware `reported_at`, following the applicable Alberta local-time history.
- Pass **only** `vehicle_id`, `staff_status`, and `reported_at` to `python/src/staff_status.py`.
- Do not join future staff-reported categories into past ML features or use them as independently verified outcomes.

The validated categorical values in Python are `unknown`, `suspicious`, `violator`. Here `violator` means **historically ticketed and confirmed**, subject to checking the restricted ticket record. The Python normalizer cannot authenticate that record. A current incident remains independently assessed using `python/src/verification.py`; do not equate a prior ticket to proof of current misconduct.

## Test and deployment status

- **Focused Node.js installer mocks:** 2 passed in isolated local testing; no Google Forms API calls made.
- **Focused Python 3.13.5 validation:** 4 passed using fabricated identifiers.
- **Full existing repository suites, live Form setup, privacy configuration and retention workflow:** not run or verified for this change.
- This feature is a **separate per-plate reporting form**, not a per-row dropdown embedded inside the existing multiline round Form.

Do not upload real plates or Form responses to public GitHub, chat, or AI prompts. A complete workflow also needs authorization rules and retention tests before production use.
