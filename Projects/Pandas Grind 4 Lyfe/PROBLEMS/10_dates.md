# 10 - Dates and time series

`answers/10_dates/qNN.py` &nbsp;|&nbsp; check with: `grade 10` or `grade 10 q03`

Levels: ★ warm-up &nbsp; ★★ core &nbsp; ★★★ challenge. Put your answer in `result`. Return columns **in the order shown** (a meaningful index counts as the leading columns); column names don't matter. Rows only need to be sorted when the question says so. Numbers match within a small tolerance.

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

---

## Problems

### Q01 &nbsp; ★ &nbsp; (warm-up)

Loans originated per calendar year. Return `year`, `loans`; sorted by `year`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **8 row(s)** &nbsp;|&nbsp; Sort the output as described. &nbsp;|&nbsp; tables: `loan`

### Q02 &nbsp; ★ &nbsp; (warm-up)

Loans originated per month of 2025, with the month as a string like `'2025-03'`. Return `month`, `loans`; sorted by `month`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **12 row(s)** &nbsp;|&nbsp; Sort the output as described. &nbsp;|&nbsp; tables: `loan`

### Q03 &nbsp; ★ &nbsp; (warm-up)

Median number of days from `application_date` to `decision_date` for **approved** applications. Return a number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter. &nbsp;|&nbsp; tables: `app`

### Q04 &nbsp; ★★ &nbsp; (core)

For live loans at 2025-12-31, the remaining term in **whole months** from 2025-12 to the `maturity_date` month
(join `maturity_date` from `loan`). Return the average, rounded to 1 dp.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter. &nbsp;|&nbsp; tables: `snap`, `loan`

### Q05 &nbsp; ★★ &nbsp; (core)

Loans originated per **Australian financial year** (FY ends 30 June; FY2025 = Jul 2024 - Jun 2025).
Return `fy`, `loans`; sorted by `fy`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **8 row(s)** &nbsp;|&nbsp; Sort the output as described. &nbsp;|&nbsp; tables: `loan`

### Q06 &nbsp; ★★ &nbsp; (core)

New hardship arrangements per month in **2020** (`start_date`), every month of 2020 present (0 if none), month as a
string like `'2020-04'`. Return `month`, `arrangements`; sorted by `month`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **12 row(s)** &nbsp;|&nbsp; Sort the output as described. &nbsp;|&nbsp; tables: `hardship_arrangement`

<details><summary>hint</summary>

`resample('MS').size()` only spans the months that have data; `reindex` to a full `pd.date_range` fills the gaps.

</details>

### Q07 &nbsp; ★★ &nbsp; (core)

Total book balance (`closing_balance` of all rows, $ millions, 2 dp) at each **2025 quarter-end** snapshot
(31 Mar, 30 Jun, 30 Sep, 31 Dec). Return `quarter_end` (as `'2025-03-31'` etc.), `balance_m`; sorted by `quarter_end`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **4 row(s)** &nbsp;|&nbsp; Sort the output as described. &nbsp;|&nbsp; tables: `snap`

### Q08 &nbsp; ★★★ &nbsp; (challenge)

Snapshot gaps: a loan should have one row for every month from MOB 0 to its last MOB. Count the loans whose number of
snapshot rows is **not** equal to `max(months_on_book) + 1`.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter. &nbsp;|&nbsp; tables: `snap`

### Q09 &nbsp; ★★★ &nbsp; (challenge)

Payment-shock watch: **active** fixed-rate loans whose `fixed_rate_expiry_date` falls in 2026, by quarter
(string like `'2026Q1'`). Return `quarter`, `loans`; sorted by `quarter`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **4 row(s)** &nbsp;|&nbsp; Sort the output as described. &nbsp;|&nbsp; tables: `loan`
