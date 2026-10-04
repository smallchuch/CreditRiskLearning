from . import P

PRIMER = r"""
## Writing SQL that doesn't take all afternoon

You don't need to be a DBA, but you should know *why* a query is slow:

```
 Slow patterns                              Faster rewrite
 ------------------------------------------ ----------------------------------------------------
 SELECT * on a wide table                    select only the columns you need
 function on a filtered column               year(d) = 2024   ->   d >= '2024-01-01' AND d < '2025-01-01'
 correlated subquery per row                 join to a pre-aggregated table, or a window function
 DISTINCT to hide a join fan-out             fix the join grain (aggregate first / EXISTS)
 NOT IN (subquery)                           NOT EXISTS
 UNION (needless dedupe)                     UNION ALL
 filter AFTER a huge join                    filter / aggregate BEFORE joining (CTE)
 COUNT(DISTINCT) everywhere                  fine in DuckDB, but check the grain first
```

Use `EXPLAIN` / `EXPLAIN ANALYZE` in the DuckDB shell to see the plan: look for big joins on the wrong side and full scans.
In this sandbox the checker only compares RESULTS - but each task says what the "naive" approach is so you practise the better one. Keep a note of why yours is better.

Habit: read from the smallest table / filter earliest / aggregate before joining.
"""

