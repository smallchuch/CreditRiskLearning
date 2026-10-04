from . import P

PRIMER = r"""
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
"""

CONCEPT = dict(id="11_window_aggregates", title="11 - Window functions II: LAG/LEAD, running totals, moving averages", primer=PRIMER, problems=[
    P(1, "Monthly originated volume for 2023 with prior-month volume: `month_start`, `amount` (0dp), `prev_amount` (0dp) using LAG. Sorted by `month_start`.",
      """WITH m AS (SELECT CAST(date_trunc('month', origination_date) AS DATE) AS ms, SUM(original_amount) AS a FROM loan WHERE origination_date >= DATE '2023-01-01' AND origination_date < DATE '2024-01-01' GROUP BY 1)
SELECT ms, ROUND(a,0), ROUND(LAG(a) OVER (ORDER BY ms),0) FROM m ORDER BY ms"""),
    P(1, "Running count of applications by month in 2025: `month_start`, `apps`, `cumulative_apps`. Sorted by `month_start`.",
      """WITH m AS (SELECT CAST(date_trunc('month', application_date) AS DATE) AS ms, COUNT(*) AS n FROM loan_application WHERE application_date >= DATE '2025-01-01' GROUP BY 1)
SELECT ms, n, SUM(n) OVER (ORDER BY ms) FROM m ORDER BY ms"""),
    P(1, "Share of total: each `purpose`'s share of total original lending (1dp %). Return `purpose`, `share_pct`; sorted by share descending then purpose.",
      "SELECT purpose, ROUND(100*SUM(original_amount)/SUM(SUM(original_amount)) OVER (),1) AS s FROM loan GROUP BY 1 ORDER BY s DESC, 1"),
    P(2, "Month-on-month growth in application volume (%): for each month of 2024-2025 return `month_start`, `apps`, `mom_pct` (1dp; NULL for the first month). Sorted by `month_start`.",
      """WITH m AS (SELECT CAST(date_trunc('month', application_date) AS DATE) AS ms, COUNT(*) AS n FROM loan_application WHERE application_date >= DATE '2024-01-01' GROUP BY 1)
SELECT ms, n, ROUND(100.0*(n/LAG(n) OVER (ORDER BY ms)-1),1) FROM m ORDER BY ms"""),
    P(2, "3-month moving average of loans originated per month, for all months in 2025: `month_start`, `loans`, `ma3` (1dp) using `ROWS BETWEEN 2 PRECEDING AND CURRENT ROW` over the full monthly series (so January 2025 uses Nov-Dec 2024 as well). Return only 2025 months, sorted.",
      """WITH m AS (SELECT CAST(date_trunc('month', origination_date) AS DATE) AS ms, COUNT(*) AS n FROM loan GROUP BY 1),
w AS (SELECT ms, n, ROUND(AVG(n) OVER (ORDER BY ms ROWS BETWEEN 2 PRECEDING AND CURRENT ROW),1) AS ma FROM m)
SELECT ms, n, ma FROM w WHERE ms >= DATE '2025-01-01' ORDER BY ms"""),
    P(2, "Days between a customer's consecutive applications: for customers with at least 2 applications, the average gap in days (1dp) across all gaps. One number. (Use LAG on `application_date` per customer ordered by date, application_id.)",
      "SELECT ROUND(AVG(application_date - prev),1) FROM (SELECT application_date, LAG(application_date) OVER (PARTITION BY primary_customer_id ORDER BY application_date, application_id) AS prev FROM loan_application) WHERE prev IS NOT NULL"),
    P(2, "Loan 1's balance history: `snapshot_date`, `closing_balance`, `prev_balance`, `principal_paid` (= prev - current, 2dp) for loan_id = 1, sorted by date. Rows with no prior month show NULL.",
      "SELECT snapshot_date, closing_balance, LAG(closing_balance) OVER (ORDER BY snapshot_date), ROUND(LAG(closing_balance) OVER (ORDER BY snapshot_date)-closing_balance,2) FROM loan_monthly_snapshot WHERE loan_id=1 ORDER BY snapshot_date"),
    P(2, "Next-month arrears: for loan 1 show `snapshot_date`, `days_past_due`, and the NEXT month's dpd with LEAD (`next_dpd`). Sorted by date.",
      "SELECT snapshot_date, days_past_due, LEAD(days_past_due) OVER (ORDER BY snapshot_date) FROM loan_monthly_snapshot WHERE loan_id=1 ORDER BY snapshot_date"),
    P(2, "Cumulative share (Pareto): rank brokers by total lending; return `broker_id`, `total` (0dp), `cum_share_pct` (1dp) for the top 10 brokers. Sorted by `total` descending, `broker_id`.",
      """WITH b AS (SELECT broker_id, SUM(original_amount) AS t FROM loan WHERE broker_id IS NOT NULL GROUP BY 1)
SELECT * FROM (SELECT broker_id, ROUND(t,0), ROUND(100*SUM(t) OVER (ORDER BY t DESC, broker_id)/SUM(t) OVER (),1) AS c FROM b) QUALIFY ROW_NUMBER() OVER (ORDER BY 2 DESC, 1) <= 10 ORDER BY 2 DESC, 1""", order=True),
    P(3, "Roll-rate seed. For each month-end in 2025, using LAG per loan, count loans that were 0 DPD last month and 30+ DPD this month (`rolled_to_30plus`) and loans that were 0 DPD last month (`from_current`). Return `snapshot_date`, `from_current`, `rolled_to_30plus`; sorted by `snapshot_date`. Only snapshot dates in 2025; non-closed loans.",
      """SELECT snapshot_date, COUNT(*) FILTER (WHERE prev_dpd=0), COUNT(*) FILTER (WHERE prev_dpd=0 AND days_past_due>=30) FROM (
 SELECT loan_id, snapshot_date, days_past_due, loan_status, LAG(days_past_due) OVER (PARTITION BY loan_id ORDER BY snapshot_date) AS prev_dpd FROM loan_monthly_snapshot)
WHERE snapshot_date >= DATE '2025-01-01' AND loan_status<>'Closed' GROUP BY 1 ORDER BY 1"""),
    P(3, "Cure rate. For 2025 snapshots, among non-closed loans that were 30-89 DPD last month, how many are at 0 DPD this month? Return one row: `were_30_89`, `cured`, `cure_rate_pct` (1dp).",
      """SELECT COUNT(*), COUNT(*) FILTER (WHERE days_past_due=0), ROUND(100.0*COUNT(*) FILTER (WHERE days_past_due=0)/COUNT(*),1) FROM (
 SELECT days_past_due, loan_status, snapshot_date, LAG(days_past_due) OVER (PARTITION BY loan_id ORDER BY snapshot_date) AS prev_dpd FROM loan_monthly_snapshot)
WHERE snapshot_date >= DATE '2025-01-01' AND loan_status<>'Closed' AND prev_dpd BETWEEN 30 AND 89"""),
    P(3, "Peak arrears: for each loan that ever reached 90+ DPD, the maximum `days_past_due` ever. Return `bucket` (`'90-179'`, `'180+'`) and `loans`, sorted by bucket.",
      "SELECT CASE WHEN m>=180 THEN '180+' ELSE '90-179' END AS b, COUNT(*) FROM (SELECT loan_id, MAX(days_past_due) AS m FROM loan_monthly_snapshot GROUP BY 1 HAVING MAX(days_past_due)>=90) GROUP BY 1 ORDER BY 1"),
    P(3, "Balance drift since the first snapshot: for loans 1-5 and their first four snapshots (`months_on_book <= 4`), return `loan_id`, `months_on_book`, `closing_balance` and `balance_vs_first` = closing_balance minus `FIRST_VALUE(closing_balance)` over that loan's history ordered by date (2dp). Sorted by `loan_id`, `months_on_book`.",
      """SELECT loan_id, months_on_book, closing_balance, d FROM (SELECT loan_id, months_on_book, closing_balance, ROUND(closing_balance-FIRST_VALUE(closing_balance) OVER (PARTITION BY loan_id ORDER BY snapshot_date),2) AS d FROM loan_monthly_snapshot WHERE loan_id<=5)
WHERE months_on_book <= 4 ORDER BY 1,2"""),
    P(3, "Months since last payment missed: for loan 1 compute for each snapshot a flag `shortfall` = `actual_repayment < scheduled_repayment` and a running count of shortfall months (`cum_shortfalls`). Return `snapshot_date`, `shortfall`, `cum_shortfalls` for loans 1, snapshots on or after 2019-01-31. Sorted by date.",
      """SELECT * FROM (SELECT snapshot_date, actual_repayment < scheduled_repayment AS sf, SUM(CASE WHEN actual_repayment < scheduled_repayment THEN 1 ELSE 0 END) OVER (ORDER BY snapshot_date) AS c FROM loan_monthly_snapshot WHERE loan_id=1) WHERE snapshot_date >= DATE '2019-01-31' ORDER BY 1"""),
    P(3, "Year-on-year: loans originated per month with the same month a year earlier (`LAG(n, 12)`), for months of 2025. Return `month_start`, `loans`, `loans_ly`, `yoy_pct` (1dp); sorted by month.",
      """WITH m AS (SELECT CAST(date_trunc('month', origination_date) AS DATE) AS ms, COUNT(*) AS n FROM loan GROUP BY 1)
SELECT * FROM (SELECT ms, n, LAG(n,12) OVER (ORDER BY ms) AS ly, ROUND(100.0*(n/LAG(n,12) OVER (ORDER BY ms)-1),1) FROM m) WHERE ms >= DATE '2025-01-01' ORDER BY ms"""),
    P(3, "Closing-balance reconciliation. For loans 1-10 and their snapshots, check balance continuity: `prev_close + interest_charged - actual_repayment` should be close to `closing_balance` (within $1 after allowing for offset effects - treat only loans with `offset_balance` = 0 or NULL). Count the snapshot rows where the difference exceeds $1. One number (information only).",
      """SELECT COUNT(*) FROM (SELECT closing_balance, interest_charged, actual_repayment, COALESCE(offset_balance,0) AS ob, LAG(closing_balance) OVER (PARTITION BY loan_id ORDER BY snapshot_date) AS pc FROM loan_monthly_snapshot WHERE loan_id <= 10)
WHERE pc IS NOT NULL AND ob=0 AND ABS(pc + interest_charged - actual_repayment - closing_balance) > 1"""),
    P(3, "Largest single-month balance drop (prepayment/lump sum) in 2025 for non-closed loans: return the top 5 loans by balance decrease vs the prior month (`loan_id`, `snapshot_date`, `drop` 0dp). Sorted by `drop` descending, then `loan_id`.",
      """SELECT loan_id, snapshot_date, ROUND(drop,0) FROM (SELECT loan_id, snapshot_date, loan_status, LAG(closing_balance) OVER (PARTITION BY loan_id ORDER BY snapshot_date)-closing_balance AS drop FROM loan_monthly_snapshot)
WHERE snapshot_date >= DATE '2025-01-01' AND loan_status<>'Closed' AND drop IS NOT NULL ORDER BY drop DESC, loan_id LIMIT 5"""),
])
