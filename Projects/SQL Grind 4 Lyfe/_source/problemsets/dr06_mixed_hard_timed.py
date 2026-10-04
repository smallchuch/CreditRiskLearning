from . import P

PRIMER = r"""
## Timed drill - interview conditions

The hardest mix: close to a senior analyst final round. Expect to combine windows, CTEs and careful definitions.

**Rules**
* Set a timer: **60 minutes** for 8 questions (about 8 min each).
* No notes, no looking at the solution. Ctrl-click the data dictionary only if you would be allowed a schema in the interview.
* Say your approach out loud (or write 2 lines of plan as a comment) BEFORE writing SQL: *grain? filters? joins? checks?*
* When time is up, stop. Run `grade dr06` and note your score and which questions ran over.
* Questions get harder as you go; skipping and returning is allowed (and realistic).

Scoring guide: 8/8 = ready | 6+ = solid | below 6 = redo the weak concept sets (the question numbers tell you which).
"""

CONCEPT = dict(id="dr06_mixed_hard_timed", title="DR06 - Timed drill: mixed hard set", primer=PRIMER, problems=[
    P(2, 'The month with the most originations in each year (ties earliest month). `yr`, `month_no`, `loans`; sorted by year.',
      'SELECT yr, mon, n FROM (SELECT year(origination_date) AS yr, month(origination_date) AS mon, COUNT(*) AS n, ROW_NUMBER() OVER (PARTITION BY year(origination_date) ORDER BY COUNT(*) DESC, month(origination_date)) AS rn FROM loan GROUP BY 1,2) WHERE rn=1 ORDER BY 1'),
    P(3, 'Customers who have 2+ loans and whose second loan was larger than the first. Count them. One number.',
      'SELECT COUNT(*) FROM (SELECT primary_customer_id, MAX(original_amount) FILTER (WHERE rn=1) AS a1, MAX(original_amount) FILTER (WHERE rn=2) AS a2 FROM (SELECT primary_customer_id, original_amount, ROW_NUMBER() OVER (PARTITION BY primary_customer_id ORDER BY origination_date, loan_id) AS rn FROM loan) GROUP BY 1) WHERE a2>a1'),
    P(3, 'Longest streak of consecutive months with 30+ DPD for any loan - and how many loans achieved that max streak. `max_streak`, `loans`.',
      'WITH g AS (SELECT loan_id, months_on_book - ROW_NUMBER() OVER (PARTITION BY loan_id ORDER BY months_on_book) AS grp FROM loan_monthly_snapshot WHERE days_past_due>=30), r AS (SELECT loan_id, grp, COUNT(*) AS run FROM g GROUP BY 1,2), m AS (SELECT loan_id, MAX(run) AS mx FROM r GROUP BY 1) SELECT MAX(mx), COUNT(*) FILTER (WHERE mx=(SELECT MAX(mx) FROM m)) FROM m'),
    P(3, 'For loans originated in 2022, what % were still open 36 months after origination (has a non-closed snapshot at MOB 36)? 1dp. One number.',
      "SELECT ROUND(100.0*COUNT(DISTINCT s.loan_id)/(SELECT COUNT(*) FROM loan WHERE year(origination_date)=2022),1) FROM loan_monthly_snapshot s JOIN loan l USING (loan_id) WHERE year(l.origination_date)=2022 AND s.months_on_book=36 AND s.loan_status<>'Closed'"),
    P(3, 'Customers who were ever 90+ DPD on a loan and still hold another live loan (not 90+) at 2025-12-31. Count distinct customers. One number.',
      "SELECT COUNT(DISTINCT l.primary_customer_id) FROM loan l WHERE EXISTS (SELECT 1 FROM loan_monthly_snapshot h WHERE h.loan_id=l.loan_id AND h.days_past_due>=90) AND EXISTS (SELECT 1 FROM loan l2 JOIN loan_monthly_snapshot s ON s.loan_id=l2.loan_id AND s.snapshot_date=DATE '2025-12-31' WHERE l2.primary_customer_id=l.primary_customer_id AND l2.loan_id<>l.loan_id AND s.loan_status<>'Closed' AND s.days_past_due<90)"),
    P(3, 'Contribution to ECL: the top 10 loans by ECL at 2025-12-31 and the % of total ECL they represent (2dp, as `top10_share_pct`) and their combined ECL (0dp). One row: `top10_ecl`, `top10_share_pct`.',
      "SELECT ROUND(SUM(e),0), ROUND(100*SUM(e)/(SELECT SUM(ecl_amount) FROM ecl_provision_quarterly WHERE reporting_date=DATE '2025-12-31'),2) FROM (SELECT ecl_amount AS e FROM ecl_provision_quarterly WHERE reporting_date=DATE '2025-12-31' ORDER BY ecl_amount DESC, loan_id LIMIT 10)"),
    P(3, 'Cohort retention matrix: for loans originated in H1 2022 (Jan-Jun), the % still open at MOB 6, 12, 18, 24. `mob`, `open_pct` (1dp); sorted by mob.',
      "WITH c AS (SELECT loan_id FROM loan WHERE origination_date>=DATE '2022-01-01' AND origination_date<DATE '2022-07-01') SELECT m.mob, ROUND(100.0*COUNT(DISTINCT s.loan_id)/(SELECT COUNT(*) FROM c),1) FROM (SELECT unnest([6,12,18,24]) AS mob) m LEFT JOIN (SELECT s.loan_id, s.months_on_book FROM loan_monthly_snapshot s JOIN c USING (loan_id) WHERE s.loan_status<>'Closed') s ON s.months_on_book=m.mob GROUP BY m.mob ORDER BY m.mob"),
    P(3, 'First-time defaulters by origination channel and year (2021-2024): number of loans whose first ever 90+ DPD happened within 24 months of origination, divided by loans originated - the 24-month default rate (2dp). `yr`, `broker_pct`, `branch_pct`, `digital_pct`, `mobile_pct`; sorted by year.',
      "WITH d AS (SELECT loan_id FROM loan_monthly_snapshot WHERE days_past_due>=90 AND months_on_book<=24 GROUP BY 1) SELECT year(l.origination_date), ROUND(100.0*COUNT(d.loan_id) FILTER (WHERE l.channel='Broker')/COUNT(*) FILTER (WHERE l.channel='Broker'),2), ROUND(100.0*COUNT(d.loan_id) FILTER (WHERE l.channel='Branch')/COUNT(*) FILTER (WHERE l.channel='Branch'),2), ROUND(100.0*COUNT(d.loan_id) FILTER (WHERE l.channel='Digital')/COUNT(*) FILTER (WHERE l.channel='Digital'),2), ROUND(100.0*COUNT(d.loan_id) FILTER (WHERE l.channel='Mobile Lender')/COUNT(*) FILTER (WHERE l.channel='Mobile Lender'),2) FROM loan l LEFT JOIN d ON d.loan_id=l.loan_id WHERE year(l.origination_date) BETWEEN 2021 AND 2024 GROUP BY 1 ORDER BY 1"),
])
