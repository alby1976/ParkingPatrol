# Synthetic Dataset Sensitivity Analysis

**Project:** ParkingPatrol — DATA120 Mini Capstone  
**Related GitHub issue:** #7

## Objective

Examine whether increasing the synthetic observation period from 10 to 30 days changes the behaviour of the two-check rule, Isolation Forest, and Local Outlier Factor (LOF).

## Experimental Results

| Metric | 10 days | 30 days |
|---|---:|---:|
| Inspection rounds | 18 | 55 |
| Vehicle sightings | 448 | 1,374 |
| Vehicle-day observations | 315 | 965 |
| Distinct feature patterns | 23 | 79 |
| Largest duplicate group | 74 | 117 |
| Two-check rule flags | 133 (42.2%) | 409 (42.4%) |
| Isolation Forest flags | 32 (10.2%) | 97 (10.1%) |
| LOF scored rows | 0 | 0 |

Both datasets were generated with random seed 120, using the existing synthetic-data generator.

## Findings

The extended 30-day dataset contained more observations and distinct feature patterns, but feature diversity increased only slightly, from 7.3% to 8.2%.

The two-check rule produced similar flagging rates across both periods. Isolation Forest also flagged approximately 10% of observations, consistent with its configured contamination parameter.

LOF remained unscored because the largest duplicate-feature groups exceeded its configured 20-neighbor threshold.

## Limitations

These datasets contain fictional observations and are not independent real-world samples. The 30-day dataset extends the same seeded simulation process.

Anomaly flags do not establish unauthorized parking. No detection accuracy, precision, or recall can be inferred without independently verified ground-truth labels.

## Conclusion

Increasing the synthetic observation period alone did not resolve LOF's duplicate-neighborhood limitation. Future experiments should prioritize meaningful feature variation and sensitivity to inspection conditions rather than simply increasing the number of observations.


---

## November 23, 2026 — S18 Realistic Inspection Sensitivity Analysis

### Objective

Evaluate how adding a complaint-triggered inspection affects rule-based detection, Isolation Forest and Local Outlier Factor (LOF).

The revised dataset simulates 10 days of activity in a 38-stall customer-only parking lot.

### Dataset

- Random seed: 120
- Completed inspections: 20
- Routine inspections: 19
- Complaint-triggered inspections: 1
- Vehicle sightings: 480
- Vehicle-day records: 321
- Unique feature patterns: 66
- Largest identical feature group: 57

### Model comparison

| Metric | Routine only | All inspections |
| --- | ---: | ---: |
| Inspections | 19 | 20 |
| Vehicle-day records | 315 | 321 |
| Rule-based flags | 118 | 137 |
| Isolation Forest flags | 32 | 30 |
| LOF | Unscored | Unscored |

Isolation Forest used contamination=0.10. The two scenarios were fitted separately.

### Rule-based findings

Including the complaint-triggered inspection produced:

- 19 newly flagged vehicle-day records
- 0 previously flagged records losing their flag
- 118 records flagged in both scenarios

All 19 newly flagged records already existed in the routine-only dataset.

This demonstrates sensitivity to inspection frequency rather than evidence of additional parking violations.

### Isolation Forest findings

Comparing the two separately fitted models:

- 22 vehicle-day records remained flagged.
- 8 existing records became flagged.
- 10 existing records lost their flags.
- 0 newly observed records became flagged.

Thus, 18 classifications changed, even though the total number of flags decreased by only two.

The Jaccard agreement between the flagged sets was 22/40 = 55%.

These differences reflect changed observation features and model refitting. Their separate contributions have not been isolated.

### LOF findings

LOF remained unscored because identical feature patterns overwhelmed its configured neighbourhood.

The realistic dataset contained 66 unique feature patterns among 321 vehicle-day records, with a largest identical group of 57.

An unscored model is not equivalent to a model detecting zero anomalies.

### Interpretation and limitations

- Customer complaints and extra inspections create nonrandom observation opportunities.
- Repeated sightings do not establish continuous parking duration.
- Model flags are candidates for human review, not confirmed violations.
- No independently verified violation labels were available for estimating precision, recall or accuracy.
- Simulation probabilities are assumptions, not measured clinic frequencies.
- Additional seeds and inspection schedules are needed to assess stability.

### Preliminary conclusion

Adding one complaint-triggered inspection increased rule-based flags from 118 to 137.

Isolation Forest changed 18 individual classifications despite producing similar total flag counts.

The experiment demonstrates inspection-sampling sensitivity, not predictive accuracy.

Related GitHub issue: #7


---

## November 24, 2026 — S19 Multi-Seed Stability Analysis

### Objective

Examine whether rule-based detection, Isolation Forest and LOF behave consistently across five fictional parking datasets generated with different random seeds.

### Experimental configuration

- Random seeds: 120, 121, 122, 123, 124
- Observation period: 10 simulated days per seed
- Parking capacity: 38 stalls
- Midday inspection skip probability: 0.25
- Optional afternoon inspection probability: 0.25
- Customer complaint probability: 0.25
- Simulated occupancy rate: 0.65
- Isolation Forest contamination: 0.10

All probabilities are experimental assumptions, not measured clinic frequencies.

### Results

| Seed | Inspections | Sightings | Vehicle-days | Rule flags | Isolation Forest flags | LOF scored |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 120 | 20 | 480 | 321 | 137 | 30 | 0 |
| 121 | 21 | 526 | 341 | 161 | 34 | 0 |
| 122 | 19 | 499 | 354 | 113 | 35 | 0 |
| 123 | 23 | 567 | 354 | 185 | 33 | 0 |
| 124 | 22 | 551 | 358 | 158 | 33 | 0 |

### Flag-rate stability

| Statistic | Rule-based | Isolation Forest |
| --- | ---: | ---: |
| Mean | 43.6% | 9.5% |
| Minimum | 31.9% | 9.2% |
| Maximum | 52.3% | 10.0% |
| Range | 20.4 percentage points | 0.8 percentage points |

Rule-based review flags varied considerably across the five synthetic scenarios.

Isolation Forest flagged approximately 10% of vehicle-day records, consistent with its configured contamination parameter. This does not establish predictive accuracy or stability of individual flagged vehicles.

LOF scored zero records across the five scenarios. It should be reported as **unscored**, not as detecting zero anomalies.

### Reproducibility

The multi-seed evaluator returned identical summary DataFrames when run twice with seeds 120–124.

The student reported:

- Five-seed evaluation test: passed
- Reproducibility test: passed
- Flag-count validation test: passed
- Full Python regression suite: 70 passed in 6.85 seconds

### Limitations

- The five datasets are synthetic, not independent real-world samples.
- Changing the random seed affects inspection scheduling and vehicle observations together.
- The experiment does not isolate inspection-frequency effects from other simulation changes.
- Isolation Forest contamination influences its overall flag rate.
- LOF could not provide anomaly predictions on these datasets.
- No independently verified violation labels were used.
- Accuracy, precision, recall and enforcement effectiveness cannot be established.

### Conclusion

The five-seed experiment found substantial variation in rule-based flag rates, while Isolation Forest's overall flag rate remained close to its configured contamination level.

LOF remained unscored in every scenario.

These results support further investigation of inspection-adjusted statistical methods and better observation data, rather than claims of demonstrated violation-detection accuracy.

Related GitHub issue: #7
