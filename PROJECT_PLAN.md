# Project Plan

This is the authoritative execution plan for CSE437 Group 18. Both team members and any AI agent must read this file before changing a notebook. Faculty feedback overrides earlier ideas.

## 1. Goal and success condition

Build a reproducible binary-classification study that predicts whether a selected city's **next calendar day** has a daily maximum supplied AQI greater than 150, using only historical information available through the current day.

A successful result is not simply a high score. The final model must be compared honestly with persistence. If no model beats persistence on PR-AUC and recall during the untouched test period, that is the correct finding.

## 2. Project status

| Stage | Status | Gate |
| --- | --- | --- |
| Notebook 01 — Audit and EDA | Complete | Passed |
| Notebook 02 — Preprocessing | Complete | Passed |
| Notebook 03 — Feature engineering | Complete | Passed |
| Notebook 04 — Modeling and tuning | Next | Requires chronological modeling and validation |
| Notebook 05 — Evaluation | Pending | Requires frozen model and test period |

## 3. Locked decisions from Notebook 01

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
| CO2 | Drop; never use as a predictor |
| Invalid pollutants | Convert negative NO2/O3 readings to missing |
| Missing AQI | Do not impute for daily AQI or target construction |
| Pollutant daily summaries | Mean and maximum of valid hourly readings; no imputation |
| Coverage indicators | Preserve observed rows, observed hours, and valid-hour counts |
| Timestamp | Use recorded clock time without shifting the day boundary; source has no offset |
| Feature timing | Strictly lagged; no information from the label day |
| Split | Chronological date split; never random |
| Baseline | Persistence before ML |
| Primary metrics | PR-AUC and recall |
| Secondary metrics | Precision, F1, confusion matrix, class prevalence |
| Cross-city study | Train on Dhaka; test transfer to the four smaller cities |
| Seasonality | Optional descriptive EDA only |
| Historical feature signals | Daily AQI plus daily mean and maximum for six pollutants (13 signals) |
| Individual feature lags | 1, 2, and 7 days before the target |
| Rolling features | 3-day and 7-day means, shifted by one day before rolling |
| Final predictor count | 65 |
| Modeling handoff | 6,000 rows, 1,200 per city, and 71 total columns |
| Coverage-count predictors | Excluded because all nine counts are constant at 24 |

The daily maximum is an operational aggregation of the supplied hourly AQI, not a claim that the project independently recomputes an official regulatory daily AQI.

### Decisions still requiring later evidence

- Exact chronological train/validation/test cut dates in Notebook 04
- Final model families, tuning spaces, and classification threshold

No teammate or agent may decide these silently. Record the evidence and decision in the relevant notebook.

## 4. Verified dataset audit

Notebook 01 established:

- 1,048,551 rows and 13 source columns in `AQI Bangladesh.csv`;
- 30 cities in the AQI file versus 103 in `cities.csv`;
- 73 metadata cities absent from the main file;
- overall timestamps from 1 January 2000 to 23 November 2025;
- long coverage only for Dhaka, with most non-Dhaka cities beginning in August 2022;
- no exact duplicates, duplicate city–timestamp pairs, or timestamp gaps in selected series;
- CO2 approximately 74% missing;
- one negative NO2 and eleven negative O3 readings;
- a row count only 24 data rows below Excel's limit;
- one contiguous block per city and an incomplete final city block.

This is strong evidence that the AQI CSV is an Excel-truncated export. The data must not be described as complete coverage of 103 cities. The faculty has allowed the project to proceed with the limitation documented.

## 5. Research questions

- **RQ1 — Transfer:** How well does a model trained on Dhaka transfer to smaller Bangladeshi cities with comparable temporal coverage?
- **RQ2 — Baseline comparison:** Can machine-learning models outperform persistence for next-day unhealthy-air prediction?
- **RQ3 — Predictive history:** Which strictly lagged pollutants and historical windows contribute most to next-day unhealthy-air prediction?

City ranking, time-of-day, and seasonal plots are descriptive EDA, not primary research questions. Same-time correlations must not be interpreted as next-day feature importance.

## 6. Notebook contracts

### Notebook 01 — Data audit and EDA

