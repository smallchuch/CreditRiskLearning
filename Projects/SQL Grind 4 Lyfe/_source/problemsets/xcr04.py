from ._gen import *
MORE_FOR = 'cr04_vintage_analysis'
PROBLEMS = []
E = "(SELECT loan_id FROM loan_monthly_snapshot GROUP BY 1 HAVING MAX(days_past_due)>=90)"
for y in range(2019,2025):
    PROBLEMS.append(P(2, f"The {y} vintage by channel: loans and ever-90+ rate (2 dp %). `channel`, `loans`, `ever90_pct`; sorted by channel.",
      f"SELECT l.channel, COUNT(*), ROUND(100.0*COUNT(e.loan_id)/COUNT(*),2) FROM loan l LEFT JOIN {E} e ON e.loan_id=l.loan_id WHERE {yr('l.origination_date',y)} GROUP BY 1 ORDER BY 1"))
for p in EXT_PURPOSES:
    PROBLEMS.append(P(2, f"Purpose `'{p}'`: 30+ DPD rate at MOB 12 (count, non-closed, 2 dp %) by origination year 2019-2024. `yr`, `loans`, `pct_30plus`; sorted by year.",
      f"SELECT year(l.origination_date), COUNT(*), ROUND(100.0*COUNT(*) FILTER (WHERE s.days_past_due>=30)/COUNT(*),2) FROM loan_monthly_snapshot s JOIN loan l USING (loan_id) WHERE l.purpose='{p}' AND s.months_on_book=12 AND s.loan_status<>'Closed' AND year(l.origination_date) BETWEEN 2019 AND 2024 GROUP BY 1 ORDER BY 1"))
for c in CHANNELS:
    PROBLEMS.append(P(3, f"Early payment default for `'{c}'`: % of loans reaching 30+ DPD within their first 6 months, by origination year 2019-2024 (2 dp %). `yr`, `loans`, `epd_pct`; sorted by year.",
      f"SELECT year(l.origination_date), COUNT(*), ROUND(100.0*COUNT(e.loan_id)/COUNT(*),2) FROM loan l LEFT JOIN (SELECT DISTINCT loan_id FROM loan_monthly_snapshot WHERE months_on_book<=6 AND days_past_due>=30) e ON e.loan_id=l.loan_id WHERE l.channel='{c}' AND year(l.origination_date) BETWEEN 2019 AND 2024 GROUP BY 1 ORDER BY 1"))
for lo,hi in [(0,70),(70,80),(80,90),(90,200)]:
    PROBLEMS.append(P(3, f"Origination LVR above {lo} and up to {hi}: the ever-90+ rate by origination year 2019-2024 (2 dp %). `yr`, `loans`, `ever90_pct`; sorted by year.",
      f"SELECT year(l.origination_date), COUNT(*), ROUND(100.0*COUNT(e.loan_id)/COUNT(*),2) FROM loan l LEFT JOIN {E} e ON e.loan_id=l.loan_id WHERE l.lvr_at_origination_pct>{lo} AND l.lvr_at_origination_pct<={hi} AND year(l.origination_date) BETWEEN 2019 AND 2024 GROUP BY 1 ORDER BY 1"))
