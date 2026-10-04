from . import P

PRIMER = r"""
## CTE = a named step. Write the query as a story, top to bottom.

```
 WITH step1 AS ( ... ),          -- 'first, get X'
      step2 AS ( ... FROM step1 ), -- 'then, using X, get Y'
 SELECT ... FROM step2;          -- 'finally, show Y'
```

Why: readable, reusable twice in the same query, easy to debug (run each step alone).

```
 loans -> [monthly_totals] -> [with_prior_month] -> final answer
```

**Recursive CTE** - a query that calls itself, used for hierarchies and sequences:
```
 WITH RECURSIVE chain AS (
     SELECT staff_id, manager_staff_id, 1 AS depth FROM dim_staff WHERE manager_staff_id IS NULL   -- anchor
     UNION ALL
     SELECT s.staff_id, s.manager_staff_id, c.depth+1
     FROM dim_staff s JOIN chain c ON s.manager_staff_id = c.staff_id                               -- recursive step
 )
 SELECT * FROM chain;
```
Anchor = the starting rows; recursive part = "find the next level"; stops when no new rows.
You can also generate a date spine: `SELECT unnest(generate_series(DATE '2025-01-01', DATE '2025-12-31', INTERVAL 1 DAY))`.
"""

CONCEPT = dict(id="09_ctes", title="09 - CTEs and recursive queries", primer=PRIMER, problems=[
    P(1, "Using a CTE named `big` of loans over $1,000,000, count them by `purpose`. Return `purpose`, `loans`; sorted by `loans` descending then `purpose`.",
      "WITH big AS (SELECT * FROM loan WHERE original_amount > 1000000) SELECT purpose, COUNT(*) AS n FROM big GROUP BY 1 ORDER BY n DESC, 1"),
    P(1, "CTE of yearly loan counts, then select years with more than 9,000 loans. Return `yr`, `loans`; sorted by `yr`.",
      "WITH y AS (SELECT year(origination_date) AS yr, COUNT(*) AS n FROM loan GROUP BY 1) SELECT yr, n FROM y WHERE n > 9000 ORDER BY 1"),
    P(1, "Two CTEs: `a` = count of loans, `b` = count of applications. Return one row: loans, applications, and loans/applications as a % (1dp).",
      "WITH a AS (SELECT COUNT(*) AS n FROM loan), b AS (SELECT COUNT(*) AS n FROM loan_application) SELECT a.n, b.n, ROUND(100.0*a.n/b.n,1) FROM a, b"),
    P(2, "Funnel with CTEs: applications by `current_status` as a share of all applications. Return `current_status`, `share_pct` (1dp); sorted by share descending.",
      "WITH s AS (SELECT current_status, COUNT(*) AS n FROM loan_application GROUP BY 1) SELECT current_status, ROUND(100.0*n/SUM(n) OVER (),1) AS p FROM s ORDER BY p DESC, 1"),
    P(2, "Monthly origination totals then month-on-month change. In a CTE build `month_start`, `amount` for 2024; then in the final select return `month_start`, `amount` (0dp) and `prev_amount` (0dp) using `LAG`. Sorted by `month_start`. (Previews window functions.)",
      """WITH m AS (SELECT CAST(date_trunc('month', origination_date) AS DATE) AS ms, SUM(original_amount) AS a FROM loan WHERE origination_date >= DATE '2024-01-01' AND origination_date < DATE '2025-01-01' GROUP BY 1)
SELECT ms, ROUND(a,0), ROUND(LAG(a) OVER (ORDER BY ms),0) FROM m ORDER BY ms"""),
    P(2, "Recursive CTE number series: produce the integers 1 to 12 (column `n`) using a recursive CTE.",
      "WITH RECURSIVE t(n) AS (SELECT 1 UNION ALL SELECT n+1 FROM t WHERE n < 12) SELECT n FROM t ORDER BY n"),
    P(2, "Recursive date spine: all month-end dates in 2025 (12 rows) starting at 2025-01-31 using `last_day(prev + INTERVAL 1 MONTH)`. Return `month_end` sorted ascending.",
      "WITH RECURSIVE d(m) AS (SELECT DATE '2025-01-31' UNION ALL SELECT last_day(m + INTERVAL 1 MONTH) FROM d WHERE m < DATE '2025-11-30') SELECT CAST(m AS DATE) FROM d ORDER BY 1"),
    P(2, "Reporting line depth. Using a recursive CTE walk the staff hierarchy from the top (`manager_staff_id IS NULL`) and return `depth`, `staff_count`; sorted by `depth`.",
      "WITH RECURSIVE c AS (SELECT staff_id, 1 AS depth FROM dim_staff WHERE manager_staff_id IS NULL UNION ALL SELECT s.staff_id, c.depth+1 FROM dim_staff s JOIN c ON s.manager_staff_id=c.staff_id) SELECT depth, COUNT(*) FROM c GROUP BY 1 ORDER BY 1"),
    P(2, "Application-to-loan pipeline in 3 CTEs: `apps` (2025 applications), `settled` (those that settled), `rates` giving the settle rate. Return `applications`, `settled`, `settle_rate_pct` (1dp) as one row.",
      """WITH apps AS (SELECT * FROM loan_application WHERE application_date >= DATE '2025-01-01' AND application_date < DATE '2026-01-01'),
settled AS (SELECT * FROM apps WHERE current_status='Settled')
SELECT (SELECT COUNT(*) FROM apps), (SELECT COUNT(*) FROM settled), ROUND(100.0*(SELECT COUNT(*) FROM settled)/(SELECT COUNT(*) FROM apps),1)"""),
    P(2, "Reuse a CTE twice: using a CTE `bal` of 2025-12-31 balances (non-closed) per loan, show the share of total balance held by the top 100 loans by balance. Return one number (`pct`, 2 dp).",
      """WITH bal AS (SELECT loan_id, closing_balance AS b FROM loan_monthly_snapshot WHERE snapshot_date=DATE '2025-12-31' AND loan_status<>'Closed'),
top AS (SELECT b FROM bal ORDER BY b DESC, loan_id LIMIT 100)
SELECT ROUND(100.0*(SELECT SUM(b) FROM top)/(SELECT SUM(b) FROM bal),2)"""),
    P(3, "Per-customer first application date, then how many customers made their first application in each year. In CTE `f` compute first `application_date` per `primary_customer_id`. Return `yr`, `new_applicants`; sorted by `yr`.",
      "WITH f AS (SELECT primary_customer_id, MIN(application_date) AS d FROM loan_application GROUP BY 1) SELECT year(d), COUNT(*) FROM f GROUP BY 1 ORDER BY 1"),
    P(3, "Refinance chains with recursion: starting from loans with no parent (`parent_loan_id IS NULL`) that have at least one internal-refinance child, follow the child links. Return `chain_length`, `chains`, where chain_length is the number of loans in the chain from the root to the last descendant. Sorted by `chain_length`.",
      """WITH RECURSIVE c AS (
  SELECT loan_id AS root, loan_id, 1 AS len FROM loan WHERE parent_loan_id IS NULL AND EXISTS (SELECT 1 FROM loan k WHERE k.parent_loan_id=loan.loan_id)
  UNION ALL SELECT c.root, l.loan_id, c.len+1 FROM loan l JOIN c ON l.parent_loan_id=c.loan_id)
SELECT mx, COUNT(*) FROM (SELECT root, MAX(len) AS mx FROM c GROUP BY 1) GROUP BY 1 ORDER BY 1"""),
    P(3, "Date spine + LEFT JOIN: for every month-end of 2025 (spine via `generate_series` or recursion) show the number of loans originated in that month, including zero months. Return `month_end`, `loans`; sorted by `month_end`.",
      """WITH sp AS (SELECT CAST(unnest(generate_series(DATE '2025-01-01', DATE '2025-12-01', INTERVAL 1 MONTH)) AS DATE) AS ms)
SELECT last_day(sp.ms), COUNT(l.loan_id) FROM sp LEFT JOIN loan l ON l.origination_date >= sp.ms AND l.origination_date < sp.ms + INTERVAL 1 MONTH GROUP BY sp.ms ORDER BY sp.ms"""),
    P(3, "Three-step arrears story: CTE `latest` = non-closed loans at 2025-12-31 with `days_past_due`; CTE `bucketed` = bucket via CASE (`'Current'` 0, `'1-29'`, `'30-89'`, `'90+'`); final = balance and loan count per bucket. Return `bucket`, `loans`, `balance` (0dp); sorted by the bucket's severity (Current first).",
      """WITH latest AS (SELECT loan_id, days_past_due AS d, closing_balance AS b FROM loan_monthly_snapshot WHERE snapshot_date=DATE '2025-12-31' AND loan_status<>'Closed'),
bk AS (SELECT CASE WHEN d=0 THEN 'Current' WHEN d<30 THEN '1-29' WHEN d<90 THEN '30-89' ELSE '90+' END AS bucket,
       CASE WHEN d=0 THEN 1 WHEN d<30 THEN 2 WHEN d<90 THEN 3 ELSE 4 END AS k, b FROM latest)
SELECT bucket, COUNT(*), ROUND(SUM(b),0) FROM bk GROUP BY bucket, k ORDER BY k"""),
    P(3, "Cumulative origination: CTE of monthly volume ($) by year-month for 2023, then a running total using `SUM() OVER (ORDER BY ms)`. Return `month_start`, `running_total` (0dp); sorted by `month_start`.",
      """WITH m AS (SELECT CAST(date_trunc('month', origination_date) AS DATE) AS ms, SUM(original_amount) AS a FROM loan WHERE origination_date >= DATE '2023-01-01' AND origination_date < DATE '2024-01-01' GROUP BY 1)
SELECT ms, ROUND(SUM(a) OVER (ORDER BY ms),0) FROM m ORDER BY ms"""),
    P(3, "Recursion with a ceiling: simulate a $500,000, 6.00% p.a. loan with $3,000 monthly repayments for 12 months. Return `month_no`, `balance` (2dp) for months 1-12. Balance_n = balance_{n-1} * (1 + 0.06/12) - 3000, starting at 500000 for month 0 (don't output month 0).",
      """WITH RECURSIVE a(m, bal) AS (SELECT 0, CAST(500000 AS DOUBLE) UNION ALL SELECT m+1, bal*(1+0.06/12)-3000 FROM a WHERE m < 12)
SELECT m, ROUND(bal,2) FROM a WHERE m >= 1 ORDER BY m"""),
    P(3, "Consecutive-event cleanup via CTE: in `application_status_history` find applications that have exactly one 'Settled' event but more than one 'Submitted' event (duplicate loads). Return the number of such applications. One number.",
      """WITH x AS (SELECT application_id, COUNT(*) FILTER (WHERE status='Settled') AS s, COUNT(*) FILTER (WHERE status='Submitted') AS sub FROM application_status_history GROUP BY 1)
SELECT COUNT(*) FROM x WHERE s=1 AND sub>1"""),
    P(3, "Rank-free top-N via CTE: for each `purpose`, which origination year had the most loans? Build `py` (purpose, year, count), then `mx` (max per purpose), join. Return `purpose`, `yr`, `loans`; sorted by `purpose`, `yr`.",
      """WITH py AS (SELECT purpose, year(origination_date) AS yr, COUNT(*) AS n FROM loan GROUP BY 1,2),
mx AS (SELECT purpose, MAX(n) AS m FROM py GROUP BY 1)
SELECT py.purpose, py.yr, py.n FROM py JOIN mx ON mx.purpose=py.purpose AND mx.m=py.n ORDER BY 1,2"""),
])