**Status:** complete; audit gate passed.

**Input:** untouched `AQI Bangladesh.csv` and `cities.csv`.

**Completed work:** schema and integrity audit, coverage arithmetic, metadata comparison, truncation investigation, missingness and invalid-value audit, temporal gaps, seasonality feasibility, city selection, common-period definition, target prevalence comparison, and audit-gate decisions.

**Acceptance:** the executed notebook contains no error outputs and records the selected scope and limitations.

### Notebook 02 — Preprocessing

**Status:** complete; preprocessing gate passed.

**Input:** raw files plus the locked Notebook 01 decisions.

**Required work:**

1. Load the raw AQI file without modifying it.
2. Standardize the audited columns and parse timestamps without shifting recorded clock times.
3. Keep only the five selected cities and timestamps from the common period.
4. Sort by city/time and assert unique city–timestamp pairs.
5. Drop CO2 and exclude identifiers from analytical predictors while retaining city/date identifiers.
6. Convert negative NO2 and O3 values to missing and report the affected rows.
7. Aggregate hourly pollutants and AQI to one row per city-date with documented statistics.
8. Preserve observation counts and valid-value counts for every pollutant.
9. Define daily AQI as maximum supplied hourly AQI only when at least 18 valid AQI hours exist.
10. Reindex each city to the full common calendar so missing days remain visible.
11. Compare hourly input and daily output row counts, missingness, and coverage.
12. Assert exactly one row per city-date, sorted dates, five cities, and the expected common calendar.

**Output:** `processed/daily_air_quality.csv` plus a compact preprocessing summary.

**Verified result:** 144,840 selected hourly rows were aggregated into 6,035 unique city-date rows with 24 columns. Every city has 1,207 dates and 24 hourly observations per date. Calendar completion inserted zero rows, and the selected scope contains no missing daily values. Pollutants use daily mean and maximum summaries with valid-hour counts; no imputation, target, lag, split, or model was created.

**Acceptance:** exactly one unique row per city-date; no target or model features are created; every transformation is documented and reproducible.

### Notebook 03 — Feature engineering

**Status:** complete; feature-engineering gate passed.

**Input:** frozen `daily_air_quality.csv` from Notebook 02.

**Completed work:**

1. Re-verified the 6,035-row, 24-column daily handoff, its five-city calendar, and its SHA-256.
2. Organized every modeling row around a target date and required the feature date to be exactly one calendar day earlier.
3. Created the main next-day AQI > 150 target and the separately named AQI > 100 sensitivity target.
4. Used 13 historical signals: daily AQI plus daily mean and maximum for PM10, PM2.5, CO, NO2, SO2, and O3.
5. Created target-minus-1, target-minus-2, and target-minus-7 lags for every signal.
6. Shifted each signal by one day before calculating 3-day and 7-day rolling means.
7. Excluded constant coverage counts, identifiers, outcome columns, CO2, and calendar-season fields from the predictor list.
8. Created and verified a feature manifest that records every predictor's source and historical period.
9. Removed only the first seven target dates per city because their complete history does not exist.
10. Ran exact lag-origin, rolling-origin, date-alignment, completeness, and leakage assertions.

**Verified result:** 6,000 modeling rows, 1,200 per city, 65 complete predictors, and 71 total columns. The main target contains 2,399 positive rows (39.98%); the sensitivity target contains 3,703 positive rows (61.72%). No split, scaler, target-driven feature selection, threshold, prediction, or model was created.

**Outputs:** `processed/modeling_dataset.csv`, `processed/notebook_03_feature_manifest.csv`, and `processed/notebook_03_feature_summary.json`.

**Acceptance:** passed. Every predictor has an auditable origin at least one day before its target, all output features are complete, and the saved-file readback checks passed.

### Notebook 04 — Modeling and tuning

**Status:** next; requires the frozen Notebook 03 modeling dataset and feature manifest.

**Input:** frozen modeling dataset.

**Required work:**

