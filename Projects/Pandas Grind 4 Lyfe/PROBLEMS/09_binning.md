# 09 - Binning and ranking: cut, qcut, rank

`answers/09_binning/qNN.py` &nbsp;|&nbsp; check with: `grade 09` or `grade 09 q03`

Levels: ★ warm-up &nbsp; ★★ core &nbsp; ★★★ challenge. Put your answer in `result`. Return columns **in the order shown** (a meaningful index counts as the leading columns); column names don't matter. Rows only need to be sorted when the question says so. Numbers match within a small tolerance.

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

---

## Problems

### Q01 &nbsp; ★ &nbsp; (warm-up)

Band every loan's `lvr_at_origination_pct` with `pd.cut` using the `ref_lvr_band` edges 0, 60, 70, 80, 90, 95, inf
(left-closed) and labels `'<= 60%'`, `'60-70%'`, `'70-80%'`, `'80-90%'`, `'90-95%'`, `'> 95%'`.
Return `band`, `loans` in band order (lowest first).

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **6 row(s)** &nbsp;|&nbsp; Sort the output as described. &nbsp;|&nbsp; tables: `loan`

<details><summary>hint</summary>

`value_counts(sort=False)` keeps the category order instead of sorting by count.

</details>

### Q02 &nbsp; ★ &nbsp; (warm-up)

Deciles of `original_amount` with `pd.qcut(q=10, labels=False)`, numbered **1 to 10**. Return `decile`, `min_amount`,
`max_amount`; sorted by `decile`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **10 row(s)** &nbsp;|&nbsp; Sort the output as described. &nbsp;|&nbsp; tables: `loan`

### Q03 &nbsp; ★★ &nbsp; (core)

Bureau-score deciles that never fail on ties: rank the non-missing `bureau_score` values with `method='first'`, then
`qcut` the rank into 10 groups numbered 1 (lowest scores) to 10. Return `decile`, `n`, `avg_score` (1 dp); sorted by `decile`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **10 row(s)** &nbsp;|&nbsp; Sort the output as described. &nbsp;|&nbsp; tables: `bureau`

### Q04 &nbsp; ★★ &nbsp; (core)

For each channel, the loan with the **second-largest** `original_amount` (ties: smaller `loan_id` ranks higher).
Return `channel`, `loan_id`, `original_amount`; sorted by `channel`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **4 row(s)** &nbsp;|&nbsp; Sort the output as described. &nbsp;|&nbsp; tables: `loan`

<details><summary>hint</summary>

Sort so the order is exactly what you want, then `groupby(...).cumcount()` numbers rows 0, 1, 2 within each group.

</details>

### Q05 &nbsp; ★★ &nbsp; (core)

Live loans at 2025-12-31 split into 5 equal-count groups on `days_past_due`. Plain `qcut` fails (most values are 0),
so `qcut` the `rank(method='first')` instead. Groups numbered 1 to 5. Return `group`, `n`, `max_dpd`; sorted by `group`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **5 row(s)** &nbsp;|&nbsp; Sort the output as described. &nbsp;|&nbsp; tables: `snap`

### Q06 &nbsp; ★★ &nbsp; (core)

Band applications by `nsr` (from `assess`) into `'< 1.0'`, `'1.0-1.25'`, `'1.25-1.5'`, `'1.5-2.0'`, `'2.0+'`
(left-closed), join the decision from `app`, and report the decline rate among decided applications.
Return `nsr_band`, `apps`, `decline_pct` (2 dp) in band order. Leave out empty bands.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **5 row(s)** &nbsp;|&nbsp; Sort the output as described. &nbsp;|&nbsp; tables: `assess`, `app`

### Q07 &nbsp; ★★★ &nbsp; (challenge)

Percentile rank of each live loan's `closing_balance` at 2025-12-31 (`rank(pct=True)`). How many loans sit in the
top 1% (percentile rank of 0.99 or more)?

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter. &nbsp;|&nbsp; tables: `snap`

### Q08 &nbsp; ★★ &nbsp; (core)

Histogram as a table: live loans at 2025-12-31 binned by `interest_rate_pct` into 0.5-point bins from 4.0 to 9.0
(left-closed; anything outside is dropped). Return `bin_start`, `loans` for bins with loans, where `bin_start` is the
lower edge as a number (e.g. 4.0); sorted by `bin_start`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **7 row(s)** &nbsp;|&nbsp; Sort the output as described. &nbsp;|&nbsp; tables: `snap`
