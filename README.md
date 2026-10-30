## Retention exception: flagged vehicles are preserved

Only expired **Assumed customer** source records are eligible for deletion. Potential offenders (recurring-use rules, verified prohibited association or stored AI finding), most likely offenders, and manually confirmed offenders are protected. Confirmation tags no longer expire automatically. Use a dated explicit ManualTags **Assumed customer** correction to release protection; Clear tag returns to automatic classification.

Cleanup considers all stored observations rather than the analysis lookback, so an old flagged vehicle is not silently reclassified just because it disappeared from the current review window. Stored AI findings continue protecting their vehicle until manually cleared as an assumed customer. Associated evidence/tag records are preserved with the plate.

A Form response contains a whole round and cannot selectively redact one original answer. If an expired round contains a protected vehicle or an uncertain plate reading, **the entire round and linked row are retained**, including any customer observations in that same round. No source record is deleted merely because it is old while classification is uncertain. Generated views may still be cleared and rebuilt from protected source history; exports and Google revision history are outside the cleanup scope.

Automatic/Manual controls remain in Settings. Manual suppresses all automatic source deletion; it does not erase flags. This repository change must also be installed in the live Google project.

## Monthly AI escalation

The same vehicle and stable AI pattern code, supported by distinct dated sightings across at least one calendar month, escalates to **Most likely offender**. **Confirmed offender** manual tags remain unchanged. Explicit manual Assumed customer overrides are also respected until cleared or expired.

AIPatternHistory stores VehicleID, pattern code, observation date and source CheckID privately. Each successful AI review records only its latest supported sighting date for that pattern; re-running unchanged evidence cannot age a flag, absence checks cannot count as sightings, and a first retrospective analysis cannot create a month of prior AI detections. At least two separately dated AI-supported findings must span the calendar-month anniversary (month-end clamped). This does not claim continuous parking or observation between checks. General “other” patterns never escalate.

Pattern findings older than three months stop influencing status even when Manual deletion is selected. Physical history deletion follows the retention mode. Automatic rules alone cannot cause this AI escalation; AI must be enabled and successfully run. Review labels are not probabilities or proof of violations.

Update **Code.gs, Core.gs and Retention.gs**, then run setupParkingPatrol to create AIPatternHistory. This change is on GitHub and not yet installed in the live Google account.

## Vehicle status logic

CurrentRoundReview now includes Parking status and Status source. Every newly seen vehicle defaults to **Assumed customer**, unless recurring-use rules, a verified prohibited association, or optional AI flags it as **Potential offender**. Neither rules nor AI can assign Confirmed offender.

Run setupParkingPatrol after updating Code.gs and Retention.gs to create **ManualTags**. Enter Plate, Province, Status, factual Reason (no names), and ReviewedAt (a Google Sheets date/time). The status dropdown allows **Confirmed offender**, **Assumed customer**, or **Clear tag**. Use **ParkingPatrol → Apply manual status changes** to refresh. The newest valid tag wins; duplicate timestamps are rejected. Assumed customer is an explicit manual override of automatic flags; Clear tag removes that override and lets current rules/AI decide again. Manual tags stay private and are not sent to AI.

Tags stop affecting status after three calendar months from ReviewedAt, even in Manual deletion mode. Physical tag-row deletion follows the selected retention mode. A continued/new sighting alone does not refresh a manual confirmation. Re-review and date a tag to renew it. No tag identifies the driver or proves the vehicle is still present.

These changes are synced to GitHub; the Google installation must be updated and setupParkingPatrol rerun before the ManualTags sheet and menu appear.

## Retention controls

After installing the latest Code.gs and Retention.gs, run setupParkingPatrol to create **Settings**.
**Settings!B2** is a dropdown: **Automatic** (default for a new Settings sheet) or **Manual**.
Re-running setup preserves your chosen mode. Automatic removes expired records once per Edmonton calendar day through the scheduled/recovery or completed-round handler. Manual stops automatic deletion; round processing continues. In Manual mode, stored records can exceed three months until you press cleanup.

