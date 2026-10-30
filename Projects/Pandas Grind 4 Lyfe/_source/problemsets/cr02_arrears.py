from . import P

PRIMER = r"""
**Credit-risk scenario.** Arrears, roll rates, cures and a first cohort default rate. Patterns from sets 06, 07, 08, 11.

## Arrears rate: count or balance?
```
 30+ rate (count)   = loans with dpd >= 30 / live loans
 30+ rate (balance) = balance of loans with dpd >= 30 / live balance     <- what APRA-style reporting uses
```

## Roll-rate matrix (this month's bucket given last month's)

```
                 Dec: Current  1-29  30-59  60-89  90+
 Nov: Current        99.3%     0.6%  0.1%    -      -        each ROW sums to 100%
      1-29           40%       35%   25%     -      -        diagonal = stayed
      30-59          15%       10%   20%    55%     -        right of diagonal = rolled forward
      ...                                                     left = cured
```
Build it: one row per loan with `bucket_nov` and `bucket_dec` (a merge of two snapshots), then
`pd.crosstab(bucket_nov, bucket_dec, normalize='index')`.

Use **ordered** labels so rows and columns come out in bucket order, not alphabetical:
```python
order = ['Current', '1-29', '30-59', '60-89', '90+']
b = pd.Categorical(labels, categories=order, ordered=True)
```

## Cohort default rate (a 12-month PD, the simple way)
Take a cohort at a start date (e.g. performing loans at 2024-12-31), follow them for 12 months, count who hit 90+.
Denominator = cohort size at the start. That's the shape of the PD your Freddie Mac project builds.
"""

BUCKET = """
order = ['Current', '1-29', '30-59', '60-89', '90+']
def bucket(dpd):
    return pd.Categorical(pd.cut(dpd, [-1, 0, 29, 59, 89, np.inf], labels=order), categories=order, ordered=True)
"""

CONCEPT = dict(id="cr02_arrears", title="cr02 - Arrears, roll rates and cures", primer=PRIMER, problems=[
    P(1, """
The **30+ arrears rate by count** of the live book at each month-end of 2025 (live = not `'Closed'` that month),
as a percentage rounded to 3 dp. Month as `'2025-01'` etc. Return `month`, `pct_30plus`; sorted by `month`.
""", """
s = snap[(snap['snapshot_date'].dt.year == 2025) & (snap['loan_status'] != 'Closed')]
r = 100 * (s['days_past_due'] >= 30).groupby(s['snapshot_date'].dt.strftime('%Y-%m').rename('month')).mean()
result = r.round(3)
""", ["loan_monthly_snapshot"], tol=0.0011),

    P(2, """
The **90+ arrears rate by balance** of the live book at 2025-12-31, as a percentage rounded to 3 dp.
""", """
live = snap[(snap['snapshot_date'] == '2025-12-31') & (snap['loan_status'] != 'Closed')]
result = round(100 * live.loc[live['days_past_due'] >= 90, 'closing_balance'].sum() / live['closing_balance'].sum(), 3)
""", ["loan_monthly_snapshot"], tol=0.0011),

    P(2, """
Live loans and balance by arrears bucket at 2025-12-31 with buckets `'Current'` (0), `'1-29'`, `'30-59'`, `'60-89'`,
`'90+'`. Return `bucket`, `loans`, `balance_m` (2 dp) in bucket order.
""", BUCKET + """
live = snap[(snap['snapshot_date'] == '2025-12-31') & (snap['loan_status'] != 'Closed')].copy()
live['bucket'] = bucket(live['days_past_due'])
g = live.groupby('bucket', observed=False).agg(loans=('loan_id', 'size'), balance_m=('closing_balance', 'sum'))
g['balance_m'] = (g['balance_m'] / 1e6).round(2)
result = g
""", ["loan_monthly_snapshot"], order=True),

    P(3, """
Roll-rate matrix November -> December 2025 for loans that are live (not `'Closed'`) in **both** month-end snapshots.
Buckets `Current`, `1-29`, `30-59`, `60-89`, `90+`; **row percentages** rounded to 2 dp,
0 where nothing rolled. Return `from_bucket` then one column per December bucket in bucket order; rows in bucket order.
""", BUCKET + """
open_ = snap['loan_status'] != 'Closed'
nov = snap.loc[(snap['snapshot_date'] == '2025-11-30') & open_, ['loan_id', 'days_past_due']]
dec = snap.loc[(snap['snapshot_date'] == '2025-12-31') & open_, ['loan_id', 'days_past_due']]
m = nov.merge(dec, on='loan_id', suffixes=('_nov', '_dec'))
t = pd.crosstab(bucket(m['days_past_due_nov']), bucket(m['days_past_due_dec']), normalize='index', dropna=False)
t = t.reindex(index=order, columns=order, fill_value=0)
result = (100 * t).round(2).rename_axis('from_bucket')
""", ["loan_monthly_snapshot"], order=True),

    P(2, """
Cure rate: of the loans 30+ days past due at 2025-06-30, what percentage were back to 0 days past due at 2025-12-31?
Denominator = those 30+ at June that still have a December snapshot. Round to 2 dp.
""", """
jun = snap.loc[(snap['snapshot_date'] == '2025-06-30') & (snap['days_past_due'] >= 30), ['loan_id']]
dec = snap.loc[snap['snapshot_date'] == '2025-12-31', ['loan_id', 'days_past_due']]
m = jun.merge(dec, on='loan_id')
result = round(100 * (m['days_past_due'] == 0).mean(), 2)
""", ["loan_monthly_snapshot"]),

    P(2, """
Share of live loans on a hardship flag at each **quarter-end of 2020** (the COVID deferral wave), as a percentage
rounded to 2 dp. Return `quarter_end` (`'2020-03-31'` etc.), `hardship_pct`; sorted by `quarter_end`.
""", """
s = snap[(snap['snapshot_date'].dt.year == 2020) & snap['snapshot_date'].dt.is_quarter_end & (snap['loan_status'] != 'Closed')]
result = (100 * s.groupby(s['snapshot_date'].dt.strftime('%Y-%m-%d').rename('quarter_end'))['hardship_flag'].mean()).round(2)
""", ["loan_monthly_snapshot"]),

    P(3, """
A 12-month cohort default rate. Cohort = live loans at 2024-12-31 that were **current** (0 days past due) then.
Bad = reached 90+ days past due at **any** 2025 month-end. Return one row: `cohort`, `bads`, `default_rate_pct` (3 dp).
""", """
start = snap.loc[(snap['snapshot_date'] == '2024-12-31') & (snap['loan_status'] != 'Closed') & (snap['days_past_due'] == 0), 'loan_id']
y25 = snap[snap['snapshot_date'].dt.year == 2025]
bad_ids = set(y25.loc[y25['days_past_due'] >= 90, 'loan_id'])
bads = int(start.isin(bad_ids).sum())
result = pd.DataFrame({'cohort': [len(start)], 'bads': [bads], 'default_rate_pct': [round(100 * bads / len(start), 3)]})
""", ["loan_monthly_snapshot"], tol=0.0011),
])
