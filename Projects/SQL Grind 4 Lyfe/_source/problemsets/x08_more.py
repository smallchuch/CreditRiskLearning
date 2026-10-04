from ._gen import *
MORE_FOR = '08_subqueries'
PROBLEMS = []
for p in EXT_PURPOSES:
    PROBLEMS.append(P(2, f"Loans with purpose `'{p}'` bigger than the average `'{p}'` loan: count them. (Scalar subquery.) One number.",
      f"SELECT COUNT(*) FROM loan WHERE purpose='{p}' AND original_amount > (SELECT AVG(original_amount) FROM loan WHERE purpose='{p}')"))
for y in YEARS:
    PROBLEMS.append(P(2, f"Loans originated in {y} with an original amount above the average for {y} loans. Count them. (Subquery filters to the same year.) One number.",
      f"SELECT COUNT(*) FROM loan WHERE {yr('origination_date',y)} AND original_amount > (SELECT AVG(original_amount) FROM loan WHERE {yr('origination_date',y)})"))
for s in STATES:
    PROBLEMS.append(P(2, f"`IN` subquery: customers whose `state` is exactly `'{s}'` and who are primary on at least one loan. Count. One number.",
      f"SELECT COUNT(*) FROM customer WHERE state='{s}' AND customer_id IN (SELECT primary_customer_id FROM loan)"))
for h in ['COVID-19 repayment deferral','Reduced repayments','Repayment deferral','Interest-only period','Term extension','Arrears capitalisation']:
    PROBLEMS.append(P(2, f"`EXISTS`: distinct primary customers with a loan that had a `'{h}'` hardship arrangement. One number.",
      f"SELECT COUNT(*) FROM customer c WHERE EXISTS (SELECT 1 FROM loan l WHERE l.primary_customer_id=c.customer_id AND EXISTS (SELECT 1 FROM hardship_arrangement h WHERE h.loan_id=l.loan_id AND h.hardship_type='{h}'))"))
for c in CHANNELS:
    PROBLEMS.append(P(3, f"Derived table: for `'{c}'` loans, the average number of loans per primary customer (2 dp) - count per customer in a subquery, then average. One number.",
      f"SELECT ROUND(AVG(n),2) FROM (SELECT primary_customer_id, COUNT(*) AS n FROM loan WHERE channel='{c}' GROUP BY 1)"))
for s in ['NSW','VIC','QLD','SA','WA']:
    PROBLEMS.append(P(3, f"Branches in `'{s}'` that originated MORE loans than the average branch (average over all branches that originated any loan). `branch_id`, `loans`; sorted by loans descending then id.",
      f"SELECT branch_id, n FROM (SELECT l.branch_id, COUNT(*) AS n FROM loan l JOIN dim_branch b USING (branch_id) WHERE b.state='{s}' GROUP BY 1) WHERE n > (SELECT AVG(n2) FROM (SELECT COUNT(*) AS n2 FROM loan WHERE branch_id IS NOT NULL GROUP BY branch_id)) ORDER BY n DESC, 1", empty_ok=True))
