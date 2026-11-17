# ParkingPatrol: Exploring Unusual Repeat-Parking Observation Patterns

**DATA120 Mini Capstone — One-Page Project Summary | Proposal (results pending)**

### Background and research question
A Calgary medical clinic has a **38-space, customer-only** parking lot. Staff inspect it approximately once or twice daily and enter observed licence plates and timestamps through Google Forms/Sheets. Arrival and departure times are not recorded; repeat sightings alone cannot establish continuous parking or a violation. **Research question:** Can unsupervised machine learning identify unusual repeat-sighting patterns compared with a transparent rule, while accounting for irregular inspections?

### Data and analytics plan
The initial dataset contains approximately **10 days of real observations**, usable only with appropriate authorization and privacy safeguards. Separately, reproducible **synthetic** data (10 days, **18 checks, 448 fictional sightings**) will support testing and demonstrations, not claims about real vehicles. In Python/pandas, the project will normalize observations, deduplicate repeated entries within the same inspection, and create features for each pseudonymous vehicle: distinct observed dates, distinct inspections with a sighting, comparable completed inspection rounds, and the fraction of completed checks with a sighting. Unperformed checks and missing observations will not be interpreted as proven absence or parking duration.

The analysis will compare **(1) a rule-based baseline** flagging sightings in two or more *distinct* rounds on the same local day, **(2) Local Outlier Factor (LOF)** for local-density anomalies, and **(3) Isolation Forest** for unusual combinations of features. **If time permits**, a **fourth, optional k-nearest-neighbours (kNN) distance-based anomaly score** will be explored—not supervised kNN classification. Methods will be evaluated using flagged-case overlap, anomaly rankings, parameter sensitivity, and inspection-frequency effects on the same appropriate feature inputs. A small sample may limit feasible model settings and conclusions.

### Similar research and expected contribution
Ma et al. (2024) review machine-learning approaches in urban parking prediction, demonstrating the relevance of data-driven parking management but not establishing unauthorized parking from repeated sightings. Breunig et al. (2000) introduced LOF, and Liu et al. (2008) introduced Isolation Forest, providing established anomaly-detection foundations. ParkingPatrol applies these ideas to **intermittent manual observations**, with an interpretable baseline and explicit human review. Outputs will be **review priorities**, never automatic ticketing/towing decisions; without independently verified violation labels, no offender-detection accuracy will be claimed.

### References (APA style)
Breunig, M. M., Kriegel, H.-P., Ng, R. T., & Sander, J. (2000). LOF: Identifying density-based local outliers. *Proceedings of the 2000 ACM SIGMOD International Conference on Management of Data*, 93–104. https://doi.org/10.1145/342009.335388

Liu, F. T., Ting, K. M., & Zhou, Z.-H. (2008). Isolation forest. *2008 Eighth IEEE International Conference on Data Mining*, 413–422. https://doi.org/10.1109/ICDM.2008.17

Ma, C., Huang, X., & Li, J. (2024). A review of research on urban parking prediction. *Journal of Traffic and Transportation Engineering (English Edition), 11*(4), 700–720. https://doi.org/10.1016/j.jtte.2023.11.004

*Academic integrity: This is an AI-assisted proposal draft for the student's review; verify assignment-specific AI rules, references, and final pagination before submission.*
