# 11 - shift, diff, cumulative and rolling

`answers/11_shift_cumulative/qNN.py` &nbsp;|&nbsp; check with: `grade 11` or `grade 11 q03`

Levels: ★ warm-up &nbsp; ★★ core &nbsp; ★★★ challenge. Put your answer in `result`. Return columns **in the order shown** (a meaningful index counts as the leading columns); column names don't matter. Rows only need to be sorted when the question says so. Numbers match within a small tolerance.

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

---

## Problems

### Q01 &nbsp; ★ &nbsp; (warm-up)

For `loan_id` 1664, the month-to-month change in `closing_balance` (sorted by `snapshot_date`, `diff`).
What was the **largest single monthly reduction**, as a positive number rounded to 2 dp?

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Sort the output as described. &nbsp;|&nbsp; tables: `snap`

### Q02 &nbsp; ★ &nbsp; (warm-up)

Cumulative number of loans originated, by year. Return `year`, `cum_loans`; sorted by `year`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **8 row(s)** &nbsp;|&nbsp; Sort the output as described. &nbsp;|&nbsp; tables: `loan`

### Q03 &nbsp; ★★ &nbsp; (core)

Year-on-year growth in the number of loans originated, as a percentage rounded to 1 dp (`pct_change`).
Return `year`, `growth_pct`; sorted by `year` (the first year is missing).

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **8 row(s)** &nbsp;|&nbsp; Sort the output as described. &nbsp;|&nbsp; tables: `loan`

### Q04 &nbsp; ★★ &nbsp; (core)

New loans per month in 2025 and their **3-month rolling average** (rounded to 1 dp; the first two months are missing).
Month as `'2025-01'` etc. Return `month`, `loans`, `rolling_3m`; sorted by `month`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **12 row(s)** &nbsp;|&nbsp; Sort the output as described. &nbsp;|&nbsp; tables: `loan`

### Q05 &nbsp; ★★ &nbsp; (core)

New arrears: count the loan-months in **2025** where `days_past_due` was 0 the month before and above 0 this month.
Use a **grouped** `shift` so one loan never borrows another loan's history.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter. &nbsp;|&nbsp; tables: `snap`

### Q06 &nbsp; ★★ &nbsp; (core)

Roll forward: how many loans were 30-59 days past due at 2025-11-30 **and** 60-89 days past due at 2025-12-31?

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter. &nbsp;|&nbsp; tables: `snap`

### Q07 &nbsp; ★★★ &nbsp; (challenge)

Ever-90 by vintage: flag each loan that **ever** reached 90+ days past due, then per origination year return `year`,
`loans`, `ever90`, `ever90_pct` (2 dp); sorted by `year`.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **8 row(s)** &nbsp;|&nbsp; Sort the output as described. &nbsp;|&nbsp; tables: `snap`, `loan`

### Q08 &nbsp; ★★★ &nbsp; (challenge)

For loans that ever reached 30+ days past due, the `months_on_book` at which they **first** did. Return the average,
rounded to 1 dp.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter. &nbsp;|&nbsp; tables: `snap`

<details><summary>hint</summary>

The first month at 30+ is just the minimum MOB among that loan's 30+ rows.

</details>
