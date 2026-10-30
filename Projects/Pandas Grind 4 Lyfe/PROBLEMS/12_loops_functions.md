# 12 - Loops over dicts, functions, building tables

`answers/12_loops_functions/qNN.py` &nbsp;|&nbsp; check with: `grade 12` or `grade 12 q03`

Levels: ★ warm-up &nbsp; ★★ core &nbsp; ★★★ challenge. Put your answer in `result`. Return columns **in the order shown** (a meaningful index counts as the leading columns); column names don't matter. Rows only need to be sorted when the question says so. Numbers match within a small tolerance.

**Read with:** McKinney ch 3 ("Functions", lambdas) and ch 10 (apply). This set is the "dictionary loop" from
notebook 03, over and over, until it's automatic.

## The pattern

```python
things = {                                # 1. name -> whatever varies (a mask, a model, a column ...)
    'Fixed':    loan['rate_type'] == 'Fixed',
    'Variable': loan['rate_type'] == 'Variable',
}
rows = {}
for name, mask in things.items():         # 2. same calculation for each
    sub = loan[mask]
    rows[name] = {'loans': len(sub), 'avg': sub['original_amount'].mean()}
table = pd.DataFrame(rows).T              # 3. one table at the end (names become rows)
```

```
 things (dict)          loop body               rows (dict of dicts)          table
 'Fixed'    -> mask  -> {'loans': .., 'avg': ..}   'Fixed':    {...}      ->     loans  avg
 'Variable' -> mask  -> {'loans': .., 'avg': ..}   'Variable': {...}             Fixed     ..   ..
                                                                                 Variable  ..   ..
```

## Functions: write once, call many times

```python
def summarise(df, by, col='original_amount'):     # col has a default
    return df.groupby(by)[col].agg(n='size', mean='mean')
```

## Vectorise before you loop over rows
A loop over **groups or models** (a handful of items) is fine. A loop over **rows** (60,000+) is slow and
rarely needed: write the formula on whole columns instead. `df.apply(f, axis=1)` is still a row loop.

---

## Problems

### Q01 &nbsp; ★ &nbsp; (warm-up)

Loop over the four channels and compute the percentage of each channel's loans that are `'Closed'`, storing results
in a dict. Return `channel`, `pct_closed` (2 dp); sorted by `channel`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **4 row(s)** &nbsp;|&nbsp; Sort the output as described. &nbsp;|&nbsp; tables: `loan`

### Q02 &nbsp; ★★ &nbsp; (core)

Segments as a dict of masks:

```python
segments = {
    'All':        all loans,
    'FHB':        first_home_buyer_flag is True,
    'Fixed':      rate_type == 'Fixed',
    'High LVR':   lvr_at_origination_pct > 80,
}
```
For each, `loans` and `avg_amount` (mean `original_amount`, 0 dp). Return `segment`, `loans`, `avg_amount`; sorted by `segment`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **4 row(s)** &nbsp;|&nbsp; Sort the output as described. &nbsp;|&nbsp; tables: `loan`

### Q03 &nbsp; ★★ &nbsp; (core)

Build a **list of dicts** in a loop over origination years 2019 to 2025 (one dict per year), then make a DataFrame.
Each row: `year`, `loans`, `avg_lvr` (2 dp), `pct_fixed` (2 dp). Sorted by `year`.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **7 row(s)** &nbsp;|&nbsp; Sort the output as described. &nbsp;|&nbsp; tables: `loan`

### Q04 &nbsp; ★★ &nbsp; (core)

Vectorised maths, no row loop: the P&I monthly repayment for each loan is
`P * r / (1 - (1 + r) ** -n)` with `P = original_amount`, `r = interest_rate_at_origination_pct / 1200`,
`n = term_months`. Return the **total** of these repayments for loans originated in 2025, rounded to 0 dp.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter. &nbsp;|&nbsp; tables: `loan`

### Q05 &nbsp; ★★ &nbsp; (core)

Write `summarise(df, by, col='original_amount')` returning, per group of `by`, `n` (rows) and `mean` (mean of `col`,
rounded to 0 dp). Call it with `by='purpose'`, leaving `col` at its default. Return `purpose`, `n`, `mean`; sorted by `purpose`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **6 row(s)** &nbsp;|&nbsp; Sort the output as described. &nbsp;|&nbsp; tables: `loan`

### Q06 &nbsp; ★★★ &nbsp; (challenge)

Compare "models" the notebook-03 way. Population: loans with an application, the primary applicant's bureau score
(thin files dropped) and the application's `assess` row. Outcome `bad` = the loan ever reached 90+ days past due.
Three single-variable "models", each a risk score where **higher = riskier**:

```python
models = {'bureau_score': -df['bureau_score'], 'nsr': -df['nsr'], 'dti_ratio': df['dti_ratio']}
```
Loop over the dict and compute each Gini (`2 * roc_auc_score(bad, score) - 1`). Return `model`, `gini` (4 dp);
sorted by `gini` (highest first).

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **3 row(s)** &nbsp;|&nbsp; Sort the output as described. &nbsp;|&nbsp; tables: `snap`, `applicant`, `bureau`, `loan`, `assess`

<details><summary>hint</summary>

`roc_auc_score(actuals, scores)`: actuals first. A score where higher = safer must be negated.

</details>

### Q07 &nbsp; ★★★ &nbsp; (challenge)

A comprehension instead of a loop: for live loans at 2025-12-31, the percentage with `days_past_due` at or above
each threshold in `[1, 30, 60, 90]`, rounded to 3 dp. Return `threshold`, `pct`; sorted by `threshold`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **4 row(s)** &nbsp;|&nbsp; Sort the output as described. &nbsp;|&nbsp; tables: `snap`

### Q08 &nbsp; ★★★ &nbsp; (challenge)

Nested loop to a wide table: approval rate (% of decided applications approved, 2 dp) for each `channel` (rows) and
application year 2023, 2024, 2025 (columns). Build it with two loops into a dict of dicts. Return `channel`, `2023`,
`2024`, `2025`; sorted by `channel`.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **4 row(s)** &nbsp;|&nbsp; Sort the output as described. &nbsp;|&nbsp; tables: `app`
