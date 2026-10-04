from . import P

PRIMER = r"""
## Timed drill - interview conditions

Fundamentals under pressure: filters, joins, grouping, NULLs, dates.

**Rules**
* Set a timer: **30 minutes** for 8 questions (about 4 min each).
* No notes, no looking at the solution. Ctrl-click the data dictionary only if you would be allowed a schema in the interview.
* Say your approach out loud (or write 2 lines of plan as a comment) BEFORE writing SQL: *grain? filters? joins? checks?*
* When time is up, stop. Run `grade dr01` and note your score and which questions ran over.
* Questions get harder as you go; skipping and returning is allowed (and realistic).

Scoring guide: 8/8 = ready | 6+ = solid | below 6 = redo the weak concept sets (the question numbers tell you which).
"""

CONCEPT = dict(id="dr01_warmup_timed", title="DR01 - Timed drill: warm-up (core skills)", primer=PRIMER, problems=[
    P(1, 'How many loans were originated in 2025 and what is their total original amount (0dp)? Return `loans`, `total_amount`.',
      "SELECT COUNT(*), ROUND(SUM(original_amount),0) FROM loan WHERE origination_date>=DATE '2025-01-01' AND origination_date<DATE '2026-01-01'"),
    P(1, 'List the 5 product names with the most loans. Return `product_name`, `loans`; sorted by loans descending, then name.',
      'SELECT p.product_name, COUNT(*) AS n FROM loan l JOIN dim_product p USING (product_id) GROUP BY 1 ORDER BY n DESC, 1 LIMIT 5'),
    P(1, 'Percentage of applications that were declined (of all applications), 1dp. One number.',
      "SELECT ROUND(100.0*COUNT(*) FILTER (WHERE decision='Declined')/COUNT(*),1) FROM loan_application"),
    P(2, 'Customers with no loans at all: how many? One number.',
      'SELECT COUNT(*) FROM customer c WHERE NOT EXISTS (SELECT 1 FROM loan l WHERE l.primary_customer_id=c.customer_id) AND NOT EXISTS (SELECT 1 FROM loan_borrower b WHERE b.customer_id=c.customer_id)'),
    P(2, 'Average days between application and decision by channel (1dp), only decided applications. `channel`, `avg_days`; sorted by channel.',
      'SELECT channel, ROUND(AVG(decision_date-application_date),1) FROM loan_application WHERE decision_date IS NOT NULL GROUP BY 1 ORDER BY 1'),
    P(2, 'Which 3 states (by property postcode) have the highest total live balance at 2025-12-31? `state`, `balance` (0dp); sorted by balance descending.',
      "SELECT d.state, ROUND(SUM(s.closing_balance),0) AS b FROM loan_monthly_snapshot s JOIN loan l USING (loan_id) JOIN property p ON p.property_id=l.property_id JOIN dim_postcode d ON d.postcode=p.postcode WHERE s.snapshot_date=DATE '2025-12-31' AND s.loan_status<>'Closed' GROUP BY 1 ORDER BY b DESC LIMIT 3"),
    P(2, 'Brokers with more than 100 loans and an average LVR above 70. `broker_id`, `loans`, `avg_lvr` (1dp); sorted by loans descending, then id.',
      'SELECT broker_id, COUNT(*) AS n, ROUND(AVG(lvr_at_origination_pct),1) FROM loan WHERE broker_id IS NOT NULL GROUP BY 1 HAVING COUNT(*)>100 AND AVG(lvr_at_origination_pct)>70 ORDER BY n DESC, 1'),
    P(2, 'Number of loans per number of borrowers (1 borrower, 2 borrowers). `borrowers`, `loans`; sorted by borrowers.',
      'SELECT n, COUNT(*) FROM (SELECT loan_id, COUNT(*) AS n FROM loan_borrower GROUP BY 1) GROUP BY 1 ORDER BY 1'),
])
