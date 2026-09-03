# AGENTS.md

These instructions apply to every AI agent or coding assistant working in this repository.

## Read first

Read `PROJECT_PLAN.md` completely before editing. Treat faculty conditions, frozen analytical decisions, and executed notebook evidence there as authoritative.

## Current project state

- Notebooks 01, 02, 03, 04, and 05 are complete and their gates passed.
- The analytical pipeline is frozen; the written report is the next remaining stage and will be handled separately.
- Locked cities: Dhaka, Dinājpur, Bherāmāra, Bhola, and Cox’s Bāzār.
- Locked common period: 5 August 2022–23 November 2025, with 1,207 usable dates per city.
- Frozen daily output: 6,035 unique city-date rows and 24 columns, with no missing values in the selected scope.
- Main positive class: next calendar day's daily maximum AQI > 150.
- Frozen modeling output: 6,000 rows, 1,200 per city, 71 total columns, and 65 complete historical predictors.
- Locked feature history: 1-, 2-, and 7-day lags plus shifted 3-day and 7-day rolling means for 13 signals.
- Frozen chronological split: 12 August 2022–28 November 2024 train; 29 November 2024–27 May 2025 validation; 28 May–23 November 2025 test.
- Frozen model: Logistic Regression with `C=1.0`, balanced class weights, 65 predictors, and threshold `0.008870`.
- Final model fitting data: 1,020 Dhaka train-plus-validation rows.
- Final untouched test result: model average precision 0.9359 and recall 0.9947; persistence average precision 0.7003 and recall 0.8032.
- Final verdict: the model beat persistence on both primary metrics overall and in all five cities.

## Scope and sequencing

- Work only on the notebook or file assigned by the user.
- Preserve the dependency chain: 01 → 02 → 03 → 04 → 05 → report.
- Do not rewrite a teammate's work or alter unrelated files.
- Do not silently change a locked decision.
- Do not rerun model selection against test outcomes, retune the final threshold, change the frozen feature list, or replace the final model during report writing.
- If a correction to a frozen notebook becomes necessary, state why, identify every downstream artifact affected, and ask before changing the analytical protocol.

## Data and evidence

- Never modify files in `data/raw/` or the shared Drive `raw/` folder.
- Never invent column names, results, dates, city coverage, metrics, or conclusions.
- Write factual findings only when supported by displayed notebook output or saved handoffs.
- Do not commit secrets, raw data, generated CSV handoffs, large binaries, or Drive paths containing personal names.
- Keep code simple, readable, and suitable for Google Colab.
- Preserve Unicode city names exactly in stored outputs.
- Keep the likely Excel-truncation limitation visible in all public summaries.

## Frozen preprocessing rules

- Keep only the five locked cities and common period.
- Use recorded source clock times without shifting the calendar-day boundary; the source has no timezone offset.
- Drop CO2 and exclude identifier columns from predictors while retaining city/date identifiers for grouping.
- Convert the one negative NO2 value and eleven negative O3 values to missing before aggregation.
- Do not impute missing AQI when constructing daily AQI.
- Define daily AQI as the maximum supplied hourly AQI only when at least 18 hourly AQI values are valid.
- Aggregate pollutants using daily mean and maximum and preserve hourly coverage counts.
- Reindex every city to a complete calendar before constructing any next-day target.

## Frozen feature rules

- Use only the 65 columns listed as features in the Notebook 03 manifest or summary.
- Treat `city`, `feature_date`, and `target_date` as identifiers, not predictors.
- Treat `target_daily_aqi`, `next_day_unhealthy`, and `next_day_usg_or_worse` as outcomes, never predictors.
- Use `next_day_unhealthy` for the main task; the AQI > 100 target is a separately named sensitivity target.
- Do not reconstruct unshifted or target-day pollutant features.
- Preserve the exact one-calendar-day relationship between feature date and target date.

## Frozen modeling and evaluation rules

- All features come from day `t` or earlier and the label belongs to exactly day `t+1`.
- The split is chronological by shared target dates and must never be randomized.
- Learned transformations are fitted only within allowed training data.
- Persistence is the required baseline and must use the same evaluation rows.
- Model tuning used only Dhaka training folds; model and threshold selection used only Dhaka validation evidence.
- The final Logistic Regression pipeline is fitted only on Dhaka train-plus-validation rows.
- The test period was evaluated once in Notebook 05; its results must not become development feedback.
- Lead interpretation with average precision and recall. Accuracy, precision, and F1 are important trade-off measures but are not the primary selection rule.
- Explain that threshold `0.008870` produced one false negative and 348 false positives on the pooled test set.
- Report transfer results separately from Dhaka within-city performance.
- Treat validation permutation importance as predictive association, not causal importance.

## Artifact contracts

Notebook 04 generated these shared-Drive handoffs:

- `processed/notebook_04_split_assignments.csv`
- `processed/notebook_04_cv_results.csv`
- `processed/notebook_04_validation_results.csv`
- `processed/notebook_04_validation_feature_importance.csv`
- `processed/notebook_04_modeling_summary.json`
- `models/notebook_04/final_model.joblib`
- `models/notebook_04/final_model_protocol.json`
- `figures/notebook_04/validation_pr_curves.png`

Notebook 05 generated these shared-Drive handoffs:

- `processed/notebook_05_test_predictions.csv`
- `processed/notebook_05_overall_results.csv`
- `processed/notebook_05_per_city_results.csv`
- `processed/notebook_05_false_negatives.csv`
- `processed/notebook_05_monthly_results.csv`
- `processed/notebook_05_transfer_results.csv`
- `processed/notebook_05_coverage_diagnostic.csv`
- `processed/notebook_05_evaluation_summary.json`
- four final evaluation figures listed in `figures/README.md`

Regenerate artifacts through the notebooks; never edit generated evidence manually.

## Report guardrails

- Use the exact displayed and saved results from Notebook 05.
- State that machine learning beat persistence on the two primary metrics, while persistence retained much higher precision, F1, and accuracy.
- Explain the operational reason for the recall-oriented threshold and its false-positive cost.
- Include within-city and transfer results, identifying Cox’s Bāzār as the weakest transfer city.
- Preserve limitations: likely Excel truncation, possible data-generation concerns, six-month test window, Dhaka-only development, four transfer cities, and hard-score persistence PR behavior.
- Do not claim causal pollutant effects or nationwide generalizability.

## Quality checks

Before finishing any task:

1. Run changed code top-to-bottom when data/runtime access permits.
2. Add assertions for important invariants.
3. Keep notebook outputs, saved handoffs, and Markdown explanations consistent.
4. Check links and filenames against the actual repository tree.
5. State anything that could not be verified.
6. Summarize changed files and the next dependency.

