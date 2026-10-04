from ._gen import *
MORE_FOR = 'cr02_arrears_delinquency'
PROBLEMS = []
SJ = "FROM loan_monthly_snapshot s JOIN loan l USING (loan_id)"
for y in range(2019,2026):
    PROBLEMS.append(P(2, f"Arrears at {y}-12-31 (live): 30+ DPD and 90+ DPD rates by count and by balance (2 dp %). `c30`, `c90`, `b30`, `b90`.",
      f"SELECT ROUND(100.0*COUNT(*) FILTER (WHERE days_past_due>=30)/COUNT(*),2), ROUND(100.0*COUNT(*) FILTER (WHERE days_past_due>=90)/COUNT(*),2), ROUND(100*SUM(closing_balance) FILTER (WHERE days_past_due>=30)/SUM(closing_balance),2), ROUND(100*SUM(closing_balance) FILTER (WHERE days_past_due>=90)/SUM(closing_balance),2) FROM loan_monthly_snapshot WHERE snapshot_date=DATE '{y}-12-31' AND loan_status<>'Closed'"))
for s in STATES:
    PROBLEMS.append(P(2, f"Property state `'{s}'` at 2025-12-31: live loans, loans 30+ DPD, 30+ rate (count, 2 dp) and dollars in arrears (0 dp). `loans`, `loans_30plus`, `rate_pct`, `arrears_dollars`.",
      f"SELECT COUNT(*), COUNT(*) FILTER (WHERE s.days_past_due>=30), ROUND(100.0*COUNT(*) FILTER (WHERE s.days_past_due>=30)/COUNT(*),2), ROUND(SUM(s.arrears_amount),0) FROM loan_monthly_snapshot s JOIN loan l USING (loan_id) JOIN property pr ON pr.property_id=l.property_id JOIN dim_postcode d ON d.postcode=pr.postcode WHERE {LIVES} AND d.state='{s}'"))
for p in PURPOSES:
    PROBLEMS.append(P(2, f"Purpose `'{p}'`: the arrears distribution at 2025-12-31 by official bucket (`ref_arrears_bucket`): `bucket_name`, `loans`, `balance` (0 dp); sorted by `bucket_id`.",
      f"SELECT b.bucket_name, COUNT(*), ROUND(SUM(s.closing_balance),0) FROM loan_monthly_snapshot s JOIN loan l USING (loan_id) JOIN ref_arrears_bucket b ON s.days_past_due BETWEEN b.dpd_from AND COALESCE(b.dpd_to,99999) WHERE {LIVES} AND l.purpose='{p}' GROUP BY b.bucket_id, b.bucket_name ORDER BY b.bucket_id"))
for c in CHANNELS:
    PROBLEMS.append(P(3, f"Channel `'{c}'`: the 30+ DPD rate (count, 2 dp) at each year-end 2022-2025. `snapshot_date`, `rate_pct`; sorted by date.",
      f"SELECT s.snapshot_date, ROUND(100.0*COUNT(*) FILTER (WHERE s.days_past_due>=30)/COUNT(*),2) FROM loan_monthly_snapshot s JOIN loan l USING (loan_id) WHERE l.channel='{c}' AND s.loan_status<>'Closed' AND s.snapshot_date IN (DATE '2022-12-31',DATE '2023-12-31',DATE '2024-12-31',DATE '2025-12-31') GROUP BY 1 ORDER BY 1"))
for y in (2020,2022,2024):
    PROBLEMS.append(P(3, f"Hardship effect at {y}-12-31: 30+ DPD loans split by `hardship_flag` (live), with each group's balance (0 dp). `hardship_flag`, `loans`, `balance`; sorted by flag.",
      f"SELECT hardship_flag, COUNT(*), ROUND(SUM(closing_balance),0) FROM loan_monthly_snapshot WHERE snapshot_date=DATE '{y}-12-31' AND loan_status<>'Closed' AND days_past_due>=30 GROUP BY 1 ORDER BY 1"))
