from ._gen import *
MORE_FOR = '09_ctes'
PROBLEMS = []
for y in YEARS:
    PROBLEMS.append(P(2, f"CTE of monthly loan counts for {y}; return only the months above that year's monthly average. `month_no`, `loans`; sorted by month.",
      f"WITH m AS (SELECT month(origination_date) AS mon, COUNT(*) AS n FROM loan WHERE {yr('origination_date',y)} GROUP BY 1) SELECT mon, n FROM m WHERE n > (SELECT AVG(n) FROM m) ORDER BY 1"))
for p in EXT_PURPOSES:
    PROBLEMS.append(P(3, f"CTE + window: within `'{p}'` loans, the 3 products with the largest total original amount. `product_id`, `total` (0 dp), `rnk`; sorted by rnk.",
      f"WITH t AS (SELECT product_id, SUM(original_amount) AS s FROM loan WHERE purpose='{p}' GROUP BY 1) SELECT product_id, ROUND(s,0), rnk FROM (SELECT product_id, s, ROW_NUMBER() OVER (ORDER BY s DESC, product_id) AS rnk FROM t) WHERE rnk<=3 ORDER BY rnk"))
for y in (2019,2021,2023,2025):
    PROBLEMS.append(P(2, f"Recursive date spine: all month-end dates of {y} (12 rows) built with a recursive CTE using `last_day(prev + INTERVAL 1 MONTH)`. Return `month_end`, sorted.",
      f"WITH RECURSIVE d(m) AS (SELECT DATE '{y}-01-31' UNION ALL SELECT last_day(m + INTERVAL 1 MONTH) FROM d WHERE m < DATE '{y}-11-30') SELECT CAST(m AS DATE) FROM d ORDER BY 1"))
for n in (10,15,20):
    PROBLEMS.append(P(2, f"Recursive CTE: the first {n} square numbers. Return `n`, `n_squared`; sorted by n.",
      f"WITH RECURSIVE t(n) AS (SELECT 1 UNION ALL SELECT n+1 FROM t WHERE n < {n}) SELECT n, n*n FROM t ORDER BY n"))
for c in CHANNELS:
    PROBLEMS.append(P(2, f"Two-step funnel for `'{c}'` applications: CTE `a` = all applications, CTE `s` = settled ones. Return `lodged`, `settled`, `settle_pct` (1 dp).",
      f"WITH a AS (SELECT * FROM loan_application WHERE channel='{c}'), s AS (SELECT * FROM a WHERE current_status='Settled') SELECT (SELECT COUNT(*) FROM a), (SELECT COUNT(*) FROM s), ROUND(100.0*(SELECT COUNT(*) FROM s)/(SELECT COUNT(*) FROM a),1)"))
for r in (5,6,7):
    PROBLEMS.append(P(3, f"Recursion with money: a $400,000 loan at {r}.00% p.a. with $2,800 monthly repayments - the balance after 12 months (2 dp). Balance_n = balance_(n-1) * (1 + rate/12) - 2800. Return one number `balance_12`.",
      f"WITH RECURSIVE a(m, bal) AS (SELECT 0, CAST(400000 AS DOUBLE) UNION ALL SELECT m+1, bal*(1+{r}.0/100/12)-2800 FROM a WHERE m<12) SELECT ROUND(bal,2) FROM a WHERE m=12"))
PROBLEMS += [
 P(3, "Chained CTEs: `y` = loans per year; `g` = year-on-year growth % (LAG); final = years where growth exceeded 10%. `yr`, `loans`, `growth_pct` (1 dp); sorted by year.",
   "WITH y AS (SELECT year(origination_date) AS yr, COUNT(*) AS n FROM loan GROUP BY 1), g AS (SELECT yr, n, ROUND(100.0*(n/LAG(n) OVER (ORDER BY yr)-1),1) AS gr FROM y) SELECT yr, n, gr FROM g WHERE gr>10 ORDER BY 1", empty_ok=True),
 P(3, "Staff hierarchy path: recursive CTE from the top person producing each staff member's `depth` and a `path` string like `Top > Mgr > Employee` of full names. Return `staff_id`, `depth`, `path` for staff with depth 3, first 10 by staff_id.",
   "WITH RECURSIVE c AS (SELECT staff_id, 1 AS depth, CAST(full_name AS VARCHAR) AS path FROM dim_staff WHERE manager_staff_id IS NULL UNION ALL SELECT s.staff_id, c.depth+1, c.path || ' > ' || s.full_name FROM dim_staff s JOIN c ON s.manager_staff_id=c.staff_id) SELECT staff_id, depth, path FROM c WHERE depth=3 ORDER BY staff_id LIMIT 10"),
]
