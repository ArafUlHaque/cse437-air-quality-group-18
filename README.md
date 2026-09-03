# CSE437: Next-Day Unhealthy Air Quality Classification

Group 18 data-science project using hourly air-quality observations from selected Bangladeshi cities.

> **Project status:** The full five-notebook analytical pipeline is complete. Notebooks 01–05 passed their audit, preprocessing, feature-engineering, modeling, and final-evaluation gates. The written report is the remaining submission task and will be completed separately.

## Problem statement

Predict whether the next calendar day's air quality will be **Unhealthy** using only information available by the end of the current day.

The main target, `next_day_unhealthy`, is 1 when the following calendar day's maximum supplied hourly AQI is greater than 150 (integer AQI 151 or above), and 0 otherwise. AQI 101–150 is not positive in the main task. A separately named `next_day_usg_or_worse` target is retained for optional sensitivity analysis.

## Final result

The frozen Logistic Regression model beat persistence on both primary metrics in the untouched pooled test period and in every selected city.

| Method | Test rows | Positive prevalence | PR-AUC (average precision) | Recall | Precision | F1 | Accuracy | TN | FP | FN | TP |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Logistic Regression | 900 | 20.89% | **0.9359** | **0.9947** | 0.3495 | 0.5173 | 0.6122 | 364 | 348 | 1 | 187 |
| Persistence | 900 | 20.89% | 0.7003 | 0.8032 | **0.8207** | **0.8118** | **0.9222** | 679 | 33 | 37 | 151 |

The low validation-selected threshold prioritizes missed-warning prevention: it reduces false negatives from 37 to 1, while producing substantially more false positives. Accuracy is therefore not the decision metric for this imbalanced, recall-oriented task.

## Dataset

