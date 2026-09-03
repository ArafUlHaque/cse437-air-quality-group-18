# Project Plan

This is the authoritative execution record for CSE437 Group 18. Faculty conditions and the locked decisions below override earlier ideas.

## 1. Goal and success condition

Build a reproducible binary-classification study that predicts whether a selected city's **next calendar day** has a daily maximum supplied AQI greater than 150, using only historical information available through the current day.

Success is defined against persistence on identical untouched test rows. The completed evaluation found that the frozen machine-learning model exceeded persistence on both primary metrics: PR-AUC (average precision) and recall.

## 2. Project status

| Stage | Status | Verified gate |
| --- | --- | --- |
| Notebook 01 — Audit and EDA | Complete | Passed |
| Notebook 02 — Preprocessing | Complete | Passed |
| Notebook 03 — Feature engineering | Complete | Passed |
| Notebook 04 — Modeling and tuning | Complete | Passed |
| Notebook 05 — Evaluation and error analysis | Complete | Passed |
| Written report | Pending | To be completed separately |

The analytical pipeline is frozen. Do not retune, change the threshold, or repeat test-guided selection while preparing the report.

## 3. Locked design and completed decisions

| Item | Decision |
| --- | --- |
| Main task | Next-day binary classification |
| Positive class | Next day's daily maximum AQI > 150 (integer AQI 151+) |
| Optional sensitivity target | Next day's daily maximum AQI > 100, named USG-or-worse |
| Selected cities | Dhaka, Dinājpur, Bherāmāra, Bhola, Cox’s Bāzār |
| Common period | 5 August 2022–23 November 2025 |
| Common usable dates | 1,207 per city |
| Time unit | One row per city per calendar day |
| Daily AQI | Maximum supplied hourly AQI when at least 18 hourly AQI values are valid |
| CO2 | Dropped; never used as a predictor |
| Invalid pollutants | Negative NO2/O3 readings converted to missing |
| Missing AQI | Not imputed for daily AQI or target construction |
| Pollutant summaries | Daily mean and maximum of valid hourly readings; no imputation |
| Coverage indicators | Retained for quality checks but excluded from predictors because all were constant at 24 |
| Timestamp | Recorded clock time used without shifting the day boundary; the source has no offset |
| Feature timing | Strictly historical; no label-day information |
| Historical signals | Daily AQI plus daily mean and maximum for six pollutants (13 signals) |
| Feature windows | 1-, 2-, and 7-day lags plus shifted 3-day and 7-day rolling means |
| Predictor count | 65 |
| Modeling handoff | 6,000 rows, 1,200 per city, and 71 total columns |
| Split | Common chronological dates; never random |
| Train dates | 12 August 2022–28 November 2024 |
| Validation dates | 29 November 2024–27 May 2025 |
| Test dates | 28 May 2025–23 November 2025 |
| Split sizes | 4,200 train, 900 validation, 900 test rows; 840/180/180 per city |
| Source model | Dhaka-only development |
| Transfer study | Frozen Dhaka model evaluated on the four smaller cities |
| Baseline | Persistence built before machine learning |
| Candidate models | Logistic Regression, Random Forest, Histogram Gradient Boosting |
| Tuning | Four-fold expanding-window `TimeSeriesSplit` on Dhaka training data |
| Tuning score | Mean average precision |
| Selected model | Logistic Regression with `C=1.0` and `class_weight="balanced"` |
| Model-selection evidence | Dhaka validation average precision, recall, then simplicity |
| Frozen threshold | 0.008870 |
| Threshold rule | Maximize Dhaka validation F2; break ties by recall, precision, proximity to 0.5, then threshold |
| Final refit | 1,020 Dhaka train-plus-validation rows |
| Primary metrics | PR-AUC (average precision) and recall |
| Secondary metrics | Precision, F1, accuracy, confusion matrix, and prevalence |
| Seasonality | Descriptive analysis only |

The daily maximum is an operational aggregation of the supplied hourly AQI. It is not a claim that the project independently recomputes an official regulatory daily AQI.

## 4. Verified dataset audit

Notebook 01 established:

- 1,048,551 rows and 13 source columns in `AQI Bangladesh.csv`;
- 30 cities in the AQI file versus 103 in `cities.csv`;
- 73 metadata cities absent from the main file;
- timestamps from 1 January 2000 through 23 November 2025;
- long coverage only for Dhaka, with most non-Dhaka cities beginning in August 2022;
- no exact duplicates, duplicate city–timestamp pairs, or timestamp gaps in the selected series;
- approximately 74% missing CO2;
- one negative NO2 and eleven negative O3 readings;
- a row count only 24 data rows below Excel's worksheet limit; and
- one contiguous block per city with an incomplete final city block.