1. Freeze chronological train, validation, and test periods.
2. Keep test labels untouched during selection and tuning.
3. Build persistence first: tomorrow's class equals today's class.
4. Add logistic regression and a small number of justified nonlinear models.
5. Tune only with training/validation data using time-aware procedures.
6. Address imbalance only inside training/validation.
7. Run within-city and Dhaka-to-smaller-city transfer experiments.
8. Freeze one final model and decision threshold without test optimization.

**Outputs:** validation comparison, fitted artifacts in shared storage, frozen split dates, and feature list.

### Notebook 05 — Evaluation and error analysis

**Input:** frozen test data, persistence outputs, and final model.

**Required work:**

1. Evaluate once on the untouched test period.
2. Report prevalence, PR-AUC, recall, precision, F1, and confusion matrices.
3. Compare persistence and ML on identical test rows.
4. Report overall and per-city results.
5. Analyze false negatives first, then severity, coverage, time, and transfer failures.
6. State plainly whether ML beat persistence.

## 7. Leakage rules

For a prediction issued after day `t`:

- allowed: measurements and aggregates from day `t` or earlier;
- prohibited: any observation from day `t+1` in predictors;
- prohibited: centered rolling windows;
- prohibited: imputation fitted using validation/test future values;
- prohibited: random train/test splitting;
- prohibited: tuning a threshold on test labels;
- prohibited: same-timestamp pollutants used to reconstruct the same timestamp's AQI label.

Minimum assertions must verify unique city-dates, sorted dates, exact next-day alignment, disjoint chronological splits, and absence of future-derived feature columns.

## 8. Recommended modeling scope

Keep the study small enough to explain:

1. Persistence baseline
2. Logistic regression
3. Random forest or a comparable bagged-tree model
4. One gradient-boosting model available in the declared dependencies

Do not add deep learning unless the faculty explicitly asks for it.

## 9. Two-person division

| Phase | Member A | Member B | Joint checkpoint |
| --- | --- | --- | --- |
| Audit | Own Notebook 01 | Review code and evidence | Approve audit gate |
| Daily data | Own Notebook 02 | Independently check transformations | Freeze `daily_air_quality.csv` |
| Features | Review daily handoff | Own Notebook 03 | Run leakage review |
| Models | Review baseline and splits | Own Notebook 04 | Freeze model and threshold |
| Final | Own plots/error tables | Draft methods/results | Complete Notebook 05 and report |

Replace Member A/B with names before submission. Ownership does not remove the review requirement.

## 10. Git and Colab workflow

- Branch from current `main` and use one owner per notebook at a time.
- Use `MyDrive/CSE437_air_quality_group_18` for raw data, processed handoffs, figures, and large model artifacts.
- Save notebook outputs before committing.
- Do not commit raw data, secrets, personal Drive paths, or large binaries.
- Open a pull request and obtain teammate review before merging.
- After merge, both members refresh from the new `main` before starting dependent work.

Suggested branches: `notebook-02-preprocessing-<name>`, `notebook-03-features-<name>`, `notebook-04-models-<name>`, `notebook-05-evaluation-<name>`.

## 11. AI-agent handoff prompt

> Read `AGENTS.md` and `PROJECT_PLAN.md` completely. Work only on Notebook 04 on a new branch. Load the frozen `modeling_dataset.csv` and feature manifest, freeze chronological train/validation/test dates, keep test labels untouched, build persistence before machine learning, fit every learned transformation on training data only, tune only with training/validation data, run the Dhaka-to-smaller-city transfer experiment, and freeze one final model and threshold. Do not perform final test evaluation or Notebook 05 error analysis. Keep every code section preceded by a markdown explanation and do not invent results.

Never ask two agents to edit the same notebook at the same time. Review every generated cell and verify outputs yourself.

## 12. Definition of done

- All five notebooks run in order from fresh Colab runtimes using shared artifacts.
- All charts and numbers come from executed code.
- Coverage and truncation are documented explicitly.
- Target definition and exact date alignment are visible.
- No leakage or random temporal split exists.
- Persistence and ML use identical test rows.
- PR-AUC and recall lead evaluation.
- Transfer results are reported for the four smaller cities.
- Limitations discuss truncation, possible generation concerns, missingness, and generalizability.
- README, report, requirements, notebook outputs, and GitHub contribution history are current.
