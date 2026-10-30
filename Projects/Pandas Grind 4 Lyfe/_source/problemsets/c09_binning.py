from . import P

PRIMER = r"""
**Read with:** McKinney ch 7 ("Discretization and binning") and ch 5 ("Ranking").

## cut = your edges, qcut = equal counts

```
 pd.cut(lvr, bins=[0, 60, 70, 80, 90, 95, np.inf], right=False)     edges you choose
     [0, 60)  [60, 70)  [70, 80) ...                                   groups of any size

 pd.qcut(amount, q=10, labels=False)                                  edges chosen from the data
     decile 0 .. 9, each about 10% of rows                             groups of equal size
```
- `right=False` makes bins **left-closed**: `[60, 70)` includes 60, excludes 70 (matches `ref_lvr_band`).
- `labels=[...]` names the bins; `labels=False` gives 0, 1, 2 ...
- A `cut` result is a **Categorical**. When you group by it, pass `observed=True` (keep only bins with rows) or
  `observed=False` (keep empty bins too). Say which one you mean; the default changed between pandas versions.

## Ties break qcut

```
 dpd values:   0 0 0 0 0 0 0 0 3 95       qcut(q=5) -> ValueError: Bin edges must be unique
 rank(method='first'):  1 2 3 4 5 6 7 8 9 10   -> qcut on the rank always works
```
`rank(method='first')` gives tied values consecutive ranks (by position), so equal-count groups exist even when
most values are identical. That is the trick from notebook 03 (tree PDs tie).

| rank method | ties 50, 50, 70 get |
|---|---|
| `'average'` (default) | 1.5, 1.5, 3 |
| `'min'` | 1, 1, 3 |
| `'dense'` | 1, 1, 2 |
| `'first'` | 1, 2, 3 |

`s.rank(pct=True)` gives the percentile rank (0 to 1).
"""

LIVE = "live = snap[(snap['snapshot_date'] == '2025-12-31') & (snap['loan_status'] != 'Closed')]\n"

CONCEPT = dict(id="09_binning", title="09 - Binning and ranking: cut, qcut, rank", primer=PRIMER, problems=[
    P(1, """
Band every loan's `lvr_at_origination_pct` with `pd.cut` using the `ref_lvr_band` edges 0, 60, 70, 80, 90, 95, inf
(left-closed) and labels `'<= 60%'`, `'60-70%'`, `'70-80%'`, `'80-90%'`, `'90-95%'`, `'> 95%'`.
Return `band`, `loans` in band order (lowest first).
""", """
labels = ['<= 60%', '60-70%', '70-80%', '80-90%', '90-95%', '> 95%']
band = pd.cut(loan['lvr_at_origination_pct'], bins=[0, 60, 70, 80, 90, 95, np.inf], right=False, labels=labels)
result = band.value_counts(sort=False).rename_axis('band')
""", ["loan"], order=True, hint="`value_counts(sort=False)` keeps the category order instead of sorting by count."),

    P(1, """
Deciles of `original_amount` with `pd.qcut(q=10, labels=False)`, numbered **1 to 10**. Return `decile`, `min_amount`,
`max_amount`; sorted by `decile`.
""", """
d = pd.qcut(loan['original_amount'], q=10, labels=False, duplicates='drop') + 1
result = loan.groupby(d.rename('decile'))['original_amount'].agg(['min', 'max'])
""", ["loan"]),

    P(2, """
Bureau-score deciles that never fail on ties: rank the non-missing `bureau_score` values with `method='first'`, then
`qcut` the rank into 10 groups numbered 1 (lowest scores) to 10. Return `decile`, `n`, `avg_score` (1 dp); sorted by `decile`.
""", """
s = bureau['bureau_score'].dropna()
d = pd.qcut(s.rank(method='first'), q=10, labels=False) + 1
result = s.groupby(d.rename('decile')).agg(n='size', avg_score='mean')
result['avg_score'] = result['avg_score'].round(1)
""", ["credit_bureau_report"]),

    P(2, """
For each channel, the loan with the **second-largest** `original_amount` (ties: smaller `loan_id` ranks higher).
Return `channel`, `loan_id`, `original_amount`; sorted by `channel`.
""", """
l = loan.sort_values(['original_amount', 'loan_id'], ascending=[False, True]).copy()
l['rk'] = l.groupby('channel').cumcount() + 1
result = l.loc[l['rk'] == 2, ['channel', 'loan_id', 'original_amount']].sort_values('channel')
""", ["loan"], hint="Sort so the order is exactly what you want, then `groupby(...).cumcount()` numbers rows 0, 1, 2 within each group."),

    P(2, """
Live loans at 2025-12-31 split into 5 equal-count groups on `days_past_due`. Plain `qcut` fails (most values are 0),
so `qcut` the `rank(method='first')` instead. Groups numbered 1 to 5. Return `group`, `n`, `max_dpd`; sorted by `group`.
""", LIVE + """
g = pd.qcut(live['days_past_due'].rank(method='first'), q=5, labels=False) + 1
result = live.groupby(g.rename('group'))['days_past_due'].agg(n='size', max_dpd='max')
""", ["loan_monthly_snapshot"]),

    P(2, """
Band applications by `nsr` (from `assess`) into `'< 1.0'`, `'1.0-1.25'`, `'1.25-1.5'`, `'1.5-2.0'`, `'2.0+'`
(left-closed), join the decision from `app`, and report the decline rate among decided applications.
Return `nsr_band`, `apps`, `decline_pct` (2 dp) in band order. Leave out empty bands.
""", """
m = assess[['application_id', 'nsr']].merge(app[['application_id', 'decision']], on='application_id')
m = m.dropna(subset=['decision'])
labels = ['< 1.0', '1.0-1.25', '1.25-1.5', '1.5-2.0', '2.0+']
m['nsr_band'] = pd.cut(m['nsr'], bins=[-np.inf, 1.0, 1.25, 1.5, 2.0, np.inf], right=False, labels=labels)
result = m.groupby('nsr_band', observed=True).agg(apps=('decision', 'size'),
                                                  decline_pct=('decision', lambda d: round(100 * (d == 'Declined').mean(), 2)))
""", ["application_assessment", "loan_application"], order=True),

    P(3, """
Percentile rank of each live loan's `closing_balance` at 2025-12-31 (`rank(pct=True)`). How many loans sit in the
top 1% (percentile rank of 0.99 or more)?
""", LIVE + """
result = int((live['closing_balance'].rank(pct=True) >= 0.99).sum())
""", ["loan_monthly_snapshot"]),

    P(2, """
Histogram as a table: live loans at 2025-12-31 binned by `interest_rate_pct` into 0.5-point bins from 4.0 to 9.0
(left-closed; anything outside is dropped). Return `bin_start`, `loans` for bins with loans, where `bin_start` is the
lower edge as a number (e.g. 4.0); sorted by `bin_start`.
""", LIVE + """
edges = np.arange(4.0, 9.01, 0.5)
b = pd.cut(live['interest_rate_pct'], bins=edges, right=False, labels=edges[:-1])
result = b.value_counts(sort=False)
result = result[result > 0].rename_axis('bin_start')
result.index = result.index.astype(float)
""", ["loan_monthly_snapshot"]),
])
