# Google Forms setup — step by step

## What you will use

Use two staff-only Google Forms linked to restricted Google Sheets:
- **Vehicle Sighting**: one submission per vehicle per check.
- **Complete Parking Check**: one submission when you finish checking an area, including when no vehicles are present.

These are setup instructions; the forms have not been created automatically.

## Surface-lot parking policy

**Customers only. Tenants and employees are not allowed to park in the surface lot.**

Do not authorize a vehicle because it belongs to a tenant or employee, create tenant/employee exemptions, or suppress their vehicles from review. Independently known tenant/employee association can be noted factually in restricted operational records. Repeated sightings alone do not prove that association or a violation.

## 1. Choose your areas

If you always inspect the entire lot, use one area: Whole Lot.
If you inspect different parts separately, assign fixed names such as North Lot and South Lot.

Absence can only be inferred within the area that was checked completely.

## 2. Choose a CheckID

Use a unique ID for every check of an area, for example:
20261029-0900-WHOLELOT

Use the same CheckID on every vehicle submission and on the completion submission.
Set spreadsheet display times to America/Edmonton. Use an explicit local observation date and time for older handwritten records; form submission time is not necessarily observation time.

## 3. Create Vehicle Sighting

In Google Forms, create these questions:

| Question | Suggested type | Required |
|---|---|---|
| CheckID | Short answer | Yes |
| Area | Dropdown | Yes |
| Check observation date | Date | Yes |
| Check observation time | Time | Yes |
| Licence plate | Short answer | Yes |
| Province/state | Dropdown with Other | Yes |
| Plate reading uncertain? | Yes/No | Yes |
| Vehicle colour/type | Short answer | No |
| Stall/location | Short answer | No |
| Observer initials | Short answer | Yes |
| Factual notes | Paragraph | No |

Do not ask for departure time. Do not collect customer names or clinic appointment information.
Preserve original plate text. Analysis may uppercase and trim spaces, but must not silently merge ambiguous characters such as O and 0.

## 4. Create Complete Parking Check

| Question | Suggested type | Required |
|---|---|---|
| CheckID | Short answer | Yes |
| Area | Same dropdown | Yes |
| Check observation date | Date | Yes |
| Check observation time | Time | Yes |
| Did you record every vehicle in this area? | Yes/No | Yes |
| Number of distinct vehicles recorded | Number | Yes; allow zero |
| Observer initials | Short answer | Yes |
| Notes about missed areas or problems | Paragraph | No |

Submit Yes only after recording all vehicles. A No means incomplete and cannot establish any departure.

## 5. Link responses

For each form, open Responses and select Link to Sheets.
Use the same restricted workbook with separate response tabs if your setup permits, or two restricted workbooks.
Restrict form access to authorized observers and spreadsheet access to authorized managers. Do not publish response summaries or spreadsheets.

## 6. Do a parking round

1. Choose the area and CheckID.
2. Walk the area and submit every plate using Vehicle Sighting.
3. Review entries for mistakes.
4. Submit Complete Parking Check.
5. If the area is empty, submit completion with zero vehicles.
6. If interrupted, submit No or leave the round incomplete.

Never mark a check complete merely because one plate of interest was recorded.

## 7. Analysis contract

Future automation should:
- Validate consistent CheckID, area, observation timestamp and completion metadata.
- Reject duplicate/conflicting completion records for review.
- Compare the stated distinct vehicle count with deduplicated sightings; mismatches invalidate absence inference until corrected.
- Exclude uncertain plate readings from definitive absence inference until reconciled, so a typo does not create a false departure.
- Process checks chronologically, independent of submission order.
- Leave incomplete or inconsistent rounds out of absence inference.
- Close an inferred visit only when a valid completed check of its area lacks the vehicle.
- Store FirstSeenAt, LastSeenAt, FirstAbsentCheckAt, Sightings and PresumedDeparted.
- Leave departure time unknown.
- Treat a subsequent sighting after absence as a new inferred visit.
- Recompute affected history after corrections or backdated imports.
- Keep empty completed checks; they close previously open visits for that area.
- Avoid interpreting movement between separately checked areas as a confirmed departure from the entire property.

## 8. Existing handwritten notes

Enter historical notes with their actual observation date/time.
Only mark historical rounds complete if you know every vehicle in the relevant area was recorded. Otherwise, import the sightings as incomplete historical observations. They can support frequency summaries but cannot establish absence.

## 9. Before enforcement use

Test with fictional plates first:
- Present → present → absent → present produces two inferred visits.
- An incomplete round never closes a visit.
- An empty completed round establishes presumed absence.
- No round on a day leaves status unknown.
- A different-area check does not close the original-area visit.
- Same plate number in different provinces remains distinct.
- Duplicate sightings do not inflate counts.
- A midnight boundary does not close a visit.

These are acceptance scenarios for future implementation, not a claim that an analyzer is already installed.
