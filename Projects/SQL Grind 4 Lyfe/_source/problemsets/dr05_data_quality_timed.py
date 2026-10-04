from . import P

PRIMER = r"""
## Timed drill - interview conditions

You've been handed an unfamiliar extract. Find the problems fast. Each question is a typical data-validation ask.

**Rules**
* Set a timer: **40 minutes** for 9 questions (about 4 min each).
* No notes, no looking at the solution. Ctrl-click the data dictionary only if you would be allowed a schema in the interview.
* Say your approach out loud (or write 2 lines of plan as a comment) BEFORE writing SQL: *grain? filters? joins? checks?*
* When time is up, stop. Run `grade dr05` and note your score and which questions ran over.
* Questions get harder as you go; skipping and returning is allowed (and realistic).

Scoring guide: 9/9 = ready | 7+ = solid | below 7 = redo the weak concept sets (the question numbers tell you which).
"""

CONCEPT = dict(id="dr05_data_quality_timed", title="DR05 - Timed drill: dirty data", primer=PRIMER, problems=[
    P(1, 'Duplicate applications: pairs of applications by the same `primary_customer_id` on the same `application_date` for the same `requested_amount`. Count the groups. One number.',
      'SELECT COUNT(*) FROM (SELECT 1 FROM loan_application GROUP BY primary_customer_id, application_date, requested_amount HAVING COUNT(*)>1)'),
    P(2, 'Customers with an impossible age at 2025-12-31 (under 18 or over 100) among those with a DOB. One number.',
      "SELECT COUNT(*) FROM customer WHERE date_of_birth IS NOT NULL AND (date_diff('year', date_of_birth, DATE '2025-12-31')<18 OR date_diff('year', date_of_birth, DATE '2025-12-31')>100)"),
    P(2, 'Loans where `maturity_date` is before `origination_date` or `term_months` <= 0. One number.',
      'SELECT COUNT(*) FROM loan WHERE maturity_date<origination_date OR term_months<=0'),
    P(2, 'Rows in `loan_monthly_snapshot` with a negative balance or `days_past_due` < 0. One number.',
      'SELECT COUNT(*) FROM loan_monthly_snapshot WHERE closing_balance<0 OR days_past_due<0'),
    P(2, 'Interest rates outside 1%-15% in the snapshot (non-closed). One number.',
      "SELECT COUNT(*) FROM loan_monthly_snapshot WHERE loan_status<>'Closed' AND (interest_rate_pct<1 OR interest_rate_pct>15)"),
    P(3, "Status events out of order: applications where a 'Settled' event timestamp is before the application's 'Submitted' timestamp (use MIN per status). Count. One number.",
      "WITH s AS (SELECT application_id, MIN(status_ts) FILTER (WHERE status='Submitted') AS a, MIN(status_ts) FILTER (WHERE status='Settled') AS b FROM application_status_history GROUP BY 1) SELECT COUNT(*) FROM s WHERE b<a"),
    P(3, 'Applications whose `current_status` disagrees with the LAST event in `application_status_history` (latest by ts then event_id). Count. One number. (Some disagreement is expected from duplicate loads - do you understand why?)',
      'SELECT COUNT(*) FROM loan_application a JOIN (SELECT application_id, status FROM application_status_history QUALIFY ROW_NUMBER() OVER (PARTITION BY application_id ORDER BY status_ts DESC, event_id DESC)=1) h USING (application_id) WHERE a.current_status<>h.status'),
    P(3, 'Customers whose `postcode` is not in `dim_postcode`. Count and the % of customers (2dp). `customers`, `pct`.',
      'SELECT COUNT(*), ROUND(100.0*COUNT(*)/(SELECT COUNT(*) FROM customer),2) FROM customer c WHERE NOT EXISTS (SELECT 1 FROM dim_postcode p WHERE p.postcode=c.postcode)'),
    P(3, 'Same person, different customer ids: pairs sharing the same cleaned email (lowercase, trimmed) - the number of customer rows that share an email with at least one other customer. One number.',
      'SELECT COUNT(*) FROM customer WHERE email IS NOT NULL AND LOWER(TRIM(email)) IN (SELECT LOWER(TRIM(email)) FROM customer WHERE email IS NOT NULL GROUP BY 1 HAVING COUNT(*)>1)'),
])
