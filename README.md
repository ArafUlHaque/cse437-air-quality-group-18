# CSE437: Next-Day Unhealthy Air Quality Classification

Group 18 data-science project using hourly air-quality observations from Bangladeshi cities.

> **Current status:** repository and methodology plan are ready. The data-coverage audit has not yet been run. Do not begin modeling until Notebook 01 passes the audit gate described in [PROJECT_PLAN.md](PROJECT_PLAN.md).

## Problem statement

Predict whether the next calendar day's air quality will be **Unhealthy** using only information available by the end of the current day.

## Primary target

`next_day_unhealthy` is 1 when the following calendar day's daily AQI is greater than 150 (integer AQI 151 or above), and 0 otherwise.

AQI 101–150 is "Unhealthy for Sensitive Groups" and is not positive in the main target. A 101+ sensitivity analysis may be reported separately, but it must use a different target name.

## Dataset

- **Name:** Bangladesh Air Quality Index (AQI) Dataset (2000–2025)
- **Source:** [Mendeley Data, Version 2](https://data.mendeley.com/datasets/9j447cynb9/2)
- **DOI:** [10.17632/9j447cynb9.2](https://doi.org/10.17632/9j447cynb9.2)
- **License:** CC BY 4.0
- **Published description:** 1,048,551 hourly rows, 103 cities, and 13 columns

The published title and row count appear inconsistent with complete hourly coverage of 103 cities from 2000–2025. Notebook 01 must therefore verify the actual date range and coverage before any seasonal or modeling claims are made.

Raw data is not committed to GitHub. See [data/README.md](data/README.md).

## Research questions

1. How well does a model trained on Dhaka transfer to smaller Bangladeshi cities with comparable temporal coverage?
2. Can machine-learning models outperform a persistence baseline for next-day unhealthy-air prediction?
3. Which strictly lagged pollutant measurements and historical windows are most useful for predicting next-day unhealthy air quality?

Seasonality remains optional EDA only if the coverage audit finds enough complete and comparable seasonal cycles.

## Non-negotiable methodology

- Use Dhaka plus 2–4 smaller cities selected after the coverage audit.
- Drop `CO2`; it is not used as a predictor.
- Aggregate hourly observations to one row per city per calendar day.
- Every predictor must be available by the end of day `t`; the label belongs to day `t+1`.
- Verify that the label date is exactly the next calendar day; never assume the next row is the next day.
- Split train/validation/test chronologically by date, never randomly.
- Establish persistence first: predict tomorrow's class from today's class.
- Compare models primarily using PR-AUC and recall. Accuracy is secondary.
- Do not report a model as useful merely because it scores well; it must beat persistence on the agreed test period.

## Notebooks

| Notebook | Responsibility | Open in Colab |
| --- | --- | --- |
| `01_data_audit_and_eda.ipynb` | Coverage, integrity, truncation audit, EDA, and city selection | [Open](https://colab.research.google.com/github/ArafUlHaque/cse437-air-quality-group-18/blob/main/notebooks/01_data_audit_and_eda.ipynb) |
| `02_preprocessing.ipynb` | Cleaning, CO2 removal, daily aggregation, missing-day handling | [Open](https://colab.research.google.com/github/ArafUlHaque/cse437-air-quality-group-18/blob/main/notebooks/02_preprocessing.ipynb) |
| `03_feature_engineering.ipynb` | Leakage-safe lag/rolling features and next-day target | [Open](https://colab.research.google.com/github/ArafUlHaque/cse437-air-quality-group-18/blob/main/notebooks/03_feature_engineering.ipynb) |
| `04_modeling_and_tuning.ipynb` | Chronological split, persistence, models, tuning, transfer experiment | [Open](https://colab.research.google.com/github/ArafUlHaque/cse437-air-quality-group-18/blob/main/notebooks/04_modeling_and_tuning.ipynb) |
| `05_evaluation_and_error_analysis.ipynb` | Untouched-test evaluation, baseline comparison, errors, limitations | [Open](https://colab.research.google.com/github/ArafUlHaque/cse437-air-quality-group-18/blob/main/notebooks/05_evaluation_and_error_analysis.ipynb) |

Run them in numerical order. Each must run top-to-bottom on a fresh Colab runtime after its required input artifacts exist.

## Google Colab and shared storage

1. In Google Drive, create a shared folder and give both members editor access.
2. Each member adds a shortcut to that folder in **My Drive** named exactly `CSE437_air_quality_group_18`.
3. Put the untouched source file inside `CSE437_air_quality_group_18/raw/`.
4. Open a notebook using the Colab link above.
5. Its setup cell mounts Drive, clones/pulls this repository, and uses the shared folder for persistent raw data, processed outputs, and model artifacts.
6. If working on a feature branch, change `GIT_BRANCH = "main"` in the notebook setup cell to the branch name.

## Collaboration workflow

- Never work directly on `main`.
- Use one branch per task, for example `notebook-01-audit-araf`.
- Pull the latest `main` before starting.
- Keep commits small and descriptive.
- Open a pull request; the other member reviews it before merge.
- Do not edit the same notebook simultaneously.
- Update the contribution table in the final report from GitHub history.

Recommended two-person ownership is documented in [PROJECT_PLAN.md](PROJECT_PLAN.md). AI agents must also follow [AGENTS.md](AGENTS.md).

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
