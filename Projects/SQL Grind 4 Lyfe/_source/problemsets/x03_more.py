from ._gen import *
MORE_FOR = '03_nulls'
PROBLEMS = []
COLS = [("customer","date_of_birth"),("loan","branch_id"),("loan","broker_id"),("loan","fixed_rate_expiry_date"),("loan","closed_date"),("loan","closure_reason"),("loan","application_id"),("loan","parent_loan_id"),
        ("loan_application","broker_id"),("loan_application","decision"),("loan_application","decline_reason_code"),("loan_application","decision_date"),("loan_application","withdrawn_date"),("loan_application","resubmission_of_application_id"),
        ("credit_bureau_report","bureau_score"),("applicant_income","verified_annual_amount"),("collections_activity","promise_amount"),("hardship_arrangement","end_date"),("complaint","resolved_date"),("dim_staff","termination_date"),("dim_staff","manager_staff_id"),("dim_branch","closed_date"),("loan","io_expiry_date"),("loan_payment","failure_reason")]
for t,c in COLS:
    PROBLEMS.append(P(1, f"NULL profile: what percentage (2 dp) of rows in `{t}` have a NULL `{c}`? Return one number. (Think about WHY they are NULL.)",
      f"SELECT ROUND(100.0*COUNT(*) FILTER (WHERE {c} IS NULL)/COUNT(*),2) FROM {t}"))
for ch in CHANNELS:
    PROBLEMS.append(P(2, f"For `'{ch}'` loans: how many have a NULL `branch_id` and how many have a NULL `broker_id`? Return `null_branch`, `null_broker`.",
      f"SELECT COUNT(*) FILTER (WHERE branch_id IS NULL), COUNT(*) FILTER (WHERE broker_id IS NULL) FROM loan WHERE channel='{ch}'"))
for p in EXT_PURPOSES:
    PROBLEMS.append(P(2, f"For `'{p}'` loans: the average `io_period_months` with NULLs treated as 0 (`COALESCE`), and the average ignoring NULLs - both 2 dp. Return `avg_coalesced`, `avg_plain`. (If both are equal, no NULLs exist - say why.)",
      f"SELECT ROUND(AVG(COALESCE(io_period_months,0)),2), ROUND(AVG(io_period_months),2) FROM loan WHERE purpose='{p}'"))
PROBLEMS += [
 P(3, "`COUNT(*)` vs `COUNT(col)`: for each `decision` status in `loan_application` (including NULL shown as `'(none)'`) return `decision_label`, `apps`, `with_decline_code` (`COUNT(decline_reason_code)`). Sorted by `decision_label`.",
   "SELECT COALESCE(decision,'(none)') AS d, COUNT(*), COUNT(decline_reason_code) FROM loan_application GROUP BY 1 ORDER BY 1"),
 P(3, "`IS NOT DISTINCT FROM`: count loans whose `branch_id` IS NOT DISTINCT FROM the branch on the originating application (join on `application_id`). One number.",
   "SELECT COUNT(*) FROM loan l JOIN loan_application a ON a.application_id=l.application_id WHERE l.branch_id IS NOT DISTINCT FROM a.branch_id"),
 P(3, "NULLS LAST: the 5 customers with the latest `date_of_birth` (youngest), ties by `customer_id`, where NULL DOBs must NOT appear first. Return `customer_id`, `date_of_birth`.",
   "SELECT customer_id, date_of_birth FROM customer WHERE date_of_birth IS NOT NULL ORDER BY date_of_birth DESC, customer_id LIMIT 5"),
 P(3, "Average of averages trap: average `bureau_score` across ALL reports (2 dp) vs the average of per-`enquiries_last_12m` averages (2 dp). Return `overall_avg`, `avg_of_avgs`.",
   "SELECT (SELECT ROUND(AVG(bureau_score),2) FROM credit_bureau_report), (SELECT ROUND(AVG(a),2) FROM (SELECT AVG(bureau_score) AS a FROM credit_bureau_report GROUP BY enquiries_last_12m))"),
 P(3, "Coalesce chain: for loans 1-10 show the first non-NULL of `closed_date`, `fixed_rate_expiry_date`, `maturity_date` as `key_date`. Sorted by `loan_id`.",
   "SELECT loan_id, COALESCE(closed_date, fixed_rate_expiry_date, maturity_date) FROM loan WHERE loan_id<=10 ORDER BY loan_id"),
]
