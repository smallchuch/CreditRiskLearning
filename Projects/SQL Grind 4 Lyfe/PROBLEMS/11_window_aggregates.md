# 11 - Window functions II: LAG/LEAD, running totals, moving averages

`answers/11_window_aggregates/qNN.sql` &nbsp;|&nbsp; check with: `grade 11` or `grade 11 q03`

Levels: ★ warm-up &nbsp; ★★ core &nbsp; ★★★ challenge. Return columns **in the order shown**; column names don't matter. Rows only need to be sorted when the question says so. Numbers match within a small tolerance.

## Aggregates + OVER = running totals, moving averages, comparisons with the previous row

```
 month   amount   LAG(amount)   amount - LAG    SUM(amount) OVER (ORDER BY month)
 Jan     100      NULL          NULL            100
 Feb     120      100           +20             220
 Mar      90      120           -30             310
```

| Function | Gives you |
|---|---|
| `LAG(x, 1) OVER (...)` | value from the previous row |
| `LEAD(x, 1) OVER (...)` | value from the next row |
| `FIRST_VALUE(x)` / `LAST_VALUE(x)` | first / last in the frame |
| `SUM(x) OVER (PARTITION BY g)` | group total on every row (share-of-total) |
| `SUM(x) OVER (ORDER BY d)` | running total |
| `AVG(x) OVER (ORDER BY d ROWS BETWEEN 2 PRECEDING AND CURRENT ROW)` | 3-period moving average |

### The frame
```
 ROWS BETWEEN 2 PRECEDING AND CURRENT ROW      [ r-2 | r-1 | r ]   <- the rows included for row r
 ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW     (default for ORDER BY: running total)
```
Careful: if you add `ORDER BY` the default frame is "start .. current row", which is why `LAST_VALUE` often needs `ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING`.

Snapshot table pattern: `PARTITION BY loan_id ORDER BY snapshot_date` + `LAG(days_past_due)` = "what was it last month?" - the heart of **roll-rate** analysis.

---

## Problems

### Q01 &nbsp; ★ &nbsp; (warm-up)

Monthly originated volume for 2023 with prior-month volume: `month_start`, `amount` (0dp), `prev_amount` (0dp) using LAG. Sorted by `month_start`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **12 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q02 &nbsp; ★ &nbsp; (warm-up)

Running count of applications by month in 2025: `month_start`, `apps`, `cumulative_apps`. Sorted by `month_start`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **12 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q03 &nbsp; ★ &nbsp; (warm-up)

Share of total: each `purpose`'s share of total original lending (1dp %). Return `purpose`, `share_pct`; sorted by share descending then purpose.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **6 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q04 &nbsp; ★★ &nbsp; (core)

Month-on-month growth in application volume (%): for each month of 2024-2025 return `month_start`, `apps`, `mom_pct` (1dp; NULL for the first month). Sorted by `month_start`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **24 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q05 &nbsp; ★★ &nbsp; (core)

3-month moving average of loans originated per month, for all months in 2025: `month_start`, `loans`, `ma3` (1dp) using `ROWS BETWEEN 2 PRECEDING AND CURRENT ROW` over the full monthly series (so January 2025 uses Nov-Dec 2024 as well). Return only 2025 months, sorted.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **12 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q06 &nbsp; ★★ &nbsp; (core)

Days between a customer's consecutive applications: for customers with at least 2 applications, the average gap in days (1dp) across all gaps. One number. (Use LAG on `application_date` per customer ordered by date, application_id.)

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q07 &nbsp; ★★ &nbsp; (core)

Loan 1's balance history: `snapshot_date`, `closing_balance`, `prev_balance`, `principal_paid` (= prev - current, 2dp) for loan_id = 1, sorted by date. Rows with no prior month show NULL.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **28 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q08 &nbsp; ★★ &nbsp; (core)

Next-month arrears: for loan 1 show `snapshot_date`, `days_past_due`, and the NEXT month's dpd with LEAD (`next_dpd`). Sorted by date.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **28 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q09 &nbsp; ★★ &nbsp; (core)

Cumulative share (Pareto): rank brokers by total lending; return `broker_id`, `total` (0dp), `cum_share_pct` (1dp) for the top 10 brokers. Sorted by `total` descending, `broker_id`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **10 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q10 &nbsp; ★★★ &nbsp; (challenge)

Roll-rate seed. For each month-end in 2025, using LAG per loan, count loans that were 0 DPD last month and 30+ DPD this month (`rolled_to_30plus`) and loans that were 0 DPD last month (`from_current`). Return `snapshot_date`, `from_current`, `rolled_to_30plus`; sorted by `snapshot_date`. Only snapshot dates in 2025; non-closed loans.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **12 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q11 &nbsp; ★★★ &nbsp; (challenge)

