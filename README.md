# CSE437: Next-Day Unhealthy Air Quality Classification

Group 18 data-science project using hourly air-quality observations from selected Bangladeshi cities.

> **Current status:** Notebooks 01, 02, and 03 are complete and have passed their audit, preprocessing, and feature-engineering gates. Notebook 04 (modeling and tuning) is the next stage; final evaluation must wait until its chronological split, validation, model, and threshold decisions are frozen.

## Problem statement

Predict whether the next calendar day's air quality will be **Unhealthy** using only information available by the end of the current day.

## Primary target

`next_day_unhealthy` is 1 when the following calendar day's daily maximum of the supplied hourly AQI is greater than 150 (integer AQI 151 or above), and 0 otherwise.

AQI 101–150 is "Unhealthy for Sensitive Groups" and is not positive in the main target. A separate `next_day_usg_or_worse` sensitivity target may be reported using AQI greater than 100.

## Dataset

- **Name:** Bangladesh Air Quality Index (AQI) Dataset (2000–2025)
- **Source:** [Mendeley Data, Version 2](https://data.mendeley.com/datasets/9j447cynb9/2)
- **DOI:** [10.17632/9j447cynb9.2](https://doi.org/10.17632/9j447cynb9.2)
- **License:** CC BY 4.0
- **Raw files:** `AQI Bangladesh.csv` and `cities.csv`
- **Main-file checksum:** `8760175fc048eea4180b828fd60d10cb799a73a5144a7e4aca19ddbaf8dbdd62`

### Verified Notebook 01 findings

- The AQI file contains **1,048,551 rows**, **13 source columns**, and **30 cities**.
- `cities.csv` lists 103 cities; 73 of them are absent from the AQI file.
- The overall timestamp range is 1 January 2000–23 November 2025, but only Dhaka has the long history. Most non-Dhaka cities begin in August 2022.
- The file is only 24 data rows below Excel's worksheet limit and its final city block is partial. This is strong evidence of an Excel-truncated export.
- There are no exact duplicate rows, duplicate city–timestamp pairs, or timestamp gaps in the selected city series.
- CO2 is approximately 74% missing. The audit also found one negative NO2 value and eleven negative O3 values.


Raw data is not committed to GitHub. See [data/README.md](data/README.md).

## Locked study scope

| Item | Decision |
| --- | --- |
| Selected cities | Dhaka, Dinājpur, Bherāmāra, Bhola, Cox’s Bāzār |
| Main common period | 5 August 2022–23 November 2025 |
| Common usable dates | 1,207 per city |
| Daily AQI | Maximum supplied hourly AQI for each city-date |
| Usable AQI day | At least 18 valid hourly AQI observations |
| Positive class | Next day's daily maximum AQI > 150 |
| CO2 | Excluded |
| Invalid readings | Negative NO2/O3 converted to missing in Notebook 02 |
| Seasonality | Optional descriptive EDA only |

The five cities were selected for complete common coverage and geographic diversity, not for their target rates or expected model performance.

### Verified Notebook 02 preprocessing

- The locked scope contains 144,840 hourly rows: 28,968 for each of the five cities.
- Every city contains 1,207 dates and 24 observations per date during the common period.
- Pollutants are summarized by the mean and maximum of valid hourly readings; no values are imputed.
- Observation counts and valid-hour counts are retained for data-quality checks.
- Reindexing produced the expected 6,035 city-date rows and inserted no missing calendar dates.
- The final `daily_air_quality.csv` contains 24 columns, no missing values in the selected scope, and no targets or model features.


### Verified Notebook 03 feature engineering

- Notebook 03 re-verified the frozen 6,035-row, 24-column daily handoff; its SHA-256 was `460009e01b010695a256be268112aacf1ad32b1757f69ab199fd3a7611d16aca`.
- The main target is the next calendar day's daily AQI > 150; the optional sensitivity target uses daily AQI > 100.
- Thirteen historical signals were used: daily AQI plus the mean and maximum of six pollutants.
- Each signal contributes target-minus-1, target-minus-2, and target-minus-7 lags plus shifted 3-day and 7-day rolling means, for 65 predictors.
- Every rolling calculation shifts by one day first, so no predictor uses the target day.
- The nine coverage-count columns were excluded as predictors because each is constant at 24 throughout the selected scope.
- Seven initial target dates per city were removed because they lack the required seven-day history: 35 rows total.
- The final `modeling_dataset.csv` contains 6,000 rows, 1,200 per city, and 71 columns: 3 identifiers, 3 outcomes, and 65 complete predictors.
- The main target has 2,399 positive rows (39.98%); the sensitivity target has 3,703 positive rows (61.72%).
- The feature manifest, feature summary, saved-file readback, exact date-alignment checks, and leakage assertions all passed.
- No split, scaler, feature selection based on target performance, prediction, threshold, or model was created.

## Research questions

1. How well does a model trained on Dhaka transfer to smaller Bangladeshi cities with comparable temporal coverage?
2. Can machine-learning models outperform a persistence baseline for next-day unhealthy-air prediction?
3. Which strictly lagged pollutant measurements and historical windows are most useful for predicting next-day unhealthy air quality?

## Non-negotiable methodology

- Use only the five selected cities and the locked common period for the main cross-city study.
- Drop CO2; it is never a predictor.
- Aggregate hourly observations to one row per city per calendar day.
- Keep calendar gaps explicit before constructing the target.
- Every predictor must be available by the end of day `t`; the label belongs to exactly day `t+1`.
- Split train/validation/test chronologically by date, never randomly.
- Establish persistence first: predict tomorrow's class from today's class.
- Compare models primarily using PR-AUC and recall. Accuracy is secondary.
- A model is not considered useful merely because it scores well; it must be compared with persistence on identical rows.

## Notebooks

| Notebook | Responsibility | Status | Open in Colab |
| --- | --- | --- | --- |
| `01_data_audit_and_eda.ipynb` | Coverage, integrity, truncation audit, EDA, city selection | Complete | [Open](https://colab.research.google.com/github/ArafUlHaque/cse437-air-quality-group-18/blob/main/notebooks/01_data_audit_and_eda.ipynb) |
| `02_preprocessing.ipynb` | City/period filtering, invalid values, CO2 removal, daily aggregation, calendar completion | Complete | [Open](https://colab.research.google.com/github/ArafUlHaque/cse437-air-quality-group-18/blob/main/notebooks/02_preprocessing.ipynb) |
| `03_feature_engineering.ipynb` | Leakage-safe lag/rolling features and next-day target | Complete | [Open](https://colab.research.google.com/github/ArafUlHaque/cse437-air-quality-group-18/blob/main/notebooks/03_feature_engineering.ipynb) |
| `04_modeling_and_tuning.ipynb` | Chronological split, persistence, models, tuning, transfer experiment | Next | [Open](https://colab.research.google.com/github/ArafUlHaque/cse437-air-quality-group-18/blob/main/notebooks/04_modeling_and_tuning.ipynb) |
| `05_evaluation_and_error_analysis.ipynb` | Untouched-test evaluation, baseline comparison, errors, limitations | Pending | [Open](https://colab.research.google.com/github/ArafUlHaque/cse437-air-quality-group-18/blob/main/notebooks/05_evaluation_and_error_analysis.ipynb) |

Run the notebooks in numerical order. Each notebook must run top-to-bottom after its required input artifacts exist.

## Google Colab and shared storage

1. Both members should add the shared folder to **My Drive** with the name `CSE437_air_quality_group_18`.
2. Keep the untouched CSV files in `MyDrive/CSE437_air_quality_group_18/raw/`.
3. Use `processed/`, `figures/`, and `models/` inside that Drive folder for persistent generated artifacts.
4. Open the tracked notebook using its Colab link. The notebook mounts Drive and reads data directly from the shared folder; cloning the repository inside Colab is not required.
5. Commit the executed notebook to a feature branch and use a pull request for teammate review.

## Collaboration workflow

- Do not edit the same notebook simultaneously.
- Use one branch per task, such as `notebook-02-preprocessing-araf`.
- Branch from the latest `main` and keep commits focused.
- Open a pull request; the other member reviews it before merge.
- Do not commit raw CSV files, secrets, Drive paths containing personal names, or large model files.
- Update the contribution table in the final report from GitHub history.

The complete workflow and two-person division are in [PROJECT_PLAN.md](PROJECT_PLAN.md). AI agents must also follow [AGENTS.md](AGENTS.md).

## Repository structure

```text
cse437-air-quality-group-18/
├── AGENTS.md
├── PROJECT_PLAN.md
├── README.md
├── requirements.txt
├── data/
│   ├── raw/
│   ├── processed/
│   └── README.md
├── notebooks/
│   ├── 01_data_audit_and_eda.ipynb
│   ├── 02_preprocessing.ipynb
│   ├── 03_feature_engineering.ipynb
│   ├── 04_modeling_and_tuning.ipynb
│   └── 05_evaluation_and_error_analysis.ipynb
├── src/
│   └── utils.py
├── models/
├── figures/
└── report/
    └── report.md
```

## Team

| Member | Student ID | GitHub username |
| --- | --- | --- |
| _Add member_ | _Add ID_ | ArafUlHaque |
| _Add teammate_ | _Add ID_ | _Add username_ |
