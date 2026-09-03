# Models

The final fitted model is stored in shared Google Drive rather than GitHub because generated binary artifacts are excluded from version control.

## Frozen Notebook 04 model

| Item | Frozen value |
| --- | --- |
| Model family | Logistic Regression |
| Hyperparameters | `C=1.0`, `class_weight="balanced"`, `solver="liblinear"`, `max_iter=3000` |
| Predictors | 65 columns in the Notebook 03 feature manifest |
| Source city | Dhaka |
| Fit period | 12 August 2022–27 May 2025 |
| Final fitting rows | 1,020 train-plus-validation rows |
| Decision threshold | `0.008870` |
| Threshold objective | Maximum Dhaka validation F2, with recall prioritized in tie-breaking |
| Test data used during selection | No |

## Shared-Drive artifacts

Store these files under `MyDrive/CSE437_air_quality_group_18/models/notebook_04/`:

| Artifact | Purpose |
| --- | --- |
| `final_model.joblib` | Fitted scikit-learn pipeline used once in Notebook 05 |
| `final_model_protocol.json` | Feature order, target definition, model settings, threshold, split dates, checksums, and test policy |

The protocol is part of the model contract. Notebook 05 verifies it before loading test outcomes and must not refit the model, reorder features, or change the threshold.

## Reproduction

Run the notebooks in order through `notebooks/Notebook_04_final 2.0.ipynb` after the Notebook 03 handoffs exist. Notebook 04 saves both artifacts, reloads them, checks the frozen settings, and prints `NOTEBOOK 04 MODELING AND TUNING GATE PASSED` when verification succeeds.

Do not commit generated model binaries. Do not manually edit the protocol or use the final test results to retune the model.