Cure rate. For 2025 snapshots, among non-closed loans that were 30-89 DPD last month, how many are at 0 DPD this month? Return one row: `were_30_89`, `cured`, `cure_rate_pct` (1dp).

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q12 &nbsp; ★★★ &nbsp; (challenge)

Peak arrears: for each loan that ever reached 90+ DPD, the maximum `days_past_due` ever. Return `bucket` (`'90-179'`, `'180+'`) and `loans`, sorted by bucket.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **2 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q13 &nbsp; ★★★ &nbsp; (challenge)

Balance drift since the first snapshot: for loans 1-5 and their first four snapshots (`months_on_book <= 4`), return `loan_id`, `months_on_book`, `closing_balance` and `balance_vs_first` = closing_balance minus `FIRST_VALUE(closing_balance)` over that loan's history ordered by date (2dp). Sorted by `loan_id`, `months_on_book`.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **25 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q14 &nbsp; ★★★ &nbsp; (challenge)

Months since last payment missed: for loan 1 compute for each snapshot a flag `shortfall` = `actual_repayment < scheduled_repayment` and a running count of shortfall months (`cum_shortfalls`). Return `snapshot_date`, `shortfall`, `cum_shortfalls` for loans 1, snapshots on or after 2019-01-31. Sorted by date.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **22 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q15 &nbsp; ★★★ &nbsp; (challenge)

Year-on-year: loans originated per month with the same month a year earlier (`LAG(n, 12)`), for months of 2025. Return `month_start`, `loans`, `loans_ly`, `yoy_pct` (1dp); sorted by month.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **12 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q16 &nbsp; ★★★ &nbsp; (challenge)

Closing-balance reconciliation. For loans 1-10 and their snapshots, check balance continuity: `prev_close + interest_charged - actual_repayment` should be close to `closing_balance` (within $1 after allowing for offset effects - treat only loans with `offset_balance` = 0 or NULL). Count the snapshot rows where the difference exceeds $1. One number (information only).

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q17 &nbsp; ★★★ &nbsp; (challenge)

Largest single-month balance drop (prepayment/lump sum) in 2025 for non-closed loans: return the top 5 loans by balance decrease vs the prior month (`loan_id`, `snapshot_date`, `drop` 0dp). Sorted by `drop` descending, then `loan_id`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **5 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q18 &nbsp; ★★ &nbsp; (core)

Monthly new-loan counts for 2020 with the percentage change on the previous month (`LAG`, 1 dp), using the full monthly series so January compares with the prior December. `month_no`, `loans`, `mom_pct`; sorted by month.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **12 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q19 &nbsp; ★★ &nbsp; (core)

Monthly new-loan counts for 2021 with the percentage change on the previous month (`LAG`, 1 dp), using the full monthly series so January compares with the prior December. `month_no`, `loans`, `mom_pct`; sorted by month.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **12 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q20 &nbsp; ★★ &nbsp; (core)

Monthly new-loan counts for 2022 with the percentage change on the previous month (`LAG`, 1 dp), using the full monthly series so January compares with the prior December. `month_no`, `loans`, `mom_pct`; sorted by month.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **12 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q21 &nbsp; ★★ &nbsp; (core)

Monthly new-loan counts for 2023 with the percentage change on the previous month (`LAG`, 1 dp), using the full monthly series so January compares with the prior December. `month_no`, `loans`, `mom_pct`; sorted by month.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **12 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q22 &nbsp; ★★ &nbsp; (core)

Monthly new-loan counts for 2024 with the percentage change on the previous month (`LAG`, 1 dp), using the full monthly series so January compares with the prior December. `month_no`, `loans`, `mom_pct`; sorted by month.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **12 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q23 &nbsp; ★★ &nbsp; (core)

Monthly new-loan counts for 2025 with the percentage change on the previous month (`LAG`, 1 dp), using the full monthly series so January compares with the prior December. `month_no`, `loans`, `mom_pct`; sorted by month.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **12 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q24 &nbsp; ★★ &nbsp; (core)

Running total of `'Purchase - Owner Occupied'` lending by month in 2024: `month_no`, `amount` (0 dp), `running_total` (0 dp); sorted by month.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **12 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q25 &nbsp; ★★ &nbsp; (core)

Running total of `'Purchase - Investment'` lending by month in 2024: `month_no`, `amount` (0 dp), `running_total` (0 dp); sorted by month.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **12 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q26 &nbsp; ★★ &nbsp; (core)

Running total of `'Refinance'` lending by month in 2024: `month_no`, `amount` (0 dp), `running_total` (0 dp); sorted by month.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **12 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q27 &nbsp; ★★ &nbsp; (core)

