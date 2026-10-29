# Install Google Forms → Sheets → AI

## What this builds

One Google Form for each parking round, a private Google Sheet, and an Apps Script worker that checks for new data every 15 minutes. The AI proposes vehicles to review and explains why. No exact departure time is needed.

**Code is built; activation happens in your own Google account.** No live Google resources or API credentials are bundled in this repository.

## 1. Create your private Sheet

1. Open [Google Sheets](https://sheets.google.com).
2. Create a blank spreadsheet named **ParkingPatrol — Private**.
3. Keep Share → General access restricted. Give access only to authorized managers.
4. Select **Extensions → Apps Script**.
5. Name the script project **ParkingPatrol**.

## 2. Copy the two code files

1. Open [apps-script/Code.gs](../apps-script/Code.gs) in GitHub. Select **Raw**, then copy the entire file.
2. In Apps Script, replace the contents of its default **Code.gs** with that code.
3. Select **+ → Script**, name the second file **Core**, and paste all of [apps-script/Core.gs](../apps-script/Core.gs).
4. In Apps Script **Project Settings**, enable **Show appsscript.json manifest file in editor**.
5. Open appsscript.json and replace it with [apps-script/appsscript.json](../apps-script/appsscript.json).
6. Save. Do not paste an API key into either code file or into GitHub.

## 3. Run the installer

1. In the function dropdown, choose **setupParkingPatrol**.
2. Select **Run** and authorize this script in your Google account.
3. If Google identifies your own newly created project as unverified, review the project and requested access before choosing to proceed. Organization policy may require your administrator.
4. Return to the spreadsheet and reload it.
5. Open the **Setup** tab. It contains your Form edit link and responder link.

The installer creates the Form, response destination, Setup, Review, Runs and VerifiedAssociations tabs, and one 15-minute trigger for the installing account. The Form starts unpublished/closed and AI starts disabled. Re-running setup reuses its saved Form and avoids duplicate triggers for that account. Use one installing account; Google triggers are owned by their creator.

The script requires Google Forms access to create/read the Form, Sheets access to write results, trigger-management access for the worker, and external-request access to call OpenAI. It does not request Gmail or send messages.

## 4. Restrict and open your Form

1. Open the Form edit link from Setup.
2. Use the Form's publishing/sharing controls to allow only your authorized observer accounts to respond. Do not enable public response summaries.
3. Publish the Form after restricting responder access. On older Forms interfaces, turn **Accepting responses** on.
4. Open the responder link on your phone and bookmark it.
5. Do not rename or delete the four generated questions. Do not enable one-response-per-person: you will submit many rounds.

Google account and administrator settings may change the available access controls. Verify that an unauthorized account cannot submit before using real records. Keep both the Sheet and script editor access restricted: script editors can read Script Properties, including the API key.

## 5. Add your OpenAI API configuration

Use an OpenAI API project with API access/funding and an API key. Do not send the key in chat.

In Apps Script, open **Project Settings → Script properties → Edit script properties**. Keep the properties created by setup and add/update:

| Property | Value |
|---|---|
| OPENAI_API_KEY | Your API key, entered privately here |
| OPENAI_MODEL | gpt-4o-mini, or another available Responses model supporting strict JSON Schema |
| ENABLE_AI | true |
| LOOKBACK_DAYS | 60 (allowed: 1–365) |
| MAX_CALLS_PER_DAY | 12 (allowed: 1–96) |
| BUSINESS_HOURS | All businesses' customer hours, or leave the default Unknown |

The default model is configurable, not a claim about the newest model. Model access depends on your API project. Requests use the OpenAI Responses API with strict structured output and store:false. That setting is not a promise of zero provider retention; use your organization's approved data arrangements.

The daily cap limits attempted API calls, not a dollar budget. Requests that fail can still consume a slot. Also configure spending controls in your API project. Unchanged analysis input is skipped after a successful run.

## 6. Test with fictional plates first

Submit three rounds in chronological order, using the same area name:

1. Round 1: **ABC123, AB** in Plates present; select **Yes** for every vehicle recorded.
2. Round 2: **ABC123, AB** again; select **Yes**.
3. Round 3: leave Plates present empty; select **Yes**.

Separate submissions normally have different timestamps. For historical testing, use an explicit timestamp with offset in the optional field; for example **2026-10-29T09:00:00-06:00**. Use the correct actual date, time and offset for your records. Calgary normally uses -06:00 in daylight time and -07:00 in standard time; the explicit offset distinguishes repeated fall-back hours. Future timestamps beyond five minutes are rejected.

Then select **ParkingPatrol → Analyze now** in the Sheet.

- **Runs** should show SUCCESS.
- **Sessions** should show first and last sightings and the first absent check. There is no departure-time field.
- **Review** may contain no candidate: three test sightings do not necessarily demonstrate a meaningful pattern. A header-only Review after SUCCESS means the AI found no candidates.
- **DataIssues** lists malformed readings or duplicate area/time rounds.

Delete the fictional responses in the Form before collecting real data, and remove their rows from its linked response sheet separately. The worker reads the Form responses, not manual changes to the linked response sheet.

## 7. Your everyday routine

1. Open the Form on your phone.
2. Enter **Whole Lot** (or the same fixed area name every time).
3. Leave Observation time blank when submitting during the check.
4. Enter one plate per line, with province:

   ```text
   ABC123, AB
   XYZ789, AB
   ```

5. Select **Yes** only if you recorded every vehicle in that area; otherwise select **No**.
6. Submit once for the entire round. An empty completed round is important: it establishes presumed absence for previously seen vehicles.
7. Check Review after the next scheduled run, or choose Analyze now.

No separate CheckID entry or departure entry is required. The Form response ID is the CheckID. A '?' or malformed plate line makes the entire round incomplete for absence inference, while valid plate lines still contribute sightings. Correct mistakes rather than guessing O versus 0.

## 8. Known tenant/employee vehicles

In **VerifiedAssociations**, optionally enter Plate, Province, tenant or employee, and TRUE only when independently verified. No names are required. This prioritizes review; it creates no parking exemption. A vehicle association does not establish who used it on a particular visit.

## Results and limits

- Review contains private plates, qualitative priority, last-seen time, AI explanation, supporting CheckIDs, alternative explanation and next check.
- Review is replaced by each successful analysis. Keep human decisions in a separate private tab; do not type them into the generated Review tab.
- Sessions and DataIssues are generated tabs too. Never edit them as source data.
- Only the configured lookback window is analyzed. A visit already in progress before that window has an unknown beginning.
- No vehicle counts are silently truncated. Analysis stops above 100 vehicles, 1,000 checks in the window, 180,000 JSON characters, or 5,000 total Form responses. Shorten the analysis window or arrange a larger implementation. For the total-response limit, archive/delete old Form records under your retention policy before continuing.
- A successful AI response can still contain a misleading interpretation. ID/evidence checks reject invented references but cannot prove every sentence is true. Verify the cited observations.
- Latest-recorded presence is not current presence. Confirm the vehicle is still there and review actual prohibited use before contacting patrol.

## Pause, repair and troubleshoot

Select **ParkingPatrol → Pause AI** to stop API calls. To resume, set ENABLE_AI to true. The Form continues collecting responses while paused.

| Runs message | What to do |
|---|---|
| HTTP_401 | Correct/revoke-and-replace the API key in Script Properties |
| HTTP_403 / HTTP_404 | Check API project/model access and model name |
| HTTP_429 | Check API quota/rate limits; wait for the next scheduled run |
| DAILY_CALL_CAP | Wait until the next Edmonton calendar day, or deliberately raise the cap |
| INVALID_OBSERVATION_TIME | Correct a malformed, impossible or future historical timestamp |
| INVALID_AREA / INVALID_COMPLETION | Restore question titles and required answers; correct invalid responses |
| LIMIT_* | Reduce history size or archive records; no partial analysis is published |
| AI_* / ANALYSIS_FAILED | Prior Review may be stale. Check configuration and source records; retry Analyze now |

Failed analyses preserve prior results and add a stale-results note to Review A1. Check Runs before acting on results. Network bodies and API keys are not written to logs. A scheduled run with AI disabled or unchanged successful input makes no new Runs row.

To correct source data, delete the erroneous response in the Form and resubmit the corrected round using its original observation timestamp; remove the obsolete linked-sheet row separately if needed. Do not submit a second conflicting round at the same area/time without removing the original. Re-analysis rebuilds the window's inferred visits from the Form.

The lookback window does not delete stored records. Set and follow a retention policy covering Forms, linked response sheets, generated tabs, logs, exports and provider data. Pseudonymization is not full anonymization.

## Validation

Run `node --test tests/parking.test.cjs` from the repository root. Tests cover session inference, incomplete checks, uncertain readings, duplicate rounds, plate/province separation, evidence validation, API request/response handling, credential-safe failures, pseudonymization, unchanged-input skipping and pausing.

Local tests use mocked Google/API services. A live Google authorization and API smoke test must be completed in your account using step 6; this repository has not performed that live test.

## Official implementation references

- [Google Forms service](https://developers.google.com/apps-script/reference/forms/form)
- [Apps Script installable triggers](https://developers.google.com/apps-script/guides/triggers/installable)
- [OpenAI structured outputs](https://developers.openai.com/api/docs/guides/structured-outputs)