- **Name:** Bangladesh Air Quality Index (AQI) Dataset (2000–2025)
- **Source:** [Mendeley Data, Version 2](https://data.mendeley.com/datasets/9j447cynb9/2)
- **DOI:** [10.17632/9j447cynb9.2](https://doi.org/10.17632/9j447cynb9.2)
- **License:** CC BY 4.0
- **Raw files:** `AQI Bangladesh.csv` and `cities.csv`
- **Main-file SHA-256:** `8760175fc048eea4180b828fd60d10cb799a73a5144a7e4aca19ddbaf8dbdd62`

Notebook 01 found 1,048,551 rows, 13 source columns, and only 30 cities in the main AQI file, although `cities.csv` lists 103 cities. The file ends only 24 data rows below Excel's worksheet limit and its final city block is incomplete. This is strong evidence of an Excel-truncated export, so this project does not describe the file as complete coverage of all 103 published cities.

Raw data is not committed to GitHub. See [data/README.md](data/README.md) for source integrity, shared-storage paths, and generated handoffs.

## Locked study design

| Item | Decision |
| --- | --- |
| Selected cities | Dhaka, Dinājpur, Bherāmāra, Bhola, Cox’s Bāzār |
| Common period | 5 August 2022–23 November 2025 |
| Daily AQI | Maximum supplied hourly AQI for a city-date with at least 18 valid AQI hours |
| Positive class | Next calendar day's daily maximum AQI > 150 |
| Historical signals | Daily AQI plus daily mean and maximum for PM10, PM2.5, CO, NO2, SO2, and O3 |
| Features | 1-, 2-, and 7-day lags plus shifted 3- and 7-day rolling means |
| Predictor count | 65 |
| Source city | Dhaka |
| Transfer cities | Dinājpur, Bherāmāra, Bhola, Cox’s Bāzār |
| Split | Chronological and shared across all five cities |
| Baseline | Persistence: tomorrow's class equals today's class |
| Primary metrics | PR-AUC (average precision) and recall |
| CO2 | Excluded |

The five cities were selected for complete common coverage and geographic diversity, not for their target prevalence or expected model performance. All features use day `t` or earlier to predict exactly day `t+1`.

## Notebook results

### 01 — Audit and EDA

- Audited 1,048,551 hourly rows and 13 columns.
- Identified 30 AQI cities versus 103 metadata cities and documented truncation evidence.
- Found no exact duplicates, duplicate city–timestamp pairs, or timestamp gaps in the selected series.
- Found approximately 74% missing CO2, one negative NO2 value, and eleven negative O3 values.
- Locked the five-city common scope and daily aggregation rules.

### 02 — Preprocessing

- Filtered 144,840 hourly rows in the locked scope.
- Converted invalid negative NO2/O3 readings to missing and excluded CO2.
- Aggregated to 6,035 unique city-date rows: 1,207 dates per city and 24 columns.
- Retained observation and valid-hour counts; no imputation was used.
- Produced a complete daily handoff with no missing values in the selected scope.

### 03 — Feature engineering

- Created 65 strictly historical predictors from 13 signals.
- Shifted before rolling and verified every feature's historical origin.
- Produced 6,000 modeling rows, 1,200 per city, and 71 total columns.
- Main-target positives: 2,399 (39.98%); sensitivity-target positives: 3,703 (61.72%).
- Removed only the first seven target dates per city because complete seven-day history did not exist.

### 04 — Modeling and tuning

- Froze common chronological splits: 4,200 train rows, 900 validation rows, and 900 untouched test rows.
- Used four expanding-window folds within the 840-row Dhaka training period.
- Tuned Logistic Regression, Random Forest, and Histogram Gradient Boosting by mean validation average precision.
- Selected Logistic Regression (`C=1.0`, `class_weight="balanced"`) using Dhaka validation evidence.
- Selected threshold `0.008870` by maximizing validation F2, with recall prioritized in tie-breaking.
- Refit the frozen 65-feature model on 1,020 Dhaka train-plus-validation rows without accessing test outcomes.
- The strongest validation permutation-importance feature was `pm25_mean_lag1`.

### 05 — Final evaluation and error analysis

- Scored the frozen model exactly once on 900 held-out rows from 28 May–23 November 2025.
- The model beat persistence on PR-AUC and recall in 5 of 5 cities.
- Dhaka within-city: PR-AUC 0.9559, recall 1.0000.
- Four-city transfer pooled: PR-AUC 0.9376, recall 0.9932.
- Cox’s Bāzār was the weakest transfer city: PR-AUC 0.6280, recall 0.9091.
- The model produced one false negative, compared with 37 for persistence.
- Feature-day and target-day coverage counts were constant at 24, so reduced measurement coverage did not explain test errors.

## Research questions

1. **Transfer:** The Dhaka-trained model retained very high pooled transfer recall, although performance weakened most in Cox’s Bāzār.
2. **Baseline comparison:** The frozen model exceeded persistence on both primary metrics overall and in every selected city.
3. **Predictive history:** Validation permutation importance ranked recent PM2.5 history highest, led by `pm25_mean_lag1`; this is predictive evidence, not a causal claim.

## Notebooks

| Notebook | Responsibility | Status | Open in Colab |
| --- | --- | --- | --- |
| `01_data_audit_and_eda.ipynb` | Coverage, integrity, truncation audit, EDA, and scope selection | Gate passed | [Open](https://colab.research.google.com/github/ArafUlHaque/cse437-air-quality-group-18/blob/main/notebooks/01_data_audit_and_eda.ipynb) |
| `02_preprocessing.ipynb` | Cleaning, filtering, daily aggregation, and calendar completion | Gate passed | [Open](https://colab.research.google.com/github/ArafUlHaque/cse437-air-quality-group-18/blob/main/notebooks/02_preprocessing.ipynb) |
| `03_feature_engineering.ipynb` | Leakage-safe targets, lag features, rolling features, and manifest | Gate passed | [Open](https://colab.research.google.com/github/ArafUlHaque/cse437-air-quality-group-18/blob/main/notebooks/03_feature_engineering.ipynb) |
| `Notebook_04_final 2.0.ipynb` | Chronological splits, persistence, model tuning, selection, and frozen protocol | Gate passed | [Open](https://colab.research.google.com/github/ArafUlHaque/cse437-air-quality-group-18/blob/main/notebooks/Notebook_04_final%202.0.ipynb) |
| `Notebook_05_evaluation_and_error_analysis (1).ipynb` | Untouched-test evaluation, transfer study, and error analysis | Gate passed | [Open](https://colab.research.google.com/github/ArafUlHaque/cse437-air-quality-group-18/blob/main/notebooks/Notebook_05_evaluation_and_error_analysis%20%281%29.ipynb) |

Run the notebooks in numerical order from fresh runtimes after the required shared artifacts exist. Each executed notebook contains its own assertions and saved-file readback checks.

## Reproduction and storage

1. Add the shared folder to **My Drive** as `CSE437_air_quality_group_18`.
2. Keep the untouched source files in `MyDrive/CSE437_air_quality_group_18/raw/`.
3. Use `processed/`, `figures/`, and `models/` inside that folder for generated artifacts.
4. Open the tracked notebooks from the links above; they mount Drive and do not need to clone the repository inside Colab.
5. Do not commit raw data, generated CSV handoffs, large model binaries, secrets, or personal Drive paths.

The exact workflow, frozen decisions, artifact contracts, and remaining report task are documented in [PROJECT_PLAN.md](PROJECT_PLAN.md). AI assistants must also follow [AGENTS.md](AGENTS.md).

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
│   ├── Notebook_04_final 2.0.ipynb
│   └── Notebook_05_evaluation_and_error_analysis (1).ipynb
├── src/
│   └── utils.py
├── models/
│   └── README.md
├── figures/
│   └── README.md
└── report/
    └── report.md
```

## Team

| Member | Student ID | GitHub username |
| --- | --- | --- |
| Araf Ul Haque | _Add before submission_ | [ArafUlHaque](https://github.com/ArafUlHaque) |
| S M Arham Ali | _Add before submission_ | [WhyNotInan](https://github.com/WhyNotInan) |

