from ._gen import *
MORE_FOR = '17_performance_rewrites'
PROBLEMS = []
for y in YEARS:
    PROBLEMS.append(P(1, f"Naive: `WHERE year(application_date) = {y}`. Rewrite as a half-open date range and return the number of applications in {y}. One number.",
      f"SELECT COUNT(*) FROM loan_application WHERE {yr('application_date',y)}"))
for p in EXT_PURPOSES:
    PROBLEMS.append(P(2, f"Naive: `SELECT DISTINCT` after joining `loan` to `loan_borrower`. Rewrite with EXISTS: how many `'{p}'` loans have a co-applicant? One number.",
      f"SELECT COUNT(*) FROM loan l WHERE l.purpose='{p}' AND EXISTS (SELECT 1 FROM loan_borrower b WHERE b.loan_id=l.loan_id AND b.borrower_role='Co-applicant')"))
for c in CHANNELS:
    PROBLEMS.append(P(2, f"Naive: correlated subquery per row to get each customer's loan count. Rewrite with a pre-aggregation: customers with 3 or more loans via `'{c}'`. Count. One number.",
      f"SELECT COUNT(*) FROM (SELECT primary_customer_id FROM loan WHERE channel='{c}' GROUP BY 1 HAVING COUNT(*)>=3)"))
for y in (2021,2023,2025):
    PROBLEMS.append(P(2, f"Naive: join all snapshot rows then filter. Filter the snapshot to {y}-12-31 first, then join: live balance (0 dp) by `channel`. `channel`, `balance`; sorted by channel.",
      f"WITH s AS (SELECT loan_id, closing_balance FROM loan_monthly_snapshot WHERE snapshot_date=DATE '{y}-12-31' AND loan_status<>'Closed') SELECT l.channel, ROUND(SUM(s.closing_balance),0) FROM s JOIN loan l USING (loan_id) GROUP BY 1 ORDER BY 1"))
for k in (3,5,10):
    PROBLEMS.append(P(3, f"Naive: self-join for the latest status event. Use `QUALIFY ROW_NUMBER()` to get each application's latest event (by ts, then event_id) and count how many of the latest events are `'Settled'`... for applications 1 to {k*1000}. One number.",
      f"SELECT COUNT(*) FROM (SELECT status FROM application_status_history WHERE application_id<={k*1000} QUALIFY ROW_NUMBER() OVER (PARTITION BY application_id ORDER BY status_ts DESC, event_id DESC)=1) WHERE status='Settled'"))
