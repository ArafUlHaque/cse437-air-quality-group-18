# Next-Day Unhealthy Air Quality Classification

> CSE437 Group 18 report draft. Add later results only when they are produced by executed notebooks, then export the final version to `report/report.pdf`.

## Team and contributions

_Add group number, member names, student IDs, GitHub usernames, and an evidence-based contribution summary._

## 1. Problem statement

Predict whether the next calendar day's daily maximum AQI is greater than 150 using only information available through the current day.

## 2. Dataset and coverage audit

The project uses Version 2 of the Bangladesh Air Quality Index dataset. The main file contains 1,048,551 rows, 13 source columns, and 30 cities, while the accompanying metadata lists 103 cities. Seventy-three metadata cities are absent from the AQI file. The timestamp range is 1 January 2000–23 November 2025, but only Dhaka has the long history; most non-Dhaka cities begin in August 2022.

The main file is 24 data rows below Excel's worksheet limit and its final city block is incomplete. These results provide strong evidence that the published CSV is an Excel-truncated export. The project proceeds with faculty permission and treats this limitation as central to interpretation and generalizability.

No exact duplicate rows, duplicate city–timestamp pairs, or timestamp gaps were found in the selected city series. CO2 is approximately 74% missing. One negative NO2 observation and eleven negative O3 observations were identified.

The main study uses Dhaka, Dinājpur, Bherāmāra, Bhola, and Cox’s Bāzār over their common period of 5 August 2022–23 November 2025 (1,207 usable dates per city). These cities were chosen for complete overlapping coverage and geographic diversity, not target rates or expected model performance.

## 3. Research questions

1. How well does a model trained on Dhaka transfer to smaller Bangladeshi cities with comparable temporal coverage?
2. Can machine-learning models outperform a persistence baseline for next-day unhealthy-air prediction?
3. Which strictly lagged pollutant measurements and historical windows are most useful for prediction?

## 4. Target and leakage prevention

Daily AQI is operationally defined as the maximum supplied hourly AQI for a city-date with at least 18 valid AQI hours. The main positive class is the next calendar day's daily maximum AQI greater than 150. AQI 101–150 remains negative in the main task; a separately named AQI-greater-than-100 sensitivity target may be examined.

Notebook 03 will construct the target only after the complete city-calendar index exists. Every feature must originate on day `t` or earlier, and the label must be verified as exactly day `t+1`.

## 5. Preprocessing

Notebook 02 will keep only the five selected cities and common period, remove CO2, convert negative NO2/O3 readings to missing, preserve missingness and hourly-coverage indicators, aggregate hourly measurements to daily rows, and create a complete city-by-date calendar. Missing AQI will not be imputed for target construction.

## 6. Exploratory and statistical analysis

Seasonality is technically observable in the common period but remains optional descriptive EDA, not a primary research question. Same-time pollutant/AQI relationships will not be presented as evidence of next-day predictive importance.

## 7. Features and chronological validation

_Document lags, shifted rolling windows, feature selection, split dates, and class balance after Notebooks 03 and 04 are executed._

## 8. Persistence baseline, models, and tuning

_Show persistence first. Document model choices, modest search spaces, validation results, and the frozen decision threshold._

## 9. Test results and transfer study

_Lead with PR-AUC and recall; also report precision, F1, confusion matrices, and per-city results on identical test rows._

## 10. Error analysis

_Analyze false negatives, severity, city differences, data coverage, and temporal patterns._

## 11. Conclusion and limitations

_State plainly whether ML beat persistence. Discuss truncation, possible generation or mechanical-construction concerns, geographic incompleteness, missingness, threshold sensitivity, and limits on generalization._

## References

- Paul, T. (2026). *Bangladesh Air Quality Index (AQI) Dataset (2000–2025): Historical Hourly Air Pollution Data Across 103 Cities* (Version 2). Mendeley Data. <https://doi.org/10.17632/9j447cynb9.2>
