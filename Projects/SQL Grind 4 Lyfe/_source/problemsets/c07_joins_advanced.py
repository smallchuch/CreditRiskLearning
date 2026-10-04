from . import P

PRIMER = r"""
## Beyond the basic join

**Anti-join** - rows in A with NO match in B ("customers who never borrowed"):
```
 SELECT ... FROM A WHERE NOT EXISTS (SELECT 1 FROM B WHERE B.k = A.k)      -- safest
 SELECT ... FROM A LEFT JOIN B ON B.k = A.k WHERE B.k IS NULL             -- also fine
```
**Semi-join** - rows in A that HAVE a match, without duplicating them: `WHERE EXISTS (...)` or `WHERE k IN (SELECT k FROM B)`.

**Self-join** - a table joined to itself under two aliases (staff -> manager, loan -> parent loan):
```
 FROM dim_staff e JOIN dim_staff m ON m.staff_id = e.manager_staff_id
```
**Range (non-equi) join** - match on `BETWEEN`, not `=`: which RBA rate applied on a date? Which policy epoch was an application assessed under?
```
 JOIN ref_serviceability_policy p ON a.application_date >= p.effective_from AND a.application_date <= p.effective_to
```
**Fan-out** - joining 1 row to N rows repeats the 1-side's numbers. Summing a loan amount after joining to `loan_borrower` double-counts joint loans:
```
 loan (1 row, $500k)  --JOIN-->  loan_borrower (2 rows)   => $500k appears twice, SUM = $1m (wrong!)
```
Fix: aggregate the many-side to the loan grain first, or count `DISTINCT`, or join to only one row (the primary).

**Slowly-changing history tables** (`loan_rate_history`, `property_valuation`): "value at date X" = the row where `effective_from <= X < effective_to` (NULL `effective_to` = still current).
"""

