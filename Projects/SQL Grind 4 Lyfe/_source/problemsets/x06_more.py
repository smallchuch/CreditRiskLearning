from ._gen import *
MORE_FOR = '06_joins_basic'
PROBLEMS = []
for p in EXT_PURPOSES:
    PROBLEMS.append(P(1, f"For `'{p}'` loans: the 3 `product_name`s with the most loans. `product_name`, `loans`; most first, ties by name.",
      f"SELECT pr.product_name, COUNT(*) AS n FROM loan l JOIN dim_product pr USING (product_id) WHERE l.purpose='{p}' GROUP BY 1 ORDER BY n DESC, 1 LIMIT 3"))
for c in CHANNELS:
    PROBLEMS.append(P(2, f"Loans written via `'{c}'` by property state: `state`, `loans`; sorted by `state`. (Join loan -> property -> dim_postcode.)",
      f"SELECT d.state, COUNT(*) FROM loan l JOIN property p ON p.property_id=l.property_id JOIN dim_postcode d ON d.postcode=p.postcode WHERE l.channel='{c}' GROUP BY 1 ORDER BY 1"))
for s in ['NSW','VIC','QLD','SA','WA']:
    PROBLEMS.append(P(2, f"The 5 branches in `'{s}'` that originated the most loans: `branch_name`, `loans`; most first, ties by name.",
      f"SELECT b.branch_name, COUNT(*) AS n FROM loan l JOIN dim_branch b USING (branch_id) WHERE b.state='{s}' GROUP BY b.branch_id, b.branch_name ORDER BY n DESC, 1 LIMIT 5"))
for y in YEARS:
    PROBLEMS.append(P(2, f"Settled applications lodged in {y}: average primary-applicant bureau score by `channel` (0 dp). `channel`, `avg_score`; sorted by channel.",
      f"SELECT a.channel, ROUND(AVG(b.bureau_score),0) FROM loan_application a JOIN credit_bureau_report b ON b.application_id=a.application_id AND b.customer_id=a.primary_customer_id WHERE a.current_status='Settled' AND {yr('a.application_date',y)} GROUP BY 1 ORDER BY 1"))
for y in range(2019,2026):
    PROBLEMS.append(P(2, f"Loans originated in {y} by assessor `team` (join `dim_staff`). `team`, `loans`; sorted by team.",
      f"SELECT s.team, COUNT(*) FROM loan l JOIN dim_staff s ON s.staff_id=l.assessor_staff_id WHERE {yr('l.origination_date',y)} GROUP BY 1 ORDER BY 1"))
for y in (2019,2022,2025):
    PROBLEMS.append(P(3, f"LEFT JOIN keeps all 15 products: loans per product originated in {y}, with 0 for products with none. `product_id`, `loans`; sorted by product_id.",
      f"SELECT p.product_id, COUNT(l.loan_id) FROM dim_product p LEFT JOIN loan l ON l.product_id=p.product_id AND {yr('l.origination_date',y)} GROUP BY 1 ORDER BY 1"))
for h in ['COVID-19 repayment deferral','Reduced repayments','Repayment deferral','Interest-only period','Term extension','Arrears capitalisation']:
    PROBLEMS.append(P(2, f"Hardship type `'{h}'`: arrangements by loan `purpose` (join `loan`). `purpose`, `arrangements`; sorted by purpose.",
      f"SELECT l.purpose, COUNT(*) FROM hardship_arrangement h JOIN loan l USING (loan_id) WHERE h.hardship_type='{h}' GROUP BY 1 ORDER BY 1"))
PROBLEMS += [
 P(3, "Applications to loans to customers: for loans 1-10 return `loan_id`, the primary customer's `segment`, and the product `occupancy`. Three joins. Sorted by `loan_id`.",
   "SELECT l.loan_id, c.segment, p.occupancy FROM loan l JOIN customer c ON c.customer_id=l.primary_customer_id JOIN dim_product p ON p.product_id=l.product_id WHERE l.loan_id<=10 ORDER BY 1"),
 P(3, "Join four tables: for 2025 settled loans, total original amount by customer `segment` and property `state`; `segment`, `state`, `amount` (0 dp). Sorted by segment, state.",
   "SELECT c.segment, d.state, ROUND(SUM(l.original_amount),0) FROM loan l JOIN customer c ON c.customer_id=l.primary_customer_id JOIN property p ON p.property_id=l.property_id JOIN dim_postcode d ON d.postcode=p.postcode WHERE l.origination_date >= DATE '2025-01-01' GROUP BY 1,2 ORDER BY 1,2"),
 P(3, "Complaints with their branch: count complaints (with a loan) by branch region (loan -> branch; drop loans without a branch). `region`, `complaints`; sorted by complaints descending then region.",
   "SELECT b.region, COUNT(*) AS n FROM complaint c JOIN loan l USING (loan_id) JOIN dim_branch b ON b.branch_id=l.branch_id GROUP BY 1 ORDER BY n DESC, 1"),
]
