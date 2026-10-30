from . import P

PRIMER = r"""
**Read with:** McKinney ch 4 (NumPy basics: arrays, boolean indexing, vectorised maths).

## A Series is an array with labels. `.to_numpy()` (or `.values`) drops the labels.

```
 Series                         numpy array
 index  value                   [0.21, 0.04, 0.09]
 17     0.21                     position 0, 1, 2 - no labels
 42     0.04          .to_numpy()
 58     0.09          ------->
```
Arrays line up **by position**, Series line up **by label**. Mixing them is how the KS line in
notebook 03 needed `y_test.values == 1`.

## Boolean masks: the most useful idea in this whole set

```
 lvr          lvr > 80        lvr[lvr > 80]
 [65, 92, 81]  [F,  T,  T]     [92, 81]
                 .sum() = 2    (True counts as 1)
                 .mean() = 0.67 (share of Trues)
```
Combine masks with `&` (and), `|` (or), `~` (not), and **always bracket each condition**:
`(a > 1) & (b < 5)`.

## Vectorised choices

| Tool | Use |
|---|---|
| `np.where(cond, a, b)` | two outcomes |
| `np.select([c1, c2, c3], [v1, v2, v3], default)` | several ordered outcomes (first True wins) |
| `np.sign(x)` | -1 / 0 / +1 |
| `np.diff(x)` | step from each element to the next |
| `np.percentile(x, [10, 50, 90])` | percentiles |
| `np.average(x, weights=w)` | weighted average |

Missing values (`NaN`) poison sums and means in NumPy (`np.mean([1, np.nan]) = nan`); pandas skips them by default.
"""

CONCEPT = dict(id="02_numpy", title="02 - NumPy: arrays, masks, vectorised maths", primer=PRIMER, problems=[
    P(1, """
Mean `original_amount` across all loans, computed with **NumPy** on the underlying array (`.to_numpy()`), rounded to 0 dp.
""", """
result = round(np.mean(loan['original_amount'].to_numpy()), 0)
""", ["loan"]),

    P(1, """
How many loans have `lvr_at_origination_pct` strictly above 80? Use a boolean mask and `.sum()`.
""", """
result = int((loan['lvr_at_origination_pct'].to_numpy() > 80).sum())
""", ["loan"]),

    P(1, """
Label each loan `'High LVR'` if `lvr_at_origination_pct` > 80, else `'Standard'` (use `np.where`).
Return `label`, `loans`; sorted by `label`.
""", """
label = np.where(loan['lvr_at_origination_pct'] > 80, 'High LVR', 'Standard')
result = pd.Series(label).value_counts().sort_index()
""", ["loan"]),

    P(2, """
The 10th, 50th and 90th percentiles of `original_amount` (`np.percentile`), as a list of three numbers
rounded to 0 dp, in that order.
""", """
result = [round(v, 0) for v in np.percentile(loan['original_amount'].to_numpy(), [10, 50, 90])]
""", ["loan"], order=True),

    P(2, """
On `bureau`, compare the average `bureau_score` of reports **with** at least one default listing
(`default_listings > 0`) against those **without**. Thin files (missing score) are excluded.
Return `group` (`'listed'` / `'clean'`) and `avg_score` rounded to 1 dp; sorted by `group`.
""", """
s = bureau['bureau_score'].to_numpy()
listed = bureau['default_listings'].to_numpy() > 0
ok = ~np.isnan(s)
result = pd.DataFrame({
    'group': ['clean', 'listed'],
    'avg_score': [round(s[ok & ~listed].mean(), 1), round(s[ok & listed].mean(), 1)],
})
""", ["credit_bureau_report"], hint="`np.isnan(arr)` marks the thin files; combine masks with `&` and `~`."),

    P(2, """
For `loan_id` 1664 (a variable-rate loan from 2019), take its `interest_rate_pct` month by month (`snap`, ordered by `snapshot_date`).
How many month-to-month steps were **rate rises**? Use `np.diff` and `np.sign`.
""", """
rates = snap.loc[snap['loan_id'] == 1664].sort_values('snapshot_date')['interest_rate_pct'].to_numpy()
result = int((np.sign(np.diff(rates)) == 1).sum())
""", ["loan_monthly_snapshot"]),

    P(2, """
Balance-weighted average `interest_rate_pct` of the **live book** at 2025-12-31 (`snapshot_date` = 2025-12-31
and `loan_status` not `'Closed'`), weights = `closing_balance`. Use `np.average`. Round to 3 dp.
""", """
live = snap[(snap['snapshot_date'] == '2025-12-31') & (snap['loan_status'] != 'Closed')]
result = round(np.average(live['interest_rate_pct'], weights=live['closing_balance']), 3)
""", ["loan_monthly_snapshot"], tol=0.0011),

    P(3, """
Put every live loan at 2025-12-31 into a tier with `np.select` on `days_past_due`:
0 = `'Current'`, 1-29 = `'Early'`, 30-89 = `'Late'`, 90+ = `'Default'`.
Return `tier`, `loans`; sorted by `tier`.
""", """
live = snap[(snap['snapshot_date'] == '2025-12-31') & (snap['loan_status'] != 'Closed')]
d = live['days_past_due']
tier = np.select([d == 0, d < 30, d < 90], ['Current', 'Early', 'Late'], default='Default')
result = pd.Series(tier).value_counts().sort_index()
""", ["loan_monthly_snapshot"], hint="`np.select` takes the first condition that is True, so order the conditions from lowest to highest."),
])
