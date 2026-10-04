from ._gen import *
MORE_FOR = 'cr03_roll_rates'
PROBLEMS = []
B = "CASE WHEN days_past_due=0 THEN 0 WHEN days_past_due<30 THEN 1 WHEN days_past_due<60 THEN 2 WHEN days_past_due<90 THEN 3 ELSE 4 END"
def pair(d1,d2,extra=""):
    return (f"WITH m AS (SELECT loan_id, snapshot_date, {B} AS b, loan_status, LEAD({B}) OVER (PARTITION BY loan_id ORDER BY snapshot_date) AS bn, LEAD(snapshot_date) OVER (PARTITION BY loan_id ORDER BY snapshot_date) AS dn FROM loan_monthly_snapshot) ")
months = ['2025-01-31','2025-02-28','2025-03-31','2025-04-30','2025-05-31','2025-06-30','2025-07-31','2025-08-31','2025-09-30','2025-10-31','2025-11-30']
nxt = ['2025-02-28','2025-03-31','2025-04-30','2025-05-31','2025-06-30','2025-07-31','2025-08-31','2025-09-30','2025-10-31','2025-11-30','2025-12-31']
for a,b in zip(months,nxt):
    PROBLEMS.append(P(2, f"Roll from Current: of loans at 0 DPD on {a} (live, with a row on {b}), the % that were behind (1+ DPD) on {b} (3 dp %). One number.",
      pair(a,b)+f"SELECT ROUND(100.0*COUNT(*) FILTER (WHERE bn>=1)/COUNT(*),3) FROM m WHERE snapshot_date=DATE '{a}' AND dn=DATE '{b}' AND loan_status<>'Closed' AND b=0"))
for a,b in zip(months,nxt):
    PROBLEMS.append(P(3, f"Cure rate: of live loans at 1-29 DPD on {a} with a row on {b}, the % at 0 DPD on {b} (1 dp %), and the number observed. `observed`, `cure_pct`.",
      pair(a,b)+f"SELECT COUNT(*), ROUND(100.0*COUNT(*) FILTER (WHERE bn=0)/COUNT(*),1) FROM m WHERE snapshot_date=DATE '{a}' AND dn=DATE '{b}' AND loan_status<>'Closed' AND b=1"))
for p in PURPOSES[:5]:
    PROBLEMS.append(P(3, f"Purpose `'{p}'`: transition counts 2025-11-30 -> 2025-12-31 as `from_bucket`, `to_bucket`, `loans` (buckets 0=current, 1=1-29, 2=30-59, 3=60-89, 4=90+; live loans with a December row). Sorted by from, to.",
      f"WITH m AS (SELECT s.loan_id, s.snapshot_date, {B.replace('days_past_due','s.days_past_due')} AS b, s.loan_status, LEAD({B.replace('days_past_due','s.days_past_due')}) OVER (PARTITION BY s.loan_id ORDER BY s.snapshot_date) AS bn, LEAD(s.snapshot_date) OVER (PARTITION BY s.loan_id ORDER BY s.snapshot_date) AS dn FROM loan_monthly_snapshot s JOIN loan l USING (loan_id) WHERE l.purpose='{p}') SELECT b, bn, COUNT(*) FROM m WHERE snapshot_date=DATE '2025-11-30' AND dn=DATE '2025-12-31' AND loan_status<>'Closed' GROUP BY 1,2 ORDER BY 1,2"))
