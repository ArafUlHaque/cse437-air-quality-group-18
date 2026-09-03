# Figures

Notebook figures are generated reproducibly in the shared Google Drive project folder. The final report will decide which report-ready copies should be committed here later.

## Notebook 04

Directory: `MyDrive/CSE437_air_quality_group_18/figures/notebook_04/`

| Figure | Contents |
| --- | --- |
| `validation_pr_curves.png` | Dhaka validation precision–recall curves for persistence and the three tuned model families |

This is validation-only development evidence and must not be presented as final test performance.

## Notebook 05

Directory: `MyDrive/CSE437_air_quality_group_18/figures/notebook_05/`

| Figure | Contents |
| --- | --- |
| `test_pr_curves.png` | Pooled untouched-test precision–recall comparison |
| `test_confusion_matrices.png` | Pooled confusion matrices for Logistic Regression and persistence |
| `test_per_city_metrics.png` | Per-city primary-metric comparison |
| `test_monthly_recall.png` | Descriptive monthly recall during the test period |

Notebook 05 saved and verified all four files before printing `NOTEBOOK 05 FINAL EVALUATION GATE PASSED`.

## Report policy

- Use descriptive, stable filenames for any report figures copied into this repository.
- Copy only figures selected for the written report; do not change the underlying values manually.
- Keep captions consistent with the frozen split, model, threshold, and Notebook 05 metrics.
- Clearly distinguish validation figures from untouched-test figures.
- Preserve readable labels and Unicode city names.

## Committed report figures

The following exact notebook outputs are copied to `figures/report/` so that `report/report.md` renders reproducibly:

- `figure_1_aqi_distribution_and_correlation.png`
- `figure_2_test_pr_curves.png`
- `figure_3_test_confusion_matrices.png`

These copies must remain identical to the executed notebook outputs.