Use **ParkingPatrol → Delete expired records now** in either mode. It asks for confirmation before permanent Form-response deletion, then rebuilds results. Optionally insert a drawing in Sheets and assign the script name **manualRetentionCleanup** (without parentheses) to use a visible sheet button. This repository provides the menu button; a drawing is optional and has not been inserted.

Invalid or missing mode stops the scheduled handler rather than guessing permission to delete. Run setup if Settings is missing. Do not rename the Settings tab or move its B2 control. GitHub sync does not install these controls into your live Google account.

## Three-month retention cleanup

Install **apps-script/Retention.gs** as a third script file alongside Code.gs and Core.gs, replace Code.gs with the current repository version, then run setupParkingPatrol. GitHub sync does not deploy this to Google.

Cleanup runs before analysis of a submitted completed round, before Analyze now, and at least daily through the existing 15-minute recovery trigger, even with AI disabled. Cutoff is the start of the Edmonton calendar day three months earlier, clamped to the last valid day of the target month. Records exactly at the cutoff are retained.

It deletes expired Form responses and the corresponding linked response-sheet rows by observation time (submission time when observation time is blank). Independently stored copies in both sources are checked. Invalid dates or ambiguous linked-sheet identification stop cleanup before source deletion. Source deletion is permanent and not transactional; after a partial failure the next scheduled run retries. Generated Review, CurrentRoundReview, RoundStatus, Sessions, DataIssues and Runs are cleared before deletion and rebuilt by subsequent analysis. VerifiedAssociations plates with no retained sightings are removed as well, including pre-entered vehicles not yet observed.

No exports, personal copies, Google version history/backups, provider logs or data already sent to an AI service can be erased by this script. This is application-level cleanup, not a guarantee of provider-level permanent erasure. No automatic archives are created. The analysis lookback window remains separate from the storage-retention period.

Run all tests with `node --test tests/*.test.cjs`. Local tests passed; live deletion has not been run or verified in your Google account.

> **Current workflow:** Completed Form submissions start processing automatically. The 15-minute trigger is a recovery check. **CurrentRoundReview** and **RoundStatus** update without an API key, with AI disabled, or before an optional AI request fails. AI explanations remain in **Review** and must be checked against Runs for freshness.
>
> Basic rules flag verified tenant/employee vehicle associations and vehicles seen on at least three distinct local dates in the analysis window. These are review signals, not proof of non-customer use. Only vehicles seen in the latest check of each area appear in CurrentRoundReview; check the area's timestamp and completion status. InferredAreaVisits counts area visits, not proven property-wide visits. No exact departure times are assigned.
>
> **Existing Google installation:** GitHub sync does not deploy Apps Script. Replace Code.gs with the new repository version and run setupParkingPatrol once to install the Form submission trigger. No API key is needed for basic processing. Keep ENABLE_AI=false until optional AI is configured. Form results are asynchronous: open the Sheet after submission; they are not embedded live in the Google Form confirmation page. The older AI-specific instructions below apply only to optional AI.

# ParkingPatrol

A parking-observation project for a private strip-mall surface lot with customer-only parking.

## Surface-lot parking policy

**Customers only. Tenants and employees are not allowed to park in the surface lot.**

Do not authorize a vehicle because it belongs to a tenant or employee, create tenant/employee exemptions, or suppress their vehicles from review. Independently known tenant/employee association can be noted factually in restricted operational records. Repeated sightings alone do not prove that association or a violation.

## AI pattern review

Use the [AI review workflow](docs/AI_Review_Workflow.md) and [reusable reviewer prompt](prompts/Parking_Pattern_Reviewer.md) to flag potential non-customer parking patterns with supporting check references. Review priorities are qualitative, not probabilities of a violation. The automatic Google Forms → Sheets → OpenAI connection is implemented as installable Apps Script. Activation and a live test in your Google account are still required.

