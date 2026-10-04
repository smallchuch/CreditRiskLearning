from . import P

PRIMER = r"""
## Timed drill - interview conditions

Case-study style, as in a bank's analytics interview: definitions matter. Write down your definition of the live book first.

**Rules**
* Set a timer: **45 minutes** for 9 questions (about 5 min each).
* No notes, no looking at the solution. Ctrl-click the data dictionary only if you would be allowed a schema in the interview.
* Say your approach out loud (or write 2 lines of plan as a comment) BEFORE writing SQL: *grain? filters? joins? checks?*
* When time is up, stop. Run `grade dr04` and note your score and which questions ran over.
* Questions get harder as you go; skipping and returning is allowed (and realistic).

Scoring guide: 9/9 = ready | 7+ = solid | below 7 = redo the weak concept sets (the question numbers tell you which).
"""

CONCEPT = dict(id="dr04_credit_analytics_timed", title="DR04 - Timed drill: credit-risk analytics case", primer=PRIMER, problems=[
    P(1, 'Live book at 2025-12-31: loans and balance (0dp). `loans`, `balance`.',
      "SELECT COUNT(*), ROUND(SUM(closing_balance),0) FROM loan_monthly_snapshot WHERE snapshot_date=DATE '2025-12-31' AND loan_status<>'Closed'"),
    P(2, '90+ DPD rate by balance (2dp %) at each year-end 2021-2025. `snapshot_date`, `rate_pct`; sorted by date.',
      "SELECT snapshot_date, ROUND(100*SUM(closing_balance) FILTER (WHERE days_past_due>=90)/SUM(closing_balance),2) FROM loan_monthly_snapshot WHERE snapshot_date IN (DATE '2021-12-31', DATE '2022-12-31', DATE '2023-12-31', DATE '2024-12-31', DATE '2025-12-31') AND loan_status<>'Closed' GROUP BY 1 ORDER BY 1"),
    P(2, 'Investor vs owner-occupier 30+ DPD rate (count, 2dp) at 2025-12-31. `occupancy`, `rate_pct`; sorted by occupancy.',
      "SELECT p.occupancy, ROUND(100.0*COUNT(*) FILTER (WHERE s.days_past_due>=30)/COUNT(*),2) FROM loan_monthly_snapshot s JOIN loan l USING (loan_id) JOIN dim_product p ON p.product_id=l.product_id WHERE s.snapshot_date=DATE '2025-12-31' AND s.loan_status<>'Closed' GROUP BY 1 ORDER BY 1"),
    P(2, 'Which origination year has the worst ever-90+ rate? Return the year and rate (2dp) - top 1. `yr`, `ever90_pct`.',
      'SELECT yr, p FROM (SELECT year(l.origination_date) AS yr, ROUND(100.0*COUNT(e.loan_id)/COUNT(*),2) AS p FROM loan l LEFT JOIN (SELECT loan_id FROM loan_monthly_snapshot GROUP BY 1 HAVING MAX(days_past_due)>=90) e ON e.loan_id=l.loan_id GROUP BY 1) ORDER BY p DESC, yr LIMIT 1'),
    P(3, 'Roll rate: of live loans at 30-59 DPD at 2025-11-30, what % were 60+ DPD at 2025-12-31 (non-closed, 1dp)? One number.',
      "SELECT ROUND(100.0*COUNT(*) FILTER (WHERE b.days_past_due>=60)/COUNT(*),1) FROM loan_monthly_snapshot a JOIN loan_monthly_snapshot b ON b.loan_id=a.loan_id AND b.snapshot_date=DATE '2025-12-31' WHERE a.snapshot_date=DATE '2025-11-30' AND a.loan_status<>'Closed' AND b.loan_status<>'Closed' AND a.days_past_due BETWEEN 30 AND 59"),
    P(3, 'Stage 2 + 3 share of live EAD at 2025-12-31 (2dp %). One number.',
      "SELECT ROUND(100*SUM(ead) FILTER (WHERE ifrs9_stage>=2)/SUM(ead),2) FROM ecl_provision_quarterly WHERE reporting_date=DATE '2025-12-31'"),
    P(3, 'Estimate the payment-shock exposure of fixed loans expiring in the next 6 months (after 2025-12-31, up to 2026-06-30): count and balance (0dp). `loans`, `balance`.',
      "SELECT COUNT(*), ROUND(SUM(s.closing_balance),0) FROM loan l JOIN loan_monthly_snapshot s ON s.loan_id=l.loan_id AND s.snapshot_date=DATE '2025-12-31' WHERE s.loan_status<>'Closed' AND l.fixed_rate_expiry_date>DATE '2025-12-31' AND l.fixed_rate_expiry_date<=DATE '2026-06-30'"),
    P(3, 'Which broker has the highest 90-plus DPD balance rate among brokers with live balance above $100m? `broker_id`, `rate_pct` (2dp) - one row.',
      "SELECT broker_id, ROUND(100*SUM(closing_balance) FILTER (WHERE days_past_due>=90)/SUM(closing_balance),2) AS r FROM loan_monthly_snapshot s JOIN loan l USING (loan_id) WHERE s.snapshot_date=DATE '2025-12-31' AND s.loan_status<>'Closed' AND l.broker_id IS NOT NULL GROUP BY 1 HAVING SUM(closing_balance)>100000000 ORDER BY r DESC, 1 LIMIT 1"),
    P(3, 'New lending by quarter of 2025 alongside the number of loans closed in each quarter. Return `quarter` (1-4), `new_amount` (0dp), `closed_loans`; sorted by quarter.',
      'SELECT q, ROUND(a,0), c FROM (SELECT quarter(origination_date) AS q, SUM(original_amount) AS a FROM loan WHERE year(origination_date)=2025 GROUP BY 1) n JOIN (SELECT quarter(closed_date) AS q2, COUNT(*) AS c FROM loan WHERE year(closed_date)=2025 GROUP BY 1) k ON k.q2=n.q ORDER BY 1'),
])
