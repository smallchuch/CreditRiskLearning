from . import P

PRIMER = r"""
## Scenario: build the monthly credit risk pack

Every month the head of credit risk gets one pack. You assemble it with SQL. Think **KPI table**: one row per month, one column per KPI - the shape that feeds Power BI / Excel charts.

```
 month_end | live_loans | balance | new_loans | new_balance | 30+ rate | 90+ rate | closed | net growth
```
Patterns used: month-end spine, conditional aggregation, `LAG` for movement, balance roll-forward (opening + new - repayments/closures = closing), YTD with a window (`SUM() OVER (PARTITION BY year ORDER BY month)`).
Always state the definition of every KPI in a comment - the real job is making numbers that are *the same every time*.
"""

CONCEPT = dict(id="cr11_monthly_reporting_pack", title="CR11 - Building the monthly reporting pack", primer=PRIMER, problems=[
    P(1, "Live loans and total balance at each month-end of 2025. `snapshot_date`, `loans`, `balance` (0dp); sorted by date.",
      "SELECT snapshot_date, COUNT(*), ROUND(SUM(closing_balance),0) FROM loan_monthly_snapshot WHERE snapshot_date>=DATE '2025-01-01' AND loan_status<>'Closed' GROUP BY 1 ORDER BY 1"),
    P(1, "New lending by month 2025: loans and $ (0dp). `month_start`, `new_loans`, `new_amount`; sorted by month.",
      "SELECT CAST(date_trunc('month', origination_date) AS DATE), COUNT(*), ROUND(SUM(original_amount),0) FROM loan WHERE origination_date>=DATE '2025-01-01' AND origination_date<DATE '2026-01-01' GROUP BY 1 ORDER BY 1"),
    P(1, "Loans closed by month in 2025 by count (use `closed_date`). `month_start`, `closed_loans`; sorted by month.",
      "SELECT CAST(date_trunc('month', closed_date) AS DATE), COUNT(*) FROM loan WHERE closed_date>=DATE '2025-01-01' AND closed_date<DATE '2026-01-01' GROUP BY 1 ORDER BY 1"),
    P(2, "One KPI table, 2025 month-ends: `snapshot_date`, `live_loans`, `balance` (0dp), `pct_30plus` (count, 2dp), `pct_90plus` (count, 2dp). Sorted by date.",
      "SELECT snapshot_date, COUNT(*), ROUND(SUM(closing_balance),0), ROUND(100.0*COUNT(*) FILTER (WHERE days_past_due>=30)/COUNT(*),2), ROUND(100.0*COUNT(*) FILTER (WHERE days_past_due>=90)/COUNT(*),2) FROM loan_monthly_snapshot WHERE snapshot_date>=DATE '2025-01-01' AND loan_status<>'Closed' GROUP BY 1 ORDER BY 1"),
    P(2, "Net loan growth: for each 2025 month, `new_loans` minus `closed_loans` and the change in live loan count (from snapshots). Return `month_start`, `new_loans`, `closed_loans`, `net_flow`, `live_change` for Feb-Dec 2025; sorted by month. (live_change = live now - live last month-end.)",
      """WITH n AS (SELECT CAST(date_trunc('month', origination_date) AS DATE) AS m, COUNT(*) AS n FROM loan GROUP BY 1),
c AS (SELECT CAST(date_trunc('month', closed_date) AS DATE) AS m, COUNT(*) AS c FROM loan WHERE closed_date IS NOT NULL GROUP BY 1),
l AS (SELECT CAST(date_trunc('month', snapshot_date) AS DATE) AS m, COUNT(*) AS live FROM loan_monthly_snapshot WHERE loan_status<>'Closed' GROUP BY 1),
j AS (SELECT l.m, n.n, c.c, l.live, LAG(l.live) OVER (ORDER BY l.m) AS pl FROM l JOIN n USING (m) LEFT JOIN c USING (m))
SELECT m, n, COALESCE(c,0), n-COALESCE(c,0), live-pl FROM j WHERE m>=DATE '2025-02-01' ORDER BY m"""),
    P(2, "Year-to-date new lending: monthly new amount and YTD cumulative (0dp) for 2024 and 2025 using `SUM() OVER (PARTITION BY year ORDER BY month)`. `yr`, `mon`, `new_amount`, `ytd_amount`; sorted by year, month.",
      "SELECT yr, mon, ROUND(a,0), ROUND(SUM(a) OVER (PARTITION BY yr ORDER BY mon),0) FROM (SELECT year(origination_date) AS yr, month(origination_date) AS mon, SUM(original_amount) AS a FROM loan WHERE origination_date>=DATE '2024-01-01' AND origination_date<DATE '2026-01-01' GROUP BY 1,2) ORDER BY 1,2"),
    P(3, "Balance roll-forward by month for 2025 (Feb-Dec): `opening` (prior month-end live balance), `new_lending` (loans originated in the month), `closing` (live balance), and `other_movements` = closing - opening - new_lending (repayments, closures, interest; 0dp). `month_end`, `opening`, `new_lending`, `closing`, `other_movements`; sorted by date.",
      """WITH b AS (SELECT snapshot_date AS d, SUM(closing_balance) AS bal FROM loan_monthly_snapshot WHERE loan_status<>'Closed' GROUP BY 1),
n AS (SELECT last_day(origination_date) AS d, SUM(original_amount) AS n FROM loan GROUP BY 1)
SELECT d, ROUND(op,0), ROUND(n,0), ROUND(bal,0), ROUND(bal-op-n,0) FROM (SELECT b.d, LAG(b.bal) OVER (ORDER BY b.d) AS op, n.n, b.bal FROM b LEFT JOIN n ON n.d=b.d) WHERE d>=DATE '2025-02-01' ORDER BY d"""),
    P(3, "Top movers: the 5 `purpose` x `channel` segments whose live balance grew most between 2024-12-31 and 2025-12-31 (absolute $, 0dp). `purpose`, `channel`, `growth`; sorted by growth descending.",
      "SELECT l.purpose, l.channel, ROUND(SUM(s.closing_balance) FILTER (WHERE s.snapshot_date=DATE '2025-12-31') - COALESCE(SUM(s.closing_balance) FILTER (WHERE s.snapshot_date=DATE '2024-12-31'),0),0) AS g FROM loan_monthly_snapshot s JOIN loan l USING (loan_id) WHERE s.snapshot_date IN (DATE '2024-12-31', DATE '2025-12-31') AND s.loan_status<>'Closed' GROUP BY 1,2 ORDER BY g DESC, 1, 2 LIMIT 5"),
    P(3, "A one-row 'executive summary' for 2025-12-31: live loans, balance ($m, 1dp), % 90+ DPD (2dp), total ECL ($m, 1dp), ECL coverage (2dp %), new lending in Q4 2025 ($m, 1dp). `live_loans`, `balance_m`, `pct_90plus`, `ecl_m`, `coverage_pct`, `q4_new_m`.",
      """SELECT (SELECT COUNT(*) FROM loan_monthly_snapshot WHERE snapshot_date=DATE '2025-12-31' AND loan_status<>'Closed'),
 (SELECT ROUND(SUM(closing_balance)/1e6,1) FROM loan_monthly_snapshot WHERE snapshot_date=DATE '2025-12-31' AND loan_status<>'Closed'),
 (SELECT ROUND(100.0*COUNT(*) FILTER (WHERE days_past_due>=90)/COUNT(*),2) FROM loan_monthly_snapshot WHERE snapshot_date=DATE '2025-12-31' AND loan_status<>'Closed'),
 (SELECT ROUND(SUM(ecl_amount)/1e6,1) FROM ecl_provision_quarterly WHERE reporting_date=DATE '2025-12-31'),
 (SELECT ROUND(100*SUM(ecl_amount)/SUM(ead),2) FROM ecl_provision_quarterly WHERE reporting_date=DATE '2025-12-31'),
 (SELECT ROUND(SUM(original_amount)/1e6,1) FROM loan WHERE origination_date>=DATE '2025-10-01' AND origination_date<=DATE '2025-12-31')"""),
    P(3, "Rolling 12-month new lending: for each month-end from Dec 2019 to Dec 2025, the sum of new lending in the latest 12 months ($m, 1dp). Use a window `ROWS BETWEEN 11 PRECEDING AND CURRENT ROW` over a monthly series. Return only the December rows: `month_start`, `rolling_12m_m`; sorted by month.",
      """WITH m AS (SELECT CAST(date_trunc('month', origination_date) AS DATE) AS ms, SUM(original_amount) AS a FROM loan GROUP BY 1),
r AS (SELECT ms, SUM(a) OVER (ORDER BY ms ROWS BETWEEN 11 PRECEDING AND CURRENT ROW) AS s, ROW_NUMBER() OVER (ORDER BY ms) AS rn FROM m)
SELECT ms, ROUND(s/1e6,1) FROM r WHERE month(ms)=12 AND rn>=12 ORDER BY ms"""),
    P(3, "Branch scorecard for 2025: for each branch with at least 60 loans originated in 2025: loans, $ (0dp), average LVR (1dp). Top 5 by $ . `branch_name`, `loans`, `amount`, `avg_lvr`; sorted by amount descending.",
      "SELECT b.branch_name, COUNT(*), ROUND(SUM(l.original_amount),0) AS a, ROUND(AVG(l.lvr_at_origination_pct),1) FROM loan l JOIN dim_branch b USING (branch_id) WHERE l.origination_date>=DATE '2025-01-01' AND l.origination_date<DATE '2026-01-01' GROUP BY b.branch_id, b.branch_name HAVING COUNT(*)>=60 ORDER BY a DESC LIMIT 5"),
])
