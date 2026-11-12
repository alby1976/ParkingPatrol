
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


