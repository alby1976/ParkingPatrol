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
