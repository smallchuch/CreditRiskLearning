from ._gen import *
MORE_FOR = '05_aggregation'
PROBLEMS = []
DIMS = [("purpose","purpose"),("channel","channel"),("rate_type","rate_type"),("product_id","product_id"),("origination year","year(origination_date)"),("loan_status","loan_status")]
MEAS = [("the number of loans and the total original amount (0 dp)", "COUNT(*), ROUND(SUM(original_amount),0)", 1),
        ("the average original amount (0 dp) and the average origination LVR (1 dp)", "ROUND(AVG(original_amount),0), ROUND(AVG(lvr_at_origination_pct),1)", 1),
        ("the smallest and largest original amount", "MIN(original_amount), MAX(original_amount)", 1),
        ("the share of all loans (1 dp %) - hint: `COUNT(*)*100.0/SUM(COUNT(*)) OVER ()`", "ROUND(COUNT(*)*100.0/SUM(COUNT(*)) OVER (),1)", 2),
        ("the average interest rate at origination (3 dp) and the average term in months (1 dp)", "ROUND(AVG(interest_rate_at_origination_pct),3), ROUND(AVG(term_months),1)", 2)]
for dn,d in DIMS:
    for mt,me,lv in MEAS:
        PROBLEMS.append(P(lv, f"For each {dn} return {mt}. Return the {dn} first; sorted by it.",
          f"SELECT {d}, {me} FROM loan GROUP BY 1 ORDER BY 1"))
for n in (500,1000,2000):
    PROBLEMS.append(P(2, f"Origination years in which more than {n*5} loans were written: `yr`, `loans`; sorted by year." if n==500 else f"Product ids with more than {n} loans: `product_id`, `loans`; sorted by product_id.",
      "SELECT year(origination_date), COUNT(*) FROM loan GROUP BY 1 HAVING COUNT(*)>2500 ORDER BY 1" if n==500 else f"SELECT product_id, COUNT(*) FROM loan GROUP BY 1 HAVING COUNT(*)>{n} ORDER BY 1"))
for c in CHANNELS:
    PROBLEMS.append(P(2, f"For `'{c}'` loans: the count by purpose, with the % of the channel's loans (1 dp). `purpose`, `loans`, `pct`; sorted by `purpose`.",
      f"SELECT purpose, COUNT(*), ROUND(100.0*COUNT(*)/SUM(COUNT(*)) OVER (),1) FROM loan WHERE channel='{c}' GROUP BY 1 ORDER BY 1"))
for y in (2021,2023,2025):
    PROBLEMS.append(P(3, f"For {y} originations: per `purpose` the count, total amount (0 dp), and the `COUNT(*) FILTER` of loans with LVR above 80. `purpose`, `loans`, `amount`, `lvr_gt80`; sorted by `purpose`.",
      f"SELECT purpose, COUNT(*), ROUND(SUM(original_amount),0), COUNT(*) FILTER (WHERE lvr_at_origination_pct>80) FROM loan WHERE {yr('origination_date',y)} GROUP BY 1 ORDER BY 1"))
