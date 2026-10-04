from ._gen import *
MORE_FOR = 'cr06_pricing_rate_shock'
PROBLEMS = []
for y in YEARS:
    PROBLEMS.append(P(1, f"Origination pricing in {y}: average origination rate (3 dp) for `'Fixed'` and `'Variable'` loans. `avg_fixed`, `avg_variable`.",
      f"SELECT ROUND(AVG(interest_rate_at_origination_pct) FILTER (WHERE rate_type='Fixed'),3), ROUND(AVG(interest_rate_at_origination_pct) FILTER (WHERE rate_type='Variable'),3) FROM loan WHERE {yr('origination_date',y)}"))
for q,(a,b) in enumerate([('2026-01-01','2026-04-01'),('2026-04-01','2026-07-01'),('2026-07-01','2026-10-01'),('2026-10-01','2027-01-01')],1):
    PROBLEMS.append(P(2, f"Fixed-rate cliff, 2026 Q{q}: live loans (2025-12-31) whose fixed term expires in the quarter - loans, balance (0 dp), balance-weighted current rate (3 dp). `loans`, `balance`, `wtd_rate`.",
      f"SELECT COUNT(*), ROUND(SUM(s.closing_balance),0), ROUND(SUM(s.closing_balance*s.interest_rate_pct)/SUM(s.closing_balance),3) FROM loan l JOIN loan_monthly_snapshot s ON s.loan_id=l.loan_id AND s.snapshot_date=DATE '2025-12-31' WHERE s.loan_status<>'Closed' AND l.fixed_rate_expiry_date>=DATE '{a}' AND l.fixed_rate_expiry_date<DATE '{b}'"))
for pp in (1,2,3):
    for rt in ('P&I',):
        PROBLEMS.append(P(3, f"Stress test +{pp}pp: for live P&I loans at 2025-12-31 with at least 12 months of term left, total monthly repayment now and at +{pp} percentage points (0 dp) and % increase (1 dp). Remaining term = `term_months - months_on_book`. `now_total`, `stress_total`, `increase_pct`.",
          f"WITH b AS (SELECT s.closing_balance AS p, s.interest_rate_pct/1200 AS r0, (s.interest_rate_pct+{pp})/1200 AS r1, l.term_months-s.months_on_book AS n FROM loan_monthly_snapshot s JOIN loan l USING (loan_id) WHERE s.snapshot_date=DATE '2025-12-31' AND s.loan_status<>'Closed' AND s.repayment_type='P&I' AND l.term_months-s.months_on_book>=12 AND s.interest_rate_pct>0) SELECT ROUND(SUM(p*r0/(1-POWER(1+r0,-n))),0), ROUND(SUM(p*r1/(1-POWER(1+r1,-n))),0), ROUND(100*(SUM(p*r1/(1-POWER(1+r1,-n)))/SUM(p*r0/(1-POWER(1+r0,-n)))-1),1) FROM b"))
for y in (2022,2023,2024,2025):
    PROBLEMS.append(P(2, f"Events in {y}: counts of each `loan_event` type (`event_type`, `events`); sorted by events descending then type.",
      f"SELECT event_type, COUNT(*) AS n FROM loan_event WHERE {yr('event_date',y)} GROUP BY 1 ORDER BY n DESC, 1"))
for p in EXT_PURPOSES:
    PROBLEMS.append(P(2, f"Purpose `'{p}'`: weighted average rate (3 dp) of the live book at each year-end 2022-2025. `snapshot_date`, `wtd_rate`; sorted by date.",
      f"SELECT s.snapshot_date, ROUND(SUM(s.closing_balance*s.interest_rate_pct)/SUM(s.closing_balance),3) FROM loan_monthly_snapshot s JOIN loan l USING (loan_id) WHERE l.purpose='{p}' AND s.loan_status<>'Closed' AND s.snapshot_date IN (DATE '2022-12-31',DATE '2023-12-31',DATE '2024-12-31',DATE '2025-12-31') GROUP BY 1 ORDER BY 1"))
