# Synthetic parking model comparison

After each run, replace **Pending** with **Flagged**, **Not flagged**, or **Not scored** (include the reason). For LOF and Isolation Forest, add the rank when available. If the output has one row per vehicle-day, identify the synthetic day or rows the result covers.

| Pattern | What you want to check | Rule-based baseline result | Local Outlier Factor (LOF) result | Isolation Forest result |
| --- | --- | --- | --- | --- |
| A plate appears once on a day with two patrols | A single sighting should not trigger the same-day rule. | Pending | Pending | Pending |
| A plate appears in both patrols on one day | The same-day rule should flag it for review. | Pending | Pending | Pending |
| A plate appears repeatedly across a month | Check whether the month-long rule flags it and where LOF and Isolation Forest rank it. Use a month-long synthetic dataset. | Pending | Pending | Pending |

For the month-long scenario, record whether the month-long rule was available and which rule produced any flag. Use only synthetic vehicle IDs and results in this worksheet.
