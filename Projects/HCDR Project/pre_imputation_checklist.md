# HCDR Notebook — Pre-Imputation Checklist

Everything below needs to be addressed in `first_HCDR_project_notebook.ipynb` before starting imputation. Check items off as you complete them.

## 1. Decision statements (every existing subsection)

Each subsection needs the four-part structure: title/intro → code → observation → **Decision**. Currently none have observation/decision cells.

- [ ] Missing Values — Numeric
- [ ] Missing Values — Categorical
- [ ] Target Distribution & Class Imbalance
- [ ] Univariate — Binary/Continuous Separation
- [ ] Univariate — Numeric Variable Overview
- [ ] Univariate — Skew Flagging
- [ ] Univariate — Categorical Variables (describe, unique values, cardinality)
- [ ] Univariate — Binary Variables
- [ ] Bivariate — KDE Separation Plots
- [ ] Bivariate — Bucketing Method
- [ ] Correlation Analysis — Heatmap

## 2. Data quality fixes

- [ ] `DAYS_EMPLOYED`: convert sentinel value `365243` to `NaN` (it's a placeholder for unemployed/pensioner, not a real tenure) — do this before any stats or imputation touch the column
- [ ] Decide whether to add a `DAYS_EMPLOYED_ANOM` flag column to preserve the signal that was in the sentinel
- [ ] `CODE_GENDER`: decide how to handle the `'XNA'` category (drop rows, recode, or keep as its own level)
- [ ] Scan other numeric columns for similar sentinel/placeholder values (e.g. round numbers far outside the rest of the distribution)
- [ ] Drop or isolate the `credit_bucket` column added to `df` during bucketing — it's an EDA artifact, not a feature

## 3. Missingness — turn counts into decisions

- [ ] Convert missing value counts to percentages (currently raw counts only)
- [ ] Set explicit threshold(s) for drop vs. impute vs. flag-and-impute
- [ ] Apply the threshold across the housing/building block (`COMMONAREA_*`, `LANDAREA_*`, `LIVINGAREA_*`, etc. — all ~50–70% missing)
- [ ] Check whether missingness in `EXT_SOURCE_1`, `EXT_SOURCE_2`, `EXT_SOURCE_3` correlates with `TARGET` (MAR vs MNAR) before deciding fill strategy
- [ ] Check whether missingness in `OWN_CAR_AGE`, `OCCUPATION_TYPE`, `NAME_TYPE_SUITE` is informative (e.g. no car vs. car age missing)
- [ ] Decide which columns get a missing-indicator flag alongside imputation vs. silent fill

## 4. Column scoping

- [ ] Confirm `SK_ID_CURR` is excluded from the feature set (identifier only)
- [ ] Finalize a keep/drop list for the high-missing housing/building columns as a group, not column-by-column
- [ ] Decide treatment of the `FLAG_DOCUMENT_*` group (keep all 20, or collapse to a count/aggregate feature given most are near-constant and highly skewed)
- [ ] Decide treatment of high-cardinality categoricals (`ORGANIZATION_TYPE` at 58 levels) — grouping or encoding plan before it hits a pipeline

## 5. Categorical bivariate analysis (currently missing)

- [ ] Default rate by `NAME_EDUCATION_TYPE`
- [ ] Default rate by `OCCUPATION_TYPE`
- [ ] Default rate by `NAME_INCOME_TYPE`
- [ ] Default rate by `ORGANIZATION_TYPE` (or grouped version)
- [ ] Default rate by `NAME_HOUSING_TYPE` / `NAME_FAMILY_STATUS`

## 6. Leakage-safe setup

- [ ] Perform the train/validation split (stratified on `TARGET` given the 92/8 imbalance) — `train_test_split` is already imported but unused in the notebook body
- [ ] Confirm this split happens **before** any imputer or encoder is fit
- [ ] Confirm `fit_transform` will only ever run on train, `transform` on validation/test

## 7. Final pass

- [ ] Re-run the notebook top to bottom to confirm it executes cleanly end to end
- [ ] Confirm every subsection above has its Decision cell before calling EDA closed