CONCEPT = dict(id="17_performance_rewrites", title="17 - Rewrite for clarity and speed", primer=PRIMER, problems=[
    P(1, "Naive: `WHERE year(origination_date) = 2024`. Rewrite as a range filter and return the count of 2024 loans. One number.",
      "SELECT COUNT(*) FROM loan WHERE origination_date >= DATE '2024-01-01' AND origination_date < DATE '2025-01-01'"),
    P(1, "Naive: `SELECT *` then look at one thing. Return only `loan_id`, `original_amount` for the 5 biggest loans (largest first, tie `loan_id`).",
      "SELECT loan_id, original_amount FROM loan ORDER BY original_amount DESC, loan_id LIMIT 5"),
    P(1, "Naive: `UNION` of two disjoint sets. Combine loans with `purpose='Construction'` and `purpose='Refinance'` loan counts using `UNION ALL`. Return `purpose`, `loans`; sorted by purpose.",
      "SELECT purpose, loans FROM (SELECT purpose, COUNT(*) AS loans FROM loan WHERE purpose='Construction' GROUP BY 1 UNION ALL SELECT purpose, COUNT(*) FROM loan WHERE purpose='Refinance' GROUP BY 1) ORDER BY 1"),
    P(2, "Naive: a correlated subquery computing each customer's loan count. Rewrite with a pre-aggregated join: number of customers with exactly 2 loans as primary. One number.",
      "SELECT COUNT(*) FROM (SELECT primary_customer_id, COUNT(*) AS n FROM loan GROUP BY 1) WHERE n=2"),
    P(2, "Naive: `DISTINCT` after joining `loan` to `loan_borrower` to count loans with a co-borrower. Rewrite using `EXISTS` (or a semi-join). One number.",
      "SELECT COUNT(*) FROM loan l WHERE EXISTS (SELECT 1 FROM loan_borrower b WHERE b.loan_id=l.loan_id AND b.borrower_role='Co-applicant')"),
    P(2, "Naive: `NOT IN (SELECT loan_id FROM hardship_arrangement)`. Rewrite with `NOT EXISTS` and count loans never in hardship. One number.",
      "SELECT COUNT(*) FROM loan l WHERE NOT EXISTS (SELECT 1 FROM hardship_arrangement h WHERE h.loan_id=l.loan_id)"),
    P(2, "Naive: join all 2 million snapshot rows to `loan` before filtering. Filter the snapshot to 2025-12-31 FIRST (CTE), then join, and return total balance by `purpose`. `purpose`, `balance` (0dp); sorted by purpose. (Non-closed only.)",
      "WITH s AS (SELECT loan_id, closing_balance FROM loan_monthly_snapshot WHERE snapshot_date=DATE '2025-12-31' AND loan_status<>'Closed') SELECT l.purpose, ROUND(SUM(s.closing_balance),0) FROM s JOIN loan l USING (loan_id) GROUP BY 1 ORDER BY 1"),
    P(2, "Naive: three separate queries for approved, declined and withdrawn counts. Do it in ONE pass with conditional aggregation. Return one row: `approved` (`decision = 'Approved'`), `declined` (`decision = 'Declined'`), `withdrawn` (`current_status = 'Withdrawn'`).",
      "SELECT COUNT(*) FILTER (WHERE decision='Approved'), COUNT(*) FILTER (WHERE decision='Declined'), COUNT(*) FILTER (WHERE current_status='Withdrawn') FROM loan_application"),
    P(2, "Naive: self-join to get each customer's latest application. Rewrite with `QUALIFY ROW_NUMBER()`. Return the count of customers whose latest application (by date, then id) was Declined. One number.",
      "SELECT COUNT(*) FROM (SELECT decision FROM loan_application QUALIFY ROW_NUMBER() OVER (PARTITION BY primary_customer_id ORDER BY application_date DESC, application_id DESC)=1) WHERE decision='Declined'"),
    P(2, "Naive: `SELECT COUNT(DISTINCT customer_id)` via a big join. Count distinct customers who have ever been 90+ DPD with a semi-join: customers (`primary_customer_id`) having a loan with `EXISTS` a snapshot dpd>=90. One number.",
      "SELECT COUNT(DISTINCT l.primary_customer_id) FROM loan l WHERE EXISTS (SELECT 1 FROM loan_monthly_snapshot s WHERE s.loan_id=l.loan_id AND s.days_past_due>=90)"),
    P(3, "Naive: 12 near-identical queries for monthly originations in 2025. Do it with one GROUP BY. Return `month_no`, `loans`, `amount` (0dp); sorted by month.",
      "SELECT month(origination_date), COUNT(*), ROUND(SUM(original_amount),0) FROM loan WHERE origination_date >= DATE '2025-01-01' AND origination_date < DATE '2026-01-01' GROUP BY 1 ORDER BY 1"),
    P(3, "Naive: correlated `MAX` subquery to get each loan's latest snapshot. Rewrite with `QUALIFY` or `arg_max`: total closing balance of every loan's LAST snapshot row for loans with `loan_id <= 100`. One number (0dp).",
      "SELECT ROUND(SUM(closing_balance),0) FROM (SELECT closing_balance FROM loan_monthly_snapshot WHERE loan_id<=100 QUALIFY ROW_NUMBER() OVER (PARTITION BY loan_id ORDER BY snapshot_date DESC)=1)"),
    P(3, "Naive: functions on both sides of a join (`LOWER(a.x)=LOWER(b.x)`) are slow. Count customers that share an email with another customer using GROUP BY on `LOWER(email)` rather than a self-join. One number: customers whose lowercase email is shared.",
      "SELECT COUNT(*) FROM customer WHERE LOWER(email) IN (SELECT LOWER(email) FROM customer WHERE email IS NOT NULL GROUP BY 1 HAVING COUNT(*)>1)"),
    P(3, "Naive: window over everything then filter. Compute the top 3 largest loans per state of the property efficiently: first reduce to only the columns needed, then rank. Return `state`, `loan_id`, `original_amount`; sorted by state, amount descending, loan_id. Top 3 per state.",
      "SELECT state, loan_id, original_amount FROM (SELECT d.state, l.loan_id, l.original_amount, ROW_NUMBER() OVER (PARTITION BY d.state ORDER BY l.original_amount DESC, l.loan_id) AS rn FROM loan l JOIN property p ON p.property_id=l.property_id JOIN dim_postcode d ON d.postcode=p.postcode) WHERE rn<=3 ORDER BY state, original_amount DESC, loan_id"),
    P(3, "Naive: count how many loans had a 30+ DPD month by scanning with `IN (SELECT ...)`. Rewrite as an aggregate over the snapshot then count. One number: loans with `MAX(days_past_due) >= 30`.",
      "SELECT COUNT(*) FROM (SELECT loan_id FROM loan_monthly_snapshot GROUP BY 1 HAVING MAX(days_past_due)>=30)"),
    P(3, "Naive: join `loan_payment` (900k rows) to everything. Aggregate payments first: per `payment_status`, count and total (0dp) of payments made in the last 3 months to 2025-12-31 (`payment_date > 2025-09-30`). `payment_status`, `n`, `total`; sorted by status.",
      "SELECT payment_status, COUNT(*), ROUND(SUM(payment_amount),0) FROM loan_payment WHERE payment_date > DATE '2025-09-30' AND payment_date <= DATE '2025-12-31' GROUP BY 1 ORDER BY 1"),
])
