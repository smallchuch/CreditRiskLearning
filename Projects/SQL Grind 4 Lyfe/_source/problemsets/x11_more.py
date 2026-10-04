from ._gen import *
MORE_FOR = '11_window_aggregates'
PROBLEMS = []
for y in YEARS[1:]:
    PROBLEMS.append(P(2, f"Monthly new-loan counts for {y} with the percentage change on the previous month (`LAG`, 1 dp). `month_no`, `loans`, `mom_pct`; month 1 compares with December of the prior year (use the full series). Sorted by month.",
      f"WITH m AS (SELECT CAST(date_trunc('month', origination_date) AS DATE) AS ms, COUNT(*) AS n FROM loan GROUP BY 1) SELECT month(ms), n, ROUND(100.0*(n/LAG(n) OVER (ORDER BY ms)-1),1) FROM m WHERE year(ms)={y} ORDER BY ms".replace("WHERE year(ms)","QUALIFY year(ms)").replace("QUALIFY year(ms)","WHERE year(ms)") ) if False else
      P(2, f"Monthly new-loan counts for {y} with the percentage change on the previous month (`LAG`, 1 dp), using the full monthly series so January compares with the prior December. `month_no`, `loans`, `mom_pct`; sorted by month.",
      f"SELECT month(ms), n, p FROM (SELECT ms, n, ROUND(100.0*(n/LAG(n) OVER (ORDER BY ms)-1),1) AS p FROM (SELECT CAST(date_trunc('month', origination_date) AS DATE) AS ms, COUNT(*) AS n FROM loan GROUP BY 1)) WHERE year(ms)={y} ORDER BY ms"))
for p in EXT_PURPOSES:
    PROBLEMS.append(P(2, f"Running total of `'{p}'` lending by month in 2024: `month_no`, `amount` (0 dp), `running_total` (0 dp); sorted by month.",
      f"WITH m AS (SELECT month(origination_date) AS mon, SUM(original_amount) AS a FROM loan WHERE purpose='{p}' AND {yr('origination_date',2024)} GROUP BY 1) SELECT mon, ROUND(a,0), ROUND(SUM(a) OVER (ORDER BY mon),0) FROM m ORDER BY mon"))
for c in CHANNELS:
    PROBLEMS.append(P(3, f"3-month moving average of monthly loans written via `'{c}'` (use all history in the window); return the 2025 months only. `month_start`, `loans`, `ma3` (1 dp); sorted by month.",
      f"SELECT ms, n, ma FROM (SELECT ms, n, ROUND(AVG(n) OVER (ORDER BY ms ROWS BETWEEN 2 PRECEDING AND CURRENT ROW),1) AS ma FROM (SELECT CAST(date_trunc('month', origination_date) AS DATE) AS ms, COUNT(*) AS n FROM loan WHERE channel='{c}' GROUP BY 1)) WHERE ms>=DATE '2025-01-01' ORDER BY ms"))
for lid in (1003,1008,1014,1016,1018):
    PROBLEMS.append(P(2, f"Loan {lid}: for its first 6 snapshots (`months_on_book` 1-6) show `months_on_book`, `closing_balance` and the principal reduction vs the previous month (`LAG`, 2 dp). Sorted by `months_on_book`.",
      f"SELECT months_on_book, closing_balance, d FROM (SELECT months_on_book, closing_balance, ROUND(LAG(closing_balance) OVER (ORDER BY snapshot_date)-closing_balance,2) AS d FROM loan_monthly_snapshot WHERE loan_id={lid}) WHERE months_on_book BETWEEN 1 AND 6 ORDER BY 1"))
for lid in (1003,1008,1014):
    PROBLEMS.append(P(3, f"Loan {lid}: running count of months with `days_past_due > 0` and the highest dpd seen so far (`MAX() OVER`) for its first 12 snapshots (`months_on_book` 0-11). `months_on_book`, `cum_arrears_months`, `max_dpd_so_far`; sorted by months_on_book.",
      f"SELECT months_on_book, cum, mx FROM (SELECT months_on_book, SUM(CASE WHEN days_past_due>0 THEN 1 ELSE 0 END) OVER (ORDER BY snapshot_date) AS cum, MAX(days_past_due) OVER (ORDER BY snapshot_date) AS mx FROM loan_monthly_snapshot WHERE loan_id={lid}) WHERE months_on_book<12 ORDER BY 1"))
for y in (2022,2023,2024,2025):
    PROBLEMS.append(P(3, f"Share of the year: each month's share of {y}'s total new lending (1 dp %) with `SUM(amount) OVER ()`. `month_no`, `share_pct`; sorted by month.",
      f"WITH m AS (SELECT month(origination_date) AS mon, SUM(original_amount) AS a FROM loan WHERE {yr('origination_date',y)} GROUP BY 1) SELECT mon, ROUND(100*a/SUM(a) OVER (),1) FROM m ORDER BY mon"))
