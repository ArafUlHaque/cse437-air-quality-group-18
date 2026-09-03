# Data and Generated Handoffs

## Source

**Bangladesh Air Quality Index (AQI) Dataset (2000–2025): Historical Hourly Air Pollution Data Across 103 Cities**

- Dataset page: <https://data.mendeley.com/datasets/9j447cynb9/2>
- Version: 2
- DOI: <https://doi.org/10.17632/9j447cynb9.2>
- Contributor: Tapon Paul
- License: Creative Commons Attribution 4.0 (CC BY 4.0)
- Published: 21 January 2026
- Published description: 1,048,551 hourly records, 103 cities, 13 columns

## Raw files and integrity

Store both untouched files in `MyDrive/CSE437_air_quality_group_18/raw/`. They are excluded from Git because of the repository size limit.

| File | Purpose | Verified size | SHA-256 |
| --- | --- | ---: | --- |
| `AQI Bangladesh.csv` | Main hourly air-quality observations | 93.75 MiB | `8760175fc048eea4180b828fd60d10cb799a73a5144a7e4aca19ddbaf8dbdd62` |
| `cities.csv` | Published 103-city metadata and coordinates | 3,411 bytes | `dc0b7b598a2c595daf942d1011681fcd1d3475e398579d29180d0526b4ac102c` |

Do not rename, edit, overwrite, or manually clean these files. All transformations must be reproducible through the notebooks.

## Verified Notebook 01 audit

- Main AQI file: 1,048,551 rows, 13 source columns, 30 cities.
- Metadata file: 103 cities; 73 metadata cities are absent from the AQI file.
- Recorded range: 1 January 2000–23 November 2025.
- Dhaka has 9,459 days of history; most non-Dhaka cities have 1,208 days beginning 4 August 2022.
- The file ends 24 data rows below Excel's worksheet limit, and the final city block is incomplete.
- The evidence strongly indicates an Excel-truncated export; the data must not be described as complete coverage of 103 cities.
- No exact duplicates or duplicate city–timestamp pairs were found.
- CO2 is about 74% missing; one negative NO2 and eleven negative O3 observations were found.

The faculty allowed the project to proceed with this limitation documented.

## Locked analytical scope

- Cities: Dhaka, Dinājpur, Bherāmāra, Bhola, and Cox’s Bāzār.
- Common period: 5 August 2022–23 November 2025.
- Common usable dates: 1,207 per city.
- Daily AQI: maximum supplied hourly AQI for each city-date with at least 18 valid AQI hours.
- Main target: next calendar day's daily maximum AQI > 150.
- CO2: excluded.
- Negative NO2/O3: converted to missing during preprocessing.

## Generated handoffs

Generated CSV, JSON, model, and figure artifacts are stored in the shared Drive project folder and excluded from GitHub. Regenerate them by running the notebooks in numerical order; never edit them manually.

### Notebook 01 — audit evidence

Directory: `processed/notebook_01_audit/`

Contains the audit tables and summary used to lock the dataset scope and document the truncation limitation.

### Notebook 02 — daily preprocessing

| Artifact | Purpose |
| --- | --- |
| `processed/daily_air_quality.csv` | Frozen daily dataset: 6,035 rows, 24 columns |
| `processed/notebook_02_preprocessing_summary.json` | Preprocessing rules, counts, and readback evidence |

Notebook 02 aggregated 144,840 selected hourly rows into 1,207 dates for each of five cities. The selected daily output has no missing values, and calendar reindexing inserted no rows.

### Notebook 03 — model-ready features

| Artifact | Purpose |
| --- | --- |
| `processed/modeling_dataset.csv` | Frozen 6,000-row model-ready dataset with 65 predictors |
| `processed/notebook_03_feature_manifest.csv` | Source, timing, and definition for every predictor |
| `processed/notebook_03_feature_summary.json` | Feature-engineering counts, rules, and checksums |

Notebook 03 created 6,000 rows, 1,200 per city, and 71 columns: three identifiers, three outcomes, and 65 complete historical predictors. The main target contains 2,399 positives (39.98%).

### Notebook 04 — model-development evidence

| Artifact | Purpose |
| --- | --- |
| `processed/notebook_04_split_assignments.csv` | Identifier-only chronological split membership |
| `processed/notebook_04_cv_results.csv` | Four-fold expanding-window tuning results |
| `processed/notebook_04_validation_results.csv` | Persistence and candidate validation comparison |
| `processed/notebook_04_validation_feature_importance.csv` | Validation-only permutation importance |
| `processed/notebook_04_modeling_summary.json` | Frozen model-development summary and protocol references |

The frozen dates produce 4,200 train, 900 validation, and 900 untouched test rows, with 840/180/180 rows per city. Test labels were not used for model or threshold selection.

The fitted model and protocol are stored separately under `models/notebook_04/`; the validation precision–recall figure is under `figures/notebook_04/`.

### Notebook 05 — final evaluation evidence

| Artifact | Purpose |
| --- | --- |
| `processed/notebook_05_test_predictions.csv` | Frozen model and persistence scores/predictions on all test rows |
| `processed/notebook_05_overall_results.csv` | Pooled model and persistence metrics |
| `processed/notebook_05_per_city_results.csv` | Within-city and transfer-city metrics |
| `processed/notebook_05_false_negatives.csv` | Missed unhealthy days and severity evidence |
| `processed/notebook_05_monthly_results.csv` | Descriptive month-level test metrics |
| `processed/notebook_05_transfer_results.csv` | Dhaka versus pooled four-city transfer comparison |
| `processed/notebook_05_coverage_diagnostic.csv` | Coverage values by outcome/error type |
| `processed/notebook_05_evaluation_summary.json` | Final frozen metrics, verdict, and environment record |

Notebook 05 evaluated 900 rows from 28 May–23 November 2025. There were 188 positive days (20.89%). Logistic Regression achieved average precision 0.9359 and recall 0.9947; persistence achieved 0.7003 and 0.8032. The final evaluation gate passed.

## Shared folder policy

- `raw/`: original files only; never edit or overwrite them.
- `processed/notebook_01_audit/`: Notebook 01 audit tables and summary.
- `processed/`: frozen daily, feature, modeling, and final-evaluation handoffs.
- `figures/notebook_04/`: validation-only model-development figure.
- `figures/notebook_05/`: final evaluation figures.
- `models/notebook_04/`: frozen fitted model and machine-readable protocol.
- Regenerate every artifact through its notebook; do not edit generated evidence manually.

The repository contains placeholder `data/raw/` and `data/processed/` directories only to document the intended structure.

