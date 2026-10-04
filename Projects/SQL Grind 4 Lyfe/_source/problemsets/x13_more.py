from ._gen import *
MORE_FOR = '13_pivot_conditional'
PROBLEMS = []
for p in EXT_PURPOSES:
    PROBLEMS.append(P(2, f"`'{p}'` loans by origination year (rows) with one column per channel (Broker, Branch, Digital, Mobile Lender) - conditional counts. `yr`, `broker`, `branch`, `digital`, `mobile`; sorted by year.",
      f"SELECT year(origination_date), " + ", ".join(f"COUNT(*) FILTER (WHERE channel='{c}')" for c in CHANNELS) + f" FROM loan WHERE purpose='{p}' GROUP BY 1 ORDER BY 1"))
for y in YEARS:
    PROBLEMS.append(P(2, f"Applications lodged in {y}: one row per `channel` with columns `settled`, `declined`, `withdrawn`, `lapsed` (counts by `current_status`). Sorted by channel.",
      f"SELECT channel, " + ", ".join(f"COUNT(*) FILTER (WHERE current_status='{s}')" for s in ['Settled','Declined','Withdrawn','Lapsed']) + f" FROM loan_application WHERE {yr('application_date',y)} GROUP BY 1 ORDER BY 1"))
for c in CHANNELS:
    PROBLEMS.append(P(2, f"`'{c}'` loans: per `rate_type` the number of loans in LVR groups `le70`, `70_80`, `80_90`, `gt90` (upper bounds inclusive). `rate_type`, four counts; sorted by rate_type.",
      f"SELECT rate_type, COUNT(*) FILTER (WHERE lvr_at_origination_pct<=70), COUNT(*) FILTER (WHERE lvr_at_origination_pct>70 AND lvr_at_origination_pct<=80), COUNT(*) FILTER (WHERE lvr_at_origination_pct>80 AND lvr_at_origination_pct<=90), COUNT(*) FILTER (WHERE lvr_at_origination_pct>90) FROM loan WHERE channel='{c}' GROUP BY 1 ORDER BY 1"))
for y in (2021,2022,2023,2024,2025):
    PROBLEMS.append(P(3, f"Arrears at {y}-12-31 (live loans): one row per `repayment_type` with columns `current`, `d1_29`, `d30_89`, `d90plus` (loan counts) and `rate_30plus` (% 30+, 2 dp). Sorted by repayment_type.",
      f"SELECT repayment_type, COUNT(*) FILTER (WHERE days_past_due=0), COUNT(*) FILTER (WHERE days_past_due BETWEEN 1 AND 29), COUNT(*) FILTER (WHERE days_past_due BETWEEN 30 AND 89), COUNT(*) FILTER (WHERE days_past_due>=90), ROUND(100.0*COUNT(*) FILTER (WHERE days_past_due>=30)/COUNT(*),2) FROM loan_monthly_snapshot WHERE snapshot_date=DATE '{y}-12-31' AND loan_status<>'Closed' GROUP BY 1 ORDER BY 1"))
PROBLEMS += [
 P(3, "DuckDB `PIVOT`: 2025 loans by `purpose` (rows) and `channel` (columns, listed with `IN`). Return the pivoted table sorted by purpose.",
   "SELECT * FROM (PIVOT (SELECT purpose, channel FROM loan WHERE origination_date >= DATE '2025-01-01') ON channel IN ('Broker','Branch','Digital','Mobile Lender') USING COUNT(*) GROUP BY purpose) ORDER BY purpose"),
 P(3, "DuckDB `UNPIVOT`: from a one-row table of counts `(broker, branch, digital, mobile)` for 2025 loans build a tall `channel`, `loans` table with `UNPIVOT`. Sorted by channel.",
   "WITH w AS (SELECT COUNT(*) FILTER (WHERE channel='Broker') AS broker, COUNT(*) FILTER (WHERE channel='Branch') AS branch, COUNT(*) FILTER (WHERE channel='Digital') AS digital, COUNT(*) FILTER (WHERE channel='Mobile Lender') AS mobile FROM loan WHERE origination_date >= DATE '2025-01-01') SELECT channel, loans FROM (UNPIVOT w ON broker, branch, digital, mobile INTO NAME channel VALUE loans) ORDER BY channel"),
]
