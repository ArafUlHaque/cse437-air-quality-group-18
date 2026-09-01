# Data

## Source

**Bangladesh Air Quality Index (AQI) Dataset (2000–2025): Historical Hourly Air Pollution Data Across 103 Cities**

- Dataset page: <https://data.mendeley.com/datasets/9j447cynb9/2>
- Version: 2
- DOI: <https://doi.org/10.17632/9j447cynb9.2>
- Contributor: Tapon Paul
- License: Creative Commons Attribution 4.0 (CC BY 4.0)
- Published: 21 January 2026
- Published description: 1,048,551 hourly records, 103 cities, 13 columns

The title, city count, claimed period, and row count do not establish actual coverage. Complete hourly data for 103 cities over 25 years would be far larger. Notebook 01 must print the real timestamp range and coverage per city and investigate possible export truncation.

## Obtain and store the raw data

1. Download Version 2 from the Mendeley page.
2. Extract it without editing the source file.
3. Create the shared Google Drive folder described in the root README.
4. Place the untouched source file in:
   `MyDrive/CSE437_air_quality_group_18/raw/`
5. Give both team members editor access and ensure both add the same-named shortcut to My Drive.
6. Record the actual details below.

Raw data is excluded from Git because of the course repository size limit.

| Item | Value |
| --- | --- |
| Source filename | _Fill after download_ |
| Downloaded file size | _Fill after download_ |
| Download date | _YYYY-MM-DD_ |
| SHA-256 checksum | _Fill after download_ |
| Version | 2 |

## Shared folder policy

- `raw/`: original files only; never edit or overwrite them.
- `processed/`: notebook handoff files such as audit summaries, daily data, and modeling data.
- `models/`: fitted artifacts too large for GitHub.
- Regenerate processed data through notebooks; do not edit it manually.

The repository contains placeholder `data/raw/` and `data/processed/` directories only to document the intended structure.

## Required day-one verification

Notebook 01 must verify rather than assume:

- exact filename, delimiter, encoding, and schema;
- total rows and columns;
- minimum/maximum timestamp;
- rows and date coverage per city;
- readings per city-day and temporal gaps;
- missingness, duplicates, and invalid values;
- overlap among candidate cities;
- whether the row count suggests truncation.

Do not silently rename columns or make seasonal claims before this audit.
