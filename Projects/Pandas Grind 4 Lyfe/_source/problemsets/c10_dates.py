from . import P

PRIMER = r"""
**Read with:** McKinney ch 11 (dates, periods, resampling).

## The `.dt` accessor: everything about a date column

| Write | 2025-08-14 gives |
|---|---|
| `s.dt.year`, `s.dt.month`, `s.dt.day` | 2025, 8, 14 |
| `s.dt.quarter` | 3 |
| `s.dt.to_period('M')` | `2025-08` (a Period; `.astype(str)` -> `'2025-08'`) |
| `s.dt.to_period('Q')` | `2025Q3` |
| `s.dt.strftime('%Y-%m')` | `'2025-08'` (a string) |
| `s.dt.days_in_month` | 31 |

## Differences

```
 (d2 - d1)              -> Timedelta     ('45 days')
 (d2 - d1).dt.days      -> 45            (an int you can average)
 whole months:  (d2.dt.year - d1.dt.year) * 12 + (d2.dt.month - d1.dt.month)
```

## Australian financial year (ends 30 June)

```
 date        month >= 7 ?   FY
 2024-08-14  yes            2025   (Jul 2024 - Jun 2025)
 2025-03-02  no             2025
 FY = year + (month >= 7)
```

## resample: a regular time grid

```python
s = df.set_index('start_date').resample('MS').size()   # one row per month, empty months = 0
```
'MS' = month start, 'ME' = month end (older pandas: 'M'), 'QE' = quarter end.

## Month-end snapshots
`snap` has one row per loan per month-end. "As at a date" means `snap[snap['snapshot_date'] == '2025-12-31']`.
A string compares fine against a datetime column.
"""

CONCEPT = dict(id="10_dates", title="10 - Dates and time series", primer=PRIMER, problems=[
    P(1, """
Loans originated per calendar year. Return `year`, `loans`; sorted by `year`.
""", """
result = loan['origination_date'].dt.year.value_counts().sort_index().rename_axis('year')
""", ["loan"]),

    P(1, """
Loans originated per month of 2025, with the month as a string like `'2025-03'`. Return `month`, `loans`; sorted by `month`.
""", """
l = loan[loan['origination_date'].dt.year == 2025]
result = l['origination_date'].dt.to_period('M').astype(str).value_counts().sort_index().rename_axis('month')
""", ["loan"]),

    P(1, """
Median number of days from `application_date` to `decision_date` for **approved** applications. Return a number.
""", """
a = app[app['decision'] == 'Approved']
result = float((a['decision_date'] - a['application_date']).dt.days.median())
""", ["loan_application"]),

    P(2, """
For live loans at 2025-12-31, the remaining term in **whole months** from 2025-12 to the `maturity_date` month
(join `maturity_date` from `loan`). Return the average, rounded to 1 dp.
""", """
live = snap[(snap['snapshot_date'] == '2025-12-31') & (snap['loan_status'] != 'Closed')]
m = live[['loan_id']].merge(loan[['loan_id', 'maturity_date']], on='loan_id')
months = (m['maturity_date'].dt.year - 2025) * 12 + (m['maturity_date'].dt.month - 12)
result = round(months.mean(), 1)
""", ["loan_monthly_snapshot", "loan"]),

    P(2, """
Loans originated per **Australian financial year** (FY ends 30 June; FY2025 = Jul 2024 - Jun 2025).
Return `fy`, `loans`; sorted by `fy`.
""", """
d = loan['origination_date']
fy = d.dt.year + (d.dt.month >= 7).astype(int)
result = fy.value_counts().sort_index().rename_axis('fy')
""", ["loan"]),

    P(2, """
New hardship arrangements per month in **2020** (`start_date`), every month of 2020 present (0 if none), month as a
string like `'2020-04'`. Return `month`, `arrangements`; sorted by `month`.
""", """
h = hardship_arrangement[hardship_arrangement['start_date'].dt.year == 2020]
n = h.set_index('start_date').resample('MS').size()
n = n.reindex(pd.date_range('2020-01-01', '2020-12-01', freq='MS'), fill_value=0)
result = pd.Series(n.to_numpy(), index=n.index.strftime('%Y-%m'), name='arrangements').rename_axis('month')
""", ["hardship_arrangement"], hint="`resample('MS').size()` only spans the months that have data; `reindex` to a full `pd.date_range` fills the gaps."),

    P(2, """
Total book balance (`closing_balance` of all rows, $ millions, 2 dp) at each **2025 quarter-end** snapshot
(31 Mar, 30 Jun, 30 Sep, 31 Dec). Return `quarter_end` (as `'2025-03-31'` etc.), `balance_m`; sorted by `quarter_end`.
""", """
s = snap[snap['snapshot_date'].dt.year == 2025]
s = s[s['snapshot_date'].dt.is_quarter_end]
result = (s.groupby(s['snapshot_date'].dt.strftime('%Y-%m-%d').rename('quarter_end'))['closing_balance'].sum() / 1e6).round(2)
""", ["loan_monthly_snapshot"]),

    P(3, """
Snapshot gaps: a loan should have one row for every month from MOB 0 to its last MOB. Count the loans whose number of
snapshot rows is **not** equal to `max(months_on_book) + 1`.
""", """
g = snap.groupby('loan_id')['months_on_book'].agg(['size', 'max'])
result = int((g['size'] != g['max'] + 1).sum())
""", ["loan_monthly_snapshot"]),

    P(3, """
Payment-shock watch: **active** fixed-rate loans whose `fixed_rate_expiry_date` falls in 2026, by quarter
(string like `'2026Q1'`). Return `quarter`, `loans`; sorted by `quarter`.
""", """
f = loan[(loan['loan_status'] == 'Active') & (loan['fixed_rate_expiry_date'].dt.year == 2026)]
result = f['fixed_rate_expiry_date'].dt.to_period('Q').astype(str).value_counts().sort_index().rename_axis('quarter')
""", ["loan"]),
])
