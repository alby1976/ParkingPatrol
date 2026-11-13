
# Slide 1 — ParkingPatrol: Detecting Unusual Parking Patterns

## The Problem
- A customer-only parking lot has 38 spaces.
- Staff manually record vehicles during one or two inspections per day.
- Repeated observations may indicate unusual parking patterns.
- Observations alone cannot prove a parking violation.

## Research Question
Can unsupervised machine learning identify unusual repeat-parking observations compared with a simple rule-based approach?

## Methods
- Rule-based detection
- Local Outlier Factor (LOF)
- Isolation Forest

## Data
- Approximately 10 days of initial real-world observations.
- Separately generated synthetic data for software testing and demonstrations.

## Slide 2 — How ParkingPatrol Collects Data

- Customer-only parking lot with 38 spaces.
- Staff usually inspect twice daily, sometimes once.
- Google Forms records observed vehicles and timestamps.
- Google Sheets stores the inspection records.
- Arrival and departure times are not measured.
- Python analyzes observation patterns, not confirmed violations.


## Slide 3 — Understanding the Dataset

### Real Parking Data
- Initially available: approximately 10 days of observations.
- 38 parking spaces, with usually one or two inspections daily.
- No recorded arrival or departure times.

### Synthetic Dataset
- 10 simulated days.
- 18 fictional inspection rounds.
- 448 fictional vehicle sightings.
- Generated reproducibly using random seed 120.

### Important Limitation
- Synthetic records are used for testing and demonstrations only.
- Repeated observations do not prove unauthorized parking.

 ## Slide 4 — Data Cleaning and Feature Engineering

### Data Cleaning
- Normalize vehicle identifiers and timestamps.
- Remove duplicate vehicle observations within the same inspection.
- Preserve incomplete inspections and identify missing information.

### Feature Engineering (Planned)
- Number of distinct days a vehicle was observed.
- Number of inspections recording the same vehicle.
- Observation frequency relative to completed inspections.

### Why It Matters
- Models need consistent numerical inputs.
- Missing observations do not prove that a vehicle was absent.

## Slide 5 — Rule-Based Suspicious Parking Detection

### Existing Rule
- Flag a vehicle observed in two or more distinct inspection rounds on the same local day.
- Duplicate entries within one inspection count only once.
- A day with one inspection cannot trigger the two-check rule.

### Example
- Vehicle SYN_0001 appears during the 9:00 AM and 3:00 PM checks.
- Result: Suspicious — requires human review.

### Limitations
- Two observations do not prove continuous parking.
- Suspicious does not mean a confirmed violation.
- Historical Violator status requires verification of a previously issued ticket.

## Slide 6 — Unsupervised Machine Learning

### Local Outlier Factor (LOF) — Planned
- Compares a vehicle's observation features with nearby examples.
- Identifies patterns that are unusual relative to their neighbours.
- Requires sensitivity checks because the dataset is small.

### Isolation Forest — Exploratory Implementation
- Uses random partitions to identify unusual feature combinations.
- Existing Python implementation requires testing and evaluation on suitable feature data.

### Model Comparison
- Use the same features and observation window for both methods.
- Compare anomaly rankings with the two-check baseline.
- An anomaly is a review priority, not proof of a violation.

## Slide 7 — Model Comparison and Findings

### Planned Comparison
- Compare the existing two-check rule, LOF, and Isolation Forest.
- Use the same cleaned feature table and observation window.
- Examine which vehicles each method flags for review.
- Evaluate the stability of anomaly rankings when model settings change.

### Visualizations to Add
- Vehicle observation frequency chart.
- Comparison of rule-based flags versus ML anomaly flags.
- Model sensitivity or stability chart.

### Findings — To Be Completed
- Insert actual results after running and evaluating the models.
- Label synthetic demonstrations separately from real-data results.
- Do not report offender-detection accuracy without independently verified ground-truth labels.

## Slide 8 — Conclusions, Limitations and Future Work

### Conclusions — To Be Finalized
- Evaluate whether the rule-based method and unsupervised models identify useful repeat-observation patterns.
- Use anomaly detection to prioritize human investigation, not automatic enforcement.
- Report conclusions only after reviewing actual model results.

### Limitations
- Small and evolving real-world dataset.
- Usually one or two manual inspections per day.
- No recorded arrival or departure times.
- Synthetic data cannot establish real-world model accuracy.

### Future Work
- Collect more observations and assess model stability.
- Evaluate against independently verified historical records where permitted.
- Improve the secure Google Sheets-to-Python workflow.
- Maintain human verification before any new enforcement action.