## Current status

The repository includes the Form installer, automated check/session analysis, OpenAI Responses API integration, private review-sheet output, a 15-minute worker, and automated tests. It has not been installed or authorized in a Google account here; no live API test has run.

## Start here

1. Follow [Install Google Forms → Sheets → AI](docs/INSTALL_AI_CONNECTION.md). The installer uses one submission per completed or partial parking round.
2. Record every vehicle present during each parking check.
3. Mark the check complete, including a check where the area is empty.
4. Use the rules below to interpret sightings.
5. Review current circumstances and authorization before calling parking patrol.

## Agreed observation rules

- Exact arrival and departure times are not tracked or required.
- Record the observation date and time for each parking check.
- Each check has a unique CheckID and a clearly identified area.
- A check is complete only when every vehicle in that area has been recorded.
- When a previously present plate is absent from the next completed check of the same area, mark the vehicle as **presumed departed**.
- Do not assign an exact departure time. Preserve LastSeenAt and FirstAbsentCheckAt.
- A later sighting after confirmed absence starts a new inferred visit.
- Repeated sightings without an intervening completed absence are treated as the same inferred visit; leaving and returning between checks cannot be ruled out.
- Incomplete checks do not establish absence.
- A check of another area does not establish absence in the original area.
- No check on a day means unknown status, not presumed departure.
- Midnight does not automatically close a visit.
- Plate and province/state together identify a vehicle for matching. Preserve original entries and flag ambiguous plate readings for review.
- Duplicate entries within a check count as one sighting.

## Example (fictional plate)

| Completed check | ABC123 / AB | Interpretation |
|---|---|---|
| Monday 09:00 | Present | First seen |
| Monday 12:00 | Present | Same inferred visit |
| Monday 15:00 | Absent | Presumed departed |
| Tuesday 09:00 | Present | New inferred visit |

Report: **Seen Monday at 09:00 and 12:00; absent at the 15:00 check.** Do not report an exact arrival, departure, or proven continuous parking duration.

## Proposed analysis

- Distinct days seen per vehicle.
- Distribution of sightings by weekday and time of day.
- Inferred visit count based on completed checks.
- First and last sightings within each inferred visit.
- First completed absence following each visit.
- Repeated weekday routines and repeated observations outside configured business hours.
- Review of independently known tenant/employee vehicles under the no-tenant/no-employee surface-lot policy; no automatic exemptions.
- A review list explaining the observations behind each flag.

Time between sightings is an observation span, not proven continuous occupancy. Frequency or length alone does not establish that a vehicle belongs to a non-customer. Do not invent a time limit when the posted rule is customer-only.

## Human review

Flags mean **review required**, not a confirmed violation. Verify the vehicle is currently present, review applicable permissions and posted rules, and provide factual observations to patrol. The patrol provider determines whether enforcement is justified. No automatic reporting, ticketing, owner lookup, or driver identification is included.

## Data handling

This repository is public. Keep real plates, photos, response exports, vehicle-association records, credentials, and generated reports in restricted operational storage outside Git. Use fictional examples in code and documentation. Keep clinic patient records and appointment details out of parking records.

Before operating, establish appropriate collection authority, access controls, retention/deletion rules, and provider evidence requirements. A parking restriction sign alone does not resolve the privacy requirements for systematic tracking.

## Implementation

Google Forms (one round per submission) → restricted Google Sheets / Apps Script → deterministic session analysis → pseudonymized OpenAI review → private Review sheet → human verification.

Source: [Code.gs](apps-script/Code.gs), [Core.gs](apps-script/Core.gs). Test: `node --test tests/parking.test.cjs`. Scheduled runs check for changed data every 15 minutes; API use is disabled until configured. No external alerts or patrol calls are made.

AI is optional: the core session rules should be reproducible calculations. Any AI summary should distinguish recorded facts from assumptions and can use internal vehicle IDs rather than actual plates.