This is strong evidence that the AQI CSV is an Excel-truncated export. The data must not be described as complete coverage of 103 cities. The faculty allowed the project to proceed with this limitation documented.

## 5. Research questions and completed evidence

### RQ1 — Transfer

How well does a model trained on Dhaka transfer to smaller Bangladeshi cities with comparable temporal coverage?

The four-city transfer pool achieved average precision 0.9376 and recall 0.9932. Cox’s Bāzār was the weakest transfer city, with average precision 0.6280 and recall 0.9091. These results show strong pooled warning recall but uneven probability ranking across cities.

### RQ2 — Baseline comparison

Can machine-learning models outperform persistence for next-day unhealthy-air prediction?

Yes. On the same 900 held-out rows, Logistic Regression achieved average precision 0.9359 and recall 0.9947; persistence achieved 0.7003 and 0.8032. The model beat persistence on both primary metrics in all five cities.

### RQ3 — Predictive history

Which strictly lagged pollutants and historical windows contribute most to next-day unhealthy-air prediction?

Validation-only permutation importance ranked `pm25_mean_lag1` first, followed by `pm25_max_roll3_mean` and `pm10_mean_lag1`. This supports recent particulate history as useful predictive information but does not establish causality.

## 6. Notebook contracts and verified results

### Notebook 01 — Data audit and EDA

**Status:** complete; audit gate passed.

**Input:** untouched `AQI Bangladesh.csv` and `cities.csv`.

**Completed work:** schema and integrity audit, coverage arithmetic, metadata comparison, truncation investigation, missingness and invalid-value audit, temporal-gap checks, seasonality feasibility, city selection, common-period definition, target-prevalence comparison, and audit-gate decisions.

**Acceptance:** the executed notebook contains no error outputs and records the selected scope and limitations.

### Notebook 02 — Preprocessing

**Status:** complete; preprocessing gate passed.

**Input:** raw files plus the locked Notebook 01 decisions.

**Completed work:** selected-scope filtering, timestamp parsing, invalid-value correction, CO2 exclusion, daily aggregation, coverage preservation, complete-calendar reindexing, and saved-file validation.

**Verified result:** 144,840 selected hourly rows were aggregated into 6,035 unique city-date rows with 24 columns. Every city has 1,207 dates and 24 hourly observations per date. Calendar completion inserted zero rows, and the selected scope has no missing daily values. No target, lag, split, or model was created.

**Outputs:**

- `processed/daily_air_quality.csv`
- `processed/notebook_02_preprocessing_summary.json`

### Notebook 03 — Feature engineering

**Status:** complete; feature-engineering gate passed.

**Input:** frozen `daily_air_quality.csv` from Notebook 02.

**Completed work:** exact next-calendar-day targets, 65 historical features, manifest construction, structural-history filtering, exact lag/rolling-origin checks, leakage assertions, and saved-file readback checks.

**Verified result:** 6,000 modeling rows, 1,200 per city, 65 complete predictors, and 71 total columns. The main target contains 2,399 positives (39.98%); the sensitivity target contains 3,703 positives (61.72%). Seven initial target dates per city were removed because complete seven-day history did not exist.

**Outputs:**

- `processed/modeling_dataset.csv`
- `processed/notebook_03_feature_manifest.csv`
- `processed/notebook_03_feature_summary.json`

### Notebook 04 — Modeling and tuning

**Status:** complete; modeling and tuning gate passed.

**Input:** frozen Notebook 03 modeling dataset, feature manifest, and feature summary.

**Completed work:**

1. Verified the 6,000-row, 65-feature handoff and input checksums.
2. Froze identical chronological split dates for all five cities.
3. Isolated Dhaka training and validation rows while withholding all test labels.
4. Evaluated persistence before machine learning.
5. Tuned three candidate families with four expanding time-ordered folds.
6. Selected Logistic Regression using Dhaka validation evidence.
7. Selected a recall-oriented F2 threshold using validation probabilities only.
8. Calculated validation-only permutation importance.
9. Refit the selected pipeline on 1,020 Dhaka development rows.
10. Saved and reloaded every modeling handoff without performing test evaluation.

**Validation evidence:** Logistic Regression and Random Forest both reached validation average precision 0.9853, but Logistic Regression had higher recall at the default threshold (0.9185 versus 0.8519) and was simpler. At the frozen 0.008870 threshold, Logistic Regression achieved validation recall 1.0000, precision 0.7803, and F2 0.9467.

**Outputs:**

- `processed/notebook_04_split_assignments.csv`
- `processed/notebook_04_cv_results.csv`
- `processed/notebook_04_validation_results.csv`
- `processed/notebook_04_validation_feature_importance.csv`
- `processed/notebook_04_modeling_summary.json`
- `models/notebook_04/final_model.joblib`
- `models/notebook_04/final_model_protocol.json`
- `figures/notebook_04/validation_pr_curves.png`

