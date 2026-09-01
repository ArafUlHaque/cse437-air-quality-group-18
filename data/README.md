# Data

## Source

**Bangladesh Air Quality Index (AQI) Dataset (2000–2025): Historical Hourly Air Pollution Data Across 103 Cities**

- Dataset page: <https://data.mendeley.com/datasets/9j447cynb9/2>
- Version: 2
- DOI: <https://doi.org/10.17632/9j447cynb9.2>
- Contributor: Tapon Paul
- License: Creative Commons Attribution 4.0 (CC BY 4.0)
- Published: 21 January 2026
- Dataset description: 1,048,551 hourly records across 103 Bangladeshi cities, supplied as a CSV with 13 columns.

## How to obtain the raw data

1. Open the Mendeley Data link above.
2. Select **Download All** for Version 2.
3. Extract the archive without editing its contents.
4. Place the original CSV file in `data/raw/` and keep the source filename unchanged.
5. Record the downloaded filename and byte size in the table below.

Because the raw dataset is larger than the course's 50 MB Git limit, it is excluded by `.gitignore`. Do not commit it to GitHub.

| Item | Value |
| --- | --- |
| Source filename | _Fill in after download_ |
| Downloaded file size | _Fill in after download_ |
| Download date | _YYYY-MM-DD_ |
| Version | 2 |

## Folder policy

- `raw/`: original downloaded files only; never overwrite or edit them.
- `processed/`: outputs produced by the preprocessing notebook.
- Do not manually modify processed data; regenerate it by running the notebooks.

## Expected source contents

The publisher describes 13 columns containing city identifiers and names, latitude and longitude, ISO 8601 timestamps, pollutant measurements, and AQI. The exact downloaded schema must be checked and documented in `01_data_audit_and_eda.ipynb`; do not silently rename or assume columns before that audit.

