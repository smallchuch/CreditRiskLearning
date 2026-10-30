from . import P

PRIMER = r"""
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
"""

LIVE = "live = snap[(snap['snapshot_date'] == '2025-12-31') & (snap['loan_status'] != 'Closed')]\n"

EVER90_SCORED = """
ever = (snap.groupby('loan_id')['days_past_due'].max() >= 90).rename('bad').astype(int)
prim = applicant.loc[applicant['applicant_role'] == 'Primary', ['application_id', 'customer_id']]
score = prim.merge(bureau[['application_id', 'customer_id', 'bureau_score']], on=['application_id', 'customer_id'])
df = (loan[['loan_id', 'application_id']].dropna()
      .merge(score[['application_id', 'bureau_score']], on='application_id')
      .merge(assess[['application_id', 'nsr', 'dti_ratio', 'lvr_pct']], on='application_id')
      .merge(ever, left_on='loan_id', right_index=True))
df = df.dropna(subset=['bureau_score'])
"""

CONCEPT = dict(id="12_loops_functions", title="12 - Loops over dicts, functions, building tables", primer=PRIMER, problems=[
    P(1, """
Loop over the four channels and compute the percentage of each channel's loans that are `'Closed'`, storing results
in a dict. Return `channel`, `pct_closed` (2 dp); sorted by `channel`.
""", """
out = {}
for ch in sorted(loan['channel'].unique()):
    sub = loan[loan['channel'] == ch]
    out[ch] = round(100 * (sub['loan_status'] == 'Closed').mean(), 2)
result = pd.Series(out, name='pct_closed').rename_axis('channel')
""", ["loan"]),

    P(2, """
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
""", """
segments = {
    'All': pd.Series(True, index=loan.index),
    'FHB': loan['first_home_buyer_flag'],
    'Fixed': loan['rate_type'] == 'Fixed',
    'High LVR': loan['lvr_at_origination_pct'] > 80,
}
rows = {}
for name, mask in segments.items():
    sub = loan[mask]
    rows[name] = {'loans': len(sub), 'avg_amount': round(sub['original_amount'].mean(), 0)}
result = pd.DataFrame(rows).T.rename_axis('segment').sort_index()
""", ["loan"]),

    P(2, """
Build a **list of dicts** in a loop over origination years 2019 to 2025 (one dict per year), then make a DataFrame.
Each row: `year`, `loans`, `avg_lvr` (2 dp), `pct_fixed` (2 dp). Sorted by `year`.
""", """
rows = []
for y in range(2019, 2026):
    sub = loan[loan['origination_date'].dt.year == y]
    rows.append({'year': y, 'loans': len(sub),
                 'avg_lvr': round(sub['lvr_at_origination_pct'].mean(), 2),
                 'pct_fixed': round(100 * (sub['rate_type'] == 'Fixed').mean(), 2)})
result = pd.DataFrame(rows)
""", ["loan"]),

    P(2, """
Vectorised maths, no row loop: the P&I monthly repayment for each loan is
`P * r / (1 - (1 + r) ** -n)` with `P = original_amount`, `r = interest_rate_at_origination_pct / 1200`,
`n = term_months`. Return the **total** of these repayments for loans originated in 2025, rounded to 0 dp.
""", """
l = loan[loan['origination_date'].dt.year == 2025]
r = l['interest_rate_at_origination_pct'] / 1200
n = l['term_months']
pmt = l['original_amount'] * r / (1 - (1 + r) ** -n)
result = round(pmt.sum(), 0)
""", ["loan"], tol=1.01),

    P(2, """
Write `summarise(df, by, col='original_amount')` returning, per group of `by`, `n` (rows) and `mean` (mean of `col`,
rounded to 0 dp). Call it with `by='purpose'`, leaving `col` at its default. Return `purpose`, `n`, `mean`; sorted by `purpose`.
""", """
def summarise(df, by, col='original_amount'):
    out = df.groupby(by)[col].agg(n='size', mean='mean')
    out['mean'] = out['mean'].round(0)
    return out

result = summarise(loan, 'purpose')
""", ["loan"]),

    P(3, """
Compare "models" the notebook-03 way. Population: loans with an application, the primary applicant's bureau score
(thin files dropped) and the application's `assess` row. Outcome `bad` = the loan ever reached 90+ days past due.
Three single-variable "models", each a risk score where **higher = riskier**:

```python
models = {'bureau_score': -df['bureau_score'], 'nsr': -df['nsr'], 'dti_ratio': df['dti_ratio']}
```
Loop over the dict and compute each Gini (`2 * roc_auc_score(bad, score) - 1`). Return `model`, `gini` (4 dp);
sorted by `gini` (highest first).
""", EVER90_SCORED + """
from sklearn.metrics import roc_auc_score
models = {'bureau_score': -df['bureau_score'], 'nsr': -df['nsr'], 'dti_ratio': df['dti_ratio']}
rows = {}
for name, score in models.items():
    rows[name] = round(2 * roc_auc_score(df['bad'], score) - 1, 4)
result = pd.Series(rows, name='gini').rename_axis('model').sort_values(ascending=False)
""", ["loan_monthly_snapshot", "application_applicant", "credit_bureau_report", "loan", "application_assessment"],
      tol=0.00011, hint="`roc_auc_score(actuals, scores)`: actuals first. A score where higher = safer must be negated."),

    P(3, """
A comprehension instead of a loop: for live loans at 2025-12-31, the percentage with `days_past_due` at or above
each threshold in `[1, 30, 60, 90]`, rounded to 3 dp. Return `threshold`, `pct`; sorted by `threshold`.
""", LIVE + """
dpd = live['days_past_due']
result = pd.DataFrame([{'threshold': t, 'pct': round(100 * (dpd >= t).mean(), 3)} for t in [1, 30, 60, 90]])
""", ["loan_monthly_snapshot"], tol=0.0011),

    P(3, """
Nested loop to a wide table: approval rate (% of decided applications approved, 2 dp) for each `channel` (rows) and
application year 2023, 2024, 2025 (columns). Build it with two loops into a dict of dicts. Return `channel`, `2023`,
`2024`, `2025`; sorted by `channel`.
""", """
d = app.dropna(subset=['decision'])
yr = d['application_date'].dt.year
table = {}
for y in [2023, 2024, 2025]:
    col = {}
    for ch in sorted(d['channel'].unique()):
        sub = d[(yr == y) & (d['channel'] == ch)]
        col[ch] = round(100 * (sub['decision'] == 'Approved').mean(), 2)
    table[y] = col
result = pd.DataFrame(table).rename_axis('channel').sort_index()
""", ["loan_application"]),
])