### Notebook 05 — Final evaluation and error analysis

**Status:** complete; final evaluation gate passed.

**Input:** frozen test rows, model, feature order, split assignments, protocol, and daily coverage handoff.

**Completed work:**

1. Verified the frozen Notebook 04 handoff before reading test outcomes.
2. Applied the model once without refitting, retuning, or changing the threshold.
3. Compared Logistic Regression and persistence on identical rows.
4. Reported overall, per-city, within-city, and transfer metrics.
5. Analyzed false negatives first, then severity, measurement coverage, month, and transfer gaps.
6. Saved and verified the evaluation tables, summary, and figures.

**Verified result:**

| Method | Average precision | Recall | Precision | F1 | Accuracy | TN | FP | FN | TP |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Logistic Regression | 0.9359 | 0.9947 | 0.3495 | 0.5173 | 0.6122 | 364 | 348 | 1 | 187 |
| Persistence | 0.7003 | 0.8032 | 0.8207 | 0.8118 | 0.9222 | 679 | 33 | 37 | 151 |

There were 188 positive days among 900 test rows (20.89%). The low frozen threshold achieved the recall objective at the cost of many false positives. Coverage counts were constant at 24 and could not distinguish correct from incorrect predictions.

**Outputs:**

- `processed/notebook_05_test_predictions.csv`
- `processed/notebook_05_overall_results.csv`
- `processed/notebook_05_per_city_results.csv`
- `processed/notebook_05_false_negatives.csv`
- `processed/notebook_05_monthly_results.csv`
- `processed/notebook_05_transfer_results.csv`
- `processed/notebook_05_coverage_diagnostic.csv`
- `processed/notebook_05_evaluation_summary.json`
- `figures/notebook_05/test_pr_curves.png`
- `figures/notebook_05/test_confusion_matrices.png`
- `figures/notebook_05/test_per_city_metrics.png`
- `figures/notebook_05/test_monthly_recall.png`

## 7. Leakage and evaluation rules

For a prediction issued after day `t`:

- allowed: measurements and aggregates from day `t` or earlier;
- prohibited: any target-day (`t+1`) observation in predictors;
- prohibited: centered rolling windows;
- prohibited: imputation or scaling fitted with validation/test future values;
- prohibited: random train/test splitting;
- prohibited: threshold tuning with test labels; and
- prohibited: same-timestamp pollutants used to reconstruct the same timestamp's AQI label.

The final model, threshold, features, split dates, and test results are now frozen. Report writing must use the saved evidence without conducting new test-guided optimization.

## 8. Team workflow

The GitHub history records contributions from [ArafUlHaque](https://github.com/ArafUlHaque) and [WhyNotInan](https://github.com/WhyNotInan). Use the commit and pull-request history as the authoritative contribution record when completing the report table. Report drafting and the final submission review remain to be assigned between the two members.

Notebook ownership does not remove the teammate-review requirement.

## 9. Git and Colab workflow

- Branch from current `main` and use one owner per task at a time.
- Use `MyDrive/CSE437_air_quality_group_18` for raw data, processed handoffs, figures, and large model artifacts.
- Save notebook outputs before committing.
- Do not commit raw data, generated CSV handoffs, secrets, personal Drive paths, or large model binaries.
- Use focused commits and obtain teammate review before merging submission-critical changes.
- Preserve the executed final notebooks and frozen evidence while drafting the report.

## 10. Report handoff

The report is intentionally deferred. When work begins, it should:

1. use the exact dataset limitation and study design recorded here;
2. describe the chronological split, Dhaka-only development, model selection, and validation-only threshold choice;
3. lead with average precision and recall, while explaining the precision/accuracy trade-off;
4. report pooled, within-city, and transfer results;
5. discuss the single model false negative and large false-positive count;
6. answer all three research questions without causal overclaiming; and
7. retain the limitations: likely Excel truncation, possible data-generation concerns, six-month test window, Dhaka-only training, four transfer cities, and hard-score persistence PR behavior.

Do not change the frozen analytical decisions to improve the narrative.

## 11. Definition of analytical completion

- All five notebooks run in order and contain saved outputs.
- Every notebook gate passed without recorded error outputs.
- Coverage and truncation are documented explicitly.
- Target definition and exact date alignment are visible.
- No leakage or random temporal split exists.
- Persistence and machine learning use identical test rows.
- PR-AUC and recall lead the evaluation.
- Transfer results are reported for all four smaller cities.
- README, data, model, figure, project-plan, and agent documentation match the executed notebooks.

The analytical repository is complete. The written report, student IDs, and any final report-figure copies are the remaining submission items.
