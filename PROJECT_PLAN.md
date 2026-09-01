# Project Plan

This is the authoritative execution plan for CSE437 Group 18. Both team members and any AI agent must read this file before changing a notebook. Faculty feedback overrides earlier ideas.

## 1. Goal and success condition

Build a reproducible binary-classification study that predicts whether a selected city's **next calendar day** has daily AQI greater than 150, using only historical information available through the current day.

A successful result is not simply a high score. The final model must be compared honestly with persistence. If no model beats persistence on PR-AUC and recall during the untouched test period, that is the correct finding.

## 2. Locked decisions

| Item | Decision |
| --- | --- |
| Main task | Next-day binary classification |
| Positive class | Next day's daily AQI > 150 (integer AQI 151+) |
| Optional sensitivity target | AQI >= 101, named separately as USG-or-worse |
| Geography | Dhaka plus 2–4 smaller cities chosen after audit |
| Time unit | One row per city per calendar day |
| CO2 | Drop; never use as a predictor |
| Feature timing | Strictly lagged; no same-day information from label day |
| Split | Chronological date split; never random |
| Baseline | Persistence before ML |
| Primary metrics | PR-AUC and recall |
| Secondary metrics | Precision, F1, confusion matrix, class prevalence |
| Cross-city study | Train on Dhaka; test transfer to eligible smaller cities |
| Seasonality | Optional only if Notebook 01 proves adequate coverage |

### Pending decisions that require data

- Exact source filename and schema
- Reliable timestamp column and timezone interpretation
- Whether daily AQI should be the maximum provided hourly AQI; this is the proposed primary aggregation and must be justified after inspection
- Selected 3–5 cities and common study interval
- Missingness thresholds and imputation rules
- Exact chronological cut dates
- Final lag windows and model families

No agent may silently decide these from assumptions. Record each decision with evidence in the relevant notebook.

## 3. Faculty conditions converted into checks

Notebook 01 must print and save:

- total row count and column count;
- exact minimum and maximum timestamp;
- duplicate-row and duplicate city-timestamp counts;
- rows, unique timestamps, first date, last date, and observed duration per city;
- expected versus observed hourly rows per city;
- distribution of readings per city-day;
- missingness by column and city;
- invalid pollutant/AQI values;
- temporal gaps and whether cities share an overlapping study period;
- class prevalence under both >150 and >=101 candidate thresholds after a provisional daily aggregation;
- evidence that the file is or is not close to an Excel-truncated export.

### Audit gate

Before Notebook 02 begins, the team must write down:

1. the verified dataset coverage;
2. the selected 3–5 cities;
3. their common study dates;
4. whether seasonality is defensible;
5. the daily AQI aggregation;
6. the main target threshold;
7. any columns excluded and why.

If these are missing, stop. Do not build features or models.

## 4. Research questions

- **RQ1 — Transfer:** How well does a model trained on Dhaka transfer to smaller Bangladeshi cities with comparable temporal coverage?
- **RQ2 — Baseline comparison:** Can machine-learning models outperform persistence for next-day unhealthy-air prediction?
- **RQ3 — Predictive history:** Which strictly lagged pollutants and historical windows contribute most to next-day unhealthy-air prediction?

Possible city ranking, time-of-day, and seasonal plots are descriptive EDA, not primary research questions. Seasonality is removed if coverage is too short or unbalanced.

## 5. Notebook contracts

### Notebook 01 — Data audit and EDA

**Input:** untouched source file.

**Required work:**

1. Load without changing the raw file.
2. Display schema, types, example rows, and memory use.
3. Complete the arithmetic/coverage/truncation audit.
4. Inspect missingness, duplicates, invalid values, gaps, and city overlap.
5. Show careful descriptive plots, including AQI/pollutant distributions and city coverage.
6. Evaluate candidate cities using explicit eligibility criteria.
7. Write the audit-gate decision summary.

**Outputs:**

- `processed/city_coverage_summary.csv`
- `processed/audit_summary.json`
- figures used in the report
- a visible final markdown cell recording decisions

**Acceptance:** another person can understand why the cities and dates were chosen.

### Notebook 02 — Preprocessing

**Input:** raw data plus Notebook 01 decisions.

**Required work:**

1. Keep only selected cities and the common period.
2. Parse and sort timestamps; resolve duplicates explicitly.
3. Drop CO2 and exclude identifiers that cannot predict future air quality.
4. Handle impossible readings and missing values with justified rules.
5. Aggregate hourly values to daily values. Preserve coverage indicators such as hourly observation count.
6. Create a complete city-by-calendar-day index.
7. Keep missing days visible; do not make the next observed row look like the next day.
8. Compare before/after row counts and missingness.

**Output:** `processed/daily_air_quality.csv`.

**Acceptance:** exactly one unique row per city-date, sorted by city/date, with documented transformations.

### Notebook 03 — Feature engineering

**Input:** daily clean data.

**Required work:**

1. Construct the day-`t+1` label only after the complete calendar index exists.
2. Require `target_date - feature_date == 1 day`.
3. Create lag features from day `t` and earlier.
4. For rolling features, shift first and roll second.
5. Consider simple lags and rolling summaries, then control feature count.
6. Keep city/date identifiers for grouping and evaluation but not as accidental leakage.
7. Report class balance and dropped rows caused by lagging.
8. Add programmatic leakage assertions.

