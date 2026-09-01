# AGENTS.md

These instructions apply to every AI agent or coding assistant working in this repository.

## Read first

Read `PROJECT_PLAN.md` completely before editing. Treat faculty conditions and locked decisions there as authoritative.

## Scope and sequencing

- Work only on the notebook/file assigned by the user.
- Notebook order is a dependency chain: 01 → 02 → 03 → 04 → 05.
- Do not implement preprocessing, features, or models until Notebook 01 records and passes its audit gate.
- Do not rewrite another teammate's work or alter unrelated files.
- Ask before changing a locked decision.

## Data and evidence

- Never modify files in `data/raw/`.
- Never invent column names, results, dates, city coverage, metrics, or conclusions.
- Only write factual findings supported by displayed notebook output.
- Do not commit secrets, raw data, large binaries, or personal Drive paths.
- Keep code simple, readable, and suitable for Google Colab.

## Non-negotiable modeling rules

- Main positive target: next calendar day's daily AQI > 150.
- Drop CO2.
- Use Dhaka plus 2–4 cities selected from the audit.
- All features must come from day t or earlier.
- Confirm the label belongs to exactly day t+1; the next row is not automatically the next day.
- Shift before calculating rolling features.
- Split by date, never randomly.
- Fit imputers/scalers/selectors only on training data.
- Build persistence before ML.
- Lead evaluation with PR-AUC and recall; accuracy is secondary.
- Never tune on the test period.

## Quality checks

Before finishing a task:

1. Run changed code top-to-bottom when data/runtime access permits.
2. Add assertions for important invariants.
3. Keep notebook outputs and markdown explanations consistent.
4. State anything that could not be verified.
5. Summarize changed files and the next dependency.
