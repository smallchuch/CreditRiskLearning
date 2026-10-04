from . import P

PRIMER = r"""
## Timed drill - interview conditions

Rankings, running totals, LAG/LEAD and top-N - the favourite of interviewers.

**Rules**
* Set a timer: **40 minutes** for 8 questions (about 5 min each).
* No notes, no looking at the solution. Ctrl-click the data dictionary only if you would be allowed a schema in the interview.
* Say your approach out loud (or write 2 lines of plan as a comment) BEFORE writing SQL: *grain? filters? joins? checks?*
* When time is up, stop. Run `grade dr03` and note your score and which questions ran over.
* Questions get harder as you go; skipping and returning is allowed (and realistic).

Scoring guide: 8/8 = ready | 6+ = solid | below 6 = redo the weak concept sets (the question numbers tell you which).
"""

CONCEPT = dict(id="dr03_windows_timed", title="DR03 - Timed drill: window functions", primer=PRIMER, problems=[
    P(1, 'Rank the 5 largest live balances at 2025-12-31 with ROW_NUMBER (tie `loan_id`). `loan_id`, `closing_balance`, `rn`; sorted by rn.',
      "SELECT loan_id, closing_balance, rn FROM (SELECT loan_id, closing_balance, ROW_NUMBER() OVER (ORDER BY closing_balance DESC, loan_id) AS rn FROM loan_monthly_snapshot WHERE snapshot_date=DATE '2025-12-31' AND loan_status<>'Closed') WHERE rn<=5 ORDER BY rn"),
    P(2, 'For each state of property, the loan with the highest live balance at 2025-12-31 (tie `loan_id`). `state`, `loan_id`, `closing_balance`; sorted by state.',
      "SELECT d.state, s.loan_id, s.closing_balance FROM loan_monthly_snapshot s JOIN loan l USING (loan_id) JOIN property p ON p.property_id=l.property_id JOIN dim_postcode d ON d.postcode=p.postcode WHERE s.snapshot_date=DATE '2025-12-31' AND s.loan_status<>'Closed' QUALIFY ROW_NUMBER() OVER (PARTITION BY d.state ORDER BY s.closing_balance DESC, s.loan_id)=1 ORDER BY 1"),
    P(2, 'Monthly application counts for 2025 with the change vs the previous month. `month_start`, `apps`, `change`; sorted by month (change NULL for Jan).',
      "WITH m AS (SELECT CAST(date_trunc('month', application_date) AS DATE) AS ms, COUNT(*) AS n FROM loan_application WHERE application_date>=DATE '2025-01-01' GROUP BY 1) SELECT ms, n, n-LAG(n) OVER (ORDER BY ms) FROM m ORDER BY ms"),
    P(2, 'Running total of new lending ($, 0dp) by month for 2025. `month_start`, `running_total`; sorted by month.',
      "WITH m AS (SELECT CAST(date_trunc('month', origination_date) AS DATE) AS ms, SUM(original_amount) AS a FROM loan WHERE origination_date>=DATE '2025-01-01' AND origination_date<DATE '2026-01-01' GROUP BY 1) SELECT ms, ROUND(SUM(a) OVER (ORDER BY ms),0) FROM m ORDER BY ms"),
    P(3, "Each customer's second loan: `primary_customer_id`, `loan_id`, `origination_date` for customers with at least 2 loans (order by date then loan_id). Return the first 10 by customer id.",
      'SELECT primary_customer_id, loan_id, origination_date FROM loan QUALIFY ROW_NUMBER() OVER (PARTITION BY primary_customer_id ORDER BY origination_date, loan_id)=2 ORDER BY 1 LIMIT 10'),
    P(3, "Days between a customer's first and second loan: median across customers with 2+ loans (1dp). One number.",
      'SELECT ROUND(MEDIAN(d2-d1),1) FROM (SELECT MIN(origination_date) FILTER (WHERE rn=1) AS d1, MIN(origination_date) FILTER (WHERE rn=2) AS d2 FROM (SELECT primary_customer_id, origination_date, ROW_NUMBER() OVER (PARTITION BY primary_customer_id ORDER BY origination_date, loan_id) AS rn FROM loan) GROUP BY primary_customer_id) WHERE d2 IS NOT NULL'),
    P(3, '3-month moving average of 90+ DPD loan counts at month-ends of 2025 (use all history for the window). `snapshot_date`, `n90`, `ma3` (1dp); 2025 months only; sorted by date. Live loans.',
      "WITH m AS (SELECT snapshot_date, COUNT(*) AS n FROM loan_monthly_snapshot WHERE days_past_due>=90 AND loan_status<>'Closed' GROUP BY 1), w AS (SELECT snapshot_date, n, ROUND(AVG(n) OVER (ORDER BY snapshot_date ROWS BETWEEN 2 PRECEDING AND CURRENT ROW),1) AS ma FROM m) SELECT * FROM w WHERE snapshot_date>=DATE '2025-01-01' ORDER BY 1"),
    P(3, "Percentile of each product's average original loan size across products: `product_id`, `avg_amount` (0dp), `pct_rank` (2dp, ordered ascending); sorted by product_id.",
      'SELECT product_id, ROUND(AVG(original_amount),0), ROUND(PERCENT_RANK() OVER (ORDER BY AVG(original_amount)),2) FROM loan GROUP BY 1 ORDER BY 1'),
])
