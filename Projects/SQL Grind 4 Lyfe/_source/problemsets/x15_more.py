from ._gen import *
MORE_FOR = '15_time_series_cohorts'
PROBLEMS = []
for y in range(2019,2025):
    PROBLEMS.append(P(2, f"The {y} vintage: % of loans (non-closed at that point) that are 30+ DPD at months-on-book 12, and the number of loans observed. `loans`, `pct_30plus` (2 dp).",
      f"SELECT COUNT(*), ROUND(100.0*COUNT(*) FILTER (WHERE s.days_past_due>=30)/COUNT(*),2) FROM loan_monthly_snapshot s JOIN loan l USING (loan_id) WHERE {yr('l.origination_date',y)} AND s.months_on_book=12 AND s.loan_status<>'Closed'"))
for y in range(2019,2024):
    PROBLEMS.append(P(2, f"Attrition: of the loans originated in {y}, the % still open at 24 months on book (has a non-closed snapshot at MOB 24; 1 dp). One number.",
      f"SELECT ROUND(100.0*COUNT(DISTINCT s.loan_id)/(SELECT COUNT(*) FROM loan WHERE {yr('origination_date',y)}),1) FROM loan_monthly_snapshot s JOIN loan l USING (loan_id) WHERE {yr('l.origination_date',y)} AND s.months_on_book=24 AND s.loan_status<>'Closed'"))
for y in range(2019,2026):
    PROBLEMS.append(P(1, f"Live book at {y}-12-31: number of non-closed loans and total balance (0 dp). `loans`, `balance`.",
      f"SELECT COUNT(*), ROUND(SUM(closing_balance),0) FROM loan_monthly_snapshot WHERE snapshot_date=DATE '{y}-12-31' AND loan_status<>'Closed'"))
for y in (2021,2022,2023,2024,2025):
    PROBLEMS.append(P(3, f"Balance roll-forward for December {y}: opening balance (live, {y}-11-30), new loans originated in December {y}, closing balance (live, {y}-12-31) and implied run-off = opening + new - closing (0 dp). `opening`, `new_lending`, `closing`, `implied_runoff`.",
      f"SELECT ROUND(o,0), ROUND(n,0), ROUND(c,0), ROUND(o+n-c,0) FROM (SELECT (SELECT SUM(closing_balance) FROM loan_monthly_snapshot WHERE snapshot_date=DATE '{y}-11-30' AND loan_status<>'Closed') AS o, (SELECT SUM(original_amount) FROM loan WHERE origination_date>=DATE '{y}-12-01' AND origination_date<=DATE '{y}-12-31') AS n, (SELECT SUM(closing_balance) FROM loan_monthly_snapshot WHERE snapshot_date=DATE '{y}-12-31' AND loan_status<>'Closed') AS c)"))
for p in EXT_PURPOSES:
    PROBLEMS.append(P(3, f"Vintage curve for `'{p}'` loans originated in 2022: the 30+ DPD rate (2 dp, non-closed) at MOB 6, 12, 18 and 24 as four columns. `mob6`, `mob12`, `mob18`, `mob24`.",
      f"SELECT " + ", ".join(f"ROUND(100.0*COUNT(*) FILTER (WHERE s.months_on_book={m} AND s.days_past_due>=30)/NULLIF(COUNT(*) FILTER (WHERE s.months_on_book={m}),0),2)" for m in (6,12,18,24)) + f" FROM loan_monthly_snapshot s JOIN loan l USING (loan_id) WHERE l.purpose='{p}' AND {yr('l.origination_date',2022)} AND s.loan_status<>'Closed'"))
