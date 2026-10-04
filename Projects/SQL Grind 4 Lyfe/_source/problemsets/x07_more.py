from ._gen import *
MORE_FOR = '07_joins_advanced'
PROBLEMS = []
for y in YEARS:
    PROBLEMS.append(P(2, f"Anti-join: customers who lodged an application in {y} but have NEVER had a loan as primary. Count them. One number.",
      f"SELECT COUNT(*) FROM (SELECT DISTINCT primary_customer_id FROM loan_application WHERE {yr('application_date',y)}) a WHERE NOT EXISTS (SELECT 1 FROM loan l WHERE l.primary_customer_id=a.primary_customer_id)"))
for p in EXT_PURPOSES:
    PROBLEMS.append(P(2, f"Semi-join: how many distinct customers with a `'{p}'` loan (primary) have also been in a hardship arrangement on any of their loans? One number.",
      f"SELECT COUNT(DISTINCT l.primary_customer_id) FROM loan l WHERE l.purpose='{p}' AND EXISTS (SELECT 1 FROM loan l2 JOIN hardship_arrangement h ON h.loan_id=l2.loan_id WHERE l2.primary_customer_id=l.primary_customer_id)"))
for c in CHANNELS:
    PROBLEMS.append(P(2, f"Range join: `'{c}'`-channel applications per serviceability `policy_id` (match `application_date` to the policy's effective window). `policy_id`, `applications`; sorted by policy.",
      f"SELECT p.policy_id, COUNT(*) FROM loan_application a JOIN ref_serviceability_policy p ON a.application_date BETWEEN p.effective_from AND COALESCE(p.effective_to, DATE '9999-12-31') WHERE a.channel='{c}' GROUP BY 1 ORDER BY 1"))
for p in EXT_PURPOSES:
    PROBLEMS.append(P(3, f"Fan-out: for `'{p}'` loans, the true total `original_amount` and the total after joining to `loan_borrower` (double-counts joint loans), both 0 dp. `true_total`, `fanned_total`.",
      f"SELECT ROUND((SELECT SUM(original_amount) FROM loan WHERE purpose='{p}'),0), ROUND(SUM(l.original_amount),0) FROM loan l JOIN loan_borrower b USING (loan_id) WHERE l.purpose='{p}'"))
for d in ['2020-06-30','2021-06-30','2022-06-30','2023-06-30','2024-06-30','2025-06-30']:
    PROBLEMS.append(P(3, f"Point-in-time: the average interest rate (3 dp) in force across all loans on {d}, from `loan_rate_history` (`effective_from <= date` and `effective_to` NULL or after the date; ignore fractional keyed rates below 1). Return one number.",
      f"SELECT ROUND(AVG(interest_rate_pct),3) FROM loan_rate_history WHERE effective_from<=DATE '{d}' AND (effective_to IS NULL OR effective_to>DATE '{d}') AND interest_rate_pct>=1"))
for s in STATES:
    PROBLEMS.append(P(2, f"House price index for `'{s}'` at 2020-12-31 and 2025-12-31 side by side (join `ref_property_price_index` to itself) and growth % (1 dp). `idx_2020`, `idx_2025`, `growth_pct`.",
      f"SELECT a.price_index, b.price_index, ROUND(100*(b.price_index/a.price_index-1),1) FROM ref_property_price_index a JOIN ref_property_price_index b ON b.state=a.state WHERE a.state='{s}' AND a.month_end_date=DATE '2020-12-31' AND b.month_end_date=DATE '2025-12-31'"))
for t in ['Broker Credit','Retail Credit','Collections','Complex Lending','Credit Risk','Hardship']:
    PROBLEMS.append(P(2, f"Self-join: staff in the `'{t}'` team with their manager's name and the manager's team. `staff_id`, `full_name`, `manager_name`, `manager_team`; sorted by `staff_id`; first 10 only.",
      f"SELECT e.staff_id, e.full_name, m.full_name, m.team FROM dim_staff e JOIN dim_staff m ON m.staff_id=e.manager_staff_id WHERE e.team='{t}' ORDER BY e.staff_id LIMIT 10"))
