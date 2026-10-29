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