**Output:** `processed/modeling_dataset.csv`.

**Acceptance:** every feature has an auditable time origin no later than day `t`.

### Notebook 04 — Modeling and tuning

**Input:** modeling dataset.

**Required work:**

1. Freeze chronological train, validation, and test periods.
2. Never touch the test labels during selection/tuning.
3. Build persistence first: tomorrow's class equals today's class.
4. Add a simple interpretable baseline such as logistic regression.
5. Add a small number of justified nonlinear models; keep tuning spaces modest.
6. Tune only with training/validation data using time-aware procedures.
7. Address imbalance through model weighting/threshold selection only inside training/validation.
8. Run within-city and Dhaka-to-smaller-city transfer experiments.
9. Select one final model and decision threshold without test optimization.

**Outputs:**

- validation comparison table;
- fitted model and preprocessing artifacts in shared storage;
- frozen split dates and feature list.

**Acceptance:** persistence is visible before ML results and the test period is still untouched.

### Notebook 05 — Evaluation and error analysis

**Input:** frozen test data, persistence outputs, and final model.

**Required work:**

1. Evaluate once on the untouched test period.
2. Report class prevalence, PR-AUC, recall, precision, F1, and confusion matrices.
3. Compare the same test rows against persistence.
4. Report results overall and by city.
5. Analyze false negatives first because missed unhealthy days matter.
6. Inspect errors by AQI severity, missingness/coverage, and time.
7. Explain transfer failures and dataset limitations.
8. State clearly whether ML beat persistence.

**Outputs:** test-results tables, final figures, and text ready for `report/report.md`.

**Acceptance:** conclusions match the displayed evidence, including negative results.

## 6. Leakage rules

For a prediction issued after day `t`:

- allowed: measurements and aggregates from day `t` or earlier;
- prohibited: any pollutant/AQI observation from day `t+1`;
- prohibited: centered rolling windows;
- prohibited: imputation fitted using validation/test future values;
- prohibited: random train/test splitting;
- prohibited: tuning a threshold on test labels;
- prohibited: same-timestamp pollutants used to reconstruct the same timestamp's AQI label.

Minimum assertions should verify unique city-dates, sorted dates, exact next-day label alignment, disjoint chronological splits, and absence of future-derived feature columns.

## 7. Recommended modeling scope

Keep the study small enough to explain:

1. Persistence baseline
2. Logistic regression
3. Random forest or a comparable bagged-tree model
4. One gradient-boosting model available in the declared dependencies

Do not add deep learning unless the faculty explicitly asks for it. Prefer clear tuning and error analysis over many models.

## 8. Recommended two-person division

| Phase | Member A | Member B | Joint checkpoint |
| --- | --- | --- | --- |
| Setup | Maintain plan and Colab workflow | Verify source/citations and report outline | Agree on branches and shared Drive |
| Audit | Own Notebook 01 | Review audit code/results independently | Approve audit-gate decisions |
| Data | Own Notebook 02 | Own Notebook 03 after the daily file is frozen | Run leakage and reproducibility review |
| Models | Review baseline and splits | Own Notebook 04 | Freeze model and threshold |
| Final | Own plots/error tables | Draft methods/results | Complete Notebook 05, report, viva prep |

Replace Member A/B with names before submission. Ownership does not remove the review requirement.

## 9. Git and Colab workflow

- Branch from current `main`.
- Use one owner per notebook at a time.
- Use the shared Drive shortcut `MyDrive/CSE437_air_quality_group_18` for raw data, processed handoffs, and large models.
- Save notebook outputs before committing.
- Do not commit raw data, secrets, Drive paths containing personal names, or large binaries.
- Open a pull request and obtain teammate review.
- After merge, both members pull the new `main`.

Suggested branch names:

- `notebook-01-audit-<name>`
- `notebook-02-preprocessing-<name>`
- `notebook-03-features-<name>`
- `notebook-04-models-<name>`
- `notebook-05-evaluation-<name>`
- `report-<section>-<name>`

## 10. AI-agent handoff prompt

Give an AI agent a bounded task, for example:

> Read AGENTS.md and PROJECT_PLAN.md completely. Work only on Notebook 01 on branch notebook-01-audit-<name>. Implement the required audit checks without training a model. Do not invent column names; inspect the actual file first. Keep code simple and notebook-friendly. End with a decision summary and list any decisions that still require human approval.

Never ask two agents to edit the same notebook at the same time. Review every generated cell and verify outputs yourself.

## 11. Definition of done

- All five notebooks run in order from fresh Colab runtimes using shared artifacts.
- All charts and numbers come from executed code.
- The coverage/truncation concern is answered explicitly.
- The target definition and exact date alignment are visible.
- No leakage or random temporal split exists.
- Persistence and ML use identical test rows.
- PR-AUC and recall lead the evaluation.
- Transfer results are reported for eligible smaller cities.
- Limitations discuss coverage, possible truncation/generation concerns, missingness, and generalizability.
- README, report, requirements, notebook outputs, and GitHub contribution history are current.