CONCEPT = dict(id="07_joins_advanced", title="07 - Advanced joins: anti/semi, self, range, fan-out", primer=PRIMER, problems=[
    P(1, "Customers who have never been the primary borrower on a loan (anti-join). How many? One number.",
      "SELECT COUNT(*) FROM customer c WHERE NOT EXISTS (SELECT 1 FROM loan l WHERE l.primary_customer_id=c.customer_id)"),
    P(1, "Applications that became a loan (semi-join): count of applications with a matching loan. One number.",
      "SELECT COUNT(*) FROM loan_application a WHERE EXISTS (SELECT 1 FROM loan l WHERE l.application_id=a.application_id)"),
    P(1, "Staff and their manager: `staff_id`, `full_name`, `manager_name` for staff 1-12 (LEFT JOIN so the top person shows NULL manager). Sorted by `staff_id`.",
      "SELECT e.staff_id, e.full_name, m.full_name FROM dim_staff e LEFT JOIN dim_staff m ON m.staff_id=e.manager_staff_id WHERE e.staff_id <= 12 ORDER BY 1"),
    P(2, "Number of direct reports per manager. Return `manager_name`, `reports`; sorted by `reports` descending then name.",
      "SELECT m.full_name, COUNT(*) AS n FROM dim_staff e JOIN dim_staff m ON m.staff_id=e.manager_staff_id GROUP BY m.staff_id, m.full_name ORDER BY n DESC, 1"),
    P(2, "Internal refinance chain: join each child loan to its parent (`parent_loan_id`). Return `child_loan_id`, `parent_loan_id`, `parent_closed_date`, `child_origination_date` for the first 10 children by child id. (Parent should close when the child is created.)",
      "SELECT c.loan_id, p.loan_id, p.closed_date, c.origination_date FROM loan c JOIN loan p ON p.loan_id=c.parent_loan_id ORDER BY c.loan_id LIMIT 10"),
    P(2, "Which serviceability policy epoch was each application assessed under? Range-join `loan_application.application_date` to `ref_serviceability_policy` and count applications per `policy_id`. Return `policy_id`, `applications`; sorted by `policy_id`.",
      "SELECT p.policy_id, COUNT(*) FROM loan_application a JOIN ref_serviceability_policy p ON a.application_date BETWEEN p.effective_from AND COALESCE(p.effective_to, DATE '9999-12-31') GROUP BY 1 ORDER BY 1"),
    P(2, "Fan-out demonstration. Compute (a) the true total `original_amount` across loans and (b) the total after joining `loan` to `loan_borrower` (wrong). Return one row: `true_total`, `fanned_total` both rounded to 0 dp.",
      "SELECT (SELECT ROUND(SUM(original_amount),0) FROM loan), ROUND(SUM(l.original_amount),0) FROM loan l JOIN loan_borrower b USING (loan_id)"),
    P(2, "Cross-collateral loans: loans with more than one `loan_security` row. Return `loan_id`, `securities` sorted by `loan_id`.",
      "SELECT loan_id, COUNT(*) FROM loan_security GROUP BY 1 HAVING COUNT(*) > 1 ORDER BY 1"),
    P(2, "Loans that have NEVER had a hardship arrangement: count by `loan_status`. Return `loan_status`, `loans`; sorted by `loan_status`. (Anti-join.)",
      "SELECT l.loan_status, COUNT(*) FROM loan l WHERE NOT EXISTS (SELECT 1 FROM hardship_arrangement h WHERE h.loan_id=l.loan_id) GROUP BY 1 ORDER BY 1"),
    P(2, "Which RBA cash rate applied to the bank on 2024-03-15? Range-join date to `ref_rba_cash_rate` using `bank_effective_date` to the next row's effective date. Simplest: return the `cash_rate_pct` of the latest row with `bank_effective_date <= DATE '2024-03-15'`. One number.",
      "SELECT cash_rate_pct FROM ref_rba_cash_rate WHERE bank_effective_date <= DATE '2024-03-15' ORDER BY bank_effective_date DESC LIMIT 1"),
    P(3, "Interest rate on loan 1 as at 2022-12-31 using `loan_rate_history` (`effective_from <= date` and (`effective_to` is NULL or `effective_to` > date)). Return `loan_id`, `interest_rate_pct` for loans 1-10 that were already originated by that date. Sorted by `loan_id`.",
      "SELECT h.loan_id, h.interest_rate_pct FROM loan_rate_history h WHERE h.loan_id <= 10 AND h.effective_from <= DATE '2022-12-31' AND (h.effective_to IS NULL OR h.effective_to > DATE '2022-12-31') ORDER BY 1"),
    P(3, "Rate-change history: for loans 1-15 count the rows in `loan_rate_history` whose `change_reason` is `'RBA cash rate pass-through'`. Return `loan_id`, `rate_changes`; sorted by `loan_id`. Loans with none should show 0.",
      "SELECT l.loan_id, COUNT(h.rate_history_id) FROM loan l LEFT JOIN loan_rate_history h ON h.loan_id=l.loan_id AND h.change_reason='RBA cash rate pass-through' WHERE l.loan_id <= 15 GROUP BY 1 ORDER BY 1"),
    P(3, "Co-borrower income uplift. For applications with a co-applicant, how many have the co-applicant earning more than the primary? Use `application_applicant` joined to itself on `application_id` (Primary vs Co-applicant) and `income_share_pct`. Return one number: applications where co-applicant `income_share_pct` > primary's.",
      "SELECT COUNT(*) FROM application_applicant p JOIN application_applicant c ON c.application_id=p.application_id AND c.applicant_role='Co-applicant' WHERE p.applicant_role='Primary' AND c.income_share_pct > p.income_share_pct"),
    P(3, "Application resubmissions. `resubmission_of_application_id` points to an earlier application. For resubmissions, return the previous application's `current_status` and the number of resubmissions per that status. Return `prior_status`, `resubmissions`; sorted by count descending then status.",
      "SELECT o.current_status, COUNT(*) AS n FROM loan_application r JOIN loan_application o ON o.application_id=r.resubmission_of_application_id GROUP BY 1 ORDER BY n DESC, 1"),
    P(3, "Anti-join on a pair of keys. Customers whose bureau report exists on an application but who are NOT listed in `application_applicant` for that same application (a referential gap). Count them. (Probably 0; `empty_ok`).",
      "SELECT COUNT(*) FROM credit_bureau_report b WHERE NOT EXISTS (SELECT 1 FROM application_applicant a WHERE a.application_id=b.application_id AND a.customer_id=b.customer_id)"),
    P(3, "HPI revaluation join: index the loan's property to 2025-12-31. For loans 1-10 (non-internal) get the property's state through `dim_postcode`, then the `price_index` for that state at `month_end_date` = `last_day(origination_date)` and at `2025-12-31`. Return `loan_id`, `idx_orig`, `idx_now`, `growth_pct` (1dp) = (now/orig-1)*100. Sorted by `loan_id`.",
      """SELECT l.loan_id, o.price_index, n.price_index, ROUND(100*(n.price_index/o.price_index-1),1)
FROM loan l JOIN property p ON p.property_id=l.property_id JOIN dim_postcode d ON d.postcode=p.postcode
JOIN ref_property_price_index o ON o.state=d.state AND o.month_end_date=last_day(l.origination_date)
JOIN ref_property_price_index n ON n.state=d.state AND n.month_end_date=DATE '2025-12-31'
WHERE l.loan_id <= 10 ORDER BY l.loan_id""",
      hint="Join the index table twice with different aliases (`o` for origination, `n` for now)."),
    P(3, "Valuations per property: each property can have several valuation rows. For loans 1-10 list `loan_id` and the count of valuations of the loan's property and the count that are AVM zeros (valuation_amount = 0). Return `loan_id`, `valuations`, `zero_valuations`; sorted by `loan_id`.",
      "SELECT l.loan_id, COUNT(v.valuation_id), COUNT(v.valuation_id) FILTER (WHERE v.valuation_amount=0) FROM loan l LEFT JOIN property_valuation v ON v.property_id=l.property_id WHERE l.loan_id <= 10 GROUP BY 1 ORDER BY 1"),
    P(3, "Cohort pairing: pair each Active loan on loan_id 1-6 with every policy epoch (CROSS JOIN) and show whether the loan's `origination_date` fell within that epoch. Return `loan_id`, `policy_id`, `in_epoch` (boolean); sorted by `loan_id`, `policy_id`.",
      "SELECT l.loan_id, p.policy_id, l.origination_date BETWEEN p.effective_from AND COALESCE(p.effective_to, DATE '9999-12-31') FROM loan l CROSS JOIN ref_serviceability_policy p WHERE l.loan_id <= 6 ORDER BY 1,2"),
    P(3, "Staff authority breach: loans where the assessor's `lending_authority_limit` is below the loan's `original_amount`. (Policy exceptions should explain these.) Return the count of such loans. One number.",
      "SELECT COUNT(*) FROM loan l JOIN dim_staff s ON s.staff_id=l.assessor_staff_id WHERE l.original_amount > s.lending_authority_limit"),
])
