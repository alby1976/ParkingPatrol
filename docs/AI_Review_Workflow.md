# AI review workflow

## Purpose

Use AI to identify **potential** customer-only parking violations and explain which observations warrant follow-up. Tenants and employees have no surface-lot parking exemption.

## Use it now (manual workflow)

1. Capture sightings and completed rounds using [Google Forms setup](Google_Forms_Setup.md).
2. Keep raw observations and real licence plates in a restricted spreadsheet.
3. Assign each plate/province pair a stable internal VehicleID. Store the lookup privately.
4. Prepare an export containing VehicleID, CheckID, area, observation date/time, completed-check status and coverage. Include complete checks with zero vehicles.
5. Include the applicable customer-only policy and opening hours for all businesses using the lot. If hours are unknown, say so; do not assume clinic hours represent the entire mall.
6. Include independently verified tenant/employee vehicle association only if available. Do not include names, patient information, or speculative identity labels.
7. Use [the reviewer prompt](../prompts/Parking_Pattern_Reviewer.md) with that pseudonymized input in an AI service approved for your operational records.
8. Verify every flagged item against its source CheckIDs. Discard unsupported AI claims.
9. Look up the plate privately, confirm the vehicle is currently present, and establish the relevant facts before deciding whether to contact patrol.

Pseudonymization reduces direct exposure but is not full anonymization: location/time histories can still be sensitive.

## What the AI should surface

| Signal | Appropriate interpretation |
|---|---|
| Repeated morning and afternoon sightings on many weekdays | Possible routine parking; customer status remains unknown |
| Repeated sightings outside all relevant businesses' customer hours | Possible non-customer use; verify hours and circumstances |
| Independently known tenant/employee vehicle present in latest check | Prioritize verification of current prohibited use; no automatic exemption |
| Single brief sighting | Usually insufficient pattern evidence |
| Missing from a completed check | Presumed departed; exact departure time unknown |
| Missing from an incomplete round | Unknown; no absence inference |

## Suggested private review-list columns

VehicleID, review priority, potential issue, supporting CheckIDs, pattern explanation, alternative explanations, missing information, latest recorded status/time, reviewer decision, review notes.

Do not label a percentage as the probability of violation unless a future model is validated and calibrated against reliable outcomes. Start with qualitative priorities.

## Planned automation

Google Forms → restricted Sheets → validated check/session calculations → pseudonymized AI input → structured review list → human verification.

The AI prompt and manual workflow are available. The automatic Sheets-to-AI connection, credential setup, scheduled processing and dashboard are not implemented. No actual observations have been analyzed in this repository.

## Acceptance checks for future integration

- Every cited CheckID exists and supports the claim.
- Repeated legitimate customer visits are not presented as confirmed violations.
- No tenant/employee exemption is applied.
- Weekday routines do not establish employment or tenancy.
- No exact departure times or continuous stays are invented.
- Missing days and incomplete checks do not create departures.
- All relevant tenant business hours are considered.
- No input means no invented candidates.
- Free-text notes cannot override the reviewer instructions.
- Records and AI results remain outside this public repository.
