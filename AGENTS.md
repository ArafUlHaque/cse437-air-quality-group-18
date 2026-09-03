# AGENTS.md

These instructions apply to every AI agent or coding assistant working in this repository.

## Read first

Read `PROJECT_PLAN.md` completely before editing. Treat faculty conditions and the locked decisions there as authoritative.

## Current project state

- Notebooks 01, 02, and 03 have passed their audit, preprocessing, and feature-engineering gates.
- Notebook 04 modeling and tuning is the next allowed stage.
- Locked cities: Dhaka, Dinājpur, Bherāmāra, Bhola, and Cox’s Bāzār.
- Locked common period: 5 August 2022–23 November 2025 (1,207 usable dates per city).
- Daily AQI is the maximum supplied hourly AQI for each city-date with at least 18 valid AQI hours.
- Frozen daily output: 6,035 unique city-date rows and 24 columns, with no missing values in the selected scope.
- Main positive class: next calendar day's daily maximum AQI > 150.
- Frozen modeling output: 6,000 rows, 1,200 per city, 71 total columns, and 65 complete historical predictors.
- Locked feature history: 1-, 2-, and 7-day lags plus shifted 3-day and 7-day rolling means for 13 signals.
- Notebook 03 output contains 2,399 main-target positives (39.98%).

## Scope and sequencing

- Work only on the notebook or file assigned by the user.
- Notebook order is a dependency chain: 01 → 02 → 03 → 04 → 05.
- Notebook 03 outputs are frozen; do not redefine its targets, feature windows, or feature list silently.
- Notebook 04 may create chronological splits, persistence predictions, fitted transformations, tuned validation models, and the transfer experiment, but it must not perform the final untouched-test evaluation assigned to Notebook 05.
- Do not rewrite a teammate's work or alter unrelated files.
- Ask before changing a locked decision.

## Data and evidence

- Never modify files in `data/raw/` or the shared Drive `raw/` folder.
- Never invent column names, results, dates, city coverage, metrics, or conclusions.
- Only write factual findings supported by displayed notebook output.
- Do not commit secrets, raw data, large binaries, or Drive paths containing personal names.
- Keep code simple, readable, and suitable for Google Colab.
- Preserve Unicode city names exactly in stored outputs.

## Notebook 02 preprocessing rules

- Keep only the five locked cities and common period.
- Use recorded source clock times without shifting the calendar-day boundary; the source has no timezone offset.
- Drop CO2 and exclude identifier columns from predictors while retaining city/date identifiers for grouping.
- Convert the one negative NO2 value and eleven negative O3 values to missing before aggregation.
- Do not impute missing AQI when constructing daily AQI.
- Aggregate pollutants with explicitly documented statistics and preserve hourly coverage counts.
- Define daily AQI as the maximum supplied hourly AQI only when at least 18 hourly AQI values are valid.
- Reindex every city to a complete calendar before any next-day target is created.
- Save exactly one unique, sorted row per city-date to `processed/daily_air_quality.csv`.
- Do not create the next-day target until Notebook 03.


## Notebook 03 feature-engineering rules

- Read `processed/modeling_dataset.csv` together with `processed/notebook_03_feature_manifest.csv` and `processed/notebook_03_feature_summary.json`.
- Use only the 65 columns listed as features in the manifest or summary.
- Treat `city`, `feature_date`, and `target_date` as identifiers, not automatic predictors.
- Treat `target_daily_aqi`, `next_day_unhealthy`, and `next_day_usg_or_worse` as outcomes, never predictors.
- The main task uses `next_day_unhealthy`; the AQI > 100 target is a separately named sensitivity analysis.
- Do not reconstruct unshifted or target-day pollutant features.
- Preserve the exact one-day relationship between feature date and target date.

## Non-negotiable modeling rules

- All features must come from day `t` or earlier.
- Confirm the label belongs to exactly day `t+1`; the next observed row is not automatically the next day.
- Shift before calculating rolling features.
- Split by date, never randomly.
- Fit imputers, scalers, and selectors only on training data.
- Build persistence before ML.
- Lead evaluation with PR-AUC and recall; accuracy is secondary.
- Never tune on the test period.

## Quality checks

Before finishing a task:

1. Run changed code top-to-bottom when data/runtime access permits.
2. Add assertions for important invariants.
3. Keep notebook outputs and markdown explanations consistent.
4. State anything that could not be verified.
5. Summarize changed files and the next dependency.
