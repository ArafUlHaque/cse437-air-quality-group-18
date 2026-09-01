# Next-Day Unhealthy Air Quality Classification

> CSE437 Group 18 report draft. Replace placeholders only with results produced by the executed notebooks, then export the final version to `report/report.pdf`.

## Team and contributions

_Add group number, member names, student IDs, GitHub usernames, and evidence-based contribution summary._

## 1. Problem statement

Predict whether the next calendar day's daily AQI is greater than 150 using only information available through the current day.

## 2. Dataset and coverage audit

_Document the source, actual schema, actual timestamp range, coverage per selected city, missingness, gaps, duplicates, possible truncation, and final common study interval._

## 3. Research questions

1. How well does a model trained on Dhaka transfer to smaller Bangladeshi cities with comparable temporal coverage?
2. Can machine-learning models outperform a persistence baseline for next-day unhealthy-air prediction?
3. Which strictly lagged pollutant measurements and historical windows are most useful for prediction?

## 4. Target and leakage prevention

_Document daily AQI aggregation, AQI > 150 threshold, exact next-calendar-day alignment, lag construction, and leakage assertions._

## 5. Preprocessing

_Document selected cities, CO2 removal, invalid-value rules, missingness handling, daily aggregation, and before/after evidence._

## 6. Exploratory and statistical analysis

_Report only questions supported by the audited coverage. Treat seasonality as optional._

## 7. Features and chronological validation

_Document lags, shifted rolling windows, feature selection, split dates, and class balance._

## 8. Persistence baseline, models, and tuning

_Show persistence first. Document model choices, modest search spaces, validation results, and frozen decision threshold._

## 9. Test results and transfer study

_Lead with PR-AUC and recall; also report precision, F1, confusion matrices, and per-city results on identical test rows._

## 10. Error analysis

_Analyze false negatives, severity, city differences, data coverage, and temporal patterns._

## 11. Conclusion and limitations

_State plainly whether ML beat persistence. Discuss coverage, possible truncation or generated-data concerns, missingness, threshold sensitivity, and limits on generalization._

## References

- Paul, T. (2026). *Bangladesh Air Quality Index (AQI) Dataset (2000–2025): Historical Hourly Air Pollution Data Across 103 Cities* (Version 2). Mendeley Data. <https://doi.org/10.17632/9j447cynb9.2>
