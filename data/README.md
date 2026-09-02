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

## Raw files and integrity

Store both untouched files in `MyDrive/CSE437_air_quality_group_18/raw/`. They are excluded from Git because of the repository size limit.

| File | Purpose | Verified size | SHA-256 |
| --- | --- | ---: | --- |
| `AQI Bangladesh.csv` | Main hourly air-quality observations | 93.75 MiB | `8760175fc048eea4180b828fd60d10cb799a73a5144a7e4aca19ddbaf8dbdd62` |
| `cities.csv` | Published 103-city metadata and coordinates | 3,411 bytes | `dc0b7b598a2c595daf942d1011681fcd1d3475e398579d29180d0526b4ac102c` |

Do not rename, edit, overwrite, or manually clean these files. All transformations must be reproducible through the notebooks.

## Verified Notebook 01 audit

- Main AQI file: 1,048,551 rows, 13 source columns, 30 cities.
- Metadata file: 103 cities.
- Metadata cities absent from the AQI file: 73.
- Recorded range: 1 January 2000–23 November 2025.
- Dhaka has 9,459 days of history; most non-Dhaka cities have 1,208 days beginning 4 August 2022.
- The file ends 24 data rows below Excel's limit, and the final city block is incomplete.
- The evidence strongly indicates an Excel-truncated export; the data must not be described as complete coverage of 103 cities.
- No exact duplicates or duplicate city–timestamp pairs were found.
- CO2 is about 74% missing; one negative NO2 and eleven negative O3 observations were found.

The faculty has allowed the project to proceed with this limitation documented.

## Locked analytical scope

- Cities: Dhaka, Dinājpur, Bherāmāra, Bhola, and Cox’s Bāzār.
- Main common period: 5 August 2022–23 November 2025.
- Common usable dates: 1,207 for every selected city.
- Daily AQI: maximum supplied hourly AQI for each city-date.
- Minimum daily AQI coverage: 18 valid hourly observations.
- Main target: next calendar day's daily maximum AQI > 150.
- CO2: excluded.
- Negative NO2/O3: converted to missing during preprocessing.

## Verified Notebook 02 output

Notebook 02 verified the audited source checksum, applied the locked scope, removed CO2 and static identifiers, and created the daily handoff without modifying the raw files.

- Selected hourly rows: 144,840.
- Daily rows: 6,035, consisting of 1,207 dates for each of five cities.
- Daily columns: 24.
- Pollutant summaries: daily mean and maximum of valid hourly readings.
- Coverage fields: observed rows, observed hours, AQI valid hours, and pollutant valid hours.
- Missing values in the selected daily output: zero.
- Calendar rows inserted during reindexing: zero.
- Targets and model features created: none.

The generated handoffs are `processed/daily_air_quality.csv` and `processed/notebook_02_preprocessing_summary.json` in the shared Drive folder. Regenerate them by running Notebook 02; do not edit them manually.

## Shared folder policy

- `raw/`: original files only; never edit or overwrite them.
- `processed/notebook_01_audit/`: Notebook 01 audit tables and summary.
- `processed/`: Notebook 02 handoffs plus later files such as `modeling_dataset.csv`.
- `figures/`: reproducible figures used in notebooks and the report.
- `models/`: fitted artifacts too large for GitHub.
- Regenerate processed data through notebooks; do not edit it manually.

The repository contains placeholder `data/raw/` and `data/processed/` directories only to document the intended structure.
