from . import P

PRIMER = r"""
**Read with:** McKinney ch 11 ("Shifting", "Moving window functions") and ch 10 (group-wise operations).

## shift / diff / pct_change: compare a row with its neighbour

```
 month  balance   shift(1)   diff()    pct_change()
 Jan    300,000   NaN        NaN       NaN
 Feb    299,000   300,000    -1,000    -0.33%
 Mar    297,500   299,000    -1,500    -0.50%
```
**Sort first.** shift works on row order, not dates.

## The groupby version: never leak across loans

```
 loan  month  dpd   dpd.shift(1)           groupby('loan')['dpd'].shift(1)
 A     Nov    0     NaN                    NaN
 A     Dec    30    0                      0
 B     Nov    60    30   <- WRONG, that's  NaN   <- right
 B     Dec    90    60      loan A's Dec   60
```

## Cumulative and rolling

| Write | Gives |
|---|---|
| `s.cumsum()`, `s.cummax()` | running total / running max |
| `df.groupby('k')['x'].cummax()` | running max within each group (e.g. "ever 90+ so far") |
| `s.rolling(3).mean()` | 3-period moving average (first 2 are NaN) |
| `df.groupby('k')['flag'].max()` | "ever" flag per group |

## Ever-90 in one line (you'll use it everywhere)
```python
ever90 = snap.groupby('loan_id')['days_past_due'].max() >= 90
```
"""

CONCEPT = dict(id="11_shift_cumulative", title="11 - shift, diff, cumulative and rolling", primer=PRIMER, problems=[
    P(1, """
For `loan_id` 1664, the month-to-month change in `closing_balance` (sorted by `snapshot_date`, `diff`).
What was the **largest single monthly reduction**, as a positive number rounded to 2 dp?
""", """
b = snap[snap['loan_id'] == 1664].sort_values('snapshot_date')['closing_balance']
result = round(-b.diff().min(), 2)
""", ["loan_monthly_snapshot"]),

    P(1, """
Cumulative number of loans originated, by year. Return `year`, `cum_loans`; sorted by `year`.
""", """
result = loan['origination_date'].dt.year.value_counts().sort_index().cumsum().rename_axis('year')
""", ["loan"]),

    P(2, """
Year-on-year growth in the number of loans originated, as a percentage rounded to 1 dp (`pct_change`).
Return `year`, `growth_pct`; sorted by `year` (the first year is missing).
""", """
n = loan['origination_date'].dt.year.value_counts().sort_index()
result = (n.pct_change() * 100).round(1).rename_axis('year')
""", ["loan"]),

    P(2, """
New loans per month in 2025 and their **3-month rolling average** (rounded to 1 dp; the first two months are missing).
Month as `'2025-01'` etc. Return `month`, `loans`, `rolling_3m`; sorted by `month`.
""", """
l = loan[loan['origination_date'].dt.year == 2025]
n = l['origination_date'].dt.to_period('M').astype(str).value_counts().sort_index()
result = pd.DataFrame({'loans': n, 'rolling_3m': n.rolling(3).mean().round(1)}).rename_axis('month')
""", ["loan"]),

    P(2, """
New arrears: count the loan-months in **2025** where `days_past_due` was 0 the month before and above 0 this month.
Use a **grouped** `shift` so one loan never borrows another loan's history.
""", """
s = snap.sort_values(['loan_id', 'snapshot_date'])
prev = s.groupby('loan_id')['days_past_due'].shift(1)
m = (s['snapshot_date'].dt.year == 2025) & (prev == 0) & (s['days_past_due'] > 0)
result = int(m.sum())
""", ["loan_monthly_snapshot"]),

    P(2, """
Roll forward: how many loans were 30-59 days past due at 2025-11-30 **and** 60-89 days past due at 2025-12-31?
""", """
nov = snap.loc[snap['snapshot_date'] == '2025-11-30', ['loan_id', 'days_past_due']]
dec = snap.loc[snap['snapshot_date'] == '2025-12-31', ['loan_id', 'days_past_due']]
m = nov.merge(dec, on='loan_id', suffixes=('_nov', '_dec'))
result = int((m['days_past_due_nov'].between(30, 59) & m['days_past_due_dec'].between(60, 89)).sum())
""", ["loan_monthly_snapshot"]),

    P(3, """
Ever-90 by vintage: flag each loan that **ever** reached 90+ days past due, then per origination year return `year`,
`loans`, `ever90`, `ever90_pct` (2 dp); sorted by `year`.
""", """
ever = (snap.groupby('loan_id')['days_past_due'].max() >= 90).rename('ever90')
l = loan[['loan_id', 'origination_date']].merge(ever, left_on='loan_id', right_index=True, how='left')
l['ever90'] = l['ever90'].fillna(False).astype(int)
result = l.groupby(l['origination_date'].dt.year.rename('year')).agg(loans=('ever90', 'size'), ever90=('ever90', 'sum'))
result['ever90_pct'] = (100 * result['ever90'] / result['loans']).round(2)
""", ["loan_monthly_snapshot", "loan"]),

    P(3, """
For loans that ever reached 30+ days past due, the `months_on_book` at which they **first** did. Return the average,
rounded to 1 dp.
""", """
s = snap[snap['days_past_due'] >= 30]
result = round(s.groupby('loan_id')['months_on_book'].min().mean(), 1)
""", ["loan_monthly_snapshot"], hint="The first month at 30+ is just the minimum MOB among that loan's 30+ rows."),
])