Running total of `'Equity Release / Top-up'` lending by month in 2024: `month_no`, `amount` (0 dp), `running_total` (0 dp); sorted by month.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **12 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q28 &nbsp; ★★ &nbsp; (core)

Running total of `'Construction'` lending by month in 2024: `month_no`, `amount` (0 dp), `running_total` (0 dp); sorted by month.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **12 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q29 &nbsp; ★★★ &nbsp; (challenge)

3-month moving average of monthly loans written via `'Broker'` (use all history in the window); return the 2025 months only. `month_start`, `loans`, `ma3` (1 dp); sorted by month.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **12 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q30 &nbsp; ★★★ &nbsp; (challenge)

3-month moving average of monthly loans written via `'Branch'` (use all history in the window); return the 2025 months only. `month_start`, `loans`, `ma3` (1 dp); sorted by month.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **12 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q31 &nbsp; ★★★ &nbsp; (challenge)

3-month moving average of monthly loans written via `'Digital'` (use all history in the window); return the 2025 months only. `month_start`, `loans`, `ma3` (1 dp); sorted by month.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **12 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q32 &nbsp; ★★★ &nbsp; (challenge)

3-month moving average of monthly loans written via `'Mobile Lender'` (use all history in the window); return the 2025 months only. `month_start`, `loans`, `ma3` (1 dp); sorted by month.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **12 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q33 &nbsp; ★★ &nbsp; (core)

Loan 1003: for its first 6 snapshots (`months_on_book` 1-6) show `months_on_book`, `closing_balance` and the principal reduction vs the previous month (`LAG`, 2 dp). Sorted by `months_on_book`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **6 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q34 &nbsp; ★★ &nbsp; (core)

Loan 1008: for its first 6 snapshots (`months_on_book` 1-6) show `months_on_book`, `closing_balance` and the principal reduction vs the previous month (`LAG`, 2 dp). Sorted by `months_on_book`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **6 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q35 &nbsp; ★★ &nbsp; (core)

Loan 1014: for its first 6 snapshots (`months_on_book` 1-6) show `months_on_book`, `closing_balance` and the principal reduction vs the previous month (`LAG`, 2 dp). Sorted by `months_on_book`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **6 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q36 &nbsp; ★★ &nbsp; (core)

Loan 1016: for its first 6 snapshots (`months_on_book` 1-6) show `months_on_book`, `closing_balance` and the principal reduction vs the previous month (`LAG`, 2 dp). Sorted by `months_on_book`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **6 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q37 &nbsp; ★★ &nbsp; (core)

Loan 1018: for its first 6 snapshots (`months_on_book` 1-6) show `months_on_book`, `closing_balance` and the principal reduction vs the previous month (`LAG`, 2 dp). Sorted by `months_on_book`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **6 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q38 &nbsp; ★★★ &nbsp; (challenge)

Loan 1003: running count of months with `days_past_due > 0` and the highest dpd seen so far (`MAX() OVER`) for its first 12 snapshots (`months_on_book` 0-11). `months_on_book`, `cum_arrears_months`, `max_dpd_so_far`; sorted by months_on_book.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **12 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q39 &nbsp; ★★★ &nbsp; (challenge)

Loan 1008: running count of months with `days_past_due > 0` and the highest dpd seen so far (`MAX() OVER`) for its first 12 snapshots (`months_on_book` 0-11). `months_on_book`, `cum_arrears_months`, `max_dpd_so_far`; sorted by months_on_book.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **12 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q40 &nbsp; ★★★ &nbsp; (challenge)

Loan 1014: running count of months with `days_past_due > 0` and the highest dpd seen so far (`MAX() OVER`) for its first 12 snapshots (`months_on_book` 0-11). `months_on_book`, `cum_arrears_months`, `max_dpd_so_far`; sorted by months_on_book.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **12 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q41 &nbsp; ★★★ &nbsp; (challenge)

Share of the year: each month's share of 2022's total new lending (1 dp %) with `SUM(amount) OVER ()`. `month_no`, `share_pct`; sorted by month.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **12 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q42 &nbsp; ★★★ &nbsp; (challenge)

Share of the year: each month's share of 2023's total new lending (1 dp %) with `SUM(amount) OVER ()`. `month_no`, `share_pct`; sorted by month.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **12 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q43 &nbsp; ★★★ &nbsp; (challenge)

Share of the year: each month's share of 2024's total new lending (1 dp %) with `SUM(amount) OVER ()`. `month_no`, `share_pct`; sorted by month.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **12 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q44 &nbsp; ★★★ &nbsp; (challenge)

Share of the year: each month's share of 2025's total new lending (1 dp %) with `SUM(amount) OVER ()`. `month_no`, `share_pct`; sorted by month.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **12 row(s)** &nbsp;|&nbsp; Sort the output as described.
