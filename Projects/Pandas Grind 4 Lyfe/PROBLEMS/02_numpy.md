# 02 - NumPy: arrays, masks, vectorised maths

`answers/02_numpy/qNN.py` &nbsp;|&nbsp; check with: `grade 02` or `grade 02 q03`

Levels: ★ warm-up &nbsp; ★★ core &nbsp; ★★★ challenge. Put your answer in `result`. Return columns **in the order shown** (a meaningful index counts as the leading columns); column names don't matter. Rows only need to be sorted when the question says so. Numbers match within a small tolerance.

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

---

## Problems

### Q01 &nbsp; ★ &nbsp; (warm-up)

Mean `original_amount` across all loans, computed with **NumPy** on the underlying array (`.to_numpy()`), rounded to 0 dp.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter. &nbsp;|&nbsp; tables: `loan`

### Q02 &nbsp; ★ &nbsp; (warm-up)

How many loans have `lvr_at_origination_pct` strictly above 80? Use a boolean mask and `.sum()`.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter. &nbsp;|&nbsp; tables: `loan`

### Q03 &nbsp; ★ &nbsp; (warm-up)

Label each loan `'High LVR'` if `lvr_at_origination_pct` > 80, else `'Standard'` (use `np.where`).
Return `label`, `loans`; sorted by `label`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **2 row(s)** &nbsp;|&nbsp; Sort the output as described. &nbsp;|&nbsp; tables: `loan`

### Q04 &nbsp; ★★ &nbsp; (core)

The 10th, 50th and 90th percentiles of `original_amount` (`np.percentile`), as a list of three numbers
rounded to 0 dp, in that order.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **3 row(s)** &nbsp;|&nbsp; Sort the output as described. &nbsp;|&nbsp; tables: `loan`

### Q05 &nbsp; ★★ &nbsp; (core)

On `bureau`, compare the average `bureau_score` of reports **with** at least one default listing
(`default_listings > 0`) against those **without**. Thin files (missing score) are excluded.
Return `group` (`'listed'` / `'clean'`) and `avg_score` rounded to 1 dp; sorted by `group`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **2 row(s)** &nbsp;|&nbsp; Sort the output as described. &nbsp;|&nbsp; tables: `bureau`

<details><summary>hint</summary>

`np.isnan(arr)` marks the thin files; combine masks with `&` and `~`.

</details>

### Q06 &nbsp; ★★ &nbsp; (core)

For `loan_id` 1664 (a variable-rate loan from 2019), take its `interest_rate_pct` month by month (`snap`, ordered by `snapshot_date`).
How many month-to-month steps were **rate rises**? Use `np.diff` and `np.sign`.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter. &nbsp;|&nbsp; tables: `snap`

### Q07 &nbsp; ★★ &nbsp; (core)

Balance-weighted average `interest_rate_pct` of the **live book** at 2025-12-31 (`snapshot_date` = 2025-12-31
and `loan_status` not `'Closed'`), weights = `closing_balance`. Use `np.average`. Round to 3 dp.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter. &nbsp;|&nbsp; tables: `snap`

### Q08 &nbsp; ★★★ &nbsp; (challenge)

Put every live loan at 2025-12-31 into a tier with `np.select` on `days_past_due`:
0 = `'Current'`, 1-29 = `'Early'`, 30-89 = `'Late'`, 90+ = `'Default'`.
Return `tier`, `loans`; sorted by `tier`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **4 row(s)** &nbsp;|&nbsp; Sort the output as described. &nbsp;|&nbsp; tables: `snap`

<details><summary>hint</summary>

`np.select` takes the first condition that is True, so order the conditions from lowest to highest.

</details>
