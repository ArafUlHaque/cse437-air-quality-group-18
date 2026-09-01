# CSE437: Next-Day Unhealthy Air Quality Classification

## Problem statement

Predict future air pollution levels by classifying whether the next day's Air Quality Index (AQI) falls into an unhealthy category.

## Target variable

`next_day_unhealthy`: whether the next day's AQI belongs to the unhealthy category defined for the project. The exact category boundary must be documented before target construction and then used consistently throughout the notebooks and report.

## Dataset

- **Name:** Bangladesh Air Quality Index (AQI) Dataset (2000–2025): Historical Hourly Air Pollution Data Across 103 Cities
- **Source:** [Mendeley Data, Version 2](https://data.mendeley.com/datasets/9j447cynb9/2)
- **DOI:** [10.17632/9j447cynb9.2](https://doi.org/10.17632/9j447cynb9.2)
- **License:** CC BY 4.0
- **Summary:** 1,048,551 hourly observations, 103 cities, and 13 columns. City coverage varies over time and the dataset contains missing values.

Raw data is not stored in Git because it exceeds the course's 50 MB repository limit. See [`data/README.md`](data/README.md) for download and placement instructions.

## Research questions

1. Which cities experience the highest pollution levels?
2. How do pollution levels vary across seasons and times of day?
3. Which historical pollutant measurements best predict future air quality?

## Repository structure

```text
cse437-air-quality-group-18/
├── README.md
├── requirements.txt
├── .gitignore
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

The final `report/report.pdf` will be added when the report is complete.

## Notebook order

Run the notebooks in numerical order from `01` through `05`. Each notebook is expected to run from top to bottom on a fresh kernel, and its outputs should be saved before submission.

## Kaggle setup

1. Clone the existing [`cse437-air-quality-group-18`](https://github.com/ArafUlHaque/cse437-air-quality-group-18) repository.
2. Upload the original Mendeley file as a private Kaggle Dataset, or add an existing Kaggle copy whose contents you have verified against the Mendeley source.
3. Create a Kaggle Notebook and attach the raw dataset.
4. Clone or upload this repository into the Kaggle working directory.
5. Copy the untouched source CSV into `data/raw/`, keeping its original filename. Do not edit the raw file.
6. Open the project notebook you want to run, keep the repository root as the working directory, and use relative paths only.
7. Run notebooks in order and commit the updated notebooks, processed outputs, figures, and final report as appropriate.

Kaggle already includes the main data-science packages. For another environment, install the declared dependencies with:

```bash
pip install -r requirements.txt
```

## Reproducibility rules

- Never modify files in `data/raw/`.
- Write cleaned datasets to `data/processed/`.
- Use relative paths; do not use local `C:/...` paths or Google Drive mounts.
- Keep reusable functions in `src/utils.py`.
- Save report figures in `figures/`.
- Save trained model artifacts in `models/`, but do not commit large binaries.
- Use a fixed random seed where randomness is involved.
- Every member should commit from their own GitHub account throughout the project.

## Team

| Member | Student ID | GitHub username |
| --- | --- | --- |
| _Add member_ | _Add ID_ | _Add username_ |
| _Add member_ | _Add ID_ | _Add username_ |
| _Add member_ | _Add ID_ | _Add username_ |
